---
type: change_log
schema_version: 1
scope: session
created: "2026-10-08"
updated: "2026-10-08"
area: "[[Meli]]"
project:
application: "[[rio-controlplane-clickhouse]]"
entities: ["[[rio-controlplane-clickhouse]]"]
related: []
aliases: []
confidence: verified
source_session:
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# ClickHouse — Pruebas físicas locales verificadas

## Cambio

- Actualizados `30-resources/applications/rio-controlplane-clickhouse.md`, índice y log del dominio; captura fuente y agent run materializados mediante contrato.
- Antes: baseline Gradle/ping certificados; DDL no ejecutado. Ahora: 2340 tests Gradle y 14 escenarios físicos PASS con el CP y ClickHouse real; tres fixes locales y cleanup contrastados.

## Motivo y fuente

- Pedido explícito de funcionamiento/pruebas locales. Es verdad operacional vigente respaldada por [[Source — ClickHouse — Pruebas físicas locales 2026-10-08]], no memoria de razonamiento.

## Resolución aplicada

- Se conserva el baseline develop y la eliminación previa de la rama descartada. Se reflejan cambios sin commit y los límites de Kafka/Playmaker/Cloud/S3/Iceberg.
- Se sustituye el gap de Context en el ejemplo README por el fixture ya corregido, sin alterar las capturas históricas.

## Validación

- Suite completa y física PASS; recurso físico/usuario/detached cleanup = 0; metadata/provenance revisados y lint acotado al cierre del segmento.

## Compartibilidad

- Scope local. Sin credenciales, diffs completos ni logs pesados; provenance de código como repo más paths relativos.

## Rollback

- Restituir únicamente el bloque anterior de estado local y el gap de fixtures de la página canónica; conservar las fuentes históricas y cambios ajenos.
