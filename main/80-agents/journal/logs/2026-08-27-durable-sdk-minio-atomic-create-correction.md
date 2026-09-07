---
type: change_log
schema_version: 1
scope: session
created: "2026-08-27"
updated: "2026-08-27"
area: "[[Echo Forge]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application:
entities: []
related: []
aliases: []
confidence: verified
source_session: DURABLE-SDK-MINIO-ATOMIC-CREATE-CORRECTION-NORMAL
source_feedbacks:
  - "[[2026-08-27-durable-sdk-minio-atomic-create-correction-session-feedback]]"
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-08-27-durable-sdk-minio-atomic-create-correction

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `repo: xKoRx/sdk` · `pkg/shared/minio/client.go`
  - `repo: xKoRx/sdk` · `pkg/shared/minio/client_retry_test.go`
  - `repo: xKoRx/sdk` · `pkg/shared/minio/client_create_only_test.go`
  - `repo: xKoRx/sdk` · `pkg/shared/minio/README.md`

## Motivo

- Implementar la primitive congelada de create-only antes de la integración durable en Symphony, sin cambiar el pin ni el código de Symphony.

## Fuentes usadas

- Diseño previo en `Echo Forge - Arquitectura de Datos y Migración de Persistencia`, baseline SDK `2e5fa11fe9ccd628a075e00fc4b30fe1b60be486` y minio-go v7.0.95.

## Resolución aplicada

- `PutObjectIfAbsent` reutiliza `splitPutObjectMetadata`, semaphore, timeout y retry; configura `If-None-Match:*` y `DisableMultipart=true`; 412/`PreconditionFailed` retorna `ErrObjectAlreadyExists`; `PutObject` conserva overwrite.

## Validación

- Tests nuevos wire/retry PASS; `go vet ./pkg/shared/minio/...` PASS; `git diff --check` PASS; suite completa del paquete y `go test ./...` quedan degradadas por fallos preexistentes fuera de esta superficie, documentados en el checkpoint.

## Compartibilidad

- **Scope:** local / team
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Commit SDK `ea09cc1bb8b34e661c8f31f887dce58613b0475a` publicado en `origin/master`; notas append-only y cambio SDK reversible por revert del commit autorizado.
