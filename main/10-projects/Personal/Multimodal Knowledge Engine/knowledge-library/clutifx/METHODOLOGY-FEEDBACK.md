# METHODOLOGY-FEEDBACK — Clutifx (Course Intelligence)

Feedback de método del curso Clutifx. Objetivo: mejorar los videos siguientes,
no justificar decisiones pasadas. Estado tras Chapter 08 (2026-10-20 noche).
Los bloques OBSERVED de Chapters 02–07 se conservan abajo (§Ch07, §Ch06, §Ch05,
§Ch04, §Ch03, §Ch02). La skill canónica quedó en v1.2 con hardening ch03–ch07
(incl. checks W11/W12 de navegación, wikilinker corregido con idempotencia y
strip de code-spans en W01/W10); NO se toca aquí la decisión de Owner sobre ASR.

## CH08 OBSERVED (medido en Chapter 08)

| Métrica | Valor |
|---|---|
| Video | ep08-proceso.mp4 · 17:04.42 · SHA `5495798b…` |
| ASR_WALL | 30,2 min (**1,76× realtime — el peor rate del curso**; máquina con sesión gráfica y contención; corrobora que el rate ASR depende del estado de la máquina: 0,68× despejada en ch07 vs 1,76× contendida aquí) · 276 segmentos, 97 % habla |
| EXTRACTION_WALL | 4 bloques secuenciados/emparejados con revisores (~30 min) |
| REVIEW_WALL | ≈60 min (17 minutos en waves de 4-5; **2 muertes [1210] transitorias del proveedor** — min 2 y min 15 — recuperadas con retry secuencial) |
| AGENT_WALL | ≈93 min / 17,07 min ≈ **327 min/h-video — OVER (objetivo ≤120)**: contención de CPU + retries [1210] + revisores que extrajeron hasta 12 frames/minuto; registrado sin disfrazar |
| Claims | 86 (86 SUPPORTED / 0 UNCERTAIN) · 86 instructor_statement / 0 visual_observation (capítulo PROCEDURAL: todo es dicho; los referentes visuales quedan como unresolved_questions, 84 agrupadas en 8 q-ch08-*) |
| Frames | 18 base + 74 bajo demanda = 92; 64 citados |
| DOCVERIFY | ver reporte de sesión (fallback `general-purpose`; el especialista sigue caído por provider binding) |
| Checkpoint 5 min | PASS (min 0–4 VALID en ~20 min; proyección ~200/h-video — sobre objetivo pero <2×, continuado con registro) |

## CH08 LEARNED (para ep09+)

1. **El error [1210] "Invalid API parameter" del proveedor es TRANSITORIO y no determinista por imagen**: el mismo worker lee otros PNG sin problema y un retry secuencial del mismo minuto completa con frames verificados (2/2 recuperados). Protocolo para ep09+: ante un worker muerto con [1210], relanzar el minuto completo; si el retry también falla al leer PNG concreto, emitir veredicto textual con unresolved_questions de lo visual.
2. **El throughput OVER se debe a causas medibles, no al contrato**: (a) contención de CPU del host (ASR 1,76× vs 0,68×), (b) retries, (c) densidad de frames bajo demanda (4,1/min). Para ep09+ con máquina despejada el objetivo ≤120 es alcanzable (ch07: 74).
3. **Un run parcial de integrate_reviews.py SOBRESCRIBE claims.jsonl desde el pool**: re-ejecutar SIEMPRE la integración con la lista COMPLETA de minutos; ante minuto re-payloaded (min 14 ampliado por el bloque 4), la review de segunda pasada reemplaza a la primera (conservar la primera como auditoría). **FIX 2026-10-21 (preflight ch09)**: defecto reproducido con fixture (2 minutos, run de 1); el script ahora exige integración COMPLETA para escribir el canónico (todos los reviews presentes en el run + cobertura total del pool); una ejecución parcial escribe sólo `claims.jsonl.partial` y sale 1. Prueba red-green: `scripts/tests/integrator_selftest.py` (9 casos; el 7 es el defecto ch08, el 9 la cobertura incompleta).
4. **Los frames bajo demanda viven en /tmp del revisor si el worker no los copia a la biblioteca** (min 3): el integrador debe barrer los staging /tmp/minrev-* y mover los frames citados antes de validar (V03 lo caza).
5. **Los names de frame a mano siguen apareciendo aun con fórmula documentada** (f-000075 con segundos crudos 75): el validador V04 lo caza; regenerar por fórmula + declarar el nombre inválido en .deprecated_frame_names; NO citar el literal en notes de claims (V11 lo caza aunque el nombre esté declarado — la excepción aplica a referencias, no a notas).
6. **La epistemic uniforme instructor_statement fue la decisión correcta en un capítulo procedural**: en vez de fabricar visual_observation a partir de stills ambiguos, los referentes visuales quedaron como preguntas (84 → 8 agrupadas); el DOCVERIFY puede concentrarse en el ORDEN y las condiciones del proceso, que es donde vive el conocimiento.
7. **El wikilinker corregido (citas [c-XXXX] absorbidas, code-spans protegidos, idempotencia probada) pasó su primer run real sin producir una sola doble anidación** — los 8 docs de ch08 se wikilinkearon en un pase.

