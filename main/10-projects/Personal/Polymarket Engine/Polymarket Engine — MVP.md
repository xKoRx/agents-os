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
updated: 2026-09-17
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
- **M0 DESIGN_READY (documental, 2026-09-17):** Technical Platform Map canónico indexado en `30-resources/polymarket/`, con 11 partes, 7/7 OpenAPI (163 operaciones) y siete RG resueltos para diseño con exclusiones; no habilita live ni NegRisk conversion. Siguiente gate: revisión conjunta y M1 Astra → Fable → Astra.
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

**Gate M0: PASS — DESIGN_READY documental (2026-09-17).** Astra/Fable pueden diseñar sin descubrir contratos básicos. Ver [[Polymarket — Technical Platform Map — synced 2026-09-17]] y §24 de part-10. Límites frozen de M0: CTF/v2 conversion LIVE DISABLED; L2 historical backfill DISABLED; RFQ/Combos OUT_OF_SCOPE inicial; `deferExec=true`/Builder optional DISABLED; trading live sujeto a pruebas de auth, execution y reconciliación en M2–M4. Este gate NO constituye design freeze ni certificación live.

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
- [x] Ejecutar Deep Research técnico oficial de Polymarket #owner/me #type/research #area/personal
- [x] Ingerir resultado como `Polymarket — Technical Platform Map — synced YYYY-MM-DD` en `30-resources/polymarket/` #owner/me #type/research #area/personal
- [x] Reconciliar contradicciones con docs oficiales/changelog/OpenAPI/AsyncAPI #owner/me #type/research #area/personal
- [x] Confirmar nombre de repo de implementación Go: `xKoRx/polymarket-engine` (nombre acordado; verificar creación por separado) #owner/me #type/dev #area/personal

### M1
- [ ] Revisión conjunta owner/manager del M0 DESIGN_READY y boundaries disabled; no reabrir research general salvo blocker concreto
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
- **2026-09-17** — M0 DESIGN_READY documental: 11 partes del Technical Map; 7 OpenAPI/163 operaciones, RFQ AsyncAPI 13/13, Data v2 y NegRisk CTF investigados. Sin certificación live; conversion CTF/v2, historical L2 backfill y modos opt-in deshabilitados. Paso siguiente: revisión conjunta → ASTRA-1.

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
- [[Polymarket — Technical Platform Map — synced 2026-09-17]] — índice canónico y 11 partes, knowledge pack M0 DESIGN_READY.
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

## M1 — ASTRA Architecture Proposal

**Estado del shot:** `M1_ASTRA_PROPOSAL_READY_FOR_FABLE` · **Etiqueta:** `M1 — ASTRA PROPOSAL — READY FOR FABLE` · **Autor:** ASTRA-1 · **Fecha:** 2026-09-17. Esta sección propone arquitectura; no congela M1, no aprueba gates físicos, no implementa estrategias y no contiene el plan de coding de M2. Las decisiones `D-001…D-014` y el gate documental M0 permanecen vigentes. Todas las decisiones nuevas requieren challenge de FABLE y reconciliación antes del freeze.

### M1.0 — Base documental, autoridad y criterio de éxito

**Baseline leído antes de editar:** `xKoRx/agents-os`, `master`, HEAD local y remoto `822d6241de37628dfe04ab1683fbb3e79b899dd6`, worktree limpio; blob original del proyecto `10f2c8df0b95e5147aef5457e80ef4cb721de054`. Bootstrap mínimo de Agents-OS aplicado; ninguna fuente técnica ajena al context pack fue consultada. No se abrieron Internet, SDKs, contratos externos, investigaciones originales ni otros proyectos.

| Referencia interna de esta propuesta | Fuente leída íntegramente | Uso y autoridad |
|---|---|---|
| Proyecto | Este archivo, contenido anterior a M1 | Producto, macroarquitectura, capabilities, capital y workflow frozen |
| TPM / manifiesto | [[30-resources/polymarket/Polymarket — Technical Platform Map — synced 2026-09-17]] | Once partes verificadas individualmente y concatenadas: **287930 bytes**, SHA-256 `ca7e3329b39f666fa0d383ffae194e6aa09f2e741b31cea61a4dc72136be8938`, manifiesto 2026-09-17 15:35 UTC |
| P01, §§1–2 | [[30-resources/polymarket/Polymarket — Technical Platform Map — part-01-foundations]] | Superficies e identidades |
| P02, §3 | [[30-resources/polymarket/Polymarket — Technical Platform Map — part-02-rest-catalog]] | REST y DTO Data v2 |
| P03, §§4–6 | [[30-resources/polymarket/Polymarket — Technical Platform Map — part-03-auth-precision-time]] | Auth, precisión y relojes |
| P04, §§7–8 | [[30-resources/polymarket/Polymarket — Technical Platform Map — part-04-orders-lifecycle]] | Firma/DTO/wrapper, órdenes y ambigüedad |
| P05, §§9–11 | [[30-resources/polymarket/Polymarket — Technical Platform Map — part-05-market-data-positions-contracts]] | WS, books, posiciones y contratos |
| P06, §§12–13 | [[30-resources/polymarket/Polymarket — Technical Platform Map — part-06-negrisk-combos]] | CTF/v2, NegRisk, exclusión Combo/RFQ |
| P07, §§14–18 | [[30-resources/polymarket/Polymarket — Technical Platform Map — part-07-economics-resolution-history-limits]] | Fees, incentivos, resolución, históricos y cuotas |
| P08, §§19–21 | [[30-resources/polymarket/Polymarket — Technical Platform Map — part-08-specs-sdks-changelog]] | Extracciones posteriores, schemas, versiones y discrepancias |
| P09, §§22–23 | [[30-resources/polymarket/Polymarket — Technical Platform Map — part-09-security-workflows]] | Seguridad y flujos de protocolo |
| P10, §§24–25 | [[30-resources/polymarket/Polymarket — Technical Platform Map — part-10-gaps-recovery]] | Estado vigente M0, límites y recovery |
| P11, §26 | [[30-resources/polymarket/Polymarket — Technical Platform Map — part-11-sources]] | Provenance y snapshots; sus URLs no se visitaron en este shot |
| ERC, §§2–8 | [[30-resources/polymarket/Polymarket — Edge Research Consolidado 2026-09-16]] | Requisitos transversales de falsación, costes, sesgos y evidencia; no autoridad de protocolo ni estrategia implementada |

**Precedencia acotada:** el cierre fechado de P10 §24 gobierna el estado de M0 sobre encabezados históricos que todavía dicen “RG pendiente”; los DTO expandidos de P02 §3.4.1 y P08 §19.1.1 precisan tablas anteriores. Una contradicción técnica que esas ampliaciones no resuelven se conserva como incertidumbre. Ejemplos: fees Sports del ERC no se convierten en configuración; §25.2 rotula keyset como CLOB, mientras el inventario S39 lo ubica en Gamma: este diseño usa el host Gamma del inventario de operaciones. `GET /markets/{conditionId}` de §25.1 no reemplaza el contrato explícito CLOB `/clob-markets/{condition_id}`. No se corrige ni se modifica el pack en M1.

