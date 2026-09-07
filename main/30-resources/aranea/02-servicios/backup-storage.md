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

# Backup & Storage — TrueNAS, minio

## Propósito

Documentación canónica legacy de [[Aranea]]; se conserva el contenido histórico y su estado requiere verificación antes de uso operativo.

## Contenido


> **Capturado**: 2026-06-28
> **Task 2 ampliará este doc** con AUDIT.md profundo + BACKUP-SYSTEM.md (ticket `2026-06-30-011`)

## TrueNAS (qemu/145)

Ver detalle completo en [[../01-topologia/nodo-truenas]] y [[../03-storage/README]].

### Resumen de exports

#### NFS (4 exports)

| Path | Redes | Notas |
|---|---|---|
| `/mnt/pool0/proxmox_storage` | (sin restricción) | Datastore NFS compartido para Proxmox (1.6 TB) |
| `/mnt/pool0/apps/frigate/config` | 192.168.31.0/24 | Config Frigate |
| `/mnt/pool0/apps/frigate/storage/media` | 192.168.31.0/24 | Videos NVR |
| `/mnt/pool0/trading_documents` | (sin restricción) | Compartido |

#### SMB (3 shares)

| Share | Path | Guest | Datos |
|---|---|---|---|
| `aranea_storage` | `/mnt/pool0/aranea_storage` | no | 998 GB usados (47%) |
| `trading_systems` | `/mnt/pool0/trading_systems` | no | 485 GB usados (31%) |
| `trading_documents` | `/mnt/pool0/trading_documents` | **sí** ⚠️ | 24 MB |

#### iSCSI

| Target | Portal | Contenido |
|---|---|---|
| `iscsi-aranea` | 192.168.31.91:3260 | `truenas.aranea.local:truenas` |

### Datasets clave para backup

| Path | Tamaño | Función |
|---|---|---|
| `/mnt/pool0/proxmox_storage` | 372 GB | datastore NFS Proxmox (backups, ISOs, templates) |
| `/mnt/pool0/aranea_storage` | 998 GB | storage general |
| `/mnt/pool0/trading_systems` | 485 GB | datos trading MT4 |
| `/mnt/pool2/backup/trading_systems` | 305 GB | **backup** trading_systems |
| `/mnt/pool2/backup/aranea_storage` | 39 GB | **backup** aranea_storage |
| `/mnt/pool2/backup/iso_storage` | 15 GB | ISOs |
| `/mnt/pool2/pool0_backup` | (mirror lógico) | snapshot ZFS de pool0 |
| `/mnt/pool2/zfs_backup` | — | snapshot ZFS |

## minio (qemu/157)

| Item | Valor |
|---|---|
| **Propósito** | Storage S3-compatible (alternativa on-prem a AWS S3) |
| **VMID** | 157 |
| **Tipo** | qemu VM |
| **Nodo** | hades |
| **vCPUs** | 4 |
| **RAM** | 8 GB |
| **Disco** | 20 GB |
| **NetIn** | 10 GB |
| **NetOut** | 13 GB |
| **Estado** | ✅ Running |

> [!warning] minio SPOF en hades
> minio corre en hades. Si hades cae → S3-compatible storage cae.

## Backups identificados en `pool2/backup/`

```
pool2/backup/
├── trading_systems/        (305 GB)
├── aranea_storage/         (39 GB)
├── iso_storage/            (15 GB)
├── portainer/              (995 MB)
└── (varios más)
```

## Estado de backups (evaluación inicial, NO exhaustiva)

| Aspecto | Estado actual | Recomendación |
|---|---|---|
| Snapshots ZFS automáticas | ❓ No capturado | Configurar `zfs-auto-snapshot` o sanoid |
| Snapshots Proxmox (vzdump) | ✅ Soportado por `nfs-storage` (proxmox_storage) | Configurar schedule |
| Backup de configs (Traefik, OPNsense, step-ca) | ❓ No capturado | Crear procedimiento |
| Backup obsidian-sync (CouchDB) | ❓ No capturado | `couchdb-backup` o replicación |
| Backup 3-2-1 | ❌ No hay off-host | Crítico — agregar off-host copy |
| UPS para shutdown ordenado | ❌ truenas UPS STOPPED | Configurar UPS |

## Alertas

| # | Severidad | Alerta |
|---|---|---|
| 1 | 🔴 | **TrueNAS VM en hades** — si hades cae se cae TODO el storage compartido |
| 2 | 🟠 | `pool2` (donde están los backups) **sin redundancia** — disco único |
| 3 | 🟠 | Scrub de pool2 obsoleto (11 meses) — bit-rot no detectado |
| 4 | 🟠 | Sin UPS — corrupción ZFS posible en corte eléctrico |
| 5 | 🟡 | minio en hades (otro SPOF) |
| 6 | 🟡 | No hay off-host backup |

## Acción inmediata

> Esta sección es **inventario**. La **auditoría profesional profunda + diseño de sistema de backup** se ejecuta en **Task 2** (ticket `2026-06-30-011`) y produce:
> - `03-storage/AUDIT.md` (análisis detallado de cada storage)
> - `03-storage/BACKUP-SYSTEM.md` (3-2-1, snapshots ZFS, off-host, Proxmox Backup Server)
> - `04-backups/runbook.md` (procedimientos semanales)

---

**Source files**: `/home/hermes/aranea/topology/services.md`, `/home/hermes/aranea/topology/discovery/{truenas,hades}_20260628_211812.txt`, `/home/hermes/aranea/topology/nodes/truenas.md`

**Captured**: 2026-06-28 21:18 UTC. Doc generado 2026-06-30.
