---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo Futures]]"
  - "[[Echo Futures — D1 Analysis Pack]]"
aliases:
  - Echo Futures D2-04
  - EF D2-04 Operation Order Fill Position
tags:
  - kind/doc
  - area/echo
  - echo-futures
  - architecture-design
created: "2026-09-26"
updated: "2026-09-26"
---

# Echo Futures — D2-04 Operation / Order / Fill / Position

> [!info]+ Workstream D2-04
> Diseño técnico V1 del modelo `Operation / Order / Fill / Position` y su runtime dentro de Echo V3. Respeta sin reabrir las decisiones owner [[Echo Futures]] D2-01 (snapshot + contract pinning), D2-02 (fan-out + single Operation) y D2-03 (Signal + Strategy/MM boundary), y el lifecycle A2 aceptado en [[Echo Futures — D1 Analysis Pack]]. Responde Q2 (Position attribution) y Q3 (Order lifecycle). Baseline físico verificada: `xKoRx/echo origin/master = 372af59a7b83604781346613da01e3d510ea1360` (re-verificada por fetch en el repair 2026-09-26, sin delta). No implementa código productivo y no cierra D2. Tras el manager review (`D2_04_MANAGER_REVIEW = CORRECTION_REQUIRED`), este artefacto incorpora las correcciones R1–R9 registradas en la sección "Manager Repair — 2026-09-26".

## Manager Repair — 2026-09-26

- **R1:** eliminada la "referencia a la versión del binding" de Operation (contradecía D2-01). El snapshot efectivo es embebido y autosuficiente; sin entidades/referencias versionadas; sin config hash (ver rationale en §2.1).
- **R2:** `direction` nace del OPEN Signal aceptado (autoridad técnica Strategy) en el momento de materializar la Operation, antes de MM/Orders; Orders se validan contra esa dirección y nunca la definen retroactivamente (§2.1, §2.2, §3.1, I3).
- **R3:** ForceClose modelado como **intent de terminación** (`termination`), no como terminalización instantánea; toda transición a TERMINAL pasa por la evaluación uniforme de guards; `SAFETY_FLATTEN` es el eventual TerminalReason (§3.1).
- **R4:** prohibido clampear fill truth: la exposición firmada conserva el hecho físico aunque rompa la dirección intencionada; breach marcado `EXPOSURE_INVARIANT_BREACH` fail-visible; sin synthetic fills, sin reparación, sin Operation nueva (I5/I6, §6).
- **R5:** separación explícita entre estado derivado de hechos (conmutativo) y procesamiento de decisiones stateful (serializado; determinístico sólo ante la misma secuencia ordenada de eventos); adoptado `operation_event_seq` sellado por el state owner como orden de replay; la garantía "independiente del orden de llegada" queda restringida a las cantidades derivadas de hechos (§6.3, I8).
- **R6:** ventana de crash resuelta y probada end-to-end con la garantía documentada de Flink StateFun 3.2 (egress Kafka EXACTLY_ONCE vía transacción commiteada en checkpoint, 2PC) + registro de idempotencia en el adapter por `client_order_id` para el path at-least-once del consumer; `client_order_id` permanece UUIDv7 porque bajo 2PC ningún comando físico escapa sin estado commiteado (§5.6, caso 5).
- **R7:** el horizonte de dedup de fills ya no es TTL: el set de dedup persiste durante toda la vida de la Operation no terminal (naturalmente acotado) y se evicta recién en TERMINAL; se reconstruye desde checkpoint/PG en recovery (§5.5, caso 6).
- **R8:** reclasificado Position: REUSE del patrón (ingress periódico, async projection writer) / **REPLACE del shape** de dominio — la proyección Futures es neta por `(account_id, contract_id)`, no `PositionSnapshot` MT por ticket + contract_id (§2.4, §7.1, §9).
- **R9:** reducida la superficie nueva por KISS/YAGNI: eliminadas tablas `order_events`/`operation_events`, eliminadas la función `echo/operation_store` + topic `operation-facts` (writer async embebido en `echo/operation`, patrón `PositionSyncFn`) y eliminada la función `echo/execution_router` (la correlación evento→operación la posee el registry de submissions del adapter, ya requerido por R6). Superficie nueva final: 2 funciones StateFun, 2 ingress topics, 1 familia de egress, 4 tablas PG (§8.2, §10).

## 1. Executive verdict

- `STATUS: D2-04_READY_FOR_MANAGER_REVIEW` (post-repair R1–R9). El diseño cierra identidades, lifecycles, ownership, exposición lógica, partial fills, múltiples Orders vivas, cancel/replace, idempotencia (incluida la ventana de crash), reconciliation boundary, aislamiento, event ordering y crash/recovery para las cuatro entidades, con mapping físico contra Echo V3 `372af59a`.
- Decisión central: **`Operation` es el aggregate lógico; el state owner físico es una función StateFun nueva `echo/operation` keyeada por `execution_account_id:account_strategy_id`**, que serializa determinísticamente todas las Signals, Orders, Fills y decisiones MM de esa cuenta+estrategia. Cuentas/estrategias distintas viven en keys distintas → aislamiento por construcción, sin store global de MM.
- **`Order` es entity del aggregate Operation (no aggregate independiente) y `Fill` es hecho inmutable** append-only. `Position` NO participa del lifecycle: es proyección read-only de observación física neta por `(account, contract)`, comparada contra exposición lógica sólo para telemetría (`DT-EF-POSITION-RECONCILIATION-05` sigue diferida; no hay auto-repair).
- **Dirección de la Operation nace del OPEN Signal aceptado** (autoridad técnica Strategy) y es immutable desde la materialización, antes de MM/Orders/Fills; las Orders se validan contra ella y jamás la definen (R2).
- **Fill truth jamás se clampa:** la exposición firmada conserva el hecho físico aunque un comportamiento anómalo del venue produzca una exposición incompatible con la dirección intencionada; el breach se marca y es fail-visible (R4).
- **Garantía de determinismo acotada (R5):** las cantidades derivadas de hechos (exposición, filled qty, precio ponderado) son conmutativas; las decisiones stateful de MM son determinísticas ante la misma secuencia ordenada de eventos — no ante órdenes de llegada arbitrarios — y el orden relevante se preserva con `operation_event_seq` sellado por el state owner.
- **No hay ventana de doble orden física (R6):** el submit de comandos usa el egress Kafka de StateFun en semántica EXACTLY_ONCE (transacción commiteada atómicamente con el checkpoint, garantía documentada del runtime 3.2 ya desplegado), y el adapter deduplica por `client_order_id` el path at-least-once de consumo. La prueba end-to-end está en §5.6 y en el caso 5.
- Cero nuevas entidades genéricas: no `OperationLeg`, no `StrategyTrade`, no revisiones formales (D2-01), no event sourcing, no saga, no workflow engine, no microservicio nuevo. Superficie nueva mínima (R9): 2 funciones StateFun (`echo/signal_fanout`, `echo/operation`), 2 ingress topics, 1 familia de egress per-account, 4 tablas PG.
- `OWNER DECISIONS REQUIRED: NONE`. Toda corrección del repair es técnica y vive dentro de las decisiones congeladas. Quedan ratificaciones técnicas ordinarias para el manager (enum `TerminalReason`, nombres de functions/topics/tablas, y la config de despliegue EXACTLY_ONCE del egress).

## 2. Modelo de dominio mínimo

### 2.1 Operation

