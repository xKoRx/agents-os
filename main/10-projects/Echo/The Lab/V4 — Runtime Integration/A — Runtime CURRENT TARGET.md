---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo — Producto Integrado]]"
  - "[[F — Decision Register]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-22"
updated: "2026-10-22"
---

# A — Runtime CURRENT TARGET

## Propósito

Fijar el contrato ejecutable CURRENT→TARGET del runtime que integra Forge, master, journal y LAB, conservando un escritor por hecho y un solo motor operacional. Este documento es diseño Shot 1 del programa de cuatro shots; no certifica implementación, despliegue ni capacidad física. D24 prevalece sobre los handoffs anteriores: única base Echo `feature/ef-runtime-pools@2ee61791deb3139be23e1c9be3708b1d41da8d6b`; ninguna capacidad de ramas antiguas cuenta como CURRENT ni se integra el backtester histórico.

## Contenido

### 1. Corte y resultado

Lectura local del checkout autorizado con `git rev-parse HEAD` y `git status --short`: SHA exacto anterior, árbol limpio. Todas las referencias `[E##]` son `xKoRx/echo` en ese SHA, líneas del código actual; rutas relativas al repo. Sin pruebas/builds ni operaciones de infraestructura en Shot 1. El contexto obligatorio comprende [[F — Decision Register]] D09/D10/D11/D16–D24, [[0 — Submanager State]], [[SHOT4_HANDOFF]], [[Echo — Producto Integrado]], [[THE_LAB_V4_Diseno_para_revision]] y [[1 — TECHNICAL_FREEZE_PACKET]]; estos últimos aportan requisitos compatibles, no implementación vigente. Los números de línea históricos del freeze se sustituyen por los de este corte.

**Resultado de diseño:** dos fuentes operacionales legítimas. `EXTERNAL_REFERENCE` observa una estrategia ejecutada fuera del runtime nativo y usa el camino master/copiador/journal existente, con `readiness_mode=OBSERVE_MASTER`. `NATIVE_RUNTIME` utiliza Strategy→Signal→AccountStrategy→Operation del motor actual. La ingestión registra identidad y solicita provisión; jamás fabrica un Signal técnico, Fill o una Operation nativa para aparentar integración. Ambas rutas desembocan en el mismo servicio de historia V2 mediante adaptadores de hechos; LAB no gobierna trading y puede estar detenido sin impedir journalización.

### 2. CURRENT demostrado: entidades, identidades y escritores

