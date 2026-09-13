---
type: doc
schema_version: 1
status: active
area: "[[Aranea]]"
related:
  - "[[aranea-kafka-mcp]]"
  - "[[AGENT-PLATFORM - MCP Access Plane]]"
aliases: []
tags:
  - kind/doc
  - tech/kafka
  - tech/streaming
created: 2026-08-10
updated: 2026-09-13
---

# Data streaming — Kafka, Flink, EMQX

## Propósito

Mapa de alto nivel de los servicios de streaming de [[Aranea]]. El baseline Kafka DEV fue reverificado el 2026-09-13; los bloques marcados como snapshot histórico conservan evidencia de 2026-06-28 y no deben usarse como autoridad operativa sin revalidación.

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

## docker-flink (LXC 126) — snapshot histórico 2026-06-28

| Item | Valor |
|---|---|
| **Propósito** | Apache Flink — stream processing consumer Kafka |
| **VMID** | 126 |
| **Tipo** | lxc container |
| **Nodo** | hades |
| **vCPUs** | 20 |
| **RAM** | **32 GB** |
| **Disco** | 50 GB |
| **Tags** | `community-script`, `docker` |
| **NetIn** | 233 GB |
| **NetOut** | 320 GB |
| **Estado snapshot** | Running |

Patrón histórico:

```text
Kafka
  ↓ consume
[docker-flink en hades]
  ↓ output
[postgresql o mongodb]
```

> [!warning] Snapshot legacy
> La concentración de Flink en hades y sus dependencias deben revalidarse antes de decisiones operativas actuales.

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
| 2 | 🟡 | Flink/EMQX conservan baseline legacy 2026-06-28 |
| 3 | 🟡 | No existe esquema canónico de topics documentado en este recurso |

## Autoridades relacionadas

- Operación Kafka DEV agent-first → [[aranea-kafka-mcp]].
- Routing de capabilities MCP → [[aranea-mcps-expert]].
- Arquitectura/deployment MCP → [[AGENT-PLATFORM - MCP Access Plane - Architecture]].
- Proyecto de rollout MCP → [[AGENT-PLATFORM - MCP Access Plane]].

---

**Fuentes legacy preservadas:** `/home/hermes/aranea/topology/services.md`, `/home/hermes/aranea/topology/discovery/{hera,kronos,zeus,hades}_20260628_211812.txt`.

**Snapshot legacy:** 2026-06-28 21:18 UTC. **Kafka DEV reverificado:** 2026-09-13.
