---
type: known_error
schema_version: 1
scope: project
created: "2026-08-25"
updated: "2026-08-25"
area: "[[Echo]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[echo-forge]]"
entities: []
related: []
aliases:
  - flowrun lifecycle telemetry carrier mismatch
  - flow_run_start TelemetryCarrier rejection
confidence: verified
source_session: DURABLE-FLOWRUN-LIFECYCLE-WRITEBACK-E2E-NORMAL
load_policy: when_error_matches
indexable: true
index_priority: high
tags:
  - kind/known-error
  - scope/project
  - project/echo-forge
  - tech/temporal
  - error/flowrun-lifecycle
---

# FlowRun lifecycle activity rejected by strict TelemetryCarrier interceptor

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Síntoma

- A production `flow_run_start` activity is scheduled but repeatedly remains `Scheduled`.
- Temporal reports `activity argument does not implement TelemetryCarrier`; the FlowRun row remains `PENDING`.

## Causa

- The shared Temporal interceptor requires the activity payload to implement `GetTelemetry() telemetry.Context`.
- `FlowRunStartRequest` and `FlowRunSealRequest` carry lifecycle data but do not implement that interface; the workflow passes them directly to `ExecuteActivity`.

## Impacto

- The physical FlowRun lifecycle cannot advance to `RUNNING` or terminal writeback. Focused unit tests that bypass the production interceptor can remain green while the deployed worker fails at dispatch.

## Detección

- Inspect Temporal pending activities and the last failure; then compare the activity payload with the SDK `TelemetryCarrier` contract before retrying a release.

## Mitigación

- No data or code workaround was applied in this certification. Resolve the payload/interceptor contract in a separate RCA/fix session, add a real-interceptor integration test, then redeploy and rerun the physical certificate.

## Evidencia

- Evidence: baseline `db0f61bc5c397b47ee4d0a54e78cba0c4aea0a9d`, release `0.2.70`, one FlowRun row with `row_version=0`, and Temporal `flow_run_start` attempt 4 with the exact rejection above.
- Source locations: `sqx/activities/worker/flow_run_lifecycle_activity.go`, `sqx/workflows/generic_workflow.go`, and the worker registration in `sqx/cmd/sqx-worker/main.go`.
