---
type: change_log
schema_version: 1
scope: session
created: "2026-09-17"
updated: "2026-09-17"
area: "[[Echo]]"
project: "[[Echo + Echo Forge — Deferred Certification Backlog]]"
application: "[[xKoRx/symphony]]"
entities:
  - "[[Echo Forge]]"
  - "[[Echo]]"
related:
  - "[[Echo Forge — F-04 Magic allocation, version seal and handoff]]"
  - "[[AGENT-PLATFORM - MCP Access Plane]]"
aliases: []
confidence: verified
source_session:
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-09-17-f05c-cert-f04-01-exec-blocked

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `10-projects/Echo/agentes/Echo + Echo Forge — Deferred Certification Backlog.md` (nuevo delta fechado `2026-09-17 — Ejecución CERT-F04-01` con veredicto `BLOCKED` + actualización de `Estado de entrada` + reemplazo de `Próxima tarea única recomendada para NORMAL`; sin cambio de clases A/B/C y sin ejecutar ningún gate posterior)
  - `80-agents/journal/agent-runs/2026-09-17-zcode-glm-5.3-flash-f05c-cert-f04-01-exec.md` (creado)

## Motivo

- Ejecución de la misión `F05C-CERT-F04-01-EXEC` tal como fue producida por el manager: un único flujo F-04 físico real bajo release `0.2.98` / `b57bfb2`, observado hasta estado terminal, con evidencia suficiente para emitir PASS o FAIL/BLOCKED con causa concreta. Prohibiciones respetadas: sin reinstalar Windows, sin tocar `StagerReconcile`, sin publicar release, sin modificar ETCD config, sin MCP nuevo, sin DB writes manuales, sin compiles manuales, sin mocks como evidencia, sin gates posteriores.

## Fuentes usadas

- [[Echo + Echo Forge — Deferred Certification Backlog]] (deltas EXEC-prep del día) y [[Echo Forge — F-04 Magic allocation, version seal and handoff]] (contrato F-04).
- Source @ worktree `b57bfb2` (`symphony-f04-cert-20260913`): structs y validación del input, `AllocateMagicV1`, `durable_apply_selected_run_workflow.go` (flag durable cableado), `artifact_compiler.go`/`durable_artifacts.go`/`persistence.go` (diagnóstico del defecto), políticas Temporal de activities MT5.
- ETCD `aranea-etcd-ro` (config efectiva `/sqx-watcher/production/*`, `/sqx-mt5-worker/production/mt5/*`, ausencia de `echo/ingest`); MinIO `aranea-minio-ro` (sólo para descartar canal de artefactos: buckets `deploy`/`examples`, sin `sqx-strategies`).
- SSH `aranea-ssh` (`sqx-zeus` staging del input y ejecución del watcher release, logs de worker; `mt5-kronos-operator` preflight y job dir), `aranea-temporal-ro` (namespace list; límite de namespace documentado), `aranea-mongo-forge-ro` (sesión caída a nivel transporte `-32003`; canal no requerido para el veredicto).
- CLI Temporal local instalado en daedalus (pre-autorizado por el delta R1 como no-MCP) para describe/show/cancel del run propio.

## Resolución aplicada

- Ejecutado el run físico: request_id `cert-f04-01-20260917T181526Z-275d2be3`, CampaignRef `d400dba0-114b-423f-b891-c34a914ce235`, WaveRef `forge-d400dba0-114b-423f-b891-c34a914ce235-w000001`, FlowRunRef `794b0e02-aae5-4ccb-820b-17294ddb7af8`; funnel completo en la ola (15 retester / 14 optimizer / 14 WFM / 3 robust / 3 apply / 3 final reretester) y **primeras allocations durables Magic V1 de F-04** (`26090011001`/`002`/`003`, namespace `forge-live`, allocation_refs durables en `sqx.strategy_magic`, stamp/readback demostrado por Apply COMPLETED bajo contrato fail-closed).
- Veredicto **`CERT-F04-01 = BLOCKED`**: `mt5_compile_artifact` falla 100% determinístico (`persistence_deadline_required`, guard `ValidatePersistenceContext` en la descarga de source durable; la actividad no envuelve su ctx con deadline) en 3/3 compile children, attempts 99→110+, worker `1700@worker-kronos@`; sin fix de source + release nueva la cadena no alcanza EvaluationRef/seal/handoff. Causa primaria única reportada con ubicación exacta y convención de fix sugerida (decisión manager).
- Terminación segura del run propio (§6): cancel del campaign parent 19:35:36Z, propagación verificada (5/5 workflows CANCELED), read model final `CANCELLED/PARENT_CANCELLED` 19:35:45Z, flota drenada (worker Windows idle con poller único; cero watchers/screens residuales; f03cert intacto).

## Validación

- El flujo fue el objeto de certificación: todas las mutaciones de pipeline (intake, MinIO, PG, allocations) provienen del flujo productivo mismo; la única mutación fuera del pipeline fue la cancelación del run propio, explícitamente autorizada por la misión y con post-condición verificada.
- Sin bypass ni completación manual del compile; sin evidencia histórica sustituyendo evidencia del run; unicidad demostrada (exactamente 1 campaña/FlowRun/ingreso).
- Vault: sólo delta documental; repos sin cambios (dirty foráneo `phase4_performance.json` preservado); ETCD sin writes; sin secretos registrados.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales sensibles, memoria interna ni secretos

## Rollback

- Revertir el delta fechado, `Estado de entrada` y sección de recomendación en el backlog y borrar este log + el agent-run; ningún otro artefacto del vault tocado. El estado físico del run es durable por diseño (allocations write-once permanecen; workflows CANCELED) y no es objeto de rollback.
