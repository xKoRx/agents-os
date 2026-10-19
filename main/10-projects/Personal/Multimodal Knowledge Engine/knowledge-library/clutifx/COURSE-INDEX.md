# Clutifx — Índice del curso (knowledge library)

Índice vivo de la biblioteca de conocimiento del curso Clutifx. Cada capítulo vive en su carpeta con biblioteca completa (README, transcript, frames, claims, documentación). Este índice NO reemplaza los README por capítulo; apunta a ellos.

Fuentes físicas de los videos (locales, NO en Git): `/home/kor/mke/course/epNN-*.mp4`.

## Estado del curso

| # | Carpeta | Video | SHA-256 (prefijo) | Duración | Biblioteca | Estado |
|---|---|---|---|---|---|---|
| 01 | `ch01-introduccion/` | `ep01-intro.mp4` | `4de8f12d…` | 34:04 | README · claims.jsonl · documentation.md (extracción MKE V2 histórica, 1.527 claims) | PUBLICADA (motor anterior; ver su README) |
| 02 | `ch02-time/` | `ep02-time.mp4` | `fb8b3de4…` | 17:09 | biblioteca completa (skill course-knowledge-extraction, 98 claims SUPPORTED vigentes + 2 superseded por remediation DOL/DXY 2026-10-19) | DONE 2026-10-18 (remediated 2026-10-19) |
| 03 | `ch03-bias/` | `ep03-bias.mp4` | `c52dafa8…` | 41:51 | biblioteca completa (skill course-knowledge-extraction, 211 claims SUPPORTED + 6 superseded por remediation DOL/DXY) | DONE 2026-10-18 (remediated) |
| 04 | `ch04-entradas/` | `ep04-entradas.mp4` | `f69f7d62…` | 27:35 | biblioteca completa (skill course-knowledge-extraction, 111 claims SUPPORTED + 8 UNCERTAIN) | DONE 2026-10-19 |
| 05–12 | — | `ep05-smt.mp4` … `ep12-psicotrading.mp4` | sin procesar | — | — | PENDIENTE (secuencia local verificable por nombre de archivo; ep05 anunciado en ch04 [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch04-entradas/CLAIMS#c-0119|c-0119]]) |

## Capítulo 01 — Introducción (`ch01-introduccion/`)

- **Temas**: presentación del temario del curso; los 7 conceptos base: rango, rango pendiente/reiniciado, Turtle Soup, SMT, failure swing, order block, Power of 3.
- **Conceptos principales**: el rango como base de la estrategia (toma un extremo y cierra dentro → el precio va a completarlo); pendiente (a favor) vs reiniciado (en contra); invalidación por cierre fuera.
- **Reglas relevantes**: ver `ch01-introduccion/documentation.md` (motor MKE V2; grounding parcial — 1.140/1.527 claims SUPPORTED cuando se abortó la revisión).
- **Prerrequisitos declarados**: curso intermedio anterior ("sirvió para sentar la base").
- **Referencias**: anuncia ampliación de todo en este curso; enlaza hacia adelante con los temas por episodio.
- **Links**: [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch01-introduccion/README.md|README]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch01-introduccion/documentation.md|documentation]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch01-introduccion/claims.jsonl|claims.jsonl]] *(legacy MKE V2: granularidad por ventana wNNNN, sin anchors por claim — navegación por documento y sección)*.

## Capítulo 02 — Time (`ch02-time/`)

