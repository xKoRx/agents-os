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
updated: "2026-10-03"
---

# Echo Futures — BT-S01 Backtester V1 Design

## Propósito

### 0. Dictamen y alcance de esta entrega

**BT-S01 deja un diseño implementable para revisión del Primary Technical Manager, con cero decisiones materiales de Owner abiertas.** Backtester V1 será un módulo Go que ejecuta una cuenta y un contrato físico, secuencialmente, sobre las autoridades compartidas de Echo Futures. El driver histórico ordena las causas; SimExecution produce hechos físicos; una autoridad económica de cuenta actualiza lo que GerardMM y Provider observan antes de la siguiente decisión.

El resultado del shot es este contrato de diseño. No se implementó product code, no se ejecutaron tests de Echo, no se inició BT-S02 y no se modificó ni certificó D6. Las pruebas descritas son trabajo obligatorio posterior, no evidencia de pruebas ya aprobadas.

### 0.1 Baseline inmutable y precedencia

| Autoridad | Baseline revisado | Consecuencia |
| --- | --- | --- |
| Agents-OS, proyecto y BT-S00 aceptado | `xKoRx/agents-os@b999eb3ea2a9a9d2ded574e891e3f8bec8c275c2`, `master` | Autoridades vigentes y entrada aceptada por Manager. |
| Echo Futures activo | `xKoRx/echo@d361008bfe4aa54fe3d8b6380d290bf92e1f1c08`, `feature/d6-shot1-execution-vertical` | Mismo baseline de BT-S00; no apareció un delta material en esa rama al refrescarla. |
| Echo `master` | `372af59a7b83604781346613da01e3d510ea1360` | Rama anterior al trabajo D6; no se utilizó como supuesto avance del baseline. |

**SOURCE FACT.** La revisión combinó source inmutable y autoridades D2/D4/D5/D6; se verificó la integridad Git blob de 190 archivos seleccionados de Echo y 38 de Agents-OS. Eso acredita los archivos adquiridos, no una auditoría de todo el repositorio ni una ejecución física. [A01] [A02] [A03] [A04]

Antes de publicar se refrescó Agents-OS a `ea7d048c260967881bab7f6c483bae1beb30820e`: tres commits posteriores sólo modifican documentación de Multimodal Knowledge Engine. No cambian las autoridades de Echo utilizadas aquí y se preservan íntegros. Echo activo seguía en d361008b.

En este documento, **OWNER / MANAGER FROZEN** identifica una restricción ya aceptada; **SOURCE FACT** identifica comportamiento o estructura comprobable en el baseline; **DESIGN DECISION** identifica la resolución técnica de BT-S01. Las secciones prescriptivas, schemas, fórmulas, secuencias y tests son DESIGN DECISION salvo indicación contraria. **OPEN OWNER DECISION: NONE.** Los parámetros exigidos a cada corrida son datos del experimento; su obligatoriedad no delega arquitectura al implementador.

## Contenido

Las secciones 1–8 fijan motor, inputs y causalidad; 9–15 fijan economía, lifecycle, ejecución y finalización; 16–20 fijan evidencia, persistencia, findings y pruebas. El último bloque es el contrato obligatorio de BT-S02.

## 1. Qué construye V1

**OWNER / MANAGER FROZEN.** Hay un solo Backtest Engine. El mismo engine ejecuta Generic100K y una cuenta con reglas Provider. Strategy, S1/S2, GerardMM, Operation, Provider, admission, capacity, reservations y revalidation siguen siendo autoridades reales. Una regla económica que pueda cambiar una decisión participa durante la corrida. [A01]

**DESIGN DECISION.** Una corrida contiene una cuenta de ejecución, una o varias configuraciones de Strategy sobre un único contrato físico, sus owners de Operation, un Provider y un ledger de cuenta. El motor vive en `v3/backtester`; sólo importa SDK para el dominio. `Run` es una composición histórica, no otro conjunto de estrategias o reglas monetarias.

~~~mermaid
flowchart TD
    I["Dataset y controles fijados"] --> D["Driver histórico"]
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
| Un contrato real con ticks y contexto S1/S2 | Cambio de expiry/rollover se rechaza con `ROLLOVER_UNSUPPORTED_V1`. |
| Cuenta USD; contabilidad exacta y economía durante el run | Sin FX, portfolio multicurrency ni consolidación multiactivo. |
| MARKET, STOP_MARKET, CANCEL, DAY/GTC | LIMIT y native MODIFY no son capacidades del modelo histórico V1. |
| Reglas tipadas de cuenta, resultado de evaluación y cierre | Sin DSL de props, funded automático ni payout inferido. |
| `AdvanceUntil` sobre el mismo motor | Sin checkpoints durables ni resume distribuido. |
| Evidencia reproducible y primer punto de divergencia | Sin afirmar reproducción de infraestructura LIVE ausente del corpus. |
| Múltiples runs independientes | Paralelismo inicial entre procesos; cada run permanece secuencial. |

Rechazar rollover evita mezclar H4/BB de expiries diferentes: el source actual puede cambiar StreamID preservando ModuleState. No se presentará una concatenación de corridas independientes como una cuenta continua. El contrato exacto y los controles temporales dejan un punto de extensión normal para resolverlo después. [S08]

## 2. API y entrada de una corrida

La API pública del package `backtest` expone tres operaciones: `NewRun(spec, sources, recorder)`, `AdvanceUntil(T)` y `Finish()`. `Run(...)` es la conveniencia que avanza al horizonte y finaliza usando ese mismo loop.

`AdvanceUntil(T)` procesa sólo causas con tiempo lógico <= T y termina la transacción causal completa del último instante procesado. No devuelve en medio de un lote de fills ni de una secuencia de efectos. Es monótono, mantiene el estado en memoria y entrega únicamente observaciones conocidas hasta T. Una pausa no es un resultado COMPLETE. `Finish` exige horizonte alcanzado o terminación de negocio declarada y asentada, más las condiciones de §15.