**Éxito del engine:** un consumidor nuevo declara universo, datos y lógica diferenciadora; obtiene captura, replay, economics, shadow, risk y métricas comunes sin construir infraestructura paralela. Medir `TIME_TO_VALIDATED_HYPOTHESIS` desde registro aceptado hasta scorecard revisable `GO / ITERATE / NO_GO`, incluyendo tiempos de espera por datos y separando horas humanas, cómputo y coste. No se promete rentabilidad ni se exige desplegar los US$300 para cerrar el MVP.

### M1.1 — Matriz contractual y superficie activable

Los estados siguientes no son sinónimos. `SUPPORTED FOR DESIGN` admite modelar una capability; `IMPLEMENTABLE FROM DOCUMENTED CONTRACT` permite construir la ruta descrita, sin certificarla; `REQUIRES INTEGRATION VALIDATION` bloquea su activación live hasta evidencia; `DISABLED` impide construir/enrutar una operación ejecutable; `OUT_OF_SCOPE` excluye la implementación inicial. Una fila puede tener estado documental y estado operativo distintos.

| Capability | Suficiencia documental | Estado operativo propuesto y condición |
|---|---|---|
| Discovery Gamma, snapshots REST, Market WS básico | IMPLEMENTABLE FROM DOCUMENTED CONTRACT | Read-only tras gates de parsing/recovery; continuidad siempre observada, nunca garantizada |
| Lifecycle `new_market`, resolución WS y Sports | SUPPORTED FOR DESIGN; campos críticos descritos | Parsing conservador; variantes no expandidas quedan como observación raw y disparan refresh, no inferencias de fields ausentes |
| Recorder, replay de captura, datasets, SCREEN, SHADOW | SUPPORTED FOR DESIGN | Implementables como contrato interno; gates M1.15 pendientes |
| Data v2 posiciones/trades/activity/resolutions | IMPLEMENTABLE FROM DOCUMENTED CONTRACT | Lecturas agregadas; no sustituyen el ledger privado ni la cadena |
| Auth L1/L2 y órdenes CTF sobre CLOB v2, User WS, cancel/reconcile | IMPLEMENTABLE FROM DOCUMENTED CONTRACT + REQUIRES INTEGRATION VALIDATION | `LIVE_DISABLED` por defecto; aprobación independiente por wallet, protocolo y operación |
| Fee inputs y cálculo publicado | IMPLEMENTABLE FROM DOCUMENTED CONTRACT en el alcance de P03/P07 | Mapping de parámetros y redondeo no totalmente resueltos: economics intervalar; live taker bloqueado donde no exista cota certificada |
| CTF split/merge/redeem | IMPLEMENTABLE FROM DOCUMENTED CONTRACT + REQUIRES INTEGRATION VALIDATION | Capability modelada; dispatch de transacción deshabilitado inicialmente; no es prerequisito de M4 read-only/shadow |
| Protocol-v2 posiciones, rutas Router/PositionManager | SUPPORTED FOR DESIGN | Observación/identidad versionada; encoding y ejecución de cada operación requieren contrato y certificación adicionales |
| NegRisk conversión CTF | SUPPORTED FOR DESIGN; ABI fuente documentada | **DISABLED live**: deployment, mapping, permisos y ruta sin certificación; simulación sólo bajo supuestos explícitos |
| NegRisk conversión Protocol-v2 | SUPPORTED FOR DESIGN como capability ausente | **DISABLED**, ABI/selector y flujo de assets no verificados; no se prepara calldata |
| Backfill L2 vía `/orderbook-history` | No hay contrato de completitud | **DISABLED**; no reemplaza recorder ni rellena silenciosamente gaps |
| `deferExec=true`; Builder optional/CRUD/atribución | Fuera del contrato certificado | **DISABLED**; `deferExec=false`, builder cero y sin opciones para activarlos por estrategia |
| Combo/RFQ/Exchange-v3; Bridge/funding automático | Documentados parcialmente, sin necesidad inicial | **OUT_OF_SCOPE**; Sports combinatorial es relación entre mercados, no autorización de Combo/RFQ |
| Session Keys beta, auto-deploy de wallet, auto-approvals | SUPPORTED FOR DESIGN en su scope documentado | **DISABLED inicialmente** por propuesta de seguridad; owner puede promover una ruta después, nunca heredar permiso del SDK |
| External-data seam | SUPPORTED FOR DESIGN | Envelope, calidad y replay comunes; adaptador externo concreto sólo al promover una POC que lo requiera |

**Invariante:** el registro de capabilities es una allowlist versionada y cerrada. Una capability ausente, desconocida o deshabilitada no produce un comando de ejecución. Un flag de configuración no puede crear un adapter que el registro no ofrece. `LIVE_ENABLED` jamás levanta en bloque los bloqueos de conversión, v2 o modos opcionales.

### M1.2 — Arquitectura, responsabilidades y ownership

**Propuesta:** un binario Go, un proceso de servicio, módulos internos con puertos estrechos, SQLite embebido para estado transaccional, journal raw segmentado en NVMe y datasets Parquet derivados. El mismo binario puede correr el modo offline de replay; no se agrega un servicio por estrategia, una cola distribuida ni una segunda base operativa. Analytics/exportación y replay usan presupuestos de recursos independientes del servicio activo.

```text
CONTROL: config versionada + capability registry + supervisor + control local
                         │ inicia y revoca permisos
Gamma / CLOB / WS / Data / chain reads / external seam
                         │ adapters de transporte (sin dominio mutable)
                         ▼
Ingress → Capture Journal → watermark durable → normalizadores versionados
                                                   │
              ┌─────────────────┬──────────────────┼──────────────────┐
              ▼                 ▼                  ▼                  ▼
        Catalog/Universe    Book shards       Regime/Resolution   Account observations
              └─────────────────┴─────────┬────────┘                  │
                                  immutable frames                   ▼
                                         │                  Account Coordinator
                                  Strategy Runtime             orders/fills/ledger
                                         │                           ▲
                                   Opportunity                       │
                                         ▼                           │
                                Economics/Evaluator                  │
                                         │                           │
                               candidate action                      │
                                         ▼                           │
                           Risk + atomic reservation ────────────────┤
                                         │                           │
                         SCREEN | Simulator | Live gateway ──────────┘
                                              │
                                 Credential boundary → CLOB

Journal + versioned state → Replay/Experiments → scorecards/datasets
Observability recibe métricas de todos; nunca controla dominio por logging.
```

