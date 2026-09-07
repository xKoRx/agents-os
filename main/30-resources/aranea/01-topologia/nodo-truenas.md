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

# nodo-truenas — TrueNAS Scale (corre como VM en hades)

## Propósito

Documentación canónica legacy de [[Aranea]]; se conserva el contenido histórico y su estado requiere verificación antes de uso operativo.

## Contenido


> **Rol**: Almacenamiento compartido (NFS/SMB) para el cluster Aranea.
> **Recolectado**: 2026-06-28 vía `agent-read all`
> **Fuente**: `/home/hermes/aranea/topology/discovery/truenas_20260628_211812.txt` + `nodes/truenas.md` (template original)
> **Estado**: ✅ Inventario completo, **con alertas críticas de diseño**
> **Ping check 2026-06-30**: ✅ responde ICMP (192.168.31.91)

## 🪪 Identidad

| Item | Valor |
|---|---|
| Hostname | `truenas` |
| IP LAN | `192.168.31.91` |
| **Hipervisor** | **VM qemu/145 corriendo en hades** ⚠️ |
| Gateway | `192.168.31.1` |
| Tráfico acumulado | NetIn no rastreado (loopback), ~28 TB escritos por la VM |

## ⚙️ Hardware (asignado por hades a la VM)

| Item | Valor |
|---|---|
| vCPUs | 30 (15 cores × 2 sockets, SMT deshabilitado — QEMU KVM full virt) |
| RAM | 32 GB (asignada de los 251 GB de hades) |
| Disco sistema | 32 GB (boot-pool en ZFS) |
| Discos data | 9× QEMU HARDDISK (8× 931 GB SSD + 1× 7.3 TB HDD) + 2× SSD (special vdev mirror) |
| Hypervisor reported | QEMU KVM (Standard PC (Q35 + ICH9, 2009)) |

> [!danger] Toda la I/O pasa por hades
> hades → Ceph (si hubiera)/local → red 10GbE → truenas VM. Es la "VM con más tráfico" del cluster — escribir aquí es escribir en los QEMU virtio disks que viven en el LVM de hades.

## 🐧 Software

| Item | Valor |
|---|---|
| OS | TrueNAS Scale 25.04.1 |
| Kernel | Linux 6.12.15-production+truenas |
| Build | 1748248693 (≈ 2025-05-25) |
| Uptime (al 2026-06-28) | 41 días |
| Timezone | America/Santiago |
| Init | systemd |

## 🌐 Red

| Interfaz | Tipo | Estado | Notas |
|---|---|---|---|
| `enp1s0` | 10GbE copper | UP | slave de bond0 (Direct Attach Copper) |
| `enp4s0f0` | 10GbE copper | UP | slave de bond0 |
| `enp4s0f1` | 10GbE copper | UP | miembro de br0 (link-local only) |
| `bond0` | LAG failover | UP | `192.168.31.91/24` |
| `br0` | bridge | UP | sin IPv4, IPv6 link-local |
| `lo` | loopback | UP | 127.0.0.1 |

**bond0 LAG protocol = FAILOVER** (no LACP), slave ports: enp1s0, enp4s0f0.

### Rutas

```
default via 192.168.31.1 dev bond0 proto static
192.168.31.0/24 dev bond0 proto kernel scope link src 192.168.31.91
```

### Puertos listening relevantes

| Puerto | Servicio |
|---|---|
| 22 | SSH (sshd) |
| 80, 443 | nginx (reverse proxy local TrueNAS) |
| 111, 2049, 32768+ | NFS |
| 139, 445 | SMB |
| 3260 | iSCSI (iscsitarget) |
| 6000 | middleware TrueNAS API (loopback) |
| 6999 | netdata (loopback, 127.0.0.1) |
| 5353 | avahi-daemon (mDNS) |

## 💾 Almacenamiento (zpools)

### `boot-pool`

- 30 GB total, 5 GB usados, 25 GB libres
- SO TrueNAS
- Último scrub: 2026-06-22 ✅

### `pool0` (storage principal)

- **4.4 TB raw, 2.5 TB usados, 1.9 TB libres**
- **4 mirror vdevs** (8× QEMU virtio 931 GB SSD) + **special vdev mirror** (2× SSD 465 GB)
- `autotrim=on` (correcto para SSDs)
- Último scrub: **2026-06-28** (hoy), 1h13min, 0 errores ✅
- Fragmentación: 28% (moderada, aceptable)

Topología detallada (por mirror):
- `mirror-0`: scsi-0QEMU_QEMU_HARDDISK_2308E6B304D1 (sdc) ↔ scsi-0QEMU_QEMU_HARDDISK_2308E6B304E8 (sdf)
- `mirror-1`: scsi-0QEMU_QEMU_HARDDISK_2308E6B304EB (sda) ↔ scsi-0QEMU_QEMU_HARDDISK_2308E6B305FA (sdi)
- `mirror-2`: scsi-0QEMU_QEMU_HARDDISK_2341E8804152 (sdb) ↔ scsi-0QEMU_QEMU_HARDDISK_2428E8BB8C87 (sdd)
- `mirror-3`: sde1 ↔ scsi-0QEMU_QEMU_HARDDISK_2511E9AEC888 (sdh)
- `special` (mirror-4): scsi-0QEMU_QEMU_HARDDISK_9I41014000297-part1 (sdk1) ↔ scsi-0QEMU_QEMU_HARDDISK_SN232308900483-part1 (sdj1)

### `pool2` (bulk storage) ⚠️

