---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo — Producto Integrado]]"
  - "[[F — Decision Register]]"
  - "[[A — Runtime Authority and Journal]]"
  - "[[C — History Curves Rankings]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-22"
updated: "2026-10-22"
---

# B — Forge Ingestion Readiness

## Propósito

Cerrar el contrato Echo-owned `strategy-ingestion.v2`, su traducción desde Forge y la habilitación operacional verificable sobre el único baseline runtime autorizado. Este documento especifica implementación para Shot 2; no certifica una integración ni autoriza activación de estrategias de la campaña actual. `INGEST_ACCEPTED` prueba aceptación durable de identidad/historia; `ECHO_OPERATIONAL_READY` exige otra prueba y nunca depende de que LAB termine sus curvas.

## Contenido

### 1. Autoridad y evidencia actual

Rigen [[F — Decision Register]] D09/D10/D11/D16–D24 y [[Echo + Echo Forge — Environment Contract]]. El diseño V4 y [[1 — TECHNICAL_FREEZE_PACKET]] aportan requisitos compatibles, no código disponible. D24 excluye merge, adapters y migración desde backtester legacy. Esta investigación fue local y de lectura: Echo `feature/ef-runtime-pools@2ee61791deb3139be23e1c9be3708b1d41da8d6b`; Symphony `master@daded14cbe0bc85f6fafda8d079e94036f715b47`; ambos HEAD coincidían con los SHAs autorizados y `git status --porcelain` no mostró delta. No builds, suites, infraestructura ni campañas ejecutadas.

Toda referencia `E:path:line` de esta nota corresponde a `xKoRx/echo@2ee61791deb3139be23e1c9be3708b1d41da8d6b`; `S:path:line` corresponde a `xKoRx/symphony@daded14cbe0bc85f6fafda8d079e94036f715b47`. Son referencias de código, no rutas del vault.

| Observado en el corte | Evidencia | Consecuencia para Shot 2 |
|---|---|---|
| Gateway monta promociones V1; el handler declara cero efectos de runtime | `E:v3/gateway/internal/server.go:171`; `E:v3/gateway/internal/forge_ingest_handler.go:28` | No llamar operacional al receipt actual; montar V2 como aplicación universal separada |
| Aceptación V1 escribe mapping/version/promoción en una transacción | `E:v3/sdk/postgres/ingestion_service.go:209`, `:244`, `:302` | Reutilizar invariantes, no confundir esas filas con `strategy_definitions`/routing |
| Mapping V2 es inmutable y namespace-scoped, pero exige magic positivo | `E:v3/sdk/postgres/strategy_identity_repository.go:34`, `:58`, `:96`, `:178` | Mantener magics existentes; hacer opcional la asignación para registro nativo/analítico, sin inventar magic |
| Store de versiones vigente admite sólo MT4/MT5; aún no tiene recetas nativa/analítica | `E:v3/sdk/postgres/strategy_version_repository.go:18`, `:60`, `:76` | Implementar extensión de recetas ya aceptada; su presencia en otro branch no vale como integración |
| GET V1 por receipt consulta sólo UUID, sin namespace en WHERE | `E:v3/sdk/postgres/promotion_record_repository.go:170` | V2 siempre filtra namespace y writer; UUID opaco no es autorización |
| Política se enriquece desde `strategy_definitions`, carga vigencia y publica Kafka sin prueba aplicada | `E:v3/sdk/postgres/execution_policies_repository.go:44`; `E:v3/gateway/internal/execution_policy_handler.go:91` | Provisionar definición/política real y añadir ACK del consumidor sobre revisión/digest |
| `strategy_config` guarda políticas en StateFun; `WaitReady` del cache sólo alcanza highwatermark | `E:v3/core/internal/functions/strategy_config.go:147`; `E:v3/core/internal/config_cache.go:92` | Ninguno prueba que este binding/version/account esté aplicado |
| `ClientConfig` ya transporta referencia master y versión prospectiva de feed | `E:v3/sdk/domain/client_config.go:112` | Preservar campos existentes; config recibida no equivale a config aplicada |
| Forge usa sólo V1/promotions y no provisiona Echo | `S:sqx/adapters/echo-handoff/http_ingress.go:21`, `:57`, `:106` | Nuevo productor V2 usa SDK Echo; no escribir PG Echo ni introducir formatos Forge en Echo |
| Forge ya dispone de identidad exacta, versión write-once y manifest durable | `S:sqx/adapters/registry-postgres/strategy_identity.go:13`; `S:sqx/adapters/registry-postgres/strategy_version.go:20`, `:123`; `S:sqx/core/forge/handoff_producer.go:65` | Traducir desde refs selladas; carpeta, nombre o `latest` no resuelven identidad |
| Delivery Forge sólo tiene `INGESTED`/conflictos/unavailable/unknown | `S:sqx/adapters/registry-postgres/migrations/015_strategy_magic_version_seal_handoff.up.sql:52`; `S:sqx/adapters/echo-handoff/http_ingress.go:266` | Guardar acceptance y readiness V2 separados; no promover `INGESTED` a READY |

### 2. Frontera universal y nombres

Echo es dueño de `StrategyIngestionV2`, `HistoryInputV2`, `OperationInputV2`, validadores, canonicalización y recibos en `v3/sdk/contracts`; sus servicios Gateway son dueños de registro/provisión. Forge convierte datos SQX/MT5 dentro de Symphony y consume ese SDK. LAB sólo recibe cambios de heads canónicos y calcula derivados. No existe HTTP ni escritura directa Forge→LAB o Forge→PG Echo.

