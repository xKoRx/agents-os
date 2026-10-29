---
type: doc
schema_version: 1
status: active
area: "[[Personal]]"
project: "[[Polymarket Engine — MVP]]"
related:
  - "[[Preregistration — PE-005-R1 Economic Candidate W1-g 2026-10-29]]"
  - "[[Plan — Economic Hypothesis Data Acquisition W1-g 2026-10-29]]"
  - "[[Research — First Hypothesis W1-f 2026-10-29]]"
  - "[[Polymarket Engine — Continuidad Five-POC 2026-09-20]]"
aliases:
  - "W1-g economic research report"
tags:
  - kind/doc
  - topic/research-ops
created: "2026-10-29"
updated: "2026-10-29"
---

# Research — Economic Strategy Specification W1-g 2026-10-29

## Propósito

- Informe de investigación del shot W1-g (one-shot GLM-5.3-Flash Max vía ZCode en `sqx-ulab-hefesto-0`): (1) por qué PE-005-R1 es la candidata económica elegida y qué es contrato existente vs preregistro nuevo; (2) evaluación por manifests+contratos de si los datos exploratorios existentes sirven; (3) investigación de fees en fuentes primarias públicas con citas y clasificación VERIFICADO/NOT_VERIFIED; (4) registro de las correcciones W1-f aplicadas. Sin ejecutar tests, capturas ni análisis de datos.

## Contenido

### 1. Contrato original PE-005-R1 (existente) vs preregistro nuevo

- **Contrato existente (fuente primaria, leída en el checkout @ `853c0e4`):** `internal/strategy/pocs/sports/sports.go` — "POC-S02 of Research Strategies v0.1: the pre-match spread reversion research strategy (identified revision PE-005-R1 of hypothesis family PE-005 — reversion after liquidity shocks — per the Edge Research Consolidado 2026-09-16)". Elementos contractuales verificables en código: `StrategyID=poc-sports`, `HypothesisID=PE-005-R1`, `Version=1`; detección por mediana propia de `ref_frames≥2` observaciones (el frame actual jamás entra a su referencia); señal sólo pre-match con `kickoff_ms>0` (desconocido ⇒ bloqueo, jamás inferido); entrada BUY taker barrida sobre profundidad ask observada con límite al peor precio; gate económico `net_bps >= min_net_edge_bps` con fees al upper bound (`FeeHigh`); break-even `B*=(notional+feeHigh)/(size·(1−feeCoef))`; medición de reversión = toque de B\* dentro de `window_ms`; maker rechazado (UNCALIBRATED); fee exigida POINT o INTERVAL (UNRESOLVED ⇒ `FEE_UNRESOLVED`); determinismo y ring acotado. Historia de campaña previa: params congelados 2026-09-21 (Sports Week, §14 de la continuidad): `window_ms=300000 ref_frames=10 widen_min_bps=50 entry_budget=25 min_net_edge_bps=50 taker=true cuts=30`.
- **Lo que NO es contrato original y SÍ es preregistro nuevo W1-g** (decisiones ex ante razonadas fuera de resultados, registradas en [[Preregistration — PE-005-R1 Economic Candidate W1-g 2026-10-29]]): el endpoint primario θ=P(toque de B\*|ACCEPT resuelto) con p0=0,50; `fee_low_bps=0/fee_high_bps=500` (domina la fórmula documentada; alternativa 1000 descartada); n=90 señales/≥30 episodios con inflación de clustering ×1,3; bloque exploratorio=episodios 1–60 y OOS-nuevo sellado; censura 02:00–08:00 GMT-3; cortes T−75/−45/−15; ventana de observación [K−90min,K) con re-polls ≤15 min; presupuesto virtual USD 500 y exposición ≤100 abierta; criterios de suficiencia/no-admisión/abandono.
- **Razón de la elección** (no se esquivó la difícil): PE-005-R1 es la única candidata existente cuyo mecanismo es medible con las capacidades reales del Engine (books→spread→taker sweep→gate de costes) sin canastas (PE-002), sin pares ML+spread (PE-001), sin vintages de forecast (PE-030) y sin cohorte de mercados nuevos (PE-004). Es además la única con params de campaña previamente congelados (2026-09-21, anteriores a todos los datos W1), lo que minimiza el riesgo de tuning. No se eligió otra candidata más fácil.

### 2. Datos exploratorios existentes: matriz de aptitud (por manifests+contratos, sin procesar raw)

