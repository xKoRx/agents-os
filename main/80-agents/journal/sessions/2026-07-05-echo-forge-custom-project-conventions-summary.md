---
type: session
scope: session
created: "2026-07-05"
updated: "2026-07-05"
area: "[[Symphony]]"
project: "[[Echo Forge]]"
application: "[[sqx-worker]]"
entities:
  - "[[Echo Forge]]"
related: []
aliases: []
confidence: high
source_session: "241add91-8048-41f7-b2cd-87470b589ef0"
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/session
  - scope/session
---

# Echo Forge: Unificación de Carpeta Custom en Flujos y Subflujos

> [!info]+ Session summary L1
> Resumen operativo de la normalización del nombre de proyecto en StrategyQuant a "custom" para tareas y subtareas en Zeus.

## Objetivo

- Configurar el flujo de SQX (`input/example/config.json`) para procesar en paralelo grupos de a 1 subflujo, deteniendo la ejecución al retestear exitosamente 2 estrategias.
- Configurar y asegurar que tanto los flujos principales como los subflujos en paralelo se ejecuten exclusivamente bajo la carpeta del proyecto `custom` en el worker (Zeus).
- Limpiar por completo las colecciones de MongoDB (`databank_metadata`, `type_rankings`, `export_runs`) antes del inicio del flujo para verificar la correcta inserción de metadatos y rankings.
- Actualizar la documentación del repositorio para que la convención del proyecto `custom` sea respetada por futuros agentes y operadores.

## Contexto cargado

- Instrucciones de `AGENTS.md` (Symphony Portal).
- Reglas de stack en `.agents/rules/01-stack-and-tooling.md`.
- Habilidades y procedimientos de pruebas de `.agents/skills/echo-forge-testing/SKILL.md`.
- Logs del worker de Zeus vía SSH.

## Trabajo realizado

- **Limpieza de base de datos**: Se creó y ejecutó un script temporal (`clear_mongo.go`) para vaciar las colecciones `databank_metadata`, `type_rankings` y `export_runs` en la base de datos `forge` en MongoDB.
- **Configuración del flujo**: Se modificó `input/example/config.json` para:
  - Definir la carpeta del proyecto como `"folder": "custom"` en todas las tareas del workflow principal y subtareas del `group`.
  - Configurar `"batch_size": 1` y `"top_n_per_logical_type": 2` para estructurar la parada temprana con 2 estrategias válidas procesadas de una en una.
  - Asociar el archivo de configuración retester correcto `"config": "retester_test.cfx"`.
- **Ejecución y Verificación**:
  - Se copiaron los archivos `.cfx` y la configuración `.json` al directorio `input/`, gatillando la detección automática del watcher.
  - Se monitorizó en tiempo real la ejecución de los subflujos paralelos por tipo lógico en Zeus (usando `sqcli` en el proyecto `custom`).
  - El flujo terminó 100% exitosamente sin errores ni fallos.
  - Se comprobó mediante `show_mongo.go` que se rellenaron correctamente las colecciones con 44 documentos de metadatos, 15 de rankings por tipo lógico y 1 ejecución del exportador.
- **Actualización de Documentación**:
  - Se modificó `sqx/README.md` detallando la regla obligatoria de usar `"folder": "custom"` para evitar la creación de carpetas basadas en agrupaciones/tipos lógicos y para que sea seguro en ejecuciones paralelas en workers independientes.
  - Se añadió la lección en la sección de automejora de `.agents/skills/echo-forge-testing/SKILL.md`.

## Artifacts creados o modificados

- [SKILL.md](file:///Users/rjara/go/src/github.com/xKoRx/symphony/.agents/skills/echo-forge-testing/SKILL.md) (modificado)
- [README.md](file:///Users/rjara/go/src/github.com/xKoRx/symphony/sqx/README.md) (modificado)
- [config.json](file:///Users/rjara/go/src/github.com/xKoRx/symphony/input/example/config.json) (modificado)

## Memoria propuesta o creada

- Regla explícita de proyectos de ejecución StrategyQuant en Zeus: usar siempre `custom` como nombre de carpeta para prevenir la polución de directorios.

## Decisiones

- Mantener la carpeta del exportador en `SQXOverviewJsonExporter` dado que no requiere configuración dinámica descargada y es de carácter fijo en Zeus.

## Pendiente

- Ninguno. El objetivo principal de la sesión fue completamente resuelto y verificado con logs reales de Zeus y MongoDB.
