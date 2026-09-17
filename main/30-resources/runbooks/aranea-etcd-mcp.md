# Runbook — aranea-etcd-mcp (`aranea-etcd-ro`)

Creado: 2026-09-17 (Parte 2 mcp-trio). Estado: ACTIVE (server + Cursor certificados; ZCode/Codex vía patcher kor).

## Identidad

| Campo | Valor |
|---|---|
| Capability | `aranea-etcd-ro` |
| Endpoint plane | `http://mcps.lab.aranea.cl:3012/mcp` |
| Host | LXC `mcps` (192.168.31.219) |
| Upstream | greenfield FastMCP 2.12.4 (mandato owner 2026-09-17 §3; no existe upstream mantenible — ver reconciliación `~/aranea/work/mcp-trio/etcd-reconciliation.md`) |
| Backend | `etcd-mcp-ro` — imagen `local/etcd-mcp-ro:0.1.0` (HTTP streamable nativo :8000, sin mcp-proxy) |
| Proxy | `etcd-mcp-auth-ro` — nginx `5616878291a2…`, :3012→8080 |
| Red | `mcp-etcd` (bridge) |
| Cluster | 5 members `192.168.31.250-.254` (gateway v3 JSON `/v3/kv/range`, failover, timeout 3s) |
| Build tree | `/opt/mcp/etcd/build-ro/` (Dockerfile `56df4cb9…`, etcd_gateway.py `b464a315…`+fix count int, poc `etcd_poc.py`) |

## Contrato de seguridad (verificado, no asumido)

- **Deny-by-default**: solo 8 prefixes allowlist (`/echo/ /sqx-worker/ /sqx-flowkit/ /sqx-watcher/ /sqx-mt5-worker/ /deployer-watcher/ /deployer/ /symphony/`); branch `/deployer-watcher/development/minio` excluida; regex de nombres-secretos (`password|secret|token|access_key|api_key|credential|private_key|*.pem|*.crt|*.key`, case-insensitive) excluye keys en TODAS las rutas (get, list results).
- **Sin mutadores ni watch**; `etcd_get_value` capped 4KB; `etcd_list_keys` keys_only cap 200; count metadata-only.
- **El cluster NO fue escrito ni configurado** (deploy = solo plano MCP; los probes son lecturas `/v3/kv/range`). El cluster sigue sin auth — hardening = workstream `ETCD-HARDENING` (owner-gated).

## Superficie (certificada 2026-09-17, 13/13)

`etcd_list_prefixes`, `etcd_count_keys`, `etcd_list_keys`, `etcd_get_value`. serverInfo `aranea-etcd-ro 1.30.0`. Semántica streamable: initialize con id y SIN session-id header; sid desconocido → 404; notificaciones → 202.

## Health / verificación

- `docker ps --filter name=etcd-mcp` → ambos Up; unauth POST :3012/mcp → 401.
- Probe real: `etcd_count_keys /echo/` → 75; `etcd_get_value /deployer-watcher/development/service/version` → `0.1.0`.
- Negativos: `/demo/`, `/minio-example/` → prefix not in allowlist; keys secret-named → denied.

## Rollback

`docker rm -f etcd-mcp-auth-ro etcd-mcp-ro && docker network rm mcp-etcd && docker rmi local/etcd-mcp-ro:0.1.0 && rm -rf /opt/mcp/etcd`; consumer: restore backups + rm bearer kor. Cluster etcd: sin cambios (nada que revertir).

## Deuda conocida

El gateway expone SOLO lo allowlisted, pero el cluster subyacente sigue plano (sin TLS/auth): la contención de red (OPNsense/PVE) y el hardening son prerrequisitos de cualquier exposición futura más amplia. Ver `ETCD-HARDENING`.
