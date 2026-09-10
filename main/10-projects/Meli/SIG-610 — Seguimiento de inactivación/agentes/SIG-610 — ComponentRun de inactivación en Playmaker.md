---
type: project
schema_version: 1
owner: agent
root: false
status: review
priority: P1
area: "[[Meli]]"
parent: "[[SIG-610 — Seguimiento de inactivación]]"
sprint:
start: 2026-09-08
due: 2026-09-10
progress: 99
repo: https://github.com/melisource/fury_rio-playmaker
jira: SIG-610
prs: https://github.com/melisource/fury_rio-playmaker/pull/1144
aliases:
  - SIG-610 ComponentRun Playmaker
  - Inactivate ComponentRun
  - Undeploy execution tracking backend
tags:
  - kind/project
  - area/meli
  - application/rio-playmaker
  - ticket/sig-610
created: 2026-09-08
updated: 2026-09-10
---

# SIG-610 — ComponentRun de inactivación en Playmaker

> [!info]+ Proyecto delegado
> **Área:** [[Meli]] · **Estado:** review · **Prioridad:** P1 · **Parent:** [[SIG-610 — Seguimiento de inactivación]] · **Repo único:** [[rio-playmaker]]

## 🎯 Objetivo

Hacer que cada inactivación explícita aceptada por Playmaker cree exactamente un `ComponentRun` asociado a su `PipelineExecution` `INACTIVATE`, y mantener ambos estados consistentes desde `PENDING` hasta `RUNNING` y un resultado terminal. El history existente debe poder devolver ese run sin cambios de contrato. Un run de inactivación no debe alterar el cálculo ni el retry de un deploy posterior.

El cambio es deliberadamente backend-only y pequeño: no mezcla los flujos `DEPLOY` e `INACTIVATE`, no crea una segunda ejecución, no invoca la orquestación por batches y no publica más de un comando `DEPROVISION`.

## 📊 Estado actual

