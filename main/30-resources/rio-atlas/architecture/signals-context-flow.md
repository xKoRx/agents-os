---
type: resource
schema_version: 1
status: active
area: "[[Meli]]"
project: "[[Crear Context]]"
sources:
  - "[[rio-playmaker]]"
  - "[[rio-sdk-events]]"
  - "[[ads-signals-frontend]]"
  - "[[rio-frontend]]"
  - "[[rio-controlplane-kafka]]"
  - "[[rio-controlplane-flink]]"
  - "[[rio-controlplane-clickhouse]]"
  - "[[rio-controlplane-fury]]"
  - "[[rio-materializer]]"
last_verified: 2026-08-19
confidence: high
aliases:
  - signals context flow
  - context of signals
  - contrato params outputs RIO
  - matriz I/O as-is RIO
cssclasses:
  - wide
tags:
  - kind/resource
created: 2026-08-11
updated: 2026-08-19
---

# RIO — fuente del I/O y matriz AS-IS por `component_type`

> [!info] Fuente canónica del [[00-index|RIO Atlas]]
> Auditoría forense del contrato que hoy cruza `parameters`/properties, control planes/materializer, resultados y `deployment.values`/`service.values`. Es discovery previo a la SPEC técnica de [[Crear Context]]: no diseña la solución futura, no cambia `parameters` y no supone que los CP consumirán `Context`.

## Síntesis vigente

**HECHO VERIFICADO.** No existe una fuente única vigente del I/O. El contrato efectivo es la intersección de builders del front, parsers de cada CP/materializer, output builders y persistencia opaca de Playmaker. `component_type_registry` no valida create/update/deploy, sus únicos seeds locales son parciales/stale y no se encontró publisher de capabilities implementado.

**HECHO VERIFICADO.** En HEAD actualizado, ambos paths resuelven placeholders. El pipeline nuevo llama `ParameterResolutionService.resolveComponentParameters` y éste ejecuta `DestinationParseService` + `ParametersParseService` antes de `parseParams`; el legacy conserva su resolver propio. Ambos leen `service.values` y desenvuelven `.value`. El output se mezcla con `putAll`, se elimina el viejo `deployment_uuid` y se serializa idéntico en `deployment.values` y `service.values`; no hay rename, flatten ni conversión de casing.

**HECHO VERIFICADO.** La realineación de SIG-573 conserva tres capas distintas: configuración cruda de `ComponentDefinition.parameters`, output productor crudo leído de `service.values` y valor consumidor final de `params`. `ParameterResolutionService.resolveWithMetadata` reúne resultado + facts en la misma pasada; `ComponentContextBuilder` no repite el lookup ni reconstruye un output desde el valor consumidor. La metadata incluye además `configuredPath → consumerPath`: `DestinationParseServiceImpl` puede descartar destinos malformados y reindexar el array, por lo que ambos paths no son intercambiables. Evidencia: `rio-playmaker/.../service/ParameterResolutionService.java`; `.../service/ParameterResolutionResult.java`; `.../impl/ParameterParseServiceImpl.java`; `.../impl/DestinationParseServiceImpl.java`; `.../service/ComponentContextBuilder.java`.

**INFERENCIA.** El conjunto mínimo elegible para Context v1 es el de las filas auditadas como input realmente leído u output realmente referenciado. Campos sólo visuales, outputs sin consumidor y tipos sin consumer demostrado no se copian; estos últimos quedan `UNSUPPORTED`.

**GAP.** Falta evidencia runtime para resolver aliases, versiones activas de templates storage y el rol efectivo de rutas catch-all. Tampoco se ubicó un call site de cifrado pre-dispatch que materialice la promesa del SDK de “sensitive values pre-encrypted”.

## Evidencia y provenance

Inspección `2026-08-19`; Graphify fue índice/selector y cada afirmación se confirmó en el source citado. La auditoría inicial se hizo sobre `8887122`; después de `git pull --ff-only`, Playmaker avanzó a `d1741b8` e incorporó el cambio de resolución del pipeline (`fa73018a`, 2026-08-11). El refresh final de refs remotas fue rechazado por el allowlist de red del owner; por eso la compatibilidad con `origin/feature/parse-params-pipeline`, `origin/develop` y `origin/master` se evaluó contra las refs locales disponibles y queda sujeta a revalidación. La rama vieja `origin/feature/parse-params` no existe localmente. Se leyeron los `AGENTS.md` aplicables. La rama de trabajo contiene la implementación de Context todavía sin commit; `graphify-out/` permanece ajeno y sin trackear.

| repo | branch | commit HEAD |
|---|---|---|
| rio-playmaker | feature/SIG-573-component-context (base develop) | `d1741b89ad64b19a1452be7e92d412fc88762c60` |
| rio-sdk-events | feature/SIG-573-component-context (base master) | `9d86eb8e85d32ad2e10b415a82bfe9dd2d9f3b5c` |
| ads-signals-frontend | develop | `32c7fa56fc35ed7acd0199d75d35e9714f6a41ad` |
| rio-frontend | develop | `6d644ec6a41766b1eeb1b3c07b7f865980ca2c07` |
| rio-controlplane-kafka | develop | `427d090d97e5f79d67a70d4da15fc6efd2457c92` |
| rio-controlplane-flink | develop | `7af7e3f8160357f1622e382bb6b1a312b8c40ef5` |
| rio-controlplane-clickhouse | develop | `a2ca40e477f121fcc2e71076aa00ddeadc8368c2` |
| rio-controlplane-fury | develop | `7eb7932e9f3fa9233fe1a0eb2959b297da968c5b` |
| rio-materializer | develop | `56ebada250403107c4df307a783bc6c72e5121c9` |
| rio-controlplane-kms | develop | `b7b522564d0c6274b34abe94a9de550926b52f56` |
| rio-controlplane-observability | develop | `43ca94b7495d529942150a20d28bb4847192f489` |
| rio-controlplane-signals | develop | `cd127524b24147748a0c43b9860018a0db2b3524` |
| ads-signals-catalog | develop | `67f11cc83c18688d508e7539b4c1ffe10e6f0989` |

## Tres paths efectivos

