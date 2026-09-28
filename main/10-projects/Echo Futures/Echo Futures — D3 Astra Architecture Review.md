---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo Futures]]"
  - "[[Echo Futures Architecture Candidate V1]]"
  - "[[Echo Futures — D2-04 Operation Order Fill Position]]"
  - "[[Echo Futures — D2-05 Instrument Session Provider]]"
  - "[[Echo Futures — D2-06 Market Runtime]]"
  - "[[Echo Futures — D2-07 Execution Runtime]]"
  - "[[Echo Futures — D2-08 Strategy Runtime]]"
  - "[[Echo Futures — D2-09 Blocking Refactors]]"
tags:
  - kind/doc
  - area/echo
  - echo-futures
  - architecture-review
created: "2026-09-28"
updated: "2026-09-28"
---

# Echo Futures — D3 Astra Architecture Review

## 1. Scope / baselines

Single adversarial architecture review of the frozen D2 candidate. This artifact records findings only; it does not repair D2, mutate the Architecture Candidate, start D4, select an external transport, design S2, or design Gerard/hardscalping.

Authorities reviewed:
- [[Echo Futures]]
- [[Echo Futures Architecture Candidate V1]]
- [[Echo Futures — D2-04 Operation Order Fill Position]]
- [[Echo Futures — D2-05 Instrument Session Provider]]
- [[Echo Futures — D2-06 Market Runtime]]
- [[Echo Futures — D2-07 Execution Runtime]]
- [[Echo Futures — D2-08 Strategy Runtime]]
- [[Echo Futures — D2-09 Blocking Refactors]]
- [[Echo Futures — D1 Analysis Pack]] as background authority where needed.

Baselines:
- Agents-OS baseline entering review: `b0cb38fae36dfc8f7098bf9c96d1a7a57a245a0e`
- D2 authoritative gate commit: `57bdfac228d88e8c662b44cdddb665bff4c8ac20`
- Architecture Candidate repair/ratification: `7c628fa8ce9afd91678ac4cf0089613fdf85c367`
- Echo: `xKoRx/echo@372af59a7b83604781346613da01e3d510ea1360`
- Echo baseline check at D3 start: `master` identical to frozen SHA; zero delta.

Review mode: one adversarial pass. No correction loop.

## 2. Executive verdict

The D2 architecture remains coherent in its major boundaries: Strategy is account-agnostic, Operation is the account-specific aggregate, Provider is separated from transport, M1/M2 are explicitly distinct, Market computation is shared rather than multiplied by account, and the execution runtime fails closed where physical correctness cannot be proven.

The adversarial pass found **four material findings**:
- 3 HIGH correctness holes/contradictions;
- 1 MEDIUM replay-contract inconsistency;
- 0 CRITICAL;
- 0 LOW.

The strongest issues are not “missing implementation”. They are cases where the current frozen contracts permit a concrete wrong outcome:
1. multiple simultaneous reduce/exit Orders can collectively over-reduce an Operation even though each individual Order passes the current guard;
2. a deferred future cycle buffers only `OPEN(k+1)`, leaving management Signals for that not-yet-materialized cycle undefined;
3. D2-04 post-terminal Fill handling and D2-05 capacity enforcement contradict each other, allowing a genuine late Fill to create physical exposure without a defined immediate update to `firm_by_operation`.

The replay finding is narrower: the candidate sometimes speaks as if EXACT_REPLAY reproduces MM decisions generally, while the frozen recorded boundary explicitly excludes execution-domain inputs that can trigger MM. D4 can resolve this either by narrowing the guarantee or by recording normalized execution facts as replay inputs without re-executing the venue.

No finding in this review establishes a need for a Core rewrite, global event sourcing, a portfolio aggregate, automatic cross-host takeover, or a change to the frozen Provider/transport split.

ASTRA REVIEW COMPLETE

## 3. Architecture strengths relevant to validation

