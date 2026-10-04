---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo Futures]]"
  - "[[Echo Futures — BT-S00 Backtester Source Forensics and Architecture Direction]]"
aliases:
  - Echo Futures BT-S01
tags:
  - kind/doc
  - project/echo-futures
  - topic/backtester
created: "2026-10-03"
updated: "2026-10-04"
---

# Echo Futures — BT-S01 Backtester V1 Design

## Propósito

### 0. Dictamen y alcance de esta entrega

**BT-S01, integrado con BT-S01A, queda listo para freeze del Primary Technical Manager y un único BT-S02 de implementación, con cero decisiones materiales de Owner abiertas.** Backtester V1 ejecuta una cuenta y un instrumento lógico a través de múltiples contratos físicos, secuencialmente, sobre las autoridades compartidas de Echo Futures. El driver histórico ordena las causas; SimExecution produce hechos físicos; una autoridad económica de cuenta actualiza lo que GerardMM y Provider observan antes de la siguiente decisión.

La arquitectura central de BT-S01 fue aceptada por Manager. BT-S01A corrige exclusivamente rollover longitudinal, MM de horizonte arbitrario, continuidad de contexto/cashflows, desacople del dataset y parity de hecho+economía. No se implementó product code, no se ejecutaron tests de Echo, no se inició BT-S02 y no se modificó ni certificó D6. Las pruebas descritas son trabajo obligatorio posterior, no evidencia de pruebas ya aprobadas.

### 0.1 Baseline inmutable y precedencia

| Autoridad | Baseline revisado | Consecuencia |
| --- | --- | --- |
| Agents-OS, proyecto y BT-S00 aceptado | `xKoRx/agents-os@b999eb3ea2a9a9d2ded574e891e3f8bec8c275c2`, `master` | Autoridades vigentes y entrada aceptada por Manager. |
| Echo Futures activo | `xKoRx/echo@d361008bfe4aa54fe3d8b6380d290bf92e1f1c08`, `feature/d6-shot1-execution-vertical` | Mismo baseline de BT-S00; no apareció un delta material en esa rama al refrescarla. |
| Echo `master` | `372af59a7b83604781346613da01e3d510ea1360` | Rama anterior al trabajo D6; no se utilizó como supuesto avance del baseline. |

**SOURCE FACT.** La revisión combinó source inmutable y autoridades D2/D4/D5/D6; se verificó la integridad Git blob de 190 archivos seleccionados de Echo y 38 de Agents-OS. Eso acredita los archivos adquiridos, no una auditoría de todo el repositorio ni una ejecución física. [A01] [A02] [A03] [A04]

Baseline de la enmienda: BT-S01 publicado en `ab7766fd74bed760cb9a9f151bc423948bec0d3f`. [A13] Al iniciar BT-S01A, Agents-OS seguía en ese HEAD y Echo activo en d361008b; no había deltas materiales nuevos. Las autoridades D2/D4/D5/D6 referenciadas permanecen vigentes. El mandato de Manager BT-S01A de esta sesión es autoridad para reemplazar las limitaciones anteriores de V1.

En el refresh de cierre, Echo activo avanzó a `7fbd7e990ac6628df3e4cc2717e96efd83bfbbf6` y Agents-OS a `48f5260c5803c061b4f4dcabcf246897d056e19b`. El único delta de Echo corrige whitespace en el parser JSON del AddOn y su guarda; no modifica los contratos/engines compartidos citados. Agents-OS sólo añade tres artifacts de esa corrección D6. Se revisaron y se preservan, sin cambiar el alcance de BT-S01A ni actuar sobre D6. [A14] [S34]

En este documento, **OWNER / MANAGER FROZEN** identifica una restricción ya aceptada; **SOURCE FACT** identifica comportamiento o estructura comprobable en el baseline; **DESIGN DECISION** identifica la resolución técnica de BT-S01. Las secciones prescriptivas, schemas, fórmulas, secuencias y tests son DESIGN DECISION salvo indicación contraria. **OPEN OWNER DECISION: NONE.** Los parámetros exigidos a cada corrida son datos del experimento; su obligatoriedad no delega arquitectura al implementador.

## Contenido

Las secciones 1–8 fijan motor, inputs y causalidad; 9–15 fijan economía, lifecycle, ejecución y finalización; 16–20 fijan evidencia, persistencia, findings y pruebas. El último bloque es el contrato obligatorio de BT-S02.

### 0.2 Alcance integrado de BT-S01A

| Enmienda Manager | Resolución normativa |
| --- | --- |
| 1. Multi-contract/rollover | §4.3: catálogo/schedule, preparación y activación compartidas, fence de OPEN y retención del contrato anterior. |
| 2. Generic100K longitudinal | §10.1: materializador explícito de rows/selectores y ejemplo de 20 account-days. |
| 3. Same-account/context y cashflows | §11.1–11.4: controles V1, estado conservado/reemplazado y caller causal. |
| 4. Formato físico del corpus | §5.1: DatasetSource/Cursor y separación entre identidad lógica y layouts. |
| 5. Parity hecho+economía | §8.2: una transición shared y pruebas de los ingress Core e histórico reales. |

La secuencia, economía, SimExecution, result/publisher, laboratorio y protocolo BT-F01…F05 aceptados se mantienen. Los ajustes de identidad/control streaming en §13/§16 son consecuencias necesarias de permitir controles futuros del caller; no agregan workflow, campaign simulator ni otra arquitectura.

## 1. Qué construye V1

**OWNER / MANAGER FROZEN.** Hay un solo Backtest Engine. El mismo engine ejecuta Generic100K y una cuenta con reglas Provider. Strategy, S1/S2, GerardMM, Operation, Provider, admission, capacity, reservations y revalidation siguen siendo autoridades reales. Una regla económica que pueda cambiar una decisión participa durante la corrida. [A01]

**DESIGN DECISION.** Una corrida contiene una cuenta de ejecución, un instrumento lógico —NQ como fixture representativo—, una o varias configuraciones de Strategy y los contratos físicos requeridos por su schedule. Sus owners de Operation, Provider y ledger de cuenta continúan dentro del mismo run. El motor vive en `v3/backtester`; sólo importa SDK para el dominio. `Run` es una composición histórica, no otro conjunto de estrategias o reglas monetarias.

~~~mermaid
flowchart TD
    I["Dataset y controles causales"] --> D["Driver histórico"]
    D --> M["Market, Bars y Calendar"]
    M --> V["MarketContext"]
    V --> S["Strategy S1/S2"]
    S --> O["Operation + GerardMM"]
    O --> P["Provider"]
    P --> O
    O --> X["SimExecution"]
    X --> E["Economía de cuenta"]
    E --> P
    E --> O
    D --> R["Evidencia y resultado"]
~~~

El diagrama muestra autoridades y feedback; el orden exacto está en §6. La ejecución física sólo recibe comandos autorizados y comprometidos por Operation. No hay Kafka, Flink, StateFun, red de servicios ni almacenamiento remoto dentro de ese camino.

### 1.1 Límites deliberados

| Incluido en V1 | Límite explícito |
| --- | --- |
| Múltiples expiries físicos con ticks y contexto S1/S2 | Rollover sólo mediante schedule/control explícito; sin migración automática de exposición ni series continuas presentadas como físicas. |
| Cuenta USD; contabilidad exacta y economía durante el run | Sin FX, portfolio multicurrency ni consolidación multiactivo. |
| MARKET, STOP_MARKET, CANCEL, DAY/GTC | LIMIT y native MODIFY no son capacidades del modelo histórico V1. |
| Reglas tipadas, continuidad same-account y cashflows explícitos | Sin DSL de props, promoción automática, payout inferido ni bankroll dentro del engine. |
| `AdvanceUntil` sobre el mismo motor | Sin checkpoints durables ni resume distribuido. |
| Evidencia reproducible y primer punto de divergencia | Sin afirmar reproducción de infraestructura LIVE ausente del corpus. |
| Múltiples runs independientes | Paralelismo inicial entre procesos; cada run permanece secuencial. |

Rollover conserva la identidad física y evita mezclar OR/H4/BB entre expiries mediante preparación/activación por stream. El saldo, los días, las Operations y las autoridades de cuenta no se reinician al seleccionar otro contrato. Una concatenación de resultados independientes no acredita esa continuidad. [A06] [S27]

## 2. API y entrada de una corrida

La API pública del package `backtest` expone `NewRun(spec, sources, recorder)`, `AdvanceUntil(T)`, `EnqueueControl(control)` y `Finish()`. `Run(...)` ejecuta el spec cerrado mediante ese mismo loop. EnqueueControl admite sólo los controles de cuenta de §11.4; no es un scheduler genérico.

`AdvanceUntil(T)` procesa sólo causas con tiempo lógico <= T y devuelve una frontera realmente completada, después de terminar todas sus fases/efectos. No devuelve a mitad de un lote. En CALLER_CONTROLLED con AWAIT_CONTEXT puede devolver antes de T al alcanzar un outcome de etapa asentado, una vez por ese outcome, para que el caller decida un control futuro. Mantiene estado y sólo entrega observaciones <= frontera. Una pausa no es COMPLETE. Finish exige §15 y sella el conjunto de controles.

### 2.1 RunSpec V1

`RunSpec` es configuración de la ejecución histórica y composición de structs existentes. No introduce un `BacktestProfile` ni una jerarquía por prop.

| Campo | Contrato |
| --- | --- |
| `schema_version` | `echo.backtest.run.v1`. |
| `build` | Commit/tree, estado limpio o patch digest, binary SHA-256, Go version, GOOS/GOARCH, dependencias y build flags relevantes. Una publicación canónica exige identidad reconstruible. |
| `dataset` | Manifest lógico inmutable con identidad/orden/digest de registros normalizados, cobertura por stream y referencia durable de reproducción. Layout/codec pertenecen al reader externo (§5.1). |
| `warmup_start / trade_start / end_exclusive` | Instantes UTC; warmup_start <= trade_start < end_exclusive. El período operable es [trade_start,end_exclusive). |
| `config` | ConfigSnapshot compartido: una cuenta, instrumento lógico, ContractCatalog, ContractSchedule y autoridades de calendario/Strategy/MM/Provider. La forma legacy de un contrato normaliza a un catálogo/schedule de una entrada. |
| `initial_state` | Capital y estado económico explícitos; V1 exige inventario, órdenes, reservas y ciclos vacíos. Los estados técnicos nacen del warm-up. Un capsule de laboratorio no se convierte en un resume general. |
| `controls` | Controles tipados con effective_at, control_id, ordinal y payload/digest. CLOSED_SPEC los fija antes de ejecutar; CALLER_CONTROLLED admite controles futuros inmutables mediante §11.4. |
| `account_context` | context_id/stage_id, Binding/RuleSet, MM completo y rows/selectores resueltos, account-day, risk seed, términos/cobertura, cashflow treatment explícito y outcome_handling STOP o AWAIT_CONTEXT. |
| `execution_model` | Versión, fidelidad, slippage ticks, fees, edad máxima por lado y TIF vacío resuelto explícitamente. |
| `valuation_model` | `NET_FIFO_LIQUIDATION_V1`; exactitud monetaria, fuentes de bid/ask y freshness; USD. |
| `end_policy` | `REPORT_RESIDUALS` o `REQUIRE_FLAT`; esta última incluye un control de cierre anterior al horizonte. |
| `lab_fixture` | Opcional, lista finita de perturbaciones tipadas de observaciones, con coordenadas y payloads. Su digest entra en identidad. |
| `input_mode / control_namespace` | CLOSED_SPEC conserva identidad por inputs completos. CALLER_CONTROLLED exige namespace previo del caller e identidad/manifest final según §13.1. |
| `parent` | Referencias opcionales a campaign/account anterior. No aporta saldo ni eventos implícitos. |

El constructor valida configuración, compatibilidad de contrato/currency, cobertura conocida de calendarios/planes, capacidades del execution model y datos resolubles antes de ejecutar decisiones. `account_context` referencia las mismas autoridades de config por identidad/digest; no contiene una segunda RuleSet divergente. Las observaciones seed `Accounts[].Economics/Snapshot` deben coincidir con la proyección validada de initial_state o se rechazan. Durante el run, Accounting y su proyección Provider producen las nuevas revisiones; el snapshot de configuración no compite con esa autoridad. No descarga configuración cambiante a mitad de una corrida.

Las fuentes y el recorder son puertos concretos de I/O. La lógica no recibe credenciales, SDK de storage, reloj de pared ni clientes de transporte. Un recorder fallido aborta con evidencia; no se continúa una corrida que ya perdió su trazabilidad.

## 3. Ownership del estado y commit

| Estado | Dueño durante el run | Regla |
| --- | --- | --- |
| Reloj, cursor, controles, timers, cola inmediata | Driver | Un escritor secuencial. |
| Secuencia/identidad, autoridad, ladders, readiness | Shared Market | El driver no canonicaliza por su cuenta. |
| Builders, sesiones, demandas, cierres y timers analíticos | Shared Analytics/Bars/Calendar | Una construcción de barras compartida. |
| Proyecciones actuales y rings acotados | Shared MarketContext feed | Vistas sólo de lo ya comprometido. |
| Estado técnico y dedup de cada Strategy | Shared Strategy owner | Copia de trabajo antes de Handle/config. |
| Operation, órdenes, fills lógicos, MMState, claims, IDs | Shared Operation owner por account-strategy | Cambian sólo con Apply exitoso. |
| Binding/RuleSet, exposición/grants/reservas y safety | Shared Provider por cuenta | Capacidad y autorización definitivas. |
| FIFO físico, costes, balance/equity, baselines diarios | Shared Accounting por cuenta | Los fills físicos netean por account+contract. |
| Floors, breaches y lifecycle del programa | Funciones compartidas Provider + estado económico de cuenta | Datos/risk state versionados; no decisiones dentro de SimExecution. |
| Órdenes físicas, matches y observaciones pendientes | SimExecution | No posee MM, sizing ni capacidad Provider. |
| Evidencia y agregados | Recorder del run | Observa; no decide. |

**SOURCE FACT.** Operation y Provider trabajan sobre clones. Strategy muta el estado recibido. Por eso el caller debe clonar Strategy y sus cambios de configuración antes de invocarlo; extender el patrón de Operation por suposición no basta. [S07] [S09] [S14]

Cada callback calcula next-state y effects en memoria; al éxito se comprometen y se emiten en su orden original. Para un fill o quote correlacionado, las pocas estructuras afectadas —economía, Provider snapshot y Operation— se preparan como candidatos y se confirman antes de liberar efectos dependientes. No se requiere un transaction manager.

SimExecution fija hechos físicos antes de su entrega. Si falla la transición de un fill ya fijado, la corrida termina FAILED: el capsule conserva los hechos sellados todavía no aplicados y los últimos estados comprometidos. No se declara que desapareció el fill ni se reanuda sobre ese estado parcial.

Config, initial state, mapas y slices se copian profundamente por corrida. No se comparten pointers mutables, scopes, contadores, callbacks o caches entre A/B/A. Los estados de dominio mantienen sus límites existentes; la evidencia se escribe por streaming. Los índices de dedup físico/correlación de toda la corrida pueden crecer con sus órdenes/fills y se miden; no se evictan con una heurística que permita volver a cobrar un fill antiguo.

## 4. Packages y extracción compartida

**SOURCE FACT.** Parte material de Market y Analytics sigue en shells `core/internal/functions`; el feed de MarketContext y la composición congelada están en `core/internal/futuresruntime`. El harness vertical y el bridge simulator son fixtures útiles, pero no implementan por sí solos este motor causal histórico. [S01] [S02] [S03] [S19]

### 4.1 Layout decidido

| Target | Trabajo concreto |
| --- | --- |
| `v3/backtester/go.mod` | Módulo `github.com/xKoRx/echo/v3/backtester`; mismo toolchain del repo; dependencia SDK y adapter S3 cuando corresponda. |
| `v3/backtester/{run,spec,driver,controls,dataset,experiment_plan,economics_views,result,evidence,reproduce}.go` | Package público backtest: composición, loop, reader ports, materialización previa, controles de cuenta, proyecciones y reproducción. |
| `v3/backtester/internal/datasets/ndjson` | Primer adapter físico para fixtures/corpora disponibles; depende del port y lo compone la CLI. El engine no lo importa ni conoce extensión/codec. |
| `v3/backtester/internal/simexecution` | Venue histórico determinista de §12; sólo SDK. |
| `v3/backtester/internal/artifactstore` | Finalización local, checksum y publicación condicional. |
| `v3/backtester/cmd/echo-backtest` | Comandos `run`, `reproduce`, `publish`. CLI estrecha sobre los mismos packages. |
| `v3/backtester/testdata` | Ticks/controles pequeños, manifests, Generic y GAU50 modelados, trazas lab. |
| `v3/sdk/futures/market/{engine,owner_state,effects}.go` | Extraer transiciones/state de `futures_market_stream.go`; reutilizar StreamSequencer, guard, ladders, readiness, journal/recording existente. |
| `v3/sdk/futures/analytics/{engine,state,effects}.go` | Extraer `futures_market_analytics.go`: builders, calendario, demands, subscribers, quote routes y timers. |
| `v3/sdk/futures/marketctx/feed.go` | Mover ReadModelFeed, StreamStateFeed, boundedBarStore y feedReadModel desde `views.go:187–407`. |
| `v3/sdk/futures/config` | Mover ConfigSnapshot, StrategyDef, AccountDef, GerardMMDef/ScalingDef, ProviderDef, validadores y construcción GerardMM de snapshot.go/gerard_mm.go. Añadir el adapter de vistas de Operation fuera de marketctx. |
| `v3/sdk/futures/accounting` | Reducers puros fill/mark/day, FIFO y dinero exacto de §9. |
| `v3/sdk/futures/domain` | Datos `AccountProgramTerms` y envelopes mínimos requeridos, sin transportes. |
| `v3/sdk/futures/provider` | ClockFired/NextBoundary, risk/lifecycle y AccountContextUpdate atómico para binding/RuleSet/terms/snapshot. F01–F03 según protocolo. |
| `v3/sdk/futures/operation` | Observación correlacionada/normalizador compartido, RolloverEntryGate e identidad de mapping en pendientes, expiry/error propagation. F04/F05 según protocolo. |
| `v3/sdk/futures/strategy`, `strategies/s1`, `strategies/s2` | Preparación/activación por stream, DRAIN_CYCLE sin nuevos ciclos, guards exactos; mismo pipeline S1/S2 y fórmulas. |
| `v3/core/internal/functions`, `futuresruntime` | Mismas transiciones extraídas; adapters multi-contract/context y typed/raw fact+economics ingress hacia el único shared path; wiring de provenance/IDs según protocolo. |
| `go.work` | Incorporar sólo el nuevo módulo; no actualizar toolchain o dependencias por comodidad. |

