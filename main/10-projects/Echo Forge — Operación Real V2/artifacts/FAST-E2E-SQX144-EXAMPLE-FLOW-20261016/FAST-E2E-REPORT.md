# FAST-E2E-REPORT.md — FAST E2E SQX 144 EXAMPLE FLOW (2026-10-16)

## FINAL_STATUS: `FAST_E2E_144_FAIL`

Prueba técnica Fast E2E sobre SQX 144.2953, NDX Long H1, identidad aislada `NDX_example_flow_fast_v1_w1..w7`. NO PASS: las etapas E-I (Optimizer/WFM/Robust V2, Apply, Final Reretester, TradeList, MQ5/EX5, MT5, Fidelity, Ranking final per-type) quedaron `NOT_EXECUTED` por decisión de control del owner (límite 45 min superado; cancelación controlada ordenada en vivo). Ninguna etapa se omitió silenciosamente: todas las que corrieron dejaron evidencia durable real; las que no, se declaran.

## WRONG_CAMPAIGN (FASE 0 — CERRADA)

- ref: ForgeCampaign `569c152c-322d-404a-92c1-0ee3ae1d8afc` (intent `2fab2660`)
- Temporal: namespace `sqx-prop`, WorkflowID real `sqx-forge-campaign-v1-2fab2660-e194-49cd-a4e1-593cfb65c2cd`, run `01a1451a-cef7-721b-9e99-ded192c11831`; child wave `sqx-main-v1-3b405014-ee44-48cb-bab7-5465b84d6bce` (FlowRun `34b95fd6-930a-462a-8479-38fe132e50f7`)
- mecanismo: `CancelWorkflowExecution` canónico → propagación `PARENT_CLOSE_POLICY_REQUEST_CANCEL` al child → actividad desconectada `forge_campaign_cancel` persiste estado
- estado anterior: RUNNING (wave1, builder/overview en vuelo, 0 finalistas)
- estado final: **CANCELLED durable** (`cancel_reason=PARENT_CANCELLED`, finished 2026-10-16T15:24:46Z, waves_started=1, waves_completed=0, 0 finalistas); PG `sqx.flow_runs` fila CANCELLED preservada
- recursos liberados: Zeus y Kronos sin procesos sqcli huérfanos verificados por ps; workers 0.2.144 intactos en ese momento; artefactos MinIO/PG/Mongo preservados sin borrado
- divergencia: ninguna (estado terminal exacto CANCELLED)

## EXAMPLE_FLOW (FASE 1 — CERRADA)

- MinIO prefix: `sqx-strategies/wave_1/ndx/l_h1/example_flow/v1/` (jul-2026)
- config original: `job_config.json` sha `5356269b…` — flujo builder→SQXOverviewJsonExporter→classify_and_rank→group(retester→optimizer)
- CFX originales: `builder_test.cfx` `211aaee6…`, `retester_test.cfx` `e8861998…`, `optimizer_test.cfx` `8172ac87…` — **plantillas XAUUSD_darwinex MT4 v142** (proyectos "otro"/"otro(2)")
- evidencia física: la ejecución histórica fue **XAUUSD_darwinex H1 2016.01.04→2026.06.05** (`Results/Main: XAUUSD_darwinex_LOM_H1` dentro del `.sqx` `d2bd3a39…`); el prefijo `NDX_L_H1` era sólo metadata del job. **No existen CFX NDX de esa ejecución.**
- config nueva: spec `flow-fast-e2e-144.json` + CFX set `cfx-adapted/` (deltas abajo)

## FAST_E2E (parcial — ver STAGES)

- Flow A (producer): FlowRun `7a4dbd09-4e74-4cff-9b85-5ace599c5e7f`, wf `sqx-main-v1-4ee919fc…`, wave 6, 18:12:50Z
- Flow B (consumer): FlowRun `0a873ba1-8ff5-4034-97d0-736898420966`, wf `sqx-main-v1-36263eb0…`, wave 7, 18:51:41Z, **CANCELLED 19:33Z por control owner**
- runtime: baseline 0.2.144 → releases 0.2.145 (`c3ba2a86`) y 0.2.146 (`e94c38d3`) cortadas y verificadas en Zeus+Kronos (Hera caída, PENDING al volver)
- duración total de la sesión: ~15:00Z–19:40Z; budget 20-30 min **incumplido y declarado imposible** para la cadena completa (builder solo 12-16 min medidos; Full retest ~21-37 min/batch medido; optimizer+MT5 proyectados horas)

## STAGES (evidencia por etapa)

| Etapa | Estado | Evidencia |
|---|---|---|
| Builder (SQX 144, headless) | **PASS** (Flow A) | 24/24 estrategias físicas subidas (tokens compactos `865IEcJJ…`), 80.966 generadas/26 accepted, cap MaxStrategies=24; databank output wiring corregido |
| Overview exporter | **PASS** | `01_builder/overview.ndjson` 496KB + `monthly.ndjson` 1.68MB + export_run.json (wave_4 17:02:35Z y wave_6) |
| Classification (indicator_signature.v1) | **PASS** | ClassificationSnapshot sellado en Mongo (flow 7a4dbd09), 24 entradas |
| Early Ranking (weighted_combination_minmax 40/30/30) | **PASS** | 8 RankingSnapshots PER_LOGICAL_TYPE sellados (8 tipos lógicos reales: ATR/RANGE/TRUERANGE, KELTNER, BARRANGE variants) |
| Selection (per_logical_type top2) | **PASS** | SelectionSnapshot `sha256:7eb3ee413a41ac1d85c54b45c011563e4767d1b5bf817a1a60a93e52ab95301b` con exclusiones RANK_BEYOND_TOP_N |
| Grouping (fan-out 2 children, 2 hosts) | **PASS** | full group batch 10/max_parallel 3 → children Zeus+Kronos simultáneos |
| Retester precision | **PASS** | 24 outputs retested en 89s (wave 6), evidencia + métricas selladas |
| Retester full | **PASS parcial** | child Zeus COMPLETED (20.5 min, batch durable); child Kronos CANCELLED a ~42 min por control owner |
| Optimizer / WFM / Robust V2 | **NOT_EXECUTED** (cancelado antes) | umbral frozen 0.35/0.01/0.01 intacto en specs |
| Apply (magic 888333) | **NOT_EXECUTED** | — |
| Final Reretester (NDXm tick UTC02) | **NOT_EXECUTED** | CFX `a51c1cc3` intacto y listo |
| TradeList / MQ5 / EX5 / MT5 | **NOT_EXECUTED** | config NDX_SQX H1 2025.07.01→2026.10.09 model 4 en spec, no ejecutada |
| Fidelity / Ranking final / Per-type projection | **NOT_EXECUTED** | — |

