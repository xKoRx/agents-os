---
type: change_log
scope: change
created: 2026-07-11
updated: 2026-07-11
area: "[[Symphony]]"
project: "[[EchoForge]]"
application: "[[Symphony]]"
entities:
  - "[[EchoForge]]"
  - "[[Symphony]]"
related: []
aliases: []
confidence: high
source_session: "19122e0a-c18e-4878-b20d-1754f25b7755"
load_policy: manual
indexable: false
index_priority: never
tags:
  - app/symphony
  - area/symphony
  - kind/changelog
  - project/ echoforge
  - scope/change
---

# Echo Forge Pipeline Stabilization Change Log

## Cambios Realizados

- **`steps.go`**:
  - Modificado `postProcessCFX` para escanear y reemplazar de forma dinámica nombres de clases obsoletos en los XML internos de los archivos `.cfx` del proyecto (`WFMOptimizerJsonExporter` -> `EchoForgeWFMExporter` y `SQXOverviewJsonExporter` -> `EchoForgeOverviewExporter`).

- **`manifest.json`**:
  - Bump de versión a `0.1.86`.

- **`count_v15_minio.go` (Scratch)**:
  - Creado script para contar y auditar los archivos cargados bajo la versión `v15` en MinIO.

## Resultados de las Pruebas E2E

- Confirmada la ejecución y finalización de las 7 tareas secuenciales del workflow `v15`.
- PostgreSQL: Registradas 78 builder, 22 retester y 22 optimizer, con 0 duplicaciones de metadatos.
- MinIO: Cargadas 100 builder, 22 retester, 22 optimizer y 0 estrategias en `metadata/`.
- MongoDB: 127 evaluaciones WFM registradas correctamente bajo `wave_key = 15`.
