---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo Futures]]"
  - "[[Echo Futures — D1 Analysis Pack]]"
  - "[[Echo Futures — D2-04 Operation Order Fill Position]]"
aliases:
  - Echo Futures D2-05C
  - EF Provider Program Rules
tags:
  - kind/doc
  - area/echo
  - echo-futures
  - architecture-design
created: "2026-09-26"
updated: "2026-09-26"
---

# Echo Futures — D2-05C Provider Program Rules

> [!info]+ TOP C result
> D2-05C — Provider / Program / RuleSet. Design input for D2-05 integration. Echo baseline verified at 372af59a7b83604781346613da01e3d510ea1360 with no delta. No product code was changed.

## 1. Verdict

TOP_C_RESULT = READY_FOR_INTEGRATION.

Provider business identity, ProviderProgram product identity, ProgramPhase and ProviderRuleSet must be explicit and account-scoped, while execution transport remains a separate binding/capability concern. ProviderRuleSet is the only D2-05 domain where explicit version/provenance is justified.

No generic rules DSL, workflow engine or ProviderProgram mega-object is required.

## 2. Minimal model

### Provider

Business/policy owner such as a prop firm.

Minimum fields:

- provider_id: stable internal identity.
- provider_code: stable machine-facing code.
- display_name.
- operational_state: ACTIVE/DISABLED for new account bindings.

Provider is not an adapter, API, broker protocol or technology family.

### ProviderProgram

Real product/program offered by one Provider.

Minimum fields:

- provider_program_id.
- provider_id.
- program_code: provider-specific product identity.
- display_name.
- operational_state.

Do not normalize provider vocabulary into one universal Evaluation/Funded/Live enum. Provider program names remain provider-owned.

### ProgramPhase

Rules can materially change between evaluation, funded simulated and live states, so phase must be represented. KISS: phase is a child config of ProviderProgram, not a global aggregate.

Identity:

    provider_program_id + phase_key

Fields:

- phase_key: provider-local stable key.
- display_name.
- operational_state.
- rule_set_id: stable authority family to resolve for this phase.
- optional next_phase_key only if a real transition flow later needs it; omitted in V1.

No Phase table/entity independent of ProviderProgram is required.

### ProviderRuleSet

A ProviderRuleSet is a typed effective policy snapshot with explicit provenance.

Identity/provenance fields:

- rule_set_id: stable ruleset family identity.
- version: monotonically ordered within rule_set_id.
- provider_id.
- provider_program_id.
- phase_key.
- effective_at.
- retired_at optional.
- source_refs: minimal first-party evidence locators/title/date or durable internal evidence IDs.
- reviewed_at / provenance_note only when needed to explain an exception.

RuleSet versioning is specific to provider policy. It does not create a generic Version/Revision framework for Strategy, AccountStrategy, MM or Contract.

## 3. Typed rule families

Only runtime-enforceable/material families belong in V1.

### TradingWindowRules

Fields may express:

- allowed_new_risk windows.
- forced_flat cutoff(s).
- IANA timezone or named provider window authority.
- overnight/weekend permission when runtime-relevant.

These rules overlay ExchangeCalendar; they never alter it.

### InstrumentPermissionRules

- allowed instrument_ids and/or denied instrument_ids.
- optional provider-program-specific quantity limits per instrument.

Rules use canonical Instrument identity, never vendor symbols.

### ExposureRules

Typed limits such as:

- max_contracts_per_order.
- max_open_contracts_per_instrument.
- max_open_contracts_account-wide when the provider defines one.

The evaluator returns an explicit decision; it does not use an arbitrary expression language.

A hot update that lowers a maximum below current exposure blocks any increase immediately. Existing exposure is not automatically reduced unless the provider rule itself has explicit forced-reduction/forced-flat semantics. Echo does not invent liquidation policy.

### Loss / Drawdown Rules

ProviderRuleSet supplies typed parameters needed by enforcement, for example:

