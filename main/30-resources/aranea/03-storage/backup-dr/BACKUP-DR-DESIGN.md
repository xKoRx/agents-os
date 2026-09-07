---
title: "BACKUP-DR-DESIGN — Diseño final Backup/DR Aranea"
type: doc
schema_version: 1
status: active
status_detail: "Diseño final corregido. Una sola verdad activa. Supersede DESIGN-PROPOSAL.md. Decisiones congeladas en §3."
icon: 🛡️
slug: backup-dr-design
area: "[[Personal]]"
project: "[[AGENTS OS]]"
created: 2026-07-01
updated: 2026-08-10
revision_note: "Iter 5 (2026-07-01): refactor completo. Sin contradicciones activas. 14 decisiones congeladas. Decisión del owner 2026-07-01: 'cerrar sesión al terminar'. No ejecutado."
aliases:
  - Backup DR design
  - Aranea backup design
  - BACKUP-DR
tags:
  - kind/doc
  - area/personal
  - project/agents-os
  - domain/backup-dr
  - doc/design
  - lifecycle/frozen
  - authority/canonical
related:
  - "[[DIFF-CONCEPTUAL]]"
  - "[[../DESIGN-PROPOSAL]]"
  - "[[../PROPUESTA-COMPLETA-ITER4]]"
  - "[[../BACKUP-SYSTEM]]"
  - "[[../TOPOLOGY-AUDIT]]"
  - "[[../inventory]]"
  - "[[../../01-topologia/nodo-hades]]"
  - "[[../../01-topologia/nodo-truenas]]"
  - "[[../../01-topologia/nodo-kronos]]"
  - "[[../../01-topologia/nodo-hera]]"
  - "[[../../01-topologia/nodo-zeus]]"
  - "[[../../01-topologia/nodo-athena]]"
  - "[[../../../05-tickets/2026-06-30-013-storage-redesign-backup-design]]"
  - "[[../../../05-tickets/2026-06-30-011-aranea-storage-audit-backup]]"
supersedes:
  - "[[../DESIGN-PROPOSAL]]"
  - "[[../PROPUESTA-COMPLETA-ITER4]]"
cssclasses:
  - wide
---

# 🛡️ BACKUP-DR-DESIGN — Diseño final Backup/DR Aranea

## Propósito

Mantener el diseño final congelado y la policy de referencia de Backup/DR Aranea, preservando sus decisiones sin confundirlo con el contrato vivo del proyecto.

## Contenido

> **Status**: design-frozen (cero cambios ejecutados). Capa de policy.
> **Supersede**: `DESIGN-PROPOSAL.md` y `PROPUESTA-COMPLETA-ITER4.md` (mantenidos como histórico).
> **Diferencia con propuesta anterior**: este doc es la **única verdad activa**. Cualquier contradicción con otros docs = gana este.
> **Filosofía**: Policy-first · Runbook-driven · Skill-executed · Memory-informed · Inventory-grounded · Human-approved-for-dangerous-actions.

---

## 0. TL;DR (1 página)

**Cluster**: 5 Proxmox VE + 1 TrueNAS Scale (VM en hades) + 1 Hermes VM = 7 máquinas. 302 threads / 767 GB RAM / ~17.6 TB raw / ~9 TB usados (~51%).

**Restricciones duras (no negociables)**:
1. Cero capex.
2. No migrar TrueNAS a bare-metal.
3. No agregar/sacar servidores.
4. `local-sqx-{zeus,hera,kronos}` son **SAGRADOS** (SQX/Echo Forge).

**Diagnóstico**: la capacidad alcanza y sobra. El problema es organización, no capacidad.

**Solución en 4 capas**:
1. **Capa A — Configuración crítica**: `/etc/pve`, Traefik, OPNsense, step-ca, etcd, manifests. → **PBS** + **pcloud** (Restic).
2. **Capa B — Datos app-consistent**: PostgreSQL, MongoDB, CouchDB, minio, ZFS pool0. → **PBS** + **pcloud/GDrive**.
3. **Capa C — VMs/LXCs**: tier 0/1/2/3. → **PBS** (vzdump diario + semanal).
4. **Capa D — Snapshots locales**: sanoid hourly/daily/weekly/monthly en pool0 y pool2 (ZFS only). NO son backup DR.
5. **Capa E — Datasets ZFS**: `zfs send -w -c` chunked, manifest, checksums. → **GDrive** bulk.
6. **Capa F — Cloud/off-site**: tier crítico (Restic/Borg cifrado, versionado, check) + tier bulk (chunking + manifest).
7. **Capa G — Restore drills**: mensual rotativo con criterios PASS/FAIL explícitos.

**Capex**: $0. **Opex mensual cloud**: $0 (espacio ya contratado).

**Resultado esperado post-implementación**:
- Off-host real: ✅ PBS en kronos.
- Off-site: ✅ pcloud + GDrive.
- Cifrado off-host: ✅ Restic/Borg AES-256 + rclone crypt.
- Snapshots automatizados: ✅ sanoid declarativo.
- vzdump con dedup: ✅ PBS nativa.
- Restore drills mensuales: ✅ calendarizado.
- Observabilidad: ✅ alertas mínimas con thresholds.
- Secret Zero: ✅ documentado con escrow offline.
- Pool0_backup vs pool0 backup: ✅ glosario aclarado.

