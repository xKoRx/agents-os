---
type: skill
name: agents-os-vault-refactor
scope: global
created: 2026-06-27
updated: 2026-08-08
description: Plan and execute safe structural changes in the Obsidian vault. Use when the user asks to move notes, reorganize folders, rename many files, normalize templates, clean duplicate structures, migrate note classes, update backlinks after moves, or perform batch vault maintenance while preserving canonical entities, Graphify behavior, auditability, and AGENTS OS boundaries.
tags:
  - kind/skill
  - action/vault-refactor
  - tech/agents-os
---

# AGENTS OS Vault Refactor

## Purpose

Perform structural vault changes safely, with small batches, clear validation,
and rollback awareness.

This skill is lazy-loaded by `agents-os-bootstrap`. Use it for structural or
batch changes. Use narrower skills for single-note capture, entity lifecycle, or
relationship repair.

## Minimal Read

Read only:

1. `../_shared/metadata-schema.md`.
2. `../_shared/note-types.md`.
3. `../_shared/graphify-contract.md`.
4. The files directly affected by the proposed refactor.

## Procedure

1. State the refactor goal and scope in one sentence.
2. Build an inventory with focused search/Graphify, not a whole-vault read.
3. Classify each affected file:
   - Sistema 2 canonical entity;
   - Sistema 1 memory;
   - journal/log/raw session;
   - template;
   - ordinary vault note;
   - generated/archived output.
4. Exclude `40-archive/`, raw sessions, logs, generated Graphify output, and
   heavy artifacts unless the user explicitly includes them.
5. Prefer a small batch with explicit file list. Do not mix unrelated refactors.
6. Before moving or renaming, check backlinks, aliases, slugs, and Graphify
   expectations.
7. Apply edits/moves in the least disruptive way available on the surface.
8. Update internal links and routing metadata when a canonical path/title
   changes. Preserve aliases for old names.
9. Create journal logs for canonical entity changes, public-memory changes, or
   rule changes. Ordinary file moves may be summarized in the project bitacora
   if no canonical truth changed.
10. Reindex Graphify and validate at least one query for each affected entity
    class.

## Safety Gates

Ask before proceeding when the refactor would:

- delete files;
- rewrite many files at once;
- rename canonical entity titles;
- move public memory across scopes;
- touch archived historical material;
- affect files outside the configured vault root.

## Output

```text
Refactor goal:
Files changed:
Canonical entities affected:
Links/aliases updated:
Logs created:
Graphify validation:
Deferred follow-up:
```

## Hard Rules

- Do not use destructive commands without explicit user approval.
- Do not treat generated Graphify output as source of truth.
- Do not mix archive cleanup, entity rename, and memory migration in one hidden
  batch.
- Do not leave canonical links pointing to moved or merged identities.
