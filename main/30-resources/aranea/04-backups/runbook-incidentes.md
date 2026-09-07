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

# 🚨 Runbook de Incidentes — Qué hacer cuando algo se rompe

> **Cuándo se ejecuta**: bajo demanda cuando se detecta una falla
> **Tiempo objetivo de respuesta**: 1 hora para incidentes P1
> **Responsable primario**: Hermes (automatiza la respuesta), Rodrigo aprueba acciones destructivas
> **Principio**: **primero contener, después diagnosticar, después restaurar**

## 🎯 Severidades

| Sev | Ejemplos | SLA respuesta | Acción |
|---|---|---|---|
| 🔴 **P1** | TrueNAS VM no bootea, hades muerto, ransomware suspected | < 1 h | Contención inmediata, ticket crítico |
| 🟠 **P2** | Disco falla, OSD Ceph down, scrub falla con errores | < 4 h | Diagnóstico + ticket |
| 🟡 **P3** | SMART error warning, fragmentación creciente, snapshot falla | < 24 h | Diagnóstico + ticket |

---

## 📋 Incidente 1: 💽 Disco duro falla en TrueNAS (pool0 o pool2)

> **Sev**: 🟠 P2 (pool0) o 🔴 P1 (pool2, porque tiene los backups)
> **Detección**: alerta SMART, `zpool status DEGRADED`, scrub con errores

### 1.1 Diagnóstico (read-only)

```bash
# Estado del pool
ssha agent_ro@192.168.31.91 'sudo -n zpool status -v'
ssha agent_ro@192.168.31.91 'sudo -n zpool events -v | tail -50'

# SMART del disco sospechoso
ssha agent_ro@192.168.31.91 'sudo -n smartctl -a /dev/sd<X>'

# Buscar serial del disco que falla
ssha agent_ro@192.168.31.91 'sudo -n zpool status | grep -A1 "was faulted\|degraded\|offline"'
```

### 1.2 Contención

| Escenario | Acción |
|---|---|
| **pool0 mirror degraded** (1 disco del mirror caído) | ✅ Pool sigue funcional. Reemplazar disco cuando llegue repuesto. Sin urgencia. |
| **pool2 single disk faulted** | 🔴 Todos los datasets de pool2 son inaccesibles. **Saltar a 1.4 — recuperación**. |
| **smartd predijo falla** | Reemplazar disco preventivamente. Pool sigue funcional. |

### 1.3 Reemplazo de disco (pool0 mirror)

> Requiere disco de repuesto **del mismo tamaño o mayor**. Si no hay → pedirlo y abrir ticket `waiting_parts`.

```bash
# 1. Identificar disco físico (visto desde hades, NO truenas)
ssha agent_ro@192.168.31.90 'sudo -n ls -la /dev/disk/by-id/ | grep QEMU'  # en hades

# 2. Offline el disco fallido en truenas (NO destructivo)
ssha agent_ro@192.168.31.91 "sudo -n zpool offline pool0 <disk-name>"

# 3. Reemplazar físicamente el QEMU virtio disk (en hades PVE)
#    Editar VM 145 (truenas), swap disk hardware. Requiere apagar truenas.
ssha agent_ro@192.168.31.90 'sudo -n qm shutdown 145'
sleep 30
# (intervención manual para swap disk)
ssha agent_ro@192.168.31.90 'sudo -n qm start 145'

# 4. Reemplazar el disco en ZFS
ssha agent_ro@192.168.31.91 'sudo -n zpool replace pool0 <old-disk> <new-disk>'

# 5. Monitorear resilver
while ssha agent_ro@192.168.31.91 'sudo -n zpool status pool0 | grep -q "scan: resilver"'; do
  ssha agent_ro@192.168.31.91 'sudo -n zpool status pool0 | grep "scan:"'
  sleep 300
done

# 6. Scrub final
ssha agent_ro@192.168.31.91 'sudo -n zpool scrub pool0'
```

### 1.4 Recuperación cuando pool2 falla (🔴 P1)

> `pool2` es donde están los backups actuales. Si falla, **se pierde el segundo nivel de backup**. Acción: depender del off-host (si existe) o aceptar pérdida parcial.

```bash
# Si hay off-host (USB, kronos, VPS), restaurar TODO lo que se pueda
# (ver recovery-procedures.md)

# Si NO hay off-host, las opciones son limitadas:
# - Trading_systems 305 GB en pool2 → perdido, pero aún existe en pool0 (485 GB originales)
# - aranea_storage 39 GB backup → perdido, pero existe en pool0 (998 GB originales)
# - iso_storage 15 GB → perdido, descargable
# - pool0_backup/ → perdido
# - zfs_backup/ → perdido

# Acciones inmediatas:
# 1. NO tocar disco (puede haber datos recuperables con herramientas forenses)
# 2. Comprar disco nuevo 8 TB
# 3. Recrear pool2 desde cero (ver recovery-procedures.md § "Restore a ZFS dataset from off-host")
```

