---
type: feedback
schema_version: 1
scope: session
created: 2026-08-24
updated: 2026-08-24
area: "[[Personal]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
entities:
  - "[[AGENTS OS]]"
related: []
aliases: []
agent_surface: "[[Codex]]"
agent_model: unknown
agent_run: "[[2026-08-24-codex-unknown-durable-strategy-identity-v2-builder-conflict-audit]]"
session_goal: "Auditar Builder contract_conflict y ejecutar E2E con request_id nuevo"
source_session: DURABLE-STRATEGY-IDENTITY-V2-BUILDER-CONTRACT-CONFLICT-REQUEST-ID-NEW-NORMAL
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

# Session Feedback - 2026-08-24 - durable-strategy-identity-v2-builder-conflict

## Context

- Agent surface: [[Codex]]
- Agent model: unknown
- Agent run: [[2026-08-24-codex-unknown-durable-strategy-identity-v2-builder-conflict-audit]]
- Session goal: Builder RCA and fresh release 0.2.68 E2E
- Main entity: [[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]
- Skills used: [[sqx-deployer]], Agents OS bootstrap/session close
- Retrieval mode: cold bootstrap plus targeted continuity
- Artifacts changed: request input and closeout notes; no code

## Scores

Use 1-5, where 1 is poor and 5 is excellent.

- Startup clarity: 5
- Retrieval usefulness: 5
- Skill fit: 4
- Template fit: 4
- Closeout friction: 3
- Overall confidence: 4

## What Complicated The Session Most

- Observation: The fresh run passed Builder but failed later at Final Reretester, requiring a second RCA classification.
- Why it was hard: Durable SQL and Mongo evidence showed successful stage completion while Temporal failed on an activity result-shape contract.
- Proposed improvement: Add a machine-readable final activity contract assertion and surface its exact failing key/artifact in worker logs.

## Most Useful Part Of Sistema 1

- What helped: Existing continuity memory and the targeted durable identity notes.
- Why it helped: They preserved the prior FlowRun, StageExecution and legacy request evidence without broad vault loading.
- Keep/change: Keep targeted bootstrap; add a standard read-only Temporal failure extractor.

## Least Useful Or Noisy Part

- What did not help: Local screen logs were verbose and some remote hosts lacked `rg`.
- Why it was weak/noisy: Correlation required switching between SQL, Mongo, SSH and Temporal history.
- Proposed cleanup: Prefer POSIX-compatible remote commands in the operational skill.

## Missing Support

- Problem not solved by Sistema 1: No canonical query/runbook yet for summarizing one FlowRun across SQL, Mongo and Temporal.
- How Sistema 1 could help next time: Provide a read-only cross-store evidence checklist.
- Suggested artifact type: Runbook, after the RCA contracts stabilize.

## Retrieval Feedback

- Useful query or source: Prior continuity note plus StageExecution and Temporal history queries.
- Missing context: Final Reretester output contract was not described in the startup context.
- Duplicate/noisy result: Full stage/evidence dumps were larger than needed after counts were known.
- Better future query: Start with grouped stage counts and only expand the failing StageExecution.

## Skill Feedback

- Skill that worked well: sqx-deployer for release/process verification.
- Skill that was confusing: None material.
- Trigger/routing gap: A full-E2E request can encounter a distinct downstream contract after Builder passes.
- Suggested contract change: Include downstream output-shape probes in the certification workflow.

## Template Feedback

- Template used: session-feedback.md.
- Field that helped: Retrieval and Missing Support sections.
- Field that felt redundant: Repeated surface/model fields already present in the agent run.
- Missing field: Explicit “blocked by downstream contract” classification.

## Memoria Interna (Internal Memory)

- ¿Consultaste la memoria interna (`80-agents/memory/internal/`) al iniciar? sí
- ¿Qué valor operativo aportó para esta sesión (continuidad, detalles crudos, advertencias)? Conservó la evidencia de la corrida legacy y el bloqueo previo.
- ¿Dejaste algún mensaje, instrucción o hipótesis para el próximo agente en la memoria interna? La continuidad de esta sesión se conserva en el change log y known-errors.
- ¿Qué tan útil te resulta tener este espacio privado fuera de la vista directa del usuario (1-5) y cómo podemos mejorar su utilidad? 5; mantenerlo compacto y con IDs operativos.

## Pain Pattern Candidate

- Is this likely to repeat? yes
- Suggested severity: high
- Candidate owner: Symphony durable workflow maintainers
- Promote to L3 memory? yes

## One Next Improvement

- Agregar un extractor read-only de `WorkflowExecutionFailed` que imprima actividad, StageExecutionRef, input/output refs y colecciones faltantes.
