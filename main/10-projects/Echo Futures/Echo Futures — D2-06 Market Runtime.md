---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo Futures]]"
  - "[[Echo Futures — D2-04 Operation Order Fill Position]]"
  - "[[Echo Futures — D2-05 Instrument Session Provider]]"
  - "[[Echo Futures — D2-06A Market Feed Authority]]"
  - "[[Echo Futures — D2-06B Bars Hot State Warmup]]"
  - "[[Echo Futures — D2-06C Live Replay Market Boundary]]"
aliases:
  - Echo Futures D2-06
  - EF Market Runtime
tags:
  - kind/doc
  - area/echo
  - echo-futures
  - architecture-design
created: "2026-09-27"
updated: "2026-09-27"
---

# Echo Futures — D2-06 Market Runtime

## Propósito

Ser la autoridad única de lectura para D2-06 Market Runtime, integrando sin reabrir los contratos aceptados de [[Echo Futures — D2-06A Market Feed Authority]], [[Echo Futures — D2-06B Bars Hot State Warmup]] y [[Echo Futures — D2-06C Live Replay Market Boundary]].

Responde de forma conjunta Q4 Market Hot State, Q5 Bar Semantics, Q8 Feed Authority y Q14 LIVE/REPLAY Market Boundary. Consume los contratos ya congelados de [[Echo Futures — D2-04 Operation Order Fill Position]] y [[Echo Futures — D2-05 Instrument Session Provider]]. No selecciona D2-07 transport, no implementa código y no cierra D2 global.

## Contenido

D2-06 integra una sola semántica vigente: stream lógica por Instrument+Contract, authority separada del source, market state compartido sin keys por Account, barras contract-specific, readiness feed vs analytical en capas, decision observations inmutables ante late corrections, y boundary determinista basado en manifest inicial + replay anchor + journal ordenado + contenido canónico.

Los child artifacts A/B/C permanecen como evidencia y profundidad de diseño. Ante contradicción de wording histórico, este artifact integrado es la autoridad vigente de D2-06.

## 1. Executive verdict

D2-06 STATUS: READY_FOR_MANAGER_REVIEW.

Los tres children están ACCEPTED_FOR_INTEGRATION y sus repairs críticos son compatibles. No apareció una cuarta decisión arquitectónica ni evidencia nueva que obligue a reabrirlos. La integración resuelve los dos seams explícitos pendientes:

- feed/stream readiness pertenece a A; warm-up y analytical readiness pertenecen a B;
- el snapshot inicial del RunManifest es inmutable; cambios hot materiales posteriores existen como ConfigTransition ordenadas en el DeterministicInputLog y nunca reescriben las condiciones iniciales.

Los gates padres A–L quedan PASS por mecanismos explícitos, no por narrativa. La única decisión owner abierta es OD-C1: recording de EXACT LIVE REPLAY always-on V1 versus opt-in por run. Esa elección no cambia la arquitectura ni la corrección del boundary, por lo que no bloquea manager review.

Baseline físico congelado y re-verificado para esta integración:

- xKoRx/echo origin/master = 372af59a7b83604781346613da01e3d510ea1360.
- Sin delta respecto de A/B/C; por regla de integración no se repitió auditoría física general.

## 2. Scope / authorities

Autoridades directas, en orden:

1. [[Echo Futures]] — decisiones owner y estado del proyecto.
2. [[Echo Futures — D2-04 Operation Order Fill Position]] — Operation/Order/Fill/Position, MM state y recovery authority de ejecución.
3. [[Echo Futures — D2-05 Instrument Session Provider]] — Instrument/Contract, rollover, ExchangeCalendar/Session, Provider overlays y DayBoundary.
4. [[Echo Futures — D2-06A Market Feed Authority]] — stream/feed authority, normalization, identity, health y recovery.
5. [[Echo Futures — D2-06B Bars Hot State Warmup]] — hot analytical state, bars, MTF, indicators, warm-up y consumer readiness.
6. [[Echo Futures — D2-06C Live Replay Market Boundary]] — ordering, DomainClock, deterministic recording y EXACT_REPLAY.

En scope: Market Runtime V1 completo desde feed candidate hasta Signal/MM market context, incluido recovery, warm-up, bars, ordering y recording boundary.

Fuera de scope: execution transport D2-07, full backtester product, provider selection, vendor selection, implementación, sprint sizing, execution event sourcing y global D2 closure.

## 3. Integrated invariants

I1. stream_id = (instrument_id, contract_id). Binding/source no forma parte de la identidad lógica.

I2. serving_authority = binding_id + members + authority_epoch + provenance. Source switch modifica authority, no Contract.

I3. Rollover y source switch son transiciones distintas. Source switch jamás implica auto-roll.

I4. Operation pinnea instrument_id + contract_id; jamás pinnea source/binding de mercado.

I5. echo.market-events.v1 es AT_LEAST_ONCE. Todo mutador downstream aplica stream_seq guard antes de estado, volumen, trade_count o evaluación.

I6. No existe content-dedup sintético. Event identity es capability-driven A/B/C; clase C no inventa identidad.

