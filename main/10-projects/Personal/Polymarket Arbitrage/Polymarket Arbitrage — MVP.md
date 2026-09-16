---
type: project
schema_version: 1
owner: me
root: true
status: active
priority: P1
area: "[[Personal]]"
parent:
sprint:
start: 2026-09-15
due:
progress: 0
repo:
jira:
prs:
aliases:
  - Polymarket Arbitrage MVP
  - Prediction Arbitrage MVP
tags:
  - kind/project
  - area/personal
  - domain/trading
  - tech/polymarket
  - topic/arbitrage
created: 2026-09-15
updated: 2026-09-16
---

# Polymarket Arbitrage — MVP

> [!info]+ Polymarket Arbitrage — MVP
> **Área:** [[Personal]] · **Estado:** active · **Prioridad:** P1 · **Bankroll tiny-live:** US$300

## 🎯 Objetivo

Construir y validar un motor autónomo de arbitraje en Polymarket que explore **dos estrategias en paralelo** sobre una base común:

1. **Sports Combinatorial Arbitrage**.
2. **NegRisk Arbitrage**.

El proyecto debe avanzar desde **screeners read-only → shadow/simulación de entradas con books reales → tiny-live con US$300**, midiendo edge neto, capacidad ejecutable, capital velocity, latencia y fill realism antes de escalar.

El MVP es **standalone**. No depende de Echo y no modifica Echo. Si demuestra valor, la integración posterior con Echo se decide con evidencia.

Contexto completo, evidencia, oportunidades futuras y restricciones: [[Polymarket Arbitrage — Opportunity Context]].

## 📊 Estado actual

- Proyecto creado; implementación greenfield.
- Autoridad de contexto: [[Polymarket Arbitrage — Opportunity Context]].
- Dos estrategias MVP frozen: Sports Combinatorial + NegRisk.
- Orden de validación frozen: screener → recorder/replay → shadow → tiny-live.
- Bankroll live inicial frozen: US$300.
- Diversificación: operar tantas oportunidades independientes válidas como permita el bankroll/capacidad; no forzar capital deployment sin edge.
- Repo de implementación: pendiente de crear/seleccionar.
- SPEC funcional/técnica: pendientes antes de implementar código.
- Echo/Kafka/Flink quedan fuera del MVP.
- Existe una cola post-MVP de estrategias no-arbitrage para explorar sólo después de cerrar/estabilizar F6.
- Arquitectura frozen: **modular monolith first**; un motor central compartido y un módulo/servicio lógico por estrategia dentro del mismo deployable.
- Topología inicial frozen: **una sola máquina grande con holgura**, evitando ruido de red/distribución mientras se valida edge.
- El objetivo de plataforma posterior al MVP es reducir `TIME_TO_VALIDATED_HYPOTHESIS`: llevar nuevas hipótesis desde definición falsable hasta detector/replay/shadow con el mínimo trabajo específico.

## 🧱 Entrega de desarrollo

| Aplicación / repo | Branch | Base | SPEC funcional | SPEC técnica | Estado |
|---|---|---|---|---|---|
| Polymarket arbitrage app — repo por definir | por definir | greenfield | pendiente | pendiente | BLOCKED para implementación hasta materializar repo + SPECs |

## 🧩 Arquitectura MVP frozen

### Decisión principal — modular monolith first

La primera implementación será **un monolito modular, un solo deployable y preferentemente un solo proceso para el hot path**. Las estrategias tienen boundaries explícitos en código, pero **no son microservicios** ni requieren llamadas de red entre sí.

```text
                         POLYMARKET ENGINE
                    modular monolith / 1 host
                               │
        ┌──────────────────────┼──────────────────────┐
        │                      │                      │
        ▼                      ▼                      ▼
  market-data            shared engine          observability
  discovery              + hypothesis lab       + persistence
  books/WS                    │
  recorder/replay             │
                              ▼
                    strategy modules/services
                    ├── sports-combinatorial
                    ├── negrisk
                    ├── weather            [F7+]
                    ├── maker/rewards      [F7+]
                    ├── favorite-bias      [F7+]
                    └── future hypotheses  [F7+]
                              │
                              ▼
                    common feasibility/risk
                              │
                ┌─────────────┼─────────────┐
                ▼             ▼             ▼
             screener       shadow        live
```

