---
type: runbook
schema_version: 1
scope: application
created: "2026-08-13"
updated: "2026-08-13"
area: "[[Echo]]"
project: "[[Stager - Cross-Platform Deployment Lifecycle]]"
application: "[[stager-app]]"
entities:
  - "[[stager-app]]"
related:
  - "[[stager-windows-powershell-crlf-current]]"
  - "[[stager-windows-occupieddrain-delay-misses-started]]"
  - "[[stager-mt5-heartbeat-late-started]]"
aliases:
  - cutover sqx-mt5-worker StagerRuntime
  - DrainWait OccupiedDrain
confidence: verified
source_session: b0ed3608-24c7-460f-85e5-9415cc34d06a
load_policy: when_project_loaded
indexable: true
index_priority: high
tags:
  - kind/runbook
  - scope/application
  - area/echo
  - app/stager
  - os/windows
---

# stager-windows-mt5-cutover-and-occupieddrain

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Propósito

- Reemplazar `sqx-mt5-worker.exe` bajo `StagerRuntime` y armar OccupiedDrain con `Stop-Service` inmediato.

## Precondiciones

- PowerShell **Admin** en `MT4-TEST`. Pack en Mac `stager/tmp/stager-f33-windows/` o `Desktop/stager-f36-cutover/`.
- Worker esperado sha256 `fc9895b6a855010f8390e461c3f2a5aeecb69caf3c9789e2e75d4dfb159e7a0e`.
- Script ASCII con texto `Stop-Service StagerRuntime NOW`. Destino `C:\stager\` (no `C:\staging\`).
- CURRENT LF: [[stager-windows-powershell-crlf-current]].

## Procedimiento

1. Copiar `sqx-mt5-worker-f36.exe` y `Invoke-F35F36Evidence.ps1` a `C:\stager\` (Finder o `Invoke-WebRequest` desde el Mac).
2. `Stop-Service StagerRuntime` (el exe CURRENT está locked si el servicio corre).
3. `Copy-Item` el exe a `C:\ProgramData\Stager\releases\f33-lifecycle\bin\sqx-mt5-worker.exe` y al clone `f33-rollback\bin` si existe.
4. `Start-Service StagerRuntime`. Verificar hash `FC9895B6…` y `Get-Service` Running.
5. Armar DrainWait: `powershell -NoProfile -ExecutionPolicy Bypass -File C:\stager\Invoke-F35F36Evidence.ps1 -Action DrainWait`.
6. Cuando imprima `WAITING_FOR_METAEDITOR`, disparar el compile desde Symphony (`scratch/f36_occupied_start.go`, Temporal `192.168.31.46:7233`, ns `sqx-prop`, queue `sqx-mt5-queue`).
7. Esperar `FOUND … NOW` y `Service now=Stopped`. No cortar `Stop-Service`.
8. Restaurar: `Start-Service StagerRuntime`.

## Validación

- History del child: `ActivityTaskStarted` en la ventana DrainWait, luego `ActivityTaskCompleted` (no `ActivityTaskCanceled`).
- Poller `N@mt4-test@` en `sqx-mt5-queue` tras el Start final.

## Rollback / recuperación

- Si el overwrite falla por lock: repetir paso 2.
- Dual poller stale: un solo child bajo `stager-runtime`; no arrancar worker legacy `C:\SQX`.

## Evidencia

- [[2026-08-13-2300-stager-g3-occupieddrain-close-summary]] — OccupiedDrain PASS `f36-occ-4d05494c`.
