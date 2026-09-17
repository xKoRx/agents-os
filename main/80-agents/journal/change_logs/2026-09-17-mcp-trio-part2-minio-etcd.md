# Change Log — MCP Access Plane — 2026-09-17 (Parte 2: MinIO + etcd + tri-client)

## Contexto

Mandato owner 2026-09-17 (Parte 2): desbloquea MinIO (credenciales entregadas), autoriza etcd greenfield acotado, exige integración tri-cliente (Cursor/ZCode/Codex) y certificación con llamada funcional real. No repetir discovery; actualizar por delta.

## MinIO — `aranea-minio-ro` (:3011) — DEPLOYED + CERTIFIED (server + Cursor)

- **Bloqueo original resuelto sin admin**: `mcp` (usuario entregado por owner) NO tiene autoridad admin (Admin API v3 = 403 AccessDenied real en 8 variantes de firma; `mc admin info` = Access Denied). Vía aplicada: **service account self-service** — la access key owner (`zaLm…`) sí puede crear SAs para sí misma (`mc admin user svcacct add <parent> --policy embedded`). Identidad upstream = SA hija con la política scoped RO embedded (`minio-mcp-ro-policy.json`). Permisos efectivos = intersección (padre ∩ embedded) = exactamente el scope aprobado.
- **Verificación IAM previa** (probe boto3 en contenedor efímero): la key owner padre lee `etcd-backups`/`obsidian-backups` (NO permitido por scope) pero NO `deploy`/`examples`; la SA creada ve SOLO `deploy`+`examples`, DENY `etcd-backups`/`configs`, put denegado. El `list_buckets` del MCP devuelve exactamente 2 buckets (prueba real de scope).
- **Deploy** (patrón temporal): red `mcp-minio`; backend `minio-mcp-ro` = wrapper multi-stage `local/minio-mcp-http:1.4.0-mcpproxy6.7.16-g010fix` (binario Go stdio copiado de `ghcr.io/txn2/mcp-s3@sha256:09371acaca20…` + mcp-proxy 6.7.16 + fix g010; uid 1000; creds S3 por archivos 600 uid-1000 montados, exportadas a env por el entrypoint; `MCP_S3_EXT_READONLY=true` pinned); proxy `minio-mcp-auth-ro` :3011 (nginx digest canónico + bearer server-side `daedalus-ro.bearer` 640).
- **Certificación server 8/8 PASS**: 401 unauth; init (serverInfo mcp-s3 1.4.0); tools/list = 9 exactas; `s3_list_buckets` REAL = {deploy, examples}; `s3_put_object` bloqueado ("server is in read-only mode"); `s3_get_object` en `etcd-backups` = AccessDenied IAM; `s3_list_objects deploy/worker/sqx/` REAL; leak check.
- **Consumer Cursor PASS**: entry `aranea-minio-ro` en mcp.json (clon patcher determinista, backup `mcp.json.bak-minio-etcd-20260917-134138`); bearer en hermes-managed (640+ACL kor, sha16 `c93921c1a80b81d8`); chain `aranea-env.sh` parchado (backup `aranea-env.sh.bak-minio-etcd-20260917-134138`); smoke desde entry real: init + 9 tools + list_buckets = {deploy, examples}.

## etcd — `aranea-etcd-ro` (:3012) — GREENFIELD DEPLOYED + CERTIFIED (server + Cursor)

