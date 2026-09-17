---
type: skill
schema_version: 1
name: aranea-mcps-expert
description: Selecciona y gobierna capabilities MCP Aranea para agentes de desarrollo bajo aranea-agent-dev; ambiente, autoridad, estado certificado y runbook. Nunca se activa para MELI/corporativo.
scope: area
created: "2026-09-11"
updated: "2026-09-17"
area: "[[Aranea]]"
entities:
  - "[[Aranea]]"
related:
  - "[[AGENT-PLATFORM - MCP Access Plane - Architecture]]"
  - "[[Daedalus — Development Agents MCP Access & Gaps]]"
  - "[[aranea-ssh-mcp]]"
  - "[[aranea-postgres-mcp]]"
  - "[[aranea-mongodb-mcp]]"
  - "[[aranea-hasura-mcp]]"
  - "[[aranea-kafka-mcp]]"
  - "[[aranea-flink-mcp]]"
  - "[[aranea-observability-mcp]]"
  - "[[aranea-temporal-mcp]]"
  - "[[aranea-minio-mcp]]"
  - "[[aranea-etcd-mcp]]"
  - "[[aranea-mcp-capability-plane]]"
aliases:
  - aranea-mcps-expert
  - aranea mcp
  - mcp access plane
  - usar mcp
  - mcp ssh
  - mcp postgres
  - mcp mongo
  - mcp hasura
  - mcp kafka
  - mcp flink
  - mcp observability
  - mcp grafana
load_policy: manual
indexable: true
index_priority: high
tags:
  - kind/skill
  - scope/area
  - area/aranea
  - tech/mcp
  - action/mcp-routing
---

# aranea-mcps-expert

## Purpose

Router agent-facing para seleccionar el ambiente, la capability, el privilegio mínimo y el runbook del MCP Access Plane Aranea sin compartir credenciales finales ni mezclar PROD/DEV. Activar exclusivamente bajo [[aranea-agent-dev]] antes de usar un `aranea-*`; no activar para trabajo local sin MCP. **MUST NOT activate for Mercado Libre / MELI infrastructure, databases, repositories, hosts, credentials or corporate systems** (usar [[meli-agent-dev]]).

## Canonical Authority / Minimal Read

1. Leer esta skill; elegir primero ambiente y luego capability/autoridad. Hay **13 capabilities registradas/certificadas server-side al 2026-09-17** (puertos 3000–3012). Un endpoint sano o un smoke de Cursor no prueban automáticamente acceso de ZCode/Codex.
2. Para inventario fechado por cliente y necesidades Echo/Forge exclusivamente debidas a MCP, leer [[Daedalus — Development Agents MCP Access & Gaps]] (`10-projects/Aranea/AGENT-PLATFORM/agentes/workstreams/DAEDALUS-DEVELOPMENT-MCP-ACCESS.md`). Es una matriz de acceso, NO otro proyecto ni una SPEC.
3. Cargar sólo el runbook mecánico de la familia elegida en `VAULT_ROOT/30-resources/runbooks/`. No duplicar pasos operativos aquí. Si se agrega, reemplaza o reinstala una capability, cargar además [[AGENT-PLATFORM - MCP Access Plane - Architecture]].
4. Si cruza control plane + host/runtime, cargar también [[aranea-ssh-mcp]] (ejemplo Flink DEV: `aranea-flink-dev-admin` REST y `docker-echo-dev-operator` Docker). Para auth/discovery/sesiones/transporte del plano, [[aranea-mcp-capability-plane]].
5. Si hay contradicción temporal, preferir la certificación material más reciente y el runbook específico sobre snapshots históricos; no inventar un PASS con documentación únicamente.

Runbooks: [[aranea-ssh-mcp]], [[aranea-postgres-mcp]], [[aranea-mongodb-mcp]], [[aranea-hasura-mcp]], [[aranea-kafka-mcp]], [[aranea-flink-mcp]], [[aranea-observability-mcp]], [[aranea-temporal-mcp]], [[aranea-minio-mcp]], [[aranea-etcd-mcp]], [[aranea-mcp-capability-plane]]. La arquitectura común de backend/proxy/secrets pertenece a [[AGENT-PLATFORM - MCP Access Plane - Architecture]].

## Procedure

### 1. Boundary y ambiente

Si el target es MELI/corporativo, STOP. Para Aranea, elegir ambiente antes de autoridad: no pasar a DEV para leer o mutar PROD, ni reutilizar un token/usuario de mayor privilegio para superar un `POLICY_DENIED`.

### 2. Elegir capability certificada (inventario al 2026-09-17)

