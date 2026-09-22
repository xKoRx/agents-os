---
type: change_log
schema_version: 1
scope: area
area: "[[Aranea]]"
project: "[[BACKUP-DR-OWNER-PROJECT]]"
created: 2026-09-22
session: 2026-09-22-resolucion-integral-gates
mandate: "ARANEA · ONE-SHOT — Resolución integral de gates de ejecución (P1, T-21b, W-02, R2/018, paquete 25-26sep)"
tags:
  - kind/change-log
  - area/aranea
  - domain/backup-dr
---

# Change log — 2026-09-22 · Resolución integral de gates (Aranea Backup/DR)

## Contexto

Mandato owner ONE-SHOT: resolver definitivamente las incertidumbres técnicas del paquete de ejecución 25-26sep (P1 PBS, T-21b tar-race, W-02 standby, R2/018) y consolidar el paquete con 4 estados. Modo: investigación directa read-only en PVE/PBS/hermes + preparación ejecutable + edición documental. Cero mutaciones productivas.

## Cambios en vault (Sistema 2 / proyectos)

- `10-projects/Aranea/BACKUP-DR-OWNER-PROJECT/ARANEA-CONTINUIDAD-Y-VENTANA-25-26-SEP.md` — delta nuevo "mar 22 · RESOLUCIÓN INTEGRAL DE GATES" (P1 resuelto, T-21b v2, W-02 payload, R2 D-B, K2 87,03/87,09%, 018 propuesta, errata canal) + sección "Gate vigente" actualizada (P1-v3 reemplaza `qm set -scsi2`; D-B cerrado; errata kronos=.120).
- `10-projects/Aranea/BACKUP-DR-OWNER-PROJECT/BACKUP-DR-OWNER-PROJECT.md` — bitácora 2026-09-22 + status_detail ampliado.
- `10-projects/Aranea/BACKUP-DR-OWNER-PROJECT/CAPACITY-AND-RESERVATIONS.md` — §4 errata: opción recomendada anterior (2º disco pool-kronos) SUPERSEDED; P1-v3 grow in-place +250G → ≈545G; delta vs presupuesto 595G registrado con condición D-piloto.
- `10-projects/Aranea/BACKUP-DR-OWNER-PROJECT/K2-CEPH-RISK-20260920.md` — serie completa ampliada (21sep 17:31/22:39 + 22sep 08:12) y warning de tendencia al alza; veredicto SAFE_TO_DEFER sigue fechado y no garantiza futuro.
- `10-projects/Aranea/BACKUP-DR-OWNER-PROJECT/MANDATOS-MIERCOLES-23SEP.md` — erratas 22sep en banner (6 puntos: W-01(b) superseded, canal .120, T-21b v2, W-02 payload, D-A inalcanzable, paquete v2).

## Cambios en workspace hermes (evidencia y ejecutables)

- `~/aranea/work/cierre-preparatorio-20260921/PAQUETE-EJECUCION-25-26SEP.md` — v2 consolidado: 4 estados canónicos (READY/READY_AFTER_OWNER_GATE/BLOCKED/DEFER), deltas 22sep, sin comandos `qm set 180 -scsi1/-scsi2`, propuesta técnica 018, autorizaciones consolidadas. K2/P6/infra siguen independientes.
- `~/aranea/work/cierre-preparatorio-20260921/P1-GROW-IN-PLACE.md` — NUEVO runbook definitivo P1-v3: investigación completa (scsi0/1/2, ext4 crudo sin tabla, VGs, F-06, dependencias de arranque), solución única sustentada, preflight fail-closed, ejecución, verificación de datos pre-existentes, round-trip de restauración, aborto por etapa, recuperación, gates. Reemplaza la operación P1 del GATE (marcada SUPERSEDED).
- `~/aranea/work/cierre-preparatorio-20260921/GATE-AUTORIZACION-PUNTUAL-22SEP.md` — errata crítica 22sep en header (canal kronos .120; P1 superseded → P1-GROW-IN-PLACE; P2a usa diff v2). Resto vigente.
- `~/aranea/work/continuity-20260921/T21B-R1-TAR-RACE-FIX-v2.diff` — NUEVO (sha256 1ad62df8…): staging atómico para second-brain Y hermes-state; dry-run limpio sobre hash vigente bca1d148…; `bash -n` OK.
- `~/aranea/work/continuity-20260921/T21B-FIX-TEST-v2.sh` — NUEVO fixture: staging 12/12 íntegro con escritor concurrente; tar directo reproduce fallo; exclusiones rsync verificadas; pruebas negativas sin falsos PASS.
- `~/aranea/work/continuity-20260921/T21B-RUNBOOK-v2.md` — NUEVO runbook autosuficiente T-21b (copiar/aplicar/validar/run real 3/3/rollback/registro).
- `~/aranea/work/continuity-20260921/T21B-R1-TAR-RACE-FIX.diff` — marcado SUPERSEDED en header (no aplicar).
- `~/aranea/work/continuity-20260923/W-01-PBS-GROWTH.md` — marcado SUPERSEDED (opción (b) incoherente + violación F-06; no ejecutar).
- `~/aranea/work/w02-standby-20260922/` — NUEVO: README-W02.md (procedimiento definitivo, 8 aspectos resueltos, gates a/b/c) + payload/ (4 pares unit/timer espejo ConditionPathExists+Persistent=false, aranea-sb-wrapper.sh con freshness guard anti-doble-ejecución, install-w02.sh idempotente). Nada desplegado en PBS.

## Evidencia nueva (22sep 08:00-09:3x -03)

- VM 180 `qm config` completo en kronos .120 (scsi0 64G / scsi1 300G serial pbs-data / scsi2 libre); PBS guest: ext4 crudo /dev/sdb, fstab UUID+nofail, drop-ins fail-closed Requires=mnt-pbs-data.mount, datastore.cfg main verify-new true, chunks 65.536 dirs, snapshots A1 del día (PG 10:51:56Z / Mongo 10:51:22Z).
- `vgs/pvs/pvesm` kronos: local-kronos 267,51G VFree sin thin pool; pool-kronos 733,87G VFree (PV /dev/sdc Patriot P3-1TB ROTA=0).
- Hermes: boots journal (apagado nocturno 2ª noche 01:01:48 → arranque 07:50:42), timers 6 vivos (R2 LAST=- → run de hoy perdido), manifest R1 20260922-075044 (2 unidades FAIL tar-race), hash r1-backup.sh bca1d148….
- Ceph 08:12: osd.0/2 87,03/87,09% HEALTH_WARN; Kafka MCP: ~130 topics (transporte efímero RF=3; topics cert mcp-cert-*/e02cert-*).

## Decisiones técnicas registradas (no requieren owner salvo firma)

- P1: grow in-place única solución F-06-compliant; +250G elegido (≈545G; trade VFree 17,51G documentado); opción apilar LV como PV rechazada (fragilidad, KISS).
- W-02: R1 excluido del standby (fuentes en hermes); anti-doble-ejecución por freshness guard (snapshot del día / manifiesto <20h → SKIP); monitoreo v1 logs (alertas push sigue GAP → MP-06).
- 018: kafka/argus = RECONSTRUIBLE como PROPUESTA fundamentada; la firma del owner cierra el ticket.

## Pendientes owner (sin cambios de fondo)

P1-v3 · P2a (diff v2) · W-02a/b/c · K1 · P6 G-REP-0..5 · 018 firma · 020/021 · A3 · 112 · K2 escalamiento si condición · limpieza snapshots legacy pool2.
