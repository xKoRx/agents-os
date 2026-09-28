---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo Futures]]"
  - "[[Echo Futures — D1 Analysis Pack]]"
  - "[[Echo Futures — D2-04 Operation Order Fill Position]]"
  - "[[Echo Futures — D2-05 Instrument Session Provider]]"
  - "[[Echo Futures — D2-06 Market Runtime]]"
  - "[[Echo Futures — D2-07 Execution Runtime]]"
  - "[[Echo Futures — D2-08 Strategy Runtime]]"
  - "[[Echo Futures — D2-09 Blocking Refactors]]"
aliases:
  - Echo Futures Architecture Candidate V1
  - EF Architecture Candidate
  - EF D2 Integrated Architecture
tags:
  - kind/doc
  - area/echo
  - echo-futures
  - architecture-design
created: "2026-09-28"
updated: "2026-09-28"
---

# Echo Futures Architecture Candidate V1

## Propósito

**Autoridad de lectura primaria de D2.** Integra las decisiones congeladas de [[Echo Futures — D2-04 Operation Order Fill Position]], [[Echo Futures — D2-05 Instrument Session Provider]], [[Echo Futures — D2-06 Market Runtime]], [[Echo Futures — D2-07 Execution Runtime]], [[Echo Futures — D2-08 Strategy Runtime]] y [[Echo Futures — D2-09 Blocking Refactors]] sobre las decisiones owner [[Echo Futures]] D2-01/02/03 y la evidencia [[Echo Futures — D1 Analysis Pack]].

No copia los artifacts hijos: los integra. Ante contradicción de wording histórico, mandan los cierres congelados de cada workstream y este documento integra esa semántica vigente. No implementa código, no abre D3/Astra, no selecciona providers ni transports, no congela nombres físicos de topics/campos salvo donde la fuente ya lo hizo.

Baselines: vault `5af8e18f` (≥ `2c4bc4fd` close D2-08); Echo `xKoRx/echo@372af59a7b83604781346613da01e3d510ea1360` (fetch sin delta; spot-checks en D2-09 §2).

## 1. Executive architecture

```text
Market Sources (feed adapters, MARKET_DATA bindings)
  ↓  echo.market-feed-candidates.v1
Market Runtime                                   [D2-06]
  echo/market_stream        key stream_id        (authority/current/last-known/readiness)
  echo/market_analytics     key stream_id        (bars/MTF/grid)
  ↓  echo.market-events.v1  (canónico, AT_LEAST_ONCE + guards stream_seq)
Strategy Engine                                  [D2-08]
  echo/strategy_engine      key strategy_id      (1 evaluación por trigger admitido)
  ↓  echo.signals.v1        (EXACTLY_ONCE, 0..N Signals ordenadas)
Signal Fan-out                                   [D2-04/D2-08]
  echo/signal_fanout        key strategy_id      (target set linealizado; 1 Signal → N deliveries)
  ↓  SignalDelivery         (key op key)
Operation + MoneyManagement                      [D2-04/D2-08]
  echo/operation            key account:strategy (Operation/Orders/Fills/exposición/mm_state)
  echo/provider_rules       key account_id       (Stage-1 admission · Stage-2 caps · safety) [D2-05]
  ↓  Order command          (egress EXACTLY_ONCE M1)
  ↓  echo.order-commands.{execution_account_id}.v1  (candidate name)
Futures Bridge                                   [D2-07]
  proceso sibling · ExecutionAdapter interno · journal M2 write-ahead
  ↓
ExecutionAdapter  (SimExecutionAdapter primero; real = D6)
  ↓
Venue
```

Retorno (tres caminos congelados, por identidad de la observación):

```text
Venue → Adapter → Bridge
  ├─ OrderStatusEvent / OrderActionResult / Fill (correlacionados con Order Echo)
  │    → echo.execution-events.v1 (key op key) → echo/operation
  ├─ PositionUpdate  (execution_account_id + contract_id, SIN operation_id)
  │    → echo.position-observations.v1 (key account) → position/reconciliation
  └─ ExecutionSessionStatus (runtime/readiness account-scoped; naming físico = D6)
       → runtime/readiness path (jamás fact de Operation)
```

