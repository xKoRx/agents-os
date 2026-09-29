# ECHO FUTURES — D4-B1 / Q12
# S2 EXACT MECHANICAL STRATEGY

**Workstream:** D4-B1 / Q12  
**Status:** OWNER-CORRECTED CANDIDATE — READY FOR MANAGER QA  
**Scope:** Strategy only. No MoneyManagement, no provider logic, no implementation, no D4 gate.

**Owner correction D4-B3:** Strategy no posee profit target. Bollinger basis permanece exclusivamente como condición técnica de lifecycle para CLOSE_ALL; el OPEN entrega technical_stop pero no entrega target monetario ni target price a GerardMM.

---

## 1. Executive decision

**Decision: CONFIRM.**

La candidata histórica H4 trend + 5m Bollinger pullback se conserva como S2 V1 porque cumple mejor el objetivo actual que reemplazarla:

- es pequeña y explicable en menos de dos minutos;
- aporta un comportamiento distinto a S1 NY Opening Range Breakout 30m;
- usa únicamente barras e indicadores simples ya soportados por Market Runtime / Strategy Runtime;
- es completamente determinista sobre inputs canónicos ordenados;
- no necesita market firehose, order-flow, ML, DSL, portfolio logic ni nuevas abstracciones;
- permite LONG y SHORT simétricos;
- permite un re-entry mecánico sin depender del estado de ninguna Account;
- cabe en LIVE, EXACT_REPLAY y BACKTEST con la semántica ya congelada/corregida.

La decisión NO afirma que este setup sea una metodología pública de Gerard García ni que sea rentable.

Nombre canónico propuesto:

**S2 — H4 Trend / 5m Bollinger Pullback**

---

## 2. Evidence assessment

### 2.1 SOURCE-SUPPORTED

El research existente de Gerard clasifica explícitamente la candidata H4 trend + pullback LTF / Bollinger como plausible pero UNKNOWN, con confianza baja. No existe evidencia pública suficiente para atribuirle esta entrada a Gerard.

El research de Tradesfera sí respalda a nivel general una familia técnica de reversión a la media con take profits cortos y operativa intradía, pero no identifica públicamente Bollinger, H4 ni parámetros exactos como reglas de Vicente Pons.

El research de El Psicólogo del Trading no entrega una estrategia técnica mecanizable utilizable para reemplazar S2.

Conclusión de evidencia:

- H4 + Bollinger NO es SOURCE-SUPPORTED como estrategia de Gerard.
- Bollinger period, deviation, trend MA, trigger, stop y re-entry NO provienen de una fuente externa.
- La selección de esta S2 es una decisión de diseño de Echo para obtener una Strategy V1 exacta, no una reconstrucción histórica.

### 2.2 ECHO DESIGN DECISION

Todo lo siguiente se congela en este artifact como definición de Echo Futures S2:

- instrumento V1;
- timeframes;
- fórmula de tendencia;
- fórmula de Bollinger;
- touch/recovery;
- trigger por cierre;
- MARKET entry intent;
- stop técnico;
- re-arm;
- defaults;
- warm-up;
- Signal.details.

Estos parámetros se eligen por simplicidad, convencionalidad y utilidad como seed de backtest. No se presentan como óptimos.

### 2.3 UNKNOWN / NOT REQUIRED

No necesitamos resolver para Q12:

- si Gerard usa realmente este setup;
- qué parámetros usaría Gerard;
- si Tradesfera usa Bollinger;
- win rate esperado;
- expectancy;
- mejor instrumento;
- mejor sesión;
- mejores parámetros;
- interacción final con hardscalping;

Esos puntos no impiden implementar y backtestear S2.

---

## 3. S2 en lenguaje simple

S2 opera únicamente NQ.

Cada cierre de vela 5m:

1. determina la tendencia desde H4;
2. si la tendencia es LONG, espera que la vela 5m toque/perfore la banda inferior de Bollinger y cierre nuevamente dentro de la banda, pero todavía bajo la media;
3. si la tendencia es SHORT, hace el espejo sobre la banda superior;
4. cuando ocurre el recovery válido emite un OPEN MARKET en dirección de la tendencia;
5. adjunta únicamente el stop técnico detrás del extremo de la vela gatillo;
6. cuando una 5m cerrada vuelve a la media de Bollinger o la tendencia deja de ser válida, emite CLOSE_ALL para cerrar técnicamente el ciclo; la basis no es un target de profit;
7. sólo después puede abrir un nuevo ciclo en un pullback posterior.

