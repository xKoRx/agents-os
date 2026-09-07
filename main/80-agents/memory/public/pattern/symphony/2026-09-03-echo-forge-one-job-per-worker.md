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
  - "[[2026-09-03-echo-forge-worker-lifecycle-mt5-orphan-plan]]"
aliases:
  - MAX_ACTIVE_JOBS_PER_WORKER
  - worker serialization invariant
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

# 2026-09-03-echo-forge-one-job-per-worker

## Patrón

Un proceso worker por máquina y como máximo un job físico activo en ese worker. El paralelismo es horizontal entre máquinas vía Temporal. `MaxConcurrentActivityExecutionSize=1` y `MaxConcurrentLocalActivityExecutionSize=1` son la autoridad. `ActivityGate` no serializa.

## Aplicabilidad

Todos los workers físicos de Echo Forge (SQX, MT5, future class). Activities que lanzan `sqcli`, `terminal64`, MetaEditor u otra herramienta externa. Retry attempt N+1 no arranca mientras N posea descendants.

## Ejemplo

MT5 hoy: `mt5TemporalWorkerOptions` fija concurrency 1. SQX hoy pasa cero y el SDK `configuredWorkerOptions` lo normaliza a 1; no existe `WORKER_LOCAL_CONCURRENCY_CONTRACT_VIOLATION`. Compiles MT5 del incidente: 8 children Temporal, 1 físico serial. Backtests al cancel: 8 Temporal scheduled, 0 Started.
