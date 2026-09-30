# ROBUST-V2-FINITENESS-VERIFICATION

> **AUTHORITY NOTE — SUPERSEDED FOR IMPLEMENTATION (2026-09-30):** Keep the finiteness proof and fail-closed semantics. References to an explicit `evaluation_policy` selector and durable replay/Owner freeze as a prerequisite to implementation are **superseded** by [[ROBUST-V2-DESIGN-FREEZE]]. V2 uses the existing algorithm/config extension point; historical replay is deferred verification, not a Shot 1 gate.


Status: DESIGN_READY_FOR_DURABLE_REPLAY_AND_OWNER_FREEZE

Date: 2026-09-29

Scope: focused final verification of the derived-finiteness and V2 semantic-configuration amendments for Echo Forge Robust Run Selection V2. No SPEC, no product code, no implementation shots, no reopening of frozen policy choices.

## 1. Scope

This review verifies only the bounded Manager amendment accepted after ROBUST-V2-FINAL-ADVERSARIAL-REVIEW: non-finite derived policy values make the whole candidate analytical-ineligible before stability minima, and V2 semantic parameters must be finite and non-negative. Pareto, weights, MAD, center deviation, topology, cliff semantics, R_aux minimax, quality order, nested-indifference semantics, policy naming and V1/V2 coexistence remain frozen.

Authority used: [[Echo Forge — Robust Run Selection V2]], [[ROBUST-V2-DESIGN-ITERATION-2]], [[ROBUST-V2-FINAL-ADVERSARIAL-REVIEW]], plus the current Symphony V1 typed evaluator/config and durable robust-selection contracts for the compatibility check.

## 2. Amendment under verification

Candidate-wide analytical eligibility is now:

~~~text
derive:
  R_retdd
  R_sharpe
  R_profit
  R_aux
  cliff

if any derived value is non-finite:
  candidate = analytical-ineligible
~~~

This gate is applied after structural/raw required-metric eligibility and after the explicit zero-scale branches have produced their contractual 0 or +Inf result, but before any cliff comparison, ret_best calculation or aux_best calculation.

The effective V2 sequence is therefore:

~~~text
validate explicit V2 configuration
→ structural/raw evidence eligibility
→ derive D/C/R, R_aux and cliff
→ remove any candidate with non-finite R_retdd/R_sharpe/R_profit/R_aux/cliff
→ Ret/DD cliff hard gate
→ if empty: analytical FAIL
→ ret_best and epsilon_ret membership
→ aux_best and epsilon_aux membership
→ quality ordering
→ technical tie-break
~~~

V2 configuration validation is policy-scoped: cliff_threshold, epsilon_ret and epsilon_aux must each be finite and >= 0. Invalid values are configuration/contract failures before analytical Strategy evaluation; they are never silently defaulted, coerced or clamped.

## 3. Derived-finiteness proof

Let E be the candidates that passed structural and raw required-evidence eligibility. Let F be the subset of E for which R_retdd, R_sharpe, R_profit, R_aux and cliff are all finite. Let G be the subset of F that passes the finite Ret/DD cliff threshold.

If F is empty, no stability minimum is evaluated and the Strategy terminates analytical FAIL. If G is empty, no ret_best is evaluated and the Strategy terminates analytical FAIL. If G is non-empty, ret_best = min R_retdd over G is necessarily finite because every member of G has finite R_retdd. The Ret/DD survivor set is therefore defined only against a finite anchor.

The auxiliary stage receives only members of G and, by candidate-wide finiteness, every such candidate has finite R_aux. If the Ret/DD survivor set is non-empty, aux_best = min R_aux over that set is necessarily finite. Therefore neither +Inf nor NaN can become an admissible ret_best or aux_best anchor.

This directly removes the previous fail-open identity:

~~~text
+Inf <= +Inf + epsilon
~~~

because the left-hand candidate and the would-be +Inf anchor are both removed from the admissible domain before the comparison exists.

The amendment is stronger than a stage-local auxiliary cleanup: a candidate with finite R_retdd but non-finite R_aux is not allowed to define ret_best and then disappear later. It is analytically ineligible as a candidate before any stability minimum. That is coherent with the Manager contract and prevents an invalid candidate from narrowing or rebasing the primary band.

## 4. Primary-stage cases

### A — all derived primary stability non-finite

Mandatory shape, repeated for every candidate if needed:

~~~text
0 0 0
0 1 1
0 1 1
~~~

For this 3×3 metric neighborhood: median=0, scale=0, MAD=0, center=1, center deviation=1, therefore D=0, C=+Inf and R=+Inf. For Ret/DD specifically, tail=0 and cliff=0, so the old policy could reach the stability band with R_retdd=+Inf.

Under the amendment the candidate is removed by the derived-finiteness gate before cliff comparison and before ret_best. If every candidate has this shape, the candidate set becomes empty and the Strategy ends analytical FAIL. ret_best=+Inf is never formed.

Result: PASS.

### B — mixed finite and non-finite primary stability

