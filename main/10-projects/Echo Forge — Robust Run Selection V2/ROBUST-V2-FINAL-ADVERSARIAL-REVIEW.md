---

> **AUTHORITY NOTE — SUPERSEDED FOR IMPLEMENTATION (2026-09-30):** This document is retained as adversarial design history. Its mathematical findings remain evidence, including the derived-finiteness defect. The recommendation to introduce `evaluation_policy + evaluation_policy_version` is **rejected/superseded**. Canonical implementation authority is [[ROBUST-V2-DESIGN-FREEZE]]: V2 is another algorithm in the existing WFM config mechanism. Durable replay is not an implementation gate.

type: doc
schema_version: 1
status: active
area: "[[Echo]]"
project: "[[Echo Forge — Robust Run Selection V2]]"
related:
  - "[[ROBUST-V2-DESIGN-ITERATION-2]]"
  - "[[Echo Forge — Operación Real V2]]"
aliases:
  - Robust V2 Final Adversarial Review
tags:
  - kind/doc
  - area/echo
  - echo-forge
  - robust-run-selection
  - design-review
created: "2026-09-29"
updated: "2026-09-29"
---

# ECHO FORGE — ROBUST RUN SELECTION V2
# FINAL ADVERSARIAL DESIGN REVIEW

## 1. Executive verdict

~~~text
STATUS: DESIGN_ITERATION_REQUIRED
~~~

Iteration 2 survives the central architecture and stability-vs-quality attacks. Nested Ret/DD → auxiliary indifference is coherent; the exact Ret/DD-stability minimum does not have protected status once another candidate is inside epsilon_ret; center representativeness, auxiliary minimax and lexicographic quality remain defensible; V1/V2 coexistence is feasible without moving authority into select_robust_run.

The current mathematical contract does **not** survive unchanged because its +Inf sentinel can fail open.

When scale=0 and variation exists, D_x or C_x becomes +Inf and therefore R_x=+Inf. If every remaining candidate has R_retdd=+Inf, then ret_best=+Inf and the comparison +Inf <= +Inf + epsilon_ret is true under IEEE arithmetic. The same applies to R_aux. An infinitely unstable / undefined normalized candidate set can therefore reach quality.

That contradicts the fail-closed objective.

**Required correction:** before computing ret_best or aux_best, reject analytically every candidate for which any of R_retdd, R_sharpe, R_profit, R_aux or cliff is non-finite. If no candidate remains, the Strategy is an analytical FAIL.

This is one bounded semantic correction, not a redesign. No other material policy change is recommended.

## 2. Frozen Owner constraints

- V2 remains additive and explicitly selectable. Existing V1 identifiers keep V1 semantics.
- evaluate_wfm owns evaluation, admissibility, ranking and rank production.
- select_robust_run remains a consumer of the unique rank == 1.
- Scope remains strictly intra-strategy.
- Cliff and epsilon values are Owner semantic parameters, never tuned to historical winners.
- No product code and no SPEC freeze in this review.

## 3. Attack results 1–10

### Attack 1 — Ret/DD priority vs auxiliary band

**SURVIVES. Behavior is intended.**

Once two candidates are inside the Ret/DD indifference region, exact R_retdd ordering has no remaining semantic authority. Auxiliary stability is allowed to eliminate the exact R_retdd minimum.

Durable Strategy_1.8.669 example after cliff 35%:

| Candidate | R_retdd | R_aux | median Ret/DD | median Sharpe | median Profit |
|---|---:|---:|---:|---:|---:|
| 8/28 | 0.013369 | 0.019691 | 21.831445 | 1.22 | 13,578.40 |
| 9/28 | 0.023107 | 0.010917 | 21.552835 | 1.21 | 13,483.10 |

The R_retdd distance is about 0.009739. Once epsilon_ret admits 9/28, aux_best becomes 0.010917. For epsilon_aux below the ~0.008774 auxiliary gap, 8/28 is eliminated.

That is correct under indifference semantics. Protecting 8/28 merely because it is the exact minimum would make epsilon_ret partly ceremonial.

Contract: primary authority means candidates outside the Ret/DD equivalence region cannot influence later stages. It does **not** mean the exact primary minimum can never be eliminated.

