# ch02-time — Clutifx · Capítulo 2

Biblioteca de conocimiento del segundo video del curso Clutifx, extraída con la
metodología `course-knowledge-extraction` (skill canónica del vault, NO el
pipeline MKE V2).

## Identidad de la fuente

| Campo | Valor |
|---|---|
| Archivo | `/home/kor/mke/course/ep02-time.mp4` |
| SHA-256 | `fb8b3de48535bdf43a09bf820c27512d2f021f63b7c12391484b4304c6337bfb` |
| Duración | 17:09.4 (1.029,4 s), h264 + aac |
| Tema real del capítulo | Timeframes de la estrategia, horarios de apertura de las velas y momentos clave del día |
| Tema | El nombre de carpeta `ch02-time` replica el nombre del archivo (`ep01-intro` → `ch01-introduccion`); el instructor no pronuncia un título de capítulo en el video |

## Provenance de la extracción

| Campo | Valor |
|---|---|
| Fecha | 2026-10-18 (sesión 02:54–04:35 aprox.) |
| ASR | faster-whisper `large-v3`, int8 CPU, language=es (p=1,00), 213 segmentos, 97 % habla, ligado al SHA; wall 45,1 min (0,38× realtime) |
| Extracción | 3 subagentes GLM ONE-SHOT en paralelo (bloques 0–5:12, 5:12–10:05, 10:05–17:05), 98 claims propuestos en ~8,6 min |
| Revisión | 18 subagentes ONE-SHOT — UNA revisión por minuto de video (5–7 workers paralelos, 3 olas), ~19,8 min totales |
| Modelo | GLM (subagentes locales de agente; sin API pagada, sin cambio de modelo) |
| Run dir | `/home/kor/mke/clutifx-ch02-20261018/` |

## Métricas

| Métrica | Valor |
|---|---|
| Claims totales | 98 |
| SUPPORTED / UNCERTAIN / UNVERIFIED | 98 / 0 / 0 (4 UNCERTAIN iniciales adjudicados en integración con recursos ya citados; ver `review-notes.md`) |
| Contradicciones marcadas | 0 |
| Frames base (fin de minuto) | 18 |
| Frames bajo demanda | 47 |
| Referencias visuales sin resolver | 1 pregunta abierta (q-ch02-001: referente del rectángulo descartado en c-0056 — ver OPEN-QUESTIONS.md); la regla del claim mantiene soporte independiente |
| Rules / concepts / examples documentados | 16 / 17 / 11 |
| Coverage | 18/18 minutos de video con claims y revisión |
| Checkpoint 5 min | PASS (proyección ≈ objetivo; continuar automático) |
| Wall time total observado por el Owner | 2h06m (incluye ASR 45,1 min, orquestación, integración y publicación) |
| Throughput subagentes (solo extracción+revisión) | ~28,4 min wall para 17,2 min de video ≈ 99 min/h-video (objetivo ≤120); NO es el tiempo end-to-end |

## Archivos

- `documentation.md` — síntesis del capítulo por conceptos, construida SOLO sobre claims SUPPORTED, todo citado.
- `claims.jsonl` — 98 claims con veredicto, evidencia y notas (schema abajo).
- `transcript.md` — transcript completo ordenado y citable (ids `s-<HHMMSS>`).
- `rules.md`, `concepts.md`, `examples.md` — vistas operativas del mismo conocimiento.
- `repair/` — manifiesto baseline pre-reparación y registro de la remediación P1–P10 (2026-10-18).
- `review-notes.md` — incertidumbres, adjudicaciones, garbles ASR, visual no resuelto.
- `study-guide.md` — guía de estudio con preguntas y respuestas con evidencia.
- `frames/` — `f-<HHMMSS>.png`; los 18 frames base son fin de minuto (`f-00MM59.png`, y `f-001703.png` al final parcial); el resto son bajo demanda citados desde claims y documentos.

## Schema de claims (y extensiones documentadas)

Contrato base del mandato: `id`, `minute`, `kind`, `statement`, `evidence`, `verdict`, `notes`.

Extensiones usadas en esta biblioteca (declaran lo que el mandato exige distinguir):

- `epistemic`: `instructor_statement` (afirma el instructor) · `visual_observation` (muestra el gráfico) · `model_inference` (interpretación del modelo; 0 casos vigentes — c-0066 fue reclasificada a instructor_statement en la remediación P4).
- `visual_hint`: `{second, what}` cuando el claim depende de algo visual concreto.
- `source_key`: key original del bloque de extracción (A-/B-/C-), para trazabilidad.

Kinds usados: `concept`, `rule`, `parameter`, `procedure`, `observation`, `example`, `warning` (extensión sobre la terna de la skill, documentada).

## Limitaciones

- El ASR garblea términos del glosario ("tartle sub"=Turtle Soup, "el dol"=el DXY, "Pablo III"=Power of 3); los claims lo preservan y anotan (`notes: "ASR: ..."`).
- La enumeración de aperturas de la vela de 4h que da el instructor en 02:22 omite la de la 1 p.m.; el claim c-0011 conserva la enumeración literal, la pirámide SÍ incluye la vela de la 1 (f-000240) y el instructor usa esa vela después (c-0060, c-0096). Ver `review-notes.md`.
- Los frames viven en este repositorio (17 MB, 65 archivos); el video original NO está en Git: su ubicación física es `/home/kor/mke/course/ep02-time.mp4` y su SHA queda arriba para verificar identidad.
- Para corregir/ampliar un punto: operar SIEMPRE sobre los recursos citados (transcript + frames), nunca re-procesando el video (contrato de la skill).

## Método (resumen)

1. ASR faster-whisper ligado al SHA → `transcript.md` con ids `s-<HHMMSS>`.
2. 18 frames base (fin de cada minuto) con ffmpeg.
3. Extracción de claims en 3 bloques paralelos (5–10 min) con subagentes ONE-SHOT.
4. Checkpoint de rendimiento a los 5 primeros minutos → PASS.
5. Revisión POR MINUTO (18 llamadas ONE-SHOT, nunca por claim): cada revisor valida fidelidad, visual, causalidad, deícticos y duplicados de todos los claims de su minuto, y extrae frames bajo demanda.
6. Integración determinista: IDs finales `c-NNNN`, adjudicación documentada de las 4 dudas de frontera, publicación.
