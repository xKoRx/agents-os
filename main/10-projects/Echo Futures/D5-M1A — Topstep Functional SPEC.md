---
type: spec
schema_version: 1
status: review
area: "[[Echo]]"
related:
  - "[[Echo Futures]]"
  - "[[Echo Futures — D5 Prop Economics]]"
  - "[[D5-M1A — Topstep Technical SPEC]]"
  - "[[D4 — Simulator v0 Functional SPEC]]"
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

# D5-M1A — Topstep Fast Track — Functional SPEC

## 0. Authority

This SPEC freezes externally observable behavior of the D5-M1A Topstep experiment. Authorities, in order:

1. [[Echo Futures — D5 Prop Economics]] §D5.3 — accepted session-aware mathematical model (GOD Mathematical Review verdict + corrections C1–C6 + Manager Acceptance D5.3 Session Model PASS = ACCEPTED). Mathematical authority; nothing here may reinterpret it.
2. [[Echo Futures — D5 Prop Economics]] §D5.2A — Topstep 50K Standard rule packet, `captured_at=2026-09-24`, official sources only. Product-rules authority; every rule field below traces to a captured row.
3. [[D4 — Simulator v0 Functional SPEC]] and [[D4 — Simulator v0 Technical SPEC]] — certified legacy baseline `d4f42a41946f12231b75e4eb65b90d132731be0d`. D4 remains CLOSED.
4. This SPEC — user-visible behavior of the D5 mode.

If implementation evidence contradicts the mathematical authority, STOP with PLAN_CONFLICT; do not reinterpret the math. Pricing is a versioned snapshot, not permanent provider semantics.

Gate: `D5_TOPSTEP_SPEC_PASS = REVIEW`. Nothing in this SPEC authorizes implementation until the manager accepts the freeze. This document contains no code, no executed simulation, no empirical market claim, and no Tier-2 content.

## 1. Outcome

Deliver a deterministic simulation capability that answers, under the accepted structural-null session-aware model:

> Of X evaluations Topstep purchased, how many reach a first real withdrawal, and what is the cash EV?

The primary decision surface is `q_withdraw(ρ, add_count)` plus `cash_EV(ρ, add_count)`. M1A is a structural-null decision surface, not an empirical profitability claim: it can answer whether Topstep contractual asymmetry alone produces positive personal cash EV under the frozen null/session policies, and which ν regions are viable. It does NOT prove that any real strategy has those ν, edge, fill quality or operational compatibility.

## 2. Scope

Frozen product: **Topstep 50K Trading Combine — Standard purchase path ($49 / 30d + $149 activation) → 50K Express Funded Account (XFA) — Standard payout path.** Pricing snapshot `TOPSTEP_STANDARD_CURRENT` (`captured_at=2026-09-24`): purchase 49 USD per 30-day cycle, renewal 49 USD per 30 days while the evaluation is active, activation 149 USD one-time per XFA earned, funded account has no monthly fee, no DLL add-on.

In scope (M1A only): the full lifecycle from `PURCHASE_EVALUATION` to `WITHDRAWAL_RECEIVED | BURNED | INCOMPLETE` under the structural null; the frozen reference TradePolicy family; add-count modes 0–4; the ν sensitivity grid; cohort economics with censoring; the acceptance fixtures in §11.

Explicitly deferred from M1A (no implementation, no research, no execution): TPT entirely (Test and PRO), the TPT PRO `(e,m)` running-maximum kernel, TPT inside-buffer withdrawal policies, Take Profit Trader pricing snapshots, Tier-2 providers (Apex/MFFU/Tradeify), FTMO Futures, synthetic delta ≠ 0, execution commissions/slippage, Topstep resets/Back2Funded recovery (post-burn recovery is modeled only as a NEW purchased attempt), the DLL add-on, the No Activation Fee and Consistency XFA product variants, payouts #2 and beyond, multi-account/copy trading, empirical volatility calibration, Echo/NinjaTrader integration.

## 3. Structural null

The model is the accepted D5.3 structural null, unchanged:

