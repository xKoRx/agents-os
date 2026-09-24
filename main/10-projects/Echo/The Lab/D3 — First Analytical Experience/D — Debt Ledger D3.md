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
  - "[[A — Technical SPEC D3]]"
  - "[[C — Evidence D3 (Shot 1)]]"
  - "[[D — Debt Ledger D3]]"
  - "[[E — F4 Handoff D3]]"
aliases:
  - D3 debt ledger
tags:
  - kind/doc
  - area/echo
  - the-lab
  - d3
---

# D — Debt Ledger D3

## Clasificación Lab V1/V2 encontrada (para L-CLEAN; ejecución post D5, no en F3)

| Objeto | Clasificación | Nota |
|---|---|---|
| `v3/sdk/lab/**` (domain/formulas/curves/metrics/segments/dataquality/riskpolicy/ids: lab_canonical_trades, outcomes, segment_code, RECORDED_GLOBAL, InitialVirtualCapital) | REMOVE | Legacy RFC-009 V1; ninguna ruta V3 lo consume. `CalculateDrawdown` (float64) no reutilizado: D3 usa `sdk/analytics/formulas` (big.Rat). |
| `v3/lab-worker/internal/builders/{recompute,materialize_curves,materialize_snapshots,canonical_a0}.go` + sus cmd dev | REMOVE | Pipeline legacy (recorded time, R AUTO, scopes BACKTEST/SQX sobre Reference derivada). Fuera de D3 por congelado F16. |
| `v3/hasura/metadata/tables/{lab_clean,the_lab,strategy_portfolio_lab}.yaml` + `functions/{lab_clean,the_lab}.yaml` | REMOVE / L-CLEAN | Read models V1/V2 (`v_lab_strategy_screener`, `fn_lab_*`, `lab_out_*`); retirar cuando el front V3 desacople (L-CLEAN post D5 con mapa de consumidores). |
| Front legacy: `src/services/graphql/journal.js` (fn_* / mv_strategy_overview), tabs retirados en `LEGACY_TAB_IDS`, `fn_strategy_*`/`lab_out_*` | REMOVE | Ya desconectados del UI activo; borrar en L-CLEAN. |
| Tablas PG `lab_equity_curve_points`, `lab_strategy_metric_snapshots`, `lab_canonical_trades`, `lab_strategy_outcomes`, `lab_job_runs` | SHARED / REMOVE | `lab_job_runs` SHARED: D3 lo reutiliza como infraestructura de job runs (decisión B del Lab). Las demás: L-CLEAN tras verificar consumidores. |
| `echo.canonical_operations`/`echo.strategy_history_state`/mig 064 | SHARED | Autoridad D1, preservada intacta. |
| `sdk/analytics/formulas` + `sdk/contracts` | SHARED | Reutilizados como primitivas correctas (REUSED). |

## Deuda nueva introducida por D3

NINGUNA bloqueante. Notas: (1) `rpips_cumulative` registrado sin implementación — deliberado (F6/F7), requiere autoridad de spec de instrumento; (2) orden de `lab_job_runs.result` del builder nuevo agrega vocabulario `recalculate_lab_curves_v3` — infraestructura existente reutilizada; (3) front `Number(p.value)` sólo para eje del chart (display), la semántica vive en el backend.

## Deuda Shot 3 (corrección F-D3-01..07 @ 372af59a)

- `CONCURRENT_REPUBLISH_PAGINATION_SNAPSHOT = DEFERRED` (F-D3-05): la paginación offset del front bajo republicación concurrente de la misma curva puede duplicar o saltar puntos; la corrección Shot 3 hace fail-closed toda carga incompleta (página vacía prematura, página fallida, total final distinto ⇒ error, jamás parcial presentado como completo), pero el snapshot transaccional de lectura / keyset queda pospuesto por decisión de alcance del manager. Cerrarlo pertenece a un shot posterior con diseño de paginación, no a D3.
- `D3_DEV_INTEGRATION = UNVERIFIED_EXTERNAL`: PG DEV carece de la base D1 (064 sin aplicar a bases reales); aplicar 065+metadata D3 en DEV requiere primero el despliegue D1 gated (Environment Contract §5.6). No es defecto D3.

## Limitaciones verificadas

- Dataset de certificación: FIXTURE determinista vía mecanismos correctos (PUT D1 + SQL de prueba declarado para REFERENCE). Sin historia auténtica (D2/Forge pendiente) el gate D3 auténtico con estrategia real queda para la integración.
- Hasura metadata y front DEV: source artifacts sin apply físico (ver [[C — Evidence D3 (Shot 1)]] EXTERNAL).
- `TestScratch_QueryDB` (preexistente) falla en PG desechable por connStr versionado — demostrado igual en baseline; deuda del repo, no de D3.
- Ejecución combinada `go test` de sdk/postgres + lab-worker builders en una sola invocación falla por tablas A0 write-once compartidas — preexistente en baseline (verificado en `8adce7ec` limpio); correr por paquete.
