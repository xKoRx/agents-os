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
  - Conflicto de indices de MongoDB
  - IndexKeySpecsConflict
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
  - tool/mongodb
---
# MongoDB Index Specifications Conflict on Startup

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Síntoma

- Al arrancar el worker de Symphony, este crashea de forma inmediata reportando un error de inicialización de índices en MongoDB:
  `IndexKeySpecsConflict: An existing index has the same name as the requested index. Existing index: { unique: true ... }, Requested index: { ... }`

## Causa

- La base de datos de MongoDB remota ya tiene definido un índice en la colección con ciertas propiedades (por ejemplo, con restricción de unicidad `unique: true` o con un ordenamiento específico).
- En el código del adaptador de MongoDB en Go (`EnsureIndexes`), se intenta recrear o declarar el mismo índice (con el mismo nombre) pero omitiendo la opción `SetUnique(true)` (o viceversa), causando un conflicto de especificaciones que MongoDB no puede resolver sin recrear el índice.

## Impacto

- El worker de Symphony no puede arrancar, deteniendo el procesamiento de cualquier tarea orquestada por Temporal.

## Detección

- Buscar en los logs de inicialización del worker (`/var/log/symphony/symphony-worker.log` o `journalctl -u symphony-worker.service`) la cadena `IndexKeySpecsConflict` o `error al asegurar indices para coleccion`.

## Mitigación

1. Alinear la especificación del índice en el adaptador Go para que coincida exactamente con lo que está en la base de datos (por ejemplo, agregando `.SetUnique(true)` al construir la estructura `mongo.IndexModel`).
2. Alternativamente, si el índice existente es incorrecto u obsoleto, se puede entrar a la shell de MongoDB y dropear el índice en conflicto usando `db.collection.dropIndex("index_name")`, para que el worker lo vuelva a crear limpio al iniciar.

## Evidencia

- Repo `github.com/xKoRx/symphony`, path `sqx/adapters/metadata-mongo/adapter.go`.
