---
type: feedback
schema_version: 1
scope: session
created: "2026-09-08"
updated: "2026-09-08"
area: "[[Echo]]"
project: "[[Echo — E-01 Canonical SDK Foundation S0]]"
entities:
  - "[[Echo — Live Platform V1]]"
related: []
aliases: []
agent_surface: "[[ZCode]]"
agent_model: GLM-5.3-Flash
agent_run: "[[2026-09-08-zcode-glm-5.3-flash-echo-e01-contracts-s0]]"
session_goal: "Corrección acotada: rechazar UTF-8 inválido en echo-wire-json.v1 (Canonicalize/Validate)"
source_session:
confidence: high
load_policy: manual
indexable: false
index_priority: low
tags:
  - kind/feedback
  - scope/session
  - project/echo
  - agent/system1
---

# Session Feedback - 2026-09-08 - echo e01 s0 utf8 correction

## Context

- Agent surface: [[ZCode]] · model GLM-5.3-Flash (host). Run base de la fase: [[2026-09-08-zcode-glm-5.3-flash-echo-e01-contracts-s0]].
- Session goal: corrección acotada de 4 archivos wire + tests + gates + push.
- Main entity: [[Echo — E-01 Canonical SDK Foundation S0]]
- Skills used: agents-os-session-close; agents-os-session-feedback (pedido explícito).
- Retrieval mode: warm turn, sin retrieval nuevo.
- Artifacts changed: 4 archivos `v3/sdk/contracts/wire/**` en repo; subproyecto E-01 y change_log en vault; esta nota.

## Scores

- Startup clarity: 5
- Retrieval usefulness: 5
- Skill fit: 5
- Template fit: 4
- Closeout friction: 4
- Overall confidence: 5

## What Complicated The Session Most

- Observation: al escribir tests con bytes inválidos vía heredoc bash + python, un literal `\x00` quedó crudo en el source Go ("illegal character"), exigiendo un fix extra del bloque.
- Why it was hard: doble capa de escaping (bash heredoc → python string → Go source) para bytes no-UTF8 en literales.
- Proposed improvement: para fixtures con bytes inválidos, preferir escritura directa del archivo Go (Write tool) en vez de heredoc+replace, o construir los bytes en runtime (`[]byte{0xff,0xfe}`) en lugar de literales de source.

## Most Useful Part Of Sistema 1

- El gate "no bajar coverage existente" detectó de inmediato el costo de las ramas nuevas; los tests del requisito cubrieron las ramas añadidas sin rondas extra.
