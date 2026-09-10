---
type: decision
scope: project
created: 2026-07-25
updated: 2026-07-25
area: "[[Echo Forge]]"
project: "[[Echo Forge - Cierre de Etapa 4]]"
application: "[[EchoForgeTradeListExporter]]"
entities:
  - "[[TradeListArtifactWriter]]"
  - "[[EchoForgeTradeListExporter]]"
related:
  - "[[Echo Forge - Cierre de Etapa 4]]"
aliases:
  - writer-single-atomic-call
  - manifest-compressed-bytes-in-writer
confidence: verified
source_session: 2026-07-25-fix-pack-g2-review
load_policy: when_project_loaded
indexable: true
index_priority: high
tags:
  - kind/decision
  - tech/sqx-exporter
  - tech/atomicity
  - tech/contract
  - scope/public
---

# Atomicidad de artefactos multi-archivo: API única de writer

## Contexto

`TradeListArtifactWriter` (Java) escribe 4 archivos por scope (`trades.ndjson.gz`, `trades_manifest.json`, `export_run.json`, `_SUCCESS`). El manifest requiere `compressed_bytes` reales del gzip. El patrón original era:

1. Comprimir NDJSON a `gz` → conocer `compressed_bytes`.
2. Emitir `manifest` con `compressed_bytes=0` (provisional).
3. Escribir los 4 archivos vía temp+move.
4. **Después**, reescribir el manifest con el valor real (fuera del writer, en el exporter).

Ese patrón produce un `_SUCCESS` cuyo manifest es provisional; si la reescritura falla, queda sentinel + manifest inválido.

## Decisión

**Una sola API del writer arma y persiste los 4 archivos en orden atómico, sin reescritura externa.**

Firma canónica: `writeScopeArtifacts(byte[] ndjsonCanónico, TradeExtractionResult result, ExportRunSpec exportRunSpec)`. El writer:

1. Calcula `sha256` y `uncompressed_bytes` desde el NDJSON de entrada.
2. Comprime NDJSON a bytes en memoria → conoce `compressed_bytes`.
3. Compone manifest + `export_run.json` con esos valores.
4. temp+move de `gz → manifest → export_run → _SUCCESS` en orden estricto.
5. Si cualquier paso falla: cleanup de temporales + delete `_SUCCESS` + `ArtifactWriteException`.

El caller (exporter) pasa `ExportRunSpec.fromScope(scope)` y se olvida de la persistencia. **No** debe reescribir nada después.

## Rationale

- Atomicidad real: `compressed_bytes` se conoce antes de escribir el manifest, no después. El sentinel nunca se emite con datos stale.
- API de una sola llamada: el caller no tiene oportunidad de reescribir fuera del contrato.
- Los bytes ya están en memoria (NDJSON + gzip); composición de manifest/export_run en memoria no es un costo significativo vs. la complejidad evitada.
- Para casos donde el NDJSON exceda memoria disponible, el patrón debe migrar a temp+move con cálculo de `compressed_bytes` desde `tmpFile.length()` antes de componer el manifest — manteniendo siempre el orden estricto.

## Consecuencias

- **Positivas**: contrato verificable (`compressed_bytes` siempre real), error contract non-retryable más simple, smoke trivial.
- **Negativas**: si el NDJSON es muy grande (varios GB), el gzip en memoria puede ser prohibitivo. Mitigación documentada en la rama de "NDJSON grande".
- **Operacional**: el exporter pierde el bloque "rewrite post-gzip" (≈25 líneas). El writer gana `writeScopeArtifacts` (≈80 líneas nuevas) + `ExportRunSpec` record.

## Alternativas descartadas

- **Mantener write-then-rewrite con reintento del exporter**: introduce estado intermedio inconsistente; el sentinel aún se emite con datos stale.
- **Calcular `compressed_bytes` con un `CountingOutputStream`**: sigue requiriendo reescritura; misma fragilidad.
- **Escribir `_SUCCESS` último tras un "atomic swap" del directorio**: costoso, no portable entre FS.
