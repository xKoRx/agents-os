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
updated: "2026-09-17"
---

# Technical Specification — Routing KISS por scope en `rio-playmaker`

> [!danger] Regla básica e innegociable
> **EL `Environment` DEL PIPELINE NO ES EL SCOPE DE FURY.** El `Environment` existente pertenece al dominio del pipeline y continúa identificando dónde se despliegan sus componentes. `X-Rio-Scope` identifica una lane de infraestructura Fury elegida desde el frontend. Esta POC sólo toma ese header y lo convierte en el filtro BigQueue `scope:<valor>`. No persiste el scope Fury en `PipelineExecution`, no modifica el `Environment` del pipeline, no cambia idempotencia/history y no introduce ningún campo llamado `environment_scope`.

**Feature**: `rio-playmaker-fury-scope-filter`
**Owner**: Rodrigo Jara
**Project**: Signals (`rio-playmaker`)
**Status**: DRAFT — corregida y lista para revisión independiente
**Deriva de**: [SIG-599](https://spellbook.adminml.com/projects/SIG/specs/SIG-599), especialmente US-12, y [[scope-naming-standard]]
**Plan ejecutable**: [[POC KISS — Routing de scopes en Playmaker]]
**Baseline revisada**: `rio-playmaker origin/master@f350fb26091d` y `rio-sdk-events master@3e3acd1`; Fase 0 debe refrescar el SHA con GlobalProtect antes de implementar

## Propósito

Demostrar en la lane `alpha` que Playmaker recibe `X-Rio-Scope: alpha` desde el frontend y publica el deployment trigger existente con `filters.modified_fields=["scope:alpha"]`. El control plane conserva ese mismo filtro al publicar el deployment result y Playmaker mantiene el filtro disponible durante el procesamiento encadenado de esa request. La POC no crea estado de dominio ni persistencia para el scope Fury.

## Contenido

### Dos conceptos que nunca se mezclan

| Concepto | Autoridad | Para qué sirve | Esta POC lo modifica |
|---|---|---|---|
| `Pipeline Environment` | Modelo y tablas actuales de Playmaker | Identifica el ambiente funcional de un data product/pipeline y participa en delta, deployments, history e idempotencia | **No** |
| Scope de Fury | Frontend/MeliLab → `X-Rio-Scope` → Fury Routes | Selecciona la lane de infraestructura y etiqueta mensajes BigQueue como `scope:<x>` | **Sí, sólo como metadata de routing transitoria** |
| Segmento Fury | Configuración `nonprod`/`nonsite` y `withSegmentID` | Selecciona placement físico del tópico/runtime | **No** |

Reglas de separación:

1. `X-Rio-Scope` no se compara con `EnvironmentModel.name`, `environmentId` ni ningún dato del pipeline.
2. `X-Rio-Scope` no participa en hash, idempotencia, history, autorización de environments ni selección de componentes.
3. No se agrega columna a `pipeline_execution`, `deployment_group`, `deployment` ni otra tabla en esta POC.
4. No se agrega `environment_scope`, `fury_scope` ni un equivalente a `DeploymentTriggerMessage` o `DeploymentResultMessage`.
5. El único wire contract nuevo es `scope:<header>` dentro de `filters.modified_fields`.

### Baseline verificada

| Evidencia | Estado actual | Consecuencia KISS |
|---|---|---|
| `PipelineDeploymentController.deployPipeline` ya recibe `@RequestHeader Map<String,String>` | `HEAD` | Se captura el header en el endpoint existente; no se crea interceptor global |
| `PipelineDeployServiceImpl.deploy` pasa por `DeploymentGroupService` y luego por el dispatch async | `HEAD` | El valor se propaga como argumento/value object transitorio hasta `DispatchRequest` |
| `DispatchRequest` es el carrier inmutable consumido por `@Async AFTER_COMMIT` | `HEAD` | Puede transportar `routingScope` sin request context ni DB |
| `DeploymentTriggerProducerImpl` usa mqclient `3.4.9` y `producer.send(message)` | `HEAD` | Se usa la sobrecarga existente `send(message, Filters)` cuando hay scope |
| `DeploymentResultConsumerController` recibe `BigQueueMessage<DeploymentResultMessage>` pero descarta `filters` | `HEAD` | Debe conservar el filtro para continuidad dentro de la request de resultado |
| `rio-sdk-events` ya modela `BigQueueMessage.filters` y `BigQueueFilters.modifiedFields` | `CONTRACT` | No se cambia ni publica el SDK |
| mqclient `3.4.9` expone `Producer.send(Object, Filters)` | `CONTRACT` | No se migra el producer ni se introduce otro cliente |

### Arquitectura objetivo de la POC

```text
frontend
  │ X-Rio-Scope: alpha
  ▼
Fury Route ──► Playmaker alpha
                  │ captura + valida sintaxis
                  │ routingScope="alpha" (sólo memoria)
                  ▼
            DispatchRequest
                  │
                  ▼
rio-deployment-trigger--nonprod
filters.modified_fields=["scope:alpha"]
                  │
                  ▼
Flink alpha [SPEC separada]
                  │ copia el mismo filtro al result
                  ▼
rio-deployment-result--nonprod
filters.modified_fields=["scope:alpha"]
                  │
                  ▼
Playmaker result controller conserva el filtro durante esa request

PipelineExecution / Pipeline Environment / DB / idempotencia / history: SIN CAMBIOS
```

### Contrato HTTP

Header de infraestructura:

```http
X-Rio-Scope: alpha
```

Reglas:

- Nombre canónico del header: `X-Rio-Scope`.
- El valor se normaliza a lowercase y debe cumplir `^[a-z0-9][a-z0-9-]{0,62}$`.
- Header válido: se crea `RoutingScope("alpha")` y se propaga sólo por el command/dispatch en memoria.
- Header ausente: conserva el comportamiento legacy y publica sin filtro; esto permite compatibilidad y rollback sin feature flag.
- Header malformado: `400 Bad Request`; no inicia el deploy.
- El valor no se interpreta como pipeline environment y no se consulta ninguna tabla para validarlo.
- Fury Routes mantiene la autoridad sobre la existencia del scope y el target físico; Playmaker sólo valida forma y transporta el valor.

### Contrato BigQueue

El payload existente no cambia:

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
    "...": "payload actual"
  }
}
```

Reglas:

- Tag exacto: `scope:<routingScope>`.
- La POC agrega exactamente un tag `scope:` y no altera otros filtros existentes.
- `DeploymentTriggerProducerImpl` usa `producer.send(message, new Filters(List.of("scope:" + routingScope)))` cuando el header está presente.
- Sin header se conserva `producer.send(message)`.
- `ProducerBuilder.withSegmentID` permanece igual: segmento y scope son ejes distintos.
- El control plane debe copiar `scope:alpha` al result; esa implementación vive en su propia SPEC.

### Propagación transitoria dentro de Playmaker

Se crea un value object mínimo `RoutingScope` o se usa un `String` validado si el reviewer demuestra que el value object no agrega valor. El dato recorre exclusivamente:

```text
PipelineDeploymentController
  → PipelineDeployService
  → DeploymentGroupService / BatchDispatchService
  → DispatchRequest
  → BigQueueDispatchAdapter
  → DeploymentTriggerProducer