| path | cadena y params | routing/retorno |
|---|---|---|
| Pipeline nuevo | `PipelineDeploymentController` → `PipelineDeployServiceImpl` → `DeploymentGroupServiceImpl` → `BatchDispatchServiceImpl` → `ParameterResolutionService.resolveWithMetadata` → `DestinationParseService` → `ParametersParseService` → `parseParams` → `ComponentContextBuilder` → `DispatchRequest` → evento `AFTER_COMMIT` → adapter. Resuelve una vez y devuelve `resolvedParameters + references + paths`; captura el mismo output runtime usado por la sustitución y la correspondencia de paths generada por el filtrado/reindexación. JSON inválido u output faltante falla antes del request. Evidencia: `rio-playmaker/src/main/java/com/mercadolibre/rio/playmaker/service/pipeline/impl/BatchDispatchServiceImpl.java`; `.../service/ParameterResolutionService.java`; `.../service/ParameterResolutionResult.java` | `DispatchRequest` lleva `params` y Context como objetos separados. `BIG_QUEUE` sigue publicando exclusivamente `request.params()` en `DeploymentTriggerMessage`; `MaterializerRestAdapter` usa sólo IDs y tampoco envía Context. `.../service/pipeline/DispatchRequest.java`; `.../impl/BigQueueDispatchAdapter.java`; `.../impl/MaterializerRestAdapter.java` |
| Legacy/componente | `ComponentDeploymentController` → `DeploymentServiceImpl.dispatchViaBigQueue` → `resolveComponentParameters` → `DestinationParseServiceImpl` → `ParameterParseServiceImpl`. Resuelve referencias sólo en destinations activas y luego `${[dp.]component[env].property}` en el mapa. Lookup: service running → `service.values[key]`; Map → `.value`. `rio-playmaker/src/main/java/com/mercadolibre/rio/playmaker/service/impl/DeploymentServiceImpl.java:658-721,860-987`; `.../service/impl/DestinationParseServiceImpl.java:64-174`; `.../service/impl/ParameterParseServiceImpl.java:35-107,211-287` | El mismo routing puede mandar BigQueue o `createLegacy` a materializer. Persistir parameters crudos, resolver placeholders y validar contrato son acciones distintas. |
| Materializer | `MaterializerRestAdapter` ignora `DispatchRequest.params` y llama `doMaterialize(dpId, configId, serviceId, deploymentId)`; materializer recupera definición/template. `rio-playmaker/src/main/java/com/mercadolibre/rio/playmaker/service/pipeline/impl/MaterializerRestAdapter.java:35-54`; `rio-materializer/src/main/java/com/mercadolibre/rio/materializer/services/MaterializationService.java:279-305` | Factory rutea por execution engine; callback toma `materialization.result.values`. `rio-materializer/src/main/java/com/mercadolibre/rio/materializer/factories/impl/MaterializationPipelineFactory.java:312-405`; `.../mappers/NotificationMapper.java:29-59`; `.../handler/impl/MapResultTerraformHandler.java:29-65`; `.../handler/impl/MapResultCloudControllerHandler.java:31-79` |

`parseParams` llegó en commit `15f8b9026c` (2026-05-26). La auditoría sobre `8887122` veía sólo deserialización; el commit `fa73018a` (2026-08-11), presente tras actualizar a `d1741b8`, añadió la resolución compartida al pipeline. El resolver legacy permanece separado. La config `deployment-group.use-group` existe, pero el bypass fue removido en `DeploymentGroupServiceImpl.java:72`: es config stale.

## Context v1 implementado: alcance y semántica

| capa | dato preservado | fuente demostrada | regla anti-invención |
|---|---|---|---|
| configuración | `component.properties[consumer_path].configured_value`, `configured_path` y placeholder | hoja correspondiente en `ComponentDefinition.parameters` crudo; si el resolver reindexa `destinations[]`, el path sale de `ResolvedPath`, no del índice efectivo | sólo provenance; no sustituye al valor efectivo y no presupone `configured_path == consumer_path` |
| consumidor | `component.properties[path].value`, `value_type`, `consumer_path` | `params` post-resolución y post-deserialización | es exactamente el mapa que continúa hacia el adapter |
| productor | `sources|destinations[].outputs[output_path].value` y `runtime_value_path` | objeto crudo leído de `service.values` por la misma ejecución del resolver | no se crea si no existe `ResolvedReference`; wrappers se conservan y `.value` queda explícito en el path |
| mapping | placeholder, producer `output_path`, consumer `consumer_path`, fragmento sustituido y `resolved` | match concreto de esa pasada del resolver | alias se expresa con paths separados; igualdad de nombre/valor no es evidencia |
| clasificación | direction, sensitivity, JSON type, completeness/issues | matriz AS-IS o wrapper directo `{sensitive:true}` | metadata suplementaria; nunca reemplaza valores por enums/códigos; sin prueba de sensibilidad → `UNKNOWN` |

El shape está definido en `rio-sdk-events/.../context/ComponentContext.java`. La matriz conserva `14 AUDITADO`, pero la derivación ejecutable v1 cubre **13 tipos**: `aws-flink-sql-job` no tiene evidencia field-level suficiente para un contrato ejecutable y `gcp-kafka-topic` es GAP de routing, aunque otro CP tenga parser. Los demás tipos no hacen fallback a `putAll` y resultan `UNSUPPORTED`. La integración actual sólo crea Context en el path pipeline para `PROVISION`. Legacy/componente no usa `DispatchRequest`; el materializer directo tampoco. El adapter materializer del pipeline recibe un `DispatchRequest` con Context pero no lo consume ni lo envía. Por tanto, el contrato estructural v1 está definido, pero la cobertura de creación por request path sigue **PARCIAL**.

## Universo y cobertura

Unión de enums/registry/fallback del front, catálogo legacy, routing Playmaker, allowlists CP, templates materializer y seed registry.

| component_type | path/handler efectivo | clasificación | registry |
|---|---|---|---|
| `aws-flink-job` | BigQueue → Flink CP | AUDITADO | AUSENTE |
| `aws-flink-sql` | catch-all; Flink CP no acepta | GAP | AUSENTE |
| `aws-flink-sql-job` | catch-all → template materializer legacy | AUDITADO | AUSENTE |
| `aws-msk-topic` | BigQueue → Kafka CP; existe legacy materializer | AUDITADO | STALE |
| `bigqueue-signal` | catch-all → collector BigQueue | AUDITADO | AUSENTE |
| `bigqueue` | catch-all; factory cae a catalog | GAP | AUSENTE |
| `catalog-signal` | catch-all → catalog | AUDITADO | AUSENTE |
| `catalog` | catch-all/default catalog sin contrato explícito | GAP | AUSENTE |
| `clickhouse-mat-view` | BigQueue → ClickHouse CP | AUDITADO | AUSENTE |
| `clickhouse-matview` | front canónico; catch-all; CP rechaza alias | GAP | AUSENTE |
| `clickhouse-mergetree` | BigQueue → ClickHouse CP | AUDITADO | AUSENTE |
| `clickhouse-table` | front alias; catch-all; CP rechaza | GAP | AUSENTE |
| `collector-signal` | config Playmaker; sin handler exacto | GAP | AUSENTE |
| `example-connector` | ejemplo UI, no deploy productivo | NO APLICA | AUSENTE |
| `flink-job` | front canónico; catch-all; CP rechaza | GAP | AUSENTE |
| `flink-sql` | BigQueue → Flink CP | AUDITADO | AUSENTE |
| `fury-stream` | enum/front; sin handler exacto | GAP | AUSENTE |
| `fury-streams-kafka` | BigQueue → Fury outbound | AUDITADO | AUSENTE |
| `gcp-bucket` | front canónico; template local es `gcs-bucket` | GAP | AUSENTE |
| `gcp-kafka-topic` | Kafka CP acepta, Playmaker manda catch-all | GAP | STALE |
| `gcs-bucket` | catch-all → materializer | AUDITADO | AUSENTE |
| `kafka-fury-streams` | BigQueue → Fury inbound | AUDITADO | AUSENTE |
| `kafka-topic` | BigQueue → Kafka CP | AUDITADO | STALE |
| `pipeline-import` | acción UI, no componente | NO APLICA | AUSENTE |
| `s3-bucket` | catch-all → materializer | AUDITADO | AUSENTE |
| `signals-catalog-fury-app` | meta-template interno | NO APLICA | AUSENTE |
| `stream-signal` | catch-all → collector Stream | AUDITADO | AUSENTE |
| `stream` | catch-all; factory cae a catalog | GAP | AUSENTE |

Cobertura: `28/28`: `14 AUDITADO`, `11 GAP`, `3 NO APLICA`, `0 DEPRECADO`.

## Matriz principal — inputs realmente consumidos

Cada celda `campos` contiene una fila lógica `campo · tipo · regla`; no agrega campos entre sí. `P/U/D` = PROVISION/UPDATE/DEPROVISION. La dirección se basa en uso/relación, no en el nombre.

### Kafka

