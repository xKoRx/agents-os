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
> Diseño técnico V1 del modelo `Operation / Order / Fill / Position` y su runtime dentro de Echo V3. Respeta sin reabrir las decisiones owner [[Echo Futures]] D2-01 (snapshot + contract pinning), D2-02 (fan-out + single Operation) y D2-03 (Signal + Strategy/MM boundary), y el lifecycle A2 aceptado en [[Echo Futures — D1 Analysis Pack]]. Responde Q2 (Position attribution) y Q3 (Order lifecycle). Baseline físico verificada: `xKoRx/echo origin/master = 372af59a7b83604781346613da01e3d510ea1360` (sin delta al iniciar esta sesión). No implementa código productivo y no cierra D2.

## 1. Executive verdict

- `STATUS: D2-04_READY_FOR_MANAGER_REVIEW`. El diseño cierra identidades, lifecycles, ownership, exposición lógica, partial fills, múltiples Orders vivas, cancel/replace, idempotencia, reconciliation boundary, aislamiento, event ordering y crash/recovery para las cuatro entidades, con mapping físico contra Echo V3 `372af59a`.
- Decision central: **`Operation` es el aggregate lógico; el state owner físico es una función StateFun nueva `echo/operation` keyeada por `execution_account_id:account_strategy_id`**, que serializa determinísticamente todas las Signals, Orders, Fills y decisiones MM de esa cuenta+estrategia. Cuentas/estrategias distintas viven en keys distintas → aislamiento por construcción, sin store global de MM.
- **`Order` es entity del aggregate Operation (no aggregate independiente) y `Fill` es hecho inmutable** append-only. `Position` NO participa del lifecycle: es proyección read-only de observación física por `(account, contract)`, comparada contra exposición lógica sólo para telemetría (`DT-EF-POSITION-RECONCILIATION-05` sigue diferida; no hay auto-repair).
- **El venue es la autoridad física de órdenes/fills; los hechos son idempotentes y las transiciones son monótonas**, de modo que el estado final converge determinísticamente ante cancel-vs-fill cruzados, duplicados y replay: el estado final es función del set de hechos, no del orden de llegada (única excepción: corrección forward `CANCELLED→FILLED` probada por fills acumulados).
- Cero nuevas entidades genéricas: no `OperationLeg`, no `StrategyTrade`, no event sourcing, no saga, no workflow engine, no microservicio nuevo. Se reutilizan los patrones físicos existentes (StateFun keyed state, ingress/egress Kafka, kache, async PG writer, per-account command topics). `CoreCommand`/`ExecutionResult` quedan como DTOs wire legacy; el dominio nuevo nace con `Order`/`ExecutionEvent` normalizados.
- `OWNER DECISIONS REQUIRED: NONE`. El diseño vive dentro de las decisiones congeladas. Quedan dos ratificaciones técnicas ordinarias para el manager al congelar (nombres de enum `TerminalReason` y nombres de functions/topics/tablas nuevas), que no cambian semántica.

## 2. Modelo de dominio mínimo

### 2.1 Operation

- Definición: lifecycle lógico de una intención materializada para una `AccountStrategy` concreta, administrada por su `MoneyManagement`, desde la primera apertura hasta el cierre de la última exposición correspondiente (D2-02). Es el aggregate root del execution path nuevo.
- Identidad: `operation_id` UUIDv7 generado por Core al materializar (mismo generador que `utils.GenerateUUIDv7` existente). Alcance: `(execution_account_id, account_strategy_id, strategy_id, instrument_id, contract_id)`.
- Invariante D2-02: como máximo **una Operation no terminal** por `account_strategy_id`. El par `(execution_account_id, account_strategy_id)` determina unívocamente la Operation actual, lo que permite routear eventos sin conocer `operation_id`.
- Campos de autoridad (estado, no derivable): `operation_id`; `account_id`; `account_strategy_id`; `strategy_id`; `instrument_id`; `contract_id` (pinneado al crear, D2-01); `direction` (LONG/SHORT, immutable); `status`; `terminal_reason`; `created_from_signal_id`; `run_mode` (LIVE/SHADOW/DEMO/REPLAY/BACKTEST) + `run_id` (provenance para futuro Lab, constraint D1); timestamps de creación/actividad.
- Snapshot efectivo (D2-01): la Operation conserva sólo la config que su comportamiento necesita para no cambiar accidentalmente por hot updates: referencia a la versión del binding `AccountStrategy` vigente al crear, el `MoneyManagement` resuelto (id + config efectiva), y las specs vigentes del `Contract` pinneado (tick size, tick value, multiplier, qty step). No se copia configuración irrelevante ni se construye historial de revisiones.
- Datos derivados (nunca autoridad): `logical_exposure` (Σ Fills, §6), `avg_entry_price` (Σ fills ponderado), `realized_pnl` de la operación (proyección de fills, informativo V1), contador de Orders.
- State MM: blob `mm_state` namespaced dentro del estado de la Operation, propiedad exclusiva del MoneyManagement del binding (progresión Gerard, niveles de protección corrientes, etc.). El Core no interpreta su contenido; sólo lo persiste y lo entrega al MM dueño.

### 2.2 Order

