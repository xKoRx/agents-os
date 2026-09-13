---
type: index
schema_version: 1
status: active
icon: 🗂️
slug: applications-index
area: "[[Personal]]"
project: "[[AGENTS OS]]"
created: 2026-07-02
updated: 2026-09-12
reviewed: 2026-07-04
aliases:
  - applications index
  - índice de aplicaciones
  - catálogo de apps
cssclasses:
  - wide
tags:
  - kind/index
  - area/personal
  - project/agents-os
---

# 🗂️ Applications — Índice

> [!info] Wiki compilada de recursos
> Catálogo curado del dominio `applications/`. El agente lo actualiza en cada *ingest*. Reglas: [[30-resources/00-RESOURCE-WIKI|Resource Wiki]] · Bitácora: `log.md`.

## 📊 De un vistazo

- **Páginas:** 14 aplicaciones (catálogo raíz) + subdominio `echo/`
- **Última ingesta:** 2026-09-13 (consolidación KBC → subdominio `echo/`).
- **Estado:** active

## 📂 Catálogo

| App | Una línea | Área | Lang |
|---|---|---|---|
| [[30-resources/applications/echo/00-index|Echo (subdominio)]] | Plataforma de ejecución + fábrica cuantitativa + frontera: ver sub-índice. | [[Echo]] | Go, Java |
| [[stager-app]] | Reconciliador one-shot de releases locales verificadas; MinIO y Linux/Windows, independiente del consumer. | [[Echo]] | Go |
| [[rio-playmaker]] | Orquestador central de RIO: gestiona data products, componentes y despliegues, y coordina los control planes vía BigQueue. | [[Meli]] | Java |
| [[ads-signals-frontend]] | UI moderna (RIO Frontend v3, FSD): canvas drag-and-drop de pipelines, lifecycle deploy/stop, catálogo de entidades y observabilidad. | [[Meli]] | TypeScript |
| [[rio-frontend]] | ⚠️ **En deprecación** — UI legacy (SPA/DrawFlow) de RIO; reemplazada por [[ads-signals-frontend]]. | [[Meli]] | TypeScript |
| [[ads-signals-catalog]] | Fuente de verdad de metadatos de señales ADS: CRUD de señales, schemas, SLOs y destinations (REST + MySQL). | [[Meli]] | Go |
| [[rio-materializer]] | ⚠️ **En deprecación** — traduce solicitudes de presentación en infra real (K8s, S3/GCS, MSK, Flink, ClickHouse, KMS); solo le queda el flujo de inicio Signals/Catalog. | [[Meli]] | Java |
| [[rio-controlplane-kafka]] | Ciclo de vida de topics Kafka (PROVISION/UPDATE/DEPROVISION) + PEEK; disparado por Playmaker vía BigQueue. | [[Meli]] | Java |
| [[rio-controlplane-flink]] | Ciclo de vida de apps Apache Flink SQL sobre AWS Kinesis Data Analytics (CQRS + event-driven). | [[Meli]] | Java |
| [[rio-controlplane-clickhouse]] | Ciclo de vida de recursos ClickHouse (clusters, schemas, tablas, MVs, usuarios) vía REST + deployments event-driven. | [[Meli]] | Java |
| [[rio-controlplane-fury]] | Control plane del "pusher": provisiona y reconcilia pipelines de enrutamiento de eventos (Kafka↔Fury Streams). | [[Meli]] | Kotlin |
| [[rio-controlplane-kms]] | Cifrado/descifrado de secretos delegando en CKaaS y persistiendo en KVS. | [[Meli]] | Java |
| [[rio-controlplane-observability]] | Automatiza monitores Datadog, subscription filters de CloudWatch y cuotas de logs para apps Flink. | [[Meli]] | Java |
| [[rio-controlplane-signals]] | ⚠️ Repo scaffold Fury vacío (placeholder, propósito por definir); "Signals" = otro nombre de RIO, no un sub-dominio. | [[Meli]] | Java |
| [[rio-sdk-events]] | SDK/librería de eventos RIO: publica vía BigQueue + Fury Streams; contratos alineados a topics Kafka. | [[Meli]] | Java |

## Arquitectura de producto

→ Los contratos vigentes, provenance e histórico de Echo/Echo Forge viven en [[30-resources/applications/echo/00-index|Echo — Índice]] (subdominio `echo/`).

## 🚨 Salud (del último lint)

- **Huérfanos:** pendiente — correr `resource-wiki-lint-reindex` tras el reindex de Graphify depurado.
- **Contradicciones:** ninguna detectada al bootstrap.
- **Conceptos sin página:** `commons-middleend` (base de search-middleware) mencionado pero sin página propia — candidato a ingest.

## 🔗 Links

- [[30-resources/00-RESOURCE-WIKI|Reglas de la Resource Wiki]]
- [[RIO]] — servicio/plataforma que agrupa las aplicaciones del equipo Signals.
- [[echo-core-changelog]] — bitácora canónica de cambios de [[echo-core]].
- `log.md` — bitácora cronológica de este dominio
- [[graphify]] — índice derivado sobre estas páginas
