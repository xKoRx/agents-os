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
  - "[[Echo Futures — D1 Analysis Pack]]"
aliases:
  - Echo Futures D2-07A
  - EF Generic Execution Adapter Contract
tags:
  - kind/doc
  - area/echo
  - echo-futures
  - architecture-design
created: "2026-09-27"
updated: "2026-09-27"
---

# Echo Futures — D2-07A Execution Adapter Contract

## Propósito

Definir la interfaz semántica genérica que todo execution adapter de Echo Futures debe cumplir antes de que D2-07B pueda evaluar transportes y D2-07C pueda diseñar topología. Este documento no selecciona transport, no diseña la topología física, no implementa código y no cierra D2-07.

Autoridades consumidas: [[Echo Futures]], [[Echo Futures — D2-04 Operation Order Fill Position]], [[Echo Futures — D2-05 Instrument Session Provider]], [[Echo Futures — D2-06 Market Runtime]], [[Echo Futures — D1 Analysis Pack]], `EXECUTION TRANSPORT FEASIBILITY — MULTI-PROP EVIDENCE.md` y `FUTURES PROP UNIVERSE — AUTHORITATIVE EVIDENCE MATRIX.md`.

Baseline físico contrastado: `xKoRx/echo@372af59a7b83604781346613da01e3d510ea1360`, idéntico al baseline entregado por el SUBMANAGER. No hubo delta de Echo que justificara auditoría repo-wide.

## 1. Executive verdict

`D2-07A STATUS: READY_FOR_SUBMANAGER_REVIEW`.

El adapter debe ser una frontera de side effects externos, no una segunda capa de dominio. Core sigue siendo autoridad de `Operation → Order → Fill`; el adapter traduce una Order ya materializada y pinneada, ejecuta acciones sobre el venue, conserva la correlación física y devuelve observaciones normalizadas.

La garantía de D2-04 se divide literalmente en dos boundaries. **M1** termina al commit checkpoint-coordinated de StateFun + Kafka command egress y es `EXACTLY_ONCE`. **M2** comienza cuando el adapter puede producir un side effect físico externo y **no puede declararse exactly-once por Kafka, command_id, ACK local ni un registro PENDING**. M2 requiere durable write-ahead submission intent, `client_order_id` estable y una autoridad de reconciliación capaz de responder después de crash/timeout si esa identidad existe, ejecutó o fue terminal.

El point-of-no-return es el primer paso que puede alcanzar físicamente al venue. Antes de cruzarlo el intent completo debe estar durable. Después de cruzarlo, cualquier timeout/crash/ACK perdido se trata como **MAY_HAVE_EXECUTED**: nunca se reenvía a ciegas. Se consulta por `client_order_id`, idempotency key nativa o historial autoritativo. Si no puede probarse existencia ni ausencia, el estado queda `AMBIGUOUS`, se bloquea nueva exposición y no se fabrica resultado.

Readiness no equivale a socket conectado. Para abrir riesgo se requiere conexión + autenticación + binding de cuenta + entitlement + event stream + autoridad M2 de lookup/history + posición fresca + capabilities requeridas. Las reducciones/cierres pueden conservar un gate separado sólo cuando el transport puede demostrar que la acción no aumenta riesgo y conserva finality; en otro caso también falla cerrado.

El source actual de Echo V3 confirma por qué este contrato es necesario: MT4/MT5 deduplican `command_id` con un journal local, pero persisten el resultado **después** de `OrderSend` / `CTrade.Buy|Sell`. Crash entre side effect y `g_Journal.Add` permite replay físico. Ese patrón no satisface M2 y no debe copiarse a Futures.

D2-07B recibe un capability/evidence contract; ningún transport queda certificado por este documento. D2-07C recibe invariantes de ownership, durability, session generation y takeover; no se decide aquí proceso, host, store ni HA.

## 2. Evidence classification

### FACT

- D2-04 congela `Operation 1 → 0..N Order`, `Order 1 → 0..N Fill`, partial fills first-class, Fill inmutable y Position física neta por `Account + Contract`.
- `order_id = client_order_id` es identidad Core y correlation/idempotency key hacia venue.
- M1 es StateFun state + Kafka command egress `EXACTLY_ONCE`; no cubre el venue.
- D2-05 congela Provider separado de transport, binding account-scoped, entitlement explícito y `UNKNOWN != ALLOWED`.
- D2-05 congela que cancel/expire no liberan reservas sólo por enum local; release espera finality física.
- D2-06 separa market runtime de execution transport.
- Echo V3 actual marca Kafka offset después del procesamiento hacia el pipe, pero el side effect MT puede ocurrir antes de que el EA persista `command_id`.
- Echo V3 `SlaveCommandJournal` es rolling y post-side-effect: guarda ticket/resultado y reenvía results pendientes, pero no existe durable submission intent previo al envío físico.
- El research aceptado demuestra capacidades generales de órdenes/eventos en varios transports, pero **no demuestra uniformemente** authoritative negative lookup, retención/horizonte de history, client-order round-trip, stable execution identity ni native idempotency para todos ellos.

### DECISION CANDIDATE

Todo lo definido desde §3 a §19 es el contrato candidato D2-07A para integración por el SUBMANAGER.

### INFERENCE

