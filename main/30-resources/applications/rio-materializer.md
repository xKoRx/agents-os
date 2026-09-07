---
type: application
schema_version: 1
status: deprecated
slug: rio-materializer
area: "[[Meli]]"
lang: Java
github: https://github.com/melisource/fury_rio-materializer
path: ~/fuentes/rio-materializer
aliases:
  - rio materializer
tags:
  - kind/application
  - area/meli
  - app/rio-materializer
  - lifecycle/deprecated
created: 2026-08-10
updated: 2026-08-11
last_verified: 2026-08-11
confidence: high
---

# rio-materializer

> [!warning] En deprecación
> **`rio-materializer` está en proceso de deprecado.** El flujo de despliegue nuevo va directo de [[rio-playmaker]] a los control planes (trigger HTTP/BigQueue → `rio-deployment-result`), sin pasar por el materializer. Según el equipo (2026-08-11) **solo le queda el flujo de componentes de inicio de Signals/Catalog** (los que aún pasan por acá); el resto ya migró a la ruta directa. No construir features nuevos sobre esta app.

> [!info]+ rio-materializer
> **Rol:** Puente presentación↔infraestructura de RIO: materializa (crea/actualiza/destruye) componentes de data products sobre proveedores cloud reales · **Área:** [[Meli]] · **Plataforma:** [[RIO]]
> **Repo:** [remote](https://github.com/melisource/fury_rio-materializer) · **Local:** `~/fuentes/rio-materializer` · **Lang:** Java

## 🎯 Responsabilidad (estable)
- Es la capa que traduce solicitudes de la capa de presentación de RIO (crear/consultar/borrar un "component" de data product) en operaciones concretas de infraestructura: provisioning en Kubernetes, buckets S3/GCS, streams/MSK, jobs Flink, ClickHouse y cifrado vía KMS.
- Materializar = ejecutar el ciclo de vida real (build → deploy/upload → preview → status) de un componente contra el proveedor cloud que corresponda, y devolver/propagar el resultado hacia el control plane y la capa de presentación.
- Coexisten dos estilos internos: un núcleo legacy tipo CQRS (`cqrs/`, `handler/`) orientado a Cloud Controller (K8s, Flink, KMS), y un flujo más nuevo tipo hexagonal/DDD bajo `deployment/` (domain/application/infrastructure/presentation) con soporte de sagas para orquestación asíncrona multi-paso.

## 🔌 Contratos e interacciones (semi-estable)
- **Expone:** REST — `MaterializationController` (`/components/`, `/materializations/`), `MaterializationV2Controller` (`/v2/materializations`), `ControlPlaneController` (`/control-plane/components/{name}/start|stop`, consulta y streaming de sagas por `correlation_id`), `ComponentTemplateController` (`/component-templates/`), `WQMaterializationController` (`/workqueues/materialization-request`), `AdminController`, `PingController`.
- **Consume / produce:** eventos vía `ControlPlaneEventConsumer` (Kafka/control plane) y Workqueues SDK; produce/gestiona recursos en K8s, AWS MSK, S3/GCS, Flink apps y ClickHouse; cifra/descifra tokens vía KMS.
- **Llama a / lo llaman:** aplicaciones RIO — [[rio-playmaker]], [[rio-controlplane-clickhouse]], [[rio-controlplane-fury]], [[rio-controlplane-flink]], [[rio-controlplane-kafka]], [[rio-sdk-events]]; clientes propios (`clients/impl`) hacia Nexus Fury, notificaciones a Playmaker, K8s y S3.

## 🧩 Implementación (volátil · last_verified: 2026-08-10)
- **Stack:** Java 21 · Spring Boot 3.5.6 (Jetty embebido) · Gradle · versión de app `2.21.0`.
- **Librerías / infra clave:** `rio-core-java`, `rio-sdk-events`, Workqueues SDK (`java-melitk-workqueues`), BigQueue (`mqclient`), `java-toolkit-nosql` (migrado desde SDK NoSQL legacy), Spring Kafka + Apache Kafka clients, Fabric8 Kubernetes client, AWS SDK S3, Google OAuth2, Resilience4j, OpenTelemetry, Spring Boot Secrets.
- **Patrón notable:** Saga asíncrona con timeout (`SagaTimeoutJob`, `SagaRecord/SagaStatus/SagaType`) para orquestar despliegues multi-paso en `deployment/`; el módulo `cqrs/` más antiguo modela cada operación de Cloud Controller (deploy, preview, upload, stack) como command/query independientes con handlers dedicados.

## 🔗 Relaciones
- [[rio-playmaker]]
- [[rio-controlplane-clickhouse]]
- [[rio-controlplane-fury]]
- [[rio-controlplane-flink]]
- [[rio-controlplane-kafka]]
- [[rio-sdk-events]]

## 📌 Provenance
- Repo: `melisource/fury_rio-materializer` · Local: `~/fuentes/rio-materializer`
- Fuentes leídas: `README.md`, `build.gradle`, `graphify-out/GRAPH_REPORT.md` (metadata), estructura y clases de `src/main/java/com/mercadolibre/rio/materializer/**` (controllers, cqrs, deployment/*, clients, factories, strategies) — sin volcar código, solo firmas/paths.
- `last_verified: 2026-08-10` · `confidence: high`

## ✅ Tareas relacionadas

```tasks
sort by priority
not done
description includes rio-materializer
short mode
hide task count
```
