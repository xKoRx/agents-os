---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo Futures]]"
aliases:
  - clutifx objective detectors
  - detectores objetivos clutifx
tags:
  - kind/doc
  - area/echo
  - tech/strategy-research
created: "2026-10-23"
updated: "2026-10-23"
---

# CLUTIFX-OBJECTIVE-DETECTORS — Biblioteca de detectores matemáticos candidatos

FASE C de la misión GOD. Objetivo: **ninguna condición material del catálogo queda sin traducción computable o sin bloqueo explícito**. Cada detector declara: fórmula, inputs, timeframe, ventana/warmup, causalidad, riesgo de lookahead, parámetros experimentales y qué hipótesis contrasta realmente.

## 0. Metodología — tres niveles nunca mezclados

- **SOURCE**: lo que el instructor dijo/mostró (claim-id). Si el SOURCE ya es computable, el detector se llama `NATIVO` y las alternativas son refinamientos de tolerancia, no sustitutos.
- **OPERATIONALIZATION**: representación matemática del SOURCE con elecciones libres mínimas (tolerancias, ventanas) que el SOURCE no fijó. Se marca `[OP]`.
- **RESEARCH HYPOTHESIS**: alternativa propuesta por el agente NO atribuida al instructor (p.ej. usar EMA donde él dijo "movimiento alcista"). Se marca `[HIP]`. **Nada `[HIP]` puede presentarse como enseñanza Clutifx.**

Convención NQ: precios en ticks (1 tick = 0.25); `A` = ATR(14) Wilder de la TF indicada; barras 1m como fuente única (sin ticks en corpus — ver master §8); todas las horas ancladas a `America/New_York` IANA con DST (el "UTC-4" del curso es supuesto didáctico); barras compuestas (3h/4h/6h/8h/12h/1D+) construidas desde 1m con anclaje a la hora de apertura dicha (17/21/01/05/09/13 para 4h; etc.).

## 1. Rango formado (CLF-CMP-001) — detector NATIVO

- **SOURCE**: vela toma extremo de la vela anterior y cierra dentro (ch01 c-0005/c-0006/c-0009). Borde ch07 c-0065: cierre apenas fuera puede contar; ch02 c-0035: tras TS+reacción no se exige cierre; ch06 c-0028: FS activa sin toma.
- **Fórmula base** (por TF T, vela i): `rango_alcista(i) := L(i) ≤ L(i-1) ∧ H(i) < H(i-1) ∧ C(i) > L(i-1)` — i.e., la vela i toma (toca o perfora) el low anterior y cierra dentro del rango `[L(i-1), H(i-1)]`; espejo para bajista con el high. Dirección = extremo tomado.
- **Inputs**: OHLC de TF T. **Causalidad**: evaluada sólo al cierre de la vela i (o intrabar para la variante TS+reacción, §2). **Lookahead**: NINGUNO si se evalúa al cierre; la variante intrabar exige estado streaming.
- **Parámetros experimentales `[OP]`**: ε-tolerancia del "cierra dentro" (0 ticks estricto / 1 tick / ε=max(1 tick, 0.05·A_T) para el borde c-0065); "toma" = tocar (L ≤ L_prev) vs perforar (L < L_prev) vs cerrar bajo (C < L_prev) — tres lecturas materialmente distintas; flag `sin_cierre` para la variante TS+reacción.
- **Completitud** (ch01 c-0078): rango completado cuando `H(i..k)` y `L(i..k)` ambos alcanzaron los extremos del rango ⇒ se elimina. **Invalidación** (c-0076): cierre fuera del rango ⇒ eliminado (con la excepción ε).
- **Tests**: contra-ejemplos sintéticos (toma sin cierre, cierre sin toma, borde ε); idempotencia del estado de rangos activos; recomputo desde cero vs incremental idéntico.

## 2. Reacción del Turtle Soup (CLF-CMP-005) — la parte discrecional del TS

