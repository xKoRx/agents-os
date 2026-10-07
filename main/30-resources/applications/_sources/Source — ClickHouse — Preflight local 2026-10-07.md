---
type: source
schema_version: 1
status: active
area: "[[Meli]]"
source_url:
repo: melisource/fury_rio-controlplane-clickhouse
path: README.md
author:
published:
captured: "2026-10-07"
license:
checksum:
supersedes:
superseded_by:
aliases: []
tags:
  - kind/source
created: "2026-10-07"
updated: "2026-10-07"
related: ["[[rio-controlplane-clickhouse]]"]
---

# Source — ClickHouse — Preflight local 2026-10-07

## Referencia

- Repositorio: `melisource/fury_rio-controlplane-clickhouse`.
- Snapshot contrastado: `develop @ c8b20b65`, actualizado mediante `git switch develop` y `git pull` el 2026-10-07.
- Archivos: `README.md`, `build.gradle`, `docker-compose.yml`, `src/main/resources/application-local.yml`, `src/main/resources/application.yml`; clases `DeploymentEventController`, `DeploymentTriggerMapper`, `DeploymentContextResolver`, `KvsConfig`, `ConnectorLifecycleLockConfig`, `ControlPlaneKmsConfig`, `ClickHouseClientFactory`, `LocalFileBigQueueClient` y sus tests.

## Alcance

- Rama solicitada: `feature/new-component-context @ 7de630c6`; sólo `graphify-out/` estaba sin tracking. Merge de develop iniciado, pendiente de decisión sobre cinco conflictos. No se creó commit ni se publicó la rama.
- Validación en export aislado de develop: Java Corretto 25.0.4, Gradle 9.3.1; `./gradlew test bootJar` terminó `BUILD SUCCESSFUL`: 357 clases, 2335 tests, 0 fallos, 0 errores, 0 omitidos.
- `application.jar` arrancó con `SCOPE=local`, `APPLICATION=rio-controlplane-clickhouse`, contraseña aleatoria efímera y puerto de prueba 18083. `/ping` respondió `pong`, HTTP 200. El proceso se detuvo al terminar.
- `POST /triggers/deployments` con schema 1 y Context ausente respondió HTTP 200 y produjo un archivo de `rio-deployment-result` con status `FAILED`, código `DEPLOYMENT_FAILED` y diagnóstico de Context ausente. No se ejecutó DDL.
- Docker consultado: daemon 27.4.0, memoria disponible configurada 2054631424 bytes; MySQL 8.0.32 ya en ejecución en 3306, imagen ClickHouse 25.8 disponible. No se inició ni modificó ese MySQL ni un servidor ClickHouse.

## Notas de provenance

- Esta evidencia corresponde a develop y al arranque del CP; no certifica la rama fusionada, DDL contra ClickHouse, persistencia corporativa, cifrado real ni el ciclo con Playmaker.
- El README y el request Bruno de provision MergeTree consultados no incluyen Context, pero el controller vigente lo requiere para PROVISION/UPDATE. La prueba física confirmó el resultado FAILED; HTTP 200 por sí solo es ACK.
- La rama antigua usa `rio-sdk-events:0.0.1-component-version-identity` y overlay de `lastDeployedVersion.inputs`; develop usa `1.6.1`, `LatestVersion`, resolver del SDK y snapshot separado. Se solicitó decisión explícita porque conservar ambos comportamientos no es una resolución mecánica del merge.
