---
type: change_log
scope: project
created: 2026-08-02
updated: 2026-08-02
area: "[[Echo]]"
project: "[[Echo Forge - Trade List Export Contrato Remoto]]"
entities:
  - "[[Echo Forge]]"
  - "[[Echo Forge - Trade List Export Contrato Remoto]]"
  - "[[2026-08-02-minio-nosuchkey-misclassified-as-transient]]"
  - "[[2026-08-02-minio-content-type-user-metadata-rejected]]"
source_session: cursor-6ded3437-echo-forge-trade-list-close-2026-08-02
indexable: true
index_priority: medium
tags:
  - kind/changelog
  - project/echo-forge
  - area/echo
---

# Change log — trade_list MinIO Stat/Put (2026-08-02)

## Qué cambió

- **symphony** `sqx/adapters/storage-minio/trade_lists.go`: clasificador `isMinIONoSuchKey`; `objMetaForManifest` sin headers HTTP.
- **sdk** `pkg/shared/minio/client.go`: `StatObject`, `statusCodeOf` tipado, `withRetry` sin 404, `splitPutObjectMetadata` en `PutObject`.
- Releases worker: `0.2.29` (Stat) → `0.2.30` (Put metadata). SHA `0.2.30` = `f52e7bc4…ccd24c345` en Zeus/Hera/Kronos.
- Flujos de verificación: `example_flow_66` / `example_flow_67`.

## Artefactos de memoria

- [[2026-08-02-minio-nosuchkey-misclassified-as-transient]]
- [[2026-08-02-minio-content-type-user-metadata-rejected]]

## Repo / branch

- `symphony`: `fix/ef-g32-trade-list-remote-contract` (cambios locales sin commit pedido).
- `sdk`: `master` (working tree con StatObject/PutObject fixes).
