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
  - "[[Echo Futures — D1 Analysis Pack]]"
aliases:
  - Echo Futures D2-07B
  - EF Transport Eligibility
  - EF Initial V1 Transport Selection
tags:
  - kind/doc
  - area/echo
  - echo-futures
  - architecture-design
created: "2026-09-27"
updated: "2026-09-27"
---

# Echo Futures — D2-07B Transport Selection


> **OWNER DECISION SUPERSEDES THE RECOMMENDATION IN THIS CHILD — 2026-09-28**
>
> Este documento conserva la evidencia/comparación que llevó a proponer `PROJECTX_DIRECT` como candidate. Esa recomendación **ya no es la decisión vigente**. El Owner resolvió en el artifact integrado D2-07: comenzar la implementación con `FUTURES_BRIDGE_SIBLING + SimExecutionAdapter` y diferir la selección del primer transport externo real a D6, cuando exista acceso autorizado efectivo. ProjectX queda como future candidate only; no selected, no preferred, no certified.

## Propósito

Resolver exclusivamente D2-07B: contrastar ProjectX direct, NinjaTrader Desktop adapter, Tradovate direct, Rithmic direct y CQG WebAPI contra el contrato D2-07A, separar capability de ProviderProgram/API entitlement y determinar si existe un transport elegible para el primer E2E V1 sin dinero real. No diseña D2-07C, no implementa código, no cierra D2-07 y no avanza D2-08.

## Contenido


## 1. Executive verdict

**D2-07B STATUS: READY_FOR_SUBMANAGER_REVIEW.**

D2-07B corrige la separación entre selección arquitectónica y certificación física. D2 debe comparar transports, preservar el contrato genérico D2-07A y recomendar el primer camino non-real-money; D6 implementará y certificará físicamente el transport que realmente se elija. Los gaps M2 vendor-specific siguen siendo reales y obligatorios, pero son gates de deployment/certificación D6, no un blocker para diseñar D2-07C.

- **ProjectX direct = RECOMMENDED_INITIAL_NON_REAL_MONEY_CANDIDATE.** La evidencia aceptada ya demuestra API directa, submit/modify/cancel, observaciones realtime, un path Topstep simulado aceptado y menor coupling operativo inicial que Desktop. Sus gaps de customTag retention, ambiguous-submit recovery, authoritative negative semantics, Trade id scope/stability e history horizon permanecen sin probar y deberán cerrarse en D6 antes de habilitar exact physical submission.
- **NinjaTrader Desktop adapter = NOT_RECOMMENDED_AS_FIRST_GENERIC_V1_PATH.** Se conservan los findings de current-session execution history, recuperación histórica insuficiente y OrderId mutable/no-único. Eso hace débil al Desktop genérico como primer baseline de correctness, pero no declara imposible un adapter futuro provider-specific que aporte mecanismos adicionales.
- **Tradovate direct = FUTURE_ADAPTER_CANDIDATE.** Sus gaps M2 y entitlement se conservan como certificación transport-specific si alguna vez se selecciona.
- **Rithmic direct = FUTURE_ADAPTER_CANDIDATE.** La evidencia pública sigue siendo insuficiente para certificar M2; no bloquea D2 y no se investiga más en este frente.
- **CQG WebAPI = FUTURE_ADAPTER_CANDIDATE.** Mantiene las mejores primitives públicas de recovery entre las alternativas, pero sus gaps de retry/negative semantics y ProviderProgram entitlement quedan para certificación transport-specific si se implementa.

Por lo tanto:

~~~text
OD-D2-07-1 CANDIDATE:
PROJECTX_DIRECT

semantics:
recommendation only
first non-real-money implementation candidate
not transport certification
not real-money authorization
not Owner freeze
~~~

~~~text
PROJECTX M2 VENDOR CERTIFICATION = DEFERRED_TO_D6
REAL_MONEY_CERTIFICATION = NOT_DONE
D2-07C = UNBLOCKED
~~~

La recomendación no rebaja D2-07A. Antes de cualquier exact physical deployment, D6 debe cerrar los gates del transport seleccionado y mantener fail-closed cualquier capability que no pueda demostrar la semántica requerida.

## 2. Authority and evidence policy

Autoridades consumidas:

1. [[Echo Futures]].
2. [[Echo Futures — D2-04 Operation Order Fill Position]].
3. [[Echo Futures — D2-05 Instrument Session Provider]].
4. [[Echo Futures — D2-06 Market Runtime]].
5. [[Echo Futures — D2-07A Execution Adapter Contract]] — autoridad inmediata.
6. [[Echo Futures — D1 Analysis Pack]].
7. main/30-resources/futures/EXECUTION TRANSPORT FEASIBILITY — MULTI-PROP EVIDENCE.md.
8. main/30-resources/futures/FUTURES PROP UNIVERSE — AUTHORITATIVE EVIDENCE MATRIX.md.

