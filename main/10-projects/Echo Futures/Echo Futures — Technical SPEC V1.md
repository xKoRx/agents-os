# Echo Futures — Technical SPEC V1

## 1. Purpose and normative scope

This SPEC freezes the implementation-facing V1 contracts, ownership, identities, ordering and failure boundaries required to implement Echo Futures without inventing domain behavior.

Normative precedence:

1. Architecture Candidate V2.
2. Accepted D4 corrections A1/A2/A3 and B1/B2/B3.
3. D2 integrated contracts where not superseded.

This is a contract document, not source code and not an implementation framework.

---

## 2. Runtime topology and keys

| Runtime surface | Key / partition identity | Mutable authority |
|---|---|---|
| `echo/market_stream` | `stream_id = instrument_id:contract_id` | canonical market stream, serving authority, ordering/readiness |
| `echo/market_analytics` | `stream_id` | bars/shared analytical state |
| `echo/strategy_engine` | `strategy_id` | technical Strategy state/indicators/readiness |
| `echo/signal_fanout` | `strategy_id` | target-set linearization + fan-out bookkeeping |
| `echo/operation` | `account_id:account_strategy_id` | Operation/Order/MM/pending admission/local executable claims |
| `echo/provider_rules` | `account_id` | authoritative provider admission/reservations/capacity/safety |
| Futures Bridge | execution account + physical binding | M2 journal/session/reconciliation |

No V1 component may introduce another mutable authority for these concerns.

---

## 3. Core identifiers

### 3.1 Market

```text
stream_id
  = (instrument_id, contract_id)

source_event_identity
  = source-native stable identity where available
    OR source packet/message sequence + deterministic entry position
    OR absent when the source cannot provide dedup-safe identity

canonical_event_id
  = deterministic identity of the accepted canonical fact

stream_seq
  = monotonic durable order position within stream_id

authority_epoch
  = serving-authority epoch for the same logical stream
```

Hard invariant:

```text
canonical_event_id != stream_seq
```

The sequence is never treated as semantic event identity.

### 3.2 Strategy / Signal

```text
strategy_eval_identity
  = (strategy_id, trigger_identity, strategy_eval_seq)

signal_id
  = deterministic(run identity, strategy_id, strategy_eval_seq, signal_seq)

strategy_cycle_seq
  = monotonic technical cycle number within strategy_id
```

### 3.3 Account delivery

```text
operation_owner_key
  = account_id:account_strategy_id

SignalDelivery dedup
  = (account_strategy_id, signal_id)
```

### 3.4 Operation / physical execution

```text
operation_id
order_id == client_order_id
provider_execution_id
cancel_id
replace_request_id
provider reservation/grant request_id
pending admission request_id
```

Order/action IDs are stable across redelivery/restart.

Fill canonical identity uses native physical identity, normally:

```text
(execution_account_id, provider_execution_id)
```

No price/time/qty hash or local sequence may replace missing native execution identity for exact V1 execution.

---

## 4. Market ingress and canonicalization

### 4.1 Durable per-stream input order

Every market input that can affect canonicalization must be admitted into one durable order per `stream_id` before mutating canonical stream state.

Physical implementation may use keyed Kafka ingress or an equivalent ordering mechanism, but it must prove:

- all material inputs for one logical stream share one durable order;
- no concurrent owner can assign conflicting sequence positions;
- replay/redelivery cannot create a second canonical fact from the same accepted physical identity.

No global sequence across streams is required.

### 4.2 Canonical MarketEvent contract

Minimum contract-level shape:

```text
CanonicalMarketEvent {
  stream_id
  canonical_event_id
  stream_seq
  instrument_id
  contract_id
  event_type             QUOTE | TRADE
  event_ts
  authority_epoch
  source_provenance {
    source_id
    source_event_identity?
    recovery_provenance
  }
  payload
  content_digest
}
```

`receive_ts` may exist for telemetry/liveness but is not domain event-time.

### 4.3 Conflict semantics

- same `stream_id + stream_seq + canonical_event_id + digest` redelivery => no-op;
- same `stream_seq` with a different canonical fact/digest => `MARKET_IDENTITY_CONFLICT`, fail-visible;
- a source-native stable identity mapped to two incompatible canonical facts => identity conflict;
- no content-based trade dedup is allowed where the source lacks native identity.

