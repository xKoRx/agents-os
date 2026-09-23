---
type: change_log
schema_version: 1
scope: session
created: "2026-09-22"
updated: "2026-09-22"
area: "[[Meli]]"
project: "[[SIG-616 — Autorización de operaciones por equipo]]"
application:
entities:
  - "[[SIG-616 — Autorización de operaciones por equipo]]"
related:
  - "[[SPEC técnica — Slice 3 — Mutaciones y deployments de componentes]]"
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

# SIG-616 — Cierre de sincronización y variantes de prueba de Slice 3

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** conflict-resolution / updated
- **Archivo(s):**
  - `10-projects/Meli/SIG-616 — Autorización de operaciones por equipo/SIG-616 — Autorización de operaciones por equipo.md`

## Motivo

- Slice 3 debía quedar sincronizado con `develop`, estrictamente aditivo y con los findings válidos del bot resueltos antes de emitir nuevas versiones de prueba.

## Fuentes usadas

- PR #1178 en `8f9482210`, `develop@e26cf2baa`, threads de review, suites locales, commits publicados de ambas variantes y estados reportados por Fury.

## Resolución aplicada

- Se resolvió el conflicto del manifiesto por unión de escenarios/tests/checks; delete y patch compatible validan ahora la jerarquía persistida antes de ACME/efectos. Se actualizaron las ramas test3, se crearon `0.1.7-p3-committer-allowed` y `0.1.8-p3-viewer-denied`, y la nota canónica recibió la matriz manual de pruebas.

## Validación

- Suite completa y 17 selectores focalizados pasaron en F3. Los tests focalizados y contratos pasaron en ambas variantes. Fury terminó exitosamente las dos versiones desde los commits publicados; dos checks `LOCAL_STACK` quedaron bloqueados exclusivamente por Docker no disponible.

## Compartibilidad

- **Scope:** team
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Revertir sólo la actualización documental si la evidencia queda obsoleta. Para código o versiones, emitir commits/versiones correctivas; no borrar ramas ni versiones ya publicadas sin confirmar su consumo.
