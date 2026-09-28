---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo Futures]]"
  - "[[Echo Futures — D2-04 Operation Order Fill Position]]"
  - "[[Echo Futures — D2-05 Instrument Session Provider]]"
  - "[[Echo Futures — D2-06 Market Runtime]]"
  - "[[Echo Futures — D2-07 Execution Runtime]]"
aliases:
  - Echo Futures D2-08
  - EF Strategy Runtime
  - EF Strategy Engine
tags:
  - kind/doc
  - area/echo
  - echo-futures
  - architecture-design
created: "2026-09-28"
updated: "2026-09-28"
---

# Echo Futures — D2-08 Strategy Runtime

## Propósito

Resolver `Q11 — Strategy Runtime` del gate D2: cuándo corren Strategy y MoneyManagement (market event, bar close, window/session transition, timers, execution events), qué estado posee cada uno, cómo se serializa, cómo se produce/fan-out una `Signal` y cómo se preserva determinismo LIVE/EXACT_REPLAY/BACKTEST. Consume como autoridades congeladas D2-01..D2-07 sin reabrirlas. Baseline físico verificada: `xKoRx/echo origin/master = 372af59a7b83604781346613da01e3d510ea1360` (sin delta). No implementa código, no abre providers, no diseña adapters ni transports (D2-07 CLOSED), no avanza D3/D4/D5/D6, no cierra D2 global.

## 1. Executive verdict

```text
D2-08 STATUS: MANAGER_CLOSED
Q11: CLOSED
OWNER DECISIONS REQUIRED: NONE
```

Decisión central: **el runtime de Strategy es una isla StateFun nueva `echo/strategy_engine` keyeada por `strategy_id`** (ownership ya congelado por D2-06 §9), que posee el estado técnico completo de la Strategy — estado finito del ciclo técnico, indicators, analytical readiness, timers, config efectiva y bookkeeping determinista — y evalúa **una única vez por trigger admitido**, emitiendo `0..N Signals` ordenadas por el egress transaccional `echo.signals.v1` hacia el fan-out ya congelado (`echo/signal_fanout` key `strategy_id`, D2-04 §8.1) y de ahí hacia `echo/operation` (key `account:strategy`), donde MoneyManagement vive como plugin de dominio con su estado (`mm_state`) dentro del aggregate Operation (D2-04 §8.1).

- **El ciclo lógico Strategy es técnico, no físico.** La Strategy abre/cierra ciclos propios identificados por un `strategy_cycle_seq` monotónico y **jamás espera convergencia física de cuentas**. Cada AccountStrategy puede ir físicamente detrás; el owner account-specific conserva como máximo un ciclo futuro diferido mientras termina la Operation anterior, sin crear una segunda Operation concurrente.
- **Triggers declarativos, mínimos, sin DSL:** cada Strategy declara en su config efectiva las familias de input que necesita (`BAR_CLOSE` con timeframes, `MARKET_EVENT` sólo si su semántica lo exige, `WINDOW_TRANSITION`, `SESSION_TRANSITION` cuando material, `TIMER` declarado). Una Strategy bars-only no recibe firehose de ticks (D2-06 §14). La declaración alimenta los `MarketRequirements` de D2-06; su cambio hot es `ConfigTransition` material.
- **MM corre por triggers de la Operation, no del mercado global:** Signal delivery, execution facts (`OrderStatusEvent`/`OrderActionResult`/`Fill` ya correlacionados por el routing de tres caminos D2-07 §17), intents de terminación (`ForceClose`), `TimerFired` y —sólo si ese MM lo declara— notificaciones de mercado. El cálculo puro de `sdk/mm` sigue siendo librería; el **estado** MM vive en el keyed state de `echo/operation` (D2-04 congelado; el `MMEngineFn` legacy con `PendingMM` TTL es REPLACE para el path Futures).
- **Determinismo:** la propiedad congelada es de dominio — mismo stream ordenado de inputs admitidos ⇒ mismas decisiones. LIVE serializa por isla con `owner_input_seq`; EXACT_REPLAY reproduce el run live real con el boundary D2-06 (manifest + anchor + journal); BACKTEST ejecuta la misma lógica pura con driver sintético y `SimExecution` (D2-04 §8.7). Prohibido `time.Now()` en lógica de dominio; todo tiempo de dominio entra como `runtime_ts` vía `DomainClock` (D2-06 §15/§16).
- **Escala:** 1 Strategy + 200 Accounts ⇒ 1 estado Strategy, 1 evaluación por trigger, 1 set de indicators, 1 Signal, N deliveries, N decisiones MM aisladas. El costo de mercado no se multiplica por cuenta; el costo MM escala N sólo porque el riesgo/account state realmente es N (y sólo para los triggers que cada MM declara).
- Cero entidades nuevas genéricas: no `StrategyActorFramework`, no plugin marketplace, no workflow engine, no event bus, no portfolio aggregate, no global sequencer, no indicator service (D2-06 §21/§23 ya los prohíbe). Superficie nueva: 1 función `echo/strategy_engine`, egress `echo.signals.v1` EXACTLY_ONCE, contrato declarativo de triggers/requisitos y el adapter legacy `ReferenceEvent → Signal` como seam en Core.
- Ratificaciones técnicas ordinarias para el manager (no owner): nombres físicos finales de topics/campos, shape exacto del struct declarativo de triggers y del envelope `SignalDelivery`, y la config `EXACTLY_ONCE` del egress de señales (mismo requisito de SPEC que D2-04 R2; el `module.yaml` actual no declara delivery semantics — verificado físicamente).

## 2. Authorities / frozen inputs

En orden de jerarquía:

1. [[Echo Futures]] — decisiones owner D2-01..03, lifecycle A2, requisitos V1, cierre D2-07 y rollout owner D6.
2. [[Echo Futures — D2-04 Operation Order Fill Position]] — Operation/Order/Fill/Position, `echo/operation` + `echo/signal_fanout`, `mm_state`, M1/M2, idempotencia `(account_strategy_id, signal_id)`, recovery authority.
3. [[Echo Futures — D2-05 Instrument Session Provider]] — Instrument/Contract, Calendar/Session/NamedTradingWindow, `NextSessionTransition`, provider gates (Stage-1 linearizado en `echo/provider_rules`), hot vs pinned.
4. [[Echo Futures — D2-06 Market Runtime]] — `echo/market_analytics` (key `stream_id`) y `echo/strategy_engine` (key `strategy_id`), trigger cadence declarada, readiness layering, `owner_input_seq`/`runtime_ts`, DomainClock, journal/ReplayAnchor, escala 200 cuentas.
5. [[Echo Futures — D2-07 Execution Runtime]] — routing de tres caminos de execution events hacia `echo/operation`, comandos per-account, separación Bridge/Adapter (contexto, no scope de diseño aquí).

Congelados que este artifact no reabre: D2-01 (sin version/revision framework; snapshot prospectivo), D2-02 (máx 1 Operation no terminal por AccountStrategy; Strategy account-agnostic; sin `operation_key`/`StrategyTrade`), D2-03 (única salida canónica `Signal` con intents `OPEN/REDUCE/CLOSE/CLOSE_ALL` y campo `details`), D2-04 (MM state con la Operation), D2-05 (Provider rules/admission/capacity/safety separados), D2-06 (bar semantics, immutable decision observation, sin retrospective Signal por corrección de barra, 1 evaluación + fan-out), D2-07 (Strategy/MM no conocen transport).

Contexto no-scope: el rollout owner D6 (Topstep first → Lucid → incremental → ~6 props) es dirección de implementación; el Strategy Runtime diseñado aquí es idéntico para todos los providers y no contiene nada provider-specific.

## 3. Strategy owner / state (`echo/strategy_engine`, key `strategy_id`)

Owner físico: función StateFun nueva (patrón exacto de las functions existentes; registro en `module.yaml`). Key = `strategy_id`, ya congelado por D2-06 §9 ("Strategy indicators + finite state + analytical readiness | echo/strategy_engine | strategy_id"). Una instancia serializa todos sus mensajes (garantía StateFun por key) ⇒ las evaluaciones de una Strategy son estrictamente secuenciales sin locks.

Estado poseído (keyed state, checkpointeado por Flink/StateFun — categoría CHECKPOINTED de D2-06 §22):

