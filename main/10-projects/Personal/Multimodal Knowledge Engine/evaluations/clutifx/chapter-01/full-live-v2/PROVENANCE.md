# PROVENANCE — cadena de custodia

| Eslabón | Valor |
|---|---|
| Producto (código) | `ef53530756a27009517030a1bd29f0472bb3ad48` = HEAD = origin/feature/v2-layered-knowledge-model, tracked tree limpio |
| Binario ejecutado | construido de HEAD; SHA256 `7bdc4e23f7b4d3721bcb312855b2d29928e045f99c0817dc27114e92d07b1aef` |
| Source | `~/mke/course/ep01-intro.mp4` («Episodio 1 - Introducción»), SHA256 `4de8f12d4841c63022a03e7450e0b54c4947ed9c8fc8c408606dde79dd3d289b` rehasheado antes del live |
| Transcript | SHA256 `f91cc92a2bb5583bc1d067c783ac956008d92012fa32ca8e54a32b968f504c3f`, 323 segmentos, `source_sha256` = SOURCE_SHA, ASR faster-whisper large-v3 (es p=1.00) |
| L0 | REUTILIZADO del run original (`~/mke/clutifx-ch01-20260930/media-run`): source.json sha256 = SOURCE_SHA; 1040/1040 evidencia verified=1; 1040/1040 hashes del manifest verificados contra objetos en disco (0 mismatches); diff `cc13a121..ef53530` sin archivos L0 |
| Config | 130 ventanas canónicas del config original (SHA256 copia `3c5fc83f…`), budgets canónicos 2400/8000/60M (`9b92cb5c…`) |
| config_fingerprint del run | `10418ccfee9c0c6d58dd4b5ba0b86698819cf31fe8c5610d59413a17be4be478` |
| l1_fingerprint | `e2550c53f0688c0d451ea1b8885be085e1db083a21d7b765fe6106de71d9973c` |
| l2_fingerprint | `3a5c184c05f4c14b9de0d86de208b5647886289352bbeb1770e60751f4b3f392` (adapter/model ligation S2-J-03) |
| Provider | openrouter / stealth/space-bunny-alpha (probe 6/7, mismo inconclusive conocido; model_requested == model_observed) |
| Credencial | por-corrida en memoria desde `~/mke/.secrets/openrouter.env`; nunca persistida en artefactos/logs/journal |

## Inmutabilidad del producto

- `PRODUCT_CODE_CHANGED_AFTER_LIVE_STARTED = NO` (ningún touch al repo durante la misión; verificación git antes del launch y al cierre).
- Prompts/config semantics congelados: contrato `mke.claims-recon.v2 / mke.claims-ground.v1 / mke.sko-compose.v1 / mke.sko-review.v1`.
- Los únicos artefactos nuevos son tooling de análisis local (analyze/compare/export python, sin commit al producto).

## Crash/resume

- Fatal #1: w0057 `assistant content is empty` (exit 5, 2:28:31 de tramo) — snapshot `run-fatal-w0057-snapshot/run.db` + log.
- Fatal #2: w0093 misma clase (exit 5, tramo 2:27:46) — snapshot `run.db.after-w0093-fatal` + log.
- Ambos resumes adoptados por el contrato `allocatePipelineRunDirV2` (RUNNING + mismo fingerprint); las ventanas validadas se replayaron del journal sin nuevas llamadas; sólo la ventana fatal se re-invocó live.

## Salidas canónicas

- `claims.jsonl` (803 claims + 130 relations), `skos.jsonl` (0), `documentation.md` publicados por el producto en `run-live/`; este bundle los copia byte-a-byte.
- Fingerprints ligados al adapter/model; el replay recorded con el mismo config produce los mismos fingerprints de contenido (ver RUN.md §replay).
