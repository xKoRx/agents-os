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
updated: "2026-09-22"
---

# Technical Specification — Routing KISS por scope en `rio-playmaker`

> [!danger] Regla básica e innegociable
> **EL `Environment` DEL PIPELINE NO ES EL SCOPE DE FURY.** El primero sigue siendo dominio funcional. La lane de infraestructura se obtiene sólo del scope Fury del runtime y vive únicamente como filtro BigQueue. No se persiste en `PipelineExecution`, no participa en idempotencia/history y no crea `environment_scope`.

**Feature**: `rio-playmaker-fury-scope-filter`
**Owner**: Rodrigo Jara
**Status**: DRAFT revisado con criterio KISS/YAGNI
**Plan ejecutable**: [[POC KISS — Routing de scopes en Playmaker]]
**Baseline observada**: `rio-playmaker origin/develop@625f491d218e`; corte 2026-09-22

## Propósito

Hacer que las instancias canónicas alpha de Playmaker resuelvan `RuntimeLane(alpha)` al startup y publiquen todos los deployment triggers incluidos en la POC y los deployment results con `filters.modified_fields=["scope:alpha"]`.

La solución no lee `X-Rio-Scope`, no transporta metadata por request, no tiene fallback sin filtro y no intenta resolver timeout/retry cross-lane.

## Contenido

## Decisión KISS

- Un scope Fury canónico produce una lane inmutable al startup o la aplicación no arranca.
- Tres puntos de publicación cambian a `Producer.send(message, Filters)`: los dos deployment trigger producers activos y el result producer.
- Local/tests conservan sus implementaciones locales; no existe modo legacy dentro del runtime alpha.
- El timeout processing se deshabilita en alpha porque la DB compartida no tiene ownership por lane.
- No se agregan carrier, columnas, DTOs, SDKs, topics por lane ni abstracciones compartidas.

## Dos conceptos que nunca se mezclan

| Concepto | Autoridad | Uso |
|---|---|---|
| Pipeline Environment | Modelo/tablas actuales | Dominio del data product, delta, deployments, history e idempotencia |
| Scope Fury | Runtime Fury | Resolver `RuntimeLane` y construir `scope:<lane>` |
| Segmento Fury | Config `nonprod`/`nonsite` | Placement físico; no selecciona la lane |

## Baseline técnica

| Evidencia | Estado actual | Cambio requerido |
|---|---|---|
| `ScopeUtils.getScopeValue()` lee `SCOPE` y cae en `local` | Implementado | No usar ese fallback para routing canónico |
| `ScopeUtils.calculateScopeSuffix()` no mapea correctamente todas las lanes | Implementado | `prod→production`; `stage/alpha/beta/gamma→stage` |
| `application.yml` no tiene defaults seguros y usa segmento `nonsite` | Implementado | Defaults stage/nonprod para nuevos scopes nonprod |
| `service.pipeline.impl.DeploymentTriggerProducerImpl` usa `producer.send` | Implementado | Publicar filtrado |
| `restclient.impl.BigQueueDeploymentTriggerProducerImpl` usa `producer.send` y mantiene callers productivos | Implementado | Publicar filtrado también; no asumir un solo producer |
| `DeploymentResultProducerImpl` usa `producer.send` | Implementado | Publicar filtrado |
| `DeploymentTimeoutJob` consulta deployments globales por estado/timeout | Implementado | Deshabilitar procesamiento en alpha; no certificar retry |
| mqclient 3.4.9 expone `Producer.send(Object, Filters)` | Contrato | Reutilizar sin cambiar payload/SDK |

## Gates externos

Antes del rollout, Fury/BigQueue debe confirmar:

- El accessor soportado para leer scope Java/Kotlin y la precedencia entre `scope`/`SCOPE` si ambos existen.
- Filtrado server-side por `scope:alpha`.
- Preservación de `filters.modified_fields` en el push HTTP.
- Comportamiento de mensajes sin filtro frente a bindings filtrados.

La existencia de `FuryUtils.getEnv("SCOPE")` en el classpath no basta para elegirlo. La POC usa la API que Fury confirme y la encapsula en un único punto de startup.

## Contrato de naming y startup

Tokens runtime: `prod | stage | alpha | beta | gamma`. `production/staging` son etiquetas funcionales, no tokens materializados.