| component_type | op · dirección | input_key_path · tipo · required/default/validation | front · value kind | transformación · sensibilidad | registry · evidencia/gap |
|---|---|---|---|---|---|
| `aws-msk-topic` | P/U/D · both | `topic_name` · string · req, regex 1..249 | `kafkaTopicAdapter.toApiPayload` · literal/preset | prefijo env · identificador sensible | STALE · `rio-controlplane-kafka/src/main/java/com/mercadolibre/rio_controlplane_kafka/deployment/dto/KafkaParams.java:34-50`; `ads-signals-frontend/src/technologies/kafka-topic/adapter.ts:55-72` |
| `aws-msk-topic` | P/U · metadata | `partitions` · number · req ≥1 | adapter · default 3/custom | int · público | STALE · `KafkaParams.java:52-55`; front `adapter.ts:8-14` |
| `aws-msk-topic` | P/U · metadata | `replication_factor` · number · req ≥1 | adapter · default 2/custom | short · público | STALE · `KafkaParams.java:56-59` |
| `aws-msk-topic` | P/U · metadata | `retention_ms` · number|string · opt | adapter · default 86400000/custom | long; conflicto con `configs.retention.ms` · público | STALE · `KafkaParams.java:61-67,106-139` |
| `aws-msk-topic` | P/U · metadata | `configs` · map<string,string> · opt | no UI · custom | stringify · sensibilidad desconocida | STALE · `KafkaParams.java:86-103` |
| `aws-msk-topic` | P/U/D · metadata | `prefix_staging` · string | adapter · runtime/default | concatena nombre · identificador sensible | STALE · `rio-controlplane-kafka/src/main/java/com/mercadolibre/rio_controlplane_kafka/deployment/TopicNamePrefixer.java:34-77`; front `adapter.ts:46-58` |
| `aws-msk-topic` | P/U/D · metadata | `prefix_production` · string | adapter · runtime/default | concatena nombre · identificador sensible | STALE · mismos sources |
| `kafka-topic` | P/U/D · both | `topic_name` · string · req, regex | adapter · literal/preset | prefijo env · identificador sensible | STALE · `KafkaParams.java:34-50`; front `adapter.ts:55-72` |
| `kafka-topic` | P/U · metadata | `partitions` · number · req ≥1 | adapter · default 3/custom | int · público | STALE · `KafkaParams.java:52-55` |
| `kafka-topic` | P/U · metadata | `replication_factor` · number · req ≥1 | adapter · default 2/custom | short · público | STALE · `KafkaParams.java:56-59` |
| `kafka-topic` | P/U · metadata | `retention_ms` · number|string · opt | adapter · default/custom | long · público | STALE · `KafkaParams.java:106-139` |
| `kafka-topic` | P/U · metadata | `configs` · map<string,string> · opt | no UI · custom | stringify · desconocido | STALE · `KafkaParams.java:86-103` |
| `kafka-topic` | P/U/D · metadata | `prefix_staging` · string | adapter · runtime/default | prefijo · identificador sensible | STALE · `TopicNamePrefixer.java:34-77` |
| `kafka-topic` | P/U/D · metadata | `prefix_production` · string | adapter · runtime/default | prefijo · identificador sensible | STALE · mismo source |
| `gcp-kafka-topic` | P/U/D · both | `topic_name` · string · req, regex | `gcpKafkaTopicAdapter` · literal/preset | prefijo · identificador sensible | STALE · `rio-controlplane-kafka/src/main/java/com/mercadolibre/rio_controlplane_kafka/deployment/gcp/topic/GcpTopicParams.java:47-52,61-67,126-132`; front `.../gcp-kafka-topic/adapter.ts:8-37` · routing GAP |
| `gcp-kafka-topic` | P/U · metadata | `partitions` · number · req 1..max(default 1000) | adapter · default 3/custom | int · público | STALE · `GcpTopicParams.java:68-71`; `.../GcpTopicParamsValidator.java:22-56` |
| `gcp-kafka-topic` | P/U · metadata | `replication_factor` · number · opt CP default 2, 1..3 | adapter · UI default 3/custom | defaults divergen · público | STALE · `GcpTopicParams.java:58-83,111-123` |
| `gcp-kafka-topic` | P/U · metadata | `retention_ms` · number|string · opt, -1 o 1..max | adapter · default/custom | long · público | STALE · `GcpTopicParams.java:73-105`; validator `:22-56` |
| `gcp-kafka-topic` | P/U · metadata | `configs` · debe faltar/null | adapter spread · custom posible | rechazado · desconocido | STALE · `GcpTopicParams.java:86-90` |
| `gcp-kafka-topic` | P/U/D · metadata | `prefix_staging` · string | adapter · runtime/default | prefijo · identificador sensible | STALE · `TopicNamePrefixer.java:34-77`; front `gcp-kafka-topic/adapter.ts:27-37` |
| `gcp-kafka-topic` | P/U/D · metadata | `prefix_production` · string | adapter · runtime/default | prefijo · identificador sensible | STALE · mismos sources |

`name`, `description`, `source_environment_name` y `source_data_product_name` emitidos por `kafka-topic/adapter.ts:55-72` no son leídos por `KafkaParams`: front-only/no-I/O.

### Flink

El CP acepta exactamente `flink-sql` y `aws-flink-job` (`rio-controlplane-flink/src/main/java/com/mercadolibre/rio/controlplaneflink/model/FlinkComponentType.java:14-38`). La siguiente matriz expande por campo ambos contratos; aliases se muestran en la misma fila semántica.