- Definición: lifecycle lógico de una intención materializada para una `AccountStrategy` concreta, administrada por su `MoneyManagement`, desde la primera apertura hasta el cierre de la última exposición correspondiente (D2-02). Es el aggregate root del execution path nuevo.
- Identidad: `operation_id` UUIDv7 generado por Core al materializar (mismo generador que `utils.GenerateUUIDv7` existente). Alcance: `(execution_account_id, account_strategy_id, strategy_id, instrument_id, contract_id)`. La identidad es segura bajo crash/replay: bajo la garantía 2PC del egress (§5.6), ningún comando físico puede haber escapado sin estado commiteado, por lo que una re-materialización post-crash nunca convive con artefactos físicos de una intent previa.
- Invariante D2-02: como máximo **una Operation no terminal** por `account_strategy_id`. El par `(execution_account_id, account_strategy_id)` determina unívocamente la Operation actual, lo que permite routear eventos sin conocer `operation_id`.
- Dirección: tomada del **OPEN Signal aceptado** (Strategy es autoridad técnica de dirección, D2-03) en el momento de materializar; immutable durante todo el lifecycle (A2). No es derivada de Orders ni de Fills (R2).
- Campos de autoridad (estado, no derivable): `operation_id`; `account_id`; `account_strategy_id`; `strategy_id`; `instrument_id`; `contract_id` (pinneado al crear, D2-01); `direction` (LONG/SHORT, desde la Signal, immutable); `status`; `termination` (intent de terminación pendiente: none | {requested_by: MM | SAFETY_PLANE, reason, requested_at}); `terminal_reason` (cuando TERMINAL); `exposure_invariant_breach` (bool + detalle del primer breach, R4); `created_from_signal_id`; `operation_event_seq` (última secuencia procesada, R5); `run_mode` (LIVE/SHADOW/DEMO/REPLAY/BACKTEST) + `run_id` (provenance para futuro Lab, constraint D1); timestamps de creación/actividad.
- Snapshot efectivo (D2-01, KISS): la Operation conserva **embebido y autosuficiente** sólo el estado/configuración efectiva que su comportamiento necesita para no cambiar accidentalmente por hot updates: el `MoneyManagement` resuelto (id + config efectiva mínima), y las specs vigentes del `Contract` pinneado (tick size, tick value, multiplier, qty step). **No hay referencia a ninguna versión/revision formal del binding** — la única referencia estructural es el `account_strategy_id` del binding vigente, id estable sin framework de revisiones (D2-01 congelado; R1). No se propone config hash: un hash del snapshot embebido sería derivable (redundante) y un hash sobre config no embebida sería azúcar de auditoría, no corrección — YAGNI.
- Datos derivados (nunca autoridad): `logical_exposure` firmado (Σ Fills, §6 — puede romper la dirección intencionada ante un breach físico, R4), `avg_fill_price` ponderado, `filled_qty` total, contador de Orders.
- State MM: blob `mm_state` namespaced dentro del estado de la Operation, propiedad exclusiva del MoneyManagement del binding (progresión Gerard, niveles de protección corrientes, etc.). El Core no interpreta su contenido; sólo lo persiste y lo entrega al MM dueño.

### 2.2 Order

- Definición: instrucción concreta y executable emitida por MM sobre una Operation, enviada a un execution venue vía adapter. Es **entity del aggregate Operation**: no existe fuera de su Operation, no tiene lifecycle autónomo, y su identidad es estable a través de modify/replace.
- Identidad: `order_id` = `client_order_id` UUIDv7 generado por Core al construir la Order. Es el idempotency key hacia el venue y viaja como correlation tag (ProjectX `customTag`, Tradovate `clOrdId`, NT tag/comment — evidencia D1 Front D). `provider_order_id` es el ID nativo del venue, nullable hasta el ack.
- Campos: `order_id`; `operation_id`; `account_strategy_id`; `account_id`; `contract_id` (heredado del pin de la Operation); `role` (ENTRY/ADD/REDUCE/EXIT — informativo de auditoría, derivado de la decisión MM que lo creó); `order_type` (MARKET/LIMIT/STOP); `side` (BUY/SELL); `qty` (contracts, unidades del Contract); `original_qty`; `limit_price`/`stop_price` cuando aplique; `filled_qty` (Σ fills de la Order); `avg_fill_price` (derivado); `status`; `order_version` (incrementa en modify; sin tabla de eventos — historia por Kafka/OTel, R9); `replaces_order_id` / `replaced_by_order_id` (cadena de replace cancel+new); `decision_id` (id de la decisión MM que la originó); `created_at`/`updated_at`; `run_mode`/`run_id`.
- Consistencia con la dirección (R2): toda Order se valida al construirse contra la dirección de la Operation — orders ENTRY/ADD con `side == direction`; orders REDUCE/EXIT con `side` opuesto y `qty ≤ logical_exposure` vigente. Una violación de esta validación es un bug de construcción y se rechaza localmente; el venue sigue siendo autoridad de lo que efectivamente ejecuta (§6).
- Cardinalidad: `Operation 1 → 0..N Order`; múltiples Orders pueden estar vivas simultáneamente (entries paralelas, adds working mientras otra reduce). No se asume semántica MT4 ni que una Order produce un único Fill.

### 2.3 Fill

- Definición: hecho de ejecución inmutable reportado por el venue. Nunca se edita, se borra ni se ajusta (ni siquiera ante un breach — R4); un fill tardío o de reconciliación se agrega igual que uno en tiempo real.
- Identidad: `provider_execution_id` del venue + `account_id`. Dedup key global: `(account_id, provider_execution_id)`. Requisito de adapter: toda ejecución debe exponer un execution id nativo (ProjectX `Trade` con id + `orderId`; NT `Execution` con executionId/orderId) o sintetizar uno determinístico en el adapter (ej. `orderId:executionId`, `orderId:seq`); el dominio nunca dedupea por heurística de precio/tiempo.
- Campos mínimos: `provider_execution_id`; `account_id`; `order_id` (client); `provider_order_id`; `operation_id` (resuelto vía correlación del adapter, §8.2); `account_strategy_id` (stamped para routing/queries); `contract_id`; `side`; `qty`; `price`; `executed_at` (venue time); `received_at`; `commission`/`swap` cuando el venue los entregue; `operation_event_seq` (secuencia con que el state owner lo aplicó, R5); `source` (EXECUTION | RECONCILIATION | HISTORY) + `run_mode`/`run_id`.
- Orden semántico: `(executed_at, provider_execution_id)`; la exposición es una suma conmutativa (§6.3-A), por lo que el orden de llegada no afecta el valor, sólo el orden de disparo de reacciones MM (§6.3-B).

### 2.4 Position

- Definición: exposición física observada/reconciliada del venue para `(account_id, contract_id)`, en modelo netting (los venues futures V1 de la cohorte D1 reportan posición neta por cuenta+contract: ProjectX `Position = account+contractId+size+averagePrice`). NO es Operation, no es aggregate del execution path y no tiene lifecycle propio.
- Shape de dominio nuevo (R8): la proyección Futures **reemplaza el shape** del `PositionSnapshot` actual (que es MT-oriented a nivel ticket/trade: `TradeID`, `Ticket`, `StrategyID`, `ReferenceTradeID`, `LotSize`, upsert por `(account_id, ticket)`) — no es ese DTO con un `contract_id` agregado. Campos: `account_id`; `contract_id`; `net_qty` (signed, neta); `avg_price`; `venue_updated_at`; `observed_at`; `origin` (ECHO | NATIVE | MIXED_UNKNOWN). Contrato upsert/delete por batch ausente, igual semántica de consistencia que hoy pero sobre la identidad neta.
- Autoridad: exclusivamente eventos/snapshots del venue. Cualquier valor lógico está prohibido en su cómputo. Un fill de una Operation puede coexistir con exposición NATIVE en la misma Position física: la atribución por Operation es 100% lógica (vía Order), nunca se infiere desde deltas de Position.

### 2.5 Cardinalidades

| Relación | Cardinalidad | Nota |
|---|---|---|
| AccountStrategy → Operation | 1 → 0..1 no terminal; 0..N histórico | D2-02 congelado |
| Operation → Order | 1 → 0..N | entradas, adds, reducciones, exits |
| Order → Fill | 1 → 0..N | partial fills normales (evidencia NT `OnExecutionUpdate`) |
| Account+Contract → Position | 1 → 0..1 | netting por contract |
| Operation → Position | 0 correspondencia directa | agregación/netting sólo a nivel cuenta |
| Operation → Trade | 1 → 0..1 | diferido a The Lab (`DEFERRED_TO_THE_LAB`); no se congela shape |

### 2.6 Autoridad vs derivado