Candidate A can use a constant finite neighborhood such as nine 1 values: median=1, scale=1, D=0, C=0, R_retdd=0, cliff=0. Candidate B can use the mandatory scale-zero/center-deviation shape above and obtains R_retdd=+Inf.

B is removed before minima. A participates normally and alone determines any later ret_best, epsilon_ret membership, ranking and audit winner. B cannot affect the anchor or the final order.

Result: PASS.

## 5. Auxiliary-stage cases

Construct candidates with finite Ret/DD neighborhoods but a Sharpe or Net Profit neighborhood equal to the mandatory scale-zero/center-deviation shape. Their primary R_retdd may be finite, while R_sharpe=+Inf or R_profit=+Inf and therefore R_aux=+Inf.

Because analytical eligibility is candidate-wide and checked before all minima, such a candidate is removed before ret_best as well as before aux_best. The phrase “passes Ret/DD stage but has non-finite auxiliary stability” is therefore only counterfactual: its primary values are acceptable in isolation, but the complete candidate is not analytically eligible.

If every otherwise-primary-valid candidate has non-finite auxiliary derived values, all are removed and the Strategy ends analytical FAIL. No aux_best=+Inf can exist, and no invalid auxiliary candidate can influence ret_best first.

Result: PASS.

## 6. Cliff cases

A cliff can be non-finite even when R_retdd itself is finite. Example Ret/DD neighborhood: eight 0 values and one -1, with center=0. Then median=0, scale=0, MAD=0 and center deviation=0, so R_retdd=0; however tail=-1 and median != tail, therefore cliff=+Inf.

The amendment explicitly removes this candidate at the derived-finiteness gate. It does not rely on +Inf <= finite cliff_threshold evaluating false. This preserves deterministic audit semantics and prevents language/runtime comparison behavior from becoming policy authority.

Result: PASS.

## 7. Zero / near-zero cases

### Near-zero but finite

A legal 3×3 example can have median(abs(x))=1e-300 and center deviation approximately 1e-250, producing C and therefore R around 1e50. This value is extremely large but finite.

The amendment does not reject it. It remains an analytically valid derived value and is handled by the normal cliff/stability policy. No epsilon-for-zero, minimum-scale floor or arbitrary near-zero cutoff is introduced.

If IEEE arithmetic actually overflows a finite-input ratio to +Inf, the post-derivation finiteness gate intentionally rejects that result as non-finite. That is not a near-zero policy threshold; it is the same fail-closed derived-value contract.

### Zero scale with zero variation

An all-zero neighborhood has median=0, scale=0, MAD=0, center deviation=0, therefore D=0, C=0, R=0. Ret/DD also has tail=median=0, therefore cliff=0.

All derived values are finite and the candidate remains valid. A naive 0/0 implementation would violate the already-frozen explicit zero-scale branches; the amendment does not change those branches.

Result: PASS.

## 8. Configuration validity

For explicit V2 evaluation, each of cliff_threshold, epsilon_ret and epsilon_aux must satisfy both predicates:

~~~text
is_finite(value)
AND
value >= 0
~~~

Therefore NaN, +Inf, -Inf and ordinary negative values such as -0.01 are invalid configuration. Invalid configuration terminates through configuration/contract validation before Strategy analytics. There is no Strategy analytical FAIL, silent defaulting, coercion or clamp-to-zero.

This validation must remain scoped to explicit V2 selection. Applying V2-required fields or validators to an absent legacy V1 selector would violate the frozen backward-compatibility contract.

Result: PASS.

## 9. Analytical vs technical/config failure semantics

The minimum audit distinction needed for the future SPEC is conceptual rather than a large enum taxonomy:

| Situation | Level | Required semantic outcome |
|---|---|---|
| Raw required metric missing, NaN, Inf or otherwise invalid | candidate analytical eligibility | candidate excluded with raw-evidence reason |
| Finite raw input yields non-finite R_retdd/R_sharpe/R_profit/R_aux/cliff | candidate analytical eligibility | candidate excluded with derived-non-finite reason |
| No candidate remains after analytical filters | Strategy analytical result | analytical FAIL; no rank1 |
| Explicit V2 config contains invalid semantic parameter | evaluator/config contract | technical/config-validation failure; no manufactured analytical result |

Exact enum names do not need to be frozen in this verification. The four reason classes must remain distinguishable in durable audit evidence.

## 10. Finite-corpus non-regression

Assume an Iteration 2 corpus where every structurally eligible candidate has finite R_retdd, R_sharpe, R_profit, R_aux and cliff, and the explicit V2 parameters are finite and non-negative.

For every candidate the new finiteness predicate evaluates true, so the derived gate is the identity function over the candidate set. Configuration validation is also a no-op. Therefore the input set and values presented to the frozen downstream policy are identical.

Consequently the amendment preserves: same candidate set, same R values, same cliff values, same ret_best, same epsilon_ret membership, same aux_best, same epsilon_aux membership, same median quality tuple, same technical tie-break and same final rank.

