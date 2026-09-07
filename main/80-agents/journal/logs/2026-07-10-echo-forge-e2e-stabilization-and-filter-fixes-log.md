---
type: change_log
scope: change
created: 2026-07-10
updated: 2026-07-10
area: "[[Symphony]]"
project: "[[EchoForge]]"
application: "[[Symphony]]"
entities:
  - "[[EchoForge]]"
  - "[[Symphony]]"
related: []
aliases: []
confidence: high
source_session: 19122e0a-c18e-4878-b20d-1754f25b7755
load_policy: manual
indexable: false
index_priority: never
tags:
  - app/symphony
  - area/symphony
  - kind/changelog
  - project/echoforge
  - scope/change
---

# Echo Forge E2E Stabilization and Filter Fixes Change Log

## Cambios Realizados

- **`minio_storage.go`**:
  - Modificado el condicional de subida de archivos `.sqx` para tareas del optimizador. En lugar de verificar si el nombre del directorio de la tarea contiene `"optimizer"`, ahora se verifica si contiene `"wfm"`. Esto permite que las tareas del optimizador estándar (`03_optimizer`) suban con éxito sus estrategias optimizadas a MinIO y evita que el child workflow finalice de forma prematura.

- **`manifest.json`**:
  - Version bump a `0.1.75` con notas de versión actualizadas para la corrección del filtro de subida del optimizador.

- **`inspect_postgres.go` (Scratch)**:
  - Restaurado el script para agrupar y contar registros de estrategias registradas en Postgres por carpeta de tarea (`task_folder`).

- **`inspect_mongo.go` (Scratch)**:
  - Creado el script para contar y verificar el registro de matrices (`wfm_matrices`) y ejecuciones WFM (`wfm_runs`) asociadas a la wave `"1"`.

## Resultados de las Pruebas E2E

- Confirmada la subida correcta de estrategias optimizadas bajo el prefijo `wave_1/ndx/l_h1/example_flow/v5/03_optimizer/` en MinIO.
- Confirmado el registro de estrategias optimizadas en Postgres (alcanzando 300 estrategias en la carpeta `03_optimizer`).
- Confirmado el incremento continuo de registros en `wfm_runs` y `wfm_matrices` en la base de datos `forge` en MongoDB (llegando a 102 registros para wave 1).
