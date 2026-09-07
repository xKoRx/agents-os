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
  - "[[2026-08-30-durable-optimizer-wf-matrix-cardinality-rca]]"
  - "[[2026-08-30-durable-project-stages-recovery-fault-certification]]"
aliases:
  - DURABLE-OPTIMIZER-OUTPUT-CARDINALITY-CORRECTION-NORMAL
  - optimizer publishable cardinality batch gate
confidence: verified
source_session: DURABLE-OPTIMIZER-OUTPUT-CARDINALITY-CORRECTION-NORMAL
load_policy: manual
indexable: true
index_priority: high
tags:
  - kind/decision
  - scope/project
  - project/echo-forge
---

# 2026-08-30-durable-optimizer-output-cardinality-correction

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Contexto

- Correction sobre `xKoRx/symphony` @ baseline `abe19d09a0bafc7ec21abbf54ca136684e202177` (`HEAD == origin/master` al inicio), implementando la Option A congelada por [[2026-08-30-durable-optimizer-wf-matrix-cardinality-rca]]: el F8 de Slice 2 medía raw local `.sqx` (`len(st.ResultFiles)`) en la capa equivocada; el incidente del golden 0.2.81 (`Strategy_4.1.15.h0`, StageExec `c95a655d…`) materializó el falso conflicto sidecar+databank WF.

## Decisión

- **Batch preflight antes de cardinality:** nuevo puerto `capabilities.BatchPreflightStrategyUploader` — `UploadFromDiskExactWithBatchPreflight(ctx, outputDir, meta, beforeBatch, beforePut)`. El storage sigue siendo la ÚNICA autoridad de publicación: `planExactUploadCandidates` descubre raw local y aplica TODA la semántica existente (discovery recursivo, `UploadPrefixFilter`, normalización `_`/espacio, `ExactOutputName`, duplicados `(N)`, sanitización de ruta y nombre, naming HOST_KEY, `BuildMinIOPath`, digest local con snapshot) para derivar el set COMPLETO de refs publishable; `beforeBatch(refs)` corre UNA vez ANTES del primer producer record y del primer MinIO put; luego cada candidato se revalida como stable file → `beforePut` (record-before-put intacto) → `PutObjectIfAbsent`.
- **F8 redefinido en steps:** `batchGateSingletonPublishableOutputs` cuenta sólo refs `.sqx` del set preflighted — fresh 0 publishable ⇒ empty permitido; fresh 1 ⇒ permitido; >1 ⇒ `CONTRACT_CONFLICT` sin record ni put. Con `ExpectedProducerOutput` (P2B): 0 publishable ⇒ conflicto (nunca CompleteEmpty); 1 ⇒ exige igualdad exacta Store/Bucket/ObjectKey/Size/SHA256 con la autoridad sellada, mismatch ⇒ conflicto ANTES del record per-object (replay call 0); >1 ⇒ conflicto. En `uploadResults` sólo queda el atajo sound raw==0+expected (publishable ⊆ raw).
- **Compatibilidad:** `UploadFromDiskExact` y `UploadFromDiskExactWithPrePut` preservados delegando a la implementación común con batch callback nil (sin copiar el método tres veces); write-once `PutObjectIfAbsent` byte-a-byte intacto; singleton path fail-closed si el storage no implementa el puerto nuevo; Retester/FinalReretester sin cambios (el gate genérico los cubre; `rejectMultipleSQXForExactOutput` intacto para `ExactOutputName`).
- **Congelado:** sin schema, sin migration, sin bump de `sqx-optimizer.v1`, sin CFX change (`DontSaveOriginalStr` NO tocado), sin WFM/Apply changes, sin recovery machine changes; precedencia Results > Evaluation > ProducerOutput > físico intacta; UNKNOWN_COMMIT y reconcile write-once sin cambios. Comentario del package `optimizer/binding` aclarado (cells/NDJSON de WFM no son el producer; el databank WF Matrix `.sqx` seleccionado por `UploadPrefixFilter` SÍ es el `STRATEGY_SQX`) — sólo comentario.
- **Implementación:** commit `6b13c66cf195a83709c156e25aa8dfd6a17c140e` (parent exacto `abe19d0`, push OK, `HEAD == origin/master`), 6 archivos (budget 6/10): capabilities/storage.go, storage-minio/minio_storage.go, storage-minio/pre_put_test.go, steps/steps.go, steps/project_stage_recovery_test.go, optimizer/binding/contract.go. Foreign dirty preservado.

## Rationale

- La garantía exigida — todos los publishables preflighted ANTES del primer record/PUT — sólo es demostrable si quien ve el conjunto completo es el dueño de la clasificación de publicación; un gate en steps sobre raw reintroduciría el defecto y un gate que reimplemente el filtro crearía una segunda semántica de publicación.
- El digest local de TODOS los candidatos en la fase plan no abre TOCTOU material: la revalidación stable-file (`sameFileSnapshot`) cubre mutaciones entre plan y put, mismo mecanismo del flujo preexistente.
- Cambio de conducta aceptado y más seguro: errores de clasificación que antes podían ocurrir tras PUTs parciales ahora abortan con cero escrituras (preflight total antes del primer write).

## Consecuencias

- **PASS CONTRACT 24/24 verificado** (raw N permitido, publishable 0|1 enforced pre-record/pre-put, sidecar nunca publicado, WF Matrix único `STRATEGY_SQX`, expected-converge/conflict, empty fresh, singleton/0|1 intactos, sin schema/migration/bump, WFM/Apply intactos, regresiones Retester/FinalReretester PASS, write-once intacto, autoridad intacta, budget 6≤10, tests PASS, push, HEAD==origin/master).
- **Tests:** A/incidente con storage real (raw 2 → publishable 1 → record 1 → PUT 1 WF-only), C (raw 3/publishable 2 → conflicto 0/0), D (aux-only → 0 writes), E raw>0 publishable 0 (recordCalls 0), F replay-exact converge, G wrong-SHA/different-key conflicto pre-record (recordCalls 0), matriz de gate 8 subtests, regresiones de los 3 stages PASS; suites steps 0.95s / worker 10.2s / storage-minio / bindings PASS; PG targeted `StageProducerOutput|CompleteStageExecution` PASS 61s y concurrencia `SingletonConcurrency|ConcurrentProducerVsEmpty` ×10 PASS 86.6s (PG manual `.txz` + DSN + DB virgen por invocación); compile sweep y vet sin tools exit 0.
- **Fault matrix:** F8 REDEFINIDO rerun PASS (4 escenarios targeted); F0–F7 y F9–F16 de Part A (abe19d0) permanecen citables — recovery mechanics sin cambios.
- **No declarar** PROJECT_STAGE_RECOVERY ni ECHO_FORGE_DURABLE_FOUNDATION_V1: falta recertificación física.
- NEXT EXACT: `DURABLE-PROJECT-STAGES-RECOVERY-PHYSICAL-RECERTIFICATION-NORMAL` (NEW RELEASE desde `6b13c66` + NEW RequestID/FlowRun/Workflow/RunID + golden completo con F8 publishable).

## Alternativas descartadas

- **Eliminar el gate sin preflight:** aceptaría descubrir un segundo publishable después del primer record/PUT — viola la garantía de seguridad del mandato.
- **Steps reimplementa el prefix filter:** dos implementaciones de publication semantics — prohibido por el mandato y por el RCA.
- **`DontSaveOriginalStr=true`:** higiene opcional del CFX, no corrige la capa del gate ante leftovers futuros.
- **Multi-artifact Optimizer / schema nuevo / contract bump:** el sidecar es transient sin consumidor durable; B/D del RCA siguen rechazadas.
