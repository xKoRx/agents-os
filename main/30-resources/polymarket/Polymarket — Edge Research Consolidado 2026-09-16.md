---
type: resource
schema_version: 1
status: active
area: "[[Personal]]"
project: "[[Polymarket Arbitrage — MVP]]"
sources:
  - "[[Polymarket DR R1 — Mecanismos y evidencia]]"
  - "[[Polymarket DR R2 — Microestructura y oráculo]]"
  - "[[Polymarket DR R3 — Anomalías estadísticas y 24 hipótesis]]"
  - "[[Polymarket DR R4 — Taxonomía y 20 hipótesis]]"
last_verified:
confidence: medium
aliases:
  - Polymarket edge research merge
  - Polymarket 4 deep research
  - Polymarket hypothesis research consolidated
created: 2026-09-16
updated: 2026-09-16
tags:
  - kind/resource
  - area/personal
  - tech/polymarket
  - topic/prediction-markets
  - topic/quant-research
---

# Polymarket — Edge Research Consolidado 2026-09-16

> **Función:** síntesis canónica de cuatro investigaciones aportadas el 16-09-2026. Conserva hallazgos, contradicciones, taxonomía, pruebas negativas y catálogo deduplicado. Es material de investigación, **no** un registro de alpha confirmado ni una autorización para operar.
>
> **Proyecto consumidor:** [[Polymarket Arbitrage — MVP]] · [[Polymarket Arbitrage — Opportunity Context]]. F0–F6 mantienen exclusivamente Sports Combinatorial + NegRisk; nuevas familias se investigan en F7+ y no cambian esa autoridad. Echo/Echo Forge permanecen en carriles separados.

## 1. Provenance y alcance real

| Fuente | Informe recibido | Aporte distintivo | Estado |
|---|---|---|---|
| [[Polymarket DR R1 — Mecanismos y evidencia]] | *Fuentes de edge automatizable en Polymarket: investigación desde mecanismo, datos y evidencia* | Diez hipótesis causales con experimentos y NO_GO, mapa de fuentes de datos, evidencia negativa en crypto BTC, restricciones de wallet history. | Síntesis recibida; claims individuales sujetos a fuente original. |
| [[Polymarket DR R2 — Microestructura y oráculo]] | *Descubrimiento de Edge Automatizable en Polymarket: Análisis Microestructural...* | Cuatro configuraciones concretas: maker geopolítico, post-event discount, NegRisk bundle, crypto maker con filtro spot; fallas open-source. | Escenarios numéricos no son predicciones verificadas. |
| [[Polymarket DR R3 — Anomalías estadísticas y 24 hipótesis]] | *Anomalías estadísticas en prediction markets: evidencia, mecanismos y agenda empírica para Polymarket* | 24 tests H1–H24; calibración vs retornos, weighting, incentivos, discontinuidades, diseño econométrico, sesgos. | Principal fuente de diseño del research de bajo coste. |
| [[Polymarket DR R4 — Taxonomía y 20 hipótesis]] | *Microestructura y Anomalías Estadísticas en Mercados de Predicción Descentralizados...* | Veinte hipótesis, oracle risk, market maturation, temporal patterns, rewards, clasificación de FLB. | Varios números y generalizaciones chocan con R1/R3; preservar como hipótesis, no facts. |

**Conteo:** 10 + 4 + 24 + 20 = 58 formulaciones nominales; NO representan 58 edges independientes. Este documento consolida **30 familias/hipótesis operables o investigables**, agrupa variantes y preserva líneas de medición que no son estrategias autónomas. IDs `PE-001...PE-030` son del merge; los H1/H2 originales sólo son válidos dentro de su fuente. La lista es un backlog de investigación, no un ranking de rentabilidad.

## 2. Tesis transversal y qué constituye evidencia

