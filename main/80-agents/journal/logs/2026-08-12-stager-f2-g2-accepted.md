---
type: change_log
schema_version: 1
scope: session
created: "2026-08-12"
updated: "2026-08-12"
area: "[[Echo]]"
project: "[[Stager - Cross-Platform Deployment Lifecycle]]"
application: "[[stager-app]]"
entities:
  - "[[Stager - Cross-Platform Deployment Lifecycle]]"
related: []
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

# Stager F2 — G2 aceptado + canary flota Linux

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `10-projects/Echo Forge/agentes/Stager - Cross-Platform Deployment Lifecycle.md`
  - `stager/specs/STAGER-DEPLOYMENT-LIFECYCLE/VERIFICATION.md`
  - `stager/specs/STAGER-DEPLOYMENT-LIFECYCLE/TASKS.md`
  - `stager/internal/runtime/exec_windows.go`
  - `stager/deploy/windows/install-stager.ps1`

## Motivo

- Cerrar F2.8/G2 con evidencia real Windows + Zeus, y desplegar el mismo canary runtime aislado en Hera/Kronos.

## Fuentes usadas

- Matriz Windows owner-operated; canary Zeus/Hera/Kronos vía SSH; suites locales Go/vet/cross-build.

## Resolución aplicada

- Windows Stop: AttachConsole + Ctrl-Break (Interrupt SCM no soportado). Installer: CIM repetition PS 5.1.
- Linux: `/opt/stager` + solo `stager-runtime.service` (sin `stager.timer` en canary). G2 ACCEPTED. Hera/Kronos mismo layout.

## Validación

- Windows: install/stop/ACL/reboot PASS. Zeus: stop/perms/reboot PASS. Hera/Kronos: `active` + `CURRENT=f28-canary` + `symphony-worker` active.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin secretos

## Rollback

- Uninstall `stager-runtime.service` en los tres Linux; Windows `uninstall-stager.ps1`. Estado `/opt/stager` y `%ProgramData%\Stager` se conserva a propósito.