| Módulo | Responsabilidad y único estado del que es owner | Puertos/dependencias permitidos |
|---|---|---|
| Composition / Supervisor | Ciclo del proceso, capability registry, leases de activación, config revision, fallos y readiness | Construye adapters y módulos; puede detenerlos, no modificar sus proyecciones directamente |
| Transport / Venue adapters | Conexiones REST/WS, subscriptions deseadas, epochs, rate budgets IP/signer, parsing de envelope y auth de transporte | Escribe en Ingress; recibe comandos de Catalog/Execution por puertos; no escribe books ni posiciones |
| Capture | Orden local de admisión, journal, watermarks durables, manifests, integridad y discontinuidades | Recibe evidencia/control; entrega offsets; no conoce fórmulas de estrategias ni decide órdenes |
| Catalog / Universe | Revisiones Event/Market/Outcome/Asset/Condition, relaciones documentales, reglas y membership por consumidor | Lee observaciones normalizadas; publica revisiones inmutables y subscription demand; consulta REST mediante adapter |
| Market Data | Books por asset, revisión, epoch, calidad; proyecciones BBO/midpoint/trade separadas | Consume catálogo/WS; publica snapshots inmutables; no llama estrategias ni REST desde el reducer |
| Regimes / Resolution | Versiones de tick/min-size/fee/reward/delay y observaciones de resolución con provenance | Consume REST/WS/chain; publica constraints y lifecycle; cambios de régimen invalidan frames y candidatos |
| Frame Builder / Runtime | Suscripciones de consumidores, frames consistentes localmente, secuencia de delivery, estado de cada instancia Go | Lee snapshots; invoca estrategia serialmente; publica resultados; no conoce credenciales |
| Economics / Simulator | Funciones puras de VWAP, costes, capital y fill models; estado de órdenes/fills **simulados** en namespace del experimento | Recibe frame+candidato+modelo; emite resultados sintéticos identificados; nunca actualiza cuenta real |
| Risk | Reglas versionadas de límites, eligibility y sizing, evaluador puro sobre snapshot de cuenta | Devuelve decisión acotada al Account Coordinator; no mantiene una segunda copia de balance disponible |
| Account Coordinator | **Único writer de cuenta real:** órdenes/intents, fills, reservas, posiciones contables, balances observados, dedup y casos de reconciliación | Ejecuta reducers Risk/Orders/Ledger dentro de una transacción local; recibe observaciones de Reconciler y resultados Execution |
| Execution / Reconciler | Execution posee intentos de I/O, no balance; Reconciler posee jobs/cursors/observaciones pendientes, no ledger alternativo | Execution consume autorizaciones del Coordinator; Reconciler consulta REST/User WS/chain y propone hechos al mismo Coordinator |
| Credentials / Signing | Material secreto y sesión autenticada, perfil wallet y permisos; firma sólo payload tipado ya autorizado | Sólo Execution autorizado puede solicitar firma/envío; no puerto genérico `sign(bytes)` a estrategias |
| Experiment / Dataset | Registry de hipótesis, manifests inmutables, parámetros, versiones, scorecards, pins de retención, artefactos derivados | Consume capture/projections/runtime; no toca tablas privadas de ejecución ni reescribe raw |
| Operations / Telemetry | Logs, métricas, alertas y comandos locales autenticados | Kill/control por Supervisor; consultas de snapshots; no SQL arbitrario ni callbacks de estrategia |

**Regla de acoplamiento:** domain values y contratos públicos no importan adapters. Un módulo no importa implementaciones/repositorios de otro ni consulta sus tablas; solicita una vista o emite un comando tipado. No hay “event bus de cualquier cosa” ni service locator global. Los eventos de observación y comandos de efecto son tipos distintos. El composition root es el único lugar que conecta puertos. Los reducers de cuenta comparten una transacción porque reserva, intent y exposición forman una sola unidad de consistencia; esta dependencia es deliberada y no se extiende a catálogo, books o analytics. Contratos, dependencias y ownership se verifican en revisión y pruebas de imports de M2, sin inventar hoy un árbol de paquetes definitivo.

**Hot path:** admisión/captura durable → normalización → book/quality → frame → detector/evaluator → decisión; en live agrega reserva/intent durable → firma/envío. No LLM, consultas analíticas, exportación, metadata REST síncrona ni llamadas arbitrarias de estrategia. La latencia de fsync es parte del coste elegido y debe medirse. **Cold path:** discovery/refresh, compactación, SQL de reporting, extracción Parquet, backups, fixtures, replay y scorecards. Reconciliación, heartbeat y cancelación son un carril operacional prioritario; no compiten detrás de screener/replay.

**Inicio:** lock exclusivo de cuenta/estado local → validar config/schema/manifests/capabilities → recuperar journal y transacciones → iniciar captura y observabilidad → adapters públicos/catálogo/constraints → suscripciones y books nuevos → admitir runtimes elegibles. Un perfil live agrega carga explícita de identidad, check de restricciones/clock, User WS, reconciliación completa y resolución de intents ambiguos; siempre arranca `LIVE_DISABLED/RECOVERING`, nunca retoma permiso previo por persistencia de un booleano. Fallar startup de un writer no impide exponer health y diagnóstico read-only.

**Shutdown:** cerrar admisión de nuevas oportunidades/órdenes → revocar lease de envío → cancelar remanentes según política de cuenta → mantener User WS/REST y recorder mientras se concilia → detener estrategias cooperativamente → sellar journal/watermark y cerrar stores. Deadline agotado deja `UNCLEAN/UNRESOLVED` durable y alerta; no registra shutdown limpio ni “sin órdenes” sin prueba. SIGKILL/power loss se trata como recovery, no como ejecución de este protocolo.

### M1.3 — Dominio canónico, unidades y temporalidad

Clases: **E** entidad con identidad estable y estado mutable bajo owner; **S** snapshot inmutable con revisión; **D** derivación reproducible; **O** evento observado con provenance. Toda revisión conserva `observed_at`, `source_at?`, `source_ref`, `capture_ref`, versión del normalizador y payload hash. `effective_from` sólo existe si la fuente lo establece; ausencia significa “conocido desde observación”, no vigencia histórica inventada. Dos tiempos separados evitan usar metadata futura en replay.

