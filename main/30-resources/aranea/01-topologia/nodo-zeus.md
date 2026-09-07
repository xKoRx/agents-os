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

# nodo-zeus — Compute + Ceph MON/MGR/OSD.2

## Propósito

Documentación canónica legacy de [[Aranea]]; se conserva el contenido histórico y su estado requiere verificación antes de uso operativo.

## Contenido


> **Estado**: ✅ OK
> **Capturado**: 2026-06-28 vía `agent-read all`
> **Fuente**: `/home/hermes/aranea/topology/discovery/zeus_20260628_211812.txt`
> **Ping check 2026-06-30**: ✅ responde ICMP

## 🪪 Identidad

| Item | Valor |
|---|---|
| Hostname | `zeus` |
| IP LAN | `192.168.31.100` |
| IP Ceph | `10.10.10.100` |
| Gateway | `192.168.31.1` |
| Rol | Compute (1 VM grande: sqx-ulab) + Ceph MON + **MGR activo** + OSD.2 |
| Hardware Vendor | Micro-Star International Co., Ltd. (MS-7C37) |
| Firmware | H.P0 |

## ⚙️ Hardware

| Item | Valor |
|---|---|
| CPU | AMD Ryzen 9 5950X (16 cores × 2 = 32 threads) |
| Vendor ID | AuthenticAMD |
| RAM | **94 GiB** total, swap 8 GB |
| Uso de RAM | 67 GiB usados / 18 GiB free / 27 GiB available |
| Hypervisor | PVE nativo |

## 🐧 OS + Kernel

| Item | Valor |
|---|---|
| OS | Debian GNU/Linux 12 (bookworm) |
| Kernel | `6.8.12-18-pve` |
| PVE Manager | `8.4.19/a68fb383814bb1e6` |
| Uptime (al 2026-06-28) | 41 días |

## 🌐 Red

| Interfaz | Estado | Notas |
|---|---|---|
| `lo` | UNKNOWN | 127.0.0.1/8 |
| `enp39s0` | UP | sin IP (miembro de vmbr0 vía bridge directo) |
| `enp45s0` | UP | sin IP (miembro de ceph) |
| `vmbr0` | UP | `192.168.31.100/24`, IPv6 link-local |
| `ceph` | UP | `10.10.10.100/24`, IPv6 link-local ← Ceph backplane |

### Rutas

```
default via 192.168.31.1 dev vmbr0
10.10.10.0/24 dev ceph  src 10.10.10.100
192.168.31.0/24 dev vmbr0  src 192.168.31.100
```

### Puertos Ceph escuchando

```
tcp  192.168.31.100:3300   ceph-mon
tcp  192.168.31.100:6789   ceph-mon (msgr2)
tcp  192.168.31.100:6800-6803  ceph-osd
tcp  192.168.31.100:6804-6805  ceph-mgr
tcp  10.10.10.100:6800-6803   ceph-osd (cluster network)
```

## 💾 Almacenamiento local

### Discos

| Disco | Tamaño | FSTYPE | Modelo | Notas |
|---|---|---|---|---|
| `sda` | 931.5 GB | LVM2 | WD Green SATA SSD 2.5 1TB | **LVM vg `local-sqx-zeus`** (datasets SQX — **SAGRADO**) |
| `sdb` (iSCSI) | 50 GB | misc | iSCSI Disk `e9fef...` | (LUN remoto via iSCSI) |
| `sdc` (iSCSI) | 200 GB | raw | iSCSI Disk `e9f0bd...` | |
| `sdd` (iSCSI) | 200 GB | raw | iSCSI Disk `613f83...` | |
| `sde` (iSCSI) | 32 GB | xfs | iSCSI Disk `55adbd...` | |
| `sdf` (iSCSI) | 32 GB | xfs | iSCSI Disk `c8868b...` | |
| `sdg` (iSCSI) | 100 GB | ext4 | iSCSI Disk `cb144...` | |
| `nvme0n1` | 931.5 GB | LVM2 | CT1000P3SSD8 | **Ceph OSD.2** |
| `nvme1n1` | 465.8 GB | LVM2 | KINGSTON SNV2S500G | Boot + PVE data |

### LVM vg `local-sqx-zeus` (datasets SQX)