### Attack 2 — Materiality parameters

**SURVIVES WITH CONTRACTUAL CLARIFICATION.**

epsilon_ret means the maximum additional normalized Ret/DD instability treated as materially equivalent. epsilon_aux means the maximum additional worst-dimension normalized auxiliary instability treated as materially equivalent. They are thresholds, not weights; no scalar compensation exists.

Monotonicity is local to each stage:

- increasing epsilon_ret only enlarges the Ret/DD-equivalent set;
- at fixed Ret/DD set, increasing epsilon_aux only enlarges the auxiliary survivor set.

End-to-end final membership is not monotone in epsilon_ret because a newly admitted candidate can lower aux_best and eliminate previous auxiliary survivors. This is real in wave2a and is accepted as intentional nested lexicographic indifference. epsilon_ret must therefore be described as a **primary indifference radius**, not a generic permissiveness knob.

### Attack 3 — Cliff threshold

**ACTIVE AND MATERIAL; threshold remains Owner semantic.**

Exact durable CELL replay over wave2a yields 214 structurally eligible 3×3 neighborhoods across 18 of 34 Strategies.

| Cliff | Survivors | Rejected | Rejected % | Strategies losing all | Primary-stability anchor churn |
|---:|---:|---:|---:|---:|---:|
| 25% | 151 | 63 | 29.44% | 4 | 3 |
| 30% | 171 | 43 | 20.09% | 3 | 2 |
| 35% | 188 | 26 | 12.15% | 0 | 2 |
| 40% | 205 | 9 | 4.21% | 0 | 0 |

At 35%, six Strategies lose candidates: Strategy_7.51.646 4/10, Strategy_7.46.731 5/28, Strategy_6.39.493 1/14, Strategy_1.8.669 8/28, Strategy_6.24.638 7/11, Strategy_6.40.536 1/17. The primary stability anchor changes in Strategy_7.51.646 (6/32→8/32) and Strategy_6.24.638 (6/30→6/28).

Boundary sensitivity is real: Strategy_2.25.400 6/22 has cliff 0.349660, only 0.000340 below 35%; Strategy_6.40.536 9/26 is 0.348835; Strategy_1.8.669 6/34 is just above at 0.359919.

35% is therefore not inactive. This evidence describes sensitivity only; it does not select the Owner threshold.

### Attack 4 — Center representativeness

**SURVIVES. Retain R_x=max(D_x,C_x).**

Absolute center deviation should be symmetric. A center much better than the plateau is a spike; a center much worse is a trough. Both mean the applied center is not representative. Direction-sensitive downside remains separated in the Ret/DD cliff, while performance level remains in quality.

max(D,C) prevents compensation: MAD cannot hide an unrepresentative center and a representative center cannot hide broad dispersion.

Near-zero non-zero scale can produce very large finite R; that is legitimate relative-instability semantics. Exact zero scale with variation produces +Inf and, after the required correction, rejects the candidate.

Spatial permutations, axis direction, corner/direct-neighbor geometry and isolated non-center upside spikes remain invisible. No real evidence requires surface fitting or weights.

### Attack 5 — Auxiliary minimax

**SURVIVES.**

Retain R_aux=max(R_sharpe,R_profit). The inputs are dimensionless normalized instability measures; max gives authority to the worse auxiliary dimension and prevents compensation. A single epsilon_aux is defensible because it measures one common concept: additional normalized worst-dimension auxiliary instability considered immaterial.

No weighted average and no separate per-metric epsilon are justified.

### Attack 6 — Quality lexicographic

**SURVIVES.**

Retain median Ret/DD DESC → median Sharpe DESC → median Net Profit DESC after both stability gates.

A synthetic tiny-Ret/DD-vs-huge-other-quality counterexample is always possible, but that alone does not justify a new parameter. A durable wave2a probe searched post-35%-cliff pairs for <1% Ret/DD advantage combined with >5% Sharpe or >10% Profit disadvantage, while both R_retdd and R_aux gaps were <=0.03. Observed cases: **0**.

The 0.03 proximity is only an adversarial probe, not a frozen epsilon. Current evidence does not justify epsilon_quality_ret.