### 1.5 Validación post-fix

- [ ] `zpool status` muestra ONLINE
- [ ] `zpool scrub` retorna 0 errores
- [ ] Todos los datasets accesibles
- [ ] Tickets de seguimiento creados

### 1.6 Rollback

Si el resilver empeora las cosas → **NO abortar resilver**. Dejarlo terminar. Si un disco adicional muere durante resilver, abrir ticket P1 y consultar [[recovery-procedures]].

### 1.7 Tickets

- Crear `YYYY-MM-DD-NNN-disk-fail-pool<X>.md` con severidad y timeline.

---

## 📋 Incidente 2: 🐙 OSD Ceph muere

> **Sev**: 🟠 P2 (1 OSD) → 🔴 P1 (2+ OSDs simultáneos)
> **Detección**: `ceph health` reporta `OSD_DOWN`, `PG_DEGRADED`

### 2.1 Diagnóstico (read-only)

```bash
ssha agent_ro@192.168.31.120 'sudo -n ceph status'
ssha agent_ro@192.168.31.120 'sudo -n ceph health detail'
ssha agent_ro@192.168.31.120 'sudo -n ceph osd tree'
ssha agent_ro@192.168.31.120 'sudo -n ceph osd df tree'
```

### 2.2 Causas probables

| Síntoma | Causa | Acción |
|---|---|---|
| `osd.<id> down` con crash dump | Crash del proceso OSD | Reiniciar OSD |
| Disco NVMe no responde | Fallo de hardware | Reemplazar disco + re-crear OSD |
| `OSD flapping` (up/down/up) | Problema de red, switch, jumbo frames | Diagnosticar red |
| `slow ops` | Fragmentación o disco lento | `compact` + SMART |

### 2.3 Reinicio de OSD (no destructivo)

```bash
# En el nodo del OSD
ssha agent_ro@192.168.31.100 'sudo -n systemctl restart ceph-osd@2.service'  # ejemplo para osd.2 en zeus
sleep 30
ssha agent_ro@192.168.31.100 'sudo -n ceph osd tree | grep osd.2'
```

### 2.4 Reemplazo de disco NVMe (requiere HW)

```bash
# 1. Marcar OSD out (Ceph empieza a replicar datos a otros OSDs)
ssha agent_ro@192.168.31.100 'sudo -n ceph osd out osd.2'

# 2. Esperar a que PG quede clean
ssha agent_ro@192.168.31.100 'sudo -n ceph -w'  # Ctrl+C cuando "active+clean"

# 3. Stop y destroy OSD
ssha agent_ro@192.168.31.100 'sudo -n systemctl stop ceph-osd@2'
ssha agent_ro@192.168.31.100 'sudo -n ceph osd purge osd.2 --yes-i-really-mean-it'

# 4. Reemplazar disco NVMe físicamente (intervención manual)

# 5. Recrear OSD
ssha agent_ro@192.168.31.100 'sudo -n ceph-volume lvm create --data /dev/nvme0n1'

# 6. Validar
ssha agent_ro@192.168.31.100 'sudo -n ceph osd tree | grep osd.2'
ssha agent_ro@192.168.31.100 'sudo -n ceph -s | grep -E "health|recovery"'
```

### 2.5 Validación

- [ ] `ceph health` → HEALTH_OK (o solo WARN de fragmentación conocida)
- [ ] Todos los PGs `active+clean`
- [ ] 4/4 OSDs `up`

### 2.6 Rollback

`osd purge` es destructivo del OSD. No se puede deshacer. Si falla a mitad, el OSD queda marked out pero los datos siguen accesibles desde réplicas. Recrear OSD es straightforward.

---

## 📋 Incidente 3: 🖥️ Nodo Proxmox se cae

> **Sev**: 🔴 P1 si hades/athena caen; 🟠 P2 si zeus/hera/kronos caen
> **Detección**: `pvecm status` reporta nodo offline, alertas corosync

### 3.1 Diagnóstico (read-only)

```bash
ssha agent_ro@192.168.31.100 'sudo -n pvecm status'
ssha agent_ro@192.168.31.100 'sudo -n ha-manager status'
ssha agent_ro@192.168.31.10 'sudo -n journalctl -u corosync --since "1 hour ago" --no-pager | tail -30'
```

### 3.2 Si es un nodo NO-hades (zeus/hera/kronos)