Un edge automatizable debe sobrevivir: precio **ejecutable por profundidad**, fees efectivos, slippage, staleness, fill/queue uncertainty, legging risk, resolución contractual, capital inmovilizado y prueba fuera de muestra. Un midpoint barato no es fill; spread ancho no es ganancia, volumen recompensado no demuestra información, un buen wallet PnL no implica copyability y un resultado acertado no prueba EV positivo.

Distinguir tres objetos estadísticos: **calibración** (`E[Y-p]`, Brier, log-loss), **retorno de una regla** (PnL neto a precio ejecutable) y **transferencia por flujo agregado** (ponderaciones por dólares/trades). Pueden mostrar signos diferentes. Para favorecer inferencia causal usar reglas publicadas y discontinuidades: rebates por fecha y categoría, reward thresholds y cambios del lifecycle, con controles y placebo apropiados.

Para hipótesis predictivas: `EV/share ≈ P_modelo(payout) - VWAP_ask - fees - costes - prima de resolución`; en baskets/arbitraje: payoff mínimo por estado menos coste de TODAS las patas realmente ejecutables. La mera desigualdad teórica no garantiza fills simultáneos ni payout sin disputa.

**Restricción de capital:** primera ventana tiny-live US$300 totales, no por estrategia; US$300–2.000 es sólo banda de investigación futura. Medir capacity y capital turns, mantener capital ocioso cuando no hay oportunidades, separar eventos correlacionados para no disfrazar concentración de diversificación.

## 3. Hallazgos convergentes de los cuatro informes

- **Las relaciones entre contratos importan:** S1 Sports combinatorial y S2 NegRisk explotan estructura del payoff, pero necesitan reglas exactas, simultaneidad de books, depth, fees y control de piernas. R1 cita estudio NBA con 290 episodios combinatorios frente a 7 simples; muestra histórica específica, no frecuencia live garantizada.
- **Calibración es condicional:** categoría, bucket, horizonte, parent-event, posición maker/taker e incentivos modifican los estimandos. R1/R3 advierten que un paper con 588 M trades halló FLB distinta en Crypto/Politics frente a Sports y que el signo de longshots cambia al cambiar ponderación. No aplicar regla universal de comprar favoritos.
- **Microestructura es el producto:** spread relativo en tails, depth decreciente hacia resolución, price impact, queue, adverse selection, open-market maturation y hours-of-week son señales examinables pero no edge probado neto.
- **Incentivos cambian comportamiento:** maker rebates, liquidity rewards y taker rewards pueden subsidiar actividad; volumen nominal puede aumentar sin mayor información ni mejor book. Versionar regla y régimen por timestamp.
- **Resolución es una variable económica:** reglas/fuente/edge cases prevalecen sobre título; distinguir resultado observable, proposal, disputa, finalización y redención. Un aparente winner a 98¢ puede reflejar lock, disputa o stale asks, no arbitraje libre de riesgo.
- **Wallets públicas son fills, no quotes:** wallet != persona; no inferir órdenes colocadas/canceladas ni maker strategy completa de history on-chain. Evitar supervivencia, selección y look-ahead.
- **Evidencia contraria importa:** R1 documenta el dataset OpenMarket BTC/Binance (~727 M filas, ~347 ms mediana de ajuste según informe) cuya estrategia walk-forward no mejoró el book y perdió tras costes. Contradicción directa a presentar lead-lag crypto como fuente automática de ganancias.

## 4. Datos y observabilidad: contrato mínimo de investigación

| Capa | Fuente sugerida en los informes | Qué habilita | Qué NO habilita |
|---|---|---|---|
| Catálogo/eventos | Gamma | parent event, categorías, market/outcomes, rules, negRisk, lifecycle | Book histórico o equivalencia semántica automática. |
| Quotes | CLOB REST + WS propio | Snapshot, incremental books, bid/ask/VWAP, staleness, oportunidad lifetime | Reconstruir retrospectivamente un book antes de iniciar el collector. |
| Históricos de trades/precios | Data API, CLOB price history, fuentes bulk cuando corresponda | Price buckets, resultados, wallet fills, calibración | Queue position, órdenes nunca ejecutadas, L2 histórico íntegro. |
| Incentivos | Fee info por market y endpoints rewards/rebates | Régimen, elegibilidad, competition, payout observado | Rebate futuro garantizado o fill probable. |
| Resolución | Rules, resolución/UMA y fuente primaria | Outcome, propuesta, disputes, time-to-redemption | Que titular o final de evento = settlement inmediato. |
| Benchmarks externos | Weather station/forecasts, options, sports sources, releases | Fair-value model y lead-lag OOS | Matching de contratos sin revisar expiración/source/rules. |