| Modelo | Identidad interna y relaciones obligatorias | Clase / autoridad |
|---|---|---|
| Event | `GammaEventID` decimal canónico como string; slugs son atributos; contiene relaciones hacia markets y, cuando documentado, parent/subevents | E + S; Catalog, Gamma |
| Market | `GammaMarketID` independiente; links `ConditionRef?`, Event IDs, outcomes ordenados, reglas/source y operational flags | E + S; Catalog; trading eligibility derivada cruza CLOB/constraints |
| Outcome | `(GammaMarketID, outcome_index)` y label versionado; rol YES/NO validado por mapping, no por BUY/SELL | S; array de outcomes alineado con IDs, nunca join sólo por etiqueta |
| Asset / Token / Position instrument | `AssetKey{chain_id, protocol, token_contract?, wire_asset_id}`; variante CTF con token uint256; variante ProtocolV2 con position ID opaco validado por su contrato | E + S; Catalog. `AssetID` CLOB es identificador wire dentro de contexto, no wallet holding |
| Condition | `ConditionRef{protocol, raw_id}`, CTF bytes32; `QuestionID` separado; oracle/payout refs si conocidos | E + S; Catalog/Resolution, sin derivación especulativa v2 |
| Market relationship | `RelationshipID` local + revisión, endpoints tipados y tipo: containment, complement, documented NegRisk membership, semantic relation propuesta | S + D; fuente/evidencia, exhaustividad y exclusividad `UNKNOWN/VERIFIED/INVALIDATED`; compartir Event no prueba equivalencia de payouts |
| NegRisk context | Gamma Event, `NegRiskMarketID` contractual bytes32 separado, question indices/bitmasks, CTF/v2, augmented slots, `Other` y revisión de membresía | S; mapping sólo con evidencia; no cast desde Event ID o condition ID |
| Order | `IntentID` local estable + `OrderHash?` venue; cuenta/scope, AssetKey, BUY/SELL, size/price, policy, reserva, revisiones de frame/config; placement, estado REST y envío separados | E + S + O; Account Coordinator |
| Trade / Fill | `VenueTradeID` opaco por servicio; `FillKey=(account_scope, trade_id, order_hash, maker_leg_identity)` para aportes propios; IDs de maker/taker y tx/settlement independientes | O + S; reducer de cuenta; varias actualizaciones de un trade no son fills nuevos |
| Position holding | `(AccountID, AssetKey)`; cantidades settled, matched-pending, reservadas y disponibles por separado; lotes/cost basis y atribución por estrategia | E + S + D; Coordinator; Data v2 es observación, balances chain son hechos por bloque |
| Resolution | `ConditionRef/QuestionID`, reporter, proposal/dispute/finality, payout vector, block/hash/log index, raw status | O + S; Resolution. `end/closed/proposed/resolved/redeemable/redeemed` no colapsan |
| Fee configuration | `RegimeID/revision`, market/asset, campos raw `feesEnabled/base_fee/fd/mbf/tbf`, unidades y parser; curva/calculador aprobado aparte | S; Regimes. maker rebate, taker rebate, reward y builder fee son ledgers/configs distintos |
| Opportunity | `OpportunityID` local determinista por run/delivery/ordinal; estrategia, assets/relaciones, frame vector, assumptions, expiry y candidato de acciones | D inmutable, no orden ni reserva; múltiples revisiones no autorizan duplicación de intent |
| Strategy | `StrategyID` estable, versión de código/config/schema, requisitos, instancia y estado runtime | E + S; registry/runtime; POC-S01 NegRisk y POC-S02 Sports según este proyecto |
| Experiment | `ExperimentID`, revision/parent, hypothesis ID PE-xxx, manifest de datos/modelos, modo/seed, política de evaluación y scorecard | E durante ejecución; manifest y resultado sellados S; Experiment owner |

**Precisión Go propuesta:** tipos nominales distintos para cada ID; bytes32/address validados en sus namespaces. `uint256` se valida con enteros de precisión arbitraria, nunca `float64`. Precios/size/fees se parsean desde el lexema JSON (`json.Number` cuando wire es number) hacia decimal exacto `coefficient + scale`, con operaciones de enteros/racionales acotadas y copias defensivas; no exponer `*big.Int` mutable a consumidores. PnL admite signo; balances on-chain no. Unidades en tipos (`CollateralAmount`, `Shares`, `Price`, `BasisPoints`, `FeeCoefficient`), currency/contract/scale explícitos: pUSD E6 no se llama USDC.e por equivalencia supuesta. Internamente los niveles usan precio decimal normalizado, no tick index que cambie al cambiar el tick.

El boundary de órdenes aplica exactamente P03 §5: verificar grid/decimales de precio, size hacia abajo a dos decimales, amount con la secuencia publicada ceil/floor cuando corresponda, revalidar min-size y convertir a E6 según BUY/SELL. Desbordes, escalas desconocidas, amounts negativos y mapping ambiguo se rechazan. Adoptar salt seguro representable según el contrato documentado de DTO y conservarlo; nunca regenerarlo para ocultar un duplicate. Estadísticas/gráficas pueden usar floats con etiqueta de aproximación; decisiones monetarias y hash de resultados no.

**Tiempo:** conservar string/entero raw y unidad por campo; normalizar a instante UTC y precisión conocida sin inventar nanosegundos de fuente. Receive wall-time + offset monotónico por boot miden tiempos locales; monotónico no se compara entre reinicios. Order timestamp v2 ms, expiration/auth seconds, User WS seconds, Market WS ms y resolution Data v2 según tipo de lookup. Sentinel `69` en proposed price, outcome index `999`, fechas `1970-01-01` y timestamps `0` se preservan raw y normalizan a unknown en su contexto. Ni un cursor ni un timestamp es una secuencia global.

### M1.4 — Discovery, lifecycle y universos

| Etapa | Contrato propuesto | Invalidación / evidencia |
|---|---|---|
| Bootstrap catálogo | Gamma `/events/keyset` y `/markets/keyset`, `after_cursor` opaco, filtros explícitos y páginas capturadas; límite markets conservador ≤100 conforme P08 §21 | Persistir inicio/fin de scan y fingerprint de filtros/cursor. No afirmar snapshot atómico del catálogo |
| Campos de respuesta no expandidos | Usar sólo envelope/fields documentados; si la forma keyset no es suficiente para implementar desde el pack, fallback explícito a `/events` y `/markets` limit/offset de P02 | No inventar envelope keyset. Fallback conserva misma semántica de coverage parcial y validación de integración de U-03 |
| Refresh periódico | Nueva pasada desde primera página con dedup por ID; refrescar por ID markets activos, demandados, con posiciones o con órdenes; separar frecuencia activa/archivada | No borrar entidades porque no aparecieron en una pasada incompleta. Marcar ausencia/coverage y confirmar por lectura individual |
| Nuevos mercados | `new_market` WS es hint temprano hacia Catalog; realizar fetch Gamma/CLOB y validar antes de admitir | No depender de WS como índice exhaustivo; polling recupera altas no observadas |
| Identity join | Parsear arrays Gamma aunque vengan codificados como string; comprobar longitud, índices, unicidad y condición/asset en CLOB | Incompletitud o conflicto → `QUARANTINED`, sin book elegible ni firma |
| Rules/source/relaciones | Guardar cada versión observada de reglas, fuente, naming/Other y membresía; relink mediante IDs con evidencia | Cambio semántico invalida relaciones verificadas y oportunidades pendientes; no reetiquetar retrospectivamente datasets |
| Constraints | Capturar `/book`, `/clob-markets/{condition_id}`, fee lookup, tick lookup y updates WS; separar constraints de metadata editorial | Tick/min-size/fees/status nuevo invalida evaluaciones; ante contradicción no “última respuesta gana” sin revisar source/request epoch |
| Lifecycle | Flags editoriales, CLOB accepting/enabled, resolution observada, payout final y redención se conservan por separado | Cerrado/resuelto/pending deployment/identidad desconocida bloquea nuevos intents; órdenes existentes siguen en conciliación |

