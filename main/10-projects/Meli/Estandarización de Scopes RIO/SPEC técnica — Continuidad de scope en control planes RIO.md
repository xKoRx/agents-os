---
type: doc
schema_version: 1
status: active
area: "[[Meli]]"
related:
  - "[[Estandarización de Scopes RIO]]"
  - "[[SPEC técnica — Routing KISS por scope en rio-playmaker]]"
  - "[[POC KISS — Routing de scopes en Playmaker]]"
  - "[[scope-naming-standard]]"
  - "[[rio-sdk-events]]"
  - "[[rio-controlplane-flink]]"
aliases:
  - SPEC CPs scopes RIO
  - continuidad de filtros scope en CPs
tags:
  - kind/doc
  - area/meli
  - project/scopes-rio
  - tech/control-plane
created: "2026-09-21"
updated: "2026-09-22"
---

# Technical Specification — Continuidad de scope en control planes RIO

**Feature**: `rio-controlplane-scope-filter-continuity`
**Owner**: Rodrigo Jara
**Piloto**: `rio-controlplane-flink`, sólo deployment trigger/result lane-affine
**Status**: DRAFT revisado con criterio KISS/YAGNI
**Deriva de**: [SIG-599](https://spellbook.adminml.com/projects/SIG/specs/SIG-599), [[SPEC técnica — Routing KISS por scope en rio-playmaker]] y [[scope-naming-standard]]
**Baseline revisada**: `rio-controlplane-flink origin/develop@eafad6ac57ca`; `rio-playmaker origin/develop@625f491d218e`; `rio-sdk-events origin/master@ad2c98b806cf`; corte 2026-09-22

## Propósito

Demostrar el contrato mínimo `scope:x` entrada → `scope:x` salida en una instancia canónica de Flink, sin agregar carrier, persistencia, configuración por lane, cambios de payload ni librería compartida.

Una instancia `alpha-consumer-nonprod` resuelve `lane=alpha` una vez al arrancar. Después acepta sólo triggers con exactamente `scope:alpha` y todos los deployment results incluidos en la POC salen con exactamente `scope:alpha`.

La POC no declara resueltos retries, restart, GCP KVS/PubSub, schedulers ni reconciliadores. El patrón runtime-derived sólo es correcto cuando el trabajo no puede ser reclamado por otra lane.

## Contenido

## Decisión KISS

La implementación tiene cuatro piezas y ninguna fuente de verdad duplicada:

1. Fury entrega el nombre del scope al proceso.
2. El proceso resuelve una `RuntimeLane` inmutable al startup.
3. El controller compara el único filtro `scope:` entrante con esa lane.
4. El publisher agrega esa misma lane mediante `sendWithFilters`.

No se implementa:

- Modo legacy dentro del artefacto canónico.
- `expectedScope` manual.
- `RoutingContext` o propagación controller→processor→publisher.
- Campo de scope en DTOs o entidades.
- Persistencia de lane para paths que la POC no cubre.
- Framework común para todos los control planes.
- Release nueva de `rio-sdk-events` o `rio-core-java`.

Las instancias legacy conservan el artefacto anterior durante la POC. No se agrega compatibilidad especulativa al código nuevo.

## Alcance exacto

### Incluido

- Runtime Fury `alpha-consumer-nonprod` de `rio-controlplane-flink`.
- `rio-deployment-trigger` como ingreso.
- Guard antes de mapper, idempotencia, `CompletableFuture` y cualquier side effect.
- Deployment results publicados por el flujo lane-affine elegido para el golden deploy.
- Happy path alpha, mismatch beta, missing, malformed y rollback.
- Evidencia real de filtrado BigQueue y preservación del envelope.

### Excluido

- GCP deployments que persisten `GcpDeploymentRecord` y finalizan desde KVS, Pub/Sub o `GcpJobTimeoutJob`.
- Retry por timeout de Playmaker.
- Restart/recovery, schedulers y reconciliadores con storage compartido.
- Actions y runtime status.
- Kafka, ClickHouse, Fury, Signals, Observability y KMS.
- Legacy y migración masiva de scopes existentes.

En la infraestructura alpha, `kvs.gcp-pending-deployments.container-name` y `rio.gcp.pubsub.subscription` deben permanecer vacíos para que los componentes GCP condicionales no se creen. El golden deploy no usa GCP. Si otro scheduler o store durable participa en el camino elegido, la POC se detiene y ese camino queda fuera.

## Baseline verificada

| Hecho | Evidencia | Consecuencia |
|---|---|---|
| El controller recibe `BigQueueMessage<DeploymentTriggerMessage>` pero usa sólo `msg()` | `DeploymentTriggerController` | El guard cabe en la frontera sin cambiar dominio |
| `BigQueueMessage` contiene `BigQueueFilters` y `modifiedFields` puede ser nulo | `rio-sdk-events` | El parser debe manejar ausencia y malformed |
| `BigQueueClient.sendWithFilters` delega a `Producer.send(message, Filters)` | `rio-sdk-events` y mqclient 3.4.9 | No se modifica el payload |
| `BigQueueDeploymentPublisher` centraliza deployment results | Flink | Un cambio de egreso cubre el canal de la POC |
| GCP guarda trabajo y publica desde Pub/Sub/jobs posteriores | `GcpDeploymentRecord`, registry, processors y job | GCP no puede certificarse con runtime-only |
| Playmaker tiene dos producers activos de deployment trigger | producer legacy y producer pipeline | Ambos son prerrequisito de Fase 2 |
| mqclient construye `msg + filters` | mqclient 3.4.9 | No prueba filtrado server-side ni preservación del push |

## Gates externos obligatorios

Antes de implementar o desplegar el piloto, Fury/BigQueue debe demostrar:

- Cuál es el accessor soportado para obtener el scope en Java/Kotlin.
- Si el runtime lo expone como `scope`, `SCOPE` o ambos y cuál es la precedencia.
- Que un binding `scope:alpha` filtra server-side.
- Que el push HTTP conserva `filters.modified_fields=["scope:alpha"]`.
- Qué ocurre con mensajes sin filtro frente a un binding filtrado.

Flink debe identificar además el componente exacto del golden deploy y trazarlo hasta el result. El gate sólo cierra si ese camino no cruza KVS, Pub/Sub, scheduler, recovery ni un store que otra lane pueda reclamar. `No GCP` por sí solo no constituye evidencia de lane-affinity.

La presencia de `FuryUtils.getEnv("SCOPE")` en el classpath no lo convierte en la API elegida. `FuryUtils` agrega requisitos y fallos innecesarios para un valor plano; no se usa sin confirmación de Fury.

## Contrato de naming y startup

Los tokens runtime son `prod | stage | alpha | beta | gamma`. `production` y `staging` pueden existir como etiquetas funcionales, pero no son tokens del nombre materializado.

El scope canónico cumple:

- Todo lowercase; no se normalizan mayúsculas silenciosamente.
- Al menos tres tokens no vacíos.
- Primer token dentro del vocabulario de lanes.
- Último token `nonsite` para `prod` y `nonprod` para las demás lanes.
- Los tokens intermedios representan role/qualifiers y no se hardcodean en el resolver.

Ejemplos:

| Scope Fury | Resultado |
|---|---|
| `alpha-consumer-nonprod` | `RuntimeLane(alpha)` |
| `beta-consumer-flink-nonprod` | `RuntimeLane(beta)` |
| `prod-consumer-nonsite` | `RuntimeLane(prod)` |
| `alpah-consumer-nonprod` | startup failure |
| `Alpha-consumer-nonprod` | startup failure |
| `alpha-consumer-nonsite` | startup failure |
| scope ausente o error del accessor | startup failure |

La lane se resuelve una vez y queda como value object inmutable de aplicación. No se consulta el ambiente en cada mensaje ni se degrada a `local` o publish sin filtro. Los tests/local usan una `RuntimeLane` provista por su configuración de test; esa comodidad no existe en un runtime Fury desplegado.

## Contrato de ingreso

El parser inspecciona `filters.modified_fields`, ignora tags con otros prefijos y exige exactamente un tag `scope:` lowercase cuyo valor pertenezca al vocabulario.

| Runtime lane | Envelope | Resultado HTTP | Side effects |
|---|---|---|---|
| `alpha` | exactamente `scope:alpha` | flujo normal | sí |
| `alpha` | `scope:beta` | `2xx` | ninguno |
| `alpha` | sin `scope:` | `2xx` | ninguno |
| `alpha` | duplicado, vacío, uppercase, wildcard o unknown | `2xx` | ninguno |

El guard se ejecuta antes del mapper, idempotencia, dispatch async, KVS y llamadas de infraestructura. El `2xx` evita retry infinito para errores determinísticos; cada descarte emite una métrica bounded y requiere procedimiento de replay controlado. Errores transitorios posteriores mantienen la semántica actual del CP.

## Contrato de salida

`BigQueueDeploymentPublisher` recibe la `RuntimeLane` inmutable de la aplicación y publica siempre mediante:

```java
client.sendWithFilters(payload, List.of("scope:" + runtimeLane.value()));
```

No existe fallback a `client.send(payload)` dentro del runtime canónico. El publisher no recibe el scope desde el controller, payload o command. El mensaje de negocio no cambia.

Esta regla cubre solamente resultados cuyo ownership permanece en la instancia/lane que procesó el trigger. No autoriza publicar trabajo recuperado desde un store global.

## Arquitectura objetivo

```text
Fury scope: alpha-consumer-nonprod
                 │
                 ▼ startup
          RuntimeLane(alpha)
                 │
        ┌─────────┴─────────┐
        ▼                   ▼
DeploymentTriggerController   BigQueueDeploymentPublisher
        │                   │
        ├─ exige scope:alpha └─ siempre scope:alpha
        └─ luego ejecuta dominio

payload / processor / DB / SDK: SIN CAMBIOS
```

## Implementación mínima Flink

1. Escribir tests de startup, guard y publisher antes del código.
2. Resolver una `RuntimeLane` inmutable durante startup usando el accessor aprobado en G0.
3. Agregar un parser/guard pequeño para `BigQueueFilters`.
4. Invocar el guard al inicio de `DeploymentTriggerController`.
5. Inyectar `RuntimeLane` en `BigQueueDeploymentPublisher` y reemplazar `send` por `sendWithFilters` para deployment results.
6. No tocar processor, commands, events internos, records GCP, KVS ni SDK.

El nombre exacto de la clase que lee Fury se decide al cerrar G0. No se crean provider + classifier + resolver + context cuando un bean de startup y un guard alcanzan.

## Archivos conceptuales

| Acción | Superficie | Cambio |
|---|---|---|
| `new` | `routing/RuntimeLane` | Value object inmutable y validación del nombre canónico |
| `new` | `routing/ScopeFilterGuard` | Parsear el único `scope:` y compararlo con `RuntimeLane` |
| `modify` | configuración de startup | Leer Fury una vez y crear `RuntimeLane`; fallar cerrado |
| `modify` | `DeploymentTriggerController` | Guard antes de cualquier side effect |
| `modify` | `BigQueueDeploymentPublisher` | `sendWithFilters(..., [scope:<lane>])` |
| `modify` | tests asociados | Matriz contractual |

### No tocar

- `DeploymentTriggerMessage`, `DeploymentResultMessage` y `rio-sdk-events`.
- `DeploymentProcessor`, `EventFlinkApp`, commands, events internos y modelos de dominio.
- `GcpDeploymentRecord`, registry, Pub/Sub, jobs y KVS durante esta POC.
- Pipeline environment, DB, idempotencia, history, schema versions y segment IDs.
- Actions, runtime status y topics por lane.

## Matriz de tests

| Caso | Assert principal |
|---|---|
| Scope alpha canónico | Startup produce `RuntimeLane(alpha)` |
| Scope typo/uppercase/segmento incorrecto | Startup falla |
| Scope/accessor ausente o con error | Startup falla; nunca modo legacy |
| Trigger alpha | Mapper y processor se invocan |
| Trigger beta/missing/malformed/duplicado | `2xx`; cero mapper, idempotencia, async, KVS y publish |
| Otros tags + `scope:alpha` | Procesa; otros tags no alteran la lane |
| Result alpha | Llama exactamente `sendWithFilters(payload, ["scope:alpha"])` |
| Payload | Serialización equivalente; scope sólo en envelope |
| BigQueue real | Sólo consumer alpha recibe y ve el filtro intacto |
| GCP deshabilitado | Beans condicionales no existen con container/subscription vacíos |
| Rollback | Backlog filtrado drenado antes de volver al artefacto legacy |

## Observabilidad

Métricas nuevas, sin lane como tag:

- `routing_outcome:accepted|missing|malformed|mismatch`
- Contador de startup failure usando la señal operativa estándar de la aplicación, sin imprimir variables de entorno.

Cualquier `mismatch` o startup failure bloquea la certificación. No se loguea el envelope completo, payload, mapa de ambiente ni IDs como tags dinámicos.

## Rollout y rollback

1. Confirmar accessor Fury y semántica BigQueue con una prueba real.
2. Trazar y aprobar el componente Flink lane-affine del golden deploy.
3. Corregir Fase 2 para que ambos producers activos de Playmaker publiquen filtro; retry por timeout queda fuera.
4. Crear `alpha-consumer-nonprod` con GCP KVS/PubSub vacíos y sin tráfico de usuario.
5. Desplegar el artefacto Flink estricto sólo en alpha.
6. Probar alpha, mismatch, missing, malformed y payload intacto.
7. Ejecutar el golden deploy lane-affine y capturar trigger/result.

Rollback:

1. Cerrar la route/entrada alpha y detener nuevos dispatches.
2. Mantener el consumer alpha hasta drenar mensajes `scope:alpha`.
3. Confirmar backlog cero.
4. Recién entonces revertir artefacto y binding.

No se revierte primero el consumer a legacy mientras existan mensajes filtrados.

## Aplicabilidad posterior

Esta SPEC no promete un diff universal. Define un criterio de elegibilidad:

| Tipo de path | ¿Puede usar runtime-derived sin estado? | Siguiente paso |
|---|---|---|
| Request/in-process lane-affine | Sí | Repetir provider, guard y publisher local |
| Store/queue/lease aislado físicamente por lane | Sí | Probar aislamiento y restart |
| Store/scheduler/reconciler compartido | No | Diseñar ownership durable por lane en otra fase |
| Sin envelope de filtros | No directamente | Adaptar ingreso sólo si ese CP entra al alcance |
| Sin BigQueue equivalente | No aplica | No forzar el patrón |

Kafka pierde hoy el envelope, Observability usa uno propio, Fury reconcilia trabajo durable y KMS no tiene este flujo. Ninguno se modifica por anticipado.

## Design Decisions

### DD-1: Runtime lane estricta al startup

El scope Fury local es la única autoridad. Ausencia, typo, uppercase, segmento incompatible o error del accessor impiden arrancar el runtime canónico.

### DD-2: Sin compatibilidad legacy en el artefacto POC

Las instancias legacy permanecen en su versión anterior. Esto elimina el fallback fail-open y evita un flag/config temporal.

### DD-3: Sin carrier ni persistencia

La lane inmutable de aplicación alcanza para el path lane-affine. Los paths durables quedan fuera en vez de recibir una solución parcial.

### DD-4: BigQueue/Fury es gate, no supuesto

La POC no avanza a tráfico hasta demostrar filtro server-side y envelope preservado.

### DD-5: Generalizar sólo después de un segundo caso

No se cambia `rio-sdk-events`, `rio-core-java` ni Fury Toolkit desde este piloto. La extracción se evalúa con dos implementaciones reales.

## Definition of Done

- `alpha-consumer-nonprod` arranca con `RuntimeLane(alpha)` y un scope inválido no arranca.
- Trigger `scope:alpha` produce un deployment result `scope:alpha`.
- Beta, missing, malformed y duplicado producen `2xx` sin side effects.
- No existe publish sin filtro en el publisher incluido.
- Payloads, SDK, processor, DB y pipeline environment permanecen intactos.
- GCP KVS/PubSub, retry y reconciliadores no participan en el golden deploy.
- Fury demuestra filtering server-side y preservación del envelope.
- Rollback drena mensajes filtrados antes de retirar el consumer.

## Stop conditions

- Fury no confirma el accessor.
- BigQueue no filtra server-side o no preserva el envelope.
- No existe un componente Flink cuyo recorrido trigger→result sea demostrablemente lane-affine.
- Algún producer Playmaker usado por el golden flow continúa publicando sin filtro.
- Flink degrada un scope inválido a local/legacy.
- El camino elegido entra en GCP, KVS, Pub/Sub, scheduler o recovery durable.
- Aparece un solo mismatch o result con lane distinta.

## Fuentes

- Review independiente adjunto el 2026-09-22, contrastado con las refs de baseline.
- [[SPEC técnica — Routing KISS por scope en rio-playmaker]] y [[POC KISS — Routing de scopes en Playmaker]].
- [[scope-naming-standard]] para el naming materializado.
- `rio-sdk-events`: `BigQueueMessage`, `BigQueueFilters` y `BigQueueClient.sendWithFilters`.
- `rio-controlplane-flink`: controller, publisher y flujos GCP durables.
