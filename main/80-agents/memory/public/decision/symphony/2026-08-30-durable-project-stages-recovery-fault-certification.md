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
  - "[[2026-08-30-durable-retester-optimizer-recovery-rca]]"
  - "[[optimizer-wf-matrix-second-sqx-output]]"
  - "[[2026-08-30-durable-artifact-verified-reads-final-e2e-rerun]]"
aliases:
  - DURABLE-PROJECT-STAGES-RECOVERY-FAULT-CERTIFICATION-NORMAL
  - certificación final fault matrix recovery
confidence: verified
source_session: DURABLE-PROJECT-STAGES-RECOVERY-FAULT-CERTIFICATION-NORMAL
load_policy: manual
indexable: true
index_priority: high
tags:
  - kind/decision
  - scope/project
  - project/echo-forge
---

# 2026-08-30-durable-project-stages-recovery-fault-certification

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Contexto

- Sesión FINAL CERTIFICATION sobre `xKoRx/symphony` @ `abe19d09a0bafc7ec21abbf54ca136684e202177` (`HEAD == origin/master == CERTIFIED_SOURCE`, DRIFT: NONE; Slice 1 `9945f85` y Slice 2 `8caa97a` ancestros). Dos gates obligatorios: (A) FAULT/RETRY MATRIX F0–F16, (B) NEW PHYSICAL GOLDEN RUN sobre release que contenga exactamente el source autorizado. Certification-only: cero cambios de código producto.
- PART A PASS completo: suites `steps` (1.35s, 130+ tests), `worker` (9.7s), `storage-minio` (0.62s), `registry-postgres -run 'StageProducerOutput|CompleteStageExecution'` (7/7, PG real, 61.1s), stress `SingletonConcurrency|ConcurrentProducerVsEmpty -count=10` (20/20, 85.7s), bindings retester/optimizer PASS, final-reretester compila (sin tests, baseline), compile sweep sin `sqx/tools` exit 0, vet exit 0. F0–F16 todos PASS mapeados a tests existentes sobre código real `abe19d0` (detalle en checkpoint del proyecto). W0–W9 cerrada: W0–W4 físico legítimo (P0), W5–W6 producer gobierna (F9/F4), W7 Evaluation gobierna (F3), W8–W9 Results/completion gobiernan (F5/F6/F11 + linearizabilidad empty-race).
- PART B: release `0.2.81` construida con `deploy_release.sh "" 240` desde `abe19d0` (SDK pin `v0.0.0-20260827204048-ea09cc1bb8b3` == `ea09cc1bb8b34e661c8f31f887dce58613b0475a`, `vcs.revision=abe19d0` en linux+windows, SHA256 linux `83006f72…` y windows `6d31232c…` == manifest == binario on-host). WORKER ROLLOUT HARD GATE PASS: ZEUS `2007789`→`2062668` (start 20:11:07Z), HERA `774723`→`791646` (20:11:46Z), KRONOS `798248`→`814369` (20:11:28Z) verificados positivamente on-host (`/opt/stager/releases/0.2.81/bin/symphony`, SHA == manifest, PID == poller, cero procesos de release vieja); WINDOWS `worker-kronos` `8896`→`1188`→`1500` por rotación de poller + manifest pineado (sin canal de versión directa, precedente 0.2.80). Ejecución homogénea demostrada: manifest publicado 20:09:27Z, flow despachado 20:13:27Z (post-ventana), toda identidad del historial Temporal = PIDs nuevos.

## Decisión

