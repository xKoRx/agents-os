---
type: doc
schema_version: 1
status: active
area: '[[Echo]]'
related:
- '[[10-projects/Echo Forge — Operación Real V2/Echo Forge — Operación Real V2|Echo Forge — Operación Real V2]]'
- '[[Echo — Producto Integrado]]'
aliases: []
tags:
- kind/doc
created: '2026-10-27'
updated: '2026-10-27'
---

# A — Source Authority Report

## Propósito

Resolver Retester versus CustomAnalysis/Exporter y fijar las autoridades de identidad, versión, metadata, métricas, operaciones y provenance que usará la task declarativa Forge → Echo.

## Contenido

**Adjudicación del manager:** investigación de fuente completada y aceptada como baseline CURRENT de diseño. La matriz de procedencia conserva su autoridad; las decisiones TARGET están en [[B — Frozen Design]]. No acredita ejecución física.

**Estado de la investigación:** READ_ONLY_FORENSICS_COMPLETE, con gaps materiales identificados para diseño e implementación.  
**Alcance:** reconstrucción de autoridad en código, sin ejecución física, suites, acceso a stores productivos ni mutaciones remotas.  
**Fecha:** 2026-10-27.  
**Autoridad del encargo:** documento adjunto “ECHO FORGE → ECHO INGESTION V2”, especialmente §§5–8; políticas Symphony CONSTITUTION y reglas 00, 02, 03, 13. Investigación recibida y revisada por el Primary Manager como autoridad CURRENT; las decisiones TARGET están en B.

## 1. Conclusión adjudicable

Los datos no pertenecen todos al Retester, al Exporter ni a PostgreSQL. La autoridad vigente se distribuye de forma concreta:

- **SQX Retester** realiza la evaluación física y deja el ResultsGroup dentro de su artefacto .sqx. La task durable sella la identidad del stage, su output exacto y, si se observaron, las métricas extraídas.
- **EchoForgeOverviewExporter**, plugin Java CustomAnalysis, lee ese ResultsGroup y su XML, produce metadata enriquecida y métricas nativas. El **worker Go** importa y persiste; Java no escribe Mongo en la ruta inspeccionada.
- **EchoForgeTradeListExporter** extrae y normaliza operaciones cerradas ya existentes en ResultsGroup. No ejecuta un nuevo backtest ni deduce operaciones desde agregados. La activity Go vincula el TradeSet a una Evaluation previa y persiste metadata en Mongo + payload en MinIO.
- **PostgreSQL** conserva identidad, invocaciones, StageExecutions y sus enlaces exactos a Evaluations, ownership del namespace, versiones selladas y entregas. **Mongo durable** conserva Evaluations, MetricSets y TradeSets; **MinIO** conserva los bytes exactos.
- **databank_metadata y export_runs son proyecciones brownfield mutables**, no autoridades suficientes para reconstruir la Evaluation final. Tener todos los campos de StrategyMetadata no acredita a qué evaluación, versión ni periodo pertenecen.

El caso “tomar una carpeta de Full Precision Tick Retester e importar todo” todavía tiene tres huecos de contrato: resolver y acreditar el cohort exacto; disponer de una StrategyVersion/definición adecuada para SQX sin exigir artefactos MT5 inexistentes; y acreditar las dimensiones económicas que el TradeList v1 no conserva, especialmente moneda. Estos huecos son locales y delimitables: no requieren una nueva base de datos ni un framework ETL.

## 2. Baseline y comparación real

Lecturas GitHub GET confirmadas:

| Repositorio/ref | Commit HEAD verificado | Tree de commit |
|---|---|---|
| xKoRx/symphony, lab-v4/shot4-symphony | 22f337ca434549c492b2d402fd158e23ac4758a8 | 5d769ba454f9d87dc12700b4bfa9744e69d252f3 |
| xKoRx/symphony, master | dd4af7d05c03db9b39b5467b46e2c2c7d0c1fa19 | 380b595e7329a6da31070e4266d90a7d95d12757 |
| xKoRx/sdk, commit declarado por require | c7f11496b6f681687c9e1e41a773a13295640351 | lectura del tree por commit |

La comparación de trees completos, no truncados, confirma que **los productores, modelos y stores de fuente examinados tienen los mismos blobs en los dos HEADs Symphony**. En el área sqx/core, adapters, activities y workflows, las diferencias observadas son http_ingress_v2.go y su test; también cambian sqx/go.mod y go.sum. Master carece de ingestion_v2_persistence.go, migración 017_ingestion_v2_persistence.up.sql y sqx/cmd/echo-ingest-v2/main.go presentes en el candidato consolidado. Por tanto master contiene parte de V2, pero no equivale al baseline consolidado.

Todo el reporte usa el SHA Symphony **22f337ca434549c492b2d402fd158e23ac4758a8**, salvo indicación expresa. Las referencias [S01]–[S50] apuntan a ese commit; el apéndice incluye blob SHA individual.

El require de SDK es reproducible nominalmente, pero sqx/go.mod contiene replace github.com/xKoRx/sdk => ../../sdk y replace github.com/xKoRx/symphony => ../. El SDK local que hubiera usado una máquina física puede diferir del commit declarado. No se inspeccionó ese checkout local ni se probó build frío. Las estructuras Trade/TradeListManifest se contrastaron con el commit declarado, no se afirma que pruebe el binario instalado. [S48]

## 3. Superficies que no deben confundirse

| Superficie | Papel real | Ejemplo verificable |
|---|---|---|
| Task del workflow | Intención declarativa, routing y selección de actividad | TaskSpec.Type=project, Stage=retester/final_reretester; type=trade_list_exporter. [S04] |
| Task interna de SQX | Etapa dentro de project.cfx/config.xml | La construcción de CFX agrega una Task type=CustomAnalysis, apuntando a CustomAnalysis-Task1.xml. [S07], postProcessCFX/ensureProjectOverviewProducer/overviewCustomAnalysisTaskXML |
| Plugin Java | Lee ResultsGroup, XML y órdenes de SQX; emite archivos | EchoForgeOverviewExporter.processDatabank/buildStrategyRow; EchoForgeTradeListExporter.processDatabank/processStrategy. [S14], [S25] |
| Activity Temporal | Coordina I/O físico y persistencia | ProjectActivity ejecuta pipeline; ImportMetadataActivity descarga/importa metadata; ExportTradeListActivity exporta y persiste TradeSet. [S05], [S15], [S20] |
| Binding producer | Construye evidencia y refs deterministas | retester/binding, final-reretester/binding, trade-list/binding. [S08]–[S13], [S22]–[S24] |
| Store | Aplica persistencia e índices; no calcula semántica del stage | ControlPlane PG, EvidenceStore Mongo y almacenamiento MinIO. [S03], [S17], [S34], [S37] |

custom_analysis_plugin selecciona el plugin que debe correr dentro de SQX. metadata_export activa el paso de importación/exportación de metadata en el pipeline según tipo de task. overview_exporter es otra task del workflow que puede ejecutar el proyecto fijo EchoForgeOverviewExporter. metadata_import/extractor llama la activity que descarga archivos de MinIO y ejecuta ImportMetadataStep; no equivale a “hacer un retest”.