Agents-OS real al inicio del repair: master@b53f1a254d2a777c97e927d7551088679069746f. Este HEAD supera el baseline mínimo despachado 494a2fd98c6765539617f35cad9ef0c131d80801; el repair releyó las autoridades D2-07A/B y el proyecto canónico antes de editar.

D2-07A usado: main/10-projects/Echo Futures/Echo Futures — D2-07A Execution Adapter Contract.md, blob ab978a389714f739d67ee4374eb025581504eec5.

Reglas aplicadas:

- Capability técnica, ProviderProgram permission y account/API entitlement son dimensiones independientes.
- UNKNOWN nunca se promueve a ALLOWED.
- D2-07-R1 prevalece sobre el wording permisivo antiguo de D2-04: Fill restart-safe exige provider execution identity nativa, estable y con scope conocido; no se sintetiza desde price/time/qty, seq local, orderId:seq, timestamp hash ni arrival order.
- M2 requiere Route A native idempotency suficientemente fuerte/documentada, Route B authoritative lookup/history por stable client identity, o una combinación demostrada.
- Un endpoint existente no prueba semántica de correctness.
- Un ACK de cancel/replace no se interpreta como execution finality.
- Para evidence gaps que cambian eligibility se usó sólo first-party vendor/provider material.


## 3. D2-07A qualification contract

D2-07A permanece íntegro y define el estándar para **exact physical submission**. Esta revisión no cambia M1/M2, durable write-ahead intent, stable client_order_id, no blind retry, reconciliation, AMBIGUOUS fail-closed, Fill identity ni la separación readiness/connectivity.

La separación de fases es:

~~~text
D2
=
architecture + adapter/bridge boundary
+ transport feasibility/comparison
+ recommendation del first non-real-money path

D6
=
physical implementation
+ transport-specific certification
+ authorized demo/shadow/sim validation
+ M2 evidence closure for the transport actually implemented
~~~

Por ello, un candidate puede ser recomendado en D2 como primer camino non-real-money sin estar aún certificado para exact physical submission. Antes de declarar un transport exact-submission eligible en un environment implementado, D6 debe demostrar como mínimo:

~~~text
supported_order_types
modify_mode
mutable_fields
cancel
partial_fill_delivery
client_order_id_round_trip
lookup_by_client_order_id
authoritative_negative_lookup
native_idempotency
open_order_snapshot
execution_history
stable_provider_execution_id
terminal_order_history/finality
position_snapshot
reconnect_and_resubscribe
multi_account_session
external account discovery/binding
ProviderProgram automation permission
direct developer/API entitlement
~~~

Además deben conocerse cuando apliquen: idempotency scope/retention, history horizon/cursor, negative consistency window, execution-id scope, session constraints, rate limits, host/device constraints y conformance requirements. NOT_PROVEN en estas semánticas significa **certification gate**, no autorización para relajar el contrato ni razón automática para bloquear el diseño D2.


## 4. Candidate comparison

Leyenda: PROVEN = demostrado por evidencia first-party suficiente para la fila; CONDITIONAL = capability demostrada pero falta una condición externa/enforceable; NOT_PROVEN = evidencia insuficiente para el contrato; NO = evidencia first-party demuestra ausencia/incompatibilidad. Estas filas describen evidencia disponible, no certificación productiva.

| Capability / transport | ProjectX direct | NinjaTrader Desktop | Tradovate direct | Rithmic direct | CQG WebAPI |
| --- | --- | --- | --- | --- | --- |
| M2 exact submission | NOT_PROVEN | NO | NOT_PROVEN | NOT_PROVEN | NOT_PROVEN |
| Stable execution identity | NOT_PROVEN | NOT_PROVEN | CONDITIONAL | NOT_PROVEN | PROVEN |
| History / exact recovery | CONDITIONAL | NO | CONDITIONAL | NOT_PROVEN | PROVEN |
| Finality evidence | CONDITIONAL | CONDITIONAL | CONDITIONAL | NOT_PROVEN | CONDITIONAL |
| Position snapshot | PROVEN | PROVEN | PROVEN | CONDITIONAL | PROVEN |
| Reconnect / gap recovery | CONDITIONAL | CONDITIONAL | CONDITIONAL | NOT_PROVEN | CONDITIONAL |
| Multi-account | PROVEN | PROVEN | PROVEN | NOT_PROVEN | PROVEN |
| Safe simulated path | PROVEN | PROVEN | CONDITIONAL | PROVEN | PROVEN |
| ProviderProgram scope | PROVEN* | CONDITIONAL | NOT_PROVEN | NOT_PROVEN | NOT_PROVEN |
| Direct developer/API entitlement | PROVEN* | CONDITIONAL | NOT_PROVEN | CONDITIONAL | CONDITIONAL |
| Host constraints | Personal device; no VPS/VPN/remote order flow | Desktop host + C# adapter lifecycle | Web/API; Partner organization credentials | API runtime; production conformance | WebSocket/protobuf; production conformance |
| D2-07B disposition | **RECOMMENDED_INITIAL_NON_REAL_MONEY_CANDIDATE** | **NOT_RECOMMENDED_AS_FIRST_GENERIC_V1_PATH** | FUTURE_ADAPTER_CANDIDATE | FUTURE_ADAPTER_CANDIDATE | FUTURE_ADAPTER_CANDIDATE |
| Certification note | D6 must close ProjectX M2 gates before exact physical submission | Provider-specific future adapter would need additional recovery/identity proof | D6 certification required if selected | D6 certification required if selected | D6 certification required if selected |

