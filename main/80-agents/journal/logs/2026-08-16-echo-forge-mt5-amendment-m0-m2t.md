---
type: change_log
schema_version: 1
scope: session
created: "2026-08-16"
updated: "2026-08-16"
area: "[[Echo]]"
project: "[[Echo Forge - Reconciliación y Scoring MT5]]"
application: "[[echo-forge]]"
entities:
  - "[[Echo Forge - Reconciliación y Scoring MT5]]"
  - "[[Echo Forge]]"
related:
  - "[[2026-08-16-echo-forge-mt5-m0-m2t]]"
aliases: []
confidence: verified
source_session:
source_feedbacks:
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# Echo Forge MT5 — Amendment owner M0–M2-TOP (micro-corrección TOP)

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated (repo + vault)
- **Archivo(s):**
  - Repo `xKoRx/symphony`: `specs/FEAT-SQX-MT5-RECONCILIATION-SCORING/{CORPUS,INVENTORY,METRIC-MATRIX,SPEC-PARSER,SPEC-NORMALIZATION,PLAN}.md` (`550bdb0`) y fila en `specs/SPECS.md` (`00a2d7f`); ambos pusheados, HEAD remoto verificado `00a2d7f`, status limpio.
  - Vault: [[Echo Forge - Reconciliación y Scoring MT5]] (estado/gates/tareas/bitácora), [[Echo Forge]] (estado/puente/bitácora), continuidad interna global, decisión [[2026-08-16-echo-forge-mt5-comparability-taxonomy]] (L3, materializada vía contract).

## Motivo

- Micro-corrección TOP del owner: no usar `NO_COMPARABLE` por falta de evidencia; investigar el lado SQX real antes de veredictos; corregir GP/GL, DD variantes, assembly, trade_key y PLAN antes de atomizar M2-NORMAL.

## Resolución aplicada

- Investigación SQX con código real: `EchoForgeOverviewExporter.overviewFromStats` exporta `StatsKey.*` y calcula `ret_dd = net/drawdown`; `PctDrawdown` existe en el engine y no se exporta; contract spec documenta Sharpe SQX anualizado.
- Taxonomía nueva aplicada fila a fila: COMPARABLE (net_profit, trades), COMPARABLE_CONDICIONAL (ret_dd↔Recovery Factor), PENDING_VERIFICATION (drawdown/max_dd_pct/sharpe/sqn NO_BINDING_IDENTIFIED_IN_HTM/profit_factor/win_rate/expectancy/stagnation/cagr/custom); sin NO_COMPARABLE (ninguna evidencia positiva de incompatibilidad).
- Contradicción GP/GL resuelta sin concluir basis (all-loss no distingue bases de PF); 4 variantes DD preservadas con nombres canónicos; assembly fail-closed solo 1in→1out; `trade_key` source-based sobre deal IDs; PLAN sin legacy projection desde v1 con consumer brownfield identificado (`deviation_activity.go`); proposal de scoring PENDING_OWNER abierta para M5-TOP.
- M0-NORMAL/M0-TOP/M1/M2-TOP `CLOSED`; M2-NORMAL `READY / NOT STARTED`. No se inició M2-NORMAL ni M3+; Foundation no se reabrió.
