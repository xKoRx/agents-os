# CLF-E05R1 — H2–H5 FAILURE SWING FIX

Fixes: F-K05-02/03/04/05 (P0/P0/P0/P1) · Commit `3c0c683c` · `OWNER_ACCEPTANCE: REVIEW`

## H2 — Order block opcional (`fs_order_block_mode`)

`optional` (nuevo default SOURCE: identificación canónica c-0029 SIN OB; c-0047 «puedes esperar si quieres») resuelve el veredicto con reacción + motivo; `required` conserva reproducible la conjunción histórica (S14 lo declara explícito). El OB queda registrado en el veredicto como diagnóstico `order_block_present`. Valores desconocidos fail-closed; los knobs `fs_*` siguen siendo STR-006-only.

## H3 — Reacción = creación de rango opuesto

Predicado nuevo: `EventRangeCreated` con `Range.Side == dirección del swing` sobre la propia cadena del detector (1h), confirmado causalmente al cierre de la vela que crea el rango — incluida la MISMA vela del intento (c-0015 «la reacción aparece ya — durante la vela en curso del fallo»; la captura same-bar no resuelve en la vela del intento: el veredicto nunca drafttea ahí). Fallado high ⇒ rango bajista (side SHORT); fallado low ⇒ rango alcista (side LONG) — lectura ch01 c-0007/c-0009 + código de la cadena. El predicado retirado (cierre más allá del nivel) sobrevive sólo como diagnóstico `close_beyond_level`; los fixtures prueban que los predicados divergen en la MISMA vela (FX-02 B: cierra-más-allá sin creación no reacciona — el falso positivo histórico).

## H4 — Ventana `until_invalidation` (default SOURCE)

La observación permanece abierta mientras el extremo fallido NO sea tomado (c-0048); la invalidación usa el hecho de cadena (toma del extremo: `EventExtremeConsumed` o `EventRangeCreated` con Level == extremo — la toma con cierre adentro también invalida y NO cuenta como reacción). `strict`/`wide` quedan como variantes congeladas (preservan su semántica de presupuesto de velas). Guard de doble emisión: la vela que RESUELVE un veredicto no re-arma sobre sí misma (su evidencia de reacción fue consumida; re-armar adjuntaría el mismo evento a un intento fresco y re-emitiría el mismo swing). **Límite de estado corregido:** la composición 1m de la vela de referencia se congela EN el intento al armar (la vela ya cerró — causal); la retención rodante de 4 buckets no alcanza para ventanas hasta invalidación — sin este congelamiento, todo swing que resolviera >4h tras su referencia reportaba MOTIVE_UNAVAILABLE.

## H5 — Rangos adversos al evaluador real

`FailureSwing.AdverseActive(dir)` expone las rangos activas de la propia cadena; `entryFailureSwing` las pasa como `AdverseRanges` al evaluador real de red flags: un FS legítimo contra un rango adverso duro se bloquea con `CLF_RED_FLAGS_BLOCKING` (ch09 c-0007/c-0012). Fixture e2e FX-04 (`fs_redflags_test.go`): bloqueo en full mode + control `redflags_mode=off` que sí drafttea — el plano de red flags es el bloqueador. «Rangos a favor» queda como diagnóstico, nunca bloqueo extra.

## Fixtures (G1) — todos verdes

FX-01 (legítimo sin OB vs required con el mismo feed), FX-02 (A/B de predicados + same-bar), FX-03 (multi-vela + invalidación + estado acotado en 28 velas quietas), FX-04 (detector + e2e estrategia), FX-08 (C02 bit-idéntico: suite STR-002/sesiones verde sin cambios).

## Resultado físico (G2, NQZ6 2026-09-22→2026-10-05)

Funnel exacto medido con arnés de detector sobre la ventana sellada (13.800 velas 1m): **4 intentos fallidos → 4 invalidados (el extremo fue tomado antes de que reacción alguna confirmara) → 0 veredictos → 0 señales**. Con los fixtures probando la construcción y el funnel mostrando los predicados operando, la clasificación por identidad es `VALID_RARE_NO_ACTIVITY` EN LA VENTANA — la frecuencia 0 ya NO es atribuible a la conjunción excedida (corregida), es el comportamiento del mercado NQ en estas 10 sesiones bajo la lectura fuente. El eje real post-fix (OB opcional + predicado de rango + ventana) queda disponible para el quarter cuando el Owner lo autorice; T04 (horas clave) idem.
