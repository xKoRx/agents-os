---
type: known_error
scope: public
created: 2026-07-25
updated: 2026-07-25
area: "[[Echo Forge]]"
project: "[[Echo Forge - Cierre de Etapa 4]]"
application: "[[EchoForgeTradeListExporter]]"
entities:
  - "[[EchoForgeTradeListExporter]]"
  - "[[TradeListArtifactWriter]]"
related:
  - "[[Echo Forge - Cierre de Etapa 4]]"
aliases:
  - manifest-rewrite-stale-success
  - sentinel-after-manifest-rewrite
confidence: verified
source_session: 2026-07-25-fix-pack-g2-review
load_policy: when_error_matches
indexable: true
index_priority: high
tags:
  - kind/known-error
  - tech/sqx-exporter
  - tech/atomicity
  - scope/public
---

# Sentinel `_SUCCESS` emitido con datos stale por rewrite post-gzip

## Síntoma

- `trades_manifest.json` termina con `artifact.compressed_bytes = 0`.
- `_SUCCESS` está presente aunque el manifest no refleje el gzip real.
- Riesgo: si la reescritura del manifest falla, queda `_SUCCESS` + manifest inválido y el importador Go lo lee como un scope completo.

## Causa

Patrón write-then-rewrite: el writer emite `_SUCCESS` con un manifest provisional (`compressed_bytes=0`), comprime NDJSON, y luego el exporter reescribe el manifest fuera del contrato atómico. La reescritura no es temp+move del mismo `writeScopeArtifacts`, así que si falla queda estado inconsistente.

## Impacto

- **Contrato roto**: el sentinel de completitud miente. El importador Go trata el scope como completo aunque el manifest no refleje `compressed_bytes`.
- **No detectable en el smoke**: el caso `compressed_bytes=0` sólo se manifiesta con un gzip real no trivial y un fallo de reescritura posterior.
- **No-retryable**: el caller propaga `ArtifactWriteException` pero el scope ya tiene `_SUCCESS` colgado.

## Detección

- En `manifest.compressed_bytes == 0` con `gz` de tamaño > 0, el smoke debe fallar.
- Cualquier artefacto que diga `compressed_bytes` placeholder (0L) antes de un temp+move real es candidato.

## Mitigación

- API única `writeScopeArtifacts(ndjson, result, ExportRunSpec)` que comprime NDJSON en memoria, conoce `compressed_bytes` reales, compone manifest + `export_run.json` con esos valores, y emite `_SUCCESS` **sólo si los 3 archivos quedaron persistidos** (temp+move atómico por archivo).
- Eliminar toda reescritura externa del manifest desde el caller (exporter).
- Cubrir en smoke con aserción dura `manifest.compressed_bytes > 0` Y `export_run.artifact.compressed_bytes == manifest.compressed_bytes`.

## Evidencia

- Handoff G2 review (veredicto del owner) en `specs/FEAT-SQX-METRICS-CONTRACT/phase2/G2_HANDOFF.md` §Blocker B2.
- Commit `5c186a3` en `symphony` que introdujo la API `writeScopeArtifacts` y eliminó el rewrite externo.
- Smoke `TradeListExportSmoke` ahora asserta hard en `manifest.compressed_bytes` y `export_run.artifact.{sha256, compressed_bytes, uncompressed_bytes}`.
- Reproducción del fallo original previo al fix: `compressed_bytes` quedaba en 0 si el gzip fallaba entre manifest y `_SUCCESS`.