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

# 🛡️ Aranea — Propuesta completa de Storage + Backup (iter 4)

## Propósito

Documentación canónica legacy de [[Aranea]]; se conserva el contenido histórico y su estado requiere verificación antes de uso operativo.

## Contenido


## Propósito

Conservar la consolidación histórica de la iteración 4 para revisión y provenance; fue supersedida por `BACKUP-DR-DESIGN` y no es autoridad vigente.

## Contenido

> **Para**: revisión por IA externa especialista en sistemas de backup.
> **Status**: iter 4, 6 decisiones resueltas, 2 pendientes nuevas.
> **Capex**: **$0** · **Opex mensual cloud**: **$0** (espacio ya contratado).
> **Restricciones del owner (no negociables)**:
> 1. Cero capex — usar solo lo que ya hay.
> 2. No migrar TrueNAS a bare-metal. hades se queda como hypervisor de truenas.
> 3. No cambiar cantidad de servidores. 5 Proxmox + truenas-vm-en-hades + hermes-vm.
> 4. **Los 3 SSDs `local-sqx-{zeus,hera,kronos}` son SAGRADOS** — dedicados a SQX (infraestructura Echo Forge).

---

## 0. Resumen ejecutivo (1 página)

**Cluster**: 5 Proxmox VE + 1 TrueNAS Scale (VM en hades) + 1 Hermes VM = 7 máquinas. 302 threads / 767 GB RAM / ~17.6 TB raw / ~9 TB usados (~51%).

**Diagnóstico**: el cluster **tiene capacidad de sobra** para un sistema de backup 3-2-1 decente. El problema es **organización**, no capacidad. Hoy `pool2` es single disk peligroso, no hay off-host real, no hay off-site, los backups son manuales o parciales, y la doc está dispersa.

**Recomendación en 4 puntos — todo con recursos existentes, $0**:

1. **PBS en VM nueva en kronos** sobre `local-kronos` (680 GB SSD libre). vzdump daily/weekly con dedup nativa.
2. **Tier cloud segregado**: `rclone crypt` sobre pcloud (1 TB, **solo configs/datos críticos**) + Google Drive (varios TB, **bulk snapshots ZFS pool0**).
3. **Aceptar pool2 single disk** + priorizar scrub mensual + replicación a cloud (no es backup real pero se mitiga).
4. **Sin capa on-cluster `zfs recv`** — los 3 SSDs `local-sqx-*` son sagrados para SQX (Echo Forge), no se pueden tocar.

**Trade-offs explícitos**:
- Sin `zfs recv` on-cluster = un único punto de fallo menos, pero perdemos redundancia ZFS local entre pools.
- pcloud escaso (1 TB) = obliga a elegir bien qué sube; configs/secretos sí, VMs enteras no.
- GDrive bulk = depende de WAN chilena (100-300 Mbps), `--bwlimit` nocturno.
- hades SPOF (truenas VM + 25 VMs) = aceptado por owner, no se mitiga. PBS off-host en kronos sobrevive si hades cae.

---

## 1. Cluster e infraestructura

### 1.1 Nodos

| Nodo | IP LAN | IP Ceph | Rol | CPU | RAM | Storage local clave |
|---|---|---|---|---|---|---|
| **athena** | 192.168.31.10 | — | Gateway + servicios de red | i7-13620H 16t | 16 GB | NVMe 476 GB (root + local-lvm) |
| **zeus** | 192.168.31.100 | 10.10.10.100 | Compute + Ceph MON/MGR + OSD.2 | Ryzen 9 5950X 32t | 94 GB | NVMe 931 GB (OSD.2), NVMe 465 GB (boot+local-lvm), **SSD 931 GB `local-sqx-zeus` (SAGRADO)** |
| **hera** | 192.168.31.110 | 10.10.10.110 | Compute + Ceph MON + OSD.0 | 2× Xeon E5-2699 v3 72t | 125 GB | NVMe 931 GB (OSD.0), NVMe 465 GB (boot+local-lvm), **SSD 931 GB `local-sqx-hera` (SAGRADO)** |
| **kronos** | 192.168.31.120 | 10.10.10.120 | Storage powerhouse + Ceph MON/MGR + OSD.1+3 | 2× Xeon E5-2698 v4 80t | 251 GB | NVMe 931 GB × 2 (OSD.1, OSD.3), **SSD 931 GB `local-sqx-kronos` (SAGRADO)**, SSD 931 GB `local-kronos` (680 GB libre), SSD 954 GB `pool-kronos` (730 GB libre), SSD 232 GB (boot) |
| **hades** | 192.168.31.90 | 10.10.10.90 | Compute-heavy + host de TrueNAS VM (25 VMs) | 2× Xeon E5-2697 v4 72t | 251 GB (74% usado) | NVMe 119 GB (boot), 2× NVMe 465 GB (truenas special mirror), **8× SSD 931 GB SATA (`sda-sdh`, todos en truenas pool0 mirror vdevs)**, HDD 7.3 TB (truenas pool2 single disk) |
| **truenas** (VM en hades) | 192.168.31.91 | — | Almacenamiento compartido | 2× Xeon E5-2697 v4 (virt) 30t | 32 GB | ZFS `pool0` (4 mirror SSD, 4.48 TB raw, 57% usado), ZFS `pool2` (single HDD, 7.99 TB raw, 44% usado, **sin redundancia**), boot-pool 30 GB |
| **hermes-vm** | 192.168.31.122 | — | Agente IA (este sistema) | — | — | — |