I7. current market state es monotónico por (event_ts, stream_seq) sólo dentro del mismo authority_epoch. stream_seq no se reinicia entre epochs.

I8. Epoch change demotea current previo a last-known con provenance y stale; el current del nuevo epoch nace vacío y se seed-ea con el primer dato válido.

I9. Availability no equivale a READY. Last-known puede estar disponible con stream NOT_READY.

I10. One market state, many read-only consumers. Account nunca es key de feed, bars o Strategy analytical state.

I11. BarId = (stream_id, timeframe, bucket_open_utc). Cero mixing entre Contracts y cero continuous/back-adjusted V1.

I12. BAR_CLOSE decision observation es inmutable. Una corrección X→X' cambia la market projection, nunca la decisión que observó X y nunca emite Signal retrospectiva.

I13. event_ts, stream_seq, owner_input_seq y runtime_ts tienen responsabilidades distintas y no se colapsan.

I14. DomainClock.Now() usa runtime_ts monotónico; jamás event_ts de un late event.

I15. Todo TimerFired admitido por dominio se journaliza; timer identity = timer_id + generation.

I16. EXACT_REPLAY requiere initial manifest + immutable ReplayAnchor + ordered DeterministicInputLog + contenido canónico recuperable + mismo código.

I17. BAR_CLOSED/BAR_UPDATED no son autoridad grabada; se re-derivan desde market/control inputs + TimerFired + config/calendar transitions.

I18. NORMAL RESTART usa checkpoint. EXACT_REPLAY no sustituye recovery live. COLD execution recovery permanece D2-04 fail-closed.

I19. Sin total order global. El orden material es per-island owner_input_seq; Strategy multi-stream journala el merge que observó.

I20. 200 Accounts usando la misma Strategy no crean 200 feeds, builders, indicators ni evaluaciones; fan-out ocurre después de Strategy evaluation.

## 4. Instrument / Contract / authority model

Instrument es identidad económica. Contract es tradable expiry-specific y forma parte de la stream.

~~~text
stream_id = (instrument_id, contract_id)

serving_authority {
  binding_id
  members[]
  authority_epoch
  provenance
}
~~~

Source switch:

1. conserva stream_id;
2. conserva contract_id;
3. valida que la autoridad entrante pueda servir todos los Contracts demandados;
4. incrementa authority_epoch;
5. cierra readiness;
6. emite barrier;
7. invalida current/forming state afectado;
8. rebuild capability-driven;
9. reabre feed readiness cuando la evidencia de feed lo permite.

Si la nueva authority no puede servir un Contract demandado, el switch no aplica. No se re-resuelve silenciosamente otro Contract.

Rollover:

1. es acción owner explícita de D2-05;
2. cambia el Contract in-force prospectivo de Strategy;
3. crea/demanda otra logical stream;
4. mantiene viva la stream vieja mientras una Operation pinneada la demande;
5. nunca altera el Contract de una Operation existente.

## 5. Market demand / subscription

Operation declara necesidad económica, no source:

~~~text
MarketDemand {
  operation_id
  instrument_id
  contract_id
  intent: ACQUIRE | RELEASE
}
~~~

ACQUIRE ocurre cuando una Operation necesita market context del Contract pinneado. RELEASE ocurre al terminar esa necesidad. Idempotencia por membresía (operation_id, contract_id), no reference-counting framework.

Demand efectiva:

~~~text
demand(stream) =
  config_demand
  UNION
  operation_demand
~~~

Market Runtime resuelve la demanda contra la MARKET_DATA authority activa del Instrument y sus ContractIdentifiers/capabilities.

Consecuencias:

- la misma Operation puede migrar de source durante un switch sin cambiar Contract;
- rollover puede dejar simultáneamente H7 in-force para Strategy y Z6 RETIRING para una Operation vieja;
- unsubscribe sólo cuando demand = vacío;
- Account count es invisible al subscription engine.

## 6. MarketEvent / identities / idempotency

MarketEvent V1 tiene dos tipos: QUOTE/BBO y TRADE.

Campos semánticos mínimos:

~~~text
MarketEvent {
  stream_id
  instrument_id
  contract_id
  event_type: QUOTE | TRADE
  event_ts
  receive_ts
  source_event_position?
  stream_seq
  authority_epoch
  origin {
    source_id
    recovery_provenance: LIVE | RECOVERY_REPLAY | SNAPSHOT
  }
  payload
}
~~~

Semánticas:

- event_ts: autoridad temporal técnica del evento; barras/session assignment.
- receive_ts: telemetry/liveness; nunca semántica de mercado.
- stream_seq: orden/idempotencia canónica per logical stream; cruza epochs y no se resetea.
- authority_epoch: serving/recovery epoch.
- origin/source position: provenance y exact identity cuando capability lo soporta.

Tres clases de identidad:

- A EVENT: identidad de evento estable; dedup exacto.
- B POSITIONAL: packet/message sequence + posición determinística; un packet con N entries produce N MarketEvents.
- C NONE: sin dedup-safe identity; content hash/tuple prohibido.

