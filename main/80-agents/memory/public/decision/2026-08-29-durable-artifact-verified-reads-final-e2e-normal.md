---
type: decision
schema_version: 1
scope: project
created: "2026-08-29"
updated: "2026-08-29"
area: "[[Echo Forge]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[xKoRx/symphony]]"
entities:
  - "[[Echo Forge]]"
  - "[[AGENTS OS]]"
related:
  - "[[2026-08-28-durable-verified-reads-apply-reconciliation-rca]]"
  - "[[2026-08-29-durable-verified-reads-exporter-double-execution]]"
aliases: []
confidence: verified
source_session: DURABLE-ARTIFACT-VERIFIED-READS-FINAL-E2E-NORMAL
load_policy: manual
indexable: true
index_priority: high
tags:
  - kind/decision
  - scope/project
---

# 2026-08-29-durable-artifact-verified-reads-final-e2e-normal

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Contexto

- Sesión operacional/E2E sobre Symphony baseline autorizado `1f0880c2488b5d402390f66cf382a77313959a08` (== HEAD == origin/master tras fetch); `2fa17010` ancestro verificado (exit 0); SDK pin `v0.0.0-20260827204048-ea09cc1bb8b3` intacto y SDK repo HEAD `ea09cc1bb8b34e661c8f31f887dce58613b0475a`. Foreign dirty `go.work.sum` preservado; cero cambios de código producto.
- Gates previos PASS: BASELINE (HEAD==origin/master==1f0880c), LOAD-BEARING SOURCE INTEGRITY (los 8 archivos Apply blob-idénticos a `2fa17010`; steps/WFM congelados en `ce21d25`; MT5 Slice 2 en `5e93c7c`; write-once en `8619a50`/`5e3c2b3`; intervalo `2fa17010..HEAD` son 3 chores baadc35/6d30d0f/1f0880c sin fuentes .go/.sql funcionales — rebaseline operacional documentado).
- Release `0.2.79` construida y publicada por el mecanismo canónico `deploy_release.sh`: linux `symphony` sha256 `692f8c2115af6e48bacb65cc7bf405da866103d2e9b2ade47e9f20d61b939f6e` size 38559928; windows `sqx-mt5-worker.exe` sha256 `d8f285f758c7d3acd720756f3aa8111eec1f6b0c30118de90b43618705d5c116` size 36397056; `go version -m` demuestra `vcs.revision=1f0880c…` y SDK pin en ambos binarios (`vcs.modified=true` refleja dirty operacional no-Go del worktree). Manifest publicado en MinIO confirmado.
- Workers: Zeus (1720483→1875207), Hera (733932→757811) y Windows MT5 worker-kronos (5364→5936) rotaron proceso tras la publicación (evidencia por rotación de PIDs de pollers Temporal + stager canónico con binarios sha256-pineados en manifest; sin canal directo de lectura de versión por host). Kronos Linux (sqx-ulab-kron-0, PID 710524) NO rotó en toda la sesión; ninguna actividad del golden run se ejecutó en él (activities observadas: hera 757811 y builder bajo cohort z0/Zeus).
- Nueva ejecución NORMAL sin reuso: RequestID `final-verified-reads-e2e-normal-20260829T174450Z-33a12fb9`, wave `final-verified-reads-e2e-20260829-174450`, FlowRunRef `1e560644-8b39-4ddb-bede-eb2c98e33238`, FlowIntentToken `d3e8faf5-8dd3-4f0e-9889-b44460086e1d`, WorkflowID `sqx-main-v1-d3e8faf5-8dd3-4f0e-9889-b44460086e1d`, RunID `01a04ea2-2cc2-7237-b76e-02802b09206a`; strategy `example_flow_24`.

## Decisión

