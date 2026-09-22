---
type: doc
schema_version: 1
status: active
area: "[[Meli]]"
related:
  - "[[Estandarización de Scopes RIO]]"
  - "[[SPEC técnica — Routing KISS por scope en rio-playmaker]]"
  - "[[POC KISS — Routing de scopes en Playmaker]]"
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
updated: "2026-09-21"
---

# Technical Specification — Continuidad de scope en control planes RIO

**Feature**: `rio-controlplane-scope-filter-continuity`
**Owner**: Rodrigo Jara
**Project**: Signals (`rio-controlplane-flink` como piloto; contrato reusable por los control planes RIO)
**Status**: DRAFT
**Deriva de**: [SIG-599](https://spellbook.adminml.com/projects/SIG/specs/SIG-599) y [[Estandarización de Scopes RIO]]
**Baseline revisada**: `rio-sdk-events origin/master@ad2c98b806cf`; `rio-controlplane-flink origin/develop@c88038ea1359`; `rio-controlplane-kafka origin/develop@1595df01304a`; `rio-controlplane-clickhouse origin/develop@cc64f78b18a7`; `rio-controlplane-fury origin/develop@4c40042c102f`; `rio-controlplane-observability origin/develop@2cc4eaf3e265`; `rio-controlplane-signals origin/develop@a0ae1324466b`; corte 2026-09-21

## Propósito

Preservar la lane de infraestructura Fury durante el round-trip de eventos RIO: un control plane que recibe un trigger con `filters.modified_fields=["scope:alpha"]` procesa ese trigger y publica sus resultados con el mismo tag `scope:alpha`. El scope de salida se obtiene exclusivamente del envelope recibido; nunca del `SCOPE` del proceso, del pipeline environment, del segmento BigQueue ni del tipo de componente.

La POC implementa el contrato en `rio-controlplane-flink` para `rio-deployment-trigger` → `rio-deployment-result`. El diseño es payload-agnostic para extenderlo después a deployment y actions en los demás CPs sin cambiar los DTOs de negocio.

## Contenido

### Ubicación en el programa

Esta es la Fase 3 del programa alpha end-to-end: Fase 1 selecciona el backend desde el frontend, Fase 2 convierte `X-Rio-Scope` en filtro del trigger en Playmaker y Fase 3 conserva ese filtro dentro del control plane y lo devuelve en el result. No debe confundirse con la fase interna de certificación E2E del planner de Playmaker.

La unidad implementable de esta fase es Flink. La adopción en todos los CPs ocurre después de que el piloto demuestre el contrato y no forma parte del golden deploy inicial.

### Invariantes

- `Pipeline Environment ≠ Fury Scope`: `environmentId`/`environmentName` conservan su semántica funcional y no participan en este routing.
- `scope:x` es metadata de transporte en el envelope BigQueue; no se agrega a `DeploymentTriggerMessage`, `DeploymentResultMessage`, `ActionTriggerMessage` ni `ActionResultMessage`.
- El CP devuelve el mismo scope válido que recibió. No normaliza, reemplaza ni deriva el valor desde su runtime.
- El segmento BigQueue, `componentType`, auth scopes y tracing scopes son ejes independientes.
- El payload se publica directamente; nunca se envuelve manualmente en `BigQueueMessage`, porque BigQueue crea el envelope.
- `ThreadLocal`, MDC, request-scoped beans y estado global no son carriers válidos para cruzar ejecución asíncrona.

### Puntos en común verificados

| Punto común | Implementación vigente | Uso en la solución |
|---|---|---|
| Envelope tipado | `rio-sdk-events` expone `BigQueueMessage<T>` y `BigQueueFilters.modifiedFields`; Flink, Kafka, ClickHouse, Fury y Signals ya consumen contratos del SDK | Leer el filtro sin modificar el payload |
| Publicación filtrada | `BigQueueClient.sendWithFilters(Object, List<String>)` del SDK termina en `Producer.send(message, Filters)` | Publicar el result con el tag validado |
| Punto de egreso central | Los CPs concentran resultados en publishers de deployment/actions | Aplicar el filtro una vez, en el boundary de transporte |
| Punto de ingreso central | Los CPs exponen controllers de trigger que reciben el envelope | Parsear y validar antes de ejecutar dominio |
| Carrier interno | Cada CP ya transporta un command/event interno (`EventFlinkApp`, `DeploymentRequestedEvent`, processors u orchestrators) | Adjuntar un contexto de routing separado del dominio |
| Tags arbitrarios | `vis-items-loader-tagging` publica y consume tags como `process:*` y `vertical:*` mediante `modified_fields` | Confirma que `scope:*` encaja en el mecanismo de filtros existente |

`rio-sdk-events` ya contiene las primitivas de transporte necesarias; la POC no requiere publicar una nueva versión. Lo que falta es la semántica común para extraer exactamente un tag `scope:`, transportarlo y seleccionar el overload filtrado al publicar.

### Diferencias relevantes entre control planes

| Control plane | Trigger actual | Result actual | Implicancia |
|---|---|---|---|
| Flink | `BigQueueMessage<DeploymentTriggerMessage>` y `BigQueueMessage<ActionTriggerMessage>` | SDK `BigQueueClient.send(payload)` | Mejor piloto: ya usa envelope y cliente con `sendWithFilters`; debe conservar el contexto a través de `EventFlinkApp` |
| Kafka | Deployment se parsea desde `JsonNode`; actions usa envelope tipado | Publishers centralizados con SDK client | El parser debe conservar `filters` además de `msg` y routing keys existentes |
| ClickHouse | Envelope tipado | Cliente local ya implementa `sendWithFilters` | La capacidad de egreso existe; falta carrier junto a `DeploymentRequestedEvent` |
| Fury | Envelope tipado deserializado con `TypeReference` | `Producer.send(payload)`; algunos resultados salen desde reconciliadores posteriores | El path sincrónico puede usar memoria; el path reconciliado requiere persistencia operacional explícita y queda fuera de la POC |
| Signals | Envelope tipado para deployment/actions | Clientes locales y `Producer.send(payload)` | Requiere agregar overload filtrado y un wrapper de aplicación para no contaminar el evento de dominio |
| Observability | DTO local `BigQueueMessage(id,msg)` | No publica result | Participa en binding/aislamiento, pero no en echo de filtros; migrar al envelope SDK sólo si necesita validación in-app |
| KMS | No se observó consumer BigQueue | No aplica | Fuera de esta fase |

### Arquitectura objetivo

```text
rio-deployment-trigger
filters.modified_fields=["scope:alpha"]
        │
        ▼
DeploymentTriggerController [MODIFIED]
        │ parsea envelope y produce RoutingContext(scope:alpha)
        │ valida expectedScope=alpha sin usar runtime SCOPE como fuente
        ▼
ScopedDeploymentCommand [NEW, interno]
        │ payload y routing context viajan separados
        ▼
handlers / jobs del CP [UNCHANGED en dominio]
        │
        ▼
DeploymentResultPublisher [MODIFIED]
        │ sendWithFilters(result, ["scope:alpha"])
        ▼
rio-deployment-result
filters.modified_fields=["scope:alpha"]
```

### Contrato del filtro

La única forma canónica es `scope:<value>`, donde `<value>` cumple `^[a-z0-9][a-z0-9-]{0,62}$`. Playmaker entrega el valor normalizado; el CP valida y preserva, pero no normaliza una segunda vez.

| Envelope de entrada | Resultado del parser | Comportamiento |
|---|---|---|
| `filters` ausente, `modified_fields` ausente o lista vacía | `Legacy` | Procesar y publicar con `send(payload)` durante la migración |
| Exactamente un `scope:alpha` válido | `Scoped(RoutingScope("alpha"))` | Procesar y publicar con `sendWithFilters(payload, ["scope:alpha"])` |
| Más de un tag `scope:` aunque sean iguales | `Malformed(multiple_scope_tags)` | ACK `200`, no ejecutar handler y emitir reason bounded |
| `scope:` vacío, uppercase, caracteres no permitidos o largo excesivo | `Malformed(invalid_scope_tag)` | ACK `200`, no ejecutar handler y emitir reason bounded |
| Tags ajenos sin tag `scope:` | `Legacy` | No copiarlos al result; el contrato de esta fase sólo propaga routing scope |

El result copia sólo el tag `scope:` validado. No hace echo ciego de todos los filtros del envelope, porque eso propagaría metadata no autorizada y acoplaría el result a tags futuros.

### Guard de lane

El consumer alpha declara un `expectedScope=alpha` explícito en su configuración de despliegue. Si recibe otro scope válido, responde `200` sin ejecutar el handler y registra `scope_mismatch`. Este guard detecta una configuración errónea, pero no reemplaza el filtro server-side de BigQueue.

`expectedScope` no se infiere desde el nombre completo de `SCOPE`, `SCOPE_SUFFIX`, el profile Spring ni el segmento. La materialización Fury puede agregar rol y segmento, por lo que esas heurísticas no son una autoridad estable.

### Carrier interno

El boundary de entrada crea un value object inmutable `RoutingScope` y un `RoutingContext` opcional. El payload de dominio y el contexto de routing viajan juntos en un command/event interno, pero permanecen como campos distintos.

```java
public record RoutingScope(String value) {
  public String filterTag() {
    return "scope:" + value;
  }
}

public record RoutingContext(RoutingScope scope) {
  public List<String> filters() {
    return scope == null ? List.of() : List.of(scope.filterTag());
  }
}
```

La forma exacta puede adaptarse al estilo del repo, pero deben mantenerse tres propiedades: parsing único en ingreso, transporte explícito por la cadena asíncrona y selección del filtro sólo en egreso.

### Implementación del piloto Flink

1. `DeploymentTriggerController` extrae y valida `message.filters()` antes de leer/ejecutar el payload. Los errores de mapping que publican `FAILED` reciben también el mismo `RoutingContext`.
2. `DeploymentProcessor.process` recibe el contexto como argumento separado y lo copia al evento interno creado para el channel `BIGQUEUE`.
3. `EventFlinkApp` conserva el `RoutingContext` durante la cadena in-memory. Los paths `STREAM` y legacy lo dejan ausente.
4. `BigQueueDeploymentPublisher` centraliza la elección: contexto presente usa `client.sendWithFilters(payload, context.filters())`; contexto ausente usa `client.send(payload)`.
5. Todos los estados emitidos por el mismo deployment en el golden path (`STARTED`, `IN_PROGRESS`, `COMPLETED` o `FAILED`) usan el mismo contexto.
6. Actions, runtime status, streams y controllers que no participan del deployment POC permanecen sin cambios.

El scope no se agrega a `FlinkApp`, a la idempotency key ni a datos de infraestructura AWS. Para la POC, el golden deployment debe completar sin restart y antes de cualquier reconstrucción que pierda el evento in-memory.

### Límite durable

La continuidad in-memory demuestra el contrato de transporte, pero no garantiza resultados emitidos después de un restart o por un reconciliador que reconstruye su trabajo desde KVS/DB. Los CPs con ejecución durable deben persistir `routingScope` como metadata operacional del trabajo, separada de pipeline environment y de la identidad del recurso, antes de adoptar el contrato en esos paths.

Fury es el caso que obliga esta decisión: sus reconciliadores pueden publicar `COMPLETED`/`FAILED` después de la request original. No se debe desplegar continuidad de scope en ese path hasta definir lectura/escritura/cleanup de esa metadata y probar restart. La POC Flink no resuelve ese diseño por anticipado.

### Reuso y estandarización

El piloto mantiene `RoutingScope`/parser dentro de Flink para no acoplar G3 a una release nueva del SDK. Después de certificar el contrato, la segunda adopción extrae esas piezas a `rio-sdk-events` como helper de transporte sin tocar los records de trigger/result. Los CPs actualizan a esa versión y conservan sólo sus adapters/carriers internos.

La abstracción compartida debe contener validación y conversión `BigQueueFilters ↔ RoutingScope`; no debe conocer Spring, controllers, topics, `Environment`, perfiles Fury ni persistencia de ningún CP.

### Design Decisions

#### DD-1: El envelope es la autoridad del scope durante el round-trip

**Decisión**: extraer `RoutingScope` desde `BigQueueMessage.filters` y usar el mismo value object para publicar el result.

**Fundamentación**: garantiza `x → x` por construcción y evita derivar `z` desde el runtime del proceso. La alternativa de leer `SCOPE` no demuestra continuidad del mensaje y falla cuando el nombre materializado incluye rol o segmento.

#### DD-2: El payload de negocio permanece intacto

**Decisión**: transportar scope fuera de los DTOs `Deployment*`/`Action*`.

**Fundamentación**: el scope selecciona infraestructura, no describe el deployment. Agregarlo al payload obligaría una migración de schema y permitiría que consumers de dominio lo confundieran con environment.

#### DD-3: Broker filter más guard local fail-closed

**Decisión**: BigQueue filtra por `scope:alpha` server-side y el CP compara contra `expectedScope=alpha` antes de procesar.

**Fundamentación**: el broker entrega aislamiento primario y el guard vuelve observable una mala configuración. Filtrar sólo dentro de la aplicación permitiría side effects si el check se omite en un path; confiar sólo en config externa ocultaría un binding cruzado.

#### DD-4: Compatibilidad por ausencia

**Decisión**: un envelope sin `scope:` conserva el comportamiento legacy durante el rollout; un envelope con scope malformed o distinto al esperado se ACKea sin side effects.

**Fundamentación**: permite desplegar consumers/publishers antes de activar el productor filtrado y evita loops de poison messages. Un fallback desde malformed a legacy rompería el aislamiento silenciosamente.

#### DD-5: Promoción al SDK después del piloto

**Decisión**: validar el helper en Flink y moverlo a `rio-sdk-events` al comenzar la segunda adopción.

**Fundamentación**: el contrato común merece una sola implementación cuando más de un CP la consume, pero una release compartida no debe bloquear la POC que determina si Fury filtra y entrega el envelope como se espera.

### Archivos del piloto

#### Archivos nuevos

| Archivo sugerido | Propósito |
|---|---|
| `deployment/routing/RoutingScope.java` | Value object validado y tag canónico |
| `deployment/routing/RoutingScopeFilterParser.java` | Clasificar legacy/scoped/malformed desde `BigQueueFilters` |
| Tests unitarios del parser | Fijar el contrato reusable |

#### Archivos modificados

| Archivo / símbolo | Cambio |
|---|---|
| `controller/DeploymentTriggerController` | Parsear filtros, aplicar guard de lane y entregar contexto al processor/publisher de error |
| `deployment/DeploymentProcessor` | Transportar `RoutingContext` sin mezclarlo con operation, channel o idempotencia |
| Command/factory que crea `EventFlinkApp` | Copiar el contexto al evento interno |
| `handler/EventFlinkApp` | Mantener el contexto durante el golden path in-memory |
| `deployment/BigQueueDeploymentPublisher` | Usar `sendWithFilters` cuando existe scope y `send` para legacy |
| Config del consumer alpha | Declarar `expectedScope=alpha`; el binding broker vive en Fury |
| Tests de controller, processor y publisher | Cubrir exactitud, no-side-effects, legacy y estados de result |

#### No tocar

- DTOs de `rio-sdk-events`, schema version ni forma del payload.
- Pipeline environment, `environmentId`, `environmentName`, component type, idempotencia o claves de recursos.
- Actions, runtime-status, Streams, topics nuevos y producción.
- Estado durable de Flink, KVS o DB en esta POC.

### Estrategia de tests

- Parser: ausente/vacío → legacy; `scope:alpha` → scoped; duplicado, uppercase, vacío, largo y caracteres inválidos → malformed.
- Guard: `expectedScope=alpha` acepta alpha y rechaza beta sin llamar mapper, processor ni infraestructura.
- Propagación: el mismo objeto/valor cruza controller → processor → event → publisher; ningún paso consulta runtime `SCOPE`.
- Publisher: scoped llama exactamente `sendWithFilters(payload, List.of("scope:alpha"))`; legacy llama exactamente `send(payload)`; nunca doble-wrap.
- Lifecycle: `STARTED`, `IN_PROGRESS`, `COMPLETED` y `FAILED` conservan alpha en los paths cubiertos por el golden deployment.
- Wire contract: `msg` es byte-compatible con el payload actual y el único delta del envelope es `filters.modified_fields`.
- E2E: un consumer alpha recibe trigger alpha y no beta; el result alpha llega al consumer alpha de Playmaker; un mensaje malformed no produce side effects.
- Calidad: tests críticos primero y al menos 95% de cobertura sobre código nuevo.

### Observabilidad

Métricas bounded: `routing_mode=legacy|scoped`, `routing_rejection=malformed|scope_mismatch` y publish success/error existentes. El valor dinámico del scope no se usa como tag de métrica. Logs permiten el scope validado en mensajes de diagnóstico puntuales, pero no imprimen el envelope, headers, params ni valores malformed crudos.

### Rollout y rollback

1. Fury demuestra que el consumer filter `scope:alpha` se aplica server-side y que `filters.modified_fields` llega intacto al push HTTP.
2. Se crea el binding alpha de `rio-deployment-trigger` y el binding alpha de `rio-deployment-result` sin tráfico.
3. Flink alpha se despliega con parser, carrier, guard y publisher compatible con legacy.
4. Playmaker comienza a publicar triggers alpha filtrados.
5. Se ejecutan smoke legacy, golden alpha, negativo beta/malformed y un ciclo de rollback.

Rollback: Playmaker deja de emitir el filtro y el CP vuelve al path legacy por ausencia; los bindings alpha pueden quedar sin tráfico o deshabilitarse. No hay schema, backfill ni datos de dominio que revertir.

### Adopción posterior

Orden recomendado: Kafka → Signals → ClickHouse → Fury. Kafka valida el parser que hoy usa `JsonNode`; Signals y ClickHouse validan wrappers de aplicación; Fury queda al final porque exige continuidad durable a través de reconciliación/restart. Actions reutiliza el mismo contrato después de deployment; Observability sólo requiere binding o envelope SDK si necesita inspección local.

### Definition of Done

- Un trigger `scope:alpha` produce exclusivamente results `scope:alpha` en todos los estados del golden path.
- Un CP configurado para alpha no procesa `scope:beta`, aun ante un binding erróneo.
- Ausencia de filtro conserva el flujo legacy durante la migración; malformed nunca degrada a legacy.
- Payloads y environments no cambian; el scope sólo vive en envelope y carrier operacional.
- Fury demuestra filtrado server-side y preservación del envelope.
- Tests y E2E prueban `x → x`, rechazo de `x → z`, no-side-effects y rollback.

### Fuera de alcance

- Actions, runtime status, DataProductChanged, Observability, Materializer y KMS en la POC.
- Supervivencia ante restart/reconciliación y diseño de persistencia operacional.
- Nuevos topics, cambio de segmentos o routing productivo.
- Cualquier conversión entre Fury scope y pipeline environment.
- Release compartida de `rio-sdk-events` antes de certificar el piloto.

## Fuentes

- [[Estandarización de Scopes RIO]], [[SPEC técnica — Routing KISS por scope en rio-playmaker]] y [[Scopes RIO - Discovery de Integraciones y Persistencia]].
- `rio-sdk-events origin/master@ad2c98b806cf`: `bigqueue/BigQueueMessage.java`, `BigQueueFilters.java`, `BigQueueClient.java` y `impl/BigQueueClientImpl.java`.
- `rio-controlplane-flink origin/develop@c88038ea1359`: `controller/DeploymentTriggerController.java`, `handler/EventFlinkApp.java` y `deployment/BigQueueDeploymentPublisher.java`.
- `rio-controlplane-kafka origin/develop@1595df01304a`, `rio-controlplane-clickhouse origin/develop@cc64f78b18a7`, `rio-controlplane-fury origin/develop@4c40042c102f`, `rio-controlplane-signals origin/develop@a0ae1324466b` y `rio-controlplane-observability origin/develop@2cc4eaf3e265`: boundaries de trigger/result comparados.
- `vis-items-loader-tagging`: `pkg/services/item_to_publish.go`, `pkg/process/vehicle_risk_profile_unified/create.go` y `pkg/middlewares/filter.go` como evidencia de tags arbitrarios en `modified_fields`.