### 2.1 RunSpec V1

`RunSpec` es configuración de la ejecución histórica y composición de structs existentes. No introduce un `BacktestProfile` ni una jerarquía por prop.

| Campo | Contrato |
| --- | --- |
| `schema_version` | `echo.backtest.run.v1`. |
| `build` | Commit/tree, estado limpio o patch digest, binary SHA-256, Go version, GOOS/GOARCH, dependencias y build flags relevantes. Una publicación canónica exige identidad reconstruible. |
| `dataset` | Manifest inmutable con versión, SHA-256, partes, formato, orden, cobertura y referencias durables. |
| `warmup_start / trade_start / end_exclusive` | Instantes UTC; warmup_start <= trade_start < end_exclusive. El período operable es [trade_start,end_exclusive). |
| `config` | `config.ConfigSnapshot` extraído del source, con exactamente una cuenta, un contrato, calendario, ventanas, Strategy/S1/S2, MM, Provider y targets explícitos. |
| `initial_state` | Capital y estado económico explícitos; V1 exige inventario, órdenes, reservas y ciclos vacíos. Los estados técnicos nacen del warm-up. Un capsule de laboratorio no se convierte en un resume general. |
| `controls` | Secuencia finita de controles tipados, effective_at, control_id, ordinal y payload completo. Sin referencias `latest` ni closures opacos. |
| `account_context` | Binding/RuleSet exactos, selector y rows económicos, account-day, estado ACTIVE/CLOSE_ONLY/etc., términos de programa opcionales y cobertura de policy. |
| `execution_model` | Versión, fidelidad, slippage ticks, fees, edad máxima por lado y TIF vacío resuelto explícitamente. |
| `valuation_model` | `NET_FIFO_LIQUIDATION_V1`; exactitud monetaria, fuentes de bid/ask y freshness; USD. |
| `end_policy` | `REPORT_RESIDUALS` o `REQUIRE_FLAT`; esta última incluye un control de cierre anterior al horizonte. |
| `lab_fixture` | Opcional, lista finita de perturbaciones tipadas de observaciones, con coordenadas y payloads. Su digest entra en identidad. |
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
| `v3/backtester/{run,spec,driver,controls,economics_views,result,evidence,reproduce}.go` | Package público `backtest`: composición, loop, entrada, proyecciones, schema y comparación. Archivos pueden dividirse por responsabilidad sin cambiar los boundaries. |
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
| `v3/sdk/futures/provider` | ClockFired/NextBoundary, proyección económica tipada, consistencia reutilizable, lifecycle y safety de términos suplementarios. F01–F03 según su protocolo. |
| `v3/sdk/futures/operation` | ExecutionUpdate/QuoteUpdate, expiry compartido y error propagation. F04/F05 según su protocolo. |
| `v3/sdk/futures/strategy`, `strategies/s1`, `strategies/s2` | Inicialización Warmup explícita del mismo pipeline, sin fórmulas o módulos duplicados. |
| `v3/core/internal/functions`, `futuresruntime` | Shells/aliases que invocan las transiciones extraídas, config y adapters compartidos; wiring de provenance e IDs cuando se corrijan. |
| `go.work` | Incorporar sólo el nuevo módulo; no actualizar toolchain o dependencias por comodidad. |

Las transiciones Market/Analytics exponen la forma `Apply(state, typed_input, logical_now, run) -> next_state, ordered_effects, error`. Los efectos conservan los payloads reales: CanonicalMarketEvent, EpochBarrier, StreamStateSnapshot, BarsSnapshot, BarClosedDelivery, SessionTransitionDelivery, ReadinessChangedDelivery, QuoteNotification y pedidos de timer. No se introducen callbacks que escondan I/O.

Las shells Core retienen decode, ValueSpecs/load/store, enrutamiento StateFun, egress y telemetría. Preservar nombres de ValueSpecs, formas serializadas y contratos actuales; aliases/wrappers pequeños son aceptables. Las dos rutas deben llamar a una sola implementación de la transición extraída.

Dependencias permitidas: `market -> bars/domain`; `analytics -> market/bars/calendar` y los tipos actuales de Strategy/Operation; `marketctx -> market/bars/calendar`; `strategy -> marketctx`; `config -> SDK domains/engines/adapters`. `marketctx` no importa Operation ni Analytics; Market no importa Strategy. El nuevo módulo no importa `core/internal`, otro módulo hermano ni el harness. Esto respeta la independencia de módulos del repo. [S22]

### 4.2 Adapter de mercado de Operation

El adapter compartido debe resolver el `contract_id` solicitado al stream exacto configurado; un ID ajeno produce miss. El source actual ignora ese argumento y usa un único stream. La extracción incorpora la validación exacta y su regresión en el paquete compartido. [S03]

Para el baseline seleccionado, conservar la capacidad real del contexto: Mark usa el trade actual y Ready usa readiness analítica/feed. No agregar `ExecutableQuoteSource` al adapter sólo para mejorar el backtest. El wrapper `quoteScopedMarket` actual presenta el midpoint de la quote y no expone esa interfaz opcional. SimExecution y la valuación pueden utilizar BBO sin alterar esa capacidad del MM. Cualquier mejora futura del wrapper debe ser un cambio compartido con evidencia propia. [S10]

## 5. Contrato de datos históricos y fidelidad

### 5.1 Corpus mínimo

V1 consume NDJSON, opcionalmente gzip, normalizado a `market.MarketCandidateEnvelope` más referencia de registro y evidencia de los lados de quote cuando existe. El manifest enumera partes inmutables, SHA-256, conteos, período, stream/contrato, capacidad de identidad del source, cobertura TRADE/BBO, calendario y gaps conocidos. No se construye un ingest universal de vendors.

Los candidatos llegan ordenados por `event_ts`, stream y orden estable de observaciones del dataset. El shared StreamSequencer asigna `stream_seq`; no se inventa esa identidad antes de canonicalizar. En un stream, el orden de registros a igual timestamp fija ese orden canónico. La secuencia aceptada respeta la precedencia de §6; cambiar chunks o buffers de lectura no la cambia.