### Attack 7 — Algorithm identity / config compatibility

**Current scoring_algorithm is too narrow as the public V2 identity.**

V2 changes eligibility, derived validity, cliff gating, stability representation, staged admissibility, quality ordering, tie-break and audit fields; it is not merely another scalar scoring function.

Minimal contract: add one higher-level selector at the evaluate_wfm boundary:

~~~text
evaluation_policy
evaluation_policy_version
~~~

Absent evaluation_policy must route through the exact legacy V1 binding/config/digest path. Explicit V2 selects a new V2 typed config. Do not invent a registry framework.

Prefer evaluation_policy over selection_policy to avoid collision with the downstream durable DecisionPolicy in select_robust_run.

Do not silently add V2 fields to the V1 marshaled DTO if that changes historical V1 config identity merely because V2 exists.

### Attack 8 — Versioning and auditability

**Requirements are clear.**

V2 durable identity must contain, directly or transitively through a frozen policy version:

- policy id/version;
- neighborhood contract/version;
- required metric contract;
- normalization + center semantics;
- derived-finiteness semantics;
- cliff threshold;
- epsilon_ret and epsilon_aux;
- auxiliary minimax;
- quality ordering;
- technical tie-break;
- numeric comparison semantics where behavior can change.

Different behavior must yield different config identity. V1 defaults cannot silently mutate.

### Attack 9 — Empty / degenerate cases

**MATERIAL DEFECT FOUND.**

Minimal counterexample:

~~~text
0 0 0
0 1 1
0 1 1
~~~

Center=1, median=0, scale=0, MAD=0, center deviation=1. Therefore D=0, C=+Inf, R_retdd=+Inf. tail=0 and cliff=0, so the cliff passes.

If all candidates have the same non-finite R_retdd class, ret_best=+Inf and the band passes them. An analogous all-+Inf R_aux set also passes.

Correction: +Inf is a rejection sentinel, not a comparable admissible stability value. Reject any candidate with non-finite derived stability before minima are calculated.

### Attack 10 — Exact durable replay gate

**REQUIRED BEFORE SPEC FREEZE; conceptual review itself is not blocked.**

Optimizer replay is design evidence only. The known Strategy_1.8.669 discrepancy remains: Optimizer Sharpe around 1.33 versus WFM durable rank metric 1.35 in the relevant context.

The wave2a corpus already provides useful durable evidence: cells.tsv has 1,836 CELL rows with CELL EvaluationRefs and observed metrics; aggregates.tsv carries aggregate verdict/reason data; picks.tsv carries emitted ranks and CELL/MetricSet refs for picks.

That is enough for this design review, but not yet a complete V1 certification bundle because a canonical typed evaluator config document/digest plus complete CELL↔MetricSet lineage for all cells is not present in one authority set.

Do not rerun SQX if immutable durable evidence already exists.

## 4. Stability-band monotonicity analysis

For fixed post-cliff candidates:

~~~text
S_ret(e) = {c | R_retdd(c) <= ret_best + e}
~~~

S_ret is monotone in epsilon_ret.

For fixed S_ret:

~~~text
aux_best = min R_aux over S_ret
S_aux(e) = {c in S_ret | R_aux(c) <= aux_best + e}
~~~

S_aux is monotone in epsilon_aux.

The composed final set is not monotone in epsilon_ret because aux_best is recomputed when S_ret expands. This is not hidden and is accepted as the semantics of a nested indifference policy.

## 5. epsilon_ret → aux_best interaction analysis

Real durable examples:

- **Strategy_1.8.669**, epsilon_aux <=0.005: epsilon_ret ~0.009217→~0.009739 admits 9/28, aux_best 0.019691→0.010917, removing 8/28.
- **Strategy_6.40.536**, illustrative epsilon_aux=0.005: epsilon_ret ~0.019363→~0.028478 admits 7/22, aux_best 0.030603→0.022267, removing 6/32 and 9/24.
- **Strategy_6.39.493**, epsilon_aux=0.0025–0.005: epsilon_ret ~0.011617→~0.016598 admits 6/26, aux_best 0.013299→0.007789, removing 6/22, 6/24, 7/22 and 7/24.

