# Echo Futures — D6 Earn2Trade First-Party Preflight Research

**Subtask:** D6 Earn2Trade rules / automation / execution transport preflight  
**Role:** SUBMANAGER research synthesis  
**Date:** 2026-09-30  
**Final subtask status:** `BLOCKED_PENDING_PROVIDER_CONFIRMATION`  
**Project:** [[Echo Futures]]  
**Echo frozen baseline:** `xKoRx/echo@13e087a3bb762f65b060d3b3200fb00a67c6ff1d`  
**D5:** `CLOSED_BY_OWNER` / `EF_D5_FOUNDATION_PASS = REVIEW`  
**ATP entering D6:** 113 PASS / 0 FAIL / 0 INCOMPLETE / 2 DEFERRED_TO_D6  
**S12:** 13/13 PASS

## 1. Objective

Produce current first-party evidence sufficient for the Primary Manager to build:

`Echo Futures — D6 Earn2Trade Preflight + Execution Plan`

The bounded question was whether Earn2Trade can serve as the first real Echo Futures MVP provider without reopening D5, specifically:

1. current programs/account sizes;
2. exact runtime-relevant rules by Evaluation / LiveSim / Live;
3. policy for a trader-owned algorithm running exactly one account;
4. distinction between algorithmic trading and trade copying/prohibited conduct;
5. current platforms/transports;
6. actual API/automation entitlement per Earn2Trade stage;
7. environments;
8. transport authentication/capabilities;
9. provider-support unknowns;
10. purchase-affecting blockers.

This artifact synthesizes accepted worker evidence. It does not select the Echo execution adapter, select an account to buy, redesign D5, or emit a D6 gate.

## 2. Why this research was needed

D6 starts from an accepted provider-agnostic D5 architecture. Earn2Trade is the Owner-selected first real provider target, but the following could not be assumed from historical research or vendor capability alone:

- provider rules may have changed;
- funded-stage rules differ from Evaluation;
- a supported platform is not proof of custom automation permission;
- a public vendor API is not proof that an Earn2Trade account receives API credentials/entitlement;
- post-pass LiveSim/Live provisioning may change transport, credentials, partner, fees or rules;
- trade copying prohibition is not logically equivalent to own-algorithm prohibition.

Therefore first-party current evidence was required before purchase/config freeze.

## 3. Scope and non-goals

### In scope

- Earn2Trade official website, Help Center, Terms and current program pages;
- current funding lifecycle information;
- official NinjaTrader, Tradovate and Rithmic documentation where transport capability mattered;
- current prices/promotions/reset evidence;
- stage-specific rules and drawdown semantics;
- provider-support questions where public evidence ends.

### Non-goals

- no Echo source audit;
- no D5 redesign;
- no provider-specific Strategy or MoneyManagement;
- no generic broker/plugin framework;
- no rules DSL;
- no transport implementation;
- no purchase decision;
- no D6 acceptance gate.

## 4. Frozen internal context

The following are accepted internal facts and were not reopened:

- Strategy is provider-agnostic.
- GerardMM is provider-agnostic.
- ProviderRuleSet carries complete read-only provider policy for MM.
- `provider_rules(account_id)` is final account-wide provider-policy authority.
- MVP operating policy uses one Earn2Trade account active at a time.
- Echo Futures is not a leader/follower trade copier.
- No provider-specific Strategy.
- No `Earn2TradeGerardMM`.
- No generic rule DSL.
- No generic broker/plugin framework.
- Owner economics `SL = USD 2000` and `TP = USD 1500` are internal configuration, not Earn2Trade rules.

## 5. Prior artifact register

| Artifact | Status | Provenance | Disposition |
| --- | --- | --- | --- |
| Historical futures-prop research | REFERENCE_ONLY | Pre-D6 historical corpus | May orient discovery; does not satisfy current evidence |
| D1–D5 Echo Futures | ACCEPTED_INPUT for frozen internal context only | Canonical project history | Not provider-policy evidence |
| `DEEPRESEARCH-PASS-1-E2T-EXTERNAL-EVIDENCE.md` | ACCEPTED_INPUT | DEEPRESEARCH Pass 1, Agents-OS `0f6c20fca2ebb57bc87df37870b14bc29940ec70` | Accepted for current program inventory, TCP25/GAU50 rules, drawdown semantics, copier prohibition, platform inventory, vendor API capability and promotion existence |
| `RESEARCH-PASS-2-E2T-ENTITLEMENT-RULES-GAP-REPAIR.md` | ACCEPTED_INPUT | RESEARCHER Pass 2, Agents-OS `9bf0456b3d830af05643429256b892abb1017e8c` | Accepted as targeted repair; no contradictions with Pass 1 |