Proyecciones durables: `echo.operation-projections.v1` (OPERATION_SNAPSHOT / ORDER_SNAPSHOT / FILL_FACT, egress transaccional misma frontera de checkpoint) → `echo/operation_projector` → PG (query/eventual, nunca recovery authority).

## 2. Domain model (sólo lo frozen)

| Entidad | Identidad / notas |
|---|---|
| `Strategy` | `strategy_id`; account-agnostic; definición/config; 0..N Signals por evaluación. |
| `Signal` | `signal_id` determinística = f(run, strategy_id, strategy_eval_seq, signal_seq); intents `OPEN/REDUCE/CLOSE/CLOSE_ALL`; `entry_type MARKET/LIMIT/STOP`; SL/TP técnicos; `details`; `valid_until`; `source NATIVE/REFERENCE`. Sin sizing ni account/contract. |
| `AccountStrategy` | `Account + Strategy + MoneyManagement` + enabled; catálogo hot; máx 1 Operation no terminal. |
| `MoneyManagement` | Plugin de dominio dentro de `echo/operation`; `mm_state` duradero; autoridad de sizing/riesgo/exposición; triggers de Operation. |
| `Operation` | Aggregate account-specific; `operation_id` UUIDv7; dirección sellada por la Signal OPEN aceptada; `strategy_cycle_seq`; `contract_id` + specs económicas pinneados; máx 1 ciclo futuro diferido. |
| `Order` | Entity del aggregate; `order_id` = `client_order_id` UUIDv7 (idempotency key M2); `decision_id`; `replace_request_id`/`cancel_id`; `order_version`; `replaces_order_id`. |
| `Fill` | Hecho inmutable; identidad nativa `(execution_account_id, provider_execution_id)`; prohibida identidad sintética para correctness (D2-07-R1). |
| `Position` | Observación física neta `(account_id, contract_id)`; write-only desde venue; jamás dispara lifecycle. |
| `Instrument` | Económica/canónica: `instrument_id`, `quote_currency`, `exchange`, `product_group`, `calendar_ref` (obligatoria y resoluble en Futures). |
| `Contract` | Expiry-specific tradable; specs económicas (`tick_size`/`point_value`/`tick_value` derivado, qty rules); pinneado una vez por Operation. |
| `TradingSession` | `session_id = (calendar_id, session_date)`; ExchangeCalendar = datos + resolver puro IANA/tzdata; `NamedTradingWindow` por id. |
| `Provider` / `ProviderProgram` / `ProviderRuleSet` | Provider = policy owner (≠ transport); RuleSet versionado con provenance obligatoria; typed families, sin DSL. |
| `ProviderAccountBinding` | Config 1:1 de Account: provider/program/phase?/RuleSet authority + transport entitlement + DayBoundary explícito; re-binding in-place con audit facts. |

`Trade` no se congela (`DEFERRED_TO_THE_LAB`); V1 lleva `run_mode`/`run_id` en toda entidad (I11) para no cerrar la puerta. Sin `StrategyTrade`, `operation_key`, revisiones formales, event sourcing, portfolio aggregate.

## 3. Ownership matrix (mutable state)

| Estado | Owner (StateFun island) | Key |
|---|---|---|
| latest quote/trade + serving authority/readiness | `echo/market_stream` | `stream_id` |
| forming/closed bars + grid/rebuild | `echo/market_analytics` | `stream_id` |
| Strategy: estado técnico del ciclo, indicators, analytical readiness, timers, config efectiva, bookkeeping (`owner_input_seq`/`strategy_eval_seq`/`strategy_cycle_seq`, dedup triggers) | `echo/strategy_engine` | `strategy_id` |
| Signal fan-out: dedup `(strategy,signal,binding)`, target-set linearization | `echo/signal_fanout` | `strategy_id` |
| Operation: lifecycle, Orders, Fills, exposición lógica, `mm_state`, `operation_event_seq`, dedups, `current_operation_id`, ciclo diferido | `echo/operation` | `account_id:account_strategy_id` |
| Provider: admission state, RuleSet/binding/AccountState/risk, DayBoundary efectivo, `firm_by_operation` + `live_reservations`, routing index | `echo/provider_rules` | `account_id` |
| Journal M2 / submission registry | Futures Bridge / ExecutionAdapter (durability domain del side-effect owner, por binding) | — |
| Recovery authority | Checkpoints Flink/StateFun + replay Kafka ingress + egress transaccional | — |

