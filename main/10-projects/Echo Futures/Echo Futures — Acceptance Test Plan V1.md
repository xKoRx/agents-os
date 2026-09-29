# Echo Futures — Acceptance Test Plan V1

## 1. Purpose

This plan defines the minimum D5/D6 acceptance evidence required to prove the frozen Echo Futures V1 contracts.

Tests trace to Architecture Candidate V2, Functional SPEC V1 and Technical SPEC V1. Passing this plan does not by itself emit `EF_D4_ARCH_FREEZE`; it is the evidence contract for implementation/certification.

Test classes:

- **D5 UNIT/DOMAIN** — pure deterministic domain tests.
- **D5 COMPONENT** — keyed runtime/component tests with deterministic harnesses.
- **D5 INTEGRATION** — Kafka/StateFun/Bridge/SimExecution seams.
- **D6 CERTIFICATION** — physical runtime, capacity, replay golden, journal durability, real selected adapter.

---

## 2. Market identity and replay

### MKT-01 — canonical identity differs from sequence
**Trace:** Technical §3/§4.  
Given two canonical market facts in one stream, prove each has its own canonical identity and durable sequence position. Assert no code path treats `stream_seq` as the semantic event identity.  
**Evidence:** unit/component assertions + serialized fixtures.  
**Gate:** D5.

### MKT-02 — same stream sequence cannot identify different canonical facts
Inject redelivery with same stream/sequence/identity/digest => no-op. Then inject same sequence with incompatible identity or digest.  
Expected: fail-visible `MARKET_IDENTITY_CONFLICT`; no silent state mutation.  
**Gate:** D5.

### MKT-03 — duplicate canonical delivery
Redeliver an already-applied canonical event.  
Expected: market analytics and Strategy state unchanged; no duplicate bar mutation or Signal.  
**Gate:** D5.

### MKT-04 — source packet with multiple entries
For a class-B source packet/message sequence containing N physical entries, map deterministic entry positions and prove N canonical MarketEvents survive.  
**Gate:** D5 domain/adapter fixture.

### MKT-05 — legitimate identical trades
Two physical trades with same timestamp/price/qty but distinct native identity are both preserved.  
For a class-C source without dedup-safe identity, prove no content-hash suppression exists.  
**Gate:** D5.

### MKT-06 — authority switch preserves logical stream
Switch serving source with same Contract.  
Expected: same `stream_id`, new `authority_epoch`, no Contract rollover, current-state new epoch seeded independently, previous state retained only as last-known.  
**Gate:** D5.

### MKT-07 — rollover differs from source switch
Owner rolls NQ mapping from old to new Contract while old Operation remains live.  
Expected: Strategy/new demand may use new Contract prospectively; live Operation remains pinned to old Contract.  
**Gate:** D5.

### MKT-08 — crash/order recovery
Crash market owner around canonicalization/checkpoint boundaries, restore and replay.  
Expected: same accepted facts, same ordering, no duplicated canonical fact.  
**Gate:** D5 integration.

### MKT-09 — late correction after decision
Create closed bar X, trigger Strategy decision, then deliver a late event that corrects projection to X'.  
Expected: market projection becomes X'; prior decision remains based on X; no retroactive Signal.  
**Gate:** D5.

### MKT-10 — exact ContextRead capture
A decision reads quote Q and closed bars B1..Bn.  
Expected: only consumed logical reads appear in ordered `context_reads[]`; unused available state is absent.  
Repeated read of same logical key returns same observed version.  
**Gate:** D5.

### MKT-11 — exact replay context
Replay MKT-10 from recorded ordered input + `context_reads[]`.  
Expected: same Strategy/MM decision bytes/semantic result.  
Modify current live shared state before replay; replay result must remain unchanged.  
**Gate:** D5 component; D6 golden.

### MKT-12 — missing/extra replay read
Remove a required ContextRead or cause replay logic to ask for an unrecorded critical read.  
Expected: deterministic replay failure, never fallback to current/latest state.  
**Gate:** D5.

### MKT-13 — replay anchor
Record a run from t0 with required warm-up anchor. Replay from t0 and prove same initial analytical state before owner input sequence begins.  
No anchor => `REPLAY_ANCHOR_MISSING`. Corrupt digest => fail-visible invalid anchor.  
**Gate:** D6 golden.

