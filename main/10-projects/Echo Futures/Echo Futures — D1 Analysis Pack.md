---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo Futures]]"
  - "[[Echo Futures — Futures Prop Universe]]"
  - "[[Echo Futures — Prop Economics Experiment]]"
aliases:
  - Echo Futures D1
  - EF D1 Analysis Pack
tags:
  - kind/doc
  - area/echo
  - echo-futures
  - architecture-analysis
  - research
created: "2026-09-25"
updated: "2026-09-26"
---

# Echo Futures — D1 Analysis Pack

> [!warning]+ OWNER CORRECTION — PRELIMINARY MANAGER ADVANCE
> Este pack **NO cierra D1, NO resuelve Q1 por autoridad del owner y NO habilita D2**. Fue producido prematuramente por el manager al ejecutar trabajo que debía haber coordinado/delegado. Se conserva íntegramente como adelanto de evidencia y como input crítico para revisión, pero todas sus conclusiones y readiness labels son **CANDIDATE/PRELIMINARY** hasta que el manager las recorra con el owner, despache los deep researches/auditorías que correspondan y cierre el checklist D1 en conjunto.

> [!important]+ OWNER REVIEW ADDENDUM — 2026-09-26
> Este addendum **tiene precedencia** sobre terminología/propuestas anteriores dentro de este pack cuando exista contradicción.
>
> - Nombre canónico: **MoneyManagement**, no CapitalManagement. Cualquier mención previa a CapitalManagement en este pack debe leerse como antecedente histórico del mismo concepto, salvo que el contexto hable específicamente del nombre legacy.
> - **StrategyEngine** queda aceptado como nombre del runtime de estrategias internas. La forma/nombre de la implementación concreta de cada estrategia queda abierta para D2.
> - Echo debe converger a motores genéricos cross-market; no debe existir lógica de dominio separada Forex/Futures. Los motores transversales identificados son StrategyEngine y Market Feed Engine.
> - El nuevo generic execution path nace desde **canonical Signal**. `ReferenceEvent` sigue siendo legacy/source-specific y evidencia de una operación reference ya ejecutada.
> - El adapter `ReferenceEvent -> Signal` vive en **Echo Core**, en un boundary explícito antes del motor genérico. Bridge permanece edge/transport dummy.
> - La migración completa del execution path reference queda en **DT-EF-REFERENCE-SIGNAL-03 — DEFERRED_MANDATORY**; lo incremental es la migración legacy, no crear dos motores finales.
> - Signal puede representar intents `OPEN`, `REDUCE`, `CLOSE`, `CLOSE_ALL` (enum final D2). Strategy puede emitir 0..N Signals y varias por una misma evaluación; si el orden altera el resultado, debe existir procesamiento determinístico.
> - Boundary owner: Strategy = lógica **técnica**; MoneyManagement = lógica **económica/de dinero y riesgo** por AccountStrategy.
> - Strategy decide qué hacer y puede proponer direction/entry intent/precio y SL/TP técnicos. Nunca hace sizing ni decide riesgo monetario.
> - MoneyManagement decide cuánto/cómo materializar la intención: sizing, riesgo monetario, exposición, adds/reductions y protección/targets ejecutables; luego gestiona la Operation durante su lifecycle.
> - Ejemplo conceptual: Strategy puede emitir OPEN LONG con SL/TP técnicos; MoneyManagement puede resolver riesgo monetario/target monetario + quantity y producir las Orders físicas.
> - OPEN: la precedencia entre SL/TP técnicos de Strategy y ajustes monetarios/hardscalping de MoneyManagement NO está congelada; resolver en Q13. No asumir que MM siempre overridea ni que Strategy levels son inmutables.
> - Puede existir hardscalping técnico en Strategy y hardscalping monetario en MoneyManagement si cada uno conserva ownership distinto.
> - Signal debe tener expiración explícita; una señal expirada no materializa Operation. `MaxOpenDelaySeconds` legacy puede adaptarse a esa semántica.
> - MoneyManagement administra la Operation durante todo el lifecycle y debe poder reaccionar a fills/orders, account/instrument state, lifecycle/session events y market data/bars MTF. La topología física/state owner no se congela en D1.
> - Un Signal de apertura aceptado **materializa la Operation antes de MoneyManagement y antes de cualquier Order/Fill**.
> - Si MoneyManagement no puede resolver una acción ejecutable, rechaza/falla, o la Signal/entry expira sin Fill, la Operation igualmente termina con motivo explícito para trazabilidad.
> - Una Operation sin Fill no implica Position física.
> - Lifecycle conceptual aceptado: `CREATED` → `PENDING_ENTRY` → `ACTIVE` → `TERMINAL`, permitiendo terminales anticipados desde CREATED/PENDING_ENTRY. `PENDING_ENTRY` significa que existe una Order de entrada viva/working pero todavía no existe Fill. El **primer Fill que genere exposición**, incluso parcial, hace la Operation `ACTIVE`.
> - Un Order REJECTED/CANCELLED/EXPIRED no termina automáticamente la Operation: MoneyManagement puede retry/reemplazar/continuar.
> - Volver a exposición lógica cero tampoco implica TERMINAL por sí solo. TERMINAL requiere al menos exposición lógica cero, ninguna Order viva asociada y decisión de MoneyManagement de no continuar.
> - La dirección de una Operation es inmutable. Su exposición lógica se deriva de sus Fills y puede aumentar, reducirse o llegar temporalmente a cero, pero nunca cruza de LONG a SHORT ni viceversa.
> - Un reversal requiere cerrar/reducir la Operation existente y emitir una nueva `OPEN Signal` que cree otra Operation en la dirección opuesta.
> - Position sigue siendo exposición física observada por Account y puede agregar/netear múltiples Operations; no sustituye el estado lógico de exposición por Operation.
> - Signals posteriores de gestión/salida pueden actuar sobre Operations existentes sin crear una nueva Operation.
> - Operation puede producir N Orders; Order puede producir 0..N Fills; Fill es inmutable.
> - Position pertenece a **Account** y representa una proyección/snapshot del estado físico observado/reconciliado; no es Operation ni se eleva a aggregate rico sin requisito concreto.
> - `DT-EF-POSITION-RECONCILIATION-05 — DEFERRED_EDGE_CASE`: no diseñar ahora política de mismatch lógico↔físico, auto-repair ni subsystem dedicado. Reabrir sólo con evidencia real o si un transport/provider demuestra que es un caso material.
> - Trade/The Lab queda fuera de A2 y diferido al proyecto The Lab; el runtime nuevo no se deforma para conservar el modelo analítico actual.
> - El dominio nuevo no puede usar pips como unidad universal. Futures V1 requiere unidades genéricas basadas en instrument/contract specs; el legacy Forex puede adaptarse. La limpieza total de campos/workarounds pips queda como deuda candidata pendiente de ID/alcance final del owner.
> - Política de refactor: si el cambio correcto es acotado se hace en V1; si amenaza V1, seam limpio + DT explícita de Iteración 2. KISS **no** justifica romper SOLID/Clean boundaries.
> - Regla obligatoria del manager: ante una brecha material de requisitos, identities, lifecycle, ownership o semántica de dominio, **preguntar al owner antes de decidir; no asumir**.
> - Estado: **A1 Strategy/Signal/AccountStrategy/MoneyManagement = MANAGER_REVIEW_ACCEPTED_WITH_OWNER_CORRECTIONS**. **A2 Operation/Order/Fill/Position = D1_OWNER_REVIEW_ACCEPTED**; detalles exactos de Order lifecycle quedan Q3/D2; Trade/The Lab = **DEFERRED_TO_THE_LAB**. D1 completo sigue `IN_PROGRESS`; `EF_D1_ANALYSIS_PASS = NOT_EVALUATED`.


