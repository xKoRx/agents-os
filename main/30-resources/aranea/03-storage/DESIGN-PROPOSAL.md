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

# 🏗️ [DEPRECATED] Aranea storage & backup — propuesta con recursos existentes

## Propósito

Documentación canónica legacy de [[Aranea]]; se conserva el contenido histórico y su estado requiere verificación antes de uso operativo.

## Contenido


## Propósito

Conservar como evidencia histórica la propuesta de storage y backup supersedida el 2026-07-01; no es fuente de implementación vigente.

## Contenido

> [!warning] DEPRECATED 2026-07-01
> Este documento está **superseded** por [[backup-dr/BACKUP-DR-DESIGN]].
> **NO usar para implementación**. Contiene contradicciones activas detectadas en el refactor.
> Mantenido como histórico de las iteraciones 1-4.
> **Ver**: [[backup-dr/00-index]] para el set vigente de 16 archivos.

> **Status original**: propuesta. **NO comprar HW nuevo. NO migrar TrueNAS a bare-metal. NO cambiar cantidad de servidores.** 5 Proxmox + truenas-vm-en-hades = el set estable.
> **Inputs**: inventario fresco 2026-06-30 19:44 UTC (skill `aranea_agent_ro_inventory_refresh`), `BACKUP-SYSTEM.md` previo (Task 2), `AUDIT.md`, `inventory.md`, doc por nodo.
> **Restricciones explícitas del owner**:
> 1. **Cero capex** — usar solo lo que ya hay.
> 2. **No migrar TrueNAS** a otro host (hades se queda como hypervisor de truenas).
> 3. **No agregar ni sacar servidores** — el cluster es 5 Proxmox + truenas-vm + hermes-vm.

---

## 0. TL;DR (1 página)

**Diagnóstico (1 línea)**: lo que tienes **alcanza y sobra** para un backup decente. El problema es **organización**, no capacidad. Hoy `pool2` es single disk peligroso, no hay off-host real, y la doc está dispersa.

**Recomendación en 5 puntos — todo con recursos existentes**:

1. **PBS en VM nueva en kronos** sobre SSD SATA libre (reusar `local-kronos` 680 GB libre o `local-sqx-hera` 931 GB libre). Costo: $0.
2. **`pool2` → mirror con `sdf1` de hades** (SSD 931 GB actualmente spare/zfs_member no usado). Costo: $0, pero **requiere verificar primero que `sdf1` sea spare real** y no esté asignado a un pool que no se ve en el wrapper.
3. **Reusar `local-sqx-hera` (931 GB libres, vm 123 stopped)** como destino de `zfs recv` desde truenas — segunda capa de backup on-cluster sin gastar un peso.
4. **Tier cloud**: `rclone crypt` sobre pcloud (1 TB existente) + Google Drive (1-5 TB existente). Costo mensual: $0 si usas solo el espacio que ya tienes pagado.
5. **Política**: sanoid hourly/daily/weekly/monthly + vzdump a PBS diario + `zfs send` semanal a hera/kronos + `rclone crypt` weekly a pcloud.

**Capex**: **$0**. **Opex mensual cloud**: **$0** (usas pcloud y GDrive que ya tienes).

---

## 1. 📚 Buenas prácticas (resumen ejecutivo)

### 1.1 Regla 3-2-1

> **3 copias** · **2 medios distintos** · **1 copia off-site** (+ idealmente 1 offline/air-gap y 0 errores verificados)

| Estado hoy                                  | Target                                                 |
| ------------------------------------------- | ------------------------------------------------------ |
| Copia 1 (producción): Ceph/ZFS pool0        | ✅                                                      |
| Copia 2 (mismo host): pool0_backup en pool2 | ⚠️ mismo host, mismo disco físico (pool2 single disk)  |
| Copia 3 (off-host): ❌ no existe             | 🔴 PBS + pcloud                                        |
| **Off-site (geo-distinto)**: ❌              | 🔴 pcloud + GDrive                                     |
| Offline/air-gap: ❌                          | 🟡 opcional (export a USB rotativo, **cuando exista**) |

### 1.2 Herramientas (todas disponibles, $0)

| Herramienta | Rol |
|---|---|
| **Proxmox Backup Server (PBS)** | Backup VMs/LXCs — dedup, compresión, verify nativa |
| **ZFS snapshots + `zfs send/recv`** | Backup datasets ZFS incremental |
| **`sanoid` + `syncoid`** | Política retención ZFS declarativa |
| **`rclone` + `rclone crypt`** | Sync a cloud con cifrado AES-256 cliente |
| **`etcdctl snapshot`** | Backup cluster etcd |
| **`step ca backup`** | Backup step-ca |

### 1.3 ZFS — reglas de oro

- **Mirror > RAIDZ1** para backups (resilver rápido, predecible).
- **Scrub mensual obligatorio** (bit-rot).
- **`zfs send -w` (raw)** cuando hay compresión, más rápido.
- **`special vdev` (metadata)**: obligatorio para pools con muchos archivos pequeños.

### 1.4 Ceph — regla práctica

- **3× replication = baseline**.
- **Fragmentación BlueStore > 0.80** = `ceph tell osd.* compact`.
- **HEALTH_WARN actual** (osd.0 0.84, osd.2 0.82, slow ops) = fix con compact + planificar más OSDs.

---

## 2. 🔍 Recursos REALES disponibles (snapshot 2026-06-30)

### 2.1 Por nodo — qué hay, qué se usa, qué sobra

#### **athena** (gateway, OPNsense + servicios red)

| Recurso | Spec | Uso | Libre |
|---|---|---|---|
| CPU i7-13620H | 16t | gateway + VMs ligeras (etcd, traefik, pi-hole, opnsense, ca) | bajo |
| RAM 16 GB | 16 GiB | 11 GiB used | 4.2 GiB avail |
| NVMe 476 GB | nvme0n1 | root 94 GB + local-lvm 348 GB | 81 GB root libre |