| component_type | op · dirección | input_key_path · tipo · regla | front · kind | transformación/sensibilidad | evidencia/gap |
|---|---|---|---|---|---|
| `flink-sql` | P/U/D · metadata | `name`←`flink_app_name` string req | `flink-sql/adapter.ts:214-246` · literal | prefix env · id sensible | `rio-controlplane-flink/src/main/java/com/mercadolibre/rio/controlplaneflink/deployment/DeploymentTriggerMapper.java:44-149`; `.../dto/CreateFlinkAppDTO.java:454-490` |
| `flink-sql` | P/U · metadata | `fury_app`←`fury_app_name` string req | adapter · literal | descriptor · id sensible | `CreateFlinkAppDTO.java:493-524` |
| `flink-sql` | P/U · metadata | `fury_version`←`fury_app_version` string req | adapter · literal | rename · público | mismo source |
| `flink-sql` | P/U · metadata | `artifact_extension`←`fury_app_extension` string | adapter · default/custom | rename · público | mismo source |
| `flink-sql` | P/U · metadata | `runtime`←`flink_runtime` string req | adapter · preset/custom | runtime enrichment · público | `CreateFlinkAppDTO.java:221-246,454-490` |
| `flink-sql` | P/U · metadata | `log_level` string default INFO | adapter · default/custom | enum · público | `DeploymentTriggerMapper.java:44-149` |
| `flink-sql` | P/U · metadata | `metrics_level` string default OPERATOR | adapter · default/custom | enum · público | mismo source |
| `flink-sql` | P/U · metadata | `parallelism`←legacy integer default 1 | adapter · default/custom | alias · público | `CreateFlinkAppDTO.java:454-490` |
| `flink-sql` | P/U · metadata | `parallelism_per_kpu`←legacy integer | adapter · default/custom | alias · público | mismo source |
| `flink-sql` | P/U · metadata | `checkpointing_enabled`←`checkpoint` boolean | adapter · default/custom | alias/validación | `DeploymentTriggerMapper.java:44-149` |
| `flink-sql` | P/U · metadata | `checkpoint_interval_ms`←`checkpoint_interval` number | adapter · default/custom | alias/rango | mismo source |
| `flink-sql` | P/U · metadata | `min_pause_between_checkpoints_ms` number | adapter · default/custom | rango | mismo source |
| `flink-sql` | P/U · metadata | `snapshot_name` string opt | adapter · custom | id sensible | mismo source |
| `flink-sql` | P/U · metadata | `auto_scaling` boolean | adapter · default/custom | literal | mismo source |
| `flink-sql` | P/U · metadata | `start_app`←`start_application` boolean default true | adapter · default | alias | mismo source |
| `flink-sql` | P/U · metadata | `force_stop` boolean | adapter · custom | literal | mismo source |
| `flink-sql` | P/U · metadata | `rollback` object/boolean | adapter · custom | normalización · desconocido | mismo source |
| `flink-sql` | P/U · source/destination | `properties`←`properties_map` map<string,string> | `propertiesGenerator.ts:18-76` · placeholder/custom | `${component.outputKey}`; Playmaker resuelve, pero permanece el alias `properties_map`→`properties` del CP · sensibilidad desconocida | `CreateFlinkAppDTO.java:454-490` · GAP alias |
| `flink-sql` | P/U · metadata | `files[]` array | adapter · custom | descriptor · ids sensibles | `CreateFlinkAppDTO.java:493-524` |
| `flink-sql` | P/U · metadata | `criticality` string req | sin adapter exacto | inyecta tags component/environment/DP · público | `DeploymentTriggerMapper.java:44-149` · GAP fuente |
| `aws-flink-job` | P/U/D · metadata | `name`←`flink_app_name` string req | `flink-job/adapter.ts:281-305` · literal | prefix · id sensible | `DeploymentTriggerMapper.java:44-149`; `CreateFlinkAppDTO.java:454-490` |
| `aws-flink-job` | P/U · metadata | `fury_app`←`fury_app_name` string req | adapter · literal | descriptor · id sensible | `CreateFlinkAppDTO.java:493-524` |
| `aws-flink-job` | P/U · metadata | `fury_version`←`fury_app_version` string req | adapter · literal | rename · público | mismo source |
| `aws-flink-job` | P/U · metadata | `artifact_extension`←`fury_app_extension` string | adapter · default/custom | rename · público | mismo source |
| `aws-flink-job` | P/U · metadata | `runtime`←`flink_runtime` string req | adapter · preset/custom | enrichment · público | `CreateFlinkAppDTO.java:221-246,454-490` |
| `aws-flink-job` | P/U · metadata | `log_level` string default INFO | adapter · default/custom | enum | `DeploymentTriggerMapper.java:44-149` |
| `aws-flink-job` | P/U · metadata | `metrics_level` string default OPERATOR | adapter · default/custom | enum | mismo source |
| `aws-flink-job` | P/U · metadata | `parallelism`←legacy integer default 1 | adapter · default/custom | alias | `CreateFlinkAppDTO.java:454-490` |
| `aws-flink-job` | P/U · metadata | `parallelism_per_kpu`←legacy integer | adapter · default/custom | alias | mismo source |
| `aws-flink-job` | P/U · metadata | `checkpointing_enabled`←`checkpoint` boolean | adapter · default/custom | alias/validación | `DeploymentTriggerMapper.java:44-149` |
| `aws-flink-job` | P/U · metadata | `checkpoint_interval_ms`←`checkpoint_interval` number | adapter · default/custom | alias/rango | mismo source |
| `aws-flink-job` | P/U · metadata | `min_pause_between_checkpoints_ms` number | adapter · default/custom | rango | mismo source |
| `aws-flink-job` | P/U · metadata | `snapshot_name` string opt | adapter · custom | id sensible | mismo source |
| `aws-flink-job` | P/U · metadata | `auto_scaling` boolean | adapter · default/custom | literal | mismo source |
| `aws-flink-job` | P/U · metadata | `start_app`←`start_application` boolean default true | adapter · default | alias | mismo source |
| `aws-flink-job` | P/U · metadata | `force_stop` boolean | adapter · custom | literal | mismo source |
| `aws-flink-job` | P/U · metadata | `rollback` object/boolean | adapter · custom | normalización · desconocido | mismo source |
| `aws-flink-job` | P/U · source/destination | `properties`←`properties_map` map | `propertiesGenerator.ts:18-76` · placeholder/custom | Playmaker resuelve; alias de shape hacia el CP sigue sin contrato único · desconocido | `CreateFlinkAppDTO.java:454-490` · GAP alias |
| `aws-flink-job` | P/U · metadata | `files[]` array | adapter · custom | descriptor · ids sensibles | `CreateFlinkAppDTO.java:493-524` |
| `aws-flink-job` | P/U · metadata | `criticality` string req | sin adapter exacto | tags runtime | `DeploymentTriggerMapper.java:44-149` · GAP fuente |

### ClickHouse

`DeploymentTriggerMapper` convierte recursivamente snake→camel e inyecta `componentType` (`rio-controlplane-clickhouse/src/main/java/com/mercadolibre/rio/controlplane/clickhouse/deployment/adapter/rest/DeploymentTriggerMapper.java:15-31`). Campos pueden venir top-level o en `parameters`. `clickhouse-mat-view` sólo tiene command para P; U/D son GAP (`.../application/usecase/ProcessDeploymentUseCase.java:47-73,135-144`).

| component_type | op · dirección | input_key_path · tipo/regla | front · kind | transformación/sensibilidad | evidencia/gap |
|---|---|---|---|---|---|
| `clickhouse-mergetree` | P/U/D · metadata | `warehouse_name` string req | adapter `:337-386` · literal | camel · id sensible | `.../application/command/DeploymentDataExtractor.java:27-47,109-139` |
| `clickhouse-mergetree` | P/U/D · metadata | `schema_name` string req | adapter · literal | camel · id sensible | mismo source |
| `clickhouse-mergetree` | P/U/D · both | `table_name` string req | adapter · literal/preset | camel · id sensible | mismo source |
| `clickhouse-mergetree` | P/U · metadata | `engine_name` string req | adapter · preset/custom | camel · público | `DeploymentDataExtractor.java:156-345` |
| `clickhouse-mergetree` | P/U · metadata | `order_by` string/list | adapter · custom | camel · público | mismo source |
| `clickhouse-mergetree` | P/U · metadata | `primary_key` string/list opt | adapter · custom | camel · público | mismo source |
| `clickhouse-mergetree` | P/U · metadata | `partition_by` string/list opt | adapter · custom | camel · público | mismo source |
| `clickhouse-mergetree` | P/U · metadata | `ttl` string/object opt | adapter · custom | normaliza · público | mismo source |
| `clickhouse-mergetree` | P/U · metadata | `comment` string opt | adapter · custom | literal · público | mismo source |
| `clickhouse-mergetree` | P/U · metadata | `settings` map/list | adapter · custom | normaliza · desconocido | mismo source |
| `clickhouse-mergetree` | P/U · metadata | `table_fields[]` array req | adapter · custom | columnas · ids sensibles | mismo source |
| `clickhouse-mergetree` | P/U · metadata | `skip_indexes[]` array opt | adapter · custom | índices | mismo source |
| `clickhouse-mergetree` | D · metadata | `resource_type` string | front no verificado | camel | `.../command/DeleteResourceDeployment.java:41-64` · GAP |
| `clickhouse-mergetree` | D · secreto | `confirmation_token` string = `schema.table` | front no verificado | token operacional | mismo source · GAP |
| `clickhouse-mat-view` | P · source | `source_warehouse_name` string req | matview adapter `:206-231` · ref/lit | placeholder resuelto por Playmaker · id sensible | `DeploymentDataExtractor.java:68-85` |
| `clickhouse-mat-view` | P · source | `source_schema_name` string req | adapter · ref/lit | placeholder resuelto por Playmaker | mismo source |
| `clickhouse-mat-view` | P · source | `source_table_name` string req | adapter · ref/lit | usa `${X.table_created}` como nombre · MISMATCH | mismo source |
| `clickhouse-mat-view` | P · destination | `dest_warehouse_name` string req | adapter · ref/lit | placeholder resuelto por Playmaker | mismo source |
| `clickhouse-mat-view` | P · destination | `dest_schema_name` string req | adapter · ref/lit | placeholder resuelto por Playmaker | mismo source |
| `clickhouse-mat-view` | P · destination | `dest_table_name` string req | adapter · ref/lit | placeholder resuelto por Playmaker | mismo source |
| `clickhouse-mat-view` | P · both | `raw_sql` string req | adapter · custom/ref | tokens→`${X.schema_name/table_created}`; conserva SQL final y mappings por fragmento | mismo source |
| `clickhouse-mat-view` | P · metadata | `warehouse_name` string req | adapter · literal | camel · id sensible | `DeploymentDataExtractor.java:27-47,109-139` |
| `clickhouse-mat-view` | P · metadata | `schema_name` string req | adapter · literal | camel · id sensible | mismo source |
| `clickhouse-mat-view` | P · destination | `table_name` string req | adapter · literal | camel · id sensible | mismo source |