No existe decisión humana.

---

## 4. Instrument scope

V1:

~~~text
instrument_id = NQ
~~~

S2 V1 no generaliza automáticamente a ES, MNQ, MES u otros instrumentos.

La Strategy emite el Instrument canónico NQ. No resuelve Contract físico y no conoce provider/account.

El binding NQ -> Contract físico sigue perteneciendo al runtime ya definido.

Crear posteriormente otra instancia/configuración para otro Instrument no requiere cambiar la lógica S2 ni Strategy Runtime.

---

## 5. Timeframes

Structural:

~~~text
trend_tf = 4h
entry_tf = 5m
~~~

Ambos son bars canónicos del mismo Instrument/Contract efectivo observado por Market Runtime.

MTF usa la semántica D2-06 ya congelada: cada timeframe se agrega directamente desde MarketEvents canónicos; no se deriva 4h desde 5m ni 5m desde 1m.

---

## 6. Required market inputs

S2 es bars-only.

StrategyTriggerRequirements mínimos:

~~~text
bar_close:
  - instrument_id: NQ
    timeframes: [4h, 5m]

market_event: NONE
window_transitions: []
session_transitions: false
timers: []
~~~

No requiere:

- quotes;
- trades individuales;
- DOM;
- order-flow;
- volume profile;
- external indicators;
- provider/account state.

### Trigger purpose

- BAR_CLOSE 4h: actualiza readiness/indicator context; produce 0 Signals.
- BAR_CLOSE 5m: único trigger productivo de entry/re-arm.

S2 no emite Signal intrabar.

---

## 7. Exact H4 trend definition

### 7.1 Indicator

~~~text
trend_ma_type   = SMA
trend_ma_period = 50
trend_price     = CLOSE
~~~

Para cada H4 bar cerrada h:

~~~text
SMA50(h) = arithmetic mean of the CLOSE of h and the previous 49 closed H4 bars
~~~

La pendiente usa el valor inmediatamente anterior:

~~~text
SMA50_prev = SMA50(previous closed H4 bar)
~~~

### 7.2 Trend states

LONG:

~~~text
H4_close > SMA50
AND
SMA50 > SMA50_prev
~~~

SHORT:

~~~text
H4_close < SMA50
AND
SMA50 < SMA50_prev
~~~

En cualquier otro caso:

~~~text
trend = NEUTRAL
~~~

Nunca existen LONG y SHORT simultáneamente.

No existen conceptos fuzzy como strong trend, healthy trend o visual bias.

### 7.3 H4 observation used by a 5m decision

Para una 5m trigger bar m:

~~~text
trend_bar =
  latest CLOSED H4 bar
  whose bucket_close_utc <= m.bucket_open_utc
~~~

Esto impide que la vela H4 que cierra exactamente al mismo tiempo que una vela 5m sea utilizada retroactivamente por esa misma 5m.

Ejemplo:

~~~text
5m bar = 11:55 -> 12:00
eligible H4 trend bar must have closed <= 11:55

5m bar = 12:00 -> 12:05
H4 bar closed at 12:00 is eligible
~~~

La evaluación consume el MarketContext capturado para esa decisión. Si el H4 requerido no está disponible/readiness válido, la salida es no Signal.

---

## 8. Exact 5m Bollinger definition

Structural:

~~~text
bollinger_price = CLOSE
bollinger_period = 20
bollinger_deviation = 2.0
~~~

Para la 5m bar cerrada t, usando las últimas N = 20 closes e incluyendo t:

~~~text
basis(t) = SMA20(close)

population_stddev(t) =
  sqrt(
    sum((close_i - basis(t))^2) / 20
  )

upper(t) = basis(t) + 2.0 * population_stddev(t)
lower(t) = basis(t) - 2.0 * population_stddev(t)
~~~

Se usa desviación estándar poblacional, divisor N, no N-1.

Todos los valores pertenecen a la observation/captured MarketContext de esa evaluación.

---

## 9. Pullback / setup definition

### 9.1 LONG setup

Precondición:

~~~text
trend == LONG
AND
state == ARMED
~~~

La 5m trigger bar t debe cumplir todas:

~~~text
low(t) <= lower(t)
close(t) > lower(t)
close(t) < basis(t)
~~~

Interpretación mecánica:

- el precio tocó/perforó la banda inferior durante la vela;
- al cierre volvió dentro de Bollinger;
- al cierre todavía está bajo la media, por lo que la basis permanece delante como condición técnica futura de cierre del ciclo.

### 9.2 SHORT setup

Precondición:

~~~text
trend == SHORT
AND
state == ARMED
~~~

La 5m trigger bar t debe cumplir todas:

~~~text
high(t) >= upper(t)
close(t) < upper(t)
close(t) > basis(t)
~~~

Interpretación mecánica espejo:

- tocó/perforó la banda superior;
- cerró nuevamente dentro;
- continúa sobre la media.

### 9.3 NEUTRAL trend

~~~text
trend == NEUTRAL
-> no entry Signal
~~~

---

## 10. Entry trigger

La entrada nace únicamente al procesar BAR_CLOSE de la 5m trigger bar válida.

No existe:

- intrabar trigger;
- tick trigger;
- anticipación del close;
- next-bar pattern;
- discretionary confirmation.

Entry intent:

~~~text
order_intent = MARKET
signal_time = BAR_CLOSE evaluation runtime_ts
~~~

Semántica:

> emitir OPEN MARKET inmediatamente después de aceptar mecánicamente el cierre de la trigger bar.

La Strategy no simula fill y no fija execution price.

### Signal validity

Para impedir materialización tardía:

~~~text
valid_until =
  trigger_bar.bucket_close_utc + entry_tf
~~~

En V1 esto equivale a una ventana máxima de una vela 5m.

Si el OPEN llega a Operation después de valid_until, se aplica el guard ya definido y no se materializa.

---

## 11. Technical invalidation / stop reference

El stop es contexto técnico, no sizing monetario.

Para LONG:

~~~text
technical_stop =
  trigger_bar.low - (stop_buffer_ticks * instrument.tick_size)
~~~

Para SHORT:

~~~text
technical_stop =
  trigger_bar.high + (stop_buffer_ticks * instrument.tick_size)
~~~

Default:

~~~text
stop_buffer_ticks = 1
~~~

El precio resultante se normaliza al tick grid del Instrument.

S2 no calcula:

- quantity;
- dollar risk;
- percent risk;
- max loss;
- provider cap;
- account exposure.

---

## 12. Bollinger basis como lifecycle condition — no profit target

S2 no produce profit target ni fixed target price.

La Bollinger basis pertenece exclusivamente a la máquina técnica de Strategy. Durante un ciclo LONG abierto, una 5m cerrada con close >= basis de esa evaluación emite CLOSE_ALL(k). Durante un ciclo SHORT abierto, una 5m cerrada con close <= basis emite CLOSE_ALL(k).

La basis no se congela en el OPEN, no viaja como campo de target y GerardMM no la interpreta como objetivo económico. Los valores Bollinger que permanezcan en Signal.details son provenance del setup técnico; el contrato GerardMM consume entry semantics + technical_stop, no un target de Strategy.

La authority de profit-taking pertenece a GerardMM y es monetaria según D4-B3/Q13.

---

## 13. LONG / SHORT exact rules

### 13.1 LONG

~~~text
ON 5m BAR_CLOSE(t):

require analytical readiness

trend_bar = latest eligible closed H4
trend = H4 trend formula

IF trend != LONG
  -> no LONG Signal

IF state != ARMED
  -> evaluate re-arm only
  -> no LONG Signal

compute Bollinger(t)

IF low(t) <= lower(t)
AND close(t) > lower(t)
AND close(t) < basis(t)
THEN
  emit OPEN LONG MARKET
  technical_stop = low(t) - 1 tick
  state = OPEN_CYCLE_LONG
ELSE
  no Signal
~~~

### 13.2 SHORT

~~~text
ON 5m BAR_CLOSE(t):

require analytical readiness

trend_bar = latest eligible closed H4
trend = H4 trend formula

IF trend != SHORT
  -> no SHORT Signal

IF state != ARMED
  -> evaluate re-arm only
  -> no SHORT Signal

compute Bollinger(t)

IF high(t) >= upper(t)
AND close(t) < upper(t)
AND close(t) > basis(t)
THEN
  emit OPEN SHORT MARKET
  technical_stop = high(t) + 1 tick
  state = OPEN_CYCLE_SHORT
ELSE
  no Signal
~~~

Una evaluación produce como máximo una entry Signal.

---

## 14. Technical cycle close / re-entry semantics

