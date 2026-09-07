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

# TrueNAS pool2 (bulk storage) ⚠️

## Propósito

Documentación canónica legacy de [[Aranea]]; se conserva el contenido histórico y su estado requiere verificación antes de uso operativo.

## Contenido


> **Capturado**: 2026-06-28
> **Estado**: 🔴 **Sin redundancia + scrub obsoleto**

## Alertas críticas

| # | Severidad | Alerta |
|---|---|---|
| 1 | 🔴 | **Disco único `sdg1` (7.3 TB)** — sin mirror, sin redundancia |
| 2 | 🟠 | **Scrub de hace 11 meses** (2025-07-12) — bit-rot no detectado |
| 3 | 🟠 | Contiene **backups de trading_systems (305 GB), aranea_storage (39 GB), iso_storage (15 GB)** — todo en un solo disco |

## Resumen

| Item | Valor |
|---|---|
| **Pool** | `pool2` |
| **Topología** | 1 disco simple (NO mirror) |
| **Raw total** | 7.99 TB |
| **Usado** | 3.5 TB |
| **Libre** | 4.5 TB |
| **% uso** | 44% |
| **Autotrim** | OFF (default) |
| **Último scrub** | **2025-07-12 (hace 11 meses — fuera de ventana)** ⚠️ |

## Disco

| Item | Detalle |
|---|---|
| **Path** | `/dev/disk/by-partuuid/56cb3629-acd9-4af0-884c-03f7005551a4` |
| **Device** | `sdg1` (partición) |
| **Disco físico** | `sdg` (en hades) |
| **Modelo** | ST8000DM004-2U9188 (Seagate Barracuda 8 TB HDD) |
| **Tamaño** | 7.99 TB |
| **Serial** | ZR15Y75T |
| **Read errors** | 0 |
| **Write errors** | 0 |
| **Checksum errors** | 0 |
| **Fragmentación** | 0% |

## Datasets en pool2

| Dataset | Usado | Función |
|---|---|---|
| `pool0_backup` | ❓ | **Mirror lógico de pool0** (snapshots ZFS) |
| `zfs_backup` | ❓ | Snapshots ZFS |
| `backup/trading_systems` | 305 GB | Backup datos MT4 |
| `backup/aranea_storage` | 39 GB | Backup storage general |
| `backup/iso_storage` | 15 GB | ISOs |
| `backup/portainer` | 995 MB | Portainer data |
| `ix-apps` | ❓ | Apps TrueNAS nativas |

## Lo que se pierde si `sdg` falla

- 305 GB de `trading_systems` backup
- 39 GB de `aranea_storage` backup
- 15 GB de `iso_storage`
- todo el `pool0_backup/` (mirror lógico de pool0)
- todo el `zfs_backup/`

> Si este disco falla, **se pierde el backup de la mayor parte del cluster**. Lo peor del riesgo: el backup está en el mismo host físico (hades) que los datos originales.

## Acción inmediata

```bash
# Ejecutar scrub manual para validar integridad AHORA
ssh agent_ro@192.168.31.91 "zpool scrub pool2"
```

## Roadmap

- [ ] **URGENTE**: scrub manual de pool2 (validar integridad)
- [ ] Migrar pool2 a mirror vdev cuando se agreguen más discos (Task 2 debería proponerlo)
- [ ] Mover backups críticos a otro host (off-host) — **Task 2**
- [ ] Configurar scrub mensual automático
- [ ] Monitoreo SMART continuo

---

## Source files

- `/home/hermes/aranea/topology/nodes/truenas.md`
- `/home/hermes/aranea/topology/health.md` §4
- `/home/hermes/aranea/topology/discovery/truenas_20260628_211812.txt`

## Captured

2026-06-28 21:18 UTC. Doc generado 2026-06-30.