Un dato con tiempo retrocedente no se reordena oportunistamente mientras corre el dominio. El corpus histórico debe venir normalizado con orden definido o falla preflight/lectura; un caso de late delivery pertenece al fixture explícito de laboratorio o a exact replay de admisión real. Correcciones de barras siguen la autoridad compartida: actualizan proyección y no reevaluan retrospectivamente el cierre original.

**SOURCE FACT.** Identidad canónica, `stream_seq` y `content_digest` tienen funciones diferentes. EVENT/POSITIONAL preservan identidad nativa; NONE no puede ascender a identidad nativa por hash del contenido. [S04] [A05]

Para NONE, usar `IngressRecordRef{log_identity=dataset-part-digest, partition=part_ordinal, offset=record_ordinal}` y expansion_index. Eso identifica una observación importada, no prueba un evento físico único. Dos trades iguales en registros distintos se conservan. El digest detecta conflictos; nunca deduplica trades por igualdad de precio/tiempo.

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
2. **Fijar ejecución física.** SimExecution toma las órdenes aceptadas antes de C, calcula y sella sus matches usando C y quotes ya observadas. Ordena por acceptance_ordinal y order_id. Una orden creada por C no participa.
3. **Actualizar economía y aplicar fills.** Para todo C, incluso sin matches, recalcular la valuación/freshness desde la observación actual y preparar ledger/risk/Provider AccountSnapshot de la misma revisión. Comprometer esa observación antes de liberar safety o decisiones ordinarias; una nueva quote no puede dejar a Provider con el riesgo de la anterior. Retener sus efectos safety mientras se asienta el lote. Para cada fill, agregar fees/inventario y su nueva revisión; aplicar `ExecutionUpdate` con una sola invocación FILL y comprometer los candidatos al éxito. Entregar su CapacityUpdate antes de pedidos de Reservation/Revalidate; esos nuevos pedidos esperan al cierre del lote.
4. **Reconciliar y liberar protección.** Terminar todos los fills/costes/CapacityUpdate sellados; entonces entregar una PositionObservation del net físico final de ese mismo prefijo. No comparar la posición de todos los matches contra un estado lógico que sólo aplicó el primero. Actualizar trust antes de nuevos pedidos. Entregar safety comprometido antes de trabajo ordinario todavía no comprometido. Cancels emitidos por el primer fill no eliminan un segundo fill ya sellado.
5. **Entregar decisiones de mercado.** Deliveries ordinarios conservan el orden de efectos producido por Analytics, con fanout estable por owner. QUOTE observado entra como `QuoteUpdate` correlacionado. En TRADE_MODEL, la valuación modelada puede causar un EconomicsUpdate ordinario con snapshot actual; no se llama directamente a GerardMM.
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

Warm-up comienza vacío, procesa sólo el prefijo anterior a trade_start y exige cero Signals y cero ciclo abierto. Una salida inesperada es error, no descarte silencioso. En trade_start se activa el mismo estado preparado; no se reescribe ModuleState JSON. La fase de activación no cierra artificialmente una barra que cruza ese instante.

La cobertura se calcula con barras realmente cerradas y demandas reales. S2 exige sus parámetros vigentes: trendPeriod+1 H4 y BollPeriod 5m; se conserva el predicado real `H4.CloseBoundary <= entryBar.BucketOpen`. Un comentario contradictorio no cambia ese predicado. S1 puede comenzar antes de completar OR y permanecer NOT_READY legítimamente. Un inicio que solicita contexto precalentado sin prehistoria suficiente falla `WARMUP_INCOMPLETE`. [S08]

El estado operacional/económico de la cuenta no registra compras, fills o fees durante warm-up. Los controles preparan la autoridad necesaria; el trading se habilita en trade_start. El calendario y los boundaries de prehistoria siguen siendo reales.

## 8. Operation, GerardMM y Provider

### 8.1 Camino autorizado

Se conserva SignalDelivery → admission/pending admission → materialización de Operation → GerardMM real → claims locales → reservas/revalidación Provider cuando aplican → M1 OrderCommand → SimExecution. Provider no redimensiona silenciosamente la cantidad elegida por MM. Fills y finality regresan por los inputs compartidos y producen CapacityUpdate/release reales. [S09] [S11] [S14] [A07] [A08]

**SOURCE FACT.** El source permite M1 directo cuando sólo hay familias PER_ORDER o no hay caps compartidos; no corresponde inventar reservas obligatorias para ese caso. Si existe un grant compartido, su revalidación exacta antes de M1 sigue siendo obligatoria. [S09] (líneas 974–1191)

GerardMM recibe contrato pinneado, MMState, fills/claims, RuleSet completo y economía autoritativa. El ledger no llama a MM ni decide sizing. Las rows/config MM se pinnean al abrir la Operation; un nuevo account-day afecta el selector de futuras Operations y el snapshot económico de las existentes, sin reescribir su plan. [A09] [S10]

### 8.2 Economía correlacionada con Fill y Quote

**SOURCE FACT.** `buildMMInput` prefiere `DeliveredEconomics` sobre Views. El handler de fill actualiza exposición e invoca MM dentro del mismo Apply. Actualizar Views y enviar Fill puede dejar economía vieja; enviar EconomicsUpdate primero invoca MM con la exposición anterior. [S09] (líneas 797–871) [S11] (líneas 291–392)

Añadir dos variantes al union `operation.Input`, preservando la firma Apply y exactamente un input:

- `ExecutionUpdate{Fill, Economics, EconomicsUpdateID}`.
- `QuoteUpdate{Quote, Economics, EconomicsUpdateID}`.

Primero validar shape, account/strategy/operation/order, identidad nativa, dedup y staleness. Para un fill nuevo de la Operation actual, instalar el snapshot correlacionado sin un trigger adicional y usar el handler real de fill: una sola invocación `MMTriggerFill` con exposición y economía actualizadas. Quote hace lo mismo con `MMTriggerQuote`. Un duplicado jamás reinstala una revisión económica anterior.

