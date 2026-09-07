---
type: project
owner: agent
root: false
status: active
priority: P1
area: "[[Meli]]"
parent: "[[Cierre VIS]]"
sprint:
start: 2026-08-04
due:
progress: 0
repo: java-polycard-sdk
jira: VMDEM-22
prs:
aliases:
  - Implementación PRICE_HIGHLIGHT_TIER Java Polycard SDK
  - Destaque de Precio Polycard SDK
tags:
  - kind/project
  - area/meli
  - app/java-polycard-sdk
  - feature/destaques-de-precio
created: 2026-08-04
updated: 2026-08-04
cssclasses:
  - wide
---

# Destaque de Precio Search — Java Polycard SDK

%% Naming: plan de implementación del renderer de PRICE_HIGHLIGHT_TIER en PriceDecorator. Proyecto de agente bajo [[Cierre VIS]]. %%

> [!info]+ Java Polycard SDK — renderer de Destaque de Precio
> **Padre:** [[Cierre VIS]] · **Área:** [[Meli]] · **Estado:** active · **Prioridad:** P1 · **Aplicación:** [[java-polycard-sdk]]
> **Baseline:** master @ 6825a012e3, versión 8.202.0 · **Branch:** `feature/price-highlight-tier` · **Spec:** [VMDEM-22](https://spellbook.adminml.com/projects/VMDEM/specs/VMDEM-22)

## 🎯 Objetivo

Extender PriceDecorator mediante una API opt-in para renderizar PRECIO BAJO y
PRECIO MUY BAJO desde PRICE_HIGHLIGHT_TIER, manteniendo la prioridad sobre
BAJÓ DE PRECIO y preservando el precio anterior tachado cuando corresponda.

La validación de la iniciativa se limita a Price V1 con `discount_polylabel`.
Price V2 no se modifica ni valida en esta iteración.

La solución debe seguir usando PRICE. No se crea un componente top-level
nuevo ni se reutiliza PILL_PRICE_MARKDOWN.

## 📊 Estado actual

- PriceDecoratorBuilder.withPriceDropLabel recibe solo un predicate.
- PriceDecorator.buildPriceMarkdownDiscountLabel fija texto, icono y color
  para la señal BAJÓ DE PRECIO.
- El label actual se construye únicamente cuando existe previous price válido.
- BasicLabel y Style ya soportan fondo, color, padding y border radius.
- PolycardItem.attributes permite leer el atributo genérico mediante AttributeUtils.
- El SDK administra sus propias traducciones y publica el JAR i18n.

## 🧭 Alcance

### Incluye

- API pública opt-in en PriceDecoratorBuilder.
- Resolver seguro para VERY_LOW, LOW y NONE.
- Presentación Price V1 mediante `discount_polylabel`.
- Tier visible con o sin previous price.
- Tier + previous price tachado.
- Prioridad VERY_LOW > LOW > PRICE_DROPPED.
- i18n, pt-BR, DDT y compatibilidad hacia atrás.

### Fuera de alcance

- Evaluar showHighlight o el experimento Fury.
- Calcular tiers o exclusiones.
- Cambiar globalmente withPriceDropLabel.
- Cambiar Real Estate u otros consumidores que no opten a la API.
- Incorporar task-path de Search Middleware.
- Modificar o validar Price V2.

## 🏗️ Diseño propuesto

### API opt-in

Agregar una API equivalente a:

~~~java
withPriceHighlightTier(DecoratorPredicate predicate)
~~~

El predicate habilita la capacidad por consumidor/item. El SDK obtiene el
valor desde PRICE_HIGHLIGHT_TIER; Search no entrega texto ni estilos.

### Resolución segura

Crear un resolver/tipo interno con estas reglas:

~~~text
VERY_LOW -> VERY_LOW
LOW      -> LOW
NORMAL   -> NONE
null, blank, malformed, future -> NONE
~~~

No usar Enum.valueOf directo sobre el atributo. Un valor futuro no debe romper
la decoración ni bloquear el fallback a Bajó de Precio.

### Price V1

Refactorizar la decoración normal para separar:

1. selección de señal visible;
2. construcción del previous price tachado.

El tier se puede mostrar sin previous price. Cuando ambos existen, se emite el
label del tier y se conserva previous_price. hasPriceDropDiscountLabel debe
evolucionar a un concepto que represente cualquier señal que ocupe el slot
antes de ejecutar DiscountsDecorator.

### Estilos

| Tier | Texto | Fondo | Icono |
|---|---|---|---|
| VERY_LOW | #FFFFFF | #00A650 | ninguno |
| LOW | #00A650 | #E6F7EF | ninguno |

Padding y border radius se implementan con Style; los tokens finales son un
gate de UX antes de la release estable.

## ✅ Tareas

> [!example]- Fuente de tareas — planificador único
> - [x] G1 — Crear branch desde master y registrar baseline/version actual #owner/agent #type/dev #area/meli #app/java-polycard-sdk
> - [ ] G2 — Resolver OQ de promociones, tokens visuales y traducción pt-BR antes de fijar contrato final #owner/agent #type/research #area/meli #app/java-polycard-sdk #blocked
> - [x] G3 — Diseñar la API opt-in withPriceHighlightTier y validar compatibilidad binaria/fuente #owner/agent #type/dev #area/meli #app/java-polycard-sdk
> - [x] G4 — Implementar resolver allowlist de PRICE_HIGHLIGHT_TIER con VERY_LOW, LOW y NONE #owner/agent #type/dev #area/meli #app/java-polycard-sdk
> - [x] G5 — Implementar builders de label y estilos para LOW y VERY_LOW sin icono #owner/agent #type/dev #area/meli #app/java-polycard-sdk
> - [x] G6 — Refactorizar PriceDecorator para separar señal visible y previous price, conservando prioridad/fallback #owner/agent #type/dev #area/meli #app/java-polycard-sdk
> - [ ] G7 — Fuera de alcance: no modificar ni validar PriceV2Decorator en esta iteración #owner/agent #type/dev #area/meli #app/java-polycard-sdk
> - [ ] G8 — Agregar keys i18n, traducción pt-BR, regenerar keys.pot e i18ngettext-polycard.jar #owner/agent #type/dev #area/meli #app/java-polycard-sdk
> - [x] G9 — Agregar tests unitarios V1 para matriz completa, estilos, futuros y fallback #owner/agent #type/dev #area/meli #app/java-polycard-sdk
> - [ ] G10 — Agregar o ajustar DDT MLA/MLM para web, Android e iOS #owner/agent #type/dev #area/meli #app/java-polycard-sdk
> - [ ] G11 — Ejecutar quality gates del repo y verificar no regresión de RE, promociones, Consumer Credits y Meli+ #owner/agent #type/dev #area/meli #app/java-polycard-sdk
> - [ ] G12 — Publicar test version y entregar coordenadas a [[Destaque de Precio Search — Search Middleware]] #owner/agent #type/admin #area/meli #app/java-polycard-sdk
> - [ ] G13 — Incorporar feedback de integración, publicar versión estable y actualizar changelog #owner/agent #type/admin #area/meli #app/java-polycard-sdk #waiting

## 🧪 Matriz mínima de tests

| Tier | Previous price | Highlight enabled | Price drop enabled | Resultado |
|---|---:|---:|---:|---|
| VERY_LOW | no | sí | no | pill very low |
| LOW | no | sí | no | pill low |
| VERY_LOW | sí | sí | sí | pill very low + tachado |
| LOW | sí | sí | sí | pill low + tachado |
| NORMAL | sí | sí | sí | Bajó de Precio + tachado |
| futuro o malformado | sí | sí | sí | fallback Bajó de Precio |
| cualquiera | sí | no | sí | Bajó de Precio + tachado |
| cualquiera | sí | no | no | sin señal ni tachado |

La matriz se ejecuta sólo en Price V1. Agregar no regresión de promociones una
vez resuelta su precedencia funcional.

## 🚦 Gates de entrega

- API opt-in: consumidores existentes no cambian sin invocarla.
- Price V1 emite `discount_polylabel` con el significado y estilo acordados.
- LOW y VERY_LOW funcionan sin previous price.
- Tier + price drop conserva previous price tachado.
- Valores desconocidos fallan de forma segura.
- Traducciones y JAR incluidos en el mismo PR.
- Test version validada por Search Middleware antes de publicar estable.

## ❓ Decisiones bloqueantes

- ¿LOW y VERY_LOW reemplazan un % OFF o promotional label cuando coexisten?
- Confirmar padding, border radius y tokens exactos contra Figma.
- Confirmar wording pt-BR requerido por el pipeline del SDK.

No asumir estas respuestas dentro del código; resolverlas antes de G6 y G7.

## ⚠️ Riesgos y mitigaciones

| Riesgo | Mitigación |
|---|---|
| El refactor afecta RE o promociones | API opt-in + suites de no regresión |
| Valor futuro rompe el enum | parser allowlist con NONE |
| El tier elimina el tachado | decisiones independientes y matriz V1 |
| Release sin traducciones | gate conjunto de keys, pt-BR y JAR |

## 📆 Bitácora

- **2026-08-04** — Proyecto creado desde el scan de master. Se confirma que PriceDecorator no puede expresar tier/estilo y que PriceV2Decorator requiere soporte explícito.
- **2026-08-04** — Implementación de `PRICE_HIGHLIGHT_TIER` completada en `feature/price-highlight-tier`, sincronizada sobre `master @ 6825a012e3`. V1/V2, allowlist, prioridad/fallback, pt-BR y tests del decorador quedaron listos; `:decorator:test` pasó con 4177 tests. G8, DDT, quality gates completos, publicación y feedback de integración quedan pendientes.
- **2026-08-07** — Se agregó DDT MLA para Price V1 Android con el payload completo `LOW`/`VERY_LOW`/`NORMAL`, precio previo y fallback de precio bajado. JSON, mock y alias se validaron estáticamente. Price V2 quedó fuera de esta validación. La ejecución de DDT Studio/Gradle sigue pendiente: el wrapper 7.6 no puede cargar el plugin i18n compilado con Java 21.

## 🧭 Decisiones

- Reutilizar PRICE y extender PriceDecorator.
- Search habilita; el SDK interpreta atributo, prioridad, i18n y estilo.
- Mantener withPriceDropLabel sin cambios para compatibilidad.
- Validar exclusivamente Price V1 con `discount_polylabel`; Price V2 no se modifica ni valida.
- Publicar test version antes de la release estable.

## 🔗 Docs / Links

- [Spec técnica VMDEM-22](https://spellbook.adminml.com/projects/VMDEM/specs/VMDEM-22)
- [Spec funcional VMDEM-21](https://spellbook.adminml.com/projects/VMDEM/specs/VMDEM-21)
- [[Cierre VIS]]
- [[java-polycard-sdk]]
- [[Destaque de Precio Search — Search API Go]]
- [[Destaque de Precio Search — Search Middleware]]
