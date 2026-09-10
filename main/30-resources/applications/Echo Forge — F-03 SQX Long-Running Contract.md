---
type: resource
schema_version: 1
status: active
area: "[[Echo]]"
sources:
  - "[[Echo Forge — Factory V2 Completion]]"
  - "[[2026-09-06-echo-forge-mt5-execution-model-v2]]"
  - "[[2026-09-03-mt5-artifact-timeout-authority]]"
  - "[[2026-09-06-echo-forge-temporal-activity-ceiling-clamp]]"
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

`sqxActivityTechnicalCeiling` queda fijado (no conceptual) en la sección PLATFORM_CEILING: `time.Duration(1<<63-1) - time.Second`. Autoridad = SDK Temporal + representación Go/`durationpb`, no un número de negocio y no un import MT5. `ScheduleToCloseTimeout` de cómputo SQX = `0`. Adaptive está **INACTIVE/DEPRECATED — NO CHANGE**.

## Mapa de kill paths (source @ e50cb7e)

Cada límite tiene exactamente una categoría.

### BUSINESS_DEADLINE — REMOVE

| Límite | Dónde | Qué mata | Acción |
|---|---|---|---|
| `StartToCloseTimeout: 10 * 24 * time.Hour` | `genericActivityOptions`, `runGenericSQXWorkflow` ActivityOptions duplicadas, `GroupSQXWorkflow` ActivityOptions | Activity de proyecto/compute sana a los 10d | Reemplazar por `sqxActivityTechnicalCeiling` |
| `ScheduleToCloseTimeout: 20 * 24 * time.Hour` | mismos tres sitios Generic/Group | Suma de attempts (retry infinito) a los 20d | Poner `0` (unset) |
| `StartToCloseTimeout: 5d` + `ScheduleToCloseTimeout: 10d` | `mainActivityOptions` en `adaptive_workflow.go` | Residual en código **no registrado** | **INACTIVE/DEPRECATED — NO CHANGE.** No es superficie ejecutable de F-03. No alinear por simetría. |
| `WorkflowRunTimeout: 30 * 24 * time.Hour` | child `GroupSQXWorkflow` (lote secuencial y fan-in early ranking) | Child group sano a 30d | Omitir / `0` (unlimited run) |
| `context.WithTimeout(ctx, 10*time.Minute)` si el ctx no trae deadline | `WFMDurableExportActivity.Execute` | Export WFM físico sano a 10m pese a heartbeat 6s | Eliminar el timeout; el ctx de Temporal (heartbeat + cancel) basta |
| `ensureApplyDeadline` → `10*time.Minute` | `durable_apply_selected_run.go` | Apply selected run (incluye `ExecuteAndWait` SQX) a 10m | Eliminar el deadline sintético |
| `StartToCloseTimeout: 10d` / `ScheduleToCloseTimeout: 20d` | `internal/workflows/main.go` `SQXJobWorkflow` / `SQXGroupWorkflow` | Legado aún registrado por `internal/tasks/sqx_worker_refactored.go` | Misma regla si el binario legado sigue compilable; no dejar un segundo killer |
| `strings.Contains(outputStr, "Timeout reached")` → error | `pkg/sqxutils/executor.go` | Stdout de espera sqcli como failure de negocio | No clasificar elapsed wait como failure en ningún path invocado; hot path productivo es `executor-sqx` (no parsea esa frase) |
| `SQXConfig.SQCLITimeoutMs: 10000` default | `sqx/core/config/config.go` | Landmine: no está cableado en `sqx-worker` (`cmdexecutor.New` sin `WithTimeout`) | Prohibido cablear `WithTimeout` al executor de compute SQX; test de no-regresión |

### TECHNICAL_LIVENESS — KEEP/ADJUST

