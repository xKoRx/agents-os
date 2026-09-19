---
type: change_log
schema_version: 1
scope: session
created: "2026-09-19"
updated: "2026-09-19"
area: "[[Aranea]]"
project: "[[BACKUP-DR-OWNER-PROJECT]]"
application:
entities:
  - "[[BACKUP-DR-OWNER-PROJECT]]"
  - "[[BACKUP-DR-DESIGN]]"
related:
  - "[[BACKUP-DR-CONTRACT]]"
  - "[[REQUEST-CHANGES]]"
aliases:
  - "Assessment storage/Ceph/Backup-DR 2026-09-19"
confidence: high
source_session:
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
  - area/aranea
---

# 2026-09-19-storage-ceph-assessment

%% Gate documental + assessment read-only ONE-SHOT del mandato owner "ARANEA DATA & STORAGE ARCHITECTURE / CEPH RCA / BACKUP-DR ALIGNMENT" (2026-09-19). Cero mutaciones de infraestructura. %%

## Cambio

- **Tipo:** documentation + assessment (read-only)
- **Archivo(s):**
  - `10-projects/Aranea/BACKUP-DR-OWNER-PROJECT/BACKUP-DR-OWNER-PROJECT.md` — sección nueva «Dirección owner — arquitectura storage y protección de datos — 2026-09-19» (antes de Bitácora) + 1 entrada de bitácora. SHA256 baseline: `7eb604286c4a79f89941a6ce21a32350c8a34cb9043b62fd296f16a1f9461124`.
  - `80-agents/journal/logs/2026-09-19-storage-ceph-assessment.md` — este log.
  - `~/aranea/work/storage-ceph-assessment-20260919/` (FUERA del vault) — evidencia cruda read-only.
- **Sin mutaciones:** infraestructura (PVE/Ceph/TrueNAS/PBS/CTs/VMs), `BACKUP-DR-DESIGN.md`, `BACKUP-DR-CONTRACT.md`, tickets 018–021, R1/R1.5/R1.6, piloto R2 (intacto; primer disparo dom 2026-09-20 06:05), estados de otros proyectos, frontmatter status/progress del proyecto.

## Motivo

- Mandato owner one-shot: decidir con hechos qué datos/discos viven en cada backend, cómo se protegen y recuperan, y por qué Ceph presenta nearfull y episodios de lag. Primer gate OBLIGATORIO: actualizar el proyecto en el vault ANTES de investigar.

## Fuentes usadas

- `BACKUP-DR-OWNER-PROJECT.md` (vivo), `BACKUP-DR-CONTRACT.md`, `BACKUP-DR-DESIGN.md` (F-01..F-14), `REQUEST-CHANGES.md`, bootstrap Agents-OS + router `aranea-agent-dev`, enablements H4/H5/H6 y contracts citados por el mandato.
- Adjunto expandido `backup_dr_actualizacion_owner_2026-09-19.md`: NO disponible → mandato autosuficiente; delta documentado en la sección owner.

## Resolución aplicada

- Gate documental aplicado con patch incremental (no reescritura), preservando cambios concurrentes.
- Verificación mirror GitHub: el vault local NO es repo git (`/home/hermes/obsidian/SecondBrain/main/.git` ausente) → publicación por productor externo NO verificable desde esta sesión; delta registrado aquí. Vault = autoridad; sin push directo.

## Verificación

- SHA256 del proyecto tras gate: `7dd359853e4c1ff36537a96e2dff0dfdf15286f8ef041056a881ddf1d8531b71` (baseline pre: `7eb60428…`). Sección ×1, bitácora ×1, frontmatter intacto.
- R2 intacto verificado live: datastore main 733M/295G (sin drift vs baseline 18sep), timer `aranea-r2-measure.timer` pending first_run 2026-09-20 06:05, deadline 2026-09-26 (state files leídos, no tocados). Timers R1 04:00/05:00/SÁB activos, último run 20260919-115452.
- Cero mutaciones de infraestructura: todas las lecturas SSH read-only; sin scrubs, snapshots, configs, journals>200 líneas, benchmarks, SMART self-tests, rbd du ni guest exec.

## Hallazgos / Resultado

Veredicto: **ASSESSMENT PARTIAL — EVIDENCE STRONG** (handoff completo: `~/aranea/work/storage-ceph-assessment-20260919/HANDOFF-2026-09-19.md`).

