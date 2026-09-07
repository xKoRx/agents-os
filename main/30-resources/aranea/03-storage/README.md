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

# 03 — Storage (inventario)

## Propósito

Documentación canónica legacy de [[Aranea]]; se conserva el contenido histórico y su estado requiere verificación antes de uso operativo.

## Contenido


> **Capturado**: 2026-06-28 vía `agent-read all`
> **Generado**: 2026-06-30

> [!info] Sobre este folder
> Este folder contiene el **inventario** del storage. La **auditoría profesional profunda** (`AUDIT.md`) y el **diseño del sistema de backup** (`BACKUP-SYSTEM.md`) se ejecutan en la **Task 2** (ticket `2026-06-30-011`).

## 📑 Contenido

| Doc | Descripción |
|---|---|
| [[ceph-pool1]] | Pool Ceph RBD (75% usado) |
| [[truenas-pool0]] | Pool TrueNAS principal (4 mirrors + special) |
| [[truenas-pool2]] | Pool TrueNAS bulk (sin redundancia ⚠️) |
| [[nfs-shares]] | Exports NFS |
| [[smb-shares]] | Shares SMB |
| [[iscsi-target]] | Target iSCSI |
| [[datasets]] | Per-dataset breakdown |
| [[inventory]] | Storage landscape raw/used/free |

## 📊 Capacidad summary

| Componente | Tamaño raw | Usado | Libre | % Uso | Tipo |
|---|---|---|---|---|---|
| **Ceph pool1 (RBD)** | 3.6 TB | 2.1 TB | 1.6 TB | **57.19%** (raw) / **75.22%** (pool) | Distribuido |
| **Truenas pool0** | 4.4 TB | 2.5 TB | 1.9 TB | **57%** | Mirror |
| **Truenas pool2** | 7.99 TB | 3.5 TB | 4.5 TB | **44%** | Single ⚠️ |
| **Truenas boot-pool** | 30 GB | 5 GB | 25 GB | 17% | SO |
| **Truenas special (mirror)** | 498 GB | 12 GB | 486 GB | 2% | Special vdev |
| **Total truenas** | ~12 TB | ~6 TB | ~6 TB | ~50% | |
| **LVM local en PVE** | ~5 TB (suma) | varía | varía | varía | local |
| **iSCSI LUNs (de truenas)** | 1.1 TB | raw | raw | — | block |
| **TOTAL cluster** | **~20 TB** | ~10 TB | ~10 TB | ~50% | |

> ⚠️ Los números **varían por nodo** (LVM local). Ver [[inventory]] para el detalle.

## 🗺️ Mapa de storages Proxmox declarados

| Storage | Tipo | Tamaño | Función | Nodos donde está disponible |
|---|---|---|---|---|
| `pool1` | rbd (Ceph) | 1 TB | Datastore principal cluster | Todos (shared) |
| `nfs-storage` | nfs (truenas) | 1.6 TB | Backups, ISOs, templates | Todos (shared) |
| `iscsi-aranea` | iscsi (truenas) | n/a | Shared block | Todos (shared) |
| `local` | dir | 41-177 GB | iso, backup, vztmpl local | Todos (per-node) |
| `local-lvm` | lvmthin | 58-429 GB | rootdir, images per-node | Todos (per-node) |
| `local-sqx-zeus` | lvm | 931 GB | Datasets SQX en zeus (vm 108) — **SAGRADO** | zeus only |
| `local-sqx-hera` | lvm | 931 GB | Datasets SQX en hera (vm 123 stopped) — **SAGRADO** | hera only |
| `local-sqx-kronos` | lvm | 931 GB | Datasets SQX en kronos (vm 111 stopped) — **SAGRADO** | kronos only |
| `local-kronos` | lvm | 931 GB | Otros datasets en kronos | kronos only |
| `pool-kronos` | lvm | 954 GB | Datasets adicionales en kronos (vm 112 stopped, vm 138) | kronos only |

> Ver `pve_storage` en cada `discovery/{nodo}_*.txt` para JSON crudo.

## 🔗 Mapa lógico

```
                         ┌────────────────────┐
                         │    Ceph pool1      │
                         │   4 OSDs NVMe      │
                         │    (RBD)           │
                         └─────────┬──────────┘
                                   │ shared
                ┌──────────────────┼──────────────────┐
                │                  │                  │
            ┌───┴───┐         ┌────┴────┐        ┌────┴────┐
            │ athena│         │ hera    │        │ kronos  │
            │       │         │  osd.0  │        │ osd.1+3 │
            └───────┘         └─────────┘        └─────────┘
            
                         ┌────────────────────┐
                         │   truenas VM       │
                         │   (hades qemu/145) │
                         └─────────┬──────────┘
                                   │
            ┌──────────────────────┼──────────────────────┐
            │                      │                      │
        ┌───┴────┐          ┌──────┴─────┐         ┌──────┴─────┐
        │ pool0  │          │  pool2     │         │ boot-pool  │
        │ 4 mirr │          │ single ⚠️  │         │            │
        │ 4.4 TB │          │  7.2 TB    │         │  30 GB     │
        └────────┘          └────────────┘         └────────────┘
                ↓                    ↓
        NFS (proxmox_storage)   backups (single)
        SMB (aranea_storage)    
        SMB (trading_systems)   
        SMB (trading_documents) 
        iSCSI (iscsi-aranea)    
```

## Alertas críticas

| # | Severidad | Alerta |
|---|---|---|
| 1 | 🔴 | **TrueNAS VM en hades** = SPOF de todo el storage compartido |
| 2 | 🟠 | `pool2` (backups) **sin redundancia** |
| 3 | 🟠 | Scrub de pool2 obsoleto (11 meses) |
| 4 | 🟡 | Ceph OSD.0 (76%) y OSD.2 (76%) — uso alto con fragmentación |
| 5 | 🟡 | OSD.3 (kronos) — slow operations |

## Pendientes

- AUDIT.md — análisis profesional de cada storage (Task 2)
- BACKUP-SYSTEM.md — diseño 3-2-1, snapshots ZFS, off-host copy (Task 2)
- 04-backups/ — runbook operativo semanal (Task 2)

---

## Source files

- `/home/hermes/aranea/topology/discovery/{zeus,hera,kronos,athena,hades,truenas}_20260628_211812.txt`
- `/home/hermes/aranea/topology/nodes/truenas.md`
- `/home/hermes/aranea/topology/health.md`

## Captured

2026-06-28 21:18 UTC. Doc generado 2026-06-30.
