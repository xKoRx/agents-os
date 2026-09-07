---
type: pattern
schema_version: 1
scope: project
created: "2026-09-06"
updated: "2026-09-06"
area: "[[Echo Forge]]"
project: "[[Echo Forge]]"
application: "[[xKoRx/symphony]]"
entities:
  - "[[Echo Forge]]"
related:
  - "[[2026-09-03-echo-forge-one-job-per-worker]]"
  - "[[2026-09-06-echo-forge-mt5-global-physical-ownership-v2]]"
aliases:
  - mt5ActivityTechnicalCeiling
  - temporal activity timeout clamp
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

# 2026-09-06-echo-forge-temporal-activity-ceiling-clamp

## Patrón

Dos hechos de la plataforma Temporal que gobiernan cualquier timeout "infinito" de actividad. (1) Resolución: el `ActivityOptions.StartToCloseTimeout` conserva exactamente el valor que el workflow fija (en symphony, `mt5ActivityTechnicalCeiling = MaxInt64ns − 1s`); el round-trip `durationpb` no desborda. (2) Materialización: lo que la actividad observa en `activity.Info.StartToCloseTimeout` es `min(opción, WorkflowRunTimeout del entorno)`; la testsuite del Go SDK fija ese run-timeout a `maxWorkflowTimeout = 24h × 365 × 10` (87600h, constante "copiada de la implementación del servicio"), idéntica en SDK v1.35.0 y v1.44.1. El clamp es semántica de plataforma, no un timeout de negocio.

## Aplicabilidad

Misiones que eliminan timeouts de negocio de actividades long-running (B1B, B2, NORMAL D): asertar el techo a nivel de `ActivityOptions` y por igualdad entre configs; en el nivel de `activity.Info`, asertar `> 0` y `<= techo`, nunca igualdad contra la constante del entorno. Al verificar el SDK, el pin efectivo lo decide `go.work` (resuelve v1.44.1 para el módulo sqx aunque `sqx/go.mod` pinée v1.35.0): leer el código del SDK en la versión resuelta y confirmar el constante también en la pineada antes de declarar evidencia.

## Ejemplo

B1B (commit `ef65dd1`): `TestMT5BacktestArtifactActivityOptions_TechnicalCeiling` iguala `opts.StartToCloseTimeout == mt5ActivityTechnicalCeiling`; `TestMT5BacktestArtifactWorkflow_TimeoutFieldDoesNotAffectExecution` iguala el valor efectivo observado entre dos configs que difieren sólo en `tasks[].mt5.timeout` ("45m" vs "banana") y ambos caen en el mismo 87600h del entorno.
