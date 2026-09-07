---
type: application
schema_version: 1
status: active
slug: rio-playmaker
area: "[[Meli]]"
lang: Java
github: https://github.com/melisource/fury_rio-playmaker
path: ~/fuentes/rio-playmaker
aliases:
  - rio playmaker
tags:
  - kind/application
  - area/meli
  - app/rio-playmaker
created: 2026-08-10
updated: 2026-08-10
last_verified: 2026-08-10
confidence: high
---

# rio-playmaker

> [!info]+ rio-playmaker
> **Rol:** Orquestador central de RIO — gestiona data products, componentes y despliegues, y coordina su ejecución entre control planes · **Área:** [[Meli]] · **Plataforma:** [[RIO]]
> **Repo:** [remote](https://github.com/melisource/fury_rio-playmaker) · **Local:** `~/fuentes/rio-playmaker` · **Lang:** Java

## 🎯 Responsabilidad (estable)
- Orquestador de RIO: administra el ciclo de vida completo de data products, componentes, definiciones de componente, entornos, servicios y sus despliegues (CRUD + estado).
- Coordina la ejecución de despliegues y acciones disparando triggers y consumiendo resultados/estado desde los control planes (patrón consolidado en SIG-186 "DeploymentGroup Orchestration").
- Expone el bootstrap de Signals (`/sdk/context`) que usa el SDK de RIO para resolver definiciones de señales activas y su configuración de transporte.
- Gestiona solicitudes de aprobación de despliegue y el registro/carga de artefactos (jars) para servicios.
- Límite de dominio: no ejecuta el procesamiento de datos en sí (eso es de rio-materializer y de los control planes); su rol es orquestación, estado y contrato, no cómputo.

## 🔌 Contratos e interacciones (semi-estable)
- **Expone:** REST sobre `/data-products`, `/data-products/{id}/components`, `.../definitions`, `.../environments`, `.../services`, `.../deployments` (+ `/logs`), `/pipeline/components`, `/bucket/jar`, `/systems/events`, `/sdk/context` (bootstrap de señales del SDK).
- **Consume / produce:** BigQueue como bus principal — productores (`DeploymentTriggerProducer`, `ActionsTriggerProducer`, `DataProductChangedProducer`) y consumidores (`DeploymentResultConsumer`, `ActionResultConsumer`, `ComponentRuntimeStatusConsumer`, `CpCapabilityConsumer`). Clientes REST dedicados hacia los control planes de Kafka (`KafkaControlPlaneClient`, peek de mensajes) y Flink (`FlinkControlPlaneClient`, deploy de código).
- **Llama a / lo llaman:** [[rio-materializer]] (integración externa documentada en el repo), control planes [[rio-controlplane-kafka]] y [[rio-controlplane-flink]], servicio de aprobaciones (Odin) vía `ApprovalsClient`. Consume las libs [[rio-sdk-events]] (`1.3.1`) y `rio-core-java`. Es invocado por el SDK de RIO para el bootstrap de señales.

## 🧩 Implementación (volátil · last_verified: 2026-08-10)
> Detalle que puede cambiar sin cambiar la responsabilidad.
- **Stack:** Java (toolchain 25) · Spring Boot 3.5.13 · Spring Security · MySQL 8 (JPA/Hibernate). Nota: `README.md` del repo dice Spring Boot 3.3 / Java 21 — desactualizado respecto a `build.gradle`.
- **Librerías / infra clave:** `rio-sdk-events:1.3.1`, `rio-core-java:1.0.7`, `java-melitk-config` (Fury Config/ProfileManager), `java-toolkit-kvs`, `java-melitk-workqueues`, `tiger-java-helper` (auth), AWS S3 SDK (storage de jars), New Relic, SpringDoc/OpenAPI.
- **Patrón notable:** Productor/consumidor BigQueue para disparar y resolver despliegues y acciones de forma asíncrona, con clientes dedicados por control plane (Kafka/Flink) y timeout/retry sobre el ciclo de despliegue.

## 🔗 Relaciones
- [[rio-materializer]]
- [[rio-controlplane-kafka]]
- [[rio-controlplane-flink]]
- [[rio-sdk-events]]

## 📌 Provenance
- Repo: `melisource/fury_rio-playmaker` · Local: `~/fuentes/rio-playmaker`
- Fuentes leídas: `README.md`, `CLAUDE.md`, `graphify-out/GRAPH_REPORT.md` (grep dirigido, no volcado completo), `build.gradle`
- `last_verified: 2026-08-10` · `confidence: high`

## ✅ Tareas relacionadas

```tasks
sort by priority
not done
description includes rio-playmaker
short mode
hide task count
```
