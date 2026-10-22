# ch11-riesgo — Clutifx · Capítulo 11

Biblioteca de conocimiento del undécimo vídeo del curso Clutifx, extraída con la metodología `course-knowledge-extraction` (skill canónica del vault, NO el pipeline MKE V2), v1.2 + hardening ch03-ch10.

## Identidad de la fuente

| Campo | Valor |
|---|---|
| Archivo | `/home/kor/mke/course/ep11-riesgo.mp4` |
| SHA-256 | `590e4c3c1d4ab04073faaeae38580857d467693c3ac5efe48b17bb62f90767b6` |
| Duración | 26:21.42 (1581,42 s), h264 1080p, 108,5 MB |
| Tema | Gestión de RIESGO y gestión del TRADE: riesgo por etapa (challenge fase 1/fase 2, fondeada, live), la lógica del cobro (payouts → retiro → challenges), break even (por estructura, no por R), parciales (tamaños y ejemplos dichos), stop loss (no se mueve, debajo del Turtle Soup, margen por expansión, intra-TS y reentrada), salida basada en tiempo, el trade de ayer (ejemplo personal), fondeadas vs challenge (parciales como reducción de riesgo), psicología (avaricia vs miedo), pirámides (test contrafáctico, mecánica en challenge, nunca en fondeada, excepción drawdown) y el cierre del curso (último episodio de la base dicho) |
| Prerrequisitos | ch01 (rango, Turtle Soup, order block, Power of 3), ch02 (horas clave, vela de las 5), ch03 (bias/DOL), ch04 (gestión, break even, parciales, vela de las 5 como salida), ch05 (pares correlacionados), ch07 (setups, trade del 4-jun), ch08 (proceso, targets 1d/2d), ch09 (red flags), ch10 (el trade de noticias que retoma, displacement en noticia) — usados sin redefinir |
| Referencias | hacia atrás → ch04/ch07/ch08/ch09/ch10 (explícitos: «el vídeo de noticias», «lo que os decía en el capítulo de noticias», el trade de ayer); hacia delante → «este va a ser el último episodio como tal de frente a la estrategia... de la base creada del curso este va a ser el último ya» ([[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch11-riesgo/CLAIMS#c-0079|c-0079]]); ep12-psicotrading queda anunciado en ch09 pero fuera de la base de estrategia según este cierre |

## Provenance de la extracción

| Campo | Valor |
|---|---|
| Fecha | 2026-10-22 (ASR iniciado 2026-10-21 23:17) |
| ASR | faster-whisper `large-v3`, int8 CPU, language=es (p=1,00), beam 5, **320 segmentos, 96 % habla**, ligado al SHA; wall proceso 5.765,7 s = 1h36m06s (`asr.log`); **ASR_SPEED** = 1581,4/5765,7 = **0,27×** · **ASR_COST_MULTIPLIER** = 5765,7/1581,4 = **3,64×** — dentro del pronóstico del preflight (0,24-0,28× con la contención del host anunciada) |
| Extracción | 6 EXTRACTORs ONE-SHOT SECUENCIALES (bloques 0-4 / 5-9 / 10-14 / 15-19 / 20-24 / 25-26), 80 claims; ~50,6 min totales (7,1 + 43,5) |
| Revisión | 27 MINUTE_REVIEWERs ONE-SHOT en 6 olas (5/5/5/5/5/2): **27/27 `MINUTE_REVIEW = VALID`** (cardinalidad exacta); pure makespan ≈ 42,9 min; ventana extracción+revisión ≈ 100,5 min ≈ **229 min/h-video — OVER** (objetivo ≤120; contención del host: echo-core 164 % + go test ajeno, nada detenido); **0 muertes de proveedor** |
| Checkpoint 5 min | PASS (bloque 1 + min 0-4 VALID en ~15,6 min; proyección 240-250 min/h-video OVER registrada ANTES de continuar; real ~229) |
| Integración | mecánica (`integrate_reviews.py` con el contrato de evidencia visual del closeout ch10): **80/80 claims con review aplicado, cobertura total** — canónico escrito sólo con integración COMPLETA; 26 correcciones de los revisores adjudicadas y aplicadas al pool ANTES de integrar (literalidad restaurada, anclas load-bearing, evidencia de frontera, visual_hints corregidos) — detalle en [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch11-riesgo/review-notes|review-notes]] |
| Modelo | GLM (subagentes locales + integrador; sin API pagada) |
| DOCVERIFY | independiente ONE-SHOT: **PASS_WITH_FINDINGS (0 MATERIAL + 4 MENOR)** — SOURCE-FIRST 17 claims con cifras contrastados contra transcript+frames (0 discrepancias), 15 garbles preservados, 12 q-ch11 barridas contra la síntesis sin resolverse, 1160 wikilinks OK, SHA recomputado idéntico; los 4 MENOR corregidos y re-validados (cirílica en R26, headings de concepts, conteo de contextuales 33, glosa interna en E13) |

## Métricas

| Métrica | Valor |
|---|---|
| Claims totales | 80 |
| SUPPORTED / UNCERTAIN / UNVERIFIED | 79 / 1 / 0 ([[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch11-riesgo/CLAIMS#c-0068|c-0068]] — la aritmética de la excepción de drawdown: «un 1 y un 0,5» sin pronunciar «%», los % de pantalla son de TradingView y el capital de referencia no está dicho — visible como dudoso, sin resolución artificial) |
| Claims activos / superseded | 80 / 0 (sin supersessions en este capítulo) |
| Epistemic | 80 instructor_statement · 0 visual_observation · 0 model_inference (capítulo VERBAL: la sustancia es dicha; los frames sostienen deícticos) |
| Frames base (fin de minuto) | 27 (minutos 0-25 en MM:59.5 + fin del parcial [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch11-riesgo/frames/f-002621.png|f-002621]] (26:21; nombre por fórmula — el pack del Manager decía «f-001621» y el extractor lo cazó); manifiesto `frames/.base_frames`) |
| Frames bajo demanda | 60 (extraídos y verificados visualmente por revisores/extractor, fórmula desde segundos reales; incluidas las capturas de auditoría contextual de los revisores — patrón ch09/ch10), **54 citados** en total de 87 PNG físicos (33 contextuales sin citar — 17 base + 16 demanda, inventariados); inventario en [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch11-riesgo/FRAMES|FRAMES]] |
| Preguntas abiertas | 12 registradas (q-ch11-001..012): capital de referencia de los %, cuadro «challenges/0,5%» en pantalla, unidades de cifras dichas, deícticos de gráfico, garbles [ASR], «10 horas» del trade de ayer, segmento truncado del BE de parciales, cobertura fronteriza, «en 5 minutos» vs TF en pantalla, objetivos 8h/12h sin etiqueta, alcance «no se mueve» vs BE — ver [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch11-riesgo/OPEN-QUESTIONS|OPEN-QUESTIONS]] |
| Rules / concepts / examples documentados | 34 / 12 / 15 |
| Coverage | 27/27 minutos de video con claims y revisión |

## Verificación final

| Gate | Resultado |
|---|---|
| LIBRARY_VALIDATION | **PASS** (findings=0, 87 frames/80 claims; re-validado tras corregir los 4 MENOR del DOCVERIFY) |
| TERM_SOURCE_CHECK | **PASS** (80 claims vivos, 0 MATERIAL, 0 TERM_DISAMBIGUATION_REQUIRED) |
| DOCVERIFY | **PASS tras corrección** (0 MATERIAL + 4 MENOR corregidos y verificados contra el árbol físico) |

```text
CH11 = DONE
CH11_SOURCE_INTEGRITY = PASS · CH11_LIFECYCLE = PASS · CH11_SOURCE_FIRST = PASS
CH11_LIBRARY_VALIDATION = PASS · CH11_DOCVERIFY = PASS (0 MATERIAL, 4 MENOR corregidos)
```

## Throughput (reporte separado tramos vs total; nomenclatura normalizada post-ch09)

| Tramo | Valor |
|---|---|
| ASR wall | 5.765,7 s = 1h36m06s (`asr.log`) · ASR_SPEED 0,27× · ASR_COST_MULTIPLIER 3,64× (contención del host anunciada en preflight) |
| Agent wall (extracción+revisión) | ventana ≈ 100,5 min sobre 26,36 min de video ≈ **229 min/h-video** (objetivo ≤120; OVER ~1,9× — contención sostenida del host; proyección del checkpoint 240-250, real 229). Workers puros: extracción ~50,6 min + revisión ~42,9 min de makespan |
| Integración + composición | ~40 min (integración mecánica, adjudicación de 26 correcciones, 5 docs + proyecciones + wikilinks + validadores) |
| TOTAL wall | 23:17 (ASR start) → publicación ≈ 3h10m |

RESOURCE_CONTENTION = **YES** (externa: echo-core 164 % permanente + go test ajeno; ninguna carga ajena fue detenida). THROUGHPUT = **OVER** (registrado sin disfrazar; el checkpoint proyectó 240-250 y el real fue 229).

## Estructura

- [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch11-riesgo/documentation|documentation]] — síntesis por conceptos, todo citado
- [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch11-riesgo/CLAIMS|CLAIMS]] — proyección navegable por claim (autoridad: `claims.jsonl`)
- [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch11-riesgo/transcript|transcript]] — recurso citable con anchors `^s-HHMMSS`
- [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch11-riesgo/FRAMES|FRAMES]] — inventario de frames
- [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch11-riesgo/rules|rules]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch11-riesgo/concepts|concepts]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch11-riesgo/examples|examples]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch11-riesgo/study-guide|study-guide]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch11-riesgo/review-notes|review-notes]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch11-riesgo/OPEN-QUESTIONS|OPEN-QUESTIONS]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch11-riesgo/AMENDMENTS|AMENDMENTS]]
