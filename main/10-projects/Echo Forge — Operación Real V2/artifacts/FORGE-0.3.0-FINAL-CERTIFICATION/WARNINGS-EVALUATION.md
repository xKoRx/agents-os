# WARNINGS-EVALUATION — mecanismos A y B (2026-10-18)

## Veredicto

**MECHANISM_B_EXECUTED_IN_SHADOW_WITH_FROZEN_CONTRACT_LIMITS** — la activity `evaluate_strategy` (deep_warnings_shadow.v1) fue registrada en el worker, ejecutó 22/22 dentro del group (después de WFM, antes de robust selection) y persistió 22 StrategyEvaluations shadow con WarningSummary y Verdict reales. Las reglas que requieren métricas F4 o WFM no pudieron activarse: el funnel congelado no invoca `shadow_compute_only` y F4 no persiste `wfm_run_key` en la StrategyEvaluation (`domainWFMKey` devuelve "" por contrato). Cero cambios en la decisión de selección.

## Contrato revisado (mandato §5)

1. `EvaluateStrategyRequest`: scope (wave_key, request_id, run_id, strategy_id, stage, variant, result_key, cell_key, sample_type), Trades/SQXNativeValues opcionales, Baseline/Optimized opcionales.
2. Inputs: o una StrategyEvaluation persistida por `shadow_compute_only` (vía `LoadByScope`), o datos inyectados por el caller; con ninguno de los dos, el contrato define el **camino standalone** (evaluación in-memory en el scope, reglas aplicadas, enriquecimiento persistido).
3. Posición válida: task type `evaluate_strategy` ya existía en el switch de GenericSQXWorkflow (root y group). Se insertó como task del group entre `evaluate-wfm` y `select-robust`.
4. Mismo cohort, sin FlowRun nuevo: corre dentro del group de w10, batch 1 por child.
5. Cableado focalizado probado ANTES del E2E: el hueco real era que **nadie registraba la activity en el worker** (`NewEvaluateStrategyActivity` inexistente en main.go → "activity not registered" en runtime). Fix mínimo: registro con loader/wfm nil (puertos opcionales por contrato) + writer = repositorio Mongo existente (`StrategyEvaluationRepository.EnsureIndexes` ya corre en el boot).

## Evidencia real (no "la activity existe en source")

- Mongo `forge.strategy_evaluations` wave_key="10": **22 documentos** (uno por estrategia del cohort), todos `evaluation_mode="shadow"`.
- Documento tipo: `_id sha256:de65a3e0…`, `strategy_id` = nombre SQX real del cohort (`NDX_L_H1_flow_example_2_v1_….z0`), `stage=evaluation, variant=center, sample_type=FULL`, `request_id c909e463…` (el request real de w10), `evaluated_at 06:25:37Z` (ventana WFM→robust del group).
- `warning_summary`: `{"ruleset_version":"deep_warnings_shadow.v1","verdict":"INSUFFICIENT_DATA","count_by_severity":{}}` — **WarningSummary y Verdict COMPUTADOS** (INSUFFICIENT_DATA es el veredicto correcto del agregador sin datos).
- Warnings tipados: **0 activados** en 22/22 — condición esperada y documentada: sin métricas F4 ni WFM en el scope, ninguna regla de negocio activa; el veredicto agregado es INSUFFICIENT_DATA. NOTA HONESTA: certificar reglas con datos reales requiere extender el funnel (invocar shadow_compute_only con trades del cohort) — eso es NUEVA arquitectura y queda fuera de este mandato.
- Correspondencia con StrategyRef/scope real: strategy_id == nombre del SQX en el cohort; request/run = FlowRun w10; las 22 identidades corresponden 1:1 con las 22 seleccionadas.
- **Cero impacto en selección**: 22/22 SELECTED antes y después; `select_robust_run` no consume el enrichment (veredicto informativo por construcción); sin filtros ENFORCE nuevos.

## Mecanismo A (evaluate_wfm)

Ejecutado 22/22 como siempre (robust_run_selection_v2 0.35/0.01/0.01) — sus warnings legacy siguen operando igual; sin cambios.
