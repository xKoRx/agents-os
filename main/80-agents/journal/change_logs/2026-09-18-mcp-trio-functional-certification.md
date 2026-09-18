# Change Log — MCP Access Plane — 2026-09-18 (certificación funcional completa del trío)

## Contexto

Mandato owner 2026-09-18: certificar end-to-end `aranea-temporal-ro` (:3010),
`aranea-minio-ro` (:3011) y `aranea-etcd-ro` (:3012) contra los targets reales
desde los consumidores Cursor, ZCode y Codex, con casos de uso funcionales
(no repetir los smokes básicos ya cerrados 2026-09-17), sin reinstalar ni
rediseñar, y resolver bloqueos dentro del scope aprobado.

## Resultado: 9/9 PASS (3 capabilities × 3 consumidores)

### Server-side (profundidad funcional, runtime Hermes, helper `session-steps-client.py`)

- **temporal-mcp 0.2.1 → Temporal Server 1.31.2 real (gRPC :7233)**: `connection.check`
  connected; `cluster.info`; `namespace.list` = {sqx-dev, sqx, sqx-prop};
  `namespace.describe sqx-dev` real (retention 10 días); negative
  `describe temporal-system` → `NAMESPACE_NOT_ALLOWED`; `workflow.list/count`,
  `schedule.list`, `task-queue.describe`, `search-attributes.list`,
  `worker.deployment.list` responden del server vivo (0 workflows/schedules hoy —
  namespaces sqx vacíos en este momento, no es defecto); `describe/history` de ID
  inexistente → `NOT_FOUND` limpio; mutadores ausentes de la superficie
  (`temporal.workflow.start/terminate` absent PASS).
- **mcp-s3 1.4.0 → MinIO 192.168.31.92:9000 real**: `list_buckets` = exactamente
  {deploy, examples}; `list_objects` reales (examples/, deploy/worker/sqx);
  `get_object_metadata` + `get_object` reales; **integridad verificada**: objeto
  477 B con SHA256 propio `2d2dd8c7…03a3` y MD5 == ETag (`5d22b941…3329`);
  mutaciones bloqueadas (`delete_object`/`put_object` → "server is in read-only
  mode"); **IAM deny demostrado** sobre el HTM de RERUN-3 en `sqx-strategies`
  (403 HeadObject, RequestID nuevo `18D67A7AAF…`, consistente con C5B);
  not-found → 404 NoSuchKey (error de ruta distinguible de permisos).
- **aranea-etcd-ro 1.30.0 → cluster etcd 5 members real**: allowlist viva de
  8 prefixes; `count /echo/` = 75, `count /symphony/` = 133; `list_keys /echo/`
  y `/deployer/` (14/16) con keys_only; `get_value` benigna real
  (`/deployer-watcher/development/service/version` = `0.1.0`); negatives:
  `/demo/` → prefix not in allowlist, branch `/deployer-watcher/development/minio`
  → denied excluded branch, key inexistente → `found:false` (sin errores
  confusos). Cero escrituras al cluster (solo range).

### Consumer-side (Daedalus, runtime real de cada cliente)

- **Cursor 3/3 PASS**: resolución desde SU configuración efectiva
  (`~/.cursor/mcp.json` entry + `${env:VAR}` interpolado vía chain kor
  `aranea-env.sh`), sesiones por capability, tools/list 28/9/4 exactas, probe
  funcional real por familia (`namespace.list`, `get_object` con contenido,
  `count_keys`=75), negatives observables (NAMESPACE_NOT_ALLOWED, 403 IAM,
  allowlist etcd, read-only mode), absent de mutadores, leak check CLEAN.
- **ZCode 3/3 PASS** y **Codex 3/3 PASS**: mismas baterías funcionales.
  Sus configs son `600 kor` por diseño (no legibles por el operador): la SHAPE
  de ambas configs fue certificada por el patcher+smoke kor del 2026-09-17
  (`tri-patch-smoke-20260917.py`, ZCode bearer literal del chain, Codex
  `bearer_token_env_var` nativo); hoy se verificó el plano funcional completo
  resolviendo endpoint+bearer exactamente como cada cliente los resuelve
  (mapa caps certificado + chain kor). Smoke de configuración (17-sep, owner)
  y certificación funcional de runtime (18-sep) quedan clasificados como
  evidencias complementarias, NO equivalentes: juntas cubren shape + runtime.
- Instrumento: `tri-consumer-cert.py` (derivado de `templates/daedalus-cert.py`,
  transporte raw urllib idéntico, UNA sesión MCP por corrida, bearer solo por
  stdin/archivo, leak check). Stageado en `daedalus:/tmp` y ELIMINADO tras la
  corrida; copia retenida en workspace de sesión `~/aranea/work/trio-cert-20260918/`.

### Caso obligatorio HTM build 6182 — BLOCKED por IAM (owner action emitida)

- Bucket `sqx-strategies`, object key completa y expectativas
  (13,074,872 B; SHA256 `21917e144668cfd014e0d0c6a60d4f70eb3c4a17783bacac02f729eb587e8b5c`)
  tomadas de la provenance durable (delta C5, RERUN-3). `s3_get_object` vía la
  capability → 403 IAM (re-verificado hoy; el grant pedido en C5B NO fue aplicado).
- Diagnóstico: NO es error de ruta ni objeto inexistente (HeadObject 403 por
  policy, no 404); es limitación de permisos de la identidad upstream de la
  capability (deny-by-default correcto, fuera del scope certificado).
- **Owner action única, mínima y revocable** emitida en
  `~/aranea/work/trio-cert-20260918/owner-action-htm6182-minio-getobject.md`:
  statement `Allow s3:GetObject` del ARN EXACTO del objeto, insertada antes del
  Deny en la policy embedded de la SA de `aranea-minio-ro`; revocación =
  re-aplicar `minio-mcp-ro-policy.json` canónico + re-test negativo 403.
  Alternativa cero-IAM: copia byte-exacta verificable contra el SHA256.
  Con el grant aplicado, la descarga+verificación corre por el MCP real y
  CERT-F04-01 pasa de BLOCKED a ejecutable.

### Regression gate + límites

- Unauth 401 en :3001–:3012; ssh-mcp :3000 = 401 vía su bind LAN
  `192.168.31.219` (loopback 000 = quirk conocido de la familia ssh, healthy).
- Deuda preexistente sin cambios: capability adicional no incluida en el
  contrato RO de temporal (p.ej. visibility archive UI) no fue necesaria para
  diagnóstico; si aparece una necesidad real, se evalúa capability extra sin
  ampliar permisos por defecto. Configs sensibles de etcd con secretos siguen
  excluidas por diseño (regex secret-named); acceso específico = decisión
  owner separada (ETCD-HARDENING).

## Rollback

No hubo mutaciones de configuración, IAM, cluster ni runtime: certificación
observacional. Rollback = inexistente por diseño; los scripts stageados fueron
eliminados de ambos hosts y el workspace de sesión queda como evidencia.
