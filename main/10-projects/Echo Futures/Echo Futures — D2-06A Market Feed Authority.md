---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo Futures]]"
  - "[[Echo Futures — D2-05 Instrument Session Provider]]"
  - "[[Echo Futures — D2-04 Operation Order Fill Position]]"
  - "[[Echo Futures — D1 Analysis Pack]]"
aliases:
  - Echo Futures D2-06A
  - EF Market Feed Authority
tags:
  - kind/doc
  - area/echo
  - echo-futures
  - architecture-design
created: "2026-09-27"
updated: "2026-09-27"
---

# Echo Futures — D2-06A Market Feed Authority / Normalization / Health / Recovery

> [!info]+ TOP worker A — D2-06
> Deliverable del worker A del bloque D2-06 (Market Runtime). Consumes congelados: [[Echo Futures — D2-05 Instrument Session Provider]] (CLOSED), [[Echo Futures — D2-04 Operation Order Fill Position]] (CLOSED), [[Echo Futures]] D2-01..03, [[Echo Futures — D1 Analysis Pack]] Fronts B/B2/E. Baseline Echo verificada físicamente: `origin/master = 372af59a7b83604781346613da01e3d510ea1360` (HEAD local == remota, fetch sin delta). Este artefacto NO implementa código, NO cierra D2-06, NO diseña Bars/Indicators (D2-06B), NO diseña el boundary determinista LIVE/REPLAY (D2-06C), NO selecciona execution transport (D2-07).

## 1. Executive verdict

```text
D2-06A STATUS: READY_FOR_SUBMANAGER_REVIEW
```

El contrato V1 de MarketFeedEngine se congela alrededor de una sola identidad: **el market data binding de D2-05 ES la autoridad lógica de mercado**. Un stream canónico es `(binding_id, contract_id)`; todos los consumidores (Strategy vía su motor, MM de una Operation pinneada) leen del mismo stream normalizado y read-only; el número de Accounts es invisible para el engine. Los feeds físicos equivalentes (CME A/B o equivalentes vendor) viven DENTRO de un binding como *members* arbitrados; los sources heterogéneos son bindings distintos y sólo cambian por un **source switch explícito** con pérdida de readiness, nunca blend. Health separa tres dimensiones (liveness por member, continuity por primitivas del source, freshness por config) y **el calendario de D2-05 es la autoridad que decide cuándo el silencio es esperado**: ExchangeCalendar CLOSED + cero ticks por horas jamás es failure. Recovery es una máquina conceptual única con ejecución capability-specific: gap → readiness perdida → replay/snapshot/natural-refresh según el adapter declarado → dedup de overlap → barrier de reconstrucción downstream → READY con epoch nueva.

Físicamente el engine es un nuevo StateFun keyed function `echo/market_stream` (key `stream_id`) sobre los patrones ya congelados en D2-04/D2-05: adapters productores → Kafka → engine arbitra/normaliza → topic canónico `echo.market-events.v1` (transporte + recorded stream) + topic compactado de control `echo.market-stream-state.v1` (readiness/epoch). El egreso canónico es AT_LEAST_ONCE con idempotencia por `stream_seq` (decisión deliberada: exact-once transaccional retardaría ticks al intervalo de checkpoint; el gap/seam se declara, no se esconde). `OWNER_DECISIONS_REQUIRED = NONE`: el vendor de feed, umbrales de frescura y criterios de switch quedan como config técnica; la decisión owner de rollover manual ya está congelada en D2-05.

## 2. Scope / non-scope

**En scope (V1 freeze):** envelope canónico MarketEvent; identidad/dedup; identidad de stream lógico; relación Instrument/Contract/MarketDataBinding; ciclo de subscription; redundancia equivalente; switch heterogéneo; liveness/continuity/freshness; adapter capability contract; recovery; readiness barrier; provenance; coexistencia current vs pinned Contract; durable/history seam mínimo; ownership físico; reuse map Echo V3.

**Fuera de scope (exclusivo de otros workers/hitos):** barras/MTF/indicadores/warm-up depth (D2-06B); clock determinista y ordering/replay LIVE↔REPLAY completo (D2-06C); selección de transport de ejecución (D2-07); selección de vendor de feed (queda config); capacity benchmark (D6); escalado/migración global (D2-08); MoneyManagement monetary action (nunca).

## 3. Minimal MarketEvent

Envelope único y común para todo el runtime (LIVE, recovery, warmup, replay). Sólo QUOTE (BBO) y TRADE en V1: S1 (30m ORB sobre trades) y MM hardscalping (BBO) los cubren; ProjectX market hub expone quote/trade/depth y CME MDP trades/quotes/depth — depth/book no tiene consumidor V1 (sin book strategies en la cohorte) y queda DEFERRED; SESSION transitions no son market events (vienen del calendario D2-05, §8-10); BAR no es evento de feed (construcción = D2-06B).