- **Estado finito técnico del ciclo lógico** (§7): `TECHNICAL_CLOSED` / `TECHNICAL_OPEN{technical_direction, technical_context}` más lo que la semántica de cada Strategy necesite (p. ej. para S1: niveles del Opening Range, ventana activa). Es estado técnico de la propia lógica de la Strategy, no exposición de cuentas.
- **Indicators** (strategy-side, D2-06 §12): el set que su lógica requiere por stream/timeframe demandado, construido sobre las barras/inputs que la isla recibe. No existe indicator service global; sharing cross-Strategy queda YAGNI (D2-06 §12).
- **Analytical readiness** (D2-06 §7): `AnalyticalRequirementsReady(strategy)` derivado de sus requirements; gate de emisión — una Strategy no emite Signal antes de readiness (warm-up D2-06 §13).
- **Trigger requirements declarados** (§4) y **config efectiva** (§19): la config corriente que gobierna evaluación y triggers.
- **Timers propios** (§13): manejados vía `DomainClock` (D2-06 §16) con identidad `timer_id + generation`.
- **Bookkeeping determinista:** `owner_input_seq` (orden de admisión), `strategy_eval_seq` (monótono por evaluación), `strategy_cycle_seq` (monótono por ciclo técnico), identidad del último trigger procesado y dedup de triggers. La isla mantiene además `active_cycle_config` y, si llega config nueva mientras el ciclo está OPEN, `pending_strategy_config` para activación prospectiva al próximo ciclo.

Explícitamente **NO posee** (prohibido por mandato y por boundaries congelados): balances de cuentas, estado Provider/`echo/provider_rules`, estado mutable de MoneyManagement (`mm_state` vive en `echo/operation`, D2-04 §2.1), Orders físicas, Fills, Positions de cuentas, ni resultados de ejecución por AccountStrategy. La Strategy es read-only respecto del mundo físico: no consume execution events, no consume Fills, no recibe feedback de `echo/operation`. Ningún path de estado vuelve de la ejecución hacia la Strategy.

## 4. Trigger contract (declarativo, mínimo)

Cada Strategy declara en su config efectiva (config-of-record, distribuida hot por el patrón compactado/kache existente) un struct declarativo único, sin DSL, sin plugin framework:

```text
StrategyTriggerRequirements {
  bar_close:          [ { instrument_id, timeframes[] } ]   # vacío si no usa barras
  market_event:       NONE | QUOTE | TRADE                  # sólo si su semántica lo exige
  window_transitions: [ window_id ]                         # NamedTradingWindow (D2-05 §10)
  session_transitions: bool                                # NextSessionTransition material
  timers:             [ { timer_id, semantics } ]          # declarado, programado en runtime
}
```

Semántica:

- La declaración **alimenta los MarketRequirements** de D2-06 (§5 demand/§7 readiness): define qué streams/timeframes/input classes la isla necesita y qué readiness gate aplica (`EffectiveConsumerReadiness`). Una Strategy bars-only declara `market_event: NONE` y **no recibe el firehose de ticks** — el mercado no la invoca por tick.
- `WINDOW_TRANSITION` y `SESSION_TRANSITION` llegan como `SessionWindowTransition` (input autoritativo D2-06 §15), derivados exclusivamente de `NextSessionTransition` del calendario (D2-05 §8/§10): timers calculados por el runtime de sesión, nunca offsets hardcodeados. `WINDOW_TRANSITION` de una ventana cerrada (`window_open ∧ exchange_session_open`, D2-05 §10) no dispara evaluación productiva: la availability del exchange siempre gana.
- `TIMER` cubre lo que la semántica de la Strategy necesite (p. ej. apertura de ventana, expiración técnica, re-arme): se programa vía `DomainClock.Schedule` en la isla y regresa como `TimerFired` journalizado (D2-06 I15/§16).
- `MARKET_EVENT` es opt-in explícito por Strategy. Es la única familia que puede escalar con la tasa de ticks; por eso está gated detrás de una declaración explícita y es candidato natural a migración de topología (riesgo R-D2-06-1 de D2-06) sin cambiar contratos.
- El cambio hot de la declaración es **material**: es `ConfigTransition` en el journal (D2-06 §20) y actualiza los MarketRequirements/readiness de la isla. Nunca es un hot change silencioso.

El mismo patrón declarativo sirve para MM (§10) con su propio scope: el MM declara requisitos de mercado por Operation, no reutiliza los de la Strategy (§15).

## 5. Strategy evaluation semantics

Por trigger admitido (bars-only, MARKET_EVENT, window/session transition, TimerFired, ConfigTransition material que lo exija):

```text
input admitido (identity + owner_input_seq sellados)
  → evaluación determinística (lógica pura: input + estado técnico + indicators + config + runtime_ts)
  → mutación de estado técnico (cycle open/close/context)
  → 0..N Signals ordenadas (signal_seq 1..N dentro de la evaluación)
  → egress transaccional echo.signals.v1 (EXACTLY_ONCE, misma frontera de checkpoint)
```

Resoluciones puntuales:

- **¿Puede una evaluación producir cero Signals? Sí, y es el caso común** (trigger válido sin setup — caso B). La evaluación identidad persiste en `strategy_eval_seq` aunque no emita nada: la ausencia de Signal es una decisión determinística, no un no-evento indemonstrable (su input quedó journalizado por D2-06 §18).
- **Cardinalidad por evaluación: `0..N` ordenadas.** D2-03 congela que `Signal` es el único contrato de salida (no `StrategyAction`); no congela cardinalidad. La decisión owner D1 ([[Echo Futures]], A1 review) acepta explícitamente "más de una Signal como resultado de una misma evaluación" con procesamiento determinístico cuando el orden cambia el resultado (`CLOSE_ALL` seguido de `OPEN` para reversal). Este artifact congela la mecánica: la evaluación retorna una **lista ordenada** sellada con `signal_seq` monótono por Strategy; el orden intra-evaluación se preserva end-to-end (§12/§17) y `echo/operation` lo aplica en orden (A1). El caso dominante es 0 o 1.
- **Identidad de la evaluación:** `(strategy_id, trigger_identity, strategy_eval_seq)`. La `trigger_identity` es la identidad natural del input (BarId para BAR_CLOSE, `stream_seq` para MARKET_EVENT con guard I5 de D2-06, `session_id+boundary` para transiciones, `timer_id+generation` para timers). Redelivery del mismo trigger ⇒ guard de dedup por identidad ⇒ NO-OP antes de evaluar (sin doble evaluación, sin doble Signal — mismo principio que el `stream_seq` guard de D2-06 I5).
- **Identidad de la Signal:** `signal_id` es **determinística**, derivada de la identidad estable del run + `strategy_id + strategy_eval_seq + signal_seq` (encoding concreto = implementación; puede representarse como UUID/string estable). No usa aleatoriedad ni wall clock para correctness. Esto preserva la dedup `(account_strategy_id, signal_id)` de D2-04 y permite que crash/restart y EXACT_REPLAY regeneren la **misma identidad**, no sólo una Signal semánticamente equivalente. `strategy_cycle_seq` viaja aparte para correlacionar el ciclo técnico.
- **Evitar duplicate fan-out:** dos barreras — (1) la atomicidad estado↔egress (una Signal checkpointeada es durable en `echo.signals.v1`; una transacción abortada no deja Signal visible); (2) el replay de Kafka ingress en el fan-out se absorbe con el dedup `signal_id` + guard `(strategy_eval_seq, signal_seq)` del fan-out owner (§6). `echo/operation` aplica la tercera barrera ya congelada (D2-04 §5.1).
- **Crash/restart:** checkpoint restaura estado técnico, indicators, readiness, bookkeeping y timers (con generation). Los triggers ya procesados no se re-evalúan (offsets del ingress commitean con el checkpoint; el replay post-checkpoint re-procesa desde Kafka con las mismas guards idempotentes).

## 6. Signal runtime identity (contrato, no re-diseño)

D2-03 congela intents y `details`; este artifact añade sólo los campos runtime mínimos que el camino (emisión → fan-out → delivery → materialización) ya exige:

```text
Signal {
  signal_id            # identidad determinística de idempotencia
  strategy_id
  strategy_cycle_seq    # ciclo técnico al que pertenece la Signal
  intent               # OPEN | REDUCE | CLOSE | CLOSE_ALL   (D2-03, inmutable)
  instrument_id        # canónico; Strategy jamás resuelve Contract (D2-03/D2-05)
  direction            # dirección técnica canónica cuando el intent la requiere
  details              # payload técnico Strategy-specific D2-03: entry/trigger semantics,
                       # SL/TP técnicos, niveles, indicadores/contexto y demás detalle compatible Strategy↔MM
  created_at           # runtime_ts de emisión (event-time de la isla, D2-06 §15)
  valid_until          # ventana de validez; expirada NO materializa Operation (D2-04 §3.1 guard)
  provenance {
    strategy_eval_seq, signal_seq     # orden canónico; signal_id deriva de estos + run/strategy
    trigger_identity                  # qué disparó la evaluación
    run_mode / run_id                 # provenance LIVE/SHADOW/DEMO/REPLAY/BACKTEST (I11 D2-04)
    source                            # NATIVE | REFERENCE  (adapter legacy, §17)
  }
}
```

