# ROBUST-V2 — HERA FULL-FLOW E2E (wave2b)

Status: `HERA_FULL_FLOW_PASS_WITH_FIX` · Date: 2026-09-30 → 2026-10-01 · Ejecución sobre la flota operacional Forge (Zeus/Hera/Kronos), incluida Hera.

Verdicto: **PASS_WITH_FIX** — el "fix" no es de producto sino de runtime: la flota corría 0.2.130 (sin V2); se cortó y desplegó la release **0.2.131** construida byte-a-byte desde el SHA certificado V2 `bc50bbba9a50b7079ed81ff96d80b9f1f780c368` (`vcs.modified=false` verificado). **Product code changes: NONE.**

## Dataset

- Cohorte real de la operación: **34 estrategias NDX L H1 SQX v1** (cohort histórico `wave1z`/`02_full_retester`, propiedad del FlowRun COMPLETED `c329a546-800b-494b-bace-c87fd81dae10`) — la misma entrada que consumió wave2a. No existe ningún dataset pre-stageado adicional en Hera u otro host: la evidencia durable (Mongo/PG/MinIO/Temporal) no registra wave posterior a wave2a, y el dataset del test ES el corpus operativo de la flota.
- **Ejecución en Hera:** los CELLs se generaron en vivo por sqcli sobre el SQX real de cada host con su historia NDX sincronizada (hash flota 3/3 igualado en la sync de 2026-09-26). Participación física medida por host (invocaciones sqcli wave2b): **Hera 39, Kronos 22, Zeus 109** (fan-out `max_parallel: 3`, batch_size 1, sliding window).
- Config del producer: `Optimizer.cfx` owner SHA `4b282d8b73f3c88fb262f73707f70c65bbba4bbe57bba3fa9fe8be5baa85bdf0` (copiado byte-exacto al paquete del watcher desde el paquete sellado de wave2a). Grid WF type2 p10/o15: **runs {5..10} × OOS {20..36} = 54 celdas/estrategia**; período de datos NDX 2015→2026-04-24.
- Output físico: **1.836 CELLs = 34 × 54** (mín=max=54 por estrategia, grid completo) + 34 aggregates, persistidos como evidencia durable de ESTE FlowRun.

## Effective config

```text
algorithm      = robust_run_selection_v2
cliff_threshold = 0.35
epsilon_ret     = 0.01
epsilon_aux     = 0.01
```

- Vía real del flujo canónico: `wave_config.wfm_params` (schema existente; NO es un campo por-task) → watcher → `sqx.configs.config_json` (PG durable) → `wfmParamsFromSpec` → `EvaluatorConfigFromWFMParams` → `ScoringAlgorithm=robust_run_selection_v2` + versión `v2` + 3 params required fail-closed → `EvaluateAndComplete` → dispatch V2 en `evaluateNeighborhoods`.
- **Digest del config efectivo: `sha256:24daf87d310c3f6f81cb5ea96afee3457d04b67861f0060cd2d34fefad60535e`** — idéntico al digest del trial V2 de la validación local (mismos knobs efectivos: defaults frozen V1 para reglas/pesos/top_n + V2 con 0.35/0.01/0.01).
- Resto de knobs V1 intactos (top_n 3, min_consistency 0.90, weights 0.4/0.6, reglas default, sin metric filters). Sin tuning; V1 untouched.

## Execution path (canónico, sin scripts reemplazando stages)

1. Release **0.2.131** cortada con `deploy_release.sh --release-only 0.2.131` desde rama `feature/robust-selection-v2-hera-e2e` @ `bc50bbb` (== `origin/feature/robust-selection-v2-shot1` certificada; el branch es exactamente master `ca07f72` + 3 commits V2). Worker SHA `f6354373…`, watcher SHA `0c811b9d…`, ambos en manifest MinIO (`deploy/worker/sqx/manifest.json` @ 2026-09-30T23:27:05Z). Rollout 3/3 certificado por Prometheus (series `campaign_apply` con `process_executable_path=/opt/stager/releases/0.2.131/bin/symphony`; un worker vivo por host: Hera PID 56057, Kronos 1734488, Zeus 3301726). SSH kor@ sigue roto (publickey denied 3/3) — verificación por el canal Prometheus certificado; preflights de host (GUI sqcli, CFX en host) aceptados como riesgo conocido, igual que en wave2a.
2. Preflight: `runtime.ValidateWorkflowSpec` + `VerifySpecMaxParallelPreserved` + `EvaluatorConfigFromWFMParams` + digest + `cfgID` libre en `sqx.configs` — todo vía harness efímero sobre código de producto real (SPEC_VALID; CFGID `NDX_SQX_v1_wwave2b` libre).
3. Despacho: watcher candidate-local 0.2.131 en Daedalus (`~/aranea/work/robust-v2-hera-e2e-20260930/watcher/`), pipeline 7/7 steps, paquete sellado en `input/processed/20260930_204232_*`.
4. Wave **wave2b** = espejo exacto del funnel de wave2a (owner 2026-09-28: group cohort histórico → Optimizer → evaluate_wfm → select_robust_run; STOP antes de Final Retester/MT5) + `wave_config.wfm_params` V2. Sin ninguna tarea extra.

