---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo Futures]]"
  - "[[Echo Futures — D3 Astra Architecture Review]]"
  - "[[Echo Futures Architecture Candidate V1]]"
  - "[[Echo Futures — D2-06 Market Runtime]]"
  - "[[Echo Futures — D2-08 Strategy Runtime]]"
aliases:
  - Echo Futures D4-A1
  - Market Identity + Exact Replay Remediation
tags:
  - kind/doc
  - area/echo
  - echo-futures
  - architecture-correction
  - exact-replay
created: "2026-09-28"
updated: "2026-09-28"
---

# Echo Futures — D4-A1 Market Identity + Exact Replay Remediation

## 1. Scope y status

Este artifact es una corrección arquitectónica candidata para D4-A1. Resuelve conjuntamente los findings aceptados `D3-01 — Market identity / rollback` y `D3-05 — EXACT_REPLAY + pull MarketContext`, sin reabrir D1/D2 completos, sin modificar Echo físico y sin emitir ningún gate de D4.

Autoridades principales: [[Echo Futures]], [[Echo Futures — D3 Astra Architecture Review]], [[Echo Futures Architecture Candidate V1]], [[Echo Futures — D2-06 Market Runtime]] y [[Echo Futures — D2-08 Strategy Runtime]]. Evidencia puntual adicional: D2-06A/D2-06B/D2-06C y el patrón `kache` del baseline `xKoRx/echo@372af59a7b83604781346613da01e3d510ea1360`.

La corrección mantiene los boundaries D2 que no fueron refutados: `stream_id = (instrument_id, contract_id)`, source/binding separado de la stream lógica, `authority_epoch` como serving/recovery provenance, `owner_input_seq` per-island, ausencia de global ordering, estado de mercado compartido, Strategy evaluada antes del fan-out, MM mutable dentro de `echo/operation`, misma lógica de dominio LIVE / EXACT_REPLAY / BACKTEST y PostgreSQL/caches fuera de la recovery authority.

## 2. Conclusión ejecutiva

La causa común de D3-01 y D3-05 es que D2 hizo durable una parte del orden observado, pero dejó dos observaciones relevantes dependientes de scheduling no preservado: el merge previo a la asignación de `stream_seq` en `echo/market_stream`, y la versión concreta de un read model pull leída durante una decisión.

La corrección candidata introduce dos seams mínimos y complementarios, sin event sourcing global ni snapshots gigantes:

1. **Canonicalization Input Order:** toda entrada capaz de cambiar la canonicalización de un MarketEvent se serializa durablemente por `stream_id` antes de ejecutar `echo/market_stream`. `stream_seq` puede seguir siendo un ordinal monotónico por stream, pero pasa a ser una función determinística de un input durable y replayable; deja de depender de un merge recuperable sólo por scheduling.
2. **Captured context reads:** cada evaluación market-dependent usa un `MarketContext` estable durante esa decisión. LIVE registra sólo los valores/versiones realmente leídos en `context_reads[]`; EXACT_REPLAY consume esas mismas lecturas y nunca vuelve a consultar un cache `latest` para reconstruir una lectura histórica.

El resultado separa explícitamente cuatro conceptos que D2 no puede volver a fusionar: **source identity**, **canonical event identity**, **stream ordering** y **observed context version**.

No se requiere cambiar `echo.market-events.v1` a EXACTLY_ONCE como solución primaria. El egress canónico puede continuar `AT_LEAST_ONCE` si el input de canonicalización y la función de canonicalización cumplen las invariants definidas aquí. EXACTLY_ONCE queda como fallback técnico si una implementación no puede certificar esas invariants sin introducir ambigüedad.

## 3. Reconstrucción del contrato roto

### 3.1 D3-01 — qué estaba roto

D2-06 define `stream_seq` como orden/idempotencia canónica por logical stream, cruzando `authority_epoch`, y `echo.market-events.v1` como egress `AT_LEAST_ONCE`. D2-06A asigna ese `stream_seq` dentro de `echo/market_stream` desde estado checkpointeado. Los candidates físicos estaban keyeados por `stream_id|source_id`, por lo que dos inputs destinados a la misma logical stream podían llegar desde espacios de orden distintos antes de la serialización StateFun.

D3 demostró el contraejemplo suficiente: checkpoint en 100; intento A publica `X/101`; falla antes del checkpoint; X sobrevive en Kafka; el estado vuelve a 100; tras recovery el merge admite Y antes que X y publica `Y/101`, `X/102`. El downstream guard `seq <= last_applied_stream_seq` puede descartar Y legítimo y aplicar X dos veces.

El defecto no es que `AT_LEAST_ONCE` sea inválido. El defecto es usar un ordinal rollback-able como si demostrara una función estable `stream_seq -> event content` cuando el orden de inputs que construye esa función no era durable.

### 3.2 D3-05 — qué estaba roto

D2-06C journaliza el merge observado por una isla y `source_ref` del trigger. D2-06B/D2-08 permiten que Strategy y MM lean `current`, bars, readiness/session u otros timeframes mediante read models compartidos estilo kache.

El journal demuestra qué input despertó una evaluación, pero no qué versión de un read model eventual estaba visible en el proceso consumidor en el instante exacto del pull. El patrón físico del baseline confirma que `kache` mantiene latest-value in-memory mediante un consumer Kafka en background; por lo tanto la propagación hacia el cache no está linealizada por `owner_input_seq` de Strategy/MM.

