---
type: index
schema_version: 1
status: active
icon: 🗂️
slug: applications-index
area: "[[Personal]]"
project: "[[AGENTS OS]]"
created: 2026-07-02
updated: 2026-09-10
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

- **Páginas:** 16 aplicaciones
- **Última ingesta:** 2026-09-10 (F-04 Magic Allocation, Version Seal and Handoff Contract).
- **Estado:** active

## 📂 Catálogo

| App | Una línea | Área | Lang |
|---|---|---|---|
| [[echo-core]] | Motor principal, base de datos y diario de operaciones (Trade Journal) de Echo. | [[Echo]] | Go |
| [[echo-forge]] | Fábrica y admisor cuantitativo E2E de estrategias de trading; orquesta SQX y entrega finalistas a Echo Core. | [[Echo]] | Go, Java |
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

| Recurso | Alcance / vigencia |
|---|---|
| [[Echo SDK — Canonical Forge Integration and Analytics Contract V1]] | Contrato compartido propuesto: Echo SDK puro, convergencia Analytics/Scope/TradeSet/MetricSet, handoff/ingestion, B con gates acotados; sin otro TOP. |
| [[Echo + Echo Forge — Architecture Durability and Contract Review — Fable 5.1]] | Revisión de durabilidad V1 2026-09-07: decisión B (freeze con correcciones acotadas C-1…C-7), freeze matrix, O1–O3 reclasificadas, 20 leave-ugly, sin TOP; source db8a022/e25165ba. |
| [[Echo SDK — Canonical Contract Final Freeze Review — Fable 5.1]] | Freeze review final del contrato Echo SDK 2026-09-07: B con FR-1…FR-5 (identidad por inputs, regla key/basis/unit/formula, Scope sin valuation, wire agnóstico, record_digest), matriz de identidad, freeze matrix, áreas cerradas; sin TOP. |
| [[Echo — Forge Ingestion, Runtime Identity and Live Authority Contract V1]] | Contrato V1 propuesto: identidad/versión, ingestión, enrollment, raw/time/coverage y routing/policy; O1/O3 defaults técnicos Fable; catálogo CC pendiente. Body/SDK refinados por contrato canónico SDK; source Symphony db8a022. |
| [[Echo + Echo Forge — Arquitectura de producto, gaps y roadmap de cierre 2026]] | Auditoría master de source remoto al 2026-09-06: contratos frozen, gaps, 32 deudas, analytics/portfolios, calendario y roadmap ejecutable; evidencia física reportada separada de source. |
| [[Echo + Echo Forge — Independent Reality Check and Time-to-Value Plan]] | Deltas independientes, triage por reachability, mínimo V1, alternativas y siete hitos; ningún nuevo freeze. |
| [[Echo + Echo Forge — Evidencia de revisión independiente 2026-09-06]] | Source y evidencia actual sanitizada: binarios/DB/front, cohortes desde junio y archivo anterior, límites de provenance. |
| [[Echo — Fuentes de arquitectura y producto 2026-09-06]] | Provenance Echo master 04c16bd y decisiones owner; source ledger del recurso. |
| [[Echo Forge — Fuentes de arquitectura y producto 2026-09-06]] | Provenance Symphony a10c26c, SDK, contratos y evidencia física; source ledger del recurso. |
| [[Echo Forge — F-01 Canonical Generation Concurrency Contract]] | Contrato técnico F-01: CanonicalStrategyID puro, publication GENERATED con discriminator `ExecutionIntentKey`, sin HOST_KEY; sin migration. |
| [[Echo Forge — F-02 Finalist Model V2 Contract]] | Contrato técnico F-02: membership estructural ≠ Top N; Promotion 2.0.0; identity requested-vs-HTM; Campaign nullable rank; migration 014. |
| [[Echo Forge — F-03 SQX Long-Running Contract]] | Contrato F-03: elapsed ≠ failure; ceiling `MaxInt64ns−1s`; ScheduleToClose 0; Adaptive DEPRECATED no-touch; process-tree cancel; migration NONE. |
| [[Echo Forge — F-04 Magic Allocation, Version Seal and Handoff Contract]] | Contrato F-04: allocation CAS 1:1 StrategyRef↔magic; stamp/readback fail-closed; StrategyVersion S0; HandoffManifestV1 write-once; CC_MISSING_OWNER_GATE; migration 015. |

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
