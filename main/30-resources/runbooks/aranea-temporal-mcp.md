---
type: runbook
schema_version: 1
scope: area
created: "2026-09-17"
updated: "2026-09-17"
area: "[[Aranea]]"
project: "[[AGENT-PLATFORM - MCP Access Plane]]"
application:
entities:
  - "[[Aranea]]"
related:
  - "[[AGENT-PLATFORM - MCP Access Plane - Architecture]]"
  - "[[aranea-mcps-expert]]"
  - "[[aranea-mcp-capability-plane]]"
  - "[[AGENT-PLATFORM - MCP Access Plane]]"
aliases:
  - runbook temporal MCP Aranea
  - aranea temporal mcp
confidence: verified
load_policy: manual
indexable: true
index_priority: high
tags:
  - kind/runbook
  - scope/area
  - area/aranea
  - tech/mcp
  - tech/temporal
  - action/mcp-plane
---

# aranea-temporal-mcp

## Propósito

Operar la capability `aranea-temporal-ro` del MCP Access Plane: superficie, boundaries, diagnóstico y rollback. Routing agent-facing en [[aranea-mcps-expert]]; arquitectura transversal en [[AGENT-PLATFORM - MCP Access Plane - Architecture]].

## Identidad

```text
capability:  aranea-temporal-ro
endpoint:    http://mcps.lab.aranea.cl:3010/mcp
authority:   PROD-RO estricta (hardReadOnly por diseño + allowedNamespaces)
target:      Temporal Server 1.31.2 — frontend gRPC 192.168.31.46:7233 (VM temporal, VMID 158, PTR temporal.aranea.local)
namespaces:  sqx-dev, sqx, sqx-prop (allowlist); temporal-system BLOQUEADO server-side
upstream:    stevekinney/temporal-mcp npm 0.2.1 (28 tools read-only por diseño; stdio-only)
wrapper:     mcp-proxy 6.7.16 + fix GAP-ECHO-010 (respawn shared-child), patrón familia hasura
imagen:      local/temporal-mcp-http:0.2.1-mcpproxy6.7.16-g010fix (sha256 038eef5c1d56…)
backend:     container temporal-mcp-ro, red mcp-temporal, user 1000:1000, SIN host port
proxy:       container temporal-mcp-auth-ro, nginx digest canónico 5616878291a2…, publica :3010->8080
secretos:    /opt/mcp/temporal/runtime/proxy-secrets/daedalus-ro.bearer (bearer cliente→proxy, 640 root)
config:      /opt/mcp/temporal/runtime/config/temporal-mcp.json (address :7233, hardReadOnly, allowedNamespaces) — mount ro en /run/config/
build tree:  /opt/mcp/temporal/build-ro/ (Dockerfile sha 9c66bda8…, entrypoint 0a24e76a…, fix-shared-child 8436c653… = byte-identical al de hasura)
consumer:    Cursor/Daedalus entry aranea-temporal-ro → ${env:ARANEA_TEMPORAL_MCP_RO_BEARER}; chain ~/.config/mcp/aranea-env.sh lee /home/kor/.config/aranea/secrets/hermes-managed/temporal-mcp-ro.bearer (640 hermes-ops + ACL u:kor:r--, sha16 a081349e3ac1b36b)
```

## Superficie certificada (exactamente 28 tools, 2026-09-17)

Cero mutadores: `start/signal/cancel/terminate/reset/delete/pause/trigger/batch/execute` NO existen en `tools/list`. Un `tools/call` con un nombre de mutación responde `-32602 Tool not found` (negativo verificado con `temporal.workflow.start`).

```text
temporal.workflow.list / describe / count / result / query / history / history.reverse / history.summarize
temporal.schedule.list / describe / matching-times
temporal.task-queue.describe / configuration
temporal.namespace.list / describe        (describe exige namespace en allowlist → si no: NAMESPACE_NOT_ALLOWED)
temporal.search-attributes.list
temporal.cluster.info
temporal.worker.versioning-rules / task-reachability / deployment.list / deployment.describe / deployment.version.describe / deployment.reachability
temporal.connection.check
docs.status / docs.search / docs.get / docs.refresh
```

