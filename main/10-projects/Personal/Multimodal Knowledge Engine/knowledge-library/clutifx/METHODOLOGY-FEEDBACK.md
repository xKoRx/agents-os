# METHODOLOGY-FEEDBACK — Clutifx (Course Intelligence)

Feedback de método del curso Clutifx. Objetivo: mejorar los videos siguientes,
no justificar decisiones pasadas. Estado tras la regularización final (2026-10-22) — inventario del curso
COMPLETO y homogéneo: 12/12 vídeos procesados y 12/12 bibliotecas V1.2 (CH01 migrado desde MKE V2 ese mismo día; legado preservado en su `legacy-mke-v2/`).
Los bloques OBSERVED de Chapters 02–08 se conservan abajo (§Ch08, §Ch07, §Ch06,
§Ch05, §Ch04, §Ch03, §Ch02). La skill canónica quedó en v1.2 con hardening ch03–ch07
(incl. checks W11/W12 de navegación, wikilinker corregido con idempotencia y
strip de code-spans en W01/W10); NO se toca aquí la decisión de Owner sobre ASR.

## CH01 V1.2 MIGRATION OBSERVED (2026-10-22 — misión CLUTIFX FINAL REGULARIZATION)

| Métrica | Valor |
|---|---|
| Video | ep01-intro.mp4 · 34:04 · SHA `4de8f12d…` |
| ASR | **REUTILIZADO** del run MKE V2 original (transcript.json con source_sha256 verificado; 323 segmentos monótonos, cobertura completa; 0 min de ASR) |
| EXTRACTION_WALL | ~34 min de workers (6 EXTRACTORs SECUENCIALES, 132 claims ≈ 3,9/min) |
| REVIEW_WALL | 34 MINUTE_REVIEWERs en olas de 5; 6 muertes [1210] transitorias, todas recuperadas con retry completo del minuto (protocolo ch08) |
| AGENT_WALL | proyección checkpoint ~200 min/h-video (<2×, continuado con registro, criterio ch04–ch12) |
| Claims | 132 (132 SUPPORTED / 0 UNCERTAIN); 114 instructor + 18 visual |
| Frames | 35 base + 54 bajo demanda = 89; 65 citados |
| DOCVERIFY | independiente ONE-SHOT: **0 MATERIAL + 11 MENOR**, los 4 recomendados corregidos (timestamps, ventana de c-0007, cita de R27) |
| Integración | 132/132 aplicados, cobertura completa; IDs c-0001..c-0132 post-integración (patrón ch10) |
| Legado | MKE V2 preservado e inventariado (legacy-mke-v2/ con SHA-256); sin conversión automática de GROUNDING_SUPPORTED a SUPPORTED |

## CH01 LEARNED (para migraciones futuras)

1. **Reutilizar el transcript del run caro es legítimo y barato**: identidad por `source_sha256` + monotonicidad + cobertura + 0 vacíos evitó el ASR completo (la partida dominante de todos los capítulos). Es el patrón para cualquier migración MKE V2→V1.2.
2. **Los reviewers escriben `verified_evidence` en formatos heterogéneos** (ids desnudos, dicts `{segment,quote}`, strings en prosa con varios ids, a veces con el id embebido): el paquete debe FIJAR el formato de la lista de evidencia; el normalizador del Manager tuvo que unificar a ids desnuros para `validate_review.py`.
3. **4ª recurrencia del naming por segundos crudos, con variante que V04 no caza**: nombres tipo f-001932 (1932 s crudos) parsean como HHMMSS válido dentro de duración — sólo el árbitro "decode vs minuto de la review + sonda byte-idéntica al instante declarado" los detecta. Para futuros runs: el pack genera las rutas Y el chequeo post-olas compara decode(min) contra el minuto revisado + los segundos declarados en el propio texto del revisor.
4. **El borrador durante la publicación existe**: 6 frames citados desaparecieron del árbol entre dos lecturas de ~1 min sin commit de borrado (mecánica inversa de la resurrección LiveSync documentada en FRAME-RECONCILIATION-2026-10-22.md). Reposición desde spool + re-extracción fresca; los validadores lo cazan (W06/V11) si el borrado deja inconsistencia.
5. **La migración no toca los otros capítulos**: los refinamientos posteriores (ch02/ch04/ch05/ch06) se registran como relaciones INTRODUCES→REFINES/EXTENDS en documentation §10 sin sobrescribir nada.

