---
type: agent_memory
schema_version: 1
scope: project
created: "2026-09-06"
updated: "2026-09-08"
area: "[[Echo Forge]]"
project: "[[Echo Forge — Factory V2 Completion]]"
application: "[[xKoRx/symphony]]"
entities:
  - "[[Echo Forge]]"
related:
  - "[[2026-09-06-echo-forge-finalist-model-v2]]"
  - "[[Echo Forge — F-02 Finalist Model V2]]"
  - "[[Echo Forge — F-02 Finalist Model V2 Contract]]"
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
  - scope/project
---

# Echo Forge Finalist Model V2

## Continuidad

- TOP SPEC READY 2026-09-08. Symphony `origin/master` = `0509342439cfbaa048839088787458dde1ed1b05`. NORMAL no autorizado. SPEC [[Echo Forge — F-02 Finalist Model V2 Contract]]; hijo [[Echo Forge — F-02 Finalist Model V2]].
- Membership V2 = Decision FINALIST_PROMOTION@2.0.0 Finalists estructurales. Producer no copia TopProjection. RankingSnapshot.v1 no se muta.
- Identity requested vs HTM: typed result en reconcile + drop per-candidate; no abortar Generic. Infra reconcile/score sigue abortando.
- NOT_COMPARABLE include; rank nullable. Campaign cuenta unique StrategyRef. Migration `014_finalist_promotion_v2` (no NONE): policy 2.0.0 + first_rank/first_score_ref nullable.
- Dual Validate 1.0.0/2.0.0. Result v2 no exige Finalists≡TopProjection.

## Señales de carga

- Cargar con [[Echo Forge]] o Factory V2 cuando el trabajo sea Promotion V2, F-02 NORMAL, o Campaign nullable rank.

## Próxima acción

- Manager review de SPEC/TASKS. Si acepta: NORMAL T1.1–T1.6. No implementar sin autorización.
