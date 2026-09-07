---
type: change_log
scope: session
created: 2026-07-23
updated: 2026-07-23
area: "[[Echo]]"
project: "[[Echo Forge]]"
application: "[[Echo Forge - Cierre de Etapa 4]]"
entities:
  - "[[Echo Forge]]"
related:
  - "[[Echo Forge - Cierre de Etapa 4]]"
aliases: []
confidence: high
source_session: codex-2026-07-23-echo-forge-stage4-curve-algorithm
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
  - project/echo-forge
---

# Echo Forge Stage 4 curve algorithm entity update

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `10-projects/Echo Forge/agentes/Echo Forge - Cierre de Etapa 4.md`
  - `10-projects/Echo Forge/Echo Forge.md`
  - `80-agents/memory/internal/agent-memory/2026-07-23-echo-forge-stage4-phased-metrics-continuity.md`

## Motivo

- El owner rechazó que Net Profit y DD dominaran la comparación: menor beneficio puede ser preferible si PF, Sharpe, SQN, Ret/DD y forma de riesgo mejoran.
- El owner aprobó avanzar con la POC de warnings `OD-M10`.

## Fuentes usadas

- Feedback directo del owner 2026-07-23.
- `StrategyMetrics` actual en `sqx/core/domain/metadata.go`.
- Catálogo de métricas `FEAT-SQX-METRICS-CONTRACT/SPEC.md`.

## Resolución aplicada

- Plan elevado a v0.5.
- Reemplazado el score Pareto-dominante por contrato `CurveComparisonAlgorithm` y registry estático.
- Propuesto `risk_adjusted_delta.v1`: Ret/DD 25%, PF 20%, Sharpe 20%, SQN 15%, DD 15%, Net Profit 5%.
- Pareto NP/DD queda como diagnóstico; score y componentes quedan shadow.
- `OD-M10` pasó a `CONFIRMED`; la regla de warning de curva queda deshabilitada hasta aceptar `OD-M05`.

## Validación

- Los seis inputs del algoritmo inicial existen en `StrategyMetrics`.
- Pesos propuestos suman 100%.
- El ejemplo documentado reconcilia contribuciones y score redondeado.
- No se modificó código de Symphony.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin secretos; referencias locales son necesarias para el plan ejecutable.

## Rollback

- Revertir únicamente los cambios v0.5 en las notas del vault; no existe código que revertir.