## CH07 OBSERVED (medido en Chapter 07, con incidentes)

| Métrica | Valor |
|---|---|
| Video | ep07-setups.mp4 · 45:35.17 · SHA `b20ce8f7…` |
| Incidente 1 — reboot | El ASR del intento 1 (09:51) murió en un doble reboot del host (~15:10 y ~15:34) SIN escribir transcript; los 46 frames base + manifiesto + scripts del workspace sobrevivieron y se reutilizaron íntegros. Relanzado 17:01 tras verificar proceso/log/transcript (sin duplicación) |
| ASR_WALL | **68,3 min (0,68× realtime — el rate más rápido del curso; máquina despejada post-reboot)** · 480 segmentos, 98 % habla |
| EXTRACTION_WALL | 11 min (6 EXTRACTORs paralelos, 238 claims; 5,2 claims/min promedio) |
| Incidente 2 — cuota | `[1310] Weekly/Monthly Limit Exhausted` a las ~19:00 (reset 2026-10-25) mató los reintentos de 3 revisores; el DOCVERIFY subagente quedó imposible |
| REVIEW_WALL | 45 min totales: 23 minutos por subagentes ONE-SHOT (olas 1–3) + **23 minutos por el integrador-revisor (fallback)**: mismo contrato (SOURCE-FIRST, frames por fórmula verificados visualmente vía análisis VLM, cardinalidad validada); independencia preservada (el integrador nunca extrajo) |
| AGENT_WALL | ≈56 min / 45,6 min video ≈ **74 min/h-video** (objetivo ≤120 → PASS, el mejor del curso) |
| Claims | 238 (238 SUPPORTED / 0 UNCERTAIN / 0 UNVERIFIED) · 226 instructor_statement + 12 visual_observation · 0 model_inference · 1 re-adjudicación honesta de epistemic (c-0167) |
| Frames | 46 base (reutilizados) + 80 bajo demanda = 126; 64 citados en evidence |
| Revisión independiente (DOCVERIFY) | **FALLBACK** por cuota: check_term_sources PASS + contraste SOURCE-FIRST puntual + validate_library PASS (0 findings) ejecutados por el integrador; sin contraparte subagente independiente — el Owner puede pedirla post-reset |
| Checkpoint 5 min | PASS (23/23 VALID; proyección ~89 → real 74 min/h-video) |

## CH07 LEARNED (para ep08+)

1. **El fallback integrador-revisor funciona pero degrada la independencia del DOCVERIFY**: la revisión por minuto la pudo cubrir el integrador (que no extrajo claims) sin romper el contrato; el DOCVERIFY en cambio quedó sin contraparte independiente. Para ep08+: si la cuota vuelve a agotarse, la revisión por minuto puede continuar en modo híbrido, pero el DOCVERIFY subagente debería re-programarse para después del reset en vez de sustituirse.
2. **Los reboots del host matan el ASR silenciosamente**: el intento 1 dejó log truncado y ningún transcript. Para ep08+: tras cualquier incidente del host, verificar transcript.json + última línea del log ANTES de relanzar (protocolo aplicado aquí y documentado en el README del capítulo).
3. **El rate ASR mejoró 3× con la máquina despejada** (0,68× vs 0,21–0,23× canónico): la contención de CPU era la causa dominante del rate lento histórico, no el modelo. Proyección para ep08+: ~65–70 min/h-video de ASR con máquina limpia.
4. **wikilink_docs.py --all-tokens re-enlazaba tokens pegados a corchetes de cita** (doble anidación `[[[path|label]]]`, 69 enlaces rotos en ch07, reparados entonces a mano con regex iterativo). **FIX 2026-10-20 (QA ch07)**: defecto reproducido con fixture derivado del caso real (citas `[c-XXXX]` del GLOSSARY + links dentro de backticks); el script ahora (a) absorbe las citas de sólo tokens (`[c-0001, c-0002]` → links con `·`), (b) NO enlaza tokens pegados a `[` en citas mixtas (`[c-0001 [ASR]]` queda en texto plano válido), (c) protege el código inline ANTES que los wikilinks (un link dentro de backticks quedaba destruido con fuga de marcadores `\x00N\x00`). Prueba de idempotencia `first_run == second_run` + casos red-green: `scripts/tests/wikilinker_selftest.py` (10/10 PASS; los docs reales de ch07 pasan por el script sin cambios).
5. **El validador V10 exige reglas al inicio de línea** (`^\*\*R\d+`): las listas con viñeta `- **R1**` cuentan 0. Formato correcto observado en ch07 tras el fix.
6. **83 preguntas de revisión se agruparon en 18 q-ch07-***: la agrupación temática (familia DOL, familia TS, garbles sueltos, deícticos) escala mejor que una pregunta por instancia cuando el capítulo es garble-denso (98 % habla).

## PREFLIGHT ch07 sobre ch06 (2026-10-20) — GATE 4/4 PASS

