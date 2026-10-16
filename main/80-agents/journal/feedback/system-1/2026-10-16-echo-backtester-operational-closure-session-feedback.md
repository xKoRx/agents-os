---
type: session_feedback
schema_version: 1
scope: session
created: "2026-10-16"
updated: "2026-10-16"
area: "[[Echo]]"
project: "[[Echo Futures]]"
entities: []
related:
  - "[[TRADESGERARD-CONSOLIDATION]]"
aliases: []
source_session: "sess_6c1f4cfa-01c8-424a-bbb1-0540e9d3b818"
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/session-feedback
  - scope/session
---

# Session Feedback — 2026-10-16-echo-backtester-operational-closure

## Pain Pattern Candidate

- **«COMPLETE/reconciled» sin verificar las políticas del request ejecutado:** la aceptación anterior validó contabilidad pero no contrastó el request contra el preset del experimento; una omisión de un flag de receta (`--operability-policy` vacío, legal por diseño) dejó la campaña entera sin su política de retiro y nadie lo vio porque los números conciliaban. Prevención aplicada: preset versionado que conserva la política hasta el request + rechazo pre-motor; lección general: la aceptación de campañas debe incluir la comparación preset↔request, no sólo la conciliación interna.

## What Worked

- La reconstrucción por eventos existentes (estados, comandos, renovación) identificó el primer punto causal sin gastar campañas: el presupuesto de motor se usó 1/3.
- La trayectoria corregida reprodujo los cuatro antecedentes O11 (262 trades, 13 compras, cobro 1651, caja 5091) sin forzarlos — la comparación con antecedentes sirvió de corroboración, no de aserción.

## Tooling Notes

- `platform-batch` comprime `economic.ndjson.gz` cuando el output crece (la corrida con rotación produce ~6× eventos); los extractores deben manejar ambos formatos.
