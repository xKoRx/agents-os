---
type: agent_memory
schema_version: 1
scope: project
created: "2026-09-05"
updated: "2026-09-05"
area: "[[Echo Forge]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[xKoRx/symphony]]"
entities: []
related: []
aliases: []
confidence: high
memory_state: active
continuity_key: echo-forge/full-golden-flow-2026-09-05
supersedes:
superseded_by:
load_policy: when_echo_forge_loaded
indexable: false
index_priority: never
tags:
  - kind/agent-memory
  - scope/project
---

# Echo Forge FULL golden flow — 2026-09-05 checkpoint

## Continuidad

- Autoridades: source `3b0737c1efe153f1f72eec40465fd1aa883887d0`, SDK `c85594440f6755443ceb97ec4e333cd0ddb5b0ed`, release `0.2.96`, MT5 build `6180`.
- CFX TEST/GOLDEN: builder `fd5ffebe9af9b012c50a06ca0c35be1fa612e935bd8e130061e82b5b2329f185` (MaxStrategies 20); optimizer `121ec05ebb1b4ca0be1d3e427de6ca2c0f6ec272c7ec336447ecae6315c1ffed`; retester/reretester `1a993957abd89a8f65d9fb856c5eb5b3bf08ee39ddce1b484da18f54b3f9577f`.
- Ambos FULL usaron periodo `2016-01-04→2026-06-05`, H1/XAUUSD, sample FULL y wiring SQX_NATIVE→MT5_NATIVE; sin Campaign wrapper ni deltas de certificación.
- Run 1 `8088ef7c-6e49-4ce6-a5ac-b8b6b0fbe90a`: 20→17→12→12→3→3→3; 3 MT5 `backtest_timeout`; Result Surface `COMPLETED`, ranking `NOT_MATERIALIZED`, promotion `AVAILABLE`, finalists 0.
- Run 2 `162e7878-5b80-487f-bd5e-d0e7cde3a3a7`: 20→15→9→9→3→3→3; los 3 compile children completaron en MT5 6180 y los 3 backtests terminaron `backtest_timeout`. Sin HTM/parser/reconcile/Score; ranking final no materializado.

## Señales de carga

- El cero de Campaign previo se explica por MT5 lean `2026-05-04→2026-06-05` frente a baseline `2016-01-04→2026-06-05`, produciendo `NOT_COMPARABLE/period_start_utc_mismatch`; no existe threshold de finalist.
- Ambos FULL fueron semánticamente correctos hasta MT5 pero cayeron en timeout físico; no es filtro WFM ni comparabilidad. Se agotó el máximo de dos runs; no se autoriza tercer run.

## Checkpoint agregado — TradeSet baseline durability preflight (2026-09-06)

- Veredicto `PASS / CLOSED`: source y runtime de release `0.2.96` consumen `BaselineTradeSetRef` durable (`trade_sets` + MinIO) en `MT5ScoreShadowActivity`; no hay inyección activa de `ReretesterBaselineReader` legacy.
- Los seis carriers de los dos FULL runs tienen `TradeSetRef` SHA256 no vacío y exacto; los seis TradeSets existen una vez, con lineage exacto, scope `tick_retest/optimized/FULL/non-cell`, payload íntegro y decode/count/net_profit válido. `trade_lists` exact-scope = 0 en ambos runs: `LEGACY_BROWNFIELD_SURFACE_NOT_REQUIRED`.
- “3 TradeSets / 0 docs” no es defecto de producto. El lado baseline SQX habría estado listo para los seis candidatos; MT5/reconcile/Score no se ejecutaron. Próximo exacto: `ECHO-FORGE-V2-IMPLEMENTATION-PLAN-RETURN-TO-LEAD`.

## Próxima acción

- La sesión FULL queda cerrada. El blocker físico quedó arquitecturado en [[2026-09-06-echo-forge-mt5-execution-model-v2]]. Finalist Model V2 TOP cerró en [[2026-09-06-echo-forge-finalist-model-v2]]. No tercer golden hasta slots + Finalist V2 implementados y certificados. NEXT EXACT de programa: `ECHO-FORGE-TRADELIST-BASELINE-DURABILITY-PREFLIGHT`.
