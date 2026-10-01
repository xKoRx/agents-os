# WINDOWS — 4 ventanas solapadas (diseño fijado antes del live)

## Derivación (sin cherry-picking, previa a toda inferencia)

- Región base: la ventana canónica **`w0002` del gate 10W (9–36 s, 8 frames)** —región material previamente aceptada con 22 claims— extendida hacia adelante hasta 48 s usando sólo frames ya existentes en el manifest del L0.
- Los límites reales salen del PTS físico de los frames (time base 1/90000): cada ventana cita 8 frames existentes; el intervalo efectivo es [PTS mínimo, PTS máximo] de sus frames, y el pipeline deriva el transcript por solape con ese span (`windowSegments`).
- Solape objetivo 70–85% entre consecutivas: logrado 74.1–83.3%.
- Selección cerrada antes del lanzamiento del live; el config `configs/config.v2.stress4.json` se escribió y congeló antes de la primera llamada. Sin tocar el prompt de reconstruction; sin hardcodear IDs.

| Window | Interval (PTS, time base 1/90000) | Frames (PTS s) | Overlap con previa | Transcript (derivado) | Status | Claims prop. | Rel. prop. | Identity collisions | Equiv. reviews live | Resultado | Contribución canónica |
|---|---|---|---|---|---|---|---|---|---|---|---|
| w0002-o1 | 810000 – 3240000 (9–36 s) | 9,12,16,20,24,28,32,36 | — (base = w0002 canónica) | asr-00001, asr-00002, asr-00003 | ACCEPTED | 28 | 0 | 0 | 0 | commiteada | 28 claims (first observation) |
| w0002-o2 | 1440000 – 3600000 (16–40 s) | 16,20,24,28,32,36,38,40 | 20 s = 74.1%/83.3% | asr-00001, asr-00002, asr-00003 | REJECTED | 32 | 2 | 1 determinista (+1 duplicado exacto decidido) | 0 | rechazada por el ladder | 0 (atomicidad whole-window) |
| w0002-o3 | 1800000 – 3960000 (20–44 s) | 20,24,28,32,36,40,42,44 | 20 s = 83.3% | asr-00002, asr-00003 | ACCEPTED | 19 | 1 | 0 | 0 | commiteada | 19 claims + 1 relation (todos slugs nuevos) |
| w0002-o4 | 2160000 – 4320000 (24–48 s) | 24,28,32,36,40,42,44,48 | 20 s = 83.3% | asr-00002, asr-00003 | REJECTED | 23 | 1 | 3 semánticas (+1 no decidida por aborto del DECIDE) | 3 | rechazada por el ladder | 0 (atomicidad whole-window) |

## Detalle de rechazos (razones durables, byte-idénticas en replay)

- **w0002-o2** — divergencia determinista, sin adjudicación: `record cl-grafica-temporalidad-cinco-minutos@1 identity collision: kind differs (parameter vs observation) (window w0002-o1, then window w0002-o2); deterministic divergence, window rejected closed without an equivalence review`. Además decidió 1 duplicado exacto idempotente (`cl-curso-intermedio-sienta-base`) antes de abortar. Es la clase del incidente original (mismo hecho re-propuesto con atributo semántico distinto): rechaza la ventana, el run sigue.
- **w0002-o4** — 3 colisiones semánticas adjudicadas live en orden de id (`cl-curso-intermedio-no-supone-problema` EQUIVALENT, `cl-eurusd-subida-previa` EQUIVALENT, `cl-formato-similar-curso-intermedio` **DIVERGENT**) → ventana rechazada closed por la tercera; las 2 acumulaciones EQUIVALENT decididas no se aplicaron (el APPLY sólo corre en ventana aceptada). `cl-grafica-instrumento-eurusd` y `cl-grafica-temporalidad-cinco-minutos` (también re-prouestos) quedaron sin decidir por el aborto del DECIDE.

## Métricas de evidencia por ventana

```text
reconstruction_windows_total = 4
reconstruction_valid = 4  (todas pasaron ValidateProposal; 0 refs de evidencia inventadas)
reconstruction_rejected_bad_evidence_ref = 0
other_reconstruction_rejections = 2  (ambas por identity ladder en commit, no por output inválido)
```

Lista de evidence refs inválidas: **vacía** — el defecto del gate 10W (refs tipo `asr-00001 [5810-19820]`) no se reprodujo; las 4 propuestas citaron sólo IDs exactos existentes (90/90 dependency edges del run resuelven contra manifest + transcript + records).

Nota: el modelo volvió a elegir slugs mayoritariamente nuevos por ventana (o3: 20/20 nuevos pese a 83% de solape) — el espacio de slugs es abierto y eso explica los 0 colisiones del gate 10W; bajo el mismo solape, esta corrida sí produjo 4 re-usos reales de id, que es justo lo que este gate quería ejercitar.
