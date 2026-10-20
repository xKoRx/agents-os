# ch06-failure-swing — Clutifx · Capítulo 6

Biblioteca de conocimiento del sexto video del curso Clutifx, extraída con la metodología `course-knowledge-extraction` (skill canónica del vault, NO el pipeline MKE V2), v1.2 + hardening ch03/ch04/ch05.

## Identidad de la fuente

| Campo | Valor |
|---|---|
| Archivo | `/home/kor/mke/course/ep06-failure-swing.mp4` |
| SHA-256 | `470ff3c0c188e9959a357f89c5495fbfd8b5830fe3b08e7daca85ca0c0e25620` |
| Duración | 13:27.98 (807,98 s), h264 + aac |
| Tema | Failure swing: definición (falla el nuevo extremo y va directo al otro lado), los 3 motivos (SMT, final de hora/vela, brokers), rango activado sin tomar el extremo, identificación con order block, y la operativa final con rangos a favor |
| Prerrequisitos | SMT (ch05, "con la SMT ya lo habéis visto" [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch06-failure-swing/CLAIMS#c-0027|c-0027]]); definición introductoria y caso de brokers/feed de ch01; Turtle Soup/order block/rangos (ch01, ch03, ch04) |
| Referencias | hacia atrás → ch01 (motivos ya anunciados), ch05 (SMT como motivo 1); hacia delante → "nos vemos en el siguiente" [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch06-failure-swing/CLAIMS#c-0064|c-0064]] (ep07-setups) |

## Provenance de la extracción

| Campo | Valor |
|---|---|
| Fecha | 2026-10-19 |
| Preflight | video verificado (SHA + duración por ffprobe); contención externa despejada para agentes (grind r5 de Echo en CPU, load ~10/24); `integrate_reviews.py` corregido (contador de normalización `f-.png` contaba refs ya canónicas; fix con caso 6 en `integrator_selftest.py`, **6/6** PASS) sin cambio funcional del merge |
| ASR | faster-whisper `large-v3`, int8 CPU, language=es (p=1,00), beam 5, 167 segmentos, 97 % habla, ligado al SHA; wall 59,5 min (0,23× realtime, rate canónico) |
| Extracción | 3 subagentes GLM ONE-SHOT en paralelo (bloques 0–5, 5–10, 10–13:28), 64 claims en 10,6 min |
| Revisión | 14 subagentes ONE-SHOT — UNA revisión por minuto (ola 1: minutos 0–4 = checkpoint; ola 2: minutos 5–13), 14/14 `MINUTE_REVIEW = VALID` (cardinalidad exacta) |
| Integración | mecánica (`integrate_reviews.py` + `validate_review.py` por minuto); contador de normalización reportó 6 refs `.png` reales; 10 `corrections_suggested` revisadas y aplicadas por el integrador (statements literales, visual_hint corregido, hedge restaurado) |
| Modelo | GLM (subagentes locales de agente; sin API pagada, sin cambio de modelo) |
| Checkpoint 5 min | PASS (20/20 VALID tras minutos 0–4; proyección ~140 min/h-video → continuar; resultó 98 con ola única) |

## Métricas

| Métrica | Valor |
|---|---|
| Claims totales | 64 |
| SUPPORTED / UNCERTAIN / UNVERIFIED | 64 / 0 / 0 |
| Claims activos / superseded | 64 / 0 (sin supersessions en este capítulo) |
| Epistemic | 62 instructor_statement · 2 visual_observation (con frame verificado en `evidence`) · 0 model_inference |
| Contradicciones marcadas | 0 |
| Frames base (fin de minuto) | 14 (minutos 0–12 en MM:59.5 + fin del parcial [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch06-failure-swing/frames/f-001327.png|f-001327]], fade negro del cierre; manifiesto `frames/.base_frames`) |
| Frames bajo demanda | 5 ([[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch06-failure-swing/frames/f-000204.png|f-000204]], [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch06-failure-swing/frames/f-000212.png|f-000212]], [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch06-failure-swing/frames/f-000239.png|f-000239]], [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch06-failure-swing/frames/f-000419.png|f-000419]], [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch06-failure-swing/frames/f-001002.png|f-001002]]; extraídos y verificados visualmente por los MINUTE_REVIEWERs, nombres por fórmula desde segundos reales); 17 frames citados en total |
| Preguntas abiertas | 13 (q-ch06-001..013, ver [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch06-failure-swing/OPEN-QUESTIONS|OPEN-QUESTIONS]]) |
| Rules / concepts / examples documentados | 16 / 10 / 6 |
| Coverage | 14/14 minutos de video con claims y revisión |

## Throughput (reporte separado tramos vs total)

| Tramo | Valor |
|---|---|
| ASR wall | 59,5 min (0,23× realtime; partida dominante del total, rate canónico) |
| Extracción wall | 10,6 min (3 subagentes paralelos) |
| Revisión wall | ≈11,5 min (ola 1: 5 revisores, 5,3 min; ola 2: 9 revisores en paralelo, ≈8,5 min) |
| Agent wall (extracción+revisión) | ≈22 min para 13,5 min de video ≈ **98 min/h-video** (objetivo ≤120 → PASS; el mejor capítulo del curso: ch05 143, ch04 233, ch03 225) |

## Estructura

- [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch06-failure-swing/documentation|documentation]] — síntesis por conceptos, todo citado
- [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch06-failure-swing/CLAIMS|CLAIMS]] — proyección navegable por claim (autoridad: `claims.jsonl`)
- [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch06-failure-swing/transcript|transcript]] — recurso citable con anchors `^s-HHMMSS`
- [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch06-failure-swing/FRAMES|FRAMES]] — inventario de frames
- [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch06-failure-swing/rules|rules]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch06-failure-swing/concepts|concepts]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch06-failure-swing/examples|examples]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch06-failure-swing/study-guide|study-guide]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch06-failure-swing/review-notes|review-notes]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch06-failure-swing/OPEN-QUESTIONS|OPEN-QUESTIONS]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch06-failure-swing/AMENDMENTS|AMENDMENTS]]

## Run dir

`/home/kor/mke/clutifx-ch06-20261019/` (pool, payloads, reviews, epoch files, context pack).
