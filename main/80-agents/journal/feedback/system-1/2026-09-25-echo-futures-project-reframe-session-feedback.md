---
type: feedback
scope: session
created: 2026-09-25
updated: 2026-09-25
area: "[[Echo]]"
project: "[[Echo Futures]]"
entities:
  - "[[Echo Futures]]"
  - "[[Echo Futures — Prop Economics Experiment]]"
related: []
aliases: []
agent_surface: ChatGPT
session_goal: Reframe Echo Futures as a new product project and prepare D1 analysis
confidence: high
load_policy: manual
indexable: false
index_priority: low
tags:
  - agent/system1
  - area/echo
  - kind/feedback
  - project/echo-futures
  - scope/session
---

# Session Feedback — 2026-09-25 — Echo Futures project reframe

## What worked

- Separar el experimento económico terminado del nuevo proyecto canónico evitó convertir hipótesis/simulaciones previas en arquitectura por accidente.
- Mantener un `Critical Design Register` con requisitos, propuestas y preguntas abiertas hizo visible qué debe probar D1/D2 antes del freeze.
- Asignar un `owner_day` obligatorio a cada pregunta elimina el patrón de arrastrar TBDs hasta desarrollo.

## Friction

- Las skills canónicas `technical-project-manager` y `agents-os-session-close` existen en Agents-OS, pero no aparecieron en el registro de skills expuesto por la herramienta de esta sesión; hubo que descubrirlas leyendo `80-agents/skills/INDEX.md` y cargarlas directamente desde el repo.
- Esto añade pasos y puede hacer que un agente no use una skill crítica aunque esté correctamente registrada en Agents-OS.

## Improvement candidate

- **tooling/skill-discovery:** cuando una skill no aparezca en el registry runtime, el bootstrap de Agents-OS debería hacer fallback explícito al INDEX canónico antes de concluir que no existe.
- Severidad: medium.
- Evidencia: cierre y handoff D1 de Echo Futures 2026-09-25.
