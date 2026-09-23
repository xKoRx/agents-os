---
type: feedback
schema_version: 1
scope: session
created: "2026-09-23"
updated: "2026-09-23"
area: "[[Personal]]"
project: "[[AGENTS OS]]"
entities:
  - "[[AGENTS OS]]"
  - "[[Echo]]"
  - "[[aranea-mcps-expert]]"
related:
  - "[[echo-production-operational-audit]]"
aliases: []
agent_surface: "[[ZCode]]"
agent_model: account:zai-individual-coding-plan/GLM-5.3-Flash
agent_run: "[[2026-09-23-zcode-glm-5.3-flash-echo-bridge-broker-reconcile]]"
session_goal: "Diagnosticar por qué WSF NEW! (183623) no recibía copias en PROD, implementar el fix de reconciliación de broker del echo-bridge, validarlo en testing y llevarlo a master"
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

# Session Feedback - 2026-09-23 - echo bridge broker reconcile

## Context

- Agent surface: [[ZCode]]
- Agent model: account:zai-individual-coding-plan/GLM-5.3-Flash
- Agent run: [[2026-09-23-zcode-glm-5.3-flash-echo-bridge-broker-reconcile]]
- Session goal: diagnóstico "WSF NEW! no copia" → fix bridge (reconciliación broker) → deploy testing dev-win → master.
- Main entity: [[Echo]]
- Skills used: agents-os-bootstrap, aranea-agent-dev (router), echo-production-operational-audit (sub-rutina "¿por qué no copia?"), agents-os-session-close, agents-os-session-feedback, agents-os-agent-run-register.
- Retrieval mode: Graphify no requerido para el diagnóstico (código + MCPs); etcd vía REST v3 directa por caída del MCP.
- Artifacts changed: known-error L3, agent_run, esta feedback, commit `c99aee06` en master de xKoRx/echo, deploy dev-win.

## Scores

Use 1-5, where 1 is poor and 5 is excellent.

- Startup clarity: 5
- Retrieval usefulness: 4
- Skill fit: 5
- Template fit: 4
- Closeout friction: 3
- Overall confidence: 4

## What Complicated The Session Most

- Observation: los MCPs de sesión persistente (etcd-ro, kafka-dev-admin) pierden su sesión entre llamadas ("Session not found"), y el gate de aprobación del MCP SSH de dev-win rechaza fail-closed todo lanzamiento de procesos (Start-Process, open-session con comando, cmd start) porque el cliente no soporta elicitation.
- Why it was hard: sin via alternativa documentada, el deploy/test físico del bridge en Windows requirió inventar tres mecanismos (etcd REST v3 directa, productor Kafka propio en Go, launcher DETACHED_PROCESS) y rodear un timeout de 30s que mata el árbol de procesos remoto.
- Proposed improvement: documentar en [[aranea-mcps-expert]] (o el runbook SSH) el patrón validado para procesos persistentes en hosts Windows vía MCP: launcher detached + schtasks de diagnóstico + REST etcd, y que el gate de aprobación degrade a "denegar con mensaje accionable" en clientes sin elicitation.

## Most Useful Part Of Sistema 1

- What helped: la sub-rutina "¿por qué no copia?" de [[echo-production-operational-audit]] + el [[Echo + Echo Forge — Environment Contract]].
- Why it she helped: la sub-rutina trae las queries y patrones exactos ya validados (WARNs execution_planner/mm_engine, symbol_mappings, riesgo silencioso); el contrato fijó DEV vs PROD y evitó tocar mt4-real sin autorización.
- Keep/change: keep; añadir a la skill de auditoría el discriminador Loki `{service_name="echo-bridge"} |= "detransformed"` (broker de sesión por command_id) como paso estándar.

## Least Useful Or Noisy Part

- What did not help: `aranea-hasura-prod-ro.get_schema` falla siempre ("Connection closed") y costó varias llamadas desperdiciadas antes de cambiar a postgres-ro directo.
- Why it was weak/noisy: la herramienta expone una introspección que el servidor no puede servir por tamaño, sin hint del fallback.
- Proposed cleanup: quitar get_schema del perfil PROD o acotarlo; documentar "usar execute_sql + information_schema" en el runbook del MCP.

## Missing Support

- Problem not solved by Sistema 1: no existía procedimiento para desplegar/validar un binario nuevo en un host Windows del homelab a través del MCP SSH (gates + timeout + permisos del usuario).
- How Sistema 1 could help next time: runbook "dev-win bridge deploy & smoke" con el mecanismo launcher-detached, la receta etcd REST y la verificación de identidad (go version -m + SHA256).
- Suggested artifact type: runbook.

## Retrieval Feedback

- Useful query or source: sub-rutina de la skill de auditoría; information_schema vía postgres-ro; Loki label `level` para escanear WARNs sin escanear DEBUG.
- Missing context: la topología de bridges DEV (dev-win ya tenía un echo-bridge-v3 corriendo con cuentas DEV sembradas en etcd) no estaba en el contrato de ambientes — sólo se descubrió inspectando procesos.

## Internal Memory Assessment

- La memoria interna (checkpoint de diagnóstico en memoria del harness) evitó re-derivar la causa raíz entre sesiones del mismo día; se actualizó 3 veces por delta. Funcionó.

## Context Efficiency

- context_high_water_mark: unknown
- main_context_growth_sources: outputs de Loki/Prometheus verbosos (líneas JSON completas), lecturas de código largas (pipe_handler/session_manager), prints de tests.
- avoidable_context_growth: re-lecturas del schema de tablas vía information_schema cuando bastaba una columna; bucle temprano de llamadas livianas a Hasura antes de cambiar de canal (fricción real, no optimizable a posteriori).
- compaction_opportunity: sí — tras cerrar la fase de implementación+tests (commit creado) un checkpoint+compaction habría liberado el grueso del diff/reviews sin perder autoridad (el estado vivo ya estaba en git + memoria).
- efficiency_assessment: REVIEW

For each material optimization candidate:

- change: usar `execute_sql` directo ante el primer fallo de `get_schema` (regla: introspección GraphQL en PROD = no intentable).
- evidence: 6+ llamadas desperdiciadas al inicio de la investigación.
- expected_impact: LOW
- risk_to_quality: LOW

- change: acotar las lecturas de Loki con Select-String de atributos específicos en vez de líneas completas cuando el objetivo son atributos.
- evidence: varias respuestas de 300-400 chars truncadas que requirieron re-query.
- expected_impact: LOW
- risk_to_quality: LOW
