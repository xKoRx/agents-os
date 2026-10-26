# CLF-E05R1 — G0–G3 RECEIPTS

Ciclo: CLF-E05-R1 · Build: commit `3c0c683c` + binario `echo-backtest-clf-e05r1-20261026` (sha256 `a40cc96e…`) · Contrato G2: NQZ6 ventana sellada LASTCONTRACT-NQZ6-20261005 (warmup 2026-09-13T22:00Z, trade 2026-09-22T14:00Z→2026-10-05T21:00Z; 17 elegibles; dataset `/home/kor/echo-work/data/corpus/NQZ6.nt`) · `OWNER_ACCEPTANCE: REVIEW`

## G0 — implementación congelada

Catálogo corregido: 8 identidades K05 (S03/S04/S05A/S05B bias; C06/S14/S15/T04 failure swing). identity-params con SHA. Builds: commit `3c0c683c`, tree_clean=true, binario sellado. Receipts: `e05r1/receipts/` con digests verificables.

## G1 — corrección (fixtures positivos/negativos)

Suite `clf` + `detectors` verde completa sobre el commit congelado (267s + 62s; log `e05r1/go-clf-suite.log`). Fixtures FX-01..05 + dominios de config (`fs_order_block_mode`, `fs_tolerance=until_invalidation`) + C02 bit-idéntico. El G1 de cada identidad es el fixture dedicado de su fix (FX-05 bias; FX-01..04 FS).

## G2A/G2B/G2C por identidad (físico, NQZ6)

| Identidad | G2A (evals/ready/señales) | G2B | G2C | receipt |
|---|---|---|---|---|
| C06 | PASS (PASS) | INCONCLUSIVE_NO_SIGNALS | FAIL (0 rt) | `sha256:4e07fd9c099f7…` |
| S03 | PASS (PASS) | SESSION_COMPATIBLE | PASS (3 rt) | `sha256:2f937b86e6fc8…` |
| S04 | PASS (PASS) | INCONCLUSIVE_NO_SIGNALS | FAIL (0 rt) | `sha256:1e64c2f1c197c…` |
| S05A | PASS (PASS) | INCONCLUSIVE_NO_SIGNALS | FAIL (0 rt) | `sha256:79148efa96c48…` |
| S05B | PASS (PASS) | INCONCLUSIVE_NO_SIGNALS | FAIL (0 rt) | `sha256:9c62d347a097b…` |
| S14 | PASS (PASS) | INCONCLUSIVE_NO_SIGNALS | FAIL (0 rt) | `sha256:badfcd0dadcb6…` |
| S15 | PASS (PASS) | INCONCLUSIVE_NO_SIGNALS | FAIL (0 rt) | `sha256:0b7c75ee85480…` |
| T04 | PASS (PASS) | INCONCLUSIVE_NO_SIGNALS | FAIL (0 rt) | `sha256:223c44982ac7d…` |

Funnel FS exacto (arnés de detector sobre la ventana sellada): 13.800 velas 1m → 4 intentos → 4 invalidaciones (toma del extremo antes de reacción) → 0 veredictos → 0 señales. S03: 15 señales → 3 admitidas → 6 fills → 3 round-trips (2W/1L, net +10,06).

## G3 — rollover

Canario fresco bloqueado por el clasificador de propósito (`PURPOSE_CONTRADICTS_EXECUTION_IDENTITY`: la ventana corta de roll se clasifica HISTORICAL — evidencia preservada en `e05r1/g3-roll/out-E05R1-S03-G3/QUALIFICATION-BLOCKED.json`, exit 78, 0 motores). Por el precedente Q03-R1, G3 se REUTILIZA del ciclo propio de cada identidad (Q02, roll NQM6→NQU6 2026-06-07..2026-06-18) con nota de linaje honesta: el build E05-R1 cambia la capa de DECISIÓN (H1/H2-H5), no la maquinaria de warmup/Requirements/rollover; el recibo Q02 queda ligado a su propio build y el G4 se admite bajo el guard con esa cadena.

## Verificación de admisión quarter (S03)

`qualification_guard.admit_quarter` ADMITIÓ la campaña NQU6 de S03 (cadena G0-G3+G2C sellada + contract_set NQU6 + window identity + plan_digest `f5cbcf0c…`): la ejecución física del G4 es la prueba de la cadena (ver G4-ECONOMICS).
