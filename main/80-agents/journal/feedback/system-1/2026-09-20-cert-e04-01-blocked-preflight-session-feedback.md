---
type: feedback
schema_version: 1
scope: session
created: 2026-09-20
updated: 2026-09-20
area: "[[Echo]]"
project: "[[Aranea]]"
entities:
  - "[[Aranea]]"
  - "[[Echo — E-04 Forge Ingestion E1]]"
related:
  - "[[AGENT-PLATFORM - MCP Access Plane]]"
aliases: []
agent_surface: "[[ZCode]]"
agent_model: GLM-5.3-Flash
agent_run: "[[2026-09-20-zcode-glm-5.3-flash-cert-e04-01-blocked-preflight]]"
session_goal: CERT-E04-01 (T21/AC-37) — preflight golden bytes + runtime Echo; veredicto BLOCKED sin POST
source_session: ZCode (daedalus, CERT-E04-01)
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

# Session Feedback - 2026-09-20 - cert-e04-01 blocked preflight

## Context

- Agent surface: ZCode (daedalus).
- Agent model: GLM-5.3-Flash.
- Agent run: [[2026-09-20-zcode-glm-5.3-flash-cert-e04-01-blocked-preflight]].
- Session goal: certificar ingestión Echo de un golden Forge auténtico; el gate cerró BLOCKED en preflight por dos bloqueantes de autoridad (bytes del golden y runtime Echo no desplegado).
- Main entity: [[Echo — E-04 Forge Ingestion E1]] / backlog de certificaciones.
- Skills used: bootstrap, aranea-agent-dev, session-close, agent-run-register (previo), e2e-gated-validation como marco de gates.
- Retrieval mode: Graphify no requerido; routing por INDEX + registry + lecturas dirigidas.
- Artifacts changed: backlog, nota E-04, agent-run, change_log, L0/L1, este feedback, workdir owner actions.

## Scores

- Startup clarity: 5
- Retrieval usefulness: 4
- Skill fit: 5
- Template fit: 4
- Closeout friction: 4
- Overall confidence: 5

## What Complicated The Session Most

- Observation: la brecha de identidad de lectura `sqx` sobre `trading_systems_test` bloquea por tercera sesión consecutiva la misma cadena de gates (C12/C13 → F04-02 → E04-01), y el Access Plane no tiene forma de expresar la necesidad hasta que una misión la documenta.
- Why it was hard: cada misión repite el diagnóstico desde cero porque la capacidad falta en el plano, no en el método; el costo se paga en sesiones enteras de preflight.
- Proposed improvement: registrar la necesidad como petición de capability formal en el Access Plane (fila nueva `sqx-ro` con objeto/filas exactos), no sólo en el workdir de cada misión.

## Most Useful Part Of Sistema 1

- What helped: el backlog de certificaciones como única fuente de verdad de la cadena F04/E04 (delta C13 + paquete G7 del corpus permitieron arrancar el mandato sin re-discovery).
- Why it helped: continuidad entre misiones sin repetir el trabajo físico ya hecho.
- Keep/change: mantener; los deltas por misión funcionan.

## Least Useful Or Noisy Part

- What did not help: el MCP SSH viewer niega compuestos con pipes y binarios de usuario (`go version -m`), dejando sin deployment-proof directo de binarios bajo `/home/kor`.
- Why it was weak/noisy: la política es correcta, pero no existe alternativa registrada para leer buildinfo de runtimes Echo PROD.
- Proposed cleanup: runbook de deployment-proof Echo (perfil con lectura de buildinfo o layout de releases con SHA256 legible por viewer).

## Missing Support

- Problem not solved by Sistema 1: no hay capability de lectura RO sobre PostgreSQL Forge (`trading_systems_test`) ni mecanismo de solicitud owner persistente en el plano.
- How Sistema 1 could help next time: capability `sqx-ro` temporal (proxy + bearer, patrón postgres-mcp) o canal owner documentado en el Access Plane.
- Suggested artifact type: fila nueva en [[AGENT-PLATFORM - MCP Access Plane]] + runbook asociado.

## Retrieval Feedback

- Useful query or source: lectura directa del paquete G7 (`HANDOFF-E04-PACKAGE.md`) y del Access Plane.
- Missing context: ninguna fuente decía explícitamente «Echo v3 nunca fue desplegado ni migrado a base compartida» — se demostró por probes en esta sesión.
- Duplicate/noisy result: los .tmp.* residuales en `10-projects/Echo/agentes/` ensucian listings.
- Better future query: «estado de despliegue runtime Echo v3» debería resolverse en una nota de entidad, no re-probarse.

## Skill Feedback

- Skill that worked well: bootstrap + domain router (routing limpio, sin scans).
- Skill that was confusing: ninguna.
- Trigger/routing gap: ninguno.
- Suggested contract change: ninguno.

## Template Feedback

- Template used: raw-session, session-summary, session-feedback, agent-run (previo).
- Field that helped: secciones fixas del L1 (Pendiente → next exact).
- Field that felt redundant: ninguna relevante.
- Missing field: en agent-run, un campo `blockers` explícito ayudaría a filtrar runs blocked sin leer el cuerpo.

## Memoria Interna (Internal Memory)

- ¿Consultaste la memoria interna al iniciar? sí (nota global de continuidad en cold start).
- ¿Qué valor operativo aportó? reglas de retry/identidad aplicadas al diseño fail-closed del preflight (no POST con resultado incierto; identidad desde autoridad canónica).
- ¿Dejaste algún mensaje para el próximo agente? el estado completo vive en entidades + memoria ZCode (`echo-cert-e04-01-state`); no se duplicó en memoria interna.
- Utilidad del espacio privado (1-5): 4.

## Pain Pattern Candidate

- Is this likely to repeat? yes
- Suggested severity: high
- Candidate owner: owner Aranea (capability `sqx-ro`) + owner Echo (deploy v3).
- Promote to L3 memory? defer (ya promovido de facto: delta del backlog + owner actions).

## One Next Improvement

- Registrar en el Access Plane la petición de capability `sqx-ro` sobre `trading_systems_test` con las 5 filas exactas, para que la siguiente sesión de CERT-E04-01 no repita el diagnóstico.
