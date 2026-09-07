---
type: runbook
schema_version: 1
scope: project
created: 2026-08-10
updated: 2026-08-10
area: "[[Aranea]]"
project:
application:
entities:
  - "[[Aranea]]"
related: []
aliases: []
confidence: medium
source_session:
load_policy: manual
indexable: true
index_priority: high
tags:
  - kind/runbook
  - scope/project
  - area/aranea
---

## Propósito

Procedimiento operacional histórico de [[Aranea]]; validar los datos volátiles antes de ejecutarlo.

## Procedimiento

# 📆 Runbook Mensual — Scrubs + Restore Drill + Rotación

> **Cuándo se ejecuta**: **día 1° de cada mes a las 02:00 hora Chile** (scrubs), **día 15 a las 10:00** (restore drill)
> **Tiempo estimado**: scrub pool0 ~4 h, scrub pool2 ~12 h, restore drill ~1 h
> **Responsable**: Hermes ejecuta, Rodrigo aprueba el drill
> **Aprobación previa**: Rodrigo debe firmar ticket `applied` antes del día 1°

## 🎯 Objetivo

Tres tareas mensuales críticas:
1. **Scrubs programados** de `pool0` y `pool2` (validación de integridad ZFS)
2. **Restore drill real** (al menos 1 VM completa o 1 dataset completo recuperado)
3. **Rotación del medio off-host** (USB si aplica; verificación de cloud si aplica)

---

## 📋 Tarea 1 — Scrub de `pool0` (día 1° del mes, 02:00)

> **Read-only pero intensivo en I/O.** Programar para horario de baja carga.

### Procedimiento

```bash
# Lanzar scrub
ssha agent_ro@192.168.31.91 'sudo -n zpool scrub pool0'

# Monitorear (no bloqueante, poll cada 30 min)
while ssha agent_ro@192.168.31.91 'sudo -n zpool status pool0 | grep -q "scan: scrub in progress"'; do
  echo "$(date -Iseconds) — scrub en progreso"
  ssha agent_ro@192.168.31.91 'sudo -n zpool status pool0 | grep "scan:"'
  sleep 1800
done

# Reporte final
ssha agent_ro@192.168.91 'sudo -n zpool status pool0'
```

### Validación

| Check | Esperado | Acción si falla |
|---|---|---|
| `scan: scrub repaired 0` | ✅ | Si >0 errores → abrir ticket → [[runbook-incidentes]] § "Disco duro falla en TrueNAS" |
| `errors: No known data errors` | ✅ | Si hay errores → NO destruir pool, abrir ticket |

### Rollback

Scrub es **read-only**. No hay rollback. Si el scrub revela errores, **NO** tomar acciones destructivas (`zpool clear` solo con approval ticket). Consultar [[recovery-procedures]] § "Restore a ZFS dataset from snapshot or off-host copy".

---

## 📋 Tarea 2 — Scrub de `pool2` (día 3-5 del mes, 02:00)

> **CRÍTICO**: pool2 no se ha scrubbeado desde 2025-07-12 (ver [[../03-storage/truenas-pool2]]). El primer scrub debe ser **manual ASAP** (no esperar al día 1° del próximo mes).

### Acción inmediata (no esperar)

```bash
ssha agent_ro@192.168.31.91 'sudo -n zpool scrub pool2'
```

### Procedimiento mensual (post-primera vez)

Igual que pool0 pero con duración esperada mayor (HDD single disk ~7-12 h).

### Validación

- Mismo criterio que pool0.

### Rollback

Igual que pool0.

---

## 📋 Tarea 3 — Prune-backups (semanal integrado, revisado el día 1°)

### Procedimiento

```bash
# Listar backups en proxmox_storage > 30 días
ssha agent_ro@192.168.31.91 'sudo -n find /mnt/pool0/proxmox_storage/dump -name "vzdump-*.tar*" -mtime +30 | head -20'

# Mostrar config actual
ssha agent_ro@192.168.31.91 'sudo -n pvesm status | grep nfs-storage'

# Confirmar que prune-backups está activo (debería estarlo por storage config)
ssha agent_ro@192.168.31.100 'sudo -n pvesm list nfs-storage | head -5'
```

### Validación

- Política `keep-daily=7, keep-weekly=4, keep-monthly=12` configurada y respetada.
- Si no hay política → **configurar**:

```bash
ssha agent_ro@192.168.31.100 'sudo -n pvesm set nfs-storage --prune-backups keep-daily=7,keep-weekly=4,keep-monthly=12'
```

### Rollback

Ninguno destructivo. Si prune se ejecutó con error → restaurar desde off-host ([[recovery-procedures]]).

---

## 📋 Tarea 4 — Restore Drill (día 15, 10:00 hora Chile)

> **Crítico**: un backup no probado no es backup. Este drill es la prueba mensual.

### Selección de la VM a restaurar

Rotar entre:
- Mes 1: `mt4-test` (qemu/125) — producción no-crítica
- Mes 2: `obsidian-sync` (lxc/116) — verificar CouchDB
- Mes 3: `postgresql` (qemu/152) — DB production-like
- Mes 4: `mt4-test` (otra vez, distinto día)
- Mes 5: `truenas` (qemu/145) — meta: backup de la VM que hace los backups
- Mes 6: Una VM stopped (sqx-ulab-kron-1) — validar restore de VM apagada

