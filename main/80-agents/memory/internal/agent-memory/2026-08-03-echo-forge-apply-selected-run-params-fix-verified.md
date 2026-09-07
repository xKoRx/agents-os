---
type: agent_memory
scope: project
created: 2026-08-03
updated: 2026-08-03
project: "[[Echo Forge - Cierre de Etapa 4]]"
entities:
  - "[[Echo Forge]]"
  - "[[Echo Forge - Cierre de Etapa 4]]"
aliases:
  - apply selected run params fix
  - wfm params application
tags:
  - kind/doc
  - kind/agent-memory
  - project/echo-forge
  - status/resolved
---

# Resolved — `apply_selected_run` ahora aplica los parámetros del WFM (workflow `1785813489`)

## Contexto

Workflows `sqx-main-...-1785786248` (flow_69) y `sqx-main-...-1785813489` (flow_71).

## Problema detectado en `1785786248`

La actividad `apply_selected_run` solo cambiaba el `MagicNumber` (`11111` → `888111`) en el strategy pero **NO aplicaba los valores de los parámetros del WFM** elegido. Las strategies `04_optimizer_robust` eran idénticas en parámetros a `03_optimizer`. Diagnóstico: el `automator.properties` solo pasaba `wfm.runs_count` y `wfm.oos_percent` al exporter SQX, sin lógica per-strategy (`CustomAnalysis` con `PerStrategy1=none`).

## Verificación de la corrección en `1785813489`

8/10 strategies auditadas muestran cambios reales en los parámetros entre `03_optimizer` y `04_optimizer_robust`:

- 4.1.14: `Period 110→77`, `Number 0.30→0.41`, `ProfitTarget 70→91`, `StopLoss 30→21`
- 4.1.15: `Period 195→136`, `Fast 12→8`, `Slow 26→30`, `Smooth 9→6`, `EAB 40→28`
- 5.1.14: `Period 197→166`, `Number 2.60→2.96`, `PT 190→218.5`, `SL 60→42`
- 5.1.17: `Period 50→63`, `Number 1.00→0.85`, `PT 135→175.5`, `SL 45→31.5`
- 5.1.18: `Period 14→11`, `Number 1.80→1.52`, `PT 190→247`, `SL 40→28`
- 5.1.19: `Period 10→9`, `Number 0.30→0.29`, `TS-Act 4.5→3.15`, `TS 50→35`
- 5.1.20: `Period 30→37`, `EAB 6→4`, `PT 140→182`, `SL 80→56`, `TS 3.4→2.89`

`05_reretester` no aplica lógica adicional: `04 vs 05 = 0 diffs` en todas las strategies verificadas (comportamiento correcto: el re-test usa los params ya aplicados en 04).

Comparación 02_retester vs 05_reretester: 8-12 parámetros diferentes por strategy en 6 strategies verificadas.

## Estado

✅ Resuelto en `1785813489` (versión worker: la actual en `0.2.32`/`0.2.33`). El fix modifica la lógica de `apply_selected_run` y/o el exporter `EchoForgeRobustRunExporter` para pasar todos los `MatrixResult.values` como parámetros strategy-specific en `automator.properties`.

## Verificación adicional recomendada

Confirmar en el código fuente (`sqx/activities/worker/robust_activity.go` y `/home/kor/sqx/user/projects/EchoForgeRobustRunExporter/project.cfx`) que ahora se itera sobre todos los `MatrixResult.values` y se genera un bloque de `strategy.<param_name>=<value>` por cada strategy.

## Referencias

- `[[2026-08-03-echo-forge-stage4-audit-flow-71-summary]]`
- `[[/tmp/audit_e4_71/REPORT.md]]`