Sin estado mutable cruzado entre islas: coordinación por mensajería checkpointeada idempotente; PG jamás participa de correctness.

## 4. Lifecycle summary

**Strategy cycle (lógico, no físico):** `TECHNICAL_CLOSED/OPEN(k)` gobernado por las propias Signals; `strategy_cycle_seq` monotónico; jamás espera convergencia física de cuentas; config nueva durante ciclo OPEN = `pending_strategy_config` para ciclo posterior.

**Operation:** `CREATED` → (MM emite entry Order que sale) `PENDING_ENTRY` → (primer Fill con exposición) `ACTIVE` → `TERMINAL{reason}`. Guards TERMINAL: exposición lógica firmada real = 0 ∧ 0 Orders vivas ∧ intent de terminación registrado. ForceClose = intent, no transición. La exposición deriva de Fills firmados sin clamp (breach = fail-visible `EXPOSURE_INVARIANT_BREACH`); direction immutable; reversal = terminal + nueva Operation del ciclo siguiente; máx 1 Operation no terminal por AccountStrategy; `CLOSE_ALL(k)→OPEN(k+1)` difiere como máximo un ciclo (`ACCOUNTSTRATEGY_CYCLE_LAG` si llega un segundo).

**Order:** `PENDING_SUBMIT → SUBMITTED → WORKING → FILLED | CANCELLED | EXPIRED | REJECTED`; partial fill = `WORKING` + `filled_qty`; modify nativo incrementa `order_version`; replace = cancel+new con cadena auditable; única corrección forward: `CANCELLED/EXPIRED → FILLED` por fills tardíos que la completan; un estado de Order jamás termina la Operation.

**Position observation:** ingress periódico por cuenta; shape neto `(account, contract)`; upsert/delete por batch ausente (completeness declarada); comparador periódico lógico-vs-físico → `POSITION_MISMATCH` fail-visible; sin auto-repair.

## 5. Market runtime

- **Identidad lógica:** `stream_id = (instrument_id, contract_id)`; `serving_authority {binding_id, members, authority_epoch, provenance}` separada de la identidad; source switch ≠ rollover (switch preserva Contract, incrementa epoch, barrier/rebuild; rollover es owner-manual prospectivo y crea demanda de otra stream).
- **Demanda:** `MarketDemand{operation_id, instrument_id, contract_id, ACQUIRE|RELEASE}` ∪ config demand; account count invisible.
- **Eventos:** QUOTE/TRADE canónicos con `event_ts` (semántica), `stream_seq` (orden/idempotencia per stream, cruza epochs), `authority_epoch`, provenance/recovery; clases de identidad A/B/C por capability — clase C sin dedup-safe identity no inventa identidad (fail-visible o rebuild).
- **Readiness en capas:** `EffectiveConsumerReadiness = StreamReadinessFor(input class) ∧ AnalyticalRequirementsReady(consumer)`; `WARMUP_INCOMPLETE` es estado analítico del consumidor, nunca feed-global; health separa liveness/continuity/freshness; CLOSED/BREAK del calendario hace el silencio esperado.
- **Current vs last-known:** monotónico por `(event_ts, stream_seq)` intra-epoch; epoch change demotea a last-known con provenance y seed-ea current nuevo vacío; availability ≠ READY; MM usa last-known sólo si su policy lo autoriza.
- **Bars:** `BarId=(stream_id,timeframe,bucket_open_utc)`; TRADE bars V1; grid anclado a session_open; breaks no desplazan; cierre por boundary event o `TimerFired`; sin synthetic empty bars; corrección tardía X→X' cambia la projection, **jamás** la decisión que observó X (sin Signal retrospectiva); cada timeframe agrega directo desde eventos canónicos (sin cascada).
- **Warm-up/recovery:** warm-up con eventos normalizados (no vendor bars); NORMAL RESTART restaura checkpoint (nunca re-decide con historia final corregida); switch/recovery con barrier + rebuild capability-driven; `ANALYTICAL_REBUILD_UNPROVABLE` fail-closed.

