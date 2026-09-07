---
type: session
scope: session
created: "2026-07-08"
updated: "2026-07-08"
area: "[[Personal]]"
project: "[[AGENTS OS]]"
application:
entities:
  - "[[AGENTS OS]]"
related:
  - "[[2026-07-08-agents-os-session-artifact-naming-hardening-raw]]"
  - "[[2026-07-08-agents-os-session-artifact-naming]]"
aliases: []
confidence: high
source_session: "[[2026-07-08-agents-os-session-artifact-naming-hardening-raw]]"
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/session
  - scope/session
  - area/personal
  - project/agents-os
---

%% Filename: YYYY-MM-DD[-HHMM]-<human-topic>-summary.md. Never use UUIDs/hashes as visible names; put external IDs in source_session. %%

# AGENTS OS session artifact naming hardening summary

## Objetivo

- Revisar por que aparecieron archivos de sesiones con UUID/hash visible.
- Endurecer AGENTS OS para evitar que vuelva a pasar.
- Entregar un prompt maestro para regularizar los artefactos historicos restantes.

## Contexto cargado

- `80-agents/agents-os/agents-os.md`
- `80-agents/skills/agents-os-session-close/SKILL.md`
- `80-agents/skills/_shared/metadata-schema.md`
- `80-agents/templates/raw-session.md`
- `80-agents/templates/session-summary.md`
- `80-agents/memory/public/constitution/agent-constitution.md`
- `80-agents/memory/public/user-preference/rjara-agent-profile.md`
- `80-agents/memory/internal/agent-memory/global/agents-os-operating-continuity.md`

## Trabajo realizado

- Diagnosticada la causa: el cierre exigia crear artefactos L0/L1, pero no prohibia usar `source_session` como filename/H1.
- Detectados 26 artefactos historicos con UUID/hash visible en `80-agents/journal/sessions/`.
- Detectada deriva estructural adicional: subdirectorios `summaries/`, `summary/` y `system-1/` bajo `80-agents/journal/sessions/`.
- Endurecida la skill de cierre con regla obligatoria `YYYY-MM-DD[-HHMM]-<human-topic>-raw.md` y `...-summary.md`.
- Agregada regla compartida de journal artifact names al schema.
- Agregadas pistas de filename a los templates L0/L1.
- Creado log auditable del cambio.

## Artifacts creados o modificados

- Modificados:
  - `80-agents/skills/agents-os-session-close/SKILL.md`
  - `80-agents/skills/_shared/metadata-schema.md`
  - `80-agents/templates/raw-session.md`
  - `80-agents/templates/session-summary.md`
  - `80-agents/memory/internal/agent-memory/global/agents-os-operating-continuity.md`
- Creados:
  - `80-agents/journal/logs/2026-07-08-agents-os-session-artifact-naming.md`
  - `80-agents/journal/sessions/raw/2026-07-08-agents-os-session-artifact-naming-hardening-raw.md`
  - `80-agents/journal/sessions/2026-07-08-agents-os-session-artifact-naming-hardening-summary.md`
  - `80-agents/journal/feedback/system-1/2026-07-08-agents-os-session-artifact-naming-hardening-session-feedback.md`

## Memoria propuesta o creada

- No se creo L3 publica separada: la regla operativa vive en la skill y el schema, que son la fuente correcta para este comportamiento.
- Se actualizo memoria interna de continuidad para alertar a futuros agentes.

## Decisiones

- UUID/hash/conversation IDs quedan permitidos solo como metadata (`source_session`, `conversation_id`) o evidencia externa.
- No se renombraron archivos historicos en esta sesion para evitar romper links/frontmatter sin una migracion controlada.

## Pendiente

- Ejecutar una regularizacion historica: renombrar archivos afectados, actualizar wikilinks/frontmatter y consolidar summaries fuera de ubicacion canonica.
- Reindexar Graphify despues de la regularizacion.