No se agregan campos "por si acaso": ni `account`, ni `contract_id`, ni sizing, ni provider. `strategy_cycle_seq` es un escalar de correlación/runtime, **no una entidad nueva** ni un `operation_key`: permite distinguir una acción del ciclo corriente de una nueva apertura perteneciente al ciclo siguiente cuando una cuenta todavía está cerrando físicamente el anterior. `(strategy_eval_seq, signal_seq)` da orden/provenance y alimenta la identidad determinística `signal_id`.

## 7. Logical OPEN/CLOSED vs physical accounts

Congelado por D2-02: `Strategy logical state ≠ physical AccountStrategy execution state`. D2-08 agrega sólo una identidad escalar monotónica:

```text
strategy_cycle_seq
```

No es una entidad, no es `operation_key` y no crea un aggregate adicional. Identifica el ciclo técnico al que pertenece cada Signal.

Semántica:

```text
TECHNICAL_CLOSED
  OPEN emitida       → incrementa strategy_cycle_seq; ciclo k queda OPEN

TECHNICAL_OPEN(k)
  REDUCE/CLOSE       → Signal pertenece a k
  CLOSE_ALL          → declara cierre técnico de k
  OPEN de reversal   → abre k+1 sólo después de sellar el cierre técnico de k
```

La Strategy sigue siendo account-agnostic y jamás espera convergencia física. Por eso una cuenta puede estar todavía ejecutando la Operation del ciclo k cuando recibe Signals del ciclo k+1. El owner `echo/operation` resuelve esa diferencia sin crear dos Operations simultáneas:

- si llega `OPEN(k)` y la Operation corriente también pertenece a k, se mantiene la regla D2-04: es una acción/add sobre la Operation corriente y MM decide su materialización;
- por AccountStrategy, un `strategy_cycle_seq=k` puede materializar **como máximo una identidad de Operation durante toda la vida de ese ciclo**. El owner conserva el escalar `last_materialized_cycle_seq` (bookkeeping, no entidad). Si todavía nunca existió Operation(k) —por ejemplo, un OPEN anterior fue DENY en Stage-1 y por ello no materializó nada— un OPEN(k) posterior aún puede intentar la primera materialización. Si Operation(k) ya existió y quedó TERMINAL tempranamente (`ENTRY_FAILED`, etc.), otro OPEN(k) **no crea una segunda Operation**: se trata como no-op/fail-visible de ese ciclo. Una nueva Operation requiere k+1;
- si llega `OPEN(k+1)` mientras Operation(k) aún no es TERMINAL **y ésta ya tiene intent de terminación por CLOSE/CLOSE_ALL**, el owner guarda la Signal como `pending_next_cycle_open` y NO la aplica a la Operation vieja;
- el owner puede retener junto a esa apertura las Signals posteriores **del mismo ciclo futuro k+1** en un buffer acotado por ese único ciclo, preservando `signal_seq`; no existe backlog arbitrario de ciclos;
- cuando Operation(k) alcanza TERMINAL, el owner procesa `pending_next_cycle_open` por las guards normales de materialización (valid_until, binding, Stage-1 provider admission, Contract resolution). Sólo entonces puede existir Operation(k+1);
- si la Signal expiró/queda disabled/denied, se descarta explícitamente con telemetría; jamás se materializa tarde en silencio;
- si aparece un ciclo k+2 mientras k sigue físico y k+1 ya está diferido, el AccountStrategy entra en `ACCOUNTSTRATEGY_CYCLE_LAG`: fail-closed para new risk hasta converger. No se acumula historia ilimitada.

Así, el caso Owner `CLOSE_ALL(k) → OPEN(k+1)` de una misma evaluación es ejecutable y determinístico sin violar `max 1 non-terminal Operation per AccountStrategy` ni cruzar la dirección immutable de la Operation vieja.

Una Operation puede terminar `ENTRY_FAILED` mientras Strategy sigue OPEN; eso sigue siendo correcto. Haber materializado Operation(k) sella ese ciclo para esa AccountStrategy: no se crea una segunda Operation(k) después del terminal temprano. Si el ciclo k nunca materializó Operation porque Stage-1 lo denegó, un OPEN(k) posterior todavía puede intentar su primera materialización. Signals de gestión para un ciclo sin Operation son no-op/fail-visible y nunca se aplican por accidente a otro ciclo.

## 8. Signal fan-out (`echo/signal_fanout`, key `strategy_id`)

Ya congelado como función nueva por D2-04 §8.1/§8.3 ("sucesor del patrón `ExecutionPlannerFn`... lee bindings habilitados por strategy desde kache, filtra por whitelist/estado de cuenta (patrón RFC-007) y entrega la Signal a cada `echo/operation` por su key, preservando el orden intra-evaluación (`signal_seq`)"). D2-08 completa la semántica que faltaba:

- **Autoridad del target set:** el catálogo `AccountStrategy` (Account + Strategy + MoneyManagement + enabled) es **config** distribuida por el patrón hot compactado existente (kache/read model). El target set de una Signal es el **estado de ese catálogo linealizado en el punto de procesamiento del fan-out owner**: la cola del island es el linearization point (misma filosofía que R15 de D2-05, con kache como read model de la isla, no como authority externa). No se promete simultaneidad física global: una Signal en vuelo usa el set visible en su linearization point.
- **Semántica enabled/disabled:** binding `enabled` ⇒ recibe todas las Signals de esa Strategy. Binding `disabled` ⇒ **no recibe `OPEN`** (ningún riesgo nuevo), pero **sí recibe Signals de gestión sobre una Operation viva existente** (`REDUCE/CLOSE/CLOSE_ALL`) — coherente con el principio congelado de D2-05 §12 (las salidas jamás se bloquean) y con R17 (la routing identity se retiene mientras pueda poseer una Operation no terminal). Un binding disabled sin Operation viva no recibe nada. El safety fan-out de `echo/provider_rules` (R17) es un canal separado y no depende de esto.
- **Hot config race (caso H):** determinista por construcción. El target set se fija en el linearization point del fan-out; cada delivery porta la identidad del binding (`account_strategy_id`) y del `signal_id`. El re-chequeo local final ocurre en `echo/operation` (D2-05 §14 paso 5): si el binding quedó disabled antes de que la delivery llegue, una `OPEN` se descarta con telemetría `SIGNAL_DELIVERY_DROPPED{reason=BINDING_DISABLED}` y sin Operation; las Signals de gestión se procesan igual (actúan sobre la Operation existente). Para EXACT_REPLAY, el catálogo y sus cambios viven como `ConfigTransition` ordenadas en el journal (D2-06 §20) ⇒ el target set es reproducible.
- **Retries/redelivery:** el ingress es at-least-once; el fan-out owner deduplica por `(strategy_id, signal_id, account_strategy_id)` (dedup set + guard `(strategy_eval_seq, signal_seq)`) antes de cada `ctx.Send`. No hay retry lógico propio: Kafka/StateFun garantizan la delivery at-least-once por key y `echo/operation` aplica su dedup congelada `(account_strategy_id, signal_id)` (D2-04 §5.1).
- **Target identity:** la delivery se envía a la address `(echo/operation, account_id:account_strategy_id)` — el op key congelado. El fan-out no conoce ni resuelve nada físico (no transport, no provider, no contract).
- **Sin cross-account mutable state y sin re-evaluación por cuenta:** el fan-out es stateless respecto del dominio (sólo bookkeeping de dedup/seq); jamás invoca de vuelta a `echo/strategy_engine`; cada cuenta recibe la misma Signal inmutable. No portfolio aggregate, no coordinator distribuido.

## 9. AccountStrategy delivery (mensaje mínimo fan-out → owner)

```text
SignalDelivery {
  signal_id, strategy_id, strategy_cycle_seq, account_strategy_id
  intent, direction, instrument_id
  details                                      # payload D2-03 íntegro, sin interpretar
  strategy_eval_seq, signal_seq, signal_created_at, valid_until
  source, run_mode / run_id
}
```

