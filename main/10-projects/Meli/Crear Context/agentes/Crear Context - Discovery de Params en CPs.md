---
type: project
schema_version: 1
owner: agent
root: false
status: active
priority: P1
area: "[[Meli]]"
parent: "[[Crear Context]]"
sprint:
start: 2026-08-25
due:
progress: 28
repo:
jira:
prs:
aliases:
  - Crear Context CP Discovery
  - Discovery de Params en Control Planes
tags:
  - kind/project
  - area/meli
  - project/crear-context
  - agent/discovery
  - priority/p1
created: "2026-08-25"
updated: "2026-08-25"
---

# Crear Context - Discovery de Params en CPs

%% Naming: Crear Context - Discovery de Params en CPs es el link canónico del proyecto; aliases guarda variantes humanas; tags/slugs son solo automatización. %%

> [!info]+ Crear Context - Discovery de Params en CPs
> **Área:** [[Meli]] · **Estado:** active · **Prioridad:** P1 · **Parent:** [[Crear Context]] · **Owner:** agent · **Progreso:** 28%
> Este es un proyecto de comprensión: documenta dónde se consumen los datos hoy para habilitar una futura adopción de Context en los control planes. No modifica código de repos.

> [!abstract]- Ownership del proyecto (`owner`) — humano vs agente
> `owner: me` → **proyecto humano**: la iniciativa/esfuerzo que conduces tú.
> `owner: agent` → **proyecto de agente**: un curro delegado, con detalle pesado que escribe y sigue un agente. Casi siempre es subproyecto de uno humano y vive en la subcarpeta `agentes/` de su iniciativa.
> `root: true` solo en **iniciativas raíz** (sin `parent`). Todo subproyecto debe setear `parent`; si no, aparece como huérfano en [[Panel de Proyectos]].
>
> **Tarea puente:** cuando este proyecto es `owner: agent`, en su proyecto **padre** debe existir UNA sola tarea humana que lo representa (arrancar + seguimiento). Así tu cockpit ve una línea por curro delegado, no las tareas internas del agente. Ejemplo, en el padre:
> `- [ ] [[Crear Context - Discovery de Params en CPs]] arrancar + seguimiento #owner/me #type/supervision #area/meli`

## 🎯 Objetivo

Completar un discovery forense y reproducible del flujo `front → Playmaker → DeploymentTriggerMessage.params → control plane`, identificando por componente, operación, key/path, transformación y efecto operacional dónde se usan las properties que hoy el front inserta en `params` y qué repos deben cambiar cuando los CPs adopten `Context`.
El entregable debe separar consumo real de configuración, aliases, defaults, valores inyectados por runtime, outputs y datos que no tienen consumidor; cada afirmación debe quedar respaldada por `repo + commit + path relativo + líneas` y por una clasificación `VERIFIED`, `INFERRED` o `GAP`.

## 📊 Estado actual

- Proyecto creado como `owner: agent` bajo [[Crear Context]] y tarea puente agregada al proyecto padre.
- Alcance inicial congelado en 13 repos del ecosistema RIO: 2 frontends, Playmaker, SDK, 7 control planes, materializer y catálogo.
- Primera pasada verificada en los 7 repos de control plane contra sus HEAD locales del 2026-08-25. No se modificó ningún repositorio externo.
- Hallazgo principal: `properties_map` generado por el front tiene un consumidor directo inequívoco en `rio-controlplane-flink`; ClickHouse, Fury y Kafka hacen consumo operativo de otras formas de `params`; Observability usa únicamente prefijos para identidad; KMS y Signals no muestran consumidor de deployment params en el HEAD auditado.
- El reporte aún no está cerrado: falta completar la matriz field-level de los caminos legacy/materializer, validar fixtures/tests y repetir el corte contra los commits finales posteriores al merge de Context.

## 🧱 Entrega de desarrollo

%% Esta sección siempre queda disponible. En proyectos que cambian código, configuración ejecutable, schemas o infraestructura, es obligatoria: una fila por repo/branch, con SPEC funcional y técnica enlazadas antes de implementar. En proyectos no técnicos, reemplazar la tabla por `_No aplica — <motivo>._`. %%

_No aplica — este proyecto produce comprensión y documentación; no implementa cambios de código, configuración, schemas ni infraestructura._