- **7.2 TB raw, 3.5 TB usados, 3.7 TB libres**
- **1 disco simple** (`sdg1`, 7.3 TB QEMU virtio) — ST8000DM004-2U9188
- Último scrub: **2025-07-12** (**hace 11 meses — fuera de ventana**) ⚠️
- Sin redundancia

## 📂 Datasets (resumen)

```
pool0/
├── aranea_storage/             (998 GB usados, 47% — storage general)
├── proxmox_storage/            (372 GB usados, 25% — datastore Proxmox NFS)
├── trading_systems/            (485 GB usados, 31% — datos trading)
├── trading_documents/          (24 MB)
├── apps/
│   ├── frigate/{config, storage/media}
│   ├── postgresql/
│   └── mongodb/
├── ix-applications/k3s/        (k3s embebido)
└── (más)

pool2/
├── pool0_backup/               (mirror lógico de pool0, snapshots ZFS)
├── zfs_backup/
├── backup/
│   ├── trading_systems/        (305 GB)
│   ├── aranea_storage/         (39 GB)
│   ├── iso_storage/            (15 GB)
│   ├── portainer/              (995 MB)
│   └── (varios más)
└── ix-apps/                    (apps TrueNAS nativas)
```

## 📡 Shares

### SMB (3 shares)

| Share | Path | Guest | Notas |
|---|---|---|---|
| `aranea_storage` | `/mnt/pool0/aranea_storage` | no | Storage general |
| `trading_systems` | `/mnt/pool0/trading_systems` | no | Datos trading |
| `trading_documents` | `/mnt/pool0/trading_documents` | **sí** ⚠️ | Público para guests |

### NFS (4 exports)

| Path | Redes | Notas |
|---|---|---|
| `/mnt/pool0/proxmox_storage` | (sin restricción) | **Datastore NFS compartido para Proxmox** |
| `/mnt/pool0/apps/frigate/config` | 192.168.31.0/24 | Config Frigate |
| `/mnt/pool0/apps/frigate/storage/media` | 192.168.31.0/24 | Videos NVR |
| `/mnt/pool0/trading_documents` | (sin restricción) | Compartido |

> **Maproot user = root, maproot group = proxmox** para `proxmox_storage`: Proxmox accede como root con grupo proxmox. Estándar.

## 🛡️ Servicios activos

| Servicio | Estado | Notas |
|---|---|---|
| cifs (Samba) | RUNNING | SMB shares |
| iscsi (iscsitarget) | RUNNING | exporta `iscsi-aranea` a Proxmox |
| nfs | RUNNING | NFS server |
| ssh | RUNNING + enable at boot | |
| smartd | RUNNING + enable at boot | ✅ |
| ftp, snmp, ups | **STOPPED** | (sin UPS, sin SNMP) |

### Servicio systemd fallando

```
* rc-local.service loaded failed failed /etc/rc.local Compatibility
```

Hay un `/etc/rc.local` legacy con error. Investigar y limpiar.

## 📊 Storages Proxmox servidos desde truenas

| Storage | Tipo | Tamaño cluster |
|---|---|---|
| `nfs-storage` | NFS | 1.6 TB |
| `iscsi-aranea` | iSCSI | n/a |

Y Ceph usa `pool1` (RBD) que es **separado** del pool0 de truenas — vive en los OSDs NVMe de zeus/hera/kronos.

## 🚨 Alertas críticas

| # | Severidad | Alerta |
|---|---|---|
| 1 | 🔴 | **TrueNAS corre como VM en hades (qemu/145)** — si hades se cae → truenas se cae → NFS + iSCSI caen → TODAS las VMs Proxmox que usan `nfs-storage` o `iscsi-aranea` quedan sin disco. **Recomendación**: mover TrueNAS a bare-metal en una de las máquinas hoy ociosas. |
| 2 | 🟠 | **`pool2` sin redundancia** — disco único (`sdg1`). Cualquier falla del disco = pérdida de: 305 GB trading_systems backup, 39 GB aranea_storage backup, 15 GB iso_storage, todo pool0_backup/ y zfs_backup/. **Recomendación**: migrar a mirror vdev cuando se agreguen discos. |
| 3 | 🟠 | **Scrub de pool2 obsoleto** (11 meses) — silencioso, sin errores, pero no se está validando la integridad. Riesgo de bit-rot no detectado. |
| 4 | 🟠 | **SMB `trading_documents` con `guestok=true`** — cualquier host de la LAN puede leer este share sin autenticarse. **Confirmar que es intencional**. |
| 5 | 🟠 | **UPS no configurado** (`ups STOPPED`) — sin protección eléctrica. Si truenas pierde energía mientras escribe, riesgo de corrupción en ZFS. |
| 6 | 🟡 | **SNMP off** — no hay telemetría hacia监控系统 externo. |
| 7 | 🟡 | **Netdata solo en loopback** — buen monitoring local pero no agregable desde otros nodos. |
| 8 | 🟡 | **`rc-local.service` fallando** — menor, pero denota drift de mantenimiento. |

## ⚡ Comandos útiles

```bash
# Ver todo el estado
ssh agent_ro@192.168.31.91 "sudo -n /mnt/pool0/.agent_ro/bin/agent-read all"

# Solo storage
ssh agent_ro@192.168.31.91 "sudo -n /mnt/pool0/.agent_ro/bin/agent-read storage"

# Comandos manuales útiles (requiere más acceso):
zpool status
zpool iostat -v 2
zfs list -o space
smartctl -a /dev/sda
```

---

## Source files

- `/home/hermes/aranea/topology/discovery/truenas_20260628_211812.txt`
- `/home/hermes/aranea/topology/nodes/truenas.md`

## Captured

2026-06-28 21:18 UTC. Doc generado 2026-06-30.
