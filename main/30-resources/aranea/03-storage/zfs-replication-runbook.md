# Runbook — Replicación ZFS diaria pool0 → pool2 (Aranea)

> Runbook evergreen (mecánica operativa). La arquitectura y decisiones viven en el proyecto: `10-projects/Aranea/BACKUP-DR-OWNER-PROJECT/POOL0-TO-POOL2-REPLICATION-SPEC.md`. Autoridad de activación: gates G-REP-1..4 del owner. Última verificación de números: 2026-09-21 (API TrueNAS 25.04.1 + SSH ariadna@truenas).

## Contexto fijo

- pool0 = mirror ×3, 4,08T, datos productivos. pool2 = HDD single-disk 7,27T, función ÚNICA: réplica diaria de pool0 (decisión D-NEW-01; sin VMs/rootfs/apps/backups de VM).
- pool2 free operativo = **zpool free** (`zpool list`), NO el AVAIL de `zfs list` (subestima por snapshots legacy compartidos). Umbral NO-SEND: < 1,00T; aviso: < 1,50T.
- Destino: dataset `pool2/pool0-replica` (árboles legacy pool2/backup, pool2/pool0_backup, pool2/zfs_backup INTOCABLES — F-09).
- Ejecución en TrueNAS (cron interno + script zfs); JAMÁS dependiente de Hermes/agentes (D-NEW-06).

## Procedimiento diario (incremental; 04:45 -03)

1. `flock` del script (una sola sesión).
2. Snapshot: `zfs snapshot -r pool0@repl-$(date +%Y%m%d)`.
3. Derivar `<prev>` = último @repl-* presente en ORIGEN y DESTINO (`zfs list -t snapshot` ambos lados; nunca asumir ayer).
4. Si `<prev>` tiene >7 días → FAIL CERRADO + alerta (no re-enviar full automático).
5. Chequeo `zpool list pool2` → free < 1,00T = NO-SEND + alerta.
6. `zfs send -R -I pool0@repl-<prev> pool0@repl-<hoy> | zfs recv -F pool2/pool0-replica` → log + exit code.
7. Verificación: exit=0 + snapshot del día visible en destino; semanal: comparación de tamaños por dataset.

## Primera réplica (full; ventana propia gated G-REP-3)

Pre: scrub pool2 con 0 errores (G-REP-1) · presupuesto I/O exclusivo (sin vzdump fulls/G1B/migraciones ese día; Echo cerrado) · `zfs send -R pool0@repl-<hoy> | zfs recv -F pool2/pool0-replica` · monitoreo 60 min (tasa, free, errores) · duración esperada 8-12h (~2,57T a HDD).

## Snapshots y retención

- Origen: 14 × @repl-* (14 días); snapshots legacy 2025 = intocables (limpieza = decisión owner separada).
- Destino: 7-14 días en `pool2/pool0-replica`.
- Destruir snapshots/datasets = autorización independiente e irreversible; nunca en la misma operación que otra cosa.

## Recuperación (resumen; detalle en la SPEC §6)

| Escenario | Acción |
|---|---|
| Archivo borrado | clonar `pool2/pool0-replica/<ds>@repl-<d>` → montar RO → copiar a ruta nueva (jamás sobrescribir origen) |
| Dataset dañado | comparar origen vs réplica → rollback a snapshot (con backup previo del estado) o clonar réplica como nuevo dataset |
| Zvol corrupto | clonar zvol de la réplica → attach como disco NUEVO a la VM → validar → conmutar |
| Pérdida pool0 | reconstruir desde `pool0-replica` + dumps PBS (consistencia app manda para PG/Mongo/MinIO) |
| Pérdida chasis TrueNAS | **pool2 NO ayuda** (mismo chasis) → reinstalar SCALE + importar pools si discos sobreviven; si no, sólo off-site (A7/A8) + PBS |

Regla transversal: la réplica es crash-consistent; NUNCA declararla "backup consistente" de bases de datos (eso son dumps G1A/G1B).

## Salud del HDD (pool2)

Scrub MENSUAL programado (tarea creada con la activación; hoy NO existe: única tarea del sistema apunta a pool0) · error de scrub/lectura = NO-SEND + alerta · SMART sin desactivar verificaciones · una escritura diaria (delta), sin fulls innecesarios.

## Verificación de canal (RO, cualquier momento)

```
ssh -i ~/.ssh/ariadna_truenas ariadna@192.168.31.91 "sudo -n zpool list -o name,size,alloc,free"
# API: Bearer $(cat ~/aranea/secrets/truenas/truenas-api-key.txt) → /api/v2.0/pool, /pool/dataset, /zfs/snapshot
# Notas 25.04.1: /replication y /pool/periodic-snapshot/task responden 404; cronjob endpoint existe (vacío).
```
