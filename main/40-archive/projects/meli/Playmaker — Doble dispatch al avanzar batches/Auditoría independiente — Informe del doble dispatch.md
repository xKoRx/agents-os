---
type: doc
schema_version: 1
status: active
area: "[[Meli]]"
related:
  - "[[Playmaker — Doble dispatch al avanzar batches]]"
  - "[[Prompt maestro — Auditoría independiente del doble dispatch]]"
  - "[[rio-playmaker]]"
  - "[[RIO]]"
  - "[[playmaker-deploy-flow]]"
aliases:
  - Informe auditoría doble dispatch
  - Auditoría doble dispatch Playmaker
tags:
  - kind/doc
  - area/meli
  - app/rio-playmaker
created: "2026-08-21"
updated: "2026-08-25"
---

# Auditoría independiente — Informe del doble dispatch

> [!warning] RECOMENDACIÓN SUPERSEDED — 2026-08-25
> Este informe permanece congelado como evidencia independiente de causa raíz y riesgos. Su recomendación basada en `PENDING → DISPATCHING`, lock pesimista y rollout del enum queda **DEPRECATED** y no debe implementarse. La decisión vigente está en [[Playmaker — Doble dispatch al avanzar batches]], sección “Decisión vigente — hotfix acotado + refactor durable”: primero mutex KVS en `BatchCompletedEventListener` con espera/backoff y detección por deployments existentes del group, sin schema/estados/CPs; luego refactor durable con tópico externo y lógica atómica/consistente.

## Propósito

Consolidar el resultado de la auditoría en dos fases definida en [[Prompt maestro — Auditoría independiente del doble dispatch]]: causa raíz verificada desde código, contraste con el diagnóstico previo, matriz de alternativas y diseño recomendado. El estado y las tareas viven en [[Playmaker — Doble dispatch al avanzar batches]]; esta nota es el informe.

Snapshot auditado: repo `rio-playmaker`, rama `develop`, HEAD `0524ce49ef34`, refs remotas al 2026-08-20 23:29. Trabajo read-only: sin cambios de código, schema ni refs, sin `git fetch`, sin ejecutar la suite.

## Contenido

### Barrera anti-anclaje

La fase 1 se escribió y se hasheó antes de abrir el diagnóstico previo, y el checksum se verificó con `shasum -c` inmediatamente antes y después de abrirlo. Los artefactos originales fueron efímeros (fuera del vault); acá quedan sus checksums como provenance y su contenido destilado.

| Artefacto | SHA-256 |
|---|---|
| Fase 1 — investigación independiente congelada | `aa4a542fc925f5255c7b07d14fa7cd227d0113c7a7b649080ec519faee8a2bdb` |
| Fase 2 — addendum de contraste | `2c6f55a3814f332469fdc318c9074ad93867b5269a5783af685066b5ea691e9a` |

### Causa raíz

El avance de batch evalúa una **condición de nivel** — *batch N terminal Y batch N+1 en PENDING* — y actúa sobre ella **sin consumirla**. El dispatch no transiciona el `ComponentRun`: pasa a `RUNNING` sólo cuando el control plane devuelve `STARTED`, unos 3 s después. La condición sigue verdadera después de haber actuado, así que cualquier segundo evaluador la vuelve a ver verdadera y vuelve a despachar. Sitio: `rio-playmaker` · `src/main/java/com/mercadolibre/rio/playmaker/service/pipeline/impl/OrchestrationServiceImpl.java:56-129`, predicado en `:81-87`.

### Trigger: el commit que invirtió la carrera

