# Runbook — Replicación ZFS diaria pool0 → pool2 (Aranea)

> Runbook evergreen (mecánica operativa). La arquitectura y decisiones viven en el proyecto: `10-projects/Aranea/BACKUP-DR-OWNER-PROJECT/POOL0-TO-POOL2-REPLICATION-SPEC.md`. Autoridad de activación: gates G-REP-0..5 del owner. Última verificación: 2026-09-21 noche-3 (TrueNAS 25.04.1, SSH ariadna@truenas + midclt + código instalado). **Mecanismo definitivo: stack NATIVO de replicación (plugin `replication` → motor `zettarepl`), transporte LOCAL** — el plan anterior (cron interno + script zfs) quedó DESCARTADO al refutarse la "ausencia de API" (401≠404; enum `LOCAL` en `plugins/replication.py`).

## Contexto fijo

- pool0 = mirror ×3, 4,08T size / 2,44T alloc / **1,64T free zpool**, datos productivos. pool2 = HDD single-disk 7,27T / 3,19T alloc / **4,08T free zpool**, función ÚNICA: réplica diaria de pool0 (D-NEW-01; sin VMs/rootfs/apps/backups de VM).
- Capacidad SIEMPRE por **`zpool list` free**, nunca por el AVAIL de `zfs list` (subestima 2,05T por la histéresis de 442 snapshots legacy de `pool2/backup`). Umbrales: free < 1,00T → NO-SEND + alerta; < 1,50T → aviso temprano.
- Envío inicial: **2,35T base `refer`** (ledger §1 SPEC; excluidos `.ix-virt`/`.system`, 18,6G justificados).
- Destino: dataset `pool2/pool0-replica` (árboles legacy `pool2/backup`, `pool2/pool0_backup`, `pool2/zfs_backup` INTACTOS — F-09). `sync=always` de `pool0_backup` NO se hereda (fixture prueba `properties=false`; fallback `properties_override={"sync":"standard"}`).
- Ejecución 100% en TrueNAS (middleware nativo); JAMÁS dependiente de Hermes/agentes (D-NEW-06).

## Componentes nativos (creados con G-REP-4, payloads en `~/aranea/work/replicacion-pool0-pool2/`)

1. **Snapshottask** `pool.snapshottask`: dataset `pool0` recursivo, naming `repl-%Y-%m-%d_%H-%M`, **04:45**, retención 14 DAY, exclude `.ix-virt`/`.system` (efectividad Plan A/B validada en fixture G-REP-0).
2. **Replication task**: PUSH **LOCAL** `pool0` → `pool2/pool0-replica`, recursive, exclude ídem, enlazada al snapshottask, schedule **04:50**, `readonly:"SET"`, `retention_policy:"NONE"`, `allow_from_scratch:false` (jamás full implícito), retries 5.
3. **Scrub mensual pool2**: `pool.scrub.create` (domingo 00:00; el día de scrub la réplica 04:50 corre en la cola del scrub — contención aceptada 1×/mes).
4. **Alertas**: subsistema nativo del middleware; canal de entrega = G-REP-5 (`smtp=false` medido 21sep; ver `ALERTA-SMTP-PENDIENTE.md`).

## Procedimiento diario (incremental; automático)

1. 04:45 snapshottask crea el set recursivo `@repl-YYYY-MM-DD_HH-MM` (un txg, atómico multi-dataset).
2. 04:50 la tarea de replicación deriva sola los incrementales desde los snapshots comunes origen/destino (zettarepl; nunca asume "ayer").
3. Verificación: `midclt call zettarepl.list_states` (estado FINISHED/errores) + `zfs list -t snapshot -r pool2/pool0-replica` (snapshot del día visible). Semanal: comparación `refer` origen/destino por dataset.
4. Fallo/interrupción: la sesión queda en el último snapshot común; reintenta en el schedule siguiente SIN full (allow_from_scratch=false impide full automático). Cadena perdida (>7 días de fallos con retención 14d): FAILED cerrado + alerta; full re-send sólo en ventana aprobada por owner.

## Primera réplica (full; ventana exclusiva gated G-REP-3)

Pre: fixture G-REP-0 verificado · scrub pool2 con 0 errores (G-REP-1, ventana propia ~7h) · presupuesto I/O exclusivo (sin vzdump fulls/G1B/migraciones ese día; Echo cerrado) · `replication.run_onetime <id>` con schedule deshabilitado · monitoreo horario (estado job, tasa, `zpool list -o free pool2` ≥1,00T) · duración esperada **7-11h (~2,35T a HDD)** · post: `zfs list -r pool2/pool0-replica` (hijos+volsize) + drill de lectura (dataset hijo + zvol clonados RO).

## Snapshots y retención

- Origen: 14 × `@repl-*` (snapshottask). Los snapshots legacy 2025 = intocables (limpieza = decisión owner separada; ~52,9G de media frigate viven SOLO ahí — borrarlos cambia el alcance de la réplica retroactivamente).
- Destino: 7 días sobre `@repl-*` en `pool2/pool0-replica` (mecanismo elegido en fixture; default diseño: cronjob interno con destroy programado).
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

Scrub MENSUAL nativo (creado con G-REP-4; hoy NO existe tarea para pool2: la única tarea id=3 apunta a pool0) · error de scrub/lectura = NO-SEND + alerta nativa (canal G-REP-5) · SMART sin desactivar verificaciones · una escritura diaria (delta), sin fulls innecesarios.

## Verificación de canal (RO, cualquier momento)

```
ssh -i ~/.ssh/ariadna_truenas ariadna@192.168.31.91 "sudo -n zpool list -o name,size,alloc,free"
# Tareas nativas (RO): sudo -n midclt call replication.query ; pool.snapshottask.query ; zettarepl.list_states
# API: Bearer $(cat ~/aranea/secrets/truenas/truenas-api-key.txt) → /api/v2.0/replication (401 sin auth = ruta viva)
```