**Recordar:** UI price alterna midpoint y last trade cuando el spread supera US$0,10 según R1/R3. Guardar `best_bid`, `best_ask`, `midpoint`, `last_trade`, tamaños, exchange timestamp, receive timestamp, event timestamp y source separadamente. Usar decimal exacto; segmentar trades sin double-count maker/taker; distinguir tick grid y price clustering. Reproducir paridad sólo para sets exhaustivos mutuamente excluyentes verificados por las rules.

## 5. Catálogo deduplicado — 30 hipótesis para falsar

**Leyenda:** R1…R4 apuntan a las cuatro source notes anteriores. `MVP` indica que la familia ya pertenece a F2; `F7+` indica sólo backlog posterior. `Instrumental` es estudio que mejora detección o elimina falsos positivos, sin prometer PnL. Todos los experimentos son READ-ONLY de inicio. Los umbrales de NO_GO numéricos de una fuente son **supuestos de investigación**, no hechos universales ni parámetros para live: deben fijarse antes de ver los datos y justificarse por tamaño de muestra/costes.

| ID | Hipótesis falsable / mecanismo | Experimento mínimo y criterio de descarte a definir | Fuente / función |
|---|---|---|---|
| **PE-001** | Dislocaciones combinatorias Sports dentro de un mismo evento: libros se reprecian asíncronamente. | Rules→payoff matrix→WS books simultáneos→VWAP y fees para US$10/25/50; duración y todas las patas; NO_GO si net capturable/capacity son insuficientes. | R1 H1, R3 H19; **MVP**. |
| **PE-002** | NegRisk full basket y conversión parcial permiten monetizar desigualdades entre outcomes. | Reconciliar sets exhaustivos, rutas de adapter soportadas, `Other`, fees y partial fills; medir ganancias capturables, NO_GO por margen neto/capacidad. | R1 H1/H10, R2 H3, R4 H8/H9; **MVP**. |
| **PE-003** | Altas/bajas/aclaraciones de placeholders `Other` generan repricing semántico NegRisk. | Eventos de alta/cambio, snapshot antes/después, revalidar rules, full-depth opportunities; no asumir equivalencia estática. | R1 H10, R4 H8/H9; **MVP-subanálisis**. |
| **PE-004** | Nuevos listings nacen con error de precio/spread que disminuye con la madurez. | Capturar `new_market`, book a 1m/5m/1h, benchmark futuro SIN look-ahead de trading; NO_GO si sólo disminuye spread sin dirección predecible neta. | R1 H8, R3 H19; F7+. |
| **PE-005** | Shocks de consumo de liquidez sin noticia revierten tras recuperar depth. | OFI/price impact, eliminar news windows, respuesta 1s/10s/60s/5m, executable round trip; NO_GO si signo no estable OOS. | R1 H4, R4 H15; F7+. |
| **PE-006** | Entre resultado ya verificable y settlement existe a veces descuento ejecutable. | Join fuente primaria, ask, evento/UMA timeline; book +1s/+5s/+30s/+5m; descontar dispute/capital lock. NO_GO si la liquidez stale es ficticia o retorno ajustado <=0. | R1 H7, R2 H2, R3 H23, R4 H19; F7+. |
| **PE-007** | Mercados de reglas ambiguas exigen prima de disputa/oráculo. | Taxonomía manual rules/source; matched controls, spread y time-to-redemption; NO_GO por muestra escasa o efecto nulo. | R1 H6, R3 H21/H22, R4 H10/H11; F7+. |
| **PE-008** | Clarificación/actualización reglamentaria provoca price jump diferente de noticia normal. | Event study de clarification vs controles, timestamps y nuevos payoff states, separar efecto de disputa. | R1 H6/H10, R3 H22; F7+. |
| **PE-009** | Fuente exacta de resolución frente al headline general crea mispricing observable. | Parsear fuente/estación/tabla/first release; hand-validate; alinear feed a CLOB, evaluar EV y delay sin información futura. | R1 H5/H6/H7, R3 H21; F7+. |
| **PE-010** | Wallets con skill histórica generan flow predictivo incremental. | Skill sólo con mercados pasados; deciles OOS, matched markout/returns y sybil controls. NO copy trading ni inferir órdenes no observadas. | R1 H3, R3 H24; F7+. |
| **PE-011** | Maker captura spread+rebates sólo donde markout posterior no destruye margen. | Shadow quotes con fill models/queue bounds, markout 1s/5s/30s/5m y PnL inventory-adjusted; no contar resting order como fill. | R1 H9, R2 H1/H4, R3 H17; F7+. |
| **PE-012** | Nichos fee-free geopolitics permiten maker spread de baja competencia. | Screen spreads y reward configuration; simular fills y shocks, inventory worst-case. No asumir fill rate 15–40/día de R2. | R2 H1, R1 H9; F7+. |
| **PE-013** | Filtro de volatilidad externa reduce toxic fills maker en BTC 15m. | Sin órdenes: sincronizar spot/PM, quote survival, hypothetical cancellation y adverse fill rate; OOS y coste de infraestructura. Evidencia negativa R1 H5. | R2 H4, R1 H5/H9; F7+ **alta barrera de latencia**. |
| **PE-014** | Favorite–longshot sesgado por categoría y bucket, no regla global. | Reproducir P(Y=1), returns netos, Brier por bucket×categoría; Sports distinto de Crypto/Politics; bootstrap parent event. | R1 H2, R3 H1/H3, R4 H1/H2; F7+. |
| **PE-015** | Signo del longshot cambia por weighting y estructura del parent event. | Mismos trades bajo notional-, child- y parent-equal; descomponer market count y capital; si cambia de signo no promocionar regla pooled. | R3 H2, R4 H4; **instrumental**. |
| **PE-016** | Compresión hacia 50%/FLB cambia con horizonte TTR. | Logistic calibration y retornos por `<1h`, `1d`, `1–7d`, `1–4w`, `>4w`, OOS; controlar categoría y censura. | R1 H2, R3 H4, R4 H5/H6; F7+. |
| **PE-017** | En mercados políticos hay underconfidence condicional, pero no necesariamente retorno neto. | Regression slope e intervalos por subcategoría/evento y horizonte; ejecución ask/bid real; prevenir Simpson. | R1 H2, R3 H5, R4 H3/H14; F7+. |
| **PE-018** | Thresholds crypto tienen wedge frente a opciones externas replicables. | Exact strike, expiry, observation time y source; distinguir probability risk-neutral vs física; net hedge feasibility. | R3 H6, R4 H16; F7+ investigación. |
| **PE-019** | Cambio del precio mostrado al cruzar spread=10¢ genera falso momentum/reversión. | Registrar display, bid/ask, last trade y medir discontinuidad; usar como data-quality gate, NO como señal económica sin validación. | R3 H14; **instrumental**. |
| **PE-020** | Bid–ask bounce explica parte de la reversión en last-trade returns. | Comparar autocorrelación midpoint vs last price en timestamps alineados, spread y tick; rechazar si no hay roundtrip neto. | R3 H15, R1 H4; **instrumental**. |
| **PE-021** | Spreads relativos son mayores en longshots que en precios centrales. | Histórico L2; spreads absolutos/relativos por bucket, categoría/tick/volume; identificar si subsidy maker compensa adverse selection. | R3 H11, R4 H17; F7+. |
| **PE-022** | Book depth decae cerca del evento/resolución y cambia oportunidad/capacity. | Panel L1/L5/L10 within-market por TTR; controlar volume y news; cuantificar si opportunity theoretical pasa a not-capturable. | R3 H12, R4 H6; **instrumental/MVP data**. |
| **PE-023** | Spread/depth predicen error de calibración futuro. | Spread rezagado vs Brier/abs error OOS, precio/categoría/TTR controles; distinguir incertidumbre como confusor. | R3 H13; F7+. |
| **PE-024** | Liquidity Rewards crean cambio discontinuo alrededor de 10¢/90¢. | Verificar reglas vigentes; within-market crossing, regression discontinuity depth/quotes; no confundir news con threshold. | R3 H16, R4 H13; F7+. |
| **PE-025** | Maker rebate curve p(1-p) concentra depth cerca de 50%. | Fees efectivos, depth/spread por bucket y controles fee-free, medir si efecto persiste tras volatilidad. | R3 H17, R1 H9; F7+. |
| **PE-026** | Taker rebates generan más volumen low-price incentivado desde fecha de lanzamiento. | Validar fecha/fórmula histórica; DiD category weight×price×post; placebo y cambios simultáneos; no confundir volumen con PnL. | R3 H7/H9; **investigación causal**. |
| **PE-027** | Taker rebate amplify FLB/overpricing y volumen sin información. | DiD/triple-diff sobre returns, Brier y liquidity tras incentivo, outcomes resueltos; segmentar por evento y TTR. | R3 H8/H9, R4 H18; F7+. |
| **PE-028** | Horario intradía afecta spreads, depth, price discovery. | Hour-of-week por categoría con clocks normalizados; separar ventanas de noticias; medir retorno neto y reproducibilidad temporal. | R3 H18, R4 H15; F7+. |
| **PE-029** | Prices se acumulan en números redondos más allá del tick size obligatorio. | Histograma de trades/quotes en 5/10¢ con placebo, normalizar tick grid y market selection; sólo estrategia si genera predictable executable bounce. | R3 H20; F7+. |
| **PE-030** | Pronósticos meteorológicos + estación exacta + observación live dan fair-value por bucket superior al mercado. | Fuente contractual exacta, ensemble/bias historical, P(bucket), walk-forward Brier/log-loss y EV neto por VWAP, fees, settlement. Primero estadística interpretable, luego ML sólo si añade OOS. | R1 H5/H6, R4 H12; F7+. |

