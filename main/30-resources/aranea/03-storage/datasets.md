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

# Datasets (ZFS en truenas)

## Propósito

Documentación canónica legacy de [[Aranea]]; se conserva el contenido histórico y su estado requiere verificación antes de uso operativo.

## Contenido


> **Capturado**: 2026-06-28

## Resumen por pool

| Pool | Tamaño raw | Usado | Libre | % |
|---|---|---|---|---|
| boot-pool | 30 GB | 5 GB | 25 GB | 17% |
| pool0 | 4.48 TB | 2.49 TB | 1.99 TB | 57% |
| pool2 | 7.99 TB | 3.51 TB | 4.48 TB | 44% |

## pool0 datasets

| Dataset | Usado | % del pool | Función |
|---|---|---|---|
| `aranea_storage` | 998 GB | 47% | Storage general |
| `proxmox_storage` | 372 GB | 25% | Datastore NFS Proxmox |
| `trading_systems` | 485 GB | 31% | Datos MT4/MT5 |
| `trading_documents` | 24 MB | <1% | Documentos trading |
| `apps/frigate/config` | ❓ pequeño | — | Config Frigate |
| `apps/frigate/storage/media` | ❓ creciendo | — | Videos NVR (gran consumo) |
| `apps/postgresql` | ❓ | — | Dump PostgreSQL (¿backup?) |
| `apps/mongodb` | ❓ | — | Dump MongoDB (¿backup?) |
| `ix-applications/k3s` | ❓ | — | k3s embebido en TrueNAS |

## pool2 datasets

| Dataset | Usado | Función |
|---|---|---|
| `pool0_backup` | ❓ | **Mirror lógico de pool0** (snapshots ZFS) |
| `zfs_backup` | ❓ | Snapshots ZFS |
| `backup/trading_systems` | 305 GB | **Backup** trading_systems |
| `backup/aranea_storage` | 39 GB | **Backup** aranea_storage |
| `backup/iso_storage` | 15 GB | **ISOs** |
| `backup/portainer` | 995 MB | Portainer data |
| `ix-apps` | ❓ | Apps TrueNAS nativas |

## Política de snapshots

> [!warning] Política de snapshots no documentada
> El wrapper `agent-read` no expone la configuración de snapshots automáticos (`zfs-auto-snapshot`, `sanoid`, o manual). **Necesita refresh** con introspección de:
> - `zfs list -t snapshot`
> - `/etc/cron.d/zfs-auto-snapshot` o similar
> - TrueNAS Tasks → Periodic Snapshot Tasks

## Distribución de uso de disco

```
pool0 (4.48 TB raw):
├── aranea_storage    998 GB ████████████████████░░░░░░░░░░  47%
├── proxmox_storage   372 GB ████████░░░░░░░░░░░░░░░░░░░░░░  25%
├── trading_systems   485 GB ██████████░░░░░░░░░░░░░░░░░░░░  31%
├── trading_documents  24 MB ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  <1%
└── apps/             ❓     ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░   ?

pool2 (7.99 TB raw):
├── backup/*          ~360 GB ████░░░░░░░░░░░░░░░░░░░░░░░░░░  ~44%
├── pool0_backup      ❓      ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░   ?
└── zfs_backup        ❓      ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░   ?
```

## Pendientes

- [ ] Listar `zfs list -t snapshot -o name,creation,used,refer` (manualmente o ampliar wrapper)
- [ ] Documentar política de retención
- [ ] Configurar replicación ZFS off-host (Task 2 debería cubrirlo)
- [ ] Snapshots pre/post deploy

---

## Source files

- `/home/hermes/aranea/topology/nodes/truenas.md`
- `/home/hermes/aranea/topology/discovery/truenas_20260628_211812.txt`

## Captured

2026-06-28 21:18 UTC. Doc generado 2026-06-30.