| Necesidad / ambiente | Capability | Autoridad y límite |
|---|---|---|
| Echo PostgreSQL PROD | `aranea-postgres-ro` | RO sobre target/schema permitido; no DML/DDL. |
| Echo PostgreSQL DEV | `aranea-postgres-rw` | data RW; no asumir CREATE en schema `echo`; workflow de migración DEV demostrado por Hasura admin `run_sql`, no cambiar el rol PG preventivamente. |
| MongoDB Forge PROD | `aranea-mongo-forge-ro` | 18 tools RO. |
| MongoDB Forge DEV | `aranea-mongo-forge-rw` | 27 tools, mutaciones con scope/post-condición. |
| Hasura PROD | `aranea-hasura-prod-ro` | metadata/control strict-RO; **3 tools** (`get_inconsistent_metadata`, `get_schema`, `get_version`); `export_metadata` eliminado por exposición upstream. No GraphQL data-plane ni SQL. |
| Hasura DEV | `aranea-hasura-dev-admin` | 9 tools de metadata/control, incluye `run_sql`; no es cliente GraphQL genérico. |
| Kafka DEV | `aranea-kafka-dev-admin` | 19 tools de topic/config/producer/consumer/groups/offsets; PROD no cubierto. `alter_configs` conserva semántica incremental certificada. |
| Flink DEV control | `aranea-flink-dev-admin` | 22 tools REST, sin SQL; host/docker se opera por SSH autorizado. |
| Flink/StateFun host DEV | `aranea-ssh` + `docker-echo-dev-operator` | root-equivalent **sólo** en host DEV; seguir runbook Flink y autoridad Portainer stack 1. |
| SQX runtime Zeus/Hera/Kronos | `aranea-ssh` + `sqx-zeus`/`sqx-hera`/`sqx-kronos` | operator writable como `echo-dev` no-root; preferir `read-command` en inspecciones. |
| MT4/MT5 worker-kronos | `aranea-ssh` + `mt5-kronos` / `mt5-kronos-operator` | viewer para lecturas allowlisted; operator `echo-dev` no-admin para operaciones autorizadas. Evidencia SYSTEM por JSON sólo con operator (ver abajo). |
| Echo runtime PROD | `aranea-ssh` + `echo-runtime-prod` | viewer RO certificado 2026-09-15; Gateway/Core RUNNING, Bridge NOT_DEPLOYED al corte. `run-command` POLICY_DENIED, no restart/config. Logs productivos por observabilidad. |
| Grafana/Prometheus/Loki ARGUS | `aranea-observability-ro` | 22 tools RO, queries bounded, sin Jaeger toolset ni dashboard/alert admin. |
| Temporal SQX | `aranea-temporal-ro` | 28 tools strict RO, namespaces `sqx-dev`, `sqx`, `sqx-prop`; no start/signal/cancel/terminate. |
| MinIO S3 acotado | `aranea-minio-ro` | 9 tools listadas; IAM List `deploy`+`examples`, Get `deploy/worker/sqx/*` y objetos permitidos de `examples`; deny backups; put/copy/delete bloqueados por read-only. **ACTIVE/server+Cursor certificado 2026-09-17**, no lectura global de Forge. |
| etcd acotado | `aranea-etcd-ro` | 4 tools RO, 8 prefixes, exclusión secret-name, caps 200 keys/4KB; sin write/watch. **ACTIVE/server+Cursor certificado 2026-09-17**; cluster sin auth/TLS es deuda separada, nunca bypass directo. |

Las 13 capacidades son 1 SSH + 2 PostgreSQL + 2 MongoDB + 2 Hasura + Kafka + Flink + observabilidad + Temporal + MinIO + etcd. `aranea-minio-ro` y `aranea-etcd-ro` **ya existen**; cualquier nota previa que las declara BLOCKED era histórica antes de su despliegue. Su alcance sigue limitado a los runbooks citados.

Kafka PROD (`aranea-kafka-prod-ro`, `aranea-kafka-prod-ops`) y Flink PROD (`aranea-flink-prod-ro`) son nombres/planes diferidos, NO capabilities certificadas; no usar DEV como sustituto. Jaeger directa por MCP no tiene capability certificada, aunque el datasource Jaeger sea visible en Grafana. Telegram no figura como MCP certificado para agentes Daedalus: el gateway Telegram de Hermes es separado y no prueba acceso de coding agents; definir operación real antes de diseñar wrapper/MCP. Ninguna ausencia por sí sola bloquea Echo/Forge si existe otro camino autorizado que ya satisface el contrato.

### 3. Evidence publisher Windows

