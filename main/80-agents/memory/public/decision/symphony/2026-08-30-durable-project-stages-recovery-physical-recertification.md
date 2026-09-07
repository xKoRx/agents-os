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
  - "[[2026-08-30-durable-optimizer-output-cardinality-correction]]"
  - "[[2026-08-30-durable-project-stages-recovery-fault-certification]]"
  - "[[optimizer-wf-matrix-second-sqx-output]]"
aliases:
  - DURABLE-PROJECT-STAGES-RECOVERY-PHYSICAL-RECERTIFICATION-NORMAL
  - recertificación física foundation V1
confidence: verified
source_session: DURABLE-PROJECT-STAGES-RECOVERY-PHYSICAL-RECERTIFICATION-NORMAL
load_policy: manual
indexable: true
index_priority: high
tags:
  - kind/decision
  - scope/project
  - project/echo-forge
---

# 2026-08-30-durable-project-stages-recovery-physical-recertification

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Contexto

- Recertificación física FINAL sobre `xKoRx/symphony` @ `6b13c66cf195a83709c156e25aa8dfd6a17c140e` (`HEAD == origin/master`, parent exacto `abe19d0`; DRIFT NONE, CODE CHANGES NONE, foreign dirty preservado). El incidente 0.2.81 ([[optimizer-wf-matrix-second-sqx-output]]) fue corregido en código por [[2026-08-30-durable-optimizer-output-cardinality-correction]] y esta sesión debía demostrarlo físicamente con NEW release + NEW IDs y cerrar PROJECT_STAGE_RECOVERY y ECHO_FORGE_DURABLE_FOUNDATION_V1. Certification-only: sin fix, sin segunda release, sin re-run, sin Temporal Reset.

## Decisión

