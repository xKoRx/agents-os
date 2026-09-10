---
type: raw_session
schema_version: 1
scope: session
created: "2026-09-10"
updated: "2026-09-10"
area: "[[Echo]]"
project: "[[Echo Forge — F-03 SQX long-running]]"
application: "[[xKoRx/symphony]]"
entities:
  - "[[Echo Forge — F-03 SQX long-running]]"
related:
  - "[[2026-09-10-f03-sqx-long-running-summary]]"
aliases: []
confidence: verified
source_session:
load_policy: never
indexable: false
index_priority: never
tags:
  - kind/raw-session
  - scope/session
---

%% Filename: YYYY-MM-DD[-HHMM]-<human-topic>-raw.md. Never use UUIDs/hashes as visible names; put external IDs in source_session. %%

# 2026-09-10-f03-sqx-long-running-raw

> [!warning]+ Raw session L0
> Archivo de auditoría y retrofit. Excluido del retrieval normal y de Graphify.

## Contexto

- Agente: ZCode (GLM-5.3-Flash), superficie primaria; subagentes no disponibles (Token Plan error 2056).
- Proyecto o entidad: [[Echo Forge — F-03 SQX long-running]] / [[xKoRx/symphony]].
- Objetivo de la sesión: despacho NORMAL del paquete Fase 1 — ejecutar T1.1–T1.8 según SPEC, commit atómico, push, HANDOFF ≤12 líneas, session-close + feedback.

## Transcript

```
Usuario: MODELO NORMAL — F-03 SQX LONG-RUNNING. Repo xKoRx/symphony, baseline
e50cb7e obligatorio, branch feature/f03-sqx-long-running. Precondiciones:
origin/master==baseline, status CLEAN, cargar SPEC+T1.1–T1.8, STOP si baseline
cambió o dirty ajeno. CONTRATO FROZEN: sqxActivityTechnicalCeiling =
MaxInt64ns−1s; StartToClose=ceiling, ScheduleToClose=0, Heartbeat 2m,
MaximumAttempts 0, WaitForCancellation true; nada de deadlines derivados de
job/budget/config; T1.1–T1.8 exactos; sin 10d/20d LIVE; sin WithTimeout WFM/apply;
legado alineado; adaptive FORBIDDEN/NO CHANGE; MT5 no-touch. CANCEL: process-group
propio del sqcli por Execute (Setpgid, SIGTERM→SIGKILL -pgid), jamás grupo del
worker ni siblings; Canceled≠ErrorTypeTimeout, sin ErrorTypeCanceled inventado
pero permitido no-transiente en domain; recovery intacto; observabilidad duration
sin gate; MIGRATION NONE; cert SOURCE/CONTRACT/CANCEL/LIVENESS + PHYSICAL (>10m
COMPLETED + cancel de árbol) o READY FOR MANAGER REVIEW — PHYSICAL BLOCKED; git
higiene; handoff ≤12 líneas; session-close + feedback.

Agente: bootstrap AGENTS-OS OK; baseline verificado (origin/master==e50cb7e,
CLEAN); branch creado; SPEC+B1B+proyecto cargados; kill paths verificados contra
source; delegación a mm-builder falló (límite Token Plan 2056) → ejecución directa
del primario. T1.1: constante local + genericActivityOptions() + consolidación de
duplicados (idénticos campo a campo). T1.3: groupChildWorkflowOptions (REQUEST_CANCEL,
sin WorkflowRunTimeout) en ambos sitios; fix import enumspb tras 2 intentos.
T1.2: duplicado literal del ceiling en internal/workflows (2 bloques). T1.4: 10m WFM
fuera. T1.5: ensureApplyDeadline eliminada. T1.7: StartHeartbeatWithDetails en
project (reusa wfmHeartbeatDetails) + histograma duration_ms en executor-sqx.
T1.6: ErrorTypeCanceled no-transiente en domain; classifyError Canceled→canceled
(ctx y errors.Is); process_nonwindows Setpgid + terminate -pgid SIGTERM/SIGKILL 5s
sólo para DefaultTerminationPolicy; Windows intacto.
Incidentes: stash pop bloqueado por fixture phase4_performance.json mutado por
corridas de test (ruido pre-existente; restaurado y excluido); comparación vs
baseline rehecha con worktree efímero (16 fallos MT5 del worktree = dependencia
local gitignored mt5-export.htm, ausente en worktree fresco; paquete worker 100%
verde en el árbol real); data race en tests = lazy-init de telemetry.GetLogger()
del SDK, neutralizado con warmup secuencial; test que pineaba heartbeat string
estático actualizado al contrato details de T1.7; test SOURCE corregido a patrón
"WorkflowRunTimeout:".
Verificación: build sweep OK (cmd/symphony falla sólo por libzmq ausente,
pre-existente); suites tocadas verdes; -race verde; vet OK; gofmt propio OK; sets
de fallos pre-existentes idénticos a baseline (21 en sqx/workflows).
Entrega: commit a382470 atómico (15 archivos), push OK, status CLEAN.
Cierre: nota proyecto actualizada (estado/entrega/tareas/bitácora), change_log,
agent_run, L0+L1, feedback.
```

## Evidencia externa

- Commit `a382470` en `origin/feature/f03-sqx-long-running` (github.com:xKoRx/symphony).
