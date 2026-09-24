---
type: spec
schema_version: 1
status: review
area: "[[Echo]]"
related:
  - "[[Echo Futures]]"
  - "[[Echo Futures — D5 Prop Economics]]"
  - "[[D5-M1A — Topstep Functional SPEC]]"
  - "[[D4 — Simulator v0 Technical SPEC]]"
  - "[[echo-futures-astra-math-review]]"
tags:
  - kind/spec
  - area/echo
  - echo-futures
  - d5-m1a
  - topstep
created: "2026-09-24"
updated: "2026-09-24"
---

# D5-M1A — Topstep Fast Track — Technical SPEC

## 0. Freeze

Status: FROZEN PENDING MANAGER ACCEPTANCE (`D5_TOPSTEP_SPEC_PASS = REVIEW`). No coding is authorized before that gate.

Target repository: xKoRx/echo-futures. Certified implementation baseline: `d4f42a41946f12231b75e4eb65b90d132731be0d` (D4 CLOSED, gate 47/47 + coverage 96.1%). Target language: Go, stable toolchain, standard library first, no third-party dependencies without concrete need.

Behavior authority: [[D5-M1A — Topstep Functional SPEC]]. Mathematical authority: planner §D5.3 (GOD verdict + corrections C1–C6), unchanged. This SPEC extends D4 minimally; it does not redesign D4, does not re-derive any accepted formula, and does not introduce a generic plugin framework. KISS/YAGNI govern: only what Topstep forces gets built.

## 1. Design principle

- Add a NEW package and NEW CLI commands; do not mutate `internal/sim` behavior, types or tests. Zero-diff on `internal/sim` is a Shot A exit criterion and a Shot B verification target.
- The engine remains event-driven over an exact kernel: no tick simulation, no Euler path approximation as production reference (Euler is acceptable only inside Shot B oracle tooling as a contrast, never as the product sampler).
- M1A needs ONLY the 1D killed-Brownian kernel: every M1A phase (Combine, XFA) has a floor that is constant within a session (EOD trailing updates between sessions), so the `(e,m)` running-maximum kernel is out of scope by construction.
- All Topstep rule values and prices live in versioned, serializable inputs traceable to §D5.2A; nothing is hard-coded as semantics.

## 2. Repository shape

```text
go.mod                              (unchanged module github.com/xKoRx/echo-futures)
cmd/sim/main.go                     (add subcommand routing only)
internal/sim/**                     (UNTOUCHED — D4 legacy)
internal/topstep/
  rules.go        TopstepRuleSet, ConsistencyPolicy, WinningDayPolicy
  pricing.go      PricingSnapshot (+ bundled payout method fee schedule)
  session.go      SessionConfig, SessionClock
  kernel1d.go     FiniteHorizonKernel1D (exact law + realization)
  drawdown.go     TrailingDrawdownEOD
  history.go      DailyHistory, multisession sufficient state
  engine.go       session event loop + lifecycle state machine
  withdrawal.go   WithdrawalPolicy (MAX_ELIGIBLE), SettlementState
  ledger.go       personal cash ledger, I_act, C_path identity
  errorbudget.go  ErrorBudget, evidence labels
  experiment.go   ExperimentRunner (matrix driver)
  scenario.go     D5 scenario schema + strict validation
  *_test.go       fixtures S01–S26 subset + TS-F01..TS-F16 + unit tests
scenarios/topstep/  JSON fixtures + one matrix definition file
```

Names may differ only if the existing code makes another shape cleaner; the conceptual contracts of §4 are frozen. Files may be split when it makes tests clearer; no generic framework packages.

## 3. CLI

Single binary `sim`. Existing commands and flags keep their exact D4 behavior:

```text
sim validate --runs 1000000 --seed 42 [--format text|json]        # D4 T1–T8, unchanged
sim simulate / sim cohort                                          # D4, unchanged
```

New D5 commands:

```text
sim topstep --scenario <file.json> [--runs N] [--cohorts M] [--seed N] [--format text|json]
sim validate-d5 [--format text|json]        # full D5 fixture suite (S-subset + TS-F01..16)
sim experiment --matrix <file.json> [--seed N] [--format json]    # 30-point matrix driver
```

CLI flags may override runs/seed/format only; every business/model parameter comes from versioned scenario JSON with strict decoding (unknown fields rejected, NaN/Inf rejected, invalid ordering rejected, `delta≠0` rejected in D5 mode). Invalid config → non-zero exit with a precise message. `--format json` emits the machine-readable result including the ErrorBudget block; text mode is a concise summary.

## 4. Conceptual components

| Component | Frozen contract (minimum) |
|---|---|
| SessionConfig | active windows per weekday, IANA tz + pinned tzdb version, holiday/early-close calendar id+version, publication offset (16:00 CT), news windows = none in M1A, `νProfileId` + frozen shape |
| SessionClock | bidirectional map calendar time ↔ variance time by consuming σ_z(t); exposes remaining variance V to the next exogenous cut; billing clock (FIXED_30D anniversaries from purchase) runs in parallel and never affects variance time |
| FiniteHorizonKernel1D | exact killed-Brownian law per §5; input `(a, x, b, V)` in equity-variance units; output exactly one branch: `EVENT{side, τ_var, level}` or `SURVIVED{endpoint}` with the joint law of §5.4 |
| SessionState | LOCAL DIFFUSION STATE per C1: phase-relative equity `e`, current floor `F`, trade state `(h, b, next add, TP/SL levels)`, remaining variance `V` |
| DailyHistory | closed-day series sufficient state per C1: `P` (cumulative phase PnL), `N` (activity days), `A = max(0, d_j)` — NEVER omitted (S19 negative fixture), `B_open`, `H_EOD`, and for XFA `W`; no duplicated coordinates (P is not stored beside an identical e) |
| TrailingDrawdownEOD | ratchet `H_j = max(H_{j−1}, B_close,j)`, `F_j = min(0, H_j − 2000)`, lock flag; revalidation after update; XFA payout forces `F = 0` |
| ConsistencyPolicy | predicate on closed snapshots: `N≥2 ∧ P≥3000 ∧ A ≤ 0.55·P`; effective target `max(3000, A/0.55)`; strict comparison semantics per G53-09 (no epsilon) |
| WinningDayPolicy | `W += 1{activity ∧ d ≥ 150}` with 16:00 publication gate; reset after payout |
| TopstepRuleSet | versioned fields traceable to §D5.2A rows: target 3000, MLL 2000 EOD-trailing + real-time enforcement, minimum days 2, consistency 55%, winning days 5×150, request window Sun 17:00–Fri 17:00 CT, gross cap 2000, min request 125, split 90%, first-payout MLL→0, no consistency in XFA Standard, no DLL, no resets in-attempt; `ruleSetId` + `captured_at` |
| PricingSnapshot | `TOPSTEP_STANDARD_CURRENT`: purchase 49/30d FIXED_30D, renewal 49/30d, activation 149, funded fee 0; `snapshotId`, `captured_at=2026-09-24`, currency USD, source refs, confidence; separate test-only snapshots allowed for S14/S20 fixtures, always labeled non-product |
| WithdrawalPolicy | `policyId=MAX_ELIGIBLE`: eligibility state machine (`NOT_ELIGIBLE → AWAITING_PUBLICATION → PAYOUT_ELIGIBLE → PENDING_REQUEST → PENDING_RECEIPT`), `requested_amount = floor_cent(min(0.5·B, 2000))` with `R ≥ 125` and positive external cash; method fee schedule (frozen reference Aeropay 0); flatness from decision to receipt |
| SettlementState | `IDEAL_COMPLIANT` profile: deterministic approval (instant) + remittance latency (frozen 3 business days); states REQUESTED/APPROVED/RECEIVED; no rejection paths in M1A; conditional-results labeling |
| ErrorBudget | the seven components of §8 with per-observable global budgets and evidence labels |
| ExperimentRunner | drives the 30-point matrix (6 ν × 5 add counts), cohort loop with censoring, aggregate reporting per Functional SPEC §9 |