*ProjectX scope:* Topstep API access is demonstrated for eligible simulated TopstepX accounts and excludes Live Funded. D1 accepted scope for the first path is **Trading Combine + Express Funded Account**; Topstep first-party material independently confirms Trading Combine and XFA are simulated. Practice is a safe testing account, not a ProviderProgram.

## 5. ProjectX direct

### 5.1 Capability facts

First-party ProjectX docs prove:

- MARKET, LIMIT, STOP and other order types.
- Modify and cancel endpoints.
- customTag on order submission; documentation says it **must be unique across the account**.
- A duplicate customTag is a validation rejection under OrderRejected.
- Order search accepts account + time range and returns terminal/current order records including customTag, provider id, fill volume and filled price.
- Trade search accepts account + time range and returns a server trade id linked to orderId.
- Realtime order/position/trade subscriptions plus reconnect/resubscribe are documented.
- One Topstep API key/session can address multiple eligible accounts by accountId.

Topstep first-party docs additionally prove:

- automated strategies and bots are allowed through TopstepX / ProjectX API subject to platform rules;
- API access is a separately provisioned subscription/key;
- all order flow must originate on the trader's personal device; VPS, VPN and remote order relays are prohibited;
- Practice Account uses the same endpoints and realtime hubs and is the prescribed no-risk testing environment;
- Live Funded accounts cannot trade through ProjectX API because the gateway is for the simulated environment.

### 5.2 M2 evaluation

Scenario:

~~~text
submit MARKET(customTag = X)
venue may accept
connection/process dies before response
adapter restarts
~~~

What is proven:

- A second request using an already-used customTag is documented as invalid/rejected.
- The tag round-trips in Order search results.
- Recent Orders and Trades can be recovered by account/time.

What is **not** proven:

- retention/lifetime of customTag uniqueness after a terminal/fast-filled order;
- an explicit atomic “same customTag can never create a second executable order” guarantee across timeout/reconnect/restart;
- lookup directly by customTag;
- an authoritative negative result with consistency window;
- whether an accepted order can be temporarily absent from Order search after the submit response was lost;
- a documented scope/stability contract for Trade id sufficient to certify realtime/history dedup under D2-07-R1.

Verdict:

~~~text
PROJECTX M2 = NOT_PROVEN
D2-07B disposition = RECOMMENDED_INITIAL_NON_REAL_MONEY_CANDIDATE
M2_VENDOR_CERTIFICATION = DEFERRED_TO_D6
REAL_MONEY_CERTIFICATION = NOT_DONE
~~~

The existing uniqueness rule is sufficient to support ProjectX as the first non-real-money implementation candidate, but not to certify exact physical submission. D2-07A still requires idempotency scope/retention or authoritative lookup semantics; “unique across the account” is not silently expanded into an undocumented retention contract. Those claims move to the D6 certification gate.

### 5.3 Finality

Order search exposes statuses and terminal records, and trades are separate facts. That is sufficient to model status/fill observations, but the public material reviewed does not define a cancel-vs-fill race contract, late-fill delivery boundary or exact point at which a negative/cancel result is execution-final. Therefore CONDITIONAL, not PROVEN.

### 5.4 Recovery

Realtime reconnect/resubscribe is documented. Order/Trade time-window searches allow state reconstruction after a normal gap. Exact recovery remains CONDITIONAL because there is no documented cursor/watermark, history retention contract or authoritative-negative consistency window.

### 5.5 ProviderProgram / environment

~~~text
Provider: Topstep
ProviderProgram scope:
- Trading Combine — simulated — API/bot path eligible
- Express Funded Account — simulated funded-level — API/bot path eligible
- Live Funded Account — EXCLUDED from ProjectX API

Safe certification environment:
- Topstep Practice Account
- same ProjectX endpoints + realtime hubs
- no risk to Evaluation account

Deployment:
- personal trader device only
- no VPS
- no VPN
- no remote server placing/modifying/cancelling/relaying orders
~~~