**Total**: 302 threads / 767 GB RAM / 55 VMs definidas (36 running, 19 stopped) / 4 OSDs Ceph activos / ~17.6 TB raw storage.

### 1.2 Storage detallado

#### Ceph pool1 (RBD distribuido)
- **3.6 TiB raw / 2.1 TiB usados (75% pool) / 1.6 TiB libre**
- **HEALTH_WARN**: fragmentación BlueStore >0.80 en osd.0/osd.2, slow ops en osd.3.
- 4 OSDs NVMe: osd.0 (hera), osd.1 (kronos), osd.2 (zeus), osd.3 (kronos).
- **hades weight 0** — no contribuye a Ceph, solo consume recursos.

#### TrueNAS pool0 (ZFS, 4 mirror SSD + 1 special mirror)
- **4.48 TB raw / 2.49 TB usados (57%) / 1.99 TB libre** ✅
- 4 mirror vdevs × 2 SSD 931 GB + 1 mirror special × 2 NVMe 465 GB.
- Hosts: NFS `proxmox_storage` (1.5 TB usado), SMB shares (`trading_systems` 485 GB, `aranea_storage` 998 GB, `trading_documents` 24 MB), datasets apps (postgresql, mongodb, frigate).

#### TrueNAS pool2 (ZFS, single disk HDD)
- **7.99 TB raw / 3.51 TB usados (44%) / 4.48 TB libre** ⚠️
- **HDD 7.3 TB consumer, sin mirror, scrub de hace 11 meses**.
- Hosts: `backup/trading_systems` (305 GB), `backup/aranea_storage` (39 GB), `iso_storage` (15 GB), `ix-applications` (apps nativas TrueNAS), `pool0_backup` (copia de pool0).

#### LVM locales
- `local-lvm` per-node (PVE root images): 58-429 GB.
- `local-sqx-{zeus,hera,kronos}` (931 GB × 3, WD Green SATA): **SAGRADOS** — datasets SQX (Echo Forge).
- `local-kronos` (931 GB, Samsung 870 QVO): 250 GB usados, **680 GB libre**.
- `pool-kronos` (954 GB, Crucial P3): 220 GB usados, **730 GB libre**.

#### iSCSI LUNs (de truenas)
- 5 LUNs exportados desde truenas (50 GB, 200 GB × 2, 32 GB × 2, 100 GB) montados como raw devices en otros nodos.

### 1.3 VMs running relevantes

| VMID | Nombre | Nodo | Status | vCPU | RAM | Notas |
|---|---|---|---|---|---|---|
| 108 | sqx-ulab-zeus-0 | zeus | **running** | 28 | 75 GB | Única SQX activa, usa `local-sqx-zeus` |
| 118 | agent | kronos | running | 4 | 8 GB | Hermes agent VM |
| 138 | kafka-kronos | kronos | running | 4 | 8 GB | Broker Kafka |
| 152 | postgresql | hades | running | — | 24 GB | DB |
| 153 | mongodb | hades | running | — | 24 GB | DB |
| 140 | echo | hades | running | 4 | 8 GB | Echo API |
| 158 | temporal | hades | running | 4 | 8 GB | Workflow engine |
| 160 | argus | hades | running | 8 | 16 GB | (¿monitoreo IA?) |
| 159 | ubuntu-dev | hades | running | 24 | 64 GB | Workstation Rodrigo |
| 111 | sqx-ulab-kron-0 | kronos | **stopped** | 76 | 137 GB | SQX en mantenimiento |
| 123 | sqx-ulab-hera-0 | hera | **stopped** | 70 | 100 GB | SQX en mantenimiento |
| 162 | sqx-ulab-kron-1 | kronos | **stopped** | 12 | 30 GB | SQX pequeña |
| 170 | sqx-ulab-zeus-1 | zeus | **stopped** | 8 | 23 GB | SQX pequeña |
| 200 | ca-aranea | athena | running | — | — | step-ca (ticket 005) |

---

## 2. Estado actual de backups (diagnóstico)

### 2.1 Regla 3-2-1 — análisis

| Componente | Estado | Notas |
|---|---|---|
| Copia 1 (producción) | ✅ | Ceph/ZFS pool0 |
| Copia 2 (mismo host) | ⚠️ | `pool2/backup/*` parcial, **mismo host físico** (hades+truenas) |
| Copia 3 (off-host) | ❌ | **No existe** |
| Off-site (geo-distinto) | ❌ | **No existe** |
| Offline/air-gap | ❌ | No existe |

