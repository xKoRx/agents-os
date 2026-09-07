---
type: skill
schema_version: 1
name: agents-os-entity-lifecycle
scope: global
created: 2026-08-07
updated: 2026-08-24
description: Manage the lifecycle of canonical Sistema 2 vault entities. Use when the user asks to create, rename, merge, split, archive, deprecate, restore, or classify projects, areas, applications, services, technologies, workflows, integrations, concepts, or other real entities in the Obsidian vault, while preserving canonical titles, aliases, slugs, backlinks, Graphify retrieval, templates, and audit logs. For new Sistema 2 documents, always use or create the matching template.
load_policy: manual
indexable: true
index_priority: high
tags:
  - kind/skill
  - scope/global
  - action/entity-lifecycle
  - tech/agents-os
---

# AGENTS OS Entity Lifecycle

## Purpose

Manage canonical Sistema 2 entities across their lifecycle without creating
identity drift.

This skill is lazy-loaded by `agents-os-bootstrap`. Use it for structural
entity operations, not for ordinary content edits. For narrow current-truth
updates to an already identified entity, use `agents-os-entity-update`.

## Minimal Read

Read:

1. `../_shared/note-types.md` for the S1/S2 boundary and template policy.
2. `../_shared/schema-contract.md` for the executable type/version/template
   contract; use `90-system/convenciones.md` only for human conventions.
3. The affected entity note(s).
4. `agents-os-relation-maintenance` only when backlinks or relationship fields
   need repair.

## Inputs

- Desired lifecycle operation: create, rename, merge, split, archive,
  deprecate, restore, or reclassify.
- Evidence: user statement, existing notes, repo/path, Graphify result, or
  external source.
- Candidate canonical title and aliases.

## Procedure

1. Define the operation and affected entity class: project, area, application, service, technology, workflow, integration, concept, or tool. For a project, classify whether it is a development delivery because it changes executable code, configuration, schemas, or infrastructure.
2. Search by filename, title, aliases, slug, repo URL, local path, and focused
   Graphify query before creating or renaming anything.
3. Pick one canonical title. Treat aliases and slugs as routing aids only.
4. For creation:
   - choose the correct folder;
   - materialize the type with
     `python3 80-agents/skills/_shared/scripts/materialize_schema_note.py <type> <vault-relative-target.md>`;
   - reject the creation if the type is unknown, exempt/non-creatable, the
     template is absent, or the contract validator is red;
   - fill the materialized canonical template and preserve its current
     `schema_version`;
   - if a creable type lacks mapping/template, update the contract and create
     the template before or alongside the new Sistema 2 document;
   - set frontmatter with canonical routing links;
   - add aliases for user variants, old names, repo slugs, and common casing;
   - add `slug` only in the entity's own note.
   - for every project, keep `## 🧱 Entrega de desarrollo`; if the project is a development delivery, fill one row per repo/branch with its base, functional SPEC, technical SPEC and status before implementation starts; otherwise record `No aplica` with a reason.
5. For rename:
   - preserve old title as an alias;
   - update inbound links only when the tool surface can do it safely;
   - otherwise record exact follow-up links to fix.
6. For merge:
   - choose the surviving canonical entity;
   - move useful current truth into the survivor;
   - convert duplicate identity into alias or archive, not a second live entity.
7. For split:
   - create separate canonical entities only when they represent different real
     responsibilities;
   - document rationale and update relationship fields.
8. For archive/deprecation:
   - avoid deleting useful history;
   - mark the live canonical target or replacement clearly;
   - keep retrieval from preferring obsolete identity.
9. Create a `type: change_log` in `80-agents/journal/logs/` for every canonical
   entity lifecycle change.
10. Reindex Graphify and validate a query by canonical title and one alias.

## Gates determinísticos (schema S1/S2)

`../_shared/schema-contract.md` es la autoridad exacta. `../_shared/scripts/validate_schema_contract.py` valida versión, cobertura type→template, fronteras, campos declarados, tags, secciones, derivados, fragmentos, fixtures y configuración del lint. `scripts/lint.py` consume el mismo contrato y nunca modifica el vault.

- `python3 80-agents/skills/_shared/scripts/validate_schema_contract.py` —
  gate de contrato/templates; exit 1 ante drift.
- `python3 80-agents/skills/_shared/scripts/resolve_schema_type.py <type>` —
  resuelve template/versión o rechaza la creación.
- `python3 80-agents/skills/_shared/scripts/materialize_schema_note.py <type> <target>` —
  crea sin overwrite desde el mapping validado; es la única ruta de creación
  canónica.

- `python3 scripts/lint.py --check` — reporte completo; exit 1 si hay ERROR.
- `python3 scripts/lint.py --strict <path...>` — valida notas nuevas/modificadas contra la versión actual y exige cero findings; no usa Git.
- `python3 scripts/lint.py --gate` — compara el corpus con el baseline contratado; mientras contiene deuda heredada bloquea fingerprints nuevos, y con baseline vacío funciona como gate estricto all-vault porque cualquier finding bloquea.
- `python3 scripts/lint.py --emit-baseline` — imprime a stdout un candidato determinístico; nunca escribe el baseline.
- `python3 scripts/lint.py --check <path>` — lint puntual que bypassa exclusiones para pilotos y fixtures.

Tras crear/renombrar/reclasificar una entidad, correr `--check` sobre la nota y
confirmar 0 ERROR antes de cerrar. Fixtures de contrato en `scripts/fixtures/`.

## Output

```text
Operation:
Canonical entity:
Affected notes:
Aliases/slugs:
Relations updated:
Journal log:
Graphify validation:
Residual risk:
```

## Hard Rules

- Do not create a new entity until duplicate search has been performed.
- Do not remove aliases that explain historical or external names.
- Do not silently delete entity notes; archive or merge with a log.
- Do not rename an entity only to match a slug or repo casing.
- Do not mix Sistema 1 memory into the canonical entity body.
- Do not create a Sistema 2 entity document without a matching template.
- Do not start implementation from a development project whose `## 🧱 Entrega de desarrollo` lacks either SPEC or an explicit branch and base for every affected repo.
- Do not create or modify a versioned note with an unsupported or missing
  `schema_version`; legacy notes are read-only until explicitly migrated.