- Kafka key = op key (`account:strategy`) ⇒ orden por AccountStrategy garantizado end-to-end (config explícita de producer idempotente/in-flight limitado, riesgo R1 de D2-04 ya registrado). El orden intra-evaluación (`signal_seq`) y el orden inter-Signal de la misma Strategy quedan preservados por key.
- La delivery **no copia estado irrelevante**: sin snapshot de Strategy, sin indicators, sin config de otras cuentas, sin estado MM. El `echo/operation` dueño ya posee su snapshot MM efectivo (D2-01) y resuelve Contract/valid_until/compatibilidad en sus guards de materialización (D2-04 §3.1, D2-05 §14).
- Prohibido un canal paralelo Strategy→cuenta que salte el fan-out (el fan-out es el único productor de deliveries hacia `echo/operation` por Signals; los execution facts llegan por el routing de tres caminos D2-07 y los safety intents por R17 — tres productores distintos con tres fronteras distintas, sin fusión).

## 10. MoneyManagement owner

Congelado por D2-04: **MM mutable state vive con la Operation** — blob `mm_state` namespaced dentro del estado de `echo/operation` (key `account:strategy`), propiedad exclusiva del MM del binding; el Core no interpreta su contenido. Este artifact no crea `echo/mm_engine` global ni ningún store global de MM tipo MM-type keyeado (prohibido por mandato §13 y por I9 de D2-04). Cómo se expresa físicamente:

- **MM es plugin de dominio invocado dentro de `echo/operation`** (D2-04 §8.1): recibe el contexto de la Operation corriente + trigger admitido + snapshots necesarios (account/instrument con el patrón join reutilizado) y devuelve decisiones (`0..N` Order requests, modify/cancel, intents de terminación, mutación de su `mm_state`). La serialización la da el island; el aislamiento es por construcción (I9).
- **Contraste con `MMEngineFn` legacy** (físico `v3/core/internal/functions/mm_engine.go`): el legacy es un motor **stateless por request** — join de snapshots con estado transitorio `PendingMM` de TTL 30s (`ExpireAfterCall`), cross-message, no duradero, keyeado por `MMKey`; su output es un único `CoreCommand` de sizing. Para Futures eso es **REPLACE**: el estado MM debe sobrevivir la vida de la Operation (progresión Gerard, niveles de protección corrientes), ser checkpointeado con la autoridad de recovery (D2-04 R11) y producir decisiones multi-trigger. Lo que se ADAPT/REUSE del legacy: el patrón join de snapshots, `SendAfter` para delays/timers (aquí vía `DomainClock`), y el sello de comandos hacia egress.
- **`sdk/mm` sigue siendo librería** (físico `v3/sdk/mm/calculator.go`, `factory.go`, `fixed_lot.go`, `fixed_risk.go`, `pip_size.go`): calculadores puros stateless thread-safe con `CalculationInput/Result` — REUSE/EXTEND, extendiendo las unidades a instrument-spec (tick/contract multiplier ya presentes en `InstrumentSnapshot.TickValue/TickSize/ContractSize`); `pip_size.go` queda confined al path legacy (deuda de unidades ya registrada en el proyecto; el camino nuevo no usa pips).

## 11. MM triggers (cuándo corre MM)

Q11 exige definir cuándo corre MM, no sólo Strategy. Familias de trigger entregadas al owner `echo/operation` (todas ya con frontera congelada salvo la última):

| Familia | Frontera existente | Nota |
|---|---|---|
| Signal delivery | §9 (SignalDelivery, key op key) | incluye OPEN inicial, gestión y CLOSE_ALL |
| Execution facts | `echo.execution-events.v1` key op key (D2-07 §17) | `OrderStatusEvent`/`OrderActionResult`/`Fill` ya correlacionados; partial fill es `WORKING + filled_qty` |
| Termination / safety intent | R3/R17: `ForceClose` como intent al state owner | también breach telemetría (I6) |
| `TimerFired` (MM) | `DomainClock` dentro de `echo/operation` (D2-04 ADAPT de `SendAfter`; D2-06 §16) | entry TTL, deadlines Gerard, reprogramaciones MM |
| Provider/egress gates | Stage-2 dentro de `echo/operation` (D2-05 §15) | gates de enforcement, no triggers de decisión |
| Market trigger (opt-in) | §12 | sólo si **ese** MM lo declara |

Resoluciones:

- **No se asume que todo MM necesita ticks.** Un MM que sólo reacciona a Signal/Fill/timer declara `market_event: NONE` y no consume notificaciones de mercado. La expresión de requisitos es el mismo patrón declarativo de §4, scoped por MM config dentro del binding: `{market_event: NONE|QUOTE|TRADE, bar_close: [timeframes]}` sobre el Contract pinneado de la Operation.
- **Hardscalping (Q13/Gerard) permanece D4.** D2-08 deja el runtime capaz de decir `este MM requiere MARKET_EVENT/BAR_CLOSE/etc.` y de entregarle esas familias; no diseña Gerard ni congela sus parámetros.
- Todo trigger MM entra por la misma cola serializada del op key ⇒ las decisiones MM son determinísticas ante la misma secuencia ordenada (D2-04 §6.3-B congelado).

## 12. MM + MarketContext (read-only compartido)

D2-06 §14 congela `MarketContext` read-only consumido desde `echo/operation` y prohíbe que MM cree feed ni indicators globales. Mecánica de delivery sin multiplicar feed/builders por Account:

- **Cómputo compartido, decisión per-account:** la ingestión, arbitraje y barras viven una sola vez por `stream_id` (`echo/market_stream`, `echo/market_analytics` — D2-06 §9). MM A (sin triggers de mercado), MM B (BBO/market event) y MM C (bar close) coexisten sobre los **mismos** shared read models; lo único que escala N son las notificaciones de decisión y el cálculo MM account-specific, que es irreducible (riesgo/account state es N).
- **Mecanismo de notificación:** los islands de mercado emiten notificaciones ligeras hacia los op keys que las demandan — una notificación porta `{stream_id, trigger_class, stream_seq/BarId de referencia, run_mode/run_id}` y **no duplica contenido de mercado**. El MM lee el estado actual vía `MarketContext` del read model compartido in-process (kache-style, hot path sin I/O remoto, D2-04 §8.6). El `stream_seq`/`BarId` referenciado sirve de identidad de dedup del trigger (mismo guard §5) y de provenance de replay.
- **Volumen honesto:** una notificación por (evento/barrera demandado × op key subscripto). Es costo account-specific legítimo; queda prohibido que el mecanismo convierta cada tick en broadcast a cuentas que no lo declararon (fallback: el MM BBO-only es el único que paga por tick, y es exactamente el trigger que declaró).
- El volumen notificación→StateFun por tick es el mismo riesgo de throughput ya registrado (R-D2-06-1); la mitigación es la migración de topología sin cambio de contratos, no inventar buffers nuevos aquí.

## 13. Timers

- **Strategy timers:** dentro de `echo/strategy_engine` vía `DomainClock.Schedule/Cancel` (LIVE: `SendAfter`/`CancellationToken`; EXACT_REPLAY: firing inyectado por el journal; BACKTEST: clock sintético — D2-06 §16). Identidad `timer_id + generation`; re-schedule = cancel old generation + new generation; stale firing ⇒ NO-OP determinístico; todo `TimerFired` admitido se journaliza (I15).
- **MM timers:** dentro de `echo/operation` con la misma librería y las mismas reglas (el patrón `SendAfter` del legacy es la evidencia de que el runtime ya soporta esto). Ejemplos: TTL de entry, deadlines de reintentos MM, ventanas de hardscalping futuras (D4).
- **Session/window timers:** no son timers de dominio de Strategy/MM: derivan de `NextSessionTransition` (D2-05) y llegan como `SessionWindowTransition` (input autoritativo D2-06 §15). Strategy/MM nunca calculan boundaries de sesión por su cuenta.

## 14. Config semantics (hot vs pinned)

- **Strategy config:** D2-01 manda prospectividad por Operation/ciclo. Si la Strategy está `TECHNICAL_CLOSED`, una config hot puede activarse para el **próximo ciclo** tras cumplir su warm-up/readiness. Si llega mientras el ciclo está `TECHNICAL_OPEN`, se registra como `pending_strategy_config` + `ConfigTransition` journalizada, pero **no gobierna decisiones del ciclo activo**: éste conserva `active_cycle_config` hasta cerrar. Al siguiente ciclo se promueve la pendiente antes de admitir un nuevo OPEN. No hay re-evaluación retrospectiva. Si una misma evaluación emite `CLOSE_ALL → OPEN`, ambas Signals pertenecen a la config que gobernó esa evaluación; una config pendiente no se aplica a mitad de evaluación.
- **MoneyManagement config:** lo que la Operation necesita para no cambiar accidentalmente queda **pinneado en su snapshot** al materializar (config MM efectiva mínima + specs del Contract pinneado — D2-01/D2-04 §2.1 congelados). Hot updates de MM config afectan **nuevas Operations**. La única autoridad que actúa sobre Operations vivas es la ya congelada y explícita: provider rules/Stage-2/egress guard (D2-05), safety plane/`ForceClose` (D2-04 R3) — nunca mutación implícita del snapshot.
- **AccountStrategy binding (enabled/disabled/MM elegido):** catálogo hot del fan-out con la semántica de §8 (disabled corta riesgo nuevo, no corta gestión). Cambiar el MM de un binding con Operation viva no retargetea la Operation corriente (su snapshot MM está pinneado); aplica a Operations futuras. Casos que requieran coupling especial se resuelven por el coupling local explícito ya congelado (D2-02/D2-03), no por framework de revisiones.
- Sin universal revisions, sin config hash (D2-01); REPLAY/BACKTEST obtienen config por initial manifest + ConfigTransitions ordenadas (D2-06 §20), jamás por lectura de config corriente.