El contraejemplo D3-05 es suficiente: NQ cierra y dispara Strategy; ES analytics ya produjo X y X′; en LIVE el cache de Strategy todavía expone X; otro schedule con exactamente los mismos producer journals puede exponer X′. El mismo trigger y el mismo `source_ref` no seleccionan la observación original.

## 4. Modelo de identidad y ordering corregido

### 4.1 Conceptos normativos

| Concepto | Scope | Función | No debe usarse como |
|---|---|---|---|
| `stream_id` | logical stream | `(instrument_id, contract_id)`, estable ante source switch | source identity, event identity |
| `source_event_identity?` | source identity space | identidad dedup-safe del evento físico cuando la capability la demuestra | orden canónico universal |
| `canonical_event_id` | logical stream | identidad estable del MarketEvent canónico aceptado | orden |
| `stream_seq` | logical stream | ordinal monotónico de MarketEvents canónicos aceptados | source identity, content hash, recovery attempt |
| `authority_epoch` | logical stream | provenance/readiness de serving/recovery | identidad de evento, orden global |
| `owner_input_seq` | owner/key | orden de admisión observado por una isla | market-event identity |
| `runtime_ts` | owner/key | tiempo lógico monotónico usado por DomainClock | venue/event time |

`event_ts` conserva exclusivamente semántica técnica de mercado. `receive_ts` conserva liveness/telemetría. Ninguno participa como correctness identity.

### 4.2 Source identity

Se conservan las clases D2:

- **A — EVENT:** el source entrega identidad nativa estable. `source_event_identity = (identity_space_id, native_event_id)`.
- **B — POSITIONAL:** la identidad es posición nativa determinística. `source_event_identity = (identity_space_id, packet_or_message_sequence, entry_index)`.
- **C — NONE:** no existe identidad dedup-safe del evento físico. Está prohibido fabricar una con hash de contenido, timestamp+price+qty o equivalente.

`identity_space_id` es parte del capability contract. Members equivalentes sólo comparten `identity_space_id` cuando la evidencia demuestra que comparten realmente el mismo espacio de identidad. Un source switch heterogéneo puede cambiar `identity_space_id`; `authority_epoch` también cambia por la semántica D2, pero el epoch no sustituye al identity space.

### 4.3 Canonicalization Input Order

Se congela una única regla nueva para `echo/market_stream`:

> Todo input capaz de cambiar si un candidate se convierte o no en MarketEvent, qué `authority_epoch` recibe o qué payload canónico produce debe entrar por un orden durable único por `stream_id` antes de ejecutar la función de canonicalización.

El logical contract es `MarketStreamInput`. Debe cubrir como mínimo:

- `FeedCandidate`;
- source/authority transition que cambie qué member/source puede servir la stream;
- recovery/barrier transition que cambie epoch o admisibilidad;
- capability/config transition que cambie dedup/arbitraje/canonicalización.

Inputs que sólo cambian telemetry o freshness y no pueden cambiar aceptación, epoch ni contenido del MarketEvent no necesitan pasar por esta frontera.

La implementación V1 más KISS es evolucionar la capa Kafka que ya existe antes de `echo/market_stream` para que el routing material sea **key = `stream_id`**, no `stream_id|source_id`, y que los controls materialmente relevantes entren por la misma secuencia per-stream. Esto no crea orden global: sólo convierte en durable el orden que una única StateFun key igualmente debía serializar.

El Kafka ingress puede exponer una `ingress_record_ref = (log_identity, partition, offset)` al envelope entregado al runtime. Ese ref es infraestructura/provenance y no se convierte en identidad de negocio. Su utilidad es demostrar que el mismo input durable vuelve a entrar en el mismo orden después de restore.

### 4.4 Canonical event identity

`canonical_event_id` se deriva determinísticamente de evidencia estable anterior a `stream_seq`:

- clase A/B: `canonical_event_id = DeterministicID(stream_id, source_event_identity)`;
- clase C: `canonical_event_id = DeterministicIngressID(stream_id, ingress_record_ref, expansion_index)`.

Para clase C este ID significa **identidad de la observación canónica ingresada**, no prueba de identidad del evento físico. Dos ingress records distintos que pudieran corresponder al mismo evento físico no se fusionan por heurística. La recovery policy de clase C sigue siendo la de D2: cursor no solapado, snapshot/full rebuild autoritativo o fail-visible.

`content_digest` puede acompañar al evento para integridad y conflict detection, pero está explícitamente prohibido usarlo como dedup identity.

### 4.5 Semántica de `stream_seq`

`stream_seq` se conserva porque es útil y barato, pero cambia su prueba de correctness:

- se asigna sólo a MarketEvents aceptados;
- es monotónico por `stream_id`;
- cruza `authority_epoch`;
- un duplicate candidate deduped antes de canonicalización no consume un nuevo `stream_seq`;
- su valor es una función determinística del prefijo ordenado de `MarketStreamInput` y del estado restaurable de la función;
- el mismo `stream_seq` DEBE mapear al mismo `canonical_event_id` y al mismo contenido canónico en todos los retries/recoveries del run.

Por lo tanto `stream_seq` es **ordering**, no identidad. La identidad es `canonical_event_id`. El downstream puede usar `stream_seq` como fast-path de idempotencia sólo porque ahora existe una prueba de estabilidad `stream_seq -> canonical_event_id/content`.

