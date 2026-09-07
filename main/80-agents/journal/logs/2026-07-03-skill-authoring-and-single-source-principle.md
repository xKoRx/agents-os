---
type: change_log
scope: global
created: 2026-07-03
area: "[[Personal]]"
project: "[[AGENTS OS]]"
entities:
  - "[[AGENTS OS]]"
related:
  - "[[agent-constitution]]"
  - "[[context-router]]"
tags:
  - kind/changelog
  - area/personal
  - project/agents-os
---

# 2026-07-03 — Principio "una fuente por hecho" + skill de autoría de skills

## Motivo
Generalizar el aprendizaje del Context Router (separar comportamiento agent-facing de la
explicación humana) a todo el sistema, sin caer en duplicación/drift. El owner lo evangelizará.

## Cambios
- **Constitución (`updated` → 2026-07-03):** nueva Regla Base **"Una fuente canónica por hecho;
  comportamiento en skills, explicación en docs"** — el procedimiento vive en su skill (agente,
  mínimo, sin rationale); la explicación rica en su doc humano que **enlaza**, no repite.
- **`_shared/skill-contract.md`:** nueva sección **"Audience Split"** — SKILL.md es agent-facing
  (imperativo, cero prosa de rationale); la explicación humana va en doc aparte que enlaza.
- **Nueva skill `agents-os-skill-authoring`:** procedure lean para crear/refinar skills; referencia
  `note-types.md` + `skill-contract.md` + template (NO los duplica). Registrada en `skills/INDEX.md`.

## Decisión de diseño (anti-drift)
- No se duplicó ninguna regla: la skill de autoría **referencia** las fuentes canónicas.
- El principio global vive en la **constitución**; su aplicación específica a skills, en el **contrato**.

## Validación
- Constitución, contrato, skill e índice actualizados de forma cruzada y sin repetición.
