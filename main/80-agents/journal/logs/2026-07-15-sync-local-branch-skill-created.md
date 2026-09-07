---
type: change_log
scope: global
created: 2026-07-15
updated: 2026-07-15
share_scope: local
project: "[[AGENTS OS]]"
entities:
  - "[[AGENTS OS]]"
related:
  - "[[sync-local-branch]]"
aliases: []
confidence: verified
source_session:
source_feedbacks: []
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/global
  - project/agentsos
  - change/created
---

# Skill de sincronización local de ramas

## Cambio

- Se creó `80-agents/skills/sync-local-branch/SKILL.md` con flujo parametrizado para sincronizar una rama local con otra.
- Incluye precondiciones, comandos permitidos, resolución conservadora de conflictos, commit `merge <base>` y push sin reescritura.

## Motivo

- Repetir de forma segura el comportamiento solicitado para `develop`, `master` o cualquier rama base local explícita.

## Validación

- Scaffold generado con `skill-creator` y completado contra `80-agents/templates/skill.md` y `_shared/skill-contract.md`.
- Validación estructural manual ejecutada contra el contrato AGENTS OS; el `quick_validate.py` genérico de Codex no acepta los campos `type`/`tags` requeridos por AGENTS OS.
- Forward-test de precondiciones: detectó correctamente que `develop` no existe localmente y bloqueó la sincronización.
