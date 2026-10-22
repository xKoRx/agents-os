# ch12-psicotrading — Clutifx · Capítulo 12

Biblioteca de conocimiento del duodécimo y último vídeo del inventario actual del curso Clutifx, extraída con la metodología `course-knowledge-extraction` (skill canónica del vault, NO el pipeline MKE V2), v1.2 + hardening ch03-ch11.

## Identidad de la fuente

| Campo | Valor |
|---|---|
| Archivo | `/home/kor/mke/course/ep12-psicotrading.mp4` |
| SHA-256 | `b9fc83c579547667a3f64c9d326ee3322d4afb389fa0ed3870b642c607f147c6` |
| Duración | 31:24.25 (1884,25 s), h264 1280x720 + AAC, 80,3 MB |
| Tema | PSICOTRADING/mentalidad — «un pequeño vídeo de psicología que me habéis pedido»: la experiencia propia del instructor sobre gestión de emociones aplicada a esta estrategia (confianza antes de operar, el límite del 1% y la aritmética de la calma, la escalera del descontrol, buscar buenos trades y no dinero, la prisa y el tiempo a favor, herramientas prácticas —cerrar gráficos, múltiples cuentas, journal del estado mental—, challenges vs fondeadas, verlo como inversión). Es el capítulo anunciado en ch09 ([[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch09-red-flags/CLAIMS#c-0137|ch09 c-0137]] «mentalidad») y situado por el instructor en ch11 ([[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch11-riesgo/CLAIMS#c-0079|ch11 c-0079]]) FUERA de la base de estrategia. TODO el contenido es relato de experiencia dicho — ninguna cifra o promesa es una validación empírica. |
| Prerrequisitos | ch01-ch11 usados sin redefinir (challenge/fase 2, fondeada, drawdown, riesgo 1%, revenge trading). SIN referencias intercapítulo dichas: 0 menciones de «capítulo»/«vídeo de» en el transcript; los «lo he dicho antes» son intra-vídeo (s-001647, s-002618, s-002813, s-003011) |
| Referencias | hacia atrás → ninguna dicha (conexión temática documentada en documentation §16); hacia delante → sin anuncios de episodios (despedida abierta a peticiones, [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch12-psicotrading/CLAIMS#c-0135|c-0135]]) — cierre del inventario actual del curso |

## Provenance de la extracción

| Campo | Valor |
|---|---|
| Fecha | 2026-10-22 (ASR iniciado 08:51 local) |
| ASR | faster-whisper `large-v3`, int8 CPU, language=es (p=1,00), beam 5, **583 segmentos, 99 % habla (el más denso del curso)**, ligado al SHA; wall proceso 10.373,5 s = 172,9 min (`asr.log`); **ASR_SPEED** = 1884,25/10373,5 = **0,18×** · **ASR_COST_MULTIPLIER** = 5,50× — POR DEBAJO del pronóstico del preflight (0,24-0,28×): contención nueva en vuelo (functions.test + postgres.test ajenos desde el minuto ~46 del ASR, load 15-19; el proceso cayó de ~200 % a ~133 % CPU); nada ajeno detenido |
| Extracción | 6 EXTRACTORs ONE-SHOT SECUENCIALES (bloques 0-5 / 6-10 / 11-15 / 16-20 / 21-25 / 26-31), 135 claims; makespan 80,8 min, runtime puro ≈ 66,8 min |
| Revisión | 32 MINUTE_REVIEWERs ONE-SHOT en 6 olas (5/5/5/5/5/7): **32/32 `MINUTE_REVIEW = VALID`** (cardinalidad exacta); makespan puro de olas ≈ 40,3 min; ventana extracción+revisión ≈ 88,9 min ≈ **170 min/h-video — OVER** (objetivo ≤120, ~1,4×; contención del host); **0 muertes de proveedor en 33 subagentes** |
| Checkpoint 5 min | PASS (bloque 1 + min 0-4 en ~22,6 min; proyección 144 min/h-video OVER 1,2× registrada ANTES de continuar; real 170 — la revisión del pronóstico por la contención en vuelo está en review-notes) |
| Integración | mecánica (`integrate_reviews.py`, integración COMPLETA 32/32, cobertura 135/135) + 28 correcciones adjudicadas al pool ANTES de integrar + 5 frames targeted-adjudicados con prueba md5 (`evidence-adjudications.json`); IDs globales c-0001..c-0135 asignados post-integración; detalle en [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch12-psicotrading/review-notes|review-notes]] |
| Modelo | GLM (subagentes locales + integrador; sin API pagada) |
| DOCVERIFY | independiente ONE-SHOT: **PASS_WITH_FINDINGS (6 MATERIAL + 3 MENOR)** — 17 claims con cifras + 8 [ASR] contrastados contra transcript (0 discrepancias en claims.jsonl), SHA recomputado idéntico, foco mandato (endurecimientos de hedges ×2, generalización desde experiencia ×1); los 9 corregidos y re-validados |

## Métricas

| Métrica | Valor |
|---|---|
| Claims totales | 135 |
| SUPPORTED / UNCERTAIN / UNVERIFIED | 135 / 0 / 0 (capítulo de relato sin claims visuales: los 18 frames citados sostienen deícticos, no observaciones load-bearing) |
| Claims activos / superseded | 135 / 0 (sin supersessions en este capítulo) |
| Epistemic | 135 instructor_statement · 0 visual_observation · 0 model_inference (99 % habla; las promesas de win-rate y los mecanismos psicológicos se publican como DICHO del instructor con su condicional) |
| Frames base (fin de minuto) | 32 (minutos 0-30 en MM:59.5 + fin de video [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch12-psicotrading/frames/f-003124.png|f-003124]] a 31:24); manifiesto `frames/.base_frames` |
| Frames bajo demanda | 21 (extraídos y verificados visualmente por extractores/revisores/integrador, fórmula desde segundos reales), **18 citados** en evidence de 53 PNG físicos (35 contextuales inventariados); inventario en [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch12-psicotrading/FRAMES|FRAMES]] |
| Preguntas abiertas | 11 registradas (q-ch12-001..011): garbles ASR de audio (toblos/estoblos, fumo, C&K, propiedad/esbeona, draw claro…), signos del caso del alumno, unidades no dichas, deícticos de gráfico, tweet/PDFs no verificables, truncamientos del ASR — ver [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch12-psicotrading/OPEN-QUESTIONS|OPEN-QUESTIONS]] |
| rules/concepts/examples | 71 (43 R + 28 W) / 22 / 15 entradas (23 de los 34 example claims) |
| Coverage | 32/32 minutos de video con claims y revisión |

## Verificación final

| Gate | Resultado |
|---|---|
| LIBRARY_VALIDATION | **PASS** (findings=0, 53 frames/135 claims; re-validado tras corregir los 9 findings del DOCVERIFY) |
| TERM_SOURCE_CHECK | **PASS** (135 claims vivos, 0 MATERIAL, 0 TERM_DISAMBIGUATION_REQUIRED) |
| DOCVERIFY | **PASS tras corrección** (6 MATERIAL + 3 MENOR corregidos y verificados contra el árbol físico) |

```text
CH12 = DONE
CH12_SOURCE_INTEGRITY = PASS · CH12_LIFECYCLE = PASS · CH12_SOURCE_FIRST = PASS
CH12_LIBRARY_VALIDATION = PASS · CH12_DOCVERIFY = PASS (6 MATERIAL + 3 MENOR corregidos)
```

## Throughput (reporte separado tramos vs total; nomenclatura normalizada post-ch09; conciliado contra epochs/spools del run dir)

| Tramo | Valor |
|---|---|
| ASR wall | 10.373,5 s = 172,9 min (`asr.log`; ventana epochs 08:51:12→11:44:22 = 173,2 min) · ASR_SPEED 0,18× · ASR_COST_MULTIPLIER 5,50× (contención en vuelo: go tests ajenos desde el minuto ~46) |
| Agent wall (extracción+revisión) | ventana ≈ 88,9 min sobre 31,4 min de video ≈ **170 min/h-video** (objetivo ≤120; OVER ~1,4× — contención del host; proyección del checkpoint 144, real 170). Workers puros: extracción ≈ 66,8 min + revisión ≈ 40,3 min de makespan en olas (interleaved con extracción) |
| Integración + composición + DOCVERIFY | 44,5 min (epochs 13:23:02→14:07:33: integración mecánica + 28 correcciones + 5 adjudicaciones + 5 docs + proyecciones + validadores + corrección del renombre erróneo + DOCVERIFY y sus 9 correcciones) |
| TOTAL wall (a fin de integración) | 08:51:12 → 14:07:33 ≈ **316 min ≈ 5h16m**; a publicación remota se completa con el tramo de commit/push (ver AMENDMENTS/handoff si se necesita la cifra exacta) |

RESOURCE_CONTENTION = **YES** (externa: echo-core 173 % permanente + functions.test/postgres.test ajenos intermitentes; ninguna carga ajena fue detenida). THROUGHPUT = **OVER** (registrado sin disfrazar).

## Estructura

- [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch12-psicotrading/documentation|documentation]] — síntesis por conceptos, todo citado
- [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch12-psicotrading/CLAIMS|CLAIMS]] — proyección navegable por claim (autoridad: `claims.jsonl`)
- [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch12-psicotrading/transcript|transcript]] — recurso citable con anchors `^s-HHMMSS`
- [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch12-psicotrading/FRAMES|FRAMES]] — inventario de frames
- [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch12-psicotrading/rules|rules]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch12-psicotrading/concepts|concepts]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch12-psicotrading/examples|examples]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch12-psicotrading/study-guide|study-guide]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch12-psicotrading/review-notes|review-notes]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch12-psicotrading/OPEN-QUESTIONS|OPEN-QUESTIONS]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch12-psicotrading/AMENDMENTS|AMENDMENTS]]
