# RANKING REVIEW — Primer experimento real de ranking de Echo Forge (Cohort 001 · wave1c)

> Orientado al OWNER. Responde: **“¿Forge está rankeando y priorizando como yo lo haría?”** sobre las mismas 727 estrategias reales del Cohort 001.

## 1. Global

| Métrica | Valor |
|---|---:|
| Cohort total | 727 |
| Eligibles (evidence completa) | 727 |
| Excluidas / con error | 0 / 0 |
| Tipos lógicos (indicator_signature.v1@1.0.0) | 8 |
| Seleccionadas para el Retester (top 5 por tipo) | 34 |
| Retester ejecutadas | 34/34 COMPLETED (0 fallos de ejecución) |
| Sobreviven al retest (PF_retest ≥ 1.0 y net_profit_retest > 0 — convención de lectura, no veredicto de producto) | 34/34 |

## 2. Por tipo lógico — seleccionadas, frontera y bottom

### `ATR,RANGE,TRUERANGE_CLOSE,HIGH,OPEN_ATR,RANGE,TRUERANGE` — 431 estrategias, seleccionadas 5

**Seleccionadas (rank pre-retester → resultado retest):**

| # | filename | rank | rvalue | PF | Sharpe | DD | PF_retest | NP_retest | trades_retest | resultado |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | Strategy_6.39.759.sqx | 1 | 0.8209 | 2.28 | 1.36 | 481 | 1.97 | 9812 | 393 | SOBREVIVE |
| 2 | Strategy_7.51.646.sqx | 2 | 0.8201 | 2.47 | 1.21 | 447 | 2.18 | 7827 | 268 | SOBREVIVE |
| 3 | Strategy_2.33.473.sqx | 3 | 0.7556 | 2.34 | 1.29 | 582 | 1.91 | 8513 | 322 | SOBREVIVE |
| 4 | Strategy_1.51.675.sqx | 4 | 0.7509 | 2.05 | 1.46 | 587 | 1.80 | 13530 | 554 | SOBREVIVE |
| 5 | Strategy_8.20.704.sqx | 5 | 0.7462 | 2.37 | 1.20 | 530 | 2.17 | 8883 | 260 | SOBREVIVE |

**Last selected:** `Strategy_8.20.704.sqx` (rvalue 0.7462) · **First rejected:** `Strategy_1.52.708.sqx` (rvalue 0.7252, Δ=-0.0210)

**Bottom 5:**

| # | filename | rank | rvalue | PF | Sharpe | DD |
|---|---|---:|---:|---:|---:|---:|
| 1 | Strategy_1.76.407.sqx | 427 | 0.2032 | 1.55 | 0.98 | 938 |
| 2 | Strategy_3.68.564.sqx | 428 | 0.1988 | 1.55 | 1.15 | 1117 |
| 3 | Strategy_4.99.675.sqx | 429 | 0.1928 | 1.55 | 1.26 | 1239 |
| 4 | Strategy_6.99.636.sqx | 430 | 0.1872 | 1.44 | 1.13 | 1055 |
| 5 | Strategy_4.55.704.sqx | 431 | 0.1758 | 1.55 | 1.18 | 1194 |

### `ATR,BOLLINGERBANDS,RANGE,TRUERANGE_CLOSE,OPEN_ATR,BOLLINGERBANDS,RANGE,TRUERANGE` — 232 estrategias, seleccionadas 5

**Seleccionadas (rank pre-retester → resultado retest):**