Las transiciones Market/Analytics exponen la forma `Apply(state, typed_input, logical_now, run) -> next_state, ordered_effects, error`. Los efectos conservan los payloads reales: CanonicalMarketEvent, EpochBarrier, StreamStateSnapshot, BarsSnapshot, BarClosedDelivery, SessionTransitionDelivery, ReadinessChangedDelivery, QuoteNotification y pedidos de timer. No se introducen callbacks que escondan I/O.

Las shells Core retienen decode, ValueSpecs/load/store, enrutamiento StateFun, egress y telemetría. Preservar nombres de ValueSpecs, formas serializadas y contratos actuales; aliases/wrappers pequeños son aceptables. Las dos rutas deben llamar a una sola implementación de la transición extraída.

Dependencias permitidas: `market -> bars/domain`; `analytics -> market/bars/calendar` y los tipos actuales de Strategy/Operation; `marketctx -> market/bars/calendar`; `strategy -> marketctx`; `config -> SDK domains/engines/adapters`. `marketctx` no importa Operation ni Analytics; Market no importa Strategy. El nuevo módulo no importa `core/internal`, otro módulo hermano ni el harness. Esto respeta la independencia de módulos del repo. [S22]

### 4.2 Adapter de mercado de Operation

El adapter compartido indexa ContractCatalog por contract_id y resuelve su stream exacto, incluido uno retirándose con obligaciones. ResolveContract(instrument_id) sirve sólo la selección prospectiva para nueva materialización; Mark/Ready(contract_id) no vuelven a consultar ese mapping. Un ID desconocido produce miss. El source actual ignora ese argumento y usa un único stream. La extracción incorpora la validación exacta y su regresión en el paquete compartido. [S03]

Para el baseline seleccionado, conservar la capacidad real del contexto: Mark usa el trade actual y Ready usa readiness analítica/feed. No agregar `ExecutableQuoteSource` al adapter sólo para mejorar el backtest. El wrapper `quoteScopedMarket` actual presenta el midpoint de la quote y no expone esa interfaz opcional. SimExecution y la valuación pueden utilizar BBO sin alterar esa capacidad del MM. Cualquier mejora futura del wrapper debe ser un cambio compartido con evidencia propia. [S10]

### 4.3 Contratos físicos, selección y continuidad de Strategy

**MANAGER REQUIRED / DESIGN DECISION.** Un run mantiene una cuenta y un instrumento lógico, por ejemplo NQ, sobre múltiples contratos físicos. ContractCatalog contiene para cada contract_id su ContractSnapshot, instrument_id, stream exacto, external ref, unidades, calendario y cobertura de datos; registra last_tradable_at cuando la autoridad lo conoce. ContractSchedule contiene una secuencia finita e inmutable de `{control_id, previous_selection_control_id, instrument_id, contract_id, prepare_at, effective_at, strategy_config_refs}`. Los refs fijan los ConfigEnvelope/demandas de cada Strategy y su digest. Validar catálogo completo, cadena de selección, prepare_at <= effective_at, orden total y cobertura requerida; no descubrir roll dates por volumen/OI ni ajustar precios. El preflight rechaza schedules que exijan preparar un sucesor no inmediato de la selección vigente o excedan tres slots por Strategy, reservando el slot del activo que pueda seguir drenando. Durante el warm-up inicial el primer contrato ocupa la selección inicial a estos efectos. No omitir ni retrasar un prepare_at para hacer caber el schedule.

Las selecciones son intervalos [effective_at,next_effective_at). En fase 2, `ContractSelectionChanged` cambia el mapping prospectivo y deja el anterior RETIRING. ResolveContract sólo usa esa selección al materializar nueva Operation. Una Operation materializada conserva contrato, stream, units, MM plan, órdenes y correlaciones hasta terminar; no migra inventario ni genera un fill de rollover. Provider calcula capacidad de la misma cuenta con todos los contratos todavía expuestos. MarketContext, Bars, current, readiness y valuación permanecen por stream físico. [A05] [A06] [S27]

El test MKT07 vigente demuestra el pin de la Operation anterior mientras continúa su mercado e inyecta un OPEN nuevo; no demuestra por sí solo la transición técnica real de S1/S2. Strategy filtra hoy triggers por instrument_id y guarda LastBarBucket por instrumento/timeframe. La corrección compartida añade el guard de stream exacto y la clave stream/timeframe, sin añadir contract_id a Signal ni SignalDelivery: esa separación es autoridad existente. [S07] [S27] [S28] [S29] [S30] [S31]

Cada Strategy conserva un único owner, sus contadores globales de evaluación/ciclo y un solo ciclo técnico activo. Dentro del owner hay contextos técnicos acotados: activo, candidato seleccionado y siguiente candidato en preparación; máximo tres slots, compartiendo slot cuando activo=seleccionado. La preparación de B comienza en prepare_at y consume solamente su propio prefijo causal mediante el warm-up compartido de §7. No reproduce historia futura ni rellena indicadores de B con barras de A. Si el caller no proporciona suficiente prehistoria, B permanece no preparado o falla el requisito WARMUP_INCOMPLETE declarado; no se sigue abriendo A por fallback.

Al seleccionar B, el contexto A entra en `DRAIN_CYCLE`: sigue recibiendo su mercado y aplica las condiciones reales de gestión/cierre de S1/S2, con `AllowNewCycle=false` en el branch compartido que abre ciclos. No descartar Signals después de abrir un ciclo ni borrar ModuleState. B se activa sólo cuando es la selección vigente, está preparado y el ciclo técnico A terminó. Se instala su ModuleState/config preparado y stream guard, preservando IDs y contadores globales. La observación que completa preparación no se reevalúa como trigger normal; el primer trigger normal posterior puede abrir.

El cierre físico de una Operation no autoriza por sí solo a borrar un ciclo técnico A que sigue vivo: Strategy no consulta la cuenta para decidir su ciclo. A la inversa, si el ciclo técnico cerró pero la Operation A espera finality/cierre físico, B puede activarse; su nuevo OPEN usa el mecanismo existente y acotado de PendingNextCycleOpen en ese AccountStrategy, sin crear una segunda Operation concurrente allí. Si otro rollover llega mientras A drena, reemplazar el candidato nunca activado por el seleccionado vigente y registrar el descarte; jamás volver a una selección vencida. El siguiente candidato se prepara en el tercer slot. No retener indicadores de todos los expiries.

**Fence compartido de entrada.** Añadir en el owner de ejecución por AccountStrategy `RolloverEntryGate{selection_control_id, enabled, minimum_strategy_eval_seq}`. La selección deshabilita entradas e invalida PendingAdmission/PendingNextCycleOpen no materializados bajo la selección anterior; nunca borra una Operation existente. La activación técnica publica el gate habilitado, con el primer ordinal normal admisible, antes de emitir un OPEN nuevo. Al recibir OPEN, pinnear en el contexto de ejecución pendiente gate/control y contrato esperado; validar ordinal y selección al admitir y otra vez al materializar/promover. Una autorización ALLOW tardía, un OPEN de A todavía en vuelo o una selección A→B→A no revive trabajo anterior. Los inputs de gestión/reducción/cierre de la Operation pinneada siguen su correlación existente, sin ese bloqueo de nueva entrada. Signal conserva su contrato instrument-only. [A08] [S09] [S30] [S31]

Retener el stream y las vistas/órdenes necesarias de A mientras haya ciclo técnico A, Operation materializada, inventario/orden física, fill sellado, finality o reconciliación pendiente para A. Retirar buffers/builders sólo cuando se liberen todas esas referencias; conservar catálogo, facts y dedup necesarios. Una quote de B no actualiza mark/readiness de A ni oculta su falta de mercado. Si A necesita seguir vivo fuera de su cobertura, registrar `OLD_CONTRACT_DATA_UNAVAILABLE` y terminar INCOMPLETE con los residuales; un archivo corrupto sigue siendo FAILED. El caller puede programar un cierre normal previo a last_tradable_at con mercado suficiente; rollover no equivale a liquidación. No se presenta una serie continua sintética como observación física.

## 5. Contrato de datos históricos y fidelidad

### 5.1 DatasetSource: registros normalizados y formato externo

El engine depende del port mínimo `DatasetSource.Open(selection) -> HistoricalCursor`, con `Peek/Next/Close`. selection fija streams físicos y rangos UTC del manifest. El cursor entrega `HistoricalRecord{source_record_ref, source_order, candidate, quote_side_evidence}`: candidate es el MarketCandidateEnvelope compartido, más evidencia de origen/lados cuando existe. Abrir, descomprimir, decodificar y leer archivos pertenece al adapter; el causal/domain engine no recibe extensiones, paths, row groups, SDK de storage ni codecs. No hay ejecución sobre una base de datos.

La primera implementación S02 puede ser `internal/datasets/ndjson`, con gzip opcional, útil para fixtures/debugging/corpora pequeños. Otro adapter puede usar Parquet/ZSTD u otro layout eficiente sin modificar Backtest Engine, Strategy, Operation, MM, Provider o identidades de dominio. No hay corpus/benchmark representativo suficiente en este shot para congelar honestamente un formato productivo; quedan congelados el port y su conformance. Elegir o reemplazar codec no requiere otro design shot del engine.

| Artefacto | Autoridad |
| --- | --- |
| Manifest lógico inmutable | corpus_id/version, schema normalizado, identidad/capacidades de fuente, orden por stream, rangos/cobertura por contrato, calendario/gaps, conteos y digests de registros normalizados; referencia canónica durable de reproducción con versión/digest. |
| Manifest de representación física | Objetos/partes inmutables, formato/codec, byte SHA-256, tamaños, rangos de ordinals y prueba de correspondencia con el mismo manifest lógico. |
| Receipt de lectura | Representación realmente usada, digests verificados, buffers/opciones y métricas operacionales; externo a la identidad semántica y al gzip canónico del resultado. |

El RunSpec fija el manifest lógico y su referencia canónica durable. Un adapter puede leer una representación alternativa equivalente, validada contra ese mismo manifest, sin reemplazar esa referencia ni alterar ImmutableInputs. El receipt conserva qué bytes se leyeron. Reempaquetar no autoriza a borrar la fuente durable con la que el resultado puede reproducirse. No se usa un nombre mutable “latest” ni un servicio de registry nuevo.

Lectura streaming con batches/buffers configurados y acotados; merge estable con un lookahead por stream activo, sin cargar ni ordenar todo el histórico en RAM. Activar sus rangos desde prepare_at/warmup_start; no abrir tardíamente un prefijo anterior al reloj para insertarlo en el pasado. El número de buffers depende de streams/rangos activos, no del número de ticks. La memoria de metadata de catálogo/schedule/planes y de dedup físico se declara separadamente. Chunks, prefetch, compresión y tamaño de buffer no cambian los registros ni el orden entregado. Si se necesita una normalización/sort inicial, ocurre fuera del loop y produce un dataset nuevo con manifest; no un reorder oportunista dentro del dominio.

Los candidatos llegan por `(event_ts, stream_id, source_order)`, donde source_order conserva el orden lógico de captura por stream, independiente de la partición física. El shared StreamSequencer asigna stream_seq al canonicalizar. EVENT/POSITIONAL conservan identidad nativa. En NONE, la captura asigna una vez `IngressRecordRef{log_identity=logical_log_id, partition=logical_partition, offset=source_record_ordinal}` y expansion_index; un transcode/repack debe preservar esos valores. No derivarlos del digest/número de archivo o row group actual. Esto identifica una observación importada, sin probar un evento físico único: dos trades iguales en registros distintos permanecen distintos; content_digest detecta conflicto, no deduplica por precio/tiempo. [S04] [A05]

El adapter valida schema/unidades exactas, orden, cobertura, identidad y hashes de cada segmento consumido; el resultado fija además el digest del prefijo normalizado realmente admitido. Decode/truncación/conflicto o discrepancia de digest falla explícitamente. Prefetch puede leer bytes posteriores, pero ningún registro/lookup posterior a la frontera llega al dominio ni a una observación del caller. Correcciones de barras conservan su autoridad: actualizan proyección y no reevaluan retrospectivamente el cierre original. Un late delivery experimental se declara como fixture de laboratorio.

S02 debe comparar un corpus normalizado leído como una parte, múltiples chunks y un segundo adapter de conformance en memoria/particionado: mismo spec/build/namespace, idénticos inputs normalizados, IDs, records, estados, economía y gzip. Reportar peak RSS, buffers, counts y bytes de un corpus representativo; no inventar throughput o SLA. Cualquier adapter productivo futuro pasa ese mismo gate y demuestra memoria acotada sin cambiar el engine.

### 5.2 TRADE, BID, ASK, mark y fill

| Concepto | Autoridad y uso |
| --- | --- |
| TRADE | Última transacción observada; alimenta Bars y triggers declarados; trigger de stop V1. |
| BID/ASK | Observaciones de cada lado con source/ref, tiempo y epoch propios. |
| BBO ejecutable | Ambos lados ya observados, coherentes con contrato/epoch, bid <= ask y edad permitida de cada lado. |
| Mark del MM | Lo que devuelve el contexto compartido en esa invocación: trade o midpoint de Quote scoped, según source actual. |
| Mark económico | Bid para inventario neto long; ask para short, según modelo declarado. |
| Fill price | Lado ejecutable más slippage determinista; no es necesariamente trade, midpoint ni stop price. |

Si el proveedor entrega updates separados de BID/ASK, el normalizador sólo emite BBO cuando ya conoce ambos y conserva los timestamps/refs individuales. Actualizar BID no rejuvenece ASK. Sin esa evidencia, el corpus no puede declararse `OBSERVED_BBO`. No se leen registros futuros para completar el lado faltante.

Dos modos cerrados:

1. `OBSERVED_BBO`: trades y BBO observados para el contrato. No hay fallback desde BBO vencido a last. Un precio de ejecución necesita ambos lados válidos bajo la edad explícita.
2. `TRADE_MODEL`: `bid=last-bid_offset_ticks*tick_size`, `ask=last+ask_offset_ticks*tick_size`, offsets enteros no negativos y explícitos. Los lados son precios modelados de SimExecution/valuación, con referencia al trade causal. No se fabrican eventos QUOTE canónicos ni identidad nativa de mercado. MM conserva su contexto real; los cambios de valuación se entregan como AccountEconomicsUpdate derivado del trade. El resultado declara que no reproduce el cadence QUOTE/BBO de LIVE.

En ambos modos los fills y sus fuentes quedan ligados al cursor físico que los habilitó. Cero spread/slippage/fees es permitido sólo si está escrito en el spec. No hay RNG, latencia aleatoria, profundidad ni impacto implícitos.

### 5.3 Cobertura y readiness

Readiness de feed, readiness analítica y freshness económica son dimensiones distintas. Un intervalo sin trades no prueba un gap; el manifest/calendario y los controles de fuente distinguen ausencia de operaciones de datos faltantes. Epoch/recovery/readiness pasan por Market real. El BACKTEST no activa la regla de wall-clock freshness exclusiva de LIVE; sí valida edad histórica de quotes, cobertura y marks requeridos. [S01] [S05]

Una degradación declarada puede producir una denegación de riesgo válida dentro de un run COMPLETE. Un archivo truncado, checksum incorrecto o autoridad obligatoria irresoluble es un error de ejecución. No confundir abstención del dominio con datos corruptos.

## 6. Driver histórico y causalidad

### 6.1 Una cola pequeña, un reloj

El driver usa un cursor de dataset, controles temporales ordenados, mapa acotado de timers tipados activos y colas FIFO de efectos inmediatos. El próximo instante es el mínimo entre dataset, control y deadline. Siempre verifica el error de `VirtualClock.Set`; nunca avanza al siguiente tick saltándose timers intermedios. [S06]

**OWNER / MANAGER FROZEN.** Para causas independientes con tiempo T: [A06] (§9)

| Fase | Orden |
| --- | --- |
| 1 | Recovery/epoch barriers. |
| 2 | Configuración material/control. |
| 3 | Transiciones de sesión, ventana y account-day. |
| 4 | Market por `(event_ts, stream_id, stream_seq)`. |
| 5 | Timers restantes por `(deadline, timer_id)`. |

Los controles de una misma fase ordenan por ordinal estable y control_id. Una consecuencia derivada jamás precede a su causa: el barrier generado por un control se procesa como hijo suyo, sin moverlo retrospectivamente a fase 1. Los eventos de calendario transportados como timers pertenecen semánticamente a fase 3. Entry expiry y bar close ordinario son fase 5.

Un input raíz y sus efectos causales se completan antes del siguiente input raíz. No se procesan todos los ticks de T para recién entonces correr Strategy. La única retención especial es el lote físico sellado de un mismo market input, explicado a continuación.

Coordenada de evidencia: `{root_input_ordinal, phase, step_seq, parent_step_seq, effect_index, owner_input_seq, runtime_ts}`, más owner y ref del input. `step_seq` es un orden diagnóstico local, no una nueva secuencia global LIVE. Efectos mantienen su índice original.

### 6.2 Una observación de mercado C