**Diagnóstico**: gateway, no debería correr storage. Saturada en RAM. **No candidata a PBS ni a storage adicional**.

#### **zeus** (compute + Ceph OSD.2)

| Recurso | Spec | Uso | Libre |
|---|---|---|---|
| CPU Ryzen 9 5950X | 32t | VMs compute | ~70% |
| RAM 94 GB | 94 GiB | 67 GiB used | 27 GiB avail |
| NVMe 931 GB | nvme0n1 | **Ceph OSD.2** | 0 |
| NVMe 465 GB | nvme1n1 | boot + local-lvm 400 GB | ~16 GB |
| SSD 931 GB (WD Green) | sda | LVM `local-sqx-zeus` (vm 108 sqx) | ~280 GB |

**Diagnóstico**: bien balanceado. **No candidata a PBS** (kronos es mejor).

#### **hera** (compute + Ceph OSD.0)

| Recurso | Spec | Uso | Libre |
|---|---|---|---|
| CPU 2× Xeon E5-2699 v3 | 72t | medio (vm 123 stopped, otras) | ~50% |
| RAM 125 GB | 125 GiB | medio | ~80 GB |
| NVMe 931 GB | nvme1n1 | **Ceph OSD.0** | 0 |
| NVMe 465 GB | nvme0n1 | boot + local-lvm 338 GB | ~22 GB |
| **SSD 931 GB (WD Green)** | sda | LVM `local-sqx-hera` (vm 123 stopped) | **931 GB LIBRE** |

**Diagnóstico**: **931 GB SSD desperdiciado** porque vm 123 está stopped. **Candidata ideal para destino de `zfs recv` desde truenas** (LXC privilegiada o pequeño VG LVM-thin que reciba backups ZFS).

#### **kronos** (storage powerhouse + Ceph OSD.1+3)

| Recurso | Spec | Uso | Libre |
|---|---|---|---|
| CPU 2× Xeon E5-2698 v4 | 80t | medio | ~50% |
| **RAM 251 GB** | 251 GiB | medio | **muy grande** |
| NVMe 931 GB × 2 (Kingston) | nvme0n1 + nvme1n1 | **Ceph OSD.1 + OSD.3** | 0 |
| SSD 931 GB (WD Green) | sda | LVM `local-sqx-kronos` (vm 111 stopped) | ~280 GB |
| SSD 931 GB (Samsung 870 QVO) | sdb | LVM `local-kronos` (250 GB usados) | **~680 GB** |
| SSD 954 GB (Crucial P3) | sdc | LVM `pool-kronos` (220 GB usados) | **~730 GB** |
| SSD 232 GB (Samsung 870 EVO) | sdd | boot + root + local-lvm 54 GB | ~10 GB |

**Diagnóstico**: **el nodo con más recursos libres**. ~1.7 TB SSD SATA libres. 251 GB RAM. **Candidata #1 para PBS** (datastore sobre `local-kronos` 680 GB o `pool-kronos` 730 GB).

#### **hades** (compute-heavy + host de TrueNAS VM)

| Recurso | Spec | Uso | Libre |
|---|---|---|---|
| CPU 2× Xeon E5-2697 v4 | 72t | load 9-10, 25 VMs | ~10% |
| **RAM 251 GB** | 251 GiB | **187 GiB used (74%)** | 64 GiB avail |
| NVMe 119 GB | nvme2n1 | boot + local-lvm 54 GB | ~10 GB |
| NVMe 465 GB | nvme0n1 | **truenas special mirror** | 0 (ZFS) |
| NVMe 476 GB | nvme1n1 | **truenas special mirror** | 0 (ZFS) |
| **SSD 931 GB × 7** | sda-sde, sdg, sdh | **truenas pool0 (mirror-0,1,2,3)** | 0 (ZFS) |
| **SSD 931 GB (sdf)** | sdf | **`zfs_member` pero NO aparece en zpool_status** → probable **SPARE** o no asignado | **LIBRE** ⚠️ requiere verificar |
| HDD 7.3 TB | sdi | **truenas pool2 (single disk)** | 0 (ZFS) |

**Diagnóstico**: 
- 8 SSDs SATA originalmente pensados para truenas pool0 → solo 7 están en pool0 (mirrors 0-3). **`sdf` está libre / spare**.
- **El plan original era 8 SSDs en 4 mirrors = 16 dispositivos para 4 mirrors; pero solo 7 están asignados.** ¿`sdf` se quedó sin asignar? Verificar antes de tocar.
- **Si `sdf` realmente está libre** → **mirror de pool2 posible con SSD de 931 GB**. No es HDD 8 TB como el `sdi`, pero **añade redundancia SSD al single-disk pool2** (y cambia el perfil: pool2 pasa a ser SSD mirror, no HDD single). Riesgo: pool2 con SSD pierde el "batch barato" que tenía con el HDD 7.3 TB.

**Decisión arquitectural a tomar**: si `sdf` está libre, **pool2 podría**:
- **A. Convertirse en mirror SSD 2×931 GB** → 931 GB usable, todo SSD, batch diario OK.
- **B. Quedarse single HDD 7.3 TB + agregar `sdf` como cache device (L2ARC/ZIL)** → +931 GB cache SSD sobre HDD bulk. Más complejo pero conserva capacidad.
- **C. No tocar pool2**, usar `sdf` como mirror de un **pool1 NUEVO** (que reemplaza a pool2 conceptualmente).

**Recomendación**: A o C, no B. B es más complejo y `sdf` solo como L2ARC no resuelve el single-disk del data.

#### **truenas** (VM en hades)

