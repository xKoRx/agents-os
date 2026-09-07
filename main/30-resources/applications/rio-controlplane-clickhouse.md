---
type: application
schema_version: 1
status: active
slug: rio-controlplane-clickhouse
area: "[[Meli]]"
lang: Java
github: https://github.com/melisource/fury_rio-controlplane-clickhouse
path: ~/fuentes/rio-controlplane-clickhouse
aliases:
  - rio controlplane clickhouse
tags:
  - kind/application
  - area/meli
  - app/rio-controlplane-clickhouse
created: 2026-08-10
updated: 2026-08-10
last_verified: 2026-08-10
confidence: high
---

# rio-controlplane-clickhouse

> [!info]+ rio-controlplane-clickhouse
> **Rol:** Control plane RIO que gestiona el ciclo de vida de recursos ClickHouse (clusters, schemas, tablas, vistas materializadas, usuarios) vía REST y deployments dirigidos por eventos · **Área:** [[Meli]] · **Plataforma:** [[RIO]]
> **Repo:** [remote](https://github.com/melisource/fury_rio-controlplane-clickhouse) · **Local:** `~/fuentes/rio-controlplane-clickhouse` · **Lang:** Java

## 🎯 Responsabilidad (estable)
- Control plane de la plataforma de datos RIO para ClickHouse: crea/administra clusters, schemas, tablas, materialized views, usuarios/grants y warehouses.
- Orquesta deployments de forma síncrona (REST CRUD) y asíncrona (evento `DeploymentRequestedEvent` recibido vía Fury Streams), con idempotencia sobre KVS.
- Ejecuta acciones puntuales sobre ClickHouse (ej. `describe table`) y expone métricas/jobs periódicos.

## 🔌 Contratos e interacciones (semi-estable)
- **Expone:** REST API — clusters, schemas, tablas, materialized views, provisioning de usuarios, disparo de acciones (`ActionTriggerController`), `POST /events` (deployments), `POST /jobs/metrics`, `GET /ping`.
- **Consume / produce:** consume `DeploymentRequestedEvent` vía Fury Streams; publica eventos de ciclo de vida de deployment (STARTED/UPDATED/FINISHED) vía Fury Streams (`rio-sdk-events`) y BigQueue; persiste estado de deployment en Fury KVS (idempotencia); usa Fury Secrets para credenciales; llama a la API de ClickHouse Cloud (discovery + ejecución SQL) y a un servicio de KMS interno para cifrar passwords de usuarios.
- **Llama a / lo llaman:** lo invoca [[rio-materializer]] (dispara deployments) y consumidores REST directos (posible UI tipo rio-frontend, Fury Cron para métricas); llama a servicio interno de KMS para provisioning de usuarios.

## 🧩 Implementación (volátil · last_verified: 2026-08-10)
- **Stack:** Java (JDK con `--enable-preview`, README menciona JDK 25) · Spring Boot 3.5.16 · Gradle · Jetty (Tomcat excluido) · SpringDoc OpenAPI.
- **Librerías / infra clave:** `com.clickhouse:client-v2:0.9.1` (cliente ClickHouse) · `java-toolkit-kvs:0.6.1` (KVS) · `mqclient:3.4.9` (BigQueue) · `rio-sdk-events:1.3.0` + `java-melitk-streams:3.4.6` (Fury Streams) · `resilience4j-retry:2.2.0` (patrón ResilientProxy) · `spring-boot-starter-secrets` + `java-melitk-secrets` (Fury Secrets) · New Relic, OpenTelemetry, Datadog metrics.
- **Patrón notable:** organización por dominio con separación CQRS (`command`/`query`) en `cluster`, `schema`, `table`, `materializedview`; capas `adapter/rest` + `application` + `client/impl` por módulo; `ResilientProxy` con estrategias de reintento (`shared/resilience`).

## 🔗 Relaciones
- [[rio-materializer]]
- [[rio-controlplane-kms]]

## 📌 Provenance
- Repo: `melisource/fury_rio-controlplane-clickhouse` · Local: `~/fuentes/rio-controlplane-clickhouse`
- Fuentes leídas: `README.md`, `build.gradle`, estructura `src/main` (paquetes `cluster`, `schema`, `table`, `materializedview`, `deployment`, `users`, `warehouse`, `action`, `shared`), controllers REST (`SchemaController`, `ClusterController`, `JobController`, `ActionTriggerController`, `DeploymentEventController`, `UserProvisioningController`, `PingController`), `meli/extracted/functional-spec.md` y `meli/extracted/raw/code-analysis/{architecture,fury-services}/*.md` (specs internas generadas por reverse-eng, marcadas 🔸 CODE_ONLY). No existe `ARCHITECTURE.md` ni `graphify-out/GRAPH_REPORT.md` con contenido de arquitectura útil (solo índice de comunidades).
- Nota: el README raíz conserva el texto scaffold genérico ("basic model for JDK 25 / Spring") sin descripción de rol propia; el rol se infirió de código + specs internas `meli/extracted/*`, de ahí que igual se documenten aquí volátiles con `last_verified`.
- `last_verified: 2026-08-10` · `confidence: high`

## ✅ Tareas relacionadas

```tasks
sort by priority
not done
description includes rio-controlplane-clickhouse
short mode
hide task count
```
