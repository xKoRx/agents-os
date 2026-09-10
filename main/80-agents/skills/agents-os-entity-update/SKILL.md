---
type: skill
schema_version: 1
name: agents-os-entity-update
scope: global
created: 2026-06-27
updated: 2026-08-10
description: Propose safe updates to Sistema 2 canonical entity notes. Use when a session changes what is currently true about a project, application, service, workflow, technology, integration, or concept, or when Sistema 1 memory artifacts must be linked back to canonical documentation without mixing history into the entity. For newly created or substantially repaired Sistema 2 documents, require the matching template or create it first.
aliases:
  - agents-os-entity-update
load_policy: manual
indexable: true
index_priority: high
tags:
  - kind/skill
  - action/entity-update
  - tech/agents-os
  - scope/global
---

# Agent Memory System Entity Update

## Purpose

Keep Sistema 2 accurate while preserving the boundary between canonical
documentation and Sistema 1 agent memory.

## Minimal Read

Canonical create: use `materialize_schema_note.py` per `note-types.md`; never hand-copy frontmatter.

Read `../_shared/note-types.md` for the Sistema 1/Sistema 2 boundary and
template policy. Read `90-system/convenciones.md` section "Schema de Sistema
2" if entity frontmatter changes are needed. Read
`../_shared/metadata-schema.md` only when creating or modifying a linked
Sistema 1 artifact.

## Procedure

1. Identify the affected entity note.
2. Decide whether the new information changes current truth or only adds memory.
3. If current truth changes, apply a focused edit directly.
4. Link related L3 artifacts under existing sections or a compact related-memory block.
5. Preserve stable entity responsibilities, integrations, aliases, repo/path metadata.
6. Record the change in `80-agents/journal/logs/`.
7. If contradiction appears, call `agents-os-conflict-resolution` and log the resolution.

## Canonical Sections

Use the note's existing shape first. Do not restructure an entity just to match
this list. Create a Sistema 2 note only through `materialize_schema_note.py`.
If no mapping exists, update contract+template first. A substantial repair
migrates the existing note explicitly instead of replacing it. Prefer these
minimal sections by entity type.

Application notes:

- `## 📝 Descripción`: what the app is responsible for now.
- `## 🔧 Datos útiles`: repo, local path, stack, main commands, docs.
- `## ✅ Tareas relacionadas`: task query or explicit active task links.
- `## 🔗 Links`: repo, docs, dashboards, runbooks, related apps.
- Optional `## 🧠 Memoria relacionada`: compact links to L3 memory when the
  note already has enough related memory to justify a section.

Project notes:

- `## 🎯 Objetivo`: current outcome the project is trying to achieve.
- `## 📊 Estado actual`: current facts, phase, blockers, and latest stable
  progress.
- `## ✅ Tareas`: source task block or task query.
- `## 📆 Bitácora`: short factual timeline, not a raw session.
- `## 🧭 Decisiones`: stable decisions or links to ADR/L3 decision notes.
- `## 🔗 Docs / Links`: PRDs, repos, docs, artifacts.
- `## 💡 Ideas`: non-canonical ideas that are not yet decisions/tasks.

Area notes:

- `## 🎯 Objetivo`: enduring standard or purpose for the area.
- `## 📊 Estado actual`: current situation at area level.
- `## 🟢 Proyectos de esta área`: project rollup.
- `## 📚 Recursos de esta área`: resource rollup.
- `## ✅ Tareas abiertas`: area task query.
- `## 🧭 Decisiones relevantes`: stable area decisions.
- `## 🔗 Links`: dashboards, references, external docs.

Concept/workflow/service notes should use the same principle:

- identity and current truth first;
- useful operational data second;
- related tasks/links/memory last.

## Direct Edit Policy

Apply direct edits in the MVP when all are true:

- The affected Sistema 2 note is clearly identified.
- The new claim is current truth, not session progress.
- The source is explicit: user statement, repository file, official doc,
  successful command, existing memory, or a clearly named artifact.
- The edit is narrow and preserves existing frontmatter, aliases, repo/path
  metadata, task blocks, and human-facing layout.
- A `type: change_log` note is created in `80-agents/journal/logs/`.

Do not directly edit when:

- the entity identity is ambiguous;
- the source only supports a hypothesis;
- the change would rewrite large sections;
- the correct canonical target is unclear;
- the claim belongs in L3 memory rather than current entity truth.

