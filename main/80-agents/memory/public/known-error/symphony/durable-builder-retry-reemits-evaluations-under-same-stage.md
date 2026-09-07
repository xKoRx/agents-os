---
type: known_error
schema_version: 1
scope: application
created: "2026-08-24"
updated: "2026-08-24"
area: "[[Echo]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[Symphony]]"
entities:
  - "[[StrategyQuant X]]"
  - "[[Strategy Identity v2]]"
related:
  - "[[2026-08-23-durable-strategy-identity-v2-cutover]]"
aliases:
  - Builder contract conflict on retry
  - CompleteStageExecution contract conflict
confidence: verified
source_session: DURABLE-STRATEGY-IDENTITY-V2-BUILDER-CONTRACT-CONFLICT-REQUEST-ID-NEW-NORMAL
load_policy: when_error_matches
indexable: true
index_priority: high
tags:
  - kind/known-error
  - scope/application
  - app/echo-forge
  - tech/symphony
---

# Builder retry re-emits evaluations under the same StageExecution

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Síntoma

- El primer intento completa el Builder con N evaluaciones. Un reintento del mismo Temporal Workflow/Run vuelve a ejecutar SQX y produce N nuevas evaluaciones bajo el mismo `StageExecutionRef`; `CompleteStageExecution` responde `CONTRACT_CONFLICT`.

## Causa

- El `FlowRun` y la `StageExecution` son durables e idempotentes por contrato, pero el activity de Builder no reutiliza el conjunto persistido al reintentarse: vuelve a generar StrategyRefs/EvaluationRefs físicos nuevos. El `request_id` legado explica la reutilización del contexto, pero el conflicto se reprodujo como defecto de reintento.

## Impacto

- Se acumulan Strategy rows y Evaluation docs huérfanas de la segunda/tercera ejecución; el workflow queda incompleto y la identidad durable queda sin cierre consistente.

## Detección

- Correlacionar el mismo `StageExecutionRef` con múltiples lotes temporales de EvaluationRefs y observar `Attempt 2/3` en Temporal con el mismo WorkflowID/RunID.

## Mitigación

- No reintentar ciegamente ni limpiar datos históricos. Investigar/fijar el contrato de retry para que el activity sea idempotente o rechace la generación duplicada antes de persistir. Usar un `request_id` nuevo sólo para aislar corridas, no como corrección del defecto.

## Evidencia

- Auditoría read-only: FlowRun `14bb6c89-7a12-440f-a950-579003cbfe85`, StageExecution `27894a0f-8cd0-45c1-8106-6b6d4d80df64`, 20 refs persistidas frente a 20 refs intentadas en cada uno de los dos reintentos; Mongo registró 60 Evaluation docs y SQL 60 memberships.
