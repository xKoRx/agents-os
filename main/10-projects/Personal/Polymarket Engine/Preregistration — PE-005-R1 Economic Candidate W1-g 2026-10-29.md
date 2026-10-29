---
type: doc
schema_version: 1
status: active
area: "[[Personal]]"
project: "[[Polymarket Engine — MVP]]"
related:
  - "[[Plan — Economic Hypothesis Data Acquisition W1-g 2026-10-29]]"
  - "[[Research — Economic Strategy Specification W1-g 2026-10-29]]"
  - "[[Preregistration — First Hypothesis W1-f 2026-10-29]]"
  - "[[Polymarket Engine — Continuidad Five-POC 2026-09-20]]"
aliases:
  - "W1-g preregistration PE-005-R1"
  - "PE-005-R1 economic preregistration"
tags:
  - kind/doc
  - topic/research-ops
created: "2026-10-29"
updated: "2026-10-29"
---

# Preregistration — PE-005-R1 Economic Candidate W1-g 2026-10-29

## Propósito

- Preregistro económico **completo y ejecutable por especificación** de UNA candidata existente: **PE-005-R1 "pre-match spread reversion"** (familia PE-005, engine `poc-sports` v1, `internal/strategy/pocs/sports/sports.go` @ `853c0e4`). Especifica el experimento de falsación ANTES de adquirir cualquier dato nuevo. No promete beneficios, no optimiza parámetros y no abre live.
- Estado al congelar: checkout `w0/offline-causal-replay-20261027` @ `853c0e46c9be2de4e84201e240e9cf8366b1036e` limpio; **cero datos nuevos adquiridos** para esta candidata; OOS históricos ATL `3901955` / SEA `3901953` permanecen sellados; el OOS **nuevo** aún no existe (sin IDs inventados).
- Entradas del autor (ningún resultado económico consultado): continuidad canónica §§1–18, manifests W1-b/W1-c/W1-d/W1-f (sólo metadata/contadores ya generados), fuente Go del Engine, y documentación pública de fees citada en [[Research — Economic Strategy Specification W1-g 2026-10-29]].
- Límite epistémico registrado: la copia de máquina y su hash en OUT demuestran **disponibilidad e integridad del artefacto al sellarse**; no constituyen prueba independiente de que la redacción precedió a toda inspección previa (la evidencia de orden es la del registro observable de la sesión).

## Contenido

### 1. Identidad de la hipótesis

- **ID:** `PE-005-R1-E1` (primera falsación económica de la revisión R1; el registro del engine mantiene la traza padre PE-005 → PE-005-R1).
- **Enunciado falsable:** en mercados moneyline deportivos de Polymarket, ANTES del kickoff, un ensanchamiento del spread de un outcome frente a su propia mediana reciente viene seguido, dentro de `window_ms`, de una recuperación del mejor bid hasta el nivel de break-even B\* (round trip taker completo con fee al bound superior conservador) en una fracción de señales estrictamente mayor a 0,50.
- **Veredicto NO económico:** este experimento mide factibilidad de la ruta (reversión que repara costes completos). Nunca certifica rentabilidad, alpha ni autoriza órdenes; la certificación económica exige además el gate de fee (§13).

### 2. Universo y exclusiones

- **Universo:** mercados Gamma con `sportsMarketType == "moneyline"` (case-insensitive), `closed==false`, `active==true`, `acceptingOrders==true`, `umaResolutionStatus` ausente/vacío, `gameStartTime` parseable y futuro al momento de selección, `conditionId` y exactamente 2 `clobTokenIds` no vacíos (regla ex ante idéntica a la v6 ya ejecutada y probada en W1-d; `gameId` NO es requisito).
- **Exclusiones duras:** (a) OOS históricos `3901955`/`3901953` — jamás consultados, seleccionados ni inscritos (gate id-only pre-interpretación); (b) mercados no-moneyline, combos y parlays; (c) mercados cuya ventana de observación intersecte la pausa 02:00–08:00 GMT-3 (censura preregistrada, §10); (d) cualquier mercado cuyo kickoff no esté disponible como hecho capturado ex ante (jamás inferido de `startDate`/`endDate`/`createdAt`).
- **Sin nuevos IDs consultados:** este preregistro no consulta Gamma hoy y no asigna IDs; la selección real correrá bajo `catalog select` con nuevo preregistro de máquina vinculado por hash.

### 3. Identidad mercado/outcome y disponibilidad temporal

