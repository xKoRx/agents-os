---
type: application
schema_version: 1
status: active
slug: rio-controlplane-flink
area: "[[Meli]]"
lang: Java
github: https://github.com/melisource/fury_rio-controlplane-flink
path: ~/fuentes/rio-controlplane-flink
aliases:
  - rio controlplane flink
tags:
  - kind/application
  - area/meli
  - app/rio-controlplane-flink
created: 2026-08-10
updated: 2026-08-10
last_verified: 2026-08-10
confidence: high
---

# rio-controlplane-flink

> [!info]+ rio-controlplane-flink
> **Rol:** Control plane que crea y administra el ciclo de vida de apps Apache Flink SQL sobre AWS Kinesis Data Analytics (KDA) · **Área:** [[Meli]] · **Plataforma:** [[RIO]]
> **Repo:** [remote](https://github.com/melisource/fury_rio-controlplane-flink) · **Local:** `~/fuentes/rio-controlplane-flink` · **Lang:** Java

## 🎯 Responsabilidad (estable)
- Orquesta el ciclo de vida completo de aplicaciones **Apache Flink SQL** ejecutadas en **AWS Kinesis Data Analytics (KDA)**: crear, actualizar, iniciar, detener y eliminar.
- Sube los archivos SQL (DDL/DML) a S3, verifica la disponibilidad del JAR runtime (`rio-flink-sql.jar`, pre-subido por otro proceso, no lo construye) y configura la app en KDA (checkpointing, parallelism, tags, log group/stream).
- Usa **CQRS** (`Command`/`Query`) más un **flujo dirigido por eventos**: cada paso del lifecycle es un `EventStep` que avanza una cadena de `Handler`s (`CHECK_ARTIFACT` → `CHECK_TO_CREATE_APP_IN_AWS` → `CREATE_LOG_GROUP_STREAM_IN_AWS` → `CREATE_APP_IN_AWS` → `ADD_TAGS_TO_APP_IN_AWS` → `START_APP_IN_AWS`).
- Jobs programados (`job/impl/`, cada 30s) resuelven transiciones asíncronas de estado en AWS (`CheckIfAppRunningJob`, `CheckIfAppStoppedJob`, etc.) hasta confirmar el estado final.
- No ejecuta lógica de negocio del Flink SQL en sí (eso corre en `rio-flink-sql.jar` dentro de KDA); su límite es la orquestación de infraestructura y estado, no el procesamiento de streams.

## 🔌 Contratos e interacciones (semi-estable)
- **Expone:** REST — `POST/PUT /flink/apps`, `GET /flink/apps/{name}`, `GET /flink/apps/{name}/logs`, `DELETE /flink/apps/{name}`, `PATCH /flink/apps/{name}/start|stop`; `GET/DELETE /flink/sql-code/{workspace}/...`; `POST /triggers/actions`; `POST /triggers/deployments`; `POST /events`; `GET /ping`.
- **Consume / produce:** SQS (`ReadKdaEventsFromSQSQuery`, estado async de KDA); BigQueue vía `rio-sdk-events` (`BigQConfig`, `BigQueueClientFactory`) para publicar resultados (`ControlPlaneEventPublisher`, `ComponentResultEventPublisher`, `StreamDeploymentPublisher`, `BigQueueDeploymentPublisher`, `ActionResultPublisher`); S3 para SQL files y JAR; AWS CloudWatch Logs para log groups/streams de cada app Flink.
- **Llama a / lo llaman:** invocado por [[rio-materializer]] (vía WorkQueue) que a su vez atiende pedidos de [[rio-playmaker]]/rio-frontend; notifica cambios de estado al resto de la plataforma RIO.

## 🧩 Implementación (volátil · last_verified: 2026-08-10)
> Detalle que puede cambiar sin cambiar la responsabilidad.
- **Stack:** Java 21 (virtual threads habilitados globalmente) · Spring Boot (Jetty embebido) · Gradle.
- **Librerías / infra clave:** AWS SDK v2 — `kinesisanalyticsv2`, `s3`, `cloudwatchlogs`, `sqs` (todas 2.33.9); `rio-core-java` 1.1.0; `com.mercadolibre.rio.sdk.events` (BigQueue); `java-melitk-bom` 2.2.1, `java-melitk-secrets`, `spring-boot-starter-secrets`, `spring-boot-starter-config`, New Relic agent.
- **Patrón notable:** CQRS estricto (`Command<T,U>`/`Query<T,U>`, nunca instanciados directo) + cadena de `@EventListener` por `EventStep` sobre `EventFlinkApp`; dos publishers separados — `ControlPlaneEventPublisher` (plataforma) vs `ComponentResultEventPublisher` (solo si `event.isSuppressControlPlaneEvents()`, o sea caller interno); `NeedToCheck` (`ConcurrentHashMap` en memoria) trackea apps en espera de confirmación async de AWS.

## 🔗 Relaciones
- [[rio-playmaker]]
- [[rio-materializer]]
- [[rio-sdk-events]]

## 📌 Provenance
- Repo: `melisource/fury_rio-controlplane-flink` · Local: `~/fuentes/rio-controlplane-flink`
- Fuentes leídas: `README.md`, `CLAUDE.md`, `build.gradle`, `graphify-out/GRAPH_REPORT.md`, vistazo shallow a `src/main/java/.../controlplaneflink/` (controllers, config/BigQConfig, events/, adapter/, cqrs/)
- `last_verified: 2026-08-10` · `confidence: high`

## ✅ Tareas relacionadas

```tasks
sort by priority
not done
description includes rio-controlplane-flink
short mode
hide task count
```
