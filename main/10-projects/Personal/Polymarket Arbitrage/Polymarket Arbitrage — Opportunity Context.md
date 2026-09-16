---
type: doc
schema_version: 1
status: active
area: "[[Personal]]"
project: "[[Polymarket Arbitrage — MVP]]"
created: 2026-09-15
updated: 2026-09-16
aliases:
  - Polymarket opportunities
  - Prediction market arbitrage opportunities
tags:
  - kind/doc
  - area/personal
  - domain/trading
  - tech/polymarket
  - topic/arbitrage
---

# Polymarket Arbitrage — Opportunity Context

## Propósito

Contexto canónico de oportunidad para el proyecto [[Polymarket Arbitrage — MVP]]. La meta es construir un proyecto personal, autónomo y operable con capital propio, sin clientes, sin SaaS y sin depender de Echo durante el MVP. Si el producto demuestra edge y ejecución útil, la integración con Echo se evalúa después; antes de eso, YAGNI.

Esta nota también mantiene la **cola de hipótesis post-MVP**. El objetivo no es enamorarse de una estrategia, sino acumular candidatos, construir detectores baratos y falsarlos progresivamente.

## Restricciones del owner

- Proyecto personal; cero clientes y cero dependencia de terceros como modelo de negocio.
- Debe poder avanzar en paralelo a Echo y Echo Forge sin bloquearlos.
- Primera implementación live con bankroll total de **US$300**.
- Objetivo operacional inicial: usar el capital en la mayor cantidad de oportunidades independientes que sea razonable para diversificar, sujeto a capacidad real, liquidez, exposición y ejecución.
- No forzar trades para “usar” el bankroll: capital ocioso es válido cuando no existe edge neto.
- El MVP debe validar con datos reales antes de arriesgar capital: **screeners → medición/shadow → tiny-live**.
- El hot path no depende de Echo, Kafka, Flink ni MT5 durante el MVP.
- Echo puede absorber o controlar esta capacidad después sólo si hay evidencia de valor.

## Tesis general

Polymarket expone libros de órdenes CLOB y relaciones económicas entre contratos que pueden quedar temporalmente inconsistentes. En el MVP, el proyecto no busca predecir eventos; busca detectar portfolios cuyo coste ejecutable sea menor que su payoff mínimo o que una conversión protocolar realizable.

Después del MVP, el mismo data/execution plane puede evaluar estrategias de **probabilidad, microestructura e información**, siempre bajo un ciclo de validación separado.

La ventaja buscada no es “tener un bot”. El edge, si existe, estará en una combinación de:

- descubrir relaciones correctas entre instrumentos;
- mantener books locales consistentes;
- calcular capacidad por profundidad real, no por top-of-book;
- incorporar fees y slippage;
- ejecutar suficientes patas antes de que desaparezca la oportunidad;
- reciclar capital con alta velocidad;
- modelar probabilidades mejor que el mercado cuando aplique;
- entender exactamente qué fuente/regla resuelve un contrato;
- medir adverse selection y comportamiento post-fill;
- rechazar oportunidades aparentes que no sean ejecutables.

## Estrategias MVP — exploración en paralelo

### S1 — Sports Combinatorial Arbitrage

**Idea:** modelar múltiples mercados relacionados con un mismo partido/evento deportivo y encontrar una combinación de contratos cuyo payoff mínimo sea superior al coste total ejecutable.

No limitarse al arbitraje simple de dos outcomes. La oportunidad objetivo está en relaciones combinatorias entre mercados asociados al mismo evento.

Evidencia pública relevante:

- Paper 2026: *Arbitrage Analysis in Polymarket NBA Markets* — https://arxiv.org/abs/2605.00864
- Reconstruyó más de 75 millones de snapshots en 173 partidos NBA.
- Encontró sólo 7 episodios ejecutables de arbitraje simple in-game, mediana 3,6 s: señal de que el caso trivial está altamente arbitrado.
- Encontró 290 episodios de arbitraje combinatorio, principalmente hacia el final de partidos live.
- Retorno mediano reportado: 101 bps (~1,01%).
- 76,9% de las oportunidades combinatorias estuvieron limitadas por profundidad, con tamaño ejecutable medio de sólo 14,8 shares: capacidad pequeña, pero compatible con bankroll retail.