- drift = 0 (no drift term in any phase);
- synthetic delta = 0; a D5 configuration with `delta≠0` is invalid and rejected (isolation fixture S16);
- nominal execution costs = 0: no commissions, no slippage, no exchange fees against nominal equity; every result is labeled `STRUCTURAL_NULL_ZERO_EXECUTION_COST` and must not be read as net-of-execution economics;
- personal cash flows remain active: evaluation purchase, subscription renewals, activation fee, payout method fee and payout receipt are real personal-cash events and are never mixed with nominal account equity.

All settlement-dependent results are conditional on `SettlementState = IDEAL_COMPLIANT` (approval and remittance occur with frozen deterministic latency; compliance/KYC satisfied). They are not empirical probabilities of receiving money.

## 4. Lifecycle

| State | Entry | Exit |
|---|---|---|
| PURCHASE_EVALUATION | attempt starts; personal cash −49 | subscription active at first session open |
| EVALUATION_ACTIVE | first Combine session opens | EVALUATION_PASSED (pass predicate) or BURNED (MLL breach) or INCOMPLETE (censored) |
| EVALUATION_PASSED | pass predicate true on a published EOD snapshot | Combine closes; subscription auto-cancels; evaluation profits are NOT transferred |
| FUNDED_ACTIVATED | activation completed: I_act=1, personal cash −149 (once per XFA earned) | XFA state initialized (§6.2) |
| FUNDED_ACTIVE | first XFA session opens | PAYOUT_ELIGIBLE, BURNED, or INCOMPLETE |
| PAYOUT_ELIGIBLE | eligibility conditions met on a published snapshot (§6.5) | WITHDRAWAL_REQUESTED, BURNED, or INCOMPLETE |
| WITHDRAWAL_REQUESTED | MAX_ELIGIBLE fires (§6.6); account held flat | WITHDRAWAL_APPROVED or (no clawback case modeled) |
| WITHDRAWAL_APPROVED | internal approval; balance debited, MLL forced to 0 | WITHDRAWAL_RECEIVED |
| WITHDRAWAL_RECEIVED | positive external cash arrives: J=1; terminal SUCCESS | — |
| BURNED | MLL breach in EVALUATION_ACTIVE or FUNDED_ACTIVE (or PAYOUT_ELIGIBLE before request); terminal FAILURE | — |
| INCOMPLETE | attempt alive or settlement pending at the declared censoring horizon; terminal-for-run, NOT failure | — |

Success = `WITHDRAWAL_RECEIVED` with positive external cash (J=1). Pass, activation, eligibility, request and approval are diagnostic states, never success. A pending receipt is never counted as received; an alive account is never converted to BURNED (S18/S25).

## 5. Evaluation phase — Trading Combine 50K Standard

### 5.1 Session boundaries

- A trading day runs 17:00 `America/Chicago` through 15:10 CT of the next enabled calendar day; no positions are held from one session to the next; weekends have no sessions.
- The session calendar (holidays, early closes) is a versioned input using IANA timezone identity and a pinned tzdb version; on an early close the forced flatten moves to 15 minutes before the early market close; holidays and early closes are exogenous windows and never create additional trading days.
- No news-event flatten windows are modeled in M1A.

### 5.2 EOD forced flat

- At the session boundary a surviving position is liquidated at its conditioned close price `S_close`; realized balance `B_close = E_close`; no price and no PnL are generated during the 15:10–16:00 interval; winning-day publication occurs at 16:00 CT.
- The frozen decision policy is EOD: pass and eligibility are evaluated on the complete daily snapshot, never on intraday extremes. The potential gap versus an early-flatten policy is real and must stay labeled, not optimized away.

### 5.3 Daily activity semantics

- `N` counts sessions with at least one executed round-trip; a session with 100 trades counts exactly once; a session without activity is not a trading day even if external credits exist.
- Daily profit `d = B_close − B_open` excludes personal-cash debits (renewals are never trading PnL).

### 5.4 EOD MLL update (trailing drawdown)

- `H_j = max(H_{j−1}, B_close,j)` with `H_0 = 0` (relative to phase start); `F_j = min(0, H_j − 2000)` with `F_0 = −2000`; equivalently `F_j = max(F_{j−1}, min(0, B_close,j − 2000))`. The floor never decreases; within day `j` the floor `F_{j−1}` applies.
- After the ratchet, solvency is revalidated against the new floor; a survivor can never be killed by the ratchet itself (no-PnL operation).

