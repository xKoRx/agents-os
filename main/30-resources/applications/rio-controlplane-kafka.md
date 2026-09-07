---
type: application
schema_version: 1
status: active
slug: rio-controlplane-kafka
area: "[[Meli]]"
lang: Java
github: https://github.com/melisource/fury_rio-controlplane-kafka
path: ~/fuentes/rio-controlplane-kafka
aliases:
  - rio controlplane kafka
tags:
  - kind/application
  - area/meli
  - app/rio-controlplane-kafka
created: 2026-08-10
updated: 2026-08-10
last_verified: 2026-08-10
confidence: high
---

# rio-controlplane-kafka

> [!info]+ rio-controlplane-kafka
> **Rol:** Control plane del ciclo de vida de topics Kafka (PROVISION/UPDATE/DEPROVISION) e inspección de mensajes (PEEK) · **Área:** [[Meli]] · **Plataforma:** [[RIO]]
> **Repo:** [remote](https://github.com/melisource/fury_rio-controlplane-kafka) · **Local:** `~/fuentes/rio-controlplane-kafka` · **Lang:** Java

## 🎯 Responsabilidad (estable)
- Control plane que gestiona el ciclo de vida de topics Kafka: crea, actualiza y da de baja topics (PROVISION/UPDATE/DEPROVISION) y permite inspeccionar mensajes recientes de un topic sin comprometer offsets (PEEK).
- Recibe triggers system-to-system desde Playmaker (plataforma RIO) vía BigQueue, ejecuta la operación contra el cluster Kafka real (GCP Managed Kafka o AWS MSK) usando `AdminClient`, y publica el resultado de vuelta vía BigQueue.
- Domain-agnostic en su mecanismo de idempotencia (guard compartido entre dominios Actions y Deployment) para tolerar redelivery de BigQueue sin duplicar operaciones.
- No es el owner de la decisión de negocio de *cuándo* aprovisionar — eso vive en Playmaker; este componente ejecuta y confirma.

## 🔌 Contratos e interacciones (semi-estable)
- **Expone:**
  - `GET /ping` — health check.
  - `POST /triggers/deployments` — consumidor de trigger BigQueue de dominio Deployment (PROVISION/UPDATE/DEPROVISION).
  - `POST /triggers/actions` — consumidor de trigger BigQueue de dominio Actions (PEEK).
  - `POST /kafka/topic/{topicName}/peek` — lectura REST directa de mensajes recientes de un topic sin comprometer offsets.
- **Consume / produce:**
  - Consume triggers publicados por Playmaker en BigQueue (dominio Deployment y dominio Actions).
  - Publica resultados de vuelta vía BigQueue (topics de resultado por dominio: deployment result / action result), usando `rio-sdk-events` para el envelope tipado.
  - Opera contra Kafka real vía `AdminClient` con OAuth en GCP Managed Kafka (legacy-default, sin segmentación aún) y routing segmentado en AWS MSK.
  - Usa Fury KVS para idempotencia (optimistic locking / CAS) ante redelivery.
- **Llama a / lo llaman:**
  - Lo llama **rio-playmaker** (origen de los triggers de deployment y actions).
  - Relación histórica/predecesora: **rio-materializer** (comportamiento legado de creación/actualización de topics AWS MSK que este control plane reemplaza y corrige — ver migración `sdk-events-1-2-0`).
  - Depende de la librería **rio-sdk-events** (publicación tipada de eventos control-plane vía BigQueue) y de librerías `rio-core-java-*` (routing y auth GCP).

## 🧩 Implementación (volátil · last_verified: 2026-08-10)
> Detalle que puede cambiar sin cambiar la responsabilidad.
- **Stack:** Java 21, Spring Boot 3.5.7, Gradle + JaCoCo, contenedor con Jetty (no Tomcat).
- **Librerías / infra clave:** `rio-core-java-cloud-routing-spring3` (routing multi-cluster/multi-cloud), `rio-core-java-gcp-kafka-auth-spring3` (OAuth para GCP Managed Kafka vía Fury Secrets), `rio-sdk-events:1.3.1` (eventos tipados control-plane sobre BigQueue), `bigqueue-util-dtos`, `kvsclient:2.3.4` (idempotencia Fury KVS), `mqclient:3.4.8`, `kafka-clients:3.9.2`, OpenTelemetry para métricas/telemetría, Caffeine (cache), Testcontainers (Kafka) en tests.
- **Patrón notable:** dispatcher async (`CompletableFuture` + executor) que responde HTTP 200 inmediato al trigger y procesa la operación en background; `IdempotencyGuard` compartido (Fury KVS + CAS) entre dominios Deployment y Actions; resolución de cluster multi-cloud vía `ClusterRoutingEngine` con modelo legacy-default para GCP y segmentado por equipo para AWS MSK.

## 🔗 Relaciones
- [[rio-playmaker]]
- [[rio-materializer]]

## 📌 Provenance
- Repo: `melisource/fury_rio-controlplane-kafka` · Local: `~/fuentes/rio-controlplane-kafka`
- Fuentes leídas: `README.md`, `graphify-out/GRAPH_REPORT.md`, `build.gradle`, vistazo shallow a `src/main/java/.../rio_controlplane_kafka/*` (paquetes: provisioning, deployment, actions, kafka, cloud, idempotency, telemetry, events, controller), grep dirigido sobre `meli/features/*` para confirmar relación con Playmaker y rio-materializer.
- `last_verified: 2026-08-10` · `confidence: high`

## ✅ Tareas relacionadas

```tasks
sort by priority
not done
description includes rio-controlplane-kafka
short mode
hide task count
```