**Interpretación para este proyecto:** Sports simple no es la tesis. La tesis es que un solver de payoff cubra más relaciones que un scanner trivial y que el capital inicial pequeño pueda operar oportunidades cuya capacidad es insuficiente para jugadores grandes.

**Capital velocity:** atractiva porque los eventos deportivos suelen resolver en horas, no meses; aun así, settlement y liberación real del capital deben medirse y no suponerse.

### S2 — NegRisk Arbitrage

**Idea:** en eventos multi-outcome donde sólo un outcome puede ganar, Polymarket habilita relaciones entre posiciones mediante Negative Risk. La documentación oficial establece que 1 `NO` de un outcome puede convertirse atómicamente en 1 `YES` de cada uno de los demás outcomes mediante el Neg Risk Adapter.

Documentación oficial:

- Negative Risk Markets — https://docs.polymarket.com/concepts/negative-risk
- El mecanismo aplica a eventos multi-outcome donde sólo uno puede ganar.
- La conversión `NO -> YES de todos los outcomes complementarios` es atómica.
- En Augmented NegRisk, placeholders no nombrados deben ignorarse hasta ser aclarados; `Other` tiene semántica mutable y requiere especial cuidado.

Evidencia pública relevante:

- Paper 2026: *Executable Arbitrage and Market Efficiency in Prediction Markets* — https://arxiv.org/abs/2608.00666
- Estima ~US$1,12M históricos de arbitrage mechanism-linked: ~US$1,086M converter-enabled y ~US$32k settlement-based.
- Las violaciones del lado soportado por el adapter (`NO -> YES`) son menos frecuentes y más cortas: el mecanismo ya es conocido y está competido.
- Esto baja la prioridad del NegRisk simple como estrategia principal, pero lo hace barato de explorar una vez construida la infraestructura de books, sizing y simulación para Sports.

**Interpretación para este proyecto:** NegRisk se implementa como screener/solver paralelo y compite por capital con Sports. No se asume que produzca PnL relevante; debe demostrarlo.

## Economía de ejecución vigente

Fuente oficial: https://docs.polymarket.com/trading/fees

A fecha 2026-09-16 la documentación oficial indica:

- Makers: fee 0.
- Takers pagan fee sólo en mercados/categorías habilitados según `fee = C × feeRate × p × (1-p)`.
- Sports: taker fee rate 0,03; maker rebate 25%.
- Weather/Economics/Other, entre otras categorías: taker fee rate 0,05; maker rebate 25%.
- Geopolitics: fee 0 según tabla vigente.
- Los parámetros son dinámicos por mercado; consultar `feesEnabled`/market info y no hardcodear estas tasas como autoridad eterna.

**Consecuencia:** un desbalance bruto no es una oportunidad. Toda oportunidad debe registrar al menos `gross_edge`, `fees`, `depth/slippage`, `net_edge`, `executable_size`, `capital_required`, `lifetime` y `confidence`.

## Latencia

La implementación no es HFT de microsegundos, pero sí es sensible a segundos.

Objetivo de ingeniería para el MVP live:

- decisión local (`book update -> opportunity -> sizing/risk`): idealmente pocos milisegundos;
- `market update -> orders sent`: objetivo sub-segundo;
- end-to-end a ACK: medir p50/p95/p99; target inicial p95 <= 1 s, preferencia <= 500 ms si la infraestructura lo permite;
- ninguna optimización geográfica o infraestructura europea antes de demostrar que la latencia observada destruye edge.

Los ~4–5 s observados hoy en ciertas rutas de Echo no se usan como hot path del MVP.

## Bankroll inicial y diversificación

Bankroll live inicial: **US$300**.

La intención del owner es operar en tantas oportunidades válidas como sea razonable para diversificar. El allocator del MVP debe, por tanto:

1. calcular tamaño máximo ejecutable por profundidad real;
2. respetar capital libre y exposure por evento;
3. evitar concentración innecesaria cuando existan oportunidades independientes simultáneas;
4. no inventar un tamaño fijo por trade;
5. derivar límites concretos de tiny-live desde la distribución observada en shadow, no desde porcentajes arbitrarios definidos antes de tener datos.

La función práctica será del tipo:

`size = min(executable_capacity, free_capital, configured_event_cap, configured_strategy_cap)`

Los caps iniciales de tiny-live se fijan como gate de salida de shadow mediante evidencia, no en esta nota.

## Métricas que deciden si hay proyecto

La métrica principal NO es cantidad de señales ni edge bruto.

Para cada estrategia se debe poder responder por día/semana:

- oportunidades detectadas;
- oportunidades net-positive después de fees;
- oportunidades realmente ejecutables por depth;
- lifetime de la oportunidad;
- capital ejecutable por oportunidad;
- capital ejecutable por día;
- capital turns/day;
- gross/net edge;
- PnL shadow para bankroll US$300;
- PnL bajo modelo optimista/base/stress de fills;
- porcentaje de oportunidades descartadas por staleness, fees, capacity o riesgo;
- overlap/correlación entre oportunidades y eventos;
- latencia p50/p95/p99.

North star de discovery:

`Opportunity Value = frequency × executable capacity × net edge × capture probability`

North star operacional:

`Net PnL per deployed dollar × capital turns`

## Qué significa “MVP funcionando”

El MVP no obliga a que ambas estrategias ganen dinero. Debe dejar ambas estrategias técnicamente evaluables bajo el mismo motor y con ejecución live gateada por evidencia.

MVP completo:

- market discovery Polymarket operativo;
- local books confiables;
- recorder/replay suficiente para reproducir oportunidades;
- Sports combinatorial screener funcionando;
- NegRisk screener funcionando;
- sizing depth-aware + fee-aware;
- shadow trader que simule intención de entrada y salida con timestamps y estados;
- medición de fill realism y oportunidad perdida;
- allocator común para bankroll US$300;
- ejecución real disponible para cada estrategia que supere sus gates;
- reconciliación de órdenes/posiciones/capital;
- kill switch;
- dashboard/metrics mínimos;
- evidencia que permita declarar por estrategia `GO`, `NO_GO` o `CONTINUE_RESEARCH`.

Si una estrategia no demuestra edge, debe quedar deshabilitada aunque su implementación exista. No forzar live para cumplir una demo.

# Opportunity Lab post-MVP

Estas hipótesis se exploran **después de F6**. No expanden el MVP actual.

## O1 — Weather probabilistic trading

**Tesis:** construir una distribución de probabilidad sobre buckets de temperatura/precipitación usando modelos meteorológicos, observación live y error histórico; comparar fair probability vs precio ejecutable.

Primera aproximación: modelo probabilístico/estadístico interpretable, no ML obligatorio. ML sólo entra si un baseline bien calibrado deja un error explotable que justifique complejidad.

Features candidatas:

- ECMWF/GFS/Open-Meteo multi-model;
- observación live de la estación exacta;
- máximos/mínimos ya observados durante el día;
- hora local;
- bias histórico por estación/modelo/horizonte;
- dispersión entre ensembles;
- nubosidad/radiación/viento/humedad cuando aporte señal.

**Ventaja complementaria:** resolution-source edge. La estación/campo/fuente exactos importan más que el pronóstico genérico para una ciudad.

Validación: backtest/calibration → paper/shadow → tiny-live. Medir Brier/log loss además de PnL.

## O2 — Toxicity-aware market making + rewards/rebates

**Tesis:** ganar por `spread capture + liquidity rewards + maker rebates`, pero sólo cuando esos ingresos superen adverse selection e inventory risk.

Es trading activo: publicar/cancelar/reprecificar órdenes maker, recibir fills y administrar inventario. No es arb puro.

