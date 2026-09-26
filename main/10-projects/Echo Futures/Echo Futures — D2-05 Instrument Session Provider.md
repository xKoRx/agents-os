---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo Futures]]"
  - "[[Echo Futures — D1 Analysis Pack]]"
  - "[[Echo Futures — D2-04 Operation Order Fill Position]]"
  - "[[Echo Futures — D2-05A Instrument Contract]]"
  - "[[Echo Futures — D2-05B Session Calendar]]"
  - "[[Echo Futures — D2-05C Provider Program Rules]]"
aliases:
  - Echo Futures D2-05
  - EF Instrument Session Provider
tags:
  - kind/doc
  - area/echo
  - echo-futures
  - architecture-design
created: "2026-09-26"
updated: "2026-09-26"
---

# Echo Futures — D2-05 Instrument Session Provider

> [!info]+ D2-05 integrated authority candidate
> Submanager integration of D2-05A Instrument/Contract, D2-05B Session/Calendar and D2-05C Provider/Program/RuleSet. Echo physical baseline: 372af59a7b83604781346613da01e3d510ea1360, verified unchanged. This artifact is a manager-review candidate only: it does not close D2-05, D2 or advance D2-06.

## 1. Executive verdict

D2-05 STATUS = READY_FOR_MANAGER_REVIEW.

Q6, Q7 and Q10 have one coherent V1 model without contaminating Strategy or reopening D2-01..04:

    Strategy
      -> Signal(instrument_id)
      -> fan-out AccountStrategy
      -> account/provider admission
      -> resolve execution Contract
      -> Operation(contract_id pinned)
      -> MoneyManagement
      -> provider order admission
      -> Order / Fill

Three authorities remain deliberately separate:

- Instrument/Contract: what economic thing and physical expiry is traded.
- ExchangeCalendar/Session: when the market/session exists and what session_date an event belongs to.
- ProviderProgram/RuleSet + Account DayBoundary: what an execution Account is allowed to do and how provider/account safety is evaluated.

No automatic rollover, calendar microservice, provider DSL, generic revision framework or provider-config mega-object is introduced.

OWNER_DECISIONS_REQUIRED = NONE.

## 2. Minimal entity model

    Instrument 1 -> N Contract
    Instrument + mapping purpose/context -> current Contract

    Contract 1 -> N ContractExternalIdentifier

    ExchangeCalendar 1 -> N resolved ExchangeSession
    ExchangeCalendar 1 -> N NamedTradingWindow

    Provider 1 -> N ProviderProgram
    ProviderProgram 1 -> N ProgramPhase
    ProgramPhase -> stable rule_set_id
    rule_set_id 1 -> N ProviderRuleSet versions

    Account -> ProviderProgram + phase_key + execution_binding + DayBoundary
    AccountStrategy -> Account + Strategy + MoneyManagement

    Operation -> Instrument + pinned Contract
    Order/Fill -> pinned Contract inherited from Operation

Provider is business/policy authority; execution_binding is transport/capability. Neither belongs inside Strategy.

## 3. Identities and cardinalities

### Instrument

Stable economic identity: instrument_id + canonical_symbol + currency + exchange_calendar_id. Futures V1 examples are NQ/ES/CL. No generic asset taxonomy is required.

### Contract

Physical expiry identity: contract_id owned by Instrument, with contract_code/month and economic/execution specs. One Instrument has many historical/future Contracts; only a context mapping selects the current one.

### External identifier

ContractExternalIdentifier maps contract_id to a vendor/platform namespace and purpose. CME symbol, Databento identifier, ProjectX contractId and NinjaTrader string are external identifiers, not Echo identity.

### Provider domain

ProviderProgram belongs to one Provider. ProgramPhase is a child config identified by (provider_program_id, phase_key), because materially different phases can have different rules but no global Phase aggregate is needed. ProviderRuleSet versions are explicit only inside this domain.

### Account binding

Account stores provider_program_id, phase_key, execution_binding_id, Account DayBoundary semantics and operational state. AccountStrategy remains exactly Account + Strategy + MM.

## 4. Instrument / Contract / identifier mapping

