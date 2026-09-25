---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related: []
aliases: []
tags:
  - kind/doc
  - area/echo
  - the-lab
  - d3
created: "2026-09-24"
updated: "2026-09-24"
related:
  - "[[A — Technical SPEC D3]]"
  - "[[F — Independent Verification D3 (Shot 2)]]"
  - "[[D — Debt Ledger D3]]"
  - "[[E — F4 Handoff D3]]"
aliases:
  - D3 correction record Shot 3
tags:
  - kind/doc
  - area/echo
  - the-lab
  - d3
---

# G — Correction Record D3 (Shot 3)

**Corrección de los 7 hallazgos aceptados del Shot 2 + gate final D3, 2026-09-24.** Modalidad fresh context, one-shot, bounded correction sobre el candidate [[F — Independent Verification D3 (Shot 2)]]. Sin redesign, sin features nuevas, sin reabrir decisiones congeladas (H4 sigue rechazado; R_PIPS sigue `INSUFFICIENT_DATA`).

## Commits

```text
shot1_candidate:  6a111c9ec7c987fed885dfea82951256af12b6e1 (parent 8adce7ec98fc20517950635537e515e07c931144)
shot3_branch:     feature/d3-shot3-correction (worktree ~/aranea/work/d3-shot3-correction-20260924/echo)
certified_sha:    372af59a7b83604781346613da01e3d510ea1360
parent:           6a111c9ec7c987fed885dfea82951256af12b6e1 (candidate intacto, sin amend/squash)
delta:            13 archivos, +549/-50, 1 commit
working_tree:     CLEAN
```

## Correcciones

| Finding | Estado | Corrección y evidencia |
|---|---|---|
| F-D3-01 HIGH cross-version publication | FIXED | Guard de identidad fail-closed PRE-transacción en `LabCurveService.RecalculateStrategyVersion`: toda spec debe portar exactamente el `(namespace, versionRef)` pedido; mismatch ⇒ error con cero transacción y cero `lab_curves` (versref/ns/ghost/lote mixto; regresión permanente PG `TestLabCurve_SpecIdentityMismatch_IsFailClosed`). Sin FK, la protección vive en el boundary del servicio. |
| F-D3-02 MEDIUM empty dataset | FIXED | Engine `Registry.Calculate`: dataset vacío ⇒ `INSUFFICIENT_DATA/EMPTY_DATASET` con unidad declarada del algoritmo (R/CURRENCY/R), currency vacía (sin moneda inventada), cero valores fabricados, publicación válida que no viola `chk_lab_curves_unit` ni bloquea los demás results (regresiones `TestCalculate_EmptyDataset_IsInsufficientHonestNotReady` en los 3 algoritmos + `TestLabCurve_EmptyDataset_PublishesInsufficientHonest` en PG con transición vacío→datos). |
| F-D3-03 MEDIUM operation_count basis | FIXED | `countMetric` usa `BasisClosedOperations` factual en TODO camino (READY/INSUFFICIENT; UNKNOWN ya lo declaraba). Regresiones: `TestMetrics_OperationCountBasis_IsClosedOperationsFact` (engine) y `TestLabCurve_OperationCountBasis_PersistedAsClosedOperations` (PG, bases R_MONEY y MONEY). |
| F-D3-04 HIGH visual period regions | FIXED | `CurveV3Chart.vue`: 3 regiones ApexCharts reales (`x`+`x2`+`fillColor`/`fillOpacity`) TRAINING_DATA `[dominio,A]`, PRE_REAL `[A,B]`, REAL `[B,fin de dominio]`, derivadas exclusivamente de A/B; marcadores A/B retenidos; puntos intactos, sin equity intratrade, sin recálculo de períodos en front, eje sigue `event_at`; con B null NO existe región REAL (PRE_REAL abierta + nota "REAL aún sin operaciones"). Tests exigen `x2`+fill con rangos exactos, no strings. |
| F-D3-05 LOW partial pagination | FIXED_MINIMAL | `StrategyCurveV3TabContainer.loadCurveDetail`: página vacía prematura, página fallida o `rows.length !== total` ⇒ fail-closed (banner de error, cero puntos renderizados, cero métricas). Se conserva offset pagination; deuda explícita `CONCURRENT_REPUBLISH_PAGINATION_SNAPSHOT = DEFERRED`. Regresiones vitest: 5001 completo, premature-empty, total mismatch, page error. |
| F-D3-06 LOW readonly aggregate | FIXED | `allow_aggregations: true` en el permiso readonly de `lab_curve_points` (`lab_curves_v3.yaml`); validación estática: YAML parsea, aggregate autorizado, cero write permissions (readonly = SELECT ONLY). |
| F-D3-07 LOW Strategy header | FIXED | Header muestra Strategy (`canonical_strategy_id` de `strategy_versions` vía nueva query `getStrategyVersion` sobre el read model D1 existente); sin timeframe inventado (`TIMEFRAME = NOT_AVAILABLE_IN_D3_MODEL`); fallback honesto "—" si la lectura de identidad falla. |