| Límite | Autoridad | Evento que prueba pérdida | Retry/recovery | UNKNOWN / ambiguous |
|---|---|---|---|---|
| `HeartbeatTimeout: 2 * time.Minute` | Temporal ActivityOptions Generic/Group (LIVE). Adaptive no aplica | Ausencia de heartbeat >2m (worker muerto, activity stuck sin `RecordHeartbeat`) | `RetryPolicy.MaximumAttempts=0` (infinito, transiente); recovery durable existente | Un heartbeat timeout **no** es elapsed sano. Retry nuevo attempt. No reattach de proceso SQX (no hay takeover). Si hay Evaluation/producer sellados → skip físico; si StageExecution RUNNING sin sello → reiniciar físico |
| Intervalo heartbeat 6s (`sqx/activity/heartbeat_seconds`) | ETCD + `instrumentation.StartHeartbeat` / `StartHeartbeatWithDetails` | Primer heartbeat inmediato; ticker 6s | N/A (emisión) | Si ETCD ausente: default 6s. Debe permanecer ≪ 2m |
| `WaitForCancellation: true` | ActivityOptions compute | Cancel de workflow/activity | Temporal no reintenta CanceledError **si** se propaga como cancel, no como timeout de aplicación | Hoy `cmd_executor.classifyError` mapea `context.Canceled` a `ErrorTypeTimeout` — **ADJUST**: cancel explícito ≠ timeout |
| `DefaultTerminationPolicy` SIGTERM luego SIGKILL 5s | `cmd-executor` sobre el **process group** del `sqcli` de este Execute | Cancel explícito o deadline técnico del ctx de Execute | N/A | ADJUST: ver contrato process-tree. No Job Object MT5. No `taskkill` global. No matar el process-group del worker |
| `exec.CommandContext(ctx)` | `process_nonwindows.go` / utils | Mismo ctx de activity | Igual | El ctx de compute **no** debe llevar deadline de negocio |

### PLATFORM_CEILING — JUSTIFY

Valor exacto (constante local en `sqx/workflows`, no importar `mt5ActivityTechnicalCeiling`):

```text
sqxActivityTechnicalCeiling = time.Duration(1<<63-1) - time.Second
```

Eso es `MaxInt64` nanosegundos menos un segundo: el máximo `time.Duration` de Go con holgura de 1s. NORMAL **no** elige ni sustituye este número. Prohibido 365d, 10y, o cualquier cifra de negocio.

Por qué es **platform safety ceiling** y no business deadline:

- El SDK Temporal Go exige `StartToCloseTimeout` finito y `> 0` cuando `ScheduleToCloseTimeout` está unset/`0`. Omitir ambos es inválido: el SDK rechaza el StartActivity. No hay diseño legal “sin StartToClose”.
- El único techo finito que no es un SLA de SQX es el máximo representable. `durationpb` redondea a segundos; `MaxInt64` ns puro desborda ese redondeo. La holgura de 1s es el techo seguro de representación (autoridad: [[2026-09-06-echo-forge-temporal-activity-ceiling-clamp]]; el comentario de `mt5ActivityTechnicalCeiling` es evidencia del **mismo** hecho Temporal/Go, no licencia para importar MT5).
- Ningún owner, ETCD, task JSON ni duración de Builder/Optimizer/WFM justifica un número menor. Por eso no se inventa un techo “razonable”.

Qué ocurre si alguna vez se alcanza (evento de plataforma, no esperado en operación):

1. Temporal cierra el attempt con timeout `StartToClose` (`TimeoutTypeStartToClose`).
2. El ctx de la activity se cancela → el process-group del `sqcli` de ese Execute termina (padre + hijos Java + nietos).
3. No es `LifecycleCancelled` de operador. No es FAILED de negocio por elapsed.
4. Retry: `RetryPolicy.MaximumAttempts=0` (infinito, transiente). StartToClose de plataforma es retryable, igual que HeartbeatTimeout. Temporal programa un attempt nuevo.
5. Recovery: idéntica a liveness loss — no reattach; sellado skip; RUNNING sin sello = nuevo `ExecuteAndWait`.
6. Un job sano no debe llegar aquí; el techo existe solo porque Temporal exige un finito.

`ScheduleToCloseTimeout = 0` (unset):

- `0` es la única forma de no imponer un presupuesto calendario a la **suma** de attempts. El 20d actual es BUSINESS_DEADLINE sobre el retry infinito.
- Con `MaximumAttempts=0`, un ScheduleToClose finito reintroduce elapsed-as-failure a escala de campaña de retries.
- Temporal: `0` = no set; el bound por attempt es `StartToClose` (este techo) y el bound de liveness es Heartbeat 2m.
- No se copia la semántica de slots/Job Object MT5. Que B1B también deje ScheduleToClose en cero es coincidencia de API Temporal, no un import.

Tests que fijan el contrato (NORMAL; nombres ilustrativos, asserts no):