**“Servicio por estrategia” significa inicialmente un componente lógico interno**, con contrato propio, tests y estado identificable. Sólo se extrae a otro proceso/host si aparece evidencia material de que lo exige performance, aislamiento de fallos, recursos especializados o operación independiente.

### Motor central compartido

Debe absorber todo lo que razonablemente comparten las hipótesis para que agregar una nueva estrategia sea barato:

- market/event discovery;
- adapters Gamma/CLOB/WS;
- local order books + snapshot/recovery/staleness;
- canonical Event/Market/Outcome/Token model;
- raw recorder + normalized recorder;
- deterministic replay;
- fee/rebate/reward inputs dinámicos;
- full-depth/VWAP calculations;
- sizing primitives;
- bankroll/exposure accounting;
- local risk + kill switch;
- execution lifecycle/reconciliation;
- timestamps y latency instrumentation;
- common opportunity/result schema;
- experiment metadata;
- shadow accounting;
- metrics/journal/datasets;
- hypothesis registry y comparison scorecards cuando llegue F7+.

### Strategy boundary

Cada estrategia debe implementar sólo lo que la hace distinta, por ejemplo:

```text
strategy
  ├── universe / eligibility
  ├── required external data (si aplica)
  ├── relationship / fair-value model
  ├── opportunity detector
  ├── strategy-specific feasibility
  └── strategy-specific metrics
```

Sports y NegRisk son los dos primeros módulos. Weather, Maker/Rewards, Favorite/Longshot, Macro y futuras hipótesis deben poder agregarse reutilizando el mismo recorder, replay, shadow, capital/risk y observabilidad siempre que el dominio lo permita.

### Modes reutilizables

Una estrategia debe poder avanzar sin reescribir el sistema:

```text
READ_ONLY / SCREEN
        ↓
REPLAY
        ↓
SHADOW
        ↓
TINY_LIVE
        ↓
LIVE
```

La promoción cambia el modo/configuración y los gates, no la arquitectura fundamental de la estrategia.

### Deployment inicial

**Una sola máquina grande con holgura** para el monolito y sus dependencias de runtime necesarias.

Objetivo: mientras se investiga edge, no introducir problemas secundarios de distribución, scheduling, cross-host latency, networking, service discovery o consistencia eventual.

Principios:

- preferir CPU/RAM/NVMe sobrantes antes que optimizar infraestructura demasiado pronto;
- mantener market-data, books, solver, shadow/live decision path y estado caliente local al mismo host;
- persistencia/analytics puede trabajar async fuera del hot path, aunque inicialmente viva en la misma máquina;
- no Kafka/Flink/microservices/k8s para resolver problemas que todavía no existen;
- instrumentar CPU, RAM, GC, disk I/O, queue depth y latency desde el inicio;
- dividir procesos/hosts sólo cuando profiling o aislamiento operacional lo justifiquen.

No se fija aún un tamaño exacto de máquina: se elegirá con holgura deliberada en F0/F1 y se medirá antes de optimizar coste.

### Boundary funcional

**Común:**
- market discovery;
- local order books;
- canonical event/market/outcome/token model;
- recorder/replay;
- fee engine;
- depth-aware sizing;
- bankroll allocator;
- local risk;
- execution lifecycle;
- metrics/journal.

**Strategy-specific MVP:**
- Sports payoff relationships/solver.
- NegRisk conversion relationships/solver.

**No meter en MVP:**
- Echo integration;
- Kafka/Flink;
- cross-venue;
- market making/rewards;
- ML/LLM decisioning;
- UI compleja;
- HFT/co-location;
- custom Polygon node;
- decenas de abstracciones venue-agnostic antes de necesitarlas;
- microservicios por estrategia.

