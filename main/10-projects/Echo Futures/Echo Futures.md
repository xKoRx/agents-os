---
type: project
schema_version: 1
owner: me
root: true
status: active
priority: P1
area: "[[Echo]]"
parent:
sprint: 2026-09-23--2026-09-30
start: 2026-09-23
due: 2026-09-30
progress: 36
repo:
jira:
prs:
aliases:
  - Futures Prop Automation
  - Echo Futures Trading
tags:
  - kind/project
  - area/echo
created: "2026-09-23"
updated: "2026-09-24"
---

# Echo Futures

%% Naming: Echo Futures es el link canónico del proyecto; aliases guarda variantes humanas; tags/slugs son solo automatización. %%

> [!info]+ Echo Futures
> **Área:** [[Echo]] · **Estado:** active · **Prioridad:** P1 · **Sprint:** 2026-09-23 → 2026-09-30
> _parent / sprint / repo / jira / prs son opcionales._

> [!abstract]- Ownership del proyecto (`owner`) — humano vs agente
> `owner: me` → **proyecto humano**: la iniciativa/esfuerzo que conduces tú.
> `owner: agent` → **proyecto de agente**: un curro delegado, con detalle pesado que escribe y sigue un agente. Casi siempre es subproyecto de uno humano y vive en la subcarpeta `agentes/` de su iniciativa.
> `root: true` solo en **iniciativas raíz** (sin `parent`). Todo subproyecto debe setear `parent`; si no, aparece como huérfano en [[Panel de Proyectos]].
>
> **Tarea puente:** cuando este proyecto es `owner: agent`, en su proyecto **padre** debe existir UNA sola tarea humana que lo representa (arrancar + seguimiento). Así tu cockpit ve una línea por curro delegado, no las tareas internas del agente. Ejemplo, en el padre:
> `- [ ] [[Echo Futures]] arrancar + seguimiento #owner/me #type/supervision #area/personal`

## 🎯 Objetivo

- Convertir la idea inicial de operar futuros fondeados con alta intensidad y alto volumen en un sistema cuantitativo, reproducible y escalable sobre Echo + NinjaTrader, comenzando por definir y validar la operativa, la gestión monetaria y la economía real de las prop firms antes de implementar automatización.
- North star inicial: maximizar **cash neto extraído por unidad de capital real arriesgado y tiempo**, no maximizar balance nominal, cantidad de cuentas ni tasa de aprobación aislada.
- Escala objetivo de largo plazo: operar decenas de cuentas en paralelo (orden de magnitud aspiracional: 40–80) sin que la estrategia, la gestión de riesgo o la reconciliación dependan de trabajo manual por cuenta.

## 📊 Estado actual

- **2026-09-23 — Proyecto creado.** La idea está en fase de discovery operativo; no existe todavía estrategia, gestión monetaria, prop firm, instrumento ni arquitectura de ejecución congelados.
- Hipótesis del owner: estrategias de **win rate alto**, timeframes muy bajos, entradas/salidas rápidas y señales simples que pueden incluir estocásticos u otros filtros; Gerard García, Tradesfera y Psicólogo del Trading son fuentes iniciales de investigación, no autoridades mecánicas todavía.
- Hipótesis de gestión: usar un perfil agresivo al inicio y estudiar el método de hardscalping/recovery atribuido a Gerard García: cuando una posición evoluciona en contra y se cumple un trigger aún por reconstruir, aumentar exposición buscando un rebote y recalcular el objetivo/salida sobre la posición agregada.
- Hipótesis económica: aceptar una tasa alta de cuentas quemadas si el ciclo completo challenge/evaluation → funded → retiro mantiene valor esperado neto positivo después de fees, activaciones, resets, comisiones, slippage y restricciones de payout.
- El sistema debe distinguir **pasar la evaluación**, **sobrevivir funded** y **retirar dinero**; optimizar una sola de esas etapas puede empeorar la economía total.
- El target de 40–80 cuentas es un objetivo de capacidad futura, **no scope del MVP**. El primer vertical slice será una estrategia, una prop/configuración, un instrumento, una Reference y una Execution.
- **Gate histórico RESEARCH_ONLY: SUPERSEDED 2026-09-25.** D4/D5 economics cerraron suficiente incertidumbre para autorizar M0 Algo Execution MVP. Real-money continúa bloqueado hasta un gate explícito posterior.

## 🧠 Hipótesis operativa inicial

La idea no se congela como “martingala” ni como “promediar pérdidas” hasta reconstruir evidencia suficiente. El proyecto tratará el hardscalping como una **secuencia de recuperación con aumento de exposición** y deberá identificar exactamente el mecanismo causal y sus límites.

La ventaja que se quiere validar combina cuatro piezas: una entrada base de alta probabilidad, permanencia corta en mercado, capacidad de aumentar exposición bajo condiciones concretas cuando el trade va adverso y un modelo económico de prop donde el downside real por intento está acotado por el coste del challenge/cuenta y sus reglas. La fuerza bruta viene del volumen y de la repetición; no reemplaza la necesidad de demostrar valor esperado positivo.

El riesgo principal es de cola: una técnica con win rate muy alto puede esconder pérdidas raras pero suficientemente grandes para destruir la cuenta. Por eso el KPI principal no será win rate sino **distribución completa de resultados y cash extraído después de cuentas fallidas**.

## 🗓️ Horizonte de entrega — máximo 7 días

**Outcome de horizonte:** terminar la semana con al menos una operativa mecanizable seleccionada, un backtest/replay reproducible con supuestos explícitos, simulación de challenge→funded→payout sobre reglas reales de al menos una prop candidata y un veredicto `GO | ITERATE | NO_GO` para congelar o no el MVP Echo Futures.

**No-goals de esta semana:** desarrollar integración Echo/NinjaTrader productiva, construir copier multi-account, soportar múltiples props, comprar una cohorte grande de cuentas o optimizar infraestructura. Si el research no demuestra una operativa suficientemente concreta, la semana termina en `NO_GO` o `ITERATE`, no en código por inercia.

| Día | Outcome observable | Gate |
|---|---|---|
| D1 | Entrevista Gerard + tres DR completados | Corpus delimitado y outputs comparables |
| D2 | Síntesis adversarial de los DR | Principios útiles separados de inferencias; research amplio cerrado |
| D3 | Tesis matemática + contrato abstracto del simulador | Invariantes, estados, políticas y métricas definidos |
| D3.1 | **Astra/GOD valida exclusivamente la matemática del simulador** | **PASS — MATH_GO**; claims auditados + acceptance tests analíticos + condiciones de optional stopping |
| D4 | Simulador estocástico v0 implementado y verificado | Null model reproduce benchmarks analíticos antes de aceptar escenarios con edge |
| D5 | Tier-1 Topstep + TPT rulesets y economics certificados; Tier-2 después | `evaluation purchase → first real withdrawal | burn` reproducible bajo reglas reales; pass/funded sólo estados intermedios diagnósticos |
| D6 | Monte Carlo + sensitivity surfaces + cohort correlation | Break-even regions y assumptions dominantes identificados |
| D7 | Decisión `GO | ITERATE | NO_GO` para piloto de calibración | Presupuesto, tamaño de cohorte, reglas de aborto y supuestos que el piloto debe medir |

### Estrategia de research — tres one-shots + síntesis

No se investigará “todo el contenido” de cada creador. Cada one-shot buscará **extraer operativas automatizables** y deberá responder el mismo contrato. Esto permite comparar ideas y evita que el agente entregue una biografía o un resumen de YouTube.

1. **Gerard García — híbrido privado+público.** Primero el owner entrega libremente lo aprendido del curso. Luego se realiza una entrevista dirigida para cerrar huecos. En paralelo, un deep research público busca confirmar, refutar o completar parámetros usando videos, ejemplos y material accesible. El curso del owner tiene más peso para describir la técnica enseñada; evidencia pública sirve para contraste, no para sobreescribirla por popularidad.
2. **Tradesfera — deep research público one-shot.** Buscar setups repetidos, indicadores/parámetros, timing, gestión, pérdidas y evidencia de ejecución. Ignorar contenido motivacional/general salvo que cambie una regla.
3. **Psicólogo del Trading — deep research público one-shot.** Mismo contrato y mismo criterio de evidencia.
4. **Síntesis adversarial.** Un cuarto análisis recibe solo los tres outputs estructurados, no vuelve a navegar todo el corpus. Separa componentes compatibles: edge de entrada, filtros, recovery, sizing y salida; no crea un “Frankenstein” mezclando reglas sin evidencia.

### Contrato común de salida de cada deep research

Cada investigación debe entregar:

- Lista de videos/fuentes realmente usadas con URL/título/fecha o identificador reproducible y timestamp cuando exista.
- Instrumentos, sesiones y timeframes observados.
- Indicadores con parámetros exactos si son demostrables.
- Setup de entrada LONG y SHORT expresado condicionalmente.
- Condiciones de NO TRADE.
- SL/TP inicial y cualquier modificación posterior.
- Gestión monetaria inicial.
- Si existe averaging/add/recovery: trigger exacto, tamaño, cantidad máxima, precio medio y salida después de cada escalón.
- Pérdida máxima de una secuencia y criterio de abandono.
- Evidencia de operaciones ganadoras y perdedoras.
- Diferenciar `EXPLICIT` (el creador lo dice), `OBSERVED` (se ve repetidamente), `INFERRED` (deducción) y `UNKNOWN`.
- Una o más estrategias candidatas en pseudoreglas deterministas, sin código.
- Lista de ambigüedades que impedirían automatizar.
- Qué necesitaría validarse con datos antes de confiar en el edge.
- Veredicto por estrategia: `MECHANIZABLE | PARTIAL | DISCARDED`, sin puntajes subjetivos.

### Entrevista Gerard — método

La entrevista no parte preguntando veinte detalles aislados. El owner primero hace un **brain dump libre** de lo que recuerda del curso: cómo detecta setup, cómo entra, qué mira cuando va a favor/en contra, cuándo agrega, cómo cambia tamaño/SL/TP, cuándo acepta la pérdida y qué ejemplos recuerda. Después el entrevistador recorre el contrato G0 y pregunta únicamente lo que siga ambiguo.

El objetivo de la entrevista es convertir conocimiento tácito del owner en reglas falsables. Si algo se recuerda como “cuando parece que rebota”, queda `UNKNOWN` hasta precisar qué observable produce esa decisión.

### Criterio de selección rápida

Una estrategia no gana por parecer sofisticada. Para entrar a D3 debe cumplir simultáneamente:

- suficientemente mecánica para simularla sin interpretación visual humana;
- frecuencia suficiente para obtener muestra útil rápido;
- datos disponibles con resolución compatible con sus entradas/adds/salidas;
- costes de trading tolerables para su holding time;
- riesgo de cola cuantificable;
- compatible en principio con al menos una prop plausible;
- posibilidad de probar separadamente **entry edge**, **recovery** y **money management**.


## 🧪 D2 — Síntesis adversarial de los tres Deep Research

