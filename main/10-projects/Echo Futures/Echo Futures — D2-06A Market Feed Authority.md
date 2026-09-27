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
> Deliverable del worker A del bloque D2-06 (Market Runtime). Consumes congelados: [[Echo Futures — D2-05 Instrument Session Provider]] (CLOSED), [[Echo Futures — D2-04 Operation Order Fill Position]] (CLOSED), [[Echo Futures]] D2-01..03, [[Echo Futures — D1 Analysis Pack]] Fronts B/B2/E. Baseline Echo verificada físicamente: `origin/master = 372af59a7b83604781346613da01e3d510ea1360` (HEAD local == remota, fetch sin delta). Este artefacto NO implementa código, NO cierra D2-06, NO diseña Bars/Indicators (D2-06B), NO diseña el boundary determinista LIVE/REPLAY ni el recorded stream (D2-06C), NO selecciona execution transport (D2-07). Incorpora el **Manager Repair — D2-06A-R1** (R1–R7), aplicado quirúrgicamente sobre el candidato original; el documento completo refleja ya el modelo reparado, no erratas acumuladas.

## Manager Repair — D2-06A-R1

El SUBMANAGER devolvió `REPAIR_REQUIRED` sobre el candidato original por siete defects. Este repair es targeted: no reabre D2-04/D2-05, no implementa código, no avanza B/C/D2-07. Resolución:

- **R1 — Contract pinned, market source NOT pinned.** La demanda persistente del consumidor expresaba la autoridad física (`stream_id = (binding_id, contract_id)` dentro del `MarketDemand`), dejando una Operation amarrada al binding vivo cuando nació. Resolución: **la demanda es económica** — `MarketDemand{operation_id, instrument_id, contract_id, ACQUIRE|RELEASE}` — y Market Runtime la resuelve contra la *active MARKET_DATA authority* vigente para producir la subscription física. La Operation pinnea Contract (D2-01/04/05), jamás binding/source. Tras un switch, la Operation viva conserva su `contract_id` exacto y ese MISMO contract se sirve con la nueva autoridad; el source viejo puede persistir sólo durante el cutover/recovery necesario y después no queda dependencia estructural. Sin leases ni reference counting: los demand sets idempotentes siguen siendo válidos (§7).
- **R2 — NO content-based fake event identity.** Eliminada la tupla de contenido `(stream_id, event_type, event_ts, price, qty[, source_trade_id])` como identidad de dedup. Echo no inventa identidad semántica desde contenido: dos trades físicos legítimos pueden compartir ts/precio/qty y ambos deben sobrevivir. Tres clases explícitas gobernadas por capability: **A** identity de evento estable ⇒ dedup exacto; **B** sequence de transport/packet ⇒ la identity exige posición determinística dentro del packet; **C** sin identidad dedup-safe ⇒ content-dedup PROHIBIDO; recovery sólo por cursor no-solapado, cursor nativo determinístico, snapshot replacement, full rebuild desde historia autoritativa, o `NOT_READY` si la continuidad exacta no es demostrable. `stream_seq` sigue siendo el token canónico downstream y se asigna **sólo después** de que la entrada física fue aceptada como evento distinto (§4).
- **R3 — Sequence granularity.** Dejó de congelarse `(stream_id, source_seq)` como identidad semántica universal. `SourceCapabilities` declara scope/granularidad de la secuencia (EVENT vs PACKET/MESSAGE), capacidad de posición estable in-packet y clase de identidad dedup-safe. Regla dura: una sequence de packet con N market entries jamás colapsa N MarketEvents; la equivalencia entre members sólo puede arbitrarse first-wins cuando declaran compartir identidad semántica dedup-safe demostrada (§8/§11). Verificación first-party puntual ejecutada para el caso canónico: en CME MDP 3.0 la sequence vive en el header del **packet** (segmento), un packet puede contener múltiples mensajes SBE y un refresh múltiples entries ⇒ CME A/B es **packet-posicional**, no por-evento; la clase a declarar es B (POSITIONAL) con posición in-packet determinística exigida al adapter, nunca "venue_seq por evento".
- **R4 — Source switch ≠ rollover.** Separadas las dos transiciones. Un **pure source switch** preserva el `contract_id` seleccionado antes del switch (in-force de Strategy y pinneado de Operations); la nueva autoridad debe servir ese contract vía `ContractIdentifier(source, MARKET_DATA)`; si no puede, el switch **no aplica** (fail-closed, sin re-resolver silenciosamente otro Contract del backup). NQZ6→NQH7 requiere un **rollover explícito** separado/compuesto (acción owner D2-05), jamás efecto lateral del switch. El contract pinneado de una Operation jamás cambia por ninguna de las dos (§9/§14).
- **R5 — Authority / stream identity consistency.** Elegida **OPTION B (KISS): la stream lógica canónica es estable por Contract y el binding/source es authority metadata con epoch.** `stream_id = (instrument_id, contract_id)` no contiene el binding; un switch no nace ninguna stream: la misma stream lógica cambia su `serving_authority` y `authority_epoch++`. Queda unívoco qué es estable, qué cambia en switch y qué cambia en rollover (§5).
- **R6 — Continuity UNKNOWN after disruption.** `UNKNOWN ≠ GAP_DETECTED` se mantiene y se aclara: UNKNOWN tampoco es prueba positiva de continuidad. En steady-state un source sin primitivas opera bajo su capability declarada; tras disconnect/recovery no se re-certifica history-dependent consumption por un BBO fresco. Las capacidades de recovery se declaran por separado para QUOTE-current-state y TRADE-history; si una Strategy requiere bars/trade history, existe el seam de history rebuild (D2-06B) o permanece not-ready. Sin diseñar B: sólo el seam correcto de capability/readiness (§10/§11/§12).
- **R7 — Do not freeze D2-06C's recorded stream.** `echo.market-events.v1` deja de congelarse como "transporte + recorded replay stream". Es el candidato de transporte canónico LIVE, puede llevar retention y servir recovery corto si corresponde, y es una fuente posible de recording; la decisión definitiva (ordering reproducible, recording contract, retention/durability, replay injection) es de D2-06C (§16/§17/§21).
- **Provenance terminology.** `feed_kind=REPLAY` se separa en dos conceptos: `origin.recovery_provenance = LIVE | RECOVERY_REPLAY | SNAPSHOT` (por evento, recovery/switch) vs `run_mode` (nivel de run: LIVE/SHADOW/DEMO/REPLAY/BACKTEST, concepto D2-04 que D2-06C formaliza para el replay determinista). Sin diseñar C; sólo sin colisión semántica (§3).
- **Acceptance additions:** I (switch heterogéneo con Operation viva), J (switch ≠ rollover), K (trades reales idénticos sin identity nativa), L (packet sequence con N entries) — §19.
- `OWNER_DECISIONS_REQUIRED = NONE`.

## 1. Executive verdict

```text
D2-06A STATUS: READY_FOR_SUBMANAGER_REVIEW  (post-repair R1)
```

