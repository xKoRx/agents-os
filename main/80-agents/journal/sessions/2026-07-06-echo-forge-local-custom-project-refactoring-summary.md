---
type: session
scope: session
created: "2026-07-06"
updated: "2026-07-06"
area: 80-agents
project: symphony-sqx
application: symphony
entities:
  - "[[symphony]]"
related:
  - "[[2026-07-06-echo-forge-sequential-logical-type-chunking-summary]]"
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

# 2026-07-06 — Local Custom Project Refactoring — Summary

> [!info]+ Session summary L1
> Resumen operativo. Para beta queda fuera del corpus normal de Graphify.

## Objetivo

- Implementar la unificación de la carpeta física/proyecto local a `"custom"` para todas las actividades del worker (retester, optimizer, etc.), manteniendo la independencia organizativa y aislamiento en MinIO.
- Resolver el conflicto de no-determinismo y error de replay en Temporal provocado por la ordenación aleatoria de iteración de mapas en Go.

## Contexto cargado

- "symphony/sqx" (monorepo).
- "deployer-watcher" local y stager en Zeus.

## Trabajo realizado

- **Determinación del Proyecto Local**: Modificamos `ResolveLocalProjectName` en `sqx/core/runtime/config.go` para que devuelva siempre `"custom"`, salvo para la exportación de métricas `SQXOverviewJsonExporter`.
- **Modificación en steps.go**: Se actualizó `getProjectName` para llamar al resolvedor centralizado `runtime.ResolveLocalProjectName(st.Task.Folder)`.
- **Corrección de Determinismo en Temporal**: Corregimos el bucle de child workflows en `handleGroupTask` (`sqx/workflows/generic_workflow.go`), ordenando alfabéticamente las claves del mapa `loadResp.LogicalTypes` con `sort.Strings()` antes de iterar, evitando los pánicos `[TMPRL1100]` por replay inconsistente.
- **Limpieza de Colas en Temporal**: Terminamos las ejecuciones huérfanas/en bucle de error de replay del run anterior usando una secuencia Go personalizada que invoca a la API de Temporal en Zeus.
- **Despliegue E2E v0.1.50**: Compilamos y desplegamos la versión `0.1.50` vía `deploy_sqx.sh` y actualizamos el manifiesto. Limpiamos las tablas en MongoDB con `vacuum_db.go` y relanzamos el flujo de ejemplo desde cero.
- **Validación del Run**: El pipeline completo de ejemplo se ejecutó exitosamente: se importaron metadatos (`74 docs`), se generaron rankings (`27 docs`), y se guardaron los export runs completados exitosamente.
- **Documentación Actualizada**: Actualizamos `sqx/README.md` detallando la regla arquitectónica de que el worker procesa una tarea local a la vez usando el proyecto `"custom"` (evitando la polución de carpetas locales en disco), sin comprometer la estructura de almacenamiento organizada en MinIO.

## Artifacts creados o modificados

- Modificados:
  - [config.go](file:///Users/rjara/go/src/github.com/xKoRx/symphony/sqx/core/runtime/config.go)
  - [steps.go](file:///Users/rjara/go/src/github.com/xKoRx/symphony/sqx/activities/worker/steps/steps.go)
  - [generic_workflow.go](file:///Users/rjara/go/src/github.com/xKoRx/symphony/sqx/workflows/generic_workflow.go)
  - [README.md](file:///Users/rjara/go/src/github.com/xKoRx/symphony/sqx/README.md)
  - [manifest.json](file:///Users/rjara/go/src/github.com/xKoRx/symphony/deploy/manifest.json)

## Memoria propuesta o creada

- Ninguna de nivel L3 requerida; los cambios se basan en los patrones ya descritos y formalizados en la documentación técnica del proyecto.

## Decisiones

- **Unificación local a "custom"**: No se duplican nombres de agrupación en la estructura de directorios del worker físico. La base lógica de datos de la máquina es única.
- **Determinismo estricto**: Se fuerza la ordenación de cualquier mapa antes de la generación dinámica de `workflow.Go` o child workflows en Temporal.

## Pendiente

- Ninguno. El flujo se ejecuta ok y limpia/inserta correctamente.
