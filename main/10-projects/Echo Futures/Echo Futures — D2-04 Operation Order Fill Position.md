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
> Diseño técnico V1 del modelo `Operation / Order / Fill / Position` y su runtime dentro de Echo V3. Respeta sin reabrir las decisiones owner [[Echo Futures]] D2-01 (snapshot + contract pinning), D2-02 (fan-out + single Operation) y D2-03 (Signal + Strategy/MM boundary), y el lifecycle A2 aceptado en [[Echo Futures — D1 Analysis Pack]]. Responde Q2 (Position attribution) y Q3 (Order lifecycle). Baseline físico verificada: `xKoRx/echo origin/master = 372af59a7b83604781346613da01e3d510ea1360` (sin delta). No implementa código productivo y no cierra D2. Incorpora tres rounds de manager review: R1–R9 (`D2_04_MANAGER_REVIEW`), R10–R13 (`D2_04_MANAGER_REVIEW_2`) y R14 (`D2_04_MANAGER_REVIEW_3 = FINAL_CORRECTION_REQUIRED`) — todos registrados en la sección "Manager Repair — 2026-09-26".

## Manager Repair — 2026-09-26

- **R1:** eliminada la "referencia a la versión del binding" de Operation (contradecía D2-01). El snapshot efectivo es embebido y autosuficiente; sin entidades/referencias versionadas; sin config hash (ver rationale en §2.1).
- **R2:** `direction` nace del OPEN Signal aceptado (autoridad técnica Strategy) en el momento de materializar la Operation, antes de MM/Orders; Orders se validan contra esa dirección y nunca la definen retroactivamente (§2.1, §2.2, §3.1, I3).
- **R3:** ForceClose modelado como **intent de terminación** (`termination`), no como terminalización instantánea; toda transición a TERMINAL pasa por la evaluación uniforme de guards; `SAFETY_FLATTEN` es el eventual TerminalReason (§3.1).
- **R4:** prohibido clampear fill truth: la exposición firmada conserva el hecho físico aunque rompa la dirección intencionada; breach marcado `EXPOSURE_INVARIANT_BREACH` fail-visible; sin synthetic fills, sin reparación, sin Operation nueva (I4/I6, §6).
- **R5:** separación explícita entre estado derivado de hechos (conmutativo) y procesamiento de decisiones stateful (serializado; determinístico sólo ante la misma secuencia ordenada de eventos); adoptado `operation_event_seq` sellado por el state owner como orden de runtime (claim de replay acotado por R12); la garantía "independiente del orden de llegada" queda restringida a las cantidades derivadas de hechos (§6.3, I8).
- **R6:** ventana de crash resuelta y probada end-to-end con la garantía documentada de Flink StateFun 3.2 (egress Kafka EXACTLY_ONCE vía transacción commiteada en checkpoint, 2PC) + contrato restart-safe de idempotencia de efectos externos en el adapter (R10: journal durable + resolución contra venue, con gate `UNSUPPORTED_FOR_V1_EXACT_SUBMISSION` para transportes sin capacidad); `client_order_id` permanece UUIDv7 porque bajo 2PC ningún comando físico escapa sin estado commiteado (§5.6).
- **R7:** el horizonte de dedup de fills ya no es TTL: el set de dedup persiste durante toda la vida de la Operation corriente (naturalmente acotado) y se evicta recién en TERMINAL; es keyed state y se restaura con el checkpoint — PG no es autoridad de recovery (acotado por R11); duplicados post-terminal los atrapa el guard de identidad (R13) (§5.5/§5.7, caso 6/D).
- **R8:** reclasificado Position: REUSE del patrón (ingress periódico, async projection writer) / **REPLACE del shape** de dominio — la proyección Futures es neta por `(account_id, contract_id)`, no `PositionSnapshot` MT por ticket + contract_id (§2.4, §7.1, §9).
- **R9:** reducida la superficie nueva por KISS/YAGNI: eliminadas tablas `order_events`/`operation_events`, eliminadas la función `echo/operation_store` + topic `operation-facts` (writer async embebido en `echo/operation`, patrón `PositionSyncFn`) y eliminada la función `echo/execution_router` (la correlación evento→operación la posee el registry de submissions del adapter, ya requerido por R6). Superficie nueva final: 2 funciones StateFun, 2 ingress topics, 1 familia de egress, 4 tablas PG (§8.2, §10). Ampliado mínimamente por R14: + projector dedicado y + egress transaccional de proyecciones/facts, para cerrar la ventana de pérdida de durabilidad (ver R14).
- **R10:** contrato V1 de idempotencia de efectos externos del adapter: journal durable write-ahead + resolución obligatoria de `PENDING` ambiguos contra el venue (open + history por client tag, o idempotencia nativa documentada); transportes sin esa capacidad quedan `UNSUPPORTED_FOR_V1_EXACT_SUBMISSION` (§5.6, caso A).
- **R11:** autoridad de recovery congelada: checkpoint Flink/StateFun + replay de Kafka ingress + egress transaccional; PG es proyección eventual/query-only (idempotente y stale-safe por `operation_event_seq`), nunca autoridad para recrear `mm_state` ni decidir qué Orders físicas existen; pérdida real de checkpoints ⇒ `COLD_RECOVERY_REQUIRED` fail-closed (§8.5, casos B/C).
- **R12:** claim de replay reducido: lo congelado es la propiedad de dominio (determinístico ante una secuencia ordenada de input); `operation_event_seq` queda para runtime ordering, stale-event protection y provenance; V1 NO persiste el stream completo de eventos ni promete replay exacto desde PG; el seam de recorded streams pasa al workstream D2 Market/Replay (§6.3-B, §8.7, caso F).
- **R13:** guard de identidad post-terminal: todo execution event porta `operation_id`+`order_id`; eventos de operaciones no corrientes jamás mutan la Operation corriente; un fill genuino nuevo para una Operation TERMINAL se conserva como hecho + `POST_TERMINAL_EXECUTION_BREACH` (sin revivir A, sin tocar B, sin auto-repair); estado mínimo: `current_operation_id` + identidad en eventos + identidad única de fill en PG — sin tombstones infinitos (§5.7, casos D/E).
- **R14:** durable projection/fact boundary: eliminada la ventana de pérdida del writer PG embebido (escribía fuera de la frontera transaccional del checkpoint — un Fill checkpointeado pero no flusheado a PG se perdía para siempre). Ahora `echo/operation` emite facts/projections (`OPERATION_SNAPSHOT`, `ORDER_SNAPSHOT`, `FILL_FACT`) por el **mismo egress Kafka transaccional EXACTLY_ONCE** (misma frontera de checkpoint) hacia `echo.operation-projections.v1`, y un **projector dedicado** materializa PG asincrónicamente. PG sigue siendo query projection, nunca recovery authority; el topic no reconstruye `mm_state` ni decide Orders; post-terminal (R13) usa el mismo fact path durable (§5.7, §8.3, §8.5-8.6, casos A–D).

## 1. Executive verdict

