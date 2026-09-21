---
type: index
schema_version: 1
status: active
icon: 🗂️
slug: polymarket-resources-index
area: "[[Personal]]"
project: "[[Polymarket Engine — MVP]]"
created: 2026-09-16
updated: 2026-09-21
reviewed: 2026-09-21
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
- **Punto de retoma para nuevos agentes:** [[Polymarket Engine — Continuidad Five-POC 2026-09-20]]; leer junto al padre y la guía operativa antes de abrir código. Resume decisiones, SHAs, receipts, tareas con owner y bloqueos. Addendum 2026-09-21: PE-001 reality check `GO_RESEARCH` (§9), hardening `ENGINEERING_STAGE_CLOSED_RESEARCH_REPRODUCIBLE` (§10), dictamen U-02 **`V2_CASH_CONFIRMED`** (§11), S02 E2 **`NO_SIGNALS_IN_SAMPLE`** (§12) y consolidación **`MASTER_CANONICAL`** (§13, `master@a770da6`).
- **Último cierre técnico (2026-09-21):** `MASTER_CANONICAL`. Engine publicado: default `master` = `origin/main` = `a770da6`. Código Five-POC `56e8fac` / integración `85e27ff` absorbidos. M4 recertificado no-live **en `85e27ff`** (27/0/0/5), recibo `testdata/research-master/`. `LIVE_DISABLED`. `d5ce263` no mergeado. Detalle en continuidad §13, padre y [[2026-09-21-polymarket-master-consolidation]].
- **Estado de investigación:** 5/5 POCs listas para experiments offline sintéticos. `HYPOTHESIS_VALIDATED=NO`, `LIVE_DISABLED`. U-02 **`V2_CASH_CONFIRMED`** (BUY fee en pUSD, shares completas; `TAKER_PROCEEDS` = V1 archivado, no mergear). Redondeo 5 dp vs `TRUNCATE_6DP` y fee operador siguen abiertos. `REAL_FEE_READY=NO`. S02 E2 2026-09-21: **`NO_SIGNALS_IN_SAMPLE`** (4 MLB moneylines, 1800 s; no NO_GO global). PE-001 discovery 2026-09-21: 7 pares / 0 semántico∩temporal / 0 lock q=20. Weather inventariado (KLGA/RJTT) sin vintages. Catalog `first_known_at` ≠ `createdAt` demostrado; cohorte O/B real ausente. PE-004 W bloqueada por SFG-06. Factory fee `SYNTHETIC_FIXTURE`.
- **Recurso técnico M0 canónico:** [[Polymarket — Technical Platform Map — synced 2026-09-17]].
- **Original íntegro preservado:** Biblioteca `/Polymarket Engine/Resources/Polymarket — Technical Platform Map — synced 2026-09-17.md`, 160165 bytes, 1177 líneas, SHA-256 `78e6506fa67aa12843ba4acb0e4c8271a83c1841432a4a53777c73c4c723c11f`.
- **Estado M0 histórico:** `DESIGN_READY` documental 2026-09-17; siete RG resueltos para diseño con live/optional gates deshabilitados. §24 de part-10 es autoridad del estado de ese milestone; no es la baseline de implementación actual.
- **Research de oportunidades:** [[Polymarket — Edge Research Consolidado 2026-09-16]].
- **Live:** ninguna nota de research autoriza ejecución; NegRisk Protocol-v2 conversion permanece bloqueada hasta route/ABI verificadas.

## 📂 Catálogo

| Página | Una línea | Meta |
|---|---|---|
| [[Polymarket Engine — Continuidad Five-POC 2026-09-20]] | Handoff canónico de retoma: `MASTER_CANONICAL` §13, Five-POC absorbido en `master@a770da6`, U-02 `V2_CASH_CONFIRMED`, Sports E2. | `status: MASTER_CANONICAL published; LIVE_DISABLED` |
| [[Polymarket Engine — Five-POC Guía Operativa 2026-09-20]] | Ejecución de S01–S05 sobre worktree `polymarket-engine-master`. Código `85e27ff`; M4 recert `research-master` pineado a ese SHA. `hypothesis_validated=NO`. | `status: MASTER_CANONICAL offline; hypothesis_validated=NO` |
| [[Polymarket — Technical Platform Map — synced 2026-09-17]] | Knowledge pack técnico para diseño del Engine: APIs, WS, auth, orders, positions, contracts, fees, resolution, history y gaps; el agente de M0 debe trabajar directamente sobre este archivo. | `status: M0 DESIGN_READY (no live certification)` |
| [[Polymarket — Edge Research Consolidado 2026-09-16]] | Síntesis deduplicada: 58 formulaciones nominales → 30 hipótesis/familias, datos, tests, evidencia contraria, contradicciones y secuencia de falsación. | `confidence: medium` |
| [[Polymarket DR R1 — Mecanismos y evidencia]] | Origen R1: diez mecanismos y experimentos con NO_GO; riesgo de crypto lead-lag. | `type: source`, SHA-256 |
| [[Polymarket DR R2 — Microestructura y oráculo]] | Origen R2: cuatro configuraciones concretas; estimaciones de rentabilidad por verificar. | `type: source`, SHA-256 |
| [[Polymarket DR R3 — Anomalías estadísticas y 24 hipótesis]] | Origen R3: 24 tests y controles econométricos, incentivos y fallas de medición. | `type: source`, SHA-256 |
| [[Polymarket DR R4 — Taxonomía y 20 hipótesis]] | Origen R4: 20 propuestas y taxonomía; contiene claims divergentes. | `type: source`, SHA-256 |

## 🚨 Salud

- **Código vs vault vs remoto:** engine `origin/master` = `origin/main` = `a770da6` (publicado 2026-09-21). Recibo M4 vigente: `testdata/research-master/certificate.json` pineado a `85e27ff`. v07 @ `c38f6c4` es histórico.
- **Technical Map:** once partes indexadas desde la nota canónica; M0 DESIGN_READY para arquitectura; contratos dinámicos sujetos a versionado y live sujeto a certificación posterior. La versión `Intake` no es autoridad.
- **Contradicciones de edge research:** fees/rebates históricos, FLB Sports, oracle bond/settlement, estadísticas de wallets, claims de arb sin riesgo.
- **Regla técnica:** parámetros operacionales se versionan/consultan desde autoridad vigente; no convertir snapshots históricos en constantes del engine.
- **Próximo gate de research:** PE-001 par OT-emparejado o dictamen boilerplate; S04 vintages NWS; S02 siguiente ventana usable. **No mergear `d5ce263` como corrección de venue.** Ningún resultado sintético ni el hardening certifica alpha o live.

## 🔗 Links

- [[Polymarket Engine — MVP]] — autoridad operativa del producto.
- [[Polymarket Engine — Continuidad Five-POC 2026-09-20]] — punto de entrada de la siguiente sesión.
- [[Polymarket Engine — Five-POC Guía Operativa 2026-09-20]] — ejecución reproducible.
- [[Polymarket Engine — Opportunity Context]] — contexto económico y de estrategias.
- [[Polymarket — Technical Platform Map — synced 2026-09-17]] — knowledge pack técnico M0.
- [[Polymarket — Edge Research Consolidado 2026-09-16]] — hipótesis/edge research.
- [[30-resources/00-RESOURCE-WIKI|Reglas de la Resource Wiki]].
- `log.md` — bitácora del dominio.