## 6. NinjaTrader Desktop adapter

### 6.1 Capability facts

NinjaTrader Account API demonstrates multiple Account objects, order creation/submission/change/cancel, Order events, Execution events, Position events and partial/multi-fill handling. Sim101 is a valid generic simulator for capability tests.

### 6.2 M2 failure

Two first-party facts are disqualifying for a generic V1 exact-recovery adapter:

- Account.Executions contains the **current session's executions** and NinjaTrader states there is **no supported method to retrieve historical executions from the local database**.
- Order.OrderId is **not a unique value** and can change during the order lifetime.

A local Order object or strategy name cannot become a restart-safe external client identity by assumption. After process/platform restart, the generic adapter cannot prove that it can recover every missed Fill with the same native identity required by D2-07-R1.

Verdict:

~~~text
NINJATRADER M2 = NO
D2-07B disposition = NOT_RECOMMENDED_AS_FIRST_GENERIC_V1_PATH
~~~

A future provider-specific NinjaTrader connection could expose stronger broker-native recovery underneath the platform; in that case the correctness proof belongs to that provider transport/binding and its D6 certification, not to NinjaTrader Desktop generically. This worker does not declare NinjaTrader permanently unusable.

### 6.3 ProviderProgram / host implications

D1 already proves NinjaTrader is a supported automation surface for several candidate props/programs, but support of NinjaTrader is not direct API entitlement. The path also imposes Desktop lifecycle, a local host, a C# AddOn/strategy bridge and connection/session ownership. Since M2 fails first, additional commercial onboarding is not decision-changing for this worker.

## 7. Tradovate direct

### 7.1 Capability facts

First-party Partner API docs prove MARKET and other order types; optional clOrdId on Place Order; order/fill/execution-report entities; unique API entity IDs and item/list/dependency query patterns; demo/live endpoints and WebSocket/data synchronization primitives.

### 7.2 M2 evaluation

Missing first-party proof:

- uniqueness/idempotency semantics of clOrdId;
- duplicate-submit behavior when the first response is lost;
- retention/scope of any duplicate-prevention key;
- authoritative lookup/negative lookup by clOrdId;
- negative consistency window guaranteeing a missing order cannot appear later.

Therefore:

~~~text
TRADOVATE M2 = NOT_PROVEN
D2-07B disposition = FUTURE_ADAPTER_CANDIDATE
TRANSPORT_SPECIFIC_CERTIFICATION = REQUIRED_IN_D6_IF_SELECTED
~~~

Fill.id/entity IDs are materially better than heuristic fill identity, so execution identity is CONDITIONAL; D2-07-R1 still requires the exact scope/realtime-history stability to be part of the certification.

### 7.3 Entitlement

Tradovate Partner API documentation requires **Organization Admin credentials, API Key and CID**, with onboarding through Evaluation Support. That is a developer/organization entitlement contract. It is not proven for a normal user account supplied by any of the prop ProviderPrograms in scope. TradeDay is already accepted in D1 as explicitly not granting direct Tradovate API.

## 8. Rithmic direct

### 8.1 Capability facts

Rithmic first-party material proves order-management APIs, R|API+/R|Protocol families, a Rithmic Test environment and an exchange simulator suitable for integration testing. Rithmic states that test-system development does not require conformance, while production systems including Rithmic 01 / Rithmic Paper Trading and FCM IDs require conformance; live credentials then come through the FCM/broker.

### 8.2 M2 evaluation

The public first-party material reviewed does **not** define enough of stable client submission identity, duplicate/retry semantics, idempotency scope/retention, exact execution ID scope, execution-history horizon/cursor, authoritative negative lookup or terminal order recovery.

Therefore:

~~~text
RITHMIC M2 = NOT_PROVEN
D2-07B disposition = FUTURE_ADAPTER_CANDIDATE
TRANSPORT_SPECIFIC_CERTIFICATION = REQUIRED_IN_D6_IF_SELECTED
~~~

A dev kit / protocol specification may contain the missing claims, but D2-07B does not invent them from product marketing.

### 8.3 ProviderProgram / environment

Rithmic Test/Exchange Simulator is a safe non-real-money API integration environment, but it is generic Rithmic infrastructure, not proof that a specific prop ProviderProgram grants Echo direct developer credentials. Production also requires conformance.

## 9. CQG WebAPI

### 9.1 Capability facts

CQG WebAPI first-party documentation proves:

- secure WebSocket + protobuf, language agnostic;
- demo endpoint wss://demoapi.cqg.com with WebAPITest application identity;
- production requires formal conformance;
- Order.cl_order_id is a client order identifier and must be unique within a trading day for day orders and across days for multi-day orders;
- Trade.trade_id is server-assigned and **unique within account**;
- historical order requests return order/transaction status history, current working/parked orders and have a default 30-day depth;
- historical requests can cover all accounts of the authenticated user;
- production application IDs/private labels are issued after conformance.

