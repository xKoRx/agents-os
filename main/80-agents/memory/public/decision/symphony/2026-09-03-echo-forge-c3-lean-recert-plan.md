---
type: decision
schema_version: 1
scope: project
created: "2026-09-03"
updated: "2026-09-03"
area: "[[Echo]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[Symphony]]"
entities: []
related:
  - "[[2026-08-31-forge-campaign-stop-policy-v1-contract]]"
  - "[[2026-09-02-echo-forge-c3-cert-a-supply-via-aligned-mt5-window]]"
  - "[[2026-09-03-echo-forge-release-0288-cancel-smoke-certified]]"
aliases: []
confidence: verified
source_session: ECHO-FORGE-C3-LEAN-RECERT-DESIGN-TOP
load_policy: when_project_loaded
indexable: true
index_priority: high
tags:
  - kind/decision
  - scope/project
  - project/echo-forge
---

# C3 lean recertification plan (Option A sized, no historical reuse)

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Contexto

- Baseline symphony `7047a9c112502dcb68387745149eed95405b0aae` == origin/master; SDK `c85594440f6755443ceb97ec4e333cd0ddb5b0ed`; physical release `0.2.88`. C3 physical certification still pending. This session is DESIGN ONLY.
- Campaign clones the full base `WorkflowSpec` per wave (`MaterializeForgeCampaignWaveSpec`) and always starts the child with empty `Input`. Historical cohort resolution keys MinIO ownership by **execution** `Wave`, which Campaign rewrites to `forge-<CampaignRef>-wNNNNNN`. `ConfigSourceWave` only routes `.cfx` reads.

## Decisión

- **VERDICT:** `PLAN PASS / CLOSED`. C3 se certifica con Option A sized (LEAN SAFE). Partial pipeline reuse (Options B–F) is **not supported** for Campaign children without new implementation; that gap is documented, not a C3 blocker.
- **Standalone C3-SUPPLY:** ELIMINATED. CERT-A wave 1 is the nonempty-promotion proof (`target_finalists=1`, `max_waves=1`).
- **Do not skip** Builder, Retester, Optimizer, WFM, robust, Apply, final reretester if Promotion keeps `source_ranking=mt5-final-fidelity-ranking`. Score baseline stage key is `sqx_baseline_materialize@sqx-baseline.v1`.
- **Do not rebind** Promotion to `builder-early-per-type` (cheat vs production Promotion surface). Challenge to the 2016–2026 window is accepted: C3 is Campaign orchestration, not A0 Strategy Quality.
- **CERT-A:** one Campaign, one child, `target_finalists=1`, `max_waves=1`. **CERT-B:** one Campaign, two children, `target_finalists=3`, `max_waves=2`. Bound: `rankings.top_n=1` ⇒ ≤1 finalist per wave ⇒ `target > 2*1`.
- **Ephemeral sizing (not committed `input/example/config.json`):** `early_rankings.top_n=1`, `rankings.top_n=1`, `wfm_params.min_pass_cells=1`, MT5+CFX periods equal and short (recommended `2026.05.04`→`2026.06.05` unless worker CFX XML forces another pair). `pool_max`/`target_tops`/`batch_size` do not size Generic Builder.
- C3 remains **not certified**. `MT5_COMPILE_RETRY_POLICY_AUTHORITY_DRIFT` remains OPEN/NON-BLOCKING. Frozen MT5 lifecycle / Windows process tree / 0.2.88 stay frozen.

## Rationale

- Campaign stop evaluation only reads each child's `FINALIST_PROMOTION` Decision (`EvaluateForgeCampaignStop` + first-observation-wins by `StrategyRef`; TARGET precedes MAX). It does not need a prior Generic supply FlowRun.
- Cross-FlowRun reuse is certified for Generic consumers that share the producer `Wave` path. Campaign forbids that sharing by construction. `TaskSource.wave_key` is legacy ranking-store only and is forbidden on `ranking_snapshot`.
- Ranking `top_n=1` is the proven per-wave promotion cardinality bound. Early ranking remains `PER_LOGICAL_TYPE`, so SQX/MT5 fanout may exceed 1 physical candidate; Promotion still emits ≤1 finalist.

## Consecuencias

- Next exact execution prompt: `ECHO-FORGE-C3-LEAN-RECERT-NORMAL`. No source change required to start. No release. Ephemeral configs only.
- Optional later track (not C3): `source_wave` / historical namespace selector that is not the Campaign execution Wave, or injecting durable `Input` into Campaign children. Name: `CAMPAIGN_PARTIAL_PIPELINE_REUSE_NOT_SUPPORTED`.

## Alternativas descartadas

- Option B/C/D/E/F historical start: namespace keyed by execution Wave; child Input always empty.
- Standalone supply Generic: redundant if CERT-A itself must produce `effective_promoted_count>=1`.
- Rebind Promotion to builder-early: cheaper, falsifies the production Promotion surface.
- Keep 2016–2026 MT5 window: comparability needs equality, not decade span; ~47 min/candidate under one-job-per-machine.
- `target_finalists=11`: only valid for `top_n=5`; lean bound is 3.
