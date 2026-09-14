---
type: doc
schema_version: 1
status: active
area: "[[Aranea]]"
related:
  - "[[aranea-kafka-mcp]]"
  - "[[aranea-flink-mcp]]"
  - "[[AGENT-PLATFORM - MCP Access Plane]]"
aliases: []
tags:
  - kind/doc
  - tech/kafka
  - tech/flink
  - tech/streaming
created: 2026-08-10
updated: 2026-09-13
---

# Data streaming — Kafka, Flink, EMQX

## Propósito

Mapa de alto nivel de los servicios de streaming de [[Aranea]]. Kafka DEV y Flink/StateFun DEV fueron reverificados el 2026-09-13; los bloques marcados como snapshot histórico conservan evidencia previa y no deben usarse como autoridad operativa sin revalidación.

## Kafka — estado vigente

### DEV — `docker-kafka` (LXC 128)

La descripción histórica de este LXC como “cliente / dev environment” quedó **superseded**. El discovery 2026-09-13 confirmó que aloja el cluster Kafka DEV real.

| Item | Valor |
|---|---|
| **Host/LXC** | `docker-kafka.192.168.31.1` |
| **VMID** | 128 |
| **LAN IP** | `192.168.31.44` |
| **Runtime** | Docker Compose project `kafka` |
| **Kafka** | `confluentinc/cp-kafka:7.6.1` |
| **Brokers** | 6 (`kafka1` … `kafka6`) |
| **Metadata mode** | ZooKeeper clásico |
| **ZooKeeper** | `confluentinc/cp-zookeeper:7.6.1` |
| **Security path MCP** | `PLAINTEXT` |
| **Estado** | PASS / verificado 2026-09-13 |

Listeners externos certificados desde `mcps`:

```text
broker 1 -> 192.168.31.44:19091
broker 2 -> 192.168.31.44:19092
broker 3 -> 192.168.31.44:19093
broker 4 -> 192.168.31.44:19094
broker 5 -> 192.168.31.44:19095
broker 6 -> 192.168.31.44:19096
```

Bootstrap DEV:

```text
192.168.31.44:19091,192.168.31.44:19092,192.168.31.44:19093,192.168.31.44:19094,192.168.31.44:19095,192.168.31.44:19096
```

Cluster observado durante certificación MCP:

```text
cluster_id:    Eiuq4GsaTXOUPif-rLU-6Q
controller_id: 6
brokers:       6
topics:        117
```

Acceso agent-first certificado:

```text
capability: aranea-kafka-dev-admin
endpoint:   http://mcps.lab.aranea.cl:3007/mcp
runbook:    [[aranea-kafka-mcp]]
```

La capability DEV permite inspección y administración de topics/configs/partitions, produce/consume y consumer-group offsets. La disciplina operativa y limitaciones del MCP viven exclusivamente en [[aranea-kafka-mcp]].

El LXC no tiene SSH operativo para este flujo; no asumir SSH como mecanismo de administración. Cuando se requiere intervención humana directa, usar la consola/VNC disponible para el LXC.

### PROD — cluster distribuido de 3 brokers

El baseline de proyecto mantiene un cluster Kafka PROD separado de tres VMs distribuidas entre Hera, Kronos y Zeus. Este carril DEV **no revalidó ni modificó PROD**. El MCP PROD está diferido y deberá descubrir listeners/security/runtime reales antes de crear capabilities `aranea-kafka-prod-ro` / `aranea-kafka-prod-ops`.

Snapshot histórico 2026-06-28:

| VMID | Nombre | Tipo | Nodo | Status | CPU | RAM | Disco |
|---|---|---|---|---|---|---|---|
| 136 | kafka-hera | qemu | hera | **running** | 4 | 8 GB | 30 GB |
| 138 | kafka-kronos | qemu | kronos | **running** | 4 | 8 GB | 30 GB |
| 139 | kafka-zeus | qemu | zeus | **running** | 2 | 8 GB | 30 GB |

Topología histórica:

```text
Kafka PROD
├── kafka-hera   (qemu/136, hera)
├── kafka-kronos (qemu/138, kronos)
└── kafka-zeus   (qemu/139, zeus)
```

Tráfico capturado en el snapshot:

| Broker | NetIn | NetOut |
|---|---|---|
| kafka-hera | 296 GB | 336 GB |
| kafka-zeus | 415 GB | 358 GB |
| kafka-kronos | 125 GB | 151 GB |

No inferir listeners, seguridad, quorum mode ni autoridad PROD desde este snapshot; KAFKA2-PROD exige discovery propio.

## Flink / Stateful Functions — DEV vigente

El runtime Flink DEV actualmente certificado **no es el antiguo `docker-flink` del snapshot 2026-06-28**. El path operativo vigente está en `docker-echo-dev`.

