# PROVENANCE

## Identidad del experimento

| Campo | Valor |
|---|---|
| Producto (binario del live) | repo `xKoRx/multimodal-knowledge-engine`, branch `feature/v2-layered-knowledge-model`, SHA `ef53530756a27009517030a1bd29f0472bb3ad48` (= origin al momento del live; build local al runtime del gate) |
| BASE | identity remediation certificada `71b5a21` + F-ADV-01 `ef53530` (idéntico al gate 10W) |
| SOURCE_SHA256 | `4de8f12d4841c63022a03e7450e0b54c4947ed9c8fc8c408606dde79dd3d289b` (rehasheado 2026-10-01) |
| Transcript | `~/mke/clutifx-ch01-20260930/transcript.json` (SHA propio `f91cc92a…`, ligado a SOURCE_SHA; 323 segmentos) |
| Media run (L0) | `~/mke/clutifx-ch01-20260930/media-run` — REUTILIZADO, 1040/1040 evidencia verified, sin re-adquisición |
| Provider | adapter `openrouter`, modelo observado `stealth/space-bunny-alpha` en las 66 respuestas; credencial `MKE_OPENROUTER_API_KEY` por-corrida desde `~/mke/.secrets/openrouter.env` (chmod 600, mapeada en memoria, nunca persistida) |
| Probe pre-run | 6/7 PASS (mismo único `inconclusive` conocido; evidence `artifacts/runtime/evidence/probe-openrouter-daedalus-20261001T183047Z.json` en el runtime local) |
| Config | `mke.pipeline.config.v2`, 4 ventanas solapadas (diseño previo al live), `review_timeout_seconds: 120` |
| Fingerprint del run | `config b4fbdc70…` (persistido en claims.jsonl header y pipeline_state; L1/L2 en `pipeline_state`) |
| Budget | `mke.inference-budget.v1` `max_vlm_calls: 2400 / images: 8000 / tokens: 60,000,000` — consumido: 66 / 68 / 312,000 |
| Runtime local | `~/mke/clutifx-ch01-equiv-stress-20261001/` (`run-live`, `run-replay`, `replay/`, `logs/`, `configs/`, `bin/`, `export_replay_script.py`) |
| Wall time | 18:31:14Z → ~18:59:07Z (27m53s); exit 4 INCOMPLETE ordenado |

## Consumo por tarea (journal durable)

| Task | Calls | Tokens |
|---|---|---|
| claims.reconstruction | 4 | 151,661 |
| claims.equivalence_review | 3 | 1,506 |
| claims.grounding_review | 53 (48 VALIDATED + 5 primeros intentos REJECTED→reissue) | 146,660 |
| sko.composition | 1 | 7,504 |
| sko.composition_review | 5 | 4,669 |
| **Total** | **66** | **312,000** |

Costo reportado: `null` (el adapter openrouter no expone costo).

## Cadena de custodia de respuestas

- 66 invocations durables en `run-live/run.db` (`provider_invocations` con request/response/usage JSON): 4 reconstruction, 3 equivalence_review, 53 grounding_review, 1 composition, 5 composition_review. Estados: 61 VALIDATED + 5 REJECTED (primeros intentos de correctivos de grounding, reissue VALIDADO en los 5).
- Ninguna API key ni secreto en journal ni artifacts; el transporte openrouter no persiste headers.
- Las 3 adjudicaciones de equivalencia son content-addressed: quedan reutilizables por cualquier run futuro que re-coloque el mismo par de statements, sin nueva llamada live.

## Provenance física de los artifacts canónicos

- `claims.jsonl`: header con `source_id sha256:4de8f12d…` + `config_fingerprint b4fbdc70…`; 47 claims + 1 relation, cada uno con `provenance` (provider/model/prompt_version/response_id/invocation_ids), `evidence_ids`, `integrity` y `grounding` con invocation_id y razones del reviewer.
- 90/90 `dependency_edges` resuelven físicamente: evidence-ref contra manifest L0 + transcript, relation-endpoint y component contra records L1/L2. Cero residuo de las ventanas rechazadas (o2/o4 no aportan ni records, ni stage rows, ni edges — verificado por atribución de `record_stages`).
- Provenance multi-invocación (unión): 0 casos — ninguna acumulación llegó a aplicarse (ver F-1 en README).