Clase C sólo recupera de forma exacta mediante boundary/cursor no solapado, snapshot replacement cuando alcance, full rebuild autoritativo, o queda fail-visible NOT_READY/ANALYTICAL_REBUILD_UNPROVABLE.

echo.market-events.v1 es AT_LEAST_ONCE. Downstream conserva last_applied_stream_seq y todo redelivery con seq ≤ guard es NO-OP antes de mutar estado o disparar evaluación.

## 7. Health / recovery / readiness

Health mantiene tres dimensiones separadas:

- LIVENESS por member físico.
- CONTINUITY por stream y primitivas demostrables del source.
- FRESHNESS por stream, con threshold técnico source/instrument y sólo cuando el calendario permite evaluar frescura.

ExchangeCalendar CLOSED o BREAK hace el silencio esperado; cero ticks por tiempo de pared no es failure universal.

Recovery:

~~~text
READY
→ disruption/gap
→ RECOVERING + barrier
→ recovery capability-driven
→ RecoveryBarrier/epoch marker
→ rebuild downstream
→ feed readiness según evidencia
→ consumer readiness según requirements
~~~

Equivalent members con identidad compartida demostrada pueden hacer failover intra-authority sin doble evaluación y, si continuidad queda demostrada, sin barrier.

Heterogeneous backup exige source switch explícito, sin blend y con readiness loss.

Readiness layering congelado:

~~~text
EffectiveConsumerReadiness(c) =
  StreamReadinessFor(c.required_input_class)
  AND
  AnalyticalRequirementsReady(c)
~~~

Feed/stream reasons pertenecen a A:

- NO_LIVE_MEMBER
- GAP_UNRESOLVED
- RECOVERY_UNPROVABLE
- STALE_BEYOND_POLICY
- SWITCHING_AUTHORITY
- CONTRACT_NOT_SERVABLE
- CONFIG_NOT_READY

WARMUP_INCOMPLETE no es feed-level reason. Es estado analítico del consumidor. ANALYTICAL_REBUILD_UNPROVABLE también pertenece al gate analytical/history-dependent.

Una Strategy BBO-only puede quedar lista antes que otra que necesita 200×1m + 50×5m. Una Strategy nueva nunca baja globalmente la stream.

## 8. Current vs last-known state

Current-state certificado pertenece al authority_epoch vigente.

Dentro del mismo epoch, last_quote y last_trade son escaleras independientes monotónicas por (event_ts, stream_seq). Un evento tardío legítimo puede corregir barras y demostrar liveness sin hacer retroceder el current price.

En epoch change:

~~~text
current(epoch E)
→ last_known_previous {
    epoch: E
    quote/trade
    as_of
    stale
    provenance
  }

current(epoch E+1)
→ EMPTY
→ seed con primer snapshot/evento válido del nuevo epoch
→ monotonía intra-epoch
~~~

No se compara event_ts de la autoridad nueva contra el último timestamp de la autoridad anterior.

stream_seq y last_applied_stream_seq continúan monotónicos a través de epochs.

MarketContext distingue obligatoriamente:

- current state del epoch vigente;
- last-known del epoch previo;
- readiness/quality;
- as_of/stale.

Last-known disponible jamás convierte el stream en READY. MM puede usarlo sólo cuando su policy para esa acción lo autoriza explícitamente.

## 9. Hot state ownership

Shared market state:

- latest quote/trade;
- forming bars;
- bounded recent closed bars;
- session/grid context;
- quality/readiness/provenance.

Ownership físico:

| Estado | Owner | Key |
| --- | --- | --- |
| latest quote/trade + serving authority | echo/market_stream | stream_id |
| forming/closed bars + grid/rebuild segment | echo/market_analytics | stream_id |
| Strategy indicators + finite state + analytical readiness | echo/strategy_engine | strategy_id |
| MM mutable state | echo/operation | account_id:account_strategy_id |

No Account-keyed market analytics. No global indicator service. No mutable state compartido entre MM instances.

## 10. Bar semantics

BarId:

~~~text
(stream_id, timeframe, bucket_open_utc)
~~~

V1 bars son TRADE bars.

Grid:

- anclado a session_open durante toda ExchangeSession;
- Account DayBoundary no participa;
- una nueva ExchangeSession crea grid nuevo;
- internal BREAK no reinicia ni desplaza el grid;
- early close trunca y termina la sesión;
- no synthetic empty bars.

BREAK interno:

1. forming bar se trunca en break_start;
2. durante BREAK no hay barras;
3. break_end retoma el mismo grid;
4. si break_end cae dentro de un bucket nominal, puede nacer short bar hasta el próximo nominal boundary.

Evento fuera de SessionState OPEN no alimenta bars y queda observable como evento fuera de sesión según D2-05.

Cada timeframe demandado agrega directamente desde canonical MarketEvents. No 1m→5m cascade V1.

## 11. Late-data / decision observation

Bar lifecycle:

~~~text
FORMING → CLOSED
~~~

Close ocurre por el primer trigger válido:

- boundary event; o
- TimerFired del close boundary.

