---
type: skill
schema_version: 1
name: aranea-mcps-expert
description: Selecciona y gobierna el uso de las capabilities MCP del homelab Aranea bajo el dominio aranea-agent-dev, que es su única puerta de activación. Cargar antes de usar cualquier MCP aranea-* para elegir ambiente, capability, autoridad y runbook correctos; nunca aplica a MELI ni a sistemas corporativos.
scope: area
created: "2026-09-11"
updated: "2026-09-16"
area: "[[Aranea]]"
entities:
  - "[[Aranea]]"
related:
  - "[[AGENT-PLATFORM - MCP Access Plane - Architecture]]"
  - "[[aranea-ssh-mcp]]"
  - "[[aranea-postgres-mcp]]"
  - "[[aranea-mongodb-mcp]]"
  - "[[aranea-hasura-mcp]]"
  - "[[aranea-kafka-mcp]]"
  - "[[aranea-flink-mcp]]"
  - "[[aranea-observability-mcp]]"
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

Seleccionar cómo acceder a infraestructura, datos y control planes de Aranea mediante su capability plane MCP sin repartir credenciales finales ni mezclar ambientes.

Activar bajo el dominio [[aranea-agent-dev]] —su única puerta de entrada— antes de usar cualquier capability `aranea-*`, o cuando una skill de dominio determine que necesita acceso MCP a un host, PostgreSQL, MongoDB, Hasura, Kafka o Flink de Aranea. No activar para trabajo local que no requiere MCP. **MUST NOT activate for Mercado Libre / MELI infrastructure, databases, repositories, hosts, credentials or corporate systems** (dominio de [[meli-agent-dev]]).

## Canonical Authority

Esta skill es el router agent-facing. Los procedimientos mecánicos viven exclusivamente en `VAULT_ROOT/30-resources/runbooks/`:

- `30-resources/runbooks/aranea-ssh-mcp.md` → [[aranea-ssh-mcp]]
- `30-resources/runbooks/aranea-postgres-mcp.md` → [[aranea-postgres-mcp]]
- `30-resources/runbooks/aranea-mongodb-mcp.md` → [[aranea-mongodb-mcp]]
- `30-resources/runbooks/aranea-hasura-mcp.md` → [[aranea-hasura-mcp]]
- `30-resources/runbooks/aranea-kafka-mcp.md` → [[aranea-kafka-mcp]]
- `30-resources/runbooks/aranea-flink-mcp.md` → [[aranea-flink-mcp]]
- `30-resources/runbooks/aranea-observability-mcp.md` → [[aranea-observability-mcp]]
- `30-resources/runbooks/aranea-temporal-mcp.md` → [[aranea-temporal-mcp]]
- `30-resources/runbooks/aranea-mcp-capability-plane.md` → [[aranea-mcp-capability-plane]]

La arquitectura/deployment común para **agregar o reemplazar capabilities** vive en [[AGENT-PLATFORM - MCP Access Plane - Architecture]]. No redescubrirla desde cero salvo evidencia material de drift.

No copiar procedimientos desde esos runbooks a esta skill.

## Minimal Read

1. Leer esta skill para elegir ambiente y capability.
2. Si la tarea **agrega, reemplaza o reinstala** una capability MCP, cargar obligatoriamente [[AGENT-PLATFORM - MCP Access Plane - Architecture]].
3. Cargar sólo el runbook de la familia elegida.
4. Si la tarea cruza control plane + host/runtime, cargar también [[aranea-ssh-mcp]]; ejemplo canónico: Flink DEV usa `aranea-flink-dev-admin` para REST/control plane y `docker-echo-dev-operator` vía `aranea-ssh` para filesystem/Docker/lifecycle.
5. Cargar [[aranea-mcp-capability-plane]] sólo cuando el problema sea discovery/auth/transporte/policy del plano MCP mismo.

## Procedure

### 1. Confirmar boundary Aranea

Si el target es MELI/corporativo, detener esta skill y usar las autoridades corporativas correspondientes.

### 2. Elegir primero el ambiente