No modificar semántica V1 ni usarla como fallback ante fallo V2. Se conserva su contrato para consumidores existentes mientras la nueva integración usa exclusivamente V2. El recibo V2 vive separado de `promotion_records`: los productores nativos/analíticos no deben fabricar una promoción Forge. Una promoción real puede aparecer en `provenance.inputs`, sin ser un requisito universal.

Tipos básicos compartidos: `Ref` = UTF-8 opaco de 1–256 bytes sin controles; `SemanticKey` = 1–128 bytes; `CanonicalStrategyID` = 1–1024 bytes; `UUID` = representación lowercase validada; `Digest` = `sha256:` más 64 hex lowercase; `Timestamp` = RFC3339Nano con offset explícito, normalizado UTC a microsegundos; `Decimal` = string decimal exacto, sin exponentes, NaN ni infinitos, hasta 38 dígitos y escala 18, normalizado sin ceros redundantes. IDs son opacos y sensibles a mayúsculas; no extraer semántica de nombres. Campos numéricos de dinero/precio/cantidad son Decimal, nunca JSON float. Timestamps desconocidos usan el tipo de evidencia de C; no se rellenan desde `accepted_at` o `sealed_at`.

Decodificación estricta: objeto raíz único; sin trailing JSON, claves duplicadas o campos desconocidos; arrays sin IDs duplicados; UTF-8 validado explícitamente. Error identifica JSON pointer y código, nunca devuelve secretos ni el body completo.

### 3. DTO de registro e identidad

`StrategyIngestionV2` es este envelope cerrado; los nombres son contrato de wire:

| Campo | Tipo / presencia | Validación y semántica |
|---|---|---|
| `schema_version` | string requerido | Literal `strategy-ingestion.v2` |
| `producer_ref` | SemanticKey requerido | Igual al writer autorizado; no elige namespace |
| `external_strategy_ref` | Ref requerido | Identidad estable del productor; no nombre de archivo |
| `strategy` | StrategyRegistrationV2 requerido | Crear o verificar mapping; no sustituir otra identidad |
| `version_definition` | VersionDefinitionV2 requerido | Definición sellada o referencia explícita existente |
| `histories` | `HistoryInputV2[]` requerido, 1–8 | Contrato económico exacto en documento C; POST sólo creación/replay |
| `requested_curve_profiles` | `CurveProfileRequestV2[]`, opcional | Ausente solicita los cuatro perfiles ratificados con configuración default versionada; presente 1–4 IDs únicos registrados; error 422 ante ID/config desconocida |
| `operational_request` | OperationalRequestV2, opcional | Ausente equivale a `REGISTER_ONLY`; jamás activa por omisión |
| `provenance` | `{inputs: NamedRef[]}` requerido | 1–64 refs exactas con role/ref/schema_version/content_digest; campaña/decisión pueden ser inputs genéricos, no DTO Forge |

`StrategyRegistrationV2 = {canonical_strategy_id: CanonicalStrategyID, strategy_ref: UUID|null, display_name: string, instrument_ids: SemanticKey[], direction: LONG|SHORT|BOTH, timeframe: SemanticKey|null, magic_allocation: MagicAllocation|null}`. `display_name` 1–256 bytes, instrumentos 1–64 únicos canónicos resueltos por Echo; timeframe nulo se conserva si la definición no lo tiene. Si el productor conoce la UUID canónica sellada de Forge la entrega; Echo verifica mapping 1:1 `(auth_namespace,canonical_strategy_id,strategy_ref)`. Si no la conoce, Echo asigna UUID una vez, la devuelve y protege `UNIQUE(namespace,producer_writer,external_strategy_ref)`; replay jamás genera otra UUID. Otra referencia externa hacia identidad existente requiere mismo mapping íntegro, nunca crea un alias automático.

`MagicAllocation = {magic_decimal: string, allocation_ref: Digest, assigned_at: Timestamp}` mantiene 1..9223372036854775807 y unicidad `(namespace,magic)` vigente. Es nulo para recetas nativa/analítica y cuando no existe asignación demostrable; no reservar magic nuevo en Echo para un productor Forge. Un master externo sin mapping probado puede registrarse analíticamente pero queda `BLOCKED_IDENTITY_MAPPING` para operación. Un magic permite localizar el mapping dentro del scope exacto de cuenta/servidor/plataforma/rol/binding; nunca fija por sí solo una versión.

`VersionDefinitionV2` es unión exclusiva: `{existing_ref: Digest}` o `{identity_recipe, target_platform, declared_version_ref: Digest|null, construction_at: TimeEvidence, construction_data_cutoff: TimeEvidence, available_at: TimeEvidence, package: ...}`. La referencia existente debe pertenecer a la misma identidad/namespace, y las versiones nuevas deben incluir su evidencia temporal aunque sea explícitamente desconocida. El paquete no contiene curvas, ranking, run_mode ni history digest como identidad de estrategia.

