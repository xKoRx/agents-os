---
type: change_log
scope: session
created: 2026-07-28
updated: 2026-07-28
area: "[[Meli]]"
project: "[[Hito 2 - vis-items-loader-tagging]]"
application: "[[vis-items-loader-tagging]]"
entities:
  - "[[Destaques de Precio]]"
  - "[[Bajo y Muy Bajo Precio]]"
related:
  - "[[Motors pricing signals use independent site scopes]]"
aliases: []
confidence: high
source_session: codex-2026-07-28-hito-2-independent-price-signals
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
  - area/meli
  - app/vis-items-loader-tagging

# Independent Motors pricing signal scopes

## Cambio

- Actualizado el proyecto de Hito 2 para reflejar subprocesadores independientes, dos configuraciones site-scoped y ausencia de handler nuevo.
- Creada la decisión reusable `[[Motors pricing signals use independent site scopes]]`.

## Motivo

El owner solicitó mantener Bajó de Precio sólo en MLB y Destaque de Precio sólo en MLA/MLM, con selección dependiente de filtros y corrección de la semántica de bandas.

## Validación

- `go test ./...` pasó.
- `git diff --check` pasó.