## 🧪 Modelo de Hypothesis Lab

El diseño debe permitir acumular **20–30 hipótesis** y validarlas de forma incremental sin convertir cada experimento en un proyecto nuevo de infraestructura.

Cada hipótesis tendrá como mínimo:

```text
id
mechanism / causal thesis
universe
required data
signal / detector
capital lock
capacity hypothesis
latency sensitivity
competition hypothesis
supporting evidence
contrary evidence
minimum read-only experiment
GO condition
NO_GO condition
status
parent hypothesis / iteration
```

Estados objetivo:

```text
NEW
→ SCREENING
→ REPLAY
→ SHADOW
→ TINY_LIVE
→ PROMOTED

cualquier etapa
→ ITERATING
→ REJECTED
```

Las hipótesis que muestren señal pero fallen parcialmente pueden iterar (`HYP-x.y`) sin perder la trazabilidad del experimento original. Una hipótesis sólo se promueve cuando sobrevive costes y condiciones de ejecución; una idea atractiva sin evidencia no gana prioridad por narrativa.

North star de plataforma de research:

`TIME_TO_VALIDATED_HYPOTHESIS`

La plataforma debe hacer que, una vez construido el motor central, el coste marginal de agregar un nuevo detector/estrategia disminuya de forma material.

## 🪜 Fases hasta MVP

### F0 — Foundation / autoridad

**Objetivo:** dejar un carril implementable y verificable antes de tocar código.

**Entregables:**
- nombre y repo greenfield;
- branch/base definidos;
- SPEC funcional;
- SPEC técnica;
- modular monolith y single-host topology declarados en SPEC;
- contrato mínimo de strategy module/service;
- modos comunes `screen/replay/shadow/live`;
- modelo canónico mínimo de Event/Market/Outcome/Token/Book/Opportunity;
- fuentes oficiales frozen para Gamma/CLOB/fees/NegRisk;
- contracts de timestamps/decimal precision/staleness/error semantics;
- instrumentation mínima para CPU/RAM/I/O/latency;
- sizing inicial de máquina deliberadamente holgado, documentado como baseline y no como capacidad final.

**Gate F0:** implementación puede empezar sin decisiones materiales abiertas y sin necesitar diseño distribuido.

### F1 — Market discovery + live recorder

**Objetivo:** capturar el universo relevante y mantener books locales confiables.

**Scope:**
- descubrir eventos/markets Sports relevantes;
- descubrir eventos `negRisk=true`;
- resolver token IDs/outcomes;
- CLOB WebSocket + snapshots/recovery;
- timestamp exchange/local receive;
- persistencia suficiente para replay;
- detección de gaps/stale feeds/reconnects;
- medir resource headroom de la máquina y asegurar que la infraestructura no contamine las mediciones de estrategia.

**Gate F1:**
- books reproducibles y consistentes;
- no gaps inexplicados en ventanas de prueba;
- eventos Sports y NegRisk correctamente clasificados;
- recorder funcionando durante una ventana prolongada sin intervención manual;
- sin evidencia de resource starvation que invalide latency/data-quality measurements.

### F2A — Sports Combinatorial Screener

**Objetivo:** detectar portfolios Sports con payoff mínimo > coste ejecutable.

**Scope:**
- partir por **una liga/deporte** con suficiente actividad; ampliar sólo después del baseline;
- agrupar mercados del mismo evento;
- construir payoff matrix por estados finales relevantes;
- solver de portfolios combinatorios;
- fees + full-depth VWAP;
- `gross_edge`, `net_edge`, `max_executable_size`, `capital_required`, `first_seen`, `last_seen`, `lifetime`;
- registrar también falsos positivos eliminados por fees/depth.

**Gate F2A:** dataset de oportunidades Sports reproducible y explicado.

### F2B — NegRisk Screener

**Objetivo:** detectar conversiones NegRisk económicamente realizables sobre la misma infraestructura.

