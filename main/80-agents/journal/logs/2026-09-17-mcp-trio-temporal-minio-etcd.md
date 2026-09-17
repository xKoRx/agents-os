---
type: change_log
schema_version: 1
scope: area
created: "2026-09-17"
updated: "2026-09-17"
area: "[[Aranea]]"
project: "[[AGENT-PLATFORM - MCP Access Plane]]"
entities:
  - "[[Aranea]]"
related:
  - "[[AGENT-PLATFORM - MCP Access Plane]]"
  - "[[AGENT-PLATFORM - MCP Access Plane - Architecture]]"
  - "[[aranea-temporal-mcp]]"
  - "[[aranea-mcps-expert]]"
tags:
  - kind/change-log
  - area/aranea
  - tech/mcp
  - tech/temporal
---

# 2026-09-17 — mcp-trio: Temporal PASS/CLOSED, MinIO y etcd BLOCKED

## Contexto

Mandato owner 2026-09-17: reabrir T5 Temporal e incorporar MinIO y etcd al MCP Access Plane como capabilities RO certificadas (`aranea-temporal-ro`, `aranea-minio-ro`, `aranea-etcd-ro`), ciclo DISCOVER→…→DOCUMENT por familia, integración tri-cliente Daedalus, sin sesión-close de Agents-OS.

## Discovery (hechos físicos que corrigen estado previo)

- Temporal real: `192.168.31.46` (PTR `temporal.aranea.local`), frontend gRPC `:7233`, UI/API `:8080` vía Traefik (`temporal.lab.aranea`), server **1.31.2**, namespaces `sqx-dev`, `sqx`, `sqx-prop`, `temporal-system`. Sin TLS/API key interna. VMID 158.
- MinIO real: `192.168.31.92` (PTR `minio.aranea.local`), S3 API `:9000` (403 anónimo = IAM enforce), console `:9001` vía `minio.lab.aranea`. VMID 157.
- etcd real: **UN cluster** de 5 members en `192.168.31.250-.254` (VMIDs 101/147/154/155/156 de la topología; mapeo VMID→IP no existía), etcd **3.6.4**/cluster 3.6.0, `:2379` plano **sin TLS sin auth** (authRevision 1), healthy, alcanzable desde `mcps` — la deuda R1 "etcd :2379 filtrado" sólo aplicaba desde hermes-vm. 985 keys en 7 prefijos (`/sqx-flowkit`, `/deployer-watcher`, `/echo`, `/demo`, `/deployer`, `/minio-example`, `/mi-servicio`), **incluye access/secret keys de MinIO en claro** bajo `/deployer-watcher/development/minio/*` y `/minio-example/development/minio.*`.
- Daedalus (.161): host key SSH cambió — nueva pin `SHA256:IkEaqcpWKCwekKd4SrxRAZXxPGRVDBaScHLJSN02JRA` (known_hosts de hermes). Codex config.toml mtime 2026-09-16 18:49 (post-normalización bearer_token_env_var según brief owner; contenido 600 kor no verificable por hermes-ops).

## Temporal — DEPLOYED + CERTIFIED (PASS/CLOSED)

