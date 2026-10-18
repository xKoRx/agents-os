# METHODOLOGY-FEEDBACK — Clutifx Chapter 02 (2026-10-18)

Feedback de la primera ejecución completa de la skill `course-knowledge-extraction`.
NO se modificó la skill canónica durante la ejecución (contrato del mandato): estas son las observaciones y propuestas para decidir mañana con el Owner.

## Números del run

| Métrica | Valor |
|---|---|
| Duración del video | 17:09 (17,2 min) |
| Tiempo real total de sesión | ~1 h 40 min (02:54–04:35) |
| — ASR (faster-whisper large-v3, int8 CPU) | **45,1 min** (0,38× realtime) — cuello de botella dominante |
| — Setup (identificación, SHA, frames base, payloads) | ~8 min |
| — Extracción (3 subagentes paralelos) | 8,6 min |
| — Revisión (18 subagentes, olas de 5/7/6) | 19,8 min |
| — Integración + publicación biblioteca | ~15 min (manual del orquestador) |
| Inferencias/subagentes | 3 extracción + 18 revisión = 21 ONE-SHOT |
| Claims | 98 total (~5,7/min de video); 4–9 claims/minuto |
| Veredictos | inicial 94 SUPPORTED / 4 UNCERTAIN → final 98/0/0 tras 4 adjudicaciones documentadas |
| Contradicciones marcadas por revisión | 0 |
| Frames | 18 base + 44 bajo demanda (~2,6/min, sobre el presupuesto ~1/min) |
| Minutos de alta complejidad visual | 5–9 (recorrido de gráfico casi continuo) y 13–16 (esquemas dibujados) |
| Checkpoint 5 min | PASS: proyección pipeline ≈ 99 min/h-video (objetivo ≤120) |
| Throughput total incl. ASR | ~5,8 h/h-video — FUERA de objetivo si el ASR cuenta |

## Casos en que la revisión agrupada detectó errores

- 4 claims UNCERTAIN: todos por evidencia citada que caía en el minuto contiguo (payload de frontera). La revisión POR MINUTO hizo su trabajo (no aceptó silenciosamente); el coste fue 4 re-adjudicaciones baratas con recursos ya existentes.
- Nomenclatura de frames: 2 de 18 revisores nombraron frames con horas en vez de minutos (`f-044000`, `f-0048xx`) a pesar del ejemplo en el prompt. Detectado y corregido en integración.

## Errores que sobrevivieron

- Ninguno conocido tras la verificación de citas (script + revisión adversarial de `documentation.md` contra claims).
- 1 deíctico quedó honestamente sin resolver (rango descartado en 8h, c-0056) — visible en `review-notes.md`, no "resuelto" a la fuerza.

## Cuellos de botella (ordenado)

1. **ASR local (45 min)** — 47 % de la sesión. large-v3 int8 CPU con beam 5 es desproporcionado para el pipeline (el transcript es el 85-90 % del conocimiento).
2. **Publicación manual** (~15 min): escribir 8 documentos a mano. Es calidad, no desperdicio, pero es la segunda partida.
3. Revisión (19,8 min) > extracción (8,6 min): esperado; los revisores leen frames (imágenes = tokens).

## Partes del procedimiento que sobran

- Ninguna fase completa sobra. Ajustes finos:
  - El doble chequeo de cobertura que hice tras cada ola (validar keys de review vs payload) debería ser parte estándar de la integración, no un extra.
  - El frame base del último minuto parcial (`f-170903`) es casi idéntico al anterior; mantener por contrato, pero no es load-bearing.

## Partes que faltan (detectadas en este run)

1. **Payloads de frontera**: el payload de cada minuto debe incluir SIEMPRE los segmentos citados por sus claims, aunque pertenezcan al minuto contiguo (hubo 2 UNCERTAIN y 1 nota por esto). Regla propuesta: payload = segmentos del minuto ∪ segmentos citados por los claims del minuto.
2. **Contrato de naming para revisores**: dar la regla de naming como fórmula explícita (`f-00` + MM + SS, horas siempre `00`) o mejor, un mini-script `frame.sh MM:SS` que los revisores invoquen. 2/18 fallaron con ejemplo; con fórmula debería bajar a 0.
3. **Presupuesto de frames por tipo de minuto**: en capítulos de recorrido de gráfico, ~1 frame/min bajo demanda se queda corto; sugerencia: presupuesto por minuto declarado en el payload (base + tope on-demand) según densidad visual estimada del bloque.
4. **Glosario acumulado como entrada de extracción**: los 3 extractores tuvieron que adivinar garbles ("tartle sub") con la lista que les di en el prompt. Con la biblioteca creciendo, pasar `GLOSSARY.md` + tabla de garbles conocidos como input estándar asegura consistencia entre capítulos.
5. **Métricas automáticas de sesión**: los tiempos los reconstruí de mtimes; un `run-log.jsonl` (evento, timestamp) escrito por el orquestador eliminaría la reconstrucción.

## Propuestas concretas para Chapter 03 (ep03-bias, 182 MB)

1. **ASR**: medir en los primeros 2 min del video `large-v3 beam 1` (y opcionalmente `medium`) contra `large-v3 beam 5`; si el texto es equivalente, usar el rápido para el resto del curso. Ahorro potencial: ~30-40 min/video. (Decisión Owner: cambia ligeramente la herramienta de transcripción, no la metodología.)
2. **Aplicar los 5 fixes de "partes que faltan"** (payloads con segmentos citados, frame.sh, presupuesto visual, glosario como input, run-log).
3. **Publicación semi-generada**: generar de forma determinista el esqueleto de `rules.md`/`concepts.md` desde claims (campos ya estructurados) y reservar la escritura manual para `documentation.md` y `study-guide.md`.
4. **Mantener**: checkpoint a los 5 min, revisión por minuto en olas de 5-7, adjudicación documentada en el propio claim, verificación de citas por script + revisión adversarial.

## Datos para comparar con Chapter 01 (mismo curso)

| | ch01 (MKE V2 agent-VLM) | ch02 (skill, este run) |
|---|---|---|
| Video | 34 min | 17,2 min |
| Wall extracción+revisión | 44 h (abortada al 63 % de grounding) | 28,4 min (completa) |
| Claims | 1.527 (~45/min) | 98 (~5,7/min) |
| Revisión | 1 llamada/claim (1.200 ejecutadas) | 18 llamadas (1/minuto) |
| Coste frames | inspección densa por ventana | 61 frames |
| Resultado | PARTIAL (biblioteca con 3 archivos) | DONE (biblioteca completa) |

La comparación no es 1:1 (objetivos distintos: MKE V2 era certificación de motor; esto es extracción de conocimiento), pero el ratio costo/cobertura del mismo video fuente cae ~2 órdenes de magnitud.