Un scope canónico:

- Está en lowercase.
- Tiene al menos `<lane>-<role>-<segment>`.
- Usa `nonsite` para `prod` y `nonprod` para las demás lanes.
- No infiere lane desde pipeline environment, profile ni segmento.

| Scope | Lane | Profile |
|---|---|---|
| `prod-api-nonsite` | `prod` | `production` |
| `stage-api-nonprod` | `stage` | `stage` |
| `alpha-api-nonprod` | `alpha` | `stage` |
| `alpha-consumer-nonprod` | `alpha` | `stage` |
| `beta-api-nonprod` | `beta` | `stage` |
| `gamma-api-nonprod` | `gamma` | `stage` |

Scope ausente, typo, uppercase o segmento incompatible impide arrancar el runtime canónico. No se convierte en `local` ni en publicación sin filtro. Local/tests inyectan la lane o usan los producers locales ya existentes.

## Defaults base seguros

`application.yml` define los defaults mínimos de stage para que un scope nonprod nuevo no cargue recursos productivos:

- Datasource equivalente a `playmkrstg`.
- `bigqueue.segment: nonprod`.
- Topics nonprod existentes sin crear nombres por lane.
- `alpha/beta/gamma` resuelven profile `stage`; `prod` resuelve `production`.

## Contrato BigQueue

Los payloads permanecen intactos. El filtro vive en el envelope mqclient:

```json
{
  "filters": {"modified_fields": ["scope:alpha"]},
  "msg": {"...": "payload actual"}
}
```

Los tres producers productivos incluidos reciben la `RuntimeLane` inmutable y llaman siempre:

```java
producer.send(message, new Filters(List.of("scope:" + runtimeLane.value())));
```

Puntos obligatorios:

1. `service.pipeline.impl.DeploymentTriggerProducerImpl.publish`.
2. `restclient.impl.BigQueueDeploymentTriggerProducerImpl.publish`.
3. `service.pipeline.impl.DeploymentResultProducerImpl.publish`.

No existe `producer.send(message)` como fallback en esos beans canónicos. Los producers locales/no-op quedan intactos.

## Cobertura de la POC

| Camino | Producer | Resultado esperado |
|---|---|---|
| Deploy/undeploy por servicio existente | `restclient...BigQueueDeploymentTriggerProducerImpl` | `scope:alpha` |
| Trigger inicial del pipeline nuevo | `service.pipeline...DeploymentTriggerProducerImpl` | `scope:alpha` |
| Batch N+1 lane-affine | `service.pipeline...DeploymentTriggerProducerImpl` | `scope:alpha` |
| Result publicado por Playmaker | `DeploymentResultProducerImpl` | `scope:alpha` |
| Timeout/retry | Fuera de alcance y deshabilitado en alpha | No se ejecuta |

## Timeout processing en alpha

Las lanes nonprod comparten DB y `DeploymentTimeoutJob` no filtra por lane. El diseño KISS no agrega `routingLane` a las tablas.

Se agrega un único switch operacional booleano, default `true` para no cambiar runtimes existentes, y `false` en los scopes alpha de la POC. Cuando está apagado:

- El scan programado no consulta ni procesa deployments.
- La resolución lazy desde history tampoco ejecuta timeout processing.
- No se certifica retry/restart.

El nombre exacto de la property se fija en implementación junto a `DeploymentTimeoutConfig`; no contiene la lane ni duplica el scope.

## Arquitectura objetivo

```text
Fury scope alpha-api-nonprod / alpha-consumer-nonprod
                          │
                          ▼ startup
                   RuntimeLane(alpha)
                          │
       ┌───────────────────┼───────────────────┐
       ▼                   ▼                   ▼
pipeline trigger       existing trigger       result producer
       └────────────── send(message, Filters([scope:alpha]))

controller / dispatch / consumers / payloads / DB: SIN CAMBIOS
timeout processing alpha: OFF
```

## Archivos afectados

| Acción | Superficie | Cambio |
|---|---|---|
| `modify` | `ScopeUtils` o configuración de startup | Lane estricta y profile seguro |
| `modify` | `application.yml` y profiles | Defaults stage/nonprod |
| `modify` | Los dos trigger producers | Publish siempre filtrado en runtime canónico |
| `modify` | Result producer | Publish siempre filtrado |
| `modify` | `DeploymentTimeoutConfig`/`DeploymentTimeoutJob` | Switch binario para deshabilitar scan y resolución lazy en alpha |
| `modify` | Tests asociados | Matriz de startup, producers, timeout off y payload |