ProjectActivity.enableMetadata fuerza metadata para Builder durable y Retester durable. FinalReretester requiere el flag/configuración aplicable para generar observaciones; no puede suponerse que siempre tenga MetricSet. effectiveProjectTask inyecta el Overview de Builder/import; para Retester devuelve la TaskSpec solicitada porque la llamada pasa durableBuilder como segundo argumento. Su CFX/plugin debe aportar el Overview que el import obligatorio consumirá. La task legacy overview_exporter se omite cuando el mismo spec demuestra un Builder durable equivalente, para no duplicar productor. [S05] líneas 210, 280–288, 410–442; [S47] shouldSkipLegacyOverviewExporter.

## 4. Retester, FinalReretester y “Full Precision Tick”

### 4.1 Activación e identidad

La activación durable es explícita:

- IsDurableRetesterTask = type project + stage retester.
- IsDurableFinalReretesterTask = type project + stage final_reretester.
- Ambos excluyen folder/source_folder/name como fuente de semántica. [S04] líneas 396–412.

El Retester inicial usa productor **sqx-retester.v1**. Su contrato documenta un input StrategyRef/EvaluationRef por ejecución física y cero o un output .sqx; el código también contempla lotes y valida correspondencia de outputs. FinalReretester usa **sqx-final-reretester.v1** después de Apply. El workflow hace fan-out por carrier y conserva identidad del StrategyRef. Cero output sella StageExecution con conjunto exacto vacío; no se debe inventar Evaluation ni pasar estrategias descartadas. [S08], [S10], [S11], [S13], [S47] runFinalReretesterFanout/validateFinalReretesterFanoutOutput.

### 4.2 Qué existe al terminar

Para cada output durable:

1. StrategyRef y CanonicalStrategyID provienen de identidad PG/adopción y del carrier.
2. StageExecutionRef identifica la ejecución lógica; PG sella stage_execution_results con EvaluationRefs exactas.
3. EvaluationEvidence en Mongo incluye FlowRunRef, StrategyRef, StageExecutionRef, productor, Scope, ConfigurationSnapshot, InputEvaluationRefs y el OUTPUT/STRATEGY_SQX con bucket/object_key/size/SHA256.
4. MetricSetEvidence opcional contiene valores observados y estados, referencia a su Evaluation y versiones de cálculo/catálogo.
5. .sqx exacto existe como artefacto MinIO de la Evaluation; un objeto MinIO sólo listado por nombre no adquiere esta autoridad.
6. El carrier corriente contiene el EvaluationRef nuevo. Retester también actualiza BuilderMetricSetRef, cuyo nombre histórico no significa que siga apuntando al Builder. FinalReretester sólo actualiza EvaluationRef: su PersistOutcome incluye MetricSetRefs, pero ProducedBinding/carrier no expone ese hijo. [S07] persistRetesterEvidence, persistFinalReretesterEvidence; [S09]–[S13].

No aparece automáticamente un TradeSet al terminar Retester. La historia completa necesita extracción TradeList o un productor equivalente acreditado. La existencia de NumTrades, MonthlyResults o NetProfit no permite reconstruir operaciones individuales.

### 4.3 Precision y periodos

No hay un tipo de task “Full Precision Tick” ni un campo de precision en los scopes Retester/FinalReretester inspeccionados. El nombre de la carpeta no lo acredita. El stage y productor acreditan qué proceso lógico produjo el output; para certificar la precisión física hay que conservar/verificar la configuración SQX efectiva y su build. Los scopes actuales incluyen instrumento, dirección, timeframe y, cuando es determinista, el periodo configurado extraído del CFX.

ParseCFXConfiguredPeriod sólo toma Data/Setups/Setup de la configuración principal, excluye OOS/crosschecks/additional markets y devuelve missing si hay más de una ventana distinta. Su provenance es sqx_cfx_setup.v1. No conserva en este value object modo de precisión/tick, datos utilizados, zona de mercado o moneda. [S44]

El trade scope tick_retest es semántica explícita que se entrega al exporter; **no demuestra por sí solo** que el resultado fue realmente Full Precision Tick. Eso debe ser evidencia del productor/configuración, no alias de stage ni nombre de folder.

## 5. Overview enriquecido: qué se conserva y dónde

EchoForgeOverviewExporter.buildStrategyRow consulta mainResult.stats para Full, IS y OOS. En el JSON raíz, metrics es full_sample; overview retiene los tres bloques. Extrae indicadores, bloques, parámetros detectados y diagnósticos leyendo XML de estrategia. Genera monthly_results por agregación de órdenes y puede emitir trades_debug, que es diagnóstico opcional, no el contrato normalizado de historia. Produce overview.ndjson, monthly.ndjson y export_run.json. [S14] líneas 505–550, 679–733, 738–800, parseIndicators.

StrategyMetadata contiene efectivamente identidad física, wave/run, instrumento/timeframe/dirección, stage/variant, indicadores/bloques/parámetros, métricas, SPP y monthly results. Esto es capacidad del modelo; no demuestra que un exporter concreto llene todos los campos ni que sobrevivan en evidencia durable. [S01]

La proyección brownfield:

- SaveStrategyMetadataBatch hace ReplaceOne/upsert por **(wave_key, strategy_id)**, índice único igual. No incluye EvaluationRef, StageExecutionRef, versión ni run_id en la clave.
- LoadStrategyMetrics/LoadAllStrategyMetrics filtran por wave y run_id obtenido del contexto; no seleccionan por EvaluationRef.
- SaveExportRun/GetExportRun usan **(wave_key, stage, exporter)** y ReplaceOne. ExportRun guarda conteos/estado/finished_at, no una lista exacta de StrategyRefs/EvaluationRefs. [S16] líneas 133–166, 517–600, 734–747.

En durable V1 el Builder conserva databank_metadata como side-effect brownfield, pero omite export_runs. Los demás stages durables con StageExecutionRef y EvidenceStore omiten esas dos escrituras. Sus observaciones se consumen para crear evidencia inmutable. **Consultar databank_metadata después de FinalReretester puede devolver metadata de Builder, no del resultado final.** [S07] líneas 3708–3746.

La evidencia durable preserva un subconjunto: Retester sella classification_input (arrays de indicadores) y MetricSet con metrics raíz. FinalReretester no sella parámetros/bloques/diagnósticos completos ni classification_input; ConfigurationSnapshot incluye configuración descriptiva de workflow, no un definition manifest integral. Los bloques overview IS/OOS, monthly results y detalles ricos no se convierten automáticamente en MetricSets separados en estas funciones. Se pueden recuperar sólo si existe su artefacto fuente exacto o realizar una extracción versionada desde el .sqx exacto. No son hechos que deba completar una consulta por nombre al Mongo legacy. [S07], [S09], [S12]

### Hallazgo de routing ya existente

El código brownfield aún contradice regla 13:

- writeExporterProperties: si stage vacío, usa Task.Folder.
- ImportMetadataStep cuando corre exporter separado escribe stage=Task.Folder.
- Luego valida runJSON.Stage contra Task.Folder o literal builder. [S07] líneas 2992–2995, 3297, 3332–3334.

Es un defecto preexistente comprobado, no una recomendación de ampliar scope. La nueva ingesta debe consumir autoridad durable y evitar esas inferencias. Si requiere esa ruta para producir evidencia ausente, la corrección mínima es pasar/validar la semántica explícita del productor, con prueba de rename. No copiar el comportamiento defectuoso.

