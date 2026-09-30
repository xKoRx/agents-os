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
  - "[[Echo Futures — D2-07A Execution Adapter Contract]]"
  - "[[Echo Futures — D2-07B Transport Selection]]"
  - "[[Echo Futures — D2-07C Execution Runtime Topology]]"
aliases:
  - Echo Futures D2-07
  - EF Execution Runtime
  - EF Futures Bridge
tags:
  - kind/doc
  - area/echo
  - echo-futures
  - architecture-design
created: "2026-09-28"
updated: "2026-09-28"
---

# Echo Futures — D2-07 Execution Runtime

## Propósito

Autoridad única de lectura para D2-07, integrando sin reabrir los tres children aceptados [[Echo Futures — D2-07A Execution Adapter Contract]], [[Echo Futures — D2-07B Transport Selection]] y [[Echo Futures — D2-07C Execution Runtime Topology]]. Responde al scope D2-07 despachado: boundary del execution adapter, command/event integration, capacidades de idempotencia/finality/reconciliación externas, matriz de elegibilidad de transport y recomendación del primer camino V1 no-real-money. Los children quedan como evidence/design depth; ante contradicción de wording histórico, este artifact integrado es la autoridad vigente de D2-07.

No implementa código, no ejecuta ProjectX, no certifica vendors, no elige store del journal, no cierra D2-07 ni D2 global y no abre D2-08.

## 1. Executive verdict

```text
D2-07-R1 STATUS: READY_FOR_MANAGER_REVIEW

BRIDGE DECISION: FUTURES_BRIDGE_SIBLING
INITIAL V1 TRANSPORT CANDIDATE: PROJECTX_DIRECT (recommendation only)
OWNER DECISIONS REQUIRED: OD-D2-07-1 — INITIAL V1 EXECUTION TRANSPORT
```

Los tres children están `ACCEPTED_FOR_INTEGRATION`; sus repairs críticos (R1 de B y la decisión C) son compatibles y la integración no descubrió una contradicción material nueva. El contrato genérico de A, la separación D2/D6 reparada de B y la topología sibling de C se integran en una sola semántica: Core sigue siendo autoridad de `Operation → Order → Fill`; el Futures Bridge es un proceso sibling que aloja el `ExecutionAdapter` como componente interno; el adapter es la frontera de side effects externos con journal M2 write-ahead, y la certificación física del transport seleccionado es trabajo D6.

La recomendación `PROJECTX_DIRECT` no rebaja el contrato: `PROJECTX M2 = NOT_PROVEN`, `REAL_MONEY_CERTIFICATION = NOT_DONE`, y los gaps vendor-specific permanecen como certification gates D6. `NOT_PROVEN` no bloquea el diseño D2 ni autoriza declarar submission física exacta certificada, production safe o real-money ready.

**Corrección del Primary Manager aplicada (normalized event routing):** el wording integrado promovía indebidamente las cinco familias a un único stream `echo.execution-events.v1` con key op-key e ingress directo a `echo/operation`, atribuyendo a la Operation observaciones que no la portan (`PositionObservation`, identidad `(execution_account_id, contract_id)`) o que no son eventos del aggregate (`ExecutionSessionObservation`, runtime/readiness de cuenta/sesión). El artifact congela ahora el routing de **tres caminos** por identidad de la observación (§8, §17): execution facts operation-correlated (`OrderObservation`/`OrderActionObservation`/`Fill` de una Order Echo) → execution-events → `echo/operation`; `PositionObservation` → camino physical position/reconciliation; `ExecutionSessionObservation` → camino runtime/readiness account-scoped, jamás con `operation_id` fabricado y jamás como fact de Operation. Ningún otro cambio arquitectónico; `OD-D2-07-1` sigue pendiente.

Baselines: Agents-OS **integration baseline** `b45e9328c0217e77c4f91103bb5f3a422d9cd5b6` — HEAD verificado al **inicio** del worker de integración, no el estado final persistido. La integración se persistió después en `363849568383bda8dddbe9fb6ded447e15590210` y el cierre de esa sesión quedó en `89120c64cd59719949a7af495b0a75355e18d686`; el HEAD final de esta corrección (D2-07-R1) es un SHA distinto y posterior, registrado en el handoff de sesión. Echo `xKoRx/echo@372af59a7b83604781346613da01e3d510ea1360` — los tres children la verificaron sin delta; por regla de integración no se re-auditó source salvo necesidad de contradicción, y no surgió ninguna.

## 2. Scope / authorities

**En scope:** frontera genérica de ejecución, decisión Bridge/Adapter, topología runtime conceptual, modelo de comandos del adapter, event model normalizado, boundary M1/M2, submission journal, finality, readiness, reconnect/reconciliación, ownership de side effects, cardinalidad proceso/sesión/cuenta, routing Kafka, cambios de binding en caliente, degraded close, separación SimExecution, comparación compacta de transports, recomendación inicial V1, reuse map V3, gates D6, escala y acceptance cases.

**Fuera de scope:** implementación física, store del journal, certificación M2 vendor, validación demo/shadow autorizada, benchmarks de capacidad, cierre de OD-D2-07-1, D2-08 y cierre global D2.

Jerarquía de autoridades consumidas:

