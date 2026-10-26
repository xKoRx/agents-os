# CLF-Q03 — ADMISION TESTS (guard y gates de admisión)

Fecha: 2026-10-25 · Suites: `campaign-lab/test_qualification_admission.py` (16) + `test_qualification_guard.py` (14) + e2e `qualification/guard-e2e.sh`

## Regresión positiva y negativa del bypass histórico

Ver `CLF-Q03-ROOT-CAUSE-QUALIFICATION-BYPASS.md` §3: los 12 casos del mandato + 4 complementarios, todos con prueba mecánica de **cero procesos de motor lanzados** (sentinel del stub) y recibo `QUALIFICATION-BLOCKED.json` con la causa exacta. `run` y `resume --execute` comparten la única costura (`_run_one`) — sin ruta alternativa de spawn.

## E2E de admisión real (sin stub)

`guard-e2e.sh` sobre el runner real: job histórico sin recibo → `QUALIFICATION-BLOCKED HIST-UNQUALIFIED: RECEIPT_MISSING`, exit 1, `0 motores`. El fixture usa las fechas HIST selladas (`2023-10-02→2026-10-06`) tras el cambio de política (antes bloqueaba por spec ilegible — también fail-closed).

## Verificación de la cadena completa con recibos reales Q03

Los recibos G0–G4 de las tres identidades nuevas (sellados en `q03/receipts/`) fueron pasados por el guard:

```
admit_historical(C03 recibo íntegro, G0–G4 completos, reconcilado, 60 sesiones)
→ BLOCKED_QUALIFICATION_GATE / G4_NO_PASS {passed: 0, purchased: 1}
```

Es la primera vez que la cadena completa (runner → guard → recibos sellados del mismo ciclo) se verifica de extremo a extremo con recibos REALES: el gate bloquea el histórico exactamente cuando el trimestre no produjo `CHALLENGE_PASSED`, sin intervención manual.

## Suites del repositorio (sin regresión)

| suite | tests | estado |
|---|---|---|
| `test_qualification_admission.py` (nueva) | 16 | OK |
| `test_qualification_guard.py` | 14 | OK |
| `test_research_lab.py` | 75 | OK |
| `test_campaign_lab.py` | 31 | OK |
| `test_s02_trials.py` + `test_s02_trials_reconcile.py` | 6 + 12 | OK |
| `test_session_compatibility.py` (nueva) | 7 | OK |
| Go `v3/sdk/futures/strategies/clf` (+detectors) | suite completa | OK (~111s + ~63s) |

Fallos preexistentes: los 17 fallos + 1 hang de la suite Go general `v3/backtester` clasificados preexistentes por A/B en Q02 (baseline `a7e00a8e`) NO se tocaron; ningún test nuevo depende de ellos y ningún fallo nuevo fue introducido (suites del paquete clf y campaign-lab verdes antes y después).