- `STATUS: D2-04_READY_FOR_MANAGER_REVIEW` (post-repair R1–R9). El diseño cierra identidades, lifecycles, ownership, exposición lógica, partial fills, múltiples Orders vivas, cancel/replace, idempotencia (incluida la ventana de crash), reconciliation boundary, aislamiento, event ordering y crash/recovery para las cuatro entidades, con mapping físico contra Echo V3 `372af59a`.
- Decisión central: **`Operation` es el aggregate lógico; el state owner físico es una función StateFun nueva `echo/operation` keyeada por `execution_account_id:account_strategy_id`**, que serializa determinísticamente todas las Signals, Orders, Fills y decisiones MM de esa cuenta+estrategia. Cuentas/estrategias distintas viven en keys distintas → aislamiento por construcción, sin store global de MM.
- **`Order` es entity del aggregate Operation (no aggregate independiente) y `Fill` es hecho inmutable** append-only. `Position` NO participa del lifecycle: es proyección read-only de observación física neta por `(account, contract)`, comparada contra exposición lógica sólo para telemetría (`DT-EF-POSITION-RECONCILIATION-05` sigue diferida; no hay auto-repair).
- **Dirección de la Operation nace del OPEN Signal aceptado** (autoridad técnica Strategy) y es immutable desde la materialización, antes de MM/Orders/Fills; las Orders se validan contra ella y jamás la definen (R2).
- **Fill truth jamás se clampa:** la exposición firmada conserva el hecho físico aunque un comportamiento anómalo del venue produzca una exposición incompatible con la dirección intencionada; el breach se marca y es fail-visible (R4).
- **Garantía de determinismo acotada (R5):** las cantidades derivadas de hechos (exposición, filled qty, precio ponderado) son conmutativas; las decisiones stateful de MM son determinísticas ante la misma secuencia ordenada de eventos — no ante órdenes de llegada arbitrarios — y el orden relevante se preserva con `operation_event_seq` sellado por el state owner.
- **No hay ventana de doble orden física (R6/R10):** dos boundaries separados, sin mezclar garantías: (1) StateFun state + Kafka egress EXACTLY_ONCE (transacción commiteada atómicamente con el checkpoint, garantía documentada del runtime 3.2 ya desplegado); (2) adapter con contrato restart-safe de idempotencia de efectos externos (journal durable write-ahead + resolución de ambiguos contra venue). La prueba end-to-end está en §5.6, caso 5 y caso A.
- Cero nuevas entidades genéricas: no `OperationLeg`, no `StrategyTrade`, no revisiones formales (D2-01), no event sourcing, no saga, no workflow engine, no microservicio nuevo. Superficie final (R9 + R14): 2 funciones de estado (`echo/signal_fanout`, `echo/operation`) + 1 projector PG dedicado (`echo/operation_projector`) + 1 shape-replace del proyector de posiciones; 2 familias de egress transaccional EXACTLY_ONCE (comandos per-account + proyecciones/facts); 4 ingress topics; 4 tablas PG.
- **Autoridad de recovery (R11):** el estado operativo vive en checkpoints Flink/StateFun + replay de Kafka; PG es proyección eventual/query-only (queries, UI, reporting, auditoría), jamás autoridad para recrear `mm_state` ni decidir Orders físicas; cold disaster ⇒ `COLD_RECOVERY_REQUIRED` fail-closed. **Post-terminal (R13):** los eventos de operaciones terminadas no tocan la Operation corriente; un fill nuevo tardío se conserva como hecho con alerta `POST_TERMINAL_EXECUTION_BREACH`.
- **Facts durables sin loss window (R14):** los Fills inmutables y las proyecciones latest-state de Operation/Order cruzan a storage por el egress transaccional (misma frontera de checkpoint que el estado), nunca por un writer fuera de esa frontera: un Fill checkpointeado es un Fill durable en Kafka, materializado eventualmente en PG aunque el Core caiga o PG esté caída horas.
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
- Entrega durable (R14): todo Fill cruza a storage como `FILL_FACT` por el egress transaccional (misma frontera de checkpoint que el estado del aggregate, §8.3); el identity natural `(account_id, provider_execution_id)` lo hace idempotente en el projector y en PG.

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
- Recovery tras restart: §8.5. El estado se recupera del checkpoint Flink/StateFun + replay de Kafka y se reconcilia contra el venue; PG no es autoridad de recovery (R11); la terminalidad no se infiere de la ausencia de mensajes.

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
- I13 (R6/R10): **dos boundaries de exactly-once, sin mezclar garantías:** (1) ningún comando físico publicado sin un estado Core commiteado que lo represente (2PC del egress, §5.6-M1); (2) ningún resubmit/redelivery con el mismo `client_order_id` produce una segunda orden física — garantizado por el contrato restart-safe del adapter (journal durable write-ahead + resolución de ambiguos contra venue, §5.6-M2), no por un map en RAM.
- I14 (R10): todo transporte que ejecute MARKET (o cualquier orden que pueda terminar inmediatamente) debe poder resolver "¿fue X físicamente enviado/ejecutado?" contra el venue (búsqueda por client tag sobre open + history reciente, o idempotencia nativa documentada); si no puede, esa clase de orden queda `UNSUPPORTED_FOR_V1_EXACT_SUBMISSION` y no se despliega.
- I15 (R13): todo execution event porta `operation_id` + `order_id`; el state owner valida identidad antes de mutar: eventos con `operation_id != current_operation_id` jamás mutan exposición/estado/MM de la Operation corriente. Un fill genuino nuevo de una Operation TERMINAL se conserva como hecho (identidad única en PG) con alerta `POST_TERMINAL_EXECUTION_BREACH`; nunca revive la Operation terminal ni contamina su sucesora sobre la misma key.
- I16 (R14): todo fact/proyección que cruza hacia storage (`FILL_FACT`, `OPERATION_SNAPSHOT`, `ORDER_SNAPSHOT`) viaja por el egress Kafka transaccional EXACTLY_ONCE — la misma frontera atómica con el checkpoint del estado. Prohibido depender de un writer PG fuera de esa frontera como fuente durable: un hecho confirmado por checkpoint es durable en Kafka y su materialización en PG es eventual e idempotente. El topic de proyecciones no es authority del aggregate: no reconstruye `mm_state`, no decide Orders, no reemplaza el checkpoint.

## 5. Idempotencia, cancel/replace, races y crash window

### 5.1 Idempotency keys

| Flujo | Key | Mecanismo |
|---|---|---|
| Signal procesada | `(account_strategy_id, signal_id)` | dedup set en el keyed state; replay de Kafka no re-materializa |
| Orden enviada | `client_order_id` (UUIDv7) | viaja como correlation tag al venue; contrato restart-safe del adapter: journal durable write-ahead + resolución de ambiguos contra venue (R10) |
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

