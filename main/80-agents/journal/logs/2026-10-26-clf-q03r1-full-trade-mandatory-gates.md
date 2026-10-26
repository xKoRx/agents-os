---
type: change_log
schema_version: 1
scope: session
created: "2026-10-26"
updated: "2026-10-26"
area: "[[Echo]]"
project: "[[Echo Futures — Optimización de Campañas]]"
application:
entities: ["[[Echo Futures]]"]
related: []
aliases: []
confidence: verified
source_session:
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-10-26-clf-q03r1-full-trade-mandatory-gates

## Cambio

- **Tipo:** created / updated
- **Archivo(s):**
  - `xKoRx/echo` @ `experiment/clutifx-s01` `978e1803`→`a166ecb0`→`e8c2e47e` (push con readback): `campaign-lab/qualification_guard.py` (cadena funcional G0/G1/G2A/G2B/G2C/G3 obligatoria en ambas puertas; `admit_quarter` nueva con identidad de ejecución sellada y rechazo de campañas bit-idénticas), `campaign-lab/research_lab.py` (`effective_execution_purpose`, `plan_contract_set`, `plan_identity_digest`, registro de ventanas con `purpose`+`contracts`, routing QUARTER en la única costura de spawn), `campaign-lab/qualification_ledger.py` (nuevo: evidencia física read-only con round-trips posición-a-posición), `test_qualification_admission.py` (16→28), `test_qualification_guard.py` (recibos con split G2).
  - Vault: `30-resources/agents/skills/echo-retester-master/SKILL.md` + `30-resources/runbooks/echo-futures-strategy-qualification-runbook.md` (delta: G2A/B/C, puerta quarter, propósito de ejecución, Knowledge Review Loop, matriz de tests negativos, frontera del guard); planner de [[Echo Futures — Optimización de Campañas]] por delta; 12 entregables `CLF-Q03R1-*` espejados en `10-projects/Echo Futures/artifacts/clutifx-strategy-research/q03r1/` con checksums; agent-run y feedback del ciclo.

## Motivo

- Mandato Owner CLF-Q03-R1: ninguna variante puede declararse validada sin una operación completa real y conciliada en el último contrato (G2C), ninguna campaña trimestral puede arrancar sin su propia cadena funcional + identidad de ejecución sellada, ninguna variante no operativa puede quedarse sin diagnóstico causal, y las dudas de fuente deben volverse fichas de conocimiento con pregunta concreta al Owner.

## Fuentes usadas

- Mandato CLF-Q03-R1; skill `echo-retester-master` + runbook (corte Q03); matriz CLUTIFX-EXPERIMENT-MATRIX v1.0; recibos físicos de `~/echo-work/clutifx-backtest/{qualification,q02,q03}` (81 intentos censados); corpus NQZ6/NQU6 (`~/echo-work/data/corpus/`); CLAIMS.md del knowledge library Clutifx (timestamps por claim).

## Resolución aplicada

- G2C como gate físico: ≥1 fill de entrada + ≥1 fill de salida + ≥1 round-trip reconstruido desde los fills reales; 19/27 identidades lo lograron en NQZ6; las demás con clasificación causal persistente (nunca `COMPLETE` vacío).
- Puerta quarter fail-closed por identidad de ejecución sellada (propósito/contratos/ventana/plan_digest) derivada del plan, no de etiquetas del job; propósito contradictorio, plan re-preparado, contratos falsos y recibos ajenos bloquean antes del spawn; campañas bit-idénticas no re-ejecutables.
- Veredicto final único por ID (34 filas) con gates y clasificación como dimensiones separadas; G5 elegible = ∅ (0 CHALLENGE_PASSED); Knowledge Review Loop con 7 fichas KRR sin modificar el conocimiento fuente.

## Validación

28+14+7+75+31+6+12 tests python verdes; suites Go clf `ok` (105 s) en el corte R1; e2e reales con 0 motores; 27/27 corridas físicas NQZ6 COMPLETE+reconciled (binario `3bee0fd2…`@`a166ecb0`); `admit_quarter` validado con recibos REALES del ciclo (C02/C03 admitidas, C01/C06 bloqueadas por G2B); máx 5 motores, MemAvailable mín ~4,0 GiB, swap 0 B, 0 OOM, 0 huérfanos.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales de terceros, memoria interna ni secretos (los paths del run root de Hefesto son la referencia física declarada del proyecto)

## Rollback

- Revertir `e8c2e47e` (sólo orden de causa) y `a166ecb0` (puerta quarter + propósito efectivo) en el repo; la política previa (sólo guard histórico por etiqueta) vuelve con sus bypass conocidos. Los recibos y entregables R1 quedan como evidencia histórica y no dependen del rollback.
