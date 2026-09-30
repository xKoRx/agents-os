# ECHO FORGE — ROBUST RUN SELECTION V2
# DESIGN FREEZE — KISS IMPLEMENTATION AUTHORITY

Status: `READY_FOR_SHOT_1`

Date: 2026-09-30

## Authority

This document is the canonical implementation authority for Robust Run Selection V2.

Where earlier design/review artifacts conflict with this freeze, **this document wins**.

Earlier artifacts remain useful as design history and evidence, but the following prior recommendations are explicitly superseded:

- introducing `evaluation_policy` / `evaluation_policy_version`;
- making exact durable replay a blocker for implementation or SPEC;
- treating the missing historical `cells.tsv` payload as a blocker for Shot 1.

## KISS contract

### 1. V2 is another algorithm in the existing WFM configuration mechanism

V2 must be implemented as a **new algorithm selectable through the existing algorithm/config extension point** already used by WFM.

Conceptually:

```text
existing V1 algorithm/config
→ exact existing V1 behavior

new V2 algorithm/config
→ Robust Run Selection V2 behavior
```

Do **not** introduce a second policy architecture, registry, dispatch layer or `evaluation_policy`.

The exact V2 algorithm identifier should follow the naming convention already present in Symphony.

### 2. V1 is immutable

No semantic change to:

- existing V1 algorithm identifiers;
- `dispersion_cov`;
- V1 defaults;
- V1 ranking;
- V1 typed config/digest behavior;
- downstream `select_robust_run`.

`select_robust_run` continues to consume the unique `rank == 1`.

### 3. Scope

Selection remains strictly intra-strategy over 3×3 neighborhoods.

No cross-strategy ranking.

## V2 algorithm

Required metrics per neighborhood:

- Ret/DD;
- Sharpe;
- Net Profit.

For each metric `x`:

```text
M_x     = median(x[9])
scale_x = median(abs(x[9]))
MAD_x   = median(abs(x_i - M_x))

D_x =
  0                    if scale_x == 0 and MAD_x == 0
  +Inf                 if scale_x == 0 and MAD_x > 0
  MAD_x / scale_x      otherwise

C_x =
  0                               if scale_x == 0 and abs(center_x-M_x) == 0
  +Inf                            if scale_x == 0 and abs(center_x-M_x) > 0
  abs(center_x-M_x) / scale_x     otherwise

R_x = max(D_x, C_x)
```

Thus:

```text
R_retdd
R_sharpe
R_profit
R_aux = max(R_sharpe, R_profit)
```

Ret/DD cliff:

```text
L     = median(RetDD[9])
scale = median(abs(RetDD[9]))
tail  = min(RetDD[9])

cliff =
  0                         if scale == 0 and L == tail
  +Inf                      if scale == 0 and L != tail
  max(0, (L-tail)/scale)    otherwise
```

Derived fail-closed rule:

```text
if any of:
  R_retdd
  R_sharpe
  R_profit
  R_aux
  cliff
is non-finite

→ candidate ineligible
```

If no candidate remains, the Strategy has no acceptable neighborhood / analytical FAIL using the existing evaluator semantics.

Then:

```text
cliff <= configured cliff_threshold
```

Primary stability:

```text
ret_best = min(R_retdd)

keep if:
R_retdd <= ret_best + epsilon_ret
```

Auxiliary stability:

```text
aux_best = min(R_aux among primary survivors)

keep if:
R_aux <= aux_best + epsilon_aux
```

Final quality/ranking among survivors:

```text
median Ret/DD DESC
median Sharpe DESC
median Net Profit DESC
R_retdd ASC
R_aux ASC
runs ASC
OOS ASC
```

No center metric is ranking authority.

## V2 configuration

V2 adds only the configuration required by the algorithm:

```text
new algorithm identifier
cliff_threshold
epsilon_ret
epsilon_aux
```

The three numeric parameters must be finite and >= 0.

For V2, missing/invalid required parameters are configuration errors.

Do not add silent defaults merely to make V2 run.

No production numeric values are frozen by this document; they remain explicit configuration values.

## Explicitly out of scope

Do not add:

- Pareto layers;
- weighted stability authority;
- weight optimization;
- surface fitting;
- spatial/corner/axis weights;
- quality bands;
- cross-strategy ranking;
- a new policy framework;
- `evaluation_policy`;
- durable evidence recovery code;
- SQX reruns for historical reconstruction.

## Historical durable replay finding

The historical wave2a `cells.tsv` in Agents-OS is zero bytes while its checksum manifest references a non-empty payload.

That is a **historical evidence/certification issue only**.

It may be revisited later for replay/certification if the original durable evidence is recovered.

It does **not** block implementing V2 with deterministic unit/integration tests and V1 regression coverage.

## Implementation gate

```text
DESIGN = CLOSED
SHOT_1 = READY
```

Shot 1 should implement the smallest code/config/test delta necessary for the new algorithm.

If the existing algorithm extension point cannot support V2 without a material architectural change, stop and return to the Primary Manager instead of inventing a framework.