- El dedup set de fills del keyed state **no tiene evicción por TTL**: persiste durante toda la vida de la Operation corriente; es keyed state y sobrevive/restaura con el checkpoint (autoridad de recovery, R11 — PG no lo reconstruye). El horizonte relevante queda cubierto por construcción: un fill ya aplicado no puede volver a mutar la exposición mientras la Operation corriente pueda mutar. Duplicados de Operations ya terminadas no alcanzan este set: los atrapa el guard de identidad (I15, §5.7) y la identidad única en PG.
- La memoria es acotada por diseño: V1 tiene 1 Operation no terminal por AccountStrategy (D2-02) y su cantidad de fills es naturalmente pequeña (contratos futures, horizonte intradía/multi-day); al llegar a TERMINAL el set se evicta completo — un duplicado posterior no puede mutar exposición (Operation terminal, guard I5) y la PG PK lo rechaza con métrica.
- No se requiere query síncrona a PG por Fill en el hot path: la primera barrera es el dedup set en el keyed state (consistente con la exposición porque ambos viven en el mismo estado atómicamente commiteado); la PG PK es segunda barrera de profundidad.

### 5.6 Crash window / duplicate physical order (R6/R10) — dos boundaries

El modelo completo tiene **dos boundaries con garantías distintas que no se mezclan**: `StateFun state + transactional Kafka egress → command topic → restart-safe idempotent adapter → venue`. La garantía EXACTLY_ONCE del runtime cubre sólo el primer boundary (consistencia state↔egress); el side effect externo en el venue se cubre exclusivamente con el contrato del adapter (M2). Combinación mínima:

- **M1 — Atomicidad state+egress del runtime (garantía documentada, carga de la prueba):** el runtime desplegado es `apache/flink-statefun:3.2.0` (`v3/core/deploy/flink-statefun/develop/docker-compose.yml`). El Javadoc oficial de `KafkaEgressBuilder` (3.2) documenta que con `DeliverySemantics.EXACTLY_ONCE` el egress "will write all messages in a Kafka transaction" que "will be committed to Kafka on a checkpoint", con la restricción de que el transaction timeout "must not be larger than the transaction.max.timeout.ms value configured on Kafka brokers (by default, this is 15 minutes)" (URL en §14). Bajo esta semántica, el estado de `echo/operation` y el comando de la Order se commitean atómicamente (2PC): el escenario "comando A llegó al venue pero el checkpoint con A se perdió" **no puede ocurrir** — o ambos commitean (orden registrada durablemente y publicada), o ninguno (transacción abortada, comando nunca visible, evento re-procesado, MM re-decide desde el estado rollbackeado). Por la misma razón `client_order_id` puede seguir siendo UUIDv7: bajo 2PC una identidad regenerada post-crash nunca convive con un artefacto físico de la intent previa (no existe tal artefacto). **Alcance exacto:** M1 garantiza consistencia StateFun-state ↔ Kafka egress (lo visible en el command topic ↔ lo commiteado); NO garantiza el side effect externo en el venue — eso es exclusivamente M2.
- **M2 — Contrato restart-safe de idempotencia de efectos externos del adapter (R10):** el consumo del topic de comandos es at-least-once (commit híbrido con auto-commit de respaldo — `command_consumer.go`), por lo que un redelivery post-ack-parcial puede reenviar un comando ya entregado — incluso una MARKET ya ejecutada que ya no figura como open order. El adapter garantiza por contrato que un mismo `client_order_id` produce a lo sumo un side effect físico, sobreviviendo a process restart, órdenes terminales, MARKET fills inmediatos y offset redelivery:
  - **Journal durable write-ahead:** antes de emitir el submit, el adapter persiste duraderamente (mecanismo físico adapter-owned, decisión de implementación D6) un registro `PENDING{client_order_id, digest del comando, ts}`; tras ack/outcome del venue persiste el outcome. El offset de Kafka se committea sólo después del outcome — no por tiempo.
  - **Resolución de ambiguos:** un registro que queda `PENDING` tras un crash es ambiguo (no se sabe si alcanzó al venue). En restart/redelivery, el adapter DEBE resolver "¿fue X físicamente enviado/ejecutado?" contra el venue antes de re-enviar: búsqueda por client tag sobre **open orders + history reciente** que cubra desde el `ts` del registro (ProjectX order search/history con `customTag`; NT `Orders`/`Executions` por tag), o re-submit seguro cuando el venue documenta idempotencia nativa de `client_order_id`. Encontrado (vivo o terminal) → outcome adoptado + `DUPLICATE_SUBMIT_SUPPRESSED`; no encontrado → el submit nunca alcanzó el venue → re-enviar es seguro.
  - **Gate de capacidad:** si un transporte no puede resolver esa pregunta (sin búsqueda por tag que incluya terminales, ni idempotencia nativa documentada), no puede prometer exactly-once physical submission: esa clase de órdenes queda `UNSUPPORTED_FOR_V1_EXACT_SUBMISSION` (como mínimo MARKET; una LIMIT resting es resoluble por open-order search) y no se despliega. Requisito explícito de selección/verificación de adapter en D6, no oculto.
- **Requisitos de despliegue (condiciones de validez de M1, marcadas como config, no inferencia de comportamiento):** (a) los specs de egress de comandos en `module.yaml` deben declarar `EXACTLY_ONCE` con transaction timeout ≤ broker `transaction.max.timeout.ms` — el `module.yaml` actual no declara delivery semantics, por lo que esto es un requisito explícito de la SPEC (la default documentada es AT_LEAST_ONCE); (b) los consumers del topic de comandos deben leer con `isolation.level=read_committed` (comportamiento documentado de Kafka para consumidores sobre productores transaccionales); (c) el endpoint remoto del Core (las functions son HTTP remoto) participa del protocolo de checkpoint estándar de Flink, que es el mismo mecanismo que hoy protege `execution_store`/`pending_mm`.

### 5.7 Late events y reuso de la key después de TERMINAL (R13)