| Dato | Autoridad | Derivado de |
|---|---|---|
| Estado/dirección/pin de Operation | Estado del aggregate (dirección sellada por la Signal; transiciones §3.1) | — |
| `logical_exposure` (firmado) | — | Σ Fills de la Operation (nunca clamped, R4) |
| Estado de Order | Venue (con guards de corrección forward) | — |
| `filled_qty`, `avg_fill_price` | — | Σ Fills de la Order |
| `net_qty` Position | Venue (snapshots/eventos) | — |
| Terminalidad de Operation | Intent de terminación + guards (§3.1) | nunca derivada sola de fills ni de Position |

## 3. Lifecycles y tablas de transición

### 3.1 Operation

```text
CREATED ──MM emite ≥1 entry Order que sale hacia el venue──▶ PENDING_ENTRY
CREATED ──MM resuelve sin acción ejecutable / rechaza entry──▶ TERMINAL(MM_NO_ACTION | ENTRY_REJECTED)
PENDING_ENTRY ──primer Fill con qty>0──▶ ACTIVE
PENDING_ENTRY ──entry orders terminales sin fill y MM decide no reintentar, o TTL de entry──▶ TERMINAL(ENTRY_EXPIRED | ENTRY_FAILED)
ACTIVE ──exposure=0 ∧ 0 live orders ∧ intent de terminación pendiente──▶ TERMINAL(CLOSED)
ACTIVE/PENDING_ENTRY/CREATED ──ForceClose registra intent──▶ (sigue el estado actual)
cualquier estado no terminal ──exposure=0 ∧ 0 live orders ∧ intent SAFETY_PLANE──▶ TERMINAL(SAFETY_FLATTEN)
```

- Materialización (CREATED): la Signal OPEN fue aceptada y materializada (D2-02/A2: la Operation existe ANTES de MM/Orders/Fills). Guards de materialización: `now ≤ signal.valid_until` (señal expirada NO crea Operation; telemetría `SIGNAL_EXPIRED`), compatibilidad Strategy↔MM del binding (D2-03), resolución/pin de `contract_id` (D2-01) y **sella de `direction` desde la Signal** (R2). Si MM resuelve sin acción ejecutable, la Operation termina con motivo explícito (A2).
- `PENDING_ENTRY`: existe al menos una Order de entrada viva (`PENDING_SUBMIT/SUBMITTED/WORKING`) intentando exposición, sin fills. Una LIMIT/STOP working es estado operacional material.
- `ACTIVE`: primer Fill con exposición. Adds/reducciones/posteriores son Orders/Fills de la misma Operation; la exposición puede volver a cero temporalmente sin terminalidad.
- **Terminación (R3):** la transición a TERMINAL es uniforme y exige simultáneamente (guards evaluadas por el state owner en el momento de la transición): `logical_exposure == 0`, cero Orders vivas (`PENDING_SUBMIT/SUBMITTED/WORKING`), y un **intent de terminación registrado** (`termination` = decisión MM explícita de no continuar, o ForceClose del safety plane). ForceClose NO terminaliza instantáneamente: registra el intent (`requested_by=SAFETY_PLANE`), cancela Orders vivas, emite Orders de cierre según el plano de seguridad, y la Operation queda TERMINAL recién cuando los guards se satisfacen (puede requerir esperar partial fills y reconciliar fills tardíos). `SAFETY_FLATTEN` es el eventual `terminal_reason`. `terminal_reason` obligatorio (§3.3).
- Quién puede iniciar terminación: MM (decisión normal) o el safety plane vía ForceClose; ambos son intents entregados al state owner. Ningún otro componente (Position projection, front, gateway) muta el lifecycle.
- `direction` immutable desde la materialización (R2); una Operation nunca cruza de LONG a SHORT ni viceversa por construcción de sus Orders. Un breach físico puede dejar exposición firmada incompatible con la dirección (§6.2, R4) sin cambiar la dirección lógica.
- Reversal = terminal de la Operation actual + nueva Signal OPEN → nueva Operation (A2 congelado).
- Signal `REDUCE/CLOSE/CLOSE_ALL` con Operation inexistente → no-op con telemetría (`NO_ACTIVE_OPERATION`); no crean nada. Signal `OPEN` con Operation no terminal existente → se entrega a MM como acción sobre la Operation actual (D2-02), nunca crea segunda Operation.
- Recovery tras restart: §8.5. El estado se recupera de checkpoints StateFun + PG y se reconcilia contra el venue; la terminalidad no se infiere de la ausencia de mensajes.

### 3.2 Order

```text
PENDING_SUBMIT ──submit aceptado por adapter──▶ SUBMITTED
SUBMITTED ──ack/working del venue──▶ WORKING
PENDING_SUBMIT/SUBMITTED ──reject del venue o fallo de transporte terminal──▶ REJECTED
WORKING ──Σ fills ≥ qty (o venue reporta FILLED)──▶ FILLED
WORKING ──cancel confirmada con Σ fills < qty──▶ CANCELLED
WORKING ──modify nativo aceptado──▶ WORKING (order_version++, sin tabla de eventos)
WORKING ──replace como cancel+new──▶ CANCELLED(REPLACED) + nueva Order (replaces_order_id)
WORKING ──expiración venue (TTL/GTD)──▶ EXPIRED
CANCELLED/EXPIRED ──fills tardíos dejan Σ fills ≥ qty──▶ FILLED (única corrección forward permitida)
```

- `PENDING_SUBMIT`: Order construida por MM, aún no entregada (delays anti-detección, backpressure del adapter).
- Partial fill NO es un estado: es `WORKING` con `filled_qty > 0`. Menos estados, menos ambigüedad; `filled_qty` es el dato.
- Reject/cancel/expiry de una Order NUNCA termina la Operation (A2): MM decide retry/replace/replanear con una Order nueva (nuevo `order_id`, misma `decision_id` si es reintentos del mismo intent).
- Corrección forward única: si una Order `CANCELLED/EXPIRED` recibe fills tardíos que la dejan completamente ejecutada, su estado se corrige a `FILLED` (el venue ejecutó; los fills son hechos). `REJECTED` nunca se corrige. `FILLED` nunca se degrada. El historial de cambios de estado queda en Kafka/OTel, no en tablas de eventos (R9).
- `race fill-vs-cancel`: ambos eventos se procesan; el fill se appendea idempotentemente; el estado final de la Order es el último estado autoritativo del venue con la corrección forward de arriba. Las **cantidades derivadas** convergen siempre (§6.3-A); la reacción MM al resultado es parte del procesamiento serializado (§6.3-B).

### 3.3 Terminal reasons (propuesta técnica, ratificación manager)

- `MM_NO_ACTION` (MM no resolvió acción ejecutable desde CREATED); `ENTRY_REJECTED` (orders entry rechazadas y MM desiste); `ENTRY_EXPIRED` (TTL de entry/signal sin fill); `ENTRY_FAILED` (fallo de transporte terminal sin fill); `CLOSED` (cierre normal MM: full reduction, CLOSE/CLOSE_ALL ejecutado, stop/target de MM); `SAFETY_FLATTEN` (intent ForceClose del plano safety/provider completado según guards, R3).

## 4. Invariantes

