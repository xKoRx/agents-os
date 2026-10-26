# CLUTIFX-EXPERIMENT-MATRIX — Catálogo experimental v1.0 (RECONSTRUIDO)

Proyecto: Echo Futures · Misión: CLUTIFX GOD (2026-10-23) · Estado: DRAFT → congelar en GATE P1

> **PROVENANCE:** El catálogo original referenciado por el mandato GOD (`clutifx-strategy-research/`) no existía físicamente en vault, Hefesto ni ningún branch del repo echo al iniciar la misión (hallazgo material P0, ver `HEFESTO-BASELINE-AUDIT.md`). Este documento es la **versión de implementación reconstruida**: estructura de tiers, familias de variantes y estrategias según el mandato §4/§6; semántica operacional según los claims SUPPORTED de la biblioteca MKE Clutifx (1.599 claims, 12/12 PASS). Toda decisión de desambiguación está marcada `[RECON]` con su justificación. Ningún resultado se presentará como réplica de un catálogo original.

## Identidad experimental

Cada corrida queda identificada por:

```text
variant_id · parameter_set_id · strategy_spec · strategy_config_hash
dataset_seal · execution_profile · source_commit · binary_sha256
```

- `dataset_seal` = `ba6f09853a0e923e41a40544e3aeca0a9eb28c41cbf645727818b5cb9ea6b6cd` (13× NQ .nt, P0).
- Cambio en código/detector/parámetros/datos/config ⇒ nueva identidad; no se mezclan identidades en un ranking.

## Conteo canónico

| Nivel | IDs | Sustituciones efectivas |
|---|---:|---:|
| TIER 1 — Controles | 8 | 8 |
| TIER 2 — Sustituciones | 21 | 22 |
| TIER 3 — Interacciones | 5 | 5 |
| **TOTAL** | **34** | **35** |

La nota de reconciliación del mandato ("34 IDs y 35 sustituciones") se materializa así: **`S05 BIAS-DMI-ADX` lleva 2 parameter sets** (ADX≥20, ADX≥25, ambos con dirección DMI) = 1 ID, 2 sustituciones efectivas. `[RECON]` El mandato citaba el par `S6-P1a,b` del catálogo inexistente; la forma (un ID con 2 sets) se preserva, el sujeto se reasigna a DMI-ADX por ser el eje con dos umbrales naturales documentados.

## Estrategias base y su implementabilidad

| ID | Estrategia | Estado inicial | Razón |
|---|---|---|---|
| STR-001 | London ideal (3 escenarios ch07) | ADAPTATION_REQUIRED | Sesión FX→NQ; anclajes horarios a congelar |
| STR-002 | Rango pendiente hacia DOL | IMPLEMENTABLE_NOW | Cadena de rangos nativa, corpus NQ 1m suficiente con warmup multitemporal |
| STR-003 | NY continuación | ADAPTATION_REQUIRED | Anclaje NY→CME NQ; ventana E2T 10:00 ET a registrar |
| STR-004 | NY reversal | ADAPTATION_REQUIRED | Ídem STR-003 |
| STR-005 | Refinado multi-TF | ADAPTATION_REQUIRED | Overlay sobre padre (STR-002); dependencia declarada |
| STR-006 | Failure swing | IMPLEMENTABLE_NOW | Detector autónomo ch06 |
| STR-007 | SMT | DATA_REQUIRED | Sin segundo instrumento (ES/YM/DXY) sincronizado; PROHIBIDO sustituto NQ |
| STR-008 | Noticias | DATA_REQUIRED | Sin feed de calendario económico con timestamp; PROHIBIDO inferir desde velas |
| STR-009 | Reentrada intra-TS | RUNTIME_REQUIRED | Contrato Strategy account-agnostic; versión técnica (rearme) documentada como NO-equivalente del stop físico |

## TIER 1 — Controles (8)

Configuración base por estrategia; los TIER 2 sustituyen exactamente UN eje contra estos controles.