## CH12 OBSERVED (medido en Chapter 12)

| Métrica | Valor |
|---|---|
| Video | ep12-psicotrading.mp4 · 31:24.25 · SHA `b9fc83c5…` |
| ASR_WALL | 10.373,5 s = 172,9 min · **ASR_SPEED 0,18× · ASR_COST_MULTIPLIER 5,50×** — POR DEBAJO del pronóstico (0,24-0,28×): contención nueva EN VUELO (functions.test + postgres.test ajenos desde el minuto ~46 del ASR; el proceso cayó de ~200 % a ~133 % CPU) · **583 segmentos, 99 % habla (el más denso del curso)** |
| EXTRACTION_WALL | ≈ 66,8 min de runtime puro (6 EXTRACTORs SECUENCIALES, 135 claims; makespan 80,8 con checkpoint/reviews intercalados) |
| REVIEW_WALL | ≈ 40,3 min de makespan puro (32 revisores en 6 olas 5/5/5/5/5/7; 32/32 VALID); ventana gross 79,8 min intercalada con extracción |
| AGENT_WALL | 88,9 min / 31,4 min ≈ **170 min/h-video — OVER (~1,4×)**; proyección del checkpoint 144 (OVER 1,2× declarada ANTES de continuar) |
| Claims | 135 (135 SUPPORTED / 0 UNCERTAIN / 0 UNVERIFIED) · **135 instructor_statement / 0 visual** (relato verbal; 18 frames citados sostienen deícticos) |
| Frames | 32 base + 21 bajo demanda = 53; 18 citados, 35 contextuales inventariados |
| DOCVERIFY | independiente ONE-SHOT: **6 MATERIAL + 3 MENOR**, los 9 corregidos y re-validados (README ausente, 3 claims huérfanos de docs, cabecera de examples falsa, endurecimiento de 2 hedges dichos, DV09-001 sobre c-0103/q-ch12-011, garble inexistente «ímpitu», cita comprimida, cursor de frame) |
| Checkpoint 5 min | PASS (18/18 SUPPORTED en ~22,6 min; proyección 144/h OVER 1,2× < 2× → continuar con registro; real 170) |
| Proveedor | **0 muertes [1210]/[1310] en 39 subagentes** (6 extractores + 32 revisores + 1 DOCVERIFY; el original decía 33 — errata de conteo corregida 2026-10-22, valor original preservado aquí como historia) (segundo run consecutivo sin muertes, con contención del host) |
| TOTAL | ASR 08:51 → integración 14:07 ≈ 316 min; publicación remota ~14:12 ≈ **321 min ≈ 5h21m** (conciliado contra epochs/commits) |

## CH12 LEARNED (para futuros cursos)

1. **La corrección de un revisor también es una propuesta, no un hecho**: el revisor de min6 «corrigió» f-000619→f-000379 malinterpretando la fórmula (f-000619 SÍ codifica 06:19 = 379 s) y el integrador lo aplicó con sondas byte-idénticas — que NO detectan el error porque un frame del mismo instante coincide sea cual sea el nombre. **V04 lo cazó antes de publicar** (segundos 79/90/96 inválidos). Revertido y documentado. Lección doble: la sonda prueba el INSTANTE, no el NOMBRE — el árbitro del naming es la fórmula + V04; y toda corrección de worker se adjudica, jamás se aplica por autoridad.
2. **El defecto de naming del Manager alcanzó su 4ª recurrencia pese a la lección escrita EN el prompt**: rutas de frames base a mano en olas 1/3/4/5 (f-000119/f-000179/f-000239/f-000299, f-000719…, f-001019…, f-001199) — los revisores lo cazaron todas contra el directorio. Única palanca real: GENERAR las rutas del pack con código (fórmula), no escribirlas a mano.
3. **Pronóstico de ASR desactualizable en vuelo**: el preflight midió 0,24-0,28× y el run acabó en 0,18× por contención aparecida a mitad. Para futuros runs: re-medir la contención DENTRO del ASR (lectura a mitad) y revisar el pronóstico en el checkpoint, no sólo al cierre.
4. **99 % habla**: capítulo sin una sola observación visual load-bearing (135 instructor_statement); los frames sostienen deícticos. La epistemic estricta funcionó sin forzar visualización (patrón ch11 acentuado).
5. **El contrato de evidencia targeted (closeout ch10) se ejercitó con volumen por primera vez**: 5 frames adjudicados con prueba md5 de extracción fresca (incluida una frame solicitada por un revisor y materializada por el integrador, f-001245).
6. **Cobertura fronteriza adjudicada barata, 2º run consecutivo** (s-002200-002208 → c-0100; s-002506-002522 → c-0116): el protocolo ch11 evita reprocesar.

