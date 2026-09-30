---
type: resource
schema_version: 1
status: active
area: "[[Meli]]"
sources: ["[[Repositorios RIO — Ambientes locales (2026-09-30)]]"]
last_verified: "2026-09-30"
confidence: "high"
aliases: ["Ambientes locales RIO", "Comparativa control planes locales", "Research Kafka local real"]
tags: ["kind/resource", "area/meli", "app/rio-controlplane-kafka"]
created: "2026-09-30"
updated: "2026-09-30"
---

# Ambientes locales RIO — Comparativa de implementaciones

## Síntesis vigente

**Recomendación:** extender `local,local-integration` de Playmaker para conectar [[rio-controlplane-kafka]] real y ejecutar su lógica existente sobre un cluster Apache Kafka en Docker Compose. La base ya existe; falta completar la integración del control plane, acciones/PEEK e idempotencia. Para cubrir replicación 1–3 se proponen tres brokers. Usar KVS real de Fury sandbox inicialmente, tomando el precedente de KMS, sujeto a demostrar la configuración del cliente Toolkit de Kafka.

La evidencia de código fue contrastada el **2026-09-30**. La propuesta todavía no tiene validación de ejecución. Su entrega se gestiona en [[Kafka — Ambiente local con servicios reales]].

### Implementaciones encontradas

| Aplicación | Infraestructura/herramientas encontradas | Qué ejecuta realmente | Brecha frente al pedido |
|---|---|---|---|
| [[rio-playmaker]] | Compose MySQL `8.0.32`; Compose Apache Kafka `3.9.1` KRaft; scripts Bash/Gradle; perfiles `local` y `local-integration`; Spring Kafka | MySQL durable; publicación de triggers y consumo de resultados serializados por Kafka real; retries y DLT del listener | No arranca un CP. El perfil sólo reemplaza transporte de deployments. Acciones y PEEK siguen con adapters locales; KVS/locks tienen sustitutos locales. |
| [[rio-controlplane-kafka]] | `docker-compose.yml` con Apache Kafka `3.9.0` KRaft, un broker; healthcheck; perfiles por `SCOPE`; `AdminClient`; módulo Testcontainers declarado | Un broker real disponible para clientes. AWS usa conexión plaintext; GCP usa OAuth y un provisioner real | Compose no configura por sí solo la app, routing, transporte ni KVS. SDK BigQueue local escribe a archivos; sin KVS configurado el guard corre degradado. GCP exige credenciales de SA; RF default 2 no cabe en un broker. |
| [[rio-controlplane-clickhouse]] | Compose ClickHouse, volúmenes, healthcheck, usuario SQL local y perfil `local` | Operaciones SQL contra ClickHouse real por HTTP, con modelo on-premise | BigQueue local escribe a archivos y el estado/lock de deployment tiene variantes locales. El Compose usa `latest`; no representa un estándar de versionado para copiar literalmente. |
| [[rio-controlplane-flink]] | Perfil local, configuración GCP/AWS, endpoints de Cloud Controller y credenciales; Testcontainers declarado | Clientes a servicios externos si están configurados | No se encontró un stack Flink local autocontenido en la base revisada. `LocalBigQueueDeploymentPublisher` sólo loguea; KVS tiene fallback no-op si no se configura el contenedor pertinente. |
| [[rio-controlplane-fury]] | Toolkit QKVS y productores BigQueue con inicialización lazy; perfiles; colecciones Bruno | Integraciones corporativas cuando se usan los clientes reales configurados | La inicialización lazy permite diferir la conexión; no crea infraestructura local. No se encontró Compose/runner autocontenido en la base revisada. |
| [[rio-controlplane-kms]] | Perfil `local`, SDKs y guía explícita de Fury Sandbox Services/KVS | KVS sandbox real y servicios de cifrado/cloud con configuración válida | Solución híbrida dependiente de servicios corporativos. Los datos de sandbox del README son de KMS y no deben reutilizarse para Kafka. Compatibilidad del Toolkit KVS de Kafka requiere prueba propia. |
| [[rio-controlplane-observability]] | Perfiles, clientes AWS/GCP y KVS configurable | APIs cloud/KVS cuando se configuran | En local hay fallback KVS a memoria; sin configuración usa no-op. No se encontró Compose/runner autocontenido en la base revisada. |
| [[rio-controlplane-signals]] | Perfil local, script Python HTTP, pruebas `.http`; branch `feature/local-docker-setup` con Compose app + Python | Aplicación real contra un stand-in local de Catalog/Collector, o servicios externos cuando se cambian URLs | El Compose candidato levanta un mock Python, no Catalog/Collector reales. Su `LocalFileBigQueueClient` sólo loguea, y el estado es en memoria. |
| [[rio-materializer]] | Scripts Bash/Gradle y `docker run` de Bitnami Kafka `latest` | Broker Kafka real para uso local, con múltiples integraciones sustituidas | Script borra el contenedor global `kafka` y usa `latest`; no hay un entorno reproducible y aislado completo para copiar. |
| [[rio-sdk-events]] | DTO tipados, fábrica BigQueue y `LocalFileBigQueueClient` | Serialización a archivos JSON individuales en local | Captura de eventos para inspección; no entrega broker→CP→Playmaker. |