- State ownership is mostly explicit and single-writer by key.
- `Strategy -> Signal -> AccountStrategy -> Operation -> Order -> Fill` is materially cleaner than the legacy Reference path.
- `Position != Operation` and the three-path execution routing prevent fabricated Operation attribution.
- Stage-1 provider admission is correctly linearized account-keyed instead of relying on eventual kache state.
- M1 and M2 are separated, and the adapter is forbidden from blind retry after ambiguous physical submit.
- Market ingestion/bars/Strategy evaluation are not multiplied by account.
- Replay distinguishes a real run replay from a synthetic historical backtest.
- KISS/YAGNI discipline is visible: no global saga, no workflow engine, no invented rule DSL, no automatic rollover.

## 4. Findings ordered by severity

### D3-ASTRA-01

**ID:** D3-ASTRA-01  
**SEVERITY:** HIGH  
**AREA:** Operation / Order / Fill  
**CLAIM:** The frozen Operation contract permits multiple live Orders, while REDUCE/EXIT construction validates only each individual Order against current logical exposure. There is no Operation-level reservation of already-outstanding reducing quantity.  
**WHY IT IS A PROBLEM:** Two or more concurrently live reducing Orders can each be locally valid when created and collectively sell more quantity than the Operation owns. The resulting sign flip is not a venue anomaly; it can be generated by valid Core decisions under the documented rules.  
**BROKEN INVARIANT:** Operation direction is immutable; REDUCE/EXIT is intended to reduce/close exposure rather than create opposite exposure. The architecture should not create `EXPOSURE_INVARIANT_BREACH` through its own valid concurrent commands.  
**CONCRETE FAILURE SCENARIO:** Operation LONG +2. MM emits EXIT SELL 2 (Order A), still WORKING. Before A fills/finalizes, another trigger emits REDUCE/EXIT SELL 2 (Order B). Both individually satisfy `qty <= logical_exposure(2)` at construction. A and B both fill. Logical exposure becomes -2 and the system enters an invariant breach caused by its own accepted Orders. Provider Stage-2 does not solve this because exits explicitly do not require a new-risk reservation.  
**EVIDENCE:** D2-04 allows `Operation 1 -> 0..N Orders`, explicitly allows multiple live Orders, and defines REDUCE/EXIT validation as opposite side with `qty <= logical_exposure` at construction. D2-05 says an exit Fill updates capacity but an exit intent does not reserve/release firm capacity; “un Fill de salida no necesita reserva previa.”  
**AFFECTED AUTHORITY:** [[Echo Futures — D2-04 Operation Order Fill Position]]; [[Echo Futures — D2-05 Instrument Session Provider]]; [[Echo Futures Architecture Candidate V1]].  
**D2 DECISION CHALLENGED:** Order concurrency + reduction guard semantics. Not the one-Operation invariant itself.  
**MINIMUM CORRECTION DIRECTION:** Define an Operation-local reducing-quantity reservation/availability invariant across all live REDUCE/EXIT Orders, or an equivalent serial rule that proves aggregate outstanding reduce quantity cannot exceed reducible exposure. Do not rely on provider new-risk capacity to solve an Operation-local invariant.  
**BLOCKS V1? YES**  
**CONFIDENCE:** HIGH  
**TYPE:** FACT + INFERENCE from two frozen contracts.

### D3-ASTRA-02