Therefore end-to-end monotonicity in epsilon_ret is demonstrably false. The design survives because this reclassification is the intended meaning of declaring the newly admitted candidate materially equivalent on primary stability.

Audit must expose ret_best, primary membership, aux_best, auxiliary membership and exact rejection reason.

## 6. Cliff candidate-level sensitivity

25% and 30% materially reduce Strategy availability. 35% preserves all 18 pre-cliff eligible Strategies while still removing 12.15% of neighborhoods and changing two primary stability anchors. 40% is materially looser and causes no anchor churn in this corpus.

Final V2 winner/runner-up cliff distances cannot be frozen before epsilon values exist. The exact replay must report, for the chosen threshold, the final winner/runner-up margins plus nearest retained and nearest rejected candidates.

## 7. Center topology verdict

~~~text
CENTER_TOPOLOGY_VERDICT: RETAIN_MAX_MAD_CENTER_DEVIATION
~~~

Retain R_x=max(D_x,C_x). Do not add spatial weights. Only amend the non-finite branch: +Inf rejects the candidate.

## 8. Auxiliary minimax verdict

~~~text
AUX_MINIMAX_VERDICT: RETAIN
~~~

Retain max(R_sharpe,R_profit) and one epsilon_aux. No weights or averaging.

## 9. Quality ordering verdict

~~~text
QUALITY_ORDER_VERDICT: RETAIN_LEXICOGRAPHIC
~~~

Retain median Ret/DD → median Sharpe → median Net Profit. No evidence supports a quality band in V2.

## 10. Config / algorithm identity verdict

~~~text
CONFIG_IDENTITY_VERDICT:
ADD_EXPLICIT_EVALUATION_POLICY_SELECTOR
PRESERVE_V1_TYPED_CONFIG_AND_DIGEST_PATH
~~~

Legacy absence routes to current V1. Explicit V2 routes to a new V2 typed config. No registry framework and no reinterpretation of wfm_3x3_v1 or dispersion_cov.

## 11. Backward compatibility contract

~~~text
same legacy input config
→ same V1 evaluator path
→ same eligibility
→ same scoring
→ same ranking ordering
→ same tie-break
→ same rank semantics
~~~

V2 is explicit opt-in. select_robust_run remains rank-1 consumer only.

## 12. Durable identity / versioning requirements

V2 identity must distinguish every behaviorally different policy. Owner parameters are explicit. Replay output must expose the resolved typed config and digest. If a semantic is fully frozen by policy version, it may be represented transitively through that version instead of becoming another free knob.

## 13. Degenerate-case table

| Case | Required behavior | Class |
|---|---|---|
| no valid 3×3 | no rank-1 | analytical FAIL |
| all fail cliff | no rank-1 | analytical FAIL |
| all fail derived-finite gate | no rank-1 | analytical FAIL |
| one candidate after any gate | continue deterministically | valid |
| all R_retdd=+Inf | reject before ret_best | analytical FAIL |
| finite + +Inf R_retdd | reject non-finite, finite compete | analytical filter |
| all R_aux=+Inf | reject before aux_best | analytical FAIL |
| scale=0, no variation | D=C=0 | valid |
| scale=0, variation | +Inf sentinel → reject | analytical filter |
| all-zero neighborhood | stability 0; no extra quality floor | valid if structurally eligible |
| negative/mixed signs | allowed if finite | valid |
| duplicate CELL coordinate/conflicting identity | do not choose arbitrarily | technical failure |
| missing/NaN/Inf raw metric | ineligible | analytical filter |
| malformed ref/lineage | contract failure | technical failure |
| incomplete 3×3 | not a candidate | analytical filter |
| exact ties | deterministic tie-break | valid |
| input shuffle | identical result | determinism requirement |

## 14. Mandatory Strategy walkthroughs

**Strategy_1.8.669:** 8/28 is post-35 primary stability anchor (Rret 0.013369, Raux 0.019691). 9/28 (0.023107, 0.010917) can enter around epsilon_ret 0.009739 and eliminate it for small epsilon_aux. Intended. Cliff 35 rejects 8/28 candidate neighborhoods overall but leaves this anchor.

