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

# 🔄 Recovery Procedures — Restauración desde backup

> **Cuándo se ejecuta**: ante disaster real o drill mensual (ver [[runbook-mensual]] § Tarea 4)
> **Principio**: **primero verificar integridad del backup, después restaurar**
> **Tiempo objetivo**: cada restore debe tomar < 30 min desde el comando de restore hasta VM operativa
> **Responsable**: Hermes ejecuta, Rodrigo aprueba si es disaster real (no drill)

## 🎯 Alcance

Este documento cubre 5 procedimientos de restore:

| # | Procedimiento | Caso de uso | Tiempo objetivo |
|---|---|---|---|
| 1 | **Restore a VM from PBS/vzdump** | VM crítica caída | < 30 min |
| 2 | **Restore a ZFS dataset from snapshot or off-host copy** | Dataset corrupto o perdido | < 30 min |
| 3 | **Restore single file from ZFS snapshot** | Borrado accidental | < 5 min |
| 4 | **Restore entire Proxmox node from scratch** | Nodo físico muerto | < 4 h |
| 5 | **Restore Obsidian vault (CouchDB)** | Vault corrupto | < 30 min |

---

## 📋 Procedimiento 1: Restore a VM from PBS/vzdump

### 1.1 Escenario

VM (ej: `mt4-real` qemu/124) murió o está corrupta. Hay backup en PBS datastore `main` (kronos) o en NFS `proxmox_storage` (truenas).

### 1.2 Pre-flight (read-only)

```bash
# Confirmar que el backup existe
ssha agent_ro@192.168.31.120 'sudo -n pvesm list backup-pbs --vmid 124'
# o
ssha agent_ro@192.168.31.91 'sudo -n ls -la /mnt/pool0/proxmox_storage/dump/vzdump-qemu-124-*'

# Confirmar timestamp del último backup
ssha agent_ro@192.168.31.120 'sudo -n pvesm list backup-pbs --vmid 124 --output-format json | jq ".[0] | {vmid, size, backup_time}"'

# Confirmar espacio en storage destino
ssha agent_ro@192.168.31.120 'sudo -n df -h /backup/main'
```

### 1.3 Restore usando PBS (recomendado)

```bash
# Opción A: Restaurar SOBRE la VM existente (asume que la VM está detenida)
ssha agent_ro@192.168.31.120 'sudo -n qm stop 124 --timeout 60'
ssha agent_ro@192.168.31.120 'sudo -n qmrestore <backup-archive> 124 --force'

# Opción B: Restaurar como VM NUEVA (no toca la original — más seguro)
ssha agent_ro@192.168.31.120 'sudo -n qmrestore <backup-archive> 199 --storage pool1 --unique'
# 199 = nuevo VMID; usar uno libre

# Validar VM creada
ssha agent_ro@192.168.31.120 'sudo -n qm status 199'

# Arrancar
ssha agent_ro@192.168.31.120 'sudo -n qm start 199'
sleep 60

# Verificar que arranca correctamente (consola + red)
ssha agent_ro@192.168.31.120 'sudo -n qm status 199'
ssha agent_ro@192.168.31.120 'sudo -n qm guest cmd 199 network-get-interfaces'
ssha root@192.168.31.120 "ping -c 3 192.168.31.199"
```

### 1.4 Restore desde NFS (fallback si PBS no está listo)

```bash
# Listar backups disponibles
ssha agent_ro@192.168.31.91 'sudo -n ls -la /mnt/pool0/proxmox_storage/dump/'

# Restaurar desde archivo NFS
ssha agent_ro@192.168.31.100 'sudo -n qmrestore /mnt/pve/nfs-storage/dump/vzdump-qemu-124-2026_06_29-02_00_00.vma.zst 199 --storage pool1 --unique'
```

### 1.5 Validación