### 4.6 Guard downstream corregido

El viejo contrato “`seq <= last_applied_stream_seq` ⇒ NO-OP” es insuficiente como especificación aislada. V2 debe congelar:

- un redelivery del mismo `(stream_id, stream_seq, canonical_event_id, digest)` es NO-OP antes de mutar bars/current/readiness o disparar evaluación;
- un mismo `stream_seq` con `canonical_event_id` o digest distinto es `MARKET_IDENTITY_CONFLICT`, fail-visible; jamás se descarta silenciosamente;
- un mismo `canonical_event_id` con otro `stream_seq` dentro del mismo canonical run es también conflict/error de canonicalización para clases A/B; no es una segunda observación legítima;
- clase C no recibe semantic dedup entre dos ingress records diferentes; si el source necesita overlap recovery y no puede probar identidad, el runtime no declara exact recovery.

La implementación del fingerprint guard puede ser un high-watermark + ventana acotada consistente con el recovery/redelivery horizon certificado; no se congela aquí una estructura de datos específica.

## 5. Por qué D3-01 queda corregido sin EXACTLY_ONCE canónico

La función que D3 necesitaba pero D2 no demostraba pasa a ser:

```text
same durable MarketStreamInput prefix
+ same pinned/config transitions in that prefix
+ same canonicalization code
⇒ same accepted canonical_event_id sequence
⇒ same stream_seq -> canonical_event_id/content mapping
```

Un egress `AT_LEAST_ONCE` puede repetir records, pero ya no puede hacer que el mismo ordinal represente X en un intento y Y en otro, salvo violación explícita del contrato detectable como conflict.

Esto mantiene la razón D2 para no encadenar la visibilidad de cada tick al commit transaccional de checkpoint. No introduce un sequencer global, DB en hot path, producer-side consensus ni event sourcing global.

### 5.1 Alternativas evaluadas para D3-01

| Alternativa | Correctness | Costo / problema | Decisión candidata |
|---|---|---|---|
| `echo.market-events.v1` EXACTLY_ONCE | cierra la ventana de publish-before-checkpoint | visibilidad acoplada al checkpoint; contradice la intención de latencia D2 salvo nueva certificación | **Fallback**, no primaria |
| namespacear `stream_seq` por recovery attempt | evita colisión numérica | no deduplica el mismo evento ni reproduce el mismo orden; convierte retry en evento nuevo | **Rechazada** |
| usar append position del egress como única autoridad | identidad física durable del record | puede dejar estado del producer restaurado en orden distinto al ya observado externamente | **Rechazada como primaria** |
| durable per-stream canonicalization input order | mismo orden reingresa después de rollback; mantiene ALO de salida | exige re-key/envelope de ingress y controls materiales | **Seleccionada** |

Si D5 demuestra que un input material no puede entrar por esta frontera sin romper el hot path, el fallback correcto es EXACTLY_ONCE para el tramo afectado, no volver a una identidad basada en scheduling.

## 6. MarketContext corregido: decision-scoped, memoized, evidence-capturing

### 6.1 Regla normativa

Strategy/MM no pueden usar un `MarketContext` que signifique “lee lo último que casualmente tenga el cache” sin preservar qué fue leído.

Cada evaluación/decisión market-dependent usa un `MarketContext` decision-scoped asociado al input owner ya serializado. Las lecturas capturadas quedan asociadas a:

```text
(run_id, owner_key, owner_input_seq, local_decision_ordinal)
```

No es una nueva entidad de negocio ni reemplaza `strategy_eval_seq`/Operation. Es una coordenada determinística del journal.

Durante LIVE, el `MarketContext` del scope:

1. lee del shared read model existente;
2. captura exactamente la versión/valor retornado;
3. memoiza esa lectura dentro del scope;
4. una segunda lectura de la misma logical key dentro de la misma decisión devuelve la misma observación;
5. registra sólo lecturas decision-critical realmente efectuadas.

Durante EXACT_REPLAY, el mismo interface de dominio:

1. no consulta kache/latest para lecturas históricas;
2. resuelve cada pull desde `context_reads[]` grabado;
3. verifica key, ordinal, version/digest y tipo;
4. falla cerrado ante lectura faltante, extra o incompatible.

BACKTEST usa el mismo interface, pero lo alimenta el estado sintético determinístico del runner; no necesita un read-set previo porque es un run nuevo, no la reproducción de un live pasado.

### 6.2 Evidencia mínima de una lectura

`context_reads[]` es parte del journal existente, no una entidad de dominio ni un nuevo state owner. Cada entrada necesita sólo:

```text
  read_ordinal
  logical_read_key
  observed_version
  value_ref? | inline_value?
  content_digest
```

`logical_read_key` distingue al menos el tipo de dato y su scope: current quote/trade, bar/bar-range, readiness/quality o session/calendar observation. Para bars incluye `stream_id + timeframe + BarId/range`; para current-state incluye `stream_id + contract_id + field class`; para session/readiness incluye su key natural.

Se prefiere **reference** cuando la versión exacta es immutable y durable dentro del recording horizon. Se usa **inline_value mínimo** cuando el read model sólo conserva latest y la versión histórica podría desaparecer. No se hace snapshot de toda la stream, toda la ring ni todo MarketContext.

### 6.3 Version identities mínimas

V2 debe exigir version identity explícita en shared read models que pueden ser decision-critical:

- **current quote/trade:** ref al último `canonical_event_id + stream_seq + authority_epoch` que compone ese valor;
- **bar snapshot:** `BarId + bar_revision + source_upto_stream_seq` o equivalente estable; la versión observada X es immutable dentro del context_reads[] aunque el read model latest avance a X′;
- **readiness/quality:** `stream_id + authority_epoch + readiness_version/source_ref`;
- **session/window:** calendar snapshot/revision + transition ref cuando la observación no sea ya parte del owner state por una delivery ordenada.

El naming exacto puede refinarse en Technical SPEC, pero una “versión” no puede ser sólo `updated_at` wall-clock.

### 6.4 Qué NO se duplica

No se graban de nuevo:

- `mm_state`, Operation, Orders, Fills;
- finite state/indicators propios de Strategy;
- config que ya esté pinned en initial manifest o representada por `ConfigTransition`;
- todo el ring de barras si la decisión leyó una sola barra;
- read models completos por trigger;
- vendor packets cuando el canonical content ya existe.

La regla de materialidad es simple:

> Si el valor se obtiene por pull desde un shared read model y puede cambiar la decisión, el replay debe poder identificar/reconstruir exactamente el valor observado. Si ya es derivable inequívocamente del owner state y sus ordered inputs, no se duplica.

## 7. Trigger/context relation

### 7.1 BAR_CLOSED

Un `BAR_CLOSED` que dispara Strategy debe referenciar la **versión exacta del bar cerrado usada como trigger**, no “el BarId y después lee latest”.

La delivery lleva una referencia/version exacta e inmutable de X. Una corrección late X′ puede actualizar la proyección `echo.market-bars.v1`, pero no muta X, no reevalúa retroactivamente Strategy y no reemplaza el trigger evidence ya journalado.

### 7.2 MARKET_EVENT

El trigger referencia `canonical_event_id + stream_seq`. El canonical content está dentro del recording horizon; no se duplica el tick en `context_reads[]`.

### 7.3 Timer/session/config/recovery

Siguen el orden `owner_input_seq` y el inline/reference contract D2-06. Si el owner ya aplicó una transición como input antes de la evaluación, ese state es suficiente. Si la decisión además hace pull a un read model de sesión/readiness independiente, la versión realmente leída se captura como ContextRead.

### 7.4 Cross-stream pull

La delivery NQ que dispara la evaluación sólo ordena NQ respecto de otros inputs entregados a Strategy. Una lectura pull de ES es otra observación. Su `ContextRead` selecciona explícitamente qué ES bar/current version vio la evaluación, aunque ES analytics ya haya producido una versión posterior.

No se crea atomic snapshot multi-stream. El live puede observar NQ@A y ES@B en una combinación que existió por propagación real. EXACT_REPLAY reproduce esa combinación concreta, que es exactamente la semántica observable original.

## 8. Journal / recording contract corregido

El recording V2 queda conceptualmente:

```text
Run Recording =
  Initial RunManifest
  + ReplayAnchor
  + DeterministicInputLog
  + canonical content
  + context_reads[] evidence
```

`context_reads[]` extiende el mismo `echo.market-run-journal.v1`; no requiere topic, servicio, aggregate ni lifecycle nuevo.

Para cada decisión/evaluación market-dependent el journal conserva:

- owner coordinate (`owner_key`, `owner_input_seq`, local ordinal/eval seq);
- trigger/input ref;
- ordered `context_reads[]` realmente consumidos;
- decision/output digest ya existente o equivalente de integridad.

Las lecturas capturadas deben tener la misma frontera de commit que el estado/output que certifican. Una implementación no puede exponer una Signal replay-authoritative si sus `context_reads[]` correspondientes pueden faltar después de un crash exitosamente visible. La certificación física de esta atomicidad/commit coupling queda como obligación de implementación/QA; no se asume por narrativa.

La garantía EXACT_REPLAY corregida pasa a ser:

```text
same initial manifest
+ same ReplayAnchor
+ same deterministic owner inputs/runtime_ts
+ same canonical content
+ same context_reads[] evidence
+ same code
⇒ same market-dependent decisions
```

La ecuación D2 sin las lecturas concretas de contexto queda superseded para cualquier decisión que haga pull de shared read models.

## 9. Failure walkthroughs

### 9.1 External publish before checkpoint — finding D3-01

Estado estable: checkpoint de `echo/market_stream` conserva `stream_seq=100` y el durable `MarketStreamInput` está consumido hasta posición C200.

1. Candidate X entra en la misma secuencia durable per-stream como C201.
2. Candidate Y entra después como C202.
3. Intento A procesa C201, acepta X, deriva `canonical_event_id=XID`, asigna `stream_seq=101` y ALO publica `X/101`.
4. El job falla antes de completar el siguiente checkpoint. `X/101` queda externamente visible; state vuelve a seq 100 y cursor C200.
5. Recovery vuelve a consumir **C201 X antes de C202 Y**, porque el orden que construye la canonicalización es durable.
6. Se regenera X con el mismo `canonical_event_id`, mismo contenido y `stream_seq=101`; ALO puede redeliverarlo.
7. Luego C202 produce `Y/102`.
8. Downstream que ya vio el primer X/101 absorbe el segundo X/101 como duplicate exacto y aplica Y/102 una sola vez.

