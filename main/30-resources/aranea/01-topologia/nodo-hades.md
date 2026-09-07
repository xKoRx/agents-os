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

# nodo-hades — Compute-heavy (22 VMs running)

## Propósito

Documentación canónica legacy de [[Aranea]]; se conserva el contenido histórico y su estado requiere verificación antes de uso operativo.

## Contenido


> **Estado**: ⚠️ Atención — **74% RAM usado + sin OSDs Ceph + aloja truenas VM**
> **Capturado**: 2026-06-30 19:44 UTC vía `agent-read all`
> **Fuente primaria**: `/home/hermes/aranea/topology/discovery/hades_20260630_194423.txt`
> **Fuente previa (superseded)**: `/home/hermes/aranea/topology/discovery/hades_20260628_211812.txt`
> **Ping check 2026-06-30**: ✅ responde ICMP

## 🪪 Identidad

| Item | Valor |
|---|---|
| Hostname | `hades` |
| IP LAN | `192.168.31.90` |
| IP Ceph | `10.10.10.90` (peso 0, **sin OSDs**) |
| Gateway | `192.168.31.1` |
| Rol | Compute-heavy (22 VMs corriendo), aloja TrueNAS VM (qemu/145) |
| Hardware Vendor | HUANANZHI (X99-F8D PLUS) |
| Firmware | 5.11 |

## ⚙️ Hardware

| Item | Valor |
|---|---|
| CPU | **2× Intel Xeon E5-2697 v4** (18 cores × 2 = 36 cores × 2 SMT = **72 threads**) |
| Vendor ID | GenuineIntel |
| RAM | **251 GiB** total, swap 8 GB |
| Uso de RAM | **186 GiB usados / 30 GiB free / 65 GiB available** ⚠️ |
| Hypervisor | PVE nativo |

> [!warning] hades está al 74% de RAM
> De 251 GB RAM, 186 GB están en uso (74%). Margen limitado si se prenden las VMs detenidas (`win-development`: 32 GB, `sqx-ulab-hera-0`: 100 GB — esta última NO está en hades, está en hera).

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
| `enp7s0` | UP | en bond0 |
| `enp8s0` | UP | en bond0 |
| `enp4s0f1` | UP | (slave de ceph, MTU 9000) |
| `bond0` | UP | master de vmbr0 |
| `vmbr0` | UP | `192.168.31.90/24` |
| `ceph` | UP | `10.10.10.90/24` (MTU 9000, **sin OSDs**) |

### Rutas

```
default via 192.168.31.1 dev vmbr0
10.10.10.0/24 dev ceph  src 10.10.10.90
192.168.31.0/24 dev vmbr0  src 192.168.31.90
```

## 💾 Almacenamiento local

### Discos

| Disco | Tamaño | FSTYPE | Modelo | Notas |
|---|---|---|---|---|
| `sda` | 931.5 GB | zfs_member | CT1000BX500SSD1 | **truenas pool0 mirror-2 (visto desde truenas como `sdc`)** |
| `sdb` | 931.5 GB | zfs_member | CT1000BX500SSD1 | **truenas pool0 mirror-1 (visto como `sda`)** |
| `sdc` | 931.5 GB | zfs_member | CT1000BX500SSD1 | **truenas pool0 mirror-2 (visto como `sdb`)** |
| `sdd` | 931.5 GB | zfs_member | CT1000BX500SSD1 | **truenas pool0 mirror-0** |
| `sde` | 931.5 GB | zfs_member | CT1000BX500SSD1 | **truenas pool0 mirror-3 (visto como `sde1`)** |
| `sdf` | 931.5 GB | zfs_member (part) | CT1000BX500SSD1 | **truenas special mirror** |
| `sdg` | 931.5 GB | zfs_member | CT1000BX500SSD1 | **truenas pool0 mirror-2** |
| `sdh` | 931.5 GB | zfs_member | CT1000BX500SSD1 | **truenas pool0 mirror-3 (visto como `sdh`)** |
| `sdi` | 7.3 TB | zfs_member (part) | ST8000DM004-2U9188 | **truenas pool2** (disco único sin mirror ⚠️) |
| `sdj` (iSCSI) | 50 GB | misc | iSCSI Disk `e9fef...` | (LUN remoto via iSCSI) |
| `sdk` (iSCSI) | 200 GB | raw | iSCSI Disk `e9f0bd...` | |
| `sdl` (iSCSI) | 200 GB | raw | iSCSI Disk `613f83...` | |
| `sdm` (iSCSI) | 32 GB | xfs | iSCSI Disk `55adbd...` | |
| `sdn` (iSCSI) | 32 GB | xfs | iSCSI Disk `c8868b...` | |
| `sdo` (iSCSI) | 100 GB | ext4 | iSCSI Disk `cb144...` | |
| `nvme0n1` | 465 GB | zfs_member (part) | GIGABYTE G325E500G | **truenas special mirror** |
| `nvme1n1` | 476.9 GB | zfs_member (part) | NE-512 2280 | **truenas special mirror** |
| `nvme2n1` | 119.2 GB | LVM2 | NE-128 2280 | Boot + system PVE hades |
| `rbd0..rbd9` | various | (Ceph block devices) | — | RBDs montados por VMs (50G, 50G, 4M, 10G, 4M, 4M, 20G, 4M, 4M, 25G) |