Nunca depende sólo del próximo tick.

Late policy V1:

- si el evento pertenece al último bucket cerrado, la market bar projection puede corregirse X→X';
- si la siguiente barra ya cerró, el evento no cambia bars y produce late-drop telemetry;
- el MarketEvent canónico sigue existiendo en ambos casos.

Invariante central:

~~~text
Timer/boundary
→ BAR_CLOSE snapshot X
→ Strategy decision sobre X
→ late MarketEvent
→ projection X'

NUNCA:
late correction X'
→ reevaluar decisión anterior
~~~

La decision observation X es inmutable. No retrospective Signal. No segunda evaluación. correction_count/provenance hacen visible X' como projection actualizada.

## 12. MTF / indicators

MTF V1 = direct aggregation por timeframe desde MarketEvents canónicos.

Builders son demand-driven y compartidos por stream. No existe builder por Account.

Indicator ownership:

- Strategy-side dentro de echo/strategy_engine.
- MM-side dentro de su propia decisión cuando su config lo requiere, leyendo MarketContext compartido.
- no global indicator service V1.

200 Accounts usando S1:

- una Strategy evaluation;
- un set de indicators S1;
- un builder set por stream/timeframes;
- fan-out posterior a Accounts.

Sharing cross-Strategy de indicators queda YAGNI hasta que un benchmark demuestre costo material.

## 13. Warm-up / recovery / rollover

NEW RUN / NEW STRATEGY:

~~~text
MarketHistorySource
→ raw normalized MarketEvents
→ same bar semantics
→ indicators/finite state
→ Analytical READY
→ Signals
~~~

Warm-up usa eventos normalizados, no vendor bars prebuilt. Calendar/config snapshot del segmento acompaña provenance.

NORMAL RESTART:

- restaura market/analytics/strategy decision state desde checkpoint StateFun/Flink;
- no reemplaza silenciosamente decision-state con historia final corregida.

SOURCE SWITCH / RECOVERY CON EPOCH CHANGE:

1. barrier;
2. current previo → last-known;
3. forming descartada, sin synthetic close;
4. closed bars viejas quedan epoch-scoped;
5. current nuevo vacío → seed;
6. history-dependent state se reconstruye capability-driven;
7. cada consumer recupera analytical readiness según sus requirements.

Clase C sin rebuild exacto demostrable ⇒ ANALYTICAL_REBUILD_UNPROVABLE.

No existe fake cursor basado sólo en event_ts y no se descarta un evento live sólo porque event_ts < un cutover conceptual.

ROLLOVER:

- nueva stream contract-specific;
- warm-up del Contract nuevo según requirements;
- Strategy no emite sobre el Contract nuevo antes de readiness;
- Operations viejas mantienen market context de su Contract pinneado;
- jamás se mezclan Contracts en bars.

## 14. Strategy / MM consumption

Strategy consume read-only:

- BAR_CLOSED deliveries;
- current market state;
- window/session transitions;
- requirements y analytical state propios.

Trigger cadence declarada: BAR_CLOSE, MARKET_EVENT sólo si la Strategy realmente lo necesita, WINDOW_TRANSITION.

Strategy bars-only no recibe firehose de ticks. Evalúa una vez por trigger y recién después emite Signal hacia fan-out.

MM consume MarketContext read-only desde echo/operation:

~~~text
MarketContext {
  stream_id
  instrument_id
  contract_id
  authority_epoch
  current
  last_known_previous?
  bars(stream, timeframe)
  readiness
  session
}
~~~

Gate es por input requerido. Un MM BBO-only puede volver antes que un cálculo que necesita ATR/warm-up. Safety/provider/execution no quedan bloqueados por market readiness.

Market Runtime nunca inventa monetary close ni ForceClose por outage. Sólo informa calidad, readiness y current-vs-last-known; la decisión monetaria pertenece a D2-04/D2-05.

## 15. Deterministic runtime input model

La única frontera de input market-dependent es:

~~~text
MarketRuntimeInput =
  MarketEvent
  | RecoveryBarrier
  | TimerFired
  | SessionWindowTransition
  | ConfigTransition
~~~

BAR_CLOSED y BAR_UPDATED no son inputs autoritativos grabados: son outputs derivados de la lógica de bars.

Cuatro identidades:

| Identidad | Responsabilidad |
| --- | --- |
| event_ts | semántica técnica del mercado |
| stream_seq | orden/idempotencia canónica per stream |
| owner_input_seq | orden de admisión observado por una isla |
| runtime_ts | runtime logical time monotónico de esa isla |

owner_input_seq no crea total order global. Es per-island y checkpointeado.

runtime_ts:

- LIVE: max(runtime_ts previo, wall/admission time), con owner_input_seq como desempate;
- EXACT_REPLAY: valor journalado;
- BACKTEST: synthetic monotonic time según síntesis canónica.

Un late MarketEvent con event_ts anterior nunca hace retroceder DomainClock.

## 16. DomainClock / timers

API conceptual única:

~~~text
DomainClock {
  Now()
  Schedule(timer_id, deadline, payload)
  Cancel(handle)
}
~~~

LIVE:

- Now() = runtime_ts de la entrada actual;
- Schedule usa SendAfter/CancellationToken;
- firing vuelve al dominio como TimerFired.

EXACT_REPLAY:

- Now() = runtime_ts journalado;
- timer set es virtual;
- no sleeps;
- el firing ocurre cuando lo inyecta el journal.

BACKTEST:

- clock lógico sintético monotónico;
- misma lógica de dominio, sin imitar latencia live.

Timer identity:

~~~text
timer_id + generation
~~~

Re-Schedule = cancel old generation + new generation. Un stale firing de generación vieja es deterministic NO-OP. Un firing de generación inexistente en replay ⇒ REPLAY_LOG_CORRUPT.

Todo TimerFired admitido por dominio se journaliza, incluso si no muta inmediatamente un enum visible, porque puede afectar control flow futuro.

## 17. Ordering / multi-stream

No existe global sequencer.

Per-island owner_input_seq captura el orden material observado por:

- market_stream;
- market_analytics;
- strategy_engine;
- MM market gate cuando corresponda.

Cross-stream Strategy:

- key strategy_id;
- recibe deliveries de N streams + timers/transitions;
- journala el merge observado;
- cada delivery puede referenciar la posición del emisor sin duplicar contenido.

EXACT_REPLAY reproduce ES + NQ + timer en el mismo orden observado live.

BACKTEST usa canonical synthesis order, no arrival disorder:

1. RecoveryBarrier/epoch marker del escenario;
2. ConfigTransition;
3. SessionWindowTransition;
4. MarketEvent ordenado por event_ts, stream_id, stream_seq;
5. TimerFired por deadline, timer_id.

Dos órdenes distintos pueden producir decisiones distintas y ambos ser correctos: EXACT_REPLAY reproduce el live real; BACKTEST crea un run canónico nuevo.

## 18. Recorded boundary / replay anchor

Recording conceptual:

~~~text
Run Recording =
  Initial RunManifest
  + ReplayAnchor
  + DeterministicInputLog
  + canonical content
~~~

ReplayAnchor = OPTION A immutable warm-up corpus.

Contiene o referencia inmutablemente:

- EXACT normalized MarketEvents usados por warm-up;
- calendar/config snapshots correspondientes;
- corpus refs;
- digest;
- readiness assertion post-warm-up.

Se captura desde el inicio del run grabado. EXACT_REPLAY re-ejecuta el anchor con la misma lógica de warm-up B antes de owner_input_seq=0.

Nunca vuelve a consultar MarketHistorySource.

Errores fail-visible:

- REPLAY_ANCHOR_MISSING;
- REPLAY_ANCHOR_INVALID;
- REPLAY_SOURCE_MISSING;
- REPLAY_LOG_CORRUPT.

DeterministicInputLog, per run/per island, conserva owner_input_seq + runtime_ts y:

- market input por ref a contenido canónico;
- controls pequeños inline;
- source_ref para orden cross-island.

Se journaliza todo input admitido cuya omisión pueda cambiar una observación presente o futura. ALWAYS: TimerFired admitido, ConfigTransition material, RecoveryBarrier, Session/WindowTransition material, MarketEvent refs que pasan guards y deliveries cross-island necesarios. MAY OMIT: redelivery absorbido antes del dominio, duplicate exact NO-OP, telemetry-only sin efecto de control flow.

Journal egress es transaccional EXACTLY_ONCE en la misma frontera de checkpoint. El contenido canónico no se duplica dentro del journal.

## 19. EXACT_REPLAY vs BACKTEST

EXACT_REPLAY:

- reproduce un run live real;
- usa initial manifest + anchor + journal + canonical content;
- reproduce owner_input_seq y runtime_ts reales;
- reproduce late-arrival/timer/barrier ordering;
- produce market-dependent decision log;
- no toca venue;
- no sustituye restart/recovery del live.

Garantía:

~~~text
same initial manifest
+ same anchor
+ same deterministic ordered inputs/runtime_ts
+ same code
⇒ same market-dependent decisions
~~~

BACKTEST/HISTORICAL:

- es un run nuevo sobre historia;
- usa MarketHistorySource;
- usa canonical precedence;
- usa synthetic monotonic runtime clock;
- usa snapshots explícitos de Calendar/RuleSet/DayBoundary/Contract cuando correspondan;
- no promete reproducir arrival disorder de un live previo.

No se usa la palabra REPLAY para BACKTEST en contratos nuevos.

## 20. Config/calendar/source transitions

Regla: toda config capaz de cambiar una decisión market-dependent en live es pinned en initial manifest o aparece como ConfigTransition material en el journal. No existe hot change silencioso.

Casos materiales:

- ExchangeCalendar revision;
- MARKET_DATA source switch;
- Contract rollover mapping;
- MarketRequirements change;
- readiness/view transition que abre o cierra gate;
- cualquier Strategy/MM market config que una semántica futura permita cambiar hot.

Source switch se representa como ConfigTransition(switch) seguido por RecoveryBarrier(epoch++).

