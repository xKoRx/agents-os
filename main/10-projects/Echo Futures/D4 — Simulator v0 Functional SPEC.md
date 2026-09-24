---
type: spec
schema_version: 1
status: approved-for-implementation
area: "[[Echo]]"
related:
  - "[[Echo Futures]]"
  - "[[echo-futures-astra-math-review]]"
tags:
  - kind/spec
  - area/echo
  - echo-futures
  - simulator-v0
created: "2026-09-24"
updated: "2026-09-24"
---

# D4 — Simulator v0 — Functional SPEC

## 0. Authority

This SPEC freezes D4 functional behavior for Echo Futures.

Authorities, in order:

1. [[echo-futures-astra-math-review]] — mathematical authority (MATH_GO).
2. [[Echo Futures]] — product thesis and scope.
3. This SPEC — user-visible simulator behavior.

If implementation evidence contradicts the mathematical authority, STOP with PLAN_CONFLICT; do not reinterpret the math.

## 1. Outcome

Deliver today a small deterministic Monte Carlo simulator that answers:

> Given a fair or synthetically biased first-passage process, a finite adverse-add policy, abstract evaluation/funded barriers and cash costs, what are the probabilities and cash outcomes up to FIRST PAYOUT?

The simulator is a research instrument, not production trading software.

## 2. Required capabilities

v0 MUST support:

- driftless/null first-passage kernel between lower/current/upper states;
- finite adverse add list;
- self-financing add accounting;
- fixed monetary trade target and stop;
- exact phase barriers;
- phases EVALUATION, FUNDED, FAIL, FIRST_PAYOUT;
- one bounded synthetic conditional edge delta applied once after the configured adverse state/last add;
- IID attempts;
- fixed fees F, activation A, other expected per-purchase cost C, first payout cash W;
- reproducible RNG via explicit seed;
- Monte Carlo batch execution;
- JSON scenario input;
- JSON result output;
- human-readable CLI summary;
- analytical/Monte Carlo acceptance tests T1–T8.

## 3. Required outputs

At minimum:

- runs;
- seed;
- scenario/config echo;
- win/loss counts for trade-only scenarios;
- p_pass;
- p_funded_given_pass;
- q_purchase_to_first_payout;
- mean attempts to payout for cohort mode;
- mean failures before payout;
- expected cash per purchased evaluation;
- total/mean activation count;
- result distribution summary when cohort mode is used;
- acceptance-test report with expected, observed, tolerance and PASS/FAIL.

## 4. Modes

### validate

Runs T1–T8 and deterministic invariants.

Exit code non-zero if any mandatory test fails.

### simulate

Runs one supplied scenario for N Monte Carlo runs.

### cohort

Runs repeated IID purchased evaluations until first payout or a configured attempt cap and reports cash distribution.

No other modes in v0.

## 5. v0 synthetic edge semantics

delta is an explicit hypothetical input, not an inferred market property.

For v0:

- delta=0 MUST be exactly equivalent to the null kernel;
- apply delta once after the last configured adverse add, on the next terminal hitting decision only;
- reject if p_fair + delta is outside [0,1];
- report both p_fair and p_effective.

Multi-state delta_1..delta_n is NOT part of Shot 1.

## 6. Definition of Done

D4 Shot 1 is ready for independent review when:

- project compiles;
- CLI runs;
- scenario input/output works;
- T1–T8 execute automatically;
- all deterministic invariants are asserted;
- 1,000,000-run validation completes in practical local time;
- output is reproducible by seed;
- no real prop rule, historical market data, Echo integration or NinjaTrader dependency exists;
- README documents exact commands and model limitations;
- implementation updates the delegated project to review.

## 7. Explicit non-goals

- current Topstep/Lucid/Apex rules;
- trailing drawdown;
- daily loss/consistency/day-count rules;
- real futures tick size/contract value;
- historical market data;
- backtesting;
- empirical mean reversion;
- multi-state synthetic edge;
- positive hardscalping/pyramiding;
- variable risk between trades;
- slippage/commission against nominal equity;
- correlated attempts;
- UI/dashboard;
- database;
- service/API;
- Echo/Forge/NinjaTrader changes;
- production trading.