Objetivo: evitar múltiples OPEN consecutivos sobre el mismo pullback y mantener coherencia con el lifecycle técnico congelado por D2-08.

### 14.1 Initial state

Después de warm-up:

~~~text
state = ARMED
~~~

### 14.2 After LONG signal

~~~text
state = OPEN_CYCLE_LONG
~~~

Mientras el ciclo técnico LONG(k) está abierto, S2 no emite otro OPEN.

Cuando una 5m cerrada cumple:

~~~text
close >= basis
~~~

S2 emite:

~~~text
CLOSE_ALL(k)
~~~

y pasa a:

~~~text
state = ARMED
~~~

Ese BAR_CLOSE cierra técnicamente el ciclo k y NO puede simultáneamente emitir OPEN(k+1).

### 14.3 After SHORT signal

~~~text
state = OPEN_CYCLE_SHORT
~~~

Mientras el ciclo técnico SHORT(k) está abierto, S2 no emite otro OPEN.

Cuando una 5m cerrada cumple:

~~~text
close <= basis
~~~

S2 emite:

~~~text
CLOSE_ALL(k)
~~~

y pasa a:

~~~text
state = ARMED
~~~

Ese BAR_CLOSE cierra técnicamente el ciclo k y NO puede simultáneamente emitir OPEN(k+1).

### 14.4 Trend invalidation / flip

Si OPEN_CYCLE_LONG y el trend deja de ser LONG antes de volver a basis:

~~~text
emit CLOSE_ALL(k)
state = ARMED
~~~

Si OPEN_CYCLE_SHORT y el trend deja de ser SHORT antes de volver a basis:

~~~text
emit CLOSE_ALL(k)
state = ARMED
~~~

El cambio de trend no abre automáticamente el ciclo opuesto.

### 14.5 Account convergence

Strategy permanece account-agnostic.

CLOSE_ALL(k) expresa únicamente el cierre técnico del ciclo k. Una AccountStrategy puede haber cerrado antes por GerardMM monetario, protective stop o safety; en ese caso la Signal converge como no-op/fail-visible según el lifecycle existente y nunca crea una nueva Operation.

### 14.6 Maximum entries

No existe límite hardcoded por día/session.

El límite natural es:

> máximo un OPEN por ciclo técnico; el ciclo debe cerrar técnicamente antes de que exista OPEN(k+1).

Agregar max trades/day pertenece a MoneyManagement/provider/risk policy, no a Strategy S2.

---

## 15. Minimal technical state

Estado Strategy-specific mínimo:

~~~text
S2State {
  cycle_state:
    ARMED
    | OPEN_CYCLE_LONG
    | OPEN_CYCLE_SHORT

  trend_indicator_state:
    rolling last 51 closed H4 closes
    latest eligible SMA50
    previous SMA50

  entry_indicator_state:
    rolling last 20 closed 5m closes
}
~~~

Runtime bookkeeping común sigue en Strategy Runtime:

- owner_input_seq;
- strategy_eval_seq;
- strategy_cycle_seq;
- trigger dedup;
- effective config;
- readiness;
- captured context provenance.

No se crea state machine genérica.

No se persiste Account, Provider, Contract execution state ni MoneyManagement state dentro de S2.

---

## 16. Strategy cycle semantics

S2 trata cada OPEN técnico como apertura de un ciclo técnico explícito.

Al emitir OPEN:

~~~text
strategy_cycle_seq = current cycle k
emit OPEN(k)
state = OPEN_CYCLE_LONG | OPEN_CYCLE_SHORT
~~~

El ciclo k permanece técnicamente abierto hasta que S2 emite:

~~~text
CLOSE_ALL(k)
~~~

por retorno a basis o invalidación del trend según §14.

Sólo después de sellar ese cierre técnico el siguiente pullback válido puede abrir:

~~~text
OPEN(k+1)
~~~

S2 no espera que las Accounts terminen físicamente k.

No observa fills ni Position por Account.

Esto preserva el boundary account-agnostic y deja a echo/operation resolver lag físico, pending admission y materialización por ciclo según D2/D4-A3.

S2 V1 emite únicamente OPEN y CLOSE_ALL.

technical_stop viaja como referencia técnica del OPEN. S2 no entrega profit target a MoneyManagement; la basis permanece state/context de Strategy para decidir CLOSE_ALL.

---

## 17. Session filtering

V1:

~~~text
session_filter = NONE
~~~

Razón:

- no es necesario para definir mecánicamente H4 trend + 5m pullback;
- S1 ya ejercita explícitamente opening/session semantics;
- agregar NY/London a S2 introduciría otro parámetro y otra hipótesis sin evidencia material para Q12.

S2 igualmente consume sólo bars válidas construidas por Market Runtime bajo ExchangeCalendar / SessionState. Eventos fuera de sesión no alimentan bars conforme a D2-06.

Una NamedTradingWindow específica puede estudiarse luego como research parameter adicional, pero queda diferida en V1.

---

## 18. Warm-up requirements

Analytical readiness mínima:

~~~text
H4:
  51 closed bars

5m:
  20 closed bars
~~~

Motivo:

- 50 closes para SMA50 actual;
- una H4 adicional para SMA50_prev;
- 20 closes para Bollinger actual.

Hasta que ambas condiciones estén satisfechas:

~~~text
S2 emits 0 Signals
~~~

Warm-up usa el mecanismo MarketHistorySource / normalized MarketEvents ya congelado por D2-06.

No existe warm-up específico de Account.

---

## 19. Late correction semantics

S2 hereda sin modificación la regla D2-06 / D4-A1:

> una decisión basada en una observation X no se reescribe retrospectivamente por una corrección X'.

### Caso trigger bar

~~~text
5m bar X
-> S2 evaluates
-> OPEN emitted

later:
X -> X' late correction
~~~

Resultado:

~~~text
OPEN remains immutable
no retroactive cancel
no second evaluation for X'
~~~

### Caso H4 trend bar

~~~text
H4 bar H
-> later used by a 5m decision

after that decision:
H -> H' late correction
~~~

Resultado:

~~~text
past decision remains immutable
~~~

Una corrección ya incorporada antes de una evaluación futura puede formar parte del MarketContext capturado de esa evaluación futura.

LIVE registra las lecturas/versiones de contexto realmente usadas.

EXACT_REPLAY consume las mismas captured context reads y no consulta un cache latest para reconstruir el pasado.

---

## 20. Signal output contract

Cada setup válido emite exactamente un Signal OPEN.

### 20.1 Canonical Signal fields

~~~text
intent        = OPEN
instrument_id = NQ
direction     = LONG | SHORT
created_at    = evaluation runtime_ts
valid_until   = trigger_bar.bucket_close_utc + 5m
~~~

signal_id, strategy_id, strategy_cycle_seq, strategy_eval_seq, signal_seq, trigger_identity, run_mode/run_id y source usan el contrato común Strategy Runtime.

### 20.2 Signal.details mínimos S2

~~~text
details {
  strategy_spec: "S2_H4_TREND_BB_PULLBACK_V1"

  entry {
    type: MARKET
  }

  trigger {
    timeframe: 5m
    bar_id
    close
  }

  trend {
    timeframe: 4h
    bar_id
    side: LONG | SHORT
    ma_type: SMA
    ma_period: 50
    ma_value
    ma_previous
    h4_close
  }

  bollinger {
    period: 20
    deviation: 2.0
    stddev: POPULATION
    basis
    upper
    lower
  }

  technical_stop
}
~~~

No incluir:

- account_id;
- provider;
- provider program;
- contract execution binding;
- quantity;
- monetary risk;
- leverage;
- recovery step;
- prop limits.

---

## 21. Parameters

### 21.1 Structural parameters

Parte de la identidad semántica de S2 V1:

~~~text
instrument_id = NQ

trend_tf = 4h
entry_tf = 5m

trend_indicator = SMA
trend_price = CLOSE

bollinger_price = CLOSE
bollinger_stddev = POPULATION

trigger_semantics = BAR_CLOSE
entry_intent = MARKET

pullback_semantics =
  touch outer band
  + close back inside
  + close remains between outer band and basis

cycle_close_semantics =
  return to basis
  OR trend invalidation

session_filter = NONE
~~~

Cambiar esos elementos constituye una variante de Strategy, no sólo tuning de parámetros.

### 21.2 Tunable research parameters

Set intencionalmente pequeño:

~~~text
trend_ma_period = 50
bollinger_period = 20
bollinger_deviation = 2.0
stop_buffer_ticks = 1
~~~

Defaults V1:

| Parameter | Default | Motivo |
| --- | ---: | --- |
| trend_ma_period | 50 | seed simple y convencional para suavizar H4 |
| bollinger_period | 20 | convención Bollinger y seed simple |
| bollinger_deviation | 2.0 | convención Bollinger y seed simple |
| stop_buffer_ticks | 1 | separación mínima del extremo técnico |

