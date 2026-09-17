---
type: project
schema_version: 1
owner: me
root: true
status: active
priority: P1
area: "[[Personal]]"
parent:
sprint:
start: 2026-09-15
due:
progress: 0
repo:
jira:
prs:
aliases:
  - Polymarket Engine MVP
  - Polymarket Arbitrage MVP
  - Prediction Market Engine
tags:
  - kind/project
  - area/personal
  - domain/trading
  - tech/polymarket
  - topic/prediction-markets
created: 2026-09-15
updated: 2026-09-16
---

# Polymarket Engine — MVP

> [!info]+ Polymarket Engine — MVP
> **Área:** [[Personal]] · **Estado:** active · **Prioridad:** P1 · **Engine:** MVP durable · **Strategies:** POCs · **Tiny-live inicial:** US$300 totales

## 🎯 Objetivo

Construir un **engine Polymarket-native, agnóstico de estrategia**, robusto y reusable, que permita investigar, medir, simular y eventualmente ejecutar múltiples estrategias sin rehacer market-data, replay, risk, execution ni observabilidad para cada hipótesis.

La distinción es estructural:

- **Polymarket Engine = MVP durable.** No es una POC ni código descartable.
- **Strategies = POCs.** Cada estrategia puede ser promovida, iterada o eliminada sin erosionar el engine.
- El engine es **agnóstico de estrategia, no agnóstico de venue**. Debe modelar bien Polymarket y evitar abstracciones prematuras para Kalshi/sportsbooks/otros venues.
- Echo y Echo Forge continúan en paralelo y quedan fuera del hot path y del alcance del MVP.

North star del producto de research:

`TIME_TO_VALIDATED_HYPOTHESIS`

Una vez establecido el engine, el coste marginal de probar una hipótesis nueva debe caer materialmente.

## 📊 Estado actual

- Greenfield; repo de implementación pendiente.
- Arquitectura frozen a nivel macro: **Go + modular monolith + single deployable + single large host**.
- Primero se construye el Engine MVP; Sports y NegRisk dejan de ser “el MVP” y pasan a ser **POC-S01** y **POC-S02**, primeros consumidores del engine.
- Backlog research: 30 familias canónicas `PE-001…PE-030` en [[Polymarket — Edge Research Consolidado 2026-09-16]].
- Contexto económico/estratégico: [[Polymarket Engine — Opportunity Context]].
- Siguiente gate: **Deep Research técnico exhaustivo de la documentación oficial de Polymarket**, materializado en `30-resources/polymarket/` con fecha de sincronización, antes de consumir Astra/Fable.
- No se implementa código del engine hasta cerrar M0–M2.

## 🧭 Autoridad documental y economía de tokens

### Regla principal

**Este archivo es la autoridad operativa única del proyecto.**

Astra, Fable, TOP y NORMAL deben trabajar contra este archivo y actualizar aquí sus decisiones/handoffs relevantes. No crear ADRs, design docs, plans ni SPECs fragmentados salvo que exista una razón material que el owner apruebe.

Separación permitida:

- `Polymarket Engine — MVP.md` → producto, arquitectura vigente, decisiones, gates, plan de implementación y handoffs.
- `Polymarket Engine — Opportunity Context.md` → contexto de oportunidad, bankroll, criterios económicos y familias de estrategias.
- `30-resources/polymarket/` → conocimiento externo compilado: API/protocolo, Deep Research, papers, fuentes y contradicciones.
- repo de código → documentación estrictamente necesaria para operar/desarrollar el software.

**Anti-bloat:** ningún agente crea “un documento por pensamiento”. Si una decisión cabe aquí, se actualiza aquí.

## 🧱 Producto — Polymarket Engine MVP

### Principio arquitectónico

```text
                     POLYMARKET ENGINE
                Go · modular monolith · 1 host
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
 market/protocol        research runtime      trading runtime
        │                     │                     │
 discovery              recorder/replay        auth/orders
 metadata/rules         experiment runner      reconciliation
 CLOB REST/WS           screen/shadow          capital/risk
 local books            datasets/metrics       kill switch
 positions/tokens       external-data hooks    live execution
 fees/incentives
 NegRisk primitives
 resolution lifecycle
        │
        └─────────────────────┬─────────────────────┘
                              ▼
                      STRATEGY CONTRACT
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
          POC-S01         POC-S02         POC-Sxx
          NegRisk         Sports          futuras
```

