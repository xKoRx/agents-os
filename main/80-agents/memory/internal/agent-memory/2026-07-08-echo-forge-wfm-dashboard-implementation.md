---
type: agent_memory
scope: internal
created: 2026-07-08
updated: 2026-09-09
index_priority: never
indexable: false
load_policy: manual
memory_state: archived
tags:
  - kind/agent_memory
  - tech/go
  - app/symphony
  - topic/wfm
  - topic/dashboard
---

# Memoria Interna: Implementación de Echo Forge WFM Dashboard y CLI de Descarga

## Decisiones Técnicas Adoptadas:
1. **Aislamiento en generate_report**: La actividad `GenerateReportActivity` utiliza el `run_id` (Trace ID de OpenTelemetry) obtenido directamente del contexto de ejecución. Esto garantiza que las notas de reporte generadas correspondan estrictamente al lote activo actual de la wave evaluada.
2. **Consultas a MongoDB**: 
   - Se consulta `wfm_evaluations` por `wave_key` y `run_id`.
   - Para cada evaluación, se cargan la matriz de Walk-Forward correspondientes desde `wfm_matrices` y la decisión de robustez desde `selected_robust_runs` aplicando fallbacks sin `run_id` en caso de que existan discrepancias temporales de registro.
3. **MinIO Uploader**: Se utiliza la ruta `wave_<wave_key>/reports/wave_<wave_key>_strategy_<strategy_id>.md` en el bucket de estrategias por defecto `minio.BucketStrategies` para alojar los Markdowns del dashboard.
4. **Copia Rápida en Obsidian**: El script DataviewJS interactivo del panel en Obsidian no solo renderiza la matriz 3x3 en HTML/CSS, sino que inyecta un bloque de comando en el que, al hacer clic, se copia automáticamente el comando `symphony download-wave` listo para ejecutarse en terminal.
5. **Comando de Descarga**: El comando `download-wave` filtra todos los archivos en MinIO bajo `wave_<wave_key>/` que pertenezcan a las carpetas `reports`, `optimizer` o `robust` y descarga secuencialmente los archivos `.sqx` y `.md` al path de destino proporcionado.