Rollover se representa como ConfigTransition(mapping) y demanda de otra logical stream. Nunca auto-roll.

### Initial RunManifest immutability

El snapshot inicial del RunManifest es INMUTABLE y representa las condiciones de arranque del run.

Shape conceptual:

~~~text
RunManifest {
  initial {                         # immutable
    run_id
    run_mode
    replayed_run_id?
    strategy_snapshot
    mm_snapshot
    market_semantics_version
    calendar_snapshots
    source_capability_provenance
    starting_contracts_and_streams
    requirements_digest
    replay_anchor_identity
    run_time_origin
    recording_identity
  }

  operational {                     # append/accumulate metadata only
    recording_status?
    completed_at?
    ranges?
    integrity_status?
  }
}
~~~

Hot changes posteriores NO reescriben initial.

Todo cambio material posterior vive como ConfigTransition ordenada en DeterministicInputLog. Replay siempre obtiene:

~~~text
initial manifest
+ ordered ConfigTransitions
~~~

Si echo.market-run-manifests.v1 es compacted por run_id, el valor más nuevo puede acumular completion/ranges/status, pero DEBE preservar intacta la sección initial y su digest. Está prohibido usar el record compactado como latest-effective-config y perder las condiciones iniciales.

## 21. Physical topology

Topología V1 integrada:

~~~text
feed adapters
  → echo.market-feed-candidates.v1
  → echo/market_stream                    key stream_id
  → echo.market-events.v1                 canonical AT_LEAST_ONCE
  → echo/market_analytics                 key stream_id
  → echo/strategy_engine                  key strategy_id
  → echo.signals.v1
  → echo/signal_fanout
  → echo/operation                        key account:strategy
~~~

Control/read models/recording:

- echo.market-stream-state.v1 — compacted stream state/readiness/provenance.
- echo.market-bars.v1 — compacted bar ring/latest projection, read model.
- echo.market-run-journal.v1 — deterministic ordered journal, transactional EXACTLY_ONCE.
- echo.market-run-manifests.v1 — compacted per run, preserving immutable initial.
- ReplayAnchor storage/reference — same retention contract as recording.
- DomainClock — SDK library.
- ReplayDriver — offline/in-process.

No nueva flota de microservicios. No Account keys en market analytics. No consensus sequencer. No indicator service.

## 22. Durability / state ownership

CHECKPOINTED:

- runtime mutable state de market_stream;
- market_analytics forming/rings/rebuild state;
- strategy_engine analytical/decision state;
- owner_input_seq counters;
- D2-04 operation/mm_state según su propia autoridad.

DERIVED / RECONSTRUCTABLE:

- bars;
- session/grid context;
- analytical market state;
- indicators/Strategy state para NEW RUN o rebuild cuando existe fuente suficiente.

DURABLE CANONICAL:

- normalized MarketEvent content requerido durante el recording horizon.

RECORDED:

- immutable initial manifest;
- replay anchor;
- ordered deterministic journal.

READ MODEL:

- compacted stream state/latest projection;
- echo.market-bars.v1.

EXTERNAL EXECUTION AUTHORITY:

- Operation/Order/Fill/Position, physical execution effects y execution recovery permanecen D2-04/D2-05 y fuera del replay de mercado.

PG no se introduce como market runtime recovery authority.

## 23. Echo V3 reuse/adapt

REUSE:

- Flink StateFun keyed state/checkpoints;
- module ingress/egress registration pattern;
- kache + compacted hot-config pattern;
- ctx.SendAfter + CancellationToken como mecanismo LIVE de timers;
- OTel DI/telemetry;
- pure-domain package convention;
- D2-04 transactional egress pattern para durable journal.

ADAPT / EXTEND:

- MMEngine join pattern → read-only MarketContext;
- existing ValueSpecs → owner_input_seq aditivo en islands relevantes;
- fan-out pattern → Strategy Signal fan-out ya congelado por D2-04;
- mock/e2e in-process harness → ReplayDriver.

NEW logical surfaces:

- echo/market_stream;
- echo/market_analytics;
- echo/strategy_engine;
- MarketHistorySource seam;
- DomainClock library;
- ReplayDriver offline;
- market feed/events/state/bars/journal/manifests contracts.

REPLACE / DO NOT PROMOTE:

- legacy MT InstrumentSnapshot/feed no es authority Futures;
- no adaptar Bridge MT feed como Futures market-data authority;
- no usar vendor bars como canonical bar authority;
- no usar PG como replay/recovery source del market decision state.

DEFERRED_DEBT:

- recording archival/object storage beyond configured horizon;
- replay from midpoint;
- distributed multi-node replay;
- future depth/book semantics;
- indicator sharing cross-Strategy if benchmark ever justifies it.

## 24. Scale

20 o 200 Accounts usando S1 NQ:

- una logical stream por Contract;
- una ingestion/arbitration;
- un canonical event stream;
- un builder set por demanded timeframes;
- un S1 analytical state + indicator set;
- una evaluación por trigger;
- fan-out posterior a Accounts.

