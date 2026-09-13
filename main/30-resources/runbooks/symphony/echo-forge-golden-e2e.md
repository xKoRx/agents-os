---
type: runbook
schema_version: 1
scope: application
created: "2026-08-29"
updated: "2026-08-29"
area: "[[Echo Forge]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[xKoRx/symphony]]"
entities:
  - "[[Symphony]]"
related:
  - "[[e2e-gated-validation]]"
  - "[[symphony-release-certification]]"
  - "[[symphony-worker-runtime-proof]]"
  - "[[symphony-prod-probe]]"
  - "[[echo-forge-cross-system-triage]]"
aliases:
  - golden run Echo Forge
  - E2E físico Symphony
  - certificación final durable
confidence: verified
source_session: DURABLE-ARTIFACT-VERIFIED-READS-FINAL-E2E-NORMAL
load_policy: when_application_loaded
indexable: true
index_priority: critical
tags:
  - kind/runbook
  - scope/application
  - project/echo-forge
---

# echo-forge-golden-e2e

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Propósito

- Ejecutar la secuencia de gates de `e2e-gated-validation` para una certificación física E2E de Symphony/Echo Forge: baseline → source integrity → release → deploy/runtime proof → golden run → triage → closure.

## Precondiciones

- Runbook del ciclo con el objetivo del E2E ( gates exigidos, negative probes, criterios NO FALSE PASS); baseline autorizado y commits certificados desde el checkpoint del proyecto; los runbooks [[symphony-release-certification]], [[symphony-worker-runtime-proof]] y [[symphony-prod-probe]] cargados.

## Procedimiento

1. **Baseline + source:** ver [[symphony-release-certification]] (comandos exactos; foreign dirty `go.work.sum` se preserva).
2. **Release:** `./deploy_release.sh "" 60` desde el repo. OJO: el script hace DOS cosas — publica la release (build linux+windows, manifest, publicación MinIO confirmada por el deployer en screen) Y despacha el intake (bump de `strategy` en `input/example/config.json` y copia de `input/example/*` a `input/`). Antes de invocarlo: editar `input/example/config.json` con `wave` y `request_id` NUEVOS únicos de la sesión (formato vigente: request `final-<tema>-e2e-normal-YYYYMMDDTHHMMSSZ-<8hex>`, wave `final-<tema>-e2e-YYYYMMDD-HHMMSS`); el bump de strategy lo hace el script. Sesiones screen locales: `deployer` y `watcher` (logs `deployer_screen.log` / `watcher_screen.log`); el workflow aparece como `sqx-main-v1-<flow_intent_token>`.
3. **Deploy/runtime proof:** [[symphony-worker-runtime-proof]] con el probe en modo `queue` PRE/POST (identidades `pid@host`; requeridos Zeus, Hera, Kronos Linux y `worker-kronos` Windows en `sqx-mt5-queue`).
4. **Golden run — captura de identidad:** PG `sqx.flow_runs` (FlowRunRef `id`, `flow_intent_token`, `temporal_workflow_id`, `temporal_first_run_id`, `legacy_request_id` = RequestID, `wave_key`, `status`); progreso: `sqx.stage_executions` por `flow_run_id` (stage_key/status/generation/temporal_activity_id), historial Temporal con el probe (`hist`), objetos físicos por prefijo wave (`wave`).
5. **Golden run — estado esperado COMPLETED:** Builder → classification → early ranking → grouped child flows (Retester/Optimizer) → WFM → robust selection → Apply → FinalReretester → TradeSet → MQ5 → EX5 → MT5 Backtest HTM → Score → GLOBAL ranking; PASS exige workflow `Completed` y FlowRun `COMPLETED` (no vale llegar sólo a WFM/Apply). NO reutilizar RequestID/FlowRun/workflows de corridas previas; NO Temporal Reset.
6. **Triage ante fallo:** [[echo-forge-cross-system-triage]] (+ `write-once-conflict-triage` si hay CONTRACT_CONFLICT). Producto ⇒ preservar evidencia y cerrar BLOCKED; nunca fix/re-run en la misma sesión.
7. **Closure:** checkpoint append-only del proyecto + decisión + known-error si aplica + agent run + change log; reporte con ledger de gates, IDs exactos y NEXT EXACT nombrado.

## Validación

- Cada gate con su veredicto y evidencia pegada en el checkpoint; el estado final del worktree debe ser sólo: `go.work.sum` + `input/example/config.json` + `deploy/manifest.json` (+ `deploy/<versión>/` si no está gitignored). Última corrida registrada: 2026-08-29, release 0.2.79, BLOCKED por doble ejecución de exporter ([[2026-08-29-durable-artifact-verified-reads-final-e2e-normal]]).

## Rollback / recuperación

- Deploy abortado: seguir los mensajes de `deploy_release.sh` (nunca borrar releases a mano); flow colgado de una sesión previa: dejarlo como historia (no reset, no continue); intake duplicado: identificar por wave/request_id en PG antes de actuar.

## Evidencia

- Decisiones y known-errors del proyecto ([[2026-08-28-durable-artifact-verified-reads-final-e2e-normal]] como ejemplo de historia de intento fallido, [[2026-08-29-durable-verified-reads-exporter-double-execution]] como defecto vigente).