- **Unidad de decisión:** un outcome asset (token) de un mercado moneyline; el instrumento es el par bid/ask observado de ese asset.
- **Kickoff:** `gameStartTime` convertido a UTC exacto, capturado en la selección (hecho de calendario publicado ANTES de la ventana; legítimo para uso ex ante). Pasa al strategy como `kickoff_ms` (epoch ms). Jamás se sustituye por tiempo editorial o reloj actual: `kickoff_ms<=0` bloquea toda señal (comportamiento v0.1).
- **Relación al kickoff:** sólo señales estrictamente pre-match (`nowMs < kickoffMs`). La ventana de observación por episodio es `[kickoff−90min, kickoff)`. Post-kickoff el strategy bloquea (`blocked++`) y no hay señales nuevas.
- **Metadata (tick/fee):** observaciones CLOB con `known_at` = recepción real del journal; vigencia prospectiva `TTL=15 min` (política de investigación congelada en W1-e); re-polls preregistrados cada ≤15 min dentro de la ventana (Plan §4) para que el gate real no degrade a stale por diseño.

### 4. Señal numérica (unidad, lookback, referencia, umbral)

- **Magnitud:** `spread_bps = (ask−bid)·10000/mid`, truncado a entero, sobre el mejor bid/ask de libros OBSERVED_USABLE no cruzados.
- **Lookback:** últimos `ref_frames=10` frames del MISMO asset (mediana de spreads para detección; mediana de mids para el nivel de referencia L). El frame actual jamás entra a su propia referencia (por construcción v0.1).
- **Umbral de detección:** `spread_bps >= ref_bps + widen_min_bps` con `widen_min_bps=50`.
- **Valores ex ante:** `window_ms=300000`, `ref_frames=10`, `widen_min_bps=50`, `entry_budget=25`, `min_net_edge_bps=50`, `taker=true` — el conjunto **congelado el 2026-09-21** en la campaña Sports Week (anterior a todos los datos W1-b…W1-f), reutilizado sin ajuste. Alternativa descartada registrada: `widen_min_bps=150` (convención del fixture fivepoc, no de campaña). Ningún parámetro se elige mirando resultados.

### 5. Fee: escenarios etiquetados y prohibiciones

- **Prohibido:** default fee 0; inferir `mbf/tbf=1000` como "10% aplicable"; tratar `fee_rate_bps=0` de un trade como certificación de fee nula.
- **Escenario A (fórmula documentada, taker):** `fee[USDC] = C·rate·p·(1−p)` con rate 0,05 deportes (vigencia desconocida para nuestros mercados; docs actuales 2026-10-29). Como fracción del notional: `rate·(1−p) < rate = 5%`.
- **Escenario B (cap legacy, engine-native):** `mbf/tbf` (bps, "charged on proceeds") como CAP → INTERVAL [0, 1000] bps con supuesto U-02 (estado actual medido en W1-e/W1-f).
- **Elección ex ante del experimento:** `fee_low_bps=0; fee_high_bps=500` — bound superior que **domina el Escenario A para todo p∈(0,1)** y es más preciso que el cap 1000 del Escenario B. Alternativa 1000 registrada y descartada (menos precisa, aún válida como cota). El strategy aplica FeeHigh en entrada y salida (conservador por diseño).
- **Gate de certificación (independiente, bloquea claims):** fee queda `REAL_FEE_READY=false` hasta (a) mapeo documental verificado de `mbf/tbf`↔`fd.r`↔fee aplicada, o (b) evidencia de trades convergente en ventana. El escenario A/B sigue siendo hipótesis etiquetada, no tarifa certificada.

### 6. Entrada, lado y precio

- **Entrada:** BUY taker del asset ensanchado, precio como **barrido conservador sobre la profundidad ask observada** (`WalkSide`), límite al **peor precio efectivamente barrido** (`sweep.WorstPrice`), tamaño `floor2(min(entry_budget/bestAsk, profundidad))`. Un solo lote; sin órdenes maker (v0.1 las rechaza: UNCALIBRATED).
- **Gate económico de admisión a medición:** sólo entra al set de medición la señal cuyo escenario "reversión al nivel L con salida taker" deja `net_bps >= min_net_edge_bps=50` con fees al bound (50 bps ya descontados); si muere por costes → `REVERT_INSUFFICIENT_AFTER_COSTS` (control negativo explícito, contado como `cost_killed`).
- **Tamaño VIRTUAL y exposición máxima:** presupuesto virtual total **USD 500** (futuro, estado TESTING, sin fondos ni cuenta verificados; jamás dinero real). Por entrada ≤ USD 25; exposición abierta simultánea ≤ USD 100; despliegue acumulado ≤ USD 500. Sin reentrada sobre una señal ya abierta del mismo asset.

