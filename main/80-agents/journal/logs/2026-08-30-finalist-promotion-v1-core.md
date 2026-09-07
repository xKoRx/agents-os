---
type: change_log
schema_version: 1
scope: session
created: "2026-08-30"
updated: "2026-08-30"
area:
project:
application:
entities: []
related: []
aliases: []
confidence: verified
source_session:
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-08-30-finalist-promotion-v1-core

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** created
- **Archivo(s):**
  - `sqx/core/domain/decision.go`
  - `sqx/core/runtime/config.go`, `sqx/core/runtime/mt5_task_config.go`
  - `sqx/adapters/registry-postgres/decision_store.go`, `sqx/adapters/registry-postgres/migrations/009_finalist_promotion_decisions.up.sql`
  - `sqx/activities/worker/rank_snapshot_activity.go`, `sqx/workflows/generic_workflow.go`, worker wiring and regression tests

## Motivo

- Implemented Promotion V1 CORE within the hard 14-file budget, without touching Result Surface, Echo ingestion, Campaign, Builder Budget, or Foundation.

## Fuentes usadas

- Frozen Promotion V1 contract, corrections C1–C4, authorized baseline, and Promotion TOP/NORMAL project continuity.

## Resolución aplicada

- `SubjectKind` separates STRATEGY/FLOW; migration 009 preserves the FK and adds composite checks plus partial unique index. Optimizer algorithms remain unchanged; Promotion has its own ref/digest/policy/evidence/output.

## Validación

- Domain/runtime/worker targeted PASS; PostgreSQL idempotency + unique/load PASS; migration runner PASS; affected go vet PASS; commit/push converge.

## Compartibilidad

- **Scope:** local / team
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Revert commit `8580666c148bf31c5cde67c195fe58fdecb1a52e` if rollback is required; migration is additive and has no down migration in this slice.
