---
type: decision
schema_version: 1
scope: project
created: "2026-09-04"
updated: "2026-09-04"
area: "[[Echo]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[xKoRx/symphony]]"
entities:
  - "[[Echo Forge]]"
related:
  - "[[2026-08-31-forge-campaign-stop-policy-v1-contract]]"
  - "[[2026-09-04-echo-forge-c3-zero-supply-closure]]"
  - "[[2026-09-04-release-0-2-92-physical-c3-closure]]"
  - "[[2026-09-04-echo-forge-campaign-builder-supply-identity]]"
aliases:
  - CAMPAIGN REPLENISHMENT RESUME POLICY V1
  - Builder Budget V1
confidence: verified
source_session: "ECHO-FORGE-CAMPAIGN-REPLENISHMENT-RESUME-POLICY-V1-TOP"
load_policy: when_project_loaded
indexable: true
index_priority: high
tags:
  - kind/decision
  - scope/project
  - project/echo-forge
---

# 2026-09-04-echo-forge-campaign-replenishment-resume-policy-v1

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Contexto

- Baseline read-only: symphony `93c66651251edefcc65ef183ac9f7b832b4de5de` == HEAD == origin/master; SDK `c85594440f6755443ceb97ec4e333cd0ddb5b0ed`; release `0.2.92`; C3 `PASS / CLOSED`; Stop Policy V1 `PHYSICALLY_CERTIFIED / FROZEN`; zero-supply `PHYSICALLY_CERTIFIED / CLOSED`.
- Campaign ya puede CONTINUE y lanzar `GenericSQXWorkflow` wave N+1, pero el child nace con `Input` vacío, execution Wave nueva `forge-<CampaignRef>-wNNNNNN`, y `ConfigSourceWave=base.Wave` sólo para leer `.cfx`.
- `pool_max` / `target_tops` viven en `WaveConfig`, se validan al intake y **no se aplican** en `GenericSQXWorkflow`; son legado Adaptive. El tope físico de Builder hoy es SQX/`MaxStrategies` en CFX, no Go.
- Reuse histórico certificado (`FEAT-SQX-CROSS-FLOWRUN-REUSE`) indexa ownership por execution Wave actual; Campaign children no apuntan al namespace de la wave anterior.
- Graphify de symphony stale (graph.json 2026-09-03 17:39); no se reparó.

## Decisión

- Replenishment V1 es **NEW_BUILDER_SUPPLY bounded**. Cada `CONTINUE` crea una wave totalmente nueva desde Builder, con budget explícito por wave, StrategyRefs nuevas, y `max_waves` como único hard stop de Campaign además de `TARGET_REACHED`.
- Builder Budget V1 es **subcapability integrada**, no track separado: `forge_campaign.max_builder_candidates_per_wave` (obligatorio, ≥1). Techo de Campaign = ese valor × `max_waves`. No hay `max_builder_candidates_per_campaign` ni stop reason `BUDGET_EXHAUSTED` en V1.
- Stop Policy V1 **no se reabre**: precedencia `TARGET_REACHED > MAX_WAVES_REACHED > CONTINUE`. Budget exhaustion no es terminal reason; si el operator quiere menos supply total, baja `max_waves` o el per-wave cap.
- `CAMPAIGN_PARTIAL_PIPELINE_REUSE` queda **POST_V1**. V1 no selecciona `source_flow_run` / `source_wave` / `resume_from_stage` / reuse refs. Leftover de early ranking (`top_n` < outputs de Builder) queda stranded a propósito; el operator dimensiona `early_rankings.top_n` vs budget.
- **CHALLENGE autorizado (material), AMENDED:** el defecto (stem sin generation-batch → CONTINUE = REPROCESSED) permanece REQUIRED. El mint `wNNNNNN_` execution Wave queda **REJECT**. Autoridad de mint: [[2026-09-04-echo-forge-campaign-builder-supply-identity]] (`BuilderSupplyBatchRef`).
- No Decision nueva: no hay `REPLENISHMENT_PLAN`. Autoridad = StopEvaluation + `ForgeCampaignWave` + child FlowRun + membership `PRODUCED`. Remaining target es informativo, no dimensiona Builder (no 1 generated → 1 finalist).
- Owner: `ForgeCampaignWorkflow` / `ResolveWave` (qué child nace). Trigger: tras `FinalizeWave` con outcome `CONTINUE`, al resolver wave N+1. Enforcement del cap: post-Builder en el child, fail-closed si PRODUCED count > cap.
- Retry/reprocess/reuse/regenerate: V1 usa RETRY (StageExecution existente, frozen) y REGENERATE (Builder nuevo). REPROCESS y REUSE explícitos de Campaign = POST_V1. Reuse automático same-flow/technical recovery permanece intacto.
- Exclusion V1: Campaign dedupe sigue `StrategyRef` first-observation-wins. Canonical mint por `BuilderSupplyBatchRef` evita colisión intra-campaign. Dedupe extra por contenido, quotas de diversidad y exclusion set de rejected = POST_V1. Rejected bajo el mismo snapshot no se reingresa como supply nuevo porque las identidades de generation N no se reusan.
- Wave N+1 = fresh generation iteration. Wave identity frozen `forge-<CampaignRef>-wNNNNNN`.
- Product Ready de fábrica queryable: **SÍ, con gaps explícitos** (leftover drain, historical Campaign selector, Echo ingest, A0 live validation).

