---
type: project
schema_version: 1
owner: me
root: true
status: active
priority: P1
area: "[[Meli]]"
parent:
sprint:
start: 2026-08-31
due:
progress: 0
repo: multiple RIO repositories
jira:
prs:
aliases:
  - Adopción de Context
  - Context en Control Planes
  - Uso de Context
  - Context consumer rollout
slug: adopcion-context-control-planes
tags:
  - kind/project
  - area/meli
  - project/context-adoption
created: 2026-08-31
updated: 2026-09-04
---

# Adopción de Context en Control Planes

%% Naming: Adopción de Context en Control Planes es el link canónico del proyecto; aliases guarda variantes humanas; tags/slugs son solo automatización. %%

> [!info]+ Adopción de Context en Control Planes
> **Área:** [[Meli]] · **Estado:** active · **Prioridad:** P1 · **Sprint:** —
> Proyecto de cambio separado del discovery de comprensión [[Crear Context - Discovery de Params en CPs]]. La fuente canónica de evidencia es [[signals-context-flow]] y el contrato vigente de producción está documentado en [[Crear Context]].

## 🎯 Objetivo

Implementar progresivamente el uso de `DeploymentTriggerMessage.context` en los control planes, empezando por los consumidores que hoy reconstruyen o consumen información desde `params`, sin romper el contrato existente ni eliminar `params` antes de que todos los consumidores estén migrados.

El primer objetivo técnico es que los control planes puedan leer contexto tipado y topológico para distinguir configuración de usuario (`inputs`), resultados generados por infraestructura (`outputs`) e identidad de vecinos, manteniendo en `params` los parámetros operacionales y las properties manuales que todavía son necesarias.

## 📊 Estado actual

- La estrategia específica de ClickHouse quedó cerrada en [[Plan de implementación — Context en ClickHouse]] sobre `feature/new-component-context @ 7de630c6`: se descarta el overlay genérico de `lastDeployedVersion.inputs`, se propone una proyección interna tipada por tipo/operación con procedencia field-level y se mantiene `params` sólo como bridge explícito hasta que Context transporte requested/effective inputs y bindings de relaciones.
- `Context` ya se deriva en `rio-playmaker` como snapshot efímero por request del pipeline nuevo y se agrega a `DispatchRequest`; la derivación está en `ComponentContextServiceImpl`.
- `BigQueueDispatchAdapter` ya publica `request.context()` en `DeploymentTriggerMessage.context`; `params` continúa viajando sin reemplazo.
- `rio-sdk-events:1.4.0` contiene el contrato `ComponentContext`, `DataProduct`, `Component`, `LastDeployedVersion` y `RelatedComponent`; el campo `context` es nullable y aditivo.
- Los control planes todavía no consumen el nuevo `DeploymentTriggerMessage.context`; los consumidores actuales siguen leyendo `trigger.params()`.
- La cobertura de creación de Context no es universal: el pipeline nuevo `PROVISION` está conectado; el path legacy/componente y el materializer directo no comparten el carrier útil y quedan fuera hasta definir su integración.
- El discovery identificó que Flink es el consumidor directo de `properties_map`; ClickHouse, Kafka, Fury y Observability leen otros campos de `params`; KMS y Signals no tienen consumidor de deployment params demostrado.
- No se debe usar [[Guía de implementación — Component Context]] como guía vigente: documenta una entrega histórica abandonada. La implementación actual está reflejada en los repos y en [[Crear Context]].

## 🧭 Alcance y modelo de datos

El flujo actual que debe evolucionar es `front → Playmaker → DeploymentTriggerMessage.params → control plane`; el flujo nuevo agrega `context` en paralelo: `front/configuración → Playmaker → ComponentContext + params → BigQueue → control plane`.

`Context` es una entidad efímera calculada por request y no se persiste como snapshot propio. Se construye a partir de relaciones activas, service slots, deployments completados, autorizaciones de importación y outputs persistidos por los control planes.

El contrato v1 vigente es:

```text
ComponentContext
├─ dataProduct     DataProduct { id, name, teamName, environment }
├─ component       Component { id, name, type, lastDeployedVersion }
│                  └─ LastDeployedVersion { version, inputs, outputs }
├─ sources[]       RelatedComponent { id, name, type, inputs, outputs }
└─ destinations[]  RelatedComponent { id, name, type, inputs, outputs }
```