| Variant ID | Estrategia padre | Configuración base [RECON salvo citas] |
|---|---|---|
| CLF-VAR-C01 | STR-001 | London ideal: marco 4h (velas 21/17/01 ET), 3 escenarios, entrada tras expansión en "nuestra vela", salida temporal vela de las 5, red flags completas |
| CLF-VAR-C02 | STR-002 | Rango pendiente→DOL: cadena nativa 4h, resolución TS `TS_CLOSE` (cierre de la vela base), selección de referencia `leftmost_unbroken`, salida DOL, sin refinado, ancla horaria del curso (America/New_York), red flags completas |
| CLF-VAR-C03 | STR-003 | NY continuación: vela 5am consolidación, expansión vela 9am, DOL no tomado tras London, "cómo abren las velas" |
| CLF-VAR-C04 | STR-004 | NY reversal: objetivo completado en London ⇒ reversión en NY |
| CLF-VAR-C05 | STR-005 | Refinado base: refinado 15m sobre STR-002 (ch04 "nunca bajo de 15") |
| CLF-VAR-C06 | STR-006 | Failure swing: identificación en vivo (reacción+OB+motivo), tolerancia por defecto |
| CLF-VAR-C07 | STR-009 | Reentrada técnica intra-TS: 1 reentrada por rearme técnico, no por stop físico |
| CLF-VAR-C08 | STR-007/008 | Controles de contrato DATA_BLOCKED: fixtures sintéticos de SMT y Noticias (sin backtest NQ-only) |

`[RECON]` C08 agrupa en UN control los contratos de las dos estrategias data-blocked para no inflar conteo de estrategias; sus fixtures existen para conformance, no para backtest.

## TIER 2 — Sustituciones (21 IDs / 22 sets)

| Variant ID | Eje sustituido | Padre | Valor vs control |
|---|---|---|---|
| CLF-VAR-S01 | Resolución TS | C02 | `TS_EARLY_1M`: tras TS+reacción no hace falta cierre (ch02 R5·c-0035) — emisión al primer cierre 1m causal contra el sweep (vs `TS_CLOSE` base) |
| CLF-VAR-S02 | Resolución TS | C02 | `TS_M30`: confirmación en M30 ante duda del 15m (ch04 R23·c-0099) |
| CLF-VAR-S03 | Bias | C02 | EMA en lugar de cadena de rangos (la cadena nativa PERMANECE como control interno del detector; no desaparece) |
| CLF-VAR-S04 | Bias | C02 | Estructura swing (HH/HL) en lugar de cadena |
| CLF-VAR-S05 | Bias | C02 | DMI+ADX **con variable de dirección** (ADX≥20 / ADX≥25 — 2 parameter sets, 1 ID) |
| CLF-VAR-S06 | Ancla horaria | C02 | NY cash 09:30 ET (vs horas del curso) |
| CLF-VAR-S07 | Ancla horaria | C02 | CME 17:00 CT (America/Chicago, DST vía calendario) |
| CLF-VAR-S08 | Salida | C03 | Salida DOL en estrategia de sesión (base temporal) |
| CLF-VAR-S09 | Salida | C02 | Salida temporal vela de las 5 (base DOL) |
| CLF-VAR-S10 | TF pendiente | C02 | 1h (vs 4h) |
| CLF-VAR-S11 | TF objetivo | C02 | 1D (vs 4h) |
| CLF-VAR-S12 | Refinado | C02 | 15m — **EQUIVALENT_TO=C05** (misma identidad experimental; se ejecuta una vez y se cuenta en ambas filas como equivalencia, no como dos votos) |
| CLF-VAR-S13 | Refinado | C02 | 30m |
| CLF-VAR-S14 | Tolerancia FS | C06 | Estricta (reacción confirmada estricta) |
| CLF-VAR-S15 | Tolerancia FS | C06 | Amplia (admite variantes del motivo) |
| CLF-VAR-S16 | Tolerancia de rango | C02 | Selección estructural de vela izquierda NO adyacente (claim ch01 c-0005) vs vela inmediata |
| CLF-VAR-S17 | Resolución TS | C02 | `TS_WICK_NEXT`: confirmación por mecha de la vela siguiente al sweep (ch09 c-0035/c-0036) |
| CLF-VAR-S18 | Reentradas | C07 | 0 reentradas |
| CLF-VAR-S19 | Reentradas | C07 | 2 reentradas |
| CLF-VAR-S20 | Red flags | C02 | OFF |
| CLF-VAR-S21 | Red flags | C02 | Duras solamente (vs completas) |