### 7. Salida, riesgo y horizonte

- **Salida por precio (primaria):** el mejor bid observado del asset alcanza B\* = `(notionalEntrada + feeHighEntrada) / (tamaño·(1−feeHighCoef))` dentro de `window_ms=300000` → evento `reverted`. B\* ≥ ask de entrada en libro no cruzado (por construcción).
- **Salida temporal:** al expirar `window_ms` sin toque de B\* → `not_reverted` (con B\* conocido) o `unevaluated` (B\* desconocido).
- **Riesgo:** long-only virtual; pérdida máxima por señal = coste de entrada del escenario (USD ≤ 25); sin stop-loss en v0.1 (declarado); sin apalancamiento; 0 órdenes reales en todo el experimento.

### 8. Abstenciones y datos faltantes (fail-closed)

Bloqueo o inconcluso explícito, jamás sustitución por valores inventados: kickoff desconocido/atrasado (`blocked`); fee no declarada (`FEE_UNRESOLVED`); profundidad no observada o insuficiente (`DEPTH_UNOBSERVED`/`INSUFFICIENT_DEPTH`); referencia indisponible (`REFERENCE_UNAVAILABLE`); libro cruzado o inválido (`INVALID_MODEL`); calidad ≠ `OBSERVED_USABLE` (frame fuera del estudio); tick stale (>TTL) o cuarentena PIT → shard SYNCING → frame inelegible (contado en `frames_ineligible`). Cada exclusión es contada y reportada; ninguna se rellena.

### 9. Latencia, ejecución conservadora, slippage e impacto

- Decisión sobre el wall de recepción del frame (tiempo PIT de recepción; sin claim de PIT de venue). El barrido de entrada incorpora el impacto sobre la profundidad observada (walk de niveles). No se modela slippage más allá del libro observado (limitación declarada: la ejecución real enfrentaría consumo y cola no modelados). Sin latencia simulada: el toque de B\* se mide sobre libros recibidos; un trade que "hubiera tocado" fuera de recepción no cuenta.
- **Nofills:** los ACCEPT de SCREEN son elegibilidad de medición, jamás fills; los fills simulados sólo existen en SHADOW y se reportan aparte, jamás mezclados con trades observados de terceros.
- **Stale/empates/reconexión:** metadatos fuera de TTL → stale (bloqueo, no promoción); empates de venue-ms ordenados `(venue_ms, received_us, sequence)` con grupos de empate contados y marcados no-certificados; desconexión = epoch nuevo con gap declarado, continuidad jamás inventada; señal viva al cortarse sigue midiendo en el epoch siguiente y expira por su ventana si no hay frames.

### 10. Cortes, censura y pausa diaria

- **Cortes negativos de verificación causal:** T−75, T−45, T−15 min relativos al kickoff (los eventos recibidos en/tras el corte son invisibles en ese corte; verificación por replay y digests).
- **Censura preregistrada:** todo episodio con cualquier segundo de captura dentro de 02:00–08:00 GMT-3 queda **excluido** del set de falsación (truncado o abortado por stop-file a las 02:00). **No existen jobs nocturnos**: la pausa es completa y sin gracia.

### 11. Unidad independiente, tamaño de muestra e incertidumbre

