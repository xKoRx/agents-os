---
type: project
schema_version: 1
owner: agent
root: false
status: active
priority: P1
area: "[[Meli]]"
parent: "[[Estandarización de Scopes RIO]]"
sprint:
start: 2026-09-16
due:
progress: 5
repo: https://github.com/melisource/fury_rio-playmaker
jira: SIG-599
prs:
aliases:
  - POC Playmaker scope alpha
  - Routing KISS de scopes en rio-playmaker
tags:
  - kind/project
  - area/meli
  - project/scopes-rio
  - tech/rio-playmaker
created: "2026-09-16"
updated: "2026-09-16"
---

# POC KISS — Routing de scopes en Playmaker

> [!info]+ Estado ejecutivo
> **Ready phase:** Fase 0 · **Gate actual:** G0 `pending` · **Base local verificada:** `origin/master@f350fb26091d` · **Principio rector:** demostrar `alpha` reutilizando filtros BigQueue; ningún cambio de DTO o release de `rio-sdk-events`.

## 🎯 Objetivo

Implementar y certificar en `rio-playmaker` el slice POC de SIG-599: recibir `X-Rio-Scope: alpha`, validarlo contra `alpha-api-nonprod`, persistir `environment_scope=alpha` en la ejecución, publicar triggers con `scope:alpha` y procesar resultados sólo cuando filtro, runtime `alpha-consumer-nonprod` y ejecución persistida coinciden. El trabajo debe ser ejecutable por agentes fase a fase y revisable bajo KISS/YAGNI sin redescubrir arquitectura ni ampliar el alcance.

## 📊 Estado actual

- La planificación y la [[SPEC técnica — Routing KISS por scope en rio-playmaker]] están listas para una revisión independiente POC KISS; no se modificó ningún repositorio de código.
- Baseline `rio-playmaker`: ref local `origin/master@f350fb26091d`, tag `202609.16.0`. El checkout activo está en `feature/sig-610-inactivate-component-run@1c2601f96d58`, su upstream fue eliminado y contiene sólo untracked ajenos (`.claude/settings.local.json`, `.claude/skills/aoc-management/`, `graphify-out/`, `scripts/inactivate-probe/`); no deben tocarse. El fetch remoto falló por allowlist de GitHub sin GlobalProtect, por lo que Fase 0 revalida la base.
- Baseline `rio-sdk-events`: `master@3e3acd1`. Ya contiene `BigQueueMessage.filters`, `BigQueueFilters.modifiedFields` y `BigQueueClient.sendWithFilters`; `DeploymentTriggerMessage` y `DeploymentResultMessage` no necesitan `environment_scope`.
- Baseline mqclient: `3.4.9`, resuelto por `rio-playmaker/build.gradle`; el artefacto expone `Producer.send(Object, Filters)` y `Filters(List<String>)`.
- Trabajo restante verificado: ingreso/runtime guard, persistencia e idempotencia scope-aware, carrier async, publish filtrado inicial/siguientes batches/retry, guard de results antes de side effects, observabilidad bounded y certificación E2E con Fury/Flink.
- Estado planner: `ready_for_phase_0`. Ninguna decisión de negocio queda abierta; las capabilities externas no verificadas son spikes con stop condition en F0.

## Resumen ejecutivo y trabajo restante

La POC no necesita una fase de SDK. El filtro ya forma parte del envelope BigQueue y el producer actual soporta la sobrecarga filtrada. Playmaker sí necesita conservar el ambiente después del request HTTP porque el dispatch corre `AFTER_COMMIT`, puede saltar de thread y puede reconstruirse en un retry. Por eso la mínima fuente durable es `pipeline_execution.environment_scope`.

El recorrido objetivo tiene una sola autoridad por frontera: el runtime valida el header al ingreso; la ejecución persistida gobierna publishes y retries; el envelope lleva `scope:alpha`; el consumer exige igualdad entre envelope, runtime y ejecución antes de mutar estado. La feature queda apagada por default y sólo se habilita de forma conjunta en los runtimes alpha después de validar Fury y Flink.

## Matriz requisito → evidencia

| ID | Requisito | Estado | Evidencia | Trabajo restante |
|---|---|---|---|---|
| R1 | Capturar `X-Rio-Scope` en deploy | `partial` | `HEAD` `PipelineDeploymentController.deployPipeline` ya recibe todos los headers en `rio-playmaker@f350fb26091d:src/main/java/com/mercadolibre/rio/playmaker/controller/PipelineDeploymentController.java:L97` | Resolver/validar el header explícitamente |
| R2 | Validar scope contra runtime | `missing` | `HEAD` `ScopeUtils.getScopeValue` sólo expone `SCOPE` en `rio-playmaker@f350fb26091d:src/main/java/com/mercadolibre/rio/playmaker/util/ScopeUtils.java:L88` | Crear resolver sin cambiar perfiles legacy |
| R3 | Persistir ambiente lógico | `missing` | `HEAD` `PipelineExecutionModel` no tiene scope en `rio-playmaker@f350fb26091d:src/main/java/com/mercadolibre/rio/playmaker/model/PipelineExecutionModel.java:L33` | Columna nullable + campo inmutable + lifecycle |
| R4 | Evitar idempotencia cross-lane | `missing` | `HEAD` repository consulta hash+pipeline+status en `rio-playmaker@f350fb26091d:src/main/java/com/mercadolibre/rio/playmaker/repository/PipelineExecutionRepository.java:L54` | Incluir `environmentScope` en las tres consultas |
| R5 | Sobrevivir async y retry | `partial` | `HEAD` `DispatchRequest` es carrier inmutable y `DeploymentTimeoutJob` llega a `DeploymentGroup.pipelineExecution` | Transportar/recuperar el scope persistido |
| R6 | Publicar `scope:alpha` | `partial` | `CONTRACT` mqclient 3.4.9 ofrece `Producer.send(message, Filters)`; el impl actual usa `send(message)` | Usar la sobrecarga existente sin migrar producer |
| R7 | Consumir el filtro | `partial` | `CONTRACT` SDK modela `BigQueueMessage.filters`; `HEAD` controller lo descarta en `DeploymentResultConsumerController.java:L47` | Retener envelope y ejecutar guard antes del handler |
| R8 | Reutilizar SDK sin nuevo DTO | `done` | `CONTRACT` `rio-sdk-events@3e3acd1` ya modela filtros | No modificar ni publicar SDK |
| R9 | Aislar history/detail por lane | `missing` | `HEAD` GETs no reciben header y repository lista sólo por pipeline/environment | Exigir/validar scope con feature activa y filtrar lecturas |
| R10 | Verificar filtro server-side y continuidad Flink | `blocked` | `ROADMAP` SIG-599 lo exige; no hay evidencia runtime adjunta | F0 obtiene evidencia o bloquea G0 |

