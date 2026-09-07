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
  - "[[2026-08-20-cursor-grok-4.6-echo-forge-wfm-n5]]"
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

# Echo Forge WFM-N5 closed

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `10-projects/Echo Forge/agentes/Echo Forge - Arquitectura de Datos y Migración de Persistencia.md`
  - repo `xKoRx/symphony` commit `74443bd` (`feat: close durable WFM migration`)

## Motivo

Cerrar la migración durable de WFM: clasificar unknown producer status como non-retryable, endurecer recovery semántico CELL/MetricSet, desconectar writers legacy y rechazar el contrato público `wfm_exporter`.

## Fuentes usadas

- `specs/FEAT-SQX-DURABLE-WFM/SPEC.md`
- nota canónica del proyecto de persistencia
- HEAD previo `c278f53e7beae2ccf00eb9b0d4b1be7410a0e7a5`

## Resolución aplicada

WFM-N5 PASS. DURABLE WFM FINAL PASS / CLOSED. No N6. Siguiente: ROBUST-SELECTION-TOP.

## Validación

`go test` binding/worker-WFM/workflows-WFM/storage-minio/core-wfm PASS. `go test ./sqx/...` PASS salvo PREEXISTING `sqx/tools` multiple main. Race WFM PASS. Graphify 13514/28201 → 13548/28357.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

Revertir `74443bdd986683ec9d0638d9caacc3c668c3f3d9` en `xKoRx/symphony` y restaurar el checkpoint WFM-N4 en la nota del proyecto.