## 6. TradeList: productor, conservación, límites económicos

### 6.1 Flujo actual comprobado

ExportTradeListActivity recibe un StrategyArtifact. Carga exactamente carrier.EvaluationRef y ResolveSourceSQX exige:

- productor sqx-final-reretester.v1;
- mismo StrategyRef;
- exactamente un artifact OUTPUT/STRATEGY_SQX;
- ObjectKey idéntico a carrier.Key.

Descarga bytes por DurableArtifactRef, escribe la estrategia verificada en el proyecto EchoForgeTradeListExporter, configura wave_key=Evaluation.FlowRunRef y run_id=Evaluation.Ref, ejecuta SQX CustomAnalysis y procesa los manifests. El worker limpia input/output/overview/tradelist antes del trabajo; no se observó el riesgo de contaminación residual que existía en versiones anteriores. [S20], [S22], [S23], [S04] CleanProjectDatabanks.

El Java usa ResultsGroup.orders() y normaliza órdenes existentes. Sin WFM emite FULL; con WFM puede emitir FULL/IS/OOS y cell_key. No se mezclan mediante sumas. FUTURE se rechaza como audit-only. [S25], [S26], [S29]

La activity requiere exactamente un baseline **tick_retest/optimized/FULL sin cell_key**, y al menos un trade agregado. PersistTradeSet guarda payload gzip en MinIO y TradeSetEvidence en Mongo. **No crea una nueva Evaluation ni StageExecution del exporter**: el TradeSet es hijo de la Evaluation exacta final-reretester. El workflow añade únicamente BaselineTradeSetRef al carrier.TradeSetRef; los demás refs se retornan en el resultado de activity, pero no se propagan en el carrier de una sola referencia. [S20] líneas 225–299; [S21]; [S24]

Esto resuelve bien el caso especializado final-reretester con baseline. **No implementa todavía un exportador durable genérico para cualquier Retester/CustomAnalysis.** Añadir otros productores necesita una ampliación acotada del binding o un productor previamente acreditado; no se puede declarar que ya lo soporta porque el Java acepte stage configurable.

### 6.2 Los dos stores de trades

| Store | Identidad y comportamiento | Lectura |
|---|---|---|
| Mongo trade_lists brownfield | Upsert mutable por wave_key, request_id, run_id, strategy_id, stage, variant, result_key, cell_key, sample_type. Metadata de manifest y artifact, no array de trades. | TradeListRepository.LoadManifest(scope) exacto; ListByWave no es selector de evaluación. [S32] |
| Mongo trade_sets durable | _id=TradeSetRef derivado de EvaluationRef + ScopeDigest + parser version + normalized schema. Insert-only, same digest converge; distinto digest conflicto. Lleva FlowRunRef/StrategyRef/StageExecutionRef, Counts y ArtifactRefs. | ImmutableEvidenceStore.LoadTradeSet(ref); no existe listado público genérico de hijos por EvaluationRef en el port inspeccionado. [S02], [S17], [S19], [S46] |
| MinIO durable payload | durable/trade-list/v1/flow/strategy/evaluation/scopeDigest/trades.ndjson.gz; la autoridad de lectura es el ArtifactRef guardado, no reconstruir esa receta desde nombres. | FetchDurable/VerifyDurableArtifact y decoder existente. [S22], [S24], [S34], [S35] |

No se debe resucitar trade_lists como fallback automático cuando falta evidencia durable. Un documento histórico puede ser útil para auditoría/migración explícitamente diseñada, pero sus nueve dimensiones todavía necesitan un vínculo acreditado con StrategyRef/EvaluationRef/StrategyVersion. “Misma wave y mismo nombre” no basta.

### 6.3 Contenido económico disponible

El wire trade.v1.0.0 y TradesJson tienen: trade_key/index; identidad de scope; apertura/cierre UTC; precios; LONG/SHORT; gross/net; commission/swap; pnl_basis; instrumento/timeframe; source_timezone; duración; MAE/MFE; labels. No tienen moneda/FX, Q_i, cantidad normalizada, ciclo, fills/leg/partial-close, ni construction_at. OrderAdapter lee Size/MagicNumber/OrderId pero Size y MagicNumber no se serializan en el trade normalizado. TradeIdentity usa scope completo + OrderId, con fallback físico OrderId→Ticket→Order en el adaptador. [S26]–[S30]; SDK trade.go [SDK01].

**Costes:** la implementación no descompone comisión y swap nativos. ClosedTradeNormalizer hace net=Order.PL, commission=Order.CommSwap, swap=0.0 y gross=net−commission−swap. El cero de swap es una convención de normalización del combinado, no un hecho observado de coste swap cero. Capabilities.defaultObservedInG0 pone booleanos true fijos para comisión/swap/gross/MAE/MFE; no es un certificado por run ni la separación económica que exige Echo. [S27], [S31]

Según el contraste recibido del especialista Echo, MoneyV2 exige currency de tres letras y su status/evidence; Q_i es opcional pero no debe inventarse; commission/swap requieren disclosure honesto. Por tanto:

- Preservar net y su referencia, con moneda observada o declarada explícitamente y acreditada.
- No etiquetar la comisión combinada como comisión individual KNOWN_NONZERO ni swap como KNOWN_ZERO.
- No construir Q_i desde lotes, MAE, drawdown, net, SL nominal o una constante.
- No reconstruir ciclos/operaciones parciales desde resumen cerrado.
- Sin moneda acreditada/declarada, no existe un DTO económico honesto completo: bloquear ese perfil o registrar estrategia/evidencia según política de ausencia acordada. No inventar USD por símbolo, cuenta por defecto o nombre de carpeta.

### 6.4 Provenance y cobertura: debilidades reales

1. ProductionSQXTradeSource.getOrders intenta resultKey, luego strategyId, luego string vacío; sólo si no aplica filtro usa rawList. El manifest conserva el result_key pedido, no documenta cuál fallback efectivo resolvió órdenes. La cache usa sampleType, no resultKey. Es una limitación de provenance del parser, relevante al certificar una muestra exacta, no prueba de mezcla física en esta sesión. [S26] líneas 71–127.
2. BuildTradeSetScope conserva stage/variant/sample/cell y periodo configurado, pero no result_key, request_id ni run_id del manifest. La EvaluationRef cubre ejecución upstream; cualquier ampliación a múltiples resultados del mismo eval debe preservar result_key explícitamente para no colisionar scopes. [S23].
3. El binding durable guarda SourceArtifacts=[.sqx] y payload gzip; no guarda trades_manifest.json, export_run.json ni capabilities como artifacts. La activity valida manifest y stage/variant, pero en el camino leído no contrasta todos los campos wave/run/strategy/result ni el checksum del manifest con el payload antes de persistir. El hash durable calcula los bytes recibidos, lo cual acredita integridad posterior, no por sí solo correspondencia semántica con la Evaluation. [S20], [S23], [S24].
4. TradeExtractionService calcula period_start del primer trade en orden de cierre y period_end del último cierre. No equivale al mínimo de todas las aperturas si hay operaciones solapadas; tampoco acredita cobertura completa sin operaciones. El periodo CFX y el intervalo de actividad observada deben mantenerse distintos. [S29], [S44].
5. El normalizer escribe source_timezone="UTC"; el exporter recibe sourceTimezone del ETCD y ProductionSQXTradeSource conserva brokerTimezone, pero el servicio leído no lo usa para sobreescribir el DTO. Los timestamps se interpretan como epoch absoluto; esto no acredita la zona de origen del broker. [S20], [S26], [S27], [S29].
6. Algunos campos numéricos físicos usan fallback 0.0 al faltar lectura por reflexión. El consumidor nuevo debe distinguir valores observados de defaults de parser; el booleano general de capabilities no basta. [S26] adapt.
7. El decoder Go deserializa y llama OnTrade; no llama Trade.Validate por sí mismo. El lector para ingesta debe validar cada registro, unicidad de trade_key, conteos y coherencia del scope en ese callback o en un helper existente compatible. [S35]