Cost drivers reales:

- feed: streams × event rate;
- bars: streams × demanded timeframes × event rate;
- Strategy: strategies × triggers;
- recording: streams/control inputs + strategy merge refs + anchor per run;
- MM: per Operation por naturaleza, leyendo shared market read models.

No costo market-state × Account.

## 25. Failure semantics

Feed member down con equivalent member:

- continúa sólo si identidad/equivalencia y continuity son demostrables;
- sin double evaluation.

Heterogeneous source outage:

- switch explícito;
- contract preserved;
- barrier/rebuild;
- no blend, no auto-roll.

Gap:

- recovery por capabilities;
- A/B identity permite exact overlap dedup;
- clase C no usa heurística;
- unprovable ⇒ NOT_READY/ANALYTICAL_REBUILD_UNPROVABLE.

Exchange CLOSED:

- silencio esperado;
- freshness NOT_EVALUABLE;
- no stale/failure universal.

Feed down con live exposure:

- current puede faltar;
- last-known queda visible con stale/provenance;
- Market Runtime no cierra ni inventa flatten.

Bar close/late:

- close por event/timer;
- exactly one decision observation;
- late projection correction sin retroactive decision.

Recording/replay:

- anchor ausente/mismatch, source purgado o log corrupto ⇒ fail-visible;
- nunca replay parcial silencioso.

Cold execution recovery:

- sigue COLD_RECOVERY_REQUIRED bajo D2-04;
- market recording no reconstruye mm_state ni physical execution truth.

## 26. Parent acceptance A–L

A — FEED SHARING — PASS.
20/200 Accounts sobre S1 NQ comparten una stream/subscription/evaluation; Account count no existe en market keys y el fan-out ocurre después de Strategy evaluation.

B — EQUIVALENT DUAL FEED — PASS.
CME A/B equivalent members sólo cuando comparten identity POSITIONAL demostrada; arbitraje first-wins por packet-position antes de stream_seq evita double evaluate y conserva todas las entries del packet.

C — HETEROGENEOUS BACKUP — PASS.
Cambio cross-authority es source switch explícito: preserva Contract, incrementa epoch, cierra readiness, reconstruye current/analytical state y nunca mezcla sources.

D — GAP 100,101,104 — PASS.
Sequence gap entra RECOVERING; 102/103 se recuperan cuando capability lo demuestra; overlap A/B se deduplica por identidad exacta antes de stream_seq; clase C usa cursor/snapshot/full rebuild o queda fail-visible, nunca fake identity.

E — CLOSED MARKET — PASS.
ExchangeCalendar CLOSED/BREAK hace freshness NOT_EVALUABLE y el silencio no se interpreta como stale/failure universal.

F — CLOSED BAR — PASS.
Boundary event o TimerFired cierra sin esperar próximo tick; Strategy observa exactamente un snapshot X y el closure guard impide segunda evaluación.

G — LATE EVENT — PASS.
09:30:59.900 post-boundary corrige sólo la projection según la policy estructural; EXACT_REPLAY conserva Timer→X→decision→late→X' y no existe retrospective Signal.

H — WARMUP — PASS.
200×1m + 50×5m construyen analytical readiness per consumer; no Signal antes del gate; BBO-only es independiente; ReplayAnchor preserva el estado inicial exacto para EXACT_REPLAY.

I — ROLLOVER — PASS.
Z6→H7 es transición explícita; la Strategy cambia de logical stream sólo al Contract nuevo y sus requirements; Operation vieja mantiene Z6; bars/streams jamás mezclan Contracts.

J — OUTAGE WITH LIVE EXPOSURE — PASS.
MarketContext distingue current, last-known, readiness y quality; MM/safety deciden por policy y Market Runtime no inventa cierre monetario.

K — LIVE/REPLAY — PASS.
Mismo initial manifest + mismo anchor + mismos ordered deterministic inputs/runtime_ts + mismo código reproducen las mismas decisiones market-dependent.

L — 200 ACCOUNTS — PASS.
No hay 200 subscriptions, builders, indicator sets ni Strategy evaluations; sólo fan-out posterior y estado MM per Operation donde corresponde.

## 27. Child acceptance inherited

La integración hereda sin reabrir:

- A: A-R1..R7 y sus acceptance cases asociados.
- B: B-R1..R7 + acceptance O..U.
- C: C-R1..R3 + acceptance Q..T.

Los children siguen siendo evidencia/design depth:

- [[Echo Futures — D2-06A Market Feed Authority]]
- [[Echo Futures — D2-06B Bars Hot State Warmup]]
- [[Echo Futures — D2-06C Live Replay Market Boundary]]

El gate normativo del artifact integrado es Parent Acceptance A–L de §26. Las suites de children no sustituyen ni amplían el gate padre.

## 28. Risks / debts

R-D2-06-1 — StateFun tick throughput/latency.
La topología tick→StateFun→Kafka no está benchmarkeada con tasa Futures real. D6 debe medirla; si el runtime no cumple, la semántica/key ownership puede migrar a worker in-process sin cambiar contratos.

