---
type: doc
schema_version: 1
status: active
area: "[[Aranea]]"
related: []
aliases: []
tags:
  - kind/doc
created: 2026-08-10
updated: 2026-08-10
---

# Data streaming — Kafka, Flink, EMQX

## Propósito

Documentación canónica legacy de [[Aranea]]; se conserva el contenido histórico y su estado requiere verificación antes de uso operativo.

## Contenido


> **Capturado**: 2026-06-28

## Kafka cluster (3 brokers)

| VMID | Nombre | Tipo | Nodo | Status | CPU | RAM | Disco |
|---|---|---|---|---|---|---|---|
| 136 | kafka-hera | qemu | hera | **running** | 4 | 8 GB | 30 GB |
| 138 | kafka-kronos | qemu | kronos | **running** | 4 | 8 GB | 30 GB |
| 139 | kafka-zeus | qemu | zeus | **running** | 2 | 8 GB | 30 GB |

**Quorum**: 3/3 brokers activos ✅

### Topología y distribución

```
Kafka cluster
├── kafka-hera   (qemu/136, hera)
├── kafka-kronos (qemu/138, kronos)
└── kafka-zeus   (qemu/139, zeus)
```

> Los brokers Kafka están distribuidos en 3 nodos diferentes del Ceph cluster, asegurando resiliencia si un nodo cae.

### Tráfico

| Broker | NetIn | NetOut |
|---|---|---|
| kafka-hera | 296 GB | 336 GB |
| kafka-zeus | 415 GB | 358 GB |
| kafka-kronos | 125 GB | 151 GB |

## docker-kafka (lxc/128)

| Item | Valor |
|---|---|
| **Propósito** | Cliente / dev environment para Kafka |
| **VMID** | 128 |
| **Tipo** | lxc container |
| **Nodo** | hera |
| **vCPUs** | 4 |
| **RAM** | 17 GB |
| **Disco** | 50 GB |
| **Tags** | `base`, `docker` |
| **Estado** | ✅ Running |

> No es parte del cluster de brokers — es instancia dev/cliente.

## docker-flink (lxc/126)

| Item | Valor |
|---|---|
| **Propósito** | Apache Flink — stream processing consumer del Kafka cluster |
| **VMID** | 126 |
| **Tipo** | lxc container |
| **Nodo** | hades |
| **vCPUs** | 20 |
| **RAM** | **32 GB** |
| **Disco** | 50 GB |
| **Tags** | `community-script`, `docker` |
| **NetIn** | 233 GB |
| **NetOut** | 320 GB |
| **Estado** | ✅ Running |

### Patrón

```
[kafka-hera, kafka-kronos, kafka-zeus] (brokers)
                  ↓ consume
         [docker-flink en hades] (32 GB RAM)
                  ↓ output
        [postgresql o mongodb en hades]
```

> [!warning] SPOF de stream processing
> Flink corre **solo en hades**. Si hades cae → stream processing cae.

## EMQX (lxc/103)

| Item | Valor |
|---|---|
| **Propósito** | Broker MQTT (homelab) |
| **VMID** | 103 |
| **Tipo** | lxc container |
| **Nodo** | hades |
| **vCPUs** | 2 |
| **RAM** | 1 GB |
| **Disco** | 4 GB |
| **Tags** | `homelab` |
| **Estado** | ✅ Running |

> MQTT broker — probablemente usado por dispositivos IoT (homeassistant, frigate events).

## Resumen de dependencias

```
Producers
├── homeassistant (qemu/105, hades)  ← IoT
├── frigate (lxc/137, hades)          ← NVR events
└── (otros productores desconocidos)
                ↓
        [EMQX (lxc/103)]            ← MQTT broker
                ↓
        [kafka-* (3 brokers)]       ← log aggregation
                ↓ consume
        [docker-flink (lxc/126)]    ← stream processing
                ↓ output
        [postgresql/mongodb]        ← sink
```

## Alertas

| # | Severidad | Alerta |
|---|---|---|
| 1 | 🟡 | Flink (32 GB RAM) concentrado en hades |
| 2 | 🟡 | EMQX sin redundancia (single instance) |
| 3 | 🟡 | Sin esquema de topics documentado |

---

**Source files**: `/home/hermes/aranea/topology/services.md`, `/home/hermes/aranea/topology/discovery/{hera,kronos,zeus,hades}_20260628_211812.txt`

**Captured**: 2026-06-28 21:18 UTC. Doc generado 2026-06-30.