**ID:** D3-ASTRA-02  
**SEVERITY:** HIGH  
**AREA:** Strategy runtime / cycle lag  
**CLAIM:** The one-cycle lag mechanism specifies storage for `pending_next_cycle_open`, but does not define what happens to subsequent management Signals belonging to that same future cycle before its Operation materializes.  
**WHY IT IS A PROBLEM:** Strategy is explicitly allowed to keep advancing technically while an account is physically behind. Once `OPEN(k+1)` is deferred, Strategy can still emit `REDUCE/CLOSE/CLOSE_ALL(k+1)` before Operation(k) becomes TERMINAL. Those Signals must neither mutate Operation(k) nor be silently lost, but the frozen contract only buffers the OPEN.  
**BROKEN INVARIANT:** Signals from another cycle must never mutate the current Operation; the account-specific materialization must reflect the actual technical state of the cycle when it finally catches up; the bounded-lag design must not require an unbounded queue.  
**CONCRETE FAILURE SCENARIO:** Strategy emits `CLOSE_ALL(k) -> OPEN(k+1)`; account is slow closing k, so OPEN(k+1) is buffered. Strategy then emits `CLOSE_ALL(k+1)` before k reaches TERMINAL. If that close is dropped because no k+1 Operation exists, the buffered OPEN later materializes stale risk after the Strategy has already closed k+1. If it is queued verbatim, repeated same-cycle management Signals create the unbounded backlog the design explicitly tries to avoid.  
**EVIDENCE:** D2-08 freezes one buffered `pending_next_cycle_open`, says Signals of another cycle never mutate the current Operation, allows Strategy to advance independently of physical accounts, and caps lag at one future cycle. No canonical state/reduction rule is given for non-OPEN Signals of the buffered cycle.  
**AFFECTED AUTHORITY:** [[Echo Futures — D2-08 Strategy Runtime]]; [[Echo Futures Architecture Candidate V1]].  
**D2 DECISION CHALLENGED:** Single deferred future cycle semantics, not `strategy_cycle_seq` itself.  
**MINIMUM CORRECTION DIRECTION:** Define bounded pending-cycle state semantics. At minimum, later Signals for the deferred cycle must deterministically transform/cancel the pending future intent (for example, CLOSE_ALL invalidating a pending OPEN) without mutating the current Operation and without introducing an unbounded event backlog. Exact mechanics belong to D4.  
**BLOCKS V1? YES**  
**CONFIDENCE:** HIGH  
**TYPE:** FACT + concrete lifecycle gap.

### D3-ASTRA-03

**ID:** D3-ASTRA-03  
**SEVERITY:** HIGH  
**AREA:** Fill / post-terminal handling / Provider capacity  
**CLAIM:** D2-04 and D2-05 make incompatible promises for a genuinely new late Fill arriving after an Operation is TERMINAL. D2-04 says the Fill does not revive or mutate the terminal Operation and goes to a late-event breach path; D2-05 says every late/reconciled Fill produces a cumulative `CapacityStateUpdate` from the Operation owner so `firm_by_operation` remains authoritative.  
**WHY IT IS A PROBLEM:** After terminal cleanup, the documented source for cumulative Operation exposure no longer changes, yet the physical Fill can create new exposure. Provider capacity may therefore remain at zero/stale until a separate Position mismatch path detects the divergence. During that interval new risk can be admitted against incorrect firm capacity unless another explicit fail-closed signal exists.  
**BROKEN INVARIANT:** Provider shared-cap enforcement must account for known executed exposure; `firm_by_operation + live_reservations` is declared authoritative for enforcement. Known physical execution must not leave that authority silently stale.  
**CONCRETE FAILURE SCENARIO:** Operation A closes and becomes TERMINAL at logical exposure 0; its provider capacity state is cleaned or remains 0. Later a genuinely new Fill for A arrives and creates +1 physical contract. D2-04 records `POST_TERMINAL_EXECUTION_BREACH` but does not mutate A. The D2-05 cumulative update cannot be derived from A’s unchanged exposure. Before the next complete Position snapshot/mismatch barrier, Stage-1/Stage-2 can see capacity that omits the +1.  
**EVIDENCE:** D2-04 R13/case E: genuine new post-terminal Fill is preserved as a fact + breach, A does not revive and current Operation is untouched. D2-05 R16: “después de todo Fill Echo — ... late/reconciled Fill — echo/operation emite un update cumulativo” and provider_rules stores `firm_by_operation`. These cannot both be literally true for a post-terminal Fill that is intentionally outside aggregate mutation.  
**AFFECTED AUTHORITY:** [[Echo Futures — D2-04 Operation Order Fill Position]]; [[Echo Futures — D2-05 Instrument Session Provider]]; [[Echo Futures Architecture Candidate V1]].  
**D2 DECISION CHALLENGED:** Cross-boundary capacity behavior after post-terminal execution breach. Not the decision that TERMINAL Operations do not revive.  
**MINIMUM CORRECTION DIRECTION:** Define a fail-closed enforcement path for post-terminal execution facts that does not revive lifecycle but immediately prevents undercounted capacity—e.g. dedicated physical-exposure debt/hold in provider_rules or an explicit `PHYSICAL_STATE_UNTRUSTED` update before admitting new risk. D4 must reconcile the cumulative-update wording.  
**BLOCKS V1? YES**  
**CONFIDENCE:** HIGH  
**TYPE:** FACT; direct contradiction between frozen workstreams.

