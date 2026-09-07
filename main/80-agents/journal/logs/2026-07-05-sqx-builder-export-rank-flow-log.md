---
type: change_log
scope: user
created: 2026-07-05
updated: 2026-07-05
area: "[[Symphony]]"
project: "[[Echo Forge]]"
entities:
  - "[[Echo Forge]]"
related: []
aliases: []
confidence: verified
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/user
  - project/echo-forge
---

# 2026-07-05 — Configuración de ejemplo de flujo SQX en input

## Cambio

- **Tipo:** created
- **Archivo(s):**
  - `/Users/rjara/go/src/github.com/xKoRx/symphony/input/example/config.json`

## Motivo

Petición del usuario de configurar un flujo de SQX para procesar en el worker que contenga las 3 tareas de Builder, Export y Rankeo, y dejar un ejemplo en la carpeta `input/example`.

- Se creó el directorio `input/example` si no existía.
- Se escribió el archivo `config.json` con la especificación completa del flujo SQX de 3 tareas utilizando el formato del orquestador `GenericSQXWorkflow`.
- Se identificó la falta del flag `feature/metadata_export` en ETCD. Se escribió el valor `"true"` a `/sqx-worker/production/feature/metadata_export` y se reinició el servicio `symphony-worker` en el worker Zeus. El flujo ahora corre las 3 tareas secuencialmente y finaliza con éxito.
- A petición del usuario, se vaciaron por completo las colecciones de MongoDB `databank_metadata`, `type_rankings` y `export_runs`. Se re-lanzó el flujo en limpio y se validó que se insertaran exactamente 1 export_run, 52 databank_metadata y 24 type_rankings.
- Se extendió el archivo `config.json` agregando una tarea de tipo `group` con `batch_size: 2`, `source` de ranking con `top_n_per_logical_type: 1`, y que ejecuta la subtarea `project` en el folder `02_retester_full` en Zeus. El flujo se re-ejecutó con éxito aplicando paralelismo por tipo lógico y early-exit por lote en limpio.