Estos valores NO son “los mejores”.

Pueden variar en backtest manteniendo la misma semántica S2.

No se agregan parámetros de RSI, ATR, ADX, volumen, VWAP, news, day-of-week ni régimen.

---

## 22. Runtime compatibility

### echo/strategy_engine

Compatible sin cambios.

- una única Strategy island por strategy_id;
- state técnico pequeño;
- evaluación una vez por trigger admitido;
- 0..1 Signal por evaluación para S2.

### MarketContext

Compatible sin cambios.

S2 requiere:

- bars NQ 4h;
- bars NQ 5m;
- readiness;
- captured context version/provenance.

### bars

Compatible con D2-06.

- TRADE bars;
- contract-specific;
- direct aggregation por timeframe;
- late corrections no reevalúan decisiones previas.

### StrategyTriggerRequirements

Compatible sin nueva familia de trigger.

Sólo BAR_CLOSE 4h/5m.

### Signal

Compatible con el Signal canónico.

Los datos Strategy-specific viven en details.

### DomainClock

S2 no usa wall clock.

created_at y valid_until se resuelven sobre runtime/event semantics existentes.

### LIVE

Compatible.

Mismos bars canónicos + state + captured context => misma decisión.

### EXACT_REPLAY

Compatible con D4-A1.

- replaya owner_input_seq/runtime_ts;
- usa captured context reads;
- no consulta latest;
- reproduce la misma decisión y signal identity.

### BACKTEST

Compatible.

Usa mismas barras, fórmula, state, trigger semantics y Signal.

No requiere strategy_backtest paralela.

---

## 23. Determinism contract

Para una S2 config fija:

~~~text
same ordered canonical inputs
+ same captured MarketContext observations
+ same initial S2 state
=
same state transitions
+ same Signal / no-Signal decisions
+ same Signal.details
~~~

No hay:

- randomness;
- current wall clock;
- provider query;
- account query;
- external mutable service;
- discretionary interpretation.

---

## 24. Acceptance examples

### A1 — LONG valid

~~~text
eligible H4:
close > SMA50
SMA50 > SMA50_prev
-> trend LONG

5m:
low <= lower
close > lower
close < basis
state ARMED

=> OPEN LONG MARKET
=> technical_stop = low - 1 tick
=> OPEN_CYCLE_LONG
~~~

### A2 — LONG trend but no pullback

~~~text
trend LONG

5m:
low > lower

=> no Signal
~~~

### A3 — Pullback shape but trend invalid

~~~text
trend NEUTRAL

5m:
low <= lower
close > lower
close < basis

=> no Signal
~~~

### A4 — Touch without recovery

~~~text
trend LONG

5m:
low <= lower
close <= lower

=> no Signal
~~~

### A5 — Recovery overshoots basis

~~~text
trend LONG

5m:
low <= lower
close >= basis

=> no entry Signal
~~~

La vela ya completó el retorno a la media; no se persigue el movimiento.

### A6 — Duplicate pullback while disarmed

~~~text
previous valid LONG emitted
state OPEN_CYCLE_LONG

next 5m:
again touches lower and recovers
but close < basis

=> no Signal
~~~

### A7 — LONG re-arm

~~~text
state OPEN_CYCLE_LONG
trend still LONG

5m closes >= basis

=> state ARMED
=> no Signal on this same bar
~~~

Una pullback posterior puede abrir k+1.

### A8 — SHORT valid

~~~text
eligible H4:
close < SMA50
SMA50 < SMA50_prev
-> trend SHORT

5m:
high >= upper
close < upper
close > basis
state ARMED

=> OPEN SHORT MARKET
=> technical_stop = high + 1 tick
=> OPEN_CYCLE_SHORT
~~~

### A9 — SHORT touch without recovery

~~~text
trend SHORT

5m:
high >= upper
close >= upper

=> no Signal
~~~

### A10 — Late correction after decision

~~~text
valid trigger bar X
=> OPEN LONG emitted

later X becomes X'

=> no retroactive Signal mutation
=> no reevaluation of X
~~~

### A11 — Same canonical inputs

~~~text
same ordered canonical bars
same captured context observations
same config/state

=> same Signal or no-Signal
~~~

### A12 — H4 boundary

