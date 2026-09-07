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

# 🔍 Auditoría crítica — anomalías y observaciones topológicas Aranea

## Propósito

Documentación canónica legacy de [[Aranea]]; se conserva el contenido histórico y su estado requiere verificación antes de uso operativo.

## Contenido


## Propósito

Preservar los hallazgos y la provenance de la auditoría topológica de Aranea sin convertirlos en acciones del ticket de backup.

## Contenido

> **Status**: hallazgos. NO son parte del ticket `2026-06-30-013` (que es de backup), pero persisten aquí para visibilidad y eventual remediación futura.
> **Inputs**: snapshot 2026-06-30 19:44 UTC + análisis cruzado de `pve_resources` + `pve_storage` + `disks` por nodo.
> **Criterio**: availability × disposición × redundancy × waste. NO es "qué discos hay libres" sino "qué decisiones de topología no tienen sentido".

---

## 🚨 Anomalías detectadas

### [1] KRONOS — 3 VGs separados en SSDs SATA consumer + WD Green de 1 TB en VM productiva

**Estado actual**:
- sda WD Green SATA SSD 931 GB → `local-sqx-kronos` (vm 111 sqx-ulab-kron-0 **STOPPED**, 128 GB RAM asignados)
- sdb Samsung 870 QVO 931 GB → `local-kronos` (vm 104 stopped, vm 138 kafka-kronos corriendo)
- sdc Crucial P3 954 GB → `pool-kronos` (vm 112 stopped, vm 138 corriendo — **mismo disco, dos VMs**)
- sdd Samsung 870 EVO 232 GB → boot + local-lvm 54 GB
- 2× NVMe Kingston 931 GB → Ceph OSD.1 + OSD.3

**Problemas**:
- WD Green SATA SSD es **consumer grade** (TBW ~80 TB, sin PLP). Para VMs 24/7 es malpractice.
- Samsung QVO usa **QLC NAND** — peor para escritura intensiva.
- `local-sqx-kronos` 70% asignado a vm 111 stopped hace semanas — **despilfarro**.
- vm 138 (kafka-kronos) ocupa espacio en `local-kronos` Y `pool-kronos` simultáneamente (¿disco raw + LVM?).
- 3 VGs separados en 3 SSDs = 3 puntos de fallo independientes.

**Recomendación** (no urgente, baja prioridad):
- Matar vm 111 stopped → liberar 128 GB RAM + 650 GB disco del `local-sqx-kronos`.
- Consolidar kronos storage en UN ZFS mirror o LVM-thin unificado sobre sdb+sdc (no WD Green).
- Mover kafka-kronos (vm 138) a Ceph RBD o al local-lvm unificado.

---

### [2] HERA — vm 123 `sqx-ulab-hera-0` STOPPED con **100 GB RAM asignados** + 931 GB disco desperdiciado

**Estado actual**:
- vmid 123 STOPPED — 100 GB RAM, 50 GB disco, 70 vCPU asignados.
- vmdía 123 es parte del **clúster sqx-ulab**: zeus-0 (vmid 108 corriendo), kron-0 (111 stopped), kron-1 (162 stopped), zeus-1 (170 stopped), hera-0 (123 stopped). Solo zeus-0 corre.
- Disco 931 GB asignado a `local-sqx-hera` VG (WD Green SATA).

**Problemas**:
- **100 GB RAM parada** mientras hades está al 74%.
- 5 instancias sqx-ulab, 4 stopped — cluster sqx-ulab está casi todo apagado.
- VG `local-sqx-hera` 931 GB desperdiciado.

**Recomendación** (vinculado a Fase 2 del design proposal):
- **Confirmar con owner**: ¿sqx-ulab se va a usar? ¿O se puede destruir las 4 stopped (111, 123, 162, 170) y consolidar en zeus-0?
- Si sí → destruir las 4 stopped, liberar ~280 GB RAM + ~2 TB disco entre kronos y hera.
- Si no → al menos destruir 123 (la peor offender) y reusar el disco como destino `zfs recv` desde truenas (Fase 2 del design proposal).

---

### [3] ZEUS — vm 108 sqx-ulab-zeus-0 CORRIENDO en WD Green SATA (consumer)

**Estado actual**:
- vmid 108 sqx-ulab-zeus-0 — running, 70.7 GB RAM, 50+600 GB disco, 28 vCPU.
- Disco en `local-sqx-zeus` 931 GB WD Green SATA SSD (mismo modelo consumer que kronos).