## Alcance, no alcance y decisiones

### Alcance

- `rio-playmaker`, únicamente el flow de pipeline deployment por BigQueue y sus resultados.
- Lane `alpha`, runtimes `alpha-api-nonprod` y `alpha-consumer-nonprod`.
- Tópicos existentes `rio-deployment-trigger` y `rio-deployment-result` en nonprod.
- Header, persistencia, idempotencia, history/detail, dispatch inicial/siguientes batches/retry, result guard, métricas, tests y feature flag.

### No alcance

- Cambios o release en `rio-sdk-events`; campos nuevos en payloads; incremento de schema version.
- Actions, inactivation, `DataProductChanged`, Materializer, KMS, Observability, runtime status o topics nuevos.
- Código de Flink o infraestructura Fury; este proyecto sólo consume sus contratos y certifica el E2E.
- Producción, backfill de filas legacy, DB por lane, migración de todos los producers BigQueue o catálogo dinámico completo.

### Registro de decisiones

| ID | Estado | Resolución | Fuente/evidencia | Fase que consume |
|---|---|---|---|---|
| D1 | `CONFIRMED` | POC KISS usa filtros `scope:alpha`; no agrega `environment_scope` a los DTOs SDK | Decisión de Rodrigo 2026-09-16 + SDK existente | F0–F4 |
| D2 | `CONFIRMED` | El header viene del front y Playmaker lo captura, pero sólo lo acepta si coincide con su runtime | Decisión de Rodrigo + SIG-599 US-12 | F1 |
| D3 | `TECHNICAL_RESOLUTION` | `PipelineExecutionModel.environmentScope` es la autoridad durable; no se usa `ThreadLocal` ni request context | `AFTER_COMMIT`, async y retry verificados | F1–F3 |
| D4 | `TECHNICAL_RESOLUTION` | Idempotencia y lecturas incorporan scope para no mezclar lanes sobre DB test compartida | Queries HEAD sin scope | F1 |
| D5 | `TECHNICAL_RESOLUTION` | Se mantiene mqclient y se usa `Producer.send(message, Filters)` | Contrato mqclient 3.4.9 | F2 |
| D6 | `TECHNICAL_RESOLUTION` | Mismatch de result se ACKea con 200, sin side effects, y se mide con reason bounded | Error determinístico; evita poison-loop | F3 |
| D7 | `TECHNICAL_RESOLUTION` | Una única feature `rio.scope-routing.enabled`, default false, activa el contrato completo por runtime | Compatibilidad/rollback KISS | F1–F4 |
| D8 | `TECHNICAL_RESOLUTION` | La verificación de filtro server-side/Fury es precondición de implementación, no una suposición; si falla se marca `PLAN_CONFLICT` | Incertidumbre externa acotada | F0 |
| D9 | `TECHNICAL_RESOLUTION` | La rama será `feature/sig-599-playmaker-scope-routing-poc`, creada desde el `origin/master` revalidado después de aceptar G0 | Aislamiento de cambios y proceso de release | F1 |

## Arquitectura actual y objetivo

### Actual

```text
HTTP headers ─► PipelineDeployService ─► PipelineExecution (sin scope)
                                      └► DispatchRequest ─► producer.send(payload)
Retry ─► reconstruye payload ─► producer.send(payload)
BigQueue result envelope ─► controller descarta filters ─► handler muta estado
```

### Objetivo

```text
X-Rio-Scope ─► runtime guard ─► PipelineExecution.environmentScope
                                      │
                                      ├► DispatchRequest ─► send(payload, scope filter)
                                      ├► next batch ─────► send(payload, scope filter)
                                      └► retry ──────────► send(payload, scope filter)

result envelope ─► parse scope filter ─► runtime match ─► execution match ─► existing handler
                                                └─ mismatch: ACK + metric, zero side effects
```

## Secuencia de datos y control

