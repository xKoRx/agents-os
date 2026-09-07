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

# nodo-kronos — Storage powerhouse + Ceph MON/MGR/OSD.1+3

## Propósito

Documentación canónica legacy de [[Aranea]]; se conserva el contenido histórico y su estado requiere verificación antes de uso operativo.

## Contenido


> **Estado**: ✅ OK (el más potente en RAM, gran capacidad Ceph local)
> **Capturado**: 2026-06-28 vía `agent-read all`
> **Fuente**: `/home/hermes/aranea/topology/discovery/kronos_20260628_211812.txt`
> **Ping check 2026-06-30**: ✅ responde ICMP

## 🪪 Identidad

| Item | Valor |
|---|---|
| Hostname | `kronos` |
| IP LAN | `192.168.31.120` |
| IP Ceph | `10.10.10.120` |
| Gateway | `192.168.31.1` |
| Rol | Storage powerhouse + Ceph MON + MGR **standby** + 2× OSDs |
| Hardware Vendor | HUANANZHI (X99-F8D PLUS) |
| Firmware | 5.11 |

## ⚙️ Hardware

| Item | Valor |
|---|---|
| CPU | **2× Intel Xeon E5-2698 v4** (20 cores × 2 = 40 cores físicos × 2 SMT = **80 threads**) |
| Vendor ID | GenuineIntel |
| RAM | **251 GiB** total, swap 8 GB |
| Uso de RAM | 29 GiB usados / 207 GiB free / **222 GiB available** ← casi todo libre |
| Hypervisor | PVE nativo |

> [!note] kronos es la "bestia dormida"
> De 80 threads y 251 GB RAM, solo 11 vCPU + 24 GB RAM están asignados a VMs running. **222 GB RAM disponibles**. Es la candidata #1 para absorber VMs detenidas (especialmente `sqx-ulab-kron-0`: 76 vCPU / 137 GB RAM que está apagada).

## 🐧 OS + Kernel

| Item | Valor |
|---|---|
| OS | Debian GNU/Linux 12 (bookworm) |
| Kernel | `6.8.12-18-pve` |
| PVE Manager | `8.4.16/368e3c45c15b895c` |
| Uptime (al 2026-06-28) | 16 días (más bajo que los demás — reboot reciente) |

## 🌐 Red

| Interfaz | Estado | Notas |
|---|---|---|
| `lo` | UNKNOWN | 127.0.0.1/8 |
| `enp10s0` | UP | en bond0 |
| `enp11s0` | UP | en bond0 |
| `ens6` | UP | en `ceph` (MTU 9000) |
| `bond0` | UP | master de vmbr0 |
| `vmbr0` | UP | `192.168.31.120/24` |
| `ceph` | UP | `10.10.10.120/24` (MTU 9000) |

### Rutas

```
default via 192.168.31.1 dev vmbr0
10.10.10.0/24 dev ceph  src 10.10.10.120
192.168.31.0/24 dev vmbr0  src 192.168.31.120
```

### Puertos Ceph

```
tcp  192.168.31.120:3300   ceph-mon
tcp  192.168.31.120:6789   ceph-mon
tcp  192.168.31.120:6800-6803  ceph-osd (osd.1)
tcp  192.168.31.120:6804-6807  ceph-osd (osd.3)
tcp  10.10.10.120:6800-6803    ceph-osd.1 (cluster net)
tcp  10.10.10.120:6804-6807    ceph-osd.3 (cluster net)
```

> [!note] **kronos corre 2 OSDs (osd.1 y osd.3)** — es el nodo con más capacidad Ceph local.

## 💾 Almacenamiento local

### Discos

| Disco | Tamaño | FSTYPE | Modelo | Notas |
|---|---|---|---|---|
| `sda` | 931.5 GB | LVM2 | WD Green SATA SSD 2.5 1TB | **LVM vg `local-sqx-kronos`** (datasets SQX — **SAGRADO**, vm 111 stopped) |
| `sdb` | 931.5 GB | LVM2 | Samsung SSD 870 QVO 1TB | **LVM vg `local-kronos`** (varios VMs) |
| `sdc` | 953.9 GB | LVM2 | P3-1TB | **LVM vg `pool-kronos`** (vm 112, 138) |
| `sdd` | 232.9 GB | LVM2 | Samsung SSD 870 EVO 250GB | Boot + system |
| `sde` (iSCSI) | 50 GB | misc | iSCSI Disk `e9fef...` | (LUN remoto via iSCSI) |
| `sdf` (iSCSI) | 200 GB | raw | iSCSI Disk `e9f0bd...` | |
| `sdg` (iSCSI) | 200 GB | raw | iSCSI Disk `613f83...` | |
| `sdh` (iSCSI) | 32 GB | xfs | iSCSI Disk `55adbd...` | |
| `sdi` (iSCSI) | 32 GB | xfs | iSCSI Disk `c8868b...` | |
| `sdj` (iSCSI) | 100 GB | ext4 | iSCSI Disk `cb144...` | |
| `nvme0n1` | 931.5 GB | LVM2 | KINGSTON SNV3S1000G | **Ceph OSD.1** |
| `nvme1n1` | 931.5 GB | LVM2 | KINGSTON SNV3S1000G | **Ceph OSD.3** |

> [!note] kronos tiene **3 LVM volume groups locales** (`local-sqx-kronos`, `local-kronos`, `pool-kronos`) además de los 2 OSDs Ceph. Es el nodo con mayor capacidad de storage local por lejos.

### LVM vg `local-sqx-kronos` (datasets SQX)