- GOLDEN RUN FAILED ⇒ **CERTIFICATION BLOCKED / CLOSED**. IDs preservados: RequestID `final-stages-recovery-cert-e2e-normal-20260830T200907Z-9511775d`; FlowRunRef `abcd39d4-03e8-4621-9095-50cae6eaafd6`; WorkflowID `sqx-main-v1-c719890e-004c-478c-9186-c0420deb1f76`; RunID `01a0544e-3baf-726e-aeca-39fcaf15b1bd`; wave `final-stages-recovery-cert-e2e-20260830-200907`; strategy `example_flow_26`.
- Clasificación causal: **PRODUCT** (no INFRA, no VERSION_SKEW): el optimizador SQX de estrategias con Walk-Forward habilitado emite DOS `.sqx` — el optimizado + `WF Matrix - <nombre>.sqx` — y el gate singleton certificado (Slice 2, F8: `durable singleton stage allows at most one .sqx output; found 2 before any record or upload`) falla cerrado CONTRACT_CONFLICT non-retryable ANTES de record/put, exactamente según contrato congelado. El pipeline físico no puede completarse para cohorts con estrategias WF ⇒ gate 22 (pipeline COMPLETED end-to-end) FAILS ⇒ NO certificación.
- Evidencia física preservada (NO borrar): child workflow chunk-0 runID `01a0544e-e22e-79a6-8fb1-a084d6e5252f` EVT 17/18/19 — optimizer de `Strategy_4.1.15.h0` (subject `28a432c4…`, StageExecutionRef `c95a655d-1dae-41a6-a0b4-782febe59608`) started 20:14:33.197Z attempt=1 identity `2062668@sqx-ulab-zeus-0@`, failed 20:14:57.595Z por el gate; `WF Matrix - XAUUSD_L_H1_example_flow_26_v1_Strategy_4.1.24.h0.sqx` (1030698 B, sha256 `1458c4ed8b9f0b8f934901052ef014c17b97a946a22c84a769ce4d88c2ea4075`) + par optimizado (42045 B, sha256 `62212a807b580d4b394101332486b635128f55a035c7d8014fc86f5170cbfab3`) en `zeus:/home/kor/sqx/user/projects/custom/databanks/output/` (mtime 20:16:11Z, actividad cancelada post-workflow-failure antes de su cleanup). Estado durable coherente: 13 Retesters COMPLETED (9 non-empty con exactamente 1 producer row + 4 empty con 0), 3 optimizers RUNNING sin sellar con 0 producer rows, prefijo MinIO `03_optimizer/` sólo `.folder_marker` (ZERO PUTs), builder COMPLETED 20 evidencias; cardinalidad inválida: CERO; retry signals: CERO (todos attempt=1).
- El defecto NO es causado por Slice 2: `TestDBRegister_DurableOptimizerMultipleOutputsFailClosed` (preexistente) demuestra que múltiples outputs del optimizer ya fallaban cerrado en `db_register` antes del gate (y tras subir objetos a MinIO); el gate nuevo adelanta el fallo a upload ANTES de cualquier efecto, estrictamente más seguro. El conflicto es la cardinalidad física de SQX vs la premisa singleton del contrato congelado.
- NO corregir código, NO segunda release, NO re-run, NO Temporal Reset (mandato de la sesión). `PROJECT_STAGE_RECOVERY` queda SIN certificar; `ECHO_FORGE_DURABLE_FOUNDATION_V1` NO se declara.

## Rationale

- La matriz F0–F16 y el mecanismo durable completo se comportaron según contrato: el fallo del golden ES el gate F8 trabajando sobre datos reales; certificar en presencia de este cohort exigiría rebajar el gate o "arreglar" el producto en sesión de certificación, ambos prohibidos.
- La premisa singleton (1 `.sqx` por StageExecution de Optimizer) quedó FALSIFICADA físicamente para estrategias con walk-forward: dos estrategias independientes (4.1.15 en el fallo, 4.1.24 en los archivos preservados) produjeron el segundo artefacto `WF Matrix - `. En 0.2.80 (cohort `example_flow_25`) ningún optimizer lo emitió ⇒ comportamiento dependiente de datos/cohort, no determinista por stage.
- La precedencia de autoridades y write-once quedaron intactos y sin violación alguna durante el incidente (audit de la corrida: MINIO_LIST/STAT/ETAG/SHA-derivado/local-FS como autoridad = ZERO).

## Consecuencias

- NEXT EXACT: `DURABLE-OPTIMIZER-WF-MATRIX-CARDINALITY-RCA-TOP` — debe resolver con evidencia material: (1) por qué el cohort `example_flow_26` genera estrategias cuyo optimizer emite `WF Matrix - *.sqx` (config CFX/generación Builder vs `example_flow_25`); (2) cuál es el contrato autoritativo para ese segundo artefacto (exclusión/clasificación como secondary artifact con semántica de recovery completa, supresión en config del task, o cohort fuera de alcance V1); (3) impacto idéntico en FinalReretester/WFM si aplicara. Después: NEW release no requerida si no hay code change; re-certificación = NEW RequestID/FlowRun con `DURABLE-PROJECT-STAGES-RECOVERY-FAULT-CERTIFICATION-NORMAL` (Part A ya PASS puede citarse; re-ejecutar gates si `origin/master` avanzó).
- La release `0.2.81` queda publicada y en los workers (source autorizado `abe19d0`, sin defecto de recovery); el incidente no invalida los gates 15–20 (release/rollout). Conocimiento durable del defecto: [[optimizer-wf-matrix-second-sqx-output]].
- Código producto cambiado en esta sesión: NONE. Foreign dirty preservado (`deploy/manifest.json`, `go.work.sum`, `input/example/config.json`, `specs/FEAT-SQX-STRATEGY-EVALUATION/fixtures/phase4_performance.json`).

## Alternativas descartadas

- Continuar la certificación ignorando el fallo (declarar PASS parcial): prohibido por el mandato (gate 22 explícito) y por integridad de evidencia.
- Reintentar golden con cohort sin WF (strategy bump manual a un flow "sano"): equivaliría a seleccionar datos para pasar el gate sin resolver la causalidad; el defecto persistiría para cualquier cohort futuro con walk-forward.
- Subir el `WF Matrix` como segundo producer row / secondary artifact en hot-fix: es corrección de producto en sesión de certificación (prohibida) y requiere contrato nuevo (RCA).
- Atribuir a VERSION_SKEW o INFRA: descartado con evidencia — rollout homogéneo verificado por identidad de pollers en el historial completo; el fallo es determinístico respecto a la cardinalidad física del output del optimizer.
