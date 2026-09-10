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
  - "[[2026-09-04-mt5-terminal-build-unsupported]]"
  - "[[2026-09-04-echo-forge-mt5-report-6140-compatible-allowlist]]"
  - "[[2026-09-04-reretester-single-artifact-contract]]"
  - "[[2026-09-03-echo-forge-c3-lean-recert-plan]]"
  - "[[2026-08-31-forge-campaign-stop-policy-v1-contract]]"
aliases:
  - C3 LEAN 0.2.90 BLOCKED MT5 BUILD
  - ECHO-FORGE-RELEASE-0.2.90-AND-C3-LEAN-RECERT-NORMAL
confidence: verified
source_session: ECHO-FORGE-RELEASE-0.2.90-AND-C3-LEAN-RECERT-NORMAL
load_policy: when_project_loaded
indexable: true
index_priority: high
tags:
  - kind/decision
  - scope/project
  - project/echo-forge
---

# 2026-09-04-echo-forge-c3-lean-0290-blocked-mt5-build

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Contexto

- Misión `ECHO-FORGE-RELEASE-0.2.90-AND-C3-LEAN-RECERT-NORMAL` sobre baseline/source `32d0740ccb0fe6ee04e016eef874790bc8684efc` == HEAD == origin/master, SDK `c85594440f6755443ceb97ec4e333cd0ddb5b0ed` (HEAD == origin/master en `~/go/src/github.com/xKoRx/sdk`), `input/example/config.json` conservó SHA `2204bf0f…` y dirty foráneo intacto. GATES 0–4 PASS: release-only 0.2.90 publicada y confirmada por MinIO (manifest sha256 artefactos linux `207a5001…`, windows `23ecba36…`, `vcs.revision=32d0740`, SDK pin embebido); flota 4/4 rotó al 0.2.90 con un worker por máquina (zeus `2335182`, hera `966707`, kron-linux `972535`, worker-kronos `15852`); las 4 CFX efímeras reutilizadas byte-iguales a la tanda validada en 0.2.89 (`ParseCFXConfiguredPeriod` = `2026-05-04→2026-06-05`, patch sólo en Setup primaria, fixtures canónicos sin tocar).
- CERT-A identidad completamente nueva: request `forge-c3-lean-a-0290-20260904T052719Z-8d8af44a`, wave base `c3-lean-a-0290-20260904T052719Z-8d8af44a`, CampaignRef `baeb747d-1cb9-4cbc-8903-58d91f64c720`, token `a3d81aa3-ce67-4b78-adb7-f61d41cfbf97`, parent `sqx-forge-campaign-v1-a3d81aa3-…` RunID `01a06ae3-2ab3-701f-b9e4-a1f0e5081647`, child Generic FlowRun `67d81075-ef71-4f40-82cb-10dd2201fd9a`, Execution Wave exacta `forge-baeb747d-1cb9-4cbc-8903-58d91f64c720-w000001`, RequestID exacta `forge-campaign-baeb747d-…-wave-000001`. `config_source_wave` ABSENT; `ValidateWorkflowSpec` OK; `forge_campaign{1,1}`.

## Decisión

