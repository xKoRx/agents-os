---
type: resource
schema_version: 1
status: active
area: "[[Echo]]"
sources:
  - "[[Echo Forge — Factory V2 Completion]]"
  - "[[2026-09-06-echo-forge-mt5-execution-model-v2]]"
  - "[[2026-09-03-mt5-artifact-timeout-authority]]"
  - "[[Echo Forge — F-01 Canonical Generation Concurrency Contract]]"
  - "[[Echo Forge — F-02 Finalist Model V2 Contract]]"
last_verified: "2026-09-08"
confidence: verified
aliases:
  - F-03 SPEC
  - SQX long-running contract
  - Echo Forge F-03
  - elapsed wall-clock not business failure
related:
  - "[[Echo Forge — F-03 SQX long-running]]"
  - "[[Echo Forge — Factory V2 Completion]]"
entities:
  - "[[Echo Forge]]"
  - "[[xKoRx/symphony]]"
tags:
  - kind/resource
  - area/echo
  - project/echo-forge
created: "2026-09-08"
updated: "2026-09-08"
---

# Echo Forge — F-03 SQX Long-Running Contract

Esta Resource es el contrato técnico de `F-03 — SQX Long-Running`. Define qué debe quedar cierto. La ejecución vive en [[Echo Forge — F-03 SQX long-running]]. No es un tutorial. El único principio compartido con B1B/B2 CLOSED es: **wall-clock sano no es motivo de failure de negocio**. No se copia Slot Pool, allocator, takeover, fencing ni ownership cross-host.

Baseline de source: `xKoRx/symphony@e50cb7ea47e03ff0cff1930f09f2e0c0fba00b48` (`origin/master` verificado 2026-09-08, worktree CLEAN). Agents OS: vault local **sin** `.git`; lookup de SHA live **degraded**; última authority durable registrada en journal: `f1070bec27db3ca415fe24f3c3576139674b7e09` (E-01 S0, citada por TOP F-02). No se inventa SHA de vault.

`DATABASE MIGRATION: NONE`. Timeouts, heartbeats y cancel viven en Temporal options, `context` y el proceso `sqcli`. Recovery ya usa `StageExecutionRef` / producer outputs existentes (migrations 001–014). No hay columna ni CHECK de timeout de negocio.

## Síntesis vigente

### Problema

Un cómputo SQX sano (Builder / Optimizer / WFM durable y superficies equivalentes) puede morir porque el reloj avanzó. Eso contradice el objetivo frozen: `elapsed wall-clock != business failure`.

El kill no es un solo número de Temporal. Hay al menos tres capas: options de activity/child workflow, `context.WithTimeout` dentro de activities, y `exec.CommandContext` / terminate del `sqcli`. Campaign stop/admission **no** es kill del job; no se rediseña.

### Veredicto central

Quitar deadlines de negocio que convierten duración en FAILED. Conservar heartbeat como liveness real, retry/recovery existentes, cancel explícito cooperativo acotado al árbol del job, y serialización SQX por máquina/databank (contrato actual: un CLI físico sobre el databank del proyecto; no paralelizar).

Techo Temporal finito: **PLATFORM_CEILING** local `sqxActivityTechnicalCeiling = time.Duration(1<<63-1) - time.Second` (mismo hecho de representación ya usado en B1B como `mt5ActivityTechnicalCeiling`). Se reusa el hecho de API, **no** se importan paquetes ni semántica MT5. `ScheduleToCloseTimeout` de cómputo SQX queda **cero** (no derivado de días de negocio).

## Mapa de kill paths (source @ e50cb7e)

Cada límite tiene exactamente una categoría.

### BUSINESS_DEADLINE — REMOVE