```text
MarketEvent {
  stream_id            # identidad lógica: (binding_id, contract_id) — §5
  instrument_id        # canónico, desnormalizado para consumidores
  contract_id          # physical contract del stream
  event_type           # QUOTE | TRADE
  event_ts             # instant del evento (RFC3339Nano UTC); venue-authoritative
                       # cuando el capability lo declara; si no, source event time
  receive_ts           # wall clock de ingestion (sólo liveness/telemetría,
                       # JAMÁS semántica de dominio)
  source_seq?          # sequence del venue/source cuando el capability la entrega;
                       # ausente (no cero) para sources sin sequence
  source_trade_id?     # identidad de trade del venue cuando existe (dedup no-seq)
  stream_seq           # monotónico por stream, asignado por el engine DESPUÉS de
                       # arbitraje/dedup: contiguo, sin duplicados por construcción
  authority_epoch      # epoch de la autoridad del stream (incrementa en switch de
                       # source y en recovery que invalida continuidad)
  origin               # { source_id, feed_kind: LIVE | REPLAY | SNAPSHOT }
  payload:
    QUOTE { bid_price, bid_qty, ask_price, ask_qty }   # decimales en quote_currency
    TRADE { price, qty }
}
```

No hay quality score, no hay ontology universal, no hay campos "por si acaso". Reglas de congelación: `receive_ts` jamás participa de semántica de barras/estrategia (D2-05 §9: cuatro tiempos, el event time manda); `source_seq` es opcional por diseño — su presencia/ausencia está gobernada por el capability contract (§11), no por heurística; `stream_seq` es el token de continuidad/idempotencia del path canónico aguas abajo (dedup O(1) por comparación).

## 4. Event identity / dedup

Tres identidades distintas, jamás colapsadas:

| Capa | Identidad | Quién la asigna | Uso |
|---|---|---|---|
| **Transport message identity** | `(source_id, transport seq/packet)` del member físico | el adapter/source | diagnóstico, liveness del member |
| **Logical semantic event identity** | `(stream_id, source_seq)` con sequence fuerte; si no: `(stream_id, event_type, event_ts, precio, qty[, source_trade_id])` | el venue/source (o tupla de contenido) | dedup entre members equivalentes y overlap de replay |
| **Echo stream identity** | `stream_seq` contiguo por stream | el engine, post-arbitraje | orden canónica, idempotencia downstream, barrier |

Casos resueltos:

- **A — Source con sequence fuerte** (CME MDP A/B comparten el mismo espacio de secuencia del venue): tracking monotónico por stream; `seq ≤ last` se suprime; salto = GAP_DETECTED (§12). Dedup entre members: first-wins por `(stream, venue_seq)` — el primero que llega al engine gana, el gemelo se suprime. Sin voting, sin scoring (YAGNI).
- **B — Source sin sequence universal**: steady-state **sin dedup** (un solo feed ordenado por la partición Kafka del stream). Identity de contenido + ventana LRU acotada en el tiempo, activa **sólo durante epochs RECOVERING/SWITCHING** (overlap de reconnect/replay/switch). Fuera de esos epochs la ventana está cerrada: cero costo hot-path.
- **C — Gap replay que reentrega**: el replay entra al engine como candidate con `feed_kind=REPLAY` y `source_seq` (o content identity); el overlap contra lo ya emitido se suprime ANTES de asignar `stream_seq` ⇒ el stream canónico nunca repite ni reordena; los consumers jamás doble-cuentan.
- **D — Reconnect overlap**: igual que C; el adapter reconecta desde `last_source_seq+1` (capability) o natural refresh; el overlap resultante muere en dedup.
- **E — Equivalent A/B overlap**: mismo mecanismo que A; los dos members comparten venue authority; la salida canónica por `stream_seq` garantiza una sola evaluación de Strategy por evento de mercado.

**Prohibido congelado:** no se fabrica un UUID para "fingir" source identity; si el source no da identity, se declara en el capability y se usa identity de contenido con ventana acotada — la falsa universalidad es un defecto, no un feature.

## 5. Logical stream identity

```text
MarketStream {
  stream_id    = (binding_id, contract_id)      # binding MARKET_DATA de D2-05
  instrument_id                                 # canónico
  external_ids  = { source_id → ContractIdentifier }   # resueltas por (source, context)
  members       = [ feed members físicos equivalentes ] # config del binding
  demand        = config_demand ∪ operation_demand
  state         = SUBSCRIBING | READY | RECOVERING | RETIRING | UNSUBSCRIBED
}
```

Congelado:

- **Qué consume Strategy:** MarketEvents del stream de la *active authority binding* del Instrument (config del runtime de mercado declara UNA binding activa por instrumento; las demás bindings son standbys heterogéneos). La Strategy ve `instrument_id`, nunca `binding_id` ni `contract_id` (D2-03: Strategy agnóstica del contract físico; el StrategyEngine resuelve instrument → stream activo).
- **Qué consume MM con Operation pinneada:** MarketEvents del stream `(binding activa, contract_id pinneado)` — incluido un contrato viejo en RETIRING (§14).
- **Quién resuelve current Contract:** la fila de mapping D2-05 `(MARKET_DATA, binding_id, instrument_id) → contract_id`, hot y prospectiva. El engine la consume vía kache; no la duplica.
- **Cómo entra MarketDataBinding:** la config del binding (members, source capabilities, thresholds de freshness) es config hot con el patrón compacted-topic/kache ya congelado; readiness fail-closed (`MARKET_CONFIG_NOT_READY`).
- **Cuándo nace una subscription:** la entrada del stream en `demand` (§7). **Cuándo puede cerrarse:** salida de `demand` (último demandante liberó). **Jamás se desuscribe un Contract con consumidor vivo** — garantizado por construcción: RETIRING sólo termina cuando operation demand = ∅.
- **Convivencia current/pinned:** dos streams coetáneos bajo el mismo binding (`(dbt-main, NQZ6)` RETIRING + `(dbt-main, NQH7)` READY), cada uno con su `stream_seq`, su health y su readiness. No hay mixing posible: el stream_id ya separa los espacios.

## 6. Instrument / Contract / MarketDataBinding

Heredado sin cambios de D2-05 (§4-6): `Instrument` canónico → `Contract` expiry-specific vía mapping hot por binding; `ContractIdentifier` por `(source, context)` para el string literal del vendor; el engine resuelve `Instrument + binding → current Contract` (kache) y `Contract + source_id → identifier MARKET_DATA` (segundo paso local al suscribir). Identifier ausente para el `(source, context)` de un member = fail-closed: el member no puede suscribirse ⇒ readiness NO_READY(NO_LIVE_MEMBER) si era el único; jamás identidad por string vendor. Un cambio de mapping no muta streams existentes: crea demanda del stream nuevo (§7/§14).

## 7. Subscription lifecycle

Demand = unión de dos fuentes, sin reference counting framework:

1. **config_demand** — catálogo del runtime: instrumentos habilitados para consumo Strategy × active binding → contrato corriente. Cambia por config hot (rollover, alta/baja de instrumento).
2. **operation_demand** — demandas de MM por Operation viva: el owner `echo/operation` emite `MarketDemand{op: ACQUIRE|RELEASE, stream_id, operation_id}` transaccionalmente en su frontera de checkpoint (mismo egress fact pattern R14 de D2-04): ACQUIRE en la materialización (con el contract pinneado), RELEASE al TERMINAL. Idempotente por `operation_id` (set membership, no contadores).

```text
SUBSCRIBING  entrada en demand: resolver identifiers, conectar members,
             baseline de continuidad + snapshot/first BBO ⇒ readiness barrier
READY        sirviendo decisiones (único estado que habilita evaluación nueva)
RECOVERING   continuidad perdida; los eventos fluyen para rebuild, el gate
             de decisión está cerrado (§12/§13)
RETIRING     salió de config_demand (rollover/baja) pero operation_demand > ∅
UNSUBSCRIBED demand = ∅: desconexión y liberación — legítima porque no
             queda ningún consumidor
```

Caso H de escala por construcción: 20 o 200 execution accounts con la misma Strategy S1 = la MISMA subscription `(dbt-main, NQH7)`. Account count no aparece en el engine; el fan-out a cuentas ocurre aguas abajo (StrategyEngine/fan-out D2-04) sobre el stream compartido read-only.

## 8. Equivalent feed arbitration (dentro de una autoridad)

Config: un binding declara sus members (p.ej. `cme-a`, `cme-b` vía el mismo source vendor, o endpoints A/B equivalentes). Validación de config: members de un binding deben declarar capabilities compatibles (misma clase semántica, misma sequence kind) — mezclar clases dentro de una autoridad = config inválida fail-closed.

- **Precedence/arbitration:** first-wins por logical semantic event identity (§4-A). No hay "feed A primario": CME recomienda procesar ambos; el engine consume ambos members siempre que sea posible y arbitra por llegada.
- **Continuity/sequence:** el espacio de sequence es del venue y compartido por members equivalentes ⇒ la continuidad se evalúa sobre el venue seq, no sobre qué member entregó cada mensaje.
- **Duplicate suppression:** gemelos por `venue_seq` suprimidos; costo O(1).
- **Failover intra-autoridad:** automático y continuo. Si el member activo muere, el otro sigue entregando; si la continuidad venue-seq queda verificada, **no hay barrier** (sólo cambia `origin.source_id` en provenance + telemetría). Si el member superviviente no puede demostrar continuidad (hueco en su propia ventana), el stream cae a RECOVERING y recovery normal (§12).
- **Recovery:** capability-driven, idéntico al caso single-feed.
- **Provenance:** cada evento porta `source_id` del member que lo produjo; el estado del stream porta el member set activo. Diagnóstico "¿quién produjo este estado?" responde sin contaminar el envelope con detalles vendor.