1. Fury Route envía `X-Rio-Scope: alpha` al runtime `alpha-api-nonprod`.
2. El resolver normaliza el header, deriva `alpha` desde el runtime canónico y exige igualdad.
3. El deploy calcula delta/hash, consulta idempotencia con `environmentScope=alpha` y persiste la nueva ejecución.
4. Los grupos y batches enlazan esa ejecución; `DispatchRequest` transporta `alpha` al listener async.
5. El producer publica el payload SDK existente con `Filters(["scope:alpha"])`.
6. Flink alpha consume y publica el result con el mismo filtro; esta continuidad es contrato externo.
7. Playmaker consumer conserva el envelope, resuelve `alpha` desde runtime, correlaciona la ejecución y exige triple igualdad antes del handler actual.
8. Retries reconstruidos desde DB vuelven a publicar `scope:alpha`; nunca releen el header.

## Contratos versionados y edge cases

La autoridad completa es [[SPEC técnica — Routing KISS por scope en rio-playmaker]]. Contratos congelados para ejecución:

- HTTP v1: `X-Rio-Scope`, regex `^[a-z0-9][a-z0-9-]{0,62}$`; missing/malformed `400`, runtime mismatch `409`.
- Runtime v1: `^([a-z0-9]+)-(api|consumer)-(nonprod|nonsite)$`; POC acepta `alpha-api-nonprod` y `alpha-consumer-nonprod`.
- DB v1: `pipeline_execution.environment_scope VARCHAR(63) NULL`, inmutable para nuevas ejecuciones scoped; sin backfill.
- Envelope v1: exactamente un tag `scope:<environment>` dentro de `filters.modified_fields`; tags no-scope adicionales permitidos.
- Legacy v1: feature false conserva publish/consume actuales y filas `NULL`; feature true falla cerrado ante scope ausente.
- Result v1: filtro/runtime/ejecución deben coincidir; mismatch retorna 200 sin side effects; infraestructura transitoria después de guard válido conserva 5xx/retry.
- Seguridad: no loguear mapa de headers ni valores crudos inválidos; no usar scope dinámico como metric tag.
- Fórmulas de negocio: no aplica cálculo numérico; la única condición es igualdad exacta normalizada entre tres fuentes.

## Roadmap dependency-ordered

| Fase | Resultado | Carga relativa | Gate |
|---|---|---|---|
| F0 | Revisión independiente KISS, base fresca y capabilities externas verificadas | Media por incertidumbre externa, cero código | G0 |
| F1 | Ingreso, runtime guard, persistencia, idempotencia y lecturas aisladas | Alta por schema + API + compatibilidad | G1 |
| F2 | Trigger filtrado en dispatch inicial, siguientes batches y retry | Media por frontera async/BQ | G2 |
| F3 | Result guard fail-closed, ACK de mismatch y observabilidad | Alta por riesgo de side effects | G3 |
| F4 | Integración alpha, rollout/rollback y evidencia final | Alta por múltiples sistemas, sin ampliar código | G4 |

## Mapa de archivos y símbolos

| Acción | Superficie | Fase |
|---|---|---|
| `create` | `ScopeRoutingConfig`, `ScopeRoutingResolver` y tests unitarios | F1 |
| `create` | Migraciones equivalentes `playmkrtst`, `playmkrstg`, `playmkrprod` | F1 |
| `modify` | `PipelineDeploymentController`, `PipelineDeployServiceImpl`, `PipelineHistoryServiceImpl` y contratos asociados | F1 |
| `modify` | `PipelineExecutionModel`, lifecycle y repository | F1 |
| `modify` | `DispatchRequest`, `DispatchRequestFactory`, `BigQueueDispatchAdapter`, `DeploymentTriggerProducer`/impl | F2 |
| `modify` | `DeploymentTimeoutJob.retry` | F2 |
| `modify` | `DeploymentResultConsumerController`, consumer service/guard y `DeploymentResultMetrics` | F3 |
| `no-touch` | `rio-sdk-events`, DTOs, schema version, Actions, DataProductChanged y Materializer | Todas |
| `no-touch` | Untracked del checkout existente | Todas |

## Estrategia de validación

- Unit: resolver, parsing de filtro, publisher con `Filters`, drop reasons y no-call al handler.
- Contract: payload SDK byte-compatible, exactamente un `scope:alpha`, feature false conserva overload legacy.
- Integration: migraciones, idempotencia cross-lane, history/detail aislados, dispatch `AFTER_COMMIT`, timeout retry y consumer con DB real.
- Workflow: first batch, next batch, retry y result válido/alterado.
- E2E: header alpha → route alpha → trigger alpha → Flink alpha → result alpha → estado terminal; negativos missing/mismatch y ausencia de side effects en otra lane.
- Calidad: tests críticos antes del cambio, checks del repo y ≥95% de cobertura sobre código nuevo.

## Compatibilidad, observabilidad, rollout y rollback

- Compatibilidad por flag default false y columna nullable; no se hace backfill ni cambio de wire schema.
- Métricas con reasons bounded: `missing_header`, `invalid_header`, `runtime_mismatch`, `missing_persisted_scope`, `missing_filter`, `malformed_filter`, `execution_mismatch`.
- Rollout: migraciones → código flag off → Fury/Flink listos → flag on conjunto en API+consumer alpha → golden deploy → negativos.
- Rollback: flag off conjunto y pausa de bindings alpha si corresponde; no eliminar columna ni hacer rollback destructivo.
- Release: ninguna promoción productiva desde feature branch; la rama de POC sólo entrega PR/evidencia y el release sigue la base/proceso aprobado del repo.

## Riesgos, supuestos y controles humanos

