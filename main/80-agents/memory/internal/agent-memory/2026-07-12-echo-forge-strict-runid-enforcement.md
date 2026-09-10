---
type: agent_memory
scope: internal
created: "2026-07-12"
updated: 2026-09-09
index_priority: never
memory_state: archived
load_policy: manual
indexable: false
tags:
  - kind/agent-memory
  - scope/internal
---

# Enforzamiento Estricto de RunID y Unificación de Uploader en Echo Forge

## Contexto y Decisiones
Tras las discusiones sobre la robustez y facilidad de troubleshooting en producción de Echo Forge, se establecieron las siguientes directrices estrictas:

1. **Unificación del Uploader en SQX**:
   - Se actualizó el uploader de estrategias para usar el adaptador robusto `strategies.MinioUploader` y propagar correctamente el `RequestID` en el contexto.

2. **Prohibición de Fallbacks Dinámicos de Rutas**:
   - Se eliminaron todos los fallbacks condicionales de prefijos. El sistema ahora exige de manera estricta y sin excepciones la presencia del `RunID` en los prefijos de MinIO (formato de 8 partes) y en la descarga en `import_metadata.go`.
   - Si no está disponible el `RunID` o no se encuentra la ruta exacta estructurada con él, el sistema falla de inmediato para evitar opacidad en el troubleshooting.

## Cambios Aplicados en la Sesión (Releases `0.1.108` - `0.1.109`)
- **Adaptadores y Core**:
  - `minio_uploader.go` (adaptador): Se inyectó `RequestID: contextx.GetRequestID(ctx)`.
  - `minio_uploader.go` (core): Se agregaron campos `RunID: jobConfig.RequestID` en los metadatos de archivos de configuración (`job_config.json`), archivos `.cfx` y marcador de carpetas (`.folder_marker`).
  - `domain.go` (SDK): Se simplificaron `GenerateObjectKey` y `ParseObjectKey` para forzar incondicionalmente el uso de `RunID`.
  - `job_config.go` y `steps.go` (actividades): Se eliminaron los fallbacks dinámicos en `GenerateStoragePrefix` y `getStoragePrefix` para usar siempre la estructura de versión con `RequestID`.
  - `import_metadata.go`: Se retiró el fallback legacy a la carpeta principal sin `RequestID`.

- **Operaciones**:
  - Se reinició el daemon local de screen `watcher` con el nuevo código.
  - Se compiló y desplegó la release `0.1.109` a Zeus. El worker de Temporal se actualizó y reinició exitosamente.
  - Se modificó la configuración del builder en `input/example/builder_test.cfx` (editando `config.xml` interno) para cambiar el valor `<MaxStrategies>` de `100` a `20`, limitando la generación de estrategias a 20.
  - Se corrigió `ParseConfigStep` en `steps.go` (watcher) para generar un UUID aleatorio si el OpenTelemetry TraceID es no-op o nulo (`00000000000000000000000000000000`), evitando así que la estructura de carpetas inicial se cree fuera de la carpeta del `RunID` en MinIO.