Polymarket expone APIs de rewards con configuración, min size/max spread, market competitiveness, earnings y porcentaje del reward; existe filtro `no_competition`. También expone maker rebates por mercado/día.

Métrica central: **markout post-fill**.

Registrar al menos:

- markout 1s / 5s / 30s / 5m;
- spread captured;
- reward share;
- maker rebate;
- inventory PnL;
- adverse-selection loss;
- quote uptime/scoring eligibility;
- capital tied in inventory.

No seleccionar mercados por reward bruto; un reward alto puede coexistir con flujo tóxico.

## O3 — Favorite / Longshot Bias harvesting

**Definición:** longshot = outcome de muy baja probabilidad/precio con gran payout potencial; favorite = outcome de alta probabilidad/precio.

Paper 2026: *The Favorite-Longshot Bias in Prediction Markets: Evidence from Polymarket* — https://arxiv.org/abs/2609.12878

Sobre 588M trades / 2,48M cuentas reporta, agregadamente, pérdidas fuertes en compras <10¢ y retorno positivo pequeño en compras >=90¢. El resultado depende de cómo se agrupen contratos y el patrón no aparece igual en Sports.

**Tesis:** reproducir el fenómeno por categoría, bucket de precio, horizonte, liquidez y modo maker/taker; sólo después estudiar si existe una estrategia ejecutable.

No confundir con “comprar favoritos al final”. La hipótesis puede existir semanas/días antes si un contrato a 91¢ tiene fair probability materialmente superior.

## O4 — Macro nowcasting + probabilistic portfolios

**Tesis:** estimar una distribución completa para releases discretizadas en buckets (CPI, unemployment, Fed, etc.) y comprar/vender sólo los outcomes donde la fair probability difiere del precio ejecutable con margen suficiente.

Ejemplo conceptual:

- mercado: `P(0.2)=29%`, `P(0.3)=39%`;
- modelo: `P(0.2)=40%`, `P(0.3)=42%`;
- no significa “sé que será 0.2”; significa que ciertos buckets están infra/sobrevalorados.

Una cartera probabilística expresa varias diferencias simultáneamente, con sizing según edge, incertidumbre, liquidez y concentración.

Métrica base por share comprado YES:

`EV ≈ fair_probability × $1 - executable_price - costs`

Usar fractional Kelly o un allocator conservador sólo después de demostrar calibración. El verdadero cuello de botella es `P(real)` bien calibrada, no la fórmula de sizing.

## O5 — Resolution-source / information-latency edge

Polymarket define por mercado una **resolution source**, end date y edge cases. El título es orientativo; las reglas determinan el payout.

**Tesis:** detectar mercados donde el dato contractual exacto puede observarse/modelarse mejor o antes que el concepto genérico que mira la mayoría.

Ejemplos de superficie:

- weather: estación exacta/campo exacto;
- economics: tabla/release exacto, primera publicación vs revisiones;
- estadísticas oficiales estructuradas;
- resultados deportivos oficiales;
- fuentes públicas con actualización programática.

No es “apostar por una ambigüedad”; es modelar el dato que las reglas dicen que resolverá el contrato.

## O6 — Cross-market logical arbitrage

Relaciones lógicas entre mercados distintos: implicación temporal, exclusión, exhaustividad, thresholds, etc. Ejemplo conceptual: si `A antes de junio` implica `A antes de diciembre`, la condición más restrictiva no debería ser más probable/cara bajo precios consistentes.

Referencia histórica: *Unravelling the Probabilistic Forest: Arbitrage in Prediction Markets* — https://arxiv.org/abs/2508.03474

Problema principal con bankroll pequeño: capital puede quedar bloqueado demasiado tiempo. Priorizar time-to-resolution corto y retorno anualizado/capital velocity.

## O7 — Model-driven market making

Fair value externo + CLOB + inventory skew + adverse-selection filter. Candidatos: weather, sports con odds externas y macro. Potencialmente mayor moat, pero requiere modelo probabilístico y dataset. Puede converger con O1/O2 después de validarlas por separado.

