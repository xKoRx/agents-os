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
updated: 2026-09-15
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

## 🧱 Entrega de desarrollo

| Aplicación / repo | Branch | Base | SPEC funcional | SPEC técnica | Estado |
|---|---|---|---|---|---|
| Polymarket arbitrage app — repo por definir | por definir | greenfield | pendiente | pendiente | BLOCKED para implementación hasta materializar repo + SPECs |

## 🧩 Arquitectura MVP frozen

Mantener cuatro responsabilidades lógicas; pueden vivir en pocos procesos/binarios al principio:

```text
Polymarket APIs / WS
        ↓
market-data + canonical books
        ↓
strategy solvers
   ├── sports-combinatorial
   └── negrisk
        ↓
execution feasibility
(depth + fees + slippage + lifetime)
        ↓
shadow / allocator / local risk
        ↓
real execution (fase tiny-live)
```

### Boundary

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

**Strategy-specific:**
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
- decenas de abstracciones venue-agnostic antes de necesitarlas.

## 🪜 Fases hasta MVP

### F0 — Foundation / autoridad

**Objetivo:** dejar un carril implementable y verificable antes de tocar código.

**Entregables:**
- nombre y repo greenfield;
- branch/base definidos;
- SPEC funcional;
- SPEC técnica;
- modelo canónico mínimo de Event/Market/Outcome/Token/Book/Opportunity;
- fuentes oficiales frozen para Gamma/CLOB/fees/NegRisk;
- contracts de timestamps/decimal precision/staleness/error semantics.

**Gate F0:** implementación puede empezar sin decisiones materiales abiertas.

### F1 — Market discovery + live recorder

**Objetivo:** capturar el universo relevante y mantener books locales confiables.

**Scope:**
- descubrir eventos/markets Sports relevantes;
- descubrir eventos `negRisk=true`;
- resolver token IDs/outcomes;
- CLOB WebSocket + snapshots/recovery;
- timestamp exchange/local receive;
- persistencia suficiente para replay;
- detección de gaps/stale feeds/reconnects.

**Gate F1:**
- books reproducibles y consistentes;
- no gaps inexplicados en ventanas de prueba;
- eventos Sports y NegRisk correctamente clasificados;
- recorder funcionando durante una ventana prolongada sin intervención manual.

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
- [ ] Congelar fuentes oficiales/API/contracts vigentes #owner/me #type/research #area/personal

### F1 — Data plane
- [ ] Implementar discovery Sports + NegRisk #owner/me #type/dev #area/personal
- [ ] Implementar CLOB snapshots/WS/local books #owner/me #type/dev #area/personal
- [ ] Implementar recorder + replay source #owner/me #type/dev #area/personal
- [ ] Certificar gaps/staleness/timestamps #owner/me #type/dev #area/personal

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

## 📆 Bitácora

- **2026-09-15** — Proyecto creado desde investigación Polymarket. Se decide KISS: app standalone, dos solvers paralelos (Sports Combinatorial + NegRisk), screeners primero, shadow después, tiny-live US$300 al final. Echo queda explícitamente fuera hasta demostrar valor.

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

## 🔗 Docs / Links

- [[Polymarket Arbitrage — Opportunity Context]]
- Polymarket docs: https://docs.polymarket.com/
- Sports arb paper 2026: https://arxiv.org/abs/2605.00864
- NegRisk arb paper 2026: https://arxiv.org/abs/2608.00666
- Cross-market arb paper: https://arxiv.org/abs/2508.03474

## 💡 Ideas

### Backlog de ideas

- Reward-aware market making.
- Cross-market logical arbitrage.
- Favorite/longshot bias harvesting.
- Weather/model-driven market making.
- Cross-venue arbitrage.
- Integrar con Echo como control plane sólo tras evidencia.

### Motivos / principios

- KISS/YAGNI: demostrar plata antes de arquitectura grande.
- Un solo motor, múltiples solvers.
- Net executable edge > señal teórica.
- Capital velocity importa especialmente con bankroll pequeño.
- El mercado puede ser el limitante antes que el bankroll.
- Medir p95/p99, no enamorarse de la mediana.