- Selección: `stevekinney/temporal-mcp` npm 0.2.1 (28 tools RO por diseño, policy engine con `hardReadOnly` y `allowedNamespaces`, audit logging, redaction). Alternativa GethosTheWalrus descartada (expone start/signal/cancel/batch = FAIL RO). POC stdio en contenedor efímero: initialize PASS, tools/list 28, cero mutadores; conexión gRPC sólo con `:7233` (con `:8080` da deadline aunque TCP/H2 pasen — lección registrada).
- Deploy (patrón Architecture, familia nueva): red `mcp-temporal`; backend `temporal-mcp-ro` (imagen local `local/temporal-mcp-http:0.2.1-mcpproxy6.7.16-g010fix` sha256 `038eef5c1d56…`, uid 1000, sin host port, mcp-proxy 6.7.16 + fix g010 byte-identical a hasura); nginx proxy `temporal-mcp-auth-ro` `:3010` con digest canónico y bearer server-side (`/opt/mcp/temporal/runtime/proxy-secrets/daedalus-ro.bearer`, 640 root, generado server-side). Config `/opt/mcp/temporal/runtime/config/temporal-mcp.json` (mount ro): address `192.168.31.46:7233`, `hardReadOnly: true`, `allowedNamespaces [sqx-dev, sqx, sqx-prop]`. Build tree `/opt/mcp/temporal/build-ro/` con shas documentados.
- Certificación server (evidencia): unauth `:3010/mcp` → 401; initialize → 200 (serverInfo temporal-mcp 0.1.0); tools/list → exactamente 28 sin mutadores; `temporal.namespace.list` → datos reales del server 1.31.2 (smoke funcional); negative mutación → `temporal.workflow.start` = `-32602 Tool not found`; allowlist → `describe temporal-system` = `NAMESPACE_NOT_ALLOWED` vs `describe sqx` OK. Ciclo con `notifications/initialized` y `Mcp-Session-Id` verificado.
- Integración Daedalus/Cursor: bearer replicado mcps→daedalus por stdin pipe sin imprimir (archivo hermes-managed 640 + ACL `u:kor:r--`, sha16 `a081349e3ac1b36b` = igual al de mcps); chain `~/.config/mcp/aranea-env.sh` parchado in-place por ACL (marker `# [aranea-mcp] temporal-mcp-ro (added by hermes-managed 2026-09-17)`, backup `aranea-env.sh.bak-temporal-20260917-021846`, `bash -n` PASS); entry Cursor `aranea-temporal-ro` → `http://mcps.lab.aranea.cl:3010/mcp` con `${env:ARANEA_TEMPORAL_MCP_RO_BEARER}` (backup `mcp.json.bak-temporal-20260917-021950`). **Consumer smoke PASS**: init + tools/list 28 + `namespace.list` devolviendo los 4 namespaces reales, desde la entry real de Cursor.
- ZCode/Codex: configs 600 kor inaccesibles por diseño — inspector read-only redactado stageado en `daedalus:/tmp/tri-kor-config-inspect-20260917.py` (sha16 `f290562f49e8b64b`, self-test PASS contra sintéticos). **Owner action**: ejecutarlo como kor. La incorporación de la entry temporal a ZCode/Codex (si el owner quiere paridad tri-cliente ya) sigue el patrón de patcher determinista kor del 2026-09-16.
- Documentación: runbook nuevo `30-resources/runbooks/aranea-temporal-mcp.md`; skill `aranea-mcps-expert` (routing table + runbook list + nota familias MinIO/etcd); Architecture (inventario 11 capabilities + sección Temporal); proyecto (Bitácora + T5 cerrado + backlog MinIO/etcd); skill local `mcp-access-plane-operations` (gotchas npm-wrapper, gRPC vs UI, bearer mount obligatorio, etcd sin auth, IPs reales).

## MinIO — BLOCKED (owner action requerida)

- Upstream seleccionado y pinneado: `txn2/mcp-s3` v1.4.0 (tag→commit `a99d4ca2…`, imagen ghcr digest `sha256:09371acaca20…`, uid 1000 `mcp`, RO default con put/delete/copy bloqueados server-side, size caps, prefix ACLs, multi-connection). Imagen pull + inspect + limpieza POC verificados (cero residuo).
- Blocker: no existe identidad upstream dedicada RO para MinIO. IAM enforce (unsigned → 403). Crear `mcp_minio_ro` (+policy readonly scoped, sin buckets backups/admin) exige `mc admin` con credencial admin = **owner action** (mandato §16: no usar root/admin permanente ni credenciales dev de etcd). Con la credencial, el deploy es réplica del patrón temporal (`:3011`, red `mcp-minio`).

## etcd — BLOCKED (owner decision)

- Sin upstream MCP mantenible: `rleungx/etcd-mcp-server` (1 commit 2025, muerto), `tsonglew/mcp-etcd` (3 commits, sin tools), `Coderad00/mcp-etcd` (API v2, put/delete/get_all sin RO), `anveshreddy18/etcd-mcp-server` ("under construction"). Detalle completo: `~/aranea/work/mcp-trio/etcd-reconciliation.md`.
- Greenfield (FastMCP sobre gateway HTTP v3) es la única vía = **requiere decisión owner** (mandato §2/§16 prohíbe construir sin escalar). Boundary adicional: cluster sin auth y con secretos MinIO en keys → un `aranea-etcd-ro` necesita prefix allowlist excluyente (o activar auth/RBAC, mutación de cluster PROD aparte y gated). Watch sin acotación queda fuera del contrato inicial.

