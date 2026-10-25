---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo Forge — Operación Real V2]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-25"
updated: "2026-10-25"
---

# 05 — Technical Specification

## Propósito

Contrato **PROPUESTO** `dynamic-groups.v1`. Diseñado sobre `xKoRx/symphony@dd4af7d`; no existe todavía en ese HEAD. Los nombres nuevos de este documento son el freeze técnico del Shot 1. Los contratos V1 existentes conservan bytes e identidades.

## Contenido

### 1. Superficie declarativa y validación

Añadir `WorkflowSpec.execution_contract` con valor opcional `dynamic-groups.v1`. Ausente conserva el camino vigente. El watcher, worker y CLI de validación comparten parser estricto para esta versión; rechazo de campos desconocidos de las extensiones, y check de preservación raw→typed→config durable antes de dispatch. Un binario que no declara esa capability no recibe la ejecución. No depender sólo de `json.Unmarshal`, que descarta campos desconocidos.

Añadir a `TaskSpec`: `target` (sólo group), `input_bindings` (sólo tareas con capability declarada), `execution_inputs` (refs/config versionados del adapter cuando corresponda). `batch_size` sigue siendo Y; `max_parallel` limita leaves admitidas desde el group raíz, no crea un nuevo pool SQX. Cada task de un flujo V2 tiene `name` único global según el normalizador existente y `TaskPath` estructural resuelto al congelar spec. Los nombres eligen la task, no activan lógica física. El producer binding se compila a TaskPath; task de mismo tipo con otro nombre es distinta.

`target` exige: `schema=group-target.v1`, `partition_by=logical_type`, `source`, `top_n`, `ranking`, `continuation=until_target_or_exhausted`. X,Y positivos <=2^31−1; K positivo y no mayor al presupuesto de children congelado en spec. No X=0, no default 5. `target` y source/source_folder/cohort_wave legacy simultáneos son inválidos. La fuente actual se declara `current_batch`; ranking completo y SelectionSnapshot son otras alternativas explícitas. No listado implícito si input vacío.

El JSON Schema `group-target.schema.json` valida el bloque completo `target`; los ejemplos contienen TaskSpec completos bajo `examples/`. Un segundo pase semántico obligatorio valida TaskSpec con `ValidateWorkflowSpec`, los binding descriptors y los invariantes aquí descritos. JSON Schema no pretende resolver el grafo de dependencias ni probar existencia de bytes/refs externos. Las referencias de fixtures de los ejemplos son ilustrativas, no candidatas de producción.

### 2. Contratos C01–C15 y dueño

