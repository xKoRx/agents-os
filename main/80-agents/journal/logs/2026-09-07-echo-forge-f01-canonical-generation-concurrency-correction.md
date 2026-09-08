---
type: change_log
schema_version: 1
scope: session
created: "2026-09-07"
updated: "2026-09-07"
area: "[[Echo]]"
project: "[[Echo Forge — Factory V2 Completion]]"
application: "[[xKoRx/symphony]]"
entities:
  - "[[Echo Forge]]"
  - "[[Echo Forge — F-01 Canonical generation concurrency]]"
related:
  - "[[Echo Forge — F-01 Canonical Generation Concurrency Contract]]"
  - "[[2026-09-04-echo-forge-campaign-builder-supply-identity]]"
aliases: []
confidence: verified
source_session: ECHO-FORGE-F01-TOP-CORRECTION-01
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
  - area/echo
  - project/echo-forge
---

# 2026-09-07-echo-forge-f01-canonical-generation-concurrency-correction

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `30-resources/applications/Echo Forge — F-01 Canonical Generation Concurrency Contract.md` (updated in-place) — SPEC F-01 corregida.
  - `10-projects/Echo/agentes/Echo Forge — F-01 Canonical generation concurrency.md` (updated in-place) — TASKS T1.1–T1.4 y planned diff corregidos.
  - `10-projects/Echo/agentes/Echo Forge — Factory V2 Completion.md` (updated) — enlace mínimo / planning / bitácora.
  - `30-resources/applications/00-index.md` (updated) — fila de catálogo.
  - `30-resources/applications/log.md` (updated) — ingest de la corrección.

## Motivo

- Manager `CORRECTION REQUIRED`: `OutputNamespaceOwnership` no discrimina producers intra-FlowRun (T7 sibling ACK); `BuilderSupplyBatchRef` namespacía la wave; Campaign `beforePut=nil` no enlaza producer authority a publication.

## Fuentes usadas

- `xKoRx/symphony@db8a022703082fd7ee9d1e15243c5d1b2feaf578`
- Agents OS parent commit `419c64084459c9c903061cad0ecf900f33313b09`
- [[Echo Forge — F-01 Canonical Generation Concurrency Contract]] (versión previa, corregida in-place)
- `sqx/core/domain/persistence_identity.go` `NewStageExecutionIdentity`
- `sqx/adapters/registry-postgres/output_namespace_ownership_test.go` T7
- `sqx/activities/worker/steps/steps.go` Campaign upload `beforePut=nil`

## Resolución aplicada

- Logical producer = Builder StageExecution. Discriminador durable = `ExecutionIntentKey`. Token filename = `p`+hex. Publication GENERATED proyecta el token y cablea `StageProducerOutputStore` existente. `DATABASE MIGRATION: NONE`. Sin segunda SPEC ni TASKS paralelas.

## Validación

- `python3 80-agents/skills/agents-os-implementation-planning/scripts/validate_plan.py` sobre el subproyecto.
- `python3 80-agents/skills/agents-os-entity-lifecycle/scripts/lint.py --strict` sobre notas tocadas.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin secretos, sin paths de máquina, sin memoria interna

## Rollback

- Revertir este commit de corrección sobre `419c640` si el manager rechaza `ExecutionIntentKey` como authority.
