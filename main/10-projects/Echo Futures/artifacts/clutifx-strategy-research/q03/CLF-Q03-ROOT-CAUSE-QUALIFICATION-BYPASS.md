# CLF-Q03 — ROOT CAUSE: QUALIFICATION BYPASS (FASE 1)

Fecha: 2026-10-25 · Rama `experiment/clutifx-s01` · Base `c127b894` → Fix `2ee3f7fc` (+`fb950d68` higiene)
Archivo: `v3/backtester/tools/tradesgerard/campaign-lab/research_lab.py`

## 1. Causa raíz confirmada

El guard de admisión histórica (commit `a7e00a8e`, Q02) se invocaba únicamente cuando el PROPIO job declaraba su tier:

```python
qual = item.get("qualification") or {}
if qual.get("tier") == "G5":   # ← el requisito dependía de la etiqueta del propio job
    qualification_guard.admit_historical(...)
```

Un job histórico de investigación de una estrategia nueva que OMITIERA `qualification` (o la clave `tier`) saltaba el control completo. Peor: un job de horizonte histórico podía declarar `tier: "G2"` y quedar exento por diseño. La necesidad de cualificación no puede depender de una etiqueta opcional enviada por el interesado — defecto de seguridad del flujo de investigación, confirmado por lectura del código y por los planes Q02 (los planes del ciclo Q02 no declaraban `qualification` en absoluto: `qualification: null` verificado en `plan-Q02-S03-G2.json`).

## 2. Corrección: clase de ejecución efectiva desde la identidad del plan

Nuevo en `research_lab.py` (aplicado en `_run_one`, la ÚNICA costura de spawn, cubriendo `run` y `resume --execute`):

1. `effective_execution_class(spec, lab_job)` clasifica cada plan por su identidad temporal REAL:
   - `HISTORICAL`: ventana sellada `HIST-*` o horizonte económico (`trade_start..end_exclusive`) > 120 días (un contrato físico NQ abarca ~un trimestre; un horizonte mayor es histórico).
   - `QUARTER`: 45–120 días (contrato único).
   - `SHORT`: < 45 días (smoke/canario).
   - `UNCLASSIFIED`: fechas ilegibles → bloqueado (fail closed).
2. Para todo job `HISTORICAL`:
   - Ausencia de `qualification` → `RECEIPT_MISSING` (bloqueado).
   - Ausencia de `tier` → clasificado sin ambigüedad como histórico cualificable por la autoridad del plan (la ventana) y el recibo decide.
   - Tier declarado ≠ `G5` → `TIER_CONTRADICTION_EXECUTION_CLASS`: un job de horizonte histórico no puede auto-degradarse.
   - Identidad/digests/recibo en desacuerdo → razones exactas del guard (`IDENTITY_MISMATCH`, `GATE_G4_NOT_PASS`, `G4_NO_PASS`, `SESSIONS_BELOW_MINIMUM`, `QUARTER_DATASET_MISMATCH`, …).
   - Plan ilegible → `EXECUTION_CLASS_UNCLASSIFIED`.
3. El bloqueo ocurre ANTES del `subprocess`, escribe `QUALIFICATION-BLOCKED.json` con causa exacta y retorna 78 (bloqueo de política permanente, nunca reintentable).
4. Flujos legacy legítimos sin regresión: los planes `QUARTER` y `SHORT` (los gates G2/G3/G4 que PRODUCEN los recibos) no exigen recibo; el driver R03 y el resto de herramientas no pasan por esta costura.

El código del runner impide automáticamente repetir el bypass: no existe ruta de spawn que no pase por `_run_one`.

## 3. Pruebas adversariales (todas con prueba de CERO spawn)

Suite nueva `campaign-lab/test_qualification_admission.py` — 16 tests, motor stub que deja un SENTINEL al invocarse; cada rechazo demuestra que el sentinel nunca aparece y que no se escribió `receipt.json`:

| # | Caso | Razón esperada | Resultado |
|---|---|---|---|
| 1 | Histórico sin `qualification` | `RECEIPT_MISSING` | BLOQUEADO, 0 spawn |
| 2 | Histórico sin `tier` y sin recibo | `RECEIPT_MISSING` | BLOQUEADO, 0 spawn |
| 2b | Histórico sin `tier` con recibo íntegro | — | ADMITIDO (clasificado por autoridad del plan) |
| 3 | Histórico con tier falso `G2` | `TIER_CONTRADICTS_EXECUTION_CLASS` | BLOQUEADO, 0 spawn |
| 4 | Histórico que cambia la identidad de variante | `IDENTITY_MISMATCH` | BLOQUEADO, 0 spawn |
| 5 | Histórico con G4 ≠ PASS | `GATE_G4_NOT_PASS` | BLOQUEADO, 0 spawn |
| 6 | Histórico con 0 aprobaciones | `G4_NO_PASS` | BLOQUEADO, 0 spawn |
| 7 | Histórico con 10 sesiones elegibles | `SESSIONS_BELOW_MINIMUM` | BLOQUEADO, 0 spawn |
| 8 | Histórico con digest de dataset alterado | `QUARTER_DATASET_MISMATCH` | BLOQUEADO, 0 spawn |
| 9 | `resume --execute` sin recibo | `RECEIPT_MISSING` | BLOQUEADO, 0 spawn |
| 10 | Job `QUARTER` válido (91 días) | — | EJECUTA sus gates |
| 11 | Job `G5` válido con recibo íntegro | — | ADMITIDO en prueba sin ejecutar histórico real (stub) |
| 12 | Flujo legacy `SHORT` sin regresión | — | EJECUTA |
| + | Clasificación de clase efectiva (unit) | — | 100% |
| + | Spec ilegible | `EXECUTION_CLASS_UNCLASSIFIED` | BLOQUEADO, 0 spawn |

E2E de admisión real (`qualification/guard-e2e.sh`, actualizado a fechas HIST selladas): `RECEIPT_MISSING`, exit 1 del runner, `0 motores (nunca spawn)`.

## 4. Regresión

Suites existentes en el mismo directorio tras el cambio: `test_qualification_guard` 14/14, `test_research_lab` 75/75, `test_campaign_lab` 31/31, `test_s02_trials` 6/6, `test_s02_trials_reconcile` 12/12 — OK. Sin cambios de política para los flujos fuera de alcance; R03 intacto.
