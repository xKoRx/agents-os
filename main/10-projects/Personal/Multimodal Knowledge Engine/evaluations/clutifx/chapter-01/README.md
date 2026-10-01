# README — Clutifx Chapter 01 · Full Real Extraction (MKE V2) — **RESULT: BLOCKED**

## TL;DR

La primera extracción completa live de MKE V2 (`cc13a121`) sobre el capítulo 1 de Clutifx (34:03.9) terminó **BLOCKED**: el **L0 completo del capítulo es válido** (transcript, inspección visual, 1040 evidence, 130 ventanas), pero el pipeline L1 live terminó **FATAL (exit 5) en la ventana w0003** al detectar el contrato congelado de identidad (Shot 3, S2-B-01) que `cl-chart-instrument-eurusd@1` fue propuesto por w0002 y w0003 con contenido divergente. **No se publicó ningún claim/relation/SKO.** El bloqueo es **estructural para escala full-chapter en vivo** (ver `OMISSIONS.md` y `MANAGER-REVIEW.md`): la igualdad de contenido incluye `evidence_ids` window-locales y los claim ids son slugs del modelo, por lo que todo hecho visual persistente re-proposto en ventanas posteriores diverge ⇒ FATAL. Observado en el primer par de ventanas contiguas con un visual persistente (2→3).

## Ficha del run

| Campo | Valor |
|---|---|
| Curso | CURSO DE TRADING CLUTIFX (12 episodios, share SMB TrueNAS) |
| Capítulo | 1 — "Episodio 1 - Introducción" (evidencia de ordering: nombre original SMB `Episodio 1 - Introducción.mp4`, byte-size exacto) |
| Source SHA-256 | `4de8f12d4841c63022a03e7450e0b54c4947ed9c8fc8c408606dde79dd3d289b` |
| Duración / tamaño | 2043.93 s / 136,600,238 bytes (1080p30 h264 + AAC 44.1k stereo) |
| MKE SHA | `cc13a121cebbddf153f283a3df0f4197dfb92cc1` (`feature/v2-layered-knowledge-model`, HEAD == origin, árbol limpio) |
| Provider / adapter | live `openrouter` (API key por-corrida, nunca persistida) |
| Modelo | `stealth/space-bunny-alpha` (default del adapter; probe 6/7 PASS) |
| ASR | faster-whisper large-v3 int8 CPU, `es` (p=1.00), 323 segmentos, 97% habla, ligado al SHA |
| Resultado | `CLUTIFX_CH01_EXTRACTION = BLOCKED` (L0 COMPLETE; L1 FATAL contractual @ w0003; L2 no alcanzado) |

## Qué revisar y en qué orden

1. **`OMISSIONS.md`** — la causa exacta del bloqueo con el par divergente y su análisis.
2. **`REVIEW-INDEX.md`** — cronología física del run: las 3 reconstrucciones VALIDATED, los 56 claims + 4 relations **propuestos (NO committeados)** y el par fatal completo.
3. **`RUN.md`** — comandos reales, configs, budgets, tiempos de pared y estado por etapa.
4. **`COVERAGE.md`** — qué parte del capítulo quedó representada (L0 completo; L1 sólo 3/130 ventanas; 0 conocimiento publicado).
5. **`transcript.json`** — transcript canónico completo que MKE consumió (id/start/end/text por segmento).
6. **`MANAGER-REVIEW.md`** — facts para el Primary Manager (sin conclusiones) y `SCALE-ESTIMATE.md` — proyección lineal naive a 200 h / 400 GB marcada como SINGLE-CHAPTER LINEAR ESTIMATE.
7. **`provenance.jsonl`** / `provider-requests.jsonl` / `journal-*.jsonl` — navegación SKO-propuesta→L0→source, audit de las 5 boundaries y estado del journal.
8. **`review-evidence/`** — los 24 frames de las 3 ventanas reconstruidas + `MANIFEST.json` (evidence id → timestamp → nota).
9. **`replay-fatal/`** — evidencia de que el path de fallo es determinista: el replay recorded de las 3 respuestas vivas reproduce el mismo FATAL byte-idéntico en mensaje.

## Convenciones y límites del bundle

- `PRODUCT_CODE_CHANGED = NO`; `DESIGN_CHANGED = NO`; `D4_TOUCHED = NO`; `V3_SCOPE_ADDED = NO`; `SOURCE_VIDEO_UPLOADED = NO`.
- No existen `claims.jsonl` / `skos.jsonl` / `documentation.md`: el engine no los escribió (fatal previo a publication). Su ausencia ES el resultado honesto.
- Los 56 claims propuestos que aparecen en este bundle NO son conocimiento canónico: son respuestas del provider en el journal durable, rechazadas por el engine antes de commit. Están etiquetados `PROPOSAL_NOT_COMMITTED` en todas las superficies.
- `SUPPORTED_BY_AUTOMATED_REVIEW` no aplica: ninguna review llegó a ejecutarse.
- Run completo local (forensic): path en `RUN.md`.