## CH11 CLOSEOUT (2026-10-22 — targeted post-publicación; mandato: 2 defectos documentales + duda q-ch11-012, sin reprocesar nada)

Gate CH11_CROSS_CHAPTER_REFERENCES + CH11_METRICS_RECONCILED + CH11_SOURCE_FIRST (q-ch11-012) = PASS. Dos correcciones documentales, cero cambios en claims:

1. **Referencia intercapítulo mal clasificada bajo CH07 (am-ch11-doc-001)**: documentation.md §16 y study-guide §6 colocaban bajo «CH07 (setups/checklist)» las conexiones de c-0012 y c-0070, pero ambas remiten literalmente al vídeo de noticias (ch10: s-000410 «he explicado antes con el vídeo de noticias»; s-002310/s-002313 «lo que os decía en el capítulo de noticias también»). El transcript de ch11 tiene exactamente dos referencias intercapítulo y ambas son a ch10; 0 menciones de setups/checklist en claims. Corrección: bullet CH07 eliminado, c-0070 movida al bullet CH10, README/COURSE-INDEX sin ch07 en prerrequisitos/referencias. Lección: al redactar §16 «relación con capítulos previos», verificar cada conexión contra los segmentos citados del transcript — el clasificador del run asignó el capítulo por tema del trade (el 4-jun también apareció en walkthroughs) y no por la referencia dicha.
2. **Errata de métricas (am-ch11-doc-002)**: el handoff publicó TOTAL_WALL ≈ 190 min sin respaldo; epochs/spools/commits dan ASR 23:17:43 → push 03:37:37 = **259,9 min ≈ 4h20m**. Reconciliado: ASR_WALL 96,1 min CONFIRMADO (asr.log; ventana epochs 103,5 con setup), EXTRACTION pura ~50,6 CONFIRMADA (makespan ventana 60,6 con checkpoint intercalado), REVIEW puro ≈ 48 min (no 42,9; ventana gross 92,6 solapada con extracción), INTEGRACIÓN 48,3 min (no ~40), TOTAL a publicación remota 4h20m (no 3h10m). Cifras originales preservadas como historia en el README (§ Throughput, errata). Lección: el TOTAL_WALL del handoff se estimó antes de terminar la integración + publicación; para ep12+ el TOTAL se cierra contra el commit de publicación, nunca contra estimación de dispatch.
3. **q-ch11-012 verificada sin cambios**: «el stop loss no se mueve» (c-0020) vs break even (c-0019/c-0028) — documentation §7 cita sólo el literal; rules R4 textual; la conciliación (stop inicial vs protección de profit) vive como ejercicio con «pista» en study-guide §7.4 y la duda queda PARTIAL en OPEN-QUESTIONS. Ningún documento convierte la lectura en resolución universal. La duda NO bloquea CH12.

## CH11 OBSERVED (medido en Chapter 11)