| Check | Esperado | Comando |
|---|---|---|
| VM existe en PVE | ✅ | `qm config 199` |
| VM arranca | ✅ | `qm status 199` muestra `running` |
| Red funcional | ✅ | `qm guest cmd 199 network-get-interfaces` devuelve IPs |
| Servicios internos | ✅ | SSH a la VM y verificar |
| Datos consistentes | ✅ | Aplicación específica (ej: MT4 muestra cuenta real) |

### 1.6 Post-restore (cleanup)

```bash
# Si todo OK y la VM original estaba comprometida:
ssha agent_ro@192.168.31.120 'sudo -n qm stop 124 --timeout 60'
ssha agent_ro@192.168.31.120 'sudo -n qm destroy 124'

# Renombrar la nueva VM (opcional)
ssha agent_ro@192.168.31.120 'sudo -n qm set 199 --name mt4-real'

# Actualizar config de red para que use la IP original (si era distinta)
ssha agent_ro@192.168.31.120 'sudo -n qm set 199 --ipconfig0 ip=192.168.31.124/24,gw=192.168.31.1'
```

### 1.7 Rollback

| Escenario | Rollback |
|---|---|
| Restore falla a mitad → VM 199 está corrupta | `qm destroy 199`, intentar de nuevo |
| Restore OK pero VM no arranca | Verificar config de VM (`qm config 199`), comparar con backup |
| Restore funcionó pero datos son viejos | Aceptar (es lo que había en el backup); considerar RPO/RTO insuficiente |

### 1.8 Tickets

- `YYYY-MM-DD-NNN-restore-vm-<name>.md` con timeline y validación.

---

## 📋 Procedimiento 2: Restore a ZFS dataset from snapshot or off-host copy

### 2.1 Escenario

Dataset ZFS (ej: `pool0/aranea_storage`) está corrupto o perdido. Hay snapshots locales o copia off-host (kronos vía `zfs send/recv`).

### 2.2 Restaurar desde snapshot local (caso más simple)

```bash
# 1. Listar snapshots disponibles
ssha agent_ro@192.168.31.91 'sudo -n zfs list -t snapshot -o name,creation,used -H | grep aranea_storage'

# 2. Verificar contenido del snapshot antes de rollback
ssha agent_ro@192.168.31.91 'sudo -n ls /mnt/pool0/aranea_storage/.zfs/snapshot/<snap-name>/'

# 3. Opción A: rollback destructivo (vuelve el dataset al estado del snapshot, datos entre snapshot y ahora SE PIERDEN)
ssha agent_ro@192.168.31.91 'sudo -n zfs rollback pool0/aranea_storage@<snap-name>'
# ⚠️ Requiere ticket approved. Borra snapshots más nuevos.

# Opción B: restaurar archivos individuales (ver Procedimiento 3)

# Opción B alternativa: clonar el snapshot como dataset nuevo
ssha agent_ro@192.168.31.91 'sudo -n zfs clone pool0/aranea_storage@<snap-name> pool0/aranea_storage_recovered'
# Ahora tenés una copia accesible en /mnt/pool0/aranea_storage_recovered
```

### 2.3 Restaurar desde off-host (kronos o VPS)

```bash
# 1. Verificar que la copia off-host existe y está sana
ssha agent_ro@192.168.31.120 'sudo -n zfs list -t all | grep pool0_recv'
# o
ssh -i "$OFFHOST_KEY" backup@offhost 'ls /backup/pool0/recv/aranea_storage@*/'

# 2. Identificar snapshot a restaurar
SNAP="pool0/aranea_storage@weekly-2026-06-29"

# 3. Recevir el snapshot al truenas (dry-run primero con -n)
ssha agent_ro@192.168.31.120 "sudo -n zfs send -R $SNAP" | \
  ssha agent_ro@192.168.31.91 'sudo -n zfs recv -v pool0/aranea_storage_restored'

# 4. Validar
ssha agent_ro@192.168.31.91 'sudo -n zfs list -t all | grep aranea_storage_restored'
ssha agent_ro@192.168.31.91 'sudo -n ls /mnt/pool0/aranea_storage_restored/'

# 5. Si todo OK, swap:
ssha agent_ro@192.168.31.91 'sudo -n zfs rename pool0/aranea_storage pool0/aranea_storage_broken_$(date +%Y%m%d)'
ssha agent_ro@192.168.31.91 'sudo -n zfs rename pool0/aranea_storage_restored pool0/aranea_storage'

# 6. Verificar NFS/SMB sirve el nuevo dataset
ssha agent_ro@192.168.31.91 'sudo -n midclt call smb.get_smb_shares'  # o reiniciar servicio SMB
```

