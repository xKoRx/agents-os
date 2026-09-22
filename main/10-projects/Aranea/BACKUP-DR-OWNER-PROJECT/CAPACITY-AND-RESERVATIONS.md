---
title: "CAPACITY-AND-RESERVATIONS — Presupuesto por backend (medido 21sep 2026)"
type: doc
schema_version: 1
status: active
icon: 📊
slug: capacity-and-reservations
area: "[[Aranea]]"
project: "[[BACKUP-DR-OWNER-PROJECT]]"
created: "2026-09-21"
updated: "2026-09-22"
aliases:
  - CAPACITY-AND-RESERVATIONS
  - Presupuesto capacidad backend Aranea
tags:
  - kind/doc
  - area/aranea
  - domain/backup-dr
  - project/backup-dr
related:
  - "[[POOL0-TO-POOL2-REPLICATION-SPEC]]"
  - "[[TWO-LAYER-BACKUP-SPEC]]"
  - "[[STORAGE-ORGANIZATION-FREEZE]]"
  - "[[MASTER-PLAN-STORAGE-BACKUP-DR]]"
---

# 📊 CAPACITY-AND-RESERVATIONS — Presupuesto por backend (21sep 2026)

## Propósito

- Presupuesto de capacidad y reservas futuras por backend, con las mediciones vigentes (no cifras refutadas). **Regla del proyecto: re-medir en el preflight de cada gate** — esta nota congela la lógica del presupuesto; los números se re-validan al ejecutar (CAPACITY-FREEZE v2 con serie 7d la actualizará).
- Principio anti-doble-asignación: el mismo espacio libre no se asigna a dos funciones. Cada reserva aparece una sola vez; las funciones se apilan sobre el mismo libre.

## Contenido

## 1. pool2 (TrueNAS, HDD single-disk, size 7,27T)

| Concepto | Valor | Fuente/estado |
|---|---|---|
| Total zpool | 7,27T | `zpool list` 21sep 18:23 -03 |
| Usado (alloc) | 3,19T | ídem |
| **Libre real (zpool)** | **4,08T** | el número operativo; la vista `zfs list` AVAIL (2,15T) subestima 2,05T por histéresis `usedbychildren` de 442 snapshots legacy (`pool2/backup`) — convergerá a ~4,2T si el owner los limpia (decisión separada, F-09) |
| Reserva: legacy F-09 | 0 nueva (preservado tal cual) | `pool2/backup`, `pool2/pool0_backup`, `pool2/zfs_backup` intocables |
| Reserva: 1ª réplica pool0→pool2 | +2,35T (base `refer`; presupuesto 2,4T) | [[POOL0-TO-POOL2-REPLICATION-SPEC]] §1 — GATED G-REP-3 |
| Reserva: retención destino @repl-* | 0 en steady-state (la retención manda el snapshottask en ORIGEN; destino = último snapshot + policy (i)/(ii)/(iii) a probar en G-REP-0) | SPEC §3bis |
| Reserva: crecimiento diario | ≤50G/d presupuestado (UNKNOWN real → serie 7d antes de G-REP-4) | SPEC §2 |
| **Margen post-full (peor caso 100% árbol)** | **≥1,71T (24%)** | CAPACITY_GO certificado por aritmética |
| Steady-state proyectado (retención 14d, 50G/d) | ~1,0-1,4T libres | freno duro: free <1,00T → NO-SEND + alerta; aviso <1,50T (se mide sobre `zpool list`) |

**Post-vm-backup (pendiente de medir)**: cuando `pool0/vm-backup` (capa pool1→pool0) reciba sus snapshots, la réplica de TODO pool0 los incluye → el envío base deja de ser 2,35T. Orden recomendado (ya en SPEC §2): medir vm-backup real tras su primer ciclo → fijar retención final @repl (7 vs 14d). NO cerrar 7/14d sin esa estimación.

## 2. pool0 (TrueNAS mirror, 4,08T size)

