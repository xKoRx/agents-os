---
type: feedback
schema_version: 1
scope: session
created: "2026-10-01"
updated: "2026-10-01"
area: "[[Echo]]"
project: "[[Echo Forge — Robust Run Selection V2]]"
entities:
  - "[[Echo Forge — Robust Run Selection V2]]"
  - "[[echo-forge]]"
related: []
aliases: []
agent_surface: "[[ZCode]]"
agent_model: GLM-5.3-Flash
agent_run: "[[2026-10-01-zcode-glm53-robust-v2-hera-e2e]]"
session_goal: "E2E full-flow de Robust Run Selection V2 por el flujo canónico de Echo Forge sobre datos reales de la flota (wave2b, FlowRun 0cbd0f34)"
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

# Session Feedback - 2026-10-01 - echo-forge robust-v2 hera-e2e

## Context

- Agent surface: [[ZCode]]
- Agent model: GLM-5.3-Flash
- Agent run: [[2026-10-01-zcode-glm53-robust-v2-hera-e2e]]
- Session goal: E2E full-flow V2 (wave2b) sobre la flota operacional; ~21h de corrida monitoreada.
- Main entity: [[Echo Forge — Robust Run Selection V2]]
- Skills usados: agents-os-bootstrap, forge-wave-dispatch (skill del repo), agents-os-agent-run-register, agents-os-session-feedback.
- Retrieval mode: Graphify no requerido; routing directo por paths canónicos del vault + Mongo/PG/ETCD/MinIO/Prometheus MCPs.
- Artifacts changed: ROBUST-V2-HERA-E2E.md/.csv, artifacts/hera-e2e-20261001/, agent-run, project note, release 0.2.131 (repo symphony).

## Scores

- Startup clarity: 5
- Retrieval usefulness: 4
- Skill fit: 5
- Template fit: 5
- Closeout friction: 4
- Overall confidence: 5

## What Complicated The Session Most

- Observation: ambos MCPs Mongo de Forge (`aranea-mongo-forge-ro/rw`) murieron a mitad de sesión con `session not found` en toda llamada (incluso `list-connections`); la evidencia V2 (aggregates con scope v2) vive en Mongo, así que el canal principal de verificación se cayó durante el E2E.
- Why it was hard: no hay señal de por qué la sesión murió ni cómo reconectarla; el `connect` del propio MCP también devolvía `session not found`.
- Proposed improvement: healthcheck/sesión-resiliente en el MCP Mongo (reconnect automático o error accionable); mientras tanto quedó validado el fallback (helper efímero read-only con `mongo.Connect` directo al `192.168.31.221:27017` del ETCD) — considerar documentarlo en [[aranea-mcps-expert]].

## Most Useful Part Of Sistema 1

- What helped: la skill `forge-wave-dispatch` versionada EN el repo (canal sin SSH certificado por Prometheus, identidad de wave quemada, advertencia watcher stale) + el historial de la nota de proyecto con los FlowRuns/precedentes de wave2a.
- Why it helped: permitió reconstruir el procedimiento completo de despacho/rollout/verificación sin SSH y sin re-descubrir trampas ya pagadas (screens viejas, cfgID, cohort_wave/cohort_flow_run).
- Keep/change: keep; el patrón "skill de operación vive en el repo owner" funciona mejor que en el vault para este dominio.

## Least Useful Or Noisy Part

- What did not help: el MCP Temporal sigue bound al namespace legacy `sqx` (no `sqx-prop`): las listas devuelven workflows de sept-23/24 y el describe del root de wave2b da `not found`.
- Why it was weak/noisy: parecería que la flota está muerta cuando no lo está (trampa ya documentada en la skill, pero el MCP sigue sin flag de namespace).
- Proposed cleanup: que el profile `aranea` del MCP Temporal exponga/rotee namespace o devuelva el namespace consultado en cada respuesta.

## Missing Support

- Problem not solved by Sistema 1: SSH kor@ roto 3/3 es fricción recurrente que fuerza canales indirectos (Prometheus) para preflights de host (GUI sqcli, CFX byte-exacto en host); el aranea-ssh MCP (echo-dev) no estaba disponible en esta superficie.
- How Sistema 1 could help next time: registrar en el entorno del proyecto qué superficies tienen aranea-ssh y cuál es el fallback exacto por canal.
- Suggested artifact type: runbook corto de verificación-sin-SSH ya existe en la skill del repo; falta el map "qué MCPs de observación tiene cada superficie ZCode".

## Retrieval Feedback

- Useful query or source: bitácora del proyecto [[Echo Forge — Operación Real V2]] (FlowRuns, releases, fallos típicos) + `sqx.configs`/ETCD `/sqx-worker/production/` para endpoints reales.
- Missing context: nada material; el freeze/certificación del proyecto Robust V2 dieron el SHA exacto.
- Duplicate/noisy result: no.
- Better future query: para waves, buscar primero en la bitácora del proyecto de operación, no en skills del vault.

## Skill Feedback

- Skill that worked well: forge-wave-dispatch (repo) — procedimiento exacto y vigente.
- Skill that was confusing: ninguna del vault en esta sesión.
- Trigger/routing gap: ZCode Skill tool no resuelve skills del INDEX del vault (limitación de superficie ya conocida; lectura directa de SKILL.md funcionó).
- Suggested contract change: ninguno.
