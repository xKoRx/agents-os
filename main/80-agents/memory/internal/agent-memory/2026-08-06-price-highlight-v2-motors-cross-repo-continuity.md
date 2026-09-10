---
type: agent_memory
schema_version: 1
scope: session
created: 2026-08-10
updated: 2026-09-09
memory_state: archived
area: "[[Personal]]"
project:
application:
entities: []
related: []
confidence: medium
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/agent-memory
  - scope/session
---

## Continuidad

# Price highlight V2 Motors — cross-repo continuity

## Estado al cierre

- SDK branch: `feature/price-highlight-tier`.
  - `PriceDecorator` (V1) y `PriceV2Decorator` renderizan `PRICE_HIGHLIGHT_TIER`.
  - La tipografía del destaque quedó en `XS`; se conservaron los paddings originales (`2/4`) y se descartaron los aumentos fallidos.
  - Versión de trabajo: `0.0.5-price-highlight-tier`.
- Search Middleware branch: `feature/price-highlight-tier`.
  - `PriceDropExperimentModel` lee `showPill` y `showHighlight` como flags independientes.
  - Force params independientes: `price-drop-motors.force` y `price-highlight-motors.force`.
  - El flujo task-path y el registry legado configuran `withPriceHighlightTier` para Motors.
  - Con `showHighlight=true`, Motors selecciona PriceV2 si la plataforma/versión soporta el contrato; en caso contrario conserva PriceV1 como fallback.
  - La dependencia apunta a `0.0.6-price-highlight-tier`.
  - Se integró desde `feature/price-highlight-tier-test` el mock de visualización: en scopes cuyo nombre contiene `test`, Search API inyecta tiers `NORMAL`, `LOW` y `VERY_LOW` de forma rotativa en ítems Motors, y el experimento activa `showPill` + `showHighlight`.

## Validación

- Pasaron los tests focalizados de destaque V1/V2 del SDK.
- El SDK `0.0.5-price-highlight-tier` se publicó solo en Maven local para validar Search.
- Pasaron los tests focalizados de `PriceDropMotorsExperimentTask` y ambos `PriceDecoratorFactory` de Search.
- `git diff --check` quedó limpio en ambos repos.
- El checkstyle global de Search no es una señal accionable: emite millones de errores preexistentes fuera de estos archivos y se interrumpió. Los archivos modificados compilaron y sus suites pasaron.

## Siguiente paso

Publicar `0.0.5-price-highlight-tier` en el repositorio de artefactos antes de ejecutar CI de Search; luego revisar, commitear y subir cada rama. Los archivos no trackeados preexistentes de ambos repos se preservaron.


## Señales de carga

- Cargar sólo cuando la entidad o síntoma coincida con esta continuidad.
