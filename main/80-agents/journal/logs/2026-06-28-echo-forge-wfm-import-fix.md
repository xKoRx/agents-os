---
type: change_log
scope: session
created: "2026-06-28"
updated: "2026-06-28"
area: "[[Personal]]"
project: "[[Symphony]]"
application: "[[Echo Forge]]"
entities:
  - "[[Symphony]]"
  - "[[Echo Forge]]"
related: []
aliases: []
confidence: verified
source_session: "8e111370-744b-4d70-8c21-e2ed84e0d2d9"
load_policy: manual
indexable: false
index_priority: never
tags:
  - app/echo-forge
  - app/echoforge
  - area/personal
  - kind/changelog
  - project/symphony
  - scope/session
---
# Change Log - 2026-06-28 - WFM Metadata Import Fix

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - [WFMOptimizerJsonExporter.java](file:///Users/rjara/go/src/github.com/xKoRx/symphony/sqx/exporter-plugin/src/SQ/CustomAnalysis/WFMOptimizerJsonExporter.java)
  - [steps.go](file:///Users/rjara/go/src/github.com/xKoRx/symphony/sqx/activities/worker/steps/steps.go)
  - [manifest.json](file:///Users/rjara/go/src/github.com/xKoRx/symphony/deploy/manifest.json)

## Motivo

- Corregir el fallo en el pipeline de importación de metadatos de robustez Walk-Forward (`metadata_import` / `03_wfm_optimizer`) que causaba la falta de archivos `export_run.json` y caídas por desreferenciación nula en el worker.

## Fuentes usadas

- Traza de logs de `/var/log/symphony/symphony-worker.log` y de `/home/kor/sqx/user/projects/03_wfm_optimizer/log/` en Zeus.

## Resolución aplicada

1. Cambiamos la ubicación del plugin a snippets compilables de SQX en Zeus (`user/extend/Snippets/SQ/CustomAnalysis/WFMOptimizerJsonExporter.java`) y limpiamos el `.jar` obsoleto.
2. Sincronizamos el nombre del plugin registrado en el constructor Java a `"WFMOptimizerJsonExporter"` para alinearlo con el CFX.
3. Agregamos una verificación defensiva contra celdas vacías (`wfm_cells` vacía / `centerCell` nulo) en el deserializador de Go para prevenir panics de puntero nulo.

## Validación

- Ejecución de Wave 13 de prueba con éxito completo, importando las matrices y corridas a MongoDB sin panics de telemetría ni errores de archivos faltantes.