### 2.2 Backups existentes

| Tipo | Herramienta actual | Destino | Problema |
|---|---|---|---|
| VMs/LXCs Proxmox | `vzdump` | NFS `proxmox_storage` (pool0) | Sin dedup, mismo host físico, `prune-backups=keep-all` (llena disco) |
| Ceph RBD (pool1) | ❌ | — | Sin snapshots automatizados |
| ZFS pool0 (truenas) | manual (`zfs snapshot` ad-hoc) | mismo pool | Sin `sanoid`, política retención no declarativa |
| ZFS pool2 (truenas) | manual | mismo pool | Single disk peligroso, scrub 11 meses sin ejecutar |
| Bases de datos (PostgreSQL, MongoDB) | ❌ | — | Sin dumps automatizados |
| Obsidian vault (CouchDB) | replicación LiveSync | CouchDB otro nodo | OK, pero no off-host |
| minio | ❌ | — | Sin backup |
| Traefik config | ❌ | — | Manual |
| step-ca | ❌ | — | **Crítico** (claves privadas) sin backup |
| etcd | `etcdctl snapshot` manual | local | Sin automatización |
| OPNsense config | export XML manual | local | Sin automatización |
| `/etc/pve` | ❌ | — | Sin backup |

### 2.3 Diagnóstico crítico

1. **No existe off-host real** (todo en hades → si hades cae, todo muere — aceptado por owner).
2. **No existe off-site** (no hay DR para terremoto/incendio).
3. **pool2 single disk** es punto único de fallo. Sin forma de mirror sin comprar o romper pool0 — se mitiga con off-host (PBS + cloud).
4. **PBS no implementado** (vzdump a NFS, sin dedup).
5. **Ceph HEALTH_WARN** (fragmentación + slow ops).
6. **SSDs consumer** (WD Green SATA en pool0 y `local-sqx-*`) — riesgo de falla más alto que enterprise.

---

## 3. Recursos disponibles para backup (sin comprar nada)

### 3.1 Inventario de SSDs/HDDs libres

| Recurso | Nodo | Tamaño | Tipo | Estado | Uso propuesto |
|---|---|---|---|---|---|
| `local-kronos` | kronos | 680 GB libre | SSD SATA (Samsung 870 QVO) | ✅ Libre | **Datastore PBS** |
| `pool-kronos` | kronos | 730 GB libre | SSD SATA (Crucial P3) | ✅ Libre | Buffer/expansión PBS o destino `zfs recv` (opcional) |
| `local-sqx-zeus` | zeus | 931 GB (250 GB libre) | SSD SATA (WD Green) | 🚫 **SAGRADO** | Solo SQX (vm 108) |
| `local-sqx-hera` | hera | 931 GB libre | SSD SATA (WD Green) | 🚫 **SAGRADO** | Solo SQX (vm 123 stopped, se reusará) |
| `local-sqx-kronos` | kronos | 931 GB (280 GB libre) | SSD SATA (WD Green) | 🚫 **SAGRADO** | Solo SQX (vm 111 stopped) |
| Ceph pool1 libre | distribuido | 1.6 TiB libre | RBD NVMe | ✅ Libre | Storage VMs running |
| pcloud (cloud) | externo | 1 TB | cloud oficial | ✅ Pagado | **Tier caliente — solo configs/datos críticos** |
| Google Drive (cloud) | externo | varios TB | cloud oficial | ✅ Pagado | **Tier bulk — snapshots ZFS pool0** |

### 3.2 Por qué `local-sqx-*` son sagrados

Las VMs SQX (`sqx-ulab-{zeus,hera,kronos}-*`) son la infraestructura de **Echo Forge** (programa propio, repo `xKoRx/symphony`, módulo `sqx` — Go + Java + Python) que orquesta **StrategyQuant X** (tool comercial, builder de estrategias de trading).

Owner declaró el 2026-07-01: **"esos discos (que son 3 iguales de 1 TB cada uno) se deben quedar para eso nomás"**. Las VMs SQX:
- Están en mantenimiento actualmente (4 de 5 stopped).
- Cuando operen, consumirán ~80% de los recursos de su host (zeus, hera, kronos) para procesar y desarrollar nuevas estrategias.
- Los 3 SSDs WD Green SATA son su storage exclusivo para datasets SQX (datos de mercado, databanks, exports).
- **Cualquier rol que no sea SQX está prohibido** en esos 3 SSDs.

Esto **descarta** la Fase 2 original que proponía destruir `local-sqx-hera` para hacer `zfs recv` desde truenas.

### 3.3 ¿Por qué PBS y no `zfs recv`?

