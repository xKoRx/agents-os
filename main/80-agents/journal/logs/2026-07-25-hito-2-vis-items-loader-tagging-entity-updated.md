---
type: change_log
scope: session
created: "2026-07-25"
updated: "2026-07-25"
area: "[[Meli]]"
project: "[[Implementación Hito 2 - Destaques de Precio]]"
application: "[[vis-items-loader-tagging]]"
entities:
  - "[[Hito 2 - vis-items-loader-tagging]]"
related:
  - "[[Destaques de Precio]]"
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
  - area/meli
---

# Hito 2 vis-items-loader-tagging — plan de implementación actualizado

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `10-projects/Destaques de Precio/agentes/Hito 2 - vis-items-loader-tagging.md`
  - `10-projects/Destaques de Precio/Implementación Hito 2 - Destaques de Precio.md`

## Motivo

- El usuario confirmó el contrato del tercer atributo y pidió un plan de
  implementación escalable que integre Bajó de Precio y Destaque de Precio.

## Fuentes usadas

- Declaración del usuario del 2026-07-25:
  `VEHICLE_PRICE_HIGHLIGHT_TIER` usa `LOW` / `VERY_LOW` o limpieza.
- Repositorio `/Users/rjara/fuentes/vis-items-loader-tagging`, baseline vigente
  `3dce2f29534d9da73f5f63b63aab103592c524ce` sobre `develop`.
- `pkg/middlewares/filter.go`, `pkg/handlers/bq_consumer.go`,
  `pkg/orchestrator/orchestrator.go`,
  `pkg/process/price_before_discount/price_before_discount.go`,
  `pkg/process/price_drop_calendar_cleanup/price_drop_calendar_cleanup.go`.

## Resolución aplicada

- Se dejó un plan phase-gated con exactamente tres paquetes:
  1. procesamiento unitario común para Bajó de Precio y Destaque de Precio;
  2. proceso masivo basado en una única lista materializada de IDs y páginas
     autocontenidas;
  3. consumer de cambios en atributos baneadores.
- Se eliminó la propuesta de paginación keyset y el término Backfill para esta
  capacidad. Los consumers de página no consultan BigQuery.
- Se movió la tarea puente del producer a WIP y se cerró la definición del
  contrato producer en el proyecto humano.
- El plan queda bloqueado antes de Fase 1 hasta cerrar las reglas exactas del
  Sugeridor y validar la granularidad del evento de atributos.

## Validación

- Referencias de código verificadas contra el working tree actual.
- `validate_plan.py`: 3 fases, 3 gates, 3 despachos, 11 referencias locales,
  0 errores y 0 warnings.
- Working tree del repositorio de aplicación preservado: solo permanecen los
  archivos no versionados preexistentes del usuario.
- Graphify reindexado correctamente; `explain` resolvió el nodo canónico
  `Hito 2 - vis-items-loader-tagging` y sus secciones principales.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** no contiene secretos ni datos de ítems.

## Rollback

- Revertir las dos notas de proyecto y eliminar este log.