- I1: como máximo una Operation no terminal por `(execution_account_id, account_strategy_id)` (D2-02).
- I2: toda Order pertenece a exactamente una Operation; todo Fill pertenece a exactamente una Order (y por transitividad a una Operation). No hay fills huérfanos: un evento sin resolución de identidad (correlación del adapter ausente) va a cuarentena de eventos con métrica, nunca se inventa atribución.
- I3: `direction` de la Operation es sellada por el OPEN Signal aceptado en la materialización (R2) e immutable; toda Order se construye consistente con ella (entry `side == direction`; reduce lado opuesto con `qty ≤ exposure` vigente — guard de construcción de nuestros comandos). El venue sigue siendo autoridad de lo que ejecuta físicamente (§6.2).
- I4: `logical_exposure == Σ±Fill.qty` **sobre los hechos reales, sin clamp** (R4); se recalcula de los Fills, jamás se ajusta manualmente ni se lee desde Position. La suma puede producir un valor incompatible con la dirección intencionada ante un breach físico; eso se marca, no se corrige (I6).
- I5: TERMINAL requiere la evaluación simultánea de guards: `{exposure == 0 (valor firmado real)} ∧ {0 Orders vivas} ∧ {intent de terminación registrado}` (A2 + R3). Un estado de Order no termina la Operation; exposición cero temporal no termina la Operation; Position nunca termina la Operation; un ForceClose tampoco por sí solo.
- I6: **fill truth es immutable y nunca se clampa ni se sintetiza** (R4): ante un fill que exceda lo ordenado o invierta la exposición intencionada, el hecho se conserva y la Operation marca `exposure_invariant_breach` + telemetría `EXECUTION/EXPOSURE INVARIANT BREACH` fail-visible. Prohibido: synthetic fills, reparación automática, creación automática de Operation nueva. La reacción (incluida una decisión del safety plane) pasa por intents al state owner.
- I7: todo evento de ejecución es idempotente por su identity natural (§5.1); reprocesarlo no cambia estado ni exposición. El horizonte de dedup de fills cubre toda la vida de la Operation no terminal (R7).
- I8: las transiciones de estado son monótonas y guardadas; no hay paths que revivan aggregates terminales (única excepción: corrección forward `CANCELLED/EXPIRED → FILLED` de Order). **Alcance de determinismo (R5):** las cantidades derivadas de hechos son conmutativas; el procesamiento de decisiones (MM, transiciones disparadas por llegada) es serializado por el state owner y determinístico ante la misma secuencia ordenada de eventos, no ante órdenes de llegada arbitrarios.
- I9: una cuenta no puede mutar el estado de otra: todo mutador de estado vive en el contexto keyeado por `(execution_account_id, account_strategy_id)`; no existe store global mutable de cuentas accesible por MM (§8).
- I10: `Position` es write-only desde eventos del venue y read-only para el resto; jamás dispara transiciones de Operation.
- I11: toda entidad carries `run_mode` + `run_id` (provenance LIVE vs simulado) — constraint de reutilización para replay/backtest del D1.
- I12: fills son append-only; la mutación de estado se limita a columnas de status/version de Operation/Order; sin tablas de eventos en V1 (historia en Kafka/OTel, R9).
- I13 (R6): **ningún comando físico puede haber sido entregado al venue sin un estado Core commiteado** que lo represente (garantía 2PC del egress, §5.6); complementariamente, un resubmit con el mismo `client_order_id` nunca genera una segunda orden física (dedup del adapter).

## 5. Idempotencia, cancel/replace, races y crash window

### 5.1 Idempotency keys

| Flujo | Key | Mecanismo |
|---|---|---|
| Signal procesada | `(account_strategy_id, signal_id)` | dedup set en el keyed state; replay de Kafka no re-materializa |
| Orden enviada | `client_order_id` (UUIDv7) | viaja como correlation tag al venue; dedup del adapter para resubmits (R6) |
| Fill | `(account_id, provider_execution_id)` | dedup set con horizonte = vida de la Operation no terminal (R7) + PK inmutable en PG |
| Decisión MM | `decision_id` (UUIDv7) | las Orders la referencian; replay de la misma decisión no duplica Orders |
| Replace | `replace_request_id` | idempotencia de modify/cancel (venue puede duplicar acks) |
| Reconciliation | mismos keys que el flujo normal | los hechos de reconciliación pasan por las mismas guards |

### 5.2 Cancel/replace

- Replace preferente: si el venue soporta modify nativo (ProjectX `order-modify`, NT `Change`), la Order conserva `order_id` y `provider_order_id` e incrementa `order_version` (snapshot previo/posterior queda en Kafka/OTel; sin tabla de eventos, R9). `qty` refleja la cantidad working actual; `original_qty` se preserva.
- Replace cancel+new (venues sin modify): la Order vieja termina `CANCELLED(REPLACED)`, se crea una Order nueva con `replaces_order_id` y la misma `decision_id`; la cadena es auditable vía Kafka/OTel y el intent MM queda agrupado por `decision_id`.
- Cancel request = comando con id propio (`replace_request_id`/`cancel_id`); el ack del venue es el que transiciona la Order; la ausencia de ack activa timeout del adapter → reconciliación (query del estado real), no asunción.

### 5.3 Race fill-vs-cancel (caso 4)

- Ambos eventos entran por la cola serializada de la Operation y se aplican como hechos: el fill se agrega (dedup por execution id), la cancelación se registra. Reglas de convergencia de estado de Order: si el venue confirma cancelled con `Σ fills < qty` → `CANCELLED` con `filled_qty` retenido; si los fills acumulados alcanzan `qty` (aunque el ack de cancel llegó primero) → corrección forward a `FILLED`. Exposición final = Σ fills en ambos casos (conmutativa). La secuencia de reacciones MM difiere según el orden de llegada en vivo (§6.3-B); el estado derivado y la coherencia Order/Operation quedan garantizados en ambos órdenes.

### 5.4 Duplicados y replay

- Kafka at-least-once + replays: todos los handlers aplican I7. Duplicados de ejecución tras reconnect/replay (receta Databento/CME aceptada en D1): dedup por `provider_execution_id` con el horizonte de R7, más la PK inmutable en PG como segunda barrera.
- Eventos de reconexión que traen snapshot completo de orders/posiciones: cada snapshot se materializa como eventos diff-only (estado venue reportado por Order/Position) que pasan por las mismas guards monótonas.

### 5.5 Fill dedup — horizonte sin TTL (R7)

- El dedup set de fills del keyed state **no tiene evicción por TTL**: persiste durante toda la vida de la Operation no terminal y se reconstruye desde el checkpoint (el set es keyed state) o desde `echo.fills` en el caso de gap frío. El horizonte relevante de una Operation/recovery queda así cubierto por construcción: un fill ya aplicado no puede volver a mutar la exposición mientras la Operation pueda mutar.
- La memoria es acotada por diseño: V1 tiene 1 Operation no terminal por AccountStrategy (D2-02) y su cantidad de fills es naturalmente pequeña (contratos futures, horizonte intradía/multi-day); al llegar a TERMINAL el set se evicta completo — un duplicado posterior no puede mutar exposición (Operation terminal, guard I5) y la PG PK lo rechaza con métrica.
- No se requiere query síncrona a PG por Fill en el hot path: la primera barrera es el dedup set en el keyed state (consistente con la exposición porque ambos viven en el mismo estado atómicamente commiteado); la PG PK es segunda barrera de profundidad.

### 5.6 Crash window / duplicate physical order (R6) — estrategia V1

Combinación mínima de dos mecanismos, con la garantía central documentada:

- **M1 — Atomicidad state+egress del runtime (garantía documentada, carga de la prueba):** el runtime desplegado es `apache/flink-statefun:3.2.0` (`v3/core/deploy/flink-statefun/develop/docker-compose.yml`). El Javadoc oficial de `KafkaEgressBuilder` (3.2) documenta que con `DeliverySemantics.EXACTLY_ONCE` el egress "will write all messages in a Kafka transaction" que "will be committed to Kafka on a checkpoint", con la restricción de que el transaction timeout "must not be larger than the transaction.max.timeout.ms value configured on Kafka brokers (by default, this is 15 minutes)" (URL en §14). Bajo esta semántica, el estado de `echo/operation` y el comando de la Order se commitean atómicamente (2PC): el escenario "comando A llegó al venue pero el checkpoint con A se perdió" **no puede ocurrir** — o ambos commitean (orden registrada durablemente y publicada), o ninguno (transacción abortada, comando nunca visible, evento re-procesado, MM re-decide desde el estado rollbackeado). Por la misma razón `client_order_id` puede seguir siendo UUIDv7: bajo 2PC una identidad regenerada post-crash nunca convive con un artefacto físico de la intent previa (no existe tal artefacto).
- **M2 — Idempotencia del adapter por `client_order_id` (cubre el path at-least-once restante):** el consumo del topic de comandos por el adapter es at-least-once (el `CommandConsumer` actual usa commit híbrido con auto-commit de respaldo — evidencia `v3/bridge/internal/session/command_consumer.go`), y un redelivery post-ack-parcial puede reenviar un comando ya entregado al venue. El adapter mantiene un **submission registry** en memoria + reconstrucción por reconexión: al arrancar/recuperar, sincroniza las open orders del venue por su correlation tag (ProjectX `Order/searchOpen` + `customTag`; NT `Orders` + tag) y al recibir un submit cuyo `client_order_id` ya tiene una orden viva en el venue, lo mapea a esa orden existente (no-op físico con métrica `DUPLICATE_SUBMIT_SUPPRESSED`) en lugar de colocar una segunda. El venue es el registro durable de órdenes vivas; el registry local cubre además órdenes ya terminales en la ventana corta de redelivery.
- **Requisitos de despliegue (condiciones de validez de M1, marcadas como config, no inferencia de comportamiento):** (a) los specs de egress de comandos en `module.yaml` deben declarar `EXACTLY_ONCE` con transaction timeout ≤ broker `transaction.max.timeout.ms` — el `module.yaml` actual no declara delivery semantics, por lo que esto es un requisito explícito de la SPEC (la default documentada es AT_LEAST_ONCE); (b) los consumers del topic de comandos deben leer con `isolation.level=read_committed` (comportamiento documentado de Kafka para consumidores sobre productores transaccionales); (c) el endpoint remoto del Core (las functions son HTTP remoto) participa del protocolo de checkpoint estándar de Flink, que es el mismo mecanismo que hoy protege `execution_store`/`pending_mm`.

