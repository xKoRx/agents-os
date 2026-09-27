---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo Futures]]"
  - "[[Echo Futures — D2-06A Market Feed Authority]]"
  - "[[Echo Futures — D2-06B Bars Hot State Warmup]]"
  - "[[Echo Futures — D2-05 Instrument Session Provider]]"
  - "[[Echo Futures — D2-04 Operation Order Fill Position]]"
  - "[[Echo Futures — D1 Analysis Pack]]"
aliases:
  - Echo Futures D2-06C
  - EF Live Replay Market Boundary
tags:
  - kind/doc
  - area/echo
  - echo-futures
  - architecture-design
created: "2026-09-27"
updated: "2026-09-27"
---

# Echo Futures — D2-06C Deterministic Market Boundary / LIVE / REPLAY / Ordering / Clock

> [!info]+ TOP worker C — D2-06
> Deliverable del worker C del bloque D2-06 (Market Runtime). Consumes congelados: [[Echo Futures — D2-06A Market Feed Authority]] (`ACCEPTED_FOR_INTEGRATION`) y [[Echo Futures — D2-06B Bars Hot State Warmup]] (`ACCEPTED_FOR_INTEGRATION`) — sus contratos son INPUT congelado y NO se modifican — más [[Echo Futures — D2-05 Instrument Session Provider]] (CLOSED), [[Echo Futures — D2-04 Operation Order Fill Position]] (CLOSED), [[Echo Futures]] D2-01..03 y [[Echo Futures — D1 Analysis Pack]] Fronts B/B2/E. Baseline Echo re-verificada en ventana: `origin/master = 372af59a7b83604781346613da01e3d510ea1360` (clon `~/aranea/work/d4-shot1-20260925/echo`, fetch sin delta; re-verificada nuevamente en la ventana del repair R1, fetch sin delta). Incorpora el **Manager Repair — D2-06C-R1** (R1 replay anchor, R2 runtime logical clock, R3 completitud de TimerFired + regla de journal reescrita + clarificación de costo OD-C1), aplicado quirúrgicamente sobre el candidato revisado por el SUBMANAGER @ ae960a6f; el documento completo refleja ya el modelo reparado, no erratas acumuladas. Sin auditoría física general (el SUBMANAGER ya verificó A+B contra esa baseline): sólo se inspeccionaron los patterns necesarios — module.yaml ingress/egress (sin delivery semantics declarada, keyType string), `ctx.SendAfter` + `CancellationToken` (`mm_engine.go:610`, mock `statefun_mock.go:193-204`), kache/compacted (Gateway symbol-mapping handler), volúmenes checkpoint/savepoint del deploy, `run_mode/run_id` ausente del código (sólo `curve_run_id` de Lab), y ausencia total de market-data/bars/replay/clock en v3. Este artefacto NO implementa código, NO cierra D2-06 global, NO avanza D2-07, NO diseña execution transport, NO reabre A/B/D2-04/D2-05, NO convierte Echo en event sourcing y NO diseña el backtester completo.

## Manager Repair — D2-06C-R1

El SUBMANAGER revisó físicamente el artefacto @ ae960a6f y aceptó la dirección general de C (event_ts ≠ stream_seq ≠ runtime order; `owner_input_seq` per-isla; sin total order global; `MarketRuntimeInput` común; TimerFired como input determinístico; BAR_CLOSED re-derivado; EXACT_REPLAY ≠ HISTORICAL; journal per-isla; DomainClock inyectable; sin event sourcing de Echo; restart normal por checkpoints; recording boundary mercado/estrategia/MM-only). Devolvió tres defectos (R1–R3), la regla general de journal y una clarificación de OD-C1. Este repair es targeted: NO rediseña C, NO reabre A/B/D2-04/D2-05, NO implementa código, NO avanza D2-07. Resolución:

- **R1 — EXACT REPLAY ANCHOR (OPTION A: immutable warm-up corpus).** El candidato dejaba EXACT_REPLAY reproduciendo "desde `owner_input_seq=0`" sin estado inicial: el warm-up B §17 del run live (200×1m + 50×5m + indicadores + finite state) no estaba en el recording — el manifest porta config/revisiones/hashes, jamás estado derivado — así que el replay llegaba vacío a seq=0 y no podía reproducir la primera evaluación de la Strategy. Elección: **el recording conserva el corpus EXACTO de MarketEvents normalizados + snapshots de calendario/config que el warm-up del run consumió**, con identidad inmutable (refs + digest) identificada en el RunManifest; EXACT_REPLAY re-ejecuta ese corpus con la MISMA lógica B §17 (una sola lógica de construcción de estado, sin segunda serialización de estado derivado — la razón para preferir A sobre un snapshot semántico), verifica digest + readiness y recién entonces arranca `owner_input_seq=0`. PROHIBIDO volver a consultar `MarketHistorySource` en replay y asumir igualdad. Sin anchor ⇒ `REPLAY_ANCHOR_MISSING` fail-visible. (§15/§18/§20/§21)
- **R2 — Runtime logical time (`runtime_ts`) separado de event time.** El candidato hacía `DomainClock.Now()` = `event_ts` del input corriente en REPLAY: ante TimerFired deadline 09:31:00 seguido de MarketEvent `event_ts=09:30:59.900` el reloj RETROCEDÍA — prohibido. Congelado: **event time** (`event_ts`) gobierna barras/OHLC/session assignment y puede llegar atrasado respecto al orden de runtime; **runtime logical time** (`runtime_ts`) es monotónico por isla, gobierna `DomainClock.Now()`, schedules relativos, timers y la lógica time-based de Strategy/MM, y JAMÁS retrocede ni se deriva de `event_ts`. LIVE: cada isla deriva `runtime_ts` al admitir cada input (`max(runtime_ts previo, wall clock de admisión)`; `owner_input_seq` tie-break) y lo journala; REPLAY: `Now()` = el `runtime_ts` journalado de la entrada corriente; BACKTEST: reloj sintético no-decreciente desde la precedencia canónica, sin imitar latencia live. (§4/§5/§6/§15/§21)
- **R3 — TimerFired completeness.** Eliminada la change-detection para timers: **TODO TimerFired admitido por el dominio se journala** (bar-close, session/window, health/freshness, Strategy/MM declarados), porque un firing puede programar el próximo timer, reemplazar/cancelar otro, avanzar el control flow o ser prerequisito de un firing futuro sin mutar estado observable ahora (health tick que re-agenda = el ejemplo raíz). Identidad suficiente: `timer_id` namespaced + **`generation`** del handle (re-Schedule = cancel old + new generation); un firing stale de generación vieja NO ejecuta dominio y es absorbido determinísticamente por el guard de generación; EXACT_REPLAY valida cada firing contra el timer set virtual reconstruido. (§6/§7/§22)
- **Regla de journal reescrita (criterio de materialidad).** Sustituido el criterio "muta estado observable ahora" por **"¿puede este input afectar una observación de dominio presente o futura?"** — ALWAYS: todo TimerFired admitido, ConfigTransition material, RecoveryBarrier, transiciones Session/Window cuando son inputs separados, refs de MarketEvent canónicos que pasan guards y afectan la isla, deliveries/refs cross-island necesarios. MAY OMIT: redeliveries de transporte absorbidos antes del dominio, duplicados exactos que guards hacen NO-OP, facts telemetry-only sin efecto presente NI futuro sobre control flow. (§15)
- **OD-C1 se mantiene como decisión owner** (no resuelta aquí), con el costo material actualizado: el recording conserva además el warm-up corpus (R1) — una captura inmutable al iniciar el run, acotada por MarketRequirements, misma retención que el recording; delta marginal frente a la retención del contenido canónico ya exigida. La opción "opt-in diferido" queda efectivamente comprometida AL INICIAR el run (el anchor debe capturarse entonces; un run sin anchor es permanentemente no-replayable desde t0), lo que refuerza la recomendación always-on sin cambiar la arquitectura. `OWNER DECISIONS REQUIRED = 1` (§28-R-C9, §31).
- Estado resultante: `READY_FOR_SUBMANAGER_REVIEW` (no PASS, no CLOSED, no D2-07).

## 1. Executive verdict

```text
D2-06C-R1 STATUS: READY_FOR_SUBMANAGER_REVIEW  (post-repair R1)
```

El boundary determinista V1 se congela alrededor de cuatro separaciones durables: **(1) runtime-order ≠ event-time ≠ stream_seq ≠ runtime logical time** — `event_ts` gobierna semántica técnica de mercado (asignación de barras, B §6) y puede llegar atrasado, `stream_seq` es el token de orden/idempotencia del transporte canónico por stream (A §3), **`owner_input_seq`** es el contador monótono que cada isla de dominio checkpointea y que numera el orden EN QUE esa isla admitió inputs — la identidad que reproduce las observaciones de decisión, y **`runtime_ts`** es el runtime logical time monotónico por isla derivado en la admisión — la única fuente de `DomainClock.Now()` (R2); **(2) una sola frontera de input común** — `MarketRuntimeInput` es la unión congelada de MarketEvent + RecoveryBarrier + TimerFired + Session/WindowTransition + ConfigTransition que TODO consumidor de mercado recibe; no existen `OnLiveTick`/`OnBacktestTick`; BAR_CLOSED **no es input autoritativo grabado: se re-deriva** (§17) porque la pareja (market inputs ordenados + TimerFired en su posición registrada) reproduce exactamente cada snapshot observado X y cada corrección X', con una sola autoridad de contenido; **(3) el recorded deterministic boundary es el LOG DE INPUTS DEL RUN + SU ESTADO INICIAL, no un dump** — `DeterministicInputLog` por isla (entradas de control inline con `owner_input_seq`/`runtime_ts` + referencias posicionales al contenido canónico `echo.market-events.v1` + `echo.market-run-manifests.v1`), grabado por egress transaccional EXACTLY_ONCE en la misma frontera de checkpoint (patrón R14 de D2-04), más el **replay anchor**: el corpus inmutable de warm-up (refs+digest en el manifest, R1) del que EXACT_REPLAY reconstruye con la misma lógica B el estado de dominio previo a `owner_input_seq=0`; `echo.market-events.v1` SOLO **es insuficiente** (sin timers, sin configuración, sin orden entre islas, sin estado inicial) y retención de Kafka ≠ contrato de recording; **(4) DOS modos separados que jamás comparten palabra** — `EXACT_REPLAY` (reproduce las decisiones de un run live previo desde su replay anchor + log grabado, incluidas las observaciones pre-corrección X) y `HISTORICAL/BACKTEST` (sintetiza una secuencia canónica de inputs desde `MarketHistorySource` con la regla de precedencia congelada §9; NO pretende reproducir el desorden de llegada de ningún run live). `run_mode` (D2-04 I11) queda formalizado: REPLAY ≡ EXACT_REPLAY, BACKTEST ≡ HISTORICAL; `origin.recovery_provenance` (A §3) permanece per-evento y jamás colisiona con el modo del run.

