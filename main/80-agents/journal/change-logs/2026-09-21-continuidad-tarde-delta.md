---
type: change_log
schema_version: 1
scope: session
created: "2026-09-21"
updated: "2026-09-21"
area: "[[Aranea]]"
project: "[[BACKUP-DR-OWNER-PROJECT]]"
application:
entities:
  - "[[BACKUP-DR-OWNER-PROJECT]]"
  - "[[ARANEA-CONTINUIDAD-Y-VENTANA-25-26-SEP]]"
related:
  - "[[FIRST-MAINTENANCE-WINDOW-20260920]]"
  - "[[PLACEMENT-DECISIONS-20260920]]"
aliases:
  - "Continuidad tarde 2026-09-21 delta R2 y desacoplamiento"
confidence: verified
source_session:
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - area/aranea
  - domain/backup-dr
---

# Change log — 2026-09-21 · Continuidad tarde: R2, desacoplamiento Hermes, T-21b, paquete martes

Sesión ONE-SHOT (mandato owner «lunes 21» §2-§6, tarde). Cero mutaciones de infraestructura:
todo el trabajo es verificación RO + staging documental gated en `~/aranea/work/continuity-20260921/`.

## Cambios

1. **Serie R2 certificada con evidencia dura** (proyecto + continuidad actualizados): first_run=20sep
   (run-20260920.jsonl: 6/6 CTs rc=0 + verify TASK OK 09:08:05Z + snapshots ct/* 09:05-09:08Z PBS),
   19sep NO ejecutó (2 intentos manuales fuera de ventana; run-20260919.jsonl), 21sep perdido por
   apagado de hermes (timer non-Persistent POR DISEÑO; journal). Serie máxima 6/7 → D-A tolerancia
   CERO. **Errata en `~/aranea/work/first-window-20260926/MANDATO-P0.md`** (§6/§7 "7º run"→"6/7").
2. **E2 WP-HD desacoplamiento Hermes** staged gated: ejecutor standby = PBS 180 (up 2d11h, ya
   ejecuta ingesta A1/A0, datastore 232G), timers espejo `ConditionPathExists` + `Persistent=false`,
   flag manual `ACTIVE` (rutina de apagado owner), sin auto-activación ni catch-up retroactivo
   (no reponer >09:00 en día de mercado). 3 gates owner (diseño/credencial/ejecución).
3. **T-21b empaquetado y probado**: `T21B-R1-TAR-RACE-FIX.diff` (copia atómica cp -a + tar;
   dry-run de patch limpio) + `T21B-FIX-TEST.sh` (fixture: staging 4/4 rc=0 tar íntegro vs tar
   directo 3/4 rc=1 por race; prueba negativa sin falso PASS). OWNER_GATE sin cambio.
4. **Matriz de decisiones del martes + mandato E6**: `E4-E5-R2-SERIE-Y-DECISIONES-MARTES.md`
   (W1-W5/PBS/Ceph con evidencia del día) + `MANDATO-MARTES-22.md` (READY).
5. **Deltas operacionales medidos hoy** (RO): pi-hole 149 PVE=RUNNING pero L2-dead persistente
   (ICMP 100% loss); mcps 113 rootfs 88% (2,4G libres, subió desde 85% → prune a P1); Ceph
   osd.0/2 85,20/85,23% (banda estable, alerta K2 no disparada, slow ops vigentes); Echo con 1
   posición abierta 09:44 (protección G1A intacta); A7 payload ≈264M cabe en daedalus 16G (push
   viable); Prometheus sin exposición HTTP consultable desde hermes → precheck Echo de la ventana
   usa canal dump de posiciones (query G1A ya demostrada), no métricas.
6. **E1 estado del lunes**: A1 PASS (histórico); R1 PARTIAL (diff listo gated); A3/CouchDB BLOCKED
   (única llave: credencial `_reader` owner); R2 PARTIAL; WP-HD DEFER a gates; Ceph STABLE-WARN;
   Echo SANO en operación.

## Archivos

- Vault: `BACKUP-DR-OWNER-PROJECT.md` (status_detail + [ver sección Bitácora del proyecto para
  tareas T-21b/T-22 actualizadas]), `ARANEA-CONTINUIDAD-Y-VENTANA-25-26-SEP.md` (sección delta
  tarde), `MANDATO-P0.md` workspace (errata 6/7).
- Workspace: `~/aranea/work/continuity-20260921/` → `T21B-R1-TAR-RACE-FIX.diff`,
  `T21B-FIX-TEST.sh`, `E2-WP-HERMES-DECOUPLING.md`, `E4-E5-R2-SERIE-Y-DECISIONES-MARTES.md`,
  `MANDATO-MARTES-22.md`.

## Sin cambios

F-01..F-14, tickets 018-021, timers/horarios, R2 driver, driver R1 (diff staged NO aplicado),
Ceph/TrueNAS/PBS/guests, secretos (ninguno expuesto en esta sesión).