Estas observaciones no autorizan un rediseño general. La extensión mínima es un read/binding validado de TradeSet y evidencia explícita de los campos indispensables, junto con una salida missing/blocking cuando el productor no puede acreditarlos.

## 7. Matriz de autoridad exigida

| Dato requerido por Echo | Productor real | Store / clave exacta | Evidencia / límite | Mecanismo de lectura reutilizable |
|---|---|---|---|---|
| Cohort exacto de salida | Task durable productora | PG stage_execution_results por StageExecutionRef + Mongo evaluations | Resultado sellado; vacío es válido; no listing por basename. [S03], [S37] | LoadStageExecutionIdentity/Results → LoadEvaluation |
| Origen histórico source_folder | Productor que reclamó namespace | PG output namespace owner bucket+namespace; Mongo evals por FlowRun+artifact prefix | Folder sólo routing; validar stage completado y pertenencia result set. [S17], [S36] | LoadOutputNamespaceOwner / FlowRunStatus + ListNamespaceOutputEvaluations |
| StrategyRef | Adopción de estrategia | PG sqx.strategies.id | AdoptStrategy llama upsertStrategyV2. [S38] | LoadStrategyIdentity(ref) |
| CanonicalStrategyID | Identidad persistida productora | PG strategies, unique canonical_strategy_id para identity_model_version=2 | No recalcular desde filename en ingesta. [S38], [S39], [S45] | LoadStrategyManifestIdentity(ref) |
| Instrumento/timeframe/dirección | Identidad PG y scope productor | PG strategy row + Mongo Evaluation.Scope | Contrastar ambos; config física no garantiza moneda. [S09], [S12], [S39] | LoadStrategyManifestIdentity + LoadEvaluation |
| StrategyVersion | Sellador F04 tras Apply+Compile verificados | PG sqx.strategy_versions.version_ref | Seis campos S0; no config.Version ni SHA del .sqx tomado como EX5. [S40], [S42], [S43] | LoadStrategyVersion(versionRef); ListStrategyVersions sólo auditoría/selección explícita |
| Definición ejecutable SQX | Resultado SQX / XML contenido | MinIO EvaluationArtifact OUTPUT/STRATEGY_SQX exacto | .sqx ≠ XML ≠ MQ5 ≠ EX5 ≠ definition manifest. [S02], [S07], [S14] | FetchDurable exacto + extracción/parser productor versionado cuando se necesite |
| Effective inputs/runtime/deps sellados | Forge seal desde Apply, compile y readback | effective-inputs artifact MinIO; versión PG contiene digests | Ruta MT5 existente, no automáticamente disponible tras Retester. [S42], [S43] | Exact Apply/Compile Evaluation + artifacts + LoadStrategyVersion |
| Parámetros/bloques/diagnósticos ricos | Overview Java leyendo XML | overview.ndjson; brownfield databank_metadata | No todos se sellan en Evaluation durable; exact binding faltante para metadata histórica. [S01], [S07], [S14], [S16] | Preferir artefacto exacto/versionado; no join wave+name sin prueba |
| Indicadores de clasificación | Overview del Builder/import/Retester | Mongo Evaluation.Payload.classification_input | Retester los sella; FinalReretester no copia el payload rico. [S07], [S09], [S12] | LoadEvaluation exacto; upstream sólo como provenance explícita |
| Métricas nativas Full | SQX stats → Overview → binding Go | Mongo metric_sets._id / evaluation_ref | SourceClass SQX_NATIVE, calculator/catalog/formula versions; no equivalencia Lab. [S09], [S12], [S17] | LoadMetricSet(ref); binding hijo exacto por eval si único |
| IS/OOS agregados, SPP, mensual | Overview / otros exporters | JSON fuente y proyección metadata | Modelo no demuestra productor ni persistencia durable completa. [S01], [S14] | Artefacto exacto o extensión producer específica; nunca crear trades desde aquí |
| Operaciones cerradas | ResultsGroup.orders → TradeList normalizer | Mongo trade_sets + MinIO PayloadArtifact | TradeSet hijo de Evaluation final exacta; parser contract version. [S20]–[S30] | LoadTradeSet(ref) + FetchDurable + Decode/Validate |
| Muestras/historias múltiples | Productor + manifest TradeList | TradeSetRef por scope; payload lleva result/sample/cell/run | Mantener Full/IS/OOS/MT5 separados; carrier actual sólo baseline. [S21], [S23], [S25] | Refs explícitas o read hijo exacto por eval+selector; gap actual de port |
| Trade key | TradeIdentity Java | NDJSON trade_key | Hash scope+orderId; no cross-run dedupe implícita. [S30] | Campo fuente validado; preservar mapping en provenance |
| Apertura/cierre/precios/dirección | Campos Order SQX | NDJSON | Epoch interpretado UTC; dirección/reflection requiere contrato producer acreditado. [S26]–[S29] | Decoder + Trade.Validate + validación scope |
| P&L net | Order.PL | NDJSON net_profit | net_after_commission_swap; moneda ausente. [S27], [S28] | Decimalización estable del valor fuente + currency evidence explícita |
| P&L gross / costes | Normalizer a partir de PL y CommSwap | NDJSON gross/commission/swap | Coste combinado; no desglose observado. [S27] | Mapear disclosure honesto; preservar raw evidence |
| Moneda y FX | No productor acreditado en scope/Trade v1 leído | Ausente | No inferir de símbolo/folder/default. [S23], [S28], [SDK01] | Extensión mínima producer o declaración explícita con evidence_ref; ausencia visible |
| Q_i / ciclos / parcialidad | No productor acreditado en wire actual | Ausente | No reconstruir desde agregado ni cantidad. [S28], [SDK01] | Ausente; sólo aceptar evidencia nueva tipada y acreditada |
| Cobertura y timezone | CFX period + normalizer | Scope configured_from/to; actividad en manifest/payload | Configured period ≠ intervalo de operaciones; timezone origen no acreditado sólo por literal UTC. [S23], [S27], [S29], [S44] | Leer ambas autoridades y declarar coverage/missing sin sobreprometer |
| construction_at / disponibilidad | No construction_at observado en modelos inspeccionados | created_at de evidencia; sealed_at de versión | Fechas de persistencia/sello no son construcción ni disponibilidad al mercado. [S01], [S02], [S40] | Campos separados; no sustituir timestamp ni inventar fecha |
| Artifact refs / hashes | Upload y productores durables | Mongo EvaluationArtifact + MinIO; PG producer-output recovery | Store+bucket+object_key+size+SHA256; ETag no identidad. [S02], [S03], [S34] | FetchDurable/VerifyDurableArtifact |
| Provenance ejecución | Foundation productores | Evaluation + StageExecution + refs upstream | FlowRunRef, stage, producer versions, exact evaluations. [S02], [S37], [S46] | Lecturas exactas, más spec/TaskPath del control plane según diseño de orquestación |

