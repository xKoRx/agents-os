---
type: decision
schema_version: 1
scope: project
created: "2026-09-03"
updated: "2026-09-03"
area: "[[Echo Forge]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[xKoRx/symphony]]"
entities:
  - "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
related:
  - "[[2026-09-03-orphan-mt5-after-cancel]]"
  - "[[2026-09-03-echo-forge-worker-lifecycle-mt5-orphan-plan]]"
  - "[[2026-09-03-echo-forge-one-job-per-worker]]"
  - "[[2026-09-03-echo-forge-cancel-drain-lifecycle]]"
aliases:
  - ECHO_FORGE_WORKER_EXECUTION_MODEL_V1
  - one job per worker
  - one job per machine
confidence: verified
source_session: ECHO-FORGE-WORKER-LIFECYCLE-AND-MT5-ORPHAN-RCA-TOP
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

# 2026-09-03-echo-forge-worker-execution-model-v1

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Contexto

- RCA read-only `RCA-001-orphan-mt5-after-cancel` sobre Symphony `bac1d6ef93cd4714c1af4f2e44516bea44642e80` y SDK `c85594440f6755443ceb97ec4e333cd0ddb5b0ed`. Runtime `0.2.86`. C3 BLOCKED por `ORPHAN_MT5_PROCESS_AFTER_CANCEL`.
- CancelWorkflow de GenericSQXWorkflow selló CANCELLED; 8 MT5 backtest children tenían `ParentClosePolicy=Terminate`; 1 child `Terminated` `by parent close policy`; CommandExecutor Windows mata sólo el proceso directo.
- El worker MT5 configura `MaxConcurrentActivityExecutionSize=1`. SQX pasa `0`, pero la autoridad exacta del SDK `c85594440f6755443ceb97ec4e333cd0ddb5b0ed`, `pkg/shared/temporal/client.go`, normaliza `0→1`; ambos tienen concurrencia efectiva 1.

## Decisión

- PROJECT DECISION FROZEN `ECHO_FORGE_WORKER_EXECUTION_MODEL_V1`: `ONE_WORKER_PROCESS_PER_MACHINE=true`; `MAX_ACTIVE_JOBS_PER_WORKER=1`; `MAX_ACTIVE_JOBS_PER_MACHINE=1`; `PARALLELISM_SCOPE=HORIZONTAL_ACROSS_MACHINES_VIA_TEMPORAL`; `APPLIES_TO=ALL_ECHO_FORGE_WORKERS`.
- Autoridad de serialización: Temporal worker options, no `ActivityGate`.
- Cancel Temporal de Generic: REQUEST_CANCEL + WaitForCancellation en children MT5 artifact; esperar todos los futures; activity no completa hasta drain del process tree owned; FlowRun CANCELLED después del barrier.
- Windows MT5: ownership del árbol (`terminal64`/`metatester64`); Job Object preferido; no multiplexar Job A vs Job B en la misma VM.
- Contrato de fix: dos slices B (lifecycle Temporal) y C (ownership/drain Windows), ambos requeridos para release `0.2.87`. No existe Slice A de concurrencia y no se modifican workers.

## Rationale

- Un worker process por máquina y el contrato SDK zero→one mantienen un job activo por worker; no se debe reabrir ni “corregir” concurrency.
- ParentClosePolicy TERMINATE no espera cleanup de activity. WaitForCancellation en la activity es inútil si el child workflow ya fue Terminated.
- `Process.Kill()` en Windows no mata descendants. 8 children Temporal no son 8 jobs físicos.

## Consecuencias

- Todo worker Forge que lance herramientas externas debe serializar a 1 activity física.
- No se reabre Campaign, ConfigSourceWave, Promotion, Strategy Identity, FlowRun writers (salvo esperar barrier), ni CHANGE-001 (stop/Stager).
- Replay: `workflow.GetVersion("mt5-artifact-child-cancel-v1", DefaultVersion, 1)` conserva opciones legacy para histories anteriores y habilita opciones explícitas para nuevas ejecuciones; no se elige un gate operativo ni Worker Versioning.

## Alternativas descartadas

- Option E (sólo Temporal): no mata `metatester64`.
- Option G sola: no explica el orphan de cancel.
- Option A (Kill directo): es el defecto actual.
- Slice A de concurrencia: rechazada; contradice la autoridad del SDK y el modelo congelado.
