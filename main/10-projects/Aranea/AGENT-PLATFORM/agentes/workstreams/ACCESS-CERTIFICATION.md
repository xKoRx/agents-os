---
type: note
status: active
area: "[[Aranea]]"
parent: "[[AGENT-PLATFORM - MCP Access Plane]]"
created: "2026-09-14"
updated: "2026-09-16"
tags:
  - area/aranea
  - tech/mcp
  - kind/certification
---

# MCP Access Certification — workstream del MCP Access Plane

> Componente del proyecto [[AGENT-PLATFORM - MCP Access Plane]]. **No es un proyecto paralelo.**
>
> Certificación física de accesos del access plane ejecutada por el agente desde la superficie MCP real. Ante conflicto con notas históricas, manda esta evidencia fechada; la autoridad agent-facing sigue siendo [[aranea-mcps-expert]].

## Veredicto

```text
ACCESS_CERTIFICATION_PARTIAL — run 2026-09-14
H1 RESOLVED 2026-09-15 · H2 RESOLVED 2026-09-15 (remediation run, evidencia abajo)
Echo runtime observation: RESUELTO 2026-09-15 — GAP-ECHO-004 CLOSED (owner seed instalado;
recertificación viewer echo-runtime-prod PASS end-to-end desde Daedalus; detalle abajo)
```

Ninguna superficie obtiene PASS incondicional: hay dos hallazgos HIGH (boundary viewer SSH no aplicado; credenciales upstream expuestas por `export_metadata`) y varias superficies con verbos no demostrables o no ejercidos por diseño. No se declara ningún acceso nuevo certificado más allá de lo listado; el trigger de reactivación del [[Echo + Echo Forge — Deferred Certification Backlog]] **no** queda abierto por esta run.

## Remediation run 2026-09-16 (c) — GAP-ECHO-010 REPAIRED_AND_CERTIFIED

Ejecutada por Ariadna (Hermes) vía management path `mcps-ops` + certificación consumer desde Daedalus. Causa raíz **PROVEN** (detalle completo en change_log `2026-09-16-gap-echo-010-shared-stdio-child-repaired`):

- **Causa:** `mcp-proxy` 6.7.16 en las imágenes http-wrapper spawnea UN hijo stdio compartido y multiplexa todas las sesiones HTTP sobre ese `Client`. Si el hijo muere, no hay respawn: `initialize` sigue respondiendo 200+sid (metadata cacheada) mientras todo `tools/*` devuelve `-32603 Not connected` hasta `docker restart`. Mapeo: `-32001`=sid inexistente/reapado; `-32000`=sin header sid; `202` sin sid = notificaciones id-less, no initialize requests. `ssh-mcp` (pool-64) y `flink-mcp` (SDK Java, servlet propio) **no comparten** esta causa.
- **Fix:** patcher determinista `fix-shared-child.mjs` en los build trees (`/opt/mcp/hasura/http-wrapper/`, `/opt/mcp/hasura/build-prod-ro/`) aplicado al bundle del CLI; respawnea el upstream en el próximo `createServer`. Imágenes nuevas con rollback intacto: `local/hasura-mcp-http:1.0.0-9ba59f2-mcpproxy6.7.16-g010fix` (dev) y `local/hasura-mcp-http:1.0.0-9ba59f2-prod-ro-h1fix-mcpproxy6.7.16-g010fix` (prod-ro). Containers recreados con mounts/env/red/policy idénticos.
- **Verificación del fix:** kill del hijo ⇒ sesión vieja `-32603` (esperado) ⇒ initialize fresco 200+sid ⇒ calls OK sin restart (dev y prod-ro).
- **Certificación:** server-side dev 50/50 y prod-ro 30/30 ciclos `initialize→tools/list→tools/call→DELETE` PASS; consumer Daedalus dev 50/50 (`tools=9`) y prod-ro 30/30 (`tools=3`) PASS ⇒ `CONSUMER_DAEDALUS_PASS`, `DEVELOPER_UNBLOCKED: NOT_PROVEN` (sin agente Echo/Forge identificable como afectado hoy).
- **Regresión:** 401 unauth en 3001–3009; superficie DEV 9 tools intacta; PROD-RO exactamente 3 tools post-H1 (`export_metadata` ausente); H2 `POLICY_DENIED` intacto; cero drift en el resto del plane.
- **Veredicto:** `REPAIRED_AND_CERTIFIED`. Deuda residual: flink (Java SDK) y ssh-mcp (pool-64) requieren diagnóstico propio si muestran síntomas; fix a nivel bundle — evaluación upstream de mcp-proxy diferida.

