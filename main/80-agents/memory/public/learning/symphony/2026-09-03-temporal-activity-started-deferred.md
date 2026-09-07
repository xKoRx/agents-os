---
type: learning
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
  - "[[2026-09-03-mt5-artifact-timeout-retry-loop]]"
  - "[[2026-09-03-echo-forge-cancel-drain-lifecycle]]"
aliases:
  - TEMPORAL_ACTIVITY_STARTED_DEFERRED
  - pendingActivities authority
  - TEMPORAL_DISPATCH_VISIBILITY_ANOMALY retired
confidence: verified
source_session: ECHO-FORGE-MT5-TIMEOUT-RETRY-AND-RELEASE-ISOLATION-V1-TOP
load_policy: when_project_loaded
indexable: true
index_priority: high
tags:
  - kind/learning
  - scope/project
  - project/echo-forge
  - tech/temporal
---

# 2026-09-03-temporal-activity-started-deferred

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Aprendizaje

- Temporal difiere `ActivityTaskStarted` en Event History hasta que la Activity completa o agota retries. `ActivityTaskScheduled` presente + `ActivityTaskStarted` ausente durante ejecución/retries es semántica esperada, no anomalía de dispatch.
- Autoridad de runtime: `DescribeWorkflowExecution` → `pendingActivities` (`activityId`, `state`, `attempt`, `lastFailure`, `lastWorkerIdentity`, heartbeat). `last_started=1970-01-01` es coherente con Started diferido.
- Retirar la clasificación `TEMPORAL_DISPATCH_VISIBILITY_ANOMALY` salvo evidencia nueva independiente de esta semántica.

## Aplicabilidad

- **Cuándo cargarlo:** diagnóstico de activities MT5/SQX con history corto y ejecución física activa.
- **Cuándo no cargarlo:** auditoría de Event History post-cierre, donde Started sí aparece al completar.

## Entidades relacionadas

- [[Echo Forge - Arquitectura de Datos y Migración de Persistencia]] · [[2026-09-03-mt5-artifact-timeout-retry-loop]]

## Evidencia

- Fuente: checkpoint 2026-09-03 de [[Echo Forge - Arquitectura de Datos y Migración de Persistencia]] — pendingActivities `state=Scheduled` attempt=2 `last_worker_identity=30160@worker-kronos@` mientras terminal64 ejecutaba `backtest\5-2`.
