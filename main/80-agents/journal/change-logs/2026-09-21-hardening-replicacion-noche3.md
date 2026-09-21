# Change log — 2026-09-21 — Storage Organization & Placement Freeze (noche-4)

- **Hora**: 21sep 2026, sesión nocturna (post noche-3). **Mandato**: "Storage Organization & Placement Freeze · Antes de iniciar Backup/DR" (ONE-SHOT; NO iniciar backups/replicaciones/migraciones).
- **Alcance**: documental. Cero mutaciones de infraestructura; Echo operando; R2/timers intactos; tickets 018-021 intactos; F-01..F-14 intactos.
- **Escrituras** (proyecto `10-projects/Aranea/BACKUP-DR-OWNER-PROJECT/`):
  - `STORAGE-ORGANIZATION-FREEZE.md` — NUEVO (E6): gate `STORAGE_ORGANIZATION_COMPLETE` con 9 criterios, veredicto de migraciones (ninguna imprescindible; MIGRATIONS_NOT_READY el viernes), correcciones a mandatos, puntero a TABLA-APROBACION-23SEP.
  - `PLACEMENT-DECISIONS-20260920.md` — sección **§F PLACEMENT-FREEZE-V2** (E2): clasificación final por workload con clasificación de discos (SO reconstruible vs datos críticos como unidades distintas), tabla de migraciones vacía de activas, reglas binding; autoridad sobre A-E donde contradiga.
  - `CAPACITY-AND-RESERVATIONS.md` — NUEVO (E3): presupuesto pool2/pool0/pool1/PBS/local-lvm con reservas obligatorias y sin doble-asignación (auto-corrección adversarial: W5 no estaba asignado; errata dejada como registro).
  - `FIRST-MAINTENANCE-WINDOW-20260920.md` — **§8.2** plan de ejecución consolidado (E4): DAG, viernes (preflight + MIGRATIONS_NOT_READY + cierre Echo), sábado (K2→K1→P0-1, sin P0-2), réplica-full en ventana exclusiva G-REP-3, reglas de no-solape I/O TrueNAS.
  - `MANDATO-MIGRACIONES-SPEC.md` — errata: fila W1/W2 estaba en imperativo ("reubicar", "alta nfs-pool2") contradiciendo su estado CANCELADAS → corregida a NINGUNA/OBSOLETA.
  - `BACKUP-DR-OWNER-PROJECT.md` — status_detail actualizado (ronda freeze), bitácora con delta noche-4, tarea **T-23a DONE** añadida.
  - `ARANEA-CONTINUIDAD-Y-VENTANA-25-26-SEP.md` — delta noche-4 (E1-E8) como bloque superior.
  - `ROADMAP-WP-BACKUP-DR.md` — clasificación MANDATO 1: doc de preparación + tarea 2 reclasificada como runbook de ejecución (G-NFSVM).
- **Verificación**: números tomados de las SPECs congeladas (2,35T refer / 4,08T pool2 / 1,64T pool0 / banda Ceph 85,2-87,9% / VG 267,5G vs pool-kronos 733,87G / hades 33,4G); sin re-mediciones nuevas (mandato lo prohíbe implícitamente al reutilizar la evidencia del 21-09; re-medición = preflights).
- **No ejecutado (por diseño)**: backups, réplica, scrub, migraciones, borrados, K1.
- **Pendiente owner** (tabla única): P1/P4/P6 urgentes · T=018/020/021 · P2/P3/P5.