### Capabilities objetivo del Engine MVP

El Deep Research técnico debe confirmar nombres, contratos y autoridad exacta; esta lista define **capability intent**, no endpoint contracts todavía.

**Protocol / market model**
- Event / Market / Outcome / Token / Condition / parent-child relationships.
- Market lifecycle y estado operacional.
- Rules y resolution source versionadas cuando sea posible.
- NegRisk/Augmented NegRisk semantics.
- Positions/tokens, split/merge/redeem/conversion primitives relevantes.
- Combos/RFQ sólo si el research demuestra que son materialmente útiles al producto; no asumir.

**Market data**
- market discovery/catálogo;
- CLOB REST snapshots;
- market WebSocket y recovery;
- canonical in-memory order books;
- best bid/ask, midpoint, last trade y full depth separados;
- timestamps exchange/source/receive;
- gap, staleness y reconnect detection;
- metadata updates/new-market lifecycle.

**Recorder / datasets / replay**
- raw event recording;
- normalized events;
- deterministic replay;
- versionado de fee/rebate/reward/rules regimes por timestamp cuando aplique;
- reproducibilidad de un experimento;
- datasets derivados sin contaminar raw evidence.

**Research / hypothesis runtime**
- strategy/hypothesis registry;
- common experiment metadata;
- screen/read-only mode;
- replay mode;
- shadow mode;
- comparison scorecards;
- optimistic/base/stress fill models;
- executable-depth/VWAP primitives;
- latency sensitivity.

**Trading / execution**
- wallets/auth/session model exacto según docs;
- order create/cancel/manage lifecycle;
- real-time user/order updates;
- idempotency/retry/recovery semantics;
- reconciliation entre local state, CLOB y chain/account state;
- sizing, bankroll/exposure accounting, local risk;
- kill switch/cancel-all;
- live mode sólo después de certificación.

**Economics / incentives**
- fees como parámetros dinámicos, nunca constantes globales;
- maker/taker rebates;
- liquidity rewards;
- market competitiveness/eligibility cuando esté expuesto;
- capital lock y settlement timing como datos económicos.

**External data seam**
- el Engine debe admitir que una strategy consuma una fuente externa sincronizada (weather, sports, macro, crypto) sin convertir hoy esa posibilidad en un framework universal.
- primera implementación concreta sólo cuando una POC promovida la necesite.

**Observability**
- p50/p95/p99 del pipeline `receive → book → strategy → decision → send → ack/fill`;
- CPU/RAM/GC/disk I/O/queue depth;
- WS gaps/reconnects/staleness;
- strategy/opportunity/fill/reconciliation metrics;
- evidencia suficiente para distinguir fallo de infraestructura de ausencia de edge.

### Deliberadamente fuera del MVP del engine

- venue-agnostic abstractions;
- Kafka/Flink;
- microservicios por estrategia;
- Kubernetes por defecto;
- multi-region/co-location/HFT infra sin evidencia;
- Echo integration;
- UI compleja;
- LLM en el hot path;
- modelos ML específicos de estrategia;
- cualquier capability cuyo único argumento sea “quizás algún día”.

## 🖥️ Topología inicial

**Una máquina grande, con holgura deliberada.**

Objetivo: durante discovery/validación no introducir como variables independientes problemas de scheduling, service discovery, cross-host latency, consistencia distribuida o starvation de recursos.

Principios:

- hot state local;
- suficiente CPU/RAM/NVMe para recorder + replay + múltiples screeners;
- persistencia/analytics fuera del hot path;
- medir antes de optimizar coste;
- extraer proceso/host sólo por profiling, aislamiento real o recurso especializado.

## 🧩 Strategy POC contract

Una POC implementa **sólo lo que la hace distinta**. Conceptualmente:

```text
strategy
  ├── universe / eligibility
  ├── required data
  ├── relationship | fair-value model
  ├── opportunity detector
  ├── strategy-specific feasibility
  └── strategy-specific metrics
```

