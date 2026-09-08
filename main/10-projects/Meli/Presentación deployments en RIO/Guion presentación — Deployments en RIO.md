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

## Formato

- Duración objetivo: 10 a 12 minutos, más preguntas.
- Artefacto visual: `30-resources/grids/rio-deployments-critical-flow.html`.
- Tesis: un flujo se detiene cuando un actor confirma una etapa antes de dejar persistida la obligación de ejecutar la siguiente.
- Frase ancla: **un ACK confirma transporte; no confirma aceptación durable ni éxito del deployment.**

## Slide 1 — Deployments en RIO

### Objetivo

Abrir con el problema real: RIO distribuye un deployment entre varios dueños y algunas fronteras no tienen recuperación durable.

### Speech

“Quiero revisar el deployment completo, no sólo el camino feliz. La pregunta que guía la presentación es simple: si una instancia muere en cada frontera, ¿alguien puede reconstruir lo que faltaba hacer? RIO sí tiene MySQL, BigQueue, KVS, locks y timeouts, pero esas piezas no siempre forman una cadena de recuperación. Eso explica por qué algunos flujos pueden quedar detenidos aunque cada servicio, visto por separado, parezca estar funcionando.”

### Transición

“Partamos viendo quién posee cada parte del flujo y dónde cambia la responsabilidad.”

## Slide 2 — Flujo vigente y tecnologías

### Puntos que deben quedar claros

- Playmaker recibe el estado deseado y persiste la jerarquía de ejecución en MySQL.
- Eventos Spring `AFTER_COMMIT` y `@Async` disparan continuaciones locales.
- BigQueue usa `rio-deployment-trigger` para llegar a los control planes.
- Cada CP ejecuta contra Kafka, Flink, ClickHouse, Fury, Signals o Materializer y mantiene idempotencia en KVS/QKVS o NoSQL.
- Los terminales vuelven por `rio-deployment-result` y Playmaker avanza el siguiente batch.

### Speech

“El frontend pide reconciliar un pipeline. Playmaker calcula el delta y persiste en MySQL una execution, sus groups, component runs y deployments. Después del commit, un evento Spring local inicia el dispatch. La mayoría de los componentes viaja por BigQueue en `rio-deployment-trigger`; el control plane correspondiente recibe el mensaje, toca la infraestructura y mantiene estado de idempotencia en KVS o QKVS. Cuando termina, publica un `DeploymentResultMessage` en `rio-deployment-result`. Playmaker consolida ese resultado en MySQL y otro evento local intenta avanzar el siguiente batch. Materializer sigue como camino REST para storages y para tipos legacy que caen al catch-all.”

### Frase para señalar los marcadores rojos

“Los cuatro marcadores no dicen que el flujo falle siempre. Dicen que una caída en esa ventana puede dejar dos sistemas con versiones distintas de la verdad.”

## Slide 3 — Grid de durabilidad

### Objetivo

Comparar todas las fronteras con el mismo criterio: qué se confirmó, qué quedó durable y quién hace replay.

### Speech

“Esta tabla resume el problema. En el primer handoff, MySQL puede confirmar el deployment y el evento de dispatch seguir sólo en memoria. En Kafka, Flink y ClickHouse, BigQueue puede recibir HTTP 200 antes de que exista un job durable. Después, el recurso puede quedar listo o el KVS terminal, pero el resultado hacia Playmaker todavía puede perderse. Finalmente, Playmaker puede persistir que un batch terminó y perder el evento que debía iniciar el siguiente. Fury CP es la referencia más fuerte porque separa estado reportado de estado publicado y un reconciler vuelve a intentar desde QKVS.”

### Punto de énfasis

“La unidad de análisis correcta no es el servicio. Es cada frontera entre dos servicios.”

## Slide 4 — Muerte súbita de un control plane

### Speech

“Tomemos el ejemplo más claro. BigQueue hace push al CP. El handler acepta el request, lanza un `CompletableFuture` o trabajo equivalente y devuelve 200. Para BigQueue el mensaje ya quedó entregado. Si el pod muere antes de persistir el trabajo o completar el efecto, el executor desaparece con la instancia y BigQueue no tiene por qué reenviar. Playmaker sólo ve silencio. Si había timeout, eventualmente puede fallar el deployment; si el recurso alcanzó a crearse, podemos terminar con infraestructura real y Playmaker en `FAILED`. Si no alcanzó a crearse, tenemos un trabajo perdido. En ambos casos falta una aceptación durable antes del ACK.”

### Solución que presentar

“El CP debería persistir un inbox o job `ACCEPTED` con `deployment_id` antes del 2xx. Un worker con lease lo ejecuta y otra réplica puede tomarlo si el owner muere.”

### Transición

“Pero esta no es la única ventana, y algunas son bastante menos visibles.”

## Slide 5 — Fallas menos obvias

### Speech

“Hay cuatro detalles que vale la pena llevarse. Primero, si Playmaker cae después del commit inicial pero antes del adapter, `timeout_at` sigue en null, por lo que el job de timeouts ni siquiera selecciona ese deployment. Segundo, el Fury Lock del avance de batch evita dos avances simultáneos, pero no reconstruye un evento perdido. Tercero, en algunos CP se guarda el terminal en KVS antes de publicar el resultado; si publicar falla, una redelivery puede encontrar el terminal y descartar el mensaje, dejando a Playmaker esperando para siempre. Cuarto, un timeout de `STARTED` no sabe si el proveedor sigue trabajando: fallar por reloj puede crear un falso negativo y dejar un recurso huérfano.”