## Remediation run 2026-09-16 (d) — tri-client config normalization (Cursor/ZCode/Codex en Daedalus)

Recuperación de la sesión colgada 18:56 y cierre del brief owner. Cambio log: `80-agents/journal/logs/2026-09-16-tri-client-mcp-config-normalization.md`.

- **Cursor: READY** — refs Mongo `ARANEA_MONGO_FORGE_MCP_RO/RW_BEARER` corregidas y persistidas en disco (verificado por parse directo; mtime 15:29); 11/11 sweep PASS; clon `aranea-postgres-ro-hermes-managed` RETAINED (contrato del mecanismo B2: `mcp-onboard.py`/`consumer-smoke.py` lo referencian).
- **ZCode: funcional conservado** — smoke 10/10 heredado; `${env:}` en headers HTTP NO documentado por ZCode ⇒ bearer literals se mantienen (600 kor) por decisión del brief; alternativa (rotación + canal kor-only) pendiente de decisión owner.
- **Codex: PENDING** — config `600 kor` sin ACL (ilegible para `hermes-ops` por diseño). Instrumento read-only staged: Daedalus:`/tmp/tri-kor-inspect.py` (sha16 `de782b8708a13a82`), el owner lo ejecuta como kor; redactado, con backups `.bak-tri-*`; normalización sólo contra drift demostrado usando `bearer_token_env_var` (mecanismo nativo del binario).
- **Anomalía abierta:** ambos configs kor con mtime 2026-09-16 13:26:41 + backups `.bak-mcp-20260916-132641` sin change_log que ampare la edición (la sesión vault de esa mañana declara read-only). Origen a identificar por el owner.
- Sin smokes, sin herramientas MCP ejecutadas, sin secretos impresos, sin cambios de ACL.

## Remediation run 2026-09-16 (b) — E-02 CLOSED con runtime topology owner FROZEN

Continuación de la misma fecha: AC-11/AC-12/AC-01 + verifier independiente **PASS** → `E02 CLOSED` (software). **Autoridad arquitectónica owner (FROZEN, aplica a toda certificación futura):**

- **Daedalus `192.168.31.161` = runtime temporal/dev de Echo y Echo Forge** (builds, fixtures, procesos de certificación). `.75` = infra DEV compartida (Hasura/Flink/Portainer) — **jamás runtime Echo** (sin binarios, procesos, services, containers persistentes ni autostart de componentes Echo). `.71` = Echo PROD, observation-only. `.211` = antiguo ubuntu-dev, retirado/offline (referencias históricas = stale).
- **DNS canónico (Pi-hole `192.168.31.31`):** `dev.echo.core.lab.aranea → 192.168.31.161` (actualizado por owner). El runtime/DNS actual manda sobre documentación histórica.
- Regla durable: **"Application runtime follows declared topology; infrastructure proximity is never authority to colocate product components."** Antes de elegir dónde ejecutar un componente, la certificación debe descubrir la runtime topology declarada (esta nota + [[Echo — Access & Physical Capability Matrix]]), no inferirla de proximidad de infraestructura.
- Hallazgo de targeting: el resolver embebido de Docker (127.0.0.11) NO consulta `/etc/hosts` del host — los containers de Flink en `.75` resuelven vía Pi-hole. Un hosts-fixture en el host no alcanza a los containers; la autoridad real del nombre es el DNS del lab. Verificar el resolver efectivo del consumidor antes de elegir el mecanismo de targeting; prohibido `extra_hosts`/compose override para esta clase de fix (decisión owner: DNS canónico).
- Detalle técnico de ACs, KEEP (062 en `.220/echo-develop`) y REMOVE (fixtures) en change_log `2026-09-16-e02-closed` y bitácora E-02.

## Remediation run 2026-09-16 — E-02 physical gates + 2º caso del defecto async-202