`UniverseSpec` es un selector declarativo sobre tags, tipos de mercado, Event/Market IDs, fechas, protocol y relationship requirements. Catalog devuelve `UniverseRevision{members, exclusions_with_reason, coverage, observed_at}` y `UniverseChanged` al runtime. La estrategia puede filtrar elegibilidad semántica sobre esa vista; no pagina Gamma ni maneja subscriptions. El Subscription Planner une/refcuenta las demandas de estrategias, recorder y cuentas; retiene assets con órdenes/posiciones aunque salgan del universo. Un scan incompleto puede servir investigación marcada parcial, pero no probar “no existen oportunidades”.

Sports consume eventos/markets/line/rules, books multiasset y, si declara necesidad, Sports WS con matching de `slug/gameId/team` versionado y verificado; un score sin join verificable no se asigna por similitud de título. NegRisk consume membresía/exhaustividad/Other versionados y protocol context. Ninguno necesita redefinir discovery. RTDS y proveedores futuros entran por `ExternalObservation{source, source_key, event_time, receive_time, payload_version, quality}` y el mismo recorder; el cálculo de fair value/payoff particular permanece en la estrategia.

### M1.5 — Market data, books y cutover sin garantías inventadas

**Unidad de ownership:** un asset pertenece a un solo book shard y a una sola conexión/epoch autora en cada momento. Un reader por conexión conserva orden de frames recibidos; los arrays/mensajes multiasset conservan ordinal interno. La serialización local por asset no prueba orden de generación del exchange. No se mezclan deltas de sockets distintos durante una migración: el nuevo epoch espera snapshot completo y el anterior queda fenced. Heartbeats: Market/User PING cada 10 s; Sports responde al ping del servidor de 5 s dentro del límite documentado de 10 s; RTDS PING 5 s si ese adapter se activa. Son contratos de transporte, no prueba de frescura del book.

| Estado de book | Significado interno | Uso autorizado |
|---|---|---|
| `UNINITIALIZED` | Sin full snapshot de epoch actual | Sólo diagnóstico |
| `SYNCING` | Subscription enviada; esperando `book`, constraints y mapping válidos | Sin oportunidades elegibles |
| `OBSERVED_USABLE` | Snapshot completo y updates admitidos, sin anomalía conocida, requisitos de freshness cubiertos | SCREEN/SHADOW y LIVE sólo con política certificada; calidad **best-effort observada**, nunca garantía lossless |
| `REST_OBSERVATION` | Foto REST independiente sin continuidad WS asociada | Triage/read-only o experimento explícito de snapshots; no baseline para mezclar deltas WS |
| `STALE` | Venció presupuesto de frescura de observación/check, source time o transporte | Bloquea evaluación ejecutable; puede reportar diagnóstico |
| `SUSPECT` | Overflow, regresión temporal significativa, crossed book, schema/ID conflict, control perdido o discrepancia de comprobación | Invalidación inmediata; nueva sincronización requerida |
| `HALTED` | Cierre/estado de mercado incompatible, protocolo no admitido o shutdown | Sin nuevos intents; no elimina posiciones ni cancela hechos de fills |

**Bootstrap normal:** suscribir Market WS con `initial_dump=true` y esperar `book` completo por asset (P05 §9). REST puede obtener constraints y una foto independiente durante ese período. Deltas anteriores al primer `book` se capturan pero no se aplican a una base REST ni se guardan para “replay después”: carecen de frontera comparable. El `book` inaugura el epoch local; sólo los mensajes recibidos después alimentan esa proyección. Timeout de initial book → renovar conexión/suscripción con backoff y permanecer bloqueado. Un book WS posterior sustituye niveles completos y aumenta revisión; no implica sanear incertidumbre de metadata/protocolo.

**REST → WS:** no existe operación de merge certificable entre ambas superficies. La foto REST se mantiene en su namespace; el primer full WS la reemplaza como fuente de continuidad, sin pegar deltas buffered por timestamp. **WS → REST:** tras gap, REST permite observar estado actual o comparar niveles; no reconstruye el intervalo perdido. Para reanudar updates se crea epoch nuevo con snapshot WS. Un modo degradado exclusivamente REST puede producir estudios de snapshots con disclosure, pero no habilita live ni completa un dataset L2. El precio de esta decisión es menor disponibilidad, elegido sobre una sincronización ficticia.

**Aplicación:** `book` reemplaza; `price_change` asigna size absoluto en lado/precio y size cero elimina; `last_trade_price` no muta niveles; BBO extendido no sustituye profundidad; tick change invalida constraints y candidatos, sin reescalar niveles antiguos. Books REST se reordenan canónicamente bids descendentes/asks ascendentes al normalizar (wire REST tiene best al final). Validar precios/rangos/unidades, sizes no negativos, asset/condition, duplicados de nivel, grid y BBO; un book vacío válido no equivale a error, pero no tiene profundidad ejecutable. Hash se conserva opaco, nunca se usa como cadena/checksum probado. No deduplicar mensajes de mercado sólo por timestamp/hash: dos observaciones iguales pueden ser legítimas; un delta size absoluto repetido no suma volumen.

**Orden y comprobaciones:** no ordenar deltas por timestamp de fuente ni retrasar mensajes para inventar una secuencia. El orden de recepción capturado manda para reproducir nuestro estado. Una regresión/dato incompatible se registra y vuelve `SUSPECT`; igualdad de timestamps no permite conocer causalidad. Comprobación REST periódica por sample/universo activo captura intervalo request→response y revisiones WS a ambos extremos; diferencias con tráfico concurrente son `INCONCLUSIVE`, no prueba de corrupción. Coincidencia de niveles/hash aporta evidencia limitada; ni siquiera una coincidencia demuestra ausencia de gaps. Una discrepancia no explicada dispara nueva sincronización, sin parche selectivo de niveles. Conservar métricas de falsos bloqueos para ajustar políticas con evidencia.

**Frame multiasset:** el Frame Builder solicita a los owners un corte local `capture_seq=C` y conserva la revisión de cada book/metadata/regime disponible a ese corte; los shards confirman un watermark procesado (también para posiciones sin mutación relevante). Entrega un vector inmutable, no lecturas sucesivas de punteros “latest” cambiantes. La antigüedad de cada book, la diferencia de receive times, source times con incertidumbre y el mayor offset durable forman parte del frame. Un corte local es coherencia de nuestra observación, **no snapshot simultáneo del mercado**. Si un shard no llega al corte dentro del budget, el frame no es elegible; los demás consumidores siguen. Coalescing y policy de corte se versionan/capturan.

