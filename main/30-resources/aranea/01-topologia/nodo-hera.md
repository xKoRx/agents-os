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

# nodo-hera — Compute + Ceph MON/OSD.0

## Propósito

Documentación canónica legacy de [[Aranea]]; se conserva el contenido histórico y su estado requiere verificación antes de uso operativo.

## Contenido


> **Estado**: ✅ OK (subutilizado: 72 cores, 125 GB RAM, solo 9 vCPU + 28 GB RAM asignados)
> **Capturado**: 2026-06-28 vía `agent-read all`
> **Fuente**: `/home/hermes/aranea/topology/discovery/hera_20260628_211812.txt`
> **Ping check 2026-06-30**: ✅ responde ICMP

## 🪪 Identidad

| Item | Valor |
|---|---|
| Hostname | `hera` |
| IP LAN | `192.168.31.110` |
| IP Ceph | `10.10.10.110` |
| Gateway | `192.168.31.1` |
| Rol | Compute + Ceph MON + OSD.0 |
| Hardware Vendor | MACHINIST (E5-D8-MAX) |
| Firmware | 5.11 |

## ⚙️ Hardware

| Item | Valor |
|---|---|
| CPU | **2× Intel Xeon E5-2699 v3** (18 cores × 2 = 36 cores físicos × 2 SMT = **72 threads**) |
| Vendor ID | GenuineIntel |
| RAM | **125 GiB** total, swap 8 GB |
| Uso de RAM | 29 GiB usados / 90 GiB free / **96 GiB available** ← muy libre |
| Hypervisor | PVE nativo |

> [!note] hera está muy subutilizada
> De 72 threads y 125 GB RAM, solo 9 vCPU + 28 GB RAM están asignados a VMs running. Es candidata natural para absorber carga si hades se congestiona.

## 🐧 OS + Kernel

| Item | Valor |
|---|---|
| OS | Debian GNU/Linux 12 (bookworm) |
| Kernel | `6.8.12-18-pve` |
| PVE Manager | `8.4.16/368e3c45c15b895c` (versión levemente distinta) |
| Uptime | 41 días |

## 🌐 Red

| Interfaz | Estado | Notas |
|---|---|---|
| `lo` | UNKNOWN | 127.0.0.1/8 |
| `enp5s0` | DOWN | (sin conexión) |
| `enp6s0` | UP | sin IP (en bond0) |
| `enp129s0f0` | DOWN | (sin conexión) |
| `enp129s0f1` | DOWN | (sin conexión) |
| `ens14` | UP | sin IP (en bond0) |
| `bond0` | UP | master de vmbr0 |
| `vmbr0` | UP | `192.168.31.110/24` |
| `ceph` | UP | `10.10.10.110/24` |

### Rutas

```
default via 192.168.31.1 dev vmbr0
10.10.10.0/24 dev ceph  src 10.10.10.110
192.168.31.0/24 dev vmbr0  src 192.168.31.110
```

### Puertos Ceph

```
tcp  192.168.31.110:3300   ceph-mon
tcp  192.168.31.110:6789   ceph-mon
tcp  192.168.31.110:6800-6803  ceph-osd
tcp  10.10.10.110:6800-6803    ceph-osd (cluster network)
```

## 💾 Almacenamiento local

### Discos

| Disco | Tamaño | FSTYPE | Modelo | Notas |
|---|---|---|---|---|
| `sda` | 931.5 GB | LVM2 | WD Green SATA SSD 2.5 1TB | **LVM vg `local-sqx-hera`** (datasets SQX — **SAGRADO**, vm 123 stopped) |
| `sdb` (iSCSI) | 50 GB | misc | iSCSI Disk `e9fef...` | (LUN remoto via iSCSI) |
| `sdc` (iSCSI) | 200 GB | raw | iSCSI Disk `e9f0bd...` | |
| `sdd` (iSCSI) | 200 GB | raw | iSCSI Disk `613f83...` | |
| `sde` (iSCSI) | 32 GB | xfs | iSCSI Disk `55adbd...` | |
| `sdf` (iSCSI) | 32 GB | xfs | iSCSI Disk `c8868b...` | |
| `sdg` (iSCSI) | 100 GB | ext4 | iSCSI Disk `cb144...` | |
| `nvme0n1` | 465.8 GB | LVM2 | GIGABYTE G325E500G | Boot + system |
| `nvme1n1` | 931.5 GB | LVM2 | CT1000P3SSD8 | **Ceph OSD.0** |

