---
type: skill
schema_version: 1
name: agents-os-conflict-resolution
scope: global
created: 2026-06-27
updated: 2026-08-10
description: Detect and handle contradictions in Agent Memory System knowledge. Use when new information conflicts with existing Sistema 2 documentation, Sistema 1 memory, ADRs, known errors, user preferences, or Graphify-retrieved context, and the agent must resolve the contradiction and leave an auditable log.
aliases:
  - agents-os-conflict-resolution
load_policy: manual
indexable: true
index_priority: high
tags:
  - kind/skill
  - action/conflict-resolution
  - tech/agents-os
  - scope/global
---

# Agent Memory System Conflict Resolution

## Purpose

Prevent silent corruption of the vault. Make contradictions explicit, sourced, resolved by the agent when possible, and auditable through journal logs.

## Minimal Read

Canonical create: use `materialize_schema_note.py` per `note-types.md`; never hand-copy frontmatter.

Read only the conflicting source notes and `../_shared/note-types.md` if the conflict type is unclear.

## Procedure

1. State the old claim and source.
2. State the new claim and source.
3. Classify the conflict:
   - stale canonical fact;
   - competing decisions;
   - obsolete learning;
   - ambiguous naming/entity duplicate;
   - evidence gap.
4. Decide the safest resolution from available sources and loaded context.
5. Update affected memory or Sistema 2 notes directly when needed.
6. Create a journal log with old claim, new claim, source links, resolution, changed files, and rationale.

## Output

```text
Conflict:
Old source:
New source:
Impact:
Recommended resolution:
Applied change:
Journal log:
```

## Examples

### Stale Entity Fact

- Old source: `[[active-entity]]` says a dependency is version A.
- New source: repository build file shows version B and tests run against B.
- Resolution: update the Sistema 2 application note to version B, link evidence by
  file path/commit when available, and create a `change_log` with
  `Tipo: updated`.

### Obsolete Learning

- Old source: L3 learning says a workaround is required for a command.
- New source: successful validated run shows the workaround is no longer needed.
- Resolution: update the learning if the historical rationale is still useful,
  or delete/replace it if it would mislead future agents. Create a `change_log`
  explaining why the old behavior is obsolete.

## Hard Rules

- Do not merge contradictory claims by wording around them.
- Do not demote an ADR or learning without recording why.
- Do not block on broad user questions; create a logged resolution or a follow-up task only when evidence is truly insufficient.
