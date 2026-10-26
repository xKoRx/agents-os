# CLUTIFX-SOURCE-COVERAGE — Cobertura de fuente v1.0 (RECONSTRUIDO)

Proyecto: Echo Futures · Misión CLUTIFX GOD (2026-10-23) · Congelado en GATE P1

> **PROVENANCE:** Compilado desde la biblioteca MKE Clutifx (1.599 claims ACTIVE, 1.584 SUPPORTED, 15 UNCERTAIN, 9 superseded; 12/12 LIBRARY_VALIDATION PASS; READY_FOR_COMPILATION). Este documento consolida qué cubre la fuente, qué queda NOT_IN_SOURCE y cómo se resolvió cada hueco.

## Reglas de consumo

- Sólo ACTIVE + SUPPORTED. UNCERTAIN (15) = preguntas, nunca hechos. Superseded (9) navegan a su reemplazo.
- Dudas materiales heredadas: q-ch01-002 ("doble"→DOL/DXY) y análogas; q-ch03-004/q-ch04-002 (sigla PDM); q-ch09-002 ("breakable"→lectura BE no confirmada).
## C. Tabla capítulo→tema + UNCERTAIN/superseded

### C1. Capítulos
| ch | Tema | Aporta a |
|---|---|---|
| ch01 | Rango, pendiente/reiniciado, Turtle Soup (intra-TS), failure swing (base), order block, Power of 3, SMT (base) | STR-002, STR-006, STR-007, B1, B2, B5, B7, B14 |
| ch02 | Timeframes, horas clave, sesiones en velas 4h/6h, HTF manda, TS-sin-cierre | STR-003/004 (base), B4, B5, B12 |
| ch03 | Bias (6h–3D), jerarquía TF, DOL, vela de la izquierda, PDM, gestión BE/parciales | STR-002, B3, B4, B13, B14 |
| ch04 | Refinado 8h→4h→1h→15m, orden de entradas, order block, salidas (Entry Model), reentrada | STR-005, STR-009, B13, B14 |
| ch05 | SMT (3 casos), DXY −1, anticipación por rango | STR-007, B11 |
| ch06 | Failure swing (definición, 3 motivos, identificación) | STR-006, B8 |
| ch07 | Setups London (3 escenarios) y NY (continuación/reversal), checklist 4 preguntas | STR-001, STR-003, STR-004 |
| ch08 | Proceso top-down, gestión (BE, salida por precaución) | B4, B13 |
| ch09 | Red flags (4 + sesión), inside candle, secuencia 1-5-9 | B9, B10 |
| ch10 | Noticias (selección, horas, posicionamiento, whipsaw/blow) | STR-008, B11 |
| ch11 | Riesgo | (fuera de alcance A/B; sólo c-0068 UNCERTAIN listado) |
| ch12 | Psicotrading | (fuera de alcance A/B) |

### C2. UNCERTAIN activos (15 — NO consumibles como conocimiento; son preguntas)
- ch04: c-0038, c-0041, c-0042, c-0043, c-0057, c-0078, c-0102, c-0108 (gestión/entradas puntuales dudosas).
- ch05: c-0073 (garble del esquema del 2º caso SMT).
- ch09: c-0063 ("no expansión tras expansión" — q-ch09-010), c-0075 (zigzag TF 4h vs 2h — q-ch09-011).
- ch10: c-0032 (confirmación sube probabilidad), c-0069 (noticia "8:15"), c-0113 (rango en 6h "no hay nada").
- ch11: c-0068 (riesgo de la excepción).

### C3. Superseded (9 — navegar al reemplazo; no consumir el original)
- ch02: c-0066 → c-0099 (DOL en vela de las 5); c-0089 → c-0100 (HTF 8h).
- ch03: c-0089 → c-0212 (días de bias); c-0093 → c-0213 (PDM + reacción); c-0116 → c-0214 (rango contrario innecesario); c-0121 → c-0215 (noticia lleva al DOL); c-0122 → c-0216 (semana reinicia rangos); c-0123 → c-0217 (llegada no limpia).
- ch10: c-0030 (UNCERTAIN+superseded) → c-0200 (Excel de noticias).
- Nota: los 8 superseded de DXY (ch02/ch03) fueron remediation de término — el reemplazo ya dice DOL; en este documento sólo se citan los reemplazos.

### C4. Dependencias de duda material relevantes (OPEN-QUESTIONS)
- q-ch01-002 y análogas: garble "doble" → DOL vs DXY (afecta citas antiguas; los claims citados aquí ya están remediated).
- q-ch03-004 / q-ch04-002: expansión de la sigla PDM abierta.
- q-ch09-002: "mover tu tarjeta breakable" → lectura candidata break even NO confirmada (usar con cautela en B10.1).
- q-ch09-010 / q-ch09-011: ver C2-ch09.

## Consolidado NOT_IN_SOURCE y resolución de implementación

| Hueco | Dónde | Resolución [RECON] |
|---|---|---|
| Taxonomía reacción R1/R3/R4 | B6 | Sustituida por modos TS_CLOSE/TS_EARLY_1M/TS_M30/TS_WICK_NEXT (citados) |
| Tolerancia numérica "cierra dentro" | STR-002/B1 | `close_inside_tolerance_ticks` param tipado; base = 0 ticks (cierre estricto dentro); el matiz "apenas fuera parece dentro" (ch07 R13·c-0065) queda como variante documentada, no base |
| Umbral de "expansión" | STR-003 | Param `expansion_min_range_pct` del rango de referencia; base = sin umbral (cualquier toma de extremo cuenta como expansión estructural) |
| Stop del failure swing | STR-006 | Stop técnico en el extremo fallido ( espejo de stop-en-TS, ch01 c-0067); documentado como decisión |
| Contenido completo Entry Model | STR-005/B13 | Sólo la gestión 30m (ch04 c-0110) es implementable; el resto queda fuera |
| R por trade / sizing | todas | Fuera de Strategy: MM de investigación fijo (gerardmm) en evaluación A; GAU50 en evaluación B |
| Umbral divergencia SMT | STR-007 | DATA_BLOCKED de todas formas (sin segundo instrumento) |
| Lista canónica noticias operables | STR-008 | DATA_BLOCKED (sin calendario); valoraciones puntuales de la fuente NO son un feed |
| DST / UTC-4 | B12 | `America/New_York` IANA (DST-safe), decisión documentada |
| Nº máx rangos activos simultáneos | STR-002 | Sin límite en fuente; implementación mantiene todos, prioridad vela de la izquierda |
| Nº máx reentradas / mismo stop | STR-009 | Param `max_reentries` (base 1; variantes S18=0, S19=2); reentrada usa el MISMO esquema de stop del setup re-armado |
| Conflicto rangos contrarios (ch02 R9 vs ch03 R11) | B1 | Resolución: los rangos en contra ACTIVOS en el momento de decidir bloquean (ch03 R11·c-0094/c-0214); los completados no; el objetivo permanece y los contrarios pendientes ordenan el recorrido (ch02 R9) — ambas reglas conviven con alcances distintos (bloqueo vs ordenación) |