| Sistema / necesidad | Ambiente | Capability | Authority |
|---|---|---|---|
| Echo PostgreSQL consulta productiva | PROD | `aranea-postgres-ro` | read-only |
| Echo PostgreSQL lectura o mutación de desarrollo | DEV | `aranea-postgres-rw` | read/write; puede usarse para lecturas DEV sin mutar |
| Echo Forge MongoDB consulta productiva | PROD | `aranea-mongo-forge-ro` | read-only |
| Echo Forge MongoDB lectura o mutación de desarrollo | DEV | `aranea-mongo-forge-rw` | read/write; puede usarse para lecturas DEV sin mutar |
| Hasura inspección administrativa productiva | PROD | `aranea-hasura-prod-ro` | read-only estricto; exactamente 3 tools Hasura server-side (post-H1 2026-09-15; `export_metadata` eliminado) |
| Hasura administración de desarrollo | DEV | `aranea-hasura-dev-admin` | admin Hasura; mutaciones sólo con scope/post-condición explícitos |
| Kafka inspección o administración de desarrollo | DEV | `aranea-kafka-dev-admin` | admin Kafka DEV; topics/configs/partitions/produce-consume/groups/offsets |
| Flink control plane de desarrollo | DEV | `aranea-flink-dev-admin` | admin Flink REST DEV; exactamente 22 tools certificadas, sin SQL |
| Flink/StateFun host-runtime DEV | DEV runtime | `aranea-ssh` + `docker-echo-dev-operator` | root operator sobre `docker-echo-dev`; filesystem/Docker/lifecycle |
| runtime/logs/archivos SQX Zeus/Hera/Kronos | DEV runtime | `aranea-ssh` + `sqx-zeus` / `sqx-hera` / `sqx-kronos` | operator writable como `echo-dev`; no root-equivalent; preferir `read-command` para inspección y usar mutación sólo cuando la tarea lo requiera |
| Observabilidad de Aranea (Grafana/Prometheus/Loki) lectura | PROD-RO | `aranea-observability-ro` | read-only estricto; exactamente 22 tools RO (`--disable-write` + allowlist 5 toolsets); toda query bounded; administración de Grafana/dashboards NO pertenece a esta capability |
| Temporal (SQX) inspección workflows/schedules/namespaces | PROD-RO | `aranea-temporal-ro` | read-only estricto por construcción (`hardReadOnly` + `allowedNamespaces [sqx-dev, sqx, sqx-prop]`); exactamente 28 tools sin mutadores; endpoint `http://mcps.lab.aranea.cl:3010/mcp`; start/signal/cancel/terminate NO existen en la superficie |
| MT4/MT5 worker-kronos inspección | DEV runtime | `aranea-ssh` + `mt5-kronos` | viewer / read-only |
| MT4/MT5 worker-kronos mutación | DEV runtime | `aranea-ssh` + `mt5-kronos-operator` | operator writable como `echo-dev` |
| Observación runtime Echo PROD (identity/logs/listeners) | PROD runtime | `aranea-ssh` + `echo-runtime-prod` | viewer / read-only — **CERTIFICADO 2026-09-15, GAP-ECHO-004 CLOSED** (identity `echo-dev@echo` sin sudo; Gateway/Core RUNNING, Bridge NOT_DEPLOYED; negative `run-command` POLICY_DENIED; cobertura allowlist: systemctl/docker/curl/clase safe rechazados, journal propio únicamente); logs/metrics productivos por `aranea-observability-ro` (`service=echo-core`) |

**Invariante:** elegir ambiente antes que autoridad. No cambiar de ambiente para conseguir más permisos ni usar una capability DEV para verificar estado PROD.

Kafka PROD todavía no tiene capability certificada. `aranea-kafka-prod-ro` y `aranea-kafka-prod-ops` son nombres reservados para el workstream PROD diferido; no asumir que existen ni usar DEV como sustituto.

Flink PROD todavía no tiene capability certificada. `aranea-flink-prod-ro` está diferido; no usar `aranea-flink-dev-admin` ni `docker-echo-dev-operator` como sustitutos para PROD.