### Qué hay en común

- **Activación/configuración:** `SCOPE` y perfiles Spring seleccionan `application-<perfil>.yml`; configuración por archivos/env y `bootRun` permiten desarrollar desde host/IDE.
- **Servicios abiertos reales en Docker:** Playmaker usa MySQL y Kafka; ClickHouse usa su servidor real; Kafka tiene su broker. Los launchers actuales dejan las JVM en el host, lo que facilita debugging.
- **Integraciones corporativas:** se resuelven mediante SDKs y configuración/credenciales de Fury, o se sustituyen con archivos, logs, memoria y no-op. No se encontró una plataforma común autocontenida que replique todo Fury en los repos revisados.
- **Contratos comunes:** `rio-sdk-events` proporciona los mensajes de trigger/result; compartir el nombre del DTO no demuestra compatibilidad cuando los repos usan versiones diferentes.
- **Tests:** varias apps declaran Testcontainers. En Kafka se encontró la dependencia del módulo Kafka, pero no una instancia `KafkaContainer` en los tests de la base examinada; los tests Spring revisados reemplazan dependencias con Mockito. La dependencia declarada no demuestra integración con broker real.

### La base concreta de Playmaker

`local/00-integration-pipeline.sh` inicia MySQL y Kafka, crea `rio-deployment-trigger-local`, `rio-deployment-result-local` y `rio-deployment-result-local-dlt`, y ejecuta Playmaker con `local,local-integration`.

`LocalKafkaDeploymentTriggerProducer` publica JSON de `DeploymentTriggerMessage` y espera ACK del broker. `LocalKafkaDeploymentResultListener` consume JSON de `DeploymentResultMessage`, valida los campos mínimos y delega al `DeploymentResultConsumerService` real. Su error handler tiene retries acotados y DLT. `LocalKafkaBootstrapGuard` restringe el bootstrap a una dirección loopback.

La arquitectura del mismo repo declara explícitamente pendiente el nivel L1: un servicio real del ecosistema conectado. Por tanto, la oportunidad es completar esa pieza. El flujo actual de Kafka CP recibe triggers HTTP de BigQueue; le faltan listeners locales equivalentes y publicación de resultados al broker local.

### Brechas específicas que debe resolver Kafka

1. **Routing y conexión:** incluir fixtures de routing locales que apunten al Compose. El cluster GCP usa una fábrica OAuth concreta; desacoplar la obtención del cliente para que el provisioner real pueda operar contra Kafka local. Ese cambio se limita al perfil de integración; no debe producir una condición de éxito sintética.
2. **Replicación:** `GcpTopicParams` define RF default 2 y rango 1–3. Tres brokers permiten cubrir esos valores y reassignment. Un broker sólo permite RF=1 y obliga a cambiar las entradas o defaults de la prueba.
3. **Resultados:** reemplazar el cliente de archivos de `BigQConfig` en el perfil de integración por publicación a Kafka real para deployments y acciones. Mantener la serialización, IDs y errores del SDK.
4. **Idempotencia:** `IdempotencyGuard` necesita KVS real con versión, create/CAS y TTL. `NoOpKvsClient` falla intencionalmente y activa el modo degradado; ese arranque no certifica deduplicación.
5. **Acciones y PEEK en Playmaker:** su `BigQueueActionsProducerLocal` es no-op y `KafkaControlPlaneClientImplLocal` devuelve un mensaje sintético incluso cuando se combina `local` con `local-integration`. Ambos necesitan selección/configuración específica para el CP real.
6. **Contratos:** Playmaker declara SDK Events `1.5.0`; Kafka `1.3.1`. Verificar JSON producido/consumido y campos desconocidos con esas versiones antes de decidir si una actualización del SDK resulta necesaria.
7. **Semántica de transporte:** Kafka es un sustituto local real del transporte. BigQueue usa entrega HTTP push, redelivery y configuración propias; el broker Kafka no demuestra equivalencia operacional. Preservar los handlers de negocio y registrar la brecha de ACK anticipado/procesamiento asíncrono que aparezca en los escenarios.

### Recomendación de diseño