| Contrato | Dueño / entrada → salida | Validación, identidad y persistencia | Compatibilidad / error |
|---|---|---|---|
| C01 GroupTarget | runtime; target + group TaskSpec → plan congelado | X,Y,K, named algorithms, fuente única; digest canonical spec; PG config actual | Opt-in; INVALID_SPEC |
| C02 TaskSequence | workflows; tasks+StratBatch+scope → TaskResult/StratBatch | misma dispatch para raíz/nesting; paths estructurales, dependencias; historial Temporal | Shell legacy para replay; UNSUPPORTED_TASK |
| C03 LogicalBatch | group; cursor+i+Y → slice de candidatas | exactamente min(Y,remaining), orden congelado, dedupe StrategyRef; manifest antes de dispatch | Sin alterar batch legacy; CANDIDATE_CONFLICT |
| C04 PartitionSource | fuente; snapshot/input + clasificación → CandidateUniverse | snapshot exacto, ownership de input, logical_type único, no truncar top implícitamente; hash manifest MinIO | Sin fuentes live; SOURCE_CONFLICT |
| C05 RankingAlgorithm | domain/ranking; candidates+algorithm/version/params → orden y componentes | catálogo cerrado extensible por código; delega MinMaxV1 o score sort; digest de algoritmo+params | V1 intacto; UNKNOWN_ALGORITHM |
| C06 RankingEvidence | activities; task path+instance scope+selector+StrategyRef → EvidenceInput | producer exacto, ref/digest/schema/units/windows y supervivencia; ledger de task results | No latest; EVIDENCE_MISSING/AMBIGUOUS |
| C07 PartitionCheckpoint | PG group control; expected revision+iteration result → checkpoint | CAS y chain predecessor; ref universo y accumulator; una fila por partición | Nueva tabla justificada; CAS_CONFLICT |
| C08 CandidateSupply | source resolver; frozen universe+cursor → batch/ExhaustionProof | EOF sólo si cursor==count, manifest verificado; límite no equivale a EOF | Campaign Builder supply separado; SOURCE_UNAVAILABLE |
| C09 GroupResult | group; estados terminales+ranking → StratBatch con refs | COMPLETE exact X; UNDERFILLED <X con EOF; sin duplicates; SelectionSnapshot V2 | Forma normal para consumidores; INCOMPLETE_ACCOUNTING |
| C10 DynamicInput | runtime resolver; producer binding+selector+target → ResolvedBinding | capability, tipo, orden y scope; inputs exactos+digest en config/evaluation | Opt-in; UNSUPPORTED_BINDING |
| C11 SelectedWFMPeriod | WFM adapter; Decision+CELL → SelectedPeriod | mismo StrategyRef, celda, último no future, parámetros e IS; Evaluation inmutable | No fallback V1 ambiguo; WFM_PERIOD_INVALID |
| C12 SQXEffectiveConfig | SQX adapter; frozen CFX+period+setup selector → CFX artifact | sólo dos atributos; hash fuente+resultado, readback; MinIO y Evaluation | Sin binding usa ruta existente; CFX_PATCH_CONFLICT |
| C13 MT5EffectiveConfig | MT5 adapter; EX5 lineage+period+config → INI/report | fechas representables, data/calendar profile; readback+hash; durable evidence | Sin binding conserva fechas fijas; PERIOD_NOT_REPRESENTABLE |
| C14 EvidenceLedger | Foundation; TaskResult → ledger immutable | StrategyRef+TaskPath+scope+generation, exact refs; no overwrite de productores | Campos aditivos de carrier; PAYLOAD_CONFLICT |
| C15 Recovery | workflow+stores; checkpoint+history+version → resume | misma identidad/config/inputs, insert-once y drain físico; bounded replay | Contratos V1/V2 separados; INCOMPATIBLE_RESUME |

Extensión prevista: nuevos task handlers y selectors se registran en el mismo módulo con tipos y pruebas; nuevos algoritmos se implementan en el mecanismo existente; otros campos dinámicos usan descriptors. No DSL de expresiones, scripting remoto, registry de servicio ni engine nuevo.

### 3. Fuente, partición y supply

`source.kind` es una unión: `current_batch` (entrada actual explícita), `selection_snapshot` (ref exacta V1/V2, el universo es su selección declarada), `ranking_snapshot_full` (lista de refs exactas PER_LOGICAL_TYPE y sus OrderedEntries completos). Cada source declara `classification_name`; se resuelve a exactamente un binding ClassificationSnapshot del input, o a la misma clasificación citada por las snapshots. Snapshot externa requiere FlowRun productor terminal y permisos de lectura del consumidor; validar cada carrier/artefacto y registrar membresía REPROCESSED cuando el mecanismo vigente lo exige. Nunca reconstruir StrategyRef de keys.

CandidateUniverse.v1 = {group_execution_key, source_refs, classification_ref, partitions:[{logical_type, members:[{ordinal,strategy_ref,artifact_ref,input_evaluation_ref,input_bindings_ref}]}]}. Orden canónico: logical_type lexicográfico; miembros por StrategyRef para current/selection, o rank asc/StrategyRef para ranking_full. Ordinal se asigna tras dedupe. Duplicado idéntico se colapsa; mismo StrategyRef con artefacto, logical_type o refs diferentes falla. La clasificación congelada no se recalcula después de optimizar y no cambia por pérdida de métricas.