No existe el interleaving `Y/101, X/102` porque la diferencia de scheduling previa al owner dejó de ser una entrada válida del contrato. Si aparece el mismo seq con otro ID/digest, el runtime falla visible como `MARKET_IDENTITY_CONFLICT`.

### 9.2 Transport redelivery y semantic duplicate

**Mismo canonical record redelivered:** igual `stream_seq + canonical_event_id + digest`; guard => NO-OP antes de bars/current/evaluation.

**Mismo source event llega por member equivalente A y B:** ambos candidates llevan el mismo `source_event_identity`; el durable order decide cuál candidate se procesa primero; la canonicalización first-wins produce un solo `canonical_event_id/stream_seq`; el segundo candidate es dedup pre-canonical y no consume seq.

**Clase C:** dos records distintos no se colapsan por contenido. Si recovery del source puede solapar el mismo evento físico y no existe identidad, debe usar la ruta D2 de cursor no solapado/snapshot/full rebuild o quedar NOT_READY/fail-visible.

### 9.3 Crash durante evaluación Strategy después de leer contexto

1. NQ trigger entra como `owner_input_seq=450`.
2. LIVE MarketContext lee ES bar X y agrega `{ES, X/v17}` a `context_reads[]` de esa decisión.
3. Strategy calcula Signal S.
4. El job falla antes de que checkpoint/recording/output queden committed.
5. Al retry, el mismo input 450 puede encontrar ES X′/v18 y producir S′.
6. Sólo el intento cuyo state + observation evidence + output alcanzan la frontera de commit se convierte en verdad del run.
7. EXACT_REPLAY reproduce el intento committed, no una evaluación abortada que nunca quedó autoritativamente visible.

Esto evita exigir que el sistema congele caches para intentar reproducir scheduling de una ejecución que fue descartada.

### 9.4 Replay de decisión con MarketContext compartido

Run live: BAR_CLOSED NQ Xnq dispara Strategy. La decisión además lee current BBO NQ y 5m bar NQ desde shared read models.

`context_reads[]` registra únicamente el BBO `canonical_event_id/stream_seq` leído y la versión exacta del bar 5m. Si durante el run el latest BBO/bar avanza antes de que termine replay, eso es irrelevante.

EXACT_REPLAY inyecta el mismo BAR_CLOSED trigger y el ReplayMarketContext entrega exactamente esas dos observaciones. La Strategy recibe el mismo trigger, mismo local state, mismo runtime_ts y mismo read-set, por lo que la decisión es reproducible sin snapshot global.

### 9.5 Cross-stream NQ + ES — finding D3-05

1. ES analytics produce bar X v17.
2. ES analytics procesa una late correction y produce X′ v18.
3. El producer/read model autoritativo ya conoce v18, pero el cache visible a Strategy todavía está en v17.
4. NQ BAR_CLOSED dispara la evaluación.
5. Strategy pide `bars(ES, 1m).latest` y LIVE recibe X v17.
6. Se registra `ContextRead{ES, BarId, version=v17, value/digest=X}`.
7. EXACT_REPLAY puede reconstruir ES hasta v18 antes de ejecutar NQ; **no usa ese latest** para el pull histórico. Entrega X v17 desde la evidencia grabada y opcionalmente verifica que la versión sea coherente con el producer history.
8. La Signal resultante coincide con el run live.

El sistema no intenta fabricar un global snapshot NQ+ES. Reproduce la mezcla realmente observada.

### 9.6 MM con notificación ligera + pull

La notificación D2-08 puede seguir siendo ligera y transportar `stream_id + trigger_class + trigger_ref`. Al entrar a `echo/operation`, la decisión MM abre su MarketContext decision scope. Si el plugin consulta BBO/bar/readiness, esas lecturas se capturan exactamente igual que en Strategy.

MM state sigue viviendo exclusivamente en Operation; no se crea un MM read model global ni se duplica feed por cuenta. El costo nuevo es proporcional a las **lecturas realmente hechas por decisiones MM que ya eran account-specific**.

## 10. Invariants candidatas

**I-A1 — Stable canonicalization input:** toda entrada que pueda cambiar acceptance/epoch/payload de un MarketEvent comparte un durable total order **por stream**, no global.

**I-A2 — Canonical function stability:** mismo prefijo ordenado de `MarketStreamInput` + misma config/código ⇒ misma secuencia de `canonical_event_id` aceptados.

**I-A3 — Sequence stability:** mismo prefijo aceptado ⇒ mismo mapping `stream_seq -> canonical_event_id/content`.

**I-A4 — Identity/order separation:** `canonical_event_id` identifica; `stream_seq` ordena; `authority_epoch` da provenance; ninguno sustituye a otro.

**I-A5 — No fake source identity:** clase C nunca usa content hash/tuple como dedup-safe identity.

**I-A6 — ALO conflict visibility:** redelivery exacto es NO-OP; mismo seq con contenido/ID distinto es error visible, nunca drop silencioso.

**I-A7 — No global ordering:** todas las garantías son per-stream o per-owner; no existe `run_order` global ni sequencer central.

**I-A8 — Decision-scoped context:** una decisión ve un MarketContext estable; repeated read de la misma logical key retorna la misma versión.

**I-A9 — Sparse read-set:** sólo se registra shared state realmente leído y capaz de cambiar la decisión.

**I-A10 — Replay no latest:** EXACT_REPLAY jamás usa un shared `latest` cache para satisfacer una lectura histórica decision-critical.

