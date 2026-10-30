---
type: doc
schema_version: 1
status: active
area: "[[Personal]]"
project: "[[Polymarket Engine — MVP]]"
related:
  - "[[Research — Single Episode Public Pilot W1-j 2026-10-29]]"
  - "[[Polymarket Engine — Continuidad Five-POC 2026-09-20]]"
  - "[[Plan — Executable Single Episode Pilot W1-j 2026-10-29]]"
  - "[[2026-10-30-polymarket-w1j-causal-gate-summary]]"
  - "[[2026-10-30-zcode-glm-5.3-flash-polymarket-w1j-causal-gate]]"
aliases:
  - "W1-k causal gate diagnosis"
  - "W1-j gate adjudication"
tags:
  - kind/doc
  - topic/research-ops
created: "2026-10-30"
updated: "2026-10-30"
---

# Research — W1-j Causal Gate Diagnosis 2026-10-30

## Resultado actual

**El gate de costes v0.1 NO es no-positivo por construcción: un contraejemplo sintético plausible ejecutado contra la implementación congelada pasa el gate en ambos escenarios de fee (A-500 y S-1000, test `TestW1kSyntheticCounterexample` PASS, commit `c0c35e7`).** Lo que hizo negativas las 36 decisiones de señal del episodio sellado fue la FORMA del libro: widenings liderados por caída del bid con ask pegado, dejando el ask de entrada estrictamente sobre el nivel de referencia `L` (36/36 con `best_ask − L` ∈ [+0.005, +0.015] USD), de modo que el gross mark-to-`L` fue negativo en 36/36 (−1.1028 … −0.1838 USD por entrada virtual de 25) y las fees lo llevaron a −1069…−2397 bps, muy bajo el umbral congelado de +50 bps. **Decisión: el ensayo v0.1 se mantiene INCONCLUSIVE de un mercado** — no hay inconsistencia demostrada del harness (réplica del gate 72/72 exacta) — y la revisión económica queda especificada (no implementada, sin captura).

## Separación de hechos

1. **Identidad algebraica (fuente congelada).** Detección: `spread ≥ ref + widen_min_bps` con `spread = trunc((ask−bid)·10⁴/mid)` (`sports.go:267`, `:632`); `ref` = mediana inferior de las últimas 10 dispersiones previas al frame (sin look-ahead, `sports.go:319`). Salida: `L` = mediana inferior de las últimas 10 medianas de `mid` **incluyendo el frame de señal** (`sports.go:335`; `Detect` agrega en `:282` antes de que `Evaluate` lea `referenceLevel`). Gate: `netAtRef = L·size − entryNotional − entryFeeHigh − exitFeeHigh`, `netBps = trunc(netAtRef·10⁴/entryNotional)`, ACCEPT si `netBps ≥ 50` (`sports.go:522-556`); `size = floor2(min(entryBudget/bestAsk, askDepth))` (`:500`); `B* = (entryNotional+entryFeeHigh)/(size·(1−coef))` (`:546`). Fees por pata `notional × bps/10⁴` en `economics.BuildQuote` (`internal/economics/economics.go`); el schedule tipo venue `regimes.FeeSchedule.LevelCost` (`internal/regimes/schedule.go`, `rate·p^e·(1−p)^e·take`, TRUNCATE_6DP, provenance REAL_UNVERIFIED/SYNTHETIC_FIXTURE) es otra función, nunca aplicada en el piloto (ver ERRATA abajo).
2. **Condiciones para gross/net positivos.** `gross = size·(L − VWAP_entry) > 0 ⟺ bestAsk < L` (fills de un nivel): el ask debe cotizar estrictamente debajo de la mediana reciente de mids — una caída de precio de dos lados. Las fees exigen además `(L−VWAP)·size > entryFeeHigh + exitFeeHigh` (≈10% del precio bajo `L` a 500 bps/pata con los tamaños observados; ≈20% a 1000), más el margen de 50 bps.
3. **Episodio (artefacto sellado `93e7fe79…`).** En las 36 señales el ask quedó SOBRE `L`; `B* > L` en 36/36 — ni la reversión completa al nivel propio del escenario llegaba a empatar. El origen bid-led queda probado en el episodio por `best_ask > L` con widening de spread sobre `ref` (150–299 bps); el bid/mid del frame de referencia NO viajan en la fuente autorizada y no se inventaron (sólo estimados derivados de la identidad del spread truncado, etiquetados como tales en el extractor).
4. **Test (Engine real, ejecutado).** Ver sección Contraejemplo: PASS con las cinco formas exactas del perfil de recuperación.

