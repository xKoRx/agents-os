---
type: raw_session
scope: session
created: "2026-08-14"
updated: "2026-08-14"
area: "[[Echo]]"
project: "[[Echo Forge]]"
application: "[[echo-forge]]"
entities:
  - "[[Echo Forge]]"
  - "[[Symphony]]"
related:
  - "[[2026-08-14-echo-forge-wfm-exporter-slow-summary]]"
aliases: []
confidence: verified
source_session: "temporal-wf-sqx-main-00_configs-v1-XAUUSD-H1-L-1786733372"
load_policy: never
indexable: false
index_priority: never
tags:
  - kind/raw-session
  - scope/session
---

# Diagnóstico ejecución lenta sqx-main XAUUSD H1 (workflow 1786733372)

> [!warning]+ Raw session L0
> Archivo de auditoría y retrofit. Excluido del retrieval normal y de Graphify.

## Contexto

- Owner reportó ejecución Temporal `sqx-main-00_configs-v1-XAUUSD-H1-L-1786733372` (namespace `sqx-prop`, server `192.168.31.46:7233`) con 57 min de duración "exagerada". Investigación con subagentes (troubleshooter para datos masivos + general-purpose para revisión de código), solo lectura sobre repo `symphony`.
- Realidad: el workflow duró **74 min** (18:49:34→20:03:34 UTC del 2026-08-14). El 78% es UNA activity.

## Descomposición de los 74 min (historial Temporal)

- Builder (project sid=5, kron-0): 0.80 min.
- OverviewExporter (project sid=11, zeus-0): 0.80 min.
- classify_and_rank + load_logical_types: ~0 min.
- GroupSQXWorkflow children (16 retester/optimizer): 4.87 min.
- **wfm_exporter (project sid=176, kron-0): 57.57 min (77.8%)** — evento 176, worker `118070@sqx-ulab-kron-0@`, intento 1, sin retries/timeouts/failures.
- evaluate_wfm / select_robust_run fanout (12x): ~0 min.
- apply_selected_run fanout (12x): 1.40 min.
- reretester (project sid=347, zeus-0): 0.31 min.
- trade_list_exporter fanout (12x): 1.13 min.
- generate_report: ~0 min.
- mt5_exporter fanout (12x): 2.65 min.
- list_mt5_artifacts: 0.87 min.
- Child MT5BacktestArtifactWorkflow: 3.51 min.

## Causa raíz 1 — doble ejecución SQX del wfm_exporter

- `execute_sqx` (`sqx/activities/worker/steps/steps.go:598-616`) corre `EchoForgeWFMExporter` completo (RUN 1).
- `import_metadata` (`steps.go:1013-1046`) borra el overview del RUN 1, re-copia las estrategias output→input, escribe `exporter.properties` y re-ejecuta idéntico (RUN 2). Solo el RUN 2 se persiste; RUN 1 se descarta.
- Prueba dura: `result.sqx_raw_log` del evento 178 muestra 26 min 39 s de una ejecución (proyecto 10:56:24→11:23:03 local). 2 × 26.6 min + overhead I/O ≈ 57.6 min exactos de la activity.
- Orden del pipeline: `sqx/activities/worker/pipeline/builder.go:24-41` (`prepare_input → download_strategies → download_config → execute_sqx → collect_results → import_metadata → upload_results → db_register`).
- La task la despacha `sqx/workflows/generic_workflow.go:260-278` (UNA activity monolítica con las 12 keys; variante grupo en `:1820-1832`).

## Causa raíz 2 — plugin Java caro por diseño

