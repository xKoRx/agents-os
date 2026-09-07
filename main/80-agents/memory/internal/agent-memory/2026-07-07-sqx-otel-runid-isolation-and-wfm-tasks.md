---
type: agent_memory
scope: internal
created: 2026-07-07
updated: 2026-07-07
tags:
  - kind/agent_memory
  - tech/go
  - app/echo-forge
  - topic/workflow
  - topic/configuration
  - topic/isolation
---

# Continuidad Operativa: Aislamiento por Trace ID en DB, Filtro Optimizer en MinIO y Configuración de Tareas WFM (Symphony)

## Qué se hizo
- **Reversión de Ola en MinIO**: Se quitó la inyección del UUID en `req.Spec.Wave` al inicio del workflow `GenericSQXWorkflow` en [generic_workflow.go](file:///Users/rjara/go/src/github.com/xKoRx/symphony/sqx/workflows/generic_workflow.go). Las carpetas en MinIO vuelven a guardarse estáticamente en `wave_1/`.
- **Aislamiento por Trace ID en MongoDB**:
  - Agregado el campo `RunID` (`run_id` en BSON) a los structs de dominio: `StrategyMetadata`, `TypeRanking`, `WFMMatrix`, `WFMRunsDocument` y `WFMEvaluation` en [metadata.go](file:///Users/rjara/go/src/github.com/xKoRx/symphony/sqx/core/domain/metadata.go).
  - Extracción automática del Trace ID de OTel desde el contexto de Go (`ctx`) para asignarlo a `RunID` en los escritores ([steps.go](file:///Users/rjara/go/src/github.com/xKoRx/symphony/sqx/activities/worker/steps/steps.go) y [classify_and_rank.go](file:///Users/rjara/go/src/github.com/xKoRx/symphony/sqx/activities/worker/classify_and_rank.go)).
  - Modificado el adaptador Mongo en [adapter.go](file:///Users/rjara/go/src/github.com/xKoRx/symphony/sqx/adapters/metadata-mongo/adapter.go) para filtrar dinámicamente consultas por `run_id` si existe Trace ID en el contexto, logrando aislamiento absoluto por corrida de workflow.
- **Filtro de Subida de Optimizer**: Se configuró `UploadFromDisk` en [minio_storage.go](file:///Users/rjara/go/src/github.com/xKoRx/symphony/sqx/adapters/storage-minio/minio_storage.go) para que si la carpeta de la tarea contiene `"optimizer"`, solo se suban estrategias `.sqx` que comiencen por `"WF_Matrix"`.
- **Nuevas Tareas de Ejemplo**: Añadidas las tareas `"evaluate_wfm"` y `"classify_and_rank"` a [config.json](file:///Users/rjara/go/src/github.com/xKoRx/symphony/input/example/config.json).
- **Clasificación y Ranking de Runs Robustos**:
  - Añadido el campo `UseRobustMetrics` en `TaskSpec` y `ClassifyRequest` para diferenciar las ejecuciones de `classify_and_rank` que deben rankear los runs robustos seleccionados.
  - Modificada la actividad `classify_and_rank` para cargar los datos usando `ListSelectedRobustRuns` y usar sus métricas en lugar de la estrategia base.
  - Soportada la compatibilidad con `LogicalType` existente en `groupBySignature` (en `classification.go`) cuando la estrategia no tiene indicadores crudos.
  - Agregado el campo `RunID` en los modelos `SelectedRobustRun` y `RobustRunSetup`, propagándolo e indexándolo por `run_id` en MongoDB para aislamiento completo.
- **Pruebas y Verificación**: Compilado y pruebas unitarias `go test -race -cover ./sqx/...` validadas de forma exitosa, incluyendo el nuevo test `TestClassifyAndRankActivity_UseRobustMetrics`.

## Próximos pasos
- Monitorear ejecuciones del stager y validar aislamiento de Base de Datos para corridas simultáneas.