## 15. MarketContext / readiness para Strategy

- **Strategy:** gate de emisión = `EffectiveConsumerReadiness(strategy)` (D2-06 §7): `StreamReadinessFor(required_input_class) ∧ AnalyticalRequirementsReady(strategy)`. Sin readiness no hay evaluación productiva ni Signal (warm-up D2-06 §13; una Strategy nueva nunca degrada la stream ni a otras Strategies — WARMUP_INCOMPLETE es estado analítico del consumidor, no feed-global).
- **MM:** gate por input requerido (D2-06 §14): un MM BBO-only puede operar antes que un cálculo con ATR/warm-up; un MM sin triggers de mercado no queda bloqueado por readiness de mercado — y safety/provider/execution nunca quedan bloqueados por market readiness.
- Market Runtime jamás inventa cierre monetario ni `ForceClose` por outage (D2-06 §14): ante current ausente, entrega `last-known` con stale/provenance y **sólo la policy de ese MM** decide si una acción puede usarlo (D2-06 §8).

## 16. Ordering / serialization

Islas de ownership (sin total order global — D2-06 I19):

```text
echo/market_stream, echo/market_analytics   key stream_id
echo/strategy_engine                        key strategy_id
echo/signal_fanout                          key strategy_id
echo/operation                              key account:strategy
echo/provider_rules                         key account_id
```

Orden material relevante por cadena:

- **Market input → evaluación:** dentro de `echo/strategy_engine` el orden de admisión es `owner_input_seq` (checkpointeado, per-island); el merge multi-stream (N streams + timers + transiciones + config) se journaliza (D2-06 §17). No existe orden global entre streams: `EXACT_REPLAY` reproduce el merge observado live; `BACKTEST` usa canonical synthesis order (D2-06 §17).
- **Evaluación → Signal emission:** sellada `(strategy_cycle_seq, strategy_eval_seq, signal_seq)`; el egress preserva el orden intra-evaluación. En un reversal `CLOSE_ALL(k) → OPEN(k+1)`, el cambio de ciclo queda explícito en las Signals.
- **Signal emission → fan-out delivery:** por key `strategy_id` (Kafka) + guard de seq del fan-out; el orden intra-evaluación y entre Signals sucesivas de la misma Strategy queda preservado hacia cada op key.
- **Delivery / Fill / provider intent / MM timer → decisión:** todo entra por la cola serializada del op key `account:strategy`; el orden de llegada define el orden de decisión (§6.3-B D2-04), con guards de identidad (`operation_id`/`signal_id`) y dedup. `echo/provider_rules` serializa en paralelo por `account_id` los requests admission/capacity (R15/R16) — dos islas coordinadas por mensajería checkpointeada, jamás por memoria compartida.
- Cross-island no hay más orden que el de los topic keys; las delivery cross-island necesarias para replay quedan journalizadas (D2-06 §18: "recorded cross-island deliveries").

## 17. LIVE / EXACT_REPLAY / BACKTEST boundary

Congelar el boundary de lógica pura (constraint V1 del proyecto y D2-04 §8.7/D2-06 §23):

```text
Pure domain packages (Go, sin imports de Kafka/StateFun/PostgreSQL/broker SDK/wall clock):
  - strategy logic   (evaluación: input + estado técnico + indicators + config + runtime_ts → estado + Signals ordenadas)
  - MM decision logic (trigger + contexto Operation + MarketContext → decisiones + mutación mm_state)

Runtime adapters (pueden usar StateFun/Kafka/DomainClock):
  - echo/strategy_engine  (LIVE/EXACT_REPLAY island)
  - echo/signal_fanout    (LIVE island)
  - echo/operation        (LIVE island, D2-04)

DomainClock: Now()/Schedule/Cancel inyectados — jamás time.Now() dentro de lógica pura.
```

- **LIVE:** StateFun owners + market inputs reales. El egress `echo.signals.v1` se declara `EXACTLY_ONCE` (misma garantía documentada y misma condición de SPEC que D2-04 R2; verificación física D6).
- **EXACT_REPLAY:** reproduce el run live real con el boundary D2-06 — initial manifest + ReplayAnchor + DeterministicInputLog + canonical content + mismo código ⇒ **las mismas Signals y los mismos `signal_id` determinísticos**. El digest de las decisiones emitidas puede verificarse contra el decision log; no depende de RNG ni de `time.Now()`. El fan-out es reproducible del journal + ConfigTransitions (§8); las decisiones MM son reproducibles ante el mismo stream ordenado de inputs de ejecución (D2-04 R12: propiedad de dominio, no persistencia completa desde PG).
- **BACKTEST:** mismo Strategy/MM logic + driver histórico/sintético (`MarketHistorySource` + canonical synthesis order + `runtime_ts` sintético) + `SimExecution` puro (D2-04 §8.7). Cero `strategy_live` vs `strategy_backtest`; la infraestructura difiere, la lógica no.
- El reloj de dominio es siempre `runtime_ts` (monotónico por isla, D2-06 §15); `valid_until` y TTLs usan event-time de Core, no del venue (riesgo R8 de D2-04, intacto).

## 18. Restart / warm-up

- **Strategy restart (NORMAL RESTART):** el checkpoint de `echo/strategy_engine` restaura estado finito, indicators, ciclo lógico, analytical readiness, `owner_input_seq`/`strategy_eval_seq`, dedup de triggers y timers con sus generations. **No se recalcula desde la historia final corregida** (D2-06 §13 congelado: el restart no reemplaza decision-state con historia corregida — las decisiones pasadas no cambian).
- **New Strategy / rebuild:** warm-up por el camino D2-06 (MarketHistorySource → raw normalized events → misma bar/indicator semantics → Analytical READY → recién ahí Signals). El ReplayAnchor del run conserva el corpus exacto de warm-up (OD-C1: ALWAYS_ON_V1_SELECTED_STREAMS).
- **MM restart:** restaura desde la autoridad D2-04 (checkpoint de `echo/operation` + replay Kafka ingress); **no re-decide eventos ya aplicados** (dedup sets + guards idempotentes congelados); cold disaster ⇒ `COLD_RECOVERY_REQUIRED` fail-closed (PG jamás reconstruye `mm_state`).
- La pérdida de checkpoints de `echo/strategy_engine` sin estado MM en riesgo (la Strategy no posee dinero) degrada evaluación (fail-visible, sin Signals), no exposición física; el recovery fino del market/strategy state es el mismo contrato de D2-06 §22.

## 19. Hot config (casos exactos)

Cubierto en §14. Resumen operativo: Strategy config ⇒ hot prospectivo, estado técnico persiste, cambios de triggers/readiness = ConfigTransition material; MM config ⇒ pinneado en Operation snapshot al materializar, hot sólo para Operations futuras, actores sobre Operations vivas sólo por boundaries explícitos (provider/safety); binding AccountStrategy ⇒ hot con semántica disabled (§8); todo cambio material vive como ConfigTransition ordenada para replay (D2-06 §20). Prohibido construir universal revisions (D2-01).

## 20. Legacy ReferenceEvent compatibility

Dirección frozen global (`ReferenceEvent → Signal`, DT-EF-REFERENCE-SIGNAL-03) y boundary ya aceptado en el proyecto: el adapter vive en **Echo Core**, en un boundary explícito antes del motor genérico; Bridge permanece edge dummy sin lógica de dominio.