- daily loss threshold and basis.
- trailing drawdown threshold/basis.
- whether the provider semantics require DENY_NEW_RISK only or termination/flatten once breached.

Account daily calculations use Account DayBoundary, not ExchangeSession.

### Automation / Copy / Hosting Restrictions

Runtime-relevant capability rule:

- automation = ALLOWED | FORBIDDEN | CONDITIONAL.
- optional allowed execution capability/transport constraints proven by provider/program/phase evidence.
- copy/multi-account restrictions only when Echo can evaluate the actual condition.

These rules determine whether an Account may be bound/enabled and whether new risk may be admitted. Unknown entitlement is not interpreted as allowed.

### News / Consistency / Administrative Rules

Include only when Echo has both authoritative parameters and runtime inputs to enforce them correctly.

- news blackout may become a typed runtime rule when a canonical event source exists.
- consistency/payout rules that only affect provider economics/reporting stay out of the execution hot path.
- administrative KYC, payout timing, fees and account purchase rules are not ProviderRuleSet hot-path rules.

## 4. Account binding

Execution Account owns provider/program/rule authority; AccountStrategy does not.

Minimum Account-side binding:

    account_id
    provider_program_id
    phase_key
    execution_binding_id
    account_day_boundary_id / effective reset semantics
    operational state

Current ProviderRuleSet version is resolved dynamically from ProviderProgram + phase rule_set_id. Account does not pin a version forever.

AccountStrategy remains:

    Account
    + Strategy
    + MoneyManagement

No provider/program/rules payload is embedded into AccountStrategy.

Execution binding/capability is separate:

    account_id -> execution_binding_id -> adapter/transport capability

A ProviderProgram can therefore be business-compatible while a particular Account transport entitlement is not.

## 5. Rule resolution

ProviderRuleResolver loads the current effective ProviderRuleSet for:

    Account
      -> ProviderProgram
      -> ProgramPhase
      -> rule_set_id
      -> current effective version

Fail closed for new risk when:

- account program/phase binding is missing;
- current ruleset cannot be resolved;
- automation/transport entitlement required by the program is unknown or forbidden;
- rule evaluation needs missing safety-critical account/session inputs.

Closing/reducing existing exposure remains allowed where the execution venue permits it; safety must not be blocked merely because new-risk admission config is incomplete.

## 6. Enforcement boundaries

There are two admission stages plus one asynchronous safety path. This split is required to remain consistent with D2-04, where Operation exists before MM/Orders.

### Stage 1 — pre-materialization admission

Flow:

    Signal OPEN
      -> fan-out
      -> AccountStrategy existence/enabled check
      -> Account + ProviderProgram/Phase RuleGate
      -> Contract/session resolvability
      -> ALLOW | DENY_NEW_RISK

Rules evaluable without an MM order are applied here:

- account/provider operational state;
- automation/transport eligibility;
- permitted Instrument;
- exchange open/provider allowed-new-risk window;
- current daily-loss/drawdown state when semantics say block new risk;
- Account state such as CLOSE_ONLY.

DENY_NEW_RISK means no Operation is created for that AccountStrategy. The decision is recorded with provider_program_id + phase_key + rule_set_id + version + reason.

### Stage 2 — post-materialization order admission

D2-04 then materializes Operation before MM. MM proposes Orders against the pinned Contract.

Before any new-risk Order leaves Core, ProviderRuleGate checks rules that depend on proposed or current quantity/exposure:

- max contracts per order;
- max exposure per Instrument/account;
- provider-specific size constraints.

Result:

- ALLOW_ORDER;
- DENY_ORDER_NEW_RISK.

No silent clamping by the generic gate. If the provider exposes a hard maximum, MM may later consume remaining capacity as an input, but the enforcement boundary still validates the final Order.

If every entry Order of a newly-created Operation is denied, D2-04 resolves the Operation through its normal CREATED/PENDING_ENTRY failure path with explicit provider-admission provenance; it is not silently deleted.

