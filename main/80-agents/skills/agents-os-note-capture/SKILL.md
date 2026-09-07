---
type: skill
schema_version: 1
name: agents-os-note-capture
scope: global
created: 2026-06-27
updated: 2026-08-10
description: Create or normalize vault notes without loading the whole vault. Use when the user asks to create a note, capture an idea, add meeting/action/tool/project/application/area documentation, choose or create the correct template, place a note in the right vault location, or convert loose content into a canonical Obsidian note while preserving AGENTS OS metadata, Graphify retrieval, aliases, and Sistema 1/Sistema 2 boundaries. For Sistema 2 real-entity documents, always use an existing template or create the missing template before creating the document.
load_policy: manual
indexable: true
index_priority: high
tags:
  - kind/skill
  - action/note-capture
  - tech/agents-os
  - scope/global
---

# AGENTS OS Note Capture

## Purpose

Create or normalize notes in the vault with the right location, template,
metadata, links, and retrieval behavior.

This skill is lazy-loaded by `agents-os-bootstrap`. Do not read it during
startup unless the task is about creating, capturing, importing, or normalizing
vault notes.

## Minimal Read

Canonical create: use `materialize_schema_note.py` per `note-types.md`; never hand-copy frontmatter.

Read only what the task needs:

1. `../_shared/note-types.md` to decide Sistema 1 vs Sistema 2 and apply the
   template policy.
2. After classification, read exactly one metadata authority:
   `90-system/convenciones.md` section "Schema de Sistema 2" for S2, or
   `../_shared/metadata-schema.md` for S1.
3. The exact mapping resolved programmatically by `materialize_schema_note.py`.
4. The target entity note only when linking to or updating an existing entity.

## Inputs

- User-provided content or source artifact.
- Intended note type, if the user names one.
- Candidate entity/project/area/application context.

## Procedure

1. Identify whether the note is Sistema 1 memory/journal, Sistema 2 real
   entity, or ordinary vault content.
2. Resolve the main entity to a canonical Obsidian title before writing.
3. Search filenames/frontmatter aliases/slugs and run a focused Graphify query
   before creating a new canonical note.
4. Choose location:
   - projects: `10-projects/`
   - areas: `20-areas/`
   - applications/resources: `30-resources/`
   - ordinary templates: `70-templates/`
   - AGENTS OS memory/journal: `80-agents/memory/` or `80-agents/journal/`
5. Resolve and materialize the exact contracted type with
   `materialize_schema_note.py`; direct template copies are invalid.
6. If a creable type lacks mapping/template, update contract+template in the
   same change and validate before materializing.
7. Derived/fragment artifacts follow only their explicit contract exemption.
8. Use canonical links in `area`, `project`, `application`, `entities`, and
   `related`. Put variants in `aliases`; put technical identifiers in `slug`
   and tags.
9. Keep capture factual. Put questions in a question/open section; do not
   promote hypotheses to current truth.
10. If the capture changes an existing canonical entity, call
   `agents-os-entity-update` and create a journal log.
11. Reindex Graphify when the new note should be retrievable.

## Output

```text
Created/updated note:
Type:
Canonical entity:
Template used:
Template created:
Links added:
Graphify status:
Follow-up:
```

## Hard Rules

- Do not create duplicate entity notes for casing, accents, aliases, old names,
  or repo slugs.
- Do not place session transcripts in normal notes; use
  `agents-os-session-close`.
- Do not create public memory unless the content passes L3 reuse rules.
- Do not leave a new note unlinked when a canonical entity is known.
- Do not use `status` in AGENTS OS memory notes.
- Do not create a Sistema 2 document without a template. If the template is
  missing, create it first or in the same change.