- **PBS** (`local-kronos`, 680 GB SSD libre en kronos): backup VMs/LXCs Proxmox completo, **dedup nativa a nivel de bloque** (ahorra mucho espacio cuando hay OS base repetido entre VMs), compresión, verificación, retención declarativa (`prune-backups keep-daily=N keep-weekly=M keep-monthly=K`).
- **`zfs recv` on-cluster** (antes propuesto): copia de datasets ZFS de truenas, depende de tener un SSD libre que no sea SQX. **No hay SSD libre suficiente en hera/kronos que no sea SQX** (los únicos libres son `local-kronos` y `pool-kronos`, ambos en kronos, y se usan para PBS).
- **Cloud tier** (`rclone crypt`): off-site, geo-distinto. Complementa PBS.

**Resultado**: PBS off-host + cloud tier dual reemplazan completamente la capa `zfs recv` que se descartó.

### 3.4 Capacidad efectiva del plan

| Tier | Capacidad | Latencia restore | Uso |
|---|---|---|---|
| **Producción** (Ceph/ZFS) | varios TB | ms-seg | VMs/LXCs running |
| **PBS** (kronos `local-kronos`) | 680 GB SSD | seg-min | vzdump VMs/LXCs, 7d+4w+12m |
| **pcloud** (cloud) | 1 TB | minutos | configs/dumps críticos, semanal |
| **GDrive** (cloud) | varios TB | horas | snapshots ZFS pool0, mensual |

Suficiente para 3-2-1 modesto sin comprar HW.

---

## 4. Arquitectura objetivo (post-mejoras)

```
                          ┌──────────────────────┐
                          │  WAN / Internet      │
                          └─────────┬────────────┘
                                    │
                              ┌─────▼─────┐
                              │  athena   │  ← gateway (OPNsense)
                              └─────┬─────┘
                                    │ LAN 192.168.31/24 + Ceph 10.10.10/24
        ┌────────────┬────────────┼────────────┬────────────┐
        │            │            │            │            │
    ┌───▼───┐    ┌───▼───┐    ┌───▼───┐    ┌───▼───┐    ┌───▼───┐
    │ zeus  │    │ hera  │    │kronos │    │ hades │    │truenas│
    │Ceph   │    │Ceph   │    │Ceph   │    │       │    │(VM)   │
    │OSD.2  │    │OSD.0  │    │OSD.1+3│    │compute│    │pool0  │
    │compute│    │compute│    │+ PBS  │    │25 VMs │    │SSD    │
    │       │    │       │    │VM(NEW)│    │+ truenas│  │mirror │
    │[SDA]  │    │[SDA]  │    │[SDA]  │    │ VM    │    │       │
    │sqx    │    │sqx    │    │sqx    │    │       │    │pool2  │
    │SAGRADO│    │SAGRADO│    │SAGRADO│    │       │    │HDD    │
    │       │    │       │    │[SDB]  │    │       │    │single │
    │       │    │       │    │local- │    │       │    │       │
    │       │    │       │    │kronos │    │       │    │       │
    │       │    │       │    │PBS    │    │       │    │       │
    │       │    │       │    │680GB  │    │       │    │       │
    └───────┘    └───────┘    └───────┘    └───────┘    └───────┘
                                                              │
                                            zfs send (cron)  │
                                            rclone crypt    │
                                                              ▼
                                                    ┌──────────────────┐
                                                    │ pcloud (1TB)     │
                                                    │  - configs       │
                                                    │  - dumps DB      │
                                                    │  - step-ca       │
                                                    │                  │
                                                    │ Google Drive     │
                                                    │  (varios TB)     │
                                                    │  - pool0 snaps   │
                                                    │  - archive       │
                                                    └──────────────────┘
```

---

## 5. Diseño detallado por componente

### 5.1 PBS — Proxmox Backup Server (kronos)

**Recursos asignados**:
- VM PBS nueva (vmid propuesto 180) sobre `local-lvm` kronos (boot SO 32 GB).
- **8 GB RAM** (decisión owner: default mínimo, ajustar si métricas lo piden).
- 4-8 vCPU (kronos tiene 80t libres).
- Datastore `main` sobre `local-kronos` (680 GB SSD libre, Samsung 870 QVO).
- SO: Proxmox Backup Server 4.x sobre Debian 12.
- Red: vmbr0 (192.168.31.x).

**Setup**:
```bash
# En kronos, crear VM 180 via PVE UI o CLI
qm create 180 --name pbs-kronos --memory 8192 --cores 4 --sockets 1 \
  --net0 virtio,bridge=vmbr0 --scsihw virtio-scsi-pci \
  --scsi0 local-lvm:32 --ide2 local:iso/proxmox-backup-server_4.x.iso,media=cdrom \
  --boot order=ide2 --ostype l26

# Instalar PBS desde ISO, configurar:
# - Hostname: pbs-kronos.aranea.lab
# - Network: DHCP o static (recomendado static, ej 192.168.31.180)
# - Disk: usar TODO local-kronos para datastore (montar /backup/main)

# Post-install en PBS:
proxmox-backup-manager datastore create main --path /backup/main \
  --prune-backups keep-daily=7,keep-weekly=4,keep-monthly=12
proxmox-backup-manager user create backup@pbs --comment "PBS backup user"
proxmox-backup-manager user update backup@pbs --password <STRONG_PASSWORD>

# En cada uno de los 5 PVE nodes (athena, zeus, hera, kronos, hades):
pvesm add pbs backup-pbs --server 192.168.31.180 --datastore main \
  --username backup@pbs --password <STRONG_PASSWORD> \
  --content backup --prune-backups keep-daily=7,keep-weekly=4,keep-monthly=12
```

