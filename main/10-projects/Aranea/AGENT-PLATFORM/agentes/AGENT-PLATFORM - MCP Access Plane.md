---
type: project
schema_version: 1
owner: agent
root: false
status: active
priority: P1
area: "[[Aranea]]"
parent: "[[AGENT-PLATFORM-OWNER-PROJECT]]"
sprint:
start: 2026-09-07
due:
progress: 85
repo:
jira:
prs:
aliases:
  - MCP Access Plane
  - Centralización MCP
  - MCP Gateway
tags:
  - kind/project
  - area/aranea
  - project/aranea-agent-platform
  - tech/mcp
created: "2026-09-07"
updated: "2026-09-13"
---

# AGENT-PLATFORM - MCP Access Plane

> [!info]+ Access plane compartido para agentes
> **Padre:** [[AGENT-PLATFORM-OWNER-PROJECT]] · **Owner:** agent · **Estado:** active · **Prioridad:** P1

## 🎯 Objetivo

- Convertir el host MCP existente de Aranea en un access plane reutilizable para Hermes, Daedalus y agentes futuros, centralizando sesiones, credenciales reales, perfiles de acceso, auditoría y políticas sin repartir secretos de los servicios destino entre máquinas o runtimes.
- Adoptar MCPs existentes antes de construir; modificar o forkear sólo cuando un gap real de seguridad, persistencia o caso de uso quede demostrado.

## 📊 Estado actual

