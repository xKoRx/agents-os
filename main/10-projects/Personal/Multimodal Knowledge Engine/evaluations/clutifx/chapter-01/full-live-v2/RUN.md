# RUN — CLUTIFX CH01 FULL LIVE (producto ef53530)

Veredicto: `CLUTIFX_CH01_FULL_LIVE = INCOMPLETE_USEFUL` — las 130 ventanas fueron intentadas, el pipeline completo (L1 + grounding + intento L2 + publicación) corrió sobre producto congelado, y el knowledge canónico (853 supported / 80 non-supported) es íntegro, auditable y reproducible por replay. INCOMPLETE es terminal ordenado (exit 4): 26 ventanas rechazadas por decisiones contractuales auditabless + L2 no alcanzado por transporte.

## Precondiciones (verificadas antes del live, en orden)

1. **Git:** repo `xKoRx/multimodal-knowledge-engine`, branch `feature/v2-layered-knowledge-model`, `HEAD == origin == ef53530756a27009517030a1bd29f0472bb3ad48`, tracked tree limpio (único untracked: `wt/`, worktree de review previo, no producto).
2. **Source rehasheado:** `4de8f12d…` exacto (ver SOURCE.md).
3. **L0 reutilizado con binding demostrado físicamente:** `L0_REUSED = YES` (SOURCE.md; sin re-ejecutar ASR/media/acquisition).
4. **Config:** las 130 ventanas canónicas del config original; sin eliminar/reordenar/fabricar ventanas; la config del gate 10W se verificó como las primeras 10 canónicas; budgets canónicos 2400/8000/60M.
5. **Binario:** construido de HEAD (SHA256 `7bdc4e23…`), sin código modificado.
6. **Probe openrouter 6/7:** mismo único `inconclusive` documentado de las corridas anteriores (`malformed_output_rejected` no ejercitado); `model_requested = model_observed = stealth/space-bunny-alpha`.
7. **Credencial:** `MKE_OPENROUTER_API_KEY` en memoria del proceso desde `~/mke/.secrets/openrouter.env`, por-corrida, nunca persistida (scan del bundle: 0 hits).

## Ejecución live (3 tramos, 2 crashes + resume contractual)

```text
bin/mke pipeline ~/mke/clutifx-ch01-20260930/media-run \
  --video ~/mke/course/ep01-intro.mp4 \
  --transcript ~/mke/clutifx-ch01-20260930/transcript.json \
  --config configs/config.v2.json --vlm openrouter \
  --budget configs/pipeline-budget.json --out run-live --timeout 600
```

| Tramo | Inicio (UTC) | Wall | Fin |
|---|---|---|---|
| Attempt 1 | 2026-10-01T20:42:19Z | 2:28:31 | FATAL exit 5 en w0057 |
| Resume 1 | 2026-10-01T23:14:18Z | 2:27:46 | FATAL exit 5 en w0093 |
| Resume 2 | 2026-10-02T01:43:00Z | 4:31:00 | INCOMPLETE exit 4 (terminal) |

Wall total de cómputo: **9h27m17s** (ventana de calendario 20:42Z → ~06:14Z). Los 2 fatales son la misma clase de provider (`parse-structured [fatal]: assistant content is empty` — el backend devolvió contenido vacío; transiente recurrente, ~1 cada ~36 ventanas). Ambos se recuperaron con el **crash/resume contractual** del producto (`allocatePipelineRunDirV2`: sólo adopta un run RUNNING con el mismo config fingerprint): las ventanas ya validadas se replayaron del journal durable sin nuevas llamadas (verificado físicamente: w0001–w0056 no re-invocadas en resume 1; w0058–w0092 no re-invocadas en resume 2), y sólo la ventana fatal se re-invocó live (ambas VALIDATED al retry). Snapshots de evidencia: `run-fatal-w0057-snapshot/` (local). `PRODUCT_CODE_CHANGED_AFTER_LIVE_STARTED = NO`; ninguna intervención semántica en respuestas, claims ni reintentos manuales.

## Fases y terminal state