**Prohibido congelado:** sumar ticks A+B como si fueran eventos distintos, y ejecutar Strategy dos veces por el mismo evento — ambos imposibles por construcción (dedup previo a `stream_seq`; una sola salida canónica).

## 9. Heterogeneous source switch (entre autoridades)

Bindings distintos = autoridades distintas, jamás mezcladas. V1 congela: **el switch es una transición explícita de config** (cambio de active binding del instrumento, operador/owner u automatismo operacional futuro — no silencioso nunca); no hay failover automático cross-vendor en V1 (ningún evidence lo exige; B2 lo deja como decisión técnica; KISS lo difiere con alerta de readiness como mitigation).

Semántica del switch:

```text
1. config: active_binding NQ: dbt-main → dbt-backup (hot, prospectiva)
2. engine: stream viejo (dbt-main, NQ*) → RETIRING si operation_demand lo retiene,
   sino UNSUBSCRIBED; stream nuevo (dbt-backup, NQH7) → SUBSCRIBING
3. authority_epoch++ en el stream nuevo; readiness NOT_READY(SWITCHING_AUTHORITY)
4. boot del stream nuevo según capabilities del source nuevo:
   snapshot BBO/refresh natural + baseline de continuidad propia (su seq space)
5. warmup: los consumers reconstruyen hot state sobre el stream nuevo desde el
   barrier/epoch marker (contrato de rebuild = D2-06B); el estado previo NO se
   fusiona ni se traslada
6. READY con epoch nueva y provenance del source nuevo
```

- **Readiness loss:** siempre (aunque el source nuevo esté "sano": semantic differences no auditables ⇒ barrier obligatoria).
- **Gap/recovery handling:** tras el switch rige el capability del source nuevo; si no puede cubrir el hueco desde el último estado común (p.ej. replay bounds excedidos), el stream queda NOT_READY(GAP_UNRESOLVED) fail-closed — sin síntesis de datos.
- **Hot-state rebuild:** obligatorio downstream (D2-06B); el engine emite el epoch marker que delimita la reconstrucción.
- **Provenance:** `authority_epoch` + `origin.source_id` en cada evento; el estado compactado del stream porta la historia de epochs.
- **READY nuevamente:** sólo con baseline de continuidad del source nuevo completa + warmup downstream consumado (señal de B, §13).

Nunca silent blend: la fusión de dos autoridades en una serie es un defecto arquitectónico, no un modo.

## 10. Liveness / Continuity / Freshness

Tres dimensiones separadas por congelación; ninguna se colapsa en un booleano "healthy":

| Dimensión | Scope | Evidencia válida | Estados |
|---|---|---|---|
| **LIVENESS** | por member físico | conexión + heartbeat del source cuando existe (CME Admin Heartbeat, Databento heartbeat); inactividad sólo cuenta mientras `SessionState=OPEN` del calendar_id del instrumento | CONNECTED / DEGRADED(heartbeat o inactividad bajo sesión OPEN) / DISCONNECTED |
| **CONTINUITY** | por stream | exclusivamente primitivas del source: sequence jump, reconnect callback con rango, estado de replay. **Un salto de timestamps NO es evidencia de gap** (B2 correction); un source sin primitivas declara CONTINUITY=UNKNOWN, no "roto" | CONTIGUOUS / GAP_DETECTED / UNKNOWN |
| **FRESHNESS** | por stream | `event_ts`/`receive_ts` vs wall clock contra threshold **config por source/schema/instrument**; supervisión activa sólo con sesión OPEN | FRESH / STALE(policy) / NOT_EVALUABLE(session cerrada/break) |

Estados compuestos obligatorios (verificación del modelo, no enum normativo):

- transport CONNECTED pero stream gapped ⇒ LIVENESS ok + CONTINUITY GAP_DETECTED ⇒ RECOVERING.
- DISCONNECTED pero último market state usable ⇒ NOT_READY(NO_LIVE_MEMBER) con `last_known_state` + `as_of` + stale flag aún legible para MM/safety (§15.1).
- CONNECTED sin actividad porque ExchangeCalendar=CLOSED ⇒ liveness supervisa heartbeats (si el source los emite en sesión cerrada), freshness NOT_EVALUABLE; **jamás failure por elapsed wall-clock**.
- "no tick en 5 segundos" jamás es regla universal: los umbrales son config técnica por source/instrument y se evalúan sólo bajo sesión OPEN (B2 manager: no freeze timeout universal).
- RECOVERING ⇒ barrier cerrada; READY ⇒ gate abierta.

## 11. Adapter capability contract

Declarado por source en config (namespace `source` = el mismo de `ContractIdentifier`, D2-05 §4). El engine es genérico sobre capabilities; las diferencias reales de vendors quedan visibles, no escondidas tras una interface falsa:

```text
SourceCapabilities {
  source_id
  sequence:      NONE | SOURCE_LOCAL | VENUE_STRONG   # VENUE_STRONG = compartida
                                                      # entre members equivalentes
  gap_detection: SEQUENCE_BASED | NONE                 # NONE ⇒ CONTINUITY=UNKNOWN
  replay:        { supported, modes: [FROM_SEQ|FROM_TIME|FROM_DISCONNECT],
                   bounds, typical_latency_class }
  snapshot:      { supported, kinds: [BBO_SNAPSHOT|BOOK_SNAPSHOT|NATURAL_REFRESH] }
  heartbeat:     { supported, interval }
  reliable_ts:   [EVENT_VENUE | EVENT_SOURCE | RECEIVE_ONLY]
  dedup_identity: SEQUENCE | CONTENT
  recovery_semantics: REPLAY_EVENTS | SNAPSHOT_REPLACE | NATURAL_REFRESH
}
```

Reglas de validación (fail-closed en carga de config): `sequence=NONE` ⇒ `gap_detection=NONE` y `dedup_identity=CONTENT`; recovery prometido sin replay ni snapshot ⇒ config inválida; `reliable_ts=RECEIVE_ONLY` ⇒ `event_ts` no puede marcar barras venue-authoritative (B decide cómo tratarlo con esa declaración). El engine no infiere capabilities por comportamiento observado: lo no declarado es "no soportado".

## 12. Recovery

Máquina conceptual V1 (ejecución capability-specific; es el único algoritmo permitido y no hay recovery universal):

```text
CONTIGUOUS (READY)
  → gap/reconnect detectado por primitiva del source (§10)
  → stream pierde readiness ⇒ RECOVERING (barrier ON; gate de decisión cerrado)
  → recovery según capability:
      REPLAY_EVENTS     → pedir rango faltante (FROM_SEQ/TIME/DISCONNECT) al
                          MarketHistorySource o al live replay del vendor
      SNAPSHOT_REPLACE  → snapshot del estado (BBO) + retomar desde ahí
      NATURAL_REFRESH   → resuscribir, descartar viejo, continuar desde lo nuevo
  → overlap dedup (§4 C/D/E) antes de asignar stream_seq
  → epoch marker / RecoveryBarrier emitido aguas abajo
    { stream_id, epoch_nuevo, rango afectado o snapshot marker }
  → affected downstream hot state se reconstruye (bars/forming/indicadores:
    contrato de D2-06B; el engine delimita, no reconstruye)
  → readiness barrier levantada sólo con continuidad demostrada + warmup
    downstream consumido ⇒ READY (epoch nueva)
```

- **Qué se pausa:** sólo la *evaluación de decisiones nuevas* de ese stream (gate). **Qué sigue disponible:** el último market state (marcado as_of/stale), el path de Orders/Fills/Operations (ejecución es otro dominio), la telemetría, y los eventos de recovery que fluyen para rebuild.
- **Provenance de recovery:** `feed_kind=REPLAY|SNAPSHOT` en cada evento + `authority_epoch` en el stream ⇒ cualquier estado downstream declara de qué epoch proviene.
- **Downstream sabe que los datos no son confiables** por tres señales coherentes: estado de readiness del stream (compacted topic), RecoveryBarrier/epoch markers inline, y provenance por evento.
- **Reinicio de evaluación segura de Strategy:** el StrategyEngine/MM evaluadores consumen el gate READY del stream; mientras RECOVERING, los inputs de evaluación están invalidados y las Strategies no producen decisiones nuevas para ese stream; MM/safety aplican su policy (§15). La evaluación se re-habilita con el stream READY y el warmup downstream completo — nunca antes.
- **Fuera de bounds** (p.ej. hueco mayor que replay bounds del vendor): NOT_READY(GAP_UNRESOLVED) persistente + alerta operador; sin síntesis, sin "mejor esfuerzo" silencioso.

NO se define MoneyManagement monetary action: Market Runtime informa quality/readiness; MM/safety deciden qué hacer monetariamente.

## 13. Readiness (barrier)

Superficie canónica por stream, publicada en `echo.market-stream-state.v1` (compacted, key `stream_id`) y como epoch markers inline en `echo.market-events.v1`:

```text
StreamState {
  stream_id, epoch, readiness: READY | RECOVERING | NOT_READY,
  reasons: [ NO_LIVE_MEMBER | GAP_UNRESOLVED | STALE_BEYOND_POLICY
           | SWITCHING_AUTHORITY | WARMUP_INCOMPLETE | CONFIG_NOT_READY ],
  last_known_state_ref/as_of, members activos, authority provenance
}
```

