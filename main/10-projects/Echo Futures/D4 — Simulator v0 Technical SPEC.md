---
type: spec
schema_version: 1
status: approved-for-implementation
area: "[[Echo]]"
related:
  - "[[Echo Futures]]"
  - "[[D4 — Simulator v0 Functional SPEC]]"
  - "[[echo-futures-astra-math-review]]"
tags:
  - kind/spec
  - area/echo
  - echo-futures
  - simulator-v0
created: "2026-09-24"
updated: "2026-09-24"
---

# D4 — Simulator v0 — Technical SPEC

## 0. Freeze

Status: APPROVED FOR SHOT 1.

Target repository: xKoRx/echo-futures (new, isolated from Echo/Echo Forge).

Target implementation language: Go.

Shot 1 MUST NOT redesign the mathematics. Mathematical authority: [[echo-futures-astra-math-review]].

## 1. Design principle

Do not simulate ticks or Brownian time steps in v0.

The engine is event-driven and samples the next event directly from the exact first-passage kernel.

This is a research CLI/library. Standard library first. No database, HTTP server, UI, broker, market-data or production framework.

## 2. Repository shape

Expected minimum files:

```text
go.mod
README.md
cmd/sim/main.go
internal/sim/model.go
internal/sim/kernel.go
internal/sim/trade.go
internal/sim/lifecycle.go
internal/sim/cohort.go
internal/sim/validation.go
internal/sim/*_test.go
scenarios/t2-add-minus30.json
scenarios/eval-3000-2000.json
```

Files may be split further only when it makes tests clearer. Do not create generic framework packages.

Module target: github.com/xKoRx/echo-futures.

Use the installed stable Go toolchain and record go version in the delivery evidence. No third-party dependencies without a concrete need; Shot 1 should require none.

## 3. Numeric model

Use float64 in v0.

Rationale: normalized mathematical research, not production accounting. Exact decimal money is explicitly deferred.

All configuration validation MUST reject NaN/Inf and invalid ordering.

Use epsilon only for deterministic conservation asserts; never silently repair invalid probability or barriers.

## 4. Core types

Logical contract:

```text
Scenario
  Name
  Runs
  Seed
  Trade
  Evaluation
  Funded
  Economics
  SyntheticEdge
  Cohort

TradePolicy
  TargetMoney G > 0
  StopMoney L > 0
  InitialQty h0 > 0
  MaxQty hMax >= h0
  Adds[]

Add
  Price      relative price level; strictly adverse/decreasing for LONG v0
  Qty        positive quantity added

PhasePolicy
  Target > 0
  Drawdown > 0

Economics
  EvaluationFee F >= 0
  ActivationFee A >= 0
  OtherCost C >= 0
  FirstPayout W >= 0

SyntheticEdge
  Delta      signed probability-point shift
  Enabled    bool

Cohort
  AttemptCap > 0
```

LONG-only normalized price is sufficient for v0 because short symmetry adds no mathematical information.

## 5. Position bookkeeping

Represent current trade PnL as:

`Y(s) = b + h*s`

At open:

`s=0, b=0, h=h0`.

At add deltaH > 0 at current price s:

`h_new = h + deltaH`

`b_new = b - deltaH*s`

The implementation MUST assert:

`Y_before(s) == Y_after(s)` within numeric tolerance.

This self-financing invariant is non-negotiable.

## 6. Exact hitting kernel

Function contract:

`HitUpperProbability(lower, current, upper) -> p`

Precondition:

`lower < current < upper`.

Formula:

`p = (current-lower)/(upper-lower)`.

Reject malformed input. Do not clip.

Sampling:

`upperHit = rng.Float64() < p`.

The seed MUST make complete runs reproducible.

Shot 1 remains single-threaded to preserve deterministic RNG order and KISS. Do not parallelize.

## 7. Active barriers

For realized phase equity B and current trade bookkeeping b,h:

Trade lower price:

`tradeLower = (-StopMoney - b)/h`

Trade upper price:

`tradeUpper = (TargetMoney - b)/h`

Phase lower price:

`phaseLower = (-Drawdown - B - b)/h`

Phase upper price:

`phaseUpper = (Target - B - b)/h`

Terminal lower:

`terminalLower = max(tradeLower, phaseLower)`

Terminal upper:

`terminalUpper = min(tradeUpper, phaseUpper)`.

The next unused adverse add is eligible only when:

`terminalLower < add.Price < currentPrice`.

If eligible, the lower event sampled against terminalUpper is add.Price; otherwise it is terminalLower.

There is no favorable/pyramiding event in v0.

## 8. Event loop

For each active trade:

1. Compute terminal lower and upper.
2. Select the nearest eligible adverse add below current price, if any.
3. Define lowerEvent = eligible add price or terminalLower.
4. Define upperEvent = terminalUpper.
5. Compute pFair from exact kernel.
6. If synthetic-edge flag is armed, compute pEffective=pFair+Delta; validate 0<=pEffective<=1; consume the flag for this decision.
7. Sample upper/lower.
8. Move current price exactly to the selected event level.
9. Resolve event priority: phase barrier, trade close, add.
10. On add, apply self-financing bookkeeping and continue same trade.
11. On trade close without phase absorption, realize B=E and start a fresh trade at s=0,b=0,h=h0 with add index reset.
12. On phase upper/lower, transition/absorb lifecycle.

