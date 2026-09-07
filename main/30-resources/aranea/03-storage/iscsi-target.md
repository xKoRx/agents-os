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

# iSCSI Target

## Propósito

Documentación canónica legacy de [[Aranea]]; se conserva el contenido histórico y su estado requiere verificación antes de uso operativo.

## Contenido


> **Capturado**: 2026-06-28
> **Servidor**: truenas (192.168.31.91)
> **Servicio**: iscsi / iscsitarget (RUNNING)

## Target

| Item | Valor |
|---|---|
| **Portal** | `192.168.31.91:3260` |
| **Target IQN-style** | `truenas.aranea.local:truenas` |
| **Nombre Proxmox** | `iscsi-aranea` |
| **Tipo en Proxmox** | iSCSI (plugintype) |
| **Uso** | Shared block storage para VMs (LUNs) |

## Configuración en Proxmox

```bash
# pvesm status (en cualquier nodo)
iscsi-aranea  iscsi  shared  available  truenas.aranea.local:truenas
```

```json
{
  "portal": "192.168.31.91",
  "target": "truenas.aranea.local:truenas",
  "content": "images",
  "shared": 1,
  "storage": "iscsi-aranea",
  "type": "iscsi"
}
```

## LUNs distribuidos

### LUNs vistos por nodo (desde iSCSI initiator)

Cada PVE node ve los mismos LUNs (es shared). Los siguientes dispositivos son LUNs iSCSI:

| LUN serial | Tamaño | Nodos donde aparece |
|---|---|---|
| `e9fef88011c47ac` | 50 GB | athena (sda), zeus (sdb), hera (sdb), kronos (sde), hades (sdj) |
| `e9f0bdbbc475acc` | 200 GB | athena (sdb), zeus (sdc), hera (sdc), kronos (sdf), hades (sdk) |
| `613f83676c06bd5` | 200 GB | athena (sdc), zeus (sdd), hera (sdd), kronos (sdg), hades (sdl) |
| `55adbd546f2b026` | 32 GB | athena (sdd), zeus (sde), hera (sde), kronos (sdh), hades (sdm) |
| `c8868b2391c3591` | 32 GB | athena (sde), zeus (sdf), hera (sdf), kronos (sdi), hades (sdn) |
| `cb14492b0da9fc6` | 100 GB | athena (sdf), zeus (sdg), hera (sdg), kronos (sdj), hades (sdo) |

> Hay **6 LUNs iSCSI** de ~600 GB totales, distribuidos en todos los PVE nodes. No se usan activamente como `storage` (todos los devices aparecen como `raw` o `xfs`/`ext4` con uso local).

## Puerto

```
tcp  0.0.0.0:3260  iscsi-scstd
```

## Servicio en truenas

| Servicio | Estado |
|---|---|
| iscsi (iscsitarget) | RUNNING |

## Initiator en PVE nodes

```
iscsid.service  loaded active running  iSCSI initiator daemon (iscsid)
```

## Uso potencial

- **No está siendo usado activamente** como datastore Proxmox en este momento (el `storage` `iscsi-aranea` está declarado pero los VMs no se crean ahí según `pve_resources`)
- Los LUNs aparecen como dispositivos raw en cada nodo (probablemente usados por hades para los QEMU virtio disks de la VM truenas, o legacy)

## Alertas

| # | Severidad | Alerta |
|---|---|---|
| 1 | 🔴 | **Si hades cae → iSCSI cae** (truenas VM cae → iscsi-truenas cae) → todos los LUNs desaparecen |
| 2 | 🟡 | Los LUNs aparecen como `raw` o con filesystems locales en los PVE nodes — puede ser confuso (¿es local o compartido?) |

## Acción recomendada

- Documentar exactamente qué hace cada LUN (cuales son ZFS volumes de truenas exportados via iSCSI)
- Evaluar si conviene seguir usando iSCSI vs todo NFS+RBD

---

## Source files

- `/home/hermes/aranea/topology/services.md`
- `/home/hermes/aranea/topology/discovery/{athena,zeus,hera,kronos,hades,truenas}_20260628_211812.txt`

## Captured

2026-06-28 21:18 UTC. Doc generado 2026-06-30.
