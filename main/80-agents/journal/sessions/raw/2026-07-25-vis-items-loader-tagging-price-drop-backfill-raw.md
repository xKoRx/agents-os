---
type: raw_session
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
  - "[[2026-07-25-vis-items-loader-tagging-price-drop-backfill-summary]]"
confidence: verified
source_session:
load_policy: never
indexable: false
priority: never
tags:
  - kind/raw-session
  - scope/session
  - area/meli
  - project/bajo-de-precio
  - app/vis-items-loader-tagging
---

# vis-items-loader-tagging — Price Drop Motors Backfill

## Contexto

Implementación de un flujo retroactivo para regularizar ítems de Bajó de Precio Motors antes del rollout de Search y VPP.

## Transcripción

> Contenido disponible en la sesión fuente de Codex. Este placeholder preserva el ancla L0 sin duplicar el transcript completo.

## Evidencia

- Repo: `/Users/rjara/fuentes/vis-items-loader-tagging`
- Handler: `pkg/handlers/price_drop_motors_backfill_handler.go`
- Consumer: `pkg/handlers/price_drop_motors_backfill_consumer.go`
- Proceso: `pkg/process/price_drop_motors_backfill/price_drop_motors_backfill.go`
- Calendario productivo: `pkg/services/price_drop_calendar_publisher.go`