- Reconstruction: 130/130 ventanas intentadas → 104 aceptadas, 26 rechazadas fail-closed (22 identity ladder: 16 divergencias deterministas + 6 semánticas; 4 por evidence refs inventadas).
- Ladder (línea durable de documentation.md): 1039 claims + 168 relations propuestos, 1 exact duplicate, 38 identity collisions (1 deterministic-equivalent + 15 semantic-equivalent merges + 22 divergent), 21 adjudicaciones semánticas (17 llamadas live + 4 re-verdictos content-addressed), 22 ventanas rechazadas por ladder.
- Integrity: 933/933 INTEGRITY_PASS.
- Grounding: 1048 llamadas (932 VALIDATED + 115 correctivos con reissue + 1 parse fatal → 1 REVIEW_UNAVAILABLE).
- L2: composition intentada 1 vez → `composition_unavailable` por transporte (`read-body retry-exhausted`); **0 SKOs**; razón durable `L2 composition unavailable: …`. Comportamiento contractual, sin reintento manual.
- Publicación: INCOMPLETE (exit 4) con `853 supported / 80 non-supported` (74 INSUFFICIENT + 5 CONTRADICTED + 1 REVIEW_UNAVAILABLE), 0 superseded.

## Resultado canónico

- **803 claims + 130 relations** publicados (`claims.jsonl` en este bundle, byte-a-byte del run).
- Kinds: 251 claim, 250 observation, 104 parameter, 101 rule, 97 procedure_step.
- Epistemic: 675 INSTRUCTOR_SAID, 236 VIDEO_OBSERVED, 22 MODEL_INFERRED.
- Idioma: **803/803 español** (0 inglés; 7 statements sin marcadores fueron verificados uno a uno — español sin tildes).
- Grounding: 746/803 claims + 112/130 relations SUPPORTED.

## REPLAY (recorded, 0 llamadas remotas)

Script exportado del journal durable (`replay-script.json` en este bundle; 1079 fixtures + 2 entradas de error de la misma clase frozen para el parse fatal de grounding y el transport failure de composition; 115 primeros intentos correctivos no representables — contrato 1 fixture por (task,target); las 4 respuestas recon REJECTED se fixture-aron byte-a-byte y el replay re-derivó el mismo rechazo).

```text
bin/mke pipeline … --vlm recorded:replay/script.json --out run-replay
→ exit 4 INCOMPLETE, 853 supported / 80 non-supported (mismo outcome funcional)
```

`REPLAY = PASS`. Comparación semántica (`replay-comparison.json`):

| Artefacto | Resultado |
|---|---|
| `skos.jsonl` | idéntico (0 SKOs en ambos) |
| `claims.jsonl` | 934/934 filas idénticas salvo 1 razón de error con wrapping extra del scripted error (`REVIEW_UNAVAILABLE` de `cl-rango-rectangular-vertical`: mismo estado, mismo código, texto de error con capa `grounding` adicional) |
| `documentation.md` | idéntico salvo 4 líneas de razones con la misma causa (i) las 3 ventanas rechazadas en crashes dicen en live «rejected in a previous attempt» (historia del resume) y en replay la razón original de validación; (ii) los 2 textos de error con wrapping extra) |
| Outcome, ventanas rechazadas, ladder line, records, supported/non-supported | **byte-idénticos** |

Deltas de budget live vs replay: vlm_call 1194 vs 1196, vlm_token 8,600,403 vs 8,597,595 (Δ 0.03% — los primeros intentos correctivos no son representables con 1 fixture por target). Ninguna diferencia material oculta.

## Nota de clasificación (corrección respecto de gates previos)

Las 4 ventanas con invocation REJECTED (w0003, w0005, w0043, w0110) NO son JSON malformado: sus respuestas son JSON válido con envelope correcto y fallaron **validación de propuesta por evidence refs inventadas** (`asr-00003 [34850-49400]`, `asr-00005 [61640-81320]`, `asr-00098 [572710-594750]`, `transcript asr-00245`) — exactamente el patrón `asr-NNNNN [range]` visto en el gate 10W. Frecuencia real en full chapter: **4/130 = 3.1%**, 0 ventanas con decode fallido.
