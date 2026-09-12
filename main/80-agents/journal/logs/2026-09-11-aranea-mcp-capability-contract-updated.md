---
type: change_log
scope: area
created: "2026-09-11"
updated: "2026-09-11"
area: "[[Aranea]]"
project: "[[AGENT-PLATFORM - MCP Access Plane]]"
application:
entities:
  - "[[Aranea]]"
  - "[[Echo]]"
  - "[[Echo Forge]]"
related:
  - "[[aranea-mcps-expert]]"
  - "[[aranea-postgres-mcp]]"
  - "[[aranea-mongodb-mcp]]"
  - "[[aranea-ssh-mcp]]"
  - "[[aranea-mcp-capability-plane]]"
aliases:
  - Aranea MCP capability contract updated
confidence: verified
source_session:
load_policy: manual
indexable: false
index_priority: never
tags:
  - area/aranea
  - kind/changelog
  - scope/area
  - tech/mcp
---
# 2026-09-11 Aranea MCP Capability Contract Updated

## Cambio

- **Tipo:** updated
- **Archivo(s):** `30-resources/agents/skills/aranea-mcps-expert/SKILL.md`, `80-agents/memory/public/runbook/aranea-postgres-mcp.md`, `80-agents/memory/public/runbook/aranea-mongodb-mcp.md`, `80-agents/memory/public/runbook/aranea-ssh-mcp.md`, `80-agents/memory/public/runbook/aranea-mcp-capability-plane.md`, `30-resources/aranea/02-servicios/ml-ia.md`, `30-resources/agents/00-index.md`, `30-resources/agents/log.md`, `30-resources/aranea/log.md`.

## Motivo

La documentación previa mezclaba autoridad con ambiente y podía inducir a usar una capability RO de PROD como paso previo o verificación para operaciones DEV. La certificación real estableció el contrato simple del owner: para data planes Aranea, PROD es read-only y DEV es read/write; no existen sandboxes o perfiles dinámicos implícitos. También se observó un fallo de discovery Mongo causado por bearer env vars ausentes en el proceso cliente, no por MongoDB.

## Resolución aplicada

- `aranea-mcps-expert` ahora elige ambiente antes que capability y contiene las rutas físicas canónicas de los runbooks bajo `80-agents/memory/public/runbook/`.
- PostgreSQL Echo quedó documentado como PROD `echo` / `mcp_echo_prod_ro` mediante `aranea-postgres-ro` y DEV `echo-develop` / `mcp_echo_dev_rw` mediante `aranea-postgres-rw`.
- Mongo Forge quedó documentado con el mismo contrato PROD RO / DEV RW y con troubleshooting de discovery/env antes de diagnosticar backend.
- SSH registró la certificación real de operator `run-command` y SFTP; `POLICY_DENIED` sobre viewer se documentó como boundary esperado.
- El capability-plane documenta que un bloque configurado no implica tool discovery si el proceso no heredó sus env vars.
- La Resource Wiki e índices apuntan a la skill y a los runbooks sin duplicar procedimientos.

## Validación

- PostgreSQL PROD: `current_user=mcp_echo_prod_ro`, `current_database=echo`; SELECT verificado y escritura ausente.
- PostgreSQL DEV: `current_user=mcp_echo_dev_rw`, `current_database=echo-develop`; lectura y probe DDL/DML temporal con rollback verificados.
- SSH: `run-command` operator y SFTP upload/download/delete verificados sobre worker-kronos; viewer denegó `run-command` por policy como se esperaba.
- Mongo Forge: las env vars `ARANEA_MONGO_FORGE_MCP_RO_BEARER` y `ARANEA_MONGO_FORGE_MCP_RW_BEARER` pasaron de `NOT_SET` a `SET` y quedaron persistidas en daedalus; smoke funcional posterior al restart queda pendiente de nueva evidencia.
- Ningún valor de bearer/password/private key fue persistido en documentación.