| # | filename | rank | rvalue | PF | Sharpe | DD | PF_retest | NP_retest | trades_retest | resultado |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | Strategy_2.73.608.sqx | 1 | 0.8344 | 2.32 | 1.46 | 620 | 2.00 | 10946 | 382 | SOBREVIVE |
| 2 | Strategy_2.75.621.sqx | 2 | 0.8334 | 2.22 | 1.42 | 515 | 2.05 | 12170 | 407 | SOBREVIVE |
| 3 | Strategy_2.76.686.sqx | 3 | 0.8175 | 2.21 | 1.41 | 529 | 2.06 | 12188 | 406 | SOBREVIVE |
| 4 | Strategy_1.21.576.sqx | 4 | 0.8101 | 2.28 | 1.30 | 504 | 1.96 | 9538 | 335 | SOBREVIVE |
| 5 | Strategy_3.35.586.sqx | 5 | 0.7995 | 2.27 | 1.38 | 583 | 1.85 | 9332 | 364 | SOBREVIVE |

**Last selected:** `Strategy_3.35.586.sqx` (rvalue 0.7995) · **First rejected:** `Strategy_4.25.515.sqx` (rvalue 0.7863, Δ=-0.0132)

**Bottom 5:**

| # | filename | rank | rvalue | PF | Sharpe | DD |
|---|---|---:|---:|---:|---:|---:|
| 1 | Strategy_8.40.747.sqx | 228 | 0.2553 | 1.61 | 1.23 | 1014 |
| 2 | Strategy_1.26.673.sqx | 229 | 0.2462 | 1.73 | 1.34 | 1212 |
| 3 | Strategy_6.36.475.sqx | 230 | 0.2381 | 1.67 | 1.26 | 1117 |
| 4 | Strategy_7.50.612.sqx | 231 | 0.2217 | 1.59 | 1.11 | 964 |
| 5 | Strategy_5.33.723.sqx | 232 | 0.1906 | 1.64 | 1.34 | 1252 |

### `ATR,KELTNER,RANGE,TRUERANGE_CLOSE,OPEN_ATR,KELTNER,RANGE,TRUERANGE` — 28 estrategias, seleccionadas 5

**Seleccionadas (rank pre-retester → resultado retest):**

| # | filename | rank | rvalue | PF | Sharpe | DD | PF_retest | NP_retest | trades_retest | resultado |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | Strategy_8.46.640.sqx | 1 | 0.7871 | 1.93 | 1.19 | 638 | 1.74 | 9164 | 418 | SOBREVIVE |
| 2 | Strategy_2.50.514.sqx | 2 | 0.7651 | 1.89 | 1.40 | 874 | 1.63 | 11502 | 596 | SOBREVIVE |
| 3 | Strategy_1.83.581.sqx | 3 | 0.7575 | 1.92 | 1.36 | 876 | 1.69 | 10722 | 541 | SOBREVIVE |
| 4 | Strategy_1.53.401.sqx | 4 | 0.7323 | 1.89 | 1.35 | 873 | 1.63 | 11146 | 588 | SOBREVIVE |
| 5 | Strategy_8.34.407.sqx | 5 | 0.7235 | 1.86 | 1.25 | 737 | 1.63 | 9522 | 491 | SOBREVIVE |

**Last selected:** `Strategy_8.34.407.sqx` (rvalue 0.7235) · **First rejected:** `Strategy_2.67.641.sqx` (rvalue 0.7182, Δ=-0.0053)

**Bottom 5:**

| # | filename | rank | rvalue | PF | Sharpe | DD |
|---|---|---:|---:|---:|---:|---:|
| 1 | Strategy_6.19.441.sqx | 24 | 0.5231 | 1.69 | 1.01 | 610 |
| 2 | Strategy_4.57.731.sqx | 25 | 0.5067 | 1.72 | 1.20 | 895 |
| 3 | Strategy_2.1.718.sqx | 26 | 0.4800 | 1.60 | 0.95 | 511 |
| 4 | Strategy_4.37.399.sqx | 27 | 0.2600 | 1.52 | 1.30 | 1209 |
| 5 | Strategy_2.98.541.sqx | 28 | 0.1577 | 1.48 | 1.15 | 1166 |

### `ATR,RANGE_CLOSE,HIGH,OPEN_ATR,RANGE` — 16 estrategias, seleccionadas 5

