---
type: change_log
schema_version: 1
scope: session
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
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-08-25-durable-flowrun-lifecycle-writeback

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `xKoRx/symphony/sqx/core/capabilities/persistence.go`
  - `xKoRx/symphony/sqx/adapters/registry-postgres/flow_run.go`
  - `xKoRx/symphony/sqx/activities/watcher/steps.go`
  - `xKoRx/symphony/sqx/activities/worker/flow_run_lifecycle_activity.go`
  - `xKoRx/symphony/sqx/workflows/generic_workflow.go`

## Motivo

- Corregir el gap confirmado: no había writer productivo posterior a `ResolveFlowRun`, dejando lifecycle/correlation siempre en PENDING/vacío.

## Fuentes usadas

- Contrato de la sesión `DURABLE-FLOWRUN-LIFECYCLE-WRITEBACK-CORRECTION-NORMAL`, dominio `FlowRunState.Transition`, schema existente y baseline `20356f2`.

## Resolución aplicada

- Se cableó dispatch writeback watcher, root-start recovery, terminal seal determinista y cancellation cleanup con contexto desconectado cuando aplica. CAS sin last-write-wins; no se cambiaron identidades congeladas.

## Validación

- Tests focalizados, `go vet` y `git diff --check` PASS. Full registry queda DEGRADED sólo por `TestUpsertStrategyV2_V0V1V2Coexistence`, fallo baseline ajeno.

## Compartibilidad

- **Scope:** local / team
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Revertible por el commit publicado `db0f61bc5c397b47ee4d0a54e78cba0c4aea0a9d`; no se tocaron migraciones ni foreign dirty.