## 6. Worker iteration log

### Iteration 1 — DEEPRESEARCH

**Question assigned:** broad current first-party corpus for Earn2Trade programs, rules, automation policy and execution transports.

**Returned result:** current inventory and substantial stage/rule corpus; exact drawdown semantics; explicit trade-copier prohibition; current NinjaTrader–Tradovate path; vendor API capability for NinjaTrader/Tradovate/Rithmic; entitlement gaps clearly separated.

**Review verdict:** ACCEPTED_INPUT.

**Repair triggered because:**

- own-algorithm permission remained ambiguous;
- all custom/direct transport entitlements remained unknown;
- funded transport continuity remained unknown;
- larger account-size rule rows were incomplete;
- promo expiry/reset interactions were incomplete.

### Iteration 2 — RESEARCHER

**Question assigned:** targeted entitlement/policy/rule-row/commercial repair only.

**Returned result:** no public first-party evidence closes own-algorithm permission or direct/custom transport entitlement; funded continuity only partially closes; dynamic rule rows remain incomplete for several account sizes; promotion expiry/reset interactions remain unresolved.

**Review verdict:** ACCEPTED_INPUT.

**Contradictions with Pass 1:** NONE.

**Further worker triggered:** NO. Public-document research is exhausted for the material blockers. The remaining evidence must come from Earn2Trade / funded-partner confirmation, not another web-research pass.

## 7. Current program inventory

### Trader Career Path®

Current first-party inventory:

- TCP25
- TCP50
- TCP100

Current base evaluation prices captured:

- TCP25: USD 150/month
- TCP50: USD 190/month
- TCP100: USD 350/month

Current public promotion on 2026-09-30:

- code: `50PLUSRESET`
- advertised: 50% OFF + one free reset with every evaluation
- explicit public expiration: UNKNOWN

Supported discounted interpretation from the current offer:

- TCP25: USD 75 floor directly advertised
- TCP50: USD 95 arithmetic implication of 50% off, not independently rendered as a separate current selected checkout value in Pass 1
- TCP100: USD 175 same limitation

### The Gauntlet Mini™

Current first-party inventory:

- GAU50
- GAU100
- GAU150
- GAU200

Current base prices:

- GAU50: USD 170
- GAU100: USD 315
- GAU150: USD 375
- GAU200: USD 550

Current 50% checkout values captured:

- GAU50: USD 85
- GAU100: USD 157.50
- GAU150: USD 187.50
- GAU200: USD 275

### Candidate evidence quality

This is not a purchase ranking.

| Program | Current existence | Complete current stage-row evidence in this corpus |
| --- | --- | --- |
| TCP25 | FACT | HIGH |
| TCP50 | FACT | INCOMPLETE overall; Evaluation repaired |
| TCP100 | FACT | INCOMPLETE |
| GAU50 | FACT | HIGH |
| GAU100 | FACT | INCOMPLETE |
| GAU150 | FACT | INCOMPLETE |
| GAU200 | FACT | INCOMPLETE |

For immediate runtime-rule modeling, TCP25 and GAU50 are the only sizes with sufficiently complete current rows in the accepted public corpus. That is an evidence-completeness statement only.

## 8. Stage model and generic rules

Current first-party stage model establishes:

| Rule / property | Evaluation | LiveSim® | Live |
| --- | --- | --- | --- |
| Environment | Simulated evaluation with real market data | Simulated capital with live market data; withdrawals possible | Real funded/live account |
| Drawdown type | End-of-Day | End-of-Day | Trailing |
| TCP top-stage exception | N/A | N/A | 200K/400K top growth stages use fixed drawdown |
| Daily Loss Limit | YES | YES | YES |
| Consistency | 30% | NO | NO |
| Minimum trading days | NONE | NONE | NONE |
| News trading | Allowed | Allowed | Allowed |
| General close window | Flatten before applicable close window; general rule includes 15:50 CT with instrument/exchange exceptions | Flat 15:50–17:00 CT | Flat 15:50–17:00 CT |
| Trade copiers | PROHIBITED | PROHIBITED | PROHIBITED |
| Current post-pass outcome | N/A | Funding partner may offer | Funding partner may offer |

Instrument/session-specific windows remain material; runtime must not collapse all products into one generic close time without the selected instrument calendar.

## 9. Exact drawdown semantics

### Evaluation / LiveSim — End-of-Day Drawdown

**Classification:** FACT.

- Minimum balance starts at starting balance minus drawdown amount.
- Positive end-of-day account balance performance ratchets the minimum balance upward dollar-for-dollar.
- Watermark advancement is processed at EOD / market-close processing.
- A lower later EOD balance never lowers the watermark.
- Watermark stops advancing once the minimum balance reaches original starting balance.
- Open/unrealized equity still participates in breach detection intraday: equity at or below the established minimum can fail the account before the next EOD ratchet.

Operational model:

`EOD balance watermark + intraday equity breach check + monotonic upward ratchet + cap at starting balance`.

### Live — Trailing Drawdown

**Classification:** FACT.

- Tracks positive performance intraday.
- Uses both closed and open/unrealized equity.
- Positive unrealized PnL can advance the threshold before the position closes.
- Threshold advances dollar-for-dollar with new positive performance.
- It never retreats after losses.
- It stops advancing once the threshold reaches original starting balance.

Operational model:

`intraday equity trailing + unrealized included + monotonic upward + cap at starting balance`.

### TCP top growth stages — Fixed Drawdown

**Classification:** FACT.

A static minimum balance applies to the TCP funded 200K/400K top stages; it does not trail.

## 10. Captured concrete rule rows

### TCP25 Evaluation

- start: USD 25,000
- profit target: USD 1,750
- EOD drawdown: USD 1,500
- daily loss: USD 550
- max/progression: up to 3 contracts
- consistency: 30%
- minimum days: none
- news: allowed

### TCP25 LiveSim

- start: USD 25,000
- progression target: USD 1,750
- EOD drawdown: USD 1,500
- daily loss: USD 550
- max/progression: up to 3 contracts
- no consistency
- no minimum days

### TCP25 Live

- start: USD 25,000
- progression target: USD 1,750
- trailing drawdown: USD 1,500
- daily loss: USD 550
- max/progression: up to 3 contracts
- no consistency
- no minimum days

### GAU50 Evaluation

- start: USD 50,000
- profit target: USD 3,000
- EOD drawdown: USD 2,000
- daily loss: USD 1,100
- max/progression: up to 6 contracts
- consistency: 30%
- minimum days: none
- news: allowed

### GAU50 LiveSim

- start: USD 50,000
- EOD drawdown: USD 2,000
- daily loss: USD 1,100
- max/progression: up to 6 contracts
- no consistency
- no minimum days

### GAU50 Live

- start: USD 50,000
- trailing drawdown: USD 2,000
- daily loss: USD 1,100
- max/progression: up to 6 contracts
- no consistency
- no minimum days

### TCP50 Evaluation — repaired in Pass 2

- start: USD 50,000
- profit target: USD 3,000
- EOD drawdown: USD 2,000
- daily loss: USD 1,100
- max/progression: up to 6 contracts
- consistency: 30%
- minimum days: none
- current reset display: USD 100

### Still incomplete complete-stage rows

- TCP50 LiveSim/Live
- TCP100 Evaluation/LiveSim/Live
- GAU100 Evaluation/LiveSim/Live
- GAU150 Evaluation/LiveSim/Live
- GAU200 Evaluation/LiveSim/Live

No missing value is filled from neighboring sizes, historical pages, default dynamic tabs or growth-stage values.

## 11. Automation-policy evidence

Central question:

> Can a trader run exactly one Earn2Trade account at a time using the trader's own software to generate and send orders automatically, with no copying, mirroring, leader/follower, hedging or synchronization with another account?

