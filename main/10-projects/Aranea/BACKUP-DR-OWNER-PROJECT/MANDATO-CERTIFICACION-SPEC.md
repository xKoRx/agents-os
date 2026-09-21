---
title: "MANDATO 6 — Certificación y recuperación (restore drills + runbook + cierre)"
type: doc
schema_version: 1
status: active
area: "[[Aranea]]"
project: "[[BACKUP-DR-OWNER-PROJECT]]"
created: "2026-09-21"
updated: "2026-09-21"
tags: [kind/doc, area/aranea, domain/backup-dr]
---

# MANDATO 6 — Certificación y recuperación

**Ejecutor**: Ariadna (Backup/DR). **Base**: [[BACKUP-DR-RUNBOOK]] + [[BACKUP-DR-CHECKLIST]] + RESTORE-DRILL-TEMPLATE; WP-R7. **Principio**: restauración demostrada = único criterio de cobertura.

## Propósito

Mandato de certificación: restore drills y procedimientos de recuperación con evidencia.

## Contenido

## Drills a certificar (en orden de dependencia; targets scratch, jamás sobre producción)
1. **Restore completo 1 CT T0 desde PBS** → scratch (re-certificación con la plataforma de producción B1; patrón CT 990).
2. **Restore completo 1 VM T0 desde PBS** → scratch, con arranque y check de servicio (PRIMERA certificación VM completa del sistema; candidato: echo 140 con Echo cerrado, o PG 152 con su dato en zvol aparte — el SO restaurado + `SELECT 1` contra el dato vivo).
3. **Restore VM a backend alternativo** (pool1→local-lvm o nfs-vmbackup): valida la ruta "sin Ceph original" (DR-T4).
4. **Recuperación sin clúster original (parcial)**: VM cuya config se reconstruye con `pve-config` (R1.5) + storage.cfg + vmid conf — demostrar que con PBS + configs se levanta un guest sin el clúster (metadatos mínimos de reconstrucción §5 del mandato de réplica: vmid conf, storage.cfg, red/bridge, PBS fingerprint/token).
5. **Restore de datos desde la réplica pool2**: clonar 1 dataset hijo en TrueNAS y leerlo (valida §6 de la SPEC de réplica).
6. **Recuperación coordinada multi-zvol** (parcial/documental hasta ventana): orden PG/Mongo (dumps mandan) + MinIO (G1B) documentado en runbook.

## Procedimientos DR (estado)
- DR-T1/T4: ejecutables post B1 (drills 1-3). DR-T2: documental. DR-T3: mitiga con capa `nfs-vmbackup`; drill de mesa + restore cruzado. DR-T5: requiere TrueNAS config export (WP-B2) — drill en ventana. DR-T6: bloqueado por A7 (020/021) — 3-2-1 NO declarado.

## Gates
Drills a scratch: AUTO (sin ventana, targets aislados; restauraciones NUNCA sobre los originales). DR-T5 drill: ventana. Todo resultado PASS/FAIL con evidencia en change log; un drill FAIL 2× = deuda documentada en RUNBOOK §0, no "PASS condicional".

## Rollback / limpieza
Targets scratch se destruyen al terminar (identificación exacta del objeto; jamás en la misma operación que otro borrado); nada de producción se toca.

## DoD
Drills 1-3 PASS con evidencia; drill 4 documentado o ejecutado; MATRIZ (columna restore probado) y RUNBOOK actualizados; [[TWO-LAYER-BACKUP-SPEC]] §3 reconciliada; cierre con change log y bitácora del proyecto.