| Límite | Dónde | Qué mata | Acción |
|---|---|---|---|
| `StartToCloseTimeout: 10 * 24 * time.Hour` | `genericActivityOptions`, `runGenericSQXWorkflow` ActivityOptions duplicadas, `GroupSQXWorkflow` ActivityOptions | Activity de proyecto/compute sana a los 10d | Reemplazar por `sqxActivityTechnicalCeiling` |
| `ScheduleToCloseTimeout: 20 * 24 * time.Hour` | mismos tres sitios Generic/Group | Suma de attempts (retry infinito) a los 20d | Poner `0` (unset) |
| `StartToCloseTimeout: 5 * 24 * time.Hour` + `ScheduleToCloseTimeout: 10 * 24 * time.Hour` | `mainActivityOptions` en `adaptive_workflow.go` | Adaptive compute a 5d / 10d total | Misma regla Generic (ceiling + ScheduleToClose 0) si el archivo permanece; Adaptive **no** está registrado en `sqx/cmd/sqx-worker` |
| `WorkflowRunTimeout: 30 * 24 * time.Hour` | child `GroupSQXWorkflow` (lote secuencial y fan-in early ranking) | Child group sano a 30d | Omitir / `0` (unlimited run) |
| `context.WithTimeout(ctx, 10*time.Minute)` si el ctx no trae deadline | `WFMDurableExportActivity.Execute` | Export WFM físico sano a 10m pese a heartbeat 6s | Eliminar el timeout; el ctx de Temporal (heartbeat + cancel) basta |
| `ensureApplyDeadline` → `10*time.Minute` | `durable_apply_selected_run.go` | Apply selected run (incluye `ExecuteAndWait` SQX) a 10m | Eliminar el deadline sintético |
| `StartToCloseTimeout: 10d` / `ScheduleToCloseTimeout: 20d` | `internal/workflows/main.go` `SQXJobWorkflow` / `SQXGroupWorkflow` | Legado aún registrado por `internal/tasks/sqx_worker_refactored.go` | Misma regla si el binario legado sigue compilable; no dejar un segundo killer |
| `strings.Contains(outputStr, "Timeout reached")` → error | `pkg/sqxutils/executor.go` | Stdout de espera sqcli como failure de negocio | No clasificar elapsed wait como failure en ningún path invocado; hot path productivo es `executor-sqx` (no parsea esa frase) |
| `SQXConfig.SQCLITimeoutMs: 10000` default | `sqx/core/config/config.go` | Landmine: no está cableado en `sqx-worker` (`cmdexecutor.New` sin `WithTimeout`) | Prohibido cablear `WithTimeout` al executor de compute SQX; test de no-regresión |

### TECHNICAL_LIVENESS — KEEP/ADJUST

| Límite | Autoridad | Evento que prueba pérdida | Retry/recovery | UNKNOWN / ambiguous |
|---|---|---|---|---|
| `HeartbeatTimeout: 2 * time.Minute` | Temporal ActivityOptions Generic/Group/Adaptive | Ausencia de heartbeat >2m (worker muerto, activity stuck sin `RecordHeartbeat`) | `RetryPolicy.MaximumAttempts=0` (infinito, transiente); recovery durable existente | Un heartbeat timeout **no** es elapsed sano. Retry nuevo attempt. No reattach de proceso SQX (no hay takeover). Si hay Evaluation/producer sellados → skip físico; si StageExecution RUNNING sin sello → reiniciar físico |
| Intervalo heartbeat 6s (`sqx/activity/heartbeat_seconds`) | ETCD + `instrumentation.StartHeartbeat` / `StartHeartbeatWithDetails` | Primer heartbeat inmediato; ticker 6s | N/A (emisión) | Si ETCD ausente: default 6s. Debe permanecer ≪ 2m |
| `WaitForCancellation: true` | ActivityOptions compute | Cancel de workflow/activity | Temporal no reintenta CanceledError **si** se propaga como cancel, no como timeout de aplicación | Hoy `cmd_executor.classifyError` mapea `context.Canceled` a `ErrorTypeTimeout` — **ADJUST**: cancel explícito ≠ timeout |
| `DefaultTerminationPolicy` SIGTERM luego SIGKILL 5s | `cmd-executor` sobre el PID de `sqcli` | Cancel/deadline del ctx de Execute | N/A | ADJUST: matar el **árbol** (process group Unix del `sqcli` de **este** Execute). No Job Object MT5. No `taskkill` global. Hijos Java de otro job / worker / sibling no se tocan |
| `exec.CommandContext(ctx)` | `process_nonwindows.go` / utils | Mismo ctx de activity | Igual | El ctx de compute **no** debe llevar deadline de negocio |