### Current result

| Stage | Own algorithm policy |
| --- | --- |
| Evaluation | UNKNOWN |
| LiveSim | UNKNOWN |
| Live | UNKNOWN |

### What is FACT

- Trade copiers are explicitly prohibited across Evaluation and funded stages.
- Account mirroring/collaborative/manipulative conduct covered by current rules is prohibited.
- Terms contain a clause prohibiting programs/bots/routines used to automatically access or manipulate the Earn2Trade “Service”.
- Prohibited Conduct identifies software/AI/ultrafast techniques when used to manipulate the environment or gain unfair advantage.
- Earn2Trade supports platforms whose vendors technically support automated trading.

### What is not FACT

Public Earn2Trade documentation does not explicitly state that a trader-owned automated strategy on one account is allowed or prohibited.

A reading that the Prohibited Conduct software language targets manipulative/unfair uses rather than software per se is only a **SUPPORTED_INTERPRETATION**. It is not sufficient provider permission.

### Separation that must be preserved

`OWN_ALGORITHMIC_TRADING` is not equivalent to:

- `TRADE_COPYING`
- `LEADER_FOLLOWER`
- `ACCOUNT_MIRRORING`
- `MULTI_ACCOUNT_COORDINATION`
- `UNFAIR_ADVANTAGE_OR_MANIPULATION`
- automation of the Earn2Trade website/service layer itself

Provider written confirmation is required.

## 12. Current platform / transport inventory

Current relevant candidates:

1. NinjaTrader Desktop / NinjaScript using the current Earn2Trade NinjaTrader–Tradovate route.
2. Tradovate direct REST/WebSocket.
3. Rithmic R|API+ / R|Protocol.
4. R Trader / R Trader Pro as supported Rithmic frontend/operational tooling, not treated as Echo's direct API surface here.

Material 2026 change:

- New Earn2Trade-provided NinjaTrader access uses the NinjaTrader–Tradovate path.
- Legacy Earn2Trade-provided NinjaTrader/Rithmic access ended for new/current rollout purposes after June 30, 2026.
- A personally licensed NinjaTrader/Rithmic path is a distinct case and not proof of Earn2Trade entitlement.

## 13. Transport capability vs entitlement matrix

| Candidate | PLATFORM_SUPPORTED | Vendor automation/API exists | E2T account/stage automation entitlement |
| --- | --- | --- | --- |
| NinjaTrader + NinjaScript via E2T Tradovate route | YES | YES | UNKNOWN all stages |
| Tradovate REST/WebSocket direct | YES as current platform/feed | YES | UNKNOWN all stages |
| Rithmic R|API+ / R|Protocol direct | YES as E2T Rithmic transport family | YES | UNKNOWN all stages |

### NinjaTrader / NinjaScript

**FACT:** NinjaTrader supports custom automated Strategies/AddOns and the required order/execution lifecycle primitives.

**UNKNOWN:** Earn2Trade permission for custom NinjaScript order automation, including unattended/VPS execution, on Evaluation, LiveSim and Live.

### Tradovate direct API

**FACT:** Tradovate exposes REST/WebSocket trading/account/order APIs and marks automated orders.

**FACT:** Public retail developer prerequisites include an appropriate Live account, API Access and API key.

**FACT:** Earn2Trade provisions Tradovate credentials for supported platform access.

**UNKNOWN:** whether Earn2Trade-issued Evaluation/LiveSim/Live credentials include or can obtain direct REST/WebSocket developer entitlement/API-key rights, including any B2B exception to normal retail prerequisites.

### Rithmic direct API

**FACT:** Rithmic exposes custom algorithmic APIs.

**FACT:** custom applications require conformance before production/Paper systems, then applicable broker/FCM credentials/fees.

**FACT:** Earn2Trade provisions Rithmic credentials for supported frontends/Evaluation paths.

**UNKNOWN:** whether Earn2Trade credentials can be used by a conformed custom R|API+/R|Protocol application, and what partner/FCM/application identity/fees apply per stage.

## 14. Authentication and environments

### Earn2Trade Evaluation

**FACT:** simulated/virtual account with real market data.

### LiveSim

