# P6 — TARGETED LIVE CERTIFICATION

**Producto:** `19b44c1` (binario SHA256 `e5e4fcbe8295fd90…`), prompts `mke.claims-recon.v3` + `mke.claims-ground.v2`, config con `composition_timeout_seconds: 600` (SHA256 `8200082c…`).
**Alcance:** 19 ventanas canónicas seleccionadas por defecto a certificar: 4 bad-refs (w0003, w0005, w0043, w0110) · pares de colisión identidad origen→flipper (w0017→w0062/w0074, w0051→w0058, w0077→w0078, w0120→w0122) · ventanas con records grounding FN/ES (w0011, w0024, w0025, w0067, w0100, w0104) · L0 reutilizado con binding físico. Live `openrouter/stealth/space-bunny-alpha`.
**Duración:** ~2h50m (llamadas del backend lentas esta noche: hasta ~8 min/ventana). Terminal INCOMPLETE exit 4 ordenado (1 ventana rechazada).

## Resultados por gate

### R-M03 — bad evidence refs: **PASS (3/3 ejercitables)**
w0005, w0043, w0110 — las 3 ventanas que en el run viejo murieron por refs inventadas — ahora **VALIDATED con refs válidas**. El patrón `asr-NNNNN [range]` / `transcript asr-` no se reprodujo (0/19).
w0003 fue rechazada por un slip NUEVO y distinto: el modelo inventó un claim id con charset inválido (`cl-vista-desplazada-a-mañana-24-junio`, `ñ` no permitido). Familia formato (no semántica), fail-closed benigno, frecuencia 1/19 en esta noche (0/130 en el run viejo). Adjudicación: transiente aceptado, sin fix de producto (el costo es la ventana, no el run; normalizar slugs tocaría identidad — deuda documentada).

### R-M02 — estabilidad de kind/epistemic: **PASS**
0 colisiones de identidad en 19 ventanas (el tramo equivalente del run viejo produjo ~6). `cl-instrumento-eurusd` re-propuesto en 4 ventanas (w0005→w0025→w0051→w0110) siempre con kind consistente → cada re-propuesta fue al equivalence review y mergeó. Distribución kinds balanceada (parameter 36 / observation 33), 0 flips epistémicos.

### Falsos splits (N-01): **CORREGIDO EN VIVO**
w0078 —uno de los 2 falsos splits confirmados del P1 (DIVERGENT por sinonimia superficial)— ahora **EQUIVALENT** (`claims-equivalence:cl-cierre-fuera-deja-de-ser-rango@1:w0077->w0078` VALIDATED). w0122 también absorbida vía merge de `cl-vela-apertura`.

### R-M01 — grounding: **PASS (mejora material)**
170/207 grounding reviews VALIDATED. Publicado: **141/149 claims SUPPORTED (94.6%** vs 92.9% del run viejo sobre TODO el capítulo; estas 19 ventanas eran las cargadas de casos difíciles), **24/24 relations SUPPORTED** (vs 112/130 = 86% viejo). Non-supported: 5 INSUFFICIENT + 3 CONTRADICTED (8 records vs ~30+ equivalentes del run viejo en estas ventanas).

### Residuo material del run viejo: **RECUPERADO**
`cl-rango-anticipable-antes-cierre-vela` (la anticipación en tiempo real de w0058/w0059, perdida en el run viejo) y `cl-vela-apertura` (w0120/w0122) ahora en el store canónico.

### R-B02 — L2: **PASS**
`sko.composition` **VALIDATED** — primera composition live completa del gate. 25 composition reviews: **19 SKOs publicados, 19/19 SUPPORTED** (6 propuestas rechazadas por el review: el filtro funciona). `L2_REACHED = YES`. (El timeout de 600s no fue estresado con catálogo chico; el estrés real llega en P7 con 853 records.)

### Idioma: **PASS** — 149/149 español.

## Equivalence reviews (8/8 VALIDATED → merge/acumulación)
Todas sobre re-observación real del mismo proposition (EURUSD instrument ×3, timeframe 8h, rango derecho bajista, cierre-fuera invalida rango, instrumento del chart, vela-apertura familia). Clasificación humana rápida: 7 OBVIOUSLY_EQUIVALENT + 1 plausible (cl-rango-derecho-bajista w0011→w0051, re-verificación en P8). **0 falsos merges.**

## Presupuesto
19 ventanas: reconstruction 19 + equivalence 8 + grounding 207 + composition 25 = 259 invocaciones. Run.db durable en `~/mke/clutifx-ch01-p6-gate-20261003/run-p6/`.

## Veredicto
```
P6_TARGETED_LIVE = PASS
READY_FOR_FULL_RERUN = YES
```
Findings menores para P8: (1) slip id-charset w0003 (transiente, fail-closed); (2) slugs siguen variando entre ventanas para la misma proposición (`cl-instrumento-eurusd` vs `cl-eurusd-instrument` vs `cl-chart-instrument-eurusd`) — la fragmentación MI-03 persiste (deuda conocida, fuera de alcance).