### MKT-14 — timer close without next tick
Last tick occurs before a bar boundary; timer fires at boundary.  
Expected: bar closes on time without synthetic market event.  
**Gate:** D5.

### MKT-15 — internal break grid
Session has an internal break.  
Expected: forming bar truncates at break, no bars during break, same session grid resumes after break, no grid reset.  
**Gate:** D5.

### MKT-16 — stale last-known is not READY
Feed becomes not-ready but last BBO remains available.  
Expected: Strategy new Signals blocked; MarketContext exposes stale/as-of; any MM policy use must be explicitly allowed by that decision contract.  
**Gate:** D5.

---

## 3. Calendar/session

### CAL-01 — DST-aware wall-clock resolution
Resolve the same named window across DST transition dates using IANA zones.  
Expected: wall-clock semantics preserved without fixed UTC offset.  
**Gate:** D5.

### CAL-02 — holiday / early close
Apply dated calendar override.  
Expected: exchange availability/bars/windows truncate from dataset; no hardcoded holiday logic.  
**Gate:** D5.

### CAL-03 — account day differs from session date
Choose an instant where account reset and exchange session boundaries differ.  
Expected: GerardMM daily economics use account day; Strategy bars/session use exchange calendar.  
**Gate:** D5.

### CAL-04 — unresolved calendar
Instrument enabled for Futures with missing/unresolvable `calendar_ref`.  
Expected: market/Strategy/new risk fail closed; no default 24x7.  
**Gate:** D5.

---

## 4. S1 acceptance

### S1-01 — exact opening range
Provide the six valid 5m bars for 09:30–10:00 ET.  
Expected: OR high/low equal extrema of those bars only.  
**Gate:** D5.

### S1-02 — OR incomplete
Missing/invalid one required OR bar.  
Expected: no OPEN for that day.  
**Gate:** D5.

### S1-03 — LONG strict breakout
Last canonical TRADE <= OR high; next canonical TRADE > OR high.  
Expected: exactly one LONG OPEN with frozen provenance. Touch at OR high does not open.  
**Gate:** D5.

### S1-04 — SHORT strict breakout
Symmetric crossing below OR low.  
**Gate:** D5.

### S1-05 — LONG technical stop
Configured premarket start P. At OPEN time, previous closed 5m bar is B.  
Expected stop = minimum low of all closed 5m bars from P through B; forming bar excluded.  
**Gate:** D5.

### S1-06 — SHORT technical stop
Expected stop = maximum high over same closed-bar interval.  
**Gate:** D5.

### S1-07 — missing premarket config
No `premarket_window_id` / unresolved window.  
Expected: fail closed for OPEN; no invented hour.  
**Gate:** D5.

### S1-08 — stop adverse-side validation
Computed stop invalid relative to entry or tick grid.  
Expected: fail-visible setup invalid; no OPEN.  
**Gate:** D5.

### S1-09 — technical stop close
Open LONG/SHORT cycle reaches frozen stop.  
Expected: CLOSE_ALL once; technical cycle closes.  
**Gate:** D5.

### S1-10 — back-inside close
After breakout, accepted re-entry condition into OR occurs.  
Expected: CLOSE_ALL according to frozen S1 semantics.  
**Gate:** D5.

### S1-11 — re-arm
After close, feed closed-bar sequence satisfying exact re-arm rule.  
Expected: ARMED only at the defined later bar; no same-bar reopen.  
**Gate:** D5.

### S1-12 — new day reset
Technical cycle still open at next window/day transition.  
Expected: required CLOSE_ALL before reset; new day's OR starts cleanly.  
**Gate:** D5.

### S1-13 — no profit target
Inspect S1 OPEN Signal.  
Expected: technical stop present; no Strategy/Gerard profit target field/value.  
**Gate:** D5 contract test.

---

## 5. S2 acceptance

### S2-01 — warm-up
50 H4 closed bars is insufficient; 51 per frozen semantics enables trend evaluation. 19 5m bars insufficient; 20 enables Bollinger.  
**Gate:** D5.