### Fury

| component_type | op · dirección | input_key_path · tipo/regla | front · kind | transformación/sensibilidad | evidencia/gap |
|---|---|---|---|---|---|
| `kafka-fury-streams` | P/U/D · source | `source.type` enum KAFKA | `fury-stream/adapter.ts:60-76` · preset | enum público | `rio-controlplane-fury/src/main/kotlin/com/mercadolibre/rio_controlplane_fury/pusher/model/SourceDescriptor.kt:46-79` |
| `kafka-fury-streams` | P/U/D · source | `source.name` string req/regex | adapter · preset/lit | topic id sensible | mismo source |
| `kafka-fury-streams` | P/U/D · source | `source.brokers` opt/ignorado | no emitido | inyectado config/runtime · id sensible | `SourceDescriptor.kt:46-79`; `.../PusherOrchestrator.kt:203-215` |
| `kafka-fury-streams` | P/U · source | `source.kafka_properties` map opt | no UI · custom | desconocido | `SourceDescriptor.kt:46-79` |
| `kafka-fury-streams` | P/U/D · destination | `destination.type` enum FURY_STREAMS | adapter · preset | enum | `.../model/DestinationDescriptor.kt:56-80` |
| `kafka-fury-streams` | P/U/D · destination | `destination.name` string req | adapter · literal | stream id sensible | mismo source |
| `kafka-fury-streams` | P/U/D · destination | `destination.application_name` string opt | adapter · preset | id sensible | mismo source |
| `kafka-fury-streams` | P/U · metadata | `input_rate_limit_rpm` int|string positivo opt | adapter · default/custom | int | `PusherOrchestrator.kt:967-1014` |
| `fury-streams-kafka` | P/U/D · source | `source.type` enum FURY_STREAMS | outbound adapter `:63-80` · preset | enum | `SourceDescriptor.kt:99-118` |
| `fury-streams-kafka` | P/U/D · source | `source.application_name` string req | adapter · literal | id sensible | mismo source |
| `fury-streams-kafka` | P/U/D · source | `source.name` string req | adapter · literal | id sensible | mismo source |
| `fury-streams-kafka` | P/U · source | `source.mappingId` string opt | runtime legacy | id sensible | mismo source |
| `fury-streams-kafka` | P/U · source | `source.sink_batch_size` int default 50, 1..100 | adapter · default/custom | snake/camel | mismo source |
| `fury-streams-kafka` | P/U/D · destination | `destination.type` enum KAFKA | adapter · preset | enum | `DestinationDescriptor.kt:87-101` |
| `fury-streams-kafka` | P/U/D · destination | `destination.name` string req | adapter · preset/lit | topic id sensible | mismo source |
| `fury-streams-kafka` | P/U/D · destination | `destination.brokers` opt/ignorado | no emitido | runtime config · id sensible | `DestinationDescriptor.kt:87-101`; `PusherOrchestrator.kt:485-498` |
| `fury-streams-kafka` | P/U · destination | `destination.kafka_properties` map opt | no UI · custom | desconocido | `DestinationDescriptor.kt:87-101` |
| `fury-streams-kafka` | P/U · metadata | `input_rate_limit_rpm` int|string positivo opt | adapter · default/custom | int | `PusherOrchestrator.kt:967-1014` |

Fury registra body y params completos (`rio-controlplane-fury/src/main/kotlin/com/mercadolibre/rio_controlplane_fury/controller/DeploymentTriggerController.kt:104-128`, CWE-532): riesgo probado, sin reproducir valores.

### Materializer

