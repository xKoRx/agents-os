---
type: doc
schema_version: 1
status: active
area: "[[Meli]]"
related:
  - "[[Presentación deployments en RIO]]"
  - "[[Deployments en RIO — flujo completo]]"
  - "[[RIO]]"
aliases:
  - Speech deployments RIO
  - Guion corto deployments RIO
tags:
  - kind/doc
  - area/meli
  - project/presentacion-deployments-rio
created: "2026-09-08"
updated: "2026-10-01"
---

# Guion presentación — Deployments en RIO

## Propósito

Explicar completamente el recorrido de un deploy de pipeline dentro de Playmaker: qué decide, qué entidades crea y cuándo, cómo entrega el trabajo y cómo procesa su resultado, cierra la execution y devuelve ese progreso mediante el polling del front. La meet se apoya en código y en las decisiones que explican ese recorrido.

## Recorrido acotado

Seis paradas en código, siguiendo el mismo caso de principio a fin. Como presupuesto orientativo se mantienen 20–25 minutos; el tiempo definitivo queda por ajustar al ensayar. La propuesta visual de seis capítulos sirve de apoyo: diagramas, estados y etiquetas cortas. El detalle se explica oralmente y al abrir código; no se copia el guion dentro de las slides. Este guion es la fuente del recorrido actual.

Caso ilustrativo: un pipeline tiene un topic y un engine que requieren deploy, más un componente sin cambios. El topic entra al primer batch, el engine al segundo y el componente sin cambios queda SKIP. El ejemplo permite explicar entidades, outputs y avance sin recorrer por separado cada control plane.

**Apertura:** “Voy a seguir una solicitud de deploy desde el front, a través de Playmaker y hasta la vuelta del polling: qué compara, qué guarda, cuándo sale cada mensaje y cómo una respuesta del CP hace que el pipeline continúe.”

**Base de código:** `melisource/fury_rio-playmaker`, `origin/master` local `3cd0daf6e17841ab79381f1eb5e2bd014ad68bd1`, revisado el 2026-10-01. El checkout está en otra revisión: para mostrar este recorrido, abrir los archivos de esa ref. La evidencia es de código local; configuración y release efectivas de producción siguen pendientes.

Los archivos Java indicados abajo son relativos a `src/main/java/com/mercadolibre/rio/playmaker/` dentro de ese repo. Abrirlos antes de la meet y mostrar sólo los métodos señalados.

## 1. Entra la solicitud: ¿qué hay que cambiar?

**Mostrar:** `service/impl/PipelineDeployServiceImpl.java`, método `deploy`; saltar a `service/pipeline/impl/DeltaComputationServiceImpl.java`, `evaluateComponent`, para explicar la comparación. El endpoint está en `controller/PipelineDeploymentController.java#deployPipeline`: `POST /data-products/{name}/environments/{envName}/pipeline/deploy`.

Antes de entrar a Playmaker, `useDeployPipeline` activa `isDeploying` y envía el POST desde el browser con `components`, `force` y `sourcePipelineExecutionId` opcionales. `api/pipeline/index.ts` valida membresía, path, body y freezes; llama a Playmaker y normaliza la respuesta. Una execution nueva vuelve con 202; COMPLETED reutilizada vuelve con 200 y no inicia polling. El BFF normaliza el 409 de execution equivalente en curso a una respuesta CONFLICT con su ID.

Playmaker busca DataProduct, Environment activo y Pipeline, obtiene al caller y aplica freezes. Esas entidades, los Component y sus ComponentDefinition ya existen; esta solicitud parte de esa configuración.

El delta se calcula por componente y environment. La definición deseada se resuelve desde rollback si se pidió, desde el Service de ese environment o desde la última definición global para el primer deploy. Se compara contra la definición del Deployment activo del Service. Sin Service o con definición distinta, resulta DEPLOY; con la misma definición, se evalúan remoción, fallo previo o Service terminado antes de decidir SKIP. Mostrar el orden real de los `if`, porque cambia qué condición prevalece.

Después se aplican el filtro opcional de componentes y `force`: puede convertir SKIP con configuración conocida en DEPLOY. El hash se calcula con las parejas `componentId:configId` de entradas no-SKIP. Se puede reutilizar una execution COMPLETED del mismo pipeline y hash; se rechaza una equivalente PENDING/RUNNING incluso con force. Si no hay entradas desplegables, se devuelve un error antes de crear la execution.

