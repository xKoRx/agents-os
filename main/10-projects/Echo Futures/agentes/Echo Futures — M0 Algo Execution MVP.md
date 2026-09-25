---
type: project
schema_version: 1
owner: agent
root: false
status: active
priority: P1
area: "[[Echo]]"
parent: "[[Echo Futures]]"
sprint: 2026-09-25--2026-09-27
start: 2026-09-25
due: 2026-09-27
progress: 0
repo: "xKoRx/echo-futures"
aliases:
  - Echo Futures Algo MVP
tags:
  - kind/project
  - area/echo
  - echo-futures
  - execution
  - algo-trading
created: "2026-09-25"
updated: "2026-09-25"
---

# Echo Futures — M0 Algo Execution MVP

## Goal

Build the smallest runnable algorithmic-trading vertical slice that can execute the same deterministic strategy and position-management code in replay and provider-authorized live/shadow environments, with provider rules fail-closed.

M0 is NOT production multi-prop, not a frontend, and not real-money authorization.

## Architecture freeze

```text
MarketDataSource
    |
    v
Strategy
    |
    v
TradeIntent
    |
    v
PositionManager
    |
    v
ManagedIntent
    |
    v
PortfolioCoordinator
    |
    +--> AccountState + PropPolicy/ComplianceGuard
    |          |
    |          v
    |      SizedOrderIntent
    |
    v
ExecutionVenue
    |
    +--> ProjectXAdapter
    +--> NinjaTraderBridgeAdapter
    +--> future Rithmic/Tradovate adapters
    |
    v
Order/Fill/Reconciliation Events
    |
    +--> AccountState
    +--> EventJournal
    +--> Metrics
```

### Hard separations

**Strategy** knows market state and emits an intent. It does not know Topstep/Lucid, evaluation/funded state, balances, payout rules, account count, or transport credentials.

**PositionManager** owns deterministic intra-position behavior: HOLD, ADD_ADVERSE, ADD_FAVORABLE, MOVE_STOP, MOVE_TARGET, EXIT. Hardscalping/recovery belongs here, never inside a provider adapter.

**InterTradeRiskPolicy / AccountPolicy** maps account stage and prior results into risk/sizing. P150-style EVAL/BULTO/QUALIFY/RELOAD behavior belongs here.

**PropPolicy / ComplianceGuard** owns firm/plan constraints and must fail closed. It is pure domain logic where possible and versioned by captured rule set.

**ExecutionVenue** only translates normalized order intents into a technical transport and reconciles broker/provider state. A venue is not a prop firm.

**AccountBinding** joins `provider + plan + account + executionVenue + credentialsRef + policyVersion`.

## Core contracts

### Market data

`MarketEvent` is the common input for live and replay.

Minimum fields:
- eventTime;
- receiveTime;
- instrument;
- bid/ask/last as available;
- OHLC/bar event where produced;
- source;
- sequence.

Implement:
- `ReplayFeed`;
- `LiveFeed` interface;
- append-only recorder.

### Strategy

`OnMarket(state, event) -> []TradeIntent`

TradeIntent:
- strategyId;
- signalId;
- instrument;
- direction;
- entry semantics;
- invalidation;
- setup/context metadata;
- desired risk profile id.

No account identifiers.

### Position manager

`OnPosition(position, market, accountPolicyState) -> []PositionAction`

Actions:
- OPEN;
- HOLD;
- ADD_ADVERSE;
- ADD_FAVORABLE;
- MOVE_STOP;
- MOVE_TARGET;
- EXIT.

Every action is deterministic and journaled with reason code.

### Account/risk

AccountState minimum:
- provider/plan;
- lifecycle phase;
- nominal balance;
- realized/unrealized PnL;
- drawdown/floor state;
- trading-day counters;
- payout counters;
- account-specific exposure;
- enabled/disabled/kill state.

RiskSizer outputs quantity from a normalized dollar-risk request subject to account and provider limits.

### PropPolicy

Pure contract:
- `PreTrade(account, intent) -> ALLOW | DENY(reason)`;
- `OnFill/OnEOD/OnSession(...) -> AccountState`;
- `CanAutomate()`;
- `AllowedTradingWindow()`;
- max position / drawdown / consistency / payout-stage fields;
- compliance diagnostics.