---

## 5. Market authority epochs and current state

A source switch retains the same `stream_id` and increments `authority_epoch`.

On an epoch transition:

- previous current market state is demoted to last-known with prior epoch/as-of/stale metadata;
- current-state ladders for the new epoch start empty;
- the first valid new-epoch observation seeds current state;
- `stream_seq` itself does not reset.

Readiness remains independent of last-known availability.

---

## 6. Bars and analytical state

### 6.1 Bar identity

```text
BarId = (stream_id, timeframe, bucket_open)
```

A closed bar also has revision/version provenance and the canonical source sequence up to which it was derived.

### 6.2 State owner

`echo/market_analytics(stream_id)` owns:

- forming bar state;
- bounded closed-bar rings required by declared market requirements;
- session grid state;
- last-applied stream-sequence guards;
- analytical reconstruction state.

Strategies do not own duplicate shared bars.

### 6.3 Session boundaries

Bar bucketing uses `Instrument.calendar_ref -> ExchangeCalendar`.

Buckets:

- never cross session open/close or internal break boundaries;
- close on timer/boundary, not on “next tick”;
- do not fabricate empty bars;
- use one session grid anchored to session open across internal breaks.

Late correction may revise bar projection but not previous decisions.

---

## 7. DomainClock and ordered control inputs

All domain timers use `DomainClock`.

LIVE implementation must expose monotonic runtime time per keyed owner. EXACT_REPLAY/BACKTEST use deterministic virtual time.

Material timer firings, session/window transitions, recovery barriers and material config transitions participate in the owner's deterministic admitted input order.

Domain code must not use wall clock directly for decision semantics.

---

## 8. MarketContext contract

### 8.1 Read-only decision context

Strategy and MM decisions consume shared market state through a read-only `MarketContext`.

A logical read key must identify the requested decision input, for example:

- current quote/trade for a stream;
- exact closed BarId/version;
- bounded bar range;
- stream readiness version;
- calendar/window resolved transition;
- other frozen decision-critical market view already authorized by the Strategy/MM contract.

### 8.2 LIVE read capture

For every logical read actually consumed by a decision:

```text
ContextRead {
  read_ordinal
  logical_read_key
  observed_version
  inline_value? | value_ref?
  content_digest
}
```

Repeated reads of the same logical key inside one decision are memoized to the same observation/version.

Do not record unused available market state.

### 8.3 EXACT_REPLAY

EXACT_REPLAY resolves MarketContext exclusively from the decision's recorded `context_reads[]`.

Hard failures:

- required read missing;
- digest/version incompatible;
- replay decision attempts an unrecorded decision-critical read;
- recorded read cannot be resolved to its exact value.

No `DecisionObservation`, `BarObservation` or giant snapshot entity is introduced.

---

## 9. Strategy runtime contract

`echo/strategy_engine(strategy_id)` state contains only:

- Strategy technical finite state;
- Strategy-private indicators;
- analytical readiness;
- effective/pending Strategy config according to cycle rules;
- timers/generations;
- `owner_input_seq`;
- `strategy_eval_seq`;
- `strategy_cycle_seq`;
- trigger dedup/order bookkeeping.

It never owns account/MM/provider/execution state.

### 9.1 Evaluation

```text
admitted trigger
  -> dedup guard
  -> capture decision context as consumed
  -> deterministic Strategy evaluation
  -> update technical state
  -> 0..N ordered Signals
  -> transactional Signal egress
```

### 9.2 Signal contract

```text
Signal {
  signal_id
  strategy_id
  strategy_cycle_seq
  intent
  instrument_id
  direction?
  details {
    technical Strategy-specific fields
    technical_stop?       when Strategy defines one
  }
  created_at
  valid_until
  provenance {
    run_mode
    run_id
    strategy_eval_seq
    signal_seq
    trigger_identity
  }
}
```

For S1/S2, no money/profit target field is populated for GerardMM.

---

## 10. Fan-out and delivery

`echo/signal_fanout(strategy_id)` linearizes the target AccountStrategy set visible for the Signal.

Delivery:

