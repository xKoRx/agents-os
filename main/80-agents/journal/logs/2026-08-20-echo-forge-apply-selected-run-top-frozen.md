---
type: change_log
schema_version: 1
scope: session
created: "2026-08-20"
updated: "2026-08-20"
area: "[[Echo]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[echo-forge]]"
entities:
  - "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
  - "[[Echo Forge]]"
related:
  - "[[2026-08-19-echo-forge-a6-big-bang-supersedes-a5]]"
  - "[[2026-08-20-codex-gpt-5-echo-forge-apply-selected-run-top]]"
aliases: []
confidence: verified
source_session:
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# Echo Forge apply-selected-run TOP frozen

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** created + updated
- **Archivo(s):**
  - `10-projects/Echo Forge/agentes/Echo Forge - Arquitectura de Datos y Migración de Persistencia.md`
  - `10-projects/Echo Forge/Echo Forge.md`
  - repo `xKoRx/symphony` commit `1864a807babcd3e4db3829d8ed2a30985e70fb9b`

## Motivo

Se congeló el contrato durable de la aplicación física de la Decision exacta producida por `select_robust_run`, sin implementación productiva, migración SQL, rewrite de workflows ni regeneración de Graphify.

## Fuentes usadas

- `specs/FEAT-SQX-DURABLE-PERSISTENCE-FOUNDATION/DATA_MODEL.md`
- `specs/FEAT-SQX-DURABLE-ROBUST-SELECTION/SPEC.md`
- `specs/FEAT-SQX-DURABLE-ROBUST-SELECTION/TOP-DECISIONS.md`
- `specs/FEAT-SQX-DURABLE-WFM/SPEC.md`
- código brownfield, exporter Java, bindings durable Optimizer/WFM/MinIO/PostgreSQL y workflows reales en baseline `19f2291d177380595f576f61407e659243dc516e`

## Resolución aplicada

`APPLY-SELECTED-RUN-TOP` queda `DONE / APPROVED / FROZEN`: aplica una Decision exacta, produce una Evaluation immutable con un único `OUTPUT/STRATEGY_SQX` y cero MetricSets, usa config tipada durable para runs/oos/magic/symmetry, serializa el proyecto físico por flock, persiste por key determinista y conserva Strategy/Decision en el carrier. Foundation sólo incorpora una lectura mínima por ref de identidad/generación de StageExecution. Siguiente slice exacto: `APPLY-SELECTED-RUN-NORMAL`.

## Validación

`git diff --cached --check` PASS; commit documental de tres archivos; `HEAD == origin/master == 1864a807babcd3e4db3829d8ed2a30985e70fb9b`; Graphify permanece `13735 nodes / 28921 edges` con `built_at_commit=286aad75e14dcf146e9935cea5db7265dc1f76f8`; los tres foreign dirty permanecen fuera del commit.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

Revertir el commit `1864a807babcd3e4db3829d8ed2a30985e70fb9b` en Symphony y retirar únicamente el checkpoint APPLY-SELECTED-RUN-TOP de la nota canónica, preservando el cierre ROBUST-SELECTION-NORMAL y el resto de A6.
