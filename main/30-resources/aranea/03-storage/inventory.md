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

# Storage Inventory — landscape completo

## Propósito

Documentación canónica legacy de [[Aranea]]; se conserva el contenido histórico y su estado requiere verificación antes de uso operativo.

## Contenido


> **Capturado**: 2026-06-28
> **Generado**: 2026-06-30

## Vista global

| Componente | Tipo | Tamaño raw | Usado | Libre | % Uso | Nodo(s) | Notas |
|---|---|---|---|---|---|---|---|
| **Ceph pool1** | RBD distribuido | 3.6 TiB | 2.1 TiB | 1.6 TiB | 57% raw / 75% pool | hera, kronos, zeus (hades: peso 0) | HEALTH_WARN |
| **Ceph .mgr** | RBD metadata | 13 MiB | 13 MiB | — | — | distribuido | overhead |
| **Truenas boot-pool** | ZFS mirror-1 | 30 GB | 5 GB | 25 GB | 17% | truenas VM | SO |
| **Truenas pool0** | ZFS 4 mirrors + special | 4.48 TB | 2.49 TB | 1.99 TB | 57% | truenas VM | OK |
| **Truenas pool2** | ZFS single disk | 7.99 TB | 3.51 TB | 4.48 TB | 44% | truenas VM | ⚠️ sin mirror |
| **LVM local athena** | lvmthin `pve` | 365 GB | 27 GB | 338 GB | 7% | athena | local-lvm |
| **LVM local zeus** | lvmthin `pve` | 429 GB | 89 GB | 340 GB | 21% | zeus | local-lvm |
| **LVM local hera** | lvmthin `pve` | 363 GB | 105 GB | 258 GB | 29% | hera | local-lvm |
| **LVM local kronos** | lvmthin `pve` | 58 GB | 2.4 GB | 56 GB | 4% | kronos | local-lvm |
| **LVM local hades** | lvmthin `pve` | 58 GB | 36 GB | 22 GB | 62% | hades | local-lvm |
| **LVM local-sqx-zeus** | lvm | 931 GB | (50+600=650 GB asignados a vm 108) | 281 GB | 70% | zeus | dataset SQX |
| **LVM local-sqx-hera** | lvm | 931 GB | (no usado — vm 123 stopped) | 931 GB | 0% | hera | dataset SQX (sin uso) |
| **LVM local-sqx-kronos** | lvm | 931 GB | (50+600=650 GB asignados a vm 111 stopped) | 281 GB | 70% | kronos | dataset SQX |
| **LVM local-kronos** | lvm | 931 GB | (200+50=250 GB asignados) | 681 GB | 27% | kronos | datasets locales |
| **LVM pool-kronos** | lvm | 954 GB | (120+100=220 GB asignados) | 734 GB | 23% | kronos | datasets adicionales |
| **iSCSI LUNs (de truenas)** | iscsi block | ~600 GB total | raw | raw | — | todos (visible como dispositivos raw) | mounted by hades como virtio disks de truenas VM |
| **TOTAL raw cluster** | mixto | **~17.6 TB** | ~9 TB | ~8.6 TB | ~51% | | |

> ⚠️ Números aproximados para LVM locales — derivan de `maxdisk` y `disk` en `pve_resources` por nodo. Los tamaños exactos de VGs requieren introspección no disponible en el wrapper.

## Por nodo — almacenamiento local (sistema)

| Nodo | Disco boot | Capacidad | Usado (root) | % root | Storage local adicional |
|---|---|---|---|---|---|
| athena | NVMe 476 GB | 476 GB | 8.6 GB / 94 GB | 10% | local-lvm (348.8 GB) + 5× iSCSI LUNs |
| zeus | NVMe 465 GB | 465 GB | 15 GB / 49 GB | 31% | local-lvm (399.9 GB) + local-sqx-zeus (931 GB) + 5× iSCSI LUNs |
| hera | NVMe 465 GB | 465 GB | 10 GB / 94 GB | 12% | local-lvm (337.9 GB) + local-sqx-hera (931 GB) + 5× iSCSI LUNs |
| kronos | SSD 232 GB | 232 GB | 12 GB / 166 GB | 7% | local-lvm (53.9 GB) + local-kronos (931 GB) + local-sqx-kronos (931 GB) + pool-kronos (954 GB) + 5× iSCSI LUNs |
| hades | NVMe 119 GB | 119 GB | 9.5 GB / 39 GB | 26% | local-lvm (53.9 GB) + 9 SSD QEMU disks (truenas pool0) + 2× NVMe special mirror + 1× 7.3 TB HDD (truenas pool2) + 5× iSCSI LUNs |

