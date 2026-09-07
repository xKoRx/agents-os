---
type: known_error
schema_version: 1
scope: project
created: "2026-08-23"
updated: "2026-08-23"
area: "[[Echo]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[Symphony]]"
entities:
  - "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
related: []
aliases:
  - wfm durable export heartbeat timeout
  - sqcli still running after temporal heartbeat timeout
confidence: verified
source_session: "FINAL-DURABLE-E2E-DEPLOY-RERUN-NORMAL-ATTEMPT-16"
load_policy: when_error_matches
indexable: true
index_priority: high
tags:
  - kind/known-error
  - scope/project
  - tech/temporal
  - tech/sqx
---

# sqx-wfm-durable-export-heartbeat-timeout-while-sqcli-running

## Síntoma

- Tras Group children COMPLETED, el parent queda en `wfm_durable_export` con `TIMEOUT_TYPE_HEARTBEAT`.
- `MaximumAttempts=0` reintenta indefinidamente (attempt 4, 5, …).
- En el worker Kronos `sqcli -project action=start name=EchoForgeWFMExporter` puede emitir `All tasks completed` y exit 0 *después* de que Temporal ya abandonó la activity.

## Causa

- La activity no mantiene heartbeats durante todo el wall-clock de `sqcli`.
- Temporal declara heartbeat timeout; el proceso SQX sigue y luego el worker reporta `invalid activityID or activity already timed out` / `context canceled`.

## Impacto

- El pipeline durable no sella WFM CELL/AGGREGATE. Apply, Final Reretester, MT5 compile/backtest, Score y GLOBAL ranking no se alcanzan.
- Un E2E físico queda atrapado en RUNNING hasta aborto controlado.

## Detección

- `temporal workflow describe`: pending `wfm_durable_export`, `LastFailure` heartbeat timeout, `MaximumAttempts=0`.
- Logs Kronos: success marker SQX vs ERROR activity heartbeat/context canceled en el mismo minuto.
- Mongo `wfm_evaluations` / `wfm_matrices` / `wfm_runs` en 0 para ese `flow_run_ref`.

## Mitigación

- Runtime 0.2.66 sigue expuesto hasta el próximo deploy. Cancelar exclusivamente ese WorkflowID/RunID si el retry es infinito.
- Fix en master `435562b`: `WFMDurableExportActivity.Execute` envuelve `physical.Export` con `instrumentation.StartHeartbeatWithDetails` (`phase=wfm_physical_export`) y `defer Stop`. Intervalo default 6s (`etcd` nil) << `HeartbeatTimeout` 2m. Pendiente certificación E2E en `FINAL-DURABLE-E2E-DEPLOY-RERUN-NORMAL`.

## Evidencia

- Attempt 16: WorkflowID `sqx-main-v1-436c77d6-4b9a-4308-a89e-062dab0df373`, RunID `01a02f98-9a8d-7325-88ed-027be14c418f`, FlowRunRef `e1c10f66-de39-4a56-95b4-253e6ad28598`, release `0.2.66`.
- Kronos attempt 3: duration_ms 191633, marker All tasks completed, exit 0, then heartbeat/activity timeout.
- Corrección: commit `435562b04bef931c5b16602c95235db6e1b6c434`; tests de interceptor Temporal PASS; sin deploy.