- **CH06_TARGETED_REVIEW = PASS**: aclaración acotada v1.2 sobre c-0053/c-0058/c-0059 con 12 frames puntuales (10:47–10:53, 12:06–12:37) y 1 worker MINUTE_REVIEWER targeted (3/3 SUPPORTED, cardinalidad exacta, 14 frames verificados). Statements intactos (preservan palabra dicha/deixis) → sin amendments (el contrato reserva AMENDMENTS para correcciones materiales); lo resuelto vive como evidencia ampliada + notas en claims.jsonl y estados en OPEN-QUESTIONS: q-ch06-008 RESUELTA en lo operativo ("a las 7" = las 17), q-ch06-010 RESUELTA PARCIAL (objetivo = herramienta de long hacia 1,3941; rango a favor = rectángulo 1h ~02:00–13:00; "este fellow swing aquí" queda probable), q-ch06-013 OPEN en lo literal con referentes visuales confirmados, q-ch06-009 OPEN con nota de f-001047.
- **q-ch05-009 (contrato)**: verificado que NO exige fila de amendment — la resolución ("Felux Swing" = failure swing) no modificó ningún statement (c-0100 ya preservaba la palabra dicha) y vive registrado en el OPEN-QUESTIONS de ch05 con backlinks a ch06 c-0001/c-0064; el AMENDMENTS de ch06 ya lo documentaba así.
- **CH06_NAVIGATION = PASS** (`validate_library.py` 0 findings tras integrar) · **CH06_SOURCE_FIRST = PASS** (64 vivos / 0 findings) · **CH06_METHOD_FEEDBACK = UPDATED** (este bloque).
- **Cobertura visual**: la densidad del run (19 frames para 13,5 min de pizarra) fue suficiente SALVO un hueco real: el instructor SEÑALA deícticos en 12:06–12:26 y dibuja el rectángulo recién 12:27+, y el frame base de fin de minuto no muestra el estado previo. Resuelto con captura puntual bajo demanda del preflight (sin imponer mínimo artificial); lección registrada en CH06 LEARNED #3. Sin cambios en skills: no hay defecto reproducible de contrato (la captura puntual ya es contrato vigente; fue un gap de juicio del revisor, cubierto por el mecanismo targeted).

## CH06 OBSERVED (medido en Chapter 06, sin corregir) — walls conciliadas con epochs+mtimes

| Métrica | Valor |
|---|---|
| Video | ep06-failure-swing.mp4 · 13:27.98 · SHA `470ff3c0…` |
| ASR_WALL | **59,6 min** (0,23× realtime, rate canónico; epochs 22:06:31→23:06:07) con el grind r5 de Echo en la máquina (load ~10/24) |
| EXTRACTION_WALL | 10,6 min (3 EXTRACTORs paralelos, 64 claims; spools 23:19:08–23:21:49; inicio sin epoch, cifra del run) |
| REVIEW_WALL | **13,8 min de revisores** (ola 1 min 0–4: 5,3; ola 2 min 5–13: ≈8,5; medición por dispatch) **+ 10,6 min de integración/validación entre olas** (por epochs: checkpoint 23:30:59 → fin 23:41:36). La cifra "~11,5" que quedó impresa en review-notes era una estimación previa superada por la medición por epochs (13,8) |
| AGENT_WALL | **≈22 min reportado** (10,6 + ~11,5 previo) ≈ 98 min/h-video; con la medición final la suma de runtimes de agente es 24,4 min ≈ 108 min/h-video; el muro físico observable post-ASR fue 35,5 min (23:06:07→23:41:36, incluye construcción de payloads, checkpoint e integración). Las tres lecturas ≤ objetivo 120 → PASS sin cambio de veredicto |
| Superposición real | **NINGUNA entre extracción y revisión**: los 14 payloads se construyeron a las 23:23:03, después del último spool de extracción (23:21:49); la brecha 24,4 vs 22 proviene de la cifra previa de revisión, no de solapamiento |
| Claims | 64 (64 SUPPORTED / 0 UNCERTAIN / 0 UNVERIFIED) · 62 instructor_statement + 2 visual_observation · 0 model_inference |
| Frames | 14 base + 5 bajo demanda (run) → **+12 bajo demanda en la aclaración acotada 2026-10-20 = 31; 27 citados** |
| Revisión independiente (DOCVERIFY) | PASS_WITH_FINDINGS — 8 findings (2 MATERIAL + 6 MENOR), los 8 corregidos in-mission y re-validados |
| Checkpoint 5 min | PASS (20/20 VALID; proyección ~140 min/h-video → real 98–108 con ola única de 9) |

## CH06 LEARNED (para ep07+)