| Riesgo/supuesto | Mitigación | Control humano |
|---|---|---|
| Ref local stale por falta de GlobalProtect | F0 hace fetch/rebase de evidencia o bloquea | Rodrigo acepta G0 |
| Fury filtra después de entregar y no server-side | No sustituir con filtro app silencioso; `PLAN_CONFLICT` | Rodrigo/Fury decide arquitectura |
| Flink no preserva el filtro | Detener F4 y corregir su SPEC, no agregar campo SDK sin nueva decisión | Rodrigo acepta cambio de alcance |
| DB test compartida mezcla idempotencia/history | Scope en queries y tests cross-lane | Reviewer valida G1 |
| Un publish/retry pierde filtro | Fail-closed + tests de first/next/retry | Reviewer valida G2 |
| Result incorrecto muta estado antes del guard | Guard anterior al handler y asserts zero-side-effect | Reviewer valida G3 |
| Agente amplía a otros eventos o migra producer | `No tocar`, stop behavior y review KISS | Rechazar gate |

## Definition of Done

- G0–G4 en `accepted` por el owner; ningún agente acepta su propio gate.
- SPEC técnica sigue derivando de SIG-599 y no aparece una SPEC de SDK para la POC.
- Header/runtime, persistencia, idempotencia y lecturas están aislados por `alpha`.
- Todos los triggers scoped, incluidos next batch y retry, llevan exactamente `scope:alpha`.
- Result mismatch se ACKea, se observa y no produce side effects.
- SDK, payloads, topics y eventos fuera de alcance no cambian.
- Checks, cobertura nueva ≥95%, E2E alpha, rollback y evidencia están enlazados.
- El PR está listo para revisión; no se ejecutó release productivo desde la feature branch.

## Control de gates

| Gate | current state | phase agent responsibility | owner acceptance evidence | enables |
|---|---|---|---|---|
| G0 | `pending` | Dejar revisión en `review`, adjuntar SHA fresco y pruebas de Fury/Flink o marcar `blocked` | Rodrigo confirma KISS, base y capabilities | F1 |
| G1 | `pending` | Dejar schema/API/tests en `review` | Migraciones, tests cross-lane y diff acotado aprobados | F2 |
| G2 | `pending` | Dejar publish/retry/tests en `review` | Evidencia exacta de filtro en first/next/retry | F3 |
| G3 | `pending` | Dejar guard/metrics/tests en `review` | Negativos demuestran zero-side-effect y ACK | F4 |
| G4 | `pending` | Dejar E2E/rollback/evidencia en `review` | Golden deploy, aislamiento y rollback aceptados | cierre |

## Paquetes autónomos

### Paquete autónomo Fase 0 — Revisión independiente POC KISS

**Misión exacta**

Revisar la SPEC y este planner como un agente independiente, revalidar la base de `origin/master` y convertir las dos dependencias externas en evidencia verificable sin escribir código.

**Precondiciones verificables**

- Ninguna; es la fase inicial.
- GlobalProtect disponible para refrescar refs y consultar superficies Fury necesarias; si no está disponible, la fase puede revisar diseño pero G0 queda `blocked`.

**Lectura obligatoria**

- `VAULT_ROOT/10-projects/Meli/Estandarización de Scopes RIO/SPEC técnica — Routing KISS por scope en rio-playmaker.md` completo.
- `VAULT_ROOT/30-resources/rio-atlas/architecture/scope-naming-standard.md`, US-12, business rule 15 y E2E-6.
- `rio-playmaker/AGENTS.md`, instrucciones Java/seguridad aplicables y los archivos de la matriz R1–R10 sobre la base fresca.
- `rio-sdk-events`: `BigQueueMessage`, `BigQueueFilters`, `BigQueueClient`, `DeploymentTriggerMessage`, `DeploymentResultMessage`.

**Decisiones cerradas**

- Aplicar POC KISS/YAGNI: sin campo SDK, topic nuevo, producer migration, catálogo general ni eventos adyacentes.
- El reviewer no rediseña por preferencia; reporta contradicción ejecutable como `PLAN_CONFLICT`.

**Implementación paso a paso**

1. Refrescar `origin/master`, registrar SHA/tag y comparar los símbolos citados; no cambiar el checkout sucio del usuario.
2. Confirmar por compilación/javap/test existente las firmas de mqclient y del envelope SDK.
3. Obtener evidencia de que Fury Route preserva `X-Rio-Scope`, no cruza a prod y que consumer filters sobre `modified_fields` son server-side.
4. Confirmar con la SPEC de Flink que el result conserva el mismo filtro; no implementar Flink aquí.
5. Revisar cada DD y archivo afectado, buscando sólo complejidad innecesaria, huecos de aislamiento o contradicciones.
6. Actualizar matriz, riesgos, SHA y G0; dejar G0 en `review`, `blocked` o `rejected`, nunca `accepted`.

**Archivos esperados**

- `modify`: este planner y, sólo si la evidencia contradice el diseño, la SPEC técnica.
- `create`: evidencia externa compacta sólo si no existe un artefacto enlazable.
- Código de repos: ninguno.

**No tocar**

- Cualquier código, config o infraestructura; otros planners/specs; untracked del usuario.

**Spikes permitidos**

- Read-only: fetch, `git show`, `javap`, inspección de configuración y prueba no mutante de Fury/filter. Stop si requiere deploy, binding o publicación real.

**Tests y asserts**