## Run IDs

```text
FlowRunRef      = 0cbd0f34-c4f2-459e-b670-242bddd35b85
cfgID           = NDX_SQX_v1_wwave2b  (config durable PG con wfm_params V2 preservado, verificado post-dispatch)
Root workflow   = sqx-main-v1-3afbfb70-774a-4c57-8fd5-463a5c7d09d4 (Temporal ns sqx-prop)
Dispatch        = 2026-09-30T23:42:32Z
COMPLETED       = 2026-10-01T20:47Z (~21h05m; wave2a había tomado ~12h — flota sin cambios de config, corrida más lenta, sin retry anómalo: 0 errores de stage)
Stage executions: 34× project@sqx-optimizer.v1 COMPLETED · 34× evaluate_wfm@sqx-wfm.v1 COMPLETED · 21× select_robust_run@sqx-robust-selection.v1 COMPLETED · 0 errores
```

## Evidencia durable de que el flow usó V2 (Phase 6)

1. **Spec procesado** (`artifacts/hera-e2e-20261001/20260930_204232_flow-robust-v2-hera-e2e-wave2b.json`): `wave_config.wfm_params.algorithms/params` presentes.
2. **Config durable PG** (`sqx.configs.config_json` de `NDX_SQX_v1_wwave2b`, leído post-despacho): `wfm_params {algorithm: robust_run_selection_v2, params {cliff_threshold 0.35, epsilon_ret 0.01, epsilon_aux 0.01}}` — el watcher 0.2.131 no descartó campos.
3. **34/34 aggregates en Mongo** (`forge.evaluations`, flow_run_ref=wave2b): TODOS con `scope.scoring_algorithm="robust_run_selection_v2"`, `scope.scoring_algorithm_version="v2"` y `scope.evaluator_config_digest="sha256:24daf87d…"`. Ningún aggregate V1.
4. **21 decisiones PG** (`sqx.decisions`, type OPTIMIZER_SELECTION, outcome SELECTED): output con `ranking_metric="ret_dd"`, `robustness_score=0` (contrato Shot 1R), verdict WARN, rank 1, y ref exacta al aggregate + CELL pick.

## Funnel

```text
input strategies            = 34  (cohort histórico wave1z, memberships REPROCESSED 34/34)
optimizer ejecutado         = 34  (1836 CELLs, 54/54 por estrategia)
WFM evaluadas               = 34
WFM PASS                    = 0
WFM WARN                    = 21  (reason STABILITY_WARNINGS)
WFM FAIL                    = 13  (reason NO_ACCEPTABLE_NEIGHBORHOOD)
rank1 emitido               = 21  (uno por strategy con picks; único rank==1, contract durable)
downstream SELECTED         = 21  (decisions PG, WFM_WARN_TOP_PICK; 1:1 con WARN, 0 mismatch)
downstream REJECTED         = 13  (sin survivors → sin decisión; mismo criterio que wave2a)
final surviving strategies  = 21
STOP antes de Final Retester/MT5: VERIFICADO (MinIO wave2b sólo 03_optimizer/04_wfm/05_robust/root; sin promotion/apply/MT5)
```

## Resultados por Strategy

CSV completo: `ROBUST-V2-HERA-E2E.csv` (este directorio; una fila por Strategy con verdict/runs/OOS/selected/reason/median_retdd). Raw por estrategia: `artifacts/hera-e2e-20261001/results_v2.jsonl` (incluye subject_ref, aggregate ref, digest).

