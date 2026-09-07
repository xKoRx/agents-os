---
type: decision
schema_version: 1
scope: project
created: "2026-08-27"
updated: "2026-08-27"
area:
project: "[[Echo Forge]]"
application:
entities: []
related: []
aliases: []
confidence: verified
source_session: SQX-CROSS-FLOWRUN-BUILDER-TEMPLATES-CORRECTION-NORMAL
load_policy: when_project_loaded
indexable: true
index_priority: high
tags:
  - kind/decision
  - scope/project
---

# FD-9 — Historical Builder templates use cohort provenance

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Contexto

- Historical downstream reuse was already certified closed; this decision applies only to the new Builder template mode.

## Decisión

- `stage=builder` with non-empty `source_folder` resolves one completed, cross-FlowRun historical cohort through the shared durable resolver. Source StrategyRefs are registered `REUSED`/`is_origin=false`; the cohort is passed to one Builder StageExecution whose subject remains `FLOW`.
- Stage inputs are derived internally as `template:<canonical StrategyRef>` plus the exact historical EvaluationRef. Canonical stage-input sorting makes identity independent of arrival order; changing one cohort binding changes StageExecution identity.
- Builder outputs are adopted solely from their output canonical IDs. A canonical collision with any template canonical ID is a `CONTRACT_CONFLICT` before adoption/evidence persistence. There is no individual template-to-output mapping.
- Template CFX must bind the Build task exactly once to databank `input` using the real task XML syntax. Runtime validates and fails closed; it never auto-patches the Build task.

## Rationale

- This preserves Strategy Identity v2, output namespace ownership, schema, migration, participation roles, and downstream Retester/Optimizer historical semantics. A Builder output can receive a new StrategyRef only when its canonical output identity is new under existing adoption semantics.

## Consecuencias

- Treating templates as a same-StrategyRef downstream reuse; inheriting template StrategyRefs into outputs; accepting Project-level `input` without an effective Build-task binding; using filename/listing as identity authority; adding a new schema or participation role.

## Alternativas descartadas

- Reabrir downstream historical reuse, introducir fan-out histórico para Builder, heredar StrategyRef del template, o auto-parchear el binding CFX.