- **SOURCE**: TS = toma del extremo + reacción hacia el lado contrario (ch01 c-0059/c-0063); "si sigue bajando, no es TS". La "reacción" NO está definida operativamente por el instructor ⇒ aquí vive la discrecionalidad a objetivizar.
- **Detectores candidatos de "reacción"** (todos `[OP]/[HIP]`):
  - **R1 [OP] — Retracement de la mecha**: tras tocar el extremo E en la vela i (1m o TF T), el precio retrocede ≥ ρ·(mecha desde E) dentro de la vela o de las siguientes w velas; ρ ∈ {0.38, 0.5, 0.618} como grid experimental, w ∈ {1, 3, 5} velas de la TF.
  - **R2 [OP] — Cierre direccional**: la vela que toma E cierra en la mitad superior (para toma de low) del propio rango previo; equivale a "cierra dentro" del detector §1 sin exigirlo por separado.
  - **R3 [HIP] — Momentum corto**: el retorno acumulado de las siguientes m minutos 1m (m ∈ {5, 15}) tras el toque es > 0 (low) / < 0 (high) y supera k·σ_m (k ∈ {0.5, 1.0}) con σ de ventana rodante 20 días.
  - **R4 [HIP] — Estructura de swing**: se forma un pivot confirmado (fractal de orden n ∈ {2,3}) en dirección contraria dentro de w velas.
- **Causalidad**: R1/R3 evaluables intrabar con 1m; R2 exige cierre de vela (la versión "no esperar cierre" ch04 c-0027 es intrabar por diseño ⇒ en backtest 1m, "intrabar" = resolución 1m, declarado como cota de fidelidad).
- **Lookahead**: NINGUNO si la ventana w sólo usa velas posteriores al toque, ya cerradas al momento de decisión.
- **Hipótesis que contrasta cada uno**: si la "reacción" del instructor es (retracement) vs (cierre) vs (momentum) vs (estructura) — las señales resultantes difieren en timing y en falsos positivos; el experimento mide cuál reproduce mejor la OCURRENCIA enseñada (no la rentabilidad).

## 3. Bias / "movimiento alcista-bajista" (pipeline ch03/ch08) — NATIVO por conteo + alternativas

- **SOURCE**: el bias se obtiene por PROCEDIMIENTO: marcar rangos bajando TFs; "normalmente el bias lo dan 6h–3D" (ch03 c-0050); "construir una narrativa" (ch08 c-0069); HTF manda (ch02 c-0088). El instructor NO usa indicadores.
- **Detector NATIVO [OP en tolerancias] — Cadena de rangos**: para cada TF T ∈ {12h, 8h, 6h, 4h, 1D, 2D, 3D}: `bias(T) = sign(Σ rangos activos alcistas − rangos activos bajistas)` con la vela de la izquierda pesando más (ch03 c-0059: doble peso al rango más antiguo, `[OP]`). `bias_sesión = mayoría ponderada de bias(T)` con quórum q `[OP]` (p.ej. ≥ 60% del peso). TFs con rangos enfrentados ⇒ TF "sin narrativa" (ch08 c-0050), excluida del voto.
- **Alternativas `[HIP]` para "contexto alcista" cuando se quiera contrastar la cadena nativa**:
  - Familia A — medias: Close > EMA(n) ∧ EMA'(n) > 0 (n ∈ {20, 50}); EMA rápida > EMA lenta; separación EMA20−EMA50 normalizada por A.
  - Familia B — estructura: HH+HL confirmados en los últimos k swings (k ∈ {2,3}); ruptura del máximo previo conocido; pendiente OLS de closes de ventana w normalizada por A.
  - Familia C — fuerza direccional: +DI > −DI con ADX > umbral (ADX mide fuerza, NO dirección — condición compuesta obligatoria); momentum acumulado w velas / A.