---

## 1. Glosario

| Término | Significado |
|---|---|
| **pool0** | ZFS pool en truenas VM (4 mirror SSD + special mirror). Producción primaria. |
| **pool2** | ZFS pool en truenas VM (single disk HDD 7.3 TB). **Stage temporal, no backup DR**. |
| **`pool0_backup`** | Dataset específico dentro de pool2 (`pool2/pool0_backup/`). **Snapshot semanal, mismo host**. NO es backup DR. |
| **"backup pool0"** | Política sanoid de snapshots sobre el pool0 mismo. Snapshots locales. NO son backup DR. |
| **PBS** | Proxmox Backup Server. Corre en VM dedicada en kronos. Off-host en LAN. |
| **Datastore PBS** | Volumen donde PBS guarda chunks dedupeados. En este diseño: `local-kronos` (680 GB SSD libre). |
| **Tier crítico** | Cloud tier para configs/secretos/dumps. **pcloud (1 TB)** + Restic/Borg cifrado + versionado. |
| **Tier bulk** | Cloud tier para snapshots grandes/archive. **GDrive (varios TB)** + rclone crypt + chunking. |
| **Sanoid** | Tool declarativa para autosnap + autoprune en ZFS. |
| **PBS dedup** | Deduplicación block-level nativa de PBS. |
| **Restore drill** | Prueba programada de restore. Backup no es válido sin drill PASS reciente. |
| **Secret Zero** | Passphrase/clave maestra más sensible del sistema de backup. Escrow offline obligatorio. |
| **Sagrados SQX** | Los 3 SSDs `local-sqx-{zeus,hera,kronos}` dedicados a infraestructura SQX/Echo Forge. NO TOCAR. |

---

## 2. Recursos protegidos (NO TOCAR)

| Recurso | Ubicación | Estado | Quién protege |
|---|---|---|---|
| `local-sqx-zeus` (931 GB WD Green SATA, `sda` de zeus) | zeus | Sagrado SQX — datasets vm 108 sqx-ulab-zeus-0 | Owner (regla 2026-07-01) |
| `local-sqx-hera` (931 GB WD Green SATA, `sda` de hera) | hera | Sagrado SQX — datasets vm 123 sqx-ulab-hera-0 | Owner (regla 2026-07-01) |
| `local-sqx-kronos` (931 GB WD Green SATA, `sda` de kronos) | kronos | Sagrado SQX — datasets vm 111 sqx-ulab-kron-0 | Owner (regla 2026-07-01) |
| Ceph OSDs (osd.0, osd.1, osd.2, osd.3) | hera/kronos/zeus/kronos | Producción Ceph | Sistema |
| pool0 mirror vdevs (8 SSDs SATA en hades) | truenas VM | Producción pool0 | Sistema |
| pool0 special mirror (2 NVMe en hades) | truenas VM | Producción pool0 metadata | Sistema |
| pool2 (HDD 7.3 TB single disk) | truenas VM | Stage (no producción crítica) | Sistema |
| Truenas VM misma (no migrar) | hades | Hypervisor | Owner (regla 2026-06-30) |
| VMs SQX corriendo (108 sqx-ulab-zeus-0) | zeus | Producción SQX | Owner |
| VMs SQX stopped (111, 123, 162, 170) | kronos/hera/kronos/zeus | En mantenimiento, NO destruir | Owner |

**Cualquier acción que toque un recurso protegido requiere marcar `DANGEROUS` y aprobación explícita del owner.**

---

## 3. Decisiones congeladas

