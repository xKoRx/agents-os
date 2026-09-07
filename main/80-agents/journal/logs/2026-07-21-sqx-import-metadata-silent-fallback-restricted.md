---
type: change_log
scope: session
created: "2026-07-21"
updated: "2026-07-21"
area: "[[Symphony]]"
project: "[[Echo Forge]]"
application: "[[echo-forge]]"
entities:
  - "[[Symphony]]"
related:
  - "[[2026-07-21-sqx-silent-fallback-import-metadata-fix-raw]]"
aliases: []
confidence: verified
source_session: "sqx-1784605033-silent-fallback-fix"
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# Cambio: silent fallback de import_metadata restringido a tasks no-exporter

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `sqx/activities/worker/project_activity.go` (líneas 143-156)
  - `sqx/activities/worker/project_activity_test.go` (nuevo test + import `fmt`)

## Motivo

- Workflow `sqx-main-00_configs-v1-NDX-H1-L-1784605033` falló en `classify_and_rank` con `ErrMetadataMissing` sin causa raíz visible.
- Diagnóstico reveló que el `overview_exporter` corrió en Kronos con `output_count=0` y `sqx_exit_code=0`, y `import_metadata` falló silenciosamente por el graceful fallback.

## Fuentes usadas

- Historia Temporal del workflow (Event 11 ActivityTaskCompleted con `output_count=0`).
- Logs `/var/log/symphony/symphony-worker.log.1.gz` en Zeus indicando `worker=sqx-ulab-kron-0`.
- Query MongoDB `databank_metadata` mostrando run_id de corrida previa, no de la actual.

## Resolución aplicada

- Silent fallback ahora condicionado a `!enableMetadata`.
- Agregado `telemetry.RecordError(ctx, err)` antes de retornar el failure.
- Nuevo test `TestProjectActivity_Execute_ExporterImportMetadataFailure_PropagatesError` cubre el contrato.

## Validación

- `go build ./sqx/activities/... ./sqx/workflows/... ./sqx/cmd/...` → OK.
- `go test ./sqx/activities/worker/ -run TestProjectActivity_Execute_` → PASS (8 tests).
- `go test ./sqx/activities/worker/steps/... ./sqx/activities/worker/... ./sqx/workflows/...` → PASS.
- `go vet ./sqx/activities/worker/...` → limpio.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Reemplazar el bloque `if stepName == "import_metadata" && !enableMetadata` por `if stepName == "import_metadata"` para restaurar el comportamiento anterior.
- Eliminar el test `TestProjectActivity_Execute_ExporterImportMetadataFailure_PropagatesError` y el import `fmt`.