- **Unidad independiente:** el episodio partido-mercado (cluster). La independencia binomial se asume **entre clusters**; la correlación intra-episodio se cubre con inflación conservadora del n y un requisito mínimo de clusters.
- **Cálculo ex ante (supuesto hipotético declarado):** objetivo detectar p1=0,65 vs p0=0,50, potencia 80%, α unilateral 0,05, varianza binomial: `n = [(1,645·√0,25 + 0,842·√0,2275)/0,15]² ≈ 67`; inflación por clustering ×1,3 → **n=90 señales del denominador primario** en **≥30 episodios distintos**.
- **Alternativa descartada:** p0=0,65 (n≈270, fuera de la factibilidad estimada del presupuesto de captura).
- **Métrica primaria:** θ = P(toque de B\* dentro de 300 s | señal ACCEPT con B\* conocido y ventana resuelta). **Decisión:** IC de Wilson unilateral 95% con límite inferior > 0,50 ⇒ `NOT_FALSIFIED_AT_THIS_GATE` (procede a gates de certificación); en caso contrario `FALSIFIED_NO_ADMISSION`. Se reporta además IC de dos lados y estimación por cluster (episodio).
- **Métricas secundarias (todas netas del fee al bound, ya dentro de B\*):** `net_at_ref_bps` (mediana y IQR de las señales ACCEPT), fracción `cost_killed`, `blocked`, frames inelegibles, señales por episodio. Los rellenos simulados de SHADOW se reportan separados y no entran al endpoint.
- **Sin análisis interino de outcome:** revisones de gobernanza durante la campaña leen SÓLO denominadores (frames elegibles, señales, accepted, cost_killed); `reverted`/`not_reverted` permanecen ciegos hasta el análisis final.

### 12. Split prospectivo exploratorio/OOS-nuevo

- **Bloque exploratorio:** los primeros **60 episodios** con ventana completa capturados bajo este preregistro (orden por kickoff ascendente). Su análisis produce el veredicto primario.
- **Bloque OOS-nuevo:** todo episodio posterior (kickoff > el del episodio 60). Permanece **sellado** (sin lectura de outcomes/métricas) hasta: (a) veredicto exploratorio registrado y hasheado, y (b) apertura explícita bajo los MISMOS parámetros congelados. Si el exploratorio es `FALSIFIED_NO_ADMISSION`, el OOS-nuevo no se abre y la campaña termina.
- **Prohibiciones:** OOS históricos ATL/SEA jamás se reutilizan ni re-etiquetan; el OOS-nuevo no tiene IDs hoy y no se le asignan inventados; sin re-spits, sin tuning post-hoc, sin redefinición de endpoints tras ver datos.

### 13. Criterios de suficiencia, no-admisión y abandono (sin tuning posterior)

- **SUFICIENTE:** ≥90 señales del denominador primario en ≥30 episodios → veredicto primario vinculante.
- **INSUFICIENTE (30–89 señales):** veredicto `INSUFFICIENT_DATA_FOR_PRIMARY_GATE`, sólo descriptivo; la candidata NO se admite ni se rechaza; prohibido ampliar ventana/umbral retroactivamente.
- **NOT_RUN económico (<30 señales o <8 episodios al deadline):** cierre sin claim; sólo reporte de cobertura.
- **NO-ADMISIÓN estructural (independiente del resultado):** fee sin pieza de certificación al cierre, o elegibilidad PIT de tick no demostrable en campaña → `NOT_ADMITTED_ECONOMICS_BLOCKED` con causa, aunque θ sea alto.
- **Abandono:** 2 semanas calendario consecutivas con 0 ventanas elegibles nuevas, o presupuesto de bytes/cuota agotado → cierre limpio con reporte; sin re-despacho con parámetros alterados.

### 14. Qué NO es este preregistro

No es promesa de beneficio ni estimación de alpha; no certifica fees ni ticks históricos; no habilita live, órdenes, cuentas ni fondos; no reabre el freeze de producto `PROJECT_FROZEN_OWNER_2026_09_23`; la presentación de un gate técnico (tests de infraestructura) jamás sustituye al resultado económico aquí especificado.

## Fuentes

- [[Polymarket Engine — Continuidad Five-POC 2026-09-20]] §§12–18 (params congelados Sports Week 2026-09-21; gates W1-e/W1-f).
- Fuente Go @ `853c0e4`: `internal/strategy/pocs/sports/sports.go` (mecanismo, gates, B\*, FeeHigh), `cmd/engine/{catalog_select,clob_observe,record,replay,experiment}.go`, `internal/transport/marketws/marketws.go`, `internal/experiment/experiment.go`.
- Fees (lectura as-of 2026-10-29, vigencia desconocida para mercados históricos): docs.polymarket.com `trading/fees`, `changelog/predictions`, `market-data/market-details`, `api-reference/markets/get-clob-market-info`, `programs/taker-rebates`; repos oficiales Polymarket/go-order-utils y Polymarket/py-clob-client. Citas completas y clasificación VERIFICADO/NOT_VERIFIED en [[Research — Economic Strategy Specification W1-g 2026-10-29]].
- Plan de adquisición mínimo que materializa este preregistro: [[Plan — Economic Hypothesis Data Acquisition W1-g 2026-10-29]].
