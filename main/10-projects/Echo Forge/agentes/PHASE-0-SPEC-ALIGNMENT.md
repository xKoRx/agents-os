---
type: doc
schema_version: 1
status: active
phase: 0
gate: G0
created: 2026-07-23
updated: 2026-08-10
tags:
  - kind/doc
  - doc/spec-alignment
  - phase/0
  - gate/G0
  - area/echo
---

# Phase 0 — SPEC Alignment (Echo Forge, Etapa 4 closeout)

## Propósito

Conservar la trazabilidad documental de los cambios requeridos en las tres SPECs durante el closeout de Echo Forge Etapa 4; el estado de revisión continúa expresado por `gate: G0` y por el cuerpo.

## Contenido

> Documento complementario de `PHASE-0-CAPABILITY-REPORT.md`.
> Su objetivo es dejar trazabilidad de **qué cambia en las tres SPECs** y por
> qué, alineado con el registro `OD-M01..OD-M10`, `OD-A01..OD-A02` y con §3/§6/§7 del plan.
> El Gate G0 sigue siendo `review` hasta que el owner apruebe todo el paquete.

## 0. Convenciones heredadas

- `SQX_NATIVE`: valor entregado por SQX, autoridad canónica. No se recalcula
  silenciosamente.
- `DERIVED_VALIDATION`: cálculo Go cuando SQX no entrega algo comparable o
  para reconciliar. Persistir junto al nativo y el delta.
- `CUSTOM_RJARA`: fórmula / ventana aprobada por el owner. Se implementa
  sólo en Go, con `formula_version` y nunca atribuido a SQX.

## 1. FEAT-SQX-METRICS-CONTRACT — alineación

### 1.1 Tabla de cambios

| # | Cambio | Razón / OD / §6 / §7 |
|---|---|---|
| §3.1 | Documentar que el descriptor lleva `metrics_source_class ∈ {SQX_NATIVE, DERIVED_VALIDATION, CUSTOM_RJARA}` | OD del plan §3, línea "SQX_NATIVE autoridad" |
| §4.1 | Marcar métricas que **no** se emiten en `1.1.0` pero sí están en el catálogo: `trades` aparece con `num_trades` como alias; documentar `average_trade`/`r_expectancy` que el plugin emite y la SPEC no cataloga | §2.3 del plan / capability matrix §3.2 |
| §4.1 | Aclarar `trades` se conserva como nombre canónico y `num_trades` es alias histórico. Toda métrica nativa respeta autoridad SQX (`SQX_NATIVE`) | OD-M06, §7 |
| §4.2 | Subir a la SPEC la separación: `rr_ratio` actual de la SPEC mantiene su definición histórica sólo hasta que `rr_recent_max_win_loss_v1` esté cubierta por Phase ≥ 1; mientras tanto, marcar **deprecated** y requerir alias | OD-M01, §7.2 |
| §4.2 | Marcar `recovery_time_days`, `drawdown_duration_days`, `max_dd_recency_months` como `DERIVED_VALIDATION` (no nativos de SQX en este Build) | OD-M06, §7.4 |
| §4.2 | Marcar `monthly_performance` como `SQX_NATIVE` en su forma canónica; variante agregada desde trade-list es `DERIVED_VALIDATION` | §7 |
| §8 (NEED-INFO) | `NI-MC-1` se cierra por F0: las métricas que el plugin Overview v1.1.0 entrega están documentadas (ver capability matrix). Las que no, queda registrado `nullable` y se confirma `DERIVED_VALIDATION` para los cálculos Go | §7, capability matrix §3.2 |

### 1.2 Patch proposto (extracto)

