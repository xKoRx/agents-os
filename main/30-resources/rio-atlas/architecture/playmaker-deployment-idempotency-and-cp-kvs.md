---
type: resource
schema_version: 1
status: active
area: "[[Meli]]"
sources:
  - "[[rio-playmaker]]"
  - "[[rio-controlplane-kafka]]"
  - "[[rio-controlplane-flink]]"
  - "[[rio-controlplane-clickhouse]]"
  - "[[rio-controlplane-fury]]"
  - "[[Playmaker — Doble dispatch al avanzar batches]]"
last_verified: 2026-08-25
confidence: high
aliases:
  - idempotencia de deployments RIO
  - lock KVS de control planes
  - deduplicación de comandos de deployment
tags:
  - kind/resource
  - area/meli
  - app/rio-playmaker
  - topic/idempotency
created: "2026-08-25"
updated: "2026-08-25"
---

# Playmaker — Idempotencia de deployments y lock KVS en los Control Planes

## Síntesis vigente

La solución de los Control Planes (CP) implementa deduplicación por identidad lógica del comando recibido, no una reserva global del service ni una garantía de “un solo deployment activo” en Playmaker. El patrón común es persistir un registro `IN_PROGRESS` en KVS mediante un write create-only, interpretar el conflicto como “otro worker ya reclamó esta clave”, ejecutar el comando una vez y cerrar el registro con un update CAS a `COMPLETED` o `FAILED`.

Para el problema de Playmaker, esta protección es necesaria pero insuficiente: las filas duplicadas observadas (`6421` y `6422`) tienen distintos `deployment_id`. El CP recibe por tanto dos identidades distintas y sus claves KVS (`deployment:6421` y `deployment:6422`) no colisionan. El CP puede impedir dos entregas del mismo comando; no puede decidir que dos deployments distintos representan por error el mismo avance de batch o el mismo service.

La decisión vigente separa dos horizontes. El hotfix resuelve sólo la carrera intra-execution, sin cambios de DB, estados ni CPs: mutex KVS create-only por `pipeline_execution_id + next_batch_order` directamente en `BatchCompletedEventListener`, espera con exponential backoff y relectura fresca para reconocer por deployments existentes del mismo group que el batch ya fue materializado. La solución final mueve el avance a un tópico externo durable y agrega publicación recuperable, consumo at-least-once e invariantes atómicas/consistentes, incluida la autoridad cross-execution por service.

`ComponentRun.DISPATCHING`, su CAS, sus migraciones y su rollout quedan **DEPRECATED / SUPERSEDED**. No forman parte del parche ni del diseño final acordado.

## Qué hace realmente el KVS

El KVS funciona como un registro de estado con exclusión optimista, no como un lock bloqueante tradicional.

1. El CP construye una clave estable para el comando, por ejemplo `deployment:<deployment_id>` o `action:<action_id>`.
2. Intenta guardar `IN_PROGRESS` con TTL y versión inicial `0`. Si el KVS acepta el write, ese worker ganó la reclamación; el propio registro es el lock lógico.
3. Si el write devuelve `409 CONFLICT`, el CP lee la fila existente. `COMPLETED` o `FAILED` significa duplicado terminal y se descarta; `IN_PROGRESS` reciente significa que otro worker sigue procesando y se descarta; `IN_PROGRESS` stale puede ser tomado por otro worker mediante `update` CAS usando la versión leída.
4. El worker ganador ejecuta la operación real y antes de publicar el resultado actualiza el registro a `COMPLETED` o `FAILED` con CAS sobre su versión. Si pierde el CAS, no publica otro resultado.
5. El TTL limpia registros antiguos y evita locks huérfanos después de un crash. No existe un `release` normal como en un mutex: la transición terminal y la expiración son la liberación lógica.

El protocolo depende de que el container KVS tenga optimistic locking habilitado. La configuración vacía o un error no-conflict del KVS activa modo degradado en Kafka/Flink: el CP continúa y la deduplicación deja de estar garantizada. Esa condición debe ser un gate operacional antes de promover la protección como contrato de producción.

## Patrón comparado por CP

| CP | Clave / identidad | Mecanismo observado | Qué cubre | Veredicto para el incidente |
|---|---|---|---|---|
| Kafka | `deployment:<deployment_id>` y `action:<action_id>` en `triggers-status` | `IdempotencyGuard` compartido: `save(IN_PROGRESS)` create-only, lectura de conflicto, stale takeover y finalize CAS | Redelivery y concurrencia del mismo deployment o action; métricas de `drop`, takeover y degradación | Patrón más completo, pero no evita `6421` vs `6422` |
| Flink | `deployment:<deployment_id>` en `triggers-status` | Mismo modelo de `IdempotencyGuard`; el contexto de claim viaja hasta los handlers/jobs terminales | Redelivery del mismo deployment en los caminos válidos; finalización distribuida en puntos terminales | Correcto como backstop del CP; no protege la identidad del service |
| ClickHouse | `deployment:<deployment_id>` en estado KVS | Estado `STARTED/COMPLETED/FAILED`; el flujo actual consulta `COMPLETED` y luego sobrescribe `STARTED` | Duplicados ya completados en una lectura simple; no hay claim distribuido efectivo en el flujo actual | Gap: dos pods pueden pasar el check y ejecutar juntos |
| Fury | Natural key de pipeline (`destination` o `source+destination`) + `specHash`; QKVS documenta CAS | Convergencia a un pipeline estable; mismo spec es no-op aunque cambie `deployment_id`; cambios de spec usan nueva versión | Redelivery y re-trigger equivalente con IDs distintos para el pusher | Es el único patrón que también deduplica cierta duplicidad de IDs distintos, pero sólo dentro de su dominio natural-key/specHash |

