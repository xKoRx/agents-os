# ECHO FUTURES — D4-B3
# S1 EXACT MECHANICAL STRATEGY

**Status:** OWNER-CORRECTED CANDIDATE — READY FOR MANAGER QA
**Scope:** Strategy only. No MoneyManagement, no provider logic, no implementation, no D4 gate.

## 1. Executive decision

S1 queda congelada como NY Opening Range Breakout 30m sobre NQ, con opening range 09:30–10:00 ET heredado de D2-05 y breakout intrabar por canonical TRADE. Strategy no posee profit target. El OPEN entrega direction, MARKET entry intent y technical_stop/reference. GerardMM posee sizing, monetary SL/TP y hardscalping.

La corrección Owner sobre protección S1 es literal: para LONG, technical_stop es el LOW acumulado desde el inicio autoritativo de premarket hasta la vela 5m cerrada inmediatamente anterior al evento de decisión; para SHORT es el HIGH acumulado en la misma ventana. La vela 5m que todavía está formando queda excluida. El valor se congela en el OPEN; no es trailing.

La hora concreta de inicio de premarket no se inventa en esta SPEC. Es configuración obligatoria mediante un NamedTradingWindow resoluble. Sin esa authority S1 falla cerrado y no emite OPEN.

## 2. Instrument y timeframes

~~~text
instrument_id = NQ
bar_tf = 5m
opening_range_window_id = NY_OPEN
premarket_window_id = REQUIRED_CONFIG
~~~

NY_OPEN conserva la authority D2-05: CLOCK 09:30–10:00 ET intersectada con ExchangeSession del NQ. S1 no hardcodea offsets UTC y usa timezone IANA mediante WindowContext.

premarket_window_id debe resolver exactamente un window_open_utc para el mismo window_date de NY_OPEN, debe abrir antes de NY_OPEN.window_open_utc y debe estar alineado al grid canónico 5m. Su hora es dato/configuración, no lógica de Strategy.

## 3. Trigger requirements

~~~text
StrategyTriggerRequirements {
  bar_close:
    - { instrument_id: NQ, timeframes: [5m] }

  market_event: TRADE

  window_transitions:
    - premarket_window_id
    - NY_OPEN

  session_transitions: false
  timers: []
}
~~~

BAR_CLOSE alimenta opening range, extrema cerrada, technical lifecycle y re-arm. MARKET_EVENT TRADE es el único trigger de breakout y preserva la semántica heredada de ruptura sin esperar cierre de vela.

No se usa QUOTE para declarar breakout. El precio de trigger es un trade canónico ejecutado; GerardMM resuelve su propio executable-side BBO para sizing/egress.

## 4. Session / premarket start authority

Para cada window_date d:

~~~text
premarket_start_utc(d) =
  WindowContext(premarket_window_id, d).window_open_utc

opening_range_open_utc(d) =
  WindowContext(NY_OPEN, d).window_open_utc

opening_range_close_utc(d) =
  WindowContext(NY_OPEN, d).window_close_utc
~~~

Validación obligatoria:

~~~text
premarket_start_utc < opening_range_open_utc
opening_range_close_utc - opening_range_open_utc = 30m
all boundaries resolve under IANA/calendar authority
premarket_start_utc aligned to canonical 5m grid
exchange availability valid for consumed bars
~~~

Si falta cualquiera de esas condiciones, S1 marca S1_SESSION_CONTEXT_UNRESOLVED para ese window_date y no abre riesgo.

## 5. Opening range exacta

S1 construye la opening range únicamente desde las seis barras canónicas 5m completamente contenidas en NY_OPEN:

~~~text
OR_BARS(d) = {
  b |
  b.timeframe = 5m
  AND b.bucket_open_utc >= opening_range_open_utc(d)
  AND b.bucket_close_utc <= opening_range_close_utc(d)
}

require count(OR_BARS) = 6

opening_range_high = max(b.high for b in OR_BARS)
opening_range_low  = min(b.low  for b in OR_BARS)
opening_range_last_close = close(last b in OR_BARS)
~~~

La range se congela al procesar el cierre de NY_OPEN sólo si las seis barras cerradas y sus versiones son demostrables. No synthetic empty bars. Gap o bar faltante implica S1_OPENING_RANGE_UNPROVABLE y cero OPEN para ese window_date.