The amendment is therefore a fail-closed domain guard, not a ranking-policy change.

Result: PASS.

## 11. V1 compatibility

Current Symphony V1 binds wfm_3x3_v1 / dispersion_cov through its existing typed EvaluatorConfig and hashes that exact DTO for evaluator identity. Durable select_robust_run independently consumes the unique rank==1 pick and does not recalculate the WFM ranking.

The V2 amendment does not require changing dispersion_cov, V1 scoring, the existing V1 typed DTO, V1 defaults, V1 digest semantics, legacy rank ordering or downstream rank==1 selection. The compatibility invariant is:

~~~text
legacy config with no explicit V2 evaluation_policy
→ exact existing V1 binder/DTO/digest path
→ no V2 parameter validation
→ exact existing V1 behavior
~~~

Explicit V2 selection enters the new V2 policy/config contract and only there applies the finiteness/config amendments. Any implementation that validates V2 fields globally before policy dispatch would violate this design, but that is an implementation error rather than a flaw in the amendment itself.

Result: PASS.

## 12. Remaining risks

No material design defect directly connected to the amendment remains.

Future SPEC/implementation must preserve four bounded risks already implied by this verification: perform raw validation before derivation so raw-invalid and derived-non-finite reasons do not collapse; preserve the explicit scale==0 branches so valid zero/zero cases do not become NaN; execute the derived-finiteness gate before cliff comparison and before any stability minimum; and scope V2 config validation behind explicit V2 dispatch so the legacy V1 DTO/digest path remains byte/semantic compatible.

Exact durable replay, complete CELL↔MetricSet lineage, Owner values for cliff_threshold/epsilon_ret/epsilon_aux and final Owner ratification of the frozen quality order remain next gates. Their absence is not a defect in this focused amendment verification.

## 13. Final verdict

DESIGN_READY_FOR_DURABLE_REPLAY_AND_OWNER_FREEZE

The derived-finiteness amendment closes the sole material fail-open found by the final adversarial. It makes the stability-minimum domain finite by construction, handles non-finite cliff explicitly, preserves valid zero-scale and near-zero-finite behavior, distinguishes analytical exclusion from invalid configuration, is transparent on finite corpora, and does not require any V1 semantic change.

POLICY_CHANGES_REQUIRED: none beyond the already accepted Manager amendment.

## 14. Next exact gate

Return to Primary Technical Manager.

Run the exact durable replay gate over the same immutable CELL/MetricSet authority: first reproduce V1 exactly including rank1 identity and deterministic shuffle behavior, then replay the corrected V2 with the full audit stages and no winner-driven tuning. Freeze Owner semantic values only against that evidence. Do not start SPEC or implementation until durable replay and Owner freeze are complete.

# Handoff

~~~text
STATUS:
DESIGN_READY_FOR_DURABLE_REPLAY_AND_OWNER_FREEZE

DERIVED_FINITE_GATE:
PASS

ALL_NONFINITE_PRIMARY:
PASS — all removed before ret_best; analytical FAIL; ret_best=+Inf cannot exist.

MIXED_FINITE_NONFINITE:
PASS — non-finite candidate removed; finite candidate set and anchors unchanged.

ALL_NONFINITE_AUX:
PASS — candidate-wide gate removes them before any minimum; analytical FAIL if none remain; aux_best=+Inf cannot exist.

CLIFF_NONFINITE:
PASS — explicit derived-finiteness rejection; no reliance on threshold comparison side effects.

ZERO_SCALE_ZERO_VARIATION:
PASS — D=0, C=0, R=0, cliff=0 remains valid.

NEAR_ZERO_FINITE:
PASS — extremely large but finite R remains valid; no arbitrary scale epsilon introduced.

CONFIG_VALIDATION:
PASS — cliff_threshold/epsilon_ret/epsilon_aux must be finite and >=0; invalid values fail configuration validation without default/coercion/clamp.

ANALYTICAL_VS_CONFIG_FAILURE:
PASS — raw-invalid, derived-non-finite, empty analytical candidate set and invalid V2 config remain distinct semantic classes.

FINITE_CORPUS_REGRESSION:
PASS — filter is identity when all derived values are finite; downstream policy and ranking are unchanged.

V1_COMPATIBILITY:
PASS — amendment is V2-only behind explicit policy selection; existing V1 EvaluatorConfig/digest, dispersion_cov, ranking and rank1 consumer semantics remain unchanged.

POLICY_CHANGES_REQUIRED:
NONE beyond the already accepted derived-finiteness and V2 config-validity amendment.

ARTIFACT:
main/10-projects/Echo Forge — Robust Run Selection V2/ROBUST-V2-FINITENESS-VERIFICATION.md
commit: 0f76076630c4d5546dbe50aa7098026ff302f728
blob: 28cbbf7952bcecea7044deddef4fe70acb89b72b

NEXT EXACT:
Return to Primary Technical Manager.
Do not start SPEC or implementation.
~~~
