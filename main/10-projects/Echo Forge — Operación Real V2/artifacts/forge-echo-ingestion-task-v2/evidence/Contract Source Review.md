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

# Contract Source Review

## Propósito

Conservar los hallazgos verificables del contrato compartido, consumidor Echo y entrega/persistencia V2 de Forge.

## Contenido

**Adjudicación del manager:** evidencia CURRENT revisada. Los cambios propuestos en este informe se subordinan a [[B — Frozen Design]] y [[10-projects/Echo/Ingestion V2 — Operational Integration/Forge Task — Contract Addendum|Forge Task — Contract Addendum]]. Las observaciones de source no son certificados de runtime.

Estado: **READ_ONLY_CONTRACT_REVIEW_COMPLETE**.

Alcance: revisión de fuente fijada por SHA. No se ejecutaron builds, suites, SQL, HTTP contra runtime, flota, campañas ni deploys. Este estado certifica la terminación de la investigación y no equivale a un PASS A/B/C/D/E. El manager mantiene la autoridad de adjudicación y el cierre Agents-OS sigue pendiente de orden Owner.

## 1. Conclusiones para el GOD Architect

1. La reutilización correcta es `HTTPIngressV2` + `IngestionPersistenceV2` + ControlPlane V2. El CLI existente sólo decodifica un JSON ya construido. Falta la nueva task declarativa con resolución y transformación de evidencias.
2. El pin de contratos de Symphony **no corresponde byte a byte ni por firma pública** al contrato del Echo candidato. Hay un tag real, pero es anterior a cambios materiales. Debe publicarse un único nuevo tag desde Echo y fijarse en ambos consumidores, con cold builds y goldens independientes.
3. La diferencia temporal importa directamente al producto: el tag consumido exige tres timestamps de versión; el candidato puede expresar `UNKNOWN + reason_code` mediante `VersionDefinitionV2.TemporalMetadata`. Inventar fecha de construcción para conservar el pin sería incorrecto.
4. El envelope no contiene un bloque tipado para metadata descriptiva enriquecida y métricas fuente. `provenance.inputs` preserva refs exactas, pero no importa los valores ni los vuelve consultables. Se justifica una extensión aditiva pequeña `SourceEvidenceV2`, con semántica/calidad explícitas, fuera de las recetas de StrategyVersion y fuera de métricas derivadas de The Lab.
5. `REGISTER_ONLY` existe operacionalmente; actualmente el validator exige al menos una historia. La variante correcta para una estrategia sin TradeSet es permitir **cero historias en REGISTER_ONLY**, conservando evidencia fuente tipada. No fabricar una historia vacía como sustituto de datos ausentes.
6. El adapter y su persistencia presentan defectos concretos de receipt/recovery que impiden certificar retries y reinicios: validación permisiva, pérdida de refs y scope al recuperar, UNKNOWN no persistido en rutas ambiguas, transición UNKNOWN→INGESTED bloqueada, y errores de actualización de refs ignorados.
7. Echo posee aceptación transaccional, historial y cálculo asíncrono. También hay un bug de receipt en reutilización de historia y déficits en el loader analítico que requieren oráculos focalizados.
8. `PROVISION_REFERENCE` es rechazado incondicionalmente por **POST strategy-ingestions**. Sí existe un endpoint operacional separado con resolver de profile/grants, provisioning y readiness. No concluir ausencia general de la capability operacional.
9. `UNKNOWN_RECEIPT` nunca es rechazo. Una corrección de evidencia no es un retry idéntico: POST de contenido cambiado para la misma historia devuelve HISTORY_EXISTS; Echo ya tiene PUT de revisión con CAS. No cambiar history_id o key arbitrariamente para eludir el protocolo.

### 1.1 Tabla ejecutiva de adjudicación

Las fuentes Symphony de esta tabla están fijadas en `22f337ca434549c492b2d402fd158e23ac4758a8`; las fuentes Echo en `f93cd4f80085e328f9176c1215e42e6c8e0b2404`. Severidad/gate final: adjudicación del manager. No convertir estas observaciones en una auditoría general del consumidor.

| Finding | Fuente exacta | Impacto sobre esta task | Delta mínimo candidato | Oráculo independiente |
|---|---|---|---|---|
| CONTRACT-PIN | Echo tag/subtree; contracts/strategy_ingestion_v2.go VersionDefinitionV2.Validate; strategy_history_v2.go digest methods | Productor y servidor tienen DTO/validator/API distintos; UNKNOWN temporal no expresable con pin actual | Publicar un contrato único en Echo y fijarlo en ambos consumidores | Cold build de ambos con tag remoto; hash/API/corpus exactos |
| CONTRACT-REGISTER | contracts/StrategyIngestionV2.Validate exige histories 1..8 | Sólo métricas no se puede representar sin fabricar historia | REGISTER_ONLY con histories=[] y SourceEvidence tipado | Registry/version/evidence presentes; histories y curvas económicas ausentes |
| CONTRACT-EVIDENCE | StrategyRegistrationV2, IngestionProvenanceV2 y accepted_snapshot | Metadata/MetricSet quedan sin valores tipados/readback | SourceEvidence aditivo persistido; reutilizar NamedRef/MetricV1 cuando aplicable | Recuperar valores/unidades/basis/provenance exactos; StrategyVersionRef invariante |
| FORGE-RECEIPT | HTTPIngressV2.validateReceiptV2 | Receipt malformado o de otra historia puede considerarse aceptado | Validator canónico completo, compartido; cotejar expected refs/digests/counts | Digest vacío, history equivocada, count falso y scope ajeno nunca aceptados |
| FORGE-RECOVERY | HTTPIngressV2.reconcileUnknown; ControlPlane.LoadManifest/UpdateReceipt | Se pierden UNKNOWN/refs/scope y no puede salir de UNKNOWN | Rutina única POST/GET de validación+persistencia; transición verificada y actualización atómica | Crash tras POST, restart, GET200 convergen; GET404 sigue UNKNOWN durable |
| FORGE-BINDING | migration017 UNIQUE(decision_ref,version_ref); Ingest prepara versión vacía | Cohorte/revisión/destino puede colisionar antes de red | Resolver versión y scope/destino antes de persistir; cardinalidad explícita sobre store existente | Dos estrategias de cohort; dos destinos; dos tasks concurrentes sin corrupción |
| ECHO-R1 | strategy_history_v2_service.go acceptOneHistoryV2:440–444 | Nuevo POST que reutiliza historia devuelve content_digest como revision_digest | Usar headDigest en HistoryReceiptV2.Digest | Misma historia con key nueva conserva revision_digest exacto |
| ECHO-R2 | DecodeStrategyIngestionV2 → wire.Decoded.Bind(histories) | Potencial descarte de unknown anidado y divergencia de digest | Reusar decoder estricto de HistoryInputV2 en envelope | Unknown dentro history/operation produce rechazo sin efectos |
| ECHO-R3 | VersionDefinitionV2.Validate existing_ref + resolvedVersionTemporalV2 | Riesgo de degradar metadata existente a DECLARED vacío | Preservar metadata al reutilizar versión; corrección explícita vía CAS | Existing_ref sin nueva evidencia no cambia metadata head/digest |
| LAB-C1/C2/C3 | lab_analysis_service.go loadHistoryEvents; HistoryServiceV2.insertRevisionV2 | Coverage, currency_status y UNKNOWN time pueden perder su distinción analítica | Propagar evidencia de los campos ya persistidos en loader mínimo | GAP/UNPROVEN/UNKNOWN no producen cobertura completa, moneda probada o epoch fabricado |
| OPERATIONAL-BOUNDARY | AcceptIngestionV2:174–179 y gateway.handleOperationalBindingPost | Modo integrado rechaza provisioning aunque exista endpoint separado | Task REGISTER_ONLY por defecto; no prometer camino no cableado | Registro no crea binding; regresión separada demuestra provisioning/readiness autorizado |

### 1.2 Estado de verificación de esta investigación

| Actividad | Estado |
|---|---|
| Ref refresh y Git tree/blob comparison | Revisado por fuente fijada |
| Mapping de DTO, digest y recuperación | Revisado por fuente fijada |
| Cold builds Echo / Forge | **NOT_RUN** |
| Tests unitarios / integración / adversariales de esta task | **NOT_RUN** |
| SQL / HTTP / Temporal contra runtime | **NOT_RUN** |
| Fuente auténtica y E2E A/B/C/D | **NOT_CERTIFIED_BY_THIS_REVIEW** |
| Release / deploy | **NOT_RUN** |

Claims históricos del baseline, incluidos tests reportados por otros shots, no certifican la nueva task ni reemplazan el rebuild y QA posteriores a su SHA final.

## 2. Baselines y pruebas de distribución

Refs refrescadas por GitHub Git refs API durante esta revisión:

| Repositorio / ref | Commit actual |
|---|---|
| Echo `lab-v4/shot4-integration` | `f93cd4f80085e328f9176c1215e42e6c8e0b2404` |
| Symphony `lab-v4/shot4-symphony` | `22f337ca434549c492b2d402fd158e23ac4758a8` |
| Echo tag `v3/sdk/contracts/v0.0.1-lab-v4-shot2.1` | annotated tag `00caa298a670b9adaea3a8e2b3ff441fee9ebee1` → commit `52f8d509e0e9127a9f263f02d76565dae508a2f6` |

La ruta física es `v3/sdk/contracts`; el module path es `github.com/xKoRx/echo/v3/sdk/contracts`, Go 1.24. Buscar `sdk/contracts` en la raíz o el tag sin prefijo `v3/` produce 404 y no demuestra falta de distribución.

Fuente:
- [Echo ref](https://api.github.com/repos/xKoRx/echo/git/refs/heads/lab-v4/shot4-integration)
- [Symphony ref](https://api.github.com/repos/xKoRx/symphony/git/refs/heads/lab-v4/shot4-symphony)
- [Tag ref](https://api.github.com/repos/xKoRx/echo/git/refs/tags/v3/sdk/contracts/v0.0.1-lab-v4-shot2.1)
- [Tag object](https://api.github.com/repos/xKoRx/echo/git/tags/00caa298a670b9adaea3a8e2b3ff441fee9ebee1)
- [Symphony go.mod](https://github.com/xKoRx/symphony/blob/22f337ca434549c492b2d402fd158e23ac4758a8/sqx/go.mod)
- [Echo contracts go.mod](https://github.com/xKoRx/echo/blob/f93cd4f80085e328f9176c1215e42e6c8e0b2404/v3/sdk/contracts/go.mod)

Symphony requiere contracts y shared-analytics `v0.0.1-lab-v4-shot2.1`, sin replace de Echo. Sí hay replaces para `github.com/xKoRx/sdk => ../../sdk` y `github.com/xKoRx/symphony => ../`; por tanto un cold build de Forge debe acreditar también esos inputs exactos y no depender de un sibling desconocido. El go.sum contiene:

- contracts zip: `h1:v63lfAOfRHCKj4oXx8wzJ9+CZMMN/BvDkdm54QkREbg=`
- contracts go.mod: `h1:wtoVEVwmxMd/pPT4nm9MxK30uhHXP8iI1L545fqDj9g=`

Echo sdk/go.mod y gateway/go.mod requieren contracts `v0.0.0` y lo reemplazan por su módulo local; esto explica que servidor y productor compilen contra fuentes diferentes aunque importen el mismo path. No es evidencia suficiente de distribución independiente.

### 2.1 Comparación de árboles Git

Los árboles recursivos obtenidos de GitHub no estaban truncados. Subtree contracts:

- Tag: `4aa8b38321b960c6dabdb7e90f0a7c053bcfebfb`.
- Candidato: `d579adbd56926f8cd5f8909fe7265cb9b4d5980a`.

| Archivo | Blob tag | Blob candidato | Diferencia relevante |
|---|---|---|---|
| strategy_ingestion_v2.go | c5b143756405d72fec6d06f337b67064329cbb03 | c1af8852a9495f2777aad3da6a349cffef532e57 | temporal_metadata aditiva; XOR con strings legacy; concordancia temporal entre historias y versión |
| strategy_history_v2.go | 2e9194b9b772421d375e0d4a2c3c66f22f7e45e6 | a69a7dd0d1e3cd873584069b2d72ac93b51603e8 | copy_execution opcional; firmas de digest; DecodeTemporalMetadataV2 |
| v2_common.go | 23859e2ae3886e4f9da458ce04573efca0d13c6e | 79713e344f5df53d3945da09a87d5c668092dc8b | CanonicalizeJSONBytesV2 y DigestCanonicalBytesV2 nuevos |
| wire/canonicalize.go | 20ef0eb5c31435a82f7578e9b799c84b5b7ad0af | 2ac4ecec7168570f1b958392b55a229e1d7cab4c | Go values pasan a emitter directo |
| wire/hash.go | 1d7f42e3448e3e1970e3e1e71aa8d6b2c7680e06 | 172d6ce63524e27ff82fd6ec5950eca654cd2dec | digest en streaming |
| runtime_binding_config_v2.go | ausente | dd997d58c8628c44be80ca03fbc0482a54602333 | contratos binding nuevos |
| wire/canonicalize_direct.go | ausente | 64e1033e9603815542752bd11d4d6966a5a62bed | emitter directo |

Hay además tres archivos de tests nuevos. `MovementDigestV2` y `OperationDigestV2` cambian de `(string,error)` a `string`; por tanto no hay signature parity. La receta declarada del digest se conserva para inputs legacy sin campos nuevos y existen tests diferenciales, pero **no se ejecutaron**. No confundir intención documentada de bit parity con prueba ejecutada.

Gate requerido: nuevo tag publicado y resoluble por ambos consumidores; subtree y checksum fijados; `GOWORK=off`, cache limpio controlado y sin replace local de contracts como única prueba; builds independientes; corpus compartido que compruebe bytes y errores, además de refs/digests.

## 3. Contrato actual: envelope, identidad y versión

Fuentes principales:
- [strategy_ingestion_v2.go](https://github.com/xKoRx/echo/blob/f93cd4f80085e328f9176c1215e42e6c8e0b2404/v3/sdk/contracts/strategy_ingestion_v2.go)
- [evidence.go](https://github.com/xKoRx/echo/blob/f93cd4f80085e328f9176c1215e42e6c8e0b2404/v3/sdk/contracts/evidence.go)
- [identity.go](https://github.com/xKoRx/echo/blob/f93cd4f80085e328f9176c1215e42e6c8e0b2404/v3/sdk/contracts/identity.go)
- [registry V2](https://github.com/xKoRx/echo/blob/f93cd4f80085e328f9176c1215e42e6c8e0b2404/v3/sdk/postgres/strategy_ingestion_v2_registry.go)

### 3.1 Mapping de campos del envelope

| Campo real | Semántica / mapping exigido |
|---|---|
| schema_version | Literal `strategy-ingestion.v2`. |
| producer_ref | Writer autorizado configurado server-side. Echo exige igualdad con auth.Writer. No deducir de folder. |
| external_strategy_ref | Identidad externa estable del productor; no display name ni filename. Convergencia por namespace, writer y external ref. |
| strategy.canonical_strategy_id | Identidad canónica exacta del productor (UTF-8, hasta 1024 bytes); la evidencia fuente decide su valor. |
| strategy.strategy_ref | UUID minúscula sellada; puede estar vacío para primera asignación Echo. No confundir con un ref local Forge que tenga otro dominio de identidad. |
| strategy.display_name | 1..256 bytes, dato descriptivo; participa en fingerprint del mapping de identidad, no en StrategyVersionRef. |
| strategy.instrument_ids | 1..64 instrumentos explícitos, únicos; set íntegro. |
| strategy.direction | LONG, SHORT o BOTH; fuente acreditada. |
| strategy.timeframe | Semantic key de hasta 32 bytes; vacío representa no declarado en este struct. |
| strategy.magic_allocation | Opcional y sólo si existe asignación acreditada: magic_decimal, allocation_ref SHA256, assigned_at. No generar magic para registrar. |
| version_definition | Unión existing_ref XOR paquete sellado por identity_recipe. |
| histories | Actualmente 1..8 historias. Extensión necesaria: 0 para REGISTER_ONLY sin evidencia económica. |
| requested_curve_profiles | Hasta 16 profile IDs únicos y config map; en el servicio inspeccionado sólo se valida y no configura el worker. Omitir o rechazar intención no soportada; no prometer aplicación. |
| operational_request | Omitido o REGISTER_ONLY → NOT_REQUESTED. REGISTER_ONLY exige profile vacío y revision 0. PROVISION_REFERENCE no aceptado en este POST candidato. |
| provenance.inputs | 1..64 NamedRef con role, ref, schema_version opcional, content_digest opcional. Preservar FlowRunRef, TaskPath/TaskName, StageExecutionRef, EvaluationRef, MetricSetRef, TradeSetRef, run/variante y artefactos con roles congelados, sin “latest”. |

Un `NamedRef` referencia un input exacto, no aporta resolución remota automática. Pares (role,ref) duplicados se rechazan; mismo role con refs distintas es válido. Sus hashes deben ser los de las evidencias reales, no hashes calculados sobre nombres de archivos.

### 3.2 Recetas de StrategyVersion

**sqx-v1 / native-v1**:

`H("echo-strategy-version.v1", canonical_strategy_id, target_platform, executable_sha256, effective_inputs_sha256, runtime_context_sha256, dependencies_sha256)`.

Los cuatro hashes son refs `sha256:<64 hex minúscula>`. `sqx-v1` exige target MT4/MT5/MetaTrader4/MetaTrader5 (la grafía entra al hash), execution_manifest y ArtifactRef de executable/effective inputs. `native-v1` exige ECHO_NATIVE, NATIVE_RUNTIME, módulo y descriptor nativo, además de los hashes/artefactos previstos.

**definition-v1**:

- target_platform = ANALYTIC.
- definition_manifest canónico, máximo 256 KiB.
- strategy_definition_sha256 = `D("echo-strategy-definition-content.v1", definition_manifest)`.
- version_ref = `H("echo-strategy-definition.v1", canonical_strategy_id, "ANALYTIC", strategy_definition_sha256)`.

Echo recomputa los refs y rechaza declared_version_ref o definition_sha256 incongruentes antes de crear receipt. Si sólo existe una definición analítica exacta, no fingir un paquete ejecutable. Un SQX, XML de definición, MQ5/EX5 y execution manifest no son intercambiables.

**existing_ref** verifica en SQL que la versión pertenezca a la misma namespace + canonical strategy + strategy UUID. No crea un paquete nuevo.

Métricas, evaluaciones, ranking, cuenta/broker, rutas de artefactos, fecha de ingesta y provenance **no entran a StrategyVersionRef**. Un SourceEvidence nuevo no debe modificar estas recetas. Artefactos tienen identidad de bytes (sha256 + size + kind/schema/platform) separada del locator (store_id,bucket,key).

### 3.3 Evidencia temporal

El candidato admite dos formas exclusivas para una nueva versión:

- Tres strings legacy completos: construction_at, construction_data_cutoff, available_at; se convierten internamente a evidencia DECLARED.
- `temporal_metadata` con TimeEvidenceV2 para esas tres dimensiones y echo_reference_started_at.

TimeEvidenceV2:
- PROVEN: value canónico y evidence_ref obligatorios.
- DECLARED: value obligatorio; acredita declaración, no prueba.
- UNKNOWN: value ausente y reason_code obligatorio.
- NOT_APPLICABLE: value ausente.

Incluye raw, timezone y precision (INSTANT/CIVIL_DAY/UNKNOWN) cuando existan. El timestamp canónico es UTC RFC3339Nano, sin zona implícita ni medianoche fabricada. Construction es la construcción real de la definición/versión; cutoff es límite de datos de esa construcción; available es disponibilidad acreditada. No sustituirlas por export time, filesystem mtime, primer trade o ingestion time.

Las tres dimensiones versionales conocidas deben concordar entre historias y con la versión. EchoReferenceStartedAt pertenece a cada historia, puede diferir y no debe moverse hacia atrás por una importación retrospectiva.

**Riesgo adicional de source a cubrir:** `VersionDefinitionV2.Validate` retorna temprano para existing_ref; `AcceptIngestionV2` igualmente llama `resolvedVersionTemporalV2` y `persistVersionMetadataV2`. Un existing_ref sin strings ni temporal_metadata produce DECLARED con valor vacío y puede intentar escribir nueva metadata. Oráculo obligatorio: reutilizar versión no degrada timestamps ni evidencia; corregir el branch mínimo si se confirma en integración.

## 4. Historia económica, identidad y precisión

Fuente: [strategy_history_v2.go](https://github.com/xKoRx/echo/blob/f93cd4f80085e328f9176c1215e42e6c8e0b2404/v3/sdk/contracts/strategy_history_v2.go).

### 4.1 Campos HistoryInputV2

| Campo | Requisito |
|---|---|
| schema_version | `strategy-history.v2` |
| history_id | ID fuente estable de 1..256 bytes; distingue evidencia/evaluación/run/variante. No derivar de folder ni aleatorizar en retry. |
| source_kind | FORGE_SQX, FORGE_MT5, ECHO_JOURNAL, ECHO_RUNTIME u OTHER_DECLARED; aquí fuente Forge real. |
| source_instance_ref | Instancia de productor explícita y estable. |
| account_ref / account_absence_reason | Exclusivos; una de las dos requerida. Un backtest puede declarar ausencia real de cuenta. |
| run_mode | LIVE, BACKTEST o REPLAY, obtenido de contrato del productor. |
| run_ref / run_absence_reason | BACKTEST/REPLAY exige run o motivo de ausencia. No inventar run para completar DTO. |
| role | REFERENCE, EXECUTION o NATIVE; no confundir REFERENCE histórico con readiness de trading. |
| mm_context_digest / mm_evidence_ref | Contexto y prueba de money management, cuando existan. |
| expected_revision / expected_digest | 0/ausente para creación; precondiciones CAS para revisión. |
| temporal_metadata | Cuatro TimeEvidenceV2; definición temporal anterior. |
| coverage | Intervalos [from,to), COMPLETE/PARTIAL/GAP, calendario, timezone, precisión, observed_through, known_at, evidence_ref y expected_operations cuando acreditados. |
| provenance | RawMessage existente; entra al content digest. Para semánticas nuevas indispensables usar la extensión tipada, no otro blob libre. |
| operations | Snapshot económico de hasta 250000 operaciones por historia. No reconstruir trades desde métricas. |
| retractions | CORRECTION, RETRACTION o REPRESENTATION_UPGRADE con previous/new digest, reason y source evidence exactos. |

Recetas únicas:

- history_ref = `H("echo-history.v2", namespace, version_ref, writer, history_id)`.
- operation_ref = `H("echo-history-operation-id.v2", history_ref, source_operation_id)`.
- movement_ref = `H("echo-history-movement-id.v2", history_ref, source_operation_id, source_movement_id)`.
- content_digest = `D("echo-history-content.v2", scope + temporal_metadata + coverage + provenance_source + operation_digests + change_entries)`.
- revision_digest = `H("echo-history-revision.v2", history_ref, decimal(revision), previous_revision_digest_or_empty, content_digest)`.

Sets de operaciones/movimientos/cobertura/cambios se ordenan por digests para contenido; arrays causales conservan su semántica. El request digest conserva el orden de los arrays del envelope: el productor debe construir un orden determinista y reutilizar exactamente el manifest ya preparado.

### 4.2 OperationInputV2

| Grupo de campos | Uso correcto |
|---|---|
| source_operation_id, operation_ref | Identidad estable de la operación fuente; Echo recalcula operation_ref. No usar timestamps/precios como crosswalk. |
| cycle_started_at, opened_at, closed_at | TimeEvidenceV2, estado explícito, raw/timezone cuando proceda. |
| status | OPEN, CLOSED, CANCELLED, CLOSED_INCOMPLETE_ECONOMICS o RECONCILIATION_REQUIRED. |
| instrument_id, contract_ref, side | Instrumento/contrato exactos; LONG/SHORT cuando conocidos. |
| orders_refs, fills_refs | Referencias reales de órdenes y fills; no sintetizar granularidad que el exporter no tiene. |
| granularity | CLOSED_SUMMARY XOR ECONOMIC_MOVEMENTS. |
| qi | Opcional; nunca calcular desde P&L, drawdown, stop actual o capital arbitrario. |
| closed_summary | Neto de cierre, gross opcional, breakdown y disclosure; sólo para CLOSED_SUMMARY. |
| movements | Hechos económicos firmados; exclusivos del grano ECONOMIC_MOVEMENTS. |
| reconciliation_summary | Evidencia existente de conciliación, no un motor nuevo en Forge. |
| exposure | FLAT, OPEN o UNKNOWN; quantity/unit/measured_at/evidence opcionales cuando acreditados. |
| provenance | Origen exacto del hecho. |
| correlation | Source operation, binding, reference cycle, runtime op, event, trade, opening signal, order/fill y copy-intent sólo si existe crosswalk acreditado. |
| missing_fields | Ausencias explícitas; no ceros por defecto. |

**CLOSED_SUMMARY** exige net MoneyV2 y prohíbe movements. El neto único no se suma otra vez con sus componentes. **ECONOMIC_MOVEMENTS** usa REALIZED_PNL, COMMISSION, FEE o SWAP; amount_signed, economic_at, known_at, source_event_ref y source_event_digest; inclusion_basis GROSS_DELTA o SIGNED_COST. Tiene causal stream/seq, order/fill, accounting revision, contract snapshot y cost model opcionales.

`MaxMovementsPerHistoryV2=1000000` está declarado como límite por historia, pero el validator actual compara len(movements) por operación; la task debe imponer el total por historia y el budget de bytes real, y el oráculo debe detectar que no se exceda por suma.

### 4.3 Dinero, coste, Q_i, moneda y FX

MoneyV2 exige decimal canónico **string**, moneda de tres letras mayúsculas y currency_status OBSERVED/DECLARED/UNPROVEN; OBSERVED/DECLARED requieren evidence_ref. La moneda no puede faltar en un hecho monetario. No asumir USD/EUR por instrumento o cuenta implícita.

CostDisclosureV2 declara net_basis NET_ALL_DECLARED_COSTS/GROSS_ONLY/PARTIAL_NET/UNKNOWN, y comisión/fee/swap/otros con KNOWN_ZERO/KNOWN_NONZERO/UNKNOWN/NOT_APPLICABLE más evidence_refs. Cero observado y desconocido son distintos. El validator de CLOSED_SUMMARY sólo comprueba net y que net_basis no sea vacío; por tanto el mapper debe cumplir la semántica congelada y los oráculos deben probar estados no válidos, aunque la validación actual sea más laxa.

Hallazgo coordinado con investigador de fuente: TradeList actual obtiene net de Order.PL, coloca el agregado Order.CommSwap en commission y pone swap=0. Ese cero normalizado **no acredita swap cero** ni desglose de comisión. Preservar el agregado y el artefacto fuente; declarar commission/swap UNKNOWN si falta desglose real. No dividir ni asignar todo a comisión por conveniencia. El payload fuente inspeccionado por ese investigador no trae moneda, FX o Q_i: cualquier declaración configurada necesita evidencia y semántica explícitas, o se degrada a REGISTER_ONLY/fallo según política.

QISealV2 exige monto positivo, moneda, semantic, método y versión, sealed_at, decision_ref, policy_digest, evidence_ref SHA256 y coverage. Sólo CYCLE_BUDGET + WHOLE_CYCLE y sello causal no posterior a primera exposición habilitan R/10k. FIRST_ENTRY_RISK/TICKET_INITIAL_RISK/DECLARED_UNACCREDITED no equivalen a presupuesto de ciclo. La validación shape del DTO y la acreditación analítica no son el mismo gate.

FX no forma parte de HistoryInputV2; el motor analítico tiene un perfil explícito de tasas con par, factor positivo, fecha efectiva, sello, método y evidencia. Default es NO_FX; no convertir en Forge para hacer comparables curvas. Un rate futuro se rechaza. Sin FX, money puede conservar series por moneda y el agregado ser NOT_COMPARABLE.

No usar métricas de riesgo agregadas para fabricar Q_i. Con neto/moneda/tiempos reales pero sin Q_i, puede existir curva de dinero y estados de insuficiencia para perfiles R/10k. Ese resultado honesto es diferente de cuatro curvas completas acreditadas.

## 5. Metadata y métricas fuente: extensión mínima

El contrato actual aporta identidad básica, paquete/version, histories y refs de provenance. No hay campo tipado para indicadores, parámetros enriquecidos, resultados mensuales, SPP o valores de MetricSet fuente.

Ya existen `MetricSetV1`, `MetricV1`, `MetricValue`, `MetricFormula`, `MetricCalculator`, `MetricDefaults`, `MetricCoverage` y `NamedRef` dentro del módulo compartido. Evaluar reutilización de esos tipos en SourceEvidenceV2 cuando la fuente tenga sus semánticas completas; no duplicar structs de métricas ni inventar formula/catalog/currency para forzar ese formato.

Estados existentes útiles: COMPUTED, NOT_COMPARABLE, INVALID_INPUT, UNKNOWN e INSUFFICIENT. COMPUTED exige valor finito; estados desconocidos/no comparables prohíben resultado decimal. Las métricas deben conservar key fuente, unidad, basis, fórmula/calculador y scope exacto cuando se conozcan; una cifra fuente sin equivalencia demostrada nunca se registra como métrica calculada de The Lab.

Extensión recomendada al Architect (decisión de diseño, no existente):
- Un bloque opcional y tipado SourceEvidenceV2 para metadata descriptiva acreditada y referencias/valores de métricas fuente.
- Evaluación/MetricSet/TradeSet/artifact refs y digests exactos; disponibilidad y motivos por dimensión.
- Participa en request digest y snapshot persistido de evidencia; queda fuera de StrategyVersionRef y de los resultados analíticos.
- REGISTER_ONLY admite histories=[] si no hay historia económica; distinguir ausencia de trades frente a conjunto cero trades observado por cobertura acreditada.
- Parser, validator, digest, persisted readback y docs del consumidor en un solo módulo publicado.

**Persistencia a no asumir:** accepted_snapshot actual de `strategy_ingestion_receipts` contiene sólo IngestionReceiptV2, no el request. El request canónico va a V2ArtifactStore cuando está configurado y su digest a accepted_body_artifact. History-level provenance no se inserta en columna separada del history/revision en el servicio revisado; operation provenance sí. La nueva evidencia necesita una superficie de persistencia/readback explícita sobre los stores existentes. El constructor permite art=nil; no usar esa modalidad como prueba de provenance íntegra.

## 6. HTTP, auth, aceptación y revisiones Echo

Fuentes:
- [Gateway V2](https://github.com/xKoRx/echo/blob/f93cd4f80085e328f9176c1215e42e6c8e0b2404/v3/gateway/internal/lab_v4_gateway.go)
- [HistoryServiceV2](https://github.com/xKoRx/echo/blob/f93cd4f80085e328f9176c1215e42e6c8e0b2404/v3/sdk/postgres/strategy_history_v2_service.go)
- [PUT HistoryV2](https://github.com/xKoRx/echo/blob/f93cd4f80085e328f9176c1215e42e6c8e0b2404/v3/sdk/postgres/strategy_history_v2_put.go)

### 6.1 POST y GET

POST exacto `/api/v2/strategy-ingestions`; Content-Type application/json sin parámetros; encoding identity; Idempotency-Key 1..128 bytes [A-Za-z0-9._:-]. Body limitado por configuración del gateway, profundidad/duplicadas/UTF-8/trailing y wire checks.

Auth exige producer_ingest; namespace y writer proceden de la identidad del token. Body.producer_ref debe igualar writer. 401 sin identidad; 403 identidad/role no autorizado. La key remota pertenece a (namespace,writer,key), no al body ni al filename.

Aceptación:
1. Valida identidad, modo y DTO, canoniza, recomputa request/version/definition digests.
2. Consulta receipt por scope+key+digest; conflicto de digest → 409.
3. Write-ahead del request canónico cuando hay artifact store.
4. Transacción única: advisory lock de receipt scope+key; reconsulta; mapping/version/definition; metadata versional; locks ordenados de historias; revisión/heads; accepted receipt; history_dirty_outbox.
5. Commit, 202 nuevo receipt; 200 replay.

GET `/api/v2/strategy-ingestions/by-key/{key}` y `/{receipt_id}` requieren el mismo scope writer. Ausente o ajeno → 404 sin filtrar existencia. Ambos devuelven accepted_snapshot, no estados actuales recalculados.

### 6.2 Receipt real y validación requerida

IngestionReceiptV2 está actualmente definido en sdk/postgres (no en sdk/contracts). Lleva receipt_id, schema_version, request_digest, accepted_at, acceptance, strategy_ref, strategy_version_ref, runtime_strategy_id, histories, binding_ref opcional, snapshots operational/analytics y links. **No lleva producer_ref ni namespace**.

Cada HistoryReceiptV2 contiene history_id, history_ref, revision, digest (revision_digest), content_digest, operation_count, movement_count, unchanged.

El productor debe cotejar:
- schema literal, receipt UUID, accepted_at válido, acceptance exacto.
- request_digest obligatorio y exactamente igual al manifest.
- strategy/version esperados (aceptar UUID asignada sólo cuando el request no la conocía; sellarla una vez).
- conjunto exacto de history IDs sin faltantes/duplicados/extras; content digest, counts y revision digest según creación/replay.
- history_ref calculable con namespace/writer/version/historia para acreditar scope esperado.
- snapshots operacionales separados y nunca READY inferido de aceptación.

Mover/compartir el DTO de receipt y su validator canónico en sdk/contracts es una mejora cohesionada si se toca esta superficie; no crear una copia de struct en cada consumidor.

### 6.3 Hallazgos Echo concretos

**ECHO-R1 — Digest de history reutilizada incorrecto.** `acceptOneHistoryV2`, líneas 440–444: para contenido igual al head retorna `Digest: headContent`; el campo documentado es revision_digest y se había cargado headDigest. Se reproduce por nuevo POST/key que converge a historia ya existente, no por replay del mismo receipt que vuelve temprano. Fix local: devolver headDigest y probar ambos casos con expected digests independientes.

**ECHO-R2 — Strict decoder incompleto.** `DecodeStrategyIngestionV2` hace `d.BindRequired("histories",&e.Histories)`; `wire.Decoded.Bind` usa json.Unmarshal sin DisallowUnknownFields. La historia standalone sí usa strictUnmarshalV2. Un unknown dentro de history/operation puede descartarse durante decoding del envelope, pese al comentario de estrictez; esto puede alterar el digest calculado desde typed envelope respecto al wire enviado. Corregir usando el mismo decoder estricto, no otro serializer. Oráculo nested unknowns obligatorio.

**ECHO-R3 — Reutilización existing_ref y metadata.** Riesgo source detallado en §3.3; necesita gate focalizado que demuestre no degradación.

### 6.4 Corrección de evidencia e histories existentes

POST sólo crea historia o acepta contenido igual. Contenido distinto en la misma identidad → HISTORY_EXISTS (409), aun con key nueva. La nueva key no autoriza sobrescribir.

Existe `PUT /api/v2/strategy-versions/{version_ref}/histories/{history_id}`:
- Idempotency-Key obligatorio.
- history completa; expected_revision/digest; If-Match opcional pero si está presente debe coincidir.
- Sin precondición → 428; stale → 412.
- Wrapper opcional history + pareja version_temporal_metadata/expected_metadata_revision.
- Correcciones y retractions explícitas, snapshot siguiente y cadena de digests.
- GET de esa ruta devuelve head y revisiones retenidas.

El adapter Forge actual sólo implementa POST y GET receipt. El Architect debe congelar cómo representar una revisión corregida: método adicional en el mismo adapter para el protocolo existente, o resultado tipado REVISION_REQUIRED hasta que la capability sea implementada dentro del scope aprobado. Nunca renombrar historia ni reintentar eternamente POST con nuevos IDs.

### 6.5 Registro y operacionalidad

En `AcceptIngestionV2` líneas 174–179, PROVISION_REFERENCE produce OPERATIONAL_PROVISIONING_NOT_AVAILABLE sin condición de config y antes de writes. Esto sólo describe el POST de ingesta.

El gateway sí dispone de `POST /api/v2/strategy-versions/{version_ref}/operational-bindings`, resolver de DeploymentProfile y grants server-side, assertions, CAS y `ProvisionBindingTx`, con link `/api/v2/operational-bindings/{binding_ref}/readiness`. Puede sustentar las regresiones operacionales previas sin contradecir el rechazo del modo integrado. Esta task puede limitarse a REGISTER_ONLY y rechazar configuración de provisioning que no tenga un camino completo autorizado. No invoca trading ni declara readiness.

## 7. Forge: persistir, publicar, recuperar

Fuentes:
- [HTTPIngressV2](https://github.com/xKoRx/symphony/blob/22f337ca434549c492b2d402fd158e23ac4758a8/sqx/adapters/echo-handoff/http_ingress_v2.go)
- [ControlPlane V2](https://github.com/xKoRx/symphony/blob/22f337ca434549c492b2d402fd158e23ac4758a8/sqx/adapters/registry-postgres/ingestion_v2_persistence.go)
- [Migración 017](https://github.com/xKoRx/symphony/blob/22f337ca434549c492b2d402fd158e23ac4758a8/sqx/adapters/registry-postgres/migrations/017_ingestion_v2_persistence.up.sql)
- [CLI](https://github.com/xKoRx/symphony/blob/22f337ca434549c492b2d402fd158e23ac4758a8/sqx/cmd/echo-ingest-v2/main.go)

### 7.1 Comportamiento existente útil

Config exige baseURL y bearer; store obligatorio; timeout default 130s. Ingest valida envelope/key, json.Marshal, CanonicalJSONV2Digest, LoadManifest, conflicto local por mismo key/digest distinto, SaveManifest antes de POST. Load errors no equivalen a ausencia.

202/200 → validateReceiptV2; 400/403/409/422 → REJECTED; los demás status/errores de transporte → GET-by-key. Esto incluye 401/413/415 como ambiguos en la implementación actual, por lo que la clasificación HTTP debe afinarse con el contrato del servidor.

Persistencia:
- `sqx.handoff_manifests_v2`: idempotency_key PK global, request_digest, canonical_body jsonb, source/artifact refs, wave_key, strategy/version refs, decision_ref y created_at.
- `UNIQUE(decision_ref,version_ref)` permanece en V2. Comentarios del adapter dicen separarse de esa restricción histórica, pero el SQL realmente la conserva.
- deliveries_v2 tiene estados heredados: HANDOFF_CREATED, INGESTED, CONTRACT_CONFLICT, SOURCE_BINDING_CONFLICT, UNAVAILABLE, UNKNOWN_RECEIPT; receipt jsonb, last_error, attempts y updated_at.
- INGEST_ACCEPTED se mapea a INGESTED; REJECTED se mapea a CONTRACT_CONFLICT. No existe persistencia de razón tipada para distinguir todas las causas funcionales.

### 7.2 Findings de corrección mínima

| ID | Defecto de source | Consecuencia / corrección requerida |
|---|---|---|
| FORGE-R1 | validateReceiptV2 acepta request_digest vacío, producer_ref vacío y acceptance vacío; sólo exige refs no vacías y alguna history con id/digest | Puede aceptar receipt ajeno/incompleto. Validación compartida exacta del §6.2; no exigir producer_ref mientras servidor no lo emita; acreditar scope por contrato explícito. |
| FORGE-R2 | GET recovery 200 guarda receipt con strategy/version argumentos vacíos y no asigna refs/operational en manifest | Recuperación aparenta aceptación sin refs tipadas; aplicar la misma rutina de validación y persistencia de POST y GET. |
| FORGE-R3 | reconcileUnknown ante error HTTP o GET!=200 cambia estado sólo en memoria | Restart pierde UNKNOWN; persistir transición y causa en todos los paths ambiguos, incluso cancel/timeout con una vía de persistencia acotada apropiada. |
| FORGE-R4 | SQL UpdateReceipt sólo permite salir de UNKNOWN hacia UNKNOWN | Receipt válido posterior no puede converger a INGESTED. Permitir sólo transición verificada UNKNOWN→INGESTED; conservar key/body y evidencia. |
| FORGE-R5 | LoadManifest no reconstruye SchemaVersion, ProducerRef ni Operational | Recovery debilita scope checks; restaurar invariantes del canonical body + columnas apropiadas y comprobar digest. |
| FORGE-R6 | Error de UPDATE strategy/version refs ignorado; entrega y refs no atómicos | Puede retornar éxito con refs perdidas. Transacción atómica y propagación de error. |
| FORGE-R7 | Ingest entrega siempre POST incluso si manifest cargado ya es INGEST_ACCEPTED o UNKNOWN | Falta camino de recovery prioritario. Terminal aceptado reutiliza resultado; UNKNOWN reconcilia GET antes de repetir mismo POST. |
| FORGE-R8 | PK local por key sin destino/scope; migración conserva UNIQUE(decision_ref,version_ref); Ingest deja version_ref vacío hasta receipt | Riesgo de colisión entre destinos y estrategias del lote. Persistir destino lógico + namespace/writer y versión calculada antes de red; definir cardinalidad de binding para revisiones/cohort. No fabricar decision refs arbitrarios. |
| FORGE-R9 | canonical_body se crea con json.Marshal y se guarda jsonb | El nombre promete bytes canónicos pero PostgreSQL normaliza representación. Usar CanonicalJSONV2 y guardar/reconstruir bytes canónicos de manera determinista con comprobación de digest. |
| FORGE-R10 | 64 MiB limitReader de receipt ignora read error; sin clasificación fuerte de error JSON | Leer receipt acotado, validar EOF/tamaño, preservar UNKNOWN si respuesta incompleta después de posible commit. |
| FORGE-R11 | Métodos UpdateReceipt de terminal hacen read-check y luego UPDATE; dos aceptaciones concurrentes pueden tener ganador entre ambos | Perdedor recibe error aunque receipt idéntico. Convergencia transaccional/relectura del ganador requerida en test de carrera real. |

El helper RetryBackoffV1 no ejecuta retries; el CLI llama una vez. Su jitter usa enteros y hasta aproximadamente ±40% para ciertos delays, pese al comentario ±20%, y limita attempt a 10, no tiempo global real. Si se reutiliza, corregir el helper; preferir política Temporal existente configurable y budget total real. No escribir otra infraestructura de retry.

El CLI usa `ArtifactDigest: "file:<path>"`, no un hash de contenido, y defaults sintéticos para WaveKey/DecisionRef. Es un entrypoint de harness, no fuente válida de lineage para la task nativa.

### 7.3 Invariantes que debe congelar la task

- Resolver y sellar una selección exacta de cohort/evidencia antes de preparar entregas, con una entrega aislada por estrategia/version/intención.
- Key determinista de la intención durable y destino/scope; nunca incluir attempt, wall-clock o UUID de retry.
- Preparar envelope con SDK, Validate y strict roundtrip; canonicalizar; computar digests una vez; persistir manifest antes de red.
- Tras manifest, recuperar desde el manifest sellado sin exigir releer Mongo para reconstruir un cuerpo posiblemente cambiado.
- Persistir resultado/receipt y refs atómicamente; ningún error de DB permite declarar éxito.
- Timeout, worker restart o crash después de POST → GET-by-key mismo scope; 404 sólo indica receipt no observado, no rechazo.
- Mismo key con distinto cuerpo → conflicto local; no POST.
- Corrección real de fuente → nueva intención explícita, mismo StrategyVersion si paquete no cambió, protocolo de revisión de historia cuando corresponda.
- Concurrencia de ejecuciones duplicadas debe converger al mismo manifest/receipt con arbitraje SQL, no last-writer-wins.
- Resultados tipados separan entregada, rechazada, pendiente/recuperable y outcome desconocido; readiness y analytics independientes.

## 8. The Lab: automático existente y límites de certificación

Fuentes:
- [Lab analysis service](https://github.com/xKoRx/echo/blob/f93cd4f80085e328f9176c1215e42e6c8e0b2404/v3/sdk/postgres/lab_analysis_service.go)
- [AnalysisWorkerV4](https://github.com/xKoRx/echo/blob/f93cd4f80085e328f9176c1215e42e6c8e0b2404/v3/lab-worker/internal/workers/analysis_worker_v4.go)
- [Timeline/curves](https://github.com/xKoRx/echo/blob/f93cd4f80085e328f9176c1215e42e6c8e0b2404/v3/sdk/lab/analyze/timeline.go)
- [FX](https://github.com/xKoRx/echo/blob/f93cd4f80085e328f9176c1215e42e6c8e0b2404/v3/sdk/lab/analyze/fx.go)
- [Worker main](https://github.com/xKoRx/echo/blob/f93cd4f80085e328f9176c1215e42e6c8e0b2404/v3/lab-worker/cmd/labv4-worker/main.go)

El POST inserta dirty outbox por historia en la misma transacción. RelayDirtyOutbox convierte eventos a analysis_targets/dependencies; worker reclama dos targets por pasada con lease/fencing, carga revisión exacta, calcula cuatro perfiles, publica generación por CAS y después rankings de cohortes si RankingRepo está presente. El main de labv4-worker lo configura. No hay necesidad de disparar cálculo síncrono desde Forge/HTTP.

Cuatro perfiles:
- recorded_money.v1
- r_net_cumulative.v1
- normalized_10k_open_balance.v1
- normalized_10k_initial_balance.v1

Los defaults analíticos del worker son capital normalizado 10000 y riesgo 0.01; no son economía fuente ni autorizan introducir Q_i. FXRates default nil = NO_FX.

El projector journal→history está en el mismo binario pero tiene presupuesto/loop separados y se activa con LABV4_PROJECTOR_NAMESPACE. La importación Forge ya ingresa HistoryRevision directamente; no requiere falsificar hechos Echo journal ni crear otro projector.

### Findings C focalizados

**LAB-C1 — Cobertura fuente no aplicada.** `loadHistoryEvents` consulta operaciones/movimientos, pero no coverage de strategy_history_revisions. En líneas 645–650 deriva la ventana de min/max días de actividad y fija CoveredThroughNS=WindowToNS. Así DailyBinsCovered puede recibir una cobertura completa aunque la fuente haya declarado GAP/PARTIAL. Debe probarse y corregirse el loader mínimo para preservar calendario/cobertura declarados; ningún cambio en Forge debe inventar COMPLETE.

**LAB-C2 — Estado de moneda no viaja al motor.** Los SELECT del loader leen currency/net_currency, no currency_status, y TimelineEvent sólo porta Currency. Una moneda UNPROVEN puede llegar sin esa distinción. La task no debe explotar este comportamiento; exigir evidencia/declaración honesta y probar no comparabilidad/insuficiencia para UNPROVEN.

**LAB-C3 — Tiempo desconocido puede convertirse en epoch zero.** Al insertar movements, ausencia de economic time termina con ecoNS=0; loader coalesce de opened/closed/known times también usa 0. Timeline trata KnownAtNS==0 como conocido desde siempre. El estado TimeEvidence está en canonical JSON pero no gobierna ese camino. Oráculo focalizado: UNKNOWN no produce hecho ocurrido en epoch ni conocimiento retrospectivo inventado. Requerir economía temporal acreditada para la historia publicable y mostrar insuficiencia en los otros casos.

**LAB-C4 — Cero observado vs falta de datos.** computeRecordedMoney con cero series conserva READY sin puntos. Esto puede ser correcto para un conjunto observado vacío con cobertura; no acredita ausencia de historia. La extensión REGISTER_ONLY cero historias debe dejar estado de análisis no disponible, sin una curva vacía presentada como económica.

**LAB-C5 — Profiles declarados no aplicados.** El servicio no consume RequestedCurveProfiles y relay fija default_bundle. La task debe evitar ofrecer un control que el consumidor ignora.

Estos findings no niegan la existencia del motor; delimitan qué debe falsificar el gate C y qué correcciones locales son atribuibles a esta integración.

## 9. Reutilización y oráculos obligatorios

### 9.1 Tests/activos existentes útiles (inspeccionados o inventariados; no ejecutados)

- contracts/strategy_ingestion_v2_test.go: ValidateAndDigest, RejectsUnknownField (top-level), RejectsDuplicateKey, UnionExclusive, NonCanonicalDecimal, HistoryLimits.
- contracts/strategy_history_v2_test.go y strategy_history_v2_closure_test.go: Q_i, money, time, movement/operation/history branches y recetas de digest.
- contracts/wire/canonicalize_direct_diff_test.go: DirectEqualsLegacy Edge/Marshaler/SharedPointers/Random.
- contracts/v2_common_test.go y wire hash/canonicalization tests.
- sdk/postgres/strategy_history_v2_service_test.go y closure: receipt/guards/read paths.
- sdk/postgres/strategy_ingestion_v2_registry_closure_test.go y w6fix_ingestion_identity_test.go: identidad/version/concurrencia.
- gateway/internal/lab_v4_e01_e02_test.go, lab_v4_gateway_test.go y shot4_s3a01_s3a02_regression_test.go.
- lab-worker/workerstest/cycle_e2e_test.go, w3_service_paths_test.go, w3_race_test.go, w4_ranking_test.go, wperf_golden_digests_test.go.
- Symphony http_ingress_v2_test.go sólo usa mirror httptest + store memoria. No es prueba de Gateway real ni ControlPlane.

Limitación decisiva del test Forge actual: el fixture usa definition hash fijo sin calcular el digest del manifest; la respuesta tiene history_id distinto al request y versión arbitraria, pero la validación actual los acepta. Reutilizar estructura, reemplazar esos oráculos por valores independientes y ejecutar contra el gateway real del harness. No presentar ese test como interoperabilidad.

### 9.2 Matriz mínima de falsificación

| Oráculo | Resultado exigido |
|---|---|
| Nuevo tag, cache limpio y GOWORK=off en dos consumidores | Mismo módulo publicado y checksums; builds independientes reproducibles, sin replace-only |
| Golden legacy y temporal UNKNOWN | Misma serialización canónica/ref/digest servidor-productor; errores idénticos cuando inválido |
| Unknown anidado history/operation; claves duplicadas; null; decimals no canónicos | Rechazo antes de persistir/red o cero efectos Echo |
| REGISTER_ONLY con métricas agregadas y cero histories | Estrategia/version/source evidence registradas; ninguna historia/curva económica inventada |
| Identidad mismo nombre/distinto ref; alias/source ref adicional | Aislamiento por identidad real; convergencia sólo bajo fingerprint/ref acreditados |
| Manifest persistido y crash antes de POST | Recovery publica mismo destino/scope/key/body; una aceptación |
| POST commit exitoso + timeout antes de receipt | GET-by-key recupera receipt/ref/count/digests exactos, sin segunda identidad |
| GET 404 o fallo de red | UNKNOWN durable, pendiente recuperable; no rechazo |
| Receipt ausente/corrupto/digest vacío/mismatch/foreign history/count incorrecto | No INGEST_ACCEPTED; UNKNOWN o conflicto tipado según prueba; error persistido |
| UNKNOWN durable → receipt válido | Transición a INGESTED con refs y evidence atómicas |
| Mismo key distinto contenido | Conflicto local antes de HTTP |
| Dos executions mismo key/body simultáneas | Un manifest/receipt; ambas convergen con resultado idéntico |
| Dos estrategias del mismo cohort/decision | Ninguna colisión de version_ref vacío ni corrupción cruzada |
| Error DB al actualizar refs/receipt | No éxito; recovery posible con manifest intacto |
| Mongo cae tras manifest | Recovery no reconstruye request desde fuente; usa bytes sellados |
| Fuente corregida misma historia | POST no sobrescribe; revisión explícita con CAS o resultado revision-required, sin ID arbitrario |
| POST nuevo key, historia idéntica ya presente | Digest del receipt = revision_digest real, content_digest separado, counts correctos |
| Existing_ref sin redeclarar tiempos | Metadata versional conservada |
| CommSwap combinado / swap normalizado 0 | UNKNOWN del desglose; cero sólo con evidencia; sin doble conteo |
| Sin Q_i; riesgo de ticket; sello posterior | Money según datos; R/10k insuficientes con razones, ningún Q_i inferido |
| Monedas distintas sin FX / tasa futura | NOT_COMPARABLE/insuficiencia por perfil; no conversión implícita |
| Coverage GAP/PARTIAL frente a COMPLETE; cero trades observado frente a ausencia | Sin Sharpe/ranking fabricado ni continuidad temporal inferida |
| Outbox→worker→generación→rank/screener | Readback de refs/revisión/inputs y estados reales; receipt no sustituye esta prueba |
| source_folder renombrado con mismos bindings | Misma selección, semántica y contenido; ruta opaca |

### 9.3 Gates de evidencia

A Functional Contract: resolver, mapper tipado, nueva task conectada a Temporal, persistencia y recovery. Puede verificarse con fixtures tipados y harness local.

B Echo Ingestion E2E: productor real usando contrato publicado, gateway real y readback de mapping/version/history/receipt con digests. HTTP 202 por sí solo no basta.

C The Lab E2E: outbox y worker funcionando; generación de cuatro perfiles con estados honestos, métricas, rankings/screener coherentes con suficiencia. Datos insuficientes no equivalen a FAIL del mapper, pero tampoco a cuatro curvas completas.

D Authentic Forge Source: source evidence y artefactos reales de ejecución/export autorizado con hashes y bindings exactos; no se demuestra con mocks. Si no existe fuente autorizada, BLOCKED_EXTERNAL explícito y continuar A/B/C fixture.

E Release/Deploy: posterior, separado y sujeto a autorización; no se ejecutó ni certificó aquí.

## 10. Mejora propuesta y cierre de investigación

Candidatos concretos:
1. Publicar el contrato único desde Echo, actualizando pin y compatibilidad en ambos consumidores.
2. Ampliación aditiva SourceEvidence tipado y REGISTER_ONLY sin histories; persistencia/readback explícitos.
3. Endurecer y compartir DTO/validator de receipts; arreglar digest de history reutilizada.
4. Cerrar las rutas de recovery y atomicidad del adapter/store existentes; scope/destino y binding cardinality correctos.
5. Reutilizar PUT CAS para revisión o declarar capability no soportada con resultado tipado; nunca suplantarla con nuevas identidades.
6. Oráculos C y correcciones mínimas del loader para cobertura/moneda/tiempo cuando el gate demuestre pérdida de evidencia.

Ningún código de producto fue modificado. Los archivos en contract-source son copias de lectura por SHA para la revisión del manager. No se ejecutaron tests ni cold builds y no se afirma PASS de runtime. No se cerró Agents-OS.

La investigación entrega evidencia suficiente para que el Architect congele una implementación aditiva y el manager adjudique los gaps. Los bloqueos de implementación/release enumerados no convierten la investigación completada en certificación de producto.

## Apéndice — Delta estrecho del workstream Runtime/Lab recién integrado

Revisión adicional pedida por el manager, limitada a los archivos de contratos/receipt, HistoryService/PUT, loader Lab y adapter/persistencia Forge. **No cambia las bases propuestas, no autoriza integración, merge ni despliegue.** No se ejecutaron builds, tests ni runtime.

Refs documentales comparadas:

- Echo `feature/echo-runtime-lab-v4-integration` en `2daa58daddfbebaf57e2d1c934a25ec644bf0a94`, frente a `f93cd4f80085e328f9176c1215e42e6c8e0b2404`.
- Symphony `feature/echo-runtime-lab-v4-integration` en `3dfaa5facb96fcc297c062c46ca77085f882cc1c`, frente a `22f337ca434549c492b2d402fd158e23ac4758a8`.

Los árboles Git recuperados no estaban truncados. Comparación de blobs:

| Archivo | Baseline | Workstream nuevo | Resultado |
|---|---|---|---|
| Echo contracts/strategy_ingestion_v2.go | c1af8852a9495f2777aad3da6a349cffef532e57 | mismo | Sin cambio |
| Echo contracts/strategy_history_v2.go | a69a7dd0d1e3cd873584069b2d72ac93b51603e8 | mismo | Sin cambio |
| Echo contracts/v2_common.go | 79713e344f5df53d3945da09a87d5c668092dc8b | mismo | Sin cambio |
| Echo postgres/strategy_history_v2_service.go | 1a64de5a292916b9596103b390c88640a209d605 | d58ee4e94606760f03176c693bcd6cb703eb926f | Artefactos reales de historia/metadata |
| Echo postgres/strategy_history_v2_put.go | 3077962c6a7c7791ca4e47b0c6226bf5315c764c | 52fe5b7a061205c5a45626925f1cc46cd6f3a15f | Reutiliza helpers de artefactos |
| Echo postgres/lab_analysis_service.go | 4ac9afdbc8026765d1701b854eb13f6d49e991ed | mismo | Sin cambio |
| Echo gateway/internal/lab_v4_gateway.go | 3cb6083aaf443b9a63ed8307fbda2c709f054caf | mismo | Sin cambio |
| Forge echo-handoff/http_ingress_v2.go | 056a359f42ffcc21b467ee2af4ddd4c0013aee16 | mismo | Sin cambio |
| Forge registry-postgres/ingestion_v2_persistence.go | 489ec2084b5570cd53bff3422804f89c1b8ed421 | mismo | Sin cambio |
| Forge migration017 | b68564163baa4e04448a7937d0c842ddeb18bd87 | mismo | Sin cambio |
| Forge sqx/go.mod | 6f9fc4ef6545ba1ab65dad38578081d5f5cfc017 | mismo | Pin sin cambio |

No aparece un archivo de receipt nuevo en contracts y el DTO sigue en HistoryServiceV2 sin los campos compartidos/scope propuestos por este addendum.

**Port mínimo candidato, pendiente de adjudicación:** el servicio nuevo añade `writeCanonicalArtifactV2` y `writeArtifactBytesV2`. Canoniza cada HistoryInput, escribe los bytes por SHA256 antes de la transacción y entrega ese digest a insertRevisionV2 como canonical_artifact. Hace lo propio con temporal metadata; PUT usa los mismos helpers. Esto sustituye los refs sintéticos derivados de history/version por direcciones reales de bytes reconstruibles y evita duplicar esa corrección en el nuevo programa.

La función aún devuelve un digest cuando `art == nil`; sólo se cambió el comentario del constructor para limitar ese modo a fixtures aislados. **El mandato de implementación debe exigir `art != nil` en la ruta certificada** y demostrar write-ahead/readback por hash; portar los helpers no cierra por sí solo ese gate.

Permanecen los demás findings relevantes: receipt Digest=headContent en historia unchanged, existing_ref con metadata no declarada, guard de provisioning integrado, decoder/pin, coverage/currency/time del loader y todas las rutas Forge de recovery/persistencia. No repetir una implementación de artefactos que ya existe, pero tampoco afirmar que estos commits corrigieron los otros defectos.

Fuentes del delta:

- [HistoryService nuevo](https://github.com/xKoRx/echo/blob/2daa58daddfbebaf57e2d1c934a25ec644bf0a94/v3/sdk/postgres/strategy_history_v2_service.go).
- [History PUT nuevo](https://github.com/xKoRx/echo/blob/2daa58daddfbebaf57e2d1c934a25ec644bf0a94/v3/sdk/postgres/strategy_history_v2_put.go).
- [Forge adapter sin cambio](https://github.com/xKoRx/symphony/blob/3dfaa5facb96fcc297c062c46ca77085f882cc1c/sqx/adapters/echo-handoff/http_ingress_v2.go).
- [Forge persistencia sin cambio](https://github.com/xKoRx/symphony/blob/3dfaa5facb96fcc297c062c46ca77085f882cc1c/sqx/adapters/registry-postgres/ingestion_v2_persistence.go).

## Fuentes

- Paths, commits y blobs fijados en el informe y su apéndice de comparación concurrente.
- [[B — Frozen Design]] y [[10-projects/Echo/Ingestion V2 — Operational Integration/Forge Task — Contract Addendum|Forge Task — Contract Addendum]].
