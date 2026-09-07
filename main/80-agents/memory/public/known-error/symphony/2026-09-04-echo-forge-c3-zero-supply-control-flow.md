---
type: known_error
schema_version: 1
scope: project
created: "2026-09-04"
updated: "2026-09-04"
area: "[[Echo]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[xKoRx/symphony]]"
entities: []
related:
  - "[[2026-09-04-echo-forge-c3-zero-supply-closure]]"
  - "[[2026-09-04-cert-a-no-final-reretester-survivor]]"
aliases:
  - ZERO_SUPPLY_CONTROL_FLOW
  - final reretester requires a non-empty StrategyArtifacts cohort
confidence: verified
source_session: "[[2026-09-04-echo-forge-c3-zero-supply-burndown-summary]]"
load_policy: when_error_matches
indexable: true
index_priority: high
tags:
  - kind/known-error
  - scope/project
  - project/echo-forge
---

# Zero-supply convierte rechazo de calidad en WAVE_FLOW_RUN_FAILED

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Síntoma

- WFM durable completa con `FAIL / SEVERE_WARNING` (u otros FAIL analíticos); `StrategyArtifacts` queda vacío; Generic falla en Final Reretester **antes** de activities; Campaign `FAILED / WAVE_FLOW_RUN_FAILED`; 0 Ranking GLOBAL, 0 FINALIST_PROMOTION, 0 stop evaluation.

## Causa

- Asimetría de control-flow: WFM/select/apply/trade_list/mt5_exporter tratan cohort=0 como skip exitoso; `validateFinalReretesterFanoutInput` exige cohorte no vacía. El error de workflow sella FlowRun `FAILED`. FinalizeWave short-circuita stop/promotion.
- Downstream, si se parcheara sólo ese guard: ranking noop (válido) + `runFinalistPromotion` exige exactamente un GLOBAL binding + Campaign exige Promotion AVAILABLE + Result Surface trata COMPLETED sin snapshot como INCONSISTENT.

## Impacto

- C3 no puede demostrar CONTINUE/MAX_WAVES_REACHED con 0 promoted. Un rechazo de calidad se clasifica como fallo técnico. CERT física descubre un choke por vez.

## Detección

- Mensaje exacto `final reretester requires a non-empty StrategyArtifacts cohort` en Generic. PG: `waves_started>=1`, `finalists=0`, `stop_evaluations=0`, failure `WAVE_FLOW_RUN_FAILED`.

## Mitigación

- Resuelto en source por [[2026-09-04-echo-forge-c3-zero-supply-closure]] (`ZERO_SUPPLY_CONTROL_FLOW_CLOSURE`): la cohorte exacta vacía omite stages caros y ranking, materializa Promotion V1 empty explícita y deja FlowRun COMPLETED. No recertificar físicamente ni crear release hasta ejecutar el siguiente paso autorizado.

## Evidencia

- CERT-A `097d17c2-d50d-48a4-aa08-3e3426092f1d`, FlowRun `e1a964ac-99ee-48e8-87bf-e34638663735`, release `0.2.91`, source `9641c9f`. Código: `sqx/workflows/generic_workflow.go` L1688-1690, L970-971, L984-986; `forge_campaign_activity.go` L198-213; `result.go` L326-328.
- Implementación y regresión determinista: [[2026-09-04-echo-forge-c3-zero-supply-closure-implementation]]; T1–T12 dirigidas verdes y gates race/vet de los paquetes afectados verdes. La suite workflow completa conserva fallos baseline de registro `flow_run_start`; la suite PostgreSQL completa quedó limitada por duración, con selección dirigida verde.
