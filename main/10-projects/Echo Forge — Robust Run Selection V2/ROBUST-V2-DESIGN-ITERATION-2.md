# ROBUST-V2-DESIGN-ITERATION-2

Status: `DESIGN_V2_CANDIDATE_READY`

Date: 2026-09-29

Scope: segunda iteración de diseño pre-implementación para Echo Forge Robust Run Selection V2. No SPEC final, no product code, no implementation shots.

## 1. Manager concern restatement

El problema abierto no es si stability debe importar: eso ya está aceptado. El problema es cómo darle autoridad real sin caer en dos extremos incorrectos: una scalarización arbitraria que esconda trade-offs, o una Pareto frontier tan amplia que cualquier mejora mínima en otra dimensión permita que quality vuelva a decidir casi todo.

El caso obligatorio `Strategy_1.8.669` demuestra el defecto del Pareto plain: 9/26 y 8/28 son no dominados, pero 9/26 compra aproximadamente 0.71% de median Ret/DD con aproximadamente 2.3× `D_retdd`. Pareto sólo dice "ninguno domina"; no dice si ese intercambio es materialmente aceptable.

La abstracción que faltaba es explícita: **stability equivalence / indifference**. Quality sólo puede elegir entre neighborhoods cuya diferencia de stability fue declarada previamente inmaterial por una regla versionada y auditable.

## 2. Pareto audit

### Verdict

`PLAIN_PARETO_AS_AUTHORITY = REJECTED`.

Pareto puede conservarse como diagnóstico, pero no como autoridad de ranking V2.

### Why

Con sólo tres dispersion dimensions, non-dominance sigue siendo demasiado permisiva: una mejora pequeña en Sharpe o Net Profit puede mantener vivo un candidate con una degradación mucho mayor en Ret/DD stability. La frontier no codifica magnitud, prioridad del Owner ni materialidad.

La evidencia del Manager ya muestra layer-1 amplia: mediana aproximada 32.1% de los candidates y máximo de 7 candidates por Strategy a cliff 35%. El replay de Iteration 2 confirma que el problema no es teórico: múltiples candidates materialmente distintos permanecen comparables por Pareto.

### Desired trade-off semantics

La semántica deseada no es "A domina B" sino: **A y B son suficientemente equivalentes en stability para permitir que quality arbitre**. Esa relación debe estar anclada a un baseline común y no definirse pairwise, porque tolerancias pairwise pueden producir comparadores no transitivos.

## 3. MAD / topology audit

### Normalized MAD verdict

`NORMALIZED_MAD = RETAINED_AS_BROAD_DISPERSION_COMPONENT, NOT SUFFICIENT_ALONE`.

Candidate base remains:

```text
median_x = median(x_1..x_9)
scale_x  = median(abs(x_1..x_9))
MAD_x    = median(abs(x_i - median_x))

D_x =
  0      if scale_x == 0 and MAD_x == 0
  +Inf   if scale_x == 0 and MAD_x > 0
  MAD_x / scale_x otherwise
```

MAD is appropriate for broad dispersion because it is robust, scale-free and simple, but nine observations are enough for one or two outliers to disappear from the median absolute deviation.

### Smallest topology-aware addition

The selected physical configuration is the center CELL. Therefore the minimum topology information that materially changes selection is **whether the center is representative of the neighborhood**:

```text
C_x =
  0      if scale_x == 0 and abs(center_x - median_x) == 0
  +Inf   if scale_x == 0 and abs(center_x - median_x) > 0
  abs(center_x - median_x) / scale_x otherwise

R_x = max(D_x, C_x)
```

Apply the same construction to Ret/DD, Sharpe and Net Profit.

`R_x` is not a weighted score. It is the worst of two failure modes within one metric: broad neighborhood dispersion and center unrepresentativeness.

### Why not full edge/surface geometry

Iteration 2 tested orthogonal-edge and axis-slope ideas. They detect additional spatial shapes, but they add semantics that are not yet justified by evidence: whether runs-axis roughness should matter more than OOS-axis roughness, whether corners deserve distance weighting, and how to combine edge statistics with MAD.

For V2 the KISS boundary is: **bag-of-values dispersion + center representativeness**. This distinguishes the topology that directly matters to applying the center without turning the 3×3 into a surface-fitting problem.

### Failure-mode audit