### Procedimiento (ejemplo: VM `mt4-test` desde PBS)

> Asume que PBS ya está configurado (ver [[../03-storage/BACKUP-SYSTEM]] § 4.2). Si no, adaptar a `vzdump` en NFS.

```bash
# 1. Listar backups disponibles para la VM target
ssha agent_ro@192.168.31.120 'sudo -n pvesm list backup-pbs --vmid 125'

# 2. Restaurar como VM NUEVA (no sobreescribir la original)
ssha agent_ro@192.168.31.120 'sudo -n qmrestore <backup-archive> 999 --storage pool1 --unique'

# 3. Verificar que arranca
ssha agent_ro@192.168.31.120 'sudo -n qm start 999'
sleep 60
ssha agent_ro@192.168.31.120 'sudo -n qm status 999'

# 4. Verificar red y servicios dentro de la VM
ssha agent_ro@192.168.31.120 'sudo -n qm guest cmd 999 network-get-interfaces'
ssha root@192.168.31.120 'ping -c 3 192.168.31.999'

# 5. Documentar tiempo total y hallazgos
echo "Restore drill $(date -Iseconds)" >> /var/log/aranea-restore-drills.log
echo "VM: 999 (clone of 125)" >> /var/log/aranea-restore-drills.log
echo "Source: PBS datastore main" >> /var/log/aranea-restore-drills.log
echo "Time to boot: 60s" >> /var/log/aranea-restore-drills.log

# 6. Cleanup (solo después de documentar)
ssha agent_ro@192.168.31.120 'sudo -n qm stop 999'
ssha agent_ro@192.168.31.120 'sudo -n qm destroy 999'
```

### Validación

| Check | Esperado |
|---|---|
| Backup de la VM existe en PBS/NFS | ✅ |
| Restore completa sin error | ✅ |
| VM arranca | ✅ |
| Red funcional (responde a ping) | ✅ |
| Servicios internos activos | ✅ |
| Tiempo total < 30 min | ✅ |

### Rollback

- Si restore falla a mitad → la VM original (125) no fue tocada (usamos `--unique` para crear 999).
- Cleanup `qm destroy 999` solo si todo OK o si queremos reintentar.

### Tickets

- Crear ticket `2026-MM-DD-restore-drill-N.md` documentando el drill.
- Si falla → escalar con ticket `priority=high` y consultar [[runbook-incidentes]].

---

## 📋 Tarea 5 — Rotación de medio off-host (si aplica)

> Solo si ya hay USB cifrado o NAS remoto configurado.

### Procedimiento (USB cifrado LUKS)

```bash
# 1. Verificar última sincronización exitosa al USB
ls -la /mnt/off-host-usb/.last-sync

# 2. Si >7 días → sincronizar (NO destructivo)
rsync -avh --dry-run /mnt/backup-arrival/ /mnt/off-host-usb/
# Si dry-run OK, ejecutar sin --dry-run

# 3. Validar checksum
find /mnt/off-host-usb -name "*.sha256" -exec sha256sum -c {} \;

# 4. Log
echo "USB rotation $(date -Iseconds) — OK" >> /var/log/aranea-offhost.log
```

### Validación

- Sync completa sin errores.
- Checksums válidos.

### Rollback

Ninguno destructivo (rsync no borra destino por default).

---

## 📋 Tarea 6 — Reporte mensual consolidado

```markdown
# Backup Monthly Report — {YYYY-MM}

## Scrubs

| Pool | Fecha scrub | Errores repaired | Duración |
|---|---|---|---|
| pool0 | YYYY-MM-01 | 0 | 4h 12m |
| pool2 | YYYY-MM-03 | 0 | 11h 33m |

## Restore drill

- VM target: 999 (clone of 125 mt4-test)
- Fuente: PBS datastore main
- Resultado: ✅ OK
- Tiempo total: 22 min
- Hallazgos: (ninguno / lista)

## Prune-backups

- Política activa: keep-daily=7, keep-weekly=4, keep-monthly=12
- Espacio liberado: 32 GB
- Backups restantes: 18

## Off-host copy

- USB rotación: YYYY-MM-15 ✅
- VPS sync: ✅ (si aplica)

## Acción requerida

- (si aplica)
```

---

## ✅ Validación final del mes

| Tarea | Status |
|---|---|
| Scrub pool0 | ✅ |
| Scrub pool2 | ✅ |
| Prune-backups | ✅ |
| Restore drill real | ✅ |
| Off-host rotación | ✅ |
| Reporte generado | ✅ |

---

## 👤 Responsables

- **Ejecuta**: Hermes
- **Aprueba drill**: Rodrigo (revisa ticket + métricas)
- **Revisa reporte**: Rodrigo

## ↩️ Rollback

Ninguna tarea de este runbook es destructiva en operación normal. La única acción "destructiva" potencial es `qm destroy 999` después del drill — solo se ejecuta después de documentar éxito.

---

## Captured

2026-06-30. Diseñado por Hermes Task 2 (ticket [[../05-tickets/2026-06-30-011-aranea-storage-audit-backup]]).

## Validación

- Verificar precondiciones y resultados del procedimiento antes de declarar éxito.
