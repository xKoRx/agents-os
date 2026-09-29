# GROUP-CHAINING-RCA.md

**Echo Forge — Operación Real V2 · RECOVERY C5.2 · 17.ª sesión (2026-09-28)**
Defecto: chaining silencioso Full → Optimizer truncado (wave1z `c329a546-800b-494b-bace-c87fd81dae10`).
Veredicto RCA: **CONFIRMADO** en HEAD `b2e321d` (pre-fix), refutada cualquier causa alternativa de paralelismo/config/watcher.

## 1. Cadena causal exacta (file:line verificados en HEAD `b2e321d`)

1. El root `GenericSQXWorkflow` ejecuta el group Full y al terminar aplica la regla legacy de reset:
   `sqx/workflows/generic_workflow.go:358` → `current = resetBatchKeepBindings(current)`.
2. `resetBatchKeepBindings` (`sqx/workflows/mt5_identity.go:283-290`) preserva `StrategyArtifacts` (34 carriers vivos) pero **NO copia `Keys`** → batch **artifact-only** (`Keys=[]`, 34 carriers).
3. El siguiente task del root es `03_optimizer_group` (durable, SIN `source_folder` a nivel group — el `source_folder: 02_full_retester` está sólo en el task anidado; `flow-precision-wave1z.json` EV1). En `handleGroupTask`, el gate de cohort:
   `sqx/workflows/generic_workflow.go:1530` → `if currentBatch.IsEmpty()`.
4. `StratBatch.IsEmpty()` (`sqx/core/runtime/config.go:829-831`) = `len(b.Keys) == 0` — **ciego a `StrategyArtifacts`** → el batch artifact-only entra al gate como si fuera cohort vacío.
5. El group no califica como durable-historical-source (`isDurableHistoricalSourceGroup` exige `SourceFolder` a nivel group; `generic_workflow.go:1493-1503`) → camino legacy `list_strats("03_optimizer")` (`generic_workflow.go:1559-1561`) → el folder tiene sólo `.folder_marker` → 0 keys → `"No hay estrategias disponibles, terminando grupo"` → `return runtime.StratBatch{}, nil` (`generic_workflow.go:1570-1572`) → **0 children, sin error**.
6. El chunking-por-carriers que sí soporta el chaining (`generic_workflow.go:1584-1589`, introducido en commit `13b2b8e` con comentario explícito "los lotes se arman desde los carriers exactos para que un grupo durable pueda encadenar sobre la salida del anterior") queda **INALCANZABLE**: el gate dispara antes. Defecto de clase: gate de emptiness parcial + spec sin `source_folder` a nivel group en el segundo group.

## 2. Evidencia física de wave1z (runtime durable, verificada 2026-09-28)

- `sqx-flowkit run stages c329a546-800b-494b-bace-c87fd81dae10` (schema `sqx-run-stage-timeline.v1`): `status=COMPLETED`; funnel `project@sqx-retester.v1` `executions_total=4`, 4 COMPLETED (los 4 chunks de 34/ batch 10), 0 FAILED/CANCELLED. **Ningún stage del group 03_optimizer**.
- MinIO `sqx-strategies` bucket: `wave_wave1z/ndx/l_h1/SQX/v1/02_full_retester/` = **34 archivos .sqx** + `.folder_marker`; `03_optimizer/` = **sólo `.folder_marker`**.
- Mongo `forge.evaluations`: **34 output evaluations** con `flow_run_ref=c329a546-…`, `role=OUTPUT`, `artifact_type=STRATEGY_SQX`, object_key bajo el namespace exacto (cruce 1:1 con MinIO por nombre; sha256 por artefacto; ver FULL-RECOVERY-INPUT.csv).
- Descartado: pérdida de paralelismo (fan-out wave1z certificado 16.ª: refill +51 ms), config loss (spec durable íntegro), watcher stale (`max_parallel` presente en config `a8ce3950-…`).

## 3. Defecto downstream de la misma raíz (descubierto en el fix)

`exactArtifactsForKeys` (`generic_workflow.go:1947-1993`) exige que cada `artifact.Key` exista en `currentBatch.Keys` ("has no current batch binding") — con el batch artifact-only el child-input del siguiente group habría fallado AUNQUE el gate no interceptara. El fix normaliza el cohort encadenado derivando `Keys` desde los carriers (misma forma que devuelve `buildCohortBatch` de `resolve_historical_cohort`, `sqx/activities/worker/historical_cohort_activity.go:185-189`), con lo que ambos caminos (secuencial y `runGroupChunksParallel`) operan sin cambios.

## 4. Protección adicional evaluada (mandato: "0 chunks tras carriers")

Tras el fix, todo camino de 0 ejecuciones tiene evidencia explícita: (a) cohort realmente vacío → `list_strats` llamado (T3/T7) o (b) `resolve_historical_cohort` sameFlow-noop (contrato CROSS-FLOWRUN-REUSE vigente). Con carriers>0 el chunking deriva directamente de los carriers (slices ≥ 1; keys duplicadas/vacías fallan cerrado dentro de `exactArtifactsForKeys`), por lo que "carriers → 0 chunks" es estructuralmente inalcanzable. Decisión: NO se agrega un guard de código muerto (KISS); la cerca permanente contra la regresión es el E2E T6 (`TestGroupChaining_RootFullGroupOutputsFeedOptimizerGroup`), que reproduce el shape exacto wave1z (Full → reset → Optimizer-like con max_parallel 3) y falla si el segundo group no produce children.
