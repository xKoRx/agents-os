---
type: change_log
scope: session
created: 2026-07-08
updated: 2026-07-08
area: "[[Personal]]"
project: "[[AGENTS OS]]"
entities:
  - "[[AGENTS OS]]"
related:
  - "[[agents-os-session-close]]"
aliases: []
confidence: verified
source_session:
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
  - area/personal
  - project/agents-os
  - change/updated
---

# AGENTS OS session artifact naming

## Cambio

- Endurecida `80-agents/skills/agents-os-session-close/SKILL.md` con regla
  obligatoria de nombres para L0/L1:
  `YYYY-MM-DD[-HHMM]-<human-topic>-raw.md` y
  `YYYY-MM-DD[-HHMM]-<human-topic>-summary.md`.
- Actualizado `80-agents/skills/_shared/metadata-schema.md` con regla
  compartida para journal artifacts.
- Agregada pista de filename en los templates `raw-session.md` y
  `session-summary.md`.

## Motivo

Se detectaron raw sessions y summaries con UUID completo o prefijos hash en el
filename. El contrato anterior solo indicaba ubicacion y tipo de artefacto, pero
no prohibia usar `source_session` como nombre visible.

## Validacion

- Busqueda enfocada encontro archivos historicos con nombres UUID puros y
  nombres contaminados con prefijos como `6c3cabba` o `241add91`.
- La nueva regla deja los IDs externos solo en metadata (`source_session`,
  `conversation_id`) o evidencia externa.
