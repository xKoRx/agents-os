---
type: decision
schema_version: 1
scope: project
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
load_policy: when_project_loaded
indexable: true
index_priority: high
tags:
  - kind/decision
  - tech/minio
  - tech/idempotency
  - scope/project
---

# SDK MinIO — create-only atómico

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Contexto

- El wrapper `xKoRx/sdk/pkg/shared/minio/client.go` exponía sólo `PutObject`, que sobrescribe keys; el diseño del artifact plane requiere cerrar la ventana entre evidencia inmutable y bytes físicos mutables.

## Decisión

- Agregar `func (c *Client) PutObjectIfAbsent(ctx context.Context, bucket string, objectName string, reader io.Reader, size int64, metadata map[string]string) error` como API aditiva.
- Construir `minio.PutObjectOptions` con la metadata existente, `SetMatchETagExcept("*")` (`If-None-Match: *`) y `DisableMultipart=true`; mapear HTTP 412 o código `PreconditionFailed` a `errors.Is(err, ErrObjectAlreadyExists)`.
- Mantener `PutObject` overwrite, retry transient, rewind/buffer de readers y resolución same-bytes/different-bytes fuera del SDK, en Symphony.

## Rationale

- La primitive protege que una retry o writer concurrente no reemplace bytes existentes; no decide ACK por digest ni `CONTRACT_CONFLICT`.
- 409/`ConditionalRequestConflict` permanece potencialmente retryable durante una carrera y no se clasifica como existing sin evidencia adicional.
- El soporte de atomicidad server-side depende de MinIO/S3 aplicar el header condicional; esta sesión no hizo smoke live y Symphony no se actualiza.

## Consecuencias

- `StatObject → PutObject` se descarta por TOCTOU; Object Lock/versioning no entrega create-if-absent; multipart queda fuera para esta primitive porque la condición debe acompañar el single PUT materializador.

## Alternativas descartadas

- `StatObject → PutObject` por TOCTOU; Object Lock/versioning por no entregar create-if-absent; multipart por evaluar la condición en el complete y no en el PUT materializador.