**Scope:**
- full-set/baseline;
- partial conversion paths compatibles con el Neg Risk Adapter;
- conversión `NO -> collateral/YES complementarios` según contrato oficial;
- fees + full-depth sizing;
- tratamiento explícito de Augmented NegRisk/placeholders/Other;
- misma taxonomía de opportunity que Sports.

**Gate F2B:** dataset de oportunidades NegRisk reproducible y explicado.

> F2A y F2B se desarrollan en paralelo después de F1; ninguna bloquea la evaluación de la otra.

### F3 — Replay + execution feasibility

**Objetivo:** dejar de contar “señales” y estimar qué porcentaje era realmente capturable.

**Scope:**
- replay event-driven;
- lifetime de cada oportunidad;
- quote/book age;
- profundidad y partial fills;
- estimación de legging risk para múltiples patas;
- tres modelos de fill: optimistic / base / stress;
- latencia parametrizable;
- simulación de pérdida de oportunidad por delays.

**Gate F3:** cada oportunidad puede reclasificarse como `capturable`, `ambiguous` o `not_capturable` bajo supuestos declarados.

### F4 — Shadow trader + bankroll US$300

**Objetivo:** simular exactamente las decisiones que tomaría live sin firmar ni enviar órdenes.

**Bankroll:** US$300 virtuales.

**Allocator:**
- ambas estrategias compiten por el mismo bankroll;
- sizing por capacidad ejecutable y capital libre;
- diversificar por eventos independientes cuando exista oferta suficiente;
- caps por evento/estrategia configurables;
- valores concretos de tiny-live derivados desde evidencia shadow;
- capital ocioso permitido.

**Lifecycle mínimo:**

```text
DETECTED
→ ELIGIBLE
→ SHADOW_RESERVED
→ SHADOW_LEGS
→ SHADOW_COMPLETE | SHADOW_PARTIAL | EXPIRED
→ SETTLEMENT/EXIT_SIMULATED
→ CLOSED
```

**Métricas:**
- opportunities/day por strategy;
- executable opportunities/day;
- deployable capital/day;
- capital turns/day;
- gross/net edge;
- PnL/day/week/month-equivalent sobre US$300;
- drawdown;
- concentration;
- fill-model sensitivity;
- latency sensitivity;
- strategy share of capital/PnL.

**Gate F4:** varios días/regímenes con suficiente muestra para decidir `GO`, `NO_GO` o `CONTINUE_RESEARCH` por estrategia.

### F5 — Live plumbing sin capital significativo

**Objetivo:** probar autenticación, órdenes, cancelación, reconciliación y latencia real antes de operar estrategia.

**Scope:**
- trading wallet aislada;
- credenciales/API vigentes;
- order state machine;
- cancel-all/kill switch independiente;
- CLOB user WS;
- reconciliación CLOB/wallet/chain cuando aplique;
- medición `market update -> decision -> send -> ACK` p50/p95/p99;
- no dependencia de Echo.

**Gate F5:**
- orders/cancels/reconciliation confiables;
- ningún estado ambiguo sin recovery;
- p95 suficientemente bajo para las oportunidades observadas; target inicial <=1 s, preferencia <=500 ms;
- kill switch probado.

### F6 — Tiny-live US$300

**Objetivo:** validar que live reproduce shadow dentro de tolerancia.

**Reglas:**
- bankroll máximo total: **US$300**;
- ambas estrategias habilitables de forma independiente según gates F4;
- diversificación prioritaria entre oportunidades/eventos independientes;
- no aumentar capital por pocos días verdes;
- hard caps y daily stop definidos desde distribución shadow/stress;
- si una estrategia queda `NO_GO`, permanece disabled y no bloquea a la otra.

**Evidencia requerida:**
- live vs shadow execution;
- fill ratios y partials;
- realized PnL net fees;
- capital turns;
- latency;
- settlement/reconciliation;
- drawdown y exposición máxima;
- oportunidades perdidas por capacidad/latencia.

