# Echo Futures — D5 Implementation Shots

## 1. Purpose

This document slices the accepted D4 candidate architecture into bounded implementation workstreams for D5.

It is **not** a schedule, estimate or authorization to start D5. The Primary Manager must first complete D4 final QA.

Rules for every shot:

- implement only frozen contracts;
- prefer additive slices;
- produce acceptance evidence before downstream shots depend on the slice;
- do not redesign accepted domain behavior inside implementation;
- do not select/certify a real external execution transport in D5;
- preserve existing Echo legacy paths unless the shot explicitly adapts a frozen seam.

---

## 2. Dependency overview

```text
D5-S01  Pure domain + config contracts
   ├── D5-S02  Canonical market identity / deterministic recording foundation
   │      └── D5-S03  Bars / readiness / MarketContext
   │             └── D5-S04  Generic Strategy runtime + Signal fan-out
   │                    ├── D5-S05  S1 exact
   │                    └── D5-S06  S2 exact
   │
   ├── D5-S07  Operation / Order / Fill / local executable exposure
   │      ├── D5-S08  Provider admission + reservations + final revalidation
   │      └── D5-S09  GerardMM V1
   │
   └── D5-S10  Futures Bridge sibling + SimExecution + M1/M2 seam

D5-S04 + S07 + S08 + S09 + S10
   └── D5-S11  End-to-end runtime integration / projectors / recovery / observability

D5-S02 + S03 + S04 + S05/S06 + S07/S09/S10
   └── D5-S12  Exact replay + backtest acceptance harness / D5 closure evidence
```

This graph expresses contract dependencies, not calendar sequencing.

---

## 3. D5-S01 — Pure domain and configuration contracts

### Purpose

Create the minimum shared types/pure domain packages required by all later shots without introducing runtime owners.

### Dependencies

None beyond frozen D4/D2 documents.

### Expected source surface

Primarily:

- `v3/sdk/domain` or narrowly scoped Futures domain packages;
- pure `sdk/calendar` / time-resolution package already frozen by D2;
- pure execution/market/Strategy/MM contract packages where needed;
- Gateway/config DTOs only where contract serialization must be established;
- no StateFun function implementation beyond compile-time contract fixtures.

Expected contract surfaces include:

- Instrument / Contract / ContractIdentifier / InstrumentMapping;
- ExchangeCalendar / NamedTradingWindow / WindowContext;
- Provider / ProviderProgram / ProviderRuleSet / ProviderAccountBinding;
- Signal / SignalDelivery identities;
- Operation / Order / Fill / Position contract types;
- canonical exact quantity/money/tick units;
- DomainClock interface contract;
- run provenance;
- ProviderDecision / reservation/revalidation messages;
- normalized execution observation contracts.

### Contracts implemented

- Technical SPEC identity vocabulary.
- Instrument/Contract canonical separation.
- `calendar_ref` fail-closed representation.
- native Fill identity requirements.
- exact quantity/money types.
- no Strategy profit-target field for S1/S2 Gerard path.

### Acceptance evidence

At minimum:

- serialization round-trip fixtures;
- deterministic ID fixtures;
- quantity/tick/money validation;
- calendar DST/session pure tests;
- compile-time separation showing Strategy contract does not require account/provider types for technical evaluation;
- ATP CAL-01..04 contract subset;
- ATP S1-13 and S2-09 schema assertions.

### Parallelizability

Can be split internally by pure-domain package, but one reviewer should keep naming/identity semantics coherent.

### Must NOT redesign

- no generic entity/version framework;
- no provider DSL;
- no Strategy DSL;
- no generic event-sourcing envelope;
- no cross-market ontology;
- no dynamic plugin framework.

---

## 4. D5-S02 — Canonical market identity + deterministic recording foundation

### Purpose

Implement D4-A1's market identity/order foundation and the frozen deterministic run/control recording primitives required by exact replay.

### Dependencies

D5-S01.

### Expected source surface

- new/extended market Stream StateFun function under `v3/core/internal/functions`;
- market canonical ingress/topic contracts;
- StateFun ValueSpecs for per-stream state;
- runtime module/topic configuration;
- deterministic run journal/manifests;
- DomainClock LIVE/virtual plumbing that is needed at owner boundaries;
- existing Kafka/statefun SDK patterns.

