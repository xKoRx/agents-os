# Runbook — aranea-minio-mcp (`aranea-minio-ro`)

Creado: 2026-09-17 (Parte 2 mcp-trio). Estado: ACTIVE (server + Cursor certificados 2026-09-17; certificación funcional completa 3 consumidores 2026-09-18).

## Identidad

| Campo | Valor |
|---|---|
| Capability | `aranea-minio-ro` (nombre histórico; desde 2026-09-18 noche opera **RW** por decisión owner) |
| Endpoint plane | `http://mcps.lab.aranea.cl:3011/mcp` |
| Host | LXC `mcps` (192.168.31.219) |
| Upstream | `txn2/mcp-s3` v1.4.0 (ghcr digest `09371acaca20…`, binario Go stdio) |
| Backend | `minio-mcp-ro` — imagen `local/minio-mcp-http:1.4.0-mcpproxy6.7.16-g010fix` (mcp-proxy 6.7.16 + g010fix) |
| Proxy | `minio-mcp-auth-ro` — nginx `5616878291a2…`, :3011→8080 |
| Red | `mcp-minio` (bridge) |
| S3 target | `http://192.168.31.92:9000` (path-style, region us-east-1) |
| Build tree | `/opt/mcp/minio/build-ro/` (Dockerfile `f52115e5…`, entrypoint `23a992ff…`, fix `8436c653…`) |

## Identidad upstream (crítico — CAMBIADA 2026-09-18 noche, decisión owner)

- **Desde 2026-09-18 noche la identidad es la access key FULL del owner** (lectura y escritura, todos los buckets, incluido `sqx-strategies`). Ya NO es la service account RO con policy embedded.
- Motivo: T21 de E-06 llevaba 4 sesiones bloqueada por el deny IAM de la SA RO; el owner pegó su key en chat (huellas AK sha16 `9b2a3d722ea890f7`, SK sha16 `494893a5136bfafb`) y ordenó configurarla como identidad única del MCP con lectura y escritura. La primera copia pegada resultó `NoSuchAccessKey` (el wizard de creación estaba a medio correr); la segunda ya existía y operó al tiro.
- Cambios aplicados: (1) archivos `runtime/secrets/aws_{access,secret}_key_id` reescritos con la key owner (20/40 bytes exactos, 600, dueño hermes-ops; la identidad anterior RO queda en `work/rollback-secrets-20260918/`); (2) imagen nueva `local/minio-mcp-http:1.4.0-mcpproxy6.7.16-g010fix-`**`rw`** (build tree `build-rw/`, delta = sólo `MCP_S3_EXT_READONLY=false`; fix g010 byte-idéntico sha `8436c653…`) recreando `minio-mcp-ro` byte-idéntico en resto (red `mcp-minio`, mounts RO, sin puertos host, `unless-stopped`). Proxy y bearer: sin cambios.
- **Certificación RW 2026-09-18 noche (por el plano, 4/4 exit 0):** `list_buckets` = 12 buckets (todos); metadata del MQ5 de T21 → size 282575 ✓; `put_object` real en `examples` → etag ✓; metadata lee el objeto ✓; `delete_object` → `deleted:true` ✓; HeadObject post-delete → 404 ✓. Cero residuo. Regresión: unauth 401 en :3000–:3012 ✓, contenedores Up ✓.
- Rollback: restaurar los 2 archivos desde `work/rollback-secrets-20260918/` y recrear el backend con el tag `-g010fix` (sin `-rw`) — mismo comando de recreate.

## Superficie (certificada 2026-09-17)

9 tools (`MCP_S3_EXT_READONLY=`**`false`** desde 2026-09-18 noche): `s3_list_buckets` (todos los buckets reales), `s3_list_objects`, `s3_get_object`, `s3_get_object_metadata`, `s3_presign_url`, `s3_list_connections`, `s3_copy_object`/`s3_delete_object`/`s3_put_object` (**operativos** con la key owner full; certificados con put/delete real en `examples` 2026-09-18 noche).

## Health / verificación

- `docker ps --filter name=minio-mcp` → ambos Up.
- unauth POST :3011/mcp → 401.
- Smoke server: certificador `minio-cert.py` (workspace sesión) o init+tools/list+list_buckets vía mcp-smoke.py con bearer `< /opt/mcp/minio/runtime/proxy-secrets/daedalus-ro.bearer`.
- Smoke consumer: entry `aranea-minio-ro` de `~/.cursor/mcp.json` con `${env:ARANEA_MINIO_MCP_RO_BEARER}`.
- 2026-09-18 cert funcional 3 consumidores (Cursor/ZCode/Codex): `get_object` real 477 B con SHA256 propio `2d2dd8c7…03a3` y MD5 == ETag; mutaciones → "server is in read-only mode"; **403 IAM demostrado** en `sqx-strategies` (HTM RERUN-3) → owner action pendiente `~/aranea/work/trio-cert-20260918/owner-action-htm6182-minio-getobject.md` (grant puntual GetObject del ARN exacto, revocable).
- 2026-09-18 noche (verificación post-T21, 4×403): plano SANO (unauth 401 / auth 200, contenedores Up 31h, enforcement read-only activo); los 403 reiterados sobre `sqx-strategies` son el deny IAM **correcto** de la SA — no hay defecto del plano ni del conector. La key owner no dejó copia en discos operator. Concesión T21 de A (MQ5) + B (`strategy.sqx`) stageada en `/opt/mcp/minio/work/`: `policy-t21-ab-grant.json` (`79298be79604a7ea…`) + `f04-apply-t21.py` (`74279dee3487b611…`) + `f04-owner-step-t21.sh` (`981f2b93f7139860…`); el owner aplica con UN comando (key por stdin): `ssh -t root@mcps.lab.aranea.cl 'sudo -n bash /opt/mcp/minio/work/f04-owner-step-t21.sh'`. Tras el apply, fetch/verificación SHA256/entrega Daedalus/revoke corren por Ariadna (jamás con la identidad admin). **SUPERSEDED horas después:** el owner creó la key full vía wizard MinIO y ordenó configurarla como identidad del MCP con lectura Y escritura — ver «Identidad upstream» arriba (resultado final: capacidad RW certificada 4/4, fetch T21 ejecutado y verificado).

## Rollback

`docker rm -f minio-mcp-auth-ro minio-mcp-ro && docker network rm mcp-minio && docker rmi local/minio-mcp-http:1.4.0-mcpproxy6.7.16-g010fix && rm -rf /opt/mcp/minio`; consumer: restore backups mcp.json/aranea-env.sh (hermes-managed) + rm bearer kor. La SA MinIO requiere admin para borrar (owner).

## Deudas

- SA huérfana deny-all (hija de `mcp`) sin poder borrarse sin admin → owner.
- Rotación de la key owner `zaLm…` = decisión owner (invalidaría la SA hija).
