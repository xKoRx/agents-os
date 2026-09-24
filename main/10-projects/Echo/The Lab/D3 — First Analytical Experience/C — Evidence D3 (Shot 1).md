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
  - D3 evidence
tags:
  - kind/doc
  - area/echo
  - the-lab
  - d3
---

# C — Evidence D3 (Shot 1)

Evidencia separada por provenance. Comandos ejecutados sobre worktree `/home/kor/aranea/work/d3-lab-f3-shot1-20260924/echo` (branch `feature/d3-lab-v3-first-analytical`, candidate `6a111c9e`).

## SOURCE (código/contrato, sin PG)

- `go test ./v3/sdk/analytics/curve/ -count=1` → `ok` (15 tests: empty input, one op, many ops, same timestamp, order independence, config⇒identity, dataset⇒fingerprint, missing risk, R_PIPS insuficiente, basis separation, exactitud decimal half-even, determinismo, períodos por opened_at, REFERENCE sin B ⇒ ERROR, algoritmo inexistente ⇒ error).
- `GOWORK=off go test ./...` en `v3/sdk/contracts` → `ok` (3 paquetes).
- `go test ./v3/sdk/analytics/formulas/` → `ok`.
- `gofmt -l` limpio en archivos nuevos; `go vet` limpio en paquetes afectados.

## FIXTURE (PG desechable real, schema 000+001..065 reconstruido)

- `bash v3/sdk/postgres/tests/d3_curves/run.sh` → probe BEGIN+065+ROLLBACK sin residuos, apply estricto + segunda pasada idempotente, objetos verificados (`lab_curves=1 lab_curve_points=1 lab_curve_metrics=1 uq_curve_identity=1`).
- `DATABASE_URL=… go test ./v3/sdk/postgres/ -count=1` → paquete completo `ok` salvo `TestScratch_QueryDB` — preexistente y demostrado en el baseline limpio `8adce7ec` con la misma DATABASE_URL (connStr versionado, defecto conocido). Incluye `TestLabCurve_*` 12/12: create+read, recálculo idéntico (mismo result_digest, cero duplicados), recálculo tras cambio de dataset (dataset_digest nuevo, reemplazo completo), REFERENCE añadido ⇒ stale→recompute, fallo inyectado post-publicación ⇒ rollback con materialización anterior íntegra, trazabilidad punto→operación canónica, sin head ⇒ no publica, versión inexistente ⇒ error, stream 5001 ops sin truncamiento (ListOperations default devolvería 5000), INSUFFICIENT persiste NULL (missing ≠ 0).
- `go test ./v3/lab-worker/... -count=1` → `ok` (parse + builder smoke con `lab_job_runs` SUCCEEDED; fallo con algoritmo no registrado).

## DEV (frontend build/test)

- `npx vitest run` en `v3/front` → 14 archivos, 55/55 PASS (incluye 22 nuevos: servicio GraphQL con paginación/total, chart con X datetime real + annotations A/B + unidad, metric cards missing≠0, container: header A/B, períodos, drill-down por identidad, banner INSUFFICIENT, error de carga).
- `npm run build` → ✓ built (warning de chunk size preexistente).

## AUTHENTIC (datos reales)

- NINGUNO: 064/065 no aplicadas a bases reales, no existe historia auténtica TRAINING/PRE_REAL (productor Forge pendiente) ni operaciones REFERENCE atribuibles ingestadas. Explícitamente NO declarado: `FORGE_E2E_PASS`, deploy, runtime DEV.

## EXTERNAL / pendiente

- Apply de Hasura metadata a DEV (`hasura metadata apply`) y rebuild del front DEV: mutación de infra compartida, fuera del shot (flujos de release owner).
- Ejecución del binario `lab-worker recalculate-curves` completo: requiere entorno etcd del runtime; la vía servicio está verificada físicamente; la física CLI pertenece al despliegue DEV.