### S2-02 — H4 trend LONG / SHORT
Fixtures prove accepted SMA50/current-vs-previous trend rules in both directions.  
**Gate:** D5.

### S2-03 — same-boundary H4 visibility
H4 bar closes at same boundary as trigger 5m bar.  
Expected: trigger decision uses previous eligible H4 state; newly closed H4 becomes visible next 5m decision.  
**Gate:** D5.

### S2-04 — LONG pullback OPEN
Trend LONG + accepted lower-band touch/cross + close back inside below basis.  
Expected: one LONG OPEN, exact technical stop from trigger semantics.  
**Gate:** D5.

### S2-05 — SHORT pullback OPEN
Symmetric upper-band setup.  
**Gate:** D5.

### S2-06 — basis return close
Open LONG closes at/through basis per frozen rule; SHORT symmetric.  
Expected: CLOSE_ALL. No profit-target field is emitted.  
**Gate:** D5.

### S2-07 — trend invalidation close
Open technical cycle loses trend according to frozen condition.  
Expected: CLOSE_ALL.  
**Gate:** D5.

### S2-08 — re-arm
After close, Strategy does not duplicate OPEN until exact state-machine re-arm conditions occur.  
**Gate:** D5.

### S2-09 — no Gerard target
Inspect Signal/details and GerardMM input.  
Expected: basis never treated as monetary/fixed target.  
**Gate:** D5 contract test.

---

## 6. Signal/fan-out/account admission

### SIG-01 — deterministic Signal identity
Same run + same trigger/eval/sequence produces same `signal_id` through restart/replay.  
**Gate:** D5.

### SIG-02 — 0..N ordered Signals
Exercise no-signal evaluation and a multi-Signal transition.  
Expected: stable ordered `signal_seq`; delivery order preserved.  
**Gate:** D5.

### SIG-03 — disabled binding
Disabled AccountStrategy receives no OPEN but may receive management close on a live Operation.  
**Gate:** D5.

### SIG-04 — target-set config race
Binding changes around fan-out linearization.  
Expected: deterministic target set plus final local guard; no accidental new risk.  
**Gate:** D5.

### ADM-01 — OPEN ALLOW
Stage-1 admission pending then current ALLOW.  
Expected: one materialization after remaining guards; no Operation before ALLOW.  
**Gate:** D5.

### ADM-02 — OPEN DENY
Expected: pending cleared, ProviderDecision durable, zero Operation.  
**Gate:** D5.

### ADM-03 — CLOSE invalidates pending admission
OPEN request pending, then CLOSE/CLOSE_ALL same cycle, then late ALLOW.  
Expected: late ALLOW no-op; no Operation.  
**Gate:** D5.

### ADM-04 — OPEN(k+1) supersedes pending k
Pending k then later cycle OPEN.  
Expected: prior pending invalidated; only current pending cycle can materialize.  
**Gate:** D5.

### ADM-05 — no generic backlog
Attempt to accumulate multiple future pending cycles.  
Expected: bounded frozen behavior/fail-closed cycle lag; no unbounded queue.  
**Gate:** D5.

---

## 7. GerardMM economics

### MM-01 — evaluation day 1
Economic plan resolves SL=2000, TP=1500 USD.  
**Gate:** D5.

### MM-02 — evaluation day 2
Same expected values.  
**Gate:** D5.

### MM-03 — unconfigured evaluation day
Expected: zero new risk, explicit fail-closed reason.  
**Gate:** D5.

### MM-04 — unresolved funded config
`FUNDED_INITIAL` or `FUNDED_STEADY` without configured values.  
Expected: zero new risk; no invented defaults.  
**Gate:** D5.

### MM-05 — account-day objective
`account_day_current_pnl_money=750`, TP=1500.  
Expected remaining objective=750.  
**Gate:** D5.

### MM-06 — target reached before entry
P_day >= TP.  
Expected: no new-risk Order.  
**Gate:** D5.

### MM-07 — loss headroom after prior loss
SL=2000, P_day=-600.  
Expected owner remaining loss budget=1400 before provider min.  
**Gate:** D5.

### MM-08 — prior profit does not enlarge SL
SL=2000, P_day=+1000.  
Expected owner remaining loss budget=2000, not 3000.  
**Gate:** D5.