| # | Decisión | Estado | Motivo | Evidencia | Fecha | Impacto |
|---|---|---|---|---|---|---|
| F-01 | Cero capex | FROZEN | Owner restricción hard | Mensaje 2026-06-30 | 2026-06-30 | Sin comprar HW. |
| F-02 | No migrar TrueNAS a bare-metal | FROZEN | Owner restricción hard | Mensaje 2026-06-30 | 2026-06-30 | hades sigue como hypervisor. |
| F-03 | No agregar ni sacar servidores | FROZEN | Owner restricción hard | Mensaje 2026-06-30 | 2026-06-30 | 5 Proxmox + truenas-vm + hermes-vm. |
| F-04 | `local-sqx-{zeus,hera,kronos}` son sagrados | FROZEN | Owner declaración explícita | Mensaje 2026-07-01 | 2026-07-01 | NO se tocan para nada que no sea SQX. |
| F-05 | `sdf` está en `pool0 mirror-0` (NO spare) | FROZEN | Validado `zpool status -v` | Discovery truenas 2026-06-30 | 2026-06-30 | No hay disco libre hades para mirror pool2. |
| F-06 | PBS datastore = `local-kronos` (680 GB libre, Samsung 870 QVO) | FROZEN | Owner decisión | Mensaje 2026-07-01 | 2026-07-01 | SSD en kronos, `sdb`. |
| F-07 | PBS RAM = 8 GB (default mínimo) | FROZEN | Owner decisión | Mensaje 2026-07-01 | 2026-07-01 | Ajustar si métricas lo piden. |
| F-08 | Cloud segregado: pcloud=critical, GDrive=bulk | FROZEN | Owner decisión | Mensaje 2026-07-01 | 2026-07-01 | Tier aislado por criticidad. |
| F-09 | `pool0_backup` (dataset en pool2) no se migra | FROZEN | Owner decisión | Mensaje 2026-07-01 | 2026-07-01 | Se queda donde está. |
| F-10 | Sin backup externo Ceph (RBD export) | FROZEN | Owner decisión | Mensaje 2026-07-01 | 2026-07-01 | 3× replication + vzdump PBS cubren. |
| F-11 | Optimización = Opción A (PBS dedup + ZFS raw/compressed + excluir caches) | FROZEN | Owner decisión | Mensaje 2026-07-01 | 2026-07-01 | Conservadora, simple. |
| F-12 | Fase 2 (zfs recv on-cluster) DESCARTADA | FROZEN | Sagrados SQX, sin SSD libre alternativo | Mensaje 2026-07-01 | 2026-07-01 | PBS + cloud reemplazan. |
| F-13 | hades SPOF aceptado | FROZEN | Owner decisión | Mensaje 2026-06-30 | 2026-06-30 | PBS off-host en kronos sobrevive. |
| F-14 | pool2 single disk aceptado, scrub mensual obligatorio | FROZEN | Sin disco libre para mirror | Iter 3 + validado | 2026-06-30 | Mitigado con cloud tier. |

**Cambiar cualquier decisión congelada requiere Request Change aprobado por owner. Ver `REQUEST-CHANGES.md`.**

---

## 4. Decisiones pendientes (no congeladas)

| # | Decisión | Bloquea | Owner task |
|---|---|---|---|
| P-01 | ¿Reactivar Fase 2 con `pool-kronos` (730 GB libre, NO SQX) como destino `zfs recv` secundario on-cluster? | Mejora opcional. | OWNER-TASK-OPT-ZFS-RECV |
| P-02 | Definición de "critical VMs" (tier 0): ¿cuáles VMs/LXCs? | agent-project-02 PBS policy. | OWNER-TASK-CRITICAL-VMS |
| P-03 | Ventana de mantenimiento preferida para acciones DANGEROUS | Calendario implementación. | OWNER-TASK-MAINT-WINDOW |
| P-04 | Ubicación física del Secret Zero (caja fuerte, USB cifrado en oficina, segunda casa) | Secret Zero section ejecutable. | OWNER-TASK-SECRET-ZERO |
| P-05 | ¿OAuth tokens pcloud/GDrive los maneja el owner en persona o el agente puede hacerlo? | agent-project-04/05. | OWNER-TASK-OAUTH-SCOPE |

---

## 5. Arquitectura por capas

### Capa A — Configuración crítica

Incluye:
- configuración de nodos (`/etc/pve`, `/etc/network/interfaces`, ssh config);
- configuración de cluster (`/etc/corosync/`, `/etc/ceph/`, etcd);
- red/firewall/DNS/VPN (OPNsense export XML);
- configuración de storage (`sanoid.conf`, `pve storage.cfg`);
- configuración de servicios base (Traefik dynamic configs, step-ca, OPNsense);
- certificados, CA y llaves (`step ca backup` encriptado);
- inventario (`backup-inventory-template.json`);
- manifests críticos;
- runbooks;
- exports de plataformas administradas.

**Tabla por elemento**:

| Elemento | Método | Frecuencia | Destino local | Destino off-site | Verificación | Restore | Owner tasks | Agent tasks |
|---|---|---|---|---|---|---|---|---|
| `/etc/pve/*` | `tar czf` | Semanal Sat 08:30 | PBS datastore | pcloud-crypt (Restic) | `tar tzf` smoke test | `tar xzf` + reinicio servicio | OWNER-TASK-PBS-SCHED | AGENT-TASK-ETCPVE-BACKUP |
| Traefik dynamic configs | `tar czf` | Diario 04:00 | PBS datastore | pcloud-crypt (Restic) | smoke test | restore + reload Traefik | OWNER-TASK-PBS-SCHED | AGENT-TASK-TRAEFIK-BACKUP |
| OPNsense config | UI export XML | Semanal Sat 08:00 | PBS datastore | pcloud-crypt (Restic) | XML valid parse | UI import | OWNER-OPNSENSE-EXPORT | AGENT-TASK-OPNSENSE-BACKUP |
| step-ca | `step ca backup` | Diario 04:30 + pre-change | PBS datastore (encriptado) | pcloud-crypt (Restic) | `step ca verify` | `step ca restore` + verificar firma | OWNER-TASK-PBS-SCHED | AGENT-TASK-STEPCA-BACKUP |
| etcd cluster | `etcdctl snapshot save` | Diario 05:00 | PBS datastore | pcloud-crypt (Restic) | `etcdctl snapshot status` | restore + `etcdctl snapshot restore` | OWNER-TASK-PBS-SCHED | AGENT-TASK-ETCD-BACKUP |
| Inventario (markdown + JSON) | `cp` + commit | Diario 06:00 | PBS datastore | pcloud-crypt (Restic) | JSON schema valid | restore + verificar conteos | OWNER-TASK-INVENTORY-POLICY | AGENT-TASK-INVENTORY-BACKUP |
| Sanoid policy | `cp /etc/sanoid/sanoid.conf` | post-cambio | PBS datastore | pcloud-crypt (Restic) | diff contra git | restore + reload sanoid | OWNER-TASK-PBS-SCHED | AGENT-TASK-SANOID-BACKUP |
| Runbooks críticos | `tar czf` | post-cambio | PBS datastore | pcloud-crypt (Restic) | `tar tzf` smoke | restore + lectura | OWNER-TASK-PBS-SCHED | AGENT-TASK-RUNBOOK-BACKUP |