1. **Admitir y proyectar.** Market aplica el candidato; Analytics aplica los eventos aceptados y compromete todos los cambios de barras, sesiones y current/readiness. Se retienen temporalmente los deliveries de Strategy/QUOTE hasta que sus vistas estén listas.
2. **Fijar ejecución física.** SimExecution toma sólo órdenes del contrato/stream físico de C, aceptadas antes de C, y calcula/sella matches con C y quotes ya observadas de ese mismo contrato. Ordena por acceptance_ordinal y order_id. Una orden creada por C no participa; un tick/prewarm B no ejecuta ni dispara stops de A usando una quote A retenida.
3. **Actualizar economía y aplicar fills.** Si C cambia un mark/freshness requerido por inventario o exposición actual, preparar ledger/risk/Provider AccountSnapshot de esa revisión, aun sin matches. Comprometerla antes de liberar safety o decisiones ordinarias; una quote relevante no deja a Provider con riesgo viejo. Un tick de B recibido sólo para preparación, sin obligación económica sobre B, no produce por sí solo una revisión ACCOUNT_ECONOMICS ni llamada MM sobre A. Retener efectos safety mientras se asienta el lote. Para cada fill, agregar fees/inventario y su nueva revisión; aplicar `ExecutionUpdate` por el path compartido de §8.2, con una sola invocación FILL, y comprometer candidatos al éxito. Entregar CapacityUpdate antes de pedidos de Reservation/Revalidate; esos nuevos pedidos esperan al cierre del lote.
4. **Reconciliar y liberar protección.** Terminar todos los fills/costes/CapacityUpdate sellados; entonces entregar una PositionObservation del net físico final de ese mismo prefijo. No comparar la posición de todos los matches contra un estado lógico que sólo aplicó el primero. Actualizar trust antes de nuevos pedidos. Entregar safety comprometido antes de trabajo ordinario todavía no comprometido. Cancels emitidos por el primer fill no eliminan un segundo fill ya sellado.
5. **Entregar decisiones de mercado.** Deliveries ordinarios conservan el orden de efectos producido por Analytics, con fanout estable por owner. QUOTE observado se entrega sólo a los owners cuyo contrato/stream corresponde y entra como `QuoteUpdate` correlacionado. En TRADE_MODEL, la valuación modelada puede causar un EconomicsUpdate ordinario con snapshot actual; no se llama directamente a GerardMM.
6. **Drenar.** Enrutar efectos, grants/revalidations, ACKs, cancels y finality hasta quiescencia inmediata. Los nuevos comandos pueden quedar working, pero esperan un cursor de mercado posterior para hacer match.

Los comandos ya comprometidos conservan sus dependencias por orden: NEW y su aceptación preceden al CANCEL que lo cita. Si un M1 directo quedó emitido durante feedback, se entrega a SimExecution antes de su cancel posterior, sin hacer match en C. La prioridad de safety sólo adelanta causas respecto de trabajo ordinario aún no comprometido; nunca invierte NEW→CANCEL, release→grant ni padre→hijo. Una continuación que todavía no cruzó M1 se revoca por el helper compartido de §8.3.

Se preserva el orden de cada slice de efectos dentro de su categoría causal. No ordenar arbitrariamente los ForceClose del Provider al exportar: eso ocultaría F02. La prioridad de safety y las retenciones anteriores son reglas explícitas del driver sobre tipos conocidos, no un scheduler genérico.

### 6.3 Empates, barras y timers

A las 10:00, el primer trade A puede cerrar naturalmente la barra de 09:55 y abrir la siguiente. A no pertenece a la barra cerrada. Se publican vistas y se procesa ese cierre antes del siguiente trade B, aunque B también diga 10:00. La orden causada por A no llena en A; puede llenar en B. Sin tick en el boundary, el timer cierra la barra. En cierre de sesión/break, fase 3 cierra/trunca antes del tick de fase 4. [S02] [S05]

Los timers se identifican por owner, timer_id, generación y boundary. Cancel/replacement invalida el anterior. Toda recurrencia avanza a un boundary futuro; un ciclo inmediato no convergente termina FAILED con su cadena causal.

**SOURCE FACT.** Analytics elimina una entrada de timer al dispararla y puede reutilizar generación desde una entrada ausente; su guard actual compara generación sin boundary. La extracción debe validar identidad completa y conservar monotonía, con regresión de un firing viejo recibido después de abrir otra barra. El driver no puede filtrar ese caso para ocultar el error compartido. [S02] (líneas 759–822)

Provider requiere el input compartido `ClockFired` y un `NextBoundary` estrecho para sus ventanas/cutoffs/términos. Cambiar el reloj por sí solo no ejecuta el sweep actual. Los cierres sin ticks y las transiciones account-day deben funcionar. [S14]

## 7. Strategy, Bars, Calendar y warm-up

Se reutilizan builders/grid, Calendar resolver, demands, S1/S2 y MarketContext. No se reconstruyen indicadores con otra librería. El scope de Strategy captura las lecturas reales sobre las proyecciones actuales y el BarClosedDelivery contiene la barra exacta que causó la evaluación. Una corrección posterior no reemplaza esa evidencia. [S02] [S05] [S07] [A05]

**SOURCE FACT.** S2 puede abrir un ciclo técnico durante un replay ordinario de prehistoria; filtrar sus Signals aguas abajo deja un ciclo ficticio abierto. La utilidad OHLC warmup existente sintetiza O/H/L/C y no constituye el corpus de ticks ejecutables de este producto. [S08] [S20]

**DESIGN DECISION.** Añadir `strategy.Engine.HandleWarmupWithScope`, que utiliza el mismo pipeline con `EvalInput.Warmup=true`. S1 conserva agregación de barras/sesión/account-day, OR y LastTradePrice, deteniéndose antes del branch de breakout/open-cycle. S2 conserva absorción H4/BB, deteniéndose antes de abrir/cerrar ciclos. Los paths normales mantienen Warmup=false. No hay Strategy de backtest.

El warm-up inicial comienza vacío, procesa sólo el prefijo anterior a trade_start y exige cero Signals y cero ciclo abierto. Una salida inesperada es error, no descarte silencioso. En trade_start se activa el mismo estado preparado; no se reescribe ModuleState JSON. La fase de activación no cierra artificialmente una barra que cruza ese instante.

La cobertura se calcula con barras realmente cerradas y demandas reales. S2 exige sus parámetros vigentes: trendPeriod+1 H4 y BollPeriod 5m; se conserva el predicado real `H4.CloseBoundary <= entryBar.BucketOpen`. Un comentario contradictorio no cambia ese predicado. S1 puede comenzar antes de completar OR y permanecer NOT_READY legítimamente. Un inicio que solicita contexto precalentado sin prehistoria suficiente falla `WARMUP_INCOMPLETE`. [S08]

El estado operacional/económico de la cuenta no registra compras, fills o fees durante el warm-up inicial; los cashflows account-level tienen effective_at >= trade_start. El trading se habilita en trade_start. El calendario y los boundaries de prehistoria siguen siendo reales.

El mismo warm-up prepara cada candidato físico de §4.3 desde prepare_at, mientras el contrato activo puede seguir operando y la economía de la cuenta continúa normalmente. Se aíslan ModuleState, Bars/readiness y lecturas por stream. DRAIN_CYCLE conserva absorción y cierre reales de un ciclo existente y bloquea únicamente su nueva apertura. La transición account-level de §11 conserva el estado técnico; no reinicia Strategy ni repite warm-up por cambiar de etapa.

## 8. Operation, GerardMM y Provider

### 8.1 Camino autorizado

Se conserva SignalDelivery → admission/pending admission → materialización de Operation → GerardMM real → claims locales → reservas/revalidación Provider cuando aplican → M1 OrderCommand → SimExecution. Provider no redimensiona silenciosamente la cantidad elegida por MM. Fills y finality regresan por los inputs compartidos y producen CapacityUpdate/release reales. [S09] [S11] [S14] [A07] [A08]

**SOURCE FACT.** El source permite M1 directo cuando sólo hay familias PER_ORDER o no hay caps compartidos; no corresponde inventar reservas obligatorias para ese caso. Si existe un grant compartido, su revalidación exacta antes de M1 sigue siendo obligatoria. [S09] (líneas 974–1191)

GerardMM recibe contrato pinneado, MMState, fills/claims, RuleSet completo y economía autoritativa. El ledger no llama a MM ni decide sizing. Las rows/config MM se pinnean al abrir la Operation; un nuevo account-day afecta el selector de futuras Operations y el snapshot económico de las existentes, sin reescribir su plan. [A09] [S10]

### 8.2 Economía correlacionada: un path compartido LIVE/BACKTEST

**MANAGER REQUIRED / FROZEN PROPERTY 1.** LIVE y BACKTEST usan finalmente la misma transición compartida para combinar hecho + economía, sin branch por RunMode en la semántica de Operation/MM. Los adapters normalizan evidencia; no implementan dos versiones del handler. S02 incorpora el ingress tipado de Core y su test real, aunque no despliegue D6 ni construya todo el upstream económico LIVE.

**SOURCE FACT.** buildMMInput prefiere DeliveredEconomics sobre Views; fill actualiza exposición e invoca MM dentro del mismo Apply. Actualizar Views y enviar Fill puede dejar economía vieja; enviar EconomicsUpdate primero llama MM con exposición anterior. La composición LIVE actual no demuestra un snapshot post-fill correlacionado. [S09] [S11] [S03] [S33]

Añadir al union operation.Input, manteniendo Apply y un solo input, `ExecutionUpdate{Fill, Observation}` y `QuoteUpdate{Quote, Observation}`. Observation es `EconomicsObservation{account_id, account_context_id, cause_key, revision_seq, revision_id, observed_at, covers_through, source_ref, status, reason, economics}`. Es un wrapper tipado y mode-neutral de AccountEconomics; status es AVAILABLE o UNAVAILABLE. AVAILABLE significa que existe una revisión autoritativa cuyo prefijo cubre esa causa, no que todos los marks estén frescos. economics conserva PnLFresh real. cause_key usa la correlación/dedup nativa del fill o QuoteID+contrato; covers_through identifica la frontera causal cubierta. AccountContextID cambia por transición; revision_seq es global a la cuenta/run y nunca se reinicia.

El binder/normalizador compartido valida identidad, shape, contexto, tiempo, causalidad y revisión. Historical adapter entrega la revisión del ledger que ya incorpora el fill/coste o la quote y todos los fills sellados precedentes. El ingress tipado real de Core acepta exactamente el mismo hecho y Observation y llama al mismo normalizador/Apply. Nadie consulta “latest economics” mutable dentro del callback o durante un retry. La evidencia se congela en el input.

Antes de instalar o invalidar economía, ejecutar guards de account/strategy/operation/order, dedup nativo y staleness. Para un fill nuevo de la Operation actual: instalar la observación, actualizar exposición con el handler real y llamar MM una vez con MMTriggerFill; Quote hace lo mismo con MMTriggerQuote. No generar ACCOUNT_ECONOMICS adicional por el sidecar. Un duplicado no reinstala una revisión anterior ni repite MM/coste/efectos; se permite únicamente bookkeeping diagnóstico ya definido por el owner. Un late fill de A no altera el estado económico de B por ese sidecar. Su efecto físico legítimo en la misma cuenta puede provocar después un AccountEconomicsUpdate account-wide independiente para B. F04 se prueba también en Apply, sin ocultar el input adversarial en ingress.

Los adapters raw Fill/Quote existentes de LIVE/Core conservan compatibilidad de entrada, pero normalizan determinísticamente a UNAVAILABLE cuando no traen evidencia correlacionada. No se toma Views.PnLFresh=true como prueba de economía post-fill. Para un hecho válido actual, UNAVAILABLE invalida la freshness económica efectiva del owner también para decisiones posteriores de gestión/finality; puede conservar valores conocidos para diagnóstico, sin presentarlos como autoridad actual ni fabricar una revisión económica cero. El fill físico, exposición, claims, CapacityUpdate y protección siguen sus handlers normales. GerardMM real deniega riesgo nuevo con PnLFresh=false sin devolver un error que deshaga el fill; safety/cierre siguen alcanzables. [S26]

La falta ordinaria de observación produce UNAVAILABLE. Contexto/cause_key no coincidentes, evidencia futura o revisión vieja no pueden calificarse AVAILABLE: registrar la razón y usar UNAVAILABLE para el hecho válido actual. Un conflicto de payload para una identidad/revisión ya aceptada es violación de autoridad y aborta con evidencia; si el fill ya fue sellado físicamente, preservarlo en el capsule de §3/§14. No descartar un fill físico para mejorar la economía aparente. Una causa duplicada/ajena se resuelve por sus guards antes de tocar freshness.

Un AccountEconomicsUpdate independiente, versionado y del contexto vigente, puede restaurar freshness cuando su prefijo cubre todos los hechos materiales ya aceptados; se procesa como su propia causa ACCOUNT_ECONOMICS, sin adjuntarlo retrospectivamente al fill. QUOTE y ACCOUNT_ECONOMICS genuinos al mismo timestamp conservan dos causas. Observaciones de contexto anterior o revisiones regresivas no restauran autoridad.

El callback usa el clone y los allocators transaccionales compartidos: error MM abandona estado/IDs/effects candidatos; retry recibe exactamente el mismo Observation, incluso si Views cambió entre intentos. Raw continúa UNAVAILABLE al reintentar. No adaptar los tests heredados dejando vivo el path viejo: cuando necesitan economía fresca deben aportar evidencia explícita.

**Acceptance de paridad obligatoria.** Mismo before-state, causa, Observation, RuleSet, contrato, Market capabilities/reads, clock, allocator y RunProvenance: entrada por Core tipado y por historical adapter debe producir MMInput completo, MMState/owner state y ordered effects idénticos. Otro caso entra por Core raw con Views engañosamente fresh, compara el mismo trace UNAVAILABLE histórico y luego una actualización económica independiente. Probar fill/quote, dedup/late/foreign, error/retry y contexto/revisión. El test debe cruzar el decoding/dispatch real de Core; llamar dos veces al mismo Apply no acredita adapters. Una prueba adicional conserva los allocators/provenance reales LIVE vs BACKTEST y permite sólo esas diferencias nombradas; nunca eliminar IDs/campos arbitrarios para hacer coincidir resultados. El recorder conserva las interfaces opcionales reales de Market (§4.2/§16.2).

### 8.3 Entry expiry y terminación

Pinnear `OperationRuntime.EntryExpiresAt = openingDelivery.ValidUntil` al materializar y emitir efectos tipados de schedule/cancel. La autoridad D2-04 define ENTRY_EXPIRED como TTL de entry/signal sin fill. El primer fill o la terminalidad desarma el timer; un firing viejo valida identidad/generación. Un fill exactamente al deadline gana por fase 4 antes de fase 5. [A10]

Completar el handler compartido: si la entry aún no cruzó M1, revocar su continuación local, liberar reserva por el path real y bloquear una respuesta tardía que intente publicar. Si `CommandPublished=true`, emitir CANCEL y mantener q_exec_max/claims hasta fill/finality. No fabricar finality para una orden nunca enviada. Reutilizar ese helper de revoke/cancel donde terminación y safety lo necesiten. [S11]

Propagar los errores de `replanSafetyClose` actualmente descartados en llamadas a `admitOrderRequest`. Un error al construir el cierre no puede aparecer como transición exitosa. Esta corrección y el timer guard son requisitos concretos de las transiciones tocadas, no nuevas políticas D6. [S11] (líneas 808–932)

## 9. Economía de cuenta

### 9.1 Ledger físico y exactitud

El nuevo package `accounting` sólo depende de domain/units. Mantiene inventario FIFO por account+contract, realized gross, costes cobrados, balance, marks/unrealized/equity, baselines diarios, contador de revisión y dedup nativo. No importa Strategy, MM, Provider engine ni storage.

**SOURCE FACT.** PositionObservation expresa posición física neta; Operation conserva exposición lógica derivada de sus fills. Una compra de una Operation y una venta de otra pueden netear físicamente a cero aunque ambas sigan vivas. [S12] [S13]

No sumar unrealized de cada Operation usando bid/ask como si fueran cuentas físicas independientes: cargaría spread adicional. El ledger netea fills reales sólo dentro de account+contract, preservando la atribución lógica de cada fact por separado. Un long NQH y un short NQM nunca se netean como un único lote: cada uno se valúa/cierra con su contrato y la cuenta suma sus PnL/costes. Rollover no reinicia balance, drawdown, day/stage baselines, cashflows ni revisión.

Para un lote de dirección d (+1 long, -1 short), precio de entrada a, y cierre de k contratos a p:

~~~text
delta_realized_gross = d × k × (p − a) × point_value
unrealized = suma(d × cantidad_remanente × (mark_liquidacion − a) × point_value)
realized_net = realized_gross − charged_costs
balance = initial_balance + realized_net + explicit_nontrading_cashflows
equity = balance + unrealized
~~~

Los fills opuestos consumen los lotes más antiguos; un reversal cierra y abre el residual real, sin clamp. FIFO_V1 evita serializar promedios infinitos como 100.333… en un Money decimal exacto. GerardMM conserva su aritmética de promedio actual; FIFO es una convención explícita de contabilidad física del experimento.

USD e integer contracts en V1. Calcular diferencias en ticks por tick_value o aritmética racional exacta validando representación finita; nunca float64 ni redondeo implícito. ContractSnapshot, tick_size/tick_value/currency y external ref quedan fijados. Fees exactos por contrato/lado se cobran una vez por fill nativo. Spread/slippage ya están en fill price; no se descuentan nuevamente. No se cobra comisión de una salida futura todavía no ejecutada. [S12] [S21] [A09]

### 9.2 Account-day y snapshots

Al inicio del account-day conservar balance, equity, realized/cost/cashflow baselines. La autoridad requerida por MM es:

~~~text
account_day_pnl =
    realized_gross_since_day_start
  − charged_costs_since_day_start
  + current_total_unrealized

account_day_pnl =
    current_equity
  − day_start_balance
  − nontrading_cashflows_since_day_start
~~~

Si hay posición overnight, el total unrealized actual forma parte de esa autoridad; no se resta en secreto el unrealized de apertura del día. La variación desde day_start_equity es otra métrica de análisis. El reset usa timezone/hora del binding, separado del día UTC y de la sesión del exchange. [A09]