- One outlier at center: MAD can be zero, but `C_x` exposes it.
- One/two non-center downside outliers in Ret/DD: cliff exposes the downside tail.
- One/two non-center upside outliers: may be ignored if MAD remains low; this is accepted because they do not make the selected center a peak and do not create downside fragility.
- Broad slope / monotonic surface: MAD rises and remains visible.
- Symmetric plateau: MAD and center deviation both remain low.
- Asymmetric plateau: broad asymmetry raises MAD unless concentrated in very few non-center cells.
- Mixed signs: `median(abs(x))` prevents mean cancellation.
- Duplicated values: intentionally valid; if five or more values repeat, MAD can be zero, while center deviation and cliff still cover the selected-center/downside failure modes.

## 4. Cliff / topology audit

### Cliff definition remains candidate

```text
R = RetDD[3×3]
L = median(R)
scale = median(abs(R))
tail = min(R)

cliff =
  0                if scale == 0 and L == tail
  +Inf             if scale == 0 and L != tail
  max(0, (L - tail) / scale) otherwise
```

### Topology verdict for cliff

`NO_DISTANCE_OR_AXIS_WEIGHTING_IN_V2`.

A bad diagonal corner and a bad direct runs/OOS neighbor remain equal for the hard downside-tail guard. The reason is not that they are physically identical; it is that no evidence currently justifies a different risk multiplier, and adding one would create another magic parameter family.

The topology that directly matters to the selected run is already captured by `C_retdd`: if the center itself is anomalous, stability authority sees it.

If final adversarial review later demonstrates that direct-neighbor downside must be semantically stricter than corner downside, that is a separate V2.x rule, not something to smuggle into this iteration.

## 5. Stability-vs-quality semantics

### Core contract

Stability is authoritative through **nested indifference bands anchored to the best observed stability within the same Strategy**.

After structural eligibility and cliff:

```text
R_retdd  = max(D_retdd, C_retdd)
R_sharpe = max(D_sharpe, C_sharpe)
R_profit = max(D_profit, C_profit)

R_aux = max(R_sharpe, R_profit)
```

Primary Ret/DD stability:

```text
ret_best = min(R_retdd)

RET_STABILITY_EQUIVALENT(c) :=
  R_retdd(c) <= ret_best + epsilon_ret
```

Secondary stability only inside the Ret/DD-equivalent set:

```text
aux_best = min(R_aux among RET_STABILITY_EQUIVALENT)

AUX_STABILITY_EQUIVALENT(c) :=
  R_aux(c) <= aux_best + epsilon_aux
```

Only candidates satisfying both equivalence predicates may reach quality.

### Why additive bands

All `R_x` are already dimensionless normalized dispersion quantities. An additive materiality boundary therefore has a direct interpretation: the maximum extra normalized instability that the policy declares immaterial.

Ratios such as "2× worse" are rejected as the authority because they explode or become misleading near zero.

### Why anchor to minima instead of pairwise tolerance

The minima are computed once per Strategy after cliff. Every candidate is compared to the same reference. This preserves deterministic, transitive set membership and avoids A≈B, B≈C, A≉C tolerance chains.

### Quality cannot buy material stability

A quality advantage has **zero authority** outside the stability-equivalent set. This directly prevents:

```text
tiny quality gain
-> huge stability degradation
```

Inside the set, the stability differences are definitionally below Owner-approved materiality, so quality is allowed to decide.

## 6. Candidate policy A — Nested Stability Indifference Bands

`POLICY_A = RECOMMENDED`.

### Ranking contract

```text
1. Structural + metric eligibility.
2. Ret/DD cliff hard gate.
3. Compute R_retdd, R_sharpe, R_profit.
4. Keep R_retdd <= min(R_retdd) + epsilon_ret.
5. Compute R_aux = max(R_sharpe, R_profit) inside step 4.
6. Keep R_aux <= min(R_aux) + epsilon_aux.
7. Quality of plateau:
   a. median Ret/DD DESC
   b. median Sharpe DESC
   c. median Net Profit DESC
8. Exact technical tie-break:
   a. R_retdd ASC
   b. R_aux ASC
   c. runs ASC
   d. OOS ASC
```

### Stability authority

Ret/DD gets stronger semantics by **ordering**, not by arbitrary weight: no Sharpe/Profit stability improvement can compensate for leaving the Ret/DD stability band.

Within the Ret/DD band, `R_aux=max(R_sharpe,R_profit)` prevents one secondary stability dimension from hiding a bad other dimension.