## 🔍 Alcance y criterio de evidencia

- **Capa A — properties sintetizadas por el front:** placeholders `${component.output}`, aliases de nombres, `properties_map` de Flink y `destinations[].properties`/`destination_key` de catalog-signal.
- **Capa B — parámetros propios del componente:** valores que el usuario configura en el formulario y que el front persiste dentro de `parameters`/`params`; se reportan separadamente de las properties derivadas.
- **Capa C — enriquecimiento runtime:** prefijos, tags, IDs, nombres físicos, defaults y datos de fleet que aparecen en `params` o se aplican después de leerlos.
- **Consumidor directo:** código del repo que lee una key/path del payload o la transforma en un DTO/command que llega a una API de infraestructura.
- **No consumidor:** campo deserializado o persistido que no participa en una decisión, request, identidad, validación, log o output verificable.
- **Regla de fuente:** las notas del vault, incluido [[signals-context-flow]], son índices y contexto; la autoridad de cada hallazgo es el código del repo en el commit declarado.

## 🗺️ Universo de repositorios y corte auditado

| Repo | Rol en el discovery | Branch | Commit auditado | Estado local |
|---|---|---|---|---|
| `ads-signals-frontend` | Front moderno; genera `properties_map` y destinations | `develop` | `32c7fa56` | clean |
| `rio-frontend` | Front legacy; genera relaciones, placeholders y `properties_map` | `develop` | `6d644ec6` | clean |
| `rio-playmaker` | Persistencia, resolución de placeholders y transporte a CPs | `feature/new-component-context` | `39f616c4` | dirty por implementación vigente de Context |
| `rio-sdk-events` | Contrato wire de `DeploymentTriggerMessage.params/context` | `feature/new-component-context` | `72b5a570` | clean |
| `rio-controlplane-kafka` | Consumidor de topics Kafka | `develop` | `427d090d` | clean |
| `rio-controlplane-flink` | Consumidor de apps Flink/KDA | `develop` | `7af7e3f8` | clean |
| `rio-controlplane-clickhouse` | Consumidor de recursos ClickHouse | `develop` | `a2ca40e4` | clean |
| `rio-controlplane-fury` | Consumidor de pipelines Kafka↔Fury Streams | `develop` | `7eb7932e` | clean |
| `rio-controlplane-kms` | API de secretos; verificar no consumidor de deployment params | `develop` | `b7b5225` | clean |
| `rio-controlplane-observability` | Consumidor de triggers para BigQuery/Dynamo de observabilidad | `develop` | `43ca94b7` | clean |
| `rio-controlplane-signals` | Scaffold de CP sin lógica de deployment | `develop` | `cd12752` | clean |
| `rio-materializer` | Boundary legacy y consumidor de templates; no cuenta como CP | `develop` | `56ebada2` | clean |
| `ads-signals-catalog` | Catálogo; boundary de destinations, no consumidor de deployment params | `develop` | `67f11cc` | clean |

## 🔁 Flujo AS-IS que se debe reemplazar gradualmente

`ads-signals-frontend`/`rio-frontend` persisten configuración y properties derivadas en `ComponentDefinition.parameters`; `rio-playmaker` resuelve placeholders contra outputs de servicios y construye el mapa efectivo; `rio-sdk-events` lo transporta como `DeploymentTriggerMessage.params`; cada CP aplica su propio parser, alias, default y transformación antes de llamar a infraestructura o persistir estado.
En el pipeline nuevo, `ParameterResolutionService` resuelve destinations y parámetros antes del dispatch, `BatchDispatchServiceImpl` construye `DispatchRequest` y `BigQueueDispatchAdapter` sigue publicando `request.params()` junto con `request.context()`. En el path legacy, `DeploymentServiceImpl` resuelve y publica `params` sin Context. Esta diferencia es un gate del rollout.

## 📍 Reporte AS-IS: origen y transporte de las properties

### Front moderno: `ads-signals-frontend`

