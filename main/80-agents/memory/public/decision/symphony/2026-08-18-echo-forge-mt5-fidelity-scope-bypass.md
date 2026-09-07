---
type: decision
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
  - "[[2026-08-18-sqx-mt5-scope-identity-mismatch]]"
  - "[[2026-08-16-echo-forge-mt5-comparability-taxonomy]]"
aliases:
  - M6-NORMAL scope bypass
  - fidelity instrument timeframe period TODO
confidence: verified
source_session: 62c3bb1f-553c-4963-b25d-b9633df6c4a5
load_policy: when_application_loaded
indexable: true
index_priority: high
tags:
  - kind/decision
  - scope/application
  - app/echo-forge
  - area/echo
  - project/echo-forge
---

# Echo Forge MT5 — Bypass temporal de instrument/timeframe/period

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Contexto

- M6-NORMAL Attempt 6 recorrió parser/reconcile/score sobre Durable Foundation y persistió Scores `NOT_COMPARABLE` por `instrument_mismatch`, `timeframe_mismatch` y periodo configured ausente en el baseline SQX.
- El owner pidió comentar esas 4 puertas con TODO para ejercitar el comparador y volver al corte de arquitectura sin atribuir un falso verde al refactor.

## Decisión

- En `sqx/core/evaluation/mt5_fidelity.go` (`MT5FidelityComparabilityReasons`, commit `8f0cfa0`) quedan comentados los `textPair` de `instrument`, `timeframe`, `period_start_utc` y `period_end_utc`.
- Attempt 7 (`0.2.53`) es un checkpoint para probar el comparador: 13 Scores `COMPUTED`. No cierra M6-NORMAL. Esos valores no son evidencia comparable ni input de calibración.
- Restaurar las 4 puertas es trabajo del corte de arquitectura, junto con alias SQX connection↔símbolo MT5 y un periodo configured compartido. M6-NORMAL, M6-TOP y M7 siguen abiertos.

## Rationale

- Sin el bypass el comparador no llega a `net_profit`/`trades` reales. Con el bypass se prueba el algoritmo, no la comparability.

## Consecuencias

- Cualquier Score `COMPUTED` de `0.2.53` / `m6-shadow-20260818-007` es manzanas vs peras.
- El TODO en código es deuda explícita; no silenciarlo ni copiar `config.json` sobre ambos scopes.

## Alternativas descartadas

- Inferir periodo SQX desde first/last trade (prohibido por contrato).
- Copiar `config.instrument` a ambos lados (esconde `XAUUSD_darwinex`).
- Apagar todo el predicado, incluidas `pnl_basis` y `sample_type`.
