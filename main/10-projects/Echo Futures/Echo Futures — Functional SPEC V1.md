# Echo Futures — Functional SPEC V1

## 1. Purpose

This SPEC freezes externally meaningful V1 behavior and domain semantics for Echo Futures. It describes what the system must do, not how source files are organized.

It consumes Architecture Candidate V2 plus the accepted D2/D4 authorities. It does not emit `EF_D4_ARCH_FREEZE` and does not authorize D5.

---

## 2. System modes

The same domain rules apply in:

- LIVE;
- DEMO/SHADOW where configured;
- EXACT_REPLAY;
- BACKTEST.

Differences between modes are input/time/execution adapters, not duplicated Strategy or MoneyManagement business logic.

EXACT_REPLAY reproduces the exact ordered decision inputs and exact decision-critical context consumed by the recorded run. BACKTEST is a new deterministic historical run and is not required to reproduce the arrival disorder of a past live run.

---

## 3. Market readiness

A Strategy may evaluate productively only when all market requirements it declared are ready.

Readiness is composed from:

1. market stream readiness for the required consumption class;
2. analytical readiness for required bars/indicators;
3. resolvable calendar/session/window state;
4. current effective Strategy config.

Availability of stale last-known price is not equivalent to readiness.

Missing or unresolved calendar, missing Contract mapping, history-dependent recovery that cannot be proven, or incomplete warm-up must not be converted into an implicit 24x7/default-ready state.

New technical Signals are fail-closed while required readiness is false.

---

## 4. Canonical market behavior

Each logical stream is identified by `(instrument_id, contract_id)`.

A canonical market fact has an identity distinct from its position in the stream:

```text
canonical_event_id != stream_seq
```

Two different canonical facts must never silently occupy the same sequence position.

A market-source switch may change serving authority/epoch but does not roll the Contract. Rollover is a separate owner-driven change.

Late data may correct a derived market projection. It never rewrites a past Strategy/MM decision already made from an earlier observed version.

---

## 5. Strategy S1 — NY Opening Range Breakout 30m

### 5.1 Configuration

Required:

- Instrument NQ.
- 5m canonical bars.
- canonical TRADE events.
- `opening_range_window_id = NY_OPEN`, whose authority resolves 09:30–10:00 America/New_York intersected with exchange availability.
- `premarket_window_id` explicitly configured and resolvable.

No hardcoded premarket start is allowed. Missing/invalid premarket configuration makes the Strategy unable to open new risk.

### 5.2 Opening range

The opening range is built from the exact six valid closed 5m bars of the NY_OPEN window.

If the range cannot be proven from canonical closed bars, the day is not tradable by S1.

### 5.3 Breakout

After the range closes:

- LONG breakout requires a strict canonical TRADE crossing from at/below the OR high to above it.
- SHORT breakout requires a strict canonical TRADE crossing from at/above the OR low to below it.

A touch without crossing is not an OPEN.

### 5.4 Technical stop

At the OPEN decision instant:

```text
LONG:
technical_stop = minimum low of all closed 5m bars
                 from configured premarket start
                 through the previous closed 5m bar

SHORT:
technical_stop = maximum high over the same closed-bar range
```

The forming candle is excluded.

The stop must be on the adverse side of the entry and valid on the Contract tick grid. Once emitted for the technical cycle it is the Strategy technical reference; Strategy does not turn it into a monetary target.

### 5.5 Lifecycle

S1 emits only the technical lifecycle intents required by its frozen behavior:

- OPEN;
- CLOSE_ALL.

No Strategy profit target exists.

Technical stop hit or the frozen “back inside opening range” close condition emits CLOSE_ALL. Re-arm follows the frozen closed-bar condition and never opens again on the same close that performs the re-arm.

A new trading-window day closes any still-open technical cycle before the Strategy resets for the next day.

---

## 6. Strategy S2 — H4 Trend / 5m Bollinger Pullback

### 6.1 Inputs/readiness

S2 requires:

- 51 eligible closed H4 bars for trend readiness;
- 20 eligible closed 5m bars for Bollinger readiness;
- the frozen same-boundary rule that a H4 bar closing at the same boundary as the trigger 5m bar is not visible until the next 5m decision.

Trend uses the accepted H4 SMA50 semantics.

Bollinger uses period 20, deviation 2.0 and population standard deviation over closed 5m closes.

### 6.2 Setup

LONG requires the accepted H4 LONG trend plus an ARMED 5m pullback touching/crossing the lower band and closing back above lower band while still below the basis.