### 2.4 Validación

- [ ] `zfs list` muestra el dataset restored
- [ ] `ls /mnt/pool0/<dataset>/` muestra archivos esperados
- [ ] SMB/NFS clients pueden acceder
- [ ] `zpool scrub` retorna 0 errores

### 2.5 Rollback

| Escenario | Rollback |
|---|---|
| Restore incompleto | `zfs destroy` del dataset restored, intentar de nuevo |
| Dataset restored está vacío | Verificar snapshot origen (puede estar corrupto upstream) |
| NFS/SMB no sirve el nuevo dataset | Reiniciar servicio: `midclt call service.restart cifs` |

---

## 📋 Procedimiento 3: Restore single file from ZFS snapshot

### 3.1 Escenario

Usuario borró o corrompió un archivo individual dentro de un dataset ZFS. Necesita recuperar la versión anterior.

### 3.2 Procedimiento (instantáneo, read-only por default)

```bash
# 1. Identificar el snapshot que contiene la versión buena
ssha agent_ro@192.168.31.91 'sudo -n zfs list -t snapshot -o name,creation -H | grep aranea_storage'
# Ej: pool0/aranea_storage@daily-2026-06-28

# 2. Navegar al snapshot (es accesible via .zfs)
ssha agent_ro@192.168.31.91 'sudo -n ls -la /mnt/pool0/aranea_storage/.zfs/snapshot/daily-2026-06-28/path/to/file.txt'

# 3. Copiar el archivo restaurado a la ubicación original
ssha agent_ro@192.168.31.91 'sudo -n cp -a /mnt/pool0/aranea_storage/.zfs/snapshot/daily-2026-06-28/path/to/file.txt /mnt/pool0/aranea_storage/path/to/file.txt'

# 4. Validar
ssha agent_ro@192.168.31.91 'sudo -n ls -la /mnt/pool0/aranea_storage/path/to/file.txt'
ssha agent_ro@192.168.31.91 'sudo -n sha256sum /mnt/pool0/aranea_storage/path/to/file.txt'
```

### 3.3 Variante: restaurar directorio completo

```bash
ssha agent_ro@192.168.31.91 'sudo -n cp -a /mnt/pool0/aranea_storage/.zfs/snapshot/daily-2026-06-28/path/to/dir/. /mnt/pool0/aranea_storage/path/to/dir/'
```

### 3.4 Validación

- [ ] Archivo existe en destino
- [ ] Permisos correctos
- [ ] Contenido coincide con versión del snapshot (`diff` si hay duda)
- [ ] Aplicación que lo usa funciona

### 3.5 Rollback

N/A — el snapshot original sigue accesible, no se modifica nada.

### 3.6 Casos especiales

| Caso | Solución |
|---|---|
| Snapshot no existe | Tomar uno ahora (`zfs snapshot`) y restaurar desde off-host (Procedimiento 2) |
| Archivo está en Ceph RBD (no ZFS) | Usar `rbd snap rollback` (ver más abajo) |
| Archivo está en LVM (no ZFS) | Usar LVM snapshot o backup vzdump |

### 3.7 Variante Ceph RBD (para imágenes RBD)

