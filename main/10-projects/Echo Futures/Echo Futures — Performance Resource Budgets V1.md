# Echo Futures — Performance Resource Budgets V1

## 1. Purpose

This document freezes the V1 performance/resource **architecture budgets** required to detect structural failure during D5/D6.

It does **not** fabricate benchmark results or unsupported latency SLOs.

Two classes are used:

- **HARD ACCEPTANCE BUDGET** — an architectural bound/invariant that implementation must satisfy.
- **MEASUREMENT REQUIRED IN D6** — a quantity that must be benchmarked before physical certification because existing authorities do not justify an exact numeric threshold yet.

Primary architecture scale target:

```text
100–200 accounts without architectural redesign
```

The fundamental topology budget is:

```text
1 Strategy market evaluation
  -> 1 Signal
  -> N account deliveries
  -> N account-local MM/provider/execution decisions
```

Market subscriptions, bar construction, shared analytical state and Strategy indicators must not multiply by account count.

---

## 2. Budget philosophy

Performance correctness for V1 means:

1. no accidental `market_work × accounts`;
2. no unbounded state growth hidden inside keyed owners;
3. no synchronous remote I/O in decision hot paths where the architecture already provides local/checkpointed/read-model state;
4. no throughput optimization that weakens identity, replay, capacity or M2 correctness;
5. 100–200 accounts remain a capacity/certification problem, not a reason to redesign domain boundaries.

Latency numbers not supported by authorities are measured in D6 rather than invented in D4.

---

## 3. Scale envelope

### HARD ACCEPTANCE BUDGET — account scale topology

The implementation must be able to instantiate and exercise **200 AccountStrategy deliveries from one Strategy Signal without architectural changes**.

For one Strategy evaluation and one resulting Signal delivered to `N <= 200` eligible bindings:

```text
Strategy evaluations          = 1
Signal objects emitted        = 1
shared indicator evaluations  = 1 per Strategy evaluation path
market subscriptions          independent of N
bar construction              independent of N
account deliveries            <= N
MM invocations                <= N
provider account decisions    account-scoped as required
physical account actions      account-scoped as required
```

A solution that creates one Strategy instance, one market feed, one bar builder or one indicator graph per account **fails** this budget.

### MEASUREMENT REQUIRED IN D6

Measure at 100 and 200 accounts:

- steady-state CPU;
- peak CPU during fan-out;
- RSS/heap;
- StateFun mailbox/backpressure metrics;
- Kafka producer/consumer lag;
- provider owner queueing;
- command topic/consumer overhead;
- bridge session/journal overhead;
- reconnect storm behavior.

No exact CPU/RAM limit is frozen here because current authorities provide topology but not measured physical capacity.

---

## 4. Bounded-state budgets

### 4.1 Market state

**HARD ACCEPTANCE BUDGET**

Market hot state must be bounded by declared active streams/timeframes/lookbacks and current recovery needs, not by:

- number of accounts;
- total run duration;
- total historical market corpus.

Bar/indicator retention in hot state is bounded to what active MarketRequirements need plus implementation-local bounded bookkeeping justified by recovery/dedup.

No unbounded all-history in keyed StateFun state.

### 4.2 Strategy state

**HARD ACCEPTANCE BUDGET**

Per `strategy_id`, hot state is bounded by:

- finite Strategy state;
- required indicator lookback;
- active/pending Strategy config allowed by the frozen cycle rules;
- timer generations;
- monotonic counters/high-watermarks;
- bounded dedup/order bookkeeping.

It must not grow with account count.

### 4.3 AccountStrategy / Operation state

**HARD ACCEPTANCE BUDGET**

Per `account_id:account_strategy_id`:

```text
non-terminal Operations                  <= 1
pending_admission                        <= 1
accepted future-cycle deferred OPEN      <= frozen one-cycle behavior
active hardscalping branch               <= 1
bounded add attempts                     <= configured finite maximum
```

No arbitrary cycle backlog, workflow history or event-store log may accumulate in hot state.

### 4.4 Provider state

**HARD ACCEPTANCE BUDGET**

Per account, provider hot state may scale with:

- current firm attributable exposure;
- currently outstanding executable reservations/grants;
- current typed provider-rule state;
- live routing/safety references needed for affected Operations.

Released/final reservations must not remain as an unbounded in-memory history.

### 4.5 M2 journal

**HARD ACCEPTANCE BUDGET**

The Bridge journal must retain all non-terminal/ambiguous physical intents required for correctness.

It must never GC `AMBIGUOUS` merely to stay small.

Terminal records may be compacted/tombstoned only after the frozen redelivery/recovery/history-horizon safety conditions are met.

### MEASUREMENT REQUIRED IN D6

