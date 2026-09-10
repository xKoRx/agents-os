---
type: decision
schema_version: 1
scope: project
created: "2026-08-25"
updated: "2026-08-25"
area: "[[Echo]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[xKoRx/symphony]]"
entities:
  - "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
related:
  - "[[DURABLE-FLOWRUN-RESUMABILITY-RCA-TOP]]"
aliases: []
confidence: verified
source_session: DURABLE-FLOWRUN-LIFECYCLE-WRITEBACK-CORRECTION-NORMAL
load_policy: manual
indexable: true
index_priority: high
tags:
  - kind/decision
  - scope/project
  - scope/project
---

# Durable FlowRun lifecycle writeback

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Contexto

- `sqx.flow_runs` era insert-only aunque el lifecycle y la correlación Temporal ya estaban congelados en el dominio y schema.

## Decisión

- El watcher es dueño del dispatch inicial después de StartV1 ACK; el root `GenericSQXWorkflow` es dueño de la seguridad de lifecycle y del terminal seal.
- Los commands tipados validan `FlowRunRef`, token, target y correlación; usan CAS con `row_version`, recuperación por lectura fresca y `UNKNOWN_COMMIT` según las semantics existentes.
- Se preservan las transiciones normales. Un dispatch duplicado sobre `COMPLETED`, `FAILED` o `CANCELLED` devuelve ACK compatible y nunca reabre el FlowRun.
- `temporal_workflow_id`, `temporal_namespace`, `temporal_first_run_id` y `temporal_current_run_id` son sólo correlación; `first_run_id` es immutable.

## Rationale

- La corrección quedó publicada en `xKoRx/symphony` con commit `db0f61bc5c397b47ee4d0a54e78cba0c4aea0a9d`, dentro del máximo de 11 archivos.
- El reset administrativo de Temporal y el `Terminate` manual permanecen fuera de sincronización automática; no se introdujeron heurísticas, reaper ni observer.

## Consecuencias

- No se habilitó `COMPLETED|FAILED|CANCELLED → RUNNING`; si producto necesita representar reset administrativo como lifecycle normal, debe escalarse a TOP con evidencia.

## Alternativas descartadas

- 
