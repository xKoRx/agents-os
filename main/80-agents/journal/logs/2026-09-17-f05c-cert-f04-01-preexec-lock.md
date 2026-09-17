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

# 2026-09-17-f05c-cert-f04-01-preexec-lock

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `10-projects/Echo/agentes/Echo + Echo Forge — Deferred Certification Backlog.md` (delta fechado `2026-09-17 — Preexec lock CERT-F04-01 (corrección manager del handoff R1 aceptada; ningún gate ejecutado, ningún estado de gate cambiado)` + `updated` del frontmatter; sin cambio de clases A/B/C y sin cambio de estados de gates físicos)
  - `80-agents/journal/agent-runs/2026-09-17-zcode-glm-5.3-flash-f05c-cert-f04-01-preexec-lock.md` (creado)

## Motivo

- Misión NORMAL F05C-F04-01-PREEXEC-LOCK del manager: cerrar exclusivamente tres precondiciones que impiden autorizar CERT-F04-01-EXEC — (1) el handoff R1 usó implícitamente `deploy/manifest.json` Git (que declara 0.2.96 @ `3d0e8c9` y no contiene `deploy/0.2.98`) como si sustentara la publicación; la autoridad real del release es remota y debía demostrarse; (2) la identidad del worker Windows `worker-kronos` (PID 1700) quedaba UNKNOWN y la materialización del binario 0.2.98 Windows no demostrada (rollout 2026-09-13 INCONCLUSIVE); (3) el input canónico de CERT-F04-01 y la cláusula contractual de delivery fail-closed debían quedar congelados y citados antes de cualquier EXEC.

## Fuentes usadas

- Repo `xKoRx/symphony` @ `3d0e8c9` (HEAD == origin): `deploy/manifest.json` (0.2.96), `deployer/cmd/release-authority/main.go` (interfaz read-back read-only), `deploy/windows/sqx-mt5-worker/` (README + scripts canónicos Install/Start/Rollback), `docs/services/sqx-mt5-worker-windows.md`, `sqx/cmd/sqx-watcher/main.go` (mecanismo input/watcher), `input/example/config.json`.
- Worktree de certificación `symphony-f04-cert-20260913` @ `b57bfb2`: `deploy/manifest.json` dirty (0.2.98), artefactos `deploy/0.2.98/`, `deployer_screen.log` (registro de publicación 2026-09-13T03:20:38–41Z).
- MinIO producción vía CLI `release-authority --target 0.2.98` (sólo ListObjects/GetObject): `published_version=0.2.98`, `authority_state=CONSISTENT`, `target_state=EXACT_MATCH`.
- SSH `mt5-kronos` viewer + `mt5-kronos-operator` (sólo lecturas autorizadas): proceso `sqx-mt5-worker` PID 1700, WMI, inventario `C:\SQX`/`C:\stager`/`C:\stager_old`/`C:\ProgramData\Stager`/`C:\MT5\test`, hashes f33/f36, netstat PID 1700.
- `sqx-flowkit campaign get a9e73e66-5062-44d7-b665-22740383c676` (read models PG, exit 0): provenance recert 0.2.92.
- [[Echo Forge — F-04 Magic Allocation, Version Seal and Handoff Contract]] (§PHYSICAL, delivery matrix, D1–D18) y [[Echo + Echo Forge — Deferred Certification Backlog]] (CERT-F04-01, delta R1, preflight).

## Resolución aplicada

- Delta en el backlog que registra: precondición A PASS (autoridad remota 0.2.98: manifest publicado `worker/sqx/manifest.json` bucket `deploy` CONSISTENT EXACT_MATCH byte-exacto de 6 objetos; artefacto Windows `worker/sqx/0.2.98/windows-amd64/sqx-mt5-worker.exe` size 37250048 sha256 `0bceda4b…`; source `vcs.revision=b57bfb2c…`; publicación 2026-09-13T03:20:41Z); precondición B FAIL (Windows NO converged: PID 1700 vivo con poller Temporal establecido pero identidad no atribuible sin elevación owner; `C:\SQX` inexistente; ningún binario legible coincide con 0.2.98; receta owner emitida con scripts canónicos y paso 0 de identity read-back elevado); precondición C PASS (input canónico congelado: watcher + provenance `a9e73e66` + deltas contractuales F-04; cláusula delivery fail-closed citada del contrato §PHYSICAL); veredicto A–E: A PASS, B FAIL, C PASS, D PASS, E FAIL ⇒ **NO READY TO EXECUTE**, blocker único = convergencia Windows owner; corrección del handoff R1 registrada (los UNKNOWNs Windows sí gatean la autorización EXEC y se cierran antes de la campaña, no dentro de ella).

## Validación

- Baseline: symphony HEAD == `origin/codex/f05-release-prep` == `3d0e8c9…`; dirty ajeno `phase4_performance.json` intacto antes y después del build del CLI (verificado con `git status`).
- `release-authority` exit 0 con salida JSON completa; corrida con binario en `/tmp`, sin escribir en el repo.
- Windows: viewer `hostname` OK; todas las lecturas por operator fueron read-only (Get-Process, Get-CimInstance denegado, Get-ChildItem, Get-FileHash, netstat, Get-Service); cero instalación, cero stop/start, cero writes.
- `sqx-flowkit campaign get` exit 0, comando de lectura contractual; sin writes.
- Ningún estado de gate cambiado; sin ejecutar SQX/MT5/compile/Temporal; sin MCP nuevo; sin secretos leídos ni registrados.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Revertir el delta fechado en el backlog y borrar este log + el agent-run; ningún otro artefacto tocado.