## 6. Strategy runtime

- Isla `echo/strategy_engine` (key `strategy_id`); serialización por key; **NO posee** cuentas/provider/MM state/Orders/Fills/Positions; cero feedback de ejecución.
- **Triggers declarativos sin DSL:** `StrategyTriggerRequirements{bar_close[], market_event NONE|QUOTE|TRADE, window_transitions[], session_transitions, timers[]}` alimenta MarketRequirements/readiness; bars-only no recibe firehose; transiciones de sesión vía `NextSessionTransition`; cambio de declaración = `ConfigTransition` material.
- **Evaluación:** una por trigger admitido (dedup por trigger identity) ⇒ 0..N Signals ordenadas (`signal_seq`; 0 es el caso común); egress `echo.signals.v1` EXACTLY_ONCE; crash pre-checkpoint ⇒ regeneración determinística del mismo `signal_id`.
- **Fan-out:** target set = catálogo AccountStrategy linealizado en la isla; enabled ⇒ todo; disabled ⇒ sin `OPEN` pero gestión de Operation viva sí; dedup triple (fan-out + `(account_strategy_id, signal_id)` + guards); entrega `SignalDelivery` mínima por op key sin copiar estado.

## 7. Provider runtime

- **Stage-1 (pre-materialización):** `AdmissionRequest → echo/provider_rules(account_id) → AdmissionResult{ALLOW|DENY_NEW_RISK}` — linearization point account-keyed compartido con RuleSet/binding/account/risk/DayBoundary updates; kache = prefilter solamente; DENY ⇒ `ProviderDecision` durable, sin Operation; `UNKNOWN` jamás es ALLOWED.
- **Stage-2 (post-MM, pre-egress):** PER_ORDER local + shared caps por reserva serializada (GROSS/NET_ABS/GROUP_WEIGHTED); guard de egress revalida epoch del grant (`ReservationRevalidate`); `PENDING_FINALITY` es reservation state, no Order.status; finality venue-authoritative libera.
- **Capacity:** `firm_by_operation` + `live_reservations`; **todo** Fill Echo (ENTRY/ADD/REDUCE/EXIT/safety/late) emite `CapacityStateUpdate` cumulativo firmado con `operation_event_seq` (idempotente en replay); sin portfolio aggregate.
- **Safety:** asíncrono por intents; `ProviderForceClose` fan-out determinístico sobre el routing index completo (incluye disabled/close-only con Operation viva); key sin Operation = no-op; entitlement revocado ⇒ deny new risk + suspensión + operador, **sin** flatten automático; salidas (REDUCE/EXIT/CLOSE) jamás se bloquean.

## 8. Execution runtime

- **Topología:** Core → Kafka (`echo.order-commands.{execution_account_id}.v1`, candidate name; account-isolated routing; sin transport branching en Core) → **Futures Bridge** (proceso sibling; shell runtime: config/sesiones per-account/consumers/telemetría) → **ExecutionAdapter** (componente interno transport-specific) → Venue.
- **M1:** StateFun state + egress transaccional EXACTLY_ONCE — consistencia state↔command publication; **no** cubre el venue.
- **M2:** comando ↔ side effect físico: journal durable write-ahead (`PREPARED/SUBMITTING/VENUE_BOUND/TERMINAL/AMBIGUOUS`) antes del point-of-no-return; `client_order_id` estable; reconciliación autoritativa por client identity/history o idempotencia nativa; **no blind retry**; `AMBIGUOUS` fail-closed; Kafka offset/Core PG/process memory jamás physical truth; transport/order-class sin capacidad ⇒ `UNSUPPORTED_FOR_V1_EXACT_SUBMISSION` (gated).
- **Correlación:** adapter-owned (submission registry); execution facts llegan ya correlacionados; eventos no correlacionables van a observación, jamás fabrican Operation.
- **Readiness/reconnect:** static eligibility (D2-05) ≠ dynamic readiness (7 dimensiones); `EXECUTION_READY_NEW_RISK` sólo tras barrier completa; reconnect = recovery, nunca resubmit; Orders vivas pinneadas al binding físico original; ForceClose con edge down = pending + reconcile-first; sin synthetic close ni emergency switch.
- **Ownership:** una side-effect authority por `(execution account, physical binding)`; **NO AUTOMATIC CROSS-HOST TAKEOVER**; fail-closed antes que falso HA; `1 Bridge → N accounts` o `1 → 1` según transport; cinco identidades separadas (bridge/adapter/session/execution account/provider external account).
- **Implementación:** `SimExecutionAdapter` primero (ejercita el seam y el journal/recovery real sin credenciales); transport externo real = selección/certificación **D6** (OD-D2-07-1 cerrada); `Domain SimExecution` (backtest) ≠ `SimExecutionAdapter` (seam).