- **VEREDICTO: `ECHO_FORGE_CAMPAIGN_STOP_POLICY_V1_C3: BLOCKED / CLOSED`** (no certificada). CERT-A NO alcanza strong PASS por un defecto bloqueante nuevo, no atribuible al fix 0.2.90: `MT5_TERMINAL_BUILD_UNSUPPORTED` — `mt5_reconcile_v1` falla cerrado con `mt5 report: build not supported: build=6140` (`contract_error`, non-retryable) tras un backtest físicamente exitoso. DEFECT RULE aplicado: evidencia preservada, sin patch, sin release, retorno al lead.
- **Fix Final Reretester validado en su tramo producido:** el pipeline 0.2.90 atravesó `project@sqx-final-reretester.v1` COMPLETED (subject `75ed071a…`, 1 input → 1 producido) y continuó downstream (trade list → MQ5/EX5 → MT5 backtest) sin la violación de cardinalidad de 0.2.89. El branch `CompleteEmpty` no se ejercitó físicamente (no surgió un output vacío legítimo); su garantía sigue siendo la unitaria `TestFinalReretesterFanoutRejectsPartialAndInvalidOutputs` invertida en `32d0740`.
- CERT-B, dedupe entre waves y replay matrix NO EJECUTADOS por hard gate de misión. Exact redelivery de CERT-A terminal PASS (idempotencia): re-entrega byte-exacta a las 05:44:40Z convergió sin `forge campaign created` al mismo CampaignRef/token/RunID, 0 filas nuevas (waves=1, finalists=0, stop_evaluations=0), 0 workflows nuevos; verified read `LoadForgeCampaignResult` PASS y coincide exacto con durable (`FAILED`, `WAVE_FLOW_RUN_FAILED`, `waves_started=1`, `waves_completed=0`, `effective_unique_finalists=0`).
- Topología demostrada en history del parent: exactamente un `StartChildWorkflowExecutionInitiated` → `GenericSQXWorkflow` con `ParentClosePolicy=RequestCancel`; los Group subflows son descendientes del Generic. MT5 physical safety: 1 job local, worker vivo, `terminal64=0`/`metatester64=0` tras el fallo, 1 MT5 child por Generic (≤4).

## Rationale

- El score `mt5_fidelity_shadow.v1` exige métricas `MT5_NATIVE` de un reporte reconciliado; con el parser congelado (`SupportedBuild = 6090`, SPEC-PARSER §4) y el terminal físico auto-actualizado a build `6140` (mtime 2026-09-02 19:18 local), ningún backtest completado puede reconciliarse ⇒ ningún promoted finalist con score `COMPUTED` ⇒ CERT-A no puede llegar a `TARGET_REACHED` en esta flota. El smoke 0.2.88 no detectó el drift porque cancela el backtest y nunca reconcilia un reporte de éxito.
- El defecto no es regresión de 0.2.90 ni del fix `32d0740`: es colisión entre drift ambiental y contrato congelado fail-closed. Continuar, degradar el terminal o ampliar `SupportedBuild` son decisiones del lead (requieren nuevo ciclo TOP→NORMAL), no operaciones de certificación.

## Consecuencias

- Release 0.2.90 queda publicada, inmutable y operativa; la flota 4/4 permanece en 0.2.90. C3 sigue NO certificada; `ECHO_FORGE_CAMPAIGN_STOP_POLICY_V1` NO se congela físicamente. Se preservan `CAMPAIGN_PARTIAL_PIPELINE_REUSE` (CAPABILITY GAP/OPTIONAL) y `MT5_COMPILE_RETRY_POLICY_AUTHORITY_DRIFT` (OPEN/NON-BLOCKING).
- Identidades consumidas en esta sesión: CERT-A `baeb747d…`/token `a3d81aa3…`/request `forge-c3-lean-a-0290-20260904T052719Z-8d8af44a` (terminal FAILED, no reutilizar). Las históricas `11741c54…` y `592944e2…` permanecen terminal FAILED como evidencia.
- Camino de desbloqueo (cerrado por RCA TOP posterior [[2026-09-04-echo-forge-mt5-report-6140-compatible-allowlist]], no en esta sesión de certificación): allow-list explícita `{6090, 6140}` en `mt5-report.v1` + fixture 6140 + tests; no pin del terminal. NEXT EXACT: `ECHO-FORGE-MT5-REPORT-CERTIFIED-BUILD-ALLOWLIST-6140-FIX-NORMAL`. Recert C3 con identidad CERT-A/B nueva; no reutilizar `baeb747d…`. C3 permanece `BLOCKED / CLOSED`.

## Alternativas descartadas

- Repetir CERT-A con otra identidad: el fallo es determinista del ambiente MT5; sólo contaminaría.
- Downgradear el terminal o editar `SupportedBuild` durante la sesión: prohibido por DEFECT RULE / NO SOURCE CHANGES.
- Iniciar CERT-B o saltar MT5 con config alterada: falsearía la superficie productiva de Promotion.