El contrato V1 de MarketFeedEngine se congela alrededor de dos identidades separadas por construcción: **la stream lógica canónica, estable por Contract** (`stream_id = (instrument_id, contract_id)`), y **la autoridad MARKET_DATA que la sirve** (binding D2-05 + members + `authority_epoch`, metadata que cambia por switch explícito). Todos los consumidores (Strategy vía su motor, MM de una Operation pinneada) leen streams lógicas read-only por `contract_id`; el número de Accounts es invisible para el engine. La **demanda es económica**: los consumidores declaran qué contract necesitan; el engine la resuelve contra la autoridad activa vigente para producir subscriptions físicas — un switch de autoridad re-sirve los MISMOS contratos con la nueva fuente y ningún demandante queda amarrado al binding abandonado. Los feeds físicos equivalentes (CME A/B o endpoints equivalentes) viven DENTRO de una autoridad como *members* arbitrados **sólo cuando declaran compartir identidad dedup-safe demostrada** (CME A/B = clase packet-posicional); los sources heterogéneos son autoridades distintas y sólo cambian por un **source switch explícito** que preserva contratos (jamás rollea), con pérdida de readiness, nunca blend. Health separa tres dimensiones (liveness por member, continuity por primitivas del source, freshness por config) y **el calendario de D2-05 es la autoridad que decide cuándo el silencio es esperado**: ExchangeCalendar CLOSED + cero ticks por horas jamás es failure. Recovery es una máquina conceptual única con ejecución capability-specific y **clases de identidad honestas**: si el source no da identidad dedup-safe, no se fabrica — la continuidad se demuestra por cursor/snapshot/rebuild o el stream queda NOT_READY. `OWNER_DECISIONS_REQUIRED = NONE`.

Físicamente el engine es un nuevo StateFun keyed function `echo/market_stream` (key `stream_id` lógica) sobre los patrones ya congelados en D2-04/D2-05: adapters productores → Kafka → engine arbitra/normaliza → topic canónico `echo.market-events.v1` (transporte LIVE; grabación definitiva = decisión D2-06C) + topic compactado de control `echo.market-stream-state.v1` (readiness/epoch). El egreso canónico es AT_LEAST_ONCE con idempotencia por `stream_seq` (decisión deliberada: exact-once transaccional retardaría ticks al intervalo de checkpoint; el gap/seam se declara, no se esconde). La demanda de Operation egresa por el fact path transaccional de D2-04.

## 2. Scope / non-scope

**En scope (V1 freeze):** envelope canónico MarketEvent; identidad/dedup por clases capability-driven; identidad de stream lógica vs autoridad servidora; relación Instrument/Contract/MarketDataBinding; ciclo de subscription por demanda económica; redundancia equivalente capability-driven; separación switch de autoridad vs rollover; liveness/continuity/freshness; adapter capability contract; recovery por clase; readiness barrier; provenance (recovery vs run); coexistencia current vs pinned Contract; durable/history seam mínimo; ownership físico; reuse map Echo V3.

**Fuera de scope (exclusivo de otros workers/hitos):** barras/MTF/indicadores/warm-up depth (D2-06B); clock determinista, ordering/replay LIVE↔REPLAY, recorded stream contract y retención definitiva (D2-06C); selección de transport de ejecución (D2-07); selección de vendor de feed (queda config); capacity benchmark (D6); escalado/migración global (D2-08); MoneyManagement monetary action (nunca).

## 3. Minimal MarketEvent

Envelope único y común para todo el runtime (LIVE, recovery, warmup, replay). Sólo QUOTE (BBO) y TRADE en V1: S1 (30m ORB sobre trades) y MM hardscalping (BBO) los cubren; ProjectX market hub expone quote/trade/depth y CME MDP trades/quotes/depth — depth/book no tiene consumidor V1 (sin book strategies en la cohorte) y queda DEFERRED; SESSION transitions no son market events (vienen del calendario D2-05, §8-10); BAR no es evento de feed (construcción = D2-06B).

```text
MarketEvent {
  stream_id            # identidad LÓGICA: (instrument_id, contract_id) — estable ante
                       # switch de autoridad (§5)
  instrument_id        # canónico, desnormalizado para consumidores
  contract_id          # physical contract del stream
  event_type           # QUOTE | TRADE
  event_ts             # instant del evento (RFC3339Nano UTC); venue-authoritative
                       # cuando el capability lo declara; si no, source event time
  receive_ts           # wall clock de ingestion (sólo liveness/telemetría,
                       # JAMÁS semántica de dominio)
  source_event_position?   # { sequence, entry_index?, native_event_id? } — la
                       # posición del evento en el source según capability (§11);
                       # ausente (no cero) para sources sin ninguna de ellas
  stream_seq           # monotónico por stream, asignado por el engine SÓLO DESPUÉS
                       # de aceptar la entrada física como evento distinto (post-
                       # arbitraje/dedup por identidad declarada): contiguo, sin
                       # duplicados por construcción, jamás renumerado
  authority_epoch      # epoch de la AUTORIDAD SERVIDORA de la stream lógica
                       # (incrementa en switch de source y en recovery que invalida
                       # continuidad; NO cambia por rollover)
  origin               # { source_id, recovery_provenance:
                       #    LIVE | RECOVERY_REPLAY | SNAPSHOT }
  payload:
    QUOTE { bid_price, bid_qty, ask_price, ask_qty }   # decimales en quote_currency
    TRADE { price, qty }
}
```

No hay quality score, no hay ontology universal, no hay campos "por si acaso". Reglas de congelación: `receive_ts` jamás participa de semántica de barras/estrategia (D2-05 §9: cuatro tiempos, el event time manda); `source_event_position` es opcional por diseño — su presencia/ausencia está gobernada por el capability contract (§11), no por heurística; `recovery_provenance` describe la **procedencia de recovery del evento** (replay de source o snapshot durante un cutover) y jamás significa el modo de ejecución del run — el modo del run es `run_mode` (LIVE/SHADOW/DEMO/REPLAY/BACKTEST, D2-04), cuyo replay determinista pertenece a D2-06C; `stream_seq` es el token de continuidad/idempotencia del path canónico aguas abajo (dedup O(1) por comparación).

## 4. Event identity / dedup — tres clases capability-driven

Tres identidades distintas, jamás colapsadas:

| Capa | Identidad | Quién la asigna | Uso |
|---|---|---|---|
| **Transport message identity** | `(member/source_id, transport seq/packet)` del feed físico | el adapter/source | diagnóstico, liveness del member |
| **Logical semantic event identity** | según clase declarada del source (A/B/C, §11) | el source (clases A/B); inexistente (clase C) | dedup entre members equivalentes y overlap de replay |
| **Echo stream identity** | `stream_seq` contiguo por stream | el engine, tras aceptar el evento como distinto | orden canónica, idempotencia downstream, barrier |

**Clases de identidad semántica (gobernanza de dedup):**

- **Clase A — identity de evento estable.** El source entrega una identidad que identifica exactamente UN evento canónico: native event/trade id del venue, o una sequence cuyo scope declarado es EVENT. Dedup exacto permitido: tracking monotónico por stream; `seq ≤ last` se suprime; salto = GAP_DETECTED (§12).
- **Clase B — sequence de transport/packet con posición determinística.** La sequence identifica PACKET/MESSAGE, no evento. La identity dedup-safe DEBE incluir la posición dentro del packet/message: `(sequence, entry_index)` o `(sequence, native_event_key)`, y sólo existe si el adapter puede construirla **determinísticamente**. Ejemplo probado first-party: CME MDP 3.0 — la sequence va en el header del packet UDP (segmento), un packet puede contener múltiples mensajes SBE y un refresh múltiples entries ⇒ CME A/B es clase B, nunca "venue_seq por evento"; una packet sequence 100 con 3 market entries produce TRES MarketEvents con identities (100,0), (100,1), (100,2).
- **Clase C — sin identidad dedup-safe.** Content-hash/content-tuple dedup de trades está **PROHIBIDO**: dos trades físicos legítimos pueden compartir `event_ts/price/qty` y ambos deben conservarse (alterar uno corrompe volume/bars/indicadores/decisiones). Echo no inventa la identidad. Recovery sólo por mecanismos que no exigen distinguir gemelos: cursor/rango no-solapado, cursor nativo determinístico del source, snapshot replacement cuando la semántica lo permite, full rebuild desde historia autoritativa, o `NOT_READY` si la continuidad exacta no puede demostrarse. En steady-state un solo feed ordenado por la partición Kafka no necesita dedup.

