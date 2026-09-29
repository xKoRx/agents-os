# GROUP-CHAINING-FIX-VERIFICATION.md

**Echo Forge — RECOVERY C5.2 · 17.ª sesión (2026-09-28)**
Fix: `3765d14` (+`dd6c4bb` docs, `0a10612` gofmt) → master `0a10612..af8f1ae` (origin pushed).
Release canónica: **0.2.130** (manifest `deploy/worker/sqx/manifest.json` @ MinIO, worker sha `98291e1ce3b4d8586bc8abdc91016b5df26cf1c233aa664cd92bfad805423815`, watcher sha `d810bed267cf45423e48d789d20175c410c20438cb82f71ddcdcc582b93e0a13`, publicado 2026-09-28T18:35Z por `deploy_release.sh --release-only 0.2.130`; release commit `af8f1ae`).

## 1. Semántica del fix (contrato en 3 estados)

`sqx/workflows/generic_workflow.go` — gate de cohort de `handleGroupTask` ahora es artifact-aware:

- **A1 — chained durable carriers** (`Keys==0 && StrategyArtifacts>0`, group sin source histórico): los carriers SON el cohort actual; se derivan `Keys` desde los carriers (misma forma del batch de `resolve_historical_cohort`) → chunking → children. **NO** `list_strats`, **NO** resolve historical. Telemetría nueva: `Cohort encadenado artifact-only para group` con `carriers_count`.
- **A2 — truly empty** (`Keys==0 && StrategyArtifacts==0`): mecanismo vigente intacto — durable historical source → `resolve_historical_cohort`; legacy → `list_strats`.
- **A3 — ambiguous authority** (carriers + `source_folder` histórico a nivel group): **fail-closed `CONTRACT_CONFLICT`** ("exactly one cohort authority is allowed") sin ejecutar nada. No ignorar `source_folder`. Alineado con `ValidateWorkflowSpec` (que ya rechaza `cohort_wave` sin `source_folder`) y con el vocabulario canónico de `specs/FEAT-SQX-CROSS-FLOWRUN-REUSE/SPEC.md`.

NO tocado: task types, persistencia, reimport, lookups, fan-out (`runGroupChunksParallel`/`groupParallelChildrenEnabled`/`workflow.GetVersion("group-parallel-children")`), worker concurrency (`MaxConcurrentActivityExecutionSize: 1`), R12, ranking, `max_parallel`.

## 2. Tests (T1–T7 nuevos en `sqx/workflows/group_chaining_test.go`; T8 = regresión)

| # | Test | Cubre | Estado |
|---|---|---|---|
| T1 | `TestGroupChaining_ArtifactOnlyCohortFansOutWithoutListingOrResolve` (cohort 1 y 5) | cohort encadenado: 0 list, 0 resolve, exactly-once, carrier 1:1 por key | PASS |
| T2 | `TestGroupChaining_ParallelChainingKeepsSlidingWindow` | chaining con `max_parallel=3`: concurrencia máxima == 3 exacto, ventana deslizante, exactly-once 5/5 | PASS (estable ×3) |
| T3 | `TestGroupChaining_TrulyEmptyLegacyStillLists` | vacío real legacy conserva `list_strats` (0 resultados → 0 children, sin error) | PASS |
| T4 | `TestGroupChaining_TrulyEmptyHistoricalStillResolves` | vacío real + source histórico conserva `resolve_historical_cohort` (3/3 fan-out exacto) | PASS |
| T5 | `TestGroupChaining_HistoricalSourceWithChainedCarriersFailsClosed` | A3: `CONTRACT_CONFLICT`, sin children, sin list, sin resolve | PASS |
| T6 | `TestGroupChaining_RootFullGroupOutputsFeedOptimizerGroup` | **E2E raíz anti-regresión del defecto wave1z**: Full-like (batch 10, maxp 3) → reset → Optimizer-like (batch 1, maxp 3) produce 4 children con carriers exactos + evaluate_wfm + select_robust_run por StrategyRef; list/resolve prohibidos (fail-loud) | PASS |
| T7 | `TestGroupChaining_ZeroRealOutputKeepsLegacyListBehavior` | cero output real: camino vacío existente preservado (list consume folder) | PASS |
| T8 | Regresión suites | `sqx/workflows` fail-set **idéntico a master** (21-22; única diferencia = `TestDurableSelect_GroupSelectedCarrier`, flaky preexistente que falla 2/5 también en master limpio — race de orden de mock, sin relación con el fix). `sqx/core/...`, `sqx/activities/...`, `sqx/adapters/...` verdes | PASS |