```diff
@@ Modelo Conceptual §3.1
- cada métrica del catálogo se describe con los siguientes atributos conceptuales:
+ cada métrica del catálogo se describe con los siguientes atributos conceptuales:
+ Para Eco Forge la métrica lleva, además, `metrics_source_class ∈ {SQX_NATIVE, DERIVED_VALIDATION, CUSTOM_RJARA}`
+ que indica la autoridad semántica y quién la calcula.

@@ §4.1 Métricas core SQX (origen sqx_plugin)
- | `trades` | count | range_target | … | hard_filter | Número de operaciones cerradas. …
+ | `trades` (`num_trades` en plugin v1.1.0) | count | range_target | … | hard_filter | Número de operaciones cerradas. …
+ | `average_trade` | currency | higher | … | informational | Ganancia media por trade (alias histórico del plugin; se documenta por compatibilidad, no como principal). Marcada `metrics_source_class=SQX_NATIVE` si SQX la expone; en caso contrario `DERIVED_VALIDATION` desde trade-list. |
+ | `r_expectancy` | ratio | higher | … | informational | R-expectancy entregado por SQX; alias histórico adicional. Se mantiene por compatibilidad con plugins v1.1.0; la SPEC introduce `expectancy` como canónico. |
+ 
+ > Nota de Phase 0 (Gate G0): la matriz de capabilities en `phase0/capability_matrix.json`
+ > confirma que `num_trades` (no `trades`) es lo que el plugin Overview v1.1.0 emite hoy.
+ > La diferencia es de nomenclatura, no de semántica. La autoridad sigue siendo SQX.

@@ §4.2 Métricas de evaluación profunda
- | `rr_ratio` | ratio | higher | evaluation, robust_run_setup | score_input | R:R = máximo profit de un trade / máxima pérdida de un trade (valores absolutos, desde trade list). |
+ | `rr_ratio` | ratio | higher | evaluation, robust_run_setup | score_input | **DEPRECATED** desde 2026-07-23. Se conserva para documentos históricos. La métrica activa para esa ventana es `rr_recent_max_win_loss_v1` (CUSTOM_RJARA), introducida en la Fase 1 y diseñada contra los últimos 12 meses operativos del FULL (OD-M01/OD-M02). |
+ | `recovery_time_days` | days | lower | evaluation | soft_warning | **DERIVED_VALIDATION**: SQX no expone curva intratrade en este Build; se reconstruye desde trade-list por `TradeListImporter`. |
+ | `drawdown_duration_days` | days | lower | evaluation | soft_warning | **DERIVED_VALIDATION**, idem. |
+ | `max_dd_recency_months` | months | higher | evaluation | soft_warning | **DERIVED_VALIDATION**, idem. |

@@ §8 NEED-INFO
- 1. **NI-MC-1**: Confirmar qué métricas de §4.1/§4.2 expone realmente la API interna de SQX Build 142 al plugin (depende del spike de FEAT-SQX-JAVA-EXPORTER-PLUGIN). Las que no estén disponibles pasan a `internal_calc` desde trade list o quedan `nullable`.
+ 1. **NI-MC-1 — CERRADO en Phase 0 (Gate G0)**: capability matrix `phase0/capability_matrix.json` lista
+    la separación real entre lo que emite el plugin Overview v1.1.0 (Build 142.2399) y lo que el catálogo
+    declara. `trades ↔ num_trades` queda alias; `average_trade`/`r_expectancy` se documentan por
+    compatibilidad; las restantes (`trades`, `monthly_performance`, `recovery_*`, `drawdown_duration_*`,
+    `max_dd_recency_months`, `mae`, `mfe`, `native_equity`, `stagnation`) quedan `nullable` y/o
+    `DERIVED_VALIDATION` desde trade-list, con matriz publicada en capability_matrix.json.
```

## 2. FEAT-SQX-STRATEGY-EVALUATION — alineación

### 2.1 Tabla de cambios

