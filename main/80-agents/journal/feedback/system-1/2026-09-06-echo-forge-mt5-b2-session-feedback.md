---
type: feedback
schema_version: 1
scope: session
created: 2026-09-06
updated: 2026-09-06
area: "[[Echo]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
entities:
  - "[[Echo Forge]]"
related:
  - "[[2026-09-06-zcode-glm-5.3-flash-echo-forge-mt5-b2]]"
aliases: []
agent_surface: "[[ZCode]]"
agent_model: GLM-5.3-Flash
agent_run: "[[2026-09-06-zcode-glm-5.3-flash-echo-forge-mt5-b2]]"
session_goal: ECHO-FORGE-MT5-CANCEL-CAUSE-JOB-LIFETIME-SINGLETON-DRAIN-V2-NORMAL-B2
source_session: ECHO-FORGE-MT5-CANCEL-CAUSE-JOB-LIFETIME-SINGLETON-DRAIN-V2-NORMAL-B2
confidence: high
load_policy: manual
indexable: false
index_priority: low
tags:
  - kind/feedback
  - scope/session
  - project/agentsos
  - agent/system1
---

# Session Feedback - 2026-09-06 - mt5-b2

## Context

- Agent surface: [[ZCode]]
- Agent model: GLM-5.3-Flash
- Agent run: [[2026-09-06-zcode-glm-5.3-flash-echo-forge-mt5-b2]]
- Session goal: ECHO-FORGE-MT5-CANCEL-CAUSE-JOB-LIFETIME-SINGLETON-DRAIN-V2-NORMAL-B2
- Main entity: [[Echo Forge]]
- Skills used: Agents OS bootstrap, project workflow, session close, agent-run register.
- Retrieval mode: canonical vault notes + source del repo y del SDK en module cache.

## Friction

- `registry-postgres`/migrations fallan a nivel máquina por SysV shm agotado (`shmget: No space left on device`) en macOS; obliga a clasificar siempre contra worktree del baseline para no atribuir el fallo al delta. Workaround aplicado y documentado; candidato a known-error ambiental si reaparece.
- La testsuite de activities del SDK no permite inyectar una cause de cancelación al contexto de una activity real (`GetInfo` panica fuera de activity), lo que limita los tests de entry point artifact a nivel coordinador + helper compartido.

## What worked

- Leer el source efectivo del SDK (v1.44.1 en module cache) antes de diseñar: el clasificador congelado D1 coincide con el discriminador interno `isActivityCanceled` y la conversión a `RespondActivityTaskCanceled` quedó probada por evidencia, no por supuesto.

## Pain Pattern Candidate

- Ninguno nuevo; se reconfirma que las suites ambientales (postgres embebido, `sqx/tools`) exigen diff contra baseline en worktree eférico como paso estándar de toda misión NORMAL.