### D3-ASTRA-04

**ID:** D3-ASTRA-04  
**SEVERITY:** MEDIUM  
**AREA:** EXACT_REPLAY / MM boundary  
**CLAIM:** The integrated candidate sometimes states the determinism property as “same ordered inputs => same decisions (MM/Strategy)”, while D2-06 explicitly defines EXACT_REPLAY as a market/runtime recording and places Operation/Order/Fill/physical execution recovery outside that replay boundary. MM, however, is explicitly triggered by execution facts such as Fill and OrderStatusEvent.  
**WHY IT IS A PROBLEM:** A replay cannot generally reproduce execution-triggered MM decisions unless the normalized execution facts observed in live are included as deterministic replay inputs. Re-executing the venue is not required, but omitting the facts narrows the guarantee.  
**BROKEN INVARIANT:** A declared replay guarantee must name the full input set required by the deterministic function it claims to reproduce.  
**CONCRETE FAILURE SCENARIO:** Live MM receives Fill F, mutates `mm_state`, and emits an ADD/protection Order. Market recording is complete, but EXACT_REPLAY does not replay execution-domain F. Strategy decisions reproduce; the MM branch after F does not. A report claiming general “same MM decisions” would therefore be false for this run.  
**EVIDENCE:** D2-08: MM triggers include OrderStatusEvent/OrderActionResult/Fill. D2-06 §18–22 records market/runtime inputs and states Operation/Order/Fill/physical execution effects and recovery remain outside market replay. Architecture Candidate §10 scopes execution domain out, while also expressing a broad deterministic property for MM/Strategy.  
**AFFECTED AUTHORITY:** [[Echo Futures — D2-06 Market Runtime]]; [[Echo Futures — D2-08 Strategy Runtime]]; [[Echo Futures Architecture Candidate V1]].  
**D2 DECISION CHALLENGED:** Wording/scope of EXACT_REPLAY guarantee, not the decision to avoid physical venue re-execution.  
**MINIMUM CORRECTION DIRECTION:** Either narrow EXACT_REPLAY’s V1 guarantee explicitly to market/Strategy (and any MM decisions driven only by recorded inputs), or include normalized execution facts as recorded deterministic inputs for MM replay while still keeping physical submission out of replay.  
**BLOCKS V1? NO**  
**CONFIDENCE:** HIGH  
**TYPE:** FACT + contract inconsistency.

## 5. Challenged invariants

| Invariant | Result |
|---|---|
| Max 1 non-terminal Operation per AccountStrategy | Preserved structurally; D3-ASTRA-02 challenges deferred-cycle semantics around it. |
| Operation direction immutable | Structurally preserved; D3-ASTRA-01 shows valid concurrent exits can still generate opposite exposure. |
| Provider capacity reflects executed risk | Challenged by D3-ASTRA-03. |
| Exact replay reproduces declared deterministic decisions | Needs scope normalization per D3-ASTRA-04. |
| Fill identity native/stable | No material D3 finding. |
| Position never fabricated into Operation | No material D3 finding. |
| M1/M2 separation | No material D3 finding. |
| No automatic cross-host takeover | No material D3 finding. |
| Market computation not multiplied by account | No material D3 finding. |
| Provider != transport | No material D3 finding. |
| Instrument != Contract / Operation pins Contract | No material D3 finding. |

