# CLF-Q03-R1 — SESSION COMPATIBILITY (G2B, último contrato NQZ6)

Fecha: 2026-10-26 · Herramienta canónica: `campaign-lab/session_compatibility.py` · Ventana AccountPolicy E2T/GAU50: `[09:30, 15:55)` ET, fin excluyente, DST vía zoneinfo `America/New_York`. Correlación por `SignalID` desde los records `OPERATION_APPLY/CAMPAIGN_SIGNAL` de cada traza económica real.

Diagnósticos por identidad en `q03r1/session-compatibility/STRATEGY_SESSION_COMPATIBILITY-<ID>-G2-NQZ6.json` (27 archivos, traza sha sellada en cada uno).

## Veredictos sobre el último contrato

| identidad | señales | en ventana | fuera | rechazadas por sesión | hora ET de emisión | veredicto |
|---|---:|---:|---:|---:|---|---|
| C01 | 2 | 0 | 2 | 2 | 01:00×2 | **SESSION_INCOMPATIBLE** |
| C02 | 8 | 8 | 0 | 0 | (campaña compró y operó) | SESSION_COMPATIBLE |
| C03 | 1 | 1 | 0 | 0 | 13:00 | SESSION_COMPATIBLE |
| C04 | 3 | 0 | 3 | 3 | 05:00×1, 09:00×2 | **SESSION_INCOMPATIBLE** |
| C06 | 0 | — | — | 0 | — | INCONCLUSIVE_NO_SIGNALS |
| C07 | 8 | 8 | 0 | 0 | — | SESSION_COMPATIBLE |
| S01 | 0 | — | — | 0 | — | INCONCLUSIVE_NO_SIGNALS |
| S02 | 0 | — | — | 0 | — | INCONCLUSIVE_NO_SIGNALS |
| S03 | 8 | 8 | 0 | 0 | — | SESSION_COMPATIBLE |
| S04 | 8 | 8 | 0 | 0 | — | SESSION_COMPATIBLE |
| S05A | 8 | 8 | 0 | 0 | — | SESSION_COMPATIBLE |
| S05B | 8 | 8 | 0 | 0 | — | SESSION_COMPATIBLE |
| S06 | 9 | 9 | 0 | 0 | — | SESSION_COMPATIBLE |
| S07 | 5 | 5 | 0 | 0 | — | SESSION_COMPATIBLE |
| S09 | 8 | 8 | 0 | 0 | — | SESSION_COMPATIBLE |
| S10 | 5 | 5 | 0 | 0 | — | SESSION_COMPATIBLE |
| S11 | 6 | 6 | 0 | 0 | — | SESSION_COMPATIBLE |
| S12 | 8 | 8 | 0 | 0 | — | SESSION_COMPATIBLE |
| S13 | 7 | 7 | 0 | 0 | — | SESSION_COMPATIBLE |
| S15 | 0 | — | — | 0 | — | INCONCLUSIVE_NO_SIGNALS |
| S16 | 6 | 6 | 0 | 0 | — | SESSION_COMPATIBLE |
| S17 | 0 | — | — | 0 | — | INCONCLUSIVE_NO_SIGNALS |
| S19 | 8 | 8 | 0 | 0 | — | SESSION_COMPATIBLE |
| S20 | 8 | 8 | 0 | 0 | — | SESSION_COMPATIBLE |
| S21 | 8 | 8 | 0 | 0 | — | SESSION_COMPATIBLE |
| T01 | 5 | 5 | 0 | 0 | — | SESSION_COMPATIBLE |
| T04 | 0 | — | — | 0 | — | INCONCLUSIVE_NO_SIGNALS |

## Causalidad de las incompatibles

Las emisiones de C01/C04 ocurren en los cierres causales de las velas del curso (London open 01:00 ET; velas 05:00/09:00 ET) — idéntico al patrón medido en NQU6 (C01: 1×01:00; C04: 4×05:00 + 2×09:00). La ventana operable empieza 09:30 ET: **no existe intersección posible** por construcción del curso. Las 5 emisiones fueron rechazadas por `SESSION_ENTRY_WINDOW` (política legítima del AccountPolicy); ninguna orden se envió.

- C01: 2 señales @01:00 ET, 0 órdenes, 0 fills. Además 2 rechazos `CAMPAIGN_UNAVAILABLE` (sin cuenta).
- C04: 3 señales (05:00/09:00), 0 órdenes, 0 fills, 6 rechazos de campaña totales.
- C03 (control positivo de sesión): 1 señal @13:00 ET (cierre vela 09:00) → admitida → 1 round-trip completo.

S01/S02/S17 quedan `INCONCLUSIVE_NO_SIGNALS` sobre NQZ6 (0 señales en 9 sesiones); su veredicto dominante `SESSION_INCOMPATIBLE` viene de su trimestre NQU6 (4/4 señales fuera de ventana por SignalID, `q03/session-compatibility/`). Ambas dimensiones quedan en el ledger.

## Consecuencia de admisión

`G2B` con veredicto distinto de `SESSION_COMPATIBLE` bloquea la puerta quarter (`admit_quarter` → `G2B_NOT_SESSION_COMPATIBLE`), verificado mecánicamente con recibos reales de C01 y C06 en `q03r1/quarter-door-real-receipts.json`. Prohibido modificar horarios de Provider ni ventanas de prop firms para fabricar entradas; una adaptación de ancla horaria es una identidad NUEVA pre-declarada (fichas KRR-001/KRR-002).
