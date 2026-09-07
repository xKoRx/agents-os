---
type: skill
schema_version: 1
name: agents-os-session-feedback
scope: global
created: 2026-06-27
updated: 2026-08-11
description: Capture compact feedback only when AGENTS OS had real friction, degraded retrieval, an uncovered Sistema 1 gap, periodic sampling, or an explicit feedback request. A normal clean close does not invoke this skill.
load_policy: manual
indexable: true
index_priority: high
tags:
  - kind/skill
  - action/feedback
  - tech/agents-os
  - scope/global
---

# agents-os-session-feedback - Session Feedback Capture

## Purpose

Capture one compact Sistema 1 feedback note from the acting agent — but only
when feedback is warranted. Feedback is **event-driven**, not automatic.

Trigger conditions (any one):

- Real friction was encountered (tool failure, missing support, slow path).
- Retrieval was degraded and a workaround was needed.
- A gap in Sistema 1 was detected that the system does not solve.
- Periodic sampling asks for one (e.g. the hygiene cycle requests one).

A clean close with no friction → no feedback note. Do not write feedback to
fill a quota; that pollutes the evidence base the system is trying to keep
clean.

Feedback is not L3 memory by default. It is evaluation data. Promote only
repeated or high-confidence patterns through `agents-os-memory-distillation`.
Operational coordination or hypotheses belong in internal memory
(`80-agents/memory/internal/`) only when they provide durable continuity; the
feedback note may assess whether that memory helped.

## Minimal Read

Canonical create: use `materialize_schema_note.py` per `note-types.md`; never hand-copy frontmatter.

Read only when needed:

- `../../templates/session-feedback.md` for the general note shape.
- `../../templates/graphify-feedback.md` for the Graphify-specific note shape.
- `../_shared/metadata-schema.md` for frontmatter if creating or editing a
  feedback note.
- `../_shared/note-types.md` for Sistema 1 boundaries.

## Inputs

- Current session goal and main entity.
- Canonical agent surface, exact model and related `agent_run` when available.
- Skills used in the session.
- Retrieval mode and relevant sources (especially Graphify CLI/MCP commands).
- Artifacts created, updated, or intentionally skipped.
- The agent's own operational assessment of AGENTS OS and Graphify friction.

## Procedure

1. **Decide if feedback is warranted** by the trigger conditions in Purpose.
   If the session was clean (no friction, no degradation, no gap, not part
   of periodic sampling) → skip this skill entirely. Record nothing.
2. If warranted during a close, run near its end, after the persistence
   outcome is known and before the final user report.
3. Materialize one `type: feedback` note under
   `80-agents/journal/feedback/system-1/` as
   `YYYY-MM-DD-<entity-or-topic>-session-feedback.md`.
4. **Graphify-Specific Feedback**: NOT automatic. Create a dedicated note
   under `80-agents/journal/feedback/graphify/` using
   `YYYY-MM-DD-<entity-or-topic>-graphify-feedback.md` ONLY when Graphify
   was used AND something notable happened — degradation, novel query
   pattern, new pitfall, or unexpected failure. Routine Graphify use with
   no surprises does not warrant a separate note; aggregate it during
   `agents-os-hygiene-cycle` instead.
5. Fill `agent_surface` with the canonical profile link, `agent_model` with the exact reported identifier and `agent_run` with the related execution record when available. Never parse or infer them from legacy free-text `agent` values.
6. Fill the notes with direct, concrete observations from the acting agent (including a critical assessment of the usage and value of Internal Memory in the general session feedback).
7. Keep answers short: one to three bullets per section is enough.
8. Score the session and tool components honestly from 1-5.
9. Identify at most one "Pain Pattern Candidate" that may deserve future L3
  promotion.
10. If a pain pattern is severe, repeated, or immediately actionable, call
  `agents-os-memory-distillation` to decide whether to create/update a
  learning, known error, runbook, ADR, or follow-up task.
11. Do not change public memory only because one feedback note complained about
  something; use feedback as evidence, not automatic policy.

## Output

```text
Feedback note:
Scores:
Most useful:
Main friction:
Missing support:
Pain pattern candidate:
Promotion recommendation:
```

## Hard Rules

- Do not ask the user to write the agent's feedback; the acting agent writes it.
- Do not store secrets, credentials, heavy logs, or private chain-of-thought.
- Do not quote internal memory in the feedback note.
- Do not treat feedback as canonical truth; it is session evidence.
- Do not use feedback as the performance census. Code performance lives in `agent_run`; feedback links it only when feedback is independently warranted.
- Keep feedback notes outside normal retrieval unless AGENTS OS explicitly
  changes the indexing policy later.
- **Feedback is event-driven.** Run this skill only when one of the trigger
  conditions in Purpose holds. A clean session with no friction → no feedback
  note. Do NOT create feedback just because closeout ran.
- Graphify-specific feedback is NOT automatic. Aggregate routine Graphify
  observations during `agents-os-hygiene-cycle`; create a dedicated note only
  when something notable happened.
## Context Efficiency

Assess context/token efficiency observationally.

This is NOT an instruction to reduce work, evidence, autonomy, or verification.

Report only what can be supported from the observed session trajectory.

- `context_high_water_mark`: exact value only if exposed by the agent surface;
  otherwise `unknown`.
- `main_context_growth_sources`: at most 3 concrete contributors.
- `avoidable_context_growth`: repeated reads, oversized command/log/test/query
  output, redundant retrieval, or stale trajectory that materially increased
  context without adding evidence.
- `compaction_opportunity`: whether a durable checkpoint + context compaction
  could have occurred after a closed phase without losing required authority.
- `efficiency_assessment`: GOOD / REVIEW / POOR.

For each material optimization candidate:

- `change`
- `evidence`
- `expected_impact`: LOW / MEDIUM / HIGH
- `risk_to_quality`: LOW / MEDIUM / HIGH

Maximum 3 candidates.

Do not invent token counts or cache metrics that were not exposed by the
surface.

Do not recommend:
- skipping required evidence;
- reducing physical verification;
- weakening auditability;
- reducing necessary reasoning;
- changing product/session protocol merely to save tokens.

Prefer `no material optimization identified` over speculative optimization.