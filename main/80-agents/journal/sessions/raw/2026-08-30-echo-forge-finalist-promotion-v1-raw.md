---
type: raw_session
schema_version: 1
scope: session
created: "2026-08-30"
updated: "2026-08-30"
area: "[[Echo Forge]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[xKoRx/symphony]]"
entities:
  - "[[Echo Forge]]"
related:
  - "[[2026-08-30-echo-forge-finalist-promotion-v1]]"
aliases: []
confidence: verified
source_session: ECHO-FORGE-FINALIST-PROMOTION-V1-TOP
load_policy: never
indexable: false
index_priority: never
tags:
  - kind/raw-session
  - scope/session
---

%% Filename: YYYY-MM-DD[-HHMM]-<human-topic>-raw.md. Never use UUIDs/hashes as visible names; put external IDs in source_session. %%

# 2026-08-30-echo-forge-finalist-promotion-v1-raw

> [!warning]+ Raw session L0
> Archivo de auditoría y retrofit. Excluido del retrieval normal y de Graphify.

## Contexto

- Agente: Cursor Grok 4.6
- Proyecto o entidad: [[Echo Forge]]
- Objetivo de la sesión: TOP architecture contract para Finalist Promotion V1. READ ONLY.

## Transcript

```
User: ECHO-FORGE-FINALIST-PROMOTION-V1-TOP sobre xKoRx/symphony master baseline 0674818. Golden FlowRun 812ec6ce ranking effective_top_n=0 promotion NOT_IMPLEMENTED. Cerrar contrato RankingSnapshot → Promotion Decision → Finalists. Tracks A–Y. PASS contract 25 puntos. Cerrar AGENTS OS y dejar feedback.

Agent: cold start AGENTS OS; git fetch HEAD==origin/master==0674818; graphify Decision/RankingSnapshot/GenericSQXWorkflow; lectura de decision.go, 004_durable_decisions.up.sql, ranking_snapshot.go, forge/result.go, generic_workflow.go runGlobalRankingSnapshots+sealFlowRun, durable_select_robust_run CompleteEmpty, persistence_identity taskPathPattern, WorkflowSpec Rankings.

Hallazgos load-bearing: Decision/schema optimizer-only; RankingSnapshot.TopProjection es prefijo exacto; ranking activity no tiene StageExecution; select_robust_run ya CompleteEmpty; Promotion no puede ser TaskSpec porque el ranking global corre después del loop de tasks; empty=0 rows sería ambiguo.

Contrato FROZEN. Código NONE. NEXT ECHO-FORGE-FINALIST-PROMOTION-V1-NORMAL.
```

## Evidencia externa

- HEAD `067481859ee81d494642450c5691ce291d2c3b4a`
- Golden FlowRun `812ec6ce-5bc6-48cc-9e84-0f722997b439`
- RankingSnapshotRef `sha256:6ef6e8aa…`
