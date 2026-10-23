---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo Futures]]"
aliases:
  - clutifx experiment matrix
  - matriz experimental clutifx
tags:
  - kind/doc
  - area/echo
  - tech/strategy-research
created: "2026-10-23"
updated: "2026-10-23"
---

# CLUTIFX-EXPERIMENT-MATRIX — Variantes materiales y plan experimental

FASE E de la misión GOD. Diseña el espacio experimental para el backtester de Echo Futures (futuro encargo; aquí NO se ejecuta nada). Identidad estable por variante, ejecutable por lotes, comparación independiente. **Sin producto cartesiano ciego**: cada variante existe porque cambia UNA decisión material o explora UNA hipótesis de interacción.

## 0. Reglas de diseño

1. TIER 1 (controles): una versión simple, objetiva y reproducible por familia — la operacionalización más literal del SOURCE.
2. TIER 2 (ortogonales): sustituir UN detector o UNA decisión por vez, manteniendo el resto constante, para medir su impacto causal.
3. TIER 3 (combinaciones): sólo combinaciones con hipótesis de interacción explícita.
4. Equivalencia observable: si dos variantes producen señales idénticas o casi (correlación de activaciones > 0.9 en el dataset de control, o equivalencia semántica demostrable), se documenta la relación y NO se duplican en nuevos runs (los IDs se mantienen para trazabilidad).
5. Nada de este documento pre-selecciona ganadores ni optimiza parámetros. La selección del conjunto a ejecutar es del Owner (`EXPERIMENT_MATRIX_OWNER_APPROVAL = PENDING`).
6. Convención de IDs: `CLF-VAR-###` con prefijo de estrategia (`S1-`, `S2-`, …) y sufijo de eje (`-D#` decisión, `-P#` parámetro). Los grid de parámetros se declaran como RANGOS, no como variantes individuales.

## 1. Ejes de variación por estrategia (dimensiones materiales)

| Estrategia | Eje D1 contexto | Eje D2 trigger | Eje D3 sesión | Eje D4 salida | Ejes de parámetro (grid) |
|---|---|---|---|---|---|
| STR-001 London ideal | bias: cadena nativa vs [HIP] A/B/C | TS: R1/R2/R3/R4 (§2 detectores) | ancla vela 1 (NY) vs ancla CME propuesta | DOL/vela-5 | ε-rango {0,1t,0.05A}; ρ-reacción {.38,.5,.618}; ventana reacción w {1,3,5} |
| STR-002 Pendiente | TF objetivo {4h, 1D} | creación del pendiente (NATIVO) | sesión libre | DOL/vela-5 | ε-rango; TF del pendiente {1h, 4h} |
| STR-003 NY continuación | secuencia 1-5-9 (NATIVO) | TS de la vela previa + rangos | ancla 9:00 NY vs 9:30 ET | DOL/vela-5 | δ-ventana P3 {25%,33%,50%} |
| STR-004 NY reversal | objetivo completado (NATIVO) | vela-5 toma low + rango nuevo | ancla vela 5 | extremos 6–8h | δ; confirmación reacción R1/R2 |
| STR-005 Refinado | hereda padre | hereda padre | libre | hereda | escala de TFs {8h→4h→1h→15m; 4h→1h→30m→15m; sin refinado} |
| STR-006 Failure swing | tendencia hacia extremo (NATIVO) | rango de reacción (NATIVO) | libre | rango activado como target | ε-nivel {2t, .25A, .5A}; fracción final {15%, 25%} |
| STR-007 SMT | régimen contra-tendencia (NATIVO) | casos 1/3 | libre | negación c-0076 | τ-sincronía {1,3 velas} — BLOQUEADO hasta 2º instrumento |
| STR-008 Noticias | dolls intactos + TS previo | P3 de la vela de noticia | hora de la noticia | BE al llegar | calendario {rojo, rojo+naranja} — requiere feed |
| STR-009 Reentrada | bias correcto + rango | cierre dentro tras stop | libre | plan original | máx reentradas {1, 2} `[PENDIENTE: límite no enseñado]` |

## 2. TIER 1 — Controles (una por familia; ~8 variantes)