### 3. Elegir autoridad mínima dentro del ambiente correcto

En SSH, elegir primero el profile exacto del host y después el tool mínimo para la intención. Los tres profiles SQX (`sqx-zeus`, `sqx-hera`, `sqx-kronos`) son `operator/readOnly=false`, pero eso sólo habilita escritura bajo la identidad remota `echo-dev`: **no implica root, no obliga a mutar y no convierte una lectura en `run-command`**. Para evidencia usar `read-command`; para mutación justificada usar `run-command` o `sftp-upload`; sesiones/background/signal/privileged sólo cuando la tarea realmente los necesita. `mt5-kronos` sigue siendo viewer; `mt5-kronos-operator` es la superficie writable de ese host. `docker-echo-dev-operator` es root-equivalent sólo en ese host DEV.

`approvalPolicy="auto"` en un profile operator no equivale a human-in-the-loop: el servidor puede autoautorizar una acción clasificada como destructive/privileged. Antes de mutar, el agente debe fijar target, scope/blast radius, rollback o post-condición y luego verificar el resultado. La policy del MCP no sustituye ese gate.

En data/control-plane MCPs no inventar capabilities nuevas como workaround. En Hasura, PROD y DEV son contratos distintos: PROD es inspección estricta; DEV puede administrar metadata/DDL cuando la tarea lo requiere. En Kafka, la capability certificada actual es DEV admin: usar lecturas cuando basten y reservar mutaciones para targets explícitos, con blast radius y post-condición definidos. En Flink, usar `aranea-flink-dev-admin` para cluster/jobs/savepoints/rescale/JAR/control plane; usar `docker-echo-dev-operator` sólo cuando la acción pertenece al host/runtime como editar bind-mounted config, logs/exec Docker, restart o redeploy del stack.

Para Hasura PROD, la superficie certificada es exclusivamente:

```text
get_inconsistent_metadata
get_schema
get_version
```

Son exactamente 3 tools desde el H1 fix 2026-09-15: `export_metadata` fue ELIMINADO de la superficie PROD-RO porque exponía `database_url` con credenciales upstream embebidas. `run_sql`, `reload_metadata`, `export_metadata` y mutadores de metadata no existen en la capability PROD. No ampliar esta superficie para resolver una tarea puntual.

Para Flink DEV, SQL no forma parte del contrato actual: no hay SQL Gateway verificado y `tools/list` no expone tools SQL. No inventar SQL como workaround.

### 4. Cargar el runbook de la familia

- host/runtime → [[aranea-ssh-mcp]]
- PostgreSQL → [[aranea-postgres-mcp]]
- MongoDB → [[aranea-mongodb-mcp]]
- Hasura → [[aranea-hasura-mcp]]
- Kafka → [[aranea-kafka-mcp]]
- Flink / StateFun → [[aranea-flink-mcp]]
- Observabilidad (Grafana/Prometheus/Loki) → [[aranea-observability-mcp]]

Si se está incorporando una familia nueva, la arquitectura común se toma de [[AGENT-PLATFORM - MCP Access Plane - Architecture]] y sólo se documenta aparte lo específico del servicio.

- Temporal → [[aranea-temporal-mcp]] (nueva, 2026-09-17)
- MinIO/S3 y etcd: NO tienen capability certificada aún (workstreams abiertos 2026-09-17; MinIO espera identidad upstream dedicada, etcd carece de upstream MCP mantenible — decisión owner pendiente). No inventar capabilities como workaround.

### 5. Acotar y ejecutar

Fijar host/perfil o database/schema/table/collection/metadata object/cluster/topic/group/job/container/config exacto. Ejecutar sólo la operación necesaria. Para mutaciones, identificar primero el target en el mismo ambiente, fijar blast radius, declarar rollback/post-condición cuando corresponda, ejecutar y verificar en ese mismo ambiente.

### 6. Tratar boundaries como evidencia