- La key del state owner (`account:strategy`) es estable: tras terminar la Operation A puede nacer la Operation B sobre la misma key. Para impedir contaminación, **todo execution event porta obligatoriamente `operation_id` + `order_id`** (correlación del adapter desde su submission registry, §8.2) y el state owner **valida identidad antes de mutar**: `event.operation_id != current_operation_id` ⇒ el evento nunca toca la exposición, el estado ni el `mm_state` de la Operation corriente (I15).
- **Duplicado antiguo** (fill ya aplicado a A, reaparece con A terminada): guard de identidad → late-event path → emite `FILL_FACT{post_terminal=true}` durable (§5.6-M1) → el projector intenta materializarlo y la identidad única `(account_id, provider_execution_id)` lo detecta como duplicado (PK conflict) → métrica de duplicado, sin fila nueva, sin breach definitivo, sin tocar B.
- **Fill genuino nuevo de una Operation TERMINAL** (execution id no visto antes, para Order de A): es un hecho físico real. Manejo V1: el guard lo saca del aggregate corriente y el late-event path emite por el **mismo fact path durable** (egress transaccional, R14) un `FILL_FACT{operation_id=A, post_terminal=true}` + telemetría inmediata de candidato a breach; el projector, al materializar por primera vez un fact con `post_terminal=true` (PK nueva — sin duplicado), levanta el alerta definitivo `POST_TERMINAL_EXECUTION_BREACH` (métrica/log/surface). El hecho y su bandera quedan **durables en Kafka** aunque PG esté caída; A permanece TERMINAL (el hecho no recomputa decisiones de un aggregate terminal); B no se contamina; la política de reacción (p. ej. bloquear nueva exposición de la cuenta) es del safety plane — sin auto-repair, `DT-EF-POSITION-RECONCILIATION-05` sigue diferida. La observabilidad del breach no depende exclusivamente de un write PG: el fact está durably en el topic y la telemetría Core es inmediata.
- **Estado mínimo que sobrevive — justificación KISS:** el guard sólo necesita `current_operation_id` (ya existe en el keyed state) + la identidad que porta el evento; la pregunta "¿este execution id ya se aplicó a una operación anterior?" se resuelve fuera del aggregate con la identidad única del fact materializado por el projector (best-effort, no correctness — la correctness del aggregate vive en el guard) y la verdad física en la reconciliación del venue. No se requiere archivo de tombstones en StateFun: la membresía histórica vive en `echo.fills` y en los `FILL_FACT` durables del topic, y ningún hot path la consulta.

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
- **Orden de runtime — `operation_event_seq` (adoptado, claim acotado R12):** el state owner asigna un entero monótono por Operation a cada input event de dominio de ejecución que procesa (signals, acks/status de orders, fills, intents de terminación) y lo sella en las escrituras durables (fills, estado de orders, estado de la Operation). No se crea una tabla de eventos nueva (R9): la secuencia viaja en los propios registros. **Alcance congelado:** la secuencia sirve a (a) orden de runtime y stale-event protection, (b) debugging/provenance. La propiedad de dominio "determinístico ante una secuencia ordenada de input" pertenece al motor puro, no a la infraestructura: V1 **no persiste el stream completo** de inputs (signals, acks, transiciones, intents, inputs de mercado) y **no se promete reconstruir los eventos 1..seq desde PG** ni replay exacto de una sesión live. El diseño de recorded streams / market-event ordering / replay histórico cierra en el workstream D2 de Market/Replay — seam explícito, sin event store nuevo (YAGNI). No se afirma que un arrival ordering arbitrario reproduzca el mismo outcome live.

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
- V1 NO hace auto-repair, synthetic fills, remapping ni subsystem de reconciliación (DT-EF-POSITION-RECONCILIATION-05 diferido, reafirmado). El mismatch es señal para el operador/safety plane; la única reacción automática permitida es la telemetría y (si el owner lo habilita por config) el bloqueo de nuevas aperturas de esa cuenta por el safety plane existente, nunca la mutación del estado lógico. Un `POST_TERMINAL_EXECUTION_BREACH` (R13) se manifiesta también aquí: el hecho tardío de una Operation terminada deja la proyección física desalineada del agregado lógico y dispara la misma señal fail-visible.
- Caso 7 (mandato): dos Strategies de la misma Account con exposición opuesta sobre el mismo Contract → dos Operations lógicas independientes (+N y −M), una Position física neta (N−M). Ambas verdades coexisten; el comparador usa la suma.

## 8. Runtime: ownership, aislamiento y recovery

### 8.1 State owner y partition key

- Owner del estado: función StateFun nueva `echo/operation`, una instancia por `key = execution_account_id + ":" + account_strategy_id`. Es el único mutador del estado de Operation/Order y de la exposición, el contexto de invocación de MM, y el asignador de `operation_event_seq`. Serializa todos sus mensajes (garantía StateFun por key) → determinismo de decisión por cuenta+estrategia (§6.3-B).
- MM vive como plugin de dominio invocado dentro de `echo/operation`: recibe el contexto de esa Operation + snapshots de cuenta/instrumento (patrón join de `MMEngineFn` reutilizado) y devuelve decisiones (0..N Order requests, modify/cancel, intents de terminación, mutación de su `mm_state`). MM nunca accede a estado de otras keys ni a un store global (I9). El aislamiento es por construcción del runtime, no por disciplina.
- `echo/signal_fanout` (función nueva, sucesora del patrón `ExecutionPlannerFn`): lee bindings habilitados por strategy desde kache, filtra por whitelist/estado de cuenta (patrón RFC-007) y entrega la Signal a cada `echo/operation` por su key, preservando el orden intra-evaluación (`signal_seq`).

### 8.2 Correlación evento→operación (adapter-owned, R9)

- El adapter de ejecución posee el **submission journal/registry** (§5.6-M2): conoce, por `client_order_id`, la `(account, account_strategy_id, operation_id, order_id)` de cada comando que emitió. Publica los execution events (acks, status, fills) en `echo.execution-events.v1` **ya correlacionados** — con `operation_id` + `order_id` obligatorios (R13) — y con Kafka key = op key → el ingress los entrega directo a `echo/operation` (no existe función router en Core). Eventos sin correlación resoluble → cuarentena de eventos (I2); eventos cuya `operation_id` no coincide con la Operation corriente → late-event path (§5.7), nunca el aggregate corriente. Los eventos del venue sin origen Echo (trading manual, posiciones) van a los topics de observación/proyección (§7), no al state owner.
- Esto elimina la función `echo/execution_router` y su registry en Core: la correlación es un dato de transporte que el adapter stamped al enviar y devuelve al recibir (mismo primitivo D1: customTag/clOrdId); la resolución de eventos sin tags (reconnect/replay) queda cubierta por el registry que el adapter ya debe sostener para M2, reconciliando open orders por tag.

### 8.3 Topología final (R9)

| Componente | Tipo | Key | Contenido |
|---|---|---|---|
| `echo/signal_fanout` | función StateFun (nueva) | strategy_id | fan-out de Signal a AccountStrategies habilitadas |
| `echo/operation` | función StateFun (nueva) | `account:strategy` | aggregate Operation: lifecycle, Orders, Fills, exposición, MM, seq; emite comandos y facts/projections por egress transaccional — **sin writer PG embebido (R14)** |
| `echo/operation_projector` | projector dedicado (nuevo, R14) | op key (ingress) | consume `echo.operation-projections.v1` y materializa PG asincrónicamente (upserts idempotentes/stale-safe; patrón async-writer `PositionSyncFn`) |
| position projection | shape-replace del slot `PositionSyncFn` (R8) | account_id | proyección neta `(account, contract)` |
| `echo.signals.v1` | ingress (nuevo) | strategy_id | Signal canónica D2-03 emitida por StrategyEngine |
| `echo.execution-events.v1` | ingress (nuevo) | op key | eventos normalizados del venue, correlacionados por el adapter |
| `echo.operation-projections.v1` | ingress del projector / egress de `echo/operation` (nuevo, R14) | op key | `OPERATION_SNAPSHOT` / `ORDER_SNAPSHOT` / `FILL_FACT`; **EXACTLY_ONCE, misma frontera de checkpoint que el estado** |
| `echo.order-commands.{account_id}.v1` | egress (familia nueva) | client_order_id | OrderRequest / Modify / Cancel; **EXACTLY_ONCE + read_committed (§5.6)** |
| `echo.position-observations.v1` | ingress (nuevo, proyección) | account_id | observaciones netas de posición del venue |
| configs (existente) | kache/KVS | — | bindings AccountStrategy, specs Instrument/Contract + hot mapping |

