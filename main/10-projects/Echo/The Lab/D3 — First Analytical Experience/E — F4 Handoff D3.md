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
  - D3 F4 handoff
tags:
  - kind/doc
  - area/echo
  - the-lab
  - d3
---

# E — F4 Handoff D3

## Boundary que Fase 4 debe invocar

```go
// módulo github.com/xKoRx/echo/v3/sdk
svc := postgres.NewLabCurveService(db, nil) // nil ⇒ registry con los algoritmos V3 registrados
results, err := svc.RecalculateStrategyVersion(ctx, registryNamespace, versionRef, specs)
// specs nil ⇒ todas las especificaciones por defecto (algoritmos registrados, config vacía)
// results []postgres.RecalculateResult{Spec, Status, Published, CurveID}
```

Flujo F4: `canonical history changed → dirty → recalculate → publish`:

1. **Detección de dirty:** comparar el `history_digest`/`dataset_digest` persistidos en `echo.lab_curves` contra el head vigente (`postgres.NewStrategyHistoryRepository(db).GetHistoryHead`) y/o recomputar: cualquier cambio del dataset canónico cambia `dataset_digest`.
2. **Recálculo:** una llamada por StrategyVersion afectada. El servicio toma head+operaciones en snapshot REPEATABLE READ con el advisory lock del replacement D1 y publica TODAS las specs de la versión en una transacción (atómico, idempotente, sin duplicados).
3. **Publish/read:** al commitear, el read model (Hasura sobre lab_curves/points/metrics) refleja el nuevo estado; el front renderiza lo publicado.

Sin head D1 la llamada NO publica y devuelve resultados con `Status=ERROR, Published=false` — el worker F4 puede tratarlo como "aún no importado". El worker automático (timer/checkpoint sobre journal) NO existe todavía: es exactamente el alcance de Fase 4, invocando este método. `lab_job_runs` ya registra ejecuciones manuales vía `lab-worker recalculate-curves`.

## Entry points operativos

- CLI: `lab-worker recalculate-curves --namespace <ns> --strategy-version-ref <sha256:…> [--algorithm id@version …] [--triggered-by …]` (flags: `curves_parse.go`; job run: `internal/builders/recalculate_curves.go`).
- Tests/verificación: `bash v3/sdk/postgres/tests/d3_curves/run_tests.sh` (PG desechable + schema + suite); `go test ./v3/sdk/analytics/curve/`; `npx vitest run` + `npm run build` en `v3/front`.

## Estados congelados

- `FORGE_DUAL_HISTORY_INTEGRATION = PENDING` — cuando Forge incorpore operaciones nuevas por la interfaz canónica (PUT `strategy-history.v1`), F3 funciona sin cambios: el engine consume la autoridad, y F4 dispara recálculo por dirty.
- Real (REFERENCE) hoy: sólo vía D4 (worker journal). El engine ya clasifica REAL y la UI muestra "REAL aún sin operaciones" cuando corresponde.

## Qué debe intentar falsar el Shot 2 (resumen)

Ver [[C — Evidence D3 (Shot 1)]] y `specs/FEAT-THELAB-D3-CURVE-ENGINE/`: determinismo (`result_digest`), no truncamiento analítico (5001 ops), atomicidad de publicación (fallo inyectado), trazabilidad punto→operación, missing ≠ 0 en métricas persistidas, períodos por opened_at contra A/B del head, cero dependencia Forge / cero escritura trade_journal / cero segunda autoridad.
