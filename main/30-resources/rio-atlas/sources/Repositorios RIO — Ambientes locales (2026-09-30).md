---
type: source
schema_version: 1
status: active
area: "[[Meli]]"
source_url: "https://github.com/melisource/fury_rio-playmaker/blob/f087e4b7cc185d93618de4bdeaeb76b53486ac47/docs/architecture.md"
repo: "melisource/fury_rio-playmaker"
path: "docs/architecture.md"
author:
published:
captured: "2026-09-30"
license:
checksum:
supersedes:
superseded_by:
aliases: ["Evidencia ambientes locales RIO 2026-09-30"]
tags: ["kind/source", "area/meli"]
created: "2026-09-30"
updated: "2026-09-30"
---

# Repositorios RIO — Ambientes locales (2026-09-30)

## Referencia

- **Origen resoluble:** repositorios `melisource/fury_rio-*`, enlazados a commits inmutables en la tabla y el catálogo siguiente.
- **Fecha de captura:** 2026-09-30.
- **Método:** `git pull` literal sobre diez bases limpias y lectura de archivos. Kafka y Playmaker se examinaron primero por GitHub API/tarball y después sus `develop` existentes se actualizaron desde worktrees limpios, preservando los checkouts originales con trabajo pendiente. Los SHAs finales coincidieron con las fuentes remotas leídas. Copias de análisis temporales fuera del vault.

## Alcance

Siete control planes RIO más Playmaker; Materializer y SDK Events como precedentes/dependencias. Búsqueda enfocada por Compose, perfiles/configuración local, adaptadores y clientes reales, Testcontainers, sandbox y runners.

