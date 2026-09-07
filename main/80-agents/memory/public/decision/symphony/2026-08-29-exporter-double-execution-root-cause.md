---
type: decision
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
  - "[[2026-08-29-durable-verified-reads-exporter-double-execution]]"
  - "[[2026-08-29-durable-artifact-verified-reads-final-e2e-normal]]"
  - "[[2026-08-27-durable-artifact-plane-write-once-final-e2e]]"
aliases:
  - exporter double execution root cause
  - RCA overview_exporter CONTRACT_CONFLICT
confidence: verified
source_session: c6fb690d-88af-4e9d-88d0-f416d9d033e5
load_policy: manual
indexable: true
index_priority: high
tags:
  - kind/decision
  - scope/project
  - priority/high
---

# 2026-08-29-exporter-double-execution-root-cause

RCA read-only del bloqueo del E2E final `0.2.79` (FlowRun `1e560644-8b39-4ddb-bede-eb2c98e33238`, workflow `sqx-main-v1-d3e8faf5-8dd3-4f0e-9889-b44460086e1d`). No se modificó código, no se re-ejecutó nada.

## Contexto

- La premisa de la sesión anterior — «subida fantasma **sin** `ActivityTaskStarted`» — descansaba en una lectura incorrecta de la semántica de Temporal, no en un hueco de evidencia.
- El historial Temporal recuperado es **completo**: 41 eventos, una sola página (`MaximumPageSize: 200`), `HISTORY_EVENT_FILTER_TYPE_ALL_EVENT`. No hubo paginación ni filtrado.
- El campo `attempt` del evento fallido **nunca se capturó** (el probe falló a compilar `GetAttempt`); la afirmación previa `attempt=1` era una inferencia de cardinalidad de eventos, no evidencia.

## Decisión

**Causa raíz.** El `overview_exporter` de nivel superior es una tarea **no durable** (excluida de `durableProjectTask`, sin `StageExecution` ni execution-intent) cuyos artefactos son **byte-no-deterministas por construcción**: `EchoForgeOverviewExporter.java` deriva `job_id` de `new SimpleDateFormat("yyyyMMdd_HHmmss").format(new Date())` y `finished_at` de `new Date()` en cada corrida. Bajo la semántica *at-least-once* de Temporal con `RetryPolicy.MaximumAttempts: 0`, un segundo intento legítimo regeneró `metadata/export_run.json` con **la misma longitud (848 B)** y **distinto SHA-256** sobre la misma key determinista, y el write-once del artifact plane falló cerrado con `CONTRACT_CONFLICT` (no reintentable) → workflow `Failed`, FlowRun `FAILED`.

**Atribución del primer PUT (17:48:38.483Z).** Fue producido por un intento anterior **de la misma activity task** encolada en el evento 29, no por un proceso externo:

1. Los metadatos del objeto (`X-Sqx-Workflow-Id = sqx-main-v1-d3e8faf5-…`, `X-Sqx-Task-Folder = metadata`, `X-Sqx-Wave`, `X-Otel-Trace-Id`) solo los escribe `upload_results`, que los deriva de `activity.GetInfo(ctx)`; el SDK de Go **panica** fuera de un contexto de activity ⇒ el escritor estaba dentro de una activity de este workflow.
2. El cuerpo del objeto se autoidentifica: `project: "EchoForgeOverviewExporter"`, `stage: "metadata"`, `output_dir: /home/kor/sqx/user/projects/EchoForgeOverviewExporter/overview`. El Builder durable usa el proyecto `custom` y subió su propio `export_run.json` a `01_builder/` a las 17:47:50.
3. `expected_count = written_count = 20` = la cohorte exacta del Builder, que es el `source_folder` del exporter.
4. La config tiene **una** tarea `overview_exporter` y el workflow la encola **una** vez (evt 29). Ninguna otra activity del historial puede producir esa key.
5. Cronología coherente: evt 29 encolado 17:47:51.083; el job SQX arranca 17:48:11 (20 s de cleanup + descarga de 20 `.sqx`), termina 17:48:32Z, y los tres objetos suben 17:48:38.483–38.800.

**Semántica de Temporal (por qué no hay evento del primer intento).** El servidor escribe `ActivityTaskStarted` de forma perezosa: un único evento por activity task, materializado al cerrar (completed/failed/timed-out definitivo). Los intentos intermedios no dejan evento. Por lo tanto «un `Scheduled` + un `Started`» **no** implica un solo intento; la cardinalidad de eventos no lleva información sobre el número de intentos. El evento 30 (`17:50:51.895`, identity `757811@sqx-ulab-hera-0`) registra el **último** intento, no el primero.

**Prueba de que ambos artefactos tienen igual tamaño y distinto digest.** `VerifyArtifactStream` compara primero tamaño y solo entonces SHA-256. El error fue `artifact checksum mismatch`, no un mismatch de tamaño ⇒ el `export_run.json` regenerado por el reintento también medía exactamente 848 B. Esto descarta cualquier hipótesis de contenido estructuralmente distinto y confirma que la única diferencia son los campos derivados del reloj.