Una late correction posterior no reescribe retroactivamente la range observada por la decisión. D4-A1 gobierna exact versions/context_reads para replay.

## 6. High/low acumulado Owner-provided

Para un evento de decisión en instante t del mismo window_date:

~~~text
previous_closed_bar(t) =
  latest canonical 5m bar b
  such that b.bucket_close_utc <= t

CLOSED_CONTEXT_BARS(t) = {
  b |
  b.timeframe = 5m
  AND b.bucket_open_utc >= premarket_start_utc
  AND b.bucket_close_utc <= previous_closed_bar(t).bucket_close_utc
}
~~~

Sólo se admiten barras cerradas con cobertura demostrable bajo ExchangeCalendar. La barra cuyo bucket contiene t no pertenece a CLOSED_CONTEXT_BARS(t).

~~~text
observed_low_to_previous_close(t) =
  min(b.low for b in CLOSED_CONTEXT_BARS(t))

observed_high_to_previous_close(t) =
  max(b.high for b in CLOSED_CONTEXT_BARS(t))
~~~

LONG:

~~~text
technical_stop =
  observed_low_to_previous_close(t)
~~~

SHORT:

~~~text
technical_stop =
  observed_high_to_previous_close(t)
~~~

El technical_stop se valida contra tick_size y debe quedar estrictamente del lado adverso del breakout trade; de lo contrario no hay OPEN y se registra S1_TECHNICAL_STOP_INVALID.

El extremo usado queda congelado dentro de la Signal emitida. S1 no lo actualiza después del OPEN y no implementa trailing técnico.

## 7. Exact breakout trigger

Al cerrar NY_OPEN, si la range es válida:

~~~text
state = ARMED
last_trade_price = opening_range_last_close
~~~

Para cada canonical TRADE e posterior, mientras state = ARMED y e pertenece al mismo window_date con exchange OPEN:

LONG breakout:

~~~text
last_trade_price <= opening_range_high
AND e.price > opening_range_high
~~~

SHORT breakout:

~~~text
last_trade_price >= opening_range_low
AND e.price < opening_range_low
~~~

Después de procesar cada TRADE se actualiza last_trade_price = e.price.

Una equality con el boundary no es breakout. Debe existir cruce estricto.

## 8. BAR_CLOSE vs intrabar semantics

Opening range y technical reference consumen sólo 5m BAR_CLOSE.

La entrada es intrabar y se decide sobre canonical TRADE después de que NY_OPEN ya quedó congelada.

La forming 5m bar nunca participa en technical_stop. Un trade a 10:03 ET usa como previous_closed_bar la 5m terminada a 10:00 ET. Un trade a 10:07 ET usa la 5m terminada a 10:05 ET.

No existe confirmación al cierre, next-bar entry ni interpretación discrecional.

## 9. LONG exact rule

~~~text
ON canonical TRADE e:

require state == ARMED
require opening range frozen and valid
require exchange OPEN
require same window_date
require last_trade_price <= opening_range_high
require e.price > opening_range_high

previous = previous_closed_bar(e.event_ts)
require closed-context coverage from premarket_start through previous

stop = observed_low_to_previous_close(e.event_ts)
require stop < e.price

emit OPEN(k) {
  direction = LONG
  entry.type = MARKET
  technical_stop = stop
}

state = OPEN_CYCLE_LONG
cycle_technical_stop = stop
last_trade_price = e.price
~~~

## 10. SHORT exact rule

~~~text
ON canonical TRADE e:

require state == ARMED
require opening range frozen and valid
require exchange OPEN
require same window_date
require last_trade_price >= opening_range_low
require e.price < opening_range_low

previous = previous_closed_bar(e.event_ts)
require closed-context coverage from premarket_start through previous

stop = observed_high_to_previous_close(e.event_ts)
require stop > e.price

emit OPEN(k) {
  direction = SHORT
  entry.type = MARKET
  technical_stop = stop
}

state = OPEN_CYCLE_SHORT
cycle_technical_stop = stop
last_trade_price = e.price
~~~

## 11. Signal validity

El breakout es intrabar y no debe materializarse tarde.

~~~text
valid_until =
  next canonical 5m bucket close strictly after trigger event_ts
~~~

Si la OPEN llega a echo/operation después de valid_until, el guard existente la descarta. Strategy no simula fill ni fija execution price.

## 12. Strategy does not own profit target

S1 no calcula ni entrega monetary TP, desired USD profit, fixed target price ni technical profit target.

