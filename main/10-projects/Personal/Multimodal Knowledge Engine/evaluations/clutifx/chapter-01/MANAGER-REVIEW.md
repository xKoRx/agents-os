# MANAGER-REVIEW — facts para el Primary Manager (sin conclusiones)

Preparado por el operador de la corrida. La evaluación final es del Primary Manager en otra sesión.

## 1. Run health

| Item | Dato |
|---|---|
| Código | `cc13a121cebbddf153f283a3df0f4197dfb92cc1` (== origin, árbol limpio, binario reconstruido de ese árbol) |
| Dispatch | config schema `mke.pipeline.config.v2` → ruta L0→L1→L2 |
| Preflight live | `probe-runtime --backend openrouter`: 6/7 PASS; `vlm.malformed_output_rejected` inconclusive (backend respondió JSON válido; path de rechazo no ejercitado); modelo observado == solicitado `stealth/space-bunny-alpha` |
| L0 | COMPLETE completo del capítulo (transcript 323 seg/97% habla; inspección 2044 frames stride 1s, 531 persistidos, complete=true, unobserved=null; acquire 1040/1040; 130 ventanas 8 frames) |
| L1 live | 3/130 ventanas reconstruidas (VALIDATED); FATAL sticky exit 5 durante commit de w0003; 0 records committeados; 0 grounding reviews ejecutados; 0 canonical outputs escritos |
| Budget | `max_vlm_calls 2400 / max_vlm_images 8000 / max_vlm_tokens 60M`; consumido real: 3 calls / 24 images / 100,725 tokens; 0 retries; 0 provider failures de transporte |
| Transporte | 3/3 recon calls OK (27s, 45s, ~6 min incl. arranque); timeout 600s no rozado |

## 2. El FATAL (contrato congelado, no crash)

- Mensaje exacto: `pipeline journal record identity corruption failed: record cl-chart-instrument-eurusd@1 was committed twice with divergent content (window w0002, then window w0003): same id/version with different content is corruption, never a silent replacement` — `internal/pipeline/v2_stages.go` `commitClaimCandidates` → `claimEntryContentEqual` (Shot 3, S2-B-01). Sticky fatal; `pipeline_state.status` quedó `RUNNING` (sin terminal en journal; exit 5 único terminal).
- Divergencia real (journal): w0002 `"The displayed chart instrument is EUR/USD."` @ frame p1080000 (00:12) vs w0003 `"The displayed chart instrument is EURUSD."` @ frame p3330000 (00:37). Difiere el texto del statement Y los evidence ids.
- La igualdad de contenido compara `Kind+Statement+Epistemic+EvidenceIDs` (claims) e ítem análogo para relations. Los evidence ids son window-locales por construcción de ventanas; los claim ids son slugs generados por el modelo (`cl-<stable-slug>` en el prompt congelado).
- Condición de disparo observada: primer par de ventanas contiguas que comparte un visual persistente (el gráfico EURUSD está en pantalla ~todo el capítulo). Con 130 ventanas y ~19 claims/ventana, la re-proposición de hechos persistentes con el mismo slug natural es el caso común, no el excepcional (1 divergencia en la 1.ª oportunidad observada).
- Determinismo del fallo: replay recorded de las 3 respuestas vivas → mismo exit 5 y MISMO mensaje (`replay-fatal/` en bundle).

## 3. Counts y densidad observada (3 ventanas)

| Métrica | Valor |
|---|---|
| Claims propuestos | 56 (11/31/14 por w0001/w0002/w0003) |
| Relations propuestos | 4 |
| kinds | claim 20, parameter 16, observation 14, rule 3, procedure_step 3 |
| epistemic | VIDEO_OBSERVED 30, INSTRUCTOR_SAID 26 |
| evidencia citada | frames 54, asr 26 |
| Tokens | prompt 81,099 / completion 19,626 / total 100,725 |
| Idioma statements (heurística) | en 45, es-like 10, other 1 — el modelo escribió mayoritariamente en inglés sobre contenido en español; el prompt congelado no declara política de idioma |

## 4. Cobertura física

- 00:00–00:42 reconstruida (proposals en journal, no committeados). 00:42–34:03.9 no procesada. L0 completo (ver `COVERAGE.md`).
- `frames_inspected 2044`, `unobserved_intervals: null`, `complete: true`; acquire 1040/1040 verificados.

## 5. Hotspots de review sugeridos (por densidad/anomalía, sin veredicto)

1. La semántica del bloqueo de identidad en escala multi-ventana (Sección 2) — decisión Owner/Manager requerida para cualquier corrida full-chapter.
2. Idioma de statements (inglés sobre fuente española) — el contrato actual no fija idioma.
3. El techo `max_vlm_calls 2400` habría detenido un run full-chapter incluso sin el fatal: proyección ~2.600+ calls (19 claims/ventana ⇒ ~1 review/record). Dato de planificación, no defecto.
4. Densidad de proposals en w0002 (31 claims/8 frames) vs w0001 (11) — variabilidad del modelo por ventana.
5. `pipeline_state.status=RUNNING` tras fatal — estado terminal del journal no escrito en la ruta ClassFatal.

## 6. Provenance

- Chain observable en `provenance.jsonl`: proposal → l0_refs (evidence_id, time_ns, content_sha256, source_id) → source SHA. Invocaciones completas con request/response en `provider-requests.jsonl` y `journal-*` (las 5 boundaries contractuales quedan documentadas en las 3 recon calls; no hubo calls de review/composition).
- `TestV2PhysicalProvenanceTraceResolvesToSourceSHA` de Shot 3 no aplica aquí (no hubo SKOs).

## 7. Artefactos

Bundle persistido: `main/10-projects/Personal/Multimodal Knowledge Engine/evaluations/clutifx/chapter-01/` (commit SHA en el handoff de la misión). Runtime local completo: `~/mke/clutifx-ch01-20260930/`.
