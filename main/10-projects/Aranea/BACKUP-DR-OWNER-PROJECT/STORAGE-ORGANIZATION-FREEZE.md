---
title: "STORAGE-ORGANIZATION-FREEZE — Gate antes de Backup/DR (2026-09-21)"
type: doc
schema_version: 1
status: active
icon: 🧭
slug: storage-organization-freeze
area: "[[Aranea]]"
project: "[[BACKUP-DR-OWNER-PROJECT]]"
created: "2026-09-21"
updated: "2026-09-21"
aliases:
  - STORAGE-ORGANIZATION-FREEZE
  - Gate STORAGE_ORGANIZATION_COMPLETE
  - Placement Freeze Backup DR
tags:
  - kind/doc
  - area/aranea
  - domain/backup-dr
  - project/backup-dr
related:
  - "[[MASTER-PLAN-STORAGE-BACKUP-DR]]"
  - "[[PLACEMENT-DECISIONS-20260920]]"
  - "[[CAPACITY-AND-RESERVATIONS]]"
  - "[[POOL0-TO-POOL2-REPLICATION-SPEC]]"
  - "[[TWO-LAYER-BACKUP-SPEC]]"
  - "[[MANDATO-MIGRACIONES-SPEC]]"
---

# 🧭 STORAGE-ORGANIZATION-FREEZE — Gate antes de Backup/DR

## Propósito

- Registrar el gate **`STORAGE_ORGANIZATION_COMPLETE`** (mandato owner "Storage Organization & Placement Freeze", 21sep; **depurado por mandato correctivo 21sep noche-5 — BACKUP FIRST**): la organización de recursos queda congelada y verificada como CIERRE de la fase de optimización de storage. **NO es requisito de Backup/DR** — esa dependencia fue REVOCADA por el owner: la implementación y certificación de Backup/DR avanzan sobre el placement actual, las migraciones van DESPUÉS protegidas por backups verificados, y cada servicio migrado se recertifica.
- Los backups certificados que ya funcionan NO se detienen. La implementación de jobs nuevos y de la réplica pool0→pool2 avanza por sus PROPIOS gates específicos (G-B1=D+018+019, G-NFSVM, G-REP-0..5) — este gate no los bloquea.

## Criterios del gate (todos obligatorios)

1. **Placement definitivo documentado** → [[PLACEMENT-DECISIONS-20260920]] §F (v2, congelado; MIGRATE = ninguna activa).
2. **Migraciones imprescindibles terminadas o explícitamente diferidas** → veredicto del viernes 25sep = `MIGRATIONS_NOT_READY` por diseño: ninguna migración es imprescindible para corregir una condición peligrosa; W5 queda reevaluación por VM post-activación de la réplica (§3). Diferimiento explícito ≠ deuda silenciosa. **Criterio de desbloqueo por migración (noche-5): cada migración futura exige `BACKUP_BASELINE_VERIFIED` de su unidad — nunca este gate.**
3. **Capacidad y reservas verificadas** → [[CAPACITY-AND-RESERVATIONS]] (presupuesto por backend sin doble-asignación; re-medición en preflight de cada gate).
4. **Ausencia de discos con propietario desconocido dentro del alcance** →UNKNOWN vigentes (kafka scsi1 ×3, argus scsi1-4, interior MT4, CouchDB) están FUERA del alcance de organización: pertenecen a 018/decisión owner y NO alteran placement de discos productivos. El gate exige "sin propietarios desconocidos dentro del alcance definido", no 0 UNKNOWN globales.
5. **Servicios validados en sus destinos** → no hay migraciones ejecutadas: todo servicio sigue en su ubicación ya validada por operación (KEEP). Sin movimiento = sin revalidación pendiente.
6. **Volúmenes antiguos conservados según política aprobada** → F-09 (legacy pool2/pool0_backup intactos), sin borrados de datasets legacy ni RBD huérfanas (WP-S1 gated dueño).
7. **Dependencias y recovery paths documentados** → Master Plan D5/D6 + SPEC réplica §6 + TWO-LAYER §1 (rutas de restore).
8. **Matriz de 59 guests reconciliada** → [[MATRIZ-59-GUESTS-BACKUP]] 59/59 (drifts 125/132 corregidos; regularización formal en 018).
9. **Sin cambios pendientes que alteren materialmente el volumen de pool0 a replicar** → tras activar réplica + capa vm-backup el árbol vivo crece respecto del envío inicial 2,35T: la retención final @repl (7 vs 14d) y el presupuesto de pool2 se fijan midiendo `pool0/vm-backup` real tras su primer ciclo (orden recomendado de la SPEC §2). Condición: decisiones owner abiertas que cambien datasets pool0 (trading_systems inclusiones, limpieza legacy, frigate RC) resueltas o explícitamente diferidas antes de G-REP-4.