### PLATFORM_CEILING — JUSTIFY

Temporal exige `StartToCloseTimeout` finito y >0. El techo de representación usado en este repo es `time.Duration(1<<63-1) - time.Second`. F-03 fija `sqxActivityTechnicalCeiling` a ese valor en `sqx/workflows` **sin importar** `mt5_artifact_workflow.go`. Semantics: no es timeout de negocio; un job sano no debe terminar por este techo. Tests: igualdad exacta al techo; `ScheduleToCloseTimeout==0`; ningún test de compute pinnea 10d/20d/5d/30d/10m como éxito.

`WorkflowExecutionTimeout` / `WorkflowRunTimeout` de Generic: hoy no se setean en el parent Generic (0). Conservar 0. Child group: quitar 30d.

No dejar `365d` ni otro número arbitrario de NORMAL.

### KEEP (fuera del kill de compute largo; no confundir)

| Límite | Por qué no es F-03 compute |
|---|---|
| `forgeCampaignActivityOptions` `StartToCloseTimeout: 30s` | Control plane (start/resolve/finalize/cancel DB). No ejecuta sqcli. Conservar. Campaign `MaxWaves` / stop policy = budget/admission, **no** mata un Generic sano por wall-clock |
| `context.WithTimeout(..., 30s)` FlowRun start/seal, ForgeCampaign activities, watcher intake | I/O corto |
| `WithTimeout(..., 2*time.Minute)` rank/reconcile/score/seal WFM/select/classify | Activities cortas de persistencia/score, no CLI Builder/Optimizer/WFM físico |
| `maintenance/timeout_ms` + `cmdexecutor.WithTimeout` | Maintenance executor, no compute SQX |
| MT5 `mt5ActivityTechnicalCeiling` / Slot Pool / `tasks[].mt5.timeout` ignorado | B1B/B2 CLOSED. No-touch |
| Cleanup databanks hook | Determinismo de retry, no timeout |

## Cancel contract

No se rediseña B2.

**Quién puede cancelar**

- Operador Temporal (`CancelWorkflow`) sobre el WorkflowID del Generic (o Campaign padre).
- `ForgeCampaignWorkflow` ante `ctx.Err()` canceled: `PARENT_CLOSE_POLICY_REQUEST_CANCEL` + `WaitForCancellation` del child Generic (ya existe).
- Drain/PENDING del worker: no admite activities nuevas; jobs BUSY siguen; no es cancel de negocio.

**Cómo llega a Activity / proceso**

1. Cancel del workflow → activities con `WaitForCancellation=true` reciben ctx canceled.
2. `execute_sqx` / `ExecuteAndWait` → `CommandExecutor.Execute` → `effectiveCtx.Done()` → `process.terminate`.
3. ADJUST: process **group** del `sqcli` de esa invocación (padre + descendientes Java de ese start). SIGTERM entonces SIGKILL acotado a ese grupo.

**Qué debe morir**

- Árbol del job objetivo: Generic cancelado, sus Group children, activities `project` / WFM export / apply de ese árbol, proceso `sqcli` y descendientes de **esa** ejecución.

**Qué NO debe morir**

- Otros Generic/Campaign en el mismo worker o cluster.
- Worker `sqx-worker`, Temporal, ETCD, Postgres, MinIO.
- Databank/proceso de un job distinto.
- Slot Pool / procesos MT5 (no-touch).
- Control-plane Campaign salvo el child cuyo padre canceló.

**Estado durable final**

- FlowRun: `LifecycleCancelled` vía `sealFlowRun` (ya distingue cancel de fail).
- StageExecution FAILED/CANCELLED: fail-closed; **no** se recupera como éxito (`project_stage_recovery.go`).
- Campaign: `ForgeCampaignCancelActivity` en disconnected context (ya existe).

**Retry / no-retry**

- Cancel explícito: **no retry**. Prohibido reetiquetar `context.Canceled` como `ErrorTypeTimeout` (hoy sí ocurre en `classifyError`).
- Heartbeat timeout / crash de worker: retry técnico según policy existente (`MaximumAttempts=0`).

