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

# nodo-athena — Gateway + servicios de red

## Propósito

Documentación canónica legacy de [[Aranea]]; se conserva el contenido histórico y su estado requiere verificación antes de uso operativo.

## Contenido


> **Estado**: ✅ OK con alertas de diseño
> **Capturado**: 2026-06-28 vía `agent-read all`
> **Fuente**: `/home/hermes/aranea/topology/discovery/athena_20260628_211812.txt`
> **Ping check 2026-06-30**: ✅ responde ICMP

## 🪪 Identidad

| Item | Valor |
|---|---|
| Hostname | `athena` |
| IP LAN | `192.168.31.10` |
| IP Ceph | — (no participa en Ceph, **solo corosync**) |
| Gateway | `192.168.31.1` |
| Rol | Gateway de red + servicios de red (OPNsense, Pi-hole, Traefik) + etcd member |
| Chassis | desktop 🖥️ (Default string — HW vendor no detectado) |

## ⚙️ Hardware

| Item | Valor |
|---|---|
| CPU | Intel Core i7-13620H (13th Gen) @ 4.3 GHz (max 4.9 GHz) |
| Cores / threads | 10 cores × 2 = **16 threads** |
| Cache L3 | 24 MiB |
| RAM | 15 GiB total (16 GB nominal), swap 8 GB |
| Uso de RAM | 11 GiB usados / 1.4 GiB free / 4.3 GiB available |
| Hypervisor | PVE nativo (no es VM) |

## 🐧 OS + Kernel

| Item | Valor |
|---|---|
| OS | Debian GNU/Linux 12 (bookworm) |
| Kernel | `6.8.12-17-pve` (los demás nodos en `-18-pve` — drift menor) |
| PVE Manager | `8.4.19/a68fb383814bb1e6` |
| Uptime (al 2026-06-28) | 136 días, 2h22 |
| Timezone | America/Santiago (asumido por default Debian) |

> [!warning] Drift de kernel
> athena corre kernel `-17-pve`, los demás `-18-pve`. Cosmético pero conviene `apt update && apt upgrade` + reboot en próxima ventana de mantenimiento.

## 🌐 Red

| Interfaz | Estado | Notas |
|---|---|---|
| `lo` | UNKNOWN | 127.0.0.1/8, ::1/128 |
| `enp2s0` | UP | sin IP |
| `enp3s0` | UP | sin IP |
| `enp4s0` | DOWN | NO-CARRIER (cable desconectado o puerto apagado) |
| `enp5s0f0np0` | UP | slave de bond0 (active) |
| `enp5s0f1np1` | DOWN | NO-CARRIER (slave de bond0) |
| `enp5s0f2np2` | DOWN | NO-CARRIER (slave de bond0) |
| `enp5s0f3np3` | UP | slave de bond0 (active) |
| `bond0` | UP | master de vmbr0 (LAG VEPA) |
| `bond1` | UP | master de vmbr1 (LAG failover) |
| `vmbr0` | UP | IPv6 link-local `fd27:9003:c298:e14:62be:b4ff:fe1f:78c0/64` |
| `vmbr1` | UP | `192.168.31.10/24` ← LAN principal |
| `vmbr2` | UP | IPv6 link-local |

### Rutas

```
default via 192.168.31.1 dev vmbr1
192.168.31.0/24 dev vmbr1  src 192.168.31.10
```

### VLANs observadas

- `enp4s0` (DOWN): VLAN 1 PVID Egress Untagged
- `bond0`: VLAN 1 PVID + 4094 VLANs tagged (configuración estándar)

## 💾 Almacenamiento local

### Discos físicos

| Disco | Tamaño | FSTYPE | Modelo | Notas |
|---|---|---|---|---|
| `sda` (iSCSI) | 50 GB | misc | iSCSI Disk `e9fef...` | (LUN remoto via iSCSI — ver [[03-storage/iscsi-target]]) |
| `sdb` (iSCSI) | 200 GB | raw | iSCSI Disk `e9f0bd...` | (LUN remoto via iSCSI) |
| `sdc` (iSCSI) | 200 GB | raw | iSCSI Disk `613f83...` | (LUN remoto via iSCSI) |
| `sdd` (iSCSI) | 32 GB | xfs | iSCSI Disk `55adbd...` | (LUN remoto via iSCSI) |
| `sde` (iSCSI) | 32 GB | xfs | iSCSI Disk `c8868b...` | (LUN remoto via iSCSI) |
| `sdf` (iSCSI) | 100 GB | ext4 | iSCSI Disk `cb144...` | (LUN remoto via iSCSI) |
| `nvme0n1` | 476.9 GB | LVM2 | YMTC PC210-512GB-D | Boot + system |

### LVM (volume group `pve`)

