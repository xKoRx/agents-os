---
type: runbook
schema_version: 1
scope: area
created: "2026-09-13"
updated: "2026-09-13"
area: "[[Aranea]]"
project: "[[AGENT-PLATFORM - MCP Access Plane]]"
application:
entities:
  - "[[Aranea]]"
related:
  - "[[aranea-mcps-expert]]"
  - "[[aranea-mcp-capability-plane]]"
  - "[[AGENT-PLATFORM - MCP Access Plane - Architecture]]"
  - "[[Data streaming — Kafka, Flink, EMQX]]"
aliases:
  - runbook Kafka MCP Aranea
  - aranea kafka mcp
  - mcp kafka
  - aranea-kafka-dev-admin
confidence: verified
source_session:
load_policy: manual
indexable: true
index_priority: high
tags:
  - kind/runbook
  - scope/area
  - area/aranea
  - tech/mcp
  - tech/kafka
  - action/mcp-kafka
---

# aranea-kafka-mcp

## Propósito

Operar y diagnosticar Kafka DEV de Aranea mediante la capability administrativa `aranea-kafka-dev-admin`, sin repartir acceso Kafka directo a los agentes ni exponer el backend MCP al host. El routing agent-facing vive en [[aranea-mcps-expert]], la mecánica común del plano MCP en [[aranea-mcp-capability-plane]] y la arquitectura/deployment en [[AGENT-PLATFORM - MCP Access Plane - Architecture]].

## Capability certificada

| Ambiente | Capability | Endpoint | Autoridad | Estado |
|---|---|---|---|---|
| DEV | `aranea-kafka-dev-admin` | `http://mcps.lab.aranea.cl:3007/mcp` | administración Kafka DEV | PASS / CLOSED end-to-end |

No existe capability Kafka PROD certificada. `aranea-kafka-prod-ro` y `aranea-kafka-prod-ops` pertenecen al workstream PROD diferido y no deben inventarse ni sustituirse con DEV.

## Runtime Kafka DEV verificado

Target actual:

```text
host/LXC: docker-kafka.192.168.31.1
LAN IP:   192.168.31.44
runtime:  Docker Compose project kafka
mode:     ZooKeeper clásico
Kafka:    confluentinc/cp-kafka:7.6.1
brokers:  6
```

Brokers/listeners externos certificados desde `mcps`:

```text
192.168.31.44:19091  broker 1
192.168.31.44:19092  broker 2
192.168.31.44:19093  broker 3
192.168.31.44:19094  broker 4
192.168.31.44:19095  broker 5
192.168.31.44:19096  broker 6
```

Bootstrap canónico DEV:

```text
192.168.31.44:19091,192.168.31.44:19092,192.168.31.44:19093,192.168.31.44:19094,192.168.31.44:19095,192.168.31.44:19096
```

Security protocol observado para este path: `PLAINTEXT`. No se observaron SASL/TLS/authorizer en los listeners usados por el MCP.

El LXC `docker-kafka` no expone SSH operativo para este flujo; su administración humana se hace por consola/VNC cuando sea necesaria. No asumir SSH al LXC como precondición del MCP.

## Backend MCP adoptado

Upstream:

```text
repo:    wklee610/kafka-mcp
version: 2.0.0
commit:  0b3bf477ac482468fbd9bbafedf056d0ee83f325
license: Apache-2.0
```

Runtime Aranea pinneado:

```text
confluent-kafka: 2.13.0
FastMCP:         3.0.1
image:           local/kafka-mcp:2.0.0-0b3bf47-inc1-fm3.0.1
```

FastMCP no es una capability adicional: es el framework usado por `wklee610/kafka-mcp` para implementar MCP. Aranea ejecuta el mismo servidor con transporte HTTP interno en `:8000/mcp`; Nginx sigue siendo el único listener host-facing.

El upstream declara `fastmcp>=3.0.0`, pero su `uv.lock` fijaba `3.0.1`. El Dockerfile upstream instalaba con `pip install .` y no respetaba el lock, por lo que un build inicial resolvió FastMCP `4.0.3`. La imagen certificada Aranea fija explícitamente `FastMCP==3.0.1` para reproducibilidad.

## Seguridad de alteración de configs — patch Aranea

El baseline upstream implementaba `alter_configs` con `ConfigResource.set_config()` + `AdminClient.alter_configs()`. Esa API no es segura para cambios parciales: la documentación oficial de `confluent-kafka` advierte que, al usar `alter_configs`, las propiedades no incluidas pueden volver a sus valores por defecto. Kafka marca además `alterConfigs` como deprecated desde 2.3 y recomienda `incrementalAlterConfigs`.