**Ideas complementarias que no se deben inventar como hypotheses independientes sólo para llegar a un número:** macro nowcasting con probabilistic portfolios (requiere benchmark externo y calibración OOS; ya está en [[Polymarket Arbitrage — Opportunity Context]]), in-play reverse-FLB (subgrupo de PE-014, **disputado**), smart-money/leaderboard copy (PE-010 sólo flow study), wash-trading/duplicated volume (calidad de dataset), settlement manipulation (investigación de riesgo/sensibilidad, NO estrategia de manipulación), capital lock/holding rewards (input económico, no edge per se).

## 6. Mapa de dependencias y secuencia de falsación barata

| Paquete | Datos mínimos | Hipótesis habilitadas | Gate |
|---|---|---|---|
| **A — Historia/resolved events** | Gamma, results, parent-event, historic trades/price, category, TTR, timestamps | PE-014–017, PE-026–027, PE-029 | Test OOS con net returns donde exista book; por ahora *statistical anomaly only* cuando no exista book. |
| **B — CLOB recorder ya previsto por F1** | Snapshot/WS/recovery, exact fee info, depth, latency, event changes | PE-001–005, PE-011–013, PE-019–025, PE-028 | Datos íntegros, book reproducible, precios ejecutables; NO_GO ante staleness o gap no reconciliado. |
| **C — Source/settlement joins** | Rules, source primario, oracle/dispute/clarifications, exact timestamps | PE-006–009 y PE-030; PE-003 con lifecycle | Matching manual spot checks y no-lookahead. |
| **D — Wallet/bulk advanced** | Trades/positions wallet históricos; cohortes, outcomes y market controls | PE-010 | Separar price discovery predictivo vs copyability; no usar fills futuros para skill. |

