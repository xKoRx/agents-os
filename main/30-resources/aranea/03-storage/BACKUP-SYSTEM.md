---
type: doc
schema_version: 1
status: active
area: "[[Aranea]]"
related: []
aliases: []
tags:
  - kind/doc
created: 2026-08-10
updated: 2026-08-10
---

# 🛡️ BACKUP-SYSTEM — Diseño del sistema de backup Aranea

## Propósito

Documentación canónica legacy de [[Aranea]]; se conserva el contenido histórico y su estado requiere verificación antes de uso operativo.

## Contenido


> **Diseñador**: Hermes (Task 2, ticket [[../05-tickets/2026-06-30-011-aranea-storage-audit-backup]])
> **Inputs**: [[AUDIT]] + inventario [[README]] + tickets 005/006/007/008
> **Datos**: 2026-06-28 21:18 UTC (drift 2 días al 2026-06-30)
> **Owner**: Rodrigo Jara · **Nivel**: homelab production-critical (incluye cuenta real MT4 + bases de datos)

---

## 1. 🎯 Amenazas (threat model Aranea-específico)

| # | Amenaza | Probabilidad | Impacto | Notas |
|---|---|---|---|---|
| T1 | **hades cae** (hardware, PSU, mobo) | Media (un solo host concentra 22 VMs + truenas) | **Catastrófico** | hades = SPOF del SPOF (ver [[AUDIT]] §9.1) |
| T2 | **TrueNAS VM no bootea** (metadata corruption, ZFS scrub error) | Media-baja (sin UPS, sin SMART continuo) | **Catastrófico** | Sin UPS → corte eléctrico = riesgo |
| T3 | **Disco único `sdg` de pool2 falla** | Alta (HDD consumer 8 TB, sin mirror, sin scrub hace 11 meses) | **Catastrófico** | Pierde TODOS los backups actuales |
| T4 | **Ceph pierde 2 OSDs simultáneamente** | Baja (3× replica) | Alto (datos en pool1) | Necesita resilvering rápido |
| T5 | **OS reinstall / config drift** en un PVE node | Media | Medio | /etc/pve, red, ssh keys |
| T6 | **Accidental delete** (rm -rf, droplet Destroy) | Media | Variable | Snapshots son la defensa |
| T7 | **Ransomware** en VM accesible | Baja-Media (homelab, sin endpoint protection) | **Catastrófico** | Sin segmentación ni EDR |
| T8 | **step-ca compromise** (clave privada robada) | Baja | Alto | Emite certs válidos para *.lab.aranea |
| T9 | **Obsidian vault corrupto / CouchDB dañada** | Baja | Medio (research + runbooks) | Sin replicación |
| T10 | **Nodo Proxmox se cae** (zeus/hera/kronos) | Baja (corosync quorum 3/5) | Medio | Ceph sobrevive, VMs migradas |
| T11 | **UPS STOPPED + corte eléctrico** | Media (sísmico Chile) | Alto (ZFS corruption) | truenas sin UPS |
| T12 | **Cable de red 10GbE se suelta / switch falla** | Baja | Medio | bond failover cubre slave |

---

## 2. 📐 Regla 3-2-1 aplicada a Aranea

> **3 copias** · **2 medios distintos** · **1 copia off-host**

| Componente | Hoy (2026-06-30) | Target | Gap |
|---|---|---|---|
| **Copia 1 (producción)** | Disco principal (Ceph RBD / ZFS pool0 / pool2) | ✅ existe | — |
| **Copia 2 (mismo host)** | `pool2/backup/*` (cuando existe) | ✅ parcial | Solo trading_systems y aranea_storage |
| **Copia 3 (off-host)** | ❌ **NO EXISTE** | 🔴 TARGET PRINCIPAL | 🔴 Crítico |

### 2.1 Política de retención propuesta

