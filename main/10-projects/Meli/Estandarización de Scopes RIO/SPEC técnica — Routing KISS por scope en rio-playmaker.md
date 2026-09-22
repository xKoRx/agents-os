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
updated: "2026-09-21"
---

# Technical Specification — Routing KISS por scope en `rio-playmaker`

> [!danger] Regla básica e innegociable
> **EL `Environment` DEL PIPELINE NO ES EL SCOPE DE FURY.** El `Environment` existente pertenece al dominio del pipeline y continúa identificando dónde se despliegan sus componentes. El scope Fury identifica la instancia de infraestructura donde corre Playmaker. Esta POC deriva la lane exclusivamente desde el `SCOPE` del runtime y la convierte en el filtro BigQueue `scope:<lane>`. No persiste el scope Fury en `PipelineExecution`, no modifica el `Environment` del pipeline, no cambia idempotencia/history y no introduce ningún campo llamado `environment_scope`.

**Feature**: `rio-playmaker-fury-scope-filter`
**Owner**: Rodrigo Jara
**Project**: Signals (`rio-playmaker`)
**Status**: DRAFT — lista para revisión
**Deriva de**: [SIG-599](https://spellbook.adminml.com/projects/SIG/specs/SIG-599) y [[scope-naming-standard]]
**Plan ejecutable**: [[POC KISS — Routing de scopes en Playmaker]]
**Baseline observada**: `rio-playmaker origin/master@f350fb26091d`; refrescar antes de implementar

## Propósito

Demostrar en la lane `alpha` que cada runtime de Playmaker deriva su lane desde `ScopeUtils.getScopeValue()` y publica los deployment triggers y results con `filters.modified_fields=["scope:alpha"]`. El diseño cubre el trigger inicial, el trigger de batch N+1, el retry por timeout y el result sin propagar metadata desde HTTP ni modificar estado de dominio.

## Contenido

## Dos conceptos que nunca se mezclan

| Concepto | Autoridad | Para qué sirve | Esta POC lo modifica |
|---|---|---|---|
| `Pipeline Environment` | Modelo y tablas actuales de Playmaker | Identifica el ambiente funcional de un data product/pipeline y participa en delta, deployments, history e idempotencia | **No** |
| Scope de Fury | Variable `SCOPE` del runtime | Identifica la instancia/lane de infraestructura y origina el tag BigQueue `scope:<lane>` | **Sí, sólo como fuente runtime de routing** |
| Segmento Fury | Configuración `nonprod`/`nonsite` y `ProducerBuilder.withSegmentID` | Selecciona placement físico del tópico/runtime | **Sí, sólo para que el default base sea `nonprod`; sigue siendo un eje distinto del filtro** |

Reglas de separación:

1. `ScopeUtils.getScopeValue()` no se compara con `EnvironmentModel.name`, `environmentId` ni ningún dato del pipeline.
2. La lane no participa en hash, idempotencia, history, autorización de environments ni selección de componentes.
3. No se agrega columna a `pipeline_execution`, `deployment_group`, `deployment` ni otra tabla.
4. No se agrega `environment_scope`, `fury_scope` ni un equivalente a `DeploymentTriggerMessage` o `DeploymentResultMessage`.
5. El tag `scope:<lane>` vive únicamente en `Filters.modifiedFields` del envelope mqclient.

## Baseline técnica

| Evidencia | Estado actual | Consecuencia KISS |
|---|---|---|
| `ScopeUtils.getScopeValue()` lee `System.getenv("SCOPE")` y cae en `local` | Implementado | Es la única fuente de la lane dentro de Playmaker |
| `ScopeUtils.isKnownProfile()` reconoce sólo `local | test | stage | production` | Implementado | El vocabulario canónico requiere una resolución explícita de profile |
| `ScopeUtils.calculateScopeSuffix()` usa el primer token cuando no encuentra un profile conocido | Implementado | `alpha` falla, `prod` no carga `production` y `beta` puede cargar configuración productiva |
| `application.yml` no define datasource y usa `bigqueue.segment: nonsite` | Implementado | El default base debe pasar a datasource stage y segmento nonprod |
| `application-beta.yml` apunta a `playmkrprod`, `rio-deployment-trigger-prod` y `nonsite` | Implementado | `beta-api-nonprod` nunca debe activar el profile `beta` |
| `DeploymentTriggerProducerImpl.publish` usa `producer.send(message)` | Implementado | El overload con `Filters` cubre trigger inicial, N+1 y timeout retry |
| `DeploymentResultProducerImpl.publish` usa `producer.send(message)` | Implementado | El mismo overload cubre results |
| mqclient `3.4.9` expone `Producer.send(Object, Filters)` | Contrato | No se migra el producer ni se cambia el SDK |
| `SegmentationUtils.getSegmentId()` deriva el eje hermano desde `System.getenv("SEGMENT")` con default `legacy` | Precedente de plataforma | Derivar scope/segmento desde el runtime es un patrón conocido |

## Arquitectura objetivo

Fury Routes usa `X-Rio-Scope` para elegir la instancia antes de que la request llegue a Playmaker. El header no es un contrato de Playmaker y no se lee dentro de la aplicación.

```text
frontend -- X-Rio-Scope --> Fury Routes --> Playmaker web/consumer
                                             │
                                             │ SCOPE=alpha-<role>-nonprod
                                             ▼
                                   ScopeUtils.getScopeValue()
                                             │
                         ┌───────────────────┴───────────────────┐
                         ▼                                       ▼
             profile Spring seguro                  lane = primer token válido
             alpha → stage                           alpha → alpha
                         │                                       │
                         │                    ┌──────────────────┴──────────────────┐
                         │                    ▼                                     ▼
                         │       DeploymentTriggerProducerImpl.publish   DeploymentResultProducerImpl.publish
                         │                    │                                     │
                         └────────────────────┴──── send(message, Filters([scope:alpha]))

PipelineExecution / Pipeline Environment / HTTP controller / dispatch / result consumer / SDK: SIN CAMBIOS
```

## Contrato de resolución del runtime

### Fuente

`ScopeUtils.getScopeValue()` continúa leyendo `SCOPE`. No se agrega una segunda fuente, no se consulta el request context y no se acepta un override por header.

### Derivación de lane

Se agrega `ScopeUtils.getLane()` como operación pura sobre el valor de `ScopeUtils.getScopeValue()` con el siguiente contrato:

- Divide el scope por `-`, toma el primer token no vacío y lo normaliza a lowercase.
- Devuelve lane sólo si el token pertenece a `prod | stage | alpha | beta | gamma`.
- Para `alpha-api-nonprod` y `alpha-consumer-nonprod` devuelve `alpha`.
- Para un valor vacío, malformed, legacy o fuera del vocabulario devuelve ausencia; nunca infiere una lane desde role, qualifier, segmento, Spring profile ni pipeline environment.

El tipo concreto puede ser `Optional<String>` o un enum/value object mínimo si los tests demuestran que reduce estados inválidos; el vocabulario debe existir en un único lugar dentro de `ScopeUtils`.

### Resolución del Spring profile

`ScopeUtils.calculateScopeSuffix()` aplica primero la semántica canónica:

| Primer token canónico | Spring profile |
|---|---|
| `prod` | `production` |
| `stage` | `stage` |
| `alpha` | `stage` |
| `beta` | `stage` |
| `gamma` | `stage` |

Después conserva la compatibilidad vigente para `local | test | stage | production` y scopes legacy que ya resuelven esos profiles. Un token desconocido no se convierte en una lane, aunque la resolución legacy de profile pueda conservar su fallback actual.

Casos obligatorios:

| Scope Fury | Lane | Profile |
|---|---|---|
| `stage-api-nonprod` | `stage` | `stage` |
| `alpha-api-nonprod` | `alpha` | `stage` |
| `alpha-consumer-nonprod` | `alpha` | `stage` |
| `beta-api-nonprod` | `beta` | `stage` |
| `gamma-api-nonprod` | `gamma` | `stage` |
| `prod-api-nonsite` | `prod` | `production` |

### Defaults base seguros

`application.yml` define los defaults mínimos de stage para que un scope nuevo sin archivo propio no dependa de recursos productivos:

- `spring.datasource` usa las credenciales, endpoint, driver y base `playmkrstg` equivalentes al profile stage.
- `bigqueue.segment` pasa de `nonsite` a `nonprod`.
- Los nombres base de tópicos nonprod existentes se conservan.
- La resolución canónica de `beta` a profile `stage` impide que `beta-api-nonprod` cargue `application-beta.yml` y vuelve no explotable esa colisión.

## Contrato BigQueue

Los payloads existentes no cambian. El filtro pertenece al envelope construido por mqclient:

```json
{
  "filters": {
    "modified_fields": ["scope:alpha"]
  },
  "msg": {
    "...": "DeploymentTriggerMessage o DeploymentResultMessage actual, sin campos nuevos"
  }
}
```

Reglas:

- Tag exacto: `scope:<lane>`.
- `DeploymentTriggerProducerImpl.publish` resuelve la lane del runtime al publicar y, si existe, usa `producer.send(message, new Filters(List.of("scope:" + lane)))`.
- `DeploymentResultProducerImpl.publish` aplica exactamente la misma regla.
- Lane ausente o fuera del vocabulario usa `producer.send(message)`; no se crea un filtro vacío y no se adivina una lane.
- Cada producer agrega exactamente un tag `scope:` y no modifica el payload.
- `ProducerBuilder.withSegmentID` permanece igual; segmento y scope siguen siendo ejes diferentes.
- El consumer no parsea `envelope.filters`, no valida estructura y no propaga el tag. Sólo recibe lo que su binding server-side le entrega.

## Cobertura de los cuatro caminos

| Camino | Runtime que publica | Punto único de implementación | Resultado esperado en alpha |
|---|---|---|---|
| Primer batch del deploy | Scope web | `DeploymentTriggerProducerImpl.publish` | `scope:alpha` |
| Batch N+1 | Scope consumer | `DeploymentTriggerProducerImpl.publish` | `scope:alpha` |
| Retry por timeout | Runtime cuyo `DeploymentTimeoutJob` reclama el deployment | `DeploymentTriggerProducerImpl.publish` | `scope:<lane del runtime>` |
| Result | Scope que adapta/publica el resultado | `DeploymentResultProducerImpl.publish` | `scope:alpha` |

La coincidencia entre web y consumer no requiere coordinación: `alpha-api-nonprod` y `alpha-consumer-nonprod` derivan el mismo primer token.

## Errores y observabilidad

| Escenario | Comportamiento | Señal bounded |
|---|---|---|
| Lane válida | Publish con `scope:<lane>` | `routing_mode:filtered` |
| Lane ausente, malformed o desconocida | Publish legacy sin filtro | `routing_mode:legacy` |
| Fallo mqclient | Semántica actual de `QueueException` | Métrica existente de publish failure |

Ninguna métrica usa la lane, el scope completo, IDs o variables de entorno como tag dinámico. Los logs operativos pueden registrar el modo `legacy|filtered`, pero no necesitan imprimir el valor completo de `SCOPE`.

## Design Decisions

- **DD-1 — separación y autoridad runtime:** pipeline environment y scope Fury son conceptos distintos; la única fuente de lane dentro de Playmaker es `ScopeUtils.getScopeValue()` y el dato no toca modelo, DB, idempotencia ni history.
- **DD-4 — contratos de aplicación intactos:** no existe carrier por request, no se lee `X-Rio-Scope`, no se modifica controller/dispatch/consumer y los DTOs de deployment permanecen iguales.
- **DD-5 — mqclient existente:** se usa la sobrecarga `Producer.send(message, Filters)`; no se migra el producer.
- **DD-6 — compatibilidad por fallback:** lane no resoluble publica sin filtro; no se agrega feature flag ni se inventa una lane.

## Archivos afectados

### Modificar

| Archivo/símbolo | Cambio |
|---|---|
| `ScopeUtils.calculateScopeSuffix()` | Mapear scopes canónicos a profiles seguros y conservar compatibilidad legacy |
| `ScopeUtils.getLane()` | Derivar el primer token y validarlo contra el vocabulario canónico |
| `application.yml` | Agregar datasource `playmkrstg` y cambiar el segmento base a `nonprod` |
| `DeploymentTriggerProducerImpl.publish` | Publicar con filtro cuando `ScopeUtils.getLane()` resuelva una lane |
| `DeploymentResultProducerImpl.publish` | Aplicar la misma regla al result |
| Tests de utility, configuración y producers | Cubrir matriz, fallback, payload y ambos overloads |

### No tocar

- `PipelineDeploymentController`, `PipelineDeployService`, sus implementaciones y el flujo HTTP.
- `DeploymentGroupService`, `BatchDispatchService`, `DispatchRequest`, `DispatchRequestFactory` y `BigQueueDispatchAdapter`.
- `DeploymentResultConsumerController`, consumer services y parsing del envelope.
- `PipelineExecutionModel`, `EnvironmentModel`, repositories, migrations, idempotencia, history/detail/logs y lifecycle del pipeline.
- `rio-sdk-events`, payload DTOs y `DeploymentSchemaVersion`.
- Nombres de tópicos, Actions, inactivation, `DataProductChanged` y Materializer.
- `DeploymentTimeoutJob`; queda cubierto porque ya publica mediante `DeploymentTriggerProducerImpl.publish`.

## Estrategia de tests

- `ScopeUtils`: matriz completa de scope→lane→profile; normalización de mayúsculas; valores vacíos, delimitadores, legacy y desconocidos; compatibilidad de `local | test | stage | production`.
- Configuración: el contexto base obtiene datasource `playmkrstg` y segmento `nonprod`; alpha/beta/gamma usan profile stage; prod usa production; beta nonprod nunca carga recursos de `application-beta.yml`.
- Trigger producer: lane alpha llama exactamente `send(message, Filters(["scope:alpha"]))`; lane no resoluble llama exactamente `send(message)`.
- Result producer: misma matriz filtered/legacy.
- Wire: `DeploymentTriggerMessage` y `DeploymentResultMessage` serializados permanecen idénticos; no aparecen `environment_scope`, `fury_scope` ni campos equivalentes.
- No-regression: ningún test, query, model, controller, dispatch, consumer, migration o SDK cambia por esta feature.
- E2E: deploy alpha con más de un batch verifica trigger inicial, result, batch N+1 y retry por timeout con `scope:alpha`.
- Calidad: tests críticos primero, checks del repo y ≥95% de cobertura sobre código nuevo.

## Rollout y rollback

1. Implementar y desplegar primero la resolución segura de profiles y defaults base.
2. Crear o validar `alpha-api-nonprod` y `alpha-consumer-nonprod`; ambos deben cargar profile stage, datasource `playmkrstg` y segmento `nonprod`.
3. Desplegar los dos producers con filtro y confirmar `routing_mode` en un smoke controlado.
4. Ejecutar un deploy alpha multibatch y capturar evidencia de trigger inicial, result y batch N+1.
5. Provocar un timeout controlado y verificar el retry `scope:alpha`.

Rollback: revertir el artefacto y la configuración de Playmaker a la versión anterior. No hay schema, backfill, estado persistido ni cambios de frontend que revertir. No se hace release productivo desde una feature branch.

## Limitación aceptada de la POC

Las lanes nonprod comparten la base `playmkrtst` y `DeploymentRepository.findByStatusInAndTimeoutAtBefore` escanea por `status + timeout_at` sin discriminador de lane. El `DeploymentTimeoutJob` de una lane puede reclamar un deployment creado por otra y publicar el retry mediante `DeploymentTriggerProducerImpl.publish`, que estampará su propia lane runtime. Es asumible para la POC. Resolverlo requiere estado durable y una decisión separada; no se agregan columnas ni se toca `PipelineExecution` en este proyecto.

## Definition of Done

- La regla `Pipeline Environment ≠ Fury Scope` está visible y respetada por el diff.
- Todos los scopes canónicos resuelven una lane y un Spring profile seguros según la matriz.
- El default base usa datasource `playmkrstg` y segmento `nonprod`.
- `DeploymentTriggerProducerImpl.publish` y `DeploymentResultProducerImpl.publish` generan exactamente `scope:alpha` en runtime alpha.
- Trigger inicial, result, batch N+1 y retry por timeout quedan certificados en E2E.
- Lane no resoluble mantiene el publish legacy sin filtro.
- Payloads, SDK, controller/dispatch/consumer, modelo y persistencia del pipeline permanecen iguales.
- La limitación cross-lane del timeout job queda documentada y no se maquilla con persistencia.
- Checks, cobertura ≥95%, E2E y rollback generan evidencia enlazable desde el planner.

## Fuera de alcance

- Cualquier cambio en pipeline environment, `PipelineExecution`, DB, migrations, idempotencia o history.
- Lectura o validación de `X-Rio-Scope` en Playmaker.
- Carrier transitorio o durable en controller, services, dispatch o consumers.
- Parsing o validación de `envelope.filters` en el result consumer.
- Campos `environment_scope`/`fury_scope` en payloads o entidades.
- Aislamiento durable de retries entre lanes.
- Código de infraestructura Fury dentro de este repo, topics nuevos, producción u otros eventos.

## Dependencias y stop conditions

- Fury aplica filtros server-side por decisión cerrada del owner; no existe spike, gate ni fallback a topics separados.
- Si los scopes canónicos no pueden usar profiles stage/production sin cargar recursos productivos incorrectos, registrar `PLAN_CONFLICT` y no crear las lanes.
- Si mqclient no soporta el overload contratado, registrar `PLAN_CONFLICT`; no agregar campos al payload ni cambiar el SDK.
- Si un camino de los cuatro no converge en los dos producers identificados, reabrir F1 con evidencia; no propagar scope por controllers, dispatches, consumers ni entidades.

## Fuentes

- [SIG-599](https://spellbook.adminml.com/projects/SIG/specs/SIG-599) y [[scope-naming-standard]].
- `rio-playmaker origin/master@f350fb26091d`: `ScopeUtils`, profiles Spring, configuración base, ambos producers, avance de batch y timeout job.
- mqclient `3.4.9`: `Producer.send(Object, Filters)` y `Filters(List<String>)`.
- `com.fury.toolkit.shared.SegmentationUtils.getSegmentId()` como precedente del patrón runtime para el eje de segmento.
