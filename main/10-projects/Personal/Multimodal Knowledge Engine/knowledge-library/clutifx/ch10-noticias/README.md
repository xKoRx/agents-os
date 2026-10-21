# ch10-noticias — Clutifx · Capítulo 10

Biblioteca de conocimiento del décimo vídeo del curso Clutifx, extraída con la metodología `course-knowledge-extraction` (skill canónica del vault, NO el pipeline MKE V2), v1.2 + hardening ch03–ch09 (incluida la regla anti-resolución-de-ambigüedades del cierre ch09).

## Identidad de la fuente

| Campo | Valor |
|---|---|
| Archivo | `/home/kor/mke/course/ep10-noticias.mp4` |
| SHA-256 | `cdd6ee7bfcbd5a8e8cab029f3514f4545473965fe4a04a88dfbbe7874dd0d3f1` |
| Duración | 35:48.47 (2148,47 s), h264 + aac |
| Tema | Las NOTICIAS: qué noticias se pueden operar (Excel propio «NEWS - ONE TO ONE ENG» + Myfxbook/Forex Factory), cómo posicionarse (entrar ANTES de la noticia, vela que las contiene), noticias buenas/malas (CPI/GDP/NFP/PMI/FOMC), whipsaw y blow acc, uso con Turtle Soup/Power 3, confirmación por pares correlacionados, DXY simétrico, prop firms/challenges y red flags de noticias — con 3 walkthroughs de días reales |
| Prerrequisitos | ch01 (rango, Turtle Soup, order block, Power of 3), ch02 (noticias 8:30, vela que las contiene, horas clave), ch03 (NFP/CPI llevan al DOL), ch04 (gestión, break even), ch05 (pares correlacionados/DXY), ch06 (failure swing), ch07 (checklist de 4 preguntas — su 4ª pregunta es noticias; vela de las 5 operable con 8:30/8:45), ch09 (red flags) — usados sin redefinir |
| Referencias | hacia atrás → ch01–ch09; hacia delante → el instructor anuncia seguir con los vídeos restantes de la mentoría (c-0199; sin títulos dichos) |

## Provenance de la extracción

| Campo | Valor |
|---|---|
| Fecha | 2026-10-21 |
| ASR | faster-whisper `large-v3`, int8 CPU, language=es (p=1,00), beam 5, **523 segmentos, 97 % habla**, ligado al SHA; wall 2h27m07s = 8.826,8 s medidos por el proceso (`asr.log`); **ASR_SPEED** = 2148,5/8826,8 = **0,24×** (video/wall) · **ASR_COST_MULTIPLIER** = 8826,8/2148,5 = **4,11×** — contención sostenida del host (echo-core + go tests ajenos), dentro del pronóstico del preflight (0,25-0,30×) |
| Extracción | 6 EXTRACTORs ONE-SHOT secuenciales (bloques 0-5 / 6-11 / 12-17 / 18-23 / 24-29 / 30-35), 199 claims; suma de workers ~61 min (~102 min/h-video); ventana 17:38→19:06 con la ola-1 de revisión y adjudicaciones intercaladas (~88 min); 1 muerte [1210] recuperada con retry |
| Revisión | 36 minutos × 1 revisor ONE-SHOT en 7 olas de 5-6: **36/36 `MINUTE_REVIEW = VALID`** (cardinalidad exacta `validate_review.py`); checkpoint 5 min PASS (proyección ~269 min/h-video registrada, OVER, continuado con el criterio ch09); 4 muertes [1210] recuperadas con retry completo |
| Integración | mecánica (`integrate_reviews.py` con safety parcial-integration): **199/199 claims con review aplicado, cobertura total** — canónico escrito sólo con integración COMPLETA; ~50 correcciones de los revisores adjudicadas y aplicadas al pool ANTES de integrar (literalidad restaurada, evidencia de frontera, kinds por hedges, visual_hints falsos corregidos, adjudicaciones visuales con palabra dicha preservada) — detalle en review-notes |
| Modelo | GLM (subagentes locales + integrador; sin API pagada) |
| DOCVERIFY | ver fila de verificación final |
| Checkpoint 5 min | PASS (bloque 1 + min 0-4 VALID; OVER registrado) |

## Métricas