1. **El rate ASR canónico (0,23×) se sostiene con el grind r5 de Echo en la máquina** (probe de preflight + epochs). Para ep07 (45:35, el más largo desde ch03) proyectar ASR ~3,3–3,8 h y solapar el preflight del capítulo con el ASR del siguiente en vez de esperar: el ASR es mecánico, reversible y no toca la biblioteca.
2. **La aclaración acotada targeted funciona como contrato de preflight**: 1 worker + 12 frames puntuales resolvieron referentes y confirmaron una lectura operativa en ~15 min sin re-procesar nada (contrato v1.2 ejecutado tal cual; los statements preservaron la palabra dicha y NO generaron amendments).
3. **Captura en el momento del SEÑALAMIENTO, no sólo del dibujo**: el frame de fin de minuto acumula dibujos pero no muestra el estado previo cuando el instructor señala deícticos antes de dibujar (hueco 12:06–12:26 de ch06). Para ep07+: si un deíctico queda sin resolver y el dibujo ocurre después dentro del mismo minuto, el reviewer debe pedir la captura del segundo del señalamiento.
4. **La revisión targeted no rubber-stampea**: el worker corrigió al Manager la extensión del rectángulo (02:00–13:00 vs el 06:00–10:00 de la herramienta de long) — independencia real demostrada en un paquete de 3 claims.
5. **La medición por epochs+mtimes es la autoridad de las walls**: las cifras previas ("~11,5", AGENT_WALL "22") eran estimaciones de dispatch; conciliadas declarando las tres lecturas (runtimes 24,4 / reportado 22 / muro físico 35,5) sin inventar tiempos ni ocultar la ausencia de solapamiento.

## CH05 OBSERVED (medido en Chapter 05, sin corregir)

| Métrica | Valor |
|---|---|
| Video | ep05-smt.mp4 · 18:29.7 · SHA `072f669d…` |
| ASR_WALL | **92,5 min** (0,20× realtime; rate canónico — máquina despejada, verificado con probe 28 s en preflight: 0,21×) |
| EXTRACT_WALL | 9,7 min (4 EXTRACTORs paralelos, 100 claims) |
| REVIEW_WALL | 34,1 min (19 MINUTE_REVIEWERs, 3 olas de 5/7/7) |
| AGENT_WALL | ≈44 min / 18,5 min video ≈ **143 min/h-video** (objetivo ≤120; banda 2× = 240 → PASS; el mejor capítulo del curso: ch03 225, ch04 233) |
| Claims | 100 (99 SUPPORTED / 1 UNCERTAIN / 0 UNVERIFIED) · 83 instructor_statement + 17 visual_observation · 0 model_inference · 3 re-adjudicaciones de epistemic en integración (sustancia verbal, patrón P1 de ch02) |
| Frames | 19 base + 62 bajo demanda = 81; 66 citados en evidence |
| Revisión independiente (DOCVERIFY) | ejecutada sobre la biblioteca publicada; ver handoff del run |
| Checkpoint 5 min | PASS (26/26 VALID; proyección ~162 min/h-video; real 143) |
| Preflight | GO por probe (no se arrancó el ASR full a ciegas); integrate_reviews.py de ch04 generalizado + integrator_selftest 5/5 |

## CH05 LEARNED (para ep06+)

1. **El integrador generalizado funciona**: `scripts/integrate_reviews.py` (paths por argumento + normalización f-.png) se usó tal cual; el selftest cazó un bug de índice antes de producción. Los run dirs ya no necesitan copiar el integrador.
2. **El briefing de términos críticos dentro del prompt del reviewer** (no sólo en el context pack) evitó el defecto DOL/DXY: 0 sustituciones indebidas; DXY quedó documentado como término genuino con sus garbles propios. Mantener en ep06+ (los términos críticos cambian por capítulo: el de ep06 será failure swing vs "Felux Swing").
3. **Los reviewers propusieron 6 correcciones de statement y 1 de metadato** y todas se aplicaron vía pool sin edición manual canónica; el flujo "reviewer propone → integrador revisa → pool → integrador mecánico" maduró (en ch04 el fix de normalización fue post-integración; ahora está en el script).
4. **Olas de 7 con payloads homogéneos (~5-6 claims/minuto) dieron el makespan más bajo del curso** (34,1 min); la video-duración corta ayudó, pero el despacho plano por minutos ya no necesita optimización.
5. **El ASR sigue dominando el total** (92,5 min para 18,5 min de video); la decisión Owner (GPU/modelo menor) sigue abierta y es la única palanca grande que queda.
6. **Los frames extraídos y descartados por los reviewers** (no citados, quedan como auditoría contextual) sumaron 15: el presupuesto por bloque funcionó sin tope rígido.
7. **Defecto reproducible → skill endurecida (FINDING→FIX→TEST→SKILL→FEEDBACK)**: los extractores de ch05 escribieron `visual_hint.second` como HHMMSS pegado (5 casos, p.ej. 1635 por 16:35). Fix: V08 de `validate_library.py` ahora marca hints fuera de duración (con `--duration-seconds`), caso red-green G en `fixtures_selftest` (11/11), contrato EXTRACTOR actualizado en `course-knowledge-worker` (second = segundos reales por fórmula). Sin impacto en ch02–ch04 (0 hints fuera de duración).

## PREFLIGHT (2026-10-19, obligatorio antes de Chapter 04 — PASS 5/5)

