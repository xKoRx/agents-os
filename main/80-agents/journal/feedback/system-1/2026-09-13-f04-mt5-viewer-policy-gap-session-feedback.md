---
type: feedback
schema_version: 1
scope: session
created: "2026-09-13"
updated: "2026-09-13"
area: "[[Personal]]"
project: "[[Echo Forge — F-04 Magic allocation, version seal and handoff]]"
entities:
  - "[[AGENTS OS]]"
  - "[[Aranea]]"
related:
  - "[[Echo Forge]]"
agent_surface: "[[Codex]]"
agent_model: unknown
agent_run:
session_goal: "Resolver el gap Windows mt5-kronos con probes viewer mínimos y cerrar sin bypass."
source_session: 2026-09-13-f04-mt5-viewer-policy-gap
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

# Session Feedback - 2026-09-13 - F-04 MT5 Viewer Policy Gap

## Context

- Agent surface: [[Codex]]
- Agent model: unknown
- Agent run: no material coding/debug/review/testing segment; skipped.
- Session goal: resolver el gap Windows mt5-kronos con probes viewer mínimos y cerrar sin bypass.
- Main entity: [[Echo Forge]] / [[Aranea]]
- Skills used: agents-os-bootstrap, aranea-agent-dev, aranea-mcps-expert, aranea-ssh-mcp, deployment-proof, e2e-gated-validation, agents-os-session-close y agents-os-session-feedback.
- Retrieval mode: focused Markdown + MCP Aranea viewer.
- Artifacts changed: F-04 project/parent status, session summary, feedback y change log; no product code.

## Scores

- Startup clarity: 5
- Retrieval usefulness: 5
- Skill fit: 5
- Template fit: 4
- Closeout friction: 4
- Overall confidence: 5

## What Complicated The Session Most

- Observation: el viewer Windows permitió identidad básica pero rechazó todas las operaciones mínimas de servicio, proceso, filesystem y executable.
- Why it was hard: la policy responde que incluso comandos seguros son rechazados por readOnly, sin exponer un probe runtime equivalente.
- Proposed improvement: publicar un allowlist Windows viewer explícito para servicio, proceso, path, release/hash y poller.

## Most Useful Part Of Sistema 1

- What helped: la regla de autoridad mínima y el procedimiento de reducir una lectura por llamada.
- Why it helped: permitió distinguir capability policy gap de viewer ausente y evitó usar operator como bypass.
- Keep/change: mantener el criterio fail-closed y agregar una matriz de probes Windows certificados.

## Least Useful Or Noisy Part

- What did not help: los registros históricos de intentos previos no listan todas las formas mínimas admitidas y rechazadas.
- Why it was weak/noisy: obligó a redescubrir la frontera exacta durante la sesión.
- Proposed cleanup: documentar respuestas exactas por operación en el runbook de SSH.

## Missing Support

- Problem not solved by Sistema 1: no existe lectura viewer Windows admisible para StagerRuntime, sqx-mt5-worker, effective path/release o sqx-mt5-queue.
- How Sistema 1 could help next time: mantener un contrato de probe read-only por perfil con una operación por llamada.
- Suggested artifact type: runbook/capability correction.

## Retrieval Feedback

- Useful query or source: F-04 project, runtime-authority correction summary, aranea-ssh-mcp y deployment-proof.
- Missing context: allowlist Windows efectiva del servidor MCP.
- Duplicate/noisy result: históricos que sólo dicen POLICY_DENIED sin separar identidad admitida de evidencia runtime requerida.
- Better future query: buscar primero el contrato de profile/policy y luego los probes mínimos por pregunta.

## Skill Feedback

- Skill that worked well: aranea-mcps-expert junto con deployment-proof.
- Skill that was confusing: ninguna en esta sesión.
- Trigger/routing gap: el tool schema no publica el allowlist efectivo del profile.
- Suggested contract change: exponer probes read-only certificados o un error que enumere la operación admisible sin ampliar autoridad.

## Template Feedback

- Template used: session feedback materializado.
- Field that helped: Missing Support y Pain Pattern Candidate.
- Field that felt redundant: ninguno.
- Missing field: operación exacta y respuesta de policy como campos estructurados.

## Memoria Interna (Internal Memory)

- ¿Consultaste la memoria interna (80-agents/memory/internal/) al iniciar? sí.
- ¿Qué valor operativo aportó para esta sesión (continuidad, detalles crudos, advertencias)? recordó fallar cerrado ante evidencia física no demostrada y no repetir efectos laterales.
- ¿Dejaste algún mensaje, instrucción o hipótesis para el próximo agente en la memoria interna? no; el delta quedó en el proyecto y este cierre.
- ¿Qué tan útil te resulta tener este espacio privado fuera de la vista directa del usuario (1-5) y cómo podemos mejorar su utilidad? 5; mantenerlo compacto y separado del estado de proyecto.

## Pain Pattern Candidate

- Is this likely to repeat? yes
- Suggested severity: medium
- Candidate owner: Aranea MCP / runtime operations
- Promote to L3 memory? defer

## One Next Improvement

- Exponer y certificar un probe Windows viewer mínimo que entregue StagerRuntime, proceso, path/release y poller sin elevar autoridad.