En cada boundary: finalizar el día anterior; actualizar watermark EOD; establecer el nuevo balance baseline y day_id; activar el selector explícito de nuevas Operations; publicar snapshots coherentes antes de decisiones del nuevo día. Días calendario/de negocio y días efectivamente operados tienen contadores distintos.

La secuencia de revisión es monótona durante toda la cuenta/run, incluidos rollovers, cashflows y cambios de contexto. Una revisión económica contiene `account_id, account_context_id, revision, observed_at, cause_ref, account_day_id, initial_balance, balance, equity, realized_gross, charged_costs, realized_net, unrealized, day_start_balance, day_realized_net, account_day_pnl, stage_net_pnl, best_day_net, marks, freshness` y risk state. Proyectar desde esa misma revisión:

| Consumidor | Proyección |
| --- | --- |
| Operation/GerardMM | `AccountEconomics`: PnL account-day, currency, AccountDayID, PnLSnapshotVersion, PnLFresh, headroom monetario y selector aplicable. |
| Provider | `AccountSnapshot`: Known, AccountState, breaches, PhysicalTrust, AccountDayID, consistencia y cap-breach evidence. La revisión se registra junto a la entrega aunque el struct actual no tenga ese campo. |
| Result/lifecycle | Balance/equity, floors, límites/cobertura, causa, marks y resultado económico. |

**SOURCE FACT.** Provider consume AccountSnapshot; el ingester es responsable del reset diario y de los flags autoritativos. El view adapter actual sirve economía, no la calcula. [S03] [S15]

Añadir funciones puras compartidas `provider.EvaluateEconomicRisk` y un evaluador de lifecycle con structs tipados; reciben observación, risk state anterior y RuleSet/términos completos. Su resultado no es sizing: produce floors, headroom, flags y outcome. Provider Apply sigue resolviendo admission/safety.

La observación económica se actualiza ante cada cambio material de mark requerido, fill, coste, account-day, control o freshness. Un stream usado sólo para preparar un contrato futuro no invalida ni refresca una cuenta/Operation que todavía no lo requiere. Antes de una decisión que pueda abrir riesgo, las proyecciones validan la edad contra el reloj lógico actual; si la evidencia venció desde la última entrega, el driver compromete primero la nueva revisión de freshness/Provider y sus efectos, como consecuencia de ese avance lógico. No mantener Known/PnLFresh verdaderos sólo porque no llegó otro tick.

Un mark requerido ausente/vencido produce PnLFresh=false y estado de riesgo no resuelto, bloqueando nuevo riesgo. `nil headroom` significa que no aplica una familia monetaria; no significa error de cálculo. Inventario neto cero puede valuarse con balance sin quote. La confianza física se obtiene reconciliando PositionObservation con los hechos, jamás forzando la exposición lógica al valor observado.

## 10. Contextos Generic100K y prop

### 10.1 Generic100K: horizonte arbitrario con GerardMM real

**OWNER / MANAGER FROZEN.** Generic100K fija sólo initial_balance=USD 100000. El caller aporta MM/config, account-day, binding/RuleSet ACTIVE de simulación, fees, ejecución y horizonte. No se salta Provider ni se inventa entitlement LIVE. [A01]

**DESIGN DECISION.** Antes de NewRun, `MaterializeExperimentPlanV1` en la configuración del backtester admite una tabla resuelta explícita o la única política generada V1 `FIXED_BUDGET_PER_ACCOUNT_DAY_V1`. Sus inputs son policy_id/version, account/context, activación/end_exclusive, timezone/boundary/calendario/tzdata, first_day_ordinal positivo, SL/TP Money explícitos y `ordinal_basis=EVERY_RESOLVED_ACCOUNT_DAY`. No es una regla real de prop ni código dentro de GerardMM.

La función enumera todos los intervalos account-day que intersectan el período de ese contexto, incluidos primer/último día parcial y días sin trades según el calendario declarado. Warm-up no consume ordinal. Resolver boundaries de calendario, sin sumar 24 horas a través de DST. Para cada intervalo genera account_day_id/start/end/ordinal, una EconomicPlanRow EVALUATION ordinaria y los selectores MMConfigSnapshot correspondientes. El resolver vigente acepta EvaluationDayOrdinal positivo; no limita el contrato a días 1/2. [S16] [S32]

Policy original, versión de materializador, tabla expandida completa, EconomicPlanRows, selectores resueltos y sus digests quedan en ImmutableInputs/result. NewRun valida cobertura exacta, claves únicas, ausencia de gaps/overlaps, rango/overflow, moneda y presupuestos; runtime sólo consume filas normales. Ningún `if generic`, “day2 forever”, extensión en caliente o fallback entra en GerardMM. Una tabla directa incompleta sigue fallando, incluso si falta day3. Una transición posterior materializa su propio horizonte antes de admitirse y trae sus filas dentro del nuevo contexto.

En cada boundary cambia el selector de futuras Operations; la Operation abierta sigue usando la row/config pinneada y su autoridad continúa disponible. Repetir explícitamente un presupuesto es una decisión de experimento representada por N filas, no reutilizar escondidamente el ordinal 2. Memoria O(account-days) para esta metadata es admisible; no implica retener ticks.

**Ejemplo obligatorio S02: `generic100k-fixed-budget-20-days-v1`.** Veinte account-days UTC 00:00, [2026-10-05T00:00:00Z,2026-10-25T00:00:00Z), stage_id GENERIC_LONG_HORIZON, selector EVALUATION ordinals 1…20, SL USD 2000 y TP USD 1500 en cada row; evaluation_target=nil. Adds deshabilitados, currency/scaling, RuleSet SIM sin restricciones opcionales, fees/slippage/TIF y calendario quedan explícitos. Los valores de días 1/2 coinciden con el ejemplo Owner; extenderlos a veinte días es política declarada de este experimento, no autoridad de la prop. [A09]

La fixture debe producir decisiones y operaciones válidas después del segundo día y en el tramo final, usando GerardMM real, además de verificar los veinte selectores. Precios sintéticos se identifican como fixture de modelo; las fechas son coordenadas reproducibles, no una afirmación de disponer de mercado observado futuro. La misma materialización soporta cualquier horizonte finito solicitado con cobertura/datos válidos; no hay límite arquitectónico de dos días.

### 10.2 Contexto GAU50 representativo

**SOURCE FACT.** La materialización vigente GAU50-EVAL@1 tiene cap GROSS 6, ventanas Mon–Fri [00:00,15:50) y [17:10,23:59) America/Chicago, DLL USD 1100 con PREV_DAY_CLOSE/flatten, trailing EOD USD 2000 con INITIAL_BALANCE/flatten y consistencia 30%. Su guard exige ForcedFlatCutoff=nil. Por tanto, bloquear admission fuera de ventana no demuestra por sí solo el cierre de órdenes/posiciones a las 15:50. [S17] [S25] [A11]

Conservar los bytes/digest y EffectiveAt de esa autoridad. El contexto demostrativo utiliza initial_balance USD 50000 y un suplemento tipado claramente identificado, sin editar el JSON D6.

| Restricción del modelo | Cálculo/acción dentro del run |
| --- | --- |
| GROSS 6 | Provider real, claims/reservas/revalidation; sin resize. |
| Ventanas vigentes | Semántica actual exacta, incluidos 17:10 y el gap de 23:59; no “corregir” silenciosamente. |
| DLL 1100 | Floor = day_start_balance − 1100; headroom = max(0,equity−floor). `loss >= 1100` es comparator conservador explícito del modelo. |
| EOD trailing 2000 | F0=48000; al EOD, F_next=min(50000,max(F_previous,B_close−2000)); intradía no ratchetea; equity <= F incumple. |
| Headroom a MM | Mínimo de familias monetarias aplicables y resueltas, con revisión/provenance; GerardMM conserva su min con presupuesto Owner. |
| Consistency 30% | Reutilizar/exportar la función exacta compartida: best_day×100 >= 30×total no cumple; total <=0 es indeterminado. No es un rechazo de cada orden ni hard fail inmediato. |
| Target 3000 | Evaluador de lifecycle sobre stage net realized y consistencia en punto quiescente; no inferir entrega de cuenta FUNDED. |
| Flat horario | Deadlines fechados explícitos y cierre anticipado por Provider compartido, como §10.3. |
| Reset diario/EOD del modelo | 17:00 America/Chicago con tzdata fijada y cashflow explícito. |

El preflight aceptado respalda target 3000, equity <= EOD floor y el día 17:00–17:00; no establece con igual precisión el comparator de igualdad DLL. También dice progresión “hasta 6” sin thresholds. No inferir una tabla de progresión ni un mínimo histórico de diez días; el preflight vigente dice sin mínimo. [A12] [S18]

El escenario se denomina `gau50-eval-frozen-fixed-cap-model-v1`. Puede demostrar cómo estas restricciones cambian causalmente riesgo, MM y continuidad. Su resultado de éxito es `MODELED_EVALUATION_PASS`; `real_program_qualification=UNRESOLVED` mientras falten progression tiers, excepciones relevantes o evidencia de policy. No representa aprobación real de Earn2Trade, payout ni certificación LIVE.

Si las reglas fechadas 2026-10-01 se aplican a precios anteriores, exigir `policy_application=FROZEN_RULESET_COUNTERFACTUAL`. Conservar EffectiveAt original y declarar scenario_activation_at por separado. No reescribir la fecha para aparentar políticas conocidas históricamente.

### 10.3 AccountProgramTerms: suplemento mínimo

Añadir datos compartidos `domain.AccountProgramTerms`, ligados a un RuleSet exacto, con:

| Campo | Semántica decidida |
| --- | --- |
| `terms_id, version, digest, source_refs` | Identidad y evidencia del suplemento. |
| `ruleset_id, ruleset_version, ruleset_digest` | Parent exacto; mismatch invalida contexto. |
| `stage_id` | Identidad de la etapa, sin que el string aporte reglas. |
| `evaluation_target` | Money explícito; nil indica que no se solicita evaluación de pass. |
| `minimum_traded_days` | Entero >=0 explícito para habilitar PASS. El ejemplo GAU50 fija 0 según fuente; nil significa evidencia/término no resuelto y no habilita PASS. |
| `required_flat` | Lista finita de `{deadline_id, close_request_at, deadline_at, reopen_at, source_ref}`, instantes UTC resueltos con timezone/calendario. |
| `terminal_breaches` | Familias concretas que latchean FAIL: DAILY_LOSS, TRAILING_DRAWDOWN y REQUIRED_FLAT en el ejemplo. No parser ni expresiones libres. |
| `coverage` | Aspectos verificados, modelados y no resueltos; modo de aplicación temporal. |

`close_request_at < deadline_at < reopen_at`; la anticipación de cierre es una política explícita de ejecución del escenario, por ejemplo 60 segundos en el fixture, y no un dato de la prop. Este campo permite cerrar con ticks reales posteriores sin inventar un fill al deadline.

En close_request_at, el pequeño controlador compartido de programa instala CLOSE_ONLY y genera ForceClose por el mismo sweep de Provider, conservando las identidades de episodio y la provenance del run. En deadline_at evalúa physical net position cero y ausencia de órdenes físicas working; además exige quiescencia lógica/finality para que el engine continúe con seguridad. Una posición física no cero u orden física working al deadline produce `MODELED_EVALUATION_FAIL` con reason `REQUIRED_FLAT_VIOLATION`, latcheado para esa etapa del modelo. Una inconsistencia exclusivamente lógica/finality se registra como `MODEL_OPERATIONAL_FAILURE`, latcheada para impedir continuidad insegura, sin presentarla como prueba de infracción real de la prop. El deadline es fase 3: exige estar flat antes del market input del mismo timestamp; ese tick no repara retrospectivamente el incumplimiento.

En `reopen_at`, retirar sólo el bloqueo temporal identificado por deadline_id. Restablecer ACTIVE únicamente si no quedan otro deadline activo, bloqueo/config de cuenta, breach terminal, fallo operacional o autoridad faltante. Un resultado terminal no se borra por reapertura. Mantener razones de bloqueo tipadas para no sobrescribir CLOSE_ONLY impuesto por otra causa. La familia `program_required_flat` ocupa un lugar fijo después de `forced_flat_cutoff` y antes de `daily_loss` en el sweep; ambas usan el mismo enrutamiento ForceClose.

No derivar forced-flat de todos los cierres de AllowedNewRiskWindow; 23:59 no crea otra liquidación. No adivinar holidays/product exceptions: el fixture acota contrato/fechas y proporciona deadlines completos. Un breach económico terminal queda latcheado: recuperación de precio o reset diario no revive la etapa. Se bloquea riesgo nuevo y se sigue procesando el cierre/costes/finality necesarios.

## 11. Lifecycle, transición de contexto y cashflows de cuenta

### 11.1 Outcome de etapa y continuidad

El evaluador compartido produce AccountLifecycle con account_id, stage/context digest, observed_at/effective_at, cause_ref, resultado y razones. Distingue ACTIVE, MODELED_EVALUATION_FAIL, MODELED_EVALUATION_PASS y MODEL_OPERATIONAL_FAILURE; AWAITING_NEXT_CONTEXT es estado de continuidad, conserva el outcome de la etapa. Son resultados del modelo, no una taxonomía universal de empresas.

Pass exige target alcanzado en stage net realized, consistencia cumplida, minimum_traded_days explícito/satisfecho, cobertura suficiente y la quiescencia de §11.2. Cuenta días operados por account_day_ids distintos con un ExecutionFill válido, único y de cantidad positiva durante esa etapa; duplicates no suman, no exige día positivo. El ejemplo GAU50 fija mínimo 0; nil impide PASS. Target observado sólo en unrealized no acredita pass; consistency temporalmente excedida puede resolverse después sin quemar por sí sola la cuenta.

RunSpec declara `outcome_handling=STOP|AWAIT_CONTEXT`. STOP detiene por outcome y finaliza sólo tras asentamiento requerido. AWAIT_CONTEXT latchea el outcome, mantiene CLOSE_ONLY y drena riesgo/finality; al quedar quiescente expone AWAITING_NEXT_CONTEXT y puede continuar con un siguiente contexto suministrado por el caller. No hay transición automática PASS→FUNDED, elección de prop ni reseteo de saldo por el nombre del stage.

### 11.2 AccountContextTransition, obligatorio V1

`AccountContextTransition{control_id, effective_at, ordinal, account_id, expected_context_digest, next_context, state_modes, expected_balance?}` es un control causal de fase 2. next_context es completo: context_id nuevo no reutilizado/stage_id, Provider binding/RuleSet, AccountProgramTerms o ausencia explícita, estado operacional de cuenta, GerardMM config/currency/scaling/planes, selectores resueltos por Strategy/account-day, calendario de cuenta, límites/risk seed, cashflow treatment y coverage/source refs/digests. El caller proporciona los valores, el engine no los deriva de PASS ni de labels. El calendario account-level rige economía/MM; no reemplaza automáticamente el calendario de exchange ni la configuración técnica de Strategy.

Quiescencia exige inventario físico cero en **cada contrato**, PhysicalTrust reconciliado/trusted, Operations ausentes o terminales sin exposición lógica/q_exec, cero órdenes ejecutables, finality/actions/fills sellados pendientes, reservas/claims/firm exposure, admissions/revalidations/DeferredOpen y cola inmediata relacionada. Incluye hechos físicos futuros ya programados por una fixture; un cancel ACK o netear dos contratos/opuestas no basta. El ciclo técnico de Strategy puede seguir vivo: no es exposición de cuenta y no se borra por cambiar stage. Esto difiere de la activación técnica de rollover (§4.3).

Al admitir, validar shape, identidades, autoridades completas y cobertura; es lícito encolar una transición futura mientras hoy existe exposición. En effective_at comprobar expected_context_digest, expected_balance si existe y quiescencia contra el estado real. Si entonces no hay quiescencia, fallar `CONTEXT_NOT_QUIESCENT`; no forzar cierre, esperar hasta que casualmente quede flat ni cambiarle la fecha. expected_context_digest evita aplicar una transición preparada para un contexto anterior. Un cambio de ProviderAccountRef que signifique otra cuenta física requiere otro account/run relacionado; AccountID, moneda base, RunID y modelo físico de esta cuenta no cambian.

| Estado | Acción V1 |
| --- | --- |
| AccountID/RunID; ledger acumulado, fills/costes/cashflows, dedup, correlaciones y secuencias de revisión/IDs | PRESERVAR; nunca reutilizar IDs ni borrar historia. |
| Market/Bars/Calendar de exchange, Strategy, ciclos técnicos y contadores; ContractCatalog/Schedule/pins | PRESERVAR; cambiar stage no reescribe mercado ni reinicia warm-up. |
| Ledger balance/equity y confianza física | PRESERVAR; expected_balance sólo valida. Mover dinero requiere AccountCashflow. |
| Binding/RuleSet, terms, MM config/rows/selectores, account operational state, contexto y coverage | REEMPLAZAR atómicamente por autoridades completas, validadas. |
| Progreso de etapa | `PRESERVE_STAGE` exige mismo stage_id; `START_NEW_STAGE` exige stage_id nuevo, archiva outcome/PnL/contadores anteriores y comienza sus baselines explícitos en el balance actual. Ledger acumulado intacto. |
| Account-day | `CONTINUE_CURRENT_DAY` exige mismo calendario y conserva baseline; `START_NEW_CONTEXT_DAY` sólo junto a START_NEW_STAGE, cierra el segmento parcial etiquetado y abre otro hasta el siguiente boundary natural. No finge un EOD. |
| Risk state | `PRESERVE_RISK_STATE` sólo con definiciones/bases/moneda compatibles; `REPLACE_EXPLICIT_RISK_SEED` exige valores completos por familia aplicable: floors, watermarks, referencias, caps y latches válidos. Un seed de riesgo no es dinero. |
| Bloqueos/episodios/timers de contexto | Conservar los de autoridades preservadas; retirar sólo los pertenecientes al contexto sustituido, guardados por context_id/generación. No limpiar faults de confianza física. |