R-D2-06-2 — Recording retention.
EXACT_REPLAY depende de conservar initial manifest + anchor + journal + canonical content por el horizonte declarado. Purga incompleta ⇒ REPLAY_SOURCE_MISSING. Archival/object storage es deuda, no prerequisite arquitectónico V1.

R-D2-06-3 — Class C history continuity.
Sources sin dedup-safe identity pueden quedar incapaces de demostrar rebuild history-dependent tras disruption. Fail-closed es correcto; vendor capability debe verificarse antes de confiar bars/indicators a esa fuente.

R-D2-06-4 — ReplayDriver fidelity.
El driver in-process re-maneja paquetes puros, no todo el runtime StateFun. D6 debe certificar con golden live recording → exact replay y decision log semánticamente idéntico.

R-D2-06-5 — Transactional journal configuration.
La auditabilidad del DeterministicInputLog depende de egress EXACTLY_ONCE/config y atomicidad con checkpoint. Debe certificarse físicamente junto a los requisitos carry de D2-04; no se asume porque el código baseline no lo declare todavía.

R-D2-06-6 — Backup Contract servability.
Un heterogeneous backup incapaz de servir un Contract in-force o pinneado bloquea el switch. Es fail-closed deliberado; config/ops debe validar cobertura antes de necesitarla.

R-D2-06-7 — Strategy runtime completeness.
D2-06 congela ownership/input/output/readiness de echo/strategy_engine, no su lenguaje/configuration product completo. Ese diseño posterior no puede violar este boundary.

R-D2-06-8 — Runtime clock implementation.
LIVE debe derivar runtime_ts monotónico por isla; usar wall clock directo o event_ts como Now() violaría determinismo. Assertions live + replay deben detectar regresión.

## 29. Owner decisions

OWNER_DECISIONS_REQUIRED: OD-C1 únicamente.

OD-C1 — EXACT LIVE REPLAY recording default:

OPTION 1 — ALWAYS-ON V1.

OPTION 2 — OPT-IN por run.

La arquitectura es idéntica. La diferencia es operacional/producto: default de recording, retención contractual y alcance de certificación.

Restricción no negociable: el ReplayAnchor se captura DESDE EL INICIO. Un run iniciado sin recording/anchor no puede convertirse retroactivamente en exact-replayable desde t0.

Recomendación técnica heredada de C: ALWAYS-ON, porque el delta de recording es principalmente refs+control y un anchor acotado por MarketRequirements; no se convierte en decisión owner aquí.

OD-C1 no bloquea READY_FOR_MANAGER_REVIEW porque no altera identidad, ordering, recovery, bars ni el deterministic boundary.

## 30. Implementation handoff / next boundary

Este artifact está listo para Primary Manager review. No se generan SPECs ni tasks de código en D2-06.

Una futura implementación autorizada debe preservar, como gates de contrato:

- stream_id económico y source authority separada;
- stream_seq guard en todo downstream;
- readiness feed vs analytical sin WARMUP_INCOMPLETE global;
- current-state scoped por epoch + previous last-known;
- bars contract-specific, timer-close y immutable decision observation;
- DomainClock sin time.Now() de dominio;
- owner_input_seq/runtime_ts per-island;
- immutable initial manifest;
- replay anchor capturado desde run start;
- ConfigTransitions ordenadas para hot changes;
- no dual authority BAR_CLOSED;
- no Account-keyed market analytics;
- D2-04 execution recovery boundary intacto.

NEXT: Return to D2-06 SUBMANAGER/MANAGER. Do not start D2-07.

## Fuentes

- [[Echo Futures]]
- [[Echo Futures — D2-04 Operation Order Fill Position]]
- [[Echo Futures — D2-05 Instrument Session Provider]]
- [[Echo Futures — D2-06A Market Feed Authority]]
- [[Echo Futures — D2-06B Bars Hot State Warmup]]
- [[Echo Futures — D2-06C Live Replay Market Boundary]]
- xKoRx/echo@372af59a7b83604781346613da01e3d510ea1360

## Owner decision OD-C1 — CLOSED — 2026-09-27

**Decision:** `ALWAYS_ON_V1_SELECTED_STREAMS`.

Owner ratifies always-on EXACT LIVE REPLAY recording for the market streams actually selected/demanded by the run/Strategy/MM runtime, **not for the entire market universe**.

Semantics:

- A run captures its immutable ReplayAnchor from t0 for every selected/demanded stream required by its MarketRequirements.
- DeterministicInputLog/journal recording is always-on for those streams and their material timers/config/session/recovery transitions.
- Symbols/contracts not selected or demanded by the run are not recorded merely because the market-data provider can expose them.
- Adding a new symbol/stream after the run starts creates a new material Config/MarketRequirements transition and begins recording for that stream from its activation point; it does **not** make the pre-activation history exact-replayable unless that history is explicitly part of the newly captured warm-up/anchor extension contract.
- Retention horizon remains operational policy. Always-on means default capture at run start for selected streams, not infinite retention.

This closes OD-C1 without changing the D2-06 architecture.
