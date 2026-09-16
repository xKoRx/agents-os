---
type: doc
schema_version: 1
status: active
area: "[[Personal]]"
project: "[[Polymarket Arbitrage — MVP]]"
created: 2026-09-15
updated: 2026-09-15
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

Polymarket expone libros de órdenes CLOB y relaciones económicas entre contratos que pueden quedar temporalmente inconsistentes. El proyecto no busca predecir eventos; busca detectar portfolios cuyo coste ejecutable sea menor que su payoff mínimo o que una conversión protocolar realizable.

La ventaja buscada no es “tener un bot”. El edge, si existe, estará en una combinación de:

- descubrir relaciones correctas entre instrumentos;
- mantener books locales consistentes;
- calcular capacidad por profundidad real, no por top-of-book;
- incorporar fees y slippage;
- ejecutar suficientes patas antes de que desaparezca la oportunidad;
- reciclar capital con alta velocidad;
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

- Makers: fee 0.
- Takers pagan fee en categorías habilitadas según `fee = C × feeRate × p × (1-p)`.
- Sports: taker fee rate 0,05; maker fee 0; maker rebate 15% a fecha 2026-09-15.
- Fees se aplican al match; el detector debe usar parámetros reales del mercado, no constantes hardcodeadas como autoridad eterna.

**Consecuencia:** un desbalance bruto no es una oportunidad. Toda oportunidad debe registrarse al menos como `gross_edge`, `fees`, `depth/slippage`, `net_edge`, `executable_size`, `capital_required`, `lifetime` y `confidence`.

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

## Oportunidades posteriores — fuera del MVP

Estas quedan registradas para exploración futura, pero no deben contaminar el MVP:

### Reward-aware market making / Liquidity Rewards

Seleccionar mercados donde Polymarket remunera liquidez y competir por rewards/rebates + spread. Es trading direccional/inventory-bearing, no arbitraje puro. Puede ser atractivo, pero requiere gestión de inventario y adverse selection.

### Cross-market logical arbitrage

Relaciones lógicas entre mercados distintos: implicación temporal, exclusión, exhaustividad, thresholds, etc. Ejemplo conceptual: si `A antes de junio` implica `A antes de diciembre`, el precio de la condición más restrictiva no debería exceder al de la más amplia. Requiere instrument/relationship graph y validación semántica estricta.

Referencia histórica: *Unravelling the Probabilistic Forest: Arbitrage in Prediction Markets* — https://arxiv.org/abs/2508.03474

### Favorite / Longshot Bias harvesting

Edge estadístico, no arb. Investigar buckets de precio/categoría/time-to-resolution y si contratos favoritos muestran retorno positivo neto tras execution costs. No mezclar con el MVP hasta tener baseline.

### Model-driven market making

Fair value externo + CLOB + inventory skew + adverse-selection filter. Candidatos: weather, sports con odds externas y macro. Potencialmente mayor moat, pero requiere modelo probabilístico y dataset.

### Cross-venue arbitrage

Polymarket vs Kalshi/sportsbooks/otros venues. Requiere capital prefondeado, semantic matching contractual, legging state machine y más capital. Fuera del MVP.

### Holding rewards / incentivos auxiliares

Sólo como mejora económica de otra estrategia; no como estrategia standalone salvo que cambien sustancialmente los términos.

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

- Polymarket Negative Risk: https://docs.polymarket.com/concepts/negative-risk
- Polymarket Fees: https://docs.polymarket.com/trading/fees
- Polymarket Order Book API: https://docs.polymarket.com/api-reference/market-data/get-order-book
- NBA arbitrage 2026: https://arxiv.org/abs/2605.00864
- NegRisk arbitrage 2026: https://arxiv.org/abs/2608.00666
- Cross-market arbitrage 2025: https://arxiv.org/abs/2508.03474

## Decisiones frozen al crear el proyecto

- MVP standalone, no Echo.
- Dos estrategias paralelas: Sports Combinatorial + NegRisk.
- Screeners antes de ejecución.
- Shadow/measurement antes de tiny-live.
- Bankroll tiny-live inicial: US$300.
- Diversificación por oportunidad/evento como objetivo; caps concretos derivados de shadow.
- KISS: una base común de market-data/books/sizing/risk; solvers separados por estrategia.