Físicamente C no añade NINGUNA función StateFun nueva: añade el contador `owner_input_seq` al estado de las islas existentes (A/B/strategy_engine, campo aditivo C-owned), dos topics nuevos (journal + manifests, egress transaccional para el journal), la captura inmutable del replay anchor al iniciar el run grabado (refs+digest, sin componente nuevo, R1), la librería `DomainClock` inyectable (LIVE = derivación `runtime_ts` + SendAfter durable / REPLAY-BACKTEST = reloj virtual que reproduce los `runtime_ts` journalados o sintetiza el canónico) y un `ReplayDriver` offline que re-maneja los paquetes puros de dominio (patrón `v3/e2e/execution_engine.go`) — cero flota nueva, cero Kafka Streams/CEP.

`OWNER DECISIONS REQUIRED: 1` (§31): si EXACT LIVE REPLAY es capacidad de producto V1 con recording always-on (recomendación) o capability diferida con recording opt-in por run. El boundary congelado es idéntico en ambos casos; la decisión define sólo el default operacional de recording y el alcance de certificación D6.

## 2. Frozen inputs A / B / D2-05 / D2-04

**De A (inmodificable):** `stream_id = (instrument_id, contract_id)` lógica estable ante switch; `serving_authority{binding_id, members, authority_epoch}`; `MarketEvent` QUOTE|TRADE con `event_ts`/`receive_ts` (jamás semántica de dominio), `source_event_position?`, `stream_seq` contiguo post-dedup jamás renumerado y cruza epochs, `authority_epoch`, `origin{source_id, recovery_provenance: LIVE|RECOVERY_REPLAY|SNAPSHOT}`; RecoveryBarrier/epoch marker inline; switch ≠ rollover; `echo.market-events.v1` transporte LIVE canónico AT_LEAST_ONCE (grabación definitiva deliberadamente dejada a C, R7 de A); `MarketHistorySource.read(stream_id, from, to) → [MarketEvent]` seam de warm-up/recovery, NO autoridad de EXACT REPLAY; capabilities con `reliable_ts`; `StreamState` compactado con readiness.

**De B (inmodificable):** una sola market state compartida; guard `last_applied_stream_seq` (R1); escaleras current-state monótonas `(event_ts, stream_seq)` scoped por `authority_epoch` con demote→seed en el marker (R7); barras FORMING→CLOSED con cierre por boundary de reloj/timer jamás "próximo tick"; corrección acotada al último bucket cerrado que jamás reevalúa Strategy; **MARKET BAR PROJECTION ≠ DECISION OBSERVATION** (R3): la evaluación observó X y es hecho inmutable; autoridades de recovery congeladas — NORMAL RESTART = checkpoint, NEW RUN = warm-up, COLD = `COLD_RECOVERY_REQUIRED` salvo recorded boundary suficiente (requisito que C cierra aquí), EXACT REPLAY = requisito delegado a C; timers close por (stream, tf) con reprogramación por `NextSessionTransition`; requisitos explícitos a C: autoridad de timers LIVE=wall-clock/REPLAY=orden registrado con interleaving determinístico timer↔eventos (B §8/§22), y reproducción exacta de demote→seed en el mismo orden relativo (B §19/§30-U). La semántica de warm-up B §17 es además el insumo del replay anchor (R1): EXACT_REPLAY reconstruye el estado inicial re-ejecutando el corpus grabado con esa MISMA lógica — sin re-consultar `MarketHistorySource` en replay.

**De D2-05:** `calendar_ref → calendar_id` única referencia runtime; resolver puro `SessionState/SessionBoundaries/NextSessionTransition` con dataset `calendar_version` + `revision_hash`; distribución hot compacted+kache (`CALENDAR_NOT_READY` fail-closed); NamedTradingWindow `EXCHANGE_SUBSET|CLOCK` con transiciones derivadas exclusivamente de `NextSessionTransition`; **LIVE consume config hot, REPLAY/BACKTEST inyecta snapshots explícitos** (Calendar/RuleSet/DayBoundary/Contract, §19 de D2-05); DayBoundary con transición prospectiva y `not_before` (R18); rollover owner-manual prospectivo jamás auto-roll.

**De D2-04:** `echo/operation` key `account:strategy` serializa por key; propiedad de dominio **same ordered input sequence → same decisions** (R5/R8); `operation_event_seq` runtime-ordering scoped a execution; autoridad de recovery = checkpoint + replay Kafka + egress transaccional; PG proyección eventual jamás autoridad; `COLD_RECOVERY_REQUIRED` fail-closed; `run_mode`/`run_id` en toda entidad (I11); **R12: V1 NO persiste el stream completo de inputs de ejecución y no promete replay exacto de sesiones live — el seam de recorded streams quedó explícitamente en este workstream** (sólo el MARKET/STRATEGY/MM input seam, no el execution stream); egress transaccional EXACTLY_ONCE como patrón durability (R14/I16).

**De D1:** hot state acotado + historia durable separada; forming vs closed distintos con timestamp anti look-ahead; same Strategy/domain code reusable live/backtest mientras adapters/clock/execution difieren; no inferir event store general (B/V2 corrections).

## 3. Determinism invariant (congelado)

```text
GIVEN:
  (a) mismo run manifest inicial (§20) — config/calendar/contract/requirements pinneados —
      y el mismo replay anchor (R1): el corpus inmutable de warm-up del que se
      reconstruye el estado de dominio inicial previo a owner_input_seq=0;
  (b) misma secuencia ordenada de inputs de dominio (MarketRuntimeInput) observada por
      cada isla — la que grabó el DeterministicInputLog en LIVE (con sus runtime_ts),
      o la sintetizada canónica en BACKTEST/HISTORICAL;
  (c) mismo código de dominio (paquetes puros + mismos guards);
THEN:
  las decisiones market-dependent de Strategy y MM son idénticas: mismos triggers de
  evaluación, mismos snapshots observados (incluidas observaciones pre-corrección X),
  mismas Signals, mismas decisiones MM de mercado, misma evolución de la proyección
  de barras (incluidas correcciones en el mismo punto relativo).
```

**Alcance — DOMAIN DETERMINISM ≠ PHYSICAL TRANSPORT TIMING.** El invariante habla de la secuencia serializada que cada isla observa, no de latencias: el desfase físico de llegada, el scheduling de goroutines, el interleave de batches Kafka y la duración de hops son transporte; su único efecto permitido es DETERMINAR (en live) el `owner_input_seq` — que se graba — jamás alterar la semántica. **NO se promete determinismo:** ante inputs distintos; ante config distinta (aunque diff mínima); ante vendor history final que no preserve el orden de llegada/timers del run live (esa historia reproduce la PROYECCIÓN final del segmento, no las observaciones — B §10); ante missing decision-state/anchor/recording (fail-visible/fail-closed, §18/§23); ante concurrencia arbitraria no serializada (fuera del modelo StateFun por key). El determinismo del path de ejecución completo (signals→orders→fills) NO se promete aquí: requiere además el stream de ejecución grabado, explícitamente fuera (D2-04 R12).

## 4. Runtime input model — `MarketRuntimeInput`

Frontera común única. El dominio (market_analytics, strategy_engine, MM market gate) recibe exactamente estos tipos, en LIVE/REPLAY/BACKTEST:

```text
MarketRuntimeInput =
  | MarketEvent            # A §3, QUOTE|TRADE, con stream_seq/authority_epoch/origin
  | RecoveryBarrier        # A §12: epoch marker {stream_id, epoch_nuevo, rango|snapshot}
  | TimerFired             # {owner_key, timer_id, generation, deadline} (§7)
  | SessionWindowTransition# SessionTransition {session_id, state, boundaries} |
                           # WindowTransition {window_id, context} — derivadas de
                           # NextSessionTransition D2-05, agendadas por timers (§12)
  | ConfigTransition       # {config_class, payload/ref, revision/hash, applied_seq} (§13)
```

**Decidido explícitamente qué entra y qué NO:** entran los cinco tipos anteriores y nada más. No entran: BAR_CLOSED ni BAR_UPDATED (derivados por B, §17); StreamState/readiness como tipo aparte — el efecto de gate viaja como ConfigTransition aplicada al consumidor cuando su vista de readiness cambia (§13, materiality); eventos de ejecución (D2-04); health metrics/telemetría; snapshots de posición. Los nombres son conceptuales; ratificación técnica del manager de shapes exactos.

