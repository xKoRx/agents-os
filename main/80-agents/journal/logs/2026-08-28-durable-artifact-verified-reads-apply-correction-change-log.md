---
type: change_log
schema_version: 1
scope: session
created: "2026-08-28"
updated: "2026-08-28"
area: "[[Echo Forge]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[xKoRx/symphony]]"
entities:
  - "[[Echo Forge]]"
related:
  - "[[2026-08-28-durable-artifact-verified-reads-apply-correction]]"
aliases: []
confidence: verified
source_session: DURABLE-ARTIFACT-VERIFIED-READS-APPLY-CORRECTION-NORMAL
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-08-28-durable-artifact-verified-reads-apply-correction-change-log

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** created
- **Archivo(s):**
  - `sqx/core/capabilities/persistence.go`
  - `sqx/adapters/registry-postgres/migrations/008_stage_producer_outputs.up.sql`
  - `sqx/adapters/registry-postgres/stage_producer_output.go`
  - `sqx/adapters/apply-selected-run/binding/{contract.go,evidence.go}`
  - `sqx/adapters/storage-minio/apply_selected_run.go`
  - `sqx/activities/worker/durable_apply_selected_run.go`
  - `80-agents/memory/internal/agent-memory/global/agents-os-operating-continuity.md`

## Motivo

- Implementar la corrección aceptada para que Apply tenga autoridad durable independiente antes de MinIO y replay exacto después de Evaluation.

## Fuentes usadas

- [[2026-08-28-durable-verified-reads-apply-reconciliation-rca]], contratos congelados del usuario, baseline `5e93c7cda3f4fcc825f3939a951247cd4e63fec2`, commit `2fa17010c0fed887430d857fa5de2889fe57075c`.

## Resolución aplicada

- Se agregó la tabla/control port insert-only; se ligó producer context determinísticamente; se sustituyó la reconciliación self-authoritative por verificación contra un expected ref; se implementaron ramas COMPLETED/RUNNING/producer record/first production y fault-injection contracts.

## Validación

- `git diff --check` pasó; `HEAD == origin/master`; suites focales y compilación `sqx` sin tools pasaron. PostgreSQL integrado quedó no ejecutable por shared memory del host y la suite global por errores preexistentes de `sqx/tools`.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Revertir el commit `2fa17010c0fed887430d857fa5de2889fe57075c` sólo mediante una nueva decisión explícita; no alterar el registro insert-only para acomodar datos nuevos.
