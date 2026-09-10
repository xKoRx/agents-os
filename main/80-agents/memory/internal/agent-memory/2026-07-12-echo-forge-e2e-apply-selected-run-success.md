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

# Continuidad — Echo Forge E2E Apply Selected Run Success (2026-07-12)

- **Estado actual**: Se ha completado con éxito la ejecución del pipeline E2E completo (`v15`) tras corregir el bug de multitenancy de MongoDB (BYPASS_RUN_ID) y la resolución de la clave de descarga/subida de estrategias en `apply_selected_run` utilizando el prefijo lógico del ID de estrategia.
- **Logros clave**:
  1. **BYPASS_RUN_ID**: Configurado `BYPASS_RUN_ID=true` en el script de arranque del worker en Zeus (`0.1.92`+) para evitar la filtración por `run_id` en las consultas de metadatos de MongoDB, solucionando el problema de desalineación de spans de OTel de Temporal.
  2. **Resolución de Descarga Lógica**: Se implementó una lógica robusta en `robust_activity.go` (versión `0.1.93`+) para extraer el instrumento, timeframe y dirección analizando el prefijo del `StrategyID` en lugar de confiar ciegamente en `targetMeta` (que contiene datos internos del backtest XML, ej. `EURUSD` en lugar del par del flujo `NDX`). Los fallbacks dinámicos resuelven nombres con/sin prefijo y carpetas de dirección largas (`long_h1`) y cortas (`l_h1`).
  3. **Alineación de Rutas de Subida**: Modificadas las claves de subida en `robust_activity.go` (versión `0.1.94`+) para almacenar los `.sqx` robustos resultantes y archivos `.mq5` bajo el prefijo del par del flujo (`wave_1/ndx/l_h1/example_flow/v15/04_optimizer_robust/`) en lugar del par del XML.
  4. **Ejecución y Verificación E2E exitosa**: El workflow `sqx-main-00_configs-v15-NDX-H1-L-1783864373` completó todas sus actividades sin errores. El directorio `04_optimizer_robust/` contiene ahora las 17 estrategias robustecidas correctas, y `ea_export/` contiene los archivos `.mq5` generados.
  5. **Concurrencia del Worker**: Se verificó que el SDK establece `MaxConcurrentActivityExecutionSize: 1`, por lo que las ejecuciones de `apply_selected_run` ocurren de forma estrictamente secuencial, evitando conflictos en la carpeta del proyecto de exportación.
