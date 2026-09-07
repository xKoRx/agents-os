---
type: agent_run
schema_version: 1
scope: session
created: "2026-08-30"
updated: "2026-08-30"
area: "[[Echo Forge]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[xKoRx/symphony]]"
entities:
  - "[[Echo Forge]]"
  - "[[AGENTS OS]]"
related:
  - "[[2026-08-30-durable-optimizer-wf-matrix-cardinality-rca]]"
  - "[[2026-08-30-zcode-glm-5-3-flash-project-stages-recovery-fault-certification]]"
  - "[[embedded-postgres-maven-dns-timeout]]"
aliases: []
agent_surface: "[[ZCode]]"
agent_model: GLM-5.3-Flash
model_source: builtin:zai-coding-plan/GLM-5.3-Flash
task_type: coding
task_complexity: high
outcome: success
verification: verified
evaluator: agent
user_rework: unknown
source_session: DURABLE-OPTIMIZER-OUTPUT-CARDINALITY-CORRECTION-NORMAL
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/agent-run
  - scope/session
---

# Agent Run — 2026-08-30-zcode-glm-5-3-flash-optimizer-output-cardinality-correction

## Trabajo

- **Objetivo:** corregir el cardinality gate F8 de Slice 2 sobre `xKoRx/symphony` @ `abe19d0` para que el contrato 0|1 se aplique a PUBLISHABLE outputs (clasificación de publicación del storage) y no a raw local `.sqx` files (SQX del Optimizer deja sidecar original + `WF Matrix - <strategy>.sqx`; con `UploadPrefixFilter=WF_Matrix` sólo el databank WF es publishable). Option A congelada por el RCA: filter/classify before cardinality; sin multi-artifact, sin schema, sin contract bump, sin CFX change, sin WFM/Apply/FinalReretester changes.
- **Alcance atribuible a esta combinación superficie×modelo:** nuevo puerto `capabilities.BatchPreflightStrategyUploader` (`UploadFromDiskExactWithBatchPreflight(ctx, dir, meta, beforeBatch, beforePut)`); refactor del exact uploader en `minio_storage.go` a plan/preflight/publish (`planExactUploadCandidates` aplica TODA la semántica de publicación existente — discovery recursivo, prefix filter, `_`/space normalization, ExactOutputName, duplicados `(N)`, sanitización, HOST_KEY naming, BuildMinIOPath, digest local — y deriva el set COMPLETO de refs antes de cualquier remote write; `beforeBatch` corre una vez con el set completo ANTES del primer record/PUT; `UploadFromDiskExact`/`UploadFromDiskExactWithPrePut` delegan a la implementación común con callbacks nil, write-once byte-a-byte intacto); en `steps.go` el gate raw `len(ResultFiles)>1` se REEMPLAZA por `batchGateSingletonPublishableOutputs` (0 publishable fresh = empty permitido; con `ExpectedProducerOutput` = conflicto; 1 publishable con expected exige ref exacto Store/Bucket/Key/Size/SHA256 o conflicto ANTES del record per-object; >1 publishable = CONTRACT_CONFLICT) conservando sólo el atajo sound raw==0+expected en `uploadResults` (publishable ⊆ raw); record-before-put per-candidate preservado (`recordSingletonProducerOutput`); comentario del package `optimizer/binding` aclarando que cells/NDJSON de WFM no son el producer y que el databank WF Matrix `.sqx` SÍ es el `STRATEGY_SQX` (sólo comentario, sin bump de `sqx-optimizer.v1`).
- **Artefactos afectados:** 6 archivos (budget 6/10): `core/capabilities/storage.go` (+14), `adapters/storage-minio/minio_storage.go` (+102/−94), `adapters/storage-minio/pre_put_test.go` (+119), `activities/worker/steps/steps.go` (+57/−17), `activities/worker/steps/project_stage_recovery_test.go` (+125/−19), `adapters/optimizer/binding/contract.go` (+7/−7 comentario). Commit `6b13c66cf195a83709c156e25aa8dfd6a17c140e` (parent exacto `abe19d09a0bafc7ec21abbf54ca136684e202177`, push OK, `HEAD == origin/master`). Foreign dirty preservado sin stagear (deploy/manifest.json 0.2.81, go.work.sum, input/example/config.json, fixture phase4).

## Evidencia

- **Validaciones ejecutadas (tests A–M del mandato):** A/incidente raw 2 (`sidecar.sqx` + `WF Matrix - …4.1.24.h0.sqx`) / publishable 1 → batch ve exactamente la ref WF Matrix con backend vacío, record 1, PUT 1, sidecar ausente en storage bajo cualquier key (`OptimizerSidecarFilteredBeforeCardinality`, storage REAL); B ordering batch → record → PUT asertado por contadores y backend vacío en ambos hooks; C raw 3 / publishable 2 → CONTRACT_CONFLICT con 0 records y 0 PUTs; D raw aux-only / publishable 0 → 0 writes, vacío permitido; E expected+zero publishable → conflicto (variante raw==0 preexistente + variante raw>0 vía publicable-only-nueva con recordCalls 0 y 0 puts); F expected+exact → converge con replay ACK + PUT 1 (`ProducerRowMissingObjectRegeneratesExactAndSeals` PASS en los 3 stages); G expected+wrong SHA y different key → conflicto ANTES del record per-object (recordCalls 0, asertado nuevo); H cubierto por different-key del batch gate; I/J regresión Retester/FinalReretester en los 3 stages PASS (`MultiplePhysicalOutputsConflictBeforeRecord` ahora vía batch gate, adaptado a `uploadStrategyResults` directo porque el gate raw ya no corta antes de `activity.GetInfo`); K/L legacy + write-once intactos (`NilCallbackPreservesWriteOnce`, pre-put hooks, write_once tests sin cambios); M recovery: matriz gate directa (`TestBatchGateSingletonPublishableOutputs` 8 subtests) + suites de recovery completas PASS.
- **Suites:** steps 0.95s PASS, worker 10.2s PASS, storage-minio PASS, optimizer/retester binding PASS; PG targeted `-run 'StageProducerOutput|CompleteStageExecution'` PASS 61s y concurrencia `-run 'SingletonConcurrency|ConcurrentProducerVsEmpty' -count=10` PASS 86.6s (PG manual desde `.txz` cacheado + `TEST_POSTGRES_DSN` + DB virgen por invocación, sin SHM issues); compile sweep `./sqx/...` sin tools exit 0; vet sin tools exit 0.
- **Resultado observable:** raw N permitido; publishable 0|1 enforced en la capa de publicación ANTES del primer producer record y del primer MinIO PUT; el incidente del golden 0.2.81 (2 raw .sqx del Optimizer) queda demostrado PASS en test con storage real; StageProducerOutput singleton, Evaluation 0|1, precedence Results > Evaluation > Producer > físico, write-once, UNKNOWN_COMMIT y PutObjectIfAbsent sin cambios funcionales.
- **Limitaciones de la evidencia:** sin E2E físico ni release (mandato: correction termina en code+tests+commit+push; recertificación física es sesión separada); F0–F7 y F9–F16 de Part A permanecen citables (recovery mechanics intactos) y F8 queda REDEFINIDO (rerun cubierto por los 4 escenarios targeted); `sqx/workflows` 24 fixtures y `sqx/tools` no reabiertos (baseline ajeno).