| LV | Tamaño |
|---|---|
| `local--sqx--kronos-vm--111--disk--0` | 50 GB (boot vm 111) |
| `local--sqx--kronos-vm--111--disk--1` | 600 GB (data vm 111) |

### LVM vg `local-kronos`

| LV | Tamaño |
|---|---|
| `local--kronos-vm--138--disk--0` | 100 GB xfs (kafka-kronos) |
| `local--kronos-vm--138--disk--1` | 100 GB xfs |
| `local--kronos-vm--104--disk--0` | 50 GB (ryma-linux, stopped) |
| `local--kronos-vm--111--disk--0` | 50 GB (vm 111) |

### LVM vg `pool-kronos`

| LV | Tamaño |
|---|---|
| `pool--kronos-vm--112--disk--0` | 120 GB (kronos-sqx, stopped) |
| `pool--kronos-vm--138--disk--0` | 100 GB xfs (kafka-kronos) |

### Ceph OSDs (kronos)

```
nvme0n1  931.5 GB → osd.1 (KINGSTON SNV3S1000G, 50026B7687197593)
nvme1n1  931.5 GB → osd.3 (KINGSTON SNV3S1000G, 50026B76871BD6FE)
```

### `df`

```
/dev/mapper/pve-root            ext4      166G   12G  147G   7%  /
tmpfs                           tmpfs     126G   28K  126G   1%  /var/lib/ceph/osd/ceph-1
tmpfs                           tmpfs     126G   28K  126G   1%  /var/lib/ceph/osd/ceph-3
192.168.31.91:/mnt/pool0/proxmox_storage  nfs4   1.5T  372G  1.2T  25%  /mnt/pve/nfs-storage
```

## 📦 Storages Proxmox disponibles en kronos

| Storage | Tipo | Tamaño | Uso |
|---|---|---|---|
| `local` | dir | 177 GB | iso,vztmpl,backup (7% usado) |
| `local-lvm` | lvmthin | 58 GB | rootdir,images (4% usado) |
| `local-sqx-kronos` | lvm | 1 TB | Datasets SQX (vm 111) |
| `local-kronos` | lvm | 931 GB | Datasets locales (vm 104, 138) |
| `pool-kronos` | lvm | 954 GB | Datasets adicionales (vm 112, 138) |
| `nfs-storage` | nfs | 1.5 TB | 25% usado |
| `pool1` | rbd | 1 TB | 75% usado |
| `iscsi-aranea` | iscsi | — | truenas |

## 🖥️ VMs corriendo en kronos

| VMID | Tipo | Nombre | Status | CPU | RAM | Disco |
|---|---|---|---|---|---|---|
| 104 | qemu | ryma-linux | **stopped** | 2 | 4 GB | 50 GB (exposed) |
| 106 | qemu | jobs | **running** | 2 | 4 GB | 32 GB |
| 111 | qemu | sqx-ulab-kron-0 | **stopped** | **76** | **137 GB** | 50 GB ⚠️ |
| 112 | qemu | kronos-sqx | **stopped** | 4 | 30 GB | 120 GB |
| 114 | qemu | mt4-test | **stopped** | 2 | 8 GB | 50 GB |
| 118 | qemu | agent | **running** | 4 | 8 GB | 32 GB ← Hermes agent VM |
| 138 | qemu | kafka-kronos | **running** | 4 | 8 GB | 30 GB (broker Kafka) |
| 154 | lxc | etcd-kronos | running | 1 | 4 GB | 18 GB |
| 162 | qemu | sqx-ulab-kron-1 | **stopped** | 12 | 30 GB | 20 GB |

**Total kronos**: 4 corriendo (qemu 106/118/138 + lxc 154), 11 vCPU asignados, 24 GB RAM asignados. **5 VMs detenidas disponibles** (sumarían 96 vCPU + 209 GB RAM — cabe en kronos).

> [!info] `agent` (qemu/118) es **la VM que corre Hermes-agent**. Vive en kronos (no en `hermes-vm` como el README global sugiere). Drift entre docs: el README menciona `hermes-vm .122` como "agente IA" pero la VM real que ejecuta al agente es qemu/118 en kronos. ❓ Necesita refresh.

## 🛡️ Ceph

`kronos` es Ceph MON + MGR standby + 2× OSDs:

| Servicio | Estado |
|---|---|
| ceph-mon | activo (quorum: hera, zeus, kronos) |
| ceph-mgr | **standby** (primary: zeus) |
| ceph-osd.1 | up (333 GB usado / 932 GiB raw — **35%**) |
| ceph-osd.3 | up (378 GB usado / 932 GiB raw — **40%**, **slow ops**) |

> [!warning] OSD.3 (kronos) tiene slow operations
> Performance degradada para escrituras. Verificar SMART del disco NVMe.

## 🔌 Servicios systemd

| Estado | Cantidad |
|---|---|
| Running | ceph-mon, ceph-osd (×2), pve-cluster, pveproxy, sshd, etc. |
| Failed | **0** ✅ |

## 🚨 Alertas en este nodo

| Severidad | Alerta |
|---|---|
| 🟡 | OSD.3 (kronos) — slow operations en BlueStore |
| 🟡 | iSCSI LUNs `sdg/sdh/sdi/sdj` (4 dispositivos) están como raw / sin filesystem visible localmente |

---

## Source files

- `/home/hermes/aranea/topology/discovery/kronos_20260628_211812.txt`
- `/home/hermes/aranea/topology/services.md`

## Captured

2026-06-28 21:18 UTC. Doc generado 2026-06-30.
