---
type: decision
schema_version: 1
scope: project
created: 2026-07-28
updated: 2026-08-10
area: "[[Meli]]"
project: "[[Hito 2 - vis-items-loader-tagging]]"
application: "[[vis-items-loader-tagging]]"
entities:
  - "[[Destaques de Precio]]"
  - "[[Bajo y Muy Bajo Precio]]"
related: []
aliases: []
confidence: high
load_policy: manual
indexable: true
index_priority: high
tags:
  - kind/decision
  - scope/project
---

## Contexto

Decisión histórica migrada al contrato vigente.

## Decisión

---
type: decision
scope: project
created: 2026-07-28
updated: 2026-07-28
area: "[[Meli]]"
project: "[[Hito 2 - vis-items-loader-tagging]]"
application: "[[vis-items-loader-tagging]]"
entities:
  - "[[Destaques de Precio]]"
  - "[[Bajo y Muy Bajo Precio]]"
related:
  - "[[Hito 2 - vis-items-loader-tagging]]"
aliases:
  - independent-price-signals
  - vehicle-price-highlight-site-scopes
confidence: verified
source_session: codex-2026-07-28-hito-2-independent-price-signals
load_policy: when_project_loaded
indexable: true
index_priority: high
tags:
  - kind/decision
  - area/meli
  - app/vis-items-loader-tagging
  - feature/destaques-de-precio
  - scope/project

# Motors pricing signals use independent site scopes

## Contexto

El processor común de Motors debe convivir con Bajó de Precio y Destaque de Precio sin forzar que ambas señales estén activas en los mismos sites. El plan anterior describía una ejecución siempre conjunta y contemplaba un handler adicional para enrutar eventos.

## Decisión

- Mantener un único `vehicle_price_highlight_motors` como implementación de `models.Processor`, con subprocesadores internos seleccionados por filtro y scope.
- Mantener dos configuraciones operativas: `price_before_discount_motors` para MLB/CARS_AND_VANS y `vehicle_price_highlight_motors` para MLA/MLM. El wiring deriva sólo la unión de sites para el filtro externo del processor.
- No agregar un handler Motors; la entrada permanece en `/consume-process-item`.
- Reutilizar `PriceDropAttributes` para que el legacy y el processor común compartan la construcción de `PREVIOUS_PRICE`, `HAS_LOWER_PRICE` y expiración.
- Clasificar Destaque de Precio con `VERY_LOW` si `lower_limit <= price < lower_band`, `LOW` si `lower_band <= price <= estimated_price * 0.98`, y `NORMAL` en cualquier otro caso. No emitir una mutación cuando el valor persistido ya coincide.

## Rationale

La configuración es la fuente de activación por site y evita duplicar processors o umbrales. El filtro common permite que el mismo proceso sea enrutable para ambos sites; el filtro legacy conserva compatibilidad selectiva para Bajó de Precio. La regla `NORMAL` evita dejar tiers anteriores cuando el ítem deja de estar en una banda válida.

## Consecuencias

- MLB ejecuta Bajó de Precio y no consulta el Sugeridor de Destaque.
- MLA/MLM ejecutan Destaque de Precio y no ejecutan la lógica de Bajó de Precio.
- `go test ./...` valida el wiring, la selección por site/filtro, los bordes de bandas y los errores reintentables.
- La eliminación de la instancia Motors legacy queda como un despliegue posterior, una vez drenados sus mensajes.

## Alternativas descartadas

- Crear un handler dedicado para Motors: agrega una entrada operativa innecesaria y rompe el flujo estándar existente.
- Ejecutar siempre ambos subprocesadores: impide activar las señales de forma independiente y puede aplicar una señal fuera de su site.


## Consecuencias

- Consultar el contenido histórico y validar su vigencia antes de aplicar.