Los inputs raw Fill/Quote y el EconomicsUpdate independiente siguen disponibles. Dos causas reales QUOTE y ACCOUNT_ECONOMICS se procesan por separado aunque compartan timestamp; el sidecar no borra un evento económico independiente. El input correlacionado sólo representa el contexto observado de su propio hecho.

Un fill genuino antiguo de A no modifica B mediante ese sidecar. Puede cambiar la economía física de la cuenta; B podrá recibir después un AccountEconomicsUpdate explícito como consecuencia account-wide, conservando la separación de ownership de F04. Otras Operations vivas reciben el cambio account-wide en orden estable. Sólo un fill físico válido de la misma cuenta/contrato puede cambiar su ledger. Un payload de otra cuenta o una correlación imposible queda como anomalía explícita, sin crédito/débito en esta cuenta; las pruebas F04 lo entregan además al handler compartido para comprobar su guard, sin ocultarlo en el ingress.

### 8.3 Entry expiry y terminación

Pinnear `OperationRuntime.EntryExpiresAt = openingDelivery.ValidUntil` al materializar y emitir efectos tipados de schedule/cancel. La autoridad D2-04 define ENTRY_EXPIRED como TTL de entry/signal sin fill. El primer fill o la terminalidad desarma el timer; un firing viejo valida identidad/generación. Un fill exactamente al deadline gana por fase 4 antes de fase 5. [A10]

Completar el handler compartido: si la entry aún no cruzó M1, revocar su continuación local, liberar reserva por el path real y bloquear una respuesta tardía que intente publicar. Si `CommandPublished=true`, emitir CANCEL y mantener q_exec_max/claims hasta fill/finality. No fabricar finality para una orden nunca enviada. Reutilizar ese helper de revoke/cancel donde terminación y safety lo necesiten. [S11]

Propagar los errores de `replanSafetyClose` actualmente descartados en llamadas a `admitOrderRequest`. Un error al construir el cierre no puede aparecer como transición exitosa. Esta corrección y el timer guard son requisitos concretos de las transiciones tocadas, no nuevas políticas D6. [S11] (líneas 808–932)

## 9. Economía de cuenta

### 9.1 Ledger físico y exactitud

El nuevo package `accounting` sólo depende de domain/units. Mantiene inventario FIFO por account+contract, realized gross, costes cobrados, balance, marks/unrealized/equity, baselines diarios, contador de revisión y dedup nativo. No importa Strategy, MM, Provider engine ni storage.

**SOURCE FACT.** PositionObservation expresa posición física neta; Operation conserva exposición lógica derivada de sus fills. Una compra de una Operation y una venta de otra pueden netear físicamente a cero aunque ambas sigan vivas. [S12] [S13]

No sumar unrealized de cada Operation usando bid/ask como si fueran cuentas físicas independientes: cargaría spread adicional. El ledger netea fills reales, preservando la atribución lógica de cada fact por separado.

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

Una revisión económica contiene `account_id, revision, observed_at, cause_ref, account_day_id, initial_balance, balance, equity, realized_gross, charged_costs, realized_net, unrealized, day_start_balance, day_realized_net, account_day_pnl, stage_net_pnl, best_day_net, marks, freshness` y risk state. Proyectar desde esa misma revisión:

| Consumidor | Proyección |
| --- | --- |
| Operation/GerardMM | `AccountEconomics`: PnL account-day, currency, AccountDayID, PnLSnapshotVersion, PnLFresh, headroom monetario y selector aplicable. |
| Provider | `AccountSnapshot`: Known, AccountState, breaches, PhysicalTrust, AccountDayID, consistencia y cap-breach evidence. La revisión se registra junto a la entrega aunque el struct actual no tenga ese campo. |
| Result/lifecycle | Balance/equity, floors, límites/cobertura, causa, marks y resultado económico. |

**SOURCE FACT.** Provider consume AccountSnapshot; el ingester es responsable del reset diario y de los flags autoritativos. El view adapter actual sirve economía, no la calcula. [S03] [S15]

Añadir funciones puras compartidas `provider.EvaluateEconomicRisk` y un evaluador de lifecycle con structs tipados; reciben observación, risk state anterior y RuleSet/términos completos. Su resultado no es sizing: produce floors, headroom, flags y outcome. Provider Apply sigue resolviendo admission/safety.

La observación económica se actualiza ante cada cambio material de mark, fill, coste, account-day, control o freshness. Antes de una decisión que pueda abrir riesgo, las proyecciones validan la edad contra el reloj lógico actual; si la evidencia venció desde la última entrega, el driver compromete primero la nueva revisión de freshness/Provider y sus efectos, como consecuencia de ese avance lógico. No mantener Known/PnLFresh verdaderos sólo porque no llegó otro tick.

Un mark requerido ausente/vencido produce PnLFresh=false y estado de riesgo no resuelto, bloqueando nuevo riesgo. `nil headroom` significa que no aplica una familia monetaria; no significa error de cálculo. Inventario neto cero puede valuarse con balance sin quote. La confianza física se obtiene reconciliando PositionObservation con los hechos, jamás forzando la exposición lógica al valor observado.

## 10. Contextos Generic100K y prop

### 10.1 Generic100K sin defaults secretos

**OWNER / MANAGER FROZEN.** Generic100K fija sólo `initial_balance=USD 100000`. [A01]

El caller debe proporcionar MM selector/rows soportados, scaling explícito, account-day, binding/RuleSet de simulación sin restricciones opcionales, fees, ejecución y horizonte. La ausencia de política restrictiva se representa con un RuleSet ACTIVE válido y explícito; no con saltarse Provider o fingir un entitlement LIVE.