- Semántica del topic de proyecciones (R14, KISS): tres record types — `OPERATION_SNAPSHOT` (latest-state de la Operation, incluye `termination`/`terminal_reason`/`exposure_invariant_breach` y `operation_event_seq`; no incluye `mm_state`), `ORDER_SNAPSHOT` (latest-state de la Order, `order_version` + seq) y `FILL_FACT` (inmutable, identity `(account_id, provider_execution_id)`, flag `post_terminal`). Idempotencia en el projector: `FILL_FACT` insert-only por identity natural; snapshots stale-safe por `operation_event_seq` (sólo aplican si la secuencia avanza). No es un log de eventos del aggregate: no se persiste cada transición, sólo latest-state + hechos inmutables; sin tablas `operation_events`/`order_events` (R9 se mantiene). Requisito de config: retention del topic ≥ ventana máxima tolerable de caída del projector/PG (se dimensiona en implementación; p. ej. días, no horas).

- Las funciones nuevas se registran en `module.yaml` con ingress/egress propios (patrón exacto del existente); la topología legacy queda intacta durante la migración.

### 8.4 Event ordering

- Orden por cuenta+estrategia: Kafka preserva orden por key con producer idempotente (config explícita in-flight limitado); StateFun procesa serialmente por instancia → las Signals y eventos de una Operation se aplican en orden y las decisiones son reproducibles ante la misma secuencia (I8).
- Orden intra-evaluación: StrategyEngine sella `signal_seq` monótono por strategy; el fan-out preserva el orden por key; `echo/operation` rechaza regresiones (dedup + telemetría). CLOSE_ALL→OPEN en la misma evaluación se aplica en orden (A1: procesamiento determinístico).
- Orden venue: `executed_at` + `provider_execution_id` para el orden semántico de fills; `operation_event_seq` fija el orden efectivamente observado para replay (§6.3-B).

### 8.5 Crash / recovery

- **Autoridad de recovery normal (R11):** Flink/StateFun checkpoint del keyed state (incluye dedup sets R7, `mm_state`, `operation_event_seq`) + replay del Kafka ingress (los offsets commitean con el checkpoint) + egress transaccional (§5.6-M1). Al restaurar, los eventos posteriores al checkpoint se re-procesan desde Kafka por las mismas guards idempotentes; **nada se lee desde PG para reconstruir estado o decidir**.
- **PG = proyección eventual/query-only (R11/R14):** `echo.operations` / `echo.orders` / `echo.fills` / `contract_positions` se materializan por el projector dedicado consumiendo `echo.operation-projections.v1` (upserts idempotentes y **stale-safe**: sólo aplican si `operation_event_seq` avanza; `FILL_FACT` insert-only por identity natural). La fuente durable de los facts/projections es el topic (egress transaccional, misma frontera de checkpoint que el estado — R14): si PG cae 30 minutos, el trading continúa y el projector replayea idempotentemente al volver (caso C de R14). PG adelantada al checkpoint (caso B de R11: PG seq 50, checkpoint 45) sigue siendo inofensiva — el runtime restaura 45 y el replay re-aplica 46..50 con contenido idéntico. PG failure/lag jamás cambia decisiones live ni bloquea Operation/MM (métrica de lag del projector; sin backpressure hacia el aggregate). PG sirve a queries, UI, reporting, observabilidad y auditoría — no a la recreación de `mm_state` ni a decidir qué Orders físicas existen.
- **Cold disaster (checkpoints realmente perdidos):** `COLD_RECOVERY_REQUIRED` — comportamiento fail-closed mínimo congelado: reconciliar estado físico contra el venue, **bloquear nueva exposición/risk** y ejecutar un procedimiento controlado de bootstrap/recovery operado por el operador. La forma completa (qué se precarga, cómo se re-ancla `mm_state`) queda para implementación/DR; prohibida la recuperación exacta silenciosa desde PG — `mm_state` no es reconstruible sin checkpoint.
- **Reconciliación de venue (arranque/reconnect — no recovery de estado):** resubscribe + query de estado autoritativo (ProjectX `Order/searchOpen` + positions; NT `Orders/Executions/Positions`) + fetch de historial de executions desde el último hecho visto (capacidad documentada en D1 Front D por transporte); el adapter re-correlaciona por tag y los hechos entran con `source = RECONCILIATION|HISTORY` por las mismas guards.
- Convergencia: las cantidades derivadas de hechos convergen siempre (§6.3-A); la terminalidad exige guards reales; duplicados absorbidos por I7 e I15.

### 8.6 Hot path y persistencia

- En el hot path (signal → materialización → sizing → submit) no hay I/O remoto síncrono: snapshots de cuenta/instrumento se sirven de las KVS functions / kache (patrón actual); la proyección PG es escritura async batched embebida (patrón `PositionSyncFn`/`AccountSyncFn`); ningún query a PG por Fill o por comando (R7).
- **Persistencia autoritativa y durable (R11/R14):** el estado operativo (identidad/estado de Operation y Orders, exposición, dedup sets R7, `mm_state`, `operation_event_seq`) vive en el keyed state checkpointeado por Flink/StateFun. Los facts durables (Fills inmutables, incluidos los post-terminal) y las proyecciones latest-state de Operation/Order cruzan a storage **sólo** por el egress transaccional `echo.operation-projections.v1` (misma frontera atómica con el checkpoint — un hecho confirmado por checkpoint es durable en Kafka); PG es la materialización eventual de ese topic para queries/reporting/auditoría. Cold disaster ⇒ `COLD_RECOVERY_REQUIRED` (§8.5); los `FILL_FACT`/snapshots durables en Kafka preservan la historia económica exacta para forense/materialización posterior, sin reconstruir `mm_state` (que no viaja en el topic, R11).
- Volumen: el estado vivo por key es acotado (1 Operation no terminal + sus Orders vivas + sets acotados); la historia completa vive en PG, no en el estado caliente.

### 8.7 Backtest / replay reuse