## Tasa de uso por categoría

### Distribución de uso

```
Ceph pool1:        2.1 TiB  ████████████████░░░░░░░░░░░░░░  (57% raw, 75% pool)
Truenas pool0:     2.49 TB  ███████████████████░░░░░░░░░░░  (57%)
Truenas pool2:     3.51 TB  ██████████░░░░░░░░░░░░░░░░░░░░  (44%)
LVM locales PVE:   ~0.3 TB  ██░░░░░░░░░░░░░░░░░░░░░░░░░░░░  (varía)
────────────────────────────────────────────────────────
Total raw cluster: ~17.6 TB ████████████░░░░░░░░░░░░░░░░░░░  (~51%)
```

## Por servicio (¿quién guarda qué?)

| Servicio | Ubicación principal | Backup |
|---|---|---|
| Proxmox VMs (raíces) | `pool1` (Ceph) y `local-lvm` (per-node) | `nfs-storage` (proxmox_storage NFS) — `prune-backups=keep-all` |
| Proxmox templates | `local` (per-node) y `nfs-storage` | `nfs-storage` mismo |
| Proxmox ISOs | `local` (per-node) y `nfs-storage` | `nfs-storage` mismo |
| Datos MT4 | SMB `trading_systems` (pool0, 485 GB) | `pool2/backup/trading_systems/` (305 GB) |
| Datos trading varios | SMB `trading_documents` (pool0, 24 MB) | ❓ no backup |
| Storage general | SMB `aranea_storage` (pool0, 998 GB) | `pool2/backup/aranea_storage/` (39 GB) |
| NVR (Frigate) | NFS `apps/frigate/storage/media` (pool0) | ❓ no backup explícito |
| Configuración Frigate | NFS `apps/frigate/config` (pool0) | ❓ |
| PostgreSQL dump | `apps/postgresql` (pool0) | ❓ |
| MongoDB dump | `apps/mongodb` (pool0) | ❓ |
| SQX datasets (research) | LVM `local-sqx-{zeus,hera,kronos}` | ❓ (dentro de VMs SQX) |
| minio | local-lvm en hades (20 GB) | ❓ |

## Resiliencia actual

| Storage | Redundancia | Riesgo |
|---|---|---|
| Ceph pool1 | 3x replicación (default) | Si caen 2 OSDs simultáneamente → datos perdidos |
| Truenas pool0 | 4 mirrors (data) + 1 mirror (special) | ✅ Muy redundante |
| Truenas pool2 | **single disk** ⚠️ | 🔴 Cualquier falla del disco = pérdida total |
| LVM locales (PVE) | single vg per nodo | 🟡 Si disco muere → VMs afectadas |
| NFS `proxmox_storage` | compartido vía truenas | 🔴 Si truenas cae → todo el cluster pierde acceso |

## Pendientes

- [ ] **AUDIT.md** — análisis detallado de cada storage (Task 2)
- [ ] **BACKUP-SYSTEM.md** — diseño 3-2-1, snapshots ZFS, off-host (Task 2)
- [ ] Wrapper `agent-read` debería exponer `disks` por VG (no solo por disco físico)
- [ ] `smartctl -a` por disco (no capturado en discovery)

---

## Source files

- `/home/hermes/aranea/topology/discovery/{athena,zeus,hera,kronos,hades,truenas}_20260628_211812.txt`
- `/home/hermes/aranea/topology/nodes/truenas.md`
- `/home/hermes/aranea/topology/health.md`

## Captured

2026-06-28 21:18 UTC. Doc generado 2026-06-30.