Las particiones vienen del conjunto explícito de la clasificación intersectado con el universo; se conservan particiones vacías identificadas por la clasificación para reportar 0/X. Lista de particiones vacía produce group completo vacío sin buscar fuentes adicionales. El universo completo se persiste antes de iniciar children; cuenta, digest y páginas quedan congelados. Su lectura paginada usa ordinal estable, no offset sobre una consulta mutable. Historical supply significa más candidatas de ese manifest. Builder supply ocurre en `ForgeCampaignWorkflow` fuera del group; una wave nueva crea invocación nueva. No añadir un Builder escondido cuando source se agota.

### 4. Estado y algoritmo del control

Estados por partición: READY → ITERATION_PLANNED → RUNNING → RESULTS_COMMITTED → RANKED → READY / COMPLETE / UNDERFILLED. PAUSED, FAILED y CANCELLED son salidas operacionales, separadas del resultado analítico. `top_n` alcanzado al cierre de la iteración tiene precedencia sobre EOF si coinciden. La partición vacía va directamente a UNDERFILLED con selección vacía y exhaustion proof.

```text
freeze universe/config and create partition rows idempotently
for each partition, while not terminal:
    if checkpoint has planned iteration: recover exactly that plan
    else reserve next min(Y, remaining) unique candidates; persist plan
    if no candidates: validate exhaustion; publish UNDERFILLED
    execute declared sequence from task 0 for new candidates only
    require outputs + analytic_rejections == planned candidates
    persist all task result evidence; atomically commit iteration reference
    accumulator = prior survivor refs UNION new survivor refs
    rank entire accumulator using declared source/policy/version
    if eligible_count >= X: publish first X and COMPLETE
    else if cursor == universe_count: publish eligible and UNDERFILLED
    else advance iteration and repeat
publish normal StratBatch after all partitions terminal
```

Un survivor conserva la salida de la última task y las métricas exactas de la task de ranking, aunque sean productoras diferentes. Re-rankear es obligatorio para minmax: nuevos extremos pueden cambiar el score de todos. No acumular sólo Top X parcial ni normalizaciones de batches independientes. Tie-break por StrategyRef ascendente, sin clocks, host ni completion order. `created_at` se fija una vez al crear el registro durable y se recupera en retries; no altera identidad ni payload en re-publicación.

Una iteración por partición en vuelo evita que races cambien el corte. Scheduler raíz en round-robin de particiones ordenadas, máximo K leaf executions y presupuestos de workers físicos existentes. Groups anidados consumen tokens sólo cuando lanzan leaves; un parent esperando child no retiene un token que cause deadlock. K global se propaga como contexto de la invocación, no se multiplica por profundidad. Cancellation/error cancela siblings, drena futures y espera cleanup físico según contratos actuales antes de liberar recursos. Ningún resultado final parcial se publica si otra partición falló por contrato/infraestructura; sus evidencias válidas se conservan para recuperación.

### 5. Persistencia e identidad exactas

**Nueva tabla PROPUESTA `sqx.group_partition_runs`**: `group_execution_key text`, `logical_type text`, `flow_run_id uuid FK`, `group_stage_execution_id uuid FK`, `contract_version text`, `config_digest text`, `universe_ref text`, `universe_count bigint`, `cursor bigint`, `iteration bigint`, `state text`, `planned_iteration_ref text nullable`, `accumulator_ref text nullable`, `ranking_ref text nullable`, `selection_ref text nullable`, `exhaustion_ref text nullable`, `row_version bigint`, `created_at`, `updated_at`. PK `(group_execution_key,logical_type)`; unique ref digest checks in adapters; cursor entre 0 y universe_count, iteration>=0; estados terminales inmutables. Se crea una sola vez con config/universe congelados y readback comparativo. No tabla de métricas duplicada.