- Las entidades, la máquina de transiciones y el contrato de decisiones MM viven como paquetes Go puros (SDK domain layer), sin imports de Kafka/StateFun; las funciones StateFun son adaptadores finos que invocan el mismo motor. `SimExecution` implementa el mismo contrato `ExecutionEvent` que los adapters reales (fills determinísticos por seed).
- Contrato de replay (R5, acotado por R12): la propiedad congelada es de dominio — dado un stream ordenado de input (eventos de ejecución + mercado), el mismo motor produce las mismas decisiones. V1 no persiste ese stream completo ni promete replay exacto de sesiones live; el grabado/ordenamiento de streams para replay es diseño del workstream D2 Market/Replay (seam explícito). El backtester futuro ejecuta `Signal → Operation → MM → Order → Fill → exposición` con el mismo código de dominio y Clock/event-time inyectables, cumpliendo la constraint de reutilización del D1 sin `*_live` vs `*_backtest`.

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
| Bridge (sesiones, command consumer, pipes, producer) | **REUSE (patrones) / ADAPTER NUEVO** | `v3/bridge/internal/session/command_consumer.go` (topic dedicado por cuenta, commit híbrido at-least-once, circuit breaker) y `pipe_handler.go` (keys de publicación: ExecutionResult/CloseResult = TradeID, PositionSnapshots = AccountID). Los patterns son el estándar para los adapters futures; el adapter nuevo añade el contrato restart-safe de idempotencia (§5.6-M2: journal durable write-ahead + resolución de ambiguos contra venue) y consumo `read_committed` del topic de comandos. El adapter MetaTrader actual no se deforma. |
| trade_journal / canonical_operations / TradeJournalFn | **REUSE intacto (boundary analítico)** | `v3/core/internal/functions/trade_journal.go`, migraciones 062/064. No es state owner del runtime nuevo; la proyección Operation→Trade queda diferida a The Lab (owner 2026-09-26). |
| Hot symbol mapping (Gateway→Kafka→cache) | **REUSE/EXTEND** | `v3/gateway/internal/symbol_mapping_handler.go` (blob a9364d4a…): patrón hot-update compactado; se extiende a mapping `Instrument → Contract`; el pin de Operation vive en el dominio, no en el mapping. |
| PostgreSQL como store duradero + migraciones numeradas | **REUSE** | `v3/sdk/postgres/migrations/` (…064 canonical_operations, 065 lab_curves). Nuevas migraciones para `operations/orders/fills` + proyección neta de posiciones; numeración a coordinar en implementación (la rama E-04 fuera de master reservó 068). |

## 10. Implicaciones de refactor / migración

- SDK domain nuevo (paquete puro): structs `Operation/Order/Fill`, proyección `Position` neta, enums de estado, máquina de transiciones con guards (incluida terminación por intent, R3), `operation_event_seq`, y contratos `MMPlugin` (decisiones) + `ExecutionEvent` (eventos venue) + `SimExecution`. Sin dependencias de infra — es el boundary Q14.
- Core: **3 componentes nuevos** — `echo/signal_fanout` y `echo/operation` (funciones de estado; `echo/operation` sin writer PG embebido: emite facts/projections por egress transaccional, R14) y `echo/operation_projector` (projector PG dedicado, patrón async-writer `PositionSyncFn`) + 1 shape-replace del slot de position projection. Registro en `module.yaml` (ingress signals / execution-events / position-observations / operation-projections; egress per-account de comandos + egress de proyecciones, ambos con `EXACTLY_ONCE` y transaction timeout ≤ broker `transaction.max.timeout.ms`, §5.6). Retention de `echo.operation-projections.v1` dimensionada a la ventana máxima tolerable de caída de projector/PG. Sin router (R9); el store function fue reemplazado por el projector sobre el topic durable (R14).
- PG: migraciones nuevas `echo.operations` (upsert por operation_id, incluye `termination`, `exposure_invariant_breach`, `operation_event_seq`), `echo.orders` (upsert por order_id, `order_version`, sin tabla de eventos), `echo.fills` (insert-only, PK `(account_id, provider_execution_id)`, `operation_event_seq`), `echo.contract_positions` (proyección neta, upsert `(account_id, contract_id)`). Todas las escrituras de proyección son idempotentes y stale-safe por `operation_event_seq` (sólo aplican si la secuencia avanza; R11). Índices por `(account_strategy_id, status)` y `(contract_id)`. Numeración a coordinar con ramas en vuelo al implementar. Sin `order_events`/`operation_events` (historia en Kafka/OTel, R9).
- Adapters futures (D6): implementan `ExecutionEvent` correlacionado (`operation_id` + `order_id` obligatorios) + per-account command consumer (`read_committed`) + contrato restart-safe de idempotencia (journal durable write-ahead, resolución de ambiguos contra venue por tag sobre open + history, o `UNSUPPORTED_FOR_V1_EXACT_SUBMISSION`) + reconciliación de reconexión por tag (§5.6, §5.7, §8.2); cada rareza de venue queda aislada en su adapter.
- Legacy: la path Reference→ExecutionPlanner→MMEngine→CoreCommand→Bridge sigue operando intacta; el adapter `ReferenceEvent → Signal` (DT-EF-REFERENCE-SIGNAL-03) es el puente futuro. ExecutionStoreFn queda como proyección de compatibilidad.
- Refactors bloqueantes detectados: ninguno nuevo que exceda el registro D1 §6 (Signal boundary limpio + identities/lifecycle eran ya blocking design items; este workstream los especifica). No hay reescritura de Core (Q1 owner-accepted).

## 11. Riesgos y deudas

- **R1 — Ordering Kafka:** la garantía de orden por key depende de config explícita del producer (idempotence + in-flight limitado) y de keys consistentes end-to-end; el adapter debe setear la Kafka key de `echo.execution-events.v1` = op key (contrato del adapter, testeable).
- **R2 — Config EXACTLY_ONCE del egress:** la garantía 2PC de §5.6-M1 es válida sólo si **ambos** specs de egress (comandos per-account y proyecciones/facts R14) declaran `EXACTLY_ONCE` (el `module.yaml` actual no declara delivery semantics) y el broker tolera el transaction timeout configurado; la verificación física del despliegue (y del consumo `read_committed` por el adapter) es requisito de D6 y quedará cubierta por el gate de certificación correspondiente. Marcado como config requirement, no como comportamiento ya demostrado en runtime.
- **R3 — Capacidades de venue/transporte:** la recuperación post-gap de fills y la resolución de submissions ambiguos (R10) dependen de que cada transporte exponga history/search por client tag (o idempotencia nativa documentada); donde no, la clase de orden queda `UNSUPPORTED_FOR_V1_EXACT_SUBMISSION` y el gap post-desastre queda visible como mismatch persistente (fail-visible). Requisito de selección de adapter en D6, no defecto del dominio.
- **R4 — Capacity 100–200 cuentas:** el diseño multiplica estado por (cuenta×estrategia) y fan-out por signal; el trabajo por instrumento (feed/estrategia) no se multiplica por cuenta (requerimiento del proyecto). El benchmark de capacidad sigue siendo trabajo D6 (misma disposición D1).
- **R5 — ForceClose vs MM concurrently:** un flatten del safety plane mientras MM gestiona puede duplicar intents de cierre; mitigación: hechos idempotentes, dedup por client tag, y terminalidad sólo por guards (R3) — el doble intento converge, no corrupte.
- **R6 — Breach handling residual:** qué safety policy reacciona a `EXPOSURE_INVARIANT_BREACH` (más allá de la telemetría fail-visible) es decisión del safety plane; el modelo V1 define la representación y la reacción vía intents, no la política automática.
- **R7 — Deuda existente heredada:** `DT-EF-POSITION-RECONCILIATION-05` sigue diferida; `DT-EF-REFERENCE-SIGNAL-03` sigue siendo el carril legacy→nuevo; unidades pips legacy (deuda con ID pendiente de ratificación owner) no entra al camino nuevo.
- **R8 — Reloj y `valid_until`:** la validez de Signal y TTLs de entry usan event-time de Core (no del venue); clock skew se resuelve en el diseño técnico de implementación (no cambia el modelo).
- **R9 — Cold recovery procedure:** el procedimiento completo `COLD_RECOVERY_REQUIRED` (re-anclaje de `mm_state`, bootstrap controlado, DR) queda para implementación/DR; V1 congela sólo el comportamiento fail-closed (reconciliar venue + bloquear nuevo riesgo), no la reconstrucción exacta. Los `FILL_FACT`/snapshots durables en Kafka (R14) preservan la historia económica para forense, pero no re-anclan `mm_state`.
- **R10 — Retention y lag del topic de proyecciones (R14):** la durabilidad del fact chain depende de que la retention de `echo.operation-projections.v1` cubra la ventana máxima tolerable de caída simultánea de projector y PG (config explícita de implementación, p. ej. días); el lag del projector es métrica operacional obligatoria (alerta si crece), sin backpressure nunca hacia el aggregate.

