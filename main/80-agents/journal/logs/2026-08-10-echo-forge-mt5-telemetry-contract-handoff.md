---
type: change_log
scope: session
created: 2026-08-10
updated: 2026-08-10
area: "[[Echo]]"
project: "[[Echo Forge]]"
entities:
  - "[[Echo Forge]]"
  - "[[Echo Forge - Etapa 6]]"
  - "[[echo-forge]]"
related:
  - "[[Echo Forge - Etapa 6]]"
aliases: []
confidence: verified
source_session:
load_policy: manual
indexable: false
index_priority: never
share_scope: local
tags:
  - kind/change-log
  - scope/session
  - area/echo
  - project/echo-forge
  - change/updated
---

# Change Log — Handoff de contrato de telemetría MT5

## Cambios

- **Actualizado** `10-projects/Echo Forge/agentes/Echo Forge - Etapa 6.md` con
  el diagnóstico reproducible y el próximo paso de implementación.

## Hallazgo verificado

- `list_mt5_artifacts` recibe `domain.MT5ArtifactListRequest`, que no
  implementa `TelemetryCarrier`. El interceptor estricto del SDK rechaza el
  argumento antes de ejecutar la activity.
- `domain.ArtifactTaskRequest`, que reciben `mt5_compile_artifact` y
  `mt5_backtest_artifact`, tiene la misma omisión. El worker Windows aún no
  interviene en el error observado; lo hará después del listado si no se cubre
  el segundo contrato.
- La cobertura existente omite el interceptor productivo: tests directos de
  activity y mocks de workflow no ejercitan esa validación.

## Próximo paso

Implementar de forma aditiva la propagación de `telemetry.Context` y
`GetTelemetry()` en ambos payloads y todos sus callers; sumar assertions de
interfaz y una prueba que instale el interceptor de producción. Validar el
worker principal y el binario Windows antes de retomar el smoke físico.
