# RUN — Comandos y configuración reales

## Identidad del código

- Repo `xKoRx/multimodal-knowledge-engine`, branch `feature/v2-layered-knowledge-model`, HEAD `cc13a121cebbddf153f283a3df0f4197dfb92cc1` == `origin/feature/v2-layered-knowledge-model`, árbol limpio al iniciar. Binario construido de ese árbol (`go build ./cmd/mke`); ningún archivo product fue modificado (`git status` limpio durante todo el run).
- Pipeline V2 seleccionado por config schema `mke.pipeline.config.v2` (dispatch antes de decode estricto).

## Secuencia ejecutada (comandos literales)

```bash
# ASR local (ruta certificada V1; transcript ligado al SHA-256 del fuente)
python3 ~/mke/asr/transcribe.py ~/mke/course/ep01-intro.mp4 --out transcript.json
#   → es detectado (p=1.00), 323 segmentos, habla 1979.8s/2043.9s (97%), 6463.6s pared (0.32x realtime)

# L0 media (SPEC-01), con transcript
./bin/mke media ~/mke/course/ep01-intro.mp4 --transcript transcript.json \
  --config configs/media-config.json --out media-run
#   → COMPLETE: 2044 frames inspeccionados, 531 persistidos, 23 eventos; 2995s pared

# Plan determinista (policy m0-selection-baseline-v1)
./bin/mke plan --media-run media-run --out acquire-batch.json
#   → 1040 FRAME requests

# Acquire (SPEC-02) con budget explícito mke.budget.v1
./bin/mke acquire media-run --video ~/mke/course/ep01-intro.mp4 \
  --requests acquire-batch.json --budget configs/acquire-budget.json
#   → COMPLETE 1040/1040; 3248.9s pared

# Ventanas (policy m0-windows-baseline-v1) y transformación mecánica v1→v2 del mismo conjunto
./bin/mke windows --media-run media-run --out windows-v1.json
#   → 130 ventanas (8 frames c/u, gap ≤10s, w0001..w0130)
#   configs/config.v2.json = {schema: mke.pipeline.config.v2, windows: <mismas 130>, review_timeout_seconds: 120}

# Probe del backend live (sanity pre-run)
MKE_OPENROUTER_API_KEY=... ./bin/mke probe-runtime --backend openrouter --host-class daedalus --timeout 300
#   → 6/7 tests PASS; único "inconclusive": malformed_output_rejected (el backend respondió JSON válido,
#     path de rechazo no ejercitado); modelo observado = solicitado = stealth/space-bunny-alpha

# Pipeline V2 LIVE
MKE_OPENROUTER_API_KEY=... ./bin/mke pipeline media-run \
  --video ~/mke/course/ep01-intro.mp4 --transcript transcript.json \
  --config configs/config.v2.json --vlm openrouter \
  --budget configs/pipeline-budget.json --out run-clutifx-ch01 --timeout 600
#   → exit 5 (FATAL): identity corruption S2-B-01 @ commit de w0003; 481s pared

# Replay del path de fallo (determinismo del failure, no del modelo)
python3 export_replay_script.py run-clutifx-ch01/run.db replay-fatal/
./bin/mke pipeline media-run --video ~/mke/course/ep01-intro.mp4 --transcript transcript.json \
  --config configs/config.v2.json --vlm recorded:replay-fatal/script.json \
  --budget configs/pipeline-budget.json --out run-replay-fatal
#   → exit 5, MISMO mensaje de error byte-idéntico (replay determinista del fatal)
```

## Configs

- `configs/media-config.json`: `{schema: mke.media.config.v1, inspection: {stride_us: 1000000, max_frames: 4096}, extraction: {format: png, seek_margin_us: 2000000}}` — dimensionado al fuente completo (errata 6 del runbook).
- `configs/acquire-budget.json`: `mke.budget.v1` — `max_requests: 1040, max_images: 1040, max_sequences: 0, max_sequence_members: 0, max_bytes: 4294967296, max_wall_clock_ns: 14400000000000, max_retry_attempts: 2`.
- `configs/pipeline-budget.json`: `mke.inference-budget.v1` — `max_vlm_calls: 2400, max_vlm_images: 8000, max_vlm_tokens: 60000000` (techos de seguridad; no se alcanzaron).
- `configs/config.v2.json`: schema `mke.pipeline.config.v2`, 130 windows, `review_timeout_seconds: 120`. Sin `composition_catalog_limit` (ilimitado) y sin override de prompts (constantes congeladas).

## Provider

| Campo | Valor |
|---|---|
| Adapter | `openrouter` (internal/providers/openrouter) |
| Credencial | `MKE_OPENROUTER_API_KEY` por-corrida desde `~/mke/.secrets/openrouter.env` (chmod 600, fuera de repos); nunca persistida en artifacts |
| Modelo | `stealth/space-bunny-alpha` (default del adapter; igual al certificado en V1 live 2026-09-28) |
| Timeout por intento | 600 s (errata 8 del runbook) |
| Reintentos | budget del adapter (2); 0 usados |
| Costo reportado | `null` — el adapter no expone costo (Usage = prompt/completion/total tokens) |

## Estado del run y tiempos

| Etapa | Estado | Pared |
|---|---|---|
| ASR | COMPLETE | 6463.6 s |
| media | COMPLETE (2044/531/23) | 2995.0 s |
| plan | COMPLETE (1040) | ~3 s |
| acquire | COMPLETE (1040/1040) | 3248.9 s |
| windows | COMPLETE (130) | ~2 s |
| pipeline L1 live | **FATAL exit 5** (3/130 ventanas reconstruidas; 0 records committeados; 0 reviews ejecutadas) | 481 s |
| replay fatal | exit 5, error idéntico | — |

Inicio pipeline: 2026-10-01T02:27:13Z · Fin: 2026-10-01T02:35:14Z.

## Errores y retries

- 0 errores de transporte/retry; el run terminó por **ClassFatal contractual**: `pipeline journal record identity corruption failed: record cl-chart-instrument-eurusd@1 was committed twice with divergent content (window w0002, then window w0003)` — comportamiento exacto del fix Shot 3 S2-B-01 (`internal/pipeline/v2_stages.go`, `commitClaimCandidates`/`claimEntryContentEqual`). Sticky fatal; sin ruta de resume.
- `pipeline_state.status` quedó `RUNNING` en el journal (el fatal no escribe estado terminal; el exit code 5 es el único terminal).

## Artifacts runtime locales (forensic; NO versionados)

- Workspace completo: `~/mke/clutifx-ch01-20260930/`
  - `media-run/` (362 MB: source.json, media/, evidence/ 1040 objetos, run.db)
  - `run-clutifx-ch01/` (run.db del run live fatal), `run-replay-fatal/`, `replay-fatal/` (script+fixtures)
  - `transcript.json`, `acquire-batch.json`, `windows-v1.json`, configs, logs, exporters
- El bundle persistido en el vault es autocontenido: evaluación sin depender de este directorio.
