# Echo Forge — Operación Real V2 — Freeze arquitectónico fleet fan-out — Change Log

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - main/10-projects/Echo Forge — Operación Real V2/Echo Forge — Operación Real V2.md (decisión R12 añadida al registro de decisiones; bitácora 15.ª añadida)
  - repo xKoRx/symphony master `3a79654`+`b2e321d` (pushed; ver agent-run para detalle de archivos)

## Motivo

- Mandato owner "ECHO FORGE — FREEZE ARQUITECTÓNICO / FLEET FAN-OUT / SQX CONCURRENCY / AGENTE TOP" (2026-09-28): cerrar y congelar como autoridad arquitectónica el paralelismo SQX certificado físicamente en wave1z @ 0.2.129, sin rediseño ni reapertura.

## Fuentes usadas

- [[Echo Forge — Operación Real V2]] (bitácora 14.ª: implementación + certificación wave1z; decisiones R1–R11).
- Repo xKoRx/symphony @ `021ce14` (master, limpio): `sqx/cmd/sqx-worker/main.go`, `sqx/workflows/generic_workflow.go` (`runGroupChunksParallel`), `sqx/workflows/group_parallel_children_test.go`, `sqx/core/runtime/{config,mt5_task_config}.go`, `sqx/activities/watcher/steps.go`, `specs/FEAT-SQX-WORKFLOWS-GENERIC/SPEC.md`, `.agents/skills/forge-wave-dispatch/SKILL.md`.
- Evidencia física Temporal namespace `sqx-prop` (helper efímero RO `~/aranea/work/forge-precision-shot1-20260926/ephemeral/wave1z-history/`): root wave1z `sqx-main-v1-a92c7ab1` (FlowRun `c329a546`) con children `subflow-0/1/2` minteados 02:58:27.112Z y arrancados en <110 ms.

## Resolución aplicada

- R12 (FLEET_FANOUT_ARCHITECTURE_FROZEN) registrada como decisión del proyecto: fleet fan-out es autoridad arquitectónica; revertir groups durables sin source a dispatch secuencial está prohibido salvo defecto material de corrección demostrado y reapertura explícita del owner.
- SAFETY congelada en código: `MaxConcurrentActivityExecutionSize: 1` explícito en `sqxTemporalWorkerOptions` + test permanente `TestSQXTemporalWorkerOptions_SerializesActivities` (no es knob ETCD).
- Preflight watcher fail-closed: `runtime.VerifySpecMaxParallelPreserved` (JSON bruto vs spec parseado antes de persistir/despachar) + 6 tests; wiring en `sqx/activities/watcher/steps.go` tras `ValidateWorkflowSpec`.
- Test de refill determinista `TestGroupParallelChildren_SlidingWindowRefillOrder` (max_parallel=3, 5 lotes: ventana inicial exacta, refill tras el primer completion con los demás en vuelo, concurrencia máxima == 3 exacto, exactly-once, merge == secuencial).
- SPEC `FEAT-SQX-WORKFLOWS-GENERIC` §4.4 FROZEN (invariante/safety/compatibility/failure/preflight) y skill `forge-wave-dispatch` reconciliada (regla anti-max_parallel 2026-09-27 SUPERSEDED, historia conservada; baseline Precision 90 / Full 10 / Optimizer 1 con max_parallel 3).

## Validación

- Suite afectada: `go test ./sqx/workflows/ ./sqx/core/runtime/ ./sqx/activities/watcher/... ./sqx/cmd/sqx-worker/... ./sqx/cmd/sqx-mt5-worker/...` — todos los paquetes verdes salvo el fail-set preexistente de `sqx/workflows` (22 fallos idénticos a master limpio, diff vacío salvo timings; comparación con `git stash -u`).
- Commits pushed a origin/master (`021ce14..b2e321d`); sin release ni rollout (la flota ya corre 0.2.129; el preflight watcher sube con la próxima release natural).
- Nota de higiene del vault: existe una COPIA STALE del proyecto en `main/10-projects/Echo Forge/Echo Forge — Operación Real V2.md` (152 líneas, sin bitácora 14.ª); la canónica activa es `main/10-projects/Echo Forge — Operación Real V2/Echo Forge — Operación Real V2.md`. El edit accidental en la copia stale fue revertido; recomendación: consolidar duplicados con agents-os-entity-lifecycle (no ejecutado en esta sesión, fuera de mandato).

## Cierre H (post-edición inicial)

- Refill natural capturado (06:55:34Z): subflow-2 COMPLETED 06:47:36.188Z → subflow-3 START_CHILD 06:47:36.239Z con subflow-0/1 aún en vuelo; firma sqcli del completion en Zeus (PID 3117769), Kronos/Hera con sqcli en vuelo. Evidence pack `~/aranea/work/forge-precision-shot1-20260926/EVIDENCE-FLEET-FANOUT-REFILL-20260928.md`. Bitácora 15.ª y agent-run actualizados con el resultado.