**Decisión a explicar:** el delta distingue configuración deseada por environment y configuración desplegada. El hash evita ciertas ejecuciones equivalentes; no equivale a un lock de todo el pipeline.

**Transición:** “Ya sabemos qué cambia. Ahora eso se convierte en registros de ejecución.”

## 2. Nace la ejecución: ¿qué registros aparecen antes del envío?

**Mostrar:** las llamadas `lifecycleService.create`, `enrichWithServiceIds` y `deploymentGroupService.create` en `deploy`; abrir `service/impl/DeploymentGroupServiceImpl.java#create` para ver el orden del primer dispatch. Como apoyo, `service/pipeline/impl/PipelineExecutionLifecycleServiceImpl.java#create` muestra los inserts.

| Momento | Registro | Qué representa en nuestro caso |
|---|---|---|
| `lifecycleService.create` | Una PipelineExecution PENDING | La reconciliación completa de ese pipeline y environment |
| Dentro del mismo create | Un ComponentRun PENDING por entrada no-SKIP | Topic y engine dentro de esa execution, con su definición y `runOrder`; el componente SKIP no genera run |
| `enrichWithServiceIds` | Service si falta | El slot `component × environment`; en siguientes deploys se reutiliza |
| `deploymentGroupService.create` | Un DeploymentGroup PENDING | La orquestación asociada a la execution: criticidad, estrategia, DP y environment |
| Dispatch del primer batch | Deployment por componente despachado | En este punto nace el del topic; el del engine todavía no existe |

`TopologicalSortServiceImpl` calcula los batches. En esta ref está activo `FORCE_CONFIG_ORDER`: orden 0 para no-engines y 1 para engines, en lugar de usar el orden topológico del DAG. Tras despachar el primer batch, group y execution pasan a RUNNING. El método de entrada es transaccional: las llamadas participan de la transacción antes de que el trigger externo salga.

**Distinción clave:** DeploymentGroup y batch son conceptos distintos. Este camino crea un group para la execution; los batches se reconocen por `ComponentRun.runOrder`. Los Deployments de los siguientes batches usarán ese mismo group.

**Transición:** “La execution ya conoce todos sus runs, pero sólo el batch habilitado obtiene Deployments.”

### Dentro de la segunda parada: nace el Deployment: ¿qué queda listo para despachar?

**Mostrar:** `service/pipeline/impl/BatchDispatchServiceImpl.java#dispatchItem`; abrir `service/pipeline/impl/DeploymentAttemptFactory.java#create` y `resolveCorrelationId` para ver los campos persistidos.

El dispatcher carga las definiciones y Services, valida los Deployments activos y, cuando corresponde, desactiva el anterior. Crea el nuevo Deployment ligado a Service, ComponentDefinition y group: estado REQUESTED, activo, `retryCount=0` y deadline corto de dispatch. Después genera o recupera la correlation UUID persistida.

Recién entonces resuelve los parámetros de la definición y arma el DispatchRequest. Los outputs guardados en los Services pueden alimentar parámetros de componentes posteriores. Finalmente publica `DeploymentDispatchRequestedEvent` dentro de Spring; todavía no es un trigger BigQueue.

**Identidades a mostrar:** el ID de la fila Deployment identifica el registro de MySQL; la correlation UUID identifica el intercambio asíncrono; el ID del group vincula la orquestación. ComponentRun representa el componente dentro de la execution y no tiene FK directa al Deployment.

**Decisión a explicar:** crear el Deployment antes de enviar permite encontrarlo si el resultado vuelve muy rápido. El deadline ya existe antes del listener: en esta ref dejó de ser correcto explicar que el Deployment nuevo nace con `timeout_at=null`.

**Transición:** “Hasta aquí construimos intención y request. El commit habilita el envío externo.”

## 3. Sale de Playmaker: ¿quién decide la ruta y arma el mensaje?

**Mostrar:** `service/pipeline/impl/DeploymentDispatchEventListener.java#onDispatchRequested`; seguir `DeploymentTransportRegistry.resolve` y terminar en `service/pipeline/impl/BigQueueDispatchAdapter.java#dispatch` / `buildTriggerMessage`.

