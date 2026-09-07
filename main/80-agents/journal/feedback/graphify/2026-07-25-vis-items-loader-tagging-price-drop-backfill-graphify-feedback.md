---
type: graphify_feedback
scope: session
created: 2026-07-25
updated: 2026-07-25
area: "[[Meli]]"
project: "[[Bajó de Precio]]"
application: "[[vis-items-loader-tagging]]"
related:
  - "[[2026-07-25-vis-items-loader-tagging-price-drop-backfill-summary]]"
confidence: high
source_session: "[[2026-07-25-vis-items-loader-tagging-price-drop-backfill-raw]]"
load_policy: never
indexable: false
priority: never
tags:
  - kind/graphify-feedback
  - scope/session
  - area/meli
  - app/vis-items-loader-tagging
---

# Graphify feedback — Price Drop Motors Backfill

## Utilidad

3/5. Permitió ubicar rápido `[[vis-items-loader-tagging]]`, `[[Bajó de Precio]]` y el contexto de `PriceBeforeDiscount`, pero las consultas amplias trajeron bastante ruido para un cambio focalizado.

## Hallazgos útiles

- La aplicación era la entidad canónica correcta para guardar la topología vigente.
- El proyecto contenía la bitácora y el backlog humano adecuados para registrar el pendiente de infraestructura.
- La sesión exigía corregir una afirmación de continuidad previa antes de reindexar.

## Mejora sugerida

Priorizar queries dirigidas por símbolo, endpoint y nombre exacto de tópico; después usar `explain` solo sobre las entidades actualizadas. Para cambios acotados, resumir el resultado de `update` por notas afectadas.