1. [[Echo Futures]] — decisiones owner D2-01..03 y estado D2.
2. [[Echo Futures — D2-04 Operation Order Fill Position]] — Operation/Order/Fill/Position, M1/M2, correlación adapter-owned (§8.2), recovery authority.
3. [[Echo Futures — D2-05 Instrument Session Provider]] — Provider/Program/RuleSet, `ProviderAccountBinding`, transport entitlement, DayBoundary, admission/capacity/safety.
4. [[Echo Futures — D2-06 Market Runtime]] — separación market runtime / execution transport.
5. D2-07A — contrato del adapter (autoridad inmediata de §6–§12 de este artifact); sus 14 constraints a C son vinculantes y quedan integradas.
6. D2-07B — comparación de transports, separación D2/D6, gaps como gates D6.
7. D2-07C — topología física conceptual, sibling, ownership, routing, reuse map.

Children congelados para esta integración: D2-07A congela la frontera Bridge/Adapter, una sola domain Order, M1 vs M2, durable write-ahead submission intent, no blind retry, AMBIGUOUS fail-closed, finality venue-authoritative, immutable partial/multi-fill, Position = Account + Contract, static eligibility ≠ dynamic readiness, reconnect = recovery nunca resubmit, y no synthetic/heuristic execution identity. D2-07B congela (post-repair R1) `PROJECTX_DIRECT = recommended initial non-real-money implementation candidate`, no Owner freeze, no M2-certified, no real-money-certified. D2-07C congela `FUTURES_BRIDGE_SIBLING` con Bridge = process/runtime shell y ExecutionAdapter = componente interno transport-specific, sin `ExecutionAdapterHost`.

## 3. Aclaración D2-07-R1 — execution identity

D2-04 §2.3 contiene wording antiguo demasiado permisivo que admite "sintetizar un execution id determinístico en el adapter (ej. `orderId:executionId`, `orderId:seq`)". Para D2-07 rige la regla más estricta del SUBMANAGER: **no heuristic/synthetic execution identity for correctness**. Prohibidos como sustituto de una identidad nativa de ejecución estable: `orderId:seq`, secuencia local, precio/tiempo/qty, hash de timestamps, arrival index. Una composición como `account_id + provider_execution_id` es válida sólo si `provider_execution_id` ya es una identidad nativa estable del venue.

Los tres children ya aplican esta regla (A §10, B §10, C sin sintéticos). Este artifact **no modifica D2-04**: registra la aclaración y la exporta al Primary Manager para alinear el wording de D2-04 §2.3 antes del freeze global de D2, igual que los children lo dejaron señalado. El dedup key canónico vigente es `(execution_account_id, provider_execution_id)` con `provider_execution_id` de origen nativo; un transport sin esa capability queda incompatible con V1 exact execution semantics.

## 4. Generic execution boundary (target architecture)

```text
Strategy/MM
   ↓
Core / Operation  (echo/operation, key account:strategy)
   ↓
normalized Order command  (SubmitOrder / modify / cancel D2-07A §5)
   ↓
Kafka  (comandos account-isolated, egress EXACTLY_ONCE M1)
   ↓
Futures Bridge  (process/runtime shell)
   ↓
ExecutionAdapter  (componente interno transport-specific, journal M2)
   ↓
Platform / Venue
```

Retorno:

```text
Platform / Venue
   ↓
ExecutionAdapter
   ↓
Futures Bridge
   ↓
normalized execution observations  (cinco familias D2-07A §9)
   ↓
Kafka  (echo.execution-events.v1, key op key)
   ↓
Core / Operation
```

Market Runtime permanece separado (D2-06): el adapter no es autoridad de barras, replay ni logical market stream. El Bridge nunca es autoridad de dominio: no posee Strategy, MM, reglas provider, sizing, rollover ni lifecycle; su única "verdad" local es el journal M2 y las observaciones físicas. La correlación evento→operación es adapter-owned (D2-04 §8.2): los eventos llegan a `echo/operation` ya correlacionados con `operation_id` + `order_id`, sin función router en Core.

## 5. Futures Bridge decision

```text
FUTURES_BRIDGE_SIBLING
```

La ejecución futures vive en un proceso propio (nombre conceptual `v3/futures-bridge`; naming final = decisión de implementación D4/D6) que reutiliza patrones y librerías del Bridge V3, no extiende `v3/bridge`. Motivación principal (C §5, con evidencia física en baseline): el Bridge V3 es Windows-only por Named Pipes y su transporte/handshake/journal son semántica MetaTrader (pipe manager, registro EA vía HTTP, detransform broker-symbol, snapshots por ticket, `ExecutionResult` single-result, journal EA post-side-effect); extenderlo acoplaría crash domains, deployment, release cadence y hosts incompatibles; deformaría el path MetaTrader estable; y aislar failure/deployment/release domains exige el sibling. Los patrones reutilizables (sesión per-account, topic dedicado, pause/resume, circuit breaker, kache/notifier, readiness signals, telemetría, convenciones ETCD) son pequeños y se re-implementan en cientos de líneas; se reutilizan `v3/sdk/*` tal cual sin fabricar un framework universal.

**La decisión NO depende de ProjectX.** ProjectX es un candidate de adapter; la razón ontológica del Futures Bridge es la incompatibilidad física y semántica entre el edge MT y cualquier familia de ejecución network-native o desktop-hosted futura. Los dos extremos prohibidos quedan fuera: no se copia el Bridge entero y no se convierte `v3/bridge` en framework universal de execution edges.

## 6. Runtime topology