El engine conserva:

```text
market-data
books
recorder/replay
datasets
fees/incentives
full-depth execution model
shadow lifecycle
capital/risk
orders/reconciliation
observability
```

Una strategy no implementa su propio WebSocket, wallet, risk engine o replay si la capability ya pertenece al core.

## 🧪 Hypothesis lifecycle

Backlog objetivo: **20–30 hipótesis**, no 20–30 bots.

```text
IDEA / PE-xxx
    ↓
CHEAP TRIAGE
    ├── NO_SIGNAL / NO_DATA / BAD_ECONOMICS → REJECTED
    └── SURVIVES
          ↓
STRATEGY-SPECIFIC DEEP RESEARCH
          ↓
POC DESIGN / ASTRA WEEK si lo justifica
          ↓
SCREEN
          ↓
REPLAY
          ↓
SHADOW
          ↓
TINY_LIVE
          ↓
PROMOTED

cualquier etapa → ITERATING → nueva revisión
```

**Regla:** no gastar Deep Research grande ni Astra en una hipótesis que un cheap triage pueda matar.

Cada hipótesis conserva:

```text
id
mechanism
universe
required data
signal/detector
capital lock
capacity
latency sensitivity
competition
supporting evidence
contrary evidence
minimum experiment
GO / NO_GO
status
parent iteration
```

## 🧠 Uso de modelos premium — workflow frozen

### Principio

Astra y Fable **no descubren la API ni navegan documentación básica durante el diseño**. Toda información técnica vigente debe estar preparada antes en `30-resources/polymarket/`.

### Fase de diseño

```text
TECHNICAL RESOURCE PACK
        ↓
ASTRA — propuesta completa
        ↓
FABLE — adversarial challenge
        ↓
ASTRA — reconcile / segunda pasada
        ↓
FABLE — challenge final acotado si quedan findings materiales
        ↓
DESIGN FROZEN EN ESTE ARCHIVO
```

No hacer ping-pong infinito. Máximo esperado: **2 pasadas Astra + 1–2 Fable** para converger, salvo blocker material.

### Economía de Astra

Astra tiene cuota escasa (~3–4 shots/semana). Cada shot debe recibir un `CONTEXT PACK` cerrado y usar su ventana larga para trabajo estructural, no tareas pequeñas.

Uso preferente por fase:

1. propuesta/diseño completo;
2. reconciliación tras challenge;
3. auditoría de implementación o issue crítico;
4. shot de reserva si existe.

No usar Astra para collectors, structs, queries, boilerplate o bugs normales.

### Ventana Fable actual

Hasta 2026-09-20 existe cuota remanente de Fable en Cursor. Prioridad inmediata: **usar Fable intensamente en el Engine MVP**, especialmente para challengear propuestas de Astra, identificar capabilities omitidas y atacar boundaries antes de congelar diseño.

## 🏗️ Delivery workflow del Engine

### M0 — Technical Knowledge Pack

**Objetivo:** mapear Polymarket técnico antes de diseño.

Entregable canónico en `30-resources/polymarket/`:

`Polymarket — Technical Platform Map — synced YYYY-MM-DD`

Debe incluir como mínimo:

- docs index/llms.txt y changelogs;
- hosts/base URLs;
- Gamma/market discovery;
- Data API;
- CLOB REST;
- WebSockets públicos y autenticados;
- RTDS/sports/Chainlink feeds si aplican;
- entities/IDs y relaciones;
- order book semantics;
- auth/wallet/session keys/signatures;
- order types/lifecycle/status/error/retry semantics;
- positions/tokens/CTF actions;
- NegRisk/Augmented NegRisk;
- resolution/UMA/redeem;
- fees/rebates/rewards;
- rate limits;
- contracts/addresses/audits;
- matching-engine restart semantics;
- OpenAPI/AsyncAPI artifacts;
- official SDKs y qué esconden vs API directa;
- historical-data availability/retention;
- deprecated/migrated endpoints;
- known ambiguities/contradictions;
- sync timestamp y source URLs por sección.

