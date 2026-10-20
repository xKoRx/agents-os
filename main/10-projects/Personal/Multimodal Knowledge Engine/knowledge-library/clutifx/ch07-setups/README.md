# ch07-setups — Clutifx · Capítulo 7

Biblioteca de conocimiento del séptimo video del curso Clutifx, extraída con la metodología `course-knowledge-extraction` (skill canónica del vault, NO el pipeline MKE V2), v1.2 + hardening ch03–ch06.

## Identidad de la fuente

| Campo | Valor |
|---|---|
| Archivo | `/home/kor/mke/course/ep07-setups.mp4` |
| SHA-256 | `b20ce8f72bb16760f91a9c692d96e6c702c72ace1ed1e690deb34d93fb7ca726` |
| Duración | 45:35.17 (2735,17 s), h264 + aac |
| Tema | Setups de London y New York: los 3 escenarios de London (TS ya hecho / TS por hacer / expansión pasada → rango pendiente), red flags (apertura por arriba, rangos en contra, DOL tomado), ejemplos reales 4h, setups de New York (continuación vs reversal, vela de las 5 y de las 9, noticias 8:30), y el checklist de 4 preguntas |
| Prerrequisitos | ch02 (sesiones, horas clave), ch03 (rangos a favor/en contra, jerarquía de TFs), ch04 (refinado de entrada, stop en el TS, salida en la vela de las 5), ch05 (SMT, contexto Libra), ch06 (failure swing) — usados sin redefinir |
| Referencias | hacia atrás → ch02–ch06 y curso intermedio ("basado en el tiempo" [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch07-setups/CLAIMS#c-0237|c-0237]]); hacia delante → vídeo de "extras" sobre el reiniciado (anunciado en ch03, no tratado aquí), "red flags" (ep09, anunciado [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch07-setups/CLAIMS#c-0033|c-0033]]), "nos vemos en el siguiente" [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch07-setups/CLAIMS#c-0238|c-0238]] (ep08-proceso) |

## Provenance de la extracción

| Campo | Valor |
|---|---|
| Fecha | 2026-10-20 |
| Continuidad | REANUDADO: intento 1 de la mañana perdió el ASR en un doble reboot del host (sin transcript); frames base 46 + manifiesto del intento 1 reutilizados íntegros; ASR relanzado 17:01 sin duplicar proceso |
| ASR | faster-whisper `large-v3`, int8 CPU, language=es (p=1,00), beam 5, **480 segmentos, 98 % habla**, ligado al SHA; wall 68,3 min (0,68× realtime, el mejor rate del curso) |
| Extracción | 6 subagentes ONE-SHOT en paralelo (bloques 0–8:16 / 8:16–16 / 16–24 / 24–32 / 32–39 / 39–45:35), 238 claims en 11 min |
| Revisión | 46 minutos × 1 revisor (UNA revisión por minuto): 23 minutos por subagentes ONE-SHOT; **23 minutos por el integrador-revisor (fallback)** tras el agotamiento de la cuota del proveedor `[1310]` a las ~19:00 (reset 2026-10-25) — ver [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch07-setups/review-notes|review-notes]]; 46/46 `MINUTE_REVIEW = VALID` |
| Integración | mecánica (`integrate_reviews.py` + `validate_review.py` por minuto); 28 correcciones propuestas por revisores aplicadas vía pool (evidence, literalidad, hints, 1 re-adjudicación de epistemic) |
| Modelo | GLM (subagentes locales + integrador; sin API pagada) |
| Checkpoint 5 min | PASS (23/23 VALID; proyección ~89 min/h-video → real ~74) |

## Métricas

| Métrica | Valor |
|---|---|
| Claims totales | 238 |
| SUPPORTED / UNCERTAIN / UNVERIFIED | 238 / 0 / 0 |
| Claims activos / superseded | 238 / 0 (sin supersessions en este capítulo) |
| Epistemic | 226 instructor_statement · 12 visual_observation (con frame verificado en `evidence`) · 0 model_inference |
| Contradicciones marcadas | 0 |
| Frames base (fin de minuto) | 46 (minutos 0–44 en MM:59.5 + fin del parcial [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch07-setups/frames/f-004535.png|f-004535]]; manifiesto `frames/.base_frames`, reutilizado del intento 1) |
| Frames bajo demanda | 80 (46 de revisores subagente + 34 del integrador-revisor), **64 citados** en total; inventario en [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch07-setups/FRAMES|FRAMES]] |
| Preguntas abiertas | 18 registradas (q-ch07-001..018): mayormente confirmación de audio de garbles (familia DOL, Turtle Soup, Power of 3) — ver [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch07-setups/OPEN-QUESTIONS|OPEN-QUESTIONS]] |
| Rules / concepts / examples documentados | 28 / 13 / 11 |
| Coverage | 46/46 minutos de video con claims y revisión |

## Throughput (reporte separado tramos vs total)

| Tramo | Valor |
|---|---|
| ASR wall | 68,3 min (0,68× realtime) |
| Extracción wall | 11 min (6 subagentes paralelos) |
| Revisión wall | 45 min (híbrido: subagentes + integrador tras cuota agotada) |
| Agent wall (extracción+revisión) | ≈56 min / 45,6 min video ≈ **74 min/h-video** (objetivo ≤120 → PASS, el mejor del curso: ch06 98–108, ch05 143, ch04 233, ch03 225) |

## Estructura

- [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch07-setups/documentation|documentation]] — síntesis por conceptos, todo citado
- [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch07-setups/CLAIMS|CLAIMS]] — proyección navegable por claim (autoridad: `claims.jsonl`)
- [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch07-setups/transcript|transcript]] — recurso citable con anchors `^s-HHMMSS`
- [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch07-setups/FRAMES|FRAMES]] — inventario de frames
- [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch07-setups/rules|rules]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch07-setups/concepts|concepts]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch07-setups/examples|examples]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch07-setups/study-guide|study-guide]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch07-setups/review-notes|review-notes]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch07-setups/OPEN-QUESTIONS|OPEN-QUESTIONS]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch07-setups/AMENDMENTS|AMENDMENTS]]