- **Warmup**: cadena nativa necesita ~2 velas por TF (máx 1D→2 velas = 2 días + margen de rangos activos: warmup 5 días de 1m es suficiente para TFs ≤ 1D; para el "1 año desde cero" de ch08 el warmup formal es 1 año, pero el bias de sesión sólo consume 12h–3D ⇒ warmup 4 días).
- **Lookahead**: los pivotes/swings de las familias B usan confirmación retrospectiva — exigir que el swing esté confirmado por n velas cerradas antes del instante de decisión.
- **Parámetros experimentales**: conjunto de TFs votantes; pesos; quórum; tratamiento de TFs enfrentados (excluir vs voto 0).

## 4. DOL identificado (CLF-CMP-007) — NATIVO

- **SOURCE**: extremo del rango(s) de TF alta hacia el bias, vela de la izquierda predominando (ch03 c-0070); jerarquía mensual/semanal contexto · 3D-1D DOL medio plazo · 12h-4h DOL sesión (ch03 c-0206–c-0209). Objetivos tomados "ya no sirven" (ch03 c-0007).
- **Detector NATIVO**: `DOL_sesión = extremo aún no alcanzado del rango activo más antiguo (izquierda) en TFs {12h,8h,6h,4h} en dirección del bias`; `DOL_medio =` ídem en {1D,2D,3D}. "Intacto" = precio actual no lo ha alcanzado desde su formación (tracking por estado).
- **Alternativas `[HIP]`** para investigación: extremos de sesión previa (high/low del día anterior, weekly open anchors); niveles de liquidez algorítmicos (mayor concentración de volumen por tick del corpus — NO disponible sin datos L2/ticks: `DATA_BLOCKED`); swing highs/lows HTF confirmados.
- **Causalidad**: el rango dueño debe estar cerrado (o intrabar con reacción si aplica) antes de declarar el DOL. Sin lookahead si el extremo proviene de velas pasadas.

## 5. Expansión fuerte / displacement — `[OP]/[HIP]`

- **SOURCE**: "coger la expansión" (ch02 c-0080); P3 = apertura-manipulación-distribución-cierre (ch01 c-0116); displacement 5m "volando" como señal de BE (ch11 c-0041). "Fuerte" NO cuantificado por el instructor.
- **Detectores candidatos**:
  - **E1 [OP] — Rango realizado**: range(window w) / A(w) ≥ k (k ∈ {1.5, 2, 3}), w ∈ {1 vela de TF T, sesión}.
  - **E2 [OP] — Cuerpo dominante**: |C−O| / (H−L) ≥ 0.6 ∧ (H−L) ≥ k·A.
  - **E3 [HIP] — Velocidad**: retorno z-score de m minutos |r_m|/σ_m ≥ k en ≤ m minutos.
  - **E4 [HIP] — Ruptura con desplazamiento**: cierre fuera de un rango activo con cuerpo ≥ 0.6·(H−L) y extensión ≥ k ticks más allá del nivel.
- Uso en el sistema: confirmar que la vela operable "está expandiendo" (contexto de STR-003), y salida/BE por reacción contraria (§14).

## 6. Power of 3 / ventana de manipulación (CLF-CMP-010) — NATIVO temporal

- **SOURCE**: compras ideales en la etapa de manipulación de la vela (ch01 c-0121); esperar la apertura de la vela clave y entrar en su P3 (c-0122); ejemplos con horas literales.
- **Detector NATIVO**: ventana temporal `[apertura(T_clave), apertura + δ]` con T_clave ∈ {vela de la 1, de las 5, de las 9, vela de la noticia} (hora NY) y δ `[OP]` = primer 25/33/50% de la vela. La "manipulación" como zona de precio NO tiene detector nativo (el instructor la ve); proxy `[HIP]`: el extremo opuesto de la vela en formación se hace dentro de la ventana (extremo contrario al sentido final) — medible sólo al cierre ⇒ como condición de ENTRADA es parcialmente retrospectiva: implementable como "entrar cuando el precio está en contramovimiento dentro de la ventana" (precio actual en la mitad adversa del rango de la vela en formación `[OP]`), NO como saber dónde acabará la mecha.
- **Lookahead**: prohibido entrar "en la manipulación" usando el conocimiento de que esa vela terminó distribuyendo a favor — la versión causal entra cuando: (a) ventana activa, (b) bias y estructura a favor, (c) precio en retracement dentro de la vela (fracción del recorrido actual de la vela ≥ ρ).

