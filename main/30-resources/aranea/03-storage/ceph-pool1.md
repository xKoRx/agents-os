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

# Ceph pool1 (RBD)

## Propósito

Documentación canónica legacy de [[Aranea]]; se conserva el contenido histórico y su estado requiere verificación antes de uso operativo.

## Contenido


> **Capturado**: 2026-06-28
> **Estado**: ⚠️ HEALTH_WARN — fragmentación alta + slow ops

## Resumen

| Item | Valor |
|---|---|
| **Nombre** | `pool1` |
| **Tipo** | RBD (Rados Block Device) |
| **PGs** | 128 |
| **Replicación** | (default 3 copias — confirmado por `pool1`) |
| **Tamaño lógico** | 1 TB (lo que ve Proxmox como `pool1`) |
| **Tamaño raw cluster** | 3.6 TiB (4 OSDs × 932 GiB) |
| **Uso raw** | 2.1 TiB (57.19%) |
| **Uso del pool** | 708 GiB / 233 GiB max avail = **75.22%** ⚠️ |
| **Objetos** | 193.13k |
| **Estado** | 🟠 **HEALTH_WARN** |

## OSDs activos

```
ID   CLASS  WEIGHT   SIZE     RAW USE  AVAIL    %USE  STATUS  HOST
 0   nvme   0.90970  932 GiB  710 GiB  222 GiB  76.21 up     hera  ⚠️
 1   nvme   0.90970  932 GiB  333 GiB  598 GiB  35.80 up     kronos
 2   nvme   0.90970  932 GiB  710 GiB  222 GiB  76.21 up     zeus   ⚠️
 3   nvme   0.90970  932 GiB  378 GiB  554 GiB  40.54 up     kronos
 -7         0        0 B      0 B      0 B      0     -       hades  (peso 0)
```

| OSD | Host | Disco | Tamaño | Uso | Notas |
|---|---|---|---|---|---|
| **osd.0** | hera | nvme1n1 (CT1000P3SSD8) | 932 GiB | 710 GiB (76%) | ⚠️ Fragmentación BlueStore **0.836025** |
| **osd.1** | kronos | nvme0n1 (KINGSTON SNV3S1000G) | 932 GiB | 333 GiB (35%) | OK |
| **osd.2** | zeus | nvme0n1 (CT1000P3SSD8) | 932 GiB | 710 GiB (76%) | ⚠️ Fragmentación BlueStore **0.817956** |
| **osd.3** | kronos | nvme1n1 (KINGSTON SNV3S1000G) | 932 GiB | 378 GiB (40%) | ⚠️ Slow operations en BlueStore |

## Servicios Ceph

| Servicio | Daemons | Estado |
|---|---|---|
| mon | 3 daemons, quorum hera,zeus,kronos | ✅ activo (age 2w) |
| mgr | zeus (active, since 5w), standbys: kronos | ✅ |
| osd | 4 osds: 4 up, 4 in | ✅ todos up |

> hades NO corre ceph-mon, ceph-mgr ni ceph-osd. Aparece en `ceph_osd_tree` como `host hades weight 0`.

## Alertas HEALTH_WARN

```
[WRN] BLUESTORE_FREE_FRAGMENTATION: 2 OSD(s)
     osd.0 0.836025   (hera)
     osd.2 0.817956   (zeus)
[WRN] BLUESTORE_SLOW_OP_ALERT: 1 OSD(s) experiencing slow operations in BlueStore
     osd.3 observed slow operation indications in BlueStore
```

### Causa probable

- **Fragmentación >0.80**: escrituras intensivas en osd.0/osd.2 sin compactación. Performance degradada para escrituras nuevas.
- **Slow ops osd.3**: problemas de disco o red en kronos para osd.3.

### Acciones recomendadas

```bash
# Identificar el OSD lento
ceph daemon osd.3 perf dump | jq '.osd_op_queue_age_hist'

# Compactar BlueStore (reduce fragmentación)
ceph tell osd.0 compact
ceph tell osd.2 compact

# Verificar SMART del disco NVMe
smartctl -a /dev/nvme1n1    # en hera (osd.0)
smartctl -a /dev/nvme0n1    # en zeus (osd.2)
smartctl -a /dev/nvme1n1    # en kronos (osd.3)
```

## Distribución de capacidad

```
RAW  (3.6 TiB)
├── TOTAL DATA (193.13k objetos) = 708 GiB (lógico) / 2.1 TiB (raw con replicación 3x)
├── .mgr pool (overhead ceph-mgr) = 13 MiB
└── FREE = 1.6 TiB (raw) / 233 GiB (max avail en pool1)

USO EFECTIVO:
- data útil: 708 GiB
- raw usado: 708 GiB × 3 (replicas) + overhead = 2.1 TiB
- ratio: 2.1 / 3.6 = 57% raw / 75% pool
```

## Storages Proxmox servidos desde Ceph

| Storage | Tamaño (en cada nodo) | Uso |
|---|---|---|
| `pool1` (rbd) | ~1 TB (visible en todos) | Datastore principal para VMs (rootdir, images) |

## VMs corriendo en `pool1`

> VMs cuyo `storage` es `pool1` (Ceph RBD). Lista completa vía `pvesm status` — **necesita refresh**.

Aprox. según `pve_resources`:
- 36 VMs running totales, muchas usan `pool1` como datastore principal (ver `qm_list` por nodo)

## Alertas

| # | Severidad | Alerta |
|---|---|---|
| 1 | 🟡 | HEALTH_WARN — fragmentación en osd.0/osd.2 |
| 2 | 🟡 | HEALTH_WARN — slow ops en osd.3 |
| 3 | 🟡 | hades no contribuye (peso 0) |
| 4 | 🟡 | pool al 75% — quedan ~233 GiB antes de ENOSPACE |

## Roadmap

- [ ] `ceph tell osd.0 compact` (reducir fragmentación)
- [ ] `ceph tell osd.2 compact`
- [ ] Investigar slow ops osd.3
- [ ] Considerar agregar OSD NVMe a hades (1 TB) — propuesta `health.md`
- [ ] Política de scrubbing automático

---

## Source files

- `/home/hermes/aranea/topology/health.md`
- `/home/hermes/aranea/topology/discovery/{zeus,hera,kronos,hades,athena}_20260628_211812.txt` (sección `ceph_*`)

## Captured

2026-06-28 21:18 UTC. Doc generado 2026-06-30.