- Assert base: todos los símbolos/firmas persisten en el SHA fresco.
- Assert KISS: cero cambios requeridos en SDK/DTO/topic/schema version.
- Assert plataforma: evidencia explícita de route/header, aislamiento test/prod, filtro server-side y continuidad Flink; una ausencia bloquea G0.

**Entregables/Gate G0**

- Review independiente, matriz actualizada, baseline fresco y links a evidencia externa. G0 queda `review` para Rodrigo.

**Handoff a Fase 1**

- El siguiente agente recibe G0 `accepted`, SHA/base definitivos, branch name y contratos sin volver a descubrir SDK/mqclient/Fury.

### Paquete autónomo Fase 1 — Ingreso, persistencia e aislamiento de lecturas

**Misión exacta**

Implementar el runtime/header guard, persistir el scope en `PipelineExecution`, hacer idempotencia y history/detail scope-aware y mantener compatibilidad con feature apagada.

**Precondiciones verificables**

- G0 `accepted` por Rodrigo.
- Branch `feature/sig-599-playmaker-scope-routing-poc` creada desde la base aceptada; working tree sin incorporar untracked ajenos.

**Lectura obligatoria**

- `VAULT_ROOT/10-projects/Meli/Estandarización de Scopes RIO/SPEC técnica — Routing KISS por scope en rio-playmaker.md`, secciones ingreso, persistencia, compatibilidad y tests.
- `PipelineDeploymentController`, `PipelineDeployServiceImpl`, `PipelineHistoryServiceImpl`, `PipelineExecutionModel`, lifecycle y repository en la base aceptada.
- Migraciones de creación de `pipeline_execution` y convenciones tst/stg/prod.

**Decisiones cerradas**

- Feature única default false; header requerido con feature true; missing/malformed 400, mismatch 409.
- Columna nullable sin backfill; nuevas ejecuciones scoped exigen valor; idempotencia y lecturas incluyen scope.
- Resolver puro/sin estado global; no tocar la lógica legacy de perfiles de `ScopeUtils` salvo reutilizar `getScopeValue`.

**Implementación paso a paso**

1. Escribir tests críticos del resolver, error mapping, idempotencia cross-lane e isolation de history/detail.
2. Crear config/resolver y contrato de excepciones HTTP sin loguear header crudo.
3. Agregar tres migraciones equivalentes e índice; mapear `environmentScope` inmutable.
4. Extender lifecycle `create` y deploy service para resolver una vez y persistir el valor.
5. Reemplazar las tres queries completed/running/pending por variantes scope-aware cuando feature true y conservar legacy cuando false.
6. Exigir el mismo header/runtime guard en listHistory/getExecution/getComponentLogs y filtrar por `environmentScope` antes de responder.
7. Ejecutar unit/integration/format/lint del repo y actualizar el gate.

**Archivos esperados**

- `create`: `ScopeRoutingConfig`, `ScopeRoutingResolver`, tests y tres migrations.
- `modify`: controllers/services de deploy/history/logs, model, lifecycle, repository, config y tests relacionados.
- `conditional`: exception/handler dedicado si los tipos actuales no expresan 400/409 sin duplicación.

**No tocar**

- Producers/consumers BigQueue, SDK, DTOs, Flink, Actions, Materializer y untracked ajenos.

**Spikes permitidos**

- Sólo inspección puntual de la estrategia de repository/history actual. Si aislar detail/logs exige una nueva frontera de autorización no descrita, `PLAN_CONFLICT`.

**Tests y asserts**

- Feature off reproduce comportamiento actual y `environment_scope=NULL`.
- Feature on acepta sólo `alpha` contra `alpha-api-nonprod`; errores no crean ejecución.
- Misma hash/pipeline en alpha y beta no colisiona; una ejecución beta no aparece por list/detail/logs desde alpha.
- Migraciones equivalentes y reversibilidad compatible por flag; ≥95% de cobertura nueva.

**Entregables/Gate G1**

- Diff acotado, migraciones, reportes de tests/cobertura y ejemplos HTTP. G1 queda `review`.

**Handoff a Fase 2**

- El siguiente agente recibe G1 `accepted`, `environmentScope` persistido y accesible desde `PipelineExecution`, sin redescubrir ingreso/idempotencia.

### Paquete autónomo Fase 2 — Publicación filtrada y retries

**Misión exacta**

Propagar el scope persistido por el carrier async y publicar exactamente `scope:alpha` en primer dispatch, siguientes batches y timeout retry usando mqclient existente.

**Precondiciones verificables**

- G1 `accepted`; migraciones/model/lifecycle integrados.

**Lectura obligatoria**

- `VAULT_ROOT/10-projects/Meli/Estandarización de Scopes RIO/SPEC técnica — Routing KISS por scope en rio-playmaker.md`, secciones envelope, publicación y no tocar.
- `DispatchRequest`, `DispatchRequestFactory`, `DeploymentDispatchEventListener`, `BigQueueDispatchAdapter`, `DeploymentTriggerProducer`/impl, `OrchestrationServiceImpl`, `DeploymentTimeoutJob.retry` y tests asociados.

**Decisiones cerradas**

- `DispatchRequest` transporta scope; producer recibe scope y usa `new Filters(List.of("scope:" + scope))`.
- Payload SDK y `withSegmentID` no cambian; scoped missing falla cerrado, no hace fallback legacy.
- Retry lee el scope de `DeploymentGroup.pipelineExecution`.

**Implementación paso a paso**