- El journal M2 debe vivir en la durability domain del side-effect owner o en una autoridad durable accesible por él; guardarlo sólo como proyección Core/PG no cierra la ventana física.
- Un reconnect sin reconciliación completa no puede restaurar `EXECUTION_READY_NEW_RISK`.
- Un transport que no entrega stable execution identity o una autoridad equivalente de executions no puede satisfacer el Fill contract exacto de D2-04 mediante heurística local.

### UNKNOWN

- Qué transports concretos satisfacen todos los requisitos M2.
- Semántica exacta de “no encontrado” y sus ventanas de consistencia por transport.
- Retención/cursor de execution history y estabilidad de execution IDs por transport.
- Si cada client tag/order ref preserva byte-for-byte la identidad Echo y cuál es su scope de unicidad.
- Store físico, process model, lease/fencing y takeover policy de D2-07C.

## 3. Core invariants

**I1 — One domain Order.** El adapter nunca crea una segunda entidad Order de dominio para “representar” el venue. Traduce la Order Core y conserva su identidad.

**I2 — Stable submission identity.** `client_order_id` no cambia por retry, reconnect, proceso, sesión ni redelivery. Para submit es la identity key M2.

**I3 — Binding pinning.** Cada side effect guarda durablemente el `transport_id`, provider external account identity y external contract identifier usados. Un hot rebind posterior no reescribe una Order viva.

**I4 — Write before side effect.** El intent completo debe ser durable antes del point-of-no-return.

**I5 — No blind retry after uncertainty.** Después de cualquier posibilidad de side effect, retry físico sólo es legal si native idempotency hace el retry seguro con la misma key o si reconciliación autoritativa demuestra que el side effect no ocurrió.

**I6 — External truth wins.** ACK local, timeout local, Kafka offset, process memory y PG projection no son venue truth.

**I7 — Fill is immutable.** Partial/multi-fill son normales; ningún Fill se clampa, edita ni reemplaza.

**I8 — No invented execution identity.** Si el provider no entrega identidad de ejecución estable, el adapter no fabrica una dedup identity por precio/tiempo/seq local. La capability queda degradada y puede volver el transport/order-class inelegible para V1 exact submission.

**I9 — Position is observation.** Position = `execution_account_id + contract_id` neta; jamás se atribuye Operation por delta de Position.

**I10 — Manual/unknown physical activity stays unknown.** No se fabrica Operation para explicar una Position o Fill no correlacionable.

**I11 — Finality needs evidence.** Core no libera reservation, terminaliza Operation ni declara close exitoso por un enum local o request ACK.

**I12 — Reconnect is recovery, not a trigger.** Reconectar jamás reemite órdenes automáticamente.

**I13 — Static eligibility ≠ dynamic readiness.** Provider permission/capability decide si una cuenta puede usar un transport; readiness decide si puede ejecutar ahora.

**I14 — Fail closed on unresolved correctness.** Ambigüedad M2, history no autoritativa, position stale o binding inconsistente bloquean nueva exposición.

**I15 — Market/execution separation.** Adapter no es autoridad de barras, replay ni logical market stream.

## 4. Adapter identities

| Identidad | Semántica | Correctness |
|---|---|---|
| `transport_id` | Familia/config concreta de transport usada por la Account | Sí; pinneada por side effect y recovery |
| `execution_account_id` | Echo Account target | Sí; routing y scope de dominio |
| provider external account identity | ID de cuenta que el venue/transport autentica y observa | Sí; debe verificarse contra el binding antes de readiness |
| connection/session identity | Epoch efímero de conexión autenticada | Sí para ordering/readiness; **no** es idempotency key de negocio |
| adapter/process instance identity | Instancia operativa para logs/leases | Observabilidad/topología; no identifica Orders |
| `client_order_id` | Identidad Echo estable de la Order física | Sí; primary M2 correlation key |
| `provider_order_id` | Identidad nativa del order en venue | Sí cuando existe; nullable antes de ACK/reconciliation |
| `provider_execution_id` | Identidad nativa estable de un Fill/execution | Sí para canonical Fill/dedup |

Separaciones obligatorias:

```text
Echo Account
!= provider external account
!= credential/session
!= adapter process
```

La session identity cambia al reconnect; `client_order_id` no. La process identity puede cambiar por restart; `client_order_id`, provider binding y journal no.

## 5. Execution command boundary

El boundary parte de la Order de D2-04. No introduce un “BrokerOrder” de dominio.

### Submit semantic payload

```text
SubmitOrder {
  client_order_id      # = order_id D2-04
  operation_id
  order_id
  execution_account_id
  contract_id
  external_contract_identifier
  side
  order_type
  qty
  limit_price?
  stop_price?
  tif?
}
```

**Correlation only:** `operation_id`, `order_id`, `client_order_id`.

**Venue translation input:** `execution_account_id`, `external_contract_identifier`, `side`, `order_type`, `qty`, precios y TIF aplicables.

**Pinned before side effect:** `transport_id`, provider external account identity, `external_contract_identifier`, los términos completos de la Order y la identidad del command/action. El journal debe poder reconstruir exactamente qué se intentó enviar aunque el control-plane haya cambiado.

**No pertenecen al adapter command:** Strategy config, MM state, RuleSet completo, provider policy evaluators, market bars, signal logic, sizing logic, current-contract resolver ni auto-roll. Todo eso fue resuelto antes del egress.

### Modify / Cancel semantic payload

Cada acción side-effecting tiene identidad estable propia, reutilizando D2-04:

- submit: `client_order_id`;
- modify/replace: `replace_request_id`;
- cancel: `cancel_id`.

Un redelivery mantiene el mismo action id. El adapter no genera una nueva domain Order por su cuenta.

Si el transport soporta native modify/atomic replace, la acción muta la Order existente conforme D2-04. Si sólo soporta cancel+replace y D2-04 requiere una replacement Order nueva, **Core debe proporcionar la nueva `order_id/client_order_id`**; el adapter posee la coreografía física, no la identidad de dominio.

## 6. Submit semantics

### 6.1 Sequence

1. Validar static eligibility + dynamic readiness.
2. Resolver el binding activo requerido por esa Order y verificar que coincide con la identidad pinneada.
3. Persistir `PREPARED` con el intent completo y correlation.
4. Persistir `SUBMITTING` **antes** de invocar la operación que puede alcanzar al venue.
5. Cruzar el point-of-no-return enviando con el mismo `client_order_id` / native idempotency token.
6. Persistir toda evidencia devuelta: provider order id, provider response, status, timestamps/cursors.
7. Publicar normalized observations hacia Core.
8. Si el resultado es timeout, disconnect, process crash o respuesta no concluyente: no re-submit; ejecutar recovery por la misma identity.
9. Si lookup/history prueba que existe: bindear `provider_order_id`, recuperar fills/status y converger.
10. Si prueba autoritativamente que no existe: sólo entonces puede intentarse submit con **la misma identity**, y sólo si la semántica de negative lookup garantiza que no aparecerá luego una orden previa.
11. Si no puede probar ni existencia ni ausencia: `AMBIGUOUS` → fail closed.

### 6.2 Point-of-no-return

Es el primer call/write que puede producir un side effect venue-visible, no el ACK. El adapter debe entrar a estado durable `SUBMITTING` antes de ese punto.

Un crash en `PREPARED` puede terminar siendo “no enviado”. Un crash en `SUBMITTING` siempre se recupera como `MAY_HAVE_EXECUTED`, incluso si físicamente ocurrió antes de transmitir: la falta de conocimiento local no autoriza asumir ausencia.

### 6.3 Fast MARKET

Un MARKET puede llenar antes de que llegue o se persista el ACK. El Fill puede ser la primera evidencia autoritativa observada. El adapter debe aceptar `Fill before Order ACK`, bindear la correlación disponible y reconstruir el Order state desde fill/history. Nunca espera ACK para preservar un Fill real.

### 6.4 Definite reject

Un reject es terminal sólo si la respuesta del transport es contractualmente autoritativa de “no order accepted/no execution possible” para esa request identity. Un error de red, timeout, 5xx, “unknown”, session loss o SDK exception no es reject físico.

## 7. Durable submission journal

No se congela SQLite/Postgres/RocksDB/etc. Se congela semántica.

### 7.1 Identity

Primary key conceptual:

```text
(execution_account_id, client_order_id)
```

El row/record pinnea además:

```text
transport_id
provider_external_account_id
operation_id
order_id
external_contract_identifier
full submitted terms
current action ids (replace_request_id / cancel_id)
provider_order_id(s)
evidence / cursors / timestamps
state
```

No se mete session/process ID en la identity. Sí puede guardarse como provenance.

### 7.2 Minimal states

```text
PREPARED
SUBMITTING
VENUE_BOUND
TERMINAL
AMBIGUOUS
```

- `PREPARED`: intent completo durable; side effect todavía no autorizado.
- `SUBMITTING`: point-of-no-return habilitado/cruzable; outcome puede ser desconocido.
- `VENUE_BOUND`: existencia física demostrada y provider identity/status reconciliable.
- `TERMINAL`: venue execution finality demostrada y fills requeridos reconciliados.
- `AMBIGUOUS`: no puede demostrarse una verdad suficiente; requiere fail-closed/operator resolution.

No se necesita FSM decorativa para representar cada vendor status; esos status viven como evidence/observations.

### 7.3 Persisted evidence

Guardar sólo lo necesario para recovery y auditoría de correctness:

- stable client/action identities;
- physical binding;
- provider order identities y replacement chain;
- authoritative response/status;
- last reconciled execution/history cursor o watermark cuando el transport lo provea;
- observed cumulative filled qty;
- terminal evidence;
- ambiguity reason.

### 7.4 Restart

Al startup/reconnect se cargan primero todos los records no `TERMINAL`. Ninguno se reenvía antes de reconciliation.

### 7.5 Garbage collection

Nunca GC `AMBIGUOUS`. Un `TERMINAL` sólo puede compactarse cuando:

1. terminal/fill reconciliation ya está durable downstream;
2. la ventana legítima de command redelivery/recovery ya no puede reintroducir esa identity **o** queda un tombstone durable de `client_order_id`;
3. native/provider idempotency/history horizon necesario no ha sido sobrepasado durante recovery.

D2-07C decide retention/store. Para V1, preferir tombstone compacto antes que GC agresivo: UUIDv7 no se reutiliza y el costo es pequeño frente a una orden duplicada.

## 8. External idempotency / M1-M2 boundary

### M1 — Core state → Kafka command

```text
StateFun checkpoint state
+ transactional Kafka egress
= EXACTLY_ONCE boundary
```

M1 demuestra que el command que escapó de Core corresponde a estado commiteado. No demuestra que un consumer/adapter no pueda repetir un side effect después de recibirlo.

### M2 — Kafka command → venue physical side effect

