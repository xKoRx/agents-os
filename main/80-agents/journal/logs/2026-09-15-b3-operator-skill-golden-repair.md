---
type: change_log
schema_version: 1
scope: session
created: "2026-09-15"
updated: "2026-09-15"
area: "[[Aranea]]"
project: "[[HERMES — Bootstrap & Self-Sufficiency]]"
application:
entities:
  - "[[HERMES — Bootstrap & Self-Sufficiency]]"
  - "[[AGENT-PLATFORM - MCP Access Plane]]"
related:
  - "[[aranea-mcp-plane-operator]]"
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

# 2026-09-15-b3-operator-skill-golden-repair

%% Routing: area/project/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** created
- **Archivo(s):**
  - `30-resources/agents/skills/aranea-mcp-plane-operator/SKILL.md` (created: operador reusable del MCP plane vía management path nativo)
  - `10-projects/Aranea/agentes/HERMES — Bootstrap & Self-Sufficiency.md` (updated: B3.1/B3.2 PASS, bitácora, tarea B3.4 parcialmente cubierta — SoT no requirió cambios canónicos)

## Motivo

- B3.1: materializar el operador MCP reusable sin duplicar [[aranea-mcps-expert]] (que permanece consumer-facing) ni los runbooks de familia.
- B3.2: demostrar golden self-repair end-to-end sobre una capability DEV real, con consumer smoke desde el consumer real (Daedalus), sin intervención owner.

## Fuentes usadas

- Runtime real de `mcps` vía `~/aranea/bin/mcps-ops` (docker inspect/ps, ss, templates de proxy).
- `[[AGENT-PLATFORM - MCP Access Plane - Architecture]]` (topología, Gate D, pinning).
- Runbook `aranea-postgres-mcp` (contrato DEV RW: `mcp_echo_dev_rw`/`echo-develop`).
- Consumer real: `/home/kor/.cursor/mcp.json` entry `aranea-postgres-rw` (ref `${env:ARANEA_POSTGRES_MCP_RW_BEARER}`).

## Resolución aplicada

- Skill `aranea-mcp-plane-operator` creada bajo `30-resources/agents/skills/` (skill de área, no ejecutable duplicado): target/clase → baseline → backup mínimo → intervención creciente (restart→recreate) → runtime health → server smoke → consumer smoke → post-condición/drift → rollback → update de SoT.
- Golden repair ejecutado sobre `aranea-postgres-rw` (DEV, :3002; backend `postgres-mcp-echo-dev-rw` + proxy `postgres-mcp-auth-rw`): baseline completo (digests `6c605ca4…` backend, `56168782…` proxy, template sha `f9a5051e…`, server smoke PASS previo), `docker restart` controlado del backend, health 401 unauth, server smoke POST PASS (postgres-mcp 1.25.0, 9 tools), consumer smoke real desde Daedalus PASS (initialize + tools/list 9 + tools/call `list_schemas`), recovery stop/start re-verificado (server + consumer smoke PASS post-recovery), drift cero (digests, mounts, ports, template sha idénticos), artefactos temporales eliminados en `mcps` y Daedalus.

## Validación

- `validate_schema_contract.py --type skill`: errors=0.
- `lint.py --strict` sobre la SKILL.md nueva: ERROR=0 WARN=0.
- Golden repair: ver Resolución; cero secretos impresos (bearer sólo stdin), cero edición owner, ningún MCP de `mcps` usado como management path.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Skill: eliminar `30-resources/agents/skills/aranea-mcp-plane-operator/` y revertir el estado B3 en la nota del proyecto. Runtime: sin cambios persistentes (restart de container DEV que arrancó y quedó healthy; config sin modificar).
