---
type: agent_memory
scope: internal
created: 2026-07-13
updated: 2026-09-09
index_priority: never
indexable: false
load_policy: manual
memory_state: archived
tags:
  - kind/agent_memory
  - tech/go
  - app/symphony
  - topic/workflow
  - topic/robustness
---

# Continuidad Operativa: Corrección de Listado y Eliminación de Fallbacks en Robust Run (2026-07-13)

## Síntoma y Causa Raíz
Se detectó una duplicación y multiplicación indeseada de archivos en MinIO bajo el prefijo `04_optimizer_robust`.
1. **Falta de limpieza y aislamiento**: Las estrategias se compilaban físicamente en el directorio local compartido `output/robust`. Como esta carpeta no se limpiaba tras procesar cada estrategia, los archivos se acumulaban.
2. **Subida recursiva masiva**: `UploadFromDisk` escaneaba toda la carpeta `output/robust` y subía recursivamente todos los archivos presentes en el disco bajo el prefijo de la estrategia activa.
3. **Salto silencioso**: Si el batch del workflow venía vacío (por ejemplo, después de un `group` task), la tarea `apply_selected_run` se saltaba silenciosamente con un `continue` en lugar de listar desde el `SourceFolder`.

## Cambios Implementados

1. **Workflow (`generic_workflow.go`)**:
   - Agregamos la consulta dinámica vía `list_strats` en `apply_selected_run` si el batch `current` viene vacío, forzando la lectura de estrategias directamente desde el `SourceFolder` (`"03_optimizer"`).
2. **Activity (`robust_activity.go`)**:
   - **Eliminación de fallbacks**: Retiramos por completo la lógica recursiva de búsqueda alternativa y guess-directories para descargas. Si el archivo no está en la clave exacta en el folder de origen, la descarga falla de inmediato (fallo catastrófico).
   - **UploadPrefixFilter**: Se inyecta el nombre base del archivo sin extensión como filtro en `StrategyMeta`, forzando a que `UploadFromDisk` solo suba el `.sqx` robusto correspondiente al procesamiento actual.
   - **Limpieza en defer**: Implementamos limpieza diferida (`defer os.Remove(...)`) de los archivos temporales locales (`SourceStrategyArtifact` y `TargetStrategyArtifact`) para mantener despejado el disco del worker.