M2 requiere una de estas rutas probadas:

**Route A — native idempotency:** el venue acepta una client id/idempotency key estable y reintentar la misma key garantiza no crear otra order, con alcance/retención documentados.

**Route B — authoritative lookup/history:** el venue round-trips `client_order_id` y permite demostrar, tras outcome incierto, existencia/ejecuciones/terminalidad o una ausencia autoritativa suficiente para un retry seguro.

Normalmente se usan ambas cuando existen.

### Prohibited pseudo-idempotency

No satisfacen M2 por sí solos:

- dedupe de `command_id` en memoria;
- marcar Kafka offset;
- guardar `PENDING` antes del send sin lookup;
- guardar ticket/provider_order_id sólo después del ACK;
- “retry N times”;
- asumir timeout = reject;
- position snapshot que casualmente coincide;
- PG projection de Core;
- comentario/tag que no sea consultable/round-trippable autoritativamente.

Transport/order-class que no cierra M2:

`UNSUPPORTED_FOR_V1_EXACT_SUBMISSION`.

## 9. Normalized execution event model

El adapter emite cinco familias semánticas, no DTOs vendor-specific.

### 9.1 OrderObservation

```text
OrderObservation {
  execution_account_id
  operation_id
  order_id / client_order_id
  provider_order_id?
  status
  cumulative_filled_qty?
  remaining_qty?
  observed_at
  venue_time?
  source              # REALTIME | RECONCILIATION | HISTORY
  authority_evidence
}
```

Canonical `status` mínimo:

```text
ACCEPTED
WORKING
PARTIALLY_FILLED
FILLED
REJECTED
CANCELLED
EXPIRED
```

No se modela `SUBMITTING` como venue status: es journal local.

### 9.2 OrderActionObservation

Para modify/cancel/replace:

```text
action_id
kind                  # MODIFY | CANCEL | REPLACE
outcome               # ACCEPTED | REJECTED | AMBIGUOUS
target client/provider order refs
replacement refs?     # si aplica
evidence
```

Un action ACK indica que la acción fue aceptada/procesada por la API según su contrato. **No equivale automáticamente a order execution finality.**

### 9.3 Fill

Hecho físico inmutable, §10.

### 9.4 PositionObservation

Observación física neta, §11.

### 9.5 ExecutionSessionObservation

Estado de conexión/auth/binding/event-stream/reconciliation/position/readiness. Es observación de runtime, no domain Order event.

Esta separación evita convertir connection state, mutation ACKs y snapshots en estados artificiales del aggregate.

## 10. Fill semantics

Canonical Fill requerido por D2-04:

```text
provider_execution_id
provider_order_id
client_order_id / order_id
operation_id
execution_account_id
contract_id
side
qty
price
executed_at
received_at
source
fees?                 # sólo si provider lo entrega con autoridad útil
```

### Stable execution identity

Cuando el provider entrega `provider_execution_id`, dedup key:

```text
(execution_account_id, provider_execution_id)
```

Si el ID tiene scope más estrecho documentado, D2-07B debe incluir el scope necesario; no se adivina.

### No provider_execution_id

D2-07A adopta la regla explícita del mandato: **no fabricar dedup identity** con `price+time+qty`, sequence local ni hashes heurísticos.

Si el provider ofrece otra identity nativa de execution inequívoca, D2-07B puede mapearla al campo canónico con provenance. Si no ofrece ninguna y realtime/history puede duplicar/reordenar executions, el adapter no puede emitir Fills exactos de manera restart-safe: capability = incompatible con V1 exact execution semantics.

Esto deja un punto de integración a revisar con D2-04 §2.3, cuyo wording antiguo permitía ejemplos sintéticos como `orderId:seq`. D2-07A **no modifica D2-04**; exporta la contradicción al SUBMANAGER y aplica la regla más estricta recibida para este worker.

### Partial / multi-fill

BUY 3 con executions `+1,+1,+1` produce tres Fill facts y un solo Order. `filled_qty` y avg price son derivados por Core.

### Realtime + history duplicates

Misma provider execution identity = mismo Fill, independiente de source. History puede descubrir un Fill antes no visto y se emite con `source=HISTORY|RECONCILIATION`.

### Imperfect ordering

Fill puede llegar antes que ACCEPTED/WORKING. No se descarta ni retrasa esperando “orden bonito”. Correlación se resuelve por client/provider identity + journal.

## 11. Position observation

```text
PositionObservation {
  execution_account_id
  contract_id
  net_qty
  avg_price
  as_of
  source              # REALTIME | SNAPSHOT | RECONCILIATION
  snapshot_scope      # complete account snapshot vs incremental observation
}
```

No contiene `operation_id` ni Strategy attribution.

Una snapshot completa puede usar ausencia como evidencia de flat sólo si el transport declara explícitamente completeness para ese account/scope/as_of. Una actualización incremental no.

Manual order, SDK externo, liquidación del provider u otra actividad desconocida puede mover Position. Resultado:

- preservar physical observation;
- calcular `POSITION_MISMATCH` / reconciliation debt;
- marcar account degraded/alertable según severidad;
- nunca crear Operation/Fill Echo por inferencia de delta.

## 12. Modify / cancel / replace semantics

### Native modify

- misma domain Order;
- `replace_request_id` estable;
- adapter modifica sólo fields declarados mutables por capability;
- accepted action no libera reservation por sí solo;
- Core aplica nueva semántica sólo con evidence venue suficiente.