1. Escribir tests de producer/carrier/first batch/next batch/retry antes del cambio.
2. Agregar `environmentScope` al record y factory desde la ejecución persistida.
3. Extender el port/adapter/producer con la mínima firma que evite duplicar construcción del tag.
4. Usar `Producer.send(message, Filters)` sólo en scoped; feature off conserva `send(message)`.
5. Cambiar retry para resolver la ejecución y publicar con el mismo scope; missing scope scoped falla y no envía.
6. Verificar que siguientes batches derivan del mismo `PipelineExecution` sin leer request context.
7. Ejecutar tests y actualizar G2.

**Archivos esperados**

- `modify`: carrier, factory, adapter, producer interface/impl, timeout job y tests.
- `create`: helper mínimo de filtro sólo si el resolver de F1 no puede reutilizarse sin acoplamiento.

**No tocar**

- SDK/DTOs/schema version, otros producers, nombres de topic, segment ID, result consumer, infra y untracked ajenos.

**Spikes permitidos**

- Ninguno arquitectónico. Una firma mqclient distinta a la validada es `PLAN_CONFLICT`.

**Tests y asserts**

- Scoped first/next/retry llama exactamente una vez `send(message, Filters)` con `scope:alpha`.
- Scoped nunca llama overload sin filtros; legacy feature off sí conserva el overload actual.
- El scope sobrevive `AFTER_COMMIT`; publish failure conserva `QueueException` y semántica de retry/atomicidad.
- Payload serializado no gana `environment_scope`; ≥95% de cobertura nueva.

**Entregables/Gate G2**

- Diff, tests y captura/fixture del envelope de first/next/retry. G2 queda `review`.

**Handoff a Fase 3**

- El siguiente agente recibe G2 `accepted` y el contrato exacto del envelope producido, sin cambiar el publisher.

### Paquete autónomo Fase 3 — Guard de resultados antes de side effects

**Misión exacta**

Conservar el envelope del result, comparar filtro/runtime/ejecución antes del handler, ACKear mismatches sin side effects y emitir observabilidad bounded.

**Precondiciones verificables**

- G2 `accepted`; producer scoped estable.

**Lectura obligatoria**

- `VAULT_ROOT/10-projects/Meli/Estandarización de Scopes RIO/SPEC técnica — Routing KISS por scope en rio-playmaker.md`, secciones consumo, errores y observabilidad.
- `DeploymentResultConsumerController`, `DeploymentResultConsumerService`/impl, `DeploymentResultHandlerImpl`, modelos/repos de DeploymentGroup/Deployment y `DeploymentResultMetrics`.

**Decisiones cerradas**

- Exactamente un tag `scope:`; extras no-scope permitidos.
- Triple igualdad exacta; mismatch determinístico retorna 200, registra reason bounded y no llama handlers.
- `INACTIVATE` queda fuera; no cambiar su flujo en esta POC.

**Implementación paso a paso**

1. Escribir tests negativos que verifiquen explícitamente cero llamadas/mutaciones.
2. Cambiar el contrato del consumer para recibir envelope o scope parseado sin descartar filters.
3. Crear/reutilizar parser de filtro y runtime resolver de F1.
4. Correlacionar `deploymentId → Deployment → DeploymentGroup → PipelineExecution` antes del handler para ejecuciones de deployment.
5. Aplicar triple guard y ACK/drop reasons; dejar 5xx actuales sólo para fallos transitorios posteriores a un guard válido.
6. Extender métricas con catálogo bounded, sin tag dinámico ni valores crudos.
7. Ejecutar unit/integration/concurrency relevantes y actualizar G3.

**Archivos esperados**

- `modify`: controller, consumer interface/impl, metrics y tests.
- `create`: guard dedicado si mantiene el controller/service más cohesivos; no duplicar parser del resolver.
- `conditional`: query repository mínima para correlacionar ejecución si el grafo JPA actual causa N+1 o lazy failure.

**No tocar**

- State machine del handler después del guard, Flink, SDK, inactivation, producer, Actions, Materializer y untracked ajenos.

**Spikes permitidos**

- Inspección puntual de la correlación más segura. Si `deploymentId` no permite resolver una ejecución en el flow POC, `PLAN_CONFLICT`; no confiar sólo en runtime/filter.

**Tests y asserts**

- Valid alpha llama una vez al handler y conserva semántica actual.
- Null/missing/malformed/multiple scope tags, runtime mismatch y execution mismatch retornan 200, no llaman handler y emiten reason correcto.
- DB/transient failure tras guard válido conserva 5xx/retry.
- Ninguna métrica usa scope/ID dinámico como tag; ≥95% de cobertura nueva.

**Entregables/Gate G3**

- Diff, matriz de negativos, tests de zero-side-effect y evidencia de métricas. G3 queda `review`.

**Handoff a Fase 4**

- El siguiente agente recibe G3 `accepted`, build candidato y matriz local completa; sólo resta integración externa/rollout.

### Paquete autónomo Fase 4 — Certificación alpha y rollback

**Misión exacta**

Certificar el recorrido alpha real y el rollback sin ampliar código ni habilitar producción.

**Precondiciones verificables**

- G3 `accepted`.
- Fury Route, scopes, bindings y Flink alpha preparados según sus SPECs aprobadas.
- Release/candidate generado por el proceso autorizado; no desde una feature branch productiva.

**Lectura obligatoria**

- `VAULT_ROOT/10-projects/Meli/Estandarización de Scopes RIO/SPEC técnica — Routing KISS por scope en rio-playmaker.md`, rollout, DoD y dependencias.
- Evidencia G0–G3, SPEC frontend, SPEC Flink e infraestructura Fury aprobadas.

