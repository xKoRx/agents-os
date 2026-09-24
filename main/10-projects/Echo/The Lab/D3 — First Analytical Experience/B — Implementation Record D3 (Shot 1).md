---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related: []
aliases: []
tags:
  - kind/doc
created: "2026-09-24"
updated: "2026-09-24"
---
related:
  - "[[A — Technical SPEC D3]]"
  - "[[C — Evidence D3 (Shot 1)]]"
  - "[[D — Debt Ledger D3]]"
  - "[[E — F4 Handoff D3]]"
aliases:
  - D3 implementation record
tags:
  - kind/doc
  - area/echo
  - the-lab
  - d3
---

# B — Implementation Record D3 (Shot 1)

## Identidad del candidate

- **Baseline:** `xKoRx/echo origin/master@8adce7ec98fc20517950635537e515e07c931144` (D1 integrado; verificado antes de editar). La branch exploratoria accidental `origin/feature/d3-lab-v3-curve-engine` fue detectada y EXCLUIDA como baseline: no continuada, no cherry-picked.
- **Branch:** `feature/d3-lab-v3-first-analytical` (publicada en origin, FF, sin merge a master).
- **Candidate SHA:** `6a111c9ec7c987fed885dfea82951256af12b6e1` (1 commit sobre el baseline).
- **Working tree:** limpio al cierre.

## SDD en repo

`specs/FEAT-THELAB-D3-CURVE-ENGINE/{SPEC,PLAN,TASKS}.md` + registro en `specs/SPECS.md` (estado `Verifying`). `VERIFICATION.md` pertenece al Shot 2 (verifier independiente) y NO se produce aquí.

## Archivos (mapa)

- Migración: `v3/sdk/postgres/migrations/065_lab_curves_v3.{up,down}.sql` (echo.lab_curves, echo.lab_curve_points, echo.lab_curve_metrics).
- Engine: `v3/sdk/analytics/curve/{curve,engine,algorithms,metrics}.go` (+ tests).
- Persistencia/servicio: `v3/sdk/postgres/{lab_curve_repository,lab_curve_service}.go` (+ `lab_curve_integration_test.go`).
- CLI: `v3/lab-worker/cmd/lab-worker/{main.go [case + runner],curves_parse.go,curves_parse_test.go}`; `v3/lab-worker/internal/builders/{recalculate_curves.go,recalculate_curves_test.go}`.
- Harness: `v3/sdk/postgres/tests/d3_curves/{run.sh,run_tests.sh}`.
- Hasura: `v3/hasura/metadata/tables/{lab_curves_v3,canonical_history_readonly}.yaml`.
- Front: `v3/front/src/services/graphql/strategyCurveV3.js` (+test), `src/views/lab/StrategyCurveV3TabContainer.vue` (+test), `src/components/lab/v3/{CurveV3Chart,CurveV3MetricCards,CurveV3TradesTable}.vue` (+2 tests), registro en `src/views/LabView.vue` + `src/lens/lensRegistry.js`.
- Modificaciones a existentes (justificadas): `v3/lab-worker/cmd/lab-worker/main.go` (sólo switch/runner), `LabView.vue`/`lensRegistry.js` (sólo registro del tab), `specs/SPECS.md` (registro) y `v3/sdk/postgres/tests/d1_foundation/run.sh` (fix de harness: el glob del rebuild comía migraciones >064 y las aplicaba fuera de transacción; acotado a ≤064, su contrato declarado).

## Migración

065 additive y determinista; no toca 061–064, journal, TradeSet (PG063) ni E10. Aplicada sólo a PostgreSQL desechable de pruebas (harness); NO aplicada a ninguna base real (mismo estándar que 064 en D1).

## Tests

- Engine/metrics (puros, sin PG): 15 tests con la lista obligatoria del shot.
- Integración PG (`TestLabCurve_*`): 12 tests de persistencia/read model con fixture vía `ReplaceHistory` (mecanismo correcto D1) y REFERENCE por SQL de prueba declarado (provenance FIXTURE).
- Builder smoke: 2 tests (job run SUCCEEDED + fallo con algoritmo inexistente).
- CLI parse: 2 tests.
- Front: 22 tests nuevos vitest (4 archivos); suite completa 55/55; `npm run build` OK.
- Detalle de comandos y resultados: [[C — Evidence D3 (Shot 1)]]
