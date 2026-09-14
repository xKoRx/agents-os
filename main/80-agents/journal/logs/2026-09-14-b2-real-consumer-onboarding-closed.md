---
type: change_log
schema_version: 1
scope: session
created: "2026-09-14"
updated: "2026-09-14"
area: "[[Aranea]]"
project: "[[HERMES — Bootstrap & Self-Sufficiency]]"
entities:
  - "[[HERMES — Bootstrap & Self-Sufficiency]]"
  - "[[AGENT-PLATFORM - MCP Access Plane]]"
related:
  - "[[mcp-access-plane-operations]]"
aliases: []
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
---

# 2026-09-14-b2-real-consumer-onboarding-closed

%% Routing: area/project/entities/related usan links canónicos. %%

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `10-projects/Aranea/agentes/HERMES — Bootstrap & Self-Sufficiency.md` (updated: estado B2 corregido a PASS real con consumer Daedalus/Cursor; bitácora; tareas B2.1–B2.5)
  - `30-resources/runbooks/aranea-mcp-capability-plane.md` (updated: sección Consumer onboarding managed)
  - `80-agents/journal/feedback/system-1/2026-09-14-hermes-b2-session-feedback.md` (created)

## Motivo

- Cerrar B2 (consumer onboarding path) sobre un consumer REAL de Echo/Forge: Daedalus/Cursor (`kor@daedalus.lab.aranea.cl`, 192.168.31.161). El estado previo marcaba B2 PASS con sólo el harness Hermes-VM (insuficiente).

## Fuentes usadas

- Authority nueva: usuario `hermes-ops` en Daedalus (key-only, password locked, sin sudo) + ACLs scoped sobre `/home/kor/.cursor/mcp.json`, `/home/kor/.config/mcp/`, `/home/kor/.config/aranea/secrets/hermes-managed/` (OWNER ACTION BUNDLE `daedalus-hermes-ops-seed` aplicado por el owner, con validación de fingerprint pre/post).
- Config consumer real leída desde Daedalus: `/home/kor/.cursor/mcp.json` (10 servers, cero bearer literal, todo `${env:VAR}`) + chain KDE `~/.config/plasma-workspace/env/aranea-mcp.sh` → `~/.config/mcp/aranea-env.sh` (secret files 0600 de kor, inaccesibles para hermes-ops — least privilege respetado).

## Resolución aplicada

- Onboarding autónomo: entry `aranea-postgres-ro-hermes-managed` añadida in-place a `mcp.json` (edit r+ vía ACL, preserva owner kor y modo 660), clonando la entry `aranea-postgres-ro` existente y su referencia `${env:ARANEA_POSTGRES_MCP_RO_BEARER}` (cero duplicación de bearer, cero mutación del plane).
- Consumer smoke desde Daedalus resolviendo la config real del consumer: initialize PASS (postgres-mcp 1.25.0; requiere `clientInfo.version` — su validación es estricta), tools/list PASS (9 tools), tools/call `list_schemas` PASS con schema `echo` visible. Bearer sólo por stdin en memoria (copia verificada sha256 5416e5d2… del `daedalus-ro.bearer` server-side).
- Rollback demostrado: `remove` → sha256 byte-identical contra backup pre-cambio → re-add → re-smoke PASS.
- Operator durable en `~kor/.config/aranea/secrets/hermes-managed/bin/`: `mcp-onboard.py` (add/remove/status), `consumer-smoke.py`, backups con sha-pre.

## Validación

- Login `hermes-ops@daedalus` key-only PASS; host key pinneada `SHA256:IkEaqcpWKCwekKd4SrxRAZXxPGRVDBaScHLJSN02JRA` (alias `daedalus-ops`).
- Rollback: diff vacío, sha `ebd63a34…` restaurado exacto.
- Secrets: `grep` literal bearers en `mcp.json` = 0; ninguna impresión en chat/vault; `aranea-env.sh` accedido sólo vía backup byte-idéntico (el original de kor no requiere ACL para hermes-ops).
- Verificación post-bundle de boundaries: `hermes-ops` NO puede leer secrets existentes de kor (denegado, correcto); sólo `hermes-managed/` es su área.

## Compartibilidad

- Patrón B2 replicable para próximas capabilities: 2 pasos autónomos (edit `mcp.json` via ACL + smoke) sin intervención owner; alta de un NUEVO bearer server-side sigue requeriría `mcps-ops` (también autónomo).
