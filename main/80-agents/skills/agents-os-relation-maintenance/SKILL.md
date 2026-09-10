---
type: skill
name: agents-os-relation-maintenance
scope: global
created: 2026-06-27
updated: 2026-08-08
index_priority: high
indexable: true
load_policy: manual
schema_version: 1
description: Maintain relationships between vault notes and entities. Use when the user asks to add, repair, audit, validate, or explain links, backlinks, aliases, related fields, entity relationships, project/application/area connections, orphan notes, duplicate relationships, Graphify paths, or relationship maps in the Obsidian vault.
aliases:
  - agents-os-relation-maintenance
tags:
  - kind/skill
  - action/relation-maintenance
  - tech/agents-os
  - scope/global
---

# AGENTS OS Relation Maintenance

## Purpose

Keep relationships between notes explicit, canonical, and recoverable through
Graphify without turning every connection into noisy metadata.

This skill is lazy-loaded by `agents-os-bootstrap`. Use it when the task is
about links, backlinks, related fields, relationship maps, or retrieval paths.

## Minimal Read

Read:

1. `../_shared/metadata-schema.md` for canonical link fields.
2. The source and target notes being linked.
3. `../_shared/graphify-contract.md` when validating paths or retrieval.

## Relationship Model

- `area`, `project`, `application`: primary routing links.
- `entities`: real-world entities the note is about.
- `related`: supporting notes, memory, decisions, logs, or secondary links.
- Body links: human-readable navigation and context.
- Tags/slugs: automation and filtering, not replacements for canonical links.

## Procedure

1. Identify the relationship question: create, repair, audit, explain, or prune.
2. Resolve each endpoint to its canonical Obsidian title.
3. Use Graphify `path` or focused `query` before broad folder scans.
4. Open source Markdown for every relationship that will be changed.
5. Decide the lightest representation:
   - frontmatter routing field for primary ownership or retrieval;
   - body link for visible navigation or explanatory context;
   - `related` for supporting notes and memory artifacts;
   - tag only for filtering or task systems.
6. Add reciprocal links only when both notes benefit from navigation. Avoid
   forced symmetry.
7. Remove or replace links that point to aliases, obsolete duplicates, archived
   drafts, raw sessions, or logs unless the historical link is intentional.
8. If a relationship change alters canonical entity truth, call
   `agents-os-entity-update` and create a journal log.
9. Reindex Graphify and validate the expected query/path.

## Output

```text
Relationship task:
Source notes:
Target notes:
Changes applied:
Graphify/path validation:
Unresolved links:
Follow-up:
```

## Hard Rules

- Do not link to aliases when the canonical title is known.
- Do not over-link every mention; link relationships that aid navigation,
  retrieval, ownership, or audit.
- Do not use tags as the only representation of an important entity relation.
- Do not add raw sessions, logs, or archived drafts to normal retrieval paths.
