---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related: []
aliases: []
tags:
  - kind/doc
created: "2026-09-24"
updated: "2026-09-24"
---
related:
  - "[[Echo — Producto Integrado]]"
  - "[[D — Revised Roadmap]]"
  - "[[A — Product Contract — The Lab]]"
  - "[[F — Decision Register]]"
  - "[[O — D1 Closure and D2 Handoff]]"
aliases:
  - D3 technical SPEC
  - SPEC D3
tags:
  - kind/doc
  - area/echo
  - the-lab
  - d3
---

# A — Technical SPEC D3 — First Analytical Experience

## 0. Autoridad y alcance

SPEC congelada de Fase 3 de The Lab V3 (Shot 1 implementation candidate, 2026-09-24). Implementa las decisiones F1–F18 del mandato del owner, el contrato de producto [[A — Product Contract — The Lab]], las decisiones D1-M01..M12 de [[F — Decision Register]] y hereda la implementación física certificada de D1 (baseline `xKoRx/echo master@8adce7ec98fc20517950635537e515e07c931144`).

D3 consume exclusivamente `StrategyVersion + canonical operations + A/B`. Forge queda fuera (`FORGE_DUAL_HISTORY_INTEGRATION = PENDING`); `trade_journal` no se toca; no existe segunda autoridad analítica.

## 1. Invariante central

Las operaciones canónicas son la única autoridad. Las curvas son materializaciones DERIVADAS y reconstruibles: `Canonical Operations → Curve Algorithm → Curve Result → Curve Points → Metrics`. Una curva stale se recalcula; sin event sourcing, sin historial de ejecuciones, sin segunda trade store.

## 2. Engine (v3/sdk/analytics/curve)

`CurveAlgorithm { Describe() / Validate(in) / Calculate(ctx, in) }`, in-process, registrado por `algorithm_id` + `algorithm_version` + `configuration` en código (sin plugins/DSL/scripting/Kafka/Temporal/microservicio). Agregar un algoritmo no modifica el core: se implementa la interfaz y se registra.

- **Input explícito:** `Head` (proyección de `echo.strategy_history_state`: instrumento, A = `training_end_at` exclusivo, `training_timezone`, B = `live_start_at` nullable, `history_digest`) + `[]Operation` (proyección económica de `echo.canonical_operations`, decimales canónicos string).
- **Determinismo:** orden canónico D1 `(opened_at, closed_at, source_trade_id)`; el orden del input es irrelevante. Aritmética exacta `big.Rat`; única cuantización al renderizar con la primitiva A0 `formulas.DecimalString` (half-even 12dp). `dataset_digest` = receta D1 `HistoryDatasetDigest` sobre los `record_digest` consumidos; `result_digest` = `wire.HashTagged("lab-curve-result.v1", …)` sobre identidad+dataset+estado+puntos+métricas.
- **Identidad de curva:** `(registry_namespace, strategy_version_ref, algorithm_id, algorithm_version, config_digest)`; `ConfigDigest = H("lab-curve-config.v1", JSON canónico)`. Config distinto ⇒ curva distinto.
- **Períodos:** pertenencia por `source` + `opened_at` contra A/B: SQX `< A` ⇒ `TRAINING_DATA`; MT5 `[A,B)` (o `≥ A` si B pendiente) ⇒ `PRE_REAL`; REFERENCE `≥ B` ⇒ `REAL`. `closed_at` sólo posiciona el punto en el tiempo. Contradicción con el head ⇒ estado `ERROR` (fail-closed, jamás reclasificar).
- **Estados:** curva `READY | INSUFFICIENT_DATA | ERROR`; métricas además `UNKNOWN`. `INSUFFICIENT_DATA` honesto (F6): R_MONEY sin `initial_risk_money` en TODAS las ops ⇒ insuficiente; MONEY con monedas mixtas ⇒ insuficiente (sin conversión inventada); R_PIPS sin especificación de instrumento probada ⇒ insuficiente con arquitectura preparada.

## 3. Algoritmos mínimos del día (v1)

| algorithm_id | basis | unit | fórmula | requisitos |
|---|---|---|---|---|
| `rmoney_cumulative` | R_MONEY | R | `R_i = net_pnl_i / initial_risk_money_i`; `value_t = Σ R_i` | `initial_risk_money > 0` en todas las ops |
| `money_cumulative` | MONEY | moneda del dataset | `value_t = Σ net_pnl_i` | moneda única declarada |
| `rpips_cumulative` | R_PIPS | R | declarado, no implementado | spec de pip probada (no existe en V3) ⇒ INSUFFICIENT_DATA |

