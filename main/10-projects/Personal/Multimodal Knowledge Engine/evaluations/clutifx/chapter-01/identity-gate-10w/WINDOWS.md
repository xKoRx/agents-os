# WINDOWS — 10 primeras ventanas canónicas consecutivas

Fuente: `configs/config.v2.10w.json` = primeras 10 ventanas del config de 130 de la corrida original (mismos `window_id` y `evidence_ids`), 8 frames por ventana, policy `m0-windows-baseline-v1`. Sin cherry-picking.

| Window | Interval (PTS µs) | Status | Claims prop. | Rel. prop. | Identity collisions | Equiv. reviews | Resultado | Razón de rechazo | Contribución canónica |
|---|---|---|---|---|---|---|---|---|---|
| w0001 | 0 – 720000 | REJECTED | 15 | 1 | 0 | 0 | rechazada | output inválido: `cl-bienvenida-curso-completo` cita evidence ref inexistente `asr-00001 [5810-19820]` | 0 (atomicidad whole-window) |
| w0002 | 810000 – 3240000 | ACCEPTED | 22 | 2 | 0 | 0 | commiteada | — | 22 claims + 2 relations |
| w0003 | 3330000 – 3960000 | REJECTED | 9 | 1 | 0 | 0 | rechazada | output inválido: `cl-ir-directamente-al-grano` cita evidence ref inexistente `asr-00003 [34850-49400]` | 0 (atomicidad whole-window) |
| w0004 | 4320000 – 5760000 | ACCEPTED | 10 | 3 | 0 | 0 | commiteada | — | 10 claims + 3 relations |
| w0005 | 5850000 – 6750000 | ACCEPTED | 7 | 1 | 0 | 0 | commiteada | — | 7 claims + 1 relation |
| w0006 | 6840000 – 8010000 | ACCEPTED | 5 | 2 | 0 | 0 | commiteada | — | 5 claims + 2 relations |
| w0007 | 8100000 – 9720000 | ACCEPTED | 7 | 3 | 0 | 0 | commiteada | — | 7 claims + 3 relations |
| w0008 | 9990000 – 10620000 | ACCEPTED | 6 | 0 | 0 | 0 | commiteada | — | 6 claims |
| w0009 | 10710000 – 11520000 | ACCEPTED | 2 | 0 | 0 | 0 | commiteada | — | 2 claims |
| w0010 | 11880000 – 13320000 | ACCEPTED | 5 | 0 | 0 | 0 | commiteada | — | 5 claims |

Totales: 8 aceptadas / 2 rechazadas / 0 unavailable; 64 claims + 11 relations propuestas por las ventanas validadas = 64 + 11 commiteadas (0 duplicados, 0 acumulaciones, 0 colisiones).

Notas:

- Ninguna ventana fue rechazada por el identity ladder (0 colisiones de cualquier clase; 0 adjudicaciones semánticas). El incidente original (`cl-chart-instrument-eurusd` propuesto por w0002 y w0003 con contenido divergente) **no se reprodujo**: w0003 fue rechazada por citar evidencia inexistente antes de alcanzar el commit, y las renderings en español de esta corrida producen un espacio de slugs distinto al del run en inglés.
- Ambos rechazos son fail-closed contractuales sobre output del modelo (evidence refs inventadas con formato `asr-NNNNN [rango]`), no defectos de producto; el run continuó a la ventana siguiente en ambos casos.
- Tras la ventana 10 el run pasó a integrity → grounding → composition (no se ejecutaron w0011 ni el resto del capítulo).
