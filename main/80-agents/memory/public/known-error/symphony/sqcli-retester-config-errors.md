---
type: known_error
scope: application
created: "2026-06-27"
updated: "2026-06-27"
area: "[[Echo]]"
project: "[[Echo Forge]]"
application: "[[echo-forge]]"
entities: []
related: []
aliases:
  - Error de configuración del retester en sqcli
  - Retester config errors SQX
confidence: high
source_session: "8c11ec26-7ad2-4f0d-a862-0c85ceebe285"
load_policy: when_error_matches
indexable: true
index_priority: high
tags:
  - app/echo-forge
  - app/echoforge
  - area/echo
  - kind/known-error
  - project/echo-forge
  - project/echoforge
  - scope/application
  - tool/strategyquant
---
# StrategyQuant CLI Retester Config Errors

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Síntoma

- Al iniciar la tarea del Retester (`02_retester_full` o similar) a través de `sqcli`, el comando falla con código de salida `1` o finaliza prematuramente reportando errores de configuración en los logs internos:
  `Cannot start project '02_retester_full', it has config errors in task 'Retest strategies'.`
  `Error: You have to set up at least one backtest!, in setting: Data`
  `Error: Cannot load fitness function. FitnessCriteria - No Settings found for method 'ComputeFromStrategyResult' in field: FitnessFunction, in setting: Rankings`

## Causa

- **Falta de Backtest (Data):** El archivo `.cfx` (su XML interno de la tarea de retest) tiene el bloque `<Data>` incompleto, vacío o haciendo referencia a un símbolo, broker o timeframe que no existe en el workspace del usuario o base de datos local de la instalación física de StrategyQuant.
- **Error en Fitness Function (Rankings):** El bloque `<Rankings>` o `<FitnessCriteria>` en el XML de la tarea del archivo `.cfx` intenta cargar una función de aptitud (`ReturnDDRatio`, `ComputeFromStrategyResult`, etc.) que no está completamente configurada o cuyos parámetros (`Settings`) no fueron serializados o mapeados de forma correcta en el XML de plantilla.

## Impacto

- El proceso `retest` o `optimize` falla inmediatamente en StrategyQuant, finalizando la actividad con éxito ficticio en la CLI (exit code 0 o 1 pero sin generar resultados) y dejando el databank de salida vacío. Como consecuencia, las siguientes actividades (como `evaluate_wfm`) fallan o procesan 0 registros, resultando en `wfm_runs` y `wfm_matrices` con 0 documentos en MongoDB.

## Detección

- Revisar los logs internos de la ejecución de `sqcli` en el worker buscando cadenas como:
  * `has config errors in task`
  * `You have to set up at least one backtest!`
  * `No Settings found for method`

## Mitigación

1. **Revisar y corregir el XML de la tarea:** Verificar que el bloque `<Data>` y `<Rankings>` de la tarea (ej: `Retest-Task1.xml`) esté completo y use métodos e indicadores válidos.
2. **Uso de un proyecto base válido de la UI:** La manera más robusta de mitigar esto es abrir StrategyQuant en modo gráfico en el entorno de desarrollo, crear un proyecto vacío, configurar la tarea de Retest y el backtest apuntando a un símbolo real existente en los Databanks (ej: `XAUUSD` H1), exportar ese `.cfx` y usarlo como plantilla para envolver el XML dinámico del pipeline.
3. La sesión fuente usó un script efímero `fix_cfx_final.py` para inyectar bloques quirúrgicamente (como cambiar `ReturnDDRatio` por `NetProfit` o inyectar el bloque de `<Resources>` extraído de un proyecto funcional); el artefacto no es una dependencia durable ni portable.

## Evidencia

- Evidencia efímera de la sesión fuente: `check_workflows_status.go`, `get_history.go` y `fix_cfx_final.py`; no se conservan como locators canónicos.
