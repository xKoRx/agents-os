---
type: agent_memory
schema_version: 1
scope: project
created: "2026-09-02"
updated: "2026-09-02"
area: "[[Personal]]"
project: "[[Echo Forge]]"
application:
entities: []
related: []
aliases: []
confidence: high
load_policy: manual
indexable: true
index_priority: high
tags:
  - kind/agent-memory
  - scope/project
  - project/echo-forge
---

# Echo Forge C3 — contaminated FlowRun drain checkpoint

## Continuidad

- El blocker correcto queda fijado como `CONTAMINATED_FLOW_HAS_ACTIVE_MT5_WORK`; no usar `WINDOWS_STALE_WORKER_HAS_ACTIVE_JOB` para este caso.
- FlowRunRef `d7693ebe-4ea8-4c10-a65e-c45d676ac788`, WorkflowID `sqx-main-v1-6726577e-d571-4399-9c04-76286bd785bd`, RunID `01a06431-52ac-7318-bb7c-31eace95736f`.
- Se emitió exactamente un `CancelWorkflow`; Temporal padre terminó `Canceled` y PostgreSQL selló `CANCELLED`. Siete hijos reportaron cancelación; un hijo quedó observado como `Terminated` con actividad `CancelRequested`.

## Señales de carga

- El worker Windows y el servicio StagerRuntime siguieron en 0.2.86; `terminal64.exe` desapareció, pero `metatester64.exe` PID 10040 persistió 30 s con parent PID 6940 ya ausente. No matar procesos, reiniciar servicios ni usar Terminate.
- La compuerta física es `ORPHAN_MT5_PROCESS_AFTER_CANCEL`; C3 queda `BLOCKED / CLOSED`. No se lanzó supply fresco ni Campaign.

## Próxima acción

- Próxima acción: retorno al lead para drenaje operativo autorizado del huérfano y nueva auditoría; no reutilizar ranking/promotion del FlowRun contaminado.