- `src/features/flink-properties-sync/propertiesGenerator.ts:8-76` genera keys compuestas `{componentName.replace('-', '_')}_{flinkPropertyKey}` y valores `${componentName.outputKey}`; preserva entradas manuales y reconstruye las generadas al cambiar conexiones.
- `src/features/flink-properties-sync/componentMappings.ts:13-88` define qué outputs de Kafka, S3/GCS, ClickHouse, catálogo, BigQueue y Stream se inyectan en Flink; ClickHouse selecciona credenciales readonly/crud según dirección.
- `src/features/flink-properties-sync/syncFlinkNodeProperties.ts:80-96` lee el `properties_map` existente y persiste `{ ...baseParams, properties_map: newPropertiesMap }` en `PATCH /pipeline/components/{name}/config`.
- `src/features/catalog-destinations-sync/destinationsBuilder.ts:19-125` construye `destinations[]`, usa `${component.field}` como `destination_key`/`brokers`, y toma `partitions` como snapshot desde `componentParams`.
- `src/features/catalog-destinations-sync/syncCatalogDestinations.ts:56-71` vuelve a persistir `{ ...baseParams, destinations }` dentro de `params` del `catalog-signal`.
- `api/definitions/index.ts:32-159,317-332` valida `properties_map`, valida algunos tipos y envía `parameters` a Playmaker; para tecnologías no cubiertas por el schema del front, el mapa pasa sin normalización específica.

### Front legacy: `rio-frontend`

- `app/nordic-pages/v2/template/wizard/pipeline-definition/hooks/properties-event-listener/flink-properties/propertiesGenerator.ts:12-68` genera templates con soporte adicional para componentes importados `${sourceDP.component[env].property}`.
- `app/nordic-pages/v2/template/wizard/pipeline-definition/hooks/properties-event-listener/flink-properties/propertiesManager.ts:7-32` escribe los valores generados en `flinkNode.parameters.properties_map`.
- `app/nordic-pages/v2/template/wizard/pipeline-definition/hooks/properties-event-listener/componentMappings.ts:14-47` define el catálogo legacy de outputs que alimenta Flink.
- `app/nordic-pages/v2/template/wizard/pipeline-definition/hooks/properties-event-listener/catalog-destinations/kafkaDestinationManager.ts:22-82` escribe `destinations[].properties.brokers` como placeholder, `partitions` como snapshot y `with_envelope` como default editable.
- `app/components/v2/component-relation-logic/resolveRelationProperties.ts:61-176` usa las keys de `properties_map` para inferir nodos fuente cuando el grafo está stale y actualiza templates directos a formato full-path; esta lógica es UI/provenance, no un consumidor de CP.

### `rio-playmaker` y `rio-sdk-events`

- `rio-playmaker/src/main/java/com/mercadolibre/rio/playmaker/service/ParameterResolutionService.java:28-40` ejecuta primero `DestinationParseService` y luego `ParametersParseService` sobre la configuración persistida.
- `rio-playmaker/src/main/java/com/mercadolibre/rio/playmaker/service/pipeline/impl/BatchDispatchServiceImpl.java:246-279` parsea el JSON resuelto, crea el Context y arma el `DispatchRequest`; el `params` que sigue es el mapa efectivo, no el JSON crudo del front.
- `rio-playmaker/src/main/java/com/mercadolibre/rio/playmaker/service/pipeline/impl/BigQueueDispatchAdapter.java:86-104` construye `DeploymentTriggerMessage` con `request.params()` y `request.context()`; el Context vigente no reemplaza `params` todavía.
- `rio-playmaker/src/main/java/com/mercadolibre/rio/playmaker/service/impl/DeploymentServiceImpl.java:885-949` mantiene un path legacy que resuelve y publica `params` sin construir Context.
- `rio-sdk-events/src/main/java/com/mercadolibre/rio/sdk/events/deployment/DeploymentTriggerMessage.java:72-113` mantiene `params` como `Map<String,Object>` y agrega `context` nullable; los CPs actuales deserializan y pueden ignorar el campo nuevo.

## 🧭 Reporte por control plane: consumidores precisos

### `rio-controlplane-kafka`