Rule set must be versioned and date-stamped.

### Execution

Normalized `OrderIntent`:
- clientOrderId/idempotency key;
- accountId;
- instrument;
- side;
- qty;
- order type;
- limit/stop;
- parent signal/action;
- deadline/time-in-force.

ExecutionVenue:
- Connect;
- SubscribeMarket;
- Submit;
- Cancel;
- Replace;
- Flatten;
- Snapshot;
- Events.

All submit/cancel/replace operations are idempotent from the core perspective.

### Reconciliation / safety

Fail closed on:
- stale account state;
- stale market data;
- lost venue session;
- unknown working order;
- policy version missing;
- risk computation failure.

Always permit protective reduction/flatten where technically possible.

Global kill switch and per-provider/per-account disable switches mandatory.

## Provider/venue plan

### Topstep

Provider: Topstep.
Initial venue: ProjectX/TopstepX API.
M0: auth + account discovery + market/order event contract + shadow/demo/sim order path only.
Do not assume the same venue works after transition to Live Funded.

### Lucid

Provider: Lucid.
Initial venue target: generic NinjaTrader Bridge.
M0 bridge is provider-neutral: local C# component exposes account/order/market events to the Go runtime and accepts normalized order commands.
Do not bake Lucid rules into the bridge.

### Later

MFFU may reuse NinjaTrader/Rithmic/other venue adapter after rule/connection capture.
Tradeify remains conditional because of cross-firm bot-exclusivity.
Apex/TPT are not M0 automated providers.

## Replay/backtest design

Do NOT build a second strategy implementation.

`ReplayFeed -> same Strategy -> same PositionManager -> SimExecutionVenue -> same EventJournal`.

M0 replay needs:
- deterministic clock;
- deterministic event ordering;
- commission/slippage hook;
- account/prop policy execution;
- exported trade/account lifecycle events.

Historical dataset acquisition is NOT a blocker for implementing the engine. M0 may use synthetic fixtures and any legally available recorded data; live recorder starts creating our own corpus as soon as a feed is connected.

## Persistence

Weekend KISS:
- append-only NDJSON/JSONL event journal, optionally zstd-compressed;
- run manifest with git SHA, strategy config, policy versions, seed/replay source;
- snapshots only for fast restart; journal remains authority for reconstruction.

No Kafka/Postgres requirement for M0.

## Observability

Structured logs + Prometheus-style counters if already cheap.
Mandatory:
- strategy signals;
- intents allowed/denied;
- policy denial reason;
- orders/fills/rejects;
- reconciliation mismatches;
- kill-switch transitions;
- per-account realized PnL/exposure.

No frontend required.

## Weekend plan

### M0-A — contracts + deterministic runtime
Freeze domain types/interfaces, event journal, deterministic clock, replay feed, SimExecutionVenue, account inventory, kill switch.

Gate: one synthetic scenario replays byte/reason-code deterministically.

### M0-B — strategy + position-management vertical slice
Implement Random50 control plus ONE mechanically defined strategy placeholder/candidate and a PositionManager shell supporting adds/stops/targets without provider knowledge.

Gate: same strategy code executes under replay and shadow runtime.

### M0-C — Topstep ProjectX adapter
Auth/config boundary, account discovery, market/account/order event ingestion, shadow first; demo/sim execution only when policy/credentials permit.

Gate: reconcile remote account/orders with local state; kill switch proven.

### M0-D — NinjaTrader bridge
Minimal C# bridge contract for market/account/order events + submit/cancel/flatten. No Lucid-specific logic.

Gate: mock/Sim account E2E from Go signal to NT order lifecycle.

### M0-E — Topstep + Lucid policy adapters
Topstep current rule adapter and Lucid rule adapter sufficient to block invalid orders. Rules date/version stamped.

Gate: provider-incompatible intent denied before transport; valid mock intent routed.

### M0-F — E2E weekend certification
Replay -> strategy -> manager -> risk -> policy -> simulated venue -> fills -> account state -> journal.
Then shadow/demo provider path.