## 6. Exposición lógica y determinismo

### 6.1 Derivación

- Definición: `logical_exposure(op) = Σ_fills sign(fill) × qty` sobre **todos los fills reales**, con `sign = +1` si `fill.side == op.direction`, `-1` en caso contrario. Unidad: contracts según spec del Contract pinneado (no pips; constraint cross-market V1 del proyecto).
- Ejecución incremental: contador firmado mantenido en el keyed state, recalculable siempre desde `echo.fills` (PG) como verificación; cualquier divergencia contador↔recomputo es bug y se alarma.

### 6.2 Fill truth sin clamp (R4)

- Las guards de construcción (I3) impiden que **nuestros** comandos emitan reducciones mayores que la exposición; pero un fill físico anómalo (bug del venue, race, comportamiento del provider) puede dejar `logical_exposure` negativo respecto de la dirección intencionada (ejemplo: LONG +1 y un SELL 2 inesperado → exposición firmada −1).
- En ese caso: el fill se conserva como hecho (I6), la exposición firmada mantiene su valor real, la Operation marca `exposure_invariant_breach` y emite telemetría `EXECUTION/EXPOSURE INVARIANT BREACH` fail-visible. Prohibido clamp, synthetic fill, Operation nueva automática o cualquier reparación silenciosa. MM recibe el evento de breach en su stream y decide (incluido pedir flatten); el safety plane puede actuar vía ForceClose (R3). La política de reconciliación física sigue fuera de scope (`DT-EF-POSITION-RECONCILIATION-05`).
- El guard de TERMINAL usa la exposición firmada real (I5): una Operation con breach no puede terminalizar mientras la exposición real no sea cero.

### 6.3 Commutatividad de hechos vs decisiones stateful (R5)

- **A. Fact-derived state (conmutativo):** total filled qty, `logical_exposure` firmado, `avg_fill_price` ponderado. Estos valores no dependen del orden de llegada; ante cancel/fill cruzados o fills tardíos convergen siempre al mismo valor.
- **B. Stateful decision processing (serializado, no conmutativo):** las decisiones de MM y las transiciones que disparan se toman sobre eventos en orden, con estado previo. Dos órdenes de llegada distintos pueden producir decisiones live distintas — eso es esperado y aceptable. La garantía correcta es: **same ordered event stream → same decisions** (procesamiento serializado por el state owner, código de dominio puro determinístico).
- **Orden de replay — `operation_event_seq` (adoptado):** el state owner asigna un entero monótono por Operation a cada input event de dominio de ejecución que procesa (signals, acks/status de orders, fills, intents de terminación) y lo sella en las escrituras durables (fills, estado de orders, estado de la Operation). No se crea una tabla de eventos nueva (R9): la secuencia viaja en los propios registros. Contrato de replay/post-V1: mismo stream ordenado de eventos de ejecución (por `operation_event_seq`) + stream de mercado grabado (input de MM) → mismas decisiones. No se afirma que un arrival ordering arbitrario reproduzca el mismo outcome live.

## 7. Position / reconciliation boundary

### 7.1 Autoridad física y shape (R8)

- Position se actualiza únicamente con eventos/snapshots de posición del venue, proyectados por una función con el mismo slot y patrón que la actual (ingress periódico por cuenta, async batched writer, upsert idempotente + delete por ausencia en batch) pero con el **shape nuevo neto** `(account_id, contract_id, net_qty, avg_price, …)` — no el `PositionSnapshot` MT por ticket (§2.4). La proyección legacy `active_positions` no se toca.
- Sin I/O en el hot path de decisiones; la proyección es consumidor aparte del mismo stream de observaciones del venue.

### 7.2 Correlación con Operations sin atribución falsa (Q2)

- La atribución de fills a Operations es **estructural**: cada Fill llega referenciando la Order que Echo emitió (la correlación `client_order_id`/`operation_id` la porta el adapter desde su submission registry, §8.2). No se atribuyen fills por inferencia de deltas de Position.
- En cuentas netting, la Position física agrega todo (Operations Echo + trading NATIVE/manual); V1 no intenta descomponerla por Operation ni reclama ownership físico por Strategy. La verdad por Operation es 100% lógica (I4).
- La identidad física de Position es `(account_id, contract_id)` — coincide con el modelo de los venues futures de la cohorte (netting por contract), por lo que no se requiere modo hedging en V1.

### 7.3 Comparación y mismatch V1

- Comparador periódico (proyección, fuera del hot path): por `(account, contract)`: `physical_net_qty` vs `Σ signed exposure de Operations no terminales sobre ese contract + exposición NATIVE conocida si existe`. Delta fuera de tolerancia → evento/telemetría `POSITION_MISMATCH{account, contract, physical, logical, delta, ts}` + surface de observabilidad. Un `exposure_invariant_breach` (R4) típicamente se manifiesta aquí también.
- V1 NO hace auto-repair, synthetic fills, remapping ni subsystem de reconciliación (DT-EF-POSITION-RECONCILIATION-05 diferido, reafirmado). El mismatch es señal para el operador/safety plane; la única reacción automática permitida es la telemetría y (si el owner lo habilita por config) el bloqueo de nuevas aperturas de esa cuenta por el safety plane existente, nunca la mutación del estado lógico.
- Caso 7 (mandato): dos Strategies de la misma Account con exposición opuesta sobre el mismo Contract → dos Operations lógicas independientes (+N y −M), una Position física neta (N−M). Ambas verdades coexisten; el comparador usa la suma.

## 8. Runtime: ownership, aislamiento y recovery

### 8.1 State owner y partition key

- Owner del estado: función StateFun nueva `echo/operation`, una instancia por `key = execution_account_id + ":" + account_strategy_id`. Es el único mutador del estado de Operation/Order y de la exposición, el contexto de invocación de MM, y el asignador de `operation_event_seq`. Serializa todos sus mensajes (garantía StateFun por key) → determinismo de decisión por cuenta+estrategia (§6.3-B).
- MM vive como plugin de dominio invocado dentro de `echo/operation`: recibe el contexto de esa Operation + snapshots de cuenta/instrumento (patrón join de `MMEngineFn` reutilizado) y devuelve decisiones (0..N Order requests, modify/cancel, intents de terminación, mutación de su `mm_state`). MM nunca accede a estado de otras keys ni a un store global (I9). El aislamiento es por construcción del runtime, no por disciplina.
- `echo/signal_fanout` (función nueva, sucesora del patrón `ExecutionPlannerFn`): lee bindings habilitados por strategy desde kache, filtra por whitelist/estado de cuenta (patrón RFC-007) y entrega la Signal a cada `echo/operation` por su key, preservando el orden intra-evaluación (`signal_seq`).

### 8.2 Correlación evento→operación (adapter-owned, R9)

