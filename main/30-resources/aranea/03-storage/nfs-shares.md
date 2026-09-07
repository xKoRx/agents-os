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

# NFS Exports

## Propósito

Documentación canónica legacy de [[Aranea]]; se conserva el contenido histórico y su estado requiere verificación antes de uso operativo.

## Contenido


> **Capturado**: 2026-06-28
> **Servidor**: truenas (192.168.31.91)
> **Mount point cliente**: `/mnt/pve/nfs-storage` (en todos los PVE nodes)

## Exports

| Path en truenas | Redes permitidas | Mount point en PVE | Función |
|---|---|---|---|
| `/mnt/pool0/proxmox_storage` | **(sin restricción)** | `/mnt/pve/nfs-storage` | Datastore NFS compartido para Proxmox (ISO, templates, backups) |
| `/mnt/pool0/apps/frigate/config` | `192.168.31.0/24` | (montado en docker-frigate) | Configuración de Frigate |
| `/mnt/pool0/apps/frigate/storage/media` | `192.168.31.0/24` | (montado en docker-frigate) | Videos NVR |
| `/mnt/pool0/trading_documents` | **(sin restricción)** | (no montado en PVE) | Compartido, expuesto vía SMB también |

## Configuración

- **Maproot user = root, maproot group = proxmox** para `proxmox_storage` (Proxmox accede como root con grupo proxmox)
- **Maproot no configurado** para los otros exports (asumir defaults)

## Tamaño del datastore Proxmox

```
192.168.31.91:/mnt/pool0/proxmox_storage
Size: 1.5 TB
Used: 372 GB (25%)
Free: 1.2 TB
Mounted on: /mnt/pve/nfs-storage  (en todos los 5 PVE nodes)
```

## Uso en Proxmox

```bash
# En cada PVE node:
ls /mnt/pve/nfs-storage/
# ├── template/    (templates de VMs)
# ├── iso/        (ISOs)
# ├── snippets/   (cloud-init snippets)
# └── dump/       (backups vzdump)
```

## Puertos NFS

```
tcp  0.0.0.0:2049        nfsd
tcp  0.0.0.0:111         rpcbind
tcp  0.0.0.0:32768+      rpc.mountd (puertos dinámicos)
udp  0.0.0.0:2049
udp  0.0.0.0:111
udp  0.0.0.0:32768+      rpc.mountd
udp  0.0.0.0:34932, 35209  puertos efímeros
udp  0.0.0.0:788, 42256    rpc.statd
```

## Servicios NFS en truenas

| Servicio | Estado |
|---|---|
| nfs | RUNNING |
| rpcbind | RUNNING |
| rpc.mountd | RUNNING |
| rpc.statd | RUNNING |

## Alertas

| # | Severidad | Alerta |
|---|---|---|
| 1 | 🔴 | **Si hades cae → NFS cae → todos los PVE nodes pierden acceso al datastore NFS** — incluyendo templates, ISOs, backups |
| 2 | 🟡 | `proxmox_storage` exportado **sin restricción de red** (cualquier IP puede montar). Para homelab es OK, pero documentar |
| 3 | 🟡 | No hay Kerberos ni NFSv4 con seguridad mejorada |

## Acción inmediata

- Asegurar que `pve_storage` tiene `prune-backups` configurado (ya tiene `keep-all=1` — todos los backups se retienen, ⚠️ llenar disco)

---

## Source files

- `/home/hermes/aranea/topology/nodes/truenas.md`
- `/home/hermes/aranea/topology/services.md`
- `/home/hermes/aranea/topology/discovery/truenas_20260628_211812.txt`

## Captured

2026-06-28 21:18 UTC. Doc generado 2026-06-30.
