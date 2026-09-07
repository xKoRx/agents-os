---
type: known_error
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
  - "[[stager-mt5-heartbeat-late-started]]"
  - "[[stager-windows-mt5-cutover-and-occupieddrain]]"
aliases:
  - DrainWait delay 1.5s
  - OccupiedDrain Stop tarde
confidence: verified
source_session: b0ed3608-24c7-460f-85e5-9415cc34d06a
load_policy: when_error_matches
indexable: true
index_priority: high
tags:
  - kind/known-error
  - scope/application
  - area/echo
  - app/stager
  - os/windows
---

# stager-windows-occupieddrain-delay-misses-started

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Síntoma

- DrainWait imprime `FOUND MetaEditor64` y `Service now=Stopped`, pero Temporal ya tiene `ActivityTaskCompleted` antes del `Stop-Service`.

## Causa

- Compile dura ~1s. Un `Start-Sleep` 1.5s después de FOUND deja el Stop fuera de la ventana Started.
- PowerShell 5.1 no admite em-dash en scripts (`â€"` rompe `Invoke-F35F36Evidence.ps1`).

## Impacto

- OccupiedDrain operativo sin overlap contractual. G3 no cierra.

## Detección

- El script debe decir `Stop-Service StagerRuntime NOW`, no `delay 1.5s`.
- `Select-String -Path C:\stager\Invoke-F35F36Evidence.ps1 -Pattern "NOW","delay 1.5s"`.

## Mitigación

- `Stop-Service StagerRuntime` inmediato al FOUND. OccupiedDrain = `Stop-Service`, nunca Task Manager / `Stop-Process`.
- Armar DrainWait **antes** de disparar el compile. Copiar el `.ps1` a `C:\stager\` (no existe `C:\staging\`). Overwrite del exe requiere `Stop-Service` primero (file lock).
- Scripts Windows: ASCII only.

## Evidencia

- [[2026-08-13-2300-stager-g3-occupieddrain-close-summary]] — PASS con Stop NOW, `pid=5612`, parent `f36-occ-4d05494c`.
