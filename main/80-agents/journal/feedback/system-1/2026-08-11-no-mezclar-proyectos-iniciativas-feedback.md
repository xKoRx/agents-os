---
type: feedback
schema_version: 1
scope: session
created: 2026-08-11
updated: 2026-08-11
area: "[[Personal]]"
project: "[[AGENTS OS]]"
entities:
  - "[[AGENTS OS]]"
related:
  - "[[Onboarding Signals]]"
  - "[[Crear Context]]"
  - "[[rjara-agent-profile]]"
aliases:
  - no mezclar proyectos ni iniciativas
agent: claude-opus-4-8
session_goal: Discovery del flujo actual (contrato de componente) para Signals
source_session:
confidence: high
load_policy: manual
indexable: false
index_priority: low
tags:
  - kind/feedback
  - scope/session
  - project/agents-os
  - agent/system1
---

# Session Feedback - 2026-08-11 - no mezclar proyectos ni iniciativas

## Context

- Agent: claude-opus-4-8
- Session goal: entender el flujo actual del contrato de componente en RIO
- Main entity: [[Onboarding Signals]] / [[Crear Context]]
- Artifacts changed: notas de proyecto [[Crear Context]] y [[Onboarding Signals]]

## What Complicated The Session Most

- **Observación:** metí el discovery/comprensión del flujo actual (as-is + dolor) dentro del proyecto de **cambio** ([[Crear Context]]), cuando pertenece al proyecto de **comprensión** ([[Onboarding Signals]]).
- **Por qué estuvo mal:** confundí dos tipos de iniciativa. Onboarding = entender el sistema (research); Crear Context = meter un cambio (delivery). No se puede iniciar/lidera un cambio antes de completar el entendimiento, y el entendimiento no es contenido del proyecto de cambio.
- **Corrección durable:** directiva `[DURA]` "No mezclar proyectos ni iniciativas" agregada a [[rjara-agent-profile]]. El discovery vive en el proyecto de comprensión; el de cambio solo referencia y arranca cuando el entendimiento está completo. Ante duda de pertenencia, preguntar.

## Pain Pattern Candidate

- Is this likely to repeat? yes (riesgo alto al arrancar proyectos derivados)
- Suggested severity: high
- Promote to L3 memory? done (directiva global en el perfil)

## One Next Improvement

- Al crear un proyecto derivado, clasificar explícitamente su tipo (comprensión vs cambio) y sus dependencias antes de escribir contenido en él.