- **Estado del plan:** `ready_for_owner_review`; la validación runtime cerró correctamente con el mismo artefacto en los scopes web y consumer. El PR #1144 está abierto, con CI, coverage, dependencias, análisis estático y workflow verdes, pendiente de aceptación humana.
- **Código:** rama `feature/sig-610-inactivate-component-run` publicada en `1c2601f96`; el fallback especulativo de “usar el único run” fue revertido y la correlación vuelve a ser estricta por `executionId + componentId`. History productivo no se modifica.
- **Versión de prueba actual:** [`0.0.7-test-sig-610-dev-0`](https://web.furycloud.io/rio-playmaker/versions/detail/0.0.7-test-sig-610-dev-0) terminó `FINISHED` desde `feature/sig-610-inactivate-component-run`; el tag remoto apunta exactamente a `1c2601f96d582fa5058b5f84c41395e10113d412`.
- **Base de trabajo:** `feature/sig-610-inactivate-component-run`, creada desde `develop` sincronizado con `origin/develop` en `2f7f572a9545feb1a4f5742dfc38ef963847e2d3`.
- **Superficie verificada:** Fase 2 añadió sólo el filtro positivo por `DEPLOY` en `ComponentRunRepository` y sus callers, la eliminación de la consulta muerta y las pruebas correspondientes; history, contratos, schema, frontend, SDK y control planes siguen sin cambios.
- **Working tree actual:** sin cambios tracked; `graphify-out/` y `scripts/inactivate-probe/` permanecen untracked y fuera de los commits. El repo conserva la colisión conocida entre `CLAUDE.md` y `Claude.md` en filesystems case-insensitive.
- **Problema resuelto:** `ComponentInactivationServiceImpl.dispatch` resuelve service y `componentDefinition` antes del lifecycle, rechaza configuración no resoluble con `422 INVALID_COMPONENT_STATUS` y entrega exactamente un `DeltaEntry(UNDEPLOY)`.
- **Resultado actual:** `PipelineHistoryServiceImpl.getExecution` conserva su query y mapeo; una prueba con ejecución `INACTIVATE` confirma que expone automáticamente el run persistido.
- **Gap de consistencia resuelto:** `InactivationResultHandlerImpl` bloquea la `PipelineExecution` con `PESSIMISTIC_WRITE` antes de los guards y actualiza execution/run/component/service en la misma transacción; resultados simultáneos del mismo executionId se serializan y el segundo terminal queda como no-op.
- **Exposición de error resuelta:** el handler no registra ni persiste el payload crudo del CP; conserva sólo un code con allowlist y máximo de 100 caracteres más un mensaje genérico propio, omitiendo el message/details upstream.
- **Acoplamiento resuelto:** `DeltaComputationServiceImpl` y el guard de delete consultan runs sólo con `PipelineExecutionType.DEPLOY`; un `INACTIVATE` no contamina retries ni bloquea por sí solo el delete. `findFirstByComponentIdOrderByIdDesc` y su Javadoc obsoleto fueron eliminados.
- **Ausencia de reaper para `INACTIVATE`:** el handler terminaliza run y ejecución cuando llega el resultado del control plane. Si el control plane nunca responde, `DeploymentTimeoutJob` no alcanza esta ejecución porque recorre exclusivamente filas de `DeploymentModel`; el lock de data product se recupera por TTL, pero el run queda no terminal. No se agrega un reaper en esta entrega.
- **Delete durante undeploy:** el guard de runs filtra por `DEPLOY`, pero `PipelineComponentDeleteServiceImpl` todavía bloquea por infraestructura activa mientras el service no sea terminal. La cobertura confirma ambas condiciones.
- **Fuente de configuración resuelta:** el `configId` del run y los parámetros del `DEPROVISION` usan la misma `ServiceModel.componentDefinition`, sin cambiar la semántica del comando existente.
- **Validación runtime cerrada:** `test3` publica el comando de inactivación y `bq-consumer-test-nonprod` procesa `rio-deployment-result`; ambos ejecutaron `0.0.6-test-sig-610-dev-0`. Para una ejecución nueva, el consumer recibió `STARTED` y `COMPLETED`, resolvió `componentId=8962` y `runId=3298` por lookup exacto y llevó execution/run `PENDING → RUNNING → COMPLETED`, sin fallback. Esto confirma que el síntoma previo provenía del desfase de artefactos entre scopes.

## 🧱 Entrega de desarrollo

| Aplicación / repo | Branch | Base | SPEC funcional | SPEC técnica | Estado |
|---|---|---|---|---|---|
| [[rio-playmaker]] | `feature/sig-610-inactivate-component-run` | `develop` sincronizado con `origin/develop`, `2f7f572a9545feb1a4f5742dfc38ef963847e2d3` | [SIG-610 — Undeployment Functional Specification](https://spellbook.adminml.com/projects/SIG/specs/SIG-610) | [SIG-614 — ComponentRun de inactivación en Playmaker](https://spellbook.adminml.com/projects/SIG/specs/SIG-614) y este plan | `phase_2_g2_review`; HEAD `1c2601f96` |

> [!warning]+ Gate de repositorio — sincronización y creación de rama
> Antes de tocar código, en este orden exacto:
>
> 1. Situarse en `develop` y sincronizarlo con el remoto: `git checkout develop`, `git fetch origin`, `git pull --ff-only origin develop`. Si el pull no puede resolverse fast-forward, detenerse con `PLAN_CONFLICT`; no rebasar ni mergear a ciegas.
> 2. Verificar el working tree. Sólo `graphify-out/` untracked es esperado. `Claude.md` o `CLAUDE.md` marcado como modificado es la colisión de mayúsculas descrita en Estado actual, no un cambio real: neutralizarla con `git update-index --skip-worktree Claude.md` y continuar, sin commitear ese archivo ni revertir la marca. Cualquier otro archivo modificado o borrado detiene el trabajo con `PLAN_CONFLICT`; nunca limpiar ni sobrescribir trabajo del usuario.
> 3. Crear `feature/sig-610-inactivate-component-run` desde ese `develop` sincronizado y registrar el SHA resultante en la Bitácora.
> 4. Leer `REPO_ROOT/AGENTS.md` y las reglas Java que éste enrute.
>
> Nunca crear la rama desde una `release/*` ni desde un SHA congelado en este documento.

## Resumen ejecutivo y trabajo restante

0. Sincronizar `develop`, verificar el baseline y crear la rama de implementación.
1. Resolver `ServiceModel.componentDefinition` para el componente en el ambiente objetivo y reutilizarla en el run y el comando existente.
2. Construir un único `DeltaEntry` `UNDEPLOY` y pasarlo al lifecycle existente, que persistirá el `ComponentRun` `PENDING` en la misma transacción que la ejecución.
3. Extender el handler de resultados de inactivación para actualizar run y ejecución de manera atómica en `STARTED`, `IN_PROGRESS`, `COMPLETED` y `FAILED`.
4. Filtrar por `DEPLOY` las dos consultas activas que no deben consumir runs `INACTIVATE` y eliminar `findFirstByComponentIdOrderByIdDesc`.
5. Probar invariantes, regresiones y cobertura de las clases modificadas; no tocar history, frontend, SDK, CPs ni schema.

## Matriz requerimiento → evidencia

| ID | Requerimiento | Estado | Evidencia actual | Trabajo requerido |
|---|---|---|---|---|
| R1 | Inactivate es un flujo separado de deploy | `done` | `HEAD` — `ComponentInactivationServiceImpl.inactivate/dispatch`; `PipelineDeployServiceImpl.deploy` | No modificar |
| R2 | Una inactivación aceptada crea una ejecución `INACTIVATE` | `done` | `HEAD` — `ComponentInactivationServiceImpl.dispatch` | Conservar |
| R3 | La ejecución contiene exactamente un run del target | `done` | `ComponentInactivationServiceImpl.dispatch` entrega una lista con un `DeltaEntry(UNDEPLOY)` y el lifecycle existente persiste el run | Conservar |
| R4 | El run referencia una configuración única, resoluble y coherente con el comando efectivamente publicado | `done` | La misma `ServiceModel.componentDefinition` alimenta `DeltaEntry.configId` y `resolveDeprovisionParams`; test verifica config/params | Conservar |
| R5 | History devuelve el run | `done` | Test de `PipelineHistoryServiceImpl` con execution `INACTIVATE` y un run target; cero cambios productivos en history | Conservar |
| R6 | Estado activo observable | `done` | `InactivationResultHandlerImpl` mueve execution/run a `RUNNING` y asigna `ComponentRun.startedAt` una sola vez | Conservar |
| R7 | Estado terminal consistente | `done` | Handler mueve ambos a `COMPLETED`/`FAILED`, asigna `completedAt` al run y error seguro cuando corresponde | Conservar |
| R8 | Duplicados/out-of-order no regresan terminales | `done` | Lookup `PESSIMISTIC_WRITE` por executionId antes de los guards; test cubre un `FAILED` contradictorio posterior a `COMPLETED` sin saves ni side effects | Conservar |
| R9 | Inactivate no contamina el retry del deploy | `done` | `findLastRunsByComponentIds` filtra positivamente por `PipelineExecutionType.DEPLOY` dentro del max-id subquery; test JPA cubre INACTIVATE más reciente | Conservar |
| R12 | Un run de inactivación no bloquea de forma permanente el delete lógico del componente | `done` | `existsByComponentIdAndPipelineExecutionTypeAndStatusIn` recibe `DEPLOY`; test unitario/JPA cubre aislamiento y el guard posterior de infraestructura activa sigue vigente | Conservar |
| R13 | El contrato de `POST /inactivate` queda declarado cuando la configuración no es resoluble | `done` | Tests cubren service ausente y `componentDefinition` ausente antes de lifecycle, lock o publish, con `422 INVALID_COMPONENT_STATUS` | Conservar |
| R10 | No cambia el dispatch | `done` | `HEAD` — publicación única post-commit de `DEPROVISION` | Probar que continúa siendo una publicación |
| R11 | Relaciones/imports impiden inactivar | `done` | `HEAD` — `validateInactivation`, `guardActiveImports`, `findActiveByComponentId` | No modificar |

## Alcance

### Dentro

- Creación de un `ComponentRun` para cada nueva ejecución `INACTIVATE` aceptada.
- Uso de `ServiceModel.componentDefinition` como fuente única del `configId` y de los parámetros del comando existente.
- Estados y timestamps del run; estado `RUNNING` de la ejecución padre.
- Persistencia de error estructurado del run en `FAILED`, con fallback seguro si falla la serialización.
- Compatibilidad con ejecuciones antiguas sin run durante rollout.
- Filtro positivo por `PipelineExecutionType.DEPLOY` en `findLastRunsByComponentIds` y `existsByComponentIdAndStatusIn`.
- Conservación del guard de infraestructura activa del delete lógico.
- Eliminación de `findFirstByComponentIdOrderByIdDesc` y de su referencia Javadoc obsoleta.
- Tests unitarios, repository/integration cuando corresponda y suite/gate de cobertura.

### Fuera

- Frontend, BFF y polling.
- Cambiar los endpoints o DTOs de history.
- Crear un error HTTP nuevo para configuración no resoluble; se reutiliza el `422 INVALID_COMPONENT_STATUS` existente.
- Crear `Deployment`, `DeploymentGroup` o batches para el inactivate.
- Cambiar el evento `DeploymentTriggerMessage` o `rio-sdk-events`.
- Modificar control planes o su operación `DEPROVISION`.
- Cambiar el lock por data product, su respuesta `409` o su granularidad.
- Cambiar autorización del history.
- Incorporar `CANCELLED`, `updatedAt` o secuencias de eventos.
- Cambiar la semántica final del canvas (`INACTIVE`/`TERMINATED` versus `READY_TO_DEPLOY`).
- Cambiar la validación de relaciones activas, imports o infraestructura previa.
- Cambiar los parámetros o la fuente actual del `DEPROVISION`; cualquier expansión exige `PLAN_CONFLICT`.

## Registro de decisiones

| ID | status | resolution | source/evidence | phase consuming it |
|---|---|---|---|---|
| D1 | `CONFIRMED` | Deploy e inactivate son botones y ejecuciones separadas; este cambio no debe unirlos ni disparar dos flujos. | Confirmación del owner, 2026-09-08; `ComponentInactivationServiceImpl` | F0–F2 |
| D2 | `CONFIRMED` | El único resultado funcional de esta entrega es agregar seguimiento por `ComponentRun`, dejándolo siempre consistente y terminal. | Confirmación del owner, 2026-09-08 | F1 |
| D3 | `CONFIRMED` | No se puede inactivar mientras existan asociaciones activas; la validación existente queda intacta. | Confirmación del owner + `ComponentInactivationServiceImpl.validateInactivation` | F0–F2 |
| D5 | `TECHNICAL_RESOLUTION` | `STARTED` e `IN_PROGRESS` convergen a `RUNNING`; `startedAt` se asigna una vez. `COMPLETED/FAILED` son terminales y asignan `completedAt`. | Enums actuales + contrato SDK `DeploymentResultStatus` | F1 |
| D6 | `TECHNICAL_RESOLUTION` | Donde se filtre por tipo de ejecución, se filtra positivamente por `PipelineExecutionType.DEPLOY` en vez de excluir `INACTIVATE`; es fail-closed ante tipos futuros. | `DeltaComputationServiceImpl` y `PipelineExecutionType` | F2 |
| D7 | `TECHNICAL_RESOLUTION` | Las ejecuciones legacy sin run conservan el comportamiento actual del handler y generan warning; no fallan ni bloquean el rollout. | Compatibilidad rolling deploy | F1 |
| D8 | `TECHNICAL_RESOLUTION` | No hay migración: `component_run` y sus estados ya existen; la relación ejecución/componente ya tiene unique constraint. | `ComponentRunModel` + migrations existentes | F0–F2 |

| D9 | `CONFIRMED` | Filtrar `existsByComponentIdAndStatusIn` positivamente por `DEPLOY`; no agregar reaper. Mientras el undeploy corre, el guard posterior de infraestructura activa sigue bloqueando el delete. El filtro evita que un `INACTIVATE` viejo bloquee después de que el service ya está terminal. | Owner, 2026-09-09; `PipelineComponentDeleteServiceImpl`; `ComponentServiceImpl.findServicesActiveEnvironments` | F2 |
| D10 | `CONFIRMED` | Usar `ServiceModel.componentDefinition` como fuente única del `configId`, igual que los parámetros que hoy viajan en `DEPROVISION`; no cambiar el comando. | Owner, 2026-09-09; `resolveDeprovisionParams` | F1 |
| D11 | `TECHNICAL_RESOLUTION` | Componente inexistente conserva `404`. Service ausente ya deriva en `NOT_DEPLOYED` y `422 INVALID_COMPONENT_STATUS`; una `componentDefinition` no resoluble debe rechazarse antes del dispatch reutilizando el mismo `422`, no con `400` ni con un contrato nuevo. | Owner, 2026-09-09; `ComponentStatusService.resolveStatus`; `guardInfrastructureStatus`; `ControllerExceptionHandler` | F1 |
| D12 | `CONFIRMED` | Filtrar por `DEPLOY` exactamente `findLastRunsByComponentIds` y `existsByComponentIdAndStatusIn`. No filtrar las consultas de history/handler por `pipelineExecutionId`, porque deben encontrar runs `INACTIVATE`. | Owner, 2026-09-09; callers actuales de `ComponentRunRepository` | F2 |
| D13 | `CONFIRMED` | Eliminar `findFirstByComponentIdOrderByIdDesc` y su referencia Javadoc porque no tiene callers en `main` ni en `test`. | Owner, 2026-09-09; búsqueda de callers | F2 |

## Arquitectura actual y objetivo

### Actual

```text
POST inactivate
  -> valida estado/relaciones/imports
  -> crea PipelineExecution(INACTIVATE, PENDING) sin runs
  -> toma lock de data product
  -> publica un DEPROVISION después del commit
  -> result handler:
       STARTED/IN_PROGRESS: no-op
       COMPLETED/FAILED: actualiza sólo execution y dominio
  -> history: component_runs=[]
```

### Objetivo

```text
POST inactivate
  -> mismas validaciones
  -> resuelve Service + ServiceModel.componentDefinition
  -> crea PipelineExecution(INACTIVATE, PENDING)
       └── ComponentRun(target, serviceConfig, PENDING)
  -> mismo lock
  -> misma y única publicación DEPROVISION
  -> result handler transaccional:
       STARTED/IN_PROGRESS -> execution RUNNING + run RUNNING
       COMPLETED           -> execution/run COMPLETED + dominio actual
       FAILED              -> execution/run FAILED + error; dominio actual
  -> history existente devuelve exactamente ese run
```

No se llama `OrchestrationService`, no se crean `DeploymentGroup` y no se emite `BatchCompletedEvent` desde el handler de inactivación.

## Contratos de datos y actividad

### `configId`

`configId` es el PK de `ComponentDefinitionModel` que identifica la configuración que el run declara haber inactivado. `ComponentRunModel.componentDefinition` es una FK obligatoria, de modo que no puede crearse un run sin una definición resoluble.

La fuente cerrada en `D10` es la misma que usa hoy el comando:

```text
component + environment
  -> ServiceRepository.findByComponentIdAndEnvironmentId
     -> ServiceModel.componentDefinition
        ├── id         == DeltaEntry.configId
        └── parameters == DeploymentTriggerMessage.params
```

La invariante es que el `configId` del run y los parámetros que viajan en el `DEPROVISION` salen de la misma `ComponentDefinition`. No se consulta el deployment activo, no se usa la última definición global y no se inventa una FK.

Si el componente no existe, se conserva `404`. Si no existe el service, el flujo actual resuelve `NOT_DEPLOYED` y responde `422 INVALID_COMPONENT_STATUS`. Si existe el service pero no tiene `componentDefinition` resoluble, se debe extender o reutilizar el mismo guard para responder ese `422` antes de crear la ejecución, adquirir el lock o publicar el comando.

### Estado del run

| Evento CP | Estado previo permitido | Execution resultante | ComponentRun resultante | Timestamps/error |
|---|---|---|---|---|
| aceptación HTTP | — | `PENDING` | `PENDING` | sin timestamps |
| `STARTED` | `PENDING/RUNNING` | `RUNNING` | `RUNNING` | `startedAt` si estaba null |
| `IN_PROGRESS` | `PENDING/RUNNING` | `RUNNING` | `RUNNING` | `startedAt` si estaba null |
| `COMPLETED` | no terminal | `COMPLETED` | `COMPLETED` | `completedAt=now`, error null |
| `FAILED` | no terminal | `FAILED` | `FAILED` | `completedAt=now`, error serializado o null |
| cualquier evento luego de terminal | terminal | sin cambio | sin cambio | sin regresión |

La actualización del run, la ejecución, el componente/servicio y la programación de liberación del lock permanecen dentro de la transacción actual del handler. Un fallo de persistencia debe revertir el conjunto.

### Error

- Si `DeploymentErrorPayload` existe, serializarlo mediante el `ObjectMapper` inyectado usando el mismo criterio seguro de `DeploymentResultHandlerImpl`.
- Si la serialización falla, persistir un JSON fijo sin payload sensible, por ejemplo `{"error":"serialization_failed"}`, y loguear sólo IDs/código seguro.
- Si el payload es null, permitir `ComponentRun.error=null`.

## Secuencia, bordes e idempotencia

- El lifecycle se invoca antes del lock, como hoy. Si `tryAcquire` falla, la transacción revierte tanto execution como run.
- La publicación sigue ocurriendo sólo `afterCommit`, evitando que un resultado llegue antes de que execution y run sean visibles.
- La unique constraint `(pipeline_execution_id, component_id)` garantiza máximo un run del target por ejecución.
- Un `STARTED` duplicado no reemplaza `startedAt`.
- `IN_PROGRESS` recibido antes de `STARTED` igualmente establece `RUNNING`, porque no se debe dejar el tracker en `PENDING` ante evidencia de trabajo activo.
- Un resultado terminal duplicado o un evento activo tardío no modifica execution/run ni vuelve a liberar el lock.
- Para una ejecución legacy sin run, el handler conserva la actualización actual de execution/componente/service. Debe registrar el defecto sin lanzar una excepción.
- El history invoca resolución de timeouts de deployments, pero una ejecución `INACTIVATE` no tiene `DeploymentGroup/Deployment`; esa consulta queda vacía y `DeploymentTimeoutJob` tampoco alcanza el run. Si el control plane nunca responde, el run puede quedar no terminal aunque el lock se recupere por TTL. Esta entrega no agrega retry ni timeout; filtrar el guard de runs por `DEPLOY` evita que esa fila bloquee el delete cuando el service ya no tiene infraestructura activa.

## Mapa de archivos y símbolos

| Acción | Archivo | Símbolos/responsabilidad |
|---|---|---|
| `modify` | `REPO_ROOT/src/main/java/com/mercadolibre/rio/playmaker/service/impl/ComponentInactivationServiceImpl.java` | `dispatch`, resolución de `ServiceModel.componentDefinition`, guard `422` y `DeltaEntry` único |
| `modify` | `REPO_ROOT/src/main/java/com/mercadolibre/rio/playmaker/service/impl/InactivationResultHandlerImpl.java` | lookup y transiciones de `ComponentRun`, timestamps/error, compatibilidad legacy |
| `modify` | `REPO_ROOT/src/main/java/com/mercadolibre/rio/playmaker/repository/ComponentRunRepository.java` | filtrar por `DEPLOY` `findLastRunsByComponentIds` y `existsByComponentIdAndStatusIn`; eliminar `findFirstByComponentIdOrderByIdDesc` y su Javadoc |
| `modify` | `REPO_ROOT/src/main/java/com/mercadolibre/rio/playmaker/service/pipeline/impl/DeltaComputationServiceImpl.java` | consumir consulta filtrada |
| `modify` | `REPO_ROOT/src/main/java/com/mercadolibre/rio/playmaker/service/impl/PipelineComponentDeleteServiceImpl.java` | pasar/consumir `PipelineExecutionType.DEPLOY` en el guard de runs sin alterar el guard posterior de infraestructura activa |
| `modify` | `REPO_ROOT/src/test/java/com/mercadolibre/rio/playmaker/service/impl/PipelineComponentDeleteServiceImplTest.java` | cobertura: `INACTIVATE` no bloquea por run, `DEPLOY` activo sí y la infraestructura activa continúa bloqueando durante undeploy |
| `modify` | `REPO_ROOT/src/test/java/com/mercadolibre/rio/playmaker/service/impl/ComponentInactivationServiceImplTest.java` | captura/assert del `DeltaEntry`, config y publicación única |
| `modify` | `REPO_ROOT/src/test/java/com/mercadolibre/rio/playmaker/unit/service/InactivationResultHandlerImplTest.java` | matriz completa de estados/idempotencia/legacy/error |
| `modify` | `REPO_ROOT/src/test/java/com/mercadolibre/rio/playmaker/unit/service/DeltaComputationServiceImplTest.java` | filtro del último run |
| `create` condicional | `REPO_ROOT/src/test/java/com/mercadolibre/rio/playmaker/integration/ComponentRunRepositoryIntegrationTest.java` | demostrar la query filtrada si no existe fixture equivalente reutilizable |
| `no-touch` | `PipelineHistoryServiceImpl`, controllers/DTOs de history | ya devuelven cualquier run persistido |
| `no-touch` | `PipelineExecutionLifecycleServiceImpl`, `ComponentRunModel`, enums y migrations | ya soportan la fila y estados necesarios |
| `no-touch` | `CLAUDE.md` / `Claude.md` | colisión de mayúsculas en el índice; nunca commitear ni revertir su `skip-worktree` |
| `no-touch` | frontend, BFF, SDK y control planes | fuera del repo/scope |

## ✅ Tareas

> [!note]+ Contrato atómico
> Cada tarea incluye objetivo, archivos/símbolos, precondiciones, implementación, tests y evidencia esperada. El executor actualiza `[ ] → [/] → [r] → [x]` dentro de esta nota; sólo el owner acepta gates.

- [x] **T0.0 · Cerrar decisiones abiertas** — objetivo: obtener del owner la resolución de `D9`–`D13`; archivos: esta nota; precondición: ninguna; implementación: resoluciones registradas en Registro de decisiones y propagadas a Alcance, Contratos, fases y Definition of Done; tests: ninguno; evidencia: filas `D9`–`D13` cerradas el 2026-09-09 #owner/me #type/decision #area/meli
- [x] **T0.1 · Sincronizar base y congelar baseline** — objetivo: dejar `develop` local idéntico al remoto, crear la rama de trabajo desde ahí y verificar que la evidencia sigue vigente; archivos/símbolos: repo, `AGENTS.md`, las clases productivas y los tests del mapa; precondición: T0.0; implementación: ejecutar el Gate de repositorio completo —`checkout develop`, `fetch`, `pull --ff-only`, verificación de working tree, creación de la rama—, registrar el SHA resultante y comparar las firmas de los símbolos del mapa contra lo que este plan afirma; tests: ninguno; evidencia: rama `feature/sig-610-inactivate-component-run`, base `2f7f572a9545feb1a4f5742dfc38ef963847e2d3`, sólo `graphify-out/` untracked #owner/agent #type/dev #area/meli
- [x] **T0.2 · Especificar fixtures críticos primero** — objetivo: escribir/ajustar tests rojos que expresen run único, configuración del service, estados, `422` para definición ausente y aislamiento del deploy; archivos: tests listados; precondición: T0.1; implementación: fixtures mínimos, sin producción todavía; tests: ejecución focalizada compiló y falló como se esperaba: delta vacío, service ausente aceptado, `STARTED`/`IN_PROGRESS` sin transición a `RUNNING`; evidencia: cuatro fallos de contrato documentados en Bitácora; G0 aceptado por owner #owner/agent #type/dev #area/meli
- [x] **T1.1 · Crear el run de inactivación** — objetivo: entregar un `DeltaEntry` único al lifecycle; archivos: `ComponentInactivationServiceImpl` y test; precondición: G0 accepted; implementación: resolver `ServiceModel.componentDefinition`, rechazar su ausencia con el `422 INVALID_COMPONENT_STATUS` existente, construir `UNDEPLOY`, reutilizar la definición para config/params y conservar publicación; tests: run exacto, configId/params de la misma fuente, ausencia de filas inválidas, rollback de lock, una publicación; evidencia: `ComponentInactivationServiceImplTest` verde, 23 tests #owner/agent #type/dev #area/meli
- [x] **T1.2 · Mantener estados consistentes** — objetivo: actualizar execution + run en todos los resultados; archivos: `InactivationResultHandlerImpl` y test; precondición: T1.1; implementación: repository/object mapper, helpers de transición y error; tests: STARTED, IN_PROGRESS, COMPLETED, FAILED, duplicados, terminal tardío, legacy sin run, serialización fallida; evidencia: `InactivationResultHandlerImplTest` verde, 18 tests, con timestamps/asserts #owner/agent #type/dev #area/meli
- [x] **T1.3 · Probar visibilidad en history sin modificarlo** — objetivo: demostrar que el run persistido es consumible por el query actual; archivos: test de history existente; precondición: T1.1–T1.2; implementación: aserción con fixture `INACTIVATE` y run target; tests: detail contiene un run target y tipo `INACTIVATE`; evidencia: `PipelineHistoryServiceImplTest` verde, 10 tests y cero cambios productivos en history #owner/agent #type/dev #area/meli
- [x] **T2.1 · Aislar los runs de inactivación** — objetivo: que un run de inactivación no se lea como run de deploy ni bloquee el delete después de que la infraestructura ya está terminal; archivos: repository, delta service, servicio de delete y tests; precondición: G1 accepted; implementación: filtrar positivamente por `DEPLOY` `findLastRunsByComponentIds` y `existsByComponentIdAndPipelineExecutionTypeAndStatusIn`, conservar el guard de infraestructura activa y eliminar `findFirstByComponentIdOrderByIdDesc` más su Javadoc; tests: último `INACTIVATE FAILED` ignorado por delta, último `DEPLOY FAILED` conservado, combinación elige último deploy, run `INACTIVATE` no bloquea por sí solo, infraestructura activa y run `DEPLOY` sí bloquean; evidencia: tests unitarios y 2 tests JPA verdes #owner/agent #type/dev #area/meli
- [x] **T2.2 · Regresión y cobertura** — objetivo: validar el conjunto; archivos: sólo tests/ajustes estrictamente derivados; precondición: T2.1; implementación: ejecutar suites focalizadas y suite completa; tests: funcionalidad crítica primero, luego cobertura reportada; evidencia: `./gradlew clean test jacocoTestReport` verde, 3.650 tests, 2 skipped, 0 failures/errors; Melicov remoto reportó 100,00% de PR coverage #owner/agent #type/dev #area/meli
- [x] **T2.3 · Entrega y cierre técnico** — objetivo: dejar diff revisable y proyecto honesto; archivos: esta nota y repo; precondición: T2.2; implementación: revisar diff/stat/status, confirmar no-touch, actualizar progreso/bitácora y mover G2 a review; tests: no adicionales; evidencia: `git diff --check` verde, contracts/history/schema/frontend/SDK/CPs sin cambios, `graphify-out/` preservado #owner/agent #type/admin #area/meli
- [x] **T2.4 · Exponer tipo canónico al iniciar inactivate** — objetivo: hacer que el `202 Accepted` entregue `type: INACTIVATE` junto al `execution_id` para que el frontend pueda rastrear y renderizar la inactivación sin inferirla; archivos: `InactivateComponentResponseDTO`, `ComponentInactivationServiceImpl` y sus tests; precondición: corrección explícitamente solicitada por el owner tras G2; implementación: agregar el campo público `type`, poblarlo desde la ejecución creada y verificarlo en las pruebas de servicio/controlador; tests: 25 pruebas focalizadas verdes y `git diff --check`; evidencia: commit `423cb38d5` publicado y versión Fury de prueba `0.0.2-test-sig-610-dev-0` pendiente #owner/agent #type/dev #area/meli
- [x] **T2.5 · Revertir fallback especulativo** — objetivo: impedir que una correlación rota actualice un run arbitrario; archivos: `InactivationResultHandlerImpl` y pruebas; precondición: revisión crítica del workaround `20b16fe91`; implementación: eliminar la selección del único run y conservar exclusivamente el lookup por `executionId + componentId`; tests: suites focalizadas y `./gradlew check` verdes; evidencia: revert `67d0b1430` publicado en la rama original #owner/agent #type/dev #area/meli
- [x] **T2.6 · Validar ruta runtime del resultado** — objetivo: observar la ruta real de `DEPROVISION` de punta a punta; archivos: rama diagnóstica y probe; precondición: desplegar un mismo artefacto en web y consumer; implementación: trazas de envelope, routing, correlación y transiciones; tests: el consumer recibió `STARTED → COMPLETED`, encontró el run exacto y dejó execution/run `COMPLETED`; evidencia: `0.0.6-test-sig-610-dev-0` desplegada en `test3` y `bq-consumer-test-nonprod` #owner/agent #type/dev #area/meli
- [x] **T2.7 · Resolver findings del PR** — objetivo: cerrar la carrera entre resultados y evitar persistencia/exposición del error crudo del CP; archivos: `PipelineExecutionRepository`, `InactivationResultHandlerImpl` y tests; implementación: lock pesimista por executionId, guards posteriores al lock y error seguro; tests: suites focalizadas más `./gradlew test` verde, 2 skipped; evidencia: `6c0acae0c` publicado y ambos comentarios respondidos #owner/agent #type/dev #area/meli
- [x] **T2.8 · Recuperar coverage del PR** — objetivo: superar el piso interno de 95% bajo la semántica estricta de Melicov; archivos: `InactivationResultHandlerImpl` y tests de handler/servicio; implementación: cubrir ramas legacy, datos inconsistentes, liberación de lock y sanitización, y reemplazar switches exhaustivos que JaCoCo marcaba parciales por decisiones equivalentes comprobables; tests: suite completa verde; evidencia: commit `1c2601f96`, PR coverage remoto 100,00%, minimum coverage 94,66% y todos los checks verdes #owner/agent #type/dev #area/meli

## Roadmap y gates

| Gate | current state | phase agent responsibility | owner acceptance evidence | enables |
|---|---|---|---|---|
| G0 | accepted | Sincronizar `develop`, crear la rama y entregar tests críticos rojos para las decisiones ya cerradas | Owner aceptó el 2026-09-09: rama desde `develop`, tests rojos y alcance verificados | F1 |
| G1 | accepted | Crear run y completar su state machine con compatibilidad | Owner aceptó el 2026-09-09; tests focalizados verdes, history ve un run y existe exactamente un publish | F2 |
| G2 | review | Aislar los runs de inactivación con los dos filtros `DEPLOY`, eliminar la consulta muerta y entregar estado consistente de execution/run | Runtime E2E verde con scopes alineados; fallback especulativo revertido; findings corregidos; HEAD `1c2601f96`, PR coverage 100,00% y todos los checks verdes | Aceptación humana y posterior archivo |

El executor sólo puede dejar el gate de su fase en `review`. El owner lo cambia a `accepted`; no comenzar la siguiente fase antes de eso.

## Paquetes autónomos

### Paquete autónomo Fase 0 — Baseline y tests ejecutables

**Misión exacta**

Congelar la base real y convertir las decisiones cerradas en tests rojos, sin modificar producción.

**Precondiciones verificables**

- `D9`–`D13` cerradas por el owner en Registro de decisiones.
- Repo disponible y `origin/develop` alcanzable.
- Leer `VAULT_ROOT/10-projects/Meli/SIG-610 — Seguimiento de inactivación/agentes/SIG-610 — ComponentRun de inactivación en Playmaker.md`, secciones Estado, Decisiones, Contratos y Tareas.
- Ningún gate previo; `G0=pending`.

**Lectura obligatoria**

- `REPO_ROOT/AGENTS.md` y reglas Java enrutadas.
- `ComponentInactivationServiceImpl.dispatch/resolveDeprovisionParams`.
- `InactivationResultHandlerImpl.handle/applySuccess/applyFailure`.
- `ComponentRunRepository.findLastRunsByComponentIds` y `DeltaComputationServiceImpl.evaluateComponent`.
- Tests existentes nombrados en el mapa.
- `VAULT_ROOT/30-resources/applications/rio-playmaker.md` sólo como contexto de aplicación.

**Decisiones cerradas**

- D1–D3, D5, D7, D8. No reabrir la separación de flujos, la state machine ni la ausencia de migración.
- D9–D13 cerradas el 2026-09-09: fuente del service, `422` existente, dos filtros positivos por `DEPLOY`, sin reaper y eliminación de la consulta muerta.

**Implementación paso a paso**

1. Ejecutar el Gate de repositorio: `git checkout develop`, `git fetch origin`, `git pull --ff-only origin develop`. Si el pull no es fast-forward, detenerse con `PLAN_CONFLICT`.
2. Confirmar que sólo `graphify-out/` está untracked. `Claude.md`/`CLAUDE.md` en estado modificado es la colisión de mayúsculas conocida: neutralizar con `git update-index --skip-worktree Claude.md`. Preservar cualquier otro cambio y detener con `PLAN_CONFLICT` si solapa.
3. Crear `feature/sig-610-inactivate-component-run` desde ese `develop`, cambiar T0.1 a `[/]`, registrar rama y SHA en Bitácora y luego `[x]`.
4. Agregar primero tests críticos que fallen por los gaps reales: lifecycle recibe delta vacío; handler no toca run; query mezcla tipos.
5. Ejecutar sólo esas clases; documentar los fallos esperados, no snapshots enormes.
6. Dejar T0.2 y `G0` en `[r]/review`; detener.

**Archivos esperados**

- `modify`: los tres tests unitarios del mapa.
- `create` condicional: test repository si la semántica JPQL no queda demostrable con tests existentes.
- `modify`: esta nota sólo para estado/bitácora.

**No tocar**

- Producción, history, frontend, SDK, control planes, schema/migrations.

**Spikes permitidos**

- Sólo verificar si ya existe una base de integration test reutilizable para `ComponentRunRepository`. Máximo: localizar fixture y decidir reutilizar/crear; no rediseñar persistencia.

**Tests y asserts**

- El inactivate debe pasar una lista de tamaño 1, action `UNDEPLOY`, target correcto y config de `ServiceModel.componentDefinition`.
- Un service sin `componentDefinition` debe fallar con `422 INVALID_COMPONENT_STATUS` antes de crear execution/run o publicar.
- `STARTED/IN_PROGRESS` deben fallar hoy porque execution/run siguen `PENDING`.
- `COMPLETED/FAILED` deben fallar hoy porque run no cambia.
- El filtro debe demostrar contaminación actual con `INACTIVATE FAILED`.

**Entregables/Gate G0**

- Baseline registrado, tests críticos rojos por la causa esperada y ningún cambio productivo. `G0=review`.

**Handoff a Fase 1**

- Entregar branch/base, diff de tests, comandos exactos y lista de fallos. El siguiente executor no redescubre contratos ni amplía scope.

### Paquete autónomo Fase 1 — Creación y state machine del run

**Misión exacta**

Crear exactamente un run por inactivación y actualizarlo atómicamente hasta terminal, manteniendo el dispatch actual.

**Precondiciones verificables**

- `G0=accepted` por el owner.
- Tests críticos de F0 presentes y fallando por causas documentadas.
- Leer `VAULT_ROOT/10-projects/Meli/SIG-610 — Seguimiento de inactivación/agentes/SIG-610 — ComponentRun de inactivación en Playmaker.md`, especialmente D5, D7, D10, D11 y la tabla de estados.

**Lectura obligatoria**

- `ComponentInactivationServiceImpl`, `PipelineExecutionLifecycleServiceImpl.saveComponentRun`, `DeltaEntry`, `ServiceRepository.findByComponentIdAndEnvironmentId`.
- `InactivationResultHandlerImpl`, `ComponentRunModel`, `ComponentRunRepository.findByPipelineExecutionIdAndComponentId`.
- `DeploymentResultHandlerImpl.routeByStatus/serializeError` como patrón, sin copiar su orquestación.
- Tests de F0.
- `VAULT_ROOT/10-projects/Meli/Presentación deployments en RIO/Deployments en RIO — flujo completo.md`, sección `ComponentRun versus Deployment`.

**Decisiones cerradas**

- Un run, state machine de D5, compatibilidad legacy y cero batches/segundo publish. `ServiceModel.componentDefinition` es la fuente única y su ausencia se rechaza con el `422 INVALID_COMPONENT_STATUS` existente.

**Implementación paso a paso**

1. Marcar T1.1 `[/]`.
2. Resolver `ServiceModel.componentDefinition` antes de llamar al lifecycle; si falta, reutilizar el guard/error `422 INVALID_COMPONENT_STATUS` y no crear execution/run ni publicar.
3. Construir `DeltaEntry(componentId, UNDEPLOY, serviceDefinitionId, serviceId, componentType)` y pasar `List.of(entry)`; reutilizar la misma definición al resolver los params actuales del `DEPROVISION`.
4. Conservar la correlación executionId, lock, publish-after-commit y payload existentes.
5. Hacer verdes los tests de creación, error de integridad y publicación única; cerrar T1.1.
6. Marcar T1.2 `[/]`; inyectar `ComponentRunRepository` y `ObjectMapper` en el handler.
7. Resolver el run por executionId + target; actualizar active/terminal según tabla sin regresiones.
8. Persistir error seguro en failed; mantener comportamiento legacy cuando falta run.
9. Probar rollback/idempotencia/liberación de lock; cerrar T1.2.
10. Demostrar que history devuelve el run sin cambiar producción en history; cerrar T1.3.
11. Dejar `G1=review`; detener.

**Archivos esperados**

- `modify`: `ComponentInactivationServiceImpl`, `InactivationResultHandlerImpl` y sus tests.
- `modify` condicional sólo test: history/lifecycle test para visibilidad.
- `modify`: esta nota.

**No tocar**

- Orchestration, `DeploymentGroup`, `BatchCompletedEvent`, history productivo, API/DTO, frontend, SDK, CPs, relaciones y authorization.

**Spikes permitidos**

- Ninguno. Si `ServiceModel.componentDefinition` no puede obtenerse con repositorios existentes o no puede reutilizarse el `422 INVALID_COMPONENT_STATUS`, `PLAN_CONFLICT`; no introducir fallback global ni un contrato HTTP nuevo.

**Tests y asserts**

- Exactamente un delta/run y un publish.
- El `configId` del run y los parámetros publicados en el `DEPROVISION` salen de la misma `ComponentDefinition`.
- Service sin `componentDefinition` responde `422 INVALID_COMPONENT_STATUS`, cubierto por test.
- Fallo de lock revierte execution/run; no publish.
- STARTED e IN_PROGRESS llevan padre/run a RUNNING; `startedAt` no cambia en duplicado.
- COMPLETED/FAILED llevan ambos a terminal; completedAt presente; error seguro.
- Evento posterior a terminal es no-op y no libera lock otra vez.
- Ejecución legacy sin run no rompe el comportamiento previo.
- History detail entrega tipo INACTIVATE y un run target.

**Entregables/Gate G1**

- Tests focalizados verdes, diff acotado, estado/bitácora actualizados y `G1=review`.

**Handoff a Fase 2**

- Entregar SHAs/diff, suites focalizadas y cualquier riesgo observado. F2 no vuelve a diseñar creación/state machine.

### Paquete autónomo Fase 2 — Aislamiento del deploy y certificación

**Misión exacta**

Evitar que un run `INACTIVATE` se lea como run de deploy o bloquee por sí solo el delete cuando la infraestructura ya está terminal, y certificar la entrega completa.

**Precondiciones verificables**

- `G1=accepted` por el owner.
- Creación y transiciones del run verdes.
- Leer `VAULT_ROOT/10-projects/Meli/SIG-610 — Seguimiento de inactivación/agentes/SIG-610 — ComponentRun de inactivación en Playmaker.md`, D6, D9, D12, D13, riesgos y Definition of Done.

**Lectura obligatoria**

- `ComponentRunRepository.findLastRunsByComponentIds`, `existsByComponentIdAndStatusIn` y el método muerto `findFirstByComponentIdOrderByIdDesc` que se debe eliminar.
- `DeltaComputationServiceImpl.computeDelta/evaluateComponent`.
- `PipelineComponentDeleteServiceImpl`, BR-1 paso 4.
- `DeploymentTimeoutJob`, para confirmar que no alcanza ejecuciones `INACTIVATE`.
- Tests unitarios/integration de repositories y delta.
- Reglas de build/test desde `REPO_ROOT/AGENTS.md`.
- `VAULT_ROOT/30-resources/rio-atlas/architecture/playmaker-deploy-flow.md` para confirmar que esta query sólo decide delta de deploy.

**Decisiones cerradas**

- Filtrar positivamente por `PipelineExecutionType.DEPLOY` `findLastRunsByComponentIds` y `existsByComponentIdAndStatusIn`; no hardcodear una exclusión que acepte tipos futuros. Conservar el guard posterior de infraestructura activa y eliminar `findFirstByComponentIdOrderByIdDesc` con su Javadoc.

**Implementación paso a paso**

1. Marcar T2.1 `[/]`.
2. Reemplazar/ampliar la query para obtener el último run por componente sólo dentro de executions `DEPLOY`; el `MAX(id)` y el filtro deben vivir en la misma selección.
3. Actualizar el caller y probar orden mixto: INACTIVATE fallido más reciente no reemplaza el último DEPLOY; DEPLOY fallido sí conserva retry.
3b. Filtrar `existsByComponentIdAndStatusIn` por `DEPLOY`, adaptar `PipelineComponentDeleteServiceImpl`, conservar su guard posterior de infraestructura activa y eliminar `findFirstByComponentIdOrderByIdDesc` con su Javadoc.
4. Cerrar T2.1 y abrir T2.2.
5. Ejecutar formatter/checkstyle definido por el repo, tests focalizados y suite completa.
6. Medir cobertura de las clases productivas modificadas; agregar sólo tests de comportamiento hasta ≥95% line/branch.
7. Revisar diff/stat/status: ninguna segunda publicación, ningún cambio history/DTO/schema/frontend y `graphify-out/` intacto.
8. Cerrar T2.2; completar T2.3 con comandos, conteos, SHAs y riesgos.
9. Dejar `G2=review`, `status: review`, `progress: 100`, mover la tarea puente del padre a `[r]` y detener para revisión humana.

**Archivos esperados**

- `modify`: `ComponentRunRepository`, `DeltaComputationServiceImpl` y tests.
- `create` condicional: integration test de repository.
- `modify`: esta nota y tarea puente del padre.

**No tocar**

- Todos los no-scope; además, no hacer refactors cosméticos ni corregir deuda preexistente encontrada durante la suite.

**Spikes permitidos**

- Sólo ajustar la forma JPQL si H2/MySQL difieren; probar ambas mediante la suite disponible. Si requiere SQL nativo específico o migración, `PLAN_CONFLICT`.

**Tests y asserts**

- Query devuelve un run por componente y sólo de execution `DEPLOY`.
- Último `INACTIVATE FAILED` no fuerza retry.
- Último `DEPLOY FAILED` sí fuerza retry.
- Un run `INACTIVATE` no terminal no bloquea por sí solo el delete una vez terminal la infraestructura; un run `DEPLOY` activo sí lo bloquea.
- Mientras el service conserve infraestructura activa durante undeploy, el delete sigue respondiendo `422 COMPONENT_HAS_ACTIVE_INFRASTRUCTURE`.
- Inactivate exitoso deja el service `TERMINATED`; un deploy posterior sigue siendo decidido por la regla existente de servicio terminado, no por el run.
- Suite completa sin regresiones y cobertura ≥95% en alcance.

**Entregables/Gate G2**

- Diff final, suite/cobertura, status y no-touch verificables; `G2=review`.

**Handoff posterior**

- El owner revisa. Si acepta, marca tarea puente `[x]`; entonces usar `agents-os-entity-lifecycle` para archivar proyecto delegado y padre con log. El executor no autoacepta su gate ni archiva antes de esa confirmación.

## Validación

Comandos mínimos; adaptar sólo si `AGENTS.md` define wrappers distintos:

```bash
git checkout develop && git fetch origin && git pull --ff-only origin develop
./gradlew test --tests '*ComponentInactivationServiceImplTest' --tests '*InactivationResultHandlerImplTest' --tests '*DeltaComputationServiceImplTest'
./gradlew test --tests '*PipelineHistory*' --tests '*ComponentRunRepositoryIntegrationTest'
./gradlew clean test jacocoTestReport jacocoTestCoverageVerification
git diff --check
git status --short
```

No afirmar suite ni cobertura hasta ejecutar y conservar el resultado real. Un fallo preexistente debe aislarse y documentarse; no editar código ajeno para obtener verde.

## Compatibilidad, observabilidad, rollout y rollback

- **Compatibilidad:** filas antiguas `INACTIVATE` sin run siguen procesando resultados por el camino legacy; las nuevas filas lo incluyen. No backfill.
- **Persistencia:** aditiva en datos, sin DDL. El endpoint de history conserva el mismo schema y pasa de `component_runs=[]` a una lista de un elemento para ejecuciones nuevas.
- **Observabilidad:** mantener logs por `executionId`, `componentId` y status. Agregar warning cuando una ejecución nueva/legacy no tenga run; no loguear params ni error payload completo.
- **Rollout:** deploy normal de Playmaker. Durante rolling deploy pueden existir ejecuciones sin run; el handler tolera ambas.
- **Rollback de código:** revertir el commit de la feature. Los `component_run` ya persistidos son compatibles con el schema y history; no borrarlos.
- **Rollback de datos:** no aplica y no debe intentarse.

## Riesgos residuales y mitigaciones

| Riesgo | Mitigación dentro del proyecto | Fuera de alcance |
|---|---|---|
| El run declara una configuración distinta de la que viaja en el `DEPROVISION` | Run y comando leen `ServiceModel.componentDefinition` | Rediseñar la semántica actual de params del comando |
| Run queda no terminal para siempre si el CP nunca responde | No ocultarlo; history muestra estado real y el filtro `DEPLOY` impide que ese run bloquee por sí solo el delete cuando la infraestructura ya es terminal | Rediseño general del reaper de deployments |
| Evento terminal legacy sin run | Conservar comportamiento y warning | Backfill histórico |
| `INACTIVATE FAILED` contamina deploy | Filtrar positivamente por execution type `DEPLOY` | Rediseño general del delta |
| Delete durante inactivate | El guard de runs ignora `INACTIVATE`, pero el guard posterior de infraestructura activa continúa bloqueando mientras el service no sea terminal | Cambiar el contrato del endpoint de delete |
| Service sin `componentDefinition` | Reutilizar `422 INVALID_COMPONENT_STATUS` antes de crear execution/run o publicar | Crear un error HTTP nuevo o rediseñar los guards de inactivación |
| Relaciones/imports | Tests de no-regresión y no-touch | Cambiar regla funcional |

## Definition of Done

- Una aceptación `202` nueva persiste execution `INACTIVATE` y exactamente un run del target en la misma transacción.
- El `configId` del run y los parámetros del `DEPROVISION` publicado provienen de la misma `ComponentDefinition`, y el history existente devuelve el run.
- Execution y run reflejan `RUNNING`, `COMPLETED` o `FAILED` sin regresiones; todo run que recibe terminal queda terminal.
- `FAILED` conserva el componente activo y registra error seguro; `COMPLETED` conserva los cambios actuales de componente/servicio.
- Continúa existiendo exactamente una publicación `DEPROVISION` y cero invocaciones de batches/orchestration.
- El último run usado por la lógica de retry pertenece a una execution `DEPLOY`; `existsByComponentIdAndStatusIn` también filtra positivamente por `DEPLOY` y las consultas de history/handler siguen aceptando `INACTIVATE`.
- Un run `INACTIVATE` no terminal no bloquea por sí solo el delete cuando la infraestructura ya es terminal; el guard de infraestructura activa continúa bloqueando durante el undeploy normal.
- Componente inexistente conserva `404`; service ausente o sin `componentDefinition` resoluble responde `422 INVALID_COMPONENT_STATUS`, cubierto por test.
- `findFirstByComponentIdOrderByIdDesc` y su referencia Javadoc fueron eliminados.
- `D9`–`D13` figuran resueltas en Registro de decisiones, sin filas `OPEN`.
- No se modifican migrations, history productivo, frontend, SDK ni CPs. Excepción aprobada por el owner: el contrato del `202` de inactivate suma sólo `type: INACTIVATE`.
- Tests críticos, suite completa y gate de coverage reales quedan verdes; ≥95% line/branch para clases productivas modificadas por la entrega.
- La rama salió de un `develop` sincronizado con el remoto, y su SHA de base está en la Bitácora.
- Working tree y diff no contienen `graphify-out/`, `CLAUDE.md`/`Claude.md` ni cambios ajenos.
- `G2=review`, proyecto/tarea puente listos para aceptación humana.
- Tras aceptación del owner, ambos proyectos se archivan con change log; nunca antes.

## Prompt común para executor

```text
Trabaja únicamente la fase asignada del proyecto canónico “SIG-610 — ComponentRun de inactivación en Playmaker”. Lee primero su paquete autónomo, las decisiones cerradas y REPO_ROOT/AGENTS.md. La nota del proyecto es la única fuente de verdad: actualiza tareas, progress, Estado actual, gates y Bitácora a medida que avances.

Antes de tocar código ejecuta el Gate de repositorio: sincroniza develop con el remoto por fast-forward y crea la rama desde ahí. Nunca partas de una release/* ni de un SHA congelado en el documento. Respeta la base y cambios del usuario. No borres graphify-out/, no commitees CLAUDE.md ni Claude.md —colisionan por mayúsculas y una de las dos siempre aparece modificada—, no limpies cambios ajenos y no uses comandos Git destructivos. La evidencia manda en este orden: código/tests ejecutables, contratos runtime, documentos del proyecto. Si contradice una decisión o requiere tocar No tocar, detente con PLAN_CONFLICT y registra evidencia exacta.

Las decisiones D9 a D13 están cerradas y no se rediseñan durante la ejecución: usa `ServiceModel.componentDefinition`, reutiliza `422 INVALID_COMPONENT_STATUS`, filtra por `DEPLOY` exactamente las dos consultas activas definidas y elimina la consulta muerta, sin agregar reaper. Implementa KISS. No conectes inactivate con deploy, no crees Deployment/DeploymentGroup/batches, no cambies history/API/frontend/SDK/CPs y no publiques un segundo evento. Escribe primero tests de comportamiento crítico y luego completa cobertura hasta ≥95% line/branch en las clases modificadas.

Al terminar tu fase deja su gate en review y detente. No aceptes tu propio gate, no empieces otra fase y no archives el proyecto. La aceptación y el archivo final requieren al owner.
```

**Despacho Fase 0**

```text
FASE_ASIGNADA=0
PAQUETE_CANONICO=Paquete autónomo Fase 0 — Baseline y tests ejecutables
GATE_REQUERIDO=D9-D13 cerradas por el owner el 2026-09-09
TAREAS=T0.1-T0.2
SALIDA=develop sincronizado + rama creada con SHA registrado + tests críticos rojos por causas esperadas + G0 review
STOP=G0 review; prohibido modificar producción o iniciar F1
```

**Despacho Fase 1**

```text
FASE_ASIGNADA=1
PAQUETE_CANONICO=Paquete autónomo Fase 1 — Creación y state machine del run
GATE_REQUERIDO=G0 accepted
TAREAS=T1.1-T1.3
SALIDA=run persistido + state machine consistente + history visible + G1 review
STOP=G1 review; prohibido filtrar delta o iniciar F2
```

**Despacho Fase 2**

```text
FASE_ASIGNADA=2
PAQUETE_CANONICO=Paquete autónomo Fase 2 — Aislamiento del deploy y certificación
GATE_REQUERIDO=G1 accepted
TAREAS=T2.1-T2.3
SALIDA=query aislada + regresión/cobertura + diff final + G2 review
STOP=G2 review; prohibido autoaceptar o archivar antes del owner
```

## 📆 Bitácora

- **2026-09-10** — Findings del PR resueltos en la rama canónica `feature/sig-610-inactivate-component-run`: `PESSIMISTIC_WRITE` por `PipelineExecution` antes de los guards, resultado terminal contradictorio como no-op y persistencia segura del error sin payload upstream. Suites focalizadas y suite completa verdes; commit/push `6c0acae0c`. Respuestas publicadas a Ale y al bot; G2 sigue en review humana.
- **2026-09-10** — La primera publicación dejó PR coverage en 89,24% porque no se midió con la regla de Melicov que trata ramas parciales como no cubiertas. Se agregaron tests de comportamiento para todas las ramas nuevas y se reemplazaron dos switches exhaustivos con ramas sintéticas inalcanzables por decisiones equivalentes medibles. `./gradlew clean test jacocoTestReport` cerró con 3.650 tests, 2 skipped y cero fallos; Melicov remoto confirmó PR coverage 100,00% y todos los checks verdes en `1c2601f96`.
- **2026-09-10** — Fury creó [`0.0.7-test-sig-610-dev-0`](https://web.furycloud.io/rio-playmaker/versions/detail/0.0.7-test-sig-610-dev-0) desde la rama canónica y completó el build `1635` correctamente. `fury list-versions` confirmó estado `FINISHED` y el tag remoto resolvió al head esperado `1c2601f96d58`.
- **2026-09-09** — Fase 0 iniciada: `develop` quedó idéntico a `origin/develop`, SHA `2f7f572a9545feb1a4f5742dfc38ef963847e2d3`; se creó `feature/sig-610-inactivate-component-run`. El working tree sólo contiene el `graphify-out/` untracked esperado. El SPEC técnico SIG-614 fue contrastado con el plan y confirma el mismo alcance.
- **2026-09-09** — G0 pasado a `review`: `./gradlew test --tests ComponentInactivationServiceImplTest --tests InactivationResultHandlerImplTest --no-daemon` compiló y dejó cuatro rojos esperados, todos por gaps de producción: (1) lifecycle recibe `[]`, no un `DeltaEntry(UNDEPLOY)`; (2) service ausente permite publicar, no responde `422 INVALID_COMPONENT_STATUS` sin efectos; (3) `IN_PROGRESS` deja la execution `PENDING`; (4) `STARTED` deja la execution `PENDING`. La rama no contiene producción modificada. Se detectó que `PipelineExecutionModel` no tiene `startedAt`; el timestamp activo requerido se implementará sólo sobre `ComponentRun`, como prescribe SIG-614.
- **2026-09-09** — Owner aceptó G0. Se habilita Fase 1; mantener el scope de SIG-614, conservar los tests rojos como contrato y no iniciar Fase 2 hasta que G1 quede aceptado.
- **2026-09-09** — Fase 1 iniciada: T1.1 quedó en progreso. Se preservan los tests rojos de Fase 0; la implementación se limita a resolver la definición del service antes del lifecycle, crear un único `UNDEPLOY` y reutilizar esa definición para los params del `DEPROVISION`.
- **2026-09-09** — Fase 1 pausada antes de editar producción: `apply_patch` fue rechazado porque `~/fuentes/rio-playmaker` está fuera de las raíces de escritura de la sesión; la superficie CUA tampoco habilita el editor/terminal del repo. No se modificó producción ni se alteraron los tests rojos de Fase 0. Para retomar T1.1 se requiere exponer ese repo como raíz escribible.

- **2026-09-09** — El checkout del repo `rio-playmaker` está en `develop` con sólo `graphify-out/` untracked, pero el sandbox rechazó la escritura de `.git/index.lock` y `.git/FETCH_HEAD`; no se pudo sincronizar, crear la rama ni editar código. Spellbook también quedó inaccesible por permiso denegado del navegador; la planificación local mantiene SIG-610 como entidad canónica y no se marcaron tareas como completadas.

- **2026-09-09** — Owner cerró `D9`–`D13`. Se usará `ServiceModel.componentDefinition` como fuente única para `configId` y params; configuración no resoluble reutiliza `422 INVALID_COMPONENT_STATUS`; `findLastRunsByComponentIds` y `existsByComponentIdAndStatusIn` filtran positivamente por `DEPLOY`; `findFirstByComponentIdOrderByIdDesc` y su Javadoc se eliminan; no se agrega reaper. Se corrige además la semántica del delete: filtrar el run `INACTIVATE` no permite borrar durante undeploy porque el guard de infraestructura activa sigue vigente. Plan listo para Fase 0; código no iniciado.
- **2026-09-09** — Revisión del plan contra `develop`. La base congelada quedó 160 commits atrás, pero la superficie del alcance no cambió: sólo `ComponentInactivationServiceImpl` recibió ajustes en el guard de componentes importados. Se reemplaza el SHA congelado por sincronización de `develop` y creación de rama desde ahí. Se abren `D9`–`D13`: bloqueo permanente del delete lógico por un run sin reaper, fuente única de `configId` frente a los params del `DEPROVISION`, contrato del endpoint ante configuración no resoluble, alcance del filtro por tipo, y destino de `findFirstByComponentIdOrderByIdDesc`. Verificado además que mover la ejecución a `RUNNING` no rompe ningún guard, y que `DeploymentResultStatus` tiene exactamente los cuatro valores que cubre `D5`.
- **2026-09-09** — Fase 1 completada: `ComponentInactivationServiceImpl` valida service/`componentDefinition` antes de crear execution, lock o publish; crea exactamente un `UNDEPLOY` y reutiliza la misma definición para `configId` y params. `InactivationResultHandlerImpl` actualiza execution + `ComponentRun` de forma transaccional, con `RUNNING`, terminales, timestamps en el run, error seguro, no-op terminal y warning legacy.
- **2026-09-09** — Evidencia de G1: `./gradlew test --tests 'com.mercadolibre.rio.playmaker.service.impl.ComponentInactivationServiceImplTest' --tests 'com.mercadolibre.rio.playmaker.unit.service.InactivationResultHandlerImplTest' --tests 'com.mercadolibre.rio.playmaker.unit.service.PipelineHistoryServiceImplTest' --no-daemon` terminó `BUILD SUCCESSFUL`: 23 + 18 + 10 = 51 tests, sin fallos. `git diff --check` pasó; diff limitado a cinco archivos y `graphify-out/` permanece intacto/untracked. G1 queda en `review`; Fase 2 no se inicia hasta aceptación explícita del owner.
- **2026-09-09** — Owner aceptó G1 y habilitó Fase 2. T2.1 completada: `findLastRunsByComponentIds` aplica el filtro `DEPLOY` dentro del max-id subquery, el guard de delete consulta sólo runs `DEPLOY`, y se eliminó `findFirstByComponentIdOrderByIdDesc`; no se modificaron history, contratos ni schema.
- **2026-09-09** — T2.2/T2.3 completadas: `./gradlew clean test jacocoTestReport --no-daemon` terminó `BUILD SUCCESSFUL` con 3.639 tests, 2 skipped y 0 failures/errors. Cobertura Fase 2: `DeltaComputationServiceImpl` 97,4% líneas/100% branches y `PipelineComponentDeleteServiceImpl` 100%/100%; `git diff --check` pasó. G2 queda en `review`, pendiente de aceptación humana.
- **2026-09-09** — Entrega técnica committeada y publicada: `72a9db944` (`feat(SIG-610): track component inactivation runs`) en `origin/feature/sig-610-inactivate-component-run`. Se incluyeron sólo los 11 archivos del alcance; `graphify-out/` quedó fuera del commit. G2 continúa en `review`, pendiente de aceptación del owner.
- **2026-09-09** — Fury aceptó la creación de la versión de prueba `0.0.1-test-sig-610-dev-0`, asociada al commit `72a9db944493` en `feature/sig-610-inactivate-component-run`; estado inicial `pending`: [seguimiento en Fury](https://web.furycloud.io/rio-playmaker/versions/detail/0.0.1-test-sig-610-dev-0). Falta esperar el build y desplegarla sólo en scope test para la validación runtime.
- **2026-09-09** — El owner reabrió G2 para una corrección de contrato solicitada desde la integración frontend: el `202` de `POST .../inactivate` debe incluir `type: INACTIVATE`. No se cambia el tipo canónico a `UNDEPLOY`: éste es la acción de infraestructura; el frontend será corregido por otro dev para preservar/renderizar `INACTIVATE` como Undeploy.
- **2026-09-09** — Corrección T2.4 entregada: `InactivateComponentResponseDTO` expone `type`, `ComponentInactivationServiceImpl` lo puebla desde la ejecución creada y las pruebas de servicio/controlador lo verifican. `./gradlew test --tests 'com.mercadolibre.rio.playmaker.service.impl.ComponentInactivationServiceImplTest' --tests 'com.mercadolibre.rio.playmaker.controller.ComponentInactivationControllerTest' --no-daemon` terminó `BUILD SUCCESSFUL` (25 tests); `git diff --check` pasó. Commit/push: `423cb38d5` (`fix(SIG-610): expose inactivation execution type`). Fury aceptó `0.0.2-test-sig-610-dev-0` para ese commit, estado `pending`: [seguimiento en Fury](https://web.furycloud.io/rio-playmaker/versions/detail/0.0.2-test-sig-610-dev-0). G2 vuelve a `review`.
- **2026-09-09** — Evidencia runtime reabre G2: para `6a0c1c61-5a1a-4c38-a7ca-3b73d75bf5e4`, Kafka publicó `STARTED` y `COMPLETED` de `DEPROVISION` en el mismo segundo; history devolvió execution `COMPLETED`, `type=INACTIVATE`, pero su único run (`componentId=8962`) permaneció `PENDING`. Se corrige la transición del run sin asumir que el frontend sea la causa.
- **2026-09-09** — T2.5 publicada: `InactivationResultHandlerImpl` conserva el lookup preciso `executionId + componentId` y, ante correlación ausente, actualiza sólo el único run de esa execution; si hay más de uno conserva el fallback seguro y no adivina. `./gradlew test --tests 'com.mercadolibre.rio.playmaker.unit.service.InactivationResultHandlerImplTest' --tests 'com.mercadolibre.rio.playmaker.integration.DeploymentResultConsumerIntegrationTest' --no-daemon` terminó `BUILD SUCCESSFUL` (26 tests); `git diff --check` pasó. Commit/push: `20b16fe91` (`fix(SIG-610): complete uncorrelated inactivation run`). Fury aceptó [`0.0.3-test-sig-610-dev-0`](https://web.furycloud.io/rio-playmaker/versions/detail/0.0.3-test-sig-610-dev-0), estado `pending`; G2 queda en `review`.
- **2026-09-09** — Diagnóstico T2.6 publicado en `feature/sig-610-inactivate-component-run-test`: revierte `20b16fe91` para no enmascarar el problema y agrega trazas `INFO` para el payload completo del resultado, routing `INACTIVATE`, execution/`desiredStateHash`, componente resuelto, lookup del run y transición/persistencia `RUNNING`/terminal. La integración inyecta los dos `DeploymentResultMessage` equivalentes al flujo observado (`aws-msk-topic`, mismo UUID, `STARTED` y `COMPLETED`) a `DeploymentResultConsumerService`; terminó con execution y run `COMPLETED`. `./gradlew test --tests 'com.mercadolibre.rio.playmaker.integration.DeploymentResultConsumerIntegrationTest' --tests 'com.mercadolibre.rio.playmaker.unit.service.InactivationResultHandlerImplTest' --no-daemon` terminó `BUILD SUCCESSFUL`; commit/push `79843ded6` (`test(SIG-610): trace inactivation result handling`). Fury aceptó [`0.0.4-test-sig-610-dev-0`](https://web.furycloud.io/rio-playmaker/versions/detail/0.0.4-test-sig-610-dev-0), estado `pending`.
- **2026-09-09** — Validación E2E cerrada con `0.0.6-test-sig-610-dev-0` activa en `test3` y `bq-consumer-test-nonprod`: `POST /inactivate` respondió `202/Pending/INACTIVATE`; BigQueue entregó `STARTED` y `COMPLETED`; el consumer resolvió el run exacto y history mostró execution/ComponentRun `COMPLETED`. El desfase de artefactos queda confirmado como causa del síntoma observado. En la rama original se publicó el revert `67d0b1430`, seguido de limpiezas test-only derivadas de Zord (`a66545116`, `888b014e5`); `./gradlew check` y el workflow remoto pasaron. El PR #1144 quedó documentado y listo para aceptación humana.
- **2026-09-08** — Proyecto creado y planificado desde código `release/202609.1.0 @ 3982cc1de`, SIG-610, proposal de Grid, docs RIO y confirmaciones del owner. Decisiones cerradas: flujos separados; run obligatorio y terminal; relaciones activas siguen bloqueando; filtro de runs por tipo `DEPLOY`; alcance exclusivo de Playmaker. Listo para Fase 0 con un executor de menor capacidad.

## 🧭 Decisiones

- Serializar los resultados por la fila de `PipelineExecution`, no por Data Product, componente ni run; el primer terminal aceptado queda persistido y los posteriores son no-op.
- Tratar `DeploymentErrorPayload` como dato no confiable para history: no guardar ni loguear `message/details` upstream; aceptar sólo un code sintácticamente validado y un mensaje genérico propio.
- El registro completo está en “Registro de decisiones”; no crear decisiones paralelas aquí.

## 🔗 Docs / Links

- [[SIG-610 — Seguimiento de inactivación]]
- [[rio-playmaker]]
- [SIG-610 en Spellbook](https://spellbook.adminml.com/projects/SIG/specs/SIG-610)
- [Proposal en Grid](https://grid.adminml.com/d/01M14Z9X9XDHWY9C8RNHMAD6QQ/view)
- `VAULT_ROOT/30-resources/applications/rio-playmaker.md`
- `VAULT_ROOT/30-resources/rio-atlas/architecture/playmaker-deploy-flow.md`
- `VAULT_ROOT/10-projects/Meli/Presentación deployments en RIO/Deployments en RIO — flujo completo.md`

## 💡 Ideas

### Backlog de ideas

- Proyecto separado para discrepancias frontend/contratos de SIG-610 si el owner lo prioriza.

### Motivos / principios

- Un `ComponentRun` es seguimiento del componente dentro de una ejecución, no un segundo dispatch.
- El filtro positivo por tipo protege el deploy de ejecuciones presentes y futuras con otra semántica.

### Memoria pública / interna

- **Memoria pública:** [[rio-playmaker]] y documentación RIO enlazada.
- **Memoria interna:** no aplica; este proyecto contiene toda la continuidad necesaria.
- **Motivo:** el executor debe poder trabajar sin reconstruir discovery ni consultar el transcript.