### Stability indifference parameters

`epsilon_ret` and `epsilon_aux` are semantic policy parameters and remain Owner decisions. They must be versioned in the eventual policy config and must not be fitted against profit or winner preference.

No numeric value is frozen in this design.

## 7. Candidate policy B — Materiality-normalized minimax regret tiers

`POLICY_B = VIABLE_BUT_NOT_RECOMMENDED_FOR_V2`.

Alternative:

```text
ideal_i = min(R_i) for each stability dimension
regret_i = (R_i - ideal_i) / epsilon_i
tier(c) = max_i ceil(regret_i)

lowest tier
-> plateau quality
-> technical tie-break
```

This gives a single deterministic stability tier with bounded trade-offs and avoids weighted sums.

Why not recommend it:

- requires one materiality scale per dimension or another grouping rule;
- hides the Owner's explicit Ret/DD priority inside a generalized minimax construction;
- harder to explain operationally than "Ret/DD equivalent first, then auxiliary equivalent";
- introduces bucket-boundary behavior without solving a problem Policy A leaves open.

Policy B remains a useful adversarial comparator, not the V2 candidate.

## 8. Concrete wave2a comparisons

All numbers below use the available `OPTIMIZER-CANDIDATES.csv` replay and are design evidence, not final WFM durable certification.

### Strategy_1.8.669

Relevant post-cliff candidates:

| Candidate | R_retdd | D_retdd | C_retdd | R_aux | median Ret/DD | median Sharpe | median Net Profit | epsilon_ret required to enter |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 8/28 | 0.0134 | 0.0134 | 0.0000 | 0.0197 | 21.8314 | 1.22 | 13,578.4 | 0 |
| 9/28 | 0.0231 | 0.0231 | 0.0231 | 0.0109 | 21.5528 | 1.21 | 13,483.1 | 0.0097 |
| 6/22 | 0.0283 | 0.0283 | 0.0144 | 0.0165 | 22.6470 | 1.20 | 13,099.5 | 0.0149 |
| 9/26 | 0.0307 | 0.0307 | 0.0000 | 0.0132 | 21.9858 | 1.22 | 13,618.6 | 0.0174 |

The Manager's 9/26-vs-8/28 objection becomes explicit: 9/26 is not allowed to use its ~0.71% median Ret/DD gain unless `epsilon_ret >= 0.0174`. Below that boundary, 8/28 has authority. Above it, secondary stability and then quality may decide.

This is aligned with the V2 objective because the materiality trade-off is no longer implicit in Pareto membership.

### Strategy_6.40.536

| Candidate | R_retdd | R_aux | median Ret/DD | median Sharpe | median Net Profit | epsilon_ret required |
|---|---:|---:|---:|---:|---:|---:|
| 6/32 | 0.0111 | 0.0342 | 20.8536 | 1.17 | 16,908.0 | 0 |
| 9/24 | 0.0233 | 0.0306 | 18.5207 | 1.13 | 15,577.0 | 0.0122 |
| 7/22 | 0.0396 | 0.0223 | 22.2366 | 1.27 | 18,443.8 | 0.0285 |

7/22 has clearly better plateau quality, but it must spend 0.0285 additional normalized Ret/DD instability before quality is even allowed to compare it. This is the exact bounded trade-off the first design lacked.

### Strategy_8.10.634

| Candidate | R_retdd | R_aux | median Ret/DD | median Sharpe | median Net Profit | epsilon_ret required |
|---|---:|---:|---:|---:|---:|---:|
| 9/30 | 0.0176 | 0.0331 | 9.4101 | 1.14 | 11,901.6 | 0 |
| 6/34 | 0.0243 | 0.0250 | 11.3986 | 1.20 | 12,683.0 | 0.0066 |
| 6/22 | 0.0871 | 0.0227 | 11.7347 | 1.32 | 13,900.5 | 0.0694 |

This is the inverse failure mode. Exact stability-first would choose 9/30 and throw away roughly 21% median Ret/DD versus 6/34 for only 0.0066 of normalized Ret/DD stability. The indifference region exists precisely so such a small stability difference can be declared immaterial and quality can choose 6/34.

### Strategy_2.17.581