Iteration plan, committed result, accumulator y exhaustion son Evaluations inmutables sobre subject BATCH en las colecciones actuales, con manifest de miembros en MinIO cuando el payload supere 256 KiB. Ref de manifest incluye digest/size; historial Temporal transporta refs y contadores, no todo el universo. El acumulador se almacena como manifest completo de refs ordenadas por StrategyRef para simplicidad y verificabilidad; mantiene también `previous_accumulator_ref` para audit. No pruning antes de ranking final.

Protocolo de commit: persistir bytes MinIO insert-once → persistir Evaluation/MetricSets Mongo insert-once → verificar refs → CAS PG sobre expected row_version, planned_iteration_ref y estado. CAS idéntico ya aplicado = éxito idempotente; contenido distinto = conflicto. Crash después de Mongo antes de PG: retry encuentra mismos hashes y completa CAS. Crash después de PG antes de ACK: readback devuelve mismos refs, no ejecuta de nuevo ni avanza cursor. Evidencia no alcanzable por CAS se conserva como intento no publicado, nunca se considera acumulada. Cursor avanza sólo al commit del accounting completo; planned slice permanece reservado durante reintentos.

GroupExecutionKey = `HashIdentity("group-execution.v1", FlowRunRef, groupTaskPath, parentScopeDigest, generation, groupConfigDigest, universeDigest)`. PartitionKey incorpora logical_type exacto. IterationKey = Hash(partitionKey, ordinal, ordered candidate refs digest). TaskPath conserva `root(/[0-9]+)*`; no insertar nombres, UUIDs ni logical_type en ese path.

**Extender StageExecution identity a V2**, sin cambiar `NewStageExecutionIdentity` V1: `slot=HashIdentity("stage-instance.v2", taskPath, stageKey, subjectKind, subjectToken, inputsDigest, executionScopeDigest, effectiveConfigDigest)`; `intent=HashIdentity("stage-execution.v2", FlowRunRef,slot,generation)`. executionScopeDigest = hash de la pila de group execution keys + partition + iteration + physical-slice ordinal (si aplica). StrategyRef no cambia por task/retry; generaciones sólo cambian por reevaluación deliberada. Antes de conocer StageExecutionRef, config y manifests se direccionan por hash/scope, evitando una dependencia circular.

PG `stage_executions` añade `identity_schema_version` (default v1), `execution_scope_digest` y `effective_config_digest` nullable; validar v1 sin columnas V2 y v2 con ambas. Actualizar constructores, readers, convergencia y unique execution_intent existente; no renumerar refs V1. SubjectSnapshot guarda scope/config refs para audit, no reemplaza autoridad de las columnas/digest.

TaskResult.v2 = {task_path,execution_scope_digest,generation,strategy_ref,stage_execution_ref,status,outputs[],rejection?,evidence:[{role,evaluation_ref,metric_set_refs[],trade_set_refs[],schema_version}],effective_config_ref}. `status` = SURVIVED / ANALYTIC_REJECTED; errores de contrato/infra no son una tercera forma de éxito. Output cardinality es contrato de la tarea; para este group las transformaciones preservan StrategyRef 1:1 o descartan. Un handler que crea identidades nuevas debe declarar lineage map bijectivo hacia candidate y garantizar una salida por candidate; multiplicidad ambigua es incompatibilidad pre-dispatch, no dedupe arbitrario.

Carrier/Batch añaden `task_result_bindings` (refs del ledger por StrategyRef), `group_results` (refs+status por partición) y `input_presence=EXPLICIT`. Los campos EvaluationRef/ApplyEvaluationRef/CompileEvaluationRef existentes conservan su función. Group output contiene tanto Keys como artifacts coherentes; `batchKeysFrom`, `batchKeysForExactArtifacts`, merge y reset deben preservar nuevos bindings y presencia explícita. Consumidor con vacío explícito no llama list_strats. SelectionSnapshot no autoriza promoción ni Echo.