### 5.5 Intraday breach enforcement

- The current floor is constant within a session and equity is killed continuously against it, including unrealized losses (official: MLL monitored in real time); touching the floor liquidates the account for the rest of the day and terminates the attempt: BURNED. The final EOD endpoint can never rescue an intraday breach, and a breach has absolute priority over flatten, trade close and adds.

### 5.6 MLL lock

- When `H` reaches 2000 (nominal balance 50,000) the MLL locks permanently at 0 (relative): the floor is 0 forever; trades, days, payouts and time never move it down.

### 5.7 Consistency (55%)

- `A = max(0, d_1, …, d_N)` over closed days only; `P = B` cumulative realized phase profit. Pass requires `N ≥ 2` AND `P ≥ 3000` AND `A ≤ 0.55·P`.
- The effective target is `T_eff = max(3000, A / 0.55)` with no rounding; equality satisfies the rule (55% is a hard line); exceeding consistency never burns the account — it only blocks the pass until later days lower the ratio; losses never reduce `A`; the provisional intraday value `max(A_locked, d_current, 0)` is reporting-only and never substitutes the frozen closed-day `A`.
- The pass is not recognized for having touched 3000 intraday; only the published EOD snapshot passes (§5.2 policy).

### 5.8 Pass predicate and transition

- On a published EOD snapshot with `N≥2 ∧ P≥3000 ∧ A≤0.55·P`: state → EVALUATION_PASSED; the Combine closes and its subscription auto-cancels; evaluation profits are not transferred; the first 30,000-relative point of the XFA is a fresh account, not a continuation.
- Activation is modeled immediately at pass (frozen policy; no activation deadline exists in the captured authority — MISSING field, therefore not modeled as a constraint).

### 5.9 Renewal charging (billing)

- Renewal is 49 USD every 30 days measured from the purchase date (`FIXED_30D`); the billing clock runs on calendar days regardless of trading.
- A renewal falling while the evaluation is active is a real personal cost (fixture TS-F07); passing cancels the subscription so no further renewal is charged (fixture TS-F08); burning cancels the subscription by policy action at the burn (accrued renewals remain in `C_path`).
- Billing tie order (frozen convention SD-3): if a renewal anniversary coincides with the pass/burn cancellation date, the cancellation wins and no renewal is charged that day; a one-charge sensitivity is reported with the matrix.
- The engine must expose renewal counts per attempt as a required output.

### 5.10 Burn behavior

- MLL breach ⇒ BURNED; no reset, no rebuy and no Back2Funded exist inside an attempt; post-burn recovery is exclusively a NEW purchased attempt starting at PURCHASE_EVALUATION with a fresh pricing-snapshot instance.

## 6. XFA phase — 50K Standard

### 6.1 Activation transition

- EVALUATION_PASSED → FUNDED_ACTIVATED: `I_act = 1{activation completed}` (lifecycle indicator, independent of price); personal cash `−149` exactly once per XFA earned (fixture TS-F09); with a zero-activation-fee snapshot the indicator is still 1 and the debit 0 (contract fixture S20; mathematical fixture only, not a Topstep product claim).

### 6.2 State reset

- Phase equity reference resets to 0: the XFA nominal balance starts at 0 and the 50,000 is buying power, never personal cash and never a deposit.
- Fresh day history: `N_XFA = 0`, `W = 0`; drawdown state resets: `H = 0`, `F = −2000` (official: the XFA MLL starts at −2,000). No consistency gate exists in XFA Standard (frozen path). No evaluation state carries over.

### 6.3 XFA loss floor

- MLL is 2000, EOD trailing on the maximum balance with permanent lock at 0 once the balance reaches 2000 (the lock is the safety net: the account cannot fall below 0); identical ratchet/lock machinery to §5.4–5.6 applied to the XFA balance; breach ⇒ liquidation and permanent close ⇒ BURNED.

### 6.4 Winning-day count

- `W += 1{session has activity AND d ≥ 150}`; days need not be consecutive; each session_id counts at most once; a day locking 149.99 does not count; the count is published at the 16:00 CT day lock and is not usable before publication; the day of a payout request does not count toward the next cycle; `W` resets to 0 after each payout (continuation state; first withdrawal remains the only terminal success).