Casos resueltos:

- **A — CME MDP A/B (clase B demostrada):** los members comparten el espacio de sequence de packet del venue; dedup first-wins por `(stream, sequence, posición in-packet)`; el gemelo (mismo packet, misma posición, por el otro feed) se suprime ANTES de asignar `stream_seq`; las 3 entries de un packet sobreviven como 3 eventos. Sin voting, sin scoring (YAGNI).
- **B — Gap replay que reentrega:** el replay entra como candidate con `recovery_provenance=RECOVERY_REPLAY` y su `source_event_position` (clase A/B); el overlap contra lo ya emitido se suprime por identidad ANTES de asignar `stream_seq` ⇒ la stream canónica nunca repite ni reordena.
- **C — Reconnect overlap (clase A/B):** el adapter reconecta desde `last_sequence+1` (capability) o natural refresh; el overlap resultante muere en dedup por identidad.
- **D — Reconnect/disruption (clase C):** prohibido re-solapar rangos ambiguos: recovery por cursor no-solapado, snapshot de estado, o full rebuild; si ninguna es suficiente para el consumo requerido ⇒ NOT_READY (§12). En steady-state no hay dedup y no hay costo hot-path.
- **E — Trade nativo con id (clase A vía `native_event_id`):** dedup exacto aunque no haya sequence; `source_trade_id`/event id es identidad del venue, jamás sintetizada por Echo.

**Prohibido congelado:** no se fabrica identidad desde contenido ni un UUID para "fingir" source identity; no se sacrifica un evento físico real para aparentar idempotencia — la falsa apariencia de dedup es un defecto, no un feature. Si el recovery no puede distinguir exactamente dos trades idénticos, ambos se preservan o el stream queda fail-visible (no heurística de pérdida).

## 5. Logical stream identity — OPTION B (KISS)

```text
MarketStream {
  stream_id    = (instrument_id, contract_id)      # LÓGICA: estable ante switch;
                                                   # el binding NO participa
  serving_authority = { binding_id (MARKET_DATA de D2-05), members físicos,
                        authority_epoch }
  external_ids = { source_id → ContractIdentifier }   # resueltas por (source, context)
  demand       = config_demand ∪ operation_demand     # económica (§7)
  state        = SUBSCRIBING | READY | RECOVERING | RETIRING | UNSUBSCRIBED
}
```

Univocidad R5 — qué es estable y qué cambia:

```text
STABLE (jamás cambia por switch ni rollover):
  stream_id = (instrument_id, contract_id) de cada contrato demandado;
  el contract_id pinneado de cada Operation; stream_seq (token downstream,
  jamás renumerado); la identidad de los demandantes.

CAMBIA EN SOURCE SWITCH (transición explícita de autoridad):
  serving_authority {binding_id, members}; authority_epoch++; provenance por
  evento; readiness (barrier + rebuild). NINGÚN contract_id cambia; la demanda
  sigue idéntica; no nace ni muere ninguna stream lógica.

CAMBIA EN ROLLOVER (acción owner explícita D2-05, prospectiva):
  la selección in-force del Contract corriente para consumo Strategy ⇒ pasa a
  demandarse OTRA stream lógica (contract nuevo). Las streams de contratos
  pinneados por Operations persisten hasta RELEASE.
```

Congelado:

- **Qué consume Strategy:** MarketEvents de la stream lógica del contract **in-force** del Instrument (la selección corriente cambia sólo por rollover explícito, §14; jamás se re-deriva por un switch). La Strategy ve `instrument_id`, nunca binding ni fuente física (D2-03; el StrategyEngine resuelve instrument → stream in-force).
- **Qué consume MM con Operation pinneada:** MarketEvents de la stream lógica `(instrument, contract_id pinneado)` — siempre el mismo `contract_id`, sea cual sea la autoridad servidora; incluido un contract viejo en RETIRING (§14). La migración entre autoridades ocurre detrás de la readiness barrier (§9) y es transparente para el demandante.
- **Quién resuelve current Contract (dos pasos D2-05, roles distintos):** la fila de mapping `(MARKET_DATA, binding_id, instrument_id) → contract_id` es la **selección corriente por binding** y sólo se evalúa en acciones explícitas de selección/rollover; `ContractIdentifier(source, MARKET_DATA, contract)` es la **servabilidad** de un contract específico por fuente y se consulta al suscribir y al validar un switch. Un switch consulta servabilidad, jamás re-evalúa la selección (§9).
- **Cómo entra MarketDataBinding:** la config de cada autoridad (binding: members, capabilities, thresholds de freshness) y la selección de autoridad activa por instrumento son config hot con el patrón compacted-topic/kache ya congelado; readiness fail-closed (`MARKET_CONFIG_NOT_READY`).
- **Cuándo nace una subscription:** la entrada del (instrument, contract) en `demand` (§7). **Cuándo puede cerrarse:** salida de `demand`. **Jamás se desuscribe un Contract con consumidor vivo** — garantizado por construcción: RETIRING sólo termina cuando operation demand = ∅.
- **Convivencia current/pinned:** dos streams lógicas coetáneas (`(NQ, NQZ6)` RETIRING + `(NQ, NQH7)` READY), cada una con su `stream_seq`, su health y su readiness, ambas servidas por la misma autoridad activa. No hay mixing posible: el stream_id ya separa los espacios.

## 6. Instrument / Contract / MarketDataBinding

Heredado sin cambios de D2-05 (§4-6): `Instrument` canónico → `Contract` expiry-specific vía mapping hot por binding; `ContractIdentifier` por `(source, context)` para el string literal del vendor; los identifiers NO participan del mapping y se resuelven en un segundo paso local al suscribir. Identifier ausente para el `(source, context)` requerido = fail-closed: el member no puede suscribirse ⇒ readiness NO_READY(NO_LIVE_MEMBER) si era el único; jamás identidad por string vendor. Un cambio de mapping no muta streams existentes: una acción de rollover crea demanda de la stream nueva (§7/§14). Dos roles separados desde R4: **mapping row = selección corriente** (evaluada sólo en selección/rollover explícito) y **ContractIdentifier = servabilidad** (consultada al suscribir y en cada switch).

## 7. Subscription lifecycle — demanda económica

Demand = unión de dos fuentes, sin reference counting framework. **La demanda expresa necesidad económica, nunca autoridad física** (R1): no contiene `binding_id`; el engine la resuelve contra la autoridad activa vigente:

1. **config_demand** — catálogo del runtime: instrumentos habilitados para consumo Strategy × contract in-force (seleccionado por acción explícita de config/rollover contra la autoridad activa). Cambia por config hot (rollover, alta/baja de instrumento) o por switch de autoridad que re-sirve los mismos contratos.
2. **operation_demand** — demandas de MM por Operation viva. El owner `echo/operation` emite transaccionalmente en su frontera de checkpoint (mismo egress fact pattern R14 de D2-04):

```text
MarketDemand {
  operation_id
  instrument_id
  contract_id          # el pinneado por la Operation (D2-01/04/05)
  intent: ACQUIRE | RELEASE
}
```

   ACQUIRE en la materialización (con el contract pinneado), RELEASE al TERMINAL. Idempotente por membresía `(operation_id, contract_id)` (set, no contadores). Sin leases, sin reference counting.

