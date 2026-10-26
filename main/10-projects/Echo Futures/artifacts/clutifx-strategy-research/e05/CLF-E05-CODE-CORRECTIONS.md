# CLF-E05 — CODE CORRECTIONS

Fecha: 2026-10-26 · `OWNER_ACCEPTANCE: REVIEW`

## Código del motor Echo: SIN cambios

`xKoRx/echo` rama `experiment/clutifx-s01` @ `e8c2e47e` — árbol limpio antes y después del ciclo; sin commits, sin merge, sin LIVE. Razón: no hubo defecto de motor demostrable por recibos; los dos defectos encontrados viven en (a) scripts de auditoría del run root y (b) la semántica del gate de bias, cuya corrección correcta exige la fuente (K05 ausente) y decisión Owner. Corregir (b) sin esa decisión habría cambiado silenciosamente la semántica de 4 variantes e invalidado recibos — prohibido por /frozen y por la constitución del ciclo.

## Correcciones aplicadas (scripts de auditoría, run root `~/echo-work/clutifx-backtest/e05/`)

| Script | Corrección | Rojo → Verde |
|---|---|---|
| `census_e05.py` (deriva de `q04/census_q04.py`) | trades = operaciones completas únicamente (entry+exit fills); ops `MM_NO_ACTION`, ordenadas-sin-fill y abiertas al horizonte van a contadores de funnel separados | estado rojo documentado: censo Q04 sumaba 56 con S13=3 (`NO_ORDERS`×2 contados como trades); verde: S13=1 y total 54=32W/22L |
| `build_tables_e05.py` (deriva de `q04/build_tables_q04.py`) | `trades`/`executed_trades`/`max_achievable_all_win` desde trades completos; columna de nota contable y funnel en evidencia | CSVs regenerados: `CLF-E05-Q04-ALL19-FUNDING-FAILURES.csv`, `CLF-E05-TARGET-FEASIBILITY.csv`, `CLF-E05-FREQUENCY-AND-COVERAGE.csv` |
| `test_accounting_e05.py` (nuevo) | 3 regresiones: sintético 3×MM_NO_ACTION+1 abierta+1 completa ⇒ trades=1; S13 real ⇒ 1/0W/1L/−334,98; reconciliación global vs `CLF-Q03R1-G4-QUALIFICATION.csv` por identidad + totales 54/32/22 | `ALL REGRESSIONS GREEN` (salida íntegra en el run root) |
| `r03_temporal_audit.py` + `r03_spanning_finder.py` (nuevos) | auditoría temporal del control R03 por timestamps reales | FASE 3 resuelta con cero incógnitas (ver `CLF-E05-R03-TEMPORAL-CONTROL.md`) |
| `audit_census_hist.py` (nuevo, read-only) | histograma pre-fix que selló el estado rojo (56 total, sólo S13 con NO_ORDERS) | evidencia |

## Suite Go afectada (FASE 6/7)

`go test -count=1 ./v3/sdk/futures/strategies/clf/...` sobre e8c2e47e: `ok clf 116,9s` · `ok clf/detectors 70,0s` · `EXIT=0` (log `e05/gotest_clf_pkg.log`). Cero cambios de código ⇒ cero regresiones propias; baseline limpio sin fallos preexistentes conocidos en este paquete.

## Pendientes de código (bloqueados, con causa)

- E05-01 (bias gate): requiere decisión de fuente/Owner → crearía identidades nuevas S03'/S04'/S05' y repetición G1–G4 propia (KRR-008).
- KRR-003 (conjunción Failure Swing): requiere K05/video review.
- S08/T03 (materialización) y T02 (parámetro stop_extra_ticks): requieren spec Owner (KRR-007/KRR-005).