- NO cerrar `ARTIFACT_VERIFIED_READS`. La certificación física final queda `BLOCKED / CLOSED` por un defecto de producto detectado en runtime: doble producción de `metadata/export_run.json` dentro del mismo flow — una ejecución fantasma de la tarea `overview_exporter` (subida 17:48:38Z con identidad completa del flow, job sqx `20260829_174811`, 20 estrategias del builder) que NO aparece en el historial Temporal, y el intento registrado (scheduled 17:47:51, started 17:50:51, failed 17:51:36, attempt 1, identity 757811@sqx-ulab-hera-0) que re-ejecutó el export y reintentó la subida con bytes distintos.
- El contrato write-once falló cerrado correctamente: `bytes differ: artifact checksum mismatch` → `CONTRACT_CONFLICT` NON-RETRYABLE, `DOWNSTREAM_CONSUMER_CALLS: 0`, sin overwrite físico. Workflow `Failed`, FlowRun `FAILED` (builder COMPLETED, stage `project@sqx-overview.v2` COMPLETED por la activity 11 con temporal_activity_id=11).
- Siguiente RCA exacto: `DURABLE-VERIFIED-READS-EXPORTER-DOUBLE-EXECUTION-RCA-TOP` (ver [[2026-08-29-durable-verified-reads-exporter-double-execution]]). No se aplicó fix, no se re-corrió el flow, no Temporal Reset, cero cambios de código.

## Rationale

- Línea física temporal: builder (activity 11) corrió 17:47:26→17:47:50 en Zeus (cohort z0, 20 .sqx + export_run.json/overview.ndjson/monthly.ndjson en `01_builder/`); classification 17:47:50.9; early_rank 17:47:51.06; ventana de rollout de workers 17:47:51→17:50:51 con la cola vacía; subida fantasma a `wave_final-verified-reads-e2e-20260829-174450/xauusd/l_h1/example_flow_24/v1/metadata/` (export_run.json 848B sha256 `a6d3fdaafc7e2f25e962e1c90180b0cd2e544e6f46aedfcaf757f20f380e086a` + monthly.ndjson 1502792B + overview.ndjson 431273B, todos 17:48:38.4-.8Z) con metadatos X-Sqx-* del flow y job sqx ejecutado 17:48:11→17:48:32; el intento Temporal registrado arrancó 17:50:51 (2m13s después de la subida fantasma) y chocó con el conflicto a la primera subida del batch (orden alfabético: export_run.json).
- El flow viejo `16017335` (wave `test`) no subió ningún objeto el 2026-08-29 (listado MinIO vacío para ese prefijo en el día) ⇒ la subida fantasma no proviene del flow 0.2.78; el watcher local no registró actividad a las 17:48; el channel de etcd `version` es estático (0.0.21) y Loki no contiene logs de workers ⇒ la demostración de versión por worker quedó limitada a rotación de pollers + manifest pineado (gap de observabilidad registrado como feedback).
- Las tareas exporter (`overview_exporter`, `wfm_exporter`) no participan del sistema durable de stage executions (steps.go:1489) ⇒ no tienen execution-intent idempotente que impida doble producción; el write-once del plano de artefactos fue la única barrera y actuó como red de seguridad fail-closed.

## Consecuencias

- Gates del runbook NO ejecutados por no alcanzados: STRATEGY_REF_CONTINUITY, cadena F→M→E→H, APPLY producer authority/evidence/bytes, COMPLETED replay, negative probes 1-10, authority audit, write-once regression probe de esta sesión (el contrato write-once sí quedó ejercitado en producción real por el conflicto mismo: same-key different-bytes → CONTRACT_CONFLICT, overwrite ZERO).
- Release 0.2.79 queda desplegada en Zeus/Hera/MT5; Kronos Linux pendiente de rotación (verificar stager antes del siguiente E2E).
- El flujo viejo `16017335` (0.2.78) permanece RUNNING en Temporal/PG como historia; no se tocó.
- NEXT EXACT: RCA read-only de la doble ejecución del exporter y del write fantasma fuera del historial Temporal en ventana de restart; corrección separada bajo regla FIX → NEW RELEASE → NEW REQUEST ID → NEW FLOW RUN.

## Alternativas descartadas

- No se reinterpretó el conflicto como transitorio ni se re-lanzó un segundo flow para "completar la certificación": la causa de la escritura fantasma es desconocida y un PASS sin explicación violaría NO FALSE PASS.
- No se clasificó como INFRA remediable: la subida fantasma tiene identidad completa del flow (wave/strategy/request/workflow en contenido y metadatos) y un job sqx real ejecutado en un worker host; su mecanismo (entrega Temporal no registrada vs. job async de sqx vs. carrera de restart) está sin determinar.