| Concepto | Valor | Estado |
|---|---|---|
| Usado lógico (árbol vivo) | 2,59T (aranea_storage 1,11T + proxmox_storage 417G + trading_systems 485G + iscsi 539G + apps 14,1G refer + ix-applications 10,1G + varios) | SPEC §1 (medido 21sep) |
| **Libre real (zpool)** | **1,64T** | auditoría noche-3 (la vista dataset 945G subestima por histéresis) |
| Reserva: crecimiento operativo | Δ diario ≤50G/d presupuestado (medir) | compartido con proyección pool2 |
| Reserva: capa `vm-backup` (pool1→pool0) | ≈0,43-1,03T según compresión real (T0 vzdump semanal keep-weekly=4) | [[TWO-LAYER-BACKUP-SPEC]] §1 — GATED G-NFSVM; dataset nuevo `pool0/vm-backup`, storage `nfs-vmbackup`; `nfs-storage` INTOCADO |
| Reserva: snapshots `@repl-*` 14d (retención en origen) | ≈0,27-1,09T según delta diario | SPEC §2 |
| **Peor caso combinado** | deja ~0,12T en pool0 → **CABE pero margen ACOTADO** | orden de activación: medir vm-backup real antes de fijar retención final |
| Reserva: no asignadas | limpieza legacy / zvols win 606G = decisiones owner separadas (WP-S1, D-W3), NO cuentan como espacio disponible | F-09 / 018 |

## 3. pool1 (Ceph RBD, 4 OSD × 932GiB, réplica ×3)

| Concepto | Valor | Estado |
|---|---|---|
| Uso osd.0/osd.2 (los llenos) | banda 85,19-87,90%; lecturas 21sep: 08:05 85,19/85,17 → 17:31 85,59/85,59 → 22:39 86,56/86,60 (noche-6, aceleración vespertino ≈1,8G/OSD/h en sesión US; margen a backfillfull ≈31,7G/OSD ≈ 18-80h según ritmo) | HEALTH_WARN persistente (nearfull ×2 + slow ops BlueStore); NO_GO estructural (CRUSH host + 1 OSD/host probados 19sep) |
| Ratios efectivos | nearfull 0,85 · backfillfull 0,90 · full 0,95 | verificados en osd dump 20sep |
| Márgenes a backfillfull/full | ≈21,8G / ≈68G por OSD lleno | K2-CEPH-RISK |
| Reservas | **NINGUNA asignación nueva** (D-NEW-03: sin discos nuevos ni migraciones hacia pool1) | condición de alerta K2: ≥89% ×2 lecturas ≥1h → acción gated `qm shutdown 125` |
| Liberaciones futuras (no contabilizadas) | RBD huérfana vm-112-disk-0 (5,9G usados reales, no 120G — errata noche-6) + W5 por VM (~64G+) | carril Ceph/Storage S1, gate dueño por VMID; W5 = reevaluación por VM post-réplica — [Corrección 21sep] 162/170 YA liberadas por el owner (20sep 23:58); 112 = única liberación pendiente (alivio marginal) |

## 4. PBS (VM 180, kronos; datastore `main` 295G)

| Concepto | Valor | Estado |
|---|---|---|
| Uso actual | 48G/295G (18%); 14.796 chunks (+253/32h, tendencia baja); verify TASK OK | CAPACITY-FREEZE 21sep |
| Umbral de operación | 70% (207G) | D3 master plan |
| Reserva: crecimiento | **+250G in-place (P1-v3, errata 22sep): `lvextend` de `local-kronos/vm-180-disk-1` + `resize2fs` online → ≈545G. ERRATA: la "opción recomendada" previa (2º disco VG `pool-kronos`) quedó SUPERSEDED** — era incoherente (el datastore del guest es ext4 crudo sin VG) y violaba F-06 ("PBS datastore = local-kronos", FROZEN); runbook `cierre-preparatorio-20260921/P1-GROW-IN-PLACE.md`. Trade: local-kronos VFree 267,51G → 17,51G | P1-GROW-IN-PLACE (verificado live 22sep: scsi1 serial pbs-data, ext4 crudo, sin thin pool en el VG) |
| Con +250G | ≈545G total (delta -50G vs el presupuesto 595G anterior: la validación del footprint real T0a-d ocurre en D-piloto; si lo excede, gate de crecimiento adicional propio) | post-P0-1/D |

## 5. local-lvm por nodo (destinos W5 / restauraciones)