| Hecho / entidad | Identidad y escritor actual | Evidencia y límite |
|---|---|---|
| Strategy de registro | `(registry_namespace, canonical_strategy_id)`→`strategy_ref`; repository/servicio de ingestión persiste mapping, aliases scoped | [E01] `v3/sdk/postgres/strategy_identity_repository.go:35,91,161,235`. Magic, nombre o broker no sustituyen identidad. |
| StrategyDefinition de copier | `ID=strategy_id`; configuración declarativa usada por ExecutionPolicy loader | [E02] `v3/sdk/domain/execution_policy.go:56,99`. No es por sí sola StrategyVersion ni Strategy técnica ejecutable. |
| Strategy técnica | Plugin puro `Strategy.Evaluate`, elegido por `StrategyDef{ID,Module,StreamID,Params}`; owner strategy genera output | [E03] `v3/sdk/futures/strategy/strategy.go:17`; `v3/sdk/futures/config/snapshot.go:29,50`; `v3/core/internal/futuresruntime/runtime.go:156`. Módulos admitidos `s1/s2/tg`; no compilación genérica de EA Forge por recibir JSON. |
| StrategyVersion | Paquete write-once `(namespace,version_ref)`; ref S0 recomputado desde canonical/platform y cuatro hashes | [E04] `v3/sdk/postgres/strategy_version_repository.go:15,50,76,101,200`. Validador actual admite sólo `MT5/MT4`; no posee recipes `native-v1/definition-v1` del TARGET. |
| `domain.Signal` técnico | `DeriveSignalID(strategy_id,run_mode,run_id,eval_seq,signal_seq)`; Strategy owner, salida inmutable sin cuenta/contrato/MM | [E05] `v3/sdk/futures/domain/signal.go:33,78,117`. StrategyCycleSeq agrupa ciclo; ni `strategy_version_ref` ni tenant están en Signal. |
| AccountStrategy | Binding Account+Strategy+MM+enabled/config; fanout target da `(account_id,account_strategy_id)`, instrumento y tuple opcional pool | [E06] `v3/sdk/futures/strategy/fanout.go:14,19,61,71`. OwnerKey `account:account_strategy`, validado sin `:` en componentes: `v3/sdk/futures/domain/identity.go:67`. Scope tenant/run no está en la clave actual. |
| SignalDelivery | Fanout copia señal técnica con binding y tuple asociación/generación/epoch; no reevalúa Strategy | [E07] `v3/sdk/futures/domain/fanout.go:13,84,92`; `v3/sdk/futures/strategy/fanout.go:107`. Enabled bloquea nuevo OPEN pero conserva management del ciclo vivo. |
| Operation | Aggregate raíz por ciclo ejecutado de AccountStrategy; Operation owner después de admisión y pin de contrato/MM/binding | [E08] `v3/sdk/futures/domain/operation.go:145`; `v3/sdk/futures/operation/engine.go:1148,1182,1194,1251,1275`. Operation nace antes de `invokeMM`. No hay versión, Q_i ni tiempos de apertura/cierre certificados en su forma actual. |
| OperationID / OrderID | Engine consume ordinal desde clone; LIVE usa UUIDv7; deterministic runs hash `(run_id,owner_key,ordinal)` | [E09] `v3/sdk/futures/operation/ids.go:71`; `v3/core/internal/futuresruntime/runtime.go:102`; `v3/core/internal/futuresruntime/ids.go:12,67`. No cambiar IDs durables existentes por nuevos hashes. |
| Orders / comandos | OrderID=ClientOrderID; engine crea orden de decisión MM, reserva/revalida y emite comando; provider/venue confirma | [E10] `v3/sdk/futures/domain/operation.go:63`; `v3/sdk/futures/operation/mm.go:348`; `v3/sdk/futures/operation/engine.go:2125,2330`. Role es descriptivo, seguridad por efecto ejecutable. MARKET/LIMIT/STOP_MARKET existen. |
| Fills | Venue es autoridad física; bridge normaliza; owner acepta correlación y dedup `(execution_account_id,provider_execution_id)` | [E11] `v3/sdk/futures/domain/operation.go:211`; `v3/sdk/futures/domain/execution.go:48`; `v3/sdk/futures/operation/engine_inputs.go:324`. Nunca hash precio/qty/hora como sustituto de ID nativo. Sin account/operation/order/contrato correcto sólo audit/quarantine, sin atribuir exposición. |
| MM y snapshots | MoneyManager puro devuelve decisiones/estado; Operation owner valida/aplica. Config y contrato se sellan al materializar; MMState mutable queda sólo en checkpoint | [E12] `v3/sdk/futures/operation/mm.go:378`; `v3/sdk/futures/operation/engine.go:1194,1864,2083`; `v3/sdk/futures/operation/runtime.go:15`. MMConfigSnapshot no demuestra presupuesto de ciclo. |
| Account economics | `accounting.Ledger` es inventario FIFO de cuenta/contrato; cuenta observa saldo/PnL/fees; sidecar post-causa llega al owner | [E13] `v3/sdk/futures/accounting/ledger.go:138,334,464`; `v3/sdk/futures/operation/engine.go:76`; `v3/sdk/futures/operation/evidence.go:167`. Delta de cuenta no equivale a resultado lógico por Operation. |
| StateFun | OwnerState completo checkpointed: una Operation no terminal, pending admission y deferred next OPEN; state+egress en handler | [E14] `v3/sdk/futures/operation/engine.go:34,62,116,123,150`; `v3/core/internal/functions/futures_operation.go:186,194,201`. Secuencia monotónica de owner continúa entre operaciones; caps hot-state no son retención histórica. |
| Operation facts | Operation owner emite `OPERATION_SNAPSHOT`, `ORDER_SNAPSHOT`, `FILL_FACT`, `PROVIDER_DECISION`, `DRAIN_REFUTATION`; envelope run/owner/seq | [E15] `v3/sdk/futures/operation/wire.go:40,67,98`; `v3/sdk/futures/operation/engine.go:848`; `v3/core/internal/functions/futures_operation.go:439`. Topic actual `echo.futures.operation-facts.v1`; snapshot excluye MMState. No movimientos monetarios ni QI_SEALED. |
| Proyección SQL | Projector escribe últimos snapshots, fills y decisiones; Kafka offset sólo después de apply | [E16] `v3/futures-projector/core/projector/projector.go:63,94`; `v3/futures-projector/adapters/pgstore/store.go:58,117`; `v3/futures-projector/adapters/kafka/runner.go:88,146`. Migration 066 PK operations=owner_key; run no aísla PK; fills DO NOTHING omite comparación de payload. No reconstruye MMState/verdad venue. |
| Master ReferenceEvent | EA Reference genera `trade_id` UUIDv7; bridge→`echo.reference-events.v1`, key trade_id; hecho de apertura física master | [E17] `v3/sdk/domain/reference_event.go:62,71`. Cuenta/ticket/precio/lote/magic, timestamps y riesgo opcional; no es Signal técnico ni Operation. |
| Copia Execution | Planner por policies genera CalculateRiskReq→MMEngine→CoreCommand por cuenta; EA execution/bridge devuelve éxito/fallo/precio/ticket | [E18] `v3/core/internal/functions/execution_planner.go:280`; `v3/sdk/domain/reference_event.go:460,548,577`. CoreCommand conserva trade_id y command_id propio; ReferenceTradeID opcional no garantiza correlación universal. No usar command_id como identidad del ciclo. |
| `trade_journal` | TradeJournalFn único writer del flujo; `(trade_id,account_id)` una fila account_role REFERENCE/EXECUTION; OPEN/CLOSED/FAILED | [E19] `v3/core/internal/functions/trade_journal.go:135,154,187,254,288`; `v3/sdk/domain/trade_journal.go:134`; `v3/sdk/postgres/trade_journal_repository.go:164,189`. SaveClose exige OPEN y compara facts; no fabrica filas. Fuente operacional para master, no ledger de fills. |
| Journal→LAB actual | Readers SELECT y adaptador V1; requiere estrategia UUID y marca VERSION_UNATTRIBUTED/BINDING_MISSING/NOT_A_DEAL_LEDGER | [E20] `v3/lab-worker/internal/repo/trade_journal_lab_repo.go:47,59`; `v3/sdk/analytics/adapter/journal.go:50,93,103`. Lectura CLOSED registrada, sin scoped binding/version universal. No prueba endpoint V2 ni integración runtime V4. |

Gaps concretos adicionales: [E16] switch del projector `:94–104` rechaza `DRAIN_REFUTATION` que el wire ya permite; `applyOrderSnapshot :180–205` no proyecta StopPrice; migration `v3/sdk/postgres/migrations/066_futures_projections.up.sql:107,320` guarda sólo último ciclo por owner y no MMState. Journal usa float64, Reference OPEN hardcodea moneda USD (`v3/sdk/domain/trade_journal.go:406`) y reader hace COALESCE USD ([E20] `:71`): no son evidencia monetaria. `risk_money` copia InitialRiskMoney (`trade_journal.go:357,373`), sin prueba CYCLE_BUDGET. `profit_net` se genera como gross+commission+swap (`v3/sdk/postgres/migrations/057_fix_trade_journal_profit_net.up.sql:22`); no volver a descontar costes. Gateway/SDK baseline tiene history V1; las rutas V2 de handoffs históricos no son CURRENT.