**Seleccionadas (rank pre-retester → resultado retest):**

| # | filename | rank | rvalue | PF | Sharpe | DD | PF_retest | NP_retest | trades_retest | resultado |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | Strategy_3.18.626.sqx | 1 | 0.7346 | 2.07 | 1.25 | 806 | 1.86 | 9583 | 377 | SOBREVIVE |
| 2 | Strategy_6.32.425.sqx | 2 | 0.7278 | 2.02 | 1.19 | 663 | 1.75 | 7896 | 434 | SOBREVIVE |
| 3 | Strategy_7.2.741.sqx | 3 | 0.5768 | 1.84 | 1.04 | 501 | 1.68 | 6295 | 336 | SOBREVIVE |
| 4 | Strategy_7.46.731.sqx | 4 | 0.5225 | 1.69 | 1.22 | 770 | 1.61 | 13615 | 697 | SOBREVIVE |
| 5 | Strategy_8.11.487.sqx | 5 | 0.5157 | 1.79 | 1.21 | 866 | 1.69 | 12475 | 663 | SOBREVIVE |

**Last selected:** `Strategy_8.11.487.sqx` (rvalue 0.5157) · **First rejected:** `Strategy_1.14.604.sqx` (rvalue 0.4965, Δ=-0.0193)

**Bottom 5:**

| # | filename | rank | rvalue | PF | Sharpe | DD |
|---|---|---:|---:|---:|---:|---:|
| 1 | Strategy_8.11.442.sqx | 12 | 0.3449 | 1.60 | 1.12 | 837 |
| 2 | Strategy_7.47.615.sqx | 13 | 0.3425 | 1.59 | 1.08 | 760 |
| 3 | Strategy_1.16.478.sqx | 14 | 0.3291 | 1.66 | 1.23 | 1121 |
| 4 | Strategy_6.6.720.sqx | 15 | 0.2632 | 1.60 | 1.19 | 1114 |
| 5 | Strategy_3.60.460.sqx | 16 | 0.1688 | 1.51 | 1.22 | 1254 |

### `ATR,BOLLINGERBANDS,RANGE_CLOSE,OPEN_ATR,BOLLINGERBANDS,RANGE` — 11 estrategias, seleccionadas 5

**Seleccionadas (rank pre-retester → resultado retest):**

| # | filename | rank | rvalue | PF | Sharpe | DD | PF_retest | NP_retest | trades_retest | resultado |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | Strategy_2.17.503.sqx | 1 | 0.7000 | 2.00 | 1.14 | 564 | 1.90 | 8135 | 397 | SOBREVIVE |
| 2 | Strategy_2.41.524.sqx | 2 | 0.6572 | 1.88 | 1.22 | 599 | 1.83 | 9189 | 480 | SOBREVIVE |
| 3 | Strategy_2.17.581.sqx | 3 | 0.6014 | 1.86 | 1.47 | 1010 | 1.66 | 14424 | 710 | SOBREVIVE |
| 4 | Strategy_2.25.400.sqx | 4 | 0.5785 | 1.95 | 1.30 | 914 | 1.80 | 11189 | 497 | SOBREVIVE |
| 5 | Strategy_6.34.433.sqx | 5 | 0.4990 | 1.84 | 1.24 | 823 | 1.61 | 9081 | 536 | SOBREVIVE |

**Last selected:** `Strategy_6.34.433.sqx` (rvalue 0.4990) · **First rejected:** `Strategy_8.19.624.sqx` (rvalue 0.3863, Δ=-0.1127)

**Bottom 5:**

