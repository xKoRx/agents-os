---
type: change_log
schema_version: 1
scope: session
created: "2026-09-20"
updated: "2026-09-20"
area: "[[Aranea]]"
project: "[[BACKUP-DR-OWNER-PROJECT]]"
application:
entities:
  - "[[BACKUP-DR-OWNER-PROJECT]]"
related:
  - "[[K2-CEPH-RISK-20260920]]"
  - "[[FIRST-MAINTENANCE-WINDOW-20260920]]"
aliases:
  - "K2 Ceph risk assessment 2026-09-20"
confidence: verified
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

# 2026-09-20-k2-ceph-risk-assessment

%% Assessment read-only ONE-SHOT del mandato owner "K2 · Riesgo inmediato de Ceph" (dom 2026-09-20 21:10-22:00 -03). Cero mutaciones de infraestructura. Echo y R2 intactos. %%

## Cambio

- **Tipo:** documentation + assessment (read-only)
- **Archivo(s):**
  - `10-projects/Aranea/BACKUP-DR-OWNER-PROJECT/K2-CEPH-RISK-20260920.md` — nueva decisión K2 (veredicto SAFE_TO_DEFER, evidencia, condición de alerta, acción única preparada).
  - `80-agents/journal/logs/2026-09-20-k2-ceph-risk-assessment.md` — este log.
  - `80-agents/journal/feedback/system-1/2026-09-20-aranea-k2-ceph-session-feedback.md` — feedback de sesión.
  - `~/aranea/work/k2-ceph-risk-20260920/K2-EVIDENCE.md` (FUERA del vault) — evidencia cruda de la medición.
- **Sin mutaciones de infraestructura:** PVE/Ceph/TrueNAS/PBS/guests. Sin escrituras, limpieza, borrado de RBD, cambios CRUSH, migraciones, backups, reinicios ni pruebas de carga. Echo sin contacto; timers R1/R1.5/A1/R2 verificados por listado (`list-timers` hermes 21:10), no tocados. Otros documentos del proyecto (Operating State, PLACEMENT, WINDOW) sin edición — sus imprecisiones quedan corregidas por referencia desde la nota K2.

## Motivo

- Mandato owner one-shot: decidir con métricas si Ceph puede mantenerse sin intervención hasta la ventana del 26-09, identificar el workload que explica el crecimiento reciente, distinguir crecimiento real de efectos de replicación/medición, y emitir SAFE_TO_DEFER / OWNER_ACTION_REQUIRED / INCONCLUSIVE con una única acción propuesta si corresponde.

## Fuentes usadas

- Bootstrap Agents-OS + router `aranea-agent-dev`; contrato `30-resources/runbooks/ceph-storage-operations-contract.md` (baseline H4 18sep 87,17%, clasificación de operaciones); handoff 19-09 (topología CRUSH, 0 slow-ops 7d, escenario kronos); Operating State 20sep y su evidencia (`ceph-live.txt`, `rbd-du2.txt`, `pve-live.txt`); CAPACITY-METRICS; sondas H5 del 19-09 (`ceph_probe_20260919_110.txt`).
- Mediciones vivas propias (RO, desde MON hera; athena sin confianza Ceph): 21:16:37, 21:29:31, 21:54:49 y 21:57:24 del 20-09 — `ceph osd df`, `ceph -s`, `ceph osd dump` (ratios), `ceph health detail`, `ceph osd perf`, `dump_ops_in_flight` (osd.0), `rbd ls/du/status pool1`, configs qemu/pmxcfs, índice de tareas de hades.

## Resolución aplicada

- Delta de crecimiento descompuesto con serie de 4 puntos y diferenciador T2→T3 (25 min): objetos 223,66k→223,43k y stored 817→815 GiB ⇒ la banda 85,6-87,9% es **oscilación con recesión**, no pendiente sostenida; el "+20G/día" de las citas previas era el flanco ascendente de una ráfaga.
- Escritor de la ráfaga atribuido por evidencia directa: op en vuelo en osd.0 → object `rbd_data.0134b09c5de1e2` → imagen `vm-125-disk-1` (mt4-test, lock exclusivo, watcher 192.168.31.90; +1,4 GiB/h en fase activa; congelada al llegar a 48,3/50 GiB). Contexto: 125 encendido hoy 18:54:44 (qmstart OK); la entrada "up 42d" de la matriz era imprecisa.
- Ratios efectivos verificados en osd dump: 0,85/0,90/0,95 (corrige el supuesto 0,90/0,95 de los documentos del 20sep; los márgenes correctos son ≈22G a backfillfull y ≈68G a full por OSD lleno).
- Slow ops re-atribuidos a osd.1/osd.3 (kronos) — no a los OSD llenos — y clasificados como transitorios: 564 ms a las 21:16 → 5 ms a las 21:57 sin intervención.
- Veredicto emitido en la nota K2: **SAFE_TO_DEFER** con condición de alerta (`osd df` ≥89% en dos lecturas ≥1h) y una única acción preparada no ejecutada (`qm shutdown 125`, gated por OK owner).

## Validación

- Contrastes cruzados: baseline H4 (18sep) y sondas H5 (19sep) contra mediciones propias del 20sep — la serie es consistente en los 3 MONs (health detail idéntico desde hera) y el retroceso nocturno se observó en 2 métricas independientes (object count del mon y stored de pool, más raw por OSD en T4).
- Identidad del escritor verificada por 3 vías independientes: object id en la op en vuelo ≡ imagen en `rbd ls` (id 0134b09c5de1e2) ≡ watcher en `rbd status` (IP de hades, donde corre 125).
- Cero mutaciones: ninguna operación de escritura Ceph/PVE ejecutada; las únicas conexiones SSH fueron lecturas (ariadna@hera/kronos/hades).

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- No aplica (assessment read-only). La nota K2 creada puede retirarse con borrado del archivo si el owner no la valida; ningún estado de infraestructura fue alterado.
