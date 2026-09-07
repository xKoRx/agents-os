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
source_session: codex-2026-07-23-echo-forge-stage4-metrics-decisions
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

# Echo Forge Stage 4 metrics decisions entity update

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `10-projects/Echo Forge/agentes/Echo Forge - Cierre de Etapa 4.md`
  - `10-projects/Echo Forge/Echo Forge.md`
  - `80-agents/memory/internal/agent-memory/2026-07-23-echo-forge-stage4-phased-metrics-continuity.md`

## Motivo

- El owner respondió el registro `OD-M01..OD-M10` y solicitó propuestas concretas para recovery mensual, comparación de curvas y una POC inicial de warnings.
- También cuestionó portfolio y período futuro; se rastreó su origen al prompt de investigación y se reclasificaron como restricciones técnicas, no métricas custom.

## Fuentes usadas

- Respuestas directas del owner 2026-07-23.
- Prompt maestro preservado en `[[Echo Forge - Cierre de Etapa 4]]`.
- `sqx/activities/worker/evaluate_wfm.go`, `sqx/core/robust/selector.go` y contratos de dominio actuales para preservar el comportamiento legacy de warnings.

## Resolución aplicada

- Confirmadas ventana/ancla de R:R, comparación mejor mes/peor año y PnL neto de comisión/swap.
- Definida jerarquía SQX nativo → trade list de reconciliación.
- Propuestas `OD-M03/M05/M10` documentadas con fórmulas, edge cases, reglas y modo shadow sin efecto en selección.
- Plan elevado a v0.4; G0 sigue bloqueado hasta aprobación humana y spike técnico.

## Validación

- Se verificó que deep warnings no se agreguen conceptualmente a `WFMEvaluation.Warnings`, porque el selector actual penaliza todos los strings.
- Se mantuvieron portfolio/future en exportación y regresión sin incorporarlos al scoring individual.
- No se modificó código de Symphony.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin secretos; paths/referencias locales son deliberados para ejecución del proyecto.

## Rollback

- Revertir solo los cambios v0.4 de las notas del vault; no existe cambio de código que revertir.
