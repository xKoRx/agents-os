# CLF-E05R1 — H1 BIAS FIX

Fix: F-K05-01 (P1) · Commit: `3c0c683c` · Binario sellado: `echo-backtest-clf-e05r1-20261026` sha256 `a40cc96e26cf41e5da396c33362fea6c9fe2b2686090deab194919e58a74406c` · `OWNER_ACCEPTANCE: REVIEW`

## Qué cambió

Las cuatro puertas de entrada (`decision.go::entryRange`, `decision.go::entryFailureSwing`, `session_decision.go::entryLondon`, `session_decision.go::entryNYContinuation`) consultaban `p.bias.NativeAggregate()` — la lectura nativa SIEMPRE — dejando los motores sustitutos (S03 ema, S04 structure, S05 dmi_adx) inertes por cableado (E05-01/KRR-008). Ahora consultan `p.bias.Aggregate()` (el agregado del motor configurado).

**Semántica pre-declarada (fijada antes de codificar, según el handoff):** agregado neutral (`facing|mixed|none|undetermined|di_equal|warmup`) ⇒ la entrada se rechaza con `CLF_BIAS_NOT_FAVORING` — fail-closed, SIN fallback silencioso al nativo (coherente con ch08 R5 «rangos enfrentados ⇒ ignorar el TF»). La lectura nativa se conserva como diagnóstico del payload (`bias_native_control` + `bias_engine`, SOLO para motores sustitutos: los payloads del motor nativo conservan los bytes planos históricos — C02 bit-idéntico, FX-08a). `entryNYReversal` NO lleva puerta de bias por diseño (documentado en el docstring, F-K05-13).

## Fixtures (G1)

`bias_gate_test.go` + `gates_test.go`: FX-05 — EMA opuesto al nativo rechaza LONG (y el espejo SHORT); structure y dmi_adx neutrales rechazan fail-closed; engine=native conserva la decisión y la forma del payload; warmup consume en silencio con motor sustituto; LONG/SHORT; snapshot/restore (round-trip JSON completo por evaluación en todo el arnés); rollover=costura de estado (el canario físico G3 es del ciclo propio, ver recibos).

## Escenario pesado (estructura/DMI opuestos reales)

`TestCLFBiasGateStructureAndDMIOpposite_FX05`: escenario de 23 días (descenso + ciclos D/U con pivotes LH/LL confirmados + DMI -DI>+DI) donde structure y dmi_adx leen SHORT contra las entradas LONG del control nativo: ambos motores vetan CADA barra de emisión del control con `CLF_BIAS_NOT_FAVORING` y la lectura 1d persistida dice `SHORT` — la negación es por lectura opuesta, no por warmup. (El motor puede además pasar sus propias emisiones SHORT de acuerdo — la misma puerta funcionando.)

## Prueba física (G2, última contrato NQZ6, ventana sellada 2026-09-22→2026-10-05)

| Identidad | evals | ready | fills | ops | round-trips | net |
|---|---|---|---|---|---|---|
| C02 control (q03r1, misma ventana, build anterior) | 13.867 | 12.060 | 8 | 4 | 4 | -1.244,90 |
| **S03 ema (E05-R1)** | 13.867 | 12.060 | 6 | 3 | 3 (2W/1L) | **+10,06** |
| S04 structure | 13.867 | 12.060 | 0 | 0 | 0 | 0 |
| S05A/S05B dmi_adx | 13.867 | 12.060 | 0 | 0 | 0 | 0 |

S03 ya NO es réplica de C02: mismo window, mismas sesiones, decisiones y economía distintas — el eje de sustitución de motor mide de verdad. El tape de S03 muestra sus propios rechazos `CLF_BIAS_NOT_FAVORING` (el motor EMA veta emisiones que el gate nativo habría pasado). S04/S05A/S05B: ready pleno y cero entradas porque sus agregados no favorecieron ninguna emisión en la ventana — desacuerdo real de motor (los fixtures FX-05 prueban el cableado), no defecto; sus funnel están en los recibos G2A.

## Regresiones

Suite `clf` + `detectors` completa verde (267s + 62s); C02/sesiones/TS/DOL/red-flags sin cambios de comportamiento (los payloads nativos bit-idénticos).