| Receta | Package y ref que Echo recomputa |
|---|---|
| `sqx-v1` | `{executable_sha256,effective_inputs_sha256,runtime_context_sha256,dependencies_sha256,execution_manifest,executable_artifact,effective_inputs_artifact,dependency_artifacts}`; primeros cuatro Digest, manifest Ref, artefactos `ArtifactRef` del SDK. Ref existente `wire.HashTagged("echo-strategy-version.v1",canonical_id,platform,exec,inputs,context,deps)` intacto. Tokens `MT4`, `MT5`, `MetaTrader4`, `MetaTrader5` preservan grafía dentro del hash |
| `native-v1` | Mismo significado natural de cuatro digests, plataforma `ECHO_NATIVE`, `execution_manifest` con capacidad `NATIVE_RUNTIME`; ref con misma receta `echo-strategy-version.v1`. El build/descriptor identifica una implementación nativa admitida, no código arbitrario aportado por Forge |
| `definition-v1` | Plataforma `ANALYTIC`; `{strategy_definition_sha256:Digest,definition_manifest:object}` con capacidad `ANALYTIC`; campos ejecutables SQL NULL. Ref `wire.HashTagged("echo-strategy-definition.v1",canonical_id,"ANALYTIC",definition_sha)`. Digest de definición calculado por `wire.Digest("echo-strategy-definition-content.v1",definition_manifest)` |

`ArtifactRef` usa store_id/ref/digest/size según SDK actual, store en allowlist; no se aceptan URLs arbitrarias ni paths absolutos. Artefacto ejecutable requerido por receta ejecutable debe existir/verificar digest/size antes de commit. `definition_manifest` máximo 256 KiB. Para I1 el transporte de historia es inline: no activar variant artefacto/multipart sin contrato de commit y medición que la necesite. Paquetes de identidad existentes no se rehashean ni se normalizan retrospectivamente. Mismo ref con paquete sellado distinto = 409 `VERSION_SEALED_CONFLICT`; receta no admitida = 422, no degradación a analítica silenciosa.

`CurveProfileRequestV2 = {profile_id: string, config: object}` con IDs `recorded_money.v1`, `r_net_cumulative.v1`, `normalized_10k_open_balance.v1`, `normalized_10k_initial_balance.v1`; configuración conforme al descriptor versionado de C. Sin config explícita se aplican defaults del descriptor y se devuelve el config_digest resultante; riesgos virtuales no modifican políticas operacionales.

### 4. Histories, revisiones y atomicidad

La definición canónica de `HistoryInputV2` y `OperationInputV2`, sus números económicos, revisiones y selección vive en el documento C de este paquete. El envelope B no los adapta ni introduce otro formato. Encabezado mínimo integrado: `history_id`, `source_kind`, `source_instance_ref`, `account_ref`/ausencia explícita, `run_mode`, `run_ref`/ausencia explícita, `role`, `mm_context_digest`, `expected_revision`, `expected_digest`, cuatro evidencias temporales, `coverage`, `provenance`, `operations`, `retractions`. Identidad = `(auth_namespace,strategy_version_ref,producer_writer,history_id)`, con source/account/run/role/MM sellados por historia. Datos de Echo/journal sólo aceptan writer interno Echo, aunque la credencial Forge pertenezca al mismo namespace.

POST acepta únicamente historias nuevas (`expected_revision=0`, `expected_digest=null`) o una historia previamente registrada con contenido idéntico. Contenido diferente bajo el mismo history ID = 409 `HISTORY_EXISTS`; se corrige por PUT completo con CAS. PUT requiere `expected_revision` y `expected_digest` coincidentes con `If-Match`; ausencia de precondición = 428, desacuerdo header/body = 400 y head distinto = 412. Cada cambio efectivo inserta snapshot inmutable N+1, conserva N y mueve head con invalidación/cola en la misma transacción. Sin cambios devuelve 200 `UNCHANGED`; no aumenta revisión. Replay del receipt precede al CAS, por lo que un retry de una escritura aceptada sigue convergiendo aunque el head haya avanzado después.

Orden de aceptación: autenticar y fijar scope → limitar/parsear/validar envelope completo → recomputar request_digest → buscar receipt por scope/key → copiar/verificar input exacto append-only → transacción con locks ordenados por identidad/history → verificar mapping+version → insertar snapshot/revisión y heads → registrar `strategy_definitions` mínimo y vínculo de registry → insertar receipt, cabeceras/jobs LAB y petición/outbox de provisión → commit. Un error de cualquier historia revierte todas; ningún efecto Kafka/control de trading ocurre antes de commit. Artefactos staging huérfanos son permitidos y no referenciados; no hay GC concurrente I1. No mantener lock SQL durante cálculo de curvas ni esperar respuestas de consumidores.

`strategy_definitions.id` continúa siendo la clave que consumen políticas/journal. Si `(canonical_strategy_id)` existente coincide inequívocamente se preserva; para nuevo registry entry se fija una vez `runtime_strategy_id = "sv2:" + strategy_ref` y se devuelve, con `UNIQUE(namespace,runtime_strategy_id)` y crosswalk explícito. Se inserta la definición con symbol principal sólo si la estrategia declara uno; multiinstrumento usa instrumento por evento y relación normalizada version↔instrument; no elegir un símbolo por conveniencia. Una definición legacy ya ligada a otra UUID/versión no se sobrescribe: 409 `RUNTIME_IDENTITY_CONFLICT`. La tabla de definición enriquece/relaciona; la autoridad de versión sigue siendo el registry sellado.

### 5. HTTP, autorización y límites fijados

| Método y ruta | Contrato |
|---|---|
| `POST /api/v2/strategy-ingestions` | `202` primera aceptación; `Location` receipt. `200` replay/unchanged; el resultado de aceptación original es estable y el estado operacional consultado puede haber avanzado |
| `GET /api/v2/strategy-ingestions/{receipt_id}` | Receipt del namespace+writer autenticados; `200`, `404` si ausente o ajeno |
| `GET /api/v2/strategy-ingestions/by-key/{key}` | Recuperación autoritativa scope+key; `200`/`404`; no crear efectos |
| `PUT /api/v2/strategy-versions/{version_ref}/histories/{history_id}` | Snapshot completo del writer autorizado, CAS + Idempotency-Key, `202` cambio o `200` unchanged/replay |
| `GET /api/v2/strategy-versions/{version_ref}/histories/{history_id}` | Metadata/head/coverage y enlaces a lectura paginada; respeta writer/roles de lectura |
| `POST /api/v2/strategy-versions/{version_ref}/operational-bindings` | Operador config o producer con grant explícito de profile; body `OperationalRequestV2`, Idempotency-Key y `expected_binding_revision`; permite crear/reconciliar el perfil autorizado sin reimportar historia |
| `GET /api/v2/operational-bindings/{binding_ref}/readiness` | Snapshot operacional separado con desired/applied checkpoints, motivos, scope y valid_until |

Todas las rutas de mutación usan Bearer opaco dedicado, resuelto por ETCD al startup, comparación constant-time, TLS fuera del harness loopback; credenciales distintas para producer-ingest/config-operator/runtime-ack/front-read. Mapeo server-side `credential → namespace, producer_writer, allowed_profiles, allowed_version_recipes, permissions`. No confiar namespace/writer del body. Permiso `strategy:ingest` no concede cuentas, policies, activación LIVE ni escritura de historias Echo. `operational:provision:<profile_ref>` sólo habilita el profile autorizado. Front/Hasura leen views filtradas; mutations de negocio pasan por estos servicios. Falta de config/auth es 503 fail-closed; token ausente/inválido 401, actor válido sin grant 403. GET de objeto ajeno devuelve 404 para no filtrar existencia.

Límites I1: request descomprimido 134.217.728 bytes (128 MiB), 8 historias, 250.000 operaciones/historia, 1.000.000 movements/historia; sin truncado ni división de historia por símbolo. No aceptar `Content-Encoding` distinto de identity en esta versión (415). Streaming a staging privado del servicio mediante `MaxBytesReader`; validación por historia sin retener simultáneamente todas; staging máximo 2 GiB/proceso, cleanup al finalizar, abortar sin commit si se agota. Una admisión bulk por proceso y una por namespace, sin cola HTTP; exceso 429 + Retry-After 2s. Hasta 4 provisiones pequeñas y 2 publicaciones outbox concurrentes por proceso, una por binding; SQL pool reservado al tráfico operacional existente. Deadline bulk 120s, lock timeout SQL 5s, GET 5s y provisión 15s; todos parametrizados ETCD con esos defaults. El HTTP cliente Forge usa 130s para bulk y 5s GET; `202` se obtiene después del commit completo, no al recibir bytes.

Meta de implementación a medir: readiness de profile aislado sin dependencia faltante ≤45s desde commit, antes del master simulado en t+60s; no es garantía actual ni gate para cortar/hacer caber artificialmente un histórico. Registrar por separado tiempo upload, validate, commit, provision y ACK. Si se excede, readiness sigue pendiente/degradada con causa visible y la observación se conserva.

| HTTP | code / retry |
|---|---|
| 400 | `INVALID_WIRE`, `INVALID_INPUT`, `HEADER_BODY_MISMATCH`; corregir input |
| 401/403 | `UNAUTHENTICATED` / `FORBIDDEN`; no retry ciego |
| 404 | `NOT_FOUND`; en recuperación consultar y reintentar sólo mismo key/body; no prueba ausencia de request aún en vuelo |
| 409 | `IDEMPOTENCY_CONFLICT`, `IDENTITY_CONFLICT`, `VERSION_SEALED_CONFLICT`, `HISTORY_EXISTS`, `RUNTIME_IDENTITY_CONFLICT`, `BINDING_CONFLICT`; requiere corregir conflicto, no cambiar key para eludirlo |
| 412/428 | `PRECONDITION_FAILED` / `PRECONDITION_REQUIRED`; refrescar head para una nueva intención; replay conocido se resuelve primero |
| 413/415 | `PAYLOAD_TOO_LARGE` / `UNSUPPORTED_MEDIA_TYPE`; cero truncado y cero aceptación parcial |
| 422 | `UNSUPPORTED_RECIPE`, `UNSUPPORTED_PROFILE`, `DIGEST_MISMATCH`, `NON_CANONICAL_INSTRUMENT`, `INVALID_ECONOMICS`; input inválido no se degrada a datos suficientes |
| 429 | `CAPACITY_EXCEEDED`, retryable true, Retry-After; mismo body/key |
| 503/504 | `UNAVAILABLE` / `DEADLINE_EXCEEDED`, retryable true; outcome puede ser incierto tras commit, GET-by-key antes de repetir |

Error envelope `{code:string,retryable:boolean,field_or_ref:string|null,request_id:UUID}`. Ingest válido con falta de presupuesto Q_i no es 422 automáticamente: aceptación válida y perfil R/10k `INSUFFICIENT_DATA` según C. Dependencia operacional faltante después de aceptación no transforma la ingesta durable en fallo HTTP: se refleja en readiness.

### 6. Receipt, idempotencia y concurrencia

`Idempotency-Key` requerido: 1–128 bytes `[A-Za-z0-9._:-]`; productor recomienda UUID y persiste key+body exactos antes de enviar. Scope durable `(namespace,producer_writer,method,logical_resource,key)`, con unique física; GET-by-key de la colección usa ese scope de creación. Request digest = `wire.Digest("echo-strategy-ingestion.v2", normalized_envelope)` utilizando la canonicalización SDK; orden por IDs para conjuntos histories/operations/movements/profiles/inputs, orden de arrays semánticos preservado; no incluir headers ni timestamps asignados por servidor. El productor utiliza el mismo encoder/validador y verifica digest retornado. `wire.HashTagged` actual hashea un array JSON compacto, no concatenaciones ad hoc (`E:v3/sdk/contracts/wire/hash.go:10`).

Primero resolver receipt: misma key+digest devuelve aceptación/IDs originales; misma key+digest distinto = 409; otra key no evita unicidad de historia/versión ni crea una segunda operación. Locks SQL por identidad y luego historias ordenadas, constraints únicas y relectura del ganador; ningún loser de una carrera genera otra revisión/job/provisión. CAS de binding/head protege reconcile concurrente. Bounded retry de serialización/deadlock: máximo 3 intentos con backoff 50/100/200ms dentro del deadline; luego 503.

Receipt durable `{receipt_id:UUID,schema_version:"strategy-ingestion-receipt.v2",request_digest:Digest,accepted_at:Timestamp,acceptance:"INGEST_ACCEPTED",strategy_ref:UUID,strategy_version_ref:Digest,runtime_strategy_id:string,histories:[{history_id,revision:int64,digest:Digest,operation_count:int64,movement_count:int64}],binding_ref:UUID|null,operational:{state,revision,reasons[]},analytics:{state,requested_profiles:[{profile_id,config_digest,status}],publication_ref:Ref|null},links:{self,readiness,histories}}`. La parte acceptance/identidad/heads aceptados es inmutable. Las secciones operational/analytics son snapshots actuales marcados `observed_at`; conservar referencia a la revisión aceptada aunque el head actual cambie. Estados analytics `ANALYTICS_PENDING|PROCESSING|READY|INSUFFICIENT_DATA|FAILED|STALE` no modifican acceptance ni habilitan órdenes.

Tras timeout/respuesta truncada/error 5xx: Forge registra `UNKNOWN_RECEIPT`, GET-by-key y compara request_digest+Strategy/Version. Si aún 404, espera jitter y puede repetir la misma key/body; el primer request podría seguir en vuelo y la unique debe converger. Si GET falla conserva UNKNOWN, nunca asume fracaso ni usa otra key. Retry externo 1/2/4/8/16/30s con jitter ±20%, máximo 10 minutos por intento de entrega; luego queda retryable durable para acción explícita, no bucle infinito. Receipt encontrado se vincula una vez al manifest V2 Forge; readiness sólo se actualiza desde la lectura Echo del binding exacto.

### 7. Provisión operacional separada

`OperationalRequestV2 = {mode:REGISTER_ONLY|PROVISION_REFERENCE,deployment_profile_ref:Ref|null,expected_binding_revision:int64}`. REGISTER_ONLY exige profile nulo y revision 0; registra definición, pero devuelve operacional `NOT_REQUESTED`. PROVISION_REFERENCE exige profile autorizado y revision 0 para creación; el endpoint separado exige revisión vigente para reconciliar. No incluir lotes, cuenta libre, credenciales ni políticas arbitrarias en el body productor.

Un `DeploymentProfileV1` Echo-owned se carga desde ETCD mediante SDK al startup y se sella por digest: `{profile_ref,profile_version:int64,namespace,allowed_producer_writer,source_mode:EXTERNAL_REFERENCE|NATIVE_RUNTIME,readiness_mode:OBSERVE_MASTER|SIMULATED_EXECUTION,run_mode:LIVE|BACKTEST|REPLAY,run_id:Ref,reference_account_id:Ref,reference_role:REFERENCE,execution_accounts:Ref[],instrument_ids:SemanticKey[],symbol_mapping_refs:Ref[],policy_template_refs:Ref[],mm_policy_ref:Ref|null,execution_mode:SIMULATED|LIVE,required_consumers:ConsumerRequirement[],authorization_ref:Ref|null}`. OBSERVE_MASTER con EXTERNAL_REFERENCE permite `execution_accounts=[]` y `mm_policy_ref=null`; no exige inventar copia ni riesgo. SIMULATED_EXECUTION exige cuentas/mappings/policies/MM concretas de un harness aislado. Native exige módulo admitido y config snapshot real del runtime A; no importa ejecutables MT5 como módulo Go. Las combinaciones incompatibles fallan 422.

I1 certifica profiles SIMULATED, recursos propios del harness y master simulado por contrato real. Un profile LIVE sin autorización económica/operacional vigente devuelve `BLOCKED_PERMISSION` y jamás ejecuta. El perfil no convierte las estrategias que Forge está extrayendo en candidatas para migración/activación; esas quedan REGISTER_ONLY hasta trabajo futuro autorizado.

`RuntimeBindingV1` inmutable por UUID incluye `{binding_ref,namespace,strategy_ref,strategy_version_ref,runtime_strategy_id,profile_ref,profile_digest,source_mode,readiness_mode,run_mode,run_id,reference_account_id,reference_role,config_revision:int64,config_digest:Digest}`. Cada revisión material de configuración genera nueva revisión sellada vinculada a la previa, no reescribe un binding que ya identificó un ciclo. El puntero activo cambia con CAS; un OPEN conserva el binding vigente al ingreso, un CLOSE se resuelve por el binding de su ciclo. No resolver operaciones históricas contra la versión actual mutable.

Mínimo durable adicional para B: `echo.strategy_ingestion_receipts`, `echo.runtime_bindings` con head/revisiones y desired/applied state, `echo.runtime_config_outbox` y `echo.runtime_config_acks`. Los crosswalks de identity/cycle/journal son los de A; historias/revisiones son los de C. No segunda tabla canónica de estrategias ni base LAB operacional. Outbox unique `(binding_ref,config_revision,target_consumer)`; ACK unique `(binding_ref,config_revision,target_consumer,consumer_incarnation)`. SQL conserva estado de control y prueba aplicada; no reemplaza checkpoints/estado operacional runtime.

En una transacción de registro/provisión: verificar profile/grants y scope de cuentas existentes → resolver definición/crosswalk → crear binding/version pin → insertar/update CAS policies reales `echo.account_strategy_risk_policy` sólo cuando el profile requiere ejecución y referencias reales account/config/symbol → insertar outbox por targets → commit. Nunca crear cuentas reales automáticamente ni editar recursos fuera del profile. Si faltan cuenta/policy/map no se confirma una provisión parcial engañosa: binding queda BLOCKED con lista y outbox sólo para configuraciones coherentes; aceptación/historia sigue confirmada. Una falla de persistencia antes del commit inicial revierte ingesta completa; una falla de propagación posterior se recupera desde outbox sin reingestar historia.

Reconciler Echo reclama outbox por lease+fencing monotónico (30s, heartbeat 10s), publica por mecanismos existentes de account-configs/execution-policies y configuración real del runtime según A. No inferir éxito desde webhook Hasura: el reconciler realiza publicación explícita desde snapshot exacto confirmado, de modo que el nuevo flujo no depende de triggers ausentes de metadata. Mensajes/outbox incluyen binding_ref, config_revision y config_digest; consumidores deduplican revisión/digest, ignoran antiguas y rechazan misma revisión distinta. Fencing impide que worker vencido marque APPLIED. Retry de envío 1/2/4/8/16/30s, timeout por intento 5s; a 45s expone demora; no borra trabajo ni declara READY por agotar retries. Reconcile explícito reutiliza refs deseadas; no renueva una autorización por el solo hecho de reintentarse.

### 8. Prueba de configuración aplicada y estados honestos

Nuevo contrato `RuntimeConfigAppliedV1` en canal autenticado `echo.runtime-binding-acks.v1`: `{schema_version:"runtime-config-applied.v1",namespace,binding_ref,config_revision:int64,config_digest:Digest,consumer_kind,consumer_id,consumer_incarnation:UUID,status:APPLIED|REJECTED,applied_at:Timestamp,checkpoint_ref:Ref,input_watermarks:[{stream,partition:int32,offset:int64}],lease_valid_until:Timestamp,reason_code:string|null}`. Actor runtime-ack server-side debe coincidir con consumer_kind/id requerido; un productor Forge/operador no puede autodeclarar ACK. No aceptar timestamp/watermark futuros o regresivos ni un digest distinto; `REJECTED` bloquea con causa.

APPLIED se emite desde el consumidor después de instalar la revisión exacta en su estado efectivo y checkpointarla según su mecanismo real. En StateFun la emisión debe ocurrir como efecto coherente con el checkpoint; para cache en memoria se usa incarnation+lease, revisión comprobada por lookup y re-ACK tras reinicio. Si no hay checkpoint/lookup coherente disponible, ese target sigue pendiente: no simular prueba. ACK de un broker Kafka sólo prueba transporte y no cumple este contrato. ConfigVersion de feed existente se conserva como versión de su perfil, distinta de `config_revision` de binding; ACK debe referenciar ambas cuando participa feed.

| state operacional | Condición verificable |
|---|---|
| `NOT_REQUESTED` | Registro/historias sin solicitud profile |
| `PROVISIONING` | Binding y desired revision confirmados; faltan publicación/ACK/probes |
| `BLOCKED` | Reasons tipados: NO_DEPLOYMENT_PROFILE, PERMISSION, ACCOUNT, IDENTITY_MAPPING, SYMBOL_MAPPING, POLICY, MM, UNSUPPORTED_RUNTIME, CONFIG_REJECTED, RECOVERY_INCOMPLETE |
| `ECHO_OPERATIONAL_READY` | Todos los gates del scope exacto pasan y leases vigentes; versión/binding/config/run/cuenta explícitos |
| `DEGRADED` | Binding antes listo pierde sesión/lease/checkpoint, llega nueva desired revision o falla recovery; nuevos OPEN sin dispatch |
| `REVOKED` | Operador revoca grant/profile; no nuevas aperturas; cierre/gestión segura de ciclos existentes conservada |

`ECHO_OPERATIONAL_READY` EXTERNAL_REFERENCE/OBSERVE_MASTER exige registry+version sellados, definition/crosswalk real, master account rol REFERENCE probado, mappings/instrumentos autorizados, ingress que resuelve binding exacto, journal writer disponible con readback probe sin órdenes y ACK aplicado de account/config/identity/bridge/session requeridos. Si el profile requiere copia, añadir planner/strategy_config/policies/MM/execution accounts ACK y route/permission gates; si es observación pura, informar `execution_enabled=false`, sin fingir política de copia. No require s1/s2 nativos ni una Operation del engine para master externo.

NATIVE_RUNTIME exige además módulo admitido y engine/runner configurado para ese run, recuperación/checkpoint completo, MM real pinneado y readiness de datos conforme a A; su feed técnico no se convierte por sí mismo en ReferenceEvent. La recepción de un master externo nunca crea domain.Signal u Operation nativa. Cada condición retorna `{gate_id,status,reason_code,evidence_ref,expected_revision,applied_revision,expected_digest,applied_digest,observed_at,valid_until}`. Requisitos vacíos sólo se omiten si el profile los declara no aplicables y la respuesta lo hace visible.

Lease/readiness TTL 15s renovable por consumidor cada 5s en el harness; validity global es el mínimo de targets/sesión/grants. Gateway/dispatcher verifica binding activo+revisión+TTL en el instante de decidir NEW OPEN, no sólo cuando Forge leyó un GET. Reinicio cambia incarnation y retira readiness hasta nuevo recovery/ACK. Cambiar config, revocar perfil o sesión caída invalida inmediatamente, sin depender de que LAB recalculase.

### 9. Carrera con master, journal y recuperación

Ingreso master autenticado usa cuenta/servidor/plataforma/rol/magic+mapping explícito y binding/run fijados; nunca `latest`, nombre, símbolo o magic global. Correlación de A: `reference_cycle_id` determinista con dominio `echo.execution.reference-cycle.v1` y tuple `(namespace,version_ref,run_mode,run_id,reference_account_id,source_family,opening_source_id)`; MASTER usa trade_id, TECHNICAL usa SignalID OPEN, crosswalk único y vínculo exacto si existe. Se conserva `runtime_operation_id` nullable; no igualar OperationID, SignalID, trade_id ni fila journal. A fija la codificación y writer del crosswalk; B sólo la consume.

Antes de READY se admite observación autenticada durable como `PENDING_BINDING_READY`, con fuente original, event_id/source_seq, binding candidato o causa unresolved. Dedupe de intake por `(namespace,source_instance_ref,source_event_id)` y journal por identidad real; captura pendiente no equivale a fill ni recepción operacional lista. Cap del harness: 10.000 eventos o 64 MiB por binding, 24h de retención recuperable; exceder rechaza/backpressure antes de ACK al productor, sin perder silenciosamente. No mezclar filas pendientes sin identidad con journal de una estrategia adivinada; se reconcilian cuando el mapping exacto existe o quedan `UNRESOLVED` con evidencia.

Cuando aparece readiness se resuelven y journalizan los hechos observados pendientes mediante el writer canónico A con `NOT_DISPATCHED_PRE_READY`; no reenviar OPEN antiguos a ejecución. Sólo eventos nuevos recibidos con binding READY son elegibles para dispatch y aún pasan la política vigente de delay/seguridad. Esto permite conservar historia y observar el master a t+60s sin crear órdenes antes de readiness ni una apertura tardía por recuperación. CLOSE/MODIFY de un ciclo existente sigue su ruta de gestión segura con binding original; no bloquear salidas por el gate de nuevas aperturas. Si CLOSE precedió la conciliación de OPEN, rearmar el ciclo desde secuencia fuente completa, no fabricar timestamps/fills.

Crash tras commit/antes publish: outbox reanuda. Crash tras publish/antes ACK: redelivery misma revisión/digest, consumidor converge. Crash tras APPLIED/antes receipt snapshot: recomputar readiness desde ACK vigente y lookup/checkpoint del consumidor. Reinicio runtime: incarnation anterior inválida. Crash tras master observado/antes journal: intake durable vuelve a writer con identidad estable. Crash después de journal/antes LAB: proyección read-only A/C reanuda desde watermark y misma revisión, sin duplicar operación/PNL. No recuperar abriendo órdenes a partir de curvas o proyección PG.

### 10. Traducción concreta Forge y superficies mínimas

Forge V2 toma `sqx.strategies` por StrategyRef exacto, `sqx.strategy_versions` por version_ref sellado y asignación `sqx.strategy_magic` correspondiente; comprueba canonical ID/receta/digests, y construye el DTO del SDK Echo. `construction_at` no se infiere de `sealed_at`; si el productor no guarda su evidencia real se transmite UNKNOWN y C marca los segmentos/analytics insuficientes. `construction_data_cutoff`, available_at e inicio Echo no se sustituyen. Los extractores SQX/MT5 producen OperationInputV2/CLOSED_SUMMARY o movimientos auténticos según evidencia; no inventan fills/Q_i, ni USD ni pares de historias inexistentes.

Persistir en Forge un manifest V2 write-once y delivery V2 con request_digest/key/canonical_body/refs exactos y receipt Echo; mantenerlo separado de la restricción histórica del V1 `UNIQUE(decision_ref,version_ref)`, porque una nueva revisión de historia no debe fabricar otra decisión/wave. Un registro V2 puede referenciar la promoción existente; no cambia su autoridad. Actualizar delivery state `INGEST_ACCEPTED`, `UNKNOWN_RECEIPT`, `RETRYABLE_ERROR`, `REJECTED`, más snapshot operacional independiente `binding_ref/revision/state/observed_at`; no un único enum que mezcle entrega y readiness. Forge puede guardar los refs retornados en su dominio inmediatamente tras acceptance, aunque analytics/operación estén pendientes.

| Repo/superficie | Cambio mínimo target |
|---|---|
| Echo `v3/sdk/contracts` + `wire` | DTOs V2, unión de recetas, canonicalización/validadores compartidos; preservar V1 |
| Echo `v3/sdk/postgres` | Registry extension aditiva, namespace/writer scoped GETs, receipt/histories de C, definición crosswalk A, binding/outbox/ACK y CAS |
| Echo `v3/gateway/internal/server.go`, nuevo handler/service V2 y config ETCD | Montaje real rutas; admisión/auth; una transacción application; worker reconcile acotado independiente de LAB |
| Echo policies/accounts/config consumers, Bridge/StateFun y native runtime de A | Propagar version/binding/revision/digest; ACK efectivo; gate OPEN; dedupe y recovery en owners existentes |
| Symphony `sqx/core/capabilities`, `sqx/core/forge`, `sqx/adapters/echo-handoff`, registry persistence | Productor SDK V2, exact refs, persistir manifest/delivery V2, GET reconcile y lectura readiness; sin lógica Echo duplicada |
| Echo Hasura/LAB | Read models de receipts/readiness filtrados; ningún permiso mutation ni dependencia para readiness |

Migraciones aditivas nuevas sobre el máximo real `066` del baseline; el paquete root adjudica números únicos entre A/B/C antes de implementar, sin editar las migraciones antiguas ni copiar las de ramas históricas. B aporta las tablas indicadas; no crea un runner nuevo. Probar en PG descartable y conservar guards de ownership/permisos; no aplicar metadata ni SQL en servicios compartidos durante Shot 1.

### 11. Aceptación ejecutable para los shots siguientes

Estos son casos a implementar/ejecutar en los shots posteriores; todos `NOT_RUN` en Shot 1. No equivalen a test verde ni autorización física. Integración Forge auténtica/Hasura físico queda `BLOCKED_EXTERNAL` cuando la ventana/artefacto/permisos no estén disponibles, no PASS inferido desde source.

| ID | Estímulo / oráculo requerido |
|---|---|
| B01 universal | Productor no Forge definition-v1 registra versión/historia sin promoción ni magic; Forge MT conserva UUID/ref MT exactos; mismo registry, receipt nuevo separado |
| B02 atomicidad | Segunda historia inválida, digest erróneo o runtime crosswalk incompatible: cero receipt/head/definition/outbox parcial; paquete anterior intacto |
| B03 idempotencia | 20 POST concurrentes mismo scope/key/body, respuesta perdida y GET reconcile: 1 receipt, 1 head, 1 job por perfil, 1 petición provisioning; otro body/key igual 409; otro namespace no lee UUID ajena |
| B04 CAS | PUT N→N+1 compite con otro escritor: uno acepta, otro 412; replay original posterior devuelve receipt original sin incrementar N+2 |
| B05 límites | Envelope representativo completo y límites 128MiB/8/250k/1M; exceso exacto 413 sin truncado; dos bulk simultáneos 429; demostrar memoria acotada con envelope V2 real |
| B06 permisos | Ingest producer sin profile grant no muta cuentas/policies; credenciales front/Hasura no provisionan ni ACK; GET ajeno 404; live no autorizado BLOCKED sin órdenes |
| B07 config real | Kafka PublishSync OK pero consumer retenido: PROVISIONING; ACK viejo/digest ajeno/incarnation vencida no produce READY; ACK aplicado más lookup real/checkpoint exacto sí lo permite |
| B08 master ~60s | Fixture auténtico aislado Forge→V2; detener LAB; master simulado a accepted_at+60s por endpoint/evento real → misma Strategy/Version/binding → journal writer real/readback con trade_id/cycle → historia Echo y continuidad C cuando LAB vuelve; ninguna dependencia al worker para READY |
| B09 pre-ready | Master entra antes ACK: capture durable, cero dispatch/órdenes; luego READY + reconcile produce journal `NOT_DISPATCHED_PRE_READY`, no replay de OPEN; nuevo master posterior READY usa binding correcto |
| B10 recovery | Cortar tras commit/publish/ACK/journal en cada frontera y reiniciar: IDs estables, sin doble journal/economía y sin opens retroactivos; native exige recovery gate A, external no requiere s1/s2 |
| B11 independencia | Analytics FAILED/INSUFFICIENT_DATA con operación READY válida; analytics READY con mapping/policy ausente sigue operacional BLOCKED; no booleano READY compartido |
| B12 versionado | Dos versiones misma estrategia y eventos tardíos: ciclo conserva versión/binding de apertura; rollout posterior no reasigna histórico; ejecución copy nunca se suma a Reference |
| B13 evidencia | Q_i/costes/monedas/construction unknown preservados y señalados; CLOSED_SUMMARY no fabrica fills; comparación API/readback contra artefacto fuente y journal auténticos |

Evidencia mínima por caso físico: SHAs/builds ejecutados, namespace/profile/run/binding/config_revision/digest, receipt/request digest, fuente histórica exacta y tamaño, checkpoints/ACKs por consumidor, t_commit/t_ready/t_master/t_journal, query/readback con identidad, órdenes emitidas (cero en observación/pre-ready), revisión de historia y watermark. Métricas/OTel usan request_id/receipt/binding/run; IDs de cuenta/trade se guardan como atributos trazables, no etiquetas métricas de cardinalidad ilimitada. El estado inicial real de este paquete es `DESIGN_SPECIFIED`, implementación `NOT_RUN`, físico `NOT_RUN` y campaña actual `NOT_ACTIVATED`.

## Fuentes

- [[F — Decision Register]], D17/D18/D23/D24 y D09/D10/D11/D16.
- [[Echo — Producto Integrado]], [[0 — Submanager State]] y [[SHOT4_HANDOFF]]: requisitos/antecedentes; capacidades de ramas históricas no prueban el baseline runtime.
- [[THE_LAB_V4_Diseno_para_revision]], §§E.1/E.2, y [[1 — TECHNICAL_FREEZE_PACKET]], R02/R04/R06: recetas, snapshots, CAS y límites compatibles.
- [[Echo + Echo Forge — Environment Contract]] y [[aranea-agent-dev]]: autoridad/ambiente y aislamiento.
- Código local fijado por repositorio, path y línea en §1 y §10; sin consultas remotas ni mutaciones de infraestructura.
