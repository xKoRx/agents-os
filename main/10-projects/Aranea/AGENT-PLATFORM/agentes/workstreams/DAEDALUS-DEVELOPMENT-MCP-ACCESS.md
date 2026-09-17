---
type: note
status: active
area: "[[Aranea]]"
parent: "[[AGENT-PLATFORM - MCP Access Plane]]"
created: "2026-09-17"
updated: "2026-09-17"
aliases:
  - "Daedalus — Development Agents MCP Access & Gaps"
tags:
  - area/aranea
  - tech/mcp
  - kind/access-matrix
---

# Daedalus — Development Agents MCP Access & Gaps

> Corte documental: 2026-09-17. Alcance EXCLUSIVO: capabilities MCP para coding agents de Daedalus que trabajan en Echo/Echo Forge. No es SPEC/estado de producto ni arquitectura nueva. Router: [[aranea-mcps-expert]], inventario y deployment: [[AGENT-PLATFORM - MCP Access Plane - Architecture]], procedimientos: runbooks `aranea-*-mcp`. Esta nota reconcilia evidencia de certificación ya registrada; NO es un nuevo smoke vivo.

## Estados: no confundir servidor, cliente y operación

- `SERVER CERTIFIED`: backend, proxy, auth y boundary materialmente comprobados en `mcps`.
- `CONSUMER CERTIFIED`: el CLIENTE ESPECÍFICO de Daedalus (`Cursor`, `ZCode`, `Codex`) pasó entry/env/handshake/tools/call bajo su identidad real; smoke Cursor no prueba Codex ni ZCode.
- `OPERATION CERTIFIED`: el verbo y target realmente requeridos fueron demostrados, no sólo una tool listada. `READ ONLY` no autoriza publicar, borrar ni controlar workflows.
- `ACCESS GAP`: operación sin capability cubierta ni camino alternativo autorizado demostrado. Antes de nuevo MCP: objetivo, verbo, target, error/permiso, contrato, identidad, scope, negativos, rollback y consumer smoke.

## Inventario registrado 2026-09-17: 13 capabilities

| Puerto | Capability | Authority real / límite |
|---:|---|---|
| 3000 | `aranea-ssh` | perfiles por host, SQX `echo-dev` no-root, MT5 operator `echo-dev` no-admin, Docker DEV root, Echo PROD viewer; sin OS admin universal |
| 3001 | `aranea-postgres-ro` | Echo PROD SQL RO sobre esquema permitido; sin writes/DDL |
| 3002 | `aranea-postgres-rw` | Echo DEV data RW; no asumir schema CREATE; E-05 demostró migración DEV 063 vía Hasura admin `run_sql` existente |
| 3003 | `aranea-mongo-forge-ro` | Forge PROD RO, 18 tools |
| 3004 | `aranea-mongo-forge-rw` | Forge DEV RW, 27 tools |
| 3005 | `aranea-hasura-prod-ro` | control/metadata strict-RO, 3 tools post-H1; sin `export_metadata`, SQL ni GraphQL data plane |
| 3006 | `aranea-hasura-dev-admin` | metadata/control DEV, 9 tools incluido `run_sql`; NO GraphQL data-plane genérico |
| 3007 | `aranea-kafka-dev-admin` | Kafka DEV 19 tools produce/consume/admin; PROD no cubierto |
| 3008 | `aranea-flink-dev-admin` | Flink REST/control DEV 22 tools sin SQL; Docker DEV separado por SSH |
| 3009 | `aranea-observability-ro` | Grafana/Prometheus/Loki ARGUS, 22 tools read-only bounded; SIN Jaeger toolset, sin administración dashboards/alertas |
| 3010 | `aranea-temporal-ro` | Temporal SQX 28 tools RO, namespaces sqx-dev/sqx/sqx-prop; sin start/signal/cancel/terminate |
| 3011 | `aranea-minio-ro` | S3 RO; IAM List `deploy`,`examples`; Get `deploy/worker/sqx/*` y objetos autorizados `examples`; deny backups; put/copy/delete bloqueados incluso si visibles en upstream |
| 3012 | `aranea-etcd-ro` | 4 tools lectura; 8 prefixes allowlisted, secret-names excluidos, caps 200 keys/4KB, sin put/delete/txn/watch; cluster sin auth/TLS = hardening aparte, no acceso directo |