Measure:

- bytes per active Order/action;
- terminal tombstone bytes;
- journal write amplification;
- disk growth under representative order rate;
- compaction behavior;
- recovery scan time.

---

## 5. Hot-path I/O budget

### HARD ACCEPTANCE BUDGET

The following decision paths must not require synchronous PostgreSQL/Hasura/vendor-history I/O for every decision:

- canonical market normalization;
- bar construction;
- Strategy evaluation;
- Signal fan-out;
- Operation/MM decision;
- provider reservation/revalidation.

They use keyed/checkpointed state and local read models/config caches according to the frozen architecture.

External network I/O is naturally allowed only at actual external boundaries such as physical execution/reconciliation and configured market adapters.

A design that performs a DB query per tick, per Strategy evaluation or per MM decision fails this budget.

---

## 6. Market ingestion budget

### HARD ACCEPTANCE BUDGET

Canonical market ingestion work is proportional to accepted market events and active logical streams, not account count.

Per accepted physical/canonical input, identity/order bookkeeping must remain bounded and must not scan unbounded event history.

Content-based whole-history dedup is prohibited both for correctness and resource reasons.

### MEASUREMENT REQUIRED IN D6

For representative selected Futures streams, record:

- ingress events/s sustained and burst;
- p50/p95/p99 canonicalization latency;
- CPU/event;
- bytes/event;
- Kafka lag;
- recovery catch-up rate;
- effect of authority switch/recovery bursts.

No hard events/s number is frozen until measured against the selected feed/runtime.

---

## 7. Bar construction budget

### HARD ACCEPTANCE BUDGET

One logical stream/timeframe bar builder serves all consumers requiring that shared bar surface.

Bar close is timer/session driven and must not require scanning all retained history.

MTF work scales with demanded timeframes, not accounts.

### MEASUREMENT REQUIRED IN D6

Measure:

- event-to-bar-update latency;
- boundary timer close latency;
- correction processing cost;
- hot-state bytes per stream/timeframe;
- warm-up/rebuild time for S1/S2 requirements.

---

## 8. Strategy evaluation budget

### HARD ACCEPTANCE BUDGET

A Strategy is evaluated once for each admitted Strategy trigger, regardless of number of AccountStrategies bound to it.

Indicator computation remains Strategy/market scoped.

One Strategy cannot execute account-specific MM or provider logic before Signal fan-out.

### MEASUREMENT REQUIRED IN D6

Per S1 and S2, measure:

- p50/p95/p99 evaluation latency by trigger type;
- CPU/evaluation;
- indicator-state bytes;
- warm-up time;
- impact of simultaneous Strategy triggers.

No hard millisecond SLO is invented in D4.

---

## 9. Signal fan-out budget

### HARD ACCEPTANCE BUDGET

Fan-out cost is `O(N eligible AccountStrategies)` for a Signal and performs no Strategy recomputation.

For `N=200`, a structural acceptance test must show:

- one source Signal;
- no duplicate target delivery;
- bounded per-delivery bookkeeping;
- no market/indicator state copy per account.

Fan-out must not hold an unbounded retry queue outside the runtime's normal delivery/recovery mechanisms.

### MEASUREMENT REQUIRED IN D6

At N = 50, 100, 200, measure:

- Signal-to-last-delivery latency;
- p50/p95/p99 per-delivery dispatch latency;
- CPU/Signal;
- allocation rate;
- mailbox/Kafka backpressure;
- behavior under config churn.

---

## 10. Operation / MoneyManagement budget

### HARD ACCEPTANCE BUDGET

Operation/MM invocation is account-local and serialized by the Operation owner key.

GerardMM may inspect bounded Operation/Order/Fill state, Account snapshot and read-only ProviderRuleSet/context. It must not scan all Operations in the account to reconstruct account-day PnL; it consumes the authoritative account-wide PnL input.

Decision cost must not grow with historical account lifetime.

### MEASUREMENT REQUIRED IN D6

Measure:

- SignalDelivery-to-MM-decision latency;
- execution-event-to-MM-decision latency;
- CPU/invocation;
- allocations/invocation;
- state bytes per live Operation;
- effects of partial-fill bursts.

---

## 11. Provider admission/reservation/revalidation budget

### HARD ACCEPTANCE BUDGET

`echo/provider_rules(account_id)` is the single serialized authority for that account.

Correctness has priority over eliminating the internal hop.

Every not-yet-egressed exact shared-cap grant must traverse final `ReservationRevalidate`; no performance shortcut may bypass it.

Provider state and calculations must remain account-scoped and bounded by current firm/outstanding executable state, not historical decisions.

### MEASUREMENT REQUIRED IN D6