No timeout. No censored run. A technical runaway guard may abort with explicit INCOMPLETE/ERROR but must never convert the run to FAIL.

## 9. Synthetic edge v0

For Shot 1, arm synthetic edge only after the last configured adverse add is actually executed.

It applies to the next terminal hitting decision once, then is consumed.

`Delta=0` must follow the identical null code path except arithmetic addition of zero; validation T7 must confirm equivalence.

Do NOT implement delta per add/state in Shot 1.

## 10. Lifecycle

States:

`PURCHASE -> EVALUATION -> FUNDED -> FIRST_PAYOUT | FAIL`.

Purchase:

- personal cash starts at `-(F+C)`.

Evaluation:

- phase equity B starts at 0;
- upper phase barrier: record pass, personal cash `-=A`, enter FUNDED with B=0 and fresh trade;
- lower phase barrier: FAIL.

Funded:

- upper phase barrier: personal cash `+=W`, FIRST_PAYOUT;
- lower phase barrier: FAIL.

Per-attempt cash identity:

`R = J*W - F - I*A - C`, with `J<=I`.

## 11. Cohort mode

v0 cohort attempts are IID.

Repeat full purchased attempts until FIRST_PAYOUT or AttemptCap.

Report:

- attempts used;
- failures before payout;
- activations paid;
- total personal cash;
- whether payout occurred.

Across many cohort runs report mean plus P5/P50/P95 cash and attempts.

No correlation model in Shot 1.

## 12. CLI

Single binary: `sim`.

Required commands:

```text
sim validate --runs 1000000 --seed 42 [--format text|json]
sim simulate --scenario <file.json> [--runs N] [--seed N] [--format text|json]
sim cohort --scenario <file.json> [--cohorts N] [--seed N] [--format text|json]
```

CLI flags may override runs/seed only. Business/model parameters come from scenario JSON.

Invalid config -> non-zero exit with precise message.

`--format json` writes machine-readable result to stdout. Text mode is concise human-readable output.

## 13. Validation authority T1–T8

Implement exactly the acceptance cases from [[echo-futures-astra-math-review]].

Mandatory:

- T1 ±100 no adds -> p≈0.5, EV≈0.
- T2 add +1 at -30 -> reach add≈10/13, conditional win≈0.35, total win≈0.5.
- T3 adds +1 at -20 and -40 -> total win≈0.5.
- T4 phase +3000/-2000 -> pass≈0.4.
- T5 IID q=.1 -> mean attempts≈10, failures≈9, CDF n=10/20/30 as authority.
- T6 pPass=.4, pFunded=.25, F=100,A=50,W=1500,C=10 -> q=.1, EV=20, qBE=.0866667.
- T7 T2 delta=0 -> null identity.
- T8 T2 delta=.10 -> conditional=.45, total=15/26≈.5769231, EV=200/13≈15.384615.

Use authority tolerance:

`5*sqrt(p*(1-p)/N)` for probabilities.

For mean outputs use the corresponding 5-sigma standard-error tolerance from the authority.

Validation command MUST print expected, observed, tolerance and PASS/FAIL for each assertion.

## 14. Deterministic invariants

Tests MUST assert:

- add conserves Y within tight epsilon;
- J<=I always;
- h<=hMax always;
- probabilities outside [0,1] reject config;
- invalid/non-monotone adverse add list rejects config;
- add beyond active lower barrier does not execute;
- phase barrier wins ties over trade close, trade close wins ties over add;
- same seed + same config = byte-equivalent JSON result where ordering is deterministic.

## 15. Testing / quality gate

Run:

```text
go test ./...
go test -race ./...
go test -coverprofile=coverage.out ./...
go run ./cmd/sim validate --runs 1000000 --seed 42 --format text
```

New simulator core target coverage: >=95%.

Do not game coverage with meaningless tests.

## 16. Shot 1 evidence

Deliver:

- actual local repo path;
- branch and HEAD;
- `go version`;
- file tree;
- test/race/coverage results;
- complete T1–T8 validation output;
- one sample `simulate` output;
- one sample `cohort` output;
- known limitations;
- commit SHA.

Move delegated project gate to REVIEW. Do not start Shot 2.

## 17. No tocar

- xKoRx/echo;
- Echo Forge;
- NinjaTrader;
- Agents-OS files outside the delegated project/status update;
- real prop rules;
- market data/backtesting;
- remote production systems;
- credentials/secrets.

## 18. Stop conditions

STOP with PLAN_CONFLICT instead of guessing if:

- T1–T8 authority appears internally inconsistent;
- event ordering cannot reproduce T2/T3 analytically;
- repo creation/location conflicts with an existing user project;
- implementation would require changing frozen mathematics;
- a requested feature belongs to explicit non-goals.
