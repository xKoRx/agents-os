---
type: change_log
schema_version: 1
scope: session
created: "2026-10-15"
updated: "2026-10-15"
area: "[[Aranea]]"
project: "[[Echo Forge — Robust Run Selection V2]]"
application:
entities:
  - "[[Echo Forge — Robust Run Selection V2]]"
related:
  - "[[2026-10-15-zcode-glm53-echo-forge-stager-session-supervisor]]"
  - "[[2026-10-15-echo-forge-mt5-runtime-hardening-evidence]]"
aliases: []
confidence: verified
source_session:
source_feedbacks:
  - "[[2026-10-15-echo-forge-stager-recovery-session-feedback]]"
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-10-15-echo-forge-stager-session-supervisor-deploy

Cambios de la sesión one-shot "ECHO FORGE — STAGER ACTIVATION RECOVERY / FINAL ROLLOUT 0.2.143" (ZCode/GLM-5.3-Flash, manager GPT-6). Veredicto: recuperación de la activación 0.2.142 + despliegue 0.2.143 Windows/Linux + Gate B canario PASS. Cierra el bloqueo `BLOCKED_INFRA` dejado por [[2026-10-15-echo-forge-mt5-gateb-final-remediation]] (misma fecha, sesión previa).

## Repo `xKoRx/stager` (commits `88cde8e` + `83ed477` + `32e1554`, pusheados a origin/master sobre `083dff2`)

- Nuevo driver de runtime **`windows-session-supervisor`** (`internal/runtime/session.go` + `session_windows.go` + stubs por OS): puerto de activación **observation-only** que admite `signal-accepted`/`running-observed` sólo cuando existe un proceso vivo cuyo ejecutable es el entrypoint stageado de la release pedida (`releases/<release>/<entrypoint>`); rechaza procesos duplicados, rutas inseguras y releases sin stagear con `ErrRuntimePending` (reconcile `pending` idempotente). El supervisor interactivo conserva la propiedad única del proceso; el stager conserva la state machine durable. Los adaptadores `windows-scm` y `systemd` quedan intactos (tests de factory lo fijan).
- Fix CLI: `stager status --json` resolvía mal el target config con el subcomando `status` (fallaba siempre); ahora lo resuelve por `STAGER_TARGET_CONFIG`.
- `validRuntimeTarget` acepta el nuevo driver; fixture de config test OS-agnóstico (`filepath.IsAbs` differía en Windows — defecto detectado ejecutando las suites sobre el host físico).
- Despliegue en worker-kronos: `bin\stager.exe` (SHA256 `18b103399d93…`, luego `df237440f14f…` con el fix CLI) + `target.yaml` con `driver: windows-session-supervisor`, `target: EchoForgeMT5WorkerSession`. Respaldo previo completo en `C:\ProgramData\Stager\backup-20261015-stager-fix\` (estado, marcadores legacy, XMLs de tareas, binario anterior).

## Host worker-kronos (via aranea-ssh `mt5-kronos-admin`)

- Activación `65771612…` (0.2.141→0.2.142, `signaled` sin ack desde 19:21Z) **recuperada por eventos del coordinador** (sin tocar `ACTIVATION.json`/`CURRENT`/`RUNNING` a mano, sin arrancar StagerRuntime): prueba lógica — `Request` rechaza activaciones no terminales, y la nueva activación se creó con `from=0.2.142` ⇒ la prevista alcanzó terminal `committed` primero.
- Activación `b6a3a8e2…` 0.2.142→0.2.143 `committed` 23:44:01Z (dos pases de reconcile: stage desde MinIO con SHA verificado → CURRENT flip → supervisor interactivo hizo kill 0.2.141-PID 780 → launch 0.2.143-PID 29292 en ≤30 s). Worker vivo: `releases\0.2.143\bin\sqx-mt5-worker.exe`, SHA256 `50f61b638a043af566bb4bc3764bbeb293eb08f64d480bb25954b345478b7fe3` (exacto al manifest), proceso único, pollers Temporal `sqx-prop`/`sqx-mt5-queue`, `env=production`. `StagerReconcile` `Last Result: 0` estable (noop idempotente). Servicio `StagerRuntime` sigue Stopped+Disabled y **nadie lo arrancó**.
- Gate B canario (worker 0.2.143): workflow existente `MT5BacktestArtifactWorkflow` con `smoke_canary: true`, EX5 durable auténtico 89171ea6 (SHA `92b025f2…`), config certificada NDX_SQX H1 2025.07.01–2026.10.14. Primera pasada (r1) reutilizó evidencia derivada del mismo SourceKey (gate §14 `reuseBacktestArtifact`) sin backtest físico ⇒ re-despacho sobre stem nuevo `smoke-canary-02143-20261015/` (r2): backtest REAL ~4.3 min, HTM 2 029 826 B (`c5a960e7…`), evidencia completa en MinIO, smoke del slot-1 `status=PASS build=6230 htm_build=6230 parser_contract=mt5-report.v1 normalizer_contract=mt5-normalize.v1 trades_closed=145 deals=290`, superscripción conservada. Lease liberada; worker singleton sano; sin terminales huérfanos.

## Flota Linux (zeus/hera/kronos, via aranea-ssh `sqx-*`)

- 3/3 en 0.2.143: CURRENT (root+state)=0.2.143, RUNNING por activación propia (`544343e8`/`0c174b5b`/`b07ac095`), `stager-runtime.service`+`stager.timer` activos, hashes de `bin/symphony` `202bee0c…`, `bin/sqx-watcher` `7060c92d…`, `bin/run-symphony` `8f240eb2…` byte-iguales al manifest publicado (bucket `deploy`, key `worker/sqx/manifest.json`, etag `e05e1cb4…`). Driver `systemd` intacto (paridad del requisito "adaptadores existentes preservados").

## Sin cambios

- Echo (cero llamadas), wave3t, cinco finalistas, Robust V2, Fidelity, ranking. `LiveUpdate 6230`: el terminal ya corre build 6230 y la evidencia Gate B quedó ligada a él (`terminal_sha256 5ece7395…`, `build=6230`) — el pendiente owner de LiveUpdate queda materialmente resuelto por la evidencia vigente.
- Restricción conocida intacta: logon manual post-reboot (sin autologon, sin credenciales).
