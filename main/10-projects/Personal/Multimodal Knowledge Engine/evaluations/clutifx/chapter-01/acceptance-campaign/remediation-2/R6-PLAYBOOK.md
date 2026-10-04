# R6 — PLAYBOOK P8 FINAL (sobre P7b @ e7bc387)

Preparado por el track P8/P9 manager antes de la terminalidad de P7b. Ejecutar CUANDO `run-rerun2` sea terminal (exit 0 o 4 en `logs/run-rerun2.log`, `pipeline_state.status` ≠ RUNNING).

## 0. Verificación de terminalidad y bindings

```bash
tail -3 ~/mke/clutifx-ch01-rerun2-20261004/logs/run-rerun2.log       # EXIT_CODE=
go version -m ~/mke/clutifx-ch01-rerun2-20261004/bin/mke | grep vcs.revision   # e7bc387…
sqlite3→python3: pipeline_state (status, config_fingerprint f05c95e4…, l1 469ad44d…, l2 3a5c184c…)
sha256sum bin/mke configs/config.rerun.v2.json   # bin 72bdde7b… / config 02f5f7ad…
```

Chequeos inmediatos de las 3 reparaciones:
- **R-M05:** skos.jsonl con sko_count>0; composition con objetos descartados con razón durable por objeto.
- **Tolerancia validador:** 0 records «reviewer produced a malformed verdict» sin recuperar; los 9 del P7 → SUPPORTED.
- **R-M06:** targets correctivos de recon presentes si hubo slips; sin ventana rechazada por formato si el correctivo validó.

## 1. Análisis canónico + corpus

```bash
cd ~/mke/clutifx-ch01-full-live-20261001 && mkdir -p analysis-p7b
python3 analyze_run.py ~/mke/clutifx-ch01-rerun2-20261004/run-rerun2 \
  ~/mke/clutifx-ch01-20260930/media-run ~/mke/clutifx-ch01-20260930/transcript.json \
  ~/mke/clutifx-ch01-rerun2-20261004/configs/config.rerun.v2.json analysis-p7b
cd "<vault>/evaluations/clutifx/chapter-01"
python3 acceptance-campaign/p8-comparison/build_corpus.py \
  ~/mke/clutifx-ch01-rerun2-20261004/run-rerun2 \
  ~/mke/clutifx-ch01-rerun2-20261004/configs/config.rerun.v2.json \
  ~/mke/clutifx-ch01-20260930/media-run ~/mke/clutifx-ch01-20260930/transcript.json \
  acceptance-campaign/p8-final-audit2/corpus analysis-p7b→coverage.json (path explícito)
```

## 2. Replay (R6 debe re-validar con el bundle)

```bash
export_replay_script.py run-rerun2/run.db replay-p7b/   # (copiar del full-live-20261001)
bin/mke pipeline … --vlm recorded:replay-p7b/script.json --out run-replay-p7b  # SIN api key
compare_replay.py run-rerun2 run-replay-p7b --json replay-p7b/replay-comparison.json
```
Expectativa: claims idénticos normalizados; SKOs idénticos (los que R-M05 publique); diffs sólo presentación.

## 3. Workers ONE-SHOT (mismos prompts de la ronda 1, actualizando: run dir, corpus p8-final-audit2, números de rechazo reales, y añadiendo verificación de reparación)

- claims×4 (w0001–w0033 / w0034–w0066 / w0067–w0099 / w0100–w0130) + MISSING-KNOWLEDGE + regression watch (los 4 baseline + w0037-nuevo).
- relations (todas), grounding (todos los non-supported + muestra distribuida + los que antes eran malformed/parse-fatal UNO A UNO), identity (reviews+colisiones+caché+fragmentación), provider (0 run-kills, reissues, budget), L2 (SKOs publicados, descartes por objeto, refs), rejected windows (residuo <19).

## 4. Síntesis + gates

- OLD-VS-NEW final (ef53530 vs e7bc387-run), umbrales P2 completos, RESIDUAL-FINDINGS, adjudicación.
- ACs del R3-ADJUDICATION: AC1.4 (+9 replay), AC2.2–2.4 (anti-rubber-stamp live: los 8 CONTRADICTED correctos siguen rechazados; 0 FP), AC4.4 (L2 con razones por objeto).

## 5. P9 freeze

`acceptance-campaign/p9-freeze/`: CHAPTER-01-ACCEPTANCE.md · FINAL-METRICS.json · FINAL-KNOWN-DEBT.md · FINAL-PROVENANCE.md · SCALE-READINESS.md. Concurrencia explícita de tracks (A: extracción/remediación + R5; B: P8/R1-R3/R6/P9) en PROVENANCE. Project note delta + push.
