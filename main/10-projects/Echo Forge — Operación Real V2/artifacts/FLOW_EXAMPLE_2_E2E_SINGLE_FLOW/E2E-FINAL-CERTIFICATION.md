# E2E-FINAL-CERTIFICATION — FLOW_EXAMPLE_2 (SQX 144 · NDX · FLUJO ÚNICO · 2026-10-17)

## Veredicto

**FLOW_EXAMPLE_2_E2E_PASS** — un único `config.json` con UN único `GenericSQXWorkflow` raíz ejecutó físicamente TODAS las etapas del mandato (Builder → Overview → Classification → Early Ranking → Selection → GROUP interno con source `ranking_snapshot` → Apply → Final Reretester → TradeList/Report → MQ5 → EX5 → MT5 → Fidelity → Ranking final → Promoción), con `FlowRun` terminal **COMPLETED** sellado en el registro durable. Sin integración Echo (cero ingress, cero deployments, cero órdenes).

- **FlowRun**: `8248f7fa-e3bd-45e4-b0de-66dcfcd564db` (wave 9, cfgID `NDX_flow_example_2_v1_w9`)
- **WorkflowID**: `sqx-main-v1-b7f29b77-3e82-4ed7-baaa-fd3a35cd07d2` (namespace Temporal `sqx-prop`, cola `sqx-main-queue`)
- **T0**: 2026-10-17T02:07:41Z · **sello COMPLETED**: 2026-10-17T04:17:11Z · **duración total: 2h09m30s**
- **Spec**: `CONFIG-E2E-SINGLE-FLOW.json` — SPEC_VALID `runtime.ValidateWorkflowSpec` (11 tasks), CFX del Owner byte-exactos (SHA256 4/4 contra `C:\Users\KoR\Desktop\SQX144\user\configs\basetest`)

## Historia de la prueba (transparencia completa)

El intento w8 (FlowRun `c6a18689`, 2026-10-16T22:43Z) ejecutó el pipeline físico completo hasta MT5 30/30 y **falló no-retryable en `mt5_score_shadow_v1`** (fidelidad): `normalized trade scope mismatch: contract_conflict`. Causa raíz: `CanonicalSymbol` no tenía el alias `usatechidxusd_dukascopy_utc02` del dataset del Owner. Fix mínimo `b77af11` (+1 alias exacto UTC02, fila negativa UTC03, regresión), release **0.2.147** (`0e4c9908…`), rollout 3/3 verificado por MCP (proceso+SHA byte-exacto en Zeus/Hera/Kronos). Un reset Temporal del workflow w8 probó que el score pasaba con el fix, pero el sello `flow_run_seal` rechazó FAILED→COMPLETED (transición terminal, contrato correcto) — el "continuar" del §7 se materializó como re-despacho del MISMO flujo único con identidad nueva (w9). w8 queda documentado como intento con defecto corregido; ningún resultado de w8 se usa como sustituto de w9.

## Cadena físicamente certificada (w9)

