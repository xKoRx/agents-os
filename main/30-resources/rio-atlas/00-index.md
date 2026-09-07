---
type: index
schema_version: 1
status: active
icon: 🗺️
slug: "rio-atlas-index"
area: "[[Meli]]"
project: "[[Onboarding Signals]]"
created: 2026-08-10
updated: 2026-08-19
reviewed: 2026-08-12
aliases:
  - RIO Atlas
  - rio atlas
  - atlas RIO
cssclasses:
  - wide
tags:
  - kind/index
---

# 🗺️ RIO Atlas — Índice

> [!info] Wiki compilada de recursos
> El **RIO Atlas** documenta [[RIO]] **como sistema** (cómo una intención cruza apps, genera eventos, toca infra y vuelve como estado/resultado), a diferencia de las fichas verticales por app en [[30-resources/applications/00-index|applications]] (~13 apps: backend RIO + frontends + catálogo). Generado en parte por la herramienta [[rio-inspector]]. Proyectos: [[Onboarding Signals]] y [[Estandarización de Scopes RIO]].

## 📊 De un vistazo

- **Páginas:** 7 vistas activas ([[system-map]], [[integration-map]], [[deploy-component]], [[signals-context-flow]], [[deploy-request-path]], [[playmaker-deployment-idempotency-and-cp-kvs]], [[scope-inventory]]) + herramienta [[rio-inspector]]
- **Última ingesta:** 2026-08-12 ([[scope-inventory]]: Inventario 3 parcial con 21 `used`, 62 `no-evidence`, 1 `retirement-candidate` y 3 `inactive`, cruzando Fury, BigQueue y ownership técnico)
- **Estado:** active

## 📂 Catálogo

| Página | Una línea | Meta |
|---|---|---|
| [[system-map]] | Vista de 30 s: quién recibe/orquesta/ejecuta/habla con infra; sync vs async; dónde viven los contratos. | resource |
| [[integration-map]] | Grafo real producer→consumer→transport→channel, generado por rio-inspector (19 integraciones). | resource |
| [[deploy-component]] | Journey del contrato de I/O de un componente (front→playmaker→BigQueue→CP), as-is + dolor. | resource |
| [[signals-context-flow]] | Baseline params→outputs (kafka/clickhouse/flink/fury), fork pipeline/legacy y límites del registry; matriz field-level exhaustiva aún en research. | resource · revalidated 2026-08-19 |
| [[deploy-request-path]] | Diagrama end-to-end del camino de un request de deploy (front→playmaker→BigQueue→CP→result) + fork de ruteo a materializer; corrige el transporte del trigger. | resource |
| [[playmaker-deployment-idempotency-and-cp-kvs]] | Delimita la idempotencia de CPs y documenta dos tracks para Playmaker: hotfix KVS en `BatchCompletedEventListener` sin DB/estados/CPs y refactor durable con tópico externo y atomicidad. | resource · high confidence · 2026-08-25 |
| [[scope-inventory]] | Inventario live de 87 scopes backend RIO: estado Fury, consumidores BigQueue, clasificación de uso, owner técnico, perfil efectivo y riesgos de naming/configuración. | resource · verified 2026-08-12 |
| [[rio-inspector]] | Herramienta que genera el Integration Map desde código/config de los repos RIO. | tool |

### ⬜ Vistas pendientes (backlog Atlas — ver [[Onboarding Signals]])

- architecture/contracts — Contract Map de [[rio-sdk-events]] (eventos, campos, lifecycle, compat).
- architecture/lifecycle — estados de un componente (desired vs actual, reconciliación, idempotencia).
- architecture/failure-map — fallas, retry, DLQ, timeouts, dónde miro.
- architecture/runtime-map — observabilidad: logs/metrics/traces/dashboards/alerts por app.
- glossary — RIO, Signals, ADS, Control Plane, Materializer, BigQueue, CPS, Fury…; `scope` ya tiene baseline operativo en [[scope-inventory]], falta definición conceptual final.
- how-rio-works — narrativa 5-10 pág → candidato a contexto L1 de agentes.

## 🚨 Salud (del último lint)

- Huérfanos: ninguno (todas enlazadas desde [[RIO]] y este índice).
- Contradicciones: transporte del trigger reconciliado en [[deploy-request-path]]; [[scope-inventory]] abre contradicciones de ambiente/perfil, configuraciones sin scope live y un consumidor productivo pausado que requieren validación operacional.
- Conceptos sin página: `control-plane`, `data-product`, `CPS` — candidatos a glossary.

## 🔗 Links

- Plataforma [[RIO]] · Apps [[30-resources/applications/00-index|applications]] · Metodología [[data-mesh]]
- Herramienta [[rio-inspector]] · Proyectos [[Onboarding Signals]] y [[Estandarización de Scopes RIO]]
- [[30-resources/00-RESOURCE-WIKI|Reglas de la Resource Wiki]]

> [!quote] Norte del onboarding
> "Si mañana me dicen que un deployment en RIO quedó pegado, ¿puedo explicar qué componentes participaron, qué eventos debieron circular, qué estados debieron cambiar y dónde miro para descubrir dónde falló?" — cuando la respuesta sea **sí**, dejé de conocer 10 repos y empecé a **entender RIO**.