Aranea aplica un patch mínimo y exclusivo sobre `src/kafka_mcp/tools/admin.py`:

```python
resource.add_incremental_config(
    ConfigEntry(
        key,
        value,
        incremental_operation=AlterConfigOpType.SET,
    )
)
admin_client.incremental_alter_configs([resource])
```

Semántica certificada:

- `incremental_alter_configs` modifica sólo las entradas mencionadas y conserva el resto;
- `AlterConfigOpType.SET` fija el valor de la entrada indicada;
- Kafka soporta `IncrementalAlterConfigs` desde broker 2.3.0;
- el golden smoke DEV cambió únicamente `retention.ms` y verificó que `cleanup.policy`, `retention.bytes`, `min.insync.replicas` y otras configs permanecieran intactas.

Referencias oficiales:

- Confluent Kafka Python — `AdminClient.incremental_alter_configs`, `ConfigResource.set_config`, `ConfigEntry`, `AlterConfigOpType`: https://docs.confluent.io/platform/current/clients/confluent-kafka-python/html/index.html
- Apache Kafka Admin API — `incrementalAlterConfigs` y deprecación de `alterConfigs`: https://kafka.apache.org/38/javadoc/org/apache/kafka/clients/admin/Admin.html
- Apache Kafka protocol — `IncrementalAlterConfigs` API key 44: https://kafka.apache.org/40/design/protocol/

No volver al `alter_configs()` legacy upstream salvo evidencia material y nueva certificación completa.

## Deployment certificado

Topología:

```text
Cursor / Daedalus
  -> Authorization: Bearer capability token
  -> mcps.lab.aranea.cl:3007/mcp
  -> kafka-mcp-auth-dev-admin (Nginx)
  -> kafka-mcp-dev-admin:8000/mcp
  -> Kafka DEV 192.168.31.44:19091-19096
```

Containers:

```text
kafka-mcp-dev-admin
kafka-mcp-auth-dev-admin
```

Invariantes:

- backend `kafka-mcp-dev-admin` sin host port;
- proxy Nginx es el único container que publica `3007`;
- red Docker privada `mcp-kafka`;
- bearer cliente→MCP independiente de Kafka y montado read-only al proxy;
- `restart=unless-stopped`;
- source, dependencias críticas e imagen pinneados;
- valores de secrets nunca se guardan en Agents-OS, prompts, logs ni Cursor JSON.

## Tool surface certificada

`tools/list` server-side y desde cliente autenticado devolvió exactamente 19 tools:

```text
alter_configs
consume_messages
create_partitions
create_topic
delete_topic
describe_brokers
describe_cluster
describe_cluster_health
describe_configs
describe_consumer_group
describe_topic
get_broker_metrics
get_consumer_group_offsets
get_topic_metrics
list_consumer_groups
list_topics
produce_message
reset_consumer_group_offset
rewind_consumer_group_offset_by_timestamp
```

No existe tool de `delete_consumer_group` en este baseline.

## Certificación material 2026-09-13

Read-only E2E desde Cursor:

```text
cluster_id:    Eiuq4GsaTXOUPif-rLU-6Q
controller_id: 6
brokers:       6
topics:        117
```

Boundary de auth:

```text
GET sin bearer a :3007/mcp -> HTTP 401
request con bearer válido -> atraviesa Nginx; un GET no-MCP puede responder 406
MCP authenticated tools/list -> 19 tools
MCP authenticated describe_cluster -> PASS
```

Golden admin smoke ejecutado exclusivamente sobre recursos temporales:

```text
topic: mcp-cert-20260913-150530
group: mcp-cert-group-20260913-150530
```

Gates PASS:

1. `create_topic`: 1 partition, RF=3.
2. `describe_topic`: existencia y 1 partition.
3. `describe_configs`: baseline leído.
4. `alter_configs`: sólo `retention.ms` → `3600000`.
5. `describe_configs`: valor DYNAMIC y configs ajenas intactas.
6. `create_partitions`: 1 → 2.
7. `produce_message` + `consume_messages`: marker round-trip.
8. `describe_consumer_group` + `get_consumer_group_offsets`: group temporal visible.
9. `reset_consumer_group_offset` → latest: lag 0.
10. `delete_topic`: topic temporal eliminado.

Ningún topic preexistente fue mutado.

## Cliente Daedalus / Cursor

Secret cliente:

```text
~/.config/mcp/secrets/kafka-mcp-dev-admin.bearer
mode: 0600
env:  ARANEA_KAFKA_MCP_DEV_ADMIN_BEARER
```

Carga persistente KDE:

```text
~/.config/plasma-workspace/env/aranea-mcp.sh
  -> source ~/.config/mcp/aranea-env.sh
  -> ARANEA_KAFKA_MCP_DEV_ADMIN_BEARER
```

Cursor usa:

```text
name: aranea-kafka-dev-admin
url:  http://mcps.lab.aranea.cl:3007/mcp
Authorization: Bearer ${env:ARANEA_KAFKA_MCP_DEV_ADMIN_BEARER}
```

El bearer literal nunca vive en `~/.cursor/mcp.json`.

Secret proxy en `mcps`:

```text
/opt/mcp/kafka/runtime/proxy-secrets/daedalus-dev-admin.bearer
```

Documentar el path, nunca el contenido.

## Limitaciones conocidas del baseline

### `create_topic`

Aunque la firma upstream declara `config: Optional[Dict[str, str]] = None`, el golden smoke vía MCP requirió enviar `config={}` explícitamente; `null`/omitido falló en la superficie MCP certificada. Para operación agent-first, enviar siempre un dict, vacío cuando no haya overrides.

### `consume_messages`

No acepta `group_id`. El código pinneado crea internamente un consumer group efímero `mcp-inspector-<uuid>` y asigna partitions directamente. No usar `consume_messages` para demostrar consumo de una aplicación/group específico.

### Consumer groups

El baseline puede listar/describir groups, consultar offsets, resetearlos y rebobinarlos por timestamp. No registra una tool para eliminar consumer groups. Un group temporal creado mediante operaciones de offsets puede quedar `EMPTY` aun después de borrar el topic asociado.

## Disciplina de operación DEV

`aranea-kafka-dev-admin` tiene autoridad real de administración. DEV no significa “mutar libremente sin scope”.

Antes de una mutación:

1. identificar cluster, topic/group/config exactos;
2. confirmar que el target es DEV;
3. fijar blast radius y post-condición;
4. para probes, usar nombres temporales `mcp-cert-*` y limpiar al terminar;
5. para offsets, preferir `dry_run=true` antes de aplicar cuando la tool lo permita;
6. no usar `force=true` sobre groups activos salvo autorización explícita y evidencia de necesidad;
7. después de `alter_configs`, releer las keys relevantes y confirmar que configs no objetivo permanecen intactas;
8. verificar toda mutación en el mismo ambiente.

No usar esta capability contra Kafka PROD ni como sustituto de futuras capabilities PROD.

## Troubleshooting

- capability ausente en Cursor → revisar env/restart/handshake según [[aranea-mcp-capability-plane]];
- `401` → bearer cliente→Nginx; no tocar Kafka;
- `406` con `curl GET /mcp` autenticado → puede ser petición HTTP no válida para MCP y no prueba caída; ejecutar handshake MCP real;
- backend Up pero tools ausentes → validar FastMCP/transport y `tools/list` antes de Kafka;
- `describe_cluster` falla con handshake PASS → revisar reachability `mcps` → `192.168.31.44:19091-19096` y advertised listeners;
- `alter_configs` cambia configs ajenas → capability fuera de contrato; detener mutaciones y restaurar imagen patchada certificada;
- consumer group `STABLE` o con members → no forzar reset automáticamente;
- necesidad de borrar consumer group → la tool no existe; usar flujo humano/administrativo separado si realmente es necesario, no inventar bypass agent-first.

## Hard Rules

- Aranea-only; nunca usar contra MELI/corporativo.
- DEV primero; Kafka PROD queda fuera de esta capability.
- No acceder a los brokers directamente desde agentes cuando `aranea-kafka-dev-admin` cubre la operación.
- No publicar el backend MCP al host.
- No usar source/main flotante ni dependencias FastMCP flotantes.
- No revertir el patch incremental por conveniencia.
- No tocar topics/groups existentes para probes de salud o certificación; usar recursos temporales.
- No imprimir ni registrar bearer tokens.
- No asumir SSH hacia el LXC `docker-kafka`.
- No instalar Kafka CLI ad-hoc en `mcps`; `mcps` sigue siendo appliance MCP Docker/Portainer.

## Validación

```text
Environment:          DEV
Capability:           aranea-kafka-dev-admin
Endpoint:             http://mcps.lab.aranea.cl:3007/mcp
Proxy unauthenticated: 401
MCP initialize/tools: PASS / 19 tools
Backend host port:    none
Cluster id:           Eiuq4GsaTXOUPif-rLU-6Q
Brokers:              6
Admin smoke:          create/config/partitions/produce/consume/group-offset/delete PASS
Config mutation:      incremental only
Secrets exposed:      no
PROD authority:       none / deferred
```
