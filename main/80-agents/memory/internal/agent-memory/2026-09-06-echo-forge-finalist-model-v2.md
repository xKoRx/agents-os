---
type: agent_memory
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
  - "[[2026-09-06-echo-forge-finalist-model-v2]]"
  - "[[2026-09-06-echo-forge-mt5-execution-model-v2]]"
  - "[[2026-09-05-echo-forge-full-golden-flow-continuity]]"
aliases: []
confidence: high
memory_state: active
continuity_key: echo-forge/finalist-model-v2
supersedes:
superseded_by:
load_policy: when_project_loaded
indexable: false
index_priority: never
tags:
  - kind/agent-memory
  - agent/internal
  - project/echo-forge
---

# Echo Forge Finalist Model V2

## Continuidad

- TOP read-only PASS / CLOSED. Baseline `3b0737c1efe153f1f72eec40465fd1aa883887d0` == HEAD == origin/master. SDK `c85594440f6755443ceb97ec4e333cd0ddb5b0ed`. Release `0.2.96`. Dirty foráneo preservado.
- Cadena V1: `ScoreComputed` → eligible ranking → `TopProjection` truncada por `top_n` → `promotionFinalists(snapshot.TopProjection.Entries)` → Campaign unique StrategyRef. `NOT_COMPARABLE`/`INVALID_INPUT` = exclusion ranking, no finalista.
- Boundary V2: post-reconcile estructural (success HTM + parser + normalize + NativeMetricSetRef + StrategyRef/EX5 + instrument/timeframe requested==observed). Score/ranking/top_n no admiten.
- RankingSnapshot no necesita mutar: `Candidates` ya es el cohort; Promotion V2 deja de copiar `TopProjection`.
- Warnings: `PERIOD_MISMATCH`, `FIDELITY_NOT_COMPARABLE`, `PNL_SIGN_FLIP`. No inventar `FIDELITY_SCORE_LOW` ni umbrales de desviación.
- Versioning: `finalist_promotion@2.0.0`, output v2, `forge-result.v2`. V1 histórico intacto.
- Campaign: cuenta unique StrategyRef del Decision; `first_rank`/`first_score_ref` nullable en flujos nuevos. CONTINUE por shortfall de membresía estructural, no por comparable/top_n.
- Result Surface V1 `crossCheckPromotion` exige Finalists ≡ TopProjection; V2 debe romper esa igualdad o todo FlowRun V2 queda `INCONSISTENT_RESULT`.
- Graphify symphony stale (2026-09-03): documentado, no reparado. No implementar, no release, no Campaign, no FULL.

## Señales de carga

- Cargar con [[Echo Forge]] cuando el siguiente trabajo sea Promotion V2, warnings de fidelidad, ranking vs membresía, o certificación de finalists con period mismatch.

## Próxima acción

- NEXT EXACT: `ECHO-FORGE-TRADELIST-BASELINE-DURABILITY-PREFLIGHT`. Después: NORMALs MT5 Slot V2 + Finalist Model V2, un release, certificación 3-slot, FULL golden.