## 5. Finite-horizon 1D kernel (accepted law, verbatim contract)

### 5.1 Law

For state `x` interior to `(a, b)`, `ℓ = b−a`, `r = (x−a)/ℓ`, `λ_n = n²π²/(2ℓ²)`, variance horizon `V`:

- surviving endpoint density: `k_V(x,y) = (2/ℓ) Σ_{n≥1} sin(nπr) sin[nπ(y−a)/ℓ] exp(−λ_n V)`, `a<y<b`;
- survival mass: `Q_x(V) = (2/π) Σ_{n≥1} [(1−(−1)^n)/n] sin(nπr) exp(−λ_n V)`;
- exit fluxes per unit variance: `f_a(v|x) = (π/ℓ²) Σ_{n≥1} n sin(nπr) exp(−λ_n v)` and `f_b(v|x) = (π/ℓ²) Σ_{n≥1} (−1)^(n+1) n sin(nπr) exp(−λ_n v)`;
- cumulative sub-CDFs (preferred for sampling/inversion — no v=0 singularity): `U_x(V) = r − (2/π) Σ_{n≥1} [(−1)^(n+1)/n] sin(nπr) exp(−λ_n V)`; `L_x(V) = 1−r − (2/π) Σ_{n≥1} [1/n] sin(nπr) exp(−λ_n V)`;
- identities: `Q_x(V) + ∫_0^V (f_a+f_b) dv = 1`; `U_x(∞) = r`, `L_x(∞) = 1−r` (D4 marginal recovered); mean exit time `(x−a)(b−x)` in variance units; `U'_x = −f_b`, `L'_x = −f_a`.

Units: the kernel is stated in PRICE-variance with generator ½∂yy; in EQUITY coordinates with `de = h·dW_v` use `h²V` in the unit kernel (or equivalently coefficient `h²/2`); NEVER multiply twice by h² and never confuse price variance with equity variance. The variance clock conversion to calendar time flows through σ_z(t).

Anchors (machine-precision, from the GOD review, for fixture S03/S01): `a=0,b=1,x=.25`: `V=.1` → `Q=.553175891850086`, `L=.429195269138053`, `U=.0176288390118612`; `V=1` → `Q=.0064749699291492`, `L=.746762514183855`, `U=.246762515886996`.

### 5.2 Realization