| Item | Valor |
|---|---|
| **Host/LXC** | `docker-echo-dev` |
| **VMID** | 141 |
| **LAN IP** | `192.168.31.75` |
| **Runtime** | Docker / Portainer |
| **Compose project** | `flink` |
| **Containers** | `statefun-master`, `statefun-worker` |
| **Image** | `apache/flink-statefun:3.2.0-java11` |
| **Flink** | `1.14.3` commit `98997ea` |
| **StateFun** | `3.2.0` |
| **JobManager REST** | `http://192.168.31.75:8082` → container `:8081` |
| **JobManager RPC** | host `:6123` |
| **HA** | none |
| **TaskManagers** | 1 |
| **Slots** | 2 total / 0 free al certificar |
| **Estado** | PASS / verificado 2026-09-13 |

Job observado durante la certificación:

```text
name:        StatefulFunctions
job id:      974f0479256bc8ffe71fe962750e9c90
state:       RUNNING
vertices:    14/14 RUNNING
subtasks:    28/28 RUNNING
parallelism: 2
```

Configuración persistente relevante:

```text
/root/statefun/conf/flink-conf.yaml
/root/statefun/modules/
```

Persistencia runtime del stack Portainer:

```text
/var/lib/docker/volumes/portainer_data/_data/compose/1/statefun/checkpoints/
/var/lib/docker/volumes/portainer_data/_data/compose/1/statefun/savepoints/
```

Source-of-truth declarativo recuperado:

```text
Portainer stack id: 1
host path: /var/lib/docker/volumes/portainer_data/_data/compose/1/docker-compose.yml
Portainer-internal path: /data/compose/1/docker-compose.yml
```

No reconstruir un `compose.yaml` paralelo como autoridad. Para cambios de config bind-mounted que no alteran topología, editar el source persistente autorizado y reiniciar controladamente. Para cambios de topology/ports/env/volumes, operar sobre el stack canónico Portainer y verificar el redeploy.

Acceso agent-first certificado:

```text
control plane:
  capability: aranea-flink-dev-admin
  endpoint:   http://mcps.lab.aranea.cl:3008/mcp
  surface:    22 tools exactas, sin SQL

host/runtime:
  capability: aranea-ssh
  profile:    docker-echo-dev-operator
  authority:  root operator DEV

runbook: [[aranea-flink-mcp]]
```

`aranea-flink-dev-admin` cubre cluster/jobs/savepoints/rescale/JAR/metrics/config observable; filesystem, Docker, logs, exec y lifecycle pertenecen a `docker-echo-dev-operator`. PROD `aranea-flink-prod-ro` queda diferido y no reutiliza autoridad DEV.

### `docker-flink` (LXC 126) — snapshot histórico 2026-06-28

Este bloque se conserva sólo como evidencia histórica; **no es autoridad para Flink DEV vigente**.

| Item | Valor |
|---|---|
| **Propósito histórico** | Apache Flink — stream processing consumer Kafka |
| **VMID** | 126 |
| **Tipo** | lxc container |
| **Nodo** | hades |
| **vCPUs** | 20 |
| **RAM** | **32 GB** |
| **Disco** | 50 GB |
| **Tags** | `community-script`, `docker` |
| **NetIn snapshot** | 233 GB |
| **NetOut snapshot** | 320 GB |
| **Estado snapshot** | Running |

No usar este snapshot para routing, lifecycle ni selección de capability actual.

## EMQX (LXC 103) — snapshot histórico 2026-06-28

| Item | Valor |
|---|---|
| **Propósito** | Broker MQTT homelab |
| **VMID** | 103 |
| **Tipo** | lxc container |
| **Nodo** | hades |
| **vCPUs** | 2 |
| **RAM** | 1 GB |
| **Disco** | 4 GB |
| **Tags** | `homelab` |
| **Estado snapshot** | Running |

El vínculo EMQX → Kafka descrito en el snapshot legacy no se considera autoridad actual sin revalidación.

## Alertas / deuda documental

| # | Severidad | Alerta |
|---|---|---|
| 1 | 🟡 | Kafka PROD requiere discovery actualizado antes de desplegar MCP PROD |
| 2 | 🟡 | Flink PROD requiere discovery propio antes de `aranea-flink-prod-ro`; DEV ya está cerrado y certificado |
| 3 | 🟡 | EMQX conserva baseline legacy 2026-06-28 |
| 4 | 🟡 | No existe esquema canónico de topics documentado en este recurso |

## Autoridades relacionadas

- Operación Kafka DEV agent-first → [[aranea-kafka-mcp]].
- Operación Flink/StateFun DEV agent-first → [[aranea-flink-mcp]].
- Routing de capabilities MCP → [[aranea-mcps-expert]].
- Arquitectura/deployment MCP → [[AGENT-PLATFORM - MCP Access Plane - Architecture]].
- Proyecto de rollout MCP → [[AGENT-PLATFORM - MCP Access Plane]].

---

**Fuentes legacy preservadas:** `/home/hermes/aranea/topology/services.md`, `/home/hermes/aranea/topology/discovery/{hera,kronos,zeus,hades}_20260628_211812.txt`.

**Snapshot legacy:** 2026-06-28 21:18 UTC. **Kafka DEV y Flink/StateFun DEV reverificados:** 2026-09-13.
