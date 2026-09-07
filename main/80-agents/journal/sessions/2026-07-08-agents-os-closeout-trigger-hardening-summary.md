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
  - "[[2026-07-08-agents-os-closeout-trigger-hardening-raw]]"
  - "[[2026-07-08-agents-os-explicit-closeout-only]]"
  - "[[2026-07-08-agents-os-session-artifact-naming]]"
aliases: []
confidence: high
source_session: "[[2026-07-08-agents-os-closeout-trigger-hardening-raw]]"
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

# AGENTS OS closeout trigger hardening summary

## Objetivo

- Investigar por que agentes estaban creando artefactos de sesion con UUID/hash visible.
- Entregar un prompt maestro para regularizar los artefactos historicos.
- Corregir que agentes ejecutaran cierre completo antes de pedido explicito del usuario.
- Cerrar sesion solo despues del pedido explicito del usuario.

## Contexto cargado

- `80-agents/agents-os/agents-os.md`
- `80-agents/skills/agents-os-session-close/SKILL.md`
- `80-agents/skills/_shared/metadata-schema.md`
- `80-agents/skills/INDEX.md`
- `80-agents/skills/agents-os-behavior-config/SKILL.md`
- `80-agents/memory/public/constitution/agent-constitution.md`
- `80-agents/memory/public/user-preference/rjara-agent-profile.md`
- `80-agents/memory/internal/agent-memory/global/agents-os-operating-continuity.md`

## Trabajo realizado

- Diagnosticada causa de UUID/hash visible: faltaba regla dura de naming y algunos agentes copiaban `source_session` al filename/H1.
- Endurecida `agents-os-session-close`, `_shared/metadata-schema` y templates L0/L1 con naming `YYYY-MM-DD[-HHMM]-<human-topic>-raw|summary.md`.
- Detectados 26 artefactos historicos con UUID/hash visible y subdirectorios no canonicos de summaries.
- Entregado prompt maestro para una migracion historica link-safe.
- Diagnosticada causa de cierres automaticos: reglas contradictorias entre la skill, `skills/INDEX.md`, constitucion/proactividad y memoria interna.
- Persistida preferencia dura del usuario: cierre completo solo por pedido explicito.
- Agregado trigger guard a `agents-os-session-close` y corregido `skills/INDEX.md`.

## Artifacts creados o modificados

- Modificados:
  - `80-agents/agents-os/agents-os.md`
  - `80-agents/skills/agents-os-session-close/SKILL.md`
  - `80-agents/skills/_shared/metadata-schema.md`
  - `80-agents/skills/INDEX.md`
  - `80-agents/skills/agents-os-behavior-config/SKILL.md`
  - `80-agents/templates/raw-session.md`
  - `80-agents/templates/session-summary.md`
  - `80-agents/memory/public/constitution/agent-constitution.md`
  - `80-agents/memory/public/user-preference/rjara-agent-profile.md`
  - `80-agents/memory/internal/agent-memory/global/agents-os-operating-continuity.md`
- Creados:
  - `80-agents/journal/logs/2026-07-08-agents-os-session-artifact-naming.md`
  - `80-agents/journal/logs/2026-07-08-agents-os-explicit-closeout-only.md`
  - `80-agents/journal/sessions/raw/2026-07-08-agents-os-session-artifact-naming-hardening-raw.md`
  - `80-agents/journal/sessions/2026-07-08-agents-os-session-artifact-naming-hardening-summary.md`
  - `80-agents/journal/feedback/system-1/2026-07-08-agents-os-session-artifact-naming-hardening-session-feedback.md`
  - este cierre L0/L1/feedback.

## Memoria propuesta o creada

- No se creo L3 publica separada: las reglas operativas viven en las fuentes correctas (`agent-constitution`, `rjara-agent-profile`, skill de cierre y schema).
- Se actualizo memoria interna de continuidad para futuros agentes.

## Decisiones

- UUID/hash/conversation IDs quedan solo en metadata/evidencia, no en nombres visibles.
- Cierre completo L0/L1/feedback/distillation/reindex corre solo cuando el usuario lo pida explicitamente.
- Al terminar una tarea normal, el agente debe responder compacto; si necesita continuidad, puede tocar nota de proyecto o memoria interna, no crear cierre completo.

## Pendiente

- Regularizar historicos: 26 artefactos con UUID/hash visible y summaries bajo rutas no canonicas.
- Reindexar Graphify despues de la regularizacion o cuando convenga por los cambios indexables realizados.
