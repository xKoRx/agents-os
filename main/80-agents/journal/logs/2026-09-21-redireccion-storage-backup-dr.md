# Change log — 2026-09-21 (noche-2): Redirección owner D-NEW-01..06 + SPEC freeze

**Mandato**: "Storage Architecture + Backup/DR · Rediseño dirigido y SPEC Freeze" (ONE-SHOT; NO implementar). **Ejecutor**: Ariadna. **Tipo**: documental + sondas RO. **Cero mutaciones de infraestructura** (Echo operando durante toda la sesión).

## Decisiones owner registradas (autoridad nueva)
D-NEW-01 pool2 = réplica diaria de TODO pool0, exclusivo (W1/W2→pool2 CANCELADAS, sin alta nfs-pool2, P0-2 retirado) · D-NEW-02 pool0 = datos + snapshots + respaldos recuperables de pool1 · D-NEW-03 pool1 por workload con NO_GO vigente · D-NEW-04 dos mecanismos no intercambiables · D-NEW-05 cloud priorizado, 3-2-1 NO declarado sin A7 · D-NEW-06 backups sin Hermes. F-01..F-14 intactos (sin conflicto material; F-14/F-09 se respetan en las SPECs).

## Archivos creados (10-projects/Aranea/BACKUP-DR-OWNER-PROJECT/)
- POOL0-TO-POOL2-REPLICATION-SPEC.md (E2: inventario 2,57T, capacidad 4,08T zpool, 04:45 incremental diario, consistencia, vida HDD, recuperación, gates G-REP-1..4)
- TWO-LAYER-BACKUP-SPEC.md (E3: mecanismo A vzdump/PBS + exclusión ledger + capa nfs-vmbackup pool1→pool0; mecanismo B matriz por servicio; MinIO última copia verificable)
- MANDATO-PREP-SPEC.md · MANDATO-BACKUP-VMS-SPEC.md · MANDATO-BACKUP-DATOS-SPEC.md · MANDATO-REPLICACION-SPEC.md · MANDATO-MIGRACIONES-SPEC.md · MANDATO-CERTIFICACION-SPEC.md (E6: seis mandatos)

## Archivos actualizados
- MASTER-PLAN-STORAGE-BACKUP-DR.md — §7 Redirección owner + erratas de capacidad (E1)
- PLACEMENT-DECISIONS-20260920.md — §D: cancelaciones W1/W2/nfs-pool2/2º-target, recolocación W3/W4/W5 (E4)
- ROADMAP-WP-BACKUP-DR.md — §Redirección: A6 reemplazado por SPEC, B1 ampliado, P0-2 retirado, orden actualizado (E5)
- ARANEA-CONTINUIDAD-Y-VENTANA-25-26-SEP.md — delta noche-2 al inicio (E7)
- 30-resources/aranea/03-storage/zfs-replication-runbook.md — NUEVO runbook evergreen (E8)
- 30-resources/aranea/03-storage/BACKUP-DR-RUNBOOK.md — delta §0 con enlace

## Evidencia nueva (sondas RO 21sep noche, sin mutaciones)
TrueNAS 25.04.1 (API v2.0 + SSH ariadna@truenas): pool0 ONLINE mirror×3 scrub OK 6sep 0 errores, used 2,59T (aranea_storage 1,09T, trading_systems 485G, proxmox_storage 417G, iscsi 539G, apps 67G, resto 26G); pool2 7,27T/alloc 3,19T/**free zpool 4,08T** (vista zfs list 2,15T subestima; sin quotas; "4,18T" del freeze corregido a 4,08T); pool2 SIN scrub desde 12jul2025 (0 errores ese día) y sin tarea programada (única tarea id=3 → pool0); 606 snapshots (156 pool0 jul-2025/residuales, 442 pool2 legacy); 0 periodic-snapshot tasks; 0 cron jobs; /replication y /pool/periodic-snapshot/task = 404; NFS exports ids 15-18 con hosts=[*] (endurecimiento = deuda previa del carril storage, NO tocada); PVE storage.cfg leído vía ariadna@pve (sin edición).

## Pendientes que este cambio NO ejecuta (gated)
G-REP-1..4 (réplica), G-B1/G-NFSVM (VMs), G-A7 (020/021), G-A3/G-A4/G-T21B/D2 — ver SPECs y TABLA-APROBACION. La ventana 26sep queda reducida a K2/K1/P0-1 según sus gates.
