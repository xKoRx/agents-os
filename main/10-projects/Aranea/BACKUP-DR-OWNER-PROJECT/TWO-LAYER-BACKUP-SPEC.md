---
title: "SPEC — Two-Layer Backup: VM/LXC completo + datos consistentes (2026-09-21)"
type: doc
schema_version: 1
status: active
icon: 🧱
slug: two-layer-backup-spec
area: "[[Aranea]]"
project: "[[BACKUP-DR-OWNER-PROJECT]]"
created: "2026-09-21"
updated: "2026-09-21"
aliases:
  - TWO-LAYER-BACKUP-SPEC
  - SPEC dos mecanismos backup
tags:
  - kind/doc
  - area/aranea
  - domain/backup-dr
  - project/backup-dr
related:
  - "[[MATRIZ-59-GUESTS-BACKUP]]"
  - "[[MASTER-PLAN-STORAGE-BACKUP-DR]]"
  - "[[POOL0-TO-POOL2-REPLICATION-SPEC]]"
  - "[[BACKUP-DR-KEY-RECOVERY]]"
---

# 🧱 SPEC — Two-Layer Backup (VM/LXC + datos consistentes)

> Autoridad: D-NEW-04 del mandato 21sep noche. Los dos mecanismos NO son intercambiables. **Regla binding: un backup de VM con un disco excluido NO declara recuperación integral del servicio sin procedimiento de restauración de ese disco o de sus datos.** Fuente canónica de los 59 guests: [[MATRIZ-59-GUESTS-BACKUP]] (esta SPEC NO la duplica; añade exclusiones ledger + RTO + mecanismo pool1→pool0). Ejecución GATED; mandatos en [[MANDATO-BACKUP-VMS-SPEC]] y [[MANDATO-BACKUP-DATOS-SPEC]].

## Propósito

Define los dos mecanismos de backup no intercambiables (D-NEW-04): imagen VM/LXC vía PBS y datos consistentes por servicio, con exclusiones ledger, capa pool1→pool0 y matriz de cobertura. Ejecución GATED.

## Contenido

## 1. Mecanismo A — Backup de VM/LXC completo (PBS, independiente)

**Qué cubre**: configuración + SO + discos incluidos → restaurar la máquina completa. Motor: vzdump→PBS VM 180 (datastore `main`, dedup, verify jobs) — mecanismo pilotado por R2 (6 CTs, verify TASK OK) y adoptado como producción por B1 tras decisión D.

**Rutas de restauración** (resumen; procedimiento ejecutable en [[BACKUP-DR-RUNBOOK]] + [[MANDATO-CERTIFICACION-SPEC]]):
1. Restore completo VM/LXC → mismo nodo o alternativo (`qmrestore`/`pct restore`; CT 990 demostrado).
2. Restore de disco individual → desde snapshot PBS (file-level `pxar` para configs; imagen para discos).
3. Restore hacia backend alternativo → `--storage` en restore (p.ej. pool1 caído → local-lvm del nodo destino).
4. Sin Ceph original → los T0 de pool1 (echo 140, PG/Mongo/MinIO SOs) se restauran a local-lvm/nfs; **ningún restore de datos requiere pool1 vivo** (post-A0: dumps y configs viven en PBS).
5. Configs PVE y referencias a storage → `pve-config` semanal (R1.5, node-local 5/5) + pmxcfs bundle gated; storage.cfg + vmid conf + red son prerrequisitos documentados de DR-T3/T5.
6. Orden de arranque de dependencias: red/edge (opnsense, traefik) → quorum (etcd) → storage (truenas) → datos (PG/Mongo/MinIO) → apps (echo, flink, hasura) → validación de red y aplicaciones por servicio (checklist por guest en MANDATO-CERTIFICACION-SPEC).

**Exclusiones ledger** (toda exclusión = justificación + mecanismo alternativo + evidencia + procedimiento; `backup=0` NO significa protegido):

| Exclusión | Guest/disco | Justificación | Mecanismo alternativo | Estado |
|---|---|---|---|---|
| `local-sqx-*` | 108/111/123 + worker 135 | F-04 sagrado | artefactos SQX vía MinIO G1B | vigente, intocable |
| Media frigate | dataset pool0/apps | reconstruible | no aplica | vigente (exclusión OPCIONAL ampliable a la réplica sólo por RC owner) |
| Labs T3 stopped (12) | 102/104/107/109/110/112/114/117/120/159/162/170 | sin valor de recuperación | reconstrucción desde template; 112/162/170 liberación gated dueño | vigente (018 puede cambiar) |
| Datos kafka scsi1 | 136/138/139 | valor UNKNOWN | sin alternativa hoy → UNKNOWN explícito | 018 (contrato regla 4) |
| Datos argus scsi1-4 | 160 | retención vs reconstruible UNKNOWN | ARGUS = observabilidad; re-puebla con exporters | 018 |
| R2 exclusión 148 | etcd-keeper rootfs | mandato R2 permanente | etcd snapshot lógico cubre sus DATOS | vigente |
| pool1 como destino | — | NO_GO nearfull | vzdump LEE pool1, escribe PBS/local-lvm | vigente |

