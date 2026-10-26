# CLF-Q03-R1 — IMPLEMENTATION FIXES

Fecha: 2026-10-26 · Rama `experiment/clutifx-s01`: `978e1803` (base) → `a166ecb0` (corte de cualificación) → `e8c2e47e` (orden de causa-raíz G2B, post-cualificación) · Sin merge, sin LIVE.

## Principio aplicado

Resolver defectos **demostrados** sin modificar la intención económica de las estrategias. No se aceptó ningún fix que sólo eliminara filtros para aumentar operaciones. No hubo que modificar NINGÚN código Go de Strategy/detector/MM/Provider: el comportamiento del motor quedó demostrado correcto en las 27 corridas físicas (ver RCA).

## Defecto 1 — Admisión QUARTER sin cualificación propia (FASE 2 del mandato)

- **Reproducción rojo:** un plan QUARTER sin bloque `qualification` arrancaba motor (test `test_10_valid_quarter_job_runs` del ciclo Q03 lo exigía verde — era la política antigua).
- **Causa raíz:** la puerta de admisión sólo protegía la clase HISTORICAL; las campañas del trimestre podían consumir cómputo económico sin demostrar G0–G3 ni operación completa.
- **Cambio mínimo:** `qualification_guard.admit_quarter` (nuevo) + routing en `research_lab._run_one` (única costura de spawn). La cadena funcional exigida es G0/G1/G2A/G2B/G2C/G3 con veredicto de sesión `SESSION_COMPATIBLE` y G2C con ≥1 fill de entrada, ≥1 de salida y ≥1 round-trip reconciliado.
- **Regresión verde:** 28 tests de admisión (16→28), 14 del guard, 7 de sesión, 75 de research_lab, 31 de campaign_lab, 6+12 de s02_trials; suites Go clf `ok` (105 s). E2E real `guard-e2e-quarter.sh`: bloqueado con `RECEIPT_MISSING`, 0 motores.
- **SHA:** commit `a166ecb0`; binario R1 `3bee0fd2…`.

## Defecto 2 — Identidad de ejecución no sellada (etiquetas y duraciones como autoridad)

- **Reproducción rojo:** un job de horizonte histórico podía declarar `execution_purpose: QUARTER` (y en Q02, `tier` arbitrario) para intentar re-clasificarse.
- **Causa raíz:** el propósito efectivo no se derivaba del plan; el `contract_set` físico no participaba en la clasificación.
- **Cambio mínimo:** `research_lab.effective_execution_purpose` (ventana registrada + contratos físicos realmente leídos + horizonte) + `plan_contract_set` (filas acotadas del `source_read_plan`) + `plan_identity_digest` (JSON canónico del plan sin la declaración de cualificación) + verificación de identidad sellada en `admit_quarter` (`execution_purpose`, `contract_set`, `window_identity`, `plan_digest`). Contradicción ⇒ `PURPOSE_CONTRADICTS_EXECUTION_IDENTITY` antes de leer cualquier recibo.
- **Regresión verde:** casos adversariales del mandato: histórico etiquetado quarter ⇒ bloqueado; estudio multicontrato de 90 días ⇒ clasificado HISTORICAL y bloqueado sin cadena G5; plan re-preparado con otro digest ⇒ `PLAN_DIGEST_MISMATCH`; contratos declarados ≠ leídos ⇒ `CONTRACT_SET_MISMATCH`. Cada rechazo con prueba de cero spawn (sentinel).
- **SHA:** ídem `a166ecb0`.

## Defecto 3 — Construcción de planes R1 (dos costuras de fan-out, corregidas en el driver)

- **Reproducción rojo:** 26 corridas fallaron `exit=2` ("strategy … has no fan-out target set") y luego ("fan-out references … which the account does not declare").
- **Causa raíz:** el template sellado del smoke NQZ6 lleva `fanout_targets` y `accounts[].account_strategy_ids` ligados al id de la estrategia del template; el swap de identidad debe re-asociar ambas costuras (lección conocida de Q03 intento3).
- **Cambio mínimo:** `q03r1/build_r1_specs.py` re-asocia `fanout_targets` (clave + `account_strategy_id`) y `accounts[].account_strategy_ids` al id del candidato.
- **Regresión verde:** 27/27 corridas `exit=0` COMPLETE+reconciled. Intentos fallidos preservados con causa (`-intento1-fanout`, `-intento2-accountids`), jamás sobrescritos.
- **SHA:** driver en run root (`q03r1/`), sin cambios en el repo del motor.

## Correcciones NO hechas (con motivo)

- **C01/C04/S01/S02/S17 (sesión):** no se movió ninguna ancla horaria. La incompatibilidad es estructura del curso vs ventana de la cuenta; la adaptación sería identidad nueva autorizada (fichas KRR-001/002/004).
- **C06/S15/T04 (0 setups):** no se aflojó ninguna conjunción del detector para fabricar señales (KRR-003).
- **T02:** no se inventó el ancho de stop (KRR-005).
- **Campañas NQU6 existentes:** ninguna re-ejecutada; sus recibos quedan como evidencia.

## Estado de FASE 6

Cero defectos de Strategy/detector/MM/ejecución demostrados en R1; las correcciones entregadas son de la **malla de admisión y construcción** (lo que el mandato llama a corregir). Cero regresiones nuevas atribuibles a los cambios: todas las suites verdes antes y después; el comportamiento del motor es byte-idéntico al corte Q03 (sólo cambió tooling Python).