## O8 — Cross-venue arbitrage

Polymarket vs Kalshi/sportsbooks/otros venues. Requiere capital prefondeado, semantic matching contractual, legging state machine y más capital. Fuera del MVP y baja prioridad inicial.

## O9 — Holding/reward incentives auxiliares

Usar rewards/rebates/holding incentives únicamente como mejora económica de otra estrategia; no tratarlos como tesis standalone salvo cambio material de términos.

# Fuentes sistemáticas para generar nuevas ideas

La investigación futura no debe preguntar sólo “¿qué bot gana en Polymarket?”. Debe buscar **mecanismos repetibles de edge**.

## A. Documentación/API oficial

Revisar periódicamente:

- fees y maker rebates;
- rewards y `market_competitiveness`;
- nuevos endpoints;
- nuevos tipos de mercados;
- sports metadata/market types;
- NegRisk/Augmented NegRisk;
- resolution/clarifications;
- WebSocket/data fields nuevos.

Cambios de mecanismo pueden crear oportunidades antes de que la comunidad los explote completamente.

## B. Market-wide data mining

Usar Gamma/CLOB/Data API para construir un mapa completo por:

- category/tag/series;
- volume/liquidity/open interest;
- spread/depth;
- fee/reward configuration;
- time-to-resolution;
- price bucket;
- volatility;
- maker/taker flow si puede inferirse;
- realized outcome.

Buscar anomalías repetibles, no mercados individuales “interesantes”.

## C. Trader/wallet archetype mining

Polymarket expone leaderboard por categoría/periodo, activity, positions y closed positions. Analizar wallets públicas como **arquetipos de comportamiento**, sin intentar identificar personas:

- especialistas Weather;
- makers/reward farmers;
- high-probability/favorite traders;
- event-driven traders;
- alta rotación vs hold-to-resolution;
- concentración por categoría.

Objetivo: inferir hipótesis comprobables (`entry price`, holding time, category, sizing, exit behavior), nunca copiar PnL ciegamente.

## D. Papers de microestructura/prediction markets

No limitarse a papers que contienen “Polymarket”. Buscar también Kalshi, betting exchanges y prediction-market microstructure:

- adverse selection;
- favorite-longshot bias;
- informed price impact;
- market making;
- calibration;
- order-flow toxicity;
- information incorporation;
- combinatorial markets.

Los mecanismos suelen transferirse aunque cambie el venue; luego se verifica localmente.

## E. Open-source bots — especialmente los que perdieron

Repos públicos son útiles para ideas de ingeniería y, sobre todo, para descubrir **por qué una estrategia teórica falla**.

Buscar:

- resultados live explícitos;
- drawdown;
- fill/slippage handling;
- calibration;
- threshold selection;
- sizing;
- stale data;
- repo abandonado con postmortem.

Un bot weather open-source reportó en 2026 111 trades, ~51,4% win rate y PnL neto de -US$62,51 pese a partir de una tesis razonable; este tipo de fracaso es más informativo para diseño que un screenshot de ganancias.

## F. Comunidades / Reddit / Discord / X

Usarlas como **radar de hipótesis**, no evidencia de rentabilidad.

Extraer:

- nichos repetidos;
- nuevos bots;
- wallets mencionadas;
- problemas de ejecución;
- cambios de reglas;
- categorías donde traders dicen ver ineficiencia.

Toda hipótesis comunitaria debe volver a datos públicos antes de entrar al backlog serio.

## G. Mercados adyacentes

Buscar mecanismos de otros dominios y traducirlos:

- sports betting exchanges: favorite/longshot, closing-line value, correlated props;
- options: market making, inventory skew, calibration/distribution trading;
- crypto/CLOB: markout, queue position, adverse selection;
- meteorology: ensemble calibration/nowcasting;
- macro: nowcasting/event studies;
- pari-mutuel/betting literature: behavioral biases.

# Cómo orientar próximos Deep Research