## Gate

EF_D1_ANALYSIS_PASS = NOT_EVALUATED

D1 sigue **IN_PROGRESS**. Este artefacto es un evidence pack preliminar; no sustituye el trabajo guiado del manager ni los deep researches específicos que el owner decida ejecutar.

## Baselines de evidencia

| Autoridad / repo | Baseline usado | Rol |
| --- | --- | --- |
| Agents-OS | xKoRx/agents-os master@79477c8367d30acf1e19ee3967273feaad76ca79 | Proyecto canónico, frozen owner decisions, roadmap y Critical Design Register. Incluye 493ca539cba7f031f2cc015b51916948ebc0ae00 y feedback posterior 79477c83. |
| Echo Core | xKoRx/echo master@372af59a7b83604781346613da01e3d510ea1360 | Source físico V3. |
| Echo SDK/domain | xKoRx/echo master@372af59a7b83604781346613da01e3d510ea1360 | Source físico V3. |
| Echo Bridge | xKoRx/echo master@372af59a7b83604781346613da01e3d510ea1360 | Source físico V3. |
| Echo Gateway | xKoRx/echo master@372af59a7b83604781346613da01e3d510ea1360 | Source físico V3. |
| Echo Futures experiment repo | xKoRx/echo-futures master@d4f42a41946f12231b75e4eb65b90d132731be0d | Evidencia histórica/simulador; NO autoridad de arquitectura. |

Los README/RFC V1/V2 y el antiguo M0 se trataron como evidencia histórica. Cuando discrepan con V3, manda el source V3.

## 1. Resultado preliminar Q1 — Echo physical/source fit

Q1 = CANDIDATE_FOR_OWNER_REVIEW.

El source audit realizado por el manager queda como evidencia reutilizable, no como cierre unilateral. El próximo manager debe recorrer esta matriz con el owner y decidir qué puntos requieren source audit adicional o un agente especializado antes de cerrar Q1.

Conclusión: Echo Futures debe extender Echo V3 incrementalmente. No apareció ningún bloqueo material que obligue a reescribir Core V3. Sí aparecen boundaries de dominio que no deben resolverse reciclando nombres actuales con semántica incorrecta: Signal no es ReferenceEvent; Operation no es trade_id; Order no es CoreCommand; Fill no es ExecutionResult; Strategy ejecutable no es StrategyConfig; CapitalManagement no es solamente MMEngine.

### Source/domain map físico

