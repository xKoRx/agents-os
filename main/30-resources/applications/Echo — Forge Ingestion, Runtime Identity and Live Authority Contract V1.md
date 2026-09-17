---
type: resource
schema_version: 1
status: active
area: "[[Echo]]"
sources: ["[[Echo — Fuentes de arquitectura y producto 2026-09-06]]", "[[Echo Forge — Fuentes de arquitectura y producto 2026-09-06]]", "[[Echo + Echo Forge — Evidencia de revisión independiente 2026-09-06]]"]
last_verified: "2026-09-06"
confidence: high
aliases: []
tags:
  - kind/resource
created: "2026-09-06"
updated: "2026-09-07"
---

# Echo — Forge Ingestion, Runtime Identity and Live Authority Contract V1

> [!important] Supersession acotada — 2026-09-07
> [[Echo SDK — Canonical Forge Integration and Analytics Contract V1]] sustituye las propuestas de autoridad en `xKoRx/sdk` y rechazo total de unknown keys por módulo puro Echo SDK + conservación lossless de campos opcionales/capabilities. Mantiene exactamente VersionRef/key y autoridades live ratificadas. Sus §§10–12 gobiernan el nuevo body extensible; el body fijo/rechazo unknown que aparece más abajo queda como propuesta histórica, no para implementar. O1/O3 siguen defaults técnicos de Fable; sólo catálogo CC es decisión owner pendiente.

## Síntesis vigente

### 1. Executive verdict

1. **Cadena actual: NO, todavía incompleta; contrato propuesto: coherente bajo los gates explícitos de este documento.**
2. **Mayor gap semántico:** GeneratedStrategy durable no tiene aún una versión ejecutable exportable ni un productor del binding físico de Reference.
3. **Mayor riesgo de versiones:** resolver un CLOSE o un retry contra la versión/current policy del momento.
4. **Mayor riesgo BWC:** canonical de Campaign puede exceder 64 caracteres; ampliar magic también rompe el layout binario EA, y los tickets MT5 siguen estrechados en DTOs.
5. **Mayor gap raw:** el OPEN no conserva versión/config/SL inicial verificable y el CLOSE actual confunde emisión con tiempo económico; falta coverage demostrable.
6. **Puede congelarse:** identity/version envelope, ingestión individual transaccional, enrollment físico, hechos por posición/deal y resultado esperado por destinatario, con las salvedades owner de §11.
7. No se implementó, no se evaluó performance, no se rehízo auditoría/roadmap ni se estimaron plazos. PASS de este TOP significa contrato documentado, no runtime certificado.

## Autoridad, corte y reglas de lectura

**S** = código/schema inspeccionado; **P** = evidencia física/producción fechada; **D** = decisión owner/frozen existente; **I** = propuesta de este TOP; **U** = no demostrado. Todo MUST/contrato de las secciones 2–12 es **I listo para ratificación**, excepto donde se identifica D. No existe nuevo freeze owner por publicar este Resource. Prioridad: source actual → evidencia física actual → D → Resources → historia → I. Una restricción D no implementada sigue siendo requisito, nunca descripción del runtime.

### Baseline revalidado, last_verified 2026-09-06

| Autoridad | Lectura de esta sesión | Alcance |
|---|---|---|
| Symphony HEAD y master remoto | `db8a022703082fd7ee9d1e15243c5d1b2feaf578`, ambos por git read-only | Sustituye `a10c26c` para source actual. Dirty ajeno en manifest/input/fixtures/specs/workspace preservado y excluido. |
| Echo HEAD local | `e25165ba2e57a86b7cdcbd78d44406f66fc9ba23`, limpio | Source directamente inspeccionado. |
| Echo master remoto | `04c16bd2bd7b69725560873950a5d6b067fd3a4f`, `ls-remote` | El objeto no está local. La diferencia readiness-only está probada por las fuentes anteriores, no recertificada aquí: `gh` sin autenticación. No se hizo fetch/clone. |
| SDK externo HEAD/master | `c85594440f6755443ceb97ec4e333cd0ddb5b0ed` | Distinto de `echo/v3/sdk`. |
| Temporal módulo SQX | `sqx/go.mod` declara **v1.35.0** | S; no representarlo como pin v1.44.1. |
| Temporal build en workspace actual | `go.work` incluye raíz/SQX/deployer; raíz requiere **v1.44.1**; `GOPROXY=off GOSUMDB=off go list -m -mod=readonly go.temporal.io/sdk` desde SQX devuelve **v1.44.1** | S de resolución local; no build ni test ni prueba del binario desplegado. La frase previa «root no gobierna este runtime» es demasiado absoluta para este workspace. |
| Echo core desplegado | P anterior `e25165ba`, binary SHA `447ac7c2e275ca1233043269919418fd4e150e01f2218c28c4e4baccc0fd806d` | Revalidación SSH de lectura rechazada por autenticación. **U actual**, conservar P anterior sin rejuvenecerla. No DB/broker queries aquí. |
| Forge desplegado | P reportada release `0.2.96` | No nueva verificación física. HEAD nuevo no equivale a deploy. |

### Estado congelado de Forge recuperado, sin reabrirlo

| Contrato | Estado exacto al corte actual | Autoridad / límite |
|---|---|---|
| MT5 Slot Pool NORMAL A | Source PASS/CLOSED `1489937` + `a10c26c` | Lease/roots locales por slot; no es prueba física de flota. |
| Global Ownership V2 | Diseño frozen; corregido por V3 | ETCD persistente no-TTL + CAS; lease local sigue válido. |
| Fencing/Cancellation V3 | Frozen | No takeover cross-host desde Symphony, token no fence físico; D1 cancel explícito vs pérdida de intento; singleton y drain. |
| NORMAL B1A | Commit `185825c`, ownership global | S presente; reutilizar antes de spawn. |
| NORMAL B1B | Commit `ef65dd1`, elimina wall-clock limits | S presente; no cap Campaign=4 como autoridad física. |
| NORMAL B2 | Commit `db8a022`, checkpoint PASS/CLOSED | S + certificación local reportada; singleton Windows/drain físico aún no certificados aquí. |
| Finalist V2 C1/C2 | D frozen, **pendientes** | `decision.go` aún policy 1.0.0/output v1 y `promotionFinalists` copia TopProjection. C1 core/result/gates; C2 Campaign/rank nullable/BWC. |
| SQX long-running D | Pendiente según contrato recuperado | Mantiene serialización por databanks; no hereda allocator MT5. No se modifica ni certifica en esta misión. |

NEXT EXACT factory actual: `ECHO-FORGE-FINALIST-MODEL-V2-CORE-PROMOTION-WARNINGS-STRUCTURAL-GATES-NORMAL-C1`. Los Resources anteriores que dicen B1/B2 pendientes describen su corte `a10c26c`; no son el checkpoint actual.

## 2. Canonical identity graph

```text
Forge CampaignRef ──owns── BuilderSupplyBatchRef (CampaignRef:gNNNNNN)
  └─ waves → FlowRunRef ──PRODUCED/REPROCESSED── StrategyRef UUID
                                    ↕ 1:1, identity_model_version=2
                          canonical_strategy_id (GeneratedStrategy)
                                    ├─ 1:1 Forge magic allocation (stable)
                                    └─ 1:N StrategyVersionRef (I, sealed executable semantics)
                                           └─ executable + effective inputs + dependency manifest
FlowRunRef → FINALIST_PROMOTION DecisionRef ──member StrategyRef
  └─ immutable handoff manifest binds member → exact tested StrategyVersionRef
       → Echo PromotionRecord / receipt ──N:1── Echo strategy_versions
            └─ Echo strategy_definitions.id = canonical_strategy_id (descriptor)
StrategyVersionRef → runtime_binding/enrollment (physical attach epoch)
  └─ broker account + magic + executable/config proof
       → Reference OPEN: trade_id + origin position key + binding_id (pinned)
            ├─ MODIFY / partial CLOSE / final CLOSE: same trade_id
            └─ routing result per operation
                 ├─ excluded recipient + reason
                 └─ expected recipient → economic command + applied policy snapshot
                       → Execution deals/positions: same trade_id and command_id lineage
```

### Identidades actuales y propuestas

| Identidad | Creator / autoridad | Formato y scope / unicidad | Store durable | Inmutabilidad, cambio y reconstrucción / BWC |
|---|---|---|---|---|
| `canonical_strategy_id` | S Builder publication + `CanonicalStrategyID`; PG adopt congela; D GeneratedStrategy batch-scoped | String exacto, no algoritmo de equivalencia de lógica. V2 UNIQUE global parcial. Campaign basename incluye CampaignRef + gNNNNNN + ResultsGroup/cohort. | S `sqx.strategies.canonical_strategy_id`, migration006 | Nunca recalcular en Echo, ni renombrar tras adopción. Recuperable desde registry/evidencia exacta; no reconstruible de filename actual/host actual. V0/V1 no se promueven a V2 por inferencia. |
| `StrategyRef` | S PG adopción | UUID `sqx.strategies.id`, global en registry Forge; 1:1 canonical V2 | S `sqx.strategies` | No cambia por otro config/FlowRun. Recuperar fila, no fabricar UUID desde canonical. Scope instancia registry fijo, no namespace nuevo por reinicio. |
| `FlowRunRef` | S intake/PG | UUID; RunIntentKey hash(config UUID, FlowIntentToken). Token global de intención; no Temporal RunID | S `sqx.flow_runs`, relaciones `flow_run_strategies` | Retry conserva; rerun deliberado nuevo token/run. UUID se recupera del store, no se deduce del hash. Config de primera adopción es provenance, no identidad Strategy. |
| `CampaignRef` | S Forge Campaign intake/PG | UUID por intención Campaign; token UUID y content digest separados | S `sqx.forge_campaigns`/waves | Replay conserva; Campaign deliberadamente nueva crea ref. Recuperar registro/token; no usar latest. |
| Builder generation | S/D `NewBuilderSupplyBatchRef` y publicación `steps.go` | Campaign UUID + `:g` + ordinal de 6 dígitos; `(CampaignRef,ordinal,ResultsGroup,cohort suffix)` delimita nueva supply | S wave durable previa al child; canonical publicado/Strategy origin | Batch derivable de esa wave bajo policy V1 1:1, no por fecha/folder. Generic no Campaign conserva autoridad existente. Nuevo batch puede crear nueva Strategy aunque lógica/bytes coincidan. `.zN/.hN/.kN` no son StrategyVersion. |
| `PromotionDecisionRef` | S producer `FINALIST_PROMOTION` | `sha256:<64hex>`; hash namespaced de stage/type/flow/policy/evidence; **no UUID** | S PG `sqx.decisions` + `decision_evidence` | Immutable content digest; no supersedes para Promotion histórica. Se verifica con algoritmo de su versión; no se fabrica desde rank. V1/V2 separados. |
| `magic` canónico | D Forge registry, I asignador concreto | Decimal positivo signed int64 interoperable, `1..9223372036854775807`; único por Strategy en registry Forge, estable cross-cuenta/versiones | I `sqx.strategy_magic`; copia autoritativa recibida en Echo descriptor | Nunca reciclado ni inferido por parsing semántico. Puede reservarse antes de producir finalista y quedar sin uso; no liberarlo. No existe asignador global demostrado en source actual. |
| Artifact ref | S producer + artifact plane | Store identity + bucket + key + SHA256 + size + kind/schema. Ubicación exacta; content digest separado de ref lógico | S MinIO; PG producer output y Mongo evidence | Durable write-once; misma longitud/ETag no prueba bytes. Copia con nuevo locator conserva SHA, no identidad de origen. Permiso/URL puede cambiar. |
| EX4 / EX5 | Compiler, no canonicalizer | Bytes de plataforma específica; SHA256 + size | Forge artifact plane; I copia operativa Echo | Nueva build con bytes distintos = versión nueva. No reconstruir viejo executable compilando source nuevo. EX4 legacy no pasa por EX5 renombrado. |
| Params/config | S Apply config digest; I **effective runtime inputs** completo | Typed map canónico + chart context/dependencies. CFX y apply `ApplicationConfig` no equivalen a todos los inputs EA | S config/evaluations/artifacts; I sealed version manifest | Inputs efectivos inmutables por versión. Defaults deben estar materializados. Mutable config row o nombre `60oos...` no reconstruye parámetros históricos. |
| Echo definition | S Hasura/journal writer, I gateway para namespace nuevo | `strategy_definitions.id` debe ser canonical exacto; no nuevo `echo_strategy_id` | S PG `echo.strategy_definitions` | Labels editables; columnas de provenance protegidas de UPDATE/DELETE. `wave/config` UI no autoridad de versión. Legacy placeholders permanecen distinguibles. |
| Reference strategy ID | S collector hoy `magic_<n>`; D nuevo path canonical antes del journal | Mismo canonical, no identidad extra por cuenta Reference | S payload/journal; I config map por binding | `client_reference_strategy_id` fallback magic=0 no es mapa de todas las estrategias. Legacy alias scoped; no global replace. |
| `StrategyVersionRef` | I Forge seal posterior a compile/config verification | `sha256:<64hex>` sobre execution manifest mínimo de §3, scoped a canonical | I Forge manifest write-once + Echo `strategy_versions` | Inmutable y verificable desde manifest preservado; nunca desde current_version. V2 de Strategy identity y Promotion V2 son ejes independientes. |
| `binding_id` | I Echo registra attach observado | UUID por attach epoch; referencia instancia lógica física, no PID solo | I `echo.reference_bindings` | No se reasigna a otra versión/account. Reattach/rollback = binding nuevo; PID/boot/readback se guardan en proof. |
| `trade_id` | S Reference EA UUIDv7 | Único global del trade económico Reference; Execution hereda. Un trade puede tener N deals | S EA TradeMapper/journal; I raw + position map durable | OPEN/CLOSE/MODIFY comparten ID; retry conserva. No reconstruir UUID aleatorio si se perdió mapa; recuperar mapping central o marcar U. |
| `command_id` | S Core UUIDv7 | Una operación económica concreta a una cuenta; N por trade | S transporte/EA journal; I `economic_commands` | Se asigna una vez al insertar intención durable, antes de enviar; replay reutiliza, no vuelve a llamar constructor random. |

**Challenge identidad:** D más reciente es `GENERATED_STRATEGY / generation-batch-scoped`, no «misma lógica en cualquier Builder = misma Strategy». La identidad semántica cross-generación requeriría otro contrato y está excluida. Misma Strategy significa conservar el StrategyRef adoptado al evolucionar sus parámetros dentro de su lineage, no demostrar equivalencia de código.

## 3. StrategyVersion V1

### Semántica de versión y representación elegida

**I:** versión = paquete exacto de semántica ejecutable de una GeneratedStrategy: plataforma, bytes ejecutables, inputs efectivos, contexto lógico de ejecución y dependencias ejecutables. Se sella **después** de conocer los bytes definitivos y el config efectivo; existe antes de ingestion/attach. No es contador `sqx.strategies.version`, ni WFM selected run, ni expectativa analítica, ni deployment.

Canonización contractual: `H(tag, fields)` = SHA256 del UTF-8 de un array JSON compacto `[tag,...fields]`, orden fijo, strings exactos sin normalización Unicode, escape JSON estándar determinista; nada de floats binarios en identidades. Digests lowercase `sha256:<64hex>`. Los mapas de inputs se serializan como lista ordenada por nombre con `[name,type,value]`; enteros y decimales en string canónico, booleanos `true/false`, enum/string exactos; sin nombres duplicados, NaN, null implícito ni default omitido. Lista de dependencias ordenada por rol y nombre lógico, cada una SHA/size/plataforma; manifest vacío explícito si no hay dependencias. Canonización de strings: UTF-8 sin BOM; escapar sólo comilla, backslash y controles U+0000–001F (escapes cortos b/t/n/f/r donde aplican, resto u00xx lowercase); no escapar slash ni caracteres Unicode restantes. Objetos de schema tienen orden de campos fijado por la lista contractual; claves de maps se ordenan por bytes UTF-8. Enteros: 0 o signo menos opcional seguido de dígito1–9 y resto de dígitos; sin + ni ceros iniciales. Decimales: forma expandida sin exponente, sin ceros iniciales/finales fraccionarios, sin punto si entero, -0 normaliza a 0. Magic/size/ordinal rechazan signo negativo. Fixtures de normalización son parte del contrato compartido.

```text
StrategyVersionRef = H("echo-strategy-version.v1", [
  canonical_strategy_id, target_platform, executable_sha256,
  effective_inputs_sha256, runtime_context_sha256, dependencies_sha256
])
runtime_context = canonical instrument + timeframe + strategy execution mode
```

Magic input se materializa entre los inputs efectivos y debe coincidir con la allocation canónica. Artifact locator, FlowRun, Campaign, rank, timestamps, compiler label y baseline no entran al hash; los bytes o inputs que cambian sí. El compilador/build/source `.sqx`/MQ5/CFX/selected optimization y producer version se conservan como provenance del seal, no como identidades competidoras. Dependency manifest incluye DLL/indicadores/imports que afecten comportamiento; dependencia mutable desconocida impide seal. Execution mode aquí significa knobs propios del algoritmo (si no están ya en inputs), no account hedging/netting; no duplicar un mismo knob en dos hashes. Feed, cuenta, broker alias y terminal build se observan en binding, no convierten automáticamente el binario en otra versión.

| Cambio | Misma Strategy | Nueva StrategyVersion |
|---|---|---|
| EX5 bytes nuevos, incluso mismo source/compilador distinto | Sí si misma StrategyRef | **MUST**, sin presumir equivalencia semántica de compilaciones. |
| Inputs efectivos distintos | Sí | **MUST**, aunque el EX5 no cambie. |
| Nuevo resultado de optimización | Sí si derivación del mismo Ref | MUST si cambian inputs/bytes/contexto; **MUST NOT** si sólo cambia evidencia y el paquete es idéntico. |
| Nuevo CFX | Sí si no es nuevo Builder batch | MUST sólo por cambio resultante del paquete; MUST NOT por CFX de test/metadata solamente. |
| Misma lógica recompilada | Sí dentro de lineage | MUST si bytes distintos; MUST NOT si paquete idéntico. Compiler provenance distinta se añade en promoción/build evidence. |
| Metadata/label/descripción/rank/warnings | Sí | **MUST NOT**. |
| Nueva baseline/Expectation | Sí | **MUST NOT** por sí sola. Nuevo binding analítico de evidencia, no reescribir versión ni heredar selección ex ante. |
| Nuevo magic canónico | **Cambio prohibido por D** para la misma Strategy | No legitimarlo creando versión. Corregir allocation/mapping con evidencia; cualquier excepción exige owner y preservación histórica. |
| Override magic de Execution | Sí | MUST NOT: política aplicada, no cambio del ejecutable Reference. |
| Nuevo broker mapping/servidor/cuenta | Sí | MUST NOT si sólo routing/symbol alias. MUST si cambia input compilado/materializado o contexto lógico de estrategia. |
| MT4→MT5 | Sí sólo si Forge declara lineage al mismo Ref | MUST: plataforma y executable diferentes; no deducir continuidad desde nombre/magic. |
| Nueva generación Builder con lógica igual | **No** bajo D actual | Nueva Strategy; no dedupe por digest de lógica/bytes. |

**MAY** crear versión al comprobar que un cambio técnico afectó el paquete; no hay «MAY por gusto» para metadata: paquete idéntico debe converger a un Ref. Si efecto de CFX/dependencia es U, no se publica una versión pretendidamente equivalente: resolver los inputs primero.

**Elección I:** una tabla pequeña `echo.strategy_versions`, PK version_ref, FK canonical_strategy_id, manifest inmutable (inputs y dependency manifest o copia local garantizada), executable/config locators verificados. Justificada por FK de bindings/trades, queries versión→manifest y vida independiente de 0..N promociones. `strategy_definitions` sólo puede contener identidad/projection/current pointer; un JSON mutable de versiones allí no protege FK ni rollover. `PromotionRecord + immutable binding` podría funcionar con indirection a la primera promoción, pero acaba mezclando unicidad versión y operación/promoción; elegir dos tablas acotadas evita esa segunda autoridad. No version service, no tabla Forge obligatoria: Forge guarda seal write-once en artifact plane y lo referencia en handoff. Ninguna duplicación de métricas históricas.

Una nueva baseline/Expectation para versión idéntica se guarda como un vínculo analítico inmutable versionado (Ref + versión + selection/sealed_at + actor/reason), no UPDATE a una Promotion aceptada. V1 puede adjuntar el vínculo inicial al proof de enrollment; cambios posteriores son facts de control `BASELINE_BINDING.v1` en el mismo mecanismo raw con referencia al vínculo previo. Su productor es el operador/Echo de analytics autorizado, nunca ingestion por reenvío con key cambiada. No precisa catálogo/tabla Expectation nuevo ni puede declarar retroactivamente ex-ante un baseline sellado después de observar.

### Magic allocation y ciclos que se eliminan

**D exacto recuperado:** «pertenece a la Strategy; estable entre versiones y cuentas; asignado por registry Forge en promoción; nunca reutilizado». La sección F de la auditoría owner ubica asignación «tras Decision OPTIMIZER_SELECTION» y propone `YYMMCCQQQQ`; el catálogo CC sigue pregunta owner. No asumir que el ejemplo 10=XAUUSD es catálogo aprobado.

**I interpretación implementable de “promoción”:** reservar magic en Forge al preparar Apply/artefacto final, después de selección y **antes** de stamping/export/compile/backtest. Nunca esperar a `FINALIST_PROMOTION`, porque esa Decision necesita EX5/backtest ya ejecutado. Reintento usa allocation existente bajo UNIQUE StrategyRef/canonical y UNIQUE magic; no liberar por fracaso posterior. Echo recibe/verifica la asociación certificada por Forge en el manifest autenticado, no asigna magic. Reserve→Apply→compile→seal→structural promotion→handoff es acíclico. Si “promoción” owner significaba exclusivamente FINALIST_PROMOTION, ratificar esta precisión antes de implementar el asignador.

Signed int64 positivo es el mínimo E2E compatible con Go/PG y `POSITION_MAGIC` long; no impone int32. Wire nuevo usa **string decimal** para magic y broker IDs (incluye JS/Hasura/UI) y parseo con bounds exactos, sin Number/double. MT4 no admite un magic fuera de su rango; rechazar operación MT4, nunca truncar/modulo. El esquema semántico CC debe resolverse antes de allocation; no se sustituye silenciosamente por secuencia opaca.

### Rollover con posición abierta

| Momento | Autoridad y resultado |
|---|---|
| V1 abre | Collector verifica binding B1 y persiste `(origin_position_key, trade_id, canonical, V1, B1, initial risk, OPEN payload)` antes de emisión. Echo conserva mismo pin. |
| V2 se ingiere/se vuelve current | No altera B1 ni posiciones. `current_version` es catálogo y no autoriza attach/copy. |
| V2 empieza a observarse | Binding B2 nuevo con proof. V1/V2 pueden coexistir en cuentas distintas usando el mismo magic canónico. Series se separan por versión. |
| V1 sigue abierta | B1 puede quedar DRAINING (sin nuevos OPEN) pero sigue recibiendo MODIFY/CLOSE de posiciones ya atribuidas. No eliminar mapa por TTL. |
| V1 cierra después | CLOSE usa origin key→trade_id→pin V1/B1. Nunca magic→versión vigente. Execution cierre usa comandos/posición original de V1 y cuenta destino original. |
| Misma cuenta, mismo magic, dos EAs/versiones | **V1 mínimo lo prohíbe mientras existan posiciones u órdenes pendientes V1**: el EA de estrategia podría adoptar/gestionar posiciones por magic aunque el collector pudiera distinguir el OPEN por hora. Collector binding_id no evita interferencia económica. |
| Excepción futura same-account | Sólo con prueba de aislamiento del EA por position/instance y captura de esa instancia desde el productor económico. Un UUID añadido únicamente al collector no prueba cuál EA operó. Requiere TOP sólo si se pide esa capacidad. |
| Same-account tras drain | Inventario broker sin posiciones ni pendientes antiguas; barrier de captura, nuevo B2/readback, intervalo sin ambigüedad. Eventos tardíos conservan B1 por mapa durable. |
| Rollback a V1 | Reusar V1 bytes/inputs; nuevo B3 y proof, sin borrar B2. Cierres de V2 siguen V2; default usa cuenta distinta o espera drain. No bajar un contador ni editar manifests. |

## 4. Forge → Echo Ingestion V1

### Proceso y autoridad

S Gateway (`v3/gateway/internal/server.go`) ya posee HTTP de control y PG; Core procesa hechos/órdenes, lab-worker analytics. **I owner:** dominio Echo, endpoint en Gateway existente + repository transaccional `echo/v3/sdk/postgres`. No nuevo proceso. PostgreSQL obligatorio para endpoint; PG ausente = 503. Forge usa un cliente del SDK externo/protocolo versionado, no importa Echo core ni escribe DB Echo.

`POST /api/v1/forge/promotions` acepta **un miembro**. `GET /api/v1/forge/promotions/by-key/{key}` devuelve la aceptación durable con misma auth; lookup adicional por receipt ID es alias de lectura, no otro agregado. V1 síncrona y bounded por límites de manifest/artefacto y deadline configurados; sin batch/202/state machine de provisioning.

Auth V1 I: identidad de servicio Forge exclusiva con permiso `forge:ingest` y namespace registry configurado en Echo; TLS y credencial de servicio verificable en Gateway (token opaco rotatable es suficiente), permisos read del receipt por el mismo namespace. Namespace se obtiene de credencial/config, no de body no confiable. CORS/admin secret Hasura no son auth. Ref de artefacto sólo se resuelve en stores/buckets autorizados, nunca URL arbitraria del usuario. Rotar credencial no cambia namespace ni keys. UI/Hasura no puede crear/update/delete identidades, versiones o promociones aceptadas.

### Exact minimum request (I)

Request body es un **handoff manifest inmutable**, producido por una operación Forge de lectura exacta posterior a Promotion, conservada write-once. Se envía inline para no necesitar API de consulta de DB entre sistemas. El productor autenticado certifica pertenencia leyendo `Decision` por Ref en sus propios stores; el consumidor valida estructura/digests y binding, no pretende que un hash por sí solo autentique al productor.

```text
Headers:
  Authorization: service credential (never stored in receipt)
  Idempotency-Key: H("forge-echo-ingest.v1", [registry_namespace,
                    wave_key, canonical_strategy_id, strategy_version_ref])
Body:
  contract_version: "forge-echo-ingestion.v1"
  strategy:
    canonical_strategy_id, strategy_ref, identity_model_version: 2
    instrument, direction, timeframe
    magic_allocation: {magic_decimal, allocation_ref, assigned_at}
  version:
    version_ref, execution_manifest (defined in §3)
    executable_artifact, effective_inputs_artifact, dependency_artifacts[]
    build_lineage: {apply_evaluation_ref, compile_evaluation_ref,
                   selected_decision_ref, source_artifact}
  promotion:
    decision_ref, decision_content_digest, policy_id, policy_version,
    output_schema, flow_run_ref, wave_key
    member_proof: {strategy_ref, structural_evidence_refs,
                   tested_executable_sha256, tested_inputs_sha256,
                   requested_instrument, observed_instrument,
                   requested_timeframe, observed_timeframe}
    campaign_ref?: exact Campaign that owns this FlowRun
  evidence?: {baseline_manifest_ref, expectation_ref,
              trade_set_refs[], metric_set_refs[]}
```

`member_proof.strategy_ref` repeats only as a cross-boundary assertion from Decision membership; it MUST equal `strategy.strategy_ref`. No free-standing caller rank/score/warnings used as admission. `structural_evidence_refs` includes exact successful backtest artifact, parsed/normalized/reconcile evaluation and NativeMetricSetRef; these are distinct from optional analytics refs. The handoff compiler resolves transitive dependencies into this compact proof and fails if any ambiguity; it cannot choose “latest EX5”. Full Decision stays Forge-owned; receipt retains its content digest and attested selected member, not a new rival membership list. Re-audit can resolve original Decision via artifact access/export contract with retention. Authenticated export is a trust boundary, not a cryptographic proof against a malicious Forge producer.

All artifact descriptors: `{store_id,bucket,key,kind,schema?,size,sha256}`. Binary EX5 has kind/platform, no fake JSON schema. Inline execution manifest includes target platform/context/input digest/dependency digest; exact actual inputs bytes are verified before acceptance. `allocation_ref` is the canonical immutable registry allocation identifier exported by Forge (I deterministic `H("forge-magic-allocation.v1",[registry_namespace,canonical,magic_decimal])`); no second Echo allocator. `assigned_at` is audit only, never identity.

**Payload digest:** Echo computes `H("forge-echo-payload.v1",[canonical body])`; canonical body has fixed schema, rejects duplicate/unknown keys and normalizes supported decimal strings once. Persist the canonical accepted body and digest. Optional transport Content-Digest may be checked but is not normative input. No expired URLs/auth/session timestamps in body. Fields absent vs explicit null have one canonical representation (optional absent, null rejected).

| Candidate field | Classification | Rationale |
|---|---|---|
| contract_version | REQUIRED | Protocol dispatch, separate from Promotion/identity versions. |
| idempotency_key | REQUIRED header, DERIVABLE + verified | Preserves D wave/canonical/version tuple with namespace. Reject arbitrary key; do not substitute Campaign for wave. |
| payload_digest | DERIVABLE SAFELY; DO NOT SEND as business field | Server computes, response returns. Caller assertion alone is not verification. |
| canonical_strategy_id, StrategyRef, identity model | REQUIRED | String↔UUID association and global V2 scope must be asserted once by Forge. |
| StrategyVersionRef | REQUIRED, recomputed | Seal verifies exact semantics and consistency across promotions. |
| magic allocation | REQUIRED | Registry authority, not runtime inference. |
| PromotionDecisionRef/content digest/policy/output version | REQUIRED | Member authority and V1/V2 dispatch; Ref alone is not output content. |
| FlowRunRef + wave_key | REQUIRED | Decision subject + owner idempotency tuple. Wave is not safely parsed from canonical. |
| CampaignRef | OPTIONAL (required when Campaign-owned) | Verify exact flow ownership in exporter; no requirement for Generic flows. |
| executable/config/dependencies refs+hashes | REQUIRED | Exact operational/recovery package; no locator-only executable. |
| Separate EX5/config digest duplicate | DO NOT SEND | Descriptor/manifest already carries them; proof tested digest is a necessary equality assertion, not convenience metadata. |
| Structural NativeMetricSetRef/reconcile/backtest evidence | REQUIRED inside proof | V2 physical membership, distinct from analytical ranking. |
| Analytical TradeSet/MetricSet refs | OPTIONAL | Useful baseline, not gate for ingestion when not required by structural authority. Typed role and schema required when present. |
| ScoreRef/RankingSnapshotRef/rank/warnings | DERIVABLE from retained Promotion/evidence; DO NOT SEND standalone V1 | No second authority or rank=0 fiction. Read/display later through evidence contract. Warnings embedded in original authority stay intact. |
| baseline/Expectation refs | OPTIONAL | Ingestion can succeed without comparable baseline; enrollment Quality readiness remains separate. |
| Name/indicators/free description | OPTIONAL through later metadata edit; DO NOT SEND in minimal manifest | Real descriptor comes from canonical/instrument/direction/timeframe. UI name may equal canonical until enriched. |
| Echo strategy ID, status, eligibility, account, policy, capital, attach command | DO NOT SEND | Derived ID or another action boundary. |

### Version-aware membership validation

| Input | Exporter + Echo validation | Outcome |
|---|---|---|
| New V2 flow | Exact persisted completed FINALIST_PROMOTION; policy `finalist_promotion@2.0.0`, output `sqx-finalist-promotion-output.v2`, matching V2 result contract. Selected StrategyRef exists exactly once in structural membership. Exact structural refs and requested=observed instrument/timeframe; tested EX5/inputs match version. | Accept independent of numeric score/rank. `NOT_COMPARABLE`, PERIOD_MISMATCH/PNL_SIGN_FLIP do not remove membership. |
| V1 historical promotion | Match exact V1 policy/output and original immutable membership, never recalculate it. Allowed only tagged historical provenance on an existing historical flow proven by exporter. | May ingest if executable/identity requirements also satisfied; does not turn evidence into V2 or begin old forward. |
| V2 flow with V1 policy/output, mixed schemas, unknown version | Reject `UNSUPPORTED_AUTHORITY_VERSION` / `MEMBERSHIP_CONFLICT` | No downgrade fallback based on client assertion of “legacy”. |
| Member absent, structural mismatch or bytes from another finalist | Reject 422/409 deterministically | Rank/folders/score/latest cannot repair proof. |
| Zero members | No POST | No dummy receipt/strategy. Factory result stays its own authority. |

The implementation must read the flow's persisted producer/result version, not wall clock or request label, to establish legacy V1. C1/C2 retain authority of how structural membership is produced. This handoff adds a selected member→execution manifest assertion without changing membership criteria.

### Persistence, idempotency and errors

**I local transaction:** lock canonical identity; verify/create descriptor identity mapping; verify/insert version; insert `strategy_promotions` row with unique `(registry_namespace,idempotency_key)` and secondary unique `(registry_namespace,decision_ref,version_ref)`; return receipt only after commit. Protect immutable fields with DB constraints/permissions. Mutable descriptive name is separate. Ingestion neither advances `current_version` automatically nor publishes runtime config; optional pointer remains NULL until an explicit catalogue action. Receipt = projection of PromotionRecord, **no IngestionReceipt table**. ArtifactBinding = fields of version, **no separate table**.

| Persistent concept | Minimum store / why |
|---|---|
| Strategy descriptor + Forge mapping/magic | Extend `strategy_definitions` with nullable legacy-safe immutable registry/ref/magic/model fields and lifecycle marker; protect canonical writes/deletes. Needed to reject conflicting identity before facts. |
| StrategyVersion | Small immutable table §3; live FK and recovery independent of promotion frequency. |
| PromotionRecord/receipt | One immutable acceptance row per operation; request body/digest, verified artifact identities, source authority, accepted_at/actor namespace, fixed result ID. Needed for retries, audit and campaign queries. |
| Legacy alias mapping (sólo cuando hay evidencia) | I `strategy_identity_aliases`: alias exacto, role/source account/server/platform, intervalo, canonical target y proof. Tabla acotada justificada por lookup many-to-one y exclusión de intervals contradictorios entre Strategies; no backfill ni placeholder sin prueba. No contiene una segunda identidad canónica. |
| Artifact copies | Echo operational store exact bytes keyed by SHA; database version references. No new service, use configured existing blob storage or PG bytea for bounded executable/config if no durable blob store exists. Choice of physical store is deployment detail gated by restore proof. |

| Case | Exact deterministic behavior |
|---|---|
| Same key + same canonical payload | 200, same receipt ID/version/accepted_at/digest; no new row or effects. Lookup existing receipt before dependency/network verification so Forge outage does not defeat a completed retry. |
| Same key + different digest | 409 `IDEMPOTENCY_CONFLICT`, no accepted state change. Compare computed body, not supplied digest. |
| Same canonical promoted again | Same StrategyRef/magic/immutable attrs required. New wave/promotion can append record; mismatch = 409 identity conflict. |
| Same version, another Campaign | New wave/key/PromotionRecord; same version row and magic. No duplicate executable required. |
| Same Strategy, new version | New version_ref and key; immutable version row + receipt, no implicit rollover. |
| Same version, same wave but different Decision/evidence | 409 under frozen wave/canonical/version key. Do not append random suffix. If repeated deliberated promotions per same tuple become a real requirement, owner must amend key; not silently introduced now. |
| Same Decision/version with changed wave/key | Reject source binding conflict via secondary uniqueness; keys cannot bypass acceptance identity. |
| Timeout before commit | No successful receipt; safe GET then resend identical body/key. Any unreferenced verified copies are staging orphans, not acceptance. |
| Timeout after commit | GET returns exact committed receipt; retry returns same 200. |
| Concurrent duplicate POST | PG unique/transaction serializes winner; loser rereads committed row and compares digest. Identical = 200; different = 409. No “both accepted”. |
| Artifact failure before transaction | 422 for definitive hash/schema mismatch; 503 for transport/unavailable, 403 upstream access failure surfaced with stable code; no version/receipt commit. Never hold identity transaction during streaming download. |

201 first acceptance / 200 exact replay response: `{receipt_id,contract_version,canonical_strategy_id,strategy_version_ref,payload_digest,accepted_at,state:"INGESTED"}` plus Location for authorized lookup. No readiness/eligible/active true defaults. Errors `{code,retryable,field_or_ref?,receipt_id?}`: 400 malformed/key formula, 401 unauthenticated, 403 unauthorized, 409 identity/version/idempotency conflict, 413 configured size limit, 422 authority/artifact/schema contradiction, 429 throttled with Retry-After, 503 dependency unavailable. Unknown output version 422, no endless retry. Before acceptance missing artifact is 503 only when producer/storage readiness is transient; a sealed manifest referencing a definitively nonexistent artifact is 422. Operator corrects source by new legitimate authority, not editing accepted row.

### Artifact ownership and exact non-effects

Forge owns source SQX/MQ4/MQ5, CFX, build/optimizer evidence, Decision, HTM, TradeSets, MetricSets, scores/rankings. Echo **must** retain a verified operational copy of executable, all effective inputs, runtime dependencies and compact accepted manifest before marking INGESTED; can reference large research evidence only. No ticks/trade histories copied by ingestion. Copy source ref and SHA are separate from Echo locator/access grant. Verify content size/SHA by streaming, schema for typed documents, consistent platform/kind, member/tested bytes binding; store verified copies before DB commit, record only immutable identities. Partial copies never become accepted artifacts. Lost response/duplicate content converges on SHA. Temp/expiring URL is transport only; refresh it without changing identity/payload key.

Retention: no deletion of version/manifests/mapping/economic facts while any position, command, binding, promotion or retained audit references them. Forge evidence references must survive Temporal history/Campaign cleanup. Keep for lifetime of retained trading history; if retention contract cannot guarantee a referenced indispensable item, copy it or reject readiness. Inability to recover large optional baseline later means baseline U, never fabrication. Backup/restore includes Echo version bytes, facts and mappings, and exportable Forge proof; cross-DB SQL joins are forbidden.

Successful ingestion does **not** attach EA, provision Reference, enable copying, create Portfolio membership, allocate risk, activate strategy, declare eligibility or start canonical forward. It creates an inspectable accepted package. Broker account absent from minimal request is intentional. Expectation accepted as ref does not start observation.

## 5. Runtime binding / enrollment V1

**I one durable fact combines binding and enrollment**, not a generic deployments framework. `echo.reference_bindings` row has immutable identity/proof and separately controlled lifecycle transitions; it is not accounts/policies renamed. It answers what is physically attached; accounts/policies remain operational intent. No automatic attach required.

| Required field/fact | Producer / purpose |
|---|---|
| binding_id UUID + strategy_version_ref | Echo registers attach epoch; canonical/magic/artifact digests derive via immutable version/strategy. No repeated editable copies. |
| account_id + broker server/login/platform identity | Echo resolves actual broker account readback to catalogue; bare login alone insufficient across servers. `broker_id/platform` derive only from immutable binding snapshot, not today's mutable account row. |
| terminal installation identity + boot/session + chart/EA attach identity | Operator/terminal readback; PID alone not durable unique. binding_id is logical runtime instance; do not introduce another unused runtime ID. |
| actual executable/dependency hashes and effective inputs readback | Files loaded at attach, input serialization and chart context match version. Account report alone cannot prove EX5 hash. |
| collector identity/build/schema + observed registry map revision | Authenticated Bridge associates sender to registered account/collector and exact mapping; producer cannot claim another account. |
| proof payload/ref + actor + reason + recorded_at | Audit and recovery; manual is acceptable, marked MANUAL_VERIFIED. Account mode (hedging) and inventory of positions/pending orders included. |
| accepts_opens_from / accepts_opens_to; enrollment_started_at | Server-confirmed capture barrier/readback, half-open admission interval. End NULL until explicit stop. Existing position closes accepted after accepts_opens_to. |
| state PREPARED → OBSERVING → DRAINING → CLOSED, or SUSPENDED | PREPARED is not enrollment. SUSPENDED stops canonical coverage/new openings admission; it never erases existing facts. Explicit state transition actor/reason/time retained. |

Canonical `strategy_id`, magic, EX5/config refs need not be editable columns again: derive from immutable version FK, while **observed** values in proof are separate assertions checked for equality. Broker/platform/account snapshot must remain pinned even when catalogue changes. Broker login/account namespace association must be unique for enrolled account; collision/quarantined account cannot start observation.

**Start protocol, manual V1:** (1) accepted package and exact map available; (2) operator loads verified package, captures hash/input/account/server/terminal/chart readback and confirms no competing same-account same-magic manager; (3) collector startup registers map and reports broker connection, strategy running/enabled state, positions/pending inventory, durable local journal continuity and capture cursor; (4) Bridge/server acknowledges durable capture readiness and persists proof + enrollment. Start is max(proof recorded, confirmed capture barrier), **not** file copied, DB row inserted, earliest broker trade time or first eventual close. First trade not required: valid coverage can start with no trades. Existing positions discovered at startup are PRE_ENROLLMENT, retain OPEN provenance if available but do not become new forward entries.

A generic account collector cannot inspect arbitrary EA input state or infer it from magic. Minimum physical proof needs terminal chart/input readback under controlled attach plus exact file hashes and continuous EA liveness evidence (existing EA signal if present; otherwise a narrow strategy heartbeat/readback hook in export). Exported EA hook is I, absent S today. Do not claim reading file on disk proves in-memory loaded bytes after hot replacement; reattach under controlled barrier, attest loaded file and forbid replacement during binding. If no continuous EA health signal is available, coverage is U after last verifiable readback; terminal connectivity alone is insufficient.

### Canonical observation scope

**I:** at most **one canonical OPEN-admitting Reference enrollment per StrategyVersion globally** at a time. Multiple strategies per account are fine with distinct allocated magic. Parallel versions use separate series and, V1 default, separate accounts. Two accounts observing the same version: one explicitly canonical, second SHADOW/MIRROR; never sum their trades as independent strategy opportunities. This scope is a readiness choice needing owner ratification (§11), not inferred from existing account role metadata.

Switching canonical account for the same version is explicit: stop admitting old OPENs at cutover, reconcile inventory/cursor and prove other account is not inheriting the same open economic positions before new admission. Old enrollment DRAINING may close old canonical trades; this does not make a second OPEN stream. Quality windows retain enrollment provenance; do not blend two broker environments invisibly. Strategy-level summaries cannot sum V1+V2 as one strategy run without a separately declared analytical selection rule.

One authorized collector writer per physical account at a time, with durable collector epoch and local singleton/account association. Server rejects stale epoch as canonical writer. This is a capture ownership check, not physical trading fence. Replay of already committed events from an old epoch is allowed only as exact same event/digest; historical backlog recovery is explicitly authorized with closed cursor bounds and has no economic dispatch. Detect duplicates through broker position/deal identity even if malicious/duplicate collector minted a fresh UUID. Never rely only on UNIQUE trade_id. MT4 and MT5 cannot share a canonical enrollment; platform migration closes/adapts old binding and creates new version/binding, preserving old closes.

## 6. Reference authority V1

### What Reference is

**S:** `SendTradeIntent` calls `PositionSelectByTicket`, reads actual price/volume/SL/magic and creates UUIDv7; Bridge maps `reference_event`/legacy `trade_intent` into ReferenceEvent. **Truth:** operation/fill/position observed on the designated Reference broker account, with the actual Reference execution environment. **Not truth:** pre-broker strategy signal, all rejected/unsent strategy intentions, theoretical fill, or counterfactual profit.

Sufficient for intended Quality of **realized Reference behavior** vs a comparable, pinned baseline, and Fidelity of Echo Execution reproduction relative to that Reference plus applied command. It cannot answer “did the Reference broker reject an intended strategy order before any fill?” or “what was pure signal→Reference slippage?”. Those questions require producer-side intent telemetry; no requirement here proves that plane necessary. Do not add it or call Reference an ideal signal. An EX5 that produced no order due to its own logic and one whose request was rejected are not distinguished by fill facts; scope statements must preserve this limit.

### Trade and event identity

`trade_id` remains Reference-created UUIDv7 (D/S), reused by OPEN/MODIFY/all CLOSE parts and every Execution lineage. New canonical path adds a **source origin key, not reference_trade_id**: `(broker_server_id, account_registration_id, platform, broker_position_identifier)`; account registration is stable across reconnects, changes only on actual different account/reuse of login proven by Echo. MT5 position identifier is distinct from position ticket; preserve both, plus order/deal IDs as decimal strings. POSITION_IDENTIFIER joins DEAL_POSITION_ID and remains stable when ticket changes; netting reversals can retain identifier, hence V1 supports certified **hedging** only for canonical new path. [MetaQuotes position properties](https://www.mql5.com/en/docs/constants/tradingconstants/positionproperties).

Local durable mapping created before first publish contains origin key→trade_id→version/binding; central raw acceptance stores UNIQUE origin→trade association through a partial unique index on accepted logical OPEN rows; subsequent DEAL/MODIFY/CLOSE rows reference that OPEN. No second trade registry/table is needed. Collector replacement restores this map before observing old positions; loss of map does not authorize minting another UUID for the same origin. Duplicate origin/different UUID = quarantine conflicting observation, retain evidence and respond existing mapping; never route twice. Same trade_id/different origin = identity conflict. Existing account_id is linked to broker/server identity during enrollment; caller cannot assign namespaces freely.

Each immutable observation has `source_event_id`: stable producer-assigned UUID persisted with its payload, reused on transport retries. Broker **deal facts** additionally unique by `(physical account,deal_id)`; OPEN position aggregate and entry deals are linked records, not additive profits. A material MODIFY without stable broker revision uses collector monotonic sequence persisted per position under the single writer; snapshot-only recovery cannot invent missing intermediate modifications. Late explicit correction is a new fact referencing superseded event with reason, never UPDATE raw economics. Kafka coordinates diagnose transport duplicates, not economic identity.

### Minimum immutable raw capture

Reuse `echo.raw_trade_events` (migration029), adding fields/indexes and payload protection for the new protocol; it already stores logical JSON, hash, Kafka coordinates, processing status. New capture stores original message bytes **at the first Echo Bridge boundary** plus versioned normalized envelope; invalid JSON is quarantined raw with transport identity. This avoids silently losing number precision/fields before validation. PG payload/economic columns immutable, processing status/error may change. Journal remains derived operational projection and existing Lab path remains untouched.

| Raw fact | Minimum non-reconstructible content | Null/missing and integrity |
|---|---|---|
| Every event | source_event_id, schema/producer build, collector epoch, origin position key, trade_id, role/source kind, binding_id/version, broker account association, event kind and producer sequence; source raw clock + clock basis; observed_at, first Bridge received_at, DB recorded_at; raw payload/hash | Version+binding required for canonical new write. Legacy/U observations retained but not treated as version-proven. Topic/partition/offset when available; Bridge persistence may precede Kafka. |
| OPEN | actual symbol + canonical symbol/mapping revision, side, volume, actual fill entry price/time; order/position/deal identifiers, initial SL/TP presence and values, initial risk basis/pip units/MM type/currency; entry commission/fees when known; chart context | All effective inputs derive from immutable version; broker specs/pip size at OPEN pinned if used for R. Absent SL differs from zero or unknown. First observed SL is not necessarily initial SL; only entry evidence/continuous capture can certify initial risk. |
| MODIFY | changed SL/TP/volume state and source reason if available, prior observation link, exact sequence/time or observed interval | Required for risk/exit changes and management attribution. A size change from deals keeps those deals; do not synthesize fills from current volume difference. No price-tick stream required. |
| Entry/exit deal (partial included) | immutable deal/order/position IDs, IN/OUT kind, actual volume/price, broker time, commission/swap/fee/profit components and currency, broker reason if supplied | Keep every deal once. Entry costs cannot be recovered from final exit commission. Positive/negative costs preserve source sign, missing ≠ 0. |
| Final CLOSE | original trade/version/binding pin; closing deal refs, remaining volume=0 proof from reconciled broker inventory/history, actual last economic close time | Final trade totals derive from complete deal set, never “last deal overwrites”. CLOSE arriving before OPEN stays durable unresolved; no invented OPEN/current version. |

SL/risk: preserve broker initial SL and pre-offset intent separately where available. For Reference only observed initial SL is fact; do not copy Execution policy into it. `initial_risk_pips` usable only with basis and formula version; current canonical Lab R remains `profit_pips/risk_pips`, **not** money-risk ratio. Realized money/cost calculations can be derived from complete raw deals and currency. Missing original SL remains U for R even if later current SL exists. No MAE/MFE/tick archive required by this seam.

Raw durable acceptance is before economic routing eligibility. **I process choice:** Bridge preserva bytes originales y first received_at en el envelope nuevo, entrega a Kafka y sólo confirma transporte al EA después del ACK durable del producer; el EA conserva su outbox/mapping hasta confirmación adecuada, no sólo write al pipe. Bridge no tiene PG en el handler S actual. Core, que ya posee PG, añade aceptación raw al boundary de TradeJournalFn o una función interna adyacente en el mismo proceso: nuevo topic/protocol ingresa únicamente a esa función, valida/persiste raw y después hace fanout a planner y proyección de journal. Cambiar el wiring StateFun del nuevo protocolo es obligatorio: los dos consumidores paralelos legacy no prueban raw-before-route. No agregar DB credentials a cada Bridge ni un servicio nuevo.

Core no confirma consumo mientras el commit raw o la entrega del fanout recuperable esté incompleta; transientes retornan error. El raw row conserva estado de publicación pendiente y un dispatcher acotado en Core reanuda pendientes con la misma accepted_event_id. Si hubo commit y se perdió ACK, una redelivery encuentra la misma fila/digest y reanuda; el planner usa su routing key durable para no duplicar órdenes. No XA PG/Kafka: la recuperación explícita cierra esa ventana. Kafka conserva raw envelope hasta aceptación, PG pasa a autoridad durable independiente de su retención. Bytes inválidos/identity conflicts quedan en cuarentena con identidad de transporte, sin fanout económico; raw facts válidos pueden replayarse sólo a journal/analytics sin dispatch. `recorded_at` es commit/captura PG, no Bridge arrival. El defecto actual de journal ACK sigue siendo una dependencia de implementación separada, sin fix aquí.

### Time authority

**S discrepancy:** `EchoCommon.mqh::NowUnixMillis` uses TimeCurrent then TimeLocal; Reference CLOSE payload uses `timestamp_ms` emitted now and does not carry an authoritative `closed_at_ms`. Labels “Unix ms” alone do not certify UTC. TimeCurrent is last server quote time; TimeGMT uses local machine timing/DST calculation. [MetaQuotes TimeCurrent](https://www.mql5.com/en/docs/dateandtime/timecurrent), [TimeGMT](https://www.mql5.com/en/docs/dateandtime/timegmt).

| Clock / cutoff | Meaning and authority V1 I |
|---|---|
| broker/server raw time | Economic timestamp as broker reports it, plus raw basis/precision/server identity. Preserve unchanged; conversion to UTC requires verified offset rule for that event, including DST. |
| EA time / observed_at | When collector detected the fact, clock_id/boot/sequence and precision recorded. Not economic fill time. EA emission retries do not replace first observation. |
| event_at_utc | Normalized actual broker event time only when basis verified. Store converter version and offset evidence; otherwise NULL/time_quality=UNKNOWN. Never infer timezone from a late network receive delta. |
| received_at | First trusted Echo Bridge receipt, UTC server clock; duplicate does not advance it. Useful transport freshness, not market duration. |
| recorded_at | DB first durable capture timestamp; receipt response only after commit. Immutable knowledge boundary; if consumer inserts hours later, do not claim original Kafka publish was DB recording. |
| processed_at | Processing attempt/result time, mutable operational metadata; not event or enrollment time. |
| analytics as_of | Completed publication knowledge cutoff + input capture cursor/recording set. Include only committed facts visible at that run; late corrections create another publication, not rewrite previous knowledge. |
| Trade duration | Last economic exit minus first economic entry with verified broker/UTC basis; raw server duration only if offset continuity proved. Unknown conversion across DST → duration U, not received-close minus recorded-open. |
| Forward cutoff | Enrollment starts only at verified capture barrier; evaluate events after admission start with identity and coverage. Selection/baseline sealed_at must precede admitted observation for ex-ante claims. Arrival later can be included in later as_of without moving start earlier. |
| Window membership | New versioned analytics path declares event-time window `[from,to)` and as_of cutoff; pending/late facts are visible as incompleteness. Existing Lab recorded timeline remains unchanged. |
| Freshness / coverage | Server receive/record age plus producer cursor/health and broker clock quality. Event-time lag alone may mean market closed; receipt freshness alone may hide stopped EA. |
| Replay | Same event ID/content/economic timestamps/first received and recorded facts. Replay processing clocks new; never route again solely because a fact was replayed. |

### Observation coverage, minimum without monitoring framework

Same raw store accepts `REFERENCE_COVERAGE.v1` interval reports from collector/Bridge. Required: binding/collector epoch, sequence and cursor bounds, interval `[from,to)`, terminal broker connection, strategy EA running/enabled proof, auto-trading permissions, symbol session state, local journal backlog/continuity, last source event sequence, last raw-accepted cursor, server received/recorded timestamps. Existing account heartbeat may supply account connectivity, but not EA health or pipeline completeness. One configured heartbeat interval/freshness tolerance per protocol, persisted with enrollment; certification supplies values, no undocumented heuristic.

| State | Minimum positive evidence | Permitted inference |
|---|---|---|
| VALID NO SIGNAL | Healthy/enabled EA + connected terminal + open relevant market/session + collector continuous + pipeline cursors reconciled over interval | Zero **observed Reference operations**, not proof no rejected/pre-broker signal. Counts only fully covered interval. |
| MARKET CLOSED | Verified symbol/broker session schedule/status and collector heartbeat | Scheduled closure, not EA failure. Do not infer solely from stale quote on weekend. |
| STRATEGY DISABLED | Explicit EA/terminal permission/strategy enable state with time | Exclude interval from active strategy exposure; no decay conclusion. |
| REFERENCE TERMINAL DISCONNECTED | Fresh collector heartbeat explicitly reports broker disconnected | Terminal alive, broker observation unavailable. |
| EA/COLLECTOR DOWN | Independent Bridge/terminal process readback proves EA absent or collector exited | If only heartbeat vanished, cause U, not DOWN proven. |
| PIPELINE FAILURE | Producer sequence/outbox advances or backlog accumulates while durable server cursor does not, with healthy sender/readback | Coverage incomplete until reconciliation; no zero-trade claim. |
| UNKNOWN | Missing/stale/contradictory proof or unverified runtime configuration | No activity denominator. Preserve observed trades but mark interval incomplete. |

Coverage is a vector with a derived display state; do not erase simultaneous market closed+terminal down by selecting a comforting label. Fully missing heartbeat stops certified coverage at the last positively covered interval, not at an invented later threshold. Recovery may append evidence closing a gap only if durable local events/cursors and continuous EA state survived; observed trades alone cannot reconstruct “healthy and no signal” time.

## 7. Expected routing / applied policy authority V1

### Source and scope

S `execution_planner.go` reads mutable kache policies, emits telemetry routing count, skips restricted accounts; `mm_engine.go` sizes with snapshots, creates fresh command UUID, applies magic override/offsets and samples delay. `v_trade_execution_delta` is an INNER JOIN of observed Reference/Execution; cannot identify missing vs unrequested. Existing policy version exists but rows are mutable, so `(account,strategy,version)` without immutable history is not a reproducible snapshot.

**I routing owner:** Core planner owns candidate/exclusion result; MM owns sizing decision and command. Persist with existing Echo PG, not new service/Decision framework. Two bounded stores: `trade_routing` for immutable routing snapshot + per-recipient results, and `economic_commands` for emitted economic intents and recoverable delivery/outcomes. Snapshot inputs are embedded for V1, because current config rows are mutable; replace by refs later only if referenced revisions are truly retained immutable.

### Exact routing authority

Routing key = `(reference source_event_id, operation kind)`; OPEN has one event/operation. Snapshot records trade_id/version/binding, accepted raw event ref, decision_at/recorded_at, planner schema/build, catalogue/config revision **and the exact considered universe**, then one result per account. Scope V1 universe = all accounts with a policy/assignment for that Strategy in the resolved snapshot, including disabled/expired ones. Other accounts are NOT_REQUESTED/NO_ASSIGNMENT under that retained snapshot, not missing Execution. Empty universe is a durable EMPTY_ROUTING result. A cache without a known complete synchronized revision cannot prove empty/unassigned: result INCOMPLETE_CONFIG, no opens.

| Recipient result | Meaning / authority |
|---|---|
| EXCLUDED(reason, relevant input snapshot) | No economic command was expected: no assignment, disabled/whitelist, expired policy, version not enabled for copy, insufficient data/specs, risk/MM rejection or unsupported account mode. Preserve reason and gate inputs. |
| PENDING_DECISION | Candidate reached MM but final allowed/blocked decision not durable yet. Not excluded and not a missing broker execution denominator yet; unresolved decision is operationally visible. |
| EXPECTED(command_id, operation, payload_digest) | Economic intent accepted and durably created after policy/sizing checks; eligible to dispatch. Later transport/broker failures do not remove it from expected set. |
| SUPERSEDED_BY_EXPLICIT_CANCEL | Optional subsequent action, with actor/reason/command lineage; original expected fact preserved, not erased from audit. |

Core transaction commits final recipient EXPECTED and command row together. Routing candidate snapshot is inserted once before fanout; each recipient can move once from PENDING to an immutable final EXCLUDED/EXPECTED result under CAS; the completed routing seal is valid only after all candidates final. Redelivery never re-evaluates finalized decisions against current config. MM transient crash leaves PENDING retriable, deterministic policy block becomes EXCLUDED. A replay of an old raw event for analytics does not create a new routing snapshot or imply authorization for a late economic command.

Version-specific copy gate is REQUIRED: existing `(account,strategy)` policy must not automatically copy newly ingested/newly observed V2. Route configuration needs explicit allowed version/binding revision for new opens (nullable means legacy-only, not all future versions). This is an additive binding field on existing policy/assignment, not Portfolio design. S `close_handler.go` ya consulta ExecutionLookupResp y genera cierres de ejecuciones abiertas; se conserva esa dirección de lineage. I CLOSE/MODIFY destinations derive from original open commands/positions, not current strategy policies; a removed recipient may still require its V1 close. Uncertain original OPEN remains in reconciliation scope, not presumed absent.

### Applied policy snapshot: snapshot vs reference

| Input/result | Persist at decision/command time |
|---|---|
| policy identity | `(account_id,canonical_strategy_id)`, source revision/version, content digest, valid_until and schema; nullable policy UUID only if one exists. No invented mandatory policy ID. |
| sizing | risk type, configured amount/currency or fixed lot, calculated risk basis and output volume, rounding rule/version, selected volume after min/max/step. |
| SL/TP | Reference observed levels, initial risk basis, pre-offset intended levels, configured offsets/pip units, final physical requested SL/TP. Retain both; later current rows cannot reconstruct. |
| destination | account, broker server/platform, canonical and actual broker symbol, symbol mapping revision/content, actual runtime magic override if any. Canonical Strategy magic remains separate. |
| delay | configured min/max **and sampled delay**, not redraw on retry; created_at, not_before and open TTL/expiry basis. |
| decision reason | allowed or exact blocked code, gate/code version and relevant input values. Expected persists even when broker later rejects. |
| account state | revision + actual values used: enable/whitelist and sizing inputs (equity/balance/currency/free margin only when consumed), snapshot timestamp/freshness. Do not copy unused full account data. |
| instrument specs / quote | consumed contract/tick/pip sizes and values, currency conversion rates, lot bounds/step, quote price/time and mapping. Omit unused attributes; timestamp alone cannot identify historical spec. |
| PortfolioVersion | nullable immutable ref if an upstream authority supplies one; absent now. Do not fabricate portfolio or allocation from policy. |

A snapshot proves **what was applied**, not correctness of risk budget or broker acceptance. Safety state may change after decision: dispatch recheck can block and records delivery BLOCKED_AFTER_DECISION; do not overwrite the snapshot or pretend not expected. New authorized calculation after such change is a new command operation with explicit reason/sequence, never accidental retry.

### Command lineage and recovery

`economic_commands`: command_id UUIDv7 PK; unique `(routing_key,recipient_account_id,operation,operation_sequence)`; trade_id, StrategyVersionRef, raw event/binding, routing result, immutable policy/sizing snapshot, exact payload and hash, optional PortfolioVersion; mutable dispatch/outcome metadata separately protected. Persist one UUID on insert before sending. Same key/content returns same command; changed intent under key conflicts. Durable row is a bounded outbox: existing Core publisher retries only unsent/known-safe dispatch with same command ID; at-least-once transport never proves exactly-once broker execution.

Bridge/EA propagate IDs unchanged; EA preserves pending intent before broker effect and records order/deal/position IDs after. Unknown broker outcome requires reconciliation by stored command/position/order evidence before another order, not blind resend with new UUID. Implementing this existing known recovery defect is separate from this TOP. Command→deal can be 1:N; Execution trade_id remains original Reference trade_id, and Execution OPEN pins originating Reference V1 even if its own broker magic differs. Execution close actor may be manual/broker; record actual actor/reason and lineage, do not relabel it as a routed reference command.

## 8. Cross-contract invariants (18)

1. New canonical Strategy identity is Forge's adopted GeneratedStrategy; neither magic, content hash, current host nor semantic similarity may recreate it.
2. StrategyRef↔canonical V2 and Strategy↔allocated magic are immutable; no registry namespace rotation to evade uniqueness or recycle numbers.
3. StrategyVersion fixes executable/input/dependency semantics; metadata, baseline and promotions cannot mutate or relabel it.
4. Magic is allocated before stamping/compile; version is sealed after exact bytes/config are known; Finalist membership precedes handoff ingestion. No circular allocation/promotion/version dependency.
5. V2 membership is read from FINALIST_PROMOTION structural authority; rank/top_n/score/folders/latest are never fallback membership.
6. Same ingestion key cannot accept different canonical content; identical concurrent/retried ingestion resolves to the same receipt.
7. Accepted ingestion commits identity/version/promotion atomically and has zero provisioning, copy, eligibility or capital effects.
8. No canonical Reference enrollment starts without account/runtime/inputs/readback and capture barrier proof; DB presence and elapsed time are insufficient.
9. One canonical OPEN-admitting Reference stream per StrategyVersion; shadow/parallel accounts and versions are never silently summed.
10. OPEN pins version/binding and original risk facts; CLOSE/MODIFY/replay never follow current_version or current mapping.
11. Same-account same-magic version overlap is forbidden V1 until physical position-management isolation is proven; attribution labels alone cannot prove isolation.
12. One physical origin position maps to one trade_id; duplicate collectors cannot create extra canonical trades or commands by minting new UUIDs.
13. Raw immutable facts survive rejected parsing, late arrival and processing failure; replay updates processing metadata, not economic/knowledge timestamps.
14. Partial fills/costs retain broker IDs and signed components; last exit is not a substitute for all entry/exit deals or initial risk.
15. Unknown coverage cannot imply zero trades/valid no signal; broker time without verified basis cannot be silently called UTC.
16. A mutable policy/config row is not historical authority; applied inputs, sampled delay and exact command are sealed before dispatch.
17. Missing execution is defined against retained EXPECTED recipients; PENDING decisions, EXCLUDED and absent assignment are distinguishable, including zero-recipient trades.
18. CLOSE/MODIFY routing follows existing economic lineage, not today's memberships/policies; uncertain broker outcomes require reconciliation before retrying economic effects.

## 9. BWC / migration matrix

| Existing surface | Additive/new-write treatment | Forbidden / certification |
|---|---|---|
| historical `magic_*`, including repeated/ambiguous aliases | Nullable alias facts scoped by source account/broker/platform/interval and proof, pointing to canonical only when unambiguous; retain raw old string | No global text substitution, no magic-only join. Prior P records same execution magic across strategies. Ambiguous alias = U. |
| identity V0/V1 Forge | Read exact original records/ref; no automatic adoption/backfill. New exports require proven V2 association or explicit legacy adaptation manifest | Do not reinterpret partial uniqueness of old rows as global. |
| magic int32→int64 | PG policy override bigint, MQL5 long, all pipe/JSON SDK DTO/client code and UI decimal strings; new protocol version/capability negotiation | Test >2^31, >2^53 and signed max; no narrowing/float conversion. MT4 incompatible value rejects only that binding. |
| EA binary TradeMapRecord | Versioned header/record length/checksum; decoder of exact old layout → atomic new file with backup, validate count/IDs/tickets before switching | Appending fields changes FileReadStruct record stride; comment saying append is BWC is false. Never reinterpret or truncate old file. Unsupported layout requires operator recovery, no clear/recreate. |
| Canonical ID length | Extend new canonical field path and all downstream DB/FK/views/DTO/EA storage to variable-length exact IDs, preferably text/length-delimited UTF-8 with an explicit protocol size bound | Campaign naming includes UUID and may exceed varchar(64)/uchar[64]. No shortening/hash alias in canonical strategy_id. Test >64 end-to-end; no freeze on illustrative max until full surface scan. |
| ticket/position/deal IDs | V2 decimal string DTO, int64/ulong-safe parsing, preserve POSITION_IDENTIFIER separately from changing ticket | Current ReferenceTicket int32 is another narrowing point. Same ticket in another account/server is not same origin. |
| `strategy_definitions` | Retain old rows/labels; add nullable Forge mapping/protected identity fields. New Gateway insert creates real immutable-linked descriptor | No journal autoprovision placeholder for new canonical namespace; legacy behavior retained only for old producer protocol. Protect cascade delete of accepted identities. |
| Existing journal rows | Leave economics/times/IDs; nullable version/binding additions only for exact new facts; sidecar alias/provenance may enrich read model | No version backfilled from current_version, magic or oldest available EX5. Existing recorded Lab semantics preserved. |
| Positions open before versions exist | Preserve known trade_id/origin; `attribution_status=LEGACY_UNVERIFIED`; reconcile closures through original mapping | Do not assign newly ingested version merely because same magic. Such positions block same-account version rollover until drain; no forced close. |
| FinalistPromotion V1 | Exact historical policy/output dispatch; immutable membership; explicit legacy tag proven by source version | No regenerate from latest ranking, no converting V1 Decision to V2 or fabricating missing version artifact. |
| Promotion V2 | New-flow version-aware structural proof; nullable rank/score | Mixed V1/V2 contracts reject; requires C1/C2 source implementation, not assumed present today. |
| Current MT4 Reference cohort | Continue legacy capture separately; retain EX4/old identity and clocks. Canonical version proof only via explicit adapter and physical evidence | No retrospective performance evaluation, no global MT4 migration, no magic int64 forced through MQL4. Old cohort does not certify MT5. |
| Future MT5 Reference | New protocol with version/binding, exact magic/IDs, hedging/account readback, coverage and deal facts | Broker/platform metadata alone cannot certify physical EA. Cert with >64 ID, >int32 magic/ticket and open-position rollover across accounts. |
| Mutable policies and current command DTO | Add snapshots and version opt-in for new path; legacy producers keep marked legacy semantics | No historical policy recompute as fact, no auto-copy of newly ingested V2 via Strategy-wide policy. |
| raw_trade_events migration029 | Extend with original bytes/identity/binding clocks and economic duplicate keys; preserve existing historical logical-JSON contract | Existing created_at/received_at meanings not redefined for old rows. New schema says exactly where first reception occurs. |

## 10. Source surface map and implementability ledger

Paths below are verified repository-relative locators; proposed files/tables explicitly labelled **I**. Migration numbers intentionally not assigned before NORMAL starts. Source read is `echo@e25165ba` and `symphony@db8a022`; previous remote Echo equivalence is dated evidence, not fresh object inspection.

| Contract | Actual repository/module/path/symbol / current schema | Likely additive delta / API / client / SDK |
|---|---|---|
| F-ID GeneratedStrategy | Symphony `sqx/core/domain/canonical_strategy_id.go`; `persistence_identity.go`; `adapters/registry-postgres/adopt_strategy.go::upsertStrategyV2`, `strategy_identity.go::LoadStrategyIdentity`; migrations005/006; `sqx.strategies` | No redesign canonicalizer/adoption. Handoff uses LoadStrategyIdentity. Existing `version` attribute remains origin token. |
| F-GEN Campaign scope | Symphony `sqx/core/domain/forge_campaign.go::NewBuilderSupplyBatchRef`; `activities/worker/steps/steps.go` ResultsGroup; `adapters/registry-postgres/forge_campaign.go`, migration013 | Read exact batch/wave association, no new generation authority. |
| F-MAG allocation/stamping | Symphony `sqx/adapters/apply-selected-run/binding/contract.go::EffectiveConfig`, `activities/worker/durable_apply_selected_run.go`, `durable_apply_selected_run_physical.go`; exporter-plugin `src/SQ/CustomAnalysis/EchoForgeRobustRunExporter.java` | I registry migration/adapter `strategy_magic`, service allocation transaction, bind typed MagicNumber from registry. Exporter hook only as needed for readback/health. |
| F-VER version seal | Symphony `sqx/core/domain/artifact_paths.go`, artifact contracts; `adapters/storage-minio/durable_artifacts.go::VerifyArtifactStream/ProbeDurableArtifact`, Apply and MT5 compile/reconcile evidence | I execution-manifest seal producer after compile; immutable artifact; no Forge table required. Export exact effective inputs, not ApplicationConfig alone. |
| F-PROM membership | Symphony `sqx/core/domain/decision.go`; `activities/worker/rank_snapshot_activity.go::buildFinalistPromotionDecision/promotionFinalists`; `core/forge/result.go::crossCheckPromotion`; `adapters/registry-postgres/decision_store.go`; migrations004/009/010 | C1/C2 own V2 implementation; I handoff exporter/CLI/service adapter reads decisions and structural refs. No changes to membership criterion in boundary slice. |
| F-EVID operational bytes | Symphony `sqx/activities/worker/mt5_reconcile_activity.go`, `adapters/mt5/binding/reretester_baseline.go`; Mongo `evidence_store.go`; MinIO durable artifacts | I narrow manifest export + authenticated artifact read access. No Echo SQL into PG/Mongo. Retention agreement and verified copy, no download-all baseline. |
| E-ING API | Echo `v3/gateway/internal/server.go::NewServer`, existing pgClient repository composition; `v3/sdk/postgres/client.go`; baseline001 `strategy_definitions` | I authenticated promotion handler, transaction repo, migration strategy mapping/versions/promotions. No route currently. GET receipt, no Kafka/economic effect from POST. |
| Shared boundary SDK | External `xKoRx/sdk` used by Symphony; Echo local `v3/sdk/domain` is separate module | I versioned JSON schemas/fixtures + narrow Go DTO/client in external SDK; Echo validates same contract without dependency on Forge core. Do not silently make Echo SDK the shared external SDK. |
| E-CONFIG runtime map | Echo `v3/sdk/domain/client_config.go::ClientConfig`, `execution_policy.go`; gateway config/webhook handlers; Bridge config delivery | I binding/map revision and capabilities, allow-version on copy policy; no use of ReferenceStrategyID magic=0 fallback as global map. |
| E-BIND enrollment | Echo baseline001 `accounts`, `account_strategy_risk_policy`; no observed immutable binding table | I `reference_bindings` + protected transitions/proof in existing Gateway. Manual attach verification surface + narrow EA health/readback; new table is observation fact, not provisioning framework. |
| E-REF collect | Echo `v3/clients/mt5/reference_v3.mq5::GetEffectiveStrategyID/SendTradeIntent/SendTradeClose/SyncCurrentOrders`; `EchoPersistence.mqh::TradeMapRecord/WriteAll/CleanupOld`; `EchoCommon.mqh::NowUnixMillis` | I versioned variable-length persistence, initial risk pin, origin/position/deal identity, actual close clock, recovery/coverage. Legacy MT4 separate adapter, not forced upgrade. |
| E-RAW accept | Echo `v3/bridge/internal/reference_pipe_handler.go`; `v3/core/internal/functions/trade_journal.go`; `v3/core/deploy/flink-statefun/production/module.yaml`; `v3/sdk/domain/reference_event.go`; migration029 `raw_trade_events` | I Bridge raw envelope + Kafka ACK, Core raw commit/fanout recuperable; bytes/dedupe/version columns; StateFun module.yaml nuevo ingress único; pipe/schema/capability versionadas. |
| E-JOURNAL project | Echo `v3/core/internal/functions/trade_journal.go`; `v3/sdk/postgres/trade_journal_repository.go::ensureJournalParentRows`, `trade_journal_open.go`, `trade_journal_close.go`; migrations043/045/057/060 | I additive pinned fields and validation for new protocol; independent ACK/recovery bug fix required before cert, not performed here. |
| E-TIME/analytics | Echo `v3/lab-worker/internal/builders/recompute.go`, `repo/canonical_repo.go`, migration046 `lab_*`; SDK lab riskpolicy | I new version-aware reader/path with explicit event/recorded/as_of semantics; no alteration of historical Lab by this contract. |
| E-ROUTE | Echo `v3/core/internal/functions/execution_planner.go::doProcessReferenceEvent`, account restriction validation; policy cache/domain | I PG routing snapshot/candidate and final recipient authority before emission. Complete config revision and empty-routing result. |
| E-POLICY/COMMAND | Echo `v3/core/internal/functions/mm_engine.go`; `v3/sdk/mm/fixed_risk.go`; `domain/reference_event.go::NewCoreCommand`; `execution_policy.go`; `postgres/execution_policies_repository.go` | I `economic_commands` migration/repo with applied snapshot and unique operation key; original UUID persisted once; no new risk/portfolio engine. |
| E-EFFECT recovery | Echo `v3/core/internal/functions/close_handler.go::emitCloseCommands` y `v3/sdk/domain/trade_close.go`; Bridge command/result path; `v3/clients/mt5/execution_agent_v3.mq5` ExecuteOrder and journal; `v3/sdk/domain` command/result DTOs | I IDs/version/snapshots survive pipe/pending/restart; effect uncertainty certification. Existing command dedupe alone not broker exactly-once. |
| E-FID future denominator | Echo migration043 `v_trade_execution_delta` | Keep existing view; future read uses routing/commands and raw executions. No full Fidelity analytics built. |
| E-ALIAS scoped legacy | Echo `v3/sdk/postgres/migrations/001_schema_baseline.up.sql` strategy definitions/journal, aún sin alias authority | I `strategy_identity_aliases` y lectura scoped; columnas account/server/platform/role/interval/proof, FK canonical; no rewrite de journal ni alias global por magic. |
| E-WIDE ID propagation | Echo baseline001/043/046 and dependent views/Hasura; MQL persistence `[64]`; SDK `ReferenceTicket int32` | I coordinated additive length/type migration and capability negotiation; inspect every cast/column/client in slice before choosing wire max. No canonical shortening. |

### Cross-contract challenge register: EVIDENCE → IMPACT → ALTERNATIVE → RECOMMENDATION

| Challenge | Evidence → impact | Alternative → recommendation / classification |
|---|---|---|
| CH1 B1/B2 state drift | Current commits185825c/ef65dd1/db8a022 and project checkpoint vs Resources at a10c26c → obsolete NEXT EXACT | Retain dated snapshots, add current delta. **S correction**, no design reopening. |
| CH2 Temporal authority | sqx pin1.35 + workspace selected1.44.1 → single “runtime pin” assertion insufficient | Separate declared/resolved/deployed, as above. **S erratum**; deployed SDK U. |
| CH3 Strategy=semantic logic | GeneratedStrategy D newer explicitly batch-scoped → cross-generation dedupe would violate identity V2 | Keep adopted Ref lineage; semantic families DEFER. **D precedence**, no new family framework. |
| CH4 Version before stamping | Companion proposed content-bound version “before stamped/selected”; bytes only exist after compile → circular/impossible digest authority | Allocation before Apply, seal after compile/config, membership then handoff. **I correction of prior I**, ready to freeze. |
| CH5 Ingestion before mt5_exporter | Old NI-EI insertion point precedes EX5 and Finalist evidence → cannot validate exact V2 finalist/bytes | New ingestion after structural Promotion; old insertion point superseded for this contract. **I against historical plan**, no change to actual pipeline today. |
| CH6 accounts/policies sufficient binding | Current mutable tables omit version/hash/terminal/readback/interval; old owner wording says storage already correct/no deployments table → cannot prove trade runtime | One observation fact table `reference_bindings`, keep intent in accounts/policies. **NEEDS OWNER ratification** of correction; do not implement a deployments framework. |
| CH7 magic across versions vs execution override | Owner canonical magic stable; current policy allows different Execution magic, prior P same override across strategies → global observed magic uniqueness false | Forge canonical magic unchanged; Execution runtime override is command-local lineage, never strategy resolver. **I clarification for owner**; if owner forbids overrides globally, disable for new path explicitly rather than pretend source lacks them. |
| CH8 canonical varchar64 | Campaign published basename includes UUID/generation and semantic tokens; source Echo varchar64 + EA64 → legal Forge IDs need not fit | Widen full new path, preserve canonical exact. **I necessary adapter**, not new identity; no truncation/rehash. |
| CH9 one version per magic+time | V1 position survives rollover; same-magic EA managers may adopt each other's positions → interval attribution alone insufficient | Pin OPEN and use separate accounts until old positions/pending drain, unless physical isolation proven. **I bounded restriction** needing owner scope approval. |
| CH10 raw clock/cost authority | Current CLOSE now emission, last-deal economics and entry cost omission; trade duration/initial risk not reconstructible from current row | New raw deal/time/initial-risk producer path, preserve old rows/semantics. **S gap / I additive contract**, no historical evaluation. |

## 11. Ready to freeze / owner questions / physical gates

| Classification | Contract / precise unresolved point | Impact / safe default |
|---|---|---|
| READY TO FREEZE (I, not yet D) | §§2–4 immutable version seal, Gateway individual ingestion, deterministic key/transaction/receipt, artifacts/non-effects; §§6–8 raw/event/time/command invariants | Contract definitions complete enough for bounded NORMAL after owner accepts recommendations. |
| NEEDS OWNER DECISION O1 | Ratify `reference_bindings` as minimum observed fact despite old “accounts/policies already sufficient” wording; choose proposed **one canonical enrollment per version** with separate accounts for overlap | Without acceptance, no canonical new enrollment claim; ingestion design still usable. |
| NEEDS OWNER DECISION O2 | Confirm scope of magic rule: Forge canonical stable and Execution overrides remain explicitly command-local; resolve CC catalogue for `YYMMCCQQQQ` and clarify allocation-before-Apply meaning of promotion | No allocator implementation until exact semantic catalogue is approved. Do not replace semantic code scheme by preference. |
| NEEDS OWNER DECISION O3 | Ratify conservative same-account rollover restriction while old positions/pending orders exist; different-account V1/V2 parallel is recommended | Prevents EA management ambiguity; no forced position close. Advanced same-account coexistence deferred. |
| NEEDS ANOTHER TOP | **None for recommended bounded path** after O1–O3. Only if owner demands same-account concurrent versions/netting/pre-broker signal plane or incompatible magic allocation semantics | These are scope expansions, not mandatory new discovery to implement this document. |
| NEEDS PHYSICAL EVIDENCE P1 | Running Echo core/collector build/config, server account identity/mode; exact EX5 load+inputs/dependency readback | This session SSH failed; previous deployed core P kept dated. Must pass before OBSERVING. |
| NEEDS PHYSICAL EVIDENCE P2 | Certified EA health, restart/mapper restore, V1 delayed CLOSE after V2 on another account, duplicate collector and lost ACK | Contracts are I; no physical proof invented. |
| NEEDS PHYSICAL EVIDENCE P3 | Broker timestamps/offset basis, complete entry/exit deal fees, partial close, pending orders/hedging behavior | Unknown time/risk/coverage stays U, not zero. |
| NEEDS PHYSICAL EVIDENCE P4 | V2 nonempty structural member with exact tested executable+effective inputs; artifact retention/restore and service auth | C1/C2 source and factory physical gates precede real V2 ingestion certificate; deterministic fixtures can certify transaction protocol first. |
| DEFER | Historical backfill/recovery analysis, quality/performance/ranking, Portfolio design/optimization, advanced routing analytics, generic provisioning/event sourcing, multiasset/tenant abstraction | No changes or evaluation in this mission. Known journal/security/effect defects implemented only in their own authorized slices. |

## 12. Implementation slices and NEXT EXACT

File budget categories are scope controls, not effort estimates. Every slice is proposal I; no implementation authorization follows from TOP closure. NORMAL certification requires critical-path tests first and applicable repository coverage rules; physical effects remain separately gated. Future slice start reads then-current source/AGENTS, does not reuse today's hashes as a guaranteed baseline.

| Name | Contract / repo | Budget | Dependencies | Certification required |
|---|---|---|---|---|
| `ECHO-FORGE-LIVE-IDENTITY-WIRE-V1-NORMAL` | Shared exact manifest/decimal/ID canonicalization + schema fixtures; external SDK + adapters Echo/Symphony | normal; split consumers if repo/file budget exceeded | Owner ratification of this contract; no physical runner | Golden hashes across implementations, malformed/duplicate fields, >64 canonical, int64 bounds, wrong member/bytes, no float loss. |
| `FORGE-MAGIC-ALLOCATION-AND-VERSION-SEAL-V1-NORMAL` | Registry allocation, typed stamping inputs, immutable executable version manifest; Symphony | split: allocation/stamping then seal/export | O2, wire; existing Apply/compile/evidence | Concurrent allocation, never recycle, retry stable, changed params/bytes new version, same package cross-Campaign same Ref; no magic allocation after compiled package. |
| `FORGE-FINALIST-HANDOFF-EXPORT-V1-NORMAL` | Exact Decision→member→tested package manifest and authenticated thin client; Symphony + external SDK | normal | C1/C2 for new V2, version seal | V1 read intact; V2 NOT_COMPARABLE admitted, structural mismatch rejected, no latest/folder query, empty no POST. |
| `ECHO-INGESTION-TRANSACTION-V1-NORMAL` | Gateway endpoint/auth, descriptor/versions/promotions persistence, operational artifact copy; Echo | split: persistence then handler/artifact access | wire, seal fixtures; O1 not required for ingestion | All §4 concurrency/timeout cases, identity conflicts, same version repeated, copy failure no DB acceptance, no activation/copy writes. |
| `ECHO-LIVE-IDENTITY-BWC-V1-NORMAL` | Wide canonical/64-bit wire + variable-length EA persistence + migration adapters; Echo | split: DB/SDK then Bridge/EA/client | wire, reviewed old binary layouts | Backup/atomic conversion/restart, old map preservation, >int32 magic/ticket, >2^53 wire, >64 canonical, unsupported old layout fail-closed. |
| `ECHO-REFERENCE-BINDING-ENROLLMENT-V1-NORMAL` | One observed fact, account proof, map/capability and coverage start barrier; Echo, narrow Forge exporter health hook only if needed | medium; split if hook crosses budget | O1/O3, ingestion, BWC | Manual exact readback, duplicate collector, no trading/observation on DB-only state, shadow vs canonical, no same-account overlap. |
| `ECHO-REFERENCE-RAW-AUTHORITY-V1-NORMAL` | OPEN pin, deals/MODIFY/CLOSE clocks/costs, durable raw acceptance and coverage; Echo | split: producer+recovery, then raw ingress/projector | BWC/binding, known journal ACK fix in own scope | Offline/restart/partial fills/late CLOSE/cost completeness, initial-risk unknown handling, duplicate origin, outage coverage U; replay cannot dispatch. |
| `ECHO-EXPECTED-ROUTING-AND-POLICY-FACTS-V1-NORMAL` | Candidate universe, final expected/excluded, applied snapshot + command uniqueness/outbox; Echo | split: planner snapshot then MM/command persistence | Accepted raw identity, version opt-in, existing effect recovery fix separately | Empty config vs unknown, exclusions vs expected, MM crash PENDING, policy mutation/retry same command, sampled delay fixed, CLOSE uses V1 recipients. |
| `ECHO-BOUNDARY-LIVE-AUTHORITY-CERTIFICATION-V1-NORMAL` | Cross-system readback/restore and evidence-only acceptance certificate | normal, evidence-led | Above + real V2 supply when available; owner authorization for any later physical workload | One complete future chain, raw preservation/lookup by trade_id, separate-account rollover V1 CLOSE after V2, retries/restore, no implicit portfolio/risk/eligibility. |

**NEXT EXACT boundary:** owner ratification of O1–O3 against this concrete contract, then `ECHO-FORGE-LIVE-IDENTITY-WIRE-V1-NORMAL`; no new broad product audit. CC catalogue must be fixed before magic allocator slice. **NEXT EXACT factory remains C1** at current checkpoint; this Resource does not steal/change that track. No schedule or delivery estimate.

## Evidencia y provenance

Read and reconciled all five requested Resources: master architecture, Independent Reality Check, Echo source, Forge source and independent evidence; scoped owner audit alignment of 24-08, GeneratedStrategy cutover, BuilderSupplyBatch correction, Finalist V2, MT5 V2/V3, current project checkpoint and both Astra feedback notes. Source citations are the actual locations in §10; prior physical counts were not re-queried or evaluated. Only git/read-only source/module resolution and official MetaQuotes docs were used; no source edits, tests/builds, migrations, deployments, DB/MinIO/ETCD/Kafka/Temporal writes or trading actions.

D references: [[Echo - Auditoria POC e Identidad Forge-Echo 2026-08-23]]; [[2026-08-23-durable-strategy-identity-v2-cutover]]; [[2026-09-04-echo-forge-campaign-builder-supply-identity]]; [[2026-09-06-echo-forge-finalist-model-v2]]; [[2026-09-06-echo-forge-mt5-execution-model-v2]]; [[2026-09-06-echo-forge-mt5-global-physical-ownership-v2]]; [[2026-09-06-echo-forge-mt5-fencing-and-cancellation-v3]]. Current source/implementation checkpoint: [[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]. Context: [[Echo + Echo Forge — Arquitectura de producto, gaps y roadmap de cierre 2026]] and [[Echo + Echo Forge — Independent Reality Check and Time-to-Value Plan]].

This Resource is the single contract authority proposal for this seam. No acceptance of a new D is implied, no historical truth rewritten, no production state certified. Open owner questions and physical gates are bounded and explicit. Session close/feedback/change log link to this document instead of copying its contracts.

## Límites y contradicciones

Las propuestas I requieren ratificación en los puntos O1–O3; los hechos S no certifican deploy. El source Echo remoto se reconfirmó por hash, pero el objeto remoto y runtime vivo no fueron releídos por falta de acceso. El contrato de versión/input readback y coverage describe el productor que falta, no una capacidad física ya existente. No hubo evaluación de resultados ni mutaciones fuera del vault.

Cierre documental verificado 2026-09-07: [[2026-09-06-forge-ingestion-runtime-live-authority-v1]] registra disposición I; [[2026-09-06-echo-forge-live-authority-contract]] conserva cambios/validación; [[2026-09-06-codex-gpt-6-astra-high-echo-live-authority]] y [[2026-09-06-echo-live-authority-session-feedback]] registran ejecución y feedback. PASS/CLOSED del TOP; O1–O3 permanecen pendientes de ratificación.

Revisión independiente 2026-09-07: [[Echo + Echo Forge — Architecture Durability and Contract Review — Fable 5.1]] confirma §§2–8 como contrato a congelar con correcciones acotadas (C-1…C-7), reclasifica O1/O3 como default técnico y O2 como catálogo CC owner, y no identifica TOP adicional. Este documento no se reescribe; la disposición vigente vive allí.