| Recurso | Spec | Uso | Libre |
|---|---|---|---|
| pool0 | ZFS 4 mirror SSD + special mirror | 4.48 TB raw / 2.49 TB usado (57%) | OK |
| pool2 | ZFS 1 disk HDD 7.3 TB | 7.99 TB raw / 3.51 TB usado (44%) | ⚠️ single disk |
| boot-pool | 30 GB | SO TrueNAS | OK |
| RAM 32 GB | 32 GiB | de los 251 de hades | OK |
| vCPUs 30 | 30 | de los 72 de hades | OK |

### 2.2 Capacidad cluster total (corregida)

| Storage | Raw | Usado | % | Estado |
|---|---|---|---|---|
| Ceph pool1 | 3.6 TiB | 2.1 TiB | 75% pool | HEALTH_WARN |
| Truenas pool0 | 4.48 TB | 2.49 TB | 57% | OK |
| Truenas pool2 | 7.99 TB | 3.51 TB | 44% | ⚠️ single disk |
| LVM locales PVE | ~1.7 TB totales | ~300 GB | bajo | OK |
| LVM `local-sqx-*` | ~2.8 TB | ~1.3 GB (vm 108) + 0 GB (vm 123 stopped) + ~650 GB (vm 111 stopped) | varía | **931 GB en hera LIBRE**, ~930 GB en kronos ocupado por vms stopped |
| LVM `local-kronos` | 931 GB | 250 GB | 27% | **680 GB libre** |
| LVM `pool-kronos` | 954 GB | 220 GB | 23% | **730 GB libre** |
| **TOTAL raw** | **~17.6 TB** | **~9 TB** | **~51%** | |

### 2.2 Hallazgo clave: recursos para backup (sin comprar nada) — **CORREGIDO 2026-06-30**

| Recurso libre | Tamaño | Tipo | Uso propuesto | Status |
|---|---|---|---|---|
| **`local-kronos` (libre en kronos)** | 680 GB | SSD SATA | **Datastore PBS** | ✅ confirmado libre |
| **`pool-kronos` (libre en kronos)** | 730 GB | SSD SATA | Datastore PBS alternativo | ✅ confirmado libre |
| **`local-sqx-*` (zeus/hera/kronos)** | 931 GB × 3 | SSD SATA WD Green | **SAGRADOS** — datasets SQX, NO TOCAR | 🚫 regla del owner (2026-07-01) |
| **`local-sqx-hera` (libre en hera)** | 931 GB | SSD SATA | ~~Destino `zfs recv`~~ | ❌ **DESCARTADO** — `local-sqx-*` son sagrados (regla owner 2026-07-01) |
| **`sdf1` hades** | 931 GB | SSD SATA | ~~Mirror pool2~~ | ❌ **NO LIBRE — está en pool0 mirror-0** (ver output truenas 2026-06-30) |
| **pcloud** | 1 TB | cloud oficial | **Tier caliente — solo configs/datos críticos** (NO bulk) | ✅ |
| **Google Drive** | varios TB | cloud oficial | **Tier bulk — snapshots ZFS pool0, datasets** | ✅ |
| **RAM kronos** | ~200 GB libre | DDR | **VM PBS** (8 GB suficiente, ver decisión § 12.2) | ✅ |

**Cambio importante**: `sdf` NO es spare de ZFS. El `zpool status -v` en truenas (2026-06-30) muestra que `sdf` ya está como **mirror-0 de pool0** junto con `sdc`. Los 8 SSDs SATA de hades están todos en pool0 (4 mirrors completos). **No hay disco físico libre en hades para mirror de pool2 sin romper pool0**.

**Cambio crítico iter 4 (2026-07-01)**: el owner declara los 3 SSDs `local-sqx-{zeus,hera,kronos}` como **sagrados** — dedicados a las VMs SQX (`sqx-ulab-*`) que son la infraestructura de Echo Forge (generación y optimización de estrategias de trading). Esto **elimina** la Fase 2 que proponía destruir `local-sqx-hera` para hacer `zfs recv`. El plan queda: PBS off-host (kronos) + cloud tier dual (pcloud = configs, GDrive = bulk).

**Capacidad total disponible para backup sin comprar HW**: ~1.4 TB SSD on-cluster (`local-kronos` 680 GB + `pool-kronos` 730 GB) + 1+ TB cloud (pcloud) + varios TB cloud (GDrive). Sigue siendo suficiente para PBS off-host + tier cloud, pero perdemos la capa on-cluster `zfs recv` que tenía la propuesta original. **El plan se simplifica a PBS off-host + cloud dual**.

---

## 3. 🎯 Recomendación de uso (slots PCIe, topología)

> **Premisa**: no comprar HW. Aprovechar lo que hay.

### 3.1 Asignación propuesta

#### **athena** — sin cambios

Mantener gateway + UPS (si hay). Sin rol storage.

#### **zeus** — sin cambios

Mantener Ceph OSD.2 + compute. **Cero asignación de backup** (kronos es mejor opción).

#### **hera** — **destino secundario de `zfs recv` desde truenas**

- Mantener Ceph OSD.0 + compute.
- **Reusar `local-sqx-hera` (931 GB SSD libre) como destino de `zfs recv`** desde truenas.
  - Opción simple: destruir el VG `local-sqx-hera` (vm 123 está stopped, no se pierde nada operativo), recrear como `zfspool` storage en PVE, y dentro crear un ZFS pool `recv`.
  - O bien: crear LXC privilegiada en hera con acceso al disco raw y montar ZFS ahí.
  - **Resultado**: cuando truenas haga `zfs send -R pool0@daily`, lo recibimos acá.

#### **kronos** — **aquí corre PBS**