**FACT:** simulated capital with live market data and withdrawal capability.

### Live

**FACT:** real funded/live account provided through funding partner.

### NinjaTrader–Tradovate

Earn2Trade provisions Tradovate credentials for the current NinjaTrader route; Evaluation uses simulated account mode. Exact custom-automation permission remains unknown.

### Tradovate direct API

Vendor supports token/API-key/OAuth style developer access and WebSocket authorization. Earn2Trade data credentials are not proof of API-key entitlement.

### Rithmic

Earn2Trade provisions Rithmic data-feed credentials for supported platform use. Direct custom API use requires Rithmic's developer/conformance path, but the E2T account mapping remains unknown.

## 15. Funded transport continuity

### FACT

- After passing, Earn2Trade verifies the evaluation and forwards it to a funding partner such as Helios Trading Partners or Appius Trading Limited.
- The funding partner can offer LiveSim or Live.
- For the documented NinjaTrader Live path, the prop firm creates the live account and supplies new live credentials.

### UNKNOWN_REQUIRES_PROVIDER_CONFIRMATION

- whether Evaluation transport can be retained in LiveSim;
- whether Evaluation transport can be retained in Live;
- LiveSim credential reprovisioning;
- partner-specific Helios/Appius transport differences;
- whether automation/API approval must be repeated post-pass;
- whether an approved direct Tradovate or Rithmic API entitlement carries into funded stages.

## 16. Commercial evidence

### Current promotion

**FACT on 2026-09-30:**

`50PLUSRESET` advertises 50% off plus one free reset with every evaluation.

**UNKNOWN:**

- expiration date/time;
- code-specific eligibility/geography;
- whether promotional free reset stacks with TCP's monthly-rebill free reset.

### TCP reset pricing

Current purchase UI displays:

- TCP25 reset: USD 100
- TCP50 reset: USD 100

However current official reset policy describes these reset prices as dynamic/promotion-adjusted and below current new-subscription price. Under the active promotion, the public sources do not reconcile cleanly.

Classification:

- displayed USD 100: FACT about UI display;
- actual amount charged under `50PLUSRESET`: UNKNOWN_REQUIRES_PROVIDER_CONFIRMATION.

## 17. Rejected / superseded evidence

### SUPERSEDED

- older material requiring 10 minimum trading days;
- older material treating Evaluation as Rithmic-only;
- legacy Earn2Trade-provided NinjaTrader/Rithmic route for new subscriptions after the 2026 rollout.

### REJECTED_FOR_GENERAL_PROMO

Affiliate-specific checkout discounts that conflict with the current site-wide `50PLUSRESET` offer are not used as the general promotion authority.

### NOT PROMOTED

Older funding/data-feed material predating the 2026 NinjaTrader–Tradovate rollout is not promoted into a universal current transport rule.

## 18. Evidence contradictions / limitations

### Terms bot clause vs automation-capable ecosystem

Unresolved publicly. This does not prove automated trading allowed and does not prove it prohibited.

### Reset policy vs current displayed reset amount

Unresolved publicly. Exact promo-adjusted charge requires provider confirmation.

### Dynamic UI rule tables

Evidence is selection-scoped. Proving a plan selector exists does not prove the numeric rule row behind another plan/stage. No values were transplanted across tabs.

## 19. Exact provider-support questions

The following seven questions are the minimum set needed to close the public-evidence blockers.

1. **Own algorithm policy**  
   I will trade exactly one Earn2Trade account at a time with my own algorithmic strategy, under my own control. My software will generate and send orders automatically. I will not copy, mirror, leader/follow, hedge, synchronize or coordinate trades with any other account. Is this permitted on (a) Evaluation, (b) LiveSim®, and (c) Live? Are unattended/VPS/cloud sessions permitted for this use case? Please also clarify whether the Terms clause about programs/bots automatically accessing or manipulating the Service applies to automated order execution through an Earn2Trade-supported trading interface.

2. **NinjaTrader / NinjaScript**  
   For an Earn2Trade account using the current NinjaTrader–Tradovate route, may I run a custom NinjaScript Strategy or AddOn that automatically places, modifies and cancels orders on (a) Evaluation, (b) LiveSim®, and (c) Live?