| Concepto / owner actual | Source V3 | Semántica real / lifecycle | Identity / state owner / persistence | Evidencia y deuda D1 |
| --- | --- | --- | --- | --- |
| ExecutionPlannerFn | v3/core/internal/functions/execution_planner.go — blob 371bf5e337b97dcc6188688e7e377e1a3dcb095c | Recibe ReferenceEvent, resuelve policies por strategy y fan-out a requests de MM por execution account. | StateFun keyed por trade/correlation; StrategyConfig/Kache entrega policies. | Test físico execution_planner_test.go blob d7e47b43. Reutilizable como patrón de fan-out, no como Strategy runtime. |
| StrategyConfigFn | v3/core/internal/functions/strategy_config.go — blob b89a9a1a61f71c1e1bae0876504589d5844543cd | KVS de ExecutionPolicy[] por strategy_id; procesa POLICY_UPDATE/DELETE y lookups. | StateFun ValueSpec StateStrategyConfig. | Test blob a2fbd342. El nombre strategy no implica código ejecutable de Strategy. |
| MMEngineFn | v3/core/internal/functions/mm_engine.go — blob e725ceb0bd056f3312365b96fbd93e6f52fdde5f | Junta AccountSnapshot + InstrumentSnapshot, calcula fixed-lot/fixed-risk y produce CoreCommand con offsets SL/TP. | StateFun pending MM keyed por account:strategy:trade; snapshots son inputs. | Test blob 2e54d438. Sirve como primitive de sizing/risk; no administra el lifecycle completo de Operation. |
| ExecutionStoreFn | v3/core/internal/functions/execution_store.go — blob d8c61700e8d3a97e286a485aae896c30632c372d | Mantiene ejecuciones abiertas por trade_id; agrega un OpenExecution por ExecutionResult exitoso y remueve al cerrar. | StateFun ExecutionStore {TradeID, []OpenExecution}. | Test blob d0628164. Su modelo actual asume un resultado/fill simplificado y no representa bien Order 1:N Fill. |
| PositionSyncFn | v3/core/internal/functions/position_sync.go — blob b7d8657e4a38126afc591b7fea0706512ffade79 | Replica el estado físico observado de posiciones activas y elimina las ausentes. | PositionSnapshot reportado por execution edge; persiste active_positions en PostgreSQL. | Evidencia fuerte de que Position es estado físico/reconciliado, no la intención lógica de una Operation. |
| TradeJournalFn | v3/core/internal/functions/trade_journal.go — blob d37a6bd10ce9898944988ce374aa2ae2619b5cdf | Ledger OPEN/CLOSED/FAILED para reference, executions, native/import y cierres; alimenta analytics/Lab. | PostgreSQL echo.trade_journal + quarantine; TradeJournalEntry en SDK. | Test SQL/mock blob 0c4bed93. Debe preservarse como boundary analítico, no elevar la fila del journal a aggregate Operation. |
| ReferenceEvent | v3/sdk/domain/reference_event.go — blob 7d514a79ad0fc8aafb35877ad45a3679cf16ede1 | Evento de una operación ya ejecutada en cuenta reference: trae account, broker, ticket, lot, precio, SL/TP, MM metadata. | TradeID + ReferenceAccountID + ReferenceTicket. | No cumple frozen Signal: contiene sizing/account/provider/execution y carece de MARKET/LIMIT/STOP como intención. |
| CoreCommand | v3/sdk/domain/reference_event.go — mismo blob | DTO de comando por execution account: lot, broker symbol, SL/TP físicos, delay y metadata. | CommandID + TradeID + ExecutionAccountID; enviado a edge. | Es transporte/comando, no Order aggregate. Puede adaptarse como wire DTO. |
| ExecutionResult | v3/sdk/domain/reference_event.go — mismo blob | Resultado éxito/fallo de un comando, ticket y un FillPrice. | CommandID + TradeID + ExecutionAccountID + ticket. | Colapsa lifecycle a single result; no modela múltiples fills parciales ni eventos de cambio de orden. |
| ExecutionPolicy | v3/sdk/domain/execution_policy.go — blob 295f7ea2c6058d05540988eea23c1c2d5e5cfa84 | Asociación strategy→execution account con fixed lot/risk, offsets, delays, magic override y StrategyDefinition. | StrategyID + ExecutionAccountID + version. | Es el precursor más cercano a AccountStrategy, pero mezcla binding, risk/MM y knobs de ejecución. |
| OpenExecution / CloseCommand / CloseResult | v3/sdk/domain/trade_close.go — blob 3ffe13e69d993cbaecba6f2107017230c247e42d | OpenExecution representa posición abierta derivada de un command; CloseCommand cierra ticket/lot y CloseResult reporta cierre enriquecido. | CommandID / TradeID / ExecutionAccountID / ExecutionTicket. | CloseCommand ya comenta cierre parcial como futuro; no existe Order lifecycle general. |
| PositionSnapshot | v3/sdk/domain/position_snapshot.go — blob 443b6ba2f27ad4468fd45d372c254471a1a073a1 | Estado físico actual: ticket, symbol, qty/lot, avg/open price, PnL, SL/TP, origin, strategy/ref trade. | AccountID + Ticket/platform position; snapshot periódico. | Test blob 4db2e28f. Reusar como reconciled physical position, extendido a Contract/provider semantics. |
| AccountSnapshot / InstrumentSnapshot | v3/sdk/domain/snapshots.go — blob d319d0a3587a3d5ec56ed68911cd60d86b096da8 | Estado de cuenta y specs de símbolo/broker: bid/ask, tick, lot, stop level, contract size. | AccountID; Broker + CanonicalSymbol. | Buenos primitives; InstrumentSnapshot aún mezcla instrumento económico y símbolo físico de broker y no tiene expiry/exchange/session. |
| TradeJournalEntry | v3/sdk/domain/trade_journal.go — blob 99a4f809678742f60916b25c4caff140dce8c393 | Ledger por cuenta con strategy/ticket/symbol/side/size/open-close/risk/PnL/source/status. | TradeID + AccountID + ticket y source. | REUSE/EXTEND para Lab; falta provenance explícita de replay/backtest/run_id para futuro runtime compartido. |
| Bridge V3 | v3/bridge/internal/bridge.go — blob 53cbcfe8b33b09a1586f0c599c3c31524fdd4937 y config_cache.go blob 1f461333... | Edge Windows: register, Named Pipes, sessions, hot ClientConfig, Kafka, snapshots/results, symbol mapping y telemetry. | Bridge/process + execution account sessions; Kafka/Kache y local caches. | Reutilizar host/control/reconciliation patterns; adapter actual es MetaTrader-specific. |
| Gateway V3 | v3/gateway/internal/server.go — blob 2987db5c5b8b74ff066b8278add3d07410c13bee | Control plane Hasura/Postgres/Kafka: config, webhooks, close/manual actions. | HTTP/Hasura events; Kafka topics. | REUSE/EXTEND; no debe convertirse en market-data hot path. |
| Hot symbol mapping | v3/gateway/internal/symbol_mapping_handler.go — blob a9364d4a8e40a13bb4562b2870784545293a39c5 | Hasura/Postgres update → Kafka compactado → Bridge cache. | Key broker:symbol; canonical_symbol payload; tombstones para delete. | Patrón hot-update reutilizable. Futures necesita canonical Instrument→physical Contract, no sólo broker symbol rename. |
| Day boundary | v3/core/internal/functions/account_sync.go — blob b0f8f1ce426ce9f5ac6285bd97a990624bd6ca9e | Detecta reset diario por timezone/reset time para reglas/account HWM. | Cache por accountID; fallback UTC 23:00. | NO es TradingSession/calendar: no expresa exchange holidays, early close, product hours ni DST-aware session templates de mercado. |

### REUSE / EXTEND / ADAPT / REPLACE / NEW / DEFERRED_DEBT

| Modelo candidato | D1 disposition | Base física / motivo |
| --- | --- | --- |
| Strategy | NEW | StrategyConfig/StrategyDefinition son metadata/policy, no runtime ejecutable. Reusar sólo IDs/config helpers. |
| Signal | NEW | Frozen contract distinto de ReferenceEvent. Puede existir adapter legacy ReferenceEvent→compatibility path, pero no contaminar Signal. |
| AccountStrategy | ADAPT | Extraer binding explícito desde ExecutionPolicy; mantener version/config hot. |
| CapitalManagement | ADAPT + EXTEND | Reusar SDK mm calculators y parte de MMEngine; agregar lifecycle stateful de Operation y callbacks de Bar/event/fill. |
| Operation | NEW | Reusar correlation/fan-out mechanics, no usar TradeID actual como semántica completa por accidente. |
| Order | NEW | CoreCommand queda como DTO de transporte; hace falta aggregate/lifecycle normalizado. |
| Fill | NEW | ExecutionResult debe adaptarse a emitir facts de fill; un Order puede producir múltiples fills. |
| Position | ADAPT + EXTEND | Reusar PositionSnapshot/PositionSync como physical/reconciled state; añadir Contract/provider/venue identity. |
| Trade | EXTEND | Preservar trade_journal/The Lab; definir Trade lógico cerrado y proyectarlo al ledger. |
| Account | REUSE + EXTEND | Reusar account/snapshots/rules plumbing; añadir provider/program/trader scope cuando corresponda. |
| Provider | NEW | Broker actual no representa prop firm ni policy owner. |
| ProviderProgram | NEW | Reglas cambian por programa y fase dentro del mismo provider. |
| ProviderRuleSet | NEW/ADAPT | Reusar day-boundary/risk-rule primitives donde sean genéricos; typed rule set versionado es nuevo dominio. |
| Instrument | EXTEND | Partir de canonical symbol/specs; representar root/economic instrument independiente del contrato vigente. |
| Contract | NEW | Expiry/physical futures contract y provider/platform contract id no existen como entidad separada. |
| Bar | NEW | No existe un market-data/bar engine canónico en Echo V3. |
| Session | NEW | DayBoundary de account no sirve como exchange TradingSession/calendar. |