`DataRequirements` fija máxima edad desde observación/check de book, edad de metadata/fees, clock uncertainty y skew entre assets; silence budget y edad desde último cambio son métricas separadas para no tratar automáticamente un mercado quieto como desconectado. En ausencia de criterio aprobado, live falla cerrado. Antes de emitir intent se revalida el frame y, antes de enviar, la lease de calidad/constraint revision; un cambio lo invalida y exige una nueva evaluación. Ni esto ni la firma limit price garantizan fills múltiples ni cancelan una race posterior al último check.

### M1.6 — Recorder, evidencia durable y replay

**Contrato de captura:** se registra cada frame entrante y respuesta REST relevante antes de publicar su efecto, más solicitudes públicas, subscription/control events, errores, clock samples, config/universe changes, admission/quality transitions y decisiones. Capturar el payload wire disponible sin transformaciones de negocio, acompañado por envelope versionado. Los bytes secretos de auth, cookies, headers HMAC y mensajes User WS auth se excluyen/redactan **antes** del journal; la redacción tiene versión y lista de campos. Payloads privados de cuenta tienen storage/ACL separados. El replay del dominio no depende de secretos ni de una firma reutilizable.

| Campo de envelope | Semántica |
|---|---|
| `capture_id`, `boot_id`, `capture_seq` | Identidad única del journal y orden total local asignado por un único admisor; no orden global Polymarket |
| `surface`, `connection_id`, `epoch`, `frame_ordinal`, `request_id` | Fuente, fencing y correlación; una respuesta REST conserva tiempos de inicio/fin de su request |
| `received_wall`, `received_mono_offset`, `source_time_raw`, `source_unit`, `source_time?` | Hora local vs fuente y precisión; source time puede faltar o ser inválido sin reemplazo silencioso |
| `schema_version`, `normalizer_version`, `config_revision`, `content_hash` | Interpretación reproducible y trazabilidad |
| `payload_bytes`, `redaction_policy`, `quality/control_kind` | Evidencia raw permitida o control explícito de pérdida/cambio |
| `segment_id`, `offset`, `length`, `checksum` | Ubicación y detección de escritura parcial/corrupción |

**Formato propuesto:** journal append-only de records length-prefixed con versión, envelope, bytes y CRC por record; segmentos acotados por bytes/tiempo, footer con rango/count/SHA-256 y enlace al hash previo. Un writer secuencial, batch/group commit configurable y `fsync` antes de avanzar `durable_seq`. Segmentos sellados se comprimen fuera del hot path y quedan inmutables, con checksum del contenido lógico y del comprimido. Rename/manifest y directorio se sincronizan al sellar. Checksums detectan corrupción; no prueban que el proveedor envió todo ni protegen contra un administrador malicioso que reescriba toda la cadena de hashes.

**Política por defecto: durable-before-publish.** Books/estrategias sólo consumen records hasta `durable_seq`. La cola entre socket y writer es acotada; si no puede admitir un frame, se revoca inmediatamente el estado elegible del epoch por una señal de seguridad fuera de la cola saturada, se corta/reconecta transporte y se crea discontinuidad. Si el disco impide persistirla, readiness cae y el siguiente arranque parte de un boot no cerrado con intervalo final desconocido. No se promete contar los mensajes perdidos antes de admisión. No liberar decisiones usando datos que sólo viven en RAM; no configurar “drop oldest” en evidencia L2.

**Crash:** escanear último segmento hasta el último record completo y checksum válido, preservar evidencia del sufijo inválido, recuperar manifest y watermarks; nada posterior a la frontera demostrable se considera capturado. Registros físicamente presentes después del último watermark publicado pueden conservarse como evidencia recuperada, pero no se afirma que hayan sido vistos por estrategias. Reinicio abre boot/epoch nuevos, marca intervalo entre última evidencia y nuevos snapshots como discontinuidad y reconcilia cuenta antes de live. Un crash puede perder frames en kernel/cola/no-fsync; el diseño hace esa pérdida visible, no imposible. Un fallo de NVMe/host puede perder todo lo no respaldado fuera de él.

**Dos productos de replay, sin conflación:**

1. **Replay de observación:** reconstruye reducers/books a partir de exactamente los records durables seleccionados, incluidos gaps, snapshots y cambios conocidos a cada `capture_seq`. Determinista para el mismo manifest, código, parámetros y seed; no reconstruye cotizaciones que no se capturaron ni valida orden remoto.
2. **Replay de decisiones entregadas:** además usa el journal de `DeliveryFrame{run_id, ordinal, trigger, cut_seq, revision_vector, quality, virtual_time}` y resultados/controles de runtime. Reproduce coalescing, skips y el input exacto de la estrategia. Un delivery sin resultado durable al crash queda `INCOMPLETE`; no se atribuye una decisión o efecto live por reejecutarlo.

El scheduler registra durablemente el descriptor del frame antes de invocarlo; luego registra resultado determinista/errores. Para recuperar un corte pasado se usan checkpoints derivados con offsets/checksum y journal, no un puntero a “latest”. El replay no carga credenciales ni puede enviar órdenes. El reloj virtual se mueve por el tiempo de delivery/recepción definido en el manifest; timers son eventos registrados/ordenados. Randomness sólo por seed inyectada, maps se serializan en orden canónico y reducers no dependen del scheduling Go. No se ordena por event-time para llenar huecos; una simulación alternativa con reordenamiento es otro experimento y otra versión de dataset.

**Manifest de experimento:** hashes/rangos de segmentos, coverage por stream/asset/epoch, holes, checkpoints, revisiones metadata/rules/fees/relationships y su disponibilidad temporal, normalizador, estrategia/binario/Go toolchain/dependencies, parámetros, seed, clocks, fill/cost/risk models, delivery policy, sample split y política de censura. Inputs posteriores al cutoff nunca rellenan retroactivamente metadata “conocida”. Dataset parcial permanece parcial; un estudio que cruza una discontinuidad termina ese episodio o lo etiqueta no evaluable según regla ex ante. Cada exclusión se cuenta en denominadores para evitar selección de sólo episodios limpios rentables.

### M1.7 — Persistencia, datasets, retención y recuperación

| Store propuesto | Qué guarda / owner | Garantía, índices y límites |
|---|---|---|
| SQLite embebido, WAL, synchronous FULL | Metadata versionada, registry/manifests, órdenes/intents/reservas/fills/ledger y checkpoints, vía owners | Transacción ACID local; writer serial con transacciones breves. Índices ID/protocol/account/status/event y known-at; raw stream no se inserta fila por fila aquí |
| Capture journal segmentado | Raw sanitizado y eventos de control/delivery; Capture | Append secuencial durable; índice reconstruible `(surface, asset/condition, receive-range, seq-range)→segment/offset`; el índice no es autoridad |
| Execution private store | Payload exacto preparado, order hash, intent, attempt y auth profile **sin claves**; Coordinator | Bytes de orden firmada cifrados en reposo como artefacto sensible; headers HMAC no se persisten. Escritura durable antes del intento; clave de cifrado externa a DB/backups |
| Parquet particionado | Datasets normalizados/episodios/metrics/scorecards, derivados de manifests | Partición por dataset/date/surface y rangos, evitando archivo por asset minúsculo; lineage y schema version. Dinero como decimal/int exacto, no float obligatorio |
| In-memory | Books, snapshots, caches, colas y runtimes | Reconstruibles; nunca única prueba de intent enviado, fill o saldo disponible |