- `inputs` es configuración ingresada por el usuario desde `component_definition.parameters`; conserva objetos y arrays como JSON compacto y no desenvuelve un objeto que casualmente tenga una propiedad `value`.
- `outputs` son resultados generados por el control plane desde `_values`/`service.values`; el resolver desenvuelve envelopes `{type, value, sensitive}` y entrega el valor efectivo.
- `inputs` y `outputs` siempre salen del mismo service slot; si el slot no se resuelve, ambos mapas quedan vacíos.
- Una relación activa se conserva aunque el vecino no tenga outputs; la topología no se descarta por falta de datos.
- Un vecino importado solo puede leer el componente original con un par autorizado `(importedComponentId, sourceComponentId)`; las importaciones transitivas se rechazan y conservan el vecino con mapas vacíos.
- `lastDeployedVersion` usa el último deployment no eliminado con status exactamente `deploy_completed`, no el estado deseado de `componentDefinition`.
- `params` permanece separado e intacto; `Context` no es un reemplazo automático de todos los parámetros.

## 🔄 Flujo técnico vigente

- `ParameterResolutionService.resolveComponentParameters` ejecuta `DestinationParseService` y `ParametersParseService` antes de que exista el `DispatchRequest`; el resultado es el mapa efectivo que reciben hoy los CPs.
- `BatchDispatchServiceImpl` resuelve `params`, obtiene la versión, llama a `ComponentContextService.build(...)` y coloca ambos valores en `DispatchRequest`.
- `safelyBuildContext` permite que el deployment continúe sin Context si falla la derivación; una adopción futura puede cambiar esa política cuando todos los consumidores estén listos.
- `BigQueueDispatchAdapter` construye `DeploymentTriggerMessage` con `request.params()` y `request.context()`.
- `DeploymentTriggerMessage` conserva los campos planos de identidad y el constructor compatible de 14 argumentos; los consumers viejos pueden ignorar `context`.
- El path legacy de `DeploymentServiceImpl` resuelve y publica `params` sin construir Context.
- `MaterializerRestAdapter` recibe un `DispatchRequest`, pero usa IDs para materializar y no envía `params` ni `context` al materializer.
- Los tres batches de dispatch del pipeline nuevo pasan por el mismo punto de creación; el batch siguiente puede tener más outputs porque los resultados del batch anterior ya fueron persistidos.

## 🧩 Matriz de control planes y consumo de `params`

### `rio-controlplane-flink`

Flink es el consumidor prioritario para la adopción porque consume directamente el `properties_map` generado por los frontends y lo transforma en configuración AWS KDA.

- Entrada: `DeploymentTriggerMapper` copia todo `trigger.params()`, agrega tags derivados de criticality, componente, ambiente y data product, y llama a `CreateFlinkAppDTO.fromEventData`.
- Normalización: `flink_app_name → name`, `flink_runtime → runtime`, aliases legacy de checkpointing, monitoring, parallelism, rollback y `properties_map → properties`.
- Properties operacionales: `CreateApplicationRequestAdapter` y `UpdateApplicationRequestAdapter` llaman `buildRuntimeProperties()`, conservan las entries de `properties` y agregan `rio_parallelism` y properties de archivos.
- Destino final: el mapa termina en el grupo AWS KDA `APPLICATION_PROPERTIES`; los valores sensibles pueden pasar por `DecryptionService`.
- Metadata consumida: `name`, `runtime`, `checkpointing_enabled`, `checkpoint_interval`, `min_pause_between_checkpoints`, `log_level`, `metrics_level`, `parallelism`, `parallelism_per_kpu`, `auto_scaling_enabled`, `rollback_enabled`, `files`, `fury_app` y `tags`.
- Adopción propuesta: usar `context.sources[].outputs` y `context.destinations[].outputs` para resolver lineage y outputs de vecinos, pero conservar properties manuales, configuración runtime, aliases necesarios y cualquier entrada que realmente llegue a KDA.
- Riesgo: no se puede eliminar `params.properties_map` en la primera iteración porque el CP aún necesita el mapa de runtime y existe información manual que no está representada en Context.

### `rio-controlplane-clickhouse`

ClickHouse está identificado como consumidor real de `params`, aunque no consume `properties_map`.