**Problemas**:
- WD Green SATA consumer, sqx-ulab genera mucha escritura.
- 70 GB RAM en un nodo que tiene 94 GB totales (zeus es compute + Ceph OSD.2).

**Recomendación** (baja prioridad):
- Evaluar mover vm 108 a Ceph RBD (pool1) — Ceph ya está al 75%, sumar 600 GB más lo llevaría al 90%+.
- O mover vm 108 a kronos (más RAM: 251 GB).

---

### [4] HADES — concentración extrema de servicios pesados

**Estado actual**:
- 24 VMs/LXCs running + 1 stopped + TrueNAS VM = **25 workloads** en 1 host.
- 187/251 GB RAM usado = **74%**.
- Concentra: truenas VM (32 GB), mt4-real (cuenta producción, 8 GB), 4× mt4 total, postgresql (24 GB), mongodb (24 GB), minio, temporal, flink (32 GB), docker-frigate (12 GB), ubuntu-dev (64 GB), sqx-ulab-hera-0 stopped (100 GB), obsidian-sync CouchDB, etc.

**Problemas**:
- SPOF del SPOF: hades cae = truenas cae = NFS/iSCSI caen = todo el cluster sin storage compartido.
- mt4-real (cuenta producción) corre acá.
- RAM al 74%, agregar cualquier VM más = swap.

**Recomendación** (decisión owner, **NO se migra hades**):
- hades NO debería tener TODOS los servicios pesados.
- Distribución ideal: PG/Mongo/minio/temporal → kronos (251 GB RAM, vacío de storage workloads).
- MT4 (production) → zeus o hera (más RAM libre).
- ubuntu-dev (workstation personal 64 GB) → kronos.
- obsidian-sync → kronos o athena (réplica).
- **Pero el owner decide mantener hades así**.

---

### [5] CEPH — fragmentación crítica + hades weight 0

**Estado actual**:
- 4 OSDs NVMe en zeus, hera, kronos × 2.
- osd.0 (hera) fragmentación 0.84.
- osd.2 (zeus) fragmentación 0.82.
- 3/4 OSDs con slow ops BlueStore.
- 75% pool usage.
- hades weight 0 (no contribuye, pero consume vía RBD mounts).

**Problemas**:
- 75% pool cerca del threshold peligroso (80%+ degrada dramáticamente).
- Si caen 2 nodos OSD simultáneamente → cluster Ceph down.
- hades desperdicia 251 GB RAM y 72 threads desde el punto de vista de Ceph.

**Recomendación** (Fase 0 quick win):
- `ceph tell osd.* compact` mensual.
- hades DEBERÍA contribuir con 1-2 NVMe como OSD — liberar 1 de los NVMe special de truenas, mover special a spare.

---

### [6] TRUENAS — pool0_backup DENTRO de pool2 (mismo host)

**Estado actual**:
- `pool0_backup` es un dataset dentro de `pool2`.
- `pool0_backup/iscsi`, `pool0_backup/home`, etc. se montan en `/mnt/mnt/pool0/`.

**Problemas**:
- **NO es backup, es segunda copia en mismo hardware**.
- Si hades cae → pool0 muere Y pool0_backup muere.
- Peor aún: pool2 es SINGLE DISK HDD.

**Recomendación** (cubierto en design proposal § 4):
- NO usar pool2 como destino de backup.
- Migrar `pool0_backup` a kronos pool1 (cuando exista) o a PBS via vzdump.

---

### [7] TRUENAS — pool2 single HDD 7.3 TB sin mirror

**Estado actual**:
- 1 disco HDD 7.3 TB (guid `56cb3629-acd9-4af0-884c-03f7005551a4`).
- Scrub 11 meses sin hacerse.
- 3.5 TB usado de 7.99 TB raw.

**Problemas**:
- Cualquier falla del HDD = pérdida total de archive.
- Sin parity, sin mirror.
- Scrub obsoleto = bit-rot no detectado.

**Recomendación** (cubierto en design proposal § 4 + Fase 4):
- **No se puede mirror sin comprar HW o romper pool0** (`sdf` ya está en pool0).
- **Aceptar como single disk + scrub mensual + rclone crypt off-host mensual** (mitigación).
- Marcar como "stage, no backup" en la doc.

---

### [8] iSCSI LUNs de truenas montadas en TODOS los nodos (uso incierto)

