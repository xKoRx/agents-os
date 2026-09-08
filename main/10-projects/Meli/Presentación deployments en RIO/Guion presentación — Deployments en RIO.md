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
updated: "2026-09-08"
---

# Guion presentación — Deployments en RIO

## Propósito

Entregar un speech verificable para recorrer el flujo completo de deployments en RIO, explicar su modelo de datos y revisar después las fronteras de recuperación sin convertir la sesión en un pitch.

## Contenido

El documento organiza el relato slide por slide, conserva respuestas a preguntas probables y separa hechos verificados de configuración viva todavía pendiente de contraste.

## Formato

- Duración objetivo: 10 a 12 minutos, más conversación.
- Artefacto visual: `30-resources/grids/rio-deployments-critical-flow.html`.
- Propósito: mostrar mi lectura actual del flujo después del primer mes en el equipo, contrastarla con quienes conocen el sistema y después revisar las fronteras de recuperación.
- Tono: revisión técnica entre pares; describir lo verificado, separar las inferencias y dejar abiertas las configuraciones de producción todavía no contrastadas.
- Frase ancla: **un ACK confirma transporte; no necesariamente confirma que el trabajo quedó recuperablemente aceptado.**

## Slide 1 — Flujo completo de deployments

### Speech

“La idea de esta presentación es mostrar cómo entiendo hoy el flujo completo de deployments en RIO. Voy a partir por Playmaker: cómo calcula el cambio, qué guarda, qué mensaje construye y cómo lo distribuye. Después voy a seguir el efecto dentro del control plane y el regreso del resultado. Recién con ese mapa compartido voy a marcar las fronteras donde una caída podría dejar el flujo sin una continuación recuperable. Hay partes verificadas en código local y otras, como el routing vivo, que quiero validar con ustedes.”

### Transición

“Este es el recorrido completo, desde el delta hasta el siguiente batch.”

## Slide 2 — Del delta al siguiente batch

### Puntos que deben quedar claros

- `DeltaComputationService` compara el estado deseado con el estado desplegado por componente y environment. Devuelve `DEPLOY`, `UNDEPLOY` o `SKIP` y calcula el `desiredStateHash`.
- Playmaker crea primero la `PipelineExecution`, los `ComponentRun` y los `DeploymentGroup` en MySQL.
- El `Deployment` se crea después, cuando se despacha el batch: queda `REQUESTED` con correlation UUID dentro de una transacción. Después del commit, el listener `AFTER_COMMIT` llama al adapter.
- Playmaker, no BigQueue, estructura el trigger: el adapter construye el `DeploymentTriggerMessage` final, persiste `timeout_at` y publica.
- BigQueue transporta el mensaje por `rio-deployment-trigger`; no define el payload de negocio.
- Hay seis CPs sin contar KMS: Kafka, Flink, ClickHouse, Fury, Signals y Observability. Los cinco primeros son owners de efectos terminales; Observability consume una copia lateral.
- Todos usan algún KVS, pero con roles distintos: Kafka, Flink, ClickHouse y Signals usan Fury KVS; Fury CP usa QKVS; Observability usa KVS para capacidades laterales, no para cerrar el deployment.
- El resultado vuelve por `rio-deployment-result`. Playmaker actualiza el estado, agrega un `DeploymentLog` y mezcla los outputs en `Deployment.values` y `Service.values`.

### Speech

“La solicitud llega por HTTP y Playmaker calcula el delta con `DeltaComputationService`. Este servicio mira el estado deseado y lo compara con el estado activo por componente y environment; para cada componente decide `DEPLOY`, `UNDEPLOY` o `SKIP`. También construye el hash del estado deseado que identifica la reconciliación.”

“Con ese resultado, Playmaker persiste en MySQL la execution, los component runs y los grupos de despliegue. Cuando llega el turno de un batch, resuelve los parámetros y crea el `Deployment` como `REQUESTED`, con su correlation UUID. Esa transacción hace commit y recién entonces corre el listener Spring `AFTER_COMMIT` y `@Async`. El adapter arma el `DeploymentTriggerMessage`, escribe el deadline `timeout_at` y lo publica. BigQueue sólo lo transporta al CP correspondiente.”

“Sin contar KMS, aparecen seis CPs: Kafka, Flink, ClickHouse, Fury, Signals y Observability. Kafka, Flink, ClickHouse y Signals usan Fury KVS; Fury CP usa QKVS con desired/observed state; Observability también usa KVS, pero para administración lateral de observabilidad. No es owner del resultado terminal.”

“El CP realiza el efecto contra su tecnología: topics de Kafka en AWS o GCP, aplicaciones Flink, tablas o materialized views de ClickHouse, recursos Fury o signals en Catalog y collectors. Cuando publica el resultado, Playmaker lo consolida. `DeploymentLog` no son los logs generales de la app: es el historial de estados, outputs y mensajes de ese deployment. `Service.values` son los outputs técnicos acumulados del slot componente por environment, por ejemplo identificadores o endpoints que devolvió el CP.”

