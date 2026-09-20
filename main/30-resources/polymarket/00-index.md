---
type: index
schema_version: 1
status: active
icon: 🗂️
slug: polymarket-resources-index
area: "[[Personal]]"
project: "[[Polymarket Engine — MVP]]"
created: 2026-09-16
updated: 2026-09-17
reviewed: 2026-09-17
aliases:
  - Polymarket resources index
cssclasses:
  - wide
tags:
  - kind/index
  - tech/polymarket
---

# Polymarket — Índice de recursos

> [!info] Wiki compilada de recursos
> Entrada curada para conocimiento técnico y research de Polymarket. Las hipótesis son candidatas por falsar, no alpha verificado. Reglas: [[30-resources/00-RESOURCE-WIKI|Resource Wiki]]. Bitácora: `log.md`.

## 📊 De un vistazo

- **Proyecto consumidor:** [[Polymarket Engine — MVP]].
- **Recurso técnico M0 canónico:** [[Polymarket — Technical Platform Map — synced 2026-09-17]].
- **Original íntegro preservado:** Biblioteca `/Polymarket Engine/Resources/Polymarket — Technical Platform Map — synced 2026-09-17.md`, 160165 bytes, 1177 líneas, SHA-256 `78e6506fa67aa12843ba4acb0e4c8271a83c1841432a4a53777c73c4c723c11f`.
- **Estado M0:** `DESIGN_READY` documental 2026-09-17; siete RG resueltos para diseño con live/optional gates deshabilitados. Revisión conjunta antes de ASTRA-1; §24 de part-10 es autoridad del estado.
- **Research de oportunidades:** [[Polymarket — Edge Research Consolidado 2026-09-16]].
- **Live:** ninguna nota de research autoriza ejecución; NegRisk Protocol-v2 conversion permanece bloqueada hasta route/ABI verificadas.

## 📂 Catálogo

| Página | Una línea | Meta |
|---|---|---|
| [[Polymarket — Technical Platform Map — synced 2026-09-17]] | Knowledge pack técnico para diseño del Engine: APIs, WS, auth, orders, positions, contracts, fees, resolution, history y gaps; el agente de M0 debe trabajar directamente sobre este archivo. | `status: M0 DESIGN_READY (no live certification)` |
| [[Polymarket — Edge Research Consolidado 2026-09-16]] | Síntesis deduplicada: 58 formulaciones nominales → 30 hipótesis/familias, datos, tests, evidencia contraria, contradicciones y secuencia de falsación. | `confidence: medium` |
| [[Polymarket Engine — Five-POC Guía Operativa 2026-09-20]] | Guía operativa de las cinco POCs (S01–S05): HOW TO RUN, input, mode, output, artifacts, research surface y limitaciones; baseline `feature/five-poc-integration@037c15d`, M4 recert no-live. | `status: RESEARCH_READY (hypothesis_validated=NO)`
| [[Polymarket DR R1 — Mecanismos y evidencia]] | Origen R1: diez mecanismos y experimentos con NO_GO; riesgo de crypto lead-lag. | `type: source`, SHA-256 |
| [[Polymarket DR R2 — Microestructura y oráculo]] | Origen R2: cuatro configuraciones concretas; estimaciones de rentabilidad por verificar. | `type: source`, SHA-256 |
| [[Polymarket DR R3 — Anomalías estadísticas y 24 hipótesis]] | Origen R3: 24 tests y controles econométricos, incentivos y fallas de medición. | `type: source`, SHA-256 |
| [[Polymarket DR R4 — Taxonomía y 20 hipótesis]] | Origen R4: 20 propuestas y taxonomía; contiene claims divergentes. | `type: source`, SHA-256 |

## 🚨 Salud

- **Technical Map:** once partes indexadas desde la nota canónica; M0 DESIGN_READY para arquitectura; contratos dinámicos sujetos a versionado y live sujeto a certificación posterior. La versión `Intake` no es autoridad.
- **Contradicciones de edge research:** fees/rebates históricos, FLB Sports, oracle bond/settlement, estadísticas de wallets, claims de arb sin riesgo.
- **Regla técnica:** parámetros operacionales se versionan/consultan desde autoridad vigente; no convertir snapshots históricos en constantes del engine.
- **Gate inmediato:** revisión conjunta del M0 DESIGN_READY y paso a diseño Astra/Fable. Nunca interpretar M0 como habilitación live ni como certificación de contratos fuera de scope.

## 🔗 Links

- [[Polymarket Engine — MVP]] — autoridad operativa del producto.
- [[Polymarket Engine — Opportunity Context]] — contexto económico y de estrategias.
- [[Polymarket — Technical Platform Map — synced 2026-09-17]] — knowledge pack técnico M0.
- [[Polymarket — Edge Research Consolidado 2026-09-16]] — hipótesis/edge research.
- [[30-resources/00-RESOURCE-WIKI|Reglas de la Resource Wiki]].
- `log.md` — bitácora del dominio.
