---
type: pattern
schema_version: 1
scope: project
created: "2026-09-03"
updated: "2026-09-03"
area: "[[Echo Forge]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[xKoRx/symphony]]"
entities:
  - "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
related:
  - "[[2026-09-03-echo-forge-worker-execution-model-v1]]"
  - "[[2026-09-03-orphan-mt5-after-cancel]]"
aliases:
  - cancel drain barrier
  - lifecycle invariant
confidence: verified
load_policy: when_project_loaded
indexable: true
index_priority: high
tags:
  - kind/pattern
  - scope/project
  - project/echo-forge
  - tech/temporal
---

# 2026-09-03-echo-forge-cancel-drain-lifecycle

## Patrón

Cuando GenericSQXWorkflow recibe CANCEL: solicita cancel de cada MT5 artifact child; `ParentClosePolicy=REQUEST_CANCEL`; `WaitForCancellation=true`; espera todos los children; el child no termina hasta que la activity drena el process tree owned; entonces Generic; entonces FlowRun CANCELLED. Cleanup de workspace después del drain. Distinto de CHANGE-001 (stop del worker OS no mata el job aceptado).

## Aplicabilidad

CancelWorkflow de jobs Forge con children que lanzan procesos externos. No aplica a multiplexación local (prohibida). No usa TERMINATE para children con cleanup físico.

## Ejemplo

Incidente C3: Generic selló `01:28:22.217Z` y cerró `01:28:22.243Z`; child Terminated `01:28:22.257Z` `by parent close policy`. `collectMT5ArtifactChildren` retorna en el primer `CanceledError`. ForgeCampaign ya usa REQUEST_CANCEL + WaitForCancellation para su Generic child; MT5 artifact children no.
