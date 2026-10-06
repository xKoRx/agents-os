---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo Futures]]"
  - "[[BTG-PLAN]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-06"
updated: "2026-10-06"
---

# BTG-S01-FUNCTIONAL-BASELINE-PROFILE

## Propósito

Fijar la configuración funcional offline elegida por el submanager bajo autorización nueva Owner; elimina el bloqueo de elegir reglas económicas para esta prueba, conservando trazabilidad y el objetivo de hacer funcionar backtesting. No acredita una prop o cuenta física ni cambia S2 o fórmulas GerardMM.

## Contenido

### Autoridad nueva

Owner 2026-10-06, respuesta a la pregunta de perfil real: «de momento deja una wea consistente, las reglas específicas las voy a iterar mas adelante. tu foco es hacer funcionar backtesting. deja las reglas consistentes, el único fin es hacer funcionar esta wea». Root tiene autoridad para seleccionar un baseline funcional explícito, no necesita recuperar un perfil físico inexistente para empezar. Se supersede exclusivamente el bloqueo de selección/configuración de este baseline; las políticas futuras de prop/funded/campaña siguen pendientes de S02. PnL negativo no se ajusta.

### Perfil seleccionado — BTG_FUNCTIONAL_NQ_EVAL_V1

| Campo | Valor cerrado / procedencia |
| --- | --- |
| Strategy | S2_H4_TREND_BB_PULLBACK_V1, implementación/defaults compartidos SMA50 H4/BB20/dev2/buffer1; no optimización. |
| Cuenta | Una cuenta in-process, inicial flat, USD100000; contexto SIM/GENERIC100K existente de BT-S01, elegido ahora para baseline funcional. |
| Provider | SIMRuleSet existente validado, sin mutar reglas D6/GAU50 ni atribuir restricciones de una prop. Terms de target/min traded days/consistency/trailing prop ausentes explícitamente. |
| GerardMM | Manager compartido, EVALUATION; SL USD2000/TP USD1500 cada account-day, expansión explícita FIXED_BUDGET_PER_ACCOUNT_DAY_V1 para la ventana observada. Extensión uniforme day3+ es elección funcional autorizada ahora, no recuperación de config actual ni herencia oculta day2. |
| Scaling | Omitido explícitamente (adds fail-closed en BACKTEST), política NO_ADDS_FUNCTIONAL_BASELINE_V1. No cambiar Manager ni emitir QuoteUpdate inventada para completar el port. Esta configuración no valida scaling; activarlo después requiere su trigger/modelo nativo correcto y evidencia nueva. |
| Boundary de cuenta | America/Chicago, 17:00, matching session start; warmup no consume ordinal. Atribución de intervalo exactamente coincidente con boundary debe estar fijada en el modelo antes del run; no backdate de facts. |
| Stage | EVALUATION único, sin transición funded ni campañas/compras/retiros. REPORT_RESIDUALS a horizonte; Outcome STOP ante terminalidad que el dominio efectivamente produzca. |
| NQ real | Tick0.25 puntos; USD20/point; USD5/tick. Snapshot por contrato físico, exact units; no usar NQFixtureContract cuyo pointvalue5 es fixture sintético declarado. |
| Costes modelados | Fee USD2.49 por contrato por fill/lado, slippage1tick, bid/ask modeled offsets1/1tick, TIF GTC, max mark age1m. Reutiliza importes del benchmark certificado, no pretende comisión Earn2Trade/NT observada. |
| Fidelidad | OHLC_1M_MODEL_V1, SL_FIRST_NEXT_OPEN_V1; entry MARKET posterior al BAR_CLOSE en próximo Open elegible de su contrato. Stops gap al Open adverso, SL antes de TP ante ambos en minuto. Los fills/marks son modelados, no BBO/ticks observados. |
| Calendario inicial | Modelo semanal CME-like, America/Chicago, sesiones Sunday..Thursday17:00 hasta día siguiente16:00, trade-date shift+1, break16:00..17:00; SessionGrid/tzdata compartidos. Sin overrides históricos inferidos: cualquier gap/early-close exige clasificación por evidencia antes de ampliar un claim longitudinal. El calendario semanal funcional no se presenta como calendario holiday completo. |
| Gaps/rollover | Ningún registro inventado/interpolado. Primera discontinuidad material esperada detiene o invalida readiness de forma explícita. Smoke un expiry con warmup51H4/20x5m; rollover multi-expiry se fija sólo tras manifiestos/coverage, sin mark del contrato nuevo para exposición vieja. |

Esta elección es operacionalmente consistente y limitada. Scaling desactivado es un campo del baseline elegido, no un cambio de señales, fórmulas o targets para mejorar rentabilidad. El port debe rechazar o diagnosticar explícitamente configuraciones de scaling no soportadas en vez de ignorar eventos; futuros tests no pueden convertir esta elección en default de producción.

### Gates pendientes

Originales NT completos siguen pendientes de transferencia autorizada: SFTP dev-win denegado por policy viewer, aunque los trece nombres y muestras son legibles. Se pidió ZIP del directorio al Owner mientras continúa implementación. Lector corregidoe44b741e, driver/venuee2e15a35 y account-day171fc712 tienen pruebas independientes acotadas; CLI198f29f4 materializa RunSpec/config/model/calendar digests y ejecuta el perfil compartido sobre corpus sintético, [[BTG-S01-NATIVE-INTEGRATED-FINAL-REVIEW]]. F09/F10 CLI están en remediación fresh. Original corpus/digests y corrida histórica siguen NOT_RUN; el cuadro no acredita ejecución histórica. Bajo baseline sin adds, ACCOUNT_ECONOMICS puede ejercitar TP/protection reales, pero no prueba toda la trayectoria GerardMM con scaling.

## Fuentes

- Autoridad directa Owner registrada arriba y [[BTG-S01-OWNER-S2-BARS-AUTHORITY]].
- [[Echo Futures — BT-S01 Backtester V1 Design]] §10.1 y código certificado fixtures/SIMRuleSet, experiment plan; benchmark Generic20 como fuente de valores explícitamente elegidos, datos sintéticos siguen REFERENCE_ONLY.
- [[BTG-S01-OHLC-RUN-CONTRACT]] para Mark/context y diferencia de triggers GerardMM; [[BTG-S01-NT-CANDLES-ACQUISITION]] para muestras y boundary de transferencia.
- [CME E-mini Nasdaq-100 Contract Specs](https://www.cmegroup.com/markets/equities/nasdaq/e-mini-nasdaq-100.contractSpecs.html), consultado2026-10-06, especifica20USD por punto y tick0.25. Horario semanal aquí declarado como modelo inicial, no validación completa de holiday schedules.
