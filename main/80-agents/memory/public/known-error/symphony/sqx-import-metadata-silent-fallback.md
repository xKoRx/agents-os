---
type: known_error
scope: application
created: "2026-07-21"
updated: "2026-07-21"
area: "[[Symphony]]"
project: "[[Echo Forge]]"
application: "[[echo-forge]]"
entities:
  - "[[Symphony]]"
related: []
aliases:
  - ErrMetadataMissing downstream sin causa raíz visible
  - classify_and_rank falla con ErrMetadataMissing después de exporter exitoso
  - import_metadata graceful fallback oculta fallo de plugin Java
confidence: high
source_session: "sqx-1784605033-silent-fallback-fix"
load_policy: when_error_matches
indexable: true
index_priority: high
tags:
  - app/echo-forge
  - app/echoforge
  - area/symphony
  - kind/knownerror
  - project/echo-forge
  - project/echoforge
  - scope/application
---

# SQX Silent Fallback en import_metadata oculta fallos del plugin Java

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Síntoma

- Un workflow `GenericSQXWorkflow` falla en el activity `classify_and_rank` con `ErrMetadataMissing` (`metadata missing for wave`, non-retryable).
- El activity previo `overview_exporter` (o `wfm_exporter`) aparece como `COMPLETED` con `status=ok` y `sqx_exit_code=0` en Temporal.
- En MongoDB `databank_metadata` **no existen documentos** con el `run_id` (TraceID) de esa corrida; sólo aparecen de corridas previas.

## Causa

- En `sqx/activities/worker/project_activity.go`, el loop del pipeline detectaba errores del step `import_metadata` y los tragaba con `continue` + `WARN`, sin distinguir si la task era exporter o no.
- Como resultado, si el plugin Java del exporter escribía 0 documentos (por ejemplo, porque las estrategias descargadas no eran procesables, o el exporter encontraba un edge case y terminaba sin output), la activity reportaba éxito.
- El pipeline continuaba hasta `classify_and_rank`, que al no encontrar documentos lanzaba `ErrMetadataMissing`, ocultando que la causa raíz estaba varios pasos atrás.

## Impacto

- Workflows SQX fallan con un error que **no indica la causa raíz**, dificultando debugging.
- El sintoma aparenta ser del clasificador/ranker cuando en realidad es del exporter o del plugin Java.
- Costo alto de investigación por run (Timestamps, Multiple workers, MinIO, MongoDB, Temporal history).

## Detección

- Workflow `GenericSQXWorkflow` falla con `ErrMetadataMissing` en `classify_and_rank`.
- En la historia de Temporal, el activity previo tipo `overview_exporter` o `wfm_exporter` figura `COMPLETED` con `output_count=0` y `keys=[]`.
- En MongoDB, query `databank_metadata` por `run_id = <trace_id_del_workflow>` retorna 0 documentos.

## Mitigación

Aplicada en `sqx/activities/worker/project_activity.go` (versión posterior a v0.1.126):

- El silent fallback de `import_metadata` ahora **sólo aplica cuando el task NO es exporter** (`!enableMetadata`).
- Cuando la task es `overview_exporter`, `wfm_exporter`, o `project` con `MetadataExport=true`, el error se propaga con `telemetry.RecordError` y la activity retorna failure.
- Test de regresión: `TestProjectActivity_Execute_ExporterImportMetadataFailure_PropagatesError`.

## Evidencia

- Workflow de referencia: `sqx-main-00_configs-v1-NDX-H1-L-1784605033` (namespace `sqx-prop`).
- Log Zeus: `/var/log/symphony/symphony-worker.log.1.gz` (2026-07-20 23:37:35 – 23:38:05 UTC-3).
- Plugin Java ejecutado en worker `sqx-ulab-kron-0` con `output_count=0`.