No abrir F7+ hasta después del MVP; se permite archivar research e identificar datos baratos reutilizables en F1 sin meter features en la arquitectura por anticipado. El monolito modular/una máquina grande siguen frozen; no hay justificación para Flink/Kafka/microservicios aquí.

## 7. Contrato común para cada hipótesis nueva

```text
id / parent_id / revision / title
mecanismo causal / por qué podría persistir
universo y exclusions / resolution rule/source
antecedentes: evidencia pro/contra y qué es claim vs verificado
frequency potencial, capacity, capital lock, latency, competition
inputs y provenance / observables faltantes
experimento read-only más barato / baseline y negative controls
estimando primario + unidad estadística (trade/market/parent event)
train/test split temporal, out-of-sample y multiple-testing correction
cost model: VWAP, fees by market, queue/fill, slippage, capital lock, oracle risk
GO / ITERATE / NO_GO ex ante + sample/CI caveats
estado: NEW → RESEARCH → SCREEN → REPLAY → SHADOW → TINY_LIVE
         → PROMOTED | ITERATING | REJECTED | INCONCLUSIVE
```

No confundir `INCONCLUSIVE` (sin datos suficientes) con `NO_GO`. Una iteración conserva parent e hipótesis original, registra por qué cambió y no reutiliza el mismo holdout para tuneo ilimitado. No usar ROI/PNL ilustrativos como forecast. Research Priority mide **coste de falsación y dependencia de datos**, Economic Viability exige capital desplegable, fill capture realista, drawdown y PnL neto.