SHORT is symmetric against the upper band.

Entry is MARKET from the 5m BAR_CLOSE evaluation and uses the frozen Signal validity window.

### 6.3 Technical stop

S2 emits its accepted trigger-bar technical stop, including configured tick buffer.

The technical stop remains Strategy output.

### 6.4 Technical close

The Bollinger basis is **not a profit target**.

For an open LONG technical cycle, a qualifying closed 5m bar returning to/through the basis emits CLOSE_ALL. SHORT is symmetric.

Trend invalidation also emits CLOSE_ALL according to the frozen S2 state machine.

No GerardMM target is stored in Signal details.

---

## 7. Signal lifecycle

A Strategy evaluation may emit zero or multiple ordered Signals.

Each Signal has:

- deterministic identity;
- a Strategy technical cycle;
- an intent;
- canonical Instrument;
- validity window;
- ordered provenance.

The Strategy technical state is account-agnostic. It does not wait for physical execution convergence in each account.

Signal redelivery must not produce a second logical evaluation or duplicate account action.

---

## 8. AccountStrategy fan-out

One immutable Signal is evaluated once by Strategy and then delivered to the currently applicable AccountStrategy bindings.

Functional rules:

- an enabled binding receives its Strategy Signals;
- a disabled binding receives no new-risk OPEN;
- a disabled binding with a live Operation may still receive technical management Signals required to reduce/close it;
- target-set changes are linearized in the fan-out runtime and final local binding validity is rechecked by the Operation owner;
- no Strategy indicators or technical setup are recomputed per account.

---

## 9. Stage-1 provider admission

Before an OPEN can materialize an Operation, the account must pass authoritative provider admission.

While the authoritative response is pending, `echo/operation` may hold exactly one nullable pending-admission record. No Operation/MM/Order exists because of that pending state.

Functional behavior:

- ALLOW for the still-active request continues normal materialization.
- DENY clears pending admission and no Operation is created.
- CLOSE/CLOSE_ALL for that same cycle invalidates pending admission.
- OPEN for a later technical cycle supersedes the older pending admission.
- a late result for a superseded/invalidated request is a no-op with visible provenance.
- no generic saga, workflow or backlog of multiple future cycles exists.

---

## 10. Operation creation

An Operation is created only from an OPEN that remains valid and passes all materialization guards.

At creation it freezes:

- account/account-strategy/strategy/cycle identity;
- technical direction;
- current execution Contract;
- required Contract economic specs;
- effective MM config;
- run provenance;
- provider admission reference.

Exactly one Operation may ever materialize for a given AccountStrategy technical cycle. At most one is non-terminal at a time.

If the Strategy reaches a new cycle while the current Operation is physically terminating, only the bounded one-future-cycle behavior already frozen by the runtime is allowed.

---

## 11. Initial GerardMM decision

GerardMM receives the new Operation plus required account/market/provider context.

Before opening risk it must have an explicit economic plan for the current account stage/day.

Evaluation plan:

```text
day 1: SL 2000 USD / TP 1500 USD
day 2: SL 2000 USD / TP 1500 USD
```

A day without an explicit configured row fails closed for new risk.

Funded modes `FUNDED_INITIAL` and `FUNDED_STEADY` are valid schema states, but their SL/TP amounts must be configured. No implicit funded numbers are allowed.

Initial quantity is exact and must satisfy:

- technical-stop risk economics;
- Contract quantity/tick rules;
- current Owner loss budget;
- provider per-order restrictions;
- provider shared-cap authorization where applicable.

A denied exact quantity is not silently resized.

If no executable action remains, the Operation follows an explicit no-action/failed-entry termination path rather than disappearing.

---

## 12. Account-day monetary economics

The economic authority consumed by GerardMM is:

```text
account_day_current_pnl_money
```

It represents current realized + unrealized PnL account-wide for the current account day.

GerardMM must not reconstruct other Operations' PnL.

Remaining daily objective:

```text
remaining_profit_objective_money =
  max(0, configured_TP - account_day_current_pnl_money)
```

Owner remaining loss headroom:

```text
owner_remaining_loss_budget_money =
  min(
    configured_SL,
    max(0, configured_SL + account_day_current_pnl_money)
  )
```

Provider hard monetary headroom may reduce the effective available loss budget.

Prior account-day profit does not expand the Owner SL beyond its configured value.

Other Operations' current unrealized PnL changes these account-day values because the input is account-wide.

---

## 13. Dynamic daily profit exit

Strategy never supplies GerardMM with a fixed profit target price.