Consumers (StrategyEngine, MM market gate, fronts) kache-an este estado (patrón compacted/WaitReady). El gate de decisión nueva exige READY del stream referenciado; el calendar CLOSED acota availability antes del gate (D2-05 §10), de modo que readiness y session availability componen sin solaparse. La barrera se levanta con evidencia, no con timeout.

## 14. Rollover / current vs pinned Contract

Escenario obligatorio (congelado D2-05 §6; aquí su cara de feed):

```text
NQ mapping (dbt-main): NQZ6 → NQH7  (owner, hot, prospectivo)

1. config_demand muta: nace (dbt-main, NQH7) → SUBSCRIBING → barrier → READY
2. (dbt-main, NQZ6) → RETIRING: sigue READY funcional y sirve NQZ6
3. Strategy: nuevas evaluaciones resuelven NQ → stream NQH7
4. Operation A (pinned NQZ6): su ACQUIRE sigue vivo ⇒ NQZ6 NO desaparece;
   MM de A sigue recibiendo QUOTE/TRADE de Z6 para trailing/gestión
5. A TERMINAL ⇒ RELEASE ⇒ demand(Z6)=∅ ⇒ UNSUBSCRIBED
6. jamás remap, jamás auto-roll, jamás migración de stream (D2-05 §6 intacto)
```

KISS logrado: la coexistencia no requiere reference counting framework — es la unión de dos demand sets idempotentes; el caso "old Contract todavía usado" está cubierto porque RELEASE sólo proviene del terminal de la Operation que lo pedía.

## 15. Failure semantics (los seis casos)

1. **Feed down, último hot state usable:** readiness NOT_READY(NO_LIVE_MEMBER); `last_known_state` + `as_of` + stale flag siguen legibles; MM/safety deciden según su policy (gestionar exits con estado marcado, etc.). El engine no bloquea el path de ejecución; sólo deja de certificar frescura.
2. **Continuity unknown** (source sin primitivas): CONTINUITY=UNKNOWN no es NOT_READY por sí mismo; liveness (heartbeat/disconnect callback) + freshness config son la evidencia; readiness cae cuando esas tripan. La incertidumbre queda declarada en StreamState, no normalizada a "ok".
3. **Stream recovering:** RECOVERING + barrier (§12); eventos fluyen para rebuild; decisiones nuevas pausadas para ese stream.
4. **Equivalent backup ready:** failover intra-binding automático y continuo (§8); readiness se conserva si la continuidad venue queda demostrada; provenance cambia de member.
5. **Sólo heterogeneous backup disponible:** switch explícito de autoridad (§9) con readiness loss, rebuild y epoch nueva; jamás blend; si el backup no puede cubrir desde el último estado común ⇒ fail-closed persistente + operador.
6. **Live Operation expuesta durante outage:** el engine expone readiness/staleness/barrera; **Market Runtime no cierra posiciones ni inventa flatten** (ni por market quality ni por ningún otro trigger market-driven en V1). La reacción monetaria (suspender riesgo nuevo, close-only, ForceClose provider-driven) pertenece a MM/safety/provider_rules D2-04/D2-05, que ya tienen sus planes asíncronos.

## 16. Durable / history seam

Tres cosas distintas que no se colapsan:

| Pieza | Qué es | V1 físico |
|---|---|---|
| **Hot state** | estado vivo por stream/aguas abajo | in-memory (engine state + D2-06B), reconstructable |
| **Recoverable market history** | fuente de recuperación/warmup | `MarketHistorySource` interface con adapters (vendor replay/history); **sin elección de data lake/DB en D2-06A** |
| **Recorded replay stream** | la serie normalizada grabada para replay/backtest | el propio `echo.market-events.v1` con retention config: grabar = side-effect de emitir; el consumer de replay es boundary de D2-06C |

`MarketHistorySource.read(stream_id, from, to) → [MarketEvent]` — mismo envelope canónico, misma semántica; lo consume recovery (§12) y el warmup handoff de D2-06B (reconstrucción de barras/indicadores previa a READY). Restart del engine: estado desde checkpoint Flink; demand sets re-derivan del propio estado checkpointeado (config + operation demands son parte del keyed state); los members reconectan con resubscribe/baseline por capability. No event sourcing, no store nuevo, no DB monstruosa.

## 17. Physical topology (feed portion)

```text
feed adapters (procesos edge, 1 por source member)
  vendor SDK/socket → normaliza schema vendor → MarketEvent candidate
  → Kafka `echo.market-feed-candidates.v1` (key: stream_id|source_id)
        ↓
echo/market_stream  (StateFun keyed, key = stream_id)   [NUEVO]
  arbitra members / dedup / detecta gap / ejecuta recovery
  asigna stream_seq + epoch + origin
  mantiene: demand sets, health counters, dedup windows (sólo epochs activos)
  state = Flink checkpointed; timers SendAfter = ticks de health/freshness
        ↓ egress AT_LEAST_ONCE + idempotencia stream_seq
echo.market-events.v1        (canónico; key stream_id; transport + recorded stream)
echo.market-stream-state.v1  (compacted; readiness/epoch/health; kache)
        ↓
consumers: StrategyEngine / MM market gate / B-bars / fronts (kache + topic)

config hot: stream catalog + SourceCapabilities + thresholds
  → patrón compacted-topic + kache (igual que calendars D2-05 §8)
```