### Capa B — Datos app-consistent

| Servicio | Método | Consistencia | Frecuencia | Retención | Destino | Verificación | Restore | Riesgos |
|---|---|---|---|---|---|---|---|---|
| **PostgreSQL** (vm 152) | `pg_dumpall` + `pg_dump --schema` | app-consistent | Diario 01:00 | 7d local PBS | PBS datastore + pcloud-crypt | `pg_restore --list` + count tables | `createdb` + `psql < dump.sql` | DB en uso requiere `pg_dump --lock-wait-timeout` |
| **MongoDB** (vm 153) | `mongodump --oplog` | app-consistent | Diario 01:30 | 7d local PBS | PBS datastore + pcloud-crypt | `mongorestore --dryRun` | `mongorestore --oplogReplay` | oplog window >24h |
| **Obsidian vault** (lxc 116) | CouchDB dump (`curl /_all_dbs` + replicador) | eventually consistent | Diario 00:00 | 7d local PBS + 30d pcloud | PBS datastore + pcloud-crypt | doc count match | restore CouchDB + LiveSync pull | replicación puede perder cambios < 24h |
| **minio** (vm 157) | `mc mirror --remove --overwrite` | eventual | Diario 03:00 | 7d local PBS | PBS datastore + pcloud (solo bucket crítico) | `mc ls` count match | `mc mirror` inverso | sync bidireccional requiere cuidado |
| **ZFS pool0 datasets** | sanoid (hourly/daily/weekly/monthly) | crash-consistent | hourly + daily + weekly + monthly | 24h + 30d + 8w + 12m | snapshots locales + `zfs send -w -c` chunked → GDrive | `zfs send -R | zfs recv` test | `zfs recv` desde snapshot | snapshots ≠ backup DR |

### Capa C — VMs/LXCs (tiers)

| Tier | Tipo | Backup | Retención inicial | Excluir | Restore drill |
|---|---|---|---|---|---|
| **Tier 0** | crítico/acceso/red/control plane | diario PBS + off-site semanal | conservadora (7d + 4w + 12m) | nada esencial | mensual |
| **Tier 1** | productivo | diario o cada 2 días | conservadora (7d + 4w + 6m) | caches/logs | mensual rotativo |
| **Tier 2** | importante/reconstruible | semanal | baja/media (4w + 6m) | caches | trimestral |
| **Tier 3** | pesado/lab/reproducible | manual/selectivo | mínima (4w) | media/caches/ISOs | según necesidad |

**Tier 0 (candidatos a confirmar con owner en P-02)**:
- step-ca (CTID 200 en athena) — claves privadas, control plane TLS.
- OPNsense VM (si corre como VM) — gateway.
- postgresql (152), mongodb (153) — DBs producción.
- mt4-real, mt5-real — trading producción.
- obsidian-sync (CouchDB) — Second Brain del owner.

**Tier 1**: sqx-ulab-* cuando estén activas, ubuntu-dev, kafka-kronos, etcd, traefik, mcps, echo, temporal.

**Tier 2**: VMs stopped la mayoría del tiempo (sqx-ulab-kron-1, sqx-ulab-zeus-1, ryma-linux, mt4-test, kronos-sqx, agent), docker-observability, frigate.

**Tier 3**: lab, dev efímero, ISOs.

**No prometer retención anual sin validar capacidad real y ratio de deduplicación**.

### Capa D — Snapshots locales

```
Snapshot local = rollback rápido.
Snapshot local != backup DR.
```

| Pool | Template | Snapshots | Pruning |
|---|---|---|---|
| pool0 (datasets producción) | critical | hourly 48 + daily 90 + weekly 12 + monthly 24 + yearly 5 | automático vía sanoid |
| pool0 (datasets archive) | production | hourly 24 + daily 30 + weekly 8 + monthly 12 | automático vía sanoid |
| pool2 (stage) | backup | daily 14 + weekly 8 + monthly 12 | automático vía sanoid |