| # | filename | rank | rvalue | PF | Sharpe | DD |
|---|---|---:|---:|---:|---:|---:|
| 1 | Strategy_3.58.471.sqx | 7 | 0.3765 | 1.78 | 1.28 | 996 |
| 2 | Strategy_8.10.634.sqx | 8 | 0.3621 | 1.63 | 1.37 | 966 |
| 3 | Strategy_2.16.742.sqx | 9 | 0.3154 | 1.76 | 1.36 | 1177 |
| 4 | Strategy_3.44.399.sqx | 10 | 0.3033 | 1.73 | 1.25 | 1007 |
| 5 | Strategy_5.21.486.sqx | 11 | 0.1275 | 1.61 | 1.24 | 1121 |

### `ATR,BOLLINGERBANDS,RANGE,TRUERANGE_CLOSE,HIGH,OPEN_ATR,BOLLINGERBANDS,RANGE,TRUERANGE` — 5 estrategias, seleccionadas 5

**Seleccionadas (rank pre-retester → resultado retest):**

| # | filename | rank | rvalue | PF | Sharpe | DD | PF_retest | NP_retest | trades_retest | resultado |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | Strategy_1.8.669.sqx | 1 | 0.5750 | 2.05 | 1.23 | 491 | 1.72 | 7742 | 351 | SOBREVIVE |
| 2 | Strategy_1.13.611.sqx | 2 | 0.5521 | 2.25 | 1.27 | 690 | 1.82 | 8033 | 337 | SOBREVIVE |
| 3 | Strategy_6.39.493.sqx | 3 | 0.5250 | 2.13 | 1.48 | 897 | 1.97 | 13361 | 530 | SOBREVIVE |
| 4 | Strategy_6.40.536.sqx | 4 | 0.2076 | 1.79 | 1.26 | 736 | 1.62 | 10934 | 574 | SOBREVIVE |
| 5 | Strategy_6.41.479.sqx | 5 | 0.1831 | 1.77 | 1.25 | 736 | 1.58 | 10671 | 596 | SOBREVIVE |

**Last selected:** `Strategy_6.41.479.sqx` (rvalue 0.1831) · **First rejected:** n/a

**Bottom 5:**

| # | filename | rank | rvalue | PF | Sharpe | DD |
|---|---|---:|---:|---:|---:|---:|
| 1 | Strategy_1.8.669.sqx | 1 | 0.5750 | 2.05 | 1.23 | 491 |
| 2 | Strategy_1.13.611.sqx | 2 | 0.5521 | 2.25 | 1.27 | 690 |
| 3 | Strategy_6.39.493.sqx | 3 | 0.5250 | 2.13 | 1.48 | 897 |
| 4 | Strategy_6.40.536.sqx | 4 | 0.2076 | 1.79 | 1.26 | 736 |
| 5 | Strategy_6.41.479.sqx | 5 | 0.1831 | 1.77 | 1.25 | 736 |

### `ATR,BARRANGE,BOLLINGERBANDS,RANGE_CLOSE,OPEN_ATR,BARRANGE,BOLLINGERBANDS,RANGE` — 2 estrategias, seleccionadas 2

**Seleccionadas (rank pre-retester → resultado retest):**

| # | filename | rank | rvalue | PF | Sharpe | DD | PF_retest | NP_retest | trades_retest | resultado |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | Strategy_8.26.438.sqx | 1 | 0.7000 | 1.82 | 1.21 | 870 | 1.66 | 11060 | 511 | SOBREVIVE |
| 2 | Strategy_5.38.585.sqx | 2 | 0.3000 | 1.53 | 1.23 | 1075 | 1.46 | 15301 | 1054 | SOBREVIVE |

**Last selected:** `Strategy_5.38.585.sqx` (rvalue 0.3000) · **First rejected:** n/a

**Bottom 5:**

| # | filename | rank | rvalue | PF | Sharpe | DD |
|---|---|---:|---:|---:|---:|---:|
| 1 | Strategy_8.26.438.sqx | 1 | 0.7000 | 1.82 | 1.21 | 870 |
| 2 | Strategy_5.38.585.sqx | 2 | 0.3000 | 1.53 | 1.23 | 1075 |