## Rationale

- Snapshot de Campaign es inmutable; CONTINUE bajo la misma config no puede “arreglar” rejects reejecutando WFM/MT5 sobre las mismas StrategyRefs.
- Historical resolver no ve la wave anterior porque el namespace incluye execution Wave; wiring automático existente no drena inventory.
- `pool_max` no es Builder Budget. Declarar “usar pool_max” sería insuficiente y falso.
- Extender Stop Policy con `BUDGET_EXHAUSTED` mezclaría un cap de supply con terminalidad de Campaign; V1 mantiene un solo bound de olas.
- Prefix de execution Wave en canonical_id queda REJECT; el mint namespaced es `BuilderSupplyBatchRef`, no WaveKey. Ver [[2026-09-04-echo-forge-campaign-builder-supply-identity]].

## Consecuencias

- NEXT EXACT: `ECHO-FORGE-CAMPAIGN-REPLENISHMENT-RESUME-POLICY-V1-NORMAL`.
- Schema: `ForgeCampaignSpec.max_builder_candidates_per_wave` + persistencia `ReplenishmentPolicy` guard (no identidad) junto a StopPolicy; `DisallowUnknownFields` se mantiene.
- Child contract: Spec materializado (Wave/WaveKey/RequestID nuevos, `ConfigSourceWave=base.Wave`, `ForgeCampaign=nil`) + `Input` vacío + cap inyectado de autoridad Campaign + Builder canonical mint por `BuilderSupplyBatchRef` (no WaveKey).
- Tests R1–R14: R9 se interpreta como `MAX_WAVES_REACHED` con cap por wave (no tercera reason). R5 es test negativo: wave 2 no lee namespace `w000001`. R6 es immutability/conflict intra-campaign; invalidation cross-campaign queda documentada POST_V1. R11/R2b/R2c de mint: [[2026-09-04-echo-forge-campaign-builder-supply-identity]].
- File budget: un NORMAL cohesivo, ≤14 files; si Builder mint+enforcement desborda, split técnico Campaign contract vs Builder adopt — no split Budget vs Replenishment.

## Alternativas descartadas

- Resume/reuse-aware V1 / leftover drain: correcto para TIME_TO_QUERYABLE_FINALISTS a largo plazo, pero es `CAMPAIGN_PARTIAL_PIPELINE_REUSE` (source_wave + skip Builder + cohort histórico). Complejidad material; no bloquea autonomía si el cap y el mint por `BuilderSupplyBatchRef` existen.
- Mapear budget exhaustion a `MAX_WAVES_REACHED` mintiendo `waves_started`.
- Reusar `WaveConfig.PoolMax`/`TargetTops` como budget de Campaign.
- Decision `REPLENISHMENT_PLAN` sin autoridad de negocio adicional.
- Reabrir Stop Policy, Identity v2, ranking, WFM, Promotion o zero-supply.
- Relación lineal remaining_target → generation_budget.