`AraneaEvidencePublish` (SYSTEM, cada 5 min) publica `C:\ProgramData\Aranea\evidence\stager-evidence-latest.json`, consumido vía `aranea-ssh` + **`mt5-kronos-operator`** como `echo-dev` no-admin usando `Get-Content`/`Get-Item` read-only. **ACTIVE/CERTIFIED 2026-09-17, owner seed resuelto**: SYSTEM, self-hash, segunda publicación, ACE read-without-write, negativos y worker 0.2.98 hash exacto documentados en [[aranea-ssh-mcp]]. El profile viewer `mt5-kronos` + `sftp-download` da `POLICY_DENIED` 3/3 (el viewer SFTP de la nota H2 2026-09-15 era Linux efímero; no generalizar). No ampliar viewer ni elevar `echo-dev`.

Certificación de runtime: `generated_at_utc` ≤ 15 min, `partial=false`, `evidence.inspector_sha256` igual a registro y `run_identity=SYSTEM`. `health_stale_after_hours=8` es sólo observación health, no despliegue. Reporte inexistente/STALE ⇒ UNKNOWN y diagnóstico del publisher mediante capacidades existentes; no inspector one-shot ni owner gate por inercia. Evidencia SYSTEM es lectura, NO autorización para modificar servicio, task, releases ni ACL.

### 4. Verificar consumidor real

La secuencia 2026-09-16 normalizó Cursor/ZCode/Codex (Cursor 11/11; ZCode 10/10 heredado; Codex 10/10 tras owner kor y `bearer_token_env_var`). El 2026-09-17 las nuevas Temporal/MinIO/etcd obtuvieron server/certificación Cursor; ZCode y Codex requieren su patcher/smoke tri-client posterior con la identidad `kor`, aún sin PASS de estas 3. No afirmar 13/13 en los tres clientes sin E2E separado. Usar config/chain reales, no tokens inventados ni prueba de otro cliente. Procedimiento de onboarding: [[aranea-mcp-capability-plane]].

### 5. Ejecutar mínimo privilegio y tratar boundaries

- `read-command` para inspecciones SSH aunque profile operator; mutaciones sólo target exacto, blast radius, rollback/post-condición, verificación. `approvalPolicy="auto"` NO es aprobación humana. `privileged-command` no concede sudo/admin si usuario OS no lo tiene.
- Datos/control plane: ejecutar sólo operación permitida en ambiente correcto. Hasura PROD es strict-RO sin export; Kafka DEV incremental configs; Flink REST no shell/Docker. No inventar capabilities para esquivar permisos.
- `401` ⇒ revisar autenticación cliente/servidor sin imprimir bearer; `POLICY_DENIED`/Access Denied ⇒ boundary, no ampliar ACL/policy automáticamente; timeout ⇒ bounded scope; `isError=false` aislado no garantiza éxito de una tool. La sesión hasura/mcp-proxy vieja puede devolver `-32603 Not connected` tras muerte del hijo; inicializar sesión nueva con fix g010; `-32001` sid inexistente, `-32000` header faltante, `202` sin sid no equivale a initialize exitoso. No atribuir ese defecto a SSH/Flink.
- Para nuevos MCP: evidencia de necesidad y failure path, identidad upstream dedicada, separación bearer cliente/upstream, backend no publicado, pin/digest, tool surface y negativos, server + consumer smoke y rollback. Ver arquitectura; no crear rutas ad-hoc.

## Output

```text
Environment:  <PROD|DEV|runtime>
Capability:   <aranea-* + profile exacto>
Authority:    <viewer|operator|RO|RW|admin + usuario OS efectivo>
Consumer:     <Cursor|ZCode|Codex|otro> / PASS|NOT_CERTIFIED
Operation:    <acción exacta>
Evidence:     <resultado vivo, schema/freshness si corresponde>
Mutation:     <none | target+rollback/post-condition+verificación>
Boundary:     <none | error/policy exactos, sin bypass>
```

## Hard Rules

- Aranea-only bajo [[aranea-agent-dev]]; jamás MELI/corporativo.
- Ambiente primero; ningún token/identidad PROD usado en DEV ni DEV usado para PROD por conveniencia.
- El appliance `mcps` aloja MCPs Docker/Portainer: no instalar allí clientes ad-hoc de servicios destino ni convertirlo en jump host.
- Nunca pedir, imprimir, copiar al vault, logs, prompts ni repos bearer tokens, contraseñas, API secrets o private keys; secret references server-side.
- No usar endpoint directo cuando existe capability MCP canónica ni alterar ACL/privilegios/red como workaround automático.
- Hasura PROD sin export/SQL/mutación; Kafka/FlinK DEV no concede PROD; MinIO RO no concede RW ni backups; etcd RO no autoriza endpoint anónimo; Temporal RO no habilita control; SSH operator no crea OS admin.
- Skills consumidoras referencian este router y runbooks; no duplicar inventarios/endpoints. No copiar esta skill a `80-agents/skills/` ni duplicar runbooks fuera de `30-resources/runbooks/`.
