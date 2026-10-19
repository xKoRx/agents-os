# review-notes — Clutifx Chapter 05 (SMT)

Notas de la revisión por minuto (19/19 `MINUTE_REVIEW = VALID`) y del proceso. Estado final: **100 claims: 99 SUPPORTED / 1 UNCERTAIN / 0 UNVERIFIED** · 80 instructor_statement + 20 visual_observation · 0 model_inference.

## ASR y provenance

- ASR: faster-whisper large-v3 int8 CPU (beam 5, es p=1,00), 193 segmentos, 96 % habla, ligado al SHA. Wall **92,5 min (0,20× realtime)** — rate canónico (probe preflight 0,21×; la máquina estaba despejada, a diferencia de ch04).
- Preflight generalizó `integrate_reviews.py` de ch04 a los scripts de la skill (paths por argumento + normalización de refs `f-XXXXXX.png`, defecto real de ch04) con `integrator_selftest.py` (5/5). El selftest cazó un bug de índice en el descubrimiento de minutos antes de producción.

## Decisiones de revisión notables

- **Myfxbook (c-0006)**: el garble "MyForexBook [ASR]" se resolvió con la URL visible en pantalla ([00:42] f-000042: `myfxbook.com/forex-market/correlation`); el reviewer propuso la corrección y el integrador la aplicó. Es una verificación por fuente visual, no una normalización de glosario.
- **"el dol" (c-0028, s-000504)**: statement preserva la palabra dicha con [ASR]; el reviewer adjudicó la lectura **DOL (objetivo)** en `reason` con los frames f-000514/f-000603 (euro completa el rango y va a los niveles objetivo marcados, alcanzados en pantalla). Sin confirmación literal del término en este capítulo → q-ch05-004 abierta.
- **DXY es término genuino de este capítulo**: dicho literalmente (s-000032), escrito en el esquema del instructor (f-001559) y con garbles propios ("el tema de x y" s-001531 → DXY por rótulo; "dxi" → variante ortográfica del mismo acrónimo; "Punto el dxi" s-001555 → acción de dibujo, f-001557). Aquí NO aplica la lectura DOL: el contexto de divergencia/índice es inequívoco. El briefing del context pack (DOL vs DXY) operó como estaba diseñado.
- **"S&T" / "de sentir" / "empty"**: garbles recurrentes de SMT de lectura única en este capítulo (SMT dicho literal en s-000740, s-001116, s-001332, s-001355, s-001431, s-001635); normalización aceptada por referente único, documentada por los reviewers en `reason`.
- **c-0073 (UNCERTAIN, la única)**: sobre "voy a sacar la de sentido arriba [ASR]" (s-001246) los frames muestran que el dibujo del caso 2 NO pasa a velas alcistas (mantiene la orientación del primer caso con objetivos abajo) — contradicción marcada como "CONTRADICTION:" y claim dejado en UNCERTAIN con el statement corregido que preserva la palabra dicha. q-ch05-007.
- **Revisión que corrigió el extractor**: los reviewers ajustaron tiempos de visual_hint erróneos (c-0099: second 1804→1084, excedía la duración del video) y descartaron frames que no mostraban lo afirmado (f-000053: columna NZDUSD fuera de viewport; f-001400: aún caso 2 cuando el claim es del caso 3; f-000148: diálogo de búsqueda tapa el gráfico).
- **Preservación de la palabra dicha**: "veris" [ASR] (bearish), "por una es en ti" [ASR], "el que habituó las entradas" [ASR], "reinicia la perfección" [ASR], "Felux Swing" [ASR] — todos quedaron en statements/notes con candidatos, sin normalizaciones por glosario.

## Correcciones aplicadas en integración (reviewer propone, integrador aplica)

| Claim | Corrección |
|---|---|
| c-0006 | "MyForexBook [ASR]" → "Myfxbook" (URL verificada en frame) |
| c-0035 | "ya estaba" → "ya está" (presente dicho) + re-encolado literal de "de dos días de aquí" |
| c-0050 | "esas velas" → "estas velas" (literal en s-000908) |
| c-0073 | retirada la glosa inventada "pasando las velas a sentido alcista"; statement corregido preservando [ASR] y documentando la contradicción |
| c-0083 | retirada la glosa no dicha "(en la estrategia)" |
| c-0090 | "tienen" → "tenemos" (literal: "Y tenemos esto como objetivo en el DXI") |

## Garbles ASR del capítulo (para futuros capítulos)

| Garble | Lectura | Nota |
|---|---|---|
| "S&T", "de sentir", "sentir", "empty" | SMT | lectura única en el capítulo (SMT literal en ≥6 segmentos) |
| "MyForexBook" | Myfxbook | RESUELTO visualmente (f-000042) |
| "GDP" (s-000202) | GBP | contexto de pares |
| "veris" (s-001211) | bearish | conocido de ch02/ch04 |
| "el dol" (s-000504) | ¿DOL? | adjudicado DOL por contexto+frames; sin confirmación literal (q-ch05-004) |
| "el tema de x y" (s-001531) | DXY | resuelto por rótulo escrito en pantalla (f-001559) |
| "dxi" / "DXI" | DXY | variante ortográfica del mismo acrónimo (rótulo en pantalla) |
| "Punto el dxi" (s-001555) | ¿"Pinto el DXY"? | acción de dibujo; f-001557 |
| "JP" (s-000032) | ¿JPY? | SIN resolver (q-ch05-001) |
| "por una es en ti" (s-000648) | ¿"por la SMT"? | SIN resolver (q-ch05-005) |
| "el que habituó las entradas" (s-000811) | ¿"el capítulo de las entradas"? | SIN resolver (q-ch05-008) |
| "reinicia la perfección" (s-001024/1026) | ¿término del curso o garble? | SIN resolver (q-ch05-006) |
| "el lunes, el jueves" (s-000116) | día del caso E1 | contradicción; frames muestran jueves (12/26 jun '25) (q-ch05-002) |
| "Felux Swing" (s-001817) | ¿failure swing? | roadmap ep06; a confirmar con el siguiente capítulo (q-ch05-009) |
| "otros sales" (s-001749) | ¿"o sales"/"otros salen"? | menor, no afecta sustancia |
| "play más alto" (s-000858) | ¿plazo/temporalidad? | menor, sin claim propio |

## Lecciones de método para ep06+ (delta sobre METHODOLOGY-FEEDBACK)

1. El checkpoint de 5 min volvió a operar: PASS con 26/26 y proyección honesta (real 143 min/h-video, mejor capítulo).
2. Las 3 olas de 5/7/7 con payloads ~6 claims/minuto dieron el makespan más bajo del curso (34,1 min de revisión); el despacho por tamaño de payload (payloads ya homogéneos por construcción) sigue siendo suficiente.
3. El briefing de términos críticos EN EL PROMPT del reviewer (no sólo en el context pack) evitó el defecto DOL/DXY: cero sustituciones indebidas; el único garble adjudicado sin literal quedó en q-ch05-004, igual que el patrón ch04.
4. Los reviewers llegaron con la instrucción de descartar frames que no muestren lo afirmado: 4 frames extraídos y no citados quedaron en disco como auditoría (sin contaminar evidence).
