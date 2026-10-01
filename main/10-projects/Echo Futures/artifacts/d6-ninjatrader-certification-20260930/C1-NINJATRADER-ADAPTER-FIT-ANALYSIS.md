# Echo Futures — D6 C1 NinjaTrader / NinjaScript Adapter Fit Analysis

**Shot:** D6 C1 — Adapter fit analysis (source + physical + official docs; no implementation, no orders)
**Role:** TOP Execution Integration Architect / Source Forensics Specialist
**Date:** 2026-09-30
**Project:** [[Echo Futures]]
**Echo frozen baseline:** `xKoRx/echo@13e087a3bb762f65b060d3b3200fb00a67c6ff1d` (`feature/d5-shot3-remediation`, verificada localmente == HEAD del branch)
**D6 program:** GAU50 (5 evaluaciones + 5 resets, 1 cuenta activa Echo a la vez)
**Transport target:** `NINJATRADER_TRADOVATE` — NinjaTrader Desktop 8.1.8.3 (dev-win 192.168.31.132, build 26100.5074) sobre credenciales Tradovate de Earn2Trade
**Prior artifacts:** C0 (`./C0-NINJATRADER-PHYSICAL-TRANSPORT-CERTIFICATION.md` — transporte físico PASS, observables GUI BLOCKED/pendiente owner); Earn2Trade preflight (entitlement/policy NO reabiertos)
**Verdict:** `D6_C1_ADAPTER_FIT = PASS` — el seam congelado D2-07/D5 es reutilizable tal cual para NinjaTrader Desktop: el contrato `ExecutionAdapter` implementa 1:1 contra la API NinjaScript real (`Account`, `Order`, `Execution`, `Position`, `AddOnBase`), el modelo de eventos normalizados mapea nativo, y no existe contradicción material con D5. La superficie mínima dentro de NT es un **AddOn** (`NinjaTrader.NinjaScript.AddOnBase`, presente y verificable por reflexión en el binario 8.1.8.3); el journal M2 y todo el estado durable permanecen en el Futures Bridge (congelado). El único trabajo material nuevo es wiring D6: (1) componente desktop AddOn, (2) endpoint bridge↔AddOn, (3) productor del stream de mercado (D5 no tiene ningún productor real), (4) ruta de publicación del corpus de warm-up REBUILD (D5 sólo tiene los tipos + pinning en manifest, sin ejecución), y (5) certificación M2 específica de Tradovate/NinjaTrader.

## 0. Hard safety y alcance

No se envió, modificó ni canceló orden alguna (`ORDERS_SENT = 0`). No se instaló NinjaScript, no se cambió ACL ni identidad en dev-win (mandato /execute.G: sin cambios de identidad en este shot), no se tocó product code D5. Inspección NT = reflexión read-only sobre los assemblies instalados (`NinjaTrader.Core.dll` 8.1.8.3 vía `[Reflection.Assembly]::LoadFrom` por `aranea-ssh` perfil `dev-win-operator`) + documentación oficial NinjaTrader. Inspección Echo = source read-only en el clone de trabajo `~/aranea/work/d5-foundations-20260929/echo` @ 13e087a3. Las referencias Echo usan forma `xKoRx/echo@13e087a3:<repo-relative-path>`.

## 1. Convención de evidencia

Cada claim se clasifica: **FACT** (observado en source/binario local, o quote directo de doc oficial), **SUPPORTED_INTERPRETATION** (inferencia declarada sobre FACT), **UNKNOWN** (no demostrado; va a gate D6 si es material). Fuente NT oficial = `static.ninjatrader.com/support/helpGuides/nt8/*` y `developer.ninjatrader.com/docs/desktop/*` (URLs por claim). Evidencia física NT = reflexión sobre `C:\Program Files\NinjaTrader 8\bin\NinjaTrader.Core.dll` (FileVersion 8.1.8.3, re-verificada hoy; C0 E1/E2 la certificó por recurso de versión).

---

## A. Account identity / selection

**Representación de las 5 GAU50.** FACT: NinjaTrader expone las cuentas de la conexión activa como objetos `NinjaTrader.Cbi.Account` en la colección estática `Account.All` (reflexión: propiedad estática `All` : `Collection<NinjaTrader.Cbi.Account>`). Cada `Account` expone `Id` (**System.Int64**), `Name`, `DisplayName`, `Denomination`, `Connection`, `ConnectionStatus`, `AccountStatus`, y colecciones observables `Orders` / `Executions` / `Positions` / `ExecutionPositions`. El login Tradovate de Earn2Trade materializa las 5 evaluaciones GAU50 en esa colección (C0 + observación owner registrada en project note: "One Earn2Trade/Tradovate login exposes all 5 purchased GAU50 Evaluation accounts").

**Identificador estable.** FACT: `Account.Id` es Int64 (reflexión) — el id numérico Tradovate encaja naturalmente. `Account.Name` es la identidad string visible en GUI. Regla de identidad del adapter: resolver la cuenta autorizada **por Id (y cross-check Name)** desde `Account.All`, no por posición en la colección ni por la selección de GUI. UNKNOWN (gate D6): estabilidad del `Account.Id` de una cuenta GAU50 a través de restart de NT y reprovision de la evaluación — observable barato de certificar.

**Selección programática.** FACT: toda la superficie de órdenes es por objeto explícito: `Account.CreateOrder(...)` / `Account.Submit` / `Account.Change` / `Account.Cancel` / `CancelAllOrders` / `CancelOrdersByOcoID` / `Flatten` / `FindOrderById` (métodos reflejados). No existe ningún parámetro "cuenta seleccionada en GUI" en esa superficie; el account selector del Control Center es UI de entrada manual. SUPPORTED_INTERPRETATION: la selección GUI es irrelevante para órdenes programáticas — el AddOn referencia explícitamente el objeto `Account` resuelto. Esto satisface la owner policy "account selection debe ser autoridad explícita del runtime": la autoridad es la config del binding Echo (ETCD `futures-bridge/accounts/{id}/*`, `provider-external-account-id`), y el adapter la verifica bind-time.

**Garantía de una sola cuenta autorizada.** REUSE_AS_IS: el bridge ya resuelve identidad por cuenta con defence-in-depth — el payload del comando debe matchear la cuenta de la sesión (`xKoRx/echo@13e087a3:v3/futures-bridge/internal/session/session.go:300-306`), el pin de binding por orden (session.go:326-331), y el journal carry `ProviderExternalAccountID`/`ExternalContractIdentifier` (`v3/futures-bridge/core/capabilities/journal.go:54-55`). El adapter NT añade una verificación propia: después de Connect, `Account.All` debe contener exactamente la cuenta configurada (Id+Name); mismatch ⇒ binding no verificado ⇒ readiness `PROVIDER_ACCOUNT_BINDING_NOT_VERIFIED` (el readiness conjunction de `v3/futures-bridge/core/capabilities/readiness.go:31-66` ya falla cerrado). MULTIPLE accounts nunca reciben egress porque el topic es per-account y la sesión per-account: `echo.order-commands.{execution_account_id}.v1` consumido con validación de identidad (`v3/futures-bridge/adapters/kafka/command_consumer.go:79` + session.go:300-306). Las otras 4 GAU50 visibles en NT no reciben comandos (no hay sesión Echo para ellas).

**Cuenta que desaparece / reconecta / se reprovisiona.** FACT: `NinjaTrader.Cbi.Connection` expone evento `ConnectionStatusUpdate` + métodos `Connect`/`Disconnect` y colección estática `Connections` (reflexión). FACT: existe el evento `Account.AccountRoll` + `AccountStatus`/`AccountStatusUpdate`/`AccountLiquidationChanged` en el binario (reflexión) — NT modela reemplazo/estado de objetos Account; docs públicas no describen `AccountRoll` (buscado; sin resultados en help guides) ⇒ **SUPPORTED_INTERPRETATION**: el patrón documentado/comunitario y consistente con la API es re-resolver `Account.All` tras cada transición de `ConnectionStatusUpdate` a Connected y re-subscribir eventos (fuente: [Account Class – NinjaScript](https://ninjatrader.com/support/helpguides/nt8/account_class.htm), [ConnectionStatusUpdate](https://ninjatrader.com/support/helpguides/nt8/connectionstatusupdate.htm), [OnConnectionStatusUpdate](https://developer.ninjatrader.com/docs/desktop/onconnectionstatusupdate)). Regla adapter: tras cada (re)connect, re-resolver por Id+Name configurados; no encontrado o ambiguo (duplicado) ⇒ fail-closed `DISCONNECTED/RECONCILING` + barrier; ningún submit contra una referencia stale. clasificación: SMALL_D6_ADAPTER_WORK (la barrier genérica ya está congelada e implementada en `session.RunRecoveryBarrier`, session.go:148-243; falta el provider-side NT).

---

## B. Market data

**Realtime NQ.** FACT: `Instrument.MarketData` expone evento `Update` con `NinjaTrader.Data.MarketDataEventArgs{Ask, Bid, Last, Price, Volume, Time, MarketDataType, Instrument, IsReset}` y `MarketDataType{Ask, Bid, Last, DailyHigh, DailyLow, DailyVolume, ...}` (reflexión). Cubre Bid/Ask (BBO) y Last (trades) tick-a-tick con timestamp. `Instrument` expone además `MarketDepth` y `HistoricalData` (reflexión). Identidad del instrumento: `Instrument.FullName` (formato "NQ 12-26"), `Id`, `Expiry`, `MasterInstrument` — el `external_contract_identifier` del binding Echo (config ETCD por cuenta, `main.go:218-220`) mapea 1:1 a `FullName`; resolución del objeto `Instrument` es API estándar NinjaScript. El mapping canónico `NQ → NQZ6` (config hot owner) es REUSE_AS_IS de D2-05: el hot mapping vive en Echo, no en NT.

**Subscripciones.** SUPPORTED_INTERPRETATION (por forma de API + doc [BarsRequest](https://static.ninjatrader.com/support/helpGuides/nt8/barsrequest.htm)): un AddOn subscriba `instrument.MarketData.Update += handler` (realtime BBO/trades) y administre alta/baja según demanda de stream (`Operation ACQUIRE|RELEASE` ya modelado en D2-06; el demand plumbing `bars/demands.go` existe). `IsReset` señala reset de serie ⇒ tratar como barrier de continuidad, no como dato.

**Histórico y granularidades.** FACT: `NinjaTrader.Data.BarsPeriodType` = {Tick, Volume, Range, Second, Minute, Day, Week, Month, Year, ...} (reflexión). FACT: `BarsRequest` es la clase AddOn-documented para pedir histórico y subscribir realtime bars: constructores por `barsBack` o rango `fromLocal/toLocal` (fechas locales, días completos), con handler `Update` y `Request()` ([BarsRequest – NinjaScript](https://static.ninjatrader.com/support/helpGuides/nt8/barsrequest.htm)). UNKNOWN (gate D6): profundidad real de histórico tick de la conexión Tradovate demo (los proveedores limitan tick history; minute/day es profundo). FACT débil: la caché local `db\NinjaTrader.sqlite` contiene metadata de instrumentos NQ/ES (C0 E8).

**Warm-up S2 (H4 SMA50 + 5m Bollinger 20/2) — FACT del requisito:** S2 declara `BarClose NQ [4h, 5m]` con lookback 64 ("warm-up 51 H4 + 20 5m + headroom") y `MarketEventClass: NONE` (`xKoRx/echo@13e087a3:v3/sdk/futures/strategies/s2/s2.go:36-56,133-141`; `v3/sdk/futures/strategy/requirements.go`). 51 barras H4 ≈ ~17 días de sesión ETH ⇒ requiere histórico ≈ 17 días.

**Caminos de warm-up (análisis):**

- **Modelo congelado:** warm-up = corpus `RebuildSegment`/`ReplayAnchor` que entra por el MISMO camino canónico (`v3/sdk/futures/market/recording.go:286-320,541-575`; "EXACT_REPLAY re-executes this corpus… NEVER consults MarketHistorySource (R1)"). FACT crítico de D5: **esa ruta de ingestión NO está implementada** — `ReplayAnchor`/`RebuildSegment` no tienen constructores fuera de tests; el journal es write-only; el anchor llega en el control envelope `RUN_START` y sólo se verifica y pinnea en el manifest (`v3/core/internal/functions/futures_market_stream.go:438-455`), nunca se re-ejecuta. Warm-up en D5 existe sólo como publicación directa de envelopes en tests (`v3/core/internal/futuresvertical/harness.go`). ⇒ D6 runtime wiring obligatorio: productor del corpus (publica envelopes históricos por `echo.futures.market-feed-candidates.v1` antes de `RUN_START`).
- **Fidelidad requerida por las estrategias congeladas:** las barras Echo son TRADE bars construidas desde eventos canónicos sin cascada entre timeframes (`v3/sdk/futures/bars/demands.go:22-25` "V1 bars are TRADE bars… no 1m→5m cascade"; `bars/payload.go` TRADE=`{"price","qty"}`, QUOTE=`{"bid_price","bid_qty","ask_price","ask_qty"}`). S2 consume **sólo closes** (SMA50 H4, Bollinger 5m closes — D4-B1 frozen); S1 consume OHLC de 5m (Opening Range high/low + stop desde closed 5m bars — D4-B3). SUPPORTED_INTERPRETATION: un corpus sintetizado a resolución 5m exacta (OHLC de 5m) reproduce **exactamente** todos los valores de warm-up de S1 y S2: 4 TRADE sintéticos por bucket 5m (O,H,L,C ordenados determinísticamente) reproducen la 5m bar exacta vía los builders TRADE existentes, y la H4 agregada desde esos eventos reproduce H4 OHLC exacto. La única pérdida vs rebuild tick-true es la trayectoria intra-bar de barras de warm-up, que ninguna decisión congelada consume (el stop de S2 usa el trigger bar, que siempre es una barra live real).
- **Fuente del corpus en NT:** SUPPORTED_INTERPRETATION: un fetch one-shot al arrancar el run vía `BarsRequest` (Minute-1 o Minute-5, ~20 días) del instrumento NQ en la propia conexión NT; Echo-side sintetiza determinísticamente los TRADE del corpus y los publica por el camino canónico. **NT NO se convierte en autoridad histórica durable**: es fuente de bootstrap one-shot; lo durable es el corpus pinneado en el run manifest (Exactamente como manda /baseline).
- UNKNOWN/gate D6: gaps/completitud del histórico minute servido por Tradovate demo en la ventana requerida (17+ días) — verifiable con una request real en D6; si la ventana no cubre, fail-closed de warm-up (`WARMUP_INCOMPLETE` ya es estado analítico downstream, no bloquea el feed).

**Separación de planos (mandato /execute.B).** Realtime runtime = MarketData/BarsRequest realtime events del AddOn → envelopes QUOTE/TRADE → topic ingress → `echo/market_stream` → `echo/market_analytics` (código D5 intacto). Warm-up histórico = corpus sintetizado one-shot (arriba). Replay/backtest durable de Echo = EXACT_REPLAY/BACKTEST congelados (D2-06/D5-S12) — NT no participa. MARKET_DATA_FIT = **PASS** (BBO + trades tick con timestamps + identidad FullName). HISTORICAL_DATA_FIT = **PARTIAL**: suficiente para warm-up S1/S2 vía síntesis 5m determinística; tick-history profundo de Tradovate no asumido; ruta de ingestión del corpus por construir (wiring D6).

---

## C. Order execution

**Tipos soportados.** FACT: `NinjaTrader.Cbi.OrderType` = {Market, Limit, MIT, StopMarket, StopLimit, Unknown} (reflexión); `OrderAction` = {Buy, Sell, BuyToCover, SellShort}; `TimeInForce` = {Day, Gtc, Ioc, Opg, Gtd}. **FACT crítico D5:** el dominio congelado sólo emite MARKET y LIMIT — `domain.OrderType` no tiene STOP (`v3/sdk/futures/domain/operation.go:38-43`), `Order.Validate` rechaza cualquier otra cosa (operation.go:94-101), y el "protective stop" de GerardMM es un **LIMIT en reposo** con `Role=PROTECTIVE` al precio de stop, con tighten por cancel+replace y salida MARKET si el mark ya cruzó (`v3/sdk/futures/gerardmm/gerardmm.go:417-578`; `PROTECTIVE_STOP_CROSSED` → `profitExitShape`). Las estrategias no emiten órdenes (sólo Signals con `TechnicalStop` provenance). ⇒ El adapter NT necesita MARKET→Market y LIMIT→Limit; STOP_MARKET existe en NT pero queda sin uso en V1 (sin contradicción: el seam D5 es más angosto que el wording D2-03 y eso es el freeze vigente).

**Submit / ciclo de vida.** FACT (reflexión + docs): submit asíncrono — `Account.Submit(order)` retorna y los cambios llegan por eventos. `OrderState` = {Initialized, Submitted, Accepted, Working, PartFilled, Filled, Cancelled, CancelPending, CancelSubmitted, ChangePending, ChangeSubmitted, Rejected, TriggerPending, Suspended, AcceptedByRisk, Unknown}. Mapping a `OrderStatusEvent.venue_status` (observación venue; el estado del aggregate Core sigue siendo D2-04 §3.2 — WORKING + fills para parciales, `v3/sdk/futures/domain/execution.go:14-23`).

- accepted/working: Accepted → Working ([Order Status Definitions](https://support.ninjatrader.com/s/article/Order-Status-Definitions); [OnOrderUpdate](https://static.ninjatrader.com/support/helpGuides/nt8/onorderupdate.htm)).
- modify: `Account.Change(...)` con estados ChangePending/ChangeSubmitted; cancel: `Account.Cancel(...)` con CancelPending/CancelSubmitted y ack físico = estado **Cancelled**. Map directo a `OrderActionResult` (`action_id` estable ya en el contrato, `execution.go:37-46`). FACT.
- partial fill: FACT — "An order can generate multiple executions (partial fills)" ([OnExecutionUpdate](https://static.ninjatrader.com/support/helpGuides/nt8/onexecutionupdate.htm)); `Order.Filled` acumulado; estado PartFilled. full fill: Filled.
- reject: Rejected (+AcceptedByRisk como rechazo de riesgo local); EVENTO DE ORDER por `Account.OrderUpdate` → `OrderEventArgs` (reflexión). Soporte `IsOrderTypeSupported` existe por cuenta (reflexión).
- positions: `Account.PositionUpdate` → `PositionEventArgs{Position, MarketPosition(Long/Short/Flat), Quantity, AveragePrice, Operation}`; `Position{Account, Instrument, MarketPosition, Quantity, AveragePrice}` (reflexión). Shape neto Account×Instrument — casa 1:1 con `PositionUpdate` family `(execution_account_id, contract_id, net_qty, ...)` (`execution.go:92-107`).

**Ordering guarantees conocidas.** FACT (docs): `OnExecutionUpdate` "is typically called after OnOrderUpdate()"; "execution.Order … may not be up to date if an ExecutionUpdate is seen before an OrderUpdate in a partial fill"; "Instances of multiple fills at the same time … sequence of events are not guaranteed due to provider API design" (dicho para Rithmic/IB — se extrapola como caveat de clase, no claim de Tradovate). ⇒ Regla adapter: **correlacionar por ids (execution.OrderId string), nunca por orden de llegada ni por punteros de objeto**. El diseño Echo ya es tolerante: Fill puede preceder ACK (D2-07 §8 congelado), correlación adapter-owned por `operation_id`/`order_id`, Fill identity nativa.

**Identidades nativas.** FACT: `Order.Id` = **Int64** (id local NT por conexión), `Order.OrderId` = **String** (id nativo venue/Tradovate), `Execution.ExecutionId` = **String**, `Execution.OrderId` = **String** (reflexión). El dedup Echo exige `(execution_account_id, provider_execution_id)` nativo estable (`v3/sdk/futures/domain/operation.go:214-222` FillIdentity — sin sustitutos sintéticos; regla D2-07-R1). Candidato: `provider_execution_id = Execution.ExecutionId` (nativo Tradovate). GATES D6 (no bloquean C1): unicidad/stability de `ExecutionId` realtime↔history↔restart, y retention de `Order.OrderId` + `Order.Name` tras reconnect/restart (ver D). El histórico de executions es configurable por cuenta: propiedades `Account.LookbackDaysExecutions` / `LookbackDaysOrders` (reflexión) — horizon material para el recovery gate.

ORDER_LIFECYCLE_FIT = **PASS** (todas las transiciones Echo del contrato tienen evento/estado NT nativo; idempotencia nativa de submit NO existe — ver D).

---

## D. M1 / M2 fit

**M1 (Core state ↔ command publication).** REUSE_AS_IS — intocado por NT. Implementado en D5: egress transaccional per-account (`v3/core/internal/functions/futures_operation.go:369-377`), envelope proyectado field-by-field (`v3/core/internal/futuresruntime/runtime.go:263-330`), consumo `ReadCommitted` + commit-after-outcome en el bridge (`v3/futures-bridge/adapters/kafka/command_consumer.go:64,159-186`). Config EXACTLY_ONCE del producer sigue siendo requisito de deployment D5/D6 (module.yaml lo declara como comentario de despliegue; no cambiar por NT).

**M2 (command ↔ physical side effect).** El contrato congelado (D2-07 §9-11) mapea así sobre NinjaTrader:

| Obligación congelada | Mapeo NinjaTrader | Clasificación |
|---|---|---|
| Durable PREPARED antes del point-of-no-return | `journal.Prepare` (journalfs, fsync por append — `v3/futures-bridge/adapters/journalfs/journal.go:160-181`) antes de tocar NT | REUSE_AS_IS |
| SUBMITTING antes del paso que alcanza al venue | `journal.MarkSubmitting` antes de la llamada `Account.Submit` (el point-of-no-return físico es esa llamada) | REUSE_AS_IS + SMALL_D6_ADAPTER_WORK (llamada NT dentro de `ExecutionAdapter.Submit`) |
| Stable client identity | **No hay parámetro nativo de client-order-id en `Account.CreateOrder/Submit`**. Primitiva disponible: `order.Name` (signal name, visible en `OrderUpdate`/history — docs match by `order.Name`: [OnOrderUpdate](https://static.ninjatrader.com/support/helpGuides/nt8/onorderupdate.htm)). `client_order_id` ⇒ `order.Name`. Retention/uniqueness = gate D6 | SMALL_D6_ADAPTER_WORK + D6_CERTIFICATION_ONLY |
| No blind retry | Journal + guard de sesión ya lo fuerzan (`session.go:310-372`); el retry físico sólo tras reconcile que demuestre ausencia | REUSE_AS_IS |
| Reconcile-before-resubmit (ambiguous submit) | Resolver contra: `Account.Orders` (órdenes vivas re-sincronizadas), `Account.FindOrderById` (Id Int64 in-session), scan de `Account.Executions` por `Execution.OrderId`+`ExecutionId` dentro del horizon `LookbackDaysExecutions`; encontrado ⇒ adoptar outcome (VENUE_BOUND); ausencia autoritativa dentro del horizon ⇒ retry legal por ausencia (`ResubmitApprovedByAbsence` ya existe en `ReconciliationReport`, `adapter.go:392-407`); ni-ni ⇒ `AMBIGUOUS` fail-closed | REUSE_AS_IS (flujo congelado) + SMALL_D6_ADAPTER_WORK (búsquedas NT) + D6_CERTIFICATION_ONLY (horizon real) |
| Dedup/idempotencia de fills | `(execution_account_id, ExecutionId)` vía `ExecutionFill.DedupKey` + gate de fills del bridge (`v3/futures-bridge/internal/session/gate.go:88-100`) | REUSE_AS_IS + D6_CERTIFICATION_ONLY (ExecutionId stability) |
| Native idempotency del venue | **NO EXISTE** en la API NinjaScript (sin dedup por client tag documentado) ⇒ V1 no puede reclamar exactly-once por plataforma; la corrección M2 viaja por journal + reconciliación, que es exactamente el diseño congelado para transports sin native idempotency | FACT → sin contradicción; transport queda en la clase "idempotency via reconciliation" |

**Punto M2 que no se redefinirá:** "OrderId mutable/no único" del record D2-07B es un riesgo de clase (stale order objects); NT lo mitiga con ids duales (Id Int64 + OrderId nativo string) y el patrón documentado de re-obtener referencias vivas ([GetRealtimeOrder](https://static.ninjatrader.com/support/helpGuides/nt8/getrealtimeorder.htm)). La regla congelada D2-07-R1 (sólo identidad nativa estable para Fill; prohibidos sintéticos) queda intacta: si D6 no demuestra `ExecutionId` estable, el transport queda `UNSUPPORTED_FOR_V1_EXACT_SUBMISSION` — gated, no aproximado.

M1_M2_FIT = **PASS** (mecanismo mapeable sin redefinir D5; idempotencia nativa ausente ya está contemplada por el diseño).

---

## E. Recovery / reconciliation

**Qué es observable después de reconnect/restart.** FACT (reflexión): por `Account` — `Orders` (working orders re-sincronizadas de la conexión), `Executions` (historial según `LookbackDaysExecutions`), `Positions`/`GetPosition` (neta por instrumento), `GetAccountItem` (AccountItem: cash/balance/etc., con evento `AccountItemUpdate`), `AccountStatus`. Por conexión — `ConnectionStatusUpdate`, y el re-sync de estado ocurre tras `Connected`. docs: [Account Class](https://ninjatrader.com/support/helpguides/nt8/account_class.htm). Physical NT restart: working orders de Tradovate viven server-side y son re-synced; UNKNOWN (gate D6): si `Order.Name` (client identity) y `Order.OrderId` sobreviven el restart de NT con los mismos valores — observable directo.

**Mapeo a la barrier congelada** (D2-07 §13; implementada en `session.RunRecoveryBarrier`, session.go:148-243): autenticar (ConnectionStatus) → verificar physical account binding (Account.All ∩ config Id+Name) → restablecer subscriptions (MarketData re-subscribe) → cargar journal no-terminal (journalfs.ListNonTerminal) → resolver cada PREPARED/SUBMITTING/VENUE_BOUND/AMBIGUOUS por client identity (scan Orders por Name + Executions por OrderId/ExecutionId) → listar/reconciliar open orders desconocidas → `UnknownLiveOrders` quarantine (ya en `ReconciliationReport`, adapter.go:392-407) → recuperar executions/missed fills desde horizon con dedup por ExecutionId → Position autoritativa fresh (`GetPosition`/`Positions` + `PositionUpdate` events) → emitir observaciones normalizadas → contrastar físico vs lógico. **No existe "on reconnect → replay pending commands"** en NT ni se necesita.

**Casos /execute.E:** submit ambiguo → reconcile arriba (D). Fill durante disconnect → `Account.Executions` history + dedup ExecutionId. Order working tras restart → re-sync Orders + pinning del journal al binding original (journal per binding, `main.go` config). Partial fills → history + dedup. Cancel pendiente → estado Cancelled/Filled + fills que ganaron la race (conservación de late fill ya congelada D2-07 §11). Missing local event → history dentro del horizon; si el horizon no cubre el outage ⇒ AMBIGUOUS/not-ready fail-closed (R5 de D2-07 §27, correcto por diseño).

RECOVERY_RECONCILIATION_FIT = **PASS** (mecanismos completos y mapeables; horizon y retention = gates D6).

---

## F. Runtime placement

**Superficie mínima dentro de NinjaTrader: un AddOn (`NinjaTrader.NinjaScript.AddOnBase`).** Justificación con source real:

1. FACT: `NinjaTrader.NinjaScript.AddOnBase` existe en `NinjaTrader.Core.dll` 8.1.8.3 con ciclo de vida propio (`State`, `SetState`, `NotifyCreated/Destroyed/Restored/Saved`, `OnStateChange`) y es la superficie NinjaScript **no-Strategy** documentada para automatización host-side ([OnWindowCreated / AddOn framework](https://static.ninjatrader.com/support/helpGuides/nt8/onwindowcreated.htm); sample oficial AddOnFramework: "NT creates an instance of each class derived from AddOnBase").
2. FACT: el AddOn accede a todo lo requerido: `Account.All`, eventos de cuenta (`OrderUpdate/ExecutionUpdate/PositionUpdate/AccountItemUpdate/AccountStatusUpdate`), `Account.Submit/Change/Cancel/Flatten`, `Instrument.MarketData.Update` realtime, `BarsRequest` histórico.
3. Un **NinjaScript Strategy** queda descartado: acoplaría las órdenes Echo a lifecycle de chart/bars y a la máquina de estados de Strategy de NT — exactamente lo que /frozen prohíbe (no provider-specific Strategy; el decision-making vive en Echo). El AddOn es transport puro, sin autoridad de dominio (D2-07 §5: "Bridge sin autoridad de dominio").
4. SUPPORTED_INTERPRETATION: la operación de un AddOn sin UI es viable (la subscripción de ventana `OnWindowCreated` es opcional; el estado y los eventos no requieren ventana) — certificación "headless real" (NT arrancado y AddOn vivo sin interacción) = gate D6 barato.

**División física del adapter (coherente con el congelado):** D2-07 §6 ya congeló `DesktopHostedAdapter` = "conector + componente platform-side dentro del desktop" como **parte del adapter**, sin identidad de dominio propia. Concretamente: (a) **bridge-side (Linux, futures-bridge)** — todo lo congelado queda: consumer per-account, journal M2 journalfs, guards, readiness, publisher de observaciones; el adapter NT implementa la interfaz `ExecutionAdapter` delegando sobre el canal. (b) **desktop-side (AddOn en NT)** — endpoint físico: resuelve/subscribe cuentas, captura eventos, ejecuta submits/cancels, publica observaciones y market events, y hace el fetch de warm-up. **Canal AddOn↔bridge:** conexión TCP/WebSocket outbound iniciada por el AddOn hacia el bridge (el bridge ya escucha en LAN; NT hoy abre listeners pero el AddOn puede ser cliente puro). KISS: un canal bidireccional que transporta (i) JSON de comandos (envelope SUBMIT/CANCEL/REPLACE ya definido, `runtime.go:263-330`), (ii) observaciones normalizadas (envelope `{schema, family, event}`, `v3/futures-bridge/adapters/kafka/publisher.go:22-26`), (iii) market envelopes canónicos (`MarketCandidateEnvelope`/`MarketControlEnvelope`, `v3/sdk/futures/market/ingress.go` + `control.go`). Sin Kafka dentro de NT (evita cliente .NET-Kafka + credenciales en el desktop; el bridge es el único productor/consumidor Kafka — topología congelada).

**Estado durable:** NADA nuevo en el desktop. El journal M2, el pin de binding, y las identidades viven en el bridge (congelado §10: la durability domain del side-effect owner). El AddOn es stateless-recuperable: cuentas/positions/orders se re-observan de NT tras reconnect (E); in-flight lo posee el journal bridge-side. Config del AddOn (URL del bridge, account esperado, contrato NQ): archivo de config local del perfil NT — detalle de implementación D6.

**Lifecycle:** NT arranca → instancia el AddOn → AddOn conecta outbound al bridge → bridge ya está consumiendo su topic per-account → handshake/estado → `ConnectionStatusUpdate(Connected)` → barrier → `ReadyNewRisk`. Apagado: reverse. La adición de un `NINJATRADER_BRIDGE` transport ya está anticipada por el enum de `TransportSpec` (`v3/sdk/futures/domain/provider.go:289-293` comenta `PROJECTX | NINJATRADER_BRIDGE | TRADOVATE_API | RITHMIC | CQG | SIM_EXECUTION`) y el switch duro SIM-only del D5 (`main.go:137-140` "vendor transports are D6") es el punto exacto donde se habilita.

---

## G. Local identity / evidence (pregunta abierta de C0)

**Respuesta: el componente NinjaScript publica directamente lo necesario — no se requiere cambiar ACL ni identidad, y no se requiere NT bajo otra identidad para el runtime.** FACT: el AddOn corre dentro del proceso NT en la sesión interactiva del owner (KoR) y por tanto tiene acceso completo al estado vivo de la app (cuentas, órdenes, ejecuciones, positions, market data) que hoy es ACL-inaccesible para `dev-win\echo-dev` (C0 E9). FACT: el canal AddOn→bridge saca esa evidencia por red (outbound), sin tocar el filesystem del perfil KoR. ⇒ camino (c) publisher de evidencia de C0 §6, resuelto como parte del propio diseño del adapter. La identidad de automatización (`dev-win\echo-dev`) mantiene su rol actual; los logs nativos de NT (`Documents\NinjaTrader 8\log|trace`) siguen siendo evidencia de soporte, no del hot path — si algún día se requieren, es decisión owner (ACL o identidad), fuera de este shot. Instalación/compilación del AddOn (NinjaScript Editor compila a `Documents\...\bin\Custom` del perfil interactivo) = paso one-time asistido por owner, no parte del runtime. Sin cambios de ACL/identidad ejecutados en este shot (cumplido).

---

## H. Delta classification

| Obligación | Clasificación |
|---|---|
| Strategy/Signal/Operation/GerardMM/ProviderRuleSet/ReservationRevalidate/`egress_authorized`/journal/recovery contracts/EXACT_REPLAY/BACKTEST/M1 | `REUSE_AS_IS` |
| Futures Bridge shell, journalfs, guards de sesión, EventGate dedup, readiness conjunction, recovery barrier, routing 3-caminos, projectors | `REUSE_AS_IS` |
| Contrato de market ingress (topic + `MarketCandidateEnvelope`/control + payloads `{"price","qty"}` / `{"bid_price","bid_qty","ask_price","ask_qty"}`) | `REUSE_AS_IS` |
| Mapping canónico NQ → contrato físico + `external_contract_identifier` por cuenta (ETCD) | `REUSE_AS_IS` (config) |
| Enum transport `NINJATRADER_BRIDGE` en `TransportSpec` | `CONFIG_ONLY` (ya existe como valor anticipado; la elección por cuenta es config ETCD) |
| Transport branch en `buildSession` (hoy hard-fail SIM-only, `main.go:137-140`) + registro del adapter NT + `CapabilityDeclaration` NT | `SMALL_D6_ADAPTER_WORK` |
| Implementación NT de `ExecutionAdapter` bridge-side (Submit/Cancel/Replace → canal; Reconcile/ListOpenOrders/PositionSnapshot → NT por canal; ReadinessInputs) | `SMALL_D6_ADAPTER_WORK` |
| AddOn desktop: resolución de cuenta (Id+Name), subscriptions MD, captura de 4 eventos de cuenta, ejecución de órdenes, `BarsRequest` warm-up fetch, síntesis determinística del corpus, publicación de envelopes por el canal | `D6_RUNTIME_WIRING` |
| Endpoint canal AddOn↔bridge (TCP/WS, framing JSON, heartbeats, sesión) en ambos lados | `D6_RUNTIME_WIRING` |
| Productor del stream de mercado + ruta de publicación del corpus REBUILD (hoy inexistente fuera de tests; anchor sólo se pinnea) | `D6_RUNTIME_WIRING` |
| Gates: `ExecutionId` unicidad/stability realtime↔history↔restart; retention de `Order.Name`/`Order.OrderId` tras reconnect/restart; `LookbackDaysOrders/Executions` horizon vs outage tolerable; re-sync de open orders post-reconnect; estabilidad de `Account.Id` GAU50; AddOn headless real; warm-up corpus fidelity (5m exacto) aceptada; C0 GUI checklist pendiente (NQ visible, MD, balances, positions/orders) + disconnect/restart B2 | `D6_CERTIFICATION_ONLY` |
| Config cuentas: binding con entitlement (entitlement real Tradovate/GAU50 permanece según preflight `BLOCKED_PENDING_PROVIDER_CONFIRMATION` — no reabierto aquí) | `CONFIG_ONLY` / riesgo owner vigente |
| `MATERIAL_D5_CONTRADICTION` | **NONE** (ver §5) |

---

## 5. Contradicciones / hallazgos de materialidad

1. **Ninguna contradicción material con D5.** El contract congelado mapea nativo contra NinjaTrader; cada boundary M2 tiene análogo físico; ningún contrato D5 requiere redefinición. El wording D2-03 que menciona `STOP` como entry_type de Signal nunca llegó al dominio congelado (`OrderType` sólo MARKET/LIMIT) — el freeze D5 es el vigente y es consistente end-to-end; se registra como aclaración, no contradicción.
2. **Gap de implementación D5 relevante para D6 (no defecto):** la ruta de ingestión del corpus REBUILD/anchor no existe en runtime (sólo tipos + pinning). Sin ella, S2 queda en `WARMUP_INCOMPLETE` indefinidamente desde arranque frío. Es wiring D6 obligatorio, ya contemplado conceptualmente por el modelo congelado.
3. **D5 no tiene ningún productor real de market data** (`echo.futures.market-feed-candidates.v1` sólo tiene constructores de test). El AddOn NT será el primer productor — el contrato del envelope ya está congelado e implementado en el consumer.
4. **Nota operacional menor observada:** `v3/futures-projector/adapters/kafka/runner.go:86` consume con `OffsetOldest` y aislamiento default (ReadUncommitted) sobre topics transaccionales — candidato a config `ReadCommitted` en D6 (coherencia con el resto del pipeline; no afecta C1).
5. **Seguridad de superficie:** NT expone listeners LAN `0.0.0.0:4530/36973` (C0 E10). El canal AddOn↔bridge debe autenticarse (token compartido mínimo) y restringirse a LAN de confianza; hardening ya registrado en C0.

## 6. Implementation shot inputs (para el Primary Manager)

- Shot de implementación D6-N1 recomendado: **"NinjaTrader AddOn vertical read-only"** — AddOn que (1) resuelve la cuenta GAU50 por Id+Name de config, (2) subscribes `MarketData.Update` de NQ y publica envelopes QUOTE/TRADE al bridge, (3) captura `OrderUpdate/ExecutionUpdate/PositionUpdate/AccountItemUpdate` y publica observaciones, (4) expone session status. Sin submits. Cierra observables C0 pendientes con evidencia propia del AddOn (no GUI) y certifica headless.
- Shot D6-N2: **ejecución** — transport branch + adapter bridge-side + submits/cancels con journal M2 + reconcile; sim scenarios NT-like como fixtures. Requires: gates de certificación ejecutándose en paralelo (ExecutionId/Name retention/history horizon).
- Shot D6-N3: **warm-up + S2 live-demo** — BarsRequest fetch + síntesis corpus + RUN_START con anchor + S2Signals sobre datos reales (sim execution o NT según avance de certificación).
- La elección account activa autorizada (1 de 5) y el id/nombre (sanitizado) es input owner en el momento del shot (policy: 1 activa a la vez).

## 7. Handoff

```text
D6_C1_ADAPTER_FIT = PASS

ARTIFACT:
main/10-projects/Echo Futures/artifacts/d6-ninjatrader-certification-20260930/C1-NINJATRADER-ADAPTER-FIT-ANALYSIS.md

AGENTS_OS_SHA:
<registered-at-close>

ECHO_BASELINE:
13e087a3bb762f65b060d3b3200fb00a67c6ff1d

PHYSICAL_TARGET:
NinjaTrader Desktop 8.1.8.3 / Tradovate / GAU50

RECOMMENDED_NINJATRADER_SURFACE:
NinjaScript AddOn (NinjaTrader.NinjaScript.AddOnBase) — host-side transport component, no Strategy, no UI dependency; bridge-side half of the adapter stays in futures-bridge per frozen topology (DesktopHostedAdapter = connector + desktop component).

ACCOUNT_IDENTITY:
5 GAU50 Evaluation accounts exposed as NinjaTrader.Cbi.Account objects in static Account.All; stable Id=Int64 + Name; adapter resolves the ONE authorized account by configured Id+Name and re-resolves after every reconnect (ConnectionStatusUpdate); GUI account selector irrelevant for programmatic orders.

ACTIVE_ACCOUNT_SELECTION:
Explicit runtime authority = ETCD futures-bridge/accounts/{id}/* binding (provider-external-account-id) + bind-time verification against Account.All + per-submit binding pin + payload-vs-session defence-in-depth (all already implemented in D5 bridge). Exactly one Echo session per account; the other 4 GAU50 receive no commands.

MARKET_DATA_FIT:
PASS (realtime Bid/Ask/Last tick stream with timestamps via Instrument.MarketData.Update; instrument identity = FullName/Expiry mapping to external_contract_identifier).

HISTORICAL_DATA_FIT:
PARTIAL (BarsRequest Minute history sufficient to synthesize an exact 5m-resolution warm-up corpus reproducing all S1/S2 warm-up values — closes for S2, OHLC for S1; NT used as one-shot bootstrap source only, corpus pinned in run manifest; tick-history depth of Tradovate demo UNKNOWN; warm-up REBUILD ingestion path must be built in D6 — D5 has only the frozen types + manifest pinning).

ORDER_LIFECYCLE_FIT:
PASS (MARKET/LIMIT map natively — domain emits only MARKET/LIMIT in frozen D5, GerardMM protective stop = resting LIMIT; async submit; full OrderState set incl. PartFilled/CancelPending/ChangePending/Rejected; PositionUpdate net Account×Instrument native; correlation must be id-based: Order.OrderId String + Execution.ExecutionId String are the native identities; no venue-side submit idempotency).

M1_M2_FIT:
PASS (M1 untouched; M2: journal write-ahead + point-of-no-return at Account.Submit + client identity via order.Name + reconcile-before-resubmit over Account.Orders/FindOrderById/Executions with LookbackDays horizon; ambiguity → AMBIGUOUS fail-closed; frozen D2-07-R1 native-execution-identity rule intact and gated).

RECOVERY_RECONCILIATION_FIT:
PASS (post-reconnect observables complete: Orders re-sync, Executions history, Positions, AccountItem; maps 1:1 onto frozen RunRecoveryBarrier incl. UnknownLiveOrders quarantine; history horizon vs outage and Name/OrderId retention across restart = D6 certification gates).

MINIMUM_RUNTIME_COMPONENTS:
1) Desktop AddOn (account resolution, MD subscriptions, order-event capture, order submission, BarsRequest warm-up fetch, canonical envelope publication, outbound channel client); 2) bridge-side NINJATRADER_BRIDGE ExecutionAdapter implementation + channel endpoint (all frozen bridge machinery reused); 3) market-feed producer path (bridge publishes NT envelopes to echo.futures.market-feed-candidates.v1) + REBUILD corpus publication at RUN_START.

D5_REUSE:
100% of Core/StateFun owners, futures-bridge shell/journal/guards/readiness/barrier, normalized event families, Kafka routing, market canonicalization/analytics, S1/S2/GerardMM, provider plane, EXACTLY_ONCE egress contract. Zero product-code changes to D5 required by this analysis.

CONFIG_ONLY:
TransportSpec value NINJATRADER_BRIDGE (already anticipated in enum); per-account ETCD binding config; NQ external_contract_identifier.

SMALL_D6_ADAPTER_WORK:
buildSession transport branch (currently SIM-only hard fail); NINJATRADER_BRIDGE adapter implementation against the frozen ExecutionAdapter interface; capability declaration; STOP absent by design (no work needed); projector ReadCommitted config note.

RUNTIME_WIRING:
AddOn desktop component; AddOn↔bridge bidirectional JSON channel (commands/observations/market envelopes); market producer path; REBUILD/warm-up corpus publication before RUN_START; AddOn config file.

CERTIFICATION_ONLY:
ExecutionId uniqueness/stability; Order.Name + Order.OrderId retention across reconnect/restart; Account.Id stability across NT restart; LookbackDaysOrders/Executions horizon adequacy; open-order resync post-reconnect; AddOn headless real-run; warm-up corpus fidelity acceptance (5m-exact synthesis); C0 GUI checklist + disconnect/restart observables (B2); Earn2Trade/Tradovate automation entitlement remains per preflight (owner risk accepted, not re-litigated here).

MATERIAL_D5_CONTRADICTIONS:
NONE

BLOCKERS:
NONE for C1. D6 implementation preconditions carried from C0: owner GUI checklist (C0 §8) and reconnect/restart evidence (B2) remain pending and are absorbed by the D6-N1 read-only AddOn shot as an alternative evidence path; Earn2Trade automation/API entitlement stays an owner-accepted risk per preflight.

IMPLEMENTATION_SHOT_INPUTS:
D6-N1 read-only AddOn vertical (accounts+MD+events+session, no orders); D6-N2 execution (transport branch + adapter + journal M2 live + reconcile); D6-N3 warm-up (BarsRequest fetch + 5m-exact corpus synthesis + RUN_START anchor + S2 demo). Owner input needed at shot time: which GAU50 is the authorized active account (sanitized Id/name).

NEXT_MANAGER_ACTION:
Dispatch D6-N1 as the first implementation shot (read-only AddOn, closes C0 GUI observables via AddOn evidence and starts the D6 certification-gate collection); sequence D6-N2/D6-N3 per inputs above; keep PROJECTX/Rithmic/CQG untouched.
```
