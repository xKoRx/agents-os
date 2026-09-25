---
type: project
schema_version: 1
owner: agent
root: false
status: active
priority: P1
area: "[[Echo]]"
parent: "[[Echo Futures]]"
start: 2026-09-25
due: 2026-10-02
progress: 0
repo: "xKoRx/echo-futures"
aliases:
  - Echo Futures Prop Universe
tags:
  - kind/project
  - area/echo
  - echo-futures
  - prop-firms
  - research
created: "2026-09-25"
updated: "2026-09-25"
---

# Echo Futures — Futures Prop Universe

## Execution gate — canonical Echo Futures

Este track forma parte de **D1 Analysis** del nuevo [[Echo Futures]]. A fecha 2026-09-25 queda preparado pero **no debe ejecutarse fuera del manager de D1**. Su output será evidencia para diseñar Provider/Program/RuleSet; no congela por sí mismo arquitectura ni selección comercial de props.


## Goal

Build and maintain the authoritative universe of credible futures prop firms relevant to Echo Futures, including firms we can automate, firms that are conditional, firms that are economically unattractive, and firms that are excluded by automation/compliance constraints.

This is not a ranking/recommendation project. It is a versioned operational catalog feeding architecture, provider rules and later economic simulations.

## Scope

For every discovered provider capture:

- provider identity + first-party official URLs;
- current operational status;
- supported countries/eligibility relevant to Chile;
- programs/account sizes;
- evaluation/funded/live lifecycle;
- pricing, resets, activation;
- drawdown/DLL/consistency;
- minimum trading days;
- payout requirements/caps/splits;
- account limits by trader/household;
- supported platforms/data/execution venues;
- explicit automation/bot/API policy;
- copy/group/cross-prop restrictions;
- HFT/microscalping/min-hold/order-frequency restrictions;
- news/overnight/weekend rules;
- DCA/averaging/add rules;
- live-transition semantics;
- rule effective/captured dates;
- confidence and unresolved conflicts.

Every material rule must be backed by first-party evidence. Secondary aggregators may be used for discovery only.

## Classification

`automation_status`:
- ALLOWED;
- CONDITIONAL;
- FORBIDDEN;
- UNKNOWN.

`echo_status`:
- CANDIDATE;
- ENABLED_LATER;
- ECONOMICS_ONLY;
- BLOCKED_RULES;
- BLOCKED_PLATFORM;
- EXCLUDED;
- RESEARCH_PENDING.

Do not conflate economically attractive with technically automatable.

## Discovery seed — September 2026

Start from the union of current 2026 futures-prop directories/comparisons plus known firms. This list is a discovery queue, NOT verified eligibility:

- Topstep
- Lucid Trading
- MyFundedFutures
- TradeDay
- FundedNext Futures
- Apex Trader Funding
- Alpha Futures
- Tradeify
- Take Profit Trader
- Bulenox
- E8 Futures
- Earn2Trade
- FTMO Futures
- Top One Futures
- OneUp Trader
- UProfit
- Funded Futures Family
- Elite Trader Funding
- Blue Guardian Futures
- TickTickTrader / other still-active futures firms discovered during census

Secondary discovery sources at project creation:
- TradeTanto 2026 futures comparison (13-firm set);
- PropFirmPicker September-2026 first-party-rule index (10-firm set).

The researcher MUST expand/contract this seed based on current evidence and remove dead/CFD-only/non-futures firms.

## Deliverables

1. `provider-catalog.yaml/json` normalized catalog.
2. One evidence packet per provider.
3. Matrix of provider rules needed to validate the generic `ProviderRuleSet`.
4. Platform/transport matrix:
   provider -> program -> platform -> execution technology.
5. Automation eligibility matrix.
6. Economic-research priority queue.
7. List of rules that cannot be represented cleanly by the current rule model.

## Architecture feedback loop

The provider census MUST be completed far enough across materially different firms before freezing a generic rules engine.

If a new provider requires a rule family not present in the model:
- add a typed rule/capability if conceptually reusable;
- use provider-specific exception only when genuinely exceptional;
- never contaminate Strategy with provider rules.

## Multi-user warning

Capture rule scope:
- ACCOUNT;
- TRADER;
- HOUSEHOLD;
- PROVIDER;
- CROSS_PROVIDER.

Later use by another household member/user must be evaluated from each provider's explicit policies; do not assume software-level separation makes coordinated/copy trading permitted.

## Gate

`FUTURES_PROP_UNIVERSE_PASS = REVIEW`

Acceptance requires:
- broad current census;
- automation status established from first-party evidence for every high-priority provider;
- at least five automatable candidates if the market actually provides them;
- rule-family coverage sufficient to inform the Core ProviderRuleSet architecture;
- explicit blocked/excluded list and reasons.