- Entrada: `DeploymentTriggerMapper` toma `trigger.params()`, convierte snake_case a lower camel case y agrega `componentType`.
- Lookup: `DeploymentDataExtractor` busca primero en el nivel superior y después dentro de `data.parameters`; aplica fallback de casing.
- `clickhouse-mergetree` consume `warehouse_name`, `schema_name`, `table_name`, `engine_name`, `order_by`, `primary_key`, `partition_by`, `ttl`, `settings`, `table_fields` y `skip_indexes`.
- `clickhouse-mergetree` también tiene campos de deprovision como `resource_type` y `confirmation_token`, pero la evidencia de origen del frontend es incompleta.
- `clickhouse-mat-view` consume `source_warehouse_name`, `source_schema_name`, `source_table_name`, `dest_warehouse_name`, `dest_schema_name`, `dest_table_name` y `raw_sql`.
- `clickhouse-mat-view` tiene command de provision; update/deprovision quedan como gap en la matriz.
- Los comandos usan esos valores para crear, actualizar o borrar recursos; el CP no busca `properties_map`.
- Sus outputs alimentan a otros componentes: ClickHouse provisiona, persiste outputs, Playmaker los lee y después Flink/Catalog los reciben mediante placeholders resueltos.
- Mismatch P0: ClickHouse produce `jdbcUrl`, `tableCreated`, `readWriteCredential.username` y `readOnlyCredential.username`, mientras el front espera `jdbc_url`, `table_created`, `crud_user_created`, `crud_user_password`, `readonly_user_created` y `readonly_user_password`.
- Los outputs de credenciales son anidados en ClickHouse y planos en el front; `crud_user_password` no tiene output runtime demostrado y debe tratarse como secreto y GAP, no como hecho.
- Una adopción de Context debe preservar casing, precedencia top-level versus `parameters`, identidad versus credenciales y la decisión de seguridad sobre qué outputs pueden salir.

### `rio-controlplane-kafka`

Kafka consume parámetros operacionales de topics, no `properties_map`.

- `DeploymentProcessor` toma `trigger.params()`, aplica `TopicNamePrefixer` y entrega el mapa a `KafkaParams.parse`.
- `kafka-topic` y `aws-msk-topic` consumen `topic_name`, `partitions`, `replication_factor`, `retention_ms` y `configs`.
- `TopicNamePrefixer` lee `prefix_staging` y `prefix_production` y reemplaza `topic_name` por el nombre físico prefijado.
- `gcp-kafka-topic` consume `topic_name`, `partitions`, `replication_factor` y `retention_ms`; rechaza `configs` y aplica routing adicional con `segment_id`, `team_id` y `cluster_key`.
- `gcp-kafka-topic` tiene un gap de routing/dispatch: el CP acepta el tipo, pero Playmaker lo manda por catch-all/materializer en ciertos paths.
- Kafka produce outputs que luego pueden ser referenciados por Flink/Catalog.
- Mismatch P1: Kafka `kafka-topic` produce `servers`, mientras el front/Flink espera `brokers`; `aws-msk-topic` usa `servers` de forma alineada con sus placeholders.

### `rio-controlplane-fury`

Fury consume descriptores estructurados dentro de `params`, no `properties_map`.

- Inbound `kafka-fury-streams`: lee `source`, `destination` e `input_rate_limit_rpm`; deserializa `SourceDescriptor` y `DestinationDescriptor`.
- Outbound `fury-streams-kafka`: lee `source`, `destination` e `input_rate_limit_rpm`; exige `source.application_name` y valida el topic destino.
- Campos de descriptores: `type`, `name`, `application_name`, `mapping_id`/`mappingId`, `sink_batch_size`, `kafka_properties` y brokers opcionales.
- Los brokers del wire no son autoridad final; el orchestrator los reemplaza con configuración de fleet.
- Outputs del orchestrator incluyen `templateName`, `deployedVersion` y `deprovisioned`; el router legacy puede producir `mappingId`, `idempotent` o `{}` según el role.
- Hay riesgo de seguridad independiente: `DeploymentTriggerController` registra body y params completos; antes de migrar Context hay que retirar o redactar ese log.
- Una adopción de Context debe conservar identidad de source/destination, `input_rate_limit_rpm` y `mapping_id` necesario para deprovision.