**Gate F6 / MVP CLOSED:**
- Sports y NegRisk están implementados end-to-end dentro del mismo motor;
- cada uno tiene estado explícito `GO`, `NO_GO` o `CONTINUE_RESEARCH`;
- al menos las estrategias `GO` pueden operar tiny-live con US$300 bajo risk/kill-switch/reconciliation;
- métricas permiten decidir si escalar bankroll o integrar con Echo.

### F7+ — Opportunity Lab post-MVP (NO bloquea F0–F6)

**Objetivo:** usar la infraestructura ya validada para descubrir y falsar nuevas fuentes de edge, una por una, sin ensanchar el MVP actual.

La cola objetivo inicial será de **20–30 hipótesis**. Los Deep Research, papers, perfiles públicos, datasets, anomalías propias y nuevas capacidades del protocolo alimentan el registry; no se implementan automáticamente.

Orden inicial de exploración:

1. **Weather probabilistic / resolution-source edge** — construir distribución de probabilidad por bucket usando modelos meteorológicos, observación live, error histórico y la fuente exacta de resolución; primero paper/shadow, luego tiny-live si el EV neto se mantiene.
2. **Toxicity-aware maker + rewards/rebates** — cotizar sólo cuando `spread capture + rewards + rebates - adverse selection - inventory risk` sea positivo; medir markout 1s/5s/30s/5m después de cada fill.
3. **Favorite/Longshot Bias** — reproducir el sesgo por price bucket/categoría/horizonte y verificar si sobrevive fees, spread, selection bias y execution real; no asumir que Sports comparte el patrón.
4. **Macro nowcasting + probabilistic portfolios** — construir distribución para CPI, unemployment, Fed/otras releases y asignar capital sólo a outcomes cuyo fair probability supere precio ejecutable con margen suficiente.
5. **Resolution-source / information-latency edge general** — mercados donde una fuente oficial, estación, tabla o primera publicación determina el payout y puede modelarse/observarse mejor que el headline genérico.
6. **Cross-market logical arbitrage** — relaciones de implicación/exclusión/exhaustividad fuera de NegRisk.
7. **Cross-venue** — sólo si capital y complejidad operacional justifican prefondeo y legging multi-venue.

**Regla F7+:** cada idea entra como mini-ciclo `hypothesis → read-only detector → historical/replay → shadow → GO/NO_GO`. No implementar ejecución nueva antes de que el detector demuestre frecuencia, capacidad y edge neto.

**Regla de priorización:** favorecer hipótesis baratas de falsar, compatibles con el capital disponible y que reutilicen alta proporción del motor central. Una hipótesis con gran narrativa pero alto coste de datos/infra puede quedar detrás de otra menos sexy que pueda medirse mañana.

## 🎚️ Criterios económicos de decisión

No definir un ROI mínimo arbitrario antes de medir. La decisión usa:

`Opportunity Value = frequency × executable capacity × net edge × capture probability`

Y para el bankroll:

`Capital Productivity = net PnL / deployed capital × capital turns`

Preguntas obligatorias antes de escalar:

1. ¿Cuántos dólares/día se pueden desplegar realmente?
2. ¿Cuánto net edge sobrevive fees/depth/fills?
3. ¿Cuántas veces rota el capital?
4. ¿Cuánto desaparece al pasar optimistic → base → stress?
5. ¿La latencia actual elimina una proporción material de oportunidades?
6. ¿US$300 está capacity-limited por bankroll o por mercado?
7. ¿Sports y NegRisk aportan oportunidades suficientemente independientes para diversificar?

## ✅ Tareas