- **Autorización**: mandato Parte 2 §3 revierte la negación previa; greenfield FastMCP mínimo autorizado con contrato RO estricto.
- **Implementación**: `local/etcd-mcp-ro:0.1.0` (FastMCP 2.12.4, HTTP streamable nativo :8000, sin mcp-proxy; uid 1000). 4 tools: `etcd_list_prefixes`, `etcd_count_keys`, `etcd_list_keys` (keys_only, cap 200), `etcd_get_value` (cap 4KB). Deny-by-default con allowlist positiva (8 prefixes Echo/Forge/SQX), branch MinIO excluida, regex de nombres-secretos excluyente en TODAS las rutas (password/secret/token/access_key/api_key/credential/private_key/*.pem/*.crt/*.key), sin mutadores ni watch, timeout 3s, failover entre los 5 members.
- **POC de contrato** (directo al módulo, antes de exponer): 10/10 PASS — denies (prefix/branch/secret-name), lecturas reales (`/echo/`=75, `/sqx-worker/`=215, value benigna `0.1.0`).
- **Certificación server 13/13 PASS**: 401 unauth; init (serverInfo aranea-etcd-ro 1.30.0); superficie exacta; `count /echo/`=75 REAL; `get_value` benigna REAL; DENY branch minio, DENY secret-named, DENY /demo/ y /minio-example/; session semantics (sid desconocido → 404); leak check. **Cero escrituras al cluster** (solo `/v3/kv/range` keys_only/lectura; `:2379` untouched).
- **Consumer Cursor PASS**: entry `aranea-etcd-ro`; bearer sha16 `bb831ab615e4e4fb`; smoke: init + 4 tools + `etcd_count_keys /echo/` = 75.

## Tri-cliente (Cursor / ZCode / Codex)

- **Cursor: 3/3 PASS** (temporal certificado en Parte 1; minio + etcd en esta parte).
- **ZCode/Codex: PENDING-OWNER (instrumento stageado)** — configs `600 kor` inaccesibles por diseño; el patcher+smoke determinista `daedalus:/tmp/tri-patch-smoke-20260917.py` (sha16 `431abdbfbf51a715`, self-test PASS vs sintéticos: patch + idempotencia + no-leak + round-trip TOML/JSON) añade las 3 entries a ambos clientes (ZCode: clon de entry existente con bearer LITERAL resuelto del chain kor — ZCode no documenta interpolación de headers; Codex: `bearer_token_env_var` nativo) y corre smoke funcional por entry (6 bloques). Ejecutar como kor: `python3 /tmp/tri-patch-smoke-20260917.py`. El inspector `tri-kor-config-inspect-20260917.py` queda como opción de auditoría previa (opcional; el patcher ya fail-closed y respeta configs existentes).
- Nota: la resolución de literales ZCode requiere que kor tenga el chain cargado (`source ~/.config/mcp/aranea-env.sh`) o el patcher fallará cerrado (correcto).

## Deudas y follow-ups

1. **SA huérfana** en MinIO: la primera SA (deny-all, hija de `mcp`) no pudo eliminarse (`svcacct rm` = Access Denied para su propio padre sin admin). Limpieza = owner action (`mc admin user svcacct rm <SA>` con identidad admin). El patcher/smoke no la usa; riesgo = una key inútil con nombre `aranea-minio-mcp-ro` vieja.
2. **Rotación de la key owner** `zaLm…` a discreción del owner: se usó UNA vez para crear la SA (por stdin, sin logs); si era sensible, rotar invalida la SA hija (la capability habría que recrearla con nueva identidad).
3. **ZCode/Codex**: ejecutar el patcher como kor (única acción para cerrar el mandato).
4. **Backlog** (no bloqueante): envío de runbooks de las familias nuevas a revisión owner; posibilidad de mover la política MinIO de `~/aranea/work/mcp-trio/` al vault como referencia canónica del scope.

## Rollback

- MinIO: `docker rm -f minio-mcp-auth-ro minio-mcp-ro && docker network rm mcp-minio && docker rmi local/minio-mcp-http:1.4.0-mcpproxy6.7.16-g010fix` + `rm -rf /opt/mcp/minio` + rm bearer kor + restore backups mcp.json/aranea-env.sh (hermes-managed). La SA en MinIO queda (requiere admin para borrar).
- etcd: `docker rm -f etcd-mcp-auth-ro etcd-mcp-ro && docker network rm mcp-etcd && docker rmi local/etcd-mcp-ro:0.1.0` + `rm -rf /opt/mcp/etcd` + rm bearer kor + restore backups. El cluster etcd NO fue modificado (rollback = solo plano MCP).

## Regression gate (post-deploy Parte 2)

:3001–:3012 → 401 unauth (todas); ssh-mcp :3000 healthy (sirve por IP LAN — curl a 127.0.0.1:3000 = 000, correcto); 26 containers Up; único exited = fixture histórico pre-existente; etcd 5/5 healthy. Cero regresión.
