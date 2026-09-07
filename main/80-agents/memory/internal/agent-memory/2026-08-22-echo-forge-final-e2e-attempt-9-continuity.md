---
type: agent_memory
schema_version: 1
scope: project
created: 2026-08-22
updated: 2026-08-22
area: "[[Aranea]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
entities:
  - "[[Echo Forge]]"
confidence: high
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/agent-memory
  - scope/project
  - project/echo-forge
  - agent/internal
---

# Continuidad — FINAL-DURABLE-E2E Attempt 9

## Continuidad

- Release live: `0.2.60` source `c8ff10e` (contiene `b43aeae`). Docs commit `d24959b`.
- Request `final-durable-e2e-normal-20260822T220435Z-30f40385` / WF `sqx-main-v1-5d9a7f65-a9bf-49ac-87ca-52c853f83dbe` / FlowRunRef `27527ee3-7e0c-409f-acf3-71c4e2aa8f24`.
- PASS: Overview inline `databank=output` expected=20 written=20 rows=20; sin segunda ejecución SQX de Overview.
- BLOCKED: `db_register` missing exact overview row para object keys MinIO (`XAUUSD_L_H1_example_flow_16_v1_Strategy_6.1.15.z0.sqx`) vs `strategy_name=Strategy 6.1.15`.
- NEXT EXACT histórico de Attempt 9: corrección de binding Overview en `db_register`; no relanzar Attempt 10 en esa sesión.
- Watcher Zeus 0.2.60 se suicida ~10s por `/opt/symphony/CURRENT` legacy `0.2.40`; stager CURRENT sí es `0.2.60`.

## Checkpoint — FIX-DURABLE-BUILDER-UPLOAD-OVERVIEW-CORRELATION-NORMAL

- Root cause: `import_metadata` sella `OverviewObservation.CanonicalStrategyID` contra `ResultFiles` locales (`Strategy 6.1.15`); `db_register` busca el CanonicalStrategyID del object key subido (`XAUUSD_L_H1_example_flow_16_v1_Strategy_6.1.15.z0`).
- Fix: `builderCorrelationCore` (token `Strategy_X.Y.Z`, sin sufijo host) y `sealBuilderOverviewToUploaded` en `persistBuilderEvidence` antes de indexar Overview. UploadedObject durable no cambió.
- Commit: `78dc5b187d93ba97316b7887351dce0b1e869c98`. HEAD == origin/master.
- NEXT EXACT: `FINAL-DURABLE-E2E-DEPLOY-RERUN-NORMAL`. No deploy ni Attempt 10 en esta sesión.

## Checkpoint — FINAL-DURABLE-E2E Attempt 10

- Release live: `0.2.61` source `78dc5b1`. Docs commit `d9c281b`.
- Request `final-durable-e2e-normal-20260822T233907Z-22397c88` / WF `sqx-main-v1-169e2e98-cbf8-4fc6-b6cd-789ccbb77ce8` / FlowRunRef `b287e2b4-47f5-4b49-8a94-641dd4ecaf65`.
- PASS: Builder durable 20/20 Strategy+Evaluation+MetricSet; Classification 20; early ranking 11 / TopProjection 16.
- BLOCKED: `exactEarlyRankingArtifacts` — key `...Strategy_1.1.14.h0.sqx` (StrategyRef `6f1452dd-...`) is not an exact current batch key at group `02_retester`.
- NEXT EXACT: `DURABLE-EARLY-RANKING-GROUP-CURRENT-BATCH-KEY-FIX-NORMAL`; no Attempt 11 in this session.

## Checkpoint — FINAL-DURABLE-E2E Attempt 11

- Release live: `0.2.62` source `6f99883`. Docs commit `9d67374`.
- Request `final-durable-e2e-normal-20260823T004624Z-62d58c3d` / WF `sqx-main-v1-ab979b54-19d9-4042-81c3-42f0a4b0f523` / FlowRunRef `36e5cef3-2bd0-4926-833b-bd61f911a0bb`.
- PASS: Builder durable 20/20 Strategy+Evaluation+MetricSet; Classification 20; early ranking 14 / TopProjection 19; exporter count 20→20 with empty exporter keys.
- BLOCKED: `exactEarlyRankingArtifacts` — full MinIO key `...Strategy_2.1.19.k0.sqx` (StrategyRef `396d1cf8-...`) is not an exact current.Keys member; current.Keys are Builder activity basenames.
- NEXT EXACT: `DURABLE-EARLY-RANKING-GROUP-EXACT-ARTIFACT-KEY-IDENTITY-FIX-NORMAL`; no Attempt 12 in this session.

## Señales de carga

- Retomar desde `DURABLE-EARLY-RANKING-GROUP-EXACT-ARTIFACT-KEY-IDENTITY-FIX-NORMAL`; no relanzar otro intento hasta resolver la identidad exacta de los artefactos del grupo.