- Options Generic/Group (incluidos duplicados en `runGenericSQXWorkflow` y `GroupSQXWorkflow`): `StartToCloseTimeout == sqxActivityTechnicalCeiling` igualdad exacta; `ScheduleToCloseTimeout == 0`; `HeartbeatTimeout == 2*time.Minute`; `WaitForCancellation == true`; `RetryPolicy.MaximumAttempts == 0`.
- `activity.Info.StartToCloseTimeout`: `> 0` y `<= sqxActivityTechnicalCeiling`. Prohibido asertar igualdad a `87600h` (clamp de testsuite SDK; ver patrón). Igualdad entre configs que no deben diferir por duración de negocio.
- SOURCE scoped a superficies LIVE: cero literales 10d/20d/30d/10m de compute en `generic_workflow.go`, WFM export, apply, `sqx-worker` `New()`, legado `internal/workflows/main.go` si T1.2 aplica. **No** fallar SOURCE por `adaptive_workflow.go`.
- Ningún test de compute pinnea 10d/20d/30d/10m como éxito.

`WorkflowExecutionTimeout` / `WorkflowRunTimeout` del parent Generic: hoy 0. Conservar 0. Child group: quitar 30d.

Si el SDK rechazara este techo en runtime: PLAN_CONFLICT. No bajar a un número de negocio.

### KEEP (fuera del kill de compute largo; no confundir)

| Límite | Por qué no es F-03 compute |
|---|---|
| `forgeCampaignActivityOptions` `StartToCloseTimeout: 30s` | Control plane (start/resolve/finalize/cancel DB). No ejecuta sqcli. Conservar. Campaign `MaxWaves` / stop policy = budget/admission, **no** mata un Generic sano por wall-clock |
| `context.WithTimeout(..., 30s)` FlowRun start/seal, ForgeCampaign activities, watcher intake | I/O corto |
| `WithTimeout(..., 2*time.Minute)` rank/reconcile/score/seal WFM/select/classify | Activities cortas de persistencia/score, no CLI Builder/Optimizer/WFM físico |
| `maintenance/timeout_ms` + `cmdexecutor.WithTimeout` | Maintenance executor, no compute SQX |
| MT5 `mt5ActivityTechnicalCeiling` / Slot Pool / `tasks[].mt5.timeout` ignorado | B1B/B2 CLOSED. No-touch. El techo SQX se declara local; no se importa |
| Cleanup databanks hook | Determinismo de retry, no timeout |

## Superficies ejecutables vs INACTIVE

F-03 certifica runtime actual. Docs/SPECs históricas no prueban ejecución.

**LIVE (in scope):** `sqx/cmd/sqx-worker/main.go` registra `GenericSQXWorkflow`, `GroupSQXWorkflow`, `MT5CompileArtifactWorkflow`, `MT5BacktestArtifactWorkflow`, `ForgeCampaignWorkflow`. Compute SQX: Generic/Group activities, WFM durable export, apply selected run, `cmd-executor`, project heartbeat. Legado aún ejecutable: `cmd/symphony sqx-worker-minio` (`internal/tasks/sqx_worker_refactored.go`) registra `SQXJobWorkflow` / `SQXGroupWorkflow`.

**INACTIVE/DEPRECATED — NO CHANGE:** `AdaptiveSQXWorkflow` y `AdaptiveTypeWorkflow` en `sqx/workflows/adaptive_workflow.go`. Evidencia de runtime: comentarios `DEPRECATED` (prototipo; producción = Generic); `sqx-worker` **no** los registra; el único `RegisterWorkflow(AdaptiveSQXWorkflow)` está en tests (`adaptive_workflow_test.go`). FEAT-SQX-ADAPTIVE-WORKFLOW T8.1 (registro planificado) no está en source actual. `adaptive_workflow.go` **fuera** de implementation scope. Los 5d/10d residuales no se tocan y no fallan SOURCE.

MT5 workflows se registran en el mismo worker pero son no-touch de F-03 (B1B/B2 CLOSED).

## Cancel contract

No se rediseña B2.

**Quién puede cancelar**

- Operador Temporal (`CancelWorkflow`) sobre el WorkflowID del Generic (o Campaign padre).
- `ForgeCampaignWorkflow` ante `ctx.Err()` canceled: `PARENT_CLOSE_POLICY_REQUEST_CANCEL` + `WaitForCancellation` del child Generic (ya existe).
- Drain/PENDING del worker: no admite activities nuevas; jobs BUSY siguen; no es cancel de negocio.

**Cómo llega a Activity / proceso**