### 3. TARGET: identidad, scopes y unión explícita

Se reutilizan Strategy/StrategyVersion/recipes del registro compartido, ampliados por B; no se crea otro catálogo. Namespace lo resuelve auth/binding confiable, nunca un body del productor, símbolo, nombre o magic aislado. Identidad persistida de binding: `binding_ref` UUID, inmutable, con `(namespace,strategy_ref,strategy_version_ref,run_id,reference_account_id,reference_role,config_revision,config_digest,source_mode)`; `source_mode=EXTERNAL_REFERENCE|NATIVE_RUNTIME`. Conservar revisiones de binding vigentes `[valid_from,valid_to)` sin solapes para misma cuenta+magic+instancia terminal. Cambiar versión produce binding sucesor, no reinterpreta un ciclo abierto. MM/config/assignment epoch pinneados en apertura conservan sus refs hasta terminar.

Para datos nuevos el `run_id` se registra como identidad globalmente única dentro del namespace; jamás reutilizarlo tras cold reset sin continuidad. `run_mode=LIVE|BACKTEST|REPLAY`; `EXACT_REPLAY` del dominio actual se transporta como `REPLAY` junto a `source_run_mode=EXACT_REPLAY` y referencia del run reproducido. El modo no crea StrategyVersion nueva. `execution_mode=SIMULATED|LIVE` distingue la prueba simulada sin llamar LIVE real a una simulación. `reference_role=REFERENCE|EXECUTION|NATIVE` expresa el rol económico, coherente con History.role de C; `reference_basis=ACTUAL|THEORETICAL|UNKNOWN` conserva por separado el carácter de la referencia. Ambos son ortogonales a run_mode y execution_mode; no convertir REFERENCE en sinónimo de LIVE. Una cuenta pertenece a tenant por binding autorizado; broker es atributo del proveedor, no ID de cuenta.

Definir `H(tag,fields...) = wire.HashTagged(tag,fields...)`: SHA256 de los bytes UTF-8 del array JSON compacto `[tag,...fields]`, todos strings con escaping canónico y resultado `sha256:` + 64 hex lowercase. `D(tag,x)=wire.Digest(tag,x)=H(tag,string(Canonicalize(x)))`. Es la receta vigente en `v3/sdk/contracts/wire/hash.go:10–44`, compartida por B/C; no crear una codificación con longitudes ni concatenación con `:`. IDs nativos existentes conservan su receta propia.

| ID TARGET | Derivación / unicidad / regla |
|---|---|
| `reference_cycle_id` | `H("echo.execution.reference-cycle.v1",namespace,version_ref,run_mode,run_id,reference_account_id,source_family,opening_source_id)`. MASTER: opening_source_id=trade_id EA. TECHNICAL: SignalID del OPEN, no signal de cierre ni eval posterior. |
| `operation_ref` analítico | Runtime: `H("echo.execution.operation-ref.v1",namespace,run_mode,run_id,execution_account_id,runtime_operation_id)`; MASTER observado: mismo tag con source family JOURNAL y `(trade_id,account_id,account_role)` como campos separados. Es ref analítica del ciclo observado; no crea `domain.Operation`. |
| `runtime_operation_id` | ID nativo existente, nullable para master externo. El hash anterior lo scopea; nunca rellenarlo con trade_id/ticket para que parezca una entidad nativa. |
| `fill_ref` | H del scope `(namespace,run_mode,run_id,provider_instance_ref,execution_account_id,provider_execution_id)`. Preserva el ID físico y su dominio; session sólo si contrato del proveedor demuestra que sus IDs se reinician por sesión. Sin ID nativo, no existe Fill certificado. |
| `movement_id` | `H("echo.execution.movement.v1",operation_ref,source_event_ref,kind,allocation_index)`. Corrección usa mismo ID bajo nueva revisión de historia, no lo vuelve a sumar. |
| `fact_id` | `H("echo.execution.fact.v2",namespace,run_mode,run_id,owner_ref,owner_event_seq,effect_index,kind)`. Varias salidas del mismo Apply comparten seq, tienen effect_index distinto. |
| Scope físico StateFun nuevo | Dirección de función con `H("echo.execution.owner.v1",namespace,run_mode,run_id,account_id,account_strategy_id)`; envelope conserva IDs legibles. Signal strategy owner y fanout con scope equivalente. Rutas existentes sin tenant sólo para bindings legacy explícitos, nunca traducidos por fallback. |

El `operation_ref` de este envelope identifica el ciclo fuente en execution; al materializar History C se guarda como `correlation.source_operation_ref` y como `source_operation_id`. C calcula su `operation_ref` de representación bajo history_ref. Son scopes distintos explícitos, no dos hechos económicos ni dos motores; el crosswalk SAME_ECONOMIC_FACT permite seleccionar una sola representación.

**Crosswalk canónico** `execution.source_correlations`: clave `(namespace,run_mode,run_id,source_family,source_id,account_id,account_role)`→`reference_cycle_id,operation_ref,runtime_operation_id?,binding_ref,strategy_version_ref,evidence_ref,payload_digest`. Source family `MASTER_TRADE|TECHNICAL_SIGNAL|RUNTIME_OPERATION|JOURNAL_ROW|EXECUTION_COMMAND|VENUE_FILL`; los IDs de orden/fill pueden ser varios por ciclo. Sólo servicio de correlación Echo a partir de autoridad autenticada o efecto del owner agrega enlaces; replay idéntico converge y payload distinto devuelve `CORRELATION_CONFLICT`. Un vínculo operación→ciclo se fija antes de publicar economía y no cambia por la configuración actual.