### Contracts implemented

- `stream_id=(instrument_id,contract_id)`;
- source identity classes without content-dedup;
- `canonical_event_id != stream_seq`;
- durable per-stream canonical ordering;
- authority epochs/source-switch barrier;
- canonical downstream redelivery guards;
- run manifest / ReplayAnchor capture for selected/demanded streams;
- deterministic owner input ordering/control records;
- ordered material timers/config/session/recovery transitions.

### Acceptance evidence

ATP:

- MKT-01..08;
- MKT-13 where foundation-level possible;
- MKT-14 control/timer primitive;
- REC-04 provenance isolation;
- failure injection around checkpoint/egress.

Evidence must explicitly demonstrate that one sequence position cannot silently identify two canonical facts.

### Parallelizability

Can run in parallel with D5-S07 after S01. D5-S03 depends on it.

### Must NOT redesign

- no global market sequencer;
- no content-hash trade identity;
- no giant market snapshot;
- no global event store;
- no account-keyed market stream;
- no automatic rollover during source switch.

---

## 5. D5-S03 — Market analytics, bars, readiness and MarketContext

### Purpose

Implement shared bars/hot analytical state, readiness layering and exact decision-critical read capture/replay interface.

### Dependencies

D5-S01, D5-S02.

### Expected source surface

- `echo/market_analytics` StateFun function;
- bar/indicator pure packages;
- market bars/readiness compacted views;
- calendar/window resolver integration;
- MarketContext LIVE and recorded/replay implementations;
- bounded warm-up/history seam.

### Contracts implemented

- shared per-stream bar ownership;
- timer/session-based close;
- session-grid/break semantics;
- no synthetic empty bars;
- late projection correction without retroactive decision mutation;
- feed readiness vs analytical readiness;
- stale last-known != READY;
- `context_reads[]` capture of only consumed reads;
- repeated logical read memoization;
- EXACT_REPLAY context resolver that never falls back to current state.

### Acceptance evidence

ATP:

- MKT-09..16;
- calendar acceptance cases;
- warm-up/readiness component cases;
- replay missing-read failure;
- bounded-state/resource assertions from Performance Budgets.

### Parallelizability

Can be developed while D5-S07/S08/S10 progress. Blocks generic Strategy runtime.

### Must NOT redesign

- no `DecisionObservation`;
- no `BarObservation`;
- no Strategy-owned duplicate bars;
- no global atomic multi-stream snapshot;
- no per-account analytics;
- no “closed bars never correct” shortcut that rewrites replay semantics.

---

## 6. D5-S04 — Generic Strategy runtime + Signal fan-out

### Purpose

Implement one reusable Strategy execution shell and account fan-out without embedding S1/S2 rules in infrastructure.

### Dependencies

D5-S01, D5-S03.

### Expected source surface

- `echo/strategy_engine` StateFun function;
- Strategy pure interface/contract package;
- Strategy config/readiness cache integration;
- `echo/signal_fanout` StateFun function;
- Signal transactional egress;
- AccountStrategy config cache/read models.

### Contracts implemented

- per-strategy technical owner;
- natural trigger ordering/dedup;
- `strategy_eval_seq`, `signal_seq`, deterministic `signal_id`;
- finite technical-cycle ownership;
- MarketContext injection/capture;
- 0..N ordered Signals;
- immutable Signal fan-out;
- no technical recomputation per account;
- disabled-binding behavior/final local guard seam;
- bounded cycle-lag behavior only.

### Acceptance evidence

ATP:

- SIG-01..04;
- SCL-01 structural assertion with N=200;
- Strategy runtime crash/redelivery tests;
- no duplicate technical evaluation after Signal redelivery;
- no account multiplication of bars/indicators.

### Parallelizability

After generic runtime compiles, S1 and S2 can be implemented in parallel as independent pure Strategy modules.

### Must NOT redesign

