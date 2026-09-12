---
type: change_log
schema_version: 1
scope: session
created: "2026-09-12"
updated: "2026-09-12"
area: "[[Echo]]"
project: "[[Echo Forge — F-04 Magic allocation, version seal and handoff]]"
application: "[[xKoRx/symphony]]"
entities:
  - "[[Echo Forge — F-04 Magic allocation, version seal and handoff]]"
  - "[[Echo Forge — F-04 Magic Allocation, Version Seal and Handoff Contract]]"
related:
  - "[[Echo Forge — Factory V2 Completion]]"
  - "[[Echo — E-04 Forge Ingestion E1]]"
aliases: []
confidence: verified
source_session:
source_feedbacks:
  - "[[2026-09-12-f04-compile-evaluation-session-feedback]]"
share_scope: team
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-09-12-echo-forge-f04-compile-evaluation-authority

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `10-projects/Echo/agentes/Echo Forge — F-04 Magic allocation, version seal and handoff.md`
  - `30-resources/applications/Echo Forge — F-04 Magic Allocation, Version Seal and Handoff Contract.md`
  - `10-projects/Echo/agentes/Echo Forge — Factory V2 Completion.md`

## Motivo

- TOP resolvió el gap único: Forge tiene bytes/artifacts durables del compile pero no un `compile_evaluation_ref` durable para `HandoffManifestV1.BuildLineage`. La autoridad canónica es un `domain.EvaluationRef` sellado en StageExecution existente; migración 017 no es necesaria.

## Fuentes usadas

- Symphony `feature/f04-magic-version-handoff` HEAD `9fad768ccd1f9d25ebb535a2d26edb3d74556c10`; `origin/master` `0b9742b09019526a8119f086199d15d1f0d42cb1`; merge parents `ea8be76` + `0b9742b`.
- Source: `handoff_producer.go`, `durable_apply_selected_run.go`, `mt5_reconcile_activity.go`, `artifact_compiler.go`, `generic_workflow.go` `executeMT5ArtifactTask`/`persistMT5ReconcileV1`, `persistence_contracts.go`, `stage_execution.go`, `evidence_store.go`.
- Echo consumer `xKoRx/echo@a99f9a63354bbe72219d1e590bb93757ed08e45e`; S0 pin `91671f6f` intacto.

## Resolución aplicada

- Contrato F-04 congelado: compile StageExecution `mt5_compiler@mt5-compile.v1` → EvaluationEvidence → `CompleteStageExecution([exactly 1])` → assembler F-04 lee por ref exacta. Persistencia en worker padre, análoga a `mt5_reconcile_v1`, no en `sqx-mt5-queue`. MIGRATION 017 = NO.

## Validación

- Git ancestry verificado (`master` ancestro de feature; feature ahead 9, behind 0). Dirty foráneo `specs/FEAT-SQX-STRATEGY-EVALUATION/fixtures/phase4_performance.json` preservado. Sin implementación de product source.

## Compartibilidad

- **Scope:** team
- **Redacción revisada:** sin identidad, paths locales de máquina, memoria interna ni secretos

## Rollback

- Revertir las actualizaciones documentales de Agents OS; no hay cambios de código Symphony/Echo que revertir.