**Estado:** `D2_PASS` para avanzar a mecanización. El research amplio se cierra aquí salvo que aparezca una fuente concreta que resuelva un UNKNOWN material.

### Calidad real de los informes

| Informe | Resultado operativo | Calidad de evidencia | Uso permitido |
|---|---|---|---|
| Gerard García | PARTIAL | **Débil públicamente / fuerte vía curso del owner** | Usar la entrevista/curso como autoridad primaria. El DR público sólo aporta ideas de parametrización; no usar HardScalping EA como prueba de que Gerard hace algo. |
| Tradesfera | PARTIAL | **Media para principios, baja para reglas** | Aceptar sólo lo explícito: mean reversion, TP corto, alto win rate/selectividad y economía de prop. VWAP/RSI/ATR/fade ORB son propuestas del investigador, no estrategia demostrada de Vicente. |
| Psicólogo del Trading | NO_GO | **Corpus técnico insuficiente** | No extraer estrategia. Cerrar investigación salvo que el owner aporte un video técnico concreto. |

### Hallazgos de auditoría

- **Gerard DR sobreafirma evidencia:** su única fuente pública técnica es un producto/EA de terceros llamado HardScalping. No demuestra metodología de Gerard. Sus secuencias “observadas” son en realidad ilustrativas. Se conservan como ejemplos de modelado, no evidencia.
- **Tradesfera DR inventa demasiado detalle:** pasar de “mean reversion + TP corto” a “VWAP + RSI(14) + ATR” no está sustentado. Esos candidatos pueden investigarse como estrategias nuestras, pero no etiquetarse como Tradesfera.
- **Psicólogo NO_GO no prueba que no existan estrategias:** prueba que el one-shot no accedió a corpus técnico suficiente. Por restricción de tiempo, no se rescata ahora.
- La mayor evidencia útil sigue siendo el **curso de Gerard revisado por el owner**, especialmente el motor monetario de recovery y la filosofía prop.
- Los influencers dejan de ser autoridades desde este punto. D3 busca **estrategias Echo Futures**, no réplicas de una persona.

### Candidatos que pasan a D3

#### C0 — Random-direction control

Control obligatorio para medir cuánto valor aporta realmente la señal.

- misma sesión/ventana que la estrategia bajo prueba;
- misma frecuencia aproximada;
- dirección aleatoria 50/50;
- mismo SL/TP y mismo motor de gestión;
- comparar distribución completa contra la señal técnica.

No pretende ser estrategia de producción.

#### S1 — NQ/MNQ Opening Range Breakout 30m

Fuente principal: curso Gerard recordado por el owner.

- construir rango con primeros 30m de la sesión objetivo;
- entrada inmediata al romper high/low, sin exigir cierre;
- señal debe ejecutarse con resolución intrabar;
- LONG y SHORT simétricos;
- primero probar entry-only;
- después aplicar negative hardscalping.

**Por qué pasa:** extremadamente mecánica, barata de implementar, no requiere interpretación gráfica y sirve como señal momentum/breakout opuesta a S2.

#### S2 — H4 trend + 5m Bollinger pullback

Fuente principal: curso Gerard; conceptualmente consistente con la familia mean-reversion explicitada por Tradesfera, pero **no se atribuye a Tradesfera**.

Ejemplo LONG:

- régimen H4 alcista definido mecánicamente en D3;
- en 5m el precio alcanza/atraviesa banda inferior;
- entrada de pullback;
- salida base hacia una referencia Bollinger predefinida;
- SHORT simétrico.

**Por qué pasa:** representa un setup de alta probabilidad potencial, opera pullbacks/reversión sin pelear contra la tendencia mayor y es objetivizable con pocos parámetros.

### Candidatos que NO pasan esta semana

- Relevant high/low continuation/reversal: “relevante” sigue ambiguo.
- Momentum Londres/NY genérico: falta trigger exacto; ORB ya cubre un experimento direccional mecánico.
- VWAP+RSI atribuido a Tradesfera: no tiene evidencia suficiente.
- Fade de ORB atribuido a Tradesfera: inferencia del investigador.
- Psicólogo: cero candidato con evidencia.
- Positive hardscalping como estrategia completa: se conserva como módulo posterior, no como primera variable a introducir.

### Orden experimental para evitar explosión combinatoria

No hacer un full-factorial gigante desde el comienzo.

**Fase A — Entry edge**
- C0, S1, S2.
- gestión simple fija.
- medir frecuencia, win rate, payoff, MAE/MFE, duración y costes.

**Fase B — Negative hardscalping**
- aplicar exactamente el mismo motor a C0/S1/S2;
- mantener riesgo monetario máximo de la secuencia;
- variar sólo pocos parámetros de add/spacing/size;
- medir delta contra Fase A.

**Fase C — Positive hardscalping**
- sólo si Fase B deja uno o más candidatos vivos;
- agregar en favorable + protección BE + extensión;
- medir incrementalmente.

**Fase D — Variable risk + prop economics**
- operar sobre la distribución de trades/secuencias ya obtenida;
- simular progression/reset y lifecycle de evaluation/funded/payout;
- no mezclar variable risk dentro del backtest de señal antes de conocer el retorno base.

### Gate para D3

D3 debe terminar con una SPEC experimental, no con código productivo. Debe congelar:

- definición exacta H4 trend;
- Bollinger period/deviation/source;
- definición exacta ORB y timezone/session;
- política de re-entry y máximo de trades por sesión;
- money SL/TP base;
- negative recovery: trigger, size, max adds, recalculation exacta;
- resolución mínima de datos;
- instrumento/contrato y roll handling;
- costes/slippage;
- backtest runner y dataset;
- output schema para que D5 pueda simular prop rules.

Una vez todo eso sea determinista, **G0 puede pasar** aunque no coincida exactamente con el “ojo” de Gerard: la finalidad es validar la idea, no clonar su discrecionalidad.


## 🧩 D3 — Modelo abstracto de la tesis y estrategia de backtest

### Principios que sobreviven a cualquier estrategia concreta

La tesis de Echo Futures se descompone en componentes reemplazables. Ningún creador es parte del diseño; sólo aportó principios/hipótesis.

#### P1 — Prop asymmetry

El capital económico realmente arriesgado no es el nominal de la cuenta, sino:

`evaluation fees + activation + resets + data/platform + commissions + opportunity cost`.

El upside es el cash efectivamente retirado.

Objetivo:

`max E[cash_withdrawn - real_costs]`

por intento y por cohorte de cuentas.

#### P2 — Signal is replaceable

La señal puede ser ORB, pullback, mean reversion, momentum, random control o cualquier estrategia futura. El resto del sistema no debe depender de ella.

Contrato conceptual:

`MarketData → SignalIntent(direction, confidence/context, invalidation)`

#### P3 — Intra-trade management is replaceable

Motor independiente que recibe una posición abierta y decide:

- HOLD
- ADD_ADVERSE
- ADD_FAVORABLE
- MOVE_STOP
- MOVE_TARGET
- EXIT

Gerard inspira dos políticas iniciales:

- `negative_recovery`
- `positive_pyramiding`

pero no son parte de la señal.

#### P4 — Inter-trade risk is replaceable

El riesgo del siguiente trade es una política separada:

`nextRisk = f(previousResults, accountState, propRules)`

Ejemplos:

- fixed;
- geometric recovery;
- bounded recovery;
- state-based.

#### P5 — Prop lifecycle is a state machine

`EVALUATION → FUNDED_PRE_PAYOUT → PAYOUT_ELIGIBLE → WITHDRAWN | BURNED`

Las reglas de Topstep/TPT/etc. son adapters/configuración, no lógica de estrategia.

#### P6 — Account inventory is a portfolio

20 cuentas copiando una Reference no son 20 muestras independientes. Son una cohorte altamente correlacionada con costes multiplicados. El modelo debe medir:

- burn rate;
- pass rate;
- funded-to-payout conversion;
- payout rate;
- cash net;
- capital lock;
- expected attempts per withdrawal.

#### P7 — High win rate is an instrument, not the objective

El win rate se usa para aumentar la probabilidad de atravesar la state machine de la prop. La métrica final sigue siendo cash neto por capital real y tiempo.

### Contratos conceptuales

```text
SignalModel
  market data -> entry intent

IntraTradeManager
  position + market path -> adds/stops/targets/exits

InterTradeRiskPolicy
  trade history + account state -> risk budget

PropRuleSet
  account state + PnL path -> violations/eligibility/transitions

ExecutionCostModel
  fills -> commissions/slippage

BacktestEngine
  market path + above components -> trade/account/cohort events

PropEconomicsSimulator
  trade/account event distribution -> attempt/payout/cash distributions
```

Todos deben ser intercambiables.

### Dos simuladores, no uno

#### A — Prop Economics Simulator

Se puede construir **antes** de tener datos de mercado.

Inputs sintéticos:

- win probability;
- win payoff;
- loss payoff;
- trade frequency;
- distribution/tail assumptions;
- variable-risk policy;
- prop rules;
- fees/activation/reset/payout.

Pregunta que responde:

> ¿Qué payout conversion mínima hace rentable una cohorte y cuánto podemos pagar por intento?

EV simplificado por attempt:

`EV = p_payout * (net_payout - success_only_costs) - always_paid_costs`

Break-even:

`p_payout* = always_paid_costs / (net_payout - success_only_costs)`

Esto permite validar la asimetría de negocio independientemente del edge.

#### B — Market Strategy Backtester

Produce distribuciones auténticas de trades/secuencias para sustituir los inputs sintéticos de A.

Orden:

1. C0 random / S1 ORB / S2 pullback con gestión simple.
2. Añadir negative recovery.
3. Sólo finalists: positive hardscalping.
4. Pasar secuencias resultantes al Prop Economics Simulator.
5. Aplicar variable-risk allí o en una capa superior reproducible.

### Resolución de datos — política

**1m sirve para screening, no para certificar hardscalping.**

Con adds + SL + TP dinámicos, una vela de 1m puede tocar múltiples niveles sin indicar el orden. Por tanto:

- **Tier 1 — discovery:** OHLCV 1m para desarrollar señales, regimes y descartar ideas malas rápidamente.
- **Tier 2 — finalist:** 1s o trades/tick para reconstruir path intrabar y secuencias de adds.
- **Tier 3 — execution proof:** NinjaTrader High Fill Resolution / Market Replay para confirmar comportamiento del finalist en la plataforma de destino.

Un resultado final basado sólo en 1m no puede cerrar G2 si el orden intrabar cambia el outcome.

### Fuente de datos recomendada para el sprint

**Databento historical CME** es el candidato preferido:

- PAYG histórico, sin necesidad de suscripción para empezar;
- CME/CBOT/NYMEX/COMEX;
- histórico amplio;
- OHLCV 1m y 1s;
- trades/tick y L1 disponibles si el finalist lo requiere;
- API permite estimar coste antes de descargar.

Estrategia de gasto:

1. bajar primero NQ/MNQ 1m para varios años;
2. D4 screening;
3. identificar periodos/configuraciones finalists;
4. descargar 1s/trades sólo para finalists y periodos de validación;
5. evitar L2/PCAP salvo evidencia de que el modelo realmente lo necesita.

CME DataMine queda como alternativa autoritativa pero no como primera opción por coste/complejidad.

### Backtest stack recomendado

#### Research harness — recomendado

Un runner pequeño y desechable, independiente de NinjaTrader.

Responsabilidades:

- ingest normalizado;
- continuous/contract-aware futures series;
- session calendar/timezone;
- deterministic signal modules;
- event-driven position/recovery engine;
- commissions/slippage;
- event log completo;
- parameter grid acotado;
- outputs Parquet/CSV.

No debe implementar prop rules profundamente; emite eventos para el simulator económico.

**Lenguaje:** elegir por velocidad de entrega, no por producción. Python tiene menor fricción con Databento y análisis; Go sigue siendo válido si reutilizarlo compensa. El harness no define arquitectura futura de Echo.

#### NinjaTrader Strategy Analyzer — verificación secundaria

Útil para reconstruir el finalist cerca del runtime futuro:

- soporta backtest/optimization/walk-forward;
- puede incluir comisiones y slippage;
- High Order Fill Resolution permite usar una serie secundaria más granular, incluso 1-tick.

No usar como única verdad del research porque acoplaría la exploración a NinjaScript y hace más incómodo separar strategy/management/prop economics.

#### NinjaTrader Playback / Market Replay — prueba final de ejecución

Usarlo después para reproducir periodos concretos y comparar el event log del harness con el comportamiento NinjaScript.

### Output mínimo por secuencia

```text
sequence_id
strategy_id
parameter_set_id
contract
session
entry_ts
direction
entry_price
initial_qty
initial_money_risk
initial_money_target

adds[]
  ts
  price
  qty
  adverse_or_favorable
  avg_price_after
  total_qty_after
  stop_after
  target_after

exit_ts
exit_reason
exit_price
gross_pnl
commission
slippage
net_pnl
mae_money
mfe_money
duration
max_qty
max_adverse_distance
```

El Prop Simulator añade posteriormente account_id, lifecycle state, fees, violations, eligibility y payouts.

### D3 acceptance gate

D3 PASS cuando:

- P1–P7 quedan aceptados como abstracciones;
- C0/S1/S2 tienen reglas exactas;
- negative recovery tiene un espacio pequeño de parámetros;
- se elige dataset y runner;
- se define el event schema;
- ninguna decisión pendiente impide que un agente implemente D4 sin reinterpretar la tesis.


## 🎲 D3 revisión — Simulation-first, market-data deferred

**Decisión:** antes de cualquier backtest histórico, construir un simulador estocástico completo de operativa + prop lifecycle. El objetivo inmediato no es probar una estrategia concreta, sino responder si la asimetría económica puede funcionar bajo supuestos explícitos y conservadores.

### Tres niveles de abstracción

#### L0 — Bernoulli ladder (sanity / optimistic bound)

Modelo deliberadamente simple:

- cada nodo de decisión tiene probabilidad `p` de resolver favorablemente;
- si falla, alcanza el siguiente trigger adverso y permite un add;
- máximo `N` adds;
- si ninguno resuelve, termina en full stop.

Con independencia artificial:

`P(sequence_win) = 1 - (1-p)^(N+1)`

Este modelo sirve para intuición y upper-bound, **no como simulación final**, porque los nodos dentro de un mismo path no son realmente independientes.

#### L1 — Stochastic price path (canonical null model)

Simular un precio sin datos históricos:

- random walk / Brownian discretizado;
- baseline sin drift = mercado martingala;
- ticks/pasos suficientemente pequeños;
- SL, TP y add levels son barreras reales;
- al tocar un add se agrega size, se recalcula average price y se vuelven a calcular las bandas monetarias;
- la probabilidad de resolver favorablemente emerge del path, no de una nueva moneda independiente.

Para un proceso sin drift y barreras lower/upper, la probabilidad de tocar upper antes que lower depende de la posición actual dentro de ambas barreras. Por tanto, una escalada puede modificar la probabilidad al cambiar average/SL/TP, pero no crea edge gratis.

#### L2 — Synthetic strategy edge

Inyectar una ventaja controlada sin datos reales:

- baseline 50%;
- escenarios equivalentes a 52.5%, 55%, 57.5%, 60%, 65% de éxito para una operación simple;
- representar ese edge mediante drift/conditional probabilities calibradas;
- recovery posterior sigue condicionado al path, no se vuelve mágicamente independiente.

Esto permite preguntar:

> Si tengo una estrategia genuina de 55% o 60%, ¿qué hace Gerard encima de esa ventaja?

### Componentes del simulador

```text
MarketProcess
  BernoulliLadder | RandomWalk | BiasedRandomWalk | optional RegimeSwitch

SignalQuality
  target simple-trade win probability / calibrated drift

TradePolicy
  initial money risk
  initial money target
  direction

RecoveryPolicy
  add triggers
  add sizes
  max adds
  average-price recalculation
  constant/variable money SL
  constant/variable money TP

PositivePyramidPolicy
  initially OFF

InterTradeRiskPolicy
  fixed | geometric | bounded recovery
  initially OFF for first experiments

PropRuleSet
  Topstep | Lucid | Apex | future adapter

AccountLifecycle
  evaluation -> funded -> payout eligible -> payout | burned

CohortPolicy
  account count
  synchronized/correlated vs staggered/independent states

MonteCarloRunner
  seeds
  runs
  sensitivity grid
```

### Critical distinction — attempts vs correlated copies

`10 accounts` only approximate ten independent attempts if their outcomes are materially decorrelated.

If all 10 accounts execute the same Reference, same risk state and same trades, correlation approaches 1: a bad sequence can burn all 10 simultaneously. The simulator MUST support:

- `rho=1`: fully synchronized copies;
- staggered lifecycle/risk states;
- independent strategies/seeds as a theoretical bound;
- mixed cohorts.

The metric `1 payout per 10 accounts` must therefore be measured as **payouts / purchased evaluations**, not inferred from count of simultaneously copied accounts.

### Metrics

Trade/recovery:
- sequence win rate;
- full-stop probability;
- expected sequence PnL;
- max/additional contracts;
- average number of adds;
- tail loss frequency;
- expected path length.

Account:
- evaluation pass probability;
- pass -> funded probability;
- funded -> first-payout probability;
- purchase -> first-payout probability;
- expected accounts burned per payout;
- expected activation fees per payout;
- expected time/trades to payout.

Business:
- gross payouts;
- net payouts after split;
- total eval/reset/activation cost;
- commissions/slippage scenario cost;
- net cash per 10/20/50/100 purchased evaluations;
- probability cohort ends net positive;
- P5/P50/P95 net cash;
- max cash outlay before first payout;
- break-even payout conversion.

### Prop adapters — initial scope

Use current official rules as versioned configuration. Rules are inputs dated by capture; never hard-code them into strategy logic.

Initial adapters:
- Topstep 50K Standard;
- Lucid 50K candidate(s);
- Apex 50K EOD candidate.

Other props enter only after these produce insight.

### Revised validation order

1. **L0:** Bernoulli ladder to sanity-check the intuition and calculate optimistic bounds.
2. **L1:** driftless random-walk market + Gerard negative recovery.
3. **L2:** inject 55/60% strategy edge and repeat.
4. Add prop lifecycle rules.
5. Add variable inter-trade risk.
6. Add cohort correlation/staggering.
7. Stress parameters and produce sensitivity surfaces.
8. Only after this decide whether historical backtest adds enough information.
9. Before a material multi-account spend, use a small live/paper/evaluation calibration cohort to measure model error.

Historical backtesting is now **DEFERRED**, not mandatory for the first economic verdict.

### Gate before real-money pilot

A strong Monte Carlo result is necessary but not sufficient because the stochastic process is an assumption, not empirical market evidence.

The simulator must identify which assumptions drive profitability and survive pessimistic scenarios. A real-money pilot, if authorized later, starts as a calibration experiment rather than jumping directly from synthetic simulation to a large synchronized cohort.


## 🧮 D3 matemática — qué hace realmente un add en un mercado aleatorio

### Resultado central

La intuición correcta es:

> después de un add existe una nueva probabilidad condicional.

La intuición incorrecta sería:

> después de un add vuelve a existir una moneda 50/50 independiente.

Bajo un random walk/Brownian sin drift, el futuro desde el nuevo precio es memoryless, pero la probabilidad de tocar TP antes que SL depende de **dónde quedó el precio actual entre ambas barreras**.

Para un precio actual `x`, barrera inferior `L` y superior `U`:

`P(hit U before L) = (x - L) / (U - L)`

### Ejemplo canónico

Entrada inicial:

- price = 0;
- qty = 1;
- TP monetario = +100;
- SL monetario = -100;
- add trigger = -30.

Si se llega a -30 y se agrega otro contrato igual:

- entradas: 0 y -30;
- average = -15;
- qty total = 2;
- para conservar +100/-100 monetarios, cada banda queda a 50 unidades del average;
- nuevo TP de precio = +35;
- nuevo SL de precio = -65.

Desde el precio actual -30:

- distancia al TP = 65;
- distancia al SL = 35.

Por tanto, bajo random walk sin drift:

`P(win | reached add) = 35 / (65 + 35) = 35%`

No 50%.

Antes del add:

`P(hit +100 before -30 | start 0) = 30 / 130 = 23.0769%`

y:

`P(reach -30 first) = 76.9231%`

Probabilidad total de acabar en +100:

`23.0769% + 76.9231% * 35% = 50%`

Exactamente la misma probabilidad inicial.

### Interpretación

El add sí transforma qué paths ganan y cuáles pierden.

Puede existir un path que:

- habría terminado en -100 con la operación original;
- pero después del add toca el TP comprimido antes;
- por tanto el recovery lo convierte en ganador.

Pero existe el conjunto complementario:

- paths que la operación original habría soportado y finalmente llevado a +100;
- el nuevo SL comprimido los corta antes;
- por tanto el recovery convierte esos winners originales en losses.

En un proceso perfectamente aleatorio ambos efectos se compensan.

### Principio general

Si el PnL es una martingala y una política de sizing:

- sólo usa información pasada/presente;
- no aporta forecasting edge;
- conserva resultados terminales fijos `+G` y `-L`;
- no tiene costes ni overshoot material;

entonces:

`P(win) = L / (G + L)`

independientemente de cómo se cambie el size durante el camino.

Para:

- +100 / -100 -> 50%;
- +1500 / -2000 -> 2000/3500 = 57.1429%;
- +500 / -2000 -> 80%.

El sizing dinámico puede cambiar:

- tiempo hasta resolución;
- máximo size;
- distribución de MAE/MFE;
- qué paths concretos ganan;
- exposición a slippage/costes;
- comportamiento frente a reglas path-dependent de una prop;

pero **no crea edge desde una martingala por sí solo**.

### Por qué no es Monty Hall

