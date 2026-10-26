# CLF-E05 — Q04 ACCOUNTING REPAIR (FASE 2)

Fecha: 2026-10-26 · Host: Hefesto · Fuente Echo: `experiment/clutifx-s01` @ `e8c2e47e` (SIN cambios de código del motor) · `OWNER_ACCEPTANCE: REVIEW`

## Hallazgo material S13 (confirmado)

Q03-R1 reporta `S13: 1 round-trip, 0W/1L`; los CSV derivados de Q04 reportaban `S13: 3 trades, 0W/1L`. El timeline Q04 ya describía la realidad física: una operación completa perdedora y **dos episodios `MM_NO_ACTION`** (causa downstream `SIZE_BELOW_MIN_CONTRACT`). Dos intentos de MM sin órdenes no son dos trades.

## Defecto exacto (script, no motor)

El script `q04/census_q04.py` agregaba **toda** `OPERATION_SNAPSHOT` como round-trip: la rama sin órdenes agregaba un registro `result="NO_ORDERS"` a la lista `roundtrips`, y `build_tables_q04.py` publicaba `n_roundtrips` como `trades` y `executed_trades`. El motor y su contabilidad (`result.json` `reconciled=true`, reconciliación posición-a-posición desde fills) estaban correctos; el defecto estaba confinado al censo del auditor. Evidencia del estado rojo: histograma por identidad del `census.json` Q04 = total 56 (54 reales + 2 `NO_ORDERS`), único afectado S13 (+2); `OPEN_AT_HORIZON = 0` en todo el corpus.

## Corrección aplicada (sólo scripts de auditoría, `~/echo-work/clutifx-backtest/e05/`)

- `census_e05.py`: un trade es una operación **completa** (≥1 fill de entrada y ≥1 fill de salida, round-trip reconciliado). Las ops sin órdenes se contabilizan en `n_ops_without_orders` (con `termination.reason`), las ordenadas-sin-fill en `n_ops_ordered_unfilled` y las abiertas al horizonte en `n_open_at_horizon` — eventos de funnel, jamás trades.
- `build_tables_e05.py`: `trades`/`executed_trades` = round-trips completos; `max_achievable_all_win = trades_completos × $465,02`; nota de funnel en la evidencia de cada fila.
- Regresiones obligatorias (`test_accounting_e05.py`, todas verdes): (1) fixture sintético con **3 `MM_NO_ACTION` + 1 abierta + 1 completa ⇒ trades=1**; (2) S13 real sellada ⇒ 1 trade, 0W/1L, net −334,98, 2 ops `MM_NO_ACTION`; (3) reconciliación global contra `q03r1/CLF-Q03R1-G4-QUALIFICATION.csv`: igualdad por identidad en las 19 y totales NQU6 **54 round-trips = 32W/22L**, obtenidos de los recibos (no impuestos).

## Derivados regenerados (e05, run root y vault)

`CLF-E05-Q04-ALL19-FUNDING-FAILURES.csv` (S13: trades 3→1, executed 3→1, max_achievable 1395,06→**465,02**; sigue `UNREACHABLE` — el veredicto económico 19/19 se robustece), `CLF-E05-TARGET-FEASIBILITY.csv`, `CLF-E05-FREQUENCY-AND-COVERAGE.csv` (S13: roundtrips_executed 3→1, conversión 1/9, trades_per_active_day 1,0). Los totales corregidos: **54 trades completos = 32W/22L**, idénticos al censo Q03-R1. Emisiones, fills, caja, equity y señales: byte-idénticos a Q04 (el defecto no tocaba el lado de emisión).

## Documentos que consumían las cifras (corrección por delta)

- `q04/CLF-Q04-STRATEGY-DECISIONS.md` §5: "2–3 ejecuciones" para S13 → leer "1 operación completa (2 admisiones muertas por tamaño no son ejecuciones)".
- `q04/CLF-Q04-ECONOMIC-ROOT-CAUSE.md` §6 "ejecutadas 2–6" → rango correcto 1–6 con S13=1.
- `q04/CLF-Q04-ENGINE-ACCOUNTING-VERIFICATION.md`: la cifra "54 en NQU6" queda ahora respaldada también por el censo del auditor (antes sumaba 56).
- Los archivos sellados de `q04/` NO se modifican (write-once preservado); esta corrección vive en `e05/` y el puntero `q04/CLF-Q04-SUPERSEDED-BY-E05.md` dirige a ella.

## Garantías

Cero re-ejecuciones de motores (0 motores nuevos); cero cambios en `xKoRx/echo`; resultados negativos previos preservados; el fix no altera ninguna decisión de señal/MM/Provider, por lo que ningún recibo G1–G4 queda invalidado.