## Datos: las 36 señales únicas

- **Dedup:** 72 filas de rechazo = escenario A (36) + escenario S (36) sobre el MISMO conjunto; clave `(asset, signal_seq)`; 0 filas sólo-en-A o sólo-en-S; `widenings_detected = 36` en ambos; `replication_match = true` en 72/72.
- **Estructura:** 18 instantes de frame × 2 activos complementarios del mercado 5784455 ("Will CA Mineiro win on 2026-10-29?", K=2026-10-29T22:30:00Z), en 3 ráfagas de 6 frames consecutivos (seqs 2057-2062 a 21:33:44.12Z, 2383-2388 a 21:34:31.17Z, 4420-4425 a 21:37:58.73Z). La información independiente ≈ 3 dislocaciones de libro, no 36 oportunidades.
- **Cobertura validada sin agregación:** assets de las señales == assets del plan (2); timestamps dentro del envelope efectivo [21:00:04.925Z, 22:21:22.701Z] y pre-K; 18,400 frames (18,393 usable); 9,200 registros WS.
- **Agregados (mediana inferior; min/med/max) sobre las 36:** spread 298/312/606 bps; ref 148/155/307 bps; widening 150/157/299 bps; `L` 0.325/0.36/0.675 USD; best ask 0.34/0.37/0.68 USD; ask−`L` +0.005/+0.01/+0.015 USD; gross mark-to-`L` antes de fees −1.1028/−0.56805/−0.1838 USD; entrada 24.9942/24.9968/24.999 USD; fees ambas patas A 2.44454/2.4710175/2.49049 USD (S: exactamente el doble); net gate A −1419/−1215/−1069 bps; S −2397/−2204/−2066 bps; shortfall vs 50 bps: A 1119/1265/1469, S 2116/2254/2447; profundidad de ENTRADA (ask) 59,691.96/76,651.11/92,806.55 shares; **profundidad de SALIDA: no consta en la fuente** (sólo `ask_depth_total`; la salida era el nivel sintético `L`, jamás profundidad observada — no se inventa); tamaño virtual 36.76/38.46/73.52 shares; `B*` A 0.3758/0.4089/0.7516 USD.

## Ejemplos (regla fijada antes de inspeccionar: min/mediana/max del gross antes de fees; desempate `asset`, `signal_seq`)

- **Min gross (−1.1028 USD):** asset `612966…`, seq 4420, ask 0.34 vs `L` 0.325, spread 606/ref 307, size 73.52, net A −1419 / S −2397.
- **Mediana (−0.56805 USD):** asset `503062…`, seq 2383, ask 0.66 vs `L` 0.645, spread 307/ref 155, size 37.87, net A −1215 / S −2204.
- **Max gross (−0.1838 USD):** asset `503062…`, seq 4420, ask 0.68 vs `L` 0.675, spread 298/ref 148, size 36.76, net A −1069 / S −2066.

## Contraejemplo — test del Engine real (ejecutado)

`internal/strategy/pocs/sports/w1k_synthetic_counterexample_test.go` (commit `c0c35e7`, único archivo, sin tocar fuentes de producto; helpers existentes del paquete; parámetros congelados del piloto: window 300s, ref 10, widen 50, budget 25, umbral 50, taker):

- **Contraejemplo (caída de dos lados, ask bajo `L`):** historia 10 frames bid 0.54/ask 0.56; shock bid 0.40/ask 0.44 → spread 952 ≥ 413 → señal; `L`=0.55 > ask 0.44; gross +6.2491 sobre entrada 24.9964; net +1375 bps (A) y +250 bps (S) ⇒ **ACCEPT en ambos escenarios**.
- **Control del patrón del episodio (bid cae, ask pegado):** shock bid 0.49/ask 0.56 → señal con `L`=0.55 < ask 0.56; gross −0.4464 (−178 bps incluso a fee 0); **REJECT `REVERT_INSUFFICIENT_AFTER_COSTS` en ambos escenarios** — exactamente el patrón de las 36 señales.

Ejecución real (formas exactas del perfil, caches offline, GOMAXPROCS=2, GOMEMLIMIT=1536MiB, prlimit as=2GiB/cpu=900, toolchain local pinneada): test-only PASS (0.005s), suite completa del paquete PASS (0.014s), build exit 0, `gofmt -w`/`-l` limpio. Commit local `c0c35e7` «test: verify frozen widening counterexample», sin push.

## Límites