**Schedule vzdump** (en cada nodo, vía `/etc/pve/vzdump.cron` o systemd timer):
- **Daily 02:00** — VMs/LXCs `critical` tag (definir cuáles): sqx-ulab-* (cuando estén running), mt4-*, postgresql, mongodb, step-ca, obsidian-sync, etc.
- **Weekly Sat 02:00** — TODAS las VMs/LXCs.
- **Monthly** — restore drill (ver § 7).

### 5.2 Tier cloud — `rclone crypt` segregado

#### 5.2.1 pcloud (1 TB) — Tier caliente (configs + críticos)

**Va acá** (tamaños pequeños, críticos):
- vzdump de configs críticas (`/etc/pve`, Traefik dynamic configs, OPNsense XML export).
- `step ca backup` (claves privadas encriptadas).
- Dumps de bases de datos (PostgreSQL `pg_dumpall`, MongoDB `mongodump`).
- CouchDB dump (Obsidian vault).
- `etcdctl snapshot save`.
- `mc mirror` de buckets minio críticos (si los hay).
- Manifests críticos (`inventory.md`, snapshots de docs del Second Brain).

**NO va acá**:
- vzdump de VMs completas (van a PBS).
- Snapshots ZFS de pool0 (demasiado grandes, van a GDrive).
- Logs, caches, `/tmp`.

#### 5.2.2 GDrive (varios TB) — Tier bulk

**Va acá** (tamaños grandes, archive):
- Snapshots ZFS de pool0: `zfs send -w pool0@snap > /backup/pool0-snap-YYYYMMDD.zfs` → rclone a GDrive.
- Datasets grandes: `aranea_storage` (998 GB), `trading_documents`, `frigate/media` (NVR — alto volumen, baja prioridad).
- Backups históricos de VMs (cuando roten de PBS).
- `rclone check` mensual para validar integridad cifrada.

**NO va acá**:
- Nada que requiera restore rápido (la WAN chilena es lenta).
- Nada pequeño/crítico (eso va a pcloud).

#### 5.2.3 Setup `rclone + crypt`

```bash
# En PBS VM o hermes-vm (decidir después)
apt install rclone

# Interactivo: rclone config
rclone config

# 1. Crear "pcloud" tipo pcloud (OAuth en navegador)
# 2. Crear "pcloud-crypt" tipo crypt sobre pcloud:/aranea-configs-crypt
#    filename_encryption=standard
#    directory_name_encryption=true
#    password=<strong-passphrase-en-bitwarden>  # NO usar la misma que gdrive
# 3. Crear "gdrive" tipo drive (OAuth Google)
# 4. Crear "gdrive-crypt" tipo crypt sobre gdrive:/aranea-archive

# Verificar
rclone lsd pcloud-crypt:
rclone lsd gdrive-crypt:
```

#### 5.2.4 Política de sync (cron jobs)

```bash
# PBS datastore → pcloud (weekly domingo 03:00)
rclone sync /backup/pbs-main-configs pcloud-crypt:aranea-configs \
  --transfers 4 --bwlimit "08:00,20M 22:00,off" \
  --log-file /var/log/rclone-pbs-pcloud.log --log-level INFO

# Snapshots ZFS pool0 → GDrive archive (monthly 1° del mes 04:00)
rclone sync /pool0-snapshots gdrive-crypt:aranea-pool0-archive \
  --transfers 2 --bwlimit "08:00,10M 22:00,off" \
  --log-file /var/log/rclone-pool0-gdrive.log --log-level INFO
```

### 5.3 ZFS `sanoid` (autosnapshot + retención declarativa)

```yaml
# /etc/sanoid/sanoid.conf (en truenas)
[pool0/aranea_storage]
  use_template = production
[pool0/proxmox_storage]
  use_template = production
[pool0/trading_systems]
  use_template = critical

[template_production]
  hourly = 24
  daily = 30
  weekly = 8
  monthly = 12
  autosnap = yes
  autoprune = yes
[template_critical]
  hourly = 48
  daily = 90
  weekly = 12
  monthly = 24
  yearly = 5
  autosnap = yes
  autoprune = yes
[template_backup]
  daily = 14
  weekly = 8
  monthly = 12
  autosnap = yes
  autoprune = yes
```

### 5.4 Scrub mensual