- T0, T2, T3 y T4 cerrados. T1 continúa WIP como contrato transversal. El carril funcional inmediato pasa a **ARGUS / Observability**; T5 Temporal queda diferido, no cancelado, hasta cerrar el baseline y access path de observabilidad.
- `progress: 85` conserva el avance histórico del scope previo a ARGUS; no se recalcula hasta dimensionar el workstream de observabilidad con evidencia real.
- `mcps` es un LXC dedicado con Docker + Portainer; IP actual `192.168.31.219`, considerada mutable y no parte del contrato estable. `mcps.lab.aranea.cl` es el endpoint estable usado por consumidores.
- SSH MCP operativo en una sola instancia/puerto con seis perfiles: read-only `sqx-zeus`, `sqx-hera`, `sqx-kronos`, `mt5-kronos`; writable/operator `mt5-kronos-operator` y `docker-echo-dev-operator`.
- Las host keys ED25519 de todos los targets están pinneadas y validadas. Hera y Kronos regeneraron keys únicas porque las VMs clonadas compartían originalmente la identidad SSH de Zeus.
- La identidad SSH dedicada `echo-dev@mcps`, fingerprint `SHA256:2Qv9f2AREQyse50bGYaTLc1PHK43gvuf3xgv5TTJ+I0`, se mantiene centralizada. La key genérica `mcp-access@mcps` queda fuera del diseño y no debe autorizarse. `docker-echo-dev-operator` usa una key dedicada propia, separada de SQX/MT5.
- En Linux SQX existe usuario remoto dedicado `echo-dev`, password bloqueado, sin sudo ni grupos extra. En `mt5-kronos` existe usuario local Windows `echo-dev`, no-admin, autenticado por public key. `docker-echo-dev-operator` entra como `root@192.168.31.75` por key-only y es root-equivalent por diseño DEV.
- `tufantunc/ssh-mcp` v2.8.0 está pinneado a tag `v2.8.0` / commit `d2d769684701e0939c1d8e56cbdde3d77fed53ef`, imagen local `local/ssh-mcp:2.8.0-d2d7696`, ejecutando como usuario no-root.
- Transporte HTTP SSH activo con bearer obligatorio, rate limit, protección de Host y `hostKeyMode=strict`; endpoint estable `http://mcps.lab.aranea.cl:3000/`.
- Cursor/Daedalus consume `aranea-ssh` de forma persistente: bearer cargado automáticamente por el entorno de KDE, sin `export` manual ni lanzamiento de Cursor desde consola.
- Multi-target PASS desde Cursor/MCP: `read-command` validado en los cuatro perfiles viewer; `run-command` rechazado por diseño en viewer y validado en `mt5-kronos-operator` como `worker-kronos\\echo-dev` y en `docker-echo-dev-operator` como `root@docker-echo-dev` con Docker/Compose operativo.
- Golden path MT4 PASS vía MCP: transferencia/copia de fuentes, compilación con MetaEditor en `master_test_001`, resolución del mirror de includes bajo el AppData de `echo-dev` y generación de `reference_v3.ex4` con 0 errors / 0 warnings.
- PostgreSQL MCP cerrado sobre `echo-develop`: `crystaldba/postgres-mcp` pinneado a commit `15c8e33353546148acc2d8bd784551cf3905d1e2`, imagen local `local/postgres-mcp:0.3.0-15c8e33`, runtime no-root `999:999`, con backends separados RO/RW detrás de proxies Nginx autenticados por bearer.
- Endpoints estables PostgreSQL: `http://mcps.lab.aranea.cl:3001/mcp` → `mcp_echo_ro` / restricted y `http://mcps.lab.aranea.cl:3002/mcp` → `mcp_echo_rw` / unrestricted. Los backends MCP no publican puertos al host; sólo los proxies exponen `3001` y `3002`.
- Cursor/Daedalus consume `aranea-postgres-ro` y `aranea-postgres-rw` de forma persistente mediante variables cargadas por KDE; ambos capabilities fueron validados desde el agente real contra `echo-develop`.
- `mcp_echo_ro` tiene CONNECT + USAGE + SELECT sólo sobre schema `echo`; no ve `hdb_catalog` y no posee permisos de escritura. `mcp_echo_rw` conserva RW sobre `echo` sin elevar privilegios globales.
- Los roles PostgreSQL MCP tienen límites scoped a `echo-develop`: `statement_timeout=60s`, `lock_timeout=5s`, `idle_in_transaction_session_timeout=60s`. Un `psql` nativo como `postgres` permanece en `0/0/0`, demostrando convivencia sin alterar clientes normales.
- El upstream PostgreSQL no ofrece límite genérico de filas ni timeout CLI para `execute_sql`; no se forkea por anticipación. La restricción temporal se aplica en PostgreSQL por rol/database. En restricted mode, un rechazo de policy puede volver como texto de error con `isError=false`, por lo que consumidores no deben interpretar ese flag como única señal de éxito.
- MongoDB MCP cerrado sobre `forge`: upstream oficial `mongodb-js/mongodb-mcp-server` pinneado a release `v2.1.1` / commit `2e8eae98d1301ca48f1e81273a3f3d5c5820f216`, imagen local `local/mongodb-mcp:2.1.1-2e8eae9`, con backends RO/RW internos y proxies Nginx bearer separados.
- Endpoints MongoDB estables: `http://mcps.lab.aranea.cl:3003/mcp` (`aranea-mongo-forge-ro`) y `http://mcps.lab.aranea.cl:3004/mcp` (`aranea-mongo-forge-rw`). Los backends no publican host ports.
- Mongo RO fue certificado con 18 tools sin mutadores; Mongo RW con 27 tools, incluyendo `insert-many`, `update-many`, `delete-many`, `create-*`, `drop-*` y `rename-collection`. El path normal usa `connectionId="preconfigured"`.
- El MongoDB de desarrollo mantiene `security.authorization` desactivado por decisión owner mientras Forge está en desarrollo; no se hardenea como parte de T4. La separación agent-facing sigue protegida por bearer + split RO/RW MCP. `mongosh` nativo permanece válido para operación humana.
- Hasura MCP quedó cerrado end-to-end con dos capabilities: `aranea-hasura-prod-ro` en `http://mcps.lab.aranea.cl:3005/mcp` y `aranea-hasura-dev-admin` en `http://mcps.lab.aranea.cl:3006/mcp`. Ambos backends son internos y sólo Nginx publica host ports.
- Hasura DEV administra el control plane con 9 tools (`apply_metadata`, `clear_metadata`, `drop_inconsistent_metadata`, `export_metadata`, `get_inconsistent_metadata`, `get_schema`, `get_version`, `reload_metadata`, `run_sql`). Hasura PROD usa una variante strict-RO construida desde source pinneado y expone exactamente 4 tools server-side: `export_metadata`, `get_inconsistent_metadata`, `get_schema`, `get_version`; no existe `run_sql`, reload ni mutadores de metadata.
- Cursor real certificó ambos Hasura MCP contra GraphQL Engine CE `v2.38.0` con metadata consistente. El `mcp_auth` mostrado por Cursor en PROD no apareció en `tools/list` server-side y no se considera parte de la superficie Hasura ni ampliación de autoridad.
- Kafka DEV MCP cerrado end-to-end como `aranea-kafka-dev-admin` en `http://mcps.lab.aranea.cl:3007/mcp`. El backend interno usa `wklee610/kafka-mcp` v2.0.0 pinneado a `0b3bf477ac482468fbd9bbafedf056d0ee83f325`, FastMCP `3.0.1`, `confluent-kafka` `2.13.0` y patch Aranea para `incremental_alter_configs`; expone exactamente 19 tools y fue certificado desde Cursor con smoke admin completo sobre recursos temporales.
- Flink DEV MCP cerrado end-to-end como `aranea-flink-dev-admin` en `http://mcps.lab.aranea.cl:3008/mcp`. Backend `vaquarkhan/flink-mcp-enterprise-server` `0.3.1` pinneado a `981bbeff3ed7f897ca7c5bde20f36669d5e93bc4`, patch Aranea compatible con Flink `1.14.3`, imagen `local/flink-mcp:0.3.1-981bbef-aranea2-flink1.14`, exactamente 22 tools y cero SQL tools. `get_cluster_info`/`list_jobs`, Daedalus y Cursor PASS.
- El host/runtime Flink DEV queda separado del control plane: `aranea-ssh` + `docker-echo-dev-operator` administra filesystem/Docker/lifecycle como root. El stack canónico es Portainer stack `1`; host source-of-truth `/var/lib/docker/volumes/portainer_data/_data/compose/1/docker-compose.yml`. Config bind-mounted vive en `/root/statefun/conf/flink-conf.yaml` y `/root/statefun/modules`.
- Cursor/Daedalus tiene actualmente nueve capabilities MCP certificadas: `aranea-ssh`, PostgreSQL RO/RW, Mongo Forge RO/RW, Hasura PROD RO/DEV admin, Kafka DEV admin y Flink DEV admin.
- La fuente canónica agent-facing del capability plane es [[aranea-mcps-expert]] (`30-resources/agents/skills/aranea-mcps-expert/SKILL.md`), exclusiva de Aranea y explícitamente prohibida para MELI/corporativo. Los runbooks mecánicos viven en AGENTS OS: [[aranea-ssh-mcp]], [[aranea-postgres-mcp]], [[aranea-mongodb-mcp]], [[aranea-hasura-mcp]], [[aranea-kafka-mcp]], [[aranea-flink-mcp]] y [[aranea-mcp-capability-plane]]. Las skills de dominio sólo deciden qué evidencia necesitan.
- `echo-forge-wfm-troubleshooting` fue refactorizada para conservar routing/conocimiento de dominio y delegar cualquier operación `aranea-*` a `aranea-mcps-expert`, eliminando duplicación de endpoints/permisos/transport semantics.
- Hardening genérico no necesario para desbloquear el uso actual — validación explícita de sesiones background, timeout extremo y revisión operativa de audit trail — se difiere a T6, donde se consolidarán health/logs/rotación/rollback y runbook transversal.
- Incidente 2026-09-13: `aranea-ssh` alcanzable en `http://mcps.lab.aranea.cl:3000/`, `/health` devuelve `200 healthy=true configured=true`, pero `initialize` autenticado devuelve `503` por límite de 64 sesiones. La observación server-side y el reinicio acotado no pudieron ejecutarse porque la autoridad administrativa existente para `mcps`/hades no está disponible en esta sesión; causa material permanece `UNKNOWN` y T6 sigue abierto.
- Recheck 2026-09-13: `aranea-ssh` quedó utilizable antes de la revalidación, sin acción de recovery ejecutada por el agente. `initialize`, `tools/list`, `resources/list` y cinco ciclos secuenciales con `DELETE` de sesión pasaron; los cuatro perfiles viewer (`sqx-zeus`, `sqx-hera`, `sqx-kronos`, `mt5-kronos`) respondieron `whoami` y `list-connections` mantuvo `sessions=0`. Veredicto operativo: `PASS / CLOSED — ARANEA SSH MCP HEALTH RESTORED`; causa del agotamiento histórico permanece `UNKNOWN` por falta de evidencia server-side retrospectiva.
- Workstream Kafka MCP por entorno:
  - **fase 1 / DEV: PASS / CLOSED** — cluster real en LXC `docker-kafka` con ZooKeeper, 6 brokers y capability `aranea-kafka-dev-admin`; endpoint `:3007/mcp`, bearer independiente, backend sin host port, 19 tools, integración Daedalus/Cursor y golden admin smoke certificados;
  - **fase 2 / PROD: DEFERRED** — cluster Kafka de tres VMs distribuidas entre Zeus, Hera y Kronos; capabilities futuras separadas `aranea-kafka-prod-ro` y `aranea-kafka-prod-ops`; requiere discovery propio antes de congelar listeners/security/runtime/boundaries.