```

En el camino de resultado:

```text
BigQueueMessage.filters
  → DeploymentResultConsumerController
  → DeploymentResultConsumerService / orchestration de la misma request
  → siguiente batch, si se dispara sin perder el contexto del result
```

No se usa `ThreadLocal`, MDC, request-scoped bean ni entidad JPA. `DispatchRequest` ya cruza el boundary `AFTER_COMMIT` como evento in-memory y es el carrier correcto para el primer dispatch.

### Límite consciente de la POC

La POC no promete supervivencia del scope Fury ante restart, timeout job o reanudación sin un header/envelope activo. No se persiste el dato para resolver esos casos. El golden path debe usar un deployment de un batch que complete antes del timeout.

Si después de validar la POC se requiere retry/restart/múltiples batches desacoplados de la request, se abre una decisión de diseño separada sobre el carrier durable correcto. Está prohibido resolverlo silenciosamente usando `PipelineExecution.environment`, agregando una columna `environment_scope` o alterando idempotencia.

### Consumo de resultados

Fury debe entregar al consumer correspondiente sólo los mensajes cuyo filtro coincide con su binding. Playmaker conserva el envelope en vez de descartar `filters` y aplica validación estructural básica:

- Si existe un tag `scope:`, debe ser único y cumplir la misma sintaxis.
- El filtro se pasa a la orquestación sólo para continuidad transitoria del siguiente publish dentro de esa request.
- No se consulta `PipelineExecution`, `EnvironmentModel` ni history para validar el scope.
- Un envelope malformed se ACKea sin ejecutar el handler y registra un reason bounded; un result legacy sin filtros conserva el comportamiento actual durante la POC.

Esta validación no reemplaza el filtro server-side de Fury. Si Fury no filtra antes de entregar, G0 queda bloqueado y no se inventa una capa de aislamiento distinta dentro de Playmaker.

### Errores y observabilidad

| Escenario | Comportamiento | Señal bounded |
|---|---|---|
| Header ausente | Legacy: publish sin filtro | `routing_mode:legacy` |
| Header malformado | `400`, sin deploy | `invalid_header` |
| Header válido | Publish con `scope:<x>` | `routing_mode:filtered` |
| Result legacy sin filters | Procesamiento actual | `routing_mode:legacy` |
| Result con más de un `scope:` o tag malformado | `200`, sin handler | `malformed_filter` |
| Fallo mqclient | Semántica actual de `QueueException` | métrica existente de publish failure |

Ninguna métrica usa el valor dinámico del scope, IDs o headers como tag. Los logs no imprimen el mapa completo de headers ni valores malformados crudos.

### Design Decisions

- **DD-1 — separación absoluta:** pipeline environment y scope Fury son conceptos distintos. El scope Fury no toca modelo, DB, idempotencia ni history.
- **DD-2 — header → filtro:** `X-Rio-Scope` es la única entrada nueva en Playmaker y se transforma directamente en `scope:<valor>`.
- **DD-3 — carrier transitorio:** el valor viaja por parámetros/command/`DispatchRequest`; no existe persistencia de scope en la POC.
- **DD-4 — SDK intacta:** filtros ya están modelados en el envelope; los DTOs de deployment no cambian.
- **DD-5 — mqclient existente:** se usa la sobrecarga `Producer.send(message, Filters)`; no se migra el producer.
- **DD-6 — compatibilidad por ausencia:** sin header/filtro se conserva legacy; no se agrega feature flag para la POC.
- **DD-7 — retries fuera:** retry/restart durable queda explícitamente fuera de alcance; resolverlo después requiere nueva decisión.

### Archivos afectados

#### Crear

| Archivo sugerido | Propósito |
|---|---|
| `src/main/java/com/mercadolibre/rio/playmaker/service/pipeline/RoutingScope.java` | Normalizar el valor del header y construir/parsing `scope:<x>`; omitir si un helper estático más pequeño resulta suficiente |
| Tests unitarios de header/filtro | Cubrir sintaxis y construcción exacta del filtro |

#### Modificar

| Archivo/símbolo | Cambio |
|---|---|
| `PipelineDeploymentController.deployPipeline` | Extraer `X-Rio-Scope` sin confundirlo con `envName` |
| `PipelineDeployService` / `PipelineDeployServiceImpl.deploy` | Propagar el routing scope sin usarlo en lógica de dominio |
| `DeploymentGroupService`, batch dispatch y factories intermedias | Transportar el valor sólo hasta cada `DispatchRequest` del golden path |
| `DispatchRequest` / `DispatchRequestFactory` | Agregar `routingScope` opcional in-memory |
| `BigQueueDispatchAdapter` / `DeploymentTriggerProducer` / impl | Elegir `send(message, Filters)` cuando hay scope |
| `DeploymentResultConsumerController` y consumer service | Conservar/parsing de `envelope.filters` para continuidad transitoria y malformed guard |
| Tests existentes asociados | Verificar payload intacto, filtro exacto y legacy |

#### No tocar

- `PipelineExecutionModel`, `EnvironmentModel`, `PipelineExecutionRepository`, `PipelineHistoryService` y todas las migrations.
- Hash/idempotencia, history/detail/logs, delta, autorización o lifecycle del pipeline.
- `rio-sdk-events`, payload DTOs y `DeploymentSchemaVersion`.
- Nombres de tópicos, segment ID, Actions, inactivation, `DataProductChanged` y Materializer.
- `DeploymentTimeoutJob` en esta POC.

### Estrategia de tests

- Header: `alpha` acepta y normaliza; ausente conserva legacy; malformed produce 400; nunca se compara con `envName` ni `EnvironmentModel`.
- Propagación: `routingScope` cruza controller→service→group/batch→`DispatchRequest` sin JPA ni contexto global.
- Producer: con `alpha` llama exactamente `send(message, Filters(["scope:alpha"]))`; sin header llama `send(message)`.
- Wire: `DeploymentTriggerMessage` serializado es idéntico; `environment_scope`/`fury_scope` no aparece en `msg`.
- Result: envelope válido conserva `scope:alpha`; malformed no llama handler; envelope legacy mantiene comportamiento actual.
- No-regression: ningún test/migration/query de `PipelineExecution`, environment, idempotencia o history cambia por esta feature.
- E2E: front envía `X-Rio-Scope: alpha`, trigger/result llevan `scope:alpha` y sólo el binding alpha recibe el mensaje.
- Calidad: tests críticos primero, checks del repo y ≥95% de cobertura sobre código nuevo.

### Rollout y rollback

1. F0 confirma que Fury Route preserva el header y el consumer filtra `modified_fields` server-side.
2. Playmaker se despliega compatible: header ausente conserva legacy.
3. Flink alpha se despliega preservando el filtro en el result.
4. Front alpha comienza a enviar `X-Rio-Scope: alpha`.
5. Se ejecuta un golden deploy de un batch y los negativos de header/filtro.

Rollback: el frontend deja de emitir el header y los productores vuelven automáticamente al overload legacy. No hay schema, backfill, feature flag ni datos persistidos que revertir. No se hace release productivo desde una feature branch.

### Definition of Done

- La regla `Pipeline Environment ≠ Fury Scope` está visible y cubierta por tests/no-touch.
- `X-Rio-Scope: alpha` produce exactamente `scope:alpha` en el envelope del trigger.
- Flink conserva el filtro en el result y Fury demuestra filtrado server-side.
- El payload SDK y todo el modelo/persistencia del pipeline permanecen iguales.
- Legacy sin header/filtro sigue funcionando.
- La limitación de retry/restart queda explícita y no se maquilla con persistencia.
- Checks, cobertura y E2E generan evidencia enlazable desde el planner.

### Fuera de alcance

- Cualquier cambio en pipeline environment, `PipelineExecution`, DB, migrations, idempotencia o history.
- Cualquier campo `environment_scope`/`fury_scope` en payloads o entidades.
- Retry, timeout y restart con scope durable.
- Código de Flink o infraestructura Fury dentro de este repo.
- Topics nuevos, producción u otros eventos.

### Dependencias externas y stop conditions

- Si Fury no preserva `X-Rio-Scope` o no filtra `modified_fields` server-side, registrar `PLAN_CONFLICT` y bloquear; no compensar con persistencia o comparaciones contra pipeline environment.
- Si el flow real de un único batch no puede propagar el valor hasta `DispatchRequest` sin persistir, registrar `PLAN_CONFLICT`; no tocar modelos JPA.
- Si Flink no puede conservar el filtro en el result usando el envelope existente, revisar su SPEC; no agregar un campo SDK desde este proyecto.

## Fuentes

- [SIG-599](https://spellbook.adminml.com/projects/SIG/specs/SIG-599) y [[scope-naming-standard]].
- `rio-playmaker origin/master@f350fb26091d`: controller, deploy service, dispatch async, producer y result controller.
- `rio-sdk-events master@3e3acd1`: `BigQueueMessage`, `BigQueueFilters`, `BigQueueClient` y payloads de deployment.
- mqclient `3.4.9`: `Producer.send(Object, Filters)` y `Filters(List<String>)`.