- **Entrada y operación:** `src/main/java/com/mercadolibre/rio_controlplane_kafka/deployment/DeploymentProcessor.java:204-215,209-210` toma `trigger.params()`, aplica `TopicNamePrefixer` y entrega el mapa a `KafkaParams.parse`.
- **Keys consumidas por `kafka-topic`/`aws-msk-topic`:** `topic_name`, `partitions`, `replication_factor`, `configs` y `retention_ms`; `KafkaParams.java:34-140` valida tipos, reconcilia `retention_ms` con `configs[retention.ms]` y elimina la key de config antes de provisionar.
- **Properties de identidad física:** `TopicNamePrefixer.java:34-76` lee `prefix_staging`/`prefix_production` y aliases legacy según `environment_name`, y reemplaza `topic_name` por el nombre físico prefijado.
- **GCP:** `GcpDeploymentProcessor.java:204,230,255` lee params para routing y parseo; `GcpTopicParams.java:47-164` consume `topic_name`, `partitions`, `replication_factor` y `retention_ms`, y rechaza `configs`; `GcpKafkaRoutingService.java:86-115` rechaza `segment_id`, `team_id` y `cluster_key` dentro de params.
- **Relación con properties generadas:** no existe lectura directa de `properties_map`; Kafka produce outputs que luego pueden ser referenciados por Flink/Catalog. `gcp-kafka-topic` tiene además un GAP de routing/dispatch que debe cerrarse antes de reemplazar su contrato.

### `rio-controlplane-flink`

- **Entrada:** `src/main/java/com/mercadolibre/rio/controlplaneflink/deployment/DeploymentTriggerMapper.java:44-145` copia todo `trigger.params()`, inyecta tags y llama `CreateFlinkAppDTO.fromEventData`.
- **Normalización:** `CreateFlinkAppDTO.java:335-399,454-524` aplica aliases (`flink_app_name→name`, `flink_runtime→runtime`, checkpoint/monitoring/parallelism legacy), `properties_map→properties`, arma `fury_app` y convierte tags.
- **Uso operativo de la property map:** `CreateApplicationRequestAdapter.java:59-155` y `UpdateApplicationRequestAdapter.java:57-158` convierten el DTO en configuración KDA; `buildRuntimeProperties()` deja las entries de `properties_map` en el `APPLICATION_PROPERTIES` group y agrega `rio_parallelism`/keys de archivos. `DecryptionService.java:49-67` puede transformar valores sensibles antes de enviarlos a AWS.
- **Keys de metadata consumidas en la misma pasada:** `name`, `runtime`, `checkpointing_enabled`, `checkpoint_interval`, `min_pause_between_checkpoints`, `log_level`, `metrics_level`, `parallelism`, `parallelism_per_kpu`, `auto_scaling_enabled`, `rollback_enabled`, `files`, `fury_app` y tags.
- **Conclusión para Context:** este es el consumidor directo prioritario de las properties que el front inserta; Context debe reemplazar la necesidad de que Flink reciba aliases/keys compuestas, pero no puede perder las properties manuales de runtime ni las entradas que realmente llegan a KDA.

### `rio-controlplane-clickhouse`

- **Entrada:** `src/main/java/com/mercadolibre/rio/controlplane/clickhouse/deployment/adapter/rest/DeploymentTriggerMapper.java:15-31` toma `trigger.params()`, convierte snake_case a camelCase y lo guarda como `DeploymentRequestedEvent.data`.
- **Lookup top-level/nested:** `DeploymentDataExtractor.java:77-139` lee fields requeridos/opcionales primero del mapa top-level y luego de `data.parameters`; `MapUtils` permite fallback de casing.
- **MergeTree:** `DeploymentDataExtractor.java:156-345` consume `warehouseName`, `schemaName`, `tableName`, `engineName`, `orderBy`, `primaryKey`, `partitionBy`, `ttl`, `settings`, `tableFields` y `skipIndexes`, incluyendo objetos anidados y listas; commands posteriores usan estos valores para crear, alterar o borrar recursos.
- **Materialized view:** `DeployMaterializedView.java:48-99` consume source/destination warehouse/schema/table y `rawSql`, validando que el SQL coincida con los params.
- **Relación con properties generadas:** el CP no lee `properties_map`; sus outputs (`table_created`, `jdbc_url`, credenciales y otros) son los que el front transforma en placeholders para Flink. La sustitución de Context debe preservar casing, precedencia top-level vs `parameters`, y la distinción entre identidad y credenciales.

### `rio-controlplane-fury`