**Resolución demanda + autoridad → subscription física:** para cada `(instrument, contract)` demandado, el engine consulta la autoridad MARKET_DATA activa del instrumento y valida servabilidad: `ContractIdentifier(source, MARKET_DATA, contract)` resoluble para los members + capabilities declaradas (§11). Servable ⇒ subscribe members; no servable ⇒ `NOT_READY(CONTRACT_NOT_SERVABLE)` fail-closed (y un switch que requiera ese contract no aplica, §9). Tras un switch, la MISMA demanda económica produce la subscription con la nueva autoridad: ninguna Operation queda estructuralmente amarrada al binding que estaba activo cuando nació.

```text
SUBSCRIBING  entrada en demand: resolver identifiers, conectar members,
             baseline de continuidad + snapshot/first BBO ⇒ readiness barrier
READY        sirviendo decisiones (único estado que habilita evaluación nueva)
RECOVERING   continuidad perdida o cutover de autoridad en curso; los eventos
             fluyen para rebuild, el gate de decisión está cerrado (§12/§13)
RETIRING     salió de config_demand (rollover/baja) pero operation_demand > ∅
UNSUBSCRIBED demand = ∅: desconexión y liberación — legítima porque no
             queda ningún consumidor
```

Caso H de escala por construcción: 20 o 200 execution accounts con la misma Strategy S1 = la MISMA subscription `(NQ, NQH7)`. Account count no aparece en el engine; el fan-out a cuentas ocurre aguas abajo (StrategyEngine/fan-out D2-04) sobre la stream compartida read-only.

## 8. Equivalent feed arbitration — capability-driven (dentro de una autoridad)

Config: un binding declara sus members (p.ej. `cme-a`, `cme-b` vía el mismo source vendor, o endpoints A/B equivalentes). **La equivalencia es capability-driven, no asumida:**

- Members pueden declararse equivalent dentro de una autoridad **sólo si declaran la misma clase de identidad dedup-safe (§4/§11) y demuestran compartirla**: clase A = mismo espacio de identidad de evento; clase B = mismo espacio de sequence de packet + misma semántica de posición in-packet determinística. La granularidad exacta de ese espacio compartido debe estar probada por evidencia first-party del source antes de declararla (para CME MDP 3.0 está probada a nivel packet-posicional, R3).
- **No demostrable ⇒ no pueden ser equivalent members de la misma authority**: son bindings distintos y su cambio es un switch explícito (§9). Mezclar clases dentro de una autoridad = config inválida fail-closed.
- **Regla dura:** una sequence de packet con N market entries jamás colapsa N MarketEvents; la identity de arbitraje es `(sequence, posición)` o no hay arbitraje.

- **Precedence/arbitration:** first-wins por logical semantic event identity declarada. No hay "feed A primario": CME recomienda procesar ambos; el engine consume ambos members siempre que sea posible y arbitra por llegada.
- **Continuity/sequence:** el espacio de identidad compartido es del venue ⇒ la continuidad se evalúa sobre ese espacio (packet-level para MDP3), no sobre qué member entregó cada mensaje.
- **Duplicate suppression:** gemelos por identidad (incluida posición in-packet) suprimidos; costo O(1). Los N entries de un packet sobreviven siempre.
- **Failover intra-autoridad:** automático y continuo. Si el member activo muere, el otro sigue entregando; si la continuidad del espacio compartido queda verificada, **no hay barrier** (sólo cambia `origin.source_id` en provenance + telemetría). Si el member superviviente no puede demostrar continuidad, el stream cae a RECOVERING y recovery normal (§12).
- **Recovery:** capability-driven, idéntico al caso single-feed.
- **Provenance:** cada evento porta `source_id` del member que lo produjo; el estado del stream porta el member set activo. Diagnóstico "¿quién produjo este estado?" responde sin contaminar el envelope con detalles vendor.

**Prohibido congelado:** sumar ticks A+B como si fueran eventos distintos, ejecutar Strategy dos veces por el mismo evento, y deduplicar por packet sequence sola (colapsaría N entries) — los tres imposibles por construcción (dedup por identidad declarada previo a `stream_seq`; una sola salida canónica).

## 9. Source authority switch ≠ contract rollover (entre autoridades)

Bindings distintos = autoridades distintas, jamás mezcladas. Son **dos transiciones separadas que nunca se implican mutuamente** (R4):

- **A. SOURCE AUTHORITY SWITCH** — cambia quién sirve las streams lógicas existentes. No toca ninguna selección de Contract: el in-force de Strategy y el pinneado de cada Operation permanecen exactos.
- **B. CONTRACT ROLLOVER** — acción owner explícita (D2-05 §6, hot, prospectiva) que cambia la selección in-force y pasa el consumo Strategy a otra stream lógica. Puede componerse con un switch como dos pasos deliberados; jamás es efecto lateral de uno.

V1 congela: **el switch es una transición explícita de config** (cambio de active authority del instrumento, operador/owner u automatismo operacional futuro — no silencioso nunca); no hay failover automático cross-vendor en V1 (ningún evidence lo exige; B2 lo deja como decisión técnica; KISS lo difiere con alerta de readiness como mitigation).

Semántica del pure switch:

```text
1. config (explícita, operador/owner): active MARKET_DATA authority NQ:
   dbt-main → dbt-backup. La selección in-force (p.ej. NQZ6) NO se re-evalúa.
2. validación de servabilidad por el engine, por cada stream lógica demandada
   de NQ (in-force + pinneadas): ContractIdentifier(dbt-backup, MARKET_DATA,
   contract) + capabilities.
   FALLA ⇒ switch RECHAZADO no-op fail-closed: la autoridad previa sigue
   sirviendo, motivo CONTRACT_NOT_SERVABLE visible en el estado de control,
   alerta al operador. JAMÁS se re-resuelve silenciosamente el Contract
   corriente distinto del backup (NQZ6→NQH7 sería auto-roll, prohibido).
3. válido ⇒ authority_epoch++ en cada stream lógica afectada; readiness
   NOT_READY(SWITCHING_AUTHORITY); barrier ON (gate de decisión cerrado);
   contract_id in-force y pinneados INTACTOS.
4. boot con la autoridad nueva según sus capabilities: snapshot BBO/refresh
   natural + baseline de continuidad propia.
5. rebuild downstream sobre el epoch marker (contrato D2-06B); MM de toda
   Operation viva migra su input de mercado tras barrier/recovery — migra el
   SERVING, no el contrato ni el demandante.
6. READY con epoch nueva y provenance del source nuevo; la conexión al source
   viejo se retira al completar el cutover (sólo el overlap transicional
   necesario; después no queda dependencia estructural al binding viejo).
```

- **Readiness loss:** siempre (aunque el source nuevo esté "sano": semantic differences no auditables ⇒ barrier obligatoria).
- **Gap/recovery handling:** tras el switch rige el capability del source nuevo; si no puede cubrir el hueco desde el último estado común, el stream queda NOT_READY(GAP_UNRESOLVED / RECOVERY_UNPROVABLE) fail-closed — sin síntesis de datos.
- **Hot-state rebuild:** obligatorio downstream (D2-06B); el engine emite el epoch marker que delimita la reconstrucción.
- **Provenance:** `authority_epoch` + `origin.source_id` en cada evento; el estado compactado del stream porta la historia de epochs.
- **READY nuevamente:** sólo con baseline de continuidad del source nuevo completa + warmup downstream consumado (señal de B, §13).
- **Caso operations/in-force mixtas tras rollover:** si además existe una stream pinneada `(NQ, NQZ6)` y la in-force es `(NQ, NQH7)`, el switch valida servabilidad de AMBAS; bloquear cualquiera bloquea el switch (el operador decide: rollear primero, o elegir backup que sirva ambas).