Use one bounded InstrumentContractMapping:

    instrument_id
    mapping_purpose = MARKET_DATA | EXECUTION
    context_id
    -> contract_id

context_id is the market-data binding for MARKET_DATA or execution_binding_id for EXECUTION.

Then resolve the physical/native name separately:

    contract_id + namespace + purpose + binding_context
    -> external_identifier

This allows feed X and execution Y to refer to the same Contract without Strategy knowing either native identifier.

No implicit fallback across contexts is allowed.

## 5. Hot rollover resolver semantics

Owner manual V1:

1. OPEN is admitted for AccountStrategy.
2. Core resolves the Account execution_binding_id.
3. ContractResolver obtains the current EXECUTION mapping for Signal.instrument_id + execution binding.
4. Missing/disabled/malformed Contract or required identifier fails closed before materialization.
5. Operation is created and pins contract_id.
6. Operation embeds only effective Contract specs required by D2-04/MM.

Hot mapping updates are prospective:

    NQ -> NQZ6
    Operation A => NQZ6
    owner update NQ -> NQH7
    Operation A remains NQZ6
    next Operation B => NQH7

An OPEN delivered while A remains non-terminal is handled by A/MM under D2-04 and therefore continues on NQZ6.

REDUCE/CLOSE/CLOSE_ALL never re-resolve through the current mapping. If the venue rejects the old Contract, fail visible; never redirect to NQH7.

## 6. Economic unit semantics

Canonical V1 units:

- price: native decimal quoted price.
- tick_size: minimum price increment.
- tick: one tick_size.
- point: price delta unit only, not universal money.
- contract quantity: physical contract count, normalized by quantity_min/quantity_step.
- tick_value: money per tick per contract.
- contract_multiplier: explicit economic multiplier/equivalent.
- currency: explicit money denomination.

No pips in the new canonical domain. MM sizes from pinned Contract specs. Missing currency conversion authority fails visible; no implicit 1:1 conversion.

## 7. ExchangeSession / Calendar

ExchangeCalendar owns:

- IANA timezone.
- recurring weekly sessions.
- recurring maintenance breaks.
- session_date assignment rule.
- dated holiday/closed/early-close exceptions.
- sparse product overrides only where necessary.

ExchangeSession is the resolved runtime result for a date/timestamp: session_date, UTC open/close and open/maintenance intervals.

Precedence is dated exception > product override > recurring base schedule.

No permanent UTC offset and no universal CME formula are allowed.

## 8. Trade/session date semantics

Resolution is:

    event timestamp UTC
      -> IANA local time
      -> recurring session + dated exception
      -> semantic session_date

An overnight session can begin on the prior civil date and still map events to the next session/trade date.

LIVE/REPLAY/BACKTEST must invoke the same calendar resolver with equivalent calendar inputs. Historical runs bind to an explicit calendar dataset/input provenance; this is run provenance, not a generic CalendarVersion framework.

## 9. Provider window overlays

Provider trading windows are overlays, not ExchangeSession mutations.

Example:

    ExchangeSession = OPEN
    ProviderRuleSet = NO_NEW_RISK
    effective result = market open, account cannot add risk

Forced-flat cutoff emits provider safety intent. It does not pretend the exchange closed.

Named Strategy sessions (NY, London, CME_RTH/ETH, custom) are NamedTradingWindow configs resolved over ExchangeCalendar. Strategy references a stable window id, never UTC offsets.

## 10. Provider / Program / Phase / RuleSet

Provider = business/policy owner.

ProviderProgram = real provider product; provider names are not forced into one universal naming enum.

ProgramPhase = provider-program-local phase config because rules can materially differ by phase. It is not a standalone aggregate.

ProviderRuleSet is the sole explicit versioned policy family in D2-05:

    rule_set_id
    version
    provider/program/phase scope
    effective_at / optional retired_at
    typed effective rules
    minimal first-party evidence provenance

Typed V1 rule families:

- trading/allowed-new-risk window + forced-flat;
- permitted/denied Instruments;
- order/account/Instrument contract quantity limits;
- daily loss/trailing drawdown parameters and documented enforcement action;
- automation/copy/hosting capability restrictions where runtime-enforceable;
- overnight/weekend constraints when runtime material.