### Cómo leer los marcadores

“Los tres marcadores rojos agrupan tres familias: pérdida durante el dispatch de Playmaker, aceptación no durable dentro del CP y separación entre efecto, resultado y continuación. En la slide de detalle la última familia se divide en dos fronteras.”

## Slide 3 — Entidades y relaciones del deployment

### Speech

“Este es el modelo que usa Playmaker. Un `DataProduct` tiene un `Pipeline` versionado y componentes lógicos. Cada `Component` apunta a una `ComponentDefinition`, que es una versión concreta de su configuración. Un `Service` representa el slot de ese componente en un environment: conserva qué definición está activa y los outputs observados en `values`.”

“Una `PipelineExecution` representa una reconciliación completa de ese pipeline en un environment. Para cada componente cuyo delta no es `SKIP`, se crea un `ComponentRun`: es el estado de ese componente dentro de esa execution. Los `DeploymentGroup` organizan esos runs en batches.”

“Un `Deployment` es el registro del dispatch concreto hacia un Service y una definición dentro de un grupo. En el primer envío normalmente hay un ComponentRun y un Deployment para ese componente. No existe una FK directa entre ambos: al volver el resultado se relacionan a través del group y la execution, más el `Service.componentId`. Además, un retry automático de un `REQUESTED` puede reutilizar la misma fila Deployment, incrementar `retryCount` y publicar con otro UUID; por eso Deployment tampoco equivale exactamente a un único intento de transporte.”

“La correlation UUID es el identificador del mensaje asíncrono: permite unir el trigger y el resultado con el Deployment. No es la identidad del componente ni de la execution.”

### Pifias o deuda de abstracción a mencionar

- `DataProduct` conserva un campo `environment` legacy, aunque el modelo actual permite varias entidades `Environment` por DP. Que un DP aparezca en más de un environment es una huella del modelo anterior, no la regla nueva que queremos comunicar.
- `ComponentRun` y `Deployment` expresan niveles distintos, pero su relación es indirecta.
- `Service.values` mezcla outputs técnicos sucesivos en un JSON; sirve para resolver parámetros posteriores, pero no es una entidad tipada por recurso.

### Transición

“Hasta aquí el camino BigQueue. Materializer sigue representando el camino anterior y hoy convive con esta máquina de estados.”

## Slide 4 — Materializer acepta por REST y termina asíncronamente

### Speech

“Históricamente este flujo pasaba por Materializer vía REST. Para los tipos que todavía usan esa ruta, así funciona hoy: Playmaker construye el request y agrega una callback URL. El POST a `/materializations/` no espera a que exista la infraestructura; Materializer persiste una materialization y su stack como `PENDING`, encola trabajo y responde 201 con un `materializationId`.”

“La ejecución continúa después mediante WorkQueue y un worker que llega a Terraform o Cloud Controller. Cuando hay avances o un terminal, Materializer hace otro request HTTP, un POST a `/deployments/{id}/logs` de Playmaker. Playmaker normaliza ese callback legacy a un `DeploymentResultMessage` y desde ahí usa la misma consolidación que el camino BigQueue.”

“Sobre el estado actual, el YAML base deja S3 y GCS como owners explícitos de Materializer y mantiene un catch-all legacy. No afirmaría todavía que sólo queda storage: `gcp-kafka-topic` no aparece en las rutas BigQueue del YAML base, aunque Kafka CP sí lo implementa. Puede haber configuración viva que cambie esa resolución y eso lo tenemos que confirmar.”

### Respuesta corta a la duda REST

“No ocurre todo dentro del request de Playmaker. El request síncrono sólo acepta y devuelve `PENDING`; el efecto y los callbacks ocurren después.”

## Slide 5 — Dónde puede quedar un gap

### Speech

“Después de entender el recorrido, estas son las cuatro fronteras concretas que me parece útil revisar, agrupadas en las tres familias de la slide 2. La primera está entre el commit de MySQL y la publicación del trigger. `AFTER_COMMIT` significa que la transacción que creó el Deployment ya terminó correctamente; el listener corre después y cualquier escritura posterior usa otra transacción. `timeout_at` es el deadline para detectar un Deployment sin resultado. Nace en null y el adapter lo completa antes de publicar. Si Playmaker muere antes de que corra el adapter, el scanner de vencidos nunca selecciona esa fila.”

“La segunda está entre el HTTP 200 del CP y el trabajo real. Si el handler responde y luego desprende un executor local, la instancia puede morir después del ACK sin que BigQueue tenga motivo para redeliver.”

“La tercera separa el efecto del resultado: el recurso o el KVS pueden quedar terminales y la publicación fallar. La cuarta separa la consolidación del resultado del siguiente batch: Fury Lock evita dos avances concurrentes, pero no reconstruye un evento Spring perdido.”

“Fury CP es un ejemplo útil porque separa `reportedDeploymentId` de `publishedDeploymentId`. QKVS guarda desired y observed state; el reconciler adquiere un lease, ejecuta el efecto y marca `reportedDeploymentId`. Sólo después de publicar el resultado marca `publishedDeploymentId`. Si los marcadores quedan distintos, otro tick vuelve a intentar la publicación incluso después de un reinicio.”

