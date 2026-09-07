---
type: feedback
schema_version: 1
scope: session
created: 2026-08-21
updated: 2026-08-21
area: "[[Personal]]"
project: "[[AGENTS OS]]"
entities:
  - "[[AGENTS OS]]"
related: []
aliases: []
agent_surface: "[[ZCode]]"
agent_model: "builtin:zai-coding-plan/GLM-5.3"
agent_run:
session_goal: "Discovery/estado de echo + fix nativas + integración handoffs"
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

# Session Feedback — graphify-obsidian CLI sin comandos del contrato (filter/query --filter)

## Context

- Agent surface: [[ZCode]]
- Agent model: builtin:zai-coding-plan/GLM-5.3
- Agent run: [[2026-08-21-zcode-glm-5.3-echo-native-open-synthesis]]
- Session goal: discovery de echo, fix nativas, integración de handoffs históricos
- Main entity: [[Echo]] / [[Echo - Discovery y Estado]]
- Skills used: agents-os-bootstrap, agents-os-context-retrieval, agents-os-agent-project-workflow, agents-os-session-close
- Retrieval mode: Graphify (degradado) + fallback
- Artifacts changed: ver change logs 2026-08-20/21 de echo

## Friction (evento)

- El contrato (`80-agents/skills/_shared/graphify-contract.md`) y la skill de retrieval documentan `graphify-obsidian filter --filter K=V`, `--title`, `--alias` y `query --filter`, pero el binario instalado en `/usr/local/bin/graphify-obsidian` delega en `graphify` upstream que NO tiene el subcomando `filter` (`error: unknown command 'filter'`). El fork vault-aware documentado no está en el PATH de esta máquina (o se perdió en una actualización).
- Impacto: Layer 0 (selección por facetas) no disponible por CLI en sesiones de ZCode → retrieval degradado; se usó el fallback documentado (emulación sobre `95-graphify/obsidian/graph.json` con Python), que funcionó pero es más lento y no registra en el query-log del wrapper.

## Workaround

- Emulación de filter/query sobre `graph.json` (python) + `explain`/`path` del CLI cuando servían. Degradación reportada al usuario según contrato.

## Pain Pattern Candidate

- Contrato de Graphify vs binario instalado pueden divergir silenciosamente; no hay verificación de superficie (`graphify-obsidian --help` vs contrato) en el bootstrap. Un doctor/check barato del CLI evitaría descubrirlo en plena sesión.

## Suggested fix

- Restaurar/instalar el fork vault-aware con `filter`/`query --filter` en `/usr/local/bin/graphify-obsidian` (ver skill `agents-os-graphify-install`), o actualizar el contrato/skills para reflejar la emulación como camino oficial en esta máquina.