**Cleanup databank/workspace**

- Pre-hook `cleanup_databanks` corre al **inicio** del siguiente attempt físico, no como destructor global al cancel.
- Cancel a mitad de SQX: databank del **proyecto de ese job** puede quedar sucio; el próximo start del mismo proyecto limpia. No limpiar databanks de otros proyectos. No inventar pool.

**Cancel vs completion/recovery**

- Si el físico ya selló Evaluation/producer output y luego llega cancel: autoridad durable gana; no publicar de nuevo; seal de FlowRun sigue cancel si el workflow fue cancelado antes del seal terminal — `sealFlowRun` ya usa disconnected context.
- Si cancel coincide con completion exitoso de activity: Temporal resuelve; no reinterpretar elapsed. Recovery en retry no debe tratar cancel como timeout recuperable.

**Aislamiento**

- Cancelar un job mata **sólo su árbol**. Group children de Generic deben usar `ParentClosePolicy=REQUEST_CANCEL` + `WaitForCancellation=true` (hoy el child group **no** setea policy → default TERMINATE). ADJUST cooperativo, no Terminate silencioso. No copiar `collectMT5ArtifactChildren`.

## Recovery contract

Autoridades existentes; no se inventa reattach.

**Identidad estable en retry**

- `StageExecutionRef` (intent: FlowRun + task_path + subject + inputs). Attempt de Temporal **no** es identidad de negocio.
- Builder: `BuilderRecovered` certificado, intacto.
- Retester/Optimizer/FinalReretester: `PhysicalExecutionRecovered` según `project_stage_recovery.go`.

**Outputs reutilizados**

- COMPLETED + 0 EvaluationRefs sellados → empty recovered, read-only, no re-SQX.
- COMPLETED + 1 EvaluationRef sellado → carrier exacto, no re-SQX.
- RUNNING/PENDING + Evaluation ya sellada → db_register idempotente, no re-SQX.
- RUNNING/PENDING sin Evaluation → pipeline físico autoritativo (reinicia CLI).
- FAILED/CANCELLED → fail closed.

**Reanudar vs reiniciar**

- Reanudar = skip físico cuando hay sello durable.
- Reiniciar = nuevo `ExecuteAndWait` sobre el mismo StageExecutionRef. **No** hay reattach a un `sqcli` vivo (eso sería takeover MT5).

**Output parcial**

- Producer write-once / claim namespace existentes. Collect+upload no marcan COMPLETED sin Evaluation/producer seal. F-03 no relaja write-once.

**Crash/liveness vs elapsed**

- Liveness loss = heartbeat ausente >2m o proceso muerto sin cancel explícito → retry técnico.
- Elapsed sano = prohibido como FAILED. Tras F-03 no debe existir `DeadlineExceeded` de negocio en compute SQX.
- Cancel = `Canceled`, durable CANCELLED, no retry.

Si faltara autoridad para “reattach a sqcli huérfano”: **no se inventa**. Gap explícito: huérfanos Java se matan sólo si pertenecen al process group del job cancelado/reemplazado; un huérfano sin grupo queda deuda operativa, no Slot Pool.

## Observabilidad

Duration se mide; **no** es gate de failure.

Mínimo (reusar lo existente):

| Señal | Superficie actual | F-03 |
|---|---|---|
| Elapsed duration | `symphony.sqx.sqcli.duration_ms` en `core/utils` y `pkg/sqxutils`; `ExecResult.DurationMs`; `HeartbeatDetails.ElapsedMs` en WFM | Emitir duration en el hot path `executor-sqx` / `cmd_executor` (ya loguea `duration_ms`). Project activity: pasar de heartbeat string estático a `StartHeartbeatWithDetails` (elapsed) **sin** usar elapsed para fail |
| Heartbeat / liveness | `StartHeartbeat` 6s; Temporal HeartbeatTimeout 2m | Conservar. Tests análogos a WFM (`wfmHeartbeatTimeoutAnalog`) |
| Cancel | `sealFlowRun` → `LifecycleCancelled`; Campaign cancel activity | Conservar; logs/span ya existentes. No nueva métrica de cardinalidad por ID |
| Retry / recovery | `activity.GetInfo.Attempt` en HeartbeatDetails; flags `BuilderRecovered` / `PhysicalExecutionRecovered` | Conservar |
| Completion | FlowRun seal Completed/Failed; `sqx_execution_success` | Conservar |

