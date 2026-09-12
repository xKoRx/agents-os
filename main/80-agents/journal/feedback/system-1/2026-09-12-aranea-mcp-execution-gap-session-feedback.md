---
type: feedback
schema_version: 1
scope: session
created: 2026-09-12
updated: 2026-09-12
area: "[[Echo]]"
project: "[[Echo Forge — F-04 Magic allocation, version seal and handoff]]"
entities:
  - "[[Echo Forge — F-04 Magic allocation, version seal and handoff]]"
  - "[[Echo Forge]]"
related:
  - "[[AGENTS OS]]"
  - "[[2026-09-12-zcode-glm-5.3-flash-f04-t2-implementation]]"
aliases: []
agent_surface: "[[ZCode]]"
agent_model: builtin:zai-coding-plan/GLM-5.3-Flash
agent_run: "[[2026-09-12-zcode-glm-5.3-flash-f04-t2-implementation]]"
session_goal: Reintentar T2.12 PHYSICAL vía superficies MCP de Aranea tras corrección del manager
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

# Session Feedback - 2026-09-12 - aranea-mcp-execution-gap

## Context

- Agent surface: [[ZCode]]
- Agent model: builtin:zai-coding-plan/GLM-5.3-Flash
- Agent run: [[2026-09-12-zcode-glm-5.3-flash-f04-t2-implementation]]
- Session goal: ejecutar F-04 T2.12 PHYSICAL vía Host MCP de Aranea
- Main entity: [[Echo Forge — F-04 Magic allocation, version seal and handoff]]
- Skills used: bootstrap, session-close
- Retrieval mode: Host MCP (`mcp__aranea-ssh`) read-command/run-command; Graphify no usado
- Artifacts changed: proyecto F-04 (bitácora + estado), este feedback

## Scores

- Startup clarity: 4
- Retrieval usefulness: 4
- Skill fit: 3
- Template fit: 4
- Closeout friction: 2
- Overall confidence: 4

## What Complicated The Session Most

- Observation: los perfiles Host MCP de los hosts Linux del fleet (`sqx-zeus`, `sqx-hera`, `sqx-kronos`) son viewer read-only: `open-session` y `run-command` devuelven POLICY_DENIED y `read-command` sólo acepta un allowlist de lectura; además `read-command` rechaza comandos compuestos, y en `mt5-kronos-operator` no hay sesión interactiva (shell no-POSIX) ni lectura de path/CWD de procesos elevados (Get-CimInstance access denied).
- Why it was hard: la certificación física F-04 exige desplegar el build de la feature en el worker padre (el fleet corre 0.2.96, pre-F-04), reiniciar workers, ejecutar `sqcli` y operar el control plane; ninguna de esas operaciones es expresable con las superficies MCP actuales, así que T2.12 queda BLOCKED — ARANEA MCP aun con todos los hosts alcanzables y las capabilities físicas presentes (MetaEditor64, sqx-mt5-worker, sqcli, license.db).
- Proposed improvement: un perfil operator (o una capability MCP de deploy/ejecución de procesos y de consulta de control plane) para los hosts Linux del fleet, más una surface MCP de ETCD para leer claves `mt5/*`, `sqcli/binary_path` y `echo/ingest/*` sin shell; y sesiones interactivas Windows vía MCP o un wrapper POSIX documentado.

## Most Useful Part Of Sistema 1

- What helped: la regla del manager de usar Host MCP como única vía llevó a un mapa de capabilities real y verificable por host (quién tiene qué binario/corriendo), que queda en la bitácora del proyecto como evidencia del bloqueo y del desbloqueo necesario.