Un mismo stage conserva breaches/outcome terminales aunque reemplace un seed; no puede resucitar una etapa fallida cambiando RuleSet. START_NEW_STAGE puede iniciar sus propios latches con evidencia explícita, manteniendo el outcome previo archivado. Si CONTINUE_CURRENT_DAY cruza una transición de etapa, conservar la métrica account-day de MM y comenzar por separado el progreso de etapa; los contadores de días operados de la etapa sólo cuentan sus propios fills.

En el mismo timestamp que el EOD natural del contexto anterior, finalizar ese EOD exactamente una vez como hijo del control antes de instalar el nuevo contexto; invalidar el timer antiguo y no repetir fase 3. Fuera de ese boundary no ratchetear EOD. Resolver íntegramente el primer intervalo del nuevo contexto; no activar dos day resets por el mismo evento.

Añadir `provider.AccountContextUpdate` al union compartido: instala binding, RuleSet, terms, snapshot y context identity en un solo Apply/sweep. No encadenar updates que permitan decidir con binding nuevo y RuleSet/estado viejo. Preparar las pocas estructuras candidatas de Provider/account/Operation views, validar y comprometer antes de liberar efectos. Publicar contexto/modes/digests y primera revisión económica del nuevo contexto; entregarla a los owners de Operation antes de otro input. revision_seq sigue monótona, AccountContextID cambia; un input económico del contexto viejo no modifica la nueva autoridad. Las rows antiguas necesarias para evidencia/dedup permanecen referenciables.

### 11.3 AccountCashflow, obligatorio V1

`AccountCashflow{control_id, effective_at, ordinal, account_id, expected_context_digest, cashflow_id, amount, kind, source_ref, treatment_digest}` aplica un Money USD con signo, distinto de cero, en fase 2. kind es PAYOUT_DEBIT (negativo), RESET_ADJUSTMENT o ADJUSTMENT (signo explícito). Dedup por account_id+cashflow_id durante toda la corrida: misma identidad/payload es no-op económico incluso después de otra transición; payload distinto es conflicto. Resolver ese dedup antes de exigir el contexto vigente para un movimiento nuevo. Context/digest/unidades inválidos no se aplican.

El único tratamiento V1 es `EXCLUDE_PERFORMANCE_PRESERVE_ABSOLUTE_RISK_V1`, seleccionado explícitamente en contexto/control:

| Magnitud | Efecto de delta |
| --- | --- |
| Balance/equity | Sumar delta inmediatamente; inventario no cambia. |
| Realized trading, fees, account-day/stage PnL, best day, consistency, traded days | No cambia; registrar cashflows separados y conservar fórmula §9. |
| Floors, watermarks y referencias monetarias absolutas intradía | Conservar; recalcular headroom con equity actual. |
| Breaches/safety | Evaluar con esa revisión antes del siguiente market input; un debit puede forzar cierre. Un credit no deslatchea un fail. |
| EOD natural posterior | Evaluación normal con balance post-cashflow; el cashflow no fabrica un EOD ni una traslación de floors. |

Ejemplo de conformance: balance=100000, inventario cero, floor=98900 y payout=-500 producen balance/equity=99500, trading PnL sin cambio y headroom=600. El tipo PAYOUT_DEBIT no acredita eligibility ni settlement comercial. Si otro modelo necesita trasladar floors/baselines, debe aportar un AccountContextTransition explícito con seed y quiescencia; no inferir otra política dentro de este tratamiento.

Cashflow se permite con posiciones abiertas y publica una revisión ACCOUNT_ECONOMICS independiente más AccountSnapshot/Provider safety por el path compartido. Si falta un mark requerido, se asienta el dinero y la revisión permanece no fresh; no se omite el movimiento. Exact retry/rollback de callbacks y trazabilidad conservan §3/§14. Si cashflow y context transition comparten timestamp, ordinal/control_id fijan el orden y cada expected_context_digest debe corresponder al prefijo real.

### 11.4 Caller controls y frontera causal

CLOSED_SPEC fija antes de NewRun todos los controles. CALLER_CONTROLLED permite `EnqueueControl` sólo mientras el engine está pausado entre fronteras completas, únicamente para AccountContextTransition/AccountCashflow. El caller debe elegir effective_at estrictamente posterior a la frontera completada, dentro o más allá del horizonte declarado; no se modifica end_exclusive, el pasado ni el ContractSchedule. Un control más allá del horizonte queda aceptado pero pendiente y declarado, sin efecto económico. No sumar automáticamente un nanosegundo ni reescribir el timestamp solicitado.

La admisión valida shape/identidades y materializa planes/términos ya proporcionados; expected_context_digest puede referir a un contexto de una transición previa ya admitida y se verifica obligatoriamente al aplicar, sin exigir que un contexto futuro ya sea el actual. Registra secuencia append-only, frontera de admisión, effective_at, ordinal y payload/digest. No editar/cancelar controles aceptados. Validaciones dependientes del estado se repiten al aplicar. La identidad de este modo se fija por namespace previo del caller (§13.1); el manifest final contiene todos los controles aceptados y sus fronteras de admisión. Reproducción reinyecta esas admisiones en las mismas fronteras; no precarga como visible al dominio lo que el caller todavía no había entregado.

AdvanceUntil(T) siempre retorna una frontera completada <=T. En CALLER_CONTROLLED/AWAIT_CONTEXT puede devolver una vez antes de T al primer outcome quiescente de la etapa, con AWAITING_NEXT_CONTEXT; el caller suministra el siguiente contexto y vuelve a avanzar. Si no lo entrega, el engine sigue bloqueando nuevas entradas y puede avanzar al horizonte con ese estado. CLOSED_SPEC usa sólo los contextos ya fijados y tampoco finaliza anticipadamente por outcome si eligió AWAIT_CONTEXT. Finish sella admisiones y exige §15; no implica PASS ni continuidad funded.

### 11.5 Campaign Simulator diferido

El futuro controller externo posee compras, fees comerciales, bankroll, cuentas, payout eligibility/settlement y reinversión; invoca AdvanceUntil/EnqueueControl con información de prefijo. Sólo traduce los efectos account-level relevantes a los dos controles anteriores. No suma nominal 50K/100K al bankroll, ni cobra al ledger de cuenta un fee de reset comercial que sólo afectó la caja del usuario.

Bankroll usa únicamente compras/fees y créditos de payout ya asentados a tiempo t; un payout conocido el día 5 no compra el día 2. Parent IDs y observaciones causales permiten relacionar cuentas físicas distintas sin fingir continuidad. No se exponen summaries futuros ni se eligen retrospectivamente corridas favorables. Cuentas completas sólo podrían paralelizarse si decisiones de campaña no alteran sus trayectorias ni hacen visible su futuro.

S02 implementa transición/cashflow/caller seam y acceptance dentro de un engine. No implementa Campaign Simulator, compras, pricing comercial, wallet ni workflow engine.

## 12. SimExecution V1

### 12.1 Estado y autorización

SimExecution mantiene comando/correlación inmutables por orden, estado físico, remaining qty, acceptance_ordinal/cursor, stop_triggered, fills, terminal finality, dedup de comandos y sesiones/binding. No vuelve a consultar una RuleSet mutable para autorizar un comando que ya cruzó M1.

**SOURCE FACT.** GerardMM seleccionado emite MARKET, STOP_MARKET y CANCEL; el bridge sim existente está orientado a scripts. El dominio ya distingue OrderObservation, ActionObservation, ExecutionFill, PositionObservation y SessionObservation. [S26] [S12] [S19]

### 12.2 Matching

| Tipo | Regla exacta |
| --- | --- |
| MARKET BUY | Primer cursor posterior a aceptación del mismo contrato/stream pinneado, sesión negociable y quote válido propio: ask + slip_ticks×tick_size. Full remaining qty. |
| MARKET SELL | Mismas condiciones: bid − slip_ticks×tick_size. |
| STOP_MARKET BUY | Sólo trade aceptado del mismo contrato/stream, posterior a aceptación, con last >= stop. Pasa a triggered MARKET y usa ask propio válido; espera otro cursor de ese contrato si falta quote. |
| STOP_MARKET SELL | Sólo trade posterior del mismo contrato/stream con last <= stop. Usa bid propio válido o espera otro cursor de ese contrato. Un gap no llena al stop solicitado. |
| CANCEL | Detiene futuros matches no sellados; ACK y finality separados. |
| Replace de GerardMM | CANCEL + NEW independientes, claims y autorización propios. |
| LIMIT/native MODIFY | Falla `UNSUPPORTED_EXECUTION_COMMAND`; no conversión a MARKET ni descarte. |

Matching no depende de que Strategy esté ready; una protección física resting sigue viva. GTC sobrevive intervalos cerrados. La sesión negociable sale del Calendar; una pérdida de conexión del cliente no apaga una orden retenida en el venue simulado. Una fixture de desconexión puede retrasar entrega de hechos, no borrar ejecución física.

El modelo tiene liquidez suficiente al lado declarado, cero profundidad/queue priority/market impact y slippage fijo. No inferir partial fills del volumen de un trade. El dominio sí procesa partial fills, y el laboratorio los inyecta explícitamente para probar carreras/finality.

### 12.3 ACK y finality

Al aceptar una orden, emitir ACCEPTED/WORKING con correlación del comando. Al cancelar, emitir ActionObservation CANCEL CONFIRMED; después status terminal y, una vez entregados todos los fills ya sellados, un OrderObservation independiente `TERMINAL_EXECUTION_FINAL`.

ACK no pone q_exec_max en cero. La liberación de claims/grants y la continuación de MM pasan por finality real. Cancel demasiado tarde produce evidencia too-late/rejected consistente; no deshace un fill. Cancel+new mantiene el claim anterior hasta su finality y exige el camino normal para la orden nueva.

TIF vacío requiere un valor en el execution_model. Los dos ejemplos fijan GTC. DAY expira en cierre de sesión del instrumento y emite EXPIRED más finality; no confundirlo con el cutoff Provider. No se expiran GTC por EOF.

Comando repetido con mismo command_id y términos idénticos es idempotente; términos diferentes con el mismo ID son conflicto fatal. IDs nativos simulados se derivan de orden y ordinal de ejecución, por ejemplo `sim-order:<order-id>` y `sim-exec:<order-id>:<fill-ordinal>`. Son identidad del venue simulado y no reemplazan IDs nativos faltantes en evidencia LIVE importada.

### 12.4 Hechos y rutas

| Hecho | Ruta |
| --- | --- |
| OrderObservation / OrderActionObservation | Operation owner correlacionado; no inferir owner por “Operation actual”. |
| ExecutionFill | Ledger dedup por execution_account_id + provider_execution_id; luego shared ExecutionUpdate/Operation y CapacityUpdate. |
| PositionObservation | Cuenta+contrato: baseline cero y updates de net físico; reconciliación separada, nunca fill sintético. |
| ExecutionSessionObservation | Cuenta/binding; startup CONNECTED/AUTHENTICATED y eventos declarados. No se convierte en input de Operation. |

La señal de conexión no acredita readiness por sí sola. Las observaciones usan los tipos existentes; no se transportan envelopes Kafka dentro del proceso. La correlación original del comando se retiene para fills tardíos, incluso después de contraer estado terminal.

### 12.5 Laboratorio de ejecución acotado

Una fixture puede retener/liberar una observación conocida, duplicarla, inyectar partial/late/wrong fill o un error definido. Cada paso identifica la coordenada causal y el payload; su digest entra en RunSpec. No hay DSL, generador aleatorio ni plataforma de escenarios.

Nunca inyectar finality si todavía existe un fill programado posterior para esa orden. Los tests de post-finality ilegal deben identificarse como anomalía deliberada y producir mismatch/failure. No filtrar anomalías antes del shared handler para que el backtest aparente converger.

## 13. Determinismo e identidad

### 13.1 RunID, controles y build

`input_sha256 = SHA256(canonical_v1(ImmutableInputs))`. ImmutableInputs incluye build/code, dataset lógico/range, config resuelta, catálogo/schedule, initial state, calendarios/tzdata, política y expansión de planes, contextos/controles aceptados y modelos. Excluye run_id derivado, representación física alternativa/receipt, paths locales, credenciales, host, duración, intentos y destino de publicación. ConfigSnapshot.Run se hashea sin el ID derivado y se liga después, evitando recursión.

| Modo | Identidad y cierre |
| --- | --- |
| CLOSED_SPEC | Todos los inputs están fijados antes de ejecutar; `run_id=bt-<input_sha256 completo>`. |
| CALLER_CONTROLLED | El caller fija control_namespace no vacío y BaseImmutableInputs antes de NewRun. `base_spec_sha256=SHA256(canonical_v1(BaseImmutableInputs))`; `run_id=bt-c-<SHA256(tuple(version,base_spec_sha256,control_namespace))>`. Namespace, modo y controles inicialmente declarados forman parte del base; no hay reloj de pared/RNG oculto. |
| Manifest final del modo controlado | ImmutableInputs añade la lista append-only de admisiones con payloads/digests, ordinal, effective_at y frontera de admisión, incluidos controles pendientes más allá del horizonte. input_sha256/control_sequence_sha256 se cierran al Finish/aborto; no cambian RunID ni IDs ya emitidos. |

CALLER_CONTROLLED no pretende que RunID sea el hash de datos futuros desconocidos. El caller asigna un namespace distinto a cada experimento causal. Mismo base/namespace y misma secuencia de admisiones reproducen exactamente los mismos IDs/records/resultado; el reproducer conserva ese modo y reproduce las admisiones en sus fronteras. Reusar namespace/base con otros inputs finales es `RUN_INPUT_CONFLICT` al comparar un resultado/registro ya existente: exclusión local y publicación create-if-absent preservan el anterior, sin overwrite. No hace falta un servicio nuevo de coordinación.

Todo owner y fact recibe RunProvenance BACKTEST con el RunID estable desde el principio. CLOSED_SPEC y CALLER_CONTROLLED equivalentes económicamente tienen identidad/provenance distinta por contrato; una comparación entre modos debe nombrar esa diferencia, nunca prometer igualdad byte a byte de dos specs distintos. La prueba exacta de determinismo conserva modo/namespace/admisiones.

Una nueva versión de código cambia la identidad normal. Una comparación diagnóstica contra otro build puede conservar el namespace del baseline, identificando ambos builds y publicando sólo bajo attempts, nunca sobre su resultado canónico.

### 13.2 IDs dentro del estado compartido

F05 requiere dos cursores persistidos en `operation.OwnerState`: issued_operation_ids e issued_order_ids. Incrementar sólo en el clone. El allocator recibe `IDRequest{RunID,OwnerKey,Ordinal}` en métodos separados por kind; devuelve prefijo de tipo + SHA-256 completo del tuple con longitud de campos explícita. Validar ordinal positivo y overflow. No mantiene contadores externos.

LIVE conserva el adapter UUIDv7. IDs de admission, reservation, revalidation y cancel siguen sus derivaciones reales. Provider mantiene su DecisionSeq clonado. Un error abandona los cursores candidatos; el retry desde estado previo obtiene las mismas identidades deterministas. [S09] [S23]

### 13.3 Orden, aislamiento y representación

Ordenar keys antes de emitir effects, asignar IDs, elegir un ganador, desalojar por empate o devolver “primer error”. Mantener slices semánticos. Provider safety conserva orden de familias y keys lexicográficas dentro de cada familia; eviction usa `(seen_seq,key)`. No basta sortear JSON o los resultados al final. [S14]

Canonicalización `echo-json-v1`: schema tipado, map keys lexicográficas, arrays con orden semántico, secuencias enteras, timestamps UTC RFC3339Nano, decimales exactos de units. Canonicalizar JSON opaco sin float64; NaN/Inf, punteros y localizaciones de hora no son datos lógicos.

El recorder es run-local. `obs` tiene sink/clock globales y no es autoridad de evidencia; no llamar SetSink/SetClock por corrida. Timing y métricas de host permanecen en logs/receipt externos. Los wrappers de observación preservan exactamente las interfaces opcionales del objeto observado. [S24] [S10]

## 14. Errores y retry

| Situación | Resultado |
| --- | --- |
| Admission denegada, readiness insuficiente declarada, consistency todavía no cumplida | Outcome válido del dominio, con evidencia; no es error del runner. |
| Fail de cuenta conforme al modelo y cierre asentado | Run puede ser COMPLETE con lifecycle FAIL. |
| Input inválido, checksum/lectura fallida, autoridad requerida irresoluble, unidad no soportada, invariantes rotas, callback error/panic | Cortar en la primera causa; FAILED. |
| Horizonte consumido pero condición obligatoria de finalización/valuación incompleta | INCOMPLETE con razón y residuales. |
| Usuario/interrupción operativa antes del horizonte | INCOMPLETE si se puede cerrar diagnóstico; nunca COMPLETE. |
| Upload timeout/conflicto | Estado de publicación separado; no altera una simulación finalizada. |

No skip-and-continue, fallback de datos, retry in-place ni “recuperación” desde estado posiblemente mutado. Un panic sólo se recupera en el límite del run para guardar el primer fallo y salir. Reintentar simulación significa un run fresco desde inputs exactos. Reintentar publicación sólo reenvía bytes ya cerrados.

Abortar evita seguir dañando el experimento, pero no cierra F05 ni ningún bug compartido. Sus regresiones deben demostrar el comportamiento correcto del owner en error/retry.

## 15. EOF, finalización y COMPLETE

El período de mercado es [trade_start,end_exclusive). Al llegar a end_exclusive, procesar transiciones/controles/timers ya requeridos hasta ese límite y drenar consecuencias inmediatas. No aceptar market con timestamp == end_exclusive, avanzar más allá para conseguir un fill, reciclar el último tick ni fabricar un cierre de barra parcial.

Cerrar sólo barras cuyo boundary real se alcanzó; las demás quedan forming. Los timers futuros permanecen residuales. Un order generado por el último tick no llena sobre ese mismo tick.