- no per-account Strategy instances;
- no Strategy DSL;
- no account/MM/provider state in Strategy;
- no arbitrary Signal/cycle queue;
- no workflow engine.

---

## 7. D5-S05 — S1 exact Strategy

### Purpose

Implement exactly the frozen `NY Opening Range Breakout 30m` technical Strategy.

### Dependencies

D5-S01, D5-S03, D5-S04.

### Expected source surface

- S1 pure Strategy module/package;
- S1 typed config;
- Strategy runtime registration/wiring;
- S1 deterministic fixtures.

### Contracts implemented

- NQ;
- canonical 5m bars;
- canonical TRADE breakout;
- NY_OPEN 09:30–10:00 ET authority;
- required `premarket_window_id`;
- exact OR construction;
- strict crossing;
- LONG/SHORT technical stop from closed bars premarket-start -> previous closed 5m bar;
- forming candle excluded;
- technical OPEN/CLOSE_ALL;
- exact re-arm/day reset;
- no profit target.

### Acceptance evidence

ATP S1-01..13.

Include fixtures proving the premarket start comes from config and no literal fallback hour exists.

### Parallelizability

Parallel with D5-S06 after S04.

### Must NOT redesign

- no hardcoded premarket start;
- no discretionary breakout interpretation;
- no price target;
- no forming-bar stop input;
- no Strategy-side sizing.

---

## 8. D5-S06 — S2 exact Strategy

### Purpose

Implement exactly the frozen `H4 Trend / 5m Bollinger Pullback` Strategy.

### Dependencies

D5-S01, D5-S03, D5-S04.

### Expected source surface

- S2 pure Strategy module/package;
- H4/5m indicator state;
- Strategy runtime registration/wiring;
- deterministic fixtures.

### Contracts implemented

- exact H4 SMA50 trend semantics;
- frozen same-boundary visibility;
- 5m Bollinger 20 / 2.0 / population stddev;
- exact LONG/SHORT pullback state machine;
- trigger-bar technical stop;
- Bollinger basis as technical CLOSE_ALL lifecycle condition only;
- trend invalidation close;
- re-arm;
- no Gerard/fixed profit target.

### Acceptance evidence

ATP S2-01..09.

### Parallelizability

Parallel with D5-S05.

### Must NOT redesign

- no basis-as-profit-target;
- no new indicator framework;
- no look-ahead;
- no Strategy money objective.

---

## 9. D5-S07 — Operation / Order / Fill + local executable exposure

### Purpose

Implement the canonical account-strategy aggregate and D4-A2 local direction-safety foundation before adding provider or Gerard-specific economics.

### Dependencies

D5-S01.

### Expected source surface

- new/adapted `echo/operation` StateFun owner;
- pure Operation/Order/Fill transition package;
- operation facts/projection egress;
- Position/reconciliation event ingress contracts;
- exact local claim/`q_exec_max` logic;
- pending Stage-1 admission local state seam.

### Contracts implemented

- one non-terminal Operation per AccountStrategy;
- immutable direction;
- Contract/spec pin;
- Fill-derived logical exposure;
- Order 1 -> 0..N Fill;
- native Fill dedup identity;
- terminal guards;
- ForceClose as intent;
- one nullable `pending_admission?`;
- CLOSE/CLOSE_ALL invalidation;
- OPEN(k+1) supersession;
- per-Order `q_exec_max`;
- local reducible-exposure claims;
- concurrent REDUCE/EXIT/ForceClose non-inversion;
- modify/cancel/replace local executable semantics;
- no Position attribution.

### Acceptance evidence

ATP:

- ADM local lifecycle subset;
- EXP-01..08;
- TERM-01,02,04,05;
- partial Fill and late Fill domain tests;
- restart/checkpoint aggregate tests;
- bounded-state budget assertions.

### Parallelizability

Can start after S01 in parallel with market work. Provider admission/reservations and GerardMM consume its seams.

### Must NOT redesign

- no legacy one-trade aggregate reuse by deformation;
- no synthetic Fill;
- no Position-derived Operation;
- no reversal-in-place;
- no WIND_DOWN;
- no generic liquidation override;
- no `max_admissible_qty`;
- no silent resize.

---

