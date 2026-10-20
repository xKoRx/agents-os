# ch05-smt — Clutifx · Capítulo 5

Biblioteca de conocimiento del quinto video del curso Clutifx, extraída con la metodología `course-knowledge-extraction` (skill canónica del vault, NO el pipeline MKE V2), v1.2 + hardening ch03/ch04 + preflight de continuidad.

## Identidad de la fuente

| Campo | Valor |
|---|---|
| Archivo | `/home/kor/mke/course/ep05-smt.mp4` |
| SHA-256 | `072f669dc13f0fc0053c53eb19d11973d9d1426af5913c55b11ea062fa9bb172` |
| Duración | 18:29.7 (1.109,7 s), h264 + aac |
| Tema | SMT: el uso de la SMT bajo esta estrategia (rangos completados/creados que no vimos), los 3 casos, la SMT con DXY (correlación −1), salidas anticipadas e invalidación |
| Prerrequisitos | SMT clásica (ch01, "ya visteis en el capítulo introductorio" [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch05-smt/CLAIMS#c-0001|c-0001]]); rangos/bias (ch03); entradas y descenso de temporalidades (ch04) |
| Referencias | hacia atrás → ch01 (explícito), ch03/ch04 (implícito en la operativa); hacia delante → "el siguiente va a ser de Felux Swing [ASR]" (ep06) [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch05-smt/CLAIMS#c-0100|c-0100]] |

## Provenance de la extracción

| Campo | Valor |
|---|---|
| Fecha | 2026-10-19 |
| Preflight | carga del sistema despejada (load 1min 4,3 tras jobs externos); probe ASR 28 s con config canónica = **0,21× realtime** (rate canónico; sin contención → GO); `integrate_reviews.py` de ch04 generalizado a `scripts/` de la skill (paths por argumento + normalización f-.png integrada) con `integrator_selftest.py` 5/5 |
| ASR | faster-whisper `large-v3`, int8 CPU, language=es (p=1,00), beam 5, 193 segmentos, 96 % habla, ligado al SHA; wall 92,5 min (0,20× realtime) |
| Extracción | 4 subagentes GLM ONE-SHOT en paralelo (bloques 0–5, 5–10, 10–15, 15–18:29.7), 100 claims en 9,7 min |
| Revisión | 19 subagentes ONE-SHOT — UNA revisión por minuto (3 olas de 5/7/7), 19/19 `MINUTE_REVIEW = VALID` (cardinalidad exacta), 34,1 min |
| Integración | mecánica (integrate_reviews.py generalizado + validate_review.py por minuto); 6 correcciones de statement propuestas por reviewers, revisadas y aplicadas por el integrador; 1 corrección de metadato (visual_hint.second de c-0099 1804→1084) |
| Modelo | GLM (subagentes locales de agente; sin API pagada, sin cambio de modelo) |
| Checkpoint 5 min | PASS (26/26 VALID tras minutos 0–4; proyección ≈162 min/h-video → continuar) |

## Métricas

| Métrica | Valor |
|---|---|
| Claims totales | 100 |
| SUPPORTED / UNCERTAIN / UNVERIFIED | 99 / 1 / 0 (la UNCERTAIN es c-0073: deíctico 'la de sentido arriba' sin resolver con contradicción de frames; visibles en documentación y [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch05-smt/OPEN-QUESTIONS|OPEN-QUESTIONS]]) |
| Claims activos / superseded | 100 / 0 (sin supersessions en este capítulo) |
| Epistemic | 83 instructor_statement · 17 visual_observation (todas con frame verificado en `evidence`) · 0 model_inference |
| Contradicciones marcadas | 1 (c-0073 → UNCERTAIN: el dibujo del caso 2 no pasa a velas alcistas) |
| Frames base (fin de minuto) | 19 (minutos 0–17 en MM:59.5 + fin del parcial f-001829, diapositiva "GRACIAS"; manifiesto `frames/.base_frames`) |
| Frames bajo demanda | 62 (extraídos y verificados visualmente por los MINUTE_REVIEWERs, nombres por fórmula desde segundos reales) |
| Preguntas abiertas | 10 (q-ch05-001..010, ver [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch05-smt/OPEN-QUESTIONS|OPEN-QUESTIONS]]) |
| Rules / concepts / examples documentados | 18 / 10 / 7 |
| Coverage | 19/19 minutos de video con claims y revisión |

## Throughput (reporte separado tramos vs total)

| Tramo | Valor |
|---|---|
| ASR wall | 92,5 min (0,20× realtime; partida dominante del total, rate canónico) |
| Extracción wall | 9,7 min (4 subagentes paralelos) |
| Revisión wall | 34,1 min (19 revisores, 3 olas de 5/7/7) |
| Agent wall (extracción+revisión) | ≈44 min para 18,5 min de video ≈ **143 min/h-video** (objetivo ≤120; banda 2× = 240 → PASS; el mejor capítulo hasta ahora: ch03 225, ch04 233) |

## Estructura

- [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch05-smt/documentation|documentation]] — síntesis por conceptos, todo citado
- [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch05-smt/CLAIMS|CLAIMS]] — proyección navegable por claim (autoridad: `claims.jsonl`)
- [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch05-smt/transcript|transcript]] — recurso citable con anchors `^s-HHMMSS`
- [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch05-smt/FRAMES|FRAMES]] — inventario de frames
- [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch05-smt/rules|rules]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch05-smt/concepts|concepts]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch05-smt/examples|examples]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch05-smt/study-guide|study-guide]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch05-smt/review-notes|review-notes]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch05-smt/OPEN-QUESTIONS|OPEN-QUESTIONS]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch05-smt/AMENDMENTS|AMENDMENTS]]

## Run dir

`/home/kor/mke/clutifx-ch05-20261019/` (pool, payloads, reviews, epoch files, context pack).