### 6.5 Payout eligibility

- First payout is EXEMPT from the positive-net-profit-since-last-payout rule; it is NOT exempt from balance sufficiency, the request minimum, the cap, the window or receipt.
- Eligibility on a published snapshot requires: `W ≥ 5`; request window open (Sunday 17:00 CT – Friday 17:00 CT, holidays excluded); compliance clean (IDEAL_COMPLIANT); `R ≥ 125`; strictly positive external cash after fees.

### 6.6 Withdrawal amount policy — `MAX_ELIGIBLE` (frozen)

- At the first eligible published snapshot, request `R = floor_cent(min(0.50 · B, 2000))` where `B` is the XFA balance relative to 0 (not 50,000 + profit); require `R ≥ 125` and external cash `c > 0`; otherwise remain eligible-and-waiting on later snapshots.
- This is a decision policy frozen for the experiment, not an optimum and not a firm rule; under flat processing and ideal settlement, changing `R` inside the allowed set does not change `q` up to the first receipt (B3 invariant, reported as a control, not a ranking).

### 6.7 Split and fees

- Trader entitlement `w = 0.90 · R` (90/10 split, trader keeps 90%); the legacy "100% of first $10,000" rule is out of the frozen path and NOT modeled.
- Payout method fee schedule is a versioned input; frozen reference method = Aeropay, fee 0 (SD-4); ACH/Wire ($30) and other methods are declared sensitivities outside the M1A matrix; external cash `c = w − f_method`; a request that would produce `c ≤ 0` is never made.

### 6.8 MLL effect after payout

- On approval: `B ← B − R` and the MLL is set to 0 permanently regardless of the prior ratchet height (fixture TS-F13); the remaining balance becomes the effective loss floor; the winning-day cycle restarts; the account remains open and tradable (continuation is outside the experiment horizon).

### 6.9 Receipt

- WITHDRAWAL_REQUESTED → WITHDRAWAL_APPROVED (balance debited, MLL forced 0) → WITHDRAWAL_RECEIVED when the external cash arrives (J=1). Processing latency is a frozen deterministic value (3 business days) under IDEAL_COMPLIANT; the account is held flat from decision until receipt; no trading and therefore no breach can occur while a request is pending; the wallet is never reused to purchase evaluations; a definitive rejection is not silently converted into BURNED (it is an explicit operational failure state; under IDEAL_COMPLIANT it does not occur).

## 7. Reference TradePolicy (frozen family — decision SD-1)

One reference family is frozen for the first experiment, derived from the D4 normalized scenarios (T2 lineage: ±100 monetary trade barriers, h0 = 1, adverse adds of 1 unit). These values are ONE explicit scenario decision for manager acceptance (SD-1); they are not optimized, not calibrated and not presented as market-representative:

| add_count k | adverse add levels | maxQty (1+k) |
|---|---|---|
| 0 | none | 1 |
| 1 | −30 | 2 |
| 2 | −30, −50 | 3 |
| 3 | −30, −50, −70 | 4 |
| 4 | −30, −50, −70, −90 | 5 |

- Trade target `G = 100`, trade stop `L = 100` (normalized money), initial qty `h0 = 1`, each add qty 1; adds are self-financing with D4 bookkeeping `Y = b + h·s`; ladder levels are strictly decreasing and the 3- and 4-add ladders are proposals (not defined by any authority — this is exactly why SD-1 exists).
- Reopen policy: open at session open; after a TP/SL close, reopen immediately while the session window remains open; no trades-per-day cap; no daily profit stop; no trading after the deadline (hard close, no reopen).
- Position limits: exposure always inside the frozen Combine maximum (5 minis / 50 micros equivalent; the 10:1 micro ratio is irrelevant in normalized money); no scaling plan is modeled (limits flat; XFA scaling tiers are out of M1A — exposure stays at h0/adds and never varies with balance).
- Session variance profile (SD-2): `σ_z(t)` is constant within each active window (frozen deterministic shape, single window per session); the scenario input is the adimensional `ρ_full = h_ref²·ν_full / D²` with `D = 2000`, i.e. full-session equity variance `ν_E = ρ_full · D²`; interpretation: full-session equity standard deviation `= sqrt(ρ_full) · 2000`; there is no hidden ν default — every scenario names its `νProfileId` and the grid values below.