News/consistency/administrative rules enter the hot path only when Echo has authoritative inputs and a meaningful runtime action. No arbitrary if/then DSL.

## 11. Account binding

Canonical relationship:

    Account
      -> ProviderProgram
      -> phase_key
      -> current ProviderRuleSet authority
      -> execution_binding_id / transport capability
      -> Account DayBoundary

    AccountStrategy
      -> Account
      -> Strategy
      -> MoneyManagement

Current RuleSet version is resolved dynamically. Account does not freeze one forever.

Execution transport capability is independently resolved from execution_binding_id. Platform support is not equivalent to API/developer entitlement; UNKNOWN never becomes ALLOWED by inference.

## 12. Enforcement ownership matrix

| Concern | Authority | Runtime owner |
| --- | --- | --- |
| Strategy direction/intention | Strategy/Signal | Strategy runtime |
| AccountStrategy + MM binding | AccountStrategy | fan-out / Operation owner |
| Exchange open/session/date | ExchangeCalendar | CalendarResolver |
| Provider/program/phase eligibility | Account + ProviderRuleSet | ProviderRuleGate |
| Contract selection | InstrumentContractMapping + Account execution binding | ContractResolver |
| Order quantity proposal | MoneyManagement | Operation owner |
| Provider quantity/exposure cap | ProviderRuleSet | ProviderRuleGate |
| Account daily reset/HWM | Account DayBoundary | Account state evaluator |
| Forced-flat/provider safety | ProviderRuleSet | safety evaluator -> Operation intent |
| Physical order acceptance/fills | venue/adapter | execution adapter |
| Operation terminality | D2-04 Operation | echo/operation only |

### Admission Stage 1 — before Operation

    OPEN Signal
      -> fan-out
      -> AccountStrategy eligibility
      -> Account/Program/Phase RuleGate
      -> exchange/provider window
      -> Contract resolvability
      -> ALLOW | DENY_NEW_RISK

This stage evaluates rules that do not require an MM-proposed Order: account state, automation capability, allowed Instrument, exchange/provider time window and current daily safety state.

DENY_NEW_RISK creates no Operation and records a ProviderRuleDecision with RuleSet provenance.

### Admission Stage 2 — after Operation materialization

D2-04 requires Operation to exist before MM. Therefore quantity/exposure rules are checked after MM proposes an Order but before physical submission.

    Operation CREATED
      -> MM proposes Order
      -> ProviderRuleGate(max contracts/exposure)
      -> ALLOW_ORDER | DENY_ORDER_NEW_RISK

No generic silent clamping. REDUCE/EXIT is not denied merely because an account is already over a newly lowered maximum.

If every entry Order is denied, the Operation follows D2-04's explicit entry-failure termination path; it is not deleted.

### Asynchronous safety

Clock/session boundary, AccountSnapshot, RuleSet update or phase/account-state change can trigger safety without another Strategy Signal.

The safety plane emits ProviderSafetyIntent carrying rule provenance to the Operation state owner. D2-04 registers termination intent, cancels/exits as needed, and reaches TERMINAL only when exposure==0, no live Orders and termination intent exists.

## 13. Hot-update semantics

### Contract mapping

Prospective only. New Operations use the new mapping; live Operations retain pinned Contract.

### Calendar

Live resolver uses new config for future resolution. Already-produced facts/bars are not rewritten. Replay/backtest uses its bound calendar input set.

### ProviderRuleSet

New effective version applies dynamically to:

- new OPEN admission;
- new-risk Order admission on live Operations;
- provider safety on live Operations.

Rule update never mutates Operation.contract_id or MM snapshot.

Safety-sensitive updates trigger re-evaluation of affected live Accounts/Operations immediately. Examples:

- forced-flat moved earlier and cutoff already passed -> termination intent now;
- max exposure lowered below current -> deny increases now, no invented liquidation unless rule explicitly requires it;
- Instrument becomes forbidden -> deny opens/adds, still permit closing old pinned exposure.

## 14. Interaction with D2-04 Operation lifecycle

D2-05 adds guards and safety inputs; it does not redefine Operation.