Monty Hall entrega información adicional correlacionada con un estado oculto fijo: el presentador sabe dónde está el premio y abre deliberadamente una puerta perdedora.

En un random walk memoryless no existe un resultado final preseleccionado de la primera entrada.

Llegar a -30 informa que el path pasado fue adverso, pero no revela que “la primera operación iba a perder”. Desde -30, los incrementos futuros siguen siendo simétricos bajo el null model.

Por eso la comparación útil no es Monty Hall sino **first-passage probabilities con barreras móviles**.

### Cuándo Gerard sí puede mejorar el resultado

El recovery puede mejorar materialmente la probabilidad o EV si al menos una de estas condiciones rompe el null model:

1. **Conditional mean reversion:** después de una excursión adversa, la probabilidad real de rebote es superior a la del random walk.
2. **Entry edge:** la señal inicial induce drift/estructura favorable.
3. **Asymmetric terminal payoff:** TP/SL monetarios no permanecen constantes; se intercambia win rate por tamaño de tail loss.
4. **Path-dependent exits:** scratches, BE, partials o pyramiding producen más de dos outcomes terminales.
5. **Prop nonlinearities:** evaluation fee, trailing drawdown, consistency, payout caps y limited liability del trader hacen que el valor económico externo no sea igual al PnL esperado dentro de la cuenta.

Por tanto, el simulador debe separar dos preguntas:

**Q1 — Trading null:** ¿negative recovery por sí solo crea algo bajo random walk?
Expected answer teórico: no; debe reproducir la invariancia anterior. Esto es un test del simulador.

**Q2 — Economic/conditional edge:** ¿qué nivel de mean reversion, signal edge o rule asymmetry hace rentable la política completa?
Ésta es la pregunta útil para Echo Futures.

### Nuevo acceptance test obligatorio del simulador

Antes de simular props:

- random walk;
- +100/-100;
- cualquier número de adds;
- cualquier sizing predictivo válido;
- barriers monetarias finales fijas.

El Monte Carlo debe converger aproximadamente a 50% win rate y EV 0 antes de costes.

Con +1500/-2000 debe converger aproximadamente a 57.1429% winners y EV 0.

Si el simulador muestra mejora material sólo por aumentar size, contiene un bug o una asunción oculta que debe declararse.


## 🎯 D3 tesis matemática — funding as a stochastic control problem

### Disciplina matemática correcta

La idea toca teoría de juegos, pero el núcleo cuantitativo inicial es:

- **gambler's ruin / first-passage probabilities**;
- **absorbing Markov chains** para evaluation/funded/payout/burn;
- **stochastic control / MDP** para elegir size, adds y riesgo según estado;
- **risk of ruin** y Monte Carlo para capital requerido;
- teoría de juegos entra después porque prop y trader tienen incentivos opuestos y reglas que cambian la estrategia óptima.

### Null model de una cuenta

Para un proceso justo sin drift, partiendo entre una barrera de pérdida `-L` y un objetivo `+G`:

`P(hit +G before -L) = L / (G + L)`

Ejemplo abstracto de evaluation:

- target +3000;
- burn -2000.

Entonces:

`P(pass before burn) = 2000 / 5000 = 40%`

y el número esperado de evaluations por pass bajo este modelo ideal es:

`1 / 0.40 = 2.5`

Esto NO modela todavía trailing drawdown, consistency, daily rules, commissions ni discrete overshoot.

### Evaluation + funded como dos estados absorbentes consecutivos

Si evaluation tiene probabilidad `p_eval` de alcanzar FUNDED y desde funded existe probabilidad `p_funded` de llegar al primer payout antes de burn:

`p_purchase_to_payout = p_eval * p_funded`

Ejemplo puramente ilustrativo con `p_eval=40%`:

| Funded barrier abstracta | p_funded bajo random walk | p_purchase_to_payout | attempts esperados / payout |
|---|---:|---:|---:|
| +3000 / -2000 | 40.00% | 16.00% | 6.25 |
| +4000 / -2000 | 33.33% | 13.33% | 7.50 |
| +5000 / -2000 | 28.57% | 11.43% | 8.75 |
| +6000 / -2000 | 25.00% | 10.00% | 10.00 |

Por tanto, **1 payout cada 10 evaluations compradas no requiere necesariamente un edge enorme** en un modelo idealizado. Puede emerger de la geometría de targets/drawdowns. Las reglas reales decidirán cuánto se aleja el producto de este bound.

### Qué significa q = 10%

Si la conversión real purchase→first payout es `q=0.10` y los intentos son independientes:

- intentos esperados hasta primer payout = `1/q = 10`;
- cuentas fallidas esperadas antes del payout = `(1-q)/q = 9`;
- probabilidad de >=1 payout dentro de 10 intentos = `1-(1-q)^10 ≈ 65.13%`;
- dentro de 20 intentos ≈ `87.84%`;
- dentro de 30 intentos ≈ `95.76%`.

Esto describe intentos independientes. Cohortes copiadas/correlacionadas requieren otro modelo.

### Economics break-even

Si cada evaluation cuesta `F`, existe un coste success-only `A` y el cash neto de un primer payout es `W`, una aproximación de break-even es:

`EV_per_attempt ≈ q_payout*W - F - p_pass*A - other_expected_costs`

Donde `p_pass` es evaluation→funded y `q_payout` es purchase→first-payout. Como normalmente `p_pass > q_payout`, usar `q_payout*A` subestima el coste de activaciones de cuentas que pasan y mueren antes de retirar.

Con `q_payout=10%`:

`W_break_even ≈ (F + p_pass*A + other_expected_costs) / 0.10`

El simulador debe utilizar cash real, nunca balance nominal.

### Rol exacto del hardscalping

Bajo martingala pura y terminales monetarios fijos, los adds no aumentan hit probability. Sí pueden:

- reducir tiempo hasta absorción;
- cambiar qué paths concretos ganan/pierden;
- adaptar el path a reglas temporales/de consistencia de la prop;
- aprovechar **conditional mean reversion** si existe.

La hipótesis Gerard relevante pasa a ser:

`P(rebound before tightened stop | adverse state) > fair first-passage probability`

No basta con “el mercado eventualmente revierte”. Debe revertir **antes del stop comprimido y dentro del horizonte permitido**.

### Variable experimental de mean reversion

En cada add state el simulador conoce la probabilidad fair teórica `p_fair`.

Debe poder inyectar:

`delta_reversion = p_real - p_fair`

y barrer, por ejemplo:

- 0 pp — null;
- +2 pp;
- +5 pp;
- +10 pp;
- +15 pp.

Así se descubre cuánto edge condicional necesita realmente Gerard para cambiar materialmente:

- sequence win probability;
- pass probability;
- purchase→payout conversion;
- cash EV.

### Pregunta central del proyecto

La primera pregunta ya no es:

> ¿Qué estrategia tiene mejor backtest?

Es:

> ¿Qué combinación mínima de geometría de prop + control de riesgo + edge condicional produce una conversión purchase→payout superior al break-even económico?

Sólo después se necesita encontrar una estrategia de mercado que produzca empíricamente ese edge condicional.


## 🧠 D3.1 — Astra/GOD mathematical review

**Objetivo:** usar un único shot corto de Astra como revisor matemático adversarial antes de congelar la SPEC e implementar. No es una sesión de research, arquitectura ni operaciones.

### Scope permitido

Astra recibe todo el modelo matemático necesario dentro del prompt y sólo debe:

- validar/corregir first-passage/gambler's ruin;
- validar condiciones de optional stopping/martingala para sizing dinámico;
- revisar el ejemplo del add en -30;
- validar composition evaluation→funded→payout;
- validar expected attempts y cash-EV;
- recomendar el **modelo estocástico mínimo coherente** para null + synthetic conditional mean reversion;
- producir acceptance tests analíticos para el simulador.

### Scope prohibido

- NO MCPs.
- NO web.
- NO GitHub.
- NO Agents-OS.
- NO logs.
- NO archivos.
- NO implementación.
- NO arquitectura Echo/NinjaTrader.
- NO investigación de props.
- NO backtesting.
- NO búsqueda de estrategias.
- NO extender el problema a portfolio optimization sofisticada.

Si falta una regla concreta de una prop, debe tratarla como variable simbólica; no buscarla.

### Claims que debe auditar

1. Driftless Brownian/random walk entre barreras fijas: `P(hit U before L)=(x-L)/(U-L)`, con condiciones y matices discrete/continuous.
2. Ejemplo: entry 0, qty 1, terminal PnL +100/-100, add qty 1 al llegar price -30; tras add, average -15, TP +35, SL -65, `P(win|-30)=35%`, total desde 0 = 50%.
3. Generalización: bajo precio martingala, estrategia self-financing/predictable, terminal wealth exactamente `+G/-L`, absorción y condiciones de optional stopping, sizing dinámico no crea expectancy y `P(win)=L/(G+L)`.
4. Evaluation abstracta +3000/-2000 bajo wealth martingale continuo: `P(pass)=40%`.
5. `P(purchase→payout)=P(pass)*P(payout|pass)`; no requiere independencia si la segunda probabilidad es condicional correctamente.
6. Para attempts IID con conversion `q`: expected attempts until payout `1/q`, expected failed attempts `(1-q)/q`, `P(>=1 payout in n)=1-(1-q)^n`.
7. First-payout economics: `EV_attempt=q_payout*W - F - p_pass*A - E[other costs]`; distinguir payout neto, activation y cuentas que pasan pero mueren antes de retirar.
8. El concepto “game theory” es secundario mientras las reglas de la prop sean exógenas; el modelo principal es stochastic control/MDP sobre un mecanismo fijo.
9. Negative recovery puede generar valor sólo si aparece conditional edge, cambia terminal payoff/state outcomes, o interactúa favorablemente con reglas path-dependent; size puro bajo null no crea edge.
10. Para synthetic mean reversion, revisar si conviene representar el edge como state-dependent transition probability / drift y cómo hacerlo sin contradecir el null model.

### Entregable esperado

Astra debe producir:

- tabla `CLAIM → CORRECT | CORRECT_WITH_CONDITIONS | WRONG`;
- corrección/proof sketch corto por claim;
- SPEC matemática mínima del simulador v0;
- acceptance tests con resultados analíticos esperados y tolerancias Monte Carlo;
- lista de hidden assumptions/counterexamples;
- qué NO modelar en v0;
- verdict final `MATH_GO | MATH_REVISE`.

No debe producir código.


## 🧾 D1 — Gerard García: extracción del curso v0

**Fuente:** brain dump + re-visionado reciente del curso privado por el owner + captura de la tabla de riesgo variable. Estado: `GERARD_V1_EXTRACTED / OBJECTIVIZATION_REQUIRED`.

### Estrategias/entradas recordadas

