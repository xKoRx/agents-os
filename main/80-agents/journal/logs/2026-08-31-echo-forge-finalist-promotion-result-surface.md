---
type: change_log
schema_version: 1
scope: session
created: "2026-08-31"
updated: "2026-08-31"
area: "[[Echo]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application:
entities: []
related:
  - "[[2026-08-30-finalist-promotion-v1-core]]"
  - "[[2026-08-31-echo-forge-finalist-promotion-v1-physical-certification]]"
aliases: []
confidence: verified
source_session: "ECHO-FORGE-FINALIST-PROMOTION-RESULT-SURFACE-NORMAL"
source_feedbacks:
  - "[[2026-08-31-echo-forge-finalist-promotion-result-surface-session-feedback]]"
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-08-31-echo-forge-finalist-promotion-result-surface

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated
- **Archivo(s):** `sqx/core/domain/forge_result.go`, `sqx/core/capabilities/forge_result_query.go`, `sqx/core/forge/result.go`, `sqx/core/forge/result_test.go`, `sqx/adapters/registry-postgres/decision_store.go`, `internal/tasks/sqx_result.go`, `internal/tasks/sqx_result_test.go`, `10-projects/Echo Forge/agentes/Echo Forge - Arquitectura de Datos y Migración de Persistencia.md`, `10-projects/Echo Forge/Echo Forge.md`

## Motivo

- Implemented the read-only Finalist Promotion V1 result projection over the immutable FlowRun config snapshot and exact FINALIST_PROMOTION Decision; the prior surface exposed `NOT_IMPLEMENTED` despite durable authority already being persisted and physically certified.

## Fuentes usadas

- Frozen Promotion V1 CORE, Supersedes guard, physical certification 0.2.83, source gate at `43eb5bed85d5404b79181425971eba9c534c25a6`, and targeted test output.

## Resolución aplicada

- Added explicit promotion statuses and JSON/human fields, narrow promotion result reader, lifecycle-aware absence semantics, Decision/config/evidence validation, exact finalist projection, and selected-ranking cross-check without reconstruction or writes.

## Validación

- PASS: core/domain, core/capabilities, core/forge, PostgreSQL promotion reader tests, metadata adapter compile, affected `go vet`, and `git diff --check`. CLI package tests remain blocked only by missing local `libzmq`.

## Compartibilidad

- **Scope:** local / team
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Revert the implementation commit if required; no migrations, workflows, ranking writers, Decision write paths, or Promotion activities changed.