```bash
# 1. Listar snapshots
ssha agent_ro@192.168.31.120 'sudo -n rbd snap ls pool1/<image-name>'

# 2. Verificar contenido del snapshot (mapearlo como device)
ssha agent_ro@192.168.31.120 'sudo -n rbd snap protect pool1/<image-name>@<snap>'
ssha agent_ro@192.168.31.120 'sudo -n rbd clone pool1/<image-name>@<snap> pool1/<image-name>_recovered'

# 3. Montar el clon
ssha agent_ro@192.168.31.120 'sudo -n rbd map pool1/<image-name>_recovered'
mount /dev/rbd0 /mnt/recovered

# 4. Copiar archivo
cp /mnt/recovered/path/to/file /tmp/

# 5. Cleanup
umount /mnt/recovered
ssha agent_ro@192.168.31.120 'sudo -n rbd unmap /dev/rbd0'
ssha agent_ro@192.168.31.120 'sudo -n rbd rm pool1/<image-name>_recovered'
ssha agent_ro@192.168.31.120 'sudo -n rbd snap unprotect pool1/<image-name>@<snap>'
```

---

## 📋 Procedimiento 4: Restore entire Proxmox node from scratch

### 4.1 Escenario

Nodo físico (ej: hades) murió completamente. Necesito reconstruir hades desde cero con todas sus VMs.

> **Esto requiere**: pre-incidente con off-host copy ZFS de los datasets truenas, PBS datastore accesible desde otro nodo, etc. Si no hay nada de esto, este procedimiento es **parcial** — recoverable solo lo que esté en PBS.

### 4.2 Fases

#### Fase A: Reinstalar PVE en el nodo físico (intervención manual)

1. Booteo desde USB con ISO de Proxmox VE 8.4.x
2. Instalar con la misma IP, hostname, red
3. Agregar el nodo al cluster: `pvecm add 192.168.31.100` (asumiendo zeus como referencia)

#### Fase B: Restaurar configuraciones críticas (read-only desde backup)

```bash
# 1. Listar backups disponibles de /etc/pve
ssha agent_ro@192.168.31.100 'sudo -n ls -la /var/backups/etc-pve/'

# 2. Restaurar /etc/pve (NO destructivo: backup primero)
ssha agent_ro@192.168.31.10 'sudo -n cp -a /etc/pve /etc/pve.broken_$(date +%Y%m%d)'
ssha agent_ro@192.168.31.10 'sudo -n rsync -avh /var/backups/etc-pve/2026-MM-DD/ /etc/pve/'

# 3. Validar
ssha agent_ro@192.168.31.10 'sudo -n pvecm status'
ssha agent_ro@192.168.31.10 'sudo -n ha-manager status'
```

#### Fase C: Restaurar VMs desde PBS

```bash
# 1. Listar todas las VMs que estaban en hades (de documentación previa)
# Ver [[../01-topologia/nodo-hades]] § VMs corriendo

# 2. Restaurar cada VM (procedimiento del Procedimiento 1)
# VMID 145 (truenas) PRIMERO — es la más crítica
ssha agent_ro@192.168.31.120 'sudo -n qmrestore <backup-truenas> 145 --storage pool1 --force'

# 3. Arrancar truenas (si los discos QEMU están disponibles localmente)
# ⚠️ Si hades es nuevo, los QEMU disks de truenas NO existen — truenas arranca sin pool0/pool2
ssha agent_ro@192.168.31.10 'sudo -n qm start 145'
sleep 120

# 4. Restaurar pool0/pool2 desde off-host (zfs recv)
ssha agent_ro@192.168.31.120 "sudo -n zfs send -R backup/pool0_recv/pool0@<snap>" | \
  ssha agent_ro@192.168.31.145 'sudo -n zfs recv -v pool0_restored'

# Renombrar (ver Procedimiento 2 § 2.3)

# 5. Restaurar el resto de las VMs de hades (una por una)
for vmid in 124 125 133 134 140 144 152 153 157 158 159 160 105; do
  echo "Restoring VM $vmid..."
  ssha agent_ro@192.168.31.120 "sudo -n qmrestore <backup-$vmid> $vmid --storage pool1 --force"
done

# 6. Arrancar todas
for vmid in 124 125 133 134 140 144 152 153 157 158 159 160 105; do
  ssha agent_ro@192.168.31.120 "sudo -n qm start $vmid"
done

# 7. Restaurar LXCs
for ctmpl in 103 113 116 126 127 129 137 141 147 148; do
  ssha agent_ro@192.168.31.120 "sudo -n pct restore $ctmpl /var/backups/lxc-$ctmpl.tar.zst --storage local-lvm"
done
```