- Las VMs se reinician automáticamente en otro nodo (si HA está configurado)
- Si no hay HA → iniciar manualmente en otro nodo con `qm start <vmid>` desde otro nodo
- Investigar causa de la caída (HW, kernel panic, OOM)

### 3.3 Si es hades (🔴 P1 — afecta todo)

> **Esto es el escenario worst-case**. hades caído = truenas caído = NFS/iSCSI caídos = todas las VMs sin disco compartido.

**Pasos inmediatos**:

1. **Verificar si es transitorio** (kernel panic, reboot) o permanente (HW muerto).
2. **Si hades revive** → verificar truenas VM → verificar NFS en todos los PVE.
3. **Si hades no revive** → restaurar desde PBS/off-host:
   - VMs críticas (mt4-real, postgres, mongo) desde PBS en kronos
   - Reconstruir truenas desde PBS (es la VM más importante)
   - Ver [[recovery-procedures]] § "Restore entire Proxmox node from scratch"
4. **Mientras tanto**: levantar VM truenas alternativa en otro nodo (kronos) con discos de réplica ZFS enviados pre-incidente. **Requiere pre-incidente: tener zfs send/recv configurado**.

### 3.4 Si es athena (gateway)

> athena caída = OPNsense caída = toda la red cae.
> Este incidente está fuera del scope de storage pero es adyacente.
> Solución: tener OPNsense en HA con CARP, o en hardware dedicado.

### 3.5 Validación

- [ ] `pvecm status` reporta quórum completo
- [ ] Todas las VMs accesibles
- [ ] Ceph HEALTH_OK
- [ ] NFS/iSCSI funcionando

---

## 📋 Incidente 4: 💾 TrueNAS VM no bootea (qemu/145 en hades)

> **Sev**: 🔴 P1 (todo el cluster depende del NFS/iSCSI de truenas)
> **Detección**: hades responde pero truenas no; mount NFS falla en otros nodos

### 4.1 Diagnóstico (read-only, desde hades)

```bash
# Estado de la VM
ssha agent_ro@192.168.31.90 'sudo -n qm status 145'

# Consola de la VM (no interactivo, solo últimos mensajes)
ssha agent_ro@192.168.31.90 'sudo -n qm show 145 --pretty'

# Logs de truenas (vía SSH si responde, o serial console)
ssha agent_ro@192.168.31.90 'sudo -n tail -50 /var/log/pve/tasks/active'
```

### 4.2 Causas probables

| Causa | Síntoma | Acción |
|---|---|---|
| Disco VM corrupto | qemu error "disk not accessible" | Restaurar disco desde backup |
| ZFS pool import falla | truenas arranca pero pool no se monta | `zpool import` manual desde shell truenas |
| Kernel panic en truenas | truenas stuck, no SSH | Serial console + reiniciar |
| hades no tiene memoria | hades RAM 100% | Liberar RAM (apagar VM stopped) |

### 4.3 Reiniciar truenas (no destructivo)

```bash
ssha agent_ro@192.168.31.90 'sudo -n qm stop 145 --timeout 60'
sleep 30
ssha agent_ro@192.168.31.90 'sudo -n qm start 145'
sleep 60

# Validar NFS
mount | grep nfs-storage  # en cada PVE node
```

### 4.4 Si truenas tiene ZFS pool corrupto (caso raro)

```bash
# Acceder a consola truenas (vía qemu monitor)
ssha agent_ro@192.168.31.90 'sudo -n qm terminal 145'

# Dentro de truenas:
zpool status
zpool import -a  # intenta importar todos los pools

# Si pool0 tiene errores graves:
zpool clear pool0  # ⚠️ solo si ticket aprobado, limpia errores
# o restaurar desde off-host (ver recovery-procedures.md)
```

### 4.5 Rollback

`qm stop`/`qm start` no es destructivo. `zpool clear` SÍ es problemático (puede empeorar la corrupción). Solo con ticket P1 aprobado.

---

## 📋 Incidente 5: 🗄️ CouchDB dañada (obsidian-sync lxc/116)

> **Sev**: 🟡 P2 (solo afecta sincronización Obsidian)
> **Detección**: vault no sincroniza, errores en logs CouchDB

### 5.1 Diagnóstico (read-only)

```bash
ssha agent_ro@192.168.31.90 'sudo -n pct enter 116'
# Dentro del LXC:
systemctl status couchdb
journalctl -u couchdb --since "1 hour ago" | tail -30
curl -s http://admin:<pw>@localhost:5984/_up
curl -s http://admin:<pw>@localhost:5984/_all_dbs
```

### 5.2 Si CouchDB no arranca