**Gate M0:** Astra/Fable pueden diseñar el engine sin salir a internet para descubrir facts básicos.

### M1 — Astra/Fable Engine Design

**Input:** este proyecto + Technical Platform Map + Edge Research Consolidado + restricciones del owner.

**Output:** actualización de ESTE archivo con:

- architecture boundaries;
- canonical domain model;
- data flows;
- state ownership;
- interfaces/contracts internos;
- persistence model;
- concurrency/backpressure model;
- error/retry/reconnect semantics;
- recorder/replay determinism;
- strategy contract;
- shadow/live lifecycle;
- security/secrets boundary;
- observability;
- test/certification strategy;
- explicit non-goals;
- unresolved decisions = 0 para pasar M2.

**Gate M1:** Astra + Fable convergen; no findings arquitectónicos materiales abiertos.

### M2 — TOP Implementation Plan

Un agente TOP recibe el diseño frozen y produce **dentro de este archivo** el plan implementable:

- dependency order;
- slices/commits;
- allowed files/packages;
- contracts to implement;
- migration/persistence setup;
- unit/integration/property/replay tests;
- physical gates;
- rollback/recovery;
- exact definition of done.

El TOP **no rediseña** salvo blocker demostrable; si encuentra uno, devuelve `BLOCKED — DESIGN ISSUE` al manager/Astra.

### M3 — NORMAL Engine Implementation

Un agente NORMAL implementa el plan completo, preferentemente en una pasada coherente, con commits/gates definidos por M2.

- no inventar arquitectura;
- no expandir scope;
- failures/retries cerrados;
- tests obligatorios;
- actualizar este archivo al terminar;
- Agents-OS session close + feedback.

### M4 — Engine Certification

Antes de POC strategies:

- market discovery correcto;
- books/reconnect/recovery certificados;
- recorder/replay determinístico;
- regimes/metadata preservados;
- strategy test fixture funciona;
- shadow runtime funciona;
- auth/order plumbing puede permanecer disabled si live todavía no es necesario, pero interfaces/recovery deben estar diseñados;
- observability y resource headroom verificados;
- failure injection básica;
- no critical/open architecture debt.

**Engine MVP CLOSED** cuando la plataforma puede consumir una strategy POC sin alterar fundamentos del core.

## 🎯 Primeras Strategy POCs

### POC-S01 — NegRisk

Primera POC estructural. Antes de implementación:

1. cheap triage usando capabilities del engine;
2. Deep Research específico y actualizado de NegRisk/Augmented NegRisk, conversions, `Other`, placeholders, execution/capital semantics, proyectos/papers y failure modes;
3. Astra week sólo si el triage sigue vivo;
4. implementar strategy module;
5. screen → replay → shadow → `GO | ITERATE | NO_GO`;
6. tiny-live sólo si supera gates.

### POC-S02 — Sports Combinatorial

Segunda POC estructural. Mismo pipeline:

1. cheap triage;
2. Deep Research específico de combinatorial sports, event grouping, payoff-state modelling, live vs pregame, latency/capacity, evidence/failures;
3. Astra review week;
4. strategy module;
5. screen → replay → shadow;
6. tiny-live si GO.

El orden S01/S02 puede invertirse por evidencia o calendario, pero ambos son consumidores del mismo engine y ninguno redefine el core por conveniencia local.

## 💰 Capital y live

Bankroll tiny-live inicial total: **US$300**.

Aplica a strategies promovidas, no al Engine MVP. Reglas:

- el engine puede existir y cerrar MVP sin arriesgar capital;
- POC strategy no necesita tiny-live para demostrar NO_GO;
- estrategias GO compiten por el mismo bankroll;
- diversificar entre eventos independientes cuando existe edge;
- capital ocioso es válido;
- caps por event/strategy derivados de shadow/stress, no inventados antes de datos.

## ✅ Tareas

### Ahora — M0
- [ ] Ejecutar Deep Research técnico oficial de Polymarket #owner/me #type/research #area/personal
- [ ] Ingerir resultado como `Polymarket — Technical Platform Map — synced YYYY-MM-DD` en `30-resources/polymarket/` #owner/me #type/research #area/personal
- [ ] Reconciliar contradicciones con docs oficiales/changelog/OpenAPI/AsyncAPI #owner/me #type/research #area/personal
- [ ] Confirmar repo/nombre de implementación Go #owner/me #type/dev #area/personal

