---
type: change_log
schema_version: 1
scope: session
created: "2026-08-27"
updated: "2026-08-27"
area: "[[Echo Forge]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[Symphony]]"
entities:
  - "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
related:
  - "[[2026-08-27-zcode-glm-5-3-sqx-cross-flowrun-historical-source-rca-top]]"
aliases: []
confidence: verified
source_session: SQX-CROSS-FLOWRUN-HISTORICAL-SOURCE-RESOLUTION-RCA-TOP
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
  - project/echo-forge
---

# 2026-08-27-sqx-cross-flowrun-historical-source-rca

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** conflict-resolution
- **Archivo(s):**
  - `10-projects/Echo Forge/agentes/Echo Forge - Arquitectura de Datos y Migración de Persistencia.md` (checkpoint append-only con la resolución completa F1–F24).

## Motivo

Cerrar el gap REQUIRED #1 del spec FEAT-SQX-CROSS-FLOWRUN-REUSE (FD-4): definir con evidencia física y de código la arquitectura mínima exacta para que un FlowRun nuevo use como input un output histórico de otro FlowRun seleccionado mediante SourceFolder, sin reabrir el ownership certificado (OUTPUT_NAMESPACE_OWNERSHIP: CERTIFIED_CLOSED).

## Fuentes usadas

- Repo `xKoRx/symphony` @ `2b73dc3` (read-only; 4 auditorías subagente + spot-check padre); PostgreSQL físico `trading_systems_test` (esquema, constraints, ownership, stage executions); Mongo físico `forge.evaluations` (BSON, índices, 6319 docs); MinIO `sqx-strategies` (censo 52.605 objetos); cohorts E2E 0.2.73 (BUILDER FlowRun `52e93a46`, 20 Evaluations) y 0.2.74 (RETESTER FlowRun `291c53f2`, 15 siblings: 12 con evidencia + 3 empty).

## Resolución aplicada

Arquitectura mínima congelada: `SourceFolder` + metadata → `BuildMinIOPath` → ownership exact-read (`LoadOutputNamespaceOwner` nuevo port PG) → gate `owner FlowRun status == COMPLETED` → query Mongo `evaluations` por `flow_run_ref` + `$elemMatch(role=OUTPUT, artifact_type=STRATEGY_SQX, bucket, object_key prefix=namespace)` (índice existente, sin índice nuevo) → carriers `runtime.StrategyArtifact{StrategyRef, EvaluationRef, CanonicalStrategyID, Key}` enriquecidos con `LoadStrategyIdentity` → `DurableInputs` → prepareDurable* existentes. Fail-closed en cada anomalía (F22); pre-007 DEFER (multi-owner físicamente demostrado); OPTION A AWKWARD / OPTION C OVERMODELING / OPTION D LEGACY_ONLY. Implementación para `SQX-CROSS-FLOWRUN-HISTORICAL-SOURCE-RESOLUTION-CORRECTION-NORMAL`.

## Validación

- PASS: proofs físicos exactos BUILDER 20/20 y RETESTER 12/12+3 empty contra datos reales del release 0.2.73/0.2.74; HEAD == baseline; repo sin cambios (`CODE_CHANGE_REQUIRED: YES` pero NO implementado por diseño read-only); convergencia de 4 auditorías independientes.
- Nota: acceso físico directo PG/Mongo/MinIO verificado viable desde la máquina local con herramientas Go read-only (corrige limitación documentada por sesiones previas).

## Compartibilidad

- **Scope:** local / team
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos (credenciales referenciadas como claves etcd, nunca valores)

## Rollback

Reversible documentalmente: revertir el checkpoint append; no se tocó código, schema, migraciones ni specs del repo.