El ejemplo entregable se llama `generic100k-evaluation-d1-d2`: elige de forma visible EVALUATION día 1/día 2, SL USD 2000 y TP USD 1500, dos account-days con boundary UTC 00:00, adds deshabilitados explícitamente, fees/slippage y TIF especificados. Esas rows vienen de la autoridad Owner; EVALUATION, los dos días y el boundary son elecciones del ejemplo, no consecuencias de tener 100K. [A09] [S16]

Un horizonte mayor requiere un calendario explícito de selectores/rows que cubra cada día aplicable. No repetir día 2, prolongar día 1 ni inventar FUNDED. Un valor que falta produce error de preflight o bloqueo explícito de nueva operación, según fuera verificable al comienzo; jamás fallback dentro de GerardMM.

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

## 11. Lifecycle y seam hacia campaña/bankroll

### 11.1 Una cuenta

El evaluador compartido produce observaciones `AccountLifecycle` con account_id, stage/context digest, observed_at/effective_at, cause_ref, resultado y razones. V1 distingue ACTIVE, MODELED_EVALUATION_FAIL, MODELED_EVALUATION_PASS, MODEL_OPERATIONAL_FAILURE y AWAITING_NEXT_CONTEXT; son resultados del modelo, no una taxonomía universal de empresas.

Pass exige target alcanzado, consistencia cumplida, `minimum_traded_days` explícito y satisfecho, cobertura modelada suficiente y exposición física/lógica cero, sin órdenes ejecutables, reservas/pendings/outbound action ni finality pendiente. El contador de días operados suma account_day_ids distintos con al menos un ExecutionFill válido, único y de cantidad positiva, atribuible a esa cuenta durante la etapa; duplicates no suman y el modelo no exige resultado positivo por día. El ejemplo fija mínimo 0; nil impide PASS por término no resuelto. Un target visto en unrealized no produce un pass retroactivo. Consistency temporalmente excedida puede resolverse con días posteriores y no quema por sí sola la cuenta.

V1 termina la evaluación o el horizonte. No instala automáticamente FUNDED. El seam de transición recibe un siguiente contexto completo: binding/RuleSet, MM selector/rows, límites, account state, política de balance/baselines y effective_at. En el futuro se aplicará en un boundary quiescente y como un control causal único. Sin esos datos, AWAITING_NEXT_CONTEXT.

Si continúa la misma cuenta física, puede conservar account_id con cambios explícitos. Si la prop entrega otra cuenta, crear otro run/account relacionado. S02 no implementa transferencia de cuenta, fees comerciales, payout ni workflow de varias etapas.

### 11.2 Campaña futura

El futuro controlador de campaña vive fuera del engine. Posee bankroll, compras, fees, cuentas activas, créditos de payout, calendario y política de reinversión. Usa `AdvanceUntil` de los mismos engines, sin inspeccionar el futuro.

~~~text
bankroll(t) =
    bankroll_initial
  − settled_purchase_reset_subscription_costs(<=t)
  + settled_payout_credits(<=t)
~~~

La compra requiere caja disponible en ese instante; descuenta el fee antes de activar la cuenta. El nominal 50K/100K nunca se suma al bankroll. Un payout conocido el día 5 no compra una cuenta el día 2. A igual settlement time, ordenar por account_id/event_id, asentar créditos/débitos definidos antes de la siguiente decisión de compra.

Los términos de fees, split, eligibility y settlement delay deberán ser datos as-of explícitos. Si un retiro cambia balance, headroom o continuidad de la cuenta, entra como control causal en su engine; no se resta después de todas las operaciones.

El seam actual conserva parent IDs, instantes y observaciones prefijo <= T. No expone summaries futuros ni permite elegir retrospectivamente corridas favorables. Ejecutar cuentas completas en paralelo será correcto sólo si ninguna decisión de campaña puede cambiar sus trayectorias y sus resultados futuros no se hacen visibles antes de tiempo.

Métricas futuras —compradas, fallidas, pasadas, funded, payouts, fees, bankroll final, tiempo a primer payout y duraciones— se derivan de esa caja y esos facts. S02 entrega el seam y su prueba de prefijo; no construye el simulador masivo.

## 12. SimExecution V1

### 12.1 Estado y autorización

SimExecution mantiene comando/correlación inmutables por orden, estado físico, remaining qty, acceptance_ordinal/cursor, stop_triggered, fills, terminal finality, dedup de comandos y sesiones/binding. No vuelve a consultar una RuleSet mutable para autorizar un comando que ya cruzó M1.

**SOURCE FACT.** GerardMM seleccionado emite MARKET, STOP_MARKET y CANCEL; el bridge sim existente está orientado a scripts. El dominio ya distingue OrderObservation, ActionObservation, ExecutionFill, PositionObservation y SessionObservation. [S26] [S12] [S19]

### 12.2 Matching

| Tipo | Regla exacta |
| --- | --- |
| MARKET BUY | Primer cursor posterior a aceptación, sesión negociable y quote válido: ask + slip_ticks×tick_size. Full remaining qty. |
| MARKET SELL | Mismas condiciones: bid − slip_ticks×tick_size. |
| STOP_MARKET BUY | Sólo trade aceptado posterior a aceptación con last >= stop. Pasa a triggered MARKET y usa ask válido; espera si falta quote. |
| STOP_MARKET SELL | Sólo trade posterior con last <= stop. Usa bid válido o espera. Un gap no llena al stop solicitado. |
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

### 13.1 RunID y build

`input_sha256 = SHA256(canonical_v1(ImmutableInputs))`; `run_id = bt-<digest completo>`. ImmutableInputs incluye build/code, dataset/range, config resuelta, initial state, calendarios/tzdata, controles y modelos. Excluye el propio run_id, paths locales, credenciales, host, duración, intentos y destino de publicación. `ConfigSnapshot.Run` se representa sin el ID derivado al hashear y se liga después al resultado, evitando recursión.

Todo owner y fact recibe `RunProvenance{BACKTEST,run_id}`. El mismo conjunto inmutable produce los mismos IDs y comportamiento. Una nueva versión de código cambia el run_id normal. Una comparación diagnóstica contra otro build puede conservar el namespace del baseline, identificando ambos builds y publicando sólo bajo attempts, nunca sobre su resultado canónico.

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

