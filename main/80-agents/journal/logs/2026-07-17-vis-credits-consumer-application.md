---
type: change_log
scope: session
created: 2026-07-17
updated: 2026-07-17
area: "[[Meli]]"
application: "[[vis-credits-consumer]]"
entities:
  - "[[vis-credits-consumer]]"
  - "[[vis-items-loader-tagging]]"
related: []
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
  - app/vis-credits-consumer
  - change/created
---

# Crear aplicación vis-credits-consumer

## Cambio

- **Tipo:** created
- **Archivo(s):**
  - `30-resources/applications/vis-credits-consumer.md`
  - `30-resources/applications/00-index.md`
  - `30-resources/applications/log.md`

## Motivo

- Registrar en la wiki de aplicaciones el consumer de Credits que integra Segments Wrapper con Item API y completa sale terms de financiabilidad para Motors.

## Fuentes usadas

- Repositorio local `~/fuentes/vis-credits-consumer`.
- `controllers/item.go`, `services/item.go`, `clients/segments.go`, `config/application.properties`.
- Relación existente en `~/fuentes/vis-items-loader-tagging`.

## Resolución aplicada

- Se creó una única entidad canónica con aliases del repo y del nombre operativo.
- Se documentó `POST /vis-credits-consumer/item-financeable` como endpoint que llama a Segments Wrapper y escribe `IS_FINANCEABLE_VEHICLE_RISK_PROFILE` para `MLB-CARS_AND_VANS`.

## Validación

- Búsqueda de duplicados en `30-resources/`, proyectos y áreas: sin coincidencias previas.
- `graphify-obsidian explain "vis-credits-consumer.md"` antes de crear: sin nodo existente.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin credenciales ni secretos.

## Rollback

- Eliminar la página, su fila de índice, la entrada de `applications/log.md` y este change log; luego reindexar Graphify.