### M1
- [ ] Preparar context pack único para Astra/Fable #owner/me #type/research #area/personal
- [ ] Astra: diseño completo Engine MVP #owner/me #type/dev #area/personal
- [ ] Fable: adversarial challenge del diseño #owner/me #type/dev #area/personal
- [ ] Astra: reconcile y freeze #owner/me #type/dev #area/personal
- [ ] Fable: challenge final sólo si quedan findings materiales #owner/me #type/dev #area/personal

### M2–M4
- [ ] TOP: implementation plan frozen en este archivo #owner/me #type/dev #area/personal
- [ ] NORMAL: implementar Engine MVP #owner/me #type/dev #area/personal
- [ ] Certificar Engine MVP #owner/me #type/dev #area/personal

### Strategy pipeline
- [ ] POC-S01 NegRisk: triage → DR → design/review → implementation → shadow #owner/me #type/research #area/personal
- [ ] POC-S02 Sports: triage → DR → design/review → implementation → shadow #owner/me #type/research #area/personal
- [ ] Mantener backlog PE-001…PE-030 priorizado por coste de falsación #owner/me #type/research #area/personal

## 📆 Bitácora

- **2026-09-15** — Inicio como proyecto de arbitraje Sports + NegRisk.
- **2026-09-16** — Se consolida research en 30 hipótesis y se adopta modular monolith / single large host.
- **2026-09-16** — Reframing canónico: **Engine = MVP durable; strategies = POCs**. Se define M0 Technical Knowledge Pack antes de Astra/Fable y delivery `Astra → Fable challenge → Astra reconcile → TOP plan → NORMAL implementation`.

## 🧭 Decisiones frozen

- `D-001` — Producto canónico: **Polymarket Engine — MVP**.
- `D-002` — Engine agnóstico de estrategia, deliberadamente Polymarket-specific.
- `D-003` — Go + modular monolith + un deployable + un host grande inicialmente.
- `D-004` — Engine no es POC; strategy modules sí lo son y pueden descartarse.
- `D-005` — Un solo archivo de proyecto como autoridad operativa; evitar proliferación documental.
- `D-006` — Antes del diseño, crear mapa técnico completo de la plataforma desde fuentes oficiales.
- `D-007` — Astra/Fable no gastan contexto descubriendo endpoints básicos.
- `D-008` — Diseño: Astra propone, Fable challengea, Astra reconcilia; ping-pong acotado.
- `D-009` — TOP planifica implementación después del design freeze; NORMAL implementa sin rediseñar.
- `D-010` — NegRisk y Sports son POC-S01/S02, primeros consumidores del Engine.
- `D-011` — Cada estrategia posterior pasa cheap triage antes de Deep Research/Astra.
- `D-012` — Bankroll tiny-live US$300 total aplica a strategies promovidas; no define éxito del Engine MVP.
- `D-013` — Echo/Echo Forge siguen separados hasta evidencia posterior de integración útil.
- `D-014` — No Kafka/Flink/K8s/microservices salvo necesidad demostrada.

## 🔗 Docs / Links

- [[Polymarket Engine — Opportunity Context]]
- [[Research — Merge de cuatro Deep Research]]
- [[Polymarket — Edge Research Consolidado 2026-09-16]]
- [[polymarket/00-index]]
- Polymarket official docs: https://docs.polymarket.com/
- Polymarket official docs index: https://docs.polymarket.com/llms.txt

## 💡 Principios

- El engine se optimiza para **falsar hipótesis rápido y de forma reproducible**, no para demostrar que una estrategia favorita funciona.
- `net executable edge > theoretical edge`.
- observabilidad suficiente para separar “no hay edge” de “nuestro sistema midió mal”.
- lo común se promueve al core sólo cuando es verdaderamente común o es capability fundamental de Polymarket.
- una strategy no deforma el core para facilitar su propia POC.
- ninguna IA premium debe gastar una ventana larga en información que pudimos preparar previamente.
