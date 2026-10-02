# COVERAGE — mapa temporal del capítulo (00:00 → 34:04)

Cobertura por ventanas canónicas. Cada ventana aceptada introdujo ≥1 record canónico (verificado: la suma de records introducidos = 933 = todos los records canónicos). Índice recorrible por el Owner: **REVIEW-INDEX.md** (una fila por ventana con el topic de transcripción y los IDs). Datos máquina: `window-coverage.json`.

- Ventanas aceptadas: 104/130 (80.0%) — continuidad temporal con huecos sólo donde MKE rechazó la ventana.
- Ventanas rechazadas: 26/130 — cada una con razón durable (ver WINDOWS.md); 22 por identity ladder y 4 por evidence refs inventadas (w0003/w0005/w0043/w0110 — patrón `asr-NNNNN [range]` / `transcript asr-NNNNN`, el mismo defecto observado en el gate 10W; frecuencia real en full chapter: 4/130 = 3.1%). 0 ventanas con JSON malformado.
- Regiones nunca observadas: 0 (las 130 ventanas fueron intentadas).
- L2 (SKOs): 0 — composition_unavailable por transporte (`read-body retry-exhausted`), razón durable persistida; el capítulo queda documentado a nivel L1.

## Bloques temáticos del capítulo (para navegación del video)

| Time | Tema del video (transcripción) | Ventanas | Records MKE |
|---|---|---|---|
| 00:00–00:48 | Intro del curso, formato similar al curso intermedio, primer gráfico EURUSD | 3 (2 aceptadas) | 43 |
| 00:48–05:30 | Qué cubrirá el capítulo (bias, entradas, estrategia, riesgo, noticias) | 22 (21 aceptadas) | 149 |
| 05:30–12:00 | Gráfico EURUSD: temporalidades, rangos, cambio de intervalo | 26 (21 aceptadas) | 170 |
| 12:00–20:00 | Concepto de rango, formación de rangos, rangos pendientes/reiniciados | 27 (19 aceptadas) | 185 |
| 20:00–27:00 | SMT divergence, failure swings, EURUSD/GBPUSD correlacionados | 26 (21 aceptadas) | 203 |
| 27:00–34:04 | Turtle Soup, order blocks, proceso del trader, cierre | 26 (20 aceptadas) | 183 |