`REQUIRE_FLAT` necesita un cierre causal previo y datos ejecutables posteriores dentro del horizonte. Si faltan, INCOMPLETE; nunca venta al último precio. Business FAIL/PASS terminal detiene trading y completa sólo después de asentar la ejecución requerida; si no converge antes del horizonte, INCOMPLETE preservando ese outcome parcial.

Condiciones conjuntas para COMPLETE:

- Inputs previstos consumidos y validados hasta el stop contractual.
- Cola inmediata drenada, sin error ni hecho físico sellado sin aplicar.
- Valuación final válida para toda posición neta y cobertura declarada.
- Residuales compatibles con end_policy y listados íntegramente.
- Lifecycle y execution_state separados; counts/digests/schema completos.
- Gzip local cerrado y verificable.

Una caída del publisher no invalida estas condiciones locales; tampoco convierte un fallo del engine en COMPLETE.

## 16. Contrato de resultado y evidencia

### 16.1 Un artifact autocontenido salvo corpus durable

`runs/<run-id>/result.json.gz` contiene un documento `echo.backtest.result.v1`. No requiere MongoDB, event sourcing, base analítica o guardar todos los ticks duplicados.

| Campo top-level | Contenido |
| --- | --- |
| `schema_version` | `echo.backtest.result.v1`. |
| `run` | RunProvenance existente. |
| `inputs` | ImmutableInputs completo; config/initial state inline y refs durables verificables de corpus/build/calendario. |
| `input_sha256` | Identidad de inputs. |
| `records` | Array ordenado escrito por streaming. |
| `summary` | Execution state, terminal_reason, último tiempo/cursor, counts, lifecycle, economía/días, residuales, state digests y fidelidad/cobertura. |
| `first_error` | Null para COMPLETE; primer capsule de fallo cuando corresponda. |
| `integrity` | Canonicalization/version, hash_algorithm, record_count, records_sha256, input_sequence_sha256 y logical_sha256. |

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
| ACCOUNT_LIFECYCLE | Outcome/transición con causa, contexto y cobertura. |

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

1. Crear spool local exclusivo por intento. Escribir header/records, luego summary/integrity.
2. Cerrar gzip con compresión fijada, mtime cero, nombre/comment vacíos y representación estable; cerrar/sync archivo.
3. Reabrir, decodificar y verificar schema/counts/digests. Finalizar localmente por rename atómico bajo exclusión del run-id; si ya existe, comparar contenido y no reemplazar un resultado diferente.
4. El publisher externo sube bytes cerrados directamente a `runs/<run-id>/result.json.gz` con create-if-absent `If-None-Match: *` y checksum. No HEAD seguido de PUT incondicional.
5. Timeout ambiguo/precondition: GET del objeto existente y comparación SHA-256 verificada. Igual es éxito idempotente; distinto es `RUN_ID_CONFLICT` y queda intacto; estado no verificable sigue pendiente/fallido.
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

Semántica: conservar account/strategy/operation/order/provider-execution originales. A no revive; B mantiene íntegros Operation, Runtime, MMState, fills, órdenes, exposición y claims. Puede avanzar una secuencia audit del owner sin fingir mutación de B. Run provenance sale de correlación original retenida; si no se resuelve, UNKNOWN explícito, nunca el run de B por conveniencia.

Regresiones `operation/bt_f04_test.go`: owner vacío; A terminal/B actual y fill nuevo de A; duplicado de A ya cobrado; orden inexistente/foreign account/strategy; fill corriente válido. Fixture integrada modifica net físico por fill nuevo de A y muestra mismatch/safety sin transferencia falsa a B. Dedup económico por cuenta+execution ID durante todo el run. No filtrar IDs antiguos antes de Apply.

### BT-F05 — IDs consumidos fuera del clone

**SOURCE FACT.** NewOperationID ocurre antes de validación/MM; NewOrderID puede consumirse antes de un error posterior. El allocator determinista actual mantiene cursores fuera de OwnerState. [S09] (líneas 661–743 y 935–956) [S23]

Semántica/fix target: §13.2. Estado, efectos y cursores se comprometen juntos. LIVE UUIDv7 mantiene su naturaleza; la repetición determinista corresponde al allocator BACKTEST.

Regresión `operation/bt_f05_test.go`: MM error después de materializar; segunda request inválida después de asignar la primera orden; fallos repetidos; serialize/restore; owners/runs independientes; retry vs baseline fresco sin fallo. Assert estado/counters intactos, cero effects y mismos IDs del éxito. Dos runs limpios o abortar antes de retry no cierran este finding.

### 19.1 Evidencia mínima de disposición

Cada finding tiene source/semántica, comando/caso baseline, resultado observado, shared diff si aplica, regresión nombrada, build y evidencia local. Si S02 lo corrige, S03 verifica independently su repro/fix; no desaparecerá de la matriz. Si queda pendiente en S02, se declara `PENDING_S03_REPRODUCTION` y nunca aprobado por omisión. Sólo evidencia que descarte la hipótesis bajo sus precondiciones permite DISPROVED_WITH_EVIDENCE.

## 20. Matriz de aceptación local

Esta matriz es obligatoria para S02 salvo las expansiones adversariales/closures expresamente asignadas a S03/S04. Los nombres son IDs estables de evidencia; los nombres Go pueden seguir la convención del repo. No se ejecutó ninguno en S01.

