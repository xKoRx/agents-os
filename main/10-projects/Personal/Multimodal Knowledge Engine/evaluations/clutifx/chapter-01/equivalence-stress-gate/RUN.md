# RUN — LIVE EQUIVALENCE STRESS GATE

## Precondiciones (verificadas antes del live, en orden)

1. **Git:** repo `xKoRx/multimodal-knowledge-engine`, branch `feature/v2-layered-knowledge-model`, `HEAD == origin == ef53530756a27009517030a1bd29f0472bb3ad48`, tracked tree limpio (único untracked: `wt/`, worktree de review previo). Verificado de nuevo inmediatamente antes del lanzamiento (18:31:14Z).
2. **Source rehasheado:** `4de8f12d…` exacto.
3. **L0 reutilizado con binding demostrado físicamente:** `media-run/source.json` SHA = SOURCE_SHA; transcript con `source_sha256` = SOURCE_SHA y SHA de archivo `f91cc92a…`; 1040/1040 evidencia `verified=1`. Diff de la remediation sin archivos L0. `L0_REUSED = YES` sin re-ejecutar ASR/media/acquisition.
4. **Binario:** construido de HEAD al runtime del gate (`bin/mke`), sin código modificado.
5. **Probe openrouter 6/7:** mismo único `inconclusive` documentado de las dos corridas anteriores (`vlm.malformed_output_rejected`: el backend respondió JSON válido y el path de rechazo no se ejercitó). `model_requested = model_observed = stealth/space-bunny-alpha`.
6. **Ventanas fijadas ANTES de cualquier inferencia live** (ver WINDOWS.md): derivadas sólo del inventario físico de frames del L0 + la región aceptada `w0002` del gate 10W. Sin mirar IDs que produjera el modelo; sin tocar prompts; sin hardcodear IDs en el prompt.
7. **Credencial:** `MKE_OPENROUTER_API_KEY` mapeada en memoria del proceso desde `~/mke/.secrets/openrouter.env` (chmod 600), por-corrida, nunca persistida en artifacts, logs ni journal (scan del bundle: 0 hits).

## Ejecución live

```text
bin/mke pipeline ~/mke/clutifx-ch01-20260930/media-run \
  --video ~/mke/course/ep01-intro.mp4 \
  --transcript ~/mke/clutifx-ch01-20260930/transcript.json \
  --config configs/config.v2.stress4.json --vlm openrouter \
  --budget configs/pipeline-budget.json --out run-live --timeout 600
```

- Inicio 2026-10-01T18:31:14Z, fin ~18:59:07Z (wall 27m53s).
- Fases: 4 reconstruction (4 propuestas VALIDATED por `ValidateProposal`; 2 commiteadas, 2 rechazadas por el identity ladder en commit) → integrity → 53 grounding review (48 first-pass + 5 correctivos, todos con reissue VALIDATED) → **composition 1 + composition review 5, todos VALIDATED → 5 SKOs** → publicación INCOMPLETE (exit 4, terminal ordenado por las 2 ventanas rechazadas).
- Terminal: `49 supported / 4 non-supported` (3 UNSUPPORTED_INSUFFICIENT + 1 UNSUPPORTED_CONTRADICTED), `47 claims + 1 relation + 5 skos`, status INCOMPLETE con razones durables.
- 66 provider calls, 0 con `error_class`, 0 ClassFatal, 0 transport failures (a diferencia del gate 10W, el transporte de composition funcionó).
- `PRODUCT_CODE_CHANGED_AFTER_LIVE_STARTED = NO` (ningún touch al repo después del lanzamiento).

## Línea de autoridad del ladder (resumen durable del run)

```text
identity ladder: 102 claims + 4 relations proposed, 1 exact duplicates,
4 identity collisions (0 deterministic-equivalent accumulations,
2 semantic-equivalent merges, 2 divergent), 3 semantic-equivalence reviews,
2 windows rejected
```

Convención de contadores (verificada contra `commitClaimCandidates`): los contadores cuentan DECISIONES del phase DECIDE; el APPLY sólo corre en ventanas plenamente aceptadas. Por eso los "2 semantic-equivalent merges" no dejaron filas `EVIDENCE_ACCUMULATED`: la ventana o4 fue rechazada completa por el DIVERGENT antes del APPLY.

## REPLAY (recorded, 0 llamadas remotas)

Script exportado del journal durable (`export_replay_script.py`, adaptado: target = marker `target:` del propio request —las adjudicaciones son content-addressed—, un fixture por (task,target), primeros intentos REJECTED de correctivos excluidos por contrato): 61 fixtures, 0 calls remotas.

```text
bin/mke pipeline ... --vlm recorded:replay/script.json --out run-replay
→ exit 4 INCOMPLETE, 49 supported / 4 non-supported (mismo outcome funcional)
```

Comparación:

| Artifact | Resultado |
|---|---|
| `claims.jsonl` | semánticamente idéntico (49/49 líneas) tras normalizar identidad de ejecución: `provenance.{provider,model,response_id,invocation_ids,config_fingerprint}`, `grounding.invocation_id`, `header.config_fingerprint` |
| `skos.jsonl` | semánticamente idéntico (6/6 líneas) bajo la misma normalización |
| `documentation.md` | idéntico tras normalizar esos campos y las 2 líneas volátiles documentadas: budget counters (live 66/68/312,000 vs replay 61/60/285,298 — los 5 primeros intentos REJECTED de correctivos no son representables con 1 fixture por (task,target)) y `provider:` |
| Razones de rechazo de ventana | byte-idénticas live vs replay |
| Contadores del identity ladder | idénticos live vs replay (`3 semantic-equivalence reviews` en ambos: el replay re-deriva las colisiones y reusa las adjudicaciones journaladas content-addressed sin nueva llamada live) |

`REPLAY = PASS` (contenido semántico idéntico; deltas explicados por superficie/tooling, no por el pipeline).