**I-A11 — Trigger immutability:** el trigger exacto de la decisión queda identificado/versionado; late correction no reescribe la versión usada ni causa retrospective Signal.

**I-A12 — Cross-stream honesty:** una decisión puede observar versiones no simultáneas de distintos streams; replay reproduce la combinación observada, no un snapshot ficticio.

**I-A13 — Fail closed on missing evidence:** read faltante, read extra incompatible, version/digest mismatch o corpus ausente ⇒ replay fail-visible; nunca fallback silencioso a latest.

**I-A14 — Cache is never replay authority:** `echo.market-bars.v1`, stream-state kache y caches derivados continúan siendo read models hot, no recovery/replay authority.

**I-A15 — Same domain logic:** Strategy/MM reciben el mismo MarketContext interface lógico en LIVE, EXACT_REPLAY y BACKTEST; cambia el provider de observación, no la lógica de dominio.

## 11. SPEC deltas requeridos

### 11.1 Market Runtime / D2-06 supersede

V2 debe reemplazar el supuesto de que la serialización StateFun posterior a candidates multi-source basta para estabilizar `stream_seq`. Debe definir `MarketStreamInput` durable per-stream y enumerar qué controls materialmente afectan canonicalización.

El key material de la frontera previa a `echo/market_stream` pasa a `stream_id`. `source_id` permanece dentro del envelope/provenance, no en el key que fragmenta el orden de una logical stream.

`MarketEvent` agrega/explicita `canonical_event_id`, `source_event_identity?`, `identity_space_id?` e ingress provenance suficiente para auditar el mapping. `stream_seq` permanece separado.

### 11.2 Feed adapters / ingress

Adapters producen candidates con source identity según capability. No asignan `stream_seq`.

El ingress runtime debe preservar la identidad/posición durable del record antes de `echo/market_stream`. En StateFun 3.2 el Kafka ingress deserializer recibe el `ConsumerRecord`, por lo que topic/partition/offset están disponibles para construir provenance/observation identity sin servicio adicional.

Controls que afecten canonicalización no pueden saltarse esta frontera mediante una cache eventual cuyo timing cambie acceptance. Config telemetry-only/readiness-only puede seguir fuera.

### 11.3 Canonical market egress

`echo.market-events.v1` puede continuar `AT_LEAST_ONCE`.

El contrato ya no dice “ALO es seguro porque `stream_seq` está checkpointeado”. Dice “ALO es seguro porque retries consumen el mismo canonicalization input order y regeneran el mismo seq→identity/content mapping; duplicates exactos se absorben”.

Si esa prueba no puede cumplirse físicamente, el tramo afectado debe usar el fallback transaccional o quedar no-certificado.

### 11.4 Market analytics / bars

Toda versión de bar que pueda ser leída por una decisión necesita una version identity estable. `echo.market-bars.v1` puede seguir compacted/latest; no se convierte en history store.

Late correction X→X′ incrementa/cambia la versión observada. context_reads[] que capturó X conserva X/ref y no se reescribe.

### 11.5 Strategy Runtime / D2-08 supersede

Pure Strategy deja de tener acceso conceptual a caches arbitrarios. Recibe un MarketContext decision-scoped.

BAR_CLOSED trigger porta/refiere la versión exacta del bar trigger.

Cross-stream/timeframe/current-state pulls pasan por el context provider instrumentado. LIVE captura; EXACT_REPLAY sirve desde evidencia; BACKTEST sirve desde estado sintético.

La determinación de `signal_id`, `strategy_eval_seq` y fan-out permanece D2.

### 11.6 MoneyManagement

El plugin MM sigue dentro de `echo/operation`; `mm_state` no cambia de owner.

La notificación ligera de mercado sigue permitida, pero “trigger ref + leer latest y asumir reproducibilidad” queda superseded. Toda decisión MM para la cual se reclame reproducibilidad market-dependent usa el mismo MarketContext decision scope.

Este artifact no amplía EXACT_REPLAY hacia physical execution. Sólo cierra la evidencia del contexto de mercado observado por la lógica MM.

### 11.7 DeterministicInputLog / replay journal

El journal debe poder expresar:

- `trigger_ref`;
- `context_reads[]` asociado a owner input/eval;
- version/ref o inline minimal value;
- integrity digest.

No necesita guardar `BAR_CLOSED` como segunda autoridad global si el trigger snapshot/ref es parte de la evidencia de decisión. El principio de no dual authority se conserva: bars siguen derivados; la copia dentro de una decisión es evidencia de **lo observado**, no autoridad del estado de mercado futuro.

### 11.8 ReplayDriver

EXACT_REPLAY reconstruye canonical streams/owner order como D2 y además instala un context provider de replay.

Ante una lectura requerida no encontrada o evidencia no consumida conforme al contract, falla visible. No consulta network, DB ni cache live para “completar” evidencia.

BACKTEST no consume `context_reads[]` de otro run.

## 12. Acceptance cases D4-A1