## 6. Cross-finding interactions

- D3-ASTRA-01 and D3-ASTRA-03 both expose the same safety principle from opposite sides: logical aggregate correctness and provider account-wide capacity must fail closed when actual executable exposure can exceed the locally expected amount.
- D3-ASTRA-02 can amplify D3-ASTRA-01 if a stale deferred OPEN materializes after the Strategy has already issued a close for that future cycle.
- D3-ASTRA-04 is independent of live correctness, but if D3-ASTRA-01/02/03 are later fixed, their new deterministic inputs/state transitions must be represented consistently in replay/backtest contracts.

## 7. Areas reviewed with no material finding

No material finding was established against:
- Strategy being account-agnostic and evaluated once before fan-out;
- `Signal.details` remaining Strategy-specific instead of expanding into a universal mega-schema;
- MM state ownership inside `echo/operation`;
- Instrument/Contract split and prospective manual rollover;
- ExchangeCalendar vs Provider windows vs Account DayBoundary separation;
- Provider/Program/RuleSet modeling with typed rules and no DSL;
- Futures Bridge sibling + internal ExecutionAdapter;
- M1 StateFun/Kafka boundary as an implementation-required guarantee rather than an existing capability;
- M2 write-ahead journal / no blind retry / ambiguous fail-closed;
- three-path execution routing;
- no automatic cross-host takeover;
- Q16 conclusion that a Core rewrite is not required;
- 100–200 account target being structurally possible without feed/bar/Strategy work multiplying by account.

## 8. Unresolved evidence gaps

No evidence gap blocks this D3 review.

D6 still owns physical certification of:
- real external transport M2 capabilities;
- native execution identity/history horizon;
- Kafka EXACTLY_ONCE/read_committed deployment semantics;
- M2 journal store fsync/corruption behavior;
- 100–200 account throughput/reconnect pressure.

Those are known implementation/certification obligations, not D3 architecture findings.

## 9. Summary table

| ID | Severity | Area | Blocks V1 | Manager QA |
|---|---|---|---|---|
| D3-ASTRA-01 | HIGH | concurrent REDUCE/EXIT reservation | YES | SUPPORTED |
| D3-ASTRA-02 | HIGH | deferred future-cycle management Signals | YES | SUPPORTED |
| D3-ASTRA-03 | HIGH | post-terminal Fill vs provider capacity | YES | SUPPORTED |
| D3-ASTRA-04 | MEDIUM | EXACT_REPLAY scope for MM | NO | SUPPORTED |

Counts:
- CRITICAL: 0
- HIGH: 3
- MEDIUM: 1
- LOW: 0

## 10. Manager QA disposition

Quality-control performed finding-by-finding against the frozen authorities.

- **SUPPORTED:** D3-ASTRA-01, D3-ASTRA-02, D3-ASTRA-03, D3-ASTRA-04
- **UNSUPPORTED_BY_EVIDENCE:** NONE
- **DUPLICATE:** NONE
- **KNOWN_IMPLEMENTATION_OBLIGATION:** NONE
- **KNOWN_DEFERRED_DEBT:** NONE
- **OWNER_DECISION_REQUIRED:** NONE
- **EVIDENCE_GAP:** NONE

None of the four findings is merely “not implemented yet”:
- 01 is a missing aggregate invariant;
- 02 is an undefined lifecycle state transition;
- 03 is a contradiction between two frozen authorities;
- 04 is a replay-contract scope inconsistency.

No correction was applied in D3.

## 11. D3 gate

```text
D3 STATUS:
READY_FOR_OWNER_REVIEW

EF_D3_ASTRA_PASS:
REVIEW

ARCHITECTURE MUTATED:
NO

D4 STARTED:
NO

OWNER DECISIONS REQUIRED:
NONE
```

Next: Owner review. If accepted, open D4 separately.
