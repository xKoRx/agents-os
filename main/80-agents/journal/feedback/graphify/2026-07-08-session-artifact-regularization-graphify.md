---
type: feedback
scope: graphify
created: 2026-07-08
updated: 2026-07-08
area: "[[Personal]]"
project: "[[AGENTS OS]]"
entities:
  - "[[AGENTS OS]]"
  - "[[graphify]]"
related:
  - "[[2026-07-08-agents-os-session-artifact-regularization-summary]]"
agent: Codex
source_session:
confidence: high
load_policy: manual
indexable: false
index_priority: low
tags:
  - kind/feedback
  - scope/graphify
  - project/agents-os
---

# Graphify Feedback - 2026-07-08 - Session Artifact Regularization

## Resultado

- `graphify-obsidian` no estaba en PATH de Codex, pero sí existía en `/Users/rjara/bin/graphify-obsidian`.
- Reindex ejecutado por ruta absoluta: `/Users/rjara/bin/graphify-obsidian update`.
- Resultado: 3662 nodes, 4244 edges, 328 communities.

## Dolor Repetible

- En entornos con PATH sanitizado, `command not found` puede inducir a reportar erróneamente que Graphify no está disponible.

## Ajuste Operativo

- Antes de declarar Graphify no disponible, probar rutas conocidas: `/Users/rjara/bin/graphify-obsidian` y `95-graphify/dist/graphify-obsidian`.