### 9.2 M2 evaluation

CQG is the strongest public technical evidence set among the alternatives because it has explicit client-order uniqueness, scoped native execution identity and bounded history.

Still missing for exact submit certification:

- documented behavior when an application retransmits the same cl_order_id after an ambiguous disconnect;
- explicit guarantee that such a retry cannot create a second executable physical order;
- authoritative-negative semantics / consistency boundary for “no matching order/status” before a retry;
- a first-party ProviderProgram entitlement that lets Echo place orders directly through WebAPI for one of the props in D1.

Therefore:

~~~text
CQG WEBAPI M2 = NOT_PROVEN
D2-07B disposition = FUTURE_ADAPTER_CANDIDATE
TRANSPORT_SPECIFIC_CERTIFICATION = REQUIRED_IN_D6_IF_SELECTED
~~~

Stable execution identity itself is PROVEN: trade_id is native, server-assigned and unique within account. History is also PROVEN for the documented order-history surface/horizon. Those strengths make CQG the preferred **second-adapter evidence target**, not a reason to waive the remaining M2/entitlement gaps.

## 10. Execution identity summary

| Transport | Native identity evidence | D2-07-R1 result |
| --- | --- | --- |
| ProjectX | Trade response/event has server id, linked orderId; exact uniqueness/scope not documented in reviewed public contract | NOT_PROVEN |
| NinjaTrader | Execution events expose execution IDs, but local historical execution recovery is unsupported and OrderId can change | NOT_PROVEN |
| Tradovate | API entities have unique IDs; Fill entity is queryable | CONDITIONAL pending exact execution scope + realtime/history stability |
| Rithmic | Public product material insufficient for exact ID contract | NOT_PROVEN |
| CQG WebAPI | trade_id server-assigned and unique within account | PROVEN |

No transport is upgraded using orderId:seq, timestamp, price+qty, arrival order or any heuristic composite.

## 11. Finality summary

- **ProjectX:** terminal order statuses/history exist, but cancel/fill race and late-fill finality boundary are not formally specified in the reviewed public docs → CONDITIONAL.
- **NinjaTrader:** realtime lifecycle/event handling is strong, but restart/history limitation prevents generic terminal reconciliation → CONDITIONAL realtime, insufficient V1 exact recovery.
- **Tradovate:** order/execution entities support terminal observation, but exact cancel/replace race semantics were not proven in this targeted pass → CONDITIONAL.
- **Rithmic:** public evidence insufficient → NOT_PROVEN.
- **CQG:** order and transaction history are strong, but D2-07B did not find a direct authoritative contract for every cancel/replace race edge → CONDITIONAL.

No request ACK is treated as finality.

## 12. Recovery / reconnect summary

- **ProjectX:** reconnect/resubscribe + order/trade time searches are real; no history cursor/horizon or authoritative-negative contract → CONDITIONAL.
- **NinjaTrader:** platform can reconnect and expose current account state, but current-session-only executions cannot close exact missed-execution recovery after restart → NO for D2 exact recovery.
- **Tradovate:** entity lists/sync make recovery technically plausible; exact M2 negative semantics remain missing → CONDITIONAL.
- **Rithmic:** public evidence insufficient → NOT_PROVEN.
- **CQG:** complete/current trade subscription snapshots plus historical order/status retrieval with documented default 30-day depth provide the strongest recovery surface → PROVEN for history surface, while submit ambiguity remains separately blocked.

## 13. Entitlement / operational constraints

| Transport | Technical API availability | ProviderProgram / account entitlement |
| --- | --- | --- |
| ProjectX | Public REST + realtime API | **PROVEN for Topstep eligible simulated path** after paid API subscription/link/key; Trading Combine + XFA scope accepted; Live Funded excluded |
| NinjaTrader | Desktop Account API | Provider/platform support is program-specific and conditional; generic Sim101 is not ProviderProgram proof |
| Tradovate | Partner REST/WebSocket API | Requires Organization Admin + API Key + CID; direct prop-user entitlement not proven |
| Rithmic | Dev kit/Test available; production conformance | Specific prop direct developer entitlement not proven |
| CQG WebAPI | WebAPITest demo + production conformance path | Specific prop direct WebAPI entitlement not proven |


## 14. ProjectX D6 certification gates

Los gaps ProjectX encontrados por B se conservan, pero se reclasifican como **PROJECTX D6 CERTIFICATION GATES**. No ejecutar PX1 ni pruebas credentialed en este repair.

Antes de habilitar ProjectX para exact physical submission, D6 debe cerrar como mínimo:

1. **customTag retention / uniqueness scope:** demostrar cuánto sobrevive la unicidad después de terminal/fill y a través de reconnect/restart.
2. **Ambiguous-submit recovery:** demostrar que un outcome desconocido no puede terminar en blind retry ni en dos órdenes ejecutables; si se reutiliza customTag, probar su atomicidad real.
3. **Authoritative negative / recovery semantics:** demostrar cuándo “no existe” es autoritativo o qué mecanismo nativo evita depender de una lectura eventualmente consistente.
4. **Execution identity:** demostrar scope y estabilidad del Trade id entre realtime e history/reconnect.
5. **History horizon:** establecer el horizonte usable o el máximo outage a partir del cual el adapter debe permanecer AMBIGUOUS/not-ready.

Estos gaps **no bloquean D2-07C**. Sí bloquean cualquier declaración de M2_VENDOR_CERTIFICATION = PASS, cualquier autorización real-money y cualquier deployment que habilite exact physical submission sin cerrar el gate.


## 15. Recommended initial V1 candidate

~~~text
PROJECTX_DIRECT
=
RECOMMENDED_INITIAL_NON_REAL_MONEY_CANDIDATE
~~~

La recommendation se sostiene únicamente con la evidencia ya aceptada:

- API directa con submit/modify/cancel.
- Observaciones realtime de orders/trades/positions.
- Topstep Trading Combine + Express Funded Account como ProviderPrograms simulados dentro del path aceptado; Practice como environment seguro de certificación, no ProviderProgram.
- Menor coupling operativo inicial que NinjaTrader Desktop.
- El Core no necesita volverse ProjectX-specific; el transport queda detrás del boundary Adapter/Bridge.

Semántica explícita:

~~~text
recommendation only
first non-real-money implementation candidate
M2 vendor certification deferred to D6
real-money certification not done
not Owner freeze
~~~

No se selecciona un segundo adapter en D2-07B. Los candidatos restantes permanecen disponibles para trabajos futuros sin exigir pre-certificar todo el universo antes de avanzar.

## 16. Exact ProviderProgram scope

### ProjectX

~~~text
Provider: Topstep
Programs in candidate scope:
- Trading Combine — SIMULATED
- Express Funded Account — SIMULATED FUNDED-LEVEL

Certification-only environment:
- Practice Account — SIMULATED, same API endpoints/hubs, not a ProviderProgram

Explicit exclusion:
- Live Funded Account — ProjectX API unavailable
~~~

### Other transports

No exact prop ProviderProgram direct-API entitlement was proven in this worker for NinjaTrader generic adapter, Tradovate direct, Rithmic direct or CQG WebAPI. Platform availability from D1 remains useful discovery evidence but is not promoted to API entitlement.

## 17. Host / operational constraints

- **ProjectX / Topstep:** order flow must originate on the trader's personal device. Private servers may support analytics/storage, but cannot place, modify, cancel, trigger or relay orders.
- **NinjaTrader:** requires Desktop lifecycle and local adapter integration; the platform process becomes part of the execution fault domain.
- **Tradovate:** direct web API is suitable for server-side designs only when Partner entitlement exists.
- **Rithmic:** API family supports multiple OS/runtime options; production use requires conformance and broker/FCM credentials.
- **CQG WebAPI:** WebSocket/protobuf is language-agnostic; WebAPITest is available before production conformance.

These constraints are inputs for D2-07C topology and later D6 certification; they do not require vendor M2 certification to be complete before D2-07C can be designed. Transport selection must remain behind the Bridge/Adapter boundary. No topology is frozen here.


## 18. Non-real-money feasibility

| Candidate | Non-real-money environment | D2-07B result |
| --- | --- | --- |
| ProjectX | Topstep Practice; Trading Combine/XFA are simulated programs | **RECOMMENDED_INITIAL_NON_REAL_MONEY_CANDIDATE**; M2 vendor certification deferred to D6 |
| NinjaTrader | Sim101 | Capability testing only; NOT_RECOMMENDED_AS_FIRST_GENERIC_V1_PATH |
| Tradovate | demo/staging simulation engines | FUTURE_ADAPTER_CANDIDATE; certification required if selected |
| Rithmic | Rithmic Test / Exchange Simulator | FUTURE_ADAPTER_CANDIDATE; certification required if selected |
| CQG WebAPI | WebAPITest / demoapi | FUTURE_ADAPTER_CANDIDATE; certification required if selected |

“Has simulator” is not equivalent to real-money authorization or ProviderProgram entitlement.


## 19. SimExecution, Bridge boundary and future adapters

D2 domain/runtime design does **not** require a real vendor transport to validate the generic execution contract. SimExecution may exercise the D2-07A contract for architecture/testing; a real transport is an additional V1 implementation/certification step required in D6.

