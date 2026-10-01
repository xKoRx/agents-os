---
type: change_log
schema_version: 1
scope: session
created: "2026-10-01"
updated: "2026-10-01"
area: "[[Echo]]"
project: "[[Echo Futures]]"
application:
entities:
  - "[[Echo Futures]]"
related:
  - "[[Echo Futures/artifacts/d6-ninjatrader-certification-20260930/C1-NINJATRADER-ADAPTER-FIT-ANALYSIS]]"
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

# Echo Futures entity updated — 2026-10-01

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `10-projects/Echo Futures/Echo Futures.md`

## Motivo

- Primary Manager QA rechazó el PASS del worker C1 hasta reparar dos conclusiones materiales: semántica física del protective order y gate de entitlement del ProviderAccountBinding.

## Fuentes usadas

- Artifact `C1-NINJATRADER-ADAPTER-FIT-ANALYSIS.md`.
- Echo frozen baseline `xKoRx/echo@13e087a3bb762f65b060d3b3200fb00a67c6ff1d`.
- `v3/sdk/futures/gerardmm/gerardmm.go` y `v3/sdk/futures/domain/operation.go`.
- `v3/sdk/futures/domain/provider.go`.
- Documentación oficial NinjaTrader sobre Limit y Stop orders.

## Resolución aplicada

- `D6_C1_MANAGER_QA = REPAIR_REQUIRED`.
- Artifact worker preservado como evidencia; su gate PASS no fue promovido.
- No se autorizó implementación D6-N1 todavía.
- No se modificó product code D5.

## Validación

- Project note actualizada en commit `65a44d08b19bffe9e515fa60bd9657c393b20a84`.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin secretos ni credenciales.

## Rollback

- Revertir el commit del project note sólo si un repair posterior refuta ambos findings y el Primary Manager emite un nuevo QA.
