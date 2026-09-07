---
type: decision
schema_version: 1
scope: project
created: "2026-09-02"
updated: "2026-09-02"
area: "[[Echo Forge]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[xKoRx/symphony]]"
entities:
  - "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
related:
  - "[[2026-09-03-orphan-mt5-after-cancel]]"
  - "[[2026-09-03-echo-forge-worker-execution-model-v1]]"
aliases:
  - ECHO_FORGE_WORKER_LIFECYCLE_MT5_ORPHAN_PLAN
confidence: verified
source_session: ECHO-FORGE-WORKER-LIFECYCLE-AND-MT5-ORPHAN-PLAN-NORMAL
load_policy: when_project_loaded
indexable: true
index_priority: high
tags:
  - kind/decision
  - scope/project
  - project/echo-forge
  - tech/temporal
  - tech/mt5
---

# 2026-09-03-echo-forge-worker-lifecycle-mt5-orphan-plan

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Contexto

- Symphony `bac1d6ef93cd4714c1af4f2e44516bea44642e80`, SDK authority `c85594440f6755443ceb97ec4e333cd0ddb5b0ed`, Temporal Go SDK `v1.44.1`, release actual `0.2.86`, release objetivo `0.2.87`.
- Incidente `d7693ebe-4ea8-4c10-a65e-c45d676ac788`: Generic canceló con ocho children MT5; siete cancelados y uno terminado por parent close policy; `terminal64.exe` salió y `metatester64.exe` sobrevivió temporalmente.

## Decisión

- RCA corregido: se retira `WORKER_LOCAL_CONCURRENCY_CONTRACT_VIOLATION` para SQX. El SDK normaliza `MaxConcurrentActivityExecutionSize == 0` a `1`; SQX y MT5 tienen concurrencia efectiva `1`. El modelo `ECHO_FORGE_WORKER_EXECUTION_MODEL_V1` queda intacto y no existe Slice A.
- Temporal: `MT5ArtifactChildWorkflowOptions` debe usar, en la rama versionada nueva, `ParentClosePolicy: enums.PARENT_CLOSE_POLICY_REQUEST_CANCEL` y `WaitForCancellation: true`. Los children se lanzan con el contexto padre vivo, para que la cancelación solicite cancel a cada child.
- Wait-all: `collectMT5ArtifactChildren` debe observar y latchear la cancelación, cambiar después a `workflow.NewDisconnectedContext(ctx)` sólo para esperar, drenar todos los futures ya lanzados y devolver `CanceledError` al final. El primer child cancelado nunca permite retorno temprano; errores de infraestructura conservan el mapeo actual y una cancelación sigue siendo resultado válido.
- Replay: envolver el cambio de opciones en `workflow.GetVersion(ctx, "mt5-artifact-child-cancel-v1", workflow.DefaultVersion, 1)`. `DefaultVersion` reproduce las opciones legacy omitidas; versión `1` emite las opciones explícitas. No usar gate operativo ni Worker Versioning.
- Windows: la ownership pertenece a `sqx/adapters/cmd-executor`. Cada invocación crea un Job Object, configura `JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE`, crea el proceso raíz con `CREATE_SUSPENDED`, asigna el proceso al job y recién entonces reanuda el thread. El executor no retorna hasta que el proceso raíz terminó y el job reporta cero procesos activos.
- Cancelación y timeout terminan el Job Object completo y esperan cero procesos antes de responder. La finalización normal no mata descendants por el solo hecho de que terminó `terminal64`; espera su salida natural y sólo cierra handles cuando el job está vacío.
- Corregir `context.Canceled` para que preserve `errors.Is(err, context.Canceled)` y no se clasifique como timeout. Es requerido en 0.2.87 porque el timeout es transitorio/retryable y la clasificación actual puede provocar retry u outcome incorrecto; `DeadlineExceeded` sigue siendo timeout.
- El barrier físico del executor ya garantiza retry/workspace safety con concurrencia efectiva uno: no agregar lock, semaphore ni subsistema de cleanup. `ArtifactRunner` y su cleanup existente quedan después del retorno del comando.

## Rationale

- `ParentClosePolicy=TERMINATE` y el retorno temprano del collector explican el child `Terminated`; `WaitForCancellation` de la activity no puede actuar si el child workflow ya murió.
- Un `exec.Cmd.Process.Kill()` sólo afecta al proceso directo. Job Objects son la primitive Windows de ownership por invocación y protegen también los descendants sin matar procesos por nombre o PID global.
- `os/exec` no expone limpiamente el primary thread suspendido para resolver la race; el constructor Windows debe usar `golang.org/x/sys/windows.CreateProcess` y conservar `ProcessInformation`.
- El root puede salir antes que `metatester64` durante una finalización normal. El contador del job, no el exit del root, define el estado físico terminal.

## Consecuencias

- El fix se divide en dos slices bisectables B (Temporal) y C (Windows), pero ambos son prerequisito de la misma release `0.2.87`; no hay certificación física intermedia.
- El cambio Windows debe conservar el camino Unix actual sin syscalls Windows en builds Linux. No se modifica worker main, SDK, ActivityGate, registration, topology, stager/deployer ni dominio MT5.
- La verificación requiere tests Temporal focalizados, tests Linux del executor, cross-compile Windows y tests de integración en Windows real. La smoke cancellation física con un FlowRun disposable precede C3.