**Strategy_6.40.536:** 6/32 is primary anchor (Rret 0.011095, Raux 0.034188). 7/22 (0.039573, 0.022267) can enter later and materially lower aux_best. Real cross-stage rebase confirmed. Cliff 35 rejects 1/17 candidates.

**Strategy_8.10.634:** 9/30 (Rret 0.017634, Raux 0.033137) versus 6/34 (0.024291, 0.025000) is the cleanest small-primary-difference / better-aux case. 35% eliminates none of its 23 eligible neighborhoods.

**Strategy_2.17.581:** 6/34 Rret 0.070349; next candidates are 0.153481, 0.175150 and 0.258071. The large primary gaps demonstrate that quality cannot casually buy primary stability degradation.

**Strategy_6.39.493:** 7/22 is anchor at Rret 0.012041/Raux 0.013299. Admitting 6/26 at Rret 0.028640/Raux 0.007789 can remove four prior auxiliary survivors at small epsilon_aux. Strongest real proof that final-set monotonicity in epsilon_ret is false.

**New counterexample:** the scale-zero / center-deviation +Inf case is a genuine fail-open defect and is the only policy change required by this review.

## 15. Remaining Owner decisions

After the non-finite correction:

1. cliff_threshold — maximum tolerated local Ret/DD downside cliff.
2. epsilon_ret — maximum extra normalized primary instability considered immaterial.
3. epsilon_aux — maximum extra normalized worst-dimension auxiliary instability considered immaterial.
4. Ratify the recommended quality order.

There is no Owner choice on the +Inf fix: fail closed is required.

## 16. Exact durable replay prerequisite

Minimum authority per Strategy:

- all 54 CELLs with StrategyRef, runs/OOS, CELL EvaluationRef, observed pass state, exact MetricSetRef, Ret/DD, Sharpe, Net Profit and CELL↔MetricSet↔StageExecution lineage;
- exact typed V1 evaluator config + digest;
- grid/neighborhood config + digest;
- scoring algorithm/version, ranking metric, primary metric, filters and rules config;
- aggregate EvaluationRef, verdict/reason/warnings and emitted V1 ranks.

Replay gate:

1. validate refs, lineage, unique coordinates, finite observations and config digest;
2. reproduce V1 exactly from durable evidence, including rank-1 identity; shuffle input and prove same output;
3. run corrected V2 offline over the same CELL/MetricSet authority and record every policy stage;
4. probe semantic breakpoints around Owner values, never optimize winner quality;
5. compare exact V1 vs V2 churn and reasons.

~~~text
V1 exact replay mismatch
→ BLOCK SPEC freeze

V1 exact replay PASS
AND corrected V2 deterministic replay PASS
AND Owner values frozen
→ SPEC may start
~~~

## 17. Complexity / KISS / YAGNI verdict

~~~text
KISS/YAGNI: PASS WITH ONE REQUIRED FAIL-CLOSED GUARD
~~~

Keep the 3×3 contract, three metrics, MAD + center deviation, max composition, one Ret/DD cliff, two semantic indifference radii, auxiliary minimax, lexicographic quality and deterministic tie-break.

Do not add Pareto, scalar weights, spatial weights, surface fitting, quality bands, per-metric auxiliary epsilons or a registry framework.

Add only the derived-finiteness rejection gate.

## 18. Final recommended policy

~~~text
explicit V2 evaluation_policy
→ structural 3×3 eligibility
→ compute M/scale/MAD/D/C/R and Ret/DD cliff
→ reject any candidate with non-finite derived R/cliff
→ Ret/DD cliff hard gate
→ retain R_retdd <= ret_best + epsilon_ret
→ R_aux=max(R_sharpe,R_profit)
→ retain R_aux <= aux_best + epsilon_aux
→ median Ret/DD DESC
→ median Sharpe DESC
→ median Net Profit DESC
→ R_retdd ASC
→ R_aux ASC
→ runs ASC
→ OOS ASC
→ evaluate_wfm emits rank/audit
→ select_robust_run consumes unique rank==1
~~~