- **Temas**: timeframes de la estrategia (lista base y límites); horario New York (UTC-4); pirámide de aperturas de velas; horas clave del día (5 a.m./p.m., 3 a.m., 8–9 a.m.); recorrido multi-timeframe EURUSD y dirección por rangos alineados; sesiones del día en velas de 4 h/6 h; noticias y la vela que las contiene; coger la expansión; "High Time Frame manda".
- **Conceptos principales**: algoritmo de rangos (crear → completar → opuestos → completar); horas clave; sesiones = velas 4 h; expansión; rangos superiores (HTF). Refinamiento del rango de ch01: tras Turtle Soup + reacción no hace falta el cierre.
- **Reglas relevantes**: 16 reglas en `ch02-time/rules.md` (R1–R16), todas citadas.
- **Prerrequisitos declarados**: los conceptos del capítulo 1 (usa "el rango pendiente que os he enseñado antes", "el Turtle Soup", "Power of 3", "SMT" sin redefinirlos).
- **Referencias**: hacia atrás → capítulo 1 (explícito ×2); hacia delante → "el episodio siguiente de la estrategia" (explícito) y el contexto para entrar fuera de horas clave (explícito, capítulo no nombrado).
- **Links**: [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch02-time/README.md|README (provenance y métricas)]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch02-time/documentation.md|documentation]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch02-time/rules.md|rules]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch02-time/concepts.md|concepts]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch02-time/examples.md|examples]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch02-time/study-guide.md|study-guide]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch02-time/review-notes.md|review-notes]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch02-time/CLAIMS.md|CLAIMS (proyección navegable por claim)]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch02-time/FRAMES.md|FRAMES (inventario)]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch02-time/OPEN-QUESTIONS.md|OPEN-QUESTIONS]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch02-time/AMENDMENTS.md|AMENDMENTS]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch02-time/claims.jsonl|claims.jsonl (autoridad)]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch02-time/transcript.md|transcript]] · frames/

## Capítulo 03 — Bias (`ch03-bias/`)

- **Temas**: cómo se saca el bias (la dirección): recorrido desde la temporalidad más alta marcando objetivos y rangos; jerarquía de TFs por rol (contexto HTF / DOL medio plazo / DOL sesión / entradas); rangos a favor vs en contra; vela de la izquierda; PDM (nuevo); aperturas de vela y Power 3; NFP y noticias; gestión (break even, parciales); rechazo explícito del "solo time-based".
- **Conceptos principales**: el bias se enseña por procedimiento, no por definición; "normalmente el bias nos viene dado por temporadas altas: 6h, 8h, 12h, 1D, 2D, 3D"; DOL = objetivo al que va el precio ("en rangos de temporalidad más alta, vela de la izquierda predominando e ir para allí"); el rango perfecto ocurre en extremos; sin rangos a favor no hay entrada.
- **Reglas relevantes**: 18 reglas en `ch03-bias/rules.md` (R1–R18), todas citadas.
- **Prerrequisitos declarados**: el vídeo de timeframes (ch02, explícito en s-000006), el curso intermedio anterior (mencionado), Turtle Soup / Power of 3 / rangos de ch01 (usados sin redefinir).
- **Referencias**: hacia atrás → ch02 (explícito) y curso intermedio; hacia delante → "el siguiente vídeo va a ser el de las entradas" (explícito, ep04) y un vídeo de "extras" sobre cuándo el reiniciado debe completarse (explícito).
- **Links**: [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch03-bias/README.md|README (provenance y métricas)]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch03-bias/documentation.md|documentation]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch03-bias/rules.md|rules]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch03-bias/concepts.md|concepts]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch03-bias/examples.md|examples]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch03-bias/study-guide.md|study-guide]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch03-bias/review-notes.md|review-notes]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch03-bias/CLAIMS.md|CLAIMS (proyección navegable)]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch03-bias/FRAMES.md|FRAMES (inventario)]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch03-bias/OPEN-QUESTIONS.md|OPEN-QUESTIONS]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch03-bias/AMENDMENTS.md|AMENDMENTS]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch03-bias/claims.jsonl|claims.jsonl (autoridad)]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch03-bias/transcript.md|transcript]] · frames/

## Cómo consultar la biblioteca (preguntas tipo)

- ¿Qué dice Clutifx sobre X? → `GLOSSARY.md` (término → capítulos) y luego `documentation.md` del capítulo.
- ¿Dónde está el ejemplo original de una regla? → `examples.md` del capítulo (timestamps + frames).
- ¿Es una afirmación confirmada? → `claims.jsonl` del capítulo (verdict + evidence).
- Corrección puntual → mecanismo de complemento de la skill: re-consultar el frame/transcript citado; nunca re-procesar el video.

Metodología vigente: [[30-resources/agents/skills/course-knowledge-extraction/SKILL.md|course-knowledge-extraction (V1.2)]] · [[30-resources/agents/skills/course-knowledge-worker/SKILL.md|course-knowledge-worker]]. Feedback de método por capítulo: [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/METHODOLOGY-FEEDBACK.md|METHODOLOGY-FEEDBACK]].