| Candidate | R_retdd | C_retdd | R_aux | median Ret/DD | median Sharpe | median Net Profit | epsilon_ret required |
|---|---:|---:|---:|---:|---:|---:|---:|
| 6/34 | 0.0703 | 0.0664 | 0.0462 | 17.3419 | 1.30 | 18,479.8 | 0 |
| 6/24 | 0.1752 | 0.0471 | 0.0587 | 18.7020 | 1.36 | 17,682.4 | 0.1048 |
| 6/22 | 0.2581 | 0.2581 | 0.0682 | 18.7020 | 1.32 | 17,754.6 | 0.1877 |

6/24 requires a very large Ret/DD stability allowance for a single-digit-percent median Ret/DD improvement. 6/22 additionally exposes a center far from its neighborhood median; normalized MAD alone would materially understate that topology. Policy A keeps both out unless the Owner explicitly declares a very large stability indifference region.

### Strategy_6.39.493

| Candidate | R_retdd | R_aux | median Ret/DD | median Sharpe | median Net Profit | epsilon_ret required |
|---|---:|---:|---:|---:|---:|---:|
| 7/22 | 0.0120 | 0.0133 | 18.0683 | 1.31 | 17,208.4 | 0 |
| 6/24 | 0.0145 | 0.0153 | 18.1205 | 1.31 | 17,236.2 | 0.0025 |
| 6/26 | 0.0286 | 0.0078 | 18.1205 | 1.32 | 17,236.2 | 0.0166 |
| 7/30 | 0.0750 | 0.0666 | 21.3533 | 1.32 | 18,501.1 | 0.0629 |

The Manager's "tiny quality gain versus ~2.4× Ret/DD dispersion" class of issue is exactly what the band controls. 6/24 is genuinely close enough to 7/22 that a very small `epsilon_ret` could intentionally let quality decide. 7/30 is not in the same stability regime unless the Owner chooses a much wider allowance.

## 9. Synthetic adversarial examples

### S1 — sharp center peak hidden by MAD

```text
10 10 10
10 20 10
10 10 10
```

For the metric shown: median=10, MAD=0, but center deviation=1.0 after normalization by scale 10. `R_x=1.0`. The center peak cannot masquerade as a stable plateau.

### S2 — one downside corner

```text
 5 10 10
10 10 10
10 10 10
```

MAD=0 and center deviation=0, but Ret/DD cliff=(10-5)/10=50%. The cliff guard owns this failure mode.

### S3 — same values, downside direct neighbor

```text
10  5 10
10 10 10
10 10 10
```

The hard cliff is still 50%. V2 intentionally does not invent a stricter direct-neighbor multiplier. The distinction is acknowledged but deferred for lack of evidence.

### S4 — tiny stability difference, huge quality difference

Candidate A: `R_retdd=0.020, median Ret/DD=10`. Candidate B: `R_retdd=0.026, median Ret/DD=20`.

Exact stability-first would always choose A. Policy A lets B compete iff `epsilon_ret >= 0.006`; the Owner controls whether that difference is materially equivalent.

### S5 — tiny quality gain, material stability loss

Candidate A: `R_retdd=0.020, median Ret/DD=10.00`. Candidate B: `R_retdd=0.100, median Ret/DD=10.05`.

For any `epsilon_ret < 0.080`, B never reaches quality. A 0.5% quality gain cannot silently buy a 0.08 normalized stability loss.

### S6 — broad monotonic surface

```text
 8  9 10
 9 10 11
10 11 12
```

Center deviation is zero, but normalized MAD is nonzero and carries the broad slope. The topology addition does not replace MAD.

### S7 — high non-center outlier

```text
20 10 10
10 10 10
10 10 10
```

MAD=0, center deviation=0 and downside cliff=0. Policy A may treat this as stable. This is deliberate: the selected center is representative of the plateau and the isolated outlier is upside, not a fragility that can make the selected center fail.

### S8 — threshold boundary

Candidate A has `R_retdd=0.0200`; Candidate B has `R_retdd=0.0301`; `epsilon_ret=0.0100`. B is out. A microscopic data change to 0.0300 puts B in.

This discontinuity is inherent to any semantic band. Mitigation is not fuzzy comparison: version the threshold, use only a small numeric epsilon for floating equality, report distance-to-boundary, and require sensitivity around the Owner-selected materiality value.

## 10. Complexity / KISS comparison