Nunca silent blend: la fusión de dos autoridades en una serie es un defecto arquitectónico, no un modo. Nunca auto-roll: el switch jamás consulta la fila de mapping de la autoridad entrante para cambiar la selección corriente.

## 10. Liveness / Continuity / Freshness

Tres dimensiones separadas por congelación; ninguna se colapsa en un booleano "healthy":

| Dimensión | Scope | Evidencia válida | Estados |
|---|---|---|---|
| **LIVENESS** | por member físico | conexión + heartbeat del source cuando existe (CME Admin Heartbeat, Databento heartbeat); inactividad sólo cuenta mientras `SessionState=OPEN` del calendar_id del instrumento | CONNECTED / DEGRADED(heartbeat o inactividad bajo sesión OPEN) / DISCONNECTED |
| **CONTINUITY** | por stream | exclusivamente primitivas del source: sequence jump, reconnect callback con rango, estado de replay. **Un salto de timestamps NO es evidencia de gap** (B2 correction); un source sin primitivas declara CONTINUITY=UNKNOWN, no "roto" | CONTIGUOUS / GAP_DETECTED / UNKNOWN |
| **FRESHNESS** | por stream | `event_ts`/`receive_ts` vs wall clock contra threshold **config por source/schema/instrument**; supervisión activa sólo con sesión OPEN | FRESH / STALE(policy) / NOT_EVALUABLE(session cerrada/break) |

Aclaración R6 sobre UNKNOWN: **UNKNOWN no es GAP_DETECTED, pero tampoco es prueba positiva de continuidad.** En steady-state, un source sin primitivas opera bajo su capability declarada (UNKNOWN visible en StreamState + liveness/freshness como evidencia operativa). Tras disconnect/reconnect o cualquier disruption, UNKNOWN no re-certifica nada: un BBO fresco certifica únicamente consumo de *current state* (QUOTE). El consumo *history-dependent* (trades/bars/indicadores) exige continuidad demostrada según la clase del source: identidad dedup-safe A/B + replay, snapshot con semántica de reemplazo suficiente, o full rebuild desde historia autoritativa (§12); QUOTE-state recovery y TRADE-history recovery se declaran como capacidades separadas (§11) y pueden diferir. Si una Strategy requiere historia y no hay rebuild demostrable, permanece not-ready hasta que D2-06B recomponga su estado — sólo se congela aquí el seam de capability/readiness.

Estados compuestos obligatorios (verificación del modelo, no enum normativo):

- transport CONNECTED pero stream gapped ⇒ LIVENESS ok + CONTINUITY GAP_DETECTED ⇒ RECOVERING.
- DISCONNECTED pero último market state usable ⇒ NOT_READY(NO_LIVE_MEMBER) con `last_known_state` + `as_of` + stale flag aún legible para MM/safety (§15.1).
- CONNECTED sin actividad porque ExchangeCalendar=CLOSED ⇒ liveness supervisa heartbeats (si el source los emite en sesión cerrada), freshness NOT_EVALUABLE; **jamás failure por elapsed wall-clock**.
- "no tick en 5 segundos" jamás es regla universal: los umbrales son config técnica por source/instrument y se evalúan sólo bajo sesión OPEN (B2 manager: no freeze timeout universal).
- RECOVERING ⇒ barrier cerrada; READY ⇒ gate abierta.
- Recovery de disruption completada con BBO fresco en source clase C ⇒ READY sólo para consumo current-state; history-dependent consumption sigue gated (RECOVERY_UNPROVABLE) hasta rebuild demostrado.

## 11. Adapter capability contract

Declarado por source en config (namespace `source` = el mismo de `ContractIdentifier`, D2-05 §4). El engine es genérico sobre capabilities; las diferencias reales de vendors quedan visibles, no escondidas tras una interface falsa:

```text
SourceCapabilities {
  source_id
  sequence:           NONE | SOURCE_LOCAL | VENUE_STRONG   # VENUE_STRONG = espacio
                                                           # compartido entre members
                                                           # equivalentes
  sequence_scope:     EVENT | PACKET | NONE                # qué identifica la secuencia:
                                                           # un evento canónico o un
                                                           # packet/message del transporte
  event_position:     NONE | DETERMINISTIC                 # posición in-packet / native
                                                           # event key construible
                                                           # determinísticamente
  dedup_identity:     EVENT | POSITIONAL | NONE            # clase de identidad dedup-safe
                                                           # declarable (§4 A/B/C)
  gap_detection:      SEQUENCE_BASED | NONE                # NONE ⇒ CONTINUITY=UNKNOWN
  replay:             { supported, modes: [FROM_SEQ|FROM_TIME|FROM_DISCONNECT],
                        bounds, typical_latency_class }
  snapshot:           { supported, kinds: [BBO_SNAPSHOT|BOOK_SNAPSHOT|NATURAL_REFRESH] }
  heartbeat:          { supported, interval }
  reliable_ts:        [EVENT_VENUE | EVENT_SOURCE | RECEIVE_ONLY]
  recovery_state:     REPLAY_EVENTS | SNAPSHOT_REPLACE | NATURAL_REFRESH
                                                           # QUOTE / current-state
  recovery_history:   REPLAY_EVENTS | FULL_REBUILD | UNSUPPORTED
                                                           # TRADE / history-dependent
}
```

Reglas de validación (fail-closed en carga de config):

- `sequence=NONE` ⇒ `gap_detection=NONE` ∧ `sequence_scope=NONE`.
- `dedup_identity=EVENT` ⇔ existe identidad de evento estable: `sequence_scope=EVENT` ∨ native event id (`native_event_id`/`source_trade_id` del venue).
- `dedup_identity=POSITIONAL` ⇔ `sequence_scope=PACKET` ∧ `event_position=DETERMINISTIC`.
- `dedup_identity=NONE` en todo otro caso ⇒ recovery obligatoriamente overlap-free (§12); content-dedup prohibido por construcción del contrato.
- recovery de historia prometido sin replay ni full-rebuild ⇒ config inválida; `recovery_history=UNSUPPORTED` ⇒ tras disruption el consumo history-dependent queda gated (no es config válida "para todo").
- `reliable_ts=RECEIVE_ONLY` ⇒ `event_ts` no puede marcar barras venue-authoritative (B decide cómo tratarlo con esa declaración).
- Members equivalentes de una misma authority: misma clase `dedup_identity` + semántica de secuencia compatible + evidencia first-party del espacio compartido (§8); distinto ⇒ no son equivalent members.

El engine no infiere capabilities por comportamiento observado: lo no declarado es "no soportado". Ejemplos: CME MDP 3.0 ⇒ `sequence=VENUE_STRONG, sequence_scope=PACKET, event_position=DETERMINISTIC, dedup_identity=POSITIONAL` (R3); un source sólo-BBO sin sequence ni ids ⇒ `dedup_identity=NONE, recovery_state=SNAPSHOT_REPLACE, recovery_history=UNSUPPORTED`.

## 12. Recovery

Máquina conceptual V1 (ejecución capability-specific; es el único algoritmo permitido y no hay recovery universal):