| component_type | op · dirección | input_key_path · tipo/regla | front · kind | transformación/sensibilidad | evidencia/gap |
|---|---|---|---|---|---|
| `catalog-signal` | P/U · metadata | `name` string req | catalog adapter `:172-204` · lit/preset | prefijos/id sensible | `rio-materializer/src/main/java/com/mercadolibre/rio/materializer/mappers/impl/SignalMapper.java:17-32` |
| `catalog-signal` | P/U · metadata | `display_name` string req | adapter · lit | público | mismo source |
| `catalog-signal` | P/U · metadata | `description` string | adapter · custom | público | mismo source |
| `catalog-signal` | P/U · metadata | `initiative` string | adapter · custom | id sensible | mismo source |
| `catalog-signal` | P/U · metadata | `system_id` string | no emitido | fuente GAP/id sensible | mismo source |
| `catalog-signal` | P/U · metadata | `criticality` string | adapter · custom | público | mismo source |
| `catalog-signal` | P/U · metadata | `identifier` string | adapter/runtime | DP+name/id sensible | mismo source |
| `catalog-signal` | P/U · metadata | `authorized_applications` array | adapter · custom | ids sensibles | mismo source |
| `catalog-signal` | P/U · metadata | `environment` string | no emitido | runtime no probado · GAP | mismo source |
| `catalog-signal` | P/U · metadata | `transport_type` string | adapter · preset | enum | mismo source |
| `catalog-signal` | P/U · destination | `destinations[].id` string | `destinationsBuilder.ts:19-125` · runtime | id sensible | `.../mappers/impl/DestinationMapper.java:33-118` |
| `catalog-signal` | P/U · destination | `destinations[].name` string | builder · runtime | exact component name | mismo source |
| `catalog-signal` | P/U · destination | `destinations[].type` enum | builder · preset | mapping | mismo source |
| `catalog-signal` | P/U · destination | `destinations[].destination_key` string | builder · placeholder | `${target.output}`; pipeline y legacy resuelven, con metadata de path exacta sólo en la implementación pipeline de Context | mismo source |
| `catalog-signal` | P/U · destination | `destinations[].active` boolean | builder · runtime | removed→false | mismo source |
| `catalog-signal` | P/U · destination | `destinations[].properties.brokers` string | builder · placeholder | `${target.servers}` | front `.../catalog-destinations-sync/componentMappings.ts:21-46` |
| `catalog-signal` | P/U · destination | `destinations[].properties.partitions` string/number | builder · literal | snapshot, no output | mismo front |
| `catalog-signal` | P/U · destination | `destinations[].properties.with_envelope` string | builder · default false | string boolean | mismo front |
| `bigqueue-signal` | P/U · both | `name` string req | bigqueue adapter · lit/preset | prefijo/id sensible | `rio-materializer/src/main/java/com/mercadolibre/rio/materializer/handler/impl/BuildBigQueueCollectorHandler.java:23-88` |
| `bigqueue-signal` | P/U · metadata | `criticality` string | adapter · custom | público | mismo source |
| `bigqueue-signal` | P/U · metadata | `ttl` number | adapter · default/custom | normaliza | mismo source |
| `bigqueue-signal` | P/U · metadata | `prl` number | adapter · default/custom | normaliza | mismo source |
| `bigqueue-signal` | P/U · metadata | `description` string | adapter · custom | público | mismo source |
| `bigqueue-signal` | P/U · metadata | `type` string | adapter · preset | enum | mismo source |
| `bigqueue-signal` | P/U · metadata | `visibility` string | adapter · preset/custom | enum | mismo source |
| `stream-signal` | P/U · both | `name` string req | stream adapter · lit/preset | prefijo/id sensible | `rio-materializer/src/main/java/com/mercadolibre/rio/materializer/handler/impl/BuildStreamCollectorHandler.java:20-50` |
| `stream-signal` | P · metadata | `description` string | adapter · custom | sólo create | mismo source |
| `stream-signal` | P/U · metadata | `retention_period_days` number | adapter · default/custom | normaliza | mismo source |
| `stream-signal` | P/U · metadata | `production_rate_limit_rpm` number | adapter · default/custom | normaliza | mismo source |
| `stream-signal` | P/U · metadata | `criticality` string | adapter · custom | público | mismo source |
| `s3-bucket` | P/U/D · destination | `bucket_name` string req template | S3 adapter `:108-126` · lit/preset | front v1 `bucket` vs template `bucket_name` · id sensible | `rio-materializer/src/main/resources/templates/ComponentTemplateAwsS3Bucket.json:10-69` · GAP versión |
| `s3-bucket` | P/U · metadata | `supported_region` string default readonly | runtime/default | template default | `ComponentTemplateAwsS3Bucket.json:10-57` |
| `s3-bucket` | P/U · metadata | `tags` map inyectado | runtime | enrichment/ids | mismo source |
| `gcs-bucket` | P/U/D · destination | `bucket_name` string req | front legacy · lit/preset | id sensible | `rio-materializer/src/main/resources/templates/ComponentTemplateGcsBucket.json:10-69` |
| `gcs-bucket` | P/U · metadata | `storage_class` string default | default/custom | enum | mismo source |
| `gcs-bucket` | P/U · metadata | `tags` map inyectado | runtime | enrichment/ids | mismo source |
| `aws-flink-sql-job` | P/U/D · metadata | contrato de template materializer | sin front exacto | bundled/runtime | `MaterializationPipelineFactory.java:707-760` · GAP field-level/runtime |

`throughput`, `payload_size` y `traffic_behavior` emitidos por `catalog-signal/adapter.ts:172-204` no son leídos por `SignalMapper`: front-only/no-I/O.

## Outputs reales → persistencia → consumidores

Regla común: output no-null → merge top-level → mismo JSON en `deployment.values` y `service.values`; wrappers permanecen. `rio-playmaker/src/main/java/com/mercadolibre/rio/playmaker/service/impl/DeploymentResultHandlerImpl.java:375-426`; `rio-sdk-events/src/main/java/com/mercadolibre/rio/sdk/events/deployment/DeploymentResultMessage.java:41-50`.