| Repo | Base examinada | Commit exacto | Actualización local |
|---|---|---|---|
| `rio-controlplane-kafka` | `develop` | [c9355395ef4b2bf438f0eb44528e24fa76ca498c](https://github.com/melisource/fury_rio-controlplane-kafka/tree/c9355395ef4b2bf438f0eb44528e24fa76ca498c) | Base actualizada en worktree limpio; checkout original preservado |
| `rio-controlplane-flink` | `develop` | [7c645ea92f86650744a3c5ee1bad0012633ef0e9](https://github.com/melisource/fury_rio-controlplane-flink/tree/7c645ea92f86650744a3c5ee1bad0012633ef0e9) | Base actualizada con git pull |
| `rio-controlplane-clickhouse` | `develop` | [afbf0f07b18a4a9fe1032932b71fba2ae56e98af](https://github.com/melisource/fury_rio-controlplane-clickhouse/tree/afbf0f07b18a4a9fe1032932b71fba2ae56e98af) | Base actualizada con git pull |
| `rio-controlplane-fury` | `develop` | [849a9f68bc83bee204264846e541c43c48b66fc8](https://github.com/melisource/fury_rio-controlplane-fury/tree/849a9f68bc83bee204264846e541c43c48b66fc8) | Base actualizada con git pull |
| `rio-controlplane-kms` | `develop` | [7fe77453c4e14ce4ee0e368188902c8ecabc21f2](https://github.com/melisource/fury_rio-controlplane-kms/tree/7fe77453c4e14ce4ee0e368188902c8ecabc21f2) | Base actualizada con git pull |
| `rio-controlplane-observability` | `develop` | [c5afde4eea49b0c9d820ff873ff86f618ffc0a32](https://github.com/melisource/fury_rio-controlplane-observability/tree/c5afde4eea49b0c9d820ff873ff86f618ffc0a32) | Base actualizada con git pull |
| `rio-controlplane-signals` | `develop` | [ce29224f7f619cb91b52c64038ce3f6fbf1143ed](https://github.com/melisource/fury_rio-controlplane-signals/tree/ce29224f7f619cb91b52c64038ce3f6fbf1143ed) | Base actualizada con git pull |
| `rio-playmaker` | `develop` | [f087e4b7cc185d93618de4bdeaeb76b53486ac47](https://github.com/melisource/fury_rio-playmaker/tree/f087e4b7cc185d93618de4bdeaeb76b53486ac47) | Base actualizada en worktree limpio; checkout original preservado |
| `rio-materializer` | `develop` | [c10e6f37e53346b958b77059c1c949ea17521d7f](https://github.com/melisource/fury_rio-materializer/tree/c10e6f37e53346b958b77059c1c949ea17521d7f) | Base actualizada con git pull |
| `rio-sdk-events` | `master` | [ad2c98b806cffb88b23513f87785932aa1707ea4](https://github.com/melisource/fury_rio-sdk-events/tree/ad2c98b806cffb88b23513f87785932aa1707ea4) | Base actualizada con git pull |

### Archivos seleccionados

#### rio-controlplane-kafka

- [docker-compose.yml](https://github.com/melisource/fury_rio-controlplane-kafka/blob/c9355395ef4b2bf438f0eb44528e24fa76ca498c/docker-compose.yml).
- [README.md](https://github.com/melisource/fury_rio-controlplane-kafka/blob/c9355395ef4b2bf438f0eb44528e24fa76ca498c/README.md).
- [build.gradle](https://github.com/melisource/fury_rio-controlplane-kafka/blob/c9355395ef4b2bf438f0eb44528e24fa76ca498c/build.gradle).
- [src/main/resources/application-local.yml](https://github.com/melisource/fury_rio-controlplane-kafka/blob/c9355395ef4b2bf438f0eb44528e24fa76ca498c/src/main/resources/application-local.yml).
- [src/main/java/com/mercadolibre/rio_controlplane_kafka/config/BigQConfig.java](https://github.com/melisource/fury_rio-controlplane-kafka/blob/c9355395ef4b2bf438f0eb44528e24fa76ca498c/src/main/java/com/mercadolibre/rio_controlplane_kafka/config/BigQConfig.java).
- [src/main/java/com/mercadolibre/rio_controlplane_kafka/config/KvsConfig.java](https://github.com/melisource/fury_rio-controlplane-kafka/blob/c9355395ef4b2bf438f0eb44528e24fa76ca498c/src/main/java/com/mercadolibre/rio_controlplane_kafka/config/KvsConfig.java).
- [src/main/java/com/mercadolibre/rio_controlplane_kafka/deployment/gcp/topic/GcpTopicParams.java](https://github.com/melisource/fury_rio-controlplane-kafka/blob/c9355395ef4b2bf438f0eb44528e24fa76ca498c/src/main/java/com/mercadolibre/rio_controlplane_kafka/deployment/gcp/topic/GcpTopicParams.java).
- [src/main/java/com/mercadolibre/rio_controlplane_kafka/deployment/gcp/topic/GcpTopicProvisioningServiceImpl.java](https://github.com/melisource/fury_rio-controlplane-kafka/blob/c9355395ef4b2bf438f0eb44528e24fa76ca498c/src/main/java/com/mercadolibre/rio_controlplane_kafka/deployment/gcp/topic/GcpTopicProvisioningServiceImpl.java).
- [src/main/java/com/mercadolibre/rio_controlplane_kafka/cloud/aws/AwsMskConnectionFactory.java](https://github.com/melisource/fury_rio-controlplane-kafka/blob/c9355395ef4b2bf438f0eb44528e24fa76ca498c/src/main/java/com/mercadolibre/rio_controlplane_kafka/cloud/aws/AwsMskConnectionFactory.java).
- [src/main/java/com/mercadolibre/rio_controlplane_kafka/idempotency/IdempotencyGuard.java](https://github.com/melisource/fury_rio-controlplane-kafka/blob/c9355395ef4b2bf438f0eb44528e24fa76ca498c/src/main/java/com/mercadolibre/rio_controlplane_kafka/idempotency/IdempotencyGuard.java).

#### rio-playmaker

- [README.md](https://github.com/melisource/fury_rio-playmaker/blob/f087e4b7cc185d93618de4bdeaeb76b53486ac47/README.md).
- [docs/architecture.md](https://github.com/melisource/fury_rio-playmaker/blob/f087e4b7cc185d93618de4bdeaeb76b53486ac47/docs/architecture.md).
- [docker-compose.yaml](https://github.com/melisource/fury_rio-playmaker/blob/f087e4b7cc185d93618de4bdeaeb76b53486ac47/docker-compose.yaml).
- [docker-compose.kafka.yaml](https://github.com/melisource/fury_rio-playmaker/blob/f087e4b7cc185d93618de4bdeaeb76b53486ac47/docker-compose.kafka.yaml).
- [local/00-integration-pipeline.sh](https://github.com/melisource/fury_rio-playmaker/blob/f087e4b7cc185d93618de4bdeaeb76b53486ac47/local/00-integration-pipeline.sh).
- [src/main/resources/application-local-integration.yml](https://github.com/melisource/fury_rio-playmaker/blob/f087e4b7cc185d93618de4bdeaeb76b53486ac47/src/main/resources/application-local-integration.yml).
- [src/main/java/com/mercadolibre/rio/playmaker/localintegration/LocalKafkaDeploymentTriggerProducer.java](https://github.com/melisource/fury_rio-playmaker/blob/f087e4b7cc185d93618de4bdeaeb76b53486ac47/src/main/java/com/mercadolibre/rio/playmaker/localintegration/LocalKafkaDeploymentTriggerProducer.java).
- [src/main/java/com/mercadolibre/rio/playmaker/localintegration/LocalKafkaDeploymentResultListener.java](https://github.com/melisource/fury_rio-playmaker/blob/f087e4b7cc185d93618de4bdeaeb76b53486ac47/src/main/java/com/mercadolibre/rio/playmaker/localintegration/LocalKafkaDeploymentResultListener.java).
- [src/main/java/com/mercadolibre/rio/playmaker/localintegration/LocalKafkaConfiguration.java](https://github.com/melisource/fury_rio-playmaker/blob/f087e4b7cc185d93618de4bdeaeb76b53486ac47/src/main/java/com/mercadolibre/rio/playmaker/localintegration/LocalKafkaConfiguration.java).
- [src/main/java/com/mercadolibre/rio/playmaker/localintegration/LocalKafkaBootstrapGuard.java](https://github.com/melisource/fury_rio-playmaker/blob/f087e4b7cc185d93618de4bdeaeb76b53486ac47/src/main/java/com/mercadolibre/rio/playmaker/localintegration/LocalKafkaBootstrapGuard.java).
- [src/main/java/com/mercadolibre/rio/playmaker/restclient/impl/BigQueueActionsProducerLocal.java](https://github.com/melisource/fury_rio-playmaker/blob/f087e4b7cc185d93618de4bdeaeb76b53486ac47/src/main/java/com/mercadolibre/rio/playmaker/restclient/impl/BigQueueActionsProducerLocal.java).
- [src/main/java/com/mercadolibre/rio/playmaker/restclient/impl/KafkaControlPlaneClientImplLocal.java](https://github.com/melisource/fury_rio-playmaker/blob/f087e4b7cc185d93618de4bdeaeb76b53486ac47/src/main/java/com/mercadolibre/rio/playmaker/restclient/impl/KafkaControlPlaneClientImplLocal.java).
- [build.gradle](https://github.com/melisource/fury_rio-playmaker/blob/f087e4b7cc185d93618de4bdeaeb76b53486ac47/build.gradle).

#### rio-controlplane-clickhouse

- [README.md](https://github.com/melisource/fury_rio-controlplane-clickhouse/blob/afbf0f07b18a4a9fe1032932b71fba2ae56e98af/README.md).
- [docker-compose.yml](https://github.com/melisource/fury_rio-controlplane-clickhouse/blob/afbf0f07b18a4a9fe1032932b71fba2ae56e98af/docker-compose.yml).
- [src/main/java/com/mercadolibre/rio/controlplane/clickhouse/shared/client/bigqueue/impl/LocalFileBigQueueClient.java](https://github.com/melisource/fury_rio-controlplane-clickhouse/blob/afbf0f07b18a4a9fe1032932b71fba2ae56e98af/src/main/java/com/mercadolibre/rio/controlplane/clickhouse/shared/client/bigqueue/impl/LocalFileBigQueueClient.java).
- [src/main/java/com/mercadolibre/rio/controlplane/clickhouse/deployment/LocalDeploymentStateService.java](https://github.com/melisource/fury_rio-controlplane-clickhouse/blob/afbf0f07b18a4a9fe1032932b71fba2ae56e98af/src/main/java/com/mercadolibre/rio/controlplane/clickhouse/deployment/LocalDeploymentStateService.java).
- [src/main/java/com/mercadolibre/rio/controlplane/clickhouse/deployment/LocalConnectorLifecycleLock.java](https://github.com/melisource/fury_rio-controlplane-clickhouse/blob/afbf0f07b18a4a9fe1032932b71fba2ae56e98af/src/main/java/com/mercadolibre/rio/controlplane/clickhouse/deployment/LocalConnectorLifecycleLock.java).

#### rio-controlplane-flink

- [src/main/resources/application-local.yml](https://github.com/melisource/fury_rio-controlplane-flink/blob/7c645ea92f86650744a3c5ee1bad0012633ef0e9/src/main/resources/application-local.yml).
- [src/main/java/com/mercadolibre/rio/controlplaneflink/deployment/LocalBigQueueDeploymentPublisher.java](https://github.com/melisource/fury_rio-controlplane-flink/blob/7c645ea92f86650744a3c5ee1bad0012633ef0e9/src/main/java/com/mercadolibre/rio/controlplaneflink/deployment/LocalBigQueueDeploymentPublisher.java).
- [src/main/java/com/mercadolibre/rio/controlplaneflink/config/KvsConfig.java](https://github.com/melisource/fury_rio-controlplane-flink/blob/7c645ea92f86650744a3c5ee1bad0012633ef0e9/src/main/java/com/mercadolibre/rio/controlplaneflink/config/KvsConfig.java).
- [build.gradle](https://github.com/melisource/fury_rio-controlplane-flink/blob/7c645ea92f86650744a3c5ee1bad0012633ef0e9/build.gradle).

#### rio-controlplane-fury

- [src/main/resources/application.yml](https://github.com/melisource/fury_rio-controlplane-fury/blob/849a9f68bc83bee204264846e541c43c48b66fc8/src/main/resources/application.yml).
- [src/main/kotlin/com/mercadolibre/rio_controlplane_fury/pusher/persistence/KvsConfig.kt](https://github.com/melisource/fury_rio-controlplane-fury/blob/849a9f68bc83bee204264846e541c43c48b66fc8/src/main/kotlin/com/mercadolibre/rio_controlplane_fury/pusher/persistence/KvsConfig.kt).
- [src/main/kotlin/com/mercadolibre/rio_controlplane_fury/pusher/bigqueue/BigQueueConfig.kt](https://github.com/melisource/fury_rio-controlplane-fury/blob/849a9f68bc83bee204264846e541c43c48b66fc8/src/main/kotlin/com/mercadolibre/rio_controlplane_fury/pusher/bigqueue/BigQueueConfig.kt).

#### rio-controlplane-kms

- [README.md](https://github.com/melisource/fury_rio-controlplane-kms/blob/7fe77453c4e14ce4ee0e368188902c8ecabc21f2/README.md).
- [src/main/java/com/mercadolibre/rio/controlplane/kms/config/KvsConfig.java](https://github.com/melisource/fury_rio-controlplane-kms/blob/7fe77453c4e14ce4ee0e368188902c8ecabc21f2/src/main/java/com/mercadolibre/rio/controlplane/kms/config/KvsConfig.java).

#### rio-controlplane-observability

- [src/main/java/com/mercadolibre/rio_controlplane_observability/config/KvsConfig.java](https://github.com/melisource/fury_rio-controlplane-observability/blob/c5afde4eea49b0c9d820ff873ff86f618ffc0a32/src/main/java/com/mercadolibre/rio_controlplane_observability/config/KvsConfig.java).
- [src/main/java/com/mercadolibre/rio_controlplane_observability/config/AwsCredentialsResolver.java](https://github.com/melisource/fury_rio-controlplane-observability/blob/c5afde4eea49b0c9d820ff873ff86f618ffc0a32/src/main/java/com/mercadolibre/rio_controlplane_observability/config/AwsCredentialsResolver.java).
- [README.md](https://github.com/melisource/fury_rio-controlplane-observability/blob/c5afde4eea49b0c9d820ff873ff86f618ffc0a32/README.md).

#### rio-controlplane-signals

- [src/main/resources/application-local.yml](https://github.com/melisource/fury_rio-controlplane-signals/blob/ce29224f7f619cb91b52c64038ce3f6fbf1143ed/src/main/resources/application-local.yml).
- [local/mock-collector.py](https://github.com/melisource/fury_rio-controlplane-signals/blob/ce29224f7f619cb91b52c64038ce3f6fbf1143ed/local/mock-collector.py).
- [src/main/java/com/mercadolibre/rio/controlplane/signals/shared/client/bigqueue/impl/LocalFileBigQueueClient.java](https://github.com/melisource/fury_rio-controlplane-signals/blob/ce29224f7f619cb91b52c64038ce3f6fbf1143ed/src/main/java/com/mercadolibre/rio/controlplane/signals/shared/client/bigqueue/impl/LocalFileBigQueueClient.java).
- [src/main/java/com/mercadolibre/rio/controlplane/signals/deployment/LocalDeploymentStateService.java](https://github.com/melisource/fury_rio-controlplane-signals/blob/ce29224f7f619cb91b52c64038ce3f6fbf1143ed/src/main/java/com/mercadolibre/rio/controlplane/signals/deployment/LocalDeploymentStateService.java).

#### rio-materializer

- [README.md](https://github.com/melisource/fury_rio-materializer/blob/c10e6f37e53346b958b77059c1c949ea17521d7f/README.md).
- [local/01-kafka-docker.sh](https://github.com/melisource/fury_rio-materializer/blob/c10e6f37e53346b958b77059c1c949ea17521d7f/local/01-kafka-docker.sh).

#### rio-sdk-events

- [src/main/java/com/mercadolibre/rio/sdk/events/bigqueue/impl/LocalFileBigQueueClient.java](https://github.com/melisource/fury_rio-sdk-events/blob/ad2c98b806cffb88b23513f87785932aa1707ea4/src/main/java/com/mercadolibre/rio/sdk/events/bigqueue/impl/LocalFileBigQueueClient.java).
- [README.md](https://github.com/melisource/fury_rio-sdk-events/blob/ad2c98b806cffb88b23513f87785932aa1707ea4/README.md).

### Variantes de Signals

- `feature/local-docker-setup@a58195a2b1937894f6423a8b6cc264db6bf3a40e`: [docker-compose.yml](https://github.com/melisource/fury_rio-controlplane-signals/blob/a58195a2b1937894f6423a8b6cc264db6bf3a40e/docker-compose.yml), app real + Python mock para Catalog/Collector. No estaba en `develop` al consultar.
- `feature/cp-signals-06-local-e2e@157252e87abb465116175d6732b1a4c96bbbb1af`: se contrastó la configuración local; usa las mismas URLs de mock/servicios externos.

### Fuentes externas de soporte

- [Apache Kafka 3.9 — Docker](https://kafka.apache.org/39/getting-started/docker/): imagen JVM oficial, consultada el 2026-09-30.
- [Docker Compose — Startup order](https://docs.docker.com/compose/how-tos/startup-order/): healthchecks y condición `service_healthy`, consultada el 2026-09-30.
- [Testcontainers Java — Kafka](https://java.testcontainers.org/modules/kafka/): módulo y listeners, consultada el 2026-09-30.

## Notas de provenance

- La evidencia es estática y reproducible desde los commits. No hubo arranque de aplicaciones, uso de sandbox, llamadas productivas ni pruebas Kafka E2E.
- Los SHAs son las bases de desarrollo consultadas; no representan una declaración de release ejecutada en producción.
- Los checkouts de Kafka y Playmaker conservaron sus ramas y modificaciones originales. No se sincronizaron sus ramas feature ni se publicaron commits.
- La búsqueda dirigida no encontró otro stack común autocontenido en las bases leídas. No afirma ausencia en todos los repos/branches históricos.
- El enlace a la guía externa Fury Sandbox del README de KMS no fue accesible; la evidencia positiva de ese precedente se limita al código/documentación del repo.

## Lifecycle

- Snapshot inmutable de evidencia al 2026-09-30; una nueva captura debe declarar su relación con esta fuente.
