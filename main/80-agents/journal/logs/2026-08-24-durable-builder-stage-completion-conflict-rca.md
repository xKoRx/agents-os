---
type: change_log
schema_version: 1
scope: session
created: "2026-08-24"
updated: "2026-08-24"
area: "[[Echo]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[Symphony]]"
entities:
  - "[[Strategy Identity v2]]"
related:
  - "[[durable-builder-retry-reemits-evaluations-under-same-stage]]"
  - "[[final-reretester-missing-strategy-artifact-return]]"
aliases: []
confidence: verified
source_session: DURABLE-BUILDER-STAGE-COMPLETION-CONFLICT-RCA-TOP
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-08-24-durable-builder-stage-completion-conflict-rca

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** conflict-resolution
- **Archivo(s):**
  - `10-projects/Echo Forge/agentes/Echo Forge - Arquitectura de Datos y Migración de Persistencia.md` checkpoint append-only DURABLE-BUILDER-STAGE-COMPLETION-CONFLICT-RCA-TOP.
  - `80-agents/memory/internal/agent-memory/global/agents-os-operating-continuity.md` delta de continuidad.
  - `80-agents/journal/agent-runs/2026-08-24-zcode-ox-alpha-durable-builder-stage-completion-conflict-rca-top.md` creado.

## Motivo

- Cerrar el RCA read-only del defecto Builder retry `contract_conflict` con root cause demostrado a nivel código, corrección mínima propuesta y handoff accionable.

## Fuentes usadas

- `symphony` @ `7c0b2892a507975dfbdced085c37a4bafbb9e858`: RetryPolicy (`sqx/workflows/generic_workflow.go`), pipeline durable (`sqx/activities/worker/project_activity.go`, `pipeline/builder.go`, `steps/steps.go`), converge/control plane (`sqx/adapters/registry-postgres/stage_execution.go`, `adopt_strategy.go`), cadena de identidad (`core/domain/canonical_strategy_id.go`, `persistence_identity.go`, `adapters/overview/binding/`), Mongo (`adapters/metadata-mongo/evidence_store.go`) y carriers downstream (`sqx/workflows/durable_*.go`).
- Evidencia operativa previa del día: FlowRun `14bb6c89-7a12-440f-a950-579003cbfe85`, StageExecution `27894a0f-8cd0-45c1-8106-6b6d4d80df64` (60 evaluaciones / 3 intentos) y corrida fresca exitosa.

## Resolución aplicada

- ROOT CAUSE confirmado: retry re-ejecuta execute_sqx porque resolve_stage_execution converge al mismo StageExecutionRef sin consultar status y no hay short-circuit COMPLETED; CompleteStageExecution y Mongo CORRECTOS; recovery data suficiente en datos pero faltan puertos públicos (LoadStageExecutionResults + rebuild []StrategyArtifact).
- Fix propuesto documentado (~6 archivos) sin implementar; KNOWN NEXT BLOCKER FINAL_RERETESTER_ONE_KEY_ONE_ARTIFACT registrado sin investigar (StageExecutionRef d5c2b631-220d-4d8d-ab4c-8e459602108a).

## Validación

- Cadena retry → nuevos refs verificada file:line contra baseline; hipótesis D del mandato CONFIRMADA; A=YES, B=YES, C=NO; sesiones read-only: cero cambios en repo o datos.

## Compartibilidad

- **Scope:** local / team
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Notas append-only; revertir = eliminar las notas creadas y el bullet de continuidad añadido.