### `rio-controlplane-observability`

Observability consume solo una parte acotada de `params`.

- `AdsRioLogsFilterBigQueryService` selecciona `prefix_production` o `prefix_staging` según el ambiente.
- Usa ese prefijo para construir `infra_component_name`, que participa en el MERGE de BigQuery y en la persistencia/borrado de criticality en Dynamo.
- No consume `properties_map` ni los parámetros funcionales completos del componente.
- El prefijo es una property operacional de identidad y no debe perderse al reemplazar gradualmente `params`.

### `rio-controlplane-kms`

En el HEAD auditado no hay referencia a `DeploymentTriggerMessage`, `trigger.params()` ni deployment params dentro de `src/main`. El repositorio expone requests HTTP independientes de encrypt/decrypt. Clasificación: `GAP/NO-CONSUMER`; no entra al rollout salvo una futura integración explícita.

### `rio-controlplane-signals`

En el HEAD auditado es un scaffold con configuración, healthcheck y DTO de muestra. No existe consumidor de deployment trigger ni lector de params. Clasificación: `GAP/NO-CONSUMER`.

## 🧱 Boundaries fuera de los CPs

- `rio-materializer` es un boundary legacy que procesa templates y outputs fuera del dispatch directo; debe auditarse por separado y no mezclarse con la adopción de Context en CPs.
- `ads-signals-catalog` construye/persiste metadata y `destinations[]`, pero no aparece como consumidor directo de `DeploymentTriggerMessage.params` en el corte.
- `rio-sdk-events` es el contrato compartido, no un consumidor de valores; `context` ya está publicado en `1.4.0`.
- No se deben copiar repos completos al vault; la evidencia de código se conserva como repo, commit, path relativo y líneas.

## 🧾 Properties derivadas que los frontends meten en `params`

La palabra “properties” se usa para tres estructuras distintas y no deben confundirse: `properties_map` de Flink, `destinations[].properties` de Catalog y parámetros propios del componente.

### `properties_map` de Flink

El frontend moderno define mappings en `ads-signals-frontend/src/features/flink-properties-sync/componentMappings.ts` y genera entradas en `propertiesGenerator.ts`.

El formato es `<componentName con guiones reemplazados por guiones bajos>_<property> → ${<componentName>.<output>}`. Ejemplo: `kafka_topic_brokers → ${kafka-topic.brokers}`.

Los targets Flink son `flink-sql`, `aws-flink-sql`, `aws-flink-job` y `flink-job`.

| Tipo de vecino | Properties generadas |
|---|---|
| `kafka-topic` | `topic_name`, `brokers` |
| `aws-msk-topic` | `topic_name`, `servers` |
| `s3-bucket` | `aws_s3_bucket_name`, `aws_s3_bucket_arn` |
| `gcp-bucket` | `bucket_name` |
| `clickhouse-mergetree` / `clickhouse-table` | `jdbc_url`, `table_created`, además credentials read-only cuando es input y credentials CRUD cuando es output |
| `catalog-signal` | `signal_id`, `signal_name` |
| `bigqueue-signal` / `bigqueue` | `bigqueue_name` |
| `stream-signal` / `stream` | `stream_name` |

Para ClickHouse, la dirección de la relación cambia las credenciales: source/input usa `readonly_user_created` y `readonly_user_password`; destination/output usa `crud_user_created` y `crud_user_password`. `jdbc_url` y `table_created` se inyectan en ambas direcciones.

El generador conserva entries manuales cuyos valores no son placeholders y reconstruye las entries derivadas cuando cambian las conexiones. El legacy equivalente mantiene la misma idea en `rio-frontend/.../flink-properties/propertiesGenerator.ts` y `propertiesManager.ts`.

### `destinations[].properties` de Catalog

Para un destino Kafka, los frontends generan `brokers`, `partitions` y `with_envelope`, además de `destination_key: ${<componente>.topic_name}`.

- `brokers` es un placeholder resuelto en runtime.
- `partitions` es un snapshot literal de la configuración del nodo Kafka y puede preservarse aunque el signal no se redeploye.
- `with_envelope` parte con default `false` y es editable.
- Properties custom del usuario se preservan.
- Destinos desconectados pueden quedar soft-deleted para conservar configuración y permitir reactivación.