### Capa E — Datasets ZFS / storage

Para datasets grandes (NVR frigate/media, aranea_storage, trading_documents):
- snapshots locales (Capa D).
- `zfs send -w -c poolX/ds@snap > chunk-NNN.zfs` chunked.
- checksums SHA-256 por chunk.
- manifest JSON con `{chunk, size, sha256, source_snap, created_at}`.
- restore test sobre chunk subset.

**NO usar archivo gigante único sin manifest y prueba de recuperación**.

### Capa F — Cloud/off-site

#### F.1 Tier crítico (pcloud + Restic)

Preferencia: **Restic** o **BorgBackup** sobre backend cifrado.
- versionado real (`restic snapshots`).
- `restic check` programado.
- passphrase en Secret Zero.

**Va acá**:
- configs Capa A.
- dumps Capa B.
- manifests.
- inventories.
- runbooks.
- secrets encriptados (step-ca backup).

**NO va acá**: snapshots ZFS de pool0 (van a GDrive bulk).

#### F.2 Tier bulk/archive (GDrive + rclone crypt)

Debe incluir:
- chunking (no archivo único > 50 GB).
- checksums (`.sha256` sidecar).
- manifests (`manifest.json`).
- prueba de restore parcial (drill mensual).

**Va acá**:
- snapshots ZFS pool0 chunked.
- datasets grandes (aranea_storage, frigate/media).
- backups históricos de VMs (cuando roten de PBS).

**NO va acá**: nada que requiera restore rápido (la WAN es lenta).

### Capa G — Restore drills

| Drill | Frecuencia | Alcance | Responsable | Evidencia | PASS/FAIL |
|---|---|---|---|---|---|
| Restore 1 VM tier 0 desde PBS | Mensual | VM crítica completa | Agente | log + boot verification | PASS si VM arranca y servicios responden |
| Restore dump PostgreSQL | Mensual | DB completa a DB scratch | Agente | log + row count match | PASS si count y checksum matchean |
| Restore dump MongoDB | Mensual | DB completa a DB scratch | Agente | log + collection count match | PASS si count y checksum matchean |
| Restore Restic repo desde pcloud | Trimestral | subset de configs | Agente | log + diff contra producción | PASS si configs idénticas |
| Restore ZFS chunk desde GDrive | Trimestral | 1 chunk random | Agente | log + `zfs recv` success | PASS si dataset recibe y monta |
| Restore step-ca completo | Semestral | backup encriptado → CA recovery | Owner | log + cert verification | PASS si CA firma certs nuevos |

---

## 6. Política detallada (resumen)

La policy ejecutable está en `backup-policy.yaml`. Esta sección resume.

### 6.1 Tiers de backup

| Tier | Retention local | Retention off-site critical | Retention off-site bulk |
|---|---|---|---|
| 0 critical | 7d + 4w + 12m | 90d Restic | — |
| 1 productive | 7d + 4w + 6m | 30d Restic | 6m rclone bulk |
| 2 reconstructible | 4w + 6m | — | — |
| 3 lab | 4w | — | — |

### 6.2 Frecuencias

| Job | Frecuencia | Hora |
|---|---|---|
| CouchDB dump | Diario | 00:00 |
| PG dump | Diario | 01:00 |
| MongoDB dump | Diario | 01:30 |
| ZFS hourly snap pool0 | Horario | :30 |
| Ceph RBD snap | Diario | 02:00 |
| vzdump tier 0 → PBS | Diario | 02:00 |
| ZFS daily snap pool0 | Diario | 03:30 |
| minio mirror | Diario | 03:00 |
| Traefik config | Diario | 04:00 |
| step-ca backup | Diario | 04:30 |
| etcd snapshot | Diario | 05:00 |
| Inventory commit | Diario | 06:00 |
| vzdump tier 1/2 → PBS | Semanal | Sat 02:00 |
| OPNsense config | Semanal | Sat 08:00 |
| /etc/pve backup | Semanal | Sat 08:30 |
| Restic push pcloud-crit | Semanal | Sun 03:00 |
| rclone push gdrive-bulk | Mensual | 1st 04:00 |
| Scrub pool0 | Mensual | 1st 02:00 |
| Scrub pool2 | Mensual | 2nd 02:00 |
| Restore drill tier 0 | Mensual | 15th 04:00 |

### 6.3 Exclusiones vzdump

- `/var/log/*` (solo últimos 7d).
- `/tmp/*`.
- `/var/cache/*`.
- `/var/lib/ceph/*` (en VMs compute, no en OSD nodes).
- swap partitions.

### 6.4 Verificación

- **PBS verify**: semanal (PBS nativo).
- **Restic check**: semanal (sobre último snapshot de cada tier).
- **rclone check**: mensual sobre subset random de chunks.
- **ZFS scrub**: mensual.
- **Ceph scrub**: semanal.
- **SMART short**: semanal. SMART long: mensual.

### 6.5 Restore drills (ver §5 Capa G).

---

## 7. Secret Zero / Escrow offline

### 7.1 Inventario de secretos requeridos

