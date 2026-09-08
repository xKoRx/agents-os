---
type: project
schema_version: 1
owner: agent
root: false
status: active
priority: P1
area: "[[Meli]]"
parent: "[[SIG-610 — Seguimiento de inactivación]]"
sprint:
start: "2026-09-08"
due:
progress: 0
repo: https://github.com/melisource/fury_rio-playmaker
jira: SIG-610
prs:
aliases:
  - SIG-610 ComponentRun Playmaker
  - Inactivate ComponentRun
  - Undeploy execution tracking backend
tags:
  - kind/project
  - area/meli
  - application/rio-playmaker
  - ticket/sig-610
created: "2026-09-08"
updated: "2026-09-08"
---

# SIG-610 — ComponentRun de inactivación en Playmaker

> [!info]+ Proyecto delegado
> **Área:** [[Meli]] · **Estado:** active · **Prioridad:** P1 · **Parent:** [[SIG-610 — Seguimiento de inactivación]] · **Repo único:** [[rio-playmaker]]

## 🎯 Objetivo

Hacer que cada inactivación explícita aceptada por Playmaker cree exactamente un `ComponentRun` asociado a su `PipelineExecution` `INACTIVATE`, y mantener ambos estados consistentes desde `PENDING` hasta `RUNNING` y un resultado terminal. El history existente debe poder devolver ese run sin cambios de contrato. Un run de inactivación no debe alterar el cálculo ni el retry de un deploy posterior.

El cambio es deliberadamente backend-only y pequeño: no mezcla los flujos `DEPLOY` e `INACTIVATE`, no crea una segunda ejecución, no invoca la orquestación por batches y no publica más de un comando `DEPROVISION`.

## 📊 Estado actual

- **Estado del plan:** `ready_for_phase_0`.
- **Código:** no iniciado.
- **Repo verificado:** `release/202609.1.0` @ `3982cc1dee8e253d9b484b43b85a78cdc861babe` (`202609.1.0-rc-1`).
- **Working tree observado:** sólo `graphify-out/` untracked, preexistente; preservarlo y no incluirlo en commits.
- **Problema exacto:** `ComponentInactivationServiceImpl.dispatch` llama a `PipelineExecutionLifecycleService.create(..., List.of())`; por eso se guarda la ejecución `INACTIVATE`, pero no existe un `component_run` atribuible al componente.
- **Resultado actual:** `PipelineHistoryServiceImpl.getExecution` ya consulta `ComponentRunRepository.findByPipelineExecutionIdOrderByRunOrder`, por lo que devolverá automáticamente el run cuando exista.
- **Gap de consistencia:** `InactivationResultHandlerImpl` ignora `STARTED`/`IN_PROGRESS` y sólo actualiza la ejecución padre en terminal; si sólo se crea el run, quedaría eternamente `PENDING`.
- **Acoplamiento descubierto:** `DeltaComputationServiceImpl` consulta el último run del componente sin filtrar `PipelineExecutionType`; un `INACTIVATE` fallido podría ser interpretado como un deploy fallido y forzar un `DEPLOY` posterior.

## 🧱 Entrega de desarrollo

