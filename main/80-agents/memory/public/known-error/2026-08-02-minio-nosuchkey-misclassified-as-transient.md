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
  - "[[2026-08-02-minio-content-type-user-metadata-rejected]]"
aliases:
  - minio nosuchkey transient
  - trade list stat The specified key does not exist
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
---

# MinIO NoSuchKey clasificado como ErrTradeTransient

## Síntoma

- `trade_list_exporter` falla con `core: trade transient error: stat …/06_trade_list/*.trades.ndjson.gz: The specified key does not exist.`
- Temporal reintenta sin fin; el plugin Java ya generó artefactos en `___FULL/`.

## Causa

- `UploadScopeArtifacts` hace `Stat` de idempotencia; ausencia es camino feliz → Put.
- `isMinIONoSuchKey` no matcheaba el Message S3 (`The specified key does not exist.`) ni el `StatusCode` de `minio.ErrorResponse` (es **campo**, no método).
- Todo error implementa `Error()`, así que el branch de `StatusCode()` era código muerto.

## Fix

- Tipar `errors.As` a `minio.ErrorResponse` + matcher del mensaje S3.
- En SDK: `statusCodeOf` lee el campo; `withRetry` no reintenta 404.
- Desplegado en worker `0.2.29+`.

## Detección

- Error Temporal con `stat … The specified key does not exist` envuelto en `ErrTradeTransient`.
- Logs `Failed to stat object` + retries `minio.stat_object` en 404.
