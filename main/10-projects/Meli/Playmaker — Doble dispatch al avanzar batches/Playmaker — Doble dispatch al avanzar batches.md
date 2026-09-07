---
type: project
schema_version: 1
owner: me
root: true
status: active
priority: P1
area: "[[Meli]]"
parent:
sprint:
start: 2026-08-21
due:
progress: 99
repo: https://github.com/melisource/fury_rio-playmaker
jira:
prs: https://github.com/melisource/fury_rio-playmaker/pull/1101
application: "[[rio-playmaker]]"
aliases:
  - Race de doble dispatch en Playmaker
  - Deployments activos duplicados en Playmaker
  - Duplicate key service deployment
  - Bug de avance de batches SIG-186
tags:
  - kind/project
  - area/meli
  - project/playmaker-double-dispatch
  - app/rio-playmaker
  - priority/p1
created: 2026-08-21
updated: 2026-09-02
---

# Playmaker — Doble dispatch al avanzar batches

> [!info]+ Estado de la investigación
> **Área:** [[Meli]] · **Aplicación:** [[rio-playmaker]] · **Estado:** active · **Prioridad:** P1  
> **Repo observado:** `~/fuentes/rio-playmaker` · rama `develop` · snapshot `0524ce49ef34` · 2026-08-21  
> **Diagnóstico preliminar:** alta confianza, todavía sujeto a reproducción concurrente y contraste independiente.  
> **Importante:** esta nota conserva el análisis previo como evidencia secundaria; no reemplaza una auditoría desde el código y los datos.

## 🎯 Objetivo

- Determinar con evidencia reproducible por qué una misma ejecución de pipeline puede crear dos intentos de deployment activos para el mismo `service_id` al avanzar entre batches topológicos.
- Elegir una solución que haga idempotente y consistente el avance del batch, conserve el historial legítimo de redeploys y proteja el invariante global de un único deployment vigente por service.
- Diseñar y validar primero el hotfix sin schema/estados nuevos; tratar migraciones, recuperación durable y rollout amplio únicamente dentro del refactor final aprobado.
- Evitar dos errores de enfoque: parchar únicamente los registros afectados y ocultar la corrupción en las lecturas.

## 📊 Estado actual

### Follow-up de robustez listo en PR #1101