| Frecuencia | Snapshots ZFS locales | Off-host | Retención |
|---|---|---|---|
| **Cada 15 min** | — | — | (no necesario para homelab) |
| **Hourly** | Snapshots de datasets críticos | — | 24 h |
| **Daily** | Snapshot ZFS todos los datasets pool0 | `zfs send` a off-host | 7 días |
| **Weekly** | Snapshot semanal | `zfs send` weekly a off-host | 4 semanas |
| **Monthly** | Snapshot mensual | off-host | 12 meses |
| **Yearly** | Snapshot anual | off-host (encriptado) | 5 años |

### 2.2 Codificación de la regla 3-2-1

```
┌──────────────────────────────────────────────────────────────────┐
│ Aranea hoy (2026-06-30)                                         │
│                                                                  │
│ pool0 (mirror SSD)   ───┐                                        │
│                          ├─ mismo host (hades)                   │
│ pool2 (single HDD)   ───┘                                        │
│                                                                  │
│ ❌ NO off-host copy                                              │
└──────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│ Aranea target (post-implementación)                              │
│                                                                  │
│ pool0 (mirror SSD) ───┐                                          │
│                       ├─ mismo host (hades)                      │
│ pool2 (single HDD) ───┘                                          │
│       │                                                          │
│       │ zfs send / zfs recv                                      │
│       ▼                                                          │
│ off-host: kronos local-sqx-kronos (931 GB libre)  ← 2do medio    │
│       │                                                          │
│       │ rsync / rclone crypt                                     │
│       ▼                                                          │
│ off-host-2: USB externo o NAS / VPS  ← 3er medio + fuera sitio   │
└──────────────────────────────────────────────────────────────────┘
```

---

## 3. 🎯 Estrategia per-asset

### 3.1 Ceph `pool1` (RBD)

| Aspecto | Decisión |
|---|---|
| **Snapshots Ceph** | `ceph mds snap` no aplica a RBD. Usar `rbd snap create <pool>/<image>@<snap>` por VM. |
| **Cadencia** | Diario 02:00 (cron) para cada imagen RBD |
| **Retención local** | 7 daily + 4 weekly |
| **Off-host** | `rbd export` → archivo → `rclone copy` a off-host (weekly) |
| **Validación** | Mensual: `rbd import` en VM de prueba + boot test |

```bash
# Ejemplo de snapshot diario (a integrar en cron en zeus/hera/kronos)
POOL=pool1
IMAGES=$(rbd ls $POOL)
TS=$(date +%Y%m%d-%H%M)
for img in $IMAGES; do
  rbd snap create "$POOL/$img@daily-$TS"
  rbd snap protect "$POOL/$img@daily-$TS"  # para poder clonar/exportar
done

# Retención: borrar snapshots > 7 días
rbd snap ls "$POOL/$img" | awk '/daily-/ {print $2}' | \
  while read snap; do
    d=$(echo "$snap" | sed 's/daily-//')
    age_days=$(( ($(date +%s) - $(date -d "$d" +%s)) / 86400 ))
    [ $age_days -gt 7 ] && rbd snap rm "$POOL/$img@$snap"
  done
```

### 3.2 TrueNAS `pool0` (ZFS mirror)

| Aspecto | Decisión |
|---|---|
| **Snapshots ZFS** | `zfs-auto-snapshot` o `sanoid` con retention policy |
| **Cadencia local** | Daily (keep 7) + Weekly (keep 4) + Monthly (keep 12) |
| **Off-host** | `zfs send -R pool0@weekly-snap \| ssh backup-host zfs recv backup/pool0` |
| **Target off-host preferido** | `kronos` → VG `local-sqx-kronos` tiene **931 GB libres** (no usado, según [[../01-topologia/nodo-kronos]]). Crear ZFS pool local en kronos para recibir. |