#### Fase D: Validación completa

```bash
# Cluster completo
ssha agent_ro@192.168.31.100 'sudo -n pvecm nodes'
ssha agent_ro@192.168.31.100 'sudo -n pvesm status'

# VMs
ssha agent_ro@192.168.31.90 'sudo -n qm list'

# Ceph
ssha agent_ro@192.168.31.120 'sudo -n ceph status'

# NFS
mount | grep nfs-storage  # en cada nodo

# Aplicaciones críticas (ejemplo mt4-real)
curl -s https://mt4.lab.aranea  # o el método que aplique
```

### 4.3 Tiempo total estimado

| Fase | Tiempo |
|---|---|
| A: Install PVE | 30 min |
| B: Restore /etc/pve | 10 min |
| C: Restore VMs (10 VMs) | 60 min |
| C: Restore truenas + pools | 60 min |
| C: Restore LXCs (10 LXCs) | 30 min |
| D: Validación | 30 min |
| **TOTAL** | **~3.5 h** |

### 4.4 Rollback

N/A en sentido estricto. Si falla la reconstrucción, el nodo queda en estado parcial. Documentar el fallo en ticket y consultar a Rodrigo.

### 4.5 Pre-requisitos para que este procedimiento funcione

- [ ] PBS con backups de las VMs de hades (configurar ANTES del incidente)
- [ ] Off-host ZFS copy de pool0/pool2 (configurar ANTES del incidente)
- [ ] Backup de /etc/pve accesible desde otro nodo (configurar ANTES)
- [ ] Imagen ISO de Proxmox disponible offline
- [ ] Hardware de repuesto para hades (CPU, RAM, motherboard)

Si alguno de estos falta → **no se puede recover hades completamente**. Solo recuperación parcial de lo que esté en PBS.

### 4.6 Tickets

- `YYYY-MM-DD-NNN-rebuild-hades-from-scratch.md` con timeline exhaustivo.

---

## 📋 Procedimiento 5: Restore Obsidian vault (CouchDB)

### 5.1 Escenario

CouchDB en `obsidian-sync` (lxc/116) está corrupta o perdida. El vault de Obsidian de Rodrigo no sincroniza.

### 5.2 Pre-flight

```bash
# Verificar estado de CouchDB
ssha agent_ro@192.168.31.90 'sudo -n pct enter 116'
# Dentro del LXC:
systemctl status couchdb
curl -s http://admin:<pw>@localhost:5984/_up
```

### 5.3 Restaurar desde dump CouchDB (recomendado)