1. Cancel del workflow → activities con `WaitForCancellation=true` reciben ctx canceled.
2. `execute_sqx` / `ExecuteAndWait` → `CommandExecutor.Execute` → `effectiveCtx.Done()` → terminate del **process group** de ese Execute.
3. ADJUST process-tree (non-Windows, obligación F-03; no copiar Job Object / `taskkill` / slots MT5):
   - `startManagedProcess` del `sqcli` de **este** Execute usa `Setpgid=true` (líder = el `sqcli` hijo). El worker **no** cambia de process-group; jamás `kill(0, …)` ni el pgid del worker.
   - Cancel explícito **o** deadline técnico del ctx de Execute: SIGTERM al grupo (`-pgid`) y luego SIGKILL a los 5s de la policy existente, acotado a ese grupo.
   - Debe morir el árbol completo: padre `sqcli` + hijos Java + nietos de **esa** invocación.
   - No debe morir: worker, Temporal, sibling Execute, otro job, process-group global.
4. `context.Canceled` se conserva como cancel. Prohibido `classifyError` → `ErrorTypeTimeout` (hoy L379–380). `ErrorTypeTimeout` es transiente y con `MaximumAttempts=0` **reanuda** un job cancelado. Si `domain.ErrorType` no tiene cancel: propagar `context.Canceled` (o `temporal.CanceledError` del SDK) sin pasar por `NewError(ErrorTypeTimeout)`. Añadir `ErrorTypeCanceled` no-transiente en `sqx/core/domain` está permitido. No importar helpers de `mt5_ownership.go`.
5. Tests CANCEL deben demostrar: tras cancel, PID padre + PID hijo + PID nieto gone; PID del worker vivo; sibling Execute vivo; `errors.Is(err, context.Canceled)` (o `temporal.IsCanceledError`) true y tipo ≠ `ErrorTypeTimeout`.

**Qué debe morir**

- Árbol del job objetivo: Generic cancelado, sus Group children, activities `project` / WFM export / apply de ese árbol, proceso `sqcli` y **todo** descendiente (Java hijos y nietos) de **esa** ejecución, vía process-group propio.

**Qué NO debe morir**

- Otros Generic/Campaign en el mismo worker o cluster.
- Worker `sqx-worker`, su process-group, Temporal, ETCD, Postgres, MinIO.
- Databank/proceso de un job distinto.
- Slot Pool / procesos MT5 (no-touch).
- Control-plane Campaign salvo el child cuyo padre canceló.

**Estado durable final**

- FlowRun: `LifecycleCancelled` vía `sealFlowRun` (ya distingue cancel de fail).
- StageExecution FAILED/CANCELLED: fail-closed; **no** se recupera como éxito (`project_stage_recovery.go`).
- Campaign: `ForgeCampaignCancelActivity` en disconnected context (ya existe).

**Retry / no-retry**

- Cancel explícito: **no retry**. `context.Canceled` permanece cancel.
- Heartbeat timeout / crash de worker / StartToClose de plataforma (si el techo se alcanzara): retry técnico según policy existente (`MaximumAttempts=0`).

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

1. **SOURCE:** grep/assert **scoped a LIVE**: ningún `StartToCloseTimeout` 10d, ningún `ScheduleToCloseTimeout` 20d, ningún `WorkflowRunTimeout` 30d en `generic_workflow.go`; ningún `WithTimeout(10*time.Minute)` en WFM export ni `ensureApplyDeadline` 10m; ningún `WithTimeout` en `cmdexecutor.New` de `sqx/cmd/sqx-worker`; legado `internal/workflows/main.go` sin 10d/20d tras T1.2. Builder/Optimizer/WFM sano no tiene business deadline restante. **Excluir** `adaptive_workflow.go` del fail de SOURCE (INACTIVE). No exigir ausencia de 5d Adaptive.
2. **CONTRACT:** retry/recovery no cambia por duración. Tests: heartbeat timeout sigue retryable; StageExecutionRef estable; sealed output no se republica; elapsed no produce `ErrorTypeTimeout` de negocio. Dual: recovery tests existentes verdes.
3. **CANCEL:** cancel explícito de un Generic mata sólo su árbol (children group REQUEST_CANCEL; process-group propio del `sqcli` de ese Execute, incluidos hijos/nietos Java). Tests: parent+child+grandchild gone; worker vivo; sibling vivo. `context.Canceled` ≠ `ErrorTypeTimeout`. Cleanup no borra workspace ajeno. No semántica MT5.
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

Finalist V2 (F-02). F-01 identity. S0 Echo. Magic/seal/handoff (F-04). F-05 release/golden. MT5 ownership/slots/takeover. Capacity/admission budget del owner. Paralelizar SQX. Reescribir B2. Números arbitrarios de NORMAL. Reattach a proceso huérfano como lease MT5. `adaptive_workflow.go` (INACTIVE/DEPRECATED — NO CHANGE).