## 9. Config semantics (hot vs pinned)

| Clase | Elementos |
|---|---|
| PINNED / SNAPSHOTTED | `Operation.contract_id` + specs económicas embebidas; `direction`; config MM efectiva del snapshot; snapshots Calendar/RuleSet/DayBoundary inyectados en runs históricos; Strategy `active_cycle_config` del ciclo activo. |
| DYNAMIC / HOT | InstrumentMapping por binding; ProviderRuleSet; ProviderAccountBinding; AccountState; ExchangeCalendar live; DayBoundary efectivo; routing catalog; Strategy config prospectiva (`pending_strategy_config` al ciclo siguiente); trigger declarations (= ConfigTransition material). |
| READ MODEL / OPTIMIZATION | kache/admission snapshot: prefilter + observabilidad, **nunca** linearization authority. |
| PROVENANCE-ONLY | `decision_id`s, epochs, hashes/snapshots de run, audit facts. |

Regla transversal: hot update afecta materializaciones/ciclos **futuros**; lo vivo conserva su snapshot; la única autoridad sobre Operations vivas es provider gates/safety plane — nunca mutación implícita. Toda config capaz de cambiar una decisión vive en el initial manifest o como `ConfigTransition` ordenada (sin hot change silencioso).

## 10. LIVE / EXACT_REPLAY / BACKTEST

```text
Misma lógica de dominio pura en los tres modos
(sin Kafka/StateFun/PG/wall clock; DomainClock runtime_ts inyectado)
```

- **LIVE:** islas StateFun + config hot + inputs reales; serialización `owner_input_seq` per-island.
- **EXACT_REPLAY:** reproduce el run live real: initial RunManifest inmutable + ReplayAnchor (warm-up corpus exacto, capturado desde t0 — OD-C1 `ALWAYS_ON_V1_SELECTED_STREAMS`) + DeterministicInputLog (TimerFired admitidos, ConfigTransitions, barriers, transiciones, market refs, deliveries cross-island) + contenido canónico + mismo código ⇒ **mismas decisiones market-dependent y mismos `signal_id`**. No toca venue; no sustituye recovery live; falla visible (`REPLAY_ANCHOR_MISSING/INVALID`, `REPLAY_LOG_CORRUPT`), nunca replay parcial silencioso. Alcance V1: boundary de mercado — el dominio de ejecución no se re-ejecuta (D2-04 R12; identidades de ejecución fuera del boundary, D2-09 §4).
- **BACKTEST:** run histórico **nuevo**: `MarketHistorySource` + canonical synthesis order + runtime clock sintético + snapshots explícitos de Calendar/RuleSet/DayBoundary/Contract + `SimExecution` determinístico. No se llama "replay".

Propiedad de dominio congelada: mismo stream ordenado de inputs admitidos ⇒ mismas decisiones (MM/Strategy); cantidades derivadas de hechos son conmutativas.

## 11. Persistence