`dac615f47` (PR #1047, en `develop` desde el 2026-08-19; incidente el 2026-08-20) reemplazó la llamada inline `orchestrationService.checkPrerequisites(run, deployment)` por `eventPublisher.publishEvent(new BatchCompletedEvent(...))`, recibido por un listener con `@Async` (pool de 16 hilos), `@TransactionalEventListener(AFTER_COMMIT)` y `PROPAGATION_REQUIRES_NEW`.

Antes, el avance se evaluaba dentro de la transacción del resultado: dos hermanos del batch 0 que terminan juntos leían al otro run como todavía no commiteado, así que **ninguno** avanzaba y la execution quedaba pegada en `RUNNING`. Después, los dos listeners corren cuando los dos commits ya son visibles, los dos ven el batch 0 terminal y el batch 1 en `PENDING`, y **los dos** despachan.

El refactor no introdujo la falla de diseño — el check-then-act sin claim ya estaba. Quitó lo único que accidentalmente la tapaba: la invisibilidad mutua de dos transacciones concurrentes. El bug pasó de manifestarse como *nadie avanza* a *todos avanzan*. La intención del cambio era correcta: la resolución de parámetros del batch siguiente necesita leer outputs ya commiteados.

Precisión importante para reproducir: lo que se volvió asíncrono **no** es la lectura de los results. El consumo sigue siendo sincrónico y además está serializado por un lock pesimista por fila de deployment (`DeploymentRepository.java:350-366`), así que dos entregas del *mismo* result no se pisan. Lo que hay que reproducir son **dos COMPLETED de componentes distintos del mismo batch** commiteando casi juntos.

### Daño real, más grave que el crash

De los dos intentos creados para el `flink-sql`, el control plane aceptó `6421` (llegó a `deploy_started`) y rechazó `6422` con `Application already exists`. **El resultado FAILED del intento espurio fue el que marcó FAILED al `ComponentRun` legítimo** (run 1827, `completed_at` 03:42:04, que coincide con el update de `6422`), y `propagateFailure` tumbó el group y la execution. `6421` murió por timeout 30 min después y su resultado se descartó por el terminal guard, dejando una aplicación Kinesis Analytics huérfana en AWS.

O sea: el doble dispatch no sólo dejó basura en la DB, hizo fracasar un deploy que iba bien.

### Por qué el fix obvio no alcanza

Existe un fix **no mergeado**, `adf5cf54f` (2026-06-22, sólo en `origin/feature/kvs-actions-segmented-test-scopes`), que agrega `pipelineExecutionRepository.findByIdForUpdate(executionId)` al inicio de `checkPrerequisites`. Ese método **no existe en develop**. Y el lock solo no arregla el doble dispatch:

- Serializa a los dos evaluadores, sí. Pero cuando el segundo toma el lock, los runs del batch siguiente **siguen en `PENDING`** — el dispatch no los transiciona — así que el predicado vuelve a ser verdadero y despacha de nuevo.
- Lo único que lo detiene es un efecto colateral: serializado, el segundo ve la fila del primero con status `deploy_requested`, que no es final, y `validateActiveDeployments` lanza `ConflictException`. Funciona **por accidente**, con log ERROR en el camino normal.
- Y deja un hueco residual real: si el control plane responde tan rápido que la fila del primero ya está *terminal*, la validación **pasa**, el segundo desactiva la del primero y crea otra. No hay doble fila activa, pero **sí un segundo PROVISION** al control plane. El daño externo persiste.

Conclusión: hay que **invalidar el predicado**, no sólo serializar. El lock se mantiene, pero por otra razón: `propagateFailure` cancela runs con `status == PENDING` de orden superior y hoy corre **sincrónico** dentro de la transacción del result (la asincronización fue parcial, sólo el camino COMPLETED), así que puede interleavear con un claim concurrente y dejar un run despachado dentro de una execution fallida.

### La duplicación es pegajosa entre deploys

Hallazgo derivado de que el DP se deployó dos veces: **el redeploy no limpia**. `loadActiveDeployments` colapsa duplicados con `Collectors.toMap(..., (first, second) -> first)` (`BatchDispatchServiceImpl.java:189-195`) y `dispatchItem` desactiva **sólo** esa fila (`:226-230`). Con dos activas: desactiva una, inserta una nueva activa, quedan dos. El conteo de deployments activos por service **nunca baja** por redeploy; la corrupción se arrastra hasta repararla a mano.

Las dos filas del incidente comparten `deployment_group_id` y `pipeline_execution_id`, y cada deploy crea un group nuevo, así que salieron ambas del **primer** deploy. El segundo sólo dejó la corrupción a la vista.

### Invariantes y su enforcement real

| Invariante | Declarada en | Enforced en DB |
|---|---|---|
| 1 `ComponentRun` por (execution, component) | entidad + migración | **Sí** (`uq_cr_execution_component`) |
| ≤1 `Deployment` con `is_active=true` por service | **sólo prosa** (`DeploymentModel.java:57`, `DeploymentRepository.java:78-79`) | **No** |
| ≤1 execution in-flight por (pipeline, hash) | check-then-act (`PipelineDeployServiceImpl.java:192-198`) | **No** |
| 1 `Deployment` por (group, service) | ninguna parte | **No**, pero se cumple de hecho |

La tabla `deployment` tiene sólo PK, dos FK y cuatro índices no únicos. Revisadas las 108 migraciones.

`is_active` tiene hoy significado ambiguo: el javadoc de `DeploymentResultHandlerImpl.java:271-275` afirma que el único escritor de `false` es el paso "desactivar el anterior", y es falso — `DeploymentDispatchEventListener.java:120` escribe `false` cuando falla el transporte, dejando el slot con **cero** filas activas, y entonces los lectores reportan `NOT_DEPLOYED` sobre un componente con historial.

### Síntoma de lectura y radio de impacto

El `IllegalStateException: Duplicate key 5120` sale de un `Collectors.toMap` por `service.id` sin función de merge en `PipelineServiceImpl.java:300-303`. El mismo bug está en `DeltaComputationServiceImpl.java:104-108`, o sea **dentro del propio camino de deploy**. Sumado a que el stacktrace entra por `patchComponentConfig`, el estado corrupto es **autobloqueante**: no se puede re-deployar ni editar la config para salir.

Radio total: 8 call sites de `Optional findByServiceIdAndIsActiveTrue` (native query) que con dos filas lanzan `IncorrectResultSizeDataAccessException`, más 3 del batch, 2 de ellos sin merge.

### Hipótesis descartadas y su falsador

| Hipótesis | Falsada por |
|---|---|
| Dos requests HTTP de deploy | cada deploy crea su propio group (`UUID.randomUUID()`) y su propia execution; ambas filas comparten los dos |
| Redelivery duplicado del mismo result | `findByDeploymentCorrelationId` es `PESSIMISTIC_WRITE`; el segundo ve el run terminal y descarta antes de publicar el evento |
| Retry interno creó la fila | `DeploymentTimeoutJob` reusa la fila (`:207-211`), no inserta |
| Dos `ComponentRun` duplicados | `uq_cr_execution_component` enforced |
| El control plane creó la duplicidad | la fila nace en playmaker antes del publish; el CP no inserta |
| Paths legacy y moderno sobre el mismo service | `createSingle` crea group propio con `pipelineExecution=null` |

Confianza en la hipótesis principal: **0.97**. El 3 % restante requiere los logs de los dos listeners.

### Estado de los tests

No hay **ningún** test de concurrencia en el repo. `DeploymentGroupServiceImplTest` afirma `times(1)` sobre un mock en un solo hilo, o sea verifica la propiedad violada exactamente donde no puede fallar.

Y la DB de test es H2 en `MODE=MySQL` con `ddl-auto: create-drop`, sin Testcontainers. Dos consecuencias: H2 no reproduce con fidelidad locks de fila ni índices únicos de InnoDB, y `create-drop` genera el schema desde las **entidades**, así que un `@UniqueConstraint` puesto sólo en la entidad **pasa los tests y no existe en producción**. Testcontainers MySQL 8 es precondición, no mejora.

### Matriz de alternativas

Criterios: intra-execution · cross-execution · redelivery · atomicidad sin fila previa · crash consistency · retries legítimos · schema · API · contención · observabilidad · testabilidad · rollout.

| Opción | Intra | Cross | Crash | Costo principal |
|---|---|---|---|---|
| Claim CAS `PENDING→DISPATCHING` | **Sí** | No | parcial, necesita reaper | valor nuevo de enum, 2 releases |
| `SELECT FOR UPDATE` sobre execution | **parcial** | No | No | contención por execution |
| UNIQUE (group, service) | backstop fuerte | No | No | `ALTER` + preflight |
| UNIQUE activo por service (columna generada) | backstop | **Sí** | No | `ALTER` + preflight |
| Mutex KVS por data product | Sí | Sí | **mal**: falla cerrado y pierde el avance | no-op en perfiles de test |
| Serializar consumo por partición | Sí | No | No | depende del transporte, no verificado |
| Sólo merge en lectores | **No** | No | No | oculta la corrupción sin métrica |
| Claim en tabla `batch_execution` | Sí | No | mejor | tabla nueva |

Ninguna opción aislada cubre intra + cross + crash. La composición es obligatoria, no estética.

### Recomendación

Cuatro capas separadas por responsabilidad.

1. **Fix funcional:** claim atómico por CAS (`UPDATE component_run SET status='DISPATCHING' WHERE pipeline_execution_id=? AND run_order=? AND status='PENDING'`, despachar sólo lo reclamado, el perdedor observa 0 filas y retorna con métrica en DEBUG, no ERROR) más el `SELECT ... FOR UPDATE` sobre `pipeline_execution` para la interleaving claim-vs-cancel. Se agregan dos correcciones: un intento superseded no debe decidir el destino terminal del run (`DeploymentResultHandlerImpl.java:313-321` y `:352-361` hoy no consultan `superseded`), y una violación de integridad nunca debe traducirse a componente FAILED.
2. **Backstop en DB:** `UNIQUE(deployment_group_id, service_id)` para la idempotencia del intento lógico — clave determinista, derivable antes del INSERT, que permite al perdedor releer al ganador — más `UNIQUE` sobre columna generada `IF(is_active=1, service_id, NULL)` para el caso cross-execution, porque MySQL no tiene índices parciales. Hay precedente de columnas generadas y de unicidad como red anti-carrera en el propio repo.
3. **Hardening de lectores:** merge determinista con contador y alarma en los dos `toMap` y en los 8 `Optional`. La métrica no es opcional: sin ella esto oculta la corrupción.
4. **Reparación de datos:** conservar el intento que el control plane reconoce como dueño del recurso vivo, no el de mayor `id`. Para el incidente concreto, dejar `6421` activo y desactivar `6422`, más reconciliar la app Kinesis Analytics huérfana.

**Requisito no negociable:** hoy el avance de batch es *at-most-once sin recuperación*. `createDeploymentAttempt` deja `timeout_at = NULL` y sólo el publish async lo setea (`BigQueueDispatchAdapter.java:54-63`), así que el predicado del job de timeout nunca ve una fila cuyo publish no corrió; y el `try/catch` del listener loguea y descarta. Un crash entre el commit del result y el publish deja la execution pegada para siempre. Hace falta un reconciliador periódico, no como extra sino como parte del fix.

### Rollout propuesto

| Etapa | Contenido | Criterio de salida |
|---|---|---|
| 0 | hardening de lectores + métrica + alarma, primero por urgencia: el estado corrupto bloquea GET, PATCH de config y el propio deploy | 500s en cero |
| 1 | preflight de duplicados en los tres ambientes + reparación + reconciliación en el CP | 0 duplicados |
| 2 | `DISPATCHING` agregado al enum y tolerado en todos los guards, **sin productor** | desplegado en todas las instancias |
| 3 | claim + `FOR UPDATE` + las dos correcciones. Sin feature flag: un claim a medias es peor que ninguno | suite concurrente verde contra MySQL real |
| 4 | los dos UNIQUE + índice `(service_id, is_active)` | `ALTER` aplicado |
| 5 | reconciliador | recupera un caso inyectado en staging |

La etapa 2 antes de la 3 es por rolling deploy: una instancia vieja que vea un run en `DISPATCHING` lo filtra de `nextBatch` y cae en `checkGroupCompletion`, que retorna sin daño — es compatible, pero el valor del enum tiene que estar liberado antes de producirse.

### Contraste con el diagnóstico previo

Convergencia independiente en 8 puntos, incluido el regresor `dac615f47` y la formulación "condición de nivel no consumida". Eso subió la confianza de 0.90 a 0.97.

El diagnóstico previo aportó toda la evidencia de DB y timestamps, y un dato que obligó a degradar una afirmación de la fase 1: el otro componente de run_order 1 (`jarita-signal-test`) **completó bien**, así que "ambos se duplicaron" queda como hipótesis no verificada.

La auditoría aportó, entre otros: el hueco residual del lock; que `validateActiveDeployments` corre fuera del try/catch per-item y aborta el batch entero; el `is_active=false` de `DeploymentDispatchEventListener`; el mismo `toMap` en el camino de deploy; el radio de impacto cuantificado; el `timeout_at=NULL` que hace irrecuperable el crash post-commit; la ausencia total de tests de concurrencia; y la trampa de H2 más `create-drop`.

Corrección sobre la deuda conocida: los dos DEBT de `meli/backlog.md:57-63` y `:65-71` están redactados en clave **cross-execution** y **ninguno describe el doble avance intra-execution**; uno apunta a un método que ya no existe y ambos proponen un índice parcial que MySQL no soporta.

### Preguntas abiertas

1. ¿El service de `component_id=8210` también tiene dos intentos en el group del incidente?
2. ¿Existen dos logs `Dispatched next batch` con `order=1` para esa execution? Es el falsador de la hipótesis principal.
3. ¿Sigue viva la app Kinesis Analytics de `6421`?
4. Autoridad final ante conflicto: ¿playmaker o el control plane? Sin eso la política de reparación no es decidible.
5. ¿Hubo recursos duplicados facturables en control planes no-Flink, donde el doble PROVISION pudo ser silencioso?
6. Isolation level efectivo, topología primary/replica y versión de MySQL en producción.
7. ¿Apareció un fix en `origin` después del 2026-08-20 23:29? Requiere autorización para `git fetch`.
8. ¿`origin/feature/kvs-actions-segmented-test-scopes` está abandonada? Lleva sin mergear desde el 2026-06-22.

## Fuentes

- Repo `rio-playmaker`, rama `develop`, HEAD `0524ce49ef34`. Rutas relativas al root del repo en [[Fuentes — Workspace de repositorios]].
- Clases: `OrchestrationServiceImpl`, `BatchCompletedEventListener`, `BatchDispatchServiceImpl`, `DeploymentResultHandlerImpl`, `DeploymentDispatchEventListener`, `BigQueueDispatchAdapter`, `PipelineServiceImpl`, `DeltaComputationServiceImpl`, `DeploymentTimeoutJob`, `DeploymentRepository`, `PipelineDeployServiceImpl`, `DeploymentGroupServiceImpl`.
- Migraciones: `20250327184420740_init_schema.sql`, `20260602144356125_create_sig186_domain_tables_prod.sql`, `20260514174340301_create_pipeline_versioning_tables_prod.sql`, `20250916172537419_add_semver_into_component_definition_table.sql`.
- Commits: `dac615f47` (trigger, PR #1047), `d1741b89a` (versión inline previa), `adf5cf54f` (fix del roll-up no mergeado), `4fe8f47ae`, `2fe774fdc`, `54aaa9160` (PR #934), `1b6706d8d`.
- Deuda: `meli/backlog.md`, `DEBT-SIG186-CONCURRENT-DEACTIVATE` y `DEBT-SIG326-DISPATCH-ACTIVE-RACE`.
- Evidencia de DB, timestamps y stacktrace del incidente: [[Playmaker — Doble dispatch al avanzar batches]], sección "Evidencia entregada".