- **Nasdaq Opening Range:** observar los primeros 30 minutos y operar en 5m la ruptura del rango a favor de la dirección de ruptura, sin exigir cierre de vela. Asociada por el owner a hard scalping positivo.
- **H4 trend + LTF pullback:** identificar tendencia clara en H4 y buscar en temporalidad inferior entradas de pullback; ejemplo alcista: precio alcanza banda inferior de Bollinger en 5m y se busca recorrido hacia banda superior.
- **Nasdaq momentum por sesión:** sumarse a tendencia/momentum en sesión de Londres y en sesión de Nueva York, tratándolas como contextos separados.
- **Range breakout genérico:** formar rango durante un periodo X y entrar inmediatamente al romper, sin esperar confirmación de cierre.
- **Relevant high/low continuation/reversal:** si cierra por debajo de un mínimo relevante, entrar buscando continuación; si la vela rompe el mínimo pero recupera y cierra por encima, considerar entrada contraria. Simétrico para máximos.

Gerard prioriza la gestión sobre el edge de entrada y, según el recuerdo del owner, sostiene que la dirección inicial podría incluso decidirse aleatoriamente. Esto queda como afirmación a contrastar, no como edge certificado.

### Tres motores de gestión que deben probarse por separado

**A. Negative hardscalping / recovery intra-trade.** Ante movimiento adverso, agrega contratos y acerca las barreras de salida. Ejemplo recordado: 3 micros + 3 + 3. La intención declarada es conservar aproximadamente el riesgo monetario y el objetivo monetario mientras aumenta el tamaño total, por lo que el SL/TP en precio se comprimen alrededor del nuevo precio medio. Gerard decide trigger, distancia y sizing de forma altamente discrecional según volatilidad/espacio disponible; por tanto el proyecto no intentará copiar su ojo, sino parametrizar esos grados de libertad y buscar regiones robustas.

**B. Positive hardscalping / pyramiding.** Cuando la operación ya avanza con fuerza a favor, agrega exposición, mueve la protección hacia breakeven y deja correr una extensión grande; el owner recuerda objetivos del orden de 1:6. Debe tratarse como motor independiente del recovery adverso.

**C. Variable risk progression entre trades.** Captura suministrada: riesgo inicial 300, multiplicador 1.20 y reward:risk 1:1.5. La tabla visible muestra aproximadamente 300→360→432→518→622→746→896→1075 de riesgo por intento. Esta progresión no es equivalente al hardscalping intra-trade y requiere aclarar regla de reset, lotaje y objetivo real.


### Entrevista Gerard — decisiones cerradas v1

- **Recovery trigger original:** discrecional. En directos agrega exposición en distintos momentos para acelerar el retorno; no existe una condición mecánica única observada por el owner.
- **Sizing intra-trade:** variable. Parte pequeño y suma progresivamente; `3 + 3 + 3 micros` es un ejemplo habitual, no una constante. La distancia disponible depende de volatilidad, timeframe, riesgo monetario y expectativa de movimiento.
- **Autoridad del riesgo:** confirmada en dólares. Si la secuencia tiene riesgo máximo de, por ejemplo, 2K, cada aumento de contratos obliga a recalcular la distancia del SL desde el nuevo precio medio para que la pérdida monetaria siga aproximadamente en 2K. Lo mismo aplica al objetivo monetario; por eso las bandas se comprimen.
- **Positive hardscalping:** también discrecional. Debe objetivizarse con reglas medibles —persistencia direccional, velas consecutivas, desplazamiento ATR/R, breakout estructural o MFE— en vez de copiar decisiones visuales.
- **Variable risk:** tras un win vuelve al primer escalón y la intención declarada es que el siguiente ganador recupere todas las pérdidas previas y además termine positivo. La foto fue tomada mientras la hoja se modificaba; sus valores no son autoridad de fórmula.
- **Entry edge:** Gerard usa distintos modelos en vivo y prioriza la gestión sobre la precisión de entrada. La tesis “podría entrar con una moneda” queda como hipótesis experimental.
- **Fondeada:** el curso prioriza un arranque agresivo, buscando rápidamente profit grande o burn, y posteriormente sesiones menores para satisfacer payout/consistency. La regla exacta debe venir siempre de la prop vigente.
- **Instrumento/lotaje:** no congelar 3 micros, 30 micros ni MNQ/NQ como constantes. El contrato correcto es riesgo monetario + espacio de precio + límite de contratos.
- **Account size inicial:** 50K es el candidato actual. 150K queda como fase posterior si la economía mejora al escalar.

### Parámetros a objetivizar

- trigger de add por movimiento adverso: puntos/ticks, ATR, fracción del SL inicial, estructura o combinación;
- número máximo de adds;
- fracción de exposición usada en cada add;
- spacing fijo vs. progresivo;
- target monetario fijo vs. variable tras cada add;
- stop monetario fijo vs. reducido;
- criterio de positive hardscalping;
- condición de BE;
- extensión de target tras momentum favorable;
- multiplicador de variable risk entre trades;
- reset tras win y stop de secuencia/cuenta.

**Principio de validación:** una solución válida debe sobrevivir en un rango de parámetros. Si sólo funciona con un punto exacto de spacing/multiplicador, falla robustness.

### Baseline experimental obligatoria

1. **Random direction:** dirección 50/50 + gestión Gerard parametrizada.
2. **Entry-only:** cada entry model con SL/TP simple, sin recovery ni variable risk.
3. **Recovery delta:** mismo entry + hardscalping adverso.
4. **Positive hardscalping delta:** agregar pyramiding favorable.
5. **Variable-risk delta:** progresión entre trades.
6. **Full stack:** combinación final.

Esto permite localizar si el edge proviene de la entrada, del recovery, de la asimetría económica de la prop o de una mezcla.

### Fórmula útil para variable risk

Si el riesgo sigue `R_n = R_0 * m^n` y el ganador paga `b * R_n`, exigir que cualquier primer win tras una cadena de pérdidas recupere todo y deje siempre el mismo beneficio inicial conduce a:

`m = 1 + 1/b`

Para `b=1.5`, `m=1.6667`. Con `R_0=300`, una cadena idealizada sería aproximadamente `300 → 500 → 833 → 1389...`, y cualquier win dejaría aproximadamente +450 neto. Es una derivación matemática del objetivo descrito por el owner; no se atribuye a Gerard hasta confirmar su hoja.

### Modelo matemático provisional del recovery

Si después de cada add el objetivo monetario (P) y la pérdida monetaria máxima (R) permanecen constantes, para una posición long agregada con cantidad total (Q), precio medio ponderado (ar p) y valor monetario por punto/unidad (v):

- (SL = ar p - R/(Qv))
- (TP = ar p + P/(Qv))

Para short, los signos se invierten. Al aumentar (Q), ambas distancias en precio se reducen. Esto reproduce exactamente la intuición de “las bandas se juntan” descrita por el owner, pero queda `INFERRED` hasta confirmar que Gerard conserva dólares constantes y recalcula sobre el average price.

### Hallazgo sobre la tabla de riesgo variable

Con (R_0=300), multiplicador (m=1.20) y payoff (1.5R), la secuencia visible implica:

- win inmediato: +450 acumulado;
- una pérdida y luego win: +240;
- dos pérdidas y luego win: -12;
- tres pérdidas y luego win: aproximadamente -314;
- cuatro pérdidas y luego win: aproximadamente -677.

Por tanto, **esa tabla por sí sola no puede significar “cualquier siguiente win recupera todo y deja positivo”**. A 1:1.5, un multiplicador asintótico superior a ~1.667 sería necesario para garantizar recuperación total de una cadena arbitraria de pérdidas. Debe existir otra regla, un objetivo distinto o el recuerdo mezcla dos modelos. Además, la última pérdida acumulada visible en la captura no sigue limpiamente la progresión 1.20, por lo que esa fila requiere explicación antes de usarla.

### Modelo económico de prop recordado

- **Topstep 50K:** el owner recuerda coste aproximado 89 USD, sin activación, profit target 3K y pérdida permitida 2K. Todo debe verificarse contra reglas oficiales vigentes antes de simular dinero.
- **Evaluation:** filosofía sacrificial/agresiva. Ejemplo recordado: buscar +1.5K con -2K de riesgo; secuencias posteriores de +500/+1K y cambios de riesgo todavía requieren explicar qué regla de la prop las origina.
- **Funded:** buscar un primer día de beneficio muy grande (orden 3K–4K) y luego varios días pequeños (ejemplo 500×4) para llegar a retiro. El motivo reglamentario exacto está `UNKNOWN`.
- **Account inventory:** mantener cuentas suplentes y rotar/replicar operaciones. Las cuentas se tratan económicamente como intentos desechables si el coste real de burn es bajo frente al payout potencial.
- Props mencionadas: Topstep y Take Profit Trader como principales; Alpha Futures, Tradeify y Lucid como secundarias. Ninguna regla actual queda congelada hasta research oficial.


### Topstep — contraste oficial vigente 2026-09-24

El curso no es autoridad de reglas comerciales. Primer contraste con documentación oficial vigente:

- Trading Combine 50K: profit target 3K, Maximum Loss Limit 2K y consistency target 55%; puede aprobarse en dos días si el mejor día no supera 55% del beneficio total.
- Límite Combine 50K: 5 minis / 50 micros.
- No hay límite de Trading Combines activos publicado; sí hay máximo de **5 Express Funded Accounts activas**.
- Precio 50K actual: **49 USD/mes Standard** + 149 USD de activación sólo al pasar, o **95 USD/mes No Activation Fee**. El 89 USD del curso/recuerdo está desactualizado.
- XFA Standard: 5 winning days de 150+ para payout. XFA Consistency: mínimo 3 días y largest day <=40% del net profit.
- Para traders nuevos aplica split 90/10. El request es hasta 50% del balance y el cap 50K es 2K Standard / 3K Consistency, salvo promociones/configuraciones específicas.
- El patrón “gran primer día + varios días pequeños” encaja mejor con Standard actual; con Consistency 40%, un día de 4K exige al menos 10K netos para que represente <=40%.
- La economía `1 payout / 20 attempts` depende del pricing path. Ejemplo simplificado: 20×95 = 1,900 USD; un request de 2K con split 90/10 entrega 1,800 antes de otros costes, por lo que no alcanza break-even. Con Standard: 20×49 + 149 de activación de la única cuenta aprobada = 1,129; 1,800 netos dejan ~671 USD antes de otros costes.

**Conclusión:** el pricing path es una variable del modelo de estrategia, no una decisión administrativa.

### Implicación económica importante

Debe distinguirse **trading EV dentro de la cuenta** de **cash EV del negocio de prop**. Una operativa puede tener expectancy mediocre o incluso negativa sobre PnL nominal y aun así ser económicamente interesante para el owner si el downside real por evaluation está limitado al fee mientras un camino exitoso habilita payouts mucho mayores. El simulador G1 debe modelar ambos niveles y nunca usar el balance nominal de 50K como capital real invertido.

### Bloqueos restantes Gerard/G0

La entrevista de conocimiento queda suficientemente cerrada para avanzar. Ya no buscamos una regla secreta para los puntos discrecionales: pasan a ser parámetros experimentales.