Ejecutada por Ariadna (Hermes) vía capabilities MCP certificadas + helper SDK consumer único (bearer por stdin, sin argv). Resultado: los tres gates físicos E-02 (Hasura roles/hook, Kafka PublishSync/redelivery, Flink restart/recovery) **PASS** — detalle y verdict en [[Echo — E-02 Control Safety, Auth and Journal Recovery]] y [[Echo — Access & Physical Capability Matrix]].

### GAP-ECHO-010 (nuevo, P1) — proxies nginx-wrapped entran en modo async-202 tras churn de sesiones

**Síntomas observados (reproducidos en 3 proxies: hasura :3006, ssh :3000, flink :3008):** tras decenas de sesiones creadas en pocas horas, el `initialize` responde `HTTP 202 Accepted` **sin `Mcp-Session-Id` en headers y sin body**; todo tool call posterior falla (`-32000 Missing mcp-session-id`, `-32603 Not connected`, `-32001 Session not found`). Clientes stateless que hacen init-per-run quedan bloqueados; el mismo request es 200-sync+sid cuando el proxy está "fresco" y 202-async en modo degradado. La ventana de recuperación natural por idle fue inconstante (60s funcionó una vez, 76s de backoff no otra).

**Workaround certificado (usado 2 veces en hasura, 1 en ssh-mcp):** `docker restart <backend-proxy>` → healthy ~8s → primer init vuelve a 200-sync+sid. No toca config, no toca targets (Echo/Flink/Gateway nunca reiniciados por esto).

**No resuelto (deuda P1):** causa raíz — el backend `mcp-proxy` 6.7.16 que envuelve backends stdio parece conservar sesiones sin cerrarlas (idle-close configurado 30min) y degrade el path sync→async; diagnóstico real pendiente (pool size, leak de sesiones, semántica de streams). Acción durable: instrumentar sesiones activas, añadir close/cleanup de sesión o TTL corto, o fijar modo sync explícito. Mientras el workaround sea restart, TODO consumidor agent-first de este plane debe tratar `202-no-sid` como "proxy degradado → reparar vía restart del proxy backend", no como fallo del target.

**Evidencia del diagnóstico del caso ssh-mcp (2026-09-16 ~02:00Z):** container `Up 5 hours (healthy)`, logs sin líneas "session limit"/pool en 3h, `/status` con `connections: 0` y `sessions=0` — es decir, **NO era el quirk conocido de pool-64-saturado** (sin conexiones activas ni logs de límite); era el mismo modo async-202 sin sid. Registrado como variante del defecto.

## Remediation run 2026-09-15 — H1/H2 RESOLVED

Ejecutada por Ariadna (Hermes) vía management path nativo `mcps-ops`; certificación consumer desde Daedalus (`daedalus-ops`, bearer por stdin). No se declaró `ACCESS_CERTIFICATION_PASS`: el gap de capability Echo runtime sigue abierto.

### H1 RESOLVED — `export_metadata` eliminado de la superficie PROD-RO

- Fix server-side en el backend MCP (patrón strict-RO existente): registro de `export_metadata` eliminado de `/opt/mcp/hasura/src-prod-ro/cli/internal/mcp/handlers/metadata.go` (sha antes `01506a1f…` → después `ec8f6771…`).
- Rebuild Go: `local/hasura-mcp:1.0.0-9ba59f2-prod-ro-h1fix` (binario sha `b64f9696…`, distinto del anterior `b7f714e9…` → `ddcf3a9a43e9`) + wrapper `local/hasura-mcp-http:1.0.0-9ba59f2-prod-ro-h1fix-mcpproxy6.7.16` (`5e955c87faf8`). Recreate con mounts/red/policy idénticos (baseline respetado).
- Server smoke (mcps, localhost): `tools/list` = exactamente `get_inconsistent_metadata`, `get_schema`, `get_version`; `get_version` v2.38.0; `get_inconsistent_metadata` consistente; negativa `export_metadata` → ausente de `tools/list` y `tools/call` rechazado sin contenido de metadata (sin `database_url`, sin `postgres://`).
- Consumer smoke Daedalus: `initialize` PASS (`aranea-hasura-prod-ro`), `tools/list` = exactamente 3 tools, `get_version` PASS, `get_inconsistent_metadata` PASS, negativa `export_metadata` PASS. RESULT: PASS.
- `get_schema`: sigue el problema de transporte pre-existente (M5) — la introspección (~11 MB) cierra el child stdio del proxy y la sesión queda "Not connected". Reproducido idéntico en la imagen DEV sin el patch H1 → no es regresión del cambio; M5 permanece abierto como diagnóstico proxy/transporte.
- Rollback demostrado: recrear el container con la imagen anterior `local/hasura-mcp-http:1.0.0-9ba59f2-prod-ro-mcpproxy6.7.16` (tags antiguos retenidos en mcps); restore de `metadata.go` desde backup byte-identical probado durante la intervención (sha `01506a1f…` verificado tras restauración accidental-verify).