- Un episodio, un mercado, 1 cluster; sin IC, sin potencia, sin claim de rentabilidad; fee UNRESOLVED, REAL_FEE_READY=false; detección ≠ fill; `L` es escenario, no ejecución; el bid/mid del frame de referencia no consta en la fuente autorizada (sólo derivados etiquetados); el SQLite del episodio (`engine.db`, proyección de regimes) nunca se abrió — la descomposición viene del artefacto de revisión sellado cuyo generador re-procesó los mismos frames con las funciones congeladas.
- **Extracto de recuperación (recovery-v2):** `verified_extractor.py` quedó escrito e inspeccionado (un único input sellado, sin SQLite/red/subprocess/eval; salidas sólo en recovery-v2), pero su ejecución `/usr/bin/python3 <ruta>` fue denegada 3× por el guard de la superficie — la derivación verificada `verified-diagnostics.json` queda NOT_RUN con causa; el artefacto previo `episode-diagnostics.json` (sha256 `a966b1ff…`) permanece **no acreditado como ejecución** y se usa sólo como borrador analítico cotejable, nunca como output de corrida.
- Este shot es offline sobre el episodio ya sellado; sin red, sin cuentas, sin OOS, sin órdenes; el freeze de producto sigue siendo el estado de producto.

## Decisión

1. **El ensayo v0.1 queda INCONCLUSIVE de un mercado** (no se rechaza su estimación: no hay bug contable demostrado — réplica 72/72 y cobertura/identidad verificadas).
2. **Propuesta de revisión económica, sólo especificada:** condición de nivel en la detección o en el gate — señalizar sólo cuando `bestAsk < L·(1 − margen)` con `margen` preregistrado ≥ fee total esperada del escenario condicional + margen del gate (orden de magnitud ≥12% bajo `L` con los tamaños observados; valor exacto a fijar en preregistro, sin tuning). Evidencia requerida antes de código/captura: (i) enmienda del prereg PE-005-R1 (secciones 5/6); (ii) re-procesamiento offline de los episodios sellados midiendo cuántos eventos habrían calificado con `ask < L` y su distribución mark-to-`L`; (iii) sólo con esa evidencia, lote nuevo preregistrado. Nada de esto autoriza captura hoy.
3. **Errata de comisiones registrada** (ver abajo y [[Research — Single Episode Public Pilot W1-j 2026-10-29]]): A (500 bps) y S (1000 bps) son sensibilidades lineales legacy del Engine (`notional × bps/10,000` por pata, `BuildQuote`), NO la fórmula actual del venue ni certificación; el schedule tipo venue es `FeeSchedule.LevelCost` y nunca se aplicó; fee del mercado UNRESOLVED, REAL_FEE_READY=false.

## ERRATA (2026-10-30) — sensibilidad de comisiones del cierre W1-j

El cierre W1-j presentó la sensibilidad A como si fuera una aplicación validada de la fórmula actual de comisiones del venue. No lo es. **A (500 bps) y S (1000 bps) son sensibilidades lineales del modelo legacy del Engine, cobradas por pata como `notional × bps/10,000`** — demostrado por `economics.BuildQuote` (`internal/economics/economics.go`, FeeLow/FeeHigh = notional × coeficiente vía `regimes.BpsToFeeCoefficient`, `internal/regimes/feeresolver.go`) — **no** la fórmula actual del fee schedule del venue ni una certificación de comisiones. El modelo con forma de venue que el Engine sí implementa es `regimes.FeeSchedule.LevelCost` (`internal/regimes/schedule.go`): `cost = rate·price^exponent·(1−price)^exponent·take` por nivel llenado (familia `price_square_v1`, truncado a 6 decimales, exponente observado 1), aplicado sólo vía `economics.BuildQuoteScheduled` (`internal/economics/scheduled.go`) y sólo sobre resolución POINT, con provenance REAL_UNVERIFIED o SYNTHETIC_FIXTURE — nunca una tarifa certificada. Las dos formas (lineal por pata vs price-square por nivel) son funcionalmente distintas. Los números del análisis W1-j y su revisión permanecen como historia del modelo que se ejecutó; no se reetiquetan como P&L. La fee aplicada al mercado sigue UNRESOLVED / REAL_FEE_READY=false. Sidecar íntegro en el paquete: `analysis-revision-w1j-20261029/ERRATA-fees-w1k-20261030.md` (sha256 `a7665be1b12f414e8833c6747ac31e44e51a99a9286c9b904ef806beafdbec2a`).
