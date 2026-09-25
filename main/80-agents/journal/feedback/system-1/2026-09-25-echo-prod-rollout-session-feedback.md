---
type: feedback
schema_version: 1
scope: session
created: 2026-09-25
updated: 2026-09-25
area: "[[Personal]]"
project: "[[AGENTS OS]]"
entities:
  - "[[AGENTS OS]]"
related: []
aliases: []
agent_surface: "[[Codex]]"
agent_model: unknown
agent_run:
session_goal:
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

# 2026-09-25 — Rollout Echo PROD (fricciones Sistema 1)

- **Pain pattern candidate (1):** acceso físico PROD de escritura inexistente para coding agents: PG PROD MCP RO-only, ETCD MCP RO + secret-named bloqueado, SSH `.71` viewer que rechaza incluso comandos safe (`POLICY_DENIED`), sin psql/pg_dump/docker en Daedalus. Todo el trabajo físico real requerirá helpers Go efímeros con secretos resueltos en memoria (patrón pgwrap) o ventanas owner. Si el rollout PROD va a ser recurrente, conviene un perfil `echo-prod-operator` autorizable por ventana.
- **hasura-prod-ro degradado:** `get_schema` y `export_metadata` fallan (`Connection closed`); sólo `get_version` y `get_inconsistent_metadata` respondieron. El export de metadata PROD se resolvió planificando `hasura metadata export -o json` vía CLI en el runbook owner.
- **ZCode Skill tool** no resuelve skills del INDEX del vault (fallback lector directo usado); ya conocido ([[zcode-skill-tool-vault-skills]]), se confirma en otra superficie/sesión.