| LV | Tamaño | Mount |
|---|---|---|
| `pve-swap` | 8 GB | [SWAP] |
| `pve-root` | 96 GB | `/` |
| `pve-data` (thin) | 348.8 GB | thinpool (aloja VMs athena) |

### VMs en `local-lvm` (athena)

| VMID | Disco | Tamaño |
|---|---|---|
| 130 (opnsense) | `pve-vm--130--disk--0` | 64 GB |
| 130 (opnsense) | `pve-vm--130--disk--1` | 4 MB (efivars) |
| 149 (pi-hole) | `pve-vm--149--disk--0` | 10 GB ext4 |
| 101 (etcd-athena) | `pve-vm--101--disk--1` | 10 GB ext4 |
| 101 (etcd-athena) | `pve-vm--101--disk--2` | 8 GB ext4 |
| 115 (traefik) | `pve-vm--115--disk--0` | 16 GB ext4 |

### `df`

```
/dev/mapper/pve-root   ext4       94G  8.6G   81G  10%  /
192.168.31.91:/mnt/pool0/proxmox_storage  nfs4  1.5T  372G  1.2T  25%  /mnt/pve/nfs-storage
```

## 📦 Storages Proxmox disponibles en athena

| Storage | Tipo | Contenido | Notas |
|---|---|---|---|
| `local` | dir | iso,backup,vztmpl | `/var/lib/vz`, 100 GB total, 9% usado |
| `local-lvm` | lvmthin | rootdir,images | 365 GB total, 7% usado |
| `nfs-storage` | nfs | todo | 192.168.31.91:/mnt/pool0/proxmox_storage, 1.5 TB total, 25% usado |
| `pool1` | rbd | images,rootdir | Ceph compartido (75% usado) |
| `iscsi-aranea` | iscsi | images | truenas portal |
| `local-sqx-zeus`, `local-sqx-hera`, `local-sqx-kronos`, `pool-kronos` | lvm | — | Solo visibles desde sus nodos |

## 🖥️ VMs y LXCs corriendo en athena

| VMID | Tipo | Nombre | Status | CPU | RAM | Disco | Tags |
|---|---|---|---|---|---|---|---|
| 101 | lxc | etcd-athena | running | 1 | 2 GB | 10 GB | — |
| 115 | lxc | traefik | running | 2 | 2 GB | 16 GB | community-script; proxy |
| 130 | qemu | opnsense | running | 8 | 8 GB | 64 GB | — |
| 149 | lxc | pi-hole | running | 2 | 1 GB | 10 GB | adblock; community-script |

**Total athena**: 4 corriendo, 13 vCPU asignados, 19.5 GB RAM asignados, uptime muy alto (algunos >1 año).

> [!danger] SPOF de red
> **OPNsense (qemu/130) corre como VM en athena**. Si athena se cae → OPNsense cae → toda la red se va con él. Considerar HA con CARP o migración a hardware dedicado.

## 🔌 Servicios systemd

| Estado | Cantidad |
|---|---|
| Running | (largo — incluye cluster PVE, sshd, chronyd, rpcbind, iscsid, pve-cluster, pveproxy, etc.) |
| Failed | **0** ✅ |

## 🛡️ Ceph

| Item | Estado |
|---|---|
| Participación Ceph | ❌ NO participa (no corre ceph-mon, ceph-mgr, ceph-osd) |
| Participación corosync | ✅ Sí (quórum) |
| Storage Ceph usado | `pool1` (compartido) — 760 GB usados en `storage/athena/pool1` |

`ceph_status` en este nodo retorna `Error: ObjectNotFound('RADOS object not found')` — esperado, athena no tiene config Ceph local.

## 🚨 Alertas activas en este nodo

| Severidad | Alerta |
|---|---|
| 🟠 | OPNsense VM en athena → SPOF de red (ver [[../00-index]] § alertas) |
| 🟡 | Kernel drift: -17-pve vs -18-pve de los demás |
| 🟡 | 3 slaves de bond0 están DOWN (enp4s0, enp5s0f1np1, enp5s0f2np2). bond0 funciona con 2 de 4 slaves activos. |

## 💻 Tráfico de red relevante (acumulado de VMs)

| VMID | Nombre | NetIn | NetOut |
|---|---|---|---|
| 130 | opnsense | 1.72 TB | **6.20 TB** (tráfico WAN) |
| 149 | pi-hole | 128 GB | 2.6 GB |
| 101 | etcd-athena | 228 GB | 99 GB |
| 115 | traefik | 18 GB | 3.2 GB |

---

## Source files

- `/home/hermes/aranea/topology/discovery/athena_20260628_211812.txt`
- `/home/hermes/aranea/topology/services.md`
- `/home/hermes/aranea/topology/README.md`

## Captured

2026-06-28 21:18 UTC (data cruda vía `agent-read all`). Doc generado 2026-06-30, drift = 2 días.