| # | Etapa | Evidencia durable | Ventana UTC |
|---|---|---|---|
| 1 | Builder (CFX owner intacto) | stage `project@sqx-overview.v2` 1/1; 760 generadas; export inyectado 745 escritas / 0 errores; Zeus | 02:07:41→02:34:52 (27m11s) |
| 2 | Overview / Metadata | overview.ndjson + monthly.ndjson (wave_9) + proceso físico `EchoForgeOverviewExporter` observado 02:44-02:52 | ~8m |
| 3 | Classification `indicator_signature.v1` | ClassificationSnapshot `sha256:161bfd25…` (flow 8248f7fa) | 02:34:5x |
| 4 | Early Ranking `weighted_combination_minmax.v1` DD40/PF30/SH30 | 7→6 RankingSnapshots PER_LOGICAL_TYPE (una por tipo real del cohort) | 02:34:54 |
| 5 | Selection `per_logical_type` top5 | **SelectionSnapshot `sha256:d15af7f9…` 30 seleccionadas, 729 exclusiones RANK_BEYOND_TOP_N** | 02:34:55 |
| 6 | GROUP interno `source.type=ranking_snapshot` | routing por partición lógica, children `GroupSQXWorkflow` batch 1 | 02:34:55 |
| 7 | Retester ×30 | stage rows `project@sqx-retester.v1` **30/30 COMPLETED** | 02:34:55→03:06:52 |
| 8 | Optimizer ×30 (1 upstream c/u, WF_Matrix) | stage rows **30/30** | 02:37:06→03:08:26 |
| 9 | Evaluate WFM ×30 (robust_run_selection_v2 0.35/0.01/0.01) | stage rows **30/30** | 02:38:18→03:09:50 |
| 10 | Robust Selection V2 ×30 | PG `sqx.decisions`: **30 OPTIMIZER_SELECTION SELECTED** con DecisionRef sha256 | 03:09:50 |
| 11 | Apply (mágica durable) | stage rows **30/30**; `sqx.strategy_magic` 26100091054..26100091083 (autoridad durable V1; el 888111 solicitado no overridea) | 03:09:50→03:13:42 |
| 12 | Final Reretester Full Precision 2026.01.01→2026.10.12 precision 2 | stage rows **30/30** | 03:13:43→03:17:47 |
| 13 | TradeList + Report | MinIO `durable/trade-list/v1/8248f7fa/` (30 TradeSets COMPLETE) + metadata report | ~03:2x |
| 14 | MQ5 export | MinIO `durable/mt5-export/v1/8248f7fa/<uuid>` 30 keys | ~03:2x |
| 15 | EX5 compile (MetaEditor real) | stage rows `mt5_compiler` **30/30**, 0 errores | 03:29:26→03:29:32 (+persist) |
| 16 | MT5 backtest ×30 NDX_SQX H1 model 4 | stage rows `mt5_backtesting` **30/30**; `terminal64.exe` serial en worker-kronos | 03:30→04:16 (~46m físicas) |
| 17 | Fidelity `mt5_fidelity_shadow.v1` (fórmula intacta) | Mongo `scores` mt5-score.v1 **30 docs COMPUTED** + baseline materialize 30/30 | 04:16:59→04:17:08 |
| 18 | Ranking final `score_descending.v1` | RankingSnapshot **`sha256:de770a6d…`** con 30 `ordered_entries` (rank+score_ref+strategy_ref) | 04:17:09 |
| 19 | Resultado por tipo lógico (máx 5) | `FINALISTS-BY-LOGICAL-TYPE.csv` — proyección EXACTA desde el ranking durable + SelectionSnapshot; 6 tipos × ≤5 | — |
| 20 | Promoción `finalist_promotion 2.0.0` | PG decision FLOW **STRUCTURAL_PROMOTED 04:17:09.095Z** + stage `promote_finalists` 1/1 | 04:17:09 |
| 21 | Sello terminal | **PG `sqx.flow_runs` status=COMPLETED** (updated 04:17:11.877Z) | 04:17:11 |

## Resultado final por tipo lógico (6 tipos reales, 5 finalistas c/u — proyección read-only exacta del ranking durable)

Corregido en reconciliación final 2026-10-17 (contraste contra el CSV durable, ver §Corrección de cifras): **16/30 finalistas con CERO trades MT5, 14/30 con trades y 0/30 con beneficio MT5 positivo** (los 14 net_profit MT5 con trades son negativos). La versión inicial de esta tabla afirmaba 5/5 trades en todos los grupos — dato erróneo, corregido sin tocar el CSV.

| logical_type | n | mejor fidelidad | finalistas con trades MT5 > 0 |
|---|---|---|---|
| RANGE_CLOSE,HIGH,LOW,OPEN_RANGE | 5 | **66.89** | 5/5 |
| RANGE_CLOSE,HIGH,LOW_RANGE | 5 | 48.51 | 4/5 |
| RANGE_CLOSE,LOW,OPEN_RANGE | 5 | **83.76** | 4/5 |
| RANGE_CLOSE,LOW_RANGE | 5 | 0.0 | 0/5 |
| RANGE_CLOSE,OPEN_RANGE | 5 | 0.0 | 0/5 |
| RANGE_CLOSE_RANGE | 5 | 1.91 | 1/5 |
| **total** | **30** | — | **14/30** |

Detalle completo (final_rank, StrategyRef, canonical_id, mágica, ScoreRef, fidelidad, SQX net_profit/trades vs MT5 net_profit/trades, DecisionRef) en `FINALISTS-BY-LOGICAL-TYPE.csv`. Los 16 finalistas con 0 trades MT5 tienen fidelidad 0.0 por definición de `mt5_fidelity_shadow.v1` (sin candidato comparable). La selección final por tipo se materializa como proyección read-only del RankingSnapshot `sha256:de770a6d…` agrupado por la clasificación del SelectionSnapshot `sha256:d15af7f9…`; la decisión durable de promoción existente es la FLOW-level `finalist_promotion 2.0.0` — no se inventan PromotionDecisionRefs adicionales.

## Alcance: tres planos distintos (no intercambiables)

- **Certificación técnica E2E = PASS.** Certifica que el pipeline físico (21 etapas, 30/30 en las particionadas) ejecutó de punta a punta con FlowRun terminal COMPLETED. No certifica calidad ni rentabilidad de las estrategias producidas.
- **Promoción estructural = EXECUTED.** La decisión durable `FINALIST_PROMOTION` (decision_ref `sha256:082447fa36ffd26f093bb41225d12c13e07aa715c63e04a4595bc2a7de92fd90`, outcome=COMPLETED, mode=ENFORCE, reasons=["STRUCTURAL_PROMOTED"], 04:17:09.095Z) selló 30 StrategyVersions (target_platform=MetaTrader5) y 30 handoff manifests y dejó 30 delivery records. Es estructural: no valida operación rentable.
- **Viabilidad operativa de las estrategias = NO CERTIFICADA.** 16/30 sin trades MT5 en la ventana 2026.01.01→2026.10.12, 14/30 con trades pero net_profit MT5 negativo, 0 con beneficio positivo. Ninguna finalista demuestra hoy rentabilidad MT5; esa evaluación es trabajo futuro del owner, no parte de este veredicto.