## 10. D5-S08 — Provider admission, capacity reservation and final revalidation

### Purpose

Implement D4-A3 plus D4-A2 account-wide provider safety as one authoritative account-keyed plane.

### Dependencies

D5-S01, D5-S07. Calendar/Account snapshot config dependencies may use S03 surfaces where needed, but market Strategy runtime is not required.

### Expected source surface

- `echo/provider_rules` StateFun owner;
- ProviderRuleSet/binding config distribution/cache;
- account snapshot/day-boundary ingestion;
- provider admission decision egress;
- admission request/result messages;
- reservation/grant/revalidation messages;
- account-wide firm/reserved executable-capacity state.

### Contracts implemented

- Stage-1 authoritative OPEN admission;
- provider binding/program/phase/entitlement authority;
- typed provider risk/window state;
- GROSS / NET_ABS / GROUP_WEIGHTED capacity;
- exact reservation;
- Fill reservation -> firm transfer;
- modify/replace reservation semantics;
- physical Position trust guard;
- **mandatory every-grant `ReservationRevalidate`**;
- `egress_authorized` one-shot provider authorization;
- authority update invalidating old grant before M1;
- complete RuleSet available read-only to MM context;
- provider ForceClose intents;
- provider runtime not a second MM.

### Acceptance evidence

ATP:

- ADM-01..05;
- PRV-01..11;
- provider half of EXP modify/replace tests;
- provider hot-update race tests;
- ForceClose fan-out/safety tests;
- concurrency tests with multiple AccountStrategies on same account.

### Parallelizability

After S07 seam, can proceed in parallel with S09 implementation if S09 uses a fake/provider context interface until integration.

### Must NOT redesign

- no local final-revalidation shortcut;
- no `egress_committed` name/semantics;
- no provider-specific MM;
- no silent quantity resize;
- no generic liquidation rule;
- no aggregate/service for pending admission;
- no saga.

---

## 11. D5-S09 — GerardMM V1

### Purpose

Implement the frozen monetary hardscalping MoneyManagement policy as an Operation-local plugin.

### Dependencies

D5-S01, D5-S07; consumes the provider context/seams of S08 and MarketContext of S03 for full integration.

### Expected source surface

- GerardMM pure package under the MM domain;
- typed GerardMM config;
- Operation invocation adapter;
- MM state serialization;
- pure economic formulas/quantity candidates;
- protective Order decision logic.

### Contracts implemented

- evaluation day 1/day 2 SL=2000, TP=1500 USD;
- funded schema with required explicit values;
- fail-closed missing economic plan;
- `account_day_current_pnl_money` account-wide authority for both SL and TP;
- Owner remaining-loss formula;
- remaining profit-objective formula;
- provider hard monetary min;
- dynamic derived target mark;
- initial exact sizing;
- protective stop monotonicity;
- bounded adverse/favorable mutually exclusive branches;
- exact quantities;
- partial Fill consumes accepted add attempt/no top-up;
- profit termination precedence;
- no portfolio reconstruction;
- no inter-Operation martingale.

### Acceptance evidence

ATP MM-01..18 plus integration with S08 deny/revalidation cases.

Property tests should cover money/tick/quantity edge cases and branch bounds.

### Parallelizability

Pure GerardMM can develop after S07 alongside S08. Full integration waits for S03/S08 contracts.

### Must NOT redesign

- no Strategy target price;
- no realized-only TP authority;
- no other-Operation scan;
- no unlimited progression;
- no auto-clipped quantities;
- no provider enforcement state inside MM;
- no research thresholds as LIVE defaults.

---

## 12. D5-S10 — Futures Bridge sibling + SimExecution + M1/M2 seam

### Purpose

Implement the physical execution boundary without choosing a real vendor transport.

### Dependencies

D5-S01 and stable Order/command contracts from S07. Provider final authorization from S08 is required before full Core command integration.

### Expected source surface