```bash
# /etc/cron.d/zfs-scrub (truenas)
# 1° del mes 02:00 — scrub pool0 (largo, 4h)
0 2 1 * * zpool scrub pool0
# 2° del mes 02:00 — scrub pool2 (más corto, 2h)
0 2 2 * * zpool scrub pool2
```

---

## 6. Política de backup consolidada

### 6.1 Por tipo de dato

| Tipo | Herramienta | Frecuencia | Retención local | Retención off-host |
|---|---|---|---|---|
| **VMs/LXCs Proxmox** (incluye SQX cuando running) | vzdump → PBS | Diario 02:00 critical + Semanal Sat all | 7d + 4w + 12m | sync PBS configs → pcloud weekly |
| **Ceph RBD (pool1)** | rbd snap (manual hasta automatizar) | Diario 02:00 | 7d + 4w | export → PBS weekly |
| **ZFS pool0 (truenas)** | sanoid | Hourly + Daily + Weekly + Monthly | 24h + 30d + 8w + 12m | `zfs send` → archivo → GDrive monthly |
| **ZFS pool2 (truenas)** | sanoid | Weekly + Monthly | 4w + 12m | rclone crypt → GDrive monthly |
| **PostgreSQL (vm 152)** | `pg_dumpall` | Diario 01:00 | 7d | dump → pcloud |
| **MongoDB (vm 153)** | `mongodump` | Diario 01:30 | 7d | dump → pcloud |
| **Obsidian vault (lxc)** | CouchDB dump | Diario 00:00 | 7d | dump → pcloud |
| **minio** | `mc mirror` | Diario 03:00 | 7d | mirror → pcloud (solo críticos) |
| **Traefik config** | `tar czf` | Diario 04:00 | 30d | copy → pcloud |
| **step-ca** | `step ca backup` | Diario 04:30 + pre-change | 90d | backup encriptado → pcloud |
| **OPNsense config** | UI export XML | Semanal Sat 08:00 | 12w | export → pcloud |
| **/etc/pve** | `tar czf` | Semanal Sat 08:30 | 12w | tar → pcloud |
| **etcd** | `etcdctl snapshot` | Diario 05:00 | 30d | snap → pcloud |

### 6.2 Cronograma visual (gantt)

```mermaid
gantt
    title Backup schedule — Aranea post-mejoras
    dateFormat HH:mm
    axisFormat %H:%m

    section Daily
    Obsidian vault (CouchDB)    :d0, 00:00, 30m
    PG dump                     :d1, 01:00, 30m
    MongoDB dump                :d2, after d1, 30m
    vzdump critical → PBS       :d3, 02:00, 60m
    Ceph RBD snap               :d4, after d3, 30m
    ZFS daily snap pool0        :d5, after d4, 30m
    Traefik + step-ca backup    :d6, after d5, 10m
    minio mirror                :d7, after d6, 30m
    zfs send pool0 → /backup    :d8, after d7, 60m
    etcd snapshot               :d9, after d8, 10m

    section Weekly
    vzdump ALL VMs → PBS        :w1, sat, 02:00, 4h
    rclone PBS → pcloud         :w2, sun, 03:00, 4h
    OPNsense config export      :w3, sat, 08:00, 30m
    /etc/pve backup             :w4, after w3, 30m

    section Monthly
    Scrub pool0                 :m1, 1st, 02:00, 4h
    Scrub pool2                 :m2, 2nd, 02:00, 4h
    Restore drill (1 VM)        :m3, 15th, 04:00, 4h
    rclone pool0 → GDrive       :m4, 1st, 04:00, 12h
```

---

## 7. Optimización de espacio (puntos abiertos)

Owner pidió "algo media tricky para reducir espacio" en backups. Tres opciones que aplican a este stack:

### Opción A — Conservadora (recomendada por simplicidad)
- **PBS dedup nativa** (block-level, ya incluida): efectiva en VMs con OS base repetido (~40-60% reducción datastore PBS).
- **ZFS `zfs send -w` (raw) + `-c` compressed**: ahorra WAN y storage en `zfs send` a GDrive (~20-30%).
- **PBS encryption + compression**: estándar.
- **`rclone crypt` con `--partial` y `--low-level-retries`**: para WAN inestable.
- **Excluir `/var/log`, `/tmp`, caches de VMs en vzdump**: ahorra 10-20%.
- **Complejidad**: baja. **Esperado**: ~40-60% reducción PBS, ~30% cloud.

### Opción B — Agresiva (mayor reducción, suma complejidad)
- Todo lo de Opción A **+ BorgBackup o restic sobre rclone**: dedup adicional content-defined (chunks variables, detecta bloques repetidos cross-VM).
- **Esperado**: ~60-80% reducción total.
- **Costo**: una capa más (Borg/restic), más complejidad operacional (init repo, prune, check).

### Opción C — Específica del owner (basada en su experiencia)