```text
CONTIGUOUS (READY)
  → gap/reconnect detectado por primitiva del source (§10)
  → stream pierde readiness ⇒ RECOVERING (barrier ON; gate de decisión cerrado)
  → recovery según capability y CLASE de identidad:
      con identidad dedup-safe (A/B) y replay:
        REPLAY_EVENTS → pedir rango faltante (FROM_SEQ/TIME/DISCONNECT) al
                        MarketHistorySource o al live replay del vendor;
                        overlap suprimido por identidad (§4 B/C) ANTES de
                        asignar stream_seq
      sin identidad dedup-safe (clase C): sólo mecanismos overlap-free:
        SNAPSHOT_REPLACE  → snapshot del estado (BBO) + retomar desde ahí
                            (certifica current-state, §10)
        NON_OVERLAPPING_CURSOR → retomar en un punto de corte acordado sin
                            re-solapar lo ya ingerido
        FULL_REBUILD      → reconstruir desde historia autoritativa
                            (MarketHistorySource) si el consumo lo exige
      heurística de descarte de "posibles duplicados": PROHIBIDA
  → epoch marker / RecoveryBarrier emitido aguas abajo
    { stream_id, epoch_nuevo, rango afectado o snapshot marker }
  → affected downstream hot state se reconstruye (bars/forming/indicadores:
    contrato de D2-06B; el engine delimita, no reconstruye)
  → readiness barrier levantada sólo con continuidad demostrada para las
    clases de consumo que cada capability soporte + warmup downstream
    consumido ⇒ READY (epoch nueva); si la continuidad exacta no es
    demostrable para un consumo requerido ⇒ NOT_READY(RECOVERY_UNPROVABLE)
```

- **Qué se pausa:** sólo la *evaluación de decisiones nuevas* de ese stream (gate). **Qué sigue disponible:** el último market state (marcado as_of/stale), el path de Orders/Fills/Operations (ejecución es otro dominio), la telemetría, y los eventos de recovery que fluyen para rebuild.
- **Provenance de recovery:** `recovery_provenance=RECOVERY_REPLAY|SNAPSHOT` en cada evento + `authority_epoch` en el stream ⇒ cualquier estado downstream declara de qué epoch proviene (sin colisionar con `run_mode`, §3).
- **Downstream sabe que los datos no son confiables** por tres señales coherentes: estado de readiness del stream (compacted topic), RecoveryBarrier/epoch markers inline, y provenance por evento.
- **Reinicio de evaluación segura de Strategy:** el StrategyEngine/MM evaluadores consumen el gate READY del stream; mientras RECOVERING, los inputs de evaluación están invalidados y las Strategies no producen decisiones nuevas para ese stream; MM/safety aplican su policy (§15). La evaluación se re-habilita con el stream READY y el warmup downstream completo — nunca antes.
- **Fuera de bounds** (p.ej. hueco mayor que replay bounds del vendor): NOT_READY(GAP_UNRESOLVED / RECOVERY_UNPROVABLE) persistente + alerta operador; sin síntesis, sin "mejor esfuerzo" silencioso, sin sacrificar eventos físicos por una falsa apariencia de idempotencia.

NO se define MoneyManagement monetary action: Market Runtime informa quality/readiness; MM/safety deciden qué hacer monetariamente.

## 13. Readiness (barrier)

Superficie canónica por stream, publicada en `echo.market-stream-state.v1` (compacted, key `stream_id`) y como epoch markers inline en `echo.market-events.v1`:

```text
StreamState {
  stream_id, epoch, readiness: READY | RECOVERING | NOT_READY,
  reasons: [ NO_LIVE_MEMBER | GAP_UNRESOLVED | RECOVERY_UNPROVABLE
           | STALE_BEYOND_POLICY | SWITCHING_AUTHORITY | CONTRACT_NOT_SERVABLE
           | WARMUP_INCOMPLETE | CONFIG_NOT_READY ],
  last_known_state_ref/as_of, members activos, authority provenance
}
```

Consumers (StrategyEngine, MM market gate, fronts) kache-an este estado (patrón compacted/WaitReady). El gate de decisión nueva exige READY del stream referenciado; el calendar CLOSED acota availability antes del gate (D2-05 §10), de modo que readiness y session availability componen sin solaparse. La barrera se levanta con evidencia, no con timeout. `RECOVERY_UNPROVABLE` y `CONTRACT_NOT_SERVABLE` son los motivos R6/R4: continuidad exacta no demostrable para el consumo requerido, y switch bloqueado por contract no servible por la autoridad entrante.

## 14. Rollover / current vs pinned Contract

Escenario obligatorio (congelado D2-05 §6; aquí su cara de feed). El rollover es la transición B (§9): acción owner explícita sobre el mapping de la autoridad activa, jamás efecto de un switch:

```text
NQ mapping (autoridad activa, p.ej. dbt-main): NQZ6 → NQH7  (owner, hot, prospectivo)

1. acción de rollover recomputa config_demand: nace la stream lógica
   (NQ, NQH7) → SUBSCRIBING (servida por la autoridad activa) → barrier → READY
2. (NQ, NQZ6) → RETIRING: sigue sirviendo NQZ6 mientras haya demanda
3. Strategy: nuevas evaluaciones resuelven NQ → stream (NQ, NQH7)
4. Operation A (pinned NQZ6): su ACQUIRE sigue vivo ⇒ NQZ6 NO desaparece;
   MM de A sigue recibiendo QUOTE/TRADE de Z6 para trailing/gestión
5. A TERMINAL ⇒ RELEASE ⇒ demand(Z6)=∅ ⇒ UNSUBSCRIBED
6. jamás remap, jamás auto-roll, jamás migración de stream (D2-05 §6 intacto)
```

KISS logrado: la coexistencia no requiere reference counting framework — es la unión de dos demand sets idempotentes; el caso "old Contract todavía usado" está cubierto porque RELEASE sólo proviene del terminal de la Operation que lo pedía. El contract pinneado jamás cambia, tanto en rollover como en switch (§9).

## 15. Failure semantics (los seis casos)

1. **Feed down, último hot state usable:** readiness NOT_READY(NO_LIVE_MEMBER); `last_known_state` + `as_of` + stale flag siguen legibles; MM/safety deciden según su policy (gestionar exits con estado marcado, etc.). El engine no bloquea el path de ejecución; sólo deja de certificar frescura.
2. **Continuity unknown** (source sin primitivas): CONTINUITY=UNKNOWN no es NOT_READY por sí mismo ni en steady-state; liveness (heartbeat/disconnect callback) + freshness config son la evidencia. UNKNOWN tampoco certifica continuidad: tras disruption, el re-gate sigue §10/§12 (current-state vs history-dependent). La incertidumbre queda declarada en StreamState, no normalizada a "ok".
3. **Stream recovering:** RECOVERING + barrier (§12); eventos fluyen para rebuild; decisiones nuevas pausadas para ese stream.
4. **Equivalent backup ready:** failover intra-binding automático y continuo (§8, sólo con equivalencia demostrada); readiness se conserva si la continuidad del espacio compartido queda demostrada; provenance cambia de member.
5. **Sólo heterogeneous backup disponible:** switch explícito de autoridad (§9): preserva contratos, valida servabilidad de todo lo demandado, readiness loss + rebuild + epoch nueva; rechazado no-op si el backup no puede servir un contract demandado; jamás blend, jamás auto-roll.
6. **Live Operation expuesta durante outage:** el engine expone readiness/staleness/barrera; **Market Runtime no cierra posiciones ni inventa flatten** (ni por market quality ni por ningún otro trigger market-driven en V1). La reacción monetaria (suspender riesgo nuevo, close-only, ForceClose provider-driven) pertenece a MM/safety/provider_rules D2-04/D2-05, que ya tienen sus planes asíncronos.