El listener corre con `AFTER_COMMIT` y `@Async`: usa un thread distinto y la transacción de creación ya terminó. Primero reclama el dispatch y renueva su deadline corto; si el claim ya no aplica, omite ese evento. El registry elige adapter por tipo de componente y versión. `config/DeploymentRoutingConfig.java#resolveFor` usa primera coincidencia, con catch-all; la tabla base está en `src/main/resources/application.yml`, sección `controlplane.deployment-routing`.

Para BigQueue, Playmaker construye el DeploymentTriggerMessage con UUID, group, componente, DP, environment, operación, criticidad, parámetros y contexto opcional. Actualiza metadata y timeout de ejecución y publica en `rio-deployment-trigger`. BigQueue transporta al CP, que es el dueño del efecto sobre infraestructura. El ACK de entrega y el resultado de negocio son momentos distintos.

La otra ruta configurada es Materializer REST: `MaterializerRestAdapter.dispatch` llama a `materializerService.doMaterialize`; al aceptar la llamada actualiza el timeout de ejecución. El trabajo termina después mediante callback HTTP. `DeploymentLogController.create` procesa ese callback y `LegacyCallbackResultAdapter.adapt` publica un DeploymentResultMessage en el bus de resultados. El registry también soporta un adapter stream, pero el YAML base leído no selecciona esa ruta.

**Decisión a explicar:** el transporte se decide en Playmaker; la capacidad de un CP por sí sola no determina el routing. Aquí basta seguir la salida y vuelta del trabajo externo para continuar el recorrido de Playmaker.

**Transición:** “El CP ejecuta el efecto. Volvamos al momento en que Playmaker recibe el resultado.”

## 4. Vuelve el resultado: ¿qué entidad cambia y cómo encuentra el run?

**Mostrar:** `service/impl/DeploymentResultHandlerImpl.java#handle`, `resolveComponentRun` y las ramas de `routeByStatus`. La entrada BigQueue es `controller/DeploymentResultConsumerController.java#consumeDeploymentResult`, `POST /events/deployment/result`, seguida de `DeploymentResultConsumerServiceImpl.consume`.

El handler busca el Deployment por la correlation UUID del mensaje y conserva `materializationId` como fallback legacy. Resuelve el run usando dos relaciones: group → execution y Service → component. Con esa pareja busca el ComponentRun; no usa una FK directa Deployment → ComponentRun. Si el run ya es terminal, descarta el resultado tardío.

Dentro de la transacción, STARTED mueve el run a RUNNING y el Deployment a STARTED; IN_PROGRESS registra output sin avanzar el estado principal. COMPLETED cierra run y Deployment, limpia timeout y, cuando corresponde, deja Service RUNNING y Component ACTIVE. FAILED persiste el fallo y lo propaga a la orquestación.

Los outputs se integran en `Deployment.values` y `Service.values`. DeploymentLog aparece en el procesamiento de resultados: guarda output nuevo y los terminales que requieren registro; la deduplicación significa que no cada mensaje recibido crea otra fila. No son logs generales de la aplicación.

**Decisión a explicar:** el resultado actualiza progreso de ejecución y estado del Service. Un componente completado todavía no implica que todo el pipeline haya terminado.

**Transición:** “El topic terminó y dejó sus outputs. Veamos qué permite enviar ahora el engine.”

## 5. Continúa o termina: ¿quién habilita el próximo batch?

**Mostrar:** `service/pipeline/impl/OrchestrationServiceImpl.java#checkPrerequisites`, `checkGroupCompletion` y `propagateFailure`. Como puente, `BatchCompletedEventListener.onBatchCompleted` toma el evento emitido por COMPLETED después del commit.

El listener intenta serializar el avance por execution y próximo `runOrder` mediante Fury Lock y luego llama a la orquestación en otra transacción. Si encuentra contención, programa retries; si Fury Lock está indisponible, esta ref tiene un fallback que intenta avanzar sin esa serialización. La orquestación también comprueba qué componentes del siguiente batch ya tienen Deployment para evitar materializarlos de nuevo.

