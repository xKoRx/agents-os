---
type: known_error
schema_version: 1
scope: project
created: "2026-08-30"
updated: "2026-08-30"
area: "[[Echo Forge]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[xKoRx/symphony]]"
entities:
  - "[[Echo Forge]]"
related:
  - "[[2026-08-30-durable-project-stages-recovery-fault-certification]]"
  - "[[2026-08-30-durable-optimizer-wf-matrix-cardinality-rca]]"
  - "[[2026-08-30-durable-retester-optimizer-recovery-rca]]"
aliases:
  - WF Matrix segundo sqx optimizer
  - singleton optimizer dos salidas
confidence: verified
source_session: DURABLE-PROJECT-STAGES-RECOVERY-FAULT-CERTIFICATION-NORMAL
load_policy: when_error_matches
indexable: true
index_priority: high
tags:
  - kind/known-error
  - scope/project
  - project/echo-forge
---

# optimizer-wf-matrix-second-sqx-output

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Síntoma

- En E2E físico, la activity `project` del stage `03_optimizer` falla con `CONTRACT_CONFLICT` non-retryable en el paso `upload_results`: `durable singleton stage allows at most one .sqx output; found 2 before any record or upload`. El child workflow del grupo falla y el FlowRun termina FAILED. Alternativamente (pre-Slice 2), el mismo dato moría después en `db_register` (`TestDBRegister_DurableOptimizerMultipleOutputsFailClosed`) posiblemente tras subir objetos a MinIO.

## Causa

- El CFX Optimizer (`Optimization type=3` Walk-Forward + `DontSaveOriginalStr=false`) hace que SQX escriba DOS archivos locales: el sidecar original (~42 KiB) y el databank `WF Matrix - <name>.sqx` (~1 MiB). El logical producer output de `sqx-optimizer.v1` es **uno**: el databank WF Matrix, que `upload_prefix_filter=WF_Matrix` publica desde 2026-07-12. Slice 2 F8 cuenta raw `ResultFiles` **antes** de ese filtro ⇒ `CONTRACT_CONFLICT` con 2 locales y 0 publishable committed. El cohort 25 vs 26 no es causal (mismo CFX; 0.2.80 no tenía F8; cleanup borra raw). RCA: [[2026-08-30-durable-optimizer-wf-matrix-cardinality-rca]].

## Impacto

- [RESUELTO 2026-08-30] El pipeline vuelve a COMPLETAR para cohorts con estrategias walk-forward desde la release **0.2.82**: golden de recertificación con FlowRun `812ec6ce` COMPLETED, 12 optimizers walk-forward publicando exactamente 1 databank WF Matrix cada uno y cardinalidad global inválida cero. Ver [[2026-08-30-durable-project-stages-recovery-physical-recertification]]. El impacto histórico (BLOCKED de la fault certification 0.2.81) quedó documentado abajo.
- El mecanismo durable NO estaba dañado: el gate falló cerrado ANTES de record/put (0 producer rows, 0 PUTs MinIO, stage RUNNING sin sello, write-once y precedencia de autoridades intactas, cardinalidad inválida cero).

## Detección

- Temporal: actividad `project` (optimizer) con error `contract_conflict` "found 2 before any record or upload" (capturar `attempt` — es perezoso). PG: `sqx.stage_executions` del optimizer en RUNNING sin producer rows. MinIO: prefijo `03_optimizer/` del wave sólo con `.folder_marker`. Workspace del worker: `~/sqx/user/projects/custom/databanks/output/` con el par `XAUUSD_..._<strategy>.sqx` + `WF Matrix - XAUUSD_..._<strategy>.sqx`.

## Mitigación

- [RESUELTO] Corrección implementada en `6b13c66` (`DURABLE-OPTIMIZER-OUTPUT-CARDINALITY-CORRECTION-NORMAL`, Opción A: batch preflight de publishables ANTES de record/put; `planExactUploadCandidates` del storage es la única autoridad de publicación) y físicamente certificada en 0.2.82 (`DURABLE-OPTIMIZER-OUTPUT-CARDINALITY-CORRECTION: PHYSICALLY_CERTIFIED`). No eliminar el WF Matrix `.sqx`. Retester/FinalReretester fuera de alcance (CFX WF `use=false`).

## Evidencia

- Golden 0.2.81 (`abe19d0`): RequestID `final-stages-recovery-cert-e2e-normal-20260830T200907Z-9511775d`, FlowRun `abcd39d4-03e8-4621-9095-50cae6eaafd6`, child chunk-0 run `01a0544e-e22e-79a6-8fb1-a084d6e5252f` EVT 19 failed 20:14:57.595Z attempt=1 en `2062668@sqx-ulab-zeus-0@`; par físico documentado (SHAs en [[2026-08-30-durable-project-stages-recovery-fault-certification]]; los archivos locales fueron consumidos por el cleanup legítimo del producto durante el golden 0.2.82). Recertificación 0.2.82: FlowRun `812ec6ce-5bc6-48cc-9e84-0f722997b439` COMPLETED con 12 optimizers WF publicando 1 databank c/u y cruce producer==evaluation 12/12 exacto — [[2026-08-30-durable-project-stages-recovery-physical-recertification]].
