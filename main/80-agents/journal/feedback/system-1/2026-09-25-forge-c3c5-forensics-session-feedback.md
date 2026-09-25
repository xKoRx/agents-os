---
type: session_feedback
schema_version: 1
created: 2026-09-25
updated: 2026-09-25
area: "[[Echo]]"
project: "[[Echo Forge — Operación Real V2]]"
application:
entities:
  - "[[aranea-mcps-expert]]"
  - "[[Echo Forge — Operación Real V2]]"
aliases: []
agent_surface: "[[ZCode]]"
agent_model: GLM-5.3-Flash
load_policy: manual
indexable: false
index_priority: low
tags:
  - kind/session-feedback
  - area/echo
  - tech/mcp
---

# Session Feedback — 2026-09-25 — forge-c3c5-forensics

## Friction

- `aranea-temporal-ro` MCP: el perfil `aranea` consulta un namespace fijo; el workflow del FlowRun vive en `sqx-prop` y toda describe/list devuelve "not found" (no es inexistencia real). La read surface alternativa (build local de `sqx/cmd/sqx-flowkit` con ENV=production) resolvió stages/resultado del FlowRun; falta cobertura de namespace `sqx-prop` en la capability o documentación del límite.
- Mongo forge RO MCP: `session not found` en toda llamada (recurrente; ya registrado en sesiones previas).

## Degradación / Gap

- Subagente `forge-functional-cartographer` (ZCode) falló 2× con "Captcha instance timed out after 10000ms" antes de producir output — infra de subagentes, no del prompt; el trabajo se hizo inline.
- Trampa del SDK etcd (`WithPrefix`): el prefijo debe incluir el slash inicial (`/sqx-worker/production/`); sin él las Gets fallan silenciosamente como "not found"/config incompleta.

## Pain Pattern Candidate

- Los estados de FlowRun declarados en bitácoras ("queda en retry y completará solo") pueden quedar stale: la verificación canónica es `sqx-flowkit run stages` + log del worker, no la expectativa del retry.