## 16. Durable / history seam

Tres cosas distintas que no se colapsan:

| Pieza | Qué es | V1 físico |
|---|---|---|
| **Hot state** | estado vivo por stream/aguas abajo | in-memory (engine state + D2-06B), reconstructable |
| **Recoverable market history** | fuente de recuperación/warmup | `MarketHistorySource` interface con adapters (vendor replay/history); **sin elección de data lake/DB en D2-06A** |
| **Recorded replay stream** | la serie normalizada grabada para replay/backtest determinista | **SEAM ABIERTO de D2-06C — no congelado aquí (R7).** `echo.market-events.v1` es el candidato de transporte canónico LIVE, puede llevar retention y servir recovery corto si corresponde, y es una fuente posible de recording; la decisión definitiva (ordering reproducible, recording contract, retention/durability requirements, replay injection) la toma D2-06C |

`MarketHistorySource.read(stream_id, from, to) → [MarketEvent]` — mismo envelope canónico, misma semántica; lo consume recovery (§12) y el warmup handoff de D2-06B (reconstrucción de barras/indicadores previa a READY). Restart del engine: estado desde checkpoint Flink; demand sets re-derivan del propio estado checkpointeado (config + operation demands son parte del keyed state); los members reconectan con resubscribe/baseline por capability. No event sourcing, no store nuevo, no DB monstruosa.

## 17. Physical topology (feed portion)

```text
feed adapters (procesos edge, 1 por source member)
  vendor SDK/socket → normaliza schema vendor → MarketEvent candidate
  → Kafka `echo.market-feed-candidates.v1` (key: stream_id|source_id)
        ↓
echo/market_stream  (StateFun keyed, key = stream_id lógico)   [NUEVO]
  resuelve demanda económica + autoridad activa → subscriptions físicas
  arbitra members por identidad declarada / dedup / detecta gap / recovery
  asigna stream_seq + epoch + origin (post-aceptación del evento)
  mantiene: demand sets, health counters, posiciones de continuidad
  state = Flink checkpointed; timers SendAfter = ticks de health/freshness
        ↓ egress AT_LEAST_ONCE + idempotencia stream_seq
echo.market-events.v1        (canónico; key stream_id; transporte LIVE;
                              grabación/retención definitiva → D2-06C)
echo.market-stream-state.v1  (compacted; readiness/epoch/health; kache)
        ↓
consumers: StrategyEngine / MM market gate / B-bars / fronts (kache + topic)

config hot: catálogo de streams/bindings + SourceCapabilities + thresholds
  → patrón compacted-topic + kache (igual que calendars D2-05 §8)
```

Justificación: **owner** = `echo/market_stream` keyed por `stream_id` lógica (cero Account en las llaves; escalar accounts no toca el engine; un switch no nace keys nuevas). **Durable** = topics Kafka (+ checkpoint Flink del estado del engine). **Derived** = readiness/health projections y el estado compactado de control. **In-memory** = posiciones de continuidad/dedup por identidad, health counters, último estado por stream. **Reconstructable** = todo el estado del engine desde Kafka ingress replay + checkpoint; el hot state downstream desde el topic canónico + `MarketHistorySource`. REUSE del runtime `apache/flink-statefun:3.2.0` ya desplegado; se registran el function y los topics nuevos en `module.yaml` con el mecanismo existente. Riesgo de throughput honesto: tráfico tick × hops Kafka/HTTP es la incógnita física — ver D6, con fallback declarado (§20).

Egresos: el canónico es AT_LEAST_ONCE + `stream_seq` idempotente (exact-once transaccional encadenaría la latencia de ticks al intervalo de checkpoint — incompatible con el hot path; la diferencia con el egreso EXACTLY_ONCE de comandos D2-04 es deliberada y declarada, ambos con su prueba de correctness propia). El egress de `MarketDemand` desde `echo/operation` viaja por el egress transaccional existente (misma frontera de checkpoint que el estado de la Operation, R14) y su consumo es idempotente por `(operation_id, contract_id)`.

## 18. Echo V3 reuse/adapt map

| Pieza V3 | Disposición | Evidencia |
|---|---|---|
| StateFun module.yaml ingress/egress + registro `echo/*` + Go SDK | **REUSE/EXTEND** | `v3/core/deploy/flink-statefun/production/module.yaml`; `v3/sdk/statefun/constants.go` |
| kache / ConfigCache (compacted topic + OffsetOldest + WaitReady) | **REUSE** para catálogo de streams/bindings, capabilities y consumo del estado compactado | `v3/core/internal/config_cache.go`; `v3/sdk/kache/*` |
| SendAfter timers (patrón mm_engine) | **REUSE** para ticks de health/freshness por stream | `v3/core/internal/functions/mm_engine.go` (`ctx.SendAfter`) |
| Compacted hot-config pattern con tombstones (SymbolMapping) | **REUSE patrón** para el catálogo de streams/bindings | `v3/gateway/internal/symbol_mapping_handler.go`; `v3/bridge/internal/symbol_mapping_cache.go` |
| OTel DI + semconv + `echo.*.v1` topic conventions | **REUSE** | `v3/core/internal/telemetry.go`; `v3/sdk/telemetry/*` |
| `echo/inst_snapshot` + `InstrumentSnapshot` (`broker:symbol`) | **REUSE legacy / no autoridad**: observación MT; el authority Futures es este engine (ya congelado en D2-05 §21) | `v3/sdk/domain/snapshots.go` |
| Egress EXACTLY_ONCE config requirement (D2-04 §5.6/R2) | **REQUIREMENT carried**: los egress transaccionales nuevos (MarketDemand fact path) exigen la misma config `EXACTLY_ONCE` + `read_committed`; el egress canónico de market events es AT_LEAST_ONCE por decisión propia (§17) | `Echo Futures — D2-04` §5.6/R2 |
| Bars/replay/market history/MarketHistorySource | **NEW** (no existe nada físicamente: verificado) | búsqueda: sin Bar/Quote/Tick/MarketData/replay en v3 |
| lab_curves / strategy history / Forge ingest | ** unrelated / DEFERRED**: historia analítica, no market feed | `v3/lab-worker/*`; `v3/gateway/internal/forge_ingest_handler.go` |
| Bridge MT5 / feed del Echo Forex | **REPLACE para Futures path**: no se adapta como fuente de market data de futuros | — |

## 19. Acceptance cases