**Veredicto sobre el write-once.** `CORRECTO`. Actuó como barrera fail-closed frente a una escritura no idempotente; `Overwrite = ZERO`, `consumer calls = ZERO`. Artifact Verified Reads sigue `PENDING`, no invalidado.

## Rationale

Matriz de candidatos evaluada contra la evidencia recuperada:

| # | Candidato | Veredicto |
|---|---|---|
| A | El historial Temporal estaba incompleto | **RECHAZADO** — 41 eventos, página única, sin filtro. Lo incompleto fue la *interpretación*, no la captura |
| B | Doble ejecución real por reintento de Temporal | **PROBADO** — mecanismo demostrado por (1)–(5) más la semántica de escritura perezosa |
| C | Otro workflow o activity invocó el exporter | **RECHAZADO** — el objeto porta el WorkflowID de este flujo y solo existe una tarea exporter |
| D | Invocación directa fuera de Temporal (script, manual, watcher) | **RECHAZADO** — `GetInfo` panica fuera de activity; el watcher local no registra actividad después de 17:47:26 |
| E | Workspace compartido `EchoForgeOverviewExporter/` atribuyendo output ajeno | **RECHAZADO como causa** — el Builder escribe en `custom/overview`. Riesgo real subsistente: el directorio no está aislado entre activities concurrentes del mismo worker |
| F | Output rancio sobreviviente al cleanup | **RECHAZADO** — `CleanProjectDatabanks` limpia `overview/` antes de correr y el plugin usa `clear_output: true`; además el `job_id` del objeto es posterior al encolado |
| G | Proceso asíncrono de SQX que subió tarde | **RECHAZADO** — `ExecuteAndWait` es síncrono y `finished_at` precede a la subida por 6 s dentro del orden de pasos de una sola activity |
| H | El hop `overview_exporter` top-level es brownfield sin consumidor durable | **PROBADO como hallazgo arquitectónico** — Classification y Early Ranking consumen la evidencia inline del Builder; ningún lector sostiene un `DurableArtifactRef` a `metadata/export_run.json` |
| I | Ausencia de idempotencia/recovery a nivel de ejecución para tareas no durables | **PROBADO — CAUSA RAÍZ** |
| J | Rollout de `0.2.79` solapado con el flujo (Kronos sin rotar) | **NO CAUSAL, CONTRIBUYENTE** — el manifest se publicó 59 s antes del intake y los reinicios del stager explican la pérdida del cierre del primer intento, pero el defecto se dispara bajo *cualquier* reintento |

Qué host ejecutó el primer intento queda **UNKNOWN y es irrecuperable**: nunca hubo acceso a logs de worker (SSH rechazado en los tres hosts, Loki sin streams) y Temporal no persiste la identity de intentos anteriores. Es inmaterial: el defecto es determinista y no depende del host.

## Consecuencias

- El E2E final `0.2.79` queda **BLOCKED / CLOSED**; no se recertifica hasta corregir el hop.
- `wfm_exporter` comparte exactamente la misma estructura (no durable, artefactos con timestamp de pared) ⇒ mismo defecto latente.
- Recomendación única: **eliminar el `overview_exporter` de nivel superior del golden path durable**, con una precondición estrecha y verificable — hoy es el **único** escritor del `databank_metadata` legacy de la wave, porque el Builder durable lo suprime (`skipLegacyDatabank` se activa cuando hay `StageExecutionRef` + evidencia). `evaluate_wfm`/`verify_wfm` (resolución de `logical_type`) y `generate_report` (Direction/Timeframe) leen esa colección. El fix debe reubicar ese único efecto lateral dentro del `import_metadata` del Builder durable, que ya parsea el mismo `overview.ndjson`. El marcador `export_runs` del exporter no tiene lector y se descarta. Sin cambio de esquema, sin migración, sin autoridad nueva.
- Si el owner decide conservar el hop por razones brownfield, entonces es obligatorio dotarlo de idempotencia a nivel de ejecución (key con scope de intento o dedup por execution-intent). «Evitar reintentos» no es una mitigación aceptable: los reintentos son parte del contrato de Temporal.

## Alternativas descartadas

- **Convertir el exporter en stage durable.** `StageProducerOutput` está atado por FK a `stage_executions` y el exporter no tiene subject de estrategia; exigiría extender el modelo para una tarea que además no tiene consumidor. Desproporcionado.
- **Reutilizar `ExportRun` de Mongo como autoridad de recovery.** Es un upsert marcador (`ReplaceOne` por `wave_key + stage + exporter`), no autoridad de artefactos; no permite reconstruir ni saltar la subida.
- **Crear una autoridad nueva de producer-output para tareas no durables.** Fundación genérica para un caso que se resuelve eliminando el caso. Rechazado por YAGNI.
- **Aislar el workspace por ejecución.** Corrige un riesgo real de concurrencia pero no toca la no-determinación de los bytes; el conflicto se reproduciría igual.
- **Sacar los artefactos del exporter del alcance del write-once.** Sería reabrir una decisión congelada ([[2026-08-27-durable-artifact-plane-write-once-final-e2e]]) para acomodar una escritura no idempotente. Se registra como challenge, no como recomendación.
