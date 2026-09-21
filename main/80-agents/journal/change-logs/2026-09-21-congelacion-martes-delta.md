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
  - "[[PLACEMENT-DECISIONS-20260920]]"
  - "[[FIRST-MAINTENANCE-WINDOW-20260920]]"
aliases:
  - "Congelación martes 22: capacidad + placement + bundle owner"
confidence: verified
source_session:
source_feedbacks:
  - "[[2026-09-21-congelacion-martes-feedback]]"
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - area/aranea
  - domain/backup-dr
---

# Change log — 2026-09-21 · Congelación martes: capacidad, placement y bundle owner

Sesión ONE-SHOT (mandato owner `~/aranea/work/continuity-20260921/MANDATO-MARTES-22.md`, tarde del 21). Cero mutaciones de infraestructura: medición RO (hermes local, PBS 180, hades/kronos vía ariadna@pve, TrueNAS vía DDP, mcps 113 vía mcps-ops) + escritura documental.

## Cambios

1. **Creado `~/aranea/work/continuity-20260922/`** con el congelamiento del día: `CAPACITY-FREEZE.md` (números fechados: PBS 48G/295G/14.796 chunks; Ceph osd.0/2 85,55/85,57% 17:10Z con slow ops, K2 no disparada; serie R2 1 OK/3 disparos, quedan 5; staging 11G/49G), `PLACEMENT-FREEZE.md` (matriz W1-W5/PBS/Ceph toda PENDIENTE_DECISIÓN, ninguna DECIDIDA), `BUNDLE-DECISIONES-MARTES.md` (D1-D8 con opciones/evidencia/impacto/rollback), `WEDNESDAY-MANDATES-INDEX.md` (M-W1..M-W5 borrador), `raw/` (sondas RO).
2. **4 erratas materiales contra fichas/mandatos vigentes** (todas ancladas a medición del día): (a) VG `local-kronos` VFree real = **267,5G** (baseline 567,5G era pre-creación del disco pbs-data de 300G) → el `+300G` de MANDATO-P0 §P0-1 no es ejecutable tal cual; opciones (a) grow ≤250G, (b) 2º disco en VG `pool-kronos` (VFree 733,9G), (c) diferir — pedida junto a D1; (b) hades local-lvm = **33,4G libres** (< los ~64G de W5) → reparto por VM o alcance reducido en T-23; (c) pi-hole 149 corre en **athena** (no hades) → el argumento de W3 "sobrevivir a hades" cae; decisión pasa a reactivar+proteger vs retiro; (d) pool2 = **4,18T libres** (vs 2,15T de la ficha) → holgura, decisión W1 no cambia.
3. **Proyecto actualizado** ([[BACKUP-DR-OWNER-PROJECT]]): T-22 → estado DONE; T-23/T-24 anotadas con insumos congelados y erratas; status_detail con delta del día.
4. **[[ARANEA-CONTINUIDAD-Y-VENTANA-25-26-SEP]] actualizada**: sección delta congelación del 21 (por encima de la de la tarde), incluyendo el paso de «bloqueante 5/7/10» a «pendiente de decisión» (el bloqueante operacional real = espacio VG, resuelto con opciones).
5. **Feedback registrado**: `80-agents/journal/feedback/session/2026-09-21-congelacion-martes-feedback.md` (canales RO verificados: `sudo ceph` requiere `-c /etc/pve/ceph.conf` en hades; K2 medible vía `pvesh /nodes/<n>/ceph/osd`; sugerencia de sección "canales por host" en runbook).

## Archivos

- Workspace: `~/aranea/work/continuity-20260922/` → CAPACITY-FREEZE.md, PLACEMENT-FREEZE.md, BUNDLE-DECISIONES-MARTES.md, WEDNESDAY-MANDATES-INDEX.md, raw/* (5 sondas).
- Vault: BACKUP-DR-OWNER-PROJECT.md (status_detail, tareas T-22..T-24), ARANEA-CONTINUIDAD-Y-VENTANA-25-26-SEP.md (delta del día), este change log, feedback.

## Sin cambios

F-01..F-14, tickets 018-021, timers/horarios, driver R2, Ceph/TrueNAS/PBS/guests (cero mutaciones; Echo operando), secretos (ninguno expuesto), MANDATO-P0 (sus erratas quedan registradas en el bundle, pendiente de incorporación por T-23/T-24).

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales (sólo workspace ~/aranea), memoria interna ni secretos.

## Rollback

- Documental: las notas del vault conservan historial de Obsidian; el workspace continuity-20260922 es aditivo (borrable sin afectar canon); erratas NO editaron fichas originales (quedan referenciadas, no reescritas).
