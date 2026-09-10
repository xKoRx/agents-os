---
type: known_error
schema_version: 1
scope: project
created: "2026-09-03"
updated: "2026-09-03"
area: "[[Echo Forge]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[xKoRx/symphony]]"
entities:
  - "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
related:
  - "[[2026-09-03-echo-forge-worker-execution-model-v1]]"
  - "[[2026-09-03-echo-forge-worker-lifecycle-mt5-orphan-plan]]"
aliases:
  - ORPHAN_MT5_PROCESS_AFTER_CANCEL
  - metatester64 orphan
confidence: verified
source_session: ECHO-FORGE-WORKER-LIFECYCLE-AND-MT5-ORPHAN-RCA-TOP
load_policy: when_error_matches
indexable: true
index_priority: high
tags:
  - kind/known-error
  - scope/symphony
  - project/echo-forge
  - tech/mt5
  - tech/temporal
  - scope/project
---

# 2026-09-03-orphan-mt5-after-cancel

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Síntoma

- Tras `CancelWorkflow` de GenericSQXWorkflow, FlowRun queda CANCELLED y `terminal64.exe` desaparece, pero `metatester64.exe` puede seguir vivo (PPID ausente). Histórico PID `10040` en Kronos Windows; revalidación 2026-09-03: proceso ya no existe.

## Causa

- `MT5ArtifactChildWorkflowOptions` no fija `ParentClosePolicy` ni `WaitForCancellation`; Temporal default TERMINATE. Generic `collectMT5ArtifactChildren` retorna en el primer `CanceledError` y sella en disconnected context antes del cleanup físico.
- `CommandExecutor` Windows: `cmd.Process.Kill()` sólo del proceso directo (`terminal64`). `metatester64` es descendiente no esperado.
- Segundo vector: restart del worker MT5 deja descendants si no hay Job Object.
- La causa no es una violación de concurrencia local SQX. La autoridad exacta del SDK `c85594440f6755443ceb97ec4e333cd0ddb5b0ed` normaliza `MaxConcurrentActivityExecutionSize == 0` a `1`, por lo que SQX y MT5 tienen concurrencia efectiva 1.

## Impacto

- C3 physical certification BLOCKED. Workspace cleanup puede correr con tester vivo. Retry N+1 sólo queda seguro si el executor bloquea el retorno hasta drenar el árbol. `context.Canceled` se clasifica como timeout en el executor y debe corregirse sólo porque puede activar retry o degradar la propagación de cancelación.

## Detección

- Temporal: child `Terminated` `reason=by parent close policy` con `ActivityTaskCancelRequested` sin `ActivityTaskCanceled`. Windows: `metatester64` sin padre. Source: `sqx/workflows/mt5_artifact_workflow.go` options; `sqx/adapters/cmd-executor/cmd_executor.go` Kill.

## Mitigación

- No matar por nombre. Si un PID concreto reaparece: FlowRun terminal + 0 activity MT5 dueña + path del run contaminado → `Stop-Process -Id` PID-specific.
- Fix: dos slices B (Temporal REQUEST_CANCEL + wait-all) y C (Windows process-tree). No existe Slice A de concurrencia ni se modifican workers. Release `0.2.87`.

## Evidencia

- FlowRun `d7693ebe-4ea8-4c10-a65e-c45d676ac788`; WorkflowID `sqx-main-v1-6726577e-d571-4399-9c04-76286bd785bd`; RunID `01a06431-52ac-7318-bb7c-31eace95736f`. RCA: `specs/FEAT-SQX-WORKER-LIFECYCLE/rca/RCA-001-orphan-mt5-after-cancel.md`.
- SDK: `go.temporal.io/sdk v1.44.1`; `WaitForCancellation` default false y `ParentClosePolicy` default TERMINATE. `NewDisconnectedContext` no propaga cancelación y sólo se usa después de solicitarla para drenar futures.
- Plan canónico: [[2026-09-03-echo-forge-worker-lifecycle-mt5-orphan-plan]].
- Gate W 2026-09-03: el primer intento falló por `WINDOWS_PROCESS_TREE_TEST_HARNESS_RECURSIVE_ROOT` (defecto TEST-ONLY del harness en `process_windows_test.go`, resuelto en commit `178d2c5fe3a3f402a633334138167f0bd3f10645`); re-ejecución Gate W 8/8 PASS demostró Job Object y drain del árbol — este known error de ORFANDAD MT5 sigue VIGENTE y no queda certificado resuelto (el gate no ejercitó cancelación MT5 productiva); la propiedad física del executor queda certificada sólo por la evidencia exacta de Gate W.
- **RESOLVED / PHYSICALLY_CERTIFIED (2026-09-03, release 0.2.88, source `7047a9c`)**: smoke de cancelación desechable — parent `sqx-main-v1-71ba89b4-c960-432b-9872-27300ab5add8` run `01a06975-35c2-779b-91c2-c0e0a1b6190a`, FlowRun `572890a4`; árbol físico `sqx-mt5-worker(20040) → terminal64(26752) → metatester64(27512)` cancelado con UN `CancelWorkflow` 23:16:24.743Z ⇒ child en ejecución `321c4d86…` ActivityTaskCanceled 23:16:38.339 + WorkflowExecutionCanceled 23:16:38.369, children encolados cancel sin dispatch físico, 0 Terminated, terminal64=0/metatester64=0 a los 14s SIN taskkill, worker/stager/poller intactos, seal tras drain. Ver [[2026-09-03-echo-forge-release-0288-cancel-smoke-certified]].