### 6. Ranking/selection sin motor paralelo

Envelope **RankingSnapshot V2** en el store actual, discriminator `ranking-snapshot.v2`; no escribir simultáneamente V1 para el mismo resultado. Identidad incluye GroupExecutionKey, logical_type, accumulator digest, ranking config digest, comparability policy digest y input evidence digest. Entries usan `strategy_ref`, `input_evidence[]` (task path, EvaluationRef, MetricSetRef/ScoreRef, scope digest), score, components y rank. ClassificationSnapshot sólo define partición; sus BuilderEvaluationRefs no se reasignan fraudulentamente a una evaluación posterior.

Selector de ranking es unión tipada `metric_set` o `score` con `task`, `role`, `schema`. Resuelve ledger de esa candidata, iteración y scope; debe haberse ejecutado dentro del subflujo. Ausencia de task, ejecución posterior, salida sibling ajena, más de un match o task sin la capability requerida = rechazo. No hay búsqueda por carpetas. Inputs omitidos por filtrado legítimo se contabilizan como rechazados antes del ranking; inputs esperados pero perdidos fallan.

Dos algoritmos iniciales, sin default: `weighted_combination_minmax.v1@1.0.0` llama al `ranking.MinMaxV1` compartido ya usado por `ranking_snapshot_per_type.go`; params `{schema_version:"weighted-combination-minmax-params.v1",metrics:[{code,direction:BENEFIT|COST,weight:integer>0}]}`. Metric code existe en catálogo; no alias; pesos relativos positivos siguen exactamente kernel vigente (no imponer suma=100). `score_descending.v1@1.0.0` reutiliza ordenamiento/validación de `BuildRankingSnapshot` sobre ScoreEvidence exacto, params `{schema_version:"score-descending-params.v1",direction:"DESC"}`. Extraer cálculo del envelope cuando sea necesario; no volver a implementar la fórmula ni registrar ranking en el registry de comparación baseline/optimized.

Elegibilidad = lista explícita de predicados `metric_status_observed`, `metric_compare` (code, op enum gt/gte/lt/lte/eq, finite numeric value) o `score_status_computed`. Todos conjunctivos; array vacío = toda evidencia estructuralmente válida. No hay PF/Sharpe/Fidelity obligatorios. Distinguir métrica requerida inexistente en schema/catálogo (CONTRACT_ERROR) de valor con status MISSING admitido por el contrato del productor (exclusión explícita `METRIC_NOT_OBSERVED` si la política la declara; de lo contrario falla). NaN/Inf, ref inconsistente o scope falso siempre error. Rankear cero elegibles genera snapshot V2 vacío válido: adaptar el guard V1 `ranking cohort cannot be empty` sin debilitar V1.

Comparability.mode = `same_window` o `declared_variable_windows`. Ambos exigen misma unidad por métrica, calculador/version, instrumento normalizado, timeframe, moneda/PNL basis y sample kind compatible. same_window exige mismas fronteras UTC y calendario; variable exige acknowledgment no vacío y misma semántica de métrica, conserva todas las ventanas/duraciones sin anualización automática. Mezcla de ventanas bajo same_window = fallo contractual de configuración; no desechar selectivamente hasta llenar X. La política variable es declaración explícita del owner de campaña, no recomendación económica ni default IMOX.

SelectionSnapshot V2 reutiliza la política top_n y store actual: source group/partition rank refs, entries genéricas, exclusions, requested/effective y status+exhaustion_ref. Lectores aceptan V1/V2, writers eligen una. Output normal = StratBatch con esos bindings y artifacts finales seleccionados, en orden `(logical_type,rank,StrategyRef)`. El ranking se ejecuta dentro del control group; los hooks globales sólo se ejecutan si fueron declarados aparte.

### 7. Dynamic bindings