El master externo crea su canonical cycle desde trade_id. La Operation técnica crea su ciclo desde opening SignalID; si su ejecución ya posee una referencia master, el enlace explícito se instala antes de la publicación y los alias usan ese mismo ciclo. No se presume igualdad entre ambas familias. Si dos refs ya publicadas reclaman después el mismo hecho físico, se registra conflicto y se excluye de agregaciones combinadas hasta corrección por nueva revisión; no se hace merge heurístico de identidades. Una fecha similar, mismo símbolo, magic o precio no autoriza unión. Sin correlación suficiente, conservar evidencia UNCORRELATED y coverage; jamás mostrar omisión como slippage cero.

### 4. APIs Go TARGET y envelope de hechos

Son contratos nuevos a implementar sobre este corte; nombres genéricos en `v3/sdk/execution`, no otro engine. Tipos de dinero/precio/cantidad reutilizan `sdk/futures/units` por alias de transición o traslado acotado sin cambiar matemática/serialización. Cualquier renombre mantiene contratos antiguos decodificables; no se mueve todo `sdk/futures` por búsqueda/reemplazo.

```go
type Scope struct {
    Namespace, RunID string
    RunMode string // LIVE | BACKTEST | REPLAY
}
type Correlation struct {
    StrategyRef, StrategyVersionRef, BindingRef string
    ReferenceCycleID, OperationRef string
    RuntimeOperationID *string
    AccountID, AccountStrategyID, AccountRole string
    OpeningSignalID, MasterTradeID, SourceFamily string
    OrderID, ProviderInstanceRef, ProviderExecutionID string
}
type Provenance struct {
    WriterRef, SourceEventRef, SourceDigest string
    ObservedAt, RecordedAt, AvailableAt time.Time
    EconomicAt time.Time
    ClockBasis, InstrumentSnapshotRef, MMConfigRef string
    CostModelRef, SourceRevisionRef string
}
type FactEnvelopeV2 struct {
    ContractVersion string // echo.execution.operation-facts.v2
    Scope Scope
    Correlation Correlation
    OwnerRef string
    OwnerEventSeq uint64
    EffectIndex uint32
    FactID, PayloadDigest, Kind string
    Provenance Provenance
    Payload json.RawMessage // exactly one allowed, validated typed payload
}
type CycleRiskSeal struct {
    Amount, Currency string // exact decimal >0
    RiskMethod string // CYCLE_BUDGET | FIRST_ENTRY_RISK | TICKET_INITIAL_RISK | DECLARED_UNACCREDITED
    MethodVersion, DecisionRef, PolicySnapshotRef string
    EvidenceRef, OpeningSourceID string
    SealedAt time.Time
}
type EconomicMovement struct {
    MovementID, OperationRef, Kind string // REALIZED_PNL | COMMISSION | FEE | SWAP
    AmountSigned, Currency string
    SourceEventRef, CostStatus, AttributionMethod string
    EconomicAt, AvailableAt time.Time
    OpeningFillRefs, ClosingFillRefs []string
}
type FactApplyResult struct { State string; FactID, HeadDigest string; Revision uint64 }
type CorrelationService interface {
    ResolveAndSeal(context.Context, SourceIdentity, BindingEvidence) (Correlation, error)
}
type RuntimeHistoryConsumer interface {
    ApplyFact(context.Context, TrustedWriter, FactEnvelopeV2) (FactApplyResult, error)
}
type JournalObservationService interface {
    Accept(context.Context, TrustedWriter, MasterObservation) (JournalReceipt, error)
}
```

`SourceIdentity={Scope,SourceFamily,SourceID,AccountID,AccountRole,PayloadDigest}`. `BindingEvidence={BindingRef,Revision,Digest,SourceEventAt,SourceInstanceRef}`; Resolve exige match temporal único, tenant/account autorizados y digest/revisión aplicada. `TrustedWriter` viene de autenticación o inyección del runtime, no JSON. `MasterObservation={SourceIdentity,BindingEvidence,EnvelopeType,Payload,ObservedAt,AvailableAt}` conserva original canónico; `JournalReceipt={ObservationID,JournalID?,SourceRevision,State,DispatchState,QualityReasons[]}`. `JournalObservationService` encamina al writer journal vigente, no escribe una segunda copia desde LAB. `RuntimeHistoryConsumer` usa el mismo servicio de aplicación de historia V2 de B/C in-process; no HTTP hacia sí mismo, parsing de SQX ni SQL directo de Forge.

Kinds admitidos: los snapshots y FILL_FACT/PROVIDER_DECISION/DRAIN_REFUTATION actuales más `CYCLE_LINKED`, `QI_SEALED`, `ECONOMIC_MOVEMENT`, `OPERATION_TERMINATED` y `JOURNAL_OBSERVED`. FILL_FACT preserva dato físico inmutable; ECONOMIC_MOVEMENT es resultado atribuible, no otro fill. Deny anterior a materialización admite `OperationRef` vacío y usa request/decision_ref; no inventa Operation. `PayloadDigest` se calcula sobre JSON canónico tipado (strings decimales normalizadas, objetos ordenados, sin floats); envelope valida shape, writer por familia y exactitud de todos los scopes. Ningún sender puede emitir `QI_SEALED` por ser sólo escritor de historia externa.