`REPORT_RESIDUALS` permite COMPLETE al haber ejecutado correctamente el horizonte: account puede seguir ACTIVE, con posiciones valorizadas, órdenes, claims, reservas, pending admission y timers futuros explícitos. No confundir ese COMPLETE con cuenta flat, evaluación pasada ni realización del unrealized.

`REQUIRE_FLAT` necesita un cierre causal previo y datos ejecutables posteriores dentro del horizonte. Si faltan, INCOMPLETE; nunca venta al último precio. Business FAIL/PASS detiene nuevas entradas de la etapa y asienta la ejecución requerida. Con outcome_handling=STOP puede completar en ese stop contractual; con AWAIT_CONTEXT conserva el outcome y procesa el siguiente contexto explícito o continúa hasta el horizonte bloqueado en AWAITING_NEXT_CONTEXT. Si un asentamiento obligatorio no converge antes del horizonte, INCOMPLETE preservando ese outcome parcial.

Condiciones conjuntas para COMPLETE:

- Inputs previstos consumidos y validados hasta el stop contractual.
- Cola inmediata drenada, sin error ni hecho físico sellado sin aplicar.
- Valuación final válida para toda posición neta y cobertura declarada.
- Residuales compatibles con end_policy y listados íntegramente.
- Lifecycle de cada etapa, estado de continuidad y execution_state separados; counts/digests/schema completos.
- Admisiones selladas; todos los controles aceptados constan en ImmutableInputs como aplicados o pendientes, sin efectos atribuidos a tiempo futuro.
- Gzip local cerrado y verificable.

Una caída del publisher no invalida estas condiciones locales; tampoco convierte un fallo del engine en COMPLETE.

## 16. Contrato de resultado y evidencia

### 16.1 Un artifact autocontenido salvo corpus durable

`runs/<run-id>/result.json.gz` contiene un documento `echo.backtest.result.v1`. No requiere MongoDB, event sourcing, base analítica o guardar todos los ticks duplicados.

| Campo top-level | Contenido |
| --- | --- |
| `schema_version` | `echo.backtest.result.v1`. |
| `run` | RunProvenance existente. |
| `records` | Array ordenado escrito por streaming después de schema_version/run. |
| `inputs` | ImmutableInputs final; base/config/initial state, catálogo/schedule, políticas/rows expandidas, contextos/cashflows/admisiones inline y refs durables verificables de corpus lógico/build/calendario. |
| `input_sha256` | Digest final de inputs; base_spec_sha256/control_sequence_sha256 explícitos cuando corresponde. |
| `summary` | Execution state, terminal_reason, último tiempo/cursor, counts, lifecycle, economía/días, residuales, state digests y fidelidad/cobertura. |
| `first_error` | Null para COMPLETE; primer capsule de fallo cuando corresponda. |
| `integrity` | Canonicalization/version, hash_algorithm, record_count, records_sha256, input_sequence_sha256 y logical_sha256. |

El orden top-level V1 es schema_version, run, records, inputs, input_sha256, summary, first_error, integrity. El writer abre records inmediatamente y escribe los inputs finales después de cerrar el array; esto permite caller controls sin retener records en RAM, reescribir IDs ni reconstruir un gzip abierto. Las admisiones sin aplicación aún no tienen efecto de dominio: su evidencia está en el manifest final con frontera y secuencia. El resumen incluye contabilidad total y por etapa/contrato, selecciones/controles aplicados y pendientes.

Cada record tiene `{record_seq, coordinate, owner_kind, owner_key, kind, payload}`; la secuencia comienza en uno. El kind define exactamente un payload tipado; no aceptar variantes desconocidas silenciosamente.

| Kinds | Payload/evidencia |
| --- | --- |
| STRATEGY_EVALUATION | Input/ref, before/after digest, config, eval/cycle seq, ContextRead ordenados, output y absorbed/no-signal. |
| MM_EVALUATION | Trigger real, call ordinal, MMInput digest, economía observada, RuleSet/contract/claims/fills/MMState digests, market reads y MMDecision real. |
| OPERATION_APPLY | Input/owner/Operation before-after, economía efectiva, estado completo hash y ordered effects; incluye no-op/denied. |
| PROVIDER_APPLY | Input, snapshot/RuleSet/binding, capacity/safety digest y decisions/grants/revalidation/ForceClose exactos. |
| SIGNAL / COMMAND | `domain.Signal` y `operation.OrderCommand` reales. |
| ORDER_OBSERVATION / ORDER_ACTION_OBSERVATION / FILL | Tipos reales; fill agrega eligibility ref, price sources y coste atribuido. |
| POSITION_OBSERVATION / EXECUTION_SESSION_OBSERVATION | Tipos reales, ruta account-level. |
| OPERATION_FACT / PROVIDER_FACT | Facts de dominio antes de contraer estado terminal. |
| ECONOMICS | Una revisión completa por cambio; decisiones la referencian. |
| ACCOUNT_LIFECYCLE | Outcome por etapa y continuidad con causa, contexto y cobertura. |
| CONTRACT_SELECTION / STRATEGY_CONTRACT_ACTIVATION | Control/schedule, selección anterior/nueva, gate, readiness, ciclo drenado, candidato descartado y referencias retenidas. |
| ACCOUNT_CONTEXT_TRANSITION | Contextos before/after, state_modes/seed y validaciones de quiescencia; refs de la revisión/Provider Apply producidos. |
| ACCOUNT_CASHFLOW | Identidad/payload/treatment, delta, balance/floors/headroom before/after y efectos económicos; duplicado no vuelve a asentar dinero. |

Envelope de evaluación común: `input_kind,input_ref,input_sha256,before_state_sha256,reads_sha256,output_sha256,after_state_sha256,output_record_refs,outcome/reason`. Hash de estado incluye MMState y bookkeeping relevante, no sólo la proyección pública.

Se conserva una evaluación compacta por cada llamada Strategy/MM/Provider y transición Operation, incluyendo no-action, dedup y denegaciones. No retener en RAM todas esas llamadas ni copiar RuleSet/fills/Operation completos en cada quote. Guardar valores pequeños leídos, versiones/digests y refs de outputs únicos; el prefijo reproducible reconstruye el resto.

`input_sequence_sha256` acumula cada input externo consumido, incluso candidato duplicado, más controles/sesiones/timers en orden; el record digest acumula records canónicos con framing por longitud. `logical_sha256` cubre schema/run/inputs/digests/summary/first_error, excluyendo su propio campo. SHA-256 de bytes gzip va en receipt/publicación externa para evitar autorreferencia.

### 16.2 Qué observó realmente cada decisión

Strategy abre `NewLiveScope` sobre el read model histórico run-local; el nombre del scope no cambia BACKTEST a LIVE. Captura lecturas efectivas en orden. CurrentMarketView puede contener trade, quote y last-known; un solo quote ID no reemplaza todo ese valor. Mantener el valor acotado inline cuando sea necesario para resolverlo exactamente. [S07] [A05]

Un decorator de MoneyManager invoca GerardMM real una vez y captura el MMInput efectivo después del override DeliveredEconomics. Envuelve Mark/Ready y, sólo si existía, ExecutableQuoteSource. Registra contract, valor/ok, ref/version y capacidad disponible. No obtiene “economía observada” mirando Views antes de buildMMInput. No expone una capacidad BBO que quoteScopedMarket escondía. [S09] [S10]

Provider observa su input y estado; registrar esos valores/revisiones y la autoridad completa referenciada. No fabricar lecturas de un contexto que ese engine no usa. El recorder no corrige, redondea ni reordena una decisión para que coincida.

### 16.3 Métricas post-hoc

Result puede calcular net/gross PnL, fees, número de fills/Operations, win rate definido sobre Operations cerradas, exposure/time, drawdown observado, duraciones y resultados por día. Las fórmulas y tratamiento de operaciones censuradas se declaran.

Reclasificar una cuenta como prop después de trades genéricos sólo es válido como métrica descriptiva contrafactual claramente limitada. Nunca sustituye el run con restricciones si éstas alteran admission, qty, forced close, MM, continuidad o payout/balance.

## 17. Persistencia local y MinIO/S3

1. Crear spool local exclusivo por intento. Escribir schema/run y records por streaming; al sellar, escribir inputs finales, input digest, summary/first_error/integrity en el orden de §16.
2. Cerrar gzip con compresión fijada, mtime cero, nombre/comment vacíos y representación estable; cerrar/sync archivo.
3. Reabrir, decodificar y verificar schema/counts/digests. Finalizar localmente por rename atómico bajo exclusión del run-id; si ya existe, comparar contenido y no reemplazar un resultado diferente.
4. El publisher externo sube bytes cerrados directamente a `runs/<run-id>/result.json.gz` con create-if-absent `If-None-Match: *` y checksum. No HEAD seguido de PUT incondicional.
5. Timeout ambiguo/precondition: GET del objeto existente y comparación SHA-256 verificada. Igual es éxito idempotente; distinto es `RUN_ID_CONFLICT` (o RUN_INPUT_CONFLICT si el namespace controlado se reutilizó con otros inputs) y queda intacto; estado no verificable sigue pendiente/fallido.
6. Retry de upload conserva exactamente el archivo. Logs/receipt contienen intentos, wall time, backend y resultado; no entran en el contenido lógico.

AWS documenta publicación íntegra de PutObject y escritura condicional; MinIO AIStor publica compatibilidad de If-None-Match. Esto no acredita la versión desplegada en Aranea. S02 debe verificar las semánticas del backend configurado en un prefijo aislado. [W01] [W02] [W03]

Usar single PUT dentro del límite certificado del backend; adapter V1 fija techo conservador de 5,000,000,000 bytes y valida contra la capacidad declarada si es menor. Sobre el límite, conservar el resultado local y devolver `PUBLISH_SIZE_UNSUPPORTED`. Multipart queda diferido hasta requerirlo y certificar su commit condicional; no se truncan decisiones para entrar.

FAILED/INCOMPLETE se guardan como diagnósticos válidos bajo `attempts/<run-id>/<attempt-id>/failure.json.gz`, sin ocupar el key canónico COMPLETE. No staging/copy/marker remotos, MongoDB ni servicio adicional. Secrets y endpoints operacionales se resuelven fuera de RunSpec y no se publican.

## 18. Laboratorio: reproducción y primera divergencia

El flujo requerido queda concreto: sospecha runtime/domain → fixture histórica con inputs suficientes → reproducción baseline → primera divergencia → fix compartido → regresión → mismo fix heredado por runtime.

`reproduce <result>` resuelve y valida build/dataset/config/state, ejecuta el mismo driver desde el inicio y compara records/effects/IDs/tiempos/lecturas/estados/economía en orden. Record extra/ausente, hash distinto o campo distinto detiene la comparación en la primera coordenada. Igual PnL o lista de trades no basta.

El primer capsule contiene:

- Tipo/código de fallo, coordenada, owner y causa.
- Record esperado/obtenido y primer field path material diferente cuando se disponga del valor.
- Input exacto y estado anterior del owner; MMInput completo si hubo llamada MM.
- Lecturas observadas, versión económica/Provider y efectos pendientes del callback actual.
- Builds esperado/candidato, digests de inputs y comando reproducible.

No promete extraer un workState privado de un Apply fallido. El before-state, input y llamada real capturada permiten repetirlo. No se guardan snapshots globales por cada tick ni se introduce event sourcing.

Para reducir un repro, conservar un prefijo suficiente para warm-up, autoridad, economía y estado previos. Cortar una semana de precios sin la historia que formó el estado no es reproducción equivalente. El command puede frenar al mismatch y materializar sólo ese contexto; un replay de una decisión Strategy mediante ReplayScope exige consumir exactamente todos sus reads y before-state reales.

### 18.1 Claims permitidos

| Claim | Evidencia exigida |
| --- | --- |
| Run repetible | Igualdad exacta del resultado lógico y bytes gzip bajo build fijado. |
| Domain parity de un fixture | Mismos inputs/estado/reads y resultados de las autoridades compartidas. |
| Fix heredado por LIVE | Cambio en SDK/transición compartida, shells llaman esa misma implementación y regresión local correspondiente pasa. |
| Exact replay de decisión | Corpus completo de before-state, trigger, reads/config y expected; consumo exacto de reads. |
| Broker/infra parity | Fuera de V1 salvo prueba física específica; BACKTEST no acredita NinjaTrader, red, StateFun, journals o latencia ausentes. |

## 19. BT-F01…BT-F05: semántica, reproducción y cierre

**OWNER / MANAGER FROZEN.** Los cinco siguen en el programa. S01 no los repara ni les asigna cierre final. S02 puede corregir un finding que bloquee físicamente su implementación; S03 debe intentar reproducir/verificar los cinco; S04 cierra todos los confirmados. Estados finales únicos: `CONFIRMED_FIXED_WITH_REGRESSION` o `DISPROVED_WITH_EVIDENCE`. DOCUMENTED no cierra. [A01]

### BT-F01 — AccountSnapshot sin RuleSet

**SOURCE FACT.** AccountSnapshot invoca monitorConsistency y éste puede dereferenciar RuleSet nil antes de comprobar autoridad. [S14] (líneas 105–110) [S18] (líneas 54–55)

Semántica: aceptar/conservar un snapshot válido sin panic; ausencia/tombstone/no-ACTIVE de RuleSet impide evaluar la familia y nuevo riesgo permanece fail-closed. No convertir autoridad ausente en pass de consistencia.

Repro/regresión compartida `provider/bt_f01_test.go`: snapshot antes de config, después de tombstone y después de distribución no-ACTIVE; luego restauración válida. Cubrir campos de consistencia presentes/ausentes, currency errónea y límites del monitor. Test baseline debe localizar el nil path; fix mínimo es el guard compartido, no ordenar siempre config primero en el runner.

### BT-F02 — Orden nondeterminista de ForceClose

**SOURCE FACT.** sweepSafety itera LiveStrategies map y emite efectos; eviction de live strategy puede desempatar según primer map entry. [S14] (líneas 141–229)

Semántica: mantener orden de familias `forced_flat_cutoff, daily_loss, trailing_drawdown, news` y account-strategy keys lexicográficas por familia; desempate de eviction `(seen_seq,key)`. El suplemento ocupa `program_required_flat` inmediatamente después de `forced_flat_cutoff`, preservando el orden relativo de todas las familias existentes.

Repro/regresión `provider/bt_f02_test.go`: varios owners y varias familias simultáneas, permutaciones de inserción/eviction y procesos independientes. Comparar el slice bruto de effects y comandos/IDs downstream, antes del exporter. Una estrategia o cien iteraciones casualmente iguales no disprueban un map sin orden.

### BT-F03 — Provenance LIVE fabricada

**SOURCE FACT.** Provider crea ForceClose con LIVE y run-id de safety. El handler de Operation no usa esa provenance para fabricar sus comandos, que toman la de la Operation. Es un defecto de provenance; no demuestra egress LIVE. [S14] (líneas 179–193) [S11] (líneas 808–888)

Semántica/fix target: `provider.NewEngine(run domain.RunProvenance)` recibe identidad inmutable validada. Wiring Core agrega Run a FuturesProviderRulesConfig y lo obtiene de ConfigSnapshot.Run; Backtest usa RunSpec. Safety copia exactamente esa provenance, conservando ForceCloseID de episodio.

Regresión `provider/bt_f03_test.go` y wiring: LIVE/BACKTEST/EXACT_REPLAY, varias familias y nueva estrategia durante episodio ya activo; assert facts y ForceClose exactos, sin namespace fabricado. No reparar los efectos dentro del runner.

### BT-F04 — Fill tardío/ajeno atribuido a la Operation actual

**SOURCE FACT.** El branch post-terminal/foreign de handleFill llega a un constructor que puede leer Operation nil o atribuir A a B; beginEvent también puede avanzar Runtime.EventSeq de B. La prueba existente del mismo terminal A no cubre A terminal → B viva. [S11] (líneas 291–433) [S09] (líneas 345–421)

Semántica: conservar account/strategy/operation/order/provider-execution originales. A no revive; B mantiene íntegros Operation, Runtime, MMState, fills, órdenes, exposición, claims y la economía efectiva/contexto que habría observado sin ese sidecar. Puede avanzar una secuencia audit del owner sin fingir mutación de B. Run provenance sale de correlación original retenida; si no se resuelve, UNKNOWN explícito, nunca el run de B por conveniencia.

Regresiones `operation/bt_f04_test.go`: owner vacío; A terminal/B actual y fill nuevo de A; duplicado de A ya cobrado; orden inexistente/foreign account/strategy; fill corriente válido. Fixture integrada modifica net físico por fill nuevo de A y muestra mismatch/safety sin transferencia falsa a B. Dedup económico por cuenta+execution ID durante todo el run. No filtrar IDs antiguos antes de Apply.

### BT-F05 — IDs consumidos fuera del clone

**SOURCE FACT.** NewOperationID ocurre antes de validación/MM; NewOrderID puede consumirse antes de un error posterior. El allocator determinista actual mantiene cursores fuera de OwnerState. [S09] (líneas 661–743 y 935–956) [S23]

Semántica/fix target: §13.2. Estado, efectos y cursores se comprometen juntos. LIVE UUIDv7 mantiene su naturaleza; la repetición determinista corresponde al allocator BACKTEST.

Regresión `operation/bt_f05_test.go`: MM error después de materializar; segunda request inválida después de asignar la primera orden; fallos repetidos; serialize/restore; owners/runs independientes; retry vs baseline fresco sin fallo. Assert estado/counters intactos, cero effects y mismos IDs del éxito. Dos runs limpios o abortar antes de retry no cierran este finding.

### 19.1 Evidencia mínima de disposición

Cada finding tiene source/semántica, comando/caso baseline, resultado observado, shared diff si aplica, regresión nombrada, build y evidencia local. Si S02 lo corrige, S03 verifica independently su repro/fix; no desaparecerá de la matriz. Si queda pendiente en S02, se declara `PENDING_S03_REPRODUCTION` y nunca aprobado por omisión. Sólo evidencia que descarte la hipótesis bajo sus precondiciones permite DISPROVED_WITH_EVIDENCE.

