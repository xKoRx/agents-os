---
type: service
schema_version: 1
status: active
area: "[[Meli]]"
repo:
path: ~/fuentes
slug: rio
last_verified: 2026-09-01
confidence: high
aliases:
  - RIO
  - Real time Input Output
  - RIO platform
  - plataforma RIO
  - Signals
  - equipo Signals
  - ADS Signals
tags:
  - kind/service
  - area/meli
  - app/rio
created: 2026-08-10
updated: 2026-09-01
---

# RIO

> [!info]+ RIO — plataforma de datos del equipo Signals
> **Área:** [[Meli]] · **Equipo:** Signals · **Workspace:** [[Fuentes — Workspace de repositorios]]
> **Metodología base:** [[data-mesh]] · **Índice de apps:** [[applications-index]] · **Vista de sistema:** [[00-index|RIO Atlas]] ([[system-map]] · [[integration-map]])

> [!note] Nombres y org
> **RIO = Real time Input Output**, también llamado **Signals** (dos nombres de la misma plataforma/equipo; no es un sub-dominio). **Signals** es el equipo (~20+ personas) dentro de **ADS / Advertising** (~200 personas) en MercadoLibre, y es **dueño de las apps RIO**. Es decir: ADS es la org grande; Signals el equipo dentro de ADS; RIO/Signals la plataforma. **El dominio del equipo son estas apps** (2026-08-11: ~13 — orquestador + materializer⚠️ + 7 control planes + sdk-events + 2 frontends [ads-signals-frontend, rio-frontend⚠️] + ads-signals-catalog; ⚠️ = en deprecación).

## Propósito

- RIO (**Real time Input Output**), también llamado **Signals**, es la **plataforma de datos self-serve** del equipo: un **control plane** que gestiona el ciclo de vida de *data products* y de la infraestructura de datos subyacente (Kafka, Flink, ClickHouse, Fury Streams), más su governance (cifrado, observabilidad). El dominio del equipo son las 10 apps de abajo.
- Materializa en la práctica los 4 principios de **data mesh** (ver [[data-mesh]]): ownership por dominio, datos como producto, infra self-serve y governance federada.

## Responsabilidades (estable)

- **Orquestación de data products:** [[rio-playmaker]] recibe la intención (crear/desplegar componentes) y coordina la ejecución.
- **Provisioning de infra de datos:** control planes por tecnología — [[rio-controlplane-kafka]], [[rio-controlplane-flink]], [[rio-controlplane-clickhouse]], [[rio-controlplane-fury]].
- **Materialización real:** [[rio-materializer]] traduce la solicitud en operaciones concretas de infraestructura (K8s, S3/GCS, MSK, Flink, ClickHouse, KMS). ⚠️ **En deprecación** — el flujo nuevo va directo Playmaker→CP; solo le queda el flujo de inicio de Signals/Catalog.
- **Presentación (UI):** [[ads-signals-frontend]] (RIO Frontend v3, FSD) es la UI actual; [[rio-frontend]] es la legacy ⚠️ **en deprecación**. Ambas componen data products en un canvas y delegan en Playmaker.
- **Catálogo de señales:** [[ads-signals-catalog]] (Go) — fuente de verdad de metadatos de señales (schemas, SLOs, destinations).
- **Governance:** cifrado ([[rio-controlplane-kms]]) y observabilidad ([[rio-controlplane-observability]]).
- **Contratos de eventos:** [[rio-sdk-events]] (librería compartida).
- **Señales:** [[rio-controlplane-signals]] materializa `catalog-signal`, `bigqueue-signal` y `stream-signal` vía Catalog/Collector, con idempotencia KVS y resultados de deployment.
- **Context of signals (deuda):** hoy los frontends arman las relaciones y las properties derivadas (`${X.field}`, `destinations[]`) en el cliente; el objetivo del [[Onboarding Signals]] es mover esa lógica al [[rio-playmaker]]. Flujo end-to-end params→outputs documentado en [[signals-context-flow]].

## Operación

- **Stack transversal:** JVM (Spring Boot, JDK 21/25); Java salvo [[rio-controlplane-fury]] en **Kotlin**. Desplegado en Fury, Docker, Gradle.
- **Flujo de deployment vigente:** [[rio-playmaker]] persiste execution/group/runs/deployments y despacha `DeploymentTriggerMessage` por **BigQueue** para 11 `component_type` explícitos; el catch-all usa [[rio-materializer]] por REST. Los CP publican `DeploymentResultMessage` por `rio-deployment-result`, que Playmaker consolida antes de avanzar el siguiente batch. El routing se decide sólo por `component_type`; detalle actualizado en [[Deployments en RIO — flujo completo]].
- **Orden actual:** aunque existe cálculo topológico, `FORCE_CONFIG_ORDER = true` lo omite y fuerza no-engines primero, engines después. Dispatch inicial y batch advance son eventos `AFTER_COMMIT` asíncronos sin outbox durable.
- **Contratos de eventos:** [[rio-sdk-events]] publica vía BigQueue + Fury Streams; topics alineados a dominios Kafka de RIO.
- **Patrones recurrentes:** CQRS (flink, clickhouse), reconciler tipo k8s-controller (fury), sagas asíncronas con timeout (materializer).
- **Estado por pieza (a 2026-09-01):** todos los CP del deployment path tienen lógica; la confiabilidad de entrega es heterogénea. Fury conserva desired/observed state y reintenta publicación; Kafka/Flink/ClickHouse desprenden trabajo después del ACK y exponen ventanas de pérdida.
- **Grafo global para navegar deps:** `~/fuentes/graphify-signals.json` (merge de 14 grafos: 12 `rio-*` + 2 `ads-signals-*`, 54030 nodos / 112407 edges a 2026-08-11). Índice operativo del workspace: `~/fuentes/AGENTS.md`.

## Relaciones

- Área [[Meli]] · Workspace [[Fuentes — Workspace de repositorios]] · Metodología [[data-mesh]] · Proyecto [[Onboarding Signals]] · Presentación [[Presentación deployments en RIO]] · Knowledge [[ads-signals-knowledge-library]] · Índice [[applications-index]]
- Vista de sistema: [[00-index|RIO Atlas]] ([[system-map]] · [[integration-map]]) · Herramienta [[rio-inspector]]
