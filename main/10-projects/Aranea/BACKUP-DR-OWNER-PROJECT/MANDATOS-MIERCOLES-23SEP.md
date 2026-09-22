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
updated: "2026-09-22"
---

# MANDATOS-MIERCOLES-23SEP

> [!warning] ERRATAS 22sep (mandato resolución integral de gates; detalle en [[ARANEA-CONTINUIDAD-Y-VENTANA-25-26-SEP]] delta mar 22)
> (1) **W-01 opción (b) SUPERSEDED**: era incoherente (`vgextend local-kronos` del host sobre un disco del guest; el datastore del guest es ext4 crudo sin VG ni tabla de particiones) y un datastore en `pool-kronos` violaba F-06 ("PBS datastore = local-kronos", FROZEN). Solución seleccionada: **P1-v3 grow in-place** (`lvextend +250G` + `resize2fs` online → ≈545G; sin `qm set`; sin reboot; datos intactos) — runbook `~/aranea/work/cierre-preparatorio-20260921/P1-GROW-IN-PLACE.md`; `W-01-PBS-GROWTH.md` marcado SUPERSEDED en hermes. Los comandos `qm set 180 -scsi1/-scsi2` quedan eliminados del paquete. (2) **Canal kronos = 192.168.31.120** (no .100, que es zeus). (3) **T-21b = diff v2** (`T21B-R1-TAR-RACE-FIX-v2.diff`): el 22sep hermes-state también falló por tar-race; v1 SUPERSEDED; runbook autosuficiente `T21B-RUNBOOK-v2.md` (DoD = run real 3/3, no el fixture). (4) **W-02 payload staged** en `~/aranea/work/w02-standby-20260922/` (units espejo ConditionPathExists + wrapper anti-doble-ejecución con freshness guard + instalador; manifiesto exacto de credenciales; R1 excluido del standby con justificación). (5) **R2: D-A inalcanzable** (runs 21 y 22sep perdidos por el apagado nocturno confirmado de hermes; máximo posible 5/7) → P4 = D-B cerrado. (6) Estado canónico del paquete = `PAQUETE-EJECUCION-25-26SEP.md` v2 con los 4 estados (READY/READY_AFTER_OWNER_GATE/BLOCKED/DEFER).

## Propósito

Paquete ejecutable para la ventana 25-26sep, preparado el 21sep (T-23 adelantado). Resuelve los 4 bloqueos de la congelación del martes con capacidad medida y sin decisiones técnicas pendientes: (1) PBS +300G inviable → alternativa con opciones owner; (2) W5 hades sin espacio → placement por VM; (3) W1/W2 → justificación workload single-disk + opción DEFER; (4) W3 → pi-hole en ATHENA y L2-dead, migración retirada. Además congela el diseño del ejecutor standby de backups (W-02), empaqueta el diff T-21b como paso ordenado, y reemplaza el MANDATO-P0 borrador por la **versión v2** con tabla de cambios trazable. **Nada ejecutado; todo gated.**

## Contenido

Canónico en `~/aranea/work/continuity-20260923/` (hermes): `W-01-PBS-GROWTH.md` (crecimiento datastore: (a) grow ≤250G / (b) 2º disco VG pool-kronos 733,87G — recomendada / (c) diferir), `W-02-BACKUPS-AUTONOMOS.md` (ejecutor standby PBS 180: 4 timers espejo, flag manual, Persistent=false, credencial custodiada, staging >3d, prueba negativa, rollback trivial; 4 gates owner; ejecución post-cierre Echo del viernes), `W-03-MIGRACIONES-POR-GUEST.md` (§0 justificación W1/W2 · §1 alta nfs-pool2 · §2 P0-2 103→116→137→113→115 · §3 W5 por VM zeus/hera/hades · §4 W3=D5), `W-04-VALIDACION-ECHO.md` (preflight GO/NO_GO por intervención, 10 checks fail-closed + cierre Echo por dump G1A sin filtro temporal), `MANDATO-P0-v2.md` (mandato de la ventana; reemplaza al borrador 20sep, queda archivado), `TABLA-APROBACION-23SEP.md` (única tabla de decisión owner, códigos de respuesta en 1 línea; urgentes **P1/P4 + P6 réplica** — P3 sin objeto por cancelación W1/W2; **P6 añadido 21sep noche-3**: GO/NO_GO del paquete réplica con gates G-REP-0..5), `MANDATO-JUEVES-24.md` (freeze T-24: READY/DEFER por mandato). Índice actualizado: `~/aranea/work/continuity-20260922/WEDNESDAY-MANDATES-INDEX.md`.

Cambios materiales v1→v2 trazados en MANDATO-P0-v2: +300G→opciones P1-1 (VG real 267,5G), 7/7→6/7 tolerancia cero, Prometheus→dump G1A, W5→placement por VM (hades 33,4G real), W3 fuera de la ventana (149 en ATHENA, L2-dead), justificación workload W1/W2 explícita, W-02 integrada, T-21b como paso ordenado. Regla reforzada: una aprobación general NO sustituye gates específicos. R2 sigue limitado a 6/7; su resultado no se anticipa (run del día se valida, no se renueva).

## Fuentes

- `~/aranea/work/continuity-20260922/` — CAPACITY-FREEZE, PLACEMENT-FREEZE, BUNDLE-DECISIONES-MARTES (D1-D8), raw/ (sondas 21sep).
- `~/aranea/work/continuity-20260921/` — E2-WP-HERMES-DECOUPLING.md, T21B-R1-TAR-RACE-FIX.diff (+TEST), E4-E5.
- [[PLACEMENT-DECISIONS-20260920]] · [[BACKUP-DR-CONTRACT]] §2 · [[ROADMAP-WP-BACKUP-DR]] · [[MATRIZ-59-GUESTS-BACKUP]] · [[BACKUP-DR-KEY-RECOVERY]] · [[FIRST-MAINTENANCE-WINDOW-20260920]].