- Definición: instrucción concreta y executable emitida por MM sobre una Operation, enviada a un execution venue vía adapter. Es **entity del aggregate Operation**: no existe fuera de su Operation, no tiene lifecycle autónomo, y su identidad es estable a través de modify/replace.
- Identidad: `order_id` = `client_order_id` UUIDv7 generado por Core al construir la Order. Es el idempotency key hacia el venue y viaja como correlation tag (ProjectX `customTag`, Tradovate `clOrdId`, NT tag/comment — evidencia D1 Front D). `provider_order_id` es el ID nativo del venue, nullable hasta el ack.
- Campos: `order_id`; `operation_id`; `account_strategy_id`; `account_id`; `contract_id` (heredado del pin de la Operation); `role` (ENTRY/ADD/REDUCE/EXIT — informativo de auditoría, derivado de la decisión MM que lo creó); `order_type` (MARKET/LIMIT/STOP); `side` (BUY/SELL); `qty` (contracts, unidades del Contract); `original_qty`; `limit_price`/`stop_price` cuando aplique; `filled_qty` (Σ fills de la Order); `avg_fill_price` (derivado); `status`; `order_version` (incrementa en modify); `replaces_order_id` / `replaced_by_order_id` (cadena de replace cancel+new); `decision_id` (id de la decisión MM que la originó); `created_at`/`updated_at`; `run_mode`/`run_id`.
- Efecto sobre la exposición: derivado de `side` vs `direction` de la Operation (mismo side = aumenta; side opuesto = reduce). `role` nunca es autoridad del efecto.
- Cardinalidad: `Operation 1 → 0..N Order`; múltiples Orders pueden estar vivas simultáneamente (entries paralelas, adds working mientras otra reduce). No se asume semántica MT4 ni que una Order produce un único Fill.

### 2.3 Fill

- Definición: hecho de ejecución inmutable reportado por el venue. Nunca se edita ni se borra; un fill tardío o de reconciliación se agrega igual que uno en tiempo real.
- Identidad: `provider_execution_id` del venue + `account_id`. Dedup key global: `(account_id, provider_execution_id)`. Requisito de adapter: toda ejecución debe exponer un execution id nativo (ProjectX `Trade` con id + `orderId`; NT `Execution` con executionId/orderId) o sintetizar uno determinístico en el adapter (ej. `orderId:executionId`, `orderId:seq`); el dominio nunca dedupea por heurística de precio/tiempo.
- Campos mínimos: `provider_execution_id`; `account_id`; `order_id` (client); `provider_order_id`; `operation_id` (resuelto vía Order); `account_strategy_id` (stamped para routing/queries); `contract_id`; `side`; `qty`; `price`; `executed_at` (venue time); `received_at`; `commission`/`swap` cuando el venue los entregue; `source` (EXECUTION | RECONCILIATION | HISTORY) + `run_mode`/`run_id`.
- Orden semántico: `(executed_at, provider_execution_id)`; la exposición es conmutativa (Σ), por lo que el orden de llegada no afecta el resultado, sólo el orden de disparo de reacciones MM.

### 2.4 Position

- Definición: exposición física observada/reconciliada del venue para `(account_id, contract_id)`, en modelo netting (los venues futures V1 de la cohorte D1 reportan posición neta por cuenta+contract: ProjectX `Position = account+contractId+size+averagePrice`). NO es Operation, no es aggregate del execution path y no tiene lifecycle propio.
- Autoridad: exclusivamente eventos/snapshots del venue (posición abierta/cerrada/modificada, snapshots periódicos, reconciliation snapshots). Cualquier valor lógico está prohibido en su cómputo.
- Campos: `account_id`; `contract_id`; `net_qty` (signed); `avg_price`; `venue_updated_at`; `observed_at`; `origin` (ECHO | NATIVE | MIXED_UNKNOWN). Persistida como proyección (`active_positions` hoy; tabla extendida con `contract_id` después).
- Un fill que pertenece a una Operation puede coexistir con exposición NATIVE en la misma Position física: la atribución por Operation es 100% lógica (vía Order), nunca se infiere desde deltas de Position.

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
| Estado/dirección/pin de Operation | Estado del aggregate (transiciones §3.1) | — |
| `logical_exposure` | — | Σ Fills de la Operation |
| Estado de Order | Venue (con guards de corrección forward) | — |
| `filled_qty`, `avg_fill_price` | — | Σ Fills de la Order |
| `net_qty` Position | Venue (snapshots/eventos) | — |
| Terminalidad de Operation | Decisión explícita MM (o ForceClose del safety plane) | nunca derivada sola de fills ni de Position |

## 3. Lifecycles y tablas de transición

### 3.1 Operation

```text
CREATED ──MM emite ≥1 entry Order que sale hacia el venue──▶ PENDING_ENTRY
CREATED ──MM resuelve sin acción ejecutable / rechaza entry──▶ TERMINAL(MM_NO_ACTION | ENTRY_REJECTED)
PENDING_ENTRY ──primer Fill con qty>0──▶ ACTIVE
PENDING_ENTRY ──entry orders terminales sin fill y MM decide no reintentar, o TTL de entry──▶ TERMINAL(ENTRY_EXPIRED | ENTRY_FAILED)
ACTIVE ──exposure=0 ∧ 0 live orders ∧ decisión MM de terminar──▶ TERMINAL(CLOSED)
ACTIVE/CREATED/PENDING_ENTRY ──ForceClose del safety plane entregado como decisión──▶ TERMINAL(SAFETY_FLATTEN)
```

