---
type: agent_memory
scope: internal
created: 2026-07-07
updated: 2026-07-07
tags:
  - kind/agent_memory
  - tech/go
  - app/symphony
  - topic/wfm
  - topic/filtering
---

# Continuidad Operativa: Comportamiento de Filtrado en evaluate_wfm (Symphony)

## Consulta de Filtrado de Estrategias FAILED en evaluate_wfm
- Se investigó la tarea `evaluate_wfm` del proceso de `sqx` en `Symphony`.
- Se confirmó que la actividad `evaluate_wfm` no realiza consultas al estado de base de datos (`StrategyState.GlobalState` o `Status` = `"FAILED"`). El método `IsValid()` del adaptador de Mongo (que filtra por `globalStateFailed`) no se invoca en esta tarea.
- Sin embargo, el workflow (`generic_workflow.go`) sí filtra del batch final todas las estrategias cuyo veredicto de evaluación WFM sea `"FAIL"` (solo conserva aquellas con `"PASS"` o `"WARN"`).
- **Filtro preventivo de etapas previas**: Las estrategias que fallan en etapas anteriores (como `retest` o `optimizer`) son removidas del lote activo (`current.Keys`) por las actividades previas en el pipeline del workflow. Por lo tanto, no llegan a ser evaluadas por `evaluate_wfm`.
- Además, en `evaluate_wfm.go`, si la matriz no se encuentra y el `export_run` de optimización general está `complete`, la actividad de WFM retorna veredicto `"FAIL"` (descarte legítimo) en lugar de error, permitiendo que el workflow la filtre del batch.

## Parámetro `folder` y Origen de Datos en `evaluate_wfm`
- **Parámetro `folder`**: En la configuración del workflow/campaña (por ejemplo, en `config.json`), la tarea de tipo `evaluate_wfm` puede tener una clave `"folder"` (por ejemplo, `"03_wfm_optimizer"`). Sin embargo, el workflow (`generic_workflow.go` y su contraparte de grupo) no utiliza ni propaga este parámetro `folder` a la actividad `evaluate_wfm`.
- **Origen de los Datos**: La actividad de evaluación de WFM no lee archivos de MinIO ni de disco. Los datos (la matriz WFM y las corridas) se leen directamente de las colecciones de **MongoDB** (`wfm_matrices` y `wfm_runs`) utilizando el adaptador `metadata-mongo` con el `wfm_run_key` (o `wave_key` + `strategy_id` como fallback).
- **Independencia de carpeta**: Si no se define o cambia la propiedad `"folder"` en la tarea `evaluate_wfm`, no habrá impacto en la carga de resultados de la actividad de WFM, ya que toda la información proviene de MongoDB, la cual fue insertada previamente por la tarea `extractor` o `metadata_import`.

## Origen de las Estrategias a Evaluar (`current.Keys`)
- **Estado del Workflow**: Las estrategias que evalúa `evaluate_wfm` no se obtienen escaneando carpetas de disco ni MinIO en el momento. Se leen del estado del lote activo del workflow (`current.Keys`).
- **Flujo de Pipeline**: Cada tarea previa de tipo `project` (como `builder`, `retester`, `optimizer`) o `metadata_import` toma un lote de entrada, lo procesa y devuelve un lote de salida actualizado (`current.Keys`). Al llegar a la etapa `evaluate_wfm`, esta simplemente itera sobre las estrategias que sobrevivieron y están presentes en `current.Keys` en ese momento de la ejecución.

## Manejo de Renombrado de Estrategias y Prefijos (`WF_Matrix-`, `WF-`)
- **Renombrado en MinIO/Storage**: Durante la optimización, las estrategias cambian su nombre original (`abc123.sqx`) a prefijos como `WF_Matrix-abc123.sqx` o `WF-abc123.sqx` al subirse a MinIO (debido a las reglas de normalización en `minio_storage.go`).
- **Desalineamiento en MongoDB**: Sin embargo, en MongoDB la base de datos registra las matrices y resultados usando la clave limpia original (`abc123`) removiendo los prefijos de optimización (ej. `"WF Matrix - "` en `steps.go`).
- **Solución con `cleanStrategyID`**: Se implementó una función helper `cleanStrategyID` en `generic_workflow.go` que remueve los prefijos comunes (`WF_Matrix-`, `WF-`, `WF_Matrix_-_`, `WF_-_`, `WF Matrix - `) y la extensión `.sqx` antes de generar el `wfmRunKey` o consultar MongoDB en actividades de validación y de WFM. Esto garantiza que la consulta a la base de datos de MongoDB coincida perfectamente con el ID de la estrategia original a pesar de que el archivo físico en MinIO tenga el nombre optimizado.



