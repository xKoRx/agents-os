---
type: known_error
schema_version: 1
scope: project
created: "2026-08-27"
updated: "2026-08-27"
area: "[[Meli]]"
project: "[[Playmaker — Doble dispatch al avanzar batches]]"
application: "[[rio-playmaker]]"
entities:
  - "[[Playmaker — Doble dispatch al avanzar batches]]"
  - "[[rio-playmaker]]"
related: []
aliases:
  - NoSuchMethodError JsonJackson getMapper en rio-playmaker
  - java-toolkit-kvs 0.6.1 incompatible con json-jackson 4
confidence: verified
source_session:
load_policy: when_error_matches
indexable: true
index_priority: high
tags:
  - kind/known-error
  - scope/project
  - area/meli
  - app/rio-playmaker
  - tech/kvs
  - tech/jackson
---

# Playmaker — java-toolkit-kvs 0.6.1 es incompatible con json-jackson 4

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Síntoma

- El container inicia el run step y luego queda sin levantar; en el stack aparece `NoSuchMethodError` al construir `com.fury.toolkit.kvs.LowLevelClient`.

## Causa

- `java-toolkit-kvs:0.6.1` fue compilado contra `JsonJackson.getMapper()` con retorno `com.fasterxml.jackson.databind.ObjectMapper`, mientras `json-jackson:4.0.0` expone `tools.jackson.databind.ObjectMapper`; el descriptor JVM no coincide aunque el nombre del método sea igual.

## Impacto

- La aplicación falla durante la creación del bean KVS y Fury deja el deployment en `waiting_application`: el proceso no llega a levantar aunque los mensajes previos de OTEL parezcan normales.

## Detección

- Buscar `NoSuchMethodError: com.mercadolibre.json.JsonJackson.getMapper()` en los logs de arranque y confirmar la resolución con `dependencyInsight` para `java-toolkit-kvs` y `json-jackson`.

## Mitigación

- Alinear `java-toolkit-kvs` a `0.7.4` cuando el runtime resuelve `json-jackson:4.0.0`, y agregar un test que construya el cliente KVS de producción para detectar el linkage durante la suite.

## Evidencia

- En `rio-playmaker`, `0.0.12-listener-lock` reprodujo el fallo; el commit `b4fa880a2` actualizó KVS a `0.7.4`, la suite completa pasó con 3.240 tests y Fury finalizó `0.0.13-listener-lock` correctamente.