Bundles: `telemetry.SQX` ya usado. Prohibido métrica con nombre dinámico por RequestID.

## Serialización SQX (conservar, no paralelizar)

`sqx-worker` **no** setea `MaxConcurrentActivityExecutionSize` (default Temporal alto). El contrato físico vigente es un databank de proyecto (`custom` / exporter fijo) + `cleanup_databanks` + file lock en WFM/apply. F-03 **no** introduce MaxConcurrent como allocator. F-03 **no** paraleliza SQX por máquina/databank. Cancel de un job no desbloquea un sibling corrompiendo el mismo databank a mitad de CLI: el sibling espera el databank como hoy.

## Certification gates

1. **SOURCE:** grep/assert: ningún `StartToCloseTimeout` de 5d/10d, ningún `ScheduleToCloseTimeout` 10d/20d, ningún `WorkflowRunTimeout` 30d, ningún `WithTimeout(10*time.Minute)` en WFM export ni `ensureApplyDeadline` 10m, ningún `WithTimeout` en `cmdexecutor.New` de `sqx/cmd/sqx-worker`. Builder/Optimizer/WFM sano no tiene business deadline restante.
2. **CONTRACT:** retry/recovery no cambia por duración. Tests: heartbeat timeout sigue retryable; StageExecutionRef estable; sealed output no se republica; elapsed no produce `ErrorTypeTimeout` de negocio. Dual: recovery tests existentes verdes.
3. **CANCEL:** cancel explícito de un Generic mata sólo su árbol (children group REQUEST_CANCEL, sqcli process group). Sibling workflow / worker / otro databank viven. `Canceled` ≠ `ErrorTypeTimeout`. Cleanup no borra workspace ajeno.
4. **LIVENESS:** stop heartbeat → activity falla por HeartbeatTimeout → retry/recovery. Analogía ya existente en `wfm_durable_export_activity_test.go` (2s vs 2m).
5. **PHYSICAL:** procedimiento (ejecuta implementación/cert, no TOP):
   - Worker SQX de lab (Hera o Zeus) con binario del commit F-03.
   - Job real: WFM durable export **o** Builder/Optimizer sobre un proyecto que hoy moriría al límite viejo **ejercible**. El killer físico más corto es WFM/apply **10m**; el Temporal 10d no es el procedimiento PHYSICAL primario.
   - Arrancar el job, dejar wall-clock **> 10 minutos** (límite viejo WFM/apply) con heartbeats vivos; debe COMPLETED o seguir RUNNING, nunca FAILED por timeout.
   - Cancelar **otro** Generic (o el mismo tras snapshot de evidencia) y probar: proceso árbol objetivo muerto; worker vivo; FlowRun CANCELLED; sibling no cancelado.
   - No se exige un job de 10 días en lab. SOURCE+CONTRACT cubren la retirada de 10d/20d/30d.
6. **Duration observable:** métrica/log `duration_ms` / `ElapsedMs` presente en el run PHYSICAL; ningún alert/gate de failure basado en ese número en F-03.
7. **No regresión F-01/F-02/B1/B2:** tests F-01 identity, F-02 promotion V2, MT5 ceiling/cancel/slot **no** se tocan; `go test` paquetes SQX de compute + no-touch MT5 workflows existentes verdes. Foreign dirty symphony intacto.

## Acceptance

- Elapsed sano ≠ FAILED en Builder, Optimizer, WFM durable, apply selected run y Group children.
- Heartbeat 2m + emisión 6s conservados.
- Cancel cooperativo, árbol-scoped, no retry.
- Recovery authorities existentes intactas.
- `DATABASE MIGRATION: NONE`.
- Campaign 30s y stop policy intactos.
- Sin Slot Pool / fencing / takeover / allocator SQX.

