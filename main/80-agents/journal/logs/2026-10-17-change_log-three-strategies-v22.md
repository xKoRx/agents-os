---
created: "2026-10-17"
updated: "2026-10-17"
area: "[[Aranea]]"
project: "[[Echo Futures]]"
entities:
  - "[[Echo Futures]]"
related: []
aliases: []
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# change_log — 2026-10-17 · Echo Futures THREE STRATEGIES V2.2 (cierre técnico)

- **Repo `xKoRx/echo`** (fuera del vault): rama `experiment/tradesgerard-3strategies`
  @ `3f63944a` (base V2.1 `9bd6acf4`, SIN merge a master ni cambios al runtime).
  Cuatro correcciones con evidencia: (1) el gate diario de Campaign
  (`entryBudgetCapacity`) ya no pausa preventivamente cuando la sala diaria no
  cabe R_op — la pausa queda para el único caso propio de la campaña (no cabe
  una entrada físicamente representable, mínimo ejecutable 24,98 en NQ) y
  elimina el literal 1000 duplicado (consume `internal_pause_loss`
  configurado) publicando `daily_capacity`/`internal_pause_loss`/
  `daily_pause_threshold`; las autoridades permanentes (margen EOD bajo R_ref)
  y el control EOD quedan intactos; (2) el RiskFinalizer reemplaza la escalera
  first-fit por la búsqueda de la MEJOR combinación legal cantidad×distancia
  (clases `QTY_REDUCTION`/`SL_TIGHTEN`/`RISK_ALIGN` + `rf_unused_budget`,
  nunca ensancha el stop, piso 1 tick, empates conservan la geometría); (3) el
  exportador de traza económica (`searchEconomicEvent`) incluye los
  `ProviderDecisionFact` — la causa de una denegación del provider ya no es
  invisible; (4) ranking caja DESCENDENTE con identidad por campaña (pases,
  cobros, entradas vs ADDs con fill, ajustes del finalizador, variantes de
  configuración con trayectoria idéntica agrupadas) y total DESCRIPTIVO
  (`generate.py report`).
- **Defecto bloqueante reproducido y cerrado (mandato §2)**: el caso −710/300
  en V2.1 moría en `DAILY_CAPACITY_BELOW_ENTRY_BUDGET` (pausa preventiva con
  290 de sala) y el finalizador jamás participó en corpus (0 cortes). Bajo
  V2.2 el recorrido COMPLETO señal→Campaign→MM real→finalizador→Provider→fill
  está bloqueado por tests: −400/−710 llenan con `PASSTHROUGH` del
  finalizador; −970 produce el mejor candidato legal (no el primer corte);
  −1000 pausa Y el finalizador rechaza `RF_DAILY_BUDGET_EXHAUSTED` sin
  órdenes; la pérdida permanente sigue siendo veredicto separado.
- **Causa exacta de la denegación histórica del ADD (mandato §4)**: C04 ciclo
  22 (2025-10-28 13:56:08Z), decision `prd:btg-functional:00000142` →
  `PHYSICAL_STATE_UNTRUSTED` ("candidate enlarges the reachable envelope",
  guard D4-A2 §8); el replay determinista bajo V2.2 reprodujo el MISMO
  decision_id con el hecho exportado. Hipótesis descartadas con evidencia:
  no era WINDOW_CLOSED (la orden pasó admisión stage-1) ni EXPOSURE_CAP
  (envelope corto G=2 ≤ cap 2 en el caso SHORT histórico).
- **ADD demostrado con fill (fixture determinista
  `platform_orb_add_fixture_test.go`)**: orb REAL + tgmm `ADVERSE_RETRACE` +
  Provider real + venue — señal `SAME_CYCLE_ONLY` del ciclo vivo, UN add del
  MM, admisión bajo capacidad válida, **orden ADD con fill**, promedio
  recalculado, protección reemplazada cubriendo toda la exposición con
  presupuestos congelados 500/250, y pérdida neta realizada del ciclo ≥ −500
  al cruzar el stop recalculado. Gemelo negativo: capacidad histórica (base
  cap 2) → `RESERVATION_DENIED` con causa `EXPOSURE_CAP` ("GROSS
  scope=account-wide cap=2 reachable=4"), sin fill, protección previa WORKING
  intacta, sin entrada fantasma. En corpus los adds siguen SIN oportunidad
  ejecutable (0 con fill): **funcionalidad probada sintéticamente, efecto
  económico histórico NO EXERCISED** (declarado).
- **Matriz V2.2**: 15/15 `COMPLETE_WITH_TRADES` reconciliadas (binario
  `c52a9fec`, run root `/srv/echo-work/runs/three-strategies-v22-20261017/`).
  Total descriptivo **−10.320** (V2.1: −10.800): A05 −1.440→−1.200 (+240; 20
  ajustes RF, 2 compras sucesoras menos), A03/A04 −2.760→−2.640 (+120 c/u;
  44 ajustes RF, 1 compra menos); 11 variantes idénticas (determinismo vs
  V2.1). **64 ajustes efectivos del finalizador en corpus (V2.1: 0)**. 0
  cobros (el retiro 2300/3000 no ejerció efecto; variantes agrupadas por
  trayectoria idéntica). Ranking en `RESULTS.md`; V2.1 conservado en
  `RESULTS-V21-BASELINE-f56d9b33.md`.
- **Familia B (limitación documentada)**: una entrada diaria con TP 300 no
  puede producir 900 en el día bajo operación nominal; evaluable como
  acumulación de días positivos, NO validación del patrón 3×900.
- **Suite**: tgmm verde; backtester con los 5 `TestBTGS05_*` pre-existentes
  del base `9bd6acf4` (re-verificado con stash cycle en esta sesión);
  operation/provider verdes. Prohibición mantenida: sin declaración de
  validación completa de las tres estrategias (el add sigue sin fill en
  corpus) y sin LIVE.
- **Memoria ZCode** — `echo-futures-three-strategies-v22-state.md` actualizada
  al estado final V2.2.