### Atomic replace

Si el transport reemplaza la order de forma atómica pero puede cambiar `provider_order_id`, el journal conserva old/new provider refs y la misma domain identity cuando D2-04 lo permita. Finality requiere que los nuevos términos sean venue-authoritative.

### Cancel + replace

Cuando la capability es cancel+replace y D2-04 requiere una nueva domain Order:

- Core crea/proporciona la replacement Order y su nuevo `client_order_id`;
- adapter no inventa esa identidad;
- old reservation/order permanece pendiente de finality mientras cancel es incierto;
- new submit sigue su propio M2 journal;
- una falla entre cancel y new submit queda visible; no se finge atomicidad.

### Partial modification

Capability declara qué dimensión puede cambiar sin replacement: remaining qty, limit, stop, TIF, etc. Pedido fuera de capability se rechaza **antes** del side effect.

### Cancel

`cancel_id` estable. Outcomes:

- request accepted ≠ cancel final;
- venue order status/historical terminal evidence + fills reconciliados = cancel final;
- timeout/disconnect = ambiguous cancel;
- late Fill siempre se preserva aunque cancel haya sido solicitado o incluso observado antes.

## 13. Capability contract

D2-07B no recibe 50 booleans. Recibe tres bloques con estado de evidencia.

### 13.1 Order capabilities

```text
supported_order_types: { MARKET, LIMIT, STOP }
modify_mode: NONE | NATIVE | ATOMIC_REPLACE | CANCEL_REPLACE
mutable_fields: set mínimo documentado
cancel: supported/unsupported
partial_fill_delivery: realtime/history/both/unknown
```

### 13.2 Recovery / correctness capabilities

```text
client_order_id_round_trip
lookup_by_client_order_id
authoritative_negative_lookup
native_idempotency
open_order_snapshot
execution_history
stable_provider_execution_id
terminal_order_history
position_snapshot
reconnect_and_resubscribe
```

Para lookup/history se registra scope, consistency y horizon cuando importan a correctness.

### 13.3 Session/topology capabilities

```text
multi_account_session
account_binding_discovery
session_recovery
provider_account_isolation
```

Estas no autorizan ejecución por sí solas; alimentan D2-07C.

### 13.4 Evidence status

Cada capability se clasifica:

```text
PROVEN
CONDITIONAL
UNKNOWN
UNSUPPORTED
```

`CONDITIONAL` debe expresar condición concreta. `UNKNOWN` nunca pasa el gate de una capability obligatoria.

D2-07B debe guardar claim-level first-party evidence, fecha y authority. Una UI/platform que “soporta NinjaTrader/Tradovate/etc.” no prueba developer/API entitlement ni M2.

## 14. Account eligibility

Static eligibility:

```text
ProviderProgram permits transport
AND transport entitlement == ALLOWED
AND adapter capabilities satisfy required Order/MM behavior
AND M2 exact submission contract satisfied for required order classes
```

`UNKNOWN != ALLOWED`.

Platform support, automation permission, API/developer entitlement y technical capability son cuatro claims separados.

El resultado static puede ser `ELIGIBLE` o `INELIGIBLE/UNKNOWN`; no implica que el runtime esté listo ahora.

## 15. Readiness

### 15.1 Component state

Mantener siete dimensiones, KISS:

1. `connection`;
2. `authentication`;
3. `account_binding`;
4. `order_event_stream`;
5. `reconciliation_authority` (lookup/history);
6. `position_state`;
7. `submission_capability`.

### 15.2 NEW_RISK gate

`EXECUTION_READY_NEW_RISK` sólo cuando:

```text
static account eligibility == ELIGIBLE
AND connected
AND authenticated
AND provider account bound/verified
AND required event stream LIVE
AND reconciliation authority AUTHORITATIVE
AND no unresolved M2 ambiguity
AND position snapshot FRESH/complete enough
AND required submit capabilities EXACT_READY
```

Command consumption saludable mientras venue está unhealthy **no** es ready.

### 15.3 CLOSE / REDUCE gate

Cerrar/reducir riesgo puede mantenerse disponible bajo degradación sólo si el adapter puede demostrar:

- target físico identificable;
- la acción solicitada no puede aumentar exposición bajo la semántica disponible;
- la acción tiene finality/reconciliation suficiente para no inventar éxito.

Si eso no se demuestra, bloquear la acción automática y elevar operator/safety state. Nunca responder “close success” porque se encoló un command.

### 15.4 Startup

Estado inicial: not ready. Authenticate → bind → establish streams → reconcile unresolved journal/open orders/fills → obtain fresh position → derive readiness. No new-risk antes.

### 15.5 Degradation

- history/lookup degraded: NEW_RISK off;
- event stream down: NEW_RISK off, recovery pending;
- position stale: NEW_RISK off;
- socket down: all physical actions unavailable hasta recovery;
- unresolved ambiguous submit/cancel/replace: account-level NEW_RISK off en V1 KISS.

## 16. Authoritative venue finality

Se distinguen:

```text
WORKING
PARTIAL
FILLED
REJECTED
CANCEL_PENDING
CANCELLED_CONFIRMED
EXPIRED_CONFIRMED
MODIFY_REPLACE_PENDING
TERMINAL_EXECUTION_FINAL
AMBIGUOUS
```

No todos deben ser `Order.status`; varios son adapter/journal/finality state.