### F0 — Foundation
- [ ] Crear/seleccionar repo greenfield para la app #owner/me #type/dev #area/personal
- [ ] Definir nombre de aplicación definitivo #owner/me #type/dev #area/personal
- [ ] Materializar SPEC funcional F0–F6 #owner/me #type/dev #area/personal
- [ ] Materializar SPEC técnica MVP #owner/me #type/dev #area/personal
- [ ] Congelar modular-monolith + single-host topology en las SPECs #owner/me #type/dev #area/personal
- [ ] Definir contrato mínimo común de strategy module/service #owner/me #type/dev #area/personal
- [ ] Definir modes comunes screen/replay/shadow/live #owner/me #type/dev #area/personal
- [ ] Definir baseline de observabilidad de recursos + latency #owner/me #type/dev #area/personal
- [ ] Congelar fuentes oficiales/API/contracts vigentes #owner/me #type/research #area/personal

### F1 — Data plane
- [ ] Implementar discovery Sports + NegRisk #owner/me #type/dev #area/personal
- [ ] Implementar CLOB snapshots/WS/local books #owner/me #type/dev #area/personal
- [ ] Implementar recorder + replay source #owner/me #type/dev #area/personal
- [ ] Certificar gaps/staleness/timestamps #owner/me #type/dev #area/personal
- [ ] Certificar headroom de la máquina para que no contamine mediciones #owner/me #type/dev #area/personal

### F2 — Screeners paralelos
- [ ] Sports: modelar evento + payoff matrix #owner/me #type/dev #area/personal
- [ ] Sports: implementar combinatorial opportunity solver #owner/me #type/dev #area/personal
- [ ] NegRisk: modelar conversion paths #owner/me #type/dev #area/personal
- [ ] NegRisk: implementar opportunity solver #owner/me #type/dev #area/personal
- [ ] Compartido: depth-aware fee-aware sizing #owner/me #type/dev #area/personal

### F3/F4 — Medición + shadow
- [ ] Implementar replay execution feasibility #owner/me #type/dev #area/personal
- [ ] Implementar fill models optimistic/base/stress #owner/me #type/dev #area/personal
- [ ] Implementar shadow lifecycle #owner/me #type/dev #area/personal
- [ ] Implementar allocator bankroll US$300 #owner/me #type/dev #area/personal
- [ ] Ejecutar ventana de observación y producir scorecard Sports vs NegRisk #owner/me #type/research #area/personal

### F5/F6 — Tiny-live
- [ ] Implementar wallet/auth/order lifecycle/reconciliation #owner/me #type/dev #area/personal
- [ ] Implementar kill switch + hard limits #owner/me #type/dev #area/personal
- [ ] Medir latencia live y validar contra lifetime observado #owner/me #type/dev #area/personal
- [ ] Derivar caps live desde shadow/stress #owner/me #type/research #area/personal
- [ ] Activar tiny-live US$300 sólo en estrategias GO #owner/me #type/dev #area/personal
- [ ] Certificar MVP y decidir scale / Echo integration / close #owner/me #type/research #area/personal

### F7+ — Research backlog, ejecutar después del MVP
- [ ] Crear hypothesis registry durable y cargar 20–30 hipótesis priorizadas #owner/me #type/research #area/personal
- [ ] Weather probabilistic + resolution-source detector/shadow #owner/me #type/research #area/personal
- [ ] Toxicity-aware maker/rewards/rebates detector/shadow #owner/me #type/research #area/personal
- [ ] Favorite/longshot bias replication + net execution study #owner/me #type/research #area/personal
- [ ] Macro nowcasting + probabilistic portfolio research #owner/me #type/research #area/personal
- [ ] Resolution-source/information-latency opportunity taxonomy #owner/me #type/research #area/personal

## 📆 Bitácora

- **2026-09-15** — Proyecto creado desde investigación Polymarket. Se decide KISS: app standalone, dos solvers paralelos (Sports Combinatorial + NegRisk), screeners primero, shadow después, tiny-live US$300 al final. Echo queda explícitamente fuera hasta demostrar valor.
- **2026-09-16** — Se incorpora una cola post-MVP de discovery: Weather, toxicity-aware maker/rewards, Favorite/Longshot Bias, macro probabilistic portfolios y resolution-source/information-latency. No cambia scope ni gates F0–F6.
- **2026-09-16** — Se congela arquitectura `modular monolith first`: motor central reusable + strategy modules/services internos; un solo deployable/host grande al inicio. El objetivo posterior es mantener 20–30 hipótesis y minimizar `TIME_TO_VALIDATED_HYPOTHESIS`. Deep Research alimentará el registry, no el backlog de implementación directamente.