## 20. Matriz de aceptación local

Esta matriz es obligatoria para S02 salvo las expansiones adversariales/closures F01–F05 expresamente asignadas a S03/S04. BT-A37…BT-A60 son los casos añadidos por BT-S01A y pertenecen al mismo S02. Los nombres son IDs estables de evidencia; los nombres Go pueden seguir la convención del repo. No se ejecutó ninguno en S01/S01A.

| ID | Caso | Aserción material |
| --- | --- | --- |
| BT-A01 | Extracted Market/Analytics vs shells con mismo input/state | Mismos next-state y ordered effects; shells sólo adaptan I/O y preservan wire/state. |
| BT-A02 | Warm-up S1/S2 con señales atractivas en prehistoria | Cero Signal/ciclo abierto; mismos OR/H4/BB del pipeline; primera decisión normal correcta. |
| BT-A03 | Primer trade de boundary + segundo al mismo T | Barra anterior excluye primero; orden no llena en causa, sí puede en segundo. |
| BT-A04 | Boundary sin tick; sesión/break/early close en T | Timers y precedencia correctos; cero barras fuera del grid. |
| BT-A05 | Timer viejo después de nueva barra y cambio de calendario | No cierre nuevo por generación reutilizada; boundary/id válidos. |
| BT-A06 | Epoch/recovery, duplicate/conflict y repeated equal-price ticks | Guards reales, identidad distinta cuando corresponde, cero reeval retrospectivo. |
| BT-A07 | Contrato desconocido, catálogo/schedule inválido y multicurrency | Miss exacto o error preflight nombrado; Mark/Ready nunca sustituyen por contrato corriente. Rollover válido se acepta. |
| BT-A08 | Inputs/config faltantes, tabla directa con day3 sin row, Warmup incompleto | Fallo explícito, cero fallback; el materializador correcto se prueba por BT-A43/44. |
| BT-A09 | MARKET BUY ask100.75, tick.25, slip1 | Fill101.00 posterior a aceptación; comisión una vez. |
| BT-A10 | SELL stop99.50, BBO98/98.25, trade98, slip1 | Trigger LAST; fill97.75; no fill99.50 inventado. |
| BT-A11 | BID nuevo/ASK viejo, quote future, TRADE_MODEL | Freshness por lado; sin lookahead; provenances y cadence declarados. |
| BT-A12 | Dos matches sellados; primer feedback causa cancel/M1 directo | Segundo match permanece; Position compara prefijo completo; NEW precede su CANCEL; nuevas órdenes esperan cursor. |
| BT-A13 | CANCEL ACK → late partial fill → finality | q_exec retenido; costes/exposición una vez; close residual correcto. |
| BT-A14 | Protective stop + profit exit/cancel+new | No double-close ni liberación temprana; continuación real MM. |
| BT-A15 | Revalidation INVALID y PER_ORDER-only | Cero submit en invalid; camino real directo en caso sin shared cap. |
| BT-A16 | Command/fill/ACK/finality duplicados y payload conflict | Idempotencia nativa; conflicto visible, sin segunda comisión. |
| BT-A17 | Entry expiry pre-M1/post-M1 y fill al deadline | Revocar vs cancelar; fill gana; grant tardío no revive entry. |
| BT-A18 | Fill + economía vs DeliveredEconomics anterior | Una llamada FILL; exposición y revisión actuales, no ACCOUNT_ECONOMICS previo. |
| BT-A19 | QuoteUpdate y ACCOUNT_ECONOMICS independiente al mismo T | Una QUOTE con sidecar; la causa independiente conserva su llamada propia. |
| BT-A20 | Dos Operations opuestas, FIFO partial y reversal | Net físico y balance exactos; sin spread doble ni ownership falso. |
| BT-A21 | Fees opening/closing, mark faltante y cuenta flat | Dinero exacto/dedup; fresh falso si requerido; flat vale balance. |
| BT-A22 | Account-day/DST, posición overnight y fees | Fórmula §9 exacta, baseline correcto, MM plan anterior pinneado. |
| BT-A23 | DLL, EOD ratchet/cap e igualdad; mark sin fills; no intraday ratchet | Snapshot/risk/safety actualizados antes de nueva señal; freshness vence sin tick; breach terminal latcheado. |
| BT-A24 | Consistency justo30%, total<=0, target con exposición y mínimo de días 0/nil/positivo | Shared evaluator exacto; días únicos por fill; nil no habilita pass; sin pass anticipado ni fail inmediato por consistencia. |
| BT-A25 | Flat deadline sin tick, cancel ACK sin finality y reopen | Cierre por reloj; violación física vs fallo lógico; reopen sólo retira su bloqueo; terminal no revive. |
| BT-A26 | Generic de 20 días y GAU50 con mismo motor/corpus compatible | Restricción cambia secuencia/sizing/admission/continuidad; ejemplos de políticas explícitas, cero post-hoc sustituto. |
| BT-A27 | Horizon dentro de barra/último tick crea orden/residuales | No fill futuro ni close parcial inventado; COMPLETE/INCOMPLETE según policy. |
| BT-A28 | Run dos veces, chunk size distinto, A/B/A y procesos nuevos | Igualdad exacta de records, IDs, economics, final state y gzip. |
| BT-A29 | Apply error/panic/recorder error | Primer error/capsule, ningún commit fallido ni COMPLETE falso. |
| BT-A30 | Mutar una observación/context read/orden de effects | Reproducer detiene primera divergencia y materializa contexto suficiente. |
| BT-A31 | Result parse, refs/digests y output truncado | Artifact válido completo o diagnóstico; no publicación parcial canónica. |
| BT-A32 | Publisher idéntico/conflicto/timeout/partial connection/size | Create-if-absent real; exact retry; conflicto intacto; local conservado. |
| BT-A33 | AdvanceUntil(T) vs Run cerrado; driver caller-controlled con payout futuro | Prefijo idéntico dentro del mismo modo/spec; ninguna observación >frontera ni cashflow futuro aplicado; no implementa campaign. |
| BT-A34 | F01–F05 | Casos directos de §19; matriz de disposición y evidencia, sin workaround del driver. |
| BT-A35 | Legacy SDK/Core/futuresvertical regression | Shared extraction/adiciones no rompen consumers; no claim físico D6 por estos tests. |
| BT-A36 | Dataset representativo de ticks + evidencia streaming | Reportar counts, memoria y tamaño; sin retener corpus/records completos en RAM. Sin SLA inventado. |
| BT-A37 | NQH→NQM→NQU en una cuenta/run, reapertura en cada selección | Balance, PnL, días, drawdown/Provider e IDs continúan; cada nueva Operation/orden/fill pinnea el físico vigente; un único resultado. |
| BT-A38 | Operation A viva después de seleccionar/activar B; mercado A detenido mientras B avanza | Quotes/stop/fill/cierre de A usan sólo A; B no dispara stop ni ejecuta MARKET A con una quote retenida; catálogo A retenido y posiciones A/B no se netean entre contratos. |
| BT-A39 | S1 y S2 reales: preparar B, drenar ciclo A, activar B | Indicadores/readiness por stream; cero mezcla/Signal de warm-up; A puede cerrar sin abrir otro ciclo; contadores globales conservados y primer trigger normal B posterior. |
| BT-A40 | OPEN A en vuelo, ALLOW tardío, PendingAdmission y DeferredOpen al cutover | EntryGate invalida el trabajo no materializado; recheck al materializar/promover; no operación A nueva ni atribución del OPEN A a B. |
| BT-A41 | A técnico vivo con Operation ya cerrada; caso inverso; A→B→C/A→B→A y preparaciones excesivas | Esperar cierre técnico para activar; si sólo resta finality física, B usa deferral real; máximo tres slots; schedule con sucesor no inmediato se rechaza y candidato vencido/ABA no resucita. |
| BT-A42 | Falta cobertura de A aún requerido; B prewarm sin exposición propia | INCOMPLETE OLD_CONTRACT_DATA_UNAVAILABLE sin precio B sustituto; prewarm B no genera revisión económica/MM espuria sobre A. |
| BT-A43 | Generic100K veinte account-days con GerardMM real | Veinte rows/selectores digeridos; trades/decisiones posteriores a day2 y en tramo final; sin rama generic ni fallback. |
| BT-A44 | Materializar N días, DST, días parciales/sin trades, gaps/duplicados/overflow | Tabla determinista y completa; ordinal explícito; row anterior sigue pinneada a Operation viva; errores antes de nueva decisión. |
| BT-A45 | Misma cuenta EVALUATION→FUNDED/INITIAL explícito y después cashflow | Cambio real de binding/RuleSet/terms/MM rows/límites/context/state; mismo RunID/account/ledger, IDs monótonos; nueva Operation consume plan FUNDED suministrado; payout no es PnL. |
| BT-A46 | Transición admitida hoy con exposición; al aplicar: posición por contrato, net opuesto, reserva/pending, cancel ACK o late fill programado | Admitir futuro no exige estar flat hoy; rechazo CONTEXT_NOT_QUIESCENT sólo si falta quiescencia efectiva, sin mutación parcial ni cambiar fecha; ciclo técnico solo no bloquea. |
| BT-A47 | Context transition en EOD/DST; off-boundary; timer/economics viejos | EOD viejo exactamente una vez, segmento parcial explícito, sin ratchet fuera de EOD; contexto/generación viejos no modifican el nuevo. |
| BT-A48 | PASS con STOP y AWAIT_CONTEXT; caller no entrega contexto o lo entrega después | Nunca PASS→FUNDED implícito; pausa en frontera completa; bloqueo persistente o continuación causal misma cuenta según control. |
| BT-A49 | Payout -500 flat con floor 98900; debit con posición abierta | E=99500/headroom600 en ejemplo; PnL/best-day/consistency intactos; debit puede disparar Provider safety antes de market; marca faltante no elimina dinero. |
| BT-A50 | Cashflow duplicate/conflict, reset credit/debit y revisión posterior | Asentar una vez incluso tras cambio de contexto; conflicto visible; dinero exacto; credit no deslatchea fail ni desplaza floor. |
| BT-A51 | Mismo dataset lógico: NDJSON una parte, chunks y otro adapter | Mismos origin refs/source_order, canonical inputs, IDs/records/estado/economía/gzip; sólo receipt físico difiere. |
| BT-A52 | Corpus grande streaming, lados quote en distintos chunks y corrupción | Buffers/RSS medidos; sin cargar corpus completo; un BID no rejuvenece ASK; schema/order/byte o normalized digest inválido falla explícitamente. |
| BT-A53 | Ingress tipado real Core vs historical para fill y quote correlacionados | Igual MMInput, next-state/MMState, market reads/capabilities y ordered effects con mismos clock/IDs/provenance/config. |
| BT-A54 | Ingress raw real Core con Views fresh viejo; actualización posterior | UNAVAILABLE/PnLFresh=false como histórico; fill/capacidad/protección conservados; sólo causa económica posterior válida restaura freshness. |
| BT-A55 | Parity: duplicate/late/foreign, contexto/revisión erróneos y error/retry | Guards antes del sidecar; B no muta por A; evidencia inválida no autoriza; clone/IDs rollback; no relectura latest ni trigger MM doble. |
| BT-A56 | Parity con allocators/provenance reales LIVE/BACKTEST y recorder | Diferencias sólo las nombradas por contrato; mismo path/semántica; wrapper no añade ExecutableQuoteSource. Config MM válida para ambas composiciones. |
| BT-A57 | CALLER_CONTROLLED: replay de admisiones, namespace repetido/conflictivo | Misma secuencia/fronteras exacta reproduce IDs/gzip; distintos inputs finales no sobrescriben resultado; Finish sella pendientes y nuevos controles se rechazan. |
| BT-A58 | Context y cashflow al mismo T; control en/pasado de frontera | Orden ordinal/control_id, expected_context exacto y snapshots antes de fase market; tiempo <=frontera rechazado; sin retroactividad. |
| BT-A59 | Preserve/reset/replace de etapa, día y risk seed | Balance sólo cambia por fill/coste/cashflow; seed no crea dinero; same-stage no borra terminalidad; START_NEW_STAGE archiva outcome y separa progreso. |
| BT-A60 | Cambio real de cuenta física, contexto incompleto y swap fallido | Otra ProviderAccountRef física exige otro run; autoridad incompleta rechazada; AccountContextUpdate no publica estados mixtos ni efectos tras error. |

Fixtures de modelo pueden usar precios artificiales mínimos, con contratos y unidades válidos. Diferenciar esas pruebas de una corrida sobre histórico externo real. Conformance MinIO usa backend/prefijo aislado autorizado; si el entorno no está disponible, conservar la prueba local y declarar esa parte NO_VERIFICADA, sin afirmar el gate de publicación completo.

## 21. Fuentes, alcance de evidencia y cobertura del mandato

Las fuentes de código están fijadas a Echo d361008b; las autoridades originales a Agents-OS b999eb3e y el artifact BT-S01 revisado a ab7766fd. HEADs refrescados al inicio y cierre; el delta concurrente de parser AddOn queda identificado en §0.1 y no cambia los seams compartidos. El mandato BT-S01A del Manager en esta sesión corrige el endpoint V1. Las decisiones nuevas no se presentan como funcionalidades ya implementadas.

| Ref | Fuente principal |
| --- | --- |
| A01 | BT-S00 aceptado y mandato BT-S01 de esta sesión. |
| A02–A04 | Proyecto/Technical SPEC y freeze D6. |
| A05–A06 | Identidad/exact replay D4-A1 y orden BACKTEST D2-06C. |
| A07–A10 | Claims/capacity, Provider authority, GerardMM y lifecycle Operation. |
| A11–A14 | Remediación D6, evidencia E2T congelada, BT-S01 revisado y delta concurrente de parser. |
| S01–S08 | Market/Analytics/views, identidad, Bars, clock, Strategy y S2. |
| S09–S16 | Operation/MM/ejecución/Provider y planes económicos. |
| S17–S26 | GAU50, consistencia, sim, warmup, unidades, módulos, IDs, observabilidad y GerardMM real. |
| S27–S34 | MKT07, Strategy config/triggers, Signal separation, MM selector, Core ingress y delta AddOn al cierre. |
| W01–W03 | APIs primarias de escritura S3/MinIO consultadas para publisher. |