- **Inbound `kafka-fury-streams`:** `src/main/kotlin/com/mercadolibre/rio_controlplane_fury/pusher/orchestrator/PusherOrchestrator.kt:186-220,967-1015` lee `params.source`, `params.destination` y el top-level `input_rate_limit_rpm`; deserializa los descriptores y usa el rate limit para el spec hash/reconciler.
- **Outbound `fury-streams-kafka`:** `PusherOrchestrator.kt:463-503,975-1015` lee `source`, `destination` y el mismo `input_rate_limit_rpm`; exige `source.application_name` y valida el topic destino.
- **Shape de descriptores:** `pusher/bigqueue/dto/SourceDescriptor.kt:16-118` consume `type`, `name`, `application_name`, `mapping_id`, `sink_batch_size`, `kafka_properties` y brokers opcionales; `DestinationDescriptor.kt:16-101` consume `type`, `name`, `application_name` y `kafka_properties`/brokers según dirección. Los brokers del wire no son autoridad: el orchestrator los reemplaza por configuración de fleet en `PusherOrchestrator.kt:203-215,485-498`.
- **Riesgo de observabilidad:** `pusher/bigqueue/DeploymentTriggerController.kt:104-128` registra el body crudo y `params` completos; antes de cualquier adopción de Context hay que retirar o redactar ese log.
- **Relación con properties generadas:** no hay lectura de `properties_map`; el CP consume descriptores estructurados. El nuevo Context podría retirar aliases y datos que el front arma, pero debe conservar identidad de source/destination, rate limit y `mapping_id` de deprovision.

### `rio-controlplane-observability`

- **Entrada:** `src/main/java/com/mercadolibre/rio_controlplane_observability/controller/DeploymentTriggerConsumerController.java:24-57` consume deployment triggers y delega a `AdsRioLogsFilterService`.
- **Única lectura directa encontrada:** `AdsRioLogsFilterBigQueryService.java:79-139` selecciona `prefix_production` o `prefix_staging` de `event.params()` para construir `infra_component_name`; ese nombre se usa como clave del MERGE en BigQuery y para guardar/borrar criticality en Dynamo.
- **Relación con properties generadas:** no consume `properties_map` ni otros fields del front; el prefijo sí es una property operacional que afecta identidad y no debe desaparecer si se reemplaza params.

### `rio-controlplane-kms`

- En el HEAD `b7b5225` no hay referencia a `DeploymentTriggerMessage`, `trigger.params()` ni `params` dentro de `src/main`; el repo expone requests HTTP de cifrado/descifrado independientes (`EncryptRequest`, `EncryptJsonRequest`, `DecryptRequest`).
- **Clasificación:** `GAP/NO-CONSUMER` para deployment params; no debe entrar al rollout de Context salvo que una futura integración explícita lo conecte.

### `rio-controlplane-signals`

- En el HEAD `cd12752` `src/main` es scaffold de aplicación y solo contiene configuración, healthcheck y DTO de muestra; no existe consumidor de deployment trigger ni lector de params.
- **Clasificación:** `GAP/NO-CONSUMER`; no hay implementación de CP que adaptar en este repositorio hoy.

## 🧱 Boundaries fuera de los 7 CPs

- `rio-materializer` debe auditarse como path legacy porque procesa templates y outputs fuera del dispatch directo; no se lo debe mezclar con el plan de adopción de Context en CPs. La matriz histórica de [[signals-context-flow]] contiene candidatos, pero el cierre de este proyecto exige revalidarlos contra `56ebada2`.
- `ads-signals-catalog` persiste/expone metadata y destinations; no aparece como consumidor del `DeploymentTriggerMessage.params` en este corte. Se conserva en el universo para detectar si el reemplazo afecta el shape de `destinations[]`.
- `rio-sdk-events` es contrato compartido, no consumidor de valores; el único cambio de wire requerido para Context ya está representado como `context` nullable en la branch auditada. La adopción no debe borrar `params` hasta que todos los consumers estén migrados.

## 🧪 Hallazgos que cambian el diseño del rollout