- **Supersession safety**: los 6 históricos de ch03 mantenían `verdict: SUPPORTED` y la proyección CLAIMS.md los mostraba como vigentes → contaminación de consultas. Contrato nuevo: GROUNDING_VERDICT (SUPPORTED/…) ≠ LIFECYCLE_STATUS (activo/superseded derivable de `superseded_by`; SIN propiedad redundante). Renderer marca `SUPERSEDED — HISTORICAL, NOT ACTIVE` + `Replacement:` navegable; validador V14 (superseded_by/supersedes bidireccional, sin ciclos), V15 (proyección con lifecycle), V16 (docs pedagógicos sin WIKILINKS a reemplazados — la mención histórica en texto plano es rastro de auditoría permitido), V10 (fila `Claims activos / superseded` obligatoria con reemplazos). Contract tests: `lifecycle_selftest.py` (10 casos). ch03 aplicado: 211/6, VALIDATION PASS.
- **DOL/DXY en ch02**: la remediation de ch03 dejó ch02 intacta "para no tocar sin evidencia"; el preflight la adjudicó con la fuente de ch02: c-0066 y c-0089 publicaban DXY donde la fuente dice "el doble"/"dol" (s-001005/s-001010) y "a por tu dol, perdón, a por tu objetivo" (s-001401) → DOL_CONFIRMED ×2, 2 supersessions (c-0099/c-0100), amend-0003/0004, docs/glosario/índice actualizados. ch03 semánticamente intacto; ch01 intacto.
- **SOURCE-FIRST hardening**: `check_term_sources.py` ahora es case-insensitive en el lado fuente (un "dol" minúscula del ASR cuenta como canónico) y trata los garbles ambiguos ("el doble", "doll", "dole", "dolls") como aliases de grupo: canónico en statement + alias en fuente sin marca `[ASR]` ⇒ `TERM_DISAMBIGUATION_REQUIRED` (REVIEW; el chequeo no decide el término). Selftest 10 casos con los casos REALES de ch03 y ch02. La verificación determinista detecta la necesidad de revisión; el reviewer adjudica.

## CH04 OBSERVED (medido en Chapter 04, sin corregir)

| Métrica | Valor |
|---|---|
| Video | ep04-entradas.mp4 · 27:35.4 · SHA `f69f7d62…` |
| ASR_WALL | **4h10m** (0,11× realtime; máquina compartida con jobs de backtest ~400 % CPU — el rate canónico era 0,21–0,38×; la carga externa dominó el total) |
| EXTRACT_WALL | 15,3 min (6 EXTRACTORs paralelos, 119 claims) |
| REVIEW_WALL | 91,9 min (28 MINUTE_REVIEWERs, 4 olas de 5/7/7/9; verificación visual frame-a-frame) |
| AGENT_WALL | 107,2 min / 27,6 min video ≈ **233 min/h-video** (objetivo ≤120; banda 2× = 240 → continúa; igual que ch03) |
| Claims | 119 (111 SUPPORTED / 8 UNCERTAIN / 0 UNVERIFIED) · 109 instructor_statement (incluye c-0016 adjudicada) + 9 visual_observation · 0 model_inference · 33 con preguntas sin resolver |
| Frames | 28 base + 77 bajo demanda = 105; 97 citados en evidence |
| Revisión independiente (DOCVERIFY) | ver handoff; ejecutada sobre la biblioteca publicada con puntos de contraste SOURCE-FIRST obligatorios |
| Checkpoint 5 min | PASS (21/21 VALID; proyección 152 min/h-video; real 233 — dentro de banda) |

## CH04 LEARNED (para ep05+)

1. **La corrección de statement por el reviewer funciona**: 7 corrections_suggested aplicadas en integración (marcas [ASR], género literal, niveles leídos con zoom); el flujo "reviewer propone, integrador aplica al pool, validate_review por minuto" evitó toda edición manual canónica.
2. **El reviewer puede RECHAZAR evidencia del extractor** (c-0083: frame mostraba 4h, no 1h): la regla "no aceptar un frame que no muestre lo afirmado" operó de verdad; los visual_hints erróneos del extractor (3) quedaron documentados en reasons sin contaminar statements.
3. **Los UNCERTAIN son productivos**: 8/119 (6,7 %) por garbles/deícticos, todos con pregunta abierta trazada (19 q-ch04-*). Mejor dudoso visible que falso SUPPORTED.
4. **Las colas de las olas dominan el makespan**: la ola de 9 tardó ~31 min (los reviewers pesados ~1,5-1,9 h de subagente con muchas lecturas de frames). Para ep05+ considerar despacho por tamaño de payload ya probado en ch03.
5. **El ASR sigue siendo el cuello absoluto** (4h10m para 28 min por carga externa): la decisión Owner (GPU/modelo menor) sigue abierta; con la máquina despejada el rate vuelve a ~0,2-0,38×.
6. **Normalizar refs `f-` en el integrador**: los reviewers escribieron 6 evidencias como `f-XXXXXX.png` (con sufijo); el integrador ahora las normaliza (el fix se hizo post-integración; incorporarlo a integrate_reviews.py).


