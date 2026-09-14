---
type: change_log
schema_version: 1
scope: session
created: "2026-09-13"
updated: "2026-09-13"
area: "[[Aranea]]"
project: "[[AGENT-PLATFORM - MCP Access Plane]]"
application:
entities:
  - "[[Aranea]]"
  - "[[Echo]]"
  - "[[Echo Forge]]"
related:
  - "[[aranea-mcps-expert]]"
  - "[[aranea-ssh-mcp]]"
aliases:
  - SQX SSH MCP operator profiles
confidence: verified
source_session:
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
  - area/aranea
  - tech/mcp
  - tech/ssh
---

# Aranea SSH MCP — SQX operator profiles

## Cambio

- **Tipo:** updated + created
- **Archivo(s):**
  - `30-resources/agents/skills/aranea-mcps-expert/SKILL.md`
  - `30-resources/runbooks/aranea-ssh-mcp.md`
  - `10-projects/Aranea/AGENT-PLATFORM/agentes/workstreams/SSH-MCP.md`

## Motivo

- Los agentes que operan SQX necesitan escritura/ejecución controlada en Zeus, Hera y Kronos; los profiles históricos viewer ya no cubrían el trabajo real.
- Era necesario distinguir capacidad MCP `operator` de privilegio OS real y dejar clara la semántica de `approvalPolicy="auto"`.

## Fuentes usadas

- Config/runtime real de `ssh-mcp` en `mcps`.
- `GET /status` autenticado después del restart.
- Handshake MCP `2025-03-26`, `tools/list` y smokes E2E ejecutados en esta sesión.

## Resolución aplicada

- `sqx-zeus`, `sqx-hera` y `sqx-kronos` quedan documentados como `operator/readOnly=false` bajo identidad remota `echo-dev`, no root-equivalent.
- La skill enruta lecturas a `read-command` y mutaciones justificadas a `run-command`/SFTP; el runbook contiene tool semantics, certification y rollback.
- Se creó `workstreams/SSH-MCP.md` dentro del MCP Access Plane como estado vigente del workstream y para superseder referencias históricas viewer sin duplicar la autoridad mecánica del runbook.
- `approvalPolicy="auto"` queda explícitamente tratado como auto-ejecución posible, no como human-in-the-loop.

## Validación

- `ssh-mcp` `running/healthy` tras reinicio acotado.
- `/status`: los tres SQX reportaron `role=operator`, `readOnly=false`.
- `sqx-zeus`, `sqx-hera`, `sqx-kronos`: `run-command` write → `read-command` verify → `run-command` cleanup, todos PASS/CLEAN.
- `mt5-kronos` permaneció viewer/read-only y los otros profiles no fueron modificados.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** no contiene bearer tokens, passwords ni private keys. Los fingerprints/credenciales concretos no se copiaron a este log.

## Rollback

- Para revertir la promoción SQX: volver los tres profiles a `role="viewer"` + `readOnly=true`, reiniciar únicamente `ssh-mcp` y revalidar `/status` + `read-command`; existe backup runtime previo al cambio.