- sibling Futures Bridge process (conceptual D2 name `v3/futures-bridge`; exact package naming may follow repo conventions);
- existing `v3/sdk` messaging/telemetry/kache/DI reuse;
- per-account session/consumer implementation;
- generic ExecutionAdapter contract;
- `SimExecutionAdapter`;
- durable M2 journal interface plus a D5-capable local implementation suitable for simulation/failure tests;
- normalized execution event producer;
- Core M1 egress/topic wiring;
- StateFun module/Kafka delivery-semantics configuration.

### Contracts implemented

- `echo.order-commands.{account}.v1` or the final frozen-equivalent routing;
- M1 transactional state -> command boundary;
- Bridge shell vs adapter separation;
- M2 journal `PREPARED -> SUBMITTING -> VENUE_BOUND/TERMINAL/AMBIGUOUS`;
- write-ahead before simulated point-of-no-return;
- no blind retry;
- stable `client_order_id`;
- normalized five execution-event families;
- reconnect/reconciliation barrier;
- Position observations;
- no automatic cross-host takeover;
- SimExecution fault scenarios.

### Acceptance evidence

ATP EXE-01..13 and TERM-03 with SimExecution.

Failure injection must include crash after simulated physical side effect and before ACK/offset to prove duplicate submit suppression.

D5 evidence here is architecture/Sim certification, **not** real vendor M2 certification.

### Parallelizability

Bridge shell/Sim can progress while S08/S09 mature if command payload stays behind the frozen contract. Final Core integration waits for S08 provider authorization and S07 Order lifecycle.

### Must NOT redesign

- no real ProjectX/CQG/etc adapter selection;
- no transport branching in Core;
- no extension/deformation of MT Bridge;
- no generic bridge framework/plugin runtime;
- no automatic HA/takeover;
- no “Kafka offset = physical exactly once” claim;
- no heuristic Fill IDs.

---

## 13. D5-S11 — End-to-end runtime integration, projection, recovery and observability

### Purpose

Wire the implemented owners into one complete SimExecution runtime path and make correctness observable/recoverable.

### Dependencies

D5-S02, S03, S04, at least one Strategy S05/S06, S07, S08, S09, S10.

### Expected source surface

- StateFun module routing/ingress/egress definitions;
- Kafka topics/config;
- Gateway config distribution handlers/kache additions;
- PostgreSQL migrations/projection writers for new domain query surfaces;
- OTel metrics/traces/logs;
- recovery hooks/failure-injection harness;
- existing backoffice/query surfaces only where necessary to inspect evidence.

### Contracts implemented

Complete:

```text
market
-> bars/context
-> Strategy
-> Signal
-> fan-out
-> pending admission
-> Operation
-> GerardMM
-> provider exact authorization
-> M1
-> Futures Bridge
-> SimExecution
-> normalized Fill/Position
-> Operation convergence
-> projection
```

Projection remains non-authoritative.

Required measurement timestamps/counters from Performance Budgets are wired here.

### Acceptance evidence

- one full S1 Sim path;
- one full S2 Sim path;
- partial Fill;
- provider deny;
- provider stale-grant invalidation;
- technical CLOSE_ALL;
- account-day target exit;
- ForceClose;
- bridge restart;
- Core restart;
- unknown manual Position;
- 200-account structural fan-out;
- projection redelivery/catch-up;
- no PROD/real-money path.

### Parallelizability

Projection/observability work can begin from stable fact contracts before all E2E features land, but final shot is an integration gate.

### Must NOT redesign

- no UI-driven authority;
- no PG recovery authority;
- no observability-as-correctness;
- no bypass around owner functions “for E2E convenience”.

---

## 14. D5-S12 — Exact replay + backtest harness integration and D5 closure evidence

### Purpose

Prove the same Strategy/MM/domain logic can run under deterministic replay/backtest boundaries and assemble evidence required before D6 certification.

### Dependencies

D5-S02, S03, S04, S05/S06, S07, S09 and execution simulation contract from S10. Full provider integration is required for replay cases involving provider decisions.

### Expected source surface

- ReplayDriver/in-process deterministic harness;
- virtual DomainClock;
- ReplayAnchor/journal readers;
- MarketContext recorded-read resolver;
- historical-run adapters;
- pure SimExecution contract reuse for backtest;
- golden fixtures;
- acceptance-report tooling.

