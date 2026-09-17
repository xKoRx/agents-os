---
type: note
status: active
area: "[[Aranea]]"
parent: "[[AGENT-PLATFORM - MCP Access Plane]]"
created: "2026-09-17"
updated: "2026-09-17"
tags:
  - area/aranea
  - tech/mcp
  - kind/access-matrix
---

# Daedalus — Development Agents MCP Access & Gaps

> Corte documental: 2026-09-17. Alcance exclusivo: capabilities del MCP Access Plane destinadas a coding agents de Daedalus para Echo/Echo Forge. NO es un estado de producto, una SPEC de Echo/Forge ni una nueva arquitectura. Fuente de routing: [[aranea-mcps-expert]]; inventario de puertos/deployment: [[AGENT-PLATFORM - MCP Access Plane - Architecture]]; procedimientos: runbooks `aranea-*-mcp`. Este corte reconcilia certificaciones ya registradas; NO constituye un nuevo smoke en vivo de los clientes.

## Semántica de estado

- `SERVER CERTIFIED`: backend/proxy y boundaries validados en el LXC `mcps`.
- `CONSUMER CERTIFIED`: cliente concreto de Daedalus comprobado con su entry/env/credencial real y una llamada inocua. El PASS de Cursor NO equivale automáticamente a ZCode o Codex.
- `NOT CERTIFIED`: la capability/operación no está demostrada; no inferir que el servicio físico no exista. `READ ONLY` nunca autoriza mutaciones.
- `ACCESS GAP`: la operación requerida no está cubierta por una capability certificada ni otro camino autorizado ya existente. Describir necesidad y gate antes de desplegar otro MCP.

## Inventario de capabilities registradas (13; 2026-09-17)

| Puerto | Capability | Alcance certificado / frontera |
|---:|---|---|
| 3000 | `aranea-ssh` | Perfiles por host; SQX operators `echo-dev` no-root; `mt5-kronos` viewer, `mt5-kronos-operator` `echo-dev` no-admin; `docker-echo-dev-operator` root DEV; `echo-runtime-prod` viewer. No implica OS admin universal. |
| 3001 | `aranea-postgres-ro` | Echo PROD, SQL RO en esquema permitido; no DDL ni writes. |
| 3002 | `aranea-postgres-rw` | Echo DEV data RW. No inferir CREATE sobre esquema `echo`; migraciones DEV E-05 usaron el workflow existente de Hasura DEV admin `run_sql`, no ampliación del rol PG. |
| 3003 | `aranea-mongo-forge-ro` | Mongo Forge PROD, 18 tools RO. |
| 3004 | `aranea-mongo-forge-rw` | Mongo Forge DEV, 27 tools incl. mutación autorizable dentro del target. |
| 3005 | `aranea-hasura-prod-ro` | Control/metadata, 3 tools estrictamente RO post-H1; no `export_metadata`, SQL, GraphQL data plane ni mutadores. |
| 3006 | `aranea-hasura-dev-admin` | Metadata/control DEV, 9 tools; `run_sql` habilitado con scope/gates DEV. No es un cliente GraphQL genérico. |
| 3007 | `aranea-kafka-dev-admin` | Kafka DEV, 19 tools; producer/consumer/admin DEV. No cubre Kafka PROD. |
| 3008 | `aranea-flink-dev-admin` | Flink REST/control DEV, 22 tools sin SQL. Host Docker DEV va por SSH `docker-echo-dev-operator`, no por este MCP. |
| 3009 | `aranea-observability-ro` | Grafana/Prometheus/Loki ARGUS, 22 tools RO y queries acotadas; NO expone toolset Jaeger ni administra dashboards/alertas. |
| 3010 | `aranea-temporal-ro` | Temporal SQX, 28 tools RO, namespaces `sqx-dev`, `sqx`, `sqx-prop`; sin start/signal/cancel/terminate. |
| 3011 | `aranea-minio-ro` | MinIO S3 RO, 9 tools registradas; IAM permite listar `deploy` y `examples`, leer sólo `deploy/worker/sqx/*` y objetos autorizados de `examples`; backups y demás prefijos denegados. Put/copy/delete listados por upstream pero bloqueados por read-only. NO es lectura global de Forge ni publicación de releases. |
| 3012 | `aranea-etcd-ro` | 4 tools de lectura, 8 prefijos allowlisted, nombres de claves secretas denegados, caps 200 keys/4KB; sin put/delete/txn/watch. El cluster subyacente sin auth/TLS es deuda de hardening separada; NO usar conexión directa como bypass del MCP. |

