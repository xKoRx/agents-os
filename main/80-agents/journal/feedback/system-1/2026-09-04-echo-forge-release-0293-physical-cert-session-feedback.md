---
type: feedback
schema_version: 1
scope: session
created: 2026-09-04
updated: 2026-09-04
area: "[[Personal]]"
project: "[[AGENTS OS]]"
entities:
  - "[[AGENTS OS]]"
related: []
aliases: []
agent_surface: "[[Codex]]"
agent_model: unknown
agent_run: "[[2026-09-04-codex-unknown-echo-forge-release-0293-physical-cert]]"
session_goal: "Certificación física de release 0.2.93 y Finalist Factory V1"
source_session: "ECHO-FORGE-RELEASE-0.2.93-AND-FINALIST-FACTORY-V1-PHYSICAL-CERT-NORMAL"
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

# Session Feedback - 2026-09-04 - Echo Forge release 0.2.93 physical cert

## Context

- Agent surface: [[Codex]]
- Agent model: unknown
- Agent run: [[2026-09-04-codex-unknown-echo-forge-release-0293-physical-cert]]
- Session goal: Certificación física de release 0.2.93 y Finalist Factory V1
- Main entity: [[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]
- Skills used: [[agents-os-bootstrap]], [[agents-os-context-retrieval]], [[agents-os-agent-run-register]], [[agents-os-session-close]]
- Retrieval mode: bootstrap + focused retrieval; Graphify stale, fallback `rg`.
- Artifacts changed: release/deploy físico y config efímera; notas Agents OS; ningún source file.

## Scores

Use 1-5, where 1 is poor and 5 is excellent.

- Startup clarity: 5
- Retrieval usefulness: 4
- Skill fit: 5
- Template fit: 5
- Closeout friction: 3
- Overall confidence: 5

## What Complicated The Session Most

- Observation: El watcher residente estaba stale y luego el source exacto expuso un conflicto v2/v1 al resolver la Campaign.
- Why it was hard: El log era enorme y el primer error de proceso ocultaba el segundo error determinante; se necesitó aislar PIDs y leer por patrones.
- Proposed improvement: Añadir al preflight un smoke read-only que valide la proyección de `ForgeCampaignSpec v2` a `ForgeCampaignStopPolicy v1` antes de permitir input físico.

## Most Useful Part Of Sistema 1

- What helped: El checkpoint histórico, known errors y decisiones de Echo Forge acotaron authorities, no-retry y Graphify stale.
- Why it helped: Permitieron distinguir el nuevo defecto de residuos de Campaign anteriores.
- Keep/change: Mantener recuperación enfocada; añadir una consulta canónica de estado Campaign pre-dispatch.

## Least Useful Or Noisy Part

- What did not help: El log append-only del watcher y el proceso huérfano.
- Why it was weak/noisy: El archivo tiene millones de líneas y mezcló ejecuciones históricas con la certificación actual.
- Proposed cleanup: Soportar un log de certificación separado por run, sin cambiar la evidencia histórica.

## Missing Support

- Problem not solved by Sistema 1: No había una alerta explícita sobre la contradicción entre schema wrapper v2 y StopPolicy v1.
- How Sistema 1 could help next time: Registrar un known error de compatibilidad de contratos y un preflight de proyección.
- Suggested artifact type: known_error + runbook de preflight.

## Retrieval Feedback

- Useful query or source: `rg` enfocado en `resolveForgeCampaign`, `ForgeCampaignStopSchema` y el request id.
- Missing context: Un selector Graphify operativo para el repositorio actualizado.
- Duplicate/noisy result: `watcher_screen.log` histórico y stale Graphify.
- Better future query: Filtrar primero por request id/timestamp y luego leer sólo la ventana de evidencia.

## Skill Feedback

- Skill that worked well: `agents-os-session-close` y `agents-os-agent-run-register`.
- Skill that was confusing: Ninguna; el cierre detallado fue necesario por el bloqueo.
- Trigger/routing gap: El bootstrap no puede comprobar por sí solo contratos físicos del repo.
- Suggested contract change: Añadir checklist de preflight para wrappers que proyectan políticas internas.

## Template Feedback

- Template used: known_error, agent_run, feedback, change_log.
- Field that helped: `source_session`, `related`, `verification`.
- Field that felt redundant: Scores cuando el resultado queda bloqueado por producto.
- Missing field: `blocking_gate` explícito en feedback.

## Memoria Interna (Internal Memory)

- ¿Consultaste la memoria interna (`80-agents/memory/internal/`) al iniciar? sí
- ¿Qué valor operativo aportó para esta sesión (continuidad, detalles crudos, advertencias)? Aportó continuidad de authorities, restricciones y residuos históricos.
- ¿Dejaste algún mensaje, instrucción o hipótesis para el próximo agente en la memoria interna? No; el known error público y el checkpoint son suficientes.
- ¿Qué tan útil te resulta tener este espacio privado fuera de la vista directa del usuario (1-5) y cómo podemos mejorar su utilidad? 4; mantenerlo compacto y enlazado a checkpoints.

## Pain Pattern Candidate

- Is this likely to repeat? yes
- Suggested severity: high
- Candidate owner: Symphony ForgeCampaign intake owner
- Promote to L3 memory? defer

## One Next Improvement

- Añadir una prueba/preflight físico de compatibilidad wrapper v2 → StopPolicy v1 antes del próximo release.