## 8. Experiment modes

- Required modes: `add_count ∈ {0, 1, 2, 3, 4}`, all under `delta = 0` exactly.
- `delta ≠ 0` is invalid in the D5 mode and must be rejected at configuration time; D4 legacy retains its own synthetic-edge contract untouched.
- The experiment matrix is the cross product of §8 modes with the ν grid in §10: 30 scenario points; no full factorial over arbitrary stop/target/add parameters exists in M1A.

## 9. Required outputs

For every scenario point `(ρ, k)`, reported with uncertainty labels and censoring bounds:

- purchased evaluations, evaluation passes, funded activations, payout-eligible count, withdrawals received (counts);
- `p_pass = P(pass evaluation)`;
- `p_withdraw_given_funded = P(first withdrawal | funded)`;
- `q_withdraw = P(purchase → first withdrawal received)`;
- attempts per withdrawal (with interval `[1/q_U, 1/q_L]`; never a finite value derived from `q_L = 0`);
- failures per withdrawal; activations per withdrawal;
- `P(no withdrawal after 5 / 10 / 20 / 50 purchased evaluations)`;
- expected cash per evaluation; expected cumulative cash until first withdrawal; net cash per 10 and per 100 evaluations;
- cash P5 / P50 / P95 (before first withdrawal, with censoring-aware quantile bounds); attempts P5 / P50 / P95;
- trading days per withdrawal; renewal counts (mean and distribution summary);
- incomplete/unresolved mass (explicitly reported, never absorbed into success or failure);
- numerical uncertainty (component budget per §ErrorBudget of the Technical SPEC) and Monte Carlo uncertainty (SE/CI), reported SEPARATELY and both always present;
- sample-completion bound `qhat_final_sample ∈ [S/N, (S+U)/N]` and the population interval (η envelope or exact binomial), labeled as distinct objects (G53-03).

Every output carries its evidence label: `RIGOROUS_BOUND`, `EMPIRICAL_CONVERGENCE` or `MONTE_CARLO_UNCERTAINTY`. No output may describe itself as empirical, real-market, or net-of-execution profitability. The q=10% of D4 fixtures is a mathematical fixture, never a benchmark or prior.

## 10. Experiment matrix

- Sensitivity grid: `sqrt(ρ_full) ∈ {0.1, 0.25, 0.5, 1, 2, 4}`.
- Recovery ladders: add_count `∈ {0, 1, 2, 3, 4}`.
- `delta = 0` only. Primary output surface: `q_withdraw(ρ, add_count)` and `cash_EV(ρ, add_count)`.
- Execution contract: run sizes per point are frozen BEFORE observing results (certification tolerance per G53-02/C2(iv)); screening runs must report their η envelope (α=0.05) and the incomplete mass; six grid points do not certify monotonicity in ν, and q is not assumed monotone (consistency/ratchet make non-monotonicity possible).
- The matrix uses ONE trade-policy family (§7) and ONE withdrawal policy (MAX_ELIGIBLE); it does not create parameter families beyond the add-count variation.

## 11. Acceptance mapping

### 11.1 D4 legacy

T1–T8 remain unchanged and green; D4 commands, semantics and scenario files are untouched (verified by zero-diff on `internal/sim`).

### 11.2 D5 S-matrix — Topstep applicability