```text
                     Core (StateFun, Linux/Aranea)
                     echo/operation  key account:strategy
                        │  egress EXACTLY_ONCE (M1)
                        ▼
        echo.order-commands.{execution_account_id}.v1   (candidate name, §17)
                        │
                        ▼
   ┌──────────────────────── Futures Bridge (1 proceso) ───────────────────────┐
   │  config/kache · session registry per account · command consumers          │
   │  telemetry · health · normalized-event egress · M2 journal (per binding)  │
   │                                                                            │
   │  ExecutionAdapter (instancia por account/binding)                          │
   │   ├─ SimExecutionAdapter            (sim, sin credenciales)                │
   │   ├─ DirectNetworkAdapter           (ProjectX: HTTP/WebSocket → venue)     │
   │   └─ DesktopHostedAdapter           (futuro: conector + componente         │
   │                                      platform-side dentro del desktop)     │
   └────────────────────────────────────────────────────────────────────────────┘
                        │  echo.execution-events.v1 (key=op key, correlacionado)
                        │  echo.position-observations.v1 (key=account, shape neto)
                        ▼
                     Core (ingress → echo/operation / proyección Position)
```

**Bridge = shell** (bootstrap/config ETCD, sesiones per-account, consumo Kafka, egress de observaciones, telemetría, health). **ExecutionAdapter = componente interno transport-specific** que implementa D2-07A: secuencia de submit con `PREPARED/SUBMITTING` durables antes del point-of-no-return, resolución de ambiguos, cinco familias de eventos, finality evidence, reconnect sequence, capability declaration. **No existe `ExecutionAdapterHost` como servicio extra ni cuarto servicio**: si hace falta nombrar el rol que aloja adapters, es un rol del propio Bridge; en la familia desktop-hosted el componente platform-side (análogo al EA MetaTrader) es parte del adapter, sin identidad de dominio propia.

La ventana M2 del legado quedó confirmada físicamente por C (MT5 valida journal **antes** de `g_Trade.Buy/Sell` y persiste **después**; MT4 igual): el runtime Futures no hereda esa forma — el journal write-ahead vive en el bridge, antes del point-of-no-return.

## 7. Adapter command model

Integra D2-07A §5. El boundary parte de la Order de D2-04; el adapter nunca crea una segunda entidad Order de dominio. Submit mínimo:

```text
SubmitOrder {
  client_order_id               # = order_id D2-04; identity key M2
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

`operation_id`/`order_id`/`client_order_id` son correlation only; el resto es input de traducción al venue. **No se agregan campos vendor-specific al contrato Core**: customTag/clOrdId y equivalentes son mecanismos físicos del adapter, elegidos en D6. Antes del point-of-no-return quedan pinneados en el journal: `transport_id`, provider external account identity, `external_contract_identifier`, términos completos de la Order y la identidad del command/action. Modify/cancel usan action identities estables propias (`replace_request_id`, `cancel_id`); un redelivery mantiene el mismo action id. Si el transport sólo soporta cancel+replace y D2-04 requiere replacement Order nueva, **Core proporciona el nuevo `order_id/client_order_id`**; el adapter posee la coreografía física, no la identidad de dominio.

## 8. Normalized event model

Cinco familias semánticas canónicas (D2-07A §9); ningún DTO vendor-specific ni `ExecutionResult` legacy como contrato Futures canónico:

```text
OrderObservation             # status/venue-state de la Order, source REALTIME|RECONCILIATION|HISTORY
OrderActionObservation       # modify/cancel/replace: action_id, kind, outcome, evidence
Fill                         # hecho físico inmutable
PositionObservation          # observación neta (account, contract)
ExecutionSessionObservation  # conexión/auth/binding/event-stream/reconciliation/readiness
```

**Fill es inmutable; partial/multi-fill first-class; Fill puede preceder al Order ACK** (un MARKET puede llenar antes del ACK; el Fill es la primera evidencia autoritativa y el Order state se reconstruye desde fill/history — nunca se descarta ni retrasa esperando "orden bonito"). BUY 3 con executions `+1,+1,+1` produce tres Fill facts y una sola Order; `filled_qty`/avg son derivados de Core.

Alineación con D2-04 (nota de integración): el `status` de `OrderObservation` es una **observación del venue**; el estado del aggregate Order en Core sigue siendo el de D2-04 §3.2 (`PENDING_SUBMIT/SUBMITTED/WORKING/FILLED/REJECTED/CANCELLED/EXPIRED`, partial fill = `WORKING` con `filled_qty > 0`). Un `PARTIALLY_FILLED` de observación se materializa en Core como `WORKING` + fills; no se crea un estado de aggregate nuevo. Las familias de eventos entran por las guards monótonas e idempotentes de D2-04 (I7/I15); el `ExecutionSessionObservation` es runtime, no evento del aggregate. La actividad venue sin origen Echo va a observación/proyección, jamás al state owner.

## 9. M1 / M2 boundary

Dos boundaries con garantías distintas que nunca se mezclan (D2-04 §5.6):

**M1 — Core state ↔ command publication:**

```text
StateFun state  +  transactional Kafka command egress  =  EXACTLY_ONCE boundary
```

Con `EXACTLY_ONCE` declarado en el egress (transacción commiteada atómicamente con el checkpoint, garantía documentada de Flink StateFun 3.2; config de SPEC, no comportamiento demostrado del baseline), ningún comando físico escapa sin estado Core commiteado. M1 **no cubre el venue**.

**M2 — Kafka command ↔ physical external side effect.** No es exactly-once por Kafka, `command_id`, ACK local ni registro PENDING. Requiere:

- durable **PREPARED** intent completo antes del point-of-no-return;
- **SUBMITTING** persistido antes del primer paso que puede alcanzar al venue;
- **stable client identity** (`client_order_id` invariante por retry/reconnect/restart/redelivery);
- **authoritative reconciliation** por lookup/history por client identity o **native idempotency** documentada, capaz de responder tras crash/timeout si la identidad existe, ejecutó o fue terminal;
- **no blind retry**: tras cualquier posibilidad de side effect, retry físico sólo es legal si la idempotencia nativa lo hace seguro con la misma key o si la reconciliación autoritativa demuestra ausencia;
- **ambiguity preserved**: si no puede probarse existencia ni ausencia, `AMBIGUOUS` → fail-closed, nueva exposición bloqueada, sin resultado fabricado.

Prohibido usar Kafka offset, Core PG o process memory como physical truth (D2-07A I6). El outcome incierto se trata como `MAY_HAVE_EXECUTED`. Un transport/order-class que no cierra M2 queda `UNSUPPORTED_FOR_V1_EXACT_SUBMISSION`, gated, no aproximado.

## 10. Submission journal

Estados mínimos (D2-07A §7.2):

```text
PREPARED      # intent completo durable; side effect aún no autorizado
SUBMITTING    # point-of-no-return habilitado/cruzable; outcome puede ser desconocido
VENUE_BOUND   # existencia física demostrada y provider identity/status reconciliable
TERMINAL      # venue execution finality demostrada y fills requeridos reconciliados
AMBIGUOUS     # no puede demostrarse verdad suficiente; fail-closed / operator resolution
```

**Authority:** la durability domain del side-effect owner — en la topología vigente, el execution edge del Futures Bridge/adapter, co-localizado con el adapter instance que ejecuta el binding (condición para que write-before-side-effect sea real). **Tecnología concreta: `DEFERRED_TO_D6`** (store durable local detrás de interface, single-writer; no se congelan SQLite/Postgres/RocksDB). **Core PG prohibido como M2 recovery authority; Kafka prohibido como journal primario.** El journal pinnea binding físico, términos completos, action ids, provider refs, cursors de reconciliación y ambigüedad reason; debe sobrevivir restart, redelivery, fast fill y lost ACK.

Notas de integración: (1) la PK conceptual de dedup `(execution_account_id, client_order_id)` de D2-07A §7.1 se mantiene como clave de dedup; D2-07C la refina registrando que la identidad física del journal es **por binding** (el pin de transporte vive dentro del record), lo que permite coexistencia de durabilities durante un hot rebind sin cambiar la clave de dedup. (2) GC: nunca GC `AMBIGUOUS`; `TERMINAL` sólo se compacta cuando la terminalidad ya está durable downstream, la ventana de redelivery ya no puede reintroducir la identidad (o queda tombstone) y el horizon nativo no fue sobrepasado; V1 prefiere tombstone compacto antes que GC agresivo. (3) Restart: al arranque se cargan primero todos los records no `TERMINAL` y ninguno se reenvía antes de reconciliación.

## 11. Finality

La finalidad es venue-authoritative y exige evidencia (D2-07A §16); ningún enum local ni request ACK la declara. Estados de finalidad (`WORKING/PARTIAL/FILLED/REJECTED/CANCEL_PENDING/CANCELLED_CONFIRMED/EXPIRED_CONFIRMED/MODIFY_REPLACE_PENDING/TERMINAL_EXECUTION_FINAL/AMBIGUOUS`) son adapter/journal/finality state, no todos `Order.status`. Puntos congelados: un MARKET `FILLED` candidate requiere además recuperar/deduplicar los Fill facts que explican la cantidad; `REJECTED` es terminal sólo si la respuesta es contractualmente autoritativa de "no order accepted" (timeout/red/5xx no son reject físico); cancel final espera reconciliar los fills que pudieron ganar la race; modify/replace final exige estado venue autoritativo con los nuevos términos. **Core libera reservation/terminaliza Operation sólo con evidence `TERMINAL_EXECUTION_FINAL` compatible con D2-05**, nunca por `cancel requested`. Un Fill nuevo estable posterior a un "cancelled confirmed" siempre se conserva y corrige forward el estado derivado (única corrección forward D2-04).

## 12. Readiness

Static eligibility ≠ dynamic readiness (D2-07A I13/I14). Static (por ProviderProgram, D2-05): transport entitlement ALLOWED ∧ capabilities satisfacen el comportamiento Order/MM requerido ∧ contrato M2 satisfecho para las order classes requeridas; `UNKNOWN != ALLOWED`; platform support, automation permission, API entitlement y technical capability son cuatro claims separados.

Dynamic readiness mantiene siete dimensiones (connection, authentication, account_binding, order_event_stream, reconciliation_authority, position_state, submission_capability). `EXECUTION_READY_NEW_RISK` sólo cuando eligibility static ELIGIBLE ∧ connected ∧ authenticated ∧ provider account bound/verified ∧ event stream LIVE ∧ reconciliation authority AUTHORITATIVE ∧ sin ambigüedad M2 no resuelta ∧ position snapshot FRESHA/suficientemente completa ∧ submit capabilities EXACT_READY. **Socket connected ≠ ready; command consumption saludable con venue unhealthy no es ready.** Degradaciones (history/lookup, event stream, position stale, socket down, ambiguous sin resolver) apagan NEW_RISK a nivel cuenta (KISS V1). CLOSE/REDUCE puede conservar gate separado sólo si el adapter demuestra target identificable, acción no-aumentadora-de-riesgo bajo la semántica disponible y finality suficiente; si no, la acción automática se bloquea y escala a operator/safety — nunca "close success" porque se encoló un command.

## 13. Reconnect / reconciliation

**Reconnect = recovery, nunca resubmit** (I12). Después de reconnect/restart: `NEW_RISK = OFF` hasta completar la barrier completa por cuenta (D2-07A §17): autenticar → verificar physical account binding → restablecer event subscriptions → cargar journal no-terminal → resolver cada `PREPARED/SUBMITTING/VENUE_BOUND/AMBIGUOUS` por client identity/native idempotency/history → listar/reconciliar open Orders y detectar desconocidas → recuperar execution history/missed Fills desde cursor/horizon con dedup por provider execution identity → obtener fresh Position autoritativa → emitir missed normalized observations → contrastar físico vs lógico y surfaciar mismatches. **No existe "on reconnect → replay pending commands".** Las Orders working durante la desconexión se recuperan como physical state, sin duplicar ni cancelar automáticamente. Sólo tras la barrier se re-evalúa readiness, y `EXECUTION_READY_NEW_RISK` exige además que la static eligibility D2-05 (entitlement/RuleSet/DayBoundary) lo permita. Consumo de comandos reanudado ≠ readiness.

## 14. Position / manual activity

`PositionObservation` es shape neto `(execution_account_id, contract_id, net_qty, avg_price, as_of, source, snapshot_scope)` — D2-04 R8 — sin `operation_id` ni attribution de Strategy; una snapshot completa puede usar ausencia como evidencia de flat sólo si el transport declara completeness explícita para ese scope/as_of. Actividad física no correlacionable con Echo (orden manual, SDK externo, liquidación del provider): se preserva la physical observation, se calcula `POSITION_MISMATCH`/reconciliation debt, se marca la cuenta degraded/alertable según severidad y **jamás se crea Operation/Fill Echo por inferencia de delta de Position** (I9/I10). Si reconciliation posteriormente demuestra que la actividad pertenece a un `client_order_id` Echo, recién entonces se emiten los canonical facts con identidad real. Se mantiene la separación logical vs physical truth de D2-04; `DT-EF-POSITION-RECONCILIATION-05` sigue diferida.

## 15. Side-effect ownership

**Single active side-effect authority per `(execution account, physical binding)`.** La asignación cuenta→bridge instance es configuración (binding plane), no emergente de Kafka. **V1: NO AUTOMATIC CROSS-HOST TAKEOVER.** Crash se recupera in-place (mismo host, mismo journal durable, mismo binding físico + reconciliación venue — seguro por diseño). Migrar el binding a otro host es acción operacional explícita: el host anterior se detiene primero, el nuevo arranca con el mismo journal y ejecuta la secuencia de recovery completa. **Fail-closed antes que falso HA.**

`Kafka ownership != physical fencing`: un consumer group vivo no impide que un proceso particionado side-effectee; session generation/epoch permite **detectar** owners stale (discrepancia visible, NEW_RISK off) pero no afirma que pueda detener mágicamente a un owner particionado con alcance al venue; la contención física la previene la regla de instancia única + operador. Doble proceso sobre la misma cuenta = config error detectable (misma cuenta en dos instancias, consumers duplicados observables, telemetría de doble-owner, generation del journal). Fencing technology real queda deferred.

## 16. Process / session / account cardinality

Core ignora la cardinalidad física: el topic per-account y el keying por cuenta hacen invisible cuántos bridges/procesos existen. La topología permite `1 Bridge process → N accounts/sessions` cuando el transport lo permite (familia network: una sesión ProjectX addressa N cuentas) y `1 process/session → 1 account` cuando el transport lo exige (familia desktop: una instancia por terminal/proceso). Identidades separadas, jamás colapsadas:

```text
Bridge instance             # proceso desplegado; no identifica negocio
ExecutionAdapter instance   # configuración/vivencia de una familia dentro del bridge; no identifica negocio
transport session           # conexión autenticada efímera (epoch); cambia en reconnect
Echo execution_account_id   # identidad de routing/dominio
provider external account   # identidad que el venue autentica/observa; verificada contra binding
```

La session identity cambia al reconnect; `client_order_id`, provider binding y journal no. Adapter process identity ≠ business identity.

## 17. Kafka routing

Se congela la **propiedad semántica**: `account-isolated command routing` — una familia de topics de comandos aislada por execution account, distinta del stream legacy, con egress account-keyed desde Core y orden por key/partición. **No se convierte el nombre exacto en owner decision**: el candidate name de C (y ya presente en D2-04 §8.3) es

```text
echo.order-commands.{execution_account_id}.v1   # IMPLEMENTATION CANDIDATE, no domain invariant
```

mientras el legado MT conserva `echo.commands.{execution_account_id}.v1` intacto (convención física vigente: `mm_engine.go:586`, `close_handler.go:369`). Familia nueva, no topic compartido: el payload Futures (`SubmitOrder`/modify/cancel) tiene semántica y requisitos de consumo distintos (`read_committed`, sin TTL-on-delivery, commit tras outcome/journal); mezclar ambos streams obligaría a versionar el payload en el stream que consume el legado. El nombre físico final queda a ratificación técnica ordinaria del manager en implementación (misma disposición que D2-04 para nombres físicos).

Garantías de routing: el bridge consume sólo las cuentas de su config/binding con validación defence-in-depth `payload execution_account_id == session account`; key/account/topic/journal en la misma identidad; **no transport branching en Core** — la resolución de transporte vive en la config del `ProviderAccountBinding` (D2-05); redelivery ≠ physical retry (el commit del side effect es el journal, nunca el offset). No se crean topic por Order, topic por transport ni function type por vendor.

**Retorno normalized:** familia `echo.execution-events.v1` (nombre por D2-04 §8.3; semántica congelada: cinco familias, key = op key, ingress directo a `echo/operation`, eventos ya correlacionados con `operation_id`+`order_id`) + `echo.position-observations.v1` (key account, shape neto). Los DTOs legacy (`ExecutionResult`/`CloseResult`/`PositionSnapshot`) no se promueven al camino futures; coexisten para el legado.

## 18. ProviderAccountBinding hot changes

Autoridad D2-05; semántica integrada (A §19 + C §16): `ProviderAccountBinding` re-bindea in-place con audit facts; `AccountStrategy` no gana transport fields; el adapter recibe un execution account binding, no una Strategy binding. **New submissions → new binding only after readiness** del nuevo (y sólo si static eligibility lo autoriza). **Las Orders físicas existentes stay pinned al original physical binding** hasta terminal/reconciliation: recovery de esas Orders continúa contra el transport/provider account original; **no live migration, no silent remap**. El runtime conserva la recovery information del binding anterior (journal + session generation de ese binding) aunque la Account ya tenga otro current binding — la identidad del journal es por binding (§10). Old inaccessible transport = **recovery debt / operator action**, no remap silencioso. Entitlement revocado: deny new risk + suspensión de emisión + operador (D2-05), sin auto-force-close salvo regla explícita; close/reduce sigue el gate conservador de §12.

## 19. Degraded close / safety

ForceClose/termination mientras el edge está DOWN: el **intent remains pending, not terminal** (D2-04 R3: ForceClose es intent, no transición instantánea), con alert/readiness degraded visibles vía `ExecutionSessionObservation`. Recovery: **reconcile first, then continue termination** — al recuperar el edge, la secuencia de barrier (§13) corre primero y recién después continúa la termination hacia guards; TERMINAL sólo cuando `exposure==0 ∧ 0 live orders ∧ intent` (guards D2-04). **No synthetic close success**; **no automatic emergency adapter switch** — sólo un diseño futuro explícito podría introducirlo. El gate CLOSE/REDUCE degradado sigue §12.

## 20. SimExecution separation

Dos usos que no se mezclan:

**Domain/backtest `SimExecution`** — el execution determinístico puro ya contemplado por D2-04 §8.7 para deterministic testing/backtest: vive en el paquete de dominio puro, implementa el mismo contrato `ExecutionEvent`, corre `Signal → Operation → MM → Order → Fill` sin Kafka/StateFun para el backtester futuro.

**Bridge seam `SimExecutionAdapter`** — componente mínimo dentro del futures-bridge que ejercita el seam completo `Core → Kafka → Futures Bridge → Adapter → observations → Core` sin credenciales externas. Puede simular ACK, reject, fills, partial fills, cancel, modify, reconnect y ambigüedad (crash post-SUBMITTING sin outcome). **No se convierte en exchange simulator completo ni en backtester.** Requisito: la simulación de ambigüedad debe ejercitar el journal + recovery real del bridge (no atajos in-memory), porque ese es exactamente el código que D6 certificará con un transport real. V1 puede comenzar con `SimExecutionAdapter + 1 real adapter en D6` y nada más.

## 21. Transport comparison (compacta)

```text
ProjectX Direct
- recommended first non-real-money candidate
- direct API / low Desktop coupling
- Topstep simulated path (Trading Combine + Express Funded; Practice = cert env, no ProviderProgram)
- M2 vendor certification deferred D6 (customTag retention, ambiguous-submit atomicity,
  authoritative negative/recovery, Trade id scope/stability, history horizon)