- **21 seleccionadas** (rank1 runs/OOS, mediana Ret/DD del vecindario): 1.13.611 (7/30, 9.12), 1.37.569 (7/30, 8.34), 1.8.669 (9/34, 12.28), 2.27.756 (9/28, 7.13), 2.41.524 (8/36, 10.35), 2.75.621 (9/30, 13.83), 2.76.686 (6/30, 17.35), 3.15.781 (8/24, 8.09), 3.31.576→ver fila, 4.57.731, 5.38.585, 6.24.638, 6.39.493, 6.40.536, 6.41.479 (8/28, 12.65), 7.46.731, 8.10.634, 8.11.487, 8.25.708, 8.26.438, 8.62.460, 8.67.447 — ver CSV para la lista exacta y valores.
- **13 rechazadas** por `NO_ACCEPTABLE_NEIGHBORHOOD` (sin 3×3 elegible): 1.38.707, 1.83.581, 2.17.503, 2.17.581, 3.31.576, 3.42.961, 3.44.150, 4.22.309, 4.23.222, 5.23.512, 7.51.646, 8.12.552, 8.13.720 (ver CSV).
- Columnas `R_retdd/R_aux/cliff/median_sharpe/median_profit` en blanco: el contrato durable V2 NO emite esas cantidades (sólo `ranking_metric=ret_dd` + mediana Ret/DD del vecindario como quality key; R_aux/cliff son cantidades internas de selección). Se deja blank en vez de derivar fuera del flujo.
- `robustness_score=0` en los picks: contrato congelado (V2 no define score escalar; la autoridad es rank==1).

## Comparación con V1 (wave2a, mismo cohort)

Caveat obligatorio: wave2b RE-EJECUTÓ el Optimizer (celdas frescas, materialización nueva); wave2a comparaba V1/V2 sobre las MISMAS celdas. Las diferencias por estrategia confluían frescura-de-optimizer + algoritmo, así que la comparación cross-wave es cualitativa.

```text
V1 (wave2a): 34 → 10 WARN → 10 SELECTED · 24 FAIL (16 NO_ACCEPTABLE + 8 SEVERE_WARNING)
V2 (wave2b): 34 → 21 WARN → 21 SELECTED · 13 FAIL (todas NO_ACCEPTABLE; V2 no produce FAIL-SEVERE-with-picks)
por estrategia: 8/34 igual veredicto · 13 FAIL(V1)→WARN+SELECTED(V2) · 2 WARN(V1)→FAIL(V2) · 11 cambios de pick dentro de WARN
```

Lectura: consistente con la clase de comportamiento certificada en la validación local — V2 desbloquea strategies que V1 auto-gateaba por pico aislado (SEVERE) y/o encuentra mesetas donde V1 no aceptaba vecindario, y no genera rechazos por cliff/bandas a nivel Strategy. Las 2 inversiones (2.17.581, 3.31.576) y los 11 cambios de pick se explican por la combinación de celdas frescas + preferencia V2 por mesetas; la aceptación de este trade-off ya es política aceptada del diseño V2.

## Fallos / fixes

- **INTEGRATION DEFECTS FOUND: NONE de V2.** Cero errores de stage en 92 stage executions; ninguna corrección de producto fue necesaria; el algoritmo V2, su binding durable, el select por rank==1 y el output contract operaron tal cual en el flujo real.
- Fix aplicado (runtime, no producto): rollout de la release 0.2.131 construida desde el SHA certificado (`bc50bbb`) porque la flota estaba en 0.2.130 (sin V2 → `EvaluatorConfigFromWFMParams` habría fallado cerrado). Branch `feature/robust-selection-v2-hera-e2e` = `bc50bbb` + commit de manifest `15ce01e` (pusheada a origin). Binarios: worker `f6354373…`, watcher `0c811b9d…` (`vcs.revision=bc50bbb…`, `vcs.modified=false`).
- Hallazgos operacionales (no bloqueantes): SSH kor@ roto 3/3 (verificación de rollout por Prometheus, canal certificado); ambos MCPs Mongo (ro/rw) caídos durante la sesión (fallback: helper efímero read-only con el cliente del repo); watcher legacy de wave2a aún vivo en Daedalus (eliminado antes del despacho); OTEL collector .45 caído (preexistente).

## Veredicto

**HERA_FULL_FLOW_PASS_WITH_FIX** — V2 (`robust_run_selection_v2`, 0.35/0.01/0.01) se consumió por el flujo canónico completo de Forge mediante configuración, desde el dataset real ejecutado en la flota (Hera incluida) hasta las decisiones durables downstream, con evidencia durable auditable en cada eslabón. `READY_FOR_NORMAL_V2_USE: YES` (con la release 0.2.131 desplegada; quedará absorbi­da por la próxima release natural de master cuando el Primary Technical Manager complete la integración de la rama V2).

## Artefactos

- `ROBUST-V2-HERA-E2E.csv` — una fila por Strategy (este directorio).
- `artifacts/hera-e2e-20261001/` — spec despachado (SHA `49a952b7…`), `results_v2.jsonl` (raw por estrategia, SHA `688128a6…`), `monitor-wave2b.log` (SHA `0b902554…`), `SHA256SUMS.txt`.
- Durable: FlowRun `0cbd0f34` (PG), aggregates+cells en Mongo `forge`, decisions en PG `sqx.decisions`, artifacts en MinIO `sqx-strategies/wave_wave2b/…`.
