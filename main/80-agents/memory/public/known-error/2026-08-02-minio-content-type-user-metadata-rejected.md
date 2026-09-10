---
type: known_error
scope: project
created: 2026-08-02
updated: 2026-08-02
area: "[[Echo]]"
project: "[[Echo Forge - Trade List Export Contrato Remoto]]"
application: "[[symphony]]"
entities:
  - "[[Echo Forge]]"
  - "[[Echo Forge - Trade List Export Contrato Remoto]]"
related:
  - "[[2026-08-02-minio-nosuchkey-misclassified-as-transient]]"
aliases:
  - minio content-type user metadata
  - unsupported user defined metadata name
confidence: verified
source_session: cursor-6ded3437-echo-forge-trade-list-close-2026-08-02
load_policy: when_error_matches
indexable: true
index_priority: high
tags:
  - kind/known-error
  - project/echo-forge
  - area/echo
  - tech/minio
  - scope/project
---

# MinIO rechaza Content-Type en UserMetadata

## Síntoma

- Tras pasar el Stat de idempotencia: `put …trades.manifest.json: Content-Type unsupported user defined metadata name`.
- Falla en todas las tasks `trade_list_exporter` al subir el sidecar.

## Causa

- `objMetaForManifest` incluía `"Content-Type": "application/json"` en el mapa pasado a `PutObject`.
- SDK metía todo el mapa en `PutObjectOptions.UserMetadata` y fijaba `ContentType` aparte a `application/octet-stream`.
- S3/MinIO prohíben headers HTTP estándar como nombres de user-metadata.

## Fix

- Adapter: user-metadata solo `x-sqx-*`; `Content-Type` vía parámetro de `putBytes`.
- SDK: `splitPutObjectMetadata` extrae `Content-Type`/`Content-Encoding` a options.
- Desplegado en worker `0.2.30`.

## Detección

- Error Temporal con `unsupported user defined metadata name` en put del `.trades.manifest.json`.