## Out of scope

Finalist V2 (F-02). F-01 identity. S0 Echo. Magic/seal/handoff (F-04). F-05 release/golden. MT5 ownership/slots/takeover. Capacity/admission budget del owner. Paralelizar SQX. Reescribir B2. Números arbitrarios de NORMAL. Reattach a proceso huérfano como lease MT5.

## Planned source diff (NORMAL, no ahora)

Modificar: `sqx/workflows/generic_workflow.go` (`genericActivityOptions`, ActivityOptions duplicadas Generic/Group, child `WorkflowRunTimeout` + ParentClosePolicy); `sqx/workflows/adaptive_workflow.go` (`mainActivityOptions`); `internal/workflows/main.go` (legado 10d/20d); `sqx/activities/worker/wfm_durable_export_activity.go` (quitar 10m); `sqx/activities/worker/durable_apply_selected_run.go` (`ensureApplyDeadline`); `sqx/adapters/cmd-executor/cmd_executor.go` + `process_nonwindows.go` (Canceled ≠ Timeout; process group); `sqx/activities/worker/project_activity.go` (heartbeat details); `sqx/adapters/executor-sqx/sqx_executor.go` (duration observable en hot path si falta). Tests espejo en esos paquetes. `pkg/sqxutils/executor.go` sólo si el path legado sigue invocado.

Crear: tests SOURCE de options (ceiling, ScheduleToClose 0, Heartbeat 2m); tests cancel vs timeout; no SQL nuevo.

## Evidencia y provenance

Inspección read-only `xKoRx/symphony@e50cb7ea47e03ff0cff1930f09f2e0c0fba00b48`.

- `sqx/workflows/generic_workflow.go` L138–164, L1830–1842, L1338–1343, L1535: 2m / 10d / 20d; child 30d; `WaitForCancellation`; retry infinito.
- `sqx/workflows/adaptive_workflow.go` L550–563: 2m / 5d / 10d. No registrado en `sqx/cmd/sqx-worker`.
- `sqx/workflows/forge_campaign_workflow.go` L80, L109–110: child REQUEST_CANCEL; activities 30s.
- `sqx/cmd/sqx-worker/main.go` L119–160, L324–326: `cmdexecutor.New` sin timeout; worker Options sin MaxConcurrent.
- `sqx/activities/worker/wfm_durable_export_activity.go` L86–89: 10m sintético; heartbeat details L116.
- `sqx/activities/worker/durable_apply_selected_run.go` L142–147: 10m.
- `sqx/adapters/cmd-executor/cmd_executor.go` L151–157, L306–320, L372–381: timeout opcional; Canceled→Timeout.
- `sqx/adapters/cmd-executor/process_nonwindows.go`: `CommandContext`, sin Setpgid.
- `sqx/core/instrumentation/heartbeat.go`: 6s ETCD; `ElapsedMs`.
- `sqx/activities/worker/steps/project_stage_recovery.go`: autoridad recovery.
- `sqx/activities/worker/steps/steps.go` `executeSQX`: un `ExecuteAndWait`, heartbeat estático.
- `internal/workflows/main.go` + `internal/tasks/sqx_worker_refactored.go`: legado 10d/20d.
- `pkg/sqxutils/executor.go` L154–159: `Timeout reached`.
- B1B freeze: [[2026-09-06-echo-forge-mt5-execution-model-v2]] principio elapsed; `mt5ActivityTechnicalCeiling` como hecho Temporal, no como modelo SQX.

## Límites y contradicciones

Si NORMAL cablea `sqcli/timeout_ms` al compute, reintroduce BUSINESS_DEADLINE: prohibido. Si se copia Slot Pool a SQX: fuera de contrato. Si `classifyError` sigue mapeando cancel a timeout, el retry infinito **reanuda** un job cancelado: debe corregirse. Adaptive no está en el worker productivo; igual se alinea para no dejar un killer latente. PHYSICAL de 10d no se exige; el límite viejo ejercible es 10m WFM/apply. Huérfanos Java sin process group quedan gap operativo, no B2.