```text
SignalDelivery {
  signal_id
  strategy_id
  strategy_cycle_seq
  account_strategy_id
  intent
  direction?
  instrument_id
  details
  strategy_eval_seq
  signal_seq
  signal_created_at
  valid_until
  run_mode
  run_id
}
```

Destination:

```text
echo/operation(account_id:account_strategy_id)
```

The fan-out maintains only required dedup/order bookkeeping. No account business state or Strategy re-evaluation occurs there.

---

## 11. Operation owner state

Minimum contract-level owner state:

```text
OperationOwnerState {
  active_operation?
  pending_admission?
  last_materialized_cycle_seq
  pending_next_cycle_open?       bounded to the accepted one-cycle behavior
  delivery_dedup/order guards
}
```

### 11.1 Operation

```text
Operation {
  operation_id
  execution_account_id
  account_strategy_id
  strategy_id
  strategy_cycle_seq
  direction
  instrument_id
  contract_snapshot {
    contract_id
    tick_size
    point_value
    tick_value
    qty_min
    qty_step
    quote_currency
  }
  mm_config_snapshot
  mm_state
  status
  termination?
  admission_decision_id?
  orders[]
  run provenance
}
```

No full ProviderRuleSet is persisted in Operation merely for history. Decisions carry provider provenance; current complete RuleSet is read-only input where required.

### 11.2 Pending admission

```text
pending_admission? {
  request_id
  opening_signal_id
  strategy_cycle_seq
  opening_signal_delivery
}
```

It contains no `operation_id`, MM state, Order or reservation.

One pending admission at most.

---

## 12. Stage-1 provider admission contract

Operation sends an account-keyed admission request with deterministic/reused continuation `request_id`.

`echo/provider_rules(account_id)` evaluates current:

- Account operational state;
- enabled ProviderAccountBinding;
- provider/program/optional phase;
- complete effective RuleSet;
- automation entitlement;
- provider new-risk window;
- provider account risk state;
- required instrument/Contract eligibility;
- current authority provenance.

Result:

```text
AdmissionResult {
  request_id
  account_id
  result                  ALLOW | DENY_NEW_RISK
  decision_id
  rule_set_id
  rule_set_version
  reasons[]
  evaluated_at
}
```

Missing/unknown/stale authority required for new risk => DENY/fail closed.

ALLOW is continuation permission, not an Operation, reservation or command grant.

---

## 13. MoneyManagement invocation contract

GerardMM executes inside the Operation owner and receives:

- current Operation/Fills/Orders;
- immutable MM config snapshot;
- Contract economic specs;
- required MarketContext;
- Account economic state;
- `account_day_id`;
- `account_day_current_pnl_money`;
- PnL snapshot version/freshness;
- complete effective ProviderRuleSet read-only;
- provider hard monetary headroom where exposed by provider authority;
- current trigger/event;
- current local executable claims.

GerardMM returns domain decisions, not physical side effects:

- zero or more exact Order requests/actions;
- MM termination intent;
- protective-order reconciliation intent;
- updated MM-owned `mm_state`.

### 13.1 Economic plan

```text
EconomicPlanKey =
  economic_stage
  + evaluation_business_day_ordinal?
  + funded_mode?
```

Configured V1 evaluation rows:

```text
day 1: SL=2000 USD, TP=1500 USD
day 2: SL=2000 USD, TP=1500 USD
```

Unconfigured key => new risk denied locally.

### 13.2 Account-day formulas

Let `P_day = account_day_current_pnl_money`.

```text
remaining_profit_objective_money =
  max(0, configured_TP - P_day)

owner_remaining_loss_budget_money =
  min(
    configured_SL,
    max(0, configured_SL + P_day)
  )
```

Effective loss headroom is min with applicable provider hard monetary headroom.

### 13.3 Derived target mark

For a live Operation with current exit-side mark `M`, signed direction `d`, quantity `Q>0`, and point value `V`:

```text
target_mark_raw =
  M + d * (remaining_profit_objective_money / (Q * V))
```

Apply the frozen conservative tick rounding.

This value is derived and must not become persisted target authority.

---

## 14. Order contract and local executable claims

### 14.1 Order fields

Contract-level Order state includes:

```text
Order {
  order_id == client_order_id
  operation_id
  role                     ENTRY | ADD | PROTECTIVE | REDUCE | EXIT
  side
  type
  requested_qty
  q_exec_max
  prices/tif as applicable
  status
  cumulative_filled_qty
  provider refs?
  cancellation/replacement state?
  rejection?
}
```

Role is descriptive. Safety is based on signed executable effect.

### 14.2 q_exec_max

`q_exec_max` is updated only from authoritative Fill/finality/action evidence.

For Operation direction safety, all simultaneously executable opposing-side Orders jointly claim reducible logical exposure.

An Order may not be authorized locally if a valid execution ordering of all outstanding `q_exec_max` claims can invert the Operation direction.

ForceClose and Strategy/MM exits obey the same envelope.

### 14.3 Claim release

Release only on facts that reduce what can still execute:

- Fill consuming executable quantity;
- venue-authoritative reject/finality;
- accepted modify-decrease reflected by venue;
- other exact finality defined by adapter contract.

Cancel request alone does not release.

---

## 15. Provider capacity reservation contract

For each exact Order action affecting a configured shared cap, Operation submits signed executable effect to `echo/provider_rules(account_id)`.

Conceptual request:

```text
ExposureReservationRequest {
  request_id
  account_id
  account_strategy_id
  operation_id
  order_id
  action_id?
  instrument_id
  contract_id
  product_group
  side
  exact_qty
  signed_effect
  q_exec_max_candidate
  required_rule_families/scopes
}
```

Provider serializes current firm exposure + outstanding reservations/account state and either denies or grants that exact quantity.

Conceptual grant:

```text
ExposureGrant {
  grant_id
  request_id
  reservation_id
  exact_qty
  signed_effect
  scopes/families
  rule_set_id/version
  authority_version
  decision_id
  state                   RESERVED | EGRESS_AUTHORIZED | INVALIDATED | FINAL
}
```

No `max_admissible_qty` or silent resize exists.

### 15.1 Metrics

The reservation engine applies the configured typed family:

- GROSS;
- NET_ABS;
- GROUP_WEIGHTED.

It must use the reachable executable envelope, not current net Position alone.

### 15.2 Fill transfer

A Fill transfers corresponding quantity from outstanding executable reservation to firm attributable exposure without widening the reachable envelope.

Reservation/bookkeeping update is idempotent by request/grant/fill identity.

---

## 16. Mandatory final provider revalidation

Every exact grant that is not yet egressed must send:

```text
ReservationRevalidate {
  grant_id
  reservation_id
  request_id
  account_id
  operation_id
  order_id
  action_id?
  exact_qty
  signed_effect
  scopes/families
  original_authority_provenance
}
```

to the authoritative `echo/provider_rules(account_id)`.

Result:

```text
ReservationRevalidateResult {
  grant_id
  result                  VALID | INVALID
  current_authority_provenance
  provider_decision_id
}
```

VALID transition:

```text
RESERVED -> EGRESS_AUTHORIZED
```

This transition is the provider authorization point.

It is not M1 publication and must not be named `egress_committed`.

INVALID ensures no command becomes visible at M1.

---

## 17. Provider RuleSet visibility and ownership

`ProviderRuleSet` is transferred/available **complete** to read-only account/MM context. Do not prefilter fields based on today's GerardMM implementation.

Only `echo/provider_rules(account_id)` may authoritatively enforce external account-wide policy.

MoneyManagement may use RuleSet facts to make its own economic decision, but cannot mutate reservations, admission or provider safety state.

Provider runtime must not decide strategy economics or choose alternative quantity on behalf of MM.

---

## 18. M1 command boundary

After:

1. local Operation executable-exposure guard;
2. exact provider reservation/grant if needed;
3. mandatory final revalidation => `EGRESS_AUTHORIZED`;
4. local Order/action still eligible;

Operation may publish the command transactionally with its checkpointed state.

```text
M1 =
  StateFun committed state
  + EXACTLY_ONCE transactional command egress
```

Candidate command routing:

```text
echo.order-commands.{execution_account_id}.v1
```

Consumer must use committed transactional data semantics.

A command must carry enough pinned data for the execution edge to act without querying mutable domain config:

- stable Order/action IDs;
- execution account;
- Operation correlation;
- pinned Contract/external identifier as required;
- exact terms;
- physical binding identity/provenance required for submission.

---