- `CREATED`: la Signal OPEN fue aceptada y materializada (D2-02/A2: la Operation existe ANTES de MM/Orders/Fills). Guard de materialización: `now ≤ signal.valid_until`; señal expirada antes de aceptación NO crea Operation (telemetría `SIGNAL_EXPIRED`). También valida compatibilidad Strategy↔MM del binding (D2-03) y resuelve/pinnea `contract_id` (D2-01).
- `PENDING_ENTRY`: existe al menos una Order de entrada viva (`PENDING_SUBMIT/SUBMITTED/WORKING`) intentando exposición, sin fills. Una LIMIT/STOP working es estado operacional material.
- `ACTIVE`: primer Fill con exposición. Adds/reducciones/posteriores son Orders/Fills de la misma Operation; la exposición puede volver a cero temporalmente sin terminalidad.
- `TERMINAL` exige simultáneamente: `logical_exposure == 0`, cero Orders vivas (`PENDING_SUBMIT/SUBMITTED/WORKING`), y una decisión explícita de no continuar registrada (MM normal o ForceClose). `terminal_reason` obligatorio (enum técnico propuesto en §3.3).
- Quién termina: únicamente el state owner de la Operation (`echo/operation`) ejecutando una decisión MM (plugin dentro del mismo contexto keyeado) o un `ForceClose` del safety plane. Ningún otro componente (PositionSync, journal, front, gateway) muta el lifecycle.
- `direction` immutable: definida por el side de la primera Order entry; una Operation nunca cruza de LONG a SHORT ni viceversa. Reversal = terminal de la Operation actual + nueva Signal OPEN → nueva Operation (A2 congelado).
- Signal `REDUCE/CLOSE/CLOSE_ALL` con Operation inexistente → no-op con telemetría (`NO_ACTIVE_OPERATION`); no crean nada. Signal `OPEN` con Operation no terminal existente → se entrega a MM como acción sobre la Operation actual (D2-02), nunca crea segunda Operation.
- Recovery tras restart: §8.5. El estado se recupera de checkpoints StateFun + PG y se reconcilia contra el venue; la terminalidad no se infiere de la ausencia de mensajes.

### 3.2 Order

```text
PENDING_SUBMIT ──submit aceptado por adapter──▶ SUBMITTED
SUBMITTED ──ack/working del venue──▶ WORKING
PENDING_SUBMIT/SUBMITTED ──reject del venue o fallo de transporte terminal──▶ REJECTED
WORKING ──Σ fills ≥ qty (o venue reporta FILLED)──▶ FILLED
WORKING ──cancel confirmada con Σ fills < qty──▶ CANCELLED
WORKING ──modify nativo aceptado──▶ WORKING (order_version++, audit trail)
WORKING ──replace como cancel+new──▶ CANCELLED(REPLACED) + nueva Order (replaces_order_id)
WORKING ──expiración venue (TTL/GTD)──▶ EXPIRED
CANCELLED/EXPIRED ──fills tardíos dejan Σ fills ≥ qty──▶ FILLED (única corrección forward permitida)
```

- `PENDING_SUBMIT`: Order construida por MM, aún no entregada (delays anti-detección, backpressure del adapter).
- Partial fill NO es un estado: es `WORKING` con `filled_qty > 0`. Menos estados, menos ambigüedad; `filled_qty` es el dato.
- Reject/cancel/expiry de una Order NUNCA termina la Operation (A2): MM decide retry/replace/replanear con una Order nueva (nuevo `order_id`, misma `decision_id` si es reintentos del mismo intent).
- Corrección forward única: si una Order `CANCELLED/EXPIRED` recibe fills tardíos que la dejan completamente ejecutada, su estado se corrige a `FILLED` (el venue ejecutó; los fills son hechos). `REJECTED` nunca se corrige. `FILLED` nunca se degrada.
- `race fill-vs-cancel`: ambos eventos se procesan; el fill se appendea idempotentemente; el estado final de la Order es el último estado autoritativo del venue con la corrección forward de arriba. El resultado converge (§5.3).

### 3.3 Terminal reasons (propuesta técnica, ratificación manager)

- `MM_NO_ACTION` (MM no resolvió acción ejecutable desde CREATED); `ENTRY_REJECTED` (orders entry rechazadas y MM desiste); `ENTRY_EXPIRED` (TTL de entry/signal sin fill); `ENTRY_FAILED` (fallo de transporte terminal sin fill); `CLOSED` (cierre normal MM: full reduction, CLOSE/CLOSE_ALL ejecutado, stop/target de MM); `SAFETY_FLATTEN` (ForceClose del plano safety/provider).

## 4. Invariantes

- I1: como máximo una Operation no terminal por `(execution_account_id, account_strategy_id)` (D2-02).
- I2: toda Order pertenece a exactamente una Operation; todo Fill pertenece a exactamente una Order (y por transitividad a una Operation). No hay fills huérfanos: un evento sin resolución de identidad va a cuarentena de eventos (telemetría + reprocess), nunca se inventa atribución.
- I3: `direction` de la Operation es immutable y la exposición nunca cambia de signo; las Orders de reducción se construyen con `qty ≤ logical_exposure` (check de construcción; el venue es autoridad final; exceso del venue → clamp + evento `EXPOSURE_ANOMALY`, nunca corrupción silenciosa).
- I4: `logical_exposure == Σ±Fill.qty` siempre; se recalcula de los Fills, jamás se ajusta manualmente ni se lee desde Position.
- I5: TERMINAL requiere `{exposure == 0} ∧ {0 Orders vivas} ∧ {decisión explícita de no continuar}` (A2). Un estado de Order no termina la Operation; exposición cero temporal no termina la Operation; Position nunca termina la Operation.
- I6: `Operation.contract_id` es write-once al materializar; un hot update del mapping `Instrument → Contract` afecta sólo Operations nuevas (D2-01).
- I7: todo evento de ejecución es idempotente por su identity natural (§5.1); reprocesarlo no cambia estado ni exposición.
- I8: las transiciones de estado son monótonas y guardadas; no hay paths que revivan aggregates terminales (única excepción: corrección forward `CANCELLED/EXPIRED → FILLED` de Order).
- I9: una cuenta no puede mutar el estado de otra: todo mutador de estado vive en un contexto keyeado por `(execution_account_id, account_strategy_id)` o `(execution_account_id)` de sólo-encaminamiento; no existe store global mutable de cuentas accesible por MM (§8).
- I10: `Position` es write-only desde eventos del venue y read-only para el resto; jamás dispara transiciones de Operation.
- I11: toda entidad carries `run_mode` + `run_id` (provenance LIVE vs simulado) — constraint de reutilización para replay/backtest del D1.
- I12: fills y facts son append-only; la mutación de estado se limita a columnas de status/version de Operation/Order (audit trail `order_events`/`operation_events` para cambios), sin reescribir historia.