| # | Cambio | Razón / OD / §6 / §7 |
|---|---|---|
| §4.2 | Sustituir `rr_ratio` por la nueva lista `rr_recent_max_win_loss_v1` (CUSTOM_RJARA) más la reconciliación derivada `win_rate_derived`, `profit_factor_derived`; persiste `sqx_value/derived_value/delta_abs/delta_pct/status` para no pisar SQX | OD-M01/OD-M02/OD-M06, §7.2/§7.3 |
| §4.2 | Sustituir la regla actual de "mes negativo dominante" por la métrica `negative_year_coverage_ratio_v1` y su warning POC `deep.negative_year.not_covered.v1`. La regla histórica `neg_month_dominant_v1` se deprecada | §7.6 / OD-M10 |
| §4.2 | Añadir `max_losing_month_streak_v1`, `losing_streak_recovery_months_v1`, `losing_streak_recovery_speed_v1`, con clasificación `FAST/ACCEPTABLE/SLOW/UNRECOVERED` y warnings POC `deep.recovery.slow.v1`, `deep.recovery.unrecovered.v1` | OD-M03, §7.5 |
| §4.3 | Veredicto se mantiene `PASS/PASS_WITH_WARNINGS/DISCARDED`; para Fase 4 se introduce un `evaluation_mode ∈ {off, shadow, warn, enforce}` (Plan §11 "Flags") y `ruleset_version` | §11 |
| §4.3 | Sustituir `EvaluationResult.warning_score` por `warning_count_by_severity` mientras `evaluation_mode=shadow`/`warn`; `warning_score` sólo se reintroduce cuando el owner apruebe un ruleset con `parameter_set_id` propio (OD-M10) | §7.10 |
| §5 | Política de selección con `evaluated_at = UTC`, `wave_key/strategy_id/stage` siempre presentes; **no** fusionar deep warnings con `WFMEvaluation.Warnings` (vive en colección separada: `strategy_evaluations.deep_warnings`). Shadow no modifica selected run | §7.10 / OD-M10 |
| §9 | Riesgo "doble registro WFM/evaluación": añadir que F5 usa `warning_id` determinista; el agregado de PWshadow wFM vive separado y se une por evaluation only para reporte | OD-M10 |

### 2.2 Patch proposto (extracto)

```diff
@@ §4.2 Cálculos obligatorios
- `rr_ratio`, `win_rate`, `ret_dd`, `profit_factor`, `sharpe_ratio`, `sqn_score`, `cagr`, `expectancy`,
- `monthly_performance` (agregaciones anuales: mejor/peor mes), `recovery_time_days`,
- `drawdown_duration_days`, `max_dd_recency_months`, comparación equity base vs optimizada
- (deltas de `ret_dd`, `net_profit`, `drawdown`).
+ Métricas activas tras Phase 0:
+ - Nativas (`SQX_NATIVE`): `ret_dd`, `profit_factor`, `sharpe_ratio`, `sqn_score`, `cagr`, `expectancy`,
+   `win_rate`, `trades`/`num_trades`, `average_trade`, `r_expectancy`, `stagnation` (si Build 142 la expone).
+ - Derivadas (`DERIVED_VALIDATION`): `closed_trade_equity_curve`, `max_closed_trade_drawdown`,
+   `monthly_performance_utc` (reconciliación), `win_rate_derived`, `profit_factor_derived`.
+ - Custom rjara (`CUSTOM_RJARA`): `rr_recent_max_win_loss_v1`, `max_losing_month_streak_v1`,
+   `losing_streak_recovery_months_v1`, `losing_streak_recovery_speed_v1`,
+   `negative_year_coverage_ratio_v1`, `best_month_covers_negative_year_v1`,
+   `optimized_vs_baseline_*` (deltas + `risk_adjusted_delta.v1`).
+ Comparación base (`retest_full`) vs optimizada: misma estrategia + misma intersección temporal +
+ mismo `pnl_basis` (`net_after_commission_swap`) + mismo `sample_type`; en otro caso,
+ `not_comparable`.

@@ §4.3 Veredicto
  EvaluationResult {
   wave_key, strategy_id, stage="evaluation",
-  verdict        // PASS | PASS_WITH_WARNINGS | DISCARDED
+  verdict        // PASS | PASS_WITH_WARNINGS | DISCARDED
+  evaluation_mode=shadow   // Phase 4 introduce el flag shadow/warn/enforce
+  ruleset_version=deep_warnings_shadow.v1
   metrics        // MetricValues calculadas (catálogo + metrics_catalog_version)
-  warnings[]     // modelo §3
-  warning_score  // Σ pesos
+  warnings[]     // modelo §3 (sólo PWshadow wFM si provenien de deep_evaluation, §7.10)
+  deep_warnings[] // rjara shadow: viven aparte del shadow, no entran a `warning_score` durante POC
+  warning_count_by_severity { INFO, WARN, CRITICAL }
   severe_count, warn_count, info_count
   rules_applied[] // rule_ids + parámetros efectivos (trazabilidad)
   evaluated_at
  }

@@ §3.3 reglas
- | `rr_ratio_low_v1` | trade_profile | WARN | `rr_ratio < umbral` |
- | `neg_month_dominant_v1` | seasonality | WARN | en algún año: `|peor mes| > mejor mes` |
+ | `rr_ratio_low_v1` | trade_profile | WARN | `rr_recent_max_win_loss_v1 < umbral` (sólo activa cuando F1+F4 cierren el gate del threshold; sin threshold POC) |
+ | `neg_month_dominant_v1` | seasonality | **DEPRECATED** | sustituida por `negative_year_coverage_ratio_v1` (§7.6) + warning POC `deep.negative_year.not_covered.v1` |
+ | `losing_month_streak_slow_v1` | drawdown_profile | WARN | activo cuando `recovery_class = SLOW` |
+ | `losing_month_streak_unrecovered_v1` | drawdown_profile | CRITICAL | activo cuando `recovery_class = UNRECOVERED` |
+ | `deep.curve.algorithm_degraded_v1` | equity_quality | WARN (POC) | activo cuando el CurveComparisonAlgorithm configurado emite degradación material; threshold/parameter_set calibrados en §7.7. POC no emitir hasta F5. |
```

