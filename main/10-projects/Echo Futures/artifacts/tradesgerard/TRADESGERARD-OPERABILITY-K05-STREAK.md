---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[TRADESGERARD-ENTRY-REPAIR]]"
  - "[[TRADESGERARD-OPERABILITY-T0]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-13"
updated: "2026-10-13"
---

# TRADESGERARD-OPERABILITY-K05-STREAK

## Hallazgo verificado

**La racha12 no alcanza el pase de ninguna cuenta.** Empieza en la primera operación: no existen pérdidas previas en esa campaña. Las primeras11 ganancias de `btg-functional`, todas EVALUATION, suman2495,22USD y dejan504,78 pendientes del target3000. La duodécima corresponde a la segunda cuenta EVALUATION y suma260,04USD allí. Racha agregada12=2755,26USD; racha de una misma cuenta/fase=11. Ninguna llegó a funded; por ello2300/3000 no eran todavía solicitudes de retiro elegibles.

No son doce TP de250: nueve netos son255,02; uno90,02 por liquidación NY; uno110,02 por objetivo parcial; otro260,04 con dos contratos. Los motivos causales proceden de `closure-reasons-final-88ed70d1.json.gz`: inferencia unívoca contra rama congelada y señales/terminación observadas, no del rol EXIT ni sólo del signo del PnL.

Al comienzo: cuenta1 balance50000, progreso0, mayor día0, piso EOD48000, piso diario48900, headroom1100; caja4880 tras compra120. Cuenta2 nace con progreso0 a20oct18:18Z. El20oct la operación11 deja día875,08; cuenta1 pasa `PAUSED_DAILY_GOAL` a18:03Z después del drenaje físico y conserva2495,22. En el siguiente cruce18:18Z, sin cuenta elegible, `OPPORTUNITY_PURCHASE` compra cuenta2 por120 y la oportunidad se entrega a esa cuenta. No se repartieron trades arbitrariamente; el cambio responde a pausa y frontera de compra causal C4.

Consistency30%: al corte de cuenta1,875,08/2495,22≈35,07%, además de faltar target. A3000,875,08/3000≈29,17% sería admisible: no hace falta aumentar el target por consistency. Cuenta2 tiene260,04/260,04=100% y faltan2739,96. MinimumTradedDays=0 en los términos efectivos C4.

## Las doce operaciones reales

A1=`btg-functional`; A2=`campaign/account/2`; fase EVALUATION en todas. Fechas UTC; el día contable es una identidad del ledger, distinto del día NY de entrada. R/T admitidos conservan la fracción exacta del productor. SL efectivo y barrera TP postfill no quedaron retenidos como economía explícita: el artefacto guarda órdenes protectoras/precios reales y netos, pero no inventa una barrera TP a partir del resultado. R es presupuesto admitido, no pérdida física garantizada.