| Property | Plain Pareto | Policy A — nested bands | Policy B — regret tiers |
|---|---|---|---|
| Ret/DD priority explicit | No | Yes | Indirect |
| Bounded quality trade-off | No | Yes | Yes |
| Weighted scalar | No | No | No |
| Materiality parameters | 0 but implicit trade-offs | 2 | 3+ |
| Handles center peak | No with MAD alone | Yes | Yes if R_x used |
| Deterministic/transitive | Yes | Yes | Yes |
| Easy Owner explanation | Medium | High | Medium |
| KISS | Medium | High | Medium-low |

Policy A adds exactly two semantic degrees of freedom: how much Ret/DD stability difference is immaterial, and how much auxiliary stability difference is immaterial.

## 11. Recommended policy

Recommend Policy A:

```text
eligibility
-> cliff gate
-> R_x = max(normalized MAD_x, normalized center deviation_x)
-> Ret/DD stability indifference band
-> Sharpe/Profit worst-dimension indifference band
-> median Ret/DD DESC
-> median Sharpe DESC
-> median Net Profit DESC
-> deterministic stability/technical tie-break
```

### Q7 — quality lexicographic verdict

Keep quality lexicographic in V2 **deliberately**, not accidentally.

Reason: once candidates reach quality, their stability differences are already bounded by explicit indifference semantics. Ret/DD being the first quality axis is consistent with the Owner's stated priority and avoids introducing another weighted utility function or another family of quality thresholds.

Iteration 2 searched the wave2a replay for a concrete red flag under several exploratory stability-band widths: cases where less than 1% median Ret/DD advantage beat an alternative with more than 5% median Sharpe advantage or more than 10% median Net Profit advantage. None were found in those probes.

Therefore a quality-equivalence band is YAGNI for V2 unless final adversarial review produces a real counterexample. Numeric floating equality still uses a canonical implementation epsilon; that epsilon is not semantic materiality.

## 12. What remains Owner-semantic

### O1 — `epsilon_ret`

The Owner must decide how much extra normalized Ret/DD instability is materially equivalent to the best post-cliff candidate.

This is the primary semantic knob. It must not be inferred from which wave2a winner looks preferable.

### O2 — `epsilon_aux`

The Owner must decide how much extra worst-dimension Sharpe/Net Profit instability is materially equivalent once Ret/DD equivalence is satisfied.

### O3 — cliff threshold

25/30/35/40 remain exploratory. 35% remains a candidate, not frozen.

### O4 — confirm deliberate quality order

Ratify that after stability equivalence, quality is intentionally `median Ret/DD -> median Sharpe -> median Net Profit`.

## 13. What remains evidence-blocked

- Exact durable replay still requires WFM CELL/MetricSet values, not only the Optimizer export.
- `OPTIMIZER-CANDIDATES.csv` and WFM durable picks can differ due re-evaluation; `Strategy_1.8.669` already demonstrates 1.33 vs 1.35 Sharpe for the same selected CELL.
- The two materiality parameters must be sensitivity-tested against exact durable evidence before SPEC freeze.
- The final adversarial review must test distance-to-band-boundary churn and input-shuffle determinism.
- No evidence currently supports axis-specific or corner-vs-direct cliff weighting.

## 14. Cliff threshold findings

The replay must distinguish pre-cliff eligibility from cliff rejection.

```text
34 total Strategies
18 have >=1 structurally complete 3×3 with all 9 CELLs cell_passed=true before cliff
16 have none before cliff
```

Among those 18 pre-cliff-eligible Strategies:

```text
cliff <= 25%:
  4 Strategies lose all candidates
  14 retain >=1

cliff <= 30%:
  3 Strategies lose all candidates
  15 retain >=1

cliff <= 35%:
  0 Strategies lose all candidates
  18 retain >=1

cliff <= 40%:
  0 Strategies lose all candidates
  18 retain >=1
```

The 34→18 reduction is therefore **pre-cliff eligibility**, not a 35% cliff effect.

## 15. Exact next gate

`FINAL_ADVERSARIAL_DESIGN_REVIEW`.

The Primary Technical Manager should review:

1. whether `R_x=max(D_x,C_x)` is sufficient topology for V2;
2. whether nested, minima-anchored additive bands correctly encode materiality;
3. Owner candidates for `epsilon_ret`, `epsilon_aux` and cliff threshold based on semantics and sensitivity, not historical outcomes;
4. exact durable WFM replay plan.

Do not start SPEC or implementation.

Final status: `DESIGN_V2_CANDIDATE_READY`.