| component_type | op | output_key_path · tipo/wrapper | consumidor/ref y sensibilidad | evidencia · gap |
|---|---|---|---|---|
| `aws-msk-topic` | P/U | `topic_name` string | Flink/catalog `${X.topic_name}` · id sensible | `rio-controlplane-kafka/src/main/java/com/mercadolibre/rio_controlplane_kafka/provisioning/KafkaProvisioningServiceImpl.java:395-407` |
| `aws-msk-topic` | P/U | `servers` string | Flink/catalog `${X.servers}` · id sensible | mismo source |
| `aws-msk-topic` | P/U | `topic_id` string opt | no consumidor · id sensible | mismo source |
| `aws-msk-topic` | P/U | `partitions_size` number | no consumidor; catalog usa literal partitions | mismo source |
| `aws-msk-topic` | P/U | `replication_factor` number | no consumidor | mismo source |
| `aws-msk-topic` | P/U | `already_existed` boolean condicional | no consumidor | `KafkaProvisioningServiceImpl.java:324-328` |
| `aws-msk-topic` | D | `topic_name` string | no ref teardown · id sensible | `KafkaProvisioningServiceImpl.java:182-206` |
| `aws-msk-topic` | D | `deleted` boolean | no consumidor | mismo source |
| `aws-msk-topic` | D | `already_absent` boolean | no consumidor | mismo source |
| `kafka-topic` | P/U | `topic_name` string | Flink/catalog misma key · id sensible | `KafkaProvisioningServiceImpl.java:395-407` |
| `kafka-topic` | P/U | `servers` string | catalog nuevo usa servers; Flink espera `brokers` · MISMATCH/id sensible | mismo source; front `ads-signals-frontend/src/features/flink-properties-sync/componentMappings.ts:65-72` |
| `kafka-topic` | P/U | `topic_id` string opt | no consumidor · id sensible | mismo source |
| `kafka-topic` | P/U | `partitions_size` number | no consumidor | mismo source |
| `kafka-topic` | P/U | `replication_factor` number | no consumidor | mismo source |
| `kafka-topic` | P/U | `already_existed` boolean | no consumidor | `KafkaProvisioningServiceImpl.java:324-328` |
| `kafka-topic` | D | `topic_name` string | no ref teardown | `KafkaProvisioningServiceImpl.java:182-206` |
| `kafka-topic` | D | `deleted` boolean | no consumidor | mismo source |
| `kafka-topic` | D | `already_absent` boolean | no consumidor | mismo source |
| `gcp-kafka-topic` | P/U/D | `topic_name` string | mapping genérico posible · id sensible | `rio-controlplane-kafka/src/main/java/com/mercadolibre/rio_controlplane_kafka/deployment/gcp/topic/GcpTopicProvisioner.java:174-200,423-482` · routing GAP |
| `gcp-kafka-topic` | P/U | `servers` string | sin mapping exacto · id sensible | mismo source |
| `gcp-kafka-topic` | P/U/D | `data_product_id` string opt | no consumidor · id sensible | mismo source |
| `gcp-kafka-topic` | P/U/D | `component_id` string opt | no consumidor · id sensible | mismo source |
| `gcp-kafka-topic` | P/U/D | `routing_mode` string | no consumidor | mismo source |
| `gcp-kafka-topic` | P/U/D | `segment_id` string | no consumidor · id sensible | mismo source |
| `gcp-kafka-topic` | P/U/D | `team_id` string | no consumidor · id sensible | mismo source |
| `gcp-kafka-topic` | P/U/D | `cluster_key` string | no consumidor · id sensible | mismo source |
| `gcp-kafka-topic` | P/U | `retention_ms` number opt | no consumidor | mismo source |
| `gcp-kafka-topic` | D | `deleted` boolean condicional | no consumidor | `GcpTopicProvisioner.java:194-200` |
| `gcp-kafka-topic` | D | `already_absent` boolean condicional | no consumidor | `GcpTopicProvisioner.java:186-191` |
| `flink-sql` | P/U | `flink_application_id` wrapper | `.value`; sin consumidor · id sensible aunque flag false | `rio-controlplane-flink/src/main/java/com/mercadolibre/rio/controlplaneflink/deployment/FlinkAppOutputBuilder.java:25-55` |
| `flink-sql` | P/U | `flink_application_arn` wrapper | `.value`; sin consumidor · id sensible | mismo source |
| `flink-sql` | P/U | `flink_application_status` wrapper | `.value`; sin consumidor · público | mismo source |
| `flink-sql` | P/U | `flink_application_version_id` wrapper | `.value`; sin consumidor · id sensible | mismo source |
| `flink-sql` | P/U | `flink_application_created_timestamp` wrapper | `.value`; sin consumidor | mismo source |
| `flink-sql` | P/U | `flink_application_last_update_timestamp` wrapper | `.value`; sin consumidor | mismo source |
| `flink-sql` | D | `output=null` | no merge de values | `rio-controlplane-flink/src/main/java/com/mercadolibre/rio/controlplaneflink/handler/impl/DeleteAppInAWSHandler.java:47-68` |
| `aws-flink-job` | P/U | `flink_application_id` wrapper | `.value`; sin consumidor · id sensible | `FlinkAppOutputBuilder.java:25-55` |
| `aws-flink-job` | P/U | `flink_application_arn` wrapper | `.value`; sin consumidor · id sensible | mismo source |
| `aws-flink-job` | P/U | `flink_application_status` wrapper | `.value`; sin consumidor | mismo source |
| `aws-flink-job` | P/U | `flink_application_version_id` wrapper | `.value`; sin consumidor | mismo source |
| `aws-flink-job` | P/U | `flink_application_created_timestamp` wrapper | `.value`; sin consumidor | mismo source |
| `aws-flink-job` | P/U | `flink_application_last_update_timestamp` wrapper | `.value`; sin consumidor | mismo source |
| `aws-flink-job` | D | `output=null` | no merge de values | `DeleteAppInAWSHandler.java:47-68` |
| `clickhouse-mergetree` | P/U | `deploymentPath` string | sin consumidor | `rio-controlplane-clickhouse/src/main/java/com/mercadolibre/rio/controlplane/clickhouse/deployment/application/command/DeploymentCommandResult.java:64-95` |
| `clickhouse-mergetree` | P/U | `schemaName` string | front espera `schema_name` · MISMATCH/id sensible | mismo source |
| `clickhouse-mergetree` | P/U | `tableName` string | front usa `table_created` como nombre · MISMATCH/id sensible | mismo source |
| `clickhouse-mergetree` | P/U | `tableCreated` boolean | front espera `table_created` · MISMATCH casing | mismo source |
| `clickhouse-mergetree` | P/U | `tableAlreadyExists` boolean | sin consumidor | mismo source |
| `clickhouse-mergetree` | U | `tableAltered` boolean | sin consumidor | mismo source |
| `clickhouse-mergetree` | P/U | `jdbcUrl` string opt | front espera `jdbc_url` · MISMATCH/id sensible | mismo source |
| `clickhouse-mergetree` | P/U | `warehouseName` string | front espera snake · MISMATCH/id sensible | mismo source |
| `clickhouse-mergetree` | P/U | `readOnlyCredential.username` string | front espera `readonly_user_created` plano · credencial | mismo source |
| `clickhouse-mergetree` | P/U | `readOnlyCredential.created` boolean | objeto anidado | mismo source |
| `clickhouse-mergetree` | P/U | `readWriteCredential.username` string | front espera `crud_user_created` plano · credencial | mismo source |
| `clickhouse-mergetree` | P/U | `readWriteCredential.created` boolean | objeto anidado | mismo source |
| `clickhouse-mergetree` | D | `resourceDeleted` boolean | sin consumidor | `DeploymentCommandResult.java:57-61` |
| `clickhouse-mergetree` | D | `schemaName` string | sin consumidor · id sensible | mismo source |
| `clickhouse-mat-view` | P | `deploymentPath` string | sin consumidor | `DeploymentCommandResult.java:105-117` |
| `clickhouse-mat-view` | P | `schemaName` string | front espera snake · MISMATCH | mismo source |
| `clickhouse-mat-view` | P | `tableName` string | sin consumidor · id sensible | mismo source |
| `clickhouse-mat-view` | P | `sourceTable` string | sin consumidor · id sensible | mismo source |
| `clickhouse-mat-view` | P | `destTable` string | sin consumidor · id sensible | mismo source |
| `clickhouse-mat-view` | P | `username` string | credencial | mismo source |
| `clickhouse-mat-view` | P | `password` string condicional | secreto, persiste sin wrapper | mismo source |
| `kafka-fury-streams` | P/U | `templateName` string | sin consumidor · id sensible | `rio-controlplane-fury/src/main/kotlin/com/mercadolibre/rio_controlplane_fury/pusher/reconciler/PusherReconciler.kt:351-365` |
| `kafka-fury-streams` | P/U | `deployedVersion` string | sin consumidor · id sensible | mismo source |
| `kafka-fury-streams` | D | `deprovisioned` boolean | sin consumidor | `PusherReconciler.kt:424-438` |
| `fury-streams-kafka` | P/U | `templateName` string | sin consumidor · id sensible | `.../pusher/outbound/OutboundReconciler.kt:204-218` |
| `fury-streams-kafka` | P/U | `deployedVersion` string | sin consumidor · id sensible | mismo source |
| `fury-streams-kafka` | D | `deprovisioned` boolean | sin consumidor | `OutboundReconciler.kt:244-255` |
| `catalog-signal` | P/U | `result` object/string | sin consumidor · desconocido | `rio-materializer/src/main/java/com/mercadolibre/rio/materializer/handler/impl/ExecuteSignalHandler.java:31-51` |
| `catalog-signal` | P/U | `signal_id` string | Flink `${X.signal_id}` · id sensible | mismo source; front `flink-properties-sync/componentMappings.ts:80-83` |
| `catalog-signal` | P/U | `signal_name` string | Flink `${X.signal_name}` · id sensible | mismos sources |
| `catalog-signal` | P/U | `signal_display_name` string | sin consumidor | `ExecuteSignalHandler.java:31-51` |
| `catalog-signal` | P/U | `<destinationId>.destination_id` string | sin consumidor · id sensible | `.../handler/impl/ExecuteDestinationHandler.java:32-57` |
| `catalog-signal` | P/U | `<destinationId>.destination_name` string | sin consumidor · id sensible | mismo source |
| `catalog-signal` | P/U | `<destinationId>.destination_type` string | sin consumidor | mismo source |
| `catalog-signal` | P/U | `<destinationId>.destination_key` string | sin consumidor · id sensible | mismo source |
| `bigqueue-signal` | P/U | `bigqueue_name` wrapper `{type,value,sensitive}` | Flink/catalog `${X.bigqueue_name}`; legacy `.value` · id sensible | `.../handler/impl/MapResultBigQueueCollectorHandler.java:31-75` |
| `stream-signal` | P/U | `stream_name` wrapper | Flink/catalog `${X.stream_name}`; legacy `.value` · id sensible | `.../handler/impl/MapResultStreamCollectorHandler.java:31-72` |
| `s3-bucket` | P/U | `aws_s3_bucket_name` terraform/wrapper | Flink misma key · id sensible | `ComponentTemplateAwsS3Bucket.json:59-69`; front mapping `:73-76` |
| `s3-bucket` | P/U | `aws_s3_bucket_arn` terraform/wrapper | Flink misma key · id sensible | mismos sources |
| `gcs-bucket` | P/U | `name` terraform/wrapper | front nuevo no referencia este type · id sensible | `ComponentTemplateGcsBucket.json:59-69` |
| `gcs-bucket` | P/U | `url` terraform/wrapper | sin consumidor · id sensible | mismo source |