- **A — FEED SHARING:** 20 accounts × S1 sobre NQ ⇒ una sola subscription `(NQ, NQH7)`; el fan-out por cuenta ocurre en StrategyEngine/fan-out D2-04 sobre la stream read-only. Account count ausente del engine. **PASS.**
- **B — EQUIVALENT DUAL FEED (CME A/B):** members A/B declaran clase POSITIONAL demostrada (mismo espacio de packet sequence + posición in-packet determinística); arbitraje first-wins por `(sequence, posición)`; muere A ⇒ B continúa; continuidad verificada sobre el espacio compartido ⇒ sin barrier, provenance cambia de member; una sola evaluación de Strategy por evento (salida única por stream_seq); las N entries de cada packet sobreviven como N eventos. **PASS.**
- **C — HETEROGENEOUS SOURCE BACKUP:** primary cae y sólo queda una autoridad distinta ⇒ switch explícito (§9): preserva contratos, valida servabilidad, epoch++, NOT_READY(SWITCHING), snapshot/boot por capabilities del nuevo, rebuild downstream, READY; sin blend jamás; sin auto-roll jamás. **PASS.**
- **D — SEQUENCE GAP (100,101,104):** seq 104 > 101+1 ⇒ GAP_DETECTED por primitiva ⇒ RECOVERING, readiness OFF; con identidad A/B, replay pide 102-103 y el overlap muere en dedup por identidad; en clase C, cursor no-solapado o snapshot según capability; RecoveryBarrier; B reconstruye lo afectado; continuidad demostrada para las clases soportadas + warmup ⇒ READY (epoch nueva); history no demostrable ⇒ RECOVERY_UNPROVABLE fail-visible. **PASS.**
- **E — EXCHANGE CLOSED:** calendar CLOSED ⇒ freshness NOT_EVALUABLE y liveness no penaliza silencio; sin failure por wall-clock; en `NextSessionTransition` OPEN la supervisión de frescura re-arranca y los primeros eventos refrescan estado. **PASS.**
- **F — ROLLOVER WITH LIVE OPERATION:** §14 paso a paso; (NQ, NQZ6) RETIRING vivo por ACQUIRE de Operation A; (NQ, NQH7) READY para Strategy; release al TERMINAL; cero remap. **PASS.**
- **G — LIVE EXPOSURE DURING OUTAGE:** readiness/staleness/barrera expuestos; `last_known_state` marcado; MM/safety aplican policy; el engine no emite ninguna acción monetaria. **PASS.**
- **H — SCALE:** +200 accounts ⇒ +0 market subscriptions (§7). **PASS.**
- **I — HETEROGENEOUS SWITCH WITH LIVE OPERATION (R1):** Operation A pinneada NQZ6; autoridad activa main; owner ordena switch main → backup. A conserva NQZ6: su demanda económica `(operation_id, NQ, NQZ6)` se re-sirve con la nueva autoridad; MM de A migra su market source después de barrier/recovery; el source viejo sólo persiste el cutover necesario y después A no tiene dependencia estructural al main. **PASS.**
- **J — SOURCE SWITCH ≠ ROLLOVER (R4):** main mapping NQ=NQZ6; backup mapping NQ=NQH7; owner ordena SÓLO switch. Resultado válido: NO se empieza a operar NQH7; se sirve NQZ6 desde backup si backup posee `ContractIdentifier(MARKET_DATA)` + capability para NQZ6; si no, el switch queda NOT_READY/BLOCKED (CONTRACT_NOT_SERVABLE) sin re-resolución silenciosa. NQZ6→NQH7 exige rollover explícito aparte. **PASS.**
- **K — IDENTICAL REAL TRADES (R2):** dos trades físicos reales con mismo timestamp, precio y qty, sin native identity (clase C). Echo NO elimina ninguno por content dedup: el recovery se ejecuta overlap-free (cursor/snapshot/full rebuild) de modo que cada trade físico se ingiere exactamente una vez; si el solape no puede distinguirse exactamente, el stream queda NOT_READY(RECOVERY_UNPROVABLE) fail-visible — nunca heurística de pérdida. **PASS.**
- **L — PACKET SEQUENCE (R3):** packet sequence=100 contiene 3 market entries (clase B). Los tres sobreviven como tres MarketEvents con identities `(100,·)` distintas y tres `stream_seq` propios; no hay dedup por packet sequence sola. **PASS.**

## 20. Risks / debts

- **Throughput/latencia del engine StateFun por tick (material):** hops adapter→Kafka→StateFun→Kafka→consumer sin benchmark. Mitigación: benchmark D6 obligatorio con tasa real del instrumento; fallback declarado (mismo contrato de estado/semántica servido por un stream worker in-process checkpointeado) — deuda condicional, no decisión hoy.
- **Egress canónico AT_LEAST_ONCE:** correctness downstream depende de respetar el dedup por `stream_seq`; es requisito de consumo en B/C y en cualquier front. Riesgo de implementación (no de diseño).
- **Sources clase C (sin identidad dedup-safe):** la corrección tras disruption depende de mecanismos overlap-free (cursor/snapshot/full rebuild); cualquier solape no distinguible ⇒ NOT_READY fail-visible. Mitigación: preferir sources con identidad declarada en la selección de vendors; la clase entera queda gated para consumo history-dependent tras disruption.
- **Switch bloqueado por servabilidad:** un backup sin `ContractIdentifier`/capabilities para un contract demandado (in-force o pinneado) rechaza el switch y deja al operador sin failover automático — fail-closed deliberado (jamás re-resolución silenciosa). Mitigación: validar identificadores de contratos pinneados/in-force al configurar un binding backup.
- **Replay bounds de vendor (p.ej. intraday 24h):** outages largos exceden bounds ⇒ fail-closed persistente + operador. Sin historia durable propia en V1 (decisión: no construir data lake ahora); revisar en D2-06B/C si el warmup la exige.
- **Automatic heterogeneous failover ausente:** un outage total del active authority requiere acción operacional (switch por config); mitigación: readiness alerts; automatización futura = config/ops, no cambio de contrato.
- **Capacidad de la ventana de demand sets:** crece con #Operations vivas por contract; acotada por TERMINAL→RELEASE; GC de streams UNSUBSCRIBED es rutina.
- **Timer density:** un timer de health por stream; con pocas decenas de streams V1 es trivial; revisar si el catálogo crece órdenes de magnitud.

## 21. Open questions — genuinely left for D2-06B/C

- **B:** contrato exacto de rebuild de bars/forming/indicadores ante RecoveryBarrier y switch de autoridad (qué se invalida, forming vs closed late-correction policy); depth/format del warmup handoff sobre `MarketHistorySource`; política de `reliable_ts=RECEIVE_ONLY` en barras.
- **C:** **elección y contrato del recorded replay stream** (D2-06A no lo congela: `echo.market-events.v1` es sólo el candidato de transporte LIVE y una fuente posible); mapping determinista stream↔replay (consumo del recording, clock injection, orden de control state vs events para replay fiel); retención/durability definitivos; formalización del `run_mode` REPLAY determinista; si el replay necesita re-derivar health/readiness o lo inyecta el run manifest.
- **Ambos:** conteo de particiones y throughput objetivo de `echo.market-events.v1`; señal exacta de "warmup consumido" que levanta la barrera (interface B↔engine).

## 22. Owner decisions

`OWNER DECISIONS REQUIRED: NONE`. Vendor de feed, thresholds de frescura/liveness, members, switches y rollovers son config técnica / acciones operacionales bajo las autoridades ya congeladas (B2 manager: health thresholds = technical D2; rollover owner-manual por D2-05 — este artefacto no lo cambia). Quedan ratificaciones técnicas ordinarias del manager: nombres físicos de topics/functions/campos, shape exacto de `SourceCapabilities`/`SourceEventPosition`/`StreamState`/`MarketDemand`, retention config del transporte, y la verificación del benchmark de throughput en D6.

## Handoff

```text
D2-06A STATUS:
READY_FOR_SUBMANAGER_REVIEW  (post-repair R1 — Manager Repair D2-06A-R1 aplicado)

ARTIFACT:
main/10-projects/Echo Futures/Echo Futures — D2-06A Market Feed Authority.md

AGENTS-OS SHA:
<pending-sync>

ECHO BASELINE:
372af59a7b83604781346613da01e3d510ea1360 (HEAD == origin/master, sin delta)

NEXT:
Return to D2-06 SUBMANAGER. Do not start D2-06B.
```
