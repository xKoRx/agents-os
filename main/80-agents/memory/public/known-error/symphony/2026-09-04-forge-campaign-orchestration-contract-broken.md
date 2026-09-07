---
type: known_error
schema_version: 1
scope: project
created: "2026-09-04"
updated: "2026-09-04"
area: "[[Echo]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[Symphony]]"
entities: []
related:
  - "[[2026-09-04-echo-forge-c3-lean-recert-blocked]]"
  - "[[2026-08-31-forge-campaign-stop-policy-v1-contract]]"
aliases:
  - FORGE_CAMPAIGN_START_TELEMETRY_CARRIER_CONTRACT_BROKEN
  - campaña no replayable WorkflowID assertion
confidence: verified
source_session: ECHO-FORGE-C3-LEAN-RECERT-NORMAL
load_policy: when_error_matches
indexable: true
index_priority: high
tags:
  - kind/known-error
  - scope/project
  - project/echo-forge
---

# 2026-09-04-forge-campaign-orchestration-contract-broken

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Síntoma

- Toda `ForgeCampaignWorkflow` queda en reintento infinito de `forge_campaign_start`: error por intento `activity argument does not implement TelemetryCarrier` en el worker 0.2.88; la campaña nunca materializa su wave 1 (0 hijos, 0 decisiones, 0 evaluaciones).
- En replay: `Workflow panic [TMPRL1100] lookup failed for scheduledEventID to activityID: scheduleEventID: 5, activityID: 5` sobre el historial real del padre de campaña.

## Causa

- Defecto 1: el interceptor estricto del SDK (`xKoRx/sdk pkg/shared/temporal/interceptor.go:122-124`) exige que el primer argumento de toda actividad implemente `TelemetryCarrier`; los 5 request types de orquestación (`ForgeCampaignStartRequest`, `ForgeCampaignResolveWaveRequest`, `ForgeCampaignFinalizeWaveRequest`, `ForgeCampaignCancelRequest`, `ForgeCampaignFailContractRequest`, `sqx/activities/worker/forge_campaign_activity.go:26-66`) no implementan `GetTelemetry()` ni tienen assertions, a diferencia de `FlowRunStartRequest`/`FlowRunSealRequest` (`flow_run_lifecycle_activity.go:55-58`). Con `RetryPolicy MaximumAttempts:0` (infinito) la campaña queda viva pero sin progreso.
- Defecto 2: `ForgeCampaignWorkflow` (`sqx/workflows/forge_campaign_workflow.go:43`) valida `info.WorkflowExecution.ID != expectedID` y retorna temprano; el replayer del SDK corre con WorkflowID fijo `ReplayId` (`internal_worker.go:1905`, sin override) ⇒ el comando de actividad nunca se registra en replay y el evento 5 pánico TMPRL1100. El workflow es no-replayable por construcción.

## Impacto

- `ECHO_FORGE_CAMPAIGN_STOP_POLICY_V1_C3` no puede certificarse físicamente: ningún gate (topología, promotion, stop evaluation, ConfigSourceWave, dedupe entre waves) es alcanzable.
- Cada intake de campaña deja una campaña colgada RUNNING (Temporal) / PENDING (PG `sqx.forge_campaigns`, temporal ids NULL) con reintento cada 30s ilimitado.

## Detección

- Sesión `ECHO-FORGE-C3-LEAN-RECERT-NORMAL` (2026-09-04): `DescribeWorkflowExecution` mostró pending activity `forge_campaign_start` state=Scheduled attempt 34→54+ con `lastFailure=activity argument does not implement TelemetryCarrier`; log worker zeus `/var/log/symphony/symphony-worker.log` con attempts crecientes; PG `sqx.forge_campaigns` fila `592944e2-1a30-426c-93c6-ebba351dc786` PENDING con 0 waves/stop_evaluations/finalists.
- Replay control PASS (padre cancel smoke 470 eventos, nondeterminism=NONE) vs REPLAY_FAILURE del padre de campaña con la misma herramienta en worktree detached `7047a9c`.

## Mitigación

- No reintentar intake de campaña hasta el fix (cada intento crea residuo colgado).
- Source fix aplicado en `a846adc3896cf578cf27eb854d9ea9bb725997d`: cinco getters zero-value con assertions runtime/SDK, payload durable intacto y eliminación del gate runtime WorkflowID del workflow; las authorities dispatcher/persistence siguen intactas.
- La Campaign residual `592944e2-…` continúa bajo release física 0.2.88 como evidencia contaminada; no fue mutada ni usada como CERT-A. Release nueva, contención segura y nuevas identidades quedan para la siguiente sesión exacta.
- No bajar el modo estricto del interceptor SDK: es contrato de telemetría congelado.

## Evidencia

- CampaignRef `592944e2-1a30-426c-93c6-ebba351dc786`; CampaignIntentToken `efd7b357-3ce8-4e03-ade8-68b8bdce6253`; WorkflowID `sqx-forge-campaign-v1-efd7b357-…`; RunID `01a069f8-228a-79ff-9ce5-208794cd3946`; base ConfigID `a68c8f76-49cf-4b2e-8973-6d5ad127fc93`.
- Decisión de sesión: [[2026-09-04-echo-forge-c3-lean-recert-blocked]].

## Resolución verificada del source fix

- Los tests focales y de race atravesaron el interceptor SDK real con los cinco requests; los JSON históricos round-tripean sin `Telemetry`.
- Replay read-only físico de la Campaign bloqueada: 5 eventos, PASS, sin `TMPRL1100` ni nondeterminism. Replay control Generic: 470 eventos, PASS, sin nondeterminism.
- La separación de autoridad queda explícita: el workflow no gatea por `WorkflowExecution.ID` runtime; dispatcher y persistence siguen exigiendo el ID canónico token-derived.
- `CAMPAIGN_PARTIAL_PIPELINE_REUSE` permanece `CAPABILITY GAP / OPTIONAL`; `MT5_COMPILE_RETRY_POLICY_AUTHORITY_DRIFT` permanece `OPEN / NON-BLOCKING`.