## 5. Idempotencia, cancel/replace y races

### 5.1 Idempotency keys

| Flujo | Key | Mecanismo |
|---|---|---|
| Signal procesada | `(account_strategy_id, signal_id)` | dedup set con TTL en el keyed state; replay de Kafka no re-materializa |
| Orden enviada | `client_order_id` (UUIDv7) | viaja como correlation tag al venue; reintentos de submit reutilizan el mismo id; el adapter dedupea donde el venue no lo hace |
| Fill | `(account_id, provider_execution_id)` | dedup set + PK inmutable en PG; duplicados → métrica + drop |
| Decisión MM | `decision_id` (UUIDv7) | las Orders la referencian; replay de la misma decisión no duplica Orders |
| Replace | `replace_request_id` | idempotencia de modify/cancel (venue puede duplicar acks) |
| Reconciliation | mismos keys que el flujo normal | los hechos de reconciliación pasan por las mismas guards |

### 5.2 Cancel/replace

- Replace preferente: si el venue soporta modify nativo (ProjectX `order-modify`, NT `Change`), la Order conserva `order_id` y `provider_order_id`, incrementa `order_version` y registra snapshot previo/posterior en `order_events`. `qty` refleja la cantidad working actual; `original_qty` se preserva.
- Replace cancel+new (venues sin modify): la Order vieja termina `CANCELLED(REPLACED)`, se crea una Order nueva con `replaces_order_id` y la misma `decision_id`; la cadena es auditable y el intent MM queda agrupado.
- Cancel request = comando con id propio (`replace_request_id`/`cancel_id`); el ack del venue es el que transiciona la Order; la ausencia de ack activa timeout del adapter → reconciliación (query del estado real), no asunción.

### 5.3 Race fill-vs-cancel (caso D del mandato)

- Ambos eventos entran por la cola serializada de la Operation y se aplican como hechos: el fill se agrega (dedup por execution id), la cancelación se registra. Reglas de convergencia: si el venue confirma cancelled con `Σ fills < qty` → `CANCELLED` con `filled_qty` retenido; si los fills acumulados alcanzan `qty` (aunque el ack de cancel llegó primero) → corrección forward a `FILLED`. Exposición final = Σ fills en ambos casos. El resultado es función del set de hechos del venue, no del orden de llegada → determinístico.

### 5.4 Duplicados y replay

- Kafka at-least-once + replays: todos los handlers aplican I7. Duplicados de ejecución tras reconnect/replay (receta Databento/CME aceptada en D1): dedup por `provider_execution_id` (y `ts_event`/count donde aplique) dentro del dedup set con TTL, más la PK inmutable en PG como segunda barrera.
- Eventos de reconexión que traen snapshot completo de orders/posiciones: cada snapshot se materializa como eventos diff-only (estado venue reportado por Order/Position) que pasan por las mismas guards monótonas.

### 5.5 Reconnect / recovery de hechos

- Al (re)conectar, el adapter ejecuta: resubscribe a streams de orders/executions/positions + query de estado autoritativo (ProjectX `Order/searchOpen` + positions; NT `Orders/Executions/Positions`) + fetch de historial de executions desde el último hecho visto (capacidad documentada en D1 Front D por transporte).
- Los hechos recuperados entran con `source = RECONCILIATION|HISTORY` y las mismas guards: convergen sin caso especial. Si un transporte no puede recuperar historial de fills, el gap queda visible como `POSITION_MISMATCH` persistente (fail-visible, no silencioso).

## 6. Derivación de exposición lógica

- Definición: `logical_exposure(op) = Σ_fills sign(fill) × qty`, con `sign = +1` si `fill.side == op.direction`, `-1` en caso contrario. Unidad: contracts según spec del Contract pinneado (no pips; constraint cross-market V1 del proyecto).
- Ejecución incremental: contador firmado mantenido en el keyed state, recalculable siempre desde `echo.fills` (PG) como verificación; cualquier divergencia contador↔recomputo es bug y se alarma.
- Restricciones: la exposición nunca cambia de signo (I3); reduce-orders se validan contra la exposición actual al construirse; fills que reducen dejan la exposición en `[0, max]`.
- La exposición es por Operation y por `contract_id` pinneado: dos Operations del mismo instrumento con contrastos físicos distintos (rollover) nunca comparten exposición lógica aunque la Position física del venue pueda netear contratos contiguos (mismatch visible, no reparado — DT-05).
- Caso A (mandato): OPEN + MM BUY 2 → entry Order qty 2 → dos partial fills de 1 → exposición +2, Operation `ACTIVE`. Caso B: REDUCE + MM SELL 1 → reduce Order → fill → exposición +1, misma Operation. Caso C: add de MM → nuevas Orders sobre la misma Operation, exposición crece.

## 7. Position / reconciliation boundary

### 7.1 Autoridad física

- Position se actualiza únicamente con eventos/snapshots de posición del venue, enrutados por `account_id` hacia la proyección (patrón `PositionSyncFn` → `active_positions` existente, extendido con `contract_id`). Sin I/O en el hot path de decisiones.

### 7.2 Correlación con Operations sin atribución falsa (Q2)

- La atribución de fills a Operations es **estructural**: cada Fill llega referenciando la Order que Echo emitió (client correlation tag / provider order id resuelto en el router §8.2). No se atribuyen fills por inferencia de deltas de Position.
- En cuentas netting, la Position física agrega todo (Operations Echo + trading NATIVE/manual); V1 no intenta descomponerla por Operation ni reclama ownership físico por Strategy. La verdad por Operation es 100% lógica (I4).
- La identidad física de Position es `(account_id, contract_id)` — coincide con el modelo de los venues futures de la cohorte (netting por contract), por lo que no se requiere modo hedging en V1.

