---
type: change_log
schema_version: 1
scope: session
created: "2026-09-03"
updated: "2026-09-03"
area: "[[Echo Forge]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[Symphony]]"
entities: []
related: []
aliases: []
confidence: verified
source_session: ECHO-FORGE-CAMPAIGN-TELEMETRY-AND-REPLAY-FIX-0.2.89-NORMAL
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-09-03-echo-forge-campaign-telemetry-replay-fix

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** created + updated
- **Archivo(s):**
  - `xKoRx/symphony:sqx/activities/worker/forge_campaign_activity.go`
  - `xKoRx/symphony:sqx/activities/worker/forge_campaign_activity_test.go`
  - `xKoRx/symphony:sqx/activities/worker/forge_campaign_telemetry_carrier_test.go`
  - `xKoRx/symphony:sqx/workflows/forge_campaign_workflow.go`
  - `xKoRx/symphony:sqx/workflows/forge_campaign_workflow_test.go`
  - `xKoRx/symphony:sqx/core/domain/forge_campaign_test.go`
  - `80-agents/memory/public/decision/symphony/2026-09-03-forge-campaign-telemetry-replay-fix.md`
  - `10-projects/Echo Forge/agentes/Echo Forge - Arquitectura de Datos y Migración de Persistencia.md`

## Motivo

- Corregir exclusivamente el contrato TelemetryCarrier de los cinco ForgeCampaign requests y retirar la dependencia replay-unsafe del WorkflowID runtime.

## Fuentes usadas

- Checkpoint canónico de Echo Forge, RCA conocida `FORGE_CAMPAIGN_START_TELEMETRY_CARRIER_CONTRACT_BROKEN`, `TEMPORAL_REPLAY_FAILURE`, SDK interceptor estricto y autoridades dispatcher/persistence.

## Resolución aplicada

- Se implementaron los cinco getters zero-value, diez assertions compile-time, tests de interceptor real, payload histórico, replay-safe workflow, correlación durable wrong-ID y distinción execution Wave/RequestID.

## Validación

- Focales no-race, race, vet, `git diff --check` y replay físico read-only PASS; suite amplia barata mantiene fallos preexistentes ajenos por `flow_run_start` no registrado en tests WFM. `staticcheck` omitido por no estar instalado.

## Compartibilidad

- **Scope:** local / team
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Las notas son recuperables; el código se puede revertir con el commit `a846adca3896cf578cf27eb854d9ea9bb725997d` si el lead lo solicita, sin tocar release ni producción.
