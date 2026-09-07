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
related:
  - "[[2026-08-30-echo-forge-post-foundation-product-resume]]"
  - "[[2026-08-30-echo-forge-result-surface-session-feedback]]"
aliases:
  - ECHO-FORGE-FINALIST-PROMOTION-V1-TOP
  - finalist promotion v1 contract
confidence: verified
source_session: ECHO-FORGE-FINALIST-PROMOTION-V1-TOP
load_policy: when_project_loaded
indexable: true
index_priority: high
tags:
  - kind/decision
  - scope/project
  - project/echo-forge
---

# 2026-08-30-echo-forge-finalist-promotion-v1

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Contexto

- Sesión TOP READ ONLY sobre `xKoRx/symphony` @ `067481859ee81d494642450c5691ce291d2c3b4a` (`HEAD == origin/master`). Foundation V1 y Result Surface V1 CERTIFIED_CLOSED. Golden `812ec6ce` tiene ranking AVAILABLE con `requested_top_n=5` / `effective_top_n=0` y `promotion.status=NOT_IMPLEMENTED`.
- El aggregate `Decision` y `sqx.decisions` (migration 004) están rígidamente atados a `OPTIMIZER_SELECTION` / `SubjectRef → strategies` / evidence `EVALUATION|METRIC_SET` / outcomes `SELECTED|REJECTED`. No basta agregar la constante `FINALIST_PROMOTION`.
- RankingSnapshot.TopProjection ya es el corte autoritativo (`entries` = prefijo exacto de elegibles, truncado a `min(requested, len(ordered))`). Ranking no es StageExecution. `select_robust_run` ya completa StageExecution con EvaluationRefs vacíos y persiste Decision.

## Decisión

- Promotion V1 es **una Decision de cohorte** por FlowRun (`FINALIST_PROMOTION`), subject `FLOW` = FlowRunRef, no N Decisions por Strategy, no aggregate Finalist, no clone de Strategy.
- Empty promotion = **una fila durable** `outcome=COMPLETED` + `reason=TOP_PROJECTION_EMPTY` + `finalists=[]` + `effective_promoted_count=0`. Cero filas queda reservado para nunca ejecutó / pendiente / falló.
- Input authority = **RankingSnapshotRef exacto** (binding del workflow + `LoadRankingSnapshot`). Evidence kind nuevo `RANKING_SNAPSHOT` role `source_ranking_snapshot`. Prohibido ranking name only / latest / Mongo newest / MinIO / ordered_entries fallback.
- Regla V1: promover **exactamente** `TopProjection.Entries`. Exige `TopProjection.Configured=true` (el ranking fuente debe tener `top_n`). `effective=0` con `requested>0` es éxito con cero finalistas.
- Policy: `finalist_promotion@1.0.0`, config `{schema, source_ranking, mode: TOP_PROJECTION}`. Sin `target_n` propio. `source_ranking` es obligatorio y debe coincidir con exactamente un `rankings[].name`.
- StageExecution: `promote_finalists@sqx-finalist-promotion.v1`, subject FLOW, CanonicalInputs `[]`, generation=1, TaskPath sintético `StructuralTaskPath(len(spec.Tasks))` (Promotion no puede ser TaskSpec: el loop de tasks corre **antes** de `runGlobalRankingSnapshots`). CompleteEmpty. Sin Evaluation artificial.
- Placement: Score → Global Ranking → **Promotion** → seal FlowRun. Configurado y falla ⇒ FlowRun FAILED. Éxito con N=0 ⇒ FlowRun COMPLETED.
- Schema: migration **009** generaliza `sqx.decisions` con CHECKs compuestos (no nueva tabla). Optimizer rows intactas. FK `subject_ref → strategies` se elimina; `subject_kind` + `subject_ref` uuid. Unique parcial `(flow_run_ref) WHERE decision_type='FINALIST_PROMOTION'`.
- Result Surface: **slice 2**. Slice 1 deja `NOT_IMPLEMENTED`. Slice 2 mapea NOT_CONFIGURED / NOT_AVAILABLE_YET / NOT_PRODUCED / AVAILABLE / INCONSISTENT. Old FlowRuns sin bloque `promotion` = NOT_CONFIGURED, sin backfill.
- Limitation: el ranking físico `mt5-final-fidelity-ranking` es fidelidad SQX↔MT5, no Strategy Quality. Golden effective=0 promueve CERO. No reabrir M7.

## Rationale

- Empty gate es arquitectónico: OPTIMIZER_SELECTION modela 1 subject Strategy; Promotion modela el conjunto. Hybrid parent+children duplica writes sin resolver el empty case. StageInput no puede cargar RankingSnapshotRef sin mentir EvaluationRef (Foundation). Decision.stage_execution_ref NOT NULL obliga StageExecution; CompleteEmpty ya es precedente. Generalizar Decision reusa PutDecision ACK/CONFLICT/UNKNOWN.

## Consecuencias

- NEXT EXACT: `ECHO-FORGE-FINALIST-PROMOTION-V1-NORMAL` (core). Después `ECHO-FORGE-FINALIST-PROMOTION-RESULT-SURFACE-NORMAL`.
- Implementación no crea Strategy/Finalist table, no escribe Echo, no backfill, no activa Supersedes, no duplica RankingSnapshot.
- Forge→Echo futuro lee `DecisionRef` + `finalists[].StrategyRef/ScoreRef/rank` + `RankingSnapshotRef`; `canonical_strategy_id` y artifacts se joinean después.

## Alternativas descartadas

- N Decisions por Strategy: empty = cero filas, ambiguo.
- Tabla `promotion_decisions` nueva: duplica idempotencia; innecesaria fuera de producción.
- Promotion como TaskSpec en `tasks[]`: correría antes del ranking global.
- Outcome REJECTED para N=0: rechaza un éxito de dominio.
- `target_n` en Promotion: duplica autoridad de RankingSnapshot.TopN.
- Extender CanonicalInputs a RankingSnapshot: Foundation relapse.
- Finalist aggregate: membresía ya es derivable del output.