3. **Tradovate direct API**  
   Do Tradovate credentials provisioned by Earn2Trade permit direct REST/WebSocket developer API access, API Access/API-key creation and automated order submission on (a) Evaluation, (b) LiveSim®, and (c) Live? If standard Tradovate retail API prerequisites do not apply to Earn2Trade accounts, how is the entitlement provisioned?

4. **Rithmic direct API**  
   After Rithmic conformance, may Earn2Trade-issued credentials be used from a custom R|API+ or R|Protocol application on (a) Evaluation, (b) LiveSim®, and (c) Live? What additional Earn2Trade/funding-partner/FCM approval, application identity, credentials and fees apply?

5. **Funded continuity**  
   For each current funding partner, which execution/data transports can be provisioned for LiveSim® and Live? Are credentials reprovisioned? Can the transport used during Evaluation be retained? Must custom automation/direct-API permission be approved again after passing?

6. **Promotion / resets**  
   What is the expiration date/time and eligibility scope of `50PLUSRESET`? Is its free reset additional to the TCP free reset earned after a monthly rebill? While the promotion is active, what amount is actually charged for TCP25 and TCP50 resets?

7. **Remaining rule rows**  
   Please confirm the complete current Evaluation, LiveSim® and Live rows for TCP50, TCP100, GAU100, GAU150 and GAU200, including starting balance, profit/progression target, drawdown amount/type, daily loss limit, max contracts/progression, consistency rule, trading hours, minimum trading days and every other stage-specific runtime rule.

## 20. Purchase-affecting findings

### P0 — own-algorithm permission

**BLOCKER.**

The mandatory MVP usage pattern is not publicly confirmed for Evaluation, LiveSim or Live.

### P0 — execution transport entitlement

**BLOCKER.**

No researched custom/direct execution path has current public Earn2Trade stage entitlement proven:

- NinjaScript: UNKNOWN
- Tradovate REST/WebSocket: UNKNOWN
- Rithmic direct API: UNKNOWN

Vendor capability and platform support are insufficient.

### P1 — funded continuity

Public evidence does not guarantee transport retention or automation/API entitlement after pass.

### P1 — promotion timing

Promotion exists currently but its expiry is not public.

### P2 — reset economics

Displayed reset values and the dynamic promotion-adjusted policy are not publicly reconciled.

## 21. Decisions enabled

The evidence is sufficient to enable these manager-level conclusions:

- Earn2Trade has current programs/rules compatible with continued D6 investigation.
- TCP25 and GAU50 have sufficiently complete public current rule rows for provider-rule modeling/provisional comparison.
- Evaluation/LiveSim EOD drawdown and Live trailing drawdown semantics are explicit enough to model accurately.
- Trade-copying prohibition is explicit and must remain distinct from Echo's single-account own-strategy model.
- NinjaTrader, Tradovate and Rithmic are technically automation-capable candidate surfaces, but none may be declared entitled for Echo yet.
- Public research alone cannot clear the purchase-dependent automation/transport gate.

## 22. Owner decisions still required

None until provider confirmation returns.

The immediate next step is evidence acquisition, not an owner product choice.

After provider confirmation, the Primary Manager can decide which program/account and minimum viable execution transport to carry into the D6 execution plan.

## 23. What this artifact explicitly does not decide

- which Earn2Trade account to purchase;
- which execution transport Echo should implement;
- whether NinjaTrader vs Tradovate vs Rithmic is architecturally preferable;
- whether provider-specific D6 deltas are acceptable;
- whether D6 passes;
- any owner gate.

## 24. Reusable assets

Accepted reusable research assets:

- provider-rule provenance matrix;
- transport entitlement checklist separating vendor capability / provider offering / account entitlement / stage entitlement;
- stage-rule comparison schema;
- provider-support question template;
- dynamic-UI provenance extension with `selected_plan` and `selected_stage`.

## 25. Reusable behavior candidates

1. **Entitlement triad:** vendor API capability, provider platform offering and actual account/stage entitlement are independent evidence claims.
2. **Dynamic-UI selection scope:** existence of a selectable plan does not prove the rule row behind that plan; evidence must identify selected plan/stage and must not transplant neighboring/default-tab values.

