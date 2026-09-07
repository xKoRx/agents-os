---
type: decision
schema_version: 1
scope: project
created: "2026-08-30"
updated: "2026-08-30"
area:
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application:
entities: []
related: []
aliases: []
confidence: verified
source_session:
load_policy: manual
indexable: true
index_priority: high
tags:
  - kind/decision
  - scope/project
---

# Finalist Promotion V1 CORE

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Contexto

- Echo Forge needs to convert `RankingSnapshot.TopProjection` into one durable finalist cohort per FlowRun, without creating Strategies/Evaluations or touching Result Surface.

## Decisión

- `FINALIST_PROMOTION` is one durable Decision per FlowRun, with logical subject `FLOW`/`FlowRunRef`, exactly one `RANKING_SNAPSHOT` evidence, policy `finalist_promotion@1.0.0`, and explicit output.
- SQL preserves the `subject_ref` foreign key to `sqx.strategies`; optimizer uses `subject_kind=STRATEGY`, while Promotion uses `subject_kind=FLOW`, `subject_ref=NULL`, reconstructing its subject from `flow_run_ref`.
- Promotion consumes only the exact GLOBAL binding produced by `runGlobalRankingSnapshots`; `effective_top_n=0` persists `COMPLETED` with `TOP_PROJECTION_EMPTY` and `finalists=[]`.

## Rationale

- Separating `RANKING` from `DECISION` prevents re-ranking, latest lookup, and false UUID identity; the partial unique index makes one Promotion per FlowRun contractual.

## Consecuencias

- Optimizer retains `DecisionRef`, `PolicyRef`, and `ContentDigestV1` bytes; Promotion has an independent digest namespace/version. Physical FlowRun certification is the next step.

## Alternativas descartadas

- Casting `FlowRunRef` as `StrategyRef`, removing the FK, creating N Decisions per Strategy, fabricating an Evaluation, or falling back to `OrderedEntries`.
