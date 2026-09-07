---
type: application
schema_version: 1
status: active
slug: rio-controlplane-fury
area: "[[Meli]]"
lang: Kotlin
github: https://github.com/melisource/fury_rio-controlplane-fury
path: ~/fuentes/rio-controlplane-fury
aliases:
  - rio controlplane fury
tags:
  - kind/application
  - area/meli
  - app/rio-controlplane-fury
created: 2026-08-10
updated: 2026-08-10
last_verified: 2026-08-10
confidence: high
---

# rio-controlplane-fury

> [!info]+ rio-controlplane-fury
> **Rol:** Control plane del "pusher" de RIO: provisiona, reconcilia y opera pipelines de enrutamiento de eventos (Kafka↔Fury Streams / Template Processing) por orden de Playmaker · **Área:** [[Meli]] · **Plataforma:** [[RIO]]
> **Repo:** [remote](https://github.com/melisource/fury_rio-controlplane-fury) · **Local:** `~/fuentes/rio-controlplane-fury` · **Lang:** Kotlin

## 🎯 Responsabilidad (estable)

- Es el "Pusher" de RIO: mantiene un fleet declarativo de `PusherMapping` (pipelines fuente→destino tipo `STREAM_TO_KAFKA`/Kafka↔TP) con estado deseado vs. observado, y lo reconcilia continuamente (provisiona, actualiza, deprovisiona) contra Kafka, Fury Streams (ALPACA SDK) y Template Processing (TP admin API).
- Recibe comandos de deploy (PROVISION/UPDATE/DEPROVISION) vía BigQueue desde Playmaker, ejecuta la convergencia y reporta el resultado (STARTED/COMPLETED/FAILED) de vuelta a Playmaker.
- Corre además el data-plane de esos pipelines dentro del mismo proceso (pump de Kafka con backpressure vía reactor-kafka), es decir es control plane + data plane híbridos, no solo orquestación.
- README aún en scaffold InnerSource inicial (sin "Why/What" propios); el rol se infiere de código, CHANGELOG y specs `meli/features`.

## 🔌 Contratos e interacciones (semi-estable)

- **Expone:** REST read-only de `PusherMapping` (`PusherMappingController`), endpoint de deprovision por mapping ID, `PingController` (liveness Fury), endpoint push-consumer `/bigqueue/deployment-trigger`.
- **Consume / produce:** consume BigQueue `rio-deployment-trigger` (`DeploymentTriggerMessage`, contratos `rio-sdk-events` SIG-187); produce BigQueue `rio-deployment-result` (`DeploymentResultPublisher`). Persiste `PusherMapping` en KVS/QKVS (`java-toolkit-kvs`). Llama a TP admin API (`tp-control-plane`, vía `TpAdminClient`/meli-restclient) y a Fury Streams (ALPACA SDK) para registrar/dar de baja sinks.
- **Llama a / lo llaman:** lo llama [[rio-playmaker]] (emisor de PROVISION/DEPROVISION y receptor del resultado); relación con [[rio-materializer]] como flujo legacy/adyacente (fuente de stream de referencia en pruebas e2e, en vías de ser reemplazado por el camino BigQueue de Playmaker).

## 🧩 Implementación (volátil · last_verified: 2026-08-10)

- **Stack:** Kotlin (JVM 21) sobre Spring Boot 3.5.7, Gradle Kotlin DSL (`build.gradle.kts`). 138 archivos `.kt` en `src/main`; 1 archivo Java residual en tests.
- **Librerías / infra clave:** `com.fury.toolkit:java-toolkit-kvs:0.7.3` (KVS/QKVS), `com.mercadolibre:mqclient:3.4.9` (BigQueue), `com.mercadolibre.library:rio-sdk-events:1.2.0` (contratos wire SIG-187), `org.apache.kafka:kafka-clients:3.9.2` + `io.projectreactor.kafka:reactor-kafka:1.3.25` (pump con backpressure), `com.mercadolibre.library:alpaca-sdk:4.2.2` (Fury Streams), `com.fury.toolkit:java-tk-template-processing:0.1.8` (TP SDK), `meli-restclient-default:3.1.3`.
- **Patrón notable:** control loop tipo reconciler (desired vs. observed status) con leases de partición por réplica (`PipelineLease`/`OwnershipConfig`/`ReplicaId`) para reparto del fleet entre instancias — análogo a un controller pattern (k8s-like) aplicado a pipelines de streaming.

## 🔗 Relaciones

- [[rio-playmaker]]
- [[rio-materializer]]

## 📌 Provenance

- Repo: `melisource/fury_rio-controlplane-fury` · Local: `~/fuentes/rio-controlplane-fury`
- Fuentes leídas: `README.md` (scaffold InnerSource), `AGENTS.md`, `build.gradle.kts`, `CHANGELOG.md`, `meli/backlog.md`, listado shallow de `src/main/kotlin/.../{controller,core,pusher}`, specs funcionales/técnicos en `meli/features/*` y `meli/wip/*` (grep dirigido, sin volcado completo). `ARCHITECTURE.md` y `graphify-out/GRAPH_REPORT.md` no aportaron descripción textual del rol más allá de métricas del grafo.
- `last_verified: 2026-08-10` · `confidence: high`

## ✅ Tareas relacionadas

```tasks
sort by priority
not done
description includes rio-controlplane-fury
short mode
hide task count
```