| ID | Caso | Debe demostrar |
|---|---|---|
| A1-01 | publish X/101 antes de checkpoint, crash, restore | retry produce X/101 idéntico antes de Y/102; nunca Y/101 |
| A1-02 | mismo canonical record ALO redelivered | bars/current/Strategy se mutan una vez |
| A1-03 | mismo seq con ID/digest distinto inyectado | fail-visible `MARKET_IDENTITY_CONFLICT`; nunca silent drop |
| A1-04 | equivalent members A/B entregan mismo source identity | exactamente un canonical event y un seq |
| A1-05 | dos eventos físicos distintos X/Y concurren desde members | el durable per-stream input order fija un único orden recuperable |
| A1-06 | clase C con recovery solapado sin identity | no content-dedup; recovery se bloquea/rebuild/fail-visible según capability |
| A1-07 | source switch heterogéneo | `stream_id` estable, `authority_epoch` cambia, canonicalization controls ordenados; seq cruza epoch |
| A1-08 | BAR_CLOSED X seguido de late correction X′ | decisión disparada por X conserva X; X′ no provoca retroactive Signal |
| A1-09 | NQ trigger + pull ES donde producer tiene X′ y cache live muestra X | read-set registra X; replay usa X aunque reconstruya X′ |
| A1-10 | una decisión lee dos veces la misma logical key mientras cache avanza | ambas lecturas dentro del scope devuelven la misma versión |
| A1-11 | decisión lee BBO + 1m bar + session | sólo esas observaciones aparecen en read-set; no snapshot global |
| A1-12 | replay sin un ContextRead requerido | fail-visible; no fallback a latest |
| A1-13 | replay contiene ContextRead extra/orden incompatible con la ejecución | mismatch visible; no aceptación silenciosa |
| A1-14 | crash después de leer contexto pero antes de commit | observación/output abortados no se vuelven authority; retry committed define el run |
| A1-15 | crash después del commit | decision evidence y output permanecen suficientes para exact replay |
| A1-16 | BACKTEST de la misma Strategy | usa mismo código/MarketContext contract con provider sintético; no depende del journal live |
| A1-17 | 200 cuentas, Strategy bars-only | read-set Strategy se captura una vez antes del fan-out; no × Account |
| A1-18 | MM BBO opt-in en N Operations | sólo decisiones MM opt-in capturan sus lecturas; no duplica feed/bar builders |

## 13. Failure semantics y observabilidad obligatoria

Los siguientes estados deben ser visibles y testeables, aunque el naming final pueda ajustarse en Technical SPEC:

- `MARKET_IDENTITY_CONFLICT`: mismo `(stream_id, stream_seq)` con ID/digest distinto;
- `MARKET_SOURCE_IDENTITY_INVALID`: source declaró A/B pero entregó identidad inválida/reutilizada fuera de su capability;
- `MARKET_CANONICALIZATION_ORDER_INVALID`: un input material llegó por fuera de la frontera durable requerida;
- `REPLAY_CONTEXT_READ_MISSING`: la lógica solicitó una lectura no grabada;
- `REPLAY_CONTEXT_READ_MISMATCH`: key/version/digest/orden no corresponde;
- `REPLAY_CONTEXT_READ_UNUSED`: evidencia grabada no consumida donde el contract exige igualdad estricta;
- `REPLAY_SOURCE_MISSING` / `REPLAY_LOG_CORRUPT`: se conservan desde D2.

Métricas/telemetría mínimas para implementación: transport redeliveries absorbidos, source duplicates absorbidos, identity conflicts, clase C recovery blocks, context_reads[] bytes/read count por decisión, replay observation mismatches y tamaño de read-set. D4 no fija budgets numéricos sin medición.

## 14. Impacto en performance y escala

La corrección D3-01 no agrega un hop conceptual: reemplaza el merge no durable pre-owner por un Kafka order per-stream en la frontera que ya existe. La partición no es global y el target de 100–200 accounts sigue irrelevante para ingestion/market_stream.

La corrección D3-05 agrega bytes proporcionales al número de lecturas decision-critical, no al tamaño del mercado ni al número total de read models. Strategy registra una vez por evaluación antes de fan-out. MM paga account-specific sólo cuando ya ejecuta una decisión y efectivamente consulta mercado.

No se exige persistir cada versión de `echo.market-bars.v1` globalmente. Las versiones antiguas necesarias para reproducir una decisión viven como refs o valores mínimos dentro del recording del run.

## 15. Boundaries que permanecen congelados

- No global sequencer ni total order global.
- `stream_id = (instrument_id, contract_id)`.
- Source switch no implica rollover.
- Operation pinnea Contract, no source.
- `authority_epoch` conserva su semántica de serving/recovery.
- `owner_input_seq` conserva orden per-island para Strategy/MM/timers/transitions.
- Market state es shared/read-only; Account no entra en keys de feed/bars.
- Strategy evalúa una vez antes de fan-out.
- MM mutable state sigue en Operation.
- BAR/analytics continúan derivados, no nueva authority.
- PostgreSQL y compacted caches no son recovery authority.
- EXACT_REPLAY sigue siendo reproducción de un run live; BACKTEST sigue siendo run nuevo sobre historia.
- Physical execution permanece fuera del market EXACT_REPLAY V1.
- No event sourcing global, snapshot global, distributed transaction framework ni nueva flota de microservicios.

## 16. Decisiones técnicas tomadas vs decisiones Owner

### 16.1 Técnicas cerradas por este candidate

- Preservar ALO para canonical market egress como primary path.
- Introducir durable per-stream ordering antes de canonicalization.
- Re-key material del ingress por logical `stream_id`.
- Separar `canonical_event_id` de `stream_seq`.
- Mantener capability-driven identity A/B/C y prohibición de fake content identity.
- Mantener `MarketContext` decision-scoped.
- Registrar en el journal existente sólo `context_reads[]` realmente usados, refs-first + inline mínimo cuando la versión histórica no es direccionable.
- Hacer fail-closed el replay cuando falte evidencia.
- Mantener BACKTEST fuera del recording live.