### 7.3 Comparación y mismatch V1

- Comparador periódico (proyección, fuera del hot path): por `(account, contract)`: `physical_net_qty` vs `Σ exposure de Operations no terminales sobre ese contract + exposición NATIVE conocida si existe`. Delta fuera de tolerancia → evento/telemetría `POSITION_MISMATCH{account, contract, physical, logical, delta, ts}` + surface de observabilidad.
- V1 NO hace auto-repair, synthetic fills, remapping ni subsystem de reconciliación (DT-EF-POSITION-RECONCILIATION-05 diferido, reafirmado). El mismatch es señal para el operador/safety plane; la única reacción automática permitida es la telemetría y (si el owner lo habilita por config) el bloqueo de nuevas aperturas de esa cuenta por el safety plane existente, nunca la mutación del estado lógico.
- Caso F (mandato): dos Strategies de la misma Account con exposición opuesta sobre el mismo Contract → dos Operations lógicas independientes (+N y −M), una Position física neta (N−M). Ambas verdades coexisten; el comparador usa la suma.

## 8. Runtime: ownership, aislamiento y recovery

### 8.1 State owner y partition key

- Owner del estado: función StateFun nueva `echo/operation`, una instancia por `key = execution_account_id + ":" + account_strategy_id`. Es el único mutador del estado de Operation/Order y de la exposición, y el contexto de invocación de MM. Serializa todos sus mensajes (garantía StateFun por key) → determinismo por cuenta+estrategia.
- Función de routing `echo/execution_router` keyeada por `execution_account_id`: recibe TODOS los eventos de ejecución del venue de esa cuenta (orders/executions), resuelve la Operation destino y reenvía. Resolución: (a) primaria, correlation tag del cliente (`client_order_id`) echoeado por el adapter; (b) fallback, registry `provider_order_id → (account_strategy_id, operation_id, order_id)` mantenido en su keyed state cuando se registran Orders vivas (cubre reconnect/replay sin tags). Eventos irresolubles → cuarentena de eventos con reprocess, jamás atribución inventada (I2).
- MM vive como plugin de dominio invocado dentro de `echo/operation`: recibe el contexto de esa Operation + snapshots de cuenta/instrumento (patrón join de `MMEngineFn` reutilizado) y devuelve decisiones (0..N Order requests, modify/cancel, terminal). MM nunca accede a estado de otras keys ni a un store global (I9). El aislamiento es por construcción del runtime, no por disciplina.

### 8.2 Topología de topics (nueva, paralela a la legacy)

| Topic | Key | Target | Contenido |
|---|---|---|---|
| `echo.signals.v1` (nuevo) | strategy_id | `echo/signal_fanout` (nuevo) | Signal canónica D2-03 emitida por StrategyEngine |
| `echo.execution-events.v1` (nuevo) | execution_account_id | `echo/execution_router` (nuevo) | eventos normalizados del venue: order ack/status, fills, positions |
| `echo.order-commands.{account_id}.v1` (nueva familia) | command/order id | adapter de ejecución | OrderRequest / Modify / Cancel hacia el venue (patrón per-account topic existente en `CommandConsumer`) |
| `echo.operation-facts.v1` (nuevo) | op key | `echo/operation_store` (nuevo) | facts de dominio para proyección PG (async writer) |
| configs (existente) | — | kache/KVS | `AccountStrategy` bindings, Instrument/Contract specs + hot mapping (patrón symbol_mapping_handler) |

- `echo/signal_fanout` reemplaza funcionalmente el fan-out de `ExecutionPlannerFn`: lee bindings habilitados por strategy desde kache y entrega la Signal a cada `echo/operation` por su key, filtrando por whitelist/estado de cuenta (patrón RFC-007 existente).
- Las funciones nuevas se registran en `module.yaml` con ingress/egress propios (patrón exacto del existente); la topología legacy (reference-events, execution-results, trade-closes) queda intacta durante la migración.

### 8.3 Event ordering

- Orden por cuenta+estrategia: Kafka preserva orden por key con producer idempotente (config explícita `max.in.flight ≤ 5` con idempotence, o 1); StateFun procesa serialmente por instancia → las Signals y eventos de una Operation se aplican en orden.
- Orden intra-evaluación: StrategyEngine sella `signal_seq` monótono por strategy; el fan-out preserva el orden por key; `echo/operation` rechaza regresiones (dedup + telemetría). CLOSE_ALL→OPEN en la misma evaluación se aplica en orden (A1: procesamiento determinístico).
- Orden venue: `executed_at` + `provider_execution_id` para el orden semántico de fills; guards monótonas hacen el estado final independiente del orden de llegada (§5).

### 8.4 Aislamiento MM (requisito crítico §6 del mandato)

