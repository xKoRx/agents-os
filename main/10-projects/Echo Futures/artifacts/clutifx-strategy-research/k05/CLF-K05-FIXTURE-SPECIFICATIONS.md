# CLF-K05 — FIXTURE SPECIFICATIONS

Fixtures exigidos para demostrar cada corrección antes de cualquier re-gateo. Formato del contrato P2 (`CLUTIFX-OBJECTIVE-DETECTORS.md`): secuencias OHLC controladas con `input bars / known information at decision_time / expected state / expected Signal / expected stop / expected lifecycle`. Todos deterministas, sin lookahead salvo los contraejemplos deliberados. Base: contrato físico vigente para G2 (NQZ6 last-contract al 2026-10-25; NQU6 trimestre).

## FX-01 — FS legítimo sin order block (demonstra F-K05-02)

Secuencia 1h: (b1) vela de referencia con high H; (b2..b4) velas cuyo high quedan por debajo de H pero dentro de ApproachTicks del extremo, con el extremo H logrado en la composición 1m dentro de los últimos EndMinutes de b1 (motivo 2 sembrado); (b5) vela que CREA rango bajista (toma el low de b4 y cierra dentro — `EventRangeCreated` side SHORT) SIN que exista order block (ningún cierre bajista por debajo del low de la última vela alcista). Esperado post-fix: veredicto `FS_LEGITIMATE` con motivo `extreme_at_candle_end`, OB ausente registrado como diagnóstico (`order_block=false`). Contraejemplo: la MISMA secuencia con el extremo logrado a mitad de b1 → `MOTIVE` falla → sin veredicto (R9).

## FX-02 — Reacción = rango opuesto, no cierre-bajo-nivel (demonstra F-K05-03)

Caso A (debe disparar): b5 crea rango bajista con su cierre AÚN POR ENCIMA del nivel fallido H (rango local bajo H). Estado actual: `reactionClose` falso → no dispara (fallo del predicado actual, fixture ROJO para el código vigente). Caso B (no debe disparar): b5 cierra por debajo de H sin crear rango bajista alguno (no toma ningún low previo / no cierra dentro). Estado actual: dispara (falso positivo del predicado actual). El par A/B es la prueba de que los predicados no son equivalentes.

## FX-03 — Ventana multi-vela hasta invalidación (demonstra F-K05-04)

Intento fallido en b4; reacción (rango opuesto) sólo en b7; el extremo H nunca es tomado en b5–b7. Esperado post-fix (modo fuente): veredicto legítimo en el cierre de b7. Contraejemplo: b6 toma H (invalidación) → `NOT_FS` y re-arma. Variante strict/wide conservada como config: strict exige reacción en b5 (comportamiento actual) — fixture prueba que el default ya no es strict.

## FX-04 — Red flag adversa en FS (demonstra F-K05-05)

FS legítimo (per FX-01) con un rango alcista ACTIVO en la cadena 1h del propio detector (creado 2 velas antes, no eliminado) y dirección del FS SHORT... (adversa = opuesta a la dirección del trade; para FS SHORT el adverso es alcista activo). Esperado post-fix: `RedFlagsReport.Blocking=true`, `DiagnosticReason=CLF_RED_FLAGS_BLOCKING`, sin draft. Contraejemplo: mismo FS sin rangos adversos → draft emitido.

## FX-05 — Gate de bias por motor configurado (demonstra F-K05-01)

Con `bias_engine=ema` y una serie donde EMA(9/21) en 1d es SHORT mientras la cadena nativa 1d es LONG: señal LONG debe ser RECHAZADA post-fix (`CLF_BIAS_NOT_FAVORING` con lectura del motor), hoy pasa (gate nativo). Contraejemplo con `engine=native`: pasa. Idem structure y dmi_adx (con +DI>-DI opuesto a la cadena). Semántica neutral pre-declarada: motor en facing/undetermined ⇒ sin entrada (bias not favoring) — fixture neutral incluido.

## FX-06 — Refinado en specs de sesión (demonstra F-K05-06)

Spec C01 con `refine_timeframe=15m`: TS base (referencia anterior a London) arma dentro de [01:00,05:00); el refinado 15m confirma TS en la misma dirección dentro de la vela siguiente al armado → draft con rule STR001 refinada y stop del refinado (TF de entrada). Esperado: exactamente UN draft; expiración al cierre de la vela de setup siguiente sin confirmación (ReasonRefineExpired). Negativo: refine en dirección opuesta ⇒ no draft.

## FX-07 — Rango activado por FS como premisa de sesión (demonstra F-K05-07)

Día donde el rango 4h/8h se activa POR FS (sin toma del extremo, `c-0197`–`c-0204`): C03-variante debe emitir en la vela de las 9 con DOL alineado; C03 control NO emite (documento del hueco). Negativo: día sin FS ni sweep → sin señal en ambas.

## FX-08 — Regresiones que NO deben romperse

(a) C02 control: la campaña NQU6 existente bit-idéntica (no re-ejecutar; sólo fixture de humo con el golden existente). (b) TS 4 modos: suites vigentes verdes. (c) DOL taken/recompute: touch-1m y borrado. (d) S16/S10/S11: ejes con comportamiento propio demostrado. (e) Simultaneidad y orden determinista (cierre HTF antes de 1m consumers; orden descendente del compositor). (f) Warmup/DST/rollover: arnés anti-lookahead vigente. (g) Draft sin campo target (SPEC §9.2) y sin gestión de cuenta en Strategy.

## Presupuesto y orden

FX-01..05 bloquean el re-gateo de C06/S14/S15/T04 (G0→G2C propios, contrato NQZ6, no el histórico). FX-06/FX-07 son identidades NUEVAS pre-declaradas (ciclo G0→G4 propio cada una, presupuesto por gate del runbook). FX-08 es regresión del paquete. Estimación de suites: sin cómputo de mercado salvo los G2 indicados.