~~~text
5m bar 11:55 -> 12:00
H4 bar closes at 12:00

=> that new H4 bar is NOT eligible for this 5m decision
~~~

Next:

~~~text
5m bar 12:00 -> 12:05

=> H4 bar closed at 12:00 is eligible
~~~

### A13 — Warm-up incomplete

~~~text
50 H4 bars only
or
19 5m bars only

=> analytical readiness false
=> no Signal
~~~

---

## 25. KISS / YAGNI sweep

### Kept

- 1 instrument;
- 2 timeframes;
- 1 trend indicator;
- 1 pullback indicator;
- 1 entry trigger;
- symmetric LONG/SHORT;
- 1 tiny re-arm state;
- 4 tunable numeric parameters.

### Explicitly not added

- RSI;
- stochastic;
- ATR filter;
- ADX;
- VWAP;
- volume filter;
- order-flow;
- news filter;
- multi-session matrix;
- day-of-week rules;
- regime engine;
- weighted score;
- DSL;
- ML;
- adaptive parameters;
- optimizer runtime;
- portfolio logic;
- account/provider logic;
- hardscalping;
- trade count cap;
- dynamic target;
- trailing stop.

Todos pueden evaluarse después sólo si evidencia/backtest demuestra que hacen falta.

---

## 26. Evidence vs design decision matrix

| Element | Classification | Note |
| --- | --- | --- |
| H4 + LTF pullback candidate exists in prior corpus | SOURCE-SUPPORTED as prior candidate | Gerard research marks it UNKNOWN, not proven Gerard |
| Bollinger specifically used by Gerard | UNKNOWN | no public support |
| Mean-reversion family exists in Tradesfera research | SOURCE-SUPPORTED at high level | not proof of Bollinger/H4 |
| NQ scope | ECHO DESIGN DECISION | V1 narrow scope |
| H4 / 5m | ECHO DESIGN DECISION | preserves historical candidate |
| SMA50 trend | ECHO DESIGN DECISION | deterministic/simple |
| Bollinger 20 / 2 population stddev | ECHO DESIGN DECISION | deterministic seed |
| outer-band touch + close-inside recovery | ECHO DESIGN DECISION | exact pullback semantics |
| close must remain before basis | ECHO DESIGN DECISION | prevents chasing completed reversion |
| MARKET on 5m close | ECHO DESIGN DECISION | exact non-intrabar trigger |
| stop beyond trigger extreme | ECHO DESIGN DECISION | technical invalidation |
| basis closes technical cycle | ECHO DESIGN DECISION + Owner boundary | lifecycle condition only; not MM profit target |
| one entry per excursion / basis re-arm | ECHO DESIGN DECISION | prevents repeated spam |
| no session filter | ECHO DESIGN DECISION | YAGNI for V1 |
| profitability / optimality | UNKNOWN / NOT REQUIRED | validation later |

---

## 27. Owner decisions required

NONE for Q12.

D4-B3 ya resolvió la frontera que antes estaba abierta: Strategy no posee profit target. S2 conserva technical_stop; Bollinger basis sólo gobierna lifecycle técnico y CLOSE_ALL. GerardMM posee el objetivo monetario y su ejecución.

No architecture change is required.

---

## 28. Implementation handoff summary

An implementer can decide every 5m BAR_CLOSE with the following closed sequence:

~~~text
1. readiness?
   no -> no Signal

2. obtain eligible H4 trend bar
   missing -> no Signal

3. calculate exact H4 trend
   neutral -> handle re-arm if needed, no entry

4. calculate exact 5m Bollinger

5. if disarmed
   evaluate exact re-arm rule
   never emit entry on the re-arm bar

6. if armed
   apply exact LONG or SHORT touch + recovery rule

7. if valid
   emit one OPEN MARKET Signal
   attach frozen technical stop; no profit target
   set disarmed side

8. otherwise
   no Signal
~~~

No discretionary branch remains.

```text
Q12_S2_DECISION: CONFIRM

S2_NAME:
H4 Trend / 5m Bollinger Pullback

S2_MECHANICAL_SPEC: COMPLETE

OWNER_DECISIONS_REQUIRED:
NONE

NEW_ARCHITECTURE_REQUIRED:
NO

DEFERRED_YAGNI:
session filter; additional instruments; extra indicators; adaptive parameters; optimization; Strategy-side trailing/dynamic exits

READY_FOR_MANAGER_QA:
YES
```