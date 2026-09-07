---
type: learning
scope: agent
created: "2026-07-01"
updated: "2026-07-01"
area: "[[Meli]]"
project: "[[Search Middleware - Correccion Bajo de Precio Motors]]"
application: search-middleware
entities:
  - "[[Meli]]"
  - "[[search-middleware]]"
related:
  - "[[Bajó de Precio]]"
aliases:
  - preservar semantica legacy al extender features
  - no relajar reglas historicas de otra vertical
confidence: high
source_session: "2026-07-01-search-middleware-re-price-drop-regression-closeout"
load_policy: contextual
indexable: true
index_priority: high
tags:
  - kind/learning
  - workflow/code-review
  - application/search-middleware
---

# Preservar Semantica Legacy Al Extender Features Multi-Verticales

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Aprendizaje

- Cuando una feature existente se extiende a una nueva vertical, primero hay que capturar en tests la semántica anterior de las verticales ya soportadas. El refactor no debe relajar reglas históricas salvo requerimiento explícito.
- Si una abstracción nueva reemplaza un helper local, validar que no se pierdan condiciones de borde escondidas en el helper anterior. En search-middleware, mover price drop de `PriceDropExperimentHelper` a reglas/gate eliminó la exclusión `domainId.contains("DEVELOPMENT")` para Real Estate.
- Los tests nuevos pueden esconder regresiones si actualizan expectativas para coincidir con el refactor en vez de preservar comportamiento previo. Revisar tests renombrados o invertidos como señales de riesgo.

## Aplicabilidad

- **Cuándo cargarlo:** al extender una feature por vertical/canal/plataforma, al refactorizar helpers existentes, o al responder reviews que indican pérdida de lógica histórica.
- **Cuándo no cargarlo:** cambios greenfield sin comportamiento legacy o refactors puramente mecánicos con equivalencia probada por tests existentes.

## Entidades relacionadas

- [[Meli]]
- [[Bajó de Precio]]
- [[Search Middleware - Correccion Bajo de Precio Motors]]
- [[search-middleware]]

## Evidencia

- Fuente: sesión `2026-07-01-search-middleware-re-price-drop-regression-closeout`.
- Prueba: `RealEstatePriceDropRule.appliesTo` pasó a aceptar todo `ItemVertical.REAL_ESTATE`, perdiendo la exclusión `DEVELOPMENT` de `PriceDropExperimentHelper.isIndividualRealEstateItem`; el review detectó que Real Estate podía emitir price drop, comportamiento antes prevenido.