**Justificación y reversibilidad:** SQLite evita servidor/operación adicional y permite atomicidad de cuenta en un host. El writer único puede convertirse en límite; analytics pesado no lee la base operacional durante transacciones críticas. PostgreSQL sería alternativa si profiling muestra contención, múltiples writers inevitables o consultas operativas incompatibles; no está descartado para siempre. Repositorios por owner y schemas de exportación lógicos aíslan el motor; una migración requerirá reconciliación y prueba de equivalencia, nunca doble escritura live sin diseño. Parquet y journal versionado permiten cambiar motor analítico sin alterar el dominio. La elección concreta de driver Go, librería decimal/Parquet y versions corresponde a selección técnica de M2 bajo estos contratos, no abre investigación de protocolo.

**Consistencia entre journal y DB:** no hay transacción atómica filesystem+SQLite. Capture sella primero evidencia; DB confirma proyección y `applied_seq` en una transacción. Al reiniciar, reprocesar desde `applied_seq+1` con dedup y claves únicas; segmentos durables huérfanos se indexan, referencias DB a evidencia ausente invalidan integridad. Las decisiones de cuenta viven primero en DB (reserva+intent+evento outbox en la misma transacción); su exportador al journal es idempotente por event ID. Nadie envía desde la outbox genérica: sólo Execution con estado/attempt autorizado. No exigir a ambos stores un “exactly once” distribuido ficticio.

**Retención propuesta para decisión del owner:** raw de mercado no pineado 30 días, datasets derivados no pineados 90 días, manifests/scorecards/config/rules/ledger de cuenta retenidos durante la vida del proyecto; segmentos necesarios para experimentos revisados quedan pineados hasta liberación explícita. Son defaults operativos propuestos, no SLA del exchange. GC sólo elimina segmentos sellados sin referencias después de backup verificable si la política lo exige; borrar un input pineado convierte el experimento en `NOT_REPRODUCIBLE`, nunca en resultado intacto. Capacidad mínima se estima con bytes/s medidos × ventana × overhead/backup, sin inventar volumen de mercado.

**Disco:** budgets separados para raw, DB, derivados y reserva operacional. Low-watermark frena replay/export y nuevas suscripciones; critical-watermark bloquea oportunidades/nuevos sends, mantiene reconciliación/cancel mientras sea posible y alerta. No borrar raw pineado para sostener live ni llenar el volumen hasta que SQLite falle. Tamaño/tiempo de segmento, batch fsync, headroom y retention son configuración validada y capturada.

**Migraciones:** schema version y compatibilidad explícitos, backup previo y writer detenido; transacción cuando sea posible. App antigua rechaza schema futuro; rollback restaura sólo bajo reconcile, porque restaurar DB vieja no deshace órdenes externas. Raw nunca se reescribe por migración; nuevo normalizador genera dataset nuevo.

**Backups:** snapshot consistente de SQLite por mecanismo de backup del motor (no copiar sólo `.db` ignorando WAL), más segmentos sellados, manifests/pins y key references; cifrado y copia a destino fuera del host como requisito para resiliencia ante pérdida física. No es otro nodo de ejecución. Snapshot registra fronteras DB/journal, outbox pendiente y hashes; restore valida esos vínculos, reproduce reducers y abre books nuevos. Propuesta inicial: snapshot DB horario, copia de segmentos al sellar y verificación diaria; RPO/RTO y destino pendientes owner, medidos mediante restore completo. Sin copia externa sólo se certifica crash recovery local, no recuperación ante pérdida del host.

### M1.8 — Contrato Go de estrategia y modos

Interfaces **de diseño**, deliberadamente sin implementación. El engine entrega todos los servicios comunes; la estrategia calcula elegibilidad, detecta oportunidades y evalúa su lógica particular. No recibe conexiones, repositorios, signer, wallet ni un callback de envío.

```go
type Strategy interface {
    Describe() Descriptor
    Universe() UniverseSpec
    RequiredData() DataRequirements
    Start(context.Context, RunContext) error
    Detect(context.Context, Frame) ([]Opportunity, error)
    Evaluate(context.Context, Opportunity, EvaluationContext) (Assessment, error)
    Observe(context.Context, Feedback) error
    Stop(context.Context, StopReason) error
}

type Factory interface {
    New(Parameters) (Strategy, error)
}

// Contratos conceptuales: todos los valores entregados son inmutables.
// RunContext: run/strategy IDs, versions, virtual clock, seeded RNG,
//             parameters, declared metric sink; sin acceso a red/secretos.
// Frame: delivery ordinal + cut seq + UniverseRevision + BookSnapshots +
//        RegimeSnapshots + RelationshipSnapshots + ExternalObservations + quality.
// EvaluationContext: mismo frame + DepthQuote/CostEnvelope + AccountView
//                    del modo + RiskPolicyView; nunca objetos mutables.
// Assessment: ACCEPT | REJECT | INCONCLUSIVE, reason codes, differentiated
//             metrics, bounded ActionCandidate y supuestos explícitos.
// Feedback: UniverseChanged | QualityChanged | EvaluationResult |
//           SimulatedExecution | LiveExecution | Timer | StopRequested.
```

`Descriptor` exige ID, versión de código/schema, hipótesis asociada, descripción de mecanismo y metric definitions. `UniverseSpec` y `DataRequirements` se validan antes de arrancar; una estrategia que requiere dato no disponible queda `WAITING_DATA/UNSUPPORTED`, no recibe campos cero sustitutos. `Start` se ejecuta una vez por instancia; `Observe(UniverseChanged)` permite incorporar/excluir miembros antes de `Detect` sobre esa revisión. `Detect` sólo produce candidatos no vinculantes; Economics construye cotizaciones y costes comunes; `Evaluate` aplica factibilidad/modelo particular sobre el mismo frame. Risk siempre revisa el resultado después. `Observe` recibe resultados posteriores sin convertirlos en prueba de fill si son simulados. `Stop` es idempotente desde la perspectiva del runtime y no coloca ni cancela órdenes.

`ActionCandidate` contiene una o varias legs tipadas de asset, side, limit/size o presupuesto, prioridad, vigencia, restricciones de parcialidad y máximo riesgo residual. Para acciones sobre posiciones sólo referencia capability y inputs tipados; no admite dirección arbitrary/calldata. Economics retorna quantities cuantizadas y coste por escenario. Una estrategia puede aportar payoff states/model outputs como datos auditables, nunca reemplazar el motor común de sizing o inventar conversiones habilitadas. Bounds de cardinalidad de oportunidades/legs/payloads impiden resultados ilimitados.

