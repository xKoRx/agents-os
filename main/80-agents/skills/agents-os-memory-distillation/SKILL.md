---
type: skill
schema_version: 1
name: agents-os-memory-distillation
scope: global
created: 2026-06-27
updated: 2026-09-03
description: Distill reusable Agent Memory System memory from a session, note, PR, incident, or implementation. Use when extracting learnings, ADRs, known errors, runbooks, patterns, anti-patterns, preferences, or other operational knowledge that should affect future agent behavior.
load_policy: manual
indexable: true
index_priority: high
tags:
  - kind/skill
  - action/distillation
  - tech/agents-os
  - scope/global
---

# Agent Memory System Memory Distillation

## Purpose

Extract only reusable knowledge. Separate learnings, decisions, known errors, runbooks, and entity updates so future agents can load the right memory cheaply.

## Minimal Read

Canonical create: use `materialize_schema_note.py` per `note-types.md`; never hand-copy frontmatter.

Read `../_shared/note-types.md` when deciding artifact type. Read `../_shared/metadata-schema.md` when creating or editing notes.

## Procedure

1. List candidate facts from the source.
2. Drop anything that is only transient progress, logs, or evidence.
3. Classify each reusable item:
   - learning;
   - decision/ADR;
   - known error;
   - runbook;
   - entity update proposal;
   - conflict.
4. Assign the narrowest scope and a concrete load policy. `always` is reserved for the single compact global internal memory; domain memory uses an entity/error/manual trigger.
5. Link every memory to at least one real Sistema 2 entity.
6. Search for duplicates before proposing a new note.
7. For continuity, resolve `continuity_key` and update the one active checkpoint in place. Create a successor only for a material scope or identity change, and retire the prior checkpoint atomically.
8. Create, update, delete, or defer compact memory artifacts and record public-memory changes in journal.

## Internal Continuity Lifecycle

1. Resolve the entity and choose a stable `continuity_key` such as `project/<project-slug>/<concern>`.
2. Search for an active note with that key before writing. If one exists, update it in place and remove stale progress; do not append another checkpoint.
3. Keep `memory_state: active` only on the current checkpoint and use `when_project_loaded`, `when_application_loaded`, `when_error_matches` or another concrete scoped trigger.
4. If replacement is unavoidable, write the successor and then change the prior note to `memory_state: superseded`, `load_policy: manual`, `index_priority: low` and `superseded_by: "[[<successor>]]"`; the successor records `supersedes`.
5. Historical cleanup changes `superseded` to `archived` only when no normal retrieval path needs it. Never reactivate an old checkpoint without first retiring the current one.

## Promotion Test

Create a memory note only if it answers at least one:

```text
What should a future agent do differently?
What decision explains current behavior?
What failure may repeat?
What operation has a validated procedure?
When should this be loaded?
```

## Confidence And Promotion Thresholds

Use the shared `confidence` values as promotion thresholds:

- `verified`: create or update memory when backed by tests, official docs,
  production evidence, committed code, or an observed successful command.
- `high`: create or update memory when validated in the session with clear
  local evidence, but not independently confirmed outside the session.
- `medium`: defer by default unless the risk of forgetting is higher than the
  risk of recording it; prefer internal memory or a follow-up task.
- `low`: do not create public L3 memory. Use internal memory only if it helps a
  future agent reason, and label it as hypothesis.

Public memory should usually require `high` or `verified`. A `medium` public
memory is allowed only when it is explicitly scoped, reversible, and includes a
clear evidence gap.

## Duplicate Detection Workflow

Before creating memory:

1. Query Graphify with `entity + type + topic` for the candidate artifact.
2. Search source Markdown by slug and likely aliases when Graphify is degraded.
3. Open matching candidate notes before deciding.
4. If the new fact refines an existing note, update that note and create a
   change log instead of creating a sibling note.
5. If the old note is obsolete, replace or delete it and log the reason.
6. Create a new note only when scope, symptom, operation, or decision rationale
   are materially different.

## Public Memory Change Logging

Any create, update, delete, or replacement under `80-agents/memory/public/`
must leave a `type: change_log` note under `80-agents/journal/logs/`.

The log should include:

- changed file path;
- change type: `created`, `updated`, `deleted`, or `conflict-resolution`;
- source session or evidence reference;
- duplicate check performed;
- reason the change should affect future agents.

Internal memory changes do not need routine public logs unless they promote or
modify shared public memory.

## Reject As Non-Reusable

Reject candidates like:

- "Ran tests today" without a stable command, failure mode, or runbook.
- "Investigated file X" when it only describes session progress.
- Raw stack traces or logs without a repeatable symptom and mitigation.
- A vague preference such as "be careful" without scope or future behavior.
- A domain fact that belongs directly in the Sistema 2 entity note.

## Output

```text
Created:
Updated:
Deleted:
Deferred:
Rejected as non-reusable:
Duplicates checked:
Entity links:
Confidence:
Journal logs:
```

## Hard Rules

- Do not duplicate entity descriptions inside memory notes.
- Do not create vague learnings without scope.
- Prefer fewer, stronger notes over many weak notes.
- Store evidence references, not heavy evidence.
- Do not use Sistema 2 `status` on memory. Internal continuity uses `memory_state`; public obsolete memory is deleted or replaced with its change log.
- Never leave more than one active note for a `continuity_key`.
