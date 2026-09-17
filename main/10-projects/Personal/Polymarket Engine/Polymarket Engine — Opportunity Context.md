---
type: doc
schema_version: 1
status: active
area: "[[Personal]]"
project: "[[Polymarket Engine — MVP]]"
created: 2026-09-15
updated: 2026-09-16
aliases:
  - Polymarket opportunities
  - Polymarket strategy opportunities
  - Polymarket Arbitrage — Opportunity Context
tags:
  - kind/doc
  - area/personal
  - domain/trading
  - tech/polymarket
  - topic/quant-research
---

# Polymarket Engine — Opportunity Context

## Propósito

Contexto económico y de research para [[Polymarket Engine — MVP]]. El proyecto busca construir una plataforma personal, autónoma y reusable para **descubrir, falsar, medir y eventualmente operar estrategias en Polymarket**.

La arquitectura durable es el Engine. Las estrategias son POCs promovibles o descartables.

Echo y Echo Forge continúan en paralelo; el engine no depende de ellos durante su MVP.

## Restricciones del owner

- proyecto personal, sin clientes ni SaaS como requisito;
- engine durable, estrategias experimentales;
- primera ventana tiny-live total: **US$300**;
- diversificar entre oportunidades independientes cuando exista edge y capacidad;
- capital ocioso es válido;
- ninguna strategy entra live antes de screen/replay/shadow;
- no forzar Echo, Kafka, Flink, MT5, microservicios o Kubernetes en el MVP;
- una máquina grande inicialmente para quitar ruido operacional;
- Go como lenguaje de implementación del engine;
- objetivo de plataforma: disminuir `TIME_TO_VALIDATED_HYPOTHESIS`.

## Tesis de producto

Polymarket ofrece varios tipos de fricción potencialmente medibles:

- relaciones matemáticas/contractuales entre mercados;
- errores de calibración por categoría/precio/horizonte;
- microestructura, spread, depth y adverse selection;
- incentivos/rebates/rewards;
- resolution-source y settlement;
- external-information lead/lag;
- heterogeneidad de comportamiento entre participantes.

El objetivo no es elegir una narrativa ganadora. Es construir la infraestructura que permita convertir cada idea en una hipótesis falsable y medirla de forma consistente.

## Primeras Strategy POCs

### POC-S01 — NegRisk

Explorar relaciones económicas de mercados multi-outcome y Negative Risk, incluyendo full baskets, conversion paths, Augmented NegRisk, placeholders y `Other`, siempre con coste ejecutable por profundidad, fees dinámicos, legging risk y capital lock.

La estrategia debe demostrar frecuencia, capacidad y edge neto; no asumir rentabilidad por la existencia del mecanismo.

### POC-S02 — Sports Combinatorial

Modelar mercados relacionados dentro de un mismo evento deportivo mediante estados/payoff vectors y buscar portfolios cuyo payoff mínimo supere el coste ejecutable real.

El foco no es el trivial YES+NO; es la relación entre múltiples mercados asociados al mismo evento.

El orden S01/S02 puede invertirse por calendario/evidencia. Ambos consumen el mismo Engine y ninguno redefine el core.

## Pipeline de una estrategia

```text
hypothesis
  ↓
cheap triage
  ↓
deep research específico si sobrevive
  ↓
POC module
  ↓
screen
  ↓
replay
  ↓
shadow
  ↓
GO | ITERATE | NO_GO
  ↓
tiny-live sólo si GO
```

## Economía de oportunidad

North star de discovery:

`Opportunity Value = frequency × executable capacity × net edge × capture probability`

North star operacional:

`Capital Productivity = net PnL / deployed capital × capital turns`

No medir una strategy sólo por win rate ni edge bruto.

Registrar como mínimo:

- gross edge;
- executable price/VWAP;
- fees/rebates/rewards aplicables;
- slippage/depth;
- executable size/capacity;
- lifetime;
- latency sensitivity;
- capital required/lock;
- fill uncertainty;
- realized/shadow net PnL;
- concentration/correlation;
- resolution risk cuando aplique.

## Bankroll inicial

Tiny-live inicial total: **US$300**, compartidos por strategies promovidas.

Allocator conceptual:

`size = min(executable_capacity, free_capital, event_cap, strategy_cap)`

Los caps concretos se derivan de shadow/stress. No se fija un tamaño arbitrario por trade antes de tener datos.

## Research backlog canónico