## 12. Decisiones owner

- `OWNER DECISIONS REQUIRED: NONE`. El diseño (y el repair R1–R9) vive dentro de las decisiones congeladas D2-01/02/03 y del lifecycle A2, sin reabrirlos y sin `BLOCKED_OWNER_DECISION`.
- Ratificaciones técnicas ordinarias para el manager (no owner, no cambian semántica): (1) enum `TerminalReason` propuesto en §3.3; (2) nombres físicos de functions/topics/tablas nuevas (§8.3/§10); (3) la config de despliegue `EXACTLY_ONCE` del egress de comandos (§5.6), que es requisito técnico de la SPEC.

## 13. Casos de validación (mandato repair §12)

- **Caso 1 — partial fills:** OPEN aceptado → Operation CREATED con `direction` sellada por la Signal (LONG) y contract pinneado → MM BUY 2 → entry Order WORKING → fill +1 + fill +1 (dedup por execution id) → exposición +2, `ACTIVE`. Una Order, dos Fills.
- **Caso 2 — reduce:** Signal REDUCE → MM SELL 1 (guard de construcción: side opuesto, qty ≤ exposición) → fill → exposición +1, misma Operation, `ACTIVE`.
- **Caso 3 — over-reduction anomaly:** LONG exposición +1; llega un fill SELL 2 no ordenado → el hecho se conserva íntegro (I6), exposición firmada = −1 (verdad física), `exposure_invariant_breach = true` + telemetría `EXECUTION/EXPOSURE INVARIANT BREACH`; sin clamp, sin synthetic fill, sin Operation nueva. La dirección lógica sigue LONG e immutable; TERMINAL exige exposición firmada real = 0; MM/safety plane reaccionan vía eventos/intents; el mismatch se refleja también en `POSITION_MISMATCH` si el venue lo confirma.
- **Caso 4 — cancel/fill race:** partial fill + cancel + fill tardío → fill tardío appendeado idempotentemente; estado de Order converge por la regla venue-authoritative + corrección forward (`FILLED` si Σ fills ≥ qty; si no, `CANCELLED` con filled_qty retenido); exposición final = Σ fills (conmutativa) en ambos órdenes de llegada; MM reacciona al estado convergido en su secuencia observada (§6.3-B).
- **Caso 5 — crash after physical submit:** comando A entregado al venue, checkpoint no completado → bajo EXACTLY_ONCE la transacción del egress abortó ⇒ el comando **nunca fue visible** para el adapter (M1); el evento se re-procesa con estado rollbackeado y MM re-decide. Complemento at-least-once: si A ya fue consumido/entregado por el adapter y su offset no se committeó, el redelivery con el mismo `client_order_id` encuentra en el journal durable un registro con outcome (suprimido) o `PENDING` ambiguo que se resuelve contra el venue — open + history por tag (M2/R10) — **no existe path end-to-end hacia una segunda orden física** (I13/I14). Caso simétrico (state commiteado, egress perdido) tampoco puede ocurrir: commitean atómicamente.
- **Caso 6 — duplicate historical Fill:** un execution ya aplicado reaparece tras cualquier horizonte → mientras la Operation es no terminal, el dedup set cubre toda su vida (R7) y el fill no muta exposición; si la Operation ya es TERMINAL, el guard I5 impide mutación y la PG PK `(account_id, provider_execution_id)` rechaza con métrica. La exposición nunca incrementa dos veces.
- **Caso 7 — two Strategies, same Account+Contract:** keys `(acct,S1)` y `(acct,S2)` independientes → dos Operations lógicas (+N/−M) con fills atribuidos estructuralmente; Position física neta (N−M) en la proyección nueva; comparador usa la suma; ningún path de estado entre keys (I9).
- **Caso 8 — safety flatten:** ForceClose llega con exposición y Orders vivas → registra `termination{SAFETY_PLANE, SAFETY_FLATTEN}`; cancela Orders working, emite Orders de cierre, espera partial fills/reconciliación; la Operation NO es TERMINAL hasta `exposure==0 ∧ 0 live orders` (I5/R3); entonces `TERMINAL(SAFETY_FLATTEN)`.

### Casos de validación — second repair (R10–R13)

- **Caso A — fast MARKET + adapter crash:** consume A → journal `PENDING` durable → submit MARKET A → fill inmediato (A nunca aparece como open order) → adapter cae sin committear offset ni outcome → restart + redelivery de A → el journal muestra `PENDING` ambiguo ⇒ resolución obligatoria contra el venue (search por tag sobre open + history desde el `ts` del registro, §5.6-M2): A aparece como orden terminal FILLED ⇒ outcome adoptado, `DUPLICATE_SUBMIT_SUPPRESSED`, offset committeado, **sin segunda orden física**. Si el transporte no soportara esa resolución, MARKET habría estado gated `UNSUPPORTED_FOR_V1_EXACT_SUBMISSION` y nunca desplegado (I14). La ventana `PENDING` es acotada: se resuelve en restart y el offset sólo commitea tras outcome.
- **Caso B — PG ahead of checkpoint:** el writer async aplicó seq 50; el checkpoint vigente es 45; crash → restore 45 + replay Kafka de 46..50; PG no se consulta para decisiones; las re-aplicaciones sobrescriben las filas con contenido idéntico (upserts stale-safe por seq) ⇒ estado legítimo = 45 + replay; PG converge. Prohibido "restaurar hasta 50" desde PG.
- **Caso C — PG behind checkpoint:** checkpoint 50, PG 45 → el runtime corre desde 50; el writer sigue aplicando eventos con seq creciente y PG converge eventualmente; el lag de PG no bloquea Operation/MM ni cambia decisiones.
- **Caso D — old duplicate after new Operation:** A TERMINAL, B ACTIVE; reaparece un duplicado de un fill viejo de A → el event porta `operation_id=A` ≠ corriente ⇒ guard I15: B no cambia (ni exposición ni `mm_state`); late-event path intenta insert en PG → PK `(account_id, provider_execution_id)` conflict → métrica de duplicado, sin fila nueva, sin breach falso.
- **Caso E — genuinely new late Fill after terminal:** A TERMINAL; llega un execution id nuevo para Order A → guard I15 lo saca del aggregate; late-event path inserta el hecho vinculado a A (insert nuevo) ⇒ `POST_TERMINAL_EXECUTION_BREACH` + alerta safety/reconciliación + `POSITION_MISMATCH` visible; A no revive, B no se contamina, sin auto-repair (DT-05 diferido).
- **Caso F — replay claim (R12):** lo congelado en V1 es la propiedad de dominio: dado el MISMO stream ordenado de input, MM/transiciones producen las mismas decisiones (motor puro, serializado). NO se promete: persistencia del stream completo (signals, acks, transiciones, intents, inputs de mercado), reconstrucción de los eventos 1..seq desde PG, ni replay exacto de una sesión live. `operation_event_seq` queda para runtime ordering, stale-event protection y provenance; recorded streams y su ordering se diseñan en el workstream D2 Market/Replay.