| ID | Caso | Aserción material |
| --- | --- | --- |
| BT-A01 | Extracted Market/Analytics vs shells con mismo input/state | Mismos next-state y ordered effects; shells sólo adaptan I/O y preservan wire/state. |
| BT-A02 | Warm-up S1/S2 con señales atractivas en prehistoria | Cero Signal/ciclo abierto; mismos OR/H4/BB del pipeline; primera decisión normal correcta. |
| BT-A03 | Primer trade de boundary + segundo al mismo T | Barra anterior excluye primero; orden no llena en causa, sí puede en segundo. |
| BT-A04 | Boundary sin tick; sesión/break/early close en T | Timers y precedencia correctos; cero barras fuera del grid. |
| BT-A05 | Timer viejo después de nueva barra y cambio de calendario | No cierre nuevo por generación reutilizada; boundary/id válidos. |
| BT-A06 | Epoch/recovery, duplicate/conflict y repeated equal-price ticks | Guards reales, identidad distinta cuando corresponde, cero reeval retrospectivo. |
| BT-A07 | Contrato ajeno/rollover/multicurrency | Miss exacto o error preflight nombrado; no uso de contrato corriente. |
| BT-A08 | Inputs/config faltantes, day3 sin row, Warmup incompleto | Fallo explícito, cero fallback/plan heredado. |
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
| BT-A26 | Generic y GAU50 con mismo motor/corpus | Restricción puede cambiar secuencia/sizing/admission/continuidad; cero post-hoc sustituto. |
| BT-A27 | Horizon dentro de barra/último tick crea orden/residuales | No fill futuro ni close parcial inventado; COMPLETE/INCOMPLETE según policy. |
| BT-A28 | Run dos veces, chunk size distinto, A/B/A y procesos nuevos | Igualdad exacta de records, IDs, economics, final state y gzip. |
| BT-A29 | Apply error/panic/recorder error | Primer error/capsule, ningún commit fallido ni COMPLETE falso. |
| BT-A30 | Mutar una observación/context read/orden de effects | Reproducer detiene primera divergencia y materializa contexto suficiente. |
| BT-A31 | Result parse, refs/digests y output truncado | Artifact válido completo o diagnóstico; no publicación parcial canónica. |
| BT-A32 | Publisher idéntico/conflicto/timeout/partial connection/size | Create-if-absent real; exact retry; conflicto intacto; local conservado. |
| BT-A33 | AdvanceUntil(T) vs Run completo y dos cuentas con payout futuro ficticio | Prefijo idéntico; ninguna observación >T ni caja futura visible. |
| BT-A34 | F01–F05 | Casos directos de §19; matriz de disposición y evidencia, sin workaround del driver. |
| BT-A35 | Legacy SDK/Core/futuresvertical regression | Shared extraction/adiciones no rompen consumers; no claim físico D6 por estos tests. |
| BT-A36 | Dataset representativo de ticks + evidencia streaming | Reportar counts, memoria y tamaño; sin retener corpus/records completos en RAM. Sin SLA inventado. |

Fixtures de modelo pueden usar precios artificiales mínimos, con contratos y unidades válidos. Diferenciar esas pruebas de una corrida sobre histórico externo real. Conformance MinIO usa backend/prefijo aislado autorizado; si el entorno no está disponible, conservar la prueba local y declarar esa parte NO_VERIFICADA, sin afirmar el gate de publicación completo.

## 21. Fuentes, alcance de evidencia y cobertura del mandato

Las fuentes de código están fijadas a Echo d361008b; las autoridades a Agents-OS b999eb3e. Las decisiones nuevas de este diseño no se presentan como funcionalidades ya implementadas.

| Ref | Fuente principal |
| --- | --- |
| A01 | BT-S00 aceptado y mandato BT-S01 de esta sesión. |
| A02–A04 | Proyecto/Technical SPEC y freeze D6. |
| A05–A06 | Identidad/exact replay D4-A1 y orden BACKTEST D2-06C. |
| A07–A10 | Claims/capacity, Provider authority, GerardMM y lifecycle Operation. |
| A11–A12 | Remediación D6 vigente y evidencia externa E2T congelada. |
| S01–S08 | Market/Analytics/views, identidad, Bars, clock, Strategy y S2. |
| S09–S16 | Operation/MM/ejecución/Provider y planes económicos. |
| S17–S24 | GAU50, consistencia, sim, warmup, unidades, módulos, IDs y observabilidad. |
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

Revisión de diseño GOD/CLOUD ONE-SHOT consolidada; cuatro especialistas cubrieron causalidad, economía, ejecución y determinismo/evidencia. Una revisión independiente de coherencia corrigió actualización de marks sin fills, dependencias NEW→CANCEL, reconciliación por prefijo, reapertura y mínimo de días. No son un gate adversarial LOCAL ni pruebas físicas. Artifact candidato listo para Manager; aceptación/freeze corresponde a Manager/Owner según el programa. La continuidad y el registro de sesión quedan en Agents-OS por delta.

`PRO_CHAT_POOL_DELTA: 0` significa cero consumo confirmado atribuible por evidencia del host; aplicabilidad Chat/Work y consumo real no expuestos permanecen UNKNOWN. No se multiplica gasto por número de subagentes ni se inventa remaining/reset.

## BT-S02 IMPLEMENTATION CONTRACT

### Rol, entrada y objetivo cerrado

**NORMAL LOCAL, ONE-SHOT de implementación.** Entrar con BT-S01 aceptado por Primary Technical Manager y baseline/branch confirmados en su mandato. Entregar un Backtester V1 funcional conforme a este documento; no rediseñar la arquitectura. Trabajar en branch/worktree aislado desde el baseline que indique Manager, respetando deltas compartidos posteriores; no editar el worktree, despliegue, bundle, config canónica ni gates de D6.

Si el baseline cambió, comparar sólo el delta material con este contrato y conservar las autoridades actuales. Una incompatibilidad real se reporta con evidencia concreta; no sustituir source activo por master antiguo ni abrir preguntas ya resueltas aquí.

### Implementar y extraer