- Mantener Ceph OSD.1 + OSD.3 + compute.
- **Crear VM PBS nueva** (sugerido vmid 180):
  - 4-8 vCPU (kronos tiene 80t libres)
  - **16 GB RAM** (kronos tiene 251 GiB)
  - Disco sistema 32 GB en `local-lvm` (kronos sdd) o `pool-kronos`.
  - **Datastore PBS sobre `local-kronos` (680 GB libre SSD SATA)** — vía disco virtio backed por el VG existente, o disco passthrough directo del SSD Samsung QVO sdb.
  - Red: vmbr0.
  - OS: Proxmox Backup Server 4.x ISO (instalable sobre Debian 12).

#### **hades** — **verificar `sdf` y mirror de pool2**

- hades se queda como hypervisor de truenas (decisión del owner).
- **Acción 1 (crítica)**: ejecutar `zpool status -v` y `zpool get spare sdf1` en truenas para confirmar si `sdf1` está como spare o si está oculto en algún pool no listado.
- **Acción 2 (depende de Acción 1)**:
  - **Si `sdf1` está libre/spare**: attach como mirror de `pool2`. Resultado: pool2 = mirror SSD 931 GB × 2.
  - **Si `sdf1` está ocupado en pool0 o donde sea**: **no tocar pool2**, ir a plan B (ver § 4.3).

#### **truenas** — **reestructurar pools** (ver § 4)

---

## 4. 🛠️ Reestructuración de TrueNAS pools (con recursos existentes)

### 4.1 Diagnóstico

- **`pool0`**: 4 mirror vdevs (8 SSDs) + 1 mirror special (2 NVMe). 8.8 TB raw, 4.4 TB usable. 57% usado. ✅ OK.
  - mirror-0: sdc + sdf
  - mirror-1: sda + sdi
  - mirror-2: sdb + sdd
  - mirror-3: sde1 (part de sde) + sdh
- **`pool2`**: 1 single disk (`sdi1`... no, era otro. En realidad `sdi` está en pool0 mirror-1. El single disk de pool2 es `56cb3629-acd9-4af0-884c-03f7005551a4` que mapea al HDD 7.3 TB físico en hades, presentado como virtio). **Sin redundancia**. Scrub de 11 meses.
- **`pool0_backup`** vive como dataset dentro de pool2. **NO es backup real** — ambos (pool0 y pool2) están en la misma VM física (truenas) y mismo hardware host (hades).

### 4.2 ❌ Plan A descartado — `sdf` NO es spare

El `zpool status -v` ejecutado en truenas el 2026-06-30 confirma que **`sdf` está en `pool0 mirror-0`** (junto con `sdc`). Los 8 SSDs SATA de hades (sda-sdh) están todos usados en los 4 mirrors de pool0. **No hay disco físico libre en hades para mirror de pool2 sin romper pool0**.

### 4.3 Plan B (recomendado, $0) — Aceptar pool2 single disk + priorizar off-host

**Mantener pool2 como single disk** (no ideal, pero aceptable porque no hay disco libre para mirror sin romper nada).

**Estrategia**:
1. **NO confiar en pool2 como backup**. Marcarlo como "stage temporal, no backup real".
2. **`zfs send` directo desde pool0 → otros destinos** (PBS, hera/kronos ZFS recv, pcloud).
3. **Scrub mensual obligatorio** para detectar bit-rot.
4. **Replicación priorizada a off-host** (PBS, pcloud) — no quedarse con la "copia" en pool2.

**Política de uso de pool2**:
- `pool2/pool0_backup/` → **migrar a kronos pool1** (cuando exista). Dejar de usar como destino de backup.
- `pool2/backup/*` (trading_systems 305 GB, aranea_storage 39 GB, iso_storage 15 GB, etc.) → mantener como archive temporal, **rclone crypt a GDrive mensualmente**.
- `pool2/ix-applications` → apps TrueNAS nativas, mantener.

### 4.4 Plan C — Crear nuevo pool `pool1` (mirror SSD) sin tocar pool0/pool2

Si en el futuro querés un batch diario SSD con redundancia, la única forma **sin comprar** sería:

- Crear `pool1` en **kronos** sobre `local-kronos` (680 GB SSD libre) o `pool-kronos` (730 GB SSD libre).
- **Mirror** requiere 2 discos del mismo tamaño. Solo tenemos 1 SSD libre en kronos (los otros están en LVM/VMs).
- **Single disk** ZFS es factible (sin redundancia pero con scrub mensual).
- **Alternativa**: `pool1` en hera sobre `local-sqx-hera` (931 GB SSD libre, vm 123 stopped), single disk, con `zfs send` off-host como "redundancia" lógica.

**No recomendado para corto plazo** — el off-host real (PBS + pcloud) cumple la función de batch con redundancia lógica.

### 4.5 Recomendación final pools

| Pool | Estado | Estrategia |
|---|---|---|
| **pool0** | sin cambios | Servicios en vivo (NFS datastore, SMB shares, apps) |
| **pool2** | single HDD, marcado como stage | Mantener archive, rclone crypt a GDrive mensual, scrub mensual |
| **NO crear pool1** por ahora | — | PBS off-host + cloud tier cubren el rol de batch con redundancia |

**Decisión arquitectural**: **no tocar pools** en corto plazo. Invertir el esfuerzo en PBS off-host + cloud tier, que da redundancia real sin riesgo de romper ZFS.

---

## 5. ☁️ Tier cloud — pcloud y Google Drive (recursos existentes)

### 5.1 Espacio disponible (política segregada — owner 2026-07-01)

| Provider | Espacio | Ya pagado | Uso propuesto |
|---|---|---|---|
| **pcloud** | 1 TB | sí | **Tier caliente (escaso)**: SOLO configs críticas, dumps DB, secretos. NO bulk. |
| **Google Drive** | varios TB | sí | **Tier bulk**: snapshots ZFS pool0 (`zfs send` → archivo `.zfs`), archive mensual. |