### Casos de validación — durability repair (R14)

- **Caso A — Fill antes de crash:** Fill F procesado → estado actualizado → `FILL_FACT` emitido por el egress transaccional → checkpoint completa (la transacción del fact commitea atómicamente con el checkpoint) → PG aún no escribió F → crash → restore desde checkpoint (F no se replayea del ingress) pero **F queda durable en Kafka** (transacción commiteada) → el projector lo materializa en PG después. Sin pérdida: la única ventana vieja (checkpoint committeado, writer PG sin flush) desaparece porque el writer PG embebido ya no existe — la entrega durable es parte de la misma transacción del checkpoint (I16).
- **Caso B — checkpoint abortado:** estado procesa F → `FILL_FACT` en la transacción del egress → el checkpoint FALLA → rollback del estado + abort de la transacción (el fact nunca fue visible en el topic) + replay del ingress → F se procesa nuevamente → nuevo `FILL_FACT` con la misma identity `(account_id, provider_execution_id)` → idempotente en projector/PG. Sin duplicado durable.
- **Caso C — PG caída 30 minutos:** el trading continúa (PG nunca está en el hot path ni en la frontera transaccional); los records de proyección/facts se acumulan durably en `echo.operation-projections.v1` (retention dimensionada, §11-R10); al volver PG, el projector reanuda desde su offset y aplica replay idempotente (PK natural para facts, seq-guard para snapshots) → las tablas convergen sin duplicados ni retrocesos.
- **Caso D — late Fill de A después de B:** A TERMINAL, B ACTIVE, llega execution nuevo para Order de A → guard I15 lo saca del aggregate corriente (B no cambia) → late-event path emite `FILL_FACT{operation_id=A, post_terminal=true}` durable + telemetría de candidato → el projector lo materializa (PK nueva ⇒ genuino) y levanta `POST_TERMINAL_EXECUTION_BREACH`; si era duplicado, la PK lo detecta → métrica sin breach falso. El fact y su bandera quedan durables en Kafka independientemente de PG; A no revive; sin auto-repair.

## 14. Evidencia

- Vault: `main/10-projects/Echo Futures/Echo Futures.md` (D2-01/02/03 OWNER_CLOSED; lifecycle A2; manager reviews 1 y 2 del repair), `main/10-projects/Echo Futures/Echo Futures — D1 Analysis Pack.md` (matriz Q1/reuse, Front D, `DT-EF-*`), Environment Contract Echo/Forge.
- Repo físico (verificado vía `git show 372af59a:<path>` sobre clon `~/aranea/work/d4-shot1-20260925/echo`; `git fetch` re-verificado en el repair con `origin/master = 372af59a…`): `v3/sdk/domain/reference_event.go`, `v3/sdk/domain/trade_close.go`, `v3/sdk/domain/position_snapshot.go` (DTO MT por ticket — base de R8), `v3/sdk/domain/snapshots.go`, `v3/sdk/domain/execution_policy.go`, `v3/core/internal/functions/{execution_planner,strategy_config,mm_engine,execution_store,position_sync,close_handler,acc_snapshot,inst_snapshot}.go` (`position_sync.go`: upsert `ON CONFLICT (account_id, ticket)` — base de R8), `v3/sdk/statefun/constants.go`, `v3/sdk/mm/calculator.go`, `v3/core/deploy/flink-statefun/develop/module.yaml` + `docker-compose.yml` (runtime `apache/flink-statefun:3.2.0-java11`; module.yaml sin delivery semantics declarada), `v3/bridge/internal/session/command_consumer.go` (commit híbrido at-least-once — base de M2), `v3/bridge/internal/pipe_handler.go`, `v3/sdk/kache/README.md`, `v3/sdk/postgres/migrations/`, `v3/sdk/utils/uuid.go`.
- Garantía StateFun 3.2 (R6-M1), documentación oficial, citas textuales: Apache Flink Stateful Functions, Javadoc `KafkaEgressBuilder` (3.2), https://nightlies.apache.org/flink/flink-statefun-docs-release-3.2/api/java/org/apache/flink/statefun/sdk/kafka/KafkaEgressBuilder.html — con `EXACTLY_ONCE` el egress "will write all messages in a Kafka transaction" que "will be committed to Kafka on a checkpoint"; el transaction timeout "must not be larger than the transaction.max.timeout.ms value configured on Kafka brokers (by default, this is 15 minutes)". Con `AT_LEAST_ONCE` el egress sólo espera ack del producer en checkpoint. La atomicidad estado↔checkpoint (rollback del estado no commiteado al restaurar) es semántica estándar documentada de Flink checkpointing (https://nightlies.apache.org/flink/flink-docs-stable/docs/internals/job_checkpointing/). Marcado explícitamente como **inferencia/config, no comportamiento demostrado**: el spec de egress actual del repo no declara `EXACTLY_ONCE` — su configuración es requisito de la SPEC (§5.6, riesgo R2) y su verificación física queda en D6. La misma garantía documentada aplica al egress de proyecciones/facts (R14).
- D1 Front D (pack aceptado, [[Echo Futures — D1 Analysis Pack]]) documenta los primitives de búsqueda/correlación por transporte — ProjectX `Order/search`/`searchOpen` + `customTag` (customTag como correlation primitive, sin garantía de idempotencia) e history con rate limits (50/30s); NT `Orders`/`Executions` — insumo para la resolución de ambiguos R10; la capacidad concreta (incluye history por tag y su ventana) se verifica por transporte en D6.

## Fuentes

- [[Echo Futures]] — proyecto canónico y decisiones owner D2-01/02/03.
- [[Echo Futures — D1 Analysis Pack]] — evidence baseline D1 aceptada.
- `xKoRx/echo@372af59a` — source físico V3 inspeccionado (paths en §14).