La implementación moderna está en `ads-signals-frontend/src/features/catalog-destinations-sync/destinationsBuilder.ts`; la legacy está en `rio-frontend/.../catalog-destinations/kafkaDestinationManager.ts`.

### Parámetros propios, no properties derivadas

- Flink: `runtime`, `checkpoint_interval`, `parallelism`, `files`, `rollback`, `fury_app` y tags.
- ClickHouse: `warehouse_name`, `schema_name`, `table_name`, `engine_name`, `table_fields`, `raw_sql` y settings.
- Kafka: `topic_name`, `partitions`, `replication_factor`, `retention_ms`, `configs`, prefijos y routing GCP.
- Fury: `source`, `destination`, `input_rate_limit_rpm`, `sink_batch_size` y `mapping_id`.

## 🔀 Outputs y mismatches relevantes

| Productor | Consumidor o placeholder | Resultado |
|---|---|---|
| Kafka `kafka-topic.servers` | Flink `${X.brokers}` | Mismatch; Playmaker no aliasa |
| Kafka `aws-msk-topic.servers` | Flink/Catalog `${X.servers}` | Alineado |
| Kafka `topic_name` | Flink/Catalog `${X.topic_name}` | Alineado según path |
| BigQueue `bigqueue_name.value` | Flink/Catalog `${X.bigqueue_name}` | Legacy desenvuelve; pipeline literal |
| Stream `stream_name.value` | Flink/Catalog `${X.stream_name}` | Legacy desenvuelve; pipeline literal |
| Catalog `signal_id`/`signal_name` | Flink mismas keys | Dependiente del path |
| S3 `aws_s3_bucket_*` | Flink mismas keys | Nombre alineado, wrapper/template runtime |
| GCS `name`/`url` o `gcp_gcs_bucket_*` | `${X.bucket_name}` | Mismatch |
| ClickHouse camelCase/anidado | Front snake_case/plano | Mismatch estructural P0 |
| Fury y Flink outputs | Consumidor no encontrado | Persistidos, pero no demostrados como consumidos |

La evidencia visual aportada para un componente ClickHouse muestra `chv7_jdbc_url → ${chv7.jdbc_url}`, `chv7_table_created → ${chv7.table_created}`, `chv7_crud_user_created → ${chv7.crud_user_created}` y `chv7_crud_user_password → ${chv7.crud_user_password}`. Esto confirma las keys esperadas por el front, no la existencia de esos outputs en runtime; especialmente el password queda como secreto/GAP.

## ⚠️ Riesgos, gaps y decisiones

- P0: ClickHouse produce camelCase y objetos anidados mientras ambos frontends esperan snake_case y campos planos; además hay passwords esperados sin output runtime demostrado.
- P0: aliases/routing dejan visibles tipos que no llegan al CP directo: `gcp-kafka-topic`, `flink-job`, `aws-flink-sql`, `clickhouse-matview` y `clickhouse-table`.
- P1: Kafka `brokers` versus `servers`.
- P1: storage `bucket_name` versus `name`/`url` versus `gcp_gcs_bucket_*`.
- P1: `component_type_registry` no es autoridad contractual: publisher no demostrado, formato incompatible con Draft 7, latest ambiguo y seeds Kafka stale.
- P1: sensibilidad: ClickHouse puede persistir password sin wrapper, Fury registra params completos y el cifrado pre-dispatch no está demostrado.
- P2: outputs de Fury dependen del role activo y outputs de Flink/Fury o flags/IDs de Kafka pueden persistir sin consumidor encontrado.
- La búsqueda “sin consumidor” solo cubre keys, placeholders, `destination_key`, `properties`, `properties_map` y `raw_sql` en los repos inspeccionados; no prueba ausencia de consumidores externos.
- El Context no debe inventar mappings por igualdad de nombres o valores. Configured path, producer path, consumer path y valor sustituido son hechos distintos.
- `params` solo puede eliminarse después de una migración explícita por CP y path; durante el rollout se mantienen ambos carriers.

## 🧱 Entrega de desarrollo