## 🧭 Decisiones

- `D-001` — La app será independiente de Echo durante MVP.
- `D-002` — Sports Combinatorial y NegRisk comparten data/books/sizing/risk, pero tienen solvers separados.
- `D-003` — Las dos estrategias se exploran en paralelo una vez disponible F1.
- `D-004` — No se usa capital real antes de screener + replay + shadow.
- `D-005` — Bankroll tiny-live inicial total = US$300.
- `D-006` — Diversificación es objetivo, no obligación de deployment: operar múltiples eventos cuando haya edge; dejar cash cuando no lo haya.
- `D-007` — Límites concretos por event/strategy se derivan de shadow; no se inventan ahora.
- `D-008` — MVP puede cerrar con una estrategia `NO_GO`; éxito del producto significa poder medir y operar correctamente las que demuestren edge, no obligar a ambas a ser rentables.
- `D-009` — La integración con Echo sólo se evalúa después de F6.
- `D-010` — Las estrategias no-arbitrage viven en F7+ y no expanden el MVP actual; se validan una por una con detector + shadow antes de cualquier ejecución.
- `D-011` — Arquitectura inicial = modular monolith; un deployable y hot path local. Los strategy services son boundaries de código, no microservicios.
- `D-012` — Deployment inicial = una máquina grande con headroom deliberado; primero eliminar ruido operacional, después optimizar coste/partición con profiling.
- `D-013` — No Kafka/Flink/k8s/service mesh para la primera implementación salvo evidencia material que obligue a introducirlos.
- `D-014` — North star de la plataforma de research post-MVP = `TIME_TO_VALIDATED_HYPOTHESIS`.
- `D-015` — La cola objetivo es 20–30 hipótesis; Deep Research y otras fuentes alimentan el registry, luego se priorizan y falsan una por una.

## 🔗 Docs / Links

- [[Polymarket Arbitrage — Opportunity Context]]
- Polymarket docs: https://docs.polymarket.com/
- Sports arb paper 2026: https://arxiv.org/abs/2605.00864
- NegRisk arb paper 2026: https://arxiv.org/abs/2608.00666
- Cross-market arb paper: https://arxiv.org/abs/2508.03474
- Favorite/Longshot Bias paper 2026: https://arxiv.org/abs/2609.12878

## 💡 Ideas

### Backlog de ideas

- Weather probabilistic trading + resolution-source edge.
- Toxicity-aware reward/rebate market making.
- Favorite/longshot bias harvesting.
- Macro nowcasting + probabilistic portfolios.
- Resolution-source / information-latency strategies.
- Cross-market logical arbitrage.
- Model-driven market making.
- Cross-venue arbitrage.
- Holding/reward incentives como mejora económica, no tesis standalone.
- Integrar con Echo como control plane sólo tras evidencia.

### Motivos / principios

- KISS/YAGNI: demostrar plata antes de arquitectura grande.
- Modular monolith before distributed system.
- Un motor central reusable; una estrategia nueva debe aportar mayormente lógica específica, no reconstruir infraestructura.
- Un solo motor, múltiples solvers/strategies sólo cuando cada una justifique existir.
- Net executable edge > señal teórica.
- Capital velocity importa especialmente con bankroll pequeño.
- El mercado puede ser el limitante antes que el bankroll.
- Medir p95/p99, no enamorarse de la mediana.
- El research debe intentar falsar ideas, no sólo encontrar ejemplos ganadores.
- Optimizar primero `TIME_TO_VALIDATED_HYPOTHESIS`; optimizar infraestructura después de medir.
