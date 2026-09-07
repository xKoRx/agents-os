---
type: decision
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
  - "[[2026-09-03-deploy-release-only]]"
  - "[[2026-09-03-mt5-artifact-timeout-authority]]"
  - "[[2026-09-03-orphan-mt5-after-cancel]]"
  - "[[2026-09-01-release-version-authority]]"
aliases:
  - RELEASE 0.2.88 CANCEL SMOKE CERTIFIED
  - ORPHAN_MT5 resuelto
confidence: verified
source_session: ECHO-FORGE-RELEASE-0.2.88-RELEASE-ONLY-AND-MT5-CANCEL-SMOKE-NORMAL
load_policy: when_project_loaded
indexable: true
index_priority: high
tags:
  - kind/decision
  - scope/project
  - project/echo-forge
  - tech/mt5
  - tech/release
---

# 2026-09-03-echo-forge-release-0288-cancel-smoke-certified

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Contexto

- Source authority `7047a9c112502dcb68387745149eed95405b0aae` == HEAD == origin/master (fixes congelados `67db6f9` timeout/retry MT5 + `7047a9c` --release-only); SDK pin `c85594440f6755443ceb97ec4e333cd0ddb5b0ed`. Physical release previa `0.2.87`; `ORPHAN_MT5_PROCESS_AFTER_CANCEL` OPEN; C3 BLOCKED/CLOSED.

## Decisión

- RELEASE-ONLY 0.2.88 CERTIFICADA: aislamiento de input demostrado SHA256(`input/example/config.json`) `2204bf0f…9ed40` idéntico before/after, cero archivos nuevos en `input/`, cero FlowRun/Workflow/watcher-delivery causados por la release. `./deploy_release.sh --release-only 0.2.88` publicó manifest 0.2.88 (`sha256 7d11437f…a26c1`; linux symphony `241d2499…7cf21b`; windows sqx-mt5-worker.exe `449c80cb…a06ac`) con `vcs.revision=7047a9c…` y SDK pin `c855944…` en ambas plataformas; flota 4/4 convergió (zeus `2306392`, hera `944368`, kron-linux `951302`, win `20040`) con SHA on-host == manifest.
- CANCEL SMOKE PASS: smoke disposable RequestID `mt5-cancel-smoke-0.2.88-20260903T221548Z-c3ce5fee`, wave `mt5-cancel-smoke-0.2.88-20260903T221548Z`, FlowRun `572890a4-f3fc-43c1-ad08-7509b3a8e1fe`, parent `sqx-main-v1-71ba89b4-c960-432b-9872-27300ab5add8` run `01a06975-35c2-779b-91c2-c0e0a1b6190a` (iniciado 22:48:04Z, post-rollout, sobre flota 0.2.88). Árbol físico capturado `sqx-mt5-worker.exe(20040) → terminal64.exe(26752) → metatester64.exe(27512)`; UN CancelWorkflow al parent 23:16:24.743Z; parent Canceled 23:16:38.473Z; FlowRun PG CANCELLED; child físicamente en ejecución `321c4d86…` (ActivityTaskStarted 23:15:01.638 attempt=1 en `20040@worker-kronos`) → ActivityTaskCanceled 23:16:38.339 → WorkflowExecutionCanceled 23:16:38.369; 2 children encolados cancel limpio (`ACTIVITY_ID_NOT_STARTED`, cero dispatch físico); 0 Terminated; terminal64=0 y metatester64=0 a los 14s del cancel sin taskkill; StagerRuntime(38460)/worker(20040)/poller intactos con topología canónica; seal `flow_run_seal` (zeus 2306392) ejecutado 23:16:38.407 DESPUÉS del drain del último child y ANTES del cierre del parent.
- Hito de timeout: el backtest físico #1 (23:04:42→) cerró por el SAFETY timeout efímero de 10m ANTES del cancel (ActivityTaskCompleted 23:15:01.615, exactamente 10m19s tras el start; startToClose visible 12m0s = 10m+2m; attempt=1, retryMax=3 sin uso) — evidencia física del contrato congelado [[2026-09-03-mt5-artifact-timeout-authority]] operando (drain + carrier funcional `backtest_timeout`, sin retry infra).
- `ORPHAN_MT5_PROCESS_AFTER_CANCEL`: RESOLVED / PHYSICALLY_CERTIFIED. `ECHO_FORGE_MT5_CANCELLATION_LIFECYCLE_FIX` y `ECHO_FORGE_WINDOWS_PROCESS_TREE_OWNERSHIP`: PHYSICALLY_CERTIFIED / FROZEN. REPLAY PASS×2 (worktree detached `7047a9c`): histórico contaminado `sqx-main-v1-6726577e…/01a06431…` 654 eventos y smoke fresco 470 eventos, nondeterminism=NONE ambos (el replayer debe inicializar DI production etcd+telemetry porque `handleGroupTask` lee globals de DI dentro del workflow).
- Auditoría final: `published=0.2.88 remote_max=0.2.88 CONSISTENT target_state=EXACT_MATCH`; cero 0.2.89; cero workflows abiertos; dirty foráneo idéntico al preflight.

## Rationale

- La misión exigía certificar cancelación MT5 sobre binario nuevo sin contaminar el slot ni gastar pipeline físico completo: cancelación apenas confirmado el árbol real, timeout de seguridad 10m, y un único smoke desechable.

## Consecuencias

- C3 permanece BLOCKED/CLOSED por decisión de la misión (certificación Campaign diferida); NO marcar Campaign Stop Policy como físicamente certificado. NEXT EXACT `ECHO-FORGE-C3-LEAN-RECERT-DESIGN-TOP` (PLAN/DESIGN primero; evaluar eliminar SUPPLY standalone usando CERT-A como prueba de promoción nonempty; NO ejecutar hasta aceptación del plan lean).
- Deuda operacional detectada: un blip de red macOS dejó procesos Go locales longevos (deployer/watcher en screen) con `dial tcp 192.168.31.92:9000: no route to host` persistente pese a LAN sana; el wrapper no puede resumir con target AVAILABLE y layout local existente (`no overwrite ni resume`) — la recuperación canónica fue `restart_deployer` replicado a mano (kill orphans → screen → boot → kick touch+manifest).

## Alternativas descartadas

- Re-ejecutar el wrapper para resumir: muere por diseño (`ya existe localmente pero target_state=AVAILABLE`).
- Esperar recuperación del deployer viejo: su stack de red quedó roto por-proceso; el propio wrapper contempla reinicio canónico.
