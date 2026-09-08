---
type: feedback
schema_version: 1
scope: session
created: "2026-09-08"
updated: "2026-09-08"
area: "[[Echo]]"
project: "[[Echo Forge — Factory V2 Completion]]"
entities:
  - "[[Echo Forge]]"
  - "[[Echo Forge — F-03 SQX long-running]]"
related:
  - "[[Echo Forge — F-03 SQX Long-Running Contract]]"
aliases: []
agent_surface: "[[Cursor]]"
agent_model: Cursor Grok 4.6
agent_run:
session_goal: "TOP F-03 SQX long-running: SPEC/TASKS canónicas, sin source"
source_session: ECHO-FORGE-F03-SQX-LONG-RUNNING-TOP
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

# Session Feedback - 2026-09-08 - echo-forge-f03-top

## Context

- Agent surface: [[Cursor]]
- Agent model: Cursor Grok 4.6
- Agent run: omitido (SPEC/Agents OS, sin source Symphony)
- Session goal: TOP F-03; elapsed ≠ failure; no copiar MT5
- Main entity: [[Echo Forge — F-03 SQX long-running]]
- Skills used: bootstrap, context-retrieval, entity-lifecycle materialize, implementation-planning validate, resource-wiki ingest, session-close
- Retrieval mode: graphify-personal en Symphony; `graphify-obsidian` hung >50s y se mató; glob/read vault
- Artifacts changed: SPEC F-03, subproyecto, Factory V2 delta, change_log, este feedback

## Scores

- Startup clarity: 4
- Retrieval usefulness: 4
- Skill fit: 4
- Template fit: 4
- Closeout friction: 3
- Overall confidence: 4

## What Complicated The Session Most

- Observation: vault local sin `.git`; `graphify-obsidian filter` se colgó >50s y hubo que kill; el prompt exige SHA de Agents OS.
- Why it was hard: no hay remoto de vault en este workstation; el lookup de authority queda degraded y hay que citar journal, no inventar SHA.
- Proposed improvement: bootstrap debe decir: si `VAULT_ROOT` no tiene `.git`, no fetch, documentar degraded y usar último SHA durable del journal (mismo gap que F-02).

## Most Useful Part Of Sistema 1

- What helped: patrón F-02 (Resource SPEC + hijo `owner:agent`) y [[2026-09-06-echo-forge-mt5-execution-model-v2]] como principio compartido sin copiar slots.
- Why it helped: evitó meter SPEC en `symphony/specs/` y evitó rediseñar B2.
- Keep/change: keep.

## Least Useful Or Noisy Part

- What did not help: queries graphify genéricas (`Builder`, `Activity`) anclaron en exporter Java y specs MT5, no en ActivityOptions.
- Why it was weak/noisy: vocabulario colisiona con pipeline Builder vs SQX Builder.
- Proposed cleanup: query `genericActivityOptions HeartbeatTimeout StartToCloseTimeout`.

## Missing Support

- Problem not solved by Sistema 1: no hay receta “SHA Agents OS cuando el vault no es git”.
- How Sistema 1 could help next time: una línea en bootstrap o learning corto (ya propuesta en feedback F-02; sigue abierta).
- Suggested artifact type: learning (defer; no duplicar si F-02 ya lo pidió).

## Retrieval Feedback

- Useful query or source: `genericActivityOptions`; `WFMDurableExportActivity` 10m; `classifyError` Canceled; child `WorkflowRunTimeout` 30d.
- Missing context: SHA live de Agents OS.
- Duplicate/noisy result: graphify BFS `WithTimeout` devolvió ~750 nodos de tests.
- Better future query: `genericActivityOptions StartToCloseTimeout ScheduleToCloseTimeout`.

## Skill Feedback

- Skill that worked well: `materialize_schema_note.py` + patrón F-02.
- Skill that was confusing: `graphify-obsidian` vs `graphify-personal` (código vs vault) en el mismo cold start.
- Trigger/routing gap: pedido explícito de session-close+feedback cubre sampling.
- Suggested contract change: none.

## Template Feedback

- Template used: resource + project + change_log + session-feedback
- Field that helped: `sources` del resource y `parent` del proyecto
- Field that felt redundant: Ideas/backlog vacío
- Missing field: none

## Memoria Interna (Internal Memory)

- ¿Consultaste la memoria interna (`80-agents/memory/internal/`) al iniciar? sí (operating-continuity always-load)
- ¿Qué valor operativo aportó para esta sesión (continuidad, detalles crudos, advertencias)? no repetir efectos laterales; no inventar SHA
- ¿Dejaste algún mensaje, instrucción o hipótesis para el próximo agente en la memoria interna? no (sin delta durable de continuidad global)
- ¿Qué tan útil te resulta tener este espacio privado fuera de la vista directa del usuario (1-5) y cómo podemos mejorar su utilidad? 4 — el checkpoint global compacto basta en cold start

## Pain Pattern Candidate

- Is this likely to repeat? yes
- Suggested severity: medium
- Candidate owner: Agents OS bootstrap
- Promote to L3 memory? defer (ya señalado en F-02)

## One Next Improvement

Documentar en bootstrap: vault sin `.git` → degraded SHA lookup; citar journal; no inventar.