## 19. Futures Bridge and ExecutionAdapter contract

### 19.1 Bridge

Bridge is a sibling runtime shell, not a domain owner. It manages:

- account consumers/sessions;
- binding-specific adapter instances;
- M2 journal;
- normalized event publication;
- health/readiness/telemetry.

### 19.2 M2 journal

Before the first transport step that may reach the venue:

```text
M2JournalRecord {
  execution_account_id
  client_order_id
  physical_binding
  full submitted terms
  action ids
  provider order refs?
  reconciliation cursors/evidence?
  state
}
```

State:

```text
PREPARED
SUBMITTING
VENUE_BOUND
TERMINAL
AMBIGUOUS
```

The physical store is D6 implementation/certification territory, but it must be genuinely durable before the side effect.

### 19.3 M2 point-of-no-return

`SUBMITTING` must be durable before the first call/write that can reach the venue.

After that point:

- timeout/disconnect/crash => MAY_HAVE_EXECUTED;
- no blind retry;
- reconcile using stable client identity/native idempotency/history;
- if absence cannot be authoritatively proven, remain AMBIGUOUS.

---

## 20. Normalized execution outputs

Five semantic families:

```text
OrderObservation
OrderActionObservation
Fill
PositionObservation
ExecutionSessionObservation
```

Operation-correlated events route by `account_id:account_strategy_id` or equivalent explicit correlation to the owning Operation function.

Position routes by account+Contract to the physical position/reconciliation surface.

Execution session state is account/binding runtime state, not an Order event.

---

## 21. Execution capability requirements

An adapter/binding used for exact V1 physical execution must prove, for the used order/action classes:

- supported order types;
- modify/replace semantics;
- cancel;
- partial Fill delivery/recovery;
- client identity round-trip;
- safe idempotency and/or authoritative lookup/history;
- authoritative negative semantics sufficient for any retry;
- open-order reconciliation;
- stable provider execution identity;
- terminal finality evidence;
- complete-enough Position snapshot;
- reconnect/resubscribe;
- provider external-account binding;
- program automation/API entitlement.

`UNKNOWN` does not pass an exact-submission gate.

D2 selects no external real transport. D5 begins with the generic bridge seam and `SimExecutionAdapter`; real transport selection/certification remains D6.

---

## 22. Execution readiness

New-risk execution readiness is the conjunction of:

```text
static binding eligibility
AND connected
AND authenticated
AND correct provider account bound
AND order/execution event stream healthy
AND reconciliation authority available
AND no unresolved M2 ambiguity
AND fresh/complete-enough Position
AND required submission capabilities exact-ready
```

Kafka consumer health or socket connectivity alone is not readiness.

On reconnect/restart new risk remains off through the full reconciliation barrier.

---

## 23. Config pinning and hot transitions

### Pinned

- Operation Contract/spec snapshot.
- MM config snapshot for the Operation.
- physical binding on submitted actions.
- stable Order/action identities.

### Hot/prospective

- current Instrument→Contract mapping for future materialization;
- provider RuleSet/binding authority;
- account operational state;
- market serving authority;
- calendar/window snapshots through ordered material transitions;
- Strategy config according to technical-cycle activation rules.

A hot provider update can invalidate a still-pending exact grant at final revalidation. Once `ReservationRevalidate` returns VALID and the exact grant becomes `egress_authorized`, later provider-authority updates are prospective for that grant even if M1 publication has not happened yet. M1 remains a separate later Core command-visibility boundary; subsequent safety/update behavior follows new authority prospectively.

---

## 24. Checkpoint / transactional boundaries

### 24.1 Market canonical transport

Canonical market transport may remain at-least-once when per-stream ordering and deterministic identity/idempotency are certified. Downstream owners guard by canonical identity/`stream_seq`.

### 24.2 Deterministic recording/control

Material run journal/control egress that binds owner state to recorded deterministic order must be checkpoint-atomic / transactional as frozen by D2-06.

### 24.3 Strategy Signal

Strategy state mutation + Signal egress must share the required transactional checkpoint boundary so crash recovery cannot commit one without the other.

### 24.4 Operation command/facts

Operation state plus Core command/fact egress must preserve M1 exactly-once semantics.

### 24.5 Provider decisions