**Origen de la ampliación 11→13:** MinIO y etcd fueron desplegados/certificados posteriormente a la fotografía de 11 del documento de arquitectura; la sección anterior a la ampliación es histórica. Fuente de verdad por familia: [[aranea-minio-mcp]], [[aranea-etcd-mcp]] y change log del workstream MCP-trio.

## Estado de consumidores Daedalus

- **Cursor:** 11 capabilities previas verificadas y MinIO/etcd añadidas con consumer smoke `3/3` para el nuevo trío Temporal+MinIO+etcd según bitácora 2026-09-17. Esto no es un re-smoke global de las 13 en este documento.
- **ZCode:** normalización histórica 10/10 del 2026-09-16; para Temporal/MinIO/etcd se dejó patcher+smoke tri-client en Daedalus pendiente de ejecución por `kor`. No marcar las 13 visibles/funcionales sin consumer proof nuevo. Los bearers literales en config 600 de ZCode son un hecho documentado, no razón para copiarlos al vault.
- **Codex:** configuración normalizada con `bearer_token_env_var` y 10/10 smoke nativo del 2026-09-16; altas posteriores Temporal/MinIO/etcd pendientes de patcher+smoke específico. `mcp.json`/`config.toml` de `kor` no son modificables por otro usuario sin autorización.
- **Hermes:** otro consumidor; su gateway Telegram y su configuración no certifican una capability MCP Telegram disponible para los coding agents de Daedalus.

Estado de consumidor se obtiene del `tools/list`/probe actual por cliente; no inferirlo de un endpoint healthy, una nota de despliegue o la configuración de otro cliente. Patcher tri-client stageado el 2026-09-17: ejecutar/certificar únicamente con autoridad `kor` cuando el procedimiento documentado lo requiera; nunca imprimir bearer ni marcar PASS antes del resultado.

## Windows evidencia privilegiada — CERRADO para inspección

`AraneaEvidencePublish` SYSTEM cada 5 min → JSON sanitizado `C:\ProgramData\Aranea\evidence\stager-evidence-latest.json` → `mt5-kronos-operator` como `echo-dev` no-admin → `Get-Content`/`Get-Item` read-only. Estado `ACTIVE/CERTIFIED 2026-09-17`; task/SYSTEM/self-hash, lectura consumer, ACE read-without-write, dos publicaciones y viewer negativo demostrados. El viewer `mt5-kronos+sftp-download` fue `POLICY_DENIED` 3/3, no ofrecerlo como alternativa. Para certificar deploy: `generated_at_utc` ≤ 15 min y `partial=false`; reporte STALE/ausente ⇒ UNKNOWN, investigar publisher antes de requerir owner. La evidencia de worker 0.2.98/sha es disponible; el veredicto final de la campaña física Forge es independiente. [[aranea-ssh-mcp]] y [[SSH MCP — workstream del MCP Access Plane]].

## Accesos MCP que podrían faltar para Echo / Forge