`input_bindings[]` = `{target,selector,source}`. Targets iniciales: `selected_period` para Apply, `evaluation_period` para SQX/MT5, `evaluation_source` para evaluate_strategy durable. Selectors iniciales: `wfm.selected_last_is.v1`, `applied_wfm_period.v1`, `exact_evaluation.v1`. Source = `{task,role,schema}` para productor previo en la misma rama; o `{scope:"group_input",role,schema}` sólo si el target admite evidencia de entrada. No JSONPath arbitrario, expresiones, latest ni ids fabricados. El ranking source siempre nombra una task del subflujo; no usa group_input directamente.

Descriptor de capability, estático junto al handler: targets aceptados y tipos, schemas de evidencia producida/consumida, cardinalidad física, required binding dependencies y empty-input behavior. Dependencias sólo se agregan por bindings declarados. Cada binding exige source dominante en la secuencia (o entrada explícita); ciclos y forward refs fallan al validar. Un producer en group anidado sólo exporta outputs declarados al boundary y no permite escoger una iteración por posición.

ResolveTaskInputs ocurre después de confirmar upstream TaskResult y **antes de calcular StageExecution V2 y despachar side effects**. Lee refs exactas en activity, devuelve canonical ResolvedBinding/EffectiveTaskConfig y queda en historia+evidencia. EffectiveTaskConfig.v1 contiene static spec digest, task path/scope/StrategyRef, source evidence refs y payload digests, resolver id/version, typed values, artifact/config SHA, adapter version y calendar/data-profile refs. Hash canónico domain struct JSON con arrays ordenadas y números finitos según contrato; nunca map serialization no especificada. Retry carga esta configuración, no vuelve a resolver desde evidencia reciente.

`exact_evaluation.v1` permite a `evaluate_strategy` reutilizar calculadores actuales con una Evaluation/TradeSet exacta por candidata, sin consulta legacy por filename. El adapter durable publica `strategy-metrics.v2` y TaskResult; ésta es la muestra de una sola tarea sin SQX/MT5. El algoritmo de ese group consume esas métricas de la task, no inventa datos. Camino shadow V1 queda intacto para replay. Cualquier otro target no soportado es UNSUPPORTED_BINDING antes de iniciar trabajo.

### 8. WFM y Apply: una autoridad para parámetros y fechas

El adapter WFM carga RobustSelection Decision exacta → `RobustSelectionOutput.CellEvaluationRef` → CELL Evaluation y matriz artifact con SHA. Verifica FlowRun/StrategyRef, runs_count/oos_percent, selected rank=1 y MetricSetRef. Lee períodos persistidos en CELL; conserva nombres serializados reales de PeriodWindow V1 (From/To/FromEpochMS/ToEpochMS). No asumir que el JSON crudo Java y el JSON durable tienen el mismo casing.

Regla seleccionada: todos los períodos deben tener índice explícito único y future flag OBSERVED; los futuros conocidos se excluyen; no future conocido false implica ninguna selección. Entre no-futuros, el de mayor period_index es el último; exigir cronología no decreciente de IS.from/IS.to y OOS boundaries observadas y que ese último sea temporalmente el más reciente. Duplicidad, índice inferido por parser sin prueba del artifact raw, future desconocido, empate conflictivo o cronología incoherente falla. No saltar un último período inválido para usar uno anterior.

IS.from/to y parámetros de ese mismo período son obligatorios. Autoridad temporal primaria = epoch_ms exactos del productor con semántica de endpoint y calendar profile certificado. Strings sin offset que produce `SimpleDateFormat` no bastan; ambos presentes deben concordar bajo el producer timezone documentado. WFM exporter V2 añade metadata de timezone, epoch semantics, endpoint semantics y period_index provenance; Java no deriva ventanas de trades. Artifact legacy sólo es utilizable si su profile versionado y readback/raw prueban todos esos hechos; de lo contrario WFM_PERIOD_INVALID, sin rellenar fechas por configuración histórica.