Nota: `docs.refresh` tiene side effects LOCALES (git sync + cache en `~/.temporal-mcp` del container efímero de sesión stdio); no muta Temporal. `temporal.workflow.query` ejecuta un query handler de un workflow en ejecución — es lectura, no mutación, pero acotar al workflow exacto.

## Boundary del target

- La conexión del backend es gRPC al frontend `:7233`. La UI/API HTTP `:8080` (ruta Traefik `temporal.lab.aranea`) NO sirve gRPC del MCP: si el config apunta a `:8080` el profile reporta `Failed to connect before the deadline` aunque TCP/HTTP2 a ese puerto pasen.
- Sin TLS ni API key en el frontend interno (LAN). El boundary agent-facing es EXCLUSIVAMENTE bearer del proxy + hardReadOnly + allowlist de namespaces.
- Cluster temporal corre namespaces SQX (dev de estrategias). Tratar `temporal-system` como interno: está bloqueado por allowlist.

## Smoke server-side (canónico)

```bash
# 401 sin bearer:
curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:3010/mcp   # → 401
# Ciclo completo con el template de skill (bearer por stdin, Accept SSE obligatorio):
sudo -n bash -c 'python3 /tmp/mcp-smoke.py http://127.0.0.1:3010/mcp \
  < /opt/mcp/temporal/runtime/proxy-secrets/daedalus-ro.bearer'
```

mcp-proxy 6.7.16: POST sin `Content-Type: application/json` → 400; sin `Accept: application/json, text/event-stream` → 406. El smoke template ya lleva ambos headers.

## Consumer smoke (Cursor/Daedalus)

Patrón B2: resolver `/home/kor/.cursor/mcp.json` entry `aranea-temporal-ro`, interpolar `${env:ARANEA_TEMPORAL_MCP_RO_BEARER}`, bearer por stdin desde `mcps-ops 'sudo -n cat …bearer'` pipe a `ssh daedalus-ops 'python3 <smoke>.py'` — script de referencia en `~/aranea/work/mcp-trio/temporal-consumer-smoke.py` (hermes-vm). PASS = initialize + tools/list 28 + `temporal.namespace.list` devolviendo los 4 namespaces reales. Un Cursor ya corriendo NO re-absorbe la env var nueva sin restart del cliente (quirk conocido del chain KDE).

## Rollback

1. Entry Cursor: `mcp.json.bak-temporal-<ts>` en `hermes-managed/` (restaurar byte-identical).
2. Chain kor: `aranea-env.sh.bak-temporal-<ts>` en `hermes-managed/` (restaurar; `bash -n` después).
3. Bearer kor: `rm /home/kor/.config/aranea/secrets/hermes-managed/temporal-mcp-ro.bearer`.
4. Plane: `docker rm -f temporal-mcp-auth-ro temporal-mcp-ro && docker network rm mcp-temporal` (+ opcional `docker rmi local/temporal-mcp-http:0.2.1-…`). `/opt/mcp/temporal/` puede quedarse (inerte) o eliminarse.
5. Post-verificación de no-regresión: probes 401 en `:3001–:3010` y `:3000/` (ssh-mcp sirve en `/`, no `/mcp`).

## Gotchas de esta familia

- El entrypoint del wrapper espera el config en `/run/config/temporal-mcp.json` vía env `TEMPORAL_MCP_CONFIG` — el mount es read-only y obligatorio.
- El fix g010 del wrapper es byte-identical al de hasura; tras cualquier rebuild, verificar `node --check` en build y el marker `[g010]` dentro de la imagen.
- Reiniciar `temporal-mcp-ro` NO afecta sesiones de otras familias (red dedicada `mcp-temporal`).
- Las credentials/secretos del cluster Temporal no intervienen: el backend no usa API key (frontend interno sin auth); NO habilitar mutación vía `TEMPORAL_MCP_BREAK_GLASS` — está fuera de contrato y detrás de allowlist namespaces igual quedaría bloqueado por `hardReadOnly`.