Topic TARGET `echo.execution.operation-facts.v2`, partición `Scope+OwnerRef`; wire V1 permanece congelado para consumers existentes hasta corte explícito. Sólo un topic alimenta una historia por binding/epoch: registro de cutover `{binding_ref,first_v2_owner_seq,last_v1_owner_seq}` impide sumar replay V1+V2. Adapter V1 sólo puede preservar evidencia limitada; nunca produce Q_i/costes inexistentes. Exportar instrument snapshot, MM config snapshot/digest, pinned binding/assignment generation/epoch y run context; MMState no viaja al read model y conserva checkpoint como autoridad.

### 5. Flujos operacionales y puente journal

**EXTERNAL_REFERENCE / OBSERVE_MASTER.** Ingestión V2 acepta Strategy/Version/historias y outbox operacional según B; profile Echo autorizado declara cuenta referencia, mapping `magic+source_instance+account`, símbolos/contratos, policies/MM y run simulado. El registry de la strategy debe usar el mismo ID consumido por `strategy_definitions`/ExecutionPolicy. Nueva revisión de binding sigue provisión→ACKs→READY, independientemente del worker LAB. No se exige registrar módulo s1/s2 ni materializar Operation nativa para una EA externa.

Al llegar ReferenceEvent se autentica origen/cuenta/instancia, resuelve binding temporal y sella correlación. Guardar observación original y resolver journal con TradeJournalFn. READY abre el gate de dispatch hacia planner/MM/cuentas permitidas; un OPEN antes de READY se conserva y journaliza cuando exista el binding, con `NOT_DISPATCHED_PRE_READY`, y no se reabre después para enviar órdenes. Los OPEN nuevos post-ready aplican caducidad configurada y estado actual de la referencia; CLOSE/MODIFY de ciclos existentes mantienen su ruta de gestión y seguridad aunque readiness de nuevas entradas se degrade. Receipt accepted no permite saltar ese gate. Si LAB cae, journal y gestión siguen; sólo aumenta backlog analítico.

**NATIVE_RUNTIME.** Reusar `StrategyEngineFn`, `SignalFanoutFn`, `OperationFn`, provider y bridge actuales; pintear binding/version/run en owner-local correlation sidecar al aceptar OPEN y copiarla a cada efecto. Ningún DTO fuerza a Strategy a depender de cuentas/MM: Signal conserva intención técnica; resolver version desde la instancia de Strategy sellada. No añadir transformador master→Signal para duplicar la decisión. El config snapshot actual se carga una vez desde ETCD `futures/enabled` y `futures/config_snapshot` al registrar (`v3/core/cmd/echo-core/main.go:545–573`); ACK de binding nativo exige aplicar revisión al owner real mediante el ACK del snapshot realmente cargado al startup definido en B; si difiere, BLOCKED_RUNTIME_RESTART_REQUIRED y sólo arranque propio del harness. No introducir hot reload ni afirmar que cambiar PG lo aplicó.

**Journal para runtime nativo.** TradeJournalFn recibe una proyección tipada de hechos confirmados con source lineage; no recibe una ReferenceEvent inventada por cada Signal. Introducir `JournalRuntimeFact` dentro del servicio journal, con canonical scope y enlaces nativos, para preservar una vista operacional de esos hechos sin hacer del viejo grano ticket un aggregate nuevo. No forzar qty entera futures a lot_size Forex, no fabricar ticket y no sumar journal a los movements de la misma Operation. El canonical journal source puede almacenar esos enlaces en `execution.journal_links` y una vista read-only de facts por Operation; la tabla ticket `trade_journal` sólo recibe filas cuando el evento satisface su contrato de apertura/cierre físico. Una Operation multientrada no se aplana como un ticket ficticio. Para I1 Forge la prueba obligatoria atraviesa el journal master existente; extender la vista de journal nativo acompaña hechos nuevos, no migra estrategias antiguas.

**Bridge journal→historia.** En la misma transacción de SaveOpen/SaveClose efectivo crear/actualizar correlación y outbox `JOURNAL_OBSERVED`, con `journal_revision` monotónico por `(trade_id,account_id)`; replay sin delta conserva revisión/outbox. Writer de journal sigue siendo autoridad, outbox no decide trading. Cerrar sin OPEN pasa a pending durable por mismo scope+trade/account, no inserta apertura sintética: cuando llega OPEN se drena en orden causal mediante el mismo writer; timeout deja MISSING_OPEN con alarma/coverage. Antes de esos cambios, CURRENT sólo quarantinea/rechaza y no se presume drenaje automático. Corrección autorizada del journal genera revisión nueva, preserva original y emite delta de observación; LAB publica snapshot completo N+1 sin duplicar importes.

El adapter selecciona `ECONOMIC_MOVEMENTS` sólo cuando existen hechos completos con IDs/economía acreditados; de una fila de cierre journal genera `CLOSED_SUMMARY` neto una vez al cierre. OPEN/FAILED no generan resultados cerrados ni fills. Si un cycle tiene movements y también fila journal, fuente activa económica `RUNTIME_MOVEMENTS` o `JOURNAL_SUMMARY` fijada por lineage/cutover; la otra sirve para conciliación. Copias EXECUTION conservan account+broker+role y no se suman a historia REFERENCE. Cuentas distintas de un mismo broker jamás colapsan.

### 6. Q_i, economía por operación y costes

**Sello causal.** Extensión aditiva `MMDecision.CycleRisk *CycleRiskSeal` y `DecisionRef` único para la decisión; `OrderRequests[].DecisionID` existentes se preservan. En `invokeMM :1873` se obtiene la decisión; `applyMMDecision :2083` valida y sella QI antes del primer comando/Fill, dentro del mismo Apply transaccional. Sidecar owner `OpeningRiskSeal` queda inmutable; emitir QI_SEALED en efecto propio con effect_index. Si Apply falla, sello/ordinals/effects se abandonan juntos. Primer Fill antes de sello impide acreditarlo retroactivamente; historia monetaria sigue válida y R queda INSUFFICIENT_DATA. `opened_at` económico se fija al primer Fill aceptado; `materialized_at` y `risk_sealed_at` son tiempos distintos, con `risk_sealed_at<=opened_at`. Un ciclo sin ejecución no fabrica fecha de fill.

