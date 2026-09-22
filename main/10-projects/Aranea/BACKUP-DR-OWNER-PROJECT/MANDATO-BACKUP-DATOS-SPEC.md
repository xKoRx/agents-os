---
title: "MANDATO 3 — Backups de datos (Mecanismo B: cierres de deuda y cloud)"
type: doc
schema_version: 1
status: active
area: "[[Aranea]]"
project: "[[BACKUP-DR-OWNER-PROJECT]]"
created: "2026-09-21"
updated: "2026-09-21"
tags: [kind/doc, area/aranea, domain/backup-dr]
---

# MANDATO 3 — Backups de datos (Mecanismo B)

**Ejecutor**: Ariadna (Backup/DR). **Base**: no rehacer lo certificado (G1A/G1B/A1/R1/R1.5) — este mandato CIERRA deudas y habilita cloud, según la matriz de [[TWO-LAYER-BACKUP-SPEC]] §2.

## Propósito

Mandato de ejecución del Mecanismo B: cierre de deudas de datos y cloud priorizado según D-NEW-05.

## Contenido

## Operaciones (por orden de valor de riesgo)

> [!info] Orden nocturno (noche-5, BACKUP FIRST): primero T-21b/W-02 (protección autónoma), luego A3/A4/A7 por sus gates; el resto del carril Backup/DR no espera organización de storage.
1. **T-21b (gated: aplicar diff)**: fix tar-race R1 second-brain — diff probado `~/aranea/work/continuity-20260921/T21B-R1-TAR-RACE-FIX.diff`; DoD: run siguiente 3/3 unidades OK.
2. **W-02 ejecutor standby PBS (gates D2 a+b+c)**: implementación según especificación cerrada `~/aranea/work/continuity-20260923/W-02-BACKUPS-AUTONOMOS.md` — post-cierre Echo del viernes, fuera de ventana; sin auto-activación; flag manual.
3. **CouchDB A3 (gate G-A3: credencial `_reader`)**: dump diario `_all_dbs` → cifrado r0d-g1a.key → PBS; drill restore scratch (conteo docs vs live).
4. **MinIO recurrente (gate G-A4: owner)**: stream G1B semanal con regla de rotación de la SPEC (última copia verificable; ≥2 certificadas; anterior NUNCA se borra antes de certificar la nueva) + decisión versioning separada.
5. **A7 cloud por prioridad D-NEW-05 (gate G-A7: 020+021)**: repo restic cifrado en pCloud; primer push = PG+Mongo dumps → CouchDB → última copia MinIO verificable → configs+inventario (R1/R1.5/A5/pve/TrueNAS/PBS) → **Secret Zero con custodia externa independiente** (r0d-g1a/g1b keys + PBS pw; sin ellas el off-site es irrecuperable). Drill de descarga+descifrado clean-room tras el push. **3-2-1 NO se declara hasta A7 verificado.**
6. **WP-B2 exports (AUTO donde el canal exista)**: TrueNAS config export (verificar método API/SSH en fixture; DR-T5 lo requiere), OPNsense export, PBS config, pi-hole/CA según D5.

## Gates
G-T21B · D2(a/b/c) · G-A3 · G-A4 · G-A7(020+021) — cada uno independiente; sin gates, las operaciones quedan DEFER (no bloquean entre sí salvo dependencia de staging/PBS común).

## Riesgo
Dumps PG/Mongo en operación (03:00-03:45) ya autorizados en MP-01; A7 = push desde staging/PBS, sin I/O local significativo; sin credenciales en claro en ningún punto (custodia [[BACKUP-DR-KEY-RECOVERY]]).

## Rollback
Timers off por unidad; revocar token pCloud; el borrado de cualquier repo/remote = CLEANUP con autorización independiente.

## DoD
Deuda cerrada por ítem con su evidencia; matriz §2 actualizada (estado y RPO real); primer push A7 VERIFIED con drill de descarga PASS.
