---
type: change_log
schema_version: 1
status: final
date: 2026-09-15
project: "[[HERMES — Bootstrap & Self-Sufficiency]]"
area: "[[Aranea]]"
tags:
  - kind/change-log
  - area/aranea
  - tech/mcp
---

# change_log 2026-09-15 — B3.3 `aranea-observability-ro` intento BLOCKED (credencial Grafana)

## Objetivo

Golden deploy/config B3.3: materializar y certificar `aranea-observability-ro` sobre el stack ARGUS existente usando `aranea-mcp-plane-operator` + management path `mcps-ops`.

## Evidencia recolectada (sesión)

- **Upstream verificado (PINNED):** `grafana/mcp-grafana` release `v1.4.2` (GitHub, publicada 2026-09-14T16:14:13Z, no draft/prerelease), commit `b56dceea39c7bff3b97aa32fcb8a3103cc0ca119`. Imagen oficial Docker Hub `grafana/mcp-grafana:1.4.2`: índice `sha256:f87fa67a561f7b3deb412402887117bd1e9f1f7a8695935d27c498543ab3458b`, amd64 `sha256:9a10fd78b359512226d3d9a3bc9f58774a5eb1613954e5cf7fd089b0fc4d4cf9`, arm64 `sha256:b35e3ffb205aea2da5af154f4b8bb4530a2e63e3b6da3cbd5e15078e8c37b4d9`. Sintaxis 1.4.2 confirmada en source: `--transport streamable-http`, `--endpoint-path /mcp`, `--disable-write`, `--enabled-tools` (allowlist), `--enable-query` = SQL crudo (queda prohibido). Soporte `GRAFANA_SERVICE_ACCOUNT_TOKEN_FILE` verificado en `pkg/mcpgrafana/mcpgrafana.go`.
- **Target proof ARGUS real:** VM `argus` = qemu/160 (hades) en `192.168.31.60`. Grafana `12.1.1` healthy (`/api/health` 200, database ok; `/api/search` sin auth → 401, token requerido). Prometheus ready 200 con `up` real (otelcol/node_exporter/prometheus). Loki ready con labels reales (`filename,host,job,level,service_name,unit`).
- **Baseline plane:** 9 capabilities vivas, puertos 3000–3008 ocupados según contrato; **3009 libre** (demostrado `docker ps` + `ss -lntp`).
- **Credencial:** no existe credencial Grafana read-only en `/opt/mcp` (búsqueda por nombre sin hits), en el canal de secretos de Hermes (0 hits) ni en la chain de secrets de Daedalus (`aranea-env.sh` / `mcp.json`, 0 hits). Crear una SA Viewer en Grafana excede la autoridad vigente de Hermes.

## Cambios ejecutados (AUTO, idempotentes, sin impacto en capabilities existentes)

- `mcps`: creados `/opt/mcp/observability/runtime/{proxy,proxy-secrets,secrets}` (root, mêmes conventions del plane).
- `mcps`: creada red Docker `mcp-observability` (`--internal`).

## Veredicto

`B3.3 BLOCKED` — falta únicamente la credencial Grafana read-only (service account token Viewer). Emitido UN `OWNER ACTION BUNDLE` (sesión 2026-09-15). No se deployó backend ni proxy, no se publicó consumer, no se cerró B3.3.

## Rollback

- `mcps`: `sudo docker network rm mcp-observability` + `sudo rm -rf /opt/mcp/observability` (sin contenedores creados; cero residuo).
- Bundle del owner: revocar el token en Grafana UI y `rm` el archivo de secret.

## Fuentes actualizadas

- `[[HERMES — Bootstrap & Self-Sufficiency]]` — bitácora 2026-09-15 (intento B3.3 + blocker).
- `[[AGENT-PLATFORM - MCP Access Plane]]` — bitácora 2026-09-15 (pre-staging + estado OBS3).
