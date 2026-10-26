# CLF-E05 — R03 TEMPORAL CONTROL (FASE 3)

Fecha: 2026-10-26 · Host: Hefesto · Método: recibos only, 0 motores · `OWNER_ACCEPTANCE: REVIEW`

## Afirmación Q04 auditada

`CLF-Q04-ECONOMIC-ROOT-CAUSE.md` §9 y `CLF-Q04-STATUS.md` gate 9 afirmaban: "233 pases en las 63 configuraciones SG `COMPLETE_RECONCILED` (1.839 compras, 12,7%) y **24 configuraciones con pases dentro de la ventana NQU6** (pases hasta 2026-10-02; ej. SG-TG-CH300-F0-R500: 18 pases, último 2026-09-28 — un pase dentro del mismo trimestre)". La ventana NQU6 sellada termina `2026-09-13T22:00:00Z`.

## Datos y método

Dataset: `~/echo-work/runs/R03-PROTECTED-CLOSE/` (baseline R03, sha256 del censo económico `614109ad763e91f5…`, 89/89 `COMPLETE_RECONCILED`). Clasificación temporal por config desde `first_pass_at`/`last_pass_at` (`R03-ECONOMIC-ALL89.csv`) + extracción de **cada** transición `PLATFORM_ACCOUNT_STATE → CHALLENGE_PASSED` con timestamp exacto desde los streams `lab/<config>/out/*/economic.ndjson.gz` (las 8 configs ambiguas quedaron resueltas por evento; cero incógnitas). Scripts y salidas: `e05/r03_temporal_audit.py|json` y `e05/r03_spanning_finder.py|json`.

## Verificación numérica

- Totales **correctos**: 63 configs SG, 1.839 compras, 233 pases — verificados contra el CSV.
- **"24 configuraciones con pases dentro de NQU6": INCORRECTO. Valor real: 13 de 63** (7 con último pase dentro + 6 spanning verificados por evento; 2 spanning sin pase in-window: ORB-5M-R500 y TG-F0-R750).

## Los 13 configs con ≥1 pase real dentro de NQU6 (timestamp real)

| Config | Último pase in-window (UTC) | Evidencia |
|---|---|---|
| LAB-SG-FBC-CH300-15M-R750 | 2026-07-10T13:45:43Z | CSV first/last (11 pases) |
| LAB-SG-FBC-CH300-60M-R750 | 2026-07-07T14:35:23Z | CSV first/last (9 pases) |
| LAB-SG-MR-01-R750 | 2026-09-01T16:20:10Z | CSV first/last (4 pases) |
| LAB-SG-MR-07-R750 | 2026-07-21T14:38:37Z | CSV first/last (5 pases) |
| LAB-SG-MR-09-R750 | 2026-07-09T14:20:11Z | CSV first/last (5 pases) |
| LAB-SG-ORB-CH300-15M-R750 | 2026-08-17T15:07:40Z | CSV first/last (7 pases) |
| LAB-SG-TG-CH300-F1-TREND-R500 | 2026-07-21T15:06:39Z | CSV first/last (15 pases) |
| LAB-SG-ORB-CH300-30M-R500 | 2026-07-21T15:09:38Z | evento stream (1 in-window) |
| LAB-SG-ORB-CH300-30M-R750 | 2026-08-06T14:10:37Z | evento stream (1 in-window) |
| LAB-SG-ORB-CH300-5M-R750 | 2026-07-28T15:38:42Z | evento stream (1 in-window) |
| LAB-SG-TG-CH300-F0-R500 | 2026-06-26T17:30:18Z | evento stream (1 in-window; ver abajo) |
| LAB-SG-MR-04-R750 | 2026-08-21T15:55:19Z | evento stream (1 in-window) |
| LAB-SG-TG-CH300-F1-TREND-R750 | 2026-07-27T15:15:32Z | evento stream (1 in-window) |

## Ejemplo citado por Q04: SG-TG-CH300-F0-R500 (los 18 pases con timestamp)

15 pases 2023-10-25…2026-04-22 (ANTES de la ventana); **1 pase DENTRO: 2026-06-26T17:30:18.390Z (account/132)**; 2 pases DESPUÉS: 2026-09-15T17:11:33Z (account/149) y 2026-09-28T15:01:35Z (account/151). La frase "un pase dentro del mismo trimestre" resulta cierta, pero **los timestamps citados como soporte (último 2026-09-28; "pases hasta 2026-10-02") son eventos posteriores a la ventana y no la prueban**; el pase in-window real es el 2026-06-26 y no estaba citado.

## Corrección de la afirmación (texto sustituto)

El mismo motor y reglas E2T con horizonte que incluye NQU6 registran 233 pases en 63 configuraciones SG (1.839 compras, 12,7%); **13 configuraciones tienen al menos un `CHALLENGE_PASSED` con timestamp verificado dentro de la ventana NQU6** (2026-06-14T22:00Z → 2026-09-13T22:00Z), listados arriba; los pases de septiembre 15/28 y octubre 2026 son posteriores a la ventana y no cuentan como aprobaciones in-window. La conclusión cualitativa del control (el simulador y la cuenta no bloquean pases; la variable separadora es la frecuencia de entrada 0,1–2,4/día vs 0,02–0,10/día) **se sostiene** con la cifra corregida.

## Garantías

R03 NO se re-ejecutó (autoridad read-only `ae1b09bc`); cero motores; recibos write-once preservados; la corrección es de reporting y de evidencia citada, no de resultados.
