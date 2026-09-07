---
type: decision
schema_version: 1
scope: project
created: "2026-09-04"
updated: "2026-09-04"
area: "[[Echo]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[xKoRx/symphony]]"
entities: []
related:
  - "[[2026-09-03-echo-forge-c3-lean-recert-plan]]"
  - "[[2026-09-04-forge-campaign-orchestration-contract-broken]]"
  - "[[2026-08-31-forge-campaign-stop-policy-v1-contract]]"
aliases:
  - C3 LEAN RECERT BLOCKED
  - TelemetryCarrier campaign start defect
confidence: verified
source_session: ECHO-FORGE-C3-LEAN-RECERT-NORMAL
load_policy: when_relevant
indexable: true
index_priority: high
tags:
  - kind/decision
  - scope/project
  - project/echo-forge
---

# 2026-09-04-echo-forge-c3-lean-recert-blocked

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Contexto

- Misión `ECHO-FORGE-C3-LEAN-RECERT-NORMAL` sobre source authority `7047a9c112502dcb68387745149eed95405b0aae` == HEAD == origin/master, SDK `c85594440f6755443ceb97ec4e333cd0ddb5b0ed`, release física 0.2.88. Preflight PASS: flota 4/4 (zeus 2306392, hera 944368, kron-linux 951302, worker-kronos 20040 con SHA == manifest), StagerRuntime Running PID 38460, terminal64=0, metatester64=0, Temporal sin workflows Running, PG OK.
- CFX authority PASS: los cuatro `input/example/*.cfx` son byte-idénticos (SHA256) a los artefactos operacionales del FlowRun smoke 0.2.88 en MinIO `wave_mt5-cancel-smoke-0.2.88-20260903T221548Z/xauusd/l_h1/example_flow_23/v1/00_configs/`.
- CFX period patch PASS: única Setup primaria `Settings/Data/Setups/Setup` con `dateFrom=2016.01.04 dateTo=2026.06.05` por CFX (las de `CrossChecks/RetestOnAdditionalMarkets` no son primarias); patch puntual `dateFrom→2026.05.04` (diff proof byte-inverso); el parser congelado `runtime.ParseCFXConfiguredPeriod` lee `2026-05-04→2026-06-05` en los 4 CFX parchados (provenance `sqx_cfx_setup.v1`).
- CERT-A efímera (`forge-c3-lean-a-20260904T010631Z-af6508ce`, wave `c3-lean-a-…`, strategy `90260501`, top_n=1/1, min_pass_cells=1, MT5 2026.05.04→2026.06.05 timeout 10m, `forge_campaign{1,1}`, sin `config_source_wave`) VALIDADA por `ValidateWorkflowSpec` y entregada por intake canónica `input/` a las 2026-09-04T01:11:02Z.

## Decisión

