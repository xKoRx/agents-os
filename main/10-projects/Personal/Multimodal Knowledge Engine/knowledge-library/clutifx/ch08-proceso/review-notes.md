# review-notes — Clutifx Chapter 08 (Proceso)

Notas de revisión y decisiones del run. Autoridad de claims: `claims.jsonl` ([[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch08-proceso/CLAIMS|CLAIMS]]).

## ASR y provenance

- faster-whisper large-v3 int8, es (p=1,00), beam 5, **276 segmentos, 97 % de habla**, ligado al SHA `5495798b…`.
- **ASR wall 30,2 min (1,76× realtime — el peor rate del curso)**: la máquina corría con sesión gráfica y contención de CPU (ASR a ~3,7 cores nice 25). Lección de ch07 confirmada en sentido inverso: el rate ASR depende del estado de la máquina (0,68× despejada vs 1,76× contendida). Para ep09+: considerar cerrar sesión gráfica o renicear el resto.
- Segmentación fina: varios segundos con 2 segmentos (sufijos a/b, p.ej. s-000224/s-000224a) — el 97 % de habla con frases cortas; el context pack avisó a los workers.

## Ejecución de waves (cuota del proveedor)

- **Dispatch híbrido**: extracción por bloques (4 workers, cada uno tras el anterior o en pareja con un revisor chico), revisión por minutos en waves de 4-5 revisores. La cuota aguantó TODO el capítulo (sin [1310] de agotamiento).
- **2 muertes transitorias [1210]** ("Invalid API parameter" del proveedor): min 2 (en wave paralela) y min 15 (en wave paralela). Ambos recuperados con retry secuencial que completó el minuto con frames verificados (el error NO es determinista por imagen: los mismos workers leyeron otros PNG sin problema).
- **Checkpoint 5 min**: min 0–4 VALID en ~20 min (proyección ~200 min/h-video, sobre objetivo 120 pero <2× → continuado con registro). Real final: **agent wall ≈93 min ≈ 327 min/h-video** — inflado por (a) contienda de CPU, (b) los 2 retries [1210] (~20 min extra), (c) revisores que hubieron frames bajo demanda (hasta 26 tool uses y 12 frames por minuto). Las cifras honestas están en el README; OVER registrado — no se declara PASS de throughput.

## Decisiones de revisión notables

- **Minuto 14 en dos pasadas**: la primera review (2 claims del bloque 3) quedó corta cuando el bloque 4 añadió 2 claims más al minuto 14; el payload regenerado exigía 4 resultados. Promovida la segunda pasada (review-min14b) como la review del minuto; la primera se conserva como `review-min14-first-pass.json` (auditoría).
- **Integración idempotente**: un run parcial del integrador con un solo minuto sobrescribió claims.jsonl desde el pool; corregido re-ejecutando la integración completa 0–16 (86/86 aplicados). Lección: integrate_reviews.py SIEMPRE con la lista completa de minutos.
- **19 correcciones aplicadas vía pool** (literalidad de citas: «como haría si», «tenemos a [ASR]», «marcamos el objetivo», «time frame de momento lo ignoras», «y esperar»; evidence de frontera: +s-000249 en c-0010, +s-000505 en c-0018, +s-000922 en c-0043; visual_hints corregidos por frame real: c-0004 44→47, c-0040 522→526, c-0065 814→817; encuadres no dichos retirados: c-0037 «Descenso continúa»; interpretaciones marcadas: c-0041, c-0045; glosa innecesaria retirada: c-0020 «[ASR: ≈ crea]»).
- **Duda resuelta por frames en review**: c-0071 (¿4d o 3d?) — f-001453 = EURUSD 4D durante «este de cuatro días»; el «si vamos a tres días» de s-001443 queda registrado como probable desliz del instructor (q-ch08-007).
- **Epistemic uniforme instructor_statement**: este capítulo no produjo visual_observation — todo lo afirmado es dicho; los frames corroboran en `evidence` (64 citados) y los referentes puramente visuales quedaron como unresolved_questions en vez de afirmarse (84 agrupadas en 8 preguntas).
- **Identidad de los pares resuelta en review**: el segundo par es AUDUSD (f-000552/f-000559 con símbolo legible); el instructor no lo nombra en el audio del tramo mostrado.

## Cobertura y presupuesto de frames

- 18 frames base (manifiesto `frames/.base_frames`) + **70 bajo demanda** extraídos y verificados visualmente por los revisores = 88 PNG; **64 citados** en `claims.jsonl.evidence`. Densidad 4,1/min (capítulo de recorrido continuo multi-TF: el instructor cambia de timeframe ~30 veces; presupuesto por bloque declarado, exceso justificado).
- f-001704 (frame final) es el negro de cierre: existe por el manifiesto pero no se cita.

## Verificación documental independiente (DOCVERIFY)

- `documentation-verifier` sigue caído (provider binding ausente, sexto capítulo consecutivo). Fallback documentado: subagente `general-purpose` ONE-SHOT con contrato adversarial completo. Resultado en el reporte de sesión.
- Checks deterministas ejecutados por el integrador: `check_term_sources.py` y `validate_library.py` (ver estado final en README/reporte).