> [!danger] hades es el hypervisor de TrueNAS
> Los 9× SSD `sda-sdh` + `nvme0n1` + `nvme1n1` (NVMe special) + `sdi` (HDD 7.3 TB) son **discos virtuales QEMU** presentados a la VM `truenas` (qemu/145). Si hades cae, **truenas pierde todos sus pools**.
>
> `loop0..loop3` también son dispositivos virtuales (snapshots/lib).

### LVM vg `pve` (boot + system)

| LV | Tamaño | Uso |
|---|---|---|
| `pve-swap` | 8 GB | [SWAP] |
| `pve-root` | 39.6 GB | `/` |
| `pve-data` (thin) | 53.9 GB | thinpool |

### `df`

```
/dev/mapper/pve-root            ext4       39G  9.5G   28G  26%  /
192.168.31.91:/mnt/pool0/proxmox_storage  nfs4   1.5T  372G  1.2T  25%  /mnt/pve/nfs-storage
```

## 📦 Storages Proxmox disponibles en hades

| Storage | Tipo | Tamaño | Uso |
|---|---|---|---|
| `local` | dir | 41 GB | iso,vztmpl,backup (25% usado) |
| `local-lvm` | lvmthin | 58 GB | rootdir,images (62% usado) |
| `nfs-storage` | nfs | 1.5 TB | 25% usado |
| `pool1` | rbd | 1 TB | 75% usado |
| `iscsi-aranea` | iscsi | — | truenas |

> [!note] hades NO tiene storage local grande
> Todo lo gordo (`pool1` Ceph, `nfs-storage`, `iscsi-aranea`) viene de la red. hades es un consumidor **neto** de storage.

## 🖥️ VMs corriendo en hades (22 — el 75% del cluster)

### QEMU

| VMID | Nombre | Status | CPU | RAM | Disco | Notas |
|---|---|---|---|---|---|---|
| 105 | homeassistant | running | 4 | 8 GB | 50 GB | Smart home |
| 124 | mt4-real | **running** | 8 | 8 GB | 50 GB | **Cuenta real (producción)** ⚠️ |
| 125 | mt4-test | running | 8 | 16 GB | 50 GB | |
| 133 | mt4-ftmo | running | 8 | 8 GB | 50 GB | FTMO prop firm |
| 134 | mt4-ttp | running | 8 | 8 GB | 50 GB | TTP trend following |
| 140 | echo | running | 4 | 8 GB | 20 GB | |
| 144 | mt4-demo | running | 4 | 16 GB | 50 GB | |
| 145 | truenas | running | 30 | 32 GB | 32 GB | ⚠️ turtles all the way down |
| 151 | win-development | **stopped** | 16 | 32 GB | 200 GB | (32 GB RAM detenida) |
| 152 | postgresql | running | 8 | 24 GB | 20 GB | DB principal |
| 153 | mongodb | running | 8 | 24 GB | 20 GB | |
| 157 | minio | running | 4 | 8 GB | 20 GB | S3-compatible |
| 158 | temporal | running | 4 | 8 GB | 32 GB | Workflow engine |
| 159 | ubuntu-dev | running | **24** | **64 GB** | 100 GB | dev workstation |
| 160 | argus | running | 8 | 16 GB | 32 GB | (¿monitoreo IA?) |

### LXC

