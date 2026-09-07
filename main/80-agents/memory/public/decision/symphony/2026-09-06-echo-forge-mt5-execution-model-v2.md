---
type: decision
schema_version: 1
scope: project
created: "2026-09-06"
updated: "2026-09-06"
area: "[[Echo Forge]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[xKoRx/symphony]]"
entities:
  - "[[Echo Forge]]"
related:
  - "[[2026-09-06-echo-forge-mt5-global-physical-ownership-v2]]"
  - "[[2026-09-03-echo-forge-worker-execution-model-v1]]"
  - "[[2026-09-03-mt5-artifact-timeout-authority]]"
  - "[[2026-08-14-echo-forge-one-vm-one-worker-one-task]]"
  - "[[2026-09-03-echo-forge-worker-lifecycle-mt5-orphan-plan]]"
  - "[[2026-09-04-echo-forge-mt5-report-6180-compatible-allowlist]]"
aliases:
  - ECHO_FORGE_MT5_EXECUTION_MODEL_V2
  - mt5 slot pool
  - long-running MT5
confidence: verified
source_session: ECHO-FORGE-MT5-SLOT-POOL-AND-LONG-RUNNING-EXECUTION-V2-TOP
load_policy: when_project_loaded
indexable: true
index_priority: high
tags:
  - kind/decision
  - scope/project
  - project/echo-forge
  - tech/mt5
  - tech/temporal
---

# 2026-09-06-echo-forge-mt5-execution-model-v2

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Contexto

- Finalist Factory V1 está PRODUCT READY / CLOSED en release `0.2.96`. Dos FULL no-Campaign llegaron a Compile 3/3 y todos los backtests físicos terminaron `backtest_timeout` sin HTM. El periodo owner era `2016.01.04→2026.06.05` con `tasks[].mt5.timeout=45m`.
- El modelo congelado V1 (`ONE_WORKER_PROCESS_PER_MACHINE` + `MAX_ACTIVE_JOBS_PER_MACHINE=1` + `MaxConcurrentActivityExecutionSize=1`) serializa una instalación portable única. Eso ya no cubre backlog lógico vs capacidad física.
- Temporal exige `StartToCloseTimeout` finito. El runner mata el Job Object con `context.WithTimeout` derivado de `mt5.timeout`. Eso contradice el intent del owner: el tiempo de cómputo no es fallo.

## Decisión

- PROJECT DECISION FROZEN `ECHO_FORGE_MT5_EXECUTION_MODEL_V2` aplica al worker Windows MT5. No reabre el modelo SQX Linux de un job físico por máquina.
- `ONE_WORKER_PROCESS_PER_MACHINE=true`. `SLOT_COUNT=N` instalaciones portable completas e independientes. `MAX_ACTIVE_PHYSICAL_JOBS_PER_SLOT=1`. `MAX_ACTIVE_PHYSICAL_JOBS_PER_MACHINE=count(READY/BUSY usable slots)`.
- Cardinalidad lógica de children MT5 no está acotada por N. El backlog vive en la task queue de Temporal. La seguridad física es lease/ownership de slot, no un hard-cap de cohort.
- Compile y Backtest compiten el mismo pool. MetaEditor y Tester mutan la instalación portable.
- Estados de slot: `READY`, `BUSY`, `DRAINING`, `QUARANTINED`.
- Allocator: lease durable local por slot (archivo/lock en el host) + mutex in-process. Temporal concurrency es capacidad de scheduling, no autoridad física. La premisa “No PostgreSQL / lease local basta contra duplicados” queda SUPERSEDED / INCOMPLETE para el invariante de flota; ver [[2026-09-06-echo-forge-mt5-global-physical-ownership-v2]]. El contrato local un-slot-un-job permanece.
- Identidad durable del job físico: `WorkflowID` + `RunID` + `ActivityID` + `RequestID` + `StrategyRef` + source artifact (key/SHA) + `SlotID`. El attempt de Temporal no es identidad de negocio. Un retry debe reattach si el proceso owned sigue vivo; jamás spawn duplicado.
- Long-running MT5: sin deadline de negocio. Heartbeat = liveness del worker/activity. Cancelación explícita y fallo de infraestructura sí terminan. `StartToCloseTimeout` queda como horizonte técnico remoto no configurable por el owner.
- `tasks[].mt5.timeout` se depreca como autoridad de runtime: se ignora para matar y no se reinterpreta. Presencia emite diagnóstico, no fallo.
- `MaxCampaignMT5BacktestChildrenPerGeneric=4` se supersede como safety física. No se cambia en esta TOP. Futuro: quitar el hard-cap o redefinirlo sólo como budget de negocio owner-configured.
- Build desconocido: el slot queda `QUARANTINED`; los demás slots certificados siguen. Live Update permitido. Allow-list explícita `{6090,6140,6180}` sin rangos. El parser HTM sigue fail-closed; el FileVersion por slot es gate nuevo de allocator.
- Drain/deploy: PENDING/stop deja de admitir slots nuevos; jobs BUSY continúan; shutdown sólo con slots idle. Un job de meses puede retrasar el cutover de esa máquina.

## Rationale

- Evidencia FULL: 6/6 backtests murieron a los 45m sobre ~10 años de ticks. El funnel de robustez no colapsó a cero.
- Subir `MaxConcurrent` a 3 sin lease durable reabre el modo prohibido (attempt 1 vivo en slot-1 y retry en slot-2). V1 lo oculta porque la concurrencia efectiva es 1.
- Job Object `KILL_ON_JOB_CLOSE` y cancel slot-scoped ya existen y deben reutilizarse. `taskkill` global sigue prohibido.
- SQX Builder/Retester/Optimizer comparte el contrato semántico (sin timeout de negocio) pero no el allocator de slots: databanks SQX siguen serializados por worker.

## Consecuencias

- Implementación en dos NORMAL cohesivos, un release de certificación, certificación física 3-slot en WORKER-KRONOS, después FULL golden. No se implementa en esta TOP.
- NEXT EXACT vigente para MT5 long-running: `ECHO-FORGE-MT5-LONG-RUNNING-GLOBAL-OWNERSHIP-RETRY-DRAIN-V2-NORMAL-B`. El anti-duplicate local-only de esta TOP queda SUPERSEDED / INCOMPLETE a nivel flota.
- Decisiones supersedidas para MT5: [[2026-09-03-echo-forge-worker-execution-model-v1]] en `MAX_ACTIVE_JOBS_PER_MACHINE=1`; [[2026-09-03-mt5-artifact-timeout-authority]] como killer de proceso; [[2026-08-14-echo-forge-one-vm-one-worker-one-task]] no aplica a slots MT5. V1 permanece para workers SQX.

## Alternativas descartadas

- Reemplazar el timeout por `365d` sin heartbeat/lease: Temporal seguiría pudiendo redeliver y duplicar procesos.
- `MaxConcurrentActivityExecutionSize=3` como única safety: no cubre restart ni retry.
- Lease en PostgreSQL/control-plane: overkill para ownership de una máquina.
- Alinear periodos SQX/MT5 o copiar fechas CFX al JSON: viola independencia owner-configured.
- Matar por ausencia de log/HTM durante el cómputo: un tester puede no emitir output útil durante meses.
- Aplicar slots al worker SQX Linux en esta TOP: el recurso físico compartido (databanks) sigue exigiendo serialización distinta.
