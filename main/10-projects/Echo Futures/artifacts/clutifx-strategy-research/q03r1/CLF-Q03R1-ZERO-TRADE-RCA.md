# CLF-Q03-R1 — ZERO-TRADE RCA (FASE 4)

Fecha: 2026-10-26 · Ejecutor: manager ZCode (GLM-5.3-Flash) · Rama `experiment/clutifx-s01` @ `a166ecb0` · Último contrato NQZ6 (17 sesiones elegibles).

Regla aplicada: ninguna variante termina como `0 trades` sin diagnóstico causal y clasificación persistente. Orden de inspección barato→caro del runbook (casos A–H). Todo número proviene de los intentos físicos R1 (`~/echo-work/clutifx-backtest/q03r1/g2-nqz6/`) y del censo físico de ciclos previos (81 intentos).

## Caso A — Nunca alcanza ready: NINGUNO

Las 27 corridas R1 sobre NQZ6: `evaluations` 13.867–14.326, `ready` 12.060 en todas (86–87%). Sin warmup perpetuo, sin resets, sin defecto de composición temporal. **El caso A está vacío en R1.**

## Caso B — Ready, cero oportunidades (setup genuinamente ausente): C06, S15, T04 + S01/S02/S17 en NQZ6

| identidad | evaluaciones | ready | señales NQZ6 | señales NQU6 (trimestre completo) | veredicto |
|---|---|---|---|---|---|
| C06 (failure swing base) | 14.037 | 12.060 | 0 | 0 (campaña completa) | `VALID_RARE_NO_ACTIVITY` |
| S15 (fs wide) | 14.037 | 12.060 | 0 | 0 (campaña completa) | `VALID_RARE_NO_ACTIVITY` |
| T04 (fs key hours) | 14.037 | 12.060 | 0 | 0 (campaña completa) | `VALID_RARE_NO_ACTIVITY` |
| S01 (TS_EARLY_1M) | 13.867 | 12.060 | 0 | 4 (todas fuera de ventana) | `SESSION_INCOMPATIBLE` (veredicto dominante del trimestre) |
| S02 (TS_M30) | 14.326 | 12.060 | 0 | 4 (ídem) | `SESSION_INCOMPATIBLE` |
| S17 (TS_WICK_NEXT) | 13.867 | 12.060 | 0 | 4 (ídem) | `SESSION_INCOMPATIBLE` |

Lectura causal: el detector quedó **ready** (12.060 evaluaciones con lookback cumplido) y los predicados del setup (reacción + order block + motivo confirmado) no ocurrieron en la ventana de 9 sesiones de trading. No es código roto: en el trimestre NQU6 completo la familia FS tampoco produjo setups, mientras las variantes TS de STR-002 sí produjeron señales (4 cada una) — todas fuera de la ventana operable. La rareza es del patrón, no del motor. El veredicto final de S01/S02/S17 lo da su evidencia de trimestre (`SESSION_INCOMPATIBLE`, correlación por SignalID en `q03/session-compatibility/`); sobre NQZ6 su funnel quedó `INCONCLUSIVE_NO_SIGNALS` (sin señales no hay incompatibilidad demostrable en esa ventana).

## Caso C — Oportunidades sin señales: NINGUNO demostrado

Ninguna identidad mostró oportunidades absorbidas sin emisión (`entry_filter_absorbed=0` en todas las trazas R1). La cadena C05 (refine) absorbe candidatos antes del SIGNAL en NQU6 (trazas Q02), pero en NQZ6 S12/S13 emitieron normalmente. No hay divergencia implementación-vs-knowledge nueva que corregir en R1.

## Caso D — Señales fuera de horario operable: C01, C04 (+ S01/S02/S17 por su trimestre)

| identidad | señales NQZ6 | distribución horaria ET | rechazos de sesión | clasificación |
|---|---|---|---|---|
| C01 (London ideal) | 2 | 2×01:00 | 2/2 | `SESSION_INCOMPATIBLE` |
| C04 (NY reversal) | 3 | 1×05:00, 2×09:00 | 3/3 | `SESSION_INCOMPATIBLE` |