Justificación: **owner** = `echo/market_stream` keyed por `stream_id` (cero Account en las llaves; escalar accounts no toca el engine). **Durable** = topics Kafka (+ checkpoint Flink del estado del engine). **Derived** = readiness/health projections y el estado compactado de control. **In-memory** = dedup windows, health counters, último estado por stream. **Reconstructable** = todo el estado del engine desde Kafka ingress replay + checkpoint; el hot state downstream desde el topic canónico + `MarketHistorySource`. REUSE del runtime `apache/flink-statefun:3.2.0` ya desplegado; se registran el function y los topics nuevos en `module.yaml` con el mecanismo existente. Riesgo de throughput honesto: tráfico tick × hops Kafka/HTTP es la incógnita física — ver D6, con fallback declarado (§20).

Egresos: el canónico es AT_LEAST_ONCE + `stream_seq` idempotente (exact-once transaccional encadenaría la latencia de ticks al intervalo de checkpoint — incompatible con el hot path; la diferencia con el egreso EXACTLY_ONCE de comandos D2-04 es deliberada y declarada, ambos con su prueba de correctness propia). El egress de `MarketDemand` desde `echo/operation` viaja por el egress transaccional existente (misma frontera de checkpoint que el estado de la Operation, R14) y su consumo es idempotente por `operation_id`.

## 18. Echo V3 reuse/adapt map

| Pieza V3 | Disposición | Evidencia |
|---|---|---|
| StateFun module.yaml ingress/egress + registro `echo/*` + Go SDK | **REUSE/EXTEND** | `v3/core/deploy/flink-statefun/production/module.yaml`; `v3/sdk/statefun/constants.go` |
| kache / ConfigCache (compacted topic + OffsetOldest + WaitReady) | **REUSE** para stream catalog, capabilities y consumo del estado compactado | `v3/core/internal/config_cache.go`; `v3/sdk/kache/*` |
| SendAfter timers (patrón mm_engine) | **REUSE** para ticks de health/freshness por stream | `v3/core/internal/functions/mm_engine.go` (`ctx.SendAfter`) |
| Compacted hot-config pattern con tombstones (SymbolMapping) | **REUSE patrón** para el catálogo de streams/bindings | `v3/gateway/internal/symbol_mapping_handler.go`; `v3/bridge/internal/symbol_mapping_cache.go` |
| OTel DI + semconv + `echo.*.v1` topic conventions | **REUSE** | `v3/core/internal/telemetry.go`; `v3/sdk/telemetry/*` |
| `echo/inst_snapshot` + `InstrumentSnapshot` (`broker:symbol`) | **REUSE legacy / no autoridad**: observación MT; el authority Futures es este engine (ya congelado en D2-05 §21) | `v3/sdk/domain/snapshots.go` |
| Egress EXACTLY_ONCE config requirement (D2-04 §5.6/R2) | **REQUIREMENT carried**: los egress transaccionales nuevos (MarketDemand fact path) exigen la misma config `EXACTLY_ONCE` + `read_committed`; el egress canónico de market events es AT_LEAST_ONCE por decisión propia (§17) | `Echo Futures — D2-04` §5.6/R2 |
| Bars/replay/market history/MarketHistorySource | **NEW** (no existe nada físicamente: verificado) | búsqueda: sin Bar/Quote/Tick/MarketData/replay en v3 |
| lab_curves / strategy history / Forge ingest | ** unrelated / DEFERRED**: historia analítica, no market feed | `v3/lab-worker/*`; `v3/gateway/internal/forge_ingest_handler.go` |
| Bridge MT5 / feed del Echo Forex | **REPLACE para Futures path**: no se adapta como fuente de market data de futuros | — |

## 19. Acceptance cases

