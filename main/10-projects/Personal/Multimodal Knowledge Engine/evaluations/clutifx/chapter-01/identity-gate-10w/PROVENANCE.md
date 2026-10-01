# PROVENANCE

## Identidad del experimento

| Campo | Valor |
|---|---|
| Producto (binario del live) | repo `xKoRx/multimodal-knowledge-engine`, branch `feature/v2-layered-knowledge-model`, SHA `ef53530756a27009517030a1bd29f0472bb3ad48` (= origin al momento del live; build local `bin/mke`) |
| Base del fix F-ADV-01 | `71b5a21d30af888874ce2965b61d33d7371f0f82` (identity remediation certificada) |
| SOURCE_SHA256 | `4de8f12d4841c63022a03e7450e0b54c4947ed9c8fc8c408606dde79dd3d289b` (rehasheado 2026-10-01) |
| Transcript | `~/mke/clutifx-ch01-20260930/transcript.json` (SHA del propio archivo `f91cc92a…`, ligado a SOURCE_SHA; 323 segmentos) |
| Media run (L0) | `~/mke/clutifx-ch01-20260930/media-run` — REUTILIZADO, sin re-adquisición |
| Provider | adapter `openrouter`, modelo observado `stealth/space-bunny-alpha` en las 91 respuestas con usage; credencial `MKE_OPENROUTER_API_KEY` por-corrida desde `~/mke/.secrets/openrouter.env` (chmod 600, nunca persistida en artifacts ni logs) |
| Probe pre-run | 6/7 PASS (mismo único `inconclusive` que la corrida original: el backend respondió JSON válido y el path de rechazo no se ejercitó); evidence `artifacts/runtime/evidence/probe-openrouter-daedalus-20261001T163036Z.json` |
| Config | `mke.pipeline.config.v2`, 10 ventanas (primeras del config de 130), `review_timeout_seconds: 120` |
| Fingerprint del run | `config 9b534568…`, `L1 3d0fe06e…`, `L2 3a5c184c…` (persistidos en `pipeline_state`) |
| Budget | `mke.inference-budget.v1` `max_vlm_calls: 2400 / images: 8000 / tokens: 60,000,000` — consumido: 91 / 127 / 583,313 |
| Runtime local | `~/mke/clutifx-ch01-10w-gate-20261001/` (`run-live`, `run-live-attempt1-snapshot`, `run-replay`, `replay/`, `logs/`) |
| Wall time | 16:30:59Z → 17:26:40Z (3341 s) |

## Cadena de custodia de respuestas

- 92 invocations durables en `run-live/run.db` (`provider_invocations` con request/response/usage JSON): 10 reconstruction, 81 grounding review, 1 composition.
- Ninguna API key ni secreto en journal ni artifacts; el request/openrouter transport no persiste headers.
- El snapshot `run-live-attempt1-snapshot` preserva el estado byte-exacto del primer intento (el `run-live` publicado y el snapshot son idénticos; el resume live no se ejecutó porque el run terminó terminal-INCOMPLETE y el contrato sólo adopta runs RUNNING).

## Provenance física de los artifacts canónicos

- `claims.jsonl`: header con `source_id sha256:4de8f12d…` + `config_fingerprint 9b534568…`; cada claim/relation lleva `provenance` con provider/model/prompt_version/response_id/invocation_ids, `evidence_ids` y `grounding` con invocation_id y reasons del reviewer.
- Los 111 `dependency_edges` del journal resuelven 111/111: 89 evidence-ref contra transcript (segmentos `asr-*`) y media evidence (`frame-*`), 22 relation-endpoint contra records L1 — verificado físicamente contra los tres stores.
