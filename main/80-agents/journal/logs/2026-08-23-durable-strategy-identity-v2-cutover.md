---
type: change_log
schema_version: 1
scope: session
created: "2026-08-23"
updated: "2026-08-23"
area: "[[Echo]]"
project: "[[Echo Forge]]"
application: "[[echo-forge]]"
entities:
  - "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
related:
  - "[[2026-08-23-durable-strategy-identity-v2-cutover]]"
  - "[[2026-08-23-cursor-grok-4-6-durable-strategy-identity-v2-cutover-normal]]"
aliases: []
confidence: verified
source_session: DURABLE-STRATEGY-IDENTITY-V2-CUTOVER-NORMAL
source_feedbacks:
  - "[[2026-08-23-echo-forge-embedded-postgres-maven-dns-session-feedback]]"
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-08-23 durable strategy identity v2 cutover

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - repo `github.com/xKoRx/symphony` paths `sqx/adapters/registry-postgres/adopt_strategy.go`, `adopt_strategy_v2_test.go`, `control_plane_integration_test.go`
  - `80-agents/memory/public/decision/symphony/2026-08-23-durable-strategy-identity-v2-cutover.md`
  - `80-agents/memory/public/known-error/symphony/embedded-postgres-maven-dns-timeout.md`
  - `80-agents/memory/internal/agent-memory/global/agents-os-operating-continuity.md`
  - `10-projects/Echo Forge/agentes/Echo Forge - Arquitectura de Datos y Migración de Persistencia.md`

## Motivo

- Activar identity v2 como contrato vigente de `AdoptStrategy()` antes del lanzamiento. Echo Forge no está en producción; no hay compatibilidad v1 que preservar.

## Fuentes usadas

- Baseline `dcba274d3bb1e569b3902a332af72181662563f2`
- Commit `7c0b2892a507975dfbdced085c37a4bafbb9e858` (`HEAD == origin/master`)
- [[2026-08-23-durable-strategy-identity-v2-storage-support]]
- Invariante: Strategy nace una vez en Builder; downstream reusa la misma StrategyRef/`canonical_strategy_id`

## Resolución aplicada

- `AdoptStrategy()` llama `upsertStrategyV2()`. Tests de cutover cubren misma Strategy cross-config/cross-FlowRun, origin `config_id` preservado, PRODUCED/REPROCESSED, conflicto, y cero escrituras v1 nuevas. Aserciones de control plane que observaban model=1 vía `AdoptStrategy()` pasan a model=2.

## Validación

- `gofmt`; `go test -c ./sqx/adapters/registry-postgres` PASS; `go vet ./sqx/adapters/registry-postgres/...` PASS; `go test ./sqx/core/domain/...` PASS; `git diff --check` PASS
- `go test ./sqx/adapters/registry-postgres/...` DEGRADED: Maven Central DNS timeout; sin Docker/Postgres local/`TEST_POSTGRES_DSN`

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths de máquina, memoria interna ni secretos

## Rollback

- Revertir el commit de cutover restaura `upsertStrategyV1()` en `AdoptStrategy()`. No hay filas v2 productivas que revertir.
