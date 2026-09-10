---
type: known_error
scope: application
created: "2026-08-10"
updated: "2026-08-10"
area: "[[Symphony]]"
project: "[[Echo Forge]]"
application: "[[echo-forge]]"
entities:
  - "[[Symphony]]"
  - "[[Echo Forge]]"
related:
  - "[[sqx-import-metadata-silent-fallback]]"
aliases:
  - apply_selected_run metadatos no encontrados run_id
  - databank_metadata cross-run wave test
confidence: high
source_session: "echo-forge-apply-selected-run-1786323448"
load_policy: when_error_matches
indexable: true
index_priority: high
tags:
  - app/echo-forge
  - area/symphony
  - kind/known-error
  - project/echo-forge
  - scope/application
---

# `apply_selected_run` falla por metadata de otro `run_id` en la misma wave

## Síntoma

- Temporal: `apply_selected_run` reintenta sin fin con
  `metadatos no encontrados para estrategia <id> en wave test`.
- Otras strategies del mismo workflow sí llegan a `APPLIED`.

## Causa

`LoadAllStrategyMetrics` filtra `databank_metadata` por `wave_key` **y** `run_id` (= request_id). Al reusar `wave=test`, quedan strategies seleccionadas (p.ej. `.z0`) cuya metadata solo existe bajo un `run_id` anterior; el run actual importó otro conjunto (p.ej. solo `.h0`).

## Detección

```text
selected_robust_runs.run_id = <actual>
databank_metadata: strategy_id existe pero run_id distinto
```

Ref: workflow `sqx-main-00_configs-v1-XAUUSD-H1-L-1786323448`, run `a68c4237…`, metadata vieja `4d04c8cf…` (flow_75).

## Mitigación

- Operativo: backfill upsert de metadata al `run_id` actual, o cancelar el workflow.
- Estructural: no reusar wave con leftovers; o fallar en select si falta metadata del mismo `run_id`; evitar retry infinito.