## 7. Rangos a favor / en contra (CLF-CMP-003/004) — NATIVO

- `en_contra(dir) = ∃ rango activo de dirección contraria a dir en TFs de sesión {4h,1h} (o conjunto experimental)`; `a_favor(dir) = ∃ rango pendiente dir ∧ ¬en_contra(dir)`. Dura "hasta que reinicia o crea pendiente" (ch09 c-0011) ⇒ recomputo por estado de rangos, no por ventana fija. La definición de "activo" (no completado, no invalidado) hereda de §1.

## 8. Vela inside (CLF-CMP-016) — NATIVO trivial

`H(i) < H(i−1) ∧ L(i) > L(i−1)`. Pausa de entrada hasta que una vela tome alguno de los dos extremos (ch09 c-0084/c-0085). Evaluada al cierre; sin parámetros.

## 9. Objetivo tomado (CLF-CMP-017) — NATIVO trivial

`precio_max_desde_formación ≥ DOL` (para DOL alcista). Con el tracking del §4. Red flag de sesión: objetivo 1D/2D/1S ya tomado al inicio de la sesión del día (ch09 c-0053).

## 10. Failure swing (CLF-CMP-011) — NATIVO con parámetros

- **SOURCE**: falla del nuevo extremo + va al otro lado (ch06 c-0004); rango activado sin toma (c-0028); motivos (a) SMT (b) final de vela ("15% final" dicho en un ejemplo ch07 c-0202) (c) feeds.
- **Detector**: contexto = tendencia hacia extremo E esperado (rango activo apuntando a E). FS confirmado cuando la vela i: (1) hace máximo M con `E − M ≤ ε` (ε ∈ {2 ticks, 0.25·A, 0.5·A} `[OP]`) — "prácticamente al nivel" — o el máximo se produjo en la fracción final f (f ∈ {15%, 25%}) de la vela previa `[OP]`; (2) **reacciona creando rango en la dirección contraria** (detector §1 en la dirección opuesta); entonces el rango se marca ACTIVADO con E como objetivo. El motivo (a) requiere 2º instrumento (§11); el (c) es `DATA_BLOCKED` single-feed.
- **Causalidad**: la confirmación es la creación del rango de reacción (vela cerrada o TS+reacción intrabar). El "ε casi tocado" se evalúa con datos hasta el instante de decisión. **Anticipar el FS está PROHIBIDO por fuente** (ch06 c-0016): no emitir señal antes del rango de reacción.
- **Lookahead**: la fracción "final de vela" se computa sobre la vela previa YA cerrada ⇒ causal.

## 11. SMT / divergencia entre instrumentos (CLF-CMP-012/013/014) — bloqueado por datos hoy

- **SOURCE**: 3 casos (ch05 c-0069–c-0083); tolerancia temporal NO dicha (los extremos "se ven" alineados visualmente).
- **Detector (cuando existan 2 streams sincronizados)**: extremos E_A(t_A), E_B(t_B) de la misma TF con `|t_A − t_B| ≤ τ` (τ ∈ {1 vela, 3 velas, 15m} `[OP]`); caso 1 = rango formado en A en la vela del extremo y en B no (extremo de B no alcanzado en ±τ); caso 3 = pendiente en A, no en B. Negación (c-0076): si el objetivo sigue más allá ⇒ clasificar como pendiente, no SMT.
- **Estado**: `MULTI_INSTRUMENT_DATA_REQUIRED` (corpus NQ-only). Propuesta NQ↔ES queda como hipótesis de adaptación futura NO enseñada.