**Gerard actual no certifica Q_i.** `computeEconomics :98–128` deriva owner remaining y effectiveBudget; `entry :220–280` usa el presupuesto para cantidad pero no lo transporta; adds recalculan presupuesto `:786`. TARGET añade emisión observacional del valor que esa decisión real elige, método `gerardmm.cycle-opening-budget.v1`, con snapshot de plan, AccountEconomics revision consumida, EntryBudgetPolicy, stop/qty inicial y evidencia de que el presupuesto es del ciclo completo bajo la política sellada (incluye adds/reentradas). No deducir esa semántica sólo desde el nombre effectiveBudget ni etiquetar toda instalación Gerard por defecto. Implementación registra método allowlisted y prueba multi-entrada contra ese contrato; sin acreditación queda FIRST_ENTRY_RISK o DECLARED_UNACCREDITED. No cambia presupuesto/órdenes para conseguir disponibilidad analítica. Los adds pueden mostrar consumo/cambio/breach posterior; nunca recalculan el Q_i original. Para external master, ticket InitialRiskMoney queda TICKET_INITIAL_RISK salvo certificado explícito de política/ciclo desde autoridad source. Config actual, SL final y pérdida observada no son pruebas de apertura.

**Atribución lógica.** Mantener `accounting.Ledger` FIFO físico de cuenta/contrato para account economics. Extraer su aritmética exacta de consumo de inventario/valorización como reducer puro compartido, sin copiar fórmulas ni añadir trading engine. Operation owner usa inventario por `(namespace,run,operation_ref,contract_snapshot)` y sólo fills que ya pasaron correlación/dedup del engine. Reducción cierra inventario de ESA Operation, FIFO dentro de ella; entrada/add agrega lote. Aplicar una vez tras validación del fill y antes de publicar efectos/MM. `REALIZED_PNL = side_sign * matched_qty * (close_price-entry_price) * point_value`, bajo precisión del instrumento. No usar diferencia de Revision global para calcular resultado de operación. Nueva superficie `sdk/execution/accounting.OperationEconomicsState` serializable del mismo reducer contiene lots, movement identities y totales; checkpoint del owner, no un worker que reejecute MM. Exact oracle: A compra1@100, B compra1@110, B vende1@115 ⇒ B gross5; account FIFO reconoce15 y deja inventario abierto distinto. Conciliación expone diferencia temporal con inventario restante, no fuerza igualdad de realized con operaciones abiertas.

**Costes.** Fill vigente no tiene fee/commission/swap. Añadir evidencia `ExecutionCost{cost_id,kind,amount_signed,currency,source_event_ref,provider_instance_ref,account_id,order_id?,provider_execution_id?,economic_at,available_at,cost_model_ref?,allocation_method}` normalizada por bridge o autoridad account; pasar a owner por input tipado y emitir ECONOMIC_MOVEMENT dentro del mismo Apply. Modelo simulado lleva versión y términos sellados; coste de broker sólo cuando observado. Si un coste de cuenta cubre varias operaciones, writer económico emite allocations explícitas y demuestra Σallocations=cost original; sin método no lo distribuye heurísticamente. Coste conocido cero requiere evidencia `cost_status=KNOWN_ZERO`; ausente=`UNKNOWN`, no “0”. Corregir convención charged_costs positiva del Ledger a amounts signed negativos en una única adaptación, con source refs; rebates positivos. OPEN puede tener costes/realizaciones ya conocidos, publicados antes de terminalidad. No mezclar net realization con sus comisiones duplicadas.

**Terminalidad y conciliación.** Operation continúa con guards actuales: intent de cierre no implica flat físico; terminar exige convergencia y ausencia de órdenes ejecutables. `OPERATION_TERMINATED` incluye `gross,costs,net,currency,economic_complete,source_frontier,movement_digest`; net=Σsigned movements exactamente cuando el grano es movements y todas monedas son compatibles. Snapshot terminal es resumen reconciliable, no otro ingreso. Net no certificado si faltan costes; recorded gross puede mostrarse con calidad explícita, los perfiles net/R/10k no se certifican como completos. Los datos existentes con USD por default permanecen moneda no acreditada hasta evidencia real; sidecar `currency_evidence_ref` del binding/EA/account snapshot auténtico resuelve nuevos eventos, no cast del literal. Floats legacy se convierten sin inventar precisión, con política documentada de redondeo y escala origen; V2 usa decimal string.

### 7. Orden, idempotencia, recuperación y proyección

| Condición | Acción TARGET |
|---|---|
| FactID repetido / digest igual | ACK DUPLICATE, cero cambio/head/job; devuelve receipt previo antes de CAS sobre un head posterior. |
| FactID o native Fill identity repetido / payload distinto | `FACT_CONFLICT` durable con referencias y fail-visible; no DO NOTHING silencioso. No se avanza el frontier del hecho conflictivo. |
| Snapshot viejo | Historial fuente preservado; último snapshot sólo avanza por seq mayor del mismo `(scope,operation_ref,entity_ref)`. Igual seq y contenido distinto es conflicto. |
| Movement tardío válido | Insertar por MovementID aunque haya snapshot con seq mayor; no usar max-seq global para descartar deltas. Actualizar historia a N+1 y invalidar derivados. |
| Secuencia recibida con huecos | Persistir facts idempotentes, medir holes; source_frontier sólo contiguo con marker de batch/effect_count por Apply. Terminal con frontier incompleto queda PENDING_SOURCE_GAP, no “completo”. |
| Fill de operación vieja/terminal | Preservar original y POST_TERMINAL_EXECUTION_BREACH / DRAIN_REFUTATION; no atribuirlo a sucesora ni reabrir trading automáticamente. Corrección económica usa nueva revisión validada desde autoridad. |
| Evento sin binding/version probado | Observación durable UNCORRELATED y quarantine con razón; no latest-version fallback. Resolver por fuente temporal exacta produce N+1, nunca edita revisión usada por ranking. |
| Error transitorio DB/Kafka | Retry con backoff acotado y mismo ID; offsets sólo tras commit de facts/projection+outbox. Timeout incierto: consultar receipt/estado durable antes de repetir efecto. |
| Poison o contrato inválido | Quarantine durable con hash/original protegido; marcar offset sólo tras quarantine confirmada. Alerta y coverage excluido; sin bucle infinito ni éxito silencioso. |