## 3. FEAT-SQX-JAVA-EXPORTER-PLUGIN — alineación

### 3.1 Tabla de cambios

| # | Cambio | Razón / OD / §6 / §7 |
|---|---|---|
| §3.2 | Fijar el registro objetivo de cinco proyectos SQX independientes: Overview, WFM, TradeList, MT5 y RobustRun; `EchoForgeAutomator` queda deprecado. La definición dinámica del flujo elige proyecto, source/input y orden; no hay host ni secuencia hardcodeada para TradeList | `OD-A01`, `OD-A02`, §4, §6, §8.3 |
| §3.3 | Reescribir `trade_lists` para que coincida con el contrato v1 del plan §6.2: `trade_index`, `trade_key`, `entry_time_utc`, `exit_time_utc`, `entry_price`, `exit_price`, `direction`, `gross_profit`, `net_profit`, `commission`, `swap`, `pnl_basis`, `instrument`, `timeframe`, `source_timezone`, `duration_seconds`, `mae`, `mfe`, `labels`. **Borrar** el campo `trades[]` antiguo y el summary inline. La contraparte resumen (count, max_profit, max_loss, etc.) se mueve a una `manifest`. | §6.2, OD-M07 |
| §3.3 | Añadir `trade-manifest.v1.0.0` con `wave_key, request_id, run_id, strategy_id, stage, variant, result_key, cell_key, sample_type, period_start/end_utc, trade_count, closed_trade_count, source_order_count, artifact{sha256, bytes}, capabilities{...}, status, errors[]` | §6.3, OD-M08, OD-M09 |
| §4 | Añadir regla de "operaciones cerradas, no legs": `EchoForgeTradeListExporter` debe reconciliar `orders() ≠ trades` antes de aceptar cardinalidad | §3, OD-M06, capability report §2.5 |
| §4 | Añadir regla "samples separados, no sumar": ningún exporter puede agregar `IS + OOS` y llamarlo `Full`. Sólo se acepta `Full` si SQX lo emite explícitamente | §3, §6.3, OD-M09 |
| §4 | Añadir regla sobre portfolio: componente debe ser identificable (`component_strategy_id` o equivalente); sin eso se rechaza como `unsupported_portfolio_identity` | §6.3, OD-M08 |
| §5.3 | Configuración local efímera: añadir nota de que la sección `trade_export.*` no se activa hasta G2; sin campos en plugin para F0. Evitar tocar `exporter.properties` de `EchoForge*` durante F0/F1 | §8.1.1, §8.3 |
| §7 | Non-goal: añadir "no emitir `_SUCCESS` sin manifest+checksum válidos" (F2) | §6.3, §11 |
| §7 | Non-goal: "operaciones cerradas, no orders genéricos; nunca aceptar `order`, `deal` o leg como trade cerrado sin reconciliar" | §3, OD-M06 |
| §9 | Riesgo: nueva entrada para "Plugin heurístico Overview cuenta `TakeProfit`/`StopLoss` como profit-like; F1+T2 lo corrige con extractor dedicado" | §7 del plan |

