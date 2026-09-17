# Runbook — aranea-minio-mcp (`aranea-minio-ro`)

Creado: 2026-09-17 (Parte 2 mcp-trio). Estado: ACTIVE (server + Cursor certificados; ZCode/Codex vía patcher kor).

## Identidad

| Campo | Valor |
|---|---|
| Capability | `aranea-minio-ro` |
| Endpoint plane | `http://mcps.lab.aranea.cl:3011/mcp` |
| Host | LXC `mcps` (192.168.31.219) |
| Upstream | `txn2/mcp-s3` v1.4.0 (ghcr digest `09371acaca20…`, binario Go stdio) |
| Backend | `minio-mcp-ro` — imagen `local/minio-mcp-http:1.4.0-mcpproxy6.7.16-g010fix` (mcp-proxy 6.7.16 + g010fix) |
| Proxy | `minio-mcp-auth-ro` — nginx `5616878291a2…`, :3011→8080 |
| Red | `mcp-minio` (bridge) |
| S3 target | `http://192.168.31.92:9000` (path-style, region us-east-1) |
| Build tree | `/opt/mcp/minio/build-ro/` (Dockerfile `f52115e5…`, entrypoint `23a992ff…`, fix `8436c653…`) |

## Identidad upstream (crítico)

- NO es admin. Es una **service account MinIO hija de la access key owner** (creada por self-service `svcacct add` con policy embedded).
- Permisos efectivos = intersección (padre ∩ policy embedded) = `deploy` (ListBucket) + `deploy/worker/sqx/*` (Get) + `examples` (List+Get); DENY explícito `*backup*`; todo lo demás denegado.
- Policy canónica: `~/aranea/work/mcp-trio/minio-mcp-ro-policy.json` (hermes-vm).
- Creds S3 en `/opt/mcp/minio/runtime/secrets/aws_{access,secret}_key_id` (600, uid 1000); el entrypoint las exporta a env.

## Superficie (certificada 2026-09-17)

9 tools, RO ext (`MCP_S3_EXT_READONLY=true`): `s3_list_buckets` (solo deploy+examples por IAM), `s3_list_objects`, `s3_get_object`, `s3_get_object_metadata`, `s3_presign_url`, `s3_list_connections`, `s3_copy_object`/`s3_delete_object`/`s3_put_object` (presentes pero bloqueados: "server is in read-only mode").

## Health / verificación

- `docker ps --filter name=minio-mcp` → ambos Up.
- unauth POST :3011/mcp → 401.
- Smoke server: certificador `minio-cert.py` (workspace sesión) o init+tools/list+list_buckets vía mcp-smoke.py con bearer `< /opt/mcp/minio/runtime/proxy-secrets/daedalus-ro.bearer`.
- Smoke consumer: entry `aranea-minio-ro` de `~/.cursor/mcp.json` con `${env:ARANEA_MINIO_MCP_RO_BEARER}`.

## Rollback

`docker rm -f minio-mcp-auth-ro minio-mcp-ro && docker network rm mcp-minio && docker rmi local/minio-mcp-http:1.4.0-mcpproxy6.7.16-g010fix && rm -rf /opt/mcp/minio`; consumer: restore backups mcp.json/aranea-env.sh (hermes-managed) + rm bearer kor. La SA MinIO requiere admin para borrar (owner).

## Deudas

- SA huérfana deny-all (hija de `mcp`) sin poder borrarse sin admin → owner.
- Rotación de la key owner `zaLm…` = decisión owner (invalidaría la SA hija).
