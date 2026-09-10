---
type: doc
index_priority: never
indexable: false
load_policy: manual
memory_state: archived
status: active
tags:
  - kind/known-error
  - area/symphony
  - tech/temporal
  - tech/sqx
created: 2026-07-30
updated: 2026-09-09
source_session: sqx-main-00_configs-v1-NDX-H1-L-1785388958
project: "[[Symphony]]"
entities:
  - "[[AGENTS OS]]"
---

# Known Error — Symphony WFM Batch Vacío 1785388958

## Síntoma

El usuario reporta que el flujo `sqx-main-00_configs-v1-NDX-H1-L-1785388958`
(strategy=`example_flow_46`, v1, wave=test) "no siguió desde 05_reretester en
adelante". El flujo SÍ se ejecutó completo a nivel Temporal, pero terminó
después del task `05_reretester / project` con `WorkflowExecutionCompleted` y
**sin ejecutar** `trade_list_exporter`, `generate_report`, `mt5_exporter`.

## Causa confirmada (evidencia)

El workflow ejecutó 46 actividades y cerró con `Completed` en
`2026-07-30T06:59:12Z`. La causa NO es un crash:

- `wfm_runs` para `example_flow_46` en MongoDB `forge`: 14 documentos
- `selected_robust_runs` para `example_flow_46`: 12 documentos
- `EchoForgeRobustRunExporter` (Kronos) log final:
  `EchoForgeAutomatorRobustRun: Processing results group NDX_L_H1_example_flow_46_v1_Strategy_3.1.17.z0`
  → solo 1 estrategia produjo output (`input=1, output=1`)

El journalctl de Kronos registra explícitamente:

```
06:58:51 ... "Actividad apply_selected_run completada con éxito"
06:58:51 ... "Procesando task", folder=05_reretester, type=project, total_tasks=11, index=8
06:59:12 ... "Actividad retornó batch vacío, terminando flujo", task_folder=05_reretester, remaining_tasks=3
```

El log del exporter también muestra que cada invocación del
`EchoForgeRobustRunExporter` procesa 1 sola estrategia de input. Con 12
invocaciones en paralelo, 11 quedaron sin output (no sobrevivieron al filtro
interno del exporter). Solo `Strategy_3.1.17.z0` quedó como robusta.

## Por qué la actividad `project` retorna batch vacío

El config actual del flow (`input/example/config.json`) declara:

- `wfm_params.min_pass_cells: 6` (WFM 3x3 = 9 cells; pedir 6 es razonable)
- `wfm_params.max_dispersion: 0.2` (20%)
- `top_n_per_logical_type: 2` para el `group` 02_retester
- `ranking.weights: pf=30, sharpe=30, drawdown=40`

Combinado con sólo 14 candidatos ingresados al WFM (un
`EchoForgeOverviewExporter` los reduce desde el retester), el filtro final del
exporter deja **solo 1 estrategia robusta** por logical_type. Para
`05_reretester` se requiere `target_tops: 5` y `top_n_per_logical_type: 2`
alimentado por `02_retester`, no por `04_optimizer_robust`. La
`select_robust_run` que se ejecuta en `04_optimizer_robust` aplica su propio
filtro y, sobre los 12 candidatos, solo calza 1 que satisface el criterio
compuesto del exporter.

## Diagnóstico

1. Recuperar workflow `sqx-main-00_configs-v1-NDX-H1-L-1785388958` vía Temporal:
   ```bash
   go run scratch/inspect_workflow_1785388958.go
   ```
2. En el worker Kronos/Hera/Zeus:
   ```bash
   grep "1785388958" /var/log/symphony/symphony-worker.log | grep -iE
     "apply_selected_run|select_robust_run|batch vacio|remaining_tasks"
   ```
3. En MongoDB `forge`:
   ```bash
   db.selected_robust_runs.find({"strategy_id": /flow_46/}).count()
   db.wfm_runs.find({"wave_key":"test", "strategy_id": /flow_46/}).count()
   ```

## Solución propuesta (diseño separado, ya entregada a otra IA)

- Relajar `min_pass_cells` (bajar a 4-5), `max_dispersion` (subir a 0.30) o
  eliminar el segundo filtro de robustas intermedio cuando el número de
  candidatos es bajo.
- Añadir fallback en `select_robust_run` para que si el exporter produce 0
  outputs, reteste el último set con `ranking` simple.
- Documentar la regla: cuando `apply_selected_run` produce N<`target_tops`,
  emitir warning y permitir continuar con `top_n` real, no abortar.