Transport selection must remain behind the Bridge/Adapter boundary. D2-07B does **not** design ExecutionAdapterHost, Futures Bridge, process topology, Kafka routing or sessions; those belong to D2-07C.

D2-07A should remain vendor-neutral. A future second adapter should prove that the contract is not accidentally ProjectX-shaped:

- **CQG WebAPI** remains the strongest contrast because it has explicit client-order uniqueness rules, stable per-account trade identity and bounded historical order retrieval.
- Adapter abstractions should expose idempotency scope/retention, history horizon, execution-ID scope, finality evidence and negative-lookup capability as declared capabilities, not hidden booleans inferred from endpoints.
- NinjaTrader Desktop can remain an integration surface later, but its local session/history semantics should not define the canonical M2 model.
- No adapter is allowed to replace external identity with Echo-local sequence, Position deltas or transport-specific heuristics.


## 20. Residual evidence gaps

These gaps are preserved as transport-specific certification or future-adapter work. They do not block D2-07C.

### ProjectX — D6 certification gates

- customTag uniqueness retention.
- Duplicate retry atomicity after ambiguous submit.
- authoritative negative lookup / consistency if Route B is needed.
- Trade id scope and realtime/history stability.
- explicit history horizon.

### NinjaTrader — first-path structural risk

- Historical executions are not available through the supported generic local API.
- OrderId is mutable/not unique.
- A future provider-specific adapter must prove additional recovery/identity semantics rather than inherit a generic PASS.

### Tradovate — future adapter certification

- clOrdId idempotency/uniqueness/retention.
- lookup by client identity and authoritative negative.
- direct ProviderProgram entitlement.

### Rithmic — future adapter certification

- protocol-level M2 semantics from dev kit/spec.
- execution identity/history/recovery semantics.
- direct ProviderProgram entitlement and conformance/account path.

### CQG — future adapter certification

- same-cl_order_id retransmission semantics.
- authoritative negative lookup/consistency.
- direct ProviderProgram entitlement for an in-scope prop.


## 21. D6 TRANSPORT CERTIFICATION GATE

Before ProjectX —or any future transport— may be declared eligible for exact physical submission in an implemented environment, D6 must verify on the transport actually selected:

- durable M2 implementation before the physical point-of-no-return;
- stable client identity behavior and retention/scope;
- ambiguous submit recovery with no blind retry;
- exact execution identity and scope;
- history/recovery horizon and authoritative recovery semantics;
- reconnect/resubscribe and gap recovery behavior;
- terminal finality, including cancel/fill and late-fill edges;
- ProviderProgram/account entitlement for the concrete environment;
- authorized host/environment constraints;
- actual E2E shadow/demo/sim validation.

Only investigate these claims for the transport actually implemented. Do not pre-certify every candidate.

## 22. Owner decision candidate

~~~text
OD-D2-07-1 CANDIDATE:
PROJECTX_DIRECT
~~~

Semantics:

~~~text
recommendation only
first non-real-money implementation candidate
not transport certification
not real-money authorization
not Owner freeze
~~~

The Owner/Primary Manager still decides. This candidate does not bypass the D6 certification gate.

## 23. Material risks

- **False idempotency from a client tag.** A unique-looking tag without documented retention/retry semantics can still leave a crash window.
- **Eventual negative lookup.** “Not found” before indexing completes can convert one physical MARKET into two.
- **Realtime-only fill identity.** An execution ID that cannot be recovered from history after restart is insufficient.
- **Platform entitlement leakage.** NinjaTrader/Tradovate/Rithmic/CQG platform availability does not grant a developer API.
- **Simulator overpromotion.** Generic Sim101/Rithmic Test/CQG demo proves transport mechanics, not a prop ProviderProgram path.
- **Topstep deployment violation.** A technically correct ProjectX adapter deployed as a remote relay/VPS would violate the documented order-flow constraint.
- **History horizon mismatch.** Recovery after the provider's retained horizon must fail closed, never infer “flat/no order”.
- **Cancel/fill race simplification.** Cancel acceptance cannot release reservations until fill/finality evidence converges.

## 24. First-party evidence register

Evidence date: **2026-09-27**.

### ProjectX / Topstep