| Categoría | Contenido |
|---|---|
| CHECKPOINTED (hot recovery authority) | estado de todas las islas (market/strategy/fanout/operation/provider), dedup sets, `mm_state`, secuencias, timers+generations |
| DURABLE (frontera transaccional) | comandos por cuenta (egress EXACTLY_ONCE); facts/projections `echo.operation-projections.v1` (misma frontera de checkpoint); journal determinístico de mercado |
| RECORDED | initial manifest + ReplayAnchor + DeterministicInputLog + canonical content (horizonte declarado) |
| PROJECTION (query/eventual) | PG: `operations`/`orders`/`fills`/`contract_positions` via projector idempotente/stale-safe; `trade_journal`/`canonical_operations` (boundary analítico intacto) |
| READ MODEL | topics compactados (stream state, bars, calendars, catálogos) + kache |
| EXTERNAL AUTHORITY | venue (ejecución física, positions, finality); PG **jamás** reconstruye `mm_state` ni decide Orders; cold disaster ⇒ `COLD_RECOVERY_REQUIRED` fail-closed |

Sin event sourcing global, sin tablas de eventos, sin saga; historia de transiciones = Kafka/OTel.

## 12. Scale — 1 Strategy × 200 Accounts

```text
1 stream / 1 builder set / 1 indicator set / 1 evaluación / 1 Signal
  ⇒ 1 fan-out ⇒ 200 deliveries (key op key)
  ⇒ ≤200 decisiones MM aisladas (sólo triggers declarados)
  ⇒ ≤200 execution sessions según transport (topic per-account)
```

- **NO multiplicado por cuenta:** feed, bars, indicators, evaluación, market analytics.
- **N por naturaleza (legítimo):** decisiones MM (el riesgo es N); notificaciones de mercado opt-in hacia op keys subscriptas; sesiones/journals de ejecución por cuenta/binding.
- Cost drivers: feed = streams×rate; bars = streams×timeframes×rate; Strategy = strategies×triggers; fan-out = signals×bindings; MM = operations×triggers declarados.
- Capacidad física (100–200 cuentas, throughput, reconnect storm, journal I/O) = certificación **D6**; la topología no impide el scale estructuralmente.

## 13. Reuse / refactor map (output Q16 — ver [[Echo Futures — D2-09 Blocking Refactors]] §16)

```text
REUSE:  StateFun runtime/module.yaml/kache/compact topics · SendAfter→DomainClock ·
        OTel/ETCD conventions · symbol-mapping hot pattern · snapshot KVS joins ·
        CloseHandler safety plane · sdk/mm calculators (unit-agnostic) ·
        trade_journal boundary · v3/sdk/* en el Bridge sibling ·
        account-isolated session/consumer/breaker patterns
ADAPT:  MMEngineFn patterns→echo/operation · ExecutionPlannerFn pattern→signal_fanout ·
        DayBoundary mechanism→hot config provider_rules · Bridge patterns→sibling ·
        consumer read_committed/commit-tras-outcome
REPLACE (path Futures):  ExecutionStore authority · PendingMM/PendingPlanning ·
        PositionSnapshot ticket-shape · prop_rulesets shape · ExecutionResult single-result ·
        journal EA post-side-effect · fallback UTC 23:00
NEW (V1): domain package puro · echo/{operation,signal_fanout,operation_projector,
        strategy_engine,market_stream,market_analytics,provider_rules} · DomainClock ·
        MarketHistorySource · ReplayDriver+recording · catálogos Instrument/Contract/
        Calendar · provider domain · Futures Bridge + ExecutionAdapter +
        SimExecutionAdapter + journal M2 · adapter ReferenceEvent→Signal · PG migrations
LEGACY_ONLY: ReferenceEvent/CoreCommand/ExecutionResult/CloseResult/ExecutionPolicy ·
        Bridge MT/pipes/EA · pip_size.go · DayBoundaryCache legacy · trade_journal content
D6:     EXACTLY_ONCE config · transport real M2/entitlement · benchmarks ·
        ReplayDriver golden · journal store · retentions
DEFERRED (Iteración 2): DT-EF-REFERENCE-SIGNAL-03 · DT-EF-FX-PROP-01 · pips cleanup ·
        DT-EF-CROSS-MARKET-INSTRUMENT-02 · DT-EF-POSITION-RECONCILIATION-05 ·
        recording archival/midpoint/distributed/depth
BLOCKING_ARCHITECTURE: NONE · CORE REWRITE: NOT_REQUIRED
```

## 14. D5/D6 obligations

