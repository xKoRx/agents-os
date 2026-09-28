# Echo Forge — Operación Real V2 — Auditoría fresca de paralelismo SQX — Change Log

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - main/10-projects/Echo Forge — Operación Real V2/Echo Forge — Operación Real V2.md (tarea C5.2 actualizada a `[/]` con estado material; bitácora 16.ª añadida; frontmatter `updated` → 2026-09-28)

## Motivo

- Mandato owner "ECHO FORGE — AUDITORÍA FRESCA DE PARALELISMO SQX" (2026-09-28): sesión cold-start para determinar definitivamente cómo funciona HOY el paralelismo (max_parallel/batching/children/utilización de flota), con veredicto y acción sólo si había bug que explicara pérdida real de paralelismo.

## Fuentes usadas

- Repo xKoRx/symphony @ `b2e321d` (= origin/master, worktree limpio, release flota 0.2.129): `sqx/workflows/generic_workflow.go` (`handleGroupTask`, `runGroupChunksParallel`, `groupParallelChildrenEnabled`, `GroupSQXWorkflow`, `isDurableHistoricalSourceGroup`), `sqx/workflows/mt5_identity.go` (`resetBatchKeepBindings`), `sqx/core/runtime/{config,mt5_task_config,spec_max_parallel_preflight}.go`, `sqx/cmd/sqx-worker/{main.go,worker_options_test.go}`, `sqx/workflows/{group_parallel_children_test,group_workflow_test}.go`, `sqx/activities/worker/{list_strategies,steps/steps}.go`, `specs/FEAT-SQX-WORKFLOWS-GENERIC/SPEC.md` §4.4, `.agents/skills/forge-wave-dispatch/SKILL.md`.
- Arqueología Git (subagente): `859dec3` fork-join origen → `7c13926` secuencialización (2026-06-21) → `10f4a9a` primer fan-out acotado (0.2.113) revertido en 9 min (`c643475`, 0.2.114) → `13b2b8e` chaining + early-exit gate (0.2.121) → `29830d4` knob `max_parallel` → `bf1696b` fan-out version-gateado (0.2.129) → `3a79654`+`b2e321d` freeze.
- Runtime físico: historial Temporal ns `sqx-prop` vía helpers efímeros RO `/tmp/wave1z-hist/` y `/tmp/wave1z-inspect/` (nuevo, imprime input del root + activities con nombre); watcher log wave1z (config durable `a8ce3950-…`, dispatch 02:58:26Z); MinIO `wave_wave1z/ndx/l_h1/SQX/v1/` (`02_full_retester/` 34 .sqx, `03_optimizer/` sólo marker); Prometheus contadores sqcli wave1z (Zeus PID 3117769 = 0.2.129).

## Hallazgos (veredicto en bitácora 16.ª)

- Paralelismo: `PARALLELISM_WORKING_AS_DESIGNED` — sliding window física probada en producción (subflow-2 COMPLETED 06:47:36.188Z → subflow-3 START_CHILD +51 ms con subflow-0 hasta 11:56:53Z y subflow-1 hasta 16:13:15Z en vuelo); spec ejecutado llegó íntegro al input del root (ambas groups con max_parallel=3 — sin config loss); worker safety 1 y tests HEAD verdes.
- Hallazgo material nuevo: wave1z COMPLETÓ 16:13:16.087Z (result 0B) **sin ejecutar Optimizer/WFM/Robust** — tras el group el reset deja batch artifact-only (Keys vacías + 34 carriers) y el gate `if currentBatch.IsEmpty()` (sólo mira Keys) en `handleGroupTask` envía `03_optimizer_group` (sin `source_folder` a nivel group) al camino legacy `list_strats` → folder vacío → 0 keys → grupo terminado sin error. El chunking-por-carriers documentado en `13b2b8e` y la skill es inalcanzable (código muerto). Funnel C5.2 truncado silenciosamente desde el primer dispatch (wave1w y wave1z). Mono-host 12:54→16:13Z = cola de partición (1 chunk restante), no defecto de scheduling.
- Acción NO ejecutada (mandato §10: sólo implementar si explicaba pérdida de paralelismo): fix mínimo candidato = gate artifact-aware; alternativa owner sin código = despachar Optimizer como wave durable histórica (`source_folder: 02_full_retester` + `cohort_wave: wave1z` + `cohort_flow_run: c329a546…` a NIVEL GROUP, patrón wave1u — verificado viable con el código vigente).

## Validación

- `go test ./sqx/workflows/ -run 'TestGroupParallelChildren|TestHistoricalDurableGroup|TestIsDurableHistoricalSourceGroup'`, `./sqx/cmd/sqx-worker/ -run TestSQXTemporalWorkerOptions`, `./sqx/core/runtime/ -run 'TestValidateMaxParallel|TestVerifySpecMaxParallelPreserved'` — todos verdes en HEAD `b2e321d`; repo sin delta.
- Temporal al cierre: 0 workflows Running (flota idle — la campaña no está en vuelo; no hay trabajo que distribuir).