| Pieza | Solución propuesta | Razón y límite |
|---|---|---|
| Arranque | Extender los Compose/scripts de Playmaker, con un perfil compartido de integración | Es el precedente más cercano y ya tiene transporte serializado. Evitar stacks independientes compitiendo por puertos/nombres. |
| Broker | Apache Kafka JVM en KRaft, tres brokers; listeners internos y loopback externos; imágenes fijadas y volúmenes | Kafka real, compatible con RF 1–3. Alinear inicialmente con la familia 3.9 usada por ambos repos; verificar tag/digest y soporte al implementar. |
| Aplicaciones | Playmaker y Kafka CP como JVM reales en host/IDE, iniciadas por un launcher común | Mantiene el patrón existente y facilita debugging; el transporte y la infraestructura sí son servicios reales. |
| Lógica | Adaptadores locales que invocan los procesadores, validadores y provisioners existentes | Permite observar fallas y efectos del código que se entrega, sin duplicar el negocio. |
| Persistencia/idempotencia | Fury KVS sandbox real, aislado por proyecto/run según política soportada | Precedente de KMS. Configuración de Toolkit KVS/CAS/TTL por demostrar; requiere conectividad corporativa y puede impedir trabajo offline. |
| Automatización | Testcontainers para regresiones con broker real y pruebas E2E sobre Compose | Son complementarios: tests efímeros y ambiente diario con datos persistentes. Mantener los mismos escenarios críticos. |
| Servicios administrados | Validación separada en un ambiente real no productivo para OAuth GCP y BigQueue | El cluster local cubre operación Kafka; no certifica resolución de secretos ni autenticación/entrega administrada. |

El Compose debe tener healthchecks y espera real de disponibilidad. Docker documenta que iniciar un contenedor no implica que el servicio esté listo y que `service_healthy` permite esperar su healthcheck. [Fuente primaria de Compose](https://docs.docker.com/compose/how-tos/startup-order/).

Apache distribuye la imagen JVM `apache/kafka`, también para la familia 3.9 utilizada por estos repos. [Documentación de Apache Kafka](https://kafka.apache.org/39/getting-started/docker/). Testcontainers tiene soporte específico para esa imagen y listeners de red adicionales. [Documentación del módulo Kafka](https://java.testcontainers.org/modules/kafka/).

### Alternativas consideradas

| Alternativa | Evaluación |
|---|---|
| Sólo usar el Compose actual de Kafka | Útil para un broker aislado; no conecta orquestación/resultados y deja RF/idempotencia incompletos. |
| Copiar el loopback o los clients locales de archivos/memoria | No satisface los efectos físicos ni entrega entre servicios requerida. |
| Copiar Signals Compose | Levanta un stand-in Python; su arquitectura no resuelve este caso con servicios reales. |
| Usar exclusivamente servicios reales de test de Fury/cloud | Da mayor fidelidad de proveedores, pero reduce aislamiento/reproducibilidad del ciclo de desarrollo. Mantenerlo para lo que Compose no cubre. |
| Introducir Redis/PostgreSQL como reemplazo local de KVS | Puede habilitar persistencia real offline, pero exige otro contrato y no demuestra Fury CAS/TTL. Considerar después si offline es un requisito. |
| Introducir Kubernetes local, Tilt, LocalStack o Redpanda | No se encontró una implementación común de esas herramientas en las fuentes examinadas que justifique incorporarlas para este alcance. Kafka/Compose ya tienen precedentes directos. |

## Evidencia y provenance

- [[Repositorios RIO — Ambientes locales (2026-09-30)]] conserva commits exactos, ramas, archivos seleccionados y estado de actualización.
- Los archivos de base `develop` de los CP/Playmaker y `master` del SDK se leyeron directamente desde las versiones registradas. También se inspeccionaron los candidatos de branches locales de Signals después del pull.
- La compatibilidad JSON, la conectividad KVS sandbox, las imágenes y el funcionamiento integrado aún requieren prueba de ejecución.

## Límites y contradicciones

- Esta comparación certifica qué contiene el código inspeccionado. No identifica la release desplegada en producción ni demuestra que un entorno local funciona: no se inició ninguno durante el discovery.
- La búsqueda de variantes se acotó a las bases vigentes y branches con nombres relacionados con local/Docker/integración disponibles en las referencias consultadas; no es una auditoría de todas las ramas históricas.
- Las fichas de aplicaciones del vault tienen información histórica, por ejemplo el stack Spring 3/Java 21 de Kafka. La fuente contrastada para este análisis es el commit actual: Kafka ya declara Spring Boot 4.1.1 y Java 25 en su documentación. Esa ficha no se modificó como parte de este alcance.
- La documentación externa de Fury Sandbox no fue accesible por el navegador. El precedente sandbox se fundamenta en el README y configuración de KMS; su viabilidad para Kafka Toolkit se mantiene pendiente, sin afirmar que basta copiar variables.
- La recomendación es híbrida para dependencias Fury y no garantiza operación completamente offline. El requisito confirmado es ejecutar Kafka y el control plane con servicios reales.
