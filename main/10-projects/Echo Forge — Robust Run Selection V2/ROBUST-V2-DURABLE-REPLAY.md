# ROBUST-V2-DURABLE-REPLAY

> **AUTHORITY NOTE — HISTORICAL EVIDENCE ONLY (2026-09-30):** This report documents the missing historical CELL/MetricSet replay authority. It is **not an implementation blocker** and does not reopen the V2 design. The zero-byte `cells.tsv` finding is deferred to later evidence/certification work. Canonical implementation authority is [[ROBUST-V2-DESIGN-FREEZE]].


Status: `DURABLE_REPLAY_BLOCKED_EVIDENCE`

Date: 2026-09-30

Scope: exact durable replay gate for Echo Forge Robust Run Selection V2. Evidence recovery only. No SPEC, no product code, no SQX rerun, no Owner values chosen.

## 1. Gate outcome

The replay stops at the first required gate:

```text
DURABLE_EVIDENCE
→ BLOCKED
```

V1 exact reproduction was not executed. V2 offline replay, cliff sensitivity, epsilon breakpoints and the Owner decision pack were not executed.

This is an evidence-access failure, not a V1 mismatch and not a V2 design defect.

## 2. Exact wave authority

Target FlowRun:

```text
80647dc2-848a-4150-842e-cc6947eed87c
```

Expected durable shape from the wave2a contract:

```text
34 Strategies
54 CELL coordinates / Strategy
1836 CELL coordinates total
runs = 5,6,7,8,9,10
OOS  = 20,22,24,26,28,30,32,34,36
```

Known durable outcome currently preserved in the compact artifacts:

```text
10 selected
24 rejected
34 aggregate rows
46 emitted V1 picks
```

## 3. Git evidence integrity finding

Canonical artifact path:

```text
main/10-projects/Echo Forge — Operación Real V2/artifacts/c52-wave2a-20260929/cells.tsv
```

Current Git payload is zero bytes.

The sibling checksum manifest declares:

```text
3e0dac89805df320d416820cf57f067d8bddf766fb74b151bc64c88cb81a76d1  cells.tsv
```

Git history was checked rather than querying an unrelated/latest wave.

The artifact bundle was introduced by:

```text
xKoRx/agents-os@8385041a88c17ed0aaba577115bac0c45b429012
```

In that commit, `cells.tsv` was introduced without a recoverable non-empty patch/content. Earlier relevant wave2a commits do not contain that path. Therefore there is no Git-history payload that can be restored and verified against the declared SHA256.

The historical zero-byte artifact is preserved unchanged.

## 4. What remains usable — but is not CELL authority

The following compact artifacts are present and useful as downstream cross-checks:

```text
aggregates.tsv
picks.tsv
ROBUST-SELECTION-AUDIT.csv
OPTIMIZER-CANDIDATES.csv
OPTIMIZER-FUNNEL.csv
SHA256SUMS.txt
```

`aggregates.tsv` preserves 34 aggregate outcomes.

`picks.tsv` preserves 46 emitted V1 picks with exact CELL EvaluationRef / MetricSetRef identities, ranks, runs/OOS, ranking metric values and robustness scores.

Those outputs are insufficient to reproduce the V1 evaluator because the complete CELL metric corpus is missing from the accessible authority.

`OPTIMIZER-CANDIDATES.csv` is explicitly not substituted for WFM durable CELL/MetricSet evidence.

## 5. Durable authority known to exist

The wave2a operating evidence records that the real run produced:

```text
1836 wfm-cell-evaluation.v1
34   wfm-aggregate-evaluation.v1
```

under the exact wave2a run, with WFM evidence in the durable evidence store / Mongo path used by Forge and raw WFM artifacts under the wave2a MinIO lineage. Robust-selection Decisions are additionally durable in PostgreSQL.

The current execution surface does not expose an authorized read path to those exact Mongo/MinIO/PostgreSQL records. This does not assert that the records are missing from the runtime; it means their exact immutable payload and lineage cannot be established from the currently accessible surfaces.

A Library search for the missing `cells.tsv` payload, its declared SHA256, a prior `ROBUST-V2-DURABLE-CELLS.csv`, and the matrix artifact did not recover an independent exact CELL corpus.

## 6. Exact missing evidence

Replay cannot proceed until a read-only recovery establishes, for the exact FlowRun and every required CELL:

```text
StrategyRef
StageExecutionRef
runs_count
oos_percent
CELL EvaluationRef
CELL MetricSetRef
cell pass state
Ret/DD + status
Sharpe + status
Net Profit + status
CELL → MetricSet lineage
CELL → StageExecution lineage
```

It must also establish the exact 34 aggregate Evaluations and the actual V1 evaluator identity/configuration:

```text
neighborhood contract
grid config + grid_config_digest
scoring_algorithm + version
ranking_metric
primary_metric
metric filters
thresholds / warning rules
top_n
typed evaluator config
evaluator_config_digest
```

The recovery must be scoped by exact refs/FlowRun. No “latest”, Strategy-name reconstruction, another FlowRun, Optimizer substitution or SQX regeneration is valid.

## 7. Phase status

### V1 reproduction

```text
NOT_RUN — durable CELL/MetricSet authority not established
```

Therefore none of these can be certified yet:

```text
34/34 aggregate reproduction
0 identity mismatches
0 rank mismatches
shuffle determinism
exact selected/rejected reproduction from evaluator inputs
```

The existing 10/24 result is preserved as reference output only.

### V2 replay

```text
NOT_RUN — hard-gated by V1 replay
```

No cliff threshold sensitivity, epsilon_ret breakpoints, epsilon_aux breakpoints, mandatory-Strategy durable comparisons or quality-order contradiction checks were computed from Optimizer approximations.

### Owner values

```text
cliff_threshold: NOT_READY
epsilon_ret:     NOT_READY
epsilon_aux:     NOT_READY
quality order:   NOT_READY_FOR_DURABLE_RATIFICATION

OWNER_VALUES_CHOSEN_BY_WORKER: NONE
```

## 8. Required next exact action

Use a read-only durable evidence channel against the original wave2a stores and exact FlowRun `80647dc2-848a-4150-842e-cc6947eed87c`.

Recover/materialize the original 1836 CELL Evaluation + MetricSet records and 34 aggregate Evaluations with provenance. If a compact canonical export does not already exist, generate:

```text
ROBUST-V2-DURABLE-CELLS.csv
```

as a deterministic replay materialization, record its row count, SHA256 and query/source contract, then verify:

```text
34 Strategies
54 coordinates each
1836 total
0 duplicate coordinates
exact FlowRun/StageExecution scope
internally consistent lineage
no cross-wave contamination
```

Only after that gate passes should V1 replay run. V2 sensitivity and the Owner decision pack remain downstream.

## 9. Final gate

```text
DURABLE_REPLAY_BLOCKED_EVIDENCE
```