Measure separately:

- Stage-1 admission latency;
- reservation request latency;
- final revalidation latency;
- account-owner queue depth;
- throughput during concurrent AccountStrategies;
- worst case at 100–200 accounts;
- effect of hot RuleSet updates.

No latency SLO is frozen before measurements exist.

---

## 12. Core -> Bridge command path budget

### HARD ACCEPTANCE BUDGET

M1 correctness is non-negotiable:

```text
committed Operation state
<-> transactional command visibility
```

Latency optimization must not replace EXACTLY_ONCE/read-committed semantics with weaker delivery.

The Bridge must consume without turning Kafka redelivery into physical retry.

### MEASUREMENT REQUIRED IN D6

Measure timestamps at:

1. Operation command authorized;
2. M1 transaction visible;
3. Bridge consumer receives command;
4. M2 journal PREPARED durable;
5. M2 journal SUBMITTING durable;
6. first physical adapter call;
7. first authoritative Order/Fill observation returned.

Report p50/p95/p99 for each segment and end-to-end.

For SimExecution, this measures platform overhead. For the selected real adapter, D6 separates network/vendor latency.

---

## 13. M2 journal write budget

### HARD ACCEPTANCE BUDGET

Before physical point-of-no-return:

```text
full physical intent durable first
side effect second
```

No batching/async optimization may acknowledge durability before the store's actual durability contract is satisfied.

Crash tests must demonstrate zero blind duplicate physical submits across the certified failure window.

### MEASUREMENT REQUIRED IN D6

After selecting journal technology, measure:

- durable write p50/p95/p99;
- fsync semantics;
- throughput under representative concurrent accounts;
- restart/open time;
- corruption behavior;
- disk pressure;
- effect on submit latency.

---

## 14. Reconciliation budget

### HARD ACCEPTANCE BUDGET

Reconnect/restart performs reconciliation before enabling new risk.

It must process all non-terminal/ambiguous journal entries and required physical state; it may be throttled/rate-limited but cannot skip unresolved entries merely to meet a startup target.

### MEASUREMENT REQUIRED IN D6

For representative 100–200-account scenarios measure:

- time to authenticate/bind;
- journal scan time;
- open-order reconciliation time;
- execution-history recovery time;
- Position refresh time;
- time-to-`EXECUTION_READY_NEW_RISK`;
- provider API/rate-limit pressure;
- reconnect storm peak CPU/RAM/network.

A numeric recovery SLA is not frozen until a real transport is selected.

---

## 15. EXACT_REPLAY budget

### HARD ACCEPTANCE BUDGET — correctness

For a certified golden run:

```text
recorded ordered inputs
+ ReplayAnchor
+ exact context_reads[]
+ same code/config
=> same decision identities and semantic decisions
```

Required exactness is 100% for compared decision outputs within the golden corpus. A mismatch is correctness failure, not an allowed tolerance.

Replay must not multiply recording/state by account count when the inputs are shared market/Strategy inputs.

### MEASUREMENT REQUIRED IN D6 — speed/resources

Measure:

- replay events/s;
- replay duration / recorded-duration ratio;
- CPU/RAM;
- journal read bandwidth;
- ContextRead resolution overhead;
- replay anchor load time.

No “must be faster than real time” requirement is supported yet.

---

## 16. Recording/retention budget

### HARD ACCEPTANCE BUDGET

Always-on V1 recording is scoped to selected/demanded streams and material deterministic control inputs, not the entire provider market universe.

Recording resource usage scales with:

- selected market streams/content retention;
- material owner control inputs;
- Strategy ordering/context reads;
- configured retention horizon.

It does not create one market recording per account.

If required content/anchor is purged, replay fails visibly; the system must not pretend exact replay remains possible.

### MEASUREMENT REQUIRED IN D6

Measure representative daily:

- canonical market bytes/stream;
- deterministic journal bytes;
- ContextRead bytes/decision;
- ReplayAnchor bytes/run;
- retention disk requirement for chosen horizon.

Retention duration remains operational policy unless separately frozen.

---

## 17. PostgreSQL projection budget

### HARD ACCEPTANCE BUDGET

PG is asynchronous projection/query state, not a synchronous correctness dependency in the hot decision path.

Projectors must be:

- idempotent;
- stale-safe by operation/event sequencing;
- batchable where useful;
- independently catch-up capable.

Trading correctness must not stall merely because a query/UI projection is behind, unless a separate explicit authority dependency says otherwise.

### MEASUREMENT REQUIRED IN D6

Measure:

- fact-to-projection lag;
- sustained writes/s;
- batch size/cost;
- catch-up after outage;
- DB storage growth.

---

## 18. Kafka/topic budget

