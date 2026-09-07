---
type: application
schema_version: 1
status: active
slug: rio-sdk-events
area: "[[Meli]]"
lang: Java
github: https://github.com/melisource/fury_rio-sdk-events
path: ~/fuentes/rio-sdk-events
aliases:
  - rio sdk events
tags:
  - kind/application
  - area/meli
  - app/rio-sdk-events
created: 2026-08-10
updated: 2026-08-10
last_verified: 2026-08-10
confidence: medium
---

# rio-sdk-events

> [!info]+ rio-sdk-events
> **Rol:** SDK de eventos de RIO (publicación BigQueue/AOP + starter Fury Streams) · **Área:** [[Meli]] · **Plataforma:** [[RIO]]
> **Repo:** [remote](https://github.com/melisource/fury_rio-sdk-events) · **Local:** `~/fuentes/rio-sdk-events` · **Lang:** Java

## 🎯 Responsabilidad (estable)
- Librería Java (`com.mercadolibre.library:rio-sdk-events`), no un servicio desplegable: `Application.java` es solo un placeholder de compilación, no un entrypoint.
- Provee dos mecanismos de publicación de eventos: (1) BigQueue vía AOP (`@PublishEvent` + `EventPublishingAspect`) y (2) un starter Spring Boot para Fury Streams (`StreamsPublisher`) con configuración jerárquica, ordering estricto por partition key y health checks.
- Define contratos de dominio reutilizables por equipos cliente, documentados como arquitectura "de dos dominios" alineada a los topics Kafka de RIO: **Deployment Events** (`deployment-topic`, orquestación de alto nivel) y **Control Plane Events** (`control-plane-topic`, operaciones de infraestructura de bajo nivel). Ambos heredan de `Event` → `RioEvent` (Lombok `@SuperBuilder`, inmutables).
- El SDK entrega los contratos base; los equipos cliente extienden las clases de dominio con payloads específicos de tecnología (ej. Flink, Kafka) sin requerir cambios en el SDK.

## 🔌 Contratos e interacciones (semi-estable)
- **Expone (API del SDK):** `@PublishEvent` (anotación) + `EventPublishingAspect` (AOP) · `BigQueueClientFactory` / `BigQueueClient` (prod: `BigQueueClientImpl`; local: `LocalFileBigQueueClient` con `SCOPE=local`) · `EventEnvelope` (correlation ID, publisher, timestamp) · dominio `Event` / `RioEvent` / `DeploymentEvent<T>` / `ControlPlaneEvent<T extends ControlPlaneData>` · `StreamsPublisher` (`send`, `sendBatch`, `sendOrdered`) + `RioStreamsAutoConfiguration` + `StreamsHealthIndicator` (Fury Streams).
- **Topics / streams:** BigQueue vía `events.bigqueue.*` (topics nombrados por el cliente, ej. `rio-events-topic`) · Fury Streams vía `rio.streams.*` (defaults globales + overrides por stream) · dominios semánticos del README: `deployment-topic` / `control-plane-topic`.
- **Quién lo consume:** apps RIO que integran estos contratos — [[rio-playmaker]], [[rio-materializer]], [[rio-controlplane-flink]], [[rio-controlplane-kafka]] (relación heredada de la nota previa, no reverificada línea por línea en esta pasada).

## 🧩 Implementación (volátil · last_verified: 2026-08-10)
- **Stack:** Java 25 (Gradle toolchain) · Spring Boot 3.4.13 (BOM) · Lombok 1.18.42 · Gradle 9.2+/Maven 3.8+ · versión publicada `1.3.1` (`build.gradle`, group `com.mercadolibre.library`).
- **Librerías / infra clave:** `com.mercadolibre:mqclient:3.4.8` (BigQueue) · `com.mercadolibre.library:java-melitk-streams:3.4.6` (Fury Streams SDK) · `java-melitk-bom:2.2.1` · Jackson forzado a `2.18.6` (parches CVE) · cobertura mínima JaCoCo 88.8%.
- **Patrón notable:** cliente BigQueue nuevo y cerrado por cada publicación (sin pool compartido); fallos de publicación se loguean pero no propagan al caller. Auto-configuración Spring vía `AutoConfiguration.imports` (`BigQueueConfig`, `RioStreamsAutoConfiguration`), ambas `compileOnly` desde la perspectiva del cliente.

## 🔗 Relaciones
- [[rio-playmaker]], [[rio-materializer]], [[rio-controlplane-flink]], [[rio-controlplane-kafka]]

## 📌 Provenance
- Repo: `melisource/fury_rio-sdk-events` · Local: `~/fuentes/rio-sdk-events`
- Fuentes leídas: `README.md`, `CLAUDE.md`, `build.gradle`, `CHANGELOG.md`, `graphify-out/GRAPH_REPORT.md`, listado shallow de `src/main/java/com/mercadolibre/rio/sdk/events/*`
- `last_verified: 2026-08-10` · `confidence: medium`

## ✅ Tareas relacionadas

```tasks
sort by priority
not done
description includes rio-sdk-events
short mode
hide task count
```