- ProjectX Place Order — https://gateway.docs.projectx.com/docs/api-reference/order/order-place/ — MARKET/LIMIT/STOP; customTag account-unique; duplicate tag is an OrderRejected validation case; returns provider order ID. Limitation: no retention/idempotency contract.
- ProjectX Search Orders — https://gateway.docs.projectx.com/docs/api-reference/order/order-search/ — account/time search, terminal order fields, customTag. Limitation: no query by tag and no authoritative-negative semantics.
- ProjectX Search Trades — https://gateway.docs.projectx.com/docs/api-reference/trade/trade-search/ — server trade id, orderId, account/time search. Limitation: no explicit uniqueness/stability scope.
- ProjectX Realtime — https://gateway.docs.projectx.com/docs/realtime/ — realtime order/position/trade subscriptions and reconnect/resubscribe. Limitation: reconnect alone is not gap recovery.
- Topstep API Access — https://help.topstep.com/en/articles/11187768-topstepx-api-access — automation/API permission, account/API key setup, personal-device/no-VPS rule, Practice environment, multi-account profile, Live Funded exclusion. Limitation: business/API entitlement source, not M2 semantics.
- Topstep Trading Combine parameters — https://help.topstep.com/en/articles/8284197-trading-combine-parameters — Trading Combine is simulated.
- Topstep Express Funded Account parameters — https://help.topstep.com/en/articles/8284215-express-funded-account-parameters — XFA is simulated funded-level.
- Topstep Practice Account — https://help.topstep.com/en/articles/8284134-practice-account — simulated sandbox account.

### NinjaTrader

- Executions — https://docs.ninjatrader.com/ninjascript/executions — current-session executions only; no supported historical-execution retrieval from local DB.
- Advanced Order Handling — https://docs.ninjatrader.com/ninjascript/advanced_order_handling — Order.OrderId is not unique and can change.
- Account / Order / Execution developer docs — official NinjaTrader Developer Docs — Create/Submit/Change/Cancel and Account/Execution/Position events. Limitation: capability does not repair restart-history gap.

### Tradovate

- Place Order — https://partner.tradovate.com/api/rest-api-endpoints/orders/place-order — includes clOrdId, MARKET and other order types.
- Architecture Overview — https://partner.tradovate.com/overview/core-concepts/architecture-overview — all entities have unique IDs; item/list query patterns and demo examples.
- Introduction / API access — https://partner.tradovate.com/overview/welcome/introduction-to-tradovate-partner-api — Organization Admin + API Key + CID; demo/live/staging endpoints. Limitation: Partner entitlement, not prop-user grant.

### Rithmic

- APIs — https://www.rithmic.com/apis — R|API+/R|Protocol capabilities, Rithmic Test, conformance path, broker/FCM live credentials.
- Exchange Simulator — https://www.rithmic.com/products/exchange-simulator — no-real-capital developer/order-flow testing. Limitation: public marketing surface does not contain full M2 protocol semantics.

### CQG WebAPI

- WebAPI — https://help.cqg.com/apihelp/Documents/cqgwebapi.htm — WebSocket/protobuf, demo endpoint and conformance requirement.
- Order — https://help.cqg.com/apihelp/Documents/messageorder.htm — cl_order_id uniqueness scope.
- Trade — https://help.cqg.com/apihelp/Documents/messagetrade.htm — server trade_id, unique within account.
- HistoricalOrdersRequest — https://help.cqg.com/apihelp/Documents/messagehistoricalordersrequest.htm — historical statuses, all-account filtering, default 30-day depth.
- Logon — https://help.cqg.com/apihelp/Documents/logon.htm — WebApiTest before production; production app identity after conformance.
- WebAPI Conformance Test — https://help.cqg.com/apihelp/Documents/webapiconformancetestandtestplan1.htm — required production conformance.


## 25. Final worker status

~~~text
D2-07B STATUS:
READY_FOR_SUBMANAGER_REVIEW

ARTIFACT:
main/10-projects/Echo Futures/Echo Futures — D2-07B Transport Selection.md

EVIDENCE DATE:
2026-09-27

D2-07A CONTRACT USED:
main/10-projects/Echo Futures/Echo Futures — D2-07A Execution Adapter Contract.md
blob ab978a389714f739d67ee4374eb025581504eec5

INITIAL NON-REAL-MONEY TRANSPORT CANDIDATE:
PROJECTX_DIRECT

WHY:
direct API + submit/modify/cancel + realtime observations
Topstep simulated ProviderProgram path already accepted
lower initial operational coupling than Desktop
vendor-specific logic remains behind Adapter/Bridge boundary

PROJECTX M2:
NOT_PROVEN — customTag retention, ambiguous-submit retry atomicity, authoritative recovery/negative semantics, Trade id scope/stability and history horizon remain open.

CERTIFICATION PHASE:
D6

REAL-MONEY CERTIFICATION:
NOT_DONE

OD-D2-07-1:
PROJECTX_DIRECT — CANDIDATE ONLY

D2-07C:
UNBLOCKED

MATERIAL RISKS:
false idempotency from client tags
eventual negative lookup
realtime-only fill identity
Topstep personal-device order-flow constraint
history-horizon mismatch and cancel/fill finality edges

NEXT:
SUBMANAGER review.
Do not start D2-07C.
Do not start D2-08.
~~~

## Fuentes

- Autoridades Agents-OS listadas en §2.
- First-party evidence register §24.