Los cinco tipos son **replay-simétricos por construcción**: cada uno tiene el mismo efecto de dominio cualquiera sea el modo que lo inyecta. Un ConfigTransition que abre/cierra el gate, un barrier que demotea current-state y seed-ea el epoch nuevo (B R7), un TimerFired que cierra barra — idéntico código en LIVE y REPLAY (misma propiedad que B §10 exige y A §19 garantiza por construcción).

**`runtime_ts` no es un campo de transporte (R2):** ningún tipo de `MarketRuntimeInput` lo porta en su envelope; es un atributo que cada isla deriva al admitir el input y journala junto a la entrada (§15). El envelope canónico de A y los shapes conceptuales de arriba quedan intactos; `generation` en TimerFired es identidad del handle del timer (§7), no del transporte.

## 5. Event-time vs runtime-order vs runtime logical time

Cuatro identidades, una por responsabilidad, jamás colapsadas:

| Identidad | Asignador | Gobierna | Jamás |
|---|---|---|---|
| `event_ts` | venue/source (A §3) | semántica técnica: bucket de barra, OHLC, escaleras current-state, session semantics | orden de observación de decisión; fuente de `DomainClock.Now()` |
| `stream_seq` | engine A, post-arbitraje | orden canónico del transporte por stream; idempotencia downstream (guard B R1) | orden entre islas; no cruza streams comparables |
| `owner_input_seq` | cada isla de dominio, checkpointeado | **runtime ordering identity**: el orden en que ESA isla observó inputs — el que EXACT REPLAY reproduce | identidad de negocio; no sale del run |
| `runtime_ts` | cada isla de dominio, derivado en la admisión (R2) | **runtime logical time**: `DomainClock.Now()`, schedules relativos, timers, lógica time-based de Strategy/MM | retroceder; derivarse de `event_ts` |

`receive_ts` permanece liveness/telemetría (A §3). El caso raíz congelado: dos MarketEvents con `event_ts A < event_ts B` pueden ser observados `B then A` — y esa observación es MATERIAL (B tiene late corrections, BAR_CLOSE observation, no reevaluación retrospectiva). Por lo tanto **EXACT REPLAY jamás ordena por event_ts**: ordena por `owner_input_seq` grabado. En síntesis (BACKTEST), el orden no proviene de llegada física sino de la regla canónica §9 sobre `event_ts`/deadlines — y por eso BACKTEST no es EXACT REPLAY.

**R2 — caso raíz del runtime logical time:** un TimerFired admitido con runtime 09:31:00 seguido de un MarketEvent `event_ts=09:30:59.900`: `DomainClock.Now()` JAMÁS retrocede (el `runtime_ts` del evento es ≥ el del timer), mientras el evento entra igualmente a la barra 09:30 por su `event_ts` (asignación/corrección B §9). El evento tardío no atrasa el reloj: retrasa sólo su propio contenido. Event time y runtime logical time gobiernan cosas distintas y viajan separados en cada entrada del journal (§15).

## 6. DomainClock

Librería inyectable (`sdk`, paquete puro sin I/O — patrón D2-04 §8.7), única fuente de tiempo para decisiones market-dependent:

```text
DomainClock {
  Now() → Instant
      # ÚNICA fuente de tiempo para decisiones market-dependent; el dominio jamás
      #   llama time.Now() (extiende D2-05 R18 y B §8).
      # LIVE: runtime_ts del input corriente (R2): derivado por la isla en la
      #   admisión como max(runtime_ts previo, wall clock de admisión) — monotónico
      #   por construcción, owner_input_seq como tie-break — JAMÁS event_ts.
      # REPLAY: el runtime_ts journalado de la entrada corriente (§15/§21):
      #   reproduce la progresión real del run — incluido un timer ya vencido
      #   seguido de un evento atrasado — y el reloj nunca retrocede.
      # BACKTEST/HISTORICAL: reloj sintético no-decreciente derivado de la
      #   precedencia canónica §9 (max(runtime_ts previo, instante event-time del
      #   input sintetizado)); no imita latencia live.
  Schedule(timer_id, deadline, msg) → TimerHandle{timer_id, generation}
      # deadline en runtime logical time. Re-Schedule con el mismo timer_id =
      #   REPLACE: la generación vieja queda cancelada y el handle nuevo porta una
      #   generation distinta (§7).
      # LIVE: ctx.SendAfter durable (StateFun) — el firing regresa como TimerFired.
      # REPLAY: registro en el timer set virtual; el firing ocurre SOLO cuando el
      #   log/la síntesis lo entrega — jamás por espera real (cero sleeps).
  Cancel(handle)
      # LIVE: CancellationToken del SDK (verificado: statefun_sdk_go v3).
      # REPLAY: remoción del timer set virtual. La generación cancelada JAMÁS
      #   ejecuta dominio: un firing tardío de una generación ya cancelada o
      #   reemplazada (race físico en LIVE) es absorbido determinísticamente por
      #   el guard de generación (§7) — no es el firing vigente.
}
```

Semántica de identidad/cancelación: `timer_id` es explícito y namespaced por dueño (`bar_close:{stream}:{tf}`, `window:{window_id}:{boundary}`, `session:{calendar_id}:{session_date}`, `strategy:{strategy_id}:{purpose}` si V1 lo necesita, `mm:{op_key}:{purpose}` si aplica); el handle porta además una **`generation`** (R3): re-Schedule con el mismo `timer_id` = replace (cancela la generación vieja + nueva generation), de modo que un firing tardío de la generación vieja es reconocible y absorbible sin confundirse con el vigente — es exactamente la reprogramación de B §8 (`el timer se reprograma con NextSessionTransition`) y de D2-05 R18 (`next_reset_at` con piso prospectivo). NO es un framework de scheduling: sólo los usos enumerados por A/B/D2-05 (bar close, transiciones de sesión/ventana, health ticks de A, timer de Strategy/MM si sus requirements V1 los declaran).

## 7. Timer semantics — BAR CLOSE (decisión del mandato)

**OPTION 1 elegida: TimerFired se graba como input determinístico.** No se graban advances continuos de reloj (Option 2) ni mecanismos híbridos (Option 3). Justificación KISS: el scheduling de un timer es función determinística de los inputs previos (boundary del grid, `NextSessionTransition`, config), así que la única información no-derivable es CUÁNDO fue visible el firing al runtime — y eso es exactamente una posición en `owner_input_seq` (+ su `runtime_ts`, R2). Reglas congeladas:

- **Journalado completo (R3):** TODO TimerFired admitido por el dominio (que pasa el guard de generación) se journala en su posición de admisión con su `runtime_ts` — **sin change-detection para timers**. Razón: un firing puede programar el próximo timer, reemplazar/cancelar otro, avanzar el control flow o ser prerequisito de un firing futuro sin mutar estado observable ahora (health tick que re-agenda = ejemplo raíz: si t1 no está en el journal, el replay no ejecuta t1 → t2 puede no existir → divergencia futura). Esto cubre bar-close, session/window, health/freshness y los timers declarados de Strategy/MM. Redelivery del MISMO firing absorbido por guards (transporte/generación) sigue siendo NO-OP no journalado (§15).
- **Identidad + generación (R3):** un firing porte `(timer_id, generation)`. Si la generación ya no es la vigente (cancelada/reemplazada antes de procesarse), NO ejecuta dominio: el guard la absorbe determinísticamente (gap del contador, §15) y jamás se confunde con el firing vigente. EXACT_REPLAY valida cada TimerFired contra el timer set virtual reconstruido: generación que nunca existió en el prefijo reproducido ⇒ `REPLAY_LOG_CORRUPT` fail-visible; generación vieja ya cancelada/reemplazada ⇒ NO-OP determinista idéntico al live.
- En REPLAY el DomainClock virtual entrega el `TimerFired` del log en la posición grabada; el re-Schedule interno de la isla (que re-ejecuta lógica idéntica) crea el timer virtual y el firing inyectado lo absorbe — sin doble disparo (un timer virtual disparado se consume; el guard de closure identity de B hace el resto).
- "Que el timer existió" es derivable (lógica + inputs previos); "cuándo fue visible" es la posición grabada; su "ordering contra market events" es esa misma posición. Los tres requisitos de B §8 quedan cubiertos.
- El mismo mecanismo sirve Session/WindowTransition (§12): son timers cuyo payload dispara la transición; se journalan con la regla idéntica.

## 8. Ordering scope — qué orden se exige y dónde

No hay total order global de Echo. El orden requerido es **per-isla de dominio, sobre los inputs que esa isla consume**, y se serializa por construcción del runtime:

```text
Isla (StateFun keyed)          Orden exigido                          Cómo se garantiza
echo/market_stream (A, stream) eventos+health+config del stream      serialización por key; owner_input_seq
echo/market_analytics (B,      eventos+barriers+transiciones+         ídem — el interleaving timer↔evento
  stream)                      timers de cierre de ESA stream         de ESA stream es intra-key ⇒ exacto
echo/strategy_engine (B,       BAR_CLOSED de N streams +              serialización por key strategy_id;
  strategy_id)                 WINDOW_TRANSITION + timers propios     el interleaving cross-stream que la
                                                                      estrategia OBSERVA se journala (§10)
MM market gate (D2-04,         inputs de mercado vía evaluaciones     hereda el orden de la cadena de
  account:strategy)            y timers MM propios; lecturas pull     delivery + sus timers journalados
```

El orden **entre** islas (analytics→strategy→operation) viaja por mensajes `ctx.Send` encadenados que preservan el orden por stream origen; el único punto donde dos órdenes per-stream se MERGEAN es la isla strategy_engine (y el fan-out D2-04 aguas abajo, que ya serializa por op key). Ese merge es el único lugar del sistema donde la concurrencia cross-stream es observable por una decisión — y es exactamente lo que el journal por isla captura (§10). Fuera de ese punto, el orden per-stream basta. Este es el scope mínimo correcto: sin consensus sequencer, sin watermark framework, sin re-abrir la topología A/B.