### Remate

“Más retries no solucionan estos casos por sí solos. Primero hay que saber qué quedó durable y si repetir el efecto es seguro.”

## Slide 6 — Materializer y routing

### Speech

“Materializer aparece principalmente en storages. Es owner explícito de `s3-bucket` y `gcs-bucket`, usa Fury NoSQL, WorkQueues, Terraform y Cloud Controller. Sin embargo, Playmaker conserva un catch-all REST para cualquier tipo que no esté en la allowlist BigQueue. Hoy `gcp-kafka-topic` es la contradicción concreta: Kafka CP lo implementa, pero la configuración base de Playmaker lo deja caer en Materializer. Además, Materializer persiste sagas, pero parte de la detección de pendientes depende de un índice en memoria y la task de WorkQueue se desprende a un future local. Por eso migrar storages no es sólo cambiar el transporte; hay que preservar saga, idempotencia y reconciliación.”

### Límite de certeza

“Esto está verificado en código local. Falta confirmar scopes, filtros y overrides vivos antes de afirmar qué porcentaje de tráfico usa cada ruta en producción.”

## Slide 7 — Deuda técnica propuesta

### Speech

“Propongo cuatro P0. Primero, outbox de dispatch en Playmaker para que ningún deployment persistido pierda su trigger. Segundo, reconciler de avance de batch para que una execution pueda continuar después de reiniciar. Tercero, inbox durable en Kafka, Flink y ClickHouse antes del ACK. Cuarto, separar efecto terminal de publicación terminal en todos los CP, siguiendo el patrón `reported/published` de Fury. Como P1 quedan reconciliar timeouts `STARTED`, unificar capabilities con routing, recuperar sagas de Materializer desde estado durable, restaurar el orden topológico y alertar estados varados.”

### Prioridad verbal

“Instrumentaría primero para medir incidencia, pero cerraría las ventanas P0 antes de sumar más lógica de retry.”

## Slide 8 — Contrato de recuperación

### Speech

“El objetivo no debería ser que nunca falle una instancia. El objetivo es que cada falla deje una próxima acción reconstruible. Para cualquier frontera deberíamos poder responder cinco preguntas: qué persistimos antes del ACK, quién retoma después de un restart, si el retry conserva identidad, si separamos el efecto de su notificación y cómo reconciliamos Playmaker, CP e infraestructura. Si alguna respuesta es ‘nadie’ o ‘queda en memoria’, ahí tenemos deuda de confiabilidad.”

### Cierre

“Hoy RIO tiene varias piezas correctas, pero las garantías cambian entre control planes. La mejora estructural es convertir cada handoff en un contrato durable. Eso nos permite pasar de flujos que a veces se paran a ejecuciones que convergen incluso cuando un pod muere en el peor momento.”

## Preguntas probables

### ¿BigQueue no debería redeliver automáticamente?

Sí, mientras el consumidor no haya confirmado la entrega. El problema aparece cuando el CP responde 2xx antes de aceptar el trabajo en un storage durable. Después de ese ACK, la muerte del executor local ya no pertenece al dominio de recuperación de BigQueue.

### ¿KVS no resuelve la idempotencia?

KVS puede evitar repetir un efecto, pero no garantiza que la continuación o el resultado lleguen al siguiente actor. Si el terminal se guarda antes de publicar y una redelivery descarta estados terminales, KVS puede bloquear la recuperación del mensaje perdido.

### ¿Por qué no reintentar todo lo que queda en `STARTED`?

Porque `STARTED` indica que el CP aceptó o comenzó el efecto. Repetir sin reconciliar puede crear recursos duplicados o ejecutar dos veces una operación no idempotente. Se necesita consultar el estado durable del CP o del proveedor.

### ¿Tenemos evidencia de que estos incidentes ocurren?

Tenemos reportes operacionales de flujos detenidos y ventanas de pérdida verificadas en el diseño. Aún falta instrumentación que atribuya frecuencia real a cada ventana. Conviene presentar la causalidad como técnicamente demostrable y la incidencia como una medición pendiente.

### ¿Qué patrón existente podemos reutilizar?

Fury CP separa `reportedDeploymentId` y `publishedDeploymentId`, mantiene desired/observed state en QKVS y usa un reconciler. Ese patrón permite terminar el efecto y seguir intentando la notificación en ticks posteriores, incluso tras un reinicio.

## Datos que conviene pedir después de la presentación

- Cantidad y edad máxima de deployments `REQUESTED` con `timeout_at = null`.
- Executions `RUNNING` cuyo batch actual está terminal y no tienen attempts en el siguiente batch.
- Diferencias entre terminales en KVS/QKVS y terminales recibidos por Playmaker.
- Timeouts `STARTED` que después generaron recursos o callbacks tardíos.
- Sagas de Materializer pendientes por más tiempo que su SLA.
- Tasa de reinicios de instancias en los CP y correlación temporal con deployments varados.

## Fuentes

- [[Deployments en RIO — flujo completo]] contiene el detalle técnico, criterios de aceptación y hashes verificados.
- [[Revisión de ads-signals-knowledge-library]] conserva las diferencias entre documentación y código.
- El Grid resume estos documentos; no reemplaza la fuente técnica ni afirma configuración viva de producción.
