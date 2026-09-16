---
type: change_log
schema_version: 1
scope: session
created: "2026-09-15"
updated: "2026-09-15"
area: "[[Meli]]"
project: "[[SIG-616 — Autorización de operaciones por equipo]]"
application:
entities:
  - "[[SIG-616 — Autorización de operaciones por equipo]]"
related:
  - "[[SPEC técnica — Slice 3 — Mutaciones y deployments de componentes]]"
  - "[[SPEC técnica — Slice 4 — Relaciones y pipelines]]"
  - "[[SPEC técnica — Slice 5 — Actions restantes]]"
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

# SIG-616 — SPECs técnicas de Slice 3, 4 y 5 creadas

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** created + updated
- **Archivo(s):**
  - `10-projects/Meli/SIG-616 — Autorización de operaciones por equipo/SPEC técnica — Slice 3 — Mutaciones y deployments de componentes.md`
  - `10-projects/Meli/SIG-616 — Autorización de operaciones por equipo/SPEC técnica — Slice 4 — Relaciones y pipelines.md`
  - `10-projects/Meli/SIG-616 — Autorización de operaciones por equipo/SPEC técnica — Slice 5 — Actions restantes.md`
  - `10-projects/Meli/SIG-616 — Autorización de operaciones por equipo/SIG-616 — Autorización de operaciones por equipo.md`

## Motivo

- El owner pidió materializar las SPECs técnicas de las entregas 3, 4 y 5, eliminar el gate final y exigir que cada PR complete sus propias pruebas y verificaciones.

## Fuentes usadas

- SIG-616 de Spellbook como requerimiento original.
- SIG-621 como SPEC funcional padre y SIG-622/SIG-623 como precedentes técnicos.
- Código y contratos actuales de `rio-playmaker`, inspeccionados sin modificar el worktree de Slice 2.
- `fury_rio-controlplane-clickhouse@7de630c6cac5`: `ClickHouseActionContract` y `ListWarehousesAction`.
- `fury_rio-frontend@6d644ec6a417`: `api/services/warehouses.ts#dispatchWarehouseLookup`.
- Decisiones consolidadas y SPECs locales de Slice 1 y Slice 2.

## Resolución aplicada

- Se crearon tres SPECs técnicas locales encadenadas sobre el head aprobado de la entrega anterior.
- Cada SPEC incluye alcance, rutas, arquitectura, decisiones, archivos, matriz de pruebas, gate de datos, smoke, coverage, rollout, tareas y criterios de aceptación en su mismo PR.
- Se actualizó el proyecto para reflejar cinco slices de código y la ausencia de una fase final de pruebas.
- La publicación remota quedó pendiente porque la sesión de la CLI de Spellbook expiró.
- Tras la revisión cruzada se documentó evidencia contractual y de consumo para `list-warehouses-for-team`; `ping` pasó a ser un check explícito y bloqueante del gate de rollout de Slice 5.

## Validación

- Las tres SPECs quedaron entre 6k y 15k caracteres, con secciones técnicas y gates por PR completos.
- El lint estricto de la entidad de proyecto y este change log terminó con `ERROR=0` y `WARN=0`.
- El canonical linter no reportó findings sobre el proyecto, las tres SPECs ni este change log; mantiene findings preexistentes fuera del alcance de SIG-616.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** no aplica para distribución externa; contiene rutas operativas locales y trazabilidad interna, sin secretos.

## Rollback

- Eliminar las tres SPECs locales y revertir únicamente las secciones agregadas al proyecto. No se modificó código ni estado externo.