| Dataset | Cobertura temporal | Receive/PIT | Categoría/identidad | Costes/fee | Inicio de evento | Esquema | Veredicto para PE-005-R1 | Qué sí aporta |
|---|---|---|---|---|---|---|---|---|
| W1-b replay (T21/T22 cohort, 4 MLB moneylines 2026-09-01, ventana [21:10Z,22:40Z)) | 90 min pre-kickoff (kickoff 22:40Z post-hoc) | receive-time; incidente 22:30–22:40 censurado; empates marcados | familia correcta (MLB moneyline); identidad CURRENT `as_of_verified=false` | 256 trades observados con `fee_rate_bps=0` — dato, NO certificación | kickoff `SCHEDULE_CORROBORATED_POSTHOC` — NO PIT | price_change/book/BBA/trades completos; 0 tick_size_change en ventana | **NO APTO para falsación** (tick PIT ausente ⇒ Qualities SYNCING ⇒ ruta económica cerrada por el gate del engine; kickoff no PIT bloquea `kickoff_ms` ex ante; fee sin certificar) | contexto de frecuencias/mecánica; prueba de cadena W1-b→W1-c; ancla de que la familia existe en el feed histórico |
| W1-b pkg-w1b8 (stage2 D/E congelados + identidad w1b6 pinneada) | ídem | ídem | ídem | ídem | ídem | derivados inmutables con contadores exactos (50.084 price_change, 544 book, 518 BBA no mapeados, 256 trades, 0 ticks) | **NO APTO** (mismas causas) | reproducibilidad (digests D=E idénticos) y derivados listos para re-import |
| W1-c journals D/E (import nativo del engine) | ídem | ídem | ídem | ídem | ídem | journals íntegros (frontier 50885) | **NO APTO** (SYNCING en 8/8 assets; shadow INCONCLUSIVE con fees UNRESOLVED) | demostración de integración histórica nativa, invariancia de schedule y comparabilidad D=E con un mismo digest |
| W1-d capture-v6 (4 moneylines futuros 2026-11-18, 5 min WS + metadata init/final) | 5 min, lejos de kickoff, ventana ≪ TTL 15 min | receive-time PIT demostrado (W1-f); re-poll fuera de ventana inexistente | familia correcta; selección v6 ex ante probada | metadata CURRENT: `fd{r:0.05,e:1,to:true}`, `mbf/tbf=1000`, tick `0.01`, min-size `5` — instantáneo, no vigencia | kickoffs ex ante legítimos (gameStartTime) | book completo por asset (20–22 niveles) | **NO APTO** (5 min ≪ TTL y ≪ window 300 s con historial; 0 trades/ticks; muestra de conveniencia) | prueba de cadena completa de captura (selección→venta→replay digest `b8c5854e…`), anclas de bytes por hora, y corroboración puntual de docs de fee/tick |
| W1-f evidencias (gate W1-e sobre capture-v6) | ídem | ídem | ídem | INTERVAL [0,1000]/UNRESOLVED, 0 POINT | ídem | contadores ya generados | **NO APTO económicamente** | gate causal demostrado; sus "predicciones P1–P7" son regresiones técnicas de semántica ya establecida en W1-e, NO evidencia económica nueva (corrección b) |

- Lectura transversal honesta: **ningún dataset existente sirve hoy para falsar E1** — pero NO por un blanket "incompleto": las causas son exactas y distintas por fila (tick PIT, kickoff PIT, fee, duración<TTL, muestra). "Mappings actuales no son universo PIT" (`as_of_verified=false`); snapshot inicial/actual de metadata no vuelve histórica una fee; un tick observado ANTES de la decisión es distinto de necesitar ver un tick cambiar (el gate prospectivo ya consume revisiones desde su recepción); el stale-test técnico de W1-f no es requisito económico del edge.

### 3. Investigación de fees en fuentes primarias públicas (lectura as-of 2026-10-29)

**VERIFICADO (URLs exactas, accesibles el 2026-10-29):**