| ID | M1A state | Applicability / disposition |
|---|---|---|
| S01 | REQUIRED | static-barrier limit: sessions/gates/trailing off ⇒ D4 marginal; eval +3000/−2000 → 0.4; sub-CDFs by side per GOD |
| S02 | REQUIRED | zero/no-update: K0 identity; observation-only boundaries; semigroup without economic action |
| S03 | REQUIRED | finite-horizon mass: `Q_x + ∫(f_a+f_b) = 1`; joint time/side law; no negative mass |
| S04 | REQUIRED | EOD ratchet monotonicity (Topstep scale) |
| S05 | REQUIRED | lock permanence; XFA payout forces F=0 |
| S06 | REQUIRED | Topstep consistency: equality passes, exceed blocks, losses never reduce A |
| S07 | DEFERRED | TPT-only consistency predicate (M1B) |
| S08 | REQUIRED | activity/winning-day counting (XFA) |
| S09 | DEFERRED | `(e,m)` PRO intraday maximum (M1B) |
| S10 | DEFERRED | `(e,m)` drawdown analytical oracle τ_D/ζ (M1B; formulas remain frozen math, but their test target does not exist in M1A) |
| S11 | REQUIRED | self-financing adds + finite-horizon stopped martingale with closed sessions |
| S12 | REQUIRED | cash identity with corrected `I_act`: `K = −C_path + J·c` |
| S13 | DEFERRED | TPT PRO closure/age clock (M1B) |
| S14 | REQUIRED (ADAPTED) | pricing-snapshot identity in general form `ΔK = −[ΔF_init + n·ΔRenewal + I_act·ΔActivation]` on identical paths; the TPT numeric form `68(1+n)+130·I_act` is deferred to M1B |
| S15 | REQUIRED | chronology: DST, session boundaries, 16:00 publication, request window edges, no ghost events |
| S16 | REQUIRED | isolation/reproducibility: delta=0 null route; delta≠0 rejected; D4 T7/T8 intact; byte-equality same environment |
| S17 | DEFERRED | TPT WAIT⊂CLOSE policy coupling (M1B) |
| S18 | REQUIRED | censoring/IID: INCOMPLETE separate; corrected bounds; q=.1 as fixture only |
| S19 | REQUIRED | missing-history-A negative fixture `[1700,700,600]` vs `[1400,900,700]` |
| S20 | REQUIRED | zero-fee activation contract fixture (I_act independent of price) |
| S21 | DEFERRED | `(e,m)` singular maximum mass (M1B) |
| S22 | REQUIRED | geometric barrier ties: SL=floor, TP=lock; hard-close priority; deterministic operators |
| S23 | DEFERRED | S10 regime coverage (M1B) |
| S24 | DEFERRED | duration-sensitive resolvent (M1B) |
| S25 | REQUIRED | exact-mass vs MC censoring labeling |
| S26 | REQUIRED | adimensional scale-invariance `ρ_i = h_ref²ν_i/D²` |

Explicit statement per mandate: S09, S10, S21, S23 and S24 exist solely for `(e,m)` TPT PRO support and are DEFERRED from M1A to M1B; S07, S13 and S17 are TPT lifecycle/policy fixtures and are equally deferred. No TPT semantics are implemented in M1A.

### 11.3 Topstep end-to-end deterministic fixtures (new, mandatory)

| ID | Fixture | Expected |
|---|---|---|
| TS-F01 | evaluation pass | closed days with N≥2, P≥3000, A≤0.55P ⇒ EVALUATION_PASSED; subscription auto-cancels; no profit transfer |
| TS-F02 | evaluation burn | intraday floor touch ⇒ immediate BURNED; subscription cancelled at burn; accrued renewals in C_path |
| TS-F03 | 55% equality pass | days [1650, 1350]: P=3000, A=1650=0.55·3000 ⇒ pass (equality satisfies) |
| TS-F04 | >55% non-pass | days [1800, 1200]: P=3000, A=1800>1650 ⇒ not passed, account alive; subsequent +300 day (P=3300, A=1800≤1815) ⇒ passes |
| TS-F05 | MLL EOD movement | B EOD 0→800→300→2200→1000 ⇒ F: −2000→−1200→−1200→0→0; unrealized gain lost before EOD never raises F |
| TS-F06 | MLL lock | H reaches 2000 ⇒ F=0 permanent; later equity moves/payouts never lower it |
| TS-F07 | renewal before pass | attempt active across a 30-day anniversary ⇒ −49 charged, attempt continues |
| TS-F08 | pass before renewal | pass occurs before the next anniversary ⇒ no further renewal; auto-cancel |
| TS-F09 | activation paid once | pass ⇒ exactly one −149 (I_act=1); later XFA burn does not re-charge |
| TS-F10 | five winning days | day series ⇒ W=5 per §6.4 (149.99 fails; 100-trade day counts once; publication gate respected) |
| TS-F11 | payout gross cap | B=5000 ⇒ R=min(2500, 2000)=2000 (cap binds over the 50%) |
| TS-F12 | 90/10 split | R=2000, Aeropay ⇒ trader cash 1800 |
| TS-F13 | first payout MLL→0 | after approval: F=0 forced even if H<2000; B←B−R; W cycle reset |
| TS-F14 | WITHDRAWAL_RECEIVED cash identity | full path: K = −(49 + renewals) − 149·I_act + 1800·J; J≤I_act; 50K never appears as personal cash |
| TS-F15 | censored/incomplete attempt | alive-at-horizon ⇒ INCOMPLETE; excluded from success/failure; present in qhat bounds |
| TS-F16 | same seed deterministic output | same seed + config ⇒ byte-equal JSON; different seed ⇒ different stream |