## 8. Límites, contradicciones y correcciones visibles

1. **Fees Sports contradictorias:** R1/R3 reportan `feeRate=0,05` y 15% maker rebate; R2/R4 mencionan `0,03`/25%. La página oficial revisada el 16-09-2026 muestra Sports `0,03`, maker 0, 25% rebate; Crypto `0,07`, Weather `0,05`; fees se determinan **por mercado al match** y `getClobMarketInfo(conditionID)` entrega params. Fuentes oficiales: https://docs.polymarket.com/trading/fees y https://docs.polymarket.com/v2-migration. No hardcodear ningún número de los informes; guardar snapshots históricos del fee regime para backtests.
2. **Incentivos vigentes vs históricos:** R3 atribuye fecha 28-05-2026 al Taker Rebate Program y pesos de categorías. Pendiente contrastar changelog/reglas históricas para experimento causal; no asumir estabilidad de weights/rewards.
3. **FLB Sports contradictoria:** R1/R3 describen débil/ausente FLB en Sports según un estudio; R4 afirma reverse FLB con retorno positivo en Sports. Son especificaciones/poblaciones quizá distintas; NO declarar reverse-FLB hecho hasta reproducir categoría, periodo, TTR, maker/taker y weighting.
4. **Arbitraje 'risk-free':** R4 califica comprar una cesta NegRisk subprice como libre de riesgo. Es sólo payoff matemático bajo exhaustividad/reglas correctas y ejecución completa; legging, fees, semantic changes, oracle, settlement y contratos ambiguos lo invalidan operacionalmente.
5. **Volúmenes/beneficios de wallets y repos:** R2/R4 entregan percentiles muy precisos, ROI y claims de fallas open-source sin una auditoría wallet/source trazable aquí. Son pistas, no evidencia certificada. No usar esos porcentajes para economics, sizing ni priorización hasta reproducir.
6. **Oracle bonds/timing:** R1 y R2/R4 describen garantías distintas (~US$750 vs US$500) y delays. Variables del protocolo sujetas a cambios; comprobar contrato/documentación por evento antes de cualquier strategy post-event. No extrapolar 2 horas a todos los casos.
7. **Crypto lead-lag:** dataset OpenMarket relatado por R1 obtuvo resultado negativo OOS pese a lead observable. R2 atribuye alta frecuencia y estimaciones de fills/beneficios a un maker BTC 15m sin esa misma validación. Tratamiento: investigación no prioritaria; nunca tomar la rapidez observada como EV.
8. **Proxies/geoblock:** R2 sugiere routing por proxy en jurisdicciones permitidas. No adoptar como plan para evadir restricciones. La documentación oficial exige comprobar elegibilidad con `https://polymarket.com/api/geoblock`; órdenes de ubicaciones bloqueadas se rechazan. Chile no aparece en la lista consultada, pero ello NO sustituye el check desde el host real ni asesoría regulatoria local. Fuente: https://docs.polymarket.com/api-reference/geoblock.
9. **Datos faltantes:** no hay quote lifecycle histórico por wallet en la fuente pública descrita, ni L2 retrospectivo first-party completo según R1/R3. No reconstruir queue o intención a partir de fills. Label `UNKNOWN` cuando no observable.
10. **Causalidad y leakage:** R3 recomienda segmentar por parent event, right censoring, múltiples tests con FDR, no mirar resultados futuros para construir señales, separar UI midpoint/last trade y no inferir taker side ingenuamente. R4 atribuye algunas correlaciones a causas más específicas de las que su evidencia permite; conservar sólo como hipótesis.
11. **Regulatorio/seguridad:** verificar condiciones de uso, elegibilidad, edad/identidad y tratamiento jurídico/fiscal antes de F5/F6; investigación read-only no equivale a autorización para poner órdenes. Nunca almacenar private keys en el research corpus.