- `https://docs.polymarket.com/trading/fees` — "Makers are never charged fees. Only takers pay fees." Ecuación: **`fee = C × feeRate × p × (1 − p)`** (C acciones, p precio, en USDC). Tabla por categoría (taker/maker/rebate): **Sports 0.05 / 0 / 15%**; Finance, Politics, Mentions, Tech 0.04/0/25%; Economics, Culture, Weather, Other 0.05/0/25%; Crypto 0.07/0/20%; **Geopolitics 0 (fee-free)**; Combos 0.05/0/0%. Rounding: "Fees are rounded to 5 decimal places. The smallest fee charged is 0.00001 USDC." Máximo deportes: $1,25 por 100 acciones en p=0,50.
- `https://docs.polymarket.com/changelog/predictions` — **Fee Structure V2 (2026-03-30)** con categorías; **deportes 0,03 → 0,05 el 2026-07-10 midnight UTC** (rebate 25%→15%); primera tarifa taker en crypto 15-min (2026-01-05, pico 1,56% en p=0,5); **2026-03-31: "Fees should now be calculated using the `feeSchedule` object within a market"**; **CLOB V2 (2026-04-17): "no more `feeRateBps` on orders", fees fijadas al match**; 2026-08-10: `grossInitialValue`/`entryFeesUsdc` en `/positions` (ausencia = no disponible, no cero).
- `https://docs.polymarket.com/market-data/market-details` — `FeeSchedule { rate: DecimalString; exponent: number; takerOnly: boolean; rebateRate: DecimalString }` (significados literales: base rate, exponente del componente de precio, taker-only, fracción de fee taker al maker). **La página NO da la ecuación completa ni el papel exacto de `exponent`.** Ticks válidos 0,1…0,0001; `0.0025` sólo World Cup to-advance/moneyline/spreads/totals; "Always read the active value from the market".
- `https://docs.polymarket.com/api-reference/markets/get-clob-market-info` — `GET /clob-markets/{condition_id}`: **`mbf`** y **`tbf`** = "maker/taker base fee in basis points" (ejemplo 0), **`fd {r: fee rate, e: fee curve exponent, to: takers only}`** (ejemplos 0,02/2/true — SIN `rebateRate`), `mts` (tick), `mos` (min size), `gst` (kickoff), `itode` (taker delay 250 ms), errores con `retry_after_seconds`. Sin ecuación.
- `https://raw.githubusercontent.com/Polymarket/go-order-utils/main/pkg/model/order.go` — campo legacy `Order.FeeRateBps`: **"Fee rate, in basis points, charged to the order maker, charged on proceeds"** — semántica de CAP maker sobre procedimientos, NO tarifa taker aplicada.
- `https://raw.githubusercontent.com/Polymarket/py-clob-client/main/py_clob_client/order_builder/builder.py` — el cliente NO calcula fees: `feeRateBps=str(order_args.fee_rate_bps)` es pass-through; `ROUNDING_CONFIG` tick 0,01 → precio 2 dp, size 2 dp, amount 4 dp.
- `https://docs.polymarket.com/programs/taker-rebates` — volumen ponderado `wV = Trade Size × (1 − Entry Price) × Category Weight × Bonuses`; "If a market's taker fee is 0 … no Weighted Volume and no rebate"; `rebate_bps` es rebate, no fee.

**Correspondencias investigadas:**

- `feeSchedule(rate, exponent, takerOnly, rebateRate)` (Gamma) ↔ `fd{r,e,to}` (CLOB) — misma tripleta rate/exponent/takerOnly; `rebateRate` documentado sólo del lado Gamma. Coherente con lo observado en capture-v6: `fd{r:0.05, e:1, to:true}` en 4/4 condiciones moneyline.
- `mbf/tbf=1000` observado: **NO existe fuente que documente el mapeo hacia `fd.r` o hacia la fee aplicada**. 1000 bps ≠ "10% aplicable"; el engine lo trata como CAP (INTERVAL [0,1000], supuesto U-02) y esa lectura sigue siendo la única sustentada por fuente primaria (go-order-utils: fee maker sobre procedimientos). Con la ecuación documentada, `fee/notional = rate·(1−p) < rate = 5%` para deportes: por eso el prereg fija `fee_high_bps=500` (domina el Escenario A) manteniendo el INTERVAL como escenario B.
- `fee_rate_bps` del trade (columna PendulumFlow / evento WS): **NOT_VERIFIED** — los intentos de localizar la página del schema del WS (`api-reference/trades/get-trades`, `developer/CLOB/websocket/market-channel`) devolvieron 404 y no se inventan URLs; el campo 0 observado en 256 trades históricos NO certifica fee nula (podría ser el campo legacy maker-on-proceeds sin setear).