### Evidence suficiente

**WORKING:** provider order existence + active/working state autoritativo.

**PARTIAL:** al menos un Fill estable + remaining/cumulative state consistente.

**FILLED candidate:** cumulative fills alcanzan qty o provider reporta filled. **Execution final** requiere además recuperar/deduplicar los Fill facts que explican esa cantidad.

**REJECTED final:** provider response/history garantiza que esa request no creó una order ejecutable.

**CANCELLED_CONFIRMED:** provider reporta old order terminal cancelled/no remaining working qty. **Execution final** espera además reconciliar fills que pudieron ganar la race.

**EXPIRED_CONFIRMED:** igual principio; venue terminal + executions cubiertas.

**MODIFY final:** authoritative order state refleja los nuevos términos, no sólo “request accepted”.

**REPLACE final:** old leg execution-final y replacement venue-bound/authoritative según la semántica del replace. Si cualquiera queda incierta, replace sigue ambiguous/pending.

### Late fills

“Cancelled confirmed” no significa que el delivery channel no pueda entregar después un Fill ocurrido antes o durante la race. Un Fill nuevo estable siempre se conserva y corrige forward el estado derivado.

Core libera reservation/terminaliza Operation sólo cuando recibe evidence de `TERMINAL_EXECUTION_FINAL` compatible con D2-05, no por `cancel requested`.

## 17. Reconnect / recovery

Recovery sequence por execution account:

1. poner NEW_RISK not-ready;
2. autenticar;
3. verificar provider external account binding;
4. restablecer event stream/resubscriptions;
5. cargar todos los journal records no terminales;
6. por cada `PREPARED/SUBMITTING/AMBIGUOUS/VENUE_BOUND`, resolver por client identity/native idempotency/provider order refs/history;
7. listar/reconciliar open Orders Echo y detectar Orders desconocidas;
8. recuperar executions desde cursor/horizon y deduplicar por provider execution identity;
9. obtener Position snapshot autoritativa;
10. emitir missed normalized observations/Fills;
11. comparar physical state vs logical state y surfacing mismatch;
12. sólo entonces reevaluar readiness.

No existe “on reconnect → replay pending commands”.

### Working orders during disconnect

Se recuperan como physical state; no se duplican ni cancelan automáticamente.

### MARKET accepted + crash before offset/result

Redelivery encuentra journal `SUBMITTING`; adapter consulta por la misma `client_order_id`. Si existe/fill, converge. No segunda order.

### Fill during disconnect

History/reconciliation recupera el execution; misma provider execution identity absorbe duplicado realtime/history.

### Ambiguous cancel

La Order conserva reservation/finality pendiente hasta evidence venue-authoritative.

### Provider order exists + journal uncertain

Se re-bindea usando `client_order_id`, native idempotency/history y provider order id descubierto. Si no puede correlacionarse inequívocamente: `AMBIGUOUS`, fail closed.

## 18. Unknown / manual execution handling

Activity venue no correlacionable con el submission registry:

- no entra a `echo/operation` como Fill Echo;
- sí alimenta PositionObservation;
- si el venue ofrece Order/Execution event desconocido, se conserva como diagnostic/reconciliation observation con provider identities;
- genera mismatch/debt;
- puede degradar NEW_RISK readiness según impacto;
- nunca fabrica Operation, Strategy attribution ni synthetic Fill.

Si posteriormente reconciliation demuestra que la activity sí pertenece a un `client_order_id` Echo, recién entonces se emiten los canonical facts con identidad real.

## 19. ProviderAccountBinding compatibility

D2-05 se mantiene:

```text
ProviderAccountBinding {
  provider/program/phase?
  RuleSet authority
  transport {
    transport_id
    entitlement
    conditions[]
  }
  day boundary
  enabled
}
```

`AccountStrategy` no gana transport fields.

El adapter recibe/posee un execution account binding, no una Strategy binding. Cada journal intent pinnea el binding físico que usó.

Hot rebind:

- afecta future submissions cuando los gates lo autoricen;
- no mueve una live physical Order al nuevo adapter;
- recovery de esa Order continúa contra el original transport/provider account hasta terminal/reconciliation;
- si el transport anterior deja de ser accesible, el estado es recovery debt/operator action, no remap silencioso.

Entitlement revocado: deny new risk y detener nuevos submits conforme D2-05; no auto-force-close salvo regla explícita. Close/reduce sigue el gate conservador §15.3.

## 20. Acceptance-case walkthrough

### A — Normal MARKET

Core crea Order/client id → M1 egress exact → adapter PREPARED durable → SUBMITTING durable → single venue submit → ACK o Fill → VENUE_BOUND → canonical Fill → PositionObservation converge → terminal execution finality. Una sola physical order.

### B — Partial fills

BUY 3 recibe tres provider executions estables `+1,+1,+1`. Adapter emite tres Fill facts inmutables. Core mantiene un Order y una Operation; filled qty/avg son derivados. No collapse en “ExecutionResult success”.

### C — Cancel/Fill race

Cancel `cancel_id` durable → request. Fill ocurre antes/durante cancel → Fill se preserva. Cancel ACK no libera. History/order state demuestra remaining=0/cancelled y executions cubiertas → finality. Si fills llegan después por delivery lag, se dedup/aplican igualmente.

### D — Fast MARKET + crash

