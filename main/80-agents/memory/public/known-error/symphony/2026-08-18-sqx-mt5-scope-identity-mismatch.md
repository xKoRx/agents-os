---
type: known_error
schema_version: 1
scope: application
created: "2026-08-18"
updated: "2026-08-18"
area: "[[Echo]]"
project: "[[Echo Forge - Reconciliación y Scoring MT5]]"
application: "[[echo-forge]]"
entities:
  - "[[Echo Forge - Reconciliación y Scoring MT5]]"
  - "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
related:
  - "[[2026-08-18-echo-forge-mt5-fidelity-scope-bypass]]"
aliases:
  - XAUUSD_darwinex vs XAUUSD
  - h1 vs H1 fidelity
confidence: verified
source_session: 62c3bb1f-553c-4963-b25d-b9633df6c4a5
load_policy: when_error_matches
indexable: true
index_priority: high
tags:
  - kind/known-error
  - scope/application
  - app/echo-forge
  - tech/symphony
---

# SQX vs MT5 — identidad de instrument/timeframe/period no canónica

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Síntoma

- Score shadow `NOT_COMPARABLE` con `instrument_mismatch`, `timeframe_mismatch`, `scope_period_start_utc_missing:baseline`, `scope_period_end_utc_missing:baseline` aunque `config.json` declara `XAUUSD` / `H1`.

## Causa

- El predicado no lee `config.json`. Baseline SQX toma `trade.Instrument`/`trade.Timeframe` del NDJSON (`XAUUSD_darwinex`, `h1`) y deja periodo configured MISSING. Candidato MT5 toma Symbol/Period del HTM (`XAUUSD`, `H1`, julio 2026).
- Los tests unitarios construyen ambos lados ya iguales; no cubren esta procedencia.

## Impacto

- Sin mapeo, no hay Score comparable. Con el bypass de M6-NORMAL el comparador corre y produce `COMPUTED` numéricamente basura para calibración.

## Detección

- Mongo `forge.metric_sets`: baseline `instrument.text=XAUUSD_darwinex` / `timeframe.text=h1`; candidate `identity.instrument.text=XAUUSD` / `identity.timeframe.text=H1`.

## Mitigación

- Temporal: bypass TODO en `MT5FidelityComparabilityReasons` (commit `8f0cfa0`). Permanente: alias SQX connection→símbolo MT5, canonicalizar timeframe, periodo configured compartido; restaurar los 4 `textPair`.

## Evidencia

- Attempt 6: `sha256:91f0e903…` vs `sha256:8e4d06eb…`. Attempt 7: 13 Scores `COMPUTED` bajo bypass, p.ej. `sha256:f86b40e2…` value `17.1875` (net_profit 434.45 vs -224.9).