When direct edit is blocked, create a proposal in the closeout or hygiene report
instead of silently inventing the canonical fact.

## Journal Log Requirements

Every direct update to Sistema 2 must create a log under:

```text
80-agents/journal/logs/YYYY-MM-DD-<entity-slug>-entity-updated.md
```

The log must include:

- changed entity path;
- old statement, when there was one;
- new statement;
- source/evidence;
- reason it is Sistema 2 current truth and not Sistema 1 memory;
- related memory links, if any;
- validation performed or validation gap.

Materialize `type: change_log` with `materialize_schema_note.py` and set:

```yaml
type: change_log
scope: session
indexable: false
index_priority: never
load_policy: manual
```

## Naming And Alias Rules

Canonical title:

- Prefer the human/project name already used in Obsidian and use it as the
  exact wikilink target everywhere.
- For applications, prefer the repo slug without organization prefix when that
  is how humans refer to it, e.g. `<application-slug>`.
- Keep platform prefixes such as `fury_` as aliases unless the prefix is the
  human-facing name.
- Do not create a second note or link target only for casing, accent removal,
  singular/plural, or English/Spanish variants.

Aliases:

- Include repo slugs, old names, common abbreviations, and external system names
  when they help retrieval.
- Include common casing/accent variants when users or tools may type them, e.g.
  `meli`, `MELI`, `Mercado Libre` for `[[Meli]]`.
- Do not make a new note just because a repo slug differs from the human name.
- Before creating an entity, search by filename, title, aliases, repo URL, and
  local path.
- If two notes share an alias, treat it as a hygiene finding or conflict unless
  one note is clearly obsolete.

Slugs and routing fields:

- Use `slug:` in the entity's own note for the technical identifier.
- Use routing fields such as `area:`, `project:`, `application:`, `entities:`
  and `related:` as canonical Obsidian links.
- For example, area entity `20-areas/Meli.md` uses `slug: meli`; project and
  memory notes refer to it with `area: "[[Meli]]"` and `#area/meli`.
- Tags and semantic paths use lowercase/kebab-case slugs and do not replace
  canonical links.

Repo/path mismatches:

- If frontmatter `github` or `path` disagrees with the body, update both in one
  focused edit and log the change.
- If a repo moved but the entity remains the same application, update the
  existing note; do not create a replacement entity.
- If the same repo now represents a different product/service, create or update
  the correct entity and log the split/rationale.

## Examples

### Application Update

Input: repository metadata shows an application stack changed and the app note
has outdated stack information.

Action:

- Edit `30-resources/applications/<application-slug>.md` under `## 🔧 Datos útiles`.
- Preserve aliases used by humans, repositories, or external systems.
- Create `80-agents/journal/logs/YYYY-MM-DD-<application-slug>-entity-updated.md`.

Output:

```text
Entity: [[active-application]]
Applied change: stack/current command metadata updated.
Reason/source: repository build file.
Journal log: <path>
Needs user validation: no, if evidence is direct.
```

### Project Update

Input: an active project control note now has a validation milestone completed.

Action:

- Update the active project roadmap/checklist and bitacora.
- Do not copy the full validation report into the project note.
- Link the report or memory only if it helps future navigation.

Output:

```text
Entity: [[active-project]]
Applied change: validation milestone marked complete.
Reason/source: completed check and report.
Journal log: optional unless this is treated as a canonical Sistema 2 change.
Needs user validation: no.
```

### Concept Update

Input: a stable definition of the live Graphify output path emerges.

Action:

- If a concept note exists, update its current definition.
- If no concept note exists and the knowledge is operational/repeatable, prefer
  L3 `known_error` or `runbook` instead of creating a concept note.
- Log any Sistema 2 concept edit.

Output:

```text
Entity: Graphify concept candidate
Applied change: none to Sistema 2; created L3 known_error instead.
Reason/source: operational validation issue, not broad concept truth.
Journal log: public-memory creation log.
Needs user validation: no.
```

## Output

```text
Entity:
Current canonical statement:
Applied change:
Reason/source:
Related memory links:
Journal log:
Risk:
Needs user validation:
```

## Hard Rules

- Do not turn entity notes into session diaries.
- Do not overwrite canonical facts without source, rationale, and journal log.
- Do not create a duplicate entity if an existing Sistema 2 note can be linked.