## 12. Order block (CLF-CMP-009) — NATIVO simple

- **SOURCE**: confirmación = cierre por fuera de la vela (ch04 c-0034); "última vela opuesta previa a desplazamiento" NO es definición del curso — el curso sólo exige el cierre fuera de la vela de referencia (la vela OB es la que el instructor señala como la de la reacción/cambio).
- **Detector NATIVO**: dada la vela candidata V (la del extremo/reacción en el rango), `OB_confirmado = cierre(i) > H(V)` (o < L(V)) para la primera vela i > V. Stop de la entrada OB-confirmada: bajo el TS / extremo relevante (ch04 c-0034: "stop loss por debajo del Turtle Soup").
- **`[HIP]` alternativa**: definición ICT-style (última vela contraria antes del impulso ≥ k·A) — etiquetada como NO Clutifx, disponible para contraste.

## 13. Consolidación / rango realizado estrecho — `[OP]` (para régimen)

`range_realizado(w)/A(w) ≤ k` (k ∈ {0.5, 0.8}) o ADX(14) < 20 `[HIP]` o ancho Bollinger(20,2)/precio en percentil bajo `[HIP]`. Uso: contexto de "tres momentos" (ch09 c-0062) y advertencia de pirámide en consolidación (ch11 c-0070).

## 14. Salida por reacción contraria / BE estructural (gestión)

- **SOURCE**: dos velas 15m fuertes en contra ⇒ salir (ch08 c-0066–c-0068 [probabilística]); BE en puntos de giro estructural (ch11 c-0013/c-0014); displacement 5m ⇒ BE (ch11 c-0041); minuto 59 precaución (ch02 c-0064).
- **Detectores**: "vela fuerte" = §5-E2 en 15m (cuerpo ≥ 0.6, tamaño ≥ k·A); dos seguidas dirección contraria al trade ⇒ señal de salida técnica (la Strategy la emite como invalidación técnica; el MM decide). BE estructural = al formarse rango en contra (§7) u objetivo tomado (§9) en TF ≥ X (X ∈ {15m, 1h} `[OP]`). Minuto 59 de {3,5,9}: predicado temporal trivial.

## 15. Equivalentes y no-duplicación (FASE E insumo)

- R2 (§2) ⊂ §1 (misma señal con la toma): si R2 activo, §1 activo por construcción ⇒ NO son detectores independientes; documentar solapamiento.
- E1 ≈ E2 correlacionados en señales (rango grande suele traer cuerpo grande): si la correlación de activaciones en el dataset de control > 0.9, colapsar a una familia (regla de equivalencia observable de `CLUTIFX-EXPERIMENT-MATRIX.md`).
- Familia A/B/C de bias: contrastan hipótesis DIFERENTES (media vs estructura vs fuerza) ⇒ mantener separadas en TIER 2.

## 16. Riesgos transversales declarados

1. **Resolución 1m**: toda condición "intrabar" del curso (reacción del TS, manipulación del P3, apurar 5m antes de noticia) se evalúa con granularidad 1m Last; sin ticks, los fills intrabar y el detalle de mechas son una COTA. Declarar en cada spec.
2. **Offset horario**: hora NY del curso anclada a IANA con DST; las velas 4h/8h del curso suponen hour-anchoring NY (17/01/05/09) que difiere del grid CME Chicago 17:00 CT en DST-edge days — el anclaje ES una decisión experimental del eje H (dos alternativas: NY-anchored literal vs CME-native grid).
3. **Warmup**: por TF compuesta T, ≥ 2·(periodo de indicador) + margen de rangos; estándar propuesto: 5 días para sesiones; 10 para 1D-3D votantes.
4. **Estado mínimo persistido por estrategia**: set de rangos activos por TF (id, extremos, dirección, dueño-izquierda, completitud), DOLs activos con intact-flags, TS recientes por TF, flags de sesión (inside, objetivo tomado, rangos en contra), posición del episodio actual.
