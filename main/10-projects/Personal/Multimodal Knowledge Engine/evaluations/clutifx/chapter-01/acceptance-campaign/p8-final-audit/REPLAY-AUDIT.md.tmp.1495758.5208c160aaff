# P8 — REPLAY AUDIT (candidato 19b44c1)

**Método:** export del journal durable (`export_replay_script.py run-rerun/run.db replay/` → 1391 fixtures, 227 filas skipped: duplicados REJECTED/REISSUE legítimos, 1 fixture por (task,target) con prioridad VALIDATED) → `bin/mke pipeline … --vlm recorded:replay/script.json --out run-replay` (0 llamadas remotas, mismo comando/config/budget que el live) → comparación semántica (`compare_replay.py` + diff normalizado campo a campo por el Manager).

## Terminal replay

```
exit 4 INCOMPLETE — idéntico al live: "1125 supported, 64 non-supported records"
claims.jsonl: 1190 rows live = 1190 rows replay
skos.jsonl: idéntico (header, sko_count 0 en ambos)
```

## Comparación normalizada (provenance/invocation/fingerprints excluidos por contrato)

- **1180/1190 records byte-idénticos** tras normalización contractual.
- **10 records difieren SOLO en el texto `grounding.reasons[].detail`** — los 10 records cuyo review falló por formato en live (5 parse-fatal + 5 de los malformed-verdict). Causa: el fixture frozen de replay re-representa el error de UN intento (re-wrap del mensaje, o el 1.er intento en vez del último en targets multi-attempt). Mismo `status`, mismo `code`, mismo outcome de publicación. Ejemplos verificados:
  - live: `…parse-structured [fatal]: assistant content is not a valid JSON object` / replay: `…grounding [fatal]: vlm provider parse-structured [fatal]: …` (wrapping extra).
  - live (último intento): `schema id "mke.claims-ground.v2", want v1` / replay (1.er intento): `addresses cl-fecha-24-06-2025@1@1, review target is cl-fecha-24-06-2025@1`.
- `documentation.md`: mismas 10 razones con wrapping anexo + líneas volátiles (budget/provider/fingerprint) — clase ya documentada en el replay del run viejo.

## Veredicto

```text
REPLAY = PASS
UNEXPLAINED_KNOWLEDGE_DIVERGENCE = 0
```

Nota: el replay hereda sko_count 0 (la propuesta de composition REJECTED es representable y se reproduce); con la remediación L2 (R-M05) el replay de la fase L2 deberá re-exportarse desde el run remediado.