| Aplicación / repo | Branch | Base | SPEC funcional | SPEC técnica | Estado |
|---|---|---|---|---|---|
| [[rio-playmaker]] | crear `feature/sig-610-inactivate-component-run` | `release/202609.1.0` @ `3982cc1dee8e253d9b484b43b85a78cdc861babe` | [SIG-610 — Undeployment Functional Specification](https://spellbook.adminml.com/projects/SIG/specs/SIG-610) | [Undeploy execution proposal](https://grid.adminml.com/d/01M14Z9X9XDHWY9C8RNHMAD6QQ/view) y este plan | `ready_for_phase_0` |

> [!warning]+ Gate de repositorio
> Antes de tocar código, leer `REPO_ROOT/AGENTS.md` y las reglas Java que éste enrute. Crear la branch desde la base exacta indicada. Si la base ya no existe o el checkout contiene cambios ajenos distintos de `graphify-out/`, detenerse con `PLAN_CONFLICT`; no limpiar ni sobrescribir trabajo del usuario.

## Resumen ejecutivo y trabajo restante

1. Resolver el `Service` y su `Deployment` activo en el ambiente objetivo para obtener la configuración realmente desplegada.
2. Construir un único `DeltaEntry` `UNDEPLOY` y pasarlo al lifecycle existente, que persistirá el `ComponentRun` `PENDING` en la misma transacción que la ejecución.
3. Extender el handler de resultados de inactivación para actualizar run y ejecución de manera atómica en `STARTED`, `IN_PROGRESS`, `COMPLETED` y `FAILED`.
4. Limitar la consulta de “último run fallido” del delta de deploy a ejecuciones `DEPLOY`.
5. Probar invariantes, regresiones y cobertura de las clases modificadas; no tocar history, frontend, SDK, CPs ni schema.

## Matriz requerimiento → evidencia

| ID | Requerimiento | Estado | Evidencia actual | Trabajo requerido |
|---|---|---|---|---|
| R1 | Inactivate es un flujo separado de deploy | `done` | `HEAD` — `ComponentInactivationServiceImpl.inactivate/dispatch`; `PipelineDeployServiceImpl.deploy` | No modificar |
| R2 | Una inactivación aceptada crea una ejecución `INACTIVATE` | `done` | `HEAD` — `ComponentInactivationServiceImpl.dispatch` | Conservar |
| R3 | La ejecución contiene exactamente un run del target | `missing` | `HEAD` — lifecycle recibe `List.of()` | Crear `DeltaEntry` único |
| R4 | El run referencia la configuración desplegada | `missing` | `CONTRACT` — `DeltaEntry.configId` documenta la config desplegada para `UNDEPLOY`; `ComponentRunModel.componentDefinition` es no-null | Resolver `DeploymentModel.componentDefinition.id` del deployment activo |
| R5 | History devuelve el run | `partial` | `HEAD` — history ya consulta y mapea todos los runs de la ejecución | Sin cambio productivo; validar por test existente/nuevo |
| R6 | Estado activo observable | `missing` | `HEAD` — handler ignora `STARTED/IN_PROGRESS` | Run y ejecución pasan a `RUNNING`, con `startedAt` idempotente |
| R7 | Estado terminal consistente | `missing` | `HEAD` — sólo la ejecución queda terminal | Run `COMPLETED/FAILED`, `completedAt` y error cuando corresponda |
| R8 | Duplicados/out-of-order no regresan terminales | `partial` | `HEAD` — guard `execution.getStatus().isFinal()` | Conservar y probar run + ejecución |
| R9 | Inactivate no contamina el retry del deploy | `missing` | `HEAD` — `findLastRunsByComponentIds` no filtra tipo | Consulta fail-closed para `PipelineExecutionType.DEPLOY` |
| R10 | No cambia el dispatch | `done` | `HEAD` — publicación única post-commit de `DEPROVISION` | Probar que continúa siendo una publicación |
| R11 | Relaciones/imports impiden inactivar | `done` | `HEAD` — `validateInactivation`, `guardActiveImports`, `findActiveByComponentId` | No modificar |

## Alcance

### Dentro

- Creación de un `ComponentRun` para cada nueva ejecución `INACTIVATE` aceptada.
- Selección explícita de la `ComponentDefinition` efectivamente desplegada como `configId`.
- Estados y timestamps del run; estado `RUNNING` de la ejecución padre.
- Persistencia de error estructurado del run en `FAILED`, con fallback seguro si falla la serialización.
- Compatibilidad con ejecuciones antiguas sin run durante rollout.
- Filtro por tipo de ejecución en la consulta que alimenta la regla de retry del deploy.
- Tests unitarios, repository/integration cuando corresponda y suite/gate de cobertura.

### Fuera

- Frontend, BFF y polling.
- Cambiar los endpoints o DTOs de history.
- Cambiar el response del `POST /inactivate`.
- Crear `Deployment`, `DeploymentGroup` o batches para el inactivate.
- Cambiar el evento `DeploymentTriggerMessage` o `rio-sdk-events`.
- Modificar control planes o su operación `DEPROVISION`.
- Cambiar el lock por data product, su respuesta `409` o su granularidad.
- Cambiar autorización del history.
- Incorporar `CANCELLED`, `updatedAt` o secuencias de eventos.
- Cambiar la semántica final del canvas (`INACTIVE`/`TERMINATED` versus `READY_TO_DEPLOY`).
- Cambiar la validación de relaciones activas, imports o infraestructura previa.
- Corregir parámetros históricos del `DEPROVISION` salvo que sea indispensable para construir el run; cualquier expansión exige `PLAN_CONFLICT`.

## Registro de decisiones

| ID | status | resolution | source/evidence | phase consuming it |
|---|---|---|---|---|
| D1 | `CONFIRMED` | Deploy e inactivate son botones y ejecuciones separadas; este cambio no debe unirlos ni disparar dos flujos. | Confirmación del owner, 2026-09-08; `ComponentInactivationServiceImpl` | F0–F2 |
| D2 | `CONFIRMED` | El único resultado funcional de esta entrega es agregar seguimiento por `ComponentRun`, dejándolo siempre consistente y terminal. | Confirmación del owner, 2026-09-08 | F1 |
| D3 | `CONFIRMED` | No se puede inactivar mientras existan asociaciones activas; la validación existente queda intacta. | Confirmación del owner + `ComponentInactivationServiceImpl.validateInactivation` | F0–F2 |
| D4 | `TECHNICAL_RESOLUTION` | `configId` será `DeploymentModel.componentDefinition.id` del deployment `is_active=true` asociado al `Service` del componente/ambiente; no la última definición global ni una configuración pendiente. | `DeltaEntry` Javadoc + `DeltaComputationServiceImpl.evaluateComponent` | F0–F1 |
| D5 | `TECHNICAL_RESOLUTION` | `STARTED` e `IN_PROGRESS` convergen a `RUNNING`; `startedAt` se asigna una vez. `COMPLETED/FAILED` son terminales y asignan `completedAt`. | Enums actuales + contrato SDK `DeploymentResultStatus` | F1 |
| D6 | `TECHNICAL_RESOLUTION` | La regla de retry consulta sólo el último run de ejecuciones `DEPLOY`, en vez de excluir únicamente `INACTIVATE`; es fail-closed ante tipos futuros. | `DeltaComputationServiceImpl` y `PipelineExecutionType` | F2 |
| D7 | `TECHNICAL_RESOLUTION` | Las ejecuciones legacy sin run conservan el comportamiento actual del handler y generan warning; no fallan ni bloquean el rollout. | Compatibilidad rolling deploy | F1 |
| D8 | `TECHNICAL_RESOLUTION` | No hay migración: `component_run` y sus estados ya existen; la relación ejecución/componente ya tiene unique constraint. | `ComponentRunModel` + migrations existentes | F0–F2 |

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
  -> resuelve Service + Deployment activo + ComponentDefinition desplegada
  -> crea PipelineExecution(INACTIVATE, PENDING)
       └── ComponentRun(target, deployedConfig, PENDING)
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

`configId` es el PK de `ComponentDefinitionModel` que identifica la versión/configuración materializada por el deployment activo del `Service` en el ambiente. `ComponentRunModel.componentDefinition` es una FK obligatoria, de modo que no puede crearse un run sin una definición resoluble.

Resolución autorizada:

```text
component + environment
  -> ServiceRepository.findByComponentIdAndEnvironmentId
  -> DeploymentRepository.findByServiceIdAndIsActiveTrue
  -> DeploymentModel.componentDefinition.id == DeltaEntry.configId
```

Si falta `Service`, deployment activo o `componentDefinition`, detener antes de crear la ejecución y antes de publicar. Usar el error tipado vigente para estado/infraestructura inválida; no inventar una FK, no usar la última definición global y no publicar un comando imposible de atribuir.

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
- El history invoca resolución de timeouts de deployments, pero una ejecución `INACTIVATE` no tiene `DeploymentGroup/Deployment`; esa consulta queda vacía y no administra el timeout de este run. No agregar retry/timeout nuevo en este proyecto.

## Mapa de archivos y símbolos

| Acción | Archivo | Símbolos/responsabilidad |
|---|---|---|
| `modify` | `REPO_ROOT/src/main/java/com/mercadolibre/rio/playmaker/service/impl/ComponentInactivationServiceImpl.java` | `dispatch`, resolución de service/deployment/config y `DeltaEntry` único |
| `modify` | `REPO_ROOT/src/main/java/com/mercadolibre/rio/playmaker/service/impl/InactivationResultHandlerImpl.java` | lookup y transiciones de `ComponentRun`, timestamps/error, compatibilidad legacy |
| `modify` | `REPO_ROOT/src/main/java/com/mercadolibre/rio/playmaker/repository/ComponentRunRepository.java` | consulta del último run por componentes filtrada por tipo `DEPLOY` |
| `modify` | `REPO_ROOT/src/main/java/com/mercadolibre/rio/playmaker/service/pipeline/impl/DeltaComputationServiceImpl.java` | consumir consulta filtrada |
| `modify` | `REPO_ROOT/src/test/java/com/mercadolibre/rio/playmaker/service/impl/ComponentInactivationServiceImplTest.java` | captura/assert del `DeltaEntry`, config y publicación única |
| `modify` | `REPO_ROOT/src/test/java/com/mercadolibre/rio/playmaker/unit/service/InactivationResultHandlerImplTest.java` | matriz completa de estados/idempotencia/legacy/error |
| `modify` | `REPO_ROOT/src/test/java/com/mercadolibre/rio/playmaker/unit/service/DeltaComputationServiceImplTest.java` | filtro del último run |
| `create` condicional | `REPO_ROOT/src/test/java/com/mercadolibre/rio/playmaker/integration/ComponentRunRepositoryIntegrationTest.java` | demostrar la query filtrada si no existe fixture equivalente reutilizable |
| `no-touch` | `PipelineHistoryServiceImpl`, controllers/DTOs de history | ya devuelven cualquier run persistido |
| `no-touch` | `PipelineExecutionLifecycleServiceImpl`, `ComponentRunModel`, enums y migrations | ya soportan la fila y estados necesarios |
| `no-touch` | frontend, BFF, SDK y control planes | fuera del repo/scope |

## ✅ Tareas

> [!note]+ Contrato atómico
> Cada tarea incluye objetivo, archivos/símbolos, precondiciones, implementación, tests y evidencia esperada. El executor actualiza `[ ] → [/] → [r] → [x]` dentro de esta nota; sólo el owner acepta gates.

- [ ] **T0.1 · Congelar baseline** — objetivo: crear la branch acordada y verificar que la evidencia sigue vigente; archivos/símbolos: repo, `AGENTS.md`, cuatro clases productivas y tres tests listados; precondición: checkout en `3982cc1de`; implementación: crear branch, registrar `git status`, releer instrucciones y comparar firmas; tests: ninguno; evidencia: branch/base/status en Bitácora #owner/agent #type/dev #area/meli
- [ ] **T0.2 · Especificar fixtures críticos primero** — objetivo: escribir/ajustar tests rojos que expresen run único, configuración desplegada, estados y aislamiento del deploy; archivos: tests listados; precondición: T0.1; implementación: fixtures mínimos, sin producción todavía; tests: ejecutar sólo clases afectadas y demostrar fallos esperados; evidencia: nombres de tests y causas de rojo #owner/agent #type/dev #area/meli
- [ ] **T1.1 · Crear el run de inactivación** — objetivo: entregar un `DeltaEntry` único al lifecycle; archivos: `ComponentInactivationServiceImpl` y test; precondición: G0 accepted; implementación: resolver service/deployment activo/definition, construir `UNDEPLOY`, reutilizar valores y conservar publicación; tests: run exacto, ausencia de filas inválidas, rollback de lock, una publicación; evidencia: tests verdes #owner/agent #type/dev #area/meli
- [ ] **T1.2 · Mantener estados consistentes** — objetivo: actualizar execution + run en todos los resultados; archivos: `InactivationResultHandlerImpl` y test; precondición: T1.1; implementación: repository/object mapper, helpers de transición y error; tests: STARTED, IN_PROGRESS, COMPLETED, FAILED, duplicados, terminal tardío, legacy sin run, serialización fallida; evidencia: tests verdes y timestamps/asserts #owner/agent #type/dev #area/meli
- [ ] **T1.3 · Probar visibilidad en history sin modificarlo** — objetivo: demostrar que el run persistido es consumible por el query actual; archivos: test de lifecycle/history existente, sólo si hace falta; precondición: T1.1–T1.2; implementación: fixture `INACTIVATE` con un run; tests: detail contiene un run target y tipo `INACTIVATE`; evidencia: test verde y cero cambios productivos en history #owner/agent #type/dev #area/meli
- [ ] **T2.1 · Aislar delta de deploy** — objetivo: que sólo runs de ejecución `DEPLOY` alimenten la regla de retry; archivos: repository, delta service y tests; precondición: G1 accepted; implementación: query filtrada por tipo, caller explícito; tests: último `INACTIVATE FAILED` ignorado, último `DEPLOY FAILED` conservado, combinación de ambos elige el último deploy; evidencia: unit + repository/integration verdes #owner/agent #type/dev #area/meli
- [ ] **T2.2 · Regresión y cobertura** — objetivo: validar el conjunto; archivos: sólo tests/ajustes estrictamente derivados; precondición: T2.1; implementación: correr formato, suites focalizadas y suite completa; tests: funcionalidad crítica primero, luego ≥95% line/branch en clases productivas nuevas o modificadas por la entrega; evidencia: comandos, conteo y reportes registrados #owner/agent #type/dev #area/meli
- [ ] **T2.3 · Entrega y cierre técnico** — objetivo: dejar diff revisable y proyecto honesto; archivos: esta nota y repo; precondición: T2.2; implementación: revisar diff/stat/status, confirmar no-touch, actualizar progreso/bitácora y mover G2 a review; tests: no adicionales; evidencia: commit(s), SHA, suites y riesgos residuales #owner/agent #type/admin #area/meli

## Roadmap y gates

| Gate | current state | phase agent responsibility | owner acceptance evidence | enables |
|---|---|---|---|---|
| G0 | pending | Congelar baseline y entregar tests críticos rojos sin inventar semántica | Diff sólo de tests/nota, nombres y fallos corresponden a R3–R9 | F1 |
| G1 | pending | Crear run y completar su state machine con compatibilidad | Tests focalizados verdes; history ve un run; exactamente un publish | F2 |
| G2 | pending | Filtrar delta, correr regresión/cobertura y entregar | Suite completa verde, cobertura ≥95% en alcance, status/diff limpios y no-touch respetado | Revisión humana y posterior archivo |

El executor sólo puede dejar el gate de su fase en `review`. El owner lo cambia a `accepted`; no comenzar la siguiente fase antes de eso.

## Paquetes autónomos

### Paquete autónomo Fase 0 — Baseline y tests ejecutables

**Misión exacta**

Congelar la base real y convertir las decisiones cerradas en tests rojos, sin modificar producción.

**Precondiciones verificables**

- Repo disponible y HEAD/base resoluble en `3982cc1dee8e253d9b484b43b85a78cdc861babe`.
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

- D1–D8. No reabrir la separación de flujos, la fuente de `configId` ni el filtro `DEPLOY`.

**Implementación paso a paso**

1. Crear `feature/sig-610-inactivate-component-run` desde la base exacta.
2. Confirmar que sólo `graphify-out/` está untracked; preservar cualquier otro cambio y detener con `PLAN_CONFLICT` si solapa.
3. Cambiar T0.1 a `[/]`, registrar baseline y luego `[x]`.
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

- El inactivate debe pasar una lista de tamaño 1, action `UNDEPLOY`, target correcto y config del deployment activo.
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
- Leer `VAULT_ROOT/10-projects/Meli/SIG-610 — Seguimiento de inactivación/agentes/SIG-610 — ComponentRun de inactivación en Playmaker.md`, especialmente D4–D7 y tabla de estados.

**Lectura obligatoria**

- `ComponentInactivationServiceImpl`, `PipelineExecutionLifecycleServiceImpl.saveComponentRun`, `DeltaEntry`, `DeploymentRepository.findByServiceIdAndIsActiveTrue`.
- `InactivationResultHandlerImpl`, `ComponentRunModel`, `ComponentRunRepository.findByPipelineExecutionIdAndComponentId`.
- `DeploymentResultHandlerImpl.routeByStatus/serializeError` como patrón, sin copiar su orquestación.
- Tests de F0.
- `VAULT_ROOT/10-projects/Meli/Presentación deployments en RIO/Deployments en RIO — flujo completo.md`, sección `ComponentRun versus Deployment`.

**Decisiones cerradas**

- Un run, config desplegada, state machine de D5, compatibilidad legacy y cero batches/segundo publish.

**Implementación paso a paso**

1. Marcar T1.1 `[/]`.
2. Resolver `Service`, deployment activo y definition antes de llamar al lifecycle.
3. Construir `DeltaEntry(componentId, UNDEPLOY, deployedDefinitionId, serviceId, componentType)` y pasar `List.of(entry)`.
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

- Ninguno. Si no se puede obtener deployment/config activo con repositorios existentes, `PLAN_CONFLICT`; no introducir fallback global.

**Tests y asserts**

- Exactamente un delta/run y un publish.
- Config ID corresponde al deployment activo del environment.
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

Evitar que runs `INACTIVATE` influyan en el delta de deploy y certificar la entrega completa.

**Precondiciones verificables**

- `G1=accepted` por el owner.
- Creación y transiciones del run verdes.
- Leer `VAULT_ROOT/10-projects/Meli/SIG-610 — Seguimiento de inactivación/agentes/SIG-610 — ComponentRun de inactivación en Playmaker.md`, D6, riesgos y Definition of Done.

**Lectura obligatoria**

- `ComponentRunRepository.findLastRunsByComponentIds`.
- `DeltaComputationServiceImpl.computeDelta/evaluateComponent`.
- Tests unitarios/integration de repositories y delta.
- Reglas de build/test desde `REPO_ROOT/AGENTS.md`.
- `VAULT_ROOT/30-resources/rio-atlas/architecture/playmaker-deploy-flow.md` para confirmar que esta query sólo decide delta de deploy.

**Decisiones cerradas**

- Filtrar positivamente por `PipelineExecutionType.DEPLOY`; no hardcodear una exclusión que acepte tipos futuros.

**Implementación paso a paso**

1. Marcar T2.1 `[/]`.
2. Reemplazar/ampliar la query para obtener el último run por componente sólo dentro de executions `DEPLOY`; el `MAX(id)` y el filtro deben vivir en la misma selección.
3. Actualizar el caller y probar orden mixto: INACTIVATE fallido más reciente no reemplaza el último DEPLOY; DEPLOY fallido sí conserva retry.
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
- Inactivate exitoso deja el service `TERMINATED`; un deploy posterior sigue siendo decidido por la regla existente de servicio terminado, no por el run.
- Suite completa sin regresiones y cobertura ≥95% en alcance.

**Entregables/Gate G2**

- Diff final, suite/cobertura, status y no-touch verificables; `G2=review`.

**Handoff posterior**

- El owner revisa. Si acepta, marca tarea puente `[x]`; entonces usar `agents-os-entity-lifecycle` para archivar proyecto delegado y padre con log. El executor no autoacepta su gate ni archiva antes de esa confirmación.

## Validación

Comandos mínimos; adaptar sólo si `AGENTS.md` define wrappers distintos:

```bash
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
| `configId` incorrecto si existe config pendiente | Usar definition del deployment activo, no service/global latest | Revisar semántica de params del DEPROVISION |
| Run queda activo para siempre si el CP nunca responde | No ocultarlo; history muestra estado real | Timeout/reaper específico para INACTIVATE |
| Evento terminal legacy sin run | Conservar comportamiento y warning | Backfill histórico |
| `INACTIVATE FAILED` contamina deploy | Filtrar positivamente por execution type `DEPLOY` | Rediseño general del delta |
| Delete durante inactivate | La validación existente ve run PENDING/RUNNING y bloquea; terminal desbloquea | Cambiar contrato de delete |
| Relaciones/imports | Tests de no-regresión y no-touch | Cambiar regla funcional |

## Definition of Done

- Una aceptación `202` nueva persiste execution `INACTIVATE` y exactamente un run del target en la misma transacción.
- El run referencia la configuración desplegada y history existente lo devuelve.
- Execution y run reflejan `RUNNING`, `COMPLETED` o `FAILED` sin regresiones; todo run que recibe terminal queda terminal.
- `FAILED` conserva el componente activo y registra error seguro; `COMPLETED` conserva los cambios actuales de componente/servicio.
- Continúa existiendo exactamente una publicación `DEPROVISION` y cero invocaciones de batches/orchestration.
- El último run usado por la lógica de retry pertenece a una execution `DEPLOY`.
- No se modifican contratos, migrations, history productivo, frontend, SDK ni CPs.
- Tests críticos, suite completa y gate de coverage reales quedan verdes; ≥95% line/branch para clases productivas modificadas por la entrega.
- Working tree y diff no contienen `graphify-out/` ni cambios ajenos.
- `G2=review`, proyecto/tarea puente listos para aceptación humana.
- Tras aceptación del owner, ambos proyectos se archivan con change log; nunca antes.

## Prompt común para executor

```text
Trabaja únicamente la fase asignada del proyecto canónico “SIG-610 — ComponentRun de inactivación en Playmaker”. Lee primero su paquete autónomo, las decisiones cerradas y REPO_ROOT/AGENTS.md. La nota del proyecto es la única fuente de verdad: actualiza tareas, progress, Estado actual, gates y Bitácora a medida que avances.

Respeta la base y cambios del usuario. No borres graphify-out/, no limpies cambios ajenos y no uses comandos Git destructivos. La evidencia manda en este orden: código/tests ejecutables, contratos runtime, documentos del proyecto. Si contradice una decisión o requiere tocar No tocar, detente con PLAN_CONFLICT y registra evidencia exacta.

Implementa KISS. No conectes inactivate con deploy, no crees Deployment/DeploymentGroup/batches, no cambies history/API/frontend/SDK/CPs y no publiques un segundo evento. Escribe primero tests de comportamiento crítico y luego completa cobertura hasta ≥95% line/branch en las clases modificadas.

Al terminar tu fase deja su gate en review y detente. No aceptes tu propio gate, no empieces otra fase y no archives el proyecto. La aceptación y el archivo final requieren al owner.
```

**Despacho Fase 0**

```text
FASE_ASIGNADA=0
PAQUETE_CANONICO=Paquete autónomo Fase 0 — Baseline y tests ejecutables
GATE_REQUERIDO=none
TAREAS=T0.1-T0.2
SALIDA=baseline registrado + tests críticos rojos por causas esperadas + G0 review
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

- **2026-09-08** — Proyecto creado y planificado desde código `release/202609.1.0 @ 3982cc1de`, SIG-610, proposal de Grid, docs RIO y confirmaciones del owner. Decisiones cerradas: flujos separados; run obligatorio y terminal; relaciones activas siguen bloqueando; filtro de runs por tipo `DEPLOY`; alcance exclusivo de Playmaker. Listo para Fase 0 con un executor de menor capacidad.

## 🧭 Decisiones

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