Materialization remains D2-04: accepted OPEN -> CREATED before MM/Orders.

D2-05 extends materialization prerequisites with Stage-1 provider/account admission and execution Contract resolution.

Operation continues to own:

- direction from Signal;
- pinned contract_id;
- MM snapshot/state;
- Orders/Fills;
- termination state;
- terminal transition.

Provider rules are dynamic external safety authority, not copied into the Operation snapshot.

Minimal provenance:

- Stage-1 ProviderRuleDecision persists provider_program_id + phase_key + rule_set_id/version + reason.
- Operation may stamp the accepted admission decision id as audit metadata only.
- ProviderSafetyIntent extends D2-04 termination provenance with decision_id + ProviderProgram + RuleSet version.
- No generic history/revision system is added.

## 15. LIVE / REPLAY / BACKTEST contract

Shared domain logic across modes:

- same Instrument/Contract identities.
- same Contract economic specs.
- same CalendarResolver/session_date semantics.
- same NamedTradingWindow definitions.
- same typed ProviderRuleSet evaluator when a simulated Account is configured with provider rules.
- same Strategy/Signal/MM/Operation semantics.

Infrastructure can differ. Backtest/replay must inject explicit catalog/calendar/rules inputs as run provenance rather than reading mutable current config mid-run.

No second strategy/MM implementation is allowed.

## 16. Echo V3 REUSE / EXTEND / ADAPT / REPLACE map

| V3 precursor | Disposition | Material evidence |
| --- | --- | --- |
| InstrumentSnapshot | ADAPT + REPLACE domain shape | v3/sdk/domain/snapshots.go · d319d0a3587a3d5ec56ed68911cd60d86b096da8 — useful tick/spec fields; current Broker+CanonicalSymbol identity mixes economic/physical concerns. |
| MMEngineFn | REUSE primitives / ADAPT inputs | v3/core/internal/functions/mm_engine.go · e725ceb0bd056f3312365b96fbd93e6f52fdde5f — sizing primitive; consume pinned Contract units, not pip-universal assumptions. |
| SymbolMappingHandler | REUSE hot-config pattern / REPLACE semantics | v3/gateway/internal/symbol_mapping_handler.go · a9364d4a8e40a13bb4562b2870784545293a39c5 — Hasura→Kafka compacted+tombstone pattern fits; broker-symbol model does not. |
| ConfigCache | REUSE | v3/bridge/internal/config_cache.go · 1f46133344022b1193e15d0566c2f76e4354ff44 — full compacted bootstrap + ready barrier + hot updates. |
| DayBoundaryCache | REUSE account-day primitive / REPLACE as market calendar | v3/core/internal/functions/account_sync.go · b0f8f1ce426ce9f5ac6285bd97a990624bd6ca9e — IANA/reset logic useful; prop_rulesets coupling + UTC 23:00 fallback is not Session/Calendar. |
| ExecutionPolicy | ADAPT / SPLIT | v3/sdk/domain/execution_policy.go · 295f7ea2c6058d05540988eea23c1c2d5e5cfa84 — precursor mixes AccountStrategy, MM and execution knobs; split provider authority out. |
| StrategyConfigFn | REUSE config/state pattern | v3/core/internal/functions/strategy_config.go · b89a9a1a61f71c1e1bae0876504589d5844543cd — do not put provider config into strategy state. |
| typed Automation evaluators | REUSE + EXTEND | v3/core/internal/automation/evaluator.go · bf97b13ae0df7af9644d7fea4f4b6c016f6d4bfc — typed registry proves no DSL required. |
| AutomationEvaluatorFn | REUSE + EXTEND | v3/core/internal/functions/automation_evaluator.go · 9503410ef0af9768b8225a4be735d17a8c115014 — enriched snapshot + exactly-once safety action pattern. |
| AutomationCache | REUSE pattern | v3/core/internal/automation/cache.go · 39a461e3f740a4d5f8403b8336c4c03227abf844 — compacted policy/account assignment cache. |
| ClientConfig AccountState/whitelist | REUSE edge guard / ADAPT authority | v3/sdk/domain/client_config.go · 587eb5c4db63b101c9f6b672230a4a7769d4e02a — defense-in-depth, not canonical provider model. |
| Gateway CloseHandler | REUSE control pattern / ADAPT lifecycle | v3/gateway/internal/close_handler.go · 4972bc50b74b5a550ba5034eca435ba48b3ea51d — close-only/close-all pattern; provider safety must enter D2-04 as termination intent. |
| Gateway control plane | EXTEND | v3/gateway/internal/server.go · 2987db5c5b8b74ff066b8278add3d07410c13bee — retain config/admin plane outside hot market path. |
| legacy prop_rulesets/symbol mappings | REPLACE semantics / migration debt | Useful source data may migrate; legacy shapes are not authority for Futures domain. |

