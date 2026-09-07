---
type: decision
schema_version: 1
scope: project
created: "2026-08-30"
updated: "2026-08-30"
area: "[[Echo Forge]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[xKoRx/symphony]]"
entities:
  - "[[Echo Forge]]"
  - "[[AGENTS OS]]"
related:
  - "[[2026-08-28-durable-verified-reads-apply-reconciliation-rca]]"
  - "[[2026-08-28-durable-artifact-verified-reads-apply-correction]]"
  - "[[2026-08-30-durable-artifact-verified-reads-final-e2e-rerun]]"
aliases:
  - DURABLE-RETESTER-OPTIMIZER-RECOVERY-RCA
  - project stages technical retry recovery
confidence: verified
source_session: DURABLE-RETESTER-OPTIMIZER-RECOVERY-RCA-TOP
load_policy: manual
indexable: true
index_priority: high
tags:
  - kind/decision
  - scope/project
  - project/echo-forge
---

# 2026-08-30-durable-retester-optimizer-recovery-rca

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Contexto

- RCA read-only sobre `xKoRx/symphony` @ `e241dd90980ec9bc12d6ff14ee389d5e3764ecb9` (`HEAD == origin/master == RCA_BASELINE`; release física `0.2.80`; Artifact Verified Reads CERTIFIED_CLOSED / FROZEN). Foreign dirty preexistente no mezclado.
- Retester, Optimizer y FinalReretester comparten ProjectActivity. Tras `ResolveStageExecution` sólo asignan `st.StageExecutionRef` y retornan (`steps.go:1358-1359`, `:1362+`, `:1398+`). No cargan `StageExecutionResults`. `executeSQX` sólo corta por `BuilderRecovered` (`steps.go:1452-1455`). Un retry técnico de StageExecution COMPLETED reejecuta SQX.
- Write-once ya está certificado: rerun no clobberea, pero si `sqcli` produce bytes distintos choca `CONTRACT_CONFLICT`. Write-once no sustituye recovery. BYTE_DETERMINISTIC = FALSE (precedente empírico Retester +2 bytes @ `1bb5fdb`; ZIP/JAR `sqcli` con timestamps DOS).

## Decisión

- Los tres stages entran en UNA corrección común (Option D con semántica Option C). FinalReretester SHARES_GAP=YES; no hay diferencia material de contrato que justifique Option E. Contratos de producer siguen siendo `sqx-retester.v1` / `sqx-optimizer.v1` / `sqx-final-reretester.v1`.
- Máquina de recovery: (1) Resolve mismo StageExecution; (2) LoadStageExecutionResults; (3) COMPLETED → reconstruir carrier 0|1 desde EvaluationRefs selladas (empty válido) y omitir SQX/collect/upload; (4) RUNNING + Evaluation determinística existente → reconstruir carrier, omitir SQX/upload, dejar que `db_register` selle Complete (idempotente); (5) RUNNING + StageProducerOutput → verificar/reconciliar MinIO contra expected ref, continuar Evidence/Complete, rerun físico sólo si el objeto falta y el rerun reproduce SHA exacto; (6) RUNNING sin output durable → SQX físico legítimo; (7) tras SQX: SHA local → RecordStageProducerOutput ANTES de PutIfAbsent → Evidence → Complete.
- Reusar `sqx.stage_producer_outputs` (migration 008) sin tabla nueva. NEW_SCHEMA_REQUIRED=NO. Añadir puerto de lectura `ListStageProducerOutputs(stageRef)` sobre la tabla existente: el object_key de Retester/Optimizer se conoce sólo tras `collect_results` (filename SQX + `BuildMinIOPath`); no cambiar naming MinIO. FinalReretester ya tiene basename `final-{StrategyRef}.sqx` pero el list-by-stage cubre los tres.
- ProducerContextDigest mínimo: schema `sqx-{stage}-producer-context.v1` + `ProducerContractVersion` + `StageExecutionRef` + subject `StrategyRef` + input `EvaluationRef`. NO copiar `DecisionRef` ni `ConfigDigest` de Apply. Empty output NO usa producer-output (`size_bytes > 0`); autoridad empty = Status COMPLETED + EvaluationRefs `[]`.
- No copiar `BuilderRecovered` skip-all (Builder también salta `db_register`). Flag de pipeline: omitir `execute_sqx`+`collect_results`+`upload_results` cuando hay autoridad sealed/evidence/producer+objeto; `db_register` sigue (Adopt/Put/Complete ya son ACK). Tres bools por stage rechazados. `PhysicalExecutionRecovered` solo como skip-físico, no como skip-persist.
- FAILED/CANCELLED fail-closed. Business reprocess intacto: producer-output y Complete scoped por StageExecutionRef; NEW FlowRun → NEW StageExecution → NEW Evaluation/artifact.