**pool1→pool0 (D-NEW-02, espacio separado en pool0 para respaldos recuperables de workloads de pool1)**: la copia PRIMARIA de VMs sigue siendo PBS (kronos). La capa pool0 es la **2ª copia local en dominio de falla distinto** (chasis hades): dataset NUEVO `pool0/vm-backup` + storage PVE `nfs-vmbackup` (patrón nfs-pool2: alta de storage nueva, `nfs-storage` INTOCADO) y **vzdump semanal snapshot-mode de las unidades T0 con discos en pool1** (140, 152, 153, 157, 133/134/144, 124-ide0+scsi0, CTs 126/129/141/128/127, etcd×5, 116/113/103/137) hacia ese storage, retención `keep-weekly=4`. PBS queda recuperable aunque caiga kronos porque esta copia vive en pool0; pool0 queda recuperable aunque caiga hades vía su réplica a pool2 — **sin cadena circular** (A no depende de la réplica; la réplica copia lo que A escribe). Evita el hueco DR-T3 (kronos caído = copias vigentes perdidas) para el dominio local. Dedup no crítica en esta capa (PBS ya deduplica); verificación = restore de prueba mensual rotativo (WP-R7).

## 2. Mecanismo B — Backup de datos consistentes

Matriz por servicio (columnas del mandato; claves por [[BACKUP-DR-KEY-RECOVERY]]):

| servicio | origen | mecanismo | consistencia | frecuencia | retención | destino local | destino cloud | cifrado | clave | RPO real | restore demostrado | estado |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| PostgreSQL 152 | dumps in-guest 13 bases+globals | G1A patrón + timers A1 03:00 | app-consistent | diaria | 30d sin prune | PBS `host/r0d-postgresql` | A7 (prioridad 1) | AES-256-CBC/PBKDF2 | `r0d-g1a.key` custodia doble | ~24h (PITR = deuda A2) | SÍ — G1A + drill MP-01 | VERIFIED+AUTOMATED |
| MongoDB 153 | dump archive in-guest | ídem A1 03:20 | app-consistent | diaria | 30d | PBS `host/r0d-mongodb` | A7 (prioridad 1) | ídem | ídem | 24h (RPO 1h NO demostrable standalone) | SÍ — G1A | VERIFIED+AUTOMATED |
| CouchDB 116 | dump `_all_dbs` replicator | WP-A3 | app-consistent | diaria (tras credencial) | 30d | PBS | A7 (prioridad 2) | ídem | `r0d-g1a.key` | ∞ hoy (sin credencial) | NO | BLOCKED — bundle A3 |
| MinIO 157 | stream tar\|zstd 12 buckets+IAM+config+`.minio.sys` | G1B | app-consistent point-in-time | semanal gated | ≥30d sin prune | PBS `host/minio-*` | A7 (prioridad 3) | AES-256 | `r0d-g1b.key` | ≤7d (one-shot hoy) | SÍ — OBJECT_COPY_PASS+FULL_DR_PASS | VERIFIED one-shot; recurrencia GATED owner |
| Echo 140 | deploy Forge en repo + config | CFG (A5) + vzdump B1 | n/a (estado en PG) | diaria | según retención | PBS + `nfs-vmbackup` | A7 (prioridad 4: inventario/configs) | AES | `r0d-g1a.key` | 1d | CFG R1 sí; vzdump post-D | PARTIAL |
| Echo Forge | repo (fuera de guests) | git | n/a | push | — | repo | repo remoto | — | — | 0 | n/a | vigente, sin cambio |
| Agents-OS/Second Brain | vault hermes | R1 second-brain 04:00 | file-consistent (tar race = deuda T-21b) | diaria | rotación staging | staging→PBS | A7 (prioridad 4) | AES | `r0d-g1a.key` | 1d (FAIL 2 días: fix gated) | R1 drill PASS 17-18sep | PARTIAL — T-21b |
| Configs Proxmox 5 nodos | `/etc/pve` node-local | R1.5 sáb 08:30 + pmxcfs bundle | file | semanal | staging | staging→PBS | A7 (prioridad 4) | AES | `r0d-g1a.key` | 7d | SÍ (drill R1.5) | VERIFIED (pmxcfs gated) |
| Config PBS 180 | `/etc/proxmox-backup*` | WP-B2/A5 | file | semanal | 30d | staging→PBS | A7 (prioridad 4) | AES | `r0d-g1a.key` | 7d | round-trip A5 | PARTIAL (datastore meta pendiente) |
| TrueNAS config | API export | WP-B2 | file | semanal | 30d | staging→PBS | A7 (prioridad 4) | AES | `r0d-g1a.key` | 7d | NO (canal por probar) | BLOCKED_TECH (método sin demostrar) |
| Red y certificados | traefik R1 + OPNsense export + CA claves | R1 + WP-B2 | file | diaria/semanal | 30d | staging→PBS | A7 | AES | `r0d-g1a.key` | traefik 1d; OPNsense/CA ∞ | traefik SÍ; resto NO | PARTIAL (acme-stepca recovery-critical) |
| etcd | snapshot cluster | R1.5 05:00 | app-consistent | diaria | staging rotación | staging→PBS | A7 | AES | `r0d-g1a.key` | 1d | SÍ (restore scratch) | VERIFIED+AUTOMATED |