- **SESSION RESULT: PASS / CLOSED** — los 28 gates del mandato PASS. Declaración: `PROJECT_STAGE_RECOVERY: CERTIFIED_CLOSED`, `ECHO_FORGE_DURABLE_FOUNDATION_V1: CERTIFIED_CLOSED`, `DURABLE_OPTIMIZER_OUTPUT_CARDINALITY_CORRECTION: PHYSICALLY_CERTIFIED`.
- **Prior fault matrix reuse PASS**: diff `abe19d0..6b13c66` = exactamente la corrección (6 archivos; `write_once.go`, `registry-postgres/*`, `project_stage_recovery.go` intactos; delta de `steps.go` confinado al gate F8). F0–F7 y F9–F16 citables de Part A (abe19d0); F8 redefinido re-ejecutado completo.
- **F8 REDEFINED PASS** (CASE A–D + matriz 8 subtests): CASE A `OptimizerSidecarFilteredBeforeCardinality` con storage real (raw 2 → publishable 1 WF-only → record 1 → PUT 1, sidecar nunca publicado); CASE B dos publishables → CONTRACT_CONFLICT antes de record/put (0 writes); CASE C producer sellado + regen con 0 publishable → conflicto, CompleteEmpty 0, PUT 0; CASE D regen exacta → replay → PUT → evidence → complete.
- **Targeted test gate PASS**: steps 1.17s / worker 9.7s / storage-minio 0.59s / optimizer-binding 0.53s / registry-postgres targeted `StageProducerOutput|CompleteStageExecution` 7/7 (PG real manual `.txz` + `TEST_POSTGRES_DSN` + DB virgen, 63.2s) / concurrencia `SingletonConcurrency|ConcurrentProducerVsEmpty` ×10 20/20 (87.4s) / compile sweep sin `sqx/tools` exit 0 / vet sin tools exit 0. SDK pin `ea09cc1bb8b34e661c8f31f887dce58613b0475a` intacto (`replace ../sdk`).
- **Release 0.2.82** (`deploy_release.sh "" 240`): `vcs.revision=6b13c66` en linux Y windows, LINUX_SHA256 `98b8475000bb38a20616cea8954788b76e3aadb64946392c9decd4f3839e8c8a` y WINDOWS_SHA256 `4b830a11305a2dd4e63d4d6ddd098845893882f88b9246a0a856c3778f9a37ef` == manifest; `vcs.modified=true` explicado por los 4 archivos dirty operacionales no-Go. Rollout HARD GATE PASS: manifest confirmado en MinIO ~21:44Z, stagers aplicaron 0.2.82 y los pollers 0.2.81 dejaron de pulsar; verificación on-host positiva (`/opt/stager/releases/0.2.82/bin/symphony`, SHA == manifest, PID == identidad del poller, NONE_OLD) en ZEUS `2077053` (start 21:44:00Z), HERA `795902` (21:43:41Z) y KRONOS `817617` (21:45:07Z, obligatorio); WINDOWS `456` por rotación de poller + manifest pineado (canal precedente 0.2.80/0.2.81). Colas al despacho: `sqx-main-queue` exactamente 3 pollers y `sqx-mt5-queue` 1 — `OLD_RELEASE_ELIGIBLE_POLLERS: ZERO`.
- **Golden run (IDs todos nuevos)**: RequestID `final-stages-recovery-recert-e2e-normal-20260830T214235Z-e216689e`; FlowRunRef `812ec6ce-5bc6-48cc-9e84-0f722997b439`; FlowIntentToken `9a6c0bec-4f64-4029-ad26-876a2f3c884d`; WorkflowID `sqx-main-v1-9a6c0bec-4f64-4029-ad26-876a2f3c884d`; RunID `01a054a4-322c-77a5-b860-16aa1b298526`; wave `final-stages-recovery-recert-e2e-20260830-214235`; strategy `example_flow_27` (bump canónico del deployer desde `example_flow_26`; mismo CFX `optimizer_test.cfx` con `upload_prefix_filter=WF_Matrix` — no se tocó DontSaveOriginalStr ni semántica de cohort). RESULTADO: **WORKFLOW Completed 22:02:53Z** (21:47:22→22:02:53, 503 eventos) y **FLOW_RUN COMPLETED**; 63 stage executions todos COMPLETED; 22/22 children GroupSQXWorkflow COMPLETED; 60/60 activities attempt=1 (cero retries); inventario completo: flow_run_start, classification_snapshot, early_rank_snapshots + rank_snapshot, 12× wfm_durable_export + 12× wfm_durable_seal, 4× select_robust_run, 4× apply_selected_run, 4× mt5_exporter, 4× mt5_reconcile, 4× mt5_score_shadow, 4× trade_list_exporter, 4× stage `mt5_backtesting@mt5-backtest.v1` COMPLETED, generate_report, flow_run_seal.
- **Optimizer incident physical proof PASS**: 12 optimizers COMPLETED; PG `stage_producer_outputs` exactamente 1 fila por stage (12); MinIO `03_optimizer/` exactamente 12 `.sqx` publicados (2.1–6.0 MB, databanks WF Matrix; tamaño del sidecar ~42KB ausente ⇒ `SIDECAR_PUBLISHED: NO`) + marker; Mongo 12 evaluaciones con exactamente 1 artifact OUTPUT STRATEGY_SQX cada una; cruce programático 12/12 product row == evaluation artifact EXACTO (Store/Bucket/ObjectKey/Size/SHA256). `RAW_LOCAL_SQX >= 2` demostrado por F8 CASE A sobre storage real en esta release (raw 2 → publishable 1); el output local del golden fue consumido por el cleanup legítimo post-upload (folder zeus vacío, comportamiento de producto esperado), sin observación viva del par.
- **Cardinalidad global**: matriz sobre los 63 stage executions → `INVALID_CARDINALITY=0` (prohibidos COMPLETED []+fila, COMPLETED [ref]+0 filas, filas>1: ninguno); retester 12 non-empty (1 fila + 1 eval c/u) + 2 empty (0 filas, 0 evals); final reretester 4/4 no-vacío y alcanzado físicamente.
- **Cadenas de autoridad**: 648/648 evaluaciones de celda WFM (54×12) contienen en `input_evaluation_refs` la EvaluationRef del optimizer de su MISMA StrategyRef (el databank WF es el artifact del producer); aggregates WFM por picks de celdas; Apply 4/4 consume optimizer eval + WFM eval de la misma estrategia y su payload trae `decision_ref` (PG Decision v1, status APPLIED); FinalReretester 4/4 consume la eval de Apply y publica `final-<StrategyRef>.sqx` (convergencia singleton ExactOutputName). Robust Selection sin evals Mongo por diseño (Decisión PG v1). Continuidad StrategyRef: 4 estrategias aplicadas con el MISMO UUID en retester→optimizer→wfm→apply→final, sin mint downstream. Lineage DecisionRef/BuilderMetricSetRef según carrier actual: preservación certificada por los tests de carrier de Slice 1/2 (suite steps PASS en esta sesión) + input Apply físico.
- **Authority audit ZERO**: MINIO_LIST_AS_RECOVERY_AUTHORITY / STAT_AS_EXPECTED_AUTHORITY / ETAG_AS_DIGEST / EXPECTED_SHA_FROM_STORAGE / LOCAL_FS_AS_DURABLE_RECOVERY_AUTHORITY = 0 en la máquina de recovery y steps; los ListObjects/StatObject restantes son legacy no-durable documentados (list_strategies, folder-marker, TradeListStorage wiring retirado). Write-once regression PASS vía los tests canónicos de esta misma release (primitiva intacta desde `ea09cc1`/slices; `write_once.go` sin diff en el intervalo) + 16 puts físicos del golden vía `PutObjectIfAbsent` con record-before-put sin overwrite ni conflicto.

