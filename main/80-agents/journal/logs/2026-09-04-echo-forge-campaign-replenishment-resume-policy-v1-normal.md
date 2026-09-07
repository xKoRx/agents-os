---
type: change_log
schema_version: 1
scope: session
created: "2026-09-04"
updated: "2026-09-04"
area: "[[Echo]]"
project: "[[Echo Forge]]"
application: "[[xKoRx/symphony]]"
entities: []
related: []
aliases: []
confidence: verified
source_session: "ECHO-FORGE-CAMPAIGN-REPLENISHMENT-RESUME-POLICY-V1-NORMAL"
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# ECHO-FORGE-CAMPAIGN-REPLENISHMENT-RESUME-POLICY-V1-NORMAL

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** created / updated
- **Archivo(s):**
  - `sqx/core/domain/forge_campaign.go`
  - `sqx/core/runtime/config.go`
  - `sqx/core/capabilities/forge_campaign.go`
  - `sqx/adapters/registry-postgres/forge_campaign.go`
  - `sqx/adapters/registry-postgres/migrations/013_forge_campaign_replenishment_policy.up.sql`
  - `sqx/activities/worker/forge_campaign_activity.go`
  - `sqx/adapters/mt5/binding/intake.go`
  - `sqx/activities/worker/steps/steps.go`
  - `sqx/adapters/storage-minio/minio_storage.go`
  - `sqx/activities/watcher/intake.go`
  - `sqx/adapters/registry-postgres/forge_campaign_result.go`
  - `sqx/adapters/registry-postgres/migrations/runner.go`
  - `sqx/core/capabilities/storage.go`
  - `sqx/adapters/registry-postgres/forge_campaign_integration_test.go`

## Motivo

- Ejecutar el contrato NORMAL autorizado sobre source `93c6665` sin crear release `0.2.93` ni Campaign física.

## Fuentes usadas

- Implementación cohesiva del contrato v2: policy con `Validate/CanonicalJSON/Digest`, content digest base+stop+policy, persistencia immutable y migration 013; `BuilderSupplyBatchRef` derivable por `CampaignRef + waveNumber`; contexto typed en snapshot de ola; namespace filename-safe exclusivo del Campaign Builder; preflight antes de registros/MinIO.

## Resolución aplicada

- Migration 013 aplica/reaplica en PostgreSQL efímero. Persistencia v2 devuelve policy exacta, digest y recovery context; política divergente converge a `CONTRACT_CONFLICT`. Directed packages, Campaign Workflow, race, vet y `git diff --check` PASS. Broad gate clasificado por fallos baseline de `sqx/tools`, WFM activity registration y duración infra.

## Validación

- Revertible por `git revert ab21526`; no revertir dirty foráneo.

## Compartibilidad

- **Scope:** local / team
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- `git revert ab21526` en `xKoRx/symphony`, preservando los dirty files foráneos y sin reset/checkout destructivo.
