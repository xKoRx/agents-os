---
type: agent_memory
scope: internal
created: "2026-07-12"
updated: "2026-07-12"
load_policy: manual
indexable: false
tags:
  - kind/agent-memory
  - scope/internal
---

# Propagación de RequestID a Subflujos Secuenciales y Fallback en import_metadata

## Contexto y Cambios
En la última parte de la sesión de estabilización de Echo Forge, se realizaron las siguientes correcciones críticas para lograr una corrida E2E perfecta:

1. **Propagación del RequestID en Subflujos Secuenciales (`generic_workflow.go`)**:
   - Se identificó que la llamada secuencial a `NewGroupRequest` y `NewProjectRequest` dentro del helper `handleGroupTask` no propagaba el `RequestID` original de la ejecución. Esto causaba que los subflujos secuenciales generaran un RequestID aleatorio, rompiendo el aislamiento y la trazabilidad de los archivos.
   - Se corrigieron todas las llamadas agregando `runtime.WithRequestID(req.RequestID)`.

2. **Fallback Dinámico en MinIO (`import_metadata.go`)**:
   - Debido a que las pruebas y simulaciones a mitad de flujo utilizan carpetas preexistentes en MinIO (mock data) creadas sin RequestID, la actividad `import_metadata` fallaba al buscar los archivos con la ruta de prefijo estructurada (`wave_<wave_key>/<request_id>/...`).
   - Se implementó un mecanismo de fallback dinámico: si la descarga falla utilizando el prefijo con `RequestID`, la actividad intenta de forma automática descargar los archivos utilizando el prefijo heredado (`wave_<wave_key>/...`). Si tiene éxito, actualiza la ruta internamente y continúa la ejecución de manera transparente.

## Estado del Sistema y Verificación E2E
- Se empaquetó y desplegó la versión **`0.1.107`** del SQX Worker a Zeus. El stager de Zeus aplicó la versión y reinició el worker correctamente.
- Se inició un flujo completo de prueba (`GenericSQXWorkflow`) a través de Temporal usando el driver `test_complete_flow.go` con `zeus-e2e-...` RequestID.
- La ejecución corrió correctamente en el worker de Zeus. La actividad `import_metadata_activity` realizó de forma exitosa el fallback dinámico para los datos mock del test, y el flujo completo completó exitosamente todas sus etapas (`import_metadata` -> `select_robust_run` -> `apply_selected_run` -> `verify_robust_run_setup`).
- El workflow de Temporal terminó con estado exitoso: `✅ Complete workflow finished successfully!`.
- Con esto se valida que todo el ciclo de control y su aislamiento de datos quedaron 100% estabilizados.