REPLACE explícito: ExecutionStore no debe seguir siendo autoridad del nuevo lifecycle si D2 confirma Operation→Order→Fill. Puede sobrevivir temporalmente como compatibility/reconciliation projection durante migración. No requiere reescribir Core.

## 2B. Manager review — B2 Feed Authority / Recovery — 2026-09-26

Formal worker artifact: `main/30-resources/futures/MARKET DATA + QUANT ENGINE FORENSICS V2.md`.

`B2_FEED_AUTHORITY_RESEARCH = ACCEPTED_WITH_CORRECTIONS`.

Accepted:
- CME dual-feed A/B arbitration is evidence for redundant equivalent-source handling.
- CME sequence/recovery/snapshot primitives establish concrete gap/recovery patterns.
- Databento heartbeats, reconnect callbacks, intraday replay, natural refresh and MBO snapshots establish concrete liveness/recovery mechanisms.
- Databento recovery recipe (`ts_event` + count per schema/instrument + duplicate filtering) is sufficient evidence that recovery can be deterministic without generic event sourcing.

Corrections:
- Databento exposes original venue `sequence`; worker statement denying visible sequence is false.
- CME MDP 3.0 has Admin Heartbeat messages; worker statement denying explicit heartbeat is false.
- Timestamp discontinuity alone is not a gap detector.
- Fixed “no ticks in X seconds” is not a universal health rule; liveness/freshness must account for session/schema.
- Do not assume CME recovery is only startup/rest-time.
- Do not freeze “closed bars never corrected” from this corpus.
- Final OWNER questions in B2 are technical D2 decisions unless implementation exposes a real product/operability trade-off.

D2 requirement inputs:
- explicit logical authority per canonical stream;
- equivalent-feed arbitration allowed within one authority;
- heterogeneous source switching explicit, never silent blending;
- health dimensions separated: connection/session liveness, continuity/gap evidence, market freshness;
- adapter-specific recovery;
- readiness barrier after recovery;
- reconstructable affected hot state;
- source/recovery provenance sufficient for diagnosis.

**Front B final:** `D1_MANAGER_REVIEW_CLOSED`.

## 2A. Manager review — formal Front B research — 2026-09-26

Formal worker artifact: `main/30-resources/futures/MARKET DATA + QUANT ENGINE FORENSICS.md`.

`B_MARKET_DATA_RESEARCH = ACCEPTED_WITH_CORRECTIONS`.

Accepted evidence/patterns:
- normalized market events before Strategy;
- bounded hot state in-memory; durable history separate;
- one market stream can fan out to multiple strategies without work per account;
- incremental bars/indicators;
- explicit event-time semantics and warmup;
- same Strategy/domain code can be reused across live/backtest while adapters/clock/execution/reconciliation differ;
- source precedence is a valid authority pattern.

Manager corrections:
- LEAN supports multiple providers with explicit precedence; do not state “single provider only”.
- LEAN can build larger bars from smaller bars and exposes working/current consolidator state.
- forming bars are allowed when explicitly requested; the prohibition is accidental look-ahead, not forming data itself.
- Nautilus cache backing is recovery/persistence, not distributed coherent hot cache, and does not restore bounded market-data histories.
- do not claim deterministic live behavior, per-instrument message-bus buffering, adapter sorting of out-of-order data, automatic readiness or automatic feed failover without source evidence.
- do not infer that Echo needs an event store.
- 100–200 account claims in the report are design heuristics, not capacity evidence.
- feed sharing is already an Echo requirement; StateFun-vs-other ownership is D2 technical design.

Readiness:
- Q4 = `D1_INPUT_SUFFICIENT_FOR_D2`
- Q5 = `D1_INPUT_SUFFICIENT_FOR_D2_WITH_CORRECTIONS`
- Q14 = `D1_INPUT_SUFFICIENT_FOR_D2`
- Q8 = `TARGETED_RESEARCH_REQUIRED`

## 2. Market-data / quant engine scouting — PRELIMINARY

Este bloque fue **scouting de patrones e implementaciones maduras**, no selección de arquitectura ni research suficiente para cerrar el frente. La intención correcta para D1 es usarlo como seed y preparar un deep research dedicado que extraiga patrones implementables para Echo: ownership de state, tick ingestion, bar aggregation, MTF, warmup/recovery, durable history, live/replay equivalence, latency y feed authority.

### Sistemas contrastados preliminarmente

1. QuantConnect LEAN.
   - Warm-up usa historia y fast-forward del mismo algoritmo; live y backtest preparan state antes de habilitar trading.
   - Consolidators agregan ticks/small bars a bars mayores; RollingWindow guarda estado reciente.
   - Live multiple data providers usa precedence order; no mezcla feeds arbitrariamente.
   - Continuous futures mapping expone el physical mapped contract y eventos de symbol change; para live se recomienda ordenar el contrato físico.
   - Referencias:
     - https://www.quantconnect.com/docs/v2/writing-algorithms/historical-data/warm-up-periods
     - https://www.quantconnect.com/docs/v2/writing-algorithms/consolidating-data/getting-started
     - https://www.quantconnect.com/docs/v2/writing-algorithms/indicators/rolling-window
     - https://www.quantconnect.com/docs/v2/writing-algorithms/historical-data/live-trading
     - https://www.quantconnect.com/docs/v2/writing-algorithms/universes/futures
     - https://www.quantconnect.com/docs/v2/writing-algorithms/datasets/quantconnect/us-futures-security-master

2. NautilusTrader.
   - Cache central in-memory guarda order books, bounded quotes/trades/bars, orders, positions, accounts e instruments; DataEngine actualiza antes de handlers de estrategia.
   - BarType explicita instrument + aggregation + price type + source; Bar separa ts_event/ts_init.
   - Backtest usa los mismos core components/strategies/execution algorithms que live; las diferencias live quedan en venue, transport, timing, persistence y reconciliation.
   - Live execution reconciliation alinea estado interno con venue en startup y recupera missing events.
   - ParquetDataCatalog separa durable historical data del hot state.
   - Referencias:
     - https://nautilustrader.io/docs/latest/concepts/cache/
     - https://nautilustrader.io/docs/latest/concepts/data/bar/
     - https://nautilustrader.io/docs/latest/concepts/backtesting/
     - https://nautilustrader.io/docs/latest/concepts/execution/reconciliation/
     - https://nautilustrader.io/docs/latest/getting_started/backtest_high_level/
     - https://nautilustrader.io/docs/latest/how_to/loading_external_data/

### Patrones maduros extraídos para D2

