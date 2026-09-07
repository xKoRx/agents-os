---
type: known_error
schema_version: 1
scope: project
created: "2026-08-29"
updated: "2026-08-29"
area: "[[Echo Forge]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[xKoRx/symphony]]"
entities:
  - "[[Echo Forge]]"
related:
  - "[[2026-08-29-durable-artifact-verified-reads-final-e2e-normal]]"
  - "[[2026-08-29-exporter-double-execution-root-cause]]"
aliases:
  - exporter double execution
  - ghost write export_run.json
confidence: verified
load_policy: manual
indexable: true
index_priority: high
tags:
  - kind/known-error
  - scope/project
  - priority/high
---

# 2026-08-29-durable-verified-reads-exporter-double-execution

## Síntoma

Durante el golden run `1e560644-8b39-4ddb-bede-eb2c98e33238` (release 0.2.79, wave `final-verified-reads-e2e-20260829-174450`), la tarea `overview_exporter` produjo dos veces `metadata/export_run.json` con bytes distintos bajo la misma key MinIO: una subida a las 17:48:38Z (job sqx `20260829_174811`, ejecutado 17:48:11→17:48:32 sobre las 20 estrategias del builder) y el intento registrado en el historial (scheduled 17:47:51, started 17:50:51, identity `757811@sqx-ulab-hera-0`). El segundo intento chocó con el write-once: `bytes differ: artifact checksum mismatch` → `CONTRACT_CONFLICT` non-retryable → workflow `Failed`, FlowRun `FAILED`.

## Causa

Cerrada en [[2026-08-29-exporter-double-execution-root-cause]] (RCA read-only 2026-08-29).

- **No hubo escritor fantasma.** El primer PUT provino de un intento anterior de **la misma activity task** (evt 29). Los metadatos `X-Sqx-*` del objeto solo los escribe `upload_results` a partir de `activity.GetInfo(ctx)`, que panica fuera de un contexto de activity; el cuerpo se autoidentifica como `project: EchoForgeOverviewExporter`, `stage: metadata`, con `expected/written = 20` (la cohorte exacta del Builder).
- **La premisa «sin `ActivityTaskStarted`» era una lectura errónea de Temporal.** El servidor escribe ese evento de forma perezosa: uno solo por activity task, al cerrar. Los intentos intermedios no dejan evento, así que la cardinalidad no informa el número de intentos. El historial estaba **completo** (41 eventos, página única, sin filtro); el `attempt` nunca llegó a capturarse (el probe falló a compilar `GetAttempt`), de modo que el `attempt=1` anterior era inferencia, no evidencia.
- **Lo que hace fatal al reintento** es que `EchoForgeOverviewExporter.java` deriva `job_id` y `finished_at` del reloj de pared, así que dos ejecuciones producen artefactos de idéntica longitud (848 B) y distinto SHA-256 bajo la misma key determinista. El error fue `checksum mismatch` y no mismatch de tamaño, lo que prueba que el reintento generó exactamente 848 B.
- El solapamiento del rollout `0.2.79` con el intake (manifest publicado 59 s antes) explica la pérdida del cierre del primer intento, pero **no es la causa**: el defecto se dispara bajo cualquier reintento. El host del primer intento es irrecuperable (SSH rechazado en los tres workers, Loki sin streams, y Temporal no persiste identity de intentos previos) y resulta inmaterial.

## Impacto

- El E2E final `0.2.79` queda BLOCKED / CLOSED. `wfm_exporter` comparte la misma estructura (no durable, artefactos con timestamp de pared) y por tanto el mismo defecto latente.

## Detección

- `ActivityTaskFailed` con `CONTRACT_CONFLICT` no reintentable cuyo mensaje interno es `artifact checksum mismatch` (no size mismatch) sobre una key `.../metadata/export_run.json` ya presente en MinIO.

## Mitigación

- Las tareas exporter no durables (`overview_exporter`, `wfm_exporter`) carecen de execution-intent idempotente (`durableProjectTask` las excluye) y producen artefactos byte-no-deterministas ⇒ cualquier reintento rompe el write-once. La barrera fail-closed actuó **correctamente** (overwrite ZERO, consumer calls ZERO); Artifact Verified Reads sigue `PENDING`, no invalidado.
- WORKAROUND OPERACIONAL: ninguno en runtime. «Evitar reintentos» no es mitigación aceptable.
- FIX REQUERIDO (separado, bajo FIX → NEW RELEASE → NEW REQUEST ID → NEW FLOW RUN): eliminar el `overview_exporter` de nivel superior del golden path durable, reubicando su único efecto lateral con lector real —el `databank_metadata` legacy de la wave, hoy suprimido en el Builder durable por `skipLegacyDatabank` y leído por `evaluate_wfm`/`verify_wfm` y `generate_report`— dentro del `import_metadata` del Builder.