**Por qué segregar**: pcloud (1 TB) es pequeño y el owner lo reservó para cosas irremplazables. GDrive tiene varios TB y es ideal para archive grande de baja prioridad de restore. Ver § 3a y § 3b para detalle de qué va a cada tier.

### 5.2 Setup (rclone + crypt)

```bash
# En hermes-vm o PBS VM
apt install rclone

# Configurar remotes (interactivo: rclone config)
rclone config
# 1. Crear "pcloud" tipo pcloud (OAuth)
# 2. Crear "pcloud-crypt" tipo crypt sobre pcloud:/encrypted
#    filename_encryption=standard
#    directory_name_encryption=true  
#    password=<strong-passphrase-en-bitwarden>
# 3. Crear "gdrive" tipo drive (OAuth Google)
# 4. Crear "gdrive-crypt" tipo crypt sobre gdrive:/aranea-archive

# Verificar
rclone lsd pcloud-crypt:
rclone lsd gdrive-crypt:
```

### 5.3 Política de sync

```bash
# PBS datastore → pcloud (weekly)
rclone sync /backup/pbs-main pcloud-crypt:aranea-pbs-weekly \
  --transfers 4 --bwlimit "08:00,20M 22:00,off" \
  --log-file /var/log/rclone-pbs-pcloud.log --log-level INFO

# pool1/staging (zfs received) → GDrive (monthly)
rclone sync /pool1/staging/cloud_export gdrive-crypt:aranea-archive \
  --transfers 2 --bwlimit "08:00,10M 22:00,off"
```

### 5.4 Costos

**$0 mensual** (usas el espacio que ya tienes contratado en pcloud y GDrive).

Si llegas al límite del espacio actual: ahí sí se discute upgrade. Pero 1 TB pcloud + 1-5 TB GDrive >> capacidad total cluster (~17 TB raw, ~9 TB usados).

### 5.5 Consideraciones

- **Cifrado obligatorio**: `rclone crypt` AES-256 antes de salir. Passphrase en bitwarden + USB cifrado.
- **Bandwidth**: WAN típica Chile 100-300 Mbps. `rclone --bwlimit` nocturno.
- **Verificación**: `rclone check` mensual (valida integridad cifrada).
- **Restore**: solo para DR real (lento, WAN-dependent).

---

## 6. 📋 Política de backup consolidada

### 6.1 Por tipo de dato

| Tipo de dato | Herramienta | Frecuencia | Retención local | Retención off-host |
|---|---|---|---|---|
| **VMs/LXCs Proxmox** | vzdump → PBS | Diario 02:00 critical + Semanal Sat all | 7d + 4w + 12m | sync PBS → pcloud weekly |
| **Ceph RBD (pool1)** | `rbd snap` + `rbd export` | Diario 02:00 | 7d + 4w | export → PBS weekly |
| **ZFS pool0 truenas** | `sanoid` | Hourly + Daily + Weekly + Monthly | 24h + 7d + 4w + 12m | `zfs send` → kronos pool1 daily; → hera semanal |
| **ZFS pool1 truenas** (si Plan A) | `sanoid` | Hourly + Daily + Weekly | 24h + 7d + 4w | rclone crypt → pcloud weekly |
| **ZFS pool1 kronos** (recv) | `sanoid` | Hourly + Daily | 24h + 7d | rclone crypt → GDrive monthly |
| **PostgreSQL (vm 152)** | `pg_dumpall` | Diario 01:00 | 7d | dump → PBS daily |
| **MongoDB (vm 153)** | `mongodump` | Diario 01:30 | 7d | dump → PBS daily |
| **Obsidian vault (lxc 116)** | CouchDB dump | Hourly | 24h | dump → PBS daily |
| **minio (vm 157)** | `mc mirror` | Diario 03:00 | 7d | mirror → PBS weekly |
| **Traefik config** | `tar czf` | Diario 04:00 | 30d | copy → PBS + pcloud |
| **step-ca** | `step ca backup` | Diario 04:30 + pre-change | 90d | backup encriptado → PBS + pcloud |
| **OPNsense config** | UI export XML | Semanal Sat 08:00 | 12w | export → PBS |
| **/etc/pve** | `tar czf` | Semanal Sat 08:30 | 12w | tar → PBS |
| **etcd** | `etcdctl snapshot` | Diario 05:00 | 30d | snap → PBS daily |

### 6.2 Cronograma (gantt)

```mermaid
gantt
    title Backup schedule — Aranea post-mejoras (sin HW nuevo)
    dateFormat HH:mm
    axisFormat %H:%M

    section Hourly
    Obsidian vault (CouchDB)    :h1, 00, 5m
    ZFS snap pool0 (sanoid)     :h2, 30, 5m
    ZFS snap pool1 (sanoid)     :h3, 30, 5m
    section Daily
    PG dump                     :d1, 01:00, 30m
    MongoDB dump                :d2, after d1, 30m
    Ceph RBD snap               :d3, 02:00, 60m
    vzdump critical VMs → PBS   :d4, after d3, 60m
    ZFS daily snap pool0        :d5, after d4, 30m
    Traefik + step-ca backup    :d6, after d5, 10m
    minio mirror                :d7, after d6, 30m
    zfs send pool0 → pool1      :d8, after d7, 60m
    etcd snapshot               :d9, after d8, 10m
    section Weekly
    vzdump ALL VMs → PBS        :w1, sat, 02:00, 4h
    rclone PBS → pcloud         :w2, sun, 03:00, 4h
    OPNsense config export      :w3, sat, 08:00, 30m
    /etc/pve backup             :w4, after w3, 30m
    section Monthly
    Scrub pool0                 :m1, 1st, 02:00, 4h
    Scrub pool1                 :m2, after m1, 4h
    Scrub pool2                 :m3, after m2, 4h
    Restore drill (1 VM)        :m4, 15th, 4h
    rclone pool1 → GDrive       :m5, 1st, 04:00, 12h
```