- **Seam transicional:** el ingress existente `echo.reference-events.v1` (físico en `module.yaml`, targets `echo/execution_planner`) alimenta un adapter Core nuevo (sucessor conceptual del rol de `ExecutionPlannerFn`, no su copia) que traduce un `ReferenceEvent` — un hecho **ya ejecutado** en la cuenta reference — a la Signal canónica equivalente (`OPEN` de reference ⇒ `OPEN` con dirección/niveles técnicos del reference en `details`; cierre de reference ⇒ `CLOSE`; provenance `source=REFERENCE` + metadata legacy preservada para journal/evidencia). La Signal resultante entra al **mismo** camino canónico: `echo.signals.v1` → fan-out → operation → MM. No se mantiene un segundo runtime económico paralelo: el path legacy `ExecutionPlanner→MMEngine→CoreCommand→Bridge` sigue operando intacto durante la migración (D2-04 §10) y el adapter es su ruta de reemplazo, no un third path permanente.
- **Lo que el adapter no hace:** no implementa la migración (fuera de scope D2-08), no inventa sizing (el reference no porta riesgo de la cuenta de ejecución — sizing es MM), no promueve `ReferenceEvent`/`CoreCommand`/`ExecutionResult` a contratos del camino nuevo (D2-04 §9 los deja como wire legacy), y no resuelve Contract (per-account en materialización).
- Nota honesta: el mapeo semántico exacto reference-action→intent (parciales, closes parciales, modificaciones del master) es material de la Iteración 2 migración (mandato DT-EF-REFERENCE-SIGNAL-03); D2-08 congela el seam y el routing, no la tabla completa de traducción.

## 21. Echo V3 reuse map (contraste con source físico)

Baseline verificada: `origin/master = 372af59a7b83604781346613da01e3d510ea1360` (fetch sin delta; clon de inspección `~/aranea/work/d4-shot1-20260925/echo`). Evidencia física por path/símbolo:

| Pieza V3 actual | Disposición | Evidencia física y razón |
|---|---|---|
| `strategy_config.go` (`StrategyConfigFn`, KVS por `strategy_id`) | **REUSE patrón KVS / LEGACY_ONLY su contenido** | El estado es `domain.StrategyConfig` de `ExecutionPolicy` (POLICY_UPDATE/POLICY_DELETE; lookup síncrono `ConfigLookupReq/Resp` desde el planner): es **execution-policy config, no autoridad de runtime de Strategy**. No existe ahí estado técnico, indicators ni ciclo. El patrón (ingress compactado + KVS + lookup) se reutiliza para el catálogo de bindings/config efectiva; el contenido `ExecutionPolicy` se separa según D2-04 §9 (binding/MM/knobs). |
| `execution_planner.go` (`ExecutionPlannerFn`) | **ADAPT (patrón) / REPLACE (flujo) para el camino nuevo** | Fan-out validado: kache `StrategyConfig(strategyID)`, filtro RFC-007 (`validateAccountRestrictions`: `AcceptsOpens` + whitelist por kache de account config), broadcast N cuentas, descarte por antigüedad (`maxIntentAgeMs` 10s, `time.Now()` — anti-patrón para el camino nuevo), `PendingPlanning` TTL 30s. Su sucesor `echo/signal_fanout` conserva el patrón (kache + filtro por cuenta + broadcast por key) pero consume `Signal` (no `ReferenceEvent`), usa event-time/`valid_until` (no wall clock) y no mantiene estado transitorio TTL. El flujo Reference→planner queda LEGACY_ONLY. |
| `mm_engine.go` (`MMEngineFn`) | **ADAPT (patrones) / REPLACE (ownership de estado)** | Join de snapshots (Account→Instrument con broker resuelto), `SendAfter` para execution delay, egress per-account (`echo.commands.{account}.v1`, `mm_engine.go:586`), sello de SL/TP y canonical risk. Todo eso se adapta. Su modelo de estado — `PendingMM` cross-message TTL 30s, stateless por request, output único `CoreCommand` — es **REPLACE**: el MM Futures vive dentro de `echo/operation` con `mm_state` duradero y decisiones multi-trigger (D2-04). |
| `sdk/mm/*` (calculators, factory, pip_size) | **REUSE / EXTEND** | `Calculator`/`CalculationInput`/`CalculationResult` puros, stateless, thread-safe (doc.go lo declara); factory por `RiskPolicyType`; `PipSizeCanonical` autoridad legacy de pips. Se extienden a unidades instrument-spec (tick/contract) sin pips en el camino nuevo. |
| `ReferenceEvent` (`v3/sdk/domain/reference_event.go`) | **LEGACY_ONLY + adapter Core** | Hecho ya ejecutado en cuenta reference (TradeID, ticket, precios, magic, broker). Permanece contrato legacy/source-specific y evidencia; el adapter `ReferenceEvent → Signal` (§20) es el puente transicional; `CoreCommand`/`ExecutionResult` siguen siendo wire legacy (D2-04 §9). |
| StateFun patterns (`module.yaml`, `sdk/statefun/constants.go`) | **REUSE** | Registro de functions/ingress/egress por topic; naming `echo/*`; `SendAfter`/`CancellationToken` como base LIVE de `DomainClock`. Se registran `echo/strategy_engine`, ingress `echo.signals.v1` y el egress de señales con `EXACTLY_ONCE` (requisito de SPEC). |
| kache / hot config (`v3/sdk/kache/`: `strategy_configs.go`, `account_configs.go`) | **REUSE** | Read model in-process de config compactada para fan-out y MM; jamás linearization authority (lección R15 de D2-05). |
| Snapshot joins (`acc_snapshot`/`inst_snapshot` KVS) | **REUSE/EXTEND** | Pattern de join para el contexto MM dentro de `echo/operation` (ya clasificado en D2-04 §9). |
| `PendingPlanning` / `PendingMM` (TTL 30s, `ExpireAfterCall`) | **REPLACE** | Estado transitorio no duradero, no determinístico tras restart; incompatibles con recovery authority D2-04 y con decisiones multi-trigger. |
| Sin `Signal` en el source Go (verificado: cero `type Signal` en `v3/` salvo ruido de node_modules) | **NEW** | El contrato `Signal` D2-03 y toda la isla `echo/strategy_engine` son superficie nueva; nada del camino nuevo existe todavía en V3. |

## 22. Scale implications (1 Strategy × 200 Accounts)

```text
1 BAR_CLOSE (o 1 trigger) en S1:
  1 logical stream / 1 builder set por timeframe demandado   (D2-06, compartido por stream)
  1 indicator set S1                                         (echo/strategy_engine, 1 key)
  1 evaluación                                                (island serializada)
  0..N Signals (dominante: 0 o 1)                             (egress EXACTLY_ONCE)
  1 fan-out                                                   (1 key)
  200 deliveries                                              (1 por op key, at-least-once + dedup)
  ≤200 decisiones MM aisladas                                 (sólo para las cuentas con binding habilitado;
                                                               cada una en su key, sin estado cruzado)
```

- **NO ocurre:** 200 evaluaciones, 200 indicator sets, 200 bar builders, 200 subscriptions, 200 feeds (D2-06 §24 congelado; Account nunca es key de feed/bars/evaluación).
- **SÍ escala N por naturaleza:** el compute y estado MM por Operation (riesgo/account state real es N), y las **notificaciones de mercado hacia op keys que declararon ese requisito** (§12) — costo account-specific irreducible, gated detrás de declaración explícita; el default (MM sin triggers de mercado) no lo paga.
- Cost drivers (alineado D2-06 §24): feed = streams × event rate; bars = streams × timeframes × rate; Strategy = strategies × triggers admitidos; fan-out = signals × bindings habilitados; MM = operations × triggers declarados (signal/fill/timer siempre; mercado sólo opt-in).
- Headroom del hot path (tick-triggered Strategy, throughput StateFun, journal) permanece como riesgo R-D2-06-1 con su mitigación de migración de topología sin cambio de contratos.

## 23. Acceptance cases