**D5 — Foundations (construir):** superficies NEW sobre los patrones REUSE/ADAPT congelados; `module.yaml` con egress `EXACTLY_ONCE` (transaction timeout ≤ `transaction.max.timeout.ms`) y consumers `read_committed`; producer idempotente in-flight limitado; domain package puro (boundary Q14); migraciones PG + projector; retention del topic de proyecciones; suite de regresión con los casos de aceptación A–L/A–T de D2-04..08.

**D6 — Multi-Prop E2E + Scale (certificar):** selección del primer transport externo real con acceso autorizado efectivo + implementación de su adapter + gates M2 del transport (customTag retention, ambiguous-submit atomicity, negative/recovery semantics, execution identity, history horizon) + entitlement/host; certificación física de la config EXACTLY_ONCE/read_committed; benchmarks (100–200 cuentas, throughput StateFun/tick, reconnect storm, journal I/O, latencia admission/reservation); ReplayDriver con golden recording; store del journal con fsync/corruption semantics; retentions + lag del projector; E2E shadow/demo/sim autorizado. El requisito V1 de transport real y la capacidad 200-account se pagan aquí.

## 15. Deferred debt (sólo deuda explícita)

`DT-EF-REFERENCE-SIGNAL-03` (migración reference path, Iteración 2 mandatoria) · `DT-EF-FX-PROP-01` (provider rules Forex) · limpieza pips legacy (ID/alcance pendiente ratificación owner; absorbe `DT-EF-UNITS-04`) · `DT-EF-CROSS-MARKET-INSTRUMENT-02` · `DT-EF-POSITION-RECONCILIATION-05` (edge case, reabrir con evidencia) · recording archival/replay-midpoint/distributed replay/depth-book · cleanup legacy V1/V2 y retiro de compatibility paths · nota de migración de identidades si el replay de ejecución se extiende (D2-09 §4.2).

Ninguna deuda bloquea V1; ninguna capacidad V1 depende silenciosamente de piezas legacy incompatibles.

## 16. Q GATE TABLE

```text
Q2  Position attribution      CLOSED (D2-04)
Q3  Order lifecycle           CLOSED (D2-04)
Q4  Market hot state          CLOSED (D2-06)
Q5  Bar semantics             CLOSED (D2-06)
Q6  Contract mapping          CLOSED (D2-05)
Q7  Session semantics         CLOSED (D2-05)
Q8  Feed authority            CLOSED (D2-06)
Q9  Execution transport       CLOSED (D2-07; OD-D2-07-1 = defer a D6)
Q10 Provider model            CLOSED (D2-05)
Q11 Strategy runtime          CLOSED (D2-08)
Q14 Backtest boundary         CLOSED (D2-06/D2-04 §8.7)
Q15 Trade/Lab                 DEFERRED_TO_THE_LAB_BY_OWNER
Q16 Blocking refactor         CLOSED (D2-09)
Q12 S2 / Q13 Gerard           → D4 (fuera del D2 gate por diseño del roadmap)
```

`OWNER_DECISIONS_REQUIRED = NONE`. Todas las owner decisions D2 están cerradas: D2-01/02/03 (OWNER_CLOSED), OD-C1 (`ALWAYS_ON_V1_SELECTED_STREAMS`), OD-D2-07-1 (`DEFER_EXTERNAL_TRANSPORT_SELECTION_TO_D6`).

```text
EF_D2_DESIGN_PASS = READY_FOR_MANAGER_REVIEW
```

Primary Manager decide el gate; este documento no se declara PASS ni cierra D2.

## Fuentes

- [[Echo Futures]] — decisiones owner y cierres D2-04..08 + rollout D6.
- [[Echo Futures — D2-04 Operation Order Fill Position]] · [[Echo Futures — D2-05 Instrument Session Provider]] · [[Echo Futures — D2-06 Market Runtime]] · [[Echo Futures — D2-07 Execution Runtime]] · [[Echo Futures — D2-08 Strategy Runtime]] — autoridades integradas (children A/B/C = evidence depth).
- [[Echo Futures — D2-09 Blocking Refactors]] — Q16, auditoría de identidades, matriz de clasificación.
- [[Echo Futures — D1 Analysis Pack]] — evidencia D1 aceptada.
- `xKoRx/echo@372af59a7b83604781346613da01e3d510ea1360` — baseline físico.