```bash
# Daily snapshot recursivo en truenas (cron en truenas, vía midclt o zfs)
ssh agent_ro@192.168.31.91 "
  for ds in aranea_storage proxmox_storage trading_systems trading_documents; do
    zfs snapshot pool0/\$ds@daily-\$(date +%Y%m%d)
  done
"

# Replicación a kronos (vía SSH + zfs send/recv)
LATEST=$(ssh agent_ro@192.168.31.91 "zfs list -t snap -o name -H | grep 'daily-' | sort | tail -1 | awk '{print \$1}'")
ssh agent_ro@192.168.31.91 "zfs send -R $LATEST" | \
  ssh root@kronos "zfs recv backup/pool0/recv"
```

### 3.3 TrueNAS `pool2` (ZFS single disk — backups)

| Aspecto | Decisión |
|---|---|
| **Crítico** | `pool2` **NO es backup, es segundo pool en mismo host**. Tratarlo como storage temporal. |
| **Snapshots ZFS** | Igual que pool0 |
| **Off-host** | **PRIORITARIO**: replicar TODO `pool2/backup/*` a off-host antes que cualquier otra cosa |
| **Migración a mirror** | Pendiente mediano plazo (agregar disco a hades, attachear como vdev a pool2) |

### 3.4 VMs/LXCs en Proxmox

| Aspecto | Decisión |
|---|---|
| **Snapshots Proxmox** | `vzdump` a `nfs-storage` (truenas) — ya configurado |
| **Cadencia** | Diario 03:00 para VMs críticas (mt4-real, postgres, mongo, ubuntu-dev, truenas, obsidian-sync); Semanal para el resto |
| **PBS (Proxmox Backup Server)** | **Recomendado**: instalar PBS en LXC de kronos (32+ GB RAM libre). Datastore en VG local. Backups deduplicados + compresión + verificación de integridad nativa. |
| **Off-host** | PBS sync job a remote (kronos → hera, o kronos → USB) |

```bash
# Configurar PBS en kronos (nuevo LXC o VM)
# Paso 1: añadir storage PBS
pvesm add pbs backup-pbs --server 10.10.10.120 --datastore main \
  --username backup@pbs --password <secret> --content backup

# Paso 2: configurar vzdump schedule
# /etc/pve/jobs.cfg
vzdump: weekly-all
        schedule sat 02:00
        all 1
        storage backup-pbs
        prune-backups keep-daily=7,keep-weekly=4,keep-monthly=12
        notification-mode notification-system
```

### 3.5 Configuraciones (Traefik, OPNsense, step-ca, /etc/pve, ssh)

| Asset | Cómo | Cadencia | Off-host |
|---|---|---|---|
| **Traefik dynamic config** | `tar czf` de `/etc/traefik/` + `/etc/traefik.d/` | Daily 04:00 | `rclone copy` a off-host |
| **step-ca** ⚠️ crítico (claves privadas) | `step ca backup` (oficial) | Daily + antes de cualquier cambio | Off-host encriptado (`age`/`gpg`) |
| **OPNsense config** | UI: System → Backup → Download (XML) | Weekly + pre/post change | Off-host |
| **/etc/pve** (PVE cluster) | `tar czf` de `/etc/pve/` | Weekly | Off-host |
| **SSH host keys + agent_ro pubkey** | Copia de `/etc/ssh/` y `~/.ssh/` | Mensual (con cambio manual) | Off-host encriptado |
| **etcd cluster** | `etcdctl snapshot save` (los 5 miembros tienen quorum, snapshot de cualquiera) | Daily 05:00 | Off-host |

### 3.6 Obsidian vault / CouchDB (lxc/116 en hades)

| Aspecto | Decisión |
|---|---|
| **CouchDB dump** | Script en obsidian-sync: `curl -X POST http://admin:<pw>@localhost:5984/_replicate` o replicación nativa |
| **Local snapshot** | Snapshot del LXC vía Proxmox (vzdump) |
| **Off-host** | `curl` dump + `rclone copy` |
| **Cadencia** | Hourly (vault cambia frecuente) |

### 3.7 minio (qemu/157 en hades)