## Rationale

- El incidente 0.2.81 se reprodujo por diseño (mismo CFX, mismo filtro WF_Matrix, cohort con walk-forward) y esta vez atravesó el caso que falló: la corrección de cardinalidad publicable demostró su contrato en physical. El mecanismo durable completo (recovery, singleton gate, record-before-put, write-once, precedencia de autoridades) no sufrió ninguna violación durante la corrida.
- La homogeneidad del rollout quedó demostrada en tres capas independientes: rotación de identidades de pollers (stale evictado por Temporal), verificación on-host del binario (path + SHA == manifest) y las identidades de los 60 activity starts del historial = PIDs nuevos exclusivamente.

## Consecuencias

- **STOP FOUNDATION ITERATION**: no abrir otro durable micro-track sin evidencia material nueva. La fundación durable V1 queda cerrada y congelada.
- NEXT EXACT: `ECHO-FORGE-POST-FOUNDATION-PRODUCT-RESUME-TOP` — volver al producto (automation, ranking/selection, operability; qué falta para explotar el pipeline ya funcional). NO nueva foundation por defecto.
- Defecto del incidente cerrado: [[optimizer-wf-matrix-second-sqx-output]] queda resuelto y físicamente certificado en 0.2.82.
- Deuda conocida NO bloqueante que sigue vigente: 24 workflow fixtures, PG harness (cache per-PID/OpenDB), aislamiento de workspace (el cleanup del producto consumió la evidencia local preservada del incidente 0.2.81 en zeus), Graphify (deuda frontmatter).
- Código producto cambiado en esta sesión: NONE. Foreign dirty preservado (`deploy/manifest.json` ahora 0.2.82, `go.work.sum`, `input/example/config.json` con wave/request de esta sesión y strategy `example_flow_27`, fixture `phase4_performance.json`).

## Alternativas descartadas

- Observar el par raw en vivo dentro del golden (pausar/cancelar un optimizer para preservar locales): habría manipulado la corrida de certificación; el mandato permite worker local evidence pero no intervenir, y F8 CASE A con storage real ya demuestra el shape raw→publishable.
- Re-ejecutar la matriz F0–F16 completa en vez de citarla: el diff verificado confirma que recovery mechanics no cambiaron; re-ejecutar habría sido costo sin valor de evidencia.
- Atribuir los folders 07/08/09 con sólo marker como pipeline incompleto: la comparación física con el golden certificado 0.2.80 muestra la MISMA forma (markers solamente; MT5×8 fue evidencia local del worker) y los stages `mt5_exporter`/`mt5_reconcile`/`mt5_score_shadow`/`mt5_backtesting` completaron 4/4 en el historial.