```bash
# Verificar espacio en disco
df -h /  # dentro del LXC

# Verificar integridad del archivo DB
ls -la /var/lib/couchdb/

# Si archivo .couch corrupto:
systemctl stop couchdb
cp /var/lib/couchdb/.delete-me-to-rebuild-the-db /tmp/  # NO rm -rf
systemctl start couchdb
# CouchDB rebuilds from .delete trigger
```

### 5.3 Restaurar desde backup

```bash
# Si hay backup (ver BACKUP-SYSTEM §3.6):
# Asumiendo backup en /var/backups/couchdb/YYYY-MM-DD/

systemctl stop couchdb
cp -a /var/lib/couchdb /var/lib/couchdb.broken
mkdir -p /var/lib/couchdb
cp -a /var/backups/couchdb/YYYY-MM-DD/* /var/lib/couchdb/
chown -R couchdb:couchdb /var/lib/couchdb
systemctl start couchdb

# Validar
curl -s http://admin:<pw>@localhost:5984/_all_dbs
```

### 5.4 Validación

- [ ] CouchDB responde a `_up`
- [ ] `_all_dbs` muestra las DB esperadas
- [ ] Cliente Obsidian sincroniza

### 5.5 Rollback

Ninguno destructivo en operación normal. El `cp -a` deja la DB rota original en `couchdb.broken` por si hay que recurrir a ella.

---

## 📋 Incidente 6: 🦠 Ransomware suspected

> **Sev**: 🔴 P1
> **Detección**: VMs encriptadas, archivos con extensión rara, ransom note

### 6.1 Contención INMEDIATA (no destructivo)

```bash
# 1. APAGAR (no destruir) las VMs sospechosas
ssha agent_ro@192.168.31.90 'sudo -n qm stop <vmid> --timeout 30'

# 2. DESCONECTAR de red (editar config de NIC)
ssha agent_ro@192.168.31.90 'sudo -n qm set <vmid> --net0 none'

# 3. AISLAR el almacenamiento (NFS read-only o desmontar)
ssha agent_ro@192.168.31.91 'sudo -n zfs set readonly=on pool0/<dataset>'

# 4. PRESERVAR evidencia: snapshot del estado actual
ssha agent_ro@192.168.31.91 'sudo -n zfs snapshot pool0/<dataset>@ransomware-suspect-$(date +%Y%m%d)'
```

### 6.2 Análisis (read-only)

```bash
# Buscar ransom notes
ssha agent_ro@192.168.31.91 'sudo -n find /mnt/pool0 -name "*.txt" -newer /tmp/last-known-good' | head

# Buscar extensiones sospechosas
ssha agent_ro@192.168.31.91 'sudo -n find /mnt/pool0 -name "*.locked" -o -name "*.crypt" -o -name "*.encrypted" 2>/dev/null' | head

# Logs
ssha agent_ro@192.168.31.91 'sudo -n cat /var/log/messages | grep -iE "ransom|crypt|encrypt|bitcoin"' | tail
```

### 6.3 Recuperación

> **No** pagar rescate. **No** intentar descifrar. Restaurar desde off-host.

```bash
# Ver recovery-procedures.md § "Restore entire Proxmox node from scratch"
# Restaurar TODAS las VMs afectadas desde PBS (off-host backup pre-ataque)
```

### 6.4 Validación post-recuperación

- [ ] VMs restauradas en estado pre-ataque
- [ ] Credenciales rotadas (root, SSH keys, CouchDB admin, step-ca provisioner)
- [ ] Firewall perimetral reforzado
- [ ] Telemetría/EDR añadido

### 6.5 Rollback

N/A — el objetivo es restaurar, no revertir. Si la infección se propagó, **NO** reconectar antes de aislar todos los nodos.

### 6.6 Tickets

- Crear `YYYY-MM-DD-NNN-ransomware-suspected.md` con timeline detallado y evidencia preservada.

---

## 👤 Responsables y escalamiento

| Sev | Primera respuesta | Escalamiento |
|---|---|---|
| 🔴 P1 | Hermes (inmediato) | Rodrigo (vía ticket + mensaje directo) |
| 🟠 P2 | Hermes (4h) | Ticket estándar |
| 🟡 P3 | Hermes (24h) | Ticket estándar |

## ↩️ Rollback general

**Principio**: ningún runbook de incidentes realiza acciones destructivas por default. Toda acción destructiva (`zpool destroy`, `qm destroy`, `rm -rf`, `wipefs`, `ceph osd purge`) requiere:
1. Ticket `applied` aprobado por Rodrigo
2. Snapshot/backup previo del estado
3. Comando guardado textualmente en el ticket para auditoría

---

## Captured

2026-06-30. Diseñado por Hermes Task 2 (ticket [[../05-tickets/2026-06-30-011-aranea-storage-audit-backup]]).

## Validación

- Verificar precondiciones y resultados del procedimiento antes de declarar éxito.
