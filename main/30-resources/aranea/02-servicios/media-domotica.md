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

# Media & Domótica

## Propósito

Documentación canónica legacy de [[Aranea]]; se conserva el contenido histórico y su estado requiere verificación antes de uso operativo.

## Contenido


> **Capturado**: 2026-06-28

## homeassistant (qemu/105)

Ver [[automation]] § homeassistant para detalle.

- VM corriendo en **hades** (4 vCPU, 8 GB RAM)
- Hub central de IoT del homelab

## docker-frigate.14 (lxc/137)

| Item | Valor |
|---|---|
| **Propósito** | NVR (Network Video Recorder) + detección de movimiento + object recognition |
| **VMID** | 137 |
| **Tipo** | lxc container |
| **Nodo** | hades |
| **vCPUs** | 5 |
| **RAM** | 12 GB |
| **Disco** | 50 GB |
| **Tags** | `docker` |
| **NetIn** | **10.5 TB** ← tráfico NVR altísimo |
| **NetOut** | 583 GB |
| **Estado** | ✅ Running |

### Almacenamiento de video

- **NFS**: `192.168.31.91:/mnt/pool0/apps/frigate/storage/media` (videos NVR)
- **NFS**: `192.168.31.91:/mnt/pool0/apps/frigate/config` (configuración)

### Eventos

Frigate publica eventos de detección vía MQTT → consumidos por:
- homeassistant (automatizaciones)
- EMQX (broker MQTT lxc/103)
- posiblemente Kafka + Flink para analytics

## Resumen

| Servicio | VMID | Nodo | RAM | Función |
|---|---|---|---|---|
| homeassistant | 105 | hades | 8 GB | Smart home hub |
| docker-frigate.14 | 137 | hades | 12 GB | NVR + detección |

## Alertas

| # | Severidad | Alerta |
|---|---|---|
| 1 | 🟡 | Todo en hades — si hades cae, casa "se queda ciega" |
| 2 | 🟡 | 10.5 TB de NetIn acumulado sugiere mucho video de cámaras pasando por la red |
| 3 | 🟡 | Sin redundancia — si hades cae, homeassistant se reinicia sin estado |

---

**Source files**: `/home/hermes/aranea/topology/services.md`, `/home/hermes/aranea/topology/discovery/hades_20260628_211812.txt`

**Captured**: 2026-06-28 21:18 UTC. Doc generado 2026-06-30.