SelectedPeriod.v1 se publica como Evaluation derivada inmutable: strategy_ref, DecisionRef, CellEvaluationRef, matrix artifact ref, runs_count/oos_percent, period_index, raw IS/OOS, normalized IS, parameters canonical JSON/digest, resolver version, calendar_profile_ref y provenance `OPTIMIZED_IS_BASELINE`. Identidad hash de estas entradas; OOS se preserva sin reinterpretación.

Apply opt-in recibe `selected_period` con ese binding; exporter robust-run V2 debe buscar el índice/celda exactos en la estrategia WFM física, verificar parámetros contra digest, aplicar **esos** testParameters y devolver readback de parámetros+period_ref+artifact SHA. La ruta V1 `getBestParameters` con último elemento sólo sigue vigente sin binding. Si el plugin no soporta pin/readback, preflight falla; no correr V1 esperando el mismo resultado. Magic allocation vigente se preserva. Apply Evaluation V2 contiene selected_period_ref y parameters digest. `applied_wfm_period.v1` para SQX/MT5 carga Apply Evaluation exacta y verifica la relación con SelectedPeriod; así ambas tareas resuelven desde la misma autoridad sin depender una de otra por nombre.

### 9. Tiempo, SQX y MT5

EvaluationPeriod.v1 = `{from_utc,to_utc,bounds:"[)",calendar_profile_ref,source_period_ref,purpose:"OPTIMIZED_IS_BASELINE"}`. Siempre from<to. Calendar profile inmutable identifica dataset timezone (IANA o offset fijo explícito), tzdb version cuando aplique, session calendar, epoch interpretation y semántica de dateFrom/dateTo y MT5 FromDate/ToDate. Si source incluye último día/instante inclusive, el adapter convierte mediante su granularidad declarada; no sumar 24h ciegamente en DST. La conversión inversa de ambas configs debe recuperar exactamente el mismo intervalo. No recortar a intersección ni desplazar horas silenciosamente.

**CFX:** watcher congela bytes y dependencias templateFile por SHA antes del run. execution_inputs.sqx = `{setup:{entry,setup_id},calendar_profile_ref,data_manifest_ref}`: selector exige una entrada ZIP exacta y un Setup activo `Data/Setups/Setup` por ID exacto; no CrossChecks/OOS/GenerateConfig. Duplicados/zip traversal/oversized entries fallan. Copiar a path de ejecución local bajo scope; editar sólo atributos dateFrom/dateTo. Mantener bytes de entradas no tocadas y verificar diff XML semántico de la entrada: sólo esos atributos cambiados; persistir SHA de ZIP original/efectivo y JSON de cambios permitidos. Template externo mutable se congela y carga desde su copia fijada o se rechaza, nunca volver a la ruta viva. El patch puede cambiar compresión/metadata ZIP; el gate de contenido de otras entradas exige bytes descomprimidos idénticos. Volver a parsear con selector estricto, no usar el parser actual permisivo que devuelve missing cuando ambiguo.

Primera versión de dynamic dates ejecuta una estrategia por unidad física. Task sequence descompone el lote según descriptor de capacidad (Optimizer sigue 1), ejecuta cada unidad bajo StageExecution/scope propios y reúne outputs antes de la task siguiente. No reduce Y ni X por limitación física. Nunca despliega un segundo worker en el host; max activity=1 sigue invariante. Source drift después del freeze se informa pero la ejecución usa los bytes congelados; falta de bytes congelados es error, no fallback. Resultado persiste período solicitado y configurado, artifact lineage, MetricSets full-tick, TradeSets y referencias de curvas existentes; no fabricar curva cuando productor no la ofrece.

**MT5:** execution_inputs.mt5 identifica calendar_profile_ref y data_manifest_ref; input EX5 debe provenir de compile del MQ5 exportado de la misma estrategia parametrizada y Apply Evaluation. Copiar MT5BacktestConfig por instancia, resolver `evaluation_period`, traducir a From/To exactos, escribir INI por execution key en slot adquirido por mecanismo actual. No modificar config compartida ni task original. Registrar INI SHA, readback de fechas en HTM/tester logs, model=4 cuando la task solicita real-tick, símbolo/canonical instrument, timeframe, dataset/data provenance y warnings. Calendar/data availability se verifica antes de ejecutar, usando manifest con coverage de sesiones y gaps explícitos; ausencia es DATA_UNAVAILABLE, nunca NO_TRADES ni UNDERFILLED.

Comparabilidad SQX/MT5 exige StrategyRef+Apply ref/parameters digest, normalized period, dataset instrument/timeframe/session model, sample kind y datos cubiertos equivalentes. Requested window ≠ first/last trade: cero trades puede ser un resultado válido con evidencia de run completo. Si readback de una build no demuestra fronteras o datos, resultado `NOT_COMPARABLE` con causa y task no satisface una política que exige comparabilidad. Fidelity existente se puede ejecutar opt-in; no puede tapar un mismatch temporal aunque su valor numérico resulte bueno. Pruebas físicas del profile por build forman parte del gate C del plan E2E.

### 10. Errores, observabilidad y recovery de versión

| Clase | Ejemplos | Acción |
|---|---|---|
| CONTRACT, non-retryable | schema/producer equivocado, source inexistente, refs cruzadas, binding no soportado, período ambiguo, CFX diff prohibido | Fallar con contexto exacto; conservar evidencia; nunca UNDERFILLED |
| OPERATIONAL, retryable conforme al adapter | store temporalmente inaccesible, worker crash, datos no disponibles transitoriamente | Retry mismo plan/config; si requiere intervención PAUSED con causa y cursor intacto |
| ANALYTIC, éxito negativo | filtros explícitos, score NOT_COMPARABLE permitido por policy, cero survivors con accounting | Excluir con motivo, consumir siguiente lote; EOF real puede UNDERFILLED |
| CANCELLED / budget | cancelación explícita, límite de concurrencia/ventana de mantenimiento | No EOF; drenar físicos, preservar checkpoint y no publicar top terminal |

Query/proyección desde PG expone estado por partición y aggregate: universo/cursor/iteration/elegibles/seleccionadas/requested, refs de última evidencia y fallo. Telemetría usa etiquetas acotadas de stage/status/reason; StrategyRef, task path y logical_type de alta cardinalidad van en trazas/eventos consultables. No consulta directa mutable desde código workflow.

Versioning: marker Temporal nuevo para activar dispatcher V2 sólo bajo execution_contract. Viejas historias siguen shell V1 hasta drenarse; mismas actividades V1 y formulas. Nuevos contratos de activity para inputs V2, sin cambiar payloads en replay. Config congelada incluye versiones de handler/resolver/kernel; worker nuevo debe soportarlas o rechaza INCOMPATIBLE_RESUME. Continue-as-new sólo en frontera RANKED/READY con cero children en vuelo, conservando FlowRun/intent y refs; se dispara por sugerencia de SDK/historial antes de límites, nunca convierte generación en retry. Root y child continuation usan mecanismo Temporal existente, no scheduler alterno.

Rollout futuro: migración aditiva → readers V1/V2 → watcher+worker compatibles y capability probe → fixtures/replay → pequeños E2E → habilitar config opt-in. Rollback deshabilita nuevas admisiones, drena o pausa V2 y mantiene workers capaces de finalizar V2; no bajar binario a uno que ignore campos nuevos mientras exista ejecución V2 ni borrar evidencias/columnas. No deploy en Shot 1.

## Fuentes

[[02 — Capability Inventory]], [[03 — Target Architecture and Decisions]], [[04 — Functional Specification]], [[06 — Implementation Plan]], [[07 — Adversarial Plan]], [[08 — Fix and Certification Plan]].