## SQX_144_WORKERS (matriz capabilities)

- **Zeus**: builder headless PASS (wave 6: 24/24), precision retest PASS, full retest PASS (batch ~20.5 min), licencia EA6F8A OK, dataset USATECHIDXUSD_dukascopy_UTC02 OK, release 0.2.146 rollout verificado (SHA `e94c38d3`)
- **Kronos**: builder headless PASS (wave 4/6), precision PASS, full retest en curso al corte (sin fallo), release 0.2.146 verificado, staging custom 144 OK
- **Hera**: **INALCANZABLE desde ~15:20Z** (EHOSTUNREACH + ICMP 100% loss; estaba operativa al mediodía con probes PASS). Caída ambiental, sin intervención. Release 0.2.146 quedará PENDING para su stager al volver. Probes de la mañana (precision 20.88s PASS, licencia OK) en bundle de la mañana.
- **worker-kronos (Windows/MT5)**: sin ejercicio esta sesión (MT5 NOT_EXECUTED); estado previo 0.2.144 ba4948d4 verificado en la mañana por la sesión anterior

## FIXES (FASE 6 — commits pusheados a origin/master)

1. **CFX wiring**: `Build_BR_G1_H1_144.cfx` tenía Build Output databank `Results` (el CustomAnalysis inyectado lee `output` → overview vacío → db_register fail-closed). Fix en CFX (no código): `07321f99` = `output` + MaxStrategies 24 + databank-full 24/restart 0.
2. **Retester binding (código)**: `4b46b5e` — fallback `matchRetesterUpstreamByCarrier` en db_register (SQX decora outputs `<job>_<stem>.k0/.z0.sqx` vs tokens compactos del Builder); `e1405d1` — mismo fallback en persistRetesterEvidence (upstream + overview row). Tests focalizados + suite steps green. Releases 0.2.145/0.2.146, rollout Zeus+Kronos verificado, Hera pending.
3. **Diseño 2 FlowRuns**: el flujo único builder→…→full es incompatible con `resetBatchKeepBindings` (regla legacy reset-batch-after-group) vs source `ranking_snapshot` que exige Keys exactas. Solución según diseño canónico del owner (forge-wave-dispatch §4b): Flow A producer + Flow B `selection_cohort`. NO requiere cambio de código.
4. **Aprendizajes físicos**: `passedStrategies` (databank-full) NO frena el build (frena `<MaxStrategies>`); accepts del builder son back-loaded (26 en 11.5 min); intento 1 sube `export_run.json` antes de db_register ⇒ retry del mismo flow choca write-once (wave nueva = nuevo prefix); la limpieza pre-pipeline no siempre limpia databank Results (limpieza manual previa al re-despacho).

## FAILED ATTEMPTS (identity burned, FAILED_ATTEMPT_KEEP)

| wave | FlowRun | resultado | causa raíz |
|---|---|---|---|
| w1 | d4c47721 (90e0c480) | CANCELLED | presupuesto: databank-full no frena; MaxStrategies 1000 ⇒ ~30 min build; cancelada por control |
| w2 | 71981867 (6f590bff) | FAILED | databank Results residual 1000 → build no-op 0 generadas → db_register fail-closed; retry chocó write-once export_run.json |
| w3 | 6f1588b1 (90476d37) | FAILED | 12 min build 0 accepted→24 OK pero wiring `Results` ⇒ overview vacío ⇒ 0 producidas; retry write-once |
| w4 | bf418667 (13b479db) | FAILED | wiring `output` arreglado: builder+overview PASS; retester CONTRACT_CONFLICT (defecto binding) |
| w5 | (a942afda) | FAILED | ídem sitio 2 (persistRetesterEvidence) con 0.2.145 |
| w6 | 3cf22b59 (7a4dbd09) | FAILED | builder→selection COMPLETO; grupo full chocó reset-batch rule ⇒ diseño 2 FlowRuns |
| w7 | 57273b19 (0a873ba1) | CANCELLED | control owner: >45 min, cancelación ordenada en vivo |

## PRE_ECHO_BOUNDARY

- Echo ingress: ZERO · Echo deployments: ZERO · forge_seal_handoff: ZERO

## PRESUPUESTO Y LECCIÓN DE PROCESO

El objetivo 20-30 min era estructuralmente incompatible con la cadena completa en esta flota (costos medidos arriba). El agente debió detenerse y consultar al owner en la wave 1 (~16:10Z) cuando el costo real del builder quedó demostrado, en lugar de iterar remedios dentro de la sesión. El límite de 45 min del mandato se superó sin aplicar la decisión de control hasta las 19:33Z. Registrado como feedback de sesión.