## 17. Migration implications

V1 migration should be additive, not big-bang rewrite:

1. introduce Instrument/Contract/catalog and new hot resolver alongside legacy broker symbol mapping;
2. introduce ExchangeCalendar/NamedTradingWindow without repurposing DayBoundaryCache;
3. introduce Provider/Program/Phase/RuleSet and Account bindings alongside legacy prop_rulesets;
4. adapt fan-out/Operation materialization to Stage-1 admission + Contract pinning;
5. adapt Operation order path to Stage-2 provider admission;
6. adapt existing automation/safety action path to ProviderSafetyIntent -> D2-04 termination intent;
7. retain legacy Forex/CFD mapping until DT-EF-CROSS-MARKET-INSTRUMENT-02; do not force expiry semantics onto it.

No product implementation is performed by D2-05.

## 18. Risks / debts

- Exact expiration/last-trade timestamp source is still non-blocking because V1 rollover is manual; do not invent timestamps.
- Old/inactive Contract closure behavior is transport-specific; fail visible, never remap.
- Cross-currency MM requires a future explicit conversion authority if V1 accounts/instruments need it.
- Provider policies can drift externally; RuleSet provenance exposes the state Echo enforced but does not solve policy ingestion cadence.
- Rules that Echo cannot observe/enforce correctly stay out of hot path.
- Calendar holiday source/import and historical dataset capture are implementation/D2-06 seams, not a reason to add a service now.
- Existing pip-based legacy fields remain migration debt; no new Futures domain field should depend on pips.

## 19. Owner decisions genuinely required

NONE.

No unresolved product/domain ambiguity changes identity, lifecycle or enforcement. Remaining choices are implementation details or explicitly deferred evidence edges.

## 20. Acceptance cases A-H

### A — rollover manual

PASS BY DESIGN. Operation A pins NQZ6. Hot mapping NQ→NQH7 only affects Operation B/new Operations. A never migrates.

### B — feed/execution identifiers differ

PASS BY DESIGN. Instrument NQ is canonical; MARKET_DATA and EXECUTION mappings can resolve the same/different physical context as configured, and ContractExternalIdentifier supplies feed X vs execution Y. Strategy sees neither.

### C — CME open, provider blocks

PASS BY DESIGN. CalendarResolver returns OPEN, Stage-1 ProviderRuleGate returns DENY_NEW_RISK. No Operation is materialized for that AccountStrategy.

### D — forced flat

PASS BY DESIGN. Provider cutoff emits ProviderSafetyIntent. D2-04 registers termination intent; Operation remains non-terminal until exposure is zero and no live Orders remain.

### E — early close

PASS BY DESIGN. Dated calendar exception replaces the session boundary. LIVE and REPLAY using the same calendar input derive identical session_date/boundaries.

### F — account day reset

PASS BY DESIGN. Account DayBoundary updates daily HWM/loss state only. ExchangeSession and Contract remain unchanged.

### G — rule update live

PASS BY DESIGN. Current RuleSet version governs new admissions/order gates immediately and triggers safety re-evaluation. Operation retains pinned Contract/MM snapshot; current provider safety can still act.

### H — old contract edge

PASS BY DESIGN. REDUCE/CLOSE uses Operation.contract_id. Current Instrument mapping is never consulted for that close. Venue rejection is surfaced; no silent remap.

D2-05 remains READY_FOR_MANAGER_REVIEW until Primary Manager + Owner perform the gate.
