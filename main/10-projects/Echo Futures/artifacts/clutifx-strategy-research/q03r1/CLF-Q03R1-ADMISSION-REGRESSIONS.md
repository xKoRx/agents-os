# CLF-Q03-R1 — ADMISSION REGRESSIONS (tests negativos de admisión)

Fecha: 2026-10-26 · Suites: `test_qualification_admission.py` (28) · `test_qualification_guard.py` (14) · `test_session_compatibility.py` (7) · `test_research_lab.py` (75) · `test_campaign_lab.py` (31) · `test_s02_trials.py` (6) + `test_s02_trials_reconcile.py` (12) · Go clf `ok` · E2E reales: `guard-e2e-quarter.sh` + `qualification/guard-e2e.sh`.

Cada rechazo demuestra **cero motores lanzados**: stub con sentinel (nunca aparece) + sin `receipt.json` + `QUALIFICATION-BLOCKED.json` con causa exacta + exit 78 (bloqueo de política permanente). La única costura de spawn (`research_lab._run_one`) cubre `run` y `resume --execute`.

## Matriz del mandato → prueba

| # | caso | resultado | prueba |
|---|---|---|---|
| 1 | Estrategia que sólo compila (quarter sin cadena) | `RECEIPT_MISSING` | `test_10_quarter_without_qualification_blocked` + e2e real |
| 2 | ready=true, cero señales / señales sin órdenes / órdenes sin fills / entrada sin cierre | `G2C_NOT_FULL_TRADE` (campos) o `GATE_G2C_NOT_PASS` (estado) | `test_r1_quarter_without_full_trade_blocked`; recibos reales C06 |
| 3 | Sesión incompatible | `G2B_NOT_SESSION_COMPATIBLE` | `test_r1_quarter_with_session_incompatible_blocked`; recibos reales C01/C06 |
| 4 | G2C de otra variante | `IDENTITY_MISMATCH` | `test_r1_quarter_g2c_from_other_variant_blocked` |
| 5 | G2C con hash alterado | `RECEIPT_ARTIFACT_TAMPERED` | `test_r1_quarter_tampered_g2c_artifact_blocked` + guard suite ídem |
| 6 | G4 sin G2C PASS | `GATE_G2C_NOT_PASS` | cadena funcional obligatoria (admit_quarter y admit_historical) |
| 7 | G5 sin G4 PASS / cero challenges / no conciliado / <45 sesiones | `GATE_G4_NOT_PASS` / `G4_NO_PASS` / `G4_UNRECONCILED` / `SESSIONS_BELOW_MINIMUM` | tests 5–7 Q03 conservados + guard suite |
| 8 | Histórico mal etiquetado como trimestre | `PURPOSE_CONTRADICTS_EXECUTION_IDENTITY` | `test_r1_hist_mislabeled_as_quarter_blocked` |
| 9 | Horizonte multicontrato corto evadiendo clasificación | clasificado `HISTORICAL` por conjunto de contratos ⇒ `RECEIPT_MISSING` sin cadena G5 | `test_r1_short_multicontract_horizon_is_historical` |
| 10 | `resume --execute` sin recibos (histórico y quarter) | bloqueado en la misma costura | `test_9_resume_execute_cannot_bypass` (conservado) |
| 11 | Identidad duplicada heredando PASS / plan re-preparado / contratos falsos | `IDENTITY_MISMATCH` / `PLAN_DIGEST_MISMATCH` / `CONTRACT_SET_MISMATCH` (+`CONTRACT_SET_MISSING`) | tests r1 ídem + `test_r1_quarter_window_identity_mismatch_blocked` (`WINDOW_IDENTITY_MISMATCH`) |
| 12 | Campaña bit-idéntica (recibo que ya trae G4) ante la puerta quarter | `RECEIPT_NOT_A_QUALIFICATION_CHAIN` | aserto de `admit_quarter`; verificado en la validación con recibos reales |
| 13 | Propósito declarado contradictorio con el plan | `PURPOSE_CONTRADICTS_EXECUTION_IDENTITY` | `test_r1_quarter_wrong_purpose_blocked` |
| 14 | Clasificación de propósito (autoridad: registro sellado + contratos + horizonte) | `ROLLOVER_CANARY`/`LAST_CONTRACT`/`QUARTER`/`UNCLASSIFIED` | `test_r1_classify_purpose_registry_and_contract_authority` |
| 15 | Positivos | quarter con cadena completa e identidad sellada ⇒ `ADMITTED`; G5 con G4 PASS ⇒ admitido; quarter/short legacy sin regresión | `test_10b_valid_quarter_chain_admitted`, `test_2b…`, `test_11…`, `test_12_legacy_short_flow_no_regression` |

## Validación con recibos REALES del ciclo (sin stub, sin spawn)

`q03r1/validate_quarter_door.py` → `quarter-door-real-receipts.json`:

- **C02 → ADMITTED** (cadena G0..G3 + G2C PASS 4 round-trips, G2B SESSION_COMPATIBLE, identidad sellada NQU6).
- **C03 → ADMITTED** (ídem, 1 round-trip).
- **C06 → BLOCKED `G2B_NOT_SESSION_COMPATIBLE`** (veredicto INCONCLUSIVE_NO_SIGNALS; además G2C FAIL — la primera causa en la cadena es G2B).
- **C01 → BLOCKED `G2B_NOT_SESSION_COMPATIBLE`** (SESSION_INCOMPATIBLE, 2/2 señales fuera de ventana).

E2E real sobre el runner: quarter sin cualificación ⇒ `RECEIPT_MISSING`, exit 1 del batch (78 en `_run_one`), `0 motores` verificado por pgrep; histórico sin recibo ⇒ ídem.

## Nota de frontera (explícita, sin promesas falsas)

El guard protege la **vía de admisión autorizada** (`research_lab run/resume`). El binario del motor puede invocarse a mano (`platform-batch` directo) y esa superficie NO está cubierta por el guard de Python; la legitimidad de una corrida manual no puede declararse cualificada sin pasar por la costura. Esta frontera está declarada en la skill y el runbook (§7).