## 26. Source / evidence index

### Worker artifacts

- `main/10-projects/Echo Futures/artifacts/d6-earn2trade-preflight-20260930/DEEPRESEARCH-PASS-1-E2T-EXTERNAL-EVIDENCE.md`
- `main/10-projects/Echo Futures/artifacts/d6-earn2trade-preflight-20260930/RESEARCH-PASS-2-E2T-ENTITLEMENT-RULES-GAP-REPAIR.md`

### Principal Earn2Trade authorities

- https://www.earn2trade.com/
- https://www.earn2trade.com/trader-career-path
- https://www.earn2trade.com/gauntlet-mini
- https://www.earn2trade.com/terms-and-conditions
- https://help.earn2trade.com/en/articles/5941958-what-are-the-evaluation-rules
- https://help.earn2trade.com/en/articles/6877364-what-happens-when-i-complete-my-evaluation
- https://help.earn2trade.com/en/articles/8117088-drawdown-types
- https://help.earn2trade.com/en/articles/5372687-how-does-end-of-day-drawdown-work
- https://help.earn2trade.com/en/articles/3292356-what-is-a-trailing-drawdown
- https://help.earn2trade.com/en/articles/3395926-how-is-my-daily-loss-calculated
- https://help.earn2trade.com/en/articles/3849975-what-is-the-maintain-consistency-rule
- https://help.earn2trade.com/en/articles/12034590-am-i-allowed-to-copy-trades-across-multiple-accounts
- https://help.earn2trade.com/en/articles/9286647-prohibited-conduct-in-earn2trade-evaluations-and-in-the-livesim-live-trading-environment
- https://help.earn2trade.com/en/articles/15359154-ninjatrader-access-at-earn2trade
- https://help.earn2trade.com/en/articles/4473826-how-to-connect-tradovate-to-ninjatrader
- https://help.earn2trade.com/en/articles/14196947-how-do-i-set-up-my-tradovate-evaluation
- https://help.earn2trade.com/en/articles/6911655-how-do-i-set-up-my-rithmic-evaluation
- https://help.earn2trade.com/en/articles/13460913-ninjatrader-live-account-access
- https://help.earn2trade.com/en/articles/11183609-reset-pricing-for-earn2trade-accounts
- https://help.earn2trade.com/en/articles/6863801-do-you-provide-free-resets
- https://help.earn2trade.com/en/articles/2280137-what-is-the-fee-structure-on-the-live-or-livesim-accounts

### Vendor authorities

- https://api.tradovate.com/
- https://docs.ninjatrader.com/ninjascript/strategy
- https://docs.ninjatrader.com/ninjascript/onexecutionupdate
- https://docs.ninjatrader.com/ninjascript/cancelorder
- https://docs.ninjatrader.com/ninjascript/changeorder
- https://www.rithmic.com/apis
- https://www.rithmic.com/products
- https://www.rithmic.com/products/exchange-simulator

## 27. Final subtask status

```yaml
D6_E2T_RESEARCH: BLOCKED

BLOCKER:
  type: PROVIDER_CONFIRMATION_REQUIRED
  reason:
    - own-algorithm policy is UNKNOWN across Evaluation / LiveSim / Live
    - NinjaScript entitlement is UNKNOWN across all stages
    - Tradovate direct API entitlement is UNKNOWN across all stages
    - Rithmic direct API entitlement is UNKNOWN across all stages
    - funded transport continuity is only partially documented

PUBLIC_RESEARCH:
  pass_1: ACCEPTED_INPUT
  pass_2: ACCEPTED_INPUT
  contradictions: NONE
  more_public_research_expected_to_close_blocker: NO

NEXT_ACTION:
  OWNER_SEND_SUPPORT_QUESTIONS_AND_RETURN_WRITTEN_RESPONSE_TO_SUBMANAGER
```

The subtask must not be promoted to `READY_FOR_PRIMARY_MANAGER_REVIEW` until either:

1. Earn2Trade/funding partner provides enough written confirmation to resolve the P0 automation + entitlement blockers; or
2. the Primary Manager explicitly accepts a provider-policy/transport blocker as the bounded result and chooses to stop or change provider before purchase.
