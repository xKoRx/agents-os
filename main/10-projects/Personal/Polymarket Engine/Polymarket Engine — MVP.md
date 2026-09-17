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