Provider authoritative state transitions and their durable decision facts must be emitted in a consistency boundary that cannot publish a decision contradicted by restored owner state.

### 24.6 Projections

PostgreSQL materializations are idempotent/stale-safe query projections. They do not become recovery authority.

---

## 25. Ordering guarantees

Required ordering scopes:

- market canonical inputs: per `stream_id`;
- Strategy evaluations: per `strategy_id`;
- ordered Signals from one evaluation: `signal_seq`;
- account deliveries/Operation state changes: per `account_id:account_strategy_id`;
- provider account-wide capacity/admission: per `account_id`;
- physical command handling: at least ordered enough per account/Order/action that adapter journal semantics remain valid.

No global ordering across independent accounts or streams is required.

---

## 26. Dedup guards

Minimum dedup surfaces:

| Surface | Dedup identity |
|---|---|
| source event A/B class | source-native identity / packet+entry position |
| canonical market downstream | stream + canonical identity/sequence/digest |
| Strategy trigger | natural trigger identity |
| Signal | deterministic `signal_id` |
| fan-out delivery | strategy + signal + account_strategy |
| Operation delivery | account_strategy + signal |
| provider admission | request_id |
| reservation/grant | request_id / grant_id |
| final revalidation | grant_id + exact grant identity |
| Order physical submission | execution account + client_order_id |
| action | cancel_id / replace_request_id |
| Fill | account + native provider_execution_id |

Dedup must precede state mutation for the protected scope.

---

## 27. Failure semantics

### Fail closed for new risk

- market/calendar/analytical not ready;
- unresolved Contract or identifier;
- Strategy required config absent;
- account/provider admission unknown/stale/denied;
- GerardMM economic plan/PnL input absent or stale;
- local executable-exposure invariant cannot be satisfied;
- provider exact reservation/revalidation denied;
- physical Position untrusted where required for capacity;
- execution binding/capability/readiness insufficient;
- M2 ambiguous;
- entitlement unknown/forbidden.

### Fail visible without inventing state

- canonical market identity conflict;
- late correction after decision;
- unmatched/manual physical activity;
- late Fill after local terminal expectation;
- inaccessible original physical binding;
- provider cap lowered below already-existing exposure;
- cold recovery requiring evidence that is unavailable.

---

## 28. S1 contract parameters

Frozen S1 parameters/inputs:

```text
instrument_id = NQ
bar_tf = 5m
opening_range_window_id = NY_OPEN
premarket_window_id = REQUIRED_CONFIG
market_event trigger = TRADE
```

Opening range 09:30–10:00 ET comes from the named-window authority.

Technical stop is derived only from closed 5m bars from resolved premarket start through previous closed 5m bar.

No profit target field exists.

---

## 29. S2 contract parameters

Frozen S2 contract:

```text
instrument_id = NQ
trend_tf = H4
trend = SMA50 current vs previous, frozen eligibility rule
entry_tf = 5m
Bollinger period = 20
Bollinger deviation = 2.0
stddev = population
```

Technical stop is Strategy output.

Bollinger basis belongs only to Strategy lifecycle close logic. It is not exported as GerardMM target authority.

---

## 30. GerardMM branch/state contract

MM-owned durable state remains minimal and Operation-local. It may include the accepted plan identity, initial reference price/stop/quantity, selected branch, consumed add attempts, branch lock and pending decision/action identities required for idempotency.

It must not persist as authority:

- account-wide PnL;
- current daily remaining objective;
- provider reservation state;
- Position;
- derived target mark;
- arbitrary portfolio state.

Adverse and favorable branch are mutually exclusive and bounded by explicit config.

---

## 31. Forbidden implementation substitutions

D5 must reject any implementation that silently introduces:

- `DecisionObservation` / `BarObservation`;
- global event sequencer;
- generic workflow/saga;
- provider-specific MM subclasses;
- a second provider economics engine;
- `max_admissible_qty`;
- silent quantity clipping;
- WIND_DOWN;
- generic liquidation override;
- Strategy profit target;
- Position-to-Operation attribution;
- automatic physical retry after ambiguity;
- automatic cross-host execution takeover;
- an unbounded pending-cycle queue;
- Core transport branching by vendor.

Any of these requires an explicit future architecture change, not “implementation detail”.
