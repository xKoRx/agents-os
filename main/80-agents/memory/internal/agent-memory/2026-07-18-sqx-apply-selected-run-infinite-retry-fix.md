---
type: agent_memory
scope: project
created: 2026-07-18
updated: 2026-09-09
index_priority: never
indexable: false
load_policy: manual
memory_state: archived
tags:
  - tech/temporal
  - tech/go
  - project/symphony
  - bug/infinite-retry
---

# Memoria Interna: Corrección de Reintentos Infinitos en apply_selected_run (Actualizado)

## Fix Aplicado

Se implementó el comportamiento definitivo para el filtrado e intersección de estrategias en la tarea `apply_selected_run` utilizando la nueva actividad `list_selected_strategies`:

1. **Lógica de la Actividad (`list_selected_strategies`)**:
   - Carga de MongoDB todas las decisiones de selección robusta para la wave provista.
   - **Intersección (Batch con datos)**: Si el batch de entrada (`req.Input.Keys`) no está vacío, se filtran las estrategias recibidas y se retorna únicamente el subconjunto de ellas que posea un robust run seleccionado.
   - **Fallback (Batch vacío)**: Si el batch está vacío, retorna todas las estrategias de la wave que tengan un robust run seleccionado en MongoDB.
   - Mapea las estrategias resultantes al formato `<StrategyID>.sqx` para compatibilidad.

2. **Modificación del Workflow (`sqx/workflows/generic_workflow.go`)**:
   - En `case "apply_selected_run"` secuencial y grupal (`GroupSQXWorkflow`), se invoca **siempre** la actividad `list_selected_strategies` enviando el batch actual en `listReq.Input`.

3. **Registro y Validación**:
   - Registrada en `sqx/cmd/sqx-worker/main.go`.
   - Mock de pruebas e2e registrado en `sqx/workflows/sqx_e2e_json_test.go`.
   - Test unitario de intersección agregado en `sqx/activities/worker/list_selected_strategies_test.go` (`TestListSelectedStrategiesActivity_Execute_FilteringSuccess`).
   - Compilación exitosa y todas las pruebas unitarias y e2e pasando al 100%.

## Verificación E2E en Zeus (2026-07-18)

Se realizó el despliegue de la versión `0.1.120` en el host Zeus (`worker.zeus.lab.aranea`) y se validó el comportamiento esperado en dos escenarios de Temporal:

1. **Intersección (Batch con datos)**: 
   - Ejecutado con `scratch/test_apply_intersection.go`.
   - Se enviaron claves de estrategia inexistentes.
   - El worker filtró las claves en `list_selected_strategies` retornando `0` estrategias válidas e interrumpió la llamada a `apply_selected_run` sin tirar error.
   - El workflow finalizó con éxito.

2. **Fallback (Batch vacío)**:
   - Ejecutado con `scratch/test_apply_fallback.go`.
   - Se envió una lista de claves vacía.
   - La actividad consultó MongoDB buscando robust runs para la wave 1.
   - Retornó `0` estrategias (sin robust runs asociados en el entorno actual) y completó el workflow con éxito omitiendo la aplicación física.

## Análisis de Incidentes de Ejecución en Zeus (2026-07-19)

Se analizaron dos incidentes específicos consultando los logs del journal de Zeus:

1. **Workflow `v45` (`sqx-main-00_configs-v45-NDX-H1-L-1784429024`)**:
   - **Problema**: Saltó la tarea `apply_selected_run` sin procesar ninguna estrategia.
   - **Causa**: La actividad `list_strats` obtuvo 0 archivos `.sqx` en la carpeta `04_optimizer_robust/` en MinIO. Al estar el batch de entrada vacío, `list_selected_strategies` realizó fallback contra MongoDB para la wave 1, retornando 0 robust runs seleccionados. El workflow ejecutó un `continue` y omitió de forma exitosa el procesamiento físico para no quedar en bucle.

2. **Workflow `v44` (`sqx-main-00_configs-v44-NDX-H1-L-1784429001`)**:
   - **Problema**: Falló inmediatamente la tarea `classify_and_rank` sin reintentar.
   - **Causa**: La actividad no cargó metadatos de MongoDB para la wave 1 (0 estrategias). Al ver esto, la actividad lanzó un error de aplicación `ErrMetadataMissing` configurado con `NonRetryable: true` en el SDK de Temporal. Al ser marcado como no reintentable, Temporal falló la ejecución del workflow de inmediato sin backoff.

3. **Diagnóstico del Exportador en Zeus (mismatch de celdas en `v42`)**:
   - **Problema**: `apply_selected_run` falló con la excepción en Java de SQX: `No WalkForwardResult exists for 20 / 14`.
   - **Causa**: El exportador en Java intentó aplicar la celda `runs=14, oos=20` (leída desde MongoDB) sobre el archivo físico `.sqx` descargado de MinIO (`03_optimizer`). El ZIP físico descargado de MinIO tenía 3.2 MB pero solo contenía carpetas de Results de `5` a `10` runs.
   - **Explicación**: El misterio se resolvió al inspeccionar el archivo `wfm_matrices.ndjson` en MinIO, el cual reportaba `NO_WFM_OBJECT` ("WalkForwardMatrixResult no encontrado en mainResult") porque la estrategia era un **Portfolio** (el ZIP tenía `strategy_Portfolio.xml` en lugar de `strategy.xml`), lo que hizo que la exportación de la matriz fallara en esta corrida.
   - **Origen del mismatch**: Como la exportación de la matriz falló, la base de datos de MongoDB de Zeus no recibió ninguna actualización de matriz para esta estrategia. Sin embargo, en MongoDB ya existía un registro viejo con el mismo `strategy_id` (generado deterministamente por SQX en pruebas pasadas) que tenía runs `9` a `14` (de cuando la wave usaba la configuración vieja de `ATR, SMA...`). La actividad `select_robust_run` cargó este registro huérfano viejo de la base de datos (mismo `strategy_id` y `wave_key`), seleccionó `14 / 20`, e intentó aplicarlo en el archivo físico nuevo de `5` a `10` runs, provocando la excepción.

4. **Análisis de Fallas en `v47`/`v48` (`classify_and_rank` falla sin reintentar - 2026-07-19)**:
   - **Problema**: El workflow `v47` y `v48` (`sqx-main-00_configs-v48-NDX-H1-L-1784472370`) falló inmediatamente en `classify_and_rank` con `ErrMetadataMissing` sin reintentar.
   - **Causa Raíz**: La base de datos de MongoDB en Zeus (`192.168.31.221:27017`) está caída / inalcanzable (`connection refused`). 
   - **Mecanismo**: Durante la ejecución de la tarea `metadata` (`overview_exporter`), el paso `import_metadata` falló al conectarse a MongoDB. Sin embargo, la actividad `"project"` tiene implementado un **graceful fallback** (retorna warning pero completa con éxito). Al continuar el workflow, la actividad `classify_and_rank` intentó leer los datos de MongoDB para la wave. Al estar la base de datos vacía / inaccesible, retornó 0 estrategias y levantó el error `ErrMetadataMissing` marcado como `NonRetryable: true` en Temporal, abortando la ejecución de inmediato.
