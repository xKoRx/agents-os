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

# change_log — 2026-10-17 · Echo Futures THREE STRATEGIES V2.1 (cierre correctivo)

- **Repo `xKoRx/echo`** (fuera del vault): rama `experiment/tradesgerard-3strategies`
  @ `9bd6acf4` (fix `f56d9b33` + registro campaña). Tres correcciones: (1) el MM
  `STRATEGIC_ENTRY_BUDGET_V1` ya no pre-veta con `TG_ENTRY_BUDGET_EXCEEDS_HEADROOM`
  — propone el presupuesto objetivo y el RiskFinalizer resuelve diario/EOD sobre la
  propuesta real (7 tests E2E del recorrido, RED/GREEN −710/300); (2) la ventana
  interna de compra es el escenario del perfil (`NY_1000_OBS_V1` / `NY_RTH_0930`,
  fail-closed bajo la apertura oficial del provider); (3) adds de orb
  `EntrySameCycleOnly` tras auditoría forense del baseline (0 adds ejecutados; los
  intents morían en la ventana o se promovían a entradas fantasma).
- **Matriz V2.1**: 15/15 `COMPLETE_WITH_TRADES` reconciliadas (binario `f7822870`,
  run root `/srv/echo-work/runs/three-strategies-v21-20261017/`, baseline V2
  conservado en `three-strategies-20261016`). Suma caja − 5.000 = −10.800; B01/B02
  ejecutables por primera vez (compra 09:35/09:45 NY); ranking y diferencias vs
  baseline en `v3/backtester/tools/tradesgerard/three-strategies/RESULTS.md`.
- **Suite**: sólo los 5 `TestBTGS05_*` fallan (pre-existentes del base, verificado
  con stash en `0c6e9797`); sdk/operation/tgmm/orb/domain verdes.
- **Memoria ZCode** — `echo-futures-three-strategies-v2-state.md` actualizada al
  estado final V2.1.
