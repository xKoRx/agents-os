---
type: runbook
schema_version: 1
scope: application
created: "2026-08-29"
updated: "2026-08-29"
area: "[[Echo Forge]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[xKoRx/symphony]]"
entities:
  - "[[Symphony]]"
related:
  - "[[readonly-production-probe]]"
  - "[[echo-forge-cross-system-triage]]"
aliases:
  - probe producción Symphony
  - herramienta read-only etcd/Temporal/MinIO/PG
confidence: verified
source_session: DURABLE-ARTIFACT-VERIFIED-READS-FINAL-E2E-NORMAL
load_policy: when_application_loaded
indexable: true
index_priority: high
tags:
  - kind/runbook
  - scope/application
  - project/echo-forge
---

# symphony-prod-probe

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Propósito

- Aplicar `readonly-production-probe` a Symphony: una herramienta Go única, efímera y read-only que consulta etcd/Temporal/MinIO/PostgreSQL/Mongo de producción vía el DI real de la app (sin secretos en código).

## Precondiciones

- Red a los servicios de producción (etcd y dependencias); módulo cache de Go poblado (builds previos del repo).

## Procedimiento

1. Crear UN archivo `scratch/probe_<sesion>_readonly.go` DENTRO de `~/go/src/github.com/xKoRx/symphony` (obligatorio: `internal/di` sólo es importable desde el módulo). Encabezado: herramienta operacional read-only de la sesión, no-producto, se elimina al cierre. Las credenciales/endpoints los resuelve `di.InitSelective` desde etcd — nada hardcodeado.
2. Esqueleto probado (firmas exactas del SDK `xKoRx/sdk` y temporal sdk v1.35): `di.InitSelective("sqx-worker", di.WithEnvironment("production"), di.WithEtcd(), di.WithTemporal(), di.WithMinIO(), di.WithPostgres())`; contenedor: `di.Container.Postgres.DB` (`*sql.DB` directo), `di.Container.MinIO` (`StatObject/GetObject/ListObjects(ctx, bucket, key)`), `di.Container.Temporal.Raw()` (client SDK: `DescribeTaskQueue(ctx, queue, enums.TaskQueueType)`, `DescribeWorkflowExecution(ctx, workflowID, runID)`, `GetWorkflowHistory(ctx, id, "", false, enums.HISTORY_EVENT_FILTER_TYPE_ALL_EVENT)` → iterator con `Next()`), namespace desde `di.Container.Etcd.Get("temporal/namespace")` (= `sqx-prop`).
3. Modos útiles por subcomando: `infra` (PG health + manifest deploy en MinIO), `queue` (pollers de `sqx-main-queue` y `sqx-mt5-queue`), `wf` (estado workflow + `stage_executions` por flow_run), `hist` (eventos con timestamps), `wave` (listing de prefijo MinIO con timestamps), `obj` (metadata+contenido de una key a `/tmp`).
4. Compilar/ejecutar: `go run scratch/probe_<sesion>_readonly.go <modo>`; si falla la resolución de módulos por el proxy Fury (403 sumdb), usar `GOFLAGS=-mod=mod GOPROXY=off GOSUMDB=off` (cache local).
5. Al cierre: `rm` del probe y verificar `git status --porcelain` = dirty preexistente únicamente.

## Validación

- Datos operacionales vigentes (2026-08-29): mongo `mongodb://192.168.31.221:27017` db `forge`; namespace Temporal `sqx-prop`; colas `sqx-main-queue` / `sqx-mt5-queue`; tablas control `sqx.flow_runs` (id, flow_intent_token, temporal_workflow_id, temporal_first_run_id, legacy_request_id, wave_key, status), `sqx.stage_executions` (stage_key, subject_*, temporal_activity_id, generation, status); bucket de artefactos `sqx-strategies`, bucket de deploy `deploy`; Loki/Jaeger en `192.168.31.60` (ver matriz en [[symphony-worker-runtime-proof]]).

## Rollback / recuperación

- Sin mutaciones no aplica rollback; el único riesgo es dejar el archivo: el cleanup está en el paso 5 y se verifica en el cierre.

## Evidencia

- Sesión 2026-08-29: el probe de esa sesión fue eliminado; patrón y firmas validados en runtime de producción; ver change log del día.
