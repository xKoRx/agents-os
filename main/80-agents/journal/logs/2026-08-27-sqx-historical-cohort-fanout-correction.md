---
type: change_log
schema_version: 1
scope: session
created: "2026-08-27"
updated: "2026-08-27"
area: "[[Echo]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[xKoRx/symphony]]"
entities:
  - "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
related:
  - "[[2026-08-27-historical-cohort-resolution-at-group-boundary]]"
  - "[[2026-08-27-codex-unknown-sqx-cross-flowrun-historical-source-fanout-correction-normal]]"
aliases: []
confidence: verified
source_session: SQX-CROSS-FLOWRUN-HISTORICAL-SOURCE-FANOUT-CORRECTION-NORMAL
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-08-27-sqx-historical-cohort-fanout-correction

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated
- **Archivo(s):** `sqx/activities/worker/historical_cohort_activity.go`, `sqx/workflows/generic_workflow.go`, wiring/tests/specs del commit `a211734`.
- **Contrato:** la resolución histórica se ejecuta una vez por cohort en `resolve_historical_cohort` dentro del boundary durable del grupo; el fan-out conserva un artifact exacto por key.

## Motivo

La inserción previa dentro de ProjectActivity entregaba N artifacts a una ejecución que exige exactamente una Strategy. La corrección mueve la misma capa de datos sin duplicarla ni rediseñarla y elimina la evasión de recortar el cohort en tests.

## Fuentes usadas

- Baseline exacto `fd042fbab658f750b363f3c0ed4280586356cfd3` y contrato canónico `specs/FEAT-SQX-CROSS-FLOWRUN-REUSE`.
- Activity/fan-out N=3/N=20, worker/core/metadata-mongo y `git diff --check` validados; commit `a211734486dfdb7e9a9bac6205276ad3757910de` publicado.

## Resolución aplicada

- Se creó la Activity narrow, se removió el step ProjectActivity, se registró el wiring del worker y se implementó la proyección exacta por slice con `batch_size` existente.
- Membership `REPROCESSED` ocurre antes del fan-out y same-flow vacío termina sin Mongo, membership ni fallback a `list_strats`.

## Validación

- PASS dirigido para la nueva Activity y fan-out; PASS para worker/core/metadata-mongo. Registry conserva sólo `TestUpsertStrategyV2_V0V1V2Coexistence`; workflows amplios conservan fallos preexistentes por `flow_run_start` no registrado.

## Compartibilidad

- **Scope:** local / team
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Revertir el commit `a211734486dfdb7e9a9bac6205276ad3757910de` restaura el código previo; no se modificó schema, índice, ownership, identidad ni MinIO path.