## 2. Qué habilita al cumplirse

- Fijar capacidad y retención definitivas de Backup/DR (decisión D extendida: B1 + G-NFSVM + @repl).
- Ejecución de jobs nuevos (MANDATO-BACKUP-VMS/DATOS) y de la réplica (G-REP-3/4).
- La preparación documental (mandatos, diffs, runbooks, fixtures planificados) sigue en paralelo desde ya.

## 3. Migraciones: imprescindibles vs diferidas (veredicto 21sep)

| Clase del mandato | Resultado |
|---|---|
| Imprescindibles (condición peligrosa) | **NINGUNA.** Edge correcto en nfs-storage (pool0, file-backend válido); SOs productivos KEEP_JUSTIFIED (D1: dato T0 fuera de Ceph); pool1 en banda estable 85,2-87,9% con condición de alerta K2 preparada (no disparada); hades concentración = SPOF aceptado F-13 |
| Que alivian Ceph | W5 down-tier: NO como bloque de ventana; reevaluación POR VM post-activación réplica (nunca simultánea con fulls); orden potencial echo→MT4→DB-SOs, gate por VM |
| Mejoran placement | W4 kafka 128→athena: sólo con causalidad demostrada del brote (P1-4 RO primero) |
| Opcionales | W3 pi-hole: decisión de función D5 (reactivar+proteger vs retiro), no migración; sin base "sobrevivir a hades" (149 corre en athena) |
| Descartadas | W1/W2→pool2, alta nfs-pool2, P0-2, 2º target PBS→pool2 (D-NEW-01) |

**Viernes 25sep**: `MIGRATIONS_NOT_READY` = ninguna ficha con preparación completa para el sábado; la ventana no se llena con operaciones sin justificación. Sábado 26sep: prechecks → K2 → K1 (si GO) → P0-1 (W-01, gates D1+P1-1+019).

## 4. Correcciones documentales aplicadas (mandatos que permitían lo cancelado)

- [[MANDATO-MIGRACIONES-SPEC]]: errata "Alcance tras D-NEW (revisión noche-3)" — la columna de W1/W2 quedaba en pasado contradictorio; corregida: alto nfs-pool2 CANCELADO + alta `nfs-pool2` OBSOLETA.
- [[FIRST-MAINTENANCE-WINDOW-20260920]]: §8.2 ya reflejaba la redirección (kafka DESCARTADO); sin doble w4.
- [[ROADMAP-WP-BACKUP-DR]] §Redirección y [[PLACEMENT-DECISIONS-20260920]] §D: vigentes sin cambios.

## 5. Tabla única de decisiones owner pendientes

Vive en `~/aranea/work/continuity-20260923/TABLA-APROBACION-23SEP.md` (no se duplica): urgentes **P1 (PBS growth W-01) · P4 (D-piloto criterio alternativo) · P6 (paquete réplica G-REP-0..5)**; T=018/020/021; P2=T-21b+W-02; P3 sin objeto (aceptación de cancelación); P5=pi-hole D5. Regla: **una aprobación general NO sustituye gates específicos**.

## Fuentes

- Mandato owner "Storage Organization & Placement Freeze · Antes de iniciar Backup/DR" (21sep).
- [[MASTER-PLAN-STORAGE-BACKUP-DR]] §7 (D-NEW-01..06) · [[POOL0-TO-POOL2-REPLICATION-SPEC]] (CAPACITY_GO, gates G-REP-0..5) · [[TWO-LAYER-BACKUP-SPEC]] · [[MANDATOS-MIERCOLES-23SEP]].