Owner ofreció su experticia en sistemas de backup a escala (mensaje 2026-07-01: *"tengo acceso a múltiples exportes de muchas materias por si quieres hacer preguntas puntuales sobre diseño de sistemas de backups. yo soy nulo, soy dev y trading algorítmico, tengo mi homelab como hobbie"*).

**Recomendación actual**: Opción A como default, Opción B si las métricas de PBS/GDrive muestran problemas de espacio.

---

## 8. Roadmap de implementación (capex $0)

### Fase 0 — Quick wins (~medio día)
1. `zpool scrub pool2` en truenas (cerrar alerta 11 meses).
2. `ceph tell osd.0 osd.2 osd.3 compact` (cerrar HEALTH_WARN fragmentación).
3. Configurar `sanoid` en truenas con política retención.
4. Documentar `lspci` por nodo (gap info).

### Fase 1 — PBS en kronos (~1 día)
1. Crear VM PBS (vmid 180) en kronos.
2. Install PBS sobre Debian 12 o ISO PBS.
3. Crear datastore `main` sobre `local-kronos` SSD SATA libre.
4. Crear user `backup@pbs` + API token.
5. Registrar storage `aranea-pbs` en los 5 PVE nodes.
6. Configurar vzdump schedule (daily-critical + weekly-all).
7. Primer vzdump manual de prueba.

### Fase 2 — ~~Destino secundario `zfs recv` en hera~~ → DESCARTADA (2026-07-01)
**Razón**: SSDs `local-sqx-*` son sagrados para SQX (Echo Forge). No hay otro SSD libre significativo en hera.

**Alternativa opcional** (no priorizada): usar `pool-kronos` (730 GB libre, NO SQX) como destino `zfs recv`. Decisión pendiente del owner.

### Fase 3 — Tier cloud (~medio día)
1. rclone config para pcloud (OAuth).
2. Crear remote `crypt` sobre pcloud.
3. rclone config para Google Drive (OAuth).
4. Crear remote `crypt` sobre GDrive.
5. Configurar sync job weekly PBS configs → pcloud.
6. Configurar sync job monthly pool0 snapshots → GDrive.
7. Probar restore desde pcloud (drill).

### Fase 4 — Pool2 scrub mensual + sanoid (~medio día)
1. `zpool scrub pool2` inmediato (cerrar alerta 11 meses).
2. Configurar `sanoid` con política retención para pool2 (template `backup`).
3. Marcar `pool2/backup/*` y `pool2/pool0_backup/` como "stage, no backup" en la doc.
4. NO migrar `pool2/pool0_backup/` (decisión owner 2026-07-01: dejar como está).

### Fase 5 — Restore drills (continuo)
1. Schedule mensual rotativo (1 VM drill/mes).
2. Ajustar sanoid retention según uso real.
3. Ajustar `rclone bwlimit` según WAN.
4. Documentar tiempo/ratio de cada restore.

---

## 9. Trade-offs explícitos y decisiones arquitecturales

### 9.1 Decisiones tomadas

| Decisión | Razón | Trade-off aceptado |
|---|---|---|
| PBS en kronos (no en otro nodo) | kronos tiene 251 GB RAM libre, 2 SSDs libres grandes (`local-kronos` 680 GB, `pool-kronos` 730 GB), Ceph MON standby | Si kronos cae, PBS off-host cae + Ceph degraded. Mitigación: cloud tier sigue accesible. |
| PBS RAM = 8 GB (no 16 GB) | Owner prefiere default mínimo | Si PBS se queda corto de RAM, métricas mostrarán presión. Ajustar. |
| PBS datastore = `local-kronos` (SSD) | Más rápido que HDD para dedup block-level | Si se llena, escalar a `pool-kronos` (NO SQX, libre). |
| `local-sqx-*` SAGRADOS | Owner declaró explícitamente | Perdemos ~2.8 TB SSD para backup. PBS off-host + cloud compensan. |
| No `zfs recv` on-cluster | SSDs libres son SQX | Sin redundancia ZFS local entre pools. Cloud tier es la redundancia. |
| pcloud = configs críticos (1 TB) | Owner declaró escasez | Obliga a elegir bien qué sube. NO bulk. |
| GDrive = bulk snapshots pool0 (varios TB) | Owner declaró disponibilidad | WAN lenta, solo DR/archive. NO restore rápido. |
| pool2 single disk aceptado | No hay disco libre para mirror sin romper pool0 | Scrub mensual obligatorio + rclone off-host. |
| hades SPOF aceptado | hades hypervisor de truenas (decisión owner) | Si hades cae, truenas VM + 25 VMs mueren. PBS off-host en kronos sobrevive. |
| Ceph sin backup externo | 3× replication on-cluster ya cubre | Sin DR-copy RBD fuera de Ceph. Aceptable porque 3× rep + vzdump PBS. |

### 9.2 Decisiones nuevas pendientes (2026-07-01)