- `events para (account A, strategy S) → única instancia `echo/operation` key A:S, serial y determinística; `events para (account B, …)` → instancias independientes, sin memoria compartida. Fills de A jamás tocan exposición de B (I9).
- MM recibe: su Operation (estado + Orders + Fills + mm_state), AccountSnapshot de su cuenta, specs del Contract pinneado, proyección Position de su cuenta (read-only), y la Signal corriente. Produce: Order requests, modify/cancel, decisión terminal, mutación de su `mm_state`. Con esto el caso G (reject de entry en una cuenta mientras otra llena) queda: cada key procesa su resultado; el reject termina/repplantea la Operation de A sin tocar la de B.

### 8.5 Crash / recovery

- Capa 1 (hot): Flink/StateFun checkpointing del keyed state (infra existente) → reanudación rápida con el estado previo al fallo.
- Capa 2 (durable): PG `echo.operations` / `echo.orders` / `echo.fills` (§10) escrita async desde `echo/operation_store`. Al detectar gap/divergencia de checkpoint, la instancia reconstruye el estado no terminal desde PG (operaciones no terminales + Orders vivas + todos los fills) al primer toque de la key.
- Capa 3 (física): reconciliación de venue al reconectar (§5.5) — la verdad física de orders/posiciones vivas es el venue; los facts perdidos (fills durante la caída) se recuperan del historial del venue con `source=HISTORY`.
- Convergencia: las tres capas aplican las mismas guards monótonas e idempotencia (I7/I8); el caso E del mandato (Core cae y vuelve, eventos duplicados) converge sin doble exposición porque el dedup por execution id y la recomputación de exposición desde fills absorben duplicados.

### 8.6 Hot path y persistencia

- En el hot path (signal → materialización → sizing → submit) no hay I/O remoto síncrono: snapshots de cuenta/instrumento se sirven de las KVS functions / kache (patrón actual); la proyección PG es egress async batched (patrón `PositionSyncFn`/`AccountSyncFn`).
- Persiste durablemente: identidad/estado de Operation y Orders (status/version), todos los Fills (inmutables), decisiones terminales y `mm_state` (blob, para recuperar la progresión económica). En bounded keyed state (checkpointed): dedup sets con TTL, registry del router (sólo Orders vivas), contadores de exposición.
- Volumen: el estado vivo por key es acotado (1 Operation no terminal + sus Orders vivas + sets TTL); la historia completa vive en PG, no en el estado caliente.

### 8.7 Backtest / replay reuse

- Las entidades, la máquina de transiciones y el contrato de decisiones MM viven como paquetes Go puros (SDK domain layer), sin imports de Kafka/StateFun; las funciones StateFun son adaptadores finos que invocan el mismo motor. `SimExecution` implementa el mismo contrato `ExecutionEvent` que los adapters reales (fills determinísticos por seed).
- El backtester futuro ejecuta la secuencia `Signal → Operation → MM → Order → Fill → exposición` con el mismo código de dominio y Clock/event-time inyectables, cumpliendo la constraint de reutilización del D1 sin `*_live` vs `*_backtest`.

## 9. Mapa físico Echo V3 — REUSE / EXTEND / ADAPT / REPLACE / DEFERRED_DEBT

Baseline `xKoRx/echo@372af59a`. Clasificación con evidencia física (repo/path/símbolo).

| Pieza V3 actual | Disposición | Base física y razón |
|---|---|---|
| StateFun runtime + module.yaml ingress/egress + Go SDK | **REUSE** | `v3/core/deploy/flink-statefun/develop/module.yaml` (ingress/egress por topic, targets `echo/*`); `v3/sdk/statefun/constants.go` (function types, topics, ValueSpecs). Se registran functions/topics nuevos con el mismo mecanismo. |
| kache (cache en-proceso de topics compactados) | **REUSE** | `v3/sdk/kache/` (AccountCache/StrategyCache, consumer group propio). Sirve bindings AccountStrategy + specs Instrument/Contract + hot mapping al fan-out y a MM sin I/O. |
| ExecutionPlannerFn (fan-out por strategy → N cuentas) | **ADAPT** | `v3/core/internal/functions/execution_planner.go` (blob 371bf5e3…): patrón de fan-out con validación RFC-007 y kache. Su sucesor `echo/signal_fanout` consume `Signal` (no ReferenceEvent); keyed hoy por trade_id vía ingress, el nuevo fan-out reenvía por `(account, account_strategy)`. |
| MMEngineFn (join snapshots + calculators + comando) | **ADAPT/EXTEND** | `v3/core/internal/functions/mm_engine.go` (blob e725ceb0…): patrón join Account+Instrument con pending TTL 30s y `SendAfter` para delays es reutilizable; su lógica se convierte en invocación del plugin MM dentro de `echo/operation` (ya no necesita pending cross-message: el estado vive en el aggregate). |
| sdk/mm calculators (fixed_lot/fixed_risk) | **REUSE/EXTEND** | `v3/sdk/mm/calculator.go` (`Calculator`, `CalculationInput/Result`), `fixed_lot.go`, `fixed_risk.go`, `pip_size.go`. Primitivas puras de sizing; se extienden a unidades instrument-spec (tick/contract multiplier ya presentes en `InstrumentSnapshot.TickValue/TickSize/ContractSize`) eliminando la semántica pips del camino nuevo (constraint cross-market). |
| CoreCommand | **ADAPT (wire DTO)** | `v3/sdk/domain/reference_event.go` (`type CoreCommand`): transporte con SL/TP físicos+ideales y metadata journal. Continúa en la path legacy; el dominio nuevo emite `OrderRequest` (DTO equivalente con `client_order_id`, `contract_id`, tipo/qty/precios) hacia adapters futures; `CoreCommand` no se promueve a aggregate. |
| ExecutionResult | **ADAPT** | mismo blob: colapsa a single result/fill. Se sustituye por `ExecutionEvent` normalizado (ack/status/fill/position) en la path nueva; el Bridge legacy sigue emitiendo `ExecutionResult` hasta su migración (DT-EF-REFERENCE-SIGNAL-03). |
| ExecutionStoreFn + ExecutionStore/OpenExecution | **REPLACE (autoridad)** | `v3/core/internal/functions/execution_store.go` (blob d8c61700…): estado por trade_id con OpenExecution single-fill y dedup por ticket. No es autoridad del lifecycle nuevo (su modelo no representa Order 1→N Fill ni adds); sobrevive como proyección de compatibilidad de la path legacy hasta retiro (registro D1 §6). |
| PositionSnapshot / PositionSyncFn | **REUSE/EXTEND** | `v3/sdk/domain/position_snapshot.go` (blob 443b6ba2…) + `v3/core/internal/functions/position_sync.go` (upsert idempotente + delete por batch ausente, async writer). Se extiende con `contract_id` y se mantiene como proyección física (§7); nunca se eleva a authority del lifecycle. |
| AccountSnapshot / InstrumentSnapshot + acc/inst_snapshot KVS | **REUSE/EXTEND** | `v3/sdk/domain/snapshots.go` (blob d319d0a3…) + `acc_snapshot.go`/`inst_snapshot.go`: KVS por account y broker:symbol para el join MM. Extensión: specs de Contract (expiry/venue ids) sin mezclar instrumento económico con símbolo físico (gap ya registrado en D1). |
| ExecutionPolicy / StrategyConfigFn | **ADAPT** | `v3/sdk/domain/execution_policy.go` (blob 295f7ea2…) mezcla binding+risk+knobs; `strategy_config.go` es KVS por strategy_id. Se separa en `AccountStrategy` (binding+compatibilidad), config MM y knobs de ejecución; el KVS pasa a keyear/configurar bindings por account_strategy. |
| CloseHandlerFn / CloseBatchCommand / CloseAllAccountCommand / automation_evaluator | **REUSE (safety plane)** | `v3/core/internal/functions/close_handler.go`, `v3/sdk/domain/trade_close.go` (CloseCommand/CloseBatch/CloseAllAccount): el flatten account-wide y las acciones de automation son el plano safety/provider existente; emite `ForceClose` hacia las Operations afectadas (terminal `SAFETY_FLATTEN`) sin convertirse en CLOSE_ALL de Strategy (D2-03). |
| Bridge (sesiones, command consumer, pipes, producer) | **REUSE (patrones) / ADAPTER NUEVO** | `v3/bridge/internal/session/command_consumer.go` (topic dedicado por cuenta, commit híbrido, circuit breaker) y `pipe_handler.go` (publica `ExecutionResult` con key=TradeID, `PositionSnapshots` con key=AccountID). Los patterns son el estándar para los adapters futures (ProjectX/NT); el adapter MetaTrader actual no se deforma. |
| trade_journal / canonical_operations / TradeJournalFn | **REUSE intacto (boundary analítico)** | `v3/core/internal/functions/trade_journal.go`, migraciones 062/064. No es state owner del runtime nuevo; la proyección Operation→Trade queda diferida a The Lab (owner 2026-09-26). |
| Hot symbol mapping (Gateway→Kafka→cache) | **REUSE/EXTEND** | `v3/gateway/internal/symbol_mapping_handler.go` (blob a9364d4a…): patrón hot-update compactado; se extiende a mapping `Instrument → Contract` con la misma mecánica; el pin de Operation (I6) vive en el dominio, no en el mapping. |
| PostgreSQL como store duradero + migraciones numeradas | **REUSE** | `v3/sdk/postgres/migrations/` (…064 canonical_operations, 065 lab_curves). Nuevas migraciones para `operations/orders/fills`; numeración a coordinar en implementación (la rama E-04 fuera de master reservó 068). |

## 10. Implicaciones de refactor / migración

- SDK domain nuevo (paquete puro): structs `Operation/Order/Fill/Position(proyección)`, enums de estado, máquina de transiciones con guards, y contratos `MMPlugin` (decisiones) + `ExecutionEvent` (eventos venue) + `SimExecution`. Sin dependencias de infra — es el boundary Q14.
- Core: 4 function types nuevos (`echo/signal_fanout`, `echo/operation`, `echo/execution_router`, `echo/operation_store`) + registro en `module.yaml` (ingress signals/execution-events, egress order-commands/operation-facts). Patrón idéntico al existente; cero cambio en functions legacy.
- PG: migraciones nuevas `echo.operations` (upsert por operation_id), `echo.orders` (upsert por order_id + tabla `order_events` append-only), `echo.fills` (insert-only, PK `(account_id, provider_execution_id)`), índices por `(account_strategy_id, status)` y `(contract_id)`. Numeración a coordinar con ramas en vuelo al implementar.
- Adapters futures (D6): implementan el contrato `ExecutionEvent` + per-account command consumer + reconciliación de reconexión (§5.5); cada rareza de venue queda aislada en su adapter (regla KISS del mandato), sin deformar el dominio.
- Legacy: la path Reference→ExecutionPlanner→MMEngine→CoreCommand→Bridge sigue operando intacta; el adapter `ReferenceEvent → Signal` (DT-EF-REFERENCE-SIGNAL-03) es el puente futuro para que la path legacy converja al mismo runtime. ExecutionStoreFn queda como proyección de compatibilidad.
- Refactors bloqueantes detectados: ninguno nuevo que exceda el registro D1 §6 (Signal boundary limpio + identities/lifecycle eran ya blocking design items; este workstream los especifica). No hay reescritura de Core (Q1 owner-accepted).

## 11. Riesgos y deudas

- **R1 — Ordering Kafka:** la garantía de orden por key depende de config explícita del producer (idempotence + in-flight limitado) y de no re-keyear en tránsito; el egress StateFun serializa por instancia, pero el ingress debe keyear consistentemente. Mitigación: convención de keys en un solo lugar (constants) + test de orden.
- **R2 — Dedup sets ilimitados:** los sets de idempotencia crecen con el volumen; mitigación TTL + bounded (un fill viejo no puede duplicar una Operation terminal; el PG PK es segunda barrera).
- **R3 — Historial de fills por transporte:** la recuperación post-gap depende de que cada venue exponga execution history; donde no, el gap queda visible como mismatch persistente (fail-visible). Es requisito de selección de adapter, no defecto del dominio.
- **R4 — Capacity 100–200 cuentas:** el diseño multiplica estado por (cuenta×estrategia) y fan-out por signal; el trabajo por instrumento (feed/estrategia) no se multiplica por cuenta (requerimiento del proyecto). El benchmark de capacidad sigue siendo trabajo D6 (misma disposición D1); nada del diseño lo impide arquitectónicamente.
- **R5 — ForceClose vs MM concurrently:** un flatten del safety plane mientras MM gestiona puede duplicar intents de cierre; mitigación: los hechos son idempotentes, los venues dedupean por client tag, y la terminalidad exige exposición 0 — el doble intento converge, no corrupte.
- **R6 — Deuda existente heredada:** `DT-EF-POSITION-RECONCILIATION-05` (política de mismatch) sigue diferida; `DT-EF-REFERENCE-SIGNAL-03` (migración del execution path) sigue siendo el carril que conecta legacy→nuevo; unidades pips legacy (deuda con ID pendiente de ratificación owner) no entra al camino nuevo (calculators extendidos a instrument-spec units).
- **R7 — Reloj y `valid_until`:** la validez de Signal y TTLs de entry usan event-time de Core (no del venue); una discusión fina de clock skew queda en el diseño técnico de implementación (no cambia el modelo).

## 12. Decisiones owner

- `OWNER DECISIONS REQUIRED: NONE`. El diseño implementa las decisiones congeladas D2-01/D2-02/D2-03 y el lifecycle A2 sin reabrirlos y sin `BLOCKED_OWNER_DECISION`.
- Ratificaciones técnicas ordinaras para el manager (no owner, no cambian semántica): (1) enum `TerminalReason` propuesto en §3.3; (2) nombres físicos de functions/topics/tablas nuevas (§8.2/§10).

## 13. Casos de aceptación (criterio de calidad §12 del mandato)

- **A — OPEN + BUY 2 con dos partial fills:** Signal OPEN aceptada → Operation CREATED (contract pinneado) → MM sizing 2 → entry Order WORKING → fill 1 + fill 2 (dedup por execution id) → exposición +2, `ACTIVE`. Dos Orders no son necesarias: una Order con 2 Fills.
- **B — REDUCE SELL 1:** Signal REDUCE → MM resuelve reduce Order qty 1 (side opuesto, ≤ exposición) → fill → exposición +1, misma Operation, `ACTIVE`.
- **C — add/hardscale:** MM emite nuevas Orders (nuevos `order_id`, misma `decision_id` o decisiones nuevas) sobre la misma Operation; exposición crece; `role=ADD` informativo.
- **D — cancel-vs-fill cruzados:** cancel request y fill en tránsito: fill appendeado idempotentemente, estado de Order converge por la regla venue-authoritative + corrección forward (`FILLED` si Σ fills ≥ qty; si no, `CANCELLED` con filled_qty retenido); exposición = Σ fills; MM reacciona al estado convergido.
- **E — caída y vuelta del Core:** checkpoints StateFun + PG + reconciliación de venue; eventos duplicados absorbidos por dedup; exposición recomputable desde `echo.fills`; ninguna doble exposición posible.
- **F — dos Strategies opuestas, misma Account/Contract:** keys `(acct,S1)` y `(acct,S2)` independientes → dos Operations lógicas (+N/−M) con sus fills atribuidos estructuralmente; Position física neta (N−M) observada por la proyección; mismatch checking usa la suma; ninguna de las dos Operations ve ni muta a la otra.
- **G — reject en una cuenta, fill en otra:** el reject transiciona la Order de A (REJECTED) y MM de A decide retry/desistir (Operation terminal si desiste); la cuenta B procesa su fill y queda `ACTIVE`; no existe ningún path de estado entre keys distintas (I9).

## 14. Evidencia

- Vault: `main/10-projects/Echo Futures/Echo Futures.md` (D2-01/02/03 OWNER_CLOSED; lifecycle A2; requisitos owner), `main/10-projects/Echo Futures/Echo Futures — D1 Analysis Pack.md` (matriz Q1/reuse, Front D order lifecycle inputs, `DT-EF-*`), contrato de ambiente `main/30-resources/aranea/07-integration/Echo + Echo Forge — Environment Contract.md`.
- Repo físico (todos verificados por esta sesión vía `git show 372af59a:<path>` en clon `~/aranea/work/d4-shot1-20260925/echo`, fetch de origin con `origin/master = 372af59a7b83604781346613da01e3d510ea1360`): `v3/sdk/domain/reference_event.go` (ReferenceEvent/CoreCommand/ExecutionResult/CalculateRiskReq), `v3/sdk/domain/trade_close.go` (OpenExecution/ExecutionStore/CloseCommand/CloseBatch/CloseAllAccount), `v3/sdk/domain/position_snapshot.go`, `v3/sdk/domain/snapshots.go` (Account/InstrumentSnapshot, `Topics`), `v3/sdk/domain/execution_policy.go`, `v3/core/internal/functions/{execution_planner,strategy_config,mm_engine,execution_store,position_sync,close_handler,acc_snapshot,inst_snapshot}.go`, `v3/sdk/statefun/constants.go` (function types/topics/ValueSpecs), `v3/sdk/mm/calculator.go` (+fixed_lot/fixed_risk/pip_size), `v3/core/deploy/flink-statefun/develop/module.yaml` (ingress keys y targets), `v3/bridge/internal/session/command_consumer.go` (per-account topics), `v3/bridge/internal/pipe_handler.go` (keys de publicación: ExecutionResult/CloseResult = TradeID, PositionSnapshots = AccountID), `v3/sdk/kache/README.md`, `v3/sdk/postgres/migrations/` (064 canonical_operations, 065 lab_curves), `v3/sdk/utils/uuid.go` (GenerateUUIDv7).
- Verificación de baseline: `git fetch origin` + `git rev-parse origin/master` = `372af59a…` (sin delta respecto a la baseline conocida de D2); `git merge-base --is-ancestor` OK.

## Fuentes

- [[Echo Futures]] — proyecto canónico y decisiones owner D2-01/02/03.
- [[Echo Futures — D1 Analysis Pack]] — evidence baseline D1 aceptada.
- `xKoRx/echo@372af59a` — source físico V3 inspeccionado (paths en §14).