| Secreto | Tipo | Quién genera | Dónde se usa |
|---|---|---|---|
| PBS datastore encryption key | passphrase | agente en setup PBS | cifra datastore PBS |
| PBS API token | secret | agente en setup PBS | auth PVE nodes |
| pcloud OAuth refresh token | OAuth | owner flow OAuth | rclone pcloud remote |
| pcloud-crypt passphrase | passphrase | agente | cifra Restic repo en pcloud |
| gdrive OAuth refresh token | OAuth | owner flow OAuth | rclone gdrive remote |
| gdrive-crypt passphrase | passphrase | agente | cifra rclone crypt en GDrive |
| step-ca backup encryption key | passphrase | step-ca | cifra backup step-ca |
| etcd cluster certs | TLS | etcd | restaurar etcd |
| SSH admin key (root@*) | SSH key | owner | acceso admin recovery |
| bitwarden recovery code | 2FA recovery | bitwarden | recuperar vault bitwarden |

### 7.2 Procedimiento de escrow (reglas)

1. **Todos los secretos se almacenan en bitwarden** (vault dedicado).
2. **Bitwarden recovery code** + master password se imprimen en papel y se guardan en **caja fuerte física** (ubicación: pendiente owner P-04).
3. **Passphrases críticas** (PBS, Restic, crypt) se duplican en **USB cifrado** (LUKS) guardado en **segunda ubicación física** (pendiente owner P-04).
4. **Rotación**: cada 12 meses o ante incidente.
5. **Procedimiento de recuperación desde cero**: ver runbook `BACKUP-DR-RUNBOOK.md §8`.

### 7.3 Validación de escrow

Mensualmente el agente verifica:
- bitwarden vault accesible.
- USB cifrado legible y con contenido.
- Caja fuerte accesible (owner confirma).

Si falla alguno → alerta crítica.

---

## 8. Observabilidad y alertas

### 8.1 Stack objetivo

