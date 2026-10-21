# ch08-proceso — Clutifx · Capítulo 8

Biblioteca de conocimiento del octavo video del curso Clutifx, extraída con la metodología `course-knowledge-extraction` (skill canónica del vault, NO el pipeline MKE V2), v1.2 + hardening ch03–ch07 (incl. checks W11/W12 de navegación y el wikilinker corregido).

## Identidad de la fuente

| Campo | Valor |
|---|---|
| Archivo | `/home/kor/mke/course/ep08-proceso.mp4` |
| SHA-256 | `5495798bf849ef1fd3f57f7304784ec508bb844e65039e9a5a132361169cbf36` |
| Duración | 17:04.42 (1024,42 s), h264 + aac |
| Tema | El proceso de análisis desde cero: "cómo se tendría que entrar al gráfico desde cero… hasta llegar a tomar tu billete [ASR: trade]" — demostrado en 4 pares (ORO, AUDUSD, USDCAD, EURUSD en vivo), bajando temporalidades desde 1 año, marcando rangos y construyendo una narrativa; reglas de rangos enfrentados ("no intentar adivinar"), ventana ideal de entrada (antes de que los rangos estén completados), gestión en el trade (BE, lo que NO quieres ver, salida por precaución) y el cierre "nunca vendáis mientras se forman rangos alcistas" |
| Prerrequisitos | ch02 (rangos, horas clave), ch03 (jerarquía de TFs, rangos a favor), ch04 (refinado, gestión), ch05 (SMT/pares correlacionados), ch06 (failure swing), ch07 (setups de sesión) — usados sin redefinir |
| Referencias | hacia atrás → ch02–ch07; hacia delante → "nos vemos al siguiente vídeo" [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch08-proceso/CLAIMS#c-0086|c-0086]] (ep09-red-flags, anunciado en ch07) |

## Provenance de la extracción

| Campo | Valor |
|---|---|
| Fecha | 2026-10-20 (noche) |
| ASR | faster-whisper `large-v3`, int8 CPU, language=es (p=1,00), beam 5, **276 segmentos, 97 % habla**, ligado al SHA; wall 30,2 min (1,76× realtime — máquina contienda con sesión gráfica; el peor rate del curso vs 0,68× de ch07 con máquina despejada) |
| Extracción | 4 subagentes ONE-SHOT (bloques 0–5:46 / 5:47–9:58 / 10:00–14:35 / 14:36–17:04), 86 claims |
| Revisión | 17 minutos × 1 revisor (UNA revisión por minuto; minuto 14 en dos pasadas: la primera con 2 claims, la segunda 14b con los 4 del payload final): 17/17 `MINUTE_REVIEW = VALID`; 2 retries por error transitorio [1210] del proveedor (min 2, min 15) |
| Integración | mecánica (`integrate_reviews.py` + `validate_review.py` por minuto); 19 correcciones propuestas por revisores aplicadas vía pool (literalidad de citas, evidence de frontera, visual_hints, 1 duda resuelta por frames c-0071) |
| Modelo | GLM (subagentes locales + integrador; sin API pagada) |
| DOCVERIFY | PASS — subagente independiente (fallback `general-purpose`): 3 MATERIAL + 1 MENOR de prosa documental (F-01 «2 h» inventada en la cadena del ORO; F-02 ejercicios atribuidos al instructor; F-03 «2M mismo target» vs «ya completado»; F-04 glosa en R10), los 4 adjudicados CONFIRMADOS y corregidos; claims/transcript/frames sin cambios; re-validación PASS |
| Checkpoint 5 min | PASS (min 0–4 VALID tras 20 min; proyección ~200 min/h-video — sobre el objetivo 120 pero <2×, continuado con registro; real final 327 por contención de máquina y retries) |

## Métricas

| Métrica | Valor |
|---|---|
| Claims totales | 86 |
| SUPPORTED / UNCERTAIN / UNVERIFIED | 86 / 0 / 0 |
| Claims activos / superseded | 86 / 0 (sin supersessions en este capítulo) |
| Epistemic | 86 instructor_statement · 0 visual_observation · 0 model_inference (los frames corroboran en `evidence` sin cambiar la epistemic: todo lo afirmado es dicho; los referentes visuales quedan como unresolved_questions) |
| Contradicciones marcadas | 0 |
| Frames base (fin de minuto) | 18 (minutos 0–16 en MM:59.5 + fin del parcial [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch08-proceso/frames/f-001704.png|f-001704]] — negro de cierre, no citado; manifiesto `frames/.base_frames`) |
| Frames bajo demanda | 75 (extraídos y verificados visualmente por los revisores), **64 citados** en total; inventario en [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch08-proceso/FRAMES|FRAMES]]. Recuento reconciliado 2026-10-21 (preflight ch09): 4 huérfanos verificados físicamente — f-000075 (nombre inválido, contenido real del segundo 75) promovido a f-000115 reemplazando una re-extracción desplazada, f-000801 retirado (casi-duplicado del citado f-000804, mismo instante 484 s), f-000814 retirado (byte-idéntico al citado f-001334; original de staging mal-nombrado desde segundos crudos), f-001536 conservado (captura real 15:36, contextual no citado) — detalle en review-notes |
| Preguntas abiertas | 8 registradas (q-ch08-001..008): garbles del capítulo (power stream/very given/el de x y/tonalidad/la crisis), garbles sin lectura, deícticos por par (ORO/AUDUSD/USDCAD/EUR), desliz "tres días" y léxico — ver [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch08-proceso/OPEN-QUESTIONS|OPEN-QUESTIONS]] |
| Rules / concepts / examples documentados | 18 / 10 / 4 |
| Coverage | 17/17 minutos de video con claims y revisión |

## Throughput (reporte separado tramos vs total)

| Tramo | Valor |
|---|---|
| ASR wall | 30,2 min (1,76× realtime — contención de máquina) |
| Agent wall (extracción+revisión) | ≈93 min / 17,07 min video ≈ **327 min/h-video** (objetivo ≤120 → OVER, ver causas en review-notes: contienda de CPU, 2 retries [1210], revisores con hasta 26 tool uses extrayendo frames) |
| Integración + composición | ≈35 min |

## Estructura

- [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch08-proceso/documentation|documentation]] — síntesis por conceptos, todo citado
- [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch08-proceso/CLAIMS|CLAIMS]] — proyección navegable por claim (autoridad: `claims.jsonl`)
- [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch08-proceso/transcript|transcript]] — recurso citable con anchors `^s-HHMMSS`
- [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch08-proceso/FRAMES|FRAMES]] — inventario de frames
- [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch08-proceso/rules|rules]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch08-proceso/concepts|concepts]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch08-proceso/examples|examples]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch08-proceso/study-guide|study-guide]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch08-proceso/review-notes|review-notes]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch08-proceso/OPEN-QUESTIONS|OPEN-QUESTIONS]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch08-proceso/AMENDMENTS|AMENDMENTS]]