La rama `feature/harden-batch-advance-lock` quedó sincronizada y pusheada en `a1c097467`. El [PR #1101](https://github.com/melisource/fury_rio-playmaker/pull/1101) resuelve los tres pendientes posteriores al PR #1079: renueva el lease de Fury Lock cada `TTL / 3`, valida ownership inmediatamente antes de la transacción fresca, conserva el token renovado para liberar y reemplaza el coalescing compartido por una cadena de retry independiente para cada señal. El fallback ante indisponibilidad de LockaaS sigue siendo deliberadamente graceful; una pérdida de ownership confirmada sí aborta antes del dispatch y reintenta.

Validación final: `./gradlew check jacocoTestReport bootJar --no-daemon` pasó con 3.436 tests, 0 fallos, 0 errores y 2 skipped. La CI 5101 y todos los checks del PR quedaron verdes. Melicov reportó 98,94% de cobertura del PR en `a1c097467`, sobre el mínimo personal de 95%; `BatchAdvanceFuryLock` quedó en 100% del diff local y desapareció de la lista remota de archivos incompletos. Riesgo residual explícito: no existe fencing durable en DB y, durante una caída de LockaaS, el fallback conserva el comportamiento previo sin serialización.

### Reemplazo Fury Lock — namespace corregido; `0.0.18-listener-lock` en creación

El commit `93550f7c6d43` en `feature/serialize-batch-completed-listener` deja Fury Lock como única exclusión distribuida, con TTL de 5 s, retry temporal de 7 s y comportamiento fail-closed: ante contención o indisponibilidad nunca ejecuta `checkNextBatch` sin lock. El stack compatible queda en `lockclient:5.0.0`, Workqueues `4.0.0` y KVS `0.7.4`; la inicialización lazy de Workqueues elimina la heurística por prefijo de scope y permite levantar scopes que no usan upload-jar. La validación runtime de [`0.0.17-listener-lock`](https://web.furycloud.io/rio-playmaker/versions/detail/0.0.17-listener-lock) en `bq-consumer-test-nonprod` demostró que la aplicación levanta y que el listener falla cerrado, pero también reveló un namespace incorrecto introducido por la implementación: configuraba `rio-playmaker-batch-advance`, mientras el servicio LockaaS existente en nonprod y nonsite se llama `batch-advance`. Lockclient 5 agregó el segmento y buscó el namespace inexistente `rio-playmaker-batch-advance-nonprod`; por eso no encontró `locks.json` ni el fallback. La corrección usa el constructor oficial `new LockApiClient()` y el namespace `batch-advance`, sin lógica por scope; 25 tests dirigidos y los 2 tests concurrentes pasan. El commit quedó pusheado con la rama sincronizada y Fury aceptó [`0.0.18-listener-lock`](https://web.furycloud.io/rio-playmaker/versions/detail/0.0.18-listener-lock), actualmente en creación. Falta esperar el build y validar el runtime.

### Decisión vigente — hotfix acotado + refactor durable

> [!warning] HOTFIX IMPLEMENTADO, PUSHEADO Y VERSIONADO — build y validación runtime pendientes
> La dirección vigente separa dos entregas. El hotfix usa Fury Lock por `pipelineExecutionId + nextBatchOrder`, TTL de 5 s, retry coalescido durante 7 s y fail-closed ante contención o indisponibilidad. Después de adquirir el lock, relee estado y deployments del group; si el batch ya fue materializado termina en no-op. La aplicación levanta sin condiciones basadas en `SCOPE` y el cliente debe usar el nombre registrado `batch-advance`; Lockclient resuelve automáticamente `batch-advance-nonprod` o `batch-advance-nonsite`. El segundo track sigue siendo un mecanismo durable externo con entrega recuperable y procesamiento idempotente. Cualquier referencia posterior a mutex QKVS, lock MySQL, fallback fail-open o `ComponentRun.DISPATCHING` pertenece a enfoques históricos y queda **SUPERSEDED**.

#### Rama y artefactos

- **Rama implementada y remota:** `feature/serialize-batch-completed-listener`, sincronizada en `93550f7c6` (`fix: use registered batch advance lock namespace`).
- **Versión Fury más reciente:** [`0.0.18-listener-lock`](https://web.furycloud.io/rio-playmaker/versions/detail/0.0.18-listener-lock), aceptada desde `93550f7c6` y actualmente en creación; corrige el namespace a `batch-advance`.
- **Versión Fury:** [`0.0.9-listener-lock`](https://web.furycloud.io/rio-playmaker/versions/detail/0.0.9-listener-lock), finalizada correctamente desde `f7d4f4881` con tests habilitados. El primer build 1534 terminó en error y el único retry idempotente posterior quedó exitoso.
- **PR actualizado:** [#1079](https://github.com/melisource/fury_rio-playmaker/pull/1079), con descripción revisada por Zord, todos los checks verdes y evidencia de 3.232 tests: el control sin lock reproduce 2 dispatches y el flujo con lock verifica exactamente 1.
- **Rama histórica que no debe promoverse:** `feature/adhoc-double-dispatch`; contiene el enfoque `DISPATCHING` deprecado y no representa la solución vigente.
- **PR #1064:** referencia histórica del proyecto; no debe presentarse como implementación del nuevo approach mientras conserve `DISPATCHING`.
- **Regla para el implementador:** partir desde la base autorizada y construir el hotfix sin reutilizar código o migraciones del enfoque deprecado; si se decide reciclar una rama existente, primero eliminar completamente `DISPATCHING` y verificar el diff contra la base.

#### Alcance exacto del hotfix

- Resolver únicamente la carrera intra-execution observada: dos `BatchCompletedEvent` legítimos, originados por componentes distintos del mismo batch, no pueden ejecutar en paralelo la evaluación/materialización del batch siguiente.
- No agregar tablas, columnas, constraints, entidades JPA, estados de `ComponentRun`, eventos públicos ni cambios en contratos de CP.
- No cambiar el consumer HTTP de deployment results ni devolver `409`: serializar ahí no cubre los listeners `AFTER_COMMIT + @Async`, y un error del listener interno no reencola el mensaje BigQueue ya reconocido.
- No modificar Kafka, Flink, ClickHouse ni Fury como parte del parche. Su idempotencia por `deployment_id` continúa como backstop downstream y no resuelve dos IDs distintos creados por Playmaker.
- No cambiar el comportamiento normal del pipeline. La única diferencia observable debe ocurrir en la interleaving duplicada: el segundo listener espera, relee estado fresco y termina como no-op idempotente si el batch ya fue materializado.
- No prometer solución cross-execution, unicidad global por `service_id`, recuperación durable de eventos Spring ni confirmación durable del publish a BigQueue; esos límites pertenecen al refactor final.

#### Diseño del hotfix

##### 1. Ubicación del lock

El lock debe envolver `BatchCompletedEventListener.onBatchCompleted`, porque ése es el punto exacto donde dos eventos internos pueden ejecutar simultáneamente `checkPrerequisites`. Un lock en `DeploymentResultConsumerServiceImpl` sólo serializaría el procesamiento previo: después de cada commit se publicarían dos eventos Spring que volverían a competir en el pool async.

##### 2. Identidad del lock

Usar una clave distribuida estable por transición de batch:

```text
batch-listener-lock:<pipeline_execution_id>:<next_batch_order>
```

No usar `run_id`, `deployment_id` ni `service_id`: los dos eventos competidores tienen runs y deployments distintos, pero comparten execution y próximo batch. Agregar un prefijo versionado si el container KVS es compartido, por ejemplo `playmaker:v1:batch-listener-lock:`.

##### 3. Primitive KVS

- Implementar adquisición create-only con versión inicial `0`, siguiendo el primitive ya probado conceptualmente por `DataProductActionLockImpl`.
- Guardar un `ownerToken` único por invocación y limitar el TTL del lease a 10 segundos para evitar locks huérfanos prolongados.
- Tratar tanto `CONFLICT` como indisponibilidad KVS como adquisición fallida y agendar un retry acotado; nunca continuar fail-open porque volvería a habilitar la carrera.
- Liberar en `finally` sólo si el owner coincide. Si el SDK ofrece delete/update condicionado por versión, preferirlo; un `get owner` seguido de `delete` simple conserva una ventana ABA y debe quedar explícitamente aceptado o corregido.
- No mantener una transacción ni conexión MySQL mientras se espera el lock.

##### 4. Retry agendado y backoff

- `tryAcquire()` hace un único intento. Si el lock está ocupado, el listener agenda un callback mediante `CompletableFuture.delayedExecutor` y devuelve inmediatamente el worker al pool.
- Usar exponential backoff con full jitter: `delay = random(0, min(cap, base * 2^attempt))`, con base 100 ms, cap 1 segundo y máximo 10 retries.
- Coalescer localmente un único retry pendiente por `(executionId, nextBatchOrder)` en cada instancia para evitar timers redundantes.
- No se mantiene una transacción, conexión DB ni thread de aplicación durante el delay; un worker se utiliza nuevamente sólo cuando vence el timer y ejecuta el siguiente intento.
- El scheduler y el evento siguen siendo in-memory y el retry es deliberadamente finito. Un restart o agotamiento deja una señal ERROR y requiere un nuevo completion event o recuperación manual; el refactor con tópico externo debe eliminar esta limitación.

##### 5. Orden transaccional obligatorio

1. Hacer una lectura corta del `ComponentRun` para obtener `pipeline_execution_id` y `run_order`; cerrar esa transacción antes de esperar.
2. Calcular `next_batch_order = run_order + 1` y adquirir el lock KVS fuera de cualquier transacción DB.
3. Después de adquirirlo, abrir una transacción `REQUIRES_NEW` nueva.
4. Releer `ComponentRun` y `Deployment` por ID dentro de esa transacción; no reutilizar entidades/snapshots obtenidos antes de la espera.
5. Recalcular prerequisites, estado de execution, current batch y next batch desde DB fresca.
6. Ejecutar el chequeo idempotente de materialización descrito abajo.
7. Sólo si el batch no está completamente materializado, llamar al flujo actual `dispatchBatch` sin cambiar su semántica.
8. Hacer commit y recién después liberar el lock en `finally`.

Este orden es obligatorio: si la transacción se abre antes de esperar, una vista consistente previa podría no observar el commit del ganador; si el lock se libera antes del commit, el segundo listener puede entrar antes de que las filas sean visibles.

##### 6. Cómo reconocer que batch N+1 ya fue materializado

No usar `ComponentRun.status` como evidencia: los runs enviados permanecen `PENDING` hasta recibir `STARTED`, por lo que el mismo predicado seguiría verdadero después del primer dispatch.

Usar únicamente datos existentes:

1. Resolver `groupId` desde el deployment/evento actual.
2. Calcular los component IDs de los runs `PENDING` del `next_batch_order` después de adquirir el lock.
3. Leer `deploymentRepository.findByDeploymentGroupId(groupId)`.
4. Derivar los component IDs materializados mediante `deployment.service.componentId`.
5. Si todos los componentes PENDING del próximo batch ya aparecen entre los deployments del group, registrar `already_materialized` y retornar normalmente sin volver a llamar `dispatchBatch`.
6. Si no todos aparecen, ejecutar el dispatch normal y conservar la semántica existente de `dispatchBatch`, incluidas sus fallas parciales por componente.

La existencia de la fila demuestra que el intento fue materializado, no que BigQueue confirmó el publish. El primer `DeploymentDispatchRequestedEvent` sigue siendo responsable de transportar el trigger después del commit. Sin un marcador durable de publicación no es posible distinguir con certeza “publish aceptado” de “fila creada y listener aún pendiente”. Para evitar duplicados, el boundary del hotfix es deliberadamente `deployment materializado`.

##### 7. Archivos y cambios esperados

- `BatchCompletedEventListener.java`: intentar adquirir/liberar el lock; agendar contention sin bloquear; separar lectura de contexto y transacción fresca; mantener el catch externo sin convertir la carrera esperable en error de negocio.
- `OrchestrationServiceImpl.java`: agregar el chequeo idempotente `all/none` antes de `dispatchBatch`; no mutar statuses.
- `DeploymentRepository.java`: reutilizar `findByDeploymentGroupId`; no agregar schema ni consultas de escritura.
- Nuevo helper/interfaz no persistente para el mutex de avance de batch, reutilizando el `KvsClient`/container disponible con namespace propio. No crear entidad JPA.
- Configuración: base/cap del backoff, TTL máximo de 10 segundos y máximo 10 retries. Las cifras deben contrastarse con la duración real de la sección crítica en staging.
- Tests: unitarios con KVS fake versionado y test concurrente con dos eventos de runs distintos del mismo batch; verificar un solo `dispatchBatch`, espera real del perdedor, relectura posterior al ganador, `already_materialized`, KVS temporalmente indisponible y liberación owner-safe.

#### Pros y contras del hotfix

**Pros**

- Diff acotado al punto exacto de la carrera.
- Sin migraciones, entidades persistentes, estados públicos ni coordinación con todos los CPs.
- Mantiene el happy path y permite que el segundo listener espere en vez de descartarse.
- Cross-pod si KVS está correctamente configurado.
- El perdedor puede observar el commit del ganador mediante deployments existentes del mismo group, incluso si el deployment ya llegó a estado terminal.

**Contras y límites aceptados**

- El evento Spring sigue siendo in-memory: un restart puede perderlo.
- Existe la ventana histórica entre commit de deployment y ejecución/publish del `DeploymentDispatchRequestedEvent`; la fila no prueba confirmación de BigQueue.
- Los retries son in-memory, finitos y no FIFO; una caída de instancia o contention superior a la ventana de retry puede dejar una transición pendiente.
- TTL incorrecto o release no atómico puede permitir overlap; KVS pasa a ser dependencia fail-closed del avance.
- No protege dos executions diferentes que compiten por el mismo service ni establece unicidad global.
- No repara datos existentes ni resuelve la semántica ambigua de `is_active`.

#### Refactor durable, robusto y escalable

El segundo approach reemplaza el evento Spring interno como frontera de entrega por un tópico externo durable de avance de batches. Debe diseñarse en SPEC funcional y SPEC técnica separadas del hotfix.

Flujo objetivo:

1. El result handler persiste el resultado y produce durablemente un comando/evento `BatchAdvanceRequested` después del estado terminal; para cerrar la dual-write DB→topic debe usarse transactional outbox o un mecanismo equivalente con garantía demostrable.
2. El tópico se particiona por `pipeline_execution_id`, preservando orden por execution y permitiendo escalar horizontalmente entre executions.
3. El consumer externo recalcula prerequisites desde DB y usa una identidad estable de transición `(execution_id, next_batch_order)` para procesar at-least-once sin volver a materializar deployments.
4. La lógica que verifica prerequisites y crea los deployment attempts debe ser atómica y consistente; el transporte posterior reutiliza una identidad/correlation ID estable en cada retry.
5. La solución final debe proteger además el invariante cross-execution de máximo un deployment vigente por service mediante una autoridad transaccional de dominio, no mediante locks ad hoc en cada CP.
6. Reintentos, takeover, DLQ/reconciliación, replay y observabilidad deben ser parte del contrato, no callbacks best-effort.
7. Los CPs mantienen idempotencia del mismo comando como backstop; no deben inferir identidad de batch de Playmaker.

**Pros**

- Entrega durable y recuperable ante restart/crash.
- Orden por execution sin bloquear threads del pool web/async de Playmaker.
- Escalabilidad horizontal natural por particiones.
- Replays y retries explícitos, observables y testables.
- Permite cerrar de forma coherente las ventanas DB→publish y cross-execution.

**Contras**

- Refactor de mayor alcance: contrato de evento, tópico, consumer, outbox/equivalente, idempotencia persistente, rollout y operación.
- Requiere acordar ownership, identidad lógica, retención, retry/DLQ, reconciliación y autoridad del active slot.
- No es apropiado como hotfix inmediato y necesita aprobación/planificación del equipo.

#### Mensaje propuesto al equipo

> Amigos, estuve cerrando la investigación del doble deployment que vimos al avanzar entre batches en Playmaker. La causa está en que dos resultados `COMPLETED` legítimos del mismo batch pueden generar dos `BatchCompletedEvent` y ejecutar en paralelo el listener que materializa el batch siguiente.
>
> El approach anterior basado en `ComponentRun.DISPATCHING` queda descartado. Cambia el lifecycle público, abre recuperación adicional ante crashes y termina resolviendo la carrera en un nivel que no corresponde.
>
> Les propongo avanzar en dos etapas complementarias:
>
> **1. Hotfix acotado**
>
> Rama propuesta: [`hotfix/serialize-batch-completed-listener`](https://github.com/melisource/fury_rio-playmaker/tree/hotfix/serialize-batch-completed-listener)
>
> - Serializar únicamente el `BatchCompletedEventListener` con un lock distribuido KVS por `pipeline_execution_id + next_batch_order`.
> - Si otro listener ya está trabajando, el segundo espera con exponential backoff y jitter; no se descarta el evento.
> - Cuando obtiene el lock, abre una transacción nueva, relee DB y verifica mediante los deployments existentes del mismo group si el batch siguiente ya fue materializado. Si ya existe, termina como no-op; si no existe, sigue el flujo actual.
> - No agrega tablas, columnas, entidades, estados ni cambios en los CPs, y no modifica el comportamiento normal de los pipelines.
>
> Este parche cubre específicamente la carrera intra-execution observada. Sus límites son conocidos: el evento Spring sigue siendo in-memory, no entrega confirmación durable del publish y no resuelve competencia entre executions diferentes.
>
> **2. Refactor durable y escalable**
>
> Propongo que acordemos como solución definitiva reemplazar el listener interno por un tópico externo de avance de batches, particionado por execution, con publicación recuperable, consumo at-least-once e idempotencia/lógica atómica que garantice una sola materialización por transición. Ese diseño también debe cerrar explícitamente la unicidad cross-execution por service y las ventanas de crash entre DB y transporte.
>
> Mi propuesta es promover primero el hotfix después de validar la concurrencia en staging y, en paralelo, abrir el SPEC funcional/técnico del refactor durable. Les agradecería feedback/aprobación sobre esta dirección antes de comenzar el segundo track.
>
> ¿Cómo lo ven?

### Revisión CP/KVS — 2026-08-25

- La revisión comparativa quedó documentada en [[playmaker-deployment-idempotency-and-cp-kvs]]. Kafka y Flink usan un guard KVS con `deployment:<deployment_id>`, create-only, TTL, stale takeover y finalize CAS; ClickHouse tiene estado KVS pero su `claimStart` no está cableado al flujo y `synchronized(this)` no protege entre pods; Fury converge por natural key + `specHash`.
- Conclusión aplicable al fix: el CP sólo puede deduplicar redelivery del mismo `deployment_id`. No puede impedir la duplicidad observada entre `6421` y `6422`; Playmaker debe resolver la identidad del avance lógico y el invariante cross-execution de un único activo por service.
- La dirección vigente separa el hotfix intra-execution descrito arriba del refactor durable. Los cambios de reserva/constraint por service no forman parte del parche y deberán resolverse en el diseño final. `PENDING → DISPATCHING` queda deprecado por completo, no sólo como solución insuficiente.

> [!warning] DEPRECATED — enfoque `DISPATCHING`
> El claim `PENDING → DISPATCHING` del commit `e17215f2d` queda **deprecado y no debe considerarse la solución acordada**. El equipo determinó que el problema debe analizarse en la multiplicidad y concurrencia de los listeners async (`BatchCompletedEvent`), no en introducir un estado persistente adicional en `ComponentRun`. Mantener las referencias siguientes sólo como historial de investigación; cualquier diseño futuro debe partir del flujo de listeners y resolver recuperación/idempotencia en el nivel correcto.

- **Auditoría independiente ejecutada y contrastada.** El informe es [[Auditoría independiente — Informe del doble dispatch]]; la barrera anti-anclaje se cumplió (fase 1 congelada y hasheada antes de abrir esta nota, checksum verificado antes y después).
- Causa raíz confirmada desde código: el avance de batch actúa sobre una condición de nivel sin consumirla, y el dispatch no transiciona el `ComponentRun`, así que el predicado sigue verdadero después de haber actuado.
- Regresor confirmado con el diff: `dac615f47` (PR #1047, en develop 2026-08-19) movió `checkPrerequisites` de inline-en-transacción a `AFTER_COMMIT` + `@Async` + `REQUIRES_NEW`. Invirtió la carrera de *nadie avanza* a *todos avanzan*. Confianza **97 %**; falta sólo el falsador de logs.
- Precisión que cambia qué testear: lo asíncrono **no** es la lectura de los results — ese camino sigue sincrónico y serializado por lock pesimista por fila. Hay que reproducir dos COMPLETED de componentes distintos del mismo batch.
- Daño mayor que el crash: el resultado FAILED del intento espurio marcó FAILED al run legítimo y tumbó group y execution, dejando una app Kinesis Analytics huérfana en AWS.
- La corrupción es pegajosa: el redeploy desactiva sólo una de las filas activas y crea otra, así que el conteo de activos por service nunca baja. El segundo deploy no la creó, sólo la dejó a la vista.
- El estado corrupto es autobloqueante: el mismo `toMap` sin merge está también en el camino de deploy, así que no se puede re-deployar ni editar la config para salir.
- El enfoque `DISPATCHING` fue implementado experimentalmente en `feature/adhoc-double-dispatch`, pero queda **deprecado**: no se debe promover, desplegar ni usar como recomendación.
- La razón de la deprecación es que agrega un estado persistente para tapar una carrera del listener y abre una deuda de recuperación ante crash/error entre el claim y el transporte. El análisis vigente debe concentrarse en los listeners async que reaccionan a múltiples `BatchCompletedEvent` legítimos.
- El historial de tests, schemas y riesgos de rollout de `DISPATCHING` se conserva sólo para poder auditar la decisión; no representa el diseño objetivo.

>[!note]+ Secciones 1–14: diagnóstico anterior a la auditoría
> Se conservan tal cual como evidencia del análisis inicial y de la barrera anti-anclaje. Donde difieran del informe, manda [[Auditoría independiente — Informe del doble dispatch]], que registra las correcciones puntuales y qué encontró cada análisis por separado.

## 🔬 Revisión del PR #1079 — evaluación de los comentarios y guía de resolución

> [!info]+ Alcance y método
> **PR:** https://github.com/melisource/fury_rio-playmaker/pull/1079 · rama `feature/serialize-batch-completed-listener` · base `origin/develop@28b929c9e` · revisor: dmuena_meli · veredicto recibido: *request changes*.
> **Método de esta evaluación:** se contrastó el diff de `origin/feature/serialize-batch-completed-listener@1eb04d0c` contra la base y contra el código que consume el lock. Los hechos de infraestructura requieren además evidencia de Fury; la configuración del repo por sí sola no prueba que un container exista o no exista.
> **Decisión de rollout (2026-08-26):** el hotfix ya se probó con el QKVS compartido en `test2` y `bq-consumer-test-nonprod`; no se ampliará el alcance a `stage`/`staging-nonprod`. Ante indisponibilidad real de KVS, el fallback acordado es fail-open controlado: registrar la señal y ejecutar el comportamiento pre-hotfix, sin mutex. Un lock ocupado sigue reintentando hasta el deadline.
> **Estado de implementación (2026-08-27):** cambios aplicados, validados, commiteados y pusheados como `b20aa2474` en `origin/feature/serialize-batch-completed-listener`.

### Veredicto por hallazgo

| # | Hallazgo | Veredicto / decisión | Estado al 2026-08-27 |
|---|---|---|---|
| C1 | El presupuesto de reintentos vence antes que el TTL | Aplica. TTL en 7 s y probe final monotónico no anterior al primer conflicto + TTL + 100 ms. | **Aplicado** |
| C2 | Reinvención de `DataProductActionLock` + TTL sin validar | Aplica como deuda/riesgo; no se generaliza el lock en este hotfix. | **Matiz:** métricas aplicadas; `KvsMutex` queda aparte |
| H1 | `"VERSION_CONFLICT"` no existe en el SDK | Aplica. Se usa `ErrorCode.CONFLICT.getCode()`. | **Aplicado** |
| H2 | KVS real en stage / staging-nonprod | No aplica al rollout. QKVS validado en `test2` y `bq-consumer-test-nonprod`. | **No se aplica** (YAGNI) |
| M1 | TTL puede expirar a mitad de transacción | Aplica como riesgo operacional; no hay renovación/fencing en este hotfix. | **Matiz:** histograma de hold; observar p99/p99.9 |
| M2 | Una sola cadena de retry puede hacer starvation | Aplica sólo por C1/scheduler. Se mantiene una cadena local coalescida. | **Aplicado**: deadline final y fallback si falla scheduler |
| M3 | Materialización parcial re-despacha el batch | Aplica. Se despacha sólo el subconjunto pendiente. | **Aplicado** |
| M4 | El test concurrente no usaba el lock real | Aplica. Se añadió carrera contra `BatchAdvanceLockImpl` y fake KVS create-only. | **Aplicado** |
| L1 | Argumentos/códigos de `KvsClientException` en tests | Aplica. | **Aplicado** |
| L2 | `attempts` / `waitedMillis` muertos | Aplica. `LockHandle` queda con key y owner. | **Aplicado** |
| L3 | Cambio de `kvs.segment` fuera del alcance | Aplica como documentación del PR, no como cambio de código. | **Pendiente:** declararlo en el PR |
| INFO | `IllegalStateException` en `componentIdOf` | INFORMATIONAL | Las relaciones persistidas son no nulas; el fail-closed es preferible a ignorar una fila que podría representar materialización existente. | No cambiar en este PR |
| SEC | `ThreadLocalRandom` en vez de `SecureRandom` para el jitter | no bloqueante | No es dato sensible ni límite de seguridad. Cambiarlo sólo si un gate concreto lo exige. | No aplica como hallazgo de seguridad |

### Lo que esta evaluación agrega o corrige respecto del review recibido

- **Decisión H2 / YAGNI.** La configuración de `stage` y `staging-nonprod` no pertenece al rollout elegido. `test2` y `bq-consumer-test-nonprod` ya ejercieron el QKVS compartido de los segmentos `nonprod`/`nonsite`; se mantiene ese recurso y namespace. No se agrega fallback No-Op ni se modifica infraestructura fuera de esos scopes.
- **C1 es peor por un motivo estructural, no por el número.** El review compara 7,5 s de reintentos contra 10 s de TTL. El problema de fondo es que los topes *hardcodeados* del código (`MAX_BACKOFF_CAP_MILLIS = 1000`, `MAX_RETRIES = 10`) hacen que el horizonte máximo alcanzable sea 10 s en el peor caso y ~5 s en el esperado. Es decir: **la configuración correcta es inalcanzable sin tocar las constantes.** No hay valor de las variables de entorno que arregle esto.
- **La transacción de dispatch está mejor acotada de lo que sugiere el review.** El envío al control plane no ocurre dentro de la transacción: `BatchDispatchServiceImpl.dispatchItem` publica un `DeploymentDispatchRequestedEvent` y `DeploymentDispatchEventListener` lo consume en `AFTER_COMMIT` + `@Async`. La transacción es DB + parsing (`ParameterResolutionService` no tiene clientes remotos). Eso no invalida M1 ni C2, pero cambia la conversación: el riesgo es de *cola de latencia de DB y tamaño de batch*, no de un round-trip HTTP. Es medible.
- **El radio de impacto de C1 es mayor que "el batch no avanza".** El lock no protege sólo el dispatch: `checkNextBatch` llama a `checkPrerequisites`, que también resuelve `propagateFailure` y `checkGroupCompletion`. Cuando se agotan los reintentos y el evento se descarta, tampoco se propaga la falla de un batch fallido ni se cierra un group terminado. Una execution puede quedar en `RUNNING` para siempre con un batch ya fallado.
- **El stall de C1 es efectivamente permanente, verificado.** `checkPrerequisites` tiene exactamente un llamador de producción: `BatchCompletedEventListener`. `DeploymentTimeoutJob` sólo actúa sobre deployments en `REQUESTED` o `STARTED`; un batch que nunca se despachó no tiene deployment, así que ningún job lo rescata.
- **M3 es un stall cuando el deployment parcial sigue activo.** El batch completo pasa por `validateActiveDeployments` antes del loop y un deployment `REQUESTED`/`STARTED` ya materializado hace fallar toda la transacción. Filtrar a los componentes faltantes es la corrección idempotente.

---

### C1 · El presupuesto de reintentos siempre vence antes que el TTL

**Verificado.** `randomBackoffMillis` calcula `upperBound = min(cap, base << intento)` y devuelve `ThreadLocalRandom.nextLong(upperBound)`, uniforme en `[0, upperBound)`. Con los defaults (`base=100`, `cap=1000`, `maxRetries=10`) los diez topes son 100, 200, 400, 800 y 1000 seis veces: **7500 ms en el peor caso, ~3750 ms esperado**. El TTL es 10 000 ms y `MAX_LOCK_TTL_SECONDS = 10` lo hardcapea. El competidor siempre se rinde antes de que el TTL pueda liberar la clave de un dueño que crasheó.

**Por qué no se arregla por configuración.** `validateRetryConfiguration` rechaza `cap > 1000` y `maxRetries > 10`. El horizonte máximo configurable es 10 × 1000 = 10 000 ms en el peor caso y 5000 ms en el esperado — sigue sin superar al TTL de forma confiable. Cualquier fix pasa por tocar código.

**Fix propuesto.** Reemplazar el presupuesto por conteo por un **deadline monotónico sólo para `CONFLICT`**. Al primer conflicto, conservar `firstContentionAt`, reintentar con backoff y garantizar un último probe no antes de `firstContentionAt + TTL + margen de scheduler`. Ante indisponibilidad KVS no se agenda retry: se registra el fallback y se ejecuta el comportamiento pre-hotfix sin mutex, decisión explícita de disponibilidad por sobre la garantía de no duplicidad durante un outage.

```java
// El timestamp se toma al primer conflicto; la antigüedad real de la lease es desconocida.
final long finalProbeAtNanos = firstContentionAtNanos + ttlNanos + schedulerMarginNanos;
if (nowNanos >= finalProbeAtNanos) { tryAcquireOnce(); }
```

Complementos necesarios:

- El conteo máximo puede seguir como protección contra tormentas, pero no puede impedir el probe final; si se alcanza antes, se agenda ese probe al deadline.
- Equal jitter es opcional: ayuda a reducir reintentos inútiles, pero el deadline —no la distribución aleatoria— es la garantía de liveness.
- **Corregir el comentario de `application.yml`**, que hoy documenta exactamente lo contrario de lo que debe cumplirse. La redacción correcta es *"el horizonte de reintentos debe superar el TTL para que el TTL funcione como backstop de crash"*.
- **Subir a WARN el log de reintentos agotados** e incluir la `transitionKey`, porque hoy es la única señal de un batch que quedó trabado para siempre.

### C2 · TTL de 10 s inventado, y duplicación del patrón de `DataProductActionLock`

**Verificado, parte A (el TTL).** `MAX_LOCK_TTL_SECONDS = 10` no tiene equivalente en el lock existente (`kvs.action-lock-ttl-seconds: 900`) y no está contrastado contra la duración real de la transacción de dispatch. La transacción incluye, por cada componente del batch: carga eager de `ServiceModel` → `ComponentDefinitionModel` → `ComponentModel`, desactivación del deployment activo previo, creación del intento, resolución de parámetros y construcción del contexto. Además `inspectNextBatchMaterialization` carga **todos** los deployments del group — no sólo los del batch siguiente — arrastrando esas mismas cadenas eager en cada avance.

**Verificado, parte B (la duplicación).** `DataProductActionLockImpl` implementa el mismo protocolo: `save` create-only con `withVersion(0)`, TTL como backstop de crash, `release` por `get` → compara owner → `delete`, y fail-closed ante `KvsClientException`. Las diferencias son de forma, no de fondo: tipo de clave (`Long` vs `String + int`), payload (JSON `{"owner":…}` vs bytes UTF-8 crudos) y retorno (`boolean` vs `Optional<LockHandle>`).

**Dónde discrepo del review.** El review recomienda consolidar sobre una versión generalizada de `DataProductActionLock` como parte de este PR. **Eso no debería bloquear el merge.** Generalizar exige extraer un `KvsMutex(String key, Duration ttl)` y reimplementar los dos call sites encima, incluyendo el lock de acciones que ya está en producción — un refactor con su propio riesgo, dentro de un hotfix P1 cuya urgencia es cerrar la duplicidad. La duplicación es deuda real, pero es deuda de forma; los dos bugs concretos que el review atribuye a haber reinventado el patrón (el código de error y el TTL) se arreglan directamente y sin consolidar nada.

**Fix propuesto.**

1. **Medir antes de cambiar el número.** Instrumentar la duración de hold del mutex y observar p99/p99.9 con el batch más grande disponible. Si se acerca al TTL, aumentar el TTL por configuración y mantener el probe por deadline de C1; la métrica detecta el riesgo, no lo elimina.
2. **Acotar la carga eager**, que es la variable que más mueve ese p99: `inspectNextBatchMaterialization` debería consultar sólo los deployments de los componentes del batch siguiente, con una proyección de `component_id` en vez de traer entidades completas.
3. **No intentar validar la garantía sólo al arrancar.** Con jitter no existe un horizonte mínimo deducible de `retries × cap`; la garantía debe estar en el scheduler como probe final dependiente del TTL.
4. **Abrir la consolidación como deuda aparte** (`KvsMutex` compartido con TTL por call site), enlazada a este PR, no dentro de él.

### H1 · `"VERSION_CONFLICT"` no existe en el SDK

**Verificado contra el bytecode.** `com.fury.toolkit.kvs.ErrorCode` tiene exactamente 13 constantes — `SERVICE_ERROR`, `NOT_FOUND`, `SERVICE_NOT_FOUND`, `KEY_TOO_LARGE`, `PAYLOAD_TOO_LARGE`, `TOO_MANY_KEYS`, `CONFLICT`, `TRANSPORT_ERROR`, `BAD_REQUEST`, `OVERQUOTA_BLOCKED`, `BLOCKED`, `SERVICE_OVERLOADED`, `OTHER` — y `CONFLICT.getCode()` devuelve `"conflict"` en minúscula. `LowLevelClient.validateHttpStatus` pasa el header `X-Kvs-Error-Code` tal cual a la fábrica de excepciones, y `ClientException` sólo cae a `ErrorCode.OTHER.getCode()` cuando el código llega nulo. `"VERSION_CONFLICT"` no se produce por ningún camino.

**Consecuencia exacta.** Cada serialización sana — el caso feliz del PR, un listener gana y el otro pierde — se loguea como `WARN "Batch listener lock KVS unavailable"`. Es decir, el PR convierte su propio éxito en una alarma de outage, y destruye la única señal que un operador usaría para distinguir contención normal de una caída real de KVS.

**Decisión adicional.** Esta corrección ya no es sólo observabilidad: el contrato debe distinguir `BUSY` de `UNAVAILABLE`. `BUSY` agenda el retry por deadline; `UNAVAILABLE` incrementa métrica y avanza inmediatamente sin lock. Mantener ambos estados como `Optional.empty()` no alcanza.

**Fix propuesto.**

```java
private static boolean isVersionConflict(final KvsClientException exception) {
  return ErrorCode.CONFLICT.getCode().equalsIgnoreCase(exception.getErrorCode());
}
```

`getErrorCode()` puede ser nulo; `equalsIgnoreCase(null)` devuelve `false`, así que un código ausente cae correctamente al branch de "no disponible". No hardcodear el literal `"conflict"`: usar la constante del SDK deja el acoplamiento donde corresponde.

### H2 · Validación del QKVS en los scopes objetivo

**Cerrado para el alcance actual.** El QKVS compartido funciona en `test2` y `bq-consumer-test-nonprod`, que son los scopes donde se validó el flujo. No se modifica `stage` ni `staging-nonprod`: hacerlo sería alcance adicional sin beneficio para esta entrega.

**Matiz importante.** No se usa `NoOpKvsClient`, porque simula adquisición exitosa y ocultaría que no hay exclusión. El fallback elegido ocurre sólo cuando un KVS real informa indisponibilidad: se deja trazabilidad y se ejecuta el flujo anterior sin lock.

**Observación adicional de disponibilidad.** En producción el mutex quedaría sobre `kvs-action-locks-nonsite`, que está declarado con criticality `medium`, compartido con el lock de acciones de data product. El avance de batches pasa a ser una dependencia dura de ese container: si se bloquea por cuota (`OVERQUOTA_BLOCKED`) por actividad del lock de acciones, el pipeline de deployments deja de avanzar. Container dedicado y criticality acorde al flujo que protege.

### M1 · Expiración del TTL a mitad de transacción

**Verificado, con el alcance real de la transacción.** El orden acquire → transacción `REQUIRES_NEW` → commit → release en `finally` es correcto: un adquirente posterior siempre lee estado comiteado. Lo que falta es renovación del lock o un fencing token validado en la escritura. Si la transacción supera el TTL, la clave expira, un competidor la adquiere, no ve deployments comiteados y despacha el mismo batch.

Lo que acota el riesgo: el envío al control plane ocurre **fuera** de la transacción (`AFTER_COMMIT` + `@Async`), y `ParameterResolutionService` no hace I/O remota. La transacción es DB + parsing. Bajo latencia normal, 10 s sobra; el riesgo vive en la cola de latencia y en pipelines grandes.

**Decisión.** No se agregan renovación, fencing ni cambios de esquema a este hotfix. Se mide la duración real y se observa el p99.9; si el hold se acerca al TTL, se abre trabajo separado. Esto conserva KISS y no intenta resolver el refactor durable dentro del parche.

### M2 · Una sola cadena de reintento por transición

**Verificado, con un matiz importante.** `scheduledRetries` es un `ConcurrentHashMap` de instancia dentro de un bean singleton: **el dedup es por pod, no global**. Con varios pods, el escenario de starvation es menos probable de lo que sugiere el review; con un solo pod es exactamente como se describe. El `putIfAbsent` descarta el evento concurrente y lo registra a nivel `DEBUG`, que es demasiado bajo para una oportunidad de avance perdida.

**Fix propuesto.** Mantener una sola cadena local es razonable para evitar tormentas, siempre que el deadline de C1 garantice el probe final y que una falla al agendar libere el marcador. No es necesario eliminar el mapa ni promover contención sana a `INFO`; sí conviene contar contención, expiraciones y fallas de scheduling.

### M3 · Materialización parcial re-despacha el batch completo

**Verificado.** `inspectNextBatchMaterialization` devuelve `ALL` sólo si *todos* los componentes del batch siguiente ya tienen deployment en el group; en cualquier estado parcial devuelve `NONE`, y `dispatchBatch` recibe la lista completa. Aguas abajo, `BatchDispatchServiceImpl.validateActiveDeployments` corre **antes** del loop por ítem y lanza `ConflictException` por el componente que ya tiene un deployment activo no final: aborta el batch entero, la transacción hace rollback, la excepción se traga en el listener y **ningún** componente avanza.

El modo de falla es stall permanente, no duplicado. La variante "fila duplicada en silencio" no es alcanzable: `nextBatch` filtra sólo runs en `PENDING`, y un componente cuyo deployment llegó a estado final ya no tiene su run en `PENDING`.

**Fix propuesto.** Colapsar el enum `NONE`/`ALL` en una sola operación que devuelva el conjunto ya materializado, y despachar sólo el pendiente. Elimina la asimetría todo-o-nada y hace innecesario el caso especial:

```java
final var materializados = materializedComponentIds(groupId, nextBatch);
final var pendientes = nextBatch.stream()
    .filter(run -> !materializados.contains(run.getComponent().getId()))
    .toList();

if (pendientes.isEmpty()) {
  log.info("Next batch already materialized: execution={} group={} order={}",
      executionId, groupId, nextBatchOrder);
  return;
}
// dispatchBatch sólo con `pendientes`
```

El test `whenOnlySomeNextBatchComponentsAreMaterialized_thenItDispatchesTheBatch` afirma hoy el comportamiento equivocado y debe reescribirse para exigir que se despache **sólo el subconjunto faltante**.

### M4 · Ningún test ejercita el lock real bajo concurrencia

**Verificado y agravado.** `BatchCompletedEventListenerConcurrencyTest` es el único test con hilos reales (`CountDownLatch` + pool de 2), pero corre contra `CoordinatedBatchAdvanceLock`, un fixture en memoria sobre `AtomicReference`. Y hay una segunda capa: el perfil `integration_test` resuelve `batchListenerLockKvsClient` a `NoOpKvsClient`, que siempre otorga el lock, así que **los tests de integración tampoco serializan nada**. `BatchAdvanceLockImpl` no tiene ninguna cobertura de contención.

Eso explica por qué H1 pasó desapercibido: los dos tests de `BatchAdvanceLockImplTest` sólo verifican `Optional.empty()`, resultado idéntico en ambos branches, así que ninguno distingue el camino de conflicto del camino de outage.

**Fix propuesto.** No borrar el archivo: conservar el harness de dos hilos y sumar pruebas de `BatchAdvanceLockImpl` con un `KvsClient` fake versionado. Deben distinguir `CONFLICT` (retry por deadline) de indisponibilidad (fallback sin lock) y no fijar el número exacto de intentos. No se agrega un test que prometa exclusión cuando el TTL expira durante la transacción: sin renovación o fencing, esa propiedad no existe; se mide y alerta como límite aceptado del hotfix.

Y reemplazar `assertEquals(3, result.lockAttempts())` por una aserción de rango (`>= 2`): fijar el número exacto de reintentos ata el test a la política de backoff, que es justamente lo que C1 obliga a cambiar.

### L1 · Argumentos invertidos en el test

**Verificado contra el bytecode:** `ClientException(String errorCode, String message)`. En `BatchAdvanceLockImplTest:66`, `new KvsClientException("kvs unavailable", "UNAVAILABLE")` pasa el mensaje como código. En la línea 57 el orden es correcto pero el código (`"VERSION_CONFLICT"`) no existe. Los dos tests terminan en el mismo branch y por eso pasan por la razón equivocada.

```java
// línea 57
doThrow(new KvsClientException(ErrorCode.CONFLICT.getCode(), "lock busy"))
// línea 66
doThrow(new KvsClientException(ErrorCode.SERVICE_ERROR.getCode(), "kvs unavailable"))
```

Además de corregir los argumentos, cada test debe verificar el **branch**, no sólo el retorno: que el conflicto no loguee WARN y que el outage sí lo haga.

### L2 · Campos muertos en `LockHandle`

**Verificado.** `attempts` y `waitedMillis` se construyen siempre como `(1, 0)` en el único call site de producción, y su único lector es una aserción de test sobre esa constante. Reducir a `record LockHandle(String key, String ownerToken) {}`.

**Métricas acordadas.** Crear un `BatchAdvanceLockMetrics` sobre el `MetricsClient` existente, sin IDs de execution, batch, owner, key, deployment ni mensaje de excepción. Sólo cuatro series: `rio.playmaker.batch_advance_lock.acquired`, `.contended`, `.fallback` y el histograma `.hold_duration_ms`; la única etiqueta opcional y acotada es `reason:kvs_unavailable|scheduler_failed`. El histograma permite observar p99/p99.9 sin generar cardinalidad de Datadog.

### L3 · Cambio de `kvs.segment` en `staging-nonprod`

**Verificado.** El cambio de `nonsite` (heredado de `application.yml`) a `nonprod` afecta también a `actionResultKvsClient` y `actionLockKvsClient` en ese scope. Hoy es inerte porque `ActionResultKvsConfig` y `ActionLockKvsConfig` resuelven a `NoOpKvsClient` con `actionsFramework.enabled: false`, pero se vuelve un cambio de ruteo real en cuanto ese flag se active. Declararlo explícitamente en la descripción del PR; hoy no figura en el alcance.

### INFO · `IllegalStateException` inalcanzables en `componentIdOf`

**Evaluación.** En datos válidos, `DeploymentModel.service`, `ServiceModel.componentDefinition` y `ComponentDefinitionModel.component` son no nulos. Si esa invariancia se rompe, ignorar el deployment como propone el review puede hacer que se lo considere no materializado y se despache otra vez. El comportamiento actual fail-closed es más seguro para este hotfix; como máximo, mejorar el mensaje y abrir una alerta de integridad.

### SEC · Auditoría de seguridad

- **`ThreadLocalRandom` para el jitter — no es hallazgo de seguridad.** El valor sólo decide un delay; no es secreto, token ni control de acceso. `ThreadLocalRandom` es la opción adecuada para este uso concurrente. Cambiar a `SecureRandom` sólo corresponde si un gate concreto del repositorio lo exige; esa regla no fue aportada como evidencia del comentario.
- **`UUID.randomUUID()` como owner token — sin observaciones.** La misma regla aprueba explícitamente `java.util.UUID` para identificadores, y UUID v4 se genera con `SecureRandom` internamente. Es la elección correcta.
- **Container compartido — confirmado.** Ver la observación de disponibilidad en H2: es un tema de vecino ruidoso y de criticality, no de seguridad.
- **TOCTOU en `release()` — confirmado y correctamente clasificado como no bloqueante.** La secuencia `get` → compara owner → `delete` tiene una ventana ABA real, pero la clave no es alcanzable por un atacante (servicio interno, clave derivada de ids internos) y el TTL ≤ 10 s la acota. Es una preocupación de corrección, no de seguridad. El comentario del código ya lo documenta honestamente.

---

### Hallazgos adicionales no cubiertos por el review

- **Una `RuntimeException` que no sea `KvsClientException` descarta la transición sin reintentar.** `KvsClient.toSync` re-lanza tal cual las `RuntimeException` que no sean `KvsClientException`, así que un fallo de transporte que llegue por esa vía escapa al `catch (KvsClientException)` de `tryAcquire`, cae en el `catch (RuntimeException)` de `tryAdvance` y **retorna sin agendar reintento**. Es el mismo modo de falla silenciosa de C1 por otra puerta. Fix: en `tryAdvance`, tratar el fallo del intento de lock como "no adquirido" y agendar reintento, en vez de abandonar.
- **El lock protege más que el dispatch.** `checkPrerequisites` también resuelve `propagateFailure` y `checkGroupCompletion`. Un evento descartado por reintentos agotados no sólo impide avanzar: puede dejar sin propagar la falla de un batch fallado y sin cerrar un group ya terminado. Vale documentarlo en el javadoc de `BatchAdvanceLock`, porque cambia qué significa perder un evento.
- **`inspectNextBatchMaterialization` carga todo el group en cada avance.** `deploymentRepository.findByDeploymentGroupId(groupId)` trae los deployments de *todos* los batches, cada uno arrastrando `service` → `componentDefinition` → `component` en fetch EAGER. Es trabajo O(deployments del group) en cada transición, dentro de la transacción cuya duración determina si el TTL alcanza. Consultar sólo por los componentes del batch siguiente, con proyección de `component_id`.

---

### Plan de resolución

| Paso | Qué toca | ¿Bloquea el merge? | Notas |
|---|---|---|---|
| 1 | H1 — `ErrorCode.CONFLICT.getCode()` en `isVersionConflict` | **Sí** | Una línea; sin él la observabilidad del lock es ruido puro |
| 2 | L1 — argumentos y códigos reales en `BatchAdvanceLockImplTest`, aserción del branch | **Sí** | Es lo que dejó pasar el paso 1 |
| 3 | H2 — conservar QKVS compartido validado en `test2` y `bq-consumer-test-nonprod`; no tocar `stage`/`staging-nonprod` | No | YAGNI: son scopes fuera del rollout |
| 4 | C2/M1 — agregar `BatchAdvanceLockMetrics` con cuatro series de baja cardinalidad y observar p99/p99.9 | No | Sin IDs, keys ni errores como tags |
| 5 | C1 — distinguir `BUSY` de `UNAVAILABLE`; reintento por deadline sólo para `BUSY`, fallback fail-open medido para outage | **Sí** | Preserva el comportamiento previo si KVS cae |
| 6 | M3 — despachar sólo el subconjunto pendiente; reescribir el test que afirma lo contrario | **Sí** | Convierte un stall permanente en avance correcto |
| 7 | M4 — probar `BatchAdvanceLockImpl` con KVS fake versionado: `CONFLICT` reintenta y outage ejecuta fallback; desacoplar el número de intentos | **Sí** | No prometer exclusión tras expirar el TTL: se observa con métrica |
| 8 | M2 — mantener una cadena local, contar fallas de scheduling y garantizar el probe del paso 5 | No | El dedup no es el defecto raíz |
| 9 | L2 — reducir `LockHandle` a sus datos usados | No | Limpieza |
| 10 | INFO — conservar fail-closed en `componentIdOf`, con alerta de integridad si se desea | No | Ignorar una fila puede reintroducir duplicidad |
| 11 | L3 — declarar el cambio de `kvs.segment` en la descripción del PR | No | Documentación |
| 12 | SEC — no cambiar `ThreadLocalRandom` salvo evidencia de un gate aplicable | No | No hay vulnerabilidad |
| 13 | C2 parte B — deuda separada: `KvsMutex` compartido con TTL por call site; container KVS dedicado en producción | No | **Fuera de este PR**, por diseño |

### Criterios de aceptación del re-review

- Existe un test determinista del scheduler donde el contender mantiene una cadena hasta un probe posterior al TTL, incluso cuando los sorteos de jitter son cero.
- Existe un test con lock real/fake versionado donde `CONFLICT` mantiene la cadena hasta el probe final y un outage ejecuta el fallback sin reintentar.
- Existe un test que verifica que un `CONFLICT` de KVS se registra como contención y **no** como outage.
- La política de retry no puede abandonar antes del probe posterior al TTL; no se intenta demostrar esa propiedad con una validación aritmética al arrancar.
- `test2` y `bq-consumer-test-nonprod` documentan la validación del QKVS compartido; no se amplía este PR a scopes no objetivo.
- Las métricas del lock no usan identificadores, claves ni mensajes como tags y permiten seguir fallback, contención y p99/p99.9 de hold.
- Un estado parcialmente materializado despacha sólo los componentes faltantes, verificado por test.
- El p99.9 medido de la transacción de dispatch está anotado en la descripción del PR, junto al TTL elegido y su margen.
- El checklist del PR ya no afirma haber validado KVS en staging si eso no ocurrió.

## 1. Resumen ejecutivo del incidente

Al modificar la configuración de un componente `flink-sql`, Playmaker respondió HTTP 500:

```text
IllegalStateException: Duplicate key 5120
(attempted merging values DeploymentModel@... and DeploymentModel@...)
```

La excepción nace en `PipelineServiceImpl.batchBuildStateResultMap`, que obtiene deployments activos y construye un mapa por `service_id`. La consulta retornó dos filas activas para `service_id=5120`; `Collectors.toMap` no puede decidir cuál representa el estado vigente.

La inspección de DB mostró dos deployments del mismo componente, service, execution y group. Ambos fueron creados el mismo segundo y ambos quedaron activos. El control plane de Flink informó que una creación duplicada intentó provisionar una aplicación que ya existía.

La lectura no creó la duplicidad: sólo hizo visible que el invariante de escritura ya había sido violado.

## 2. Evidencia entregada

### 2.1 Deployments duplicados iniciales

| Campo | Deployment 6421 | Deployment 6422 |
|---|---:|---:|
| `deployment_id` | `6421` | `6422` |
| `service_id` | `5120` | `5120` |
| `component_id` | `8213` | `8213` |
| `component_definition_id` | `10876` | `10876` |
| componente / tipo | `flink-sql` | `flink-sql` |
| ambiente | `staging` | `staging` |
| `created_at` | `2026-08-20 23:41:02` | `2026-08-20 23:41:02` |
| estado observado inicialmente | `deploy_started` | `deploy_failed` |
| `is_active` | `1` | `1` |
| correlation/materialization ID | `53a13448-...` | `d53c2ae2-...` |

Luego ambos aparecieron como `deploy_failed`, pero continuaron activos. El deployment `6421` se actualizó finalmente a las `00:11:44`; `6422`, a las `23:42:04`.

### 2.2 Misma ejecución y mismo deployment group

Ambas filas comparten:

- `pipeline_execution_id = 3d03a2cd-375b-40cd-9c91-b0e25e454fca`
- `deployment_group_id = 7f96b9ba-8572-4686-bec1-8989e2f95102`
- `desired_state_hash = 09c7919bc3626175a77de229febc05d2c89a3eac60322ccbf6da154e49c34bb7`
- `request_id = NULL`
- execution y group terminaron `FAILED`.

Esto debilita fuertemente la hipótesis de dos requests HTTP de pipeline independientes: no son dos executions ni dos groups diferentes.

### 2.3 Component runs

| Run | Orden | Componente | Resultado | Inicio | Fin |
|---:|---:|---|---|---|---|
| `1825` | `0` | `topic-1` | `COMPLETED` | `03:41:01` | `03:41:02` |
| `1826` | `0` | `topic-2` | `COMPLETED` | `03:41:01` | `03:41:02` |
| `1824` | `1` | `jarita-signal-test` | `COMPLETED` | `03:41:05` | `03:41:06` |
| `1827` | `1` | `flink-sql` | `FAILED` | `03:41:05` | `03:42:04` |

El error guardado en el run `1827` fue:

```json
{
  "code": "INTERNAL",
  "message": "Application already exists. (Service: KinesisAnalyticsV2, Status Code: 400, Request ID: 52cdf551-81d3-4763-9260-28160be87516) (SDK Attempt Count: 1)"
}
```

`deployment_log` no contenía registros. Esto es compatible con el camino agrupado: el error queda en `ComponentRun.error`; el handler no necesariamente crea `deployment_log` para ese caso.

### 2.4 Stacktrace visible al usuario

Archivo de evidencia original:

```text
/Users/rjara/.codex/attachments/b5bd091d-b777-423f-85fa-954be579ea40/pasted-text.txt
```

Camino relevante:

```text
PipelineComponentConfigController.patchComponentConfig
  → PipelineConfigPatchServiceImpl.updateComponentConfig
    → PipelineServiceImpl.getComponentData
      → PipelineServiceImpl.batchBuildStateResultMap
        → Collectors.toMap(serviceId, deployment)
          → IllegalStateException: Duplicate key 5120
```

## 3. Modelo de dominio reconstruido

### Component, Service, ComponentRun y Deployment

- `Component` es la identidad lógica del componente.
- `Service` es el slot operativo del componente en un ambiente; las lecturas y escrituras actuales tratan `service_id` como la identidad del estado desplegado.
- Cada `PipelineExecution` contiene un único `ComponentRun` por componente. La DB posee `uq_cr_execution_component` sobre `(pipeline_execution_id, component_id)`.
- Cada intento de deploy o redeploy crea una nueva fila `Deployment` para el mismo service.
- Los deployments anteriores no se eliminan: forman el historial.
- `is_active=true` identifica el intento vigente/autoritativo del service, no necesariamente un intento exitoso. El último `FAILED` también puede ser activo.

### Cardinalidades esperadas

```text
Component 1 ── N Service       (típicamente uno por environment)
Service   1 ── N Deployment    (historial de intentos)
PipelineExecution 1 ── N ComponentRun
DeploymentGroup  1 ── N Deployment
```

Invariantes inferidos de los consumidores actuales:

1. Máximo un `Deployment is_active=true` por `service_id`.
2. Un deployment group no debiera crear dos intentos equivalentes para el mismo service, salvo que exista una semántica de retry explícita y distinguible.
3. Un redeploy posterior puede crear otra fila, pero debe desactivar la fila activa anterior.

El Javadoc de `DeploymentModel` habla de “same Definition and Service”; el código vigente y sus queries operan realmente por service. Debe revisarse como documentación posiblemente obsoleta.

## 4. Reconstrucción temporal preliminar

```text
T0  topic-1 y topic-2 del batch 0 reciben COMPLETED casi juntos
T1  cada resultado persiste su ComponentRun como COMPLETED
T2  cada resultado publica un BatchCompletedEvent independiente
T3  ambos commits terminan
T4  dos listeners async arrancan en transacciones REQUIRES_NEW
T5  ambos pueden leer: batch 0 terminal + batch 1 todavía PENDING
T6  ambos invocan dispatchBatch para el batch 1
T7  ambos pueden pasar el check de active antes de observar el insert del otro
T8  ambos crean un Deployment active para service 5120
T9  el control plane acepta una creación y rechaza la otra: Application already exists
T10 una lectura posterior intenta mapear ambos active por service y falla con Duplicate key 5120
```

Los timestamps apoyan esta ventana:

- Los runs del batch 0 terminaron a las `03:41:02`.
- Los deployments `6421` y `6422` se crearon a las `23:41:02` local, equivalente por huso horario.
- El callback `STARTED` del batch 1 llegó recién a las `03:41:05`.
- Hasta recibir `STARTED`, `ComponentRun` permanece `PENDING`; por tres segundos “no despachado” y “comando ya creado/enviado” son indistinguibles en ese estado.

## 5. Punto exacto de consistencia sospechado

### Publicación de un evento por completion

`DeploymentResultHandlerImpl`, bloque `COMPLETED`:

- marca el run `COMPLETED`;
- guarda deployment/estado;
- publica `BatchCompletedEvent(runId, deploymentId)`.

Referencia: `src/main/java/com/mercadolibre/rio/playmaker/service/impl/DeploymentResultHandlerImpl.java`, aproximadamente líneas 313–348 del snapshot.

### Ejecución concurrente después del commit

`BatchCompletedEventListener` usa:

- `@Async(ExecutorConfig.ASYNC_EXECUTOR)`;
- `@TransactionalEventListener(AFTER_COMMIT)`;
- `TransactionTemplate` con `PROPAGATION_REQUIRES_NEW`.

Referencia: `src/main/java/com/mercadolibre/rio/playmaker/service/pipeline/impl/BatchCompletedEventListener.java`, líneas 61–65.

### Check de nivel sin consumo/claim

`OrchestrationServiceImpl.checkPrerequisites`:

1. carga todos los runs;
2. verifica que el batch completado esté terminal y sin failures;
3. selecciona los runs del siguiente orden que todavía estén `PENDING`;
4. llama `dispatchBatch`.

No persiste un claim del batch antes del dispatch.

Referencia: `src/main/java/com/mercadolibre/rio/playmaker/service/pipeline/impl/OrchestrationServiceImpl.java`, líneas 61–110.

### Reserva de deployment como check-then-act

`BatchDispatchServiceImpl`:

1. carga los active deployments de todos los service IDs;
2. valida que no exista uno non-terminal;
3. desactiva el terminal anterior, si existe;
4. crea una fila `Deployment REQUESTED, is_active=true`;
5. publica el evento de dispatch.

La lectura y el insert no están protegidos por una reserva estable ni por una restricción que cubra la ausencia de fila.

Referencia: `src/main/java/com/mercadolibre/rio/playmaker/service/pipeline/impl/BatchDispatchServiceImpl.java`, líneas 183–232 y 280–290.

### Detección tardía

`PipelineServiceImpl.batchBuildStateResultMap` usa `Collectors.toMap` por `service.id` sin merge. Eso refleja la expectativa “máximo uno activo por service” y falla cuando la DB ya contiene dos.

Referencia: `src/main/java/com/mercadolibre/rio/playmaker/service/impl/PipelineServiceImpl.java`, aproximadamente línea 303.

## 6. Hipótesis que una investigación independiente debe probar o falsar

| Hipótesis | Evidencia a favor | Evidencia en contra / faltante | Confianza previa |
|---|---|---|---|
| Dos completion legítimos del batch 0 consumieron dos veces la condición de avance | Dos runs order 0 terminaron el mismo segundo; un evento por COMPLETED; listener async; mismo group/execution; dos inserts simultáneos | Faltan logs de ambos listeners con execution/order | Alta |
| Entrega duplicada/concurrente de un mismo mensaje de resultado | El transporte puede ser at-least-once; el terminal guard tampoco demuestra serialización de dos consumidores simultáneos | Hay dos completion legítimos suficientes para explicar el caso; faltan delivery IDs/logs | Media-baja como trigger, relevante como requisito |
| Dos requests HTTP de pipeline distintos | Podrían competir por el mismo service | Ambos deployments comparten exactamente execution, group y desired-state hash | Baja |
| Dos ComponentRun duplicados para Flink | Podrían generar dos dispatch items | Evidencia muestra un solo run `1827`; existe unique `(execution, component)` | Muy baja |
| Retry interno creó el segundo Deployment | Sería compatible con varios intentos históricos | Ambos nacen el mismo segundo y correlation IDs distintos; falta revisar `retry_count` y call sites | Baja |
| El control plane creó la duplicidad en DB | CP puede procesar un trigger dos veces | `Deployment` se crea en Playmaker antes de publicar; CP no inserta esa fila | Muy baja |
| Replica lag o lectura stale por sí sola | Puede ampliar ventanas de carrera | No explica por sí sola dos inserts active en el mismo group/service | Baja |

La causa funcional importante no depende de cuál evento duplicó la invocación: **el avance de batch y la creación del intento no son idempotentes frente a más de una invocación válida o repetida**.

## 7. Por qué “esperar todo el batch 0” no alcanza

La validación de terminalidad sí existe. El problema es que es una condición de nivel:

```text
batch0 == terminal AND batch1 == PENDING
```

Mientras no haya una transición atómica que consuma esa condición, más de un listener puede verla verdadera. Esperar correctamente el batch previo garantiza orden topológico, pero no garantiza exactamente un avance.

## 8. Desarrollo y deuda ya encontrados

### Cambio regresor plausible

- Commit `dac615f474461983cf26645fbb5bbb3e0888f04a`, 2026-08-19, PR `#1047`.
- Introdujo `BatchCompletedEvent` y el listener async/after-commit para que la resolución de parámetros del siguiente batch lea outputs ya confirmados.
- El objetivo del cambio es válido, pero abrió o amplió la ventana donde dos listeners observan el mismo siguiente batch `PENDING`.
- Está en `develop` y en la release local `202608.19.0`; el incidente fue al día siguiente.

### Deuda explícita en develop

`meli/backlog.md` contiene:

- `DEBT-SIG186-CONCURRENT-DEACTIVATE`, líneas 57–63: dos requests concurrentes pueden desactivar el mismo terminal y crear dos active.
- `DEBT-SIG326-DISPATCH-ACTIVE-RACE`, líneas 65–71: el check-then-act de dispatch puede crear dos active; lockear sólo el deployment existente no funciona cuando todavía no hay fila.

La deuda propone estudiar lock del service slot, reserva transaccional o unicidad compatible con MySQL.

### Fix parcial no mergeado

- Commit `adf5cf54ff5359f37391dd638da0fbd95105519a`, rama local-remota `origin/feature/kvs-actions-segmented-test-scopes`.
- Agrega `PESSIMISTIC_WRITE` sobre `PipelineExecution` antes de revisar completitud.
- Su motivación declarada era otra carrera de roll-up: dos handlers podían ver al sibling incompleto y ninguno cerraba la execution.
- No está en `develop`, release ni master según las refs locales inspeccionadas.
- Es anterior al listener async actual, no introduce claim de batch y no posee una prueba concurrente exact-once. No debe tratarse como parche listo para cherry-pick.

### Falsos positivos descartados al buscar fixes

- `origin/fix/orchestration-batch-log-visibility`: sólo mejora logs de batch incompleto.
- PR `#934` / `feature/fixdeployment-race-condition`: corrige dispatch `AFTER_COMMIT` y problemas de pool/transacción; no agrega claim del siguiente batch ni unicidad active.
- No se encontró `DISPATCHING`, `claimBatch`, `claimNext`, `active_reservation` ni restricción unique de active service en las refs locales.

> [!warning]
> La revisión de trabajo pendiente se hizo sobre refs locales, sin `git fetch` ni inspección de PRs privados en vivo. “No encontrado” no significa que no exista una rama remota creada después del último fetch.

## 9. HISTÓRICO SUPERSEDED — Alternativas preliminares para contrastar

> [!warning] Esta sección quedó superseded por “Decisión vigente — hotfix acotado + refactor durable”. Se conserva exclusivamente como historial de investigación. Ninguna mención a `DISPATCHING`, schema nuevo, constraints o locks DB debe trasladarse al hotfix vigente.

Estas propuestas representan el análisis previo. La auditoría independiente las contrastó antes de que el equipo descartara el enfoque `DISPATCHING` y acotara el parche.

### A. Lock de PipelineExecution + idempotencia por group/service

1. Adquirir un lock pesimista sobre `PipelineExecution` al inicio de `checkPrerequisites`.
2. Recargar los runs dentro del lock.
3. Considerar idempotente un deployment ya existente para `(deployment_group_id, service_id)`.
4. Respaldar la idempotencia con una restricción unique en DB.

Ventajas:

- Cambio acotado para la carrera intra-execution.
- No cambia el enum público de `ComponentRun`.
- Si la primera transacción hace rollback, otra invocación puede intentar nuevamente.

Riesgos:

- El lock solo no representa semánticamente que el batch fue reclamado.
- Si se depende únicamente del active `REQUESTED`, la segunda invocación terminaría como conflicto en vez de no-op.
- No resuelve por sí solo carreras entre executions diferentes.

### B. DEPRECATED — Estado `DISPATCHING` usado como claim atómico

> Esta alternativa queda descartada por decisión del equipo. Se conserva como registro de una hipótesis/fix experimental, no como solución a implementar.

Transición conceptual:

```text
PENDING → DISPATCHING → RUNNING → COMPLETED | FAILED
```

Debe implementarse con compare-and-set:

```sql
UPDATE component_run
SET status = 'DISPATCHING'
WHERE id = :id AND status = 'PENDING';
```

Sólo la transacción que afecta las filas esperadas puede despachar.

Ventajas:

- Hace visible la diferencia entre “aún no enviado” y “comando creado/en tránsito”.
- El segundo listener observa que el batch ya fue reclamado.

Riesgos e impacto:

- Un `read PENDING` seguido de `set DISPATCHING` normal mantiene la carrera.
- Cambia Swagger/history/frontend/tests y todos los guards que conocen estados.
- `STARTED` debe implementar `DISPATCHING → RUNNING`.
- Debe existir rollback o reconciliación para crashes entre claim y publicación.
- Hoy el error async puede fallar el Deployment sin sacar el ComponentRun de un estado intermedio.
- Reusar `RUNNING` como claim falsearía su semántica actual: hoy significa callback `STARTED` del control plane.

### C. Claim del batch en DeploymentGroup o entidad dedicada

Persistir un cursor/CAS de batch, o una entidad `batch_execution` única por `(group_id, run_order)`.

Ventajas:

- Modela la exclusión en el nivel correcto: el batch, no cada run individual.
- Puede registrar owner, timestamps, intento y recuperación.

Riesgos:

- Requiere schema/migration y definición completa del lifecycle.
- Debe coordinarse transaccionalmente con la creación de deployments y la publicación posterior al commit.

### D. Lock/reserva estable por Service

Antes de leer, desactivar o crear deployments, lockear las filas `service` involucradas en un orden determinista.

Ventajas:

- Cubre el invariante global incluso entre executions distintas.
- La fila `service` existe aunque todavía no exista un deployment activo.

Riesgos:

- Puede aumentar contención y riesgo de deadlock si no se ordenan los IDs.
- No reemplaza la semántica idempotente del avance de batch; es una defensa de dominio.

### E. Unicidad DB para el intento lógico o el active slot

Posibles invariantes distintos:

- `UNIQUE(deployment_group_id, service_id)` para impedir el mismo intento lógico dentro del group.
- Reserva dedicada o generated column compatible con MySQL para garantizar máximo un active por `service_id`.

Ventajas:

- La DB se convierte en última barrera frente a carreras no previstas.
- Evita que lectores reciban un estado físicamente ambiguo.

Riesgos:

- Debe definirse la semántica de retries legítimos.
- MySQL no ofrece partial indexes nativos; hay que validar generated column, tabla de reserva u otro diseño.
- Una violación unique debe convertirse en idempotent no-op cuando corresponde; no puede propagarse ciegamente como failure del run válido.

### F. Inbox/idempotency key para eventos de resultado

Registrar y deduplicar la identidad lógica del evento o comando antes de procesarlo.

Ventajas:

- Protege contra redelivery at-least-once del mismo resultado.

Riesgos:

- Dos eventos legítimos diferentes del mismo batch seguirían necesitando un claim común del avance.
- Exige definir correctamente la clave y retención.

## 10. HISTÓRICO SUPERSEDED — Dirección preliminar del análisis previo

> [!warning] No implementar esta dirección. La decisión vigente está al inicio de la nota y reemplaza esta composición para separar hotfix y refactor durable.

No fue una decisión. La composición con mejor equilibrio encontrada en esa etapa era:

1. **Causa intra-execution:** serializar la evaluación bajo lock de execution y volver idempotente la creación por `(group, service)`.
2. **Backstop persistente:** restricción unique para el intento lógico del group.
3. **Invariante global:** reserva/lock estable sobre service o mecanismo DB equivalente para exactly-one-active entre executions.
4. **Observabilidad:** métrica y error de integridad cuando una lectura encuentre más de un active; no elegir silenciosamente uno.
5. **Verificación:** prueba concurrente real con dos completions simultáneos, redelivery duplicado y dos executions compitiendo por el mismo service.

Una alternativa basada en claim explícito de batch puede resultar superior después de evaluar recuperación, semántica de retry y costo de migración. El proyecto no debe favorecer el menor diff por sobre la corrección.

## 11. Criterios para comparar soluciones

Cada opción debe puntuarse explícitamente en:

- Garantía frente a dos completions legítimos del mismo batch.
- Garantía frente a redelivery duplicado del mismo evento.
- Garantía frente a executions concurrentes sobre el mismo service.
- Atomicidad cuando aún no existe ningún deployment.
- Semántica de retries legítimos.
- Recuperación ante crash entre persistencia y publicación.
- Compatibilidad con `AFTER_COMMIT` y el pool async.
- Preservación del historial de deployments.
- Impacto en API, frontend, enums y migraciones.
- Riesgo de deadlocks/contención.
- Observabilidad y facilidad de soporte.
- Testabilidad determinística.
- Complejidad de rollout y rollback.

## 12. Criterios de aceptación funcional

### Hotfix

- Dos `BatchCompletedEvent` de components distintos del mismo batch compiten por la misma clave y sólo un listener ejecuta la materialización.
- El perdedor espera sin mantener una transacción/conexión DB, adquiere el lock después del ganador y relee estado en una transacción nueva.
- Si todos los components PENDING del próximo batch tienen deployment en el mismo group, el perdedor termina `already_materialized` sin llamar otra vez a `dispatchBatch`.
- Si no existe ningún deployment del próximo batch, el listener conserva el flujo actual.
- Si el batch no está completamente materializado, se conserva el flujo actual de `dispatchBatch`, incluida su semántica de fallas parciales por componente.
- KVS temporalmente indisponible no habilita fail-open: el listener espera con backoff y métricas.
- No aparecen `DISPATCHING`, migraciones, entidades JPA nuevas, cambios de API/CP ni modificaciones del happy path.

### Refactor durable

- Dos components del batch N que completan simultáneamente generan exactamente un dispatch por service del batch N+1.
- Dos deliveries concurrentes del mismo resultado no generan un intento adicional.
- Una segunda invocation idempotente no marca `FAILED` un run cuyo primer dispatch es válido.
- Dos executions concurrentes sobre el mismo service no pueden dejar dos deployments activos.
- Un redeploy posterior crea una nueva fila histórica y desactiva la anterior de manera atómica.
- Un crash antes del commit no consume definitivamente el batch.
- Un crash después del commit y antes/durante el transporte es recuperable o detectable.
- El estado de DB nunca depende de que `Collectors.toMap` elija arbitrariamente una fila.
- Logs y métricas permiten identificar execution, group, batch order, service, claim/idempotency key y outcome.

## 13. Evidencia todavía necesaria

Para subir la causalidad desde alta confianza a verificada:

1. Consultar todos los deployments del group `7f96b9ba-8572-4686-bec1-8989e2f95102`, incluyendo el service de `jarita-signal-test` (`component_id=8210`). Si el batch completo fue invocado dos veces, podría existir otro intento duplicado o un conflicto parcial.
2. Buscar dos logs `Dispatched next batch` con `execution=3d03a2cd-...`, `order=1` y los run IDs `1825`/`1826`.
3. Recuperar logs del `BatchCompletedEventListener` y `BatchDispatchServiceImpl` alrededor de `03:41:02–03:41:05`.
4. Verificar `retry_count`, action y correlation IDs de todos los deployments del group.
5. Verificar identidad/delivery metadata de los mensajes COMPLETED para distinguir dos eventos legítimos de redelivery duplicado.
6. Confirmar isolation level efectivo, topología primary/replica y MySQL version de producción.
7. Revisar refs remotas/PRs actuales con autorización para confirmar si apareció un fix después del último fetch.

## 14. Plan de pruebas requerido

### Hotfix

- Test concurrente con dos `BatchCompletedEvent` de runs distintos de la misma execution/order y KVS fake versionado; usar barrera para demostrar competencia real.
- Verificar un único `dispatchBatch` y que el perdedor espera, adquiere después, abre una transacción fresca y retorna `already_materialized`.
- Verificar que la clave colisiona para mismos execution/next order y no colisiona entre executions u órdenes distintos.
- Verificar exponential backoff con jitter mediante scheduler inyectable, sin sleeps reales ni workers retenidos en unit tests.
- Verificar KVS conflict, indisponibilidad transitoria, TTL/release y owner mismatch.
- Verificar outcomes `all` y `none`, además de conservar la semántica existente de fallas parciales de `dispatchBatch`.
- Verificar que no se toca el consumer HTTP ni se agregan cambios a CPs, schema o enums.

### Refactor durable

- Test de integración con dos `ComponentRun` order 0, usando barrera/latch para que ambos listeners evalúen simultáneamente.
- Test de redelivery concurrente del mismo `COMPLETED`.
- Test de dos `PipelineExecution` diferentes compitiendo por el mismo `service_id` sin deployment previo.
- Test equivalente cuando existe un active terminal.
- Test de retry legítimo dentro del contrato elegido.
- Test de rollback antes de crear intentos y de fallo al publicar después del commit.
- Test de orden determinista de locks para batches con varios services.
- Test de migración con datos históricos y detección previa de duplicados activos.

## ✅ Tareas

- [x] Crear proyecto canónico y consolidar evidencia inicial del incidente #owner/me #type/research #area/meli ✅ 2026-08-21
- [x] Crear [[Prompt maestro — Auditoría independiente del doble dispatch]] con barrera anti-anclaje #owner/me #type/research #area/meli ✅ 2026-08-21
- [x] Ejecutar la fase 1 de investigación independiente sin abrir esta nota #owner/me #type/research #area/meli ✅ 2026-08-21
- [x] Congelar el reporte independiente y recién entonces contrastarlo con esta nota #owner/me #type/research #area/meli ✅ 2026-08-21
- [ ] Recuperar logs y rows faltantes del deployment group para validar la secuencia exacta #owner/me #type/research #area/meli
- [x] Construir una reproducción concurrente determinística en tests #owner/me #type/dev #area/meli ✅ 2026-08-26
- [x] Elaborar matriz de alternativas con criterios explícitos #owner/me #type/research #area/meli ✅ 2026-08-21
- [ ] Obtener aprobación del equipo para las dos etapas: hotfix KVS en listener + refactor durable con tópico externo #owner/me #type/research #area/meli
- [ ] Revisar la propuesta con owners de Playmaker/DB/control plane y confirmar semántica de retry #owner/me #type/pr-review #area/meli
- [x] Crear `hotfix/serialize-batch-completed-listener` desde la base autorizada, sin código `DISPATCHING` #owner/me #type/dev #area/meli ✅ 2026-08-26
- [x] Implementar mutex KVS por `executionId + nextBatchOrder` en `BatchCompletedEventListener`, con `tryAcquire` y retry agendado fuera de DB #owner/me #type/dev #area/meli ✅ 2026-08-26
- [x] Implementar chequeo `all/none` por deployments existentes del group antes de `dispatchBatch` #owner/me #type/dev #area/meli ✅ 2026-08-26
- [x] Cubrir concurrencia, espera, relectura fresca, KVS degradado y release owner-safe #owner/me #type/testing #area/meli ✅ 2026-08-26
- [x] HISTÓRICO DEPRECADO — implementar claim CAS `PENDING → DISPATCHING` y lock de `PipelineExecution` #owner/me #type/dev #area/meli ✅ 2026-08-21
- [x] HISTÓRICO DEPRECADO — cubrir el perdedor del claim `DISPATCHING` #owner/me #type/testing #area/meli ✅ 2026-08-21
- [x] PR #1079 · usar `ErrorCode.CONFLICT.getCode()` en `isVersionConflict` y corregir los códigos/argumentos de `BatchAdvanceLockImplTest` #owner/me #type/dev #area/meli ✅ 2026-08-27
- [x] PR #1079 · validar QKVS compartido en `test2` y `bq-consumer-test-nonprod`; no ampliar a `stage`/`staging-nonprod` #owner/me #type/ops #area/meli ✅ 2026-08-26
- [x] PR #1079 · agregar métricas de lock de baja cardinalidad: acquire, contend, fallback y hold-duration #owner/me #type/dev #area/meli ✅ 2026-08-27
- [x] PR #1079 · distinguir `BUSY` de `UNAVAILABLE`; aplicar deadline con probe posterior a `TTL + margen` sólo ante contención y fallback fail-open medido ante outage #owner/me #type/dev #area/meli ✅ 2026-08-27
- [x] PR #1079 · despachar sólo el subconjunto pendiente ante materialización parcial y reescribir el test que afirma lo contrario #owner/me #type/dev #area/meli ✅ 2026-08-27
- [x] PR #1079 · cubrir `BatchAdvanceLockImpl` real con fake KVS create-only en una carrera y separar `CONFLICT` de outage #owner/me #type/testing #area/meli ✅ 2026-08-27
- [x] PR #1079 · métricas de contención/fallo de scheduling y `LockHandle` a dos campos; conservar fail-closed en `componentIdOf` #owner/me #type/dev #area/meli ✅ 2026-08-27
- [x] PR #1079 · reemplazar el mutex QKVS por `PESSIMISTIC_WRITE` sobre `pipeline_execution`, relectura bajo lock y retry fail-closed #owner/me #type/dev #area/meli ✅ 2026-08-27
- [x] PR #1079 · demostrar el bug con 2 dispatches sin lock y el comportamiento corregido con exactamente 1 dispatch bajo lock #owner/me #type/testing #area/meli ✅ 2026-08-27
- [x] PR #1079 · ejecutar review Zord, aplicar correcciones con Luna, compilar, correr suite completa, commit y push de `f7d4f4881` #owner/me #type/pr-review #area/meli ✅ 2026-08-27
- [x] PR #1079 · publicar la descripción final local y en GitHub, y crear `0.0.9-listener-lock` con build exitoso #owner/me #type/release #area/meli ✅ 2026-08-27
- [x] PR #1079 · aplicar Fury Lock sin renovación, con TTL total máximo de 7 s por decisión explícita del owner; validar suite, commit, push y body #owner/me #type/dev #area/meli ✅ 2026-08-27
- [x] PR #1079 · resolver el stack de dependencias de Fury Lock, alinear `java-toolkit-kvs` con `json-jackson:4.0.0` y crear `0.0.13-listener-lock` con build exitoso #owner/me #type/release #area/meli ✅ 2026-08-27
- [x] PR #1079 · eliminar el fallback sin lock y las condiciones por scope, fijar TTL 5 s + retry 7 s, validar 3.286 tests y publicar `0.0.17-listener-lock` #owner/me #type/release #area/meli ✅ 2026-08-28
- [x] PR #1079 · publicar la corrección de namespace `batch-advance` y crear `0.0.18-listener-lock` desde `93550f7c6` #owner/me #type/release #area/meli ✅ 2026-08-28
- [ ] PR #1079 · esperar el build de `0.0.18-listener-lock` y repetir validación concurrente runtime en nonprod #owner/me #type/ops #area/meli
- [ ] Deuda separada · hacer atómico el state machine de `DeploymentResultHandlerImpl`: callbacks concurrentes `STARTED`/terminales hoy hacen read-modify-save sin `@Version` ni lock y pueden quedar last-commit-wins #owner/me #type/dev #area/meli
- [ ] PR #1079 · observar p99/p99.9 de `hold_duration_ms` en el batch más grande antes de variar el lease #owner/me #type/ops #area/meli
- [ ] PR #1079 · declarar el cambio de `kvs.segment` en la descripción del PR #owner/me #type/pr-review #area/meli
- [ ] Deuda separada · extraer un `KvsMutex` compartido con TTL por call site y evaluar container KVS dedicado en producción #owner/me #type/dev #area/meli
- [ ] Abrir SPEC funcional y SPEC técnica separados para el refactor durable con tópico externo #owner/me #type/research #area/meli
- [ ] Diseñar publicación recuperable DB→topic, identidad atómica de transición y autoridad cross-execution por service #owner/me #type/dev #area/meli
- [ ] Validar en staging bajo concurrencia antes de promover #owner/me #type/dev #area/meli
- [ ] Para el refactor durable, agregar Testcontainers MySQL 8 antes de certificar atomicidad/constraints; el hotfix KVS no introduce schema #owner/me #type/testing #area/meli
- [ ] Confirmar si la aplicación Kinesis Analytics del deployment 6421 sigue viva y reconciliarla fuera de Playmaker #owner/me #type/ops #area/meli
- [ ] Definir la autoridad final ante conflicto entre Playmaker y control plane, requisito para la política de reparación de datos #owner/me #type/research #area/meli

## 📆 Bitácora

- **2026-08-28 — Runtime de 0.0.17 y publicación de 0.0.18:** `bq-consumer-test-nonprod` levantó Jetty y registró `Started Application`, confirmando que Workqueues lazy eliminó el bloqueo de startup sin depender del nombre del scope. Dos completions concurrentes para la ejecución `a95543b0-d790-4659-8abd-e839769d422f` intentaron avanzar al batch 1; el coalescing dejó un único retry pendiente, Lockclient 5 intentó durante 7 s y cerró fail-closed sin llamar al avance. El error no era falta de provisión: el servicio existente en nonprod y nonsite se llama `batch-advance`, pero la aplicación configuraba `rio-playmaker-batch-advance`, por lo que el SDK buscaba el namespace segmentado inexistente `rio-playmaker-batch-advance-nonprod`. Se corrigió el YAML a `batch-advance`, se eliminó el default duplicado del bean, se alineó la construcción a `new LockApiClient()` según el snippet oficial y se agregó una aserción sobre `NamespaceLockClient.getNamespace()`; 25 tests dirigidos y los 2 tests concurrentes pasaron. El commit `93550f7c6` quedó pusheado con la rama en `0 ahead / 0 behind`; Fury aceptó `0.0.18-listener-lock` y dejó su creación pendiente. Los tres eventos posteriores de `7186` (`STARTED`, `STARTED`, `FAILED`) comparten el mismo DB id y deployment UUID, por lo que son callbacks duplicados/concurrentes, no evidencia de dos materializaciones; sí exponen que el handler de estados carece de control de concurrencia y requiere verificación separada del estado final en DB.

- **2026-08-27 — Arranque corregido y versión 0.0.13 finalizada:** los logs de `0.0.12-listener-lock` mostraron que los mensajes de OTEL no eran la falla: el proceso caía con `NoSuchMethodError` al construir `LowLevelClient` porque `java-toolkit-kvs:0.6.1` esperaba Jackson 2 y el runtime resolvía `json-jackson:4.0.0` con Jackson 3. Luna actualizó KVS a `0.7.4` y agregó un test del cliente productivo que reproduce la falla con `0.6.1` y pasa con `0.7.4`. `./gradlew clean check bootJar --no-daemon` pasó con 3.240 tests, 0 fallas, 0 errores y 2 skipped; `git diff --check` y el test dirigido pasaron. Se commiteó y pusheó `b4fa880a2`; Fury finalizó `0.0.13-listener-lock`. El Swagger local preexistente quedó fuera del commit y de la versión. Ver [[Playmaker — java-toolkit-kvs 0.6.1 es incompatible con json-jackson 4]] y [[2026-08-27-playmaker-kvs-jackson-release]].

- **2026-08-27 — Fury Lock cerrado hasta gate externo:** Luna implementó y corrigió el delta; se quitó la renovación por decisión explícita del owner y se limitó el TTL total a 7 s (default 5 s). Los commits `684138b62` y `565059ed4` fueron pusheados a `feature/serialize-batch-completed-listener`; el segundo agrega cobertura dirigida para el gate remoto. Las pruebas obligatorias prueban 2 dispatches sin exclusión y exactamente 1 con Fury Lock compartido. `./gradlew test jacocoTestReport --no-daemon` pasó con 3.237 tests, 0 fallas, 0 errores y 2 skipped; `./gradlew check --no-daemon` pasó. Zord hizo dos ciclos reales con backend Codex `gpt-5.6-terra`; su advertencia de renovación queda reemplazada por la restricción explícita de lease corto no renovable. El body del PR #1079 fue regenerado y publicado. La creación de `0.0.11-listener-lock` permanece condicionada a los checks remotos y a resolver la deprecación de `lockclient:3.0.1`. Ver [[2026-08-27-playmaker-fury-lock-final-entity-updated]] y [[2026-08-27-playmaker-fury-lock-orchestration-session-feedback]].

- **2026-08-27 — Cierre del PR con lock MySQL:** Zord revisó el diff final y Luna aplicó las correcciones pertinentes. El mutex QKVS fue reemplazado por `PESSIMISTIC_WRITE` sobre `pipeline_execution`, con timeout inmediato, transacción fresca, relectura idempotente y retries coalescidos en memoria. Los tests de comportamiento preservan el contrafactual: 2 dispatches cuando se ejecuta el flujo sin exclusión y exactamente 1 con el lock. `./gradlew test jacocoTestReport --no-daemon` pasó con 3.232 tests, 0 fallas, 0 errores y 2 skipped; JaCoCo global 96,36 %, listener 97,56 %, orchestration 98,58 % y métricas 100 %. `./gradlew check --no-daemon`, `git diff --check` y todos los checks del PR pasaron. Se pusheó `f7d4f4881`, se actualizó la descripción local y de GitHub, y `0.0.9-listener-lock` terminó correctamente en Fury después de un único retry idempotente del build 1534. Queda pendiente probar la contención contra MySQL real en staging y diseñar el mecanismo durable de recuperación.
- **2026-08-27 — Cierre Agents OS:** las ocho notas nuevas o modificadas pasaron lint estricto con `0 ERROR / 0 WARN`. La actualización Graphify quedó bloqueada antes de indexar por 18 findings ajenos al proyecto en las skills de Signals y `zsh-modifier-breaks-git-show-sha-path.md`; Markdown permanece como fuente de verdad y la reindexación queda como gap de higiene, sin tocar esa deuda fuera de alcance.

- **2026-08-27 — Correcciones del review aplicadas:** en `/tmp/rio-playmaker-pr1079-fix` se bajó el lease a 7 s y se implementó un probe final con deadline monotónico desde el primer conflicto; `CONFLICT` se distingue de indisponibilidad mediante el código del SDK. Tanto una indisponibilidad tipada como una excepción no tipada del `save` de QKVS, y una falla al agendar retry, ejecutan explícitamente el flujo pre-lock y emiten métricas acotadas. También se corrigen materialización parcial, datos muertos del handle y tests de KVS/concurrencia. `./gradlew test` y la batería dirigida pasan; falta commit/push y observar p99/p99.9 en entorno.

- **2026-08-27 — Commit local, push bloqueado:** se creó `b20aa2474` (`fix: harden batch advance serialization`) en `feature/serialize-batch-completed-listener`. El push fue rechazado por GitHub porque la IP actual no pertenece a la allowlist del repositorio; no hay cambios sin commitear y la rama local está `ahead 1`.

- **2026-08-27 — Push completado:** reintentado el push, GitHub aceptó `1eb04d0c4..b20aa2474` en `origin/feature/serialize-batch-completed-listener`. La rama local quedó sincronizada con origin.

- **2026-08-26 — Decisiones del review del PR #1079:** el QKVS compartido ya fue validado en `test2` y `bq-consumer-test-nonprod`, por lo que no se toca `stage`/`staging-nonprod` (YAGNI). Se mantiene el hotfix pequeño: `CONFLICT` reintenta hasta un deadline posterior al TTL; outage KVS ejecuta el flujo previo sin lock y emite una métrica, aceptando explícitamente la pérdida de exclusión durante el outage. Se agregan cuatro métricas sin cardinalidad dinámica. Se rechazan No-Op como mutex, log-and-skip de deployments corruptos y SecureRandom sin gate demostrable. La consolidación con `DataProductActionLock` queda como deuda separada.

- **2026-08-26 — Coverage del hotfix:** se agregaron tests para locks ausentes y owner-safe, excepciones de KVS y scheduler, contexto incompleto, retry bounds, grupo inexistente, materialización parcial/inválida y criticality por defecto; la suite focal quedó en 50 tests y JaCoCo reporta 100% de líneas y branches en `BatchAdvanceLockImpl`, `BatchCompletedEventListener` y `OrchestrationServiceImpl`. El perfil global quedó elevado a un piso de 95%.
- **2026-08-26 — Regression test concurrente:** se agregó `BatchCompletedEventListenerConcurrencyTest`, que ejecuta dos completion events de la misma transición en threads distintos y coordina con latches el snapshot vacío responsable de la carrera. Con la exclusión desactivada temporalmente reprodujo dos dispatches (`expected: 1 but was: 2`); con el fix verifica un solo `dispatchBatch`, retry del perdedor y relectura de la materialización del ganador. La suite completa quedó en 3216 tests, 0 fallas y 2 skipped. Commit pusheado: `abc51f476`.

- **2026-08-26 — Cierre del hotfix:** la rama `feature/serialize-batch-completed-listener` quedó pusheada hasta `1d34e7532`. El listener usa `tryAcquire`; ante contention agenda hasta 10 retries con full jitter (100 ms base, 1 segundo cap) y libera el worker durante el delay. El lease KVS dura como máximo 10 segundos, reutiliza el QKVS de action locks bajo un namespace propio y respeta los segmentos `nonprod`/`nonsite`. La suite cerró con 3215 tests, 0 fallas y 2 skipped; quedan la prueba concurrente en test2/staging y la revisión del PR.

- **2026-08-26 — Ajuste operativo:** el mutex del hotfix reutiliza el QKVS existente de action locks, con prefijo de llave independiente para evitar colisiones. El TTL quedó limitado por código a un máximo de 10 segundos y el backoff mantiene un máximo de 1 segundo por intento, para cubrir la ventana esperada de eventos paralelos y dar margen a un batch de varios componentes. La implementación base fue `da56b792f`; el ajuste final no bloqueante quedó cerrado posteriormente en `1d34e7532`.

- **2026-08-26 — Implementación hotfix:** se sincronizó `develop` con `origin/develop` en `28b929c9e` y se creó `hotfix/serialize-batch-completed-listener`. El fix agrega mutex KVS owner-safe por `executionId + nextBatchOrder`, espera con exponential backoff fuera de DB, relectura transaccional fresca y chequeo `all/none` por deployments existentes. No introduce schema, enums, cambios HTTP ni cambios de control plane, ni modifica la propagación existente de fallas de batch. `./gradlew test`, la integración de orquestación y JaCoCo pasaron; las clases nuevas del hotfix alcanzan al menos 90% de cobertura de líneas. Queda pendiente la validación concurrente en staging y la promoción/revisión del equipo.

- **2026-08-25 — Approach vigente:** el equipo descartó por completo `ComponentRun.DISPATCHING` y cualquier cambio de schema/estado como hotfix. Se documentaron dos etapas: parche acotado con mutex KVS en `BatchCompletedEventListener`, espera con exponential backoff y detección `already_materialized` mediante deployments existentes del mismo group; luego refactor durable con tópico externo, publicación recuperable y lógica atómica/consistente. La rama propuesta del parche es `hotfix/serialize-batch-completed-listener`; `feature/adhoc-double-dispatch` queda histórica y no promovible.

- **2026-08-21 — Creación:** se consolidó el incidente de staging, el modelo de lifecycle, la inspección de código, el historial git y las deudas conocidas. Tres revisiones independientes convergieron en que el problema visible es una duplicidad activa y que la transición de avance carece de idempotencia/claim. Se mantiene la causa como hipótesis de alta confianza hasta reproducirla. No se tocó código ni DB.
- **2026-08-21 — Método:** se creó un prompt de auditoría en dos fases. La IA debe congelar su investigación desde fuentes primarias antes de abrir esta nota; sólo después puede contrastar y formular una recomendación final.
- **2026-08-21 — Validación:** proyecto, prompt y change log pasaron lint estricto con `0 ERROR / 0 WARN`. La reindexación Graphify quedó bloqueada por una deuda ajena en `Crear Context/SPEC Tecnica — Context IO.md` (`missing-section: ## Contenido`); no se alteró ese archivo fuera de alcance.
- **2026-08-21 — Cierre de sesión:** continuidad lista. Próximo paso: ejecutar la fase 1 del prompt maestro y congelar el diagnóstico independiente antes del contraste.

- **2026-08-21 — Auditoría:** se ejecutó la auditoría en dos fases. Fase 1 congelada con SHA-256 antes de abrir esta nota y verificada antes y después del contraste. Convergencia independiente en 8 puntos, incluido el regresor; la confianza subió de 0.90 a 0.97. Se degradó una afirmación de fase 1 ("los dos componentes de run_order 1 se duplicaron") a hipótesis no verificada, porque `jarita-signal-test` completó bien. Informe en [[Auditoría independiente — Informe del doble dispatch]].
- **2026-08-21 — Hallazgo nuevo:** el redeploy no limpia la duplicación. `loadActiveDeployments` colapsa duplicados quedándose con el primero y el dispatch desactiva sólo esa fila, así que el conteo de activos por service nunca baja. Salió de la observación de que el DP se deployó dos veces.
- **2026-08-21 — HISTÓRICO DEPRECADO — Fix intra-execution:** en `feature/adhoc-double-dispatch` se implementó `PENDING → DISPATCHING` mediante CAS y lock pesimista de `PipelineExecution`; sus tests pasaron, pero el diseño fue posteriormente descartado y no debe promoverse ni usarse como base funcional del hotfix vigente.
- **2026-08-21 — HISTÓRICO DEPRECADO — Impacto cruzado:** se validó la compatibilidad del estado experimental con frontend/rollout y se actualizó PR #1064. Ese trabajo se conserva sólo como evidencia del costo evitado; no forma parte de la entrega vigente.

## 🧭 Decisiones

- El proyecto es `owner: me` y `root: true`: representa una iniciativa técnica humana de Playmaker, no trabajo interno delegado a un agente. No requiere tarea puente.
- No seleccionar una solución durante el diagnóstico inicial.
- No corregir el lector con una función merge como solución funcional; cualquier tolerancia de lectura debe preservar una señal explícita de corrupción.
- Conservar deployments históricos; el invariante a proteger es la vigencia por service y la idempotencia del intento lógico, no “una sola fila para siempre”.
- Entregar dos tracks separados: hotfix intra-execution sin DB/estados/CPs y refactor durable con tópico externo y atomicidad/consistencia completas.
- Tratar backlog y mensajes de commits como contexto secundario; el código, schema, tests y evidencia runtime tienen prioridad.
- Ubicar el mutex del hotfix en `BatchCompletedEventListener`; locks en el result consumer o sólo sobre una fila de deployment no cubren dos listeners async de componentes distintos.
- Intentar el mutex KVS fuera de DB; si está ocupado, agendar el retry y liberar el worker. Después de adquirirlo, comenzar una transacción fresca; el perdedor reconoce materialización por deployments existentes del mismo group, no por `ComponentRun.status`.
- Considerar `feature/adhoc-double-dispatch`, `DISPATCHING`, PR #1064 y su rollout como históricos deprecados.
- Usar Testcontainers MySQL 8 en el refactor durable y en cualquier certificación que dependa de locks/atomicidad DB; el hotfix no agrega schema, pero su prueba de visibilidad post-commit debe usar una superficie transaccional representativa.

## 🔗 Docs / Links

- Descripción del PR: [[Descripción PR — rio-playmaker — Hotfix doble dispatch]]
- Informe de la auditoría: [[Auditoría independiente — Informe del doble dispatch]]
- Prompt ejecutable: [[Prompt maestro — Auditoría independiente del doble dispatch]]
- Aplicación: [[rio-playmaker]]
- Plataforma: [[RIO]]
- Flujo existente: [[playmaker-deploy-flow]]
- Journey: [[deploy-request-path]]
- Repo local: `~/fuentes/rio-playmaker`
- Rama implementada del hotfix vigente: https://github.com/melisource/fury_rio-playmaker/tree/feature/serialize-batch-completed-listener
- PR #1064 / rama `feature/adhoc-double-dispatch`: históricos deprecados; no representan el approach vigente.
- Deuda local: `~/fuentes/rio-playmaker/meli/backlog.md`, `DEBT-SIG186-CONCURRENT-DEACTIVATE` y `DEBT-SIG326-DISPATCH-ACTIVE-RACE`
- Evidencia original: `/Users/rjara/.codex/attachments/b5bd091d-b777-423f-85fa-954be579ea40/pasted-text.txt`

## 💡 Ideas

### Backlog de ideas

- Dashboard o métrica de cardinalidad `active deployment count by service_id > 1`.
- Reconciliador que detecte claims/intentos pegados sin decidir automáticamente cuál deployment histórico borrar.
- Estado de orchestration separado del estado reportado por el control plane.
- Idempotency key explícita y trazable en todos los comandos de deployment.
- Documentar formalmente qué significa `is_active` y corregir el Javadoc stale.

### Motivos / principios

- Exactly-once físico no se asume en transporte distribuido; se busca efecto idempotente mediante persistencia y claves de identidad.
- El historial es información válida; la ambigüedad de vigencia es corrupción.
- Los locks protegen una sección crítica, las constraints protegen invariantes y la idempotencia define el comportamiento repetido. Ninguna de las tres responsabilidades debe confundirse.
- Un estado nuevo sólo se justifica si expresa una transición durable y recuperable, no si se usa como booleano decorativo.

### Memoria pública / interna

- **Memoria pública:** esta nota es la fuente de planificación y contexto del incidente; el conocimiento estable que resulte podrá promoverse después a known error/ADR o al RIO Atlas.
- **Memoria interna:** no se creó memoria interna específica.
- **Motivo:** el diagnóstico todavía está abierto y no corresponde cristalizar una hipótesis como verdad reusable antes de la reproducción y revisión humana.