## Rationale

- Identity ya converge: `ExecutionIntentKey` = FlowRunRef + TaskPath + `project@{contract}` + subject STRATEGY + inputs canónicos + generation=1. Temporal/worker/path/filename/clock/RunID no participan. COMPLETED se re-resuelve ACK sin Status; la activity no inspecciona estado. El defecto es aplicativo, no de identidad.
- COMPLETED recovery es POSSIBLE: StageExecutionRef → results → Evaluation → StrategyRef + DurableArtifactRef OUTPUT/STRATEGY_SQX → LoadStrategyIdentity → CanonicalStrategyID. Cardinalidad 0|1 simplifica vs Builder N y permite empty. EvaluationRef es content-derived (`evaluation.v1` + stage + subjectDigest + scopeDigest + contract); artifact no entra al Ref pero sí al PayloadDigest.
- El hueco pre-Evidence (W5/W6) es el mismo que forzó StageProducerOutput en Apply: objeto MinIO acceptado, Evaluation ausente, retry reejecuta SQX no determinista → write-once conflict. Record-after-local-SHA / before-Put cierra el expected sin autoridad storage-derived. Crash SQX→PG (W4) sin output durable ⇒ rerun físico legítimo.
- RCA 2026-08-26 (COMPLETED-only, `RetesterRecovered` bool, FinalReretester “likely”) queda SUPERSEDED en alcance: write-once certificado convierte el clobber en fail-closed, y tres stages idénticos en ProjectActivity invalidan el YAGNI de un flag por stage y la exclusión de FinalReretester.

## Consecuencias

- NEXT EXACT: `DURABLE-PROJECT-STAGES-RECOVERY-CORRECTION-NORMAL` en dos slices. Slice 1 (~8–10 archivos): COMPLETED + empty + Evaluation-partial (cierra W7/W8/W9). Slice 2 (~8–10): Record-before-Put + ListByStage + recovery RUNNING+producer (cierra W5/W6). Hard max 14 por slice.
- Residual irreducible (igual que Apply): producer row committed + MinIO ausente + rerun SQX byte-distinto → CONTRACT_CONFLICT; remedio = business reprocess. No depende de determinismo.
- Código/schema/release/deploy/E2E de esta sesión: NONE.

## Alternativas descartadas

- Option A sola (COMPLETED-only): deja W5/W6 como landmine write-once en retry técnico legítimo.
- Option B sola (COMPLETED + Evidence-partial): cubre W7/W9, no el crash pre-Evidence.
- Option E (recovery específico por stage): tres copias del mismo ProjectActivity gap; FinalReretester no tiene diferencia material (misma cardinalidad 0|1, mismo CompleteEmpty, mismo Resolve-sin-load). ExactOutputName no cambia el gap.
- Copiar Builder skip-db_register: W7 quedaría RUNNING con Evaluation huérfana salvo duplicar Complete en resolve.
- Copiar DecisionRef/ConfigDigest de Apply por simetría: no forman parte del producer context de estos stages.
- Tabla nueva o cambiar object keys a ExactOutputName para Retester/Optimizer: innecesario; PK existente `(stage_execution_id, object_key)` + list-by-stage basta. Renombrar keys reabre path identity.
- Usar filesystem local como autoridad: NO. Cleanup hook vacía `custom/databanks` al inicio de cada activity.