| Aspecto | Decisión |
|---|---|
| **minio mc mirror** | `mc mirror --remove --overwrite source/bucket dest/bucket` |
| **Off-host** | A otro minio remoto, o `rclone copy` con `--s3` |
| **Cadencia** | Daily (S3-compatible → cambia frecuente) |

### 3.8 Bases de datos

| DB | Cómo | Cadencia | Off-host |
|---|---|---|---|
| **PostgreSQL (qemu/152)** | `pg_dumpall -f /var/lib/postgresql/dump.sql` + cron | Daily 01:00 | `/mnt/pool0/proxmox_storage/backups/db/` |
| **MongoDB (qemu/153)** | `mongodump --gzip --archive=...` | Daily 01:30 | Mismo path |
| **Streaming replication PG** | A kronos (recomendado mediano plazo) | Continuo | — |

---

## 4. 🏗️ Proxmox Backup Server (PBS) — candidato recomendado

### 4.1 Hardware target

| Opción | Pros | Contras | Recomendación |
|---|---|---|---|
| **A. LXC en kronos** | kronos libre (222 GB RAM, 931 GB local-sqx-kronos libre) | PBS necesita ZFS, no funciona en LXC (necesita acceso raw disk) | ❌ No viable |
| **B. VM nueva en kronos** | Recursos充沛; isolación; bare-metal-equivalent | Consume vCPU/RAM de kronos | ✅ Recomendado |
| **C. LXC privilegiada en hades** | Storage cercano (pool2) | hades SPOF | ❌ Peor caso |
| **D. ZFS pool nuevo en kronos** | Aprovecha NVMe libre | Requiere configurar vdevs | ✅ Mejor |

**Recomendación final**: VM PBS en kronos con un nuevo ZFS pool sobre `nvme1n1` (931 GB libre) o espejo de 2× NVMe. vzdump deduplica + comprime + verifica automáticamente.

### 4.2 Setup sketch

```bash
# 1. Crear VM PBS (qemu/200 por ejemplo) en kronos
# 2. Dentro de PBS:
proxmox-backup-manager datastore create main --path /backup/main --prune-backups keep-daily=7,keep-weekly=4,keep-monthly=12
proxmox-backup-manager user create backup@pbs --comment "PBS backup user"
proxmox-backup-manager user update backup@pbs --password <STRONG>

# 3. En cada PVE node, registrar storage PBS:
pvesm add pbs aranea-pbs \
  --server 192.168.31.120 \
  --datastore main \
  --username backup@pbs \
  --password <STRONG> \
  --content backup \
  --prune-backups keep-daily=7,keep-weekly=4,keep-monthly=12 \
  --notification-mode notification-system

# 4. Schedule:
cat >> /etc/pve/jobs.cfg <<'EOF'
vzdump: daily-critical
        schedule mon..sun 02:00
        vmid 124,125,133,134,144,145,152,153,159,157,116
        storage aranea-pbs
        mode snapshot
        notification-mode notification-system

vzdump: weekly-all
        schedule sat 04:00
        all 1
        storage aranea-pbs
        prune-backups keep-daily=7,keep-weekly=4,keep-monthly=12
        notification-mode notification-system
EOF
```

### 4.3 PBS sync a off-host

```bash
# En PBS VM, configurar sync job (manual o vía GUI)
proxmox-backup-manager sync-job create aranea-pbs-remote \
  --remote off-host-server \
  --remote-user backup@pbs \
  --remote-password <STRONG> \
  --schedule "daily 06:00" \
  --remove-vanished
```

---

## 5. 🔐 Cifrado y transporte

### 5.1 Encryption at rest