### Kafka y Flink: guard de estado con ventana de retry

El `IdempotencyGuard` permite una ventana corta de `own-retry` (por defecto 500 ms) en la que dos entregas muy cercanas pueden continuar bajo la misma versión. El finalize CAS deja que sólo una publique el resultado, pero ambas pueden alcanzar la operación externa. Por eso el patrón garantiza deduplicación del estado y del resultado con alta probabilidad, no “exactly-once físico” de cada llamada a AWS, Kafka o ClickHouse.

El umbral stale debe ser mayor que la duración máxima legítima de la operación. Si vence mientras el primer worker sigue vivo, otro worker puede tomar el registro y ejecutar en paralelo; el CAS evita que ambos finalicen como dueños, pero no proporciona fencing sobre la infraestructura externa.

### ClickHouse: idempotencia declarada, claim no distribuido

En `ProcessDeploymentUseCase` el flujo actual hace `existsWithStatus(COMPLETED)` y después guarda `STARTED`; el controller además realiza el check antes de enviar el trabajo al executor asíncrono. La interfaz y los tests contienen `claimStart`, pero su implementación KVS usa `synchronized(this)` alrededor de `get` + `save`, que sólo serializa una instancia de JVM. El propio backlog `DEBT-002` documenta que el SDK usado no ofrecía un primitive CAS/save-if-absent para cerrar esta carrera.

El downstream de ClickHouse tiene DDL con operaciones mayormente idempotentes, por lo que el daño esperado es trabajo duplicado y eventos repetidos, no necesariamente corrupción de esquema. Eso no convierte el claim en distribuido ni lo hace equivalente al guard de Kafka/Flink.

### Fury: identidad de negocio antes que id de operación

El pusher distingue correctamente `deployment_id` como ID por operación y `pipelineId` como identidad estable de la entidad desplegada. Busca por una natural key, calcula un hash determinista del desired state y retorna no-op para el mismo spec, incluso con un deployment ID nuevo. En el alta concurrente usa un ID determinista y QKVS CAS para converger sobre el mismo documento; esto es más cercano a lo que Playmaker necesita para reconocer “mismo deployment lógico”, pero no se puede copiar sin definir primero la identidad de negocio de Playmaker.

## Aplicación al doble deployment de Playmaker

El incidente comparte `pipeline_execution_id`, `deployment_group_id`, `service_id` y `desired_state_hash`, pero creó dos filas de deployment y dos IDs. El KVS del CP ve dos comandos legítimos desde su perspectiva. Usar `service_id` como clave KVS del CP tampoco es una solución general: bloquearía redeploys y updates legítimos que deben conservar historial y cambiar el deployment vigente.

La coordinación que falta debe ubicarse donde compiten los eventos: `BatchCompletedEventListener`. Serializar el consumer HTTP de results no basta, porque cada transacción publica un evento `AFTER_COMMIT + @Async` independiente y la carrera reaparece después de liberar cualquier lock del consumer.

### Hotfix vigente

- Clave del mutex: `batch-listener-lock:<pipeline_execution_id>:<next_batch_order>`.
- Backend: KVS create-only con versión inicial `0`, owner token, TTL conservador y release owner-safe.
- Contention/KVS temporalmente indisponible: esperar fuera de una transacción DB con exponential backoff, full jitter y cap; nunca fail-open ni descarte silencioso.
- Después de adquirir: abrir una transacción nueva, releer run/deployment y recalcular prerequisites.
- Evidencia idempotente: comparar los components PENDING del próximo batch con `deploymentRepository.findByDeploymentGroupId(groupId)` y sus `deployment.service.componentId`.
- Outcome `all`: batch `already_materialized`, retorno normal sin `dispatchBatch`; outcome `none`: flujo actual; outcome `partial`: fail-closed con evidencia, nunca reenvío completo.
- Boundary: una fila demuestra materialización del intento, no confirmación de publish. El `DeploymentDispatchRequestedEvent` original sigue siendo responsable del transporte.
- Alcance excluido: cross-execution, unicidad global por service, recuperación tras restart y garantía durable DB→BigQueue.

### Refactor durable objetivo