| Métrica | Valor |
|---|---|
| Video | ep11-riesgo.mp4 · 26:21.42 · SHA `590e4c3c…` |
| ASR_WALL | 5.765,7 s = 1h36m06s · **ASR_SPEED 0,27× · ASR_COST_MULTIPLIER 3,64×** — dentro del pronóstico del preflight (0,24-0,28× anunciado con la contención medida) · 320 segmentos, 96 % habla |
| EXTRACTION_WALL | ~50,6 min (6 EXTRACTORs SECUENCIALES, 80 claims; ≤4 claims/min — capítulo con pausas de pantalla) |
| REVIEW_WALL | ~42,9 min de makespan (27 revisores en 6 olas de 5/5/5/5/5/2; 27/27 VALID) |
| AGENT_WALL | ventana ≈ 100,5 min / 26,36 min ≈ **229 min/h-video — OVER (~1,9×)**: contención sostenida del host (echo-core 164 % + go test ajeno); proyección del checkpoint 240-250, real 229 |
| Claims | 80 (79 SUPPORTED / 1 UNCERTAIN visible / 0 UNVERIFIED) · **80 instructor + 0 visual** (capítulo VERBAL: la sustancia es toda dicha) |
| Frames | 27 base + 60 bajo demanda = 87 físicos; 54 citados, 33 contextuales inventariados |
| DOCVERIFY | independiente ONE-SHOT: **0 MATERIAL + 4 MENOR**, corregidos y re-validados; SOURCE-FIRST 17 claims con cifras (0 discrepancias), 12 q-ch11 barridas sin resolverse, 1160 wikilinks OK, SHA recomputado |
| Checkpoint 5 min | PASS (bloque 1 + min 0-4 en ~15,6 min; proyección 240-250/h OVER registrada ANTES de continuar; real 229) |
| Proveedor | **0 muertes [1210]/[1310] en 33 subagentes** (primer run del curso sin muertes pese a la contención del host) |

## CH11 LEARNED (para ep12+)

1. **El prompt-error de naming ES recursivo y cazó al propio Manager**: el pack decía «f-001621» para el frame fin-de-video (26:21 = 1581 s → f-002621 por fórmula); el EXTRACTOR lo detectó y usó el nombre correcto; el revisor de min26 lo verificó doble. La lección ch10 #1 se había aplicado a los prompts de los workers pero NO al pack del Manager. Para ep12: los ejemplos de naming de TODOS los artefactos (packs incluidos) se generan con la fórmula real.
2. **Capítulo verbal = 0 visual_observation es legítimo**: los 80 claims son instructor_statement (procedimientos y cifras verbales); los frames sostienen deícticos sin forzar observaciones visuales. La epistemic estricta no obliga a fabricar visual_observation.
3. **Cobertura fronteriza verificada barato**: los revisores marcaron segmentos load-bearing sin claim en su minuto; el integrador verificó la cobertura en claims de minutos contiguos (q-ch11-008/009 RESUELTAS con rastro) sin reprocesar nada.
4. **El contrato de evidencia del closeout ch10 no hizo falta en producción** (0 adjudicaciones targeted en el run) pero el `.deprecated_frame_names` va en la RAÍZ del capítulo, no en frames/ (error propio de este run, cazado por V11).
5. **Contención ≠ muertes de proveedor**: walls degradadas por echo-core+go-test, pero 33/33 subagentes completaron sin un solo [1210]/[1310]; la fiabilidad del proveedor y la velocidad del host son dimensiones independientes.
6. **Integración ch10-compatible**: pool con clave local (b*-NN), ids globales asignados post-integración (patrón ch10); el payload builder prefiere `id` si existe — asignar ids SOLO después de integrar.

## CH10 OBSERVED (medido en Chapter 10)

| Métrica | Valor |
|---|---|
| Video | ep10-noticias.mp4 · 35:48.47 · SHA `cdd6ee7b…` |
| ASR_WALL | 2h27m07s = 8.826,8 s (`asr.log`) · **ASR_SPEED 0,24× · ASR_COST_MULTIPLIER 4,11×** (nomenclatura normalizada post-ch09): contención sostenida del host (echo-core 157 % permanente + go tests ajenos intermitentes), dentro del pronóstico del preflight (0,25-0,30×) · 523 segmentos, 97 % habla |
| EXTRACTION_WALL | ~61 min de workers (6 EXTRACTORs SECUENCIALES, 199 claims; ventana 17:38→19:06 con la ola-1 de revisión intercalada) |
| REVIEW_WALL | ~49 min pura (ola-1 11,4 + olas 2-7 37,6; 36 minutos en 7 olas de 5-6; 4 muertes [1210] recuperadas con retry completo) |
| AGENT_WALL | 159 min (17:38:16→20:17:16, epochs/spools) / 35,8 min ≈ **266 min/h-video — OVER (objetivo ≤120, ~2,2×)**: contención sostenida + revisores prudentes con frames; la proyección del checkpoint (269) quedó a 1 % del real |
| Claims | 199 (193 SUPPORTED / 6 UNCERTAIN visibles / 0 UNVERIFIED) · 197 instructor + 2 visual · 3 CONTRADICTION documentadas |
| Frames | 36 base + 62 bajo demanda = 98; 91 citados, 7 contextuales inventariados |
| DOCVERIFY | independiente ONE-SHOT: **0 MATERIAL + 5 MENOR** (metadatos), 46 claims SOURCE-FIRST, 10 garbles preservados, 1860 wikilinks OK, SHA recomputado — corregidos y re-validados |
| Checkpoint 5 min | PASS (bloque 1 + min 0-4 VALID; proyección 269/h-video OVER, continuada con criterio ch09; real 266) |