Storage diverge por engine: Cloud Controller usa `gcp_gcs_bucket_name/url`, template bundled usa `name/url`, front espera `bucket_name`. Runtime decide; GAP. `MapResultCloudControllerHandler.java:31-79`; `rio-materializer/src/main/java/com/mercadolibre/rio/materializer/utils/OutputUtils.java:27-53`.

## Producer-output → consumidores

| productor/key real | consumidor/key esperada | resultado |
|---|---|---|
| Kafka `kafka-topic.servers` | Flink `${X.brokers}` | MISMATCH; Playmaker no aliasa |
| Kafka `aws-msk-topic.servers` | Flink/catalog `${X.servers}` | key alineada; pipeline y legacy resuelven desde `service.values` |
| Kafka `topic_name` | Flink/catalog `${X.topic_name}` | key alineada; path-dependent |
| BigQueue `bigqueue_name.value` | Flink/catalog `${X.bigqueue_name}` | legacy desenvuelve; pipeline literal |
| Stream `stream_name.value` | Flink/catalog `${X.stream_name}` | legacy desenvuelve; pipeline literal |
| Catalog `signal_id/signal_name` | Flink mismas keys | path-dependent |
| S3 `aws_s3_bucket_*` | Flink mismas keys | nombre alineado; wrapper/template runtime |
| GCS `name/url` o `gcp_gcs_bucket_*` | `${X.bucket_name}` | MISMATCH |
| ClickHouse camel/nested | front snake/flat | MISMATCH estructural |
| Fury y Flink outputs | ninguno encontrado | persistidos, no consumidos |

**HECHO VISUAL DEL FRONT (2026-08-19, evidencia aportada por el owner).** La UI muestra cuatro properties configuradas contra el componente `chv7`: `chv7_jdbc_url → ${chv7.jdbc_url}`, `chv7_table_created → ${chv7.table_created}`, `chv7_crud_user_created → ${chv7.crud_user_created}` y `chv7_crud_user_password → ${chv7.crud_user_password}`. Esto confirma las **keys consumidoras y placeholders esperados por la configuración del front**, no que esos outputs existan en runtime. Al cruzarlo con el builder real de ClickHouse, permanecen los mismatches camelCase/anidado ya registrados: `jdbcUrl`, `tableCreated`, `readWriteCredential.username`, y no hay output `crud_user_password` demostrado. El último campo debe tratarse como `SECRET/CREDENTIAL` por intención; su fuente runtime continúa como GAP. No se registraron valores.

Presets en `ads-signals-frontend/src/technologies/relations.ts:71-325,350-377` copian literales del source form; no outputs. Compatibilidad `:31-65` justifica dirección, no existencia. El legacy `rio-frontend/app/components/v3/modals/rio-catalog-modal/adapter/SignalCatalogAdapter.ts:161-203` aún genera `${component.brokers}` para AWS MSK; su mapping ClickHouse también es plano/snake (`rio-frontend/app/nordic-pages/v2/template/wizard/pipeline-definition/hooks/properties-event-listener/componentMappings.ts:14-46`).

## Auditoría de `component_type_registry`

| aspecto | HECHO VERIFICADO | resultado |
|---|---|---|
| Publisher | `CPCapabilityMessage` declara topic/KVS/validación/lifecycle como trabajo futuro; no apareció publisher en CP/materializer | No es fuente productiva demostrada. `rio-sdk-events/src/main/java/com/mercadolibre/rio/sdk/events/capability/CPCapabilityMessage.java:13-20` |
| Formato | `schemaToJson` usa tipos literales (`String`) y `required` dentro de property | No es Draft 7 válido. `rio-playmaker/src/main/java/com/mercadolibre/rio/playmaker/service/impl/ComponentTypeRegistryServiceImpl.java:139-154`; `.../FieldDescriptor.java:12-19` |
| Validación | `SchemaValidator` networknt Draft 7 sólo tiene call sites de test | No participa en create/update/deploy. `rio-playmaker/src/main/java/com/mercadolibre/rio/playmaker/util/SchemaValidator.java:24-40` |
| Versiones | unique DB por tipo+semver; upsert busca por tipo/lastSeen y sobrescribe; `getAll` devuelve todas | latest no es semver y puede haber duplicados. `ComponentTypeRegistryServiceImpl.java:47-111`; `.../repository/ComponentTypeRegistryRepository.java:15-28`; migración `*controlplanes_component_registry.sql:1-21` |
| Seed | sólo tres Kafka; GCP dice `brokers` pero produce `servers`, RF required aunque defaulta 2, AWS output null | Kafka STALE; resto AUSENTE. `rio-playmaker/cli-services/bigq/seed-component-registry.yaml:1-120` |

Por tipo: los tres Kafka = **STALE**; los otros 25 = **AUSENTE**. Ninguno **ALINEADO**. Estado KVS externo: **NO VERIFICABLE** sin evidencia runtime.

## Mismatches priorizados

1. **P0:** ClickHouse produce camelCase/objetos anidados; ambos fronts esperan snake_case/plano; passwords esperados no existen en MergeTree output.
2. **P0:** aliases/routing: `gcp-kafka-topic` tiene handler pero cae al materializer; `flink-job`, `aws-flink-sql`, `clickhouse-matview` y `clickhouse-table` son visibles pero los CP directos los rechazan.
3. **P1:** Kafka `brokers` vs `servers`.
4. **P1:** storage `bucket_name` vs `name/url` vs `gcp_gcs_bucket_*`.
5. **P1:** registry stale/no-op, formato inválido y latest ambiguo.
6. **P1:** sensibilidad: ClickHouse puede persistir `password` sin wrapper; Fury loguea params; cifrado pre-dispatch no demostrado.
7. **P2:** output Fury depende del rol: orchestrator produce `templateName/deployedVersion/deprovisioned`; router legacy `mappingId/idempotent` o `{}`. `rio-controlplane-fury/src/main/kotlin/com/mercadolibre/rio_controlplane_fury/pusher/PusherEventRouter.kt:246-262,335-339,412-416`.
8. **P2:** outputs Flink/Fury y flags/IDs Kafka persisten sin consumidor encontrado.

## Preguntas humanas/runtime

- ¿Qué `component_type` y versión de template están activos por ambiente para storage, GCP Kafka y aliases del front?
- ¿El commit `fa73018a` está desplegado en todas las fleets/ambientes que ejecutan el pipeline nuevo?
- ¿Existe publisher/seed de capabilities externo no versionado? Se necesita sample redactado y estado semver real.
- ¿Dónde ocurre el cifrado prometido por el SDK y qué campos cubre KMS/redacción?
- ¿Qué fleet/role Fury está activo por ambiente?
- ¿Quién inyecta `system_id`, `environment` y `criticality` cuando el adapter no los emite?
- ¿Hay consumidores externos de outputs marcados “sin consumidor encontrado”?

## Límites y relacionados

“Sin consumidor” significa búsqueda por key exacta, placeholders, `destination_key`, `properties`, `properties_map` y `raw_sql` en los repos inspeccionados; no prueba ausencia externa. Observability consume metadata (`prefix_staging`, `prefix_production`, `criticality`) para cinco tipos y no publica result: `rio-controlplane-observability/src/main/java/com/mercadolibre/rio/controlplane/observability/service/AdsRioLogsFilterBigQueryService.java:31-35,96-142`. KMS no consume triggers y Signals no tiene handler real.

Relacionados: [[deploy-component]] · [[deploy-request-path]] · [[playmaker-deploy-flow]] · [[Crear Context]].
