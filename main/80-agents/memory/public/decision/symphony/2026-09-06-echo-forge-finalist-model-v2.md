---
type: decision
schema_version: 1
scope: project
created: "2026-09-06"
updated: "2026-09-06"
area: "[[Echo Forge]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[xKoRx/symphony]]"
entities:
  - "[[Echo Forge]]"
related:
  - "[[2026-08-30-echo-forge-finalist-promotion-v1]]"
  - "[[2026-08-30-finalist-promotion-v1-core]]"
  - "[[2026-08-31-forge-campaign-stop-policy-v1-contract]]"
  - "[[2026-09-04-echo-forge-campaign-replenishment-resume-policy-v1]]"
  - "[[2026-09-02-echo-forge-c3-mt5-fidelity-period-mismatch]]"
  - "[[2026-08-18-echo-forge-mt5-fidelity-scope-bypass]]"
  - "[[2026-09-06-echo-forge-mt5-execution-model-v2]]"
aliases:
  - ECHO_FORGE_FINALIST_MODEL_V2
  - finalist eligibility V2
  - fidelity warnings V2
confidence: verified
source_session: ECHO-FORGE-FINALIST-ELIGIBILITY-AND-FIDELITY-WARNINGS-V2-TOP
load_policy: when_project_loaded
indexable: true
index_priority: high
tags:
  - kind/decision
  - scope/project
  - project/echo-forge
---

# 2026-09-06-echo-forge-finalist-model-v2

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Contexto

- Baseline `xKoRx/symphony@3b0737c1efe153f1f72eec40465fd1aa883887d0` == HEAD == origin/master. SDK `c85594440f6755443ceb97ec4e333cd0ddb5b0ed`. Release `0.2.96`. TOP read-only.
- Finalist Factory V1 está PRODUCT READY y ranking-bound: `ScoreComputed` → ranking eligible → `TopProjection.Entries` → `FINALIST_PROMOTION`. `ScoreNotComparable` / `ScoreInvalidInput` salen del ranking y no entran a Promotion.
- Evidence C3/M6: periodos SQX `2016-01-04→2026-06-05` vs MT5 `2026-07-01→2026-07-31` producen `NOT_COMPARABLE` (`period_*_mismatch`) y Promotion vacía con `TOP_PROJECTION_EMPTY` pese a ejecución física válida.
- Owner freeze: SQX y MT5 pueden tener ventanas independientes. Fidelidad es sombra analítica. Ranking ordena. `top_n` proyecta. Warnings no borran finalistas. Corrupción estructural no es warning.

## Decisión

- PROJECT DECISION FROZEN `ECHO_FORGE_FINALIST_MODEL_V2`.
- `FINALIST_MEMBERSHIP` = StrategyRefs únicos que completan el boundary estructural post-reconcile: MT5 backtest `ArtifactStatusSuccess` + parser HTM + normalización + persist reconcile con `NativeMetricSetRef` + lineage StrategyRef/EX5 + identidad ejecutada igual al `WorkflowSpec` pedido en instrument y timeframe.
- `FIDELITY` = evidencia analítica opcional (`mt5_fidelity_shadow.v1`) adjunta al finalista. No admite ni rechaza.
- `RANKING` = ordenamiento/proyección sobre el subconjunto con score numérico `COMPUTED`. No define membresía.
- `TOP_N` = slice de display/recomendación. No es cap de finalistas. V1 exigía `ranking.top_n` para poder configurar Promotion; V2 no puede conservar ese acoplamiento de membresía.
- `WARNINGS` = diagnósticos tipados, deterministas, no destructivos, bound a `StrategyRef` + evidencia Score/comparability.
- Period mismatch: `fidelity_status=NOT_COMPARABLE` + warning `PERIOD_MISMATCH` + sin rank numérico + sigue finalista.
- Instrument/timeframe mismatch vs requested: gate estructural fail-closed en reconcile. No warning. No finalista.
- `finalist_promotion@1.0.0` / `sqx-finalist-promotion-output.v1` / `forge-result.v1` permanecen históricos y legibles. Flujos nuevos usan `finalist_promotion@2.0.0` + output v2 + result v2. Campaign cuenta unique `StrategyRef` del Decision output; `first_rank`/`first_score_ref` pasan a opcionales para campañas nuevas.
- V1 queda `SUPERSEDED FOR NEW FLOWS`. No se reescriben Decisions históricas.

## Rationale

- `RankingSnapshot.Candidates` ya guarda el cohort completo con status; `OrderedEntries`/`TopProjection` son el corte comparable. El defecto V1 es que Promotion materializa exactamente `TopProjection.Entries`.
- Score shadow ya declara que `NOT_COMPARABLE` no muta lifecycle; Promotion V1 contradice esa frontera.
- Campaign Stop Policy ya cuenta unique finalists desde `FINALIST_PROMOTION`. Si V2 cambia el output, `target_finalists` y CONTINUE se corrigen sin reabrir Stop Policy.
- `FIDELITY_SCORE_LOW` y umbrales de desviación de trades/PnL no se inventan. `PNL_SIGN_FLIP` sí es un hecho binario cuando ambos `net_profit` son finitos.

## Consecuencias

- Implementación: un NORMAL cohesivo de membresía/Promotion/result + un NORMAL de Campaign BWC/nullable rank, convergentes con MT5 Slot V2 antes de un solo release. Hard max 14 archivos productivos por slice.
- Gate de identidad requested vs HTM debe existir antes de promover todos los Candidates; si no, `instrument_mismatch` actual (hoy `NOT_COMPARABLE`) se convertiría en finalista.
- Reconcile/score error hoy aborta el Generic entero; backtest child failure sí dropea el candidato. Case D de certificación debe distinguir ambos o cambiar el workflow a drop per-candidate en reconcile.
- Result Surface V1 `crossCheckPromotion` (`sqx/core/forge/result.go`) exige `Finalists ≡ TopProjection` (mismo Ref, `top_n`, cardinalidad y cada entry). Ese check es un gate oculto: si V2 promociona el cohort estructural y deja `top_n` como proyección, el check V1 marcaría `INCONSISTENT_RESULT`. V2 lo supersede: binding de snapshot sigue; igualdad membresía↔proyección no.
- NEXT EXACT: `ECHO-FORGE-TRADELIST-BASELINE-DURABILITY-PREFLIGHT`.

## Alternativas descartadas

- Promover ciegamente todos los `ScoreNotComparable` sin reclasificar instrument/timeframe/strategy_ref.
- Rank=0 / ScoreRef dummy para no comparables.
- Mutar `ranking-snapshot.v1` para que `Eligible=true` en NOT_COMPARABLE.
- Reescribir Decisions V1 o Campaigns históricas.
- Introducir DecisionPolicy de umbral de fidelidad.
- Copiar periodos SQX a MT5 para forzar `COMPUTED`.
- Reemplazar Decision durable por latest query / folder scan.