## Archivos permitidos

- `sqx/workflows/mt5_artifact_workflow.go`
- `sqx/workflows/mt5_artifact_workflow_test.go`
- `sqx/workflows/generic_workflow.go`
- `sqx/workflows/generic_mt5_child_cancel_test.go` (nuevo)
- `sqx/adapters/cmd-executor/cmd_executor.go`
- `sqx/adapters/cmd-executor/termination_windows.go` (nuevo, `//go:build windows`)
- `sqx/adapters/cmd-executor/termination_unix.go` (nuevo, `//go:build !windows`, preserva semántica Unix)
- `sqx/adapters/cmd-executor/termination_windows_test.go` (nuevo, `//go:build windows`)
- `sqx/adapters/cmd-executor/sqcli_executor_test.go`
- `go.mod`, sólo para promover el ya fijado `golang.org/x/sys v0.40.0` a dependencia directa si el import lo exige; no cambiar versión ni `go.sum`.

## Algoritmo exacto de wait-all

- Mantener el orden determinista de los futures y lanzar todos como hoy con el contexto padre.
- Para cada future, llamar `Get` con `ctx` mientras no haya cancelación latcheada. Si devuelve `temporal.IsCanceledError`, marcar `cancelObserved`, crear inmediatamente `drainCtx, drainCancel := workflow.NewDisconnectedContext(ctx)` y repetir `Get` del mismo future con `drainCtx`.
- Para los futures restantes usar siempre `drainCtx`; nunca retornar al primer cancel. `drainCancel` queda en `defer`.
- No incrementar `failed` ni mapear como infraestructura un child cancelado. Mapear errores no-cancelables con `MapExhaustedArtifactError` como hoy. Después de drenar todos, devolver `nil, failed, temporal.NewCanceledError()` si hubo cancelación; sin cancelación, conservar resultados/errores actuales.
- El contexto desconectado se crea después de que el contexto padre ya disparó la solicitud de cancelación registrada por el SDK. No se usa para lanzar children y por tanto no corta la propagación.

## Child workflow interno

- `MT5CompileArtifactWorkflow` y `MT5BacktestArtifactWorkflow` no requieren lógica adicional: ya esperan su activity y las opciones de activity tienen `WaitForCancellation: true`. El cambio mínimo es mantener ese contrato y no devolver terminalidad antes de que la activity responda a la cancelación.

## Contrato Job Object y handles

- Crear job y límites antes del process; crear pipes heredables; llamar `CreateProcess(..., CREATE_SUSPENDED, STARTF_USESTDHANDLES)`; `AssignProcessToJobObject`; `ResumeThread`.
- En start/assign/resume failure, nunca reanudar un proceso no asignado: terminar el root suspendido o el job ya asignado, esperar root y cero activos, cerrar pipes, thread, process y job, y devolver error.
- Tras resume exitoso, el padre cierra write ends, conserva process/job handles y cierra el thread handle. Wait normal exige root terminado y luego `QueryInformationJobObject` hasta `ActiveProcesses == 0`; esperar readers antes del retorno; cerrar process y job al final.
- Cancel/deadline llama `TerminateJobObject`, espera root y cero activos, drena output y cierra handles. Fallos de wait/query/terminate no permiten reportar éxito mientras no se pueda probar que el job está vacío; se intenta kill/drain y se devuelve error sólo con la evidencia física correspondiente.
- No configurar silent breakaway ni usar `taskkill /IM`, `Stop-Process`, kill-by-image-name o enumeración global. Si el proceso ya pertenece a un job incompatible y `AssignProcessToJobObject` falla, fail closed y corregir la configuración del servicio antes de desplegar.

## Tests obligatorios

- Temporal T1/T2: aserción de `REQUEST_CANCEL` y `WaitForCancellation=true`; T3: cancelación del padre solicita cancelación al child; T4/T5: primer cancel no retorna y todos los futures llegan a terminal; T6: seal sólo después del drain; T7: normal unchanged; T8: infraestructura conserva mapping; T9: replayer cubre history legacy y marker versión 1.
- Windows W1: helper parent/child/grandchild; W2: evidencia controlada de supervivencia con kill directo; W3/W4: cancel y timeout drenan todo el job; W5: outsider sobrevive; W6: normal completion espera salida natural y no mata por root exit; W7: assign failure fail-closed; W8: ejecuciones repetidas sin leaks de procesos/handles. Incluir hooks para start/resume/wait failures cuando el entorno lo permita.
- Retry/workspace R1: Execute no retorna mientras un descendant owned siga vivo; R2: la concurrencia efectiva uno deriva que no inicia el segundo intento antes del drain, sin semaphore test; R3: la limpieza existente ocurre después del retorno drenado, sin nuevo cleanup subsystem.

## Alternativas descartadas

- Slice A de concurrency: rechazada por la autoridad SDK y el modelo congelado.
- `NewDisconnectedContext` antes de solicitar cancelación: rechazado porque impediría propagar la cancelación a children.
- `exec.CommandContext` más `Process.Kill`, `taskkill`, image-name kill o PID global: rechazado por no poseer el árbol.
- Matar descendants en normal completion: rechazado porque MT5 puede mantener `metatester64` vivo brevemente de forma legítima.
- Lock/semaphore adicional, cambios Unix, ActivityGate, worker registration, task queues, SDK o cambios de dominio: fuera de alcance y redundantes.
