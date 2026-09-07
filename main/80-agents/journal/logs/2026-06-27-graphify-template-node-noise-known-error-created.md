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
  - "[[graphify-template-node-noise]]"
  - "[[agents-os-context-retrieval]]"
aliases:
  - graphify template node noise known error created
confidence: high
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
# Graphify Template Node Noise Known Error Created

## Cambio

- **Tipo:** created
- **Archivo(s):**
  - `80-agents/memory/public/known-error/agents-os/graphify-template-node-noise.md`
  - `80-agents/skills/_shared/graphify-contract.md`
  - `80-agents/skills/agents-os-context-retrieval/SKILL.md`

## Motivo

- Se observo que queries genericas de Graphify pueden rankear templates por encima de memoria viva, lo que puede inducir malas conclusiones de retrieval.

## Fuentes usadas

- Salida de `graphify-obsidian query 'AGENTS OS known_error graphify template noisy retrieval' --budget 1200`.
- Salida de `graphify-obsidian query 'AGENTS OS context retrieval template transcript pendiente' --budget 1200`.
- Contrato existente de Graphify y skill de context retrieval.

## Resolución aplicada

- Se creo known error publico con sintoma, causa, impacto, deteccion y mitigacion.
- Se agrego manejo explicito de noisy queries al contrato Graphify.
- Se agrego seccion `Noisy Query Handling` a `agents-os-context-retrieval`.

## Validación

- Reindex ejecutado con `graphify-obsidian update`: `95-graphify/obsidian/GRAPH_REPORT.md` quedo fresco con 893 nodos y 800 edges.
- `graphify-obsidian explain "Graphify Template Node Noise"` encontro la memoria publica nueva.
- Una query amplia por `AGENTS OS known_error graphify template node noise` siguio anclando en nodos genericos (`Graphify`), lo que confirma el sintoma y la necesidad de validar por titulo/fuente cuando hay ruido.
