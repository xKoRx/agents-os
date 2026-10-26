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
created: "2026-10-26"
updated: "2026-10-26"
---

# B — Frozen Architecture

## Propósito

Congelar el delta mínimo ejecutable. Este documento es la única SPEC del nuevo workstream; A prueba CURRENT, C define aceptación y D despacha GLM. Todo nombre marcado TARGET debe implementarse, no se presenta como capacidad existente.

## Contenido

### B1. Decisiones y límites

**FROZEN · 2026-10-26 · DESIGN ONLY.** D25/D26 prevalecen sobre las partes de D23/D24 identificadas en el registro. Una ingesta V2, registry y StrategyDefinition existentes, un trade_journal operacional y el motor The Lab V4. No API V3, Signal nativa sintética, segundo journal, motor económico o scheduler de portfolios. No nuevas features de backtester, simulación Forex/Futuros ni campañas.

El flujo se divide por responsabilidad, sin acoplar tiempos: API/PG acepta identidad+historias y receipt; binding/provisioner aplica configuración; ingress/journal conserva hechos y el planner autorizado copia; outbox del journal produce revisiones de historia; worker V4 calcula y publica. `INGEST_ACCEPTED`, `ANALYTICS_PENDING` y `ECHO_OPERATIONAL_READY` jamás son sinónimos. La API no calcula métricas y la ingesta no emite órdenes. El estado analítico no es prerrequisito operacional.

Se rechaza copiar runtime completo por su divergencia y colisión SQL (A3), crear otro config plane porque Kafka/ETCD/StateFun ya existen, usar ACK de envío como aplicación, resolver por Magic global o hacer polling de analytics en el camino de una orden. Un outbox de dispatch estrecho sólo se añade para cerrar el crash entre journal y planner, reutilizando las tablas de intake/receipt como autoridad; no es otro motor.

### B2. Identidades y ownership

| Identidad | Autoridad y regla congelada |
|---|---|
| namespace / writer / principal | Auth Gateway/ingress confiable; nunca el body ni header Hasura sin verificar. `producer_ref` debe igualar writer autorizado. Grants por producer, namespace, profile y cuentas. |
| Strategy | `strategy_identity_mappings` y crosswalk `(namespace,producer_writer,external_strategy_ref)`; UUID Echo, canonical ID y fingerprint existentes. Referencia UUID sellada no concede acceso entre tenants. Display/symbol no resuelven identidad. |
| StrategyVersion | Recetas actuales `sqx-v1`, `native-v1`, `definition-v1`. Recomputar ref con helpers SDK; preservar grafía de target_platform y cuatro digests. Paquete inmutable; mismo ref+contenido igual reutiliza, distinto409. No usar ingestion time como versión. |
| runtime_strategy_id | Crosswalk actual `sv2:` + hex H(`echo-runtime-strategy.v1`,namespace,strategy_ref), `strategy_definitions` y `runtime_strategy_links`; una definición con instrumentos completos. BUY/SELL/BOTH se deriva LONG/SHORT/BOTH. No símbolo único ficticio. |
| Magic | Terna nullable inicialmente, no0 ni reserva implícita. Primera asignación certificada mediante `echo.fn_v4_assign_magic_allocation`; authority/allocation_ref/digest/evidencia. Inmutable una vez asignada. Reasignación de slot runtime es nueva vigencia de binding, no cambio de StrategyVersion. Identidad de slot `(ns,reference_account,source_instance,magic)`; no global. |
| binding / config | UUID binding inmutable por revisión; head CAS por `(ns,version,profile,run,reference_account)`; source-instance, cuentas y mode sellados en digest. Revision monotónica por head. Config digest D sobre snapshot efectivo canónico, nunca sobre sólo el nombre del profile. |
| cycle / event | Ciclo original por `(ns,source_instance,reference_account,source_cycle_id)` y binding/run/version pinneados al OPEN. Evento por `(ns,source_instance,source_event_id)`; event digest compara payload canónico exacto. source sequence ordena cambios dentro del ciclo; timestamp sólo evidencia temporal. |
| copy | Relación explícita ciclo reference→execution account→execution trade/command/fills; MM distinto permitido. Execution y Reference son hechos distintos y no se suman como rentabilidad de una misma estrategia. |
| history / revision / generation | Clave HistoryInputV2 existente con source/account/run/role/version; N inmutable, N+1 snapshot completo con digest/CAS. Cada generación fija vector revisiones+metadata+spec; read bundle fija generaciones/cohorte. |

Writers: producer sólo su registry/history; provisioner binding/config outbox; consumer sólo su incarnation/applied ACK; journal owner hechos operacionales; history projector sólo historias ECHO asignadas a su service principal; analytics sólo derivados; Hasura SELECT scoped. El productor Forge no escribe SQL Echo ni corrige historia Echo. Grants físicos del harness deben reflejarlo; no atribuir aislamiento a un usuario SQL omnipotente.

### B3. HTTP y DTO congelados

Mantener las seis rutas del mandato y sus DTO existentes. Matching exacto por segmentos/método, percent-decoding una vez, rechazar segmentos extra; métodos ajenos405, recursos no visibles404. `producer_ingest` puede sus ingest/history/binding; `lab_config_operator` sólo control autorizado; `lab_readonly` lectura scoped. ACK no es endpoint público producer.

| Ruta canónica | DTO / resultado / autoridad |
|---|---|
| POST /api/v2/strategy-ingestions | StrategyIngestionV2 → IngestionReceiptV2;202 nuevo/200 replay; producer_ingest |
| GET /api/v2/strategy-ingestions/{receipt_id} | IngestionReceiptV2 durable;200 o404 scoped al writer |
| GET /api/v2/strategy-ingestions/by-key/{key} | Mismo receipt por key original;200 o404, auth namespace+writer |
| PUT /api/v2/strategy-versions/{version_ref}/histories/{history_id} | HistoryInputV2 bare/wrapper → HistoryReceiptV2;200; key/CAS/owner obligatorios |
| POST /api/v2/strategy-versions/{version_ref}/operational-bindings | OperationalRequestV2+assertions B5 → binding_ref/config_revision/config_digest/estado y link readiness;202 creación,200 replay/no-op |
| GET /api/v2/operational-bindings/{binding_ref}/readiness | Snapshot derivado B6: estado/config/consumers/reasons/observed_at;200 no implica READY;404 fuera scope |

POST exige `Content-Type: application/json`, encoding identity, Idempotency-Key1..128 `[A-Za-z0-9._:-]`. Body usa `StrategyIngestionV2`; schema exacto, unknown/duplicate keys/UTF8 inválido y profundidad rechazan400 antes de unmarshalling. Límite128MiB,1..8 historias,≤250k operaciones/1M movements por historia, manifest definición≤256KiB; límites reales existentes se preservan y alinean con gateway/harness. No ampliación a zero-history en este programa: historia vacía con coverage honesta es válida si el DTO lo permite; no inventar una trade list para registrar identidad.

Campos/recetas y ejemplo completo: E. requested_curve_profiles sólo acepta descriptores registrados y config válida; ausencia activa los cuatro perfiles V4 por defecto. No aceptar knobs ignorados ni crear perfiles desde body. `strategy_ref` vacío asigna una vez; conjunto de instrumentos≤64 sin duplicados, IDs canónicos del catálogo configurado, dirección enum, timeframe vacío es desconocido. `magic_allocation` opcional con terna completa. Validar ArtifactRef y contrastar bytes/digest/size en backend permitido: no fetch de URLs arbitrarias del productor ni acceso a red compartida. Dependencias preservadas y digeridas, no `[]` constante. `definition_manifest` canónico debe producir exactamente `strategy_definition_sha256` mediante DefinitionContentDigest; `declared_version_ref`, si presente, debe igualar ComputeVersionRef. Paquete de otra receta rechazado; `existing_ref` no acepta paquete nuevo y debe pertenecer a la Strategy del mismo scope.

**Extensión temporal aditiva TARGET:** añadir `version_definition.temporal_metadata?: TemporalMetadataV2`, reutilizando el tipo SDK. Actualizar allowlists/decoders wire compartidos junto al campo, sin relajar unknown fields. Para versión nueva: o tres strings legacy completos, o temporal_metadata, nunca mezclados. Legacy usa evidencia coincidente válida de histories si existe; de lo contrario se traduce a DECLARED sin inventar prueba; las tres dimensiones deben coincidir con las histories. Con forma nueva se admite UNKNOWN+reason_code sin timestamp inventado. Las tres dimensiones versionales de todas las histories deben concordar; `echo_reference_started_at` pertenece a cada fuente/historia y puede diferir. No modificar la receta de version_ref: temporalidad permanece metadata versionada, no identidad ejecutable. `existing_ref` obtiene metadata de versión; nuevas histories no la sobrescriben silenciosamente.

PUT acepta forma actual bare `HistoryInputV2` o wrapper cerrado `{"history": HistoryInputV2}`. Validar bytes originales con parser estricto antes de descomponer wrapper; duplicados no desaparecen al remarshal. Idempotency-Key obligatorio como POST. `expected_revision` y `expected_digest` en HistoryInputV2; `If-Match`, si enviado, debe concordar con el digest. Falta precondición428, discrepancia header/body400, stale412. Misma key+digest retorna receipt original **antes de CAS**, incluso tras N+2. Mismo contenido con nueva key no crea revisión artificial: persistir receipt unchanged con head actual antes de devolverlo; repetición posterior recupera ese snapshot aunque avance head. No omitir receipt en rama UNCHANGED. EntityRef de ChangeEntryV2 usa operation_ref canónico: corregir SILENT_REMOVAL actual que compara source_operation_id; validar previous/new record digests del mismo scoped operation para corrección/retracción. Histories nuevas de versión existente pueden ingresar por POST usando existing_ref y su crosswalk original; projector usa servicio de historia transaccional de B9 sin repetir registry sintético.

**Corrección metadata TARGET:** wrapper PUT puede añadir `version_temporal_metadata?: TemporalMetadataV2` y `expected_metadata_revision?: int64`; son pareja obligatoria si se modifica evidencia versional. Sólo writer dueño de versión, lock/CAS metadata+history en una tx; stale412 y cambio no autorizado403. Sin pareja, diferencias con metadata versional vigente409; no last-writer-wins. Recalcular dependientes vía dirty existente. Metadata inicial se escribe una vez por request/version, no una vez por historia; artifacts retienen bytes reales. Echo-start queda por historia, no avanza metadata de otras fuentes.

POST response preserva `IngestionReceiptV2`:202 inicial,200 replay; acceptance INGEST_ACCEPTED, refs estables, request_digest, histories con revision/digests/counts, operational y analytics, links y Location. Receipt es snapshot inmutable de aceptación; GET por id/key devuelve ese snapshot, no cambia su digest con cada polling. Readiness se consulta por link binding; analytics por superficies V4 existentes. No afirmar que campos snapshot son estado actual. Error shape actual del Gateway se conserva con code/reason y path seguro; 409 identidad/key/paquete incompatible,422 semántica/economía/evidencia,401 auth,403 permiso,404 scope/ref,413 límite,415 encoding,429 backpressure Retry-After,503 dependencia no disponible. No SQL/token/stack en response.

### B4. Digest, transacción y recuperación del endpoint

Usar **exactamente** `echo-wire-json.v1`: D(`echo-strategy-ingestion.v2`, DTO normalizado canónico) = H(tag,string(canonicalJSON)). `CanonicalJSONV2Digest` y `DigestCanonicalBytesV2` son equivalentes en la fuente; no crear otro hash. Productor debe serializar el mismo DTO validado (incluidos defaults que el DTO emite), no calcular sobre un mapa arbitrario con campos omitidos distintos. Preservar recibos antiguos con su digest original; nuevas extensiones `omitempty` no cambian bytes de requests legacy. Receipt key scope `(namespace,writer,key)`; no clave global.

Orden: auth/admisión→parse/validación→canon/digest→lookup receipt→verify/store artifacts write-ahead→BEGIN→lock receipt key→replay lookup→lock registry/version y metadata→locks history refs **ordenados**→insert/verificar registry/version/definition→histories/revisions/metadata→receipt snapshot+dirty outbox→COMMIT→HTTP. Binding sólo si capability B5 completa y solicitado, dentro de la misma tx. Cualquier error revierte efectos DB; un artifact huérfano sin referencia es admisible, receipt parcial no.

FilesystemDigestStore debe escribir temporal exclusivo en mismo filesystem, verificar digest, fsync archivo, publicar atómicamente sin sobreescribir objeto existente (rename no-clobber/link apropiado), fsync directorio; objeto ya existente exige hash/size idénticos. Un archivo final parcial no se acepta. No installer fallback con store nil: Gateway falla503 antes de aceptar y el projector recibe store real. Artefactos referenciados deben ser recuperables tras reinicio; no digests inventados como sustituto de bytes. No GC nuevo.

INSERT versión en conflicto reconsulta y compara **todo** paquete sellado, no sólo ref. Diferencia409; igualdad reutiliza con nueva historia/key. Orden de locks común para POST/PUT: receipt→registry/version metadata→histories ordenados→binding head si se solicita→outboxes/targets; workers respetan inputs antes que targets. Deadlock/serialization retry acotado conserva key y consulta receipt después de commit incierto. Corte antes commit: sin efectos DB; corte después commit: GET-by-key encuentra snapshot, nunca nueva key para el mismo intento. Artifact ausente503 visible, no readback inventado.

Primer incremento E mantiene REGISTER_ONLY completo. Hasta B5 implementado, PROVISION_REFERENCE devuelve503 `OPERATIONAL_PROVISIONING_NOT_AVAILABLE` sin efectos; no receipt PROVISIONING sin binding/outbox. Esta indisponibilidad transitoria no bloquea gate endpoint, sí bloquea aceptación final del workstream.

### B5. Binding y profile efectivo

**Profile TARGET es configuración del plane existente**, no nuevo registry ni servicio: descriptor versionado bajo configuración ETCD de LabV4, cargado por SDK/Gateway como las identidades existentes; harness inyecta misma estructura por configuración explícita. Clave lógica `lab-v4/deployment-profiles/<profile_ref>` dentro del prefix/entorno configurado, sin hardcode de entorno. Resolver devuelve snapshot sellado; acceso exclusivamente de operador. Descriptor: `{profile_ref,profile_revision,namespace,source_mode,readiness_mode,run_id,run_mode,reference_account_id,source_instance_ref,execution_mode,execution_accounts,required_consumers,account_config_refs,policy_refs,instrument_mapping_refs,mm_config_refs,magic_allocation_ref?,native_descriptor_ref?}`. Refs fijan revision/digest; scope y permisos comprobados contra configuración real de cuentas, no se crean cuentas `harness` en código productivo.

No existe autoridad por valor default: OBSERVE_MASTER permite execution_accounts vacío y no necesita policies/MM de execution; exige cuenta reference autorizada y sus mapeos/config. SIMULATED_EXECUTION exige destinos simulados con policies/MM/permissions; LIVE sólo con autorización operacional específica y nunca en este programa. NATIVE_RUNTIME exige descriptor/module compatibles y snapshot aplicado del runtime; no lo simula mediante ReferenceEvent.

POST `/strategy-versions/{version_ref}/operational-bindings` conserva OperationalRequestV2 y los campos ya aceptados `reference_account_id`, `run_id`, `source_instance_ref`, `execution_accounts`, `target_consumers`. Los extras son **assertions**: si enviados deben coincidir exactamente con el profile; nunca conceden targets/cuentas libres. Ausentes se resuelven por profile. Registrar Idempotency-Key y digest de solicitud + digest de profile resuelto en receipt de mutación del binding (tabla estrecha B11); replay conserva snapshot aun si profile cambió. Mismo request con otra key y mismo desired digest devuelve binding vigente, no revisión. Expected revision obligatorio:0 si no head, N para sucesor; missing428, stale412. Ingest PROVISION_REFERENCE sólo creación expected0, usando el mismo servicio `...Tx`, no llamada HTTP interna.

Verificar versión/namespace/runtime link, fuente, grants, cuentas activas/mode, símbolos permitidos, policies y MM cuando corresponda; devolver422 con reasons si faltan datos,403 si falta grant. Un consumidor temporalmente caído no invalida identidad: binding deseado se acepta PROVISIONING. Canonical config contiene identidad completa, profile revision, config efectiva de cada consumidor y referencias de grants/policies/MM selladas, todos los required consumers y Magic certificado si necesario. Digest único incluye esas piezas; no secreto. Config revision N+1, binding_ref nuevo; CAS head y slot validity junto a outbox y receipt en una tx. Perfiles no se editan retroactivamente.

La asignación Magic posterior usa la función protegida existente con certificado del allocator productor ya autorizado por profile; no reservar número en Echo. Añadir al binding request `magic_allocation?: MagicAllocationV2` como evidencia opcional; debe resolver certificado y coincidir con profile, no basta el número declarado. Primera asignación y binding en una tx; mismo certificado replay, otro409. Mantener fingerprints históricos de crosswalk/receipts: consultar asignación sellada por su autoridad, no reescribir recibos ni permitir cambiar identidad por fingerprint. Validity [effective_from,effective_to) por slot; cierre de vigencia sólo impide OPEN nuevo, nunca pierde el binding de ciclos anteriores.

### B6. ConfigInstaller y readiness aplicada

Reutilizar RuntimeConfigSupervisor y ConfigInstaller; TARGET evoluciona claim/ACK, no se crea reconciler genérico nuevo. Cada proceso consumidor registra identidad `(ns,kind,id)` autorizada e incarnation UUID nueva al arrancar mediante CAS de epoch monotónico en runtime_consumer_incarnations. Sólo el propietario de esa identidad puede registrar/reemplazar incarnation. ACK no activa una incarnation. `ClaimOutboxBatch` filtra namespace+consumer kind/id, claims30s/heartbeat10s, token fencing monotónico; un supervisor no reclama ni acredita otro target. Retry1/2/4/8/16/30s con next_attempt/error visibles; una entrega no se borra.

Instalación: cargar binding/config snapshot y verificar digest→rechazar revision obsoleta→aplicar en el owner real→lookup de estado efectivo→checkpoint durable→ACK APPLIED. ConfigInstaller debe devolver prueba estructurada que incluya checkpoint y digest/revision leídos, no sólo un string cualquiera. Si crash después apply y antes ACK, lookup idempotente recupera prueba; si estado volátil se perdió, reaplicar antes de ACK. Marcar DELIVERED tras ACK aceptado, no al publicar Kafka. Si ACK persistió y mark-delivered falló, replay converge.

| Profile / consumidor requerido | Ruta de aplicación y checkpoint verificable TARGET |
|---|---|
| OBSERVE_MASTER · Core observation | Resolver exacto y cache de binding/instrumentos/identidad instalada en Core; lookup del mismo snapshot usado en MasterObservationFn. No requiere ejecución ficticia. |
| OBSERVE_MASTER · Bridge de source | Usar ClientConfig/SendConfigUpdate existentes para cuenta/reference e instrument mapping; devolver readback de config aplicada en la sesión del provider/EA. Escritura a socket no cuenta. Añadir confirmación con revision/digest+session incarnation en ese protocolo y simulador; owners cliente existentes v3/clients/mt4/reference_v3.mq4, execution_agent_v3.mq4 y equivalentes v3/clients/mt5/*.mq5 en handlers client_config; sin soporte consumer requerido queda PROVISIONING/BLOCKED_CAPABILITY. |
| SIMULATED_EXECUTION · Core/planner + StateFun config | Publicar por rutas Kafka account-config/execution-policy existentes con stamp binding; kache aplica y devuelve lookup del stamp efectivo. StrategyConfigFn guarda config+stamp en StateFun. Confirmación sólo desde lookup posterior al commit de estado (mensaje separado), no dentro del storage.Set provisional. Checkpoint incluye stream/topic/partition/offset y stamp. |
| SIMULATED_EXECUTION · Bridge por destino | ClientConfig aplicado y sesión provider con mapeos/MM/permissions efectivos; confirmación de aplicación y lookup. El broker simulado es destino, Core/Bridge/StateFun son reales. |
| NATIVE_RUNTIME · Core y provider bridge requerido | Componer snapshot mediante arranque/recovery ya existente; descriptor/config digest efectivo en engine. Si módulo no hot-reload, aplicar en reinicio controlado sólo del proceso propio del harness; nunca reconfigurar flota. Checkpoint de engine+recovery probado y lookup de bridge. |

Target consumer conserva formato existente kind/id, sin fallback default; catálogo cerrado de kinds CORE, BRIDGE, STATEFUN y IDs explícitos autorizados. Required consumers vienen del profile completo y se sellan en binding; no de las filas que casualmente tengan ACK. Para despliegue sin StateFun no añadirlo; para copy por StateFun es obligatorio. Una misma instancia puede servir múltiples bindings, pero cada ACK scope exacto. Si protocolo real de provider carece ACK, implementarlo en su adapter/cliente dentro de Shot2, no marcar READY con simulación de ACK sobre consumidor retenido. La falta de implementación es FAIL, no BLOCKED_EXTERNAL.

ACK debe acreditar `(ns,binding_ref,config_revision,config_digest,consumer_kind,id,incarnation,epoch,checkpoint,applied_at,lease_until,watermarks)`; auth runtime-ack restringida, tiempo DB para aceptación/lease máximo15s, applied_at no futuro ni regresivo y checkpoint correspondiente. Evento duplicado mismo payload es no-op; distinto409. Renovar cada5s **sólo** tras lookup/health del config efectivo; DELIVERED no elimina renovación. Incarnation anterior, token expirado, lookup distinto o ACK sin target se rechazan. DB/reachability perdida implica no NEW OPEN, no TTL indefinido.

Readiness deriva, no se escribe como boolean: head ACTIVO coincide exactamente con binding+revision; profile/grants siguen válidos; source session viva; todos los consumers sellados tienen ACK actual mismo digest/revision/incarnation/epoch, checkpoint confirmado y lease DB vigente. Ausencia→PROVISIONING, dependencia de config faltante→BLOCKED con reason, lease/aplicación perdida después READY→DEGRADED, revocación→REVOKED. Superseded head nunca READY para OPEN. Response incluye expected/applied por consumidor y lease/reasons, sin secretos; no devuelve READY por inferir publicación.

### B7. Reference → journal: un owner y correlación exacta

Extensión aditiva TARGET `managed_context` en envelopes reference/close/modify y comandos derivados: `{namespace,binding_ref,binding_revision,config_digest,strategy_version_ref,run_id,source_instance_ref,source_event_id,source_cycle_id,source_sequence}`. El ingress autenticado fija namespace/account/session y verifica el resto contra binding; no confía en texto de cliente. Para consumidores legacy sin campos, adapter de ingress resuelve **único** slot `(ns,account,source_instance,magic)` con vigencia acreditada por source event/session; si no hay identidad/orden exactos, intake UNRESOLVED, cero dispatch. No completar event ID con timestamp aproximado ni source instance `unknown_broker`. Native Signal sigue siendo otra entidad.

Los identificadores source_event_id y source_cycle_id son durables del productor/provider; si éste sólo expone trade_id, el adapter propio debe persistir asignación de event ID/seq antes de publicar y reutilizarla tras reconnect. Secuencia faltante con cambios incompatibles se retiene para reconciliar, no se ordena por llegada. MODIFY no crea OPEN ni nueva economía si sólo cambia SL/TP.

En module.yaml y consumidores, eventos V2 managed entran por MasterObservationFn→JournalObservationServiceV2. El legacy TradeJournalFn **omite sólo** esos eventos identificados; planner tampoco los ejecuta directamente desde topic de referencia. Eventos legacy conservan su ruta anterior. Para V2, journal owner escribe intake/receipt, ciclo pinneado, source correlation, journal_links y journal_change_outbox **en la misma tx** que SaveOpenTx/SaveCloseTx/actualización canónica correspondiente. No escribir SQL de journal desde worker LAB. Compare-and-reject de mappings existentes con distinto payload, no ON CONFLICT DO NOTHING indiscriminado.

Ciclo lookup incluye namespace, source instance, account, source cycle y run/binding; journal_id y trade_id existentes siguen autoridad del journal. Aumentar journal_change_seq monotónico por journal row bajo lock, no constantes1/2; correction/reconciliation emite nueva seq. Eventos idénticos devuelven receipt original sin nuevo journal ni outbox. Mismo event key y otro digest409/cuarentena visible. OPEN tardío o CLOSE-before-OPEN se conserva durable hasta resolver ciclo; ninguna unión aproximada.

Observación y permiso se separan: OPEN pre-READY puede quedar pendiente de identidad/config; cuando se resuelve se journaliza el hecho observado con `NOT_DISPATCHED_PRE_READY`. Congelar en intake el instante/estado de admisión y razón; reconciliar jamás cambia ese OPEN a elegible. Un OPEN nuevo posterior sí puede admitirse. Si la ingesta aún no committeó, conservar envelope autenticado con source key exacta; timer de reconciliation y cambios de binding/ACK lo retoman sin necesitar otra señal.

CLOSE/MODIFY usan binding y ejecución del ciclo original incluso si head cambió o lease expiró. Permitir cierre/reducción/protección conforme a permisos de gestión existentes; MODIFY que agrega exposición o afloja protección se trata como nuevo riesgo y exige gates vigentes. Si mapping/identity/session de gestión no se acredita, retener/reintentar con razón, no mandar a otra cuenta. CLOSE de un OPEN nunca copiado no genera orden nueva; sí actualiza observación/journal. Resultados de execution conservan rol EXECUTION y su relación de copia, nunca pasan como REFERENCE por `close_result` indiscriminado.

### B8. Copy segura y recuperación de órdenes

Reutilizar ExecutionPlannerFn→policies/account restrictions→MMEngine→Core/Bridge/StateFun. Cada execution calcula MM con su configuración vigente autorizada y la versión sellada registrada; no copia Q_i ni sizing de reference como verdad propia. `OBSERVE_MASTER` no crea dispatch rows/órdenes. Para SIMULATED_EXECUTION, un journal commit elegible crea intent de dispatch por destino **en la misma tx**, con command key estable `(ns,source_instance,source_event_id,binding_ref,binding_revision,execution_account,action)`; tabla estrecha de B11 justificada por atomicidad PG→StateFun, sin duplicar estado económico.

Relay entrega al planner existente al menos una vez, incluyendo managed_context. Planner reconsulta head/readiness/grants/policy/MM antes de reservar riesgo; dedup por command key en su estado y última barrera Bridge antes de enviar. Snapshot admission no es autorización permanente. No abrir si binding se reemplazó, lease expiró, account se revocó o configuración cambió entre intake y dispatch. Native NewRuntimeReadinessGate debe recibir identidad exacta run/account/version/binding del operation context; eliminar `ORDER BY ... LIMIT1` por strategy. Componer con recovery/arming/market gates ya presentes; no relajarlos.

Command ID estable llega al provider simulado y correlaciona execution result. Si envío puede haber sido aceptado y se perdió respuesta, estado `UNKNOWN_OUTCOME`, consultar broker/provider por ese ID antes de reenviar; sin lookup/dedupe acreditado, no reintentar OPEN automáticamente. No prometer exactly-once de un broker sin esa capacidad. Rechazo terminal conserva causa; fallo retryable antes de envío reintenta mismo ID y vuelve a verificar gates. Outcomes y fills únicos actualizan journal de execution por su owner y copy links existentes; ninguna historia reemite órdenes. Loss/restart de StateFun se reconcilia contra dispatch durable y provider antes de nuevo riesgo.

### B9. Journal → histories → The Lab

Retirar DrainJournalOutbox/ReconcilePending del retorno síncrono de MasterObservationFn. Reconciliation operacional corre en supervisor Core periódico/evento ACK; proyección analítica corre en `labv4-worker` existente con presupuesto separado y fallo aislado del análisis. No esperar métricas para journal ni copy.

Extender journal_change_outbox actual para claim/fence y scope explícito B11. Consumir snapshot_content inmutable por event_ref/journal seq, validar digest; nunca cargar todas las filas namespace y elegir una Strategy con LIMIT1. Agrupar exactamente `(ns,version_ref,run_mode,run_id,source_instance,account,role)` con binding pinneado por operación. Historia estable por ese grupo; versión distinta u otra cuenta produce otra historia. Cada grupo tiene un writer principal Echo registrado; no suplantar productor Forge ni volver a inventar display_name/direction/instrument set.

Factorizar en HistoryServiceV2 helper transaccional interno para crear/revisar historia **de versión ya registrada**, reutilizando validación, content/revision digests, COPY, append-only, receipt/CAS y dirty. Cargar snapshot N acumulado, aplicar cambios seleccionados por journal ID/seq (incluye OPEN/parciales/cierre/corrección) y producir snapshot N+1 completo; no truncar historia al tamaño del batch. Idempotency key derivada de grupo+vector exacto de eventos/seq. Recheck head/CAS y claim token al commit; conflicto recarga/reintenta. History commit+marca DELIVERED **sólo de event_refs incluidos** atómicos en misma DB. Sin identidad o evidencia técnica faltante conserva PENDING/FAILED visible; nunca marcar todo el namespace delivered. Outbox ya referenciado sin snapshot se reconstituye sólo de evidencia histórica exacta disponible; si no existe, error visible, no snapshot latest fingido.

Economía preserva decimal exacto del payload/journal snapshot; no convertir float64 de precio legacy en fill exacto. No inferir Q_i de InitialRiskPips, SL o MM actual. Sin ciclo budget certificado R/10k insuficientes; recorded money puede ser usable conforme a costos/divisa. CLOSED_SUMMARY y ECONOMIC_MOVEMENTS mutuamente exclusivos, net/gross/costes conforme al DTO; costes desconocidos distintos de cero. No crear fills/FX/SL/TP/Q. Runtime native usa sus facts y owner existentes, no un motor de Operation en LAB.

Historia Forge importada se mantiene. Historia Echo reference posterior se selecciona mediante history selection/segments V4; punto de corte real y disponibilidad temporal explícitos, no suma indiscriminada. Si hay mismo hecho económico importado/observado, exigir crosswalk SAME_ECONOMIC_FACT probado para excluir duplicación; sin prueba, no unir solapamientos automáticamente. Execution history sirve comparación/copy economics separada, nunca se suma al P&L reference. Comparación pre/post construction por opened_at y construction_at; economic_at/known_at/available_at/receipt distintos, generaciones antiguas reproducibles.

Reutilizar cadena actual HistoryRevision→history_dirty_outbox→relay→AnalysisWorkerV4→cuatro perfiles→metrics→cohortes completas→read bundle→screener/dashboard. Mantener algoritmos `recorded_money.v1`, `r_net_cumulative.v1`, `normalized_10k_open_balance.v1`, `normalized_10k_initial_balance.v1`, presets `edge_duo.v1`, `forge_quality_four.v1`, kernel shared-analytics y toda matemática/precisión/ventanas de V4 C/D/E. Input con insuficiencia produce estado/reason, no cero favorable. Worker lease60s/heartbeat20s/token y publish atómico; snapshot/cohorte completa antes de mover pointer. UI pinnea generación y membership, muestra PENDING/STALE/FAILED/INSUFFICIENT y no cambia score al cambiar sólo curva. No recalcular HTTP/Hasura/frontend.

### B10. Adapter Forge, sin dependencia inversa

Mantener `sqx/adapters/echo-handoff/http_ingress_v2.go` como adapter productor. Usar ControlPlane registry-postgres y sus `handoff_manifests`/`handoff_deliveries` existentes para implementar IngestionPersistenceV2; extender columnas/discriminador schema sólo donde el contrato V1 no represente V2. No segunda cola/framework; no sobrescribir rows V1. Manifest inmutable por scope+key contiene canonical request bytes/digest, source/artifact lineage y refs obtenidos. Load errors no equivalen a ausencia; store obligatorio, misma key otro digest conflicto local, persistir antes de red y propagar errores de update.

Conectar un entry point candidate-local de importación V2 al mismo adapter/ControlPlane para artefacto existente autorizado; no cambiar la campaña ni reiniciar workers reales. El seam de `forge_seal_handoff.go` conserva V1 por configuración explícita hasta habilitación posterior; habilitación V2 sólo en harness y usando traducción de evidencia canónica. No runtime Echo conoce clases SQX.

En200/202/GET recovery verificar schema, request_digest, producer/scope esperado, strategy/version y history IDs/digests/counts; respuesta malformada o key incompatible→UNKNOWN_RECEIPT/CONTRACT_CONFLICT, nunca INGESTED ciego. Retries1/2/4/8/16/30s con estado durable; timeout5xx consulta GET-by-key y conserva key;404 temporal no autoriza otra identidad. Guardar receipt antes de declarar éxito; operational readiness por GET aparte, sin confundir aceptación. Artefacto AUTH_FORGE bloqueado no impide implementar/validar adapter con fixtures etiquetados; sí impide declarar integración auténtica.

### B11. Persistencia aditiva mínima y migraciones

Los siguientes son **deltas TARGET**, no tablas supuestas existentes. Reservar siguiente número libre después de083, refrescado en cada integración; propuestos084 endpoint,085 binding/ACK,086 dispatch/projector. Si una capacidad se corrige sólo en Go, no crear SQL vacío para llenar número. Registrar hash/owner/preflight/ledger real del runner `v3/toolkit/cmd/apply-migration`; jamás editar067–083. No aplicar en compartidos.

| Delta | Esquema/constraint requerido |
|---|---|
| Endpoint/metadata | Reusar registry/version/history/artifact/receipt existentes. Conservar paquete completo y artifact bytes; adaptar constraints sólo si evidencia UNKNOWN requiere hacerlo. Metadata CAS por head_revision y owner_writer sellado al primer registro, persistido en metadata existente si falta; referencias a bytes verificables. No duplicar registro. |
| Binding mutation receipts | Tabla TARGET `echo.runtime_binding_mutation_receipts`: PK `(registry_namespace,principal_ref,idempotency_key)`, request_digest, resolved_profile_digest, binding_ref/revision, immutable response JSON, created_at. FK scoped a binding; append-only. Necesaria porque receipt de ingesta no es receipt de mutation autónoma. |
| Incarnation/ACK/outbox | Añadir epoch bigint>0 y claim fencing donde falten en tablas existentes; UNIQUE consumidor activo por scope, CAS al registrar; ACK FK a target y epoch/incarnation; tiempos/rev/digest/checkpoint constraints. Head CAS usa UPDATE WHERE revision=N y rowcount1; validity slot no solapado bajo lock. |
| Intake/correlación | Añadir managed context, source_cycle_id/sequence, admission_state/reason y digest fuente a tablas de intake/receipt/correlation existentes. Unique source event existente + payload compare; unique ciclo scoped. No reescribir hechos antiguos: fila legacy sin contexto no se vuelve administrada por inferencia. |
| Dispatch mínimo | Tabla TARGET `execution.reference_dispatch_outbox`: PK `(ns,command_key)`; FK observation receipt + binding/revision; execution_account/action, immutable payload+digest, state PENDING/SENT/CONFIRMED/REJECTED/UNKNOWN_OUTCOME/CANCELLED, lease/token/attempt/next_attempt, provider result refs. UNIQUE semantic command tuple; no P&L ni nuevo journal. Sólo journal owner inserta; relay actualiza entrega; provider result conserva evidencia. |
| Journal projector | Añadir a journal_change_outbox version/run/source/account-role y claim_owner/token/lease_until/attempt/next_attempt/last_error, índice parcial por estado. Scope FK por binding/journal link, snapshot digest validado, seq monotónico. Mantener snapshot_content y unique journal+seq existentes. Estado FAILED explícito si se amplía CHECK; no DELETE. |

DDL preflight rechaza checksum drift/owner incompatible antes de mutar. Roles mínimos separados en harness; grants de tablas/FKs por namespace+identidad, no confiar sólo en filtro de aplicación. Aplicar en PG aislado fresco y desde baseline; segunda aplicación por runner no-op comprobado; inyección de fallo rollback ledger+DDL. Down con datos rechaza pérdida, conserva historias/receipts; rollback normal es código compatible/deshabilitar writers propios y repair forward.

### B12. Fallos y recuperación obligatoria

| Corte/condición | Estado durable y siguiente acción | Prohibido |
|---|---|---|
| POST commit incierto | GET receipt misma key; replay original | key nueva para ocultar timeout |
| Artifact completo, tx falla | orphan sin referencia, retry mismo digest | receipt con artifact inexistente |
| Publish config sin apply | PROVISIONING; retry del consumidor | ACK al enviar Kafka/socket |
| Apply confirmado, ACK perdido | lookup+checkpoint, ACK misma revisión | reconfigurar otra revisión por latest |
| Restart/lease expiry | incarnation nueva invalida anterior; reaplicar/reACK | viejo ACK reactivando READY |
| OPEN durante bulk/provisioning | intake durable, journal al resolver, NOT_DISPATCHED_PRE_READY | copiar retroactivamente |
| CLOSE antes OPEN / replay | pending scoped; secuencia/ciclo exacto, idempotencia | fabricar OPEN/fill por timestamp |
| Revocación entre planner y Bridge | última barrera cancela NEW OPEN | confiar en READY cacheado |
| Provider aceptó, respuesta perdida | UNKNOWN_OUTCOME, lookup command ID | segundo OPEN con ID nuevo |
| Journal commit, LAB caído | journal/copy siguen; outbox pendiente | rollback operación por analytics |
| Projector crash/CAS perdido | revisar receipt/history head y event_refs; replay idempotente | delivered de filas no procesadas |
| Worker viejo/N+1/cohorte parcial | fence invalida publish, conserva generación anterior | mezcla N/N+1 o ranking por fila |

Cada fila se prueba en C con oráculo independiente. Las incertidumbres restantes son ejecución futura, no decisiones arquitectónicas abiertas. AUTH_FORGE y permisos externos concretos afectan gates propios; no convierten defectos de implementación en bloqueos externos.


### B13. Mapa concreto de implementación TARGET

Los archivos CREATE siguientes son nombres propuestos y no evidencia CURRENT. Conservar responsabilidad si un archivo equivalente aparece en HEAD refrescado; no duplicarlo. No cambia la división en shots.

| Acción / archivo relativo Echo | Símbolo/responsabilidad |
|---|---|
| MODIFY v3/gateway/internal/lab_v4_gateway.go y v2_wire.go | Routing exacto; DTO strict; receipts; assertions/profile/CAS; no cálculo |
| CREATE v3/gateway/internal/lab_v4_profiles.go | DeploymentProfileResolver desde config LabV4 existente; snapshot/grants y compatibilidad, sin DML de cuentas |
| MODIFY v3/gateway/internal/config.go y server.go | Cargar resolver; store obligatorio; inyectar servicios y capability transitoria provisioning |
| CREATE v3/sdk/contracts/runtime_binding_config_v2.go | DTO config snapshot/profile/stamp/managed_context comunes; validación/digest, sin tipos Forge |
| MODIFY v3/sdk/postgres/runtime_binding_repository.go | Servicio transaccional común para POST binding e ingest, receipt autónomo/CAS/outbox |
| MODIFY v3/sdk/postgres/runtime_config_supervisor.go y runtime_ack_repository.go | Claim por consumer, epoch/fence, installer result estructurado, renew con lookup |
| CREATE v3/core/cmd/echo-core/runtime_config_installer.go | Wire installer Core a cache/engine reales y lookup; nil fuera de capability no aparenta READY |
| CREATE v3/bridge/internal/runtime_config_installer.go | Config apply/readback por sesión y protocolo ClientConfig existente; último envío scoped |
| MODIFY v3/core/internal/functions/strategy_config.go | Stamp guardado con config; confirmación por lookup post-commit StateFun |
| MODIFY v3/core/internal/functions/master_observation.go y execution_planner.go | Owner único managed/admission, contexto exacto, dispatch al planner existente y gates |
| MODIFY v3/sdk/domain/reference_event.go y envelopes close/modify correspondientes | Extensión managed_context propagada sin crear Signal nativa |
| CREATE v3/sdk/postgres/reference_dispatch_repository.go | Persistir/reconciliar outbox estrecho B8/B11, unique command key; no decisiones MM |
| MODIFY v3/sdk/postgres/master_observation_service.go y strategy_history_v2_put.go | Intake/cycle scoped, journal seq, projector por snapshot/claim; helper historia existing version/CAS |
| MODIFY v3/lab-worker/cmd/labv4-worker/main.go | Inyectar artifact store real y ciclo projector separado; mantener worker V4 |
| CREATE migraciones siguientes libres084–086 sólo según B11 | Runner/ledger/grants/constraints; no editar migraciones históricas |
| MODIFY Symphony sqx/adapters/echo-handoff/http_ingress_v2.go y sqx/adapters/registry-postgres/strategy_version.go | Persistencia/receipt/retry del adapter real reutilizando ControlPlane |
| CREATE Symphony sqx/cmd/echo-ingest-v2/main.go | Entry point candidate-local que consume export autorizado+manifest, traduce DTO y usa adapter/store existentes; no campaña ni scheduler nuevo |

Config clients MT4/MT5 se modifican únicamente en handlers/persistencia de protocolo B6/B7, sin cargar binarios en flota. Tests del simulador deben responder sólo después de aplicar y de lookup; un ACK scripted sin aplicar no pasa. API analítica, shared-analytics, workers matemáticos, frontend/Hasura son NO-TOUCH funcional por defecto: sólo cambios mínimos demostrados por tests del nuevo flujo, preservando la SPEC V4.

## Fuentes

- Mandato Owner 2026-10-26; [[F — Decision Register]] D25/D26.
- [[A — Source Baseline and Branch Integration]] contiene los SHAs y localizadores efectivos.
- Contratos compatibles de `10-projects/Echo/The Lab/V4 — Runtime Integration/` y [[Echo + Echo Forge — Environment Contract]].
