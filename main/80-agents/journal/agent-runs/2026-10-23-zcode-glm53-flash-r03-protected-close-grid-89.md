---
type: agent_run
schema_version: 1
scope: session
created: "2026-10-23"
updated: "2026-10-23"
area: "[[Echo]]"
project: "[[Echo Futures — Optimización de Campañas]]"
application:
entities: []
related: []
aliases: []
agent_surface: "[[ZCode]]"
agent_model: GLM-5.3-Flash
model_source: host
task_type: coding
task_complexity: high
outcome: success
verification: market_evidence
evaluator: agent
user_rework: unknown
source_session:
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/agent-run
  - scope/session
---

# R03 — cierre protegido corregido + parrilla histórica 89/89

## Tarea

Corregir `SIM_SUBMIT_FAILED: PROTECTED_CLOSE_ORDER_MISMATCH` conservando invariantes, re-ejecutar las 23 campañas PARTIAL de R02, adjudicar las 89 identidades con finalizador corregido y publicar.

## Evidencia de verificación

- Root cause reproducido en la coordenada exacta con binario de diagnóstico de identidad propia (worktree `a029744a`); la única comparación fallida era `not_working:FILLED`.
- Fix `e951d258` (venue `REJECTED` sellado + owner consume intento + skip de cancel comprometido); suites operation/simexecution/provider/riskgeommm verdes; coverage venue/observe 100%, emitter 96,6%; failure-set delta 0 vs baseline (extra preexistente verificado en `c6ae3dbc` con worktree limpio).
- Caso históricamente fallido COMPLETE+reconciled bajo binario sellado `e21a28dc…` (FBC-5M-R500: 23 compras, 1 pase); 23/23 re-ejecuciones exit=0; HISTORICAL_GATE PASS 89/89; económico 3037→328 (10,8%); 3 familias ≥25%.
- Push con readback `origin == HEAD == ae1b09bc`; entregables `lab-r03/` con SHA256SUMS.

## Límites

- Cobertura del emitter: guard preexistente inalcanzable de `cancelPendingRiskOrders` sin test (documentado, no rama nueva).
- Tiempo-hasta-pase depende de `pass_events` (sin reconstrucción por cuenta pendiente).