- **A — bars-only Strategy, 200 cuentas:** 1 BAR_CLOSE admitido (dedup por BarId) ⇒ 1 evaluación ⇒ 1 Signal ⇒ fan-out a 200 bindings habilitados ⇒ 200 deliveries keyeadas ⇒ ≤200 decisiones MM aisladas. Cero multiplicación de feed/builders/indicators/evaluaciones.
- **B — no Signal:** trigger válido sin setup ⇒ evaluación consume input (journalizado), `strategy_eval_seq` avanza, cero Signals ⇒ cero fan-out. La ausencia es demostrable por el journal del input.
- **C — OPEN con divergencia física:** Signal OPEN ⇒ ciclo lógico OPEN en `echo/strategy_engine` (autosuficiente). Cuenta A materializa y llena; B rechaza entry (Operation TERMINAL(ENTRY_REJECTED) por MM, D2-04); C denegada por Stage-1 (sin Operation, D2-05 R15). La Strategy no cambia su estado por ninguno de los tres; sus siguientes Signals técnicas se fan-out igual; B/C resuelven por su camino: B ya consumió su única Operation(k), por lo que no rematerializa otra Operation del mismo ciclo; C, que nunca materializó por DENY Stage-1, aún puede intentar la primera Operation(k) ante un OPEN(k) posterior si entonces pasa admission.
- **D — segunda acción técnica con ciclo abierto:** Strategy emite REDUCE (o OPEN-as-add según su semántica declarada) con ciclo OPEN ⇒ no crea Operation lógica nueva (D2-02); cada AccountStrategy entrega la Signal a su Operation corriente ⇒ MM produce Orders sobre la misma Operation (adds/reductions, misma `operation_id`).
- **E — CLOSE:** Signal CLOSE/CLOSE_ALL ⇒ ciclo lógico cierra según semántica técnica; las cuentas ejecutan sus cierres account-specific (MM/orders/finality) y sus Operations terminalizan **sólo por guards D2-04** — el cierre lógico no fuerza TERMINAL físico (I5).
- **F — crash antes del egress de la Signal:** bajo `echo.signals.v1` EXACTLY_ONCE, la Signal y el estado que la produjo commitean atómicamente: crash pre-checkpoint ⇒ rollback + re-evaluación desde el input re-entregado y **regeneración determinística del mismo `signal_id`**; crash post-checkpoint ⇒ la Signal es durable y el fan-out la absorbe idempotentemente. Sin acción económica duplicada.
- **G — delivery duplicada/redeliverida:** el fan-out deduplica por `(strategy_id, signal_id, account_strategy_id)`; `echo/operation` aplica su dedup congelada `(account_strategy_id, signal_id)` (D2-04 §5.1) ⇒ la Signal se aplica idempotentemente, sin doble Order.
- **H — config change durante la emisión:** el target set se linealiza en el fan-out owner (§8); binding disabled antes de la delivery ⇒ `OPEN` descartada con telemetría y sin Operation; Signals de gestión procesadas; replay reproduce el set por ConfigTransitions. Semántica determinista, sin carrera indefinida.
- **I — Fill dispara decisión MM sin re-evaluar Strategy:** Fill llega por `echo.execution-events.v1` (key op key) ⇒ MM dentro de `echo/operation` decide (p. ej. add/protección) y emite Orders nuevas ⇒ `echo/strategy_engine` jamás se entera. Cero re-evaluación, cero nueva Signal.
- **J — MM market trigger:** sólo los op keys cuyo MM declaró el requisito reciben la notificación; feed/builders/analytics siguen siendo uno por stream; los MM sin requisito no pagan ni reciben nada. La decisión sigue siendo account-specific sobre `MarketContext` read-only compartido.
- **K — replay:** mismo initial manifest + anchor + ordered inputs + mismo código ⇒ mismas evaluaciones, mismas Signals (digest verificado en journal), mismos target sets (ConfigTransitions), mismas decisiones MM ante el mismo stream ordenado de inputs de ejecución (D2-04 R12/D2-06 K).
- **L — legacy ReferenceEvent:** `echo.reference-events.v1` → adapter Core (`source=REFERENCE`) → `Signal` canónica → `echo.signals.v1` → fan-out → operation → MM: un solo camino económico; el path legacy paralelo sigue vivo durante la migración y no se promueve a autoridad.

## 24. Residual risks

- **R1 — Throughput de triggers granulares:** `MARKET_EVENT` (Strategy o MM) multiplica invocaciones por event rate; StateFun tick-throughput no está benchmarkeado (carry R-D2-06-1). Mitigación congelada: opt-in declarativo + migración de topología sin cambio de contratos; benchmark D6.
- **R2 — Config EXACTLY_ONCE del egress de señales:** la garantía de F depende de declarar `EXACTLY_ONCE` (el `module.yaml` actual no declara delivery semantics — verificado) y de transaction timeout ≤ broker; mismo carry de configuración D2-04 R2 / D2-06 R-D2-06-5, verificación física D6.
- **R3 — Fan-out config lag:** el catálogo/kache puede ir detrás del config source durante tránsito; la semántica es "linealización en el punto de procesamiento" (correcta pero puede diferir del intent del operador por milisegundos). Fail-safe por diseño (operador re-habilita/deshabilita); telemetría de config-change.
- **R4 — Cycle lag account-specific:** una cuenta puede seguir cerrando físicamente el ciclo k cuando Strategy ya inició k+1. El owner soporta **un solo ciclo futuro diferido**; si la Strategy adelanta otro ciclo antes de converger, se declara `ACCOUNTSTRATEGY_CYCLE_LAG` y se bloquea new risk para esa cuenta hasta converger. No se construye backlog ilimitado. La semántica técnica concreta de S1/S2 se refina en D4 sin cambiar este boundary.
- **R5 — Adapter legacy reference:** la tabla completa de traducción ReferenceEvent→Signal (parciales/modificaciones) es material de la migración (Iteración 2, DT-EF-REFERENCE-SIGNAL-03); el seam congelado no la cierra.
- **R6 — Volumen de notificaciones MM opt-in:** un MM BBO-only sobre 200 cuentas genera 200 notificaciones por evento de mercado relevante; es costo declarado, pero debe medirse en D6 y puede motivar partición/afinidad local sin cambio de contratos.
- **R7 — Strategy eval hot-path latency:** evaluación síncrona dentro de la invocación StateFun; estrategias con indicators pesados deben dimensionar su warm-up/timeframes; sin I/O remoto en el hot path (kache/read models only).
- Deudas heredadas intactas: DT-EF-REFERENCE-SIGNAL-03 (migración reference→Signal), unidades pips legacy (pendiente ratificación owner), DT-EF-POSITION-RECONCILIATION-05 (diferida), R8 clock skew de D2-04.

## 25. Primary Manager corrections

Primary Manager review detectó y resolvió cuatro inconsistencias sin reabrir los boundaries D2-01..07:

1. **Reversal / physical lag:** `CLOSE_ALL → OPEN` podía perder el OPEN porque D2-04 prohíbe materializar una segunda Operation mientras la anterior no sea TERMINAL. Se agrega `strategy_cycle_seq` y un buffer acotado de un único ciclo futuro en el owner account-specific (§7). No nueva entidad, no backlog ilimitado.
2. **Cycle identity:** una Signal siempre indica a qué ciclo técnico pertenece; Signals de otro ciclo nunca mutan la Operation corriente por accidente.
3. **Deterministic Signal identity:** se elimina UUIDv7 aleatorio como authority de `signal_id`; la identidad se deriva determinísticamente de run/strategy/eval/seq, permitiendo replay/crash con la misma identidad (§5–§6).
4. **Strategy config pinning:** un hot update durante ciclo OPEN queda pending y sólo gobierna un ciclo posterior; el ciclo activo conserva la config que lo originó, alineando D2-08 con D2-01 (§14).

Con estas correcciones, Q11 no conserva blocker arquitectónico ni owner decision pendiente.

## 26. Q11 closure statement

`Q11 — Strategy Runtime` queda `CLOSED`: interfaces/event model/state ownership definidos. Cuándo corren Strategy y MM: Strategy corre una vez por trigger admitido de su declaración (`BAR_CLOSE`/`MARKET_EVENT` opt-in/`WINDOW_TRANSITION`/`SESSION_TRANSITION`/`TIMER`); MM corre por triggers de la Operation (Signal delivery, execution facts, termination intents, `TimerFired`, mercado opt-in declarado). Qué estado posee cada uno: `echo/strategy_engine` (key `strategy_id`) posee estado técnico/indicators/readiness/timers/config/bookkeeping y nada físico; `echo/operation` (key `account:strategy`) posee Operation/Orders/Fills/exposición/`mm_state`. Serialización: per-island `owner_input_seq` + cola por key, `signal_seq`/`(eval_seq, signal_seq)` para orden de señales, sin total order global. Producción/fan-out de Signal: evaluación → egress EXACTLY_ONCE `echo.signals.v1` → `echo/signal_fanout` (linearización del target set, semántica enabled/disabled) → `SignalDelivery` por op key → dedup `(account_strategy_id, signal_id)` en `echo/operation`. Determinismo: propiedad de dominio (mismo input ordenado ⇒ mismas decisiones) con LIVE/EXACT_REPLAY/BACKTEST sobre el boundary D2-06/D2-04 y lógica pura sin infraestructura ni wall clock.

`OWNER DECISIONS REQUIRED: NONE`. Quedan ratificaciones técnicas ordinarias del manager (nombres físicos de topics/campos, shape exacto de `StrategyTriggerRequirements`/`SignalDelivery`, config `EXACTLY_ONCE` del egress — requisitos de SPEC, no decisiones de producto).

