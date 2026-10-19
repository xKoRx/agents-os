# ch04-entradas — Clutifx · Capítulo 4

Biblioteca de conocimiento del cuarto video del curso Clutifx, extraída con la metodología `course-knowledge-extraction` (skill canónica del vault, NO el pipeline MKE V2), v1.2 + hardening ch03/ch04.

## Identidad de la fuente

| Campo | Valor |
|---|---|
| Archivo | `/home/kor/mke/course/ep04-entradas.mp4` |
| SHA-256 | `f69f7d621463471a7516a05f21063ea6d42408a5ecfd9310d455addce8cf0d32` |
| Duración | 27:35.4 (1.655,4 s), h264 + aac |
| Tema | ENTRADAS: el esquema (orden Turtle Soup → PDM/order block → Power 3 + rango pendiente), el refinado por temporalidades, cuatro ejemplos reales EURUSD y la gestión/salida |
| Prerrequisitos | bias (ch03, explícito: "en el episodio anterior se vio cómo se encuentra el dol") [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch04-entradas/CLAIMS#c-0024|c-0024]]; horas clave y sesiones (ch02) |
| Referencias | hacia atrás → ch03 (DOL) y ch01 (Turtle Soup, order block, Power of 3); hacia delante → "en el siguiente vídeo hablará de la SMT" (ep05) [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch04-entradas/CLAIMS#c-0119|c-0119]] |

## Provenance de la extracción

| Campo | Valor |
|---|---|
| Fecha | 2026-10-19 |
| Preflight | supersession safety (V14–V16 + lifecycle en CLAIMS), remediation DOL/DXY de ch02 (2 supersessions) y hardening SOURCE-FIRST (TERM_DISAMBIGUATION_REQUIRED + aliases de garbles) — los 5 gates PASS antes de extraer |
| ASR | faster-whisper `large-v3`, int8 CPU, language=es (p=1,00), beam 5, 359 segmentos, 98 % habla, ligado al SHA; wall 4h10m (0,11× realtime — máquina compartida con otros jobs; rate canónico previo 0,21–0,38×) |
| Extracción | 6 subagentes GLM ONE-SHOT en paralelo (bloques 0–5, 5–10, 10–15, 15–20, 20–25, 25–27:35), 119 claims en 15,3 min |
| Revisión | 28 subagentes ONE-SHOT — UNA revisión por minuto (4 olas de 5/7/7/9), 28/28 `MINUTE_REVIEW = VALID` (cardinalidad exacta), 91,9 min |
| Integración | mecánica (`integrate_reviews.py` + `validate_review.py` por minuto); 7 correcciones de statement propuestas por reviewers, revisadas por el integrador y aplicadas; 1 adjudicación V13 (c-0016 model_inference→instructor_statement); 1 frame del extractor rechazado por mostrar otro timeframe (c-0083) |
| Modelo | GLM (subagentes locales de agente; sin API pagada, sin cambio de modelo) |
| Checkpoint 5 min | PASS (21/21 VALID; proyección 152 min/h-video → continuar) |
| Run dir | `/home/kor/mke/clutifx-ch04-20261019/` |

## Métricas

| Métrica | Valor |
|---|---|
| Claims totales | 119 |
| SUPPORTED / UNCERTAIN / UNVERIFIED | 111 / 8 / 0 (los UNCERTAIN son garbles ASR irresolubles o deícticos sin frame; visibles en documentación y [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch04-entradas/OPEN-QUESTIONS|OPEN-QUESTIONS]]) |
| Claims activos / superseded | 119 / 0 (sin supersessions en este capítulo) |
| Epistemic | 109 instructor_statement · 9 visual_observation (todas con frame verificado en `evidence`) · 0 model_inference (c-0016 adjudicada) |
| Contradicciones marcadas | 1 (c-0078 TP arriba/abajo → UNCERTAIN) |
| Frames base (fin de minuto) | 28 (minutos 0–26 en MM:59.5 + fin del parcial f-002734, pantalla negra; manifiesto `frames/.base_frames`) |
| Frames bajo demanda | 77 (extraídos y verificados visualmente por los MINUTE_REVIEWERs, nombres por fórmula desde segundos reales) |
| Preguntas abiertas | 19 (q-ch04-001..019, ver [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch04-entradas/OPEN-QUESTIONS|OPEN-QUESTIONS]]) |
| Rules / concepts / examples documentados | 27 / 11 / 8 |
| Coverage | 28/28 minutos de video con claims y revisión |

## Throughput (reporte separado tramos vs total)

| Tramo | Valor |
|---|---|
| ASR wall | 4h10m (0,11× realtime; partida dominante del total por carga externa de la máquina) |
| Extracción wall | 15,3 min (6 subagentes paralelos) |
| Revisión wall | 91,9 min (28 revisores, 4 olas de 5/7/7/9) |
| Agent wall (extracción+revisión) | 107,2 min para 27,6 min de video ≈ **233 min/h-video** (objetivo ≤120; banda 2× = 240 → continúa; exceso por verificación visual frame-a-frame, igual que ch03) |

## Estructura

- [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch04-entradas/documentation|documentation]] — síntesis por conceptos, todo citado
- [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch04-entradas/CLAIMS|CLAIMS]] — proyección navegable por claim (autoridad: `claims.jsonl`)
- [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch04-entradas/transcript|transcript]] — recurso citable con anchors `^s-HHMMSS`
- [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch04-entradas/FRAMES|FRAMES]] — inventario de frames
- [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch04-entradas/rules|rules]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch04-entradas/concepts|concepts]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch04-entradas/examples|examples]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch04-entradas/study-guide|study-guide]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch04-entradas/review-notes|review-notes]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch04-entradas/OPEN-QUESTIONS|OPEN-QUESTIONS]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch04-entradas/AMENDMENTS|AMENDMENTS]]
