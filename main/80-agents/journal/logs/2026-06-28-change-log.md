---
type: change_log
scope: session
created: "2026-06-28"
updated: "2026-06-28"
area: "[[Symphony Portal]]"
project: "[[Symphony]]"
application: "[[StrategyQuant X]]"
entities:
  - "[[Symphony]]"
  - "[[StrategyQuant X]]"
related: []
aliases: []
confidence: verified
source_session: "4af42ce7-35ef-4f46-9445-a0a05872312a"
load_policy: manual
indexable: false
index_priority: never
tags:
  - app/strategyquant-x
  - app/strategyquantx
  - area/symphony-portal
  - area/symphonyportal
  - kind/changelog
  - project/symphony
  - scope/session
---
# Change Log - 2026-06-28 - Echo Forge Retester Troubleshooting

## Cambio

- **Tipo:** updated / conflict-resolution
- **Archivo(s):**
  - `deploy/manifest.json` (actualizado a versión `0.1.25`)
  - `sqx/activities/worker/steps/steps.go` (revertido en versión previa para eliminar sufijos)
  - `sqx/activities/worker/pipeline/step.go` (revertido en versión previa)
  - `sqx/activities/worker/pipeline/hooks/cleanup_databanks.go` (revertido en versión previa)

## Motivo

- Corregir fallo de paralelismo y la regresión introducida en los nombres de proyectos al pasarlos a `sqcli`, asegurando que el worker use nombres de proyectos físicos estáticos.
- Corregir el error de carga de proyectos de StrategyQuant X causados por la sobreescritura de `project.cfx` con configuraciones de tareas planas.

## Fuentes usadas

- Guías internas de [[Symphony]]
- Logs de ejecución del servicio `symphony-worker.service` en Zeus.

## Resolución aplicada

- Despliegue de la versión `0.1.25` con reversión completa del sufijo dinámico de proyectos.
- Creación del script `fix_new_workflow_wrapped.py` para re-empaquetar las plantillas `.cfx` del Retester y Optimizador como proyectos completos válidos con sus respectivos bloques de `<Project>`, `<Tasks>` y `<Resources>`.

## Validación

- Se verificó que el worker Zeus levantó con éxito la versión `0.1.25`.
- Se verificó que el watcher procesó y movió los archivos empaquetados como proyectos, y que la tarea de Retest en Temporal avanzó sin lanzar errores de "Project does not exist".
