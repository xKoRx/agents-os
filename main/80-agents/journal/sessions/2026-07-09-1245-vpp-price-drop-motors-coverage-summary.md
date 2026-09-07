---
type: session
scope: session
created: 2026-07-09
updated: 2026-07-09
area: "[[Meli]]"
project: "[[Bajó de Precio]]"
application: "[[vpp-backend]]"
entities:
  - "[[Bajó de Precio]]"
  - "[[vpp-backend]]"
related: []
aliases: []
confidence: high
source_session:
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/session
  - scope/session
---

# VPP Price Drop Motors Coverage — summary

## Objetivo

- Revisar el diff de Bajo de Precio Motors y elevar la cobertura de PR.

## Trabajo realizado

- Se removieron tests que representaban una VIP RE y Motors simultáneamente.
- Se agregó matriz de escenarios Motors sin suscripción RES y una aserción de reemplazo de `originalValue`.
- Se validaron suites focales y `jacocoTestReport`.

## Evidencia

- Suites focales: 682 tests, cero fallas.
- JaCoCo local: 100% de líneas para `PriceDeprecatedComponentTask` y `VipMotorsViewTrackingInfoTask`; sin misses en el método modificado de `PriceMarshaller`.

## Pendiente

- Fury debe recalcular el baseline remoto; `git diff --check` completo sigue reportando whitespace ajeno en documentación Pharma.