- Workstream Flink MCP por entorno:
  - **fase 1 / DEV: PASS / CLOSED** — Flink `1.14.3` + StateFun `3.2.0` en `docker-echo-dev`; capability `aranea-flink-dev-admin` `:3008/mcp`, 22 tools exactas sin SQL, backend privado, integración Daedalus/Cursor y operator host `docker-echo-dev-operator` certificados;
  - **fase 2 / PROD: DEFERRED** — capability futura `aranea-flink-prod-ro` strict-RO; no reutilizar DEV admin ni el operator root DEV.

### ARGUS / Observability — baseline registrado 2026-09-12

- ARGUS conserva **Jaeger v2.9.0** como backend/query de traces; no se migra a Tempo sin evidencia material.
- Pipeline real de traces: `Echo / Forge → OTLP :4317/:4318 → Jaeger → OpenSearch`.
- Pipeline real de metrics/logs: `Echo / Forge → OTLP :14317/:14318 → OTel Collector → Prometheus/Loki`.
- El OTel Collector actual no tiene pipeline `traces`; esa separación es parte del baseline y no debe colapsarse por conveniencia.
- Echo es el golden baseline de telemetría. Forge se corrige sólo después de comparar configuración y evidencia E2E contra Echo; no se toca Echo para arreglar Forge.
- OpenSearch permanece loopback-only (`127.0.0.1:9200`). El estado `yellow` single-node observado corresponde principalmente a réplicas internas y queda fuera del P1 inmediato.
- Sampling objetivo `100%` y retención objetivo `30 días` están **pendientes de verificación contra estado actual**; documentación histórica no se considera autoridad suficiente.
- Targets MCP planeados, aún no desplegados: `aranea-observability-ro` y `aranea-jaeger-ro`, ambos read-only.

## 🧱 Entrega de desarrollo

_No aplica por ahora — la primera etapa es discovery y configuración operativa sobre infraestructura existente. Si una tarea requiere cambiar código, configuración versionada, schemas o infraestructura mediante repositorio, se registrarán repo/branch/base y SPECs antes de implementar ese cambio._

## 🧩 Subproyectos

- Ninguno.

## ✅ Tareas

> [!note]+ Fuente única de planificación
> Estas tareas `#owner/agent` viven sólo en este proyecto. Cada tarea debe poder cerrarse y validarse de forma independiente antes de avanzar a la siguiente.

