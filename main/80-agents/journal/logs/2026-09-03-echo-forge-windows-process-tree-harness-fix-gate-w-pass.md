---
type: change_log
schema_version: 1
scope: session
created: "2026-09-03"
updated: "2026-09-03"
area: "[[Echo]]"
project: "[[Echo Forge]]"
application: "[[Symphony]]"
entities:
  - "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
related:
  - "[[2026-09-03-zcode-glm-echo-forge-windows-process-tree-harness-fix-gate-w-pass-normal]]"
aliases: []
confidence: verified
source_session: "ECHO-FORGE-WINDOWS-PROCESS-TREE-HARNESS-FIX-AND-GATE-W-NORMAL"
source_feedbacks:
  - "[[2026-09-03-echo-forge-windows-process-tree-harness-fix-gate-w-pass-session-feedback]]"
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-09-03-echo-forge-windows-process-tree-harness-fix-gate-w-pass

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `symphony` repo `sqx/adapters/cmd-executor/process_windows_test.go` (commit `178d2c5fe3a3f402a633334138167f0bd3f10645` `test(sqx): isolate windows process helper`, parent `033076d7eb20a9871a3172283c5a2543eeebee1d`, pushed origin/master)
  - `10-projects/Echo Forge/agentes/Echo Forge - Arquitectura de Datos y Migración de Persistencia.md` (checkpoint append-only)
  - `80-agents/journal/agent-runs/2026-09-03-zcode-glm-echo-forge-windows-process-tree-harness-fix-gate-w-pass-normal.md`
  - `80-agents/journal/feedback/system-1/2026-09-03-echo-forge-windows-process-tree-harness-fix-gate-w-pass-session-feedback.md`

## Motivo

- El Gate W de release 0.2.87 estaba bloqueado por `WINDOWS_PROCESS_TREE_INTEGRATION_FAILED`; el harness del test Windows relanzaba la suite completa de forma recursiva (clasificación hija `WINDOWS_PROCESS_TREE_TEST_HARNESS_RECURSIVE_ROOT`) y dejó 910 procesos huérfanos que agotaron el commit charge del target.

## Fuentes usadas

- Checkpoint canónico del proyecto, `process_windows_test.go`/`process_windows.go`/`cmd_executor.go` del repo, credenciales canónicas de acceso SSH/SFTP al target y evidencia física recopilada en la sesión.

## Resolución aplicada

- Fix TEST-ONLY: root del harness siempre invocado como `TestWindowsProcessHelper` con `-test.run=^TestWindowsProcessHelper$` y `SYMPHONY_CMD_EXECUTOR_HELPER_MODE` explícito por test vía `t.Setenv`; guard anti-invocación ambigua en el helper; timing deadline/grace 100ms→2s para eliminar race de arranque del árbol. Sin cambios productivos. Recovery operativa del residuo del propio defecto: kill PID-specific de los 910 huérfanos de la imagen del test binary previo (producto intacto) y purga de 20349 temp dirs de test.

## Validación

- gofmt, `git diff --check`, `go test`, `go test -race`, `go vet` (nativo y GOOS=windows) PASS; cross-compile desde `178d2c5`; SHA256 local==remota `0662763e…88b44dc8`; Gate W real en Kronos Windows 8/8 PASS con timeout externo 15min no consumido; árbol físico demostrado por sampler (suite→root→child con filter, grandchild certificado por el test); NO-RESIDUE y limpieza confirmada de artefactos de la sesión.

## Compartibilidad

- **Scope:** local / team
- **Redacción revisada:** sin identidad, paths locales de máquina, memoria interna ni secretos

## Rollback

- `git revert 178d2c5` en symphony (test-only, sin efecto runtime); la recuperación del target no requiere rollback (solo eliminación de procesos/artefactos del test).