**Deudas reales registradas (no re-labrar)**: PG PITR pendiente (WP-A2 gated) · Mongo RPO 1h no demostrado (A2b decisión topológica owner) · CouchDB sin credencial (bundle A3) · MinIO recurrente gated (regla 4.1/018) · R1 second-brain tar-race (T-21b staged) · A7/off-site bloqueado (gates 020/021; **3-2-1 NO declarado**).

**MinIO — definición de «última copia»**: la última copia **completa, verificable y recuperable** (sha por stream 12/12 + verify PBS + drill de arranque; no "el último archivo subido"). Regla de rotación: **la copia anterior NO se sobrescribe ni elimina hasta que la nueva esté certificada** (verify TASK OK + sha manifiesto); retención ≥2 copias certificadas en todo momento. Restore completo requiere: datos de buckets + IAM/usuarios + policies + config server + metadata `.minio.sys` — todo incluido en el stream G1B (diferenciar «datos» de «configuración del servicio» en cada restore drill).

## 3. Cobertura 59/59 (resumen por clase; detalle por guest = MATRIZ)

| Clase | Guests | Mecanismo A (vzdump) | Mecanismo B (datos) | RTO objetivo |
|---|---|---|---|---|
| T0a edge | 130,145,149,115 | post-D → PBS+nfs-vmbackup | config exports (B2) | ≤4h VM; cfg ≤1h |
| T0c quorum | 101,147,154,155,156,148,136,138,139 | post-D | etcd snapshot diario; kafka data UNKNOWN | ≤4h |
| T0d trading | 124,133,134,144,140,152,153,160,126,129 | post-D | dumps G1A diarios + SNAP/REPL zvol | DB ≤4h (PITR ≤2h post-A2); resto ≤4h |
| ADD-CRIT | 116,118 | post-D | CouchDB (blocked), hermes-state R1 | ≤4h |
| ADD-IMP/T2 | 113,103,105,106,157,158,142,141,127,128,132,119,137,180 | post-D | MinIO G1B semanal; configs A5 | 7d-30d |
| T3/SQX | 108,111,123,135 + 12 stopped | NO por diseño | artefactos vía G1B | n/a |

Restore probado por clase: CT genérico (990) SÍ · PG/Mongo dumps SÍ (G1A) · MinIO SÍ (G1B) · configs SÍ (R1/R1.5) · VM completa T0 NO (post-B1, primer drill en MANDATO-CERTIFICACION-SPEC) · etcd SÍ.

## 4. Gates

- **G-B1**: decisión D-piloto + 018 (lista final) + 019 (ventana inicial) → activación vzdump producción (B1) con exclusión ledger de esta SPEC.
- **G-NFSVM**: alta storage `nfs-vmbackup` + dataset `pool0/vm-backup` + schedule semanal (capa pool1→pool0).
- **G-A7**: tickets 020+021 → cloud por prioridad D-NEW-05 (PG/Mongo → CouchDB → MinIO → configs/inventario → Secret Zero escrow externo).
- **G-A3**: credencial CouchDB `_reader`. **G-A4**: recurrencia MinIO + versioning. **G-T21B**: aplicar diff tar-race.