1. **¿Reactivar Fase 2 con `pool-kronos` (730 GB libre, NO SQX) como destino `zfs recv` secundario on-cluster?** Hoy PBS + cloud cubren; respuesta puede ser "no por ahora".
2. **Optimización de espacio**: ¿Opción A (conservadora), Opción B (agresiva con Borg/restic), o algo específico del owner?

---

## 10. Riesgos y mitigaciones

| Riesgo | Probabilidad | Impacto | Mitigación |
|---|---|---|---|
| hades cae → todo muere (truenas VM + 25 VMs) | Media | Catastrófico | **Aceptado por owner**. Mitigación parcial: PBS off-host + cloud tier. |
| PBS en kronos comparte host con Ceph MON | Baja | Medio | Si kronos cae → PBS off-host cae + Ceph degraded. Mitigación: cloud tier (pcloud/GDrive) sigue accesible. |
| rclone crypt pierde passphrase | Baja | Catastrófico | Escrow offline: bitwarden offline + USB cifrado. |
| pcloud/GDrive cierran cuenta | Baja | Alto (pierdes off-site) | Mitigación: Tier cloud dual. Si querés redundancia física, futuro USB rotativo. |
| WAN lento bloquea rclone | Media | Bajo (solo cloud) | `--bwlimit` nocturno + horario. |
| Ceph se fragmenta más | Media | Medio | `ceph tell osd.* compact` mensual (Fase 0). |
| SSD WD Green (SQX sagrados) falla | Media | Medio (SQX en mantenimiento, vm 108 running) | vzdump daily a PBS cubre VM completa. Datasets SQX dentro de VM. |
| pcloud 1 TB se llena rápido | Media | Bajo | Solo configs/dumps (no bulk). Rotación mensual. |
| GDrive WAN saturada | Alta | Bajo (solo archive) | `--bwlimit` nocturno. Monthly job. |
| `local-kronos` SSD Samsung QVO falla | Baja | Medio (PBS datastore) | PBS restore desde otra copia (pcloud de configs) o rebuild. `pool-kronos` queda como buffer. |

---

## 11. Recursos de referencia en el Second Brain

- `30-resources/aranea/03-storage/DESIGN-PROPOSAL.md` — propuesta completa con detalle técnico (32 KB, 12 secciones).
- `30-resources/aranea/03-storage/BACKUP-SYSTEM.md` — Task 2 previa (políticas detalladas).
- `30-resources/aranea/03-storage/AUDIT.md` — auditoría storage previa.
- `30-resources/aranea/03-storage/TOPOLOGY-AUDIT.md` — auditoría crítica topológica (10 hallazgos).
- `30-resources/aranea/03-storage/inventory.md` — landscape storage completo.
- `30-resources/aranea/01-topologia/` — docs por nodo (athena, zeus, hera, kronos, hades, truenas).
- `30-resources/aranea/02-servicios/ml-ia.md` — detalle VMs SQX.
- `30-resources/aranea/05-tickets/2026-06-30-013-storage-redesign-backup-design.md` — ticket con iteraciones de la propuesta.
- `30-resources/tools/strategyquant-x.md` — definición tool SQX (separada de echo-forge).
- `30-resources/applications/echo-forge.md` — definición programa Echo Forge.
- `10-projects/Echo Forge/Echo Forge.md` — proyecto Echo Forge.
- Skill: `aranea_agent_ro_inventory_refresh` (en `~/.hermes/profiles/ariadna/skills/devops/`).

---

## 12. Estado de gaps del roadmap Aranea

| Gap | Estado |
|---|---|
| #1 SSH + sudo NOPASSWD para `agent_ro` | ✅ Resuelto 2026-06-30 (ticket 012) |
| #2 Inventario con drift de 2 días | ✅ Resuelto 2026-06-30 (refresh inventario) |
| #3 Auditoría profunda de storages | ✅ Diseño cerrado (ticket 013, iter 4). Pendiente ejecución. |
| #4 Diseño de sistema de backup | ✅ Diseño cerrado (ticket 013, iter 4). Pendiente ejecución. |
| #5 Detalle por VM/LXC (snapshots, configs) | Parcial — wrapper `agent-read` no expone `vm <vmid> config`. Pendiente. |
| #6 Observabilidad unificada | No existe stack Prometheus/Grafana centralizado. Pendiente. |

**Tickets activos** (no storage):
- 015 — DNS dashboard.lab.aranea → apunta a .122 en vez de Traefik.11 (low)
- 016 — Hermes config v31→v32 (low)
- 017 — Dashboard healthcheck script+cron (low)

---

**Próximo paso**: este doc se entrega al owner para revisión con IA externa especialista en sistemas de backup. Tras feedback, ajustar la propuesta 013 y abrir tickets 018-021 para ejecutar Fases 0, 1, 3, 4 (Fase 2 descartada, ver § 8).

**Estado**: propuesta pendiente de revisión externa.
**Capex**: $0. **Opex mensual cloud**: $0.
**Captured**: 2026-07-01.