`last_verified` queda vacío para el conjunto del documento: sólo se verificaron directamente las páginas oficiales de fees, CLOB V2 y geoblock listadas; los artículos, datasets y claims individuales de cuatro Deep Research NO han sido auditados exhaustivamente. `confidence: medium` refiere únicamente a la calidad de esta síntesis y su provenance, NO al retorno esperado.

## 9. Referencias externas a contrastar en las siguientes etapas

- Documentación oficial: https://docs.polymarket.com/ ; fees https://docs.polymarket.com/trading/fees ; geographic restrictions https://docs.polymarket.com/api-reference/geoblock ; CLOB V2 https://docs.polymarket.com/v2-migration .
- Papers mencionados por las investigaciones y/o proyecto: https://arxiv.org/abs/2605.00864 (NBA arb), https://arxiv.org/abs/2608.00666 (NegRisk arb), https://arxiv.org/abs/2609.12878 (favorite/longshot), https://arxiv.org/abs/2508.03474 (cross-market). Revisar version/date/paper directamente antes de trasladar resultados a una SPEC.
- Dataset OpenMarket BTC/Binance y estudios microstructura/wallet skill citados en R1/R3: recuperar URL concreta y metodología original de esos informes antes de tratar resultados como replicados; las citas internas tipo `turnXXview` dentro de los cuatro documentos fueron generadas en otras sesiones y no son identificadores web permanentes.
- Fichas de provenance originales: [[Polymarket DR R1 — Mecanismos y evidencia]], [[Polymarket DR R2 — Microestructura y oráculo]], [[Polymarket DR R3 — Anomalías estadísticas y 24 hipótesis]], [[Polymarket DR R4 — Taxonomía y 20 hipótesis]].

## 10. Siguiente ingest / mantenimiento

Cuando haya datos físicos de F1 o papers/datasets originales: añadir resultados al ID PE correspondiente; promover las hipótesis validadas a un registro operativo del proyecto con versioning; registrar en log de dominio y conservar `GO/NO_GO/INCONCLUSIVE` con muestra, periodo, fecha de rules y fee regime. No borrar contradicciones sin reproducir el método que las generó.