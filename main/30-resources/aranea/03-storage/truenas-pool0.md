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

# TrueNAS pool0 (storage principal)

## Propósito

Documentación canónica legacy de [[Aranea]]; se conserva el contenido histórico y su estado requiere verificación antes de uso operativo.

## Contenido


> **Capturado**: 2026-06-28
> **Estado**: ✅ ONLINE, scrub reciente, **sin alertas críticas**

## Resumen

| Item | Valor |
|---|---|
| **Pool** | `pool0` |
| **Topología** | 4 mirror vdevs (data) + 1 mirror vdev (special) |
| **Raw total** | 4.48 TB (4 × 996 GB) |
| **Usado** | 2.49 TB |
| **Libre** | 1.99 TB |
| **% uso** | 57% (fragmentación 28%) |
| **Autotrim** | ON (correcto para SSDs) |
| **Último scrub** | 2026-06-28 (hoy), 1h13min, 0 errores ✅ |

## Topología detallada (de la discovery)

### 4 mirror vdevs (data)

| Mirror | Disco 1 | Disco 2 |
|---|---|---|
| **mirror-0** | `sdc` (QEMU HARDDISK 2308E6B304D1) | `sdf` (QEMU HARDDISK 2308E6B304E8) |
| **mirror-1** | `sda` (QEMU HARDDISK 2308E6B304EB) | `sdi` (QEMU HARDDISK 2308E6B305FA) |
| **mirror-2** | `sdb` (QEMU HARDDISK 2341E8804152) | `sdd` (QEMU HARDDISK 2428E8BB8C87) |
| **mirror-3** | `sde1` (sde) | `sdh` (QEMU HARDDISK 2511E9AEC888) |

> Todos son **discos virtuales QEMU** de 996 GB (931.5 GiB) cada uno. En hades aparecen como `sda-sdh` con FSTYPE `zfs_member`.

### Special vdev (mirror-4)

| Disco | Detalle |
|---|---|
| `sdk1` (NE-512 2280, 476 GB) | special vdev disk 1 |
| `sdj1` (GIGABYTE G325E500G, 476 GB) | special vdev disk 2 |

> El **special vdev** en ZFS almacena metadatos y bloques pequeños. Mejor rendimiento y menor latencia para escrituras sync. **Esencial para pools con muchos archivos pequeños.**

## Datasets en pool0

| Dataset | Usado | % pool | Función |
|---|---|---|---|
| `aranea_storage` | 998 GB | 47% | Storage general |
| `proxmox_storage` | 372 GB | 25% | Datastore NFS Proxmox |
| `trading_systems` | 485 GB | 31% | Datos MT4 |
| `trading_documents` | 24 MB | <1% | Compartido |
| `apps/frigate/config` | ❓ pequeño | — | Config Frigate |
| `apps/frigate/storage/media` | ❓ creciendo | — | Videos NVR |
| `apps/postgresql` | ❓ | — | DB PostgreSQL dump |
| `apps/mongodb` | ❓ | — | DB Mongo dump |
| `ix-applications/k3s` | ❓ | — | k3s embebido |
| (otros) | — | — | |

## Alertas

| # | Severidad | Alerta |
|---|---|---|
| 1 | 🟢 | Scrub reciente y sin errores |
| 2 | 🟢 | Autotrim ON (correcto para SSDs) |
| 3 | 🟡 | Sin UPS → corrupción ZFS posible en corte eléctrico |
| 4 | 🟡 | Sin backup remoto → si hades pierde los QEMU disks, se pierde pool0 |

## Operaciones desde PVE

- **NFS** sobre `pool0/proxmox_storage` → montado en `/mnt/pve/nfs-storage` en todos los nodos
- **SMB** sobre `pool0/aranea_storage`, `pool0/trading_systems`, `pool0/trading_documents`
- **iSCSI** sobre `pool0` (LUN `iscsi-aranea` exportado a Proxmox)

## Roadmap

- [ ] Configurar UPS con shutdown ordenado (ver `health.md` §6)
- [ ] Configurar scrub semanal automático
- [ ] Implementar backup remoto (off-host) — **Task 2**
- [ ] Snapshots ZFS automatizadas (sanoid / zfs-auto-snapshot)

---

## Source files

- `/home/hermes/aranea/topology/nodes/truenas.md`
- `/home/hermes/aranea/topology/discovery/truenas_20260628_211812.txt`

## Captured

2026-06-28 21:18 UTC. Doc generado 2026-06-30.