### H2 RESOLVED — enforcement viewer tool-level en ssh-mcp

- Root cause (evidencia audit-log física 2026-09-14T15:28:57Z): `mt5-kronos` (viewer, readOnly=true) ejecutó `echo probe-should-be-denied` vía `run-command` porque `getAllowedClasses()` devuelve `['read-only']` para readOnly y `run-command` no filtra por tool — el comando clasificó `read-only` y pasó.
- Fix server-side en `/opt/mcp/src/ssh-mcp/src/policy/engine.ts` (sha `6803db94…`): allowlist `READ_ONLY_TOOLS` (read-command, list-connections, list-sessions, read-session-output, sftp-download, close-session, open-session) + denegación temprana en `evaluate()` para `profile.readOnly` con tool fuera de la allowlist (`ruleId: read-only-tool-boundary`). `open-session`/`close-session` quedan permitidos por diseño upstream documentado (viewer puede abrir background `tail -f` y debe poder cerrarlo; class gating/approval sigue aplicando). Test upstream `engine.test.ts` actualizado al nuevo mensaje (1 línea).
- Tests: suite unitaria completa `44 passed | 1 skipped (45)`, typecheck OK; test H2 dedicado (7 cases) PASS. Build `local/ssh-mcp:2.8.0-d2d7696-h2fix` (`8c09e0f41f43`), recreate con mounts/ports/entrypoint idénticos (config.toml sha intacto `22664e96…`).
- Consumer smoke Daedalus (RESULT: PASS):
  - `mt5-kronos` (viewer): `read-command whoami` PASS → `worker-kronos\echo-dev`; `run-command echo` → `POLICY_DENIED: Profile "mt5-kronos" is read-only: "run-command" is refused…` MUST DENY ✓
  - viewer Linux temporal `linux-viewer-smoke` (profile efímero sobre sqx-kronos, añadido y removido con restore byte-identical del config, sha `22664e96…` verificado): `read-command whoami` PASS → `echo-dev`; `run-command echo` → `POLICY_DENIED…` MUST DENY ✓
  - `mt5-kronos-operator`: `run-command echo` PASS → `operator-ok`
  - `docker-echo-dev-operator`: `run-command docker ps` diagnóstico PASS
  - `sqx-zeus` (operator): read PASS, run PASS (operators no afectados)
- Rollback demostrado: recrear `ssh-mcp` con `local/ssh-mcp:2.8.0-d2d7696` (imagen base retenida) + config sin cambios.

### Observación runtime Echo — 2026-09-15 (staging + observabilidad)

Ejecutada por Ariadna (Hermes) vía management path `mcps-ops` + certificación consumer desde Daedalus real. Resuelve por vía observacional el prerrequisito de observación runtime Echo (CERT-E04-01/F-04) sin mutar el host PROD:

- **Target resuelto con evidencia runtime:** `.211:8090` (referencia histórica de la matriz Echo) está MUERTO (22/8090 closed). El runtime Echo vivo es **PROD** `192.168.31.71` = `prod.echo.gateway.lab.aranea` (PTR real; `GET /health` → 200 `{"status":"ok"}`; 8082 cerrado; error 404 estilo Go net/http; coincide con webhooks del hallazgo H1 y con logs `env=production, host=echo`). El runtime DEV no está desplegado (docker-echo-dev = sólo Flink/Hasura/Portainer, verificado por Docker vía operator root).
- **Viewer staged en `aranea-ssh`:** profile `echo-runtime-prod` (`echo-dev@192.168.31.71:22`, `role=viewer`, `readOnly=true`, `group=prod`, host key pinneada `zPHN…wdfU`, keyRef existente `/run/ssh-keys/echo-dev/id_ed25519`). Config `22664e96…` → `047d00e7…`; backup `/tmp/config.toml.pre-echo-runtime-prod` en mcps; defecto transitorio de deploy (modo/ownership del config tras el patch → crash loop) corregido a `600 65532:65532`; resto del plane sin drift. **Owner gate CUMPLIDO 2026-09-15:** owner seed instaló la key en `.71` (creando la identidad dedicada `echo-dev`, que el bundle inicial asumía preexistente — corrección registrada como lección). Recertificación completa: § GAP-ECHO-004 CLOSED más abajo.
- **Enforcement H2 re-certificado consumer-side (Daedalus real, RESULT: PASS):** initialize PASS (SSH MCP Server 2.8.0), 11 tools, 7 perfiles visibles; `run-command echo` en `mt5-kronos` → `POLICY_DENIED … read-only-tool` MUST DENY ✓; `read-command whoami` viewer PASS (`worker-kronos\echo-dev`); en `echo-runtime-prod` el `run-command` falla cerrado en connect (nada ejecuta) y `read-command` queda en `Permission denied` esperado.
- **Observación runtime PROD operativa vía `aranea-observability-ro`:** sonda desde mcps (bearer stdin) — initialize PASS, 22 tools RO, `query_loki_logs {job="echo-core"}` → líneas reales en vivo (`env=production`, `host=echo`, `service=echo-core`, `account_sync: flushed snapshots`, `inst_snapshot: updated` broker ORION GOLD, source `github.com/xKoRx/echo/v3/core/internal/telemetry.go`), `query_prometheus up` instant → 5 series reales. Quirks 1.4.2 aplicados: args `logql/startRfc3339/endRfc3339/expr`, `datasourceUid` obligatorio (Loki `P8E80F9AEF21F6940`, Prometheus `PBFA97CFB590B2093`).
- **Finding de higiene SSH:** el host key ED25519 de `.71` es IDÉNTICO al de `sqx-zeus` (`SHA256:zPHNJq9WlQofIib7Rx1gkCyAtF+HeoMeWPXeltowdfU`) — clon sin regenerar host key (mismo patrón corregido en Hera/Kronos 2026-09-10). Rotación de host key en `.71` = owner action sugerida (no bloqueante).
- Scripts de smoke eliminados de mcps/Daedalus/local; sin secrets en chat/vault; sin mutación en `.71`.

### GAP-ECHO-004 CLOSED — certificación viewer `echo-runtime-prod` (2026-09-15)

Owner seed aplicado por el owner como root en `.71` (hostname `echo`): identidad dedicada `echo-dev` creada (uid/gid 1001, grupos sólo `echo-dev`, sudo DENIED), `mcps:/opt/mcp/ssh/keys/echo-dev.pub` (fingerprint `SHA256:2Qv9f2AREQyse50bGYaTLc1PHK43gvuf3xgv5TTJ+I0`) instalada en `~echo-dev/.ssh/authorized_keys` (append-only, `.ssh` 700 / archivo 600, sin reemplazo de keys existentes), `sshd -t` PASS. Corrección de runtime: el bundle asumía `echo-dev` preexistente y no lo estaba — el owner lo creó como identidad dedicada; lección de preflight registrada en runbook y skill.

Recertificación consumer desde Daedalus real (probe server-side en mcps, bearer por stdin, sesión MCP única; RESULT: PASS):