## 9. Same-instant precedence / tie-breaking

**LIVE (run grabado):** a igual instante lógico, el dominio observa en **orden de admisión** (`owner_input_seq`) — regla congelada y reproducible porque la admisión está serializada por key y journalada. No hay regla sintética impuesta: la que hubo queda grabada. La pregunta del mandato ("09:31:00.000: trade 09:30:59.900, vence bar-close timer, cambia session state — ¿qué observa primero?") tiene respuesta determinística en ambos mundos:

- **EXACT REPLAY:** el orden grabado del run live — cualquiera que haya sido — se reproduce idéntico.
- **BACKTEST/HISTORICAL (síntesis, sin llegada física):** regla canónica congelada de precedencia al instante T:
  1. `RecoveryBarrier`/epoch markers posicionados por el escenario (frontera de validez de estado);
  2. `ConfigTransition` posicionadas por el escenario;
  3. `SessionWindowTransition` con instante T;
  4. `MarketEvent` con `event_ts ≤ T` — orden `(event_ts, stream_id, stream_seq)`;
  5. `TimerFired` con `deadline ≤ T` — orden `(deadline, timer_id)`.

  Con esa regla el caso 09:31:00.000 canónico responde: **transición de sesión → trade 09:30:59.900 (event_ts menor; entra a la barra 09:30) → timer 09:31 cierra la barra** — la Strategy observa la barra INCLUYENDO el trade. Ese es el resultado canónico; el run live B del caso duro (trade llegó físicamente DESPUÉS del timer) produce el otro resultado válido — y EXACT REPLAY lo reproduce porque el journal guarda el orden de llegada, no el canónico. **Dos órdenes, dos resultados válidos, ambos determinísticos:** por eso `event_ts` solo es insuficiente y por eso los modos están separados.

Ties intra-tipo congelados: market events por `(event_ts, stream_id, stream_seq)` (stream_seq resuelve ties intra-stream por construcción contigua); timers por `(deadline, timer_id)`; transiciones por `(instant, session_id|window_id)`.

## 10. Multiple streams

Consumidor multi-stream (ej. ES+NQ): **cada isla journals su propio orden observado** — la isla strategy_engine graba, para cada delivery admitido, una entrada de orden `(owner_input_seq, kind, source_stream, source_position_ref)` donde `source_position_ref` apunta a la posición del emisor (input_seq de la isla analytics emisora o stream_seq del evento que lo causó). El contenido NUNCA se duplica en esa capa: el journal del consumidor es **sólo orden** (§17), y el contenido se re-deriva durante replay del lado de mercado.

- **EXACT REPLAY (case K):** el injector coordina las islas: replays analytics(ES) y analytics(NQ) desde sus journals hasta la posición referenciada, y entrega a strategy_engine sus deliveries en SU orden journalado — el mismo merge que la Strategy observó en vivo, incluyendo el caso "10:00:00: NQ event, ES event, timer" con cualquier interleave físico que haya ocurrido. La observación es idéntica por construcción.
- **BACKTEST/HISTORICAL:** no hay journal: la síntesis aplica la regla canónica §9 — el merge es determinístico por `(event_ts, stream_id, stream_seq)` + precedencia. La estrategia observa un orden canónico (no el de ningún run live previo) — exactamente el claim permitido.
- **Evaluaciones pull cross-stream** (leer current-state de otro stream a mitad de evaluación): son lecturas de estado cuya reproducibilidad hereda la reproducibilidad del estado — exacta en EXACT REPLAY (los estados de todas las islas están en las posiciones journaladas). Sin trabajo adicional: es la consecuencia de journalar por isla.

Contraste con las alternativas del mandato: un `run_order` global único exigiría re-plasar los timers de B por un sequencer central (reabre B, hop extra en hot path — rechazado); el "tie-break determinístico al estilo watermark" en vivo NO reproduce la observación live (el merge físico ES la semántica del caso duro B/C — rechazado). Journal por isla es la opción más simple correcta: costo acotado a strategies (no × Account, case P) y cero cambios de topología.

## 11. Authority epoch / barrier ordering

El `RecoveryBarrier` (A §12) es un `MarketRuntimeInput` de primera clase con tres propiedades congeladas:

1. **Su posición es su significado:** la frontera demote→seed de B R7 ocurre en la posición de admisión del barrier; EXACT REPLAY la reproduce en esa posición relativa — `demote current E → last-known; escaleras E+1 nacen vacías; primer dato válido seed-ea` — aunque el primer evento del epoch nuevo tenga `event_ts` menor (case F/U de A/B).
2. **`owner_input_seq` cruza epochs sin resetearse** (coherente con B R7: el guard `stream_seq` cruza epochs; el scoping por epoch aplica sólo a la escalera event-time): la identidad de orden de runtime es independiente del epoch — el ordering identity "crosses epoch independently of event_ts" del mandato.
3. **En síntesis**, un barrier entra sólo si el escenario lo posiciona (recovery simulado); la precedencia §9 lo pone antes que cualquier evento del epoch nuevo.

Recovery replay / provenance (case G): los eventos RECOVERY_REPLAY/SNAPSHOT de A ya entran al canónico con `stream_seq` propio; su posición de admisión en las islas los hace reproducibles con su provenance intacta — sin silent mixing (A §9/§12: jamás blend; el journal preserva la separación por posición+provenance).

## 12. Session / window transitions

Las transiciones son **inputs agendados, no polling**: cada isla que las consume (analytics para grid/truncation, strategy_engine para WINDOW_TRANSITION de sus triggers) agenda con `DomainClock.Schedule` el próximo `NextSessionTransition`/boundary del dataset de calendario linearizado en esa isla (kache D2-05) y el firing llega como `TimerFired`→`SessionWindowTransition` (§7). Congelado:

- La versión del dataset que agenda es la **linearizada en la isla** (aplicación de config updates en orden de admisión); una corrección de calendario hot re-agenda prospectivamente (D2-05 R18 pattern) y la transición ya agendada bajo la versión vieja se cancela/reemplaza por `timer_id` — jamás se ejecuta la frontera vieja después de activarse la autoridad nueva.
- `breaks internos`, early close, truncation (B §7, R5) son efectos derivados de la transición en la isla analytics: reproducibles porque la transición es un input journalado en posición.
- En BACKTEST, la síntesis genera las transiciones del calendario snapshot del manifest (D2-05 §19) con la precedencia §9 — la misma frontera E del mandato (`market event + session close + timer comparten instante`) tiene UN resultado determinístico.

## 13. Config / calendar transitions (hot config durante live)

**Principio congelado:** si una config puede cambiar una decisión market-dependent durante live, su transición es reproducible (ConfigTransition journalada) o la config está pinned en el manifest. No hay tercer estado.

Clasificación de materialidad (qué se journala como ConfigTransition aplicada al consumidor):

| Clase de config | Materialidad | Tratamiento V1 |
|---|---|---|
| ExchangeCalendar revision (dataset consumido) | MATERIAL — cambia grid/truncation/transiciones | ConfigTransition inline {calendar_id, revision_hash, effective owner_input_seq}; decisores previos no se reescriben (D2-05 prospectivo; case I) |
| Switch de autoridad MARKET_DATA (A §9) | MATERIAL | la config del switch + el RecoveryBarrier resultante, en posición |
| Rollover mapping (A §14/D2-05 §6) | MATERIAL | ConfigTransition {mapping_row, effective seq} — case H |
| MarketRequirements catalog (builders/warm-up, B §13/§16) | MATERIAL | ConfigTransition; expansión de lookback dispara warm-up — reproducible |
| Strategy config / MM market config | **PINNED en manifest V1** (D2-01: snapshot embebido; B §15: resuelta al registrar); si una semántica futura permite hot, será ConfigTransition explícita — nunca switch silencioso (precedente: B eliminó `bars.late_correction` toggle) | manifest + ConfigTransition si existiera |
| Readiness/view changes que abren/cierran gates (StreamState aplicado al consumidor) | MATERIAL para la decisión gateada | ConfigTransition de referencia {stream_id, epoch, readiness, reasons, applied seq} — contenido autoridad en A (StreamState compactado), orden capturado en el consumidor |
| Liveness/freshness thresholds puramente telemetry | NO material salvo que gateen (ver fila anterior) | no se journalan |
| Binding/routing catalogs que no tocan decisiones de mercado del boundary C | NO material para C | autoridad de sus dominios |

Sin framework de revisiones nuevo (D2-01/PROHIBICIÓN D2-04): la ConfigTransition es un hecho con payload/ref + `revision_hash` cuando la fuente ya lo provee (calendar D2-05, RuleSet D2-05C) — reusa el concepto snapshot-embebido/snapshot-en-manifest existente, no crea versionado universal. Una ConfigTransition con fuente sin hash propio lleva el digest del payload (identidad del hecho, no framework).

## 14. Rollover / source-switch transitions — representación

- **Source switch** (A §9): se representa por el par congelado `[ConfigTransition{switch}] → [RecoveryBarrier{epoch++}]` en posición — el switch es explícito, validado por servabilidad, con readiness loss; NUNCA cambia `stream_id` ni Contract; EXACT REPLAY reproduce validación→barrier→rebuild→READY con los mismos inputs (case F/J de A).
- **Rollover** (A §14/D2-05 §6): `ConfigTransition{rollover mapping}` en posición — nace demanda de la stream nueva (`(NQ,NQH7)` SUBSCRIBING→READY), la vieja RETIRING hasta RELEASE; la Strategy procesa H7 sólo cuando el transition es efectivo y H7 requirements READY (B §21); la Operation vieja permanece independiente; **no auto-roll** — un replay que "rodara solo" sería un defecto, no una optimización (case H).