Lee los runs del `runOrder` actual. Mientras falten terminales, espera. Si hay fallo, propaga FAILED a group y execution y cancela runs pendientes de órdenes posteriores. Si el batch terminó correctamente, busca los PENDING del siguiente orden y vuelve a BatchDispatchService: ahí nace el Deployment del engine, dentro del mismo group. Si todos los runs están COMPLETED, cierra group y execution.

Cerrar con `service/pipeline/DeploymentTimeoutJob.java#processTimeout`: escanea deadlines vencidos y un backlog legacy sin deadline. Reintenta sólo DEPLOY en REQUESTED por BigQueue cuando cumple edad, intentos y relaciones necesarias; reutiliza la fila y publica otra UUID guardada en `materializationId`. STARTED vencido se falla sin reenviar para evitar un posible doble efecto. El timeout es una decisión de Playmaker sobre su espera, no una prueba de que el recurso externo no exista.

**Transición hacia el front:** “Una solicitud crea la execution y los runs; cada batch habilitado crea sus Deployments; cada resultado actualiza Deployment, Service y run; la orquestación vuelve a despachar o cierra el pipeline. Esos son los puntos donde Playmaker transforma intención en trabajo y trabajo en progreso.”

## 6. Vuelve a la UI: ¿qué lee el polling y cuándo termina?

**Mostrar:** `PipelineHistoryServiceImpl#getExecution` en Playmaker, `api/pipeline/index.ts` y `pipelineUtils.normalizeExecution` en el BFF, `useDeployPipeline.fetchExecution` / `startPolling` y `src/entities/Deployment.ts#isExecutionFullyTerminal` en el front.

El front guarda el ID recibido y hace un primer GET inmediato a `/data-products/{name}/environments/{env}/pipeline/history/{executionId}`. El BFF valida los parámetros y proxya la consulta. Playmaker comprueba que la execution pertenece al pipeline y environment consultados, ejecuta `resolveTimeoutsForExecution` y lee los runs ordenados por runOrder. Este GET es transaccional y puede escribir al resolver timeouts; el polling también participa de esa resolución lazy.

El DTO devuelve execution ID, pipeline, tipo, estado, timestamps y component runs con componente, definición, estado, orden y error. El BFF adapta snake_case a camelCase y run_order a order. El hook valida el ID de la respuesta y la generación vigente de la observación antes de actualizar la execution en React.

El polling encadena delays de 2, 4, 8, 16 y hasta 30 segundos. Los errores reinician el delay a 2 segundos; tres errores consecutivos detienen la observación. Al llegar a 10 minutos se detiene la ventana local, conservando el ID para retomar. Ninguna de estas detenciones cancela el trabajo del backend.

**Condición final:** `isExecutionFullyTerminal` exige estado agregado terminal (COMPLETED, FAILED o PARTIAL_FAILURE) y todos los runs terminales (COMPLETED, FAILED o CANCELLED). Entonces el hook detiene polling, limpia el ID activo y libera `isDeploying`. El cierre de la historia es la respuesta HTTP convertida en estado visible de la UI.

**Fuente del front:** `melisource/fury_ads-signals-frontend`, `origin/master` local `791f79dd8050e1432bdc5c936539b22dbaa4e35d`, contrastado el 2026-10-01. [Grid propuesto — request a polling](https://grid.adminml.com/d/01M3VWJ9GQ1FHABT2GJZEN1VPA/view), seis slides Dark Theme con extractos y enlaces a las refs verificadas.

## Preparación para la meet

En la segunda escena, preguntar si el Deployment del engine ya existe; revelar que sólo nació su ComponentRun. En la quinta, volver a ese engine y mostrar qué habilitó su Deployment. En el cierre, preguntar si detener el polling cancela el trabajo: el backend continúa.

Ensayar las seis paradas con el mismo ejemplo, dejando abiertas las clases principales y saltando a los helpers sólo para mostrar la línea que sostiene cada decisión. Usar los diagramas existentes cuando ayuden a reconocer entidades o transportes. Las preguntas sobre implementaciones internas de cada CP, incidencia de fallas y posibles correcciones se responden con el documento de referencia después del recorrido.

[[Deployments en RIO — flujo completo]] y el Grid anterior conservan la investigación de septiembre; algunas afirmaciones quedaron atrás del código actual. Para esta meet usar las entidades, deadlines y transiciones verificadas en este guion. El routing vivo y la release que corre en producción requieren otra evidencia.