La fotografía anterior de 11 capabilities incluía Temporal; **se sumaron MinIO y etcd**, total 13. El inventario 9 (2026-09-13) y el 11 anterior son historia, no estado vigente. MinIO/etcd certificados server-side y Cursor el 2026-09-17 según [[aranea-minio-mcp]], [[aranea-etcd-mcp]] y bitácora 2026-09-17b de [[AGENT-PLATFORM - MCP Access Plane]].

## Disponibilidad real por cliente Daedalus

- **Cursor:** las 10 capabilities base tenían E2E previo; Temporal fue incorporada y produjo inventario 11; nuevo smoke del trío Temporal+MinIO+etcd `3/3 PASS` al 2026-09-17. Es evidencia de altas del trío, NO una nueva certificación global de 13/13 ejecutada por esta nota.
- **ZCode:** baseline 10/10 desde 2026-09-16; incorporación Temporal/MinIO/etcd mediante patcher+smoke tri-client stageado, **PENDING** de evidencia bajo identidad `kor`; config 600 con bearer literal según contrato ZCode (no copiar valor a docs).
- **Codex:** baseline 10/10 desde 2026-09-16 con `bearer_token_env_var` y native consumer smoke; el trío 3010–3012 sigue **PENDING** de patcher+smoke con identidad `kor`.
- **Hermes:** es otro consumidor; su gateway Telegram NO demuestra una capability MCP Telegram expuesta a coding agents de Daedalus.

Usar `tools/list` y llamada inocua por cliente real; endpoint/container sano o config JSON/TOML no dan PASS de consumo. El patcher de tri-client está stageado en Daedalus según bitácora; sólo ejecutar bajo autoridad efectiva autorizada para los archivos de `kor`, no ampliar ACL por conveniencia ni publicar secrets.

## Windows privileged evidence: bloqueo de lectura resuelto

`AraneaEvidencePublish` task SYSTEM cada 5 min → JSON sanitizado `C:\ProgramData\Aranea\evidence\stager-evidence-latest.json` → `aranea-ssh` `mt5-kronos-operator` como `echo-dev` no-admin → `Get-Content/Get-Item` read-only. ACTIVE/CERTIFIED 2026-09-17: identidad/self-hash, dos publicaciones, consumer lectura efectiva, Write/Create DENIED y viewer negativo. `mt5-kronos+sftp-download` = `POLICY_DENIED` 3/3; el precedente viewer SFTP de Linux efímero no prueba Windows. Certificación de deploy sólo si `generated_at_utc` ≤15 min y `partial=false`; STALE/ausente ⇒ UNKNOWN, diagnosticar publisher sin owner por inercia. Reporte observó worker PID 1700 SHA release 0.2.98, pero **certificación de F04/F05 es un gate distinto**. [[aranea-ssh-mcp]]. Esta capability NO autoriza administrar servicios, tasks, ACL ni releases.

## Gaps de ACCESO MCP por operación Echo/Forge