REDUCE/EXIT orders are not rejected by a maximum-exposure rule merely because the account is already over the new maximum.

### Stage 3 — asynchronous provider safety

Rules that can become active without a new Signal must be evaluated on the relevant trigger:

- clock/session boundary;
- AccountSnapshot/equity update;
- ProviderRuleSet hot update;
- account phase/state change.

Examples:

- forced-flat cutoff reached;
- daily/trailing loss rule whose documented action is flatten;
- automation entitlement revoked for the current phase when policy requires trading stop.

The safety plane emits a ProviderSafetyIntent to the D2-04 Operation state owner. It records a termination intent and causes cancel/exit actions according to D2-04. It never marks Operation TERMINAL directly.

## 7. Hot-update semantics

A new ProviderRuleSet version becomes authoritative for subsequent decisions at effective_at.

It applies dynamically to:

- future pre-materialization admission;
- future Order admissions on existing Operations;
- safety evaluation of live Operations.

It does not mutate:

- Operation.contract_id;
- Operation MM snapshot;
- historical ProviderRuleDecision facts.

Safety-sensitive hot updates trigger immediate re-evaluation of affected active Accounts/Operations rather than waiting for the next Strategy Signal.

Examples:

- earlier forced-flat cutoff already passed -> emit safety termination intent now;
- lowered max exposure below current live exposure -> block increases immediately; do not auto-liquidate unless the rule explicitly requires it;
- Instrument newly forbidden -> deny new risk/adds; existing close/reduce continues against pinned Contract.

## 8. Provenance

Minimum durable decision provenance is explicit but bounded.

Every material ProviderRuleDecision records:

- decision_id.
- account_id.
- provider_program_id.
- phase_key.
- rule_set_id.
- rule_set_version.
- decision = ALLOW / DENY_NEW_RISK / ALLOW_ORDER / DENY_ORDER_NEW_RISK / SAFETY_TERMINATION.
- rule_family/reason.
- decided_at.
- operation_id/order_id when they already exist.

When an Operation is created after Stage 1, it may stamp the admission decision identifiers as audit metadata. This is not a frozen provider policy snapshot and does not prevent newer safety rules from acting.

When ProviderSafetyIntent changes a live Operation, its D2-04 termination intent carries decision_id + provider_program_id + rule_set_id + rule_set_version as provenance. No generic Operation history framework is added.

## 9. Rule ownership matrix

| Concern | Authority | Runtime owner |
| --- | --- | --- |
| Strategy direction/intention | Strategy/Signal | Strategy runtime |
| AccountStrategy + MM selection | AccountStrategy | signal fan-out / Operation owner |
| Provider/program/phase eligibility | Account + ProviderRuleSet | ProviderRuleGate |
| Exchange open/session | ExchangeCalendar | CalendarResolver |
| Provider allowed window | ProviderRuleSet | ProviderRuleGate |
| Account daily reset | Account DayBoundary | Account state/account evaluator |
| Proposed Order quantity/exposure | MM proposes; provider caps | Operation owner + ProviderRuleGate |
| Forced flat/provider safety | ProviderRuleSet | safety evaluator -> Operation termination intent |
| Physical execution capability | execution binding/adapter | execution adapter |
| Operation terminality | D2-04 Operation | echo/operation only |

## 10. Echo V3 physical map