## Top-5 por tipo: proyección read-only, no decisión durable

Verificado en control plane (2026-10-17): `sqx.decisions` contiene exactamente 1 decisión `FINALIST_PROMOTION` (FLOW-level) + 30 `OPTIMIZER_SELECTION`; `sqx.forge_campaign_finalists` tiene 0 filas para este flow. No existe decisión durable per-type: el Top-5 por tipo es una proyección read-only del ranking global `sha256:de770a6d…` agrupado por tipo, reproducible desde los snapshots durables.

## Corrección de cifras y PRE_ECHO (reconciliación final 2026-10-17, read-only)

- La versión original de este informe afirmaba "5/5" trades MT5 en los 6 grupos y "forge_seal_handoff: ZERO". Ambas afirmaciones eran erróneas y quedan corregidas aquí; el CSV, scores y decisiones originales NO fueron modificados.
- **forge_seal_handoff_v1 SÍ se ejecutó**: historia Temporal del wf raíz (run `01a1479d-6a50-787a-8229-c204f3236e67`, 2027 eventos, status Completed) muestra la secuencia `promote_finalists` (eventos 2008–2010) → `forge_seal_handoff_v1` (2014–2016, COMPLETED) → `flow_run_seal` (2020–2022) → WorkflowExecutionCompleted.
- **Control plane del sello (PG trading_systems_test, esquema sqx):** 30 `strategy_versions` selladas (30 canonical ids, target_platform=MetaTrader5); 30 `handoff_manifests` creados 04:17Z por w9 (+30 creados 02:02Z por el reset diagnóstico de w8 sobre los mismos strategy_ref, sin delivery rows — artefacto durable del intento, no del FlowRun certificado); 30 `handoff_deliveries` en estado `HANDOFF_CREATED`, attempts=2, `last_error="echo ingest base url / bearer not configured: echo ingest ingress fail-closed: ingress_not_configured"` (04:17:09.3–0.7Z).
- **Entrega real a Echo = CERO, corroborada en ambos lados:** ningún delivery superó `HANDOFF_CREATED`, y lectura RO en la BD de Echo PROD muestra 0 `strategy_versions` con esos 30 version_ref y 0 `promotion_records` (total histórico 0).
- Mongo `forge.scores`: 30 docs `mt5-score.v1` COMPUTED @ 04:17:08Z (fidelidades del CSV).
- EchoDeployments: ZERO · TradingOrders: ZERO.

## Rechazos legítimos registrados

- 729 estrategias excluidas por `RANK_BEYOND_TOP_N` en la selección (listadas con rank en el SelectionSnapshot).
- Cohort builder: 760 generadas → 745 aceptadas al databank → 30 seleccionadas (top5 × 6 tipos; ningún tipo aportó más de 5).
- Mágica solicitada 888111 ≠ autoridad durable (2610009105x): comportamiento contractual certificado de `apply_selected_run` durable (la TaskSpec magic nunca overridea la asignación).

## Baseline y release

- Repo `xKoRx/symphony` HEAD al despachar: `69a6cd7` (manifest 0.2.147; fix `b77af11` incluido); release efectiva en flota **0.2.147** SHA `0e4c9908fe428b65a60261a6a059ae43b6be984679d18e3e5cd140a8a18eb684` 3/3 hosts (proceso + SHA verificados por SSH MCP).
- Workers: Zeus/Hera/Kronos (SQX 144.2953, `sqcli` vía wrapper JVM) + worker-kronos Windows (`sqx-mt5-worker`) para MQ5/EX5/MT5.
- Watcher candidate-local único en Daedalus, `ENV=production` (0 apariciones de scope development en logs), namespace `sqx-prop` (ETCD `/sqx-watcher/production/temporal/namespace`), cola `sqx-main-queue`, sin sqcli residuales pre-despacho.

## Límites declarados

- La etapa Overview usa el productor durable del builder (overview.ndjson/monthly.ndjson del CustomAnalysis inyectado) y además el exporter explícitobrownfield (sin stage row por contrato; evidencia por proceso físico y artefactos MinIO).
- Los backtests MT5 corren serializados en worker-kronos según contrato certificado; el stage row `mt5_backtesting` se sella al cierre del fan-out (la ventana del row 04:16:59→04:17:08 es bookkeeping; el span físico observado es 03:30→04:16).
- w8 (`c6a18689`) y sus docs de score del reset (02:02:40Z) quedan como evidencia del intento con defecto; NO forman parte del veredicto PASS.