### MM-09 — other Operation unrealized changes objective
Hold Operation A current PnL constant; vary account-wide PnL due solely to Operation B.  
Expected GerardMM remaining objective changes with account-wide P_day. No portfolio reconstruction inside MM.  
**Gate:** D5.

### MM-10 — dynamic target mark
Given exact Q, mark and point value, verify target mark formula and conservative tick rounding. Change account-wide PnL and/or quantity; expected target recomputes.  
Assert target is not persisted authority.  
**Gate:** D5.

### MM-11 — initial sizing exactness
Given technical stop, budget, Contract units and provider restrictions, verify exact quantity.  
If quantity invalid/denied, no silent clipping.  
**Gate:** D5.

### MM-12 — adverse branch bounded
Trigger adverse branch through configured stages.  
Expected bounded exact adds, mutual branch lock, no inter-Operation state.  
**Gate:** D5.

### MM-13 — favorable branch bounded
Symmetric favorable branch behavior.  
**Gate:** D5.

### MM-14 — partial add no top-up
Proposed add Q receives partial Fill q<Q.  
Expected branch attempt consumed according to frozen config; no compensating top-up Order.  
**Gate:** D5.

### MM-15 — protective stop never loosens
Apply initial stop, favorable protection, adverse/favorable add scenarios.  
Expected effective protection moves only toward lower risk.  
**Gate:** D5.

### MM-16 — provider denied add
Provider denies/revalidation invalidates add.  
Expected no physical command; MM/provider lock semantics prevent forbidden continued new-risk progression.  
**Gate:** D5.

### MM-17 — profit termination precedence
Account-day objective reached while add trigger also true.  
Expected termination wins; no add.  
**Gate:** D5.

### MM-18 — stale economic snapshot
Required P_day absent/stale/wrong currency without deterministic conversion.  
Expected new risk fail closed; existing exit/safety path remains available subject to its own gates.  
**Gate:** D5.

---

## 8. Local executable exposure

### EXP-01 — two concurrent REDUCE Orders
Operation exposure E. Two reductions arrive before either fills.  
Expected sum of live opposing `q_exec_max` claims never exceeds safe reducible exposure.  
**Gate:** D5.

### EXP-02 — EXIT + ForceClose
Full EXIT outstanding, then ForceClose.  
Expected no second full close capable of reversing the Operation.  
**Gate:** D5.

### EXP-03 — partial Fill transfers claim
Reducing Order partially fills.  
Expected logical exposure and remaining q_exec claim update exactly; no optimistic release.  
**Gate:** D5.

### EXP-04 — cancel request race
Cancel requested but venue may still fill.  
Expected claim remains until authoritative finality/quantity reduction. Late Fill is applied.  
**Gate:** D5.

### EXP-05 — modify decrease
Requested lower remaining qty.  
Expected local/provider release only after authoritative accepted decrease.  
**Gate:** D5.

### EXP-06 — modify increase
Expected exact delta must pass local safety and provider reservation before authorization.  
**Gate:** D5.

### EXP-07 — replace overlap
Old and replacement legs can both execute temporarily.  
Expected safety envelope includes both until old leg final.  
**Gate:** D5.

### EXP-08 — no silent resize
Propose quantity above safe/admissible exact grant.  
Expected deny; no auto-reduced command.  
**Gate:** D5.

---

## 9. Provider account-wide capacity

### PRV-01 — GROSS reservation
Two AccountStrategies concurrently reserve on same account.  
Expected serialized account owner prevents combined reachable gross exposure beyond cap.  
**Gate:** D5.

### PRV-02 — NET_ABS opposite exposure
Construct opposite firm Operations and a new Order where current net looks safe but a valid ordering of outstanding Orders enlarges reachable absolute exposure.  
Expected reservation denies unsafe exact grant.  
**Gate:** D5.

### PRV-03 — exits under NET_ABS
Two “reducing” Orders on opposite logical Operations can increase account net absolute exposure depending on execution ordering.  
Expected both participate in capacity envelope; semantic EXIT label does not bypass.  
**Gate:** D5.

### PRV-04 — GROUP_WEIGHTED
Use configured product-group weights and concurrent grants.  
Expected exact typed weighted cap.  
**Gate:** D5.

