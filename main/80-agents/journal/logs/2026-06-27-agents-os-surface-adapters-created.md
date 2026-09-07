---
type: change_log
scope: project
created: "2026-06-27"
updated: "2026-06-27"
area: "[[Personal]]"
project: "[[AGENTS OS]]"
application:
entities:
  - "[[AGENTS OS]]"
related:
  - "[[agents-os]]"
aliases:
  - AGENTS OS surface adapters created
confidence: verified
source_session:
load_policy: manual
indexable: false
index_priority: never
tags:
  - area/personal
  - kind/changelog
  - project/agents-os
  - project/agentsos
  - scope/project
  - tech/agentsos
---
# 2026-06-27 AGENTS OS Surface Adapters Created

## Cambio

- **Tipo:** created / updated
- **Archivo(s):**
  - `80-agents/adapters/README.md`
  - `80-agents/adapters/codex.md`
  - `80-agents/adapters/claude.md`
  - `80-agents/adapters/cursor.md`
  - `80-agents/adapters/antigravity.md`
  - `80-agents/skills/_shared/skill-contract.md`
  - `10-projects/AGENTS OS.md`
  - `80-agents/agents-os/agents-os.md`
  - `80-agents/agents-os/00-onboarding-ia.md`
  - `80-agents/agents-os/05-preguntas-abiertas.md`
  - `80-agents/agents-os/07-skills-y-tareas.md`

## Motivo

- El proyecto queria operar desde Codex, Claude, Cursor y Antigravity, pero la validacion beta y los pendientes solo mencionaban Codex, Claude y Antigravity.
- Existian `agents/openai.yaml` por skill, pero no una capa explicita de adaptadores por superficie.

## Fuentes usadas

- `10-projects/AGENTS OS.md`
- `80-agents/agents-os/00-onboarding-ia.md`
- `80-agents/agents-os/05-preguntas-abiertas.md`
- `80-agents/skills/_shared/skill-contract.md`
- `80-agents/skills/_shared/graphify-contract.md`

## Resolución aplicada

- Se creo `80-agents/adapters/` con adaptadores para Codex, Claude, Cursor y Antigravity.
- Se actualizo el contrato de skills para distinguir `SKILL.md` canonico de adaptadores por superficie.
- Se reconciliaron los documentos de estado para incluir Cursor en la beta y dejar claro que los adaptadores no sustituyen forward-tests reales.
- Se corrigio `progress` del proyecto de `0` a `70` para reflejar el avance real sin declarar beta lista.

## Validación

- Pendiente de validar en sesiones reales con Claude, Cursor y Antigravity.
- Codex queda parcialmente validado; el gap principal sigue siendo `agents-os-session-close` con transcript real.
