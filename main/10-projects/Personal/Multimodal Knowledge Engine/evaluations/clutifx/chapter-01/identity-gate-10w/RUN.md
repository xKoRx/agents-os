# RUN — CLUTIFX 10W LIVE GATE

## Precondiciones (todas verificadas antes del live)

1. **Etapa A cerrada primero**: F-ADV-01 (doble conteo de `divergentCollisions`) corregido en `internal/pipeline/v2_stages.go` con `resolveIdentityCollision` como única autoridad de conteo; regression `TestV2IdentityDivergentCollisionsCountedExactlyOnce` red-green (falla en el árbol pre-fix reportando "2 divergent" para 1 colisión; verde con "1"). Gates: `go test ./internal/pipeline/...` 145s ok; `go test ./...` 20/20 paquetes ok; `go vet` limpio; `go build` limpio. Commit `ef53530` pusheado FF sobre `71b5a21` (origin actualizado antes del live). `PRE_LIVE_SHA = ef53530756a27009517030a1bd29f0472bb3ad48`.
2. Source rehasheado: `4de8f12d…` exacto. Transcript ligado al mismo SHA. Media-run con 1040/1040 evidencia COMPLETE. Diff `cc13a121..ef53530` sin archivos L0. → `L0_REUSED = YES`.
3. Probe openrouter 6/7 (mismo único inconclusive documentado de la corrida original). Modelo solicitado = observado = `stealth/space-bunny-alpha`.
4. Worktree limpio al lanzar el live; después del lanzamiento **no se modificó código de producto** (`PRODUCT_CODE_CHANGED_AFTER_LIVE_STARTED = NO`).

## Ejecución

```text
bin/mke pipeline ~/mke/clutifx-ch01-20260930/media-run \
  --video ~/mke/course/ep01-intro.mp4 \
  --transcript ~/mke/clutifx-ch01-20260930/transcript.json \
  --config configs/config.v2.10w.json --vlm openrouter \
  --budget configs/pipeline-budget.json --out run-live --timeout 600
```

- Inicio 2026-10-01T16:30:59Z, fin ~17:26:40Z (55m41s).
- Fases: 10 reconstruction (8 validadas, 2 rechazadas por output inválido) → integrity → 81 grounding review (75 records, 6 correctivos) → composition UNAVAILABLE (transport read-body, retries del adapter agotados) → publicación INCOMPLETE (exit 4, terminal ordenado).
- Terminal: `66 supported / 9 non-supported`, `sko_count: 0`, status INCOMPLETE con razones durables.

## RESUME CHECK

El runtime sólo adopta runs con status RUNNING y el mismo fingerprint (fail-closed); el run terminó en INCOMPLETE **terminal** (terminación ordenada, no crash), así que no existe estado a mitad de camino que reabrir: `RESUME_NO_RECHARGE = NOT_EXERCISED` (por diseño del outcome; nada se re-cobró porque no hubo reingreso). El snapshot `run-live-attempt1-snapshot` preserva el estado del primer intento.

## REPLAY (recorded, 0 llamadas remotas)

Script exportado del journal durables (83 fixtures VALIDATED + 2 REJECTED de recon + 1 transport-error entry de composition; tooling local `export_replay_script.py` adaptado para: target = marker del request, incluir respuestas REJECTED, y dedupe (task,target) prefiriendo VALIDATED). Replay: `--vlm recorded:replay/script.json` → mismo outcome funcional (66/9, INCOMPLETE).

Comparación física:

| Artifact | Resultado |
|---|---|
| `skos.jsonl` | idéntico (tras normalizar identidad de ejecución) |
| `claims.jsonl` | contenido idéntico; únicos deltas = `provenance.provider` (openrouter vs recorded) y hashes/fingerprints derivados del adapter — contractual (la identidad del run liga el adapter, S2-J-03) |
| `documentation.md` | idéntico salvo 2 líneas explicadas: (1) texto del reason de composition (live: retry-exhausted tras 3 intentos del adapter; replay: retryable de un intento — el adapter recorded no implementa retry interno) y (2) budget counters (91/127/583,313 live vs 85/120/555,823 replay: los 6 correctivos no son representables en el script por el contrato 1-fixture-por-(task,target)) |

`REPLAY = PASS` (contenido semántico idéntico; deltas documentados y explicados por el tooling/superficie, no por el pipeline).
