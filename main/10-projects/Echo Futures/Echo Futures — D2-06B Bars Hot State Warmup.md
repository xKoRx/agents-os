---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo Futures]]"
  - "[[Echo Futures — D2-06A Market Feed Authority]]"
  - "[[Echo Futures — D2-05 Instrument Session Provider]]"
  - "[[Echo Futures — D2-04 Operation Order Fill Position]]"
  - "[[Echo Futures — D1 Analysis Pack]]"
aliases:
  - Echo Futures D2-06B
  - EF Bars Hot State Warmup
tags:
  - kind/doc
  - area/echo
  - echo-futures
  - architecture-design
created: "2026-09-27"
updated: "2026-09-27"
---

# Echo Futures — D2-06B Bars / MTF / Hot State / Indicators / Warm-up

> [!info]+ TOP worker B — D2-06
> Deliverable del worker B del bloque D2-06 (Market Runtime). Consumes congelados: [[Echo Futures — D2-06A Market Feed Authority]] (`ACCEPTED_FOR_INTEGRATION` post-repair R1 — SUBMANAGER; sus contratos son INPUT congelado para B, no se edita), [[Echo Futures — D2-05 Instrument Session Provider]] (CLOSED), [[Echo Futures — D2-04 Operation Order Fill Position]] (CLOSED), [[Echo Futures]] D2-01..03 y [[Echo Futures — D1 Analysis Pack]] Fronts B/B2/E. Baseline Echo verificada físicamente en ventana: `origin/master = 372af59a7b83604781346613da01e3d510ea1360` (fetch, HEAD==remota; clon `~/aranea/work/d4-shot1-20260925/echo`, lectura por `git show 372af59a:<path>`). Sin auditoría física general (el SUBMANAGER ya verificó los patterns sobre esa baseline): sólo se inspeccionaron los patterns estrictamente necesarios (ValueSpec/storage, SendAfter, KafkaEgressBuilder, kache, module.yaml, ausencia de bars/indicators/StrategyEngine). Este artefacto NO implementa código, NO cierra D2-06 global, NO avanza D2-06C (sólo deja requirements), NO selecciona execution transport, NO diseña el backtester completo y NO reabre A/D2-04/D2-05. Incorpora el **Manager Repair — D2-06B-R1** (R1–R6 + simplificación de la política de corrección), aplicado quirúrgicamente sobre el candidato original; el documento completo refleja ya el modelo reparado, no erratas acumuladas.

## Manager Repair — D2-06B-R1

El SUBMANAGER devolvió el candidato con seis defects (R1–R6) y una simplificación de política. Este repair es targeted: no reabre A/D2-04/D2-05, no implementa código, no avanza D2-06C/D2-07. Resolución:

- **R1 — Downstream idempotency obligatoria.** El egreso canónico de A es AT_LEAST_ONCE y `stream_seq` es el token de idempotencia downstream: B lo convierte en guard congelado. `echo/market_analytics` y `echo/strategy_engine` mantienen `last_applied_stream_seq(stream)` en su keyed state checkpointeada y toda mutación (latest state materializado, forming, volume, trade_count, triggers de cierre/evaluación) corre después del guard: `seq ≤ last_applied ⇒ NO-OP` contado en telemetría. El guard es correcto porque el topic es keyeado por `stream_id` (orden por stream preservado) y A asigna `stream_seq` contiguo post-dedup jamás renumerado ⇒ todo redelivery lleva seq ≤ last_applied. Tras restore, guard y estado que protege vuelven en la misma frontera de checkpoint; el replay re-entrega y los no-ops absorben el solape — misma propiedad de dominio D2-04 R5/R11, sin dedup DB ni autoridad nueva. Los closures entregados a strategies llevan su propio guard por identidad de closure (§22). (§2/§5/§8/§22/§25)
- **R2 — Latest market state no regresa.** Separados EVENT RECEIVED/LIVENESS de CURRENT MARKET STATE. Un evento tardío sigue existiendo íntegro (entra a la política late de barras, a métricas, prueba liveness y participa del recovery según capability) pero `last_trade`/`last_quote` son **escaleras monótonas** por `(event_ts, stream_seq)` (escaleras independientes quote/trade) y `last_event_ts` es máximo monotónico: el ejemplo del defecto — trade 10:00:02 @20001 seguido de trade 09:59:58 @19980 — deja `last_trade=20001`. `receive_ts` sigue fuera de la semántica de mercado. Si un source no permite ordenar current-state de forma fiable (`reliable_ts=RECEIVE_ONLY`), la limitación se declara por capability/readiness y queda visible, no escondida. (§5)
- **R3 — Market bar projection ≠ decision observation.** La barra corregida (X→X') pertenece a la PROYECCIÓN; la evaluación disparada por el cierre observó exactamente X y ese hecho es inmutable: sin Signal retrospectiva, sin reescritura de qué snapshot observó cada evaluación. Se elimina la afirmación falsa de que una historia genérica event-time-sorted reconstruye automáticamente el finite state exacto de una sesión live con efectos de late-arrival. Autoridades de recovery congeladas: **NORMAL RESTART** restaura el decision state de Strategy desde checkpoint StateFun (las barras pueden reconstruirse independientemente; jamás se sustituye silenciosamente el estado checkpointeado por un warm-up "más corregido"); **NEW RUN / NEW STRATEGY** construye estado inicial por warm-up (no existe decision history live que preservar); **LOSS OF REQUIRED CHECKPOINT / COLD DISASTER** ⇒ fail-closed `COLD_RECOVERY_REQUIRED` (autoridad D2-04 R11) o el recorded deterministic boundary que D2-06C diseñará — sin claim de continuación exacta desde vendor history; **EXACT REPLAY** queda como requisito de D2-06C: preservar el orden/inputs que reproduzca exactamente los BAR_CLOSE snapshots que la Strategy observó. (§9/§10/§15/§17/§19/§24)
- **late-correction simplification:** `bars.late_correction ON|OFF` desaparece como hot config. La semántica que afecta decisiones es única V1 y run-pinned: un flag que cambia semántica no puede mutar silenciosamente durante un run. La corrección queda como propiedad de la market projection; las decision observations ya emitidas son facts inmutables conceptualmente. (§9)
- **R4 — Rebuild cutover capability-driven.** `R` sobrevive como nombre conceptual del cutover, NO como "último event_ts" universal. Clases A/B: identidad/cursor/posición canónica demostrable del source, con dedup por identidad en el seam. Clase C: boundary/cursor garantizado por el history/live source, o pausa/cutover con buffer controlado que produzca dos regiones realmente disjuntas, o snapshot replacement cuando la semántica alcance, o full rebuild, o `ANALYTICAL_REBUILD_UNPROVABLE` fail-closed. **Prohibido** dropear un evento live sólo porque `event_ts < R` asumiendo que la historia lo contiene: no se sacrifica un evento físico por un stitch cómodo. (§18/§19)
- **R5 — El BREAK interno no reinicia el grid.** El grid de cada timeframe queda anclado a `session_open` durante TODA la sesión (el BREAK interno vive dentro de la MISMA `ExchangeSession`, D2-05). En `break_start` la forming se trunca; durante BREAK no se construyen barras; en `break_end` se retoma el MISMO grid: si `break_end` cae dentro de un bucket nominal existe una barra corta `[break_end, próximo boundary nominal)`; los boundaries futuros jamás se desplazan. Grid nuevo sólo con nueva `session_open` (hueco ENTRE sesiones); early close trunca y termina. Acceptance S nuevo. (§6/§7/§8)
- **R6 — Disponibilidad stale ≠ READY.** MarketContext separa availability (existe last-known + `as_of` + stale flag) de quality/readiness (autoridad A). Feed down con last BBO ⇒ `available=true, stream_ready=false, as_of/stale visible`; MM decide por POLICY si ESA acción usa el last-known — la disponibilidad jamás eleva readiness. Strategies no producen nuevas technical Signals desde un stream NOT_READY salvo semántica futura explícita; el path safety/provider/execution sigue independiente; Market Runtime no inventa flatten (A §15.6). (§3/§23/§24)
- **Acceptance additions:** O (redelivery), P (late no regresa), Q (decisión live vs barra corregida), R (rebuild clase C), S (grid con break interno), T (BBO stale) — §30.
- `OWNER_DECISIONS_REQUIRED = NONE`.

## Manager Repair — D2-06B-R2

El SUBMANAGER devolvió el candidato post-R1 con un único defect restante (R7). Este repair es targeted: no reabre A/D2-04/D2-05 ni R1–R6, no implementa código, no avanza D2-06C/D2-07. Resolución:

- **R7 — Current market state scoped por authority_epoch.** A congela `stream_id = (instrument_id, contract_id)` estable ante switch con `authority_epoch++` (A §3: el epoch también incrementa en recovery que invalida continuidad), de modo que dos autoridades distintas pueden servir sucesivamente la MISMA stream lógica. La monotonía de current-state de R2 — escaleras `(event_ts, stream_seq)` — es correcta **sólo dentro del mismo authority_epoch**: comparar el current-state de autoridades distintas como una única escalera temporal rechazaría el primer dato válido del epoch nuevo por tener `event_ts` menor que el último del epoch viejo (el snapshot de la autoridad entrante arranca con su reloj propio). Regla congelada: ante un epoch marker/RecoveryBarrier que cambia la autoridad (§19/§20), (1) el current-state certificado del epoch anterior queda invalidado COMO corriente y se preserva únicamente como **last-known** histórico/degradado con su `authority_epoch` previo, `as_of` y stale/quality visibles — no se borra: sigue expuesto para MM policy mientras el epoch nuevo recupera (R6), jamás mezclado con el current-state nuevo; (2) las escaleras del epoch nuevo nacen vacías y su primer snapshot/evento válido las **seed-ea** (`last_quote`/`last_trade` según capability y tipo disponible); (3) dentro del epoch nuevo vuelve a regir la monotonía `(event_ts, stream_seq)` de R2, sin comparación cruzada contra el epoch viejo; (4) readiness sigue siendo autoridad de A (§3): tener last-known del epoch anterior jamás hace READY al nuevo. **Orden de idempotencia ≠ orden de current-state:** `stream_seq` NO se resetea y no se crea secuencia nueva por epoch — el guard `last_applied_stream_seq(stream)` (R1) sigue monotónico por stream lógica a través de epochs (token de transporte, A §5); lo que se scopea por epoch es exclusivamente la escalera event-time del current-state de mercado. Un recovery que A NO acompaña de epoch nuevo (no invalida continuidad) mantiene la escalera corriente intacta. (§5/§19/§20/§23/§24)
- **Acceptance addition:** U (authority switch con timestamp menor) — §30.
- `OWNER_DECISIONS_REQUIRED = NONE`.

## 1. Executive verdict

```text
D2-06B STATUS: READY_FOR_SUBMANAGER_REVIEW  (post-repair R2)
```

El hot analytical state V1 se congela alrededor de tres separaciones durables: **(1) una sola market state compartida, muchos consumidores read-only** — `echo/market_analytics` (nueva, key `stream_id`) es el único owner de barras; strategies, MM y fronts leen sin duplicar por Account; **(2) readiness en dos capas que jamás se colapsan** — la feed/stream readiness queda autoridad de A y la readiness analítica por consumidor es autoridad de B, compuestas por `EffectiveConsumerReadiness = StreamReadinessFor(consumo requerido) ∧ AnalyticalRequirementsReady(consumidor)`; un Strategy BBO-only nunca queda bloqueado por el warm-up de un Strategy con lookback enorme, y un warm-up jamás degrada la feed readiness global (cierre del seam `WARMUP_INCOMPLETE`, §29); **(3) barras como proyección derivada con semántica cerrada**: identidad `(stream_id, timeframe, bucket_open)`, grid anclado a la sesión del calendario D2-05, dos fases (FORMING→CLOSED) con cierre por boundary de reloj/timer (jamás "el próximo tick cierra la barra"), ventana de corrección acotada a una barra que jamás reevalúa Strategy, cero barras sintéticas y cero look-ahead — la misma regla corre en LIVE y en REPLAY. El repair R1 añade las precisiones transversales: idempotencia downstream obligatoria por `stream_seq` (R1), latest market state con escaleras monótonas event-time que jamás regresan dentro de su authority_epoch (R2, scoping por epoch = R7), separación proyección-de-barras-corregible vs observación-de-decisión-inmutable con las cuatro autoridades de recovery congeladas (R3), cutover de rebuild capability-driven (R4), grid anclado a `session_open` a través de breaks internos (R5), disponibilidad last-known jamás igualada a READY (R6) y current-state scoped por `authority_epoch` — el previous demoteado a last-known y el epoch nuevo seed-ea desde su primer dato válido (R7); `bars.late_correction` deja de existir como toggle hot — la política V1 es única. MTF = Option A (cada timeframe demandado agrega directamente del stream canónico, sin cascada de correcciones). `OWNER_DECISIONS_REQUIRED = NONE`.

Físicamente B añade sobre la topología de A: `echo/market_analytics` (StateFun nueva, key `stream_id`) que consume `echo.market-events.v1`, reacciona a los epoch markers/RecoveryBarrier inline de A, construye barras con timers SendAfter y entrega cierres por `ctx.Send` directo a `echo/strategy_engine` (nueva, key `strategy_id`, dueña del estado analítico privado de cada Strategy) más snapshots anillados compactados en `echo.market-bars.v1` para consumo pull (MM/fronts). Ninguna key nueva por Account; ninguna función por timeframe o indicador.

## 2. Frozen inputs from A / D2-05 / D2-04

**De A (post-R1, inmodificable):** `stream_id = (instrument_id, contract_id)` lógico sin binding; `serving_authority{binding_id, members, authority_epoch}` metadata; switch de autoridad = epoch++ + barrier + `NOT_READY(SWITCHING_AUTHORITY)`, contratos intactos (A §3: el epoch también incrementa en recovery que invalida continuidad — el epoch marker es la única frontera que reinicia escaleras de current-state, R7); rollover = otra stream lógica, coexistencia RETIRING/READY; `MarketEvent` canónico QUOTE|TRADE con `event_ts`/`receive_ts` (sólo telemetría), `stream_seq` contiguo post-dedup, `authority_epoch`, `origin{source_id, recovery_provenance}`; clases de identidad A/B/C con content-dedup prohibido; recovery capability-specific con RecoveryBarrier/epoch marker + rango/snapshot; `StreamState` compactado con readiness y reasons (incl. `WARMUP_INCOMPLETE` — reinterpretado en §29); `MarketHistorySource.read(stream_id, from, to) → [MarketEvent]` como seam abierto; capabilities con `reliable_ts` declarado; consumers kache-an el stream state. El egreso del topic canónico es **AT_LEAST_ONCE** con `stream_seq` como token de idempotencia downstream (A §1/§17): B lo convierte en guard obligatorio en sus funciones (R1, §5/§25).

**De D2-05:** `SessionState(calendar_id, instant) → OPEN|BREAK|CLOSED`, `SessionBoundaries`, `NextSessionTransition`; `session_id = (calendar_id, session_date)`; breaks internos opcionales y huecos de maintenance CME = huecos entre sesiones (no breaks); instant fuera de sesión ⇒ `CLOSED(no_session)` + métrica `EVENT_OUTSIDE_SESSION`; `NamedTradingWindow` (EXCHANGE_SUBSET|CLOCK) con `WindowContext{window_open_utc, window_close_utc, window_date, session_date?, session_state}`; availability = `window_open ∧ exchange_session_open`; calendar distribuido por topic compactado + kache (`CALENDAR_NOT_READY`); **Account DayBoundary NO participa de bar semantics**; `calendar_ref → calendar_id` única referencia runtime.

**De D2-04:** `mm_state` es blob del keyed state de `echo/operation`, checkpointeado, **jamás reconstruible desde historia de mercado ni PG**; MM vive como plugin invocado dentro de `echo/operation` con inputs por snapshot/join; recovery authority = checkpoint Flink + replay Kafka + egress transaccional; `echo/signal_fanout` (key `strategy_id`) recibe Signals de StrategyEngine por `echo.signals.v1`; `run_mode`/`run_id` como provenance de nivel de run (D2-06C formaliza el replay determinista).

**De D1 (Front B/B2 con correcciones):** hot state acotado in-memory + historia durable separada; forming vs closed como eventos distintos con timestamp que impide look-ahead; warm-up reconstruye exactamente el estado necesario antes de habilitar señales, sin queries de historia por tick; prohibido congelar "closed bars nunca corregidas" desde ese corpus (la decisión V1 se congela aquí, §9); timestamp discontinuo no es detector de gap; sin timeout universal de salud.

## 3. Readiness layering (manager seam)

Dos capas, dos autoridades, una composición:

```text
EffectiveConsumerReadiness(consumer c) =
    StreamReadinessFor(c.streams, c.consumption_class)     # AUTORIDAD A (feed)
  ∧ AnalyticalRequirementsReady(c)                          # AUTORIDAD B (analítica)
```

- **Capa A — StreamReadinessFor(stream, clase de consumo):** la `StreamState` de A es feed readiness: source/authority, liveness, continuity, freshness, recovery. Se interpreta **por clase de consumo** (R6 de A): `CURRENT_STATE` (BBO/quote) y `HISTORY_DEPENDENT` (barras/indicadores) se gatean por la READINESS de A para su clase; el `last_known_state` de A §15.1 es **disponibilidad** (valor + `as_of` + stale flag), no readiness — legible por MM/safety bajo su propia policy con la marca visible, jamás equivalente a READY (R6) y scoped por epoch: pertenece al epoch que la produjo (R7). Una stream puede estar READY para current-state y NO_READY para history-dependent simultáneamente; y una feed NOT_READY puede tener last-known disponible (`available ∧ ¬ready`, §23).
- **Capa B — AnalyticalRequirementsReady(consumer):** por consumidor, jamás global: el consumidor (Strategy por `strategy_id`; MM de una Operation en su gate de mercado) declara `MarketRequirements` (§16), consume barras/cierres por la semántica congelada hasta cubrir sus lookbacks en el epoch vigente, construye su estado privado y sólo entonces declara readiness analítica. Se computa y retiene **en el consumidor** (el market runtime no conoce lookbacks por consumidor más allá del catálogo de demandas de configuración); se publica opcionalmente para observabilidad.
- **Propiedades obligatorias:** S2 (BBO-only) READY mientras S1 (200×1m+50×5m) aún warmupea; una Strategy nueva con lookback enorme NO baja la readiness de la stream ni de ningún otro consumidor; la feed readiness nunca incluye warm-up (§29); el gate de decisión (Signals nuevas / decisiones MM que requieren esos inputs) se abre con la composición, jamás con una capa sola.
- **Composición por clase de input, no por Strategy binaria:** dentro de MM, los inputs ready antes que otros habilitan las decisiones que sólo los necesitan (latest quote listo antes que las barras reconstruidas → trailing por BBO puede habilitarse antes que sizing por ATR), sin bloquear el path de ejecución/safety (D2-04/D2-05).
- **Readiness ≠ disponibilidad (R6):** el gate compuesto se abre con readiness, jamás con la existencia de un last-known: Strategies no producen nuevas technical Signals desde un stream NOT_READY (salvo semántica futura explícita que lo autorice); MM puede usar un last-known disponible para una acción concreta sólo si su policy para ESA decisión lo autoriza, con `as_of`/stale visible; el path safety/provider/execution permanece independiente (D2-04/D2-05) y Market Runtime no inventa flatten (A §15.6).

## 4. Hot-state ownership

Pertenece al **Market Runtime compartido** (un solo owner por pieza, consumidores read-only):

| Estado | Owner | Key | Naturaleza |
|---|---|---|---|
| Latest BBO/trade (`LatestMarketTick`) | `echo/market_stream` (A) | `stream_id` | in-memory + publicado en stream-state; derivable/reconstructable |
| Forming bars + anillo de barras cerradas por `(stream, tf)` demandado | `echo/market_analytics` (B, nueva) | `stream_id` | in-memory checkpointeada; **derivada/reconstructable** (no autoridad externa) |
| Grid de sesión, truncamientos, `session_date` por barra, cutover de rebuild (capability-driven, §18) | `echo/market_analytics` (B) | `stream_id` | derivado del calendario D2-05 (kache) + epoch markers |
| Readiness analítica del consumidor | el consumidor (`echo/strategy_engine` B; gate MM en `echo/operation`) | `strategy_id` / op key | estado privado del consumidor |
| `MarketRequirements` resueltas + estado de indicadores/finite state de Strategy | `echo/strategy_engine` (B, nueva) | `strategy_id` | in-memory checkpointeada; reconstructable por warm-up |
| Referencias de epoch/provenance y market quality | A (`StreamState`) | `stream_id` | compactado/kache |

**Explícitamente FUERA del market state:** indicadores por Strategy, finite state por Strategy (→ `echo/strategy_engine`, §15), `mm_state` (autoridad D2-04), Account state, provider/risk state. Principio congelado: **one market state, many read-only consumers** — prohibido duplicar market state × Account; el número de Accounts es invisible para `market_analytics` (la evaluación de Strategy y el fan-out ocurren aguas abajo, D2-04).

## 5. Latest market state

```text
LatestMarketTick {
  stream_id, contract_id, instrument_id,
  authority_epoch           # epoch a la que pertenece ESTE current-state (R7):
                            # las escaleras de abajo son monotónicas DENTRO de
                            # ella, jamás comparadas a través de epochs
  last_quote?  { bid_price, bid_qty, ask_price, ask_qty, quote_event_ts, quote_stream_seq }
  last_trade?  { price, qty, trade_event_ts, trade_stream_seq }
  last_event_ts             # máximo monotónico de event_ts de los eventos aceptados;
                            # jamás retrocede
  liveness { last_received_stream_seq, last_received_at }   # lado receive; sólo
                            # telemetría/liveness — jamás semántica de mercado
  as_of, stale_flag         # disponibilidad/frescura del last-known (A §15.1);
                            # jamás readiness (R6, §3/§23)
}
```

- **Dos planos separados (R2):** *EVENT RECEIVED / LIVENESS* — todo evento aceptado cuenta: contadores, liveness, métricas late/recovery, prueba de vida. *CURRENT MARKET STATE* — `last_quote`/`last_trade`, lo que un consumidor de current-state lee. Un evento tardío siempre existe en el primero; sólo cruza al segundo si sube la escalera.
- **Escaleras monótonas de current-state (R2):** `last_trade` se actualiza sólo si `(trade_event_ts, trade_stream_seq)` excede lexicográficamente al vigente; ídem `last_quote` en su escalera propia — quote y trade son escaleras **independientes** (una jamás hace retroceder a la otra ni se mezclan en un "precio actual"). `last_event_ts` es máximo monotónico. Un trade tardío `event_ts=09:59:58` **jamás** convierte `last_trade.price` en su precio después de un trade `event_ts=10:00:02`: entra a la política late de barras (§9), a métricas, prueba liveness y participa del recovery según capability, pero no regresa el current-state.
- **Monotonía scoped por authority_epoch (R7):** las escaleras de current-state son monotónicas **dentro del mismo authority_epoch** — dos autoridades distintas pueden servir sucesivamente la MISMA stream (`stream_id` estable, A §5) y el primer dato válido del epoch nuevo **jamás se rechaza contra el `event_ts` del epoch viejo**. Al procesar un epoch marker/RecoveryBarrier que cambia la autoridad (switch §20 o recovery que invalida continuidad, A §3): el current-state certificado del epoch anterior queda invalidado como corriente y preservado sólo como **last-known** (availability R6: `authority_epoch` previo + `as_of` + stale visibles; no se borra — MM policy puede leerlo mientras el epoch nuevo recupera — y jamás se mezcla con el current-state nuevo); las escaleras del epoch nuevo nacen vacías y el primer snapshot/evento válido del epoch nuevo las seed-ea (`last_quote`/`last_trade` según capability/tipo disponible); desde esa seed rige de nuevo la monotonía `(event_ts, stream_seq)` intra-epoch. Readiness intacta (§3): el last-known del epoch anterior jamás hace READY al nuevo; la forma demoteada viaja como `last_known_previous` en MarketContext (§23). Un recovery que A no marca con epoch nuevo mantiene la escalera corriente.
- **Orden de idempotencia ≠ orden de current-state (R7):** `stream_seq` es global de la stream lógica y **cruza epochs** (A §5: contiguo post-dedup, jamás renumerado): el guard `last_applied_stream_seq(stream)` (R1) sigue monotónico a través de transiciones de autoridad y **no se crea secuencia nueva por epoch**; el scoping por epoch aplica únicamente a la escalera event-time del current-state de mercado.
- **Idempotencia (R1):** la actualización corre tras el guard `stream_seq > last_applied_stream_seq(stream)` (§25); redelivery ⇒ NO-OP sin ningún efecto (ni current-state, ni liveness counters — el evento ya fue contado).
- `receive_ts` jamás participa de semántica de mercado (A §3): sólo liveness/display (`as_of`/stale son la proyección de frescura de A, no orden de dominio).
- **Fuente sin event-time fiable** (`reliable_ts=RECEIVE_ONLY`, A §11): la escalera de current-state no es demostrable ⇒ la limitación se **declara por capability/readiness** y queda visible en el estado/barras construidas de ese source (`EVENT_TS_SOURCE_UNRELIABLE`, R-B9) — no se esconde tras una semántica aparente.
- **No se derivan mid/last sintéticos** ni se mezclan quote y trade: los consumidores eligen su input (`last_quote` para MM hardscalping, `last_trade` para ORB) y su `event_ts`.
- **Owner:** `echo/market_stream` (A) — invariante §4 intacta. Requisito de B sobre la superficie de A: el `last_known_state` del StreamState compactado transporta el `LatestMarketTick` utilizable (payload con los `*_stream_seq` de cada lado para que todo consumidor pueda correr el guard idéntico). R7 añade sobre la misma superficie: el tick transporta `authority_epoch` (ya congelado en A §3) y B lo consume aplicando el scoping por epoch (demote + seed en el marker); la monotonía que A aplique a su estado interno es autoridad de A y no se reabre. Consumo por kache del topic compactado; **no se duplica por Account/Operation**; toda materialización B-side del latest state corre el mismo guard R1.

## 6. Bar identity

```text
BarId      = (stream_id, timeframe, bucket_open_utc)
BarRecord  {
  bar_id                     # identidad mínima congelada
  timeframe                  # de la demanda (ej. 1m, 5m)
  bucket_open_utc            # open efectivo de la barra: punto del grid nominal
                             # (session_open + k·tf) o el punto de reanudación
                             # (break_end) si el calendario partió el bucket (§7, R5)
  close_boundary_utc         # min(bucket_open + tf, corte de sesión/break impuesto)
  session_truncated: bool    # true si el calendario impuso open/close off-grid
                             # (corte de sesión o break interno)
  open/high/low/close        # price (decimal, quote_currency)
  volume                     # contracts (Σ qty trades)
  trade_count
  open_event_ts / close_event_ts     # event_ts del trade open/close
  open_seq / close_seq               # stream_seq refs (tie-break determinístico)
  session_date?              # METADATO derivado del calendario D2-05; NO identidad
  authority_epoch            # epoch bajo el que se construyó
  build_provenance           # LIVE | REBUILD{rebuild_id, history_source}
  correction_count, last_correction_seq
}
```

- **Caso obligatorio:** 09:30–09:31 NQZ6 y 09:30–09:31 NQH7 son barras distintas por `contract_id` dentro de `stream_id`; jamás existe una barra que mezcle Contracts (rollover ⇒ streams distintas, §21).
- **`session_date` = metadato derivable, no identidad:** la identidad ya es unívoca (stream + timeframe + instante de apertura del bucket); `session_date` se resuelve vía `calendar_ref → SessionBoundaries` al cerrar y viaja como metadata para reportes/consumidores. Derivar dos veces es idempotente; meterlo en identidad añadiría una llave redundante sin caso de uso.
- **Fusión determinística de OHLCV bajo out-of-order:** `high=max`, `low=min`, `volume=Σ`, `trade_count=Σ`; `open` = trade con menor `(event_ts, stream_seq)`; `close` = trade con mayor `(event_ts, stream_seq)` (mismo tie-break). La operación es asociativa/commutativa salvo los ties, que se resuelven por orden de stream — el valor final depende sólo del **set de eventos del bucket + su orden de stream**, no del orden de llegada ⇒ las correcciones (§9) y el rebuild (§19) convergen al mismo valor.
- V1 congela barras **source=TRADE** (la cohorte opera sobre trades; MM usa BBO directamente, sin barras de quote). Barras de quote/mid = no construidas (sin demanda; semántica explícita futura si aparece).

## 7. Bucket / session semantics

- **Grid anclado a la sesión:** para cada `(stream, tf)` y cada sesión del calendario (autoridad D2-05 vía `calendar_ref` del Instrument), los buckets son `[session_open + k·tf, session_open + (k+1)·tf)`; el grid **reinicia en cada apertura de sesión**. Nada de anclas de medianoche ni horas CME hardcodeadas. El grid permanece anclado a `session_open` durante TODA la sesión: un **BREAK interno** (que D2-05 permite dentro de la MISMA `ExchangeSession`) **no reinicia el grid** — los boundaries nominales siguen siendo `session_open + k·tf` (R5). Grid nuevo sólo con nueva `session_open` (siguiente sesión / post-holiday).
- **Asignación por event-time:** un evento entra al bucket `floor((event_ts − session_open)/tf)` **sólo si `SessionState=OPEN`** para su `event_ts`. Fuera de sesión (gap de maintenance, holiday, pre-open) el evento **no es input de barra** y suma `EVENT_OUTSIDE_SESSION` (métrica ya congelada en D2-05 §9; prints de settlement caen aquí). Durante BREAK interno: ídem — no se fabrica trading donde el calendario dice BREAK.
- **Truncamiento (caso obligatorio early close / bucket intersecta close / break):** si el calendario corta la sesión (close normal, early close por override, break interno) antes del boundary del bucket, la barra **cierra en el punto de corte** con `session_truncated=true` y `close_boundary_utc=corte`. El remanente del bucket no se fabrica como barra vacía (§11). Al `break_end` se retoma el **MISMO grid de la sesión** (R5): si `break_end` cae estrictamente dentro de un bucket nominal, puede existir una **barra corta** `[break_end, próximo boundary nominal del grid)` con `session_truncated=true` (su open es impuesto por el calendario); si cae en un boundary nominal, la barra siguiente es normal. Los boundaries futuros **jamás se desplazan** por un break interno. Una nueva sesión (post-holiday / siguiente sesión) sí abre grid nuevo anclado a su `session_open`; early close trunca y termina la sesión.
- **Timeframe mayor que la sesión restante / que la sesión completa:** misma regla — una barra truncada al cierre de sesión (degenera a "barra por sesión" si `tf ≥ sesión`). Sin caso especial: la matemática es uniforme.
- **Primer evento tras una frontera (apertura, post-break, post-holiday):** abre el bucket del grid que corresponda: post-break, el MISMO grid de la sesión (barra corta `[break_end, próximo boundary nominal)` si `break_end` cae dentro de un bucket nominal, R5); en apertura de sesión nueva, el grid nuevo anclado a su `session_open`. Si su `event_ts` cae en un bucket ya cubierto por un cierre truncado anterior, es evento de la región nueva (el corte anterior ya cerró).
- Todas las transiciones de sesión que B necesita (`open`, `break`, `close`, `early close`, holiday) llegan exclusivamente de `NextSessionTransition`/`SessionBoundaries` del resolver D2-05 (timers calculados, §22); B no re-deriva session semantics y jamás usa Account DayBoundary.

## 8. Forming / closed / final model

**V1 congela DOS fases + una ventana de corrección acotada; no hay tercera fase FINAL explícita.**

```text
FORMING ──transición de cierre──▶ CLOSED(=final para evaluación)
CLOSED ──(hasta que cierra el siguiente bucket del mismo tf)──▶ INMUTABLE (de-facto FINAL)
```

- **Entrada al bucket:** todo evento con `SessionState=OPEN` y `event_ts ∈ [open, open+tf)` se fusiona en la forming bar por el merge determinístico (§6) en orden de stream.
- **Qué timestamp manda:** `event_ts` para todo (asignación, open/close del OHLC, fronteras). `receive_ts` jamás (A §3).
- **Transición de cierre — dos triggers, el primero gana, jamás "el próximo tick" como única regla:**
  1. **Natural close:** el primer evento **nuevo** procesado (post-guard R1; un redelivery es NO-OP y jamás dispara nada) con `event_ts ≥ boundary` del bucket (cierra el bucket anterior con su valor corriente y abre el nuevo con ese evento).
  2. **Close timer:** un timer por `(stream, tf)` programado en el boundary (seam SendAfter, §25/§22); dispara el cierre aunque no llegue ningún tick (caso obligatorio B: último trade 09:30:50, sin trades a las 09:31:00 ⇒ la barra 09:30 cierra en el boundary con los datos hasta 09:30:50 — **no queda formando eternamente**).
  El requisito exacto al clock/timer (formalización D2-06C, no diseñado aquí): una autoridad de timers que en LIVE dispare SendAfter en wall-clock y en REPLAY en el orden registrado/simulado, con interleaving determinístico timer↔eventos (mismo orden ⇒ mismas barras, mismos valores de cierre, mismas correcciones).
- **Qué ocurre si llegan más eventos del bucket después del cierre:** son correcciones dentro de la ventana de §9 — jamás reabren la fase FORMING.
- **BREAK / early close / fuera de sesión:** cierre truncado por calendario (§7); el timer se reprograma con `NextSessionTransition` (nunca cruza el corte); al reabrir post-break, el timer del bucket se reprograma en el **próximo boundary nominal del grid** (`session_open + k·tf`), no en `break_end + tf` (R5).
- **Forming exposure:** V1 no expone forming bars a Strategies (consumo closed-bars-only en la cohorte; MM usa BBO). La forming bar vive sólo en el estado del builder y como summary de observabilidad en el snapshot compactado. Exponer updates de forming en el futuro = semántica explícita nueva (deferred), nunca comportamiento implícito.

## 9. Late / out-of-order policy — DECISIÓN CONGELADA V1

Una política única, simple y honesta. `allowed lateness` **existe como ventana estructural acotada, no como watermark framework académico**:

- **Regla:** un evento cuyo `event_ts` cae en un bucket ya CLOSED es **corrección elegible sólo si su bucket es el último bucket cerrado de ese timeframe**; si el bucket siguiente ya cerró, el evento es **demasiado tarde**. Es decir: la ventana de corrección de la barra n = hasta el cierre de la barra n+1 (acotada estructuralmente por el propio flujo; sin TTL de wall-clock, sin watermarks por fuente).
- **Corrección (dentro de la ventana):** re-fusión por el merge determinístico (§6) sobre la barra cerrada + `correction_count++` + actualización del snapshot compactado (`echo.market-bars.v1`). **Sólo corrige la MARKET BAR PROJECTION: la Strategy NO se reevalúa** (no hay segundo trigger de evaluación por barra; case A exige exactamente una), jamás re-emite Signal, y **jamás reescribe la DECISION OBSERVATION** (R3): la evaluación disparada por el cierre observó exactamente el snapshot X de ese cierre y ese hecho es inmutable — la corrección produce X' en la proyección, no otra evaluación.
- **Demasiado tarde (fuera de la ventana):** **no toca barras**; se cuenta y alerta (`EVENT_LATE_DROPPED_BARS`, fail-visible). El evento **sigue existiendo íntegro en el stream canónico** de A (con su `stream_seq`): jamás se sacrifica un evento físico — lo que se acota es su contribución a la proyección de barras, y la pérdida queda visible como anomalía. (D1 Front B: no congelar "closed bars nunca se corrigen" desde ese corpus — aquí se congela lo contrario: se corrigen dentro de una ventana de una barra, y fuera de ella se dropean a métrica.)
- **Forming:** no existe "corrección de forming" — la forming fusiona en orden de llegada con semántica conmutativa (§6); cualquier orden produce el mismo valor.
- **Config vs semántica (repair R1):** la regla anterior ES la semántica V1 **única** — no existe toggle. `bars.late_correction: ON|OFF` como hot config **se elimina**: un flag que cambia la semántica que afecta decisiones no puede mutar silenciosamente durante un run; la semántica de barras es **run-pinned** (forma parte de la provenance del run) y una política alternativa futura nacería como semántica nueva versionada, jamás como switch hot. No hay magnitud de lateness configurable (la ventana es estructural); thresholds de frescura/liveness siguen siendo autoridad de A. Las decision observations ya emitidas son facts inmutables conceptualmente, con o sin corrección posterior.
- **Caso obligatorio C:** bar 09:30:00–09:31:00, evento con `event_ts=09:30:59.900` que llega físicamente después del boundary. Resultado único V1: si la barra 09:30 es aún el último bucket cerrado de 1m cuando el evento se procesa ⇒ **corrección**: se re-fusiona (puede mover el close o el high/low), `BAR_UPDATED` vía snapshot, `correction_count++`, **sin reevaluación de Strategy**; si la 09:31 ya cerró ⇒ **drop-a-métrica** con alerta; en ambos casos el evento permanece en el stream canónico, cuenta para liveness/métricas y toca el current-state sólo si su `(event_ts, stream_seq)` excede el `last_trade` vigente (§5, R2 — escalera intra-epoch, R7). LIVE y REPLAY reproducen el mismo resultado con los mismos inputs (orden de stream + orden de timers), que es exactamente el contrato de fidelidad que D2-06C debe garantizar.
- **Tras recovery replay:** el rebuild (§19) es un camino aparte — durante rebuild no se aplican reglas de lateness (los eventos del segmento reconstruido son el pasado oficial); la política de correcciones vuelve a regir sólo en el hot path post-boundary.
- **Demonstración simultánea:** determinismo (mismo stream+timers ⇒ mismos valores y mismos triggers); no look-ahead (las correcciones sólo añaden datos del pasado del bucket, §10); latencia razonable (cierre en el boundary por timer, no espera de ticks); operación real (métricas fail-visible, sin framework); replay fiel (regla idéntica + orden reproducible = requisito a C).

## 10. No look-ahead

- **WHEN IS A BAR OBSERVABLE BY STRATEGY?** Una barra es observable como CLOSED **sólo a partir de la emisión de su transición de cierre** (natural o por timer) — y esa entrega ES el trigger de evaluación (§22). Antes de la transición, la barra no existe para ningún consumidor closed-bars-only (ni en la entrega push ni como "closed" en el snapshot).
- La evaluación sobre el cierre ve exclusivamente datos con `event_ts ≤ close_boundary` del bucket (más correcciones ya aplicadas al momento del trigger, todas del pasado del bucket). Jamás se usa historia futura para completar una barra live: el timer cierra en el boundary con lo que hay.
- MTF: una barra 5m jamás cierra antes de su propio boundary aunque todas sus 1m existan (su cierre tiene timer/boundary propio).
- Las correcciones posteriores no mueven la ventana de observación ni re-disparan evaluación (§9): el consumidor que ya evaluó no retro-ve nada; el que lea el snapshot después ve el valor corregido con su `correction_count` — trazable, no oculto.
- **PROYECCIÓN vs OBSERVACIÓN (R3):** la MARKET BAR PROJECTION es corregible dentro de la ventana (§9) — el snapshot que un lector tardío consulta muestra X' con su `correction_count`. La DECISION OBSERVATION es un hecho inmutable: la evaluación disparada por el cierre observó exactamente X; ninguna corrección la reescribe, genera una segunda evaluación o una Signal retrospectiva. Consecuencia declarada y congelada: un consumidor que reconstruya barras desde historia genérica event-time-sorted obtiene la **proyección final** del segmento, **no** los snapshots pre-corrección que una sesión live entregó a sus strategies — por lo tanto **no se afirma** que un `MarketHistorySource` genérico reconstruya automáticamente el finite state exacto de una sesión live con efectos de late-arrival (autoridades de recovery: §17/§24; requisito EXACT REPLAY: D2-06C, sin diseñarse aquí).
- Misma regla en LIVE y REPLAY por construcción (mismo código, clock inyectado por C).

## 11. Empty bars

**No synthetic empty bars. Sin forward-fill. Sin OHLC fake.**

- Exchange OPEN sin trades en un bucket ⇒ **no se emite barra** (ni forming persistida vacía ni registro); la ausencia es observable: no hay `BAR_CLOSED` para ese bucket.
- Diferencia explícita entre "no hubo barra porque CLOSED/BREAK" (el calendario lo dice: `SessionState≠OPEN`, sin grid activo) y "no hubo barra porque OPEN sin trades" (calendario OPEN, hueco de secuencia de buckets observable): ambos se distinguen consultando el session context del calendario D2-05 (kache); el market runtime no fabrica la diferencia por su cuenta.
- Si una Strategy futura necesita barras vacías/forward-fill (p.ej. para indicadores time-anchored), será una **semántica explícita declarada en su requirements** (`empty_bars: FILL_FORWARD` — no construida en V1), nunca comportamiento implícito del engine. Deferred debt con nombre, no hueco silencioso.

## 12. MTF construction — Option A congelada

**Cada timeframe demandado agrega directamente del stream canónico de eventos (Option A).** No se deriva 5m desde 1m cerradas (Option B rechazada), no híbrido.

- **Justificación contra los criterios del mandato:** (1) *correction semantics* — con Option A el mismo evento tarde corrige su bucket en cada timeframe de forma independiente y uniforme (§9); con Option B una corrección de 1m tendría que propagarse en cascada a 5m/15m con reglas de re-agregación por capa (complejidad y nueva superficie de error sin un solo consumidor que la pida); (2) *session boundaries/early close* — el truncamiento se aplica idénticamente en cada timeframe contra el mismo calendario; con B, la sesión viviría dos veces (eventos y barras base); (3) *warm-up* — A consume la misma historia de eventos que el LIVE path (§17) sin depender de un orden entre cierres de 1m y 5m; (4) *determinismo* — mismo merge determinístico en todos los timeframes; (5) *performance/bounded state* — el costo extra es exactamente un merge por evento por timeframe demandado (la cohorte: ≤3 tfs ⇒ ≤3 merges/evento, triviales frente al ingest), y el estado es el anillo por `(stream, tf)` de §13.
- **Demand-driven:** existen builders sólo para los `(stream, tf)` que algúna `MarketRequirements` activa demanda (catálogo de configuración hot); jamás builders "por si acaso", jamás × Account.
- Si un perfil futuro (muchísimos timeframes por evento) hiciera el costo relevante, la migración B es una optimización interna de `market_analytics` con el mismo contrato externo — deuda condicional registrada (§28), no decisión hoy.

## 13. Bounded recent-bar state

- **Por `(stream, tf)` demandado:** 1 forming bar + anillo de las últimas `N` barras CLOSED, con `N = max(lookback demandado por cualquier requirements activa sobre ese (stream, tf)) + headroom(32)`. Nada de historial infinito en keyed memory.
- **Sizing por demandas activas:** el catálogo de requirements (config hot, patrón compacted+kache) define los `(stream, tf, lookback)`; el anillo se dimensiona contra ese máximo. Cambio de requirements: **expansión** — el nuevo consumidor con lookback mayor warm-upea desde `MarketHistorySource` (§17) si la profundidad excede el anillo (el anillo no se rellena retroactivamente); **reducción** — GC del builder/anillo cuando la última demanda desaparece (idempotente por catálogo).
- **Eviction:** drop del extremo más viejo; evictar es seguro porque todo consumidor con lookback > anillo disponible pertenece al camino de warm-up/historia, no al hot path.
- **Durable vs reconstruible:** el anillo y forming viven en keyed state checkpointeada de `market_analytics` (restart rápido, tamaño acotado: pocas streams × pocos tfs × cientos de barras × OHLCV ⇒ trivial); **no hay autoridad externa de barras en V1** (sin DB/data lake): las barras son proyección reconstructable desde `echo.market-events.v1` + `MarketHistorySource`. El snapshot compactado `echo.market-bars.v1` es read model, no autoridad.
- **Prohibido:** history query por tick (el hot path lee sólo forming+anillo en memoria); guardar events crudos duplicados en el builder (el stream canónico de A ya es el registro).

## 14. Indicator ownership

- **Regla congelada de partida:** todo indicador (RSI/ATR/Stochastic/…) y todo estado analítico derivado pertenece al **runtime de la Strategy / estado analítico strategy-keyed** (§15). **NO existe un MarketFeedEngine global con indicadores** y no se construye un global indicator service en V1.
- **Sharing explícito permitido sólo con identidad exacta** `(stream, timeframe, indicator type, indicator config)` — y **YAGNI lo deja fuera de V1**: no hay evidencia de consumidor que justifique la infraestructura de dedup/invalidación de indicadores compartidos. Deferred debt con condición de disparo (medición de CPU de evaluación en D6 que demuestre duplicación material entre strategies distintas).
- **Cómo se evita 200 Accounts → 200 RSI idénticos:** la unidad de sharing V1 es **la evaluación de Strategy una vez por trigger, antes del fan-out**: 200 `AccountStrategies` que usan S1 comparten UNA instancia de S1 (`echo/strategy_engine`, key `strategy_id`), sus indicadores y UNA evaluación por cierre de barra; el fan-out a Accounts (D2-04) multiplica *mensajes*, jamás *cómputo de mercado*. Este es el sharing mínimo y suficiente; no requiere servicio de indicadores.

## 15. Strategy analytical state

- **Owner físico:** `echo/strategy_engine` (NUEVA, StateFun, key `strategy_id`). Estado privado por Strategy: `MarketRequirements` resueltas, flags de readiness analítica por requerimiento, series de indicadores, finite state de la Strategy (niveles OR, posición lógica de la idea, etc.). Checkpointeada; reconstructable re-ejecutando el warm-up (§17) — su estado es derivado del mercado + su lógica pura.
- **La Strategy consume market state read-only:** cierres de barra entregados push (§25), latest tick vía stream-state kache (§5), session/window context vía transiciones + calendario kache (D2-05). Jamás muta market state; jamás ve binding/source (ve `instrument_id`/`contract_id`, D2-03/A §5).
- **Señal:** al dispararse una evaluación con `EffectiveConsumerReadiness=true`, la Strategy produce 0..N `Signal` (D2-03) → `echo.signals.v1` → `echo/signal_fanout` (D2-04, key `strategy_id`). El fan-out a Accounts es posterior y ajeno a B.
- **Determinismo y recovery (R3):** el estado de Strategy es determinístico ante el mismo stream ordenado de cierres/transiciones **entregados** (misma propiedad de dominio R5 de D2-04). **NORMAL RESTART** restaura el estado completo (finite state, series de indicadores, flags de readiness) del **checkpoint** de `echo/strategy_engine` — jamás se sustituye silenciosamente por un warm-up histórico "más corregido" (§24). El warm-up de §17 construye estado inicial sólo para NEW RUN / NEW STRATEGY y series bar-dependientes tras un rebuild de epoch. No se afirma que una historia genérica event-time-sorted reconstruya el finite state exacto de una sesión live con efectos de late-arrival (§10).
- **Alcance:** B congela ownership, keys, inputs, outputs y el contrato de readiness de la pieza market-side. El diseño completo del runtime de Strategy (lenguaje de definición, motor de evaluación, config) excede D2-06B y queda en el workstream correspondiente (§28) — sin bloquear este freeze.

## 16. MarketRequirements contract

```text
MarketRequirements {
  strategy_id
  streams: [
    {
      instrument_id                    # el engine resuelve stream in-force (A §5)
      events: [TRADE | QUOTE]          # subscripciones de evento
      bars:  [ { timeframe, lookback, source: TRADE } ]   # §6; V1 sólo TRADE
    }
  ]
  windows: [ window_id ]?              # NamedTradingWindow D2-05 (transiciones)
  evaluation: {
    triggers: [ BAR_CLOSE(stream, tf) | MARKET_EVENT(stream) | WINDOW_TRANSITION(window_id) ]
  }
}
```

- Forma KISS elegida: readiness por **consumer (strategy)** con dependencias por **(stream, timeframe)** dentro de la declaración; no existe "requirement set" como entidad aparte. **No Account-keyed** (la requirements es de la Strategy; las Accounts heredan por el binding D2-01..03).
- **Los indicadores NO se declaran al market runtime** (YAGNI): el market sirve eventos+barras; los indicadores se derivan strategy-side (§14). El campo `indicator requirements` del mandato queda explícitamente fuera del shape.
- **MM declara sus necesidades de mercado en su config MM** (misma primitiva, scope Operation): típicamente `events:[QUOTE]` + bars para su indicador de sizing (ej. ATR 1m lookback N). Prohibido que MM pinnee source/binding (R1 de A).
- Distribución: catálogo hot (config → topic compactado → kache) con el patrón congelado; requirements inválidas (tf no declarado, calendar no resuelto, window inexistente) ⇒ fail-closed en carga (`REQUIREMENTS_INVALID`), sin defaults silenciosos.

## 17. Warm-up

Pasos congelados (ejemplo obligatorio S1: NQ, 1m closed lookback=200, 5m closed lookback=50, `NY_OPEN` + transiciones, evaluate on 1m close):

1. **Detect:** resolver `MarketRequirements` desde config (kache) al registrar la Strategy.
2. **Obtain historia:** calcular el span mínimo por stream: `max_lookback × tf` por timeframe (≥ 200×1m ∪ 50×5m) + alineación de sesión (el span cubre sesiones completas para que el grid anclado reconstruya ids idénticos) + leer de `MarketHistorySource` (§18) **eventos crudos normalizados** (jamás prebuilt bars en V1).
3. **Feed EXACTAMENTE la misma bar semantics:** el segmento de historia entra a los MISMOS builders de `market_analytics` por el mismo código de merge/sesión ⇒ ids y valores idénticos a los que el MISMO segmento produce por el camino LIVE. **Alcance (R3):** el warm-up construye el estado inicial de un consumidor **sin decision history live previa** (NEW RUN / NEW STRATEGY) y las series bar-dependientes tras un rebuild de epoch; NO reproduce los snapshots pre-corrección que una sesión live observó — ese claim se eliminó y la reproducción exacta es requisito de EXACT REPLAY de D2-06C (§10). La Strategy recibe esos cierres por el mismo canal push con `build_provenance=REBUILD`.
4. **Build state:** los indicadores/finite state de la Strategy se construyen con esos cierres.
5. **Ready:** `AnalyticalRequirementsReady=true` cuando (a) cerró el boundary live: procesado el marcador de frontera del rebuild (§19) y (b) los conteos por (stream, tf) cubren los lookbacks declarados en el epoch vigente. La composición con la capa A habilita el gate (§3).
6. **Signals:** sólo después del gate. Antes, la Strategy no emite nada (los triggers se acumulan o se ignoran según trigger — BAR_CLOSE acumula el último, MARKET_EVENT se ignora en warm-up).
- **No query de historia por tick** (§13); **sin semántica de bars distinta entre warm-up y LIVE** (garantía estructural del paso 3). Optimización con prebuilt bars: **rechazada en V1** — certificar que barras preconstruidas tienen exactamente esta semántica/versión exigiría un golden de equivalencia sin consumidor que lo pague; si algún día se acepta, requiere `bars_semantics_version` certificada por equivalencia contra este builder (deuda registrada §28).
- **NORMAL RESTART no pasa por warm-up (R3):** con checkpoint válido, `echo/strategy_engine` restaura su decision state del checkpoint (§24) — el warm-up es el camino de NEW RUN/NEW STRATEGY y de las series bar-dependientes tras rebuild; jamás un reemplazo silencioso del estado checkpointeado. Checkpoint perdido ⇒ `COLD_RECOVERY_REQUIRED` fail-closed (autoridad D2-04 R11), nunca "reconstrucción equivalente" desde vendor history.

## 18. MarketHistorySource requirements (qué B necesita del seam de A)

B **no selecciona DB/vendor** (seam abierto de A §16). Congela QUÉ exige del interface `read(stream_id, from, to) → [MarketEvent]`:

- **Raw normalized MarketEvents** con el envelope canónico de A (mismos campos, mismas units) — **no canonical bars** (§17).
- **Event-time range** por stream exacta: `stream_id` incluye el `contract_id` exacto (la historia de NQZ6 y NQH7 son streams distintas); `from/to` son instantes event-time.
- **Ordering assumption:** eventos retornados en **event-time no decreciente**, ties resueltos por orden del source (posición in-packet cuando aplique). No se exige orden de `stream_seq` (la historia no lo tiene: el seq lo asigna el engine; los ids de identidad A/B sí viajan en `source_event_position` cuando el source los declara).
- **Cutover capability-driven (R4) — `R` es nombre conceptual, no "último event_ts":** B no hace dual-read ingenuo y el stitch exige regiones **realmente disjuntas demostradas por el mecanismo**, no por aritmética de event-time. **Clases A/B** (identidad dedup-safe declarada): el seam se deduplica por identidad de A (packet-posicional incluida); el `R` puede ser un cursor/posición canónica demostrable del source. **Clase C** (sin identidad): el cutover exige uno de: (a) boundary/cursor garantizado por el history/live source; (b) pausa/cutover con buffer controlado que produzca dos regiones realmente disjuntas; (c) snapshot replacement cuando la semántica lo alcance; (d) full rebuild desde historia autoritativa; (e) `ANALYTICAL_REBUILD_UNPROVABLE` fail-closed. **Prohibido:** dropear un evento live sólo porque `event_ts < R` asumiendo que la historia lo contiene — jamás se sacrifica un evento físico por un stitch cómodo (coherente con A §4/§12). Provenance del segmento (`history_source`, mecanismo de cutover, rango) queda sellada en las barras REBUILD.
- **Session/calendar snapshot del window:** para reconstruir ids/truncamientos idénticos, el rebuild pinnea la versión del calendario (dataset + `revision_hash` de D2-05) vigente para la ventana; el snapshot viaja en la provenance del segmento.
- **Authority/provenance relevante:** `origin.source_id` de los eventos de historia + id del adapter de historia en la provenance de barras REBUILD (diagnóstico "¿de dónde salió esta barra?").
- Sin data lake nuevo (A §16/§20); sin selección de grabación (eso es D2-06C: B sólo deja el requisito de que el recording, si existe, pueda servir este mismo contrato).

## 19. Recovery rebuild

Comportamiento B ante el RecoveryBarrier/epoch marker de A (§12 de A delimita; B reconstruye):

- **Al recibir el epoch marker (epoch E+1) por stream:** todo estado analítico downstream de esa stream queda **inválido para evaluación** — forming bars descartadas (sin cierre sintético), anillo retenido pero **marcado por epoch** (sirve sólo como referencia histórica, jamás se corrige con eventos del epoch nuevo, jamás alimenta evaluación nueva), readiness analítica de todos los consumidores de esa stream ⇒ gate cerrado.
- **Current-state en el epoch marker (R7):** el `LatestMarketTick` del epoch anterior se demueve a **last-known** (§5: epoch previo + `as_of` + stale visibles; disponible para MM policy, jamás corriente) y las escaleras del epoch nuevo nacen vacías: el primer snapshot/evento válido del recovery (según capability: snapshot BBO, natural refresh o primer evento) las seed-ea **sin comparar `event_ts` contra el epoch viejo**; desde la seed rige la monotonía `(event_ts, stream_seq)` intra-epoch. El guard `last_applied_stream_seq` no se resetea (el orden de idempotencia no es el orden de current-state). Un recovery que A no acompaña de epoch nuevo mantiene la escalera corriente.
- **Rebuild:** se dispara el warm-up de §17 contra el epoch nuevo con cutover **capability-driven** (§18, R4) — el epoch marker/RecoveryBarrier es la frontera estructural in-band del segmento; la misma maquinaria, sin política de lateness dentro del segmento; consumidores requieren sólo su propio lookback (no la historia completa de la disrupción). El rebuild reconstruye la MARKET BAR PROJECTION y las series bar-dependientes; las decisiones ya evaluadas son hechos: sin Signals retrospectivas y sin reescritura de qué snapshot observó cada evaluación (R3); el decision state de Strategy en un restart normal vuelve de checkpoint (§24).
- **Clase de consumo manda (case K):** consumidor **BBO-only**: la recuperación de current-state de A (snapshot/natural refresh) + `AnalyticalRequirementsReady` trivial ⇒ readiness recuperable sin rebuild de historia. Consumidor **bars/history-dependent**: si la continuidad de trades no puede probarse y el rebuild vía `MarketHistorySource` no puede cubrir el hueco con autoridad (§18) ⇒ el consumidor queda `NOT_READY(ANALYTICAL_REBUILD_UNPROVABLE)` fail-closed (sin Signals, sin decisiones MM que requieran esos inputs) hasta rebuild suficiente o acción operacional; jamás se declara ready por un BBO fresco (R6 de A respetado).
- **Qué sigue vivo durante rebuild:** el path de ejecución/Orders/Fills (D2-04), los exits/safety del plano provider (D2-05), la telemetría; el current-state del epoch anterior queda expuesto como last-known con `as_of`/stale visibles (R7, §5). El rebuild jamás reconstruye `mm_state` (autoridad D2-04).
- **LIVE vs REPLAY:** idéntico camino de código; el replay reproduce barrier + segmento, incluida la transición current-state de R7 (demote + seed) con el mismo orden barrier/eventos (requisito a C).

## 20. Authority-switch rebuild (case J del mandato)

Caso: stream `(NQ, NQZ6)`, `authority_epoch=7`, forming 1m en progreso; switch heterogéneo ⇒ epoch=8. **Prohibido continuar la misma forming bar mezclando eventos de dos autoridades heterogéneas.** Política V1 (KISS, sin corrección retrospectiva de Signals):

1. **Invalidación:** la forming bar (en todos los tfs demandados) se **descarta** al procesar el epoch marker — no se cierra, no se emite, no se evalúa (`FORMING_BAR_DISCARDED_ON_SWITCH` en telemetría). No hay "barra truncada por switch": inventar un cierre con datos de una sola autoridad sería sintético; descartar es honesto y el siguiente evento del epoch nuevo abre bucket nuevo.
2. **Recently closed bars:** retenidas con su `authority_epoch=7`; inmutables para el epoch nuevo (sin correcciones cruzadas de epoch — la ventana de corrección de §9 no cruza epoch markers); los consumidores que ya evaluaron con ellas no se revisitan (jamás retrospective Signal correction).
3. **Rebuild lookback requerido:** la unión de los lookbacks activos de esa stream (§13) contra la historia de la **autoridad nueva** (§18); si la autoridad nueva no puede servir esa historia con las garantías de §18 ⇒ consumidores history-dependent `NOT_READY(ANALYTICAL_REBUILD_UNPROVABLE)` (fail-closed, operador decide) — coherente con el rechazo de switch por servabilidad de A §9.
4. **Readiness de vuelta:** `StreamReadinessFor(READY, epoch 8)` (A) ∧ rebuild consumado por consumidor (B) ⇒ `EffectiveConsumerReadiness=true`; los BBO-only pueden volver antes que los de barras (§3/§19).

## 21. Rollover behavior (case I)

- Rollover NQZ6→NQH7 (acción owner D2-05, prospectivo): nace la stream `(NQ, NQH7)`; `market_analytics` crea sus builders/warm-up **por las demandas declaradas** sobre el instrumento; `echo/strategy_engine` de S1 resuelve in-force (A §5) y cambia su evaluación a H7 **sólo cuando sus requirements sobre H7 están analíticamente READY** (mismo warm-up de §17 sobre la stream nueva); hasta entonces S1 sigue sin emitir sobre NQ (ni evalúa Z6 "de transición": el in-force ya cambió — el gap de evaluación entre rollover y READY es el comportamiento seguro).
- `(NQ, NQZ6)` RETIRING (A §14): sus barras siguen construyéndose **mientras su demanda exista** (MM de la Operation pinneada las necesita) y dejan de construirse al RELEASE (GC por catálogo). La Operation vieja conserva sus inputs de Z6: latest tick + anillo de Z6 siguen servidos read-only.
- **Jamás existe una barra que mezcle Z6+H7** (identidad por contract, §6); no hay continuous/back-adjusted (fuera V1, A §9).
- El warm-up de la stream nueva NO bloquea ni degrada la stream vieja ni a ningún otro consumidor (layering §3).

## 22. Strategy evaluation cadence

- **Congelado por triggers declarados** (§16): `BAR_CLOSE(stream, tf)` (el estándar; la entrega del cierre ES la invocación), `MARKET_EVENT(stream)` (sólo strategies que realmente necesitan ticks; asume el costo declarado), `WINDOW_TRANSITION(window_id)` (open/close de ventana y cambios de `session_state` que la afectan, derivados exclusivamente de `NextSessionTransition` de D2-05 con timers calculados — SendAfter seam, mismo requisito de clock que §8).
- **No toda Strategy recibe todos los ticks:** una bars-only jamás ve el firehose (el builder consume eventos; la Strategy recibe cierres). Ejemplo S1: trigger = BAR_CLOSE(NQ,1m); las 5m y las transiciones son contexto disponible (snapshot/kache + entregas de transición), sin triggers propios.
- **Evaluación una vez por Strategy/trigger:** el estado de mercado compartido se evalúa una vez en `echo/strategy_engine` (§14); la entrega de cierres por stream es 1 Send por strategy demandante (no por cuenta); el Signal fan-out a Accounts viene DESPUÉS (D2-04).
- **Guard de triggers (R1):** la entrega BAR_CLOSED es un mensaje que puede redeliverar tras restore: `echo/strategy_engine` guarda la identidad del último closure aplicado por `(stream, tf)` (bucket_open estrictamente creciente por closure) y absorbe redeliveries/closures viejos como NO-OP; los triggers `MARKET_EVENT` pasan por el mismo guard `stream_seq` (§5/§25) — un redelivery jamás dispara una segunda evaluación.
- Timer seam (requisito exacto a D2-06C, ya declarado en §8): autoridad de timers LIVE=wall-clock / REPLAY=orden reproducible, interleaving determinístico con el stream. B NO diseña DomainClock.

## 23. MM MarketContext (MoneyManagement market input)

Contrato **read-only** servido a MM dentro de `echo/operation` (patrón join de D2-04):

```text
MarketContext {                          # read-only snapshot de referencia
  stream_id, instrument_id, contract_id (pinneado), authority_epoch
  latest: LatestMarketTick               # kache del stream state de A (§5)
  bars(stream, tf) → ring snapshot       # kache de echo.market-bars.v1 (§25)
  readiness: { stream: {class, state, reasons, as_of},   # READINESS — autoridad A (§3)
               last_known: {present, as_of, stale_flag}, # DISPONIBILIDAD ≠ readiness (R6)
               ring_upto }                               # proyección B (§13)
  session: { session_state, session_date?, next_transition? }   # calendario kache D2-05
}
```

- **No mutable global MM store; no duplicación feed/bar × Operation:** MM obtiene referencias/snapshots de los read models compartidos; su estado propio (`mm_state`) vive y muere en D2-04. Los valores analíticos compartibles (ej. el anillo) se sirven del mismo snapshot para todas las Operations que los demandan; el cómputo del indicador de MM es per-Operation por naturaleza (es parte de su decisión), pero **lee** estado compartido.
- **Gate por input (R6):** una decisión MM que requiere un input cuyo stream **readiness** no está READY (ej. sizing por ATR durante rebuild) **no se produce por readiness** (gate de mercado §3). El uso de un `last_known` disponible para una acción concreta (ej. gestionar exits con BBO marcado stale) es **policy declarada de MM para ESA decisión**, con `as_of`/stale visible — la disponibilidad jamás eleva la readiness ni abre el gate por sí sola. Estrategias: sin Signals técnicas nuevas desde stream NOT_READY (§3). Decisiones que no dependen del mercado y el plano safety/provider (D2-05 R17) no se bloquean por market readiness; Market Runtime no inventa flatten (A §15.6).
- MM jamás pinnea source/binding (R1); accede por `instrument_id`/`contract_id` pinneado.

## 24. Restart with live Operations (case L)

Core/runtime reinicia con Operation A viva sobre NQZ6:

1. **`mm_state`** se restaura del checkpoint D2-04 (autoridad R11; jamás se reconstruye desde historia de mercado).
2. **Market state:** `echo/market_stream` restaura de checkpoint (o recovery de A); `LatestMarketTick` reconstruido por snapshot/primera quote (rápido). `echo/market_analytics` restaura forming+anillos de checkpoint si existe; **si el checkpoint es insuficiente/pérdida:** rebuild §19 con cutover capability-driven (§18, R4) desde `MarketHistorySource` — mismas garantías.
3. **Estado analítico de Strategy (R3):** `echo/strategy_engine` **restaura del checkpoint** su estado completo (finite state, series, readiness flags — misma autoridad de recovery que D2-04 R11); el warm-up §17 es el camino de NEW RUN/NEW STRATEGY o de las series bar-dependientes tras un rebuild de epoch; **jamás** se sustituye silenciosamente el decision state checkpointeado por un warm-up histórico "más corregido". Checkpoint de decision state perdido ⇒ `COLD_RECOVERY_REQUIRED` fail-closed (autoridad D2-04), nunca reconstrucción claim desde vendor history.
4. **Gates (R6):** las decisiones MM dependientes de cada input esperan la **readiness** de ESE input (BBO listo antes que barras ⇒ trailing BBO puede habilitarse antes que sizing por ATR, §3); MM no actúa con inputs requeridos non-ready salvo que su policy para ESA decisión autorice explícitamente el last-known disponible, con `as_of`/stale visible — la disponibilidad de last-known jamás equivale a READY; strategies sin Signals técnicas nuevas desde stream NOT_READY; el path de ejecución/venue/safety sigue vivo (D2-04/D2-05).
5. **Case L verificación:** MM state restaurado de D2-04 ✓; strategy decision state restaurado de checkpoint (no recalculado desde barras reconstruidas/corregidas) ✓; market/analytical bar inputs reconstruidos independientemente ✓; MM sin actuar sobre inputs requeridos non-ready (last-known sólo bajo policy declarada) ✓; orden de readiness por input, no global ✓.

## 25. Physical topology

```text
echo.market-events.v1 (A, canónico, key stream_id; epoch markers inline)
        │ ingress
        ▼
echo/market_analytics   (StateFun NUEVA, key = stream_id)          [B]
  state (ValueSpec, checkpointed, acotado):
    demandas (stream, tf) del catálogo; forming bar por (stream,tf);
    anillo closed bars por (stream,tf); grid/truncamientos de sesión;
    rebuild segment activo {rebuild_id, cutover capability-driven (§18),
    history_source, contadores};
    guard idempotencia: last_applied_stream_seq por stream (R1)
  reactúa a: eventos canónicos; epoch markers/RecoveryBarrier (A);
             NextSessionTransition (timers SendAfter de cierre de bucket);
             cambios de catálogo de requirements (config hot)
  produce:
    - ctx.Send(BAR_CLOSED | BUILD_SEGMENT) → echo/strategy_engine keys
      demandantes de ese (stream, tf)     [1 Send por strategy, NO por cuenta]
    - egress snapshot compactado → echo.market-bars.v1  [key: stream|tf;
      ring + forming summary + readiness del segmento + provenance]

echo/strategy_engine    (StateFun NUEVA, key = strategy_id)        [B]
  state: MarketRequirements resueltas; readiness analítica por (stream,tf);
         indicadores/finite state privados; último closure aplicado por
         (stream,tf) + guard stream_seq (R1: redelivery ⇒ NO-OP, jamás doble
         evaluación); restaurado de checkpoint en restart normal (R3)
  inputs: BAR_CLOSED push (§22); LatestMarketTick via stream-state kache (A);
          WINDOW_TRANSITION (timers de NextSessionTransition); calendario kache
  output: Signal → echo.signals.v1 → echo/signal_fanout (D2-04)

echo/operation (D2-04, key account:strategy)
  MM plugin lee MarketContext (pull, read-only, §23) en cada invocación;
  gate de mercado por clase de input (§3); mm_state intacto (D2-04)

config hot (patrón compacted+kache): catálogo de requirements (§16),
  demandas MM de datos  [sin toggles de semántica de barras — política V1
  única run-pinned, §9]
MarketHistorySource: interface A §16; adapter-side; usado SÓLO por el camino
  de rebuild/warm-up de market_analytics (§18) — jamás en hot path
```

Justificación owner/key/state: **owner de barras** = `echo/market_analytics` (único; cero keys por Account/timeframe-service/indicator-service); **checkpointed** = forming+anillos+segmentos (acotados §13) y estado de strategy; **derived/reconstructable** = todo el estado de B (desde `echo.market-events.v1` + `MarketHistorySource`); **durable externo** = nada nuevo en V1 (el stream canónico de A es el registro; `echo.market-bars.v1` es read model compactado); **kache** = stream state de A + bars snapshots + requirements + calendario. **Sin function explosion:** 2 funciones nuevas total, independientes del número de cuentas, timeframes, indicadores y strategies·cuentas. No Account como market/bar key.

## 26. Echo V3 reuse/adapt

| Pieza V3 | Disposición | Evidencia |
|---|---|---|
| StateFun Go SDK (`statefun.ValueSpec` + `storage.Get/Set/Remove`) | **REUSE** patrón para estado de `market_analytics` y `strategy_engine` | `v3/core/internal/functions/strategy_config.go:35-44,155-197` |
| Timers `ctx.SendAfter` | **REUSE** (patrón mm_engine anti-detection delay) para close timers de bucket + transiciones de ventana/sesión | `v3/core/internal/functions/mm_engine.go:588-625` |
| Ingress/egress Kafka + registro module.yaml (`echo/*`) | **REUSE/EXTEND**: registrar `echo/market_analytics`, `echo/strategy_engine`, ingress `echo.market-events.v1`, egress `echo.market-bars.v1` | `v3/core/deploy/flink-statefun/develop/module.yaml` |
| `ctx.SendEgress(KafkaEgressBuilder)` | **REUSE** | `mm_engine.go:627-676` |
| kache (compacted topic + cache in-memory) | **REUSE** para bars snapshots, stream state de A, requirements, calendario | `v3/sdk/kache/*` (account_configs, strategy_configs) |
| Compacted hot-config con tombstones (SymbolMapping) | **REUSE patrón** para el catálogo de requirements | `v3/gateway/internal/symbol_mapping_handler.go` |
| Fan-out patrón (ExecutionPlannerFn → signal_fanout) | **REUSE patrón** para la entrega BAR_CLOSED → strategy keys | `v3/core/internal/functions/execution_planner.go` |
| Typed evaluation + egress (automation_evaluator) | **REUSE patrón** para el evaluador de Strategy | `v3/core/internal/functions/automation_evaluator.go` |
| OTel DI + TelemetryContext propagation | **REUSE** | `v3/core/internal/telemetry.go`; patrón PendingMM |
| Checkpoint Flink/StateFun | **REUSE** (estado acotado por diseño §13) | runtime `apache/flink-statefun:3.2.0` |
| MMEngineFn join-snapshot pattern | **ADAPT**: el input de mercado de MM pasa a ser `MarketContext` read-only (§23) | `mm_engine.go` |
| Bars/MTF/indicadores/MarketHistorySource/warm-up | **NEW** (no existe nada físicamente: verificado en baseline — sin Bar/indicator/timeframe infra en v3) | búsqueda baseline 372af59a |
| Strategy runtime físico | **NEW** (no existe `StrategyEngine` en v3; D2-03/D2-04 lo referencian como emisor de Signal) | grep baseline vacío |
| lab_curves / Forge ingest / Bridge MT5 feed | **unrelated/DEFERRED** | — |

## 27. Scale

- **Ingestion cost ∝ streams × event rate.** `echo/market_stream` (A) y `echo/market_analytics` no contienen Account en ninguna key ni estado.
- **Bar aggregation cost ∝ streams × tfs demandados × event rate.** Un evento ejecuta ≤|tfs demandados| merges. Con 200 Accounts usando S1: **una** stream NQ, **un** builder set (1m, 5m), **una** forming+anillos.
- **Indicator/Strategy evaluation cost ∝ strategies × triggers.** S1 evalúa UNA vez por cierre 1m; el fan-out posterior entrega N mensajes (D2-04) sin recomputar mercado.
- **Warm-up cost ∝ strategies × lookbacks** (cada strategy warm-upea su propio estado una vez), jamás por cuenta; la historia de mercado se lee por stream, compartida.
- **MM** es per-Operation por naturaleza (decisión), pero su lectura de mercado es pull de read models compartidos ⇒ 0 duplicación de market state.
- Case M verificado estructuralmente: 200 AccountStrategies × S1 ⇒ 0 bar builders extra, 0 ATR extra de mercado, 1 warm-up de historia por stream, 1 evaluación por trigger, N mensajes de fan-out.

## 28. Risks / debts

- **R-B1 — Skew historia-vs-live (clase C):** el cutover capability-driven (§18/R4) exige regiones realmente disjuntas demostradas por el mecanismo; aun así, si la historia del vendor difiere del feed live (trades que el vendor history no tiene), el rebuild difiere del "ideal". Mitigación: provenance del segmento + `correction_count` + comparación de cobertura post-rebuild (conteo eventos historia vs stream) con alerta; sin mecanismo de cutover demostrable ⇒ `ANALYTICAL_REBUILD_UNPROVABLE` fail-closed; residuo declarado.
- **R-B2 — Corrección acotada a una barra:** trades que llegan después del cierre del bucket siguiente quedan fuera de las barras (métrica fail-visible). Es la decisión V1; si la evidencia de fuentes reales mostrara colas de lateness materiales, la ventana es extensible por decisión técnica (no estructural).
- **R-B3 — Orden timer↔eventos en restart/replay:** el valor de cierre de un bucket depende del corte exacto (eventos procesados antes de la transición). Fiel reproduce requiere el orden de timers (requisito a D2-06C, §8/§22); sin él, REPLAY puede diferir en valores de frontera. Riesgo delegado con contrato explícito.
- **R-B4 — Grid anclado a sesión vs vendor bars:** los buckets Echo nunca coincidirán 1:1 con barras diarias vendor (anclas distintas). Irrelevante en V1 (no consumimos vendor bars; rechazadas §17); documentado para evitar confusiones futuras.
- **R-B5 — Timer density:** 1 timer por (stream, tf) forming + transiciones de ventana; con decenas de streams/tfs es trivial; revisar si el catálogo crece órdenes de magnitud.
- **R-B6 — Snapshot compactado por cierre:** cada cierre/corrección republica el anillo (key `stream|tf`); tamaño = N×OHLCV (pequeños); frecuencia = cierres (baja vs ticks). Aceptable; medir en D6 si crece.
- **R-B7 — Strategy runtime full design:** B congela ownership/contrato market-side de `echo/strategy_engine`; el diseño completo del runtime de Strategy (definición, motor, config) no está despachado — el SUBMANAGER debe rutearlo (no bloquea integrar B).
- **R-B8 — Empty-bar/quote-bar/forming-exposure semantics futuras:** requisitos potenciales de strategies que hoy no existen; cada uno exige semántica explícita nueva (§8/§11), nunca implícita.
- **R-B9 — `reliable_ts=RECEIVE_ONLY` en barras:** un source así produce `event_ts` no venue-authoritative ⇒ asignación de bucket y session semantics degradadas. V1: permitido pero **flag obligatorio** `EVENT_TS_SOURCE_UNRELIABLE` en las barras construidas de ese source; el consumidor decide (A §11 declara la capability; B la hace visible). La misma limitación degrada la escalera de current-state de §5 (R2): se declara, no se esconde.
- **R-B10 — Proyección corregida vs observaciones de decisión (R3):** tras correcciones, la proyección (X') difiere del snapshot (X) que evaluaciones ya emitidas observaron; la divergencia es declarada y visible (`correction_count`, provenance) y los facts de decisión son inmutables; el warm-up de un NEW RUN parte de la proyección final del segmento. No hay claim de continuidad exacta — ésa es la frontera con D2-06C (EXACT REPLAY).

## 29. A integration note

```text
A_INTEGRATION_NOTE:
stream/feed readiness remains A (StreamState per stream; reasons
NO_LIVE_MEMBER / GAP_UNRESOLVED / RECOVERY_UNPROVABLE / STALE_BEYOND_POLICY /
SWITCHING_AUTHORITY / CONTRACT_NOT_SERVABLE / CONFIG_NOT_READY);
analytical/consumer readiness belongs to B (per consumer, §3).
Integrated D2-06 artifact should REMOVE/REINTERPRET WARMUP_INCOMPLETE from
the feed-level StreamState reasons: warm-up is a downstream dependency owned
by consumers, never a global feed gate. A §9 step 6 ("READY ... + warmup
downstream consumido") se interpreta así: la levantada de la FEED barrier es
evidencia de feed (continuidad del epoch vigente); el gate de DECISIÓN de
cada consumidor se abre con EffectiveConsumerReadiness (feed READY ∧
analytical ready). La señal "warmup consumido" que A §21 dejó abierta no
sube hacia el stream state: vive en los consumidores (§3); el interface
B↔engine se reduce a: epoch markers/RecoveryBarrier inline (ya congelados
por A) + la información de cutover que la capability del source habilite
(identidad/cursor/posición canónica para clases A/B; para clase C el
boundary debe ser garantizado por el history/live source — §18/R4: `R` es
nombre conceptual del cutover, no "último event_ts" universal).
```

Esto NO reabre A: cierra el seam A→B con la reinterpretación que A §21 explícitamente dejó a B.

## 30. Acceptance cases

- **A — CLOSED BAR / NO LOOK-AHEAD:** bar 09:30–09:31, strategy closed-bars-only: antes de la transición de cierre (natural o timer) no existe para ella (no push, no "closed" en snapshot); en la transición: exactamente una evaluación (trigger = el propio cierre); correcciones posteriores no reevalúan (§8/§9/§10). **PASS.**
- **B — NO NEXT TICK:** último trade 09:30:50; sin trades al boundary ⇒ close timer del boundary cierra la barra con datos hasta 09:30:50; sin forming eterno (§8). **PASS.**
- **C — LATE EVENT:** `event_ts=09:30:59.900` llegando post-boundary: corrección de la 09:30 si sigue siendo el último bucket cerrado (sin reevaluación), drop-a-métrica si la 09:31 ya cerró; el evento permanece en el stream canónico y toca el current-state sólo si su `(event_ts, stream_seq)` excede el `last_trade` vigente — `last_trade` jamás regresa (§5, R2); LIVE/REPLAY reproducen el mismo resultado con orden+timers (§9). **PASS.**
- **D — SESSION BREAK:** bucket que intersecta BREAK: cierre truncado al inicio del break (`session_truncated=true`), sin trading fabricado; al reabrir se retoma el MISMO grid de `session_open` (barra corta si `break_end` cae dentro de un bucket nominal); boundaries futuros sin desplazar; hueco ENTRE sesiones ⇒ grid nuevo; breaks/huecos distinguidos por el calendario D2-05, no hardcode (§7, R5). **PASS.**
- **E — EARLY CLOSE:** el calendario corta antes del boundary ⇒ última barra cierra en el corte del `SessionBoundaries`/override; sin schedule hardcodeado (§7). **PASS.**
- **F — EMPTY PERIOD:** OPEN sin trades en el bucket ⇒ no hay barra; sin synthetic OHLC; distinción CLOSED/BREAK vs OPEN-sin-trades consultable vía session context (§11). **PASS.**
- **G — MTF:** S1 requiere 1m+5m ⇒ un evento se procesa una vez por timeframe builder (2 merges), jamás × Account; las 5m usan el mismo grid/session/boundary/truncation/correction semantics congelados (§12). **PASS.**
- **H — WARMUP:** NEW RUN / nueva S1 (200×1m+50×5m): warm-up §17 con la misma semántica del builder; `AnalyticalRequirementsReady` al cubrir lookbacks + boundary live; sin Signal antes del gate compuesto (§3); una Strategy BBO-only puede estar READY antes (gate independiente); una nueva strategy con lookback enorme no baja la readiness de nadie. **NORMAL RESTART** de una S1 viva: decision state desde checkpoint, sin re-warmup silencioso (§24, R3). **PASS.**
- **I — ROLLOVER MID-SESSION:** NQZ6→NQH7: barras de streams distintas por contract (jamás mezcla); S1 evalúa sobre H7 sólo con requirements H7 READY; Operation vieja sobre Z6 conserva latest+anillos de Z6 hasta RELEASE (§21). **PASS.**
- **J — AUTHORITY SWITCH MID-BAR:** epoch 7→8: forming descartada (sin mezcla de autoridades), closed bars viejas inmutables por epoch, rebuild con historia de la autoridad nueva + lookbacks de demandas, readiness de vuelta por composición; sin corrección retrospectiva de Signals (§20). **PASS.**
- **K — RECOVERY CLASS C:** BBO recuperado ⇒ consumidor BBO-only recupera readiness (current-state, §3/§19); consumidor bars/history-dependent NO se declara ready sin rebuild suficiente; sin historia autoritativa del hueco ⇒ `NOT_READY(ANALYTICAL_REBUILD_UNPROVABLE)` fail-closed (§19). **PASS.**
- **L — LIVE OPERATION RESTART:** `mm_state` de checkpoint D2-04; market/analytical inputs reconstruidos independientes; MM sin actuar con inputs requeridos non-ready; readiness por input (BBO antes que barras); ejecución/safety viven (§24). **PASS.**
- **M — 200 ACCOUNTS:** 200 AccountStrategies × S1 ⇒ 1 stream, 1 builder set, 1 warm-up de historia por stream, 1 evaluación por trigger, fan-out posterior; cero 200 builders/ATRs/warmups de mercado (§14/§27). **PASS.**
- **N — STRATEGY CADENCE:** strategy bars-only no recibe el firehose: el builder consume eventos; triggers sólo los declarados (BAR_CLOSE/WINDOW_TRANSITION/MARKET_EVENT-declarado); evaluación 1×/trigger/strategy (§22). **PASS.**
- **O — KAFKA REDELIVERY (R1):** TRADE `stream_seq=500` llega dos veces por redelivery del canónico: merge/volume/trade_count/bar values cambian **una vez**; el segundo es NO-OP del guard (`seq ≤ last_applied`); ningún trigger de cierre/evaluación duplicado; telemetría cuenta el no-op. Tras restore de checkpoint el mismo guard absorbe el replay (misma frontera atómica guard/estado). **PASS.**
- **P — LATE EVENT DOES NOT REGRESS CURRENT PRICE (R2):** `last_trade` vigente: `event_ts=10:00:02, price=20001`; llega trade `event_ts=09:59:58, price=19980`: `last_trade` sigue 20001 (escalera monótona `(event_ts, stream_seq)`); el evento tardío entra a la política late de barras (§9), a métricas y liveness, y conserva su tratamiento recovery según capability. **PASS.**
- **Q — LIVE DECISION VS CORRECTED BAR (R3):** la Strategy evaluó el BAR_CLOSE snapshot X; luego una corrección lleva la proyección a X': sin Signal retrospectiva, sin reevaluación; el hecho "esa evaluación usó X" es inmutable; un restart normal recupera el decision state desde checkpoint — jamás lo recalcula silenciosamente desde X'. **PASS.**
- **R — CLASS C REBUILD (R4):** source sin identidad nativa ni cursor garantizado, overlap event-time ambiguo: NO stitch heurístico por `event_ts`; el rebuild exige un mecanismo capability-safe (cursor/boundary garantizado, pausa+cutover con buffer disjunto, snapshot replacement o full rebuild) o queda `ANALYTICAL_REBUILD_UNPROVABLE` fail-closed; ningún evento live se dropea por `event_ts < R`. **PASS.**
- **S — INTERNAL BREAK GRID (R5):** session_open 09:30, tf=60m, BREAK interno 10:00–10:15: la barra 09:30 se trunca en 10:00 (`session_truncated=true`); ninguna barra durante el break; en 10:15 se retoma el MISMO grid — barra corta `[10:15,10:30)`; el próximo boundary nominal 10:30 sigue derivado de `session_open + k·tf` (sin desplazamiento permanente); los buckets 10:30+ quedan intactos. **PASS.**
- **T — STALE BBO (R6):** feed NOT_READY con último BBO existente: MarketContext expone `last_known.present=true` + `as_of`/stale visible ∧ `stream NOT_READY`; MM usa el last-known sólo si su policy para ESA decisión lo permite; strategies sin Signals técnicas nuevas; safety/provider/execution independientes; sin flatten. **PASS.**

## 31. Owner decisions

`OWNER DECISIONS REQUIRED: NONE`. Todas las decisiones de este artefacto —incluidas las del repair R1 (guard de idempotencia downstream, escaleras monótonas de current-state, separación proyección/observación con autoridades de recovery, cutover capability-driven, grid fijo vía breaks internos, disponibilidad ≠ readiness, eliminación del toggle de corrección)— viven dentro de las autoridades congeladas A/D2-05/D2-04 y de las correcciones D1; la eliminación de `bars.late_correction` aplica la preferencia KISS del manager (una policy V1 run-pinned). Quedan **ratificaciones técnicas ordinarias del manager**: nombres físicos de functions/topics/campos (`echo/market_analytics`, `echo/strategy_engine`, `echo.market-bars.v1`, shapes `BarRecord`/`MarketRequirements`/`MarketContext`/`LatestMarketTick`, incluidos los campos de guard/liveness R1/R2), headroom de anillos (32), y el ruteo del diseño completo del runtime de Strategy (R-B7).

## Handoff

```text
D2-06B STATUS:
READY_FOR_SUBMANAGER_REVIEW  (post-repair R1 — Manager Repair D2-06B-R1 aplicado)

ARTIFACT:
main/10-projects/Echo Futures/Echo Futures — D2-06B Bars Hot State Warmup.md

AGENTS-OS SHA:
35909976 (HEAD del vault al aplicar el repair; el artefacto reparado viaja en el sync siguiente)

ECHO BASELINE:
372af59a7b83604781346613da01e3d510ea1360 (HEAD == origin/master, sin delta)

NEXT:
Return to D2-06 SUBMANAGER. Do not start D2-06C.
```
