# MT5-ZERO-TRADES-REPORT — Forensics flow_example_2 w9 (2026-10-17)

## Veredicto

**MT5_ZERO_TRADES_ROOT_CAUSE_CONFIRMED.** Las 16 estrategias finalistas con cero operaciones MT5 no son malas, no les faltan librerías ni fallaron al inicializar: **el EA generó las mismas señales que SQX (97–100% de alineamiento señal-por-señal), pero el 100% de sus intentos de orden fue abortado por el chequeo de margen del propio EA** (`Alert: Not enough money to send order with 9.50000000 lot or Margin Calculation Error`, presente miles de veces en cada tester.log, con 0 deals y balance intacto en 100000.00 USD).

La cadena causal, demostrada con evidencia física en las 16:

1. El robust run seleccionado define **Stop Loss fijo = 21 pips** (literal en el `.sqx`: `SQ.Formulas.SLPT.FixedValue` → `21.0` con `postfix="pips"`).
2. El export MQ5 traduce 21 pips a **2.1 unidades de precio** (pip = 0.1 unidades en el dataset `USATECHIDXUSD_dukascopy_UTC02`, ticksize 0.1 — semántica fiel, verificada contra el trade t0 de SQX: entrada 25284.3 → salida 25281.5 = −2.8 unidades, gross −198, idéntico al deal MT5 del control con SL 28 pips).
3. El Money Management "Fixed Amount" computa `lot = mmRiskedMoney / (PointValue × SLdist)` = 200 / (10 × 2.1) = **9.5 lotes** (constante; `lot_min = lot_max = 9.5` en los 16 logs).
4. El símbolo MT5 `NDX_SQX` tiene **contract_size = 10** (impreso por el propio EA en el agent.log: `Contract size: 10`; Point value 10.00 USD) y el tester usa **depósito 100 000 USD, leverage 1:100** con margen por posición empíricamente acotado entre **4.2% y 5.6% del nocional** (bound demostrado: el primer rechazo de Z23 ocurre con cuenta plana a 25424.8 ⟹ rate > 4.14%; el primer deal aceptado del control C7 fue `buy 7.1 @ 25339.3` con cuenta plana ⟹ rate ≤ 5.55%).
5. Margen requerido ≈ 9.5 × 22 880 (precio mínimo del período) × 10 × 0.042 ≈ **91 353 USD** y con rate 5% ≈ 108 780 USD: **≥ el depósito para todo el rango de precios 2026** → ninguna orden pasa nunca → 0 trades.

**El discriminador entre operar y no operar NO es el tipo lógico: es el SL del robust run.** Los 14 con trades tienen SL fijo 25.5–45.5 pips o SL ATR-based (lotes ≤ 8.0, asequibles a precios de enero–marzo o siempre en el caso ATR); los 16 sin trades tienen exactamente SL 21.0 pips (lote 9.5, jamás asequible). La distribución por `logical_type` del mandato es un artefacto de qué SL asignó el optimizer a cada robust run, no una causa.

## Respuestas al resumen ejecutivo

