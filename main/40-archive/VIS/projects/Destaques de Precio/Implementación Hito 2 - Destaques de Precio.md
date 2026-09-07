---
type: project
owner: me
root: false
status: active
priority: P1
area: "[[Meli]]"
parent: "[[Bajo y Muy Bajo Precio]]"
sprint: "[[A26Q2S7]]"
start: 2026-07-03
due:
progress: 5
repo: vis-items-loader-tagging, search-api-go, search-middleware, java-polycard-sdk, vis-octopus-lib, vpp-backend
jira:
prs:
aliases:
  - Implementacion Hito 2 Destaques de Precio
  - Implementación Destaques de Precio Motors
  - Implementación Bajo y Muy Bajo Precio
tags:
  - project
  - area/meli
  - feature/destaques-de-precio
created: "2026-07-03"
updated: "2026-07-27"
---

# Implementación Hito 2 - Destaques de Precio

%% Naming: Implementación Hito 2 - Destaques de Precio es el proyecto humano de implementación. Los proyectos de agente por app viven en agentes/ y se siguen con tareas puente acá. %%

> [!info]+ Implementación Hito 2 - Destaques de Precio
> **Área:** [[Meli]] · **Estado:** active · **Prioridad:** P1 · **Sprint:** [[A26Q2S7]]
> **Parent:** [[Bajo y Muy Bajo Precio]]

## 🎯 Objetivo

- Implementar Hito 2 de Destaques de Precio en Motors usando como fuente canónica el RFC `RFC Destaque de precio — Hito 2.md`.
- Escalar la infraestructura de [[Bajó de Precio]] mediante un processor estándar nuevo que reutiliza `ProcessorFilter`, `/consume-process-item` y `Orchestrator`, persiste los tres atributos y recibe también el proceso masivo paginado.
- Mantener subproyectos por aplicación para que cada implementación pueda avanzar con contexto y tareas propias.

## 📊 Estado actual

- RFC específico de Hito 2 corregido el 2026-07-03.
- Specs técnicas locales corregidas/creadas el 2026-07-03:
  - `Destaques de Precio — vis-items-loader-tagging — Spec Técnica Propuesta.md`
  - `Destaques de Precio — Polycard Search — Spec Técnica Propuesta.md`
  - `Destaques de Precio — VIP — Spec Técnica Propuesta.md`
- Pendientes humanos bloqueantes:
  - creación/caché/filtrabilidad del atributo
    `VEHICLE_PRICE_HIGHLIGHT_TIER` en Items/Search;
  - reglas exactas del Sugeridor para `LOW` / `VERY_LOW` / limpieza;
  - cache Search API Go y filtrabilidad en Search;
  - contrato versionado de BigQuery y trigger del proceso masivo;
  - fuente FIPE/rango/lista de exclusión para MLB;
  - experimento, rollout y observabilidad.
- Plan producer corregido el 2026-07-25 y dividido en tres partes:
  1. escalar Bajó de Precio para sumar Destaque de Precio;
  2. handler masivo que obtiene una sola lista completa de `item_id` desde
     BigQuery y publica páginas autocontenidas;
  3. consumer de cambios en atributos baneadores que solicita reevaluar ambas
     señales.
- El proceso masivo no se modela como Backfill. Sus consumers de página reciben
  IDs explícitos y no vuelven a consultar BigQuery.
- La arquitectura no introduce signals ni capabilities nuevas. El processor
  `vehicle_price_highlight_motors` ejecuta las reglas de ambas iniciativas y
  delega responsabilidades internas en services/helpers.
- Rollout acordado en dos despliegues: primero conviven el processor nuevo y
  `price_before_discount_motors` deprecado para drenar mensajes; después se
  elimina solo la instancia/configuración Motors antigua. El processor
  genérico `price_before_discount` de Real Estate permanece.

## 🧩 Subproyectos por aplicación

| Aplicación | Proyecto de agente | Foco |
|---|---|---|
| vis-items-loader-tagging | [[Hito 2 - vis-items-loader-tagging]] | Productor, consumer común, consumer atributos, proceso masivo |
| Search API Go | [[Hito 2 - Search API Go]] | Cache de atributos, filtrabilidad y contrato hacia Search |
| search-middleware | [[Hito 2 - search-middleware]] | Consumo de señal, jerarquía vs Bajó de Precio, tracking |
| java-polycard-sdk | [[Hito 2 - java-polycard-sdk]] | Validar/implementar soporte visual si el highlight genérico no alcanza |
| vis-octopus-lib | [[Hito 2 - vis-octopus-lib]] | Lectura de señal persistida para VIP |
| vpp-backend | [[Hito 2 - vpp-backend]] | Tag VIP, supresión de Bajó de Precio, layout/tracking |

## ✅ Tareas

> [!note]+ Ownership y tarea puente
> `#owner/me` = tuya · `#owner/agent` = de un agente · `#type/supervision` = tarea puente humana para seguir un proyecto de agente.

