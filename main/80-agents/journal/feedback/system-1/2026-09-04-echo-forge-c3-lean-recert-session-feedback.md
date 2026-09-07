---
type: feedback
schema_version: 1
scope: session
created: "2026-09-04"
updated: "2026-09-04"
area: "[[Echo Forge]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
entities:
  - "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
related:
  - "[[2026-09-04-echo-forge-c3-lean-recert-blocked]]"
  - "[[2026-09-04-forge-campaign-orchestration-contract-broken]]"
aliases: []
agent_surface: "[[ZCode]]"
agent_model: GLM-5.3-Flash
agent_run: "[[2026-09-04-zcode-glm-5-3-echo-forge-c3-lean-recert]]"
session_goal: certificación física LEAN C3 (CERT-A/CERT-B) sin mutación de source
source_session: ECHO-FORGE-C3-LEAN-RECERT-NORMAL
confidence: high
load_policy: manual
indexable: false
index_priority: low
tags:
  - kind/feedback
  - scope/session
  - project/echo-forge
  - agent/system1
---

# Session Feedback - 2026-09-04 - echo-forge-c3-lean-recert

## Context

- Agent surface: [[ZCode]]
- Agent model: GLM-5.3-Flash
- Agent run: [[2026-09-04-zcode-glm-5-3-echo-forge-c3-lean-recert]]
- Session goal: certificación física LEAN C3 (CERT-A/CERT-B) read-only sobre source
- Main entity: [[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]
- Skills used: agents-os-bootstrap, agents-os-session-close; runbooks symphony-prod-probe / workers-shared-access / worker-runtime-proof
- Retrieval mode: Graphify no requerido; búsqueda enfocada + checkpoint del proyecto + known-errors
- Artifacts changed: decisión + known-error + feedback + agent_run + change log + checkpoint del proyecto + continuidad interna; cero cambios en source symphony

## Scores

- Startup clarity: 5
- Retrieval usefulness: 5
- Skill fit: 4
- Template fit: 5
- Closeout friction: 4
- Overall confidence: 5

## What Complicated The Session Most

- Observation: `forge_campaign_start` falla con `activity argument does not implement TelemetryCarrier` y reintenta infinito (MaximumAttempts:0): la campaña queda RUNNING para siempre sin progreso y sin señal en el historial Temporal (pending activity state=Scheduled sin eventos Started/Failed por intento).
- Why it was hard: el historial mostraba 5 eventos mientras el worker registraba attempts crecientes; hubo que ir a `DescribeWorkflowExecution` (pending activity + lastFailure) y al log on-host del worker para reconciliar.
- Proposed improvement: documentar en el runbook de triage que actividades rechazadas por el interceptor estricto del SDK no generan eventos de historia por intento; usar DescribeWorkflowExecution como primer canal.

## Most Useful Part Of Sistema 1

- What helped: checkpoint append-only del proyecto + decisiones del 2026-09-02/03 (period mismatch, smoke 0.2.88 con SHAs de CFX y método de acceso Windows).
- Why it helped: la autoridad CFX se reconcilió directo contra los objetos MinIO del smoke (00_configs) sin redescubrir nada; el formato del patch de periodo se probó con el parser congelado en vez de adivinar XML.
- Keep/change: mantener; añadir al runbook golden-e2e el mecanismo de acceso al host Windows (worker-kronos.local → 192.168.31.128, usuario kor, ps1 de una línea / EncodedCommand).

## Least Useful Or Noisy Part

- What did not help: el runbook `symphony-prod-probe` anota firmas DI/SDK que ya no coinciden (GetObject 3 valores, ListObjects slice, ListWorkflow request-based, PollerInfo sin GetClientFeatures); cada uso obliga a corregir a prueba y error.
- Why it was weak/noisy: costó 3 ciclos de compilación.
- Proposed cleanup: actualizar el runbook con las firmas vigentes del SDK `c855944` o referenciar el probe concreto de la sesión como apéndice.

## Missing Support

- Problem not solved by Sistema 1: no existía procedimiento de desenrollado para una campaña colgada en reintento infinito (Terminate prohibido; CancelWorkflow formal queda colgado por el mismo defecto de carrier).
- How Sistema 1 could help next time: runbook "desenrollado de campaña residual" post-fix (decidir Terminate vs Cancel + limpieza PG).
- Suggested artifact type: runbook con verificación y rollback.

## Retrieval Feedback

- Useful query or source: `known-error 2026-09-02 mt5-fidelity-period-mismatch`, checkpoint del proyecto (secciones 0.2.88), `cfx_configured_period.go` como autoridad del periodo.
- Missing context: nada material.
- Duplicate/noisy result: ninguno.
- Better future query: "campaign start TelemetryCarrier" en known-errors tras este cierre.

## Skill Feedback

- Skill that worked well: agents-os-bootstrap (base mínima y NEXT EXACT en la nota global).
- Skill that was confusing: ninguna.
- Trigger/routing gap: el materializador no acepta `agent-run`/`change-log` con guion; el tipo canónico es `agent_run`/`change_log`.
- Suggested contract change: aceptar ambas grafías o documentar las normalizadas.

## Template Feedback

- Template used: session-feedback, agent-run, decision, known-error, change-log.
- Field that helped: `agent_run` enlazado desde feedback.
- Field that felt redundant: ninguna.
- Missing field: para agent-run, un campo `cost_signature` (backtests/minutos consumidos) para certificaciones físicas.

## Memoria Interna (Internal Memory)

- ¿Consultaste la memoria interna al iniciar? sí (nota global always-load).
- ¿Valor operativo? El checkpoint NEXT EXACT evitó re-planificar; la lección del replayer (DI InitSelective obligatorio) reutilizó el harness anterior sin RCA nueva.
- ¿Mensaje para el próximo agente? sí: línea de continuidad con NEXT EXACT `RETURN_TO_LEAD_AFTER_C3_BLOCKED` y estado residual de la campaña.
- Utilidad 1-5: 5.

## Pain Pattern Candidate

- Is this likely to repeat? yes (hasta el fix de carriers; cualquier intake de campaña crea residuo).
- Suggested severity: high
- Candidate owner: lead de Echo Forge
- Promote to L3 memory? yes (ya materializado como known-error).

## One Next Improvement

- Corregir los 5 request types de campaña para implementar `TelemetryCarrier` + assertions, y hacer replay-friendly la aserción de WorkflowID; es el único camino para desbloquear C3.