Physical execution ocurre después de `SUBMITTING`; proceso muere antes de persistir ACK/result/Kafka offset. Redelivery carga `SUBMITTING`, consulta la misma identity, encuentra order/fill y converge. No segundo submit.

### E — Reconnect gap

Fill ocurre desconectado. Reconnect mantiene NEW_RISK off, recovery history encuentra execution ID, emite Fill; si realtime luego repite el mismo execution, dedup. Operation converge.

### F — Manual order

Venue Position cambia y/o llega order/execution desconocido. No hay submission registry matching. Adapter emite physical observation + reconciliation mismatch; ninguna Operation es fabricada.

### G — Transport sin history/lookup/client correlation suficiente

Outcome MARKET incierto no puede responder “¿existió/ejecutó client_order_id X?”. Resultado: `UNSUPPORTED_FOR_V1_EXACT_SUBMISSION`. No se aproxima con retries ni position delta.

### H — Entitlement UNKNOWN

Aunque technical capabilities sean perfectas, static account eligibility falla. `EXECUTION_READY_NEW_RISK=false`.

## 21. Constraints exported to D2-07B

D2-07B debe evaluar por **transport + order class + provider/program entitlement**, no por marca general.

Capabilities exactas que debe probar:

1. `supported_order_types`;
2. `modify_mode`;
3. `mutable_fields`;
4. `cancel`;
5. `partial_fill_delivery`;
6. `client_order_id_round_trip`;
7. `lookup_by_client_order_id`;
8. `authoritative_negative_lookup` + consistency/horizon;
9. `native_idempotency` + scope/retention;
10. `open_order_snapshot`;
11. `execution_history` + recovery cursor/horizon;
12. `stable_provider_execution_id`;
13. `terminal_order_history/finality evidence`;
14. `position_snapshot` + completeness semantics;
15. `reconnect_and_resubscribe`;
16. `multi_account_session`;
17. provider external account discovery/binding;
18. ProviderProgram automation permission;
19. direct developer/API entitlement.

Mandatory M2 claims must be `PROVEN` or narrowly `CONDITIONAL` with a condition Echo can enforce. `UNKNOWN` fails eligibility.

El research D1 actual sirve como candidate corpus, no como certificación M2. En particular, labels generales “supports orders/reconnect/idempotency” no bastan sin first-party evidence del lookup/identity/finality concreto.

## 22. Constraints exported to D2-07C

D2-07C debe respetar:

1. **Single side-effect authority:** una execution account/binding no puede tener dos owners capaces de submit ciego simultáneamente.
2. **Durable journal before venue:** la durability domain debe sobrevivir el restart que la topología pretende tolerar.
3. **Takeover implies journal + reconciliation authority:** cross-process/host takeover sólo es seguro si el nuevo owner puede leer el mismo durable journal y consultar el original venue binding; si no, takeover debe prohibirse.
4. **Session generation:** un owner/session reemplazado no puede volver a habilitar submission después de quedar stale.
5. **Live Order stays on original physical binding** hasta terminal/reconciliation; hot rebind no la migra.
6. **Account readiness is owned coherently:** ninguna instancia aislada puede declararse ready sólo por socket local.
7. **Reconnect blocks new risk until reconciliation barrier completes.**
8. **Command consumer delivery != physical completion:** Kafka offset/pipe delivery no puede ser el commit de side effect.
9. **Journal GC horizon must dominate redelivery/recovery risk** o conservar tombstone.
10. **Unknown physical activity is observable, not auto-adopted.**
11. **Close-only degraded path needs explicit proof of non-risk-increasing semantics;** no shortcut por urgencia.
12. **Adapter process identity is not business identity.**
13. **No topology may require Core PG as M2 recovery authority.**
14. **Metrics/traces must expose ambiguity/readiness/reconciliation lag**, pero observability no es correctness.

No se decide aquí local service vs shared daemon, Windows/Linux, per-account process, connection pool, lease technology, DB concreta ni HA.

## 23. Echo V3 contrast

Inspección puntual sobre `xKoRx/echo@372af59a7b83604781346613da01e3d510ea1360`:

### Reusable semantics

- `v3/bridge/internal/session/command_consumer.go`: tópico per execution account, backpressure/retry hacia pipe y offset marcado después de delivery son patrones útiles de routing.
- `v3/sdk/domain/messages.go`: batch de results + snapshots y resend de results ayuda al delivery adapter→Core.
- `v3/sdk/domain/position_snapshot.go` + `v3/core/internal/functions/position_sync.go`: patrón de observación/proyección física reutilizable; el shape Futures se reemplaza por `Account+Contract`.
- `v3/clients/*/EchoPersistence.mqh`: durable local result journal y replay de resultados demuestran valor de persistencia en edge.

### Debt / not reusable as M2

- `SlaveCommandJournal.Add` se ejecuta después de `OrderSend` / `CTrade.Buy|Sell`; hay crash window física.
- La dedup actual es por `command_id` procesado, no por durable pre-submit intent + venue lookup.
- El journal actual guarda ticket/result, no la intención completa pinneada antes del side effect.
- rolling window / cleanup no está ligado a Kafka redelivery ni venue history horizon.
- `ExecutionResult success` modela un único resultado/ticket y no reemplaza Order→N Fill.
- PG `ON CONFLICT` de PositionSync es idempotencia de proyección, no idempotencia de execution.
- Native/manual orders hoy se convierten en `execution_result` para compatibilidad; Futures no debe fabricar Operation attribution.