Semantic clarification: epsilon_ret is an indifference radius, not a guarantee of final survivor-set monotonicity. Once inside the Ret/DD equivalence class, the exact Ret/DD minimum has no protected incumbent status.

## 19. Exact next gate

~~~text
Return to Primary Technical Manager.

Integrate one bounded design correction:
- reject non-finite derived stability before ret_best/aux_best.

Carry forward:
- nested Ret/DD → auxiliary indifference;
- intentional cross-stage final-set non-monotonicity in epsilon_ret;
- additive V2 identity and exact V1 preservation.

Do not freeze Owner numbers yet.
Do not start SPEC.
Do not implement product code.

After the corrected candidate is persisted:
- perform focused final verification of this amendment;
- then Owner freeze requires the exact durable replay bundle.
~~~

# Handoff

~~~text
STATUS:
DESIGN_ITERATION_REQUIRED

CORE VERDICT:
Iteration 2 survives the central stability/quality attacks.
One material fail-closed defect remains: non-finite derived stability can pass when every candidate is non-finite.

POLICY CHANGES REQUIRED:
- Derived-finiteness gate before ret_best/aux_best.
- Non-finite R_retdd/R_sharpe/R_profit/R_aux/cliff rejects the candidate.
- No other weights, bands or geometry.

EPSILON_RET VERDICT:
Valid primary-indifference radius; not a weight.
Ret-stage membership monotone; final survivor membership need not be.

EPSILON_AUX VERDICT:
Valid worst-dimension auxiliary-indifference radius.
At fixed Ret/DD set, membership is monotone.

CROSS-STAGE MONOTONICITY:
End-to-end monotonicity in epsilon_ret is FALSE.
Demonstrated in durable wave2a and accepted as intended semantics.

CLIFF VERDICT:
35% rejects 26/214 candidates (12.15%), affects 6 Strategies,
eliminates none, changes primary stability anchor in 2.
25%/30% eliminate all candidates for 4/3 Strategies.
40% rejects 9 and changes no primary anchor.
Threshold remains Owner semantic.

CENTER_TOPOLOGY VERDICT:
Retain R_x=max(D_x,C_x). No spatial weights.

AUX_MINIMAX VERDICT:
Retain max(R_sharpe,R_profit). One epsilon_aux.

QUALITY_ORDER VERDICT:
Retain median Ret/DD → Sharpe → Net Profit. No quality band.

CONFIG_IDENTITY VERDICT:
Add explicit evaluation_policy + version at evaluate_wfm.
Preserve legacy V1 typed config/digest path.
No registry framework.

V1 BACKWARD_COMPATIBILITY:
Existing legacy config reproduces existing V1 behavior.
V2 explicit opt-in.
select_robust_run remains rank==1 consumer.

DURABLE_IDENTITY_REQUIREMENTS:
policy/version; neighborhood contract; cliff; epsilons;
metric/normalization/center/non-finite semantics;
aux minimax; quality order; tie-break/numeric semantics.

MANDATORY STRATEGY FINDINGS:
- 1.8.669: 8/28 can be eliminated by 9/28 after epsilon_ret admits it; intended.
- 6.40.536: strong real aux_best rebase; intended.
- 8.10.634: 6/34 is clean Ret/DD-indifferent/better-aux example.
- 2.17.581: primary gaps protect stability from quality.
- 6.39.493: admitting 6/26 can remove four prior aux survivors.

OWNER DECISIONS REMAINING:
cliff_threshold; epsilon_ret; epsilon_aux; ratify quality order.
Non-finite fix is mandatory, not tunable.

EVIDENCE GATES:
Exact durable V1 replay before SPEC freeze.
Same immutable CELL/MetricSet authority for V2.
Full typed config/digest and complete CELL↔MetricSet lineage.
No SQX rerun merely to reconstruct durable evidence.

KISS/YAGNI:
PASS after one fail-closed guard.

ARTIFACT:
main/10-projects/Echo Forge — Robust Run Selection V2/ROBUST-V2-FINAL-ADVERSARIAL-REVIEW.md
<commit + blob SHA after persistence>

NEXT EXACT:
Return to Primary Technical Manager.
Apply bounded derived-finiteness correction.
Do not start SPEC or implementation.
~~~