- `properties_map` no es un contrato transversal de CPs: solo Flink lo consume directamente como mapa de propiedades KDA; los demás CPs consumen keys propias y/o descriptores anidados.
- Playmaker resuelve placeholders antes de los CPs; por tanto, los CPs no deberían volver a resolver `${...}` cuando adopten Context. La fuente de verdad del valor runtime debe quedar en Context/Playmaker y el CP debe usarlo como input ya resuelto.
- `parameters`/`params` tiene formas incompatibles: mapa plano en Kafka/Flink, mapa con fallback nested `parameters` en ClickHouse, descriptores polymórficos en Fury y prefijos puntuales en Observability.
- El reemplazo requiere mantener explícitamente valores manuales de Flink, aliases de deprovision (`mapping_id`), prefijos de identidad física, snapshots de `partitions` y la precedencia/casing de ClickHouse.
- El wire `context` puede ser aditivo mientras exista un rollout mixto; quitar o vaciar `params` antes de adaptar todos los CPs rompería Kafka/Flink/ClickHouse/Fury/Observability y los paths legacy.
- Fury tiene un riesgo de filtración de payload completo en logs; la migración de params es una oportunidad de cerrar ese riesgo, pero debe quedar como tarea explícita y no como supuesto.

## ⚠️ Gaps y preguntas abiertas

- Verificar el path `rio-materializer` completo, especialmente `catalog-signal`, `s3-bucket`, `gcs-bucket` y `aws-flink-sql-job`, y decidir si sus consumers quedan dentro o fuera de la futura adopción.
- Cerrar matriz de component types aceptados por Playmaker, front, cada CP y materializer; los aliases `aws-msk-topic`, `kafka-topic`, `gcp-kafka-topic`, `flink-sql`, `aws-flink-job` y `clickhouse-*` no están alineados en todos los repos.
- Auditar `PROVISION`, `UPDATE` y `DEPROVISION` por separado; varios parsers aceptan operaciones distintas y algunos outputs solo existen en create/update.
- Confirmar con fixtures/test de cada repo los paths que el código acepta pero no están emitidos por el front actual, sin convertir un parser genérico en evidencia de contrato soportado.
- Repetir el discovery contra los commits finales después del merge/release de Context, especialmente Playmaker/SDK y cualquier cambio de contrato de `DeploymentTriggerMessage`.
- Definir con el owner si la futura adopción debe reemplazar solo properties derivadas o también parámetros propios del componente; este proyecto reporta ambos, pero no decide el alcance de implementación.

## 🧩 Subproyectos

```base
filters:
  and:
    - 'type == "project"'
    - 'file.hasLink(this.file)'
views:
  - type: cards
    name: Subproyectos
    order:
      - file.name
      - note.status
      - note.priority
```

## ✅ Tareas

> [!note]+ Ownership y tarea puente
> `#owner/me` = tuya · `#owner/agent` = de un agente · sin owner = clasifícala.
> El board es **adaptativo según `owner` del frontmatter**:
> - **Proyecto humano** (`owner: me`): muestra tus tareas y las **tareas puente** (`#type/supervision`) que representan proyectos de agente. Las tareas de agente **no** aparecen acá; viven en su propio proyecto.
> - **Proyecto de agente** (`owner: agent`): muestra las tareas del agente.

> [!example]- Fuente de tareas — editar / mover de estado aquí
> %% Estados: [ ] To Do · [/] WIP · [r] Review · [x] Done · [-] Canceled. Owners: #owner/me, #owner/agent. Tipos: #type/dev #type/admin #type/research #type/pr-review #type/supervision. Flags: #blocked #waiting #urgent. Ver [[convenciones]]. %%
> - [x] Crear proyecto de agente, scope y corte inicial de repos #owner/agent #type/research #area/meli
> - [x] Verificar consumidores directos en los 7 repos de control plane #owner/agent #type/research #area/meli
> - [/] Completar la matriz field-level de front, Playmaker, SDK y materializer #owner/agent #type/research #area/meli
> - [ ] Auditar paths legacy, outputs, fixtures y operaciones UPDATE/DEPROVISION #owner/agent #type/research #area/meli
> - [ ] Revalidar todos los hallazgos contra los commits finales post-Context #owner/agent #type/research #area/meli
> - [ ] Entregar reporte final con lista de repos/archivos afectados y handoff al rollout de CPs #owner/agent #type/research #area/meli

