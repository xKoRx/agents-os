# review-notes — ch04-entradas (Clutifx · Chapter 04)

Notas del proceso de extracción y revisión (2026-10-19). La autoridad es [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch04-entradas/claims.jsonl|claims.jsonl]].

## Pipeline ejecutado

- ASR: faster-whisper large-v3 int8 CPU (beam 5, es p=1,00), 359 segmentos, 98 % habla, ligado al SHA. Wall **4h10m (0,11× realtime)** — la máquina estaba cargada por otros jobs (echo-backtest, ~400 % CPU en procesos concurrentes); el rate canónico de los capítulos previos era 0,21–0,38×.
- Extracción: 6 EXTRACTORs ONE-SHOT paralelos (bloques 0–5, 5–10, 10–15, 15–20, 20–25, 25–27:35), 119 claims en 15,3 min.
- Revisión: 28 MINUTE_REVIEWERs ONE-SHOT (una revisión por minuto, 4 olas de 5/7/7/9), 28/28 `MINUTE_REVIEW = VALID` (cardinalidad exacta, 91,9 min).
- Checkpoint a los 5 minutos: 21/21 VALID → proyección 152 min/h-video (continúa); real final 233 min/h-video (dentro de la banda 2× = 240; exceso por verificación visual frame-a-frame del contrato v1.1+, igual que ch03).
- Integración mecánica: `integrate_reviews.py` aplica veredictos/`verified_evidence`/preguntas tras `validate_review.py` por minuto; 7 correcciones de statement propuestas por reviewers, revisadas por el integrador y aplicadas al pool antes de la escritura canónica.

## Veredictos y adjudicaciones

- **119 claims: 111 SUPPORTED / 8 UNCERTAIN / 0 UNVERIFIED** (33 con preguntas sin resolver registradas). Los 8 UNCERTAIN son garbles ASR irresolubles o deícticos no identificables en frames — dudosos visibles, no forzados.
- **c-0016 (V13)**: el EXTRACTOR la propuso como `model_inference` (síntesis del orden de entradas); el revisor la dio SUPPORTED; el integrador la adjudicó `instructor_statement` — el orden es contenido enseñado (s-000423/s-000444/s-000451ss) y verificado visualmente en c-0020 (f-000507/f-000514/f-000535). Nota de adjudicación dentro del claim.
- **c-0078 (min 18) UNCERTAIN por CONTRADICTION**: el ASR dice "Take profit aquí abajo" pero la posición dibujada (f-001833) es larga con TP arriba y stop abajo; correction propuesta preserva la palabra dicha con [ASR].
- **c-0083 (min 19)**: el reviewer RECHAZÓ el frame citado por el extractor (f-002059 es gráfico 4h, no 1h como decía la nota) y lo sustituyó por f-001959 — regla "no aceptar un frame que no muestre lo afirmado" en acción.
- **c-0102 (min 24) UNCERTAIN**: niveles 1D mal leídos por el extractor (1,4645/1,4565 → reales 1,15145/1,14565 verificados con zoom en f-002459); corrección aplicada.
- **c-0099 (min 23)**: "el DM30" [ASR] resuelto como "el de M30" por el frame f-002359 (gráfico 30M en pantalla).
- **c-0017/c-0096 PDM espejado**: el instructor usa el PDM en el ALTO del rango en contexto bajista (y en shorts), frente a la definición de ch03 (low como soporte en alcista); no es contradicción literal (ch03 acota a alcista) pero la generalización queda abierta (q-ch04-002).
- **visual_hints erróneos detectados por reviewers** (2): c-0046/c-0048 decían "gráfico 2h" para segundos en que ya estaba en 15m (f-001118/f-001121); c-0104 decía "3 horas" donde había 4h (f-002519). Documentado en reasons; los statements no se ven afectados.

## Garbles ASR del capítulo (para futuros capítulos)

| Garble | Lectura | Nota |
|---|---|---|
| "tartle/tartel sub/soup", "tarde sub", "tardel sub", "target sub", "tarde supa", "turtle sub", "Tartel Soup" | Turtle Soup | variantes nuevas sobre las de ch02/ch03; referente no ambiguo (toma de liquidez + reacción, verificada en frames) |
| "break y venía" | break even | s-000611 |
| "orden blog" | order block | (bloque 2) |
| "temporada(s)" | temporalidad(es) | recurrente |
| "vallas"/"bayas" | bias | conocido de ch02/ch03 |
| "veris" | bearish | conocido de ch02 |
| "de favor" | a favor | palabra funcional (s-001221 y ss. sin error) |
| "la entidad" (s-000144) | ¿"la entrada"? | SIN resolver (q-ch04-001) |
| "el doble" (s-000808, s-001001, s-001547, s-002443) | ¿DOL? | preservado [ASR]; contexto favorece DOL (objetivo), sin confirmación literal en este capítulo |
| "0 de ladón" (s-001027ss) | ¿0 (de) drawdown? | SIN resolver (q-ch04-005) |
| "el sub más hondo" (s-001004) | ¿stop más hondo / Turtle Soup más hondo? | SIN resolver |
| "feliz swing" (s-000723) | ¿"este swing"? | SIN resolver |
| "método tema broker pues la entidad" (s-000735–747) | ¿? | SIN resolver |
| "el tag del súper" (s-001753ss) | ¿"el doble del superior"? | SIN resolver; el referente visual está en los MÍNIMOS (f-001802), no en el objetivo alcista (q-ch04-007) |
| "para reiniciado" (s-001917ss) | ¿"ya reiniciado"/"pendiente de reiniciar"? | SIN resolver |
| "ante/delante de Asia" (s-001616a, s-001638) | ¿"antes de Asia"/"durante Asia"? | SIN resolver |
| "tulón" (s-002610) | ¿"tu long"? | SIN resolver |
| "una hora que ya no es mía" (s-001858ss) | ¿? | SIN resolver |
| "el 2" (s-001317) | ¿low numerado / segundo rango? | SIN resolver |
| "a favor de la primera" (s-001058) | ¿de la primera qué? | SIN resolver |
| "el DM30" (s-002352) | "el de M30" | RESUELTO por frame f-002359 |

## Contrato TERM_DISAMBIGUATION aplicado

Todos los "el doble" del capítulo quedaron preservados como palabra dicha con [ASR] y candidatos en notes/unresolved_questions (DOL objetivo vs DXY índice), y el chequeo SOURCE-FIRST extendido (`check_term_sources.py` con garbles ambiguos como aliases) pasó con 0 findings sobre los 119 claims vivos. El DXY no aparece dicho en el capítulo; donde el contexto visual resolvía el referente (objetivo marcado en pantalla), el reviewer lo registró en `reason` sin sustituir el statement.

## Frames

- 28 base (fin de minuto, manifiesto `frames/.base_frames`; minuto 27 parcial en f-002734, pantalla negra al cierre del video) + 77 bajo demanda extraídos y verificados visualmente por los revisores = 105.
- Nota: f-002734 (fin del video) es pantalla negra — sin observación visual posible al cierre.
