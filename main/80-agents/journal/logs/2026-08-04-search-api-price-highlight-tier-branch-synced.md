---
type: change_log
scope: session
created: "2026-08-04"
updated: "2026-08-04"
area: "[[Meli]]"
project: "[[Destaque de Precio Search — Search API Go]]"
application: "[[search-api-go]]"
entities:
  - "[[Destaque de Precio Search — Search API Go]]"
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
  - app/search-api-go
---

# Search API — rama de PRICE_HIGHLIGHT_TIER sincronizada

## Cambio

- Se integró `origin/develop` en `feature/price-highlight-tier-search-api`.
- Se resolvió el conflicto de allowlist conservando `PRESCRIPTION_TYPE` y
  `PRICE_HIGHLIGHT_TIER`.
- Se creó el merge commit `3d432c4f16` y se publicó en origin.

## Validación

- Tests focalizados de entity, usecase y process: pasan.
- `go test ./...`: pasa.
- `HEAD` coincide con `origin/feature/price-highlight-tier-search-api`.

## Pendiente

- G8/G9 del proyecto siguen esperando deploy/reprocess y validación en una
  respuesta real.
