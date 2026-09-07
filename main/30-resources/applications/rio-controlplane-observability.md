---
type: application
schema_version: 1
status: active
slug: rio-controlplane-observability
area: "[[Meli]]"
lang: Java
github: https://github.com/melisource/fury_rio-controlplane-observability
path: ~/fuentes/rio-controlplane-observability
aliases:
  - rio controlplane observability
tags:
  - kind/application
  - area/meli
  - app/rio-controlplane-observability
created: 2026-08-10
updated: 2026-08-10
last_verified: 2026-08-10
confidence: high
---

# rio-controlplane-observability

> [!info]+ rio-controlplane-observability
> **Rol:** Automatiza monitores Datadog, filtros de logs CloudWatch y cuotas de log para apps Flink del ecosistema RIO, reaccionando a eventos de despliegue y de catálogo de datos · **Área:** [[Meli]] · **Plataforma:** [[RIO]]
> **Repo:** [remote](https://github.com/melisource/fury_rio-controlplane-observability) · **Local:** `~/fuentes/rio-controlplane-observability` · **Lang:** Java

## 🎯 Responsabilidad (estable)
- Componente de observabilidad/governance del control plane de RIO: crea, actualiza y elimina monitores Datadog (incl. process-lag) para apps Flink en base a eventos de infraestructura, gestiona subscription filters de CloudWatch Logs para enrutar logs, y aplica overrides de cuota de logs por app.
- El README del repo conserva el scaffold genérico "Spring Boot app model for JDK 21"; el rol real se infiere del código (`src/main`) y de `CLAUDE.md`, que sí documenta las features reales.

## 🔌 Contratos e interacciones (semi-estable)
- **Expone:** `PATCH/DELETE /monitors/{componentKey}` (alta/baja de monitores Datadog, tras `datadog.monitors.enabled`); `POST /events/data-product-changed` (consumidor BigQueue, tras `datadog.notifications.enabled`); `POST /triggers/deployments` (consumidor BigQueue, tras `bigqueue.deployment-trigger.enabled`); `POST/GET/DELETE /logs/quota-override` (tras `aws.dynamodb.enabled`); `/ping` y actuator health.
- **Consume / produce:** poll SQS sobre la cola `rio-events-011y` (eventos CloudTrail/EventBridge de apps Flink); tópicos BigQueue `rio-data-product-changed-{prod,test}` y `rio-deployment-trigger`; llama a la API de Datadog para gestionar monitores; lee/escribe metadata de criticidad de apps en DynamoDB (tabla `flink-log-quota`); consulta BigQuery (`AdsRioLogsFilterBigQueryService`) para filtrar logs ADS-RIO; administra subscription filters en CloudWatch Logs vía una Lambda (ARN configurable).
- **Llama a / lo llaman:** casi todas las capacidades están detrás de feature flags (`@ConditionalOnProperty`) independientes entre sí. No hay evidencia directa en el repo de qué app produce los tópicos BigQueue consumidos; se mantienen como relaciones RIO conocidas sin confirmar el productor exacto.

## 🧩 Implementación (volátil · last_verified: 2026-08-10)
- **Stack:** Spring Boot 3.5.14 (según `build.gradle`; `CLAUDE.md` menciona 3.4.7 — desalineado, ver Provenance) · Java 21 con virtual threads y `--enable-preview` · Jetty embebido · Gradle.
- **Librerías / infra clave:** AWS SDK v2 (SQS, DynamoDB, CloudWatchLogs, S3), Google Cloud BigQuery, OpenTelemetry API, New Relic agent, java-melitk-secrets (Fury Secrets), meli-restclient, kvsclient, mqclient/BigQueue, springdoc-openapi, Caffeine cache, Lombok.
- **Patrón notable:** feature flags por `@ConditionalOnProperty` a nivel de controller/service (`datadog.monitors.enabled`, `datadog.notifications.enabled`, `bigqueue.deployment-trigger.enabled`, `aws.dynamodb.enabled`) para activar capacidades de forma independiente; retry con backoff exponencial en `CloudWatchSubscriptionFilterService`.

## 🔗 Relaciones
- [[rio-playmaker]]
- [[rio-materializer]]
- [[rio-sdk-events]]

## 📌 Provenance
- Repo: `melisource/fury_rio-controlplane-observability` · Local: `~/fuentes/rio-controlplane-observability`
- Fuentes leídas: `README.md` (scaffold, no aporta rol real), `CLAUDE.md`, `build.gradle`, `innersource.json` (template sin llenar, ignorado), `.fury`, `docs/specs/swagger.yaml`, `docs/runbooks/subscription-filter-backfill.md`, `graphify-out/GRAPH_REPORT.md`, `src/main` (paquetes `controller`, `service`, `store`, `domain/datadog`, `telemetry`, `kvs`, `config`), `src/main/resources/application*.yml`.
- Nota de contradicción: `CLAUDE.md` describe la app como "Spring Boot 3.4.7 scaffold demostrando patrones o11y", pero el código real (`build.gradle` = Boot 3.5.14) implementa lógica de negocio concreta (monitores Datadog, cuotas de logs, consumers de eventos) muy por encima de un scaffold. Se documentó el rol real observado en código.
- `last_verified: 2026-08-10` · `confidence: high`

## ✅ Tareas relacionadas

```tasks
sort by priority
not done
description includes rio-controlplane-observability
short mode
hide task count
```