Reproducción exacta del patrón NQU6 (C01: 1×01:00; C04: 4×05:00 + 2×09:00). Las emisiones ocurren en los cierres causales de las velas del curso (21/17/1/5/9 ET): estructura fiel a la fuente y estructuralmente ajena a la ventana E2T `[09:30, 15:55)` ET del AccountPolicy. **Intersección posible: no existe** (la vela 09:00 cierra a las 09:00, antes de la apertura 09:30). C01 además arrastra `CAMPAIGN_UNAVAILABLE` (sin cuenta al momento de las emisiones). No se adaptó horario alguno: una adaptación NQ de ancla sería identidad NUEVA pre-declarada (eje tipo S06/S07) — ficha KRR-001/KRR-002 para decisión del Owner.

## Caso E — Señales admitidas sin fills: S13 en NQU6-G2 (7 sesiones), resuelto

En la ventana corta NQU6 06-14→06-25, S13 registró 1 señal con rechazo `SIZE_BELOW_MIN_CONTRACT` (MM no admitió el mínimo). En el trimestre NQU6 completo S13 operó (2 fills, 1 round-trip) y en NQZ6 R1 operó (8 fills, 4 round-trips). Clasificación del episodio: `SIGNAL_REJECTED_VALID_POLICY` (tamaño mínimo del RuleSet, no defecto). **Ningún `SIGNAL_EXECUTION_DEFECT` en R1.**

## Caso F — Entradas sin operación completa: NINGUNO

27/27 corridas R1 con `open_at_horizon=0`: todo fill de entrada tuvo su cierre ejecutado y conciliado (stop protector, objetivo o cierre de sesión `RESEARCH_DAILY_CLOSE_V1`). La cadena de cierre protegido (R03) no mostró wedges.

## Caso G — Round-trips completos, todos perdedores: C03 en NQZ6 (muestra negativa conservada)

C03 (NY continuación): 1 round-trip en NQZ6, PERDEDOR (−495,00 bruto, LONG 30.602,50 → 30.577,75, stop-out 19 s tras la entrada). En NQU6 la misma identidad ganó +795,04 neto con cuenta pendiente. **No es un bug**: dirección, stop y target concuerdan con la spec; el sample es pequeño y contrario. Clasificación: `FULLY_TRADED_NEGATIVE_SAMPLE` dentro del veredicto `QUARTER_NO_PASS` — la evidencia negativa se conserva y no se cambió nada para fabricar un ganador.

## Caso H — Operaciones completas, cero challenges: TODAS las 19 con G2C PASS

Las 19 identidades con operación completa en el último contrato ya ejecutaron su campaña NQU6 (18 filas de identidad, 27 campañas físicas históricas con 54 round-trips): **0 `CHALLENGE_PASSED`**. Veredicto `QUARTER_NO_PASS` por identidad; G5 elegible = ∅. Las campañas no se repiten bit-idénticamente (el guard lo bloquea: `RECEIPT_NOT_A_QUALIFICATION_CHAIN`).

## Resumen de veredictos (34 IDs, exactamente uno por fila)

| veredicto | IDs |
|---|---|
| `QUARTER_NO_PASS` | C02, C03, C07, S03, S04, S05, S06, S07, S09, S10, S11, S12, S13, S16, S19, S20, S21, T01 |
| `SESSION_INCOMPATIBLE` | C01, C04, S01, S02, S17 |
| `VALID_RARE_NO_ACTIVITY` | C06, S15, T04 |
| `ALIAS_VERIFIED` | C05 (≡S12), S14 (≡C06), S18 (≡C02) |
| `NEEDS_ITERATION` | S08, T03 (declaradas, dependencia resuelta, config pendiente de ciclo posterior) |
| `BLOCKED_SPEC` | T02 |
| `BLOCKED_DATA` | C08 (STR-007/008), T05 |
| `QUALIFIED_LAST_CONTRACT` / `PROMOTED_FOR_HIST` / `ENGINE_DEFECT` | — (vacíos: cero pases de challenge ⇒ nadie promociona; cero defectos de motor demostrados) |