## 15. Recorded deterministic boundary — qué DEBE persistirse

```text
Run Recording (conceptual) = RunManifest + ReplayAnchor (R1) + DeterministicInputLog
                             + contenido canónico

ReplayAnchor (R1): identidad inmutable del estado inicial del run — el corpus EXACTO
  de MarketEvents normalizados + snapshots de calendario/config que el warm-up B §17
  del run consumió, capturado UNA vez al iniciar el run grabado; refs + digest en el
  RunManifest (§20); misma retención que el recording; jamás se re-deriva de
  MarketHistorySource en replay.

DeterministicInputLog (per run, per isla consumidora):
  entry {
    run_id, owner_key            # isla: stream_id | strategy_id | (op key MM timers)
    owner_input_seq              # runtime ordering identity (contiguo permitiendo
                                 # gaps = no-ops absorbidos por guards, §22)
    runtime_ts                   # runtime logical time derivado en la admisión (R2):
                                 # monotónico no-decreciente por isla; JAMÁS event_ts
    input:                       # MarketRuntimeInput, en una de dos formas:
      inline                     # RecoveryBarrier, ConfigTransition, TimerFired
                                 # {timer_id, generation, deadline},
                                 # SessionWindowTransition, readiness-ref — pequeños,
                                 # autosuficientes
      ref                        # MarketEvent → (stream_id, stream_seq) — contenido
                                 # vive en el topic canónico; NUNCA se duplica el tick
                                 # en el journal (KISS, single content authority)
    source_ref?                  # en islas consumidoras (strategy_engine): posición
                                 # del emisor — (source_stream, source_input_seq)
                                 # (§10: journal de orden sin contenido)
  }

Regla de journalado (repair R1, criterio de materialidad): se journala todo input
admitido cuya omisión podría cambiar una observación de dominio presente o futura —
el criterio es "CAN THIS INPUT AFFECT PRESENT OR FUTURE DOMAIN OBSERVATION?", NO
"muta estado ahora". ALWAYS JOURNAL: todo TimerFired admitido (R3: sin
change-detection para timers); ConfigTransition material (§13); RecoveryBarrier;
Session/WindowTransition cuando son inputs separados; refs de MarketEvent canónicos
que pasan guards y afectan la isla; deliveries/refs cross-island necesarios (§10).
MAY OMIT: redeliveries de transporte absorbidos ANTES del dominio; duplicados exactos
que guards hacen NO-OP (stream_seq, generación de timer); facts telemetry-only sin
efecto presente NI futuro sobre control flow. La omisión es segura por construcción
(lo omitido es no-observable para el dominio); el gap de owner_input_seq la evidencia
y el replay la re-absorbe idénticamente porque los guards son determinísticos.
```

Cobertura mínima exigida (checklist del mandato): eventos canónicos aceptados ✓ (ref al canónico); runtime/order identity ✓ (`owner_input_seq`); runtime logical time ✓ (`runtime_ts`, R2); epoch markers/RecoveryBarriers ✓ (inline); timer firings ✓ (inline, completos — R3); calendar/session authority/version ✓ (manifest + ConfigTransition); config changes materiales ✓ (§13); source-switch/rollover ✓ (§14); run manifest/semantic versions ✓ (§20); replay anchor / estado inicial ✓ (R1: corpus de warm-up + digest + readiness assertion). **NO se graba:** operation/fill event sourcing (D2-04 tiene sus authorities; R12 intacto), todo Echo, eventos crudos vendor pre-normalización (rompería vendor-independence), barras derivadas (dual authority), estado derivado serializado (el anchor es corpus + digest, no snapshot de estado — R1).

`echo.market-events.v1` SOLO es **insuficiente y se declara**: carece de timers, config, transiciones y del orden entre islas — un replay desde el topic canónico reconstruye la proyección final, no las observaciones (B §10 ya lo declaró; aquí se cierra). Y **retención ≠ recording contract**: la correctez exige que la combinación manifest+journal+contenido sea recuperable por el horizonte de replay del run; la retención física de Kafka es config (days) y el archival a object storage es DEFERRED_DEBT (§28). Un run grabado cuyo contenido canónico fue purgado ⇒ `REPLAY_SOURCE_MISSING` fail-visible en replay attempt (§18) — jamás replay parcial silencioso.

## 16. Recording point

**Opción E elegida (combinación mínima): post-arbitración (C) + control inputs journalados en la frontera de admisión de cada isla.** Evaluación de las opciones del mandato: **(A) vendor packets pre-normalización** — rechazado: acoplaría el replay a la normalización del vendor y violaría vendor-independence; **(B) candidatos post-normalización** — rechazado: incluye lo que el arbitraje suprimió (doble evaluación en replay); **(C) aceptados post-arbitraje** — base correcta (es lo que el dominio observó) pero insuficiente solo (sin timers/config — §15); **(D) barras derivadas** — prohibido como autoridad (dual authority, §17); **(E) C + control** — elegido. Cumple los cuatro requisitos del mandato: exact technical replay ✓; vendor-independent ✓ (el dominio re-consume el envelope canónico, no el vendor); no double evaluation ✓ (una entrada por input admitido); reproduce epoch y late arrival order ✓ (barrier inline + posiciones).

Grabación en el punto de admisión (no en un observador lateral): el mismo guard `stream_seq`/`owner_input_seq` que aplica el input emite la entrada del journal por **egress transaccional EXACTLY_ONCE en la misma frontera de checkpoint** (patrón R14/I16 de D2-04) — un input checkpointeado es una entrada durable; un checkpoint abortado aborta la transacción (entrada jamás visible) y el replay del ingress la re-admite idempotentemente. Sin ventana de pérdida, sin writer lateral. El replay anchor (R1) es la excepción natural: se captura UNA vez al iniciar el run grabado (los eventos normalizados exactos que el warm-up B §17 consumió, refs inmutables + digest + readiness assertion post-warm-up), queda inmutable y muere con la retención del recording (§28-R-C2); el hot path de decisiones no cambia.

## 17. BAR_CLOSED authority decision — **B: re-derivado**

`BAR_CLOSED`/`BAR_UPDATED` **NO se graban como input autoritativo**: se re-derivan durante replay desde los market/control inputs registrados, ejecutando la MISMA lógica de B (builders, cierre por natural-close o TimerFired, corrección de ventana única) sobre la MISMA secuencia. Es la preferencia KISS del mandato confirmada contra los cinco casos de prueba:

- **late corrections:** el journal pone el evento tarde DESPUÉS del TimerFired (posición live) ⇒ re-derivación produce evaluación sobre X y luego proyección X' — exactamente el caso duro B del mandato; el orden invertido (case C) produce el otro resultado válido. ✓
- **exact decision observation X:** la entrega del cierre derivada ocurre en la misma posición relativa ⇒ la Strategy re-observa X (no X'). ✓
- **session truncation:** las transiciones journaladas reproducen truncamientos y grid (B §7). ✓
- **authority switch:** el barrier journalado reproduce descarte de forming/demote→seed (B §19/§20). ✓
- **timers:** TimerFired journalados reproducen cierres sin próximo tick (case D). ✓

**Dual authority evitado por construcción:** hay una sola autoridad de contenido (los market/control inputs); los journals de las islas consumidoras (§10) guardan SOLO orden referencial, con integridad referencial verificable (el `source_ref` debe resolverse contra la posición del emisor) — mismatch ⇒ `REPLAY_LOG_CORRUPT` fail-visible, no replay inventado. Grabar BAR_CLOSED como autoridad habría creado dos verdades (barra grabada vs estado reconstruido) y habría necesitado invalidación mutua; la re-derivación la elimina en vez de resolverla.

## 18. EXACT_REPLAY / REPLAY_LIVE_RUN (modo 1)

```text
run_mode = REPLAY (formalización de D2-04 I11)
objetivo: reproducir las decisiones market-dependent de un run live previo.
requiere: RunManifest + ReplayAnchor (R1) + DeterministicInputLog completo
          + contenido canónico recuperable.
```

- **Anclaje (R1):** antes de `owner_input_seq=0`, el driver reconstruye el estado de dominio inicial re-ejecutando el corpus de warm-up grabado (replay anchor) con la MISMA lógica B §17 — mismos builders, calendario snapshot y requirements del manifest — y verifica el digest del corpus y la readiness assertion del anchor. Anchor ausente ⇒ `REPLAY_ANCHOR_MISSING`; digest/readiness en mismatch ⇒ `REPLAY_ANCHOR_INVALID`; ambos fail-visible. PROHIBIDO volver a consultar `MarketHistorySource` en replay y asumir igualdad.
- **Inyección (§21):** el injector re-maneja los paquetes puros de dominio con DomainClock virtual; cada isla consume SUS entradas en `owner_input_seq` con `Now()` = `runtime_ts` journalado (R2); las entregas inter-isla ocurren en las posiciones `source_ref` journaladas.
- **Efectos:** el replay produce registros de decisión (decision observations, Signals, decisiones MM de mercado) hacia un **sink de observación**; `run_mode=REPLAY` gatea todo egress físico (orders/venue) — un replay jamás toca un venue. Las decisiones de ejecución física (sizing monetario sobre Account state, orders) se re-derivan sólo si su input de mercado está en el boundary — el claim es market-dependent decisions, no replay económico completo (D2-04 R12).
- **Garantía exacta:** same manifest + same anchor + same journal + same code ⇒ same decisions (§3). Ante `REPLAY_SOURCE_MISSING`/`REPLAY_LOG_CORRUPT` ⇒ fail-visible; sin aproximaciones.
- **Relación con recovery:** EXACT REPLAY es re-ejecución para reproducción/forense/verificación; **NO es la autoridad de recovery del path de ejecución** — un `COLD_RECOVERY_REQUIRED` de D2-04 no se levanta por replay (§23).

## 19. HISTORICAL / BACKTEST / NEW_RUN (modo 2)

```text
run_mode = BACKTEST (HISTORICAL)
objetivo: evaluar Strategy/MM sobre historia canónica; NUNCA clona un run live.
```

- Fuente: `MarketHistorySource` (A §16) / historia canónica — **raw normalized MarketEvents** event-time ordenado (contrato B §18: clases A/B con identidad, cutover capability-driven R4).
- Síntesis: la secuencia canónica se construye con la precedencia §9 sobre `event_ts`/deadlines + transiciones del calendario snapshot del manifest + config snapshots inyectados (D2-05 §19: Calendar/RuleSet/DayBoundary/Contract) + warm-up B §17 para estado inicial + un runtime logical clock sintético no-decreciente (R2: cada input sintetizado recibe `runtime_ts = max(runtime_ts previo, su instante event-time)` — sin imitar latencia live).
- Warm-up de un NEW RUN en vivo: mismo camino — historia canónica + misma semántica de builder (B §17); el run live arranca su `owner_input_seq` en 0 post-warm-up.
- **Claim congelado:** NO reproduce las decisiones de un run live que tuvo arrival disorder, outages, source switches o late corrections — para eso existe EXACT_REPLAY. Las dos palabras jamás se mezclan bajo un solo "REPLAY" en docs/implementación.
- Coexistencia: BACKTEST corre in-process/offline con los mismos paquetes puros (D2-04 §8.7, constraint D1) — sin `*_live` vs `*_backtest`.

## 20. Run manifest / provenance

```text
RunManifest (uno por run, publicado al iniciar y actualizado sólo por ConfigTransitions):
  run_id (UUIDv7), run_mode (LIVE|SHADOW|DEMO|REPLAY|BACKTEST), replayed_run_id? (si REPLAY)
  strategy config/reference          # embebida efectiva (D2-01 snapshot style)
  MM config/reference                # embebida efectiva según D2-01/D2-05
  market_semantics_version           # bars/policy V1 run-pinned (B §9)
  calendar snapshot {calendar_id, revision_hash} por stream consumida   # D2-05
  source capability/config provenance                                   # A §11 bindings
  starting Contract/stream selection (in-force + pinneadas al arranque)
  relevant config versions/hashes    # requirements catalog digest, etc.
  replay anchor                      # R1: {kind: WARMUP_CORPUS, corpus refs + digest,
                                     #      readiness assertion post-warm-up} —
                                     #      identidad inmutable del estado inicial;
                                     #      run sin anchor ⇒ no replayable desde t0
  run_time_origin                    # instante de arranque del run (R2: base de
                                     # interpretación de los runtime_ts journalados)
  recording identity/range           # topic/particiones/rango del DeterministicInputLog
  MM/economic snapshots cuando el run lo exija (D2-05 §19)
```

Reusa los conceptos congelados: snapshot-embebido (D2-01), snapshot-en-manifest (D2-05 §19/LIVE vs REPLAY), sin revision framework nuevo (prohibido por D2-01/D2-04). Config hot durante el run = ConfigTransition journalada (§13) — el manifest inicial NO pretende bastar solo: la transición declara cuándo se hizo efectiva (posición) y qué decisiones previas no se reescriben. El manifest es el GIVEN (a) del invariante §3; dos runs con manifests distintos no prometen igualdad aunque el diff sea mínimo.

## 21. Replay injection

```text
ReplayDriver (proceso offline, NO microservicio):
  in:  RunManifest + ReplayAnchor + DeterministicInputLog + echo.market-events.v1
       (contenido)
  hace:
    1. valida integridad: manifest ↔ journal range; owner_input_seq estrictamente
       creciente (gaps = no-ops permitidos); runtime_ts no-decreciente por isla
       (R2); source_refs resolubles — sino REPLAY_LOG_CORRUPT fail-visible
    2. ancla (R1): re-ejecuta el corpus de warm-up del replay anchor con la MISMA
       lógica B §17 sobre los mismos builders (calendario/requirements del
       manifest); verifica digest del corpus + readiness assertion — ausencia/
       mismatch ⇒ REPLAY_ANCHOR_MISSING / REPLAY_ANCHOR_INVALID fail-visible
       (jamás MarketHistorySource)
    3. instancia los paquetes puros de dominio (analytics, strategy, MM market
       logic) con DomainClock virtual y las mismas guards — cero código alternativo
    4. re-maneja por isla en owner_input_seq; DomainClock.Now() = runtime_ts
       journalado de cada entrada (R2, JAMÁS event_ts); coordina entregas
       inter-isla por source_ref (§10); barriers/transitions/config en posición;
       todo TimerFired del log valida su (timer_id, generation) contra el timer
       set virtual reconstruido (§7)
    5. emite decision log al sink de observación (run_mode=REPLAY sin egress físico)
  fuera de alcance V1: replay distribuido multi-nodo, replay desde punto medio
    (requeriría snapshot intermedio grabado — DEFERRED_DEBT), replay de ejecución.
```

Fundamento físico: el patrón de contexto mock con `SendAfter`/`CancellationToken` ya existe (`v3/core/internal/functions/testutil/statefun_mock.go`, `v3/e2e/execution_engine.go:344-349`) — el driver es la extensión de ese harness al dominio de mercado, no infraestructura nueva. Obligación de certificación (D6): golden run live grabado ⇒ replay in-process produce decision log idéntico (bit-a-bit en los campos semánticos).

## 22. Idempotency / redelivery

- **Canonical topic AT_LEAST_ONCE:** dedup downstream por `stream_seq` guard (B R1) — intacto; un redelivery jamás se journala (§15: duplicados que guards hacen NO-OP son MAY-OMIT) ni dispara trigger (guard de closure identity B §22).
- **Journal EXACTLY_ONCE:** la entrada cruza en la transacción del checkpoint (§16): sin duplicados ni pérdidas; replay assertion de monotonicidad por isla — `owner_input_seq` estrictamente creciente (gaps = no-ops permitidos) y `runtime_ts` no-decreciente (R2); regresiones = corrupto fail-visible.
- **Timers (R3):** un redelivery del mismo firing es absorbido por los guards (transporte/generación) como NO-OP sin segunda entrada; en replay, todo TimerFired del journal se valida contra el timer set virtual reconstruido: generación vieja cancelada/reemplazada ⇒ NO-OP determinista idéntico al live; generación inexistente en el prefijo reproducido ⇒ `REPLAY_LOG_CORRUPT` (§7).
- **Ingest replay post-restart:** los offsets commitean con el checkpoint (D2-04 §8.5); los inputs re-entregados encuentran `owner_input_seq ≤ restaurado` ⇒ re-absorbidos por guards, sin segunda entrada ni segunda evaluación (case L).
- **Redelivery del propio journal en replay:** el driver consume el journal con offset propio y assertion de unicidad por `owner_input_seq` — duplicado ⇒ corrupto fail-visible.

## 23. Restart / exact replay / cold / historical — cuatro cosas distintas

| Situación | Autoridad | Qué NO se hace |
|---|---|---|
| **NORMAL RESTART** | checkpoint StateFun/Flink de cada isla (D2-04 R11, B R3) — incluye `owner_input_seq` y mm_state | NO se re-reproduce el journal como sustituto; NO se recalcula decision state desde historia corregida |
| **EXACT REPLAY** | recording boundary del run (manifest + replay anchor + journal + contenido) | NO toca venues; NO es recovery del live; NO re-consulta `MarketHistorySource` (R1); requiere anchor + recording completos |
| **COLD DISASTER** | `COLD_RECOVERY_REQUIRED` fail-closed (D2-04 R11): reconciliar venue + bloquear nuevo riesgo + bootstrap operador | **incluso CON journal**: el journal cubre el input seam de mercado/strategy (el decision state analítico de Strategy ES re-derivable por replay completo), pero `mm_state` y la exposición viva dependen del stream de ejecución que D2-04 R12 no graba ⇒ el path monetario permanece fail-closed; sin continuación inventada |
| **NEW HISTORICAL RUN** | MarketHistorySource + síntesis canónica (§19) + warm-up B §17 | NO claim de reproducir arrival disorder de un run previo |

El cierre del requisito abierto de B R3 ("COLD ... salvo que exista un recorded deterministic boundary suficiente") queda así: el boundary es suficiente para el estado ANALÍTICO de mercado/strategy (re-derivable), insuficiente para el estado de ejecución (mm_state) — la frontera con D2-04 queda explícita y sin ambigüedad.

## 24. MM boundary

C posee únicamente el seam de mercado/tiempo de MM:

- **Clock inyectable:** los timers market-dependent de MM (re-evaluaciones, trailing por cadencia, si su config los declara) son `DomainClock` timers — journalling/idempotencia/replay idénticos a §7. En D2-04 los delays usan `SendAfter` (mm_engine.go:588-625): ese uso se subsume bajo `timer_id` namespaced MM.
- **Orden inyectable:** los inputs de mercado de MM llegan por la cadena delivery (signals desde evaluaciones Strategy + transiciones + timers) cuyo orden es el journalado; sus lecturas pull de MarketContext (B §23) observan el estado en la posición de la invocación — reproducible en EXACT REPLAY.
- **Propiedad preservada (D2-04 R5):** same ordered input sequence ⇒ same MM decisions — C garantiza el componente market/time de esa secuencia; el componente execution (fills/acks) sigue siendo autoridad D2-04. El replay compuesto exacto de AMBOS requiere grabar ejecución — explícitamente fuera (R12).
- **Sin duplicación de market state por Account** (B §4/§23 intacto): MM lee read models compartidos; C no añade ninguna superficie por cuenta. C no se convierte en execution event sourcing ni en contabilidad de MoneyManagement.

## 25. Physical topology (V1)

```text
                                   ┌────────────────────────── offline ──────────────────────┐
adapters → echo.market-feed-       │ ReplayDriver (in-process, paquetes puros + DomainClock   │
candidates.v1                      │ virtual) ← manifest + journal + contenido                │
        ↓                          └──────────────────────────────────────────────────────────┘
echo/market_stream (A, key stream_id)                    [EXISTENTE A]
  + C: owner_input_seq checkpointeado; journal egress transaccional
        ↓ egress AT_LEAST_ONCE (canónico)          ↓ egress EXACTLY_ONCE (journal, refs+control)
echo.market-events.v1 (contenido)               echo.market-run-journal.v1 (key owner_key)
        ↓ ingress                                        ↓
echo/market_analytics (B, key stream_id) ── ctx.Send BAR_CLOSED/… ──→ echo/strategy_engine (B, key
  + C: owner_input_seq; journal egress                                    strategy_id)
        ↓ egress compactado snapshots                                  + C: owner_input_seq;
echo.market-bars.v1                                       journal de ORDEN (source_refs) egress
        ↓                                                        transaccional
echo/operation (D2-04, key acct:strategy) ← echo.signals.v1 ←──────────┘
  MM market gate: DomainClock timers + lecturas MarketContext; + C: journal de timers MM
echo.market-run-manifests.v1 (compacted, key run_id) ← publicado al iniciar run (§20)
```

- **Dónde se asigna el orden:** en cada isla, en la admisión (`owner_input_seq`, checkpointeado).
- **Dónde se graba:** egress transaccional `echo.market-run-journal.v1` (refs+control, EXACTLY_ONCE, misma frontera de checkpoint) + `echo.market-run-manifests.v1` (compacted, con replay anchor y run_time_origin) + contenido canónico con retención de recording + replay anchor capturado una vez al iniciar el run (R1: corpus de warm-up refs+digest) (§15/§28).
- **Dónde vive/inyecta DomainClock:** librería `sdk` pura; LIVE impl sobre SendAfter+CancellationToken; virtual impl en el ReplayDriver y en BACKTEST.
- **Replay adapter/injector:** ReplayDriver offline (§21); cero flota nueva, cero Kafka Streams/Beam/CEP.
- **Quién consume inputs:** las islas existentes A/B/D2-04 — sin consumidores nuevos.
- **Qué queda StateFun checkpointeado:** todas las islas existentes + los contadores `owner_input_seq` (estado aditivo en las mismas ValueSpec). **Qué es derivado:** barras, readiness, evaluaciones, decisiones — nada de esto es autoridad grabada.
- Componente lógico nuevo total: **2** (DomainClock-lib + ReplayDriver) — el mínimo que el mandato permite ("if one new logical component is enough, prefer it"; el clock y el driver son inseparables por contrato).

## 26. Echo V3 reuse/adapt

| Pieza V3 | Disposición | Evidencia |
|---|---|---|
| `ctx.SendAfter` + `CancellationToken` (StateFun SDK Go v3) | **REUSE** — mecanismo LIVE de DomainClock | `v3/core/internal/functions/mm_engine.go:588-625`; mock `statefun_mock.go:193-204` (cancelación) |
| Egress transaccional EXACTLY_ONCE en frontera de checkpoint | **REUSE patrón** (D2-04 R14/I16) para journal egress; requiere config `EXACTLY_ONCE` + `read_committed` (requisito carried de D2-04 R2) | D2-04 §5.6/§8.3; module.yaml hoy sin delivery semantics |
| kache / compacted hot-config con tombstones | **REUSE** para manifests y para el canal de ConfigTransitions (aplicación en orden de admisión por isla) | `v3/gateway/internal/symbol_mapping_handler.go`; `v3/sdk/kache/*` |
| Contexto mock/e2e con SendAfter (harness in-process) | **ADAPT** — base del ReplayDriver | `v3/e2e/execution_engine.go:344-349`; `testutil/statefun_mock.go` |
| Paquetes de dominio puros sin infra (boundary Q14) | **REUSE convención** — los paquetes de mercado B y la lógica MM corren en LIVE y en el driver | D2-04 §8.7/§10 |
| ValueSpec/keyed state por isla | **EXTEND aditivo**: + `owner_input_seq` (C-owned) en islas A/B/strategy_engine | patrón `v3/sdk/statefun` ValueSpec |
| run_mode/run_id en entidades | **NEW físico** (concepto ya congelado D2-04 I11; no existe en código — verificado) | grep baseline: sólo `curve_run_id` Lab |
| DeterministicInputLog / journal topic / manifests / replay anchor / DomainClock / ReplayDriver | **NEW** (no existe nada físicamente) | grep baseline sin market/replay/clock |
| Archival object storage del recording; replay desde punto medio; replay multi-nodo | **DEFERRED_DEBT** | §28 |
| Bridge MT5 / lab_curves / Forge ingest | unrelated | — |

## 27. Scale

- **Recording cost ∝ streams × control-inputs** (timers/transiciones/barriers/config — NO ticks: los eventos van por ref) **+ strategies × deliveries** (journal de orden) + retention del canónico compartido **+ replay anchor una vez por run** (R1: acotado por MarketRequirements — es el mismo span que el warm-up ya leyó una vez; no escala con la duración del run). Cero multiplicación × Account (case P): 200 cuentas × S1 = 1 stream journalada, 1 strategy journal, 1 anchor, 0 journals extra.
- **Replay cost ∝ tamaño del log** (offline, sin SLA de hot path).
- **Orden/admisión:** un contador checkpointeado por isla — O(1) por input.
- **Timer density:** ya dimensionada por A §20/B §28-B5 (trivial en V1); el journal no añade timers.
- **El hot path no toca storage síncrono:** el journal egress es asíncrono transaccional (misma filosofía R14: durabilidad en la frontera de checkpoint, sin I/O en decisiones).

## 28. Risks / debts

- **R-C1 — Fidelity in-process vs runtime:** el ReplayDriver re-maneja paquetes puros, no el runtime StateFun completo; la equivalencia (mismas guards, mismos sends) es obligación de certificación D6 con golden replay (§21). Riesgo de implementación, no de contrato.
- **R-C2 — Retention como prerequisito del recording:** la purga del contenido canónico destruye la replayabilidad aunque el journal sobreviva; el replay anchor (R1) comparte la retención del recording — purgar el recording purga el anchor. `REPLAY_SOURCE_MISSING` es fail-visible pero no recupera nada. Mitigación V1: retención config explícita por horizonte + alerta; archival = deuda.
- **R-C3 — Cobertura del recording de gates:** si una superficie futura afecta decisiones sin pasar por MarketRuntimeInput (nuevo tipo de gate no clasificado material), el recording la pierde silenciosamente. Mitigación congelada: toda nueva superficie de gate DEBE clasificarse en la tabla §13 en su design review — requisito de proceso, verificable en review.
- **R-C4 — Timer visibilidad en LIVE:** el `owner_input_seq` captura el interleave físico real; runs con interleavings patológicos (timer visible muy tarde por backpressure) se reproducen fieles pero pueden diferir del canónico — comportamiento correcto, documentado para no confundir con bug.
- **R-C5 — Throughput del journal egress:** una entrada por input state-changing; en régimen normal domina el ref de eventos (pequeño). Riesgo bajo; medir en D6 junto al benchmark de A §20.
- **R-C6 — gaps de `owner_input_seq`:** los gaps (= no-ops absorbidos) son legítimos; la distinción gap-legítimo vs entrada-perdida descansa en la atomicidad del egress transaccional (R14 pattern). Si esa config no se certifica (D2-04 R2 carried), el recording no es auditable — dependencia explícita.
- **R-C7 — Decision state re-derivado en cold:** el re-anclaje analítico post-cold por replay completo existe como capacidad conceptual pero su procedimiento operacional no se diseña en V1 (queda con el DR de D2-04 R9); el fail-closed manda mientras tanto.
- **R-C8 — Run manifest distribution:** el manifest es local al run; su consulta operacional (¿qué runs están grabados y completos?) necesita un índice — V1: topic compacted + query operacional manual; debt de superficie si crece.
- **R-C9 — Runs sin anchor no son replayables (R1):** un run que arrancó sin capturar el replay anchor queda permanentemente sin EXACT REPLAY desde t0 (`REPLAY_ANCHOR_MISSING`); la captura debe ocurrir AL INICIAR el run — no existe anclaje tardío sin asumir igualdad de historia (prohibido). Decisión que interactúa con OD-C1: opt-in diferido = compromiso en el arranque del run, no retroactivo.
- **R-C10 — Monotonía de `runtime_ts` es obligación de implementación (R2):** la derivación `max(previo, wall clock)` protege contra regresión de NTP/reinicio de reloj; una implementación wall-only violaría el invariante. Verificación barata: assertion de no-decreciente por isla en el driver (§21) + telemetría live. Residual declarado: un reloj de pared congelado no es detectable como corrupto — `runtime_ts` seguiría avanzando sólo por admisiones (degradación visible en telemetría, no corrupción del recording).

## 29. A/B integration notes

```text
A_INTEGRATION_NOTE:
C NO reabre A. Sobre la topología congelada de A añade, aditivamente:
(1) owner_input_seq checkpointeado en echo/market_stream y echo/market_analytics
    (campo de estado C-owned, sin cambios semánticos A);
(2) journal egress transaccional EXACTLY_ONCE desde ambas islas (refs de eventos +
    control inline: barriers ya emitidos por A, TODO TimerFired admitido incl.
    health/freshness — R3 —, config aplicada) — nueva spec de egress en module.yaml,
    mismo mecanismo de registro;
(3) respuesta a la pregunta abierta A §21: el replay NO inyecta health/readiness
    desde el manifest — lo RE-DERIVA de los inputs journalados con la maquinaria
    normal de A (readiness es función determinística de events+health+config
    journalados); el manifest porta capabilities/provenance, no estados derivados;
(4) retención de echo.market-events.v1 pasa a tener un rol de recording cuando el
    run se graba (requisito §15/§28-R-C2) — A §16/§17 quedaban abiertos a esto.
```

```text
B_INTEGRATION_NOTE:
C NO reabre B y cierra sus dos requisitos declarados:
(1) B §8/§22 (autoridad de timers LIVE=wall-clock/REPLAY=orden registrado, interleaving
    determinístico): resuelto por DomainClock + owner_input_seq + TimerFired journalado
    (§6/§7) — B consume la librería sin cambiar su lógica de cierre;
(2) B §10/§24 (EXACT REPLAY debe reproducir las observaciones X, no reconstruir X'):
    resuelto por el DeterministicInputLog + re-derivación de BAR_CLOSED (§17).
Añade aditivamente: owner_input_seq + journal de ORDEN (source_refs) en
echo/strategy_engine; MM timers bajo DomainClock; y los read models de B (bars
snapshot/current state) quedan como las superficies que la evaluación observó en la
posición journalada — sin cambio de contrato. El warm-up B §17 de un NEW RUN sigue
siendo el camino de inicialización previo a owner_input_seq=0 del run; EXACT REPLAY
re-ejecuta el CORPUS de warm-up grabado (replay anchor, R1) con esa MISMA lógica B
para reconstruir el estado inicial antes de seq=0, y jamás re-consulta
MarketHistorySource en replay — el seam live de historia queda exclusivo de
NEW RUN/NEW STRATEGY y del rebuild de epoch.
```

Ambos notes son adiciones sobre superficies existentes; ninguna re-classifica decisión de A/B. La integración D2-06 (A+B+C) debe presentar estos tres puntos como los únicos campos de estado nuevos del bloque.

## 30. Acceptance cases A–P

- **A — SAME INPUT SAME DECISION:** invariante §3; misma manifest + mismo orden journalado/canónico + mismo código ⇒ mismas decisiones/observaciones/triggers. Estructura PASS; certificación física = golden replay D6 (§21).
- **B — LATE AFTER BAR CLOSE:** live: TimerFired pos i → evaluación observa X → trade pos i+1 → corrección X' sin reevaluación. Replay: mismas posiciones journaladas ⇒ re-derivación idéntica (X, decisión, X'). **PASS** (§17).
- **C — LATE BEFORE BAR CLOSE:** live: trade pos i → TimerFired pos i+1 ⇒ evaluación incluye el evento. Replay idéntico por posiciones. **PASS**.
- **D — NO NEXT TICK:** TimerFired del boundary journalado ⇒ replay cierra 09:31 con datos hasta 09:30:50, sin tick sintético (§7). **PASS**.
- **E — SAME-INSTANT SESSION TRANSITION:** live: orden de admisión journalado (un resultado, reproducible). Síntesis: precedencia canónica §9 (transición → eventos ≤ T → timers ≤ T). **PASS** (§9).
- **F — AUTHORITY SWITCH:** barrier journalado en posición ⇒ demote→seed reproducido en el mismo orden relativo aunque el epoch nuevo traiga event_ts menor; owner_input_seq cruza epochs (§11). **PASS**.
- **G — SOURCE RECOVERY:** eventos de recovery con provenance + posiciones journaladas; barrier ordering preservado; sin silent mixing (§11/§15). **PASS**.
- **H — ROLLOVER:** ConfigTransition de rollover en posición ⇒ transición reproducida exacta; H7 sólo post-READY; Operation vieja independiente; no auto-roll (§14). **PASS**.
- **I — CALENDAR HOT CORRECTION:** ConfigTransition {revision_hash} en posición de linearización ⇒ punto efectivo preservado; decisiones previas no reescritas; jamás "calendario más nuevo" retroactivo (§13). **PASS**.
- **J — CONFIG CHANGE:** config material ⇒ ConfigTransition en posición (o pinned en manifest si V1 lo congela); no-material declarado no-journalado; reproducible o pinned, sin tercer estado (§13). **PASS**.
- **K — MULTI-STREAM:** ES+NQ+timer: journal de orden por isla ⇒ el merge observado live se reproduce idéntico; síntesis usa merge canónico `(event_ts, stream_id, stream_seq)` + precedencia (§10). **PASS**.
- **L — KAFKA REDELIVERY:** canonical: guard stream_seq absorbe; journal: EXACTLY_ONCE en frontera de checkpoint + monotonicidad; replay: unicidad por owner_input_seq ⇒ ningún redelivery se vuelve segundo input de dominio (§22). **PASS**.
- **M — NORMAL RESTART:** checkpoints (con contadores); journal NO re-reproducido como sustituto (§23). **PASS**.
- **N — NEW HISTORICAL RUN:** MarketHistorySource + síntesis canónica + warm-up; sin claim de reproducción del disorder previo (§19). **PASS**.
- **O — COLD LOSS:** `COLD_RECOVERY_REQUIRED` (D2-04 R11) para el path de ejecución incluso con journal; estado analítico de mercado/strategy re-derivable sólo por replay completo del recording; sin journal suficiente ⇒ fail-visible; sin continuación inventada (§23). **PASS**.
- **P — 200 ACCOUNTS:** costo de recording/orden scoped por stream/strategy; cero multiplicación por cuenta (§27). **PASS**.
- **Q — INITIAL REPLAY ANCHOR (R1):** S1 (200×1m + 50×5m). LIVE: warm-up corpus W → indicator/finite state S → `owner_input_seq=0` → primera decisión D. EXACT_REPLAY: anchor W re-ejecutado con la misma lógica B §17 → mismo S → seq=0 → misma D. Run grabado sin anchor ⇒ `REPLAY_ANCHOR_MISSING` fail-visible; digest/readiness en mismatch ⇒ `REPLAY_ANCHOR_INVALID` (§18/§21). **PASS** (estructural; golden replay físico = obligación D6).
- **R — MONOTONIC RUNTIME CLOCK WITH LATE EVENT (R2):** live: TimerFired admitido con runtime 09:31:00 → después MarketEvent `event_ts=09:30:59.900`: `DomainClock.Now()` jamás retrocede (`runtime_ts` del evento ≥ 09:31:00), y el evento entra igualmente a la barra 09:30 por su `event_ts` (asignación/corrección B §9). Replay: `Now()` tras el evento ≥ 09:31:00 con event-time semantics intactas — ambas propiedades simultáneas por construcción (§5/§6). **PASS**.
- **S — NO-OP TIMER CHAIN (R3):** timer t1 dispara, sin cambio inmediato de estado de negocio, y agenda t2: t1 y t2 son ambos TimerFired admitidos ⇒ ambos journalados (§15 ALWAYS); el replay ejecuta t1 → re-agenda t2 → t2 dispara: la cadena de control flow reproduce idéntica. t1 no puede desaparecer del recording porque un enum no cambió. **PASS**.
- **T — TIMER REPLACEMENT (R3):** timer X generation 7 cancelado/reemplazado por generation 8; llega firing tardío de gen 7: el guard de generación lo absorbe como NO-OP determinista (no ejecuta dominio, jamás se confunde con el firing vigente de gen 8); replay valida (X,7) contra el timer set virtual reconstruido y absorbe idéntico; un firing de generación jamás existida ⇒ `REPLAY_LOG_CORRUPT` fail-visible (§7/§22). **PASS**.