When there is live Operation quantity, GerardMM may derive a current implicit target mark from:

- the remaining account-day objective;
- current quantity;
- current exit-side mark;
- point value.

That mark is observational/derived, not state authority.

If the account-day objective is already satisfied before an entry/add, no new risk is opened.

If it becomes satisfied while an Operation is live, profit termination has precedence over add logic. GerardMM initiates the normal exit/termination path using exact executable quantities and provider authorization.

---

## 14. Protective stop

The effective protective stop may combine:

- Strategy technical stop;
- GerardMM monetary protection;
- existing protection already installed.

Protection is monotonic toward less risk. It never loosens because of an add, partial Fill or market move.

A favorable filled add must not degrade already-achieved protection and applies the accepted break-even/protection semantics.

Modify/replace actions remain subject to physical finality and provider-capacity rules; local intent does not equal venue-final stop state.

---

## 15. Adverse hardscalping add

An adverse branch may activate only according to explicit MM configuration and the frozen trigger thresholds.

V1 behavior:

- branch is mutually exclusive with favorable branch for that Operation;
- add count is bounded;
- each proposed add has an exact quantity;
- candidate economics are recomputed with resulting quantity/average and account-day budgets;
- exact provider grant is required when a shared cap is affected;
- partial Fill consumes the accepted add attempt as frozen by GerardMM;
- no automatic top-up is sent to “complete” a partial Fill;
- provider deny or invalid final revalidation locks further new-risk scaling as specified.

No unlimited progression or inter-Operation martingale exists.

---

## 16. Favorable add

The favorable branch obeys the same safety properties:

- explicit configured trigger;
- mutually exclusive branch lock;
- bounded number of adds;
- exact quantity;
- candidate economics before emission;
- protective stop cannot loosen;
- provider exact authorization/revalidation;
- partial Fill truth;
- no top-up.

Research seed values are not LIVE/DEMO defaults.

---

## 17. Provider Order authorization

After MM proposes an exact Order, local Operation direction/executable-exposure safety is evaluated.

Where a provider shared cap is relevant, `echo/provider_rules(account_id)` serializes the account-wide reservation and returns an exact grant or deny.

Every grant that is still pending Core egress must then pass mandatory final:

```text
ReservationRevalidate
```

against current provider authority.

Only VALID final revalidation may mark that exact grant `egress_authorized`.

The provider authorization point is distinct from M1 command publication and from M2 physical submission.

An invalidated grant never escapes Core.

---

## 18. Concurrent executable exposure

All live Orders are evaluated by what can still physically execute.

Reducing/EXIT/ForceClose actions must not double-spend the same reducible Operation exposure.

Provider account-wide reservations must account for any Order that can affect a supported shared cap under a valid execution ordering. An Order is not exempt merely because its role says REDUCE/EXIT.

Cancel request does not instantly release executable claim or provider capacity.

Modify-decrease releases only after authoritative acknowledgement. Modify-increase reserves the exact delta. Replace remains conservatively represented while old and new legs can both execute.

No automatic quantity clipping is allowed.

---

## 19. Technical Strategy CLOSE_ALL

A technical CLOSE_ALL:

- records the relevant MM/Operation termination intent/path;
- blocks later new-risk actions for the terminating Operation;
- cancels/reconciles live executable Orders as needed;
- emits exact closing actions for actual reducible exposure;
- waits for physical finality and Fill truth;
- does not terminalize instantly.

A Strategy technical close and a provider safety close share the same physical safety invariants but retain distinct provenance.

---

## 20. Provider denial

Provider denial can occur at two functional points.

### 20.1 Stage-1 OPEN admission denial

No Operation exists. The OPEN is not materialized.

### 20.2 Exact Order/grant denial

The Operation already exists. The proposed Order is not emitted physically. The denial is durable and visible to MM, which may terminate, continue with existing exposure, or make a later distinct decision allowed by its policy.

The provider runtime never substitutes a smaller quantity as an implicit economic decision.

---

## 21. ForceClose

ForceClose is an account/provider safety intent delivered to each affected live Operation.

It must:

- invalidate new-risk progression;
- respect local q_exec/reducible-exposure safety;
- respect shared provider capacity semantics needed to avoid unsafe reachable exposure;
- cancel/reconcile working Orders without assuming cancel request is final;
- emit required exact close quantities only when safe/authorized;
- remain pending while execution edge is unavailable;
- reconcile first after reconnect;
- reach terminal state only when exposure is zero, no live Orders remain and termination intent is present.

No synthetic “close succeeded” is permitted.

---

