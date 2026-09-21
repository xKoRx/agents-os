---
type: raw_session
schema_version: 1
scope: session
created: "2026-09-21"
updated: "2026-09-21"
area: "[[Aranea]]"
project: "[[BACKUP-DR-OWNER-PROJECT]]"
application:
entities:
  - "[[BACKUP-DR-OWNER-PROJECT]]"
related:
  - "[[ARANEA-CONTINUIDAD-Y-VENTANA-25-26-SEP]]"
aliases: []
confidence: verified
source_session:
load_policy: never
indexable: false
index_priority: never
tags:
  - kind/raw-session
  - scope/session
  - area/aranea
---

# 2026-09-21-congelacion-martes-raw

> [!warning]+ Raw session L0
> Archivo de auditoría y retrofit. Excluido del retrieval normal y de Graphify.

## Contexto

- Agente: Ariadna (Hermes desktop, perfil ariadna, glm-5.3-flash/zai).
- Proyecto o entidad: [[BACKUP-DR-OWNER-PROJECT]] — carril Backup/DR.
- Objetivo de la sesión: ejecutar íntegramente `~/aranea/work/continuity-20260921/MANDATO-MARTES-22.md` (congelar placement/destinos/capacidad; bundle owner; preparar miércoles; SIN migraciones ni cambios productivos; registrar evidencia, feedback y cerrar sesión).

## Transcript

Registro reconstruido de evidencia (comandos y salidas clave, con timestamps; logs crudos en `~/aranea/work/continuity-20260922/raw/`):

```
14:02:39 -03  hermes: uptime 6:26; timers aranea 6/6 activos (pg 03:00, mongo 03:20, r1 04:00, etcd 05:00, r2 06:05, pve-config sáb 08:30)
              journal R2 21sep: timer stopped 01:09:35 (apagado), started 07:36:43 (boot) → run 06:05 no ocurrió
              journal 07:36:45 etcd rev 58563 5/5 healthy snap 5107744B; 07:37:21 A1-mongo-PASS; 07:38:10 A1-pg-PASS
              last -x: shutdown 01:09→07:36 (6h27m) — reboot previo sáb 19 11:54
              staging: 11G/49G (23%); runs: 20260921-073644 (R1 hoy)
17:02:40Z PBS .123 (ariadna_pbs): up 2d15h; df /mnt/pbs-data 48G/295G (18%) ext4; chunks 14796 (sudo find)
              tasks verify: A1-mongo 07:37:23 -03 TASK OK (73.70MiB, 0 errors); A1-pg 07:38:04 -03 TASK OK (UPID ...00000055)
              verify full datastore previo: 20sep 14:01:45 -03 TASK OK (14 groups)
              ct/ = {101,115,147,154,155,156}; host/ = 12 grupos (r0d-* + minio-*)
17:02:41Z hades (ariadna_pve): up 42d; sudo ceph falla sin conf (RADOS ObjectNotFound; ídem dentro de agent-read)
17:03:24Z pvesh /cluster/resources OK: quórum 5/5 online; 149 RUNNING en ATHENA (uptime 35,1d); 125 RUNNING hades (uptime 68873s); 128 running hera; 140 running hades; local-lvm hades 33,4G/53,9G libres; zeus 77,5G; hera 91,7G; nfs-storage 430,9G/1345G (30%)
17:04Z    truenas .91 (agent_ro DDP 'storage'): pool2 ONLINE single-disk 7,44TiB alloc 3,26T free 4,18TiB frag 0% scrub jul-2025 0 errores; pool0 ONLINE 4×mirror+special, free 1,67TiB, scrub ~6sep-2026
17:05:26Z kronos (ariadna_pve): vgs → local-kronos VFree 267,51g; pool-kronos VFree <733,87g; qm config 180: scsi1 local-kronos:vm-180-disk-1, serial=pbs-data, size=300G
17:06Z    mcps-ops: / 17G/20G 88% (2,4G libres); CONTAINERS=26
17:07:33Z ping 149: 100% packet loss (3/3)
17:10:51Z K2 L1 (pvesh /nodes/hades/ceph/osd): osd.0 85,55% / osd.2 85,57% (797/932 GiB; avail 135/134G); health HEALTH_WARN: OSD_NEARFULL(2) POOL_NEARFULL(2) BLUESTORE_SLOW_OP_ALERT(2) BLUESTORE_FREE_FRAGMENTATION(2); VAR 0,62-1,33; TOTAL 64,19%
17:31:17Z K2 L2 (ceph --conf /etc/pve/ceph.conf osd df): osd.0 85,59% / osd.2 85,59% (avail 134G); HEALTH_WARN idem → condición de alerta (≥89%×2≥1h) NO disparada
```

Escrituras de la sesión: `~/aranea/work/continuity-20260922/{CAPACITY-FREEZE,PLACEMENT-FREEZE,BUNDLE-DECISIONES-MARTES,WEDNESDAY-MANDATES-INDEX}.md` + `raw/*`; vault: BACKUP-DR-OWNER-PROJECT.md (bitácora + T-22 DONE + T-23 anotada + status_detail), ARANEA-CONTINUIDAD-Y-VENTANA-25-26-SEP.md (delta tarde-2), change-logs/2026-09-21-congelacion-martes-delta.md, feedback/session/2026-09-21-congelacion-martes-feedback.md, este L0 y su L1. Cero mutaciones de infraestructura (todas las sondas read-only: agent-read/pvesh/df/vgs/qm config/ping/ls/cat).

## Evidencia externa

- `~/aranea/work/continuity-20260922/raw/`: timers-hermes, r2-journal, a1-journal, pbs-180 (df/tasks), pbs-snapshots, pve-hades-resources (JSON completo), kronos-vg, truenas-storage, ceph-k2-l1-pvesh, ceph-k2-l1/l2-21sep, hermes-last-x.
