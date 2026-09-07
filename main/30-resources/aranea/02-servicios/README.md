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

# 02 — Servicios

## Propósito

Documentación canónica legacy de [[Aranea]]; se conserva el contenido histórico y su estado requiere verificación antes de uso operativo.

## Contenido


> **Capturado**: 2026-06-28 vía `agent-read all`
> **Generado**: 2026-06-30

## 📑 Catálogo por categoría

| Doc | Categoría | Servicios incluidos |
|---|---|---|
| [[red]] | Red | OPNsense, Pi-hole, Traefik, etcd |
| [[observabilidad]] | Observabilidad | Prometheus/Grafana (estado) |
| [[trading]] | Trading | MT4 (5 running + 1 stopped), MT5 |
| [[ml-ia]] | ML / IA / Workflow | sqx-ulab (3 VMs), echo, argus, mcps, temporal, ubuntu-dev |
| [[bases-de-datos]] | Bases de datos | PostgreSQL, MongoDB, obsidian-sync (CouchDB) |
| [[data-streaming]] | Streaming / Brokers | Kafka 3-broker, Flink, EMQX |
| [[backup-storage]] | Backup / Storage | TrueNAS (NFS/iSCSI/SMB), minio |
| [[automation]] | Automatización | homeassistant, runbooks |
| [[media-domotica]] | Media / Domótica | homeassistant, frigate (NVR) |
| [[dns-tls]] | DNS / TLS | Pi-hole, step-ca |
| [[misc-otros]] | Misceláneos | etcd-keeper, obsidian-sync, hasura, etc. |

## 📊 Resumen de carga por servicio (top por tráfico)

| Servicio | VMID | Nodo | NetIn | NetOut | Tipo |
|---|---|---|---|---|---|
| opnsense | 130 | athena | 1.72 TB | **6.20 TB** | network |
| docker-frigate.14 | 137 | hades | **10.5 TB** | 583 GB | NVR |
| truenas | 145 | hades | (loopback) | (loopback) | storage VM |
| postgresql | 152 | hades | 780 GB | 677 GB | DB |
| docker-hasura | 129 | hades | 486 GB | 325 GB | GraphQL |
| pi-hole | 149 | athena | 128 GB | 2.6 GB | DNS |
| echo | 140 | hades | 247 GB | 360 GB | IA |
| etcd-athena | 101 | athena | 228 GB | 99 GB | etcd |
| docker-flink | 126 | hades | 233 GB | 320 GB | streaming |
| obsidian-sync | 116 | hades | 2.9 GB | 1.5 GB | CouchDB |
| traefik | 115 | athena | 18 GB | 3.2 GB | proxy |

> [!note] Métricas acumuladas
> Los números NetIn/NetOut son **acumulados** desde la creación de cada VM (no por unidad de tiempo). Sirven para entender el patrón de tráfico, no el throughput actual.

## 🔄 Cross-references de dependencias

```
Truenas VM (qemu/145) ← corre en hades
   ├─ NFS proxmox_storage ← usado por todos los PVE nodes (mount /mnt/pve/nfs-storage)
   ├─ iSCSI iscsi-aranea ← usado por todos los PVE nodes (storages iSCSI)
   ├─ SMB aranea_storage ← compartido
   ├─ SMB trading_systems ← datos trading
   └─ SMB trading_documents ← guest-ok ⚠️

Ceph pool1 (RBD)
   ├─ osd.0 (hera) → 76% usado, fragmentación 0.83
   ├─ osd.1 (kronos) → 35% usado
   ├─ osd.2 (zeus) → 76% usado, fragmentación 0.81
   └─ osd.3 (kronos) → 40% usado, slow ops

Kafka cluster (3 brokers)
   ├─ kafka-hera (qemu/136, hera)
   ├─ kafka-kronos (qemu/138, kronos)
   └─ kafka-zeus (qemu/139, zeus)
   ↓ consumer
   docker-flink (lxc/126, hades) ← 32 GB RAM

etcd cluster (5 miembros)
   ├─ etcd-athena (lxc/101, athena)
   ├─ etcd-hera (lxc/155, hera)
   ├─ etcd-zeus (lxc/156, zeus)
   ├─ etcd-kronos (lxc/154, kronos)
   └─ etcd-hades (lxc/147, hades)
   ↑
   └─ etcd-keeper (lxc/148, hades) ← UI

Trading (5 instancias MT4)
   ├─ mt4-real (qemu/124, hades) ← CUENTA REAL
   ├─ mt4-test (qemu/125, hades)
   ├─ mt4-ftmo (qemu/133, hades)
   ├─ mt4-ttp (qemu/134, hades)
   └─ mt4-demo (qemu/144, hades)

Bases de datos
   ├─ postgresql (qemu/152, hades) ← 24 GB RAM
   └─ mongodb (qemu/153, hades) ← 24 GB RAM

Observabilidad
   ├─ docker-observability (lxc/127, hades) ← stack monitoreo (15 GB RAM)
   └─ docker-monitoreo (lxc/132, hera, stopped)
```

---

## Source files

- `/home/hermes/aranea/topology/services.md`
- `/home/hermes/aranea/topology/discovery/{athena,zeus,hera,kronos,hades,truenas}_20260628_211812.txt`
- `/home/hermes/aranea/tickets/*.md`

## Captured

**2026-06-28 21:18 UTC**. Doc generado 2026-06-30.

**2026-07-02**: además del catálogo por categoría, existen **notas individuales** para servicios tier 0 del proyecto [[10-projects/Aranea/SERVICIOS-DOCS-OWNER-PROJECT]]. Las notas individuales son **complemento**, no reemplazo del catálogo.

- [[opnsense]] — vm 130, athena
- [[pi-hole]] — vm 149, athena
- [[traefik]] — vm 115, athena