### `ATR,BOLLINGERBANDS,RANGE_CLOSE,HIGH,OPEN_ATR,BOLLINGERBANDS,RANGE` — 2 estrategias, seleccionadas 2

**Seleccionadas (rank pre-retester → resultado retest):**

| # | filename | rank | rvalue | PF | Sharpe | DD | PF_retest | NP_retest | trades_retest | resultado |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | Strategy_2.27.756.sqx | 1 | 0.7000 | 1.97 | 1.23 | 795 | 1.72 | 9461 | 429 | SOBREVIVE |
| 2 | Strategy_6.24.638.sqx | 2 | 0.3000 | 1.78 | 1.44 | 862 | 1.71 | 14109 | 788 | SOBREVIVE |

**Last selected:** `Strategy_6.24.638.sqx` (rvalue 0.3000) · **First rejected:** n/a

**Bottom 5:**

| # | filename | rank | rvalue | PF | Sharpe | DD |
|---|---|---:|---:|---:|---:|---:|
| 1 | Strategy_2.27.756.sqx | 1 | 0.7000 | 1.97 | 1.23 | 795 |
| 2 | Strategy_6.24.638.sqx | 2 | 0.3000 | 1.78 | 1.44 | 862 |

## 3. Ranking vs First Retester (comparación descriptiva)

El Retester del owner (`FirstRetestConfig.cfx` SHA `c0ea66f1…`: chart USATECHIDXUSD_darwinex H1, spread 1.5, datos M1 2016-01-01 → 2026-05-13, template `RetestPrecision.cfx`) re-corrió cada estrategia seleccionada y re-guardó sus resultados; los resultados del retest se extrajeron con el enrichment canónico (corrida técnica `wave1c_r`, FlowRun `79e0cc50`, 34/34 con MetricSets).

| Grupo | n | estrategias |
|---|---:|---|
| otros seleccionados + sobrevive | 26 | `Strategy_5.38.585.sqx`, `Strategy_1.13.611.sqx`, `Strategy_6.39.493.sqx`, `Strategy_6.40.536.sqx`, `Strategy_6.41.479.sqx`, `Strategy_2.75.621.sqx`, `Strategy_2.76.686.sqx`, `Strategy_1.21.576.sqx` … |
| top-ranked + sobrevive | 8 | `Strategy_8.26.438.sqx`, `Strategy_1.8.669.sqx`, `Strategy_2.73.608.sqx`, `Strategy_2.27.756.sqx`, `Strategy_2.17.503.sqx`, `Strategy_8.46.640.sqx`, `Strategy_6.39.759.sqx`, `Strategy_3.18.626.sqx` |

**Detalle pre vs retest por estrategia:** `RETESTER-RESULTS.csv` (PF/Sharpe/DD/net_profit/trades pre y retest, deltas, SHAs input/output). No se recalibraron pesos ni se re-ordenó nada: el ranking congelado se compara tal cual contra el outcome.

## 4. Casos raros (sólo visibles, sin juicio)