“En la slide dejé sólo las fronteras y el mecanismo de Fury como contraste. Las alternativas generales —outbox, inbox durable, WorkQueue o reconciler— quedan para la conversación posterior, porque requieren decidir qué garantía buscamos en cada frontera.”

## Slide 6 — La inconsistencia depende del momento de la caída

### Speech

“La muerte súbita de un CP es un caso, pero Playmaker puede caer en la misma clase de problema. Si muere durante el fan-out posterior al commit, pueden quedar todos los Deployments persistidos y sólo una parte de los triggers publicados. Los que nunca llegaron al adapter incluso pueden seguir sin timeout.”

“En el CP, el corte puede ocurrir después del HTTP 200 y antes de persistir o terminar el trabajo. Y más adelante el recurso puede existir sin que Playmaker reciba el resultado, o Playmaker puede guardar el resultado y perder el evento que debía iniciar el siguiente batch.”

“Por eso el síntoma no siempre es el mismo: podemos ver intención sin trigger, sólo parte de los componentes enviados, infraestructura real sin terminal en Playmaker, o un batch completo sin continuación. Mi pregunta para la revisión es qué estado durable existe hoy en cada corte y quién reconstruye la próxima acción después de un reinicio.”

### Cierre

“Hasta acá llega mi lectura del código y la documentación. Me interesa validar primero si el modelo del flujo es correcto y, sobre esa base, cuáles de estas fronteras ya tienen mitigaciones operacionales o configuración que no alcancé a ver.”

## Preguntas probables

### ¿BigQueue no debería redeliver automáticamente?

Sí, mientras el consumidor no haya confirmado la entrega. El problema aparece cuando el CP responde 2xx antes de aceptar el trabajo en un storage durable. Después de ese ACK, la muerte del executor local ya no pertenece al dominio de recuperación de BigQueue.

### ¿El trigger sólo envía o también estructura el mensaje?

BigQueue sólo transporta. Playmaker resuelve parámetros, crea el Deployment y arma el payload del `DeploymentTriggerMessage` en el adapter usando el contrato de `rio-sdk-events`.

### ¿KVS participa en el flujo de deployment?

Sí, principalmente dentro de los CP para idempotencia, claims, desired/observed state o gestión lateral. No reemplaza MySQL de Playmaker ni la entrega de BigQueue.

### ¿KVS no resuelve toda la recuperación?

No. Puede evitar repetir un efecto, pero no garantiza que la continuación o el resultado lleguen al siguiente actor. Si el terminal se guarda antes de publicar y una redelivery descarta estados terminales, KVS incluso puede bloquear la recuperación de la publicación perdida.

### ¿Qué es exactamente un ComponentRun?

Es la representación del estado de un componente lógico dentro de una `PipelineExecution`. Se crea uno por componente con delta distinto de `SKIP`. El `Deployment` registra el dispatch de ese componente hacia su Service y definición dentro de un grupo; no existe una FK directa entre ambos.

### ¿Qué son `DeploymentLog` y `Service.values`?

`DeploymentLog` es historia de resultados del deployment, no los logs generales de la aplicación. `Service.values` es el JSON con outputs técnicos acumulados del componente en ese environment, actualizado a partir de las respuestas de los CP.

### ¿Por qué no reintentar todo lo que queda en `STARTED`?

Porque `STARTED` indica que el CP aceptó o comenzó el efecto. Repetir sin reconciliar puede crear recursos duplicados o ejecutar dos veces una operación no idempotente. Se necesita consultar el estado durable del CP o del proveedor.

### ¿Tenemos evidencia de que estos incidentes ocurren?

Hay reportes operacionales de flujos detenidos y las ventanas de pérdida existen en el diseño observado. Falta instrumentación que atribuya frecuencia real a cada ventana. Conviene separar causalidad técnicamente posible de incidencia medida.

## Datos que conviene pedir después de la presentación

- Cantidad y edad máxima de deployments `REQUESTED` con `timeout_at = null`.
- Executions `RUNNING` cuyo batch actual está terminal y no tienen deployments en el siguiente batch.
- Diferencias entre terminales en KVS/QKVS y terminales recibidos por Playmaker.
- Timeouts `STARTED` que después generaron recursos o callbacks tardíos.
- Sagas de Materializer pendientes por más tiempo que su SLA.
- Routing vivo efectivo de `gcp-kafka-topic`, scopes y overrides por componente.
- Reinicios de instancias en Playmaker y CPs correlacionados con executions varadas.

## Fuentes

- [[Deployments en RIO — flujo completo]] contiene el detalle técnico y las fronteras de evidencia.
- [[Revisión de ads-signals-knowledge-library]] conserva las diferencias entre documentación y código.
- El Grid resume estos documentos; no reemplaza la fuente técnica ni afirma configuración viva de producción.