## 8. Identidad y versión: adjudicación necesaria

AdoptStrategy ejecuta upsertStrategyV2; la identidad persistida impide recrear StrategyRef desde el nombre. Las utilidades CanonicalStrategyID y matching por Strategy core todavía existen dentro de la producción para compatibilidad. En ingestión son **evidencia de cómo se produjo** un binding, no autorización para repetir la heurística. [S38], [S45]

En Retester hay normalización de espacios/guiones, comparación de stem y un fallback de substring con unicidad para correlacionar Overview con output físico. Retester fresco rechaza output sin observación; recovery puede sellar sin métricas porque usa autoridad producer-output previa. FinalReretester usa un mapa por nombre normalizado sin la misma comprobación explícita de duplicados y permite no observar métricas. Debe conservarse la diferencia entre “output durable existe” y “metadatos/métricas completos acreditados”. [S07] líneas 2504–2552, 2582–2645, 2694–2780.

StrategyVersionRecord es un contenido sellado, no la columna version del workflow. El sello actual se produce en forge_seal_handoff_v1 tras:

- exact ApplyEvaluationRef y CompileEvaluationRef;
- lectura de .sqx, .mq5, .ex5 y compile log por ArtifactRef;
- verificación de magic efectivo y éxito de compilación;
- digests canónicos effective_inputs/runtime/dependencies;
- receta contracts.StrategyVersionRef de seis campos;
- inserción write-once en sqx.strategy_versions. [S42], [S43]

LoadStrategyVersion(versionRef) y ListStrategyVersions(strategyRef) existen. La lista se ordena por sealed_at/version_ref, pero **no resuelve cuál corresponde a una Evaluation arbitraria**. El carrier no tiene VersionRef; la task genérica necesita binding exacto o una receta de versión de investigación acordada con la autoridad Echo. No usar “el último sello de la estrategia”, ni fabricar EX5 para permitir REGISTER_ONLY.

No se encontró un productor nativo genérico de StrategyDefinition/definition manifest para cualquier .sqx en las rutas inspeccionadas. Sí hay XML dentro de fuente SQX y extractor de parámetros/indicadores; eso permite una extensión mínima de definición, pero no autoriza declarar que ya está disponible como DTO canónico.

### 8.1 Reader existente para una definición de investigación

**Reutilizable:** sqx/adapters/magic-readback/readback.go, blob 3705d1c2c7afb671d25d85dc599ba72382851c68. FromSQX (línea 90) y magicFromSQXZip (101) abren el ZIP en memoria, buscan exactamente una entrada strategy_Portfolio.xml con ese nombre/case, rechazan ausencia o duplicado, limitan el contenido descomprimido a 16 MiB y verifican CRC al llegar a EOF. Un ZIP corrupto no cae a un XML alternativo. Hoy la API devuelve sólo MagicNumber y el extractor de bytes es privado. [S51]

La ampliación mínima defendible es factorizar esa lectura exacta de bytes y usar un adapter versionado de StrategyFile con parser estricto para construir **Definition ANALYTIC**. No llamar FromSQX como si devolviera definición: exige MagicNumber y el parser interno de magic usa XML Strict=false. No es necesario ejecutar SQCLI ni reconstruir un framework de parsers.

El arquitecto independiente confirmó mediante inspección read-only de dos fixtures ZIP versionadas que archivos .sqx de dos retests pueden diferir mientras strategy_Portfolio.xml permanece byte-idéntico. Reportó blobs b2bbd79442d354b367419929c5d22055affa1e70 y 21237d4669c8c9b9d335b79b68dd5755a6822a08 y hash XML 6a89cc10aef01118e216cc544679f51b4ee9335535a3a4e00e4517aad4797f41; su reporte conserva los paths exactos. Esta observación complementaria se atribuye al arquitecto, no a ejecución física propia ni a fuente auténtica del Owner.

Por ello **el hash del .sqx entero no es una definición estable**: contiene resultados/metadata de evaluación además de estrategia. El member XML puede proporcionar estrategia, reglas, variables, money management y otros nodos que realmente estén presentes. La conversión debe conservar su artifact/hash y declarar ausencias. Ese XML por sí solo no acredita settings/lastSettings de evaluación, runtime/datos/dependencias externas ni compilación/ejecutabilidad MT5. La receta de StrategyVersionV2 para una definición analítica se congela con la autoridad Echo, nunca sustituyendo los campos del sello ejecutable F04 por hashes parecidos. construction_at queda separado y no deriva de mtime ni sealed_at.

## 9. Reads reutilizables y ampliaciones mínimas

| Pieza disponible | Reutilización directa | Límite / ampliación mínima |
|---|---|---|
| StageExecutionReader | Cargar identidad/status y result refs exactas | Exigir COMPLETED y membership de cada Evaluation seleccionada; no latest |
| OutputNamespaceOwnershipReader + NamespaceOutputEvaluationReader | Resolver carpeta histórica opaca | Reusar helper puro del resolver; su Execute además registra memberships y no es sólo read |
| StrategyIdentityReader / StrategyManifestIdentityReader | Identidad estable e instrumento/timeframe/dirección | No lookup por nombre |
| ImmutableEvidenceStore | Reads de Evaluation/MetricSet/TradeSet por ref | Falta lectura de todos los TradeSets hijos con filtro tipado; añadir sólo si no se suministran refs |
| BuilderMetricSetBindingReader | En implementación consulta por evaluation_ref y rechaza múltiples | Nombre/comentario Builder; generalizar port/nombre o usar read específico, con filtro de scope/calculator si se admite más de uno |
| PayloadStore.FetchDurable / VerifyDurableArtifact | Bytes con size+SHA | No recodificar artefactos ni usar ETag como hash |
| core/trades.Reader | Streaming gzip/NDJSON | Caller valida esquema, datos, scope, conteos, unicidad; no tolerar líneas inválidas para historia acreditada |
| TradeManifestRepository.LoadManifest | Auditoría histórica exacta por natural scope | No fallback automático al faltar TradeSet durable |
| ControlPlane.LoadStrategyVersion | Versión exacta sellada existente | Vincular al source seleccionado; falta receta SQX research para versión aún no sellada |
| Existing HTTPIngressV2 + persistence 017 | Entrega V2 | Contrato/runtime del cliente lo cubre especialista Echo; no otro cliente HTTP |

Ninguna extensión propuesta necesita que Echo importe modelos internos Symphony. La dirección permitida sigue siendo Forge → Echo Contracts. Las métricas SQX conservadas son evidencia fuente; The Lab sigue calculando curvas, métricas y rankings derivados.

## 10. Gaps mínimos para el Shot 1/implementación

**G1 — Fuente/cohort exactos.** Completar reutilización del resolver histórico y carrier current, añadiendo validación StageExecutionResult cuando corresponda. Un solo selector de autoridad; rechazar mezcla ambigua de current carriers con otro owner namespace. Identificar por refs durables y no latest.

