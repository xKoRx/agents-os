---
type: resource
schema_version: 1
status: active
area: "[[Trading]]"
sources:
  - "[[echo-futures-dr03-deep-research-2026-10-28-source]]"
last_verified:
confidence: low
aliases:
  - "DR-03 mecanismos NQ"
  - "DR-03 cobertura Futures"
tags:
  - kind/resource
  - area/trading
  - project/echo-rnd
  - tech/futures
created: "2026-10-28"
updated: "2026-10-28"
---

# Echo Futures — DR-03 mecanismos NQ evidencia y cobertura

## Síntesis vigente

**Estado: RECEIVED_WITH_MATERIAL_FINDINGS / OWNER_REVIEW_PENDING.** Retorno Deep Research recibido el 2026-10-28 y conservado íntegro en [[FUT-R01-DR-03-mecanismos-NQ-2026-10-28]]. No demuestra estrategia viable, cobertura independiente, resultados NQ OOS ni utilidad económica de campaña. Aún no existe revisión independiente RV-01.

**PROPUESTA del worker (no aceptada):** cuatro líneas: momentum intradía, ORB adaptativo, gaps overnight y reversión tras exceso de volatilidad. Recomienda momentum primero y ORB después; eso no aporta necesariamente un segundo mecanismo, porque ambos pueden ser persistencia. Reversión transitoria podría ser alternativa, sujeto a contraste con MR.

**INFERENCIA taxonómica útil:** persistencia/continuación/pullback; reversión por exceso o presión transitoria; rupturas aceptadas frente a fallidas/recuperaciones. Apertura, sesión, VWAP, volatilidad y gap pueden ser contextos o medidas, no familias autónomas por usar otro indicador.

**DESCONOCIDO:** cobertura e independencia frente a TG/FBC/ORB/MR01–MR10. FBC sigue primera vela cerrada; ORB rompe rango; MR08 incluye recuperación local condicionada a tendencia H1. Sólo comparación real de reglas, señales y trayectorias permitiría establecer redundancia o independencia.

**Frontera de campaña:** evaluar asimetría de resultados, movimientos concentrados, rachas adversas, frecuencia y sequías, duración, fricciones y facilidad de tocar barreras. Sharpe, win rate >50% o esperanza positiva por trade no son gates universales. No hay probabilidades de pase/retiro inferidas aquí.

## Evidencia y provenance

- [[echo-futures-dr03-deep-research-2026-10-28-source]]: origen verificable con el texto íntegro de [[FUT-R01-DR-03-mecanismos-NQ-2026-10-28]].
- [[FUT-R01-RESEARCH-MANDATE]] v4: pregunta, restricciones de investigación, NQ exclusivo y separación Strategy/MM.
- [[Echo I+D — Cobertura Futures]]: inventario existente; no sustituirlo por clasificación de nombres en el informe.
- Bibliografía *mencionada, no verificada durante esta ingesta*: Baltussen et al. (2021, futuros); Gao et al. (2018); Rosa (2022); Holmberg et al. (2012, acciones suecas); Grant/Wolf/Yu (2005); Zarattini/Aziz/Barbon ([SSRN 4824172](https://ssrn.com/abstract=4824172), SPY).

## Límites y contradicciones

1. **Dirección temporal:** el informe dice que los últimos 30 minutos predicen el resto del día, invirtiendo predictor y tramo predicho de Baltussen; esto es material para evitar lookahead.
2. **Redundancia:** momentum y ORB adaptativo no constituyen necesariamente líneas económicas independientes; variar ventanas y filtros no prueba diversidad.
3. **Inventario mal inferido:** FBC no es failed breakout ni requiere ruptura; la cobertura TG/MR no se deduce por nombres o frases genéricas.
4. **Transferencia:** resultados SPY/ES/acciones suecas/futuros agregados no demuestran edge operativo NQ; periodos, costes y ejecución por instrumento pendientes de contraste en originales.
5. **Observabilidad:** OHLCV de 1 minuto no certifica orden intrabar stop-target, slippage, quotes/L2, presión de dealers ni ejecución.
6. **Refutación:** tasa de ganadoras >50%, Sharpe o expectativa positiva no son condiciones universales de utilidad de campaña; controles nulos y aleatorios deben ser comparables en exposición/frecuencia/costes.
7. **Datos:** cobertura real OHLCV NQ, sesiones/DST, roll, slippage y comisiones sin certificación física; tampoco OOS virgen ni sensibilidad a regímenes/decay.
8. **Autoridad:** el worker marcó RESPONDIDO; aceptación Owner y RV-01 siguen pendientes. No habilita implementación, pruebas, órdenes ni cambios de gates.

**Próxima decisión:** RV-01/submanager debe contrastar fuentes primarias, corregir refutadores, verificar cobertura real y escoger un primer mecanismo más una alternativa distinta; sin operaciones ni cierre Agents-OS.