### No tocar

- Controllers HTTP, deploy/group/batch services, dispatch, consumers y payload DTOs.
- `PipelineExecution`, `EnvironmentModel`, repositories, migrations, idempotencia e history schema.
- `rio-sdk-events`, nombres de topics, Actions, inactivation y Materializer.
- Persistencia de lane o solución durable de retries.

## Estrategia de tests

- Startup: matriz canónica lane/profile y fallo por missing, typo, uppercase o segmento incompatible.
- Config: alpha/beta/gamma usan stage/nonprod; prod usa production/nonsite; beta nunca activa recursos productivos.
- Producers: los tres puntos llaman exactamente `send(message, Filters(["scope:alpha"]))`.
- No-fallback: ningún producer canónico llama `send(message)` cuando falla la lane; el runtime no arranca antes.
- Timeout off: scan programado y resolución lazy no consultan repositories ni publican.
- Wire: trigger/result conservan serialización; scope sólo aparece en envelope.
- E2E: deploy/undeploy existente, trigger pipeline, batch N+1 y result llevan `scope:alpha`.
- Plataforma: consumer alpha recibe; beta no recibe; envelope conserva filtro.
- Calidad: tests críticos primero, checks del repo y ≥95% de cobertura nueva.

## Observabilidad

- `routing_outcome:published|startup_invalid` sin lane como tag.
- Métrica/health estándar para timeout processing disabled.
- No imprimir mapa de ambiente, payload, scope completo ni IDs como tags dinámicos.

## Rollout y rollback

1. Confirmar gates Fury/BigQueue.
2. Desplegar primero profile/defaults seguros.
3. Desplegar los tres producers filtrados y timeout processing off sólo en alpha.
4. Validar ambos trigger producers, result y batch N+1.
5. Habilitar el consumer Flink alpha y ejecutar la vuelta lane-affine.

Rollback:

1. Cerrar route/entrada alpha.
2. Drenar mensajes `scope:alpha` con consumers canónicos activos.
3. Confirmar backlog cero.
4. Revertir producers, consumers y artefactos.

## Design Decisions

- **DD-1 — Autoridad runtime:** la lane sale sólo del scope Fury local y se resuelve al startup.
- **DD-2 — Sin fallback:** scope inválido impide startup; nunca publica sin filtro.
- **DD-3 — Cobertura real:** se filtran los dos trigger producers activos y el result producer.
- **DD-4 — Retry fuera:** timeout processing se apaga en alpha; no se agrega persistencia.
- **DD-5 — SDK intacto:** filtros mqclient existentes, payloads sin cambios.

## Definition of Done

- `alpha-api-nonprod` y `alpha-consumer-nonprod` producen `RuntimeLane(alpha)`.
- Un scope inválido no arranca ni publica sin filtro.
- Ambos deployment trigger producers y el result producer emiten exactamente `scope:alpha`.
- Timeout processing está deshabilitado en alpha y no forma parte de la evidencia.
- Payloads, SDK, controllers, dominio, DB y pipeline environment permanecen intactos.
- Fury demuestra filtrado server-side y envelope preservado.
- E2E lane-affine y rollback generan evidencia enlazable.

## Fuera de alcance

- Timeout/retry/restart con ownership por lane.
- Carrier HTTP/in-memory/durable.
- Legacy dentro del artefacto canónico.
- Campos de scope en payloads o entidades.
- Actions, runtime status, Observability, Materializer y KMS.
- Release productivo desde feature branch.

## Stop conditions

- Accessor Fury no confirmado.
- BigQueue no filtra server-side o no preserva filtros.
- Alguno de los dos trigger producers usados sigue publicando sin filtro.
- Scope inválido cae en local/legacy.
- Timeout processing continúa activo en alpha.
- E2E produce un mensaje sin filtro o con lane distinta.

## Fuentes

- Review independiente del 2026-09-22 sobre `origin/develop@625f491d218e`.
- [[scope-naming-standard]] y [[Estandarización de Scopes RIO]].
- mqclient 3.4.9 y contratos existentes de `rio-sdk-events`.
