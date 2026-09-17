---
type: doc
schema_version: 1
status: active
area: "[[Meli]]"
related:
  - "[[scope-naming-standard]]"
  - "[[Estandarización de Scopes RIO]]"
  - "[[POC KISS — Routing de scopes en Playmaker]]"
  - "[[rio-playmaker]]"
  - "[[rio-sdk-events]]"
aliases:
  - SPEC Playmaker scopes RIO
  - POC KISS scope alpha Playmaker
tags:
  - kind/doc
  - area/meli
  - project/scopes-rio
  - tech/rio-playmaker
created: "2026-09-16"
updated: "2026-09-16"
---

# Technical Specification — Routing KISS por scope en `rio-playmaker`

**Feature**: `rio-playmaker-scope-filter-routing`
**Owner**: Rodrigo Jara
**Project**: Signals (`rio-playmaker`)
**Status**: DRAFT — lista para revisión independiente
**Deriva de**: [SIG-599](https://spellbook.adminml.com/projects/SIG/specs/SIG-599), especialmente US-12, y [[scope-naming-standard]]
**Plan ejecutable**: [[POC KISS — Routing de scopes en Playmaker]]
**Baseline revisada**: `rio-playmaker origin/master@f350fb26091d` y `rio-sdk-events master@3e3acd1`; el refresh remoto de Playmaker quedó bloqueado por la allowlist de GitHub sin GlobalProtect, por lo que la Fase 0 debe revalidar el SHA antes de implementar

## Propósito

Demostrar en la lane `alpha` que Playmaker captura `X-Rio-Scope`, valida que coincide con su runtime `alpha-api-nonprod`, persiste el ambiente lógico en la ejecución, publica los triggers de deployment con el filtro BigQueue `scope:alpha` y sólo aplica resultados cuyo filtro coincide con el runtime `alpha-consumer-nonprod` y con la ejecución persistida. La POC reutiliza los tópicos, payloads y clientes existentes; no agrega `environment_scope` a `DeploymentTriggerMessage` ni a `DeploymentResultMessage`.

## Contenido

### Interpretación técnica del funcional

SIG-599 exige que el ambiente lógico se conserve durante todo el recorrido y que el mensaje lleve `scope:<environment>`. En esta POC, `environment_scope` es el valor semántico persistido por Playmaker y `scope:<environment>` es su representación en el envelope BigQueue. No se duplica el mismo dato dentro del payload SDK: esa duplicación no agrega aislamiento y abre dos autoridades que podrían contradecirse.

La solución queda intencionalmente acotada a `rio-deployment-trigger` y `rio-deployment-result`. La ampliación a Actions, `DataProductChanged`, Materializer, KMS, runtime status u otros tópicos requiere otra SPEC.

### Baseline verificada

| Evidencia | Estado actual | Consecuencia |
|---|---|---|
| `PipelineDeploymentController.deployPipeline` recibe `@RequestHeader Map<String,String>` y lo entrega a `PipelineDeployService` | `HEAD` | No hace falta un interceptor global para capturar el header en la POC |
| `PipelineDeployServiceImpl.deploy` usa headers para Tiger y creación de servicios, pero no resuelve scope | `HEAD` | El ambiente debe resolverse una vez al inicio del deploy y pasarse al lifecycle |
| `PipelineExecutionModel` es la raíz persistida del orchestration flow | `HEAD` | `environment_scope` pertenece a `pipeline_execution`, no a `ThreadLocal` ni a cada deployment |
| La idempotencia consulta `desiredStateHash + pipelineId + status` | `HEAD` | Alpha y otra lane sobre la DB test podrían colisionar; la consulta debe incluir `environmentScope` |
| `DispatchRequest` es inmutable y cruza `@Async AFTER_COMMIT` | `HEAD` | Debe transportar el scope persistido para el primer publish sin depender del request HTTP |
| `DeploymentTriggerProducerImpl` usa mqclient `3.4.9` y `producer.send(message)` | `HEAD` | Se cambia sólo a la sobrecarga existente `send(message, new Filters(...))`; no se migra el producer |
| `DeploymentTimeoutJob.retry` reconstruye el trigger desde `DeploymentGroup → PipelineExecution` | `HEAD` | Los retries deben recuperar `environmentScope` desde la ejecución y republicar el mismo filtro |
| `DeploymentResultConsumerController` deserializa `BigQueueMessage<DeploymentResultMessage>` pero descarta `envelope.filters()` | `HEAD` | El controller debe conservar el envelope para validar antes de mutar estado |
| `rio-sdk-events` ya expone `BigQueueMessage.filters()`, `BigQueueFilters.modifiedFields()` y `BigQueueClient.sendWithFilters` | `CONTRACT` | No se modifica el SDK ni los DTOs de deployment |
| mqclient `3.4.9` expone `Producer.send(Object, com.mercadolibre.mqclient.entity.Filters)` | `CONTRACT` | El producer actual puede publicar filtros sin reemplazar la dependencia |

### Arquitectura objetivo

```text
ads-signals-frontend
  │ X-Rio-Scope: alpha
  ▼
Fury Route test ──► alpha-api-nonprod
                       │ resolver header == ambiente(runtime)
                       │ persist pipeline_execution.environment_scope = alpha
                       ▼
                rio-deployment-trigger--nonprod
                filters.modified_fields = ["scope:alpha"]
                       │
                       ▼
             Flink alpha consumer [FUERA DE ESTA SPEC]
                       │ preserva scope:alpha en result
                       ▼
                rio-deployment-result--nonprod
                filters.modified_fields = ["scope:alpha"]
                       │
                       ▼
                alpha-consumer-nonprod
                filtro == runtime == ejecución persistida
                       │
                       └─ sólo entonces muta Deployment/ComponentRun/PipelineExecution
```

Componentes modificados:

- `[MODIFIED]` ingreso HTTP del deploy, lifecycle de `PipelineExecution`, idempotencia, carrier asíncrono, producer BigQueue, retries y controller/consumer de resultados.
- `[UNCHANGED]` payloads `DeploymentTriggerMessage` y `DeploymentResultMessage`, nombres de tópicos, `withSegmentID`, handlers de negocio después del guard y otros eventos.
- `[EXTERNAL]` Fury Route, binding/filter server-side del consumer y propagación del filtro en Flink.

### Contrato de ingreso HTTP

Header estándar de la POC:

```http
X-Rio-Scope: alpha
```

Reglas:

1. Sólo se activa con `rio.scope-routing.enabled=true`; el default es `false` para no cambiar los scopes actuales.
2. Con la feature habilitada, el header es obligatorio, se normaliza a lowercase y debe cumplir `^[a-z0-9][a-z0-9-]{0,62}$`.
3. El ambiente esperado se deriva del primer token del `SCOPE` materializado sólo cuando el nombre completo cumple `^([a-z0-9]+)-(api|consumer)-(nonprod|nonsite)$`; para la POC los valores válidos son `alpha-api-nonprod` y `alpha-consumer-nonprod`.
4. Header ausente o malformado produce `400 Bad Request`; un valor bien formado distinto del ambiente del runtime produce `409 Conflict`.
5. El header es una declaración del caller, no la autoridad final: Playmaker sólo persiste el valor después de compararlo con su runtime.
6. La POC aplica el contrato al `POST /data-products/{name}/environments/{envName}/pipeline/deploy`. Los GET de history/detail pueden incorporar el mismo guard en esta fase si el frontend los consulta a través del entrypoint compartido; nunca deben devolver una ejecución cuyo `environmentScope` no coincide con el runtime.

No se usa `ThreadLocal`, MDC ni request-scoped bean como carrier de negocio: el publish ocurre después del commit y puede ejecutarse en otro thread o en un retry sin request original.

### Contrato persistido

Se agrega una columna nullable por compatibilidad:

```sql
ALTER TABLE pipeline_execution ADD COLUMN environment_scope VARCHAR(63) NULL;
CREATE INDEX idx_pe_scope_pipeline_hash_status ON pipeline_execution (environment_scope, pipeline_id, desired_state_hash, status);
```

El nombre SQL definitivo puede ajustarse al estándar de índices del repo sin cambiar el contrato. Deben existir migraciones equivalentes para `playmkrtst`, `playmkrstg` y `playmkrprod`, aunque la feature sólo se habilite en alpha. No se hace backfill: filas legacy quedan `NULL` y conservan su comportamiento mientras la feature esté apagada.

Para ejecuciones creadas con scope routing habilitado:

- `environmentScope` es obligatorio en el lifecycle y queda inmutable.
- Las búsquedas de idempotencia `COMPLETED`, `RUNNING` y `PENDING` incluyen `environmentScope`.
- La ejecución es la autoridad para todos los batches, publishes y retries posteriores.
- Una ejecución con `NULL` no puede publicar ni consumir por la ruta scoped; falla cerrado y emite señal acotada.

### Contrato del envelope BigQueue

El payload SDK no cambia. El mensaje publicado debe verse conceptualmente así:

```json
{
  "filters": {
    "modified_fields": ["scope:alpha"]
  },
  "msg": {
    "deployment_id": "<uuid>",
    "deployment_group_id": "<uuid>",
    "component_type": "aws-flink-sql",
    "operation": "PROVISION",
    "schema_version": 1,
    "published_at": "<instant>",
    "...": "payload existente sin environment_scope"
  }
}
```

Reglas del filtro:

- Tag canónico: `scope:<environmentScope>`.
- Debe existir exactamente un tag con prefijo `scope:`; pueden coexistir otros tags no relacionados.
- El producer construye el tag desde el scope persistido, nunca directamente desde el header crudo.
- Primer dispatch, siguientes batches y retries publican el mismo tag.
- `bigqueue.segment` y `ProducerBuilder.withSegmentID` continúan eligiendo el segmento físico; no seleccionan `alpha`.

### Publicación del trigger

`DispatchRequest` incorpora `String environmentScope`. `DispatchRequestFactory` lo lee desde `group.getPipelineExecution().getEnvironmentScope()` y valida no-null cuando la feature está activa. `BigQueueDispatchAdapter` entrega el scope junto al mensaje; la interfaz `DeploymentTriggerProducer` puede recibir `publish(message, environmentScope)` o un value object mínimo equivalente. `DeploymentTriggerProducerImpl` llama `producer.send(message, new Filters(List.of("scope:" + environmentScope)))`.

`DeploymentTimeoutJob.retry` ya recupera `DeploymentGroup` y su `PipelineExecution`; debe obtener el scope desde esa relación y usar la misma API filtrada. No existe fallback a `send(message)` en una ejecución scoped: un publish sin filtro rompería el aislamiento.

### Consumo del resultado y defensa en profundidad

El endpoint conserva el envelope completo hasta terminar el guard. La validación ocurre antes de `DeploymentResultConsumerService.consume` y antes de cualquier transición de `Deployment`, `ComponentRun`, `Service` o `PipelineExecution`.

Para un resultado scoped se evalúa:

```text
scope del filtro == scope lógico del runtime consumer == scope de la PipelineExecution correlacionada
```

Resolución de la ejecución:

- Para deploy/undeploy/rollback, se mantiene la correlación existente desde `deploymentId` hacia `Deployment → DeploymentGroup → PipelineExecution`.
- Para `INACTIVATE`, la correlación actual usa el propio `deploymentId` como execution ID; queda fuera de la POC porque Actions/inactivation no forman parte del recorrido alpha.

Si falta el filtro, está malformado, contiene más de un `scope:`, no coincide con el runtime o no coincide con la ejecución, el consumer responde `200 OK`, no ejecuta side effects y registra un drop. Se hace ACK porque un retry del mismo envelope nunca corregirá un scope determinístico y sólo produciría poison-loop. Fallos transitorios de DB o infraestructura posteriores a un guard válido continúan propagándose como 5xx según el comportamiento actual.

### Errores y observabilidad

| Escenario | Respuesta/acción | Métrica o log |
|---|---|---|
| Header ausente o inválido con feature activa | `400`; no crea ejecución | reason acotado `missing_header` o `invalid_header` |
| Header válido distinto del runtime | `409`; no crea ejecución | `runtime_mismatch` |
| Ejecución scoped sin scope al publicar | falla el dispatch; no usa publish legacy | `missing_persisted_scope` |
| Result sin filtro o filtro inválido | `200`; ACK sin side effect | `missing_filter` o `malformed_filter` |
| Filtro distinto del runtime consumer | `200`; ACK sin side effect | `runtime_mismatch` |
| Filtro distinto de la ejecución | `200`; ACK sin side effect | `execution_mismatch` |
| Error transitorio luego de validar | conserva 5xx/retry actual | señal existente del handler |

Las métricas usan motivos y outcomes de cardinalidad acotada. No agregan el scope dinámico, IDs, header crudo ni contenido del filtro como tag. Los logs pueden incluir execution/deployment ID ya usado por el flujo y el reason, pero no el mapa completo de headers.

### Compatibilidad y feature flag

- `rio.scope-routing.enabled=false` preserva el comportamiento actual: no exige header, crea ejecuciones con `environment_scope=NULL`, publica sin filtro y procesa results legacy.
- `rio.scope-routing.enabled=true` activa el contrato completo y fail-closed; no se permiten mezclas parciales dentro de una ejecución.
- Alpha API y alpha consumer deben habilitarse juntos después de que Fury y Flink estén listos. No se habilita en `prod` durante la POC.
- La columna nullable permite rollback de aplicación sin rollback destructivo de schema.
- No se incrementa `DeploymentSchemaVersion` ni se publica una nueva versión de `rio-sdk-events`.

### Design Decisions

- **DD-1 — filtro, no campo SDK:** `environment_scope` se persiste en Playmaker y viaja como `filters.modified_fields=["scope:alpha"]`. Se descarta agregarlo a ambos DTOs porque el SDK ya modela el envelope y duplicar el dato permite inconsistencias payload/filtro.
- **DD-2 — ejecución como autoridad:** `PipelineExecutionModel` conserva el scope de la operación. Se descartan `ThreadLocal`, MDC y lectura tardía del header porque el orchestration flow usa `AFTER_COMMIT`, async y retry.
- **DD-3 — mqclient existente:** se usa la sobrecarga de `Producer.send` con `Filters`. Se descarta migrar los producers a `BigQueueClient` en la POC porque no es necesario para el resultado funcional.
- **DD-4 — ACK de mismatch:** un result con scope inválido se descarta con `200` y métrica bounded. Se descarta retry/DLQ automático porque el mismo mensaje nunca se vuelve correcto y podría bloquear el consumer.
- **DD-5 — runtime valida header:** el primer token del nombre Fury estandarizado define el ambiente esperado; el header sólo puede coincidir. Se descarta confiar directamente en el browser.
- **DD-6 — feature flag única:** un switch por runtime activa ingreso, publish y consume scoped. Se descarta una combinación libre de flags parciales que permitiría ejecuciones híbridas.

### Archivos y símbolos afectados

#### Crear

| Archivo sugerido | Propósito |
|---|---|
| `src/main/java/com/mercadolibre/rio/playmaker/service/pipeline/ScopeRoutingResolver.java` | Resolver header/runtime, normalizar ambiente y construir/parsing `scope:<x>` sin estado global |
| `src/main/java/com/mercadolibre/rio/playmaker/config/ScopeRoutingConfig.java` | Exponer `rio.scope-routing.enabled` y el contrato de activación |
| Tres migraciones timestamped bajo `migrations/mysql/playmkrtst`, `playmkrstg` y `playmkrprod` | Agregar `pipeline_execution.environment_scope` e índice equivalente |
| Tests unitarios de resolver/guard | Cubrir parsing, mismatch y fail-closed |

#### Modificar

| Archivo/símbolo | Cambio |
|---|---|
| `PipelineDeploymentController.deployPipeline` / `PipelineDeployServiceImpl.deploy` | Capturar `X-Rio-Scope`, resolverlo contra runtime antes de crear la ejecución y mantener Tiger sin cambios |
| `PipelineExecutionModel`, `PipelineExecutionLifecycleService.create` e impl | Persistir `environmentScope` inmutable |
| `PipelineExecutionRepository` | Incluir scope en idempotencia y, si la POC consulta history compartida, en lecturas de ejecución |
| `DispatchRequest` / `DispatchRequestFactory.build` | Transportar el scope persistido a través de `AFTER_COMMIT` |
| `DeploymentTriggerProducer` / `DeploymentTriggerProducerImpl.publish` | Publicar con `com.mercadolibre.mqclient.entity.Filters` |
| `BigQueueDispatchAdapter.dispatch` | Entregar el scope al producer sin cambiar `DeploymentTriggerMessage` |
| `DeploymentTimeoutJob.retry` | Re-publicar con el scope de `DeploymentGroup.pipelineExecution` |
| `DeploymentResultConsumerController.consumeDeploymentResult` | No descartar `envelope.filters()` y ejecutar el guard antes del servicio |
| `DeploymentResultConsumerService` / impl o guard dedicado | Resolver ejecución, comparar filtro/runtime/persistencia y descartar sin side effects |
| `DeploymentResultMetrics` | Agregar razones bounded de drop sin tag de scope dinámico |
| Config/tests existentes asociados | Default flag false y cobertura de publish/consume/retry/idempotencia |

#### No tocar

- `rio-sdk-events` y sus DTOs `DeploymentTriggerMessage`/`DeploymentResultMessage`.
- Producers de Actions y `DataProductChanged`.
- Materializer adapters y su result producer.
- Nombres de tópicos, `bigqueue.segment`, schema version y lógica de negocio posterior al guard.

### Estrategia de tests

- **Resolver unitario:** `alpha-api-nonprod + alpha` acepta; header ausente/malformado rechaza; `beta` contra alpha produce mismatch; scope runtime no canónico falla cerrado con feature activa; feature apagada conserva legacy.
- **Persistencia/repositorio:** crea `PipelineExecution.environmentScope=alpha`; la misma hash/pipeline puede existir en dos scopes sin colisión; completed/in-flight sólo se reutiliza dentro del mismo scope; filas `NULL` siguen accesibles en legacy.
- **Producer contract:** verifica `Producer.send(message, Filters)` con exactamente `scope:alpha`; nunca llama `send(message)` para una ejecución scoped; excepción MQ conserva `QueueException`.
- **Dispatch async:** el `DispatchRequest` mantiene `alpha` después de `AFTER_COMMIT`; siguiente batch hereda la ejecución; no lee request context.
- **Retry:** `DeploymentTimeoutJob` republica `scope:alpha`; ejecución scoped sin scope no publica; la actualización de retry conserva atomicidad actual.
- **Consumer controller/guard:** envelope válido avanza; `filters=null`, `modified_fields=null`, cero o dos tags `scope:`, tag malformado, runtime mismatch y execution mismatch responden 200 sin llamar al handler y emiten el reason correcto.
- **Integración DB:** una ejecución alpha y una beta con mismo desired-state hash permanecen aisladas en la DB test compartida.
- **E2E externo:** `X-Rio-Scope: alpha` llega a `alpha-api-nonprod`; trigger y result contienen `scope:alpha`; sólo `alpha-consumer-nonprod` procesa; un result alterado se ACKea sin cambio de estado.
- **Calidad:** escribir primero los tests críticos del guard, idempotencia y retry; mantener los checks del repo y alcanzar al menos 95% de cobertura sobre código nuevo.

### Rollout y rollback

1. Validar la SPEC y confirmar con evidencia que Fury filtra server-side `modified_fields` y preserva `X-Rio-Scope` en la route.
2. Aplicar migraciones con feature apagada.
3. Desplegar código compatible con feature apagada en los runtimes existentes.
4. Preparar Flink alpha y los bindings de trigger/result con `scope:alpha`.
5. Habilitar `rio.scope-routing.enabled=true` en `alpha-api-nonprod` y `alpha-consumer-nonprod` como una unidad.
6. Ejecutar golden deploy y negativos de missing/mismatch; observar métricas de drops y ausencia de tráfico en otras lanes.

Rollback: deshabilitar la feature en ambos runtimes alpha y pausar bindings alpha si el recorrido externo está defectuoso. La columna queda nullable y no se elimina. No se hace release productivo desde una feature branch; el rollout usa un release aprobado desde la rama/base definida por el proceso del repo.

### Definition of Done técnica

- Header validado contra runtime antes de persistir.
- `environment_scope=alpha` persistido e incluido en idempotencia.
- Primer dispatch, siguientes batches y retry llevan exactamente `scope:alpha`.
- Result válido requiere igualdad filtro/runtime/ejecución antes de side effects.
- Mismatches se ACKean, se miden con cardinalidad acotada y no mutan estado.
- SDK, payloads, tópicos y otros eventos permanecen sin cambios.
- Tests críticos y E2E generan evidencia enlazable desde el planner.
- Rollback por feature flag probado.

### Fuera de alcance

- Agregar `environment_scope` a `rio-sdk-events` o publicar una versión nueva del SDK.
- Implementar el producer/result de Flink; su SPEC debe preservar el filtro.
- Crear Fury scopes, routes, consumer bindings o topics.
- Extender el contrato a Actions, inactivation, `DataProductChanged`, Materializer, KMS, Observability o runtime status.
- Separar DB por lane, crear un topic por ambiente o migrar todos los producers BigQueue.
- Habilitar producción o resolver compatibilidad histórica general más allá del rollback de la POC.

### Dependencias externas y stop conditions

- Fury debe demostrar que la route test preserva `X-Rio-Scope`, que el target `alpha-api-nonprod` no cruza a producción y que el consumer aplica `scope:alpha` server-side. Sin esa evidencia la integración queda bloqueada, no se implementa un filtro client-side como sustituto silencioso.
- Flink debe publicar `rio-deployment-result` con el mismo filtro recibido. Si no puede preservar filtros sin cambiar el SDK, se registra `PLAN_CONFLICT` y se revisa el diseño; Playmaker no compensa confiando en el payload.
- Si `origin/master` cambia las superficies citadas o mqclient deja de exponer la sobrecarga verificada, el agente detiene la fase afectada y actualiza el planner antes de codificar.

## Fuentes

- [SIG-599](https://spellbook.adminml.com/projects/SIG/specs/SIG-599) y [[scope-naming-standard]]: continuidad del ambiente y routing por `scope:<environment>`.
- `rio-playmaker origin/master@f350fb26091d`: controller de deploy, lifecycle, orchestration asíncrona, producers, retry y result consumer.
- `rio-sdk-events master@3e3acd1`: `BigQueueMessage`, `BigQueueFilters`, `BigQueueClient`, `DeploymentTriggerMessage` y `DeploymentResultMessage`.
- mqclient `3.4.9`: `Producer.send(Object, Filters)` y `Filters(List<String>)`, verificados desde el artefacto resuelto por Gradle.
