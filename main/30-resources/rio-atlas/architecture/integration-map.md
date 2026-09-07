---
type: resource
schema_version: 1
status: active
area: "[[Meli]]"
sources:
  - "[[rio-inspector]]"
  - "[[rio-sdk-events]]"
  - "[[RIO]]"
last_verified: 2026-08-10
confidence: high
aliases:
  - RIO Integration Map
  - integration map rio
  - mapa de integraciones RIO
tags:
  - kind/resource
created: 2026-08-10
updated: 2026-08-10
cssclasses:
  - wide
---

# RIO — Integration Map (generado)

> [!warning] Nota generada por [[rio-inspector]]
> Grafo real de integraciones de RIO (producer→consumer→transport→channel→sync), generado desde código/config — **no editar a mano**: regenerar con `cd ~/fuentes/rio-inspector && python3 inspect.py`. Vista de 30 s en [[system-map]]. Parte del [[00-index|RIO Atlas]].

## Síntesis vigente

19 integraciones entre las 10 apps; 13 contratos compartidos.

| Producer | Consumer | Transport | Channel | Kind | Sync |
|---|---|---|---|---|---|
| rio-controlplane-kafka | rio-playmaker | BigQueue | `provisioning-result` | result | async |
| rio-controlplane-kafka | rio-playmaker | BigQueue | `rio-action-result` | result | async |
| rio-controlplane-flink | rio-playmaker | BigQueue | `rio-action-result` | result | async |
| rio-playmaker | rio-controlplane-kafka | HTTP POST (BigQueue fallback) | `rio-action-trigger` | trigger | sync |
| rio-playmaker | rio-controlplane-flink | HTTP POST (BigQueue fallback) | `rio-action-trigger` | trigger | sync |
| rio-playmaker | rio-controlplane-clickhouse | HTTP POST (BigQueue fallback) | `rio-action-trigger` | trigger | sync |
| rio-controlplane-flink | rio-playmaker | BigQueue | `rio-component-runtime-status` | status | async |
| rio-playmaker | rio-controlplane-observability | BigQueue | `rio-data-product-changed` | notification | async |
| rio-controlplane-kafka | rio-playmaker | BigQueue | `rio-deployment-result` | result | async |
| rio-controlplane-flink | rio-playmaker | BigQueue | `rio-deployment-result` | result | async |
| rio-controlplane-fury | rio-playmaker | BigQueue | `rio-deployment-result` | result | async |
| rio-playmaker | rio-controlplane-kafka | HTTP POST (BigQueue fallback) | `rio-deployment-trigger` | trigger | sync |
| rio-playmaker | rio-controlplane-flink | HTTP POST (BigQueue fallback) | `rio-deployment-trigger` | trigger | sync |
| rio-playmaker | rio-controlplane-observability | HTTP POST (BigQueue fallback) | `rio-deployment-trigger` | trigger | sync |
| rio-playmaker | rio-controlplane-fury | HTTP POST (BigQueue fallback) | `rio-deployment-trigger` | trigger | sync |
| rio-playmaker | rio-materializer | REST | `materialize` | materialization | sync |
| rio-materializer | rio-controlplane-kms | REST | `encrypt/decrypt` | secrets | sync |
| rio-materializer | control-planes | REST | `rio-controlplanes.melisystems.com` | cp-api | sync |
| control-planes | rio-materializer | Fury Streams | `/v2/events (ControlPlaneEvent)` | lifecycle | async |

### Contratos compartidos ([[rio-sdk-events]])

`ControlPlaneEvent` · `ControlPlaneFinishedEvent` · `ControlPlaneStartedEvent` · `ControlPlaneUpdatedEvent` · `DeploymentEvent` · `DeploymentFinishedEvent` · `DeploymentRequestedEvent` · `DeploymentRequestedFailedEvent` · `DeploymentStartedEvent` · `DeploymentUpdatedEvent` · `Event` · `PublishEvent` · `RioEvent`

## Evidencia y provenance

- Generado por [[rio-inspector]] (`~/fuentes/rio-inspector/inspect.py`) desde config + código de los 10 repos en `~/fuentes`. Artefactos crudos: `~/fuentes/rio-inspector/rio-integrations.{json,mmd}` (fuera del vault, invariante 12).
- Heurística: descubre topics en `application*.yml`, clasifica rol por tipo de canal (trigger/result/status) y tipo de repo, cruza con clases `*Publisher`/`*Consumer`/`*TriggerController`, y añade aristas REST/stream conocidas con evidencia citada.
- `last_verified: 2026-08-10`.

### Detalle por app (generado)

- **rio-playmaker** · _orchestrator_ — produce: `rio-action-trigger`, `rio-data-product-changed`, `rio-deployment-trigger`; consume: `rio-deployment-result`; usa rio-sdk-events: sí
- **rio-materializer** · _executor_ — produce: —; consume: —; usa rio-sdk-events: sí
- **rio-controlplane-kafka** · _control-plane_ — produce: `provisioning-result`, `rio-action-result`, `rio-deployment-result`; consume: `rio-action-trigger`, `rio-deployment-trigger`; usa rio-sdk-events: sí
- **rio-controlplane-flink** · _control-plane_ — produce: `rio-action-result`, `rio-component-runtime-status`, `rio-deployment-result`; consume: `rio-action-trigger`, `rio-deployment-trigger`; usa rio-sdk-events: sí
- **rio-controlplane-clickhouse** · _control-plane_ — produce: —; consume: —; usa rio-sdk-events: sí
- **rio-controlplane-fury** · _control-plane_ — produce: `rio-deployment-result`; consume: —; usa rio-sdk-events: sí
- **rio-controlplane-kms** · _rest-service_ — produce: —; consume: —; usa rio-sdk-events: no
- **rio-controlplane-observability** · _control-plane_ — produce: —; consume: `rio-data-product-changed`, `rio-deployment-trigger`; usa rio-sdk-events: no
- **rio-controlplane-signals** · _scaffold_ — produce: —; consume: —; usa rio-sdk-events: no
- **rio-sdk-events** · _library_ — produce: —; consume: —; usa rio-sdk-events: sí

## Límites y contradicciones

- **Artefacto generado:** no editar la tabla a mano; regenerar con `rio-inspector` (la regeneración reescribe esta nota de forma idempotente y conforme).
- **Confianza media:** `rio-materializer`↔`control-planes` (REST vía `base-url`) y `control-planes`→`materializer` (Fury Streams `/v2/events`); reparto fino por control plane a confirmar con el tracer bullet.
- **Gap:** `rio-controlplane-clickhouse` consume trigger pero no se detectó su canal de result; `rio-controlplane-kms`/`observability` no dependen de `rio-sdk-events`.