### PRV-05 — Fill reservation transfer
Fill consumes reserved executable quantity into firm exposure without widening envelope.  
**Gate:** D5.

### PRV-06 — stale grant vs new RuleSet
Obtain reservation, hot-update RuleSet/cap, then request final revalidation.  
Expected final authority wins. Invalid grant never crosses M1.  
**Gate:** D5.

### PRV-07 — exact grant revalidation always traverses provider owner
Exercise “authority appears unchanged”.  
Expected `ReservationRevalidate` still sent; no local skip optimization.  
**Gate:** D5 contract/component assertion.

### PRV-08 — egress authorization boundary
After VALID revalidation assert grant state becomes `egress_authorized`.  
Verify no test/API names this transition `egress_committed`.  
Command is not yet physically submitted.  
**Gate:** D5.

### PRV-09 — Position mismatch
Venue Position differs materially from attributable Echo state.  
Expected provider new risk fail closed where capacity trust requires it; no Position-to-Operation attribution.  
**Gate:** D5.

### PRV-10 — cap lowered below existing exposure
Hot cap below current firm exposure.  
Expected new enlarging risk denied, over-limit visible, no automatic liquidation unless explicit typed rule says flatten.  
**Gate:** D5.

### PRV-11 — complete RuleSet read-only to MM
Populate a RuleSet field not currently used by GerardMM.  
Expected it is still present in read-only MM/account context; provider owner remains enforcement authority.  
**Gate:** D5 schema/contract.

---

## 10. ForceClose and terminality

### TERM-01 — ForceClose is intent
Deliver ForceClose with nonzero exposure.  
Expected Operation non-terminal, termination intent recorded.  
**Gate:** D5.

### TERM-02 — terminal guards
Only after exposure=0 + no live Orders + termination intent => terminal.  
Exercise each missing guard independently.  
**Gate:** D5.

### TERM-03 — bridge down
ForceClose while execution edge down.  
Expected pending termination/readiness alert; no synthetic success.  
On reconnect: reconciliation first, then continue closure.  
**Gate:** D5 integration.

### TERM-04 — direction immutable
Inject anomalous physical Fill crossing through zero.  
Expected Fill preserved, exposure invariant breach visible, Operation direction unchanged, no synthetic reversal Operation.  
**Gate:** D5.

### TERM-05 — terminal Operation not revived
After terminal state, late physical fact arrives.  
Expected fact preserved/reconciliation surfaced according to contract; aggregate not revived.  
**Gate:** D5.

---

## 11. Execution M1/M2

### EXE-01 — M1 state/command atomicity
Crash before/after checkpoint around command egress.  
Expected no visible command without corresponding committed Core state; no duplicate visible command from recovery.  
**Gate:** D5 integration + D6 config certification.

### EXE-02 — Sim normal submit
Core -> Kafka -> Futures Bridge -> SimExecutionAdapter -> normalized observations -> Core.  
Expected one physical-sim Order.  
**Gate:** D5 integration.

### EXE-03 — fast MARKET Fill before ACK
Expected Fill preserved and correlated; Order state converges later.  
**Gate:** D5.

### EXE-04 — physical side effect then crash
Persist SUBMITTING, simulated side effect occurs, bridge crashes before ACK/offset.  
Restart/redelivery must reconcile same client_order_id and suppress second physical submit.  
**Gate:** D5 SimExecution; D6 real adapter.

### EXE-05 — ambiguous submit
Simulate post-SUBMITTING uncertainty with no authoritative proof of existence/absence.  
Expected journal AMBIGUOUS, account new risk OFF, no blind retry.  
**Gate:** D5.

### EXE-06 — definite reject
Authoritative “not accepted” response.  
Expected physical rejection terminal according to adapter contract; no Fill fabricated.  
**Gate:** D5.

### EXE-07 — cancel/fill race
Cancel accepted/requested while Fill races.  
Expected Fill preserved; finality waits for authoritative terminal evidence + executions.  
**Gate:** D5.

### EXE-08 — replace
Test native/atomic/cancel+new according to adapter capability.  
Expected stable action IDs, exact physical identities, no hidden atomicity claim.  
**Gate:** D5 Sim; D6 selected adapter capability-specific.