Gate:
`M0_ALGO_EXECUTION_PASS = REVIEW`.

## Explicit weekend non-goals

- production real-money;
- UI;
- 40–80 account scale;
- full historical-data platform;
- optimization/search of strategy parameters;
- all prop firms;
- generalized distributed architecture;
- Kafka/Temporal/Kubernetes;
- integration into Echo core;
- automated payout handling.

## Definition of done

A developer can run one command that:
1. loads a versioned run config;
2. selects replay or shadow provider mode;
3. runs one strategy;
4. manages one or more account bindings;
5. blocks provider/risk violations before execution;
6. emits deterministic event journal/evidence;
7. can be killed/flattened safely.

After M0, M1 is strategy validation + additional algorithmic providers, not a rewrite of the runtime.


## Owner Correction — Multi-Prop Core + Central Reference Feed — 2026-09-25

This section SUPERSEDES the earlier provider-narrow interpretation of M0. Lucid is only one example provider; the architecture must be shaped by a first cohort of ~5 algorithmic futures prop firms and must remain extensible toward 10–20 providers and later multiple trader identities.

### Core architectural decision

**Strategy and position-management logic live in Echo Futures Core, not inside provider/platform bridges.**

Futures are exchange-centralized enough to use one canonical reference market-data plane for strategy decisions, provided the system performs explicit contract/session normalization, feed-health checks and controlled failover.

Target feed topology:

```text
FeedAdapter PRIMARY ─┐
FeedAdapter BACKUP1 ─┼─> MarketDataHub -> CanonicalMarketEvent -> BarBuilder/Indicators
FeedAdapter BACKUP2 ─┘
                                               |
                                               v
                                      Strategy Runtime
```

Rules:
- exactly one feed is authoritative for decision-making at any instant;
- backups are hot/warm and quality-monitored;
- never blend ticks from multiple vendors into one synthetic live sequence;
- failover requires gap/latency/contract checks and emits an explicit FEED_FAILOVER event;
- every raw/canonical event may be recorded for future replay/backtest;
- execution venues still report their local quote/fill state for sanity/reconciliation, but provider feeds do not silently become the strategy authority.

### Stateful strategy / hardscalping

Strategy code is shared centrally, but mutable position state is not assumed identical across accounts.

Use:
- shared StrategyDefinition / signal logic;
- account/deployment-specific StrategyInstance and ManagedPositionState where fills/rules can diverge;
- common canonical market feed;
- account-specific quantity, average fill, stop/target and recovery calculations;
- common reason-coded actions (OPEN, ADD_ADVERSE, ADD_FAVORABLE, MOVE_STOP, MOVE_TARGET, EXIT).

Thus a common signal can fan out while each account remains independently reconcilable and policy-compliant.

### Domain split

```text
REFERENCE DATA PLANE
  FeedAdapters -> MarketDataHub -> Canonical events/bars/indicators

DECISION PLANE
  StrategyDefinition -> StrategyInstance -> PositionManager

ACCOUNT/POLICY PLANE
  TraderIdentity -> AccountBinding -> AccountState
  InterTradeRiskPolicy
  ProviderRuleSet / ProgramRuleSet / ComplianceGuard

EXECUTION PLANE
  ExecutionGateway -> platform bridge/adapter -> provider account

EVIDENCE PLANE
  EventJournal + DecisionRecord + Reconciliation + metrics
```

Provider != execution technology.

Examples:
- Topstep + ProjectX
- Lucid + NinjaTrader
- MFFU + NinjaTrader
- TradeDay + NinjaTrader
- FundedNext Futures + NinjaTrader

A single NinjaTrader bridge may therefore service multiple providers without containing provider rules.

### Initial provider discovery set

Captured from current first-party rules on 2026-09-25. This is an architecture/discovery cohort, not a final economic ranking.

1. **Topstep** — custom automated bots allowed through TopstepX/ProjectX API; Live Funded requires a different future execution path.
   Authority: https://help.topstep.com/en/articles/11187768-topstepx-api-access
