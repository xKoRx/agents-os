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
# Change Log - 2026-06-28 - WFM Deserialization Fix

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - [steps.go](file:///Users/rjara/go/src/github.com/xKoRx/symphony/sqx/activities/worker/steps/steps.go)
  - [manifest.json](file:///Users/rjara/go/src/github.com/xKoRx/symphony/deploy/manifest.json)

## Motivo

- Resolver el fallo en la tarea `import_metadata_activity` debido a discrepancias de tipo en el JSON de salida generado por el plugin de Java de SQX (strings en lugar de float64 en el campo de estabilidad de celdas).

## Fuentes usadas

- Traza de error de deserialización de `/var/log/symphony/symphony-worker.log`.

## Resolución aplicada

1. Cambiamos el tipo de `Stability` en `javaWFMCell` a `map[string]any`.
2. Implementamos `parseStabilityVal` y `parseBoolVal` como parseadores seguros y tolerantes a tipos dinámicos.
3. Actualizamos las asignaciones en el mapeo de celdas y del centro del vecindario para usar los parseadores seguros.
4. Bumpeamos la release a `0.1.29` y desplegamos el binario.

## Validación

- Ejecución exitosa de la Wave 14, importando 2 matrices de WFM de optimización en MongoDB sin errores de tipos.