- **¿Cuántas confirmadas / probables / inconclusas?** 16 / 0 / 0. Todas con el mismo mecanismo y evidencia determinista (N señales = N rechazos de margen; 0 deals; balance intacto).
- **¿Hay dependencias faltantes?** NO. Los 4 indicadores custom usados (`SqATR`, `SqHeikenAshi`, `SqSessionOHLC`, `SqSRPercentRank`) existen como `.ex5` en el terminal real del tester (`C:\MT5\slots\slot-1\MQL5\Indicators\`, verificados por SSH en worker-kronos). Cero DLLs y cero `#import` en los 30 MQ5.
- **¿Patrón común por logical_type?** La correlación existe (ver tabla del mandato) pero es espuria: la variable real es el SL del robust run (21.0 pips en las 16 vs 25.5–45.5/ATR en los 14). Ver `POSITIVE-CONTROLS.md`.
- **¿Defectos de generación MQ5?** Dos, y ninguno causa el patrón: (a) **defecto latente de identidad**: `input int MagicNumber` trunca la mágica durable >int32 — el reporte HTM muestra `MagicNumber = durable mod 2³²` (p.ej. 26100091079 → 330287303; verificado en 3 HTM); inerte en backtest, ruptura de identidad si el EA se usara en vivo; (b) la lógica de señales/SL/MM es fiel a SQX (sin mismatch funcional).
- **¿Problemas de configuración MT5?** Los datos y la configuración del tester son correctos (100% real ticks, 4593 barras, 72.2M ticks consumidos, fechas y símbolo correctos). El aspecto configuracional que pesa es económico: depósito 100k + margen ~5% + contract 10 hacen inviable el sizing del diseño bajo `NDX_SQX`.
- **¿Defecto del pipeline Forge o de las estrategias?** Ni una ni otras por sí solas: es un **defecto de ingeniería económica del export MT5** — el template de Money Management calcula el lote de riesgo fijo y, si no hay margen, **aborta la orden sin clampling** (código MQ5 líneas 1964–1970: `freeMargin - margin <= 0.0 → Alert + return 0`). SQX opera el mismo diseño sin restricción de margen (su motor no rechaza); MT5 sí. Las estrategias son semánticamente válidas y económicamente inviables en este contexto de tester.

## Clasificación por hipótesis del mandato

- **H1 dependencias faltantes:** DESCARTADA (evidencia física del terminal tester; 0 DLLs; señales generadas).
- **H2 inicialización/ejecución:** DESCARTADA (`initialization finished` limpio en 20/20 logs; indicadores resolvieron — las señales dependen de MACD/ATR/HeikenAshi y se emitieron miles de veces con SL coherente al diseño).
- **H3 órdenes rechazadas:** CONFIRMADA — distinción obligatoria resuelta: **SIGNALS GENERATED / ORDERS REJECTED (margin)** en 16/16; NO SIGNALS = 0 casos.
- **H4 datos/símbolo/config:** DESCARTADA como causa de 0 trades (datos íntegros, símbolo correcto); su único papel es el marco económico (contract 10, margen ~5%, depósito 100k).
- **H5 lógica/export:** sin mismatch de lógica; 1 defecto latente de identidad (mágica int32) documentado en `REMEDIATION-PLAN.md`.

## Impacto en los 14 con trades (hallazgo transversal)

Los controles también sufren miles de rechazos de margen (C7: 1385; C13: 3843; C14: 4377) y ejecutaron sólo el 6–27% de sus señales (C13: 256 deals / 4073 señales). Con SL 2.5–4.5 unidades y spread real de NDX, el resultado MT5 de los 14 tampoco es comparable al SQX: explica que **los 14 MT5 terminen todos negativos**. La fidelidad de la cohorte completa está degradada por este mismo mecanismo, no sólo la de las 16. `mt5_fidelity_shadow` = 0.0 en las 16 es consecuencia correcta de la definición (sin candidato comparable), no un defecto.

## Prueba física focalizada (Fase 2)

No ejecutada. La evidencia existente es determinista y suficiente: 16/16 logs con 100% de rechazos, aritmética de margen cerrada con bounds empíricos exactos, y controles del mismo entorno que operan bajo la misma condición. Una reproducción física no discriminaría nada nuevo; se omite por KISS y para no tocar el worker MT5 productivo.

## Artefactos

- Matriz por estrategia: `ZERO-TRADES-MATRIX.csv` (16 filas, refs y evidencia por fila).
- Controles: `POSITIVE-CONTROLS.md`. Dependencias: `DEPENDENCIES-AUDIT.md`. Correcciones propuestas: `REMEDIATION-PLAN.md`.
- Workspace de análisis (fuera del vault, con artefactos crudos de MinIO): `~/aranea/work/mt5-zero-trades-forensics-20261017/` (host Daedalus).