Pendientes:
- confirmar, si aporta valor, la fórmula exacta de la hoja de variable risk;
- extraer 3–5 ejemplos completos para calibrar rangos razonables de spacing/adds;
- seleccionar dos entry models para D3;
- ejecutar research público de contraste, especialmente pérdidas y límites;
- cerrar una configuración como máquina de estados simulable antes de PASS G0.


## 🔬 M0 — Forense de operativa

### Fuentes iniciales

- **Gerard García:** cursos y videos que posee el owner + material público pertinente.
- **Tradesfera:** operativa pública, sesiones, explicaciones y ejemplos relevantes.
- **Psicólogo del Trading:** material público y cualquier contenido del owner que se incorpore explícitamente.
- Cada regla derivada debe guardar fuente, timestamp/lección, evidencia, nivel de confianza y si es suficientemente determinista para automatizar.

### Contrato mínimo a reconstruir por operador/estrategia

- Instrumento(s), sesión y horario efectivo.
- Timeframe de decisión y, si existe, timeframe de contexto.
- Setup completo de entrada: indicadores, parámetros, cruces/niveles, filtros, contexto y condiciones de no-trade.
- Tipo de orden y timing real de entrada.
- Tamaño inicial y unidad de sizing.
- SL y TP iniciales: distancia, fórmula y autoridad para modificarlos.
- **Trigger exacto de aumento de posición:** distancia adversa, estructura, indicador, tiempo, volatilidad u otra condición; no aceptar “cuando se da vuelta” como regla.
- Secuencia de tamaños: cantidad máxima de adds, multiplicador o escalera exacta y exposición total máxima.
- Precio medio ponderado después de cada add.
- Regla exacta de recálculo de SL/TP después de agregar exposición.
- Condición de scratch/breakeven, salida parcial y cierre forzado.
- Qué ocurre si continúa en contra después del último add.
- Stop diario, stop por sesión y número máximo de secuencias fallidas.
- Reglas de noticias, rollover, baja liquidez y desconexión.
- Evidencia de trades ganadores **y perdedores**; no inferir el modelo desde highlights.

### Output G0

G0 queda PASS únicamente cuando exista al menos una estrategia candidata expresable como una máquina de estados sin decisiones humanas ambiguas y con ejemplos que cubran entrada normal, recovery/add, salida ganadora y pérdida completa. Si una regla material sigue siendo “a ojo”, el bot queda bloqueado.

## 💰 M1 — Gestión monetaria y economía de prop

El proyecto modelará la cuenta por **capital económico realmente arriesgable**, no por el balance publicitado de 50K/100K. Cada programa de prop debe normalizar como mínimo: coste de evaluación, activación, resets, profit target, drawdown y su modalidad, daily loss, límites de contratos, consistency, días mínimos, restricciones de scaling/DCA/copier/automatización, reglas de payout, máximo de cuentas y cualquier condición capaz de invalidar esta operativa.

### Estados económicos mínimos

- **EVALUATION_AGGRESSIVE:** perfil orientado a maximizar la probabilidad/velocidad de llegar a funded bajo un presupuesto de intentos explícito.
- **FUNDED_PRE_PAYOUT:** política posiblemente distinta; optimiza probabilidad de llegar al primer retiro.
- **PAYOUT_PROTECTED:** después de retirar, estudiar si conviene reducir riesgo, reciclar beneficio o mantener agresividad.
- Estos nombres son estados de investigación, no reglas congeladas; el análisis puede demostrar que dos o los tres deben usar la misma política.

### Variables de la secuencia hardscalping

- Riesgo inicial (R_0).
- Número máximo de adds (N).
- Tamaño por escalón (q_i).
- Distancia/trigger de cada add.
- Precio medio ponderado de la posición agregada.
- SL/TP agregado y pérdida máxima si falla toda la secuencia.
- MAE/MFE, tiempo expuesto y coste real de comisión/slippage por secuencia.
- Riesgo acumulado por cuenta, por sesión y por conjunto de cuentas correlacionadas.

### Métricas económicas obligatorias

- Probabilidad de pasar evaluation antes de quemarla.
- Probabilidad de primer payout dado que se llegó a funded.
- Probabilidad y coste de ruina por etapa.
- Intentos esperados y coste esperado hasta primer payout.
- Cash neto esperado por intento y por cohorte de cuentas.
- Expected payout / challenge+activation+reset cost.
- Tiempo esperado hasta cashflow y capital lock.
- Distribución P5/P50/P95 y drawdowns; no evaluar solo promedio.
- Efecto de comisiones, slippage, fills parciales y latencia.
- Sensibilidad a rachas: una estrategia 90% WR debe demostrar qué ocurre con la cola del 10%, incluyendo secuencias consecutivas.
- Correlación entre 40–80 cuentas cuando todas siguen la misma Reference; multiplicar cuentas no multiplica independencia.

### Gate G1

No se compra escala ni se construye fan-out multi-account hasta que exista una región de parámetros con EV neto positivo bajo supuestos conservadores y sin depender de una única combinación extremadamente frágil.

## 🧪 M2 — Estrategias candidatas y simulación

- Partir con pocas estrategias mecánicas de alta frecuencia operativa y alto win rate potencial; estocásticos en TF bajos son **candidato**, no decisión.
- Elegir un solo mercado inicial después de evaluar liquidez, tick value, comisiones, horario y compatibilidad con las reglas de la prop.
- Para una lógica de adds y salidas rápidas, exigir resolución de datos suficiente para reconstruir el path intratrade; una barra OHLC que no resuelva el orden de eventos no puede certificar la estrategia.
- El simulador debe reproducir también la prop: challenge/funded/payout, no solo una curva PnL.
- Separar edge de entrada, lógica de recovery y money management para poder medir cuánto aporta y cuánto riesgo agrega cada componente.

## 🏗️ M3+ — Automatización después de validar la operativa

- **M3 — Vertical slice NinjaTrader:** una Reference + una Execution + SIM + un instrumento + una estrategia.
- **M4 — Integración Echo:** identidad, comandos idempotentes, fills, reconciliación, position truth, límites y observabilidad.
- **M5 — Primera evaluation real:** una cuenta/plan con autorización explícita del owner y presupuesto máximo conocido.
- **M6 — Primer payout y aprendizaje:** comparar simulación versus ejecución real, recalibrar slippage/fills/rules.
- **M7 — Scale-out:** fan-out controlado hacia múltiples cuentas solo después de evidencia de retiro; crecer por cohortes y no saltar directo a 40–80.

## 🚦 Gates del proyecto

| Gate | Condición | Estado |
|---|---|---|
| G0 — Operativa | Estrategia + hardscalping completamente mecánicos, incluidos casos de pérdida | **WIP** |
| G1 — Economía | EV de challenge→primer payout positivo con costes y rules reales | BLOCKED by G0 |
| G2 — Simulación | Replay/path intratrade y simulador de prop reproducibles | BLOCKED by G1 |
| G3 — Execution | Reference→Echo→Execution reconciliado en SIM | BLOCKED by G2 |
| G4 — Real pilot | Primera evaluation real dentro de presupuesto explícito | BLOCKED by G3 + owner |
| G5 — Withdrawal | Primer retiro y discrepancias sim/live entendidas | BLOCKED by G4 |
| G6 — Scale | Cohortes multi-account con límites, observabilidad y kill-switch | BLOCKED by G5 |


## 🧱 Entrega de desarrollo

%% Esta sección siempre queda disponible. En proyectos que cambian código, configuración ejecutable, schemas o infraestructura, es obligatoria: una fila por repo/branch, con SPEC funcional y técnica enlazadas antes de implementar. En proyectos no técnicos, reemplazar la tabla por `_No aplica — <motivo>._`. %%

| Aplicación / repo | Branch | Base | SPEC funcional | SPEC técnica | Estado |
|---|---|---|---|---|---|
| Echo Futures simulator v0 / xKoRx/echo-futures (local) | master | `d4f42a41946f12231b75e4eb65b90d132731be0d` | [[D4 — Simulator v0 Functional SPEC]] | [[D4 — Simulator v0 Technical SPEC]] | D4 CERTIFIED / G4C ACCEPTED |
| Echo Futures runtime | TBD tras G0/G1 | TBD | BLOCKED — congelar después de G0/G1 | BLOCKED — congelar después de G0/G1 | NOT STARTED |

## 🧩 Subproyectos

```base
filters:
  and:
    - 'type == "project"'
    - 'file.hasLink(this.file)'
views:
  - type: cards
    name: Subproyectos
    order:
      - file.name
      - note.status
      - note.priority
```

## ✅ Tareas

> [!note]+ Ownership y tarea puente
> `#owner/me` = tuya · `#owner/agent` = de un agente · sin owner = clasifícala.
> El board es **adaptativo según `owner` del frontmatter**:
> - **Proyecto humano** (`owner: me`): muestra tus tareas y las **tareas puente** (`#type/supervision`) que representan proyectos de agente. Las tareas de agente **no** aparecen acá; viven en su propio proyecto.
> - **Proyecto de agente** (`owner: agent`): muestra las tareas del agente.

> [!example]- Fuente de tareas — editar / mover de estado aquí
> %% Estados: [ ] To Do · [/] WIP · [r] Review · [x] Done · [-] Canceled. Owners: #owner/me, #owner/agent. Tipos: #type/dev #type/admin #type/research #type/pr-review #type/supervision. Flags: #blocked #waiting #urgent. Ver [[convenciones]]. %%
> - [x] D1: hacer brain dump + entrevista dirigida de Gerard y congelar su knowledge contract #owner/me #type/research #area/echo
> - [x] D1: ejecutar research one-shot Gerard público para contraste #owner/agent #type/research #area/echo
> - [x] D1: ejecutar research one-shot Tradesfera con contrato común #owner/agent #type/research #area/echo
> - [x] D1: ejecutar research one-shot Psicólogo del Trading con contrato común #owner/agent #type/research #area/echo
> - [ ] Reconstruir una estrategia Gerard completa con evidencia y reglas mecánicas, incluyendo add/recovery y pérdida total #owner/me #type/research #area/echo
> - [-] Investigar y mecanizar operativa relevante de Tradesfera — research amplio cerrado; sólo principios explícitos pasan a D2 #owner/me #type/research #area/echo
> - [-] Investigar y mecanizar operativa relevante de Psicólogo del Trading — NO_GO por corpus técnico insuficiente; no gastar más tiempo sin video concreto #owner/me #type/research #area/echo
> - [x] D2: síntesis adversarial — pasan C0 random, S1 ORB30 y S2 H4+Bollinger; research amplio cerrado #owner/agent #type/research #area/echo
> - [x] D3: congelar simulador estocástico null + synthetic conditional edge + lifecycle abstracto; backtest histórico deferred #owner/me #type/research #area/echo
> - [x] D3.1: Astra/GOD mathematical review — MATH_GO; autoridad persistida en [[echo-futures-astra-math-review]] #owner/me #type/research #area/echo
> - [x] [[Echo Futures — Simulator v0]] arrancar + seguimiento #owner/me #type/supervision #area/echo
> - [/] [[Echo Futures — D5 Prop Economics]] arrancar + seguimiento #owner/me #type/supervision #area/echo
> - [-] D3–D5: construir shortlist mínima de prop/plan y normalizar rules que afectan la operativa — absorbido por [[Echo Futures — D5 Prop Economics]] #owner/me #type/research #area/echo
> - [/] D5: modelar Tier-1 Topstep + TPT `evaluation comprada → primer retiro real` con pass/funded intermedios, fees, activation, resets, drawdown, consistency, payout eligibility y cash neto #owner/me #type/research #area/echo
> - [-] Elegir instrumento/dataset — DEFERRED; simulation-first no requiere market data en v0 #owner/me #type/research #area/echo
> - [-] Backtest/replay histórico — DEFERRED hasta decisión posterior a D6/piloto de calibración #owner/agent #type/research #area/echo
> - [ ] D6: ejecutar validación adversarial y robustness #owner/agent #type/research #area/echo
> - [ ] D7: emitir GO/ITERATE/NO_GO y, solo si GO, congelar SPEC del MVP #owner/me #type/supervision #area/echo
> - [ ] Cerrar G0 y G1 antes de autorizar implementación NinjaTrader/Echo #owner/me #type/supervision #area/echo