~~~text
Strategy OPEN
  -> direction
  -> MARKET intent
  -> technical_stop/reference

Strategy OPEN
  -X-> profit target
  -X-> desired USD profit
~~~

GerardMM posee la economía de profit/loss. Provider sigue poseyendo sus hard constraints.

## 13. Technical lifecycle OPEN / CLOSE / CLOSE_ALL

S1 V1 emite OPEN y CLOSE_ALL. No emite CLOSE parcial.

OPEN(k) ocurre sólo por §9/§10 y abre un único technical cycle.

Mientras OPEN_CYCLE_LONG:

~~~text
canonical TRADE.price <= cycle_technical_stop
-> emit CLOSE_ALL(k)
-> state = WAIT_REARM
~~~

Mientras OPEN_CYCLE_SHORT:

~~~text
canonical TRADE.price >= cycle_technical_stop
-> emit CLOSE_ALL(k)
-> state = WAIT_REARM
~~~

Este CLOSE_ALL expresa lifecycle técnico. GerardMM puede haber cerrado físicamente antes; entonces la delivery converge por los guards existentes y no crea otra Operation.

Mientras OPEN_CYCLE_LONG o OPEN_CYCLE_SHORT, una 5m cerrada con:

~~~text
opening_range_low <= close <= opening_range_high
~~~

emite CLOSE_ALL(k) y deja state = ARMED al final de esa evaluación. Ese mismo BAR_CLOSE nunca puede emitir un nuevo OPEN porque S1 abre únicamente por TRADE posterior.

Al abrir premarket_window_id de una nueva window_date, si existe un technical cycle anterior todavía abierto S1 emite CLOSE_ALL(k) antes de resetear su estado diario. Luego comienza COLLECTING_PREMARKET para la fecha nueva.

## 14. Re-entry

WAIT_REARM vuelve a ARMED sólo cuando una 5m cerrada del mismo window_date termina dentro de la opening range congelada:

~~~text
opening_range_low <= close <= opening_range_high
~~~

No hay OPEN en el BAR_CLOSE que re-arma. El siguiente canonical TRADE debe cruzar nuevamente un boundary desde el lado válido según §7.

Si un ciclo cerró por return-to-range, queda ARMED al finalizar ese BAR_CLOSE y el siguiente TRADE puede constituir una nueva ruptura.

No existe max trades/day hardcoded en Strategy. Provider/GerardMM pueden impedir materialización por sus propias authorities.

## 15. Minimal S1 state

~~~text
S1State {
  window_date

  phase:
    WAIT_PREMARKET
    | COLLECTING_PREMARKET
    | COLLECTING_OPENING_RANGE
    | ARMED
    | OPEN_CYCLE_LONG
    | OPEN_CYCLE_SHORT
    | WAIT_REARM
    | INVALID_DAY

  opening_range_high?
  opening_range_low?
  opening_range_last_close?

  observed_low_to_last_closed?
  observed_high_to_last_closed?
  last_closed_5m_bar_id?

  last_trade_price?
  cycle_technical_stop?
}
~~~

Runtime bookkeeping común permanece en Strategy Runtime: owner_input_seq, strategy_eval_seq, strategy_cycle_seq, trigger dedup, config efectiva, readiness y D4-A1 captured context provenance.

No existe estado de Account, Provider, GerardMM, Orders, Fills o Position dentro de S1.

## 16. Warm-up / readiness

Antes del freeze de opening range, S1 requiere poder demostrar la secuencia canónica de 5m bars desde premarket_start hasta 10:00 ET y las seis barras NY_OPEN.

Un restart puede reconstruir ese state desde canonical market history/warm-up ya permitido por Market Runtime. Si no puede probar cobertura exacta, INVALID_DAY para nuevas aperturas; no se rellena historia con synthetic bars.

Readiness de breakout exige además canonical TRADE current y ExchangeSession OPEN.

La introducción de S1 no degrada readiness global de la stream; es analytical readiness de este consumer.

## 17. Signal.details

OPEN S1 mínimo:

~~~text
details {
  strategy_spec: "S1_NY_ORB_30M_V1"

  entry {
    type: MARKET
  }

  trigger {
    kind: TRADE_BREAKOUT
    canonical_event_id
    stream_seq
    event_ts
    price
  }

  opening_range {
    window_id: NY_OPEN
    window_date
    open_utc
    close_utc
    high
    low
  }

  technical_reference {
    kind: PREMARKET_EXTREME_THROUGH_PREVIOUS_CLOSED_5M
    premarket_window_id
    premarket_start_utc
    previous_closed_bar_id
    observed_low
    observed_high
  }

  technical_stop
}
~~~

No incluir account_id, provider, quantity, monetary loss budget, profit objective, monetary TP, recovery step ni provider caps.

## 18. LIVE / EXACT_REPLAY / BACKTEST

LIVE procesa WindowTransitions/BAR_CLOSE/TRADE en echo/strategy_engine con ownership strategy_id. El opening range freeze, closed-context extrema, breakout crossing y lifecycle state son deterministas sobre el stream admitido.

EXACT_REPLAY reproduce los mismos ordered inputs y D4-A1 decision-scoped ContextReads. La TRADE trigger usa canonical_event_id + stream_seq; los bars/ranges observados usan sus exact versions. Late corrections no reescriben Signals históricas.

BACKTEST usa los mismos NamedTradingWindow/Calendar snapshots, canonical 5m bars, TRADE stream sintético/canónico y la misma lógica S1. No existe s1_live versus s1_backtest.

## 19. Acceptance cases

- AC-S1-01: seis 5m bars 09:30–10:00 válidas congelan opening_range_high/low y dejan ARMED.
- AC-S1-02: cinco bars o una bar no demostrable dejan INVALID_DAY y cero OPEN.
- AC-S1-03: trade exactamente en opening_range_high/low no rompe; crossing estricto sí.
- AC-S1-04: LONG breakout usa LOW acumulado desde premarket_start hasta previous_closed_bar como technical_stop.
- AC-S1-05: SHORT breakout usa HIGH acumulado desde premarket_start hasta previous_closed_bar como technical_stop.
- AC-S1-06: la 5m forming que contiene el breakout no participa del technical_stop.
- AC-S1-07: LONG trade breakout emite exactamente un OPEN LONG MARKET y state OPEN_CYCLE_LONG.
- AC-S1-08: SHORT trade breakout emite exactamente un OPEN SHORT MARKET y state OPEN_CYCLE_SHORT.
- AC-S1-09: segundo trade fuera del mismo boundary mientras cycle abierto no emite otro OPEN.
- AC-S1-10: trade cruza cycle_technical_stop y emite CLOSE_ALL, nunca CLOSE parcial.
- AC-S1-11: 5m close dentro de opening range cierra/re-arma técnicamente; no abre en ese mismo BAR_CLOSE.
- AC-S1-12: WAIT_REARM sólo vuelve a ARMED por 5m closed dentro de range.
- AC-S1-13: nueva window_date resetea extrema/range y cierra técnicamente un ciclo anterior si seguía abierto.
- AC-S1-14: premarket_window_id ausente/unresolvable produce fail-closed, no hora inventada.
- AC-S1-15: Signal.details no contiene profit target ni desired USD profit.
- AC-S1-16: misma secuencia ordenada + misma config + mismas versions/context_reads produce mismas Signals en LIVE/EXACT_REPLAY.
- AC-S1-17: BACKTEST usa la misma lógica sin branch específico.
- AC-S1-18: late correction después de OPEN no muta Signal ni technical_stop ya observado.

## 20. KISS / YAGNI

Se mantienen un Instrument, una bar TF 5m, dos NamedTradingWindow authorities, una opening range congelada, extrema cerrada acumulada, un trigger TRADE y una state machine pequeña.

No se agregan profit target Strategy-side, trailing technical stop, VWAP, ATR, order-flow, DOM, ML, optimizer, discretionary confirmation, portfolio state, provider branches ni strategy-specific MoneyManagement.

## 21. Owner decisions

La decisión Owner queda integrada sin reinterpretación: Strategy no posee profit target y S1 usa premarket-start → previous closed candle extrema como technical protection reference.

No se requiere nueva decisión Owner para la SPEC. El valor horario concreto de premarket_start es configuración obligatoria y no se convierte en constante inventada.

~~~text
S1_EXACT_SPEC: COMPLETE
STRATEGY_OWNS_PROFIT_TARGET: NO
OWNER_DECISIONS_REQUIRED: NONE
NEW_ARCHITECTURE_REQUIRED: NO
READY_FOR_MANAGER_QA: YES
~~~