## CH10 LEARNED (para ep11+)

1. **El prompt-error de naming es recursivo**: el Manager puso ejemplos de frames decimales (f-000119 por «1:59») en el prompt del extractor 1 y nombró el frame final con segundos crudos (f-002148) — los WORKERS cazaron ambos (el extractor contra `ls`; el revisor de min35 con la fórmula). Para ep11+: los prompts del Manager también deben generar sus ejemplos con la fórmula, y el revisor del último minuto verifica explícitamente el frame fin-de-video.
2. **Los visual_hints del extractor pueden describir pantallas que no existen** (2 casos: «gráfico» cuando había calendario Forex Factory o tarjeta del Excel). El revisor los corrigió; para ep11+: el checkpoint incluye leer 1-2 visual_hints contra sus frames.
3. **Dos revisores «en conflicto» pueden estar mirando minutos distintos** (Myfxbook min3 vs Excel min5): adjudicar leyendo el frame directamente cuesta menos que una revisión nueva.
4. **El integrador dropea los f-refs del pool** (sólo conserva s- + verified_evidence del revisor): si el Manager adjudica frames al pool, re-inyectarlos tras integrar (hecho con fixup; 8 refs).
5. **La contención sostenida NO rompió el pipeline** pero duplicó el wall vs ch07 despejado (266 vs 74/h): la decisión checkpoint-basada (continuar con registro, criterio ch09) fue correcta; para ep11+ con este host, anunciar OVER esperado en el preflight y medir la proyección al minuto 5.
6. **[1210] sigue siendo transitorio** (5 muertes, 5/5 recuperadas con un retry del worker completo; protocolo ch08 confirmado en extractores y revisores).

## CH10 CLOSEOUT (2026-10-21 — targeted post-publicación; mandato: 3 defectos puntuales, sin reprocesar CH01-CH10)

Gate CH10_REFUTED_CLAIM + CH10_NEWS_TIME_REVIEW + CH10_FRAME_EVIDENCE_SAFETY = PASS. Tres reparaciones, una por clase de defecto:

1. **c-0030 (claim visual refutado que permanecía UNCERTAIN/ACTIVE)**: revisión targeted independiente (5 puntos del minuto 5 verificados; 0 Myfxbook; el contenido descrito era del minuto 3, ya cubierto por c-0020) → supersession V1.2 c-0030→c-0200 (proposición nueva: el Excel «NEWS - ONE TO ONE ENG» del minuto 5, 7 frames de evidencia) + am-ch10-001 + q-ch10-010 RESUELTA. Un claim refutado ya no permanece activo «como registro honesto»: el historial honesto es el superseded navegable.
2. **q-ch10-001 (la «contradicción 8:15»)**: adjudicación SOURCE-FIRST con separación explícita instructor/gráfico/corroboración-externa (NY Fed calendario jun-2025: ADP 08:15 ET + ISM 10:00 ET el 4-jun; CPI 08:30 el 11-jun; 23-jun sin evento US 08:15). Resultado: la comparación con ch02/ch07 no demostraba contradicción — c-0165 y c-0164 promovidas a SUPPORTED (contradicciones retiradas), c-0069 permanece UNCERTAIN con la duda re-enfocada a la identificación (q-ch10-015 nueva), horas NO armonizadas. El frame «07:15» de f-001259 resultó ser el crosshair del gesto de entrada, no dato horario — leer el frame directo barató la re-adjudicación (lección CH10 #3 confirmada).
3. **integrate_reviews.py dropeaba refs f- adjudicadas** (CH10 LEARNED #4): contrato de clases de evidencia (PROPOSED / REVIEWER_VERIFIED / TARGETED_ADJUDICATED / CANONICAL): las f-* propuestas no verificadas NO entran al canónico; las de verified_evidence y las targeted-adjudicadas con prueba (<run>/evidence-adjudications.json) SÍ. Tests RED/GREEN: scripts/tests/evidence_safety_selftest.py (5 casos) + 9 selftests sin regresiones. Skills actualizadas (descripción del integrador).

DOCVERIFY targeted del closeout: 8 findings (4 MATERIAL de texto stale que contradecía la adjudicación + 4 MENOR) — corregidos y verificados contra el árbol físico; validadores PASS (library 0 findings, source-first 0). Lección reforzada: al reescribir un párrafo largo por reemplazo de prefijo, auditar la COLA del párrafo (el residuo pre-closeout fue el 100 % de los MATERIAL).

## CH09 OBSERVED (medido en Chapter 09)

| Métrica | Valor |
|---|---|
| Video | ep09-red-flags.mp4 · 34:54.53 · SHA `e4c22102…` |
| ASR_WALL | 2h09m46s (**0,27× realtime — el peor rate del curso**): contención severa del host (echo-core ~150 % + test Go de otro grind ~110 % sobre 8 cores; load 15). El probe de preflight (0,32×) subestimó el efecto de la contención creciente |
| EXTRACTION_WALL | ~49 min (6 EXTRACTORs SECUENCIALES, 137 claims; secuencial por la lección de cuota 1310 — sin incidentes) |
| REVIEW_WALL | ~70 min (7 olas de 5; 35/35 VALID; 0 errores [1210]/[1310] — la cuota del proveedor volvió tras el corte del 20-oct) |
| AGENT_WALL | ~119 min / 34,9 min ≈ **205 min/h-video — OVER (objetivo ≤120)**: contención de CPU heredada por los subagentes; registrado sin disfrazar |
| Claims | 137 (135 SUPPORTED / 2 UNCERTAIN visibles / 0 UNVERIFIED) · 133 instructor + 4 visual_observation · 1 CONTRADICTION documentada (c-0075) |
| Frames | 35 base + 38 bajo demanda = 73; 54 citados |
| DOCVERIFY | ONE-SHOT independiente sobre la biblioteca publicada (ver README del capítulo) |
| Checkpoint 5 min | PASS (min 0-4 VALID en ~12 min; proyección ~140/h-video OVER <2×; real 205 por contención) |

## CH09 LEARNED (para ep10+)

1. **El ejemplo del prompt es parte del contrato de naming**: el ejemplo «95 s → f-000095» de los prompts de la ola 1 era INCORRECTO (segundos crudos como nombre) y tres frames heredaron el patrón; cazado en el checkpoint, verificado contra el video (probes byte-idénticos) y normalizado pre-integración (f-000135/f-000337; f-000179 eliminado como duplicado de estado del base f-000259 con remapeo de evidencia). Para ep10+: el ejemplo del prompt debe generarse por la fórmula real (p.ej. 350 s → f-000550) y el checkpoint debe verificar los nombres de los frames creados por la ola 1.
2. **Los frames base también necesitan el prefijo**: la extracción de bases generó `000059.png` sin el `f-`; renombrado al contrato antes del render. El manifiesto y los archivos deben usar SIEMPRE el stem `f-HHMMSS`.
3. **V11 chapter-local extendido para aclaraciones targeted**: los wikilinks cross-chapter ([[…/CLAIMS#c-XXXX]], [[…/transcript#^s-XXXX]]) ya no disparan V11 en el capítulo anfitrión (su destino lo validan los checks W); el token desnudo de otro capítulo sigue fallando. Regresión: fixtures_selftest caso I. Habilita las aclaraciones targeted del contrato (am-ch09-001/002 en ch07) sin falsos positivos.
4. **Colisión base/bajo demanda en el mismo HHMMSS**: un frame bajo demanda a los XX:59 colisiona con el base (capturado a XX:59.5); resolución aplicada: si el base muestra el referente (verificado visualmente), se cita el base y el on-demand se elimina como duplicado de estado. Documentado en el contrato de revisión.
5. **El extractor no debe normalizar sin respaldo literal aunque el contexto sea fuerte**: 0 MATERIAL en SOURCE-FIRST; los 2 TDREQ («dole»→DOL en c-0120/0121) se cerraron con la marca [ASR: 'dole'] + la adjudicación del revisor por frames.
6. **El proveedor se recuperó solo**: tras el corte [1310] del 20-oct, el 21-oct la cuota volvió; 17 subagentes grandes sin un solo [1210]/[1310]. Mantener despacho en olas de 5.
7. **La contención del host domina el wall**: con load 15 el ASR cayó a 0,27× y los subagentes se arrastraron; el wall honesto (205/h-video) se registra OVER sin disfrazar. Para ep10+: medir load ANTES del ASR y registrar el pronóstico; si hay grinds ajenos, avisar al owner en el checkpoint.

## CH09 CLOSEOUT (cierre semántico 2026-10-21 — métricas reconciliadas + defecto residual de DV09)

Auditoría del cierre halló que 2 de las 8 correcciones del DOCVERIFY in-mission NO estaban aplicadas en el árbol publicado pese a estar registradas como corregidas: **DV09-001 (MATERIAL)** — documentation §2 y study-guide resolvían el garble abierto «mover tu tarjeta breakable» [ASR] de c-0015/q-ch09-002 al candidato «stop a break even» — y **DV09-002 residual en examples E5** (DV09-006, MENOR: frames de c-0032 adyacentes a c-0026). Corregidas con amendmends (am-ch09-doc-001/002), q-ch09-002 preservada OPEN, c-0071/c-0129 intactos, y re-verificadas con DOCVERIFY targeted ONE-SHOT (spool `run/docverify-closeout/`), que además validó la regla nueva: **una síntesis no puede resolver categóricamente una ambigüedad material que el claim citado mantiene abierta, salvo evidencia adicional adjudicada** (incorporada al contrato del DOCUMENTATION_VERIFIER y a la Composición de la skill; barrido 14 preguntas OPEN/PARTIAL × 5 docs = 0 casos residuales).

Reconciliación de métricas (am-ch09-doc-003; la tabla OBSERVED de arriba se conserva como historia, con sus erratas aplicadas así):

| Métrica | Valor original publicado | Valor reconciliado (epochs/spools/logs) |
|---|---|---|
| ASR_WALL | 2h09m46s (0,27× realtime) | 7.785,8 s por `asr.log` (el valor del proceso era correcto; la ventana por epochs 136,2 min incluye setup/post-proceso). **ASR_SPEED** = 2094,5/7785,8 = 0,27× · **ASR_COST_MULTIPLIER** = 3,72× |
| EXTRACTION_WALL | ~49 min | ~51 min (spools de bloques 11:20:33→12:11:58) |
| REVIEW_WALL | ~70 min | ~77 min (12:14:58→13:32:19; endpoint real = review-min31, no min33) |
| AGENT_WALL | ~119 min (handoff) / ~109 min (README) ≈ 205 y 187 min/h-video | **~129 min ≈ 221 min/h-video** (suma de fases observadas; ventana completa 131,8 min) — ambos valores originales eran subestimaciones sin respaldo de epochs |
| «El peor rate del curso» | afirmado en ch09 (0,27×) | **FALSO en unidades homogéneas**: mezclaba velocidad (video/wall) con multiplicador de costo (wall/video; así lo usa ch08 con «1,76×»). En costo ch09 = 3,72× = 5.º de 8; el peor es ch04 = 9,06× (velocidad 0,11×) |

Lecciones duraderas para ep10+: (1) **corrección declarada ≠ corrección aplicada** — tras adjudicar findings, verificar el árbol físico final (grep del texto corregido) antes de registrar PASS; (2) **los rates se comparan en una sola unidad** — publicar SIEMPRE ASR_SPEED y ASR_COST_MULTIPLIER explícitos, nunca «N× realtime» ambiguo; (3) la regla anti-resolución-de-ambigüedades rige para ep10+ en composición y DOCVERIFY.

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