- **A — FEED SHARING:** 20 accounts × S1 sobre NQ ⇒ una sola subscription `(dbt-main, NQH7)`; el fan-out por cuenta ocurre en StrategyEngine/fan-out D2-04 sobre el stream read-only. Account count ausente del engine. **PASS.**
- **B — EQUIVALENT DUAL FEED:** members A/B en un binding; arbitraje first-wins por venue_seq; muere A ⇒ B continúa; continuidad verificada sobre el seq venue ⇒ sin barrier, provenance cambia de member; una sola evaluación de Strategy por evento (salida única por stream_seq). **PASS.**
- **C — HETEROGENEOUS SOURCE BACKUP:** primary cae y sólo queda un binding distinto ⇒ switch explícito (§9): epoch++, NOT_READY(SWITCHING), snapshot/boot por capabilities del nuevo, rebuild downstream, READY; sin blend jamás. **PASS.**
- **D — SEQUENCE GAP (100,101,104):** seq 104 > 101+1 ⇒ GAP_DETECTED por primitiva ⇒ RECOVERING, readiness OFF; capability replay pide 102-103 (o snapshot si replays no aplica); overlap dedup; RecoveryBarrier; B reconstruye lo afectado; continuidad demostrada + warmup ⇒ READY (epoch nueva). **PASS.**
- **E — EXCHANGE CLOSED:** calendar CLOSED ⇒ freshness NOT_EVALUABLE y liveness no penaliza silencio; sin failure por wall-clock; en `NextSessionTransition` OPEN la supervisión de frescura re-arranca y los primeros eventos refrescan estado. **PASS.**
- **F — ROLLOVER WITH LIVE OPERATION:** §14 paso a paso; NQZ6 RETIRING vivo por ACQUIRE de Operation A; NQH7 READY para Strategy; release al TERMINAL; cero remap. **PASS.**
- **G — LIVE EXPOSURE DURING OUTAGE:** readiness/staleness/barrera expuestos; `last_known_state` marcado; MM/safety aplican policy; el engine no emite ninguna acción monetaria. **PASS.**
- **H — SCALE:** +200 accounts ⇒ +0 market subscriptions (§7). **PASS.**

## 20. Risks / debts

- **Throughput/latencia del engine StateFun por tick (material):** hops adapter→Kafka→StateFun→Kafka→consumer sin benchmark. Mitigación: benchmark D6 obligatorio con tasa real del instrumento; fallback declarado (mismo contrato de estado/semántica servido por un stream worker in-process checkpointeado) — deuda condicional, no decisión hoy.
- **Egress canónico AT_LEAST_ONCE:** correctness downstream depende de respetar el dedup por `stream_seq`; es requisito de consumo en B/C y en cualquier front. Riesgo de implementación (no de diseño).
- **Dedup windows no-seq acotadas:** un source sin sequence con overlap mayor que la ventana ⇒ posible duplicado residual tras recovery; mitigación: ventanas por config conservadoras + telemetría de supresión; la clase entera se evita prefiriendo sources con sequence.
- **Replay bounds de vendor (p.ej. intraday 24h):** outages largos exceden bounds ⇒ fail-closed persistente + operador. Sin historia durable propia en V1 (decisión: no construir data lake ahora); revisar en D2-06B/C si el warmup la exige.
- **Automatic heterogeneous failover ausente:** un outage total del active binding requiere acción operacional (switch por config); mitigación: readiness alerts; automatización futura = config/ops, no cambio de contrato.
- **Capacidad de la ventana de demand sets:** crece con #Operations vivas por contrato viejo; acotada por TERMINAL→RELEASE; GC de streams UNSUBSCRIBED es rutina.
- **Timer density:** un timer de health por stream; con pocas decenas de streams V1 es trivial; revisar si el catálogo crece órdenes de magnitud.

## 21. Open questions — genuinely left for D2-06B/C

- **B:** contrato exacto de rebuild de bars/forming/indicadores ante RecoveryBarrier y switch de autoridad (qué se invalida, forming vs closed late-correction policy); depth/format del warmup handoff sobre `MarketHistorySource`; política de `reliable_ts=RECEIVE_ONLY` en barras.
- **C:** mapping determinista stream↔replay (consumo del recorded topic, clock injection, orden de control state vs events para replay fiel); retención/compaction definitiva del recorded stream; si el replay necesita re-derivar health/readiness o lo inyecta el run manifest.
- **Ambos:** conteo de particiones y throughput objetivo de `echo.market-events.v1`; señal exacta de "warmup consumido" que levanta la barrera (interface B↔engine).

## 22. Owner decisions

`OWNER DECISIONS REQUIRED: NONE`. Vendor de feed, thresholds de frescura/liveness, members y switch son config técnica bajo las autoridades ya congeladas (B2 manager: health thresholds = technical D2). Rollover ya es owner-manual por D2-05; nada aquí lo cambia. Quedan ratificaciones técnicas ordinarias del manager: nombres físicos de topics/functions/campos, shape exacto de `SourceCapabilities`/`StreamState`/`MarketDemand`, retention config, y la verificación del benchmark de throughput en D6.

## Handoff

```text
D2-06A STATUS:
READY_FOR_SUBMANAGER_REVIEW

ARTIFACT:
main/10-projects/Echo Futures/Echo Futures — D2-06A Market Feed Authority.md

AGENTS-OS SHA:
11a8f043 (vault sync que contiene este artefacto; los archivos de cierre viajan en el sync siguiente)

ECHO BASELINE:
372af59a7b83604781346613da01e3d510ea1360 (HEAD == origin/master, sin delta)

NEXT:
Return to D2-06 SUBMANAGER. Do not start D2-06B.
```