> [!example]- Roadmap incremental
> %% Estados: [ ] To Do · [/] WIP · [r] Review · [x] Done · [-] Canceled. %%
> - [x] T0 Inventariar el host MCP existente: runtime, MCPs instalados, versiones, transporte, puertos, autenticación, persistencia, secretos, usuarios de servicio, red, logs y forma de despliegue #owner/agent #type/research #area/aranea
> - [/] T1 Definir y congelar el contrato mínimo de acceso: consumidores, aliases/profiles, least privilege, ubicación de secretos, autenticación cliente→MCP, auditoría, política de red y separación entre credenciales del MCP y credenciales del servicio destino #owner/agent #type/research #area/aranea
> - [x] T2 Seleccionar y validar SSH MCP para uso real de agentes: host-key strict, perfiles read/operator, bearer cliente→MCP, least privilege por target, acceso multi-host, transferencia de archivos, ejecución controlada y cero private keys entregadas al agente. Hardening transversal de background/timeout/audit pasa a T6 #owner/agent #type/admin #area/aranea
> - [x] T3 Seleccionar y validar PostgreSQL MCP con una sola base de desarrollo: perfiles RO/RW, credencial centralizada, límites de query/timeout y convivencia con `psql` nativo #owner/agent #type/admin #area/aranea
> - [x] T4 Seleccionar y validar MongoDB MCP con una sola base de desarrollo: perfiles RO/RW, `readOnly`/protecciones equivalentes, límites de consulta y convivencia con `mongosh` nativo #owner/agent #type/admin #area/aranea
> - [ ] T5 **DEFERRED** — Seleccionar y validar Temporal MCP: comenzar read-only con allowlist de namespaces; evaluar `signal/start/cancel` sólo después de demostrar la necesidad y el modelo de policy correspondiente #owner/agent #type/admin #area/aranea
> - [ ] T6 Consolidar las capabilities aprobadas en el host central, integrar al menos Hermes y Daedalus, demostrar que ambos consumen capabilities sin recibir credenciales reales de los servicios destino, y dejar health checks, logs/audit, background/timeout si aportan valor, rotación/rollback y runbook operativo mínimo #owner/agent #type/admin #area/aranea
> - [x] KAFKA0-DEV Descubrir el Kafka DEV real (LXC + ZooKeeper), validar bootstrap/security/listeners y network path desde `mcps`, seleccionar implementación MCP y certificar tool surface administrativa requerida para `aranea-kafka-dev-admin` antes del deployment #owner/agent #type/research #area/aranea
> - [x] KAFKA1-DEV Desplegar y validar `aranea-kafka-dev-admin` en `mcps`, con bearer independiente, secretos fuera de repo, backend no expuesto directamente, integración Daedalus/Cursor y smoke real de administración sobre DEV #owner/agent #type/admin #area/aranea
> - [ ] KAFKA2-PROD **DEFERRED** — descubrir y diseñar boundaries `aranea-kafka-prod-ro` / `aranea-kafka-prod-ops` sobre el cluster de tres VMs Zeus/Hera/Kronos cuando se abra explícitamente el carril PROD #owner/agent #type/research #area/aranea
> - [x] FLINK0-DEV Descubrir Flink/StateFun DEV real, validar REST/network/runtime, seleccionar backend MCP, congelar compatibilidad con Flink 1.14.3 y definir boundary control-plane vs host/runtime #owner/agent #type/research #area/aranea
> - [x] FLINK1-DEV Desplegar/certificar `aranea-flink-dev-admin` y `docker-echo-dev-operator`, integrar Daedalus/Cursor, recuperar source-of-truth Portainer y documentar lifecycle seguro #owner/agent #type/admin #area/aranea
> - [ ] FLINK2-PROD **DEFERRED** — diseñar y certificar `aranea-flink-prod-ro` strict-RO en carril separado cuando PROD se abra explícitamente #owner/agent #type/research #area/aranea
> - [/] OBS0 Verificar baseline ARGUS sin mutaciones: sampling Jaeger real, servicios Jaeger reales, policy ISM `jaeger-30d-delete` y aplicación efectiva sobre índices Jaeger #owner/agent #type/research #area/aranea
> - [ ] OBS1 Comparar Forge telemetry contra Echo golden baseline y demostrar E2E con acción real → trace real → Jaeger → spans esperados → logs correlacionables #owner/agent #type/research #area/aranea
> - [ ] OBS2 Cerrar correlación operacional `logs ↔ trace_id ↔ Jaeger` y semántica mínima de errores sin promover IDs de alta cardinalidad a labels Prometheus #owner/agent #type/research #area/aranea
> - [ ] OBS3 Seleccionar y validar acceso read-only para `aranea-observability-ro` y `aranea-jaeger-ro`; preferir MCPs existentes y crear/forkear sólo ante gap demostrado #owner/agent #type/admin #area/aranea
> - [ ] OBS4 Materializar como máximo los dashboards operacionales `Echo — Runtime`, `Forge — Pipeline` y `ARGUS — Platform Health`, sólo con preguntas operacionales concretas #owner/agent #type/admin #area/aranea
> - [ ] OBS5 **DEFERRED** — Saneamiento secundario: OpenSearch yellow single-node, capacidad/cardinalidad Prometheus, Promtail → Alloy y upgrades; no mezclar con OBS0–OBS4 sin necesidad material #owner/agent #type/admin #area/aranea

## 📆 Bitácora

