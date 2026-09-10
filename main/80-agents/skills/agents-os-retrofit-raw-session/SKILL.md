---
type: skill
schema_version: 1
name: agents-os-retrofit-raw-session
scope: global
created: 2026-06-27
updated: 2026-08-10
description: Reprocess old raw sessions into newer memory structures. Use when schemas evolve, missing learnings/ADRs/known errors/runbooks must be extracted from archived L0 sessions, or historical sessions need to be backfilled without making raw sessions part of normal retrieval.
aliases:
  - agents-os-retrofit-raw-session
load_policy: manual
indexable: true
index_priority: high
tags:
  - kind/skill
  - action/retrofit
  - tech/agents-os
  - scope/global
---

# Agent Memory System Retrofit Raw Session

## Purpose

Extract new value from archived raw sessions after the memory schema improves, while keeping L0 out of normal context loading.

## Minimal Read

Canonical create: use `materialize_schema_note.py` per `note-types.md`; never hand-copy frontmatter.

Read `agents-os-memory-distillation` first. Read `../_shared/metadata-schema.md` only when creating backfilled artifacts.

## Procedure

1. Select raw sessions by date, project, entity, or explicit path.
2. Read only the selected raw session and already-linked summary, if present.
3. Distill using the current schema.
4. Mark generated artifacts as backfilled from raw.
5. Link every artifact to Sistema 2 entities and the source raw session.
6. Recommend Graphify reindex for newly created indexable notes.

## Backfill Metadata

Use existing metadata fields before adding new ones. For every artifact
created from retrofit:

```yaml
source_session: "<raw-session-link>"
related:
  - "<raw-session-link>"
  - "<session-summary-link>" # when present
confidence: high|verified|medium
tags:
  - kind/<memory-type>
  - source/backfill
```

Rules:

- `source_session` points to the L0 raw session that was processed.
- If multiple raw sessions support the same artifact, keep the strongest one in
  `source_session` and list the others in `related`.
- Use `confidence: verified` only when the raw session cites durable evidence
  such as a committed file, test run, official doc, or production artifact.
- Use `confidence: high` when the session itself validates the behavior.
- Use `confidence: medium` only for scoped, reversible memory with a clear
  evidence gap; defer weak or ambiguous candidates.
- Do not add `status`, `draft`, or raw transcript excerpts to the generated
  artifact.

## Batch Limits

Default limits:

- Process at most 1 raw session per pass when no explicit batch size is given.
- Process at most 3 raw sessions per pass even when the user asks for a batch,
  unless the sessions are tiny and summaries already exist.
- Read the linked L1 summary first when present; open the raw L0 only for
  evidence that the summary cannot answer.
- Stop after 5 candidate memory items and run duplicate detection before reading
  more raw content.
- Keep the working context focused on one project/entity at a time.

Escalate to a follow-up task instead of continuing when:

- raw transcripts are large enough to crowd out source notes;
- the batch spans unrelated projects/entities;
- duplicates or conflicts require careful resolution;
- evidence points to Sistema 2 changes that need direct entity updates/logs.

## Duplicate Detection Against L3

Before creating backfilled memory:

1. Identify candidate type, entity, and topic.
2. Query Graphify with:

```text
<entity> <memory-type> <topic>
```

3. Search source Markdown when Graphify is degraded:

```text
80-agents/memory/public/<memory-type>/
```

4. Open matching L3 notes before deciding.
5. If an existing L3 note covers the same future behavior, update it and log the
   change instead of creating a new note.
6. If the new information only provides more evidence for an existing note, add
   a compact evidence reference and log the update.
7. If a conflict appears, call `agents-os-conflict-resolution`.

Do not create sibling notes that differ only by date, session, or wording.

## Example

Retrofit candidate:

```text
Raw session: 80-agents/journal/sessions/raw/YYYY-MM-DD-active-task-raw-session.md
Summary: 80-agents/journal/sessions/YYYY-MM-DD-active-task-summary.md
Entity: [[active-entity]]
```

Process:

1. Read the L1 summary first.
2. Confirm whether the raw session is a complete user transcript or only a
   placeholder.
3. Run the promotion test from `agents-os-memory-distillation`.
4. Reject progress-only facts as non-reusable.
5. Create L3 memory only when the candidate affects future behavior.
6. Recommend Graphify validation when indexable memory was created or changed.

Output:

```text
Raw sessions processed: 1
Artifacts created: none
Artifacts skipped: progress-only facts
Backfill source links:
  - [[YYYY-MM-DD-active-task-raw-session]]
Conflicts found: none
Graphify action: none, unless exclusion rules changed
```

## Output

```text
Raw sessions processed:
Artifacts created:
Artifacts skipped:
Backfill source links:
Conflicts found:
Graphify action:
```

## Hard Rules

- Do not load raw sessions opportunistically during normal work.
- Do not create duplicate memories already captured in L1/L3.
- Do not treat old raw content as fresher than newer canonical notes.
