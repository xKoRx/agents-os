---
type: raw_session
scope: session
created: "2026-07-05"
updated: "2026-07-05"
area: "[[Symphony]]"
project: "[[Echo Forge]]"
application: "[[echo-forge]]"
entities:
  - "[[Echo Forge]]"
related: []
aliases: []
confidence: verified
source_session: "241add91-8048-41f7-b2cd-87470b589ef0"
load_policy: never
indexable: false
index_priority: never
tags:
  - app/echo-forge
  - app/echoforge
  - area/symphony
  - kind/rawsession
  - project/echo-forge
  - project/echoforge
  - scope/session
---
# 2026-07-05-sqx-builder-export-rank-flow-raw

> [!warning]+ Raw session L0
> Archivo de auditoría y retrofit. Excluido del retrieval normal y de Graphify.

## Contexto

- Agente/superficie: Antigravity
- Proyecto o entidad: [[Echo Forge]]
- Objetivo de la sesión: Configuración y explicación de un flujo SQX con Builder, Export y Rankeo (3 tareas), corrección del error en ETCD, y posterior extensión para agregar un subflujo de retesteador agrupado de a 2 con early exit sobre 1 pasado exitosamente.

## Transcript

```
User: Configurar flujo SQX con Builder, Export, Rankeo.
Agent: Creó input/example/config.json.
User: Falló classify_and_rank con metadata missing for wave.
Agent: Investigó y descubrió que /sqx-worker/production/feature/metadata_export no existía en ETCD. Lo puso en "true", reinició el worker en Zeus y volvió a lanzar el flujo copiándolo a input/.
Result: El flujo completó con éxito las 3 tareas e importó los datos a MongoDB.
User: Vaciar databank_metadata, type_rankings y export_runs, y extender flujo para agregar subflujo de retesteador por tipo, agrupado de a 2, que necesite al menos 1 pasado para terminar (early exit).
Agent: Limpió MongoDB, modificó input/example/config.json agregando la tarea "group" con batch_size: 2, top_n_per_logical_type: 1 y el retester (02_retester_full) como subtarea. Volvió a lanzar el flujo.
Result: El flujo corrió exitosamente en limpio procesando 4 tareas, aplicando paralelismo por tipo lógico en los 27 tipos, subdividiendo en lotes de 2, y aplicando early exit al obtener 1 aprobado.
```

## Evidencia externa

- [config.json](file:///Users/rjara/go/src/github.com/xKoRx/symphony/input/example/config.json)
- [query_mongo.go](file:///Users/rjara/go/src/github.com/xKoRx/symphony/sqx/tools/query_mongo.go)


