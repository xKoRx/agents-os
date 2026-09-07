---
type: feedback
schema_version: 1
scope: session
created: 2026-08-27
updated: 2026-08-27
area: "[[Personal]]"
project: "[[Echo Forge]]"
entities:
  - "[[AGENTS OS]]"
related: []
aliases: []
agent_surface: "[[Codex]]"
agent_model: unknown
agent_run: "[[2026-08-27-codex-unknown-sqx-cross-flowrun-historical-source-resolution-e2e-normal]]"
session_goal: SQX-CROSS-FLOWRUN-HISTORICAL-SOURCE-RESOLUTION-E2E-NORMAL
source_session: SQX-CROSS-FLOWRUN-HISTORICAL-SOURCE-RESOLUTION-E2E-NORMAL
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

# Session Feedback - 2026-08-27 - SQX historical source runtime

## Context

- Agent surface: [[Codex]]
- Agent model: unknown
- Agent run: [[2026-08-27-codex-unknown-sqx-cross-flowrun-historical-source-resolution-e2e-normal]]
- Session goal: Runtime E2E de reuse histórico cross-FlowRun.
- Main entity: [[Echo Forge]]
- Skills used: [[agents-os-bootstrap]], [[agents-os-session-close]], [[agents-os-agent-run-register]]
- Retrieval mode: bootstrap cold start + targeted repo/runtime evidence.
- Artifacts changed: no product code; deploy/intake runtime artifacts preserved.

## Scores

Use 1-5, where 1 is poor and 5 is excellent.

- Startup clarity:
- Retrieval usefulness:
- Skill fit:
- Template fit:
- Closeout friction:
- Overall confidence:

## What Complicated The Session Most

- Observation: La primera publicación manual falló por ejecutar helpers Bash desde zsh; además, el primer harness temporal decodificó mal el wrapper de respuesta Activity.
- Why it was hard: La activación debe probarse físicamente en hosts y el contrato de evidencia cruza Temporal, PG, Mongo y MinIO.
- Proposed improvement: Encapsular la publicación y auditoría en entrypoints con shell explícito y un decoder común del envelope de Activity.

## Most Useful Part Of Sistema 1

- What helped: Bootstrap y contexto interno del proyecto, más la evidencia durable de Temporal/PG/Mongo.
- Why it helped: Permitió continuar desde el checkpoint exacto y distinguir harness issues de defectos de producto.
- Keep/change: Keep.

## Least Useful Or Noisy Part

- What did not help: Procesos watcher duplicados preexistentes produjeron eventos secundarios de archivos ya movidos.
- Why it was weak/noisy: Añadió ruido a logs de intake aunque el evento primario creó B/C correctamente.
- Proposed cleanup: Runbook de auditoría que identifique y reporte watchers duplicados sin modificar procesos durante certificaciones.

## Missing Support

- Problem not solved by Sistema 1: No hay un wrapper local único para release publication + fleet activation + Temporal reconciliation.
- How Sistema 1 could help next time: Registrar los cuatro gates de release y los IDs de FlowRun en un artefacto de evidencia compacto.
- Suggested artifact type: runbook.

## Retrieval Feedback

- Useful query or source: Checkpoint de Echo Forge y consultas read-only targeted a Temporal/PG/Mongo/MinIO.
- Missing context: Decoder exacto del envelope de Activity.
- Duplicate/noisy result: salida de watcher secundario por archivos procesados.
- Better future query: Resolver primero el contrato de Activity y enumerar pollers antes de interpretar logs.

## Skill Feedback

- Skill that worked well: agents-os-bootstrap.
- Skill that was confusing: ninguno relevante.
- Trigger/routing gap: ninguno.
- Suggested contract change: none.

## Template Feedback

- Template used: session-feedback.md.
- Field that helped: artifacts changed.
- Field that felt redundant: scores para una certificación runtime.
- Missing field: runtime evidence references.

## Memoria Interna (Internal Memory)

- ¿Consultaste la memoria interna (`80-agents/memory/internal/`) al iniciar? sí
- ¿Qué valor operativo aportó para esta sesión (continuidad, detalles crudos, advertencias)? checkpoint del commit exacto y del siguiente E2E.
- ¿Dejaste algún mensaje, instrucción o hipótesis para el próximo agente en la memoria interna? no; el handoff queda en la respuesta y el agent_run.
- ¿Qué tan útil te resulta tener este espacio privado fuera de la vista directa del usuario (1-5) y cómo podemos mejorar su utilidad? 5; conservar checkpoints con IDs operativos.

## Pain Pattern Candidate

- Is this likely to repeat? yes
- Suggested severity: medium
- Candidate owner: runtime certification tooling
- Promote to L3 memory? defer

## One Next Improvement

- Añadir un comando de auditoría read-only que emita release, pollers, resolver envelope, children y ownership en un formato único.
