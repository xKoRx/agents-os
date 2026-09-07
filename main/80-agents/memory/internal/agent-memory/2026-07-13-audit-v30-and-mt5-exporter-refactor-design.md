---
type: agent_memory
scope: internal
created: 2026-07-13
updated: 2026-07-13
tags:
  - kind/agent_memory
  - tech/go
  - tech/mongodb
  - app/symphony
  - topic/wfm
  - topic/refactor
---

# Continuidad Operativa: Triage de Wave v30 y Diseño de Desacoplamiento del MT5 Exporter

## 🔍 Resultados de la Investigación (Wave v30)
1. **Lote original de 5 estrategias:**
   - 3 pasaron con estado `WARN` ( stability warnings) y seleccionaron run robusto / configuraron setup:
     - `Strategy_3.1.16.z0`
     - `Strategy_3.1.24.z0`
     - `Strategy_5.1.20.z0`
   - 2 fallaron en la etapa `evaluate_wfm`:
     - `Strategy_5.1.21.z0`
     - `Strategy_5.1.23.z0`
2. **Causa de descarte en BD:**
   - Ambas estrategias descartadas tienen el campo `cells` en `wfm_matrices` y el campo `runs` en `wfm_runs` como `NIL` (vacío).
   - Al no tener celdas ni corridas de optimización WFM registradas en MongoDB, la función de evaluación de vecindario `EvaluateNeighborhood` de WFM retorna `domain.ErrInvalidGridSize` porque la grilla resultante es menor a 3x3.
   - `EvaluateWFMActivity` procesa el error y setea `verdict = FAIL` en `wfm_evaluations`, lo cual es correctamente interpretado por `SelectRobustRunActivity.Execute` para omitir la selección de run robusto. El descarte es totalmente legítimo.

## 📐 Diseño de Refactorización de MT5 Exporter
1. **Acoplamiento actual:**
   - En `ApplySelectedRunActivity.Execute` (dentro de `robust_activity.go`), la ejecución de `EchoForgeMT5Exporter` y la subida del `.mq5` a MinIO bajo la ruta dura `"ea_export"` están acopladas de manera incondicional.
2. **Desacoplamiento propuesto:**
   - Crear una nueva actividad Temporal `ExportMT5EAActivity` en `robust_activity.go` con los contratos `ExportMT5EARequest` y `ExportMT5EAResult`.
   - Modificar `ApplySelectedRunRequest` agregando `SkipMT5Export bool`. Si es `true`, `ApplySelectedRunActivity` salta la compilación/exportación inline legacy de MT5.
   - En `generic_workflow.go` (flujos normales y de grupo), mapear el nuevo tipo de tarea `"mt5_exporter"`. Si está presente en la spec, activar `SkipMT5Export = true` en la tarea anterior de selección/aplicación y disparar secuencialmente la nueva actividad para cada estrategia del lote.
   - Registrar la actividad en `main.go` y su mock en `sqx_e2e_json_test.go`.
3. **Configuración JSON (ej: v30):**
   ```json
   {
     "type": "mt5_exporter",
     "source_folder": "04_optimizer_robust",
     "folder": "mt5_eas"
   }
   ```
