---
type: decision
schema_version: 1
scope: project
created: "2026-08-28"
updated: "2026-08-28"
area: "[[Echo Forge]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[xKoRx/symphony]]"
entities:
  - "[[Echo Forge]]"
  - "[[AGENTS OS]]"
related:
  - "[[durable-verified-reads-apply-reconcile-infers-digest-from-key]]"
  - "[[2026-08-28-durable-artifact-verified-reads-final-e2e-normal]]"
  - "[[2026-08-27-durable-artifact-verified-reads-rca]]"
aliases: []
confidence: verified
source_session: DURABLE-ARTIFACT-VERIFIED-READS-APPLY-RCA-TOP
load_policy: manual
indexable: true
index_priority: high
tags:
  - kind/decision
  - scope/project
---

# 2026-08-28-durable-verified-reads-apply-reconciliation-rca

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Contexto

- RCA/DESIGN read-only sobre `xKoRx/symphony` @ `5e93c7cda3f4fcc825f3939a951247cd4e63fec2` (== origin/master; foreign dirty preservado) + SDK pin `v0.0.0-20260827204048-ea09cc1bb8b3`; blocker `durable-verified-reads-apply-reconcile-infers-digest-from-key` tras certificación 0.2.78 BLOCKED.
- `ReconcileApplySelectedRun` (`sqx/adapters/storage-minio/apply_selected_run.go:26-50`) fabrica el `DurableArtifactRef` esperado desde `StatObject` + `GetObject` + SHA de los bytes almacenados; único caller productivo `durable_apply_selected_run.go:318`.
- El gap material: physical write ACK → crash → retry encuentra objeto en MinIO sin Evaluation que entregue expected Size/SHA (`EvaluationRef` es determinística y NO incluye el artifact, `evidence.go:78`; el artifact sólo vive en `Artifacts[]` del content → `PayloadDigest`).

## Decisión

- La autoridad esperada independiente para reconciliación Apply pre-Evidence es un **registro de salida del productor en el Control Plane (PG)**, INSERT-only, escrito desde el cómputo del productor (`physical.Apply` → SHA/Size) ANTES del write MinIO: nueva tabla `sqx.stage_producer_outputs` (migration 008 aditiva) + puerto estrecho `StageProducerOutputStore/Reader` (precedente `OutputNamespaceOwnershipStore`).
- Para todo estado con Evaluation existente (C9/C10/C11) la autoridad es la **Evaluation inmutable direccionada por `EvaluationRef` determinística** (helper `BuildEvaluationRef` en binding): recovery short-circuit carga evidence exacta, verifica el objeto contra el ref (verified read), NO ejecuta SQX, y completa idempotentemente (`CompleteStageExecution` ya es replay-safe con `EqualEvaluationRefSet`, `stage_execution.go:140-156`).
- `ReconcileApplySelectedRun` se ELIMINA del path durable (y de la interfaz): el reconcile ES el write-once put (`putObjectIfAbsentAndReconcile` ya verifica el objeto existente contra el ref del caller, `write_once.go:36-87`); producción ausente → re-produce + put; ref divergente bajo objeto existente → CONTRACT_CONFLICT.
- Contrato del registro: INSERT-only first-computation-wins; mismo ref → ACK idempotente; ref distinto → CONTRACT_CONFLICT; registro presente + objeto ausente → re-produce y put si coincide, si no CONTRACT_CONFLICT (fail-closed tipo test 8). UNKNOWN_COMMIT del put se resuelve en retry vía verificación exacta contra el registro.

## Rationale

- `stage_execution_results` NO sirve: links-only `(stage_execution_id, evaluation_ref)` sellados en la tx de `CompleteStageExecution` (`stage_execution.go:171-182`), sin campos de artifact, sin camino de escritura pre-producción; extenderla rompería el contrato v1 compartido por 6 bindings.
- Option C (re-produce como autoridad) queda descartada como primaria: veredicto **BYTE_DETERMINISTIC_NOT_PROVEN** con indicación fuerte de no-determinismo — el `.sqx` es ZIP/JAR generado por `sqcli` (Java externo) con timestamps DOS por entrada (muestra real `docs/*.sqx` entries 08-19-2025) y precedente empírico Retester +2 bytes (56664 vs 56662); re-producción divergente fabricaría un expected falso o envenenaría el stage.
- Option D (metadata MinIO) comparte fate con los bytes (misma PUT) — es exactamente el defecto a cerrar. Reordenar evidence-antes-objeto queda descartado: el evidence plane registraría `Status: APPLIED` de un artifact inexistente (evidencia de intención, no de hecho).
- El registro PG es epistémicamente correcto: estado operacional mutable pre-sello pertenece al control plane (precedente lifecycle FlowRun/claims); es independiente de MinIO (store distinto, escrito desde bytes del productor, jamás desde storage reads); y cierra C5/C6/C7/C8 recuperando el ref original exacto sin re-ejecutar SQX.

## Consecuencias

- La ventana residual no elimiable: registro escrito + put no intentado/completado + productor no determinista → retry re-produce divergente → CONTRACT_CONFLICT fail-closed (ventana de ms; remedio business reprocess). La corrección NO depende del byte-determinism; el determinismo sólo mejora recuperación silenciosa (experimento físico especificado para certificación en worker host).
- Change surface ~9-10 archivos (migration 008 up/down, capabilities port, adapter PG, activity, binding helper, storage adapter sin reconcile, wiring main.go, tests adapter/contract/fakes); dentro del hard max 14.
- Frozen contracts intactos: PG control plane / Mongo evidence / MinIO artifact / Temporal no business DB / DurableArtifactRef physical authority / write-once first-bytes-win / StrategyRef conservado / StageExecution identity por intent / namespace ownership / retry técnico mismo StageExecution.
- NEXT EXACT `DURABLE-ARTIFACT-VERIFIED-READS-APPLY-CORRECTION-NORMAL`; el E2E físico posterior debe incluir el experimento de determinismo (2 corridas ≥90s de separación, diff SHA + `zipinfo -v` por entry) y fault injection en los boundaries C5/C6/C8.

## Alternativas descartadas

- Option A sola (Evaluation como authority): no cubre C8 — la Evaluation no existe en esa ventana; se adopta sólo como authority post-Evidence vía short-circuit determinista.
- Option B sobre entidad existente (forzar `stage_execution_results`): semánticamente incorrecta (result-sellado, links-only); tabla nueva es la forma mínima honesta.
- Option C como authority primaria: depende de determinismo no probado y empíricamente improbable.
- Option D (metadata/ETag): autoridad que comparte fate con los bytes; contrato congelado lo prohíbe.
- Reorden evidence-antes-put: convierte evidence en intent; rompe la semántica de plano de hechos inmutables.