| LV | Tamaño |
|---|---|
| `local--sqx--zeus-vm--108--disk--0` | 50 GB (boot vm 108) |
| `local--sqx--zeus-vm--108--disk--1` | 600 GB (data vm 108) |

### LVM vg `pve` (boot + system)

| LV | Tamaño | Uso |
|---|---|---|
| `pve-swap` | 8 GB | [SWAP] |
| `pve-root` | 50 GB | `/` |
| `pve-data` (thin) | 399.9 GB | thinpool |

### Ceph OSD.2

```
nvme0n1  931.5 GB
└─ ceph--8b4b9c06--...--osd--block--5f883e09--...  931.5 GB
```

### `df`

```
/dev/mapper/pve-root            ext4       49G   15G   32G  31%  /
tmpfs                           tmpfs      48G   28K   48G   1%  /var/lib/ceph/osd/ceph-2
192.168.31.91:/mnt/pool0/proxmox_storage  nfs4   1.5T  372G  1.2T  25%  /mnt/pve/nfs-storage
```

## 📦 Storages Proxmox disponibles en zeus

| Storage | Tipo | Tamaño | Uso |
|---|---|---|---|
| `local` | dir | 53 GB | iso,vztmpl,backup |
| `local-lvm` | lvmthin | 429 GB | rootdir,images (7% usado) |
| `local-sqx-zeus` | lvm | 931 GB | Datasets SQX (vm 108) |
| `nfs-storage` | nfs | 1.5 TB | 25% usado |
| `pool1` | rbd | 1 TB (Ceph) | 75% usado |
| `iscsi-aranea` | iscsi | — | truenas |

## 🖥️ VMs corriendo en zeus

| VMID | Tipo | Nombre | Status | CPU | RAM | Disco | Notas |
|---|---|---|---|---|---|---|---|
| 100 | qemu | win11-gpu-red | **stopped** | 4 | 10 GB | 200 GB | |
| 102 | qemu | mt5-wsl-red | **stopped** | 2 | 6 GB | 50 GB | |
| 108 | qemu | sqx-ulab-zeus-0 | **running** | 28 | **75 GB** | 50 GB | ⚠️ VM más grande del cluster |
| 139 | qemu | kafka-zeus | **running** | 2 | 8 GB | 100 GB | Broker Kafka |
| 170 | qemu | sqx-ulab-zeus-1 | **stopped** | 8 | 23 GB | 20 GB | |
| 156 | lxc | etcd-zeus | running | 1 | 4 GB | 18 GB | Miembro etcd |

**Total zeus**: 3 corriendo (qemu 108/139 + lxc 156), 31 vCPU asignados, 87 GB RAM asignados. **5 VMs detenidas disponibles para encendido** (sumarían 116 vCPU + 57 GB RAM si se prendieran todas — pero cuidado con RAM).

## 🛡️ Ceph (estado local)

`zeus` es **Ceph MON + MGR activo + OSD.2**:

| Servicio | Estado | Notas |
|---|---|---|
| ceph-mon (hera, zeus, kronos quorum) | activo, age 2w | |
| ceph-mgr | **activo (primary)** | standbys: kronos |
| ceph-osd.2 | up | 932 GiB raw, 710 GiB usado (76% — HEAVY) |

### Output local de `ceph_df`

```
POOL   ID  PGS   STORED  OBJECTS     USED  %USED  MAX AVAIL
.mgr    1    1   13 MiB        5   40 MiB      0    233 GiB
pool1   2  128  708 GiB  193.13k  2.1 TiB  75.22    233 GiB
```

## 🔌 Servicios systemd

| Estado | Cantidad |
|---|---|
| Running | ceph-mon, ceph-mgr, ceph-osd, pve-cluster, pveproxy, sshd, etc. |
| Failed | **0** ✅ |

## 🚨 Alertas en este nodo

| Severidad | Alerta |
|---|---|
| 🟡 | OSD.2 (zeus) con **76% uso** + fragmentación BlueStore **0.817956** (alto). Acción: `ceph tell osd.2 compact` |

---

## Source files

- `/home/hermes/aranea/topology/discovery/zeus_20260628_211812.txt`
- `/home/hermes/aranea/topology/services.md`

## Captured

2026-06-28 21:18 UTC. Doc generado 2026-06-30.