| Necesidad | Estado demostrado | Gate mínimo para abrirla |
|---|---|---|
| Leer releases SQX en MinIO | CUBIERTO en `deploy/worker/sqx/*` y `examples` permitidos por `aranea-minio-ro` | Fuera de scope: bucket/key exactos, GET real DENIED y justificación; IAM/prefix específico o read surface existente, nunca lectura global/backups. |
| Leer goldens/resultados/artefactos durables Forge | NO ACREDITADO para corpus completo (IAM RO actual sólo abarca paths declarados) | Probar bucket/key/manifest real y GET con identidad actual. Si falla, RO acotado al corpus o API/read surface ya autorizada. |
| Publicar releases, fixtures o resultados a MinIO | NO por `aranea-minio-ro`; put/copy/delete bloqueados | Verificar primero Stager/publisher/servicio productor existente. Si no cubre: capability RW distinta, service account scoped, prefix/verbo/overwrites/rollback/negativos; nunca convertir RO en RW. |
| Iniciar, signal o cancelar workflows/campañas Temporal | NO por `aranea-temporal-ro` | Demostrar falta de control existente y fijar namespace, workflow IDs/tipos, identidad, ownership, efectos, autorización y safety. Sólo ops capability separada acotada; no tocar flujos ajenos ni trading real. |
| Escribir/CAS/configurar etcd | NO por `aranea-etcd-ro`; cluster anónimo no es permiso | Primero hardening/auth/identidades y operación/prefix concretos; escritura separada con rollback. |
| Kafka PROD / Flink PROD | NO certificado; DEV admin NO equivale PROD | Fase que lo requiera demuestra operación, cluster/job y authority específica; RO primero, ops aparte. |
| Jaeger trace/span query directa MCP | NO certificado; Grafana ve datasource pero observability MCP no tiene toolset Jaeger | Probar si consulta Grafana/otra ruta ya autorizada basta; si no, MCP Jaeger RO con consultas bounded. |
| Reiniciar/desplegar Echo PROD / controlar Bridge | NO: `echo-runtime-prod` viewer RO | Gate por servicio/operación, identidad separada, rollback y seguridad trading; no elevar viewer. |
| Windows servicio/task/release admin | NO: `mt5-kronos-operator` no-admin y evidence SYSTEM sólo lectura | Primero ruta Stager; sólo si falta acción administrativa, owner seed de operación fija acotada, no shell admin global. |
| Telegram para coding agents Daedalus | NO existe MCP Telegram certificado en este inventario. Hermes Telegram gateway es distinto. | Definir verbo: avisos de gates, leer chats o bot control. Para avisos intentar puente explícito y autorizado vía Hermes; nuevo MCP sólo si necesidad no cubierta, con chat allowlist y token server-side, send-only por defecto. Ausencia por sí sola NO es bloqueo demostrado de Echo/Forge. |
| GitHub push/integration | Fuera de familia `aranea-*`; connector/repos existentes, no nuevo MCP homelab por defecto | Autoridad por repo/branch/gate de integración en flujo GitHub correspondiente. |

## Deuda del propio acceso / documentación

- Inventario 13 en router, Architecture, capability-plane runbook e índice de runbooks. Mantener notas de 9/10/11 sólo como snapshots históricos fechados; proyecto MCP tiene bitácora más reciente que algunos resúmenes introductorios.
- ZCode/Codex para 3010–3012: PENDING consumer smoke bajo `kor`; no promover por inferencia.
- No confundir `aranea-etcd-ro ACTIVE` con hardening del cluster (aún sin TLS/auth). No extrapolar `aranea-minio-ro` a lectura de todos los buckets ni escritura.
- Todo gap nuevo exige evidencia de failure path, minimización de authority, negativa, rollback, certificación server+consumer y actualización del router/runbook. No usar Telegram/Hermes como justificación de arquitectura antes del verbo concreto.

## Fuentes

[[AGENT-PLATFORM - MCP Access Plane - Architecture]], [[aranea-mcps-expert]], [[aranea-ssh-mcp]], [[aranea-temporal-mcp]], [[aranea-minio-mcp]], [[aranea-etcd-mcp]], [[aranea-observability-mcp]], [[aranea-mcp-capability-plane]], [[ACCESS-CERTIFICATION]]. Esta nota no contiene credenciales ni sustituye el estado runtime vivo.