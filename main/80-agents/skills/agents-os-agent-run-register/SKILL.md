---
type: skill
schema_version: 1
name: agents-os-agent-run-register
description: Register one auditable code-generation execution by canonical agent surface and exact model. Use after a material coding, debugging, review, testing or code-related work segment completes or pauses, when the user asks to compare IDEs/models, or during explicit session close if that execution has not yet been recorded.
scope: global
created: "2026-08-11"
updated: "2026-08-11"
entities:
  - "[[AGENTS OS]]"
related:
  - "[[Codex]]"
  - "[[Claude Code]]"
  - "[[Cursor]]"
  - "[[Antigravity]]"
aliases:
  - agents-os-agent-run-register
load_policy: manual
indexable: true
index_priority: high
tags:
  - kind/skill
  - scope/global
  - tech/agents-os
  - action/agent-run-register
---

# agents-os-agent-run-register — Agent Run Registration

## Purpose

Create one compact `type: agent_run` journal record per attributable surface×model work segment so later comparisons use observed evidence rather than mixed free text or event-only feedback.

## Minimal Read

Read only:

1. `../../crew/INDEX.md` to resolve the canonical surface.
2. `../../templates/agent-run.md` through `materialize_schema_note.py`; never copy it manually.
3. The relevant verification output and changed-artifact summary.

## Procedure

1. Trigger only after material code generation or modification, debugging, code review, testing, or a code-related segment that produced an attributable outcome. Documentation-only and lookup-only work does not create a run.
2. Resolve `agent_surface` to a canonical `type: agent` note. The initial supported set is [[Codex]], [[Claude Code]], [[Cursor]] and [[Antigravity]]; extend the registry before using a new surface.
3. Record the exact host- or user-reported identifier in `agent_model`. Never infer the model from the surface, date, capabilities or prose. Use `unknown` with `model_source: unknown` when the host exposes no reliable value.
4. Segment by surface×model: a model switch, delegated subagent on another model, or handoff to another surface creates a separate run when its contribution and evidence are materially attributable. Do not split routine tool calls made by the same combination.
5. Materialize `agent_run` under `80-agents/journal/agent-runs/` as `YYYY-MM-DD[-HHMM]-<surface>-<model>-<topic>.md`; use `HHMM` only for same-day collisions.
6. Fill task type, complexity, outcome, verification, evaluator and user rework from observed state. `user_rework: unknown` is correct until later user feedback provides evidence.
7. Add 1–5 score fields only when evidence supports them. Self-scoring uses `evaluator: agent`; owner corrections change it to `owner` or `mixed`. Preserve objective evidence in the body.
8. Link related feedback to the run. A run is performance evidence and does not trigger feedback; feedback remains event-driven.
9. Do not reindex Graphify for the run alone because journal paths are excluded. Reindex only if a canonical surface profile or another indexable source changed.

## Output

```text
Agent run: <path | skipped with reason>
Surface: [[canonical]]
Model: <exact | unknown>
Outcome / verification: <value> / <value>
Evaluator / rework: <value> / <value>
```

## Hard Rules

- One record per attributable surface×model segment; never one aggregate record for a multi-model session.
- Do not compare models using self-scores alone; retain outcome, verification and user rework as observable dimensions.
- Do not retrofit historical free-text `agent` values by guesswork. Normalize history only with explicit evidence.
- Never store prompts, chain-of-thought, secrets, heavy logs or full diffs in an agent run.