| Necesidad concreta | Estado de acceso | Condición para abrir trabajo (no suponer que ya bloquea el desarrollo) |
|---|---|---|
| Lectura MinIO de releases SQX | **CUBIERTA en scope exacto** `deploy/worker/sqx/*`, y `examples` autorizados, vía `aranea-minio-ro`. | Si el artefacto requerido está fuera de IAM actual, aportar bucket/key real sin secretos, GET DENIED comprobado y ampliar sólo prefix/operación necesarios; no pedir MinIO global. |
| Lectura de golden/results/artefactos durables Forge | **NO ACREDITADA para todo el corpus**: el RO actual sólo certifica prefixes limitados; no inferir que cubra `durable/*`, manifests u otros buckets. | Fijar bucket/key + identidad del artefacto y probar GET RO. Si DENIED, SA RO dedicada/policy acotada a ese corpus o reuse de API/read-surface existente. No abrir backups. |
| Escritura/publicación MinIO de releases, fixtures o resultados | **NO CUBIERTA por `aranea-minio-ro`**; sus put/copy/delete están bloqueados. | Mostrar el flujo productor exacto y verificar primero Stager/publisher/API ya autorizados. Sólo si carece de camino: capability/identidad RW separada, prefijos, operaciones, no-overwrite/rollback, auth y probes negativos; jamás convertir RO en RW. |
| Temporal: iniciar/cancelar/señalizar workflows o detener una campaña atascada | **NO CUBIERTO** por `aranea-temporal-ro`. | Probar ausencia de un control ya existente y definir namespaces, tipos/workflow IDs permitidos, caller, autorización, semántica de cancelación, guard contra tocar flujos no propios. Crear ops capability independiente sólo por necesidad demostrada. No activar trading real como efecto colateral. |
| etcd: configurar nuevos prefijos/valores, CAS, reservas y rotación | **NO CUBIERTO** por `aranea-etcd-ro`; cluster físico abierto NO es autorización. | Primero contrato de prefijos/verbs/roles e hardening/autenticación del cluster, luego escribir con identidad separada y tests reversibles. Nunca usar root/endpoint anónimo como workaround. |
| Kafka PROD y Flink PROD (lectura/operación) | **NO CERTIFICADOS**; sólo DEV admin disponible. | Fase que necesite evidencia o control físico PROD debe demostrar operación, cluster/job exacto, lectura primero, authority/rollback y separación RO vs ops. No usar DEV como sustituto. |
| Jaeger traces directas por MCP | **NO CERTIFICADO como toolset/capability separada**; `aranea-observability-ro` cubre Prometheus/Loki/Grafana y ve Jaeger como datasource, pero no ofrece tools Jaeger. | Probar si lectura desde Grafana/otras superficies ya certificadas basta para trace-id/spans requeridos. Si no: MCP Jaeger RO de queries bounded, sin escritura ni administración. |
| Echo PROD restart/deploy/config/Bridge lifecycle | **NO CUBIERTO**: `echo-runtime-prod` es viewer RO; `docker-echo-dev-operator` no es autoridad PROD. | Gate operacional explícito por servicio/comando, identidad segregada, rollback y no trading no autorizado. No escalar viewer a root. |
| Windows admin / task/service/release control | **NO CUBIERTO**: evidencia SYSTEM es observación, `mt5-kronos-operator` sigue no-admin. | Sólo cuando release/repair autorizado necesite acción administrativa no provista por Stager. Diseñar operación fija acotada con owner seed y verificación, no shell admin genérico. |
| Telegram: enviar avisos, leer chats o controlar bot desde Daedalus | **NO MCP TELEGRAM CERTIFICADO EN INVENTARIO**. Gateway Telegram de Hermes es un servicio distinto; no probar por su mera existencia que los agentes de desarrollo pueden usarlo. | Definir verbo necesario: notificación de gates vs leer mensajes vs administrar bot. Para avisos, evaluar reutilizar Hermes por un puente explícitamente autorizado; si realmente exige MCP, wrapper acotado por chat ID allowlist, sin token al cliente, sin lectura ni comandos arbitrarios por defecto. No es bloqueo demostrado de Echo/Forge sólo por no existir. |
| GitHub integration/push | No es una familia `aranea-*` de este plano; no crear un MCP homelab por duplicación de connector GitHub existente. | Resolver la autoridad por repositorio/rama y gate de integración en su flujo específico, fuera del scope de este inventario. |

## Acciones documentales / operativas restantes del propio plane

1. Reconcilia inventario 11→13 en arquitectura, proyecto, router y runbook capability-plane. Preserva snapshots históricos etiquetados como tales; evita `BLOCKED` de MinIO/etcd como CURRENT. Documenta que la certificación Cursor ≠ ZCode/Codex.
2. Corrige heading histórico `STAGED pending owner` del evidence publisher en `aranea-ssh-mcp`; no alterar su contrato ni reclasificar F05C como producto cerrado.
3. Patcher tri-client posterior a Temporal/MinIO/etcd: `PENDING CONSUMER CERT` para ZCode/Codex mientras no exista evidencia real de 13/13. No pedir al owner comandos sin analizar primero ACL/autoridad de `kor` y la herramienta de onboarding vigente.
4. Sin nuevas capabilities por intuición: cada gap exige target/operación, fallo material del camino existente, scope de acceso, auditoría, rollback y consumer smoke; actualizar [[aranea-mcps-expert]], runbook y Architecture únicamente tras certificación.

## Fuentes canónicas

- [[AGENT-PLATFORM - MCP Access Plane - Architecture]] — arquitectura y puertos; snapshot 11 obsoleto después del MCP-trio.
- [[aranea-mcps-expert]] — elección del agente.
- [[aranea-ssh-mcp]] — Windows evidence + viewer/operator.
- [[aranea-temporal-mcp]], [[aranea-minio-mcp]], [[aranea-etcd-mcp]] — contratos actuales de las nuevas familias.
- [[aranea-observability-mcp]] — límite explícito sin Jaeger toolset.
- [[ACCESS-CERTIFICATION]] — resultados fechados de autenticación/policies; no transponer un smoke a otro cliente.