| Aplicación / repo | Branch / commit de referencia | Base | SPEC funcional | SPEC técnica | Estado |
|---|---|---|---|---|---|
| `rio-playmaker` | `feature/new-component-context` @ `658f8f615` | `develop` @ `28b929c9e` | [[SPEC Funcional — Context IO]] / SIG-573 | [[SPEC Tecnica — Context IO]] / SIG-590 | Context derivado y publicado en pipeline nuevo; adopción de CP pendiente |
| `rio-sdk-events` | `master` @ `8732ee47e` | `master` @ `9d86eb8` | SIG-573 | SIG-590 | PR #43 mergeado; `1.4.0` publicado |
| `rio-controlplane-flink` | `develop` @ `7af7e3f8` | `develop` | Pendiente de spec de adopción | Pendiente de spec de adopción | Primer CP candidato; consume `properties_map` |
| `rio-controlplane-clickhouse` | `develop` @ `a2ca40e4` | `develop` | Pendiente de spec de adopción | Pendiente de spec de adopción | Consumidor real de params; no consume `properties_map`; P0 de casing/shape |
| `rio-controlplane-kafka` | `develop` @ `427d090d` | `develop` | Pendiente de spec de adopción | Pendiente de spec de adopción | Consumidor real de params; routing GCP y mismatch brokers/servers |
| `rio-controlplane-fury` | `develop` @ `7eb7932e` | `develop` | Pendiente de spec de adopción | Pendiente de spec de adopción | Consumidor real de params; requiere redacción de logs antes de migrar |
| `rio-controlplane-observability` | `develop` @ `43ca94b7` | `develop` | Pendiente de spec de adopción | Pendiente de spec de adopción | Consume prefijos de identidad |
| `rio-controlplane-kms` | `develop` @ `b7b5225` | `develop` | No aplica al corte actual | No aplica al corte actual | Sin consumidor de deployment params demostrado |
| `rio-controlplane-signals` | `develop` @ `cd12752` | `develop` | No aplica al corte actual | No aplica al corte actual | Scaffold sin consumidor de deployment params |

No se debe comenzar una modificación de CP hasta que su fila tenga una spec funcional y técnica de adopción, branch/base verificables y criterios de compatibilidad con `params`.

## ✅ Tareas

- [ ] Redactar spec funcional y técnica de adopción para Flink, definiendo qué properties derivadas pasan a `Context` y qué parámetros permanecen en `params` #owner/me #type/dev #area/meli
- [ ] Implementar lectura backward-compatible de `DeploymentTriggerMessage.context` en Flink sin eliminar `params` #owner/me #type/dev #area/meli
- [ ] Probar reconstrucción de properties de Flink desde `sources[].outputs` y `destinations[].outputs`, incluyendo outputs vacíos y neighbors no desplegados #owner/me #type/dev #area/meli
- [x] Definir y documentar la estrategia de adopción de ClickHouse, incluyendo precedencia top-level/parameters y decisión sobre outputs camelCase/anidados #owner/me #type/dev #area/meli ✅ 2026-09-04
- [ ] Definir y documentar la estrategia de adopción de Kafka, incluyendo `servers`/`brokers` y el routing de `gcp-kafka-topic` #owner/me #type/dev #area/meli
- [ ] Redactar la migración de Fury y eliminar o redactar el log de body/params completos #owner/me #type/dev #area/meli
- [ ] Mantener `prefix_staging`/`prefix_production` para Observability o sustituirlos por una fuente tipada equivalente #owner/me #type/dev #area/meli
- [ ] Resolver los gaps de legacy/componente y materializer antes de declarar cobertura completa de Context #owner/me #type/research #area/meli
- [ ] Validar consumers externos de outputs clasificados como “sin consumidor encontrado” #owner/me #type/research #area/meli
- [ ] Definir el criterio de retiro de `params` por CP y path, después de la adopción incremental #owner/me #type/dev #area/meli

## 📆 Bitácora