**Estado actual**:
- athena: 6 LUNs (sda-sdf).
- zeus: 6 LUNs (sdb-sdg).
- hera: 6 LUNs (sdb-sdg).
- kronos: 6 LUNs (sde-sdj).
- hades: 6 LUNs (sdj-sdo).
- Tamaños: 50GB, 200GB×2, 32GB×2, 100GB.

**Problemas**:
- LUNs parecen NO estar en uso activo (wrapper no muestra mounts).
- Ocupan device names y confunden el inventario.
- Si truenas VM cae → hades pierde acceso, todos los nodos también.

**Recomendación** (auditoría adicional necesaria):
- **Auditar uso real de cada LUN en cada nodo** (`mount`, `lsblk`, `pvesm status`).
- LUNs no usados → desmontar y borrar de `/etc/fstab` y `pvesm`.
- LUNs en uso → ver si la app puede moverse a Ceph RBD o NFS.

---

### [9] OBSIDIAN-SYNC (lxc/116 en hades) — SPOF del Second Brain

**Estado actual**:
- CouchDB con todo el vault Obsidian (research + runbooks + agentes).
- 64 GB disco, 2 GB RAM.
- Corre en hades.

**Problemas**:
- Si hades cae → pierdes acceso al Second Brain (no solo tú, también futuros agentes).
- hades 74% RAM = presión.

**Recomendación**:
- Configurar **réplica CouchDB** a otro nodo (kronos o athena) → DR.
- O mover lxc 116 a kronos (más RAM libre).

---

### [10] ubuntu-dev (vm 159 en hades) — workstation con 64 GB RAM

**Estado actual**:
- Workstation personal, 100 GB disco, 64 GB RAM, 24 vCPU.
- Corre en hades (74% RAM usado).

**Problemas**:
- Workstation compite con MT4-real y bases de datos por RAM.
- 64 GB RAM en hades saturado es malpractice cuando hay 251 GB libres en kronos.

**Recomendación**:
- Mover vm 159 a kronos (251 GB RAM libre, 1.7 TB SSD local libre).

---

## Resumen de impacto

| # | Anomalía | Severidad | Acción |
|---|---|---|---|
| 1 | kronos: 3 VGs en SSDs consumer | 🟡 media | Consolidar storage (baja prioridad) |
| 2 | hera: vm 123 stopped con 100 GB RAM | 🔴 alta | Destruir 123 + linked vms stopped (Fase 2 design) |
| 3 | zeus: vm 108 en WD Green | 🟡 media | Evaluar migración |
| 4 | hades: concentración extrema | 🔴 alta | Decisión owner — no se migra |
| 5 | Ceph: fragmentación + hades weight 0 | 🟠 media-alta | `compact` mensual + hades OSD |
| 6 | truenas: pool0_backup en pool2 | 🔴 alta | Migrar off-host (Fase 1+2 design) |
| 7 | truenas: pool2 single disk | 🟠 media-alta | Scrub + rclone off-host (Fase 3+4 design) |
| 8 | iSCSI LUNs: 6× en cada nodo | 🟡 media | Auditar uso real |
| 9 | obsidian-sync: SPOF Second Brain | 🟠 media-alta | Réplica CouchDB |
| 10 | ubuntu-dev: 64 GB en hades | 🟡 media | Mover a kronos |

---

## Relación con ticket 013 (backup design)

Las anomalías **#1, #2, #3, #5, #6, #7, #10** están referenciadas en el [[DESIGN-PROPOSAL]] (en particular § 2 y § 4). El design proposal NO las resuelve todas (foco en backup), pero las menciona como contexto.

Las anomalías **#4, #8, #9** son **fuera de scope** del design de backup — son problemas operacionales separados. Tickets futuros posibles:
- `2026-06-30-018-vm-cleanup` (destruir sqx-ulab stopped, mover ubuntu-dev)
- `2026-06-30-019-ceph-health` (compact + hades OSD)
- `2026-06-30-020-iscsi-audit` (auditar uso real de LUNs)
- `2026-06-30-021-obsidian-sync-replica` (CouchDB DR)

---

**Captured**: 2026-06-30 19:44 UTC (snapshot fresco).
**Authored**: 2026-06-30 por ariadna, tras análisis cruzado de inventario + pve_resources + disks por nodo.
**Status**: hallazgos persistidos para visibilidad. **No son parte del ticket 013**, son observaciones topológicas que viven en este doc separado.