| Métrica | Valor |
|---|---|
| Claims totales | 199 |
| SUPPORTED / UNCERTAIN / UNVERIFIED | 193 / 6 / 0 (c-0030 condición sobre garble; c-0032 observación visual refutada por pantalla; c-0069 y c-0165 contradicción «8 y cuarto» vs 8:30/8:45 de ch02/ch07; c-0113 «6h sin nada» vs «primer rango»; c-0164 vela «de las 7» vs «de las 8» — visibles como dudosos, sin resolución artificial) |
| Claims activos / superseded | 199 / 0 (sin supersessions en este capítulo) |
| Epistemic | 197 instructor_statement · 2 visual_observation · 0 model_inference |
| Contradicciones marcadas | 3 (c-0069/c-0165 vs ch02/ch07; c-0164 interna resuelta visualmente en q-ch10-002 pero claim conserva su veredicto; c-0113 interna) |
| Frames base (fin de minuto) | 36 (minutos 0-34 en MM:59.5 + fin del parcial [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch10-noticias/frames/f-003548.png|f-003548]] (35:48; el nombre incorrecto f-002148 fue cazado por el revisor de min35 y renombrado por fórmula); manifiesto `frames/.base_frames`) |
| Frames bajo demanda | 61 (extraídos y verificados visualmente por los revisores, fórmula desde segundos reales), **91 citados** en total de 97 PNG físicos (6 contextuales sin claims, inventariados — patrón ch09); inventario en [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch10-noticias/FRAMES|FRAMES]] |
| Preguntas abiertas | 14 registradas (q-ch10-001..014): contradicción de horas 8:15/8:30, vela 7/8, garbles del capítulo (USDJPI, Tartel Sub, temperatura, FTPO, enfondeadas…), deícticos del Excel y del walkthrough — ver [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch10-noticias/OPEN-QUESTIONS|OPEN-QUESTIONS]] |
| Rules / concepts / examples documentados | 29 / 14 / 13 |
| Coverage | 36/36 minutos de video con claims y revisión |

## Verificación final

| Gate | Resultado |
|---|---|
| LIBRARY_VALIDATION | ver fila de cierre |
| TERM_SOURCE_CHECK | ver fila de cierre |
| DOCVERIFY | ver fila de verificación final |

## Throughput (reporte separado tramos vs total; nomenclatura normalizada post-ch09)

| Tramo | Valor |
|---|---|
| ASR wall | 2h27m07s = 8.826,8 s (`asr.log`) · ASR_SPEED 0,24× · ASR_COST_MULTIPLIER 4,11× (contención del host, dentro del pronóstico) |
| Agent wall (extracción+revisión) | **156 min** (17:38:16 bloque-1 → 20:14:30 último review, spools/epochs) sobre 35,8 min de video ≈ **262 min/h-video** (objetivo ≤120; OVER ~2,2× — contención sostenida de CPU heredada por workers + revisores prudentes con frames; proyección del checkpoint 269, real 262). Workers puros: extracción ~61 min + revisión ~136 min en olas paralelas |
| Integración + composición | 20:23 (`integration_start_epoch`) → validación/publicación (~40 min: integración mecánica, adjudicación de ~50 correcciones, 5 docs + proyecciones + wikilinks + validadores) |
| TOTAL wall | 15:08 (ASR start) → publicación ≈ 5h55m |

RESOURCE_CONTENTION = **YES** (externa: echo-core 157 % permanente + go tests de otra sesión; ninguna carga ajena fue detenida). THROUGHPUT = **OVER** (registrado sin disfrazar; el checkpoint hizo su trabajo: proyección 269 vs real 262).

## Estructura

- [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch10-noticias/documentation|documentation]] — síntesis por conceptos, todo citado
- [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch10-noticias/CLAIMS|CLAIMS]] — proyección navegable por claim (autoridad: `claims.jsonl`)
- [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch10-noticias/transcript|transcript]] — recurso citable con anchors `^s-HHMMSS`
- [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch10-noticias/FRAMES|FRAMES]] — inventario de frames
- [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch10-noticias/rules|rules]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch10-noticias/concepts|concepts]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch10-noticias/examples|examples]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch10-noticias/study-guide|study-guide]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch10-noticias/review-notes|review-notes]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch10-noticias/OPEN-QUESTIONS|OPEN-QUESTIONS]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch10-noticias/AMENDMENTS|AMENDMENTS]]