## 31. Owner decisions

`OWNER DECISIONS REQUIRED: 1` — decisión de producto/operación real (ejemplo explícitamente calificado por el mandato), no de naming:

- **OD-C1 — ¿Es EXACT LIVE REPLAY una capacidad de producto V1 con recording always-on, o una capacidad diferida con recording opt-in por run?** La frontera congelada (§1..§27) es idéntica en ambos casos. La decisión define: (a) default operacional de recording para LIVE/SHADOW/DEMO (always-on recomendado: costo marginal bajo — refs+control, §27 — y habilita forense de decisiones, verificación del caso duro B/C y la prueba D3 AUTHENTIC_DATA futura); (b) retención mínima contractual del contenido canónico para runs grabados (§28-R-C2); (c) alcance de la certificación golden replay en D6. Si el owner elige diferido, el recording queda habilitado por config de run y el resto del artifact no cambia.
- **Explícitamente NO elevados a owner** (ratificación técnica ordinaria del manager): nombres físicos (`owner_input_seq`, `echo.market-run-journal.v1`, `echo.market-run-manifests.v1`, `DomainClock`, `ReplayDriver`), shapes exactos de `MarketRuntimeInput`/`RunManifest`/entradas de journal, namespacing de `timer_id`, reglas de materialidad finas de §13, defaults de retención, integración del contador en ValueSpec. Dos questions históricas del mandato ya quedan congeladas por autoridades previas y no se reabren: streams sintéticas continuas multi-contract (PROHIBIDO V1, A §9/§14 — rollover explícito) y corrección retrospectiva de decisiones emitidas (PROHIBIDA, B R3).

## Handoff

```text
D2-06C STATUS:
READY_FOR_SUBMANAGER_REVIEW

ARTIFACT:
main/10-projects/Echo Futures/Echo Futures — D2-06C Live Replay Market Boundary.md

AGENTS-OS SHA:
84c5fc49 (commit que contiene el artefacto [b66d50a2] + continuidad y feedback [84c5fc49]; el bloque handoff ampliado viaja en el sync siguiente)

ECHO BASELINE:
372af59a7b83604781346613da01e3d510ea1360 (origin/master re-verificado en ventana, fetch sin delta)

NEXT:
Return to D2-06 SUBMANAGER. Do not start D2-07.
```
