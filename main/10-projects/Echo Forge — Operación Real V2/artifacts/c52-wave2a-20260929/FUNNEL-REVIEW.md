# FUNNEL-REVIEW.md — RECOVERY C5.2 (wave2a) · Echo Forge — Operación Real V2

**2026-09-29 · cierre de la recovery del defecto de chaining (wave1z).** FlowRun recovery: `80647dc2-848a-4150-842e-cc6947eed87c` (wave `wave2a`, root `sqx-main-v1-fc999000-98ee-4158-bc9a-931f85c68106`), runtime flota **0.2.130** 3/3, fan-out `max_parallel: 3` certificado (3 stages optimizer concurrentes desde 20:49:16Z, 1 sqcli por host). Root **COMPLETED 2026-09-29T08:54Z** (duración total ≈ 12h05m; 34 corridas optimizer batch=1 a 3 concurrentes).

## Accounting completo (toda pérdida explicada)

| Etapa | Entrada | Salida | Pérdida | Explicación |
|---|---|---|---|---|
| WAVE1Z FULL (producer, FlowRun `c329a546-…`) | 34 pasantes Precision | **34 outputs** | 0 | Cohort fuente congelado; outputs en MinIO `wave_wave1z/…/02_full_retester/` |
| RECOVERY HISTORICAL COHORT (`resolve_historical_cohort`) | 34 outputs wave1z | **34 resolved** | 0 | Sellado: `sqx.flow_run_strategies` = 34 memberships, 34 REPROCESSED, StrategyRefs == FULL-RECOVERY-INPUT.csv 1:1 |
| OPTIMIZER (`project@sqx-optimizer.v1`, batch=1, maxp=3) | 34 | **34 COMPLETED** | 0 | 0 FAILED/CANCELLED (funnel flowkit); outputs .sqx optimizados = 34 en MinIO `wave_wave2a/…/03_optimizer/`; matrices WF = 34 evaluations + **1836 celdas** (6 runs × 9 OOS por estrategia) en Mongo `forge.evaluations` |
| WFM (`evaluate_wfm@sqx-wfm.v1`) | 34 | **10 WARN, 24 FAIL** | 24 excluidas por veredicto | Razones: 16 × `NO_ACCEPTABLE_NEIGHBORHOOD` (0 picks — sin vecindad estable), 8 × `SEVERE_WARNING` (con picks pero veredicto FAIL ⇒ excluidas del robust por el gate verdict PASS/WARN); 1836 `wfm-cell-evaluation.v1` + 34 `wfm-aggregate-evaluation.v1` preservadas |
| ROBUST SELECTION (`select_robust_run@sqx-robust-selection.v1`) | 10 WARN | **10 SELECTED** | 0 | 10/10 `SELECTED` con razón `WFM_WARN_TOP_PICK` (selección intra-estrategia, policy vigente evaluate_wfm → select_robust_run; decisiones durables en PG `sqx.decisions` con `decision_ref` sha256) |

**Cobertura del requisito owner (≥10 candidates cuando existan):** las **1836 celdas completas del Optimizer** (todos los candidates reales de la matriz WF, sin corte) están exportadas en `OPTIMIZER-CANDIDATES.csv`; los picks WFM (46) en `picks.tsv`; ninguna etapa cortó a top-10.

## Robust selection — los 10 seleccionados (orden por robustness_score del top pick)

| # | Estrategia | Score | Sharpe (metric ranking) | Picks WFM | WFM mean global |
|---|---|---|---|---|---|
| 1 | Strategy_1.13.611 | 0.8868 | 1.14 | 3 | 7.57 |
| 2 | Strategy_2.41.524 | 0.8669 | 0.91 | 1 | 7.44 |
| 3 | Strategy_7.46.731 | 0.8664 | 1.30 | 3 | 11.12 |
| 4 | Strategy_3.31.576 | 0.8631 | 1.08 | 3 | 5.91 |
| 5 | Strategy_1.8.669 | 0.8595 | 1.35 | 3 | 12.31 |
| 6 | Strategy_2.76.686 | 0.8428 | 1.20 | 3 | 10.18 |
| 7 | Strategy_8.25.708 | 0.8363 | 0.95 | 1 | 5.84 |
| 8 | Strategy_2.75.621 | 0.8233 | 1.11 | 1 | 7.98 |
| 9 | Strategy_7.51.646 | 0.8112 | 1.23 | 3 | 9.07 |
| 10 | Strategy_2.17.581 | 0.7896 | 1.48 | 3 | 10.18 |

