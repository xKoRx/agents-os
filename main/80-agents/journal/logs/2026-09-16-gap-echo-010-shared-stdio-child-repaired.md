---
type: change_log
schema_version: 1
created: 2026-09-16
area: "[[Aranea]]"
project: "[[AGENT-PLATFORM - MCP Access Plane]]"
tags:
  - kind/change-log
  - area/aranea
  - tech/mcp
---

# change_log 2026-09-16 — GAP-ECHO-010 reparado y certificado

## Objetivo

Diagnosticar GAP-ECHO-010 (respuestas 202 sin `Mcp-Session-Id` / calls posteriores fallando en los proxies nginx-wrapped del access plane) y, con causa demostrada, aplicar la corrección mínima; certificar server-side y desde Daedalus.

## ROOT_CAUSE: PROVEN

**Componente:** `mcp-proxy` 6.7.16 (npm punkpeye) dentro de las imágenes http-wrapper (`local/hasura-mcp-http:*-mcpproxy6.7.16*`).

**Mecanismo (evidencia en código + reproducción viva en `hasura-mcp-dev-admin`):**

1. El CLI spawnea UN hijo stdio (`/app/hasura-mcp-server`) al arranque y crea UN `Client` MCP compartido; TODAS las sesiones HTTP multiplexan sobre ese único hijo (`connect()`/`createServer()` en `dist/bin/mcp-proxy.mjs`).
2. Si el hijo muere (crash p.ej. respuesta gigante M5 `get_schema` ~11 MB, kill -9, OOM), `StdioClientTransport._emitClose()` marca `_process=undefined` y NO existe lógica de respawn.
3. Las entradas de sesión quedan vivas en `activeTransports`; `initialize` se responde localmente con metadata cacheada del handshake de arranque ⇒ 200+sid "sano" mientras TODO `tools/list`/`tools/call` responde `-32603 Not connected` — indefinidamente, hasta `docker restart`. Ese "initialize OK + calls fail" es el patrón operativo GAP-ECHO-010.
4. Mapeo de errores (reproducido y confirmado contra el stack real): `-32603 Not connected` = sesión cuyo hijo murió; `-32001 Session not found` = sid inexistente/reapado(30 min idle)/DELETE; `-32000` = sin header sid; los `202 Accepted` sin sid corresponden a mensajes id-less (notificaciones) del transporte, no a `initialize` requests (que de este stack sólo pueden salir 200+sid o 4xx/5xx).
5. NO compartían esa causa: `ssh-mcp` (pool-64 propio, quirk documentado) y `flink-mcp-dev-admin` (SDK Java con servlet HTTP propio; logs del incidente muestran initializes procesándose y cero errores de sesión).

## Reparación (mínima, aplicada)

- Patcher determinista `fix-shared-child.mjs` (marca `[g010] upstream stdio`, fail-closed ante drift, idempotente, con `node --check` pre-install) que modifica el bundle del CLI: trackea `transport.onclose` y respawnea+reconecta el upstream en el próximo `createServer`. Sesiones ligadas al hijo muerto siguen fallando `-32603` (semántica correcta); cualquier `initialize` nuevo se recupera SIN restart del container.
- Artefactos versionados: `/opt/mcp/hasura/http-wrapper/{fix-shared-child.mjs,Dockerfile}` y `/opt/mcp/hasura/build-prod-ro/{fix-shared-child.mjs,Dockerfile}` (shas: fix `9d6b5520…`, Dockerfile dev `974513af…`, Dockerfile prod-ro `185448df…`; backups pre-cambio `/tmp/Dockerfile.http.pre-g010`, `/tmp/Dockerfile.prod-ro.pre-g010`).
- Imágenes nuevas (tags certificados intactos = rollback):
  - `local/hasura-mcp-http:1.0.0-9ba59f2-mcpproxy6.7.16-g010fix` (dev)
  - `local/hasura-mcp-http:1.0.0-9ba59f2-prod-ro-h1fix-mcpproxy6.7.16-g010fix` (prod-ro)
- Containers recreados con mounts/env/red/policy idénticos al baseline; resto del plane sin drift (verificado contra inventario D0).

## Verificación del fix (condición de reproducción)

Dev `:3006` y prod-ro `:3005`: kill -9 del hijo stdio ⇒ `tools/list` en sesión vieja `-32603` (esperado) ⇒ **`initialize` fresco 200+sid ⇒ `tools/list`/`tools/call` OK sin restart** (antes: permanentemente `-32603` hasta `docker restart`).

## Certificación

- Server-side (mcps, bearer stdin): dev 50/50 ciclos `initialize→tools/list→get_version→DELETE` PASS (`init_ok=50 list_ok=50 call_ok=50 del_ok=50 fails=0`); prod-ro 30/30 PASS.
- Consumer (Daedalus real, vía `mcps.lab.aranea.cl`, mecanismo HTTP equivalente al SDK de los agentes): dev 50/50 PASS (`tools=9`), prod-ro 30/30 PASS (`tools=3`). `CONSUMER_DAEDALUS_PASS`. No hay un agente Echo/Forge identificable como consumidor bloqueado en este momento ⇒ `DEVELOPER_UNBLOCKED: NOT_PROVEN` (a nivel de plane, el mecanismo de consumo quedó desbloqueado).
- Regresión: 401 unauth en 3001-3009; superficie DEV = 9 tools (sin cambios); superficie PROD-RO = exactamente `get_inconsistent_metadata, get_schema, get_version` (H1 intacto, `export_metadata` ausente); H2 intacto (`run-command` en `mt5-kronos` ⇒ `POLICY_DENIED`); ssh-mcp/flink/kafka/mongo/pg/observability sin drift de imagen/puerto/mounts.

## Rollback

Recrear cada container con el tag anterior retenido (`…-mcpproxy6.7.16` y `…-h1fix-mcpproxy6.7.16`), mounts/env/red idénticos; restaurar Dockerfiles desde backups `/tmp` con sha; verificado que los tags viejos siguen presentes.

## Deuda residual material

- `flink-mcp-dev-admin` (Java SDK) y `ssh-mcp` (pool-64) tienen stacks de transporte distintos; no se les aplicó el fix (causa no compartida). Si muestran síntomas de sesión colgante, requieren diagnóstico propio.
- El fix es a nivel bundle del CLI (patch determinista en build). Considerar propuesta upstream/actualización de mcp-proxy sólo con certificación completa (fuera de scope de este workload).
- Residuos temporales limpiados en mcps/Daedalus/local; parche durable vive en los build trees versionados.

## Fuentes

- Nota de certificación: `10-projects/Aranea/AGENT-PLATFORM/agentes/workstreams/ACCESS-CERTIFICATION.md` (sección GAP-ECHO-010).
- Skill de mecánica: `mcp-access-plane-operations` (gotcha GAP-ECHO-010 actualizado).
