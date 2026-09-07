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
repo: search-middleware
jira: VMDEM-22
prs:
aliases:
  - Implementación PRICE_HIGHLIGHT_TIER Search Middleware
  - Destaque de Precio Search Middleware
tags:
  - kind/project
  - area/meli
  - app/search-middleware
  - feature/destaques-de-precio
created: 2026-08-04
updated: 2026-08-04
cssclasses:
  - wide
---

# Destaque de Precio Search — Search Middleware

%% Naming: plan de implementación del consumo de PRICE_HIGHLIGHT_TIER en el flujo legacy activo de Search. Proyecto de agente bajo [[Cierre VIS]]. %%

> [!info]+ Search Middleware — integración del destaque
> **Padre:** [[Cierre VIS]] · **Área:** [[Meli]] · **Estado:** active · **Prioridad:** P1 · **Aplicación:** [[search-middleware]]
> **Baseline:** feature/VMDEM-21-price-drop-all-platforms @ 08c8e5bb58a, sincronizada con develop · **Spec:** [VMDEM-22](https://spellbook.adminml.com/projects/VMDEM/specs/VMDEM-22)

## 🎯 Objetivo

Habilitar en el flujo legacy activo de Polycard la capacidad de Destaque de
Precio V1 publicada por Java Polycard SDK mediante `discount_polylabel`,
usando showHighlight de vis/item-dropprice-motors y manteniendo showPill
independiente para Bajó de Precio y el tachado.

Search no interpreta PRICE_HIGHLIGHT_TIER, no calcula tiers y no construye
estilos: limita la capacidad a Motors y configura los predicates del SDK.

## 📊 Estado actual

- La baseline ya extiende Bajó de Precio Motors a todas las plataformas.
- PriceDropExperimentModel solo expone showPill mediante el campo heredado show.
- PriceDropMotorsExperimentTask no lee showHighlight.
- El factory legacy ya configura withCrossedOutPrice y withPriceDropLabel.
- Search declara polycardVersion=8.200.1; falta integrar la nueva versión.
- Search API todavía filtra PRICE_HIGHLIGHT_TIER hasta que se entregue su
  proyecto dependiente.

## 🧭 Alcance

### Incluye

- Transportar showHighlight y mantener showPill compatible.
- Force param independiente para pruebas.
- Integrar test version y release estable del SDK.
- Configurar la API opt-in solo para Motors en el factory legacy.
- Mantener el tachado gobernado por showPill y la baja válida.
- Tests de experimento, prioridad, payload V1 y no regresión.
- Deploy apagado y rollout por site/plataforma.

### Fuera de alcance

- Interpretar el enum en Search.
- Crear un componente o DTO nuevo.
- Recalcular exclusiones del productor.
- Cambiar Real Estate o map layout.
- Implementar task-path de Polycard en este release.

## 🏗️ Diseño

### Experimento

Extender PriceDropExperimentModel:

~~~text
show           <- showPill (compatibilidad actual)
showHighlight  <- showHighlight (nuevo, default false)
~~~

PriceDropMotorsExperimentTask lee ambos valores. El fallback deja ambos en
false. Mantener price-drop-motors.force para showPill y agregar un force
independiente para highlight:

~~~text
price-highlight-motors.force
~~~

### Factory legacy

Configurar el builder así conceptualmente:

~~~java
.withCrossedOutPrice(this::shouldShowCrossedOutPrice)
.withPriceDropLabel(this::shouldShowPriceDropLabel)
.withPriceHighlightTier(this::shouldShowPriceHighlight)
~~~

shouldShowPriceHighlight solo valida:

- item Motors;
- experimento/modelo disponible;
- showHighlight=true.

El SDK resuelve el atributo y la prioridad. shouldShowCrossedOutPrice y
shouldShowPriceDropLabel conservan las reglas de showPill ya implementadas.

### Dependencia SDK

1. consumir test version;
2. validar payloads reales V1;
3. cambiar a release estable;
4. desplegar con showHighlight=false.

## ⚠️ Warning — task-path

El resolver de Polycard usa LEGACY por defecto. polycard_response=task es
opt-in y polycard_response=compare ejecuta ambos caminos pero responde legacy.
Por decisión de alcance, este proyecto no modifica:

- PolycardPriceCustomizationDataTask;
- app/polycard/overrides/common/PriceDecoratorFactory;
- PolycardPriceModel del sucesor.

Antes de activar task-path como fuente por defecto se debe portar
PriceDropMotorsExperimentTask, showPill, showHighlight y las APIs del SDK.

Costo incremental estimado después de este proyecto: 2 a 3 archivos
productivos, 2 a 3 suites y compare mode; **1 a 2 jornadas**. No requiere
cambios adicionales en Search API o SDK si el contrato opt-in queda estable.

## ✅ Tareas

> [!example]- Fuente de tareas — planificador único
> - [x] G1 — Confirmar baseline y crear branch de implementación desde la rama sincronizada indicada por el owner #owner/agent #type/dev #area/meli #app/search-middleware ✅ 2026-08-04
> - [x] G2 — Extender PriceDropExperimentModel con showHighlight=false y conservar show como showPill #owner/agent #type/dev #area/meli #app/search-middleware ✅ 2026-08-04
> - [x] G3 — Actualizar PriceDropMotorsExperimentTask para leer ambos params y agregar force independiente #owner/agent #type/dev #area/meli #app/search-middleware ✅ 2026-08-04
> - [x] G4 — Agregar tests del modelo y task para cuatro combinaciones, config ausente y fallback #owner/agent #type/dev #area/meli #app/search-middleware ✅ 2026-08-04
> - [x] G5 — Integrar test version de [[Destaque de Precio Search — Java Polycard SDK]] en build.gradle #owner/agent #type/dev #area/meli #app/search-middleware ✅ 2026-08-04
> - [x] G6 — Configurar withPriceHighlightTier en el factory legacy solo para Motors + showHighlight #owner/agent #type/dev #area/meli #app/search-middleware ✅ 2026-08-04
> - [x] G7 — Mantener separados el predicate de label y el de tachado; no alterar reglas RE o map #owner/agent #type/dev #area/meli #app/search-middleware ✅ 2026-08-04
> - [x] G8 — Agregar matriz de tests del factory para VERY_LOW, LOW, NORMAL, futuro, ausencia y coexistencia #owner/agent #type/dev #area/meli #app/search-middleware ✅ 2026-08-04
> - [x] G9 — Agregar tests de payload PRICE V1 en native/web y no regresión RE #owner/agent #type/dev #area/meli #app/search-middleware ✅ 2026-08-04
> - [ ] G10 — Validar item real desde [[Destaque de Precio Search — Search API Go]] con raw attribute presente #owner/agent #type/dev #area/meli #app/search-middleware #waiting
> - [x] G11 — Ejecutar tests focalizados, suite, checkstyle, PMD y quality gates proporcionales #owner/agent #type/dev #area/meli #app/search-middleware ✅ 2026-08-04
> - [ ] G12 — Reemplazar test version por release estable del SDK y repetir smoke tests #owner/agent #type/dev #area/meli #app/search-middleware #waiting
> - [ ] G13 — Preparar PR y deploy con showHighlight=false #owner/agent #type/pr-review #area/meli #app/search-middleware
> - [ ] G14 — Validar payloads MLA por plataforma, activar MLA y luego MLM con kill switch documentado #owner/agent #type/admin #area/meli #app/search-middleware #waiting
> - [ ] F1 — Crear seguimiento separado para paridad task-path antes del cambio de default #owner/agent #type/research #area/meli #app/search-middleware

## 🧪 Matriz mínima de tests

| Tier | showHighlight | Baja | showPill | Resultado |
|---|---:|---:|---:|---|
| VERY_LOW | ON | sí | ON | very low + tachado |
| LOW | ON | sí | ON | low + tachado |
| VERY_LOW o LOW | ON | no | cualquiera | tier sin tachado |
| VERY_LOW o LOW | OFF | sí | ON | Bajó de Precio + tachado |
| NORMAL, futuro o ausente | cualquiera | sí | ON | Bajó de Precio + tachado |
| cualquiera | OFF | sí | OFF | sin señal ni tachado |

Agregar variantes Motors, RE, no-Motors, native y web. El factory no debe
hacer asserts sobre colores internos: esos pertenecen al SDK; los tests de
payload sí verifican el contrato integrado.

## 🚦 Gates de entrega

- Search API expone el atributo en un item real.
- SDK test version validada en Price V1.
- showHighlight=false deja el output idéntico al baseline.
- showHighlight=true respeta prioridad y tachado.
- RE, map layout y no-Motors no cambian.
- Release estable integrada antes del deploy.
- Rollout inicia apagado y cuenta con showHighlight=false como kill switch.

## ⚠️ Riesgos y mitigaciones

| Riesgo | Mitigación |
|---|---|
| Acoplar showPill y showHighlight | campos, defaults y tests independientes |
| Search duplica parser o estilo del SDK | predicate booleano; SDK interpreta y renderiza |
| Integrar una test version en producción | gate explícito de reemplazo por estable |
| Regresión RE o map | API Motors-only + tests de no regresión |
| Migración task-path posterior pierde la feature | warning y follow-up obligatorio antes del switch |

## 📆 Bitácora

- **2026-08-04** — Proyecto creado desde el scan de la baseline. Se acota al flujo legacy activo y se registra task-path como deuda no bloqueante con costo estimado.
- **2026-08-04** — Implementación completada en `feature/price-highlight-tier` desde `feature/VMDEM-21-price-drop-all-platforms`: `showHighlight`, force param independiente, SDK `0.0.1-price-highlight-tier`, predicates Motors-only y payloads V1/V2 validados. `./gradlew test` y smoke focalizado pasan; Checkstyle/PMD globales quedan degradados por errores preexistentes de procesamiento en la baseline. Release estable, item real de Search API y rollout quedan pendientes.
- **2026-08-04** — Creada `feature/price-highlight-tier-test` desde `feature/price-highlight-tier`. En scopes cuyo nombre contiene `test`, la respuesta de Search API recibe `PRICE_HIGHLIGHT_TIER` secuencialmente `NORMAL → LOW → VERY_LOW`, incluyendo `value_id`, `value_name`, `values` y `value_type`, para validación visual en dispositivos sin depender de un JSON local.
- **2026-08-04** — Diagnóstico de validación visual: el mock y la SDK no son el bloqueo. La ruta task-path construye el decorador con `app/polycard/overrides/common/PriceDecoratorFactory`, que no invoca `withPriceHighlightTier(...)`; por eso el SDK no recibe la señal para renderizar la pill. Se requiere paridad en ese factory antes de continuar la prueba visual.
- **2026-08-04** — Paridad task-path aplicada en `feature/price-highlight-tier-test`: el factory invoca `withPriceHighlightTier(...)` y el predicate usa exclusivamente `priceDropMotorsExperiment.showHighlight`. `showPill` queda reservado para “Bajó de precio”. Smoke focalizado offline pasa.
- **2026-08-04** — El mock fue movido de `SearchApiMockService` a `SearchApiService`: en un scope de test modifica la respuesta real antes de Polycard; en producción no se ejecuta. La secuencia y el gate `showHighlight` están cubiertos por tests focalizados.
- **2026-08-04** — Validación de SDK y observabilidad para la prueba nativa: el JAR `0.0.1-price-highlight-tier` resuelve `PRICE_HIGHLIGHT_TIER` desde `value_name` y solo renderiza `LOW`/`VERY_LOW` (`NORMAL` omite la pill). En scope test, `vis/item-dropprice-motors` se fuerza con `showPill=true` y `showHighlight=true`; hay logs INFO para inyección de tier, override de experimento y decisión del predicate. Tests V1/V2 de la SDK pasan.
- **2026-08-07** — Alcance de integración acotado a Price V1 con `discount_polylabel`. Los factories aplican `withPriceHighlightTier(...)` sólo al builder V1; Price V2 conserva su flujo existente y no se valida para este destaque. Se retiraron las pruebas que decoraban el tier en V2.

## 🧭 Decisiones

- Search solo habilita por experimento y vertical; el SDK interpreta el tier.
- show conserva semántica de showPill; showHighlight es independiente.
- El tachado no depende de la señal visual ganadora.
- task-path no pertenece al release actual.
- El destaque se valida sólo en Price V1; Price V2 queda fuera de alcance.

## 🔗 Docs / Links

- [Spec técnica VMDEM-22](https://spellbook.adminml.com/projects/VMDEM/specs/VMDEM-22)
- [Spec funcional VMDEM-21](https://spellbook.adminml.com/projects/VMDEM/specs/VMDEM-21)
- [[Cierre VIS]]
- [[search-middleware]]
- [[Destaque de Precio Search — Search API Go]]
- [[Destaque de Precio Search — Java Polycard SDK]]
