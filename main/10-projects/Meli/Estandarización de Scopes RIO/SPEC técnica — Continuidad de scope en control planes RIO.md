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
**Project**: Signals (`rio-controlplane-flink` como piloto; contrato reusable por los control planes RIO)
**Status**: DRAFT
**Deriva de**: [SIG-599](https://spellbook.adminml.com/projects/SIG/specs/SIG-599), [[SPEC técnica — Routing KISS por scope en rio-playmaker]] y [[scope-naming-standard]]
**Baseline revisada**: `rio-sdk-events origin/master@ad2c98b806cf`; `rio-controlplane-flink origin/develop@c88038ea1359`; `rio-controlplane-kafka origin/develop@1595df01304a`; `rio-controlplane-clickhouse origin/develop@cc64f78b18a7`; `rio-controlplane-fury origin/develop@4c40042c102f`; `rio-controlplane-observability origin/develop@2cc4eaf3e265`; `rio-controlplane-signals origin/develop@a0ae1324466b`; corte 2026-09-21

## Propósito

Garantizar continuidad de lane sin transportar estado adicional: un control plane que corre en un scope Fury canónico como `alpha-consumer-nonprod` deduce `lane=alpha` desde el scope entregado por Fury, acepta sólo un trigger con `filters.modified_fields` que contenga exactamente `scope:alpha` y publica el resultado con exactamente `scope:alpha`.

La lane local es la autoridad. El filtro entrante es una aserción que se valida contra ella. El publisher vuelve a resolver la lane desde el runtime y no depende de un carrier originado en la request. El pipeline environment, el segmento BigQueue y los DTOs de negocio permanecen intactos.

La POC implementa el contrato en `rio-controlplane-flink` para `rio-deployment-trigger` → `rio-deployment-result`. La adopción del resto de los control planes ocurre después de certificar el piloto.

## Contenido

## Ubicación en el programa

Esta es la Fase 3 del programa alpha end-to-end. La Fase 1 hace que Fury Routes seleccione el backend; la Fase 2 hace que Playmaker deduzca su lane desde el scope Fury del runtime y publique el trigger con `scope:<lane>`; la Fase 3 aplica la misma regla dentro del control plane y verifica que el filtro recibido coincida con su lane antes de procesar.

No debe confundirse con la fase interna de certificación E2E del planner de Playmaker.

## Invariantes

- `Pipeline Environment ≠ Fury Scope`: `environmentId` y `environmentName` conservan su semántica funcional y no participan en routing.
- El scope Fury canónico sigue `<lane>-<role>[-<qualifier>]-<segment>` y la lane es el primer token normalizado.
- El vocabulario técnico de lane es `prod | stage | alpha | beta | gamma`; cualquier otro primer token no es una lane.
- La aplicación obtiene el scope mediante una API soportada de Fury encapsulada por `FuryRuntimeScopeProvider`; ningún controller, processor ni publisher lee directamente variables de entorno.
- El filtro `scope:x` vive sólo en el envelope BigQueue; no se agrega a `DeploymentTriggerMessage`, `DeploymentResultMessage`, `ActionTriggerMessage` ni `ActionResultMessage`.
- El CP procesa un mensaje scoped sólo cuando `incomingLane == runtimeLane`.
- El publisher deriva `runtimeLane` de nuevo y publica `scope:<runtimeLane>`; no acepta una lane arbitraria como argumento.
- El segmento Fury, `componentType`, auth scopes y tracing scopes son ejes independientes.
- El payload se publica directamente; nunca se envuelve manualmente en `BigQueueMessage`, porque mqclient construye el envelope.
- `ThreadLocal`, MDC, request-scoped beans, estado global y carriers in-memory no participan en la solución.

## Evidencia y puntos en común

| Punto común | Implementación vigente | Uso en la solución |
|---|---|---|
| Envelope tipado | `rio-sdk-events` expone `BigQueueMessage<T>` y `BigQueueFilters.modifiedFields`; Flink, Kafka, ClickHouse, Fury y Signals ya consumen contratos del SDK | Leer y validar `scope:<lane>` sin modificar el payload |
| Publicación filtrada | `BigQueueClient.sendWithFilters(Object, List<String>)` termina en `Producer.send(message, Filters)` | Publicar el result con la lane local |
| Naming canónico | Fase 2 usa scopes como `alpha-api-nonprod` y `alpha-consumer-nonprod` | Resolver ambos como `lane=alpha` mediante el primer token |
| Fuente runtime | Playmaker ya encapsula el `SCOPE` entregado por Fury en `ScopeUtils.getScopeValue()` | Replicar el patrón mediante un provider inyectable y testeable |
| Punto de ingreso | Los CPs reciben el push BigQueue en un controller/adaptor y luego ejecutan el dominio | Aplicar el guard antes de cualquier side effect |
| Punto de egreso | Los CPs concentran resultados en publishers de deployment/actions | Resolver la lane local en el último punto antes de publicar |
| Aislamiento server-side | Fury asocia consumer/binding con filtros BigQueue | Primera barrera; el guard local es defensa en profundidad |

## Hallazgo sobre Fury Toolkit

El diseño exige usar la API soportada por Fury para leer el scope y esconderla detrás de `FuryRuntimeScopeProvider`. La clase concreta no se congela todavía porque las dependencias presentes en los repos no prueban un accessor de scope uniforme: `com.fury.toolkit:java-toolkit-shared` 0.2.1–0.5.0 expone `SegmentationUtils.getSegmentId()`, pero no un equivalente `getScope`; `com.fury:furyutils` expone `FuryUtils.getEnv(String)`, pero no está declarado hoy por estos CPs y su adopción debe validarse con Fury.

G0 debe confirmar con Fury cuál es el accessor soportado para Java/Kotlin. La implementación no debe inventar `FuryScopeUtils`, agregar una dependencia no validada ni dispersar `System.getenv("SCOPE")` por el código. Si la API soportada termina siendo una lectura de `SCOPE`, sólo el adapter puede conocer ese detalle.

## Arquitectura objetivo

```text
Fury runtime scope
alpha-consumer-nonprod
        │
        ▼
FuryRuntimeScopeProvider
        │
        ▼
RuntimeLaneResolver ──────────────────────────┐
lane=alpha                                      │
        │                                           │
        ▼                                           ▼
DeploymentTriggerController                 DeploymentResultPublisher
        │                                           │
        ├─ parsea envelope: scope:alpha                   ├─ vuelve a resolver lane=alpha
        ├─ valida incoming == runtime                    └─ sendWithFilters(result, [scope:alpha])
        └─ recién entonces ejecuta dominio
        │
        ▼
processor / handlers / payloads / DB: SIN CAMBIOS
```

## Contrato de resolución de lane

`RuntimeLaneResolver` recibe el scope completo del provider, lo divide por `-`, toma el primer token no vacío, lo normaliza a lowercase y sólo devuelve un valor si pertenece a `prod | stage | alpha | beta | gamma`.

| Scope Fury | Lane |
|---|---|
| `prod-consumer-nonsite` | `prod` |
| `stage-consumer-nonprod` | `stage` |
| `alpha-consumer-nonprod` | `alpha` |
| `beta-api-nonprod` | `beta` |
| `gamma-tp-nonprod` | `gamma` |
| `consumer-alpha-nonprod` | ausencia; naming no canónico |
| `test` | ausencia; runtime legacy |
| vacío, `null` o delimitadores | ausencia |

El role y el segmento no se interpretan para reconstruir la lane. El resolver no consulta Spring profiles, pipeline environment, nombre del tópico ni configuración `expectedScope`.

## Contrato del filtro entrante

El parser inspecciona `filters.modified_fields` y considera tags cuyo prefijo exacto sea `scope:`. Tags como `componentType:FLINK` pueden coexistir y no cambian la resolución.

| Entrada | Resultado |
|---|---|
| Exactamente un `scope:alpha` y runtime lane `alpha` | Procesar |
| `scope:alpha` y runtime lane `beta` | ACK sin side effects; `scope_mismatch` |
| Dos o más tags `scope:` | ACK sin side effects; `invalid_scope_filter` |
| `scope:`, espacios, mayúsculas, slash, wildcard o lane fuera del vocabulario | ACK sin side effects; `invalid_scope_filter` |
| Sin `scope:` y runtime canónico | ACK sin side effects; `missing_scope_filter` |
| Sin `scope:` y runtime legacy/no resoluble | Procesar en modo legacy |
| Un `scope:x` válido y runtime legacy/no resoluble | ACK sin side effects; `runtime_scope_unresolved` |

El ACK evita retry storms por configuración determinísticamente inválida. Un error transitorio al consultar la fuente runtime o publicar mantiene la semántica de error/retry vigente del CP.

## Contrato de salida

El publisher no recibe `scope` ni `RoutingContext`. Antes de enviar, consulta `RuntimeLaneResolver`:

- Runtime canónico: `sendWithFilters(result, List.of("scope:" + runtimeLane))`.
- Runtime legacy/no resoluble: conserva el publish legacy sin filtro.
- Error transitorio del provider: no publica como legacy; propaga error para evitar fuga silenciosa entre lanes.

La igualdad verificada en el ingreso hace que `scope:x` entrante y `scope:x` saliente coincidan. La derivación local en el egreso evita depender de memoria de request y cubre ejecución asíncrona dentro de la misma lane.

## Modo canónico y modo legacy

No existe feature flag ni `expectedScope` manual. El naming del runtime selecciona el modo:

| Runtime | Trigger aceptado | Result publicado |
|---|---|---|
| Scope canónico con lane `x` | Sólo `scope:x` | Siempre `scope:x` |
| Scope legacy/no resoluble | Sólo mensaje sin `scope:` | Sin filtro |

Por eso el orden de rollout es obligatorio: Playmaker debe publicar filtros antes de activar el consumer con nombre canónico.

## Implementación del piloto Flink

1. Crear `FuryRuntimeScopeProvider` como puerto inyectable y una implementación de plataforma después de cerrar G0.
2. Crear `RuntimeLaneResolver` puro con el vocabulario canónico y tests de naming.
3. En `DeploymentTriggerController`, parsear el filtro y comparar `incomingLane` con `runtimeLane` antes del mapper, processor o cualquier llamada de infraestructura.
4. Mantener `DeploymentProcessor`, `EventFlinkApp`, modelos y payloads sin scope ni contexto de routing.
5. En `DeploymentResultBigQueueEventPublisher`, resolver la lane local al publicar y usar `BigQueueClient.sendWithFilters` cuando sea canónica.
6. Mantener el path de Streams sin cambios; el contrato aplica sólo a BigQueue deployment trigger/result en la POC.

Los errores de mapping que hoy publican un `FAILED` sólo pueden hacerlo después de que el guard haya validado la lane; el publisher igualmente deriva su filtro desde el runtime.

## Límite de ejecución durable

La derivación runtime elimina la necesidad de persistir el filtro sólo si el trabajo permanece en su lane. Un resultado diferido o reconciliado puede usar la lane local con seguridad cuando el storage, lease, queue o selector que recupera el trabajo impide que otra lane lo reclame.

Si un reconciliador `beta` puede reclamar trabajo iniciado en `alpha`, publicaría `scope:beta`. Ese path no puede adoptar este diseño hasta aislar la propiedad del trabajo por lane o persistir una identidad de routing operacional separada del pipeline environment.

Flink es apto para el piloto porque el flujo deployment trigger → result observado converge en el request procesado por la misma instancia. Fury queda al final de la adopción porque sus reconciliadores deben demostrar aislamiento de ownership antes de usar derivación local.

## Reuso y estandarización

La POC mantiene `RuntimeLaneResolver` y el parser del filtro dentro de Flink para no bloquearse por una release compartida. Después de una segunda adopción se decide la extracción:

- La lectura de scope debe reutilizar la API oficial de Fury; si falta un helper estable, se solicita a Fury en vez de inventar uno por CP.
- La convención de naming y el vocabulario pueden vivir en `rio-core-java` si más de un CP los necesita.
- El parser de `BigQueueFilters` puede vivir en `rio-sdk-events` porque pertenece al contrato de transporte.
- `rio-sdk-events` no debe conocer Spring, controllers, profiles, topics ni persistencia de los CPs.

No se promueve una abstracción compartida con un solo consumidor.

## Design Decisions

### DD-1: El scope Fury local es la autoridad

**Decisión**: la lane se deduce del primer token del scope canónico que Fury asigna al runtime; el filtro entrante se valida como aserción.

**Fundamentación**: replica la Fase 2, elimina configuración duplicada y hace que web/consumer con nombres canónicos converjan en la misma lane.

### DD-2: Sin `expectedScope` ni carrier

**Decisión**: no se configura `expectedScope` y no se transporta `RoutingContext` por controller, processor o eventos internos.

**Fundamentación**: ambos datos duplicarían una identidad que Fury ya entrega al proceso. La igualdad se valida al entrar y la misma regla se ejecuta al salir.

### DD-3: Broker filter más guard local fail-closed

**Decisión**: Fury filtra server-side y el CP compara el filtro recibido con su lane local antes de cualquier side effect.

**Fundamentación**: el binding es la barrera principal; el guard detecta bindings incorrectos y evita procesar `scope:z` en la lane `x`.

### DD-4: Compatibilidad determinada por naming

**Decisión**: runtime canónico exige filtro coincidente; runtime legacy procesa y publica sin filtro.

**Fundamentación**: permite coexistencia durante rollout sin feature flags ni config por lane, pero evita que un runtime canónico procese mensajes ambiguos.

### DD-5: El publisher no acepta scope externo

**Decisión**: el publisher deriva la lane local inmediatamente antes de enviar.

**Fundamentación**: reduce las superficies capaces de producir `scope:z` y preserva el filtro en tareas asíncronas de la misma lane.

## Archivos del piloto

### Archivos nuevos

| Archivo conceptual | Responsabilidad |
|---|---|
| `routing/FuryRuntimeScopeProvider` | Encapsular la API soportada por Fury y permitir tests sin tocar el ambiente real |
| `routing/RuntimeLaneResolver` | Resolver el primer token canónico y el modo canonical/legacy |
| `routing/ScopeFilterParser` | Extraer exactamente un `scope:<lane>` válido desde `BigQueueFilters` |

### Archivos modificados

| Superficie | Cambio |
|---|---|
| `deployment/DeploymentTriggerController` | Ejecutar parser y guard runtime antes de mapping/processing |
| `deployment/DeploymentResultBigQueueEventPublisher` | Resolver la lane local y usar `sendWithFilters` |
| Configuración Spring | Inyectar provider/resolver; no agregar `expectedScope` |
| Tests de controller, resolver, parser y publisher | Cubrir matriz canonical/legacy, mismatch y errores del provider |

### No tocar

- `DeploymentTriggerMessage`, `DeploymentResultMessage` y demás records de `rio-sdk-events`.
- `DeploymentProcessor`, `EventFlinkApp`, command/events internos y modelos de dominio.
- Pipeline environment, DB, KVS, idempotencia, history, payloads y schema versions.
- Segment IDs, topic names y bindings Fury desde el repo de aplicación.
- Actions, runtime status, Observability, Materializer y KMS en esta POC.

## Estrategia de tests

- Resolver: matriz `prod/stage/alpha/beta/gamma`, mayúsculas normalizadas, nombres legacy, orden incorrecto, vacío y malformed.
- Parser: un solo tag válido, coexistencia con `componentType`, duplicados, vacío, unknown, espacios y wildcard.
- Guard canónico: runtime alpha + filtro alpha ejecuta; runtime alpha + beta/missing/malformed no llama mapper, processor ni infraestructura.
- Guard legacy: runtime no resoluble + mensaje sin filtro ejecuta; runtime legacy + filtro scoped no ejecuta.
- Publisher canónico: runtime alpha llama exactamente `sendWithFilters(payload, ["scope:alpha"])`.
- Publisher legacy: runtime no resoluble conserva exactamente el publish sin filtro.
- Error provider: no degrada a legacy ni publica sin filtro.
- Wire: payload serializado no cambia y el scope aparece sólo en `filters.modified_fields`.
- Integración: trigger `scope:alpha` consumido por `alpha-consumer-nonprod` produce result `scope:alpha`; un trigger `scope:beta` no genera side effects ni result.
- No-regression: Streams y los paths legacy mantienen su comportamiento.
- Calidad: tests críticos primero, checks del repo y ≥95% de cobertura sobre código nuevo.

## Observabilidad

Métricas bounded por resultado de routing, nunca por lane dinámica:

- `routing_mode:canonical|legacy`
- `routing_outcome:accepted|missing_scope_filter|invalid_scope_filter|scope_mismatch|runtime_scope_unresolved|provider_error`

Los logs pueden incluir el outcome y un identificador de mensaje ya permitido. No imprimen el mapa completo de variables de entorno ni agregan scope, IDs o payload como tags de métrica.

## Gates y rollout

| Gate | Evidencia | Habilita |
|---|---|---|
| G0 — API Fury | Fury confirma el accessor soportado para scope Java/Kotlin; provider testeable definido sin dependencia inventada | Implementación local |
| G1 — Contrato unitario | Resolver, parser, guard y publisher verdes; payload sin cambios | Deploy alpha |
| G2 — Binding | Fury demuestra filtrado server-side y preservación de `filters.modified_fields` en el push | E2E |
| G3 — Continuidad | `scope:alpha` trigger → procesamiento alpha → `scope:alpha` result; beta/missing no procesados | Segunda adopción |

Orden:

1. Confirmar G0 y cerrar la implementación del provider.
2. Desplegar Playmaker que publica `scope:alpha`.
3. Crear/validar `alpha-consumer-nonprod` y su binding `scope:alpha`.
4. Desplegar Flink con guard y publisher runtime-derived.
5. Ejecutar happy path, mismatch, missing y rollback.

Rollback: volver al artefacto y binding legacy de Flink. No hay schema, backfill, carrier ni estado persistido que revertir.

## Adopción posterior

Orden recomendado: Kafka → Signals → ClickHouse → Fury. Los tres primeros validan adapters distintos sin reconciliación cross-lane. Fury se adopta sólo después de demostrar que cada reconciliador recupera trabajo de su propia lane o de diseñar identidad operacional durable.

Actions reutiliza el mismo contrato después de deployment. Observability sólo requiere binding o envelope SDK si necesita inspección local.

## Definition of Done

- El provider usa una API de scope soportada por Fury y es la única frontera que conoce su mecanismo concreto.
- `alpha-consumer-nonprod` deriva `alpha` desde el naming canónico sin `expectedScope`.
- Un trigger con `scope:alpha` produce un result con `scope:alpha`.
- `scope:beta`, filtro ausente o filtro malformed no generan side effects en un runtime alpha.
- Runtime legacy y mensaje legacy conservan el comportamiento previo.
- No existen carrier, cambios de payload, cambios de DB ni lectura de pipeline environment.
- Fury demuestra filtrado server-side y preservación del envelope.
- Tests, E2E, observabilidad, rollout y rollback quedan enlazados como evidencia.

## Fuera de alcance

- Configurar `expectedScope` o una lane manual por deployment.
- Propagar el filtro por commands, events internos, `ThreadLocal`, MDC, payloads o entidades.
- Inferir lane desde pipeline environment, segmento, role, topic o Spring profile.
- Adoptar reconciliadores que puedan reclamar trabajo de otra lane.
- Agregar soporte de scope a Actions, runtime status, Observability, Materializer o KMS en el piloto.
- Crear topics, cambiar DTOs o hacer release productivo desde una feature branch.

## Fuentes

- [[SPEC técnica — Routing KISS por scope en rio-playmaker]] y [[POC KISS — Routing de scopes en Playmaker]].
- [[scope-naming-standard]] para `<lane>-<role>[-<qualifier>]-<segment>`.
- `rio-sdk-events origin/master@ad2c98b806cf`: `BigQueueMessage`, `BigQueueFilters` y `BigQueueClient.sendWithFilters`.
- Refs de control planes declaradas en la baseline para controllers, wrappers y publishers existentes.
- `com.fury.toolkit:java-toolkit-shared` 0.2.1–0.5.0: `SegmentationUtils.getSegmentId()` como precedente, sin accessor de scope observado.
- `com.fury:furyutils` 1.0.1: `FuryUtils.getEnv(String)` observado, pendiente de validación de soporte/adopción con Fury.
