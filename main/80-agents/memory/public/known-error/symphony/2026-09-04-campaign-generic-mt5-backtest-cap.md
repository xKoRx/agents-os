---
type: known_error
schema_version: 1
scope: application
created: "2026-09-04"
updated: "2026-09-04"
area: "[[Echo]]"
project: "[[Echo Forge]]"
application: "[[xKoRx/symphony]]"
entities: []
related:
  - "[[2026-09-04-echo-forge-campaign-generic-mt5-backtest-hard-cap]]"
aliases:
  - CAMPAIGN_GENERIC_MT5_BACKTEST_CAP_NOT_ENFORCED
  - campaign generic mt5 backtest hard cap
confidence: verified
source_session: "ECHO-FORGE-CAMPAIGN-GENERIC-MT5-BACKTEST-HARD-CAP-V1-NORMAL"
load_policy: when_error_matches
indexable: true
index_priority: high
tags:
  - kind/known-error
  - scope/application
  - application/symphony
  - area/echo
  - tech/go
---

# CAMPAIGN_GENERIC_MT5_BACKTEST_CAP_NOT_ENFORCED

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Síntoma

- En una ola Campaign, el plan de backtest podía contener cinco ejecuciones y el quinto MT5BacktestArtifactWorkflow llegaba a materializarse antes de que la certificación externa cancelara el Generic.

## Causa

- `executeMT5ArtifactTask` conocía el plan exacto después de resolver las fuentes, pero no tenía una compuerta cardinality gate antes de `workflow.ExecuteChildWorkflow`; el fan-out completo se materializaba sin consultar el contexto tipado `ForgeCampaignWave`.

## Impacto

- La violación ocurría dentro del límite físico de MT5 Backtest y terminaba la campaña como `WAVE_FLOW_RUN_CANCELLED`, aunque el suministro nuevo de Wave2 y Replenishment ya habían sido probados correctamente.

## Detección

- La evidencia de 0.2.94 mostró cinco backtests planificados/materializados frente al máximo físico cuatro; el escenario H5 posterior confirma error preflight y cero child workflows materializados.

## Mitigación

- El producto define una única autoridad `MaxCampaignMT5BacktestChildrenPerGeneric = 4` y valida sólo ejecuciones de backtest con `req.Spec.ForgeCampaignWave != nil`; si el plan completo supera cuatro, devuelve error determinista antes del primer `ExecuteChildWorkflow`.

## Evidencia

- Corregido en commit `0f18ef0` y publicado en `origin/master`; H1-H12 dirigidos pasan, incluidos H4 con cuatro children y H5 con cero. Los fallos de la suite amplia se clasificaron como baseline no relacionados.