- Hot state acotado e in-memory; durable historical store separado.
- Un owner determinístico de estado por instrument/stream/partition; evitar shared mutable state arbitrario entre Strategy instances.
- Tick/quote/trade normalizado primero; BarBuilder stateful después; indicadores incrementales se alimentan del mismo stream.
- Multi-timeframe derivado explícitamente de una fuente canónica o de barras menores, con BarType/source y boundary claro.
- Warm-up/recovery debe reconstruir exactamente el state necesario antes de habilitar nuevas señales; no ejecutar History queries lentas en hot path.
- Forming bar y closed bar son eventos distintos; el timestamp que hace visible una barra completa debe impedir look-ahead.
- Feed PRIMARY/BACKUP: una sola autoridad de decisión en un instante; failover explícito con gap/latency/contract checks. Precedence es preferible a mezclar ticks heterogéneos.
- Restart live: durable history + gap fill + reconciliation de venue; snapshots pueden optimizar, no reemplazar la autoridad externa.
- Live/replay equivalence significa compartir Strategy/CapitalManagement/domain callbacks y semántica temporal, no forzar el mismo process/runtime físico.
- Error frecuente: usar un continuous future como orden física o permitir que un mapping cambie el target de una Operation ya viva.

### Inputs que D2 ya tiene

D2 puede decidir Q4/Q5/Q8 con un menú concreto de trade-offs: owner del hot state, input granularity, bar timestamp/finality, indicator storage, MTF derivation, warm-up contract, durable store, primary/backup policy y recovery semantics. No requiere otro discovery general.

## 3A. Manager review — formal Front C research — 2026-09-26

Formal worker artifact: `main/30-resources/futures/FUTURES PROP UNIVERSE — FIRST-PARTY DOMAIN FORENSICS.md`.

`C_PROP_UNIVERSE_RESEARCH = BLOCKED_EVIDENCE`.

The worker draft is not accepted as the authoritative provider corpus.

Material failures:
- required relevant providers omitted: TradeDay, Tradeify, Alpha Futures, TakeProfitTrader;
- direct first-party contradictions on automation status for Lucid and MFFU;
- false claim that no researched provider explicitly forbids bots;
- false claim that Topstep does not document trader API access;
- fewer than five actually verified automatable candidates;
- no claim-level source/date evidence packet despite mandate;
- unsupported “plausible / implied / known internally” API/platform conclusions;
- platform support conflated with developer/API entitlement.

Manager revalidation confirms the preliminary D1 seed was materially more accurate on these points and supplies direct first-party anchors for repair.

Reusable from worker draft only as candidate taxonomy:
- Provider + Program/Phase requirement;
- rule families;
- account/trader/household/cross-account/cross-provider scope dimension;
- runtime-vs-economics distinction.

Not authoritative until repair:
- provider automation matrix;
- program/fase values;
- platform/API matrix;
- technical feasibility cohort;
- exclusion/block list.

Q10 domain model = `D1_INPUT_SUFFICIENT_FOR_D2`.
Front C operational corpus = `REPAIR_REQUIRED_BEFORE_D`.
Front D remains blocked by corrected C output.

### 3B. Manager review — Front C repair V2 — 2026-09-26

Artifact: `main/30-resources/futures/FUTURES PROP UNIVERSE — FIRST-PARTY DOMAIN FORENSICS V2.md`.

`C_PROP_UNIVERSE_RESEARCH = BLOCKED_EVIDENCE`.

The repair failed again. Current first-party evidence directly contradicts V2 on Topstep, MFFU, FundedNext, Tradeify, TakeProfitTrader and TradeDay. V2 also failed to produce the requested claim-level evidence appendix and still uses unsupported inference language.

However, provider discovery is no longer needed to justify the D2 domain dimension:
`Provider + Program/Phase + versioned RuleSet` is sufficiently evidenced.

Remaining blocker is narrower:
authoritative `ProviderProgram -> automation -> platform -> connectivity -> API entitlement` matrix for Front D.

### 3C. Manager review — Authoritative Evidence Matrix — 2026-09-26

Artifact: `main/30-resources/futures/FUTURES PROP UNIVERSE — AUTHORITATIVE EVIDENCE MATRIX.md`.

`C_PROP_UNIVERSE_RESEARCH = ACCEPTED_WITH_MANAGER_CORRECTIONS`.

Formal defects remain in the worker artifact:
- contradiction ledger falsely says V1/V2 were unavailable;
- evidence appendix references [N] rather than literal URLs per claim;
- Lucid and Tradeify were left UNKNOWN despite first-party sources supplied by the mandate;
- some connectivity labels remain inferred rather than proven.

Manager directly revalidated the first-party anchors and corrected the operational matrix:
- Topstep sim/Express: automation + ProjectX API allowed conditionally; Live Funded ProjectX API forbidden.
- Lucid: automation/trade copiers allowed; CQG and Rithmic platform families first-party confirmed; direct API entitlement UNKNOWN.
- MFFU: own automated strategies allowed conditionally; HFT/sim-fill exploitation forbidden.
- TradeDay: ATS allowed through supported platforms; direct platform/Tradovate API forbidden; purchased third-party bots forbidden.
- FundedNext: bots/EAs allowed in Challenge and FundedNext Accounts; latency abuse/order flooding forbidden.
- Tradeify: bots conditional on sole ownership/exclusive Tradeify use/no-HFT; cross-firm use forbidden; Tradovate/Rithmic/WealthCharts platform families confirmed; direct API entitlement UNKNOWN.
- Alpha: full automation forbidden.
- TakeProfitTrader: bots/algo execution forbidden across Test/PRO/PRO+.

This is sufficient to feed transport feasibility research without pretending UNKNOWN API entitlements are allowed.

**Front C final = `D1_MANAGER_REVIEW_CLOSED`.**
**Front D = `READY_TO_EXECUTE`.**
Q10 remains `D1_INPUT_SUFFICIENT_FOR_D2`.




## 3. Futures Prop Universe — PRELIMINARY BREADTH SAMPLE

La cohorte siguiente fue investigada demasiado pronto por el manager y **NO sustituye** el track [[Echo Futures — Futures Prop Universe]]. Debe tratarse como seed/evidencia preliminar para preparar deep research first-party amplio y reproducible.

### Cohorte preliminar

