---
type: log
scope: journal
created: "2026-07-06"
updated: "2026-07-06"
---

# Echo Forge Sequential Chunking & Extension Matching Fix Journal Log

## Cambios del Monorepo (Symphony)
- **Ruta de Archivo**: [generic_workflow.go](file:///Users/rjara/go/src/github.com/xKoRx/symphony/sqx/workflows/generic_workflow.go)
- **Detalle Técnico**:
  - Inyección del `RequestID` (UUID de ejecución) en `req.Spec.Wave` al inicio del workflow genérico para aislar las tablas de base de datos y almacenamiento de cada corrida de forma absoluta.
  - Corrección de la variable `current` del lote para no ser sobrescrita con vacíos al completar tareas `project` secundarias.
  - Filtrado en `handleGroupTask` para intersectar estrategias de base de datos contra el batch actual.
  - Reemplazo de `grp-groupTask.Folder` por `subflow` en los IDs de Temporal.
- **Ruta de Archivo**: [steps.go](file:///Users/rjara/go/src/github.com/xKoRx/symphony/sqx/activities/worker/steps/steps.go)
- **Detalle Técnico**:
  - Extracción y uso de la ola estática (el prefijo antes del primer guion `-` en `Wave`) al construir la ruta de MinIO para descargar archivos `.cfx` de configuración. Esto soluciona la falla de descarga de configs ya que estas son subidas previamente por el usuario bajo `wave_1/`.
- **Ruta de Archivo**: [minio_storage.go](file:///Users/rjara/go/src/github.com/xKoRx/symphony/sqx/adapters/storage-minio/minio_storage.go#L189-L219)
- **Detalle Técnico**:
  - Restringimos el renombrado de estrategias con prefijo del constructor (`NDX_L_H1_...`) solo para archivos que no cuenten con las partes de convención de nombres.
  - Se mantiene la limpieza de los prefijos generados por SQX al subir archivos (`WF_Matrix_-_` a `WF_Matrix-` y `WF_-_` a `WF-`).
- **Acción Adicional**:
  - Despliegue de la versión `0.1.56` en Zeus.