| Nodo | Libre | Rol |
|---|---|---|
| hades | **≈20,5G libres** (ERRATA noche-6: el 33,4G del freeze era el USADO del thinpool — 53,93G al 61,96%, medido live 21sep 22:4x) | NO destino de la propuesta W5 original (<64G); regla corregida: VM ≤12G dejando ≥8G libres |
| zeus | 77,5G | destino válido W5 por VM |
| hera | 91,7G | destino válido W5 por VM |
| athena | (medir en preflight) | nodo de menor densidad; destino W4 sólo con causalidad |
| kronos | VG local-kronos 267,5G / pool-kronos 733,9G | PBS + labs |

**Corrección adversarial aplicada**: la tabla original de esta nota presentaba "nuevas asignaciones W5" como asignadas; ningún destino está asignado todavía (W5 = reevaluación por VM, gate por VM). Los mismos GB libres NO se reservan simultáneamente como destino W5 y como margen de restauración — prioridad de uso: restauración > W5.

## 7. Presupuestos por fase (mandato BACKUP FIRST 21sep noche-5)

Fases independientes; **cada fase se presupuesta con espacio REAL medido a su inicio — nunca con espacio que otra fase todavía no ha liberado.**

**Fase 0 — Baseline (backups de la infraestructura ACTUAL):**
- pool0: used 2,59T + libre zpool 1,64T (hoy). Réplica 2,35T NO va a pool0 (va a pool2) — pool0 sólo agrega `@repl-*` (0,27-1,09T) y la capa `vm-backup` (0,43-1,03T) cuando sus gates activen: **peor caso combinado deja ~0,12T** → orden obligatorio: activar `vm-backup` (G-NFSVM) → medir su consumo real → recién entonces fijar retención @repl final (7 vs 14d).
- pool2: 4,08T libres − 2,4T réplica (presupuesto) = **≥1,71T margen post-full (24%)**. No compite con ninguna otra función (RESERVADO réplica).
- PBS: 295G (18%) → +300G (W-01 opción b, pool-kronos 733,87G) = 595G → cabe T0a-d + dumps + staging con retención 7d/4w. Umbral 70%.
- **BACKUP_BASELINE_VERIFIED es alcanzable COMPLETO sin ejecutar ninguna migración** (esta es la corrección de fondo: los presupuestos de baseline no dependen de ahorros futuros).

**Fase 1 — Después de vm-backup (medición sobre pool0):**
- `pool0/vm-backup` real = medir tras su primer ciclo (TWO-LAYER §1). Si vm-backup real > 1,03T: recortar retención @repl a 7d ANTES de activarla (no después), manteniendo los frenos vigentes (NO-SEND si pool2 <1,00T; pool0 con umbral de alerta).
- Números de esta fila se congelan en CAPACITY-FREEZE v2 con la medición.

**Fase 2 — Después de migraciones (capacidad final de pool1):**
- pool1 recupera SOLO el `used` real liberado (thin), no el prov: rango realista 150-350G lógicos totales (techo nominal 1363G prov en [[ANALISIS-DISCO-POR-DISCO]] §2/§5) — ver aritmética en esa nota.
- Regla: el ahorro se CONTABILIZA al verificar `rbd du` post-liberación, nunca antes; la liberación de cada disco exige BACKUP_BASELINE_VERIFIED + gate de borrado independiente.

## 8. Reglas transversales

1. No resolver falta de capacidad borrando datasets legacy sin autorización (F-09; limpieza pool2 = decisión owner separada — liberaría ~2T de vista y haría converger AVAIL a ~4,2T).
2. No borrar imágenes RBD "huérfanas" sin demostrar ownership y ausencia de uso (WP-S1: identificación por VMID + evidencia + autorización independiente).
3. Umbrales de freno: pool2 free <1,00T = NO-SEND + alerta; PBS >70% = revisión; Ceph ≥89% ×2 lecturas = condición K2.
4. Todos los números de esta nota = 21sep 2026; la CAPACITY-FREEZE v2 (serie 7d + preflights) los reemplaza con datos frescos.

## Fuentes

- [[POOL0-TO-POOL2-REPLICATION-SPEC]] §1-2 (mediciones + aritmética noche-3) · [[TWO-LAYER-BACKUP-SPEC]] §1 · [[K2-CEPH-RISK-20260920]] · `~/aranea/work/continuity-20260922/CAPACITY-FREEZE.md` · `~/aranea/work/continuity-20260923/W-01-PBS-GROWTH.md` · [[MASTER-PLAN-STORAGE-BACKUP-DR]] D3/D3.1.