## Gates finales

```text
ENGINE:        go test ./v3/sdk/analytics/curve/ PASS (determinismo, empty→INSUFFICIENT, R/MONEY math intacto, basis CLOSED_OPERATIONS)
POSTGRES:      bash v3/sdk/postgres/tests/d3_curves/run_tests.sh 13/13 PASS (puerto 16011/16012); cross-version rechazado sin filas; empty dataset INSUFFICIENT válido; multi-spec rollback atómico; replacement D1 intacto
LARGE_SCALE:   probe disposable (NO promovido) 10000/10001/25001 ops PASS: completos, sin truncamiento, recálculo determinista (PG efímero puerto 16021, eliminado al cierre)
D1_REGRESSION: paquete sdk/postgres completo PASS contra schema 064+065; único fallo = TestScratch_QueryDB (preexistente: blob idéntico en 8adce7ec, falla igual en baseline worktree; excluido con -skip legítimo)
FRONT:         npx vitest run 63/63 PASS (14 archivos); npm run build PASS
HASURA_SOURCE: YAMLs parsean; allow_aggregations presente; SELECT-only verificado
```

## DEV integration

`D3_DEV_INTEGRATION = UNVERIFIED_EXTERNAL`. Verificado físicamente que PG DEV (`192.168.31.220:5432/echo-develop`) NO tiene la base D1: ausentes `echo.strategy_history_state` y `echo.canonical_operations` (064 sin aplicar a bases reales, pendiente de flujo de release según Environment Contract §5.6). Aplicar sólo 065 crearía derivados sin autoridad y el metadata D3 rastrearía tablas inexistentes ⇒ mutación bloqueada correctamente, no es defecto D3 ni DEV roto. No se tocó DEV (ni metadata Hasura); NO PROD. `D3_DEV_PASS` NO se declara.

**Actualización 2026-09-24 (sesión D3 DEV Integration Certification):** `D3_DEV_PASS` certificado sobre Echo DEV desde `master@372af59a` — 064+065 aplicadas como `echo_user` vía Hasura DEV (reconciliación SAFE, read-back exacto), metadata D3 aplicada y verificada por GraphQL real (readonly SELECT-only con `allow_aggregations`), release `372af59a` desplegada en Daedalus (Core/Gateway/lab-worker, `vcs.modified=false`), front construido y desplegado desde baseline con verificación visual completa de `/lab` (header F-D3-07, A/B, regiones, MONEY/R, métricas, drill-down punto→operación, rpips INSUFFICIENT honesto), dataset de verificación v1→v2 por la interfaz canónica D1 (`ReplaceHistory` service: CREATED→REPLACED, digests deterministas), recálculo manual demostrado (stale→republish, UI muestra resultado nuevo), rollback demostrado (ciclo 065 down/up con `result_digest` idénticos, rollback+forward de metadata Hasura y dist front) y `PROD_NONEFFECT` verificado. **`D3_AUTHENTIC_DATA_PASS` NO se declara**: no existe dataset auténtico ingerible (`FORGE_DUAL_HISTORY_INTEGRATION = PENDING`; journal sin mapping a StrategyVersions registradas; corpus F04-02 sin trade lists); el dataset usado es `VERIFICATION_DATASET` entrado por la interfaz canónica, no SQL ad-hoc. Hallazgo nuevo para owner: **D3-DEV-01** — en `372af59a` el `StrategyHistoryHandler` no está montado en el mux del Gateway (el boundary HTTP responde 404; el servicio SDK es funcional; los tests arman su propio mux). Evidencia completa: workspace `~/aranea/work/d3-dev-integration-20260924/`.

## Provenance

- SOURCE: diff íntegro candidate..372af59a leído y verificado; grep sin `timeframe` inventado, sin imports Forge, sin DML trade_journal.
- FIXTURE: mismos mecanismos del Shot 1 (PUT D1 `ReplaceHistory` para SQX/MT5; REFERENCE por SQL de prueba declarado); PG desechables efímeros, limpieza verificada.
- WORKSPACE: `~/aranea/work/d3-shot3-correction-20260924/` (worktree de corrección); candidate worktree del Shot 2 intacto.