### EXE-09 — reconnect barrier
Disconnect with working Orders, reconnect.  
Expected new risk OFF until auth/binding/subscriptions/journal/open orders/fills/Position/mismatch reconciliation complete. No auto-resubmit.  
**Gate:** D5.

### EXE-10 — manual order/activity
Inject unknown physical order/Position change.  
Expected observation/mismatch only; no Echo Operation/Fill attribution.  
**Gate:** D5.

### EXE-11 — duplicate Fill realtime/history
Same native execution identity arrives via realtime then history.  
Expected one Fill fact.  
**Gate:** D5.

### EXE-12 — adapter without stable execution identity
Capability UNKNOWN/unsupported.  
Expected exact V1 physical execution eligibility false. No heuristic identity.  
**Gate:** D5 contract.

### EXE-13 — hot physical binding change
Live Order on old binding; Account current binding switches.  
Expected old Order reconciles on old pinned binding; new submits only after new binding ready; no silent remap.  
**Gate:** D5.

### EXE-14 — double-owner detection
Attempt two bridge owners for same physical binding.  
Expected config/telemetry fail-visible and new-risk safety response; V1 does not claim automatic fencing.  
**Gate:** D6 operational.

---

## 12. Recovery / projection

### REC-01 — Core normal restart
Live Operation/MM state + partial fills + pending Orders. Restart runtime.  
Expected state from checkpoint/Kafka; PG projection is not queried as recovery authority.  
**Gate:** D5.

### REC-02 — projector idempotency
Redeliver operation/fill facts to PG projector.  
Expected one logical row/fact, stale `operation_event_seq` ignored safely.  
**Gate:** D5.

### REC-03 — cold recovery missing evidence
Remove required execution checkpoint/authority.  
Expected fail-visible `COLD_RECOVERY_REQUIRED`; no reconstructed trading state from projections.  
**Gate:** D5.

### REC-04 — run provenance isolation
LIVE/REPLAY/BACKTEST facts with run provenance cannot cross-contaminate authoritative state.  
**Gate:** D5.

---

## 13. Scale/correctness scenarios

### SCL-01 — 200 Account fan-out topology
One Strategy evaluation emits one Signal delivered to 200 AccountStrategies.  
Assert:
- one Strategy evaluation;
- one shared indicator/bar computation;
- 200 account deliveries/MM decisions;
- no 200x market subscription/indicator multiplication.  
**Gate:** D5 structural; D6 measured.

### SCL-02 — account isolation
Heavy/blocked Account A must not mutate Account B state or provider reservations.  
**Gate:** D5.

### SCL-03 — reconnect storm
Restart bridge with target test population and nonterminal journals.  
Expected bounded/recoverable reconciliation with no blind submit; latency/resource target measured in D6.  
**Gate:** D6.

---

## 14. KISS/YAGNI regression assertions

Static/review gates must prove no V1 implementation introduces these concepts without a separately approved architecture change:

- DecisionObservation;
- BarObservation;
- generic saga/workflow;
- global event sequencer;
- global coordinator;
- WIND_DOWN;
- max_admissible_qty;
- HARD_CAP_WINS / generic hard-cap override;
- generic liquidation override;
- inter-Operation martingale;
- provider-specific MoneyManagement classes;
- Strategy profit target;
- arbitrary pending-cycle backlog;
- automatic cross-host execution takeover;
- generic Bridge/plugin framework.

**Gate:** every D5 shot code review.

---

## 15. D6 certification carry

The following cannot be honestly certified by D5 unit/component tests alone and remain explicit D6 gates:

- actual StateFun/Kafka EXACTLY_ONCE/read_committed configuration behavior;
- golden exact replay against a recorded run;
- 100–200 account capacity/resource benchmark;
- M2 journal physical durability/fsync/corruption/restart semantics;
- selected real adapter native idempotency/lookup/history/finality identity semantics;
- authorized host/provider-program entitlement for that adapter;
- reconnect/outage longer than normal realtime gap;
- consumer/topic overhead and reconnect storm;
- physical latency distributions at the measurement points defined by the performance budget.

No D5 test may relabel these as physically certified from mocks alone.