**Decisiones cerradas**

- Sólo alpha/nonprod; no crear topics ni habilitar prod.
- API y consumer flags se activan/desactivan como una unidad.
- Un negativo debe demostrar ausencia de side effects, no sólo un status HTTP.

**Implementación paso a paso**

1. Aplicar migrations y desplegar candidato con flag off; ejecutar smoke legacy.
2. Confirmar route/header, binding server-side y continuidad Flink con recursos sin tráfico de usuario.
3. Activar flag en API+consumer alpha.
4. Ejecutar golden deploy y capturar execution ID, filtros trigger/result y estado terminal.
5. Ejecutar missing header, beta→alpha, filtro ausente y filtro alterado; comprobar DB/handlers/metrics sin side effects.
6. Ejecutar rollback flag off y smoke legacy; pausar bindings alpha si el runbook lo requiere.
7. Enlazar evidencia, dejar G4 en `review` y no promover producción.

**Archivos esperados**

- `modify`: este planner, runbook/evidencia y configuración versionada sólo donde las SPECs externas lo autoricen.
- Código Playmaker: ninguno salvo fix de bug que reabra la fase responsable y su gate.

**No tocar**

- Producción, topics, payload SDK, eventos fuera de alcance, datos de usuario no descartables y untracked ajenos.

**Spikes permitidos**

- Ninguno. Cualquier fallo de contrato reabre F1/F2/F3 o marca `PLAN_CONFLICT`; no parchear durante E2E.

**Tests y asserts**

- Golden: header `alpha`, runtime API alpha, trigger/result `scope:alpha`, runtime consumer alpha, estado terminal visible.
- Cross-lane: valores beta/missing/alterados no mutan ejecución ni recursos.
- Rollback: flag off restaura smoke legacy sin rollback de schema.

**Entregables/Gate G4**

- Evidencia E2E, negativos, métricas, rollback y residual risks. G4 queda `review` para cierre de Rodrigo.

**Handoff a Fase 5**

- No existe Fase 5 en este proyecto. Con G4 aceptado, el parent decide si promover la POC o diseñar otra lane en un proyecto separado.

## ✅ Tareas

- [ ] **T0.1** Revisar SPEC/planner | archivos: planner+SPEC | precondición: ninguna | implementación: auditar KISS/DDs | tests: checklist de no-alcance | evidencia: review independiente #owner/agent #type/pr-review #area/meli
- [ ] **T0.2** Revalidar baseline | símbolos citados | precondición: GlobalProtect | implementación: fetch+diff sin tocar worktree | tests: refs resuelven | evidencia: SHA/tag #owner/agent #type/research #area/meli
- [ ] **T0.3** Verificar Fury/Flink | contratos externos | precondición: accesos read-only | implementación: probar route/filter/continuidad | tests: server-side/no-crossing | evidencia: links o G0 blocked #owner/agent #type/research #area/meli
- [ ] **T1.1** Crear resolver/flag | config+resolver | precondición: G0 accepted | implementación: header/runtime/error contract | tests: tabla de casos | evidencia: unit tests #owner/agent #type/dev #area/meli
- [ ] **T1.2** Persistir scope | model+lifecycle+migrations | precondición: T1.1 | implementación: nullable/inmutable | tests: tst/stg/prod + integration | evidencia: schema/model #owner/agent #type/dev #area/meli
- [ ] **T1.3** Aislar idempotencia/lecturas | repository+deploy/history/logs | precondición: T1.2 | implementación: queries scope-aware | tests: alpha/beta same hash + read isolation | evidencia: integration tests #owner/agent #type/dev #area/meli
- [ ] **T2.1** Propagar carrier | DispatchRequest+factory | precondición: G1 accepted | implementación: scope persistido through async | tests: factory/record/AFTER_COMMIT | evidencia: unit/integration #owner/agent #type/dev #area/meli
- [ ] **T2.2** Publicar filtrado | adapter+port+producer | precondición: T2.1 | implementación: mqclient Filters | tests: scoped vs legacy overload | evidencia: envelope fixture #owner/agent #type/dev #area/meli
- [ ] **T2.3** Filtrar retries | DeploymentTimeoutJob | precondición: T2.2 | implementación: scope desde execution | tests: retry alpha/missing/publish failure | evidencia: unit+IT #owner/agent #type/dev #area/meli
- [ ] **T3.1** Conservar/parsear envelope | controller+consumer | precondición: G2 accepted | implementación: exactamente un scope tag | tests: malformed matrix | evidencia: controller tests #owner/agent #type/dev #area/meli
- [ ] **T3.2** Triple guard | guard+repository | precondición: T3.1 | implementación: filtro==runtime==execution | tests: zero-side-effect | evidencia: integration tests #owner/agent #type/dev #area/meli
- [ ] **T3.3** Observabilidad bounded | metrics+logs | precondición: T3.2 | implementación: reason catalog | tests: tags bounded/no raw | evidencia: metric tests #owner/agent #type/dev #area/meli
- [ ] **T4.1** Desplegar flag off | release/config/migrations | precondición: G3 accepted | implementación: candidate nonprod | tests: smoke legacy | evidencia: deploy #owner/agent #type/dev #area/meli
- [ ] **T4.2** Golden y negativos alpha | E2E | precondición: Fury/Flink listos | implementación: ejecutar matriz | tests: terminal + zero-side-effect | evidencia: IDs/logs/metrics redactados #owner/agent #type/dev #area/meli
- [ ] **T4.3** Rollback y cierre | config+planner | precondición: T4.2 | implementación: flag off/smoke | tests: rollback | evidencia: G4 review #owner/agent #type/dev #area/meli