TARGET conserva retención por operación en `execution.operations` PK `(namespace,run_mode,run_id,account_id,operation_id)`, `execution.orders` con scope+order_id, `execution.fills` con scope físico completo, `execution.economic_movements` con scope+operation_ref+movement_id y `execution.fact_receipts` con FactID/digest/frontier. Índice/vista `current_operation_by_owner` conserva consulta actual sin sobrescribir ciclos cerrados. FKs/deferred staging permiten fill antes de snapshot sin inventar padre: pending correlation se drena al recibir evento padre. Projector implementa cada kind V2 incluyendo DRAIN_REFUTATION y StopPrice; orden STOP_MARKET/stop_price se valida en nueva migración, no se modifica 066 aplicada.

Projector tiene una transacción por fact/batch: receipt/inbox→projection→outbox de history dirty→commit, después offset. LAB adapter drena outbox con leases/fencing y usa servicio común C; jamás llama al motor ni MM. Si publica historia y cae antes de marcar outbox, replay consulta FactID/receipt y no duplica movimientos; guardar head acumulado del ciclo/historia, nunca PUT de sólo el último ciclo que borre anteriores. Cada revisión de C es snapshot completo e inmutable; no segunda cadena de correcciones de movements.

Recovery operacional nativo usa savepoint/checkpoint `OwnerState+OperationRuntime+MMState+pending+dedup+assignment epoch+ID cursors` y sus mecanismos de continuidad actuales. SQL/latest history sólo recupera consulta, no engine ni posiciones. Rebuild analítico usa retained facts/artifacts+version del reducer+bindings+source revisions; no inventa ciclos perdidos desde último snapshot. Retención durable sin GC automático concurrente de I1, write-ahead de artefactos y revisiones fijadas según C. Para cold state incompatible bloquear nuevas entradas y exigir evidencia de continuidad/reconciliación con venue; no declarar READY por conexión TCP o snapshot SQL. D24 excluye una migración de estrategias/backtester para resolver esto.

### 8. Superficies exactas y secuencia mínima de implementación

| Orden / superficie CURRENT | Delta TARGET / ownership |
|---|---|
| 1. `sdk/contracts`, `sdk/postgres/strategy_{identity,version}_repository.go`, Gateway handlers, registro StrategyDefinition | B conserva recipes e identidad; binding/version/run/provisioning/outbox, plataforma/semántica exactas. No nueva tabla de estrategias paralela. |
| 2. `sdk/execution/{contracts,correlation,accounting}` nuevos | Contratos puros anteriores y reducer económico compartido; lógica infraestructura en módulos dueños. Nuevos nombres genéricos; alias de transición acotado de tipos ya usados. |
| 3. `sdk/futures/strategy`, `domain/fanout.go`, `operation/{engine.go,engine_inputs.go,mm.go,runtime.go,wire.go}` | Sidecar sellado scope/version/ciclo/binding; QI en decisión real; inventario atribuible y costes; facts V2, ordinal efecto/batch frontier; sin segunda evaluación ni cambio de estrategia. |
| 4. `sdk/futures/gerardmm`, `strategies/tgmm`, `accounting/ledger.go` | Publicar presupuesto sólo con método acreditado; extraer reducer puro existente para uso account y operation; no asumir que todos MMs soportan CycleRisk. |
| 5. `core/internal/functions/{futures_operation,trade_journal,execution_planner}.go`, `core/internal/futuresruntime`, `core/cmd/echo-core/main.go` | Persist+emit atómico, binding controls/ACK, safety management, gate dispatch READY; journal observation inbox/outbox/crosswalk y source revision. External no exige composición nativa. |
| 6. `bridge/internal/pipe_handler.go`, `sdk/domain/{reference_event,trade_close,trade_journal}.go`, `sdk/postgres/trade_journal*` | Propagar enlaces/currency/time/cost provenance de fuente y versión; respetar EA trade_id y contrato ticket. JournalRuntimeFact no fuerza representación Forex; fuente legacy preservada. |
| 7. `futures-projector/{core/projector,adapters/pgstore,adapters/kafka}`, `sdk/statefun`, module YAML DEV/PROD en repo | Decoder V2, transaction inbox/projections/outbox, kinds faltantes/StopPrice y commit-after-apply. Preparar configuración; aplicarla a servicio compartido es gate externo, no este diseño. |
| 8. Nueva migración después del max existente; metadata Hasura read-only | Tablas scope/key/retención/receipts/links y views role-filtered; no editar migraciones aplicadas, no borrar journals/facts ni event triggers compartidos. PostgreSQL sigue proyección. |
| 9. `sdk/analytics/adapter/journal.go`, `lab-worker/internal/repo/trade_journal_lab_repo.go`, consumidor runtime nuevo | Adapter explícito a historia V2 con refs de C; retirar consumo V1 sólo tras inventario y corte probado. Sin USD fallback ni suposición StrategyID UUID=versión; sumar por fuente seleccionada. |

