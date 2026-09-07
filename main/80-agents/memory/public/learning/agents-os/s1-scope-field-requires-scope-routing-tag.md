---
type: learning
schema_version: 1
scope: project
created: "2026-08-19"
updated: "2026-08-19"
area: "[[Personal]]"
project: "[[AGENTS OS]]"
entities:
  - "[[AGENTS OS]]"
  - "[[Graphify]]"
related:
  - "[[lint-explicit-paths-bypass-corpus-exclusions]]"
aliases:
  - scope field requires scope tag
  - missing-tag scope/application gate
  - lint routing tag scope
confidence: verified
source_session:
load_policy: when_project_loaded
indexable: true
index_priority: high
tags:
  - kind/learning
  - scope/project
  - tech/agents-os
  - tech/graphify
---

# s1-scope-field-requires-scope-routing-tag

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Aprendizaje

- El gate del reindex de Graphify (`graphify-obsidian update`) corre el lint estricto S1/S2 y **bloquea con deuda nueva** (`NO-GO` si `new>0` vs baseline).
- Regla clave S1: si una nota tiene el campo `scope: <x>`, **debe** existir el tag de ruteo espejo `scope/<x>` en `tags:` (p.ej. `scope: application` ⇒ `scope/application`; `scope: project` ⇒ `scope/project`). Faltarlo produce `ERROR [missing-tag] … requires routing tag 'scope/<x>'`.
- Un tag `scope/<appname>` (p.ej. `scope/symphony`) **no** cuenta: el valor debe ser el del campo `scope` (global/user/area/project/application/service/tool/technology/integration/workflow/session/graphify), no el nombre de la app.
- El material de referencia de una skill (`skills/*/references/*.md`) no lleva frontmatter canónico: se **excluye por ruta exacta** en `.graphifyignore` (precedente: `phase-plan-contract.md`), no se le inventa un `type`.

## Aplicabilidad

- **Cuándo cargarlo:** al crear/editar notas S1 (`known_error`, `learning`, `runbook`, etc.) o antes de correr el reindex, para no romper el gate por `missing-tag`, `bad-status`, `empty-field` o `missing-section`.
- **Cuándo no cargarlo:** trabajo que no toca frontmatter del vault ni el índice de Graphify.

## Entidades relacionadas

- [[AGENTS OS]] · [[Graphify]] — gate de lint del reindex.

## Evidencia

%% Cita de fuente, NO prosa narrativa: link a sesión/log/archivo + una línea de qué la respalda. No re-parafrasear el aprendizaje ya destilado arriba (constitución: memorias compactas). %%

- Fuente: `80-agents/skills/agents-os-entity-lifecycle/scripts/lint.py` (`validate_tags`) — implementa `scope: <x>` ⇒ tag requerido `scope/<x>`. Sesión 2026-08-19: se cerraron 19 ERROR + 2 WARN y el gate pasó a `GO new=0`.
