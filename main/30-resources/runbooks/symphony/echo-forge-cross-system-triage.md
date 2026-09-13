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
  - "[[distributed-incident-triage]]"
  - "[[write-once-conflict-triage]]"
  - "[[symphony-prod-probe]]"
aliases:
  - triage multi-sistema Echo Forge
  - forense Temporal/MinIO/PG
confidence: verified
source_session: DURABLE-ARTIFACT-VERIFIED-READS-FINAL-E2E-NORMAL
load_policy: when_application_loaded
indexable: true
index_priority: high
tags:
  - kind/runbook
  - scope/application
  - project/echo-forge
---

# echo-forge-cross-system-triage

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Propósito

- Aplicar `distributed-incident-triage` (y `write-once-conflict-triage` cuando corresponde) sobre el ecosistema Echo Forge: Temporal (ns `sqx-prop`) + MinIO (`sqx-strategies`, `deploy`) + PostgreSQL control (`sqx.*`) + Mongo evidence (`forge`) + watcher/deployer locales + workers remotos (sin logs accesibles).

## Precondiciones

- Probe read-only vigente ([[symphony-prod-probe]]); IDs de la corrida (FlowRun, workflow, wave) desde PG o el intake.

## Procedimiento

1. Fuentes por subsistema y cómo consultarlas: Temporal → probe `hist` (eventos con timestamps, act, attempt) y `wf` (estado); MinIO → probe `wave` (listing con timestamps de escritura = side effects físicos) y `obj` (metadata X-Sqx-* con wave/strategy/workflow/run + contenido); PG control → `sqx.flow_runs`, `sqx.stage_executions` (temporal_activity_id enlaza evento↔stage), `sqx.evaluations`, `sqx.stage_producer_outputs` (pg `trading_systems`-schema según ambiente); Mongo `forge` → evaluations/trade_sets; locales → `watcher_screen.log` / `deployer_screen.log` (grep por ventana horaria, cuidado con días previos en el mismo log); workers → SIN logs accesibles (ver matriz [[symphony-worker-runtime-proof]]): la ausencia se declara, no se infiere.
2. Timeline normalizada: volcar a una sola línea de tiempo (UTC) los eventos Temporal, los timestamps de objetos MinIO, los created_at de PG y los hits de logs locales; identificar el actor de cada entrada (activity id, proceso, watcher).
3. Correlaciones que decidieron casos reales: un side effect físico cuyo único actor aparente "no está registrado" suele ser un INTENTO ANTERIOR de la misma activity task — OJO: Temporal escribe `ActivityTaskStarted` de forma perezosa y la cardinalidad de eventos NO informa intentos; capturar siempre el campo `attempt` (caso 2026-08-29: subida 17:48:38Z pareció fantasma porque el started registrado era 17:50:51; el RCA ([[2026-08-29-exporter-double-execution-root-cause]]) demostró que fue un intento previo de la misma task regenerando bytes no deterministas); conflicto write-once ⇒ el rechazo es correcto, investigar al duplicado con `write-once-conflict-triage`; `CONTRACT_CONFLICT` non-retryable en history ⇒ no es transient, no esperar retries.
4. Clasificación causal con descartes explícitos (cada hipótesis se elimina CON evidencia, ej. "flow 0.2.78 descartado: su wave no tiene objetos escritos hoy"); salidas: PRODUCT / INFRA / VERSION_SKEW / EXTERNAL / INCONCLUSIVE.
5. Preservar: hashes de objetos, keys completas, IDs (FlowRun/workflow/run/activity), queries usadas; notes canónicas (decisión + known-error) antes de cerrar sesión.

## Validación

- Caso resuelto de referencia: [[2026-08-29-durable-verified-reads-exporter-double-execution]] (timeline completa, clasificación producto/orquestación, contract health fail-closed OK).

## Rollback / recuperación

- El triage es read-only; nada que revertir. Remedios de infra (reiniciar watcher/deployer locales en screen, esperar rotación de stager) sólo tras clasificar y documentando.

## Evidencia

- [[2026-08-29-durable-artifact-verified-reads-final-e2e-normal]] y checkpoint del proyecto; feedback de canales muertos en [[2026-08-29-symphony-worker-observability-session-feedback]].