1. Crear `v3/backtester`, API NewRun/AdvanceUntil/Finish/Run y CLI run/reproduce/publish; añadir módulo al workspace.
2. Extraer Market/Analytics y feed/config exactamente según §4. LIVE/Core y BACKTEST deben invocar la misma transición. Mantener wire/ValueSpecs/JSON.
3. Componer los engines reales Strategy/S1/S2/GerardMM/Operation/Provider, los demands/calendarios y vistas exactas. Implementar Warmup compartido de §7.
4. Implementar reader normalizado/manifest y driver secuencial de §5–6, con controles, fases, timers, lote de fills y quiescencia definidos.
5. Implementar accounting FIFO exacto, snapshots/revisión, day boundaries, risk projection y modelo de cuenta §9–10. Generic100K sólo aporta saldo.
6. Añadir ExecutionUpdate/QuoteUpdate, entry-expiry schedule/revoke/cancel y error propagation compartidos. No escribir directamente MMState/DeliveredEconomics desde el runner.
7. Implementar SimExecution §12 con tipos nativos, elegibilidad posterior, stop/gaps, ACK/finality, TIF, dedup y fixture lab acotada.
8. Implementar términos Provider tipados y lifecycle de evaluación; proveer los dos ejemplos explicitados. Mantener GAU50 source íntegro, suplemento separado y calificación modelada.
9. Implementar IDs deterministas y aislamiento §13, con el protocolo F05; si una corrección F01–F05 es físicamente necesaria, hacerla en shared domain y preservar baseline/regresión. No declarar cerrado el programa.
10. Implementar records/digests, replay/primera divergencia, EOF, finalización local y publisher condicional §14–18.

### Reutilizar y packages autorizados

Reutilizar los tipos/engines/domain policies existentes; no copiar fórmulas de S1/S2/GerardMM/claims/reservas/consistency. Tocar únicamente los targets y shells enumerados en §4, los tests consumidores necesarios y manifests/go.work/go.mod requeridos. No importar Core internals desde backtester, no reutilizar el harness como producto ni incluir transports en el loop.

### Tests que escribir y ejecutar localmente

Implementar BT-A01…BT-A36 con los casos indicados y evidencia por ID. Organizar tests junto a shared packages para correcciones de dominio y junto al runner/sim/store para composición. Escribir F01…F05 directos según §19; si S02 no los corrige, conservar repro y estado pendiente para S03, sin marcar suites rojas como verdes.

Ejecutar desde los módulos correspondientes, con el workspace y toolchain del repo:

- SDK: `go test ./futures/...`.
- Backtester: `go test ./...` y build de `./cmd/echo-backtest`.
- Core: tests de `./internal/futuresruntime`, `./internal/futuresvertical` y `./internal/functions`, incluyendo los consumers de la extracción.
- Consumers adicionales de SDK IDs/Provider identificados por búsqueda de call sites: compilar/testear su superficie afectada; no omitir futures-bridge si su compilación cambia.
- Conformance de publisher en MinIO/S3 configurado, prefijo aislado: creación, igualdad, conflicto, timeout ambiguo y no-publicación de spool abierto.
- Dos corridas idénticas + A/B/A + proceso fresco; comparar records/IDs/estado/economía y bytes gzip. Medir un corpus de ticks representativo sin prometer un SLA no medido.

No ejecutar órdenes contra brokers, egress LIVE, pruebas D6 pendientes o cambios de infraestructura como parte de este shot. Los tests compartidos de código no acreditan esos gates.

### Artifacts obligatorios

Entregar commit/branch limpio y diff revisable; README de ejecución y limitaciones; RunSpec/manifest/fixtures completos; schema V1 documentado; dos resultados Generic/GAU50 reproducibles con digests; un primer-divergence capsule demostrado; logs/comandos/build/counts de tests; reporte de conformance MinIO y estado de publicación; tabla BT-F01…F05 con evidencia y próximo responsable; mapping BT-A01…BT-A36 a tests/resultados.

Los results grandes/corpus quedan en storage durable con digest; el repositorio guarda fixtures pequeñas, manifests y reportes. No subir credenciales ni copiar el histórico completo a documentación.

### Decisiones que NORMAL no puede reabrir

Un engine y una cuenta/contrato por run; secuencial/in-process; SDK compartido real; fases y micro-order §6; economía causal con sidecars compartidos; FIFO net por cuenta; Generic sin stage/plan implícitos; GAU50 modelado con cobertura honesta; Sim sólo después de M1; ACK distinto de finality; órdenes nuevas no llenan en su causa; IDs dentro del clone; resultado exacto por streaming; create-if-absent; first divergence completa; ningún workaround exclusivo para F01…F05; ningún cambio/gate D6.

Las decisiones de nombres locales, helpers y organización menor de tests pueden seguir el estilo del repo si no cambian ese contrato. Un parámetro obligatorio no se transforma en un default oculto.

### Diferido

Rollover/múltiples contratos, multicurrency, native LIMIT/MODIFY, profundidad/queue/latencia aleatoria/Monte Carlo, optimización masiva, distribución intra-run, shared market bus, UI, Mongo/event sourcing, DSL de props/workflows, lifecycle funded/payout completo, campaign simulator masivo, multipart no certificado, resume/checkpoints durables y certificación física LIVE.

### Gate de salida

BT-S02 sale **listo para revisión de Manager y BT-S03 LOCAL adversarial** sólo si la implementación corresponde a este contrato, los casos funcionales/de extracción/determinismo/resultados requeridos tienen evidencia verde, los ejemplos producen resultados íntegros, el publisher tiene conformance acreditada cuando se declara operativo y ninguna excepción está escondida. La matriz F01…F05 puede mantener pendientes explícitos de reproducción/cierre asignados a S03/S04; ningún finding bloqueante puede quedar parcheado en el runner ni impedir el camino funcional que se afirma completo.

Si falta un requisito del gate, entregar estado exacto, repro y trabajo pendiente; no emitir PASS global. BT-S03 deberá verificar adversarialmente los cinco findings incluso si S02 ya corrigió algunos. BT-S04 deberá cerrar todo confirmado. El programa sólo termina cuando cada uno esté en **CONFIRMED_FIXED_WITH_REGRESSION** o **DISPROVED_WITH_EVIDENCE**, con fix compartido y evidencia local cuando corresponda.