### 16.2 No hay decisión Owner nueva requerida

La corrección no cambia una regla de trading, una política monetaria, un rollover product decision ni el scope de mercado. Define correctness semantics para preservar las garantías ya aceptadas: canonical event identity estable, ordering recuperable y EXACT_REPLAY de decisiones market-dependent.

EXACTLY_ONCE canónico permanece fallback técnico si la implementación no logra certificar la frontera durable per-stream; activar ese fallback por limitación física no requiere redefinir producto, pero cualquier impacto de latencia que haga inviable el requisito de Futures debería volver al Primary Manager como evidence blocker, no resolverse silenciosamente en D5.

## 17. Trazabilidad finding → correction → proof

| Finding | Defecto demostrado | Evidence principal | Candidate correction | Invariants | Acceptance |
|---|---|---|---|---|---|
| D3-01 | rollback puede reasignar mismo seq a otro contenido porque el merge pre-seq no era durable | D3 §3 D3-01; D2-06 §6/§18/§22; D2-06A §17 | `MarketStreamInput` durable per-stream + canonical_event_id separado + conflict guard | I-A1..I-A7 | A1-01..A1-07 |
| D3-05 | source_ref del trigger no identifica versiones pull observadas | D3 §3 D3-05; D2-06B §§14/22/23/25; D2-06C §10; D2-08 §12 | decision-scoped MarketContext + sparse context_reads[] read-set | I-A8..I-A15 | A1-08..A1-18 |

## 18. Evidence map

### Authorities

- `main/10-projects/Echo Futures/Echo Futures.md` — constraints de producto, same-domain-logic, scale, contract pinning y KISS/YAGNI.
- `main/10-projects/Echo Futures/Echo Futures — D3 Astra Architecture Review.md` — D3-01/D3-05 aceptados y contraejemplos exactos.
- `main/10-projects/Echo Futures/Echo Futures Architecture Candidate V1.md` — integrated D2 state a superseder en V2.
- `main/10-projects/Echo Futures/Echo Futures — D2-06 Market Runtime.md` — MarketEvent, identities, owner_input_seq/runtime_ts, recording, EXACT_REPLAY, topology/durability.
- `main/10-projects/Echo Futures/Echo Futures — D2-08 Strategy Runtime.md` — Strategy/MM ownership, triggers, lightweight MM notifications, shared MarketContext, replay boundary.
- `main/10-projects/Echo Futures/Echo Futures — D2-06A Market Feed Authority.md` — source identity classes, `stream_id`, candidate keying, seq assignment, deliberate ALO egress.
- `main/10-projects/Echo Futures/Echo Futures — D2-06B Bars Hot State Warmup.md` — compacted/read-model bars, Strategy current-state pulls, MM MarketContext shape, late corrections.
- `main/10-projects/Echo Futures/Echo Futures — D2-06C Live Replay Market Boundary.md` — per-island journals, source refs y claim refutado de que pull cross-stream requería “sin trabajo adicional”.

### Source físico puntual

- `xKoRx/echo@372af59a7b83604781346613da01e3d510ea1360`, `v3/sdk/kache/account_configs.go:38-54,98-132` — cache in-memory con consumer Kafka propio/background; prueba que latest-value propagation es independiente del owner input de Strategy/MM.
- `xKoRx/echo@372af59a7b83604781346613da01e3d510ea1360`, `v3/sdk/kache/README.md` — cache compactada, latest per key y actualizaciones automáticas; patrón reutilizable, no authority de replay.

### External puntual

- Apache Flink Stateful Functions 3.2 Kafka I/O: el egress `AT_LEAST_ONCE` permite duplicados y el ingress Kafka trabaja sobre records/offsets; suficiente para demostrar que el per-stream durable input order y su position provenance son físicamente representables sin sequencer externo. No se usa esta fuente para seleccionar vendor ni transport externo.

## 19. Handoff de integración

Architecture Candidate V2 debe superseder las siguientes frases/claims de V1/D2:

- “`stream_seq` checkpointeado + ALO basta para idempotencia” → reemplazar por durable canonicalization input order + stable seq mapping + canonical_event_id.
- “pull cross-stream hereda exactitud del producer journal sin trabajo adicional” → reemplazar por context_reads[]/read-set.
- “MM notification con trigger ref + current latest es replay provenance suficiente” → reemplazar por trigger ref + decision-scoped captured reads.
- “BAR_CLOSED identificado sólo por BarId y latest projection” → precisar exact trigger version/observation.

No debe tocar los cierres D2 no afectados ni reescribir historia para fingir que V1 nunca tuvo estos defects.

D3-01: CANDIDATE_RESOLVED
D3-05: CANDIDATE_RESOLVED
OWNER_DECISIONS_REQUIRED: NONE
CROSS_WORKSTREAM_ASSUMPTIONS: D4-A2/A3 e integración no deben usar stream_seq como event identity; cualquier nueva decisión MM market-dependent introducida por sus correcciones debe consumir el mismo decision-scoped MarketContext/context_reads[] contract; no se asume ningún cambio adicional en Operation/MM/provider ownership o lifecycle.