- El adapter de ejecución posee el **submission registry** (§5.6-M2): conoce, por `client_order_id`, la `(account, account_strategy_id, operation_id, order_id)` de cada comando que emitió. Publica los execution events (acks, status, fills) en `echo.execution-events.v1` **ya correlacionados** y con Kafka key = op key → el ingress los entrega directo a `echo/operation` (no existe función router en Core). Los eventos del venue sin origen Echo (trading manual, posiciones) van a los topics de observación/proyección (§7), no al state owner.
- Esto elimina la función `echo/execution_router` y su registry en Core: la correlación es un dato de transporte que el adapter stamped al enviar y devuelve al recibir (mismo primitivo D1: customTag/clOrdId); la resolución de eventos sin tags (reconnect/replay) queda cubierta por el registry que el adapter ya debe sostener para M2, reconciliando open orders por tag.

### 8.3 Topología final (R9)

| Componente | Tipo | Key | Contenido |
|---|---|---|---|
| `echo/signal_fanout` | función StateFun (nueva) | strategy_id | fan-out de Signal a AccountStrategies habilitadas |
| `echo/operation` | función StateFun (nueva) | `account:strategy` | aggregate Operation: lifecycle, Orders, Fills, exposición, MM, seq; writer PG async embebido (patrón `PositionSyncFn`) |
| position projection | shape-replace del slot `PositionSyncFn` (R8) | account_id | proyección neta `(account, contract)` |
| `echo.signals.v1` | ingress (nuevo) | strategy_id | Signal canónica D2-03 emitida por StrategyEngine |
| `echo.execution-events.v1` | ingress (nuevo) | op key | eventos normalizados del venue, correlacionados por el adapter |
| `echo.order-commands.{account_id}.v1` | egress (familia nueva) | client_order_id | OrderRequest / Modify / Cancel; **EXACTLY_ONCE + read_committed (§5.6)** |
| `echo.position-observations.v1` | ingress (nuevo, proyección) | account_id | observaciones netas de posición del venue |
| configs (existente) | kache/KVS | — | bindings AccountStrategy, specs Instrument/Contract + hot mapping |

- Las funciones nuevas se registran en `module.yaml` con ingress/egress propios (patrón exacto del existente); la topología legacy queda intacta durante la migración.

### 8.4 Event ordering

- Orden por cuenta+estrategia: Kafka preserva orden por key con producer idempotente (config explícita in-flight limitado); StateFun procesa serialmente por instancia → las Signals y eventos de una Operation se aplican en orden y las decisiones son reproducibles ante la misma secuencia (I8).
- Orden intra-evaluación: StrategyEngine sella `signal_seq` monótono por strategy; el fan-out preserva el orden por key; `echo/operation` rechaza regresiones (dedup + telemetría). CLOSE_ALL→OPEN en la misma evaluación se aplica en orden (A1: procesamiento determinístico).
- Orden venue: `executed_at` + `provider_execution_id` para el orden semántico de fills; `operation_event_seq` fija el orden efectivamente observado para replay (§6.3-B).

### 8.5 Crash / recovery

- Capa 1 (hot): Flink/StateFun checkpointing del keyed state (infra existente) — incluye dedup sets (R7) y `mm_state`. La atomicidad checkpoint↔egress cierra la ventana de crash de submits (§5.6).
- Capa 2 (durable): PG `echo.operations` / `echo.orders` / `echo.fills` escrita por el writer async embebido en `echo/operation` (upserts idempotentes; patrón `PositionSyncFn`). Al detectar gap/divergencia de checkpoint, la instancia reconstruye el estado no terminal desde PG (operaciones no terminales + Orders vivas + todos los fills + `operation_event_seq` máximo).
- Capa 3 (física): reconciliación de venue al reconectar — resubscribe + query de estado autoritativo (ProjectX `Order/searchOpen` + positions; NT `Orders/Executions/Positions`) + fetch de historial de executions desde el último hecho visto (capacidad documentada en D1 Front D por transporte); el adapter re-correlaciona por tag y los hechos entran con `source = RECONCILIATION|HISTORY` por las mismas guards.
- Convergencia: las cantidades derivadas de hechos convergen siempre (§6.3-A); la terminalidad exige guards reales; duplicados absorbidos por I7 (casos 5 y 6 del mandato).

### 8.6 Hot path y persistencia

- En el hot path (signal → materialización → sizing → submit) no hay I/O remoto síncrono: snapshots de cuenta/instrumento se sirven de las KVS functions / kache (patrón actual); la proyección PG es escritura async batched embebida (patrón `PositionSyncFn`/`AccountSyncFn`); ningún query a PG por Fill o por comando (R7).
- Persiste durablemente: identidad/estado de Operation y Orders (status/version + seq), todos los Fills (inmutables + seq), intents/decisiones terminales y `mm_state` (blob, para recuperar la progresión económica). En bounded keyed state (checkpointed): dedup sets (horizonte por Operation, R7), contadores de exposición, `operation_event_seq`.
- Volumen: el estado vivo por key es acotado (1 Operation no terminal + sus Orders vivas + sets acotados); la historia completa vive en PG, no en el estado caliente.

### 8.7 Backtest / replay reuse

- Las entidades, la máquina de transiciones y el contrato de decisiones MM viven como paquetes Go puros (SDK domain layer), sin imports de Kafka/StateFun; las funciones StateFun son adaptadores finos que invocan el mismo motor. `SimExecution` implementa el mismo contrato `ExecutionEvent` que los adapters reales (fills determinísticos por seed).
- Contrato de replay (R5): mismo stream ordenado de eventos de ejecución (`operation_event_seq`) + stream de mercado grabado → mismas decisiones. El backtester futuro ejecuta `Signal → Operation → MM → Order → Fill → exposición` con el mismo código de dominio y Clock/event-time inyectables, cumpliendo la constraint de reutilización del D1 sin `*_live` vs `*_backtest`.

## 9. Mapa físico Echo V3 — REUSE / EXTEND / ADAPT / REPLACE / DEFERRED_DEBT

Baseline `xKoRx/echo@372af59a` (re-verificada en el repair). Clasificación con evidencia física (repo/path/símbolo).

