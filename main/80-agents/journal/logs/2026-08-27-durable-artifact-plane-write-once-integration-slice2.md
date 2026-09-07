---
type: change_log
schema_version: 1
scope: session
created: "2026-08-27"
updated: "2026-08-27"
area: "[[Echo Forge]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[xKoRx/symphony]]"
entities:
  - "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
related: []
aliases: []
confidence: verified
source_session: DURABLE-ARTIFACT-PLANE-WRITE-ONCE-INTEGRATION-SLICE2-NORMAL
source_feedbacks:
  - "[[2026-08-27-durable-artifact-plane-write-once-integration-slice2-session-feedback]]"
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# Slice 2 write-once de Artifact Plane — cierre de implementación

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `sqx/adapters/storage-minio/artifact_store.go`
  - `sqx/adapters/storage-minio/artifact_store_test.go`
  - `sqx/adapters/storage-minio/minio_storage.go`
  - `sqx/adapters/storage-minio/minio_storage_test.go`
  - `sqx/cmd/sqx-mt5-worker/main.go`
  - `sqx/cmd/sqx-worker/main.go`
  - `10-projects/Echo Forge/agentes/Echo Forge - Arquitectura de Datos y Migración de Persistencia.md`
  - `10-projects/Echo Forge/Echo Forge.md`

## Motivo

- Cerrar los dos writers durable MT5 restantes y eliminar la inyección productiva del writer legacy, conservando la semántica frozen de Slice 1 y el SDK pin existente.

## Fuentes usadas

- Baselines: Symphony `8619a50`, SDK `ea09cc1` / pin `v0.0.0-20260827204048-ea09cc1bb8b3`; RCA Slice 2 y contrato compartido `write_once.go`.

## Resolución aplicada

- `UploadArtifactFromPath` y `PutObjectFromPath` fueron migrados a pre-hash/stable-file/create-only/reconcile; el worker MT5 delega en `*storageminio.Storage`; `sqx-worker` dejó de inyectar `TradeListStorage`; se agregaron regresiones para same/different bytes, same-size conflict y formato SHA público.

## Validación

- Tests focalizados y race PASS; vet PASS; smoke MinIO real H1–H4 PASS bajo `write-once-slice2/0c571236-8607-41b0-a9e6-9674b5185f1c/`; commit `5e3c2b3` pushed con HEAD == origin/master. Broad suite sólo conserva blockers baseline conocidos.

## Compartibilidad

- **Scope:** team
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- No se modificaron `write_once.go`, SDK, schema, migraciones ni foreign dirty. Rollback de código: revertir commit `5e3c2b3`; rollback de memoria: retirar este log y los enlaces de checkpoint correspondientes.