## 12. Prohibited interpretations

- No output may be called empirical, real-market, or real-profitability evidence; the surface is `STRUCTURAL_NULL_ZERO_EXECUTION_COST`, conditional on IDEAL_COMPLIANT settlement.
- Pass and funded are diagnostic states; success is only WITHDRAWAL_RECEIVED.
- No prior or benchmark on q may be assumed from D4's q=10% fixture or from any marketing claim.
- The pricing snapshot is not an eternal tariff; rule values trace to the captured Topstep authority with `captured_at=2026-09-24`.
- TPT economics are not a byproduct of M1A.

## 13. Shots readiness

Shot A (implementation), Shot B (independent adversarial verification against the exact Shot A commit) and Shot C (correction + certification) packages are frozen in [[D5-M1A — Topstep Technical SPEC]] §14. All three are READY pending manager acceptance of this freeze; none is executed by this document.

## 14. Open decisions

- **SD-1 — reference trade-policy family values (§7):** ladders for k=2..4 (proposed prefixes of {−30,−50,−70,−90}; T3 alternative −20/−40 for k=2 recorded); G=L=100, h0=1, add qty 1. Manager ratifies or amends at gate acceptance.
- **SD-2 — ν profile shape (§7):** constant σ within the single active window; adimensional input `ρ_full` with `ν_E = ρ_full·D²`, D=2000; grid per §10. Manager ratifies or amends.
- **SD-3 — billing conventions (§5.9):** FIXED_30D anniversaries; cancellation wins a same-day rebill tie; one-charge sensitivity reported.
- **SD-4 — payout method reference (§6.7):** Aeropay fee 0 as the frozen reference method; other methods are sensitivities outside the matrix.

## 15. Explicit non-goals

TPT in any form; Tier-2; FTMO Futures; empirical strategy edge; synthetic delta; execution costs; Topstep resets/Back2Funded inside attempts; DLL add-on; product variants (No Activation Fee, Consistency XFA); payouts #2+; multi-account; historical data/backtesting; Echo/Forge/NinjaTrader changes; UI/service/database; production trading; volatility calibration from market data.


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


## Owner Policy Correction — D5-M1A-P150 — 2026-09-24

This section SUPERSEDES the prior D5-M1A-P harvest target of +$500. The correct owner policy uses the minimum Standard-XFA winning-day threshold: **+$150** on qualification days.

### Probability semantics

Primary sensitivity input:
`p_objective_hit = P(session policy hits its positive target before its declared loss cap)`.

This is NOT automatically raw per-trade win rate. A future hardscalping submodel may map `p_trade` and intra-session management into `p_objective_hit`; that mapping is outside this discrete-policy milestone.

Linked primary grid:
`p_objective_hit ∈ {0.50, 0.51, 0.525, 0.55, 0.575, 0.60, 0.625, 0.65, 0.70, 0.75}`.

Optional stage overrides remain allowed:
`p_eval`, `p_bulto`, `p_qualify`.

### Frozen owner policy

#### Trading Combine 50K
- Day 1 objective: +$1,500 before loss cap / MLL failure.
- Day 2 objective: +$1,500 before loss cap / MLL failure.
- Any natural MLL breach burns the evaluation.
- Two successful days yield total +$3,000 with largest-day share 50%, inside Topstep's 55% consistency target.
- Under linked p and one objective event/day, analytical fixture: `P(pass)=p²`.