## TIER 3 — Interacciones (5)

| Variant ID | Interacción | Hipótesis registrada |
|---|---|---|
| CLF-VAR-T01 | Ancla CME × refinado 15m | La apertura de sesión CME relocaliza el rango de referencia y el refinado aprovecha mejor la manipulación temprana |
| CLF-VAR-T02 | TS temprano (1m causal) × stop más ancho | Entrada más temprana exige stop más ancho para sobrevivir el ruido de la reacción |
| CLF-VAR-T03 | NY reversal × objetivo HTF intacto | La reversión sólo tiene recorrido cuando el DOL del TF superior NO fue tomado en London |
| CLF-VAR-T04 | Failure swing × ventanas clave | El FS en horas 5/9 ET (aperturas de vela) tiene más valor informativo que fuera de ellas |
| CLF-VAR-T05 | Noticias × TS previo obligatorio | DATA_BLOCKED sin calendario; hipótesis documentada, fixtures de contrato sólo |

## Splits temporales (congelar antes de comparar PnL)

Particiones cronológicas desde sesiones elegibles reales (corpus 2023-10-02→2026-10-06, 672 sesiones):

```text
Development 60% · Validation 20% · Final holdout 20%
```

- Fechas exactas calculadas desde el corpus en P5 con el mayor lookback como embargo/purge.
- El holdout final NO se usa para ajustar reglas tras observar resultados.
- R02/R03 usaron el mismo histórico para otras familias (ORB/FBC/MR/TG): cualquier ventana ya usada para SELECCIONAR hipótesis Clutifx se declara contaminada; hoy no existe selección previa Clutifx, por lo que las particiones nacen limpias para esta familia (las familias previas no contaminan porque no seleccionaron variantes Clutifx).

## Dependencias y no-duplicación

- STR-005 hereda sesión/padres de STR-002: no se clasifica independiente para sesiones FX.
- STR-009 hereda dependencias de la estrategia madre + rearme técnico.
- STR-007/008: bloqueadas por datos; sus controles de contrato (C08) corren fixtures, jamás backtest NQ-only disfrazado.
- Parámetros distintos NO crean registros Strategy nuevos (misma spec, distinto parameter_set_id).

## GATE P1 (2026-10-23)

```text
RANGE_SEMANTICS               = VERIFIED  (leftmost_unbroken + c-0005 + determinismo de solapes)
TEMPORAL_CAUSALITY            = VERIFIED  (TS 5 etapas; P3 proxy apertura; sin intrabar)
MULTITF_WARMUP                = VERIFIED  (derivation por requirements; NOT_READY explícito)
STRATEGY_MM_BOUNDARY          = VERIFIED  (STR-009 rearme técnico; sin fills/cuenta en Strategy)
SESSION_PROVIDER_COMPATIBILITY= VERIFIED  (America/New_York; admisión E2T 10:00 registrada aparte)
```

Catálogo v1.0 RECONSTRUIDO congelado: STRATEGIES-MASTER + OBJECTIVE-DETECTORS + EXPERIMENT-MATRIX + SOURCE-COVERAGE + HEFESTO-BASELINE-AUDIT (34 IDs, 35 sustituciones efectivas, 1 equivalencia declarada S12≡C05).