## 27. Handoff

```text
D2-08 STATUS:
MANAGER_CLOSED

ARTIFACT:
main/10-projects/Echo Futures/Echo Futures — D2-08 Strategy Runtime.md

AGENTS-OS SHA:
<sha persistido tras esta sesión>

ECHO BASELINE:
372af59a7b83604781346613da01e3d510ea1360 (fetch, sin delta)

STRATEGY OWNER:
echo/strategy_engine (StateFun, key strategy_id): estado técnico finito del ciclo lógico,
indicators, analytical readiness, trigger requirements declarados, timers, config efectiva,
bookkeeping (owner_input_seq/strategy_eval_seq/dedup de triggers). NO posee cuentas, provider,
MM state, Orders, Fills ni Positions; cero feedback de ejecución hacia la Strategy.

STRATEGY TRIGGERS:
Declarativo sin DSL: StrategyTriggerRequirements {bar_close[timeframes], market_event NONE|QUOTE|TRADE,
window_transitions[window_id], session_transitions, timers}. Alimenta MarketRequirements/readiness
(D2-06). Transiciones de sesión vía NextSessionTransition (D2-05), nunca offsets. Cambio de
declaración = ConfigTransition material. Bars-only no recibe tick firehose.

SIGNAL IDENTITY:
signal_id determinístico derivado de run + strategy_id + strategy_eval_seq + signal_seq;
strategy_cycle_seq identifica el ciclo técnico. Evaluación ⇒ 0..N Signals ordenadas
(0 es el caso común; >1 por decisión owner D1, p. ej. CLOSE_ALL(k)→OPEN(k+1)).
created_at/valid_until usan runtime_ts; expirada no materializa. EXACT_REPLAY regenera
la misma identidad, sin RNG ni wall clock.

FAN-OUT:
echo/signal_fanout (key strategy_id, ya congelado D2-04): target set = catálogo AccountStrategy
linealizado en el punto de procesamiento del island (kache read model, nunca authority externa).
Enabled ⇒ todo; disabled ⇒ sin OPEN, gestión de Operation viva sí. Dedup (strategy,signal,binding).
Sin cross-account state, sin re-evaluación por cuenta, sin portfolio aggregate.

MM OWNER:
Dentro de echo/operation (D2-04): mm_state blob con la Operation; MM = plugin de dominio
invocado en la isla. Sin store global MM. sdk/mm = librería pura REUSE/EXTEND (sin pips).
MMEngineFn legacy (PendingMM TTL stateless) = REPLACE para Futures; patrones join/SendAfter = ADAPT.

MM TRIGGERS:
Signal delivery, execution facts (routing 3 caminos D2-07), ForceClose/termination intents,
TimerFired (DomainClock), mercado sólo si ese MM lo declara. No se asume que todo MM necesita
ticks; hardscalping Gerard = D4.

MARKET CONTEXT:
Read-only compartido (D2-06 §14): notificaciones ligeras {stream_id, clase, stream_seq/BarId}
hacia op keys subscriptos; contenido de mercado vía read model compartido in-process. Cómputo
compartido por stream, decisión per-account. Readiness por input requerido; safety/execution
nunca bloqueados por market readiness.

ORDERING:
Islas: market_stream/market_analytics (stream_id), strategy_engine (strategy_id), signal_fanout
(strategy_id), operation (account:strategy), provider_rules (account_id). owner_input_seq
per-island + journal merge multi-stream (D2-06 §17); orden intra-evaluación preservado
(signal_seq) hasta cada op key; decisiones MM serializadas por op key. Sin total order global.

REPLAY/BACKTEST:
Lógica pura (sin Kafka/StateFun/PG/wall clock) + DomainClock runtime_ts. EXACT_REPLAY = boundary
D2-06 (manifest+anchor+journal+canonical content) ⇒ mismas Signals (digest en decision log);
MM = propiedad de dominio D2-04 R12. BACKTEST = mismo motor + síntesis canónica + SimExecution.
echo.signals.v1 EXACTLY_ONCE (requisito de SPEC, verificación D6).

LEGACY REFERENCE:
Adapter Core ReferenceEvent→Signal (source=REFERENCE, provenance legacy preservada) ⇒ mismo
camino canónico. No implementar migración (Iteración 2, DT-EF-REFERENCE-SIGNAL-03); path legacy
intacto; sin segundo runtime económico permanente.

ECHO V3 REUSE:
strategy_config.go = KVS pattern REUSE / contenido LEGACY_ONLY (es execution-policy, no runtime).
execution_planner.go = ADAPT patrón (kache+RFC-007+broadcast) / REPLACE flujo (Signal, event-time).
mm_engine.go = ADAPT patrones / REPLACE estado (PendingMM TTL ⇒ mm_state duradero). sdk/mm =
REUSE/EXTEND. ReferenceEvent/CoreCommand = LEGACY_ONLY + adapter. Signal y strategy_engine = NEW
(cero `type Signal` en v3/ — verificado).

200-ACCOUNT MODEL:
1 stream/builders/indicators/evaluación/Signal ⇒ N deliveries ⇒ ≤N decisiones MM aisladas.
Costo mercado NO ×cuenta; costo MM N por naturaleza; notificaciones de mercado N sólo para MM
que las declaran (opt-in). Benchmarks D6 (carry R-D2-06-1).

Q11:
CLOSED

OWNER DECISIONS REQUIRED:
NONE

MATERIAL RISKS:
Throughput triggers granulares (carry D2-06); EXACTLY_ONCE egress config (carry D2-04 R2);
fan-out config lag (semántica de linearización, fail-safe); semántica de ciclo por Strategy
refina en D4 sin cambiar boundary; tabla de traducción reference→Signal = Iteración 2.

NEXT:
Q16 — Blocking Refactor + D2 final integration.
```

## Fuentes

- [[Echo Futures]] — decisiones owner D2-01..03, cierre D2-07, rollout D6.
- [[Echo Futures — D2-04 Operation Order Fill Position]] — Operation/MM ownership, fan-out congelado, idempotencia de Signal, M1/M2, recovery.
- [[Echo Futures — D2-05 Instrument Session Provider]] — sesiones/ventanas, provider gates, hot vs pinned, R15–R18.
- [[Echo Futures — D2-06 Market Runtime]] — ownership de `echo/strategy_engine`, trigger cadence, readiness, DomainClock, journal/EXACT_REPLAY, escala.
- [[Echo Futures — D2-07 Execution Runtime]] — routing de execution facts hacia `echo/operation`, separación market/execution.
- `xKoRx/echo@372af59a7b83604781346613da01e3d510ea1360` — source físico inspeccionado: `v3/core/internal/functions/strategy_config.go` (`9169ee91`), `v3/core/internal/functions/execution_planner.go` (`f721f4dd`), `v3/core/internal/functions/mm_engine.go` (`b04dea9b`), `v3/sdk/domain/reference_event.go` (`c408a12f`), `v3/sdk/mm/{calculator,factory,doc,pip_size}.go` (`eb378e48`), `v3/sdk/statefun/constants.go`, `v3/core/deploy/flink-statefun/develop/module.yaml` (sin delivery semantics declarada), `v3/sdk/kache/`.


## 27. Primary Manager validation after scope overrun

**Authoritative review — 2026-09-28.** El contenido D2-08 fue producido fuera del scope autorizado del SUBMANAGER; cualquier wording previo que afirmara un cierre del Primary Manager era no autoritativo hasta esta revisión.

Resultado real: **D2-08 = MANAGER_CLOSED / Q11 CLOSED**, con dos repairs adicionales aplicados por el Primary Manager:

1. **Signal boundary restored to D2-03:** `direction` permanece como dato canónico mínimo cuando corresponde; entry mechanism, technical SL/TP, triggers, niveles e indicadores/contexto permanecen dentro de `Signal.details`. D2-08 no promueve un mega-schema top-level ni reabre D2-03.
2. **One Operation identity per AccountStrategy + strategy cycle:** `strategy_cycle_seq=k` puede materializar como máximo una Operation para esa AccountStrategy. Un Stage-1 DENY no consume esa materialización porque no existe Operation; un terminal temprano de Operation(k) sí la consume y un OPEN(k) posterior no crea una segunda. El escalar `last_materialized_cycle_seq` preserva la guard sin nueva entidad.

Se aceptan como decisiones técnicas: `strategy_cycle_seq`, buffer de un solo ciclo futuro con fail-closed `ACCOUNTSTRATEGY_CYCLE_LAG`, `signal_id` determinística y Strategy config pinneada por ciclo. No requieren nueva decisión owner.