| ID | Estrategia | Descripción (operacionalización más literal) |
|---|---|---|
| CLF-VAR-S1-T1 | STR-001 | Cadena de rangos nativa (12h–4h) + DOL nativo + TS con reacción R2 (cierre) + entrada al cierre del rango a favor en la ventana P3 de la vela 1 + stop bajo TS + salida DOL o vela 5 |
| CLF-VAR-S2-T1 | STR-002 | Pendiente 4h hacia DOL 4h/1D + entrada al cierre del pendiente + stop bajo el pendiente |
| CLF-VAR-S3-T1 | STR-003 | TS de la vela previa (R2) + rangos a favor + entrada en ventana P3 de la 9 anclada 9:00 NY |
| CLF-VAR-S4-T1 | STR-004 | Objetivo completado en London + vela 5 toma low + rango alcista + entrada al cierre |
| CLF-VAR-S5-T1 | STR-005 | S1-T1 con refinado 4h→1h→15m (misma lógica, TF inferior) |
| CLF-VAR-S6-T1 | STR-006 | FS: ε=0.25·A + fracción final 25% + rango de reacción al cierre |
| CLF-VAR-S8-T1 | STR-008 | Día de noticia roja con dolls intactos + TS previo + entrada P3 vela noticia (post-feed de calendario) |
| CLF-VAR-S9-T1 | STR-009 | Regla de reentrada sola sobre S1-T1 (máx 1) |

STR-007 sin TIER 1 (bloqueado por datos). Cada TIER 1 declara: identidades de rango/DOL/TS deterministas, estado mínimo (detectores §16) y arneses de test F1 (ver §5).

## 3. TIER 2 — Sustituciones ortogonales (una decisión por vez; ~22 variantes)

| ID | Base | Sustitución única | Hipótesis que mide |
|---|---|---|---|
| S1-D2a..c | S1-T1 | reacción TS: R1 (ρ=0.5) / R3 (m=15,k=1) / R4 (fractal n=2) | qué formalización de "reacción" reproduce mejor la ocurrencia enseñada |
| S1-D1a..c | S1-T1 | bias: [HIP] familia A (EMA50) / B (HH-HL) / C (DMI+ADX) | estructura nativa vs indicadores (NO atribuido a Clutifx) |
| S1-D3a | S1-T1 | ancla de sesión: CME-native (grid Chicago) vs NY-anchored | efecto del anclaje horario |
| S1-D4a | S1-T1 | salida sólo-DOL vs sólo-vela-5 | contribución de cada salida |
| S2-P1a,b | S2-T1 | TF del objetivo 4h→1D; TF del pendiente 4h→1h | escala del fenómeno |
| S3-D3a | S3-T1 | ancla 9:30 ET (open cash) | fidelidad NQ del ancla FX |
| S4-D2a | S4-T1 | reacción R1 en vez de cierre | sensibilidad del trigger de reversal |
| S5-P1a,b | S5-T1 | escala 4h→1h→30m→15m; sin refinado (padre directo) | valor del refinado |
| S6-P1a,b | S6-T1 | ε 2 ticks; ε 0.5·A; fracción 15% | tolerancia del "prácticamente al nivel" |
| S1-D5a | S1-T1 | ε-rango 1 tick (borde ch07 c-0065) vs 0 | efecto del borde |
| S1-D6a | S1-T1 | TS exige reacción intrabar 1m (R1 intrabar) vs cierre | coste/beneficio de no esperar cierre (ch04 c-0027) |
| S9-P1a | S9-T1 | máx 2 reentradas | límite no enseñado |
| Flags-a | cualquier T1 | red flags OFF (baseline sin filtros) | contribución agregada de los filtros ch09 |
| Flags-b | cualquier T1 | sólo red flags duras (en-contra + inside) | valor de las probabilísticas |

## 4. TIER 3 — Combinaciones con hipótesis de interacción (sólo 5)

| ID | Combinación | Hipótesis de interacción |
|---|---|---|
| S1-C1 | ancla CME × refinado 15m | el refinado puede compensar un ancla de sesión desplazada |
| S1-C2 | reacción R1 intrabar × stop ε-amplio | la entrada temprana necesita stop más ancho (ch04 c-0027/c-0051) |
| S4-C1 | reversal × filtro "objetivo mayor sostiene" (ch09 c-0136) | la reversión post-objetivo sólo sobrevive con el objetivo HTF intacto |
| S6-C1 | FS × ventana horaria clave {3,5,9} | el FS "final de vela" concentra en cierres de velas clave (ch06 c-0010) |
| S8-C1 | noticia × TS-previo-obligatorio | sin TS previo el whipsaw destruye la entrada (ch10 c-0062) |

## 5. Equivalencias y no-duplicación