### 3.2 Patch proposto (extracto)

```diff
@@ §3.2 Mapping stage → exporters / acciones
- | `robust_run_setup` | Acción `EchoForgeAutomator` (aplica los parámetros del run robusto y magic number) + TradeListExporter (escribe `trade_lists` del run seleccionado) |
+ | task `project` con `project=EchoForgeRobustRunExporter` | aplica parámetros del run robusto y Magic Number usando source/input explícito |
+ | task `project` con `project=EchoForgeTradeListExporter` | exporta operaciones cerradas desde source/input explícito conforme a la matriz de contexts aceptada en G0 |
+ > Registro objetivo de proyectos fijos: `EchoForgeOverviewExporter`, `EchoForgeWFMExporter`, `EchoForgeTradeListExporter`, `EchoForgeMT5Exporter`, `EchoForgeRobustRunExporter`. `EchoForgeAutomator` está deprecado y no es fallback.
+ > El flujo puede elegir, omitir y ordenar estas piezas mediante configuración; compartir `TradeExtractionService` no fusiona proyectos ni lifecycle.
+ > El proyecto TradeList dedicado (Fase 2) reemplaza la heurística reflexiva del Overview; `trades_debug.ndjson` continúa como diagnóstico, no contrato.

@@ §3.3 trade_lists (TradeListExporter)
- **trade_lists** (TradeListExporter) — un documento por {wave_key, strategy_id, stage}:
- - wave_key, strategy_id, stage, schema_version, exported_at;
- - trades[]: {seq, open_time_utc, close_time_utc, direction (LONG|SHORT), volume,
-   open_price, close_price, profit, commission_estimate, duration_minutes};
- - summary: {count, max_profit_trade, max_loss_trade, gross_profit, gross_loss}
-   (insumo directo de rr_ratio y evaluación profunda).
+ **trade_lists** (EchoForgeTradeListExporter) — NDJSON + manifest v1 (Plan §6.2/§6.3):
+ Línea NDJSON (un trade por línea) con:
+   schema_version, wave_key, request_id, run_id, strategy_id, stage, variant,
+   result_key, cell_key, sample_type, trade_index, trade_key,
+   entry_time_utc, exit_time_utc, entry_price, exit_price, direction,
+   gross_profit, net_profit, commission, swap, pnl_basis,
+   instrument, timeframe, source_timezone, duration_seconds,
+   mae, mfe, labels.
+ Manifest (un archivo por scope {wave, request, run, strategy, stage, variant, result, cell, sample}):
+   schema_version, plugin_version, metrics_catalog_version, scope completo,
+   period_start_utc, period_end_utc, trade_count, closed_trade_count,
+   source_order_count,
+   artifact{content_type=application/x-ndjson, content_encoding=gzip,
+            sha256, compressed_bytes, uncompressed_bytes},
+   capabilities{net_profit, gross_profit, commission, swap, mae, mfe,
+                native_equity_curve},
+   status ∈ {complete, partial, failed}, errors[].
+ Timestamps normalizados a UTC indicando zone horaria origen (source_timezone).
```

## 4. Reglas comunes que las tres SPECs deben seguir tras la alineación

1. **Toda métrica nativa** se trata como autoridad SQX; cualquier cálculo paralelo
   se persiste como `DERIVED_VALIDATION` con su delta explícito. No hay overwrite.
2. **Custom rjara** nunca se atribuye a SQX. Lleva `formula_version` y se nombra con
   versiones (`*_v1`).
3. **Samples separados**: `FULL`, `IS`, `OOS` no se fusionan. `FUTURE` es audit-only
   (no entra a evaluación ni selección).
4. **Portfolio**: componente identificable es obligatorio; sin eso, `unsupported_portfolio_identity`.
5. **Shadow no cambia decisión legacy**: mientras `evaluation_mode ∈ {off, shadow, warn}`,
   la decisión de selección robusta es la del selector legacy.

## 5. Estado del Gate G0 después de la alineación

- G0 = `review`: el paquete completo (este anexo + capability report + fixtures firmadas)
  está entregado. El owner es el único que lo cambia a `accepted` o `rejected`.
- F1 no inicia hasta que G0 = `accepted`.
