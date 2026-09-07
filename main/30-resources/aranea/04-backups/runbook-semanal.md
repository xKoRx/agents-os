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

# 📅 Runbook Semanal — Verificación de backups

> **Cuándo se ejecuta**: cada **lunes 09:00 hora Chile** (cron sugerido: `0 9 * * 1`)
> **Tiempo estimado**: 15-30 minutos
> **Responsable**: Hermes (automatizable, pero humano valida)
> **Aprobación**: Rodrigo ve el reporte generado al final

## 🎯 Objetivo

Confirmar que **todos los jobs de backup de la última semana funcionaron**, **no hay alertas críticas nuevas** en storage, y **los snapshots no se están acumulando más allá de la retención**.

## ⚠️ Pre-requisitos

| Pre-req | Status al 2026-06-30 |
|---|---|
| SSH `agent_ro` + sudo NOPASSWD en 6 nodos | 🔴 ROTO en 5/6 (bloqueador — ver [[../00-index]] § roadmap gap #1) |
| Cron configurado en hermes-vm o hades | ❓ no confirmado (post-implementación) |
| Mail relay para notificación de fallos | ❓ no configurado |

> [!warning] Mientras el bloqueador de SSH esté activo, este runbook es **diseño + checklist** — no se puede ejecutar end-to-end sin acceso root/sudo.

---

## 📋 Procedimiento

### Paso 1 — Ping check (read-only)

```bash
echo "=== Ping check $(date -Iseconds) ==="
for ip in 192.168.31.10 192.168.31.90 192.168.31.91 192.168.31.100 \
          192.168.31.110 192.168.31.120; do
  if ping -c 1 -W 2 "$ip" > /dev/null 2>&1; then
    echo "✅ $ip OK"
  else
    echo "🔴 $ip DOWN"
  fi
done
```

### Paso 2 — Ceph health (read-only)

```bash
ssha agent_ro@192.168.31.120 'sudo -n ceph status' | head -50
ssha agent_ro@192.168.31.120 'sudo -n ceph health detail'
ssha agent_ro@192.168.31.120 'sudo -n ceph df'
```

**Esperado**:
- `health: HEALTH_OK` o `HEALTH_WARN` con solo fragmentación conocida
- `pool1` <80% uso
- 4/4 OSDs `up`

**Si** 🔴 aparece `HEALTH_ERR` o un OSD `down` → abrir ticket y consultar [[runbook-incidentes]] § "OSD Ceph muere".

### Paso 3 — TrueNAS pools (read-only)

```bash
ssha agent_ro@192.168.31.91 'sudo -n zpool status'
ssha agent_ro@192.168.31.91 'sudo -n zpool list -H -o name,size,alloc,free,cap,health'
ssha agent_ro@192.168.31.91 'sudo -n zfs list -t snapshot -o name,creation,used,refer -H | sort -k2'
```

**Esperado**:
- `pool0` ONLINE con scrub reciente (<14 días)
- `pool2` ONLINE (no DEGRADED, no FAULTED)
- Snapshots presentes según retention policy (7 daily + 4 weekly + 12 monthly)

**Si** 🔴 scrub ausente o falla → [[runbook-incidentes]] § "Disco duro falla en TrueNAS".

### Paso 4 — Verificar que vzdump corrió (read-only)

```bash
# Listar últimos backups en NFS proxmox_storage
ssha agent_ro@192.168.31.91 'sudo -n ls -la /mnt/pool0/proxmox_storage/dump/ | tail -20'

# Listar últimos vzdump en PBS datastore (cuando PBS exista)
# ssha agent_ro@192.168.31.120 'sudo -n ls -la /backup/main/vzdump/ | tail -20'
```

**Esperado**:
- Al menos un vzdump por VM crítica (mt4-real, postgres, mongo, ubuntu-dev, truenas, obsidian-sync) en últimos 2 días
- Tamaño razonable (< tamaño del disco de la VM)

### Paso 5 — Verificar espacio en storage destino (read-only)

```bash
ssha agent_ro@192.168.31.91 'sudo -n df -h /mnt/pool0/proxmox_storage'
ssha agent_ro@192.168.31.120 'sudo -n df -h /backup'  # cuando PBS exista en kronos
```

**Esperado**:
- `/mnt/pool0/proxmox_storage` <70% (con `prune-backups` activo)
- Si >85% → ejecutar `prune-backups` antes de que llene

### Paso 6 — Verificar SMART de discos críticos (read-only)

```bash
# pool0 SSD mirrors (vistos desde truenas como sda-sdh virtio, pero SMART físico está en hades)
ssha agent_ro@192.168.31.91 'sudo -n smartctl -H /dev/sda'  # resumen
ssha agent_ro@192.168.31.91 'sudo -n smartctl -a /dev/sda | grep -E "Reallocated|Pending|Uncorrect|Temperature"'

# pool2 single disk
ssha agent_ro@192.168.31.91 'sudo -n smartctl -a /dev/sdg | grep -E "Reallocated|Pending|Uncorrect|Temperature"'

# Ceph OSDs (NVMe en zeus/hera/kronos)
ssha agent_ro@192.168.31.100 'sudo -n smartctl -a /dev/nvme0n1'  # osd.2 zeus
ssha agent_ro@192.168.31.110 'sudo -n smartctl -a /dev/nvme1n1'  # osd.0 hera
ssha agent_ro@192.168.31.120 'sudo -n smartctl -a /dev/nvme0n1'  # osd.1 kronos
ssha agent_ro@192.168.31.120 'sudo -n smartctl -a /dev/nvme1n1'  # osd.3 kronos
```

**Esperado**:
- `Reallocated_Sector_Ct = 0`
- `Current_Pending_Sector = 0`
- `Uncorrectable_Error_Cnt = 0`
- Temperatura NVMe <70°C

**Si** alguno >0 → abrir ticket y considerar [[runbook-incidentes]].

### Paso 7 — Verificar que `zfs send` a kronos funcionó (read-only)

```bash
ssha agent_ro@192.168.31.120 'sudo -n zfs list -t all | grep recv'  # cuando exista backup pool
```

**Esperado**:
- Snapshots presentes en `backup/pool0` y `backup/pool2` con timestamp de últimos 7 días

### Paso 8 — Validar log de errores de cron (read-only)

```bash
# En el host donde corran los cron (truenas o hermes-vm)
ssha agent_ro@192.168.31.91 'sudo -n journalctl -u cron --since "7 days ago" --no-pager | grep -iE "fail|error" | tail -20'
```

### Paso 9 — Generar reporte

```bash
cat <<EOF > /tmp/backup-weekly-$(date +%Y%m%d).md
# Backup Weekly Report — $(date -Iseconds)

## Estado

| Check | Status | Notas |
|---|---|---|
| Ping 6/6 | $(...) | |
| Ceph health | $(...) | |
| pool0 scrub | $(...) | |
| pool2 scrub | $(...) | |
| vzdump últimas 24h | $(...) | |
| Off-host copy | $(...) | |
| Disco pool2 SMART | $(...) | |

## Acciones requeridas

- [ ] (si aplica)
EOF
```

---

## ✅ Validación

El runbook se considera exitoso si:
- [ ] Todos los checks `✅` o `🟡` (warning conocido)
- [ ] No hay `🔴` críticos
- [ ] Snapshots existen dentro de la retention policy
- [ ] Reporte markdown generado

## 👤 Responsable

**Primario**: Hermes (ejecuta)
**Validación**: Rodrigo (lee el reporte, escala si 🔴)

## ↩️ Rollback

Este runbook es **100% read-only**. No hay rollback que valga la pena definir — el único efecto es generar un reporte.

Si algo falla durante la verificación → no es un fallo del runbook, es un hallazgo → abrir ticket y consultar [[runbook-incidentes]].

---

## Captured

2026-06-30. Diseñado por Hermes Task 2 (ticket [[../05-tickets/2026-06-30-011-aranea-storage-audit-backup]]).

## Validación

- Verificar precondiciones y resultados del procedimiento antes de declarar éxito.