2. **Lucid Trading** — automated systems and trade copiers permitted; NinjaTrader is a supported platform.
   Authorities: https://support.lucidtrading.com/en/articles/11404728-other-trading-activities · https://support.lucidtrading.com/en/articles/11404614-lucid-trading-supported-platforms
3. **MyFundedFutures** — automated strategies tailored to the trader permitted; NinjaTrader/Tradovate supported.
   Authorities: https://help.myfundedfutures.com/en/articles/8444599-fair-play-and-prohibited-trading-practices · https://help.myfundedfutures.com/en/articles/8528335-overview-of-supported-platforms-at-mffu
4. **TradeDay** — automated/algo/bot trading permitted when using supported platforms; NinjaTrader/Tradovate among them; direct platform API is not exposed.
   Authorities: https://tradeday.freshdesk.com/en/support/solutions/articles/103000085101-automated-algo-and-bot-trading · https://tradeday.freshdesk.com/en/support/solutions/articles/103000008813-which-trading-platforms-does-tradeday-use-
5. **FundedNext Futures** — automated systems/EAs/bots expressly permitted in Challenge and FundedNext accounts; NinjaTrader/Tradovate supported; HFT/system exploitation prohibited.
   Authorities: https://helpfutures.fundednext.com/en/articles/14298560-is-the-usage-of-automated-trading-systems-eas-and-bots-allowed-in-fundednext-futures · https://helpfutures.fundednext.com/en/collections/19234504-fundednext-futures-trading-platform-faq

Conditional/excluded examples shaping the rule model:
- Tradeify: automation allowed only under restrictive ownership/non-sharing semantics; do not assume shared cross-firm strategy compatibility.
- Alpha Futures: full automation/bots prohibited.
- Bulenox: automation/AI requires explicit permitted-tool/rule treatment and some third-party algorithms require approval; keep conditional.
- OneUp/Earn2Trade: platform support exists but explicit first-party autonomous-bot permission has not yet been frozen; keep research queue.

### Provider rules architecture

Do NOT create a giant provider switch and do NOT invent a DSL up front.

Use a typed rule composition model:

```text
ProviderRuleSet
  metadata:
    provider
    program
    version
    effective_at
    evidence[]
    automation_status

  scopes:
    ACCOUNT
    TRADER
    HOUSEHOLD
    PROVIDER
    CROSS_PROVIDER

  rules:
    TradingWindowRule
    MaxPositionRule
    DailyLossRule
    DrawdownRule
    ConsistencyRule
    NewsRule
    HoldTime/MicroscalpRule
    AutomationRule
    Copy/HedgeRule
    AccountCountRule
    PayoutRule
    LifecycleRule
    custom exceptions where unavoidable
```

Every rule evaluates to ALLOW / DENY / UNKNOWN. UNKNOWN is fail-closed for new risk.

The model must be proven against the five-provider discovery cohort before it is frozen as generic.

### Multi-user future

Add `trader_id` / owner scope to domain identities now, but do not implement a full multi-tenant product this weekend.

Minimum hierarchy:

```text
TraderIdentity
  -> StrategyDeployment
  -> AccountBindings[]
```

Credentials, account inventories, provider limits and journals are isolated by trader.

Never infer that two users may copy each other merely because they run the same software. Provider restrictions on shared/coordinated strategies remain enforceable by policy.

### Backtest/replay

Backtest remains a first-class runtime mode, but lack of historical data is NOT an M0 blocker.

Implement:
`Historical/RecordedFeed -> same MarketDataHub -> same Strategy/PositionManager -> SimExecutionVenue`.

Start recording the canonical live feed as soon as a provider-independent feed is connected. This creates the project's own replay corpus over time.

### Revised weekend target

Do not spend the weekend implementing five transport adapters.

Target:
1. central MarketDataHub + feed authority/failover contract;
2. strategy/position/risk core;
3. provider-rule contract proven against the five-provider rule corpus;
4. one universal NinjaTrader bridge E2E;
5. one ProjectX bridge/adapter E2E;
6. one-account-per-provider configuration for the five initial providers where transport/rules are verified;
7. replay/sim mode using exactly the same decision code.

This architecture should scale from 5 providers × 1 account to many accounts/provider without moving strategy logic into bridges.