Los Deep Research anteriores fueron buenos para **viabilidad de bots, arquitectura y estrategias conocidas**, pero demasiado centrados en responder “qué se hace hoy” y “qué parece rentable”. Para generar un pipeline de ideas, cambiar el framing.

Prompt/research objective recomendado:

> Mapear todas las fuentes plausibles de edge automatizable en Polymarket para una cuenta propia con US$300–US$2.000, priorizando nichos donde el edge provenga de información, modelado, reglas, microestructura o incentivos y no exclusivamente de velocidad. No recomendar una estrategia por anecdotes. Para cada hipótesis: mecanismo causal, datos requeridos, capital lock, frecuencia, capacity, latencia, fees, riesgo, competencia, evidencia pública, evidencia contraria, experimento read-only mínimo y criterio cuantitativo de falsación. Buscar activamente resultados negativos y repos/bots que hayan perdido dinero. Separar claramente `observed`, `inferred`, `hypothesis` y `unknown`.

Un segundo research puede ser puramente empírico:

> Tomar todas las categorías/series disponibles en Polymarket y buscar patrones de mispricing/calibration/liquidity/rewards/price behavior que generen hipótesis nuevas, sin partir de una lista prefijada de estrategias.

La clave es **idea generation → falsification**, no “encuéntrame bots rentables”.

## Alternativas explícitamente no prioritarias

- BTC/crypto 5m latency scalping: terreno muy sensible a latencia, fees y toxic fills.
- HFT/co-location: sólo después de demostrar un edge que la latencia esté destruyendo.
- Copy-trading: PnL observado no necesariamente replicable; fill tardío y exposición oculta.
- LLM autónomo tomando decisiones/sizing: LLM puede ayudar a research/semantic parsing, no es el core del execution edge.
- Late-entry >90% como regla simple: high win-rate no equivale a EV positivo.

## Boundary con Echo

Durante el MVP:

- aplicación independiente;
- estrategia, sizing, risk y execution local;
- ninguna llamada síncrona a Echo en el hot path;
- no Kafka/Flink como dependencia necesaria;
- no cambios en Echo.

Integración futura posible si hay edge:

- Echo como control plane/global capital allocator/reporting;
- Polymarket engine conserva decisiones sensibles a latencia;
- o reutilización del execution backbone de Echo sólo si mediciones reales prueban latencia suficientemente baja y estable.

La integración es una decisión posterior, no una condición de éxito del MVP.

## Fuentes principales

- Polymarket docs: https://docs.polymarket.com/
- Polymarket Resolution: https://docs.polymarket.com/concepts/resolution
- Polymarket Fees: https://docs.polymarket.com/trading/fees
- Polymarket Rewards APIs: https://docs.polymarket.com/api-reference/rewards/get-user-earnings-and-markets-configuration
- Polymarket Market Data: https://docs.polymarket.com/market-data/overview
- Polymarket Order Book API: https://docs.polymarket.com/api-reference/market-data/get-order-book
- NBA arbitrage 2026: https://arxiv.org/abs/2605.00864
- NegRisk arbitrage 2026: https://arxiv.org/abs/2608.00666
- Cross-market arbitrage 2025: https://arxiv.org/abs/2508.03474
- Favorite/Longshot Bias 2026: https://arxiv.org/abs/2609.12878
- Adverse Selection in Prediction Markets / Kalshi 2026: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6615739

## Decisiones frozen al crear/expandir el proyecto

- MVP standalone, no Echo.
- Dos estrategias paralelas MVP: Sports Combinatorial + NegRisk.
- Screeners antes de ejecución.
- Shadow/measurement antes de tiny-live.
- Bankroll tiny-live inicial: US$300.
- Diversificación por oportunidad/evento como objetivo; caps concretos derivados de shadow.
- KISS: una base común de market-data/books/sizing/risk; solvers separados por estrategia.
- Weather, Maker/Rewards, Favorite/Longshot, Macro y Resolution-source son **post-MVP** y no deben retrasar F0–F6.
- Cada estrategia post-MVP debe entrar primero como hipótesis falsable + detector read-only + shadow.