```dataviewjs
const meta={" ":["To Do","var(--text-muted)","var(--background-modifier-border)"],"/":["WIP","#ba7517","rgba(234,124,12,.18)"],"r":["Review","#185fa5","rgba(55,138,221,.18)"],"x":["Done","#3b6d11","rgba(99,153,34,.18)"],"X":["Done","#3b6d11","rgba(99,153,34,.18)"],"-":["Canceled","var(--text-faint)","var(--background-modifier-border)"]};
function linkify(s){return String(s).replace(/\[\[([^\]|]+)(?:\|([^\]]+))?\]\]/g,(m,a,b)=>`<a class="internal-link" href="${a}" data-href="${a}">${b||a}</a>`).replace(/#[\w/-]+/g,m=>`<span style="opacity:.55;font-size:12px">${m}</span>`).replace(/📅\s*(\d{4}-\d{2}-\d{2})/g,(m,d)=>`<span style="opacity:.7;font-size:12px">📅 ${d}</span>`).replace(/[⏫🔼🔽⏬🔺]/g,"").replace(/✅\s*(\d{4}-\d{2}-\d{2})/g,"");}
function has(t,tag){return new RegExp(`(^|\\s)#${tag}(\\s|$)`).test(String(t.text));}
function render(tasks){const el=dv.el('div','');el.innerHTML=tasks.map(t=>{const[label,fg,bg]=meta[t.status]||["?","var(--text-muted)","var(--background-modifier-border)"];return `<div style="display:flex;align-items:center;gap:8px;margin:5px 0;"><span style="font-size:11px;font-weight:600;padding:1px 9px;border-radius:999px;background:${bg};color:${fg};min-width:56px;text-align:center;flex:none;">${label}</span><span>${linkify(t.text)}</span></div>`;}).join("");}
function board(tasks){const cols=[[" ","🟦 To Do"],["/","🟡 WIP"],["r","🔵 Review"]];let any=false;for(const[st,label]of cols){const c=tasks.filter(t=>t.status===st);if(c.length){any=true;dv.el('h4',label);render(c);}}const done=tasks.filter(t=>t.status==="x"||t.status==="X");if(done.length){any=true;dv.el('h4',"✅ Done");render(done);}if(!any)dv.paragraph("_Sin tareas._");}
const owner=((dv.current().owner)==="agent")?"agent":"me";
const all=dv.current().file.tasks.array();
const primary=all.filter(t=>has(t,`owner/${owner}`));
const loose=all.filter(t=>!has(t,"owner/me")&&!has(t,"owner/agent"));
dv.header(3, owner==="agent"?"🤖 Tareas del agente":"🧍 Mis tareas");
board(primary);
if(loose.length){dv.header(3,"🧺 Sin owner (clasificar)");render(loose);}
```

%% Rollup de iniciativa — descomentar solo en proyectos padre para ver las tareas #owner/me (incluye puentes) de todos los subproyectos, agrupadas por nota. Cambiar la ruta por la carpeta de esta iniciativa. Nunca muestra tareas de agente.
```dataviewjs
const meta={" ":["To Do","var(--text-muted)","var(--background-modifier-border)"],"/":["WIP","#ba7517","rgba(234,124,12,.18)"],"r":["Review","#185fa5","rgba(55,138,221,.18)"],"x":["Done","#3b6d11","rgba(99,153,34,.18)"],"X":["Done","#3b6d11","rgba(99,153,34,.18)"],"-":["Canceled","var(--text-faint)","var(--background-modifier-border)"]};
const ord={" ":0,"/":1,"r":2,"x":3,"X":3,"-":4};
function linkify(s){return String(s).replace(/\[\[([^\]|]+)(?:\|([^\]]+))?\]\]/g,(m,a,b)=>`<a class="internal-link" href="${a}" data-href="${a}">${b||a}</a>`).replace(/#[\w/-]+/g,m=>`<span style="opacity:.55;font-size:12px">${m}</span>`).replace(/📅\s*(\d{4}-\d{2}-\d{2})/g,(m,d)=>`<span style="opacity:.7;font-size:12px">📅 ${d}</span>`).replace(/[⏫🔼🔽⏬🔺]/g,"").replace(/✅\s*(\d{4}-\d{2}-\d{2})/g,"");}
function has(t,tag){return new RegExp(`(^|\\s)#${tag}(\\s|$)`).test(String(t.text));}
function render(tasks){const el=dv.el('div','');el.innerHTML=tasks.map(t=>{const[label,fg,bg]=meta[t.status]||["?","var(--text-muted)","var(--background-modifier-border)"];return `<div style="display:flex;align-items:center;gap:8px;margin:5px 0;"><span style="font-size:11px;font-weight:600;padding:1px 9px;border-radius:999px;background:${bg};color:${fg};min-width:56px;text-align:center;flex:none;">${label}</span><span>${linkify(t.text)}</span></div>`;}).join("");}
const pages=dv.pages('"10-projects/CARPETA-DE-LA-INICIATIVA"');
for(const p of pages.sort(x=>x.file.name)){const t=p.file.tasks.array().filter(x=>has(x,"owner/me")&&x.status!=="x"&&x.status!=="X").sort((a,b)=>(ord[a.status]??9)-(ord[b.status]??9));if(t.length){dv.el('h4',p.file.link);render(t);}}
```
%%

## 📆 Bitácora

%% Log diario para las dailies. Una línea por día con lo avanzado / blockers. %%
- **2026-09-23** — Proyecto creado y alcance corregido hacia operativa-first. Se registran como hipótesis: estrategias de alto win rate y TF bajo, hardscalping/recovery con aumento de exposición, gestión agresiva orientada a challenge/funded/payout y escalado futuro a decenas de cuentas. G0/G1 bloquean desarrollo hasta demostrar reglas mecánicas y economía positiva.
- **2026-09-23** — Activado management por `technical-project-manager`: horizonte máximo 7 días. Discovery se limita a tres one-shots paralelos (Gerard/Tradesfera/Psicólogo) bajo contrato común + entrevista Gerard; D2 síntesis, D3 mecanización, D4 backtest, D5 prop simulation, D6 robustness, D7 decisión y eventual freeze MVP.
- **2026-09-24** — Recibido primer brain dump del curso de Gerard + captura de risk table. Se separan tres motores: recovery adverso intra-trade, pyramiding positivo y variable-risk inter-trade. Derivado modelo provisional de bandas sobre average price y detectada contradicción útil en tabla 1.20/1:1.5: tras dos pérdidas, el siguiente win ya no recupera la secuencia.
- **2026-09-24** — Entrevista Gerard v1 suficientemente cerrada para avanzar: discrecionalidad pasa a parametrización experimental. Confirmado riesgo/TP monetario recalculado sobre average price. Derivada fórmula m=1+1/b para recovery geométrico constante y refrescada economía Topstep vigente; pricing path pasa a variable del simulador.
- **2026-09-24** — D2 PASS tras revisar los tres DR. Gerard público y Tradesfera son PARTIAL con inferencias excesivas; Psicólogo NO_GO por corpus insuficiente. Se cierra research amplio. Pasan a D3: C0 random-direction control, S1 NQ/MNQ ORB30 y S2 H4 trend + 5m Bollinger pullback. Negative hardscalping se prueba como módulo separado antes de positive pyramiding y variable risk.
- **2026-09-24** — D3 diseño abstracto iniciado: separadas SignalModel, IntraTradeManager, InterTradeRiskPolicy, PropRuleSet, ExecutionCostModel, BacktestEngine y PropEconomicsSimulator.
- **2026-09-24** — D3 replanteado a simulation-first: se pospone market data. Primero se probará toda la tesis con L0 Bernoulli, L1 random-walk y L2 synthetic-edge, luego lifecycle de props, variable risk y cohort correlation. Backtest histórico queda como herramienta posterior de calibración/falsificación, no prerrequisito.
- **2026-09-24** — Cerrada discusión matemática del add bajo null model: nueva probabilidad condicional sí, nueva moneda 50/50 no. Ejemplo +100/-100 con add en -30 y size 1+1 produce TP +35, SL -65; desde -30 la probabilidad condicional es 35%, y la probabilidad total sigue exactamente 50%. Se añade este resultado como acceptance test del simulador.
- **2026-09-24** — Reformulada tesis alrededor de `purchase→first-withdrawal conversion`. El 40% de pass del null model +3000/-2000 es sólo una propiedad del fixture abstracto y NO implica ninguna tasa real de retiro. D5 debe medir directamente `q_withdraw` bajo reglas reales; funded/pass se conserva sólo como estado intermedio diagnóstico.
- **2026-09-24** — D3.1 agregado: un único shot Astra/GOD actuará como mathematical reviewer con herramientas explícitamente prohibidas. Debe validar/corregir 10 claims, fijar el modelo estocástico mínimo y entregar acceptance tests analíticos. D4 queda bloqueado hasta `MATH_GO` o incorporación explícita de correcciones.
- **2026-09-24** — Astra/GOD devuelve `MATH_GO`. Claims 1–10 aceptados con condiciones; optional stopping/overshoot/finite-horizon quedan delimitados. Autoridad persistida en `30-resources/futures/echo-futures-astra-math-review.md`. D3 y D3.1 PASS; D4 desbloqueado.
- **2026-09-24** — D4 congelado para ejecución hoy: Functional SPEC + Technical SPEC aprobadas; target aislado `xKoRx/echo-futures` (new repo/local if remote absent); proyecto de agente [[Echo Futures — Simulator v0]] creado con Shots 1 implementación, 2 auditoría independiente y 3 corrección/certificación. No queda diseño abierto para Shot 1.
- **2026-09-24** — Shot 2 independiente PASS_FOR_SHOT_3: cero BLOCKER/MAJOR, dos MINOR (`stubRng` multi-value y NaN con 0 passes) + tres INFO. G4B accepted por owner; Shot 3 desbloqueado. Edge sintético queda explícitamente per-trade.
- **2026-09-24 — Withdrawal KPI correction:** el owner corrige una posible sobrelectura del fixture `q=10%`. No existe todavía evidencia de una tasa real de retiro. La métrica primaria desde D5 es `q_withdraw = retiros reales / evaluations compradas`; `pass` y `funded` son estados intermedios. Cualquier `q≈0.10` de D4 se etiqueta como fixture abstracto de testing.
- **2026-09-24 — D4 CLOSED / G4C accepted:** simulator v0 certificado en `d4f42a41946f12231b75e4eb65b90d132731be0d`; D5 puede usarlo como baseline sin reabrir matemática.

## 🧭 Decisiones

- **2026-09-23 — Echo Futures es una iniciativa raíz bajo [[Echo]], relacionada con [[Trading]], y no un tercer track de [[Echo — Producto Integrado]].**
- **2026-09-23 — Operativa-first:** estrategia, hardscalping, money management y prop economics se definen antes de arquitectura o desarrollo.
- **2026-09-23 — “Quemar cuentas hasta retirar” se modela como hipótesis económica falsable:** el criterio es cash neto y distribución de resultados, no pass rate ni win rate aislados.
- **2026-09-23 — No etiquetar la técnica de Gerard como martingala sin evidencia:** reconstruir trigger, sizing, límites y salida exactos.
- **2026-09-23 — Escala 40–80 cuentas es target de capacidad, no MVP:** el sistema escala por cohortes después de obtener evidencia real de payout.
- **2026-09-23 — Reference/Execution de Echo se conserva como dirección arquitectónica, pero su SPEC queda bloqueada hasta G0/G1.**
- **2026-09-23 — Horizonte máximo inicial = 7 días:** discovery operativo se comprime a 48h mediante tres research one-shot paralelos + entrevista Gerard; el resto del horizonte se dedica a mecanización, backtest/replay, prop simulation y validación adversarial.
- **2026-09-23 — Piloto “~20 cuentas de 10K” es una hipótesis ilustrativa, no una decisión:** cantidad, nominal, prop y presupuesto se dimensionan en D7 desde reglas y economía verificadas.
- **2026-09-24 — Cierre de research amplio:** los DR son insumos, no autoridades. D3 trabaja con dos señales mecanizables y un random control; no se abre otra ronda de búsqueda salvo evidencia concreta que cierre un blocker.
- **2026-09-24 — Diseño experimental secuencial:** entry edge → negative recovery → positive hardscalping → variable risk/prop economics. Prohibido mezclar todo desde el inicio porque impediría atribuir el edge.
- **2026-09-24 — Arquitectura conceptual reemplazable:** señal, gestión intra-trade, política inter-trade y prop lifecycle son componentes independientes; ningún influencer forma parte del contrato.
- **2026-09-24 — Backtest de dos niveles:** queda DEFERRED tras revisión simulation-first; si se ejecuta después, 1m será screening y 1s/tick certification.
- **2026-09-24 — Simulation-first:** antes de datos reales se construye un Monte Carlo completo con Bernoulli ladder como upper-bound, random-walk path como null model canónico, edge sintético 55–65%, hardscalping, prop lifecycle y cohort correlation.
- **2026-09-24 — No asumir independencia por add ni por cuenta:** escaladas dentro del mismo path son condicionales; cuentas copiadas desde la misma Reference están altamente correlacionadas.
- **2026-09-24 — Invariante martingala:** con mercado sin drift y outcomes monetarios terminales fijos +G/-L, el sizing dinámico no cambia la probabilidad total de éxito; `P(win)=L/(G+L)`. El recovery sólo puede aportar edge si existe estructura condicional, cambia la distribución terminal o explota no-linealidades de la prop.
- **2026-09-24 — Tesis matemática principal:** Echo Futures se modela primero como gambler's ruin + absorbing Markov chain + stochastic control sobre reglas de fondeo. La métrica crítica es `purchase→first-withdrawal conversion`, definida como `q_withdraw = P(evaluation comprada → primer retiro real)`. `p_pass`/funded es una métrica intermedia, no el objetivo. Los escenarios con `q=10%` usados en D3/D4 son fixtures matemáticos de validación, NO hipótesis ni benchmark de una prop real. Costes deben separar `p_pass` de `q_withdraw`: activation se pondera por cuentas aprobadas, no sólo por retiros.
- **2026-09-24 — Astra no investiga:** su único rol es falsificar/corregir el contrato matemático antes de implementación; ningún acceso a repos, MCPs, web, logs o infraestructura está autorizado.
- **2026-09-24 — Math authority:** `[[echo-futures-astra-math-review]]` es autoridad del simulator v0 para kernel, optional stopping, lifecycle abstracto, economics y acceptance tests T1–T8.
- **2026-09-24 — D4 scope freeze:** primero certificar null engine exacto; synthetic edge v0 se aplica como perturbación de hitting probability en un adverse state acotado. Edge por múltiples adverse states queda para extensión posterior, no para Shot 1.
- **2026-09-24 — D4 technical freeze:** Go CLI event-driven, exact hitting kernel, standard library first, deterministic single-threaded RNG, JSON scenarios/results, lifecycle abstracto, cohort IID y T1–T8. Repo separado `xKoRx/echo-futures`; Echo/Forge/NinjaTrader fuera de scope.
- **2026-09-24 — Tiering D5 owner:** Tier-1 = Topstep + Take Profit Trader y define el primer vertical slice funcional. Tier-2 = Apex Trader Funding + MyFundedFutures + Tradeify y entra sólo después de certificar el motor/rule contract Tier-1. FTMO Futures queda watchlist por lanzamiento reciente.

## 🔗 Docs / Links

- [[Echo]] — área de producto y automatización.
- [[Trading]] — área relacionada para operativa, prop firms y riesgo.
- [[Echo — Producto Integrado]] — producto vigente; Echo Futures se mantiene independiente para no alterar sus dos tracks congelados.
- [[Echo + Echo Forge — Environment Contract]] — será autoridad de ambiente si Echo Futures reutiliza infraestructura Echo/Aranea; no concede autorización de ejecución.
- [[echo-futures-astra-math-review]] — autoridad matemática del simulator v0 (`MATH_GO`).
- [[D4 — Simulator v0 Functional SPEC]] — contrato funcional congelado D4.
- [[D4 — Simulator v0 Technical SPEC]] — contrato técnico congelado D4.
- [[Echo Futures — Simulator v0]] — proyecto de agente/planificador único para Shots 1–3.
- [[Echo Futures — D5 Prop Economics]] — proyecto de agente para rulesets de props principales y validación `evaluation→withdrawal`.

## 💡 Ideas

%% Captura ideas sueltas del proyecto al final. Si maduran, promover a tarea o a nota de idea (70-templates/idea.md). %%

### Backlog de ideas

- Cohortes de cuentas con perfiles de agresividad distintos para estimar experimentalmente la frontera pass-rate / payout-rate / burn-rate.
- Risk profile dinámico por estado económico de la cuenta en vez de una gestión única.
- Reference única con fan-out a muchas Executions y límites locales por cuenta.
- Simulador Monte Carlo sobre secuencias de trades reales para estimar costo hasta payout y riesgo de cola.
- Clasificar cuentas como inventario económico: evaluation, funded pre-payout, payout-protected, burned, retired.

### Motivos / principios

- **Operativa antes que software.**
- **Cash retirado > balance nominal > win rate.**
- **High win rate no elimina tail risk.**
- **Force brute solo sirve si el EV neto después de quemas es positivo.**
- **KISS:** una prop, un instrumento y una estrategia antes de multiplicar cuentas.
- **YAGNI:** no construir multi-prop, multi-market ni 80-account fan-out antes de demostrar primer payout.
- **Separación SOLID:** signal/strategy, recovery logic, money management, prop rules y execution deben ser medibles y reemplazables por separado.

### Memoria pública / interna

%% Opcional para proyectos de agentes o conocimiento: definir qué memoria gobierna el sistema y cuál gobierna el agente, y por qué existe cada una. %%
- **Memoria pública:** por definir cuando G0/G1 produzcan reglas reutilizables verificadas.
- **Memoria interna:** no requerida para crear el proyecto; continuidad vive en esta nota hasta que exista delta durable específico.
- **Motivo:** evitar convertir hipótesis tempranas en memoria canónica.


## Manager Direction — M0 Algo Execution MVP — 2026-09-25

The owner explicitly ends the research-only phase for the immediate weekend and authorizes implementation of an algorithmic execution MVP.

### Frozen direction

- The existing D4/D5 simulator and certified Topstep P150 economics are retained as research/economics infrastructure; they are NOT rewritten into the execution runtime.
- Weekend goal is a runnable vertical slice, not a production multi-prop platform.
- Real-money deployment is NOT part of M0 acceptance. M0 may run replay, shadow, demo/sim, and provider-authorized simulated accounts.
- Every provider must have explicit current algorithmic-trading permission before its account can be enabled for automated execution.
- Provider rules and execution transport are separate abstractions.
- Backtesting/replay is included as a first-class module by feeding the same strategy/position-management code from recorded market events.
- No frontend is required this weekend.
- No Echo v3 integration is required this weekend; integration follows after the standalone runtime is proven.

### Provider disposition at freeze

- TOPSTEP: PRIMARY. Custom bots are currently allowed through TopstepX/ProjectX API subject to standard/HFT/prohibited-conduct rules; ProjectX API is not available for Live Funded Accounts, so Live is a distinct future venue path.
- LUCID: PRIMARY SECOND PROVIDER. Current help center permits automated strategies/trade copiers and supports NinjaTrader/Tradovate/Rithmic-class platforms; HFT/microscalping restrictions remain.
- MYFUNDEDFUTURES: NEXT. Current official rules permit automated strategies tailored to the trader; HFT/sim-fill exploitation prohibited.
- TRADEIFY: CONDITIONAL ONLY. Personal algorithms are allowed, but current policy requires exclusive ownership/use and says the bot must not be used across other firms. Do not route the shared Echo Futures strategy to Tradeify without an explicit compatible policy decision.
- APEX: EXCLUDED. Current official rules prohibit automation/algorithms on PA/live accounts.
- TAKE PROFIT TRADER: EXCLUDED from automated execution unless a current first-party rule explicitly authorizes autonomous bots; existing project capture classifies it economics-only.

### Weekend acceptance

A successful weekend ends with:
1. one deterministic strategy contract used unchanged by replay and live/shadow runtime;
2. one deterministic position-management contract capable of the future hardscalping/add workflow;
3. account inventory + stage-aware risk/policy state;
4. provider/plan compliance guard;
5. ProjectX/Topstep execution adapter at least through authenticated read/shadow/demo path;
6. a generic NinjaTrader bridge contract suitable for Lucid;
7. append-only event/journal + deterministic replay;
8. kill switch, reconciliation, idempotent order intents, and fail-closed behavior;
9. no real-money order enabled by default.

See [[Echo Futures — M0 Algo Execution MVP]].
