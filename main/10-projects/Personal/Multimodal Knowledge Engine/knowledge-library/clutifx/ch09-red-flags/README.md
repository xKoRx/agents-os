# ch09-red-flags — Clutifx · Capítulo 9

Biblioteca de conocimiento del noveno vídeo del curso Clutifx, extraída con la metodología `course-knowledge-extraction` (skill canónica del vault, NO el pipeline MKE V2), v1.2 + hardening ch03–ch08.

## Identidad de la fuente

| Campo | Valor |
|---|---|
| Archivo | `/home/kor/mke/course/ep09-red-flags.mp4` |
| SHA-256 | `e4c221025d94f0f2aef33ab3a63b60a22ffbd536fd506a079a93f083b12e47db` |
| Duración | 34:54.53 (2094,53 s), h264 + aac |
| Tema | Las RED FLAGS: señales negativas que pueden indicar no tomar un trade — (1) velas que abren al revés / rangos en contra (sobre todo en horas clave 3/5/8/9), (2) inside candles, (3) el objetivo ya tomado, y (4) el par correlacionado que ya completó su target; fuerza probabilística de cada una (advertencias vs invalidaciones), gestión ante contradicción del setup, errores retrospectivos y la secuencia de sesiones 1-5-9 con la expansión de Asia |
| Prerrequisitos | ch01 (rango, Turtle Soup, order block), ch02 (horas clave), ch03 (rangos a favor/en contra, jerarquía TFs), ch04 (break even, refinado), ch05 (SMT/pares correlacionados — conexión explícita c-0128), ch06 (failure swing), ch07 (setups, checklist; la red flag anunciada en su c-0033 se desarrolla aquí), ch08 (proceso) — usados sin redefinir |
| Referencias | hacia atrás → ch01–ch08; hacia delante → quedan anunciados «un vídeo de gestión de riesgo y de trades», «un vídeo de las noticias... cuáles son las noticias mejores para operar» y «alguno de mentalidad» [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch09-red-flags/CLAIMS#c-0137|c-0137]] (ep10+, sin título dicho) |

## Provenance de la extracción

| Campo | Valor |
|---|---|
| Fecha | 2026-10-21 |
| ASR | faster-whisper `large-v3`, int8 CPU, language=es (p=1,00), beam 5, **430 segmentos, 96 % habla**, ligado al SHA; wall 2h09m46s (0,27× realtime — el peor rate del curso: contención severa del host, load 15 con echo-core + test Go de otro grind) |
| Extracción | 6 EXTRACTORs ONE-SHOT secuenciales (bloques 0-5 / 6-11 / 12-17 / 18-23 / 24-29 / 30-34), 137 claims, ~49 min |
| Revisión | 35 minutos × 1 revisor ONE-SHOT en 7 olas de 5: **35/35 `MINUTE_REVIEW = VALID`** (cardinalidad exacta `validate_review.py`); checkpoint 5 min PASS (proyección ~140 min/h-video, OVER <2×, continuado con registro); 0 errores [1210]/[1310] del proveedor |
| Integración | mecánica (`integrate_reviews.py` con fix de seguridad parcial-integration del preflight ch09: sólo escribe canónico con cobertura completa) + 12 correcciones de literalidad propuestas por revisores, adjudicadas y aplicadas al pool antes de integrar |
| Modelo | GLM (subagentes locales + integrador; sin API pagada) |
| DOCVERIFY | ver fila de verificación final |
| Checkpoint 5 min | PASS (min 0-4 VALID en ~12 min; OVER <2× del objetivo, continuado con registro) |

## Métricas

| Métrica | Valor |
|---|---|
| Claims totales | 137 |
| SUPPORTED / UNCERTAIN / UNVERIFIED | 135 / 2 / 0 (c-0063 alcance del hedge «normalmente»; c-0075 contradicción «4 horas» dicho vs «2h» visible — visibles como dudosos, no forzados) |
| Claims activos / superseded | 137 / 0 (sin supersessions en este capítulo) |
| Epistemic | 133 instructor_statement · 4 visual_observation · 0 model_inference |
| Contradicciones marcadas | 1 (c-0075, CONTRADICTION: temporalidad del ejemplo) |
| Frames base (fin de minuto) | 35 (minutos 0-33 en MM:59.5 + fin del parcial [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch09-red-flags/frames/f-003454.png|f-003454]] — tarjeta de despedida, no citado; manifiesto `frames/.base_frames`) |
| Frames bajo demanda | 38 (extraídos y verificados visualmente por los revisores, fórmula desde segundos reales), **54 citados** en total; inventario en [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch09-red-flags/FRAMES|FRAMES]] |
| Preguntas abiertas | 16 registradas (q-ch09-001..016): garbles del capítulo (reza, JEP/JP/GIP, S&T, RT es menace, tarjeta breakable, azista, dark del sub), enumeración de red flags, deícticos de dibujo, alcance del hedge de c-0063, temporalidad de c-0075, deudas cross-chapter — ver [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch09-red-flags/OPEN-QUESTIONS|OPEN-QUESTIONS]] |
| Rules / concepts / examples documentados | 9 / 10 / 18 |
| Coverage | 35/35 minutos de video con claims y revisión |

## Verificación final

| Gate | Resultado |
|---|---|
| LIBRARY_VALIDATION | PASS (ver registro del run) |
| TERM_SOURCE_CHECK | PASS (ver registro del run) |
| DOCVERIFY | (independiente ONE-SHOT sobre esta biblioteca publicada; su veredicto queda registrado aquí tras ejecutarse) |

## Throughput (reporte separado tramos vs total)

| Tramo | Valor |
|---|---|
| ASR wall | 2h09m46s (0,27× realtime — contención del host, OVER registrado) |
| Agent wall (extracción+revisión) | ~109 min / 34,9 min video ≈ **187 min/h-video** (objetivo ≤120; OVER por contención de CPU heredada por los subagentes y revisores prudentes con frames; registrado sin disfrazar) |
| Integración + composición | (ver PREFLIGHT-GATE/run del 2026-10-21) |

## Estructura

- [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch09-red-flags/documentation|documentation]] — síntesis por conceptos, todo citado
- [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch09-red-flags/CLAIMS|CLAIMS]] — proyección navegable por claim (autoridad: `claims.jsonl`)
- [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch09-red-flags/transcript|transcript]] — recurso citable con anchors `^s-HHMMSS`
- [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch09-red-flags/FRAMES|FRAMES]] — inventario de frames
- [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch09-red-flags/rules|rules]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch09-red-flags/concepts|concepts]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch09-red-flags/examples|examples]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch09-red-flags/study-guide|study-guide]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch09-red-flags/review-notes|review-notes]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch09-red-flags/OPEN-QUESTIONS|OPEN-QUESTIONS]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch09-red-flags/AMENDMENTS|AMENDMENTS]]