- capability ausente del inventario → revisar discovery/config/env del cliente antes de culpar al backend;
- `401` → diagnosticar bearer/config del cliente sin pedir ni imprimir el secreto upstream;
- `POLICY_DENIED` / permission denied → revisar el boundary del runbook, no crear bypass;
- timeout → reducir scope/optimizar antes de ampliar policy;
- una capability configurada pero sin tools expuestas no prueba fallo del servicio destino: primero aislar cliente/auth/handshake;
- en SSH, `operator` describe superficie MCP, no privilegio OS: si `echo-dev` no puede hacer una acción, no elevar ni alterar ACLs automáticamente;
- en Hasura, `tools/list` server-side es evidencia de autoridad: no asumir que `--read-only` o el nombre del container hacen segura una capability PROD;
- sesión MCP en la familia hasura (wrappers mcp-proxy): `-32603 Not connected` en una sesión vieja ⇒ reconectar (un `initialize` fresco abre sesión nueva funcional; el fix g010 respawnea el upstream sin restart); `-32001` = session id inexistente/reapado; `-32000` = falta header de sesión; `202` sin sid = notificaciones id-less del transporte, no respuesta a `initialize`;
- `mcp_auth` visible en un cliente no cuenta como tool Hasura mientras no aparezca en `tools/list` server-side del backend;
- en Kafka, `alter_configs` debe conservar semántica incremental certificada; si cambia configs no objetivo, detener mutaciones y tratar la capability como fuera de contrato;
- en Flink, host/runtime y control plane son superficies distintas: necesidad de Docker/filesystem/restart no autoriza a meter shell arbitrario dentro del backend Flink MCP;
- en Flink, `docker compose up -d` no es una operación rutinaria mientras el stack Portainer vigente produzca hashes distintos con Compose CLI actual; seguir [[aranea-flink-mcp]].

## Output

```text
Environment: <PROD|DEV|runtime>
Capability: <aranea-*>
Authority: <viewer|operator|RO|RW|admin>
Target: <host/profile/database/collection/schema/metadata-object/cluster/topic/group/job/container>
Operation: <acción ejecutada>
Evidence: <resultado material>
Mutation: <none | target + rollback/post-condition + same-environment verification>
Boundary: <none | policy/error relevante>
```

## Hard Rules

- Esta skill es **Aranea-only** y se activa sólo bajo [[aranea-agent-dev]]; nunca usarla para MELI o sistemas corporativos.
- Elegir ambiente antes que capability/autoridad.
- PROD de datos/control plane es RO; DEV puede tener mayor autoridad sólo dentro de su capability explícita.
- Toda capability nueva debe respetar [[AGENT-PLATFORM - MCP Access Plane - Architecture]]: proxy bearer separado, backend interno sin host port, secretos upstream separados y pinning reproducible, salvo excepción explícitamente aprobada.
- `mcps` es appliance de servicios MCP Docker/Portainer, no workstation/jump host: no instalar clientes ad-hoc para administrar servicios destino.
- Nunca pedir, imprimir, copiar a documentación ni registrar bearer tokens, passwords, admin secrets o private keys.
- No saltar el proxy MCP ni usar acceso directo agent-first cuando existe capability canónica que cubre la acción.
- No cambiar ACLs/privilegios, publicar backends internos ni crear side channels como workaround automático.
- En SSH, `approvalPolicy="auto"` no cuenta como aprobación humana: mutaciones y privilegios requieren scope, rollback/post-condición y verificación definidos por la tarea/agente.
- Hasura PROD no expone SQL ni mutación de metadata; cualquier tarea que los requiera debe detenerse o moverse al ambiente/flujo correcto, no ampliar la capability dinámicamente.
- Kafka DEV admin no autoriza operaciones sobre Kafka PROD. No usar brokers/listeners PROD hasta que existan capabilities PROD certificadas.
- Flink DEV admin no autoriza PROD. Host/runtime Flink DEV se opera con el profile SSH dedicado; no ampliar el backend Flink con shell/Docker por conveniencia.
- Skills consumidoras deben referenciar esta skill en vez de duplicar endpoints, permisos o semántica MCP.
- No copiar esta skill a `80-agents/skills/` ni duplicar los runbooks fuera de `30-resources/runbooks/`.