| Provider | Automation | Programa/fase relevante | Platforms / technology | Restricción material para el domain |
| --- | --- | --- | --- | --- |
| Topstep | ALLOWED con scope | Trading Combine / Express sim; Live Funded distinto | TopstepX → ProjectX Gateway REST + SignalR | API permite bots, pero order flow debe originar en dispositivo personal: no VPS/VPN/remote relay. ProjectX API no disponible para Live Funded. Flat diario y holiday early-close rules. |
| Lucid Trading | ALLOWED | LucidDaily/Flex/Pro/Direct/Live varían | NinjaTrader/Tradovate CQG y Rithmic ecosystem | Automation/copy permitted; HFT/microscalping restrictions. News y drawdown cambian por programa/fase; Live puede usar límites/scaling distintos. |
| MyFundedFutures | ALLOWED / CONDITIONAL | Builder/Rapid/Pro + sim-funded/live | NinjaTrader, Tradovate, TradingView y otros | Automated strategy propia permitida, HFT/sim-fill exploitation prohibido. News restrictions pueden cambiar por plan/fase; EOD vs intraday drawdown. |
| TradeDay | ALLOWED / CONDITIONAL | Eval/funded según programa | NinjaTrader, Tradovate, TradingView, Jigsaw, Quantower; CQG/Rithmic ecosystem | Bots permitidos vía plataformas soportadas, pero NO entrega platform APIs/Tradovate API; third-party purchased bots prohibidos. |
| FundedNext Futures | ALLOWED | Challenge + FundedNext Account; varios modelos | Integraciones conectadas a Tradovate; NinjaTrader/Tradovate/TradingView | Bots permitidos; latency abuse/order flooding/HFT prohibidos. Copy sólo entre cuentas del mismo owner; DCA permitido con plan estructurado. Consistency cambia por modelo/fase. |
| Tradeify | CONDITIONAL | Eval/sim funded según plan | Tradovate, Rithmic, WealthCharts; NinjaTrader disponible con Tradovate | Bot sólo si se prueba sole ownership y nadie más/otra firma usa la misma estrategia; similarity scans/video. Hedging/correlated products y microscalping/payout constraints. |
| Alpha Futures | FORBIDDEN para full automation | Evaluation/Qualified | Varias plataformas, copy manual posible | AI/bots/full automation prohibidos; semi-auto signals con ejecución/gestión manual sí. |
| TakeProfitTrader | FORBIDDEN | Test/PRO/PRO+ | Transport irrelevante para V1 automatizado | Universal policy: no bots/algo; manual execution. |

### First-party evidence principal

- Topstep API: https://help.topstep.com/en/articles/11187768-topstepx-api-access
- Topstep trading times: https://help.topstep.com/en/articles/8284206-when-and-what-products-can-i-trade
- Topstep holidays: https://help.topstep.com/en/articles/13350348-topstep-holiday-trading-hours
- Lucid automation: https://support.lucidtrading.com/en/articles/11404728-other-trading-activities
- Lucid times: https://support.lucidtrading.com/en/articles/11404729-allowed-trading-times
- Lucid drawdown example: https://support.lucidtrading.com/en/articles/15998425-luciddaily-drawdown
- MFFU automation: https://help.myfundedfutures.com/en/articles/8444599-fair-play-and-prohibited-trading-practices
- MFFU platforms: https://help.myfundedfutures.com/en/articles/8528335-overview-of-supported-platforms-at-mffu
- MFFU news: https://help.myfundedfutures.com/en/articles/8230009-news-trading-policy
- TradeDay automation/API: https://tradeday.freshdesk.com/en/support/solutions/articles/103000085101-automated-algo-and-bot-trading
- FundedNext automation: https://helpfutures.fundednext.com/en/articles/14298560-is-the-usage-of-automated-trading-systems-eas-and-bots-allowed-in-fundednext-futures
- FundedNext copy: https://helpfutures.fundednext.com/en/articles/14298572-what-is-copy-group-trading-policy-at-fundednext-futures
- FundedNext general futures rules: https://fundednext.com/general-rules/futures/what-is-allowed
- Tradeify rules: https://help.tradeify.co/en/articles/10468318-guidelines-for-traders
- Tradeify platforms: https://help.tradeify.co/en/articles/10468221-supported-platforms
- Alpha automation: https://help.alpha-futures.com/en/articles/9508585-prohibited-trading-practices
- TPT no algo: https://takeprofittraderhelp.zendesk.com/hc/en-us/articles/34431153546397-TakeProfitTrader-Universal-Trading-Policies-UTP

### Rule families demostradas

ProviderRuleSet/ProgramRuleSet debe poder representar al menos:
- automation permission + automation ownership/exclusivity;
- lifecycle/environment: evaluation, sim-funded, live, transition;
- platform/API entitlement;
- trader/account/household/cross-provider scope;
- max position/contracts + product groups;
- MLL/drawdown: fixed, EOD trailing, intraday trailing, lock;
- daily loss: hard/soft/optional;
- consistency/profit contribution;
- trading day/min days/inactivity;
- allowed sessions, forced flatten, holiday early-close;
- news windows;
- HFT/microscalping/min-hold/order-frequency/system-exploitation;
- DCA/scaling/martingale semantics;
- hedging/correlated product restrictions;
- copy/group/cross-provider restrictions;
- payout eligibility/caps/splits;
- account-count limits;
- allowed instruments/exchanges;
- rule severity: deny new risk, soft pause, hard breach, forced flatten.

Conclusión de domain discovery: Provider no alcanza. Program/fase modifica reglas materialmente dentro del mismo provider, por lo que D2 debe mantener Provider + ProviderProgram + versioned RuleSet. Esto es evidencia para diseñar, no freeze de la forma exacta.

## 4. Execution transport feasibility — PRELIMINARY

### ProjectX / TopstepX direct

- REST order API + SignalR/WebSocket realtime.
- MARKET/LIMIT/STOP explícitos; además stop-limit/trailing/join.
- cancel y modify endpoints.
- user hub entrega account/order/position/trade events; market hub quote/trade/depth.
- Order trae fillVolume; Trade es un hecho separado con orderId, size y price.
- ejemplo oficial usa automatic reconnect y resubscribe.
- rate limit actual: history 50/30s; otros endpoints 200/60s.
- Topstep autoriza bots en sim/Express/Combine por esta API, pero no Live Funded y prohíbe que order flow venga desde VPS/remote server.
- Ruta V1 técnicamente viable: shadow/demo/sim autorizado desde máquina personal/edge local.

Refs:
- https://gateway.docs.projectx.com/docs/api-reference/order/order-place/
- https://gateway.docs.projectx.com/docs/realtime/
- https://gateway.docs.projectx.com/docs/getting-started/rate-limits/
- https://help.topstep.com/en/articles/11187768-topstepx-api-access

### NinjaTrader local bridge

- OnExecutionUpdate define execution == fill; una orden puede producir múltiples executions/partial fills.
- Account/NinjaScript APIs proveen order/account events y command path; Sim101 entrega una cuenta simulada realista.
- Encaja como adapter local para varias props que permiten automation y soportan NinjaTrader: Lucid, MFFU, TradeDay, FundedNext.
- D1 no afirma que la misma licencia/conexión funcione en toda prop: ese entitlement es provider/program data.
- Ruta técnicamente viable en sim y candidata fuerte a multi-provider reuse; D2 debe decidir si vale el costo C#/NT bridge frente a APIs directas.

Refs:
- https://docs.ninjatrader.com/ninjascript/onexecutionupdate
- https://ninjatrader.com/support/helpGuides/nt8/the_sim101_account.htm

### Tradovate direct API