- Live Funded excluded from this path

NinjaTrader Desktop
- broader Desktop integration potential
- not preferred first generic path (current-session executions only, OrderId mutable/no único)
- recovery/identity limitations; future provider-specific adapter requeriría prueba propia

Tradovate / Rithmic / CQG
- future adapter candidates
- certify only if selected (transport-specific D6 certification; CQG = strongest contrast
  evidence target: cl_order_id scoped, trade_id único por cuenta, history 30d)
```

Child B queda como evidence depth completa (capability matrix, first-party evidence register con fechas/URLs, entitlement constraints). Separación preservada: platform support ≠ API entitlement; "has simulator" ≠ ProviderProgram entitlement ni real-money authorization.

## 22. Initial V1 recommendation

```text
PROJECTX_DIRECT
=
recommended initial non-real-money implementation candidate

semantics:
recommendation only
first non-real-money implementation candidate
not transport certification
not real-money authorization
not Owner freeze
```

Sostenida únicamente con evidencia ya aceptada: API directa con submit/modify/cancel, observaciones realtime de orders/trades/positions, Topstep Trading Combine + Express Funded Account como ProviderPrograms simulados dentro del path aceptado, menor coupling operativo inicial que Desktop, y el Core sin volverse ProjectX-specific (el transport queda detrás del boundary Adapter/Bridge). La integración NO toma la decisión por el Owner (§28).

## 23. Echo V3 reuse / adapt map

```text
REUSE:
v3/sdk/*  (messaging, telemetry, kache, etcd, di; DTOs domain como wire legacy)
telemetry/config conventions  (OTel + semconv + trace propagation; namespace futures-bridge/*)
account-isolated session/consumer patterns  (topic per-account, pause/resume, circuit breaker, retry FIFO)
bootstrap DI/config/run-shutdown shape  (repetido pequeño en el sibling)
batch publishing pattern  (para observaciones normalizadas propias)

ADAPT:
bootstrap/session lifecycle  (semántica idéntica desacoplada de pipes)
health/readiness  (añadir execution-readiness surface por cuenta; gate "socket" se queda corto)
Kafka consumer behavior  (read_committed, sin TTL-on-deliver, dispatch al adapter con
                          journal write-ahead, commit tras outcome/journal)

MT_ONLY:
Named Pipes / pipe manager / pipe handlers
EA HTTP registration
MT symbol mapping semantics  (detransform broker-symbol)
ticket PositionSnapshot
ExecutionResult / CloseResult
EA command journal  (SlaveCommandJournal post-side-effect; su deuda M2 es la razón
                     por la que el path MT no se reutiliza como M2)

REPLACE_FOR_FUTURES:
M2 journal semantics  (write-ahead en el bridge, antes del point-of-no-return)
normalized execution events  (cinco familias; sin ExecutionResult single-result)
Position Account+Contract shape  (PositionObservation neta, no ticket-level)
```

No se crea shared framework prematuro: día 1 se comparte sólo lo que ya es librería (`v3/sdk/*`); las piezas bridge-internal pequeñas (session/consumer/breaker/readiness) se duplican KISS en el sibling; prohibidos bridge-framework, plugin-runtime, generic-adapter-sdk, dynamic adapter loader, adapter marketplace. La extracción se reconsidera con un tercer consumidor real o cuando una corrección tenga que replicarse más de una vez.

## 24. D6 certification gates

`PROJECTX M2 = NOT_PROVEN` no bloquea D2-07, pero antes de habilitar ProjectX —o cualquier transport— para exact physical submission en un environment implementado, D6 debe cerrar en el transport realmente seleccionado (sólo el seleccionado; no pre-certificar todo el universo):

ProjectX gates específicos (conservados del repair B):

1. **customTag retention / uniqueness scope** — cuánto sobrevive la unicidad tras terminal/fill y a través de reconnect/restart.
2. **Ambiguous-submit retry atomicity** — que un outcome desconocido no pueda terminar en blind retry ni en dos órdenes ejecutables; atomicidad real del reuse de customTag.
3. **Authoritative negative / recovery semantics** — cuándo "no existe" es autoritativo o qué mecanismo nativo evita depender de lectura eventualmente consistente.
4. **Execution identity** — scope y estabilidad del Trade id entre realtime e history/reconnect (bajo D2-07-R1).
5. **History horizon** — horizonte usable o máximo outage tras el cual el adapter permanece AMBIGUOUS/not-ready.

Gate genérico por transport (B §21): durable M2 implementation antes del point-of-no-return; stable client identity behavior/retention/scope; ambiguous submit recovery sin blind retry; exact execution identity y scope; history/recovery horizon y semántica autoritativa; reconnect/resubscribe y gap recovery; terminal finality incluyendo cancel/fill y late-fill edges; ProviderProgram/account entitlement del environment concreto; authorized host/environment constraints (Topstep: dispositivo personal del trader, sin VPS/VPN/relay); validación E2E shadow/demo/sim autorizada. También config: egress EXACTLY_ONCE + `read_committed` (carry D2-04 R2), store del journal con fsync/corruption semantics (C R1).

## 25. Scale implications

**No se certifica 100–200 accounts.** Se congela sólo que la topología no impide el scale estructuralmente: un solo proceso bridge hostea N adapter instances/sessions y Core ve cuentas, no procesos; el coste de ejecución es per `(cuenta×binding)` sin multiplicar market state por cuenta (D2-06). Pressure points identificados sin certificar; **D6 debe benchmarkear**: overhead de consumer-per-account (consumer groups/topics lineales en cuentas), journal I/O append-only por binding, reconnect storm (reconciliación por cuenta rate-limited/escalonada), límites de sesiones/credenciales por transport, adapter/provider rate limits, y cardinalidad de procesos desktop en familia desktop-hosted (1 por terminal). Alternativa de partición compartida keyed-by-account es cambio local de routing, no de boundary.

## 26. Acceptance cases

| Caso | Escenario | Resolución integrada |
|---|---|---|
| A | Normal MARKET | Order Core → M1 egress exact → PREPARED/SUBMITTING durables → single venue submit → ACK o Fill → VENUE_BOUND → canonical Fill a la Operation correcta (key op key) → finality. Una sola physical order. |
| B | Partial fills | BUY 3 con `+1,+1,+1`: tres immutable Fills por `provider_execution_id` nativo; una Order/una Operation; filled/avg derivados; sin colapso a ExecutionResult. |
| C | Cancel/fill race | `cancel_id` durable → request; el Fill que gana la race se conserva; cancel ACK no libera reservation; history/order state demuestra remaining=0/cancelled y executions cubiertas → finality; late fill posterior se dedup/aplica igual. |
| D | Fast MARKET + crash | Redelivery encuentra journal `SUBMITTING` → resolución obligatoria contra venue por la misma `client_order_id` → converge (found → adopt outcome; authoritative-absent → retry legal; ni-ni → AMBIGUOUS fail-closed). No blind retry, no segunda order. |
| E | Reconnect + missed Fill | `NEW_RISK OFF` → barrier completa; history/reconciliation recupera el execution con identity estable; dedup realtime/history; `EXECUTION_READY_NEW_RISK` sólo tras barrier + eligibility D2-05. |
| F | Manual/unknown activity | Observación física + `POSITION_MISMATCH`/debt; nada entra a `echo/operation` como Fill Echo; Operation nunca fabricada. |
| G | ForceClose con Bridge down | Termination pending, not terminal; alert/degraded; al recuperar: reconcile first → continuar termination → TERMINAL sólo por guards; sin synthetic success ni emergency switch. |
| H | Hot binding change | Submissions nuevas → binding nuevo tras readiness; Order viva pinneada al binding original con journal/recovery de ese binding; sin live migration ni silent remap; transporte viejo inaccesible = recovery debt/operador. |
| I | Multi-account runtime | Topic/consumer/sesión/journal por cuenta; fallo de sesión de A no alcanza a B (validación payload + journals por binding); cardinalidad invisible a Core. |
| J | Transport sin exact recovery | Capability gated: sin lookup/history/client correlation suficiente para resolver ambiguity, la order class queda `UNSUPPORTED_FOR_V1_EXACT_SUBMISSION`; gate demostrado en D6 antes de cualquier deployment exact. |
| K | ProjectX simulated candidate | Recomendación válida como first non-real-money candidate sin convertirlo en certified: M2 NOT_PROVEN, gates D6 §24, Live Funded excluido. |
| L | Platform support ≠ API entitlement | Separación preservada en eligibility static: soporte de plataforma/automation permission/API entitlement/technical capability son claims separados; UNKNOWN ≠ ALLOWED. |

## 27. Residual risks

- **R1 false M2 certification:** confundir client tag con lookup autoritativo puede duplicar MARKET orders (gate D6, §24).
- **R2 eventual negative lookup:** "not found" demasiado temprano puede disparar retry mientras la primera order propaga.
- **R3 unstable/missing execution identity:** realtime/history duplicado puede crear Fill doble o perdido; gated por D2-07-R1.
- **R4 hidden SDK retries:** el vendor puede reintentar internamente sin conservar client identity; capability debe documentarlo.
- **R5 history horizon < outage:** recovery tras caída larga puede quedar permanentemente ambiguous (fail-closed correcto, pero operacionalmente costoso).
- **R6 split-brain residual:** la regla NO AUTOMATIC TAKEOVER no impide físicamente que un operador arranque dos instancias; mitigación = validación config + telemetría doble-owner + generation; fail-visible, no infalible. Proceso particionado con alcance al venue sigue siendo riesgo operacional acotado (C R3).
- **R7 stale/partial Position completeness:** tratar snapshot parcial/stale como flat puede habilitar exposición incorrecta.
- **R8 cancel finality confusion:** request ACK tratado como final libera capacity prematuramente frente a late fill (C-R2/C-R3 de D2-05 permanecen: `PENDING_FINALITY` hasta venue final).
- **R9 hot rebind con live orders:** consultar el binding actual para recuperar una Order vieja puede tocar el venue equivocado (journal per binding + pin lo previenen).
- **R10 aggressive journal GC:** eliminar identidad antes del horizon de redelivery/recovery reabre duplicate risk (tombstone preference).
- **R11 journal durability real:** "durable" depende del store D6 (fsync/corruption); la corrección de D2 lo asume.
- **R12 divergencia de duplicados V1:** las piezas duplicadas session/consumer/breaker pueden divergir del legado; aceptado bajo la regla de re-extracción de §23.
- **R13 Topstep deployment violation:** un adapter ProjectX técnicamente correcto desplegado como relay/VPS violaría la constraint de order flow documentada (host placement = D6).

## 28. Owner decision

Sobrevive exactamente una decisión owner:

```text
OD-D2-07-1 — INITIAL V1 EXECUTION TRANSPORT

Candidate recomendado: PROJECTX_DIRECT
Semántica: recommendation only
           first non-real-money implementation candidate
           not certification
```

La integración NO toma la decisión por el Owner. `OD-D2-07-1` no cierra en este artifact; es el único owner decision pendiente de D2-07 y no bloquea manager review.

## Fuentes

- [[Echo Futures]] — estado D2-07 dispatch, decisiones D2-01..06, handoffs D2-07A/B/C.
- [[Echo Futures — D2-04 Operation Order Fill Position]] — M1/M2, §8.2 correlación adapter-owned, §8.3 topics, §9 Bridge = REUSE patrones/adapter nuevo, §2.3 wording bajo aclaración D2-07-R1.
- [[Echo Futures — D2-05 Instrument Session Provider]] — ProviderAccountBinding/transport entitlement/DayBoundary, reservation finality, `Account.execution_binding_id`.
- [[Echo Futures — D2-06 Market Runtime]] — separación market/execution, REPLACE/DO NOT PROMOTE del bridge MT feed.
- [[Echo Futures — D2-07A Execution Adapter Contract]] — contrato del adapter (ACCEPTED_FOR_INTEGRATION).
- [[Echo Futures — D2-07B Transport Selection]] — comparación/evidencia de transports, separación D2/D6 (ACCEPTED_FOR_INTEGRATION post-R1).
- [[Echo Futures — D2-07C Execution Runtime Topology]] — topología sibling, ownership, routing, reuse map (ACCEPTED_FOR_INTEGRATION).
- Baselines: Agents-OS `b45e9328c0217e77c4f91103bb5f3a422d9cd5b6` (HEAD verificado); Echo `xKoRx/echo@372af59a7b83604781346613da01e3d510ea1360` (verificada por los children sin delta; no re-auditada salvo contradicción — no surgió ninguna).

## Handoff

```text
D2-07 STATUS:
READY_FOR_MANAGER_REVIEW
```

Siguiente gate: Primary Manager review only. No abrir D2-08; no cerrar D2 global.