> [!example]- Fuente de tareas — editar / mover de estado aquí
> - [x] Definir contrato producer: `PREVIOUS_PRICE`, `HAS_LOWER_PRICE` y `VEHICLE_PRICE_HIGHLIGHT_TIER` (`LOW`/`VERY_LOW`/limpiar) #owner/me #type/research #area/meli #sprint/A26Q2S7
> - [ ] Alinear creación de atributos con Items/Catálogo #owner/me #type/research #area/meli #sprint/A26Q2S7 #blocked
> - [ ] Alinear con Search cache Search API Go + filtrabilidad #owner/me #type/research #area/meli #sprint/A26Q2S7 #blocked
> - [ ] Confirmar query BigQuery, límite de memoria/timeout y tamaño máximo de mensaje del proceso masivo #owner/me #type/research #area/meli #sprint/A26Q2S7 #blocked
> - [ ] Definir trigger de proceso masivo para No MLB y MLB #owner/me #type/research #area/meli #sprint/A26Q2S7 #blocked
> - [ ] Confirmar fuente FIPE, rango y lista marca/modelo/año de exclusión para MLB #owner/me #type/research #area/meli #sprint/A26Q2S7 #blocked
> - [ ] Definir experimentos, rollout y observabilidad #owner/me #type/research #area/meli #sprint/A26Q2S7 #blocked
> - [ ] Revisar y aprobar specs técnicas locales antes de llevarlas a Spellbook #owner/me #type/research #area/meli #sprint/A26Q2S7
> - [/] [[Hito 2 - vis-items-loader-tagging]] arrancar + seguimiento #owner/me #type/supervision #area/meli #app/vis-items-loader-tagging #sprint/A26Q2S7
> - [ ] [[Hito 2 - Search API Go]] arrancar + seguimiento #owner/me #type/supervision #area/meli #app/search-api-go #sprint/A26Q2S7
> - [ ] [[Hito 2 - search-middleware]] arrancar + seguimiento #owner/me #type/supervision #area/meli #app/search-middleware #sprint/A26Q2S7
> - [ ] [[Hito 2 - java-polycard-sdk]] arrancar + seguimiento #owner/me #type/supervision #area/meli #app/java-polycard-sdk #sprint/A26Q2S7
> - [ ] [[Hito 2 - vis-octopus-lib]] arrancar + seguimiento #owner/me #type/supervision #area/meli #app/vis-octopus-lib #sprint/A26Q2S7
> - [ ] [[Hito 2 - vpp-backend]] arrancar + seguimiento #owner/me #type/supervision #area/meli #app/vpp-backend #sprint/A26Q2S7

## 📆 Bitácora

- **2026-07-03** — Proyecto humano de implementación creado para organizar Hito 2 por aplicación. Se crean proyectos de agente por app y tareas puente según reglas AGENTS OS.
- **2026-07-25** — Se cierra el contrato producer del tercer atributo
  `VEHICLE_PRICE_HIGHLIGHT_TIER` con valores `LOW`/`VERY_LOW`/limpieza y se
  inicia la revisión del plan phase-gated de [[Hito 2 - vis-items-loader-tagging]].
- **2026-07-25** — Se corrige el diseño masivo: una sola lectura completa de
  IDs desde BigQuery, `total_items` calculado sobre esa lista, páginas con IDs
  explícitos y fan-out unitario sin nuevas consultas. El plan queda organizado
  en tres paquetes autónomos.
- **2026-07-27** — Se elimina del diseño la abstracción `signals`: se reutiliza
  el contrato actual de processors y se define una migración en dos
  despliegues para drenar y retirar `price_before_discount_motors`.

## 🧭 Decisiones

- El proyecto padre de implementación es humano (`owner: me`); cada aplicación tiene proyecto de agente (`owner: agent`) con tarea puente.
- Hito 2 escala Hito 1: no duplicar pipeline si el consumer/procesamiento de Bajó de Precio puede evolucionar.
- Se persisten ambas señales verdaderas; la prioridad visual entre Hito 2 e
  Hito 1 se resuelve en Search/VIP.
- El processor nuevo evalúa siempre las reglas de Bajó de Precio y Destaque de
  Precio; los productores solo usan `process:vehicle_price_highlight_motors`.

## 🔗 Docs / Links

- RFC Hito 2: `file:///Users/rjara/fuentes/second-brain/sb-main/01_Projects/previous-price-motors/RFC%20Destaque%20de%20precio%20%E2%80%94%20Hito%202.md`
- Spec técnica producer: `file:///Users/rjara/fuentes/second-brain/sb-main/01_Projects/previous-price-motors/Destaques%20de%20Precio%20%E2%80%94%20vis-items-loader-tagging%20%E2%80%94%20Spec%20T%C3%A9cnica%20Propuesta.md`
- Spec técnica Search: `file:///Users/rjara/fuentes/second-brain/sb-main/01_Projects/previous-price-motors/Destaques%20de%20Precio%20%E2%80%94%20Polycard%20Search%20%E2%80%94%20Spec%20T%C3%A9cnica%20Propuesta.md`
- Spec técnica VIP: `file:///Users/rjara/fuentes/second-brain/sb-main/01_Projects/previous-price-motors/Destaques%20de%20Precio%20%E2%80%94%20VIP%20%E2%80%94%20Spec%20T%C3%A9cnica%20Propuesta.md`
- Proyecto padre: [[Bajo y Muy Bajo Precio]]
