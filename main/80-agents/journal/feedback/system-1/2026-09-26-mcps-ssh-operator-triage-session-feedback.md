---
type: feedback
schema_version: 1
scope: session
created: 2026-09-27
updated: 2026-09-27
area: "[[Personal]]"
project: "[[AGENT-PLATFORM - MCP Access Plane]]"
entities:
  - "[[AGENT-PLATFORM - MCP Access Plane]]"
  - "[[aranea-ssh-mcp]]"
  - "[[AGENTS OS]]"
related: []
aliases: []
agent_surface: "[[Ariadna]]"
agent_model: GLM-5.3-Flash (host-reported, provider zai)
agent_run: "[[2026-09-26-ariadna-glm53-mcps-ssh-operator-triage]]"
session_goal: Exonerar el plano MCP tras reporte de pérdida de operator en SQX; identificar causa real del síntoma del agente
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

# Session Feedback - 2026-09-27 - mcps-ssh-operator-triage

## Context

- Agent surface: Ariadna (Hermes desktop, hermes-vm)
- Agent model: GLM-5.3-Flash
- Agent run: [[2026-09-26-ariadna-glm53-mcps-ssh-operator-triage]]
- Session goal: mandato owner "revisa los mcps, algo pasó ahí, deberían tener permiso de operator"
- Main entity: [[AGENT-PLATFORM - MCP Access Plane]]
- Skills used: mcp-access-plane-operations (perfil Hermes), agents-os-operations, agents-os-session-close, agents-os-agent-run-register (vault, leídas por path)
- Retrieval mode: search_files + read_file sobre rutas canónicas (sin tool Graphify en este entorno)
- Artifacts changed: nota del plano (Estado actual + Bitácora), runbook [[aranea-ssh-mcp]] (§ Triage), skill Hermes (triage + inspector), 2 notas de journal

## Scores

- Startup clarity: 4
- Retrieval usefulness: 4
- Skill fit: 5
- Template fit: 4
- Closeout friction: 3
- Overall confidence: 5

## What Complicated The Session Most

- Observation: el reporte llegó sin consumidor identificado ("un agente") y el plano estaba sano — triage por descarte a ciegas.
- Why it was hard: configs kor `600` ilegibles por diseño; el chain resuelve vacío + 401 falso bajo identidad ajena; `docker events` vacío en el LXC impide atribuir la recreación del contenedor.
- Proposed improvement: convención de reporte de incidentes por agentes: surface/consumidor + texto EXACTO del error observado, no sólo el síntoma ("perdí operator").

## Most Useful Part Of Sistema 1

- What helped: `/status` (roles por perfil, verdad viva) + probes funcionales con el helper certificado (una sesión, release explícito).
- Why it helped: exoneración del plano en minutos con evidencia reproducible, sin tocar el freeze.
- Keep/change: keep; añadir al skill el orden de triage ya aplicado (hecho).

## Least Useful Or Noisy Part

- What did not help: sintomas ambiguos del chain kor (ENOENT vs EACCES vs resolve-vacío) que simulan drift donde no lo hay.
- Why it was weak/noisy: costó 2 falsas pistas (401 del chain, falta de bearer) antes del descarte correcto.
- Proposed cleanup: nada accionable server-side; es intrinsic al diseño 600-kor — documentado como trampa.

## Missing Support

- Problem not solved by Sistema 1: sin telemetría de lifecycle docker en `mcps` — quién recreó `ssh-mcp` el 25-sep es invisible (audit log cubre sólo `mcps-ops`).
- How Sistema 1 could help next time: hook docker-events → log persistente en el LXC (decisión owner, change mínimo).
- Suggested artifact type: bullet en Ideas/Backlog del proyecto (registrado).

## Retrieval Feedback

- Useful query o source: search_files "aranea-ssh" → runbook + workstream al primer tiro.
- Missing context: ninguno.
- Duplicate/noisy result: ninguno.
- Better future query: n/a.

## Skill Feedback

- Skill that worked well: `mcp-access-plane-operations` (patterns probados: piped-bearer, session-steps, scp'd-Python).
- Skill that was confusing: ninguna; `skill_view` no resuelve skills del vault es comportamiento documentado.
- Trigger/routing gap: el agente que reportó el síntoma no dejó artefacto consultable (sin feedback/run propio vinculable) — el triage partió sin su evidencia.
- Suggested contract change: misma convención de reporte del punto "What Complicated" (surface + error exacto).

## Template Feedback

- Template used: agent-run + feedback (materializados por script).
- Field that helped: separación Evidencia/Limitaciones en agent_run.
- Field that felt redundant: scores 5-ítems duplicados en ambas notas.
- Missing field: en feedback de infra, un campo "consumidor/surface afectada" además de `agent_surface` (la superficie que REPORTA ≠ la afectada).

## Memoria Interna (Internal Memory)

- ¿Consultaste la memoria interna (`80-agents/memory/internal/`) al iniciar? no como nota aparte: el delta operativo llegó vía skill Hermes `agents-os-operations` + memoria de perfil; el bootstrap del vault se ejecutó por lectura directa de SKILL.md.
- ¿Qué valor operativo aportó? reglas de no-duplicación y de verificación de claims de hermanos aplicadas al no reescribir canon ni inventar estado del Codex.
- ¿Dejaste algún mensaje para el próximo agente? sí — § Triage en [[aranea-ssh-mcp]] + bullets en el proyecto (estado real y UNVERIFIED explícito).
- Utilidad (1-5): 4.

## Pain Pattern Candidate

- Is this likely to repeat? yes (agentes reportando síntomas sin consumidor ni error identificado).
- Suggested severity: low
- Candidate owner: convención de reporte de incidentes (Agents-OS) + telemetría docker en mcps (owner).
- Promote to L3 memory? no (queda en runbook + skill + esta nota).

## One Next Improvement

- Telemetría de lifecycle docker en `mcps` (hook events → log persistente) + convención de reporte con error exacto; cierre de la hipótesis Codex cuando el owner comparta la sección CODEX del inspector.