[A01]: https://github.com/xKoRx/agents-os/blob/b999eb3ea2a9a9d2ded574e891e3f8bec8c275c2/main/10-projects/Echo%20Futures/artifacts/backtester-v1/Echo%20Futures%20%E2%80%94%20BT-S00%20Backtester%20Source%20Forensics%20and%20Architecture%20Direction.md
[A02]: https://github.com/xKoRx/agents-os/blob/b999eb3ea2a9a9d2ded574e891e3f8bec8c275c2/main/10-projects/Echo%20Futures/Echo%20Futures.md
[A03]: https://github.com/xKoRx/agents-os/blob/b999eb3ea2a9a9d2ded574e891e3f8bec8c275c2/main/10-projects/Echo%20Futures/Echo%20Futures%20%E2%80%94%20Technical%20SPEC%20V1.md
[A04]: https://github.com/xKoRx/agents-os/blob/b999eb3ea2a9a9d2ded574e891e3f8bec8c275c2/main/10-projects/Echo%20Futures/artifacts/d6-design-freeze-20261001/ECHO-FUTURES-D6-FINAL-DESIGN-FREEZE.md
[A05]: https://github.com/xKoRx/agents-os/blob/b999eb3ea2a9a9d2ded574e891e3f8bec8c275c2/main/10-projects/Echo%20Futures/Echo%20Futures%20%E2%80%94%20D4-A1%20Market%20Identity%20%2B%20Exact%20Replay%20Remediation.md
[A06]: https://github.com/xKoRx/agents-os/blob/b999eb3ea2a9a9d2ded574e891e3f8bec8c275c2/main/10-projects/Echo%20Futures/Echo%20Futures%20%E2%80%94%20D2-06C%20Live%20Replay%20Market%20Boundary.md
[A07]: https://github.com/xKoRx/agents-os/blob/b999eb3ea2a9a9d2ded574e891e3f8bec8c275c2/main/10-projects/Echo%20Futures/Echo%20Futures%20%E2%80%94%20D4-A2%20Exposure%20%2B%20Capacity%20Safety%20Remediation.md
[A08]: https://github.com/xKoRx/agents-os/blob/b999eb3ea2a9a9d2ded574e891e3f8bec8c275c2/main/10-projects/Echo%20Futures/Echo%20Futures%20%E2%80%94%20D4-A3%20Provider%20Authority%20%2B%20Pending%20Admission%20Remediation.md
[A09]: https://github.com/xKoRx/agents-os/blob/b999eb3ea2a9a9d2ded574e891e3f8bec8c275c2/main/10-projects/Echo%20Futures/Echo%20Futures%20%E2%80%94%20D4-B2%20Q13%20Gerard%20Hardscalping%20MoneyManagement.md
[A10]: https://github.com/xKoRx/agents-os/blob/b999eb3ea2a9a9d2ded574e891e3f8bec8c275c2/main/10-projects/Echo%20Futures/Echo%20Futures%20%E2%80%94%20D2-04%20Operation%20Order%20Fill%20Position.md
[A11]: https://github.com/xKoRx/agents-os/blob/b999eb3ea2a9a9d2ded574e891e3f8bec8c275c2/main/10-projects/Echo%20Futures/artifacts/d6-shot3-20261002/D6-SHOT3-PRE-EGRESS-REMEDIATION.md
[A12]: https://github.com/xKoRx/agents-os/blob/b999eb3ea2a9a9d2ded574e891e3f8bec8c275c2/main/10-projects/Echo%20Futures/artifacts/d6-earn2trade-preflight-20260930/DEEPRESEARCH-PASS-1-E2T-EXTERNAL-EVIDENCE.md
[A13]: https://github.com/xKoRx/agents-os/blob/ab7766fd74bed760cb9a9f151bc423948bec0d3f/main/10-projects/Echo%20Futures/artifacts/backtester-v1/Echo%20Futures%20%E2%80%94%20BT-S01%20Backtester%20V1%20Design.md
[A14]: https://github.com/xKoRx/agents-os/blob/48f5260c5803c061b4f4dcabcf246897d056e19b/main/10-projects/Echo%20Futures/artifacts/d6-config-parser-fix-20261003/D6-CONFIG-PARSER-FIX.md
[S01]: https://github.com/xKoRx/echo/blob/d361008bfe4aa54fe3d8b6380d290bf92e1f1c08/v3/core/internal/functions/futures_market_stream.go
[S02]: https://github.com/xKoRx/echo/blob/d361008bfe4aa54fe3d8b6380d290bf92e1f1c08/v3/core/internal/functions/futures_market_analytics.go
[S03]: https://github.com/xKoRx/echo/blob/d361008bfe4aa54fe3d8b6380d290bf92e1f1c08/v3/core/internal/futuresruntime/views.go
[S04]: https://github.com/xKoRx/echo/blob/d361008bfe4aa54fe3d8b6380d290bf92e1f1c08/v3/sdk/futures/market/ingress.go
[S05]: https://github.com/xKoRx/echo/blob/d361008bfe4aa54fe3d8b6380d290bf92e1f1c08/v3/sdk/futures/bars/builder.go
[S06]: https://github.com/xKoRx/echo/blob/d361008bfe4aa54fe3d8b6380d290bf92e1f1c08/v3/sdk/futures/domain/clock.go
[S07]: https://github.com/xKoRx/echo/blob/d361008bfe4aa54fe3d8b6380d290bf92e1f1c08/v3/sdk/futures/strategy/engine.go
[S08]: https://github.com/xKoRx/echo/blob/d361008bfe4aa54fe3d8b6380d290bf92e1f1c08/v3/sdk/futures/strategies/s2/s2.go
[S09]: https://github.com/xKoRx/echo/blob/d361008bfe4aa54fe3d8b6380d290bf92e1f1c08/v3/sdk/futures/operation/engine.go
[S10]: https://github.com/xKoRx/echo/blob/d361008bfe4aa54fe3d8b6380d290bf92e1f1c08/v3/sdk/futures/operation/mm.go
[S11]: https://github.com/xKoRx/echo/blob/d361008bfe4aa54fe3d8b6380d290bf92e1f1c08/v3/sdk/futures/operation/engine_inputs.go
[S12]: https://github.com/xKoRx/echo/blob/d361008bfe4aa54fe3d8b6380d290bf92e1f1c08/v3/sdk/futures/domain/execution.go
[S13]: https://github.com/xKoRx/echo/blob/d361008bfe4aa54fe3d8b6380d290bf92e1f1c08/v3/sdk/futures/operation/runtime.go
[S14]: https://github.com/xKoRx/echo/blob/d361008bfe4aa54fe3d8b6380d290bf92e1f1c08/v3/sdk/futures/provider/engine.go
[S15]: https://github.com/xKoRx/echo/blob/d361008bfe4aa54fe3d8b6380d290bf92e1f1c08/v3/sdk/futures/provider/state.go
[S16]: https://github.com/xKoRx/echo/blob/d361008bfe4aa54fe3d8b6380d290bf92e1f1c08/v3/sdk/futures/domain/economics.go
[S17]: https://github.com/xKoRx/echo/blob/d361008bfe4aa54fe3d8b6380d290bf92e1f1c08/v3/core/config/futures/gau50-eval-v1.json
[S18]: https://github.com/xKoRx/echo/blob/d361008bfe4aa54fe3d8b6380d290bf92e1f1c08/v3/sdk/futures/provider/consistency.go
[S19]: https://github.com/xKoRx/echo/blob/d361008bfe4aa54fe3d8b6380d290bf92e1f1c08/v3/futures-bridge/adapters/sim/scenario.go
[S20]: https://github.com/xKoRx/echo/blob/d361008bfe4aa54fe3d8b6380d290bf92e1f1c08/v3/sdk/futures/warmup/synthesize.go
[S21]: https://github.com/xKoRx/echo/blob/d361008bfe4aa54fe3d8b6380d290bf92e1f1c08/v3/sdk/futures/units/money.go
[S22]: https://github.com/xKoRx/echo/blob/d361008bfe4aa54fe3d8b6380d290bf92e1f1c08/.agents/rules/02-architecture-independencia-modulos.md
[S23]: https://github.com/xKoRx/echo/blob/d361008bfe4aa54fe3d8b6380d290bf92e1f1c08/v3/core/internal/futuresruntime/ids.go
[S24]: https://github.com/xKoRx/echo/blob/d361008bfe4aa54fe3d8b6380d290bf92e1f1c08/v3/sdk/futures/obs/obs.go
[S25]: https://github.com/xKoRx/echo/blob/d361008bfe4aa54fe3d8b6380d290bf92e1f1c08/v3/core/config/futures/rulesets.go
[S26]: https://github.com/xKoRx/echo/blob/d361008bfe4aa54fe3d8b6380d290bf92e1f1c08/v3/sdk/futures/gerardmm/gerardmm.go
[S27]: https://github.com/xKoRx/echo/blob/d361008bfe4aa54fe3d8b6380d290bf92e1f1c08/v3/core/internal/futuresvertical/mkt07_rollover_test.go
[S28]: https://github.com/xKoRx/echo/blob/d361008bfe4aa54fe3d8b6380d290bf92e1f1c08/v3/sdk/futures/strategy/config.go
[S29]: https://github.com/xKoRx/echo/blob/d361008bfe4aa54fe3d8b6380d290bf92e1f1c08/v3/sdk/futures/strategy/trigger.go
[S30]: https://github.com/xKoRx/echo/blob/d361008bfe4aa54fe3d8b6380d290bf92e1f1c08/v3/sdk/futures/domain/signal.go
[S31]: https://github.com/xKoRx/echo/blob/d361008bfe4aa54fe3d8b6380d290bf92e1f1c08/v3/sdk/futures/domain/separation_test.go
[S32]: https://github.com/xKoRx/echo/blob/d361008bfe4aa54fe3d8b6380d290bf92e1f1c08/v3/sdk/futures/gerardmm/config.go
[S33]: https://github.com/xKoRx/echo/blob/d361008bfe4aa54fe3d8b6380d290bf92e1f1c08/v3/core/internal/functions/futures_operation.go
[S34]: https://github.com/xKoRx/echo/commit/7fbd7e990ac6628df3e4cc2717e96efd83bfbbf6
[W01]: https://docs.aws.amazon.com/AmazonS3/latest/API/API_PutObject.html
[W02]: https://docs.aws.amazon.com/AmazonS3/latest/userguide/conditional-writes.html
[W03]: https://docs.min.io/aistor/developers/s3-api-compatibility/

### 21.1 Mapa de las 26 obligaciones

| # | Obligación | Resolución |
| --- | --- | --- |
| 1–3 | Engine, ownership, packages | §1–4. |
| 4–5 | Historical driver/causal ordering | §6. |
| 6–7 | Market/Bars/Context/Strategy reuse | §4–7. |
| 8–10 | GerardMM/Operation/Provider reuse | §8–10. |
| 11–12 | Account economics y SimExecution | §9 y §12. |
| 13–14 | Generic100K y prop | §10. |
| 15–16 | Lifecycle y campaña/bankroll | §11. |
| 17–18 | Market data y EOF | §5 y §15. |
| 19–20 | IDs y errors/retry | §13–14. |
| 21–22 | Result y MinIO | §16–17. |
| 23–24 | Lab/parity y F01–F05 | §18–19. |
| 25 | Acceptance tests | §20. |
| 26 | Contrato exacto S02 | Bloque final siguiente. |

### 21.2 Cierre del shot

BT-S01 conserva su revisión de arquitectura aceptada. BT-S01A es una enmienda GOD/CLOUD ONE-SHOT; tres revisiones acotadas cubrieron rollover/Strategy, contexto/planes/cashflow y paridad. La integración verifica las cinco correcciones y sus consecuencias necesarias sobre identidad/result/control, sin reabrir el motor. Una revisión independiente cerró tres ambigüedades: matching sólo con cursor del contrato propio, validación del límite de preparación y quiescencia comprobada al aplicar el control futuro. Validación estática de documento y autoridades; no se ejecutaron tests de producto ni un gate adversarial LOCAL. El artifact queda listo para freeze del Primary Technical Manager y emisión directa de BT-S02, sin otro design shot.

La continuidad y el registro de sesión quedan en Agents-OS por delta. Feedback sólo si hay fricción reusable comprobada. `PRO_CHAT_POOL_DELTA: 0` significa cero consumo confirmado por evidencia del host; aplicabilidad Chat/Work y consumo real no expuestos permanecen UNKNOWN. No se multiplica gasto por número de subagentes ni se inventa remaining/reset.

## BT-S02 IMPLEMENTATION CONTRACT

### Rol, entrada y objetivo cerrado

**NORMAL LOCAL, UN implementation shot.** Entrar con BT-S01 integrado con BT-S01A y frozen por Primary Technical Manager, baseline/branch confirmados en su mandato. Entregar Backtester V1 funcional conforme a este documento; no rediseñar arquitectura. Trabajar en branch/worktree aislado desde el baseline que indique Manager, respetando deltas posteriores; no editar worktree, despliegue, bundle, config canónica ni gates de D6.

**Autorización explícita:** el NORMAL LOCAL lead puede utilizar subagentes NORMAL locales, con tareas ONE-SHOT acotadas, para workstreams independientes cuando ayude. Pueden cubrir extracción shared-domain; driver/dataset; accounting/ejecución/lifecycle; result/persistencia/reproducción. Son colaboradores de implementación dentro del mismo BT-S02, no shots adicionales ni arquitectos independientes. BT-S01 frozen sigue siendo autoridad. El lead asigna ownership de archivos, coordina dependencias, integra, conserva source truth y responde por todos los tests, artifacts y gate final; no delega esa responsabilidad ni permite decisiones divergentes.

Si el baseline cambió, comparar sólo el delta material con este contrato y conservar autoridades vigentes. Una incompatibilidad real se reporta con evidencia concreta; no sustituir source activo por master antiguo ni abrir preguntas ya resueltas.

### Implementar y extraer

1. Crear v3/backtester, API NewRun/AdvanceUntil/EnqueueControl/Finish/Run y CLI run/reproduce/publish; añadir módulo al workspace.
2. Extraer Market/Analytics y feed/config según §4; Core/LIVE y BACKTEST llaman la misma transición. Mantener contratos serializados existentes con adiciones compatibles explícitas.
3. Componer Strategy/S1/S2/GerardMM/Operation/Provider reales y vistas exactas; warm-up compartido, ContractCatalog/Schedule, exact stream guards, DRAIN_CYCLE/activación, RolloverEntryGate y retención de contratos de §4.3/§7.
4. Implementar DatasetSource/Cursor, primer adapter NDJSON y adapter/fixtures de conformance; manifest lógico/representación y origen estable, lectura bounded-memory. Driver secuencial §5–6 con fases, controles, timers, fills sellados y quiescencia.
5. Accounting FIFO por contrato, suma account-level exacta, snapshots/revisión, account-days y risk projection §9–10. Materializador explícito Generic100K para cualquier horizonte finito solicitado; GerardMM no incorpora fallback.
6. Path compartido ExecutionUpdate/QuoteUpdate/Observation, normalizador y adapters tipado/raw reales Core e histórico; freshness fail-closed, guards, una llamada MM por causa y equivalencia §8.2. No escribir MMState/DeliveredEconomics directamente desde runner.
7. Entry-expiry schedule/revoke/cancel y error propagation compartidos; SimExecution §12 con tipos nativos, elegibilidad posterior, stop/gaps, ACK/finality, TIF, dedup y fixture lab acotada.
8. AccountProgramTerms/risk/lifecycle, AccountContextTransition/Provider AccountContextUpdate atómico, AccountCashflow y caller controls §11; preserve/reset/replace explícitos. Continuación real de una misma cuenta entre etapas, sin Campaign Simulator.
9. IDs/determinismo/namespace controlado §13 y F05; si un fix F01–F05 es necesario para el camino funcional, hacerlo en shared domain con baseline/regresión. No declarar cerrado el programa por este shot.
10. Records/inputs finales/digests, replay/primera divergencia, EOF, finalización local y publisher condicional §14–18; ejemplos Generic de veinte días y GAU50 íntegros, más fixtures de rollover y transición/cashflow.

### Reutilizar y packages autorizados

Reutilizar tipos/engines/domain policies existentes; no copiar fórmulas S1/S2/GerardMM/claims/reservas/consistency. Tocar únicamente targets/shells de §4, tests consumidores necesarios y manifests/go.work/go.mod requeridos. No importar Core internals desde backtester, reutilizar el harness como producto o incluir transports en el loop. Las helpers de selección/contexto/paridad son shared domain; los adapters sólo suministran hechos/evidencia.

### Tests que escribir y ejecutar localmente

Implementar BT-A01…BT-A60 con evidencia por ID. Tests de fixes de dominio junto al shared package; composición junto a runner/sim/store. F01…F05 directos conforme §19: S02 conserva repro/disposición pendiente si no cierra alguno, sin declarar una suite roja como verde. La ampliación de matriz no cambia el protocolo S03/S04.

Ejecutar desde módulos correspondientes con workspace/toolchain del repo:

- SDK: `go test ./futures/...`.
- Backtester: `go test ./...` y build de `./cmd/echo-backtest`.
- Core: tests de `./internal/futuresruntime`, `./internal/futuresvertical` y `./internal/functions`, incluido el ingress real de paridad y MKT07 con Strategies reales.
- Consumers adicionales de SDK IDs/Provider por búsqueda de call sites: compilar/testear superficie afectada; incluir futures-bridge si cambia su compilación.
- Conformance MinIO/S3 en prefijo aislado: creación, igualdad, conflicto, timeout ambiguo y no-publicación de spool abierto.
- Dos corridas idénticas, A/B/A, proceso fresco, layouts/chunks distintos y replay de controles con mismo namespace; comparar records/IDs/estado/economía/gzip. Medir corpus representativo y separar buffers, metadata, dedup y output.

No ejecutar órdenes contra brokers, egress LIVE, gates D6 pendientes ni cambios de infraestructura como parte de S02. Paridad de código/adapters no acredita la provisión económica física LIVE ni su despliegue.

### Artifacts obligatorios

Commit/branch limpio y diff revisable; README de ejecución/limitaciones; RunSpecs/manifests/fixtures completos; schema V1; resultados Generic de veinte días y GAU50 reproducibles; evidencia de continuidad NQ sobre >=3 contratos y EVALUATION→FUNDED con cashflow en la misma cuenta; capsule de primera divergencia; logs/comandos/build/counts de tests; conformance MinIO/estado de publicación; matriz BT-F01…F05 con evidencia/próximo responsable; mapping BT-A01…BT-A60 a tests/resultados. Reportar workstreams/subagentes usados y consolidación del lead sin tratarlos como shots nuevos.

Corpus/results grandes quedan en storage durable con digest; repo guarda fixtures pequeñas, manifests y reportes. No incluir credenciales ni copiar todo el histórico a documentación.

### Decisiones que NORMAL no puede reabrir

Un engine, una cuenta/instrumento lógico y múltiples contratos físicos por run; secuencial/in-process; SDK compartido real; fases/micro-order §6; rollover por schedule y pins, Strategy exacta por stream; economía causal y un path compartido hecho+economía; FIFO por contrato/account; Generic arbitrary-horizon por materialización explícita; transiciones/cashflows causales V1; GAU50 modelado con cobertura honesta; Sim sólo después de M1; ACK distinto de finality; órdenes nuevas no llenan en su causa; IDs dentro del clone; dataset lógico independiente del codec; result streaming/controles con identidad estable; create-if-absent; first divergence completa; fixes F01…F05 en shared domain; ningún cambio/gate D6.

Nombres/helpers/organización menor pueden seguir el repo si no cambian contrato. Parámetros obligatorios no se convierten en defaults ocultos. Los subagentes aplican estas decisiones, no las reinterpretan.

### Diferido

Múltiples instrumentos lógicos/portfolio, multicurrency/FX, futures curves generales y selección automática de roll por volumen/OI, migración automática de posiciones, series continuas sintéticas para análisis siempre etiquetadas como derivadas, LIMIT/native MODIFY, profundidad/queue/latencia aleatoria/Monte Carlo, optimización masiva, distribución intra-run, shared market bus, UI, Mongo/event sourcing, DSL/workflows, Campaign Simulator/compras/fees comerciales/bankroll/eligibility y settlement de payout, multipart no certificado, resume/checkpoints durables y certificación/despliegue físico LIVE.

Rollover longitudinal, Generic arbitrary-horizon, transición same-account, cashflows account-level y paridad shared **no están diferidos**. El codec productivo final puede elegirse con evidencia de workload/performance bajo el port congelado, sin modificar engine o dominio; NDJSON no es su formato estructural obligatorio. La automatización comercial de funded/payout queda fuera, pero el engine aplica el contexto y movimiento de cuenta entregados por caller en V1.

### Gate de salida

BT-S02 sale **listo para revisión de Manager y BT-S03 LOCAL adversarial** sólo si implementa este contrato, los casos funcionales/extracción/paridad/determinismo/longitudinal/contexto/resultados tienen evidencia verde, ejemplos/results son íntegros, publisher tiene conformance acreditada cuando se declara operativo y no hay excepción oculta. La matriz F01…F05 puede mantener pendientes explícitos de reproducción/cierre asignados a S03/S04; ningún finding bloqueante puede estar parcheado en runner ni impedir el camino funcional declarado completo.

Si falta un requisito, entregar estado exacto, repro y pendiente; no PASS global. BT-S03 verifica adversarialmente los cinco findings incluso si S02 corrigió algunos. BT-S04 cierra todo confirmado. El programa sólo termina cuando cada uno esté en **CONFIRMED_FIXED_WITH_REGRESSION** o **DISPROVED_WITH_EVIDENCE**, con fix compartido y evidencia local cuando corresponda.
