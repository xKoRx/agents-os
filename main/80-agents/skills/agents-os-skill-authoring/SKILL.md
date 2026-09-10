---
type: skill
schema_version: 1
name: agents-os-skill-authoring
scope: global
created: 2026-07-03
updated: 2026-08-10
description: Author or refine an AGENTS OS skill so it follows the skill contract and the token-economy principles. Use when creating a new skill, refactoring an existing one, or deciding whether something should be a skill, a runbook, or a memory. Enforces lean agent-facing SKILL.md, single-source-per-fact, and separation of executable behavior from rich human explanation.
aliases:
  - agents-os-skill-authoring
load_policy: manual
indexable: true
index_priority: high
tags:
  - kind/skill
  - action/skill-authoring
  - tech/agents-os
  - scope/global
---

# AGENTS OS Skill Authoring

## Purpose

Producir/refinar una skill bien formada: comportamiento ejecutable, mínimo en tokens,
sin duplicar reglas que ya viven en otro lado.

Lazy-load. Invocar solo al crear/refinar skills o clasificar un artefacto nuevo.

## Minimal Read

Canonical create: use `materialize_schema_note.py` per `note-types.md`; never hand-copy frontmatter.

1. `../_shared/note-types.md` — decidir skill vs runbook vs memoria.
2. `../_shared/skill-contract.md` — folder shape, token budget, secciones, audience split, checklist.
3. `../../templates/skill.md` — plantilla base.

No repetir aquí el contenido de esos archivos: son la fuente canónica; esta skill los aplica.

## Procedure

1. **Clasificar** el artefacto con `note-types.md`: ¿skill (cómo repetible), runbook
   (secuencia mecánica con validación/rollback) o memoria (qué/por qué)? Si no es skill, parar
   y usar el flujo correcto (runbook → `memory/public/runbook/`; memoria → `agents-os-memory-distillation`).
2. **Materializar `type: skill` con `materialize_schema_note.py`** y completar
   `name`/`description` gatillables y tags correctos.
3. **Mantener el SKILL.md agent-facing y lean** (contrato): procedure, hard rules, output. **Sin rationale ni "por qué importa".** Cada línea cambia una decisión.
4. **Separar la explicación rica** (por qué/valor/evangelización) en un doc humano aparte que
   **enlaza** a la skill; no restatear. Una fuente por hecho (regla de constitución).
5. **Enlazar skills/runbooks/contratos relacionados** en vez de copiar su contenido.
6. Pasar el **Draft→Ready checklist** de `skill-contract.md`.
7. Registrar `type: change_log` en `journal/logs/` (obligatorio para skills, por constitución).

## Output

```text
Artefacto:            skill | runbook | memoria  (justificar clasificación)
Skill creada/refinada:
Reglas referenciadas: (note-types / skill-contract / template)
Doc humano aparte:    sí (link) | no aplica
Checklist Draft→Ready: pasa | faltan: ...
Change log:           ruta
```

## Hard Rules

- No mezclar skill + runbook + memoria en una nota (constitución).
- No duplicar reglas ya canónicas: referenciar `note-types.md` / `skill-contract.md`.
- SKILL.md no lleva prosa de rationale; eso va en un doc humano que enlaza.
- Toda skill creada/refinada/deprecada deja `change_log`.