- initialize PASS (SSH MCP Server 2.8.0); `tools/list` = exactamente 11 tools; `echo-runtime-prod` visible en `list-connections` (7 perfiles).
- identity/target proof: `whoami` → `echo-dev`; `hostname` → `echo`; `id` → `uid=1001(echo-dev) gid=1001(echo-dev) groups=1001(echo-dev)` — sin sudo, sin grupos operator.
- runtime: `echo-gateway` (PID 713, desde ago09) y `echo-core` (PID 110701, desde ago20) RUNNING como `kor`; `echo-functions` (StateFun, PID 320982, sep12) RUNNING; **Bridge NOT_DEPLOYED** (sin proceso; registrado, no se levanta). Promtail y nginx (proxy :80) corriendo en el host.
- listeners: 80, 9080, 9090, 8080, 8090 (+22/53); `ss -tlnp` no atribuye proceso de otros usuarios (límite viewer, esperado).
- logs: `journalctl -n` PASS pero acotado al user journal de `echo-dev` (sin membresía `adm`/`systemd-journal`); la correlación de logs productivos sigue siendo `aranea-observability-ro` (`service=echo-core`).
- boundary: `docker ps`, `curl`, `systemctl`, `dmesg`, `pgrep` → POLICY_DENIED (clase `safe` también rechazada en viewer); negative H2 `run-command echo cert-negative-probe` → `POLICY_DENIED … read-only` MUST DENY ✓ (observable post-seed; antes fallaba cerrado en connect por el orden upstream connect→policy).
- leak check CLEAN; sin mutación en `.71`; sin restart de Gateway/Core. Única intervención en mcps: `docker restart ssh-mcp` tras agotar el pool de 64 sesiones con probes init-only por llamada (quirk registrado en runbook/skill; container healthy de vuelta, config intacto).

GAP-ECHO-004 → **CLOSED**. El prerrequisito de observación runtime directo de CERT-E04-01 queda cubierto (viewer SSH + observabilidad). Deuda separada NO bloqueante: host key de `.71` idéntica a `sqx-zeus` (rotación owner-side sugerida).

### Post-condición remediation (verificada)

- Drift cero: mounts/puertos/red/policy de ambos containers idénticos al baseline; resto de containers del plane sin tocar; config.toml byte-identical; scripts de smoke eliminados de mcps y Daedalus (`/tmp` limpio verificado en ambos).
- Ningún secret mostrado: bearers solo por stdin entre hosts; sha256 usados como verificación de presencia.


## Run

- **Fecha:** 2026-09-14 · **Ejecutor:** agente (sesión ZCode, superficie única)
- **Método:** sondas físicas por la superficie MCP real (identidad, lectura, diagnóstico, mutaciones controladas DEV con cleanup, pruebas negativas seguras). Sin mocks, sin SSH directo, sin acceso a secretos.
- **Alcance respetado:** sin writes PROD, sin stop/restart de servicios, sin etcd/firewall/secretos, sin cerrar carriles ni tareas, sin tocar product source.
- **Cleanup:** completo y verificado (topic `mcp-cert-20260914-a` ausente; `mcp-cert-20260913-150530` en 0 particiones en eliminación final; colecciones Mongo de sonda eliminadas; `sessions=0` en SSH al cierre).

## Matriz de superficies