**G2 — Hijo MetricSet/TradeSet exacto.** FinalReretester pierde MetricSetRef en carrier y sólo baseline TradeSetRef viaja. Para selección múltiple, lista por EvaluationRef y selector tipado estable; cero→missing, múltiples→ambiguous salvo conjunto explícito. No buscar “último por fecha”.

**G3 — Versión/definición para fuente SQX no compilada.** Resolver con autoridad Echo una receta compatible para investigación o mantener requisito de versión exacta disponible; no confundir config.Version/SQX build/StrategyVersion. Es una decisión material del arquitecto y del contrato compartido.

**G4 — Moneda y economía fiel.** Requerir evidencia de moneda o declaración explícita trazable. Mantener disclosure de CommSwap combinado. Q_i, FX, partials/cycles permanecen ausentes si la fuente no los acredita.

**G5 — Metadata enriquecida de la evaluación elegida.** La proyección Mongo legacy no es exacta. Sellar el subconjunto indispensable desde .sqx/overview del productor correcto, conservando su artifact/hash; no importar todo Mongo ni promover campos agregados a historia.

**G6 — Otros productores y múltiples scopes.** El TradeList durable actual está cerrado a FinalReretester baseline. Extender sólo los productores realmente requeridos con contratos explícitos; conservar result_key/sample/cell/run. Un CFX configurable por sí solo no abre este binding.

**G7 — Routing rename.** Corregir localmente el stage=Folder existente si se usa la ruta Overview/import para producir la evidencia de ingesta. Los mismos refs de productor y evidencia deben dar el mismo significado con full_precision_tick o resultados_finales_2027.

**G8 — Acreditación física pendiente.** Código fuente y tests existentes no certifican que un run real tenga datos completos. Seleccionar una fixture autorizada y demostrar exact chain PG→Mongo→MinIO, hashes, trade count/economía, identidad y receipts en los shots de ejecución; no se hizo aquí.

Hallazgos secundarios concretos a tratar sólo si tocan el trayecto elegido: provenance del result_key fallback, materialización source_timezone, conservación de manifest/capabilities y lectura numérica sin coerción null→zero. numericMetricFields no hace comprobación explícita de null antes de deserializar a float64; es un riesgo estático de missing convertido a cero, no una falla física demostrada.

## 11. Qué queda no disponible y qué no se afirmó

- No se leyó PostgreSQL, MongoDB, MinIO, Temporal ni un host SQX de ambiente real.
- No se afirmó que un objeto de repositorio sea fuente física auténtica del Owner.
- No se ejecutó SQX, exportación, compilación, migración, suite, build frío ni llamada Echo.
- No se emitió PASS de E2E ni se probó disponibilidad o exactitud económica de un dataset real.
- No se cerró Agents-OS ni se escribió feedback.
- La lectura read-only sí quedó completa para las autoridades fuente pedidas. Los gaps tienen localización y camino aditivo; no se necesita más exploración general para que el arquitecto decida.

## 12. Improve candidates

1. **Generalizar nominalmente el reader de hijo MetricSet** hoy llamado BuilderMetricSetBindingReader, sin ampliar a búsquedas latest.
2. **Añadir lectura acotada de TradeSet por EvaluationRef+selector tipado**, sólo si la task no requiere refs explícitas.
3. **Corregir semántica stage/folder en el tramo Overview usado** y conservar metadata rica con binding de evaluación.
4. **Acreditar moneda, result_key efectivo y coste combinado en el productor** mediante campos mínimos y versionados; preservar ausencia donde no exista hecho.
5. **No cambios de skills.** No candidato de framework, replicación de Mongo o nuevo repositorio de contratos.

## 13. Índice de evidencia fuente

Todos los enlaces Symphony usan el commit 22f337ca434549c492b2d402fd158e23ac4758a8. La siguiente tabla permite auditoría por path y blob SHA. Referencias SDK son al commit c7f11496b6f681687c9e1e41a773a13295640351 declarado por require; no sustituyen certificación del replace local físico.