## REMEDIATION (2026-10-18 noche — DOL/DXY + probe ASR, mandato Primary Manager)

- **Defecto MATERIAL que la verificación documental dejó pasar**: c-0121 publicaba "al DXY" donde la fuente dice "al DOL" (s-002201 literal). Causa raíz: el glosario mapeaba el garble "el doble/dol" a DXY globalmente y extractores/revisores lo trataron como permiso de sustitución. Auditoría completa: 104 ocurrencias en 20 claims — **0 menciones genuinas de DXY en ch03**; el término del capítulo es DOL (s-001229 "el tema DOL" literal, pizarra f-004059).
- **Corrección con contrato de identidad V1.2**: 6 supersessions (c-0089→c-0212, c-0093→c-0213, c-0116→c-0214, c-0121→c-0215, c-0122→c-0216, c-0123→c-0217 — el statement publicado cambió de referente ⇒ claim nuevo + anterior superseded sin renumerar), 2 glosas inline retiradas in-place (c-0144, c-0184), notas corregidas (c-0055, c-0074, c-0080, c-0142, c-0146, c-0208, c-0031), q-ch03-001 RESUELTA, 12 amendments. ch02 NO se toca (sus lecturas DXY quedan como publicadas; el glosario queda desambiguado).
- **Contrato nuevo (skills)**: TERM_DISAMBIGUATION_REQUIRED — el statement publica la palabra dicha ([ASR]), la interpretación vive en notes; que el glosario liste una equivalencia NO la respalda. Chequeo SOURCE-FIRST determinista `check_term_sources.py` + `source_first_selftest.py` (el caso 1 es el defecto real) + obligación SOURCE-FIRST en DOCUMENTATION_VERIFIER (docs↔claims no basta: ambos pueden contener el mismo error).
- **Verificación independiente post-remediation**: 2 MATERIAL (c-0116 citado como vivo en documentation; c-0080 con nota DXY no cubierta) + 6 MENOR (numeración de amendments intercambiada en notes, FRAMES.md desincronizada, rangos de examples, remanentes DXY en review_reasons, evidence de c-0217 sin s-002215, q-ch03-001 con claim inexistente) — los 8 corregidos in-mission; re-validado (LIBRARY_VALIDATION PASS, TERM_SOURCE_CHECK PASS 211 vivos / 0 findings).
- **Lección de proceso**: el DOCVERIFY del run original contrastó docs↔claims (coherencia interna) pero no claims↔fuente (verdad). El SOURCE-FIRST es ahora mandatorio; el caso real quedó como contract test.

## ASR PROBE (2026-10-18, acotado — 36,9 min de presupuesto 45)

- 6 fragmentos × 28 s (168 s) con términos/garbles, negaciones, números/TFs y DOL/doble. A = large-v3 beam5: 1161s (0,14× fragmento) · B = beam1: 970s (0,17×) · C = medium NO EJECUTADO (no cacheado; descarga prohibida por mandato).
- Calidad: aciertos idénticos 72 % (31/43) con las MISMAS ausencias en A y B; "DOL" 3/6 en ambos; "DXY" 0/6 en ambos (correcto). Las ausencias se explican por cortes de ventana/VAD, no por beam.
- **ASR_RECOMMENDATION = KEEP_LARGE_V3_BEAM5**: beam1 sólo 1,20× más rápido (≈3 min/h de audio) — nada del 2-5× esperado — y sin medición de comportamiento full-audio. Nota: los benchmarks por fragmentos subestiman el throughput (0,14-0,17× vs 0,21× full-run) por reinicios de VAD/contexto. La palanca real sigue siendo modelo/GPU (decisión Owner).
- Detalle: `/home/kor/mke/clutifx-ch03-20261018/asr-probe/` (RECOMMENDATION.md, verdict.json, probe-report.json).

## CH03 OBSERVED (medido en Chapter 03, sin corregir)