Pendiente definir stack (no existe Prometheus/Grafana centralizado hoy — gap #6 del roadmap Aranea). Mientras tanto, integración mínima con `docker-observability` en hades (existente).

### 8.2 Alertas mínimas

| Alert | Severity | Signal | Threshold | Action | Runbook link |
|---|---|---|---|---|---|
| `backup_critical_stale` | critical | último backup crítico | > 26h | Notificar owner, page | `BACKUP-DR-RUNBOOK §3` |
| `pbs_datastore_full` | critical | % uso datastore PBS | > 80% | Expandir o prune | `BACKUP-DR-RUNBOOK §4` |
| `pbs_verify_failed` | critical | PBS verify job exit code | != 0 | Investigar y reintentar | `BACKUP-DR-RUNBOOK §4` |
| `pbs_prune_gc_failed` | warning | PBS prune/GC exit code | != 0 | Investigar y reintentar | `BACKUP-DR-RUNBOOK §4` |
| `restic_check_failed` | critical | Restic check exit code | != 0 | Investigar corrupción | `BACKUP-DR-RUNBOOK §5` |
| `rclone_sync_failed` | warning | rclone exit code | != 0 | Reintentar, notificar si > 8d | `BACKUP-DR-RUNBOOK §5` |
| `cloud_sync_stale` | warning | días desde último sync pcloud/GDrive | > 8d | Investigar y forzar | `BACKUP-DR-RUNBOOK §5` |
| `zfs_scrub_errors` | critical | `zpool status` reports errors | > 0 | Aislar disco, restaurar desde backup | `BACKUP-DR-RUNBOOK §6` |
| `smart_pending_sectors` | warning | SMART pending | > 0 | Reemplazo programado | `BACKUP-DR-RUNBOOK §7` |
| `smart_reallocated_sectors` | critical | SMART reallocated | > 0 | Reemplazo urgente | `BACKUP-DR-RUNBOOK §7` |
| `pool_health_warning` | warning | `zpool status` reports DEGRADED | != ONLINE | Diagnosticar | `BACKUP-DR-RUNBOOK §6` |
| `ceph_health_warning` | warning | `ceph health` | != HEALTH_OK | Diagnosticar | `BACKUP-DR-RUNBOOK §6` |
| `db_dump_failed` | critical | PG/Mongo dump exit code | != 0 | Investigar y reintentar | `BACKUP-DR-RUNBOOK §3` |
| `etcd_snapshot_failed` | warning | etcd snapshot exit code | != 0 | Investigar | `BACKUP-DR-RUNBOOK §3` |
| `staging_disk_full` | warning | % uso staging area | > 85% | Liberar staging viejo | `BACKUP-DR-RUNBOOK §3` |
| `restore_drill_overdue` | warning | días desde último drill PASS | > 35 | Programar drill urgente | `BACKUP-DR-RUNBOOK §8` |

### 8.3 Canales de notificación

| Severidad | Canal |
|---|---|
| critical | Telegram (owner) + email + dashboard banner |
| warning | dashboard banner + log entry |
| info | log entry |

---

## 9. Topología objetivo (post-implementación)

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
    │       │    │       │    │VM(180)│    │+ truenas│  │mirror │
    │[SDA]  │    │[SDA]  │    │       │    │ VM    │    │       │
    │SAGRADO│    │SAGRADO│    │[SDA]  │    │       │    │pool2  │
    │       │    │       │    │SAGRADO│    │       │    │HDD    │
    │       │    │       │    │       │    │       │    │single │
    │       │    │       │    │[SDB]  │    │       │    │       │
    │       │    │       │    │PBS ds │    │       │    │       │
    │       │    │       │    │680GB  │    │       │    │       │
    └───────┘    └───────┘    └───────┘    └───────┘    └───────┘
      ↑              ↑            ↑             ↑            │
      │              │            │             │            │
      └─── vzdump ───┴─── vzdump ─┴── vzdump ───┘            │
                       → PBS datastore (kronos local-kronos)  │
                                ↑                            │
                                │                            │
                       ┌────────┴──────────┐                 │
                       │                   │                 │
                  Restic push          zfs send             │
                  weekly               monthly              │
                       ↓                   ↓                 │
              ┌──────────────┐   ┌──────────────┐            │
              │ pcloud-crypt │   │ gdrive-crypt │            │
              │ tier critical│   │ tier bulk    │            │
              │ ~1 TB        │   │ varios TB    │            │
              └──────────────┘   └──────────────┘            │
                       ↑                   ↑                 │
                       └────── Restic check / rclone check ──┘
```

---

## 10. Riesgos y mitigaciones

| # | Riesgo | Probabilidad | Impacto | Mitigación |
|---|---|---|---|---|
| R-01 | hades cae → truenas VM + 25 VMs mueren | Media | Catastrófico | **Aceptado F-13**. PBS off-host en kronos sobrevive. cloud tier accesible. |
| R-02 | PBS en kronos comparte host con Ceph MON | Baja | Medio | Si kronos cae → PBS off-host cae + Ceph degraded. Cloud tier (pcloud/GDrive) sigue accesible. |
| R-03 | rclone crypt / Restic pierde passphrase | Baja | Catastrófico | Secret Zero §7 + escrow offline caja fuerte + USB cifrado. |
| R-04 | pcloud cierra cuenta | Baja | Alto (pierde tier critical off-site) | Tier crítico tiene GDrive como fallback (ver Capa F). |
| R-05 | GDrive cierra cuenta | Baja | Alto (pierde tier bulk) | tier bulk no es crítico, datos están en pool0 local + PBS local. |
| R-06 | WAN lento bloquea rclone/Restic | Media | Bajo (solo cloud) | `--bwlimit` nocturno + horario + retry exponencial. |
| R-07 | Ceph se fragmenta más | Media | Medio | `ceph tell osd.* compact` mensual. |
| R-08 | SSD WD Green (Sagrados SQX) falla | Media | Medio | SQX en mantenimiento actual, vm 108 running. vzdump daily tier 1 cubre VM completa. Datasets SQX dentro de VM. |
| R-09 | pool0 mirror disco falla | Baja | Alto | Mirror + spare NVMe (special). ZFS resilver. vzdump diario + cloud tier. |
| R-10 | pool2 single disk falla | Media | Alto (stage + `pool0_backup`) | Scrub mensual + rclone crypt mensual a GDrive tier bulk. NO mirror sin comprar. |
| R-11 | step-ca pierde claves privadas | Baja | Crítico (CA rota, todos los certs internos mueren) | `step ca backup` diario encriptado → PBS + pcloud-crit. Drill semestral. |
| R-12 | etcd consensus pierde quorum | Baja | Crítico (cluster Proxmox degraded) | Snapshot diario PBS + pcloud-crit. Restore drill anual. |
| R-13 | Bitwarden vault inaccesible | Baja | Alto | Recovery code + USB cifrado con subset crítico de secretos. |
| R-14 | Caja fuerte inaccesible | Baja | Alto (Secret Zero perdido) | Caja fuerte debe tener segundo método de acceso (pendiente owner P-04). |
| R-15 | Restore drill falla repetidamente | Baja | Crítico (no confiamos en backups) | Escalar a Request Change inmediato + auditoría profunda del stack de backup. |

---

## 11. Modelo conceptual aplicado

| Artefacto | Doc que lo define | Ejemplo |
|---|---|---|
| **Policy** (límites duros) | este doc §3, §6 + `backup-policy.yaml` | Decisión F-04 Sagrados SQX; tier 0 = crítico, retention 12m. |
| **Runbook** (verdad operacional humana) | `BACKUP-DR-RUNBOOK.md` | Cómo restaurar VM tier 0 desde PBS. |
| **Skill** (habilidad ejecutable agente) | `~/.hermes/profiles/ariadna/skills/devops/aranea_agent_ro_inventory_refresh/SKILL.md` (existente) + futuras skills de backup | `aranea_pbs_add_storage`, `aranea_restic_push`, `aranea_restore_drill`. |
| **Memory** (aprendizajes, decisiones, errores) | `~/.hermes/profiles/ariadna/memory/` + `memory` tool en runtime | "sdf NO spare" (lesson), "local-sqx-* sagrados" (owner constraint). |
| **Inventory** (estado real) | `backup-inventory-template.json` + discovery outputs en `/home/hermes/aranea/topology/discovery/` | Nodos, VMs, servicios, datasets. |
| **Request Change** (evolución controlada) | `REQUEST-CHANGES.md` | RC-001: cambiar ventana de mantenimiento. |

**Reglas de autoridad** (invariantes):
```
La policy bloquea.
El runbook manda.
La skill ejecuta.
La memoria aconseja.
El inventario aterriza.
El owner aprueba cambios riesgosos.
```

---

## 12. Diseños descartados / histórico

### Diseño descartado: Iter 1 — capex ~$650 USD (2026-06-30)

- **Qué proponía**: comprar 2× SSD enterprise 1 TB + HBA adicional para hades, mirror pool2 + reemplazar SSDs consumer.
- **Por qué se descartó**: Owner restricción F-01 (cero capex).
- **Riesgo que evita**: gasto innecesario; recursos existentes alcanzan.
- **Fecha**: 2026-06-30.

### Diseño descartado: Iter 2 — `sdf` como spare (2026-06-30)

- **Qué proponía**: usar `sdf1` (SSD 931 GB en hades) como mirror de pool2. Convertir pool2 en mirror SSD.
- **Por qué se descartó**: `sdf` está en pool0 mirror-0 (validado `zpool status -v`). No hay disco libre en hades.
- **Riesgo que evita**: si se hubiera actuado, habría roto pool0.
- **Fecha**: 2026-06-30. Decisión F-05.

### Diseño descartado: Iter 3 — Plan B con zfs recv on-cluster (2026-06-30)

- **Qué proponía**: usar `local-sqx-hera` (931 GB libre, vm 123 stopped) como destino `zfs recv` desde truenas.
- **Por qué se descartó**: Owner restricción F-04 (Sagrados SQX). Las 3 VMs SQX son infraestructura Echo Forge.
- **Riesgo que evita**: pérdida de storage dedicado a SQX.
- **Fecha**: 2026-07-01. Decisión F-12.

### Diseño descartado: backup externo Ceph (RBD export a PBS) (2026-06-30)

- **Qué proponía**: `rbd export` weekly de imágenes Ceph → PBS datastore.
- **Por qué se descartó**: Owner restricción F-10 (sin backup externo Ceph). 3× replication + vzdump PBS cubren.
- **Riesgo que evita**: complejidad + storage innecesario; Ceph ya tiene 3× rep.
- **Fecha**: 2026-07-01.

### Diseño descartado: migración de `pool0_backup` (2026-06-30)

- **Qué proponía**: mover `pool2/pool0_backup/` (dataset) a kronos pool1.
- **Por qué se descartó**: Owner restricción F-09 (dejar como está).
- **Riesgo que evita**: churn innecesario; dataset cumple rol de snapshot semanal mismo-host.
- **Fecha**: 2026-07-01.

### Diseño descartado: Opción B optimización con BorgBackup/restic (2026-07-01)

- **Qué proponía**: BorgBackup o Restic content-defined dedup sobre rclone para ~60-80% reducción.
- **Por qué se descartó**: Owner decisión F-11 (Opción A conservadora). Borg suma complejidad operacional.
- **Riesgo que evita**: complejidad innecesaria. Restic (ya incluido en Opción A) sí se usa para tier crítico.
- **Fecha**: 2026-07-01.

---

## 13. Referencias

- `DIFF-CONCEPTUAL.md` (este refactor).
- `BACKUP-DR-OWNER-PROJECT.md` (proyecto owner).
- `agent-project-00` a `agent-project-08` (subproyectos agente).
- `BACKUP-DR-RUNBOOK.md` (verdad operacional).
- `BACKUP-DR-CHECKLIST.md` (checklists).
- `backup-policy.yaml` (policy ejecutable).
- `backup-inventory-template.json` (template inventario).
- `REQUEST-CHANGES.md` (cambios propuestos).
- `../DESIGN-PROPOSAL.md` (iter 1-4, ahora histórico).
- `../PROPUESTA-COMPLETA-ITER4.md` (consolidación previa, ahora histórico).
- `../BACKUP-SYSTEM.md` (Task 2 previa).
- `../AUDIT.md` (auditoría storage).
- `../TOPOLOGY-AUDIT.md` (auditoría topológica, 10 hallazgos).
- `../inventory.md` (landscape storage).
- `../../../05-tickets/2026-06-30-013-storage-redesign-backup-design.md` (ticket origen, ahora superseded).
- Skill: `aranea_agent_ro_inventory_refresh`.

---

**Status**: design-frozen. Cero cambios ejecutados en infraestructura.
**Capex**: $0. **Opex mensual cloud**: $0.
**Captured**: 2026-07-01 (cierre de sesión, owner pidió cerrar al terminar).
**Sesión cerrada por instrucción del owner**: 2026-07-01.