| Ref | Archivo | Blob SHA |
|---|---|---|
| [S01] | sqx/core/domain/metadata.go | 55f88bbb71e1d7f3d00bd56c6e9355624e796c33 |
| [S02] | sqx/core/domain/persistence_contracts.go | 818560ffe45f8ae768ee7f3b0852db4c565968ee |
| [S03] | sqx/core/capabilities/persistence.go | 1237fdacbf972bad2afdd9b2107252d23ae8183a |
| [S04] | sqx/core/runtime/config.go | c96812151cc4919657eb0099ee81f67e46ef8a1c |
| [S05] | sqx/activities/worker/project_activity.go | dc3c0928ba6a4b97de53aa5934597dd24bf9a23d |
| [S06] | sqx/activities/worker/pipeline/builder.go | 6e1d084f35f924a77845a2e7dd2f59a7cccc8cde |
| [S07] | sqx/activities/worker/steps/steps.go | ab6a9d0a4cdc66b715d115da7a2803fc9b528c85 |
| [S08] | sqx/adapters/retester/binding/contract.go | eb6f30e0e7589f07a6527fa0df1ed1abaa9cdc52 |
| [S09] | sqx/adapters/retester/binding/evidence.go | aaf00f2b512cd7c1e3afa19f5b867c9fd056e614 |
| [S10] | sqx/adapters/retester/binding/persist.go | de423b21fc7924e6cd7446168bc1dc11e6efb374 |
| [S11] | sqx/adapters/final-reretester/binding/contract.go | 28182549166cd9a6087da9317bfe89f2a6d600e2 |
| [S12] | sqx/adapters/final-reretester/binding/evidence.go | 0deb5283c9f26f193e1f7a036704c37d9e65b003 |
| [S13] | sqx/adapters/final-reretester/binding/persist.go | 4e476e5cdc79b7baf3fed8e278f8ac6c04b29d8e |
| [S14] | sqx/exporter-plugin/src/SQ/CustomAnalysis/EchoForgeOverviewExporter.java | 23dc044cbe48fa8c00621b834bd566698a8f0aab |
| [S15] | sqx/activities/worker/import_metadata.go | e628ab94bde12c236c1da9930e290c4afdf5fa84 |
| [S16] | sqx/adapters/metadata-mongo/adapter.go | ffaedd6417233939f2912ed04e1a9ff4d32fb752 |
| [S17] | sqx/adapters/metadata-mongo/evidence_store.go | e9fa00fa84c8b1211aca54bfa32db1ea26e595df |
| [S18] | sqx/adapters/metadata-mongo/evidence_documents.go | 6551bb06db54b920085d9d211399b4c4fae09f5a |
| [S19] | sqx/adapters/metadata-mongo/evidence_indexes.go | 66be04c71648f3c62a75d579842aa28a5cd54745 |
| [S20] | sqx/activities/worker/trade_list_exporter_activity.go | 9e3c84c9a156b94f3ed0552bef837d22b78a5728 |
| [S21] | sqx/workflows/durable_trade_list_workflow.go | a774a021ca0eea96c93d9d2041e13a9278c8b2c2 |
| [S22] | sqx/adapters/trade-list/binding/contract.go | a13ca70315e382777887ffdb39acb8fb021fb7b5 |
| [S23] | sqx/adapters/trade-list/binding/evidence.go | 984f32df374577f1325eac8edfe88087634232f8 |
| [S24] | sqx/adapters/trade-list/binding/persist.go | 18b49a233b68494c1674967917a2bf19503b4883 |
| [S25] | sqx/exporter-plugin/src/SQ/CustomAnalysis/EchoForgeTradeListExporter.java | 57f6cc4fa833476a5259181d8b7e0a61d142bb76 |
| [S26] | sqx/exporter-plugin/src/SQ/CustomAnalysis/trades/ProductionSQXTradeSource.java | a2c92648acb7924a29324328152466882415e5d0 |
| [S27] | sqx/exporter-plugin/src/SQ/CustomAnalysis/trades/ClosedTradeNormalizer.java | ba4251b4fe6370d29a8c7545e3bf4625f13a04d3 |
| [S28] | sqx/exporter-plugin/src/SQ/CustomAnalysis/trades/TradesJson.java | 50828c9fcf295db93319ce3373df2886ea609450 |
| [S29] | sqx/exporter-plugin/src/SQ/CustomAnalysis/trades/TradeExtractionService.java | be80bf048799dc52b1aca9e712c173bca7f63f98 |
| [S30] | sqx/exporter-plugin/src/SQ/CustomAnalysis/trades/TradeIdentity.java | 794b427353492fc1c34f05f1cf784c5182b2075d |
| [S31] | sqx/exporter-plugin/src/SQ/CustomAnalysis/trades/TradeCapabilities.java | 9ab74c672541419f5d212c2db74c7b9b0dc63c9a |
| [S32] | sqx/adapters/metadata-mongo/trade_lists.go | 15f17fe70c0548b6c739fa5d5e401586172b14b8 |
| [S33] | sqx/adapters/storage-minio/trade_lists.go | e9333dd661cc1c1301fe507bea1af37351ebe9ea |
| [S34] | sqx/adapters/storage-minio/durable_artifacts.go | a9bbf148aa85f98f7f07dfea1a8519e2d9a79426 |
| [S35] | sqx/core/trades/decoder.go | e42fb0a96ab504706806451efa925f7601d04026 |
| [S36] | sqx/activities/worker/historical_cohort_activity.go | 4ceb3673dffcfbf79c3e72704527b013f31b3130 |
| [S37] | sqx/adapters/registry-postgres/stage_execution.go | 6cbe1747de1fb6b41d971e653d474de1a9e4846e |
| [S38] | sqx/adapters/registry-postgres/adopt_strategy.go | 4500078482d66ee803df0d38cb1f641b74d55e09 |
| [S39] | sqx/adapters/registry-postgres/strategy_manifest_identity.go | cfe0ad70f033ace26e09dc8af4ab8f6a8aab4150 |
| [S40] | sqx/adapters/registry-postgres/strategy_version.go | 6614708b12fac558e367a4223f1d45728b03ad06 |
| [S41] | sqx/adapters/registry-postgres/strategy_handoff_reads.go | 2d9a73cea1b8a5d7f7c08848f33a0ef8c96789e7 |
| [S42] | sqx/core/domain/strategy_version.go | 36e3f28502867102680dc73c058acb47a5ecc5bd |
| [S43] | sqx/activities/worker/forge_seal_handoff.go | ec955592a56fa383299db74e581bc6b55ff1d36f |
| [S44] | sqx/core/runtime/cfx_configured_period.go | 314c9a3d8053dd27ea05c84892fcc98f3af060f6 |
| [S45] | sqx/core/domain/canonical_strategy_id.go | e6e97f35c739769978fb7a37f042799ec3680a9b |
| [S46] | sqx/core/domain/persistence_identity.go | 657c1b9d6f5233b5f36e76f6238fcecf03e15d53 |
| [S47] | sqx/workflows/generic_workflow.go | 9dbdb9808180c30649e088beff205b1e5fe7487d |
| [S48] | sqx/go.mod | 6f9fc4ef6545ba1ab65dad38578081d5f5cfc017 |
| [S49] | sqx/adapters/mt5/binding/reretester_baseline.go | 01126afc68694c67a5483b625355abc02b65239f |
| [S50] | sqx/exporter-plugin/src/SQ/CustomAnalysis/trades/ManifestJson.java | cd035ae683cd460142299a9f78dbc9b718657c71 |
| [S51] | sqx/adapters/magic-readback/readback.go | 3705d1c2c7afb671d25d85dc599ba72382851c68 |
| [SDK01] | xKoRx/sdk: pkg/sqx/trade.go | 36be2efe804136bd7a8c933971beb97eb1db8416 |
| [SDK02] | xKoRx/sdk: pkg/sqx/trade_manifest.go | 3692e22e5f02c0dc99739fe7f6107dd9504e8d65 |

