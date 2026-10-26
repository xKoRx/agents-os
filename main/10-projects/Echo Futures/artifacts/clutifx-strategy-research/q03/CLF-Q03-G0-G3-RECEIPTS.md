# CLF-Q03 — G0–G4 RECEIPTS POR IDENTIDAD

Fecha: 2026-10-25 · Contrato cualificado: **NQU6 físico único** (60 sesiones elegibles, 2026-06-14T22:00Z → 2026-09-13T22:00Z, 0 rolls dentro; NQZ6=17 sesiones NO califica, declarado en Q02) · Dataset sellado: `~/echo-work/data/corpus/NQU6.nt` sha `4f63...` (ver recibos) · Correlación de recibo de datos: `qualification/…NQU6` del ciclo previo.

Identidad de ejecución (G0): rama `experiment/clutifx-s01` @ `fb950d68` (árbol limpio) · binario sellado `echo-backtest-clf-q03-20261025` sha256 `04cf933b41b6…` · MM SG-R500 (riskgeometry GROSS500, digest en recibos) · CHALLENGE_ONLY + CONTINUOUS_V1 · perfil E2T/GAU50.

## Intentos (attempts nunca sobrescritos; intentos fallidos preservados con causa)

| gate | intento | causa | estado |
|---|---|---|---|
| G2×3 | `-intento1-badbuild` | build del plan declaraba commit Q02 (`c127b894`) vs binario Q03 | preservado |
| G2×3 | `-intento2-modifiedtree` | `__pycache__` trackeado rompía `tree_clean` | preservado (higiene: commit `fb950d68` elimina los .pyc del repo) |
| G2×3 | `-intento3-fanout` | fanout_targets sin reasociar a la estrategia nueva | preservado |
| G3×3 | `-intento1-staleref` | schedule del canario con referencias al id antiguo | preservado |
| G4 | (único) | — | completo |

## G2 — Smoke individual (7 sesiones, 2026-06-14→06-25)

| identidad | evaluaciones | ready | señales | en ventana | compra | fills | resultado | estado |
|---|---|---|---|---|---|---|---|---|
| C01 | 9.709 | 6.182 | 0 | 0 | 0 | 0 | INCONCLUSIVE_NO_SIGNALS (READY_LOW_SIGNAL) | COMPLETE+rec |
| C03 | 9.709 | 6.182 | 1 | 1 | 1 | 2 | **SESSION_COMPATIBLE con ruta económica completa** (señal→admisión→2 fills) | COMPLETE+rec |
| C04 | 9.709 | 6.182 | 0 | 0 | 0 | 0 | INCONCLUSIVE_NO_SIGNALS (READY_LOW_SIGNAL) | COMPLETE+rec |

El 63,7% ready en ventana corta es consistente con el perfil Q02 (warmup 1d/4h); sin warmup perpetuo.

## G3 — Canario de rollover físico NQM6→NQU6 (2026-06-14T22:00Z; ventana 2026-06-07→06-18)

| identidad | evaluaciones | ready retenido | evaluaciones post-roll | CANDIDATE_WARMUP_FAILED | estado |
|---|---|---|---|---|---|
| C01 | 7.961 | 6.181 | 4.171 callbacks en 52 sesiones post-roll | 0 | COMPLETE+rec |
| C03 | 7.961 | 6.181 | ídem | 0 | COMPLETE+rec |
| C04 | 7.961 | 6.181 | ídem | 0 | COMPLETE+rec |

`ready` se retiene a través del roll sin re-warm perpetuo (el contador no se reinicia); las evaluaciones continúan en NQU6 desde la primera sesión post-roll. G3 **PASS** por identidad.

## G4 — Trimestre NQU6 (60 sesiones)

| identidad | compras | pases | pérdidas | pendientes | ops | fills | días con entrada | neto | sesión | promoción |
|---|---|---|---|---|---|---|---|---|---|---|
| C01 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 USD | **SESSION_INCOMPATIBLE** (1 emisión @01:00 ET) | QUARTER_NO_PASS |
| C03 | 1 | 0 | 0 | 1 | 2 | 4 | 2 | **+795,04 USD** | SESSION_COMPATIBLE | QUARTER_NO_PASS |
| C04 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 USD | **SESSION_INCOMPATIBLE** (4×05:00, 2×09:00 ET) | QUARTER_NO_PASS |

Distribuciones horarias (detalladas en `session-compatibility/*-G4.json`): C01 emite en la apertura London (01:00 ET) — fuera de la ventana E2T por estructura del curso; C04 emite en los cierres 5:00/9:00 ET; C03 convierte a las 13:00 ET (cierre de la vela 9:00), dentro de ventana.

**Condición de promoción (literal Owner): ≥1 CHALLENGE_PASSED real y conciliado. Cero pases en las tres identidades ⇒ G5 elegible = 0, ejecutado = 0.** El guard lo valida por sí mismo: `admit_historical(C03) → BLOCKED G4_NO_PASS` (verificado mecánicamente sobre el recibo sellado).

## Recibos de cualificación

`q03/receipts/*.json` (schema `echo.strategy-qualification.v1`, sellados por digest; índice en `q03/QUALIFICATION-SUMMARY.json`): C01 `receipt` con G0–G3 PASS y G4 QUARTER_NO_PASS; C03 ídem con compra conciliada (cash_events PURCHASE 120 USD, cuenta pendiente, +795,04 neto); C04 ídem. Los recibos existen y son válidos como EVIDENCIA; la promoción a histórico queda bloqueada por el propio guard.