### Ceph OSD.0

```
nvme1n1  931.5 GB
└─ ceph--f3f6ce9b--...--osd--block--da6495a6--...  931.5 GB ceph_bluestore
```

### `df`

```
/dev/mapper/pve-root            ext4       94G   10G   80G  12%  /
tmpfs                           tmpfs      63G   28K   63G   1%  /var/lib/ceph/osd/ceph-0
192.168.31.91:/mnt/pool0/proxmox_storage  nfs4   1.5T  372G  1.2T  25%  /mnt/pve/nfs-storage
```

## 📦 Storages Proxmox disponibles en hera

| Storage | Tipo | Tamaño | Uso |
|---|---|---|---|
| `local` | dir | 100 GB | iso,vztmpl,backup (11% usado) |
| `local-lvm` | lvmthin | 363 GB | rootdir,images (29% usado) |
| `local-sqx-hera` | lvm | 931 GB | Datasets SQX (vm 123 — stopped) |
| `nfs-storage` | nfs | 1.5 TB | 25% usado |
| `pool1` | rbd | 1 TB | 75% usado |
| `iscsi-aranea` | iscsi | — | truenas |

## 🖥️ VMs corriendo en hera

| VMID | Tipo | Nombre | Status | CPU | RAM | Disco |
|---|---|---|---|---|---|---|
| 107 | qemu | develop | **stopped** | 4 | 17 GB | 100 GB |
| 109 | qemu | win-serv-22 | **stopped** | 16 | 34 GB | 120 GB (template) |
| 110 | qemu | testing | **stopped** | 8 | 17 GB | 50 GB (trading) |
| 112 | qemu | kronos-sqx | **stopped** | 4 | 30 GB | 120 GB |
| 113 | qemu | sqx-ulab-hera-0 | **stopped** | 70 | **100 GB** | 50 GB ⚠️ VM detenida muy grande |
| 117 | qemu | ubuntu-server | **stopped** | 5 | 12 GB | 32 GB (template) |
| 120 | qemu | k8s-node-2 | **stopped** | 5 | 12 GB | 32 GB (template, k8s) |
| 121 | lxc | docker-mongodb-local | **stopped** | 6 | 20 GB | 10 GB |
| 122 | lxc | docker-postgres-local | **stopped** | 8 | 17 GB | 10 GB |
| 128 | lxc | docker-kafka | **running** | 4 | 17 GB | 50 GB |
| 132 | lxc | docker-monitoreo | **stopped** | 2 | 4 GB | 10 GB |
| 136 | qemu | kafka-hera | **running** | 4 | 8 GB | 30 GB (broker Kafka) |
| 155 | lxc | etcd-hera | running | 1 | 4 GB | 18 GB |

**Total hera**: 3 corriendo, 9 vCPU asignados, 28 GB RAM asignados. **10 VMs detenidas disponibles** (sumarían 130 vCPU + 263 GB RAM si se prendieran todas — sobrepasa RAM físico, evaluar con cuidado).

## 🛡️ Ceph

`hera` es Ceph MON + OSD.0:

| Servicio | Estado |
|---|---|
| ceph-mon | activo (quorum: hera, zeus, kronos) |
| ceph-mgr | NO (solo zeus activo + kronos standby) |
| ceph-osd.0 | up |

`ceph_health` local: **HEALTH_WARN** (igual que el resto del cluster — fragmentación en osd.0).

## 🔌 Servicios systemd

| Estado | Cantidad |
|---|---|
| Running | ceph-mon, ceph-osd, pve-cluster, pveproxy, sshd, etc. |
| Failed | **0** ✅ |

## 🚨 Alertas en este nodo

| Severidad | Alerta |
|---|---|
| 🟡 | OSD.0 (hera) con **76% uso** + fragmentación BlueStore **0.836025** (alto). Acción: `ceph tell osd.0 compact` |
| 🟡 | Múltiples slaves de bond0 y otros NICs DOWN. bond0 funciona con 2 slaves activos pero 5 interfaces reportan DOWN. |

---

## Source files

- `/home/hermes/aranea/topology/discovery/hera_20260628_211812.txt`
- `/home/hermes/aranea/topology/services.md`

## Captured

2026-06-28 21:18 UTC. Doc generado 2026-06-30.
