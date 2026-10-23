# ch01-introduccion — Clutifx · Capítulo 1

Biblioteca de conocimiento del primer video del curso Clutifx (introducción: el rango y los 7 conceptos base), reconstruida con la metodología `course-knowledge-extraction` **V1.2** el 2026-10-22.

## Historia del capítulo (MKE V2 → V1.2)

Este capítulo fue **originalmente extraído con el motor MKE V2** (run 2026-10-14/16, publicado 2026-10-17): ventanas `wNNNN`, 1.527 claims de granularidad por ventana, 367 relaciones, 1.894 registros, revisión por claim abortada por costo (44 h medidas para 34 min de video; grounding 1.140 SUPPORTED / 38 INSUFFICIENT / 22 CONTRADICTED / 694 UNREVIEWED al abortar). Ese resultado **no equivale a una biblioteca V1.2 certificada** (sin transcript anclado, sin frames publicados V1.2, sin revisión por minuto).

El 2026-10-22 (misión CLUTIFX FINAL REGULARIZATION) la biblioteca se **reconstruyó desde la fuente original bajo V1.2**: transcript reutilizado del run original con identidad verificada por SHA, extracción por bloques, revisión por minuto, integración con cardinalidad validada y DOCVERIFY independiente. El legado MKE V2 está **preservado intacto** en [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch01-introduccion/legacy-mke-v2/LEGACY-MANIFEST|legacy-mke-v2/]] (hashes verificados): es historia y material de contraste, **no conocimiento activo**; sus IDs `wNNNN`/`c-NNNN` no son IDs vigentes. No convertir automáticamente sus GROUNDING_SUPPORTED a SUPPORTED V1.2: los contratos de validación son distintos.

## Identidad de la fuente

| Campo | Valor |
|---|---|
| Archivo | `/home/kor/mke/course/ep01-intro.mp4` |
| SHA-256 | `4de8f12d4841c63022a03e7450e0b54c4947ed9c8fc8c408606dde79dd3d289b` |
| Duración | 34:04 (2.043,9 s) |
| Tema real | Introducción: el rango (creación, pendiente/reiniciado, completitud), Turtle Soup e intra, SMT (clásica + dos tipos), failure swing, order block, Power of 3; temario del curso |
| Título | El instructor no pronuncia un título de capítulo; "este es el primer capítulo" [33:48] ([[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch01-introduccion/CLAIMS#c-0132|c-0132]]) |

## Provenance de la extracción V1.2

| Campo | Valor |
|---|---|
| Fecha | 2026-10-22 |
| ASR | faster-whisper large-v3 (run original 2026-10-15), **reutilizado**: `transcript.json` con `source_sha256` verificado contra el video, 323 segmentos monótonos, cobertura completa (5,8 s → 2033,2 s), 0 vacíos. Anchors `^s-<HHMMSS>` añadidos con `add_block_anchors.py` (323, idempotente). |
| Extracción | 6 subagentes EXTRACTOR ONE-SHOT secuenciales (bloques de ~6 min), 132 claims propuestos |
| Revisión | 34 MINUTE_REVIEWERs ONE-SHOT (una revisión por minuto, 0–33), olas de 5; 6 muertes [1210] transitorias recuperadas con retry completo |
| Integración | `make_minute_payload.py` (contexto de frontera) + `integrate_reviews.py` (132/132, cobertura completa, 0 inválidos) + `validate_review.py` por minuto |
| Correcciones | Adjudicaciones del Manager en `<run>/evidence-adjudications.json` (7 adds de evidencia, 13 notas de garble confirmado, 3 visual_hints re-fijados); 7 frames re-nombrados por fórmula con sonda byte-idéntica |
| Run dir | `/home/kor/mke/clutifx-ch01-v12-20261022/` |
| Modelo | GLM (subagentes locales ONE-SHOT) |

## Métricas

| Métrica | Valor |
|---|---|
| Claims totales | 132 |
| Claims activos / superseded | 132 / 0 (ACTIVE KNOWLEDGE = claims sin `superseded_by`) |
| SUPPORTED / UNCERTAIN / UNVERIFIED | 132 / 0 / 0 (capítulo introductorio sin contradicciones; dudas en OPEN-QUESTIONS) |
| Epistemic | 114 instructor_statement + 18 visual_observation + 0 model_inference |
| Preguntas abiertas | 15 (`q-ch01-001..015`; 4 RESOLVED con evidencia adjudicada) |
| Frames base (fin de minuto) | 35 (manifiesto `frames/.base_frames`) |
| Frames bajo demanda | 58 (80 referencias citadas sobre 93 físicos; corrección de grounding visual 2026-10-22) |
| Rules / concepts / examples documentados | 40 / 14 / 27 |
| Revisión independiente (DOCVERIFY) | ONE-SHOT independiente 2026-10-22; ver su reporte en el run y AMENDMENTS |

## Cómo citar / consultar

- Autoridad máquina-legible: [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch01-introduccion/claims.jsonl|claims.jsonl]] · proyección navegable: [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch01-introduccion/CLAIMS|CLAIMS]]
- Síntesis: [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch01-introduccion/documentation|documentation]] · reglas: [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch01-introduccion/rules|rules]] · conceptos: [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch01-introduccion/concepts|concepts]] · ejemplos: [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch01-introduccion/examples|examples]]
- Recursos: [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch01-introduccion/transcript|transcript]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch01-introduccion/FRAMES|FRAMES]] (inventario)
- Gobierno: [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch01-introduccion/OPEN-QUESTIONS|OPEN-QUESTIONS]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch01-introduccion/AMENDMENTS|AMENDMENTS]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch01-introduccion/review-notes|review-notes]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch01-introduccion/legacy-mke-v2/LEGACY-MANIFEST|legacy-mke-v2 (LEGACY, no activo)]]