## Prompt común del executor/reviewer

Trabaja únicamente la fase indicada de [[POC KISS — Routing de scopes en Playmaker]]. Lee el paquete canónico y la SPEC técnica completos antes de actuar. Prioriza código/tests del SHA aceptado sobre notas históricas. Conserva cambios y untracked ajenos. Aplica KISS/YAGNI: no agregues campos a `rio-sdk-events`, no cambies DTOs/schema version/topics, no migres el producer, no extiendas a otros eventos y no construyas abstracciones para lanes futuras. Escribe primero los tests críticos, apunta a ≥95% de cobertura sobre código nuevo y ejecuta los checks relevantes. Si la evidencia contradice una decisión, si falta una precondición o si necesitas tocar `No tocar`, detente, registra `PLAN_CONFLICT` con file/symbol/evidencia y deja el gate `blocked`; no improvises. Actualiza tareas, Bitácora y el gate de tu fase. Puedes dejarlo `review`, `blocked` o `rejected`, nunca `accepted`, y está prohibido comenzar la siguiente fase.

**Despacho Fase 0**

```text
FASE_ASIGNADA=0
PAQUETE_CANONICO=Paquete autónomo Fase 0 — Revisión independiente POC KISS
GATE_REQUERIDO=none
TAREAS=T0.1-T0.3
SALIDA=review KISS + baseline fresco + evidencia Fury/Flink + G0 review/blocked
STOP=detener al dejar G0 review/blocked/rejected; prohibido escribir código o iniciar F1
```

**Despacho Fase 1**

```text
FASE_ASIGNADA=1
PAQUETE_CANONICO=Paquete autónomo Fase 1 — Ingreso, persistencia e aislamiento de lecturas
GATE_REQUERIDO=G0 accepted
TAREAS=T1.1-T1.3
SALIDA=resolver+schema+persistencia+queries+tests+G1 review
STOP=detener al dejar G1 review/blocked/rejected; prohibido iniciar publicación F2
```

**Despacho Fase 2**

```text
FASE_ASIGNADA=2
PAQUETE_CANONICO=Paquete autónomo Fase 2 — Publicación filtrada y retries
GATE_REQUERIDO=G1 accepted
TAREAS=T2.1-T2.3
SALIDA=carrier+publish first/next/retry+tests+G2 review
STOP=detener al dejar G2 review/blocked/rejected; prohibido iniciar consumer F3
```

**Despacho Fase 3**

```text
FASE_ASIGNADA=3
PAQUETE_CANONICO=Paquete autónomo Fase 3 — Guard de resultados antes de side effects
GATE_REQUERIDO=G2 accepted
TAREAS=T3.1-T3.3
SALIDA=envelope guard+triple match+metrics+zero-side-effect tests+G3 review
STOP=detener al dejar G3 review/blocked/rejected; prohibido iniciar rollout F4
```

**Despacho Fase 4**

```text
FASE_ASIGNADA=4
PAQUETE_CANONICO=Paquete autónomo Fase 4 — Certificación alpha y rollback
GATE_REQUERIDO=G3 accepted
TAREAS=T4.1-T4.3
SALIDA=golden deploy+negativos+rollback+evidencia+G4 review
STOP=detener al dejar G4 review/blocked/rejected; prohibido promover producción o abrir una fase nueva
```

## 🧱 Entrega de desarrollo

| Aplicación / repo | Branch | Base | SPEC funcional | SPEC técnica | Estado |
|---|---|---|---|---|---|
| `rio-playmaker` | `feature/sig-599-playmaker-scope-routing-poc` — crear tras G0 | `origin/master@f350fb26091d` local; revalidar en F0 | [SIG-599](https://spellbook.adminml.com/projects/SIG/specs/SIG-599) / [[scope-naming-standard]] | [[SPEC técnica — Routing KISS por scope en rio-playmaker]] | planner `ready_for_phase_0`; código no iniciado |

## 📆 Bitácora

- **2026-09-16** — Planner y SPEC técnica creados desde evidencia de `rio-playmaker`, `rio-sdk-events` y mqclient. Se elimina la fase SDK de la POC: `environment_scope` se persiste en Playmaker y viaja como filtro del envelope, no como campo duplicado en DTO. La primera fase es una revisión independiente KISS y revalidación de capabilities; ninguna implementación fue iniciada.

## 🧭 Decisiones

- El registro canónico de decisiones ejecutables está en [[#Registro de decisiones]].
- Cualquier propuesta que agregue SDK DTO, topic, producer migration u otro evento se rechaza como scope creep salvo nueva decisión explícita de Rodrigo.

## 🔗 Docs / Links

- Funcional: [SIG-599](https://spellbook.adminml.com/projects/SIG/specs/SIG-599) · [[scope-naming-standard]]
- Técnica: [[SPEC técnica — Routing KISS por scope en rio-playmaker]]
- Parent: [[Estandarización de Scopes RIO]]
- Front: [[SPEC técnica — Routing dinámico de backend en ads-signals-frontend]]

## 💡 Ideas

- Extender el patrón a otras lanes/eventos sólo después de aceptar G4 y en un proyecto separado; no convertirlo en requisito de esta POC.