- Reemplazar el evento Spring interno como frontera de entrega por un tópico externo `BatchAdvanceRequested`, particionado por `pipeline_execution_id`.
- Cerrar DB→topic mediante transactional outbox o garantía equivalente demostrable.
- Consumir at-least-once con identidad estable `(execution_id, next_batch_order)` y materialización atómica/consistente.
- Reutilizar correlation ID estable en retries, incorporar replay, DLQ/reconciliación y observabilidad.
- Resolver explícitamente la autoridad cross-execution por service; el orden por execution no cubre por sí solo dos executions diferentes.
- Mantener los CPs como backstop de redelivery del mismo comando, sin trasladarles la identidad de batch de Playmaker.

## Matriz mínima de validación

| Caso | Playmaker | CP esperado |
|---|---|---|
| Dos `BatchCompletedEvent` simultáneos del mismo batch | Hotfix: un listener espera; el ganador materializa y el perdedor observa `already_materialized` | Sin cambios |
| Redelivery del mismo trigger | No crear otra fila | `409` KVS → drop o takeover; sin segundo resultado |
| Dos triggers con IDs distintos pero misma execution/group/batch/service/hash | Una sola fila activa | El CP no puede arreglarlo si recibe ambos IDs |
| Dos executions distintas para el mismo service | Fuera del hotfix; requisito obligatorio del refactor durable | El CP no debe arbitrarlo con `deployment_id` solamente |
| Redeploy legítimo con spec/desired state nuevo | Nueva fila histórica y sólo un activo | Nueva identidad lógica aceptada |
| KVS del hotfix caído o sin binding | Esperar/reintentar fail-closed con backoff; no abrir la sección crítica | Sin cambios |
| Pod muere mientras espera o antes de ejecutar el evento interno | Limitación conocida del hotfix; el evento Spring no es durable | Sin cambios |
| Crash después de materializar y antes de publish | Limitación conocida; el refactor debe cerrar DB→topic | Sin cambios |

## Evidencia y provenance

- Playmaker: `repo=melisource/fury_rio-playmaker`, paths `src/main/java/com/mercadolibre/rio/playmaker/service/pipeline/impl/BatchDispatchServiceImpl.java`, `src/main/java/com/mercadolibre/rio/playmaker/service/impl/DeploymentResultHandlerImpl.java` y `src/main/java/com/mercadolibre/rio/playmaker/service/impl/DataProductActionLockImpl.java`; snapshot local `feature/new-component-context` en `39f616c46`.
- Kafka CP: `repo=melisource/fury_rio-controlplane-kafka`, paths `src/main/java/com/mercadolibre/rio_controlplane_kafka/idempotency/IdempotencyGuard.java`, `TriggerStatusRecord.java`, `deployment/DeploymentProcessor.java`, `actions/ActionProcessor.java` y `IDEMPOTENCY.md`; `develop` en `427d090`.
- Flink CP: `repo=melisource/fury_rio-controlplane-flink`, paths `src/main/java/com/mercadolibre/rio/controlplaneflink/idempotency/IdempotencyGuard.java`, `TriggerStatusRecord.java`, `deployment/DeploymentProcessor.java`, `controller/DeploymentTriggerController.java` y handlers/jobs terminales; `develop` en `7af7e3f`.
- ClickHouse CP: `repo=melisource/fury_rio-controlplane-clickhouse`, paths `src/main/java/com/mercadolibre/rio/controlplane/clickhouse/deployment/application/ProcessDeploymentUseCase.java`, `adapter/rest/DeploymentEventController.java`, `deployment/KvsDeploymentStateService.java` y `config/KvsConfig.java`; `develop` en `a2ca40e`.
- Fury CP: `repo=melisource/fury_rio-controlplane-fury`, paths `src/main/kotlin/com/mercadolibre/rio_controlplane_fury/pusher/orchestrator/PusherOrchestrator.kt` y `pusher/persistence/PusherMappingRepository.kt`; `develop` en `7eb7932`.
- Diagnóstico del incidente: [[Playmaker — Doble dispatch al avanzar batches]] y [[Auditoría independiente — Informe del doble dispatch]].
- Flujo end-to-end: [[deploy-request-path]] y contrato por tipo: [[signals-context-flow]].

## Límites y contradicciones

- La revisión es de código y documentación local; no verifica bindings KVS live, retención real de BigQueue, métricas productivas ni despliegues activos en Fury.
- “Todos los CP usan KVS para un lock” es demasiado fuerte: Kafka y Flink sí comparten un guard CAS; ClickHouse tiene una implementación KVS con claim no distribuido; Fury usa QKVS para convergencia de desired state; no existe un lock cross-CP común.
- El resultado “finalize antes de publish” evita duplicar el resultado, pero abre una ventana de pérdida de resultado si el proceso muere entre ambas operaciones; el contrato debe decidir si prioriza at-most-once o replay con payload cacheado.
- El mutex del hotfix evita la interleaving observada, pero no convierte el evento Spring en durable ni demuestra confirmación de BigQueue; esas garantías pertenecen al refactor con tópico externo.