`CONSTRAINT_FOR_D2_07C:` el side-effect owner Futures debe incorporar el journal M2 **antes** del call venue y no heredar la ventana del Execution Agent MT.

## 24. Unresolved evidence gaps

No bloquean el contrato genérico, pero sí pueden bloquear un transport en D2-07B:

- authoritative lookup by exact client identity;
- authoritative negative lookup / consistency delay;
- native idempotency scope y retention;
- stable provider execution id y scope;
- execution history retention/cursor;
- semantics de terminal order history;
- round-trip/truncation rules de client tags;
- completeness de open-order y position snapshots;
- modify/replace atomicity real;
- reconnect event-gap recovery;
- per-program direct API entitlement.

Contradicción documental a integrar por SUBMANAGER:

- D2-04 §2.3 permite wording de synthetic deterministic execution id (incluido `orderId:seq`);
- mandato D2-07A prohíbe inventar dedup identity cuando provider no la entrega;
- este candidate aplica la regla D2-07A y no modifica D2-04. El parent debe alinear el wording antes de freeze global de D2-07.

## 25. Material risks

**R1 — false M2 certification.** Confundir client tag con lookup autoritativo puede duplicar MARKET orders.

**R2 — eventual negative lookup.** “Not found” demasiado temprano puede disparar retry mientras la primera order aún está propagándose.

**R3 — unstable/missing execution identity.** Realtime/history duplicate puede crear Fill doble o perder Fill; V1 debe gatear.

**R4 — hidden SDK retries.** SDK/vendor puede reintentar internamente sin conservar client identity; capability debe documentarlo.

**R5 — history horizon shorter than outage.** Recovery después de una caída larga puede quedar permanentemente ambiguous.

**R6 — split-brain adapter.** Dos side-effect owners sobre una account pueden vencer cualquier dedupe local.

**R7 — stale Position completeness.** Tratar snapshot parcial/stale como flat puede habilitar exposición incorrecta.

**R8 — cancel finality confusion.** Request ACK tratado como final libera capacity prematuramente frente a late fill.

**R9 — hot rebind with live orders.** Consultar el binding actual para recuperar una Order vieja puede buscar/cancelar en el venue equivocado.

**R10 — aggressive journal GC.** Eliminar identity antes de terminar redelivery/recovery horizon reabre duplicate risk.

**R11 — old D1 claims.** Parte del research worker original contiene extrapolaciones que el manager ya corrigió; D2-07B debe usar las manager corrections + first-party claim-level verification.

## 26. Acceptance summary

| Caso | Resultado |
|---|---|
| A Normal MARKET | PASS estructural |
| B Partial fills | PASS estructural |
| C Cancel/Fill race | PASS estructural |
| D Fast MARKET + crash | PASS estructural por M2 journal + reconciliation |
| E Reconnect gap | PASS estructural |
| F Manual order | PASS; physical mismatch, no Operation fabricada |
| G Transport sin M2 proof | PASS; `UNSUPPORTED_FOR_V1_EXACT_SUBMISSION` |
| H Entitlement UNKNOWN | PASS; execution disabled |

No hay blocking evidence para definir el contrato genérico. Los gaps son deliberadamente inputs de D2-07B.

## 27. Files inspected

### Agents-OS

- `main/80-agents/agents-os/agents-os.md`
- `main/80-agents/agents-os/agent-constitution.md`
- `main/80-agents/skills/agents-os-bootstrap/SKILL.md`
- `main/80-agents/skills/agents-os-context-retrieval/SKILL.md`
- `main/80-agents/skills/agents-os-session-close/SKILL.md`
- `main/80-agents/skills/INDEX.md`
- `main/30-resources/agents/domain-router-registry.md`
- `main/30-resources/agents/skills/aranea-agent-dev/SKILL.md`
- `main/30-resources/aranea/07-integration/Echo + Echo Forge — Environment Contract.md`
- `main/10-projects/Echo Futures/Echo Futures.md`
- `main/10-projects/Echo Futures/Echo Futures — D1 Analysis Pack.md`
- `main/10-projects/Echo Futures/Echo Futures — D2-04 Operation Order Fill Position.md`
- `main/10-projects/Echo Futures/Echo Futures — D2-05 Instrument Session Provider.md`
- `main/10-projects/Echo Futures/Echo Futures — D2-06 Market Runtime.md`
- `main/30-resources/futures/EXECUTION TRANSPORT FEASIBILITY — MULTI-PROP EVIDENCE.md`
- `main/30-resources/futures/FUTURES PROP UNIVERSE — AUTHORITATIVE EVIDENCE MATRIX.md`

### Echo

- `v3/sdk/domain/messages.go`
- `v3/sdk/domain/position_snapshot.go`
- `v3/core/internal/functions/execution_store.go`
- `v3/core/internal/functions/position_sync.go`
- `v3/bridge/internal/session/command_consumer.go`
- `v3/bridge/internal/pipe_handler.go`
- `v3/clients/mt4/EchoPersistence.mqh`
- `v3/clients/mt4/execution_agent_v3.mq4`
- `v3/clients/mt5/EchoPersistence.mqh`
- `v3/clients/mt5/execution_agent_v3.mq5`

## 28. Final worker status

```text
D2-07A STATUS:
READY_FOR_SUBMANAGER_REVIEW

NEXT:
SUBMANAGER review only.
Do not start D2-07B/D2-07C/D2-08.
```
