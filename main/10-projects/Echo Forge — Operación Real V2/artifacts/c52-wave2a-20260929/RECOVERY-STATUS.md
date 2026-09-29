# RECOVERY-STATUS.md — C5.2 Optimizer recovery (wave2a) — STAGED / BLOCKED_RUNTIME

**2026-09-28 · 17.ª sesión.** La recovery de wave1z (Full 34/34 → Optimizer → evaluate_wfm → select_robust_run → STOP) está **100% preparada y verificada en sus precondiciones durables**, y **BLOQUEADA por runtime**: la flota SQX está 2/3 porque Hera (192.168.31.111) está OFFLINE a nivel de red (100% packet loss, sin puerto 22, sin poller Temporal, sin métricas Prometheus >90 min; última versión conocida 0.2.129). El mandato exige flota 3/3 + rollout 0.2.130 certificado 3/3 antes de despachar.

## Estado por precondición

| Preflight | Estado | Evidencia |
|---|---|---|
| Cohort durable resolve 34/34 | **READY** | Mongo `forge.evaluations`: 34 OUTPUT evaluations de `c329a546-800b-494b-bace-c87fd81dae10` en `wave_wave1z/ndx/l_h1/SQX/v1/02_full_retester/`, cruce 1:1 con los 34 .sqx de MinIO, StrategyRef/EvaluationRef/SHA únicos → `FULL-RECOVERY-INPUT.csv` |
| Spec recovery válido | **READY** | `flow-recovery-c52-wave2a.json`: `ValidateWorkflowSpec` → SPEC_VALID (group `03_optimizer`, batch_size=1, max_parallel=3, `source_folder=02_full_retester`, `cohort_wave=wave1z`, `cohort_flow_run=c329a546-…`, nested optimizer+evaluate_wfm+select_robust_run; sin Final Retester/MT5) |
| Identidad libre | **READY** | `NDX_SQX_v1_wwave2a` no existe en `sqx.configs` (últimos: w1v,w1w,w1x,w1y,w1z) |
| Paquete watcher | **READY** | `<work>/watcher/input/`: JSON + `Optimizer.cfx` (sha `4b282d8b…` == freeze wave1z/vault); watcher binario 0.2.130-build desde `af8f1ae` `vcs.modified=false` (sha `464b29d1…`), screens `forge-watcher-*` viejos eliminados |
| Flota 3/3 en 0.2.130 | **BLOCKED** | Zeus 0.2.130 ✓ (PID 3243046, poller activo), Kronos 0.2.130 ✓ (PID 1683548, poller activo), Hera OFFLINE ✗ |
| Preflights que exigen host access | **BLOCKED** | SSH kor@ roto en los 3 hosts (publickey/password denied; hera además no-route): no verificable `pgrep sqcli` (riesgo GUI single-instance), presencia de `OptimizerBase.cfx` (templateFile de Optimizer.cfx) en hosts, SHA byte-exacto del binario en host |

## Runbook de desbloqueo (mecánico, cuando Hera vuelva)

1. Owner verifica/reinicia Hera (192.168.31.111). Al boot, el stager aplica 0.2.130 automáticamente (≤6 min).
2. Verificar rollout 3/3: Prometheus `symphony_sqx_activity_result_total{process_executable_path="/opt/stager/releases/0.2.130/bin/symphony"}` por host_key z0/h0/k0 con PIDs nuevos + pollers `sqx-main-queue` = 3 hosts (`/tmp/pollers`). Si hay SSH otra vez: `scripts/verify_rollout.sh` + `pgrep -af sqcli` vacío + `sha256sum /home/kor/sqx/user/configs/OptimizerBase.cfx` presente en los 3 hosts.
3. Despachar: `cd <work>/watcher && ENV=production screen -dmLS forge-watcher-wave2a bash -c './Temp/sqx-watcher input 2>&1 | tee -a watcher-wave2a.log'` (input/ ya contiene JSON+CFX; sólo UN screen).
4. Pipeline esperado en log: validate_spec → validate_configs → upload_artifacts → save_config (flow_run_ref nuevo) → dispatch_workflow → move_processed.
5. Verificar resolución: `resolve_historical_cohort` con owner `c329a546-…` → resolved=34, chunking 34×batch=1, fan-out ≤3 (children `sqx-sub-…`), memberships REPROCESSED 34.
6. Monitoreo hasta `select_robust_run` (STOP contractual): flowkit `run stages <ref>`; candidatos reales del Optimizer en Mongo `forge.evaluations` (contract `sqx-optimizer.v1`, upload `WF_Matrix`), WFM en `04_wfm/`, decisiones robust en `05_robust/`. Exportar OPTIMIZER-CANDIDATES.csv / OPTIMIZER-FUNNEL.csv / ROBUST-SELECTION-AUDIT.csv + FUNNEL-REVIEW.md.
7. Higiene: si Hera vuelve a caer a mitad de campaña, los children en Zeus/Kronos continúan (max_parallel observado 2); NO cancelar por eso.

## Riesgo aceptado si se decide despachar con 2/3 (NO recomendado, requiere owner)

El spec recovery NO depende del fix 0.2.130 (usa el camino `cohort_flow_run` probado en wave1u @ 0.2.127), pero (a) viola el preflight 3/3, (b) no verifica GUI sqcli ni `OptimizerBase.cfx` ⇒ puede quemar `wave2a` con un fallo temprano (identidad no reutilizable). Si el owner acepta el riesgo: borrar el `input/` del paquete y renombrar wave a `wave2b` NO es necesario salvo fallo real; el orden correcto es despachar wave2a sólo con preflights verdes.