| VMID | Nombre | Status | CPU | RAM | Disco |
|---|---|---|---|---|---|
| 103 | emqx | running | 2 | 1 GB | 4 GB | broker MQTT |
| 113 | mcps | running | 2 | 4 GB | 8 GB | MCP servers |
| 116 | obsidian-sync | running | 2 | 2 GB | 64 GB | CouchDB (candidato a SPOF si hades cae) |
| 126 | docker-flink | running | 20 | 32 GB | 50 GB | Apache Flink (32 GB RAM!) |
| 127 | docker-observability | running | 6 | 15 GB | 25 GB | Stack monitoreo |
| 129 | docker-hasura | running | 4 | 8 GB | 50 GB | |
| 137 | docker-frigate.14 | running | 5 | 12 GB | 50 GB | NVR (10.5 TB netin ⚠️) |
| 141 | docker-echo-dev | running | 12 | 4 GB | 20 GB | |
| 147 | etcd-hades | running | 1 | 4 GB | 18 GB | Miembro etcd |
| 148 | etcd-keeper | running | 1 | 2 GB | 10 GB | etcd UI |

**Total hades**: **22 corriendo** (15 qemu + 10 LXC, pero algunos del listado son stopped), 152 vCPU asignados, 240 GB RAM asignados. **1 VM detenida disponible** (`win-development`: 16 vCPU / 32 GB RAM).

## 🛡️ Ceph

`hades` es miembro corosync con quórum pero **NO participa en Ceph**:

| Servicio | Estado |
|---|---|
| ceph-mon | ❌ NO |
| ceph-mgr | ❌ NO |
| ceph-osd | ❌ NO (weight 0) |

`ceph_status` local retorna error (`RADOS object not found`). Esperado — hades no tiene config Ceph local.

> [!danger] hades consume Ceph pero no contribuye
> `hades` está en corosync con quórum, tiene bridge `ceph` configurado (MTU 9000), pero **NO corre ceph-mon/ceph-osd/ceph-mgr**. Aparece en `ceph_osd_tree` como `host hades weight 0`.
>
> Si hades crece y necesita más disco local, todo va a Ceph que ya está al 75% usado.

## 🔌 Servicios systemd

| Estado | Cantidad |
|---|---|
| Running | 47 unidades incluyendo pve-cluster, pveproxy, pvedaemon, pve-ha-crm, pve-ha-lrm, pve-firewall, ceph-crash, lxcfs, etc. |
| Failed | **0** ✅ |

### Servicios PVE activos relevantes

- `pve-container@{103,113,116,126,127,129,137,141,147,148}.service` — todos los LXC
- `pve-firewall`, `pve-ha-crm`, `pve-ha-lrm`, `pve-lxc-syscalld`, `pveproxy`, `pvedaemon`
- `qmeventd`, `spiceproxy`, `pvestatd`, `pvefw-logger`
- `smartmontools` (SMART daemon activo ✅)
- `zfs-zed` (ZFS Event Daemon activo ✅)

## 🚨 Alertas activas en este nodo

| # | Severidad | Alerta |
|---|---|---|
| 1 | 🔴 | **TrueNAS VM (qemu/145) corre acá** — si hades cae → truenas cae → TODO el cluster queda sin NFS/iSCSI. Riesgo "turtles all the way down". |
| 2 | 🟠 | hades no contribuye a Ceph (peso 0, sin OSDs) — consumidor neto |
| 3 | 🟡 | RAM al 74% (186/251 GB) — margen limitado |
| 4 | 🟡 | `obsidian-sync` (LXC 116) está acá — si hades cae, **se pierde la sincronización del vault de Obsidian** |
| 5 | 🟡 | docker-frigate.14 (LXC 137) tiene **10.5 TB netin** acumulado — tráfico NVR altísimo |

### Otros datos curiosos

- **MT4 trading** concentrado 100% acá (5 instancias running: real, test, ftmo, ttp, demo + 1 stopped)
- **PostgreSQL + MongoDB** bases de datos productivas, ambas acá
- **docker-flink** (32 GB RAM) — cluster Kafka → Flink pasa por acá
- **docker-frigate** (12 GB RAM, NVR) — ingiere video de las cámaras
- **`ubuntu-dev`** (24 vCPU / 64 GB RAM) — la workstation de Rodrigo

---

## Source files

- `/home/hermes/aranea/topology/discovery/hades_20260630_194423.txt` (primaria)
- `/home/hermes/aranea/topology/discovery/hades_20260628_211812.txt` (histórica, superseded)
- `/home/hermes/aranea/topology/services.md`
- `/home/hermes/aranea/topology/health.md`

## Captured

**2026-06-30 19:44 UTC** (refresh). Doc actualizado 2026-06-30. Captura previa: 2026-06-28 21:18 UTC (superseded por drift).