Preparar cutover por writer/binding: inventario consumidores actuales→crear schema/contratos nuevos→replay fuente retenida en namespace aislado→conciliar→cambiar binding V2 en frontera explícita→validar→retirar sólo consumidores exclusivos anteriores. No dual-write económico permanente; rollback revierte routing a frontera conocida y preserva originales. No renombrar topics/direcciones StateFun activas sin mapa de savepoints y consumers; el naming genérico TARGET no autoriza perder estado. Sin modificación del backtester ni interfaz nueva de campañas/selección dinámica.

### 9. Aceptación exigida en Shot 2–4

Pruebas aquí especificadas, **NOT_RUN** en Shot 1. Su nombre describe caso futuro, no tests existentes ni PASS heredado.

1. Ingest auténtico Forge→receipt Strategy/Version→provisión profile aislado→ACKs aplicados→READY antes de emitir master simulado a t≈60s; demostrar journal OPEN/CLOSED con binding/version/run exactos aunque worker LAB esté detenido; al retomarlo, una única historia y sin pérdida/doble conteo. Si artefacto auténtico o ambiente no está autorizado, gate BLOCKED_EXTERNAL; protocolo fixture no equivale a Forge E2E.
2. `INGEST_ACCEPTED` con ACK faltante/de revisión vieja/reinicio consumer no permite dispatch OPEN; observación queda durable/journalizada NOT_DISPATCHED_PRE_READY. READY posterior no ejecuta OPEN viejo; CLOSE/MODIFY de ciclo vivo sigue gestionándose.
3. EXTERNAL_REFERENCE no crea domain.Signal ni Operation nativa; NATIVE_RUNTIME atraviesa Strategy/Signal/Fanout/Operation reales del corte y conserva su identidad; mismo version_ref en runs diferentes y tenants/cuentas homónimas sin colisiones.
4. Crosswalk master trade_id distinto de SignalID y OperationID une sólo por evidencia exacta. Broker igual/cuentas distintas, magic reutilizado en otra instancia, versión rotada con ciclo abierto, correlación ambigua: nunca latest-version fallback, merge heurístico ni suma de copias a referencia.
5. Aplicar dos veces mismo fact/fill/cost/source revision tras crash antes de offset reproduce IDs, heads e importes; mismo ID/digest distinto produce conflicto observable. Lotes con seq compartida y effect_index distintos no pierden movimientos.
6. Operation A/B del freeze: A1@100/B1@110/cierraB@115 ⇒ grossB5 frente account FIFO15; parciales, adds y multimoneda se atribuyen a Operation propia y conciliación explica timing. Probar sin importar nada de rama legacy.
7. Q_i primera entrada distinto de presupuesto completo, sello anterior al primer fill e inmutable tras adds/MM changes. CYCLE_BUDGET requiere método/policy/decision/revision; InitialRisk ticket o config no habilitan R. Apply fallido abandona sello y efectos juntos.
8. Parciales dan +0.4R antes del cierre con Q_i probado; costes de entrada/salida/swap/rebate aparecen al reconocerse. Unknown costs/currency no se vuelven cero/USD; net resumido journal no duplica comisión/swap como movements.
9. CLOSED_SUMMARY sin Fill legítimo; movements completos más resumen terminal sólo una economía. Fill tardío, close antes de open, snapshot antes/después de movimientos y DRAIN_REFUTATION preservan evidencia y no afectan sucesora ni terminalizan falsamente.
10. Rebuild desde facts/artifact retained devuelve mismos heads/economía; último snapshot SQL insuficiente bloquea recovery operacional. Reinicio/savepoint conserva MMState/ID cursors/dedup/assignment fences; sin continuidad no READY.
11. Historial de varias operaciones y runs retenido; seq vieja no hace retroceder snapshot y no elimina movimiento nuevo por tener timestamp antiguo. Hist N reproducible tras N+1, replay outbox no reemplaza set acumulado por última operación.
12. Comparación I1 muestra por referencia/copia cobertura de oportunidades esperadas/omitidas/fallidas/no correlacionadas, VWAP comparable y slippage adverso buy=`execution-reference`, sell inverso, coste/latencia separados y reloj acreditado. Quantity/MM distinto no se etiqueta slippage ni omisión cero. Portfolio estático D11 sigue requerido en C; ninguna de estas interfaces implementa I2.

Pruebas críticas de auth/tenant/source_writer/read-only Hasura son obligatorias en el gate de implementación/auditoría según B/C; si el harness las impide deben quedar NOT_RUN/BLOCKED, sin recategorizar evidencia estática como PASS. Gate de coverage ≥95% del código nuevo cubre primero los caminos críticos anteriores. La certificación física de broker/cuentas/PROD permanece fuera del permiso de Shot 1; no se tocó flota activa, servicios compartidos, campañas ni dinero real.

## Fuentes

- [[F — Decision Register]] — autoridad D09/D10/D11/D16–D24 y precedencia de la rama runtime.
- [[THE_LAB_V4_Diseno_para_revision]] y [[1 — TECHNICAL_FREEZE_PACKET]] — requisitos I1 compatibles; los paths históricos de integración/backtester no son baseline vigente.
- [[0 — Submanager State]] y [[SHOT4_HANDOFF]] — continuidad histórica, sin heredar certificados de ramas anteriores.
- [[Echo — Producto Integrado]] y [[Echo + Echo Forge — Environment Contract]] — producto/ambiente y separación entre diseño, permisos y prueba física.
- Evidencia CURRENT [E01]–[E20]: `xKoRx/echo@2ee61791deb3139be23e1c9be3708b1d41da8d6b`, archivos y líneas declarados en §2; comprobación de SHA/árbol limpio repetida al terminar la lectura.
