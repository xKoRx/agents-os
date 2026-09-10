---
type: agent_memory
scope: project
created: 2026-07-13
updated: 2026-09-09
index_priority: never
indexable: false
load_policy: manual
memory_state: archived
tags:
  - tech/go
  - project/symphony
  - task/generate-report-custom-folder
---

# Continuidad: Parametrización de Carpeta en Generate Report

Se implementó el soporte para carpetas personalizadas en la actividad `generate_report` de la siguiente manera:
1. Agregado el campo `Folder` y los campos de ruta jerárquica (`Instrument`, `Direction`, `Timeframe`, `Strategy`, `Version`) a `GenerateReportRequest` en `sqx/activities/worker/generate_report.go`.
2. Modificado el método `Execute` de la actividad para que si `req.Folder` no está vacío, se use este valor como la carpeta destino en MinIO (y en `x-sqx-task-folder`), cayendo de lo contrario al valor por defecto `"reports"`. Se actualizó la llamada a `domain.BuildMinIOPath` para pasar todas las variables de ruta y así respetar la estructura jerárquica habitual de EchoForge (`wave_<wave_key>/<instrument>/<direction_timeframe>/<strategy>/<version>/<request_id>/[folder]/[filename]`).
3. Mapeados todos los campos de ruta desde `req.Spec` y `task.Folder` en el caso `generate_report` de `sqx/workflows/generic_workflow.go`.

Las pruebas y la compilación pasaron correctamente. Se realizó el deploy exitoso de la versión `0.1.119` a Zeus.
