---
type: source
schema_version: 1
status: active
area: "[[Meli]]"
source_url:
repo: melisource/fury_rio-playmaker
path: local/00-integration-pipeline.sh
author:
published:
captured: "2026-10-07"
license:
checksum:
supersedes: "[[Source — Playmaker — Transporte local 2026-10-07]]"
superseded_by:
aliases: []
tags:
  - kind/source
created: "2026-10-07"
updated: "2026-10-07"
related: ["[[rio-playmaker]]", "[[rio-controlplane-clickhouse]]"]
---

# Source — Playmaker — Kafka local 2026-10-07

## Referencia

- Repositorio: `melisource/fury_rio-playmaker`; checkout inspeccionado `release/202610.7.0 @ 3433fc12b353b792883bad2394709fee49ce413f`.
- Archivos: `README.md`, `local/00-integration-pipeline.sh`, `local/01-mysql.sh`, `docker-compose.kafka.yaml`, `src/main/resources/application-local-integration.yml`, `localintegration/LocalKafkaDeploymentTriggerProducer.java`, `LocalKafkaDeploymentResultListener.java`, `LocalKafkaConfiguration.java`, `LocalKafkaBootstrapGuard.java`, `build.gradle` y `service/pipeline/ComponentContextService.java`.

## Alcance

- `./local/00-integration-pipeline.sh` prepara MySQL, inicia Apache Kafka 3.9.1, crea tres topics y arranca Playmaker con `local,local-integration`.
- Kafka host: `127.0.0.1:39092`; listener interno Docker: `kafka:9092`. Playmaker HTTP: 9090; MySQL usa 3306 por defecto, configurable mediante `PLAYMAKER_MYSQL_PORT` en su env file.
- Topics: `rio-deployment-trigger-local`, `rio-deployment-result-local`, `rio-deployment-result-local-dlt`. El pipeline no inicia ningún control plane.
- La publicación usa JSON de DeploymentTriggerMessage plano, key deploymentId y espera ACK del broker; el consumer de resultados recibe JSON DeploymentResultMessage plano y delega al servicio productivo de consumo.
- El perfil de integración desactiva el loopback simulado. El guard exige local y un broker loopback; errores de resultados tienen retries acotados y DLT.
- El script utiliza `PLAYMAKER_ENV_FILE` y `.env` por defecto para credenciales locales; no se debe reemplazar con las credenciales de ClickHouse.
- SDK declarado 1.5.0. Sus signatures DTO coinciden con 1.6.1 del CP y ambos tienen schema 1, según comparación estática de jars. El round-trip real sigue sin ejecutar.
- `latestVersion` se construye desde el último deployment; inputs históricos permanecen separados de los params efectivos de la nueva solicitud.

## Notas de provenance

- Inspección actual de código y scripts; no se cambió, sincronizó ni ejecutó Playmaker.
- La inspección anterior en release/202610.5.0 se conserva en [[Source — Playmaker — Transporte local 2026-10-07]]. Los archivos principales de transporte comparados entre ambos commits no tienen diff.
- La integración propuesta necesita un bridge Kafka/HTTP/archivos o adapters Kafka scoped en el CP; ninguno fue implementado en esta actualización.