## 4. Métricas mínimas (formula_version v1, window FULL)

`total_return`, `max_drawdown`, `current_drawdown`, `return_over_dd`, `profit_factor`, `win_rate`, `expectancy` sobre las contribuciones de la curva (basis coherente); `operation_count` y `coverage` con basis factual `CLOSED_OPERATIONS`. Cada métrica persiste `formula_id/formula_version/basis/unit/window/status`. `NULL` jamás equivale a `0`; los únicos ceros admitidos son ceros reales computados (p.ej. drawdown 0 en curva monótona, coverage 0 con datos). `return_over_dd` con maxDD=0 y `profit_factor` sin losses ⇒ `INSUFFICIENT_DATA` (no ∞ ni 0).

## 5. Persistencia (migración 065, additive)

- `echo.lab_curves`: header de la materialización ACTUAL por identidad (UNIQUE ns+ref+algo+versión+config). Conserva StrategyVersion identity, algorithm id/version, basis, unit, currency, `config_digest`+`config_json`, status+reason, instrumento, A/B, `history_digest`, `dataset_digest`, `operation_count`, `points_count`, `result_digest`, `computed_at`. Sin historial de ejecuciones.
- `echo.lab_curve_points`: `(curve_id, seq)` PK; `event_at` real (closed_at), `period`, `value`/`contribution` NUMERIC(38,18), trazabilidad `(source, source_trade_id)` SIN FK física a canonical_operations (el replacement D1 jamás queda bloqueado por un derivado).
- `echo.lab_curve_metrics`: `(curve_id, metric_key)`; status, `value` NULL cuando no hay dato, basis, unit, `formula_id`, `formula_version`, `time_window`.
- DELIBERADO: sin FK dura `lab_curves → strategy_versions`. Un derivado no debe bloquear el ciclo de vida de la autoridad (el repo usa TRUNCATE/DELETE de identity como reset y el replacement D1 es atómico); la integridad la garantiza el servicio resolviendo la versión antes de publicar. Grante patrón 064 (`echo_user` DML, `mcp_echo_dev_ro` SELECT).

## 6. Recalculation semantics y boundary F4

`postgres.LabCurveService.RecalculateStrategyVersion(ctx, ns, ref, specs)`:
1. resuelve la StrategyVersion (404 si no existe);
2. UNA transacción REPEATABLE READ con el MISMO `pg_advisory_xact_lock(hashtext(ns), hashtext(ref))` del replacement D1;
3. lee head + TODAS las operaciones en la misma snapshot vía `StreamAllOperations` (keyset por `(opened_at,id)`, agota el dataset: jamás truncado — el read surface D1 `ListOperations` queda para UI con default 5000/cap 50000 intacto);
4. calcula cada spec con el engine;
5. publica header+puntos+métricas en la misma transacción (upsert por identidad, delete+insert de puntos/métricas). Fallo ⇒ rollback ⇒ materialización anterior íntegra; jamás publicación parcial ni puntos duplicados.

`same semantic input → same result_digest`; `changed dataset → dataset_digest distinto → materialización anterior no current → recálculo produce nueva válida`. Sin head ⇒ no publica nada y reporta estado por spec.

Fase 4 invoca este método (worker automático fuera de F3): `canonical history changed → dirty (dataset_digest ≠ actual) → RecalculateStrategyVersion → publish`. Invocable sin CLI ni frontend.

## 7. Read model y UI

Hasura (source artifact, `v3/hasura/metadata/tables/`): `lab_curves_v3.yaml` (select readonly/admin sobre lab_curves/points/metrics) y `canonical_history_readonly.yaml` (select readonly/admin sobre strategy_versions/strategy_history_state/canonical_operations). El front RENDERIZA derivados: tab `strategyCurveV3` en The Lab (Vue3) con header (versión, instrumento, A/B, estado, dataset), chart de tiempo real con bandas A/B y períodos TRAINING/PRE_REAL/REAL (REAL "sin iniciar" si B pendiente o sin REFERENCE), selector de versión/curva/basis, métricas cards (missing ≠ 0) y drill-down punto→`canonical_operations` por identidad durable. Paginación de puntos explícita hasta el total.

## 8. No-goals

Forge, ingestion Reference→canonical (D4), worker automático, screener/calendario, money management, portfolios, Sharpe/SQN, deploy/PROD, Timescale/particionamiento, trade_journal (sólo respetado).

## 9. Invariantes congeladas

`FORGE_DEPENDENCY = NONE` · `FORGE_DUAL_HISTORY_INTEGRATION = PENDING` · `TRADE_JOURNAL_WRITES = NONE` · `SECOND_CANONICAL = NONE`
