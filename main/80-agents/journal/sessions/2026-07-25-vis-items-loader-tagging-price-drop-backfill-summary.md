---
type: session
scope: session
created: 2026-07-25
updated: 2026-07-25
area: "[[Meli]]"
project: "[[Bajó de Precio]]"
application: "[[vis-items-loader-tagging]]"
entities:
  - "[[vis-items-loader-tagging]]"
  - "[[Bajó de Precio]]"
related:
  - "[[2026-07-25-vis-items-loader-tagging-price-drop-backfill-raw]]"
  - "[[2026-07-25-vis-items-loader-tagging-backfill-entity-updated]]"
confidence: verified
source_session: "[[2026-07-25-vis-items-loader-tagging-price-drop-backfill-raw]]"
load_policy: manual
indexable: false
priority: never
tags:
  - kind/session
  - scope/session
  - area/meli
  - project/bajo-de-precio
  - app/vis-items-loader-tagging
---

# Resumen — Price Drop Motors Backfill

## Objetivo

Agregar a `vis-items-loader-tagging` una regularización retroactiva que reciba IDs, procese cada ítem de forma desacoplada y aplique las reglas históricas de Bajó de Precio Motors.

## Trabajo realizado

- Se agregó `POST /price-drop-motors-backfill`, con validación, normalización, deduplicación y publicación individual.
- Se agregó el tópico/consumer de trabajo `BIGQUEUE_TOPIC_PRICE_DROP_MOTORS_BACKFILL_TOPIC_NAME` y `POST /consume-price-drop-motors-backfill`.
- Se implementó un proceso aislado que consulta ítem e historial, identifica la última baja efectiva, valida ventana de 30 días, estabilidad previa, moneda, precio vigente, restricciones y umbrales.
- Se setea `PREVIOUS_PRICE` y se agenda su expiración por los días restantes.
- Tras una corrección del usuario, se eliminó el tópico/consumer de expiración paralelo y se reutilizó el calendario productivo existente.

## Decisiones

- El backfill posee un único tópico nuevo: el de trabajo.
- La expiración publica `PriceDropCalendarMessage` en `BIGQUEUE_TOPIC_PRICEDROP_BADGE_EXPIRE_TOPIC_NAME` y queda a cargo de `/consume-price-drop-calendar-cleanup`.
- Se mantuvo la lógica nueva duplicada y aislada, salvo el límite downstream que expresamente debe seguir siendo el flujo productivo.

## Validación

- `go test ./...`
- `go vet ./...`
- `go build ./...`
- `go test -race ./pkg/handlers ./pkg/services ./pkg/process/price_drop_motors_backfill`
- Swagger parseado correctamente y sin referencias al calendario paralelo eliminado.

## Pendientes

- Crear/configurar en infraestructura únicamente el tópico y consumer de trabajo del backfill.
- Revisar el diff y decidir stage, commit y push.

## Memoria

La verdad operativa quedó consolidada en `[[vis-items-loader-tagging]]` y se corrigió la memoria interna de continuidad. No se creó una nota L3: la conclusión es estado específico de la aplicación, no conocimiento general reusable.