## Planned source diff (NORMAL, no ahora)

Modificar: `sqx/workflows/generic_workflow.go` (`genericActivityOptions`, ActivityOptions duplicadas Generic/Group, child `WorkflowRunTimeout` + ParentClosePolicy, constante `sqxActivityTechnicalCeiling`); `internal/workflows/main.go` (legado 10d/20d del binario `sqx-worker-minio`); `sqx/activities/worker/wfm_durable_export_activity.go` (quitar 10m); `sqx/activities/worker/durable_apply_selected_run.go` (`ensureApplyDeadline`); `sqx/adapters/cmd-executor/cmd_executor.go` + `process_nonwindows.go` (Canceled ≠ Timeout; Setpgid del hijo; terminate `-pgid`); `sqx/core/domain` sólo si hace falta `ErrorTypeCanceled` no-transiente; `sqx/activities/worker/project_activity.go` (heartbeat details); `sqx/adapters/executor-sqx/sqx_executor.go` (duration observable en hot path si falta). Tests espejo en esos paquetes. `pkg/sqxutils/executor.go` sólo si el path legado sigue invocado.

**No modificar:** `sqx/workflows/adaptive_workflow.go` (INACTIVE/DEPRECATED).

Crear: tests SOURCE de options (ceiling exacto, ScheduleToClose 0, Heartbeat 2m, MaximumAttempts 0); tests cancel vs timeout; test process-tree parent+child+grandchild; no SQL nuevo.

## Evidencia y provenance

Inspección read-only `xKoRx/symphony@e50cb7ea47e03ff0cff1930f09f2e0c0fba00b48`.

- `sqx/workflows/generic_workflow.go` L138–164, L1830–1842, L1338–1343, L1535: 2m / 10d / 20d; child 30d; `WaitForCancellation`; retry infinito.
- `sqx/workflows/adaptive_workflow.go` L21–23, L103, L550–563: DEPRECATED; 5d/10d residuales. No registrado en `sqx/cmd/sqx-worker` L329–333. Tests sí lo registran. **NO CHANGE.**
- `sqx/cmd/sqx-worker/main.go` L329–333: Generic, Group, MT5 compile/backtest, Campaign. Sin Adaptive.
- `sqx/workflows/forge_campaign_workflow.go` L80, L109–110: child REQUEST_CANCEL; activities 30s.
- `sqx/cmd/sqx-worker/main.go` L119–160, L324–326: `cmdexecutor.New` sin timeout; worker Options sin MaxConcurrent.
- `sqx/activities/worker/wfm_durable_export_activity.go` L86–89: 10m sintético; heartbeat details L116.
- `sqx/activities/worker/durable_apply_selected_run.go` L142–147: 10m.
- `sqx/adapters/cmd-executor/cmd_executor.go` L151–157, L306–320, L372–381: timeout opcional; Canceled→Timeout.
- `sqx/adapters/cmd-executor/process_nonwindows.go`: `CommandContext`, sin `Setpgid` (hoy el terminate no cubre hijos Java).
- `sqx/core/instrumentation/heartbeat.go`: 6s ETCD; `ElapsedMs`.
- `sqx/activities/worker/steps/project_stage_recovery.go`: autoridad recovery.
- `sqx/activities/worker/steps/steps.go` `executeSQX`: un `ExecuteAndWait`, heartbeat estático.
- `internal/workflows/main.go` + `internal/tasks/sqx_worker_refactored.go`: legado 10d/20d.
- `pkg/sqxutils/executor.go` L154–159: `Timeout reached`.
- B1B freeze: [[2026-09-06-echo-forge-mt5-execution-model-v2]] principio elapsed. Techo: [[2026-09-06-echo-forge-temporal-activity-ceiling-clamp]] (hecho Temporal/Go). No modelo SQX de slots.

## Límites y contradicciones

Si NORMAL cablea `sqcli/timeout_ms` al compute, reintroduce BUSINESS_DEADLINE: prohibido. Si se copia Slot Pool a SQX: fuera de contrato. Si `classifyError` sigue mapeando cancel a timeout, el retry infinito **reanuda** un job cancelado: debe corregirse. Adaptive **no** se alinea: está DEPRECATED y no registrado; tocarlo por simetría está fuera de alcance. PHYSICAL de 10d no se exige; el límite viejo ejercible es 10m WFM/apply. Huérfanos Java fuera del process-group del Execute cancelado quedan gap operativo, no B2. Si el process-group se aplica al worker (pgid 0 / Setpgid del proceso padre): PLAN_CONFLICT.