### 6.3 sanoid policy (ejemplo para truenas)

```yaml
# /etc/sanoid/sanoid.conf (en truenas)
[pool0/aranea_storage]
  use_template = production
[pool0/proxmox_storage]
  use_template = production
[pool0/trading_systems]
  use_template = critical
[pool1/recv]
  use_template = backup

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

---

## 7. 📐 Topología objetivo

```
                            ┌──────────────────────┐
                            │  WAN / Internet      │
                            └─────────┬────────────┘
                                      │
                                ┌─────▼─────┐
                                │  athena   │  ← gateway
                                └─────┬─────┘
                                      │ LAN 192.168.31/24 + Ceph 10.10.10/24
        ┌──────────────┬──────────────┼──────────────┬──────────────┐
        │              │              │              │              │
    ┌───▼───┐      ┌───▼───┐      ┌───▼───┐      ┌───▼───┐      ┌───▼───┐
    │ zeus  │      │ hera  │      │kronos │      │ hades │      │truenas│
    │Ceph   │      │Ceph   │      │Ceph   │      │       │      │(VM)   │
    │OSD.2  │      │OSD.0  │      │OSD.1+3│      │compute│      │pool0  │
    │compute│      │+ ZFS  │      │+ PBS  │      │25 VMs │      │SSD    │
    │       │      │ recv  │      │VM(NEW)│      │+ truenas│    │mirror │
    │       │      │(931GB │      │680GB  │      │VM host│      │       │
    │       │      │libre) │      │libre) │      │       │      │pool1  │
    └───────┘      └───────┘      └───────┘      └───────┘      │mirror │
                                                              │SSD?  │
                                                              │(if sdf)
                                                              └───────┘
                                                                   │
                                                              zfs send
                                                                   ▼
                                                          ┌─────────────┐
                                                          │ hera recv   │
                                                          └─────┬───────┘
                                                                │
                                                          rclone crypt
                                                                ▼
                                                     ┌──────────────────┐
                                                     │ pcloud (1TB)     │
                                                     │ Google Drive     │
                                                     │   (1-5 TB)       │
                                                     └──────────────────┘
```

---

## 8. 📊 Antes / después

| Aspecto | Hoy (2026-06-30) | Target (post-mejoras) |
|---|---|---|
| Off-host real | ❌ no existe | ✅ PBS en kronos |
| Off-site (geo-distinto) | ❌ no existe | ✅ pcloud + GDrive |
| Cifrado off-host | ❌ n/a | ✅ AES-256 rclone crypt |
| pool2 single disk | ⚠️ single disk peligroso | ⚠️ single disk pero con rclone off-host priorizado (mitigación) |
| Snapshots ZFS | parcial, manual | ✅ sanoid hourly/daily/weekly/monthly |
| Backup VMs/LXCs | vzdump a NFS (sin dedup) | ✅ PBS con dedup nativa |
| Restore drill | nunca ejecutado | ✅ mensual calendarizado |
| hades como SPOF | 🔴 no se mitiga (decisión owner) | 🔴 aceptado (no se toca) |
| Migrar TrueNAS a bare-metal | — | ❌ NTH (decisión owner) |
| Política retención | ad-hoc | ✅ sanoid declarativa |
| Monitoreo backups | ❌ silencioso | ✅ rclone logs + PBS verify |
| **Capex** | — | **$0** |
| **Opex mensual cloud** | — | **$0** (espacio ya pagado) |

---

## 9. 📋 Roadmap de implementación (capex $0)

### Fase 0 — Quick wins (esta semana, **$0**)

1. `zpool scrub pool2` en truenas (cerrar alerta 11 meses)
2. `ceph tell osd.0 osd.2 compact` (cerrar HEALTH_WARN fragmentación)
3. **Verificar `sdf` en truenas**: `zpool status -v`, `zpool get spare`, identificar si está libre/spare/ocupado.
4. Configurar `sanoid` en truenas con política retención
5. Documentar `lspci` por nodo (capturar info slots PCIe reales — gap info)

### Fase 1 — PBS en kronos (~1 día, **$0**)

1. Liberar `local-kronos` o `pool-kronos` (migrar vms stopped si necesario; `sqx-ulab-kron-0` vmid 111 stopped, `sqx-ulab-zeus-0` vmid 108 corriendo — evaluar si mantener o apagar)
2. Crear VM PBS (vmid 180) en kronos
3. Install PBS sobre Debian 12 o ISO PBS
4. Crear datastore `main` sobre `local-kronos` SSD SATA libre
5. Crear user `backup@pbs` + API token
6. Registrar storage `aranea-pbs` en los 5 PVE nodes
7. Configurar vzdump schedule (daily-critical + weekly-all)
8. Primer vzdump manual de prueba

### Fase 2 — ~~Destino secundario `zfs recv` en hera~~ → RECHAZADA (2026-07-01)

**Razón**: el owner declara los 3 SSDs `local-sqx-*` (zeus, hera, kronos) como **sagrados** — dedicados a las VMs SQX que son la infraestructura de Echo Forge. Destruir `local-sqx-hera` para hacer `zfs recv` está prohibido.

**Qué reemplaza esta fase**:
- El tier on-cluster `zfs recv` se reemplaza por **PBS off-host** (Fase 1) + **cloud tier** (Fase 3).
- Si en el futuro hay otro SSD libre sin asignar (ej. cuando se consoliden las VMs SQX), se puede reactivar esta idea.
- **Alternativa válida** (no priorizada): usar `pool-kronos` (730 GB libre, `sdc` de kronos, NO es SQX) como destino `zfs recv` secundario. **Decisión pendiente** del owner — ver § 12.6.

> [!warning] Pendiente revisar con owner
> ¿`pool-kronos` puede usarse como destino `zfs recv` (Fase 2 reactivable)? Hoy no es crítico porque PBS + cloud cubren. Pero si quiere on-cluster ZFS send redundante, es la opción menos invasiva.

### Fase 3 — Tier cloud (~medio día, **$0**, usa espacio existente)

**Decisión del owner (2026-07-01)**: pcloud (1 TB) es **escaso**, reservado para configs y datos críticos. GDrive (varios TB) es el **bulk**.

#### 3a. pcloud — Tier caliente (configs + datos críticos, **~1 TB**)

**Va acá**:
- vzdump configs (`/etc/pve`, Traefik dynamic configs, OPNsense XML)
- `step ca backup` (claves privadas, encriptado)
- Dumps de bases de datos (PostgreSQL, MongoDB, CouchDB/Obsidian vault)
- `etcdctl snapshot`
- `mc mirror` de buckets minio críticos
- Manifests críticos (`inventory.md`, doc snapshots)
- Cualquier cosa **chica pero irremplazable** (configs, secretos, estado de cluster)

**NO va acá**:
- Snapshots ZFS de pool0 (demasiado grandes)
- vzdump de VMs completas (van a PBS)

#### 3b. GDrive — Tier bulk (snapshots grandes, **varios TB**)

**Va acá**:
- Snapshots ZFS de pool0 (envío semanal/mensual de `pool0@snap` → `zfs send` → archivo `.zfs` → GDrive)
- Datasets grandes de `aranea_storage`, `trading_documents`, `frigate/media` (NVR es alto volumen, baja prioridad de restore)
- Backups históricos de VMs (cuando se roten de PBS)
- `rclone check` mensual para validar integridad cifrada

**NO va acá**:
- Nada que requiera restore rápido (la WAN es lenta, GDrive es para DR/archive)
- Nada pequeño/crítico (eso va a pcloud)

#### 3c. Setup rclone + crypt

```bash
# En hermes-vm o PBS VM (lo decidimos en Fase 1)
apt install rclone

