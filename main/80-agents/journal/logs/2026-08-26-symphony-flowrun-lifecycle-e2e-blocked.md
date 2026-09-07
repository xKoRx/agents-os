---
type: change_log
schema_version: 1
scope: session
created: "2026-08-25"
updated: "2026-08-25"
area: "[[Echo]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[echo-forge]]"
entities: []
related: []
aliases: []
confidence: verified
source_session: DURABLE-FLOWRUN-LIFECYCLE-WRITEBACK-E2E-NORMAL
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-08-26-symphony-flowrun-lifecycle-e2e-blocked

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

  - **Tipo:** created
- **Archivo(s):**
  - `80-agents/memory/public/known-error/symphony/2026-08-26-flowrun-lifecycle-telemetry-carrier-mismatch.md`

## Motivo

- Registrar el defecto material descubierto durante la certificación física y la degradación de retrieval observada durante el arranque/cierre.

## Fuentes usadas

- Baseline `db0f61bc5c397b47ee4d0a54e78cba0c4aea0a9d`, release `0.2.70`, evidencia Temporal/PostgreSQL de la sesión y revisión estática del contrato `TelemetryCarrier`.

## Resolución aplicada

- Se creó una nota `known_error`; no se modificó código de producto, no se ejecutaron migrations y no se alteró PostgreSQL manualmente.

## Validación

- La ejecución física quedó `BLOCKED`: el workflow tiene `flow_run_start` reintentando con `activity argument does not implement TelemetryCarrier`, mientras la fila permanece `PENDING`, `row_version=0`.

## Compartibilidad

  - **Scope:** local
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- La nota de error es la única memoria pública nueva; retirar o reemplazarla requiere nueva evidencia y otro `change_log`.