**Criterio del fix demostrado**: `artifact-only != empty cohort` para chaining durable (T1/T3 contrastantes) y `Full-output carriers → siguiente group` alcanzable (T6 E2E).

## 3. Rollout 0.2.130 — certificación física (canales sin SSH; SSH kor@ roto en 3/3 hosts)

| Host | Evidencia | Estado |
|---|---|---|
| Zeus (z0) | Prometheus `symphony_sqx_activity_result_total{host_key="z0", process_executable_path="/opt/stager/releases/0.2.130/bin/symphony", process_pid=3243046}` (churn de PIDs del stager 3242997→3243046, antes 0.2.129 PID 3117769 = el PID certificado de wave1z) + poller Temporal `3243046@sqx-ulab-zeus-0` activo en `sqx-main-queue` + activity `campaign_apply` exitosa bajo el binario nuevo | **APPLIED & FUNCTIONAL** |
| Kronos (k0) | Ídem: 0.2.129 PID 1601599 → 0.2.130 PID 1683548 + poller `1683548@sqx-ulab-kron-0` | **APPLIED & FUNCTIONAL** |
| Hera (h0) | SSH `No route to host` (192.168.31.111, 100% packet loss; zeus responde <1 ms), sin series Prometheus >90 min, **sin poller Temporal**; última versión conocida 0.2.129 (PID 1638749, esta mañana) | **OFFLINE — no certifiable** |

**Rollout certificado 2/3** (Hera caída a nivel de red — degradación de infraestructura ajena a la release; el stager aplicará 0.2.130 automáticamente al volver). El mandato exige rollout 3/3 antes de despachar ⇒ el dispatch de la recovery queda **gated** hasta que Hera vuelva y la flota esté 3/3 en 0.2.130. Igualdad byte-exacta del binario en host no re-verificable sin SSH; la cadena publish→manifest(SHA en MinIO)→stager(layout por versión)→proceso con esa ruta exacta es la evidencia disponible, más el test de conducta (activity exitosa bajo el binario nuevo).

## 4. NO-REGRESSION FANOUT (declaración explícita)

- `runGroupChunksParallel`, `groupParallelChildrenEnabled`, `workflow.GetVersion("group-parallel-children")`, `MaxConcurrentActivityExecutionSize: 1` (`sqx/cmd/sqx-worker/main.go` + `TestSQXTemporalWorkerOptions_SerializesActivities`), preflight `runtime.VerifySpecMaxParallelPreserved`: **0 líneas modificadas** (diff del fix = 1 archivo de workflow, 31+/3-, y tests nuevos).
- `TestGroupParallelChildren_*` (4 tests, incl. `SlidingWindowRefillOrder`): verdes en la suite.
- T2 demuestra además que el fan-out funciona sobre cohort encadenado sin reabrir su implementación.
- **R12 intacto**: ninguna decisión del freeze `FLEET_FANOUT_ARCHITECTURE_FROZEN` fue reabierta.

## 5. Documentación canónica actualizada (mismo merge)

- `specs/FEAT-SQX-WORKFLOWS-GENERIC/SPEC.md` §4.2: resolución de cohort en 3 estados (A1/A2/A3) + defecto corregido con referencia wave1z.
- `.agents/skills/forge-wave-dispatch/SKILL.md`: chaining Full→Optimizer intra-FlowRun operativo desde 0.2.130; el re-despacho como wave histórica sigue siendo válido e independiente.