| Métrica | Valor |
|---|---|
| Video | ep03-bias.mp4 · 41:50.8 · SHA `c52dafa8…` |
| ASR_WALL | **3h18m** (0,21× realtime; más lento que ch02's 0,38× — 96 % de habla y 506 segmentos) — partida dominante |
| EXTRACT_WALL | 10,9 min (5 EXTRACTORs paralelos, 211 claims) |
| REVIEW_WALL | ~146 min (42 MINUTE_REVIEWERs, 6 olas de 5–8; cada revisor extrae y verifica visualmente sus frames) |
| AGENT_WALL (extracción+revisión) | ~157 min / 41,8 min video ≈ **225 min/h-video** (objetivo ≤120; banda 2× = 240 → continúa; el exceso viene de la verificación visual frame-a-frame del contrato v1.1+) |
| Claims | 211 (todos SUPPORTED; 2 UNCERTAIN del review adjudicados en integración con nota) · 176 instructor_statement + 35 visual_observation · 0 model_inference |
| Frames | 42 base + 79 bajo demanda = 121; 74 citados en evidence |
| Revisión independiente (DOCVERIFY) | 0 MATERIAL + 5 MENOR (conteos y citas cruzadas), todos corregidos in-mission |
| Checkpoint 5 min | PASS (30/30 VALID; proyección inicial ~80 min/h-video subestimó las olas reales de ~13 min) |

## CH03 REPAIRED (defectos de contrato encontrados en vuelo, con prueba)

- **`make_minute_payload.py` emitía `id` pero `validate_review.py` esperaba `key`** (y los reviewers v1.2 devuelven `claim_key`): el checkpoint lo cazó antes de dañar nada. Fix en ambos helpers + test de regresión nuevo `scripts/tests/review_pipeline_selftest.py` (5 casos, rojo-verde).
- **Frame base del minuto parcial**: la captura usa el fin real del video (f-004150 a 41:50.5); sin regla de nombre: lo decide el manifiesto.
- **Naming de frames a mano falla**: el integrador generó `f-00059` (5 dígitos) por concatenación manual en el primer lote; re-hecho con la fórmula. Confirma el contrato: SIEMPRE fórmula desde segundos reales, jamás printf a mano.
- **V11 es chapter-local**: los refs `s-` de OTRO capítulo en los docs disparan V11 falso-positivo. Los W-checks sí los resuelven (cross-file). Para ch04: citar cross-chapter con enlace a archivo + timestamp en la etiqueta (o extender V11 si Owner lo quiere).
- **5 MENOR del DOCVERIFY** corregidos: conteos README (preguntas abiertas 3→4; UNCERTAIN adjudicados 1→2), cita de ch02 atribuida a claim inexistente (→ segmentos reales sin claim, declarado), 4 frames listados en examples sin citación real (→ quitados), fórmula de rango atribuida al claim equivocado (→ c-0118/c-0100).

## CH03 LEARNED (para Chapter 04)

1. **ASR sigue siendo el cuello** (3h18m para 42 min de video): el test de 2 min (beam 1/medium vs large-v3) sigue en PROPOSED-2 esperando decisión Owner. Con ep04 (~similar duración) el ahorro potencial es >1 h/video.
2. **La verificación visual frame-a-frame es el nuevo centro de costo del review** (146 min vs 19,8 en ch02 por 2,3× video): es el precio del provenance visual v1.1+ y compró 35 visual_observation con frame verificado y 0 MATERIAL en el DOCVERIFY. Alternativa a proponer a Owner: reviewers SIN extracción propia (sólo transcript + base frame) + una sola pasada visual del integrador sobre los visual_hints; medir calidad antes de adoptar.
3. **Olas de 8 con colas de 14–16 min desperdician paralelismo**: despachar por tamaño de payload (claims×segmentos) en vez de por minuto reduces el makespan.
4. **El glosario de garbles por capítulo funciona**: ~10 garbles nuevos de ch03 ya están en review-notes para reutilizar en ch04 (ep04-entradas reutilizará el vocabulario DOL/bias/rangos).
5. **Integración por olas en background** (reviewers async + integración del integrador entre olas) funcionó sin bloquear: mantener.

## Ch02 OBSERVED (medido en Chapter 02, sin corregir)

| Métrica | Valor |
|---|---|
| Video | ep02-time.mp4 · 17:09 · SHA `fb8b3de4…` |
| OWNER_OBSERVED_ELAPSED | **2h06m** (medida del Owner; autoridad para el total end-to-end) |
| AGENT_RECONSTRUCTED_ELAPSED | ≈1h40–1h50 (02:54–04:35, mtimes/epoch) — la diferencia es ventana de observación + overhead de orquestación; se reportan ambas |
| ASR_WALL_TIME | 45,1 min (faster-whisper large-v3 int8 CPU, 0,38× realtime) — partida dominante |
| EXTRACTION_WALL_TIME | 8,6 min (3 subagentes ONE-SHOT paralelos) |
| REVIEW_WALL_TIME | 19,8 min (18 subagentes, olas 5/7/6) |
| INTEGRATION_WALL_TIME | ~20 min (primera publicación) + ~35 min (remediación P1–P10) |
| Subagentes | 21 (extracción+revisión) + 3 auditores visuales + 1 revisión independiente + 1 verificación documental |
| Claims | 98 (4–9/min) · frames 18 base + 47 demanda · 65 archivos |
| Throughput subagentes (extracción+revisión) | ~28,4 min / 17,2 min video ≈ 99 min/h-video (objetivo ≤120 ✓) — NO es el tiempo end-to-end |
| Hallazgos del Owner sobre la primera publicación | 6 (provenance visual, naming, conteos README, wall time, c-0066, c-0056) — todos reproducidos 1:1 desde los archivos |

## REPAIRED (verificado, con prueba)

- **Provenance visual estructurada**: los claims visuales citaban solo transcript;
  tras auditar físicamente 41 claims (27 visual_observation ∪ 38 visual_hint),
  `claims.jsonl.evidence` contiene 48 refs a frames verificados (antes 0).
  23/23 visual_observation con frame; epistemic realmente cambiada en 5 claims
  (4 visual_observation→instructor_statement + 1 model_inference→instructor_statement;
  41 auditadas, 36 con frames — errata B3 en repair/REPAIR-LOG).
- **Naming de frames**: f-170903→f-001703 + 5 históricos declarados en
  `.deprecated_frame_names` (el validador distingue `historical_invalid_name`
  de cita vigente). 65/65 nombres canónicos y dentro de duración.
- **Conteos reconciliados**: README (14/13) vs artefactos (16/17) resuelto —
  README = artefactos en claims/veredictos/rules/concepts/examples/frames.
- **Wall time**: el reporting distingue OBSERVED (owner, 2h06) de tramos del
  agente; el README ya no presenta los 28,4 min como tiempo total.
- **c-0066**: adjudicación A — el condicional DXY es textual del instructor →
  `instructor_statement` (era `model_inference`+SUPPORTED, inaceptable tal cual).
- **c-0056**: deíctico de 8h resuelto con comparación de estados
  (f-000758/f-000806, rango válido 1,4748–1,5803); matiz del borde inferior del
  rectángulo descartado conservado en la nota.
- **Validador determinista** (`scripts/validate_library.py`, V01–V13) +
  cardinalidad de reviews (`validate_review.py`, R01–R04) + payload builder con
  contexto de frontera (`make_minute_payload.py`) + selftest 10/10. RED capturado
  antes de reparar; `LIBRARY_VALIDATION = PASS` después.
- **Skills**: principal en **v1.2** (v1.1: 7 contratos; v1.2 mismo día: navegación
  Obsidian, proyecciones deterministas CLAIMS/FRAMES, identidad permanente,
  AMENDMENTS/OPEN-QUESTIONS, aclaración acotada, consulta por agentes, checks W);
  `course-knowledge-worker` (EXTRACTOR / MINUTE_REVIEWER / DOCUMENTATION_VERIFIER,
  spool-only, cardinalidad obligatoria, unresolved_questions, modalidad targeted)
  registrada en el INDEX federado.
- **Revisión independiente (P10)**: 10/10 puntos sustantivos PASS; 3 findings de
  registro (1 MATERIAL de libro de conteos, 2 MENOR editoriales) corregidos
  in-mission y re-validados.

## REMAINING (abierto, honesto)

1. **ASR local lento** (45 min/video en CPU): sin decidir. Opciones ya
   identificadas (beam 1, modelo menor, GPU); requiere decisión Owner porque
   cambia la herramienta de transcripción.
2. **c-0056**: el borde inferior del rectángulo descartado (~zona 1,52) se lee
   de un still en pleno dibujo — consistente, no probado como caja completa.
3. **c-0059 y c-0070**: visual_hints sin frame (sustancia hablada; los frames
   candidatos se inspeccionaron y no muestran lo afirmado). Aceptables como
   contexto; si el Owner los quiere visuales, habría que redibujar/demostrar en
   el video — no hecho.
4. **Epistemic en extracción**: las 5 reclasificaciones post-hoc eran evitables si
   los extractores aplicaran la distinción instructor/visual/inferencia con más
   rigor al proponer (el glosario y la v1.1 lo piden; no verificado en un run
   nuevo).
5. **`documentation-verifier` agent type no disponible en esta cuenta**
   (provider zai-start-plan ausente): las verificaciones se ejecutaron con
   `general-purpose` + prompt adversarial. Gap de plataforma, no de método.

## PROPOSED_FOR_NEXT_CHAPTER (ep04-entradas y sucesivos)

1. **Ejecutar el pipeline v1.2+hardening ch03 tal cual**: paquetes de worker con
   `course-knowledge-worker/SKILL.md` + ROLE; payload por
   `make_minute_payload.py`; integración con `validate_review.py`; cierre con
   `validate_library.py` = PASS + conteos reconciliados. Nada de esto requiere
   nueva construcción.
2. **Decidir ASR** con un test de 2 minutos (large-v3 beam 5 vs beam 1 vs
   medium) comparado contra el transcript actual de ch02/ch03. Ahorro potencial
   >1 h/video (ch03: 3h18m de ASR para 42 min). (Decisión Owner, sigue abierta.)
3. **Presupuesto de frames por bloque** declarado en el paquete según densidad
   visual estimada (recorrido de gráfico ⇒ más que 1/min), con exceso
   justificado en review-notes (ya es contrato v1.1; aplicar el presupuesto
   inicial desde la planificación).
4. **Epistemic estricta en EXTRACTOR**: si el statement se sostiene con citar al
   instructor, es `instructor_statement`; `visual_observation` sólo si la
   sustancia requiere mirar el gráfico; `model_inference` nunca llega a
   SUPPORTED sin adjudicación explícita (V13 lo bloquea).
5. **MINUTE_REVIEWER devuelve `verified_evidence` completo** (s- y f-), de modo
   que la integración de evidencia sea mecánica y no requiera segunda auditoría
   visual (en ch02 hizo falta una ronda P1 completa).
6. **Mantener**: checkpoint doble a los 5 min (subagentes vs total), revisión
   POR MINUTO (nunca por claim), adjudicaciones documentadas en el claim,
   `repair/` con baseline+log por capítulo.