[S01]: https://github.com/xKoRx/symphony/blob/22f337ca434549c492b2d402fd158e23ac4758a8/sqx/core/domain/metadata.go
[S02]: https://github.com/xKoRx/symphony/blob/22f337ca434549c492b2d402fd158e23ac4758a8/sqx/core/domain/persistence_contracts.go
[S03]: https://github.com/xKoRx/symphony/blob/22f337ca434549c492b2d402fd158e23ac4758a8/sqx/core/capabilities/persistence.go
[S04]: https://github.com/xKoRx/symphony/blob/22f337ca434549c492b2d402fd158e23ac4758a8/sqx/core/runtime/config.go
[S05]: https://github.com/xKoRx/symphony/blob/22f337ca434549c492b2d402fd158e23ac4758a8/sqx/activities/worker/project_activity.go
[S06]: https://github.com/xKoRx/symphony/blob/22f337ca434549c492b2d402fd158e23ac4758a8/sqx/activities/worker/pipeline/builder.go
[S07]: https://github.com/xKoRx/symphony/blob/22f337ca434549c492b2d402fd158e23ac4758a8/sqx/activities/worker/steps/steps.go
[S08]: https://github.com/xKoRx/symphony/blob/22f337ca434549c492b2d402fd158e23ac4758a8/sqx/adapters/retester/binding/contract.go
[S09]: https://github.com/xKoRx/symphony/blob/22f337ca434549c492b2d402fd158e23ac4758a8/sqx/adapters/retester/binding/evidence.go
[S10]: https://github.com/xKoRx/symphony/blob/22f337ca434549c492b2d402fd158e23ac4758a8/sqx/adapters/retester/binding/persist.go
[S11]: https://github.com/xKoRx/symphony/blob/22f337ca434549c492b2d402fd158e23ac4758a8/sqx/adapters/final-reretester/binding/contract.go
[S12]: https://github.com/xKoRx/symphony/blob/22f337ca434549c492b2d402fd158e23ac4758a8/sqx/adapters/final-reretester/binding/evidence.go
[S13]: https://github.com/xKoRx/symphony/blob/22f337ca434549c492b2d402fd158e23ac4758a8/sqx/adapters/final-reretester/binding/persist.go
[S14]: https://github.com/xKoRx/symphony/blob/22f337ca434549c492b2d402fd158e23ac4758a8/sqx/exporter-plugin/src/SQ/CustomAnalysis/EchoForgeOverviewExporter.java
[S15]: https://github.com/xKoRx/symphony/blob/22f337ca434549c492b2d402fd158e23ac4758a8/sqx/activities/worker/import_metadata.go
[S16]: https://github.com/xKoRx/symphony/blob/22f337ca434549c492b2d402fd158e23ac4758a8/sqx/adapters/metadata-mongo/adapter.go
[S17]: https://github.com/xKoRx/symphony/blob/22f337ca434549c492b2d402fd158e23ac4758a8/sqx/adapters/metadata-mongo/evidence_store.go
[S18]: https://github.com/xKoRx/symphony/blob/22f337ca434549c492b2d402fd158e23ac4758a8/sqx/adapters/metadata-mongo/evidence_documents.go
[S19]: https://github.com/xKoRx/symphony/blob/22f337ca434549c492b2d402fd158e23ac4758a8/sqx/adapters/metadata-mongo/evidence_indexes.go
[S20]: https://github.com/xKoRx/symphony/blob/22f337ca434549c492b2d402fd158e23ac4758a8/sqx/activities/worker/trade_list_exporter_activity.go
[S21]: https://github.com/xKoRx/symphony/blob/22f337ca434549c492b2d402fd158e23ac4758a8/sqx/workflows/durable_trade_list_workflow.go
[S22]: https://github.com/xKoRx/symphony/blob/22f337ca434549c492b2d402fd158e23ac4758a8/sqx/adapters/trade-list/binding/contract.go
[S23]: https://github.com/xKoRx/symphony/blob/22f337ca434549c492b2d402fd158e23ac4758a8/sqx/adapters/trade-list/binding/evidence.go
[S24]: https://github.com/xKoRx/symphony/blob/22f337ca434549c492b2d402fd158e23ac4758a8/sqx/adapters/trade-list/binding/persist.go
[S25]: https://github.com/xKoRx/symphony/blob/22f337ca434549c492b2d402fd158e23ac4758a8/sqx/exporter-plugin/src/SQ/CustomAnalysis/EchoForgeTradeListExporter.java
[S26]: https://github.com/xKoRx/symphony/blob/22f337ca434549c492b2d402fd158e23ac4758a8/sqx/exporter-plugin/src/SQ/CustomAnalysis/trades/ProductionSQXTradeSource.java
[S27]: https://github.com/xKoRx/symphony/blob/22f337ca434549c492b2d402fd158e23ac4758a8/sqx/exporter-plugin/src/SQ/CustomAnalysis/trades/ClosedTradeNormalizer.java
[S28]: https://github.com/xKoRx/symphony/blob/22f337ca434549c492b2d402fd158e23ac4758a8/sqx/exporter-plugin/src/SQ/CustomAnalysis/trades/TradesJson.java
[S29]: https://github.com/xKoRx/symphony/blob/22f337ca434549c492b2d402fd158e23ac4758a8/sqx/exporter-plugin/src/SQ/CustomAnalysis/trades/TradeExtractionService.java
[S30]: https://github.com/xKoRx/symphony/blob/22f337ca434549c492b2d402fd158e23ac4758a8/sqx/exporter-plugin/src/SQ/CustomAnalysis/trades/TradeIdentity.java
[S31]: https://github.com/xKoRx/symphony/blob/22f337ca434549c492b2d402fd158e23ac4758a8/sqx/exporter-plugin/src/SQ/CustomAnalysis/trades/TradeCapabilities.java
[S32]: https://github.com/xKoRx/symphony/blob/22f337ca434549c492b2d402fd158e23ac4758a8/sqx/adapters/metadata-mongo/trade_lists.go
[S33]: https://github.com/xKoRx/symphony/blob/22f337ca434549c492b2d402fd158e23ac4758a8/sqx/adapters/storage-minio/trade_lists.go
[S34]: https://github.com/xKoRx/symphony/blob/22f337ca434549c492b2d402fd158e23ac4758a8/sqx/adapters/storage-minio/durable_artifacts.go
[S35]: https://github.com/xKoRx/symphony/blob/22f337ca434549c492b2d402fd158e23ac4758a8/sqx/core/trades/decoder.go
[S36]: https://github.com/xKoRx/symphony/blob/22f337ca434549c492b2d402fd158e23ac4758a8/sqx/activities/worker/historical_cohort_activity.go
[S37]: https://github.com/xKoRx/symphony/blob/22f337ca434549c492b2d402fd158e23ac4758a8/sqx/adapters/registry-postgres/stage_execution.go
[S38]: https://github.com/xKoRx/symphony/blob/22f337ca434549c492b2d402fd158e23ac4758a8/sqx/adapters/registry-postgres/adopt_strategy.go
[S39]: https://github.com/xKoRx/symphony/blob/22f337ca434549c492b2d402fd158e23ac4758a8/sqx/adapters/registry-postgres/strategy_manifest_identity.go
[S40]: https://github.com/xKoRx/symphony/blob/22f337ca434549c492b2d402fd158e23ac4758a8/sqx/adapters/registry-postgres/strategy_version.go
[S41]: https://github.com/xKoRx/symphony/blob/22f337ca434549c492b2d402fd158e23ac4758a8/sqx/adapters/registry-postgres/strategy_handoff_reads.go
[S42]: https://github.com/xKoRx/symphony/blob/22f337ca434549c492b2d402fd158e23ac4758a8/sqx/core/domain/strategy_version.go
[S43]: https://github.com/xKoRx/symphony/blob/22f337ca434549c492b2d402fd158e23ac4758a8/sqx/activities/worker/forge_seal_handoff.go
[S44]: https://github.com/xKoRx/symphony/blob/22f337ca434549c492b2d402fd158e23ac4758a8/sqx/core/runtime/cfx_configured_period.go
[S45]: https://github.com/xKoRx/symphony/blob/22f337ca434549c492b2d402fd158e23ac4758a8/sqx/core/domain/canonical_strategy_id.go
[S46]: https://github.com/xKoRx/symphony/blob/22f337ca434549c492b2d402fd158e23ac4758a8/sqx/core/domain/persistence_identity.go
[S47]: https://github.com/xKoRx/symphony/blob/22f337ca434549c492b2d402fd158e23ac4758a8/sqx/workflows/generic_workflow.go
[S48]: https://github.com/xKoRx/symphony/blob/22f337ca434549c492b2d402fd158e23ac4758a8/sqx/go.mod
[S49]: https://github.com/xKoRx/symphony/blob/22f337ca434549c492b2d402fd158e23ac4758a8/sqx/adapters/mt5/binding/reretester_baseline.go
[S50]: https://github.com/xKoRx/symphony/blob/22f337ca434549c492b2d402fd158e23ac4758a8/sqx/exporter-plugin/src/SQ/CustomAnalysis/trades/ManifestJson.java
[S51]: https://github.com/xKoRx/symphony/blob/22f337ca434549c492b2d402fd158e23ac4758a8/sqx/adapters/magic-readback/readback.go

[SDK01]: https://github.com/xKoRx/sdk/blob/c7f11496b6f681687c9e1e41a773a13295640351/pkg/sqx/trade.go
[SDK02]: https://github.com/xKoRx/sdk/blob/c7f11496b6f681687c9e1e41a773a13295640351/pkg/sqx/trade_manifest.go

## Fuentes

- Source Symphony/SDK fijado por SHA y blob en el apéndice del informe.
- [[B — Frozen Design]] y [[Contract Source Review]].