- Dual representation with frozen crossover: method of images for small `V` and spectral series for large `V`, each with an explicit truncation bound (`ε_kernel` per call); series term count chosen so the declared tail bound holds; NO silent clipping, NO renormalization.
- Event sampling must preserve the JOINT law: the measure is the disjoint mixture `f_a(v)dv·δ_a ∪ f_b(v)dv·δ_b (0<v≤V) ∪ k_V(x,y)dy`. Allowed sampling orders: (side, then time from that side's conditional CDF) or (exit time from `U+L` inversion, then side by `f_b/(f_a+f_b)`); the survival branch samples the endpoint from `k_V/Q_x(V)`. It is FORBIDDEN to pick the side from `r` independently of the finite-horizon duration, or to sample time independently of side.
- Boundary and degenerate cases are handled by deterministic operators, never by tolerance: a state initialized on an absorbing boundary is absorbed at variance time 0; `V = 0` is the identity (no business events, no RNG consumption); the limits `x → boundary` and `V → 0` are non-uniform and must not be patched with an epsilon tie.

### 5.3 Invariants asserted by tests

`Q_x + L_x + U_x = 1` within declared bounds; no negative masses; endpoint conditional density interior; semigroup composition `K_{u+v} = K_u·K_v` at observation-only boundaries; conservation of the D4 marginal as `V → ∞` (S01); anchor values of §5.1 reproduced within arithmetic precision of the contract.

## 6. Session engine (event loop)

Within a session the engine reuses the D4 trade mechanics unchanged: bookkeeping `Y = b + h·s` with self-financing adds (`h' = h+Δh`, `b' = b−Δh·s`, `Y` conserved), trade barriers at `±(G or L)` in trade space, phase floor as terminal lower barrier (replacing D4's static `−Drawdown` by the current `F`), priority `phase-loss > trade-close > add`, geometric ties resolved deterministically (SL=floor ⇒ loss; TP=lock ⇒ lock updates and trade closes; hard close ⇒ no add, no reopen) — G53-05/S22.

Per trade segment: compute terminal lower/upper in price space exactly as D4 §7 (with `F` in place of the static phase drawdown; the phase UPPER absorbent barrier is disabled in prop EOD mode — pass is an EOD event, not an intraday absorption); eligible adds remain strictly between terminal lower and current price; call the kernel with `V` = remaining session variance; consume the sampled branch; on EVENT apply priority and update; on SURVIVED hold the conditioned endpoint for the boundary action.

Session close sequence for survivors (frozen order, from planner §A5):

1. Intraday breach resolution already has absolute priority and cannot be rescued by the endpoint.
2. Liquidate the surviving position at its conditioned endpoint `S_close`; cancel orders; `B_close = E_close`; no PnL during the 15:10–16:00 dead zone.
3. `d = B_close − B_open`, excluding personal-cash debits; M1A execution costs are 0.
4. Update counters: `N += 1{activity}`; `A ← max(A, d, 0)`; XFA only: `W += 1{activity ∧ d ≥ 150}`; each session_id at most once; losses never reduce `A` or `W`.
5. Apply the EOD ratchet (`H, F` update + lock) and revalidate solvency (a survivor cannot be killed by the ratchet); register lock transitions.
6. Evaluate pass (evaluation phase) or payout eligibility (XFA phase) ONLY on the published snapshot (16:00 CT); on pass: EVALUATION_PASSED → activation (I_act, −149) → state reset per Functional SPEC §6.2; no evaluation profit transfer; no XFA second ratchet (EOD trailing only, floor already constant within day).

Billing clock: the renewal anniversary set `{purchase + 30d·i}` is checked at each calendar-day boundary while the evaluation is active; a charge is emitted unless the subscription was cancelled on or before that date (cancellation wins ties, SD-3); renewals accumulate in `C_path`.

## 7. Multisession sufficient state (C1 — mandatory)

The lifecycle/policy state consumed across sessions is, at minimum: cumulative phase PnL `P`; trading-day count `N`; best closed-day profit `A` (never omitted — S19 negative fixture `[1700,700,600]` vs `[1400,900,700]` must remain distinguishable); XFA winning days `W`; trailing floor/lock (`H, F, locked`); current phase; activation state `I_act`; payout/settlement state (eligibility → request → approval → receipt); renewal/billing state (purchase date, anniversaries charged); XFA balance `B` and (continuation-only) net-since-last-payout. The oracle and any alternative evaluator must carry the same sufficient state; a 1D diffusion state plus integer counters is NOT sufficient where `A` matters (G53-01).

## 8. Error budget and reporting (C2 — mandatory)

Components declared separately: `ε_kernel` (per call/solver), `ε_history` (continuous-history representation), `ε_composition` (accumulation over K composed transitions: with uniform total-variation bounds δ_i the law error is bounded by Σδ_i; no cancellation assumed; random K requires tail control or explicit truncation with residual mass), `ε_truncation` (domain truncation), `ε_horizon` (unresolved mass at horizon), `ε_oracle` (independent-oracle residual), `ε_MC` (statistical). For bounded payoff `g`: `|E_P[g] − E_Q[g]| ≤ (sup g − inf g)·TV(P,Q)` — a 1e-4 law error on a $2,000-range payoff admits $0.20 and is NEVER presented as cent precision.

Per-observable budgets frozen at freeze time: (A) analytic/local probability fixtures: global fixture error ≤ 1e-4; (B) end-to-end `q_withdraw`: screening tolerance 1e-3 allowed ONLY labeled exploratory; the certification tolerance is frozen BEFORE results are observed; (C) expected cash: controlled directly or via a law-distance compatible with the payoff range; (D) tails/quantiles: censoring-aware CDF bounds. Deterministic ledger identities are EXACT to the arithmetic contract and consume no tolerance. Every reported error carries its label: `RIGOROUS_BOUND` (enclosure/error theorem), `EMPIRICAL_CONVERGENCE` (refinement study Δ, Δ/2, Δ/4) or `MONTE_CARLO_UNCERTAINTY` (SE/CI). Local kernel accuracy is never promoted to an end-to-end q guarantee.

## 9. Economics and ledger

- `I_act = 1{activation completed}` (lifecycle indicator, price-independent); `J = 1{WITHDRAWAL_RECEIVED}`; `J ≤ I_act` always (S12/S20).
- Personal cash: `C_path = F_initial + Σ renewals_before_cancellation + I_act·activation_fee(snapshot) + other_personal_costs` (M1A: other = 0); attempt identity `K = −C_path + J·c` with `c = 0.9·R − f_method`. Nominal 50,000 never appears as personal cash; nominal equity and personal cash are separate ledgers.
- Pricing identity control (S14 adapted): on identical paths with only the snapshot varied, `ΔK = −[ΔF_init·(1) + n·ΔRenewal + I_act·ΔActivation]`; renewal counts identical because the billing clock is cash-independent.
- D4 legacy invariant `J ≤ I` in `internal/sim` is untouched; D5 uses the corrected `I_act` semantics.
- Requests are rounded `floor_cent` AFTER the martingale/consistency arithmetic (never round equity, barriers or consistency comparisons).

## 10. Reproducibility

Byte-reproducible output in the same supported environment from: scenario (strict JSON, schema versioned) + seed + versioned ids: `ruleSetId`, `pricingSnapshotId`, `calendarId` + tzdb version, `νProfileId`, `kernelId` + tolerances, payout `methodId`, `budget` declaration. RNG: per-attempt substreams derived deterministically from the master seed and attempt index (attempts are independent; parallel execution is permitted ONLY via attempt-indexed substreams; a serial single-stream reference mode must remain available). D5 must reproduce its own bytes; no byte-equality is promised between D4 and D5 sampling (sampling consumes RNG differently); the required engine-to-engine equality is of LAW, checked by the fixtures.

## 11. Legacy compatibility

- `internal/sim` and both D4 SPEC behaviors remain untouched; T1–T8 keep their certified expectations; `sim validate` output format is unchanged.
- The Topstep package MAY call exported pure functions of `internal/sim` (e.g. `HitUpperProbability`) without modification; unexported helpers are duplicated locally rather than exported ad hoc.
- Static-barrier marginal recovery (S01) holds when sessions, gates, trailing, flatten and forced liquidations are all disabled and the first horizon goes to infinity — the D5 kernel degenerate configuration, asserted as a test, not as a runtime mode combination users are expected to run.
- The D4 legacy mode needs no session simulation and its contract is unaffected by any of the above.

## 12. Testing and quality gate

- `go test ./...` and `go test -race ./...` stay green including D4.
- D5 fixture suite (`sim validate-d5`): S01–S08, S11–S12, S14–S20, S22, S25–S26 (per the applicability table in the Functional SPEC §11.2) + TS-F01..TS-F16, each printing expected, observed, tolerance/budget, evidence label and PASS/FAIL; DEFERRED ids are listed as DEFERRED, never silently absent.
- Coverage of `internal/topstep` ≥ 95%, critical paths first (kernel joint law, ratchet/lock, consistency equality/strictness, billing ties, censoring); no meaningless coverage.
- Determinism: same seed + config ⇒ byte-equal JSON (TS-F16); machine anchors of §5.1 asserted at arithmetic precision.

## 13. No tocar / stop conditions

Do not touch: xKoRx/echo; Echo Forge; NinjaTrader; `internal/sim` behavior; D4 scenario files; Agents-OS core beyond the allowed planner/SPEC surfaces; remote systems; credentials. STOP with PLAN_CONFLICT (no silent reinterpretation) if: the accepted kernel law cannot be realized within the frozen error budget; the session composition cannot preserve the frozen event priority or joint law; TPT/`(e,m)` support is found necessary for any M1A fixture; a rule field cannot be traced to §D5.2A; the manager has not accepted the freeze.

## 14. Shot dispatch packages (prepared, NOT executed)

### 14.1 SHOT A — Implementation

- /goal: implement the D5-M1A Topstep capability exactly per the two frozen M1A SPECs on the certified D4 baseline; deliver the fixture suite green, the matrix runner, and decision-quality execution readiness for `q_withdraw(ρ, add_count)`.
- /authorities: [[D5-M1A — Topstep Functional SPEC]]; [[D5-M1A — Topstep Technical SPEC]]; planner §D5.3 (C1–C6) as mathematical authority; §D5.2A as rules authority; D4 SPECs as legacy contract.
- /baseline: repo xKoRx/echo-futures at `master = d4f42a41946f12231b75e4eb65b90d132731be0d` plus the SPEC-freeze commit SHA recorded at dispatch; work on branch `feature/d5-m1a-topstep`.
- /frozen: D4 CLOSED; model class and kernel formulas; rule values (§D5.2A); pricing snapshot; lifecycle; trade-policy family (as ratified, SD-1); ν grid and profile shape (SD-2); billing conventions (SD-3); payout method (SD-4); error-budget semantics; MAX_ELIGIBLE; no TPT, no Tier-2, no delta≠0, no execution costs.
- /scope: everything in Technical SPEC §2–§12 and nothing else: `internal/topstep`, three new CLI subcommands, fixtures, matrix runner, README section; no policy optimization, no performance rewrites of D4, no extra providers.
- /execute: fixture-first TDD (S-subset + TS-F01..16 red → green); implement kernel dual-representation with declared `ε_kernel`; engine + state machine per §6–§7; ledger + `I_act`; ExperimentRunner; run `sim validate` (T1–T8 unchanged) + `sim validate-d5`; sample matrix run per Functional SPEC §10 with uncertainty reporting.
- /verify: full suite green including D4; race clean; coverage ≥95% new package; zero-diff `internal/sim`; determinism byte-equality; error budgets declared per observable with labels; evidence package per D4 §16 pattern (repo path, branch, HEAD, go version, test/race/coverage, fixture outputs, sample matrix output, known limitations); gate `D5_TOPSTEP_IMPL_PASS → REVIEW`.
- /reuse: exported pure functions of `internal/sim` unmodified; D4 scenario/CLI/JSON conventions; D4 evidence and README formats; the GOD anchors of §5.1 as fixed test vectors.
- /improve: record improvement candidates (performance, API ergonomics) in the delivery notes WITHOUT implementing them.
- /close: exact commit SHA handed to Shot B; planner updated; no self-acceptance of any gate.

### 14.2 SHOT B — Independent adversarial verification

- /goal: independently falsify the exact Shot A commit against the frozen SPECs and the accepted mathematics; produce ranked regressions; fix NOTHING in product code.
- /authorities: same as Shot A, plus the GOD numerical-oracle contract (planner §Numerical oracle verdict) as the verification-method authority; verification surface = the exact Shot A commit SHA.
- /baseline: Shot A commit pinned read-only; a separate verification workspace (module or package outside the product import path of the kernel) for oracle code.
- /frozen: same frozen set as Shot A; the Shot A commit is immutable during the shot; no product code changes, no fixes, no config nudges.
- /scope: (1) independent numerical oracle for the 1D kernel and session composition — CTMC/finite-volume backward induction with the multisession sufficient state of §7 (history dimensions refined independently per G53-01), NOT reusing the production kernel's crossing/sampling routines; (2) analytical controls: S01 marginal, S03 mass identities with sub-CDFs by side, semigroup composition, S26 scale invariance, mean exit time; (3) adversarial determinism/RNG-order hunting, boundary/tie probing beyond the fixture set; (4) censoring and ledger identity audits; (5) independent re-computation of a q/`cash_EV` subset of the matrix for bracketing within declared budgets.
- /execute: convergence contract per GOD (Δ, Δ/2, Δ/4 refinements, barrier alignment/sensitivity, domain truncation with escape mass, positivity/conservation checks, joint-distribution comparison — not q alone); comparison against production with the C2 budget inequality; Monte Carlo contrast with explicit SE.
- /verify: PASS/FAIL verdict per checked contract with evidence; regression list ranked by decision impact (kernel law > lifecycle state > economics > reporting); each regression reproducible from a pinned command.
- /reuse: GOD verdict formulas and anchors; D4 tests as regression canaries; the production test harness only as a runner, never as a source of truth.
- /improve: verifier tooling notes reusable for M1B.
- /close: verification report with accepted-regression list handed to Shot C; no merges, no gate self-service.

### 14.3 SHOT C — Correction + certification

- /goal: absorb exactly the accepted Shot B regressions and produce the final certification of the M1A capability.
- /authorities: same as Shot A/B; the accepted-regression list is binding scope.
- /baseline: Shot A branch; each fix references its Shot B regression id.
- /frozen: no new features, no policy/rule changes, no model-class changes; a change that would touch kernel mathematics, event semantics or the error-budget contract reopens PLAN_CONFLICT instead of being absorbed silently.
- /scope: accepted regressions + their new/extended fixtures + documentation deltas only.
- /execute: fix, extend fixtures to prevent recurrence (regression tests red on the old commit, green on the new), re-run the full suite and an independent spot-check of each fix.
- /verify: full suite (D4 + D5) green; race clean; coverage maintained ≥95%; determinism re-proven; certification statement with baseline SHAs (SPEC freeze, Shot A, Shot B report, Shot C final), error budgets per observable and evidence labels.
- /reuse: Shot A/B artifacts; GOD anchors; D4 evidence patterns.
- /improve: record residual risks and M1B carry-overs (TPT kernel, `(e,m)` fixtures) explicitly.
- /close: `D5_TOPSTEP_IMPL_PASS` decision-ready for manager acceptance; planner and memory updated; matrix execution authorization requested separately (execution of the 30-point experiment is NOT part of Shot C closure).


## Owner Policy Override — D5-M1A-P Topstep Discrete Policy Economics — 2026-09-24

This override is owner-authorized and supersedes the previous immediate M1A experiment matrix, without deleting the accepted Brownian/session model. The Brownian kernel remains the later realism path; the next 3-shot milestone is a bounded discrete-policy economics experiment designed to answer the owner's exact Topstep question quickly and reproducibly.

### Primary policy

Provider/product:
- Topstep 50K Trading Combine Standard → XFA Standard.
- pricing: $49 evaluation, $149 activation.
- payout: 50% of XFA balance capped at $2,000 gross, 90/10 split.
- Chile reference settlement: Wire/SWIFT fee $30; report gross, trader-after-split, and external-cash-received separately.

Trading Combine:
- target day 1: +$1,500 before max loss / MLL failure;
- target day 2: +$1,500 before max loss / MLL failure;
- both successful days satisfy 50% best-day share, inside the 55% consistency target;
- a loss outcome in either day is BURNED for this policy;
- pass probability under linked Bernoulli hit-rate p is analytically p².

XFA payout cycle #1:
- first funded trading day: target +$4,000 before $2,000 loss; success counts as winning day #1 and locks MLL at $0 at EOD;
- then require 4 additional winning days to reach the first five-day requirement;
- harvest-day win = +$500;
- harvest-day loss cap is configurable and is a FIRST-CLASS experiment input, not fixed: $500 / $1,000 / $1,500 / $2,000;
- after winning-day eligibility is satisfied, continue until XFA balance >= $4,000 if necessary, then request exactly $2,000 gross;
- first payout external reference cash = $2,000 - 10% split - $30 Wire/SWIFT fee = $1,770.

XFA payout cycles #2+:
- after each payout, MLL remains $0 and the winning-day counter resets;
- require FIVE NEW winning days >= $150, not four;
- same +$500 / configurable-loss harvest process;
- require positive net profit since previous payout and balance >= $4,000 before requesting the fixed $2,000 gross;
- payout request day does not count toward the next five-day cycle.

Payout horizon:
- primary owner policy: STOP_AFTER_3_PAYOUTS;
- hard configurable maximum: 4;
- payout #4 is sensitivity only;
- never intentionally burn an XFA to free a slot; STOP means stop trading that account. Vendor call-up remains external/censored because Topstep does not publish a deterministic payout-count threshold.

Probability inputs:
- primary linked hit-rate p applies to the abstract daily objective event in all stages;
- grid: 0.50, 0.51, 0.525, 0.55, 0.575, 0.60, 0.625, 0.65;
- implementation MAY expose stage-specific p_eval / p_bulto / p_harvest overrides, but primary reports keep them linked;
- p is explicitly "probability that the session policy hits its positive target before its loss cap", NOT raw per-trade win rate and NOT a claim of market edge.

Portfolio:
- normalized month = 20 trading sessions plus actual-calendar mode;
- 5 concurrent account pipelines;
- modes: INDEPENDENT and PERFECT_COPY;
- after evaluation/XFA natural burn, a new Combine may start next trading session;
- after STOP_AFTER_N, that XFA remains stopped and continues occupying an XFA slot unless an external closure/call-up is supplied;
- report same-day multiple-MLL events because Topstep currently identifies multiple accounts hitting MLL in one day / account stacking patterns as responsible-trading/compliance risk.

### Required output

For every (p, harvest_loss, max_payouts, correlation_mode):
- p_pass;
- P(payout #1/#2/#3/#4 | evaluation);
- P(payout #1/#2/#3/#4 | activated XFA);
- evaluations purchased;
- activations;
- XFA burns;
- payout count;
- external cash received;
- evaluation + activation costs;
- net economic P&L;
- 20-session expected monthly P&L with 5 pipelines;
- P(month > 0), P5/P50/P95;
- probability of >=1 payout;
- account-days / payout;
- same-day multi-MLL count/rate;
- stopped-XFA slot occupancy;
- requested/approved/received amounts separately;
- settlement-latency sensitivity for international Wire/SWIFT.

### Interpretation guard

This is a synthetic POLICY hit-rate experiment. At p=0.50, asymmetric outcomes such as +$500/-$2,000 are NOT zero-EV trading; their nominal one-day expectancy is negative. The experiment asks whether prop contractual asymmetry can nevertheless make PERSONAL CASH EV positive. It must not be labeled a fair-market Brownian result or empirical strategy evidence.

### Three-shot delivery

Exactly three shots:
A. implement discrete policy engine + exact/DP reference + MC/monthly portfolio runner;
B. independently falsify probabilities, ledger, payout cycles, correlation and official-rule semantics; no product fixes;
C. correct accepted findings, certify, and RUN the full p × harvest_loss × payout_horizon × correlation matrix. Shot C must deliver the final decision table; no fourth shot.

Gate:
`D5_TOPSTEP_POLICY_SPEC_PASS = ACCEPTED_BY_OWNER`.
`D5_TOPSTEP_POLICY_IMPL_PASS = PENDING`.
Next action: DISPATCH_SHOT_A.