| Capability | Ambiente / target | Identidad verificada | Verbos probados (físicos) | Prohibición verificada | Veredicto |
|---|---|---|---|---|---|
| `aranea-postgres-ro` | PROD `echo` @ 192.168.31.220 | `mcp_echo_prod_ro` | `execute_sql` SELECT (schemas, tablas, grants, pg_roles) | Writes: bloqueo en doble capa (validador MCP rechaza no-SELECT; grants = SELECT-only en 76 tablas, no super, sin `hdb_catalog` visible) | **PASS** con finding M3 |
| `aranea-postgres-rw` | DEV `echo-develop` | `mcp_echo_dev_rw` | Temp-table create/insert/select/drop; introspección grants | DDL: `CREATE TABLE echo.*` → `permission denied for schema echo` (DML sin DDL) | **PASS** |
| `aranea-mongo-forge-ro` | `forge` (mongod único) | preconfigured RO | `list-databases`, `list-collections`, `find` sobre datos reales (`wfm_runs` 1204 docs) | `$out/$merge` → "In readOnly mode…" server-side; sin tools mutadoras expuestas | **PASS** con finding M1 |
| `aranea-mongo-forge-rw` | `forge` | preconfigured RW | create-collection, insert-many, find read-back, drop-collection (round-trip completo) | — | **PASS** |
| `aranea-hasura-prod-ro` | Hasura CE v2.38.0 PROD | admin server-side RO | `get_version`, `get_inconsistent_metadata` (consistente), `export_metadata` | Superficie = exactamente 4 tools client-side; sin `run_sql`/reload/mutadores | **PARTIAL** — `get_schema` falló ×2 (Connection closed → Not connected → server desconectado); H1 |
| `aranea-hasura-dev-admin` | Hasura CE v2.38.0 DEV | admin | `get_version`, `get_inconsistent_metadata` (consistente), `reload_metadata` (mutación idempotente), `run_sql` (falló: no existe source `default`) | `apply_metadata`/`clear_metadata`/`drop_inconsistent` no ejercidos por diseño (clase destructiva sin necesidad) | **PARTIAL** (administración probada; SQL data-plane sin fuente `default`) |
| `aranea-kafka-dev-admin` | Kafka DEV 6 brokers @ 192.168.31.44 (cp-kafka 7.6.1 + ZK) | admin | `describe_cluster`, `list_topics` (118), `list_consumer_groups` (12 `echo-statefun-*`), create/produce/consume/`alter_configs` incremental (retention.ms verificado con source dinámico)/describe_configs/delete | Sin capability PROD (structurally absent) | **PARTIAL** — `delete_topic` eventual: éxito declarado ≠ eliminación; requirió retry y el residual `mcp-cert-20260913-150530` sobrevivió una sesión completa (M4) |
| `aranea-flink-dev-admin` | Flink 1.14.3 + StateFun DEV @ docker-echo-dev | admin REST | `get_cluster_info` (1 TM, 2 slots), `list_jobs` (`StatefulFunctions` RUNNING, 28/28 tasks), `get_flink_config` (RocksDB, checkpoint 120s, restart fixed-delay) | Sin mutaciones de control plane por scope; sin SQL tools | **PASS** (lectura/control-plane); `list_jars` → 404 `/jars` (M7) |
| `aranea-ssh` | 6 perfiles | `echo-dev` (zeus/hera/kronos), `worker-kronos\echo-dev` (mt5-kronos + operator), `root` (docker-echo-dev) | `list-connections` (6, `sessions=0`), `read-command whoami` ×6, `run-command` en operators (docker ps → statefun-master/worker, hasura-graphql healthy, portainer), `list-sessions` final vacío | **ROTO:** `run-command` en viewer `mt5-kronos` **ejecutó** el comando (H2); `read-command` rechaza compuestos (`&&`) y `docker ps --format` (M8) | **PARTIAL** — H2 |

## Hallazgos (gaps y severidades)

| # | Sev | Hallazgo | Evidencia | Acción sugerida |
|---|---|---|---|---|
| H1 | HIGH | `export_metadata` de Hasura expone `database_url` con credenciales embebidas de `echo_prod` **y** `echo_test` (`postgres://echo_user:***@192.168.31.220:5432/…`) hacia cualquier agente con capability RO/DEV; además revela webhooks internos (192.168.31.71:8090). El secreto NO se persiste en el vault. | Export real 2026-09-14 | Mover credenciales a env vars de Hasura / redaction server-side en el backend MCP antes de tratar RO como seguro para agentes no confiables |
| H2 | HIGH | Boundary viewer/operator no aplicado: `run-command` ejecutó en `mt5-kronos` (rol `viewer`) — regresión vs certificación 2026-09-13 ("rechazado por diseño en viewer") | `echo probe-should-be-denied` devolvió salida en viewer | Revisar config enforcement server-side de `aranea-ssh` con autoridad admin de `mcps` (lane T6); mientras tanto, no tratar `viewer` como read-only |
| M3 | MEDIUM | `mcp_echo_prod_ro` sin límites temporales: `statement/lock/idle_in_transaction = 0/0/0` (roles DEV tienen 1min/5s/1min) | `current_setting` en PROD | `ALTER ROLE … IN DATABASE echo` con los mismos límites que DEV |
| M4 | MEDIUM | `delete_topic` Kafka: respuesta "success" no es prueba de eliminación (async/requiere retry); el residuo del smoke 2026-09-13 sobrevivió >1 día | Dos deletes con éxito + persistencia posterior; limpieza final 2026-09-14 | Documentar semántica eventual en [[aranea-kafka-mcp]]; post-condición obligatoria = `partitions=[]`/ausencia en `list_topics` |
| M5 | MEDIUM | `get_schema` de Hasura PROD no demostrable: 2 intentos con caída de transporte posterior | "Connection closed" → "Not connected" → server desconectado | Diagnosticar timeout/tamaño de introspección en proxy/backend; superficie PROD queda 3/4 verbs |
| M6 | MEDIUM | Doc drift: nota del proyecto dice `postgres-ro`→`echo-develop` con timeouts 60s/5s/60s; realidad: RO=PROD `echo` sin timeouts, RW=DEV. El router [[aranea-mcps-expert]] sí coincide con la realidad | Identidad + settings físicos 2026-09-14 | Corregir el Estado actual del proyecto en su próximo touch (fuera del alcance de esta run) |
| M7 | LOW | `list_jars` Flink → HTTP 404 `/jars` (endpoint no disponible en este deployment) | Intento real | Anotar como límite de la capability en [[aranea-flink-mcp]] |
| M8 | LOW | `read-command` rechaza comandos compuestos (`&&`) y `docker ps --format '{{…}}'` (clasificador); obliga a `run-command` para lecturas Docker | Rechazos "read-only commands, got: safe" | Ajustar allowlist o documentar patrón de comandos simples |
| I9 | INFO | Mongo RO y RW llegan al **mismo mongod** (lista de DBs y tamaños idénticos): la separación RO/RW es de autoridad MCP, no de ambiente físico | `list-databases` idénticos | Etiquetar como instancia única en runbook; no presentar "PROD/DEV" donde hay una sola instancia |
| I10 | INFO | Residuos de certificación previa (`mcp-cert-20260913-150530`, colección `__mcp_access_probe` vacía) existían antes de esta run; ambos limpiados | list/describe + drop verificados | Adoptar post-condición de cleanup obligatoria en toda certificación |

