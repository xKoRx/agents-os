---
type: known_error
schema_version: 1
scope: project
created: "2026-08-26"
updated: "2026-08-30"
area: "[[Echo]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[xKoRx/symphony]]"
related: []
aliases: []
confidence: high
source_session: DURABLE-DATA-RESUMABILITY-CERTIFICATION-2-NORMAL
entities:
  - "[[xKoRx/symphony]]"
load_policy: when_error_matches
indexable: true
index_priority: high
tags:
  - kind/known-error
  - scope/project
---

# Durable Retester Contract Conflict on Reset

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Síntoma

- Reingresar mediante Temporal Reset a un Retester `COMPLETED` ejecuta físicamente `project`; al persistir el output falla `put evaluation: contract_conflict: contract_conflict`.

## Causa

- La EvaluationRef se deriva de la identidad estable del StageExecution y puede coincidir con la ref sellada, pero el nuevo output `.sqx` puede diferir en bytes/digest. El mismo artifact key no garantiza el mismo ArtifactRef.

## Impacto

- La sesión no puede certificar Retester resumability ni continuar downstream; aplicar STOP RULE y abrir RCA específica. El FlowRun puede permanecer `COMPLETED` por la limitación del admin reset.

## Detección

- Verificar worker log del activity attempt, `DescribeWorkflowExecution.last_failure`, StageExecutionRef, EvaluationRef sellada, artifact key/size/SHA antes y después, y contadores SQL/Mongo. No introducir duplicados ni corregir código durante la certificación.

## Mitigación

- Mantener evidencia; no repetir resets del mismo target hasta RCA. Próximo paso exacto: `DURABLE-RETESTER-RESUMABILITY-RCA-TOP`.

## Estado 2026-08-30

- RESUELTO para el camino de retry técnico sobre StageExecution COMPLETED: commit `9945f85` (`DURABLE-PROJECT-STAGES-RECOVERY-SLICE1-COMPLETED-NORMAL`) hace que Retester/Optimizer/FinalReretester recuperen read-only desde la autoridad sellada (results → Evaluation → StrategyIdentity) sin reejecutar SQX ni re-subir bytes ⇒ ya no se produce el `CONTRACT_CONFLICT` de digest por re-generación física. RUNNING + Evaluation determinística existente sella idempotente; FAILED/CANCELLED fail-closed. Quedan FUERA de alcance las limitaciones administrativas de Temporal Reset (status del FlowRun) y el hueco W5/W6 (artifact uploaded sin Evaluation), que pertenece a Slice 2 (`DURABLE-PROJECT-STAGES-RECOVERY-SLICE2-PRODUCER-OUTPUT-NORMAL`).

## Evidencia

- Temporal child WorkflowID del target; ActivityID 14; worker Zeus; EvaluationRef `sha256:376b4e735ddf1ab4889b8f779ab2a3412d46fc3f64316e53f1acac72b66f0316`; artifact sellado size 56662/SHA `sha256:5a5414bf6327e0a720d952c328d8b7dd9d1c77f88af55e35f27de1de0181d29`; artifact observado después del intento size 56664/SHA `sha256:2f648c2d041d772d24ad034617ec4ec9c1edc7fc6aba1a84fbde2cf68a3bf882`.
