---
type: decision
schema_version: 1
scope: project
created: "2026-09-03"
updated: "2026-09-03"
area: "[[Echo Forge]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[Symphony]]"
entities: []
related:
  - "[[2026-09-04-forge-campaign-orchestration-contract-broken]]"
  - "[[2026-09-04-echo-forge-c3-lean-recert-blocked]]"
aliases: []
confidence: verified
source_session: ECHO-FORGE-CAMPAIGN-TELEMETRY-AND-REPLAY-FIX-0.2.89-NORMAL
load_policy: when_project_loaded
indexable: true
index_priority: high
tags:
  - kind/decision
  - scope/replace-me
---

# 2026-09-03-forge-campaign-telemetry-replay-fix

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Contexto

- El baseline autorizado de Symphony es `7047a9c112502dcb68387745149eed95405b0aae`, el SDK authority es `c85594440f6755443ceb97ec4e333cd0ddb5b0ed` y la release física permanece en `0.2.88`.
- `ActivityTelemetryInterceptor` del SDK exige un único argumento que implemente `TelemetryCarrier`; los cinco requests ForgeCampaign fallaban antes de ejecutar la activity y el WorkflowID runtime hacía fallar el replay con `TMPRL1100`.

## Decisión

- Implementar `GetTelemetry() telemetry.Context` en `ForgeCampaignStartRequest`, `ForgeCampaignResolveWaveRequest`, `ForgeCampaignFinalizeWaveRequest`, `ForgeCampaignCancelRequest` y `ForgeCampaignFailContractRequest`, devolviendo exactamente `telemetry.Context{}` y sin agregar campos serializados ni telemetry al workflow input.
- Mantener assertions explícitas contra `runtime.TelemetryCarrier` y `sdktemporal.TelemetryCarrier` para los cinco tipos y probar el interceptor SDK real con cada request.
- Eliminar únicamente la comparación de `workflow.GetInfo(ctx).WorkflowExecution.ID` contra el token-derived ID del path determinista de `ForgeCampaignWorkflow`; conservar la captura de correlación runtime para el Activity request.
- Mantener la autoridad canónica del WorkflowID en `forgeCampaignStartContract`, `ForgeCampaignDispatch.Validate` y `RecordForgeCampaignDispatch` antes de persistir.

## Rationale

- `TelemetryCarrier` es un contrato de transporte no durable; el contexto zero-value permite que el SDK cree un span sin parent cuando el input histórico no transporta trace.
- El WorkflowReplayer usa metadata runtime `ReplayId`, por lo que comparar ese valor dentro del workflow confunde metadata del replay con identidad de negocio; la identidad sigue validándose en dispatcher y persistence boundary.

## Consecuencias

- Los cinco request payloads históricos siguen round-tripeando sin campo `Telemetry`; `GetTelemetry()` retorna zero-value al deserializar payloads antiguos.
- El workflow puede emitir `forge_campaign_start` bajo un WorkflowID de testsuite distinto, mientras la dispatch/persistence authority continúa rechazando un WorkflowID durable incorrecto.

## Alternativas descartadas

- Agregar un campo durable `Telemetry`, transportar `telemetry.Context` en `ForgeCampaignWorkflowInput`, introducir un branch de replay, `ReplayId`, flags de ambiente o `GetVersion`, o debilitar las validaciones dispatcher/persistence.