| Asset | Método | Notas |
|---|---|---|
| Off-host backups (USB / VPS) | LUKS sobre disco, o `rclone crypt` (AES-256) | Llave en `~/.config/rclone/rclone.conf` + passphrase en bitwarden offline |
| step-ca keys | `age` encryption (X25519) | Llave pública para cifrar, privada en escrow offline |
| SSH agent_ro key | Passphrase + escrow USB cifrado | Ya es clave SSH, agregar passphrase fuerte |
| Snapshots ZFS locales | Nativo ZFS (no necesario cifrar en disco) | OK si disco no sale del cluster |

### 5.2 Encryption in transit

| Tramo | Método | Implementación |
|---|---|---|
| truenas → kronos (zfs send) | SSH sobre LAN | `ssh -C` (compresión) + `-c aes256-gcm@openssh.com` |
| PVE → PBS (vzdump) | TLS nativo PBS | Puerto 8007, certificado autofirmado OK para LAN |
| rclone → VPS | TLS 1.3 | `rclone copy --checkers 4 --transfers 2` |
| rsync USB | Sin cifrar (escritura física) | Cifrar disco con LUKS antes |

### 5.3 Llaves y secretos

| Llave | Storage primario | Storage secundario |
|---|---|---|
| step-ca provisioner password | step-ca VM (`/root/.step/`) | Bitwarden offline + USB cifrado |
| SSH agent_ro private key | `~/.ssh/agent_ro_aranea` (en hermes-vm) | USB cifrado en caja fuerte |
| PBS user password | PBS VM + PVE storage config | Bitwarden offline |
| rclone crypt passphrase | `~/.config/rclone/rclone.conf` (en off-host) | Bitwarden offline |
| OPNsense API key | OPNsense VM | Bitwarden offline |

---

## 6. ⏰ Cadencias — cronograma consolidado

```mermaid
gantt
    title Backup schedule (hora local Chile)
    dateFormat HH:mm
    axisFormat %H:%M

    section Hourly
    Obsidian vault (CouchDB)    :h1, 00, 5m
    section Daily
    PostgreSQL dump             :d1, 01:00, 30m
    MongoDB dump                :d2, after d1, 30m
    Ceph RBD snapshots          :d3, 02:00, 60m
    vzdump critical VMs (PBS)   :d4, after d3, 60m
    ZFS snapshot pool0          :d5, after d4, 30m
    Traefik config backup       :d6, after d5, 5m
    step-ca backup              :d7, after d6, 5m
    minio mirror                :d8, after d7, 30m
    zfs send pool0 → kronos     :d9, after d8, 60m
    ZFS snapshot pool2          :d10, after d9, 30m
    zfs send pool2 → kronos     :d11, after d10, 60m
    PBS sync → off-host         :d12, after d11, 60m
    section Weekly
    vzdump ALL VMs (PBS)        :w1, sat, 04:00, 4h
    OPNsense config export      :w2, sat, 08:00, 30m
    /etc/pve backup             :w3, sat, after w2, 30m
    etcd snapshot               :w4, sun, 03:00, 30m
    section Monthly
    Scrub pool0                 :m1, 1st, 02:00, 4h
    Scrub pool2                 :m2, after m1, 12h
    Restore drill               :m3, 15th, 4h
```

### 6.1 Tabla resumen

| Job | Qué | Dónde | Cuándo | Retención |
|---|---|---|---|---|
| Hourly | Obsidian vault dump | hades lxc/116 | `:00` | 24 h local + 30 d off-host |
| Daily | PG/Mongo dump | hades VMs 152/153 | 01:00-02:00 | 7 d local + 90 d off-host |
| Daily | Ceph RBD snap + export | zeus/hera/kronos | 02:00 | 7 d + 4 w |
| Daily | vzdump critical VMs → PBS | PBS kronos | 03:00 | 7 d + 4 w + 12 m |
| Daily | ZFS snap pool0/pool2 | truenas | 04:00 | 7 d + 4 w + 12 m |
| Daily | zfs send → kronos recv | truenas → kronos | 05:00 | 30 d |
| Daily | PBS sync → off-host | PBS → off-host | 06:00 | match PBS |
| Daily | Traefik + step-ca + minio mirror | varios | 05:00 | 30 d |
| Weekly | vzdump ALL VMs | PBS kronos | Sat 04:00 | 4 w |
| Weekly | OPNsense + /etc/pve + etcd | athena + cluster | Sat 08:00 | 12 w |
| Monthly | Scrub pool0 + pool2 | truenas | día 1 | — |
| Monthly | Restore drill (1 VM completa) | PBS kronos | día 15 | — |
| Yearly | Snapshot anual archivo | off-host encriptado | 31-Dic | 5 y |