- `sqx/exporter-plugin/src/SQ/CustomAnalysis/EchoForgeWFMExporter.java`: `processDatabank` loop serial single-thread (`:122-134`) sobre las 12 estrategias.
- NO recalcula WFM: lee `SettingsKeys.WalkForwardResult` persistido (`:224`); CrossChecks del `CustomAnalysis-Task1.xml` vacíos. El costo es la **re-extracción** de órdenes/métricas.
- Exporta matriz completa **6x9 = 54 celdas** (`:265-288`; dims default en `generic_workflow.go:282`), pero downstream (`steps.go:1244-1272`) solo consume centro + vecindario 3x3. Flag `onlyBest` existe pero inerte (`:270-272`).
- Por celda: 3× `filterOrdersByResultKey` con `filterWithClone` (`:325-327`, `:550-572`), `monthly_results` (`:333`), `periods` (`:344`); por periodo WF 3× `filterTradesByTime` (`:390-395`); `metricsFromTrades` recalcula net/PF/DD/SQN (`:591-683`) en vez de usar SQStats persistidos.
- **Cada acceso a cada trade dispara reflexión completa** (`collectScalarMap` `:1076-1116` vía `tradeCloseOrOpenTime`/`tradeProfit` `:777-797`): O(trades × periodos × celdas) con reflexión por acceso.
- ~2.2 min/estrategia/run.

## Config hallada (riesgo operativo, no causa directa)

- ActivityOptions (`generic_workflow.go:49-61`): StartToClose 10 días, ScheduleToClose 20 días, HeartbeatTimeout 2 min, RetryPolicy `MaximumAttempts: 0` (ilimitada).
- sqcli sin timeout efectivo (`sqx/adapters/cmd-executor/cmd_executor.go:115`, `main.go:116` sin `WithTimeout`).
- Worker `temporalWorker.Options{}` sin `MaxConcurrentActivityTaskExecutors` (`sqx/cmd/sqx-worker/main.go:325-327`).
- Task queue única `sqx-main-queue` compartida Zeus/Hera/Kronos (`runtime/config.go:439-443`); wfm_exporter monolítico → todo a un host (kron-0 ganó el poll). Directorios de proyecto compartidos por host (`runtime/config.go:163-195` + `hooks/cleanup_databanks.go`) impiden fan-out sin dirs por request.
- Heartbeat con mensaje estático sin progreso (`sqx/core/instrumentation/heartbeat.go:24-52`).
- Bug de accounting: result reporta `output_count=0` con 12 estrategias en databank output.

## Propuesta (priorizada, para el agente de corrección)

1. **P1 — eliminar doble ejecución** (ganancia ~2x, riesgo medio): omitir `execute_sqx` para tasks exporter en `builder.go:29` o saltar la re-ejecución en `ImportMetadataStep`, reordenando `download_strategies` → properties → única ejecución. Cubrir con tests de `project_activity_test.go`. 74 → ~46 min.
2. **P2 — cachear reflexión + exportar solo vecindario 3x3** (riesgo bajo-medio): cache `Method/Field` por clase y extracción única por trade (`EchoForgeWFMExporter.java:1076-1116`); limitar celdas a centro+8 verificando qué consume `select_robust_run`. Cada run ~26.6 → ~5-9 min. Combinado con P1: 74 → ~20 min.
3. **P3 — particionar batch entre workers** (riesgo alto, solo si hace falta): requiere resolver directorios por request (`runtime/config.go:163-195`).
4. **P4 — higiene**: heartbeat con progreso real (tail de `wfm_exporter_<jobId>.log`), timeouts realistas sqcli, `MaximumAttempts` finito, fix `output_count`.

## Evidencia y limitaciones

- Visibility `sqx-prop`: **solo 1 run `sqx-main-*` en 90 días** (el target). Sin baseline: no verificable si 57 min es sistémico u outlier.
- Artefactos efímeros en `/tmp` (pueden no existir al leer esto): `wf_1786733372_analysis.json` (descomposición), `wfm_exporter_sqx_log_full.txt` (log SQX 393KB), `wfm_logs_filtered.txt`, `audit_wfm_runs.json` (muestreo 18 runs).
- Tool reutilizable para medir el run post-fix en el repo `symphony`: `scratch/analyze_wf_1786733372.go <WID> <out.json>` (descomposición temporal completa de cualquier workflow; conecta a `192.168.31.46:7233` ns `sqx-prop`).
- Logs del proyecto en kron-0 (`/home/kor/sqx/user/projects/EchoForgeWFMExporter/log/global_log_20260814_185627.log`) no accesibles desde la máquina local; MinIO no persiste logs del wfm_exporter.
- Subagentes: troubleshooter (muestreo masivo + logs) y general-purpose (revisión Go/Java). No se modificó código productivo; scratch quedó limpio.
