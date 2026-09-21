---
type: doc
schema_version: 1
status: active
area: "[[Aranea]]"
project: "[[BACKUP-DR-OWNER-PROJECT]]"
related:
  - "[[ARANEA-CONTINUIDAD-Y-VENTANA-25-26-SEP]]"
  - "[[FIRST-MAINTENANCE-WINDOW-20260920]]"
  - "[[MANDATOS-IMPLEMENTACION-BACKUP-DR]]"
  - "[[PLACEMENT-DECISIONS-20260920]]"
aliases:
  - Mandatos miércoles 23sep
  - Paquete ventana 26sep
tags:
  - kind/doc
  - area/aranea
  - domain/backup-dr
created: "2026-09-21"
updated: "2026-09-21"
---

# MANDATOS-MIERCOLES-23SEP

## Propósito

Paquete ejecutable para la ventana 25-26sep, preparado el 21sep (T-23 adelantado). Resuelve los 4 bloqueos de la congelación del martes con capacidad medida y sin decisiones técnicas pendientes: (1) PBS +300G inviable → alternativa con opciones owner; (2) W5 hades sin espacio → placement por VM; (3) W1/W2 → justificación workload single-disk + opción DEFER; (4) W3 → pi-hole en ATHENA y L2-dead, migración retirada. Además congela el diseño del ejecutor standby de backups (W-02), empaqueta el diff T-21b como paso ordenado, y reemplaza el MANDATO-P0 borrador por la **versión v2** con tabla de cambios trazable. **Nada ejecutado; todo gated.**

## Contenido

Canónico en `~/aranea/work/continuity-20260923/` (hermes): `W-01-PBS-GROWTH.md` (crecimiento datastore: (a) grow ≤250G / (b) 2º disco VG pool-kronos 733,87G — recomendada / (c) diferir), `W-02-BACKUPS-AUTONOMOS.md` (ejecutor standby PBS 180: 4 timers espejo, flag manual, Persistent=false, credencial custodiada, staging >3d, prueba negativa, rollback trivial; 4 gates owner; ejecución post-cierre Echo del viernes), `W-03-MIGRACIONES-POR-GUEST.md` (§0 justificación W1/W2 · §1 alta nfs-pool2 · §2 P0-2 103→116→137→113→115 · §3 W5 por VM zeus/hera/hades · §4 W3=D5), `W-04-VALIDACION-ECHO.md` (preflight GO/NO_GO por intervención, 10 checks fail-closed + cierre Echo por dump G1A sin filtro temporal), `MANDATO-P0-v2.md` (mandato de la ventana; reemplaza al borrador 20sep, queda archivado), `TABLA-APROBACION-23SEP.md` (única tabla de decisión owner, códigos de respuesta en 1 línea; urgentes P1/P3/P4), `MANDATO-JUEVES-24.md` (freeze T-24: READY/DEFER por mandato). Índice actualizado: `~/aranea/work/continuity-20260922/WEDNESDAY-MANDATES-INDEX.md`.

Cambios materiales v1→v2 trazados en MANDATO-P0-v2: +300G→opciones P1-1 (VG real 267,5G), 7/7→6/7 tolerancia cero, Prometheus→dump G1A, W5→placement por VM (hades 33,4G real), W3 fuera de la ventana (149 en ATHENA, L2-dead), justificación workload W1/W2 explícita, W-02 integrada, T-21b como paso ordenado. Regla reforzada: una aprobación general NO sustituye gates específicos. R2 sigue limitado a 6/7; su resultado no se anticipa (run del día se valida, no se renueva).

## Fuentes

- `~/aranea/work/continuity-20260922/` — CAPACITY-FREEZE, PLACEMENT-FREEZE, BUNDLE-DECISIONES-MARTES (D1-D8), raw/ (sondas 21sep).
- `~/aranea/work/continuity-20260921/` — E2-WP-HERMES-DECOUPLING.md, T21B-R1-TAR-RACE-FIX.diff (+TEST), E4-E5.
- [[PLACEMENT-DECISIONS-20260920]] · [[BACKUP-DR-CONTRACT]] §2 · [[ROADMAP-WP-BACKUP-DR]] · [[MATRIZ-59-GUESTS-BACKUP]] · [[BACKUP-DR-KEY-RECOVERY]] · [[FIRST-MAINTENANCE-WINDOW-20260920]].