---

## 7. 💾 Storage targets — dónde vive cada copia

### 7.1 Off-host primario recomendado: **kronos**

| Recurso kronos | Disponible | Uso propuesto |
|---|---|---|
| 222 GB RAM libres | ✅ | PBS VM (4 vCPU / 8 GB) |
| 931 GB `local-sqx-kronos` (libre, ver [[../01-topologia/nodo-kronos]]) | ✅ | ZFS pool `backup-arrival` |
| NVMe slots libres (kronos tiene 2× NVMe 931 GB usados como OSD) | ❌ todos usados | Agregar NVMe dedicado si más capacidad |

**Riesgo**: kronos está en **el mismo sitio físico** que hades. Es off-host del storage target, pero **no es off-site**. Para DR real (terremoto, incendio) → falta capa 3.

### 7.2 Off-host secundario recomendado: **USB cifrado o VPS**

| Opción | Costo | Capacidad | Latencia | Notas |
|---|---|---|---|---|
| **A. Disco USB 4-8 TB cifrado LUKS** | $100-200 USD one-time | 4-8 TB | USB 3.0 | Rotación semanal al sitio Rodrigo. Necesita script de rotación. |
| **B. VPS storage** (Hetzner Storage Box, Backblaze B2) | $5-10 USD/mes | 1 TB+ | WAN | `rclone crypt` para cifrar. Requiere WAN estable. |
| **C. NAS secundario en casa** (si existe) | $0 si hay HW | variable | LAN | Ideal pero requiere HW |

**Recomendación**: A (USB) para empezar, B como upgrade.

### 7.3 Capa 3 (opcional): rotación a segundo sitio físico

- Llevar USB semanalmente a oficina/casa de familiar
- O usar proveedor de cloud con geo-replicación (Backblaze B2 + bucket replicado a EU si VPS en US)

---

## 8. 🧪 Plan de restore drill

> **Regla**: un backup no probado no es backup. Mínimo 1 restore drill mensual.

| Asset class | Procedimiento | Frecuencia | Target tiempo |
|---|---|---|---|
| **VM completa** | Restore vzdump desde PBS → crear VM nueva → boot → verificar network + servicios | Mensual (VM distinta cada mes, rotar) | < 30 min |
| **Dataset ZFS** | `zfs recv` snapshot de off-host → mount → verificar integridad con `zpool scrub` | Mensual | < 20 min |
| **Archivo único** | Navegar `.zfs/snapshot/` en truenas o `rbd snap rollback` | Mensual | < 5 min |
| **Proxmox node scratch** | Reinstall PVE en nodo vacío → aplicar `/etc/pve` backup → restaurar VMs desde PBS → verificar quórum | **Trimestral** | < 4 h |
| **Obsidian vault** | Restaurar CouchDB dump → verificar replicación inicial | Trimestral | < 30 min |
| **step-ca** | Reinstall step-ca → restore `step ca backup` → verificar emisión de certs | **Semestral** | < 1 h |

Ver [[recovery-procedures]] para scripts detallados.

---

## 9. ❌ Lo que NO está cubierto (gaps explícitos)