# Configurar remotes (interactivo: rclone config)
rclone config
# 1. Crear "pcloud" tipo pcloud (OAuth)
# 2. Crear "pcloud-crypt" tipo crypt sobre pcloud:/aranea-configs-crypt
#    filename_encryption=standard
#    directory_name_encryption=true
#    password=<strong-passphrase-en-bitwarden>
# 3. Crear "gdrive" tipo drive (OAuth Google)
# 4. Crear "gdrive-crypt" tipo crypt sobre gdrive:/aranea-archive

# Verificar
rclone lsd pcloud-crypt:
rclone lsd gdrive-crypt:
```

#### 3d. Política de sync

```bash
# PBS datastore + configs críticas → pcloud (weekly domingo)
rclone sync /backup/pbs-main-configs pcloud-crypt:aranea-configs \
  --transfers 4 --bwlimit "08:00,20M 22:00,off" \
  --log-file /var/log/rclone-pbs-pcloud.log --log-level INFO

# Snapshots ZFS pool0 → GDrive archive (monthly 1° del mes)
rclone sync /pool0-snapshots gdrive-crypt:aranea-pool0-archive \
  --transfers 2 --bwlimit "08:00,10M 22:00,off" \
  --log-file /var/log/rclone-pool0-gdrive.log --log-level INFO