|#|Cuenta / día contable|Entrada → cierre UTC|Neto / causa|R/T admitidos|Progreso antes → después|Mayor día después|Piso diario / EOD; headroom pre|Falta pase|
|---:|---|---|---|---|---|---|---|---:|
|1|A1 / ad-20251013|2025-10-14T18:12:00.909090909Z → 2025-10-14T18:13:26.213592233Z|255.02 / MM_CYCLE_TARGET_REACHED|1000/250|0 → 255.02|255.02|48900 / 48000; 1100|2744.98|
|2|A1 / ad-20251013|2025-10-14T18:34:00.895522388Z → 2025-10-14T18:38:17.076923076Z|255.02 / MM_CYCLE_TARGET_REACHED|1000/250|255.02 → 510.04|510.04|48900 / 48000; 67751/50|2489.96|
|3|A1 / ad-20251013|2025-10-14T18:45:01.052631578Z → 2025-10-14T18:48:51.6Z|255.02 / MM_CYCLE_TARGET_REACHED|1000/250|510.04 → 765.06|765.06|48900 / 48000; 40251/25|2234.94|
|4|A1 / ad-20251014|2025-10-15T19:02:00.48Z → 2025-10-15T19:07:11.578947368Z|255.02 / MM_CYCLE_TARGET_REACHED|1000/250|765.06 → 1020.08|765.06|2483253/50 / 2438253/50; 1100|1979.92|
|5|A1 / ad-20251014|2025-10-15T19:14:00.952380952Z → 2025-10-15T19:16:18.333333333Z|255.02 / MM_CYCLE_TARGET_REACHED|1000/250|1020.08 → 1275.10|765.06|2483253/50 / 2438253/50; 67751/50|1724.90|
|6|A1 / ad-20251014|2025-10-15T19:25:01.052631578Z → 2025-10-15T19:35:15.789473684Z|255.02 / MM_CYCLE_TARGET_REACHED|1000/250|1275.10 → 1530.12|765.06|2483253/50 / 2438253/50; 40251/25|1469.88|
|7|A1 / ad-20251016|2025-10-17T19:49:00.75949367Z → 2025-10-17T19:50:00.387096774Z|90.02 / STRATEGY_CLOSE_ALL_NY_SESSION|1000/250|1530.12 → 1620.14|765.06|1260753/25 / 1238253/25; 1100|1379.86|
|8|A1 / ad-20251019|2025-10-20T15:01:01.09090909Z → 2025-10-20T15:15:40.137931034Z|255.02 / MM_CYCLE_TARGET_REACHED|1000/250|1620.14 → 1875.16|765.06|2526007/50 / 2481007/50; 1100|1124.84|
|9|A1 / ad-20251019|2025-10-20T15:17:01.176470588Z → 2025-10-20T15:18:39.512195121Z|255.02 / MM_CYCLE_TARGET_REACHED|1000/250|1875.16 → 2130.18|765.06|2526007/50 / 2481007/50; 67751/50|869.82|
|10|A1 / ad-20251019|2025-10-20T15:29:01.363636363Z → 2025-10-20T15:55:46.56Z|255.02 / MM_CYCLE_TARGET_REACHED|1000/250|2130.18 → 2385.20|765.06|2526007/50 / 2481007/50; 40251/25|614.80|
|11|A1 / ad-20251019|2025-10-20T17:58:00.923076923Z → 2025-10-20T18:02:49.565217391Z|110.02 / MM_CYCLE_TARGET_REACHED|10494/25/5247/50|2385.20 → 2495.22|875.08|2526007/50 / 2481007/50; 93253/50|504.78|
|12|A2 / ad-20251019|2025-10-20T18:18:00.722891566Z → 2025-10-20T18:22:21.25Z|260.04 / MM_CYCLE_TARGET_REACHED|1000/250|0 → 260.04|260.04|48900 / 48000; 1100|2739.96|

Cada fila tiene pase=no por target pendiente y retiro=no por fase EVALUATION. Solicitud de referencia1000/250 en todas; operación11 admite419,76/104,94 debido a remanente diario104,94 (870−765,06), conserva rho4. Su neto110,02 incluye ejecución/ticks causales; no se cambia retrospectivamente la solicitud. Operación7 admite1000/250 pero termina por NY con90,02 antes del objetivo.

## Conciliación posterior y límites

Después de la racha, la pérdida13 en A2 es−999,96 y corta la campaña; pérdida14 en A1−999,98. No se usan esas pérdidas posteriores para explicar retrospectivamente el comienzo. Las25 filas completas, seis pérdidas, todas las órdenes, cuentas, días y transiciones están conservadas en el derivado. A1 final+460,46; A2 final−739,92; ledger global realizado−279,46. Balance nominal agregado99720,54 no es caja disponible.

Caja5000−2×120 compras−2×120 renovaciones=4520; cero créditos y pagos. Se conservan renovaciones13nov/19nov. Neto económico de caja−480; no se agrega el residual prop ni se debita otra vez la pérdida de trading. Los retiros2300/3000 C4 se verificaron separadamente y la equivalencia de pares está acreditada en C4; aquí el detalle físico principal es r3000.

No hay evidencia de defecto de pase/pago en esta racha: la primera cuenta nunca acumuló3000 y la segunda tampoco. La comparación de políticas nuevas usa este hallazgo histórico y no lo clasifica como bug retrospectivo.

## Evidencia reproducible

- Fuente C4 `88ed70d1ff9910bb157f1c14c0fed1d2b8e7ec49`; binario SHA256 `c8849bb6e5523e8625ead8282f0d97f98d8b02e14d72838e3c35de207c6bcd57`.
- ARANEA_ROOT relativo `work/tradesgerard-operability-20261013/verifier/k05-streak-reconstruction.json`, SHA256 `a838eaffb864f4c9d17706b2ca56a84ab62eaaeecef1d9c2d8d26f3eb3bd78d4`; extractor `reconstruct_k05.py`, reporte `write_streak_report.py`.
- Evidencia C4 `work/tradesgerard-entry-repair-20261013/verifier/{operation-account-day-aggregates-final-88ed70d1,monetary-authority-final-88ed70d1,closure-reasons-final-88ed70d1}.json.gz`; resultado/trace exactos referenciados dentro del derivado.
- Verificador independiente LOCAL, solicitado Sol6.1, modelo servido UNKNOWN. Derivado reutilizable HARNESS_TOOLKIT_CANDIDATE; no producto ni fixture incluido en ranking.
- Readback local realizado; sync master coordinado por manager.