| Modo | Fuente / misma lógica Strategy | Destino y permiso |
|---|---|---|
| `SCREEN` | Datos actuales o dataset declarado, universe/Detect/Evaluate idénticos | Reporta candidatos/costes; no abre orden real ni simulada por defecto; no secrets |
| `REPLAY` | Manifest cerrado, reloj virtual, mismos reducers y estrategia | Simulator bajo optimistic/base/stress; cuenta virtual y resultados reproducibles; red bloqueada |
| `SHADOW` | Datos actuales capturados, reloj de delivery y misma estrategia | Simulator con órdenes/fills sintéticos y cuenta virtual compartida; cero envío venue |
| `LIVE` | Datos actuales y feedback de cuenta real | ExecutionMode comienza `LIVE_DISABLED`; sólo un lease central certificado habilita el gateway real; no estrategia “live especial” |

Factory crea instancias aisladas por experimento; no hot-load de plugins Go ni swaps de código sobre órdenes abiertas. Cada instancia procesa un callback a la vez. Estado propio sólo en su actor; reinicio conservador crea instancia nueva desde manifest y replay de inputs, o checkpoint versionado validado contra replay. No se promete que un checkpoint arbitrario escrito por la POC sea confiable. Para reproducibilidad no usar I/O, reloj global, goroutines propias, random global ni iteración de maps sin orden dentro de callbacks; se verifica en revisión/fixtures y comparación de replay.

**Errores y aislamiento realista:** error tipado distingue `NO_SIGNAL`, `INSUFFICIENT_DATA`, `INVALID_MODEL`, `TRANSIENT_INPUT` y fallo de software. Panic recuperable en callback → instancia `FAILED`, retiro de sus candidatos y política de cancel de sus remanentes a través del Coordinator; no se recupera balance inventándolo. Deadline cancela contexto; resultado tardío se descarta mediante run generation. **Go en un proceso no ofrece sandbox de memoria, bloqueo de syscalls ni kill seguro de goroutine**: estrategias son código confiable revisado. Si un callback ignora cancelación, no se inicia otro callback/instancia que acumule goroutines; se cerca la instancia, se revoca live y se reinicia el proceso de forma controlada si no drena. Si se requiere ejecutar código hostil o aislamiento físico fuerte, excede este baseline y vuelve a decisión del owner. Una API sin secretos evita acceso implícito, no constituye defensa contra código malicioso en el mismo proceso.

### M1.9 — Hypotheses, experimentos y simulación

Registry guarda `PE-xxx`, mecanismo, evidencia pro/contra, required data, universo/exclusiones, capacidad/lock/latency, experimento mínimo y parent revision. No convierte las 30 familias del ERC en 30 módulos. Cheap triage consulta catálogo/datos disponibles y cotización de costes antes de activar captura amplia: `NO_DATA` es bloqueo/inconclusión, `NO_SIGNAL` es evidencia sólo si coverage suficiente y `BAD_ECONOMICS` requiere modelo/coste explícitos.

| Artefacto lógico dentro del framework | Contenido mínimo |
|---|---|
| Protocol de experimento | Hipótesis falsable, estimando/unidad estadística, baseline/negative controls, exclusiones, stopping rule, sample requirement, GO/ITERATE/NO_GO ex ante |
| Run manifest | M1.6 + versiones parámetros/calculadores, universo conocido-a-fecha, escenarios, estado de datos, gastos de cómputo/humanos, bankroll virtual |
| Scorecard | Cobertura y discontinuidades; señales totales/independientes; lifetime; net edge por depth/fee/latency; fill/partial/legging rates; capacity; PnL bruto/neto/realizado/no realizado; lock/capital-turns; drawdown y worst loss; markouts/adverse selection; sensitivity y caveats |
| Statistical view | Separar calibración Brier/log-loss, retorno de regla y ponderación de flujo. Splits temporales y por parent event, OOS, censura por mercados sin resolver y múltiples tests declarados; no holdout reciclado sin nueva revisión |
| Outcome | `GO` al siguiente gate, no permiso live; `ITERATE` con cambio falsable; `NO_GO` con evidencia suficiente; `INCONCLUSIVE` cuando datos/modelo/sistema impiden concluir |

**Fill engine común:** órdenes virtuales con submit-time, delay, limit/policy, remanente, cancel-latency y fill events. BUY barre asks y SELL bids al tiempo simulado de llegada, integra niveles para VWAP y rechaza cantidad no cubierta; FOK exige total y FAK admite parcial. En snapshots discretos no se interpola liquidez no observada. Un book agregado no revela FIFO, prioridad individual ni nuestra queue: resting/touch no es fill probado. Last trade y BBO no bastan para asignar todos los fills. El modelo maker estima/boundea queue y fill usando evidencia disponible y declara su incertidumbre; no certifica price-time priority.

| Escenario | Liquidez/latencia/fills | Interpretación |
|---|---|---|
| Optimistic | Profundidad observada disponible, latencia baja parametrizada, queue favorable bajo evidencia mínima declarada | Cota exploratoria, nunca evidencia suficiente de promoción |
| Base | Delays/latencia medidos o supuestos explícitos, haircut de profundidad y queue conservadora calibrable, partials y cancel races | Resultado candidato sujeto a sensibilidad; si faltan datos de calibración se etiqueta `UNCALIBRATED` |
| Stress | Mayor delay, reducción de depth, adverse selection, patas incompletas, fallo de cancel, settlement/dispute lock prolongado y costes altos | Riesgo residual y fragilidad; magnitudes preregistradas por experimento, no constantes universales |

Cada run simulado posee un ledger de liquidez **virtual consumida** por asset/precio/versión y cuenta: dos estrategias no pueden reutilizar la misma profundidad en el mismo escenario como si ambas fueran primeras. Actualizaciones posteriores no prueban reposición causada por nosotros; regla de replenishment conservadora y sensibilidad se versionan. Replay histórico no modela fielmente impacto contrafactual del bot sobre el mercado ni reacción de competidores. Fills simulados, órdenes observadas y liquidaciones chain se etiquetan de forma inequívoca.

Baskets son multi-leg no atómicos: simular orden/tiempos de legs, partials, drawdown/lock intermedio y condiciones de abandono. Si la tesis exige conversión deshabilitada o atomicidad no disponible, su resultado queda `CONDITIONAL_UNEXECUTABLE`; puede falsarse económicamente, pero no obtener GO live. El motor provee ejecución/coste de legs y soporte de payoff tables; no implementa el payoff específico de Sports/NegRisk. `GO` exige que la conclusión sobreviva los supuestos aprobados y datos aptos, no un threshold global de ROI, número de trades o latencia inventado.
