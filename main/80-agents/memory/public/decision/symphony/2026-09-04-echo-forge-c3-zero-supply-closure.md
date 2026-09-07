---
type: decision
schema_version: 1
scope: project
created: "2026-09-04"
updated: "2026-09-04"
area: "[[Echo]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[xKoRx/symphony]]"
entities: []
related:
  - "[[2026-08-30-echo-forge-finalist-promotion-v1]]"
  - "[[2026-08-31-forge-campaign-stop-policy-v1-contract]]"
  - "[[2026-09-04-cert-a-no-final-reretester-survivor]]"
  - "[[2026-09-04-echo-forge-c3-zero-supply-control-flow]]"
aliases:
  - ZERO_SUPPLY_CONTROL_FLOW_CLOSURE
  - C3 zero-supply canonical semantics
confidence: verified
source_session: ECHO-FORGE-C3-END-TO-END-BLOCKER-BURNDOWN-AND-ZERO-SUPPLY-CLOSURE-TOP
load_policy: when_project_loaded
indexable: true
index_priority: high
tags:
  - kind/decision
  - scope/project
  - project/echo-forge
---

# 2026-09-04-echo-forge-c3-zero-supply-closure

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Contexto

- Audit TOP read-only sobre symphony `9641c9f11b2a321041f61ea6b8d93ef199d5a38e` y SDK `c85594440f6755443ceb97ec4e333cd0ddb5b0ed`. Release desplegada `0.2.91`. C3 sigue `BLOCKED / CLOSED`.
- CERT-A `097d17c2-d50d-48a4-aa08-3e3426092f1d` / FlowRun `e1a964ac-99ee-48e8-87bf-e34638663735` alcanzó WFM `FAIL / SEVERE_WARNING` (55 resultados), survivor cohort vacío, y el Generic falló en `validateFinalReretesterFanoutInput` con `final reretester requires a non-empty StrategyArtifacts cohort`. Campaign selló `WAVE_FLOW_RUN_FAILED`.
- Contratos congelados en colisión: Ranking SPEC prohíbe sintetizar RankingSnapshot vacío; Promotion V1 exige Decision `FINALIST_PROMOTION` (cero filas = nunca ejecutó) con evidence `RankingSnapshotRef`; Campaign exige FlowRun `COMPLETED` + Promotion AVAILABLE antes de stop eval.

## Decisión

- Zero supply es un **outcome de negocio válido**. No es fallo técnico de FlowRun ni de Campaign.
- Detección canónica: el candidate cohort (`StrategyArtifacts` + `Keys`) llega a 0. S2 (todos WFM FAIL/REJECTED) y S4 (Final Reretester N→0 via CompleteEmpty) convergen al mismo continuation path. S6 (ranking real con top vacío / `TOP_PROJECTION_EMPTY`) permanece distinto: ahí sí existe RankingSnapshot.
- Stages caros per-strategy con cohort=0 se **SKIPPEAN** (cero activities/children): Final Reretester fan-out, TradeList, MQ5, Compile, MT5, Reconcile, Score. No invocar activities artificiales con input vacío.
- Stages cohort/campaign que **sí** se materializan: FlowRun `COMPLETED`; StageExecution `promote_finalists@sqx-finalist-promotion.v1` CompleteEmpty; Decision `FINALIST_PROMOTION` `COMPLETED` con `effective_promoted_count=0` y `finalists=[]`; Campaign stop evaluation.
- RankingSnapshot vacío: **prohibido**. Empty batch no crea snapshot ni activity (`SPEC.md` §5). No sintetizar evidencia.
- **CHALLENGE a reutilizar `TOP_PROJECTION_EMPTY` sin snapshot:** hoy Validate/Campaign Inspect/Result Surface exigen `source_ranking_snapshot`. Mentir un snapshot viola Ranking SPEC. Recomendación de implementación: reason **`TOP_PROJECTION_EMPTY`** para S6 (ranking existió); para S2/S4/S5 (no hubo ranking) enmendar Promotion V1 con evidence sin snapshot y reason reutilizada **sólo si** Validate/Inspect/Result se enmiendan en el mismo batch. Preferir reutilizar el reason para no bifurcar Campaign; no inventar `INSUFFICIENT_SUPPLY` como stop reason (ya descartado en Stop Policy V1).
- FlowRun terminal: `COMPLETED` si la wave ejecutó los gates de calidad y no hubo error de infra/contrato/corrupción. `FAILED` queda para esos errores. WFM `FAIL / SEVERE_WARNING` es rechazo analítico COMPLETED, no fallo técnico.
- Campaign: `effective_promoted_count=0` no es stop reason. Precedencia intacta: `TARGET_REACHED` > `MAX_WAVES_REACHED` > `CONTINUE`. Wave 1 / target unmet / waves remaining / 0 promoted → `CONTINUE`. Última wave / 0 promoted → `MAX_WAVES_REACHED`. Dedupe first-observation-wins intacto.
- Result Surface: `COMPLETED` + ranking configurado + 0 snapshots no debe seguir siendo `INCONSISTENT` cuando Promotion empty-without-snapshot está presente. Eso es parte del mismo FIX CONTRACT, no un follow-up.

## Rationale

- El choke actual convierte un rechazo de calidad en `LifecycleFailed` + `WAVE_FLOW_RUN_FAILED`, impidiendo stop eval. Aceptar empty Final Reretester sin cerrar Promotion/Result dejaría el siguiente BLOCKED en `finalist promotion source ranking must resolve exactly one GLOBAL binding` o `FINALIST_PROMOTION_MISSING` o Result `INCONSISTENT`.
- Skip de etapas caras ya existe en WFM/select/apply/trade_list/mt5_exporter/ranking noop. Final Reretester es la asimetría. Promotion no puede skippearse porque cero filas significa “nunca ejecutó”.

## Consecuencias

- NEXT EXACT: `ECHO-FORGE-C3-ZERO-SUPPLY-END-TO-END-CLOSURE-NORMAL`. Un solo FIX CONTRACT `ZERO_SUPPLY_CONTROL_FLOW_CLOSURE`. No release ni cert física antes de esa implementación.
- C3_REQUIRED: CONTINUE/MAX con 0 promoted. POST_C3: Campaign Replenishment general, Builder Budget, A0 Live Validation.
- Recert física lean `{1,1}` puede certificar `MAX_WAVES_REACHED` sin finalists; `TARGET_REACHED` y `CONTINUE` se demuestran primero en tests deterministas.

## Alternativas descartadas

- Fix = aceptar empty Final Reretester y parar: deja Promotion/Campaign/Result como próximos BLOCKED.
- Sintetizar RankingSnapshot vacío: contradice Ranking SPEC §5.
- Campaign acepta `PROMOTION_MISSING` en FlowRun COMPLETED: contradice Promotion V1 (cero filas = nunca ejecutó) y oculta skips-bug.
- Inferir `INSUFFICIENT_SUPPLY` como stop: ya descartado en Stop Policy V1.
- Invocar Final Reretester/Score/MT5 con input vacío “para pasar”: viola skip de etapas caras.
