---
type: change_log
scope: session
created: 2026-06-27
updated: 2026-06-27
area: "[[Personal]]"
project: "[[AGENTS OS]]"
application:
entities:
  - "[[AGENTS OS]]"
related:
  - "[[agents-os]]"
  - "[[00-onboarding-ia]]"
  - "[[03-flujos]]"
  - "[[05-preguntas-abiertas]]"
aliases:
  - agents os doc state drift updated
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
  - scope/session
---
# AGENTS OS Doc State Drift Updated

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `80-agents/agents-os/00-onboarding-ia.md`
  - `80-agents/agents-os/agents-os.md`
  - `80-agents/agents-os/03-flujos.md`
  - `80-agents/agents-os/05-preguntas-abiertas.md`
  - `10-projects/AGENTS OS.md`

## Motivo

- Los documentos de onboarding/diseno todavia describian la Capa 2 como no implementada o pendiente, mientras el documento de control y las skills locales ya registraban estructura beta, memoria always-load, higiene, retrofit, behavior config y ADR publica.
- La deriva podia hacer que un agente fresco eligiera tareas ya cerradas o cargara contexto innecesario.

## Fuentes usadas

- `10-projects/AGENTS OS.md`
- `80-agents/skills/agents-os-*.md`
- `80-agents/memory/public/decision/agents-os/public-vs-internal-memory.md`
- `80-agents/memory/internal/agent-memory/global/agents-os-operating-continuity.md`

## Resolución aplicada

- Se actualizo el estado de onboarding e indice de diseno para reflejar beta operativa en hardening.
- Se movieron a "decidido" preguntas ya cerradas por skills o validaciones previas.
- Se alinearon riesgos/tareas del documento de control con el estado real.
- Se mantuvo como pendiente el forward-test de `agents-os-session-close` con transcript real y la beta end-to-end.

## Validación

- Cambios acotados a documentacion canonica y control del proyecto.
- No se ejecuto cierre de sesion por directiva explicita del usuario.
