---
type: agent_memory
scope: project
created: 2026-07-18
updated: 2026-07-18
tags:
  - tech/temporal
  - tech/go
  - project/symphony
  - bug/infinite-retry
---

# Memoria Interna: Análisis de Reintentos Infinitos en apply_selected_run

## Contexto
En la sesión del 2026-07-18 se analizó el cuelgue en Temporal del flujo `input/example` (`sqx-main-00_configs-v42-NDX-H1-L-1784420825`).

## Diagnóstico
1. **Fallback Indeseado**: `apply_selected_run` tiene un fallback que lista todas las estrategias de `source_folder` si el batch actual viene vacío (por ejemplo, porque `select_robust_run` no seleccionó nada).
2. **Inexistencia de Datos**: Esas estrategias no filtradas no tienen un registro de selección en MongoDB. La actividad falla con un error `mongo.ErrNoDocuments` al intentar cargarlo.
3. **Cuelgue (Retry Infinito)**: Las `ActivityOptions` del workflow establecen `MaximumAttempts: 0` (reintentos ilimitados). Temporal asume que el error de base de datos es transitorio y reintenta infinitamente, dejando la tarea pegada en la UI.
4. **Flujo de Apertura y Validación**:
   - **En el Workflow**: No se evalúa nada a priori para filtrar estrategias en `apply_selected_run`. Si la estrategia está en `current.Keys` (que fue repoblado por el fallback), se le dispara la actividad.
   - **En la Actividad**: La validación es puramente reactiva. Intenta cargar de MongoDB la selección robusta (`LoadSelectedRobustRun`) usando una clave generada de forma determinista (`selectedRobustRunKey`). Si no existe en la BD (porque no fue seleccionada), falla.
5. **Paralelismo**:
   - Tareas raíz en `config.json` son secuenciales.
   - Dentro de `group`, el origen `ranking` sin `LogicalType` especificado activa paralelismo por tipo lógico (`workflow.Go` lanzando sub-workflows concurrentes).
   - En tareas de procesamiento (como `evaluate_wfm` y `select_robust_run`), el procesamiento de estrategias del lote se lanza en paralelo mediante futuros de Temporal.

## Próximos Pasos (para futuros agentes)
Cuando se retome la sesión para aplicar fixes:
1. Modificar la lógica de `apply_selected_run` para no autocompletar el batch si proviene de una tarea de selección previa que filtró a cero resultados.
2. Definir errores no reintentables en la `RetryPolicy` de Temporal (ej: no reintentar ante `ErrWFMMatrixNotFound` / `mongo.ErrNoDocuments`).