- **VERDICT: `ECHO_FORGE_CAMPAIGN_STOP_POLICY_V1_C3: BLOCKED / CLOSED`** (física NO certificada). La certificación se detiene en el arranque de la wave 1 por un defecto de contrato en source congelado.
- Defecto 1 (bloqueante): `forge_campaign_start` (y las 5 actividades de orquestación: start/resolve_wave/finalize_wave/cancel/fail_contract) falla determinísticamente con `activity argument does not implement TelemetryCarrier` — el interceptor estricto del SDK (`xKoRx/sdk pkg/shared/temporal/interceptor.go:122`) exige `TelemetryCarrier` en el argumento y `ForgeCampaignStartRequest` et al (`sqx/activities/worker/forge_campaign_activity.go:26-66`) no lo implementan (compárese `FlowRunStartRequest` que sí, `flow_run_lifecycle_activity.go:55-58`). Evidencia server-authoritative: `DescribeWorkflowExecution` pending activity attempt 54→∞ con `lastFailure=activity argument does not implement TelemetryCarrier`; retry policy `MaximumAttempts:0` (infinito) ⇒ campaña sin progreso y sin fin propio.
- CERT-B NO INICIADA por hard gate de misión (defecto idéntico garantizado; evitar segunda campaña colgada).
- Defecto 2 (no bloqueante para start, bloqueante para gate REPLAY): `ForgeCampaignWorkflow` no es replayable — aserta `info.WorkflowExecution.ID != expectedID` (`sqx/workflows/forge_campaign_workflow.go:43`) y el replayer del SDK corre con WorkflowID fijo `ReplayId` (`internal_worker.go:1905`, sin opción de override) ⇒ early-return y panic `TMPRL1100` en el evento 5. Control del harness: el padre del cancel smoke (470 eventos) REPLAY PASS con la misma herramienta ⇒ el fallo es del workflow, no del harness.
- Redelivery/idempotencia PASS: re-entrega exacta de CERT-A a las 01:28:25Z convergió al MISMO CampaignRef `592944e2-1a30-426c-93c6-ebba351dc786`, mismo CampaignIntentToken `efd7b357-3ce8-4e03-ade8-68b8bdce6253`, mismo RunID `01a069f8-…` (`ConvergeAlreadyStarted` + `loadForgeCampaignByRecovery`); 1 fila en `sqx.forge_campaigns`, 0 waves/stop_evaluations/finalists/FlowRuns, 1 workflow Temporal. Caveat: verificado con campaña no terminal (la terminalidad es inalcanzable por el defecto 1).
- Verified read PASS: `LoadForgeCampaignResult(592944e2-…)` (ControlPlane PG) devolvió resultado digest-verificado bien formado: `status=PENDING, target_finalists=1, max_waves=1, waves=[], finalists=[]`.
- Residual físico preservado: campaña CERT-A RUNNING en Temporal / PENDING en PG en reintento infinito (reintento 30s, costo despreciable, cero MT5). Terminate prohibido por misión; CancelWorkflow formal quedará igualmente colgado porque `ForgeCampaignCancelRequest` comparte el defecto 1. Decisión de desenrollado queda al lead.

## Rationale

- La misión prohíbe source patch en la misma sesión y exige promotion nonempty de CERT-A antes de CERT-B; con `forge_campaign_start` roto ningún gate posterior (topología, promotion, stop TARGET_REACHED, ConfigSourceWave, dedupe entre waves) es alcanzable.
- El bound físico se respetó: 0 backtests MT5, 0 FlowRuns nuevos, 0 cambios en flota; la pared de costo del fanout nunca se activó.

## Consecuencias

- C3 sigue NO certificada; `CAMPAIGN_STOP_POLICY_V1` no se marca físicamente certificada. `CAMPAIGN_PARTIAL_PIPELINE_REUSE` sigue CAPABILITY GAP/OPTIONAL. `MT5_COMPILE_RETRY_POLICY_AUTHORITY_DRIFT` sigue OPEN/NON-BLOCKING.
- Fix requerido (fuera de esta sesión): implementar `GetTelemetry()` en los 5 request types de campaña (o carrier común) con assertions `var _ sdktemporal.TelemetryCarrier`, y hacer replay-friendly el `ForgeCampaignWorkflow` (quitar/relajar la aserción de WorkflowID o tracer de replayer). Luego reintentar `ECHO-FORGE-C3-LEAN-RECERT-NORMAL` con workspace efímero nuevo.
- NEXT EXACT: `RETURN_TO_LEAD_AFTER_C3_BLOCKED` — decidir fix + desenrollado de la campaña residual antes de reintentar.

## Alternativas descartadas

- Iniciar CERT-B igual: crearía una segunda campaña colgada idéntica; prohibido por hard gate.
- CancelWorkflow formal de CERT-A: el camino de cancelación usa el mismo request sin carrier ⇒ colgaría en CancelRequested; no autorizado por la misión para esta clase de fallo.
- Reiniciar con otro request_id: mismo defecto determinista; sólo contaminaría.
