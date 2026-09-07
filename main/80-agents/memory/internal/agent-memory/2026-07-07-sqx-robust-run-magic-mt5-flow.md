---
type: agent_memory
scope: internal
created: 2026-07-07
updated: 2026-07-07
tags:
  - kind/agent_memory
  - tech/go
  - app/symphony
  - topic/workflow
  - topic/mt5
---

# Continuidad Operativa: Flujo Robust Run y Configuración de Magic Number en SQX/MT5

## Qué se hizo
- Respondimos a la consulta del usuario sobre cómo orquestar el flujo post-WFM en `symphony` para:
  1. Setear el run robusto en SQX.
  2. Exportar la estrategia a SQX.
  3. Setear un `magic_number`.
  4. Exportar la versión MT5 (`.mq5` / `.ex5`) con ese `magic_number`.

## Mapeo técnico en la Codebase
- **evaluate_wfm**: Ejecuta `EvaluateWFMActivity` que guarda celdas y corridas en Mongo.
- **select_robust_run**: Ejecuta la selección determinista del mejor run y genera `selected_robust_run` en Mongo ([robust_activity.go:L48-296](file:///Users/rjara/go/src/github.com/xKoRx/symphony/sqx/activities/worker/robust_activity.go#L48-L296)).
- **apply_selected_run**: Copia y sube el archivo `.sqx` robusto local (`output/robust/{strategy_id}_robust.sqx`) a MinIO ([robust_activity.go:L318-547](file:///Users/rjara/go/src/github.com/xKoRx/symphony/sqx/activities/worker/robust_activity.go#L318-L547)).
- **magic_number y mt5 export**:
  - `sqcli` nativo no soporta parámetros por línea de comandos para cambiar inputs como el `MagicNumber` o el run robusto al vuelo (solo inicia proyectos `.cfx` pre-configurados).
  - Para hacerlo de forma robusta y escalable (descartando hacks sobre el XML del `.cfx`), el camino es:
    1. **Custom Analysis Java Plugin (Opción principal)**: Un plugin Java que corra dentro de SQX al iniciar el proyecto. Vía la API de StrategyQuant (`ResultsGroup`, `Strategy`), el plugin aplica el parche de parámetros, setea el magic number y gatilla la exportación del EA `.mq5` programáticamente.
    2. **Otros mecanismos nativos de sqcli**: Investigar si existen formas nativas de pasar propiedades externas (ej. `.properties` o archivos de configuración de tareas) que `sqcli` acepte para sobreescribir inputs al exportar.
  - El spike para automatizar esto (`NI-RR-1` y `NI-JP-1`) sigue como **WIP/Pendiente** en el backlog (`agentes/Echo Forge - Etapa 4.md`).
  - **Brechas a investigar en Fase 2**:
    1. Compilación del plugin en entornos headless/CLI (¿cómo compilar snippets sin interfaz gráfica, o qué JARs de dependencia usar para compilar externamente en un pipeline?).
    2. Configuración exacta en la GUI del Custom Project para encadenar la tarea de Custom Analysis.
    3. Validación del bug de `ParametersSettings` en la Build 142 y cómo detectar `symmetricVariables` de forma segura.
    4. Confirmar si `StrategyParametersHelper` viene integrado en la Build 142 o si hay que importar obligatoriamente el helper V2 manual en `SQ/Utils`.
  - La compilación desatendida a `.ex5` la realiza la actividad `mt5_compile` en el Windows Worker (`sqx-mt5-worker`) usando `MetaEditor64.exe` ([mt5_activities.go:L40-65](file:///Users/rjara/go/src/github.com/xKoRx/symphony/sqx/activities/worker/mt5_activities.go#L40-L65)).