- `Strategy_8.26.438.sqx` (BARRANGE,BOLLINGERBANDS,RANGE_CLOSE,OPEN_BARRANGE,BOLLINGERBANDS,RANGE, rank 1/2): seleccionada con métrica débil: Sharpe,DD
- `Strategy_5.38.585.sqx` (BARRANGE,BOLLINGERBANDS,RANGE_CLOSE,OPEN_BARRANGE,BOLLINGERBANDS,RANGE, rank 2/2): PF alto pero rank bajo; seleccionada con métrica débil: PF,DD
- `Strategy_1.8.669.sqx` (BOLLINGERBANDS,RANGE,TRUERANGE_CLOSE,HIGH,OPEN_BOLLINGERBANDS,RANGE,TRUERANGE, rank 1/5): seleccionada con métrica débil: Sharpe
- `Strategy_6.39.493.sqx` (BOLLINGERBANDS,RANGE,TRUERANGE_CLOSE,HIGH,OPEN_BOLLINGERBANDS,RANGE,TRUERANGE, rank 3/5): PF alto pero rank bajo; seleccionada con métrica débil: DD
- `Strategy_6.40.536.sqx` (BOLLINGERBANDS,RANGE,TRUERANGE_CLOSE,HIGH,OPEN_BOLLINGERBANDS,RANGE,TRUERANGE, rank 4/5): seleccionada con métrica débil: PF,DD
- `Strategy_6.41.479.sqx` (BOLLINGERBANDS,RANGE,TRUERANGE_CLOSE,HIGH,OPEN_BOLLINGERBANDS,RANGE,TRUERANGE, rank 5/5): seleccionada con métrica débil: PF,Sharpe,DD
- `Strategy_4.25.515.sqx` (BOLLINGERBANDS,RANGE,TRUERANGE_CLOSE,OPEN_BOLLINGERBANDS,RANGE,TRUERANGE, rank 6/232): rechazada cerca del cutoff (Δ=-0.0132)
- `Strategy_1.33.627.sqx` (BOLLINGERBANDS,RANGE,TRUERANGE_CLOSE,OPEN_BOLLINGERBANDS,RANGE,TRUERANGE, rank 119/232): DD excelente pero rank bajo
- `Strategy_1.16.531.sqx` (BOLLINGERBANDS,RANGE,TRUERANGE_CLOSE,OPEN_BOLLINGERBANDS,RANGE,TRUERANGE, rank 124/232): DD excelente pero rank bajo
- `Strategy_1.30.496.sqx` (BOLLINGERBANDS,RANGE,TRUERANGE_CLOSE,OPEN_BOLLINGERBANDS,RANGE,TRUERANGE, rank 125/232): DD excelente pero rank bajo
- `Strategy_2.98.542.sqx` (BOLLINGERBANDS,RANGE,TRUERANGE_CLOSE,OPEN_BOLLINGERBANDS,RANGE,TRUERANGE, rank 161/232): DD excelente pero rank bajo
- `Strategy_7.54.589.sqx` (BOLLINGERBANDS,RANGE,TRUERANGE_CLOSE,OPEN_BOLLINGERBANDS,RANGE,TRUERANGE, rank 112/232): empate de ranking_value (0.5240) entre 2: Strategy_7.54.589.sqx, Strategy_7.53.540.sqx
- `Strategy_2.27.756.sqx` (BOLLINGERBANDS,RANGE_CLOSE,HIGH,OPEN_BOLLINGERBANDS,RANGE, rank 1/2): seleccionada con métrica débil: Sharpe,DD
- `Strategy_6.24.638.sqx` (BOLLINGERBANDS,RANGE_CLOSE,HIGH,OPEN_BOLLINGERBANDS,RANGE, rank 2/2): PF alto pero rank bajo; seleccionada con métrica débil: PF,DD
- `Strategy_2.17.503.sqx` (BOLLINGERBANDS,RANGE_CLOSE,OPEN_BOLLINGERBANDS,RANGE, rank 1/11): seleccionada con métrica débil: Sharpe
- `Strategy_2.41.524.sqx` (BOLLINGERBANDS,RANGE_CLOSE,OPEN_BOLLINGERBANDS,RANGE, rank 2/11): seleccionada con métrica débil: Sharpe
- `Strategy_2.17.581.sqx` (BOLLINGERBANDS,RANGE_CLOSE,OPEN_BOLLINGERBANDS,RANGE, rank 3/11): seleccionada con métrica débil: DD
- `Strategy_6.34.433.sqx` (BOLLINGERBANDS,RANGE_CLOSE,OPEN_BOLLINGERBANDS,RANGE, rank 5/11): seleccionada con métrica débil: Sharpe
- `Strategy_2.50.514.sqx` (KELTNER,RANGE,TRUERANGE_CLOSE,OPEN_KELTNER,RANGE,TRUERANGE, rank 2/28): seleccionada con métrica débil: DD
- `Strategy_1.83.581.sqx` (KELTNER,RANGE,TRUERANGE_CLOSE,OPEN_KELTNER,RANGE,TRUERANGE, rank 3/28): seleccionada con métrica débil: DD
- `Strategy_2.67.641.sqx` (KELTNER,RANGE,TRUERANGE_CLOSE,OPEN_KELTNER,RANGE,TRUERANGE, rank 6/28): rechazada cerca del cutoff (Δ=-0.0053)
- `Strategy_3.60.683.sqx` (KELTNER,RANGE,TRUERANGE_CLOSE,OPEN_KELTNER,RANGE,TRUERANGE, rank 16/28): PF alto pero rank bajo
- `Strategy_6.3.684.sqx` (KELTNER,RANGE,TRUERANGE_CLOSE,OPEN_KELTNER,RANGE,TRUERANGE, rank 17/28): DD excelente pero rank bajo
- `Strategy_8.31.709.sqx` (KELTNER,RANGE,TRUERANGE_CLOSE,OPEN_KELTNER,RANGE,TRUERANGE, rank 20/28): DD excelente pero rank bajo
- `Strategy_6.19.441.sqx` (KELTNER,RANGE,TRUERANGE_CLOSE,OPEN_KELTNER,RANGE,TRUERANGE, rank 24/28): DD excelente pero rank bajo
- `Strategy_2.1.718.sqx` (KELTNER,RANGE,TRUERANGE_CLOSE,OPEN_KELTNER,RANGE,TRUERANGE, rank 26/28): DD excelente pero rank bajo
- `Strategy_1.52.688.sqx` (RANGE,TRUERANGE_CLOSE,HIGH,OPEN_RANGE,TRUERANGE, rank 216/431): DD excelente pero rank bajo
- `Strategy_3.61.563.sqx` (RANGE,TRUERANGE_CLOSE,HIGH,OPEN_RANGE,TRUERANGE, rank 218/431): DD excelente pero rank bajo
- `Strategy_4.52.576.sqx` (RANGE,TRUERANGE_CLOSE,HIGH,OPEN_RANGE,TRUERANGE, rank 222/431): DD excelente pero rank bajo
- `Strategy_5.36.415.sqx` (RANGE,TRUERANGE_CLOSE,HIGH,OPEN_RANGE,TRUERANGE, rank 223/431): PF alto pero rank bajo; Sharpe alto pero rank bajo
- `Strategy_8.95.514.sqx` (RANGE,TRUERANGE_CLOSE,HIGH,OPEN_RANGE,TRUERANGE, rank 224/431): PF alto pero rank bajo; Sharpe alto pero rank bajo
- `Strategy_1.59.670.sqx` (RANGE,TRUERANGE_CLOSE,HIGH,OPEN_RANGE,TRUERANGE, rank 225/431): DD excelente pero rank bajo
- `Strategy_6.62.612.sqx` (RANGE,TRUERANGE_CLOSE,HIGH,OPEN_RANGE,TRUERANGE, rank 229/431): DD excelente pero rank bajo
- `Strategy_1.76.680.sqx` (RANGE,TRUERANGE_CLOSE,HIGH,OPEN_RANGE,TRUERANGE, rank 232/431): DD excelente pero rank bajo
- `Strategy_5.39.422.sqx` (RANGE,TRUERANGE_CLOSE,HIGH,OPEN_RANGE,TRUERANGE, rank 239/431): DD excelente pero rank bajo
- `Strategy_5.34.532.sqx` (RANGE,TRUERANGE_CLOSE,HIGH,OPEN_RANGE,TRUERANGE, rank 246/431): DD excelente pero rank bajo
- `Strategy_2.60.525.sqx` (RANGE,TRUERANGE_CLOSE,HIGH,OPEN_RANGE,TRUERANGE, rank 247/431): DD excelente pero rank bajo
- `Strategy_6.13.505.sqx` (RANGE,TRUERANGE_CLOSE,HIGH,OPEN_RANGE,TRUERANGE, rank 253/431): DD excelente pero rank bajo
- `Strategy_4.74.552.sqx` (RANGE,TRUERANGE_CLOSE,HIGH,OPEN_RANGE,TRUERANGE, rank 266/431): PF alto pero rank bajo
- `Strategy_5.41.745.sqx` (RANGE,TRUERANGE_CLOSE,HIGH,OPEN_RANGE,TRUERANGE, rank 267/431): Sharpe alto pero rank bajo
- `Strategy_5.81.407.sqx` (RANGE,TRUERANGE_CLOSE,HIGH,OPEN_RANGE,TRUERANGE, rank 278/431): DD excelente pero rank bajo
- `Strategy_3.35.558.sqx` (RANGE,TRUERANGE_CLOSE,HIGH,OPEN_RANGE,TRUERANGE, rank 293/431): DD excelente pero rank bajo
- `Strategy_6.36.708.sqx` (RANGE,TRUERANGE_CLOSE,HIGH,OPEN_RANGE,TRUERANGE, rank 296/431): DD excelente pero rank bajo
- `Strategy_1.60.641.sqx` (RANGE,TRUERANGE_CLOSE,HIGH,OPEN_RANGE,TRUERANGE, rank 300/431): DD excelente pero rank bajo
- `Strategy_8.30.562.sqx` (RANGE,TRUERANGE_CLOSE,HIGH,OPEN_RANGE,TRUERANGE, rank 304/431): DD excelente pero rank bajo
- `Strategy_5.53.566.sqx` (RANGE,TRUERANGE_CLOSE,HIGH,OPEN_RANGE,TRUERANGE, rank 340/431): DD excelente pero rank bajo
- `Strategy_5.36.415.sqx` (RANGE,TRUERANGE_CLOSE,HIGH,OPEN_RANGE,TRUERANGE, rank 223/431): empate de ranking_value (0.4620) entre 2: Strategy_5.36.415.sqx, Strategy_8.95.514.sqx
- `Strategy_7.40.641.sqx` (RANGE,TRUERANGE_CLOSE,HIGH,OPEN_RANGE,TRUERANGE, rank 411/431): empate de ranking_value (0.2811) entre 2: Strategy_7.40.641.sqx, Strategy_7.38.404.sqx
- `Strategy_7.2.741.sqx` (RANGE_CLOSE,HIGH,OPEN_RANGE, rank 3/16): seleccionada con métrica débil: Sharpe
- `Strategy_7.47.615.sqx` (RANGE_CLOSE,HIGH,OPEN_RANGE, rank 13/16): DD excelente pero rank bajo

## 5. Guía de revisión para el owner
1. ¿Las top-5 por tipo te habrían llamado la atención a ti? (§2)
2. ¿drawdown COST 40 pesa demasiado? Mirá cómo el min-max comprime cuando hay outliers (§4).
3. ¿Las particiones de 2 (tipos casi-singleton) deberían rankear en absoluto?
4. ¿El retest confirma o refuta tu intuición sobre las 34 seleccionadas? (§3 y CSV)

## 6. Linaje completo
Cohort 001 (freeze `79a67e80…`, 727 byte-exactos) → wave1c FlowRun `254977a0` (release 0.2.108 @ `0dfde58`, **NDX canónico**, import 727/727 COMPLETED) → classification 727 → ranking 30/30/40 PER_LOGICAL_TYPE top_n 5 → TopProjection 34 → group batch_size=1 → `FirstRetestConfig.cfx` → 34 retests COMPLETED → extracción de resultados wave1c_r FlowRun `79e0cc50` (34/34).