Detalle completo por candidata (cell_evaluation_ref, oos_percent, runs_count, robustness_score) y por decisión (decision_ref PG): `ROBUST-SELECTION-AUDIT.csv`.

## Desglose por TIPO LÓGICO (SelectionSnapshot C5.1 `sha256:5b4b441c…`, policy per_logical_type top_n=5 = 34 de 8 tipos)

| Tipo lógico (firma de indicadores) | Total | Pasaron WFM | Seleccionados |
|---|---|---|---|
| ATR,RANGE,TRUERANGE_CLOSE,HIGH,OPEN_ATR,RANGE,TRUERANGE | 5 | 3 | 3 (3.31.576, 8.25.708, 7.51.646) |
| ATR,BOLLINGERBANDS,RANGE,TRUERANGE_CLOSE,HIGH,OPEN_ATR,BB,RANGE,TRUERANGE | 5 | 2 | 2 (1.13.611, 1.8.669) |
| ATR,BOLLINGERBANDS,RANGE,TRUERANGE_CLOSE,OPEN_ATR,BB,RANGE,TRUERANGE | 5 | 2 | 2 (2.76.686, 2.75.621) |
| ATR,BOLLINGERBANDS,RANGE_CLOSE,OPEN_ATR,BB,RANGE | 5 | 2 | 2 (2.41.524, 2.17.581) |
| ATR,RANGE_CLOSE,HIGH,OPEN_ATR,RANGE | 5 | 1 | 1 (7.46.731) |
| ATR,KELTNER,RANGE,TRUERANGE_CLOSE,OPEN_ATR,KELTNER,RANGE,TRUERANGE | 5 | 0 | 0 — tipo eliminado por WFM |
| ATR,BOLLINGERBANDS,RANGE_CLOSE,HIGH,OPEN_ATR,BB,RANGE | 2 | 0 | 0 — tipo eliminado |
| ATR,BARRANGE,BOLLINGERBANDS,RANGE_CLOSE,OPEN_ATR,BARRANGE,BB,RANGE | 2 | 0 | 0 — tipo eliminado |

Nota: la selección top-5-por-tipo es la policy de **C5.1** (ya consumida para armar el cohort de 34). El `select_robust_run` de esta recovery es la policy vigente de selección **intra-estrategia** (evaluate_wfm → select_robust_run: 1 robust run por estrategia superviviente, el top pick del WFM) — no re-rankea entre estrategias ni por tipo.

## STOP — verificación

- MinIO `wave_wave2a/`: sólo `03_optimizer/` (34 .sqx), `04_wfm/`, `05_robust/` (sólo folder marker — decisiones durables en PG, no archivos) y `root/`. **No existen folders 06_/07_/08_/09_** (Final Retester, compile, backtest, MT5): ninguna ejecución post-select_robust_run.
- No se ejecutó `apply_selected_run`, promotion, ni Echo handoff.
- Funnel flowkit final: optimizer 34c/0f/0x · wfm 34c/0f/0x · robust-selection 10c/0f/0x, root COMPLETED sin error codes.

## Notas de auditabilidad

- 8 estrategias FAIL con picks WFM válidos quedan documentadas (wfm_picks en FUNNEL): material de comparación para el owner si decidiera relajar el gate de verdict — fuera de alcance de esta recovery.
- El fix de producto (0.2.130) NO fue necesario para esta recovery (camino `cohort_flow_run` canónico wave1u), pero el funnel Full→Optimizer intra-FlowRun ya queda operativo para las próximas campañas (probado por tests T1–T7 y el rollout 3/3 certificado).
- Los 10 seleccionados son **candidatos**; la decisión de avanzar a Final Retester/MT5 es del owner (STOP contractual respetado).