| Pieza V3 actual | Disposición | Base física y razón |
|---|---|---|
| StateFun runtime + module.yaml ingress/egress + Go SDK | **REUSE** | `v3/core/deploy/flink-statefun/develop/module.yaml` (ingress/egress por topic, targets `echo/*`); `v3/sdk/statefun/constants.go`; runtime `apache/flink-statefun:3.2.0` (docker-compose). Se registran functions/topics nuevos con el mismo mecanismo; el egress de comandos requiere `EXACTLY_ONCE` (§5.6). |
| kache (cache en-proceso de topics compactados) | **REUSE** | `v3/sdk/kache/`: sirve bindings AccountStrategy + specs Instrument/Contract + hot mapping al fan-out y a MM sin I/O. |
| ExecutionPlannerFn (fan-out por strategy → N cuentas) | **ADAPT** | `v3/core/internal/functions/execution_planner.go` (blob 371bf5e3…): patrón de fan-out con validación RFC-007 y kache. Su sucesor `echo/signal_fanout` consume `Signal` (no ReferenceEvent) y reenvía por `(account, account_strategy)`. |
| MMEngineFn (join snapshots + calculators + comando) | **ADAPT/EXTEND** | `v3/core/internal/functions/mm_engine.go` (blob e725ceb0…): patrón join Account+Instrument y `SendAfter` para delays reutilizables; su lógica se convierte en invocación del plugin MM dentro de `echo/operation` (el estado vive en el aggregate, no en pending cross-message). |
| sdk/mm calculators (fixed_lot/fixed_risk) | **REUSE/EXTEND** | `v3/sdk/mm/calculator.go` (`Calculator`, `CalculationInput/Result`), `fixed_lot.go`, `fixed_risk.go`, `pip_size.go`. Primitivas puras de sizing; se extienden a unidades instrument-spec (tick/contract multiplier ya presentes en `InstrumentSnapshot.TickValue/TickSize/ContractSize`) sin semántica pips en el camino nuevo. |
| CoreCommand | **ADAPT (wire DTO)** | `v3/sdk/domain/reference_event.go` (`type CoreCommand`): transporte con SL/TP físicos+ideales y metadata journal. Continúa en la path legacy; el dominio nuevo emite `OrderRequest` hacia adapters futures; `CoreCommand` no se promueve a aggregate. |
| ExecutionResult | **ADAPT** | mismo blob: colapsa a single result/fill. Se sustituye por `ExecutionEvent` normalizado (ack/status/fill/position) en la path nueva; el Bridge legacy sigue emitiendo `ExecutionResult` hasta su migración (DT-EF-REFERENCE-SIGNAL-03). |
| ExecutionStoreFn + ExecutionStore/OpenExecution | **REPLACE (autoridad)** | `v3/core/internal/functions/execution_store.go` (blob d8c61700…): estado por trade_id con OpenExecution single-fill y dedup por ticket. No es autoridad del lifecycle nuevo (su modelo no representa Order 1→N Fill ni adds); sobrevive como proyección de compatibilidad de la path legacy hasta retiro (registro D1 §6). |
| PositionSnapshot / PositionSyncFn | **REUSE pattern / REPLACE domain shape (R8)** | `v3/sdk/domain/position_snapshot.go` (blob 443b6ba2…): DTO MT-oriented a nivel ticket/trade (`TradeID`, `Ticket`, `StrategyID`, `ReferenceTradeID`, `LotSize`); `position_sync.go` upsertea por `(account_id, ticket)`. El modelo Futures congelado es `Position = Account + Contract` neto: se reutiliza el patrón (ingress periódico, async batched writer, upsert/delete por batch) **reemplazando el shape** — nuevo DTO neto por `(account_id, contract_id)` (§2.4); el projection MT legacy queda intacto para su path. |
| AccountSnapshot / InstrumentSnapshot + acc/inst_snapshot KVS | **REUSE/EXTEND** | `v3/sdk/domain/snapshots.go` (blob d319d0a3…) + `acc_snapshot.go`/`inst_snapshot.go`: KVS por account y broker:symbol para el join MM. Extensión: specs de Contract (expiry/venue ids) sin mezclar instrumento económico con símbolo físico (gap ya registrado en D1). |
| ExecutionPolicy / StrategyConfigFn | **ADAPT** | `v3/sdk/domain/execution_policy.go` (blob 295f7ea2…) mezcla binding+risk+knobs; `strategy_config.go` es KVS por strategy_id. Se separa en `AccountStrategy` (binding+compatibilidad), config MM y knobs de ejecución; el KVS configura bindings por account_strategy. |
| CloseHandlerFn / CloseBatchCommand / CloseAllAccountCommand / automation_evaluator | **REUSE (safety plane)** | `v3/core/internal/functions/close_handler.go`, `v3/sdk/domain/trade_close.go` (CloseCommand/CloseBatch/CloseAllAccount): el flatten account-wide y las acciones de automation son el plano safety/provider existente; entregan ForceClose como **intent** a `echo/operation` (R3) sin convertirse en CLOSE_ALL de Strategy (D2-03). |
| Bridge (sesiones, command consumer, pipes, producer) | **REUSE (patrones) / ADAPTER NUEVO** | `v3/bridge/internal/session/command_consumer.go` (topic dedicado por cuenta, commit híbrido at-least-once, circuit breaker) y `pipe_handler.go` (keys de publicación: ExecutionResult/CloseResult = TradeID, PositionSnapshots = AccountID). Los patterns son el estándar para los adapters futures; el adapter nuevo añade el submission registry + dedup por `client_order_id` (§5.6-M2) y consumo `read_committed` del topic de comandos. El adapter MetaTrader actual no se deforma. |
| trade_journal / canonical_operations / TradeJournalFn | **REUSE intacto (boundary analítico)** | `v3/core/internal/functions/trade_journal.go`, migraciones 062/064. No es state owner del runtime nuevo; la proyección Operation→Trade queda diferida a The Lab (owner 2026-09-26). |
| Hot symbol mapping (Gateway→Kafka→cache) | **REUSE/EXTEND** | `v3/gateway/internal/symbol_mapping_handler.go` (blob a9364d4a…): patrón hot-update compactado; se extiende a mapping `Instrument → Contract`; el pin de Operation vive en el dominio, no en el mapping. |
| PostgreSQL como store duradero + migraciones numeradas | **REUSE** | `v3/sdk/postgres/migrations/` (…064 canonical_operations, 065 lab_curves). Nuevas migraciones para `operations/orders/fills` + proyección neta de posiciones; numeración a coordinar en implementación (la rama E-04 fuera de master reservó 068). |

## 10. Implicaciones de refactor / migración

- SDK domain nuevo (paquete puro): structs `Operation/Order/Fill`, proyección `Position` neta, enums de estado, máquina de transiciones con guards (incluida terminación por intent, R3), `operation_event_seq`, y contratos `MMPlugin` (decisiones) + `ExecutionEvent` (eventos venue) + `SimExecution`. Sin dependencias de infra — es el boundary Q14.
- Core: **2 funciones nuevas** (`echo/signal_fanout`, `echo/operation` — esta última con writer PG async embebido y `operation_event_seq`) + 1 shape-replace del slot de position projection; registro en `module.yaml` (ingress signals / execution-events / position-observations; egress per-account de comandos con `EXACTLY_ONCE` y transaction timeout ≤ broker `transaction.max.timeout.ms`, §5.6). Sin router, sin store function, sin topic de facts (R9).
- PG: migraciones nuevas `echo.operations` (upsert por operation_id, incluye `termination`, `exposure_invariant_breach`, `operation_event_seq`), `echo.orders` (upsert por order_id, `order_version`, sin tabla de eventos), `echo.fills` (insert-only, PK `(account_id, provider_execution_id)`, `operation_event_seq`), `echo.contract_positions` (proyección neta, upsert `(account_id, contract_id)`). Índices por `(account_strategy_id, status)` y `(contract_id)`. Numeración a coordinar con ramas en vuelo al implementar. Sin `order_events`/`operation_events` (historia en Kafka/OTel, R9).
- Adapters futures (D6): implementan `ExecutionEvent` correlacionado + per-account command consumer (`read_committed`) + submission registry con dedup por `client_order_id` y reconciliación de reconexión por tag (§5.6, §8.2); cada rareza de venue queda aislada en su adapter.
- Legacy: la path Reference→ExecutionPlanner→MMEngine→CoreCommand→Bridge sigue operando intacta; el adapter `ReferenceEvent → Signal` (DT-EF-REFERENCE-SIGNAL-03) es el puente futuro. ExecutionStoreFn queda como proyección de compatibilidad.
- Refactors bloqueantes detectados: ninguno nuevo que exceda el registro D1 §6 (Signal boundary limpio + identities/lifecycle eran ya blocking design items; este workstream los especifica). No hay reescritura de Core (Q1 owner-accepted).

## 11. Riesgos y deudas

- **R1 — Ordering Kafka:** la garantía de orden por key depende de config explícita del producer (idempotence + in-flight limitado) y de keys consistentes end-to-end; el adapter debe setear la Kafka key de `echo.execution-events.v1` = op key (contrato del adapter, testeable).
- **R2 — Config EXACTLY_ONCE del egress:** la garantía 2PC de §5.6-M1 es válida sólo si el spec de egress declara `EXACTLY_ONCE` (el `module.yaml` actual no declara delivery semantics) y el broker tolera el transaction timeout configurado; la verificación física del despliegue (y del consumo `read_committed` por el adapter) es requisito de D6 y quedará cubierta por el gate de certificación correspondiente. Marcado como config requirement, no como comportamiento ya demostrado en runtime.
- **R3 — Historial de fills por transporte:** la recuperación post-gap depende de que cada venue exponga execution history; donde no, el gap queda visible como mismatch persistente (fail-visible). Es requisito de selección de adapter, no defecto del dominio.
- **R4 — Capacity 100–200 cuentas:** el diseño multiplica estado por (cuenta×estrategia) y fan-out por signal; el trabajo por instrumento (feed/estrategia) no se multiplica por cuenta (requerimiento del proyecto). El benchmark de capacidad sigue siendo trabajo D6 (misma disposición D1).
- **R5 — ForceClose vs MM concurrently:** un flatten del safety plane mientras MM gestiona puede duplicar intents de cierre; mitigación: hechos idempotentes, dedup por client tag, y terminalidad sólo por guards (R3) — el doble intento converge, no corrupte.
- **R6 — Breach handling residual:** qué safety policy reacciona a `EXPOSURE_INVARIANT_BREACH` (más allá de la telemetría fail-visible) es decisión del safety plane; el modelo V1 define la representación y la reacción vía intents, no la política automática.
- **R7 — Deuda existente heredada:** `DT-EF-POSITION-RECONCILIATION-05` sigue diferida; `DT-EF-REFERENCE-SIGNAL-03` sigue siendo el carril legacy→nuevo; unidades pips legacy (deuda con ID pendiente de ratificación owner) no entra al camino nuevo.
- **R8 — Reloj y `valid_until`:** la validez de Signal y TTLs de entry usan event-time de Core (no del venue); clock skew se resuelve en el diseño técnico de implementación (no cambia el modelo).