## Superficies sin capacidad certificada (gaps, no bloquean esta run)

| Recurso | Estado | Clase |
|---|---|---|
| Observación runtime Echo (Core/Gateway/Bridge; runtime vivo real `192.168.31.71` = `prod.echo.gateway.lab.aranea`; `.211` muerto) | CERTIFICADA 2026-09-15: viewer SSH `echo-runtime-prod` PASS end-to-end (identity/runtime/listeners/negative H2) + observabilidad PROD operativa (`aranea-observability-ro`); Gateway/Core RUNNING, Bridge NOT_DEPLOYED | `CERTIFIED` (prerrequisito de observación de CERT-E04-01 cubierto) |
| etcd | Sin capability; existe como servicio de red del homelab | `UNKNOWN_NEEDS_SOURCE_PROOF` |
| Observabilidad (Jaeger/OpenSearch/OTel; `docker-observability` en hades) | Targets MCP planeados no desplegados (OBS3) | `REQUIRED_LATER` |
| Temporal | T5 deferred por decisión owner | `REQUIRED_LATER` (deferred) |
| Kafka PROD / Flink PROD | Capabilities reservadas no creadas (KAFKA2-PROD, FLINK2-PROD) | `REQUIRED_LATER` (deferred) |
| MinIO/S3 | Fuera del plane actual | `LEGACY_OR_UNUSED` (sin dependencia demostrada desde Echo) |
| MT4/MT5 (MetaEditor golden path) | Identidades re-verificadas hoy; compile golden certificado históricamente 2026-09-10, no re-ejecutado aquí | `REQUIRED_NOW` (base OK para CERT-F04-01) |

## Prohibiciones respetadas

Sin writes PROD (Kafka/Hasura/etcd/PG), sin migraciones ni metadata mutations PROD, sin stop/restart de Flink/Bridge/Gateway/Core, sin rotación de secretos ni cambios de firewall, sin trading real, sin exponer secretos en el vault, sin tocar Echo Forge ni product source. Las mutaciones quedaron acotadas a DEV con post-condición y verificación en el mismo ambiente.

## Conclusión

El access plane es **operacional y parcialmente certificado**: las bases de datos (PG PROD-RO/DEV-RW, Mongo RO/RW), Kafka DEV, Flink DEV y SSH operator cubren las necesidades de diagnóstico y smoke del carril DEV. La observación directa del runtime Echo (prerrequisito directo de CERT-E04-01/T21) quedó **resuelta** el 2026-09-15: owner seed instalado en `.71` y viewer `echo-runtime-prod` certificado end-to-end desde Daedalus (GAP-ECHO-004 CLOSED; identity/runtime/listeners/negative H2 PASS). El trigger de reactivación del backlog de certificación queda **abierto** — todas las capabilities requeridas están operacionales y certificadas; el delta de readiness correspondiente vive en [[Echo + Echo Forge — Deferred Certification Backlog]].