### Contracts implemented

- EXACT_REPLAY from ordered inputs + ReplayAnchor + `context_reads[]`;
- no current-state fallback;
- late correction chronology preserved;
- same Strategy/MM pure logic;
- BACKTEST as a new deterministic historical run, not fake live replay;
- run provenance isolation;
- exact decision-comparison output.

### Acceptance evidence

ATP:

- MKT-10..13;
- REC-04;
- S1/S2 golden deterministic outputs;
- GerardMM same-input/same-decision;
- 100% compared decision identity/semantic equality for the chosen golden exact-replay corpus;
- missing/corrupt recording fails visibly.

### Parallelizability

Harness foundations can start after S02/S03. Final golden closure waits for integrated Strategy/MM/runtime behavior.

### Must NOT redesign

- no separate “backtest Strategy implementation”;
- no reconstruction from today's bars in EXACT_REPLAY;
- no decision snapshot entity;
- no execution event-sourcing rewrite;
- no tolerance-based claim for exact replay correctness.

---

## 15. Cross-shot review gates

Every shot review must answer:

1. Which frozen contract does this source change implement?
2. Which runtime owner mutates the new state?
3. Is the state bounded?
4. What is its stable identity/dedup key?
5. What happens on redelivery/restart?
6. Does any new-risk path fail closed when correctness is unknown?
7. Does the change add an abstraction not required by V1?
8. Which ATP case proves the behavior?
9. Which performance measurement point/budget is affected?
10. Did the shot accidentally move provider/MM/Strategy/physical-execution authority?

A shot is not complete with “tests pass” if its relevant adversarial ATP cases are missing.

---

## 16. Parallel execution map

Safe parallelism after D5-S01:

```text
Market lane:
  S02 -> S03 -> S04 -> {S05, S06}

Account/domain lane:
  S07 -> {S08, S09}

Execution lane:
  S10 can build Bridge/Sim shell from S01/S07 contracts,
  then integrate S08 M1 authorization when available

Closure:
  S11 integrates all lanes
  S12 consumes market/runtime foundations early and closes with full golden evidence
```

Shared contract changes across lanes require rebase/review against S01 rather than duplicating DTOs/types.

---

## 17. D5 stop conditions

D5 implementation must stop/escalate to Manager review rather than invent behavior if any of these are discovered:

- frozen documents genuinely contradict on current authority;
- S1 cannot compute exact stop from the defined closed-bar interval;
- S2 basis lifecycle cannot be represented without adding a profit-target semantic;
- account-day PnL authority does not provide the frozen account-wide current value;
- provider exact revalidation cannot be placed before M1 without another owner;
- q_exec/provider-capacity model cannot represent a physical adapter action;
- a chosen D5 source surface forces Position attribution to Operation;
- SimExecution reveals M1/M2 contract ambiguity;
- exact replay requires an unrecorded decision-critical read;
- an implementation would require any explicitly rejected KISS/YAGNI concept.

This is a request for architecture clarification, not permission to locally “fix” the contract.

---

## 18. Explicitly deferred beyond D5

D5 does not select/certify:

- ProjectX direct;
- CQG;
- NinjaTrader;
- Tradovate;
- Rithmic;
- real-money provider entitlement;
- physical host placement for a selected vendor;
- production M2 journal technology certification;
- automatic HA/takeover;
- 100–200 account physical performance certification.

Those are D6/operational certification topics after the generic V1 implementation exists.

---

## 19. D5 completion evidence package

Before the Primary Manager can consider D5 complete, implementation should be able to produce one evidence index containing:

- commit/build IDs;
- shot -> source-surface mapping;
- shot -> ATP case results;
- exact domain/config fixtures;
- failure-injection results;
- deterministic replay golden comparison;
- SimExecution M1/M2 duplicate-suppression evidence;
- provider stale-grant revalidation evidence;
- S1/S2 exact fixtures;
- GerardMM day1/day2/funded-fail-closed fixtures;
- 200-account structural fan-out evidence;
- known D6-only measurements/certification gaps.

No D5 shot may convert a D6 measurement/certification gap into an assumed PASS.