- **2026-09-14** — Access certification run `ACCESS_CERTIFICATION_PARTIAL`. Verificación física de las 9 capabilities desde la superficie MCP real: PG PROD-RO/DEV-RW, Mongo RO/RW, Hasura PROD-RO (3/4 verbs; `get_schema` con caída de transporte) y DEV admin, Kafka DEV, Flink DEV y SSH (6 perfiles). Hallazgos HIGH: `run-command` ejecutó en viewer `mt5-kronos` (boundary no aplicado) y `export_metadata` Hasura expone credenciales upstream de `echo_prod`/`echo_test` al agente. Anomalía abierta: el residual `mcp-cert-20260913-150530` reaparece tras deletes exitosos con líder rotando (posible re-creación por cliente externo); `delete_topic` documentado como eventual. Cleanup de sondas propias verificado; sin writes PROD, sin restarts, sin cerrar tareas. Artefacto: [[ACCESS-CERTIFICATION]]; delta de readiness en el backlog de certificación. Nota: el Estado actual de esta nota conserva el drift PostgreSQL-RO detectado (corrección diferida a su próximo touch).
- **2026-09-13** — Flink DEV MCP `PASS / CLOSED`. Se desplegó `aranea-flink-dev-admin` en `:3008/mcp` usando `vaquarkhan/flink-mcp-enterprise-server` `0.3.1` pinneado a `981bbeff3ed7f897ca7c5bde20f36669d5e93bc4` con patch Aranea compatible con Flink `1.14.3`; exactamente 22 tools, cero SQL tools, backend sin host port, auth proxy separada y Daedalus/Cursor PASS. Se añadió `docker-echo-dev-operator` a `aranea-ssh`, certificado como `root@192.168.31.75` para filesystem/Docker/lifecycle DEV. El stack declarativo real se recuperó desde Portainer stack `1` en `/var/lib/docker/volumes/portainer_data/_data/compose/1/docker-compose.yml`; el config runtime vive en `/root/statefun`. Runbook canónico: [[aranea-flink-mcp]]. PROD `aranea-flink-prod-ro` queda diferido.
- **2026-09-13** — Kafka DEV MCP `PASS / CLOSED`. Discovery confirmó `docker-kafka` en `192.168.31.44` como cluster DEV real de 6 brokers `cp-kafka:7.6.1` + ZooKeeper, listeners externos `19091–19096` y path `PLAINTEXT` desde `mcps`. Se adoptó `wklee610/kafka-mcp` v2.0.0 pinneado a `0b3bf477ac482468fbd9bbafedf056d0ee83f325`; la imagen Aranea fija `confluent-kafka=2.13.0` y FastMCP `3.0.1`. El `alter_configs` upstream se parchó a `incremental_alter_configs` porque la API legacy puede revertir configs no incluidas. Deployment final: backend privado `kafka-mcp-dev-admin`, proxy bearer `kafka-mcp-auth-dev-admin`, endpoint `http://mcps.lab.aranea.cl:3007/mcp`, `401` sin bearer y exactamente 19 tools autenticadas. Cursor real validó `describe_cluster`/`list_topics` y un golden admin smoke `mcp-cert-*` pasó create topic, config incremental, partitions, produce/consume, consumer-group offsets/reset y delete topic sin tocar recursos preexistentes. Runbook canónico: [[aranea-kafka-mcp]]. KAFKA0-DEV y KAFKA1-DEV cerrados; KAFKA2-PROD permanece diferido.
- **2026-09-13** — Recheck posterior al incidente: el servicio ya no estaba saturado; `initialize` autenticado `200` con `Mcp-Session-Id`, `tools/list` expuso la superficie SSH esperada, `resources/list` expuso `ssh://connections`, y `list-connections` mostró los cinco perfiles con `sessions=0`. Smokes `read-command whoami` PASS en `sqx-zeus`, `sqx-hera`, `sqx-kronos` y `mt5-kronos`. Lifecycle acotado: 5/5 ciclos `initialize=200`, `notifications/initialized=202`, `tools/list=200`, `DELETE=200`; handshake posterior y cierre PASS. No se ejecutó restart ni mutación; root cause histórico sigue `UNKNOWN`, sin regresión de autoridad observada. Veredicto: `PASS / CLOSED — ARANEA SSH MCP HEALTH RESTORED`; T6 mantiene hardening de lifecycle/health/reaper.
- **2026-09-13** — Incident recovery de `aranea-ssh`: baseline de cliente confirmó bearer `SET`, endpoint alcanzable, request sin auth `401` esperado, `/health` `200`, y dos intentos autenticados de `initialize` con `503` `Server is at its session limit (64)`. No se observaron sesiones MCP/HTTP, registry, edades, TCP, FDs, logs ni config efectiva porque no hubo autoridad administrativa para inspeccionar el LXC 113; SSH con la identidad local disponible fue rechazado por `root@mcps` y `root`/`agent_ro` en hades. No se reinició ningún servicio, no se cambió límite/auth/profile/bearer/network y no se ejecutaron profile smokes ni lifecycle test. Clasificación: `UNKNOWN` con handoff `BLOCKED — MCP RECOVERY FAILED`; requiere retomar con autoridad administrativa del runtime propio de `mcps` antes de decidir recovery o root cause.
- **2026-09-12** — Corrección de boundary Kafka: el rollout queda environment-first. DEV se implementa primero sobre el cluster LXC/ZooKeeper con capability administrativa `aranea-kafka-dev-admin`; debe permitir creación/eliminación de topics, cambios de configuración, produce/consume y administración/inspección de consumer groups/offsets. PROD queda diferido hasta cerrar DEV y se modelará sobre el cluster KRaft de tres VMs como capabilities separadas `aranea-kafka-prod-ro` y `aranea-kafka-prod-ops`. La entrada previa `aranea-kafka-ro` queda supersedida.
- **2026-09-12** — Abierto inicialmente `Kafka MCP / aranea-kafka-ro` como EXTEND del MCP Access Plane; supersedido por la corrección de boundary del mismo día antes de cualquier cambio de infraestructura.
- **2026-09-12** — Hasura MCP workstream `PASS / CLOSED`. Se desplegaron y certificaron `aranea-hasura-dev-admin` (`:3006`) y `aranea-hasura-prod-ro` (`:3005`) contra Hasura CE `v2.38.0`. DEV expone 9 tools admin. PROD no confía sólo en upstream `--read-only`: usa variante strict-RO desde commit `9ba59f273daf42205919e6d43e27d2876a6e0b32`, sin `run_sql`/reload/mutadores y con exactamente 4 tools server-side. Ambos fueron validados desde Cursor con metadata consistente; secretos upstream permanecen server-side en `mcps`.
- **2026-09-12** — Proyecto existente **EXTEND**, no CREATE: ARGUS/Observability pasa a ser el workstream inmediato del MCP Access Plane. Se registra el baseline de pipelines separados Jaeger vs OTel Collector, Echo como golden baseline, targets MCP RO futuros y gates OBS0–OBS5. T5 Temporal queda diferido. No se modifica runtime ARGUS ni se declara sampling/retención cerrados sin evidencia actual.
- **2026-09-11** — `aranea-mcps-expert` quedó canónica en el vault (`30-resources/agents/skills/`) y los runbooks en AGENTS OS. Symphony conserva sólo un pointer de discovery.
- **2026-09-11** — T4 MongoDB MCP cerrado end-to-end. Se adoptó `mongodb-js/mongodb-mcp-server` v2.1.1 pinneado a `2e8eae98d1301ca48f1e81273a3f3d5c5820f216`, imagen `local/mongodb-mcp:2.1.1-2e8eae9`. Deployment final separa backend+proxy RO (`:3003/mcp`) y RW (`:3004/mcp`), con bearer obligatorio y backends sin host port. RO expone 18 tools sin mutadores; RW 27 tools con mutación. Cursor/Daedalus muestra ambos capabilities conectados junto con SSH y PostgreSQL. Mongo `security.authorization` queda deliberadamente OFF durante desarrollo por decisión owner; hardening DB se pospone al freeze productivo. Se creó `aranea-mcps-expert` como única fuente agent-facing de capabilities Aranea y `echo-forge-wfm-troubleshooting` quedó reducida a routing de dominio.
- **2026-09-11** — T3 PostgreSQL MCP cerrado end-to-end. Deployment persistente en `mcps` con backend+proxy separados para RO (`:3001/mcp`, `mcp_echo_ro`, restricted) y RW (`:3002/mcp`, `mcp_echo_rw`, unrestricted), bearer dedicado por capability y backends sin host port. Cursor/Daedalus carga ambos bearer automáticamente vía KDE y validó identidad/base real desde los dos MCP. RO sólo expone schema `echo` y excluye `hdb_catalog`; RW mantiene permisos acotados a `echo-develop`. Ambos roles heredan `statement_timeout=60s`, `lock_timeout=5s`, `idle_in_transaction_session_timeout=60s`; `psql` nativo como `postgres` sigue `0/0/0`. El upstream no ofrece timeout/límite genérico para `execute_sql`, por lo que no se forkea: el hard limit temporal vive en PostgreSQL. POCs y red temporal eliminados tras el gate final.
- **2026-09-11** — PostgreSQL MCP POC autenticada PASS en `mcps`: source `crystaldba/postgres-mcp` pinneado a `15c8e33353546148acc2d8bd784551cf3905d1e2`, imagen local no-root `local/postgres-mcp:0.3.0-15c8e33`, Streamable HTTP conectado como `mcp_echo_rw` a `echo-develop`. Discovery, sesión MCP y RW se validaron sin mutación real. Como el upstream no aporta bearer auth, se validó Nginx 1.29.8 pinneado por digest como proxy en red privada: `401` sin bearer y `200 + Mcp-Session-Id + tools/call` con bearer dedicado.
- **2026-09-10** — T2 SSH MCP cerrado para uso real de agentes. Se validó `mt5-kronos-operator` con `run-command` como usuario Windows no-admin y el golden path MT4 `upload/copy → compile` sobre `master_test_001`; `reference_v3.mq4` compiló a `.ex4` con 0 errors / 0 warnings. La resolución de `#include` de MetaEditor ejecutado como `echo-dev` usa el AppData de ese usuario y requiere mirror del mismo hash de terminal.
- **2026-09-10** — Cursor/Daedalus quedó con autoload persistente de `ARANEA_SSH_MCP_BEARER` mediante entorno de usuario/KDE; `aranea-ssh` conecta verde al abrir Cursor normalmente, sin launcher de consola.
- **2026-09-10** — SSH MCP expandido a cuatro targets read-only en una sola instancia/puerto: `sqx-zeus`, `sqx-hera`, `sqx-kronos` y `mt5-kronos`; se añadió `mt5-kronos-operator` para mutación/ejecución controlada.
- **2026-09-10** — En Hera y Kronos se regeneraron host keys ED25519 únicas porque las VMs clonadas compartían la misma key de Zeus. `mt5-kronos` quedó autenticando por public key con usuario local no-admin `echo-dev`; se corrigió `AuthorizedKeysFile` porque OpenSSH Windows resolvía la ruta relativa bajo `C:\\WINDOWS`.
- **2026-09-10** — Primer circuito MCP completo validado: Daedalus resuelve y alcanza `mcps.lab.aranea.cl`, autentica con bearer, inicializa MCP Streamable HTTP y ejecuta `read-command("whoami")`; la private key SSH nunca se entrega a Daedalus.
- **2026-09-10** — `ssh-mcp` v2.8.0 se construyó desde source pinneado (`v2.8.0`, commit `d2d769684701e0939c1d8e56cbdde3d77fed53ef`) como `local/ssh-mcp:2.8.0-d2d7696`. Smoke test stdio PASS; transporte HTTP PASS con health, bearer auth, allowed Host, rate limit y host-key strict.
- **2026-09-08** — Primer acceso SSH real validado para `echo-dev`: `mcps` conecta a `sqx-zeus.lab.aranea.cl` mediante identidad dedicada, trust store dedicado y host-key strict; la sesión remota ejecuta como `echo-dev` en `sqx-ulab-zeus-0`.
- **2026-09-08** — El perfil inicialmente llamado `sqx-dev` se renombra a `echo-dev` porque representa capacidad de desarrollo/diagnóstico Echo/Echo Forge y no debe quedar acoplado al runtime SQX.
- **2026-09-08** — T2 iniciado con `sqx-zeus.lab.aranea.cl` (`192.168.31.101`) como primer target. Host key ED25519 validada local/remotamente y agregada al trust store dedicado.
- **2026-09-08** — DNS de `mcps` corregido: resolver directo Pi-hole `192.168.31.31`, search domain `lab.aranea.cl`.
- **2026-09-07** — T0 cerrado. Se confirmó `mcps` como LXC dedicado con Docker + Portainer, IP actual `192.168.31.219`. El stack PostgreSQL anterior se bajó con `docker compose down`; fueron removidos sus 9 contenedores y la red `postgres_mcp_net`. Verificación posterior: sólo `portainer` permanecía activo.
- **2026-09-07** — Proyecto creado para materializar incrementalmente el Capability Plane ya definido en [[AGENT-PLATFORM-ARCHITECTURE]]. Scope inicial congelado a SSH, PostgreSQL, MongoDB y Temporal; MinIO, Kafka y observabilidad quedan fuera hasta estabilizar este patrón.