La síntesis actual vive en [[Polymarket — Edge Research Consolidado 2026-09-16]] y deduplica cuatro Deep Research en **30 familias PE-001…PE-030**.

Familias que ya parecen útiles como candidatos de exploración posterior, sin implicar prioridad final:

- Weather probabilistic + exact resolution source;
- toxicity-aware maker / rewards / rebates;
- Favorite–Longshot condicionado por category × price bucket × TTR;
- Macro nowcasting + probabilistic portfolios;
- post-event/pre-settlement discount;
- new-market/opening mispricing;
- order-flow shock mean reversion;
- wallet-skill / informed-flow studies;
- resolution ambiguity/dispute premium;
- placeholder/`Other` repricing en NegRisk;
- cross-market logical relations;
- cross-venue sólo cuando capital/complejidad lo justifiquen.

## Weather — contexto

No partir obligatoriamente con ML. Baseline preferente: modelo probabilístico interpretable que combine:

- forecasts/ensembles;
- estación exacta de resolución;
- observación live;
- bias histórico por estación/modelo/horizonte;
- dispersión de modelos;
- variables meteorológicas sólo cuando aporten OOS.

Comparar distribución propia por bucket contra precios ejecutables. Medir Brier/log loss/calibration además de PnL.

## Maker / rewards — contexto

Es trading activo, no arbitraje puro.

Economía conceptual:

`maker EV = spread captured + rewards + rebates - adverse selection - inventory risk - execution costs`

Métrica crucial: **markout post-fill** a múltiples horizontes. Un reward alto no demuestra una buena estrategia si atrae toxic flow.

## Probabilistic portfolios — contexto

Para mercados por buckets, la strategy puede expresar discrepancias en múltiples outcomes en vez de “apostar al ganador”.

Por share YES, aproximación básica:

`EV ≈ P_model(payout) - executable_price - costs`

El problema difícil es estimar `P_model` bien calibrada, no el allocator. Sizing sofisticado (p. ej. fractional Kelly) sólo después de demostrar calibración y robustez.

## Favorite / Longshot — contexto

Longshot = outcome de baja probabilidad/precio y payout alto; favorite = alta probabilidad/precio.

No asumir una regla global de comprar favoritos. La evidencia consolidada muestra sensibilidad fuerte a category, horizon, event weighting y régimen. Primero replicar y segmentar; recién después evaluar una strategy ejecutable.

## Resolution-source edge — contexto

Las reglas del mercado y su fuente exacta determinan el payout. Investigar mercados donde el dato contractual pueda observarse/modelarse con más precisión que el headline genérico.

Ejemplos:

- weather: estación/campo exacto;
- economics: release/tabla exacta, primera publicación vs revisión;
- sports: resultado oficial/source;
- estadísticas públicas estructuradas.

No confundir entender mejor la regla con explotar ambigüedades de forma irresponsable; modelar explícitamente dispute/settlement risk.

## Criterios de promoción

Una POC sólo avanza si hay evidencia suficiente de:

1. fenómeno repetible;
2. edge o utilidad económica fuera de muestra;
3. supervivencia a fees/depth/fills;
4. capacity compatible con el bankroll;
5. latencia alcanzable por nuestra infraestructura;
6. comportamiento estable entre regímenes razonables;
7. riesgo/settlement/reconciliation comprendidos.

Si falla, `ITERATE` o `NO_GO`. No mantener una strategy por costo hundido.

## Boundary con Echo

Durante Engine MVP y primeras POCs:

- aplicación independiente;
- no llamadas síncronas a Echo;
- no Kafka/Flink como requisito;
- no MT5;
- no cambios en Echo.

Integración futura sólo después de demostrar que alguna strategy merece producción y que compartir control plane/capital/risk aporta más que mantener separación.

## Recursos

- [[Polymarket — Edge Research Consolidado 2026-09-16]]
- [[polymarket/00-index]]
- Polymarket official docs: https://docs.polymarket.com/
- Polymarket docs machine index: https://docs.polymarket.com/llms.txt

## Decisiones frozen

- Engine = MVP durable.
- Strategies = POCs.
- Strategy-agnostic, Polymarket-specific.
- Go modular monolith, single large host inicialmente.
- NegRisk + Sports = primeros consumidores.
- Cheap triage antes de Deep Research grande para hipótesis futuras.
- Deep Research específico antes de implementación seria de cada strategy promovida.
- US$300 tiny-live total, no por strategy.