```

#### 3e. Optimización de espacio (puntos abiertos con owner)

> [!question] Pendiente discutir con owner
> Owner pidió "algo media tricky para reducir espacio" en backups. Algunas ideas que aplican a este stack:
> - **PBS dedup nativa** (block-level, ya incluida): muy efectiva en VMs con mucho OS base repetido
> - **ZFS `zfs send -w` raw + `-c` compressed**: ahorra WAN y storage
> - **PBS encryption + compression**: estándar
> - **`rclone crypt` con `--partial` y `--low-level-retries`**: para WAN inestable
> - **Versionado por snapshot en lugar de copias completas**: sanoid ya lo hace
> - **Excluir `/var/log`, `/tmp`, caches de VMs**: ahorra 10-20%
> - **BorgBackup / restic sobre rclone**: dedup adicional content-defined, pero suma complejidad
>
> Owner es dev/trading — preferencias: simple, robusto, observable. **Decisión pendiente**.

### Fase 4 — Pool2 scrub mensual + (NTH) mirror (sin tocar pool0) — **$0**

Esta fase reemplaza al "mirror de pool2 con `sdf`" original (que era inviable porque `sdf` ya está en pool0).

1. `zpool scrub pool2` inmediato (cerrar alerta 11 meses)
2. Configurar `sanoid` con política retención para pool2 (template `backup`)
3. Marcar `pool2/backup/*` y `pool2/pool0_backup/` como "stage, no backup" en la doc
4. Migrar `pool2/pool0_backup/` a kronos pool1 (cuando exista) → eliminar dependencia de pool2 como destino de backup
5. **NTH** (not-to-have): mirror SSD de pool2 — solo si en el futuro hay disco libre nuevo. Hoy no aplica.

### Fase 5 — Restore drills (continuo, **$0**)

1. Schedule mensual (rotar VMs drill)
2. Ajustar sanoid retention según uso real
3. Ajustar `rclone bwlimit` según WAN
4. Documentar tiempo/ratio de cada restore

---

## 10. ⚠️ Riesgos y mitigaciones

| Riesgo | Probabilidad | Impacto | Mitigación |
|---|---|---|---|
| hades cae → todo muere (truenas VM + 25 VMs) | Media | Catastrófico | **Aceptado por owner** (no se migra). Mitigación parcial: PBS off-host + cloud tier. |
| `sdf` no es spare real | ~~Media~~ **confirmado** | Bajo | ~~Plan B~~ **Aplicado**: no tocar pool2, fortalecer off-host. `sdf` ya está en pool0 mirror-0 (verificado por zpool status -v 2026-06-30). |
| PBS en kronos comparte host con Ceph MON | Baja | Medio | Si kronos cae → PBS off-host cae + Ceph degraded. Mitigación: cloud tier (pcloud/GDrive) sigue accesible. |
| rclone crypt pierde passphrase | Baja | Catastrófico | Escrow offline: bitwarden offline + USB cifrado. |
| pcloud/GDrive cierran cuenta | Baja | Alto (pierdes off-site) | Mitigación: Tier cloud dual (pcloud + GDrive). Si querés redundancia física, en el futuro un USB rotativo (no prioritario). |
| WAN lento bloquea rclone | Media | Bajo (solo cloud) | `--bwlimit` nocturno + horario. |
| Ceph se fragmenta más | Media | Medio | `ceph tell osd.* compact` mensual. |
| vm 123 (`sqx-ulab-hera-0`) se necesita de vuelta | Baja | Bajo | Si está stopped hace tiempo, ¿se necesita? Validar con owner antes de destruir VG. |
| **pool2 single disk falla (HDD 7.3 TB)** | Media | Alto (pierde archive + backups actuales) | Mitigación: scrub mensual obligatorio + rclone crypt mensual a GDrive (lo importante sale fuera). **No hay forma de mirror sin comprar o romper pool0**. |

---

## 11. 📚 Referencias

- Doc previa Task 2: [[BACKUP-SYSTEM]] (políticas detalladas)
- Auditoría storage: [[AUDIT]]
- **Auditoría crítica topológica**: [[TOPOLOGY-AUDIT]] (anomalías: VGs separados, SSDs consumer, VMs stopped con RAM, iSCSI LUNs sin auditar, etc.)
- Inventario storage: [[inventory]]
- Per-nodo: [[../01-topologia/nodo-zeus]], [[../01-topologia/nodo-hera]], [[../01-topologia/nodo-kronos]], [[../01-topologia/nodo-hades]], [[../01-topologia/nodo-truenas]], [[../01-topologia/nodo-athena]]
- Pools: [[ceph-pool1]], [[truenas-pool0]], [[truenas-pool2]]
- Skill de refresh: `aranea_agent_ro_inventory_refresh`
- Tickets: [[../05-tickets/2026-06-30-013-storage-redesign-backup-design]]

---

## 12. ❓ Decisiones del owner (estado al 2026-07-01)

### Resueltas (iter 4)

1. **PBS datastore**: ✅ **`local-kronos`** (680 GB SSD libre, Samsung 870 QVO). Más pequeño, suficiente para 7d + 4w + 12m de vzdump. `pool-kronos` queda como buffer si se llena.
2. **PBS RAM**: ✅ **8 GB**. Owner prefiere default mínimo y ajustar si las métricas PBS lo piden.
3. **Cloud weekly**: ✅ **Dual segregado**:
   - **pcloud (1 TB)** = solo configs/datos críticos (NO bulk)
   - **GDrive (varios TB)** = bulk snapshots ZFS pool0, archive mensual
4. **`pool0_backup` actual** (dentro de pool2): ✅ **Dejar como está**. No migrar.
5. **vm 123 (`sqx-ulab-hera-0`)**: ✅ **NO TOCAR**. Owner confirma que las 3 VMs SQX (zeus/hera/kronos) son productivas, en mantenimiento actualmente pero **usarán 80% de los recursos de su host cuando estén activas** (SQX = StrategyQuant X, builder de estrategias de trading). Los 3 SSDs `local-sqx-*` son **SAGRADOS**.

### Nuevas decisiones pendientes

6. **Fase 2 reactivable**: ¿Usar `pool-kronos` (730 GB libre, `sdc` de kronos, NO SQX) como destino `zfs recv` secundario on-cluster? Hoy PBS + cloud cubren. Owner puede decir "no por ahora".
7. **Optimización de espacio en backups**: ✅ **Opción A** (PBS dedup nativa + ZFS raw/compressed + excluir caches de VMs). Conservadora, baja complejidad, ~40-60% reducción PBS + ~30% cloud. Owner prefiere simple y robusto. Si las métricas muestran problemas de espacio después, se puede escalar a Opción B (Borg/restic).
8. **Pool1 (Ceph) backup externo**: ✅ **NO agregar** (decidido 2026-07-01). 3× replication + vzdump a PBS de las VMs es suficiente. RDB export externo es redundante.

### Iteraciones de la propuesta

- Iter 1: capex ~$650 USD (rechazada)
- Iter 2: capex $0, asumía `sdf` spare (rechazada al validar)
- Iter 3: capex $0, Plan B definitivo (pool2 single disk + off-host priorizado)
- **Iter 4 (vigente, 2026-07-01)**: `local-sqx-*` declarados sagrados → Fase 2 descartada, política cloud segregada (pcloud=critical, GDrive=bulk)

> **Eliminado de la lista**: validación de `sdf1` como spare → ya verificado, `sdf` está en pool0 mirror-0 (no es spare).

---

**Estado**: propuesta pendiente de revisión y decisiones. Cero cambios ejecutados.
**Capex**: **$0**. **Opex mensual cloud**: **$0** (espacio ya contratado).

**Captured**: 2026-06-30 19:44 UTC (snapshot fresco).
**Diseñado**: 2026-06-30 por ariadna, **restricciones del owner aplicadas**: sin HW nuevo, sin migración TrueNAS, sin cambio de cantidad de servidores.
