---
type: decision
schema_version: 1
scope: project
created: "2026-08-30"
updated: "2026-08-30"
area: "[[Echo Forge]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[xKoRx/symphony]]"
entities:
  - "[[Echo Forge]]"
  - "[[AGENTS OS]]"
related:
  - "[[2026-08-30-durable-project-stages-recovery-physical-recertification]]"
  - "[[2026-08-30-durable-artifact-verified-reads-final-e2e-rerun]]"
  - "[[Echo - Auditoria POC e Identidad Forge-Echo 2026-08-23]]"
aliases:
  - ECHO-FORGE-POST-FOUNDATION-PRODUCT-RESUME-TOP
  - product resume post foundation V1
confidence: verified
source_session: ECHO-FORGE-POST-FOUNDATION-PRODUCT-RESUME-TOP
load_policy: manual
indexable: true
index_priority: high
tags:
  - kind/decision
  - scope/project
  - project/echo-forge
---

# 2026-08-30-echo-forge-post-foundation-product-resume

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Contexto

- Recconstrucción de producto READ-ONLY sobre `xKoRx/symphony` @ `6b13c66cf195a83709c156e25aa8dfd6a17c140e` (`HEAD == origin/master`, release física `0.2.82`, golden `812ec6ce`). Foundation V1 CERTIFIED_CLOSED / FROZEN. Pregunta: ¿Echo Forge puede entregar TOP finales de forma autónoma, o sólo ejecuta un pipeline?

## Decisión

- **PIPELINE EXECUTES ≠ PRODUCT IS AUTONOMOUS.** GenericSQXWorkflow ejecuta Builder → Classification → Early Ranking per-type → Retester/Optimizer children → WFM → Robust Selection → Apply → FinalReretester → TradeSet → MT5 → Score shadow → Global RankingSnapshot. Eso está certificado en 0.2.82. No existe fábrica autónoma ni superficie de entrega.
- **Roadmap congelado (DAG, 4 tracks):** (1) `ECHO-FORGE-RESULT-SURFACE-V1-NORMAL` — query/CLI de FlowRun status + RankingSnapshot `top_projection` + StrategyRefs + artifacts + exclusions. (2) `ECHO-FORGE-FINALIST-PROMOTION-V1-NORMAL` — Decision durable distinta de ranking (`PROMOTE`), no reabrir `OPTIMIZER_SELECTION`. (3) `ECHO-FORGE-CAMPAIGN-STOP-POLICY-V1-NORMAL` — loop de waves sobre Generic durable hasta stop policy (`target_tops` / max waves); no revivir AdaptiveTypeWorkflow. (4) `ECHO-FORGE-BUILDER-BUDGET-V1-NORMAL` — honrar presupuesto/target de generación; `pool_max` hoy es dead en Generic.
- **NEXT EXACT: `ECHO-FORGE-RESULT-SURFACE-V1-NORMAL`.** Modelo NORMAL. No reabrir foundation, ranking algorithm, WFM robust policy, Artifact Plane, Strategy Identity, ni M7.
- **CampaignEngine etcd** es ProActiva machine-id, no campaña de producto.
- **Global RankingSnapshot existe** (`rank_snapshot_v1`, Mongo `ranking_snapshots`, `score_descending.v1`, `top_n=5`) y **no es promoción**. Score = `mt5_fidelity_shadow.v1` (fidelidad de copia SQX↔MT5, no calidad de estrategia). 0.2.80 observó `SCORE_NOT_COMPARABLE`; 0.2.82 usó el mismo algoritmo; lab inalcanzable esta sesión ⇒ `top_projection.effective` no reconsultado. Superficie debe exponer exclusiones, no asumir TOP 5 de calidad.

## Rationale

- El golden 0.2.82 ya produce el objeto durable de ranking y 4 estrategias aplicadas (`41d4320e`, `945f4023`, `c9a9ea7f`, `b640302d`). El humano todavía reconstruye el resultado vía Temporal/SQL/Mongo/MinIO. Sin superficie, campaña y Builder budget no se pueden operar. Adaptive `TargetTops`/`PoolMax` está deprecado y sin activities.

## Consecuencias

- Foundation permanece CLOSED. M7 / Echo ingest / MT5 publish siguen bloqueados por contrato Echo, no por este resume.
- Product Ready V1: campaña C + target T → waves autónomas hasta stop policy → N finalistas promovidos con ranking/evidencia/artifacts queryables, sin SQL spelunking.
- North star: `TIME_TO_QUERYABLE_FINALISTS` (intake → objeto queryable de StrategyRefs+exclusions+artifacts).

## Alternativas descartadas

- Implementar ranking nuevo: el pipeline ya rankea; el gap es delivery + policy de qué significa TOP, no otro algoritmo.
- Revivir AdaptiveTypeWorkflow: prototipo mock-first, activities no registradas, no durable.
- Campaign automation como primer track: no se puede gobernar una fábrica si una wave no se puede leer.
- Reabrir M5/M7 por `SCORE_NOT_COMPARABLE`: status de dominio congelado; la superficie lo reporta. Un Score de calidad de estrategia es track posterior, no corrección de foundation.