```bash
# 1. Listar backups disponibles
ssha agent_ro@192.168.31.90 'sudo -n ls -la /var/backups/couchdb/'  # dentro del LXC
# o desde NFS si el backup está allí:
ssha agent_ro@192.168.31.91 'sudo -n ls -la /mnt/pool0/proxmox_storage/backups/couchdb/'

# 2. Stop CouchDB
ssha agent_ro@192.168.31.90 'sudo -n pct enter 116 systemctl stop couchdb'

# 3. Backup del estado actual (por si)
ssha agent_ro@192.168.31.90 'sudo -n pct enter 116 cp -a /var/lib/couchdb /var/lib/couchdb.broken_$(date +%Y%m%d)'

# 4. Restaurar dump
ssha agent_ro@192.168.31.90 'sudo -n pct enter 116 bash -c "
  rm -rf /var/lib/couchdb/*  # ⚠️ solo dentro del LXC, no es el host
  mkdir -p /var/lib/couchdb
  tar xzf /var/backups/couchdb/YYYY-MM-DD/couchdb-dump.tar.gz -C /var/lib/couchdb
  chown -R couchdb:couchdb /var/lib/couchdb
"'

# 5. Iniciar CouchDB
ssha agent_ro@192.168.31.90 'sudo -n pct enter 116 systemctl start couchdb'
sleep 30

# 6. Validar
ssha agent_ro@192.168.31.90 'sudo -n pct enter 116 curl -s http://admin:<pw>@localhost:5984/_all_dbs'
```

### 5.4 Restaurar replicando desde cliente Obsidian (alternativa)

> Si hay al menos un cliente Obsidian con copia local completa del vault, se puede usar como fuente de replicación.

```bash
# Desde un cliente Obsidian con Self-hosted LiveSync configurado:
# 1. Apuntar la URL a una CouchDB recién instalada (sin datos)
# 2. El cliente detecta DB vacía y sube todo el vault
# 3. Una vez sincronizado, otros clientes pueden reconectar
```

### 5.5 Validación

| Check | Esperado | Comando |
|---|---|---|
| CouchDB arriba | ✅ | `systemctl status couchdb` |
| Lista DBs | muestra `obsidian`, `obsidian-sync-*` | `curl -s http://admin:<pw>@localhost:5984/_all_dbs` |
| Conteos | No 0 documentos | `curl -s http://admin:<pw>@localhost:5984/obsidian` debe mostrar `doc_count > 0` |
| Cliente sincroniza | ✅ | Abrir Obsidian en escritorio, verificar sync |

### 5.6 Rollback

- Si restore no funciona → `rm -rf /var/lib/couchdb && mv /var/lib/couchdb.broken_YYYYMMDD /var/lib/couchdb && systemctl start couchdb`
- El backup pre-restore quedó en `couchdb.broken_YYYYMMDD`.

### 5.7 Tickets

- `YYYY-MM-DD-NNN-restore-obsidian-vault.md`

---

## ✅ Resumen de tiempos objetivo (RTO)

| Procedimiento | RTO |
|---|---|
| Restore single file ZFS snapshot | < 5 min |
| Restore VM from PBS | < 30 min |
| Restore ZFS dataset from snapshot | < 30 min |
| Restore ZFS dataset from off-host | < 60 min |
| Restore Obsidian vault | < 30 min |
| Restore entire Proxmox node | < 4 h |

## 📊 RPO (data loss tolerable)

| Asset | RPO actual | RPO target |
|---|---|---|
| Ceph RBD VMs | 24 h (vzdump daily) | < 1 h (con snapshot Ceph cada hora) |
| TrueNAS pool0 datasets | 24 h (daily snap) | < 1 h (con sanoid hourly) |
| TrueNAS pool2 datasets | 24 h (daily snap) | < 1 h (idem) |
| CouchDB | 24 h (daily dump) | < 1 h (con replicación continua) |
| PostgreSQL | 24 h (pg_dump) | < 5 min (con streaming replication) |
| MongoDB | 24 h (mongodump) | < 5 min (con replica set) |

> **Recomendación**: mejorar RPO con streaming replication PostgreSQL/MongoDB cuando se implemente off-host (ver [[../03-storage/BACKUP-SYSTEM]] § TODO).

---

## Captured

2026-06-30. Diseñado por Hermes Task 2 (ticket [[../05-tickets/2026-06-30-011-aranea-storage-audit-backup]]).

## Validación

- Verificar precondiciones y resultados del procedimiento antes de declarar éxito.