## 22. Partial fills

Partial Fill is normal behavior.

Functional truth:

- every native execution fact is preserved once;
- Operation exposure changes only by Fill facts;
- Order filled quantity/average price are derived;
- MM state reacts to the serially processed Fill sequence;
- a partial add does not trigger a compensating top-up;
- reservations/claims converge through Fill transfer and finality rules;
- a late Fill after cancel/expiry remains true and may forward-correct derived Order status;
- Position deltas never manufacture missing Fills.

---

## 23. Reject / cancel / replace

A request-level acknowledgement is not finality.

- A definite venue reject is terminal only with authoritative evidence that no executable Order was accepted.
- Cancel remains pending until authoritative order/fill reconciliation proves the final state.
- Replace uses native modify/atomic replace only when the adapter capability proves it; otherwise cancel+new Orders preserve independent physical identities and concurrent executable exposure.
- Timeout/disconnect after possible side effect is ambiguity, not a reject.

---

## 24. Terminal lifecycle

An Operation may become terminal only when all are true:

```text
logical_exposure == 0
AND no live executable Orders
AND termination intent is recorded
```

Operation terminality is never inferred from:

- Position being flat;
- Order cancel requested;
- a single local status;
- ForceClose arrival;
- provider denial alone.

A terminal Operation is never revived. Later physical facts are preserved and surfaced as invariant breach/reconciliation debt as defined by the execution contract, not by inventing another Operation.

---

## 25. Physical Position and manual activity

Position is venue-authoritative physical net exposure by account+Contract.

Manual/provider/external activity that cannot be correlated to an Echo Order:

- remains physical observation;
- may produce `POSITION_MISMATCH`;
- may degrade new-risk readiness;
- is never attributed to a Strategy/Operation by inference;
- never creates a synthetic Fill.

If later authoritative reconciliation proves Echo correlation, canonical execution facts are emitted with real identities.

---

## 26. Replay boundaries

### 26.1 EXACT_REPLAY

EXACT_REPLAY reproduces:

- recorded ordered decision inputs;
- material config/session/timer/recovery transitions;
- the ReplayAnchor required from run start;
- exact decision-critical `context_reads[]`.

It does not query current/latest mutable market state in place of a recorded decision observation.

A late correction recorded after a decision remains after the decision in replay and does not retroactively change it.

### 26.2 BACKTEST

BACKTEST runs the same domain logic over a deterministic historical market/time/execution source. It may use corrected historical data as a new run; that is not a claim of reproducing a past live run.

### 26.3 Execution replay boundary

Market exact replay does not magically make physical execution history event-sourced. Physical restart/recovery continues to use the Operation checkpoint/Kafka facts plus M2 venue reconciliation boundary.

---

## 27. Restart and recovery

### Core normal restart

State is restored from the runtime checkpoint and Kafka replay with idempotency guards. PostgreSQL projection state is not used to recreate authoritative Operation/MM state.

### Market analytical recovery

Normal restart restores checkpointeed analytical/Strategy state. New-run warm-up constructs initial state from history. A required cold recovery without enough deterministic recording/checkpoint evidence fails closed rather than silently rebuilding a different decision state.

### Execution edge restart/reconnect

New risk remains off until:

1. binding/auth is verified;
2. event stream is re-established;
3. non-terminal M2 journal entries are reconciled;
4. open Orders and missed Fills are recovered;
5. Position is fresh;
6. mismatches/ambiguities are surfaced;
7. execution readiness is recomputed.

Reconnect never means “resend pending commands”.

---

## 28. Configuration transitions

Hot changes are prospective and ordered.

They must not rewrite:

- past decisions;
- a live Operation's pinned Contract;
- the effective MM config pinned for that Operation;
- the physical binding of already-submitted Orders.

A provider rules update may affect the next admission/order revalidation and may trigger a typed safety action when the new rule explicitly requires it.

A Strategy config update follows the frozen cycle transition semantics; it is not silently injected halfway through an active technical cycle where the authority forbids that.

---

## 29. V1 non-goals

The functional contract does not include:

- discretionary/manual interpretation of S1/S2;
- Strategy monetary profit targets;
- account portfolio optimization;
- inter-Operation martingale;
- automatic rollover of live exposure;
- provider-specific MoneyManagement implementations;
- generic workflow/saga processing;
- automatic execution failover across hosts/transports;
- synthetic Fill/Position attribution;
- silent risk-size clipping;
- arbitrary Strategy-cycle backlog.

These require new evidence and a future design decision, not opportunistic implementation in D5.