- R2 (cierre) ⊆ detector de rango §1: cualquier variante con R2 activa implícitamente el detector NATIVO ⇒ S1-D2* comparan contra la propia base ya contenida; documentado, no duplicado.
- E1/E2 (expansión): antes de crear variantes de salida por "reacción contraria", medir correlación de activaciones; si > 0.9 colapsar.
- NATIVE vs SG del universo 89 (Hefesto): el eje MM/presupuesto (R250/500/750) YA fue explorado en campaign-lab R02 para las estrategias TG/FBC/ORB/MR — las Clutifx reutilizan ese patrón de perfiles (`PROFILE-ATR14-WILDER-M1-X1-GROSS{R}-1TO1`) sin re-definirlo aquí; el eje MM queda desacoplado por contrato (frontera Strategy/MM).
- Alias conocidos del corpus: ORB-NATIVE-Cxx ≡ ORB-CH300 (documentado en HEFESTO-BASELINE-AUDIT.md) — patrón a imitar: identidades de señal idéntica = 1 voto por familia.

## 6. Plan de validación por variante (FASE F resumida; detalle en spec de implementación futura)

1. **Correctness primero** (gates F1, obligatorios antes de cualquier evaluación económica): no-lookahead (replay de señales con información retrasada人工 imposible), causalidad intrabar, determinismo bit-exacto (replay), warmup, multi-TF (composición 1m→TFs), orden de eventos, LONG/SHORT, stop/invalidación, fills+costos ($2.49/lado + 1 tick), sesiones/DST, rollover (12 contratos físicos, roll events ya soportados por el motor), datos faltantes (exclusiones manifest), interacción Strategy/MM, reentradas/señales simultáneas (regla de prioridad invalidación→sesión→timeout→target del motor MR ya existente es reutilizable).
2. **Estadístico**: baseline de desarrollo = primeros 60% días elegibles (2023-10→2025-04 aprox.); OOS 20% (2025-04→2025-12); walk-forward 20% final (2026). Congelar períodos ANTES de inspeccionar resultados. Comparación por régimen (por año/contrato/vol quintil); robustez a costos ×0.5/×1/×2; sensibilidad de cada parámetro del grid (curva unidimensional, no optimización); estabilidad temporal (T1/T2/T3 del patrón R02); penalización por múltiples pruebas (Wilson/effective-N como mínimo, declarando dependencia entre variantes del mismo mercado-período); benchmark contra controles simples existentes (las 21 familias TG/FBC/ORB/MR ya medidas).
3. **Métricas a emitir** (el motor ya emite la mayoría): señales, trades, frecuencia/día elegible, expectancy neta, win-rate, profit factor, payoff, distribución R, MAE/MFE (con 1m), DD máx, retorno neto, tiempo en mercado, exposición, resultados por sesión/régimen/contrato, sensibilidad a costos, estabilidad OOS — más la separación challenge (E2T GAU50, 3 fases) vs calidad estadística de la señal: **una campaña que pasa challenges no es una estrategia robusta** (lección formalizada en R02: RESEARCH_ACCEPTANCE ≠ LIVE_ENABLED).
4. **Protector de honestidad**: variante del mismo mercado/período ≠ muestras independientes; prohibido reportar "N estrategias positivas" como evidencia conjunta; todo reporte declara el universo probado.

## 7. Bloqueos y dependencias

| Variante | Bloqueo | Desbloqueo |
|---|---|---|
| S7-* (SMT) | sin 2º instrumento en corpus | incorporar ES/YM 1m al corpus (decisión Owner) |
| S8-* (noticias) | sin feed de calendario económico en el runtime | conector de calendario (gap declarado en D1) |
| Todas: fidelidad intrabar fina | sin ticks | corpus de ticks (pendiente físico) |
| 23 filas R02 en cuarentena (17 SG FBC/ORB + 3 SG-TG + 3 SG-MR) | ciclo R03 ajeno en curso | re-ejecución del ciclo correctivo (Owner/otra sesión) |

## 8. Gate E

```text
VARIANTES_MATERIALES_IDENTIFICADAS = 8 TIER1 + 21 TIER2 etiquetadas + 5 TIER3 (34 IDs; la fila S6-P1a,b empaqueta 3 sustituciones ⇒ 35 sustituciones efectivas; grids declarados como rangos)
REDUNDANCIA_ELIMINADA = equivalencias R2⊆rango, E1≈E2 (pendiente medición), eje MM desacoplado, patrón alias documentado
SELECCION_DEL_CONJUNTO = PENDING (Owner)
```