## Incidente etcd (auto-rollback verificado)

Durante discovery, un probe "negativo" `kv/put` (`aranea-test` → `x`) fue **aceptado** por el cluster (auth OFF), mutando PROD (rev 55031→55032). Rollback inmediato: `kv/deleterange` exacto (`deleted:1`, rev 55033), verificación count 0 y total de keys 985 = baseline pre-incidente, cluster healthy. Lección (registrada en skill): sin auth, todo probe de escritura es una escritura real — prohibidos los probes negativos de mutación en etcd.

## Regression gate (post-deploy)

`:3001–:3010` → 401 unauth (todas las familias nginx); `:3000/` (ssh-mcp sirve en `/`) → 401 y healthy; 22 containers Up; único exited = fixture histórico pre-existente (`mongo-forge-rw-pre-confirmation-20260912`). Cero regresión. Limpieza: imágenes POC (`node:22-slim`, `ghcr.io/txn2/mcp-s3:v1.4.0`) removidas, /tmp de mcps y daedalus limpio (scripts stageados del inspector quedan sólo si el owner no los ha corrido: `tri-kor-config-inspect-20260917.py`).

## Estados resultantes

```text
aranea-temporal-ro : PASS / CLOSED  (server + Cursor; ZCode/Codex = owner inspector)
aranea-minio-ro    : BLOCKED        (owner action: identidad MinIO dedicada)
aranea-etcd-ro     : BLOCKED        (owner decision: greenfield sí/no + boundaries)
```

## Continuación 2026-09-17 (instrucciones owner: cierre controlado)

- **etcd greenfield: NO AUTORIZADO** — registrado. Creada workstream note `ETCD-HARDENING` (workstreams/): incidente, exposición real (63 keys con credenciales, `:2380` peer también expuesto a todo el LAN, LXC sin SSH → contención sólo vía OPNsense/PVE), contención de red propuesta (no implementada, GATED), y fases de hardening F1–F5 (snapshot→TLS→RBAC→rotación→re-evaluación MCP). Skill `mcp-access-plane-operations` actualizada con el alcance real de exposición.
- **Temporal:** inspector stageado verificado (sha256 completo íntegro local=Daedalus `f290562f49e8b64b…`, única escritura = `.bak-tri-*` de los propios configs kor, ENVSH read-only, auto-test PASS). Ejecución kor imposible para hermes-ops (sin sudo por diseño A0–A5, no se amplían permisos) → queda como la única OWNER ACTION para cerrar ZCode/Codex. Estado de Temporal queda PARTIAL hasta esa ejecución + integración de los dos consumidores.
- **MinIO:** `/usr/bin/mc` en mcps es Midnight Commander, no MinIO Client — sin autoridad admin local (correcto por appliance design). Política RO dedicada propuesta (scope `deploy/worker/sqx/*` + `examples`, deny explícito a `*backup*`) guardada en `~/aranea/work/mcp-trio/minio-mcp-ro-policy.json` (hermes-vm); scope a confirmar por el owner contra la lista real de buckets. Identidad + política = owner action con instrucciones exactas entregadas en el reporte.
- Feedback de sesión creado (event-driven): `80-agents/journal/feedback/system-1/2026-09-17-aranea-mcp-trio-session-feedback.md` (pain pattern: infra-docs sin mapa VMID→IP).
- Post-verificación de no-regresión: 3001–3010 en 401 unauth, ssh-mcp :3000/ healthy, etcd healthy rev 55033 (estado post-rollback intacto), ambos containers temporal Up.

## Rollback

- Temporal completo: restore backups mcp.json/aranea-env.sh (hermes-managed), rm bearer kor, `docker rm -f temporal-mcp-auth-ro temporal-mcp-ro`, `docker network rm mcp-temporal`, opcional `docker rmi local/temporal-mcp-http:0.2.1-…` y `rm -rf /opt/mcp/temporal`. Detalle en runbook.
- MinIO/etcd: sin cambios en sus targets (sólo imágenes POC borradas).
