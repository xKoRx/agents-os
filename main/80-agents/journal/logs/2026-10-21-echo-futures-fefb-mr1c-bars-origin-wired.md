---
type: change_log
schema_version: 1
created: 2026-10-21
project: "[[Echo Futures — Execution Client y Feed Batching]]"
tags:
  - kind/change-log
  - project/echo-futures-fefb
---

# 2026-10-21 — FEFB S01 MR1c: bars.origin wired (G1 repair), planner/matriz actualizados

- [[Echo Futures — Execution Client y Feed Batching]]: estado → S1_MR1C_READY_FOR_MANAGER_REVIEW (`d99e5108`, FF desde `82335b34`, publicado y con readback); bitácora MR1c agregada; entrada MR1 preservada como historial.
- [[EXECUTION-FEED-BATCHING-VERIFICATION]]: sección Evidencia MR1c (reproductores, campaña d99e5108_20261022T015808Z, cobertura universos reconciliados 621/643 y 1148/1214); etiqueta de base MR1 corregida por mandato del Manager (base = `1af0352f`; `dd175654` = correctivo interno).
- Cambio promovido por decisión del Primary Manager (G1 = BLOCKED BAR_ORIGIN_NOT_WIRED sobre `82335b34`); sin merge, sin deploy, sin accepted.