## 🧭 Decisiones

- D1: centralizar credenciales y sesiones MCP en un host dedicado; los agentes consumen capabilities y perfiles, no secretos de los servicios destino.
- D2: se conserva el LXC `mcps` y Portainer como baseline operativo; una VM nueva sólo se justifica con evidencia material.
- D3: un host central no implica una identidad omnipotente. Cada MCP/perfil usa credenciales finales separadas y least-privilege.
- D4: mantener clientes nativos (`ssh`, `psql`, `mongosh`, Temporal CLI`) donde aporten valor; MCP es la capa reusable para agentes.
- D5: la IP `192.168.31.219` es ubicación actual, no identidad estable. Consumidores usan DNS `mcps.lab.aranea.cl`.
- D6: las private keys SSH permanecen en el access plane; los agentes no reciben las credenciales finales.
- D7: `echo-dev` es identidad limitada para desarrollo/diagnóstico Echo/Echo Forge; perfiles de mayor privilegio se diseñan aparte y sólo cuando existe necesidad demostrada.
- D8: permisos remotos se agregan sólo cuando una necesidad concreta falle y pueda expresarse con least privilege; no ampliar ACLs preventivamente.
- D9: consumidores acceden al SSH MCP mediante Streamable HTTP autenticado con bearer; el bearer es independiente de la identidad SSH final.
- D10: múltiples targets SSH se concentran en una sola instancia/puerto de `ssh-mcp`; la separación se realiza mediante perfiles.
- D11: para archivos de texto/código hacia targets SSH se usa `sftp-upload`; no se levantan servidores HTTP temporales ad-hoc. Binarios/grandes deben usar staging autorizado.
- D12: T2 se considera cerrado cuando el camino real de agentes queda validado con perfiles RO/operator, strict host keys, auth MCP, least privilege, transferencia y ejecución. Hardening transversal no bloqueante (background/timeout/audit operacional) se concentra en T6 para evitar sobrediseñar cada capability.
- D13: PostgreSQL MCP se adopta desde `crystaldba/postgres-mcp` pinneado por commit e imagen local; las credenciales DB permanecen sólo en `mcps` y el runtime usa identidad PostgreSQL dedicada least-privilege.
- D14: como PostgreSQL MCP no ofrece bearer auth nativo, el endpoint remoto se protege mediante proxy Nginx pinneado, bearer dedicado y red Docker privada; el backend MCP no se publica directamente a consumidores.
- D15: PostgreSQL RO y RW se publican como capabilities separados, cada uno con bearer e identidad DB propia; los límites temporales se aplican mediante settings `ALTER ROLE ... IN DATABASE echo-develop`, evitando modificar clientes nativos o forkear el MCP sin necesidad demostrada.
- D16: en `postgres-mcp` restricted, `isError` no es autoridad suficiente para decidir éxito de `execute_sql`; un rechazo de policy puede representarse como contenido textual de error con `isError=false`.
- D17: MongoDB MCP se adopta desde `mongodb-js/mongodb-mcp-server` v2.1.1 pinneado por commit; RO y RW se publican como capabilities separados detrás de bearer proxy y los backends no se exponen al host.
- D18: el path normal Mongo para agentes usa `connectionId="preconfigured"`; la presencia de `connect` no autoriza URIs arbitrarias. En desarrollo se conserva `security.authorization` OFF por decisión owner y el hardening del servidor queda fuera de T4.
- D19: `aranea-mcps-expert` es la única fuente agent-facing para seleccionar/usar capabilities MCP Aranea. Las skills de dominio deben referenciarla y no duplicar endpoints, permisos, profiles o transport semantics. La skill MUST NOT activarse para MELI/corporativo.
- D20: la skill canónica `aranea-mcps-expert` vive en el vault bajo `30-resources/agents/skills/`; los runbooks mecánicos viven en `30-resources/runbooks/`. `80-agents/skills/` queda reservado al core AGENTS OS. Symphony puede conservar un pointer de discovery, no una segunda autoridad.
- D21: ARGUS/Observability se incorpora como workstream principal del MCP Access Plane. Jaeger se conserva; Echo es golden baseline; sampling/retención se verifican antes de mutar; accesos agent-facing nuevos parten read-only.
- D22: observabilidad no reutiliza por defecto identidades o privilegios existentes sólo por conveniencia. `aranea-observability-ro` y `aranea-jaeger-ro` deben demostrar boundaries read-only propios antes de considerarse cerrados.
- D23: Hasura se integra como admin/control-plane MCP, no como GraphQL data-plane. DEV usa `aranea-hasura-dev-admin`; PROD usa `aranea-hasura-prod-ro`; CRUD genérico de datos sigue prefiriendo PostgreSQL MCP.
- D24: Hasura PROD exige tool surface strict-RO verificable. El upstream `--read-only` no basta si conserva tools administrativas; la variante certificada elimina `run_sql`, `reload_metadata` y mutadores, dejando exactamente cuatro tools de inspección server-side.
- D25: Kafka se despliega por entorno y DEV va primero. `aranea-kafka-dev-admin` expone autoridad administrativa sobre el cluster DEV LXC/ZooKeeper y queda cerrado antes de abrir PROD. PROD se diseña después como `aranea-kafka-prod-ro` y `aranea-kafka-prod-ops`, sin reutilizar por comodidad la autoridad de DEV.
- D26: Kafka DEV adopta `wklee610/kafka-mcp` pinneado por commit con FastMCP `3.0.1` y `confluent-kafka` `2.13.0`. Aranea reemplaza el `alter_configs` legacy por `incremental_alter_configs` porque las APIs oficiales documentan que el alter legacy puede revertir propiedades no incluidas; cualquier rebuild que pierda este patch requiere recertificación antes de mutar configs.
- D27: Flink se separa por plano. `aranea-flink-dev-admin` administra Flink REST/control plane; filesystem/Docker/lifecycle DEV pertenece a `aranea-ssh` + `docker-echo-dev-operator`. No se introduce shell arbitrario en el backend Flink MCP para cubrir host operations.
- D28: Portainer stack `1` es la autoridad declarativa del stack Flink/StateFun DEV. Cambios sólo en bind-mounted config usan restart controlado; cambios de topology/env/ports/volumes/image usan redeploy explícito de Portainer. No usar `docker compose up -d` rutinariamente contra el YAML recuperado mientras Compose v5 proponga recreación por hash drift.

## 🔗 Docs / Links

- [[AGENT-PLATFORM-ARCHITECTURE]] — arquitectura v1 y definición del Capability Plane.
- [[AGENT-PLATFORM-OWNER-PROJECT]] — cockpit humano padre.
- [[aranea-mcps-expert]] (`30-resources/agents/skills/aranea-mcps-expert/SKILL.md`) — contrato canónico de selección/uso de capabilities MCP Aranea.
- `xKoRx/symphony/.agents/skills/echo-forge-wfm-troubleshooting/SKILL.md` — routing de dominio Echo Forge/WFM; delega acceso MCP a `aranea-mcps-expert`.
- [[aranea-ssh-mcp]] · [[aranea-postgres-mcp]] · [[aranea-mongodb-mcp]] · [[aranea-hasura-mcp]] · [[aranea-kafka-mcp]] · [[aranea-flink-mcp]] · [[aranea-mcp-capability-plane]] — runbooks mecánicos en AGENTS OS.

## 💡 Ideas

### Backlog de ideas

- MinIO/S3 permanece como candidato futuro; Kafka DEV y Flink DEV ya están cerrados. Kafka PROD y Flink PROD quedan diferidos hasta apertura explícita de sus carriles.

### Motivos / principios

- KISS/YAGNI: reutilizar el host MCP y software existente antes de crear infraestructura o código nuevo.
- Seguridad por capas: restricción de red + autenticación MCP + policy/profile + credencial final least-privilege.

### Memoria pública / interna

- **Memoria pública:** este proyecto conserva decisiones y estado durable; los contratos operativos de SSH/PostgreSQL/MongoDB/Hasura/Kafka/Flink viven en los runbooks AGENTS OS enlazados.
- **Memoria interna:** no se crea memoria adicional mientras el planificador contenga todo el estado necesario.
- **Motivo:** evitar duplicar el roadmap o la autoridad de acceso fuera del proyecto.