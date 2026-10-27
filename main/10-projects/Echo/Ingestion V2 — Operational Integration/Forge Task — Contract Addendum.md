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

# Forge Task — Contract Addendum

## Propósito

Autoridad del delta compartido Echo que habilita la nueva task declarativa Forge, con compatibilidad explícita y preservación de hechos fuente.

## Contenido

**Estado:** CONTRACT_DESIGN_FROZEN para este programa; implementación y distribución pendientes.  
**Autor:** GOD Architect independiente, SHOT 1.  
**Fecha:** 2026-10-27.  
**Autoridad canónica:** proyecto Echo existente en Agents-OS; diseño adjudicado por el Primary Manager el 2026-10-27.  
**Límite:** este texto diseña cambios; no afirma implementación, publicación de módulo, build ni prueba ejecutada. El diseño de la task Forge referencia este addendum sin duplicar sus decisiones.

## 1. Motivo y autoridad

El mandato Owner requiere registro de estrategia, definición, metadata, métricas fuente e historias cuando estén acreditadas, con un único contrato compartido y The Lab como autoridad analítica. El candidato Echo f93cd4f80085e328f9176c1215e42e6c8e0b2404 ya tiene el servicio V2, registry, histories, dirty outbox, Lab y readiness. Este addendum amplía únicamente las superficies que la nueva task necesita y corrige defectos concretos encontrados en ese recorrido.

Fuentes primarias:

- [Contrato de ingesta](https://github.com/xKoRx/echo/blob/f93cd4f80085e328f9176c1215e42e6c8e0b2404/v3/sdk/contracts/strategy_ingestion_v2.go).
- [Contrato de historia](https://github.com/xKoRx/echo/blob/f93cd4f80085e328f9176c1215e42e6c8e0b2404/v3/sdk/contracts/strategy_history_v2.go).
- [Métricas compartidas](https://github.com/xKoRx/echo/blob/f93cd4f80085e328f9176c1215e42e6c8e0b2404/v3/sdk/contracts/analytics.go).
- [Aceptación y receipts](https://github.com/xKoRx/echo/blob/f93cd4f80085e328f9176c1215e42e6c8e0b2404/v3/sdk/postgres/strategy_history_v2_service.go).
- [Versiones y registry](https://github.com/xKoRx/echo/blob/f93cd4f80085e328f9176c1215e42e6c8e0b2404/v3/sdk/postgres/strategy_ingestion_v2_registry.go).
- [Carga Lab](https://github.com/xKoRx/echo/blob/f93cd4f80085e328f9176c1215e42e6c8e0b2404/v3/sdk/postgres/lab_analysis_service.go).
- Informe de evidencia separado: [[10-projects/Echo Forge — Operación Real V2/artifacts/forge-echo-ingestion-task-v2/evidence/Contract Source Review|Contract Source Review]], §§2–8; observaciones de código, no certificación física.

## 2. Distribución: una autoridad, un pin nuevo

Symphony 22f337ca consume `github.com/xKoRx/echo/v3/sdk/contracts v0.0.1-lab-v4-shot2.1`. El tag real `v3/sdk/contracts/v0.0.1-lab-v4-shot2.1` apunta a 52f8d509e0e9127a9f263f02d76565dae508a2f6, y su subtree contracts es 4aa8b383…; el subtree del candidato Echo es d579adbd…. Cambian decoder, temporal metadata, canonicalización y firmas de métodos de digest. El pin actual no representa el consumidor candidato.

Decisión congelada:

1. Implementar este addendum una sola vez en `echo/v3/sdk/contracts`, sobre el candidato Echo acordado.
2. Publicar un tag nuevo del submódulo; nombre reservado para esta entrega: `v3/sdk/contracts/v0.0.1-forge-ingestion-task.1`. El nombre no acredita disponibilidad: registrar SHA de commit, objeto tag, subtree y go.sum cuando exista.
3. Fijar Symphony al tag nuevo, sin un replace local hacia Echo Contracts. Echo SDK/Gateway/worker deben consumir exactamente ese contenido; un go.work local que lo seleccione debe cotejarse contra el tag y no sustituye un build frío.
4. Resolver también el replace brownfield de Symphony hacia `../../sdk` en el manifest de build: el checkout SDK debe estar fijado al SHA publicado correspondiente, o retirarse el replace para el build de certificación. No aceptar un SDK local desconocido.
5. Golden corpus único con bytes, errores y digests esperados, versionado junto al contrato. Cada consumidor lo corre independientemente. Los goldens no pueden generarse en el test con la misma función que se está verificando.

**Compatibilidad:** campos nuevos opcionales no cambian bytes/digests de requests antiguos cuando no aparecen. La ampliación de cero historias conserva el schema strategy-ingestion.v2 y se habilita sólo en REGISTER_ONLY. Fixes de estrictez rechazan campos que nunca formaron parte del contrato. Documentar el cambio de firmas del candidato y adaptar call sites, sin reintroducir serializers paralelos.

## 3. Registro sin historia económica

### 3.1 Regla wire

`histories` continúa siendo un array requerido. La cardinalidad pasa a:

- REGISTER_ONLY explícito: 0..8.
- Cualquier modo que requiera historia: 1..8, además de sus requisitos propios.
- No se usa null, historia placeholder, operación ficticia ni cobertura fabricada.
- Una historia con operations=[] sólo representa un TradeSet realmente EMPTY y su cobertura acreditada; no representa ausencia de extracción.

Una versión/definición acreditada y la identidad de estrategia siguen siendo obligatorias. REGISTER_ONLY no autoriza una versión inventada.

### 3.2 Persistencia y consulta

La transacción existente crea/verifica registry, StrategyVersion y definición/crosswalk. Con histories=[]:

- No crea History ni HistoryRevision.
- No emite history_dirty_outbox para una historia inexistente.
- Receipt acceptance = INGEST_ACCEPTED.
- El perfil POST nativo exige `source_evidence.history_availability` cuando histories=[]: MISSING se corresponde con NO_HISTORY; NOT_REQUESTED con HISTORY_NOT_REQUESTED. AVAILABLE o PARTIAL con cero historias es inconsistente y se rechaza.
- Snapshot analytics.state = INSUFFICIENT_DATA y reason_codes=[NO_HISTORY] o [HISTORY_NOT_REQUESTED] según esa correspondencia. Ese estado y reason_codes son una extensión explícita del snapshot actual.
- Operational.state = NOT_REQUESTED para REGISTER_ONLY; ninguna aceptación se convierte en READY.
- Registry y screener deben poder mostrar la StrategyVersion y metadata sin una History/analysis generation. Usar el registry existente como raíz y un join opcional al análisis, o la proyección existente equivalente. No crear historia para satisfacer un inner join.
- Rank, score y curvas quedan ausentes; el UI muestra el motivo de insuficiencia. No inventar rank=0, score=0 o curva plana.

La corrección de la consulta/presentación de no-history es parte de B/C; no puede dejarse como una limitación externa después de que el servicio acepte correctamente el registro.

## 4. SourceEvidenceV2: extensión tipada y acotada

### 4.1 Campo y responsabilidad

Añadir `source_evidence,omitempty` a StrategyIngestionV2, con tipo compartido `SourceEvidenceV2`. Añadir el mismo tipo a IngestionReceiptV2 para conservarlo en accepted_snapshot y devolverlo por GET-by-id/by-key. La representación completa del request sigue en el artifact store canónico.

SourceEvidence conserva hechos fuente y su autoridad. No se escribe en los resultados de métricas/curvas/rankings Lab y no participa en StrategyVersionRef. Sí participa en el request digest y su propia huella canónica.

### 4.2 Estructura concreta

Los siguientes nombres/JSON tags definen el delta; el código de SHOT 2 los implementará en contracts, sin importar Symphony:

| Tipo | Campos |
|---|---|
| SourceEvidenceV2 | schema_version literal `strategy-source-evidence.v1`; sources []SourceEvaluationEvidenceV2; history_availability SourceAvailabilityV2 |
| SourceAvailabilityV2 | state `AVAILABLE\|PARTIAL\|MISSING\|NOT_REQUESTED`; reason_codes []string; evidence_refs []NamedRef |
| SourceEvaluationEvidenceV2 | source_system; source_instance_ref; strategy_ref; flow_run_ref; stage_execution_ref; evaluation_ref; evaluation_digest; producer Producer; stage; producer_contract_version; task_path/task_name opcionales acreditados; variant; run_ref opcional; sample_type/result_key/cell_key opcionales; metadata SourceStrategyMetadataV2; metric_sets []SourceMetricSetEvidenceV2; trade_sets []SourceTradeSetEvidenceV2; artifacts []SourceArtifactEvidenceV2 |
| SourceStrategyMetadataV2 | availability SourceAvailabilityV2; instrument_ids []string; timeframe; direction; entry_indicators/price_indicators/exit_indicators/entry_blocks/exit_blocks []string; parameters []SourceParameterV2; evidence_refs []NamedRef |
| SourceParameterV2 | block; name; value_text; evidence_ref. `value_text` preserva el literal fuente; no promete un tipo numérico inferido. |
| SourceMetricSetEvidenceV2 | metric_set_ref; evaluation_ref; content_digest; scope_digest; catalog_version/calculator_id/calculator_version/formula_set_digest opcionales sólo cuando existen; values []SourceMetricEvidenceV2; evidence_refs []NamedRef |
| SourceMetricEvidenceV2 | key; status MetricStatus existente; value *MetricValue existente; unit/basis opcionales; comparability MetricComparability existente; formula *MetricFormula existente opcional; availability SourceAvailabilityV2; evidence_refs []NamedRef |
| SourceTradeSetEvidenceV2 | trade_set_ref; evaluation_ref; content_digest; scope_digest; parser_id/parser_version; normalized_schema_version; status `COMPLETE\|EMPTY\|INVALID`; record_count/closed_trade_count/invalid_record_count como strings decimales canónicos no negativos; source_scope SourceTradeScopeV2; payload_artifact SourceArtifactEvidenceV2; evidence_refs []NamedRef |
| SourceTradeScopeV2 | stage; variant; sample_type; run_ref; result_key; cell_key opcional; configured_from/configured_to opcionales como TimeEvidenceV2; currency_evidence opcional; timezone_evidence opcional. Sólo valores acreditados; no rellenar campos para simular completitud. |
| SourceArtifactEvidenceV2 | role `INPUT\|OUTPUT\|EVIDENCE\|DEFINITION`; kind; artifact ArtifactRef existente (incluye Size como string decimal canónico); evidence_refs []NamedRef |

`variant` sólo transporta el identificador semántico explícito que el productor realmente tenga. Si el productor conserva una configuración variante más rica, ésta queda en su artefacto/hash acreditado; no convertir un JSON arbitrario en identidad derivada.

Reglas:

- `sources` es no vacío y ordenado determinísticamente por la tupla (evaluation_ref, source_system, source_instance_ref); tuplas duplicadas se rechazan. metric_sets y trade_sets se ordenan por su ref; values por key. Los parámetros conservan el literal acreditado y un orden estable (block, name, evidence_ref); pares contradictorios no se sobrescriben.
- Los conteos nuevos usan el helper existente de enteros canónicos no negativos: sin signo positivo, exponentes, fracciones ni ceros iniciales salvo "0"; rango int64 y límites efectivos del consumidor. record_count cuenta registros normalizados del payload; invalid_record_count cuenta registros fuente rechazados y no se suma como si fuera subconjunto del payload. La coherencia se contrasta con el schema del productor y el parseo completo. No hay size_bytes duplicado: ArtifactRef.Size es la única autoridad wire de tamaño.
- Los campos descriptivos son opcionales cuando no existe evidencia; direction usa *DirectionV2 y sólo LONG/SHORT/BOTH. No se introduce UNKNOWN dentro de ese enum. availability y reason_codes explican las ausencias, y evidence_refs identifica los valores presentes.
- Todas las refs padre/hijo se contrastan en Forge. Echo valida forma, claves y coherencia del bloque, sin consultar Mongo Forge.
- Los ids de ref no se reconstruyen desde labels. SourceEvidence puede conservar refs opacas de otros productores válidos sin que Echo conozca sus modelos internos.
- Misma metric_set_ref o trade_set_ref con distinto digest en el request: rechazo.
- SourceMetricEvidence usa MetricValue/MetricStatus/MetricComparability existentes. No copiar MetricV1/MetricSetV1.
- MetricV1 exige fórmula, unit y basis acreditados; si faltan no se fabrica un MetricV1 completo. Una cifra SQX observada puede ser COMPUTED con comparability UNKNOWN y availability AVAILABLE. UNKNOWN/INSUFFICIENT sin medición no lleva value.
- Un cero sólo es valor si el documento fuente acredita presencia. Un zero-value Go producido por campo ausente no acredita medición.
- Ausencia de unit, formula o equivalencia analítica debe ser motivo explícito; no inventar catálogo/fórmula/versiones.
- Metadatos distintos de evaluaciones distintas permanecen separados. No hacer “merge del último campo no vacío”.
- Controles de tamaño: presupuesto SourceEvidence configurable del consumidor, techo de request efectivo y límite 64 provenance inputs vigente. No elevar silenciosamente límites para pasar un fixture.
- Las entradas top-level provenance.inputs condensan las autoridades raíz y su digest dentro del límite 64; el bloque tipado conserva hijos. Si no cabe, error explícito; no truncar lineage.

El descriptor currency_evidence es el tipo compartido `SourceCurrencyEvidenceV2{currency,state,evidence_ref}`, state OBSERVED o DECLARED, con ref obligatoria. Se mapea a MoneyV2.CurrencyStatus y MoneyV2.EvidenceRef sin elevar DECLARED a OBSERVED. Si no existe dato acreditado se omite este descriptor; no admite moneda inventada. timezone_evidence usa exclusivamente `SourceTimezoneEvidenceV2{timezone,omitempty,state,evidence_ref,omitempty,reason_code,omitempty}`: OBSERVED/DECLARED requieren timezone y evidence_ref; UNKNOWN requiere timezone ausente y reason_code. TimeEvidenceV2 se reserva para instantes.

Toda declaración configurada de moneda o timezone debe estar vinculada de forma durable y verificable a la evaluación/TradeSet seleccionado y cotejarse con sus artefactos. El destino Echo, el símbolo y una cuenta implícita no son autoridad para esos campos. Una contradicción entre declaración y fuente se rechaza.

### 4.3 Dónde se conserva

Extender el receipt compartido con `source_evidence` y `source_evidence_digest`. Congelar `SourceEvidenceDigestV2(x) = DigestTagged("echo-strategy-source-evidence.v1", x)`, usando el bloque tipado completo y CanonicalJSONV2/echo-wire-json.v1 compartidos; el digest no se incluye dentro de x. La receta D existente usa HashTagged(tag, string(canonical_bytes)); no crear otra receta con separadores propios. El código existente serializa fullReceipt en `echo.strategy_ingestion_receipts.accepted_snapshot`: esa misma transacción conservará el bloque nuevo. No se crea una tabla de metadata fuente paralela.

El artifact store de request canónico debe ser obligatorio para este recorrido de producción/harness certificado. El constructor con art=nil no puede acreditar preservación de provenance y se rechaza al componer la ruta nativa certificada. El workstream paralelo Echo 2daa58daddfbebaf57e2d1c934a25ec644bf0a94 ya contiene writeCanonicalArtifactV2/writeArtifactBytesV2 en el servicio y PUT de historias: reutilizar ese fix mediante port mínimo, sin merge general ni adoptar su tolerancia art=nil. El request exacto se verifica por digest antes de commit.

GET-by-id/by-key devolverá la evidencia del accepted_snapshot, incluyendo refs y valores. La consulta de detalle de StrategyVersion debe enlazar la ingesta aceptada correspondiente mediante referencias existentes o un selector explícito de receipt; no elegir “el último snapshot fuente” por timestamp. Si hay múltiples ingestas, devolver sus referencias como alternativas y conservar el source seleccionado. El screener usa sólo identidad/metadata apropiadas; ninguna métrica fuente se presenta en columnas de métrica Lab sin equivalencia demostrada.

## 5. Receipt compartido y comprobación

Mover los tipos actuales IngestionReceiptV2, HistoryReceiptV2, OperationalSnapshotV2, AnalyticsSnapshotV2 y ProfileReceiptV2 de sdk/postgres a sdk/contracts. Dejar aliases en postgres si evitan churn de imports; la definición real y decoder/validator están una vez en contracts.

Ampliar receipt con registry_namespace, producer_writer, producer_ref e idempotency_key, iguales al scope autenticado/aceptado y la key recibida. registry_namespace procede de AuthV2.Namespace; producer_writer=producer_ref=AuthV2.Writer, nunca de campos no contrastados del body. Esto es necesario especialmente para histories=[] donde no hay HistoryRef calculable que pruebe scope. Incluir SourceEvidence y sus digests cuando exista. Añadir reason_codes al analytics snapshot para ausencia/insuficiencia.

Un decoder compartido y estricto sirve a todos los receipts; la validación semántica se selecciona explícitamente por perfil. `ValidateNativeIngestionReceiptV2` corresponde al POST nativo de este programa y su GET/recovery. El perfil PUT conserva HISTORY_PUT_ACCEPTED y sus campos aplicables; los snapshots históricos tienen su propio perfil de compatibilidad. No aplicar las exigencias nuevas de POST indiscriminadamente a PUT ni convertirlas en opcionales para el POST nativo.

La validación del receipt nativo compara, sin campos opcionalmente vacíos:

1. schema, receipt_id UUID, accepted_at canónico, acceptance exacta.
2. Namespace, writer/producer, idempotency scope configurados.
3. request_digest exacto del manifest inmutable.
4. strategy_ref conocida o UUID asignada una vez; nunca sustituir una StrategyRef Forge por la UUID Echo.
5. strategy_version_ref esperada calculada antes del POST o existing_ref exacta.
6. Conjunto exacto de history_id, sin duplicados/faltantes/extras; vacío sólo si el request lo era.
7. Cada history_ref por HistoryRefV2; content_digest y revision_digest; counts exactos. Nuevo POST creación espera revisión 1; historia preexistente idéntica verifica la revisión exacta indicada por el receipt y su readback cuando sea necesario, sin asumir siempre revisión 1 ni comparar con un head que pudo avanzar después.
8. SourceEvidence/digest exactos cuando se solicitaron.
9. Operational/analytics son snapshots de aceptación, no estado vivo; su presencia no acredita readiness ni cálculos terminados.

GET-by-key usa exactamente el mismo decoder/validator que POST. Nunca aceptar una respuesta sólo porque es HTTP 200.

Compatibilidad histórica: un receipt viejo sin nuevos campos no certifica este nuevo perfil nativo. Puede mantenerse su lectura histórica por el protocolo previo. No reescribir snapshots inmutables antiguos para hacerlos parecer nuevos. Los keys nuevos incluyen versión de mapping; no dependen de receipts legacy incompletos.

## 6. Fixes mínimos de consumidor incluidos en SHOT 2

| ID | Cambio concreto | Oráculo |
|---|---|---|
| EC-01 | Decoder del envelope llama el decoder estricto de HistoryInputV2 para cada historia; strictness también en operaciones/bloques nuevos. | Unknown anidado, duplicado, trailing y decimal no canónico: error común, cero writes. |
| EC-02 | `acceptOneHistoryV2` usa headDigest como revision digest cuando contenido ya existe; devuelve conteos reales también en rama unchanged. | Nueva key/mismo contenido y replay misma key devuelven refs/digests/counts verificados independientemente. |
| EC-03 | ExistingRef conserva metadata temporal versional existente cuando no se redeclara; no la sustituye por UNKNOWN de otra historia. | Ingesta seguida de existing_ref sin tiempos no degrada hechos previos. |
| EC-04 | Validar enums/semántica CostDisclosure y total de movimientos por historia, no sólo por operación; usar contrato compartido. | Valores de costes inválidos y suma >1,000,000 fallan antes de persistir. |
| EC-05 | Permitir 0 historias sólo registro, persistir metadata y dar readback/screener sin historia. | Registry visible, cero History/Revision/outbox ficticios, ausencia de curva/rank explícita. |
| EC-06 | Carga Lab conserva coverage COMPLETE/PARTIAL/GAP, ventanas/calendario y moneda/status acreditados; no sustituye coverage por min/max de actividad. | Mismos trades, distinta cobertura: estados y métricas justificables distintos. |
| EC-07 | Desconocido temporal no se transforma en epoch ni “conocido desde siempre”; loader conserva estado o rechaza como insuficiente. | UNKNOWN economic/known_at no crea punto en 1970 ni look-ahead. |
| EC-08 | Pin/distribución+receipt shared+source_evidence+artifact requirement según §§2–5. | Cold builds y corpus golden cruzado, persist/reload. |

EC-06/07 corrigen propagación de evidencia a las capacidades analíticas existentes. No crean otro motor, no cambian fórmulas ni agregan portfolios.

`requested_curve_profiles` no es un control efectivo en el consumidor examinado; la task nueva lo omite y su config rechaza overrides de perfiles con UNSUPPORTED_CAPABILITY. El worker existente conserva su bundle de cuatro perfiles. No se anuncia una configuración que se ignora.

## 7. Versiones y definición SQX analítica

Las recetas existentes permanecen:

- sqx-v1: StrategyVersionRef sobre canonical_strategy_id, target_platform, executable/effective_inputs/runtime_context/dependencies hashes. Usar sólo la versión sellada acreditada.
- definition-v1: target_platform ANALYTIC, DefinitionContentDigest compartido sobre manifest tipado y ComputeVersionRef compartido. No equivale a ejecutable MT5 ni otorga readiness.
- existing_ref: referencia exacta que Echo verifica pertenece al namespace/estrategia correctos.

El nuevo productor Forge puede aportar un manifest `sqx-strategyfile.v1` cuyo contenido de identidad es exactamente:

```json
{
  "schema_version": "sqx-strategyfile.v1",
  "media_type": "application/xml",
  "document_sha256": "sha256:<hash-real-del-XML>",
  "document_encoding": "UTF-8",
  "document_xml": "<bytes-XML-exactos-representados-como-string>"
}
```

El decoder requiere UTF-8, root StrategyFile y estructura soportada. La serialización JSON canónica escapa el string, pero al decodificarlo recupera los mismos bytes XML. No canonicalizar XML ni quitar atributos/nombres/comentarios; cualquier cambio en XML produce nueva versión conservadoramente. ObjectKey, folder, .sqx hash, hora de lectura, métricas y source refs quedan fuera de este manifest y dentro de SourceEvidence/provenance.

El techo vigente es 262144 bytes del manifest JSON completo emitido, incluido wrapper y escapes de document_xml, después de canonicalización. Superarlo produce DEFINITION_TOO_LARGE aun cuando el XML sin escape sea menor a 256 KiB. Añadir golden en ese borde; no truncar, omitir el manifest obligatorio ni reemplazarlo por un hash vacío. Los bytes XML observados se conservan como artifact con hash y referencia, separados de la receta/manifest; su locator no participa en la identidad.

Esto prueba una definición analítica del documento observado, no la equivalencia de comportamiento con una instalación SQX ni con settings/lastSettings del backtest. Esas configuraciones pertenecen al contexto fuente de cada evaluación. Un source de forma no soportada debe aportar una definición explícita acreditada o recibir VERSION_DEFINITION_UNAVAILABLE.

## 8. Economía y temporalidad

- TradeList de resumen cerrado → CLOSED_SUMMARY; net único. Nunca crear movimientos para representar de nuevo ese mismo net.
- CommSwap combinado no acredita commission individual ni swap cero. Conservar el hecho combinado en SourceEvidence/provenance; commission/swap/fee/other_costs UNKNOWN salvo prueba específica. NetBasis PARTIAL_NET o UNKNOWN conforme al contrato del productor; NET_ALL_DECLARED_COSTS sólo si está acreditado.
- Currency observada o declarada con evidencia. No USD por símbolo ni XXX para pasar el validator. Historia presente sin moneda requerida es error de la estrategia; IF_AVAILABLE no oculta el defecto.
- Q_i ausente → qi omitido/missing_fields, perfiles R/10k INSUFFICIENT_DATA. No extraerlo de PnL, MAE, drawdown, SL actual o presupuesto virtual.
- No FX en Forge. Se preserva moneda; comparabilidad y FX pertenecen al perfil Lab existente.
- construction_at, cutoff y available_at desconocidos → TemporalMetadata UNKNOWN + reason_code. created_at de evidencia, sealed_at y receipt time no sustituyen esas dimensiones.
- Apertura/cierre no acreditados no se convierten en timestamps cero. Coverage de backtest declarada no se infiere de min/max de operaciones; intervalo de actividad no implica COMPLETE.
- Source facts de ciclos, fills y operaciones parciales sólo se mapean cuando un productor válido los acredita. TradeList v1 no los tiene; no fabricarlos.

## 9. Correcciones e idempotencia del consumidor

La task nativa se limita a CREATE_ONLY. El POST existente crea historias o acepta el mismo contenido. Si una misma identidad de historia cambia, el resultado es REVISION_REQUIRED; ni una key nueva ni un history_id aleatorio convierten una corrección en creación.

El protocolo de revisión ya existente es `PUT /api/v2/strategy-versions/{version_ref}/histories/{history_id}` con expected_revision/digest y CAS. No se implementa un cliente nuevo ni provisioning como parte de este programa. El oráculo debe demostrar 409 HISTORY_EXISTS, 428 sin precondición, 412 stale y preservación de la historia, aunque la task no ejecute PUT.

Una ejecución física distinta acreditada puede producir otra historia, con run/evaluation/scope distintos. Cambio de parser o corrección del mismo conjunto económico no debe cambiar su history_id. Si el productor no acredita si es nueva ejecución o corrección, fallar HISTORY_IDENTITY_UNPROVEN; no resolver por fecha o filename.

## 10. Gates del addendum

- A: construcción/validación/digests/errores y source snapshot tipado correctos.
- B: Gateway+PG+artifact store reales de harness, request productor, receipt y readback; no basta httptest espejo.
- C: worker Lab real, revisiones exactas, curvas/métricas/rankings/screener y estados de insuficiencia; no cuatro curvas inventadas.
- D: dataset físico auténtico de Forge con lineage/hashes/configuración acreditados, o BLOCKED_EXTERNAL demostrado.
- E: release/deploy separado, no autorizado por este diseño.

El corpus debe incluir: registro sin historia; EMPTY observado; net con moneda declarada; CommSwap combinado; Q_i ausente; FX no acreditado; cobertura PARTIAL/GAP; temporal UNKNOWN; identidad con labels iguales; multiple histories; replay; corrección rechazada; scopes distintos; receipt ajeno; módulo pin antiguo que falla la matriz.

## 11. Decisiones y pendientes

| Decisión | Fuente/motivo | Estado |
|---|---|---|
| Un pin compartido nuevo, sin structs duplicados | Tree diff/tag real, mandato §7 | Congelada; ejecución pendiente |
| Zero histories sólo REGISTER_ONLY | Requisito real de registro; validator actual 1..8 | Congelada por Manager; ejecución pendiente |
| SourceEvidence tipado en request+receipt snapshot | Campos fuente sin destino actual; snapshots existentes | Congelada; ejecución pendiente |
| SQX XML exacto definition-v1 ANALYTIC | Dos fixtures/repositorio + reader reutilizable | Congelada por Manager; prueba de implementación pendiente |
| Sin nuevo provisioning ni perfiles ignorados | Guard 503 y profiles no consumidos | Congelada; ejecución pendiente |
| Revision conflict explícito CREATE_ONLY | POST/PUT CAS existentes | Congelada por Manager; ejecución pendiente |
| Lab conserva cobertura/moneda/tiempo | Findings EC-06/07 | Fix delimitado incluido |
| Disponibilidad de tag nuevo, cold build, runtime real | No ejecutados en SHOT 1 | PENDING_EXECUTION |
| Fuente auténtica Owner actual | No se accedió infraestructura | UNKNOWN; afecta D, no excusa defectos de A/B/C |

**Freeze adjudicado por el Primary Manager tras revisión independiente. No FULL_CERTIFIED; no implementación/runtime acreditados en esta fase.**

## Fuentes

- [[10-projects/Echo Forge — Operación Real V2/artifacts/forge-echo-ingestion-task-v2/B — Frozen Design|B — Frozen Design]] y [[10-projects/Echo Forge — Operación Real V2/artifacts/forge-echo-ingestion-task-v2/evidence/Contract Source Review|Contract Source Review]] del programa Forge.
- Fuentes Echo fijadas por SHA al comienzo del addendum.
- [[F — Decision Register]] y [[Echo + Echo Forge — Environment Contract]].
