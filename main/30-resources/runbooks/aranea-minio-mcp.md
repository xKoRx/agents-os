# Runbook — aranea-minio-mcp (`aranea-minio-rw`)

Creado: 2026-09-17 (Parte 2 mcp-trio). Estado: **ACTIVE/RW** — identidad = key owner FULL; server certificado 2026-09-17 (como `-ro`) y **recertificado RW 2026-09-18 noche** (put/delete reales 4/4 + smoke chain kor 6/6). **Rename oficial 2026-09-18 noche: `aranea-minio-ro` → `aranea-minio-rw`** — el nombre viejo es histórico en toda la documentación.

## Identidad

| Campo | Valor |
|---|---|
| Capability | **`aranea-minio-rw`** (ex `aranea-minio-ro`; rename 2026-09-18 noche por decisión owner) |
| Endpoint plane | `http://mcps.lab.aranea.cl:3011/mcp` |
| Host | LXC `mcps` (192.168.31.219) |
| Upstream | `txn2/mcp-s3` v1.4.0 (ghcr digest `09371acaca20…`, binario Go stdio) |
| Backend | `minio-mcp-rw` — imagen `local/minio-mcp-http:1.4.0-mcpproxy6.7.16-g010fix-rw` (mcp-proxy 6.7.16 + g010fix, `MCP_S3_EXT_READONLY=false`) |
| Proxy | `minio-mcp-auth-rw` — nginx `5616878291a2…`, :3011→8080, bearer file `daedalus-rw.bearer` |
| Red | `mcp-minio` (bridge) |
| S3 target | `http://192.168.31.92:9000` (path-style, region us-east-1) |
| Build tree | `/opt/mcp/minio/build-rw/` (delta vs `build-ro/` = sólo `MCP_S3_EXT_READONLY=false`; fix `8436c653…` byte-idéntico) |

## Identidad upstream (crítica — CAMBIADA 2026-09-18 noche, decisión owner)

- **La identidad es la access key FULL del owner** (lectura y escritura, TODOS los buckets, incluido `sqx-strategies`). Ya NO es la service account RO con policy embedded.
- Motivo: T21 de E-06 llevaba 4 sesiones bloqueada por el deny IAM de la SA RO; el owner pegó su key en chat (huellas AK sha16 `9b2a3d722ea890f7`, SK sha16 `494893a5136bfafb`) y ordenó configurarla como identidad única del MCP con lectura y escritura. La primera copia pegada resultó `NoSuchAccessKey` (el wizard de creación estaba a medio correr); la segunda ya existía y operó al tiro.
- Cambios aplicados: (1) archivos `runtime/secrets/aws_{access,secret}_key_id` reescritos con la key owner (20/40 bytes exactos, 600, dueño hermes-ops; la identidad RO anterior queda en `work/rollback-secrets-20260918/`); (2) imagen nueva tag `-rw` (delta = sólo la línea READONLY del entrypoint) recreando el backend byte-idéntico en resto (red `mcp-minio`, mounts RO, sin puertos host, `unless-stopped`); (3) **rename** de contenedores (`minio-mcp-rw`, `minio-mcp-auth-rw`), bearer file (`daedalus-rw.bearer`, mismo VALOR que el `-ro` anterior: sha16 `87f18c6637d24139`) y template de proxy (`proxy_pass http://minio-mcp-rw:8000`).
- **Certificación RW 2026-09-18 noche (por el plano, 4/4 exit 0):** `list_buckets` = 12 buckets (todos); metadata del MQ5 de T21 → size 282575 ✓; `put_object` real en `examples` → etag ✓; metadata lee el objeto ✓; `delete_object` → `deleted:true` ✓; HeadObject post-delete → 404 ✓. Cero residuo. Regresión: unauth 401 en :3000–:3012 ✓.
- **T21 desbloqueado con esta identidad:** `t21.mq5` (282575 B, sha `6c598d79…`) y `t21.sqx` (4167219 B, `a5e9b4c1…`) descargados, verificados y entregados en `daedalus:/tmp/t21-artifacts/` (644).
- Rollback de identidad: restaurar los 2 archivos desde `work/rollback-secrets-20260918/` y recrear el backend con el tag `-g010fix` (sin `-rw`).

## Superficie (certificada 2026-09-17; RW desde 2026-09-18 noche)

9 tools (`MCP_S3_EXT_READONLY=false`): `s3_list_buckets` (todos los buckets reales), `s3_list_objects`, `s3_get_object`, `s3_get_object_metadata`, `s3_presign_url`, `s3_list_connections`, `s3_copy_object`/`s3_delete_object`/`s3_put_object` (**operativos** con la key owner full; certificados con put/delete real en `examples` 2026-09-18 noche).

## Health / verificación

- `docker ps --filter name=minio-mcp` → ambos Up (`minio-mcp-rw`, `minio-mcp-auth-rw`).
- unauth POST :3011/mcp → 401.
- Smoke server: init+tools/list+list_buckets vía mcp-smoke.py con bearer `< /opt/mcp/minio/runtime/proxy-secrets/daedalus-rw.bearer`.
- Smoke consumer: entry **`aranea-minio-rw`** de `~/.cursor/mcp.json` con `${env:ARANEA_MINIO_MCP_RW_BEARER}` (renombrada 2026-09-18 noche; smoke funcional RW 6/6 vía chain kor).
- Histórico 2026-09-18: cert funcional 3 consumidores como `-ro` (get real 477 B, mutaciones bloqueadas, 403 IAM demostrado en `sqx-strategies`); verificación post-T21 (4×403 = deny IAM correcto de la SA, plano nunca caído); concesión puntual A+B stageada en `/opt/mcp/minio/work/` (**SUPERSEDED** — nunca aplicada; la key full del owner resolvió el fetch directo).

## Consumidores (Daedalus, estado 2026-09-18 noche)

- **Cursor**: entry `aranea-minio-rw` aplicada (var `ARANEA_MINIO_MCP_RW_BEARER`; bearer sin cambio de valor; smoke 6/6).
- **ZCode/Codex**: rename **pendiente del patcher kor** stageado en `daedalus:/tmp/minio-rw-rename-zcode-codex.py` (sha256 `d7c64f17…`, self-test 6/6: happy/idempotente/4 aborts fail-closed, sin leaks; el owner lo corre como kor). Chain kor: var `ARANEA_MINIO_MCP_RW_BEARER` YA activa (archivo `hermes-managed/minio-mcp-rw.bearer`, valor idéntico al `-ro`; bloque `-ro` removido con backup).

## Rollback

`docker rm -f minio-mcp-auth-rw minio-mcp-rw && docker network rm mcp-minio && docker rmi local/minio-mcp-http:1.4.0-mcpproxy6.7.16-g010fix-rw && rm -rf /opt/mcp/minio`; consumer: restore backups (patrón `.bak-miniorw-*` junto a cada config; chain/cursor en `/tmp/mcp-minio-align3-*`) + rm bearer kor.

## Deudas

- Ejecutar el patcher kor para ZCode/Codex (entry renames); hasta entonces esos clientes pueden seguir usando la entry `-ro` con el MISMO bearer (funciona: mismo endpoint/proxy) o referenciar la var RW ya activa en el chain.
- SA huérfana deny-all (hija de `mcp`) sin poder borrarse sin admin → owner.
- Rotación de la key owner usada como identidad = decisión owner (invalidaría la capability completa hasta re-swap).