%% Log diario para las dailies. Una línea por día con lo avanzado / blockers. %%
- **2026-09-04** — Revisión read-only de `rio-controlplane-clickhouse/feature/new-component-context @ 7de630c6` y plan documentado en [[Plan de implementación — Context en ClickHouse]]. Decisión: no extender `DeploymentRequestedEvent.data` ni hacer overlay de maps; tipar el dominio en el CP, aislar el SDK temporal, medir resolución por field y migrar por `PARAMS_ONLY → SHADOW → CONTEXT_PREFERRED → CONTEXT_REQUIRED`. Se precisó que el blocker de retiro no es la cantidad de keys: `params` representa los inputs efectivos de `requestedVersion`, mientras `lastDeployedVersion.inputs` pertenece al deployment completado anterior y puede faltar en el primero. El contrato objetivo agrega `requestedVersion.effectiveInputs`, conserva `lastDeployedVersion` como estado histórico y exige bindings sólo en paths relacionales ambiguos; los gaps `view*`, ownership/UPDATE de Kafka y target Java se mantienen separados como blockers del rollout correspondiente.
- **2026-08-31** — Se creó este proyecto de delivery separado del discovery. Se trasladó la investigación completa del uso de Context, los siete CPs auditados, los boundaries, el inventario de properties de ambos frontends, los mismatches y los paths de dispatch. La fuente de evidencia sigue siendo [[signals-context-flow]] y el discovery original [[Crear Context - Discovery de Params en CPs]].

## 🧭 Decisiones

- ClickHouse no agrega `ComponentContext` a `DeploymentRequestedEvent`: el SDK queda en adapters y el dominio recibe specs tipadas por `component_type × operation` con un reporte de resolución sin valores.
- `component.lastDeployedVersion.inputs` no es autoridad para PROVISION/UPDATE. Durante la transición, los campos no representados por Context usan fallback explícito desde params efectivos; no existe overlay genérico.
- La retirada total de params requiere `requestedVersion.effectiveInputs` con paridad respecto de los params post-resolución de la misma solicitud; `lastDeployedVersion` conserva inputs/outputs históricos y nunca sustituye el desired state.
- `requestedVersion` y `lastDeployedVersion` pueden compartir un value object de inputs efectivos, pero no el mismo DTO: la versión solicitada aún no tiene outputs y la desplegada representa un resultado histórico. Se evita el nombre ambiguo `currentVersion`.
- Los bindings por ID/rol son obligatorios sólo para un path que deba elegir entre relaciones potencialmente ambiguas; no son un blocker universal para comenzar a consumir Context.
- La adopción es incremental y aditiva: `context` se consume sin retirar `params` inicialmente.
- Flink es el primer CP candidato porque consume directamente `properties_map`; ClickHouse, Kafka, Fury y Observability requieren tracks propios porque sus contratos de `params` son diferentes.
- ClickHouse está dentro del alcance de adopción, pero su mismatch camelCase/anidado versus snake_case/plano debe resolverse explícitamente y no mediante alias inventados.
- KMS y Signals no se incluyen en la primera ola porque no tienen consumidores de deployment params demostrados.
- El discovery de comprensión y este proyecto de cambio permanecen separados; este proyecto enlaza la evidencia sin convertirse en su dueño.

## 🔗 Docs / Links

- [[Crear Context]]
- [[Crear Context - Discovery de Params en CPs]]
- [[signals-context-flow]]
- [[SPEC Funcional — Context IO]]
- [[SPEC Tecnica — Context IO]]
- [[Plan de implementación — Context en ClickHouse]]
- [[Descripción PR — rio-playmaker]]
- [[rio-playmaker]]
- [[rio-sdk-events]]
- [[RIO]]

## 💡 Ideas

### Backlog de ideas

- Explorar una capa adaptadora por CP que combine `Context` tipado con parámetros propios, sin convertir `Context` en un contenedor genérico de toda la configuración.
- Usar la matriz field-level como contrato de migración y como gate para retirar cada placeholder del frontend.

### Motivos / principios

- La fuente de verdad del output runtime es el resultado persistido por el CP, no el mapping que el frontend guarda.
- Un valor igual no demuestra una relación; los mappings requieren evidencia del path productor y consumidor.
- Un Context parcial debe conservar topología y representar explícitamente mapas vacíos.
- La seguridad debe tratar `params`, `inputs` y `outputs` como potencialmente sensibles y evitar logs crudos.

### Memoria pública / interna

- **Memoria pública:** [[signals-context-flow]] conserva la auditoría field-level y su provenance; [[Crear Context]] conserva el contrato y estado del proyecto de origen.
- **Memoria interna:** no aplica; este proyecto usa fuentes públicas del vault y código con repo/commit/path relativo.
- **Motivo:** mantener la comprensión reusable separada de las decisiones y tareas de implementación.