#### XFA payout cycle #1
- XFA starts balance 0, MLL -$2,000.
- First funded session "bulto": target +$4,000 before $2,000 loss / MLL breach.
- Bulto success: balance=$4,000; this is winning day #1; at EOD MLL locks to $0.
- Bulto failure: natural XFA burn.
- Then require FOUR additional winning days with target +$150 each, because Topstep Standard requires five winning days >=$150 and the +$4,000 day already counts as day #1.
- Qualification-day loss amount is an explicit config. Primary owner case: `qualify_loss=2000`; sensitivities: 150, 300, 500, 1000, 1500, 2000.
- A qualification loss does NOT automatically mean burn unless balance reaches the MLL floor. Apply the actual balance debit and continue if alive.
- Once 5 winning days are complete, request the fixed $2,000 gross only when balance >=$4,000. If eligibility is complete but balance<4,000, continue the same qualification policy until balance>=4,000 or natural burn.

Expected no-loss path:
0 → +4000 → +150 → +150 → +150 → +150 = 4600;
request 2000 gross; post-payout balance=2600.

#### XFA payout cycle #2
- Winning-day counter resets to zero after payout #1.
- First post-payout session "reload bulto": target +$2,000; primary loss cap $2,000.
- If success from balance 2600: balance=4600 and counts as winning day #1.
- Then require FOUR additional +$150 winning days to reach five new winning days.
- Expected no-loss balance before request: 5200.
- Request fixed $2,000 gross; expected no-loss post-payout balance=3200.
- If reload bulto loses $2,000 but account remains above MLL, primary policy is `CONTINUE_IF_ALIVE`; do not invent an intentional burn. Continue qualification/recovery until eligibility + balance>=4000 or natural burn.

#### XFA payout cycle #3
- Same mechanics: counter reset; reload bulto target +$2,000 / primary loss cap $2,000; four additional +$150 winning days; then fixed $2,000 gross if eligible and balance>=4000.
- Expected no-loss balance path: 3200 → 5200 → 5800 → payout 2000 → 3800.
- Primary owner policy: `STOP_AFTER_3_PAYOUTS`.
- Payout #4 remains sensitivity only if requested by owner; no deterministic vendor call-up threshold is assumed.

### Official-rule semantics preserved

Current Topstep Standard XFA requires:
- 5 winning days of at least $150;
- days need not be consecutive;
- the payout-request trading day does not count toward the next five-day cycle;
- after each payout the 5-day count restarts;
- after the first payout there must be positive net profit since the previous payout;
- payout request is 50% of account balance up to the 50K Standard cap of $2,000;
- profit split is 90/10;
- MLL resets/locks at $0 after payout.

### Required experiment axes

Primary matrix:
- linked `p_objective_hit` grid above;
- `qualify_loss ∈ {150,300,500,1000,1500,2000}`;
- payout horizon = 3;
- payout #4 sensitivity;
- 5 account pipelines;
- 20-session normalized month plus explicit-calendar mode;
- INDEPENDENT vs PERFECT_COPY account correlation.

Required stage-level outputs:
- `P(pass)`;
- `P(bulto1 success | XFA)`;
- `P(payout1 | XFA)`;
- `P(payout1 | evaluation purchased)`;
- `P(payout2 | payout1)`;
- `P(payout3 | payout2)`;
- natural-burn probability in each stage;
- expected sessions in each stage;
- expected account balance entering/leaving each payout cycle.

Required portfolio outputs:
- evaluations/month;
- activations/month;
- XFA burns/month;
- payout1/2/3 counts;
- external cash/month;
- total fees/month;
- net cash/month;
- P(month>0), P5/P50/P95;
- active/stopped XFA slot occupancy;
- same-day multi-MLL diagnostics;
- break-even contour in (`p_objective_hit`, `qualify_loss`).

### Interpretation

At linked `p_objective_hit=0.50`, a +150/-2000 qualification objective has negative nominal expectancy; this experiment is intentionally testing whether Topstep's external payoff asymmetry can overcome that at the personal-cash level. Do not label it a fair-market trading result.

The accepted Brownian/session model is not deleted; it remains the later realism bridge. This P150 discrete policy is the immediate three-shot economics experiment.