## 12. Decisiones owner

- `OWNER DECISIONS REQUIRED: NONE`. El diseño (y el repair R1–R9) vive dentro de las decisiones congeladas D2-01/02/03 y del lifecycle A2, sin reabrirlos y sin `BLOCKED_OWNER_DECISION`.
- Ratificaciones técnicas ordinarias para el manager (no owner, no cambian semántica): (1) enum `TerminalReason` propuesto en §3.3; (2) nombres físicos de functions/topics/tablas nuevas (§8.3/§10); (3) la config de despliegue `EXACTLY_ONCE` del egress de comandos (§5.6), que es requisito técnico de la SPEC.

## 13. Casos de validación (mandato repair §12)

- **Caso 1 — partial fills:** OPEN aceptado → Operation CREATED con `direction` sellada por la Signal (LONG) y contract pinneado → MM BUY 2 → entry Order WORKING → fill +1 + fill +1 (dedup por execution id) → exposición +2, `ACTIVE`. Una Order, dos Fills.
- **Caso 2 — reduce:** Signal REDUCE → MM SELL 1 (guard de construcción: side opuesto, qty ≤ exposición) → fill → exposición +1, misma Operation, `ACTIVE`.
- **Caso 3 — over-reduction anomaly:** LONG exposición +1; llega un fill SELL 2 no ordenado → el hecho se conserva íntegro (I6), exposición firmada = −1 (verdad física), `exposure_invariant_breach = true` + telemetría `EXECUTION/EXPOSURE INVARIANT BREACH`; sin clamp, sin synthetic fill, sin Operation nueva. La dirección lógica sigue LONG e immutable; TERMINAL exige exposición firmada real = 0; MM/safety plane reaccionan vía eventos/intents; el mismatch se refleja también en `POSITION_MISMATCH` si el venue lo confirma.
- **Caso 4 — cancel/fill race:** partial fill + cancel + fill tardío → fill tardío appendeado idempotentemente; estado de Order converge por la regla venue-authoritative + corrección forward (`FILLED` si Σ fills ≥ qty; si no, `CANCELLED` con filled_qty retenido); exposición final = Σ fills (conmutativa) en ambos órdenes de llegada; MM reacciona al estado convergido en su secuencia observada (§6.3-B).
- **Caso 5 — crash after physical submit:** comando A entregado al venue, checkpoint no completado → bajo EXACTLY_ONCE la transacción del egress abortó ⇒ el comando **nunca fue visible** para el adapter (M1); el evento se re-procesa con estado rollbackeado y MM re-decide. Complemento at-least-once: si A ya fue consumido/entregado por el adapter y su offset no se committeó, el redelivery con el mismo `client_order_id` es suprimido por el submission registry / mapeado a la orden viva del venue (M2) — **no existe path end-to-end hacia una segunda orden física** (I13). Caso simétrico (state commiteado, egress perdido) tampoco puede ocurrir: commitean atómicamente.
- **Caso 6 — duplicate historical Fill:** un execution ya aplicado reaparece tras cualquier horizonte → mientras la Operation es no terminal, el dedup set cubre toda su vida (R7) y el fill no muta exposición; si la Operation ya es TERMINAL, el guard I5 impide mutación y la PG PK `(account_id, provider_execution_id)` rechaza con métrica. La exposición nunca incrementa dos veces.
- **Caso 7 — two Strategies, same Account+Contract:** keys `(acct,S1)` y `(acct,S2)` independientes → dos Operations lógicas (+N/−M) con fills atribuidos estructuralmente; Position física neta (N−M) en la proyección nueva; comparador usa la suma; ningún path de estado entre keys (I9).
- **Caso 8 — safety flatten:** ForceClose llega con exposición y Orders vivas → registra `termination{SAFETY_PLANE, SAFETY_FLATTEN}`; cancela Orders working, emite Orders de cierre, espera partial fills/reconciliación; la Operation NO es TERMINAL hasta `exposure==0 ∧ 0 live orders` (I5/R3); entonces `TERMINAL(SAFETY_FLATTEN)`.

## 14. Evidencia

- Vault: `main/10-projects/Echo Futures/Echo Futures.md` (D2-01/02/03 OWNER_CLOSED; lifecycle A2; manager review del repair), `main/10-projects/Echo Futures/Echo Futures — D1 Analysis Pack.md` (matriz Q1/reuse, Front D, `DT-EF-*`), Environment Contract Echo/Forge.
- Repo físico (verificado vía `git show 372af59a:<path>` sobre clon `~/aranea/work/d4-shot1-20260925/echo`; `git fetch` re-verificado en el repair con `origin/master = 372af59a…`): `v3/sdk/domain/reference_event.go`, `v3/sdk/domain/trade_close.go`, `v3/sdk/domain/position_snapshot.go` (DTO MT por ticket — base de R8), `v3/sdk/domain/snapshots.go`, `v3/sdk/domain/execution_policy.go`, `v3/core/internal/functions/{execution_planner,strategy_config,mm_engine,execution_store,position_sync,close_handler,acc_snapshot,inst_snapshot}.go` (`position_sync.go`: upsert `ON CONFLICT (account_id, ticket)` — base de R8), `v3/sdk/statefun/constants.go`, `v3/sdk/mm/calculator.go`, `v3/core/deploy/flink-statefun/develop/module.yaml` + `docker-compose.yml` (runtime `apache/flink-statefun:3.2.0-java11`; module.yaml sin delivery semantics declarada), `v3/bridge/internal/session/command_consumer.go` (commit híbrido at-least-once — base de M2), `v3/bridge/internal/pipe_handler.go`, `v3/sdk/kache/README.md`, `v3/sdk/postgres/migrations/`, `v3/sdk/utils/uuid.go`.
- Garantía StateFun 3.2 (R6-M1), documentación oficial, citas textuales: Apache Flink Stateful Functions, Javadoc `KafkaEgressBuilder` (3.2), https://nightlies.apache.org/flink/flink-statefun-docs-release-3.2/api/java/org/apache/flink/statefun/sdk/kafka/KafkaEgressBuilder.html — con `EXACTLY_ONCE` el egress "will write all messages in a Kafka transaction" que "will be committed to Kafka on a checkpoint"; el transaction timeout "must not be larger than the transaction.max.timeout.ms value configured on Kafka brokers (by default, this is 15 minutes)". Con `AT_LEAST_ONCE` el egress sólo espera ack del producer en checkpoint. La atomicidad estado↔checkpoint (rollback del estado no commiteado al restaurar) es semántica estándar documentada de Flink checkpointing (https://nightlies.apache.org/flink/flink-docs-stable/docs/internals/job_checkpointing/). Marcado explícitamente como **inferencia/config, no comportamiento demostrado**: el spec de egress actual del repo no declara `EXACTLY_ONCE` — su configuración es requisito de la SPEC (§5.6, riesgo R2) y su verificación física queda en D6.

## Fuentes

- [[Echo Futures]] — proyecto canónico y decisiones owner D2-01/02/03.
- [[Echo Futures — D1 Analysis Pack]] — evidence baseline D1 aceptada.
- `xKoRx/echo@372af59a` — source físico V3 inspeccionado (paths en §14).