- REST + WebSocket/market-data services, demo engine separado y order placement.
- Es technology común en varias props.
- No asumir portabilidad del API entitlement: TradeDay declara explícitamente que no expone Tradovate API; para otras firmas el login de plataforma no prueba developer API.
- D2 puede mantenerlo como transport family, condicionado a entitlement por ProviderProgram.

Refs:
- https://api.tradovate.com/
- https://partner.tradovate.com/api/rest-api-endpoints/orders/place-order
- https://tradeday.freshdesk.com/en/support/solutions/articles/103000085101-automated-algo-and-bot-trading

### Rithmic direct

- R|API+ C++/.NET y R|Protocol language-agnostic; market data, reference, order management y execution reports.
- Exchange Simulator con live exchange data + simulated fills; soporta market/limit/stop/brackets/OCO.
- Production access exige conformance; test no.
- Reutilizable potencialmente entre props Rithmic, pero credentials de plataforma no equivalen a developer entitlement.

Refs:
- https://www.rithmic.com/apis
- https://www.rithmic.com/products/exchange-simulator

### Feasibility candidate

La evidencia preliminar sugiere al menos una ruta técnicamente plausible para V1 —ProjectX simulated— y una familia reusable vía NinjaTrader, pero D1 todavía debe decidir con el owner qué profundidad de research/verification necesita antes de declarar execution feasibility cerrada. No convertir este scouting en selección de transport.

## 5. Futures semantics / inputs D2

### Instrument vs Contract

- CME futures tienen ticker/root, contract specs, expiry/month contract y trading hours.
- LEAN separa continuous symbol del physical Mapped contract y advierte que live orders deben usar el underlying physical.
- ProjectX también separa symbolId del contractId.
- Input D2: Instrument debe representar el económico/canonical root; Contract debe representar expiry/physical tradable + venue identifiers/specs.
- La propuesta de que una Operation pinnee Contract al crearse queda READY_FOR_D2: evita que un hot mapping rollover retargetee una orden/posición viva.
- Rollover automático sigue fuera V1 por owner decision; mapping manual hot sí es requerido.

Refs:
- https://www.quantconnect.com/docs/v2/writing-algorithms/universes/futures
- https://www.quantconnect.com/docs/v2/writing-algorithms/datasets/quantconnect/us-futures-security-master
- https://gateway.docs.projectx.com/docs/realtime/

### TradingSession / calendar

- Echo DayBoundary actual sólo representa reset de cuenta por timezone/hora.
- CME publica regular hours + 2026/2027 holiday schedules/early closes y los horarios varían por producto.
- Props agregan encima forced-flat cutoffs propios: Topstep 3:10 PM CT y early-close offsets; Lucid 4:45 PM ET en varias cuentas y distintos horarios live según connection.
- Input D2: Session necesita exchange/product calendar, timezone/IANA + DST, regular open/close/breaks, holiday overrides/early close y provider/program trading-window overlays. No hardcodear un UTC reset como session de mercado.

Refs:
- https://www.cmegroup.com/trading-hours.html
- https://help.topstep.com/en/articles/8284206-when-and-what-products-can-i-trade
- https://support.lucidtrading.com/en/articles/11404729-allowed-trading-times

### Order / Fill / Position / Operation

- NinjaTrader prueba que una Order puede generar múltiples Fill executions y que partial fills son normales.
- ProjectX publica Order y Trade como entidades/eventos separados; Trade referencia orderId; Position es account+contract+size+averagePrice.
- Echo actual ExecutionResult de single FillPrice no alcanza para este lifecycle.
- Evidencia lista para Q2/Q3:
  - Order necesita identity estable + status transitions + submit/change/cancel + requested qty/prices/type.
  - Fill debe ser immutable execution fact con order id, qty, price, timestamp/provider execution id.
  - Position debe reflejar estado físico neto/reconciliado del account/contract; no debe ser igual a Operation.
  - Operation sigue siendo una candidata lógica para gestionar Signal×Account y sus Orders/Fills; D2 debe confirmar cardinalidades exactas y attribution rules.
- Netting/hedging no debe resolverse con supuestos MT4. Transport reporta el estado físico real; domain debe poder reconciliarlo.

Refs:
- https://docs.ninjatrader.com/ninjascript/onexecutionupdate
- https://gateway.docs.projectx.com/docs/realtime/

### Trade → trade_journal → Lab

- Echo V3 ya tiene boundary estable: TradeJournalFn → echo.trade_journal → The Lab.
- Conservarlo evita reescribir Lab.
- D2 debe definir projection de Trade lógico cerrado hacia journal y provenance para LIVE/REPLAY/BACKTEST, source/run_id; no mezclar una simulación con live sin identificación.
- Journal es projection/ledger analítico, no state owner del live Operation.

### Backtest/replay reuse boundary

- Frozen owner constraint es compatible con patrones LEAN/Nautilus: compartir Strategy + CapitalManagement + domain event semantics y deterministic clock/event ordering.
- Live-only: feed adapters, sockets/API auth, retries/backpressure, reconciliation, provider connectivity, remote order IDs.
- Reusable pure/domain: Strategy, Signal, CapitalManagement decisions/state transitions, Operation/Order/Fill semantics, Instrument/Contract/Session normalization, ProviderRule evaluation cuando sea determinista.
- Sim-only adapter: simulated execution/fill model, slippage/commission model y historical/recorded feed.
- Esto deja Q14 READY_FOR_D2 sin exigir que backtester y Core live sean el mismo proceso.

### Event cadence para Strategy / CapitalManagement

D1 no congela callback API, pero D2 ya tiene el set completo que debe resolver:
- tick/quote/trade;
- forming bar update cuando una estrategia lo solicite;
- closed bar;
- multi-timeframe closed/forming semantics;
- fill/partial fill;
- order accepted/rejected/cancelled/replaced;
- position/reconciliation change;
- account/risk/provider rule event;
- session open/close/holiday transition;
- contract mapping update para nuevas Operations, sin mutar las ya pinned.

## 6. Blocking refactor register

### Blocking para implementar el diseño una vez que D2 lo congele

1. Signal boundary limpio separado de ReferenceEvent.
2. Operation/Order/Fill identities y lifecycle; adaptar CoreCommand/ExecutionResult como wire contracts, no domain aggregates.
3. Instrument/Contract + hot mapping semantics.
4. TradingSession/calendar separado de account day boundary.
5. CapitalManagement contract stateful sobre Operation, reutilizando MM calculators.
6. Provider/ProviderProgram/versioned RuleSet domain.
7. Trade projection/provenance para Lab live/replay/backtest.

Estos son blocking design/refactors, no evidencia de que haya que reescribir Core V3.

### Non-blocking deferred debt

- ExecutionStore puede mantenerse como compatibility projection mientras migra la autoridad al nuevo lifecycle.
- Bridge tiene patrones muy reutilizables pero adapter MetaTrader-specific; no necesita eliminarse para introducir NT/ProjectX adapters.
- Gateway/Hasura siguen como control plane; no deben entrar al hot path.
- ConfigCache consume topics compactados desde inicio: aceptable hoy; medir startup/capacity antes de escalar.
- Fan-out por account y topic/consumer topology a 100–200 cuentas requiere benchmark/capacity test, no rediseño preventivo.
- Legacy V2 source/docs pueden limpiarse después; no son prerrequisito.
- DayBoundaryCache actual no reemplaza calendar/session y su fallback UTC no debe propagarse a Futures.

## 7. Critical Questions — PRELIMINARY READINESS ONLY

| Q | Estado actual | Nota |
| --- | --- | --- |
| Q1 Echo fit | CANDIDATE_FOR_OWNER_REVIEW | Source audit preliminar existe; owner/manager debe revisarlo antes de cerrar. |
| Q2 Position attribution | OPEN_D1_INPUTS_AVAILABLE | Evidencia preliminar disponible; decisión pertenece a D2. |
| Q3 Order lifecycle | OPEN_D1_INPUTS_AVAILABLE | Evidencia preliminar disponible; completar research/transport corpus según manager. |
| Q4 Market hot state | D1_INPUT_SUFFICIENT_FOR_D2 | Formal Front B accepted with corrections; exact owner/topology remains D2. |
| Q5 Bar semantics | D1_INPUT_SUFFICIENT_FOR_D2_WITH_CORRECTIONS | Formal Front B sufficient after manager corrections; forming/closed and late/out-of-order policy remain D2 design details. |
| Q6 Contract mapping | OPEN_D1_INPUTS_AVAILABLE | Evidencia preliminar; incluir futura reutilización cross-market/FX en la discusión. |
| Q7 Session semantics | OPEN_D1_INPUTS_AVAILABLE | Evidencia preliminar; falta revisión guiada del scope requerido. |
| Q8 Feed authority | D1_INPUT_SUFFICIENT_FOR_D2_WITH_CORRECTIONS | B2 provides CME/Databento authority, liveness and recovery evidence; exact policy/topology remains D2. |
| Q9 Execution transport | READY_FOR_FRONT_D_RESEARCH | Front C operational corpus is now sufficient; formal transport feasibility research can execute. |
| Q10 Provider model | D1_INPUT_SUFFICIENT_FOR_D2 | Provider+Program/Phase + versioned RuleSet need is sufficiently evidenced; Front C operational matrix still requires repair before D. |
| Q11 Strategy runtime | OPEN_D1_INPUTS_AVAILABLE | Source audit preliminar; diseño pertenece a D2. |
| Q12 S2 | READY_FOR_D4 | Owner day permanece D4. |
| Q13 Gerard +/- | READY_FOR_D4 | Owner day permanece D4. |
| Q14 Backtest boundary | D1_INPUT_SUFFICIENT_FOR_D2 | Formal Front B supports shared domain/strategy semantics with different live/sim infrastructure. |
| Q15 Trade/Lab | OPEN_D1_INPUTS_AVAILABLE | Source audit preliminar disponible; diseño pertenece a D2. |
| Q16 Blocking refactor | OPEN_D1_INPUTS_AVAILABLE | Register preliminar; sólo se cierra después de revisar todos los frentes D1. |

No existe cierre de D1 todavía; por lo tanto no corresponde afirmar que todos los UNKNOWN relevantes están eliminados.

## 8. Evidence gaps reales

Estos gaps no bloquean D1 y están scoped para D2/implementation:

- No se hizo credentialed smoke contra ninguna prop/provider. D1 requería feasibility, no operar ni usar credenciales. ProjectX/NT simulator paths están documentados oficialmente.
- Tradovate developer API entitlement NO está demostrado para MFFU/FundedNext; login Tradovate no equivale a API key. Mantener capability UNKNOWN/conditional por ProviderProgram hasta confirmación.
- Rithmic production access requiere conformance; no se intentó solicitar kit ni credenciales.
- No se benchmarkeó fan-out 100–200 cuentas sobre Echo V3. Es capacity verification posterior, no identity/lifecycle discovery.
- No se eligió market-data vendor concreto. D2 elige architecture/capabilities; vendor procurement queda posterior si no cambia el domain.
- No se definió una tabla completa de contract rollover dates. V1 es manual rollover; D2 sólo necesita modelar Contract + mapping hot + pinned operation.
- No se reauditaron economics del proyecto histórico; no son autoridad para D1 architecture.

## 9. Reusable assets para D2

- Este D1 Analysis Pack.
- Source/domain map V3 con blob SHAs.
- Q1 reuse matrix.
- Provider cohort + first-party references.
- Rule-family catalog.
- Transport feasibility matrix.
- Market-data comparison LEAN/Nautilus.
- Futures semantics evidence set.
- Blocking/deferred refactor register.
- Terminology mapping:
  - ReferenceEvent = legacy executed-reference input, no Signal.
  - ExecutionPolicy = current binding/risk/execution config precursor, no final AccountStrategy.
  - CoreCommand = transport DTO, no Order aggregate.
  - ExecutionResult = legacy command result, no Fill aggregate.
  - PositionSnapshot = physical/reconciled state precursor.
  - TradeJournalEntry = analytical ledger projection, no Operation aggregate.

## 10. Reusable behavior candidates

- **technical-project-manager manager/worker boundary**: esta sesión demostró un defecto concreto en la skill. El manager ejecutó discovery/research y autoavanzó el gate en vez de coordinar con el owner. La skill fue corregida el 2026-09-25 para obligar manager mode, owner checkpoints, global→detalle, delegación mediante master prompts y no self-accept.

## 11. Gate status after owner correction

D1 no está cerrado.

Trabajo útil preservado:
- source/domain audit preliminar de Echo V3;
- primera matriz REUSE/EXTEND/ADAPT/NEW;
- scouting LEAN/Nautilus;
- muestra preliminar de futures props;
- scouting de transports;
- primeras hipótesis de futures semantics y refactors.

Trabajo que debe continuar bajo conducción owner+manager:
- recorrer D1 globalmente y acordar orden de frentes;
- revisar Q1 con el owner antes de cerrarla;
- Front B market-data research + B2 feed-authority review = CLOSED for D1;
- ejecutar el track Futures Prop Universe como research formal, no como muestra improvisada;
- research de execution transports apoyado en el corpus real de props;
- revisar futures semantics y backtest boundary contra esos outputs;
- revisar blocking/deferred debt;
- ejecutar checklist D1 completo y recién entonces proponer `EF_D1_ANALYSIS_PASS = REVIEW`.

Next exact milestone: **continuar D1 — manager-guided Problem + Domain Discovery**.
