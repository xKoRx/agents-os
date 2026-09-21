---
type: known_error
schema_version: 1
scope: project
created: "2026-09-21"
updated: "2026-09-21"
area: "[[Echo]]"
project: "[[Echo — E-04 Forge Ingestion E1]]"
application:
entities:
  - "[[Echo]]"
related:
  - "[[Echo + Echo Forge — Environment Contract]]"
aliases:
  - FK KEY SHARE UPDATE privilege
  - write-once REVOKE UPDATE
confidence: verified
source_session:
load_policy: when_error_matches
indexable: true
index_priority: high
tags:
  - kind/known-error
  - scope/project
  - tech/postgres
---

# PostgreSQL FK KEY SHARE exige UPDATE en tablas write-once

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Síntoma

- INSERT en una tabla hija (p.ej. `echo.strategy_versions`) falla con `permission denied` sobre la tabla padre (`echo.strategy_identity_mappings`) aunque el rol tenga SELECT+INSERT.
- El CONTEXT de PostgreSQL muestra `SELECT … FOR KEY SHARE`.

## Causa

- El chequeo de RI toma `FOR KEY SHARE` sobre la fila referenciada. Ese lock exige privilegio **UPDATE** en la tabla padre, no sólo SELECT.
- Un endurecimiento write-once vía `REVOKE UPDATE` deja el SELECT intacto y rompe los INSERT con FK.

## Impacto

- El Gateway puede copiar artefactos y luego devolver 503/error de persistencia: el path HTTP llega al commit y el FK aborta la transacción.

## Detección

- Reproducir el INSERT como el rol runtime (`echo_user`) y leer CONTEXT. `has_table_privilege(role, table, 'UPDATE')` en las tablas referenciadas.

## Mitigación

- Conservar triggers BEFORE UPDATE/DELETE write-once como autoridad de inmutabilidad.
- GRANT UPDATE al rol runtime sobre las tablas identity/promotion referenciadas. No usar REVOKE UPDATE como único control write-once.
- No reescribir filas: el trigger sigue bloqueando UPDATE/DELETE reales.

## Evidencia

- DEV `echo-develop` 2026-09-21: ingestión Gateway falló hasta GRANT UPDATE; receipt `338bd937-95ad-4389-9278-89285908b0a6` INGESTED después. Detalle: `~/aranea/work/echo-dev-ingest-close-20260921/FINDINGS-INGEST-CLOSE-20260921.md`.