| Gap | Riesgo | Mitigación temporal |
|---|---|---|
| **Off-host copy encriptado**: no implementado | Robo de disco USB = leak | Cifrar LUKS desde día 1 |
| **Restore drill**: nunca ejecutado | Primer restore será caótico | Hacer el primero el próximo sábado |
| **UPS**: truenas `ups STOPPED` | Corte eléctrico = corrupción ZFS | Comprar UPS $100-200, configurar NUT |
| **Replicación streaming PostgreSQL** | DB production punto único | Pendiente (kronos tiene RAM de sobra) |
| **Replica set MongoDB** | DB production punto único | Pendiente |
| **OPNsense HA** (CARP) | athena SPOF red | Pendiente (fuera de scope storage) |
| **Migrar TrueNAS a bare-metal** | hades SPOF SPOF | Pendiente (alto esfuerzo) |
| **Cifrado de snapshots locales** | Disco robado = leak | OK si disco no sale del cluster; cifrar USB sí |
| **Monitoring de backups** (alertas si fallan) | Backup falla silenciosamente | Configurar `notification-mode` en PVE + cron con exit codes + watchdog |
| **Disaster Recovery plan escrito y probado** | Sin runbook, improvisation | ESTE doc + [[../04-backups/recovery-procedures]] |

---

## 10. 📋 TODO — implementación

| # | Acción | Responsable | ETA sugerido |
|---|---|---|---|
| 1 | **Decidir target off-host primario** (kronos local-sqx-kronos vs USB vs VPS) | Rodrigo | Esta semana |
| 2 | **Configurar SSH agent_ro NOPASSWD** en 5/6 nodos | Rodrigo (root manual) | Antes de implementar nada |
| 3 | `zpool scrub pool2` inmediato | Hermes | Hoy |
| 4 | `ceph tell osd.0/osd.2 compact` | Hermes | Hoy |
| 5 | Documentar política snapshots ZFS en truenas (`sanoid` config) | Hermes | Esta semana |
| 6 | Configurar vzdump schedule (vzdump en `nfs-storage` con prune-backups) | Hermes | Esta semana |
| 7 | Crear VM PBS en kronos + datastore `main` | Hermes | Próximo sábado |
| 8 | Configurar PBS sync job a off-host (cuando exista) | Hermes | Cuando (1) decidido |
| 9 | Documentar `step ca backup` + automatizar | Hermes | Esta semana |
| 10 | Crear `~/.ssh/agent_ro_aranea.pub` escrow USB cifrado | Rodrigo | Cuando (2) listo |
| 11 | Configurar UPS + NUT en truenas | Rodrigo (HW) + Hermes (config) | Próximo mes |
| 12 | Restore drill #1 (VM mt4-test desde PBS hipotético) | Hermes + Rodrigo | Una vez (7) listo |

---

## Source files

- [[AUDIT]]
- [[README]]
- [[inventory]]
- [[ceph-pool1]]
- [[truenas-pool0]]
- [[truenas-pool2]]
- [[nfs-shares]]
- [[smb-shares]]
- [[iscsi-target]]
- [[datasets]]
- [[../01-topologia/nodo-truenas]]
- [[../01-topologia/nodo-hades]]
- [[../01-topologia/nodo-kronos]]
- [[../02-servicios/backup-storage]]
- [[../02-servicios/bases-de-datos]]
- [[../02-servicios/dns-tls]]
- [[../02-servicios/trading]]
- [[../05-tickets/2026-06-29-005-install-step-ca]]

## Captured

**Datos**: 2026-06-28 21:18 UTC (drift 2 días al 2026-06-30).
**Diseñado**: 2026-06-30 por Hermes (Task 2, ticket [[../05-tickets/2026-06-30-011-aranea-storage-audit-backup]]).

## TODO

- Validar diseño contra decisión del owner sobre (a) off-host target, (b) ventana de restore drill, (c) presupuesto HW (UPS, USB, VPS).
- Cuando se ejecute el primer `zfs send` real contra kronos, documentar tamaño transferido + tiempo + tuning necesario (`-c aes256-gcm`, `-L`).
- Cuando se cree PBS VM, ajustar datastore path y prune policy según capacidad real disponible.