**Conclusión fee:** la documentación actual resuelve el diseño **prospectivo** (escenario A acota la fee aplicada ≤500 bps de notional para deportes) pero **NO certifica nuestros mercados históricos** ni la vigencia por mercado; por eso el prereg separa (i) medición con bound conservador y (ii) gate de certificación (mapeo documental verificado o evidencia de trades convergente) que bloquea cualquier claim económico. Ambigüedad restante registrada como escenario etiquetado + bloqueo, sin fee-0 por defecto y sin forzar POINT.

### 4. Correcciones W1-f aplicadas (historia preservada, sin re-ejecutar nada)

- **(a) Orden prereg→medición:** en W1-f, la existencia y el hash del prereg al correr (y el fail-closed del harness) demuestran **artefacto disponible e íntegro al medir**, no que la escritura precedió a toda inspección previa. La evidencia de orden es la del registro observable de la sesión (transcripción + artefactos); las notas W1-f fueron corregidas con fe de erratas explícita; `frozen_before_measurement` queda como declaración registrada, no como prueba independiente por missing-file-gate.
- **(b) P1–P7 como regresiones técnicas:** las "predicciones confirmadas" ya eran semántica establecida por W1-e (gate prospectivo, TTL, cuarentenas PIT); su confirmación en W1-f es regresión técnica de la cadena, **no nueva evidencia económica**. El veredicto W1-f `DATA_SUFFICIENT_FOR_GATE_AVAILABILITY_TRIAL` es de disponibilidad técnica.
- **(c) 74 vs 8+73 — resuelta como UNIDADES DISTINTAS con residuo no conciliado:** `74` = **registros** de journal en la superficie `marketws/data` (`surface_histogram`, unidad: registro del journal; capture-status-v6 muestra 103 frames WS recibidos / 74 admitidos / 0 rechazados). `8+0+0+0+0+73=81` = **eventos** enumerados parseando los payloads de esos 74 registros con `ParseMarketWSFrame` (unidad: evento wire; cada registro puede traer múltiples eventos array-wrapped) — código de contadores: `internal/experiment/w1f_hypothesis_integration_test.go` (líneas del bucle de enumeración, contador por `rec.Envelope` vs por `env`). La ecuación "74 = 8+73" escrita en `W1-F-MANIFEST.json` y en las notas W1-f es una errata de confluencia de unidades: lo medido es "74 registros → 81 eventos clasificados (8 book + 73 no clasificados)". **No conciliado (desconocido exacto, nombrado sin releer frames):** qué registros traían >1 evento y si algún registro rindió 0 eventos; la diferencia 81−74=7 sólo acota que al menos 7 registros llevaron eventos múltiples. Los artifacts OUT de W1-f permanecen inmutables (son evidencia); la corrección vive en las notas canónicas y en el paquete OUT W1-g.
- Historia de manifests sobrescritos en corridas 2–3 de W1-f: preservada; no se recrearon bytes perdidos ni se certificaron intermedios por hash; desde la corrida 4 todo nombre lleva run-id.

## Límites

- Lectura documental as-of: la vigencia de fees/ticks para mercados pasados o futuros puede cambiar sin aviso ("can change at any time without notice"); ninguna tarifa queda certificada por este informe. Sin acceso a ayuda centrada en artículos de help center (rutas 404; se registran, no se inventan). Este informe no ejecuta nada y no constituye resultado económico.

## Fuentes

- URLs citadas en §3 (docs.polymarket.com; github.com/raw.githubusercontent.com de Polymarket/go-order-utils y Polymarket/py-clob-client), accedidas 2026-10-29 vía WebFetch HTTPS.
- Fuente Go del checkout @ `853c0e4`: `internal/strategy/pocs/sports/sports.go`; `cmd/engine/{main,catalog,catalog_select,clob_observe,record,replay,experiment}.go`; `internal/transport/marketws/marketws.go`; `internal/experiment/{experiment.go,w1f_hypothesis_integration_test.go}`.
- Manifests autorizados: W1-b (`exploratory-manifest.json`, `w1b-run-manifest-latest.json`), W1-c (`W1-C-MANIFEST.json`), W1-d (6 manifests v6 + `journal/manifest.json`), W1-f (`W1-F-MANIFEST.json`, evidencia 14:45:03Z p1), `.private-execution/w1g/inputs.json` (12 hashes, intachables).
- [[Preregistration — PE-005-R1 Economic Candidate W1-g 2026-10-29]] · [[Plan — Economic Hypothesis Data Acquisition W1-g 2026-10-29]].