### HARD ACCEPTANCE BUDGET

Current V1 routing may retain per-account command topics/consumers because it preserves the frozen bridge pattern and boundary.

This is accepted only while it remains operationally viable for the 100–200 account target.

Changing later to shared partitioned topics keyed by account is allowed as a local routing optimization if it preserves contracts; it is not an architecture redesign.

### MEASUREMENT REQUIRED IN D6

At 100 and 200 accounts measure:

- topic/partition/consumer-group count;
- broker metadata overhead;
- rebalance behavior;
- bridge startup time;
- consumer memory/file descriptors;
- command lag.

If this physical model becomes the bottleneck, optimize routing without moving domain ownership.

---

## 19. Failure/backpressure budgets

### HARD ACCEPTANCE BUDGET

Backpressure may delay work but must not cause:

- duplicate Strategy evaluation;
- duplicate Signal delivery effect;
- grant revalidation bypass;
- command visibility without committed state;
- physical blind retry;
- silent market-event loss;
- silent provider state loss;
- unbounded in-memory retry queues.

When correctness evidence becomes stale due to delay, new risk must fail closed according to the relevant readiness contract.

### MEASUREMENT REQUIRED IN D6

Inject sustained pressure and measure:

- mailbox depths;
- Kafka lag;
- memory growth;
- recovery after pressure removal;
- staleness-driven deny rates;
- whether bounded state returns to baseline.

---

## 20. Observability measurement points

Every implementation must expose timestamps/counters sufficient to measure, at minimum:

1. physical market receive;
2. canonical market admission;
3. canonical market publication;
4. bar update and BAR_CLOSE;
5. Strategy trigger admitted;
6. Strategy evaluation complete;
7. Signal published;
8. fan-out delivery emitted;
9. Operation delivery admitted;
10. MM decision complete;
11. provider admission request/result;
12. reservation request/result;
13. final ReservationRevalidate request/result;
14. M1 command authorized;
15. M1 command visible;
16. Bridge command consumed;
17. M2 PREPARED durable;
18. M2 SUBMITTING durable;
19. physical submit call;
20. Order/Fill observation received;
21. normalized execution event ingested by Core;
22. reconciliation start/end;
23. replay input/context read/decision comparison.

Observability must not become correctness authority.

---

## 21. Architectural failure indicators

Any of these is a V1 budget failure requiring repair before certification:

- market subscriptions/bar builders/Strategy indicators scale linearly with account count;
- keyed hot state grows with run duration without an explicit bounded retention reason;
- Strategy evaluation occurs per account;
- GerardMM reconstructs account portfolio PnL by scanning Operations;
- provider rules use unbounded historical reservation logs in hot state;
- synchronous PG query appears in tick/Strategy/MM/provider decision loops;
- final provider revalidation is skipped to reduce latency;
- M2 write-ahead is weakened/batched beyond its durability contract;
- recording duplicates shared market streams per account;
- exact replay uses current state because recording was “too expensive”;
- correctness queues grow without bound under backpressure;
- 200-account structural test requires changing owner boundaries.

---

## 22. D6 benchmark report minimum

D6 must publish a reproducible benchmark/certification record including:

```text
hardware/runtime versions
commit/build IDs
Kafka/Flink/StateFun configuration
selected stream/Strategy set
account counts tested
input rate/load shape
order/reconciliation load shape
test duration
p50/p95/p99 per measurement point
CPU/RAM/disk/network
Kafka/state backpressure
journal durability settings
replay correctness result
replay throughput/resource result
reconnect/recovery result
all failures/unknowns
```

No benchmark from a different topology may be silently used as proof for V1.

---

## 23. Final classification

### HARD ACCEPTANCE BUDGETS

- 100–200 account topology without market/Strategy work multiplying by account.
- Bounded hot state by active domain need, not history duration.
- one non-terminal Operation and one pending admission per AccountStrategy owner.
- no synchronous DB I/O in decision hot paths.
- final provider revalidation always traversed.
- M1 transactional correctness preserved.
- M2 durable intent before side effect.
- zero blind physical retry under ambiguity.
- EXACT_REPLAY golden decision equality = exact, not statistical.
- recording shared by selected streams/Strategies, not accounts.

### MEASUREMENT REQUIRED IN D6

Exact numeric budgets for:

- market throughput/latency;
- bar latency;
- Strategy latency;
- fan-out latency;
- MM/provider latency;
- Core->Bridge->adapter latency;
- M2 durable-write cost;
- reconciliation time;
- CPU/RAM/disk/network;
- Kafka consumer/topic overhead;
- replay speed;
- recording/storage volume.

These measurements must become certification evidence before V1 physical scale is claimed.
