---
type: change_log
schema_version: 1
scope: session
area: "[[Aranea]]"
project: "[[BACKUP-DR-OWNER-PROJECT]]"
session: 2026-09-22-resolucion-gates-backup-dr-summary
created: 2026-09-22
tags:
  - kind/change-log
  - area/aranea
  - domain/backup-dr
---

# Change log — 2026-09-22 · Verificación del mandato ONE-SHOT (reauditoría gates)

## Contexto

Sesión de verificación independiente sobre la sesión `2026-09-22-resolucion-integral-gates` (otra superficie): re-auditar sus claims contra la realidad (live read-only) y cerrar las incoherencias documentales residuales antes del ciclo T-24/owner. Cero mutaciones de infraestructura.

## Verificación (evidencia live)

- Hash `~/aranea/bin/r1-backup.sh` = `bca1d148…17366` (patch NO aplicado) + dry-run limpio del diff v2 sobre el árbol vivo + staging v2 ≈2,9G pico sobre 36G libres.
- kronos .120 live: VFree `local-kronos` 267,51G (≥250G), `qm config 180` scsi1 = serial `pbs-data` 300G, `pool-kronos` VFree 733,87G → runbook P1-v3 correcto y ejecutable.
- PBS .123 live: `/mnt/pbs-data` ext4 295G/48G (18%), proxmox-backup + proxy active → precondiciones P1-v3 OK.
- Manifests R1 22sep (run 20260922-075044 catch-up): FAIL ×2 tar-race (second-brain + hermes-state, sha null) → v2 justificado; A1 PG/Mongo indemnizados 10:50Z.
- K2 día 22 COMPLETE: L1 87,03/87,09% 08:12 · L2 87,10/87,15% 09:13 (Δ71 min) — condición ≥89% ×2 NO disparada.

## Correcciones documentales

- `~/aranea/work/cierre-preparatorio-20260921/GATE-AUTORIZACION-PUNTUAL-22SEP.md`: §P1 reestructurado (P1-v3 VIGENTE al frente; bloque `qm set 180 -scsi2` con banner `[SUPERSEDED — NO EJECUTAR NI FIRMAR]` — la fila vieja del registro deja de ser firmable y la tabla registra P1-v3); §P2a actualizado al diff v2 (título, hash del diff, verificación previa de hash en comandos, certificación = 3 runs 23-25sep); §K2 con resultado del día.
- `~/aranea/work/continuity-20260923/TABLA-APROBACION-23SEP.md`: banner SUPERSEDED (reemplazada por el GATE; códigos obsoletos).
- `~/aranea/work/continuity-20260923/MANDATO-JUEVES-24.md`: paso 1 (ingesta de decisiones) apunta al gate vigente, no a la tabla muerta.
- `10-projects/Aranea/BACKUP-DR-OWNER-PROJECT/K2-CEPH-RISK-20260920.md`: fila lectura 2 del día 22.
- `10-projects/Aranea/BACKUP-DR-OWNER-PROJECT/ARANEA-CONTINUIDAD-Y-VENTANA-25-26-SEP.md`: delta "Verificación Ariadna 22sep" (certificación técnica + correcciones + K2 COMPLETE).

## Sin cambios (verificado, no tocado)

`r1-backup.sh` (hash intacto), timers/systemd, PBS y kronos (sólo lectura), payload W-02 (staged, sin secretos; scripts shell `bash -n` OK), proyecto del gemelo (claims verificados ciertos; sin reescritura de su histórico).
