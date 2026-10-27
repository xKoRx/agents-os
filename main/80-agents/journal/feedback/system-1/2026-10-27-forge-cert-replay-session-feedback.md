---
type: feedback
schema_version: 1
scope: session
created: 2026-10-27
updated: 2026-10-27
area: "[[Echo]]"
project: "[[Echo Forge — Operación Real V2]]"
entities:
  - "[[AGENTS OS]]"
related: []
aliases: []
agent_surface: "[[ZCode]]"
agent_model: GLM-5.3-Flash
agent_run: "[[2026-10-27-zcode-glm53-forge-cert-replay-blocked]]"
session_goal: certificación replay-based E2E de Echo Forge (ONE-SHOT owner)
source_session: ZCode CLI 2026-10-26/27
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

# Session Feedback - 2026-10-27 - short-topic

## Context

- Agent surface: [[ZCode]]
- Agent model: GLM-5.3-Flash
- Agent run: [[2026-10-27-zcode-glm53-forge-cert-replay-blocked]]
- Session goal: certificación replay-based E2E de Echo Forge (ONE-SHOT owner)
- Main entity: [[Echo Forge — Operación Real V2]]
- Skills used: agents-os-bootstrap, aranea-agent-dev (router), agentes-os-session-close/feedback, agent-run-register
- Retrieval mode: Graphify no requerido; focused search + fuentes canónicas (contrato ambiente, nota proyecto)
- Artifacts changed: nota proyecto (estado+bitácora), agent run, change log, memoria ZCode, paquete cert-replay en rama symphony

## Scores

- Startup clarity: 5
- Retrieval usefulness: 4
- Skill fit: 5
- Template fit: 4
- Closeout friction: 3
- Overall confidence: 4

## What Complicated The Session Most

- Observation: los MCPs del gateway Aranea (`aranea-ssh`, `aranea-mongo-forge`) expiraron a mitad de sesión ("Session not found or expired", 3+ reintentos) y bloquearon el acceso a worker-kronos y a Mongo directo; además la quota de subagentes mató al verificador adversarial dos veces.
- Why it was hard: sin worker-kronos la FASE H física completa es imposible (children MT5 sin poller); sin subagentes la verificación independiente quedó reducida a checks mecánicos del implementador con anclas independientes (oráculo §5.3, SHA256, commits).
- Proposed improvement: re-inicialización del gateway desde el cliente (o TTL más largo) y señalizar quota de subagentes antes de despachar (patrón burst ya conocido).

## Most Useful Part Of Sistema 1

- What helped: el contrato de ambientes Echo/Forge + la nota de proyecto con el historial completo permitieron resolver ambiente, authority y precedentes (w9/w11) sin re-investigar.
- Why it helped: una fuente canónica por hecho con estado operativo actualizado.
- Keep/change: mantener; la entrada nueva de estado ya enlaza el paquete y next exact.

## Least Useful Or Noisy Part

- What did not help: el namespace ETCD de `sqx-flowkit/production` apunta a `sqx-dev` (peculiaridad no documentada en el vault) — costó un ciclo de debug del helper temporal.
- Why it was weak/noisy: dato operacional vivo que vive sólo en ETCD.
- Proposed cleanup: documentar el quirk de flowkit en el wiki de dominio aranea (candidato a L3).

## Missing Support

- Problem not solved by Sistema 1: no existe runbook vigente de "flota física actual" (los hosts `sqx-ulab-*` ya no coinciden con la evidencia de sesiones previas; `/home/echo-dev` inaccesible para `kor`, sin workers visibles).
- How Sistema 1 could help next time: un inventario AS-BUILT corto de la flota (host→instalación SQX→datasets→licencia→worker) como recurso de dominio.
- Suggested artifact type: recurso wiki de dominio (30-resources/aranea) con last_verified.

## Retrieval Feedback

- Useful query or source: grep enfocado sobre `sqx/` + helpers RO propios (certread/certtemporal/certminio/certmongo) como superficie de evidencia.
- Missing context: nada adicional.
