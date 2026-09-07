---
type: change_log
schema_version: 1
scope: session
created: "2026-08-19"
updated: "2026-08-19"
area: "[[Personal]]"
project: "[[AGENTS OS]]"
application:
entities:
  - "[[AGENTS OS]]"
  - "[[Graphify]]"
related:
  - "[[s1-scope-field-requires-scope-routing-tag]]"
aliases: []
confidence: verified
source_session:
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-08-19-graphify-lint-gate-frontmatter-debt-cleared

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated (+ created 1 learning)
- **Archivo(s):** 21 findings del gate de lint del reindex (19 ERROR + 2 WARN) → 0/0.
  - 13 notas S1: agregado tag de ruteo `scope/<scope>` faltante (11 `scope/application`, 2 `scope/project`); en 2 se reemplazó tag `scope/<appname>` erróneo por `scope/application`.
  - [[Echo Forge - Etapa 6]]: `status: done` → `completed` (valor inválido para `project`).
  - `30-resources/storage/echo-go-workspace.md`: `aliases` vacío → 3 aliases.
  - `Diagrama visual — Entidades y persistencia de Echo Forge.md` (`doc`): agregadas secciones `## Propósito` y `## Contenido`.
  - [[signals-spec-authoring]] SKILL: headers `## Para Qué Sirve`/`## Procedimiento` → canónicos `## Purpose`/`## Procedure`.
  - `.graphifyignore`: excluidas las 2 referencias de la skill signals (patrón `phase-plan-contract.md`).
  - Nueva learning: [[s1-scope-field-requires-scope-routing-tag]].

## Motivo

- El reindex bloqueaba (`NO-GO`) por deuda nueva de frontmatter fuera del baseline (baseline vacío ⇒ cualquier finding es nuevo).

## Fuentes usadas

- `80-agents/skills/agents-os-entity-lifecycle/scripts/lint.py`, `80-agents/skills/_shared/schema-contract.md`.

## Resolución aplicada

- Fix por tipo de finding (missing-tag / bad-status / empty-field / missing-section / no-frontmatter) alineado al contrato de schema.

## Validación

- `lint.py --check` → `ERROR=0 WARN=0`. `graphify-obsidian update` → `GO: no-new-debt new=0`; índice reconstruido (5830 nodos / 7104 edges).

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales sensibles, memoria interna ni secretos

## Rollback

- Revertir los headers/tags/status editados y quitar las 3 líneas nuevas de `.graphifyignore`; borrar la learning y este log. Ninguna nota canónica fue sobrescrita en su contenido. 
