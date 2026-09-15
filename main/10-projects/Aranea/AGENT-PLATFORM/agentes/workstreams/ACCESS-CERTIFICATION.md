---
type: note
status: active
area: "[[Aranea]]"
parent: "[[AGENT-PLATFORM - MCP Access Plane]]"
created: "2026-09-14"
updated: "2026-09-14"
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
```

Ninguna superficie obtiene PASS incondicional: hay dos hallazgos HIGH (boundary viewer SSH no aplicado; credenciales upstream expuestas por `export_metadata`) y varias superficies con verbos no demostrables o no ejercidos por diseño. No se declara ningún acceso nuevo certificado más allá de lo listado; el trigger de reactivación del [[Echo + Echo Forge — Deferred Certification Backlog]] **no** queda abierto por esta run.

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
| Observación runtime Echo (Core/Gateway/Bridge HTTP, host 192.168.31.71:8090 visto en webhooks Hasura) | Sin capability ni perfil SSH | `REQUIRED_LATER` (prerrequisito CERT-E04-01) |
| etcd | Sin capability; existe como servicio de red del homelab | `UNKNOWN_NEEDS_SOURCE_PROOF` |
| Observabilidad (Jaeger/OpenSearch/OTel; `docker-observability` en hades) | Targets MCP planeados no desplegados (OBS3) | `REQUIRED_LATER` |
| Temporal | T5 deferred por decisión owner | `REQUIRED_LATER` (deferred) |
| Kafka PROD / Flink PROD | Capabilities reservadas no creadas (KAFKA2-PROD, FLINK2-PROD) | `REQUIRED_LATER` (deferred) |
| MinIO/S3 | Fuera del plane actual | `LEGACY_OR_UNUSED` (sin dependencia demostrada desde Echo) |
| MT4/MT5 (MetaEditor golden path) | Identidades re-verificadas hoy; compile golden certificado históricamente 2026-09-10, no re-ejecutado aquí | `REQUIRED_NOW` (base OK para CERT-F04-01) |

## Prohibiciones respetadas

Sin writes PROD (Kafka/Hasura/etcd/PG), sin migraciones ni metadata mutations PROD, sin stop/restart de Flink/Bridge/Gateway/Core, sin rotación de secretos ni cambios de firewall, sin trading real, sin exponer secretos en el vault, sin tocar Echo Forge ni product source. Las mutaciones quedaron acotadas a DEV con post-condición y verificación en el mismo ambiente.

## Conclusión

El access plane es **operacional y parcialmente certificado**: las bases de datos (PG PROD-RO/DEV-RW, Mongo RO/RW), Kafka DEV, Flink DEV y SSH operator cubren las necesidades de diagnóstico y smoke del carril DEV. No se alcanza `ACCESS_CERTIFICATION_PASS` por H1/H2 y porque la observación del runtime Echo (prerrequisito directo de CERT-E04-01/T21) sigue sin capability. El trigger de reactivación del backlog de certificación **permanece cerrado**; el delta de readiness correspondiente vive en [[Echo + Echo Forge — Deferred Certification Backlog]].