| Current piece | Classification | Why |
| --- | --- | --- |
| v3/sdk/domain/execution_policy.go · ExecutionPolicy · blob 295f7ea2c6058d05540988eea23c1c2d5e5cfa84 | ADAPT / SPLIT | It already binds Strategy→ExecutionAccount and risk/execution knobs, but it mixes AccountStrategy, MM and execution details. Extract AccountStrategy/MM; ProviderRuleSet must be account/program authority and has its own justified version. |
| v3/core/internal/functions/strategy_config.go · StrategyConfigFn · blob b89a9a1a61f71c1e1bae0876504589d5844543cd | REUSE PATTERN | Stateful config update/lookup pattern is useful; provider policy should not be stuffed into strategy config. |
| v3/core/internal/automation/evaluator.go · typed RuleEvaluator registry · blob bf97b13ae0df7af9644d7fea4f4b6c016f6d4bfc | REUSE + EXTEND | Strong precursor for typed rule families without DSL. Add provider evaluators/context rather than arbitrary expressions. |
| v3/core/internal/functions/automation_evaluator.go · AutomationEvaluatorFn · blob 9503410ef0af9768b8225a4be735d17a8c115014 | REUSE + EXTEND | Snapshot-driven evaluation and exactly-once action egress fit safety triggers; route resulting provider safety intent through Operation lifecycle. |
| v3/core/internal/automation/cache.go · AutomationCache · blob 39a461e3f740a4d5f8403b8336c4c03227abf844 | REUSE PATTERN | Compacted profile/account assignment cache is a direct pattern for hot ProviderRuleSet resolution. |
| v3/core/internal/functions/account_sync.go · DayBoundaryCache · blob b0f8f1ce426ce9f5ac6285bd97a990624bd6ca9e | ADAPT | Existing daily HWM/reset state is reusable for provider daily rules but legacy prop_rulesets coupling must be split from exchange calendar. |
| v3/sdk/domain/client_config.go · AccountState / whitelist · blob 587eb5c4db63b101c9f6b672230a4a7769d4e02a | REUSE EDGE GUARDS / ADAPT AUTHORITY | ACTIVE/CLOSE_ONLY and edge whitelist are useful defense-in-depth. They are not the canonical ProviderRuleSet. |
| v3/gateway/internal/close_handler.go · CloseHandler · blob 4972bc50b74b5a550ba5034eca435ba48b3ea51d | REUSE CONTROL PATTERN / ADAPT LIFECYCLE | Existing CLOSE_ONLY + close-all command path proves control-plane safety actions, but Futures provider safety must emit D2-04 termination intents to Operation owners rather than directly define terminality. |
| v3/bridge/internal/config_cache.go · ConfigCache · blob 1f46133344022b1193e15d0566c2f76e4354ff44 | REUSE PATTERN | Hot account config bootstrap/update mechanics can carry derived edge guards/capabilities. |
| legacy prop_rulesets table/model | REPLACE SEMANTICS / MIGRATE | Useful data may migrate, but it currently conflates day reset/rules without Provider→Program→Phase→versioned RuleSet provenance. |

## 11. Acceptance semantics

### Provider blocks while exchange open

ExchangeCalendar OPEN + provider Stage-1 window DENY_NEW_RISK => OPEN Signal is rejected for that AccountStrategy before Operation materialization.

### Forced flat

Cutoff trigger emits ProviderSafetyIntent carrying rule provenance. D2-04 Operation records termination intent, cancels/exists as needed, and becomes TERMINAL only after exposure=0 and no live Orders.

### Rule update live

New current RuleSet version is used immediately for new decisions. Existing Operation retains Contract/MM snapshot but is subject to current provider safety constraints.

### Phase change

Account phase_key changes, resolver switches to that ProgramPhase's current RuleSet. AccountStrategy is untouched.

## 12. Risks / non-blocking unknowns

- Some provider rules are contractual/business rules but not algorithmically observable. Keep them outside the hot path until Echo has authoritative runtime inputs.
- Direct API entitlement can differ from platform support. execution_binding capability remains separate and UNKNOWN never becomes ALLOWED by inference.
- Provider policies can change externally without notice. Operational ingestion/review cadence is implementation/governance scope; explicit RuleSet provenance makes drift visible.
- A provider-specific forced-reduction rule can be added as a typed exception when first-party evidence requires it; do not generalize it preemptively.

OWNER_DECISIONS_REQUIRED = NONE.
