---
type: change_log
scope: session
created: 2026-07-25
updated: 2026-07-25
area: "[[Meli]]"
project: "[[Bajó de Precio]]"
application: "[[vis-items-loader-tagging]]"
related:
  - "[[2026-07-25-vis-items-loader-tagging-price-drop-backfill-summary]]"
confidence: verified
source_session: "[[2026-07-25-vis-items-loader-tagging-price-drop-backfill-raw]]"
load_policy: never
indexable: false
priority: never
tags:
  - kind/change-log
  - scope/session
  - change/updated
  - change/conflict-resolution
  - app/vis-items-loader-tagging
---

# Cambio — Arquitectura del backfill de Bajó de Precio Motors

## Contradicción

La primera versión del código y de la memoria de continuidad afirmaba que el backfill tendría tópico y consumer de expiración propios. El usuario aclaró que ese efecto pertenece al flujo productivo normal.

## Resolución

- Se eliminaron el tópico, consumer y proceso de expiración exclusivos del backfill.
- Se extendió `PriceDropCalendarPublisher` para aceptar `attributeSetAt` y `deliveryTime` retroactivos sin cambiar el contrato del mensaje.
- El backfill ahora publica en `BIGQUEUE_TOPIC_PRICEDROP_BADGE_EXPIRE_TOPIC_NAME`; `/consume-price-drop-calendar-cleanup` conserva el apagado y la detección de ciclos.
- Se corrigieron la memoria interna, `[[vis-items-loader-tagging]]` y la bitácora de `[[Bajó de Precio]]`.

## Evidencia

- `cmd/api/initializers/resources.go`
- `pkg/services/price_drop_calendar_publisher.go`
- `pkg/process/price_drop_motors_backfill/price_drop_motors_backfill.go`
- `docs/guide/processes/price_drop_motors_backfill.md`

## Validación

Suite completa, vet, build y race tests focalizados exitosos. Una búsqueda negativa confirmó que no quedan símbolos, rutas ni variables de un calendario de backfill separado.

## Rollback

Revertir las ediciones de las entidades y de la memoria interna, y restaurar el código anterior desde el diff local si la arquitectura vuelve a cambiar.