```dataviewjs
const meta={" ":["To Do","var(--text-muted)","var(--background-modifier-border)"],"/":["WIP","#ba7517","rgba(234,124,12,.18)"],"r":["Review","#185fa5","rgba(55,138,221,.18)"],"x":["Done","#3b6d11","rgba(99,153,34,.18)"],"X":["Done","#3b6d11","rgba(99,153,34,.18)"],"-":["Canceled","var(--text-faint)","var(--background-modifier-border)"]};
function linkify(s){return String(s).replace(/\[\[([^\]|]+)(?:\|([^\]]+))?\]\]/g,(m,a,b)=>`<a class="internal-link" href="${a}" data-href="${a}">${b||a}</a>`).replace(/#[\w/-]+/g,m=>`<span style="opacity:.55;font-size:12px">${m}</span>`).replace(/📅\s*(\d{4}-\d{2}-\d{2})/g,(m,d)=>`<span style="opacity:.7;font-size:12px">📅 ${d}</span>`).replace(/[⏫🔼🔽⏬🔺]/g,"").replace(/✅\s*(\d{4}-\d{2}-\d{2})/g,"");}
function has(t,tag){return new RegExp(`(^|\\s)#${tag}(\\s|$)`).test(String(t.text));}
function render(tasks){const el=dv.el('div','');el.innerHTML=tasks.map(t=>{const[label,fg,bg]=meta[t.status]||["?","var(--text-muted)","var(--background-modifier-border)"];return `<div style="display:flex;align-items:center;gap:8px;margin:5px 0;"><span style="font-size:11px;font-weight:600;padding:1px 9px;border-radius:999px;background:${bg};color:${fg};min-width:56px;text-align:center;flex:none;">${label}</span><span>${linkify(t.text)}</span></div>`;}).join("");}
function board(tasks){const cols=[[" ","🟦 To Do"],["/","🟡 WIP"],["r","🔵 Review"]];let any=false;for(const[st,label]of cols){const c=tasks.filter(t=>t.status===st);if(c.length){any=true;dv.el('h4',label);render(c);}}const done=tasks.filter(t=>t.status==="x"||t.status==="X");if(done.length){any=true;dv.el('h4',"✅ Done");render(done);}if(!any)dv.paragraph("_Sin tareas._");}
const owner=((dv.current().owner)==="agent")?"agent":"me";
const all=dv.current().file.tasks.array();
const primary=all.filter(t=>has(t,`owner/${owner}`));
const loose=all.filter(t=>!has(t,"owner/me")&&!has(t,"owner/agent"));
dv.header(3, owner==="agent"?"🤖 Tareas del agente":"🧍 Mis tareas");
board(primary);
if(loose.length){dv.header(3,"🧺 Sin owner (clasificar)");render(loose);}
```

%% Rollup de iniciativa — descomentar solo en proyectos padre para ver las tareas #owner/me (incluye puentes) de todos los subproyectos, agrupadas por nota. Cambiar la ruta por la carpeta de esta iniciativa. Nunca muestra tareas de agente.
```dataviewjs
const meta={" ":["To Do","var(--text-muted)","var(--background-modifier-border)"],"/":["WIP","#ba7517","rgba(234,124,12,.18)"],"r":["Review","#185fa5","rgba(55,138,221,.18)"],"x":["Done","#3b6d11","rgba(99,153,34,.18)"],"X":["Done","#3b6d11","rgba(99,153,34,.18)"],"-":["Canceled","var(--text-faint)","var(--background-modifier-border)"]};
const ord={" ":0,"/":1,"r":2,"x":3,"X":3,"-":4};
function linkify(s){return String(s).replace(/\[\[([^\]|]+)(?:\|([^\]]+))?\]\]/g,(m,a,b)=>`<a class="internal-link" href="${a}" data-href="${a}">${b||a}</a>`).replace(/#[\w/-]+/g,m=>`<span style="opacity:.55;font-size:12px">${m}</span>`).replace(/📅\s*(\d{4}-\d{2}-\d{2})/g,(m,d)=>`<span style="opacity:.7;font-size:12px">📅 ${d}</span>`).replace(/[⏫🔼🔽⏬🔺]/g,"").replace(/✅\s*(\d{4}-\d{2}-\d{2})/g,"");}
function has(t,tag){return new RegExp(`(^|\\s)#${tag}(\\s|$)`).test(String(t.text));}
function render(tasks){const el=dv.el('div','');el.innerHTML=tasks.map(t=>{const[label,fg,bg]=meta[t.status]||["?","var(--text-muted)","var(--background-modifier-border)"];return `<div style="display:flex;align-items:center;gap:8px;margin:5px 0;"><span style="font-size:11px;font-weight:600;padding:1px 9px;border-radius:999px;background:${bg};color:${fg};min-width:56px;text-align:center;flex:none;">${label}</span><span>${linkify(t.text)}</span></div>`;}).join("");}
const pages=dv.pages('"10-projects/CARPETA-DE-LA-INICIATIVA"');
for(const p of pages.sort(x=>x.file.name)){const t=p.file.tasks.array().filter(x=>has(x,"owner/me")&&x.status!=="x"&&x.status!=="X").sort((a,b)=>(ord[a.status]??9)-(ord[b.status]??9));if(t.length){dv.el('h4',p.file.link);render(t);}}
```
%%

## 📆 Bitácora

%% Log diario para las dailies. Una línea por día con lo avanzado / blockers. %%
- **2026-08-25** — Proyecto materializado como `owner: agent` bajo [[Crear Context]]; se definió la tarea puente y se congeló el universo de 13 repos sin copiar clones ni dumps al vault.
- **2026-08-25** — Primera pasada de código verificada contra 7 CPs: Kafka consume params planos y prefijos; Flink consume `properties_map` como propiedades KDA; ClickHouse consume mapa plano/nested con aliases; Fury consume descriptores y rate limit; Observability consume prefijos; KMS y Signals no tienen consumidor de deployment params en sus HEADs.
- **2026-08-25** — Lint estricto de las tres notas canónicas PASS; Graphify update quedó bloqueado por 11 errores y 6 warnings de deuda preexistente fuera del proyecto, por lo que la fuente Markdown sigue siendo válida y el índice derivado queda pendiente.
- **2026-08-25** — Sesión cerrada con continuidad preservada; próximo paso exacto: completar la matriz field-level de front, Playmaker, SDK y materializer, y luego revalidar contra los commits finales post-Context.

## 🧭 Decisiones

- El discovery vive en un proyecto de comprensión separado del proyecto de cambio [[Crear Context]]; el rollout de Context en CPs no empieza desde esta nota hasta cerrar la matriz y obtener revisión humana.
- Se auditan repos externos por `repo + path relativo + commit`; no se persisten rutas absolutas ni clones en el vault.
- `signals-context-flow` se usa como índice/historial de discovery, pero cada afirmación nueva se valida contra el código del commit declarado.
- La tarea puente del padre solo puede avanzar a Review cuando este proyecto entregue el reporte final; el agente no la marca Done.

## 🔗 Docs / Links

- [[Crear Context]]
- [[signals-context-flow]]
- [[RIO]]
- [[rio-playmaker]] · [[rio-sdk-events]] · [[rio-controlplane-kafka]] · [[rio-controlplane-flink]] · [[rio-controlplane-clickhouse]] · [[rio-controlplane-fury]] · [[rio-controlplane-kms]] · [[rio-controlplane-observability]] · [[rio-controlplane-signals]]
- [[rio-materializer]] · [[ads-signals-frontend]] · [[rio-frontend]] · [[ads-signals-catalog]]

## 💡 Ideas

%% Captura ideas sueltas del proyecto al final. Si maduran, promover a tarea o a nota de idea (70-templates/idea.md). %%

### Backlog de ideas

- Crear una matriz machine-readable `component_type × operation × input_path × consumer × output_path` solo después de cerrar la evidencia humana; no reemplaza esta nota.

### Motivos / principios

- Separar lo que el front inventa/deriva de lo que el usuario configura y de lo que el runtime inyecta; esa separación define qué debe migrar a Context y qué sigue siendo configuración del CP.

### Memoria pública / interna

%% Opcional para proyectos de agentes o conocimiento: definir qué memoria gobierna el sistema y cuál gobierna el agente, y por qué existe cada una. %%
- **Memoria pública:** 
- **Memoria interna:** 
- **Motivo:** La comprensión durable debe quedar en esta nota y en las páginas canónicas de aplicaciones; la memoria interna solo debe guardar deltas de continuidad que cambien la siguiente acción.