1. **Nearfull Ceph = causa estructural PROBADA** (no desbalance): CRUSH chooseleaf host + 1 solo OSD en hera y zeus + 2 en kronos + réplica 3 ⇒ todo PG coloca réplica en osd.0(hera) y osd.2(zeus): data 797=797=373+424 GiB demostrado; balancer upmap declara distribución perfecta. Márgenes: -7 GiB hasta nearfull, 40 hasta backfillfull. **Caída del host kronos = re-replicate imposible** (800 GiB vs 80 GiB disponibles). NOT_GO nuevos discos pool1 reconfirmado.
2. **MinIO 157 (creencia owner INVERTIDA, verificado)**: SO = pool1 RBD (`vm-157-disk-0`), datos = zvol pool0/iscsi/minio_data via iSCSI LUN6 (49,8G usados de 100G zvol; metadata PVE size=16G es vieja). PG 152 / Mongo 153 mismo patrón: SO pool1 + datos iSCSI zvol pool0, todos `backup=0` → **hoy sin ninguna protección de backup** (ni vzdump ni dumps).
3. **Hardware Ceph**: 4 NVMe QLC consumer (Crucial P3 ×2, Kingston NV3 ×2) con endurance usada 64% / 100% / 100% / **201%**; latencia 7-8ms en las Crucial vs 1-2ms Kingston. BlueStore fragmentación 0,90 en osd.0/2.
4. **Red**: red dedicada 10.10.10/24 MTU9000 existe y la RÉPLICA SÍ fluye por ella (corrección E2 adversarial: cluster_addr=10.10.10.x en 4/4 OSDs, ~18TB por la 10G vs ~0,9TB por LAN). mClock global = `high_recovery_ops` + recovery_sleep 0 (perfil temporal dejado permanente). Episodios históricos de lag: **NOT_PROVEN** (sin instrumentación; 0 slow-ops últimos 7d). Hipótesis restantes de lag: hardware QLC desgastado (latencia base 7-8ms en osd.0/2) + perfil mClock recovery-prioritario durante recoveries.
5. **TrueNAS**: pool0 OK (scrub 06-sep-2026, 0 errores) pero **sin snapshots recientes** (solo reconstrucción jul-2025) y `pool2/pool0_backup` **STALE desde jul-2025** (no es copia viva; F-09 intacta). pool2 = ~4,2T en 3 árboles legacy congelados + 2,15T libres; **pool2 sin scrub desde 12-jul-2025** (riesgo F-14 vigente). NFS exports sin restricción de red en pool0/proxmox_storage y pool0/trading_documents (toda la LAN). Used de zvols = refreservation (E1): pg_data/mongo_data/minio_data sin snapshots.
6. **LUN2 doble-attach latente**: zvol vm-zeus-win-disk apuntado por VMs 151 y 100 (ambas stopped). VMIDs 112/162/170: NO huérfanos como VMs (112 = sqx-deprecado stopped con disco activo LVM `pool-kronos`; 162/170 sqx-ulab stopped); matiz E3: la imagen RBD `vm-112-disk-0` 120G de pool1 SÍ es huérfana de config (lock stale) — candidata a liberación gated a dueño. Trash RBD vacío.
7. **RPO 1h**: PG viable con alta confianza (WAL archiving/PITR, archive_timeout corto; NOT_CERTIFIED hasta drill); Mongo condicionado a topología (standalone → dumps no alcanzan; requiere replica set/PBM) — UNKNOWN sin acceso guest. 3-2-1 hoy **NO CUMPLE** (0 off-site real activo; Secret Zero 020 pendiente).
8. Próximo paso mínimo propuesto (requiere aprobación): **R3 mínimo = dumps lógicos diarios PG+Mongo → staging+PBS + restore drill scratch**, gated por tickets 018/020. No ejecutado.

Revisión adversarial independiente: `~/aranea/work/storage-ceph-assessment-20260919/adversarial-review.md` (resultado consolidado al cierre).

## Lecciones

- El "size=" que PVE muestra en discos iSCSI puede ser metadata vieja (LUN6 decía 16G, zvol real 100G): el tamaño canónico vive en TrueNAS (extent/zvol), no en el config del guest.
- `ceph config dump` con `osd_op_queue=mclock_scheduler` ignora sleep options: para diagnosticar latencia revisar SIEMPRE el perfil mClock efectivo (global vs por-OSD) antes de culpar hardware o red.
- La distribución PG "asimétrica" (129/61/129/68) con FD=host y hosts de 1-2 OSDs es matemática, no patología: cruzar `osd df` con la regla CRUSH antes de proponer rebalanceos.

