---
type: change_log
schema_version: 1
scope: session
created: "2026-08-13"
updated: "2026-08-13"
area: "[[Echo Forge]]"
project: "[[Stager - Cross-Platform Deployment Lifecycle]]"
application: "[[stager-app]]"
entities:
  - "[[Stager - Cross-Platform Deployment Lifecycle]]"
related:
  - "[[2026-08-13-stager-f3r-linux-runtime-deployed]]"
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

# F3.R — Runtime Stager desplegado en Windows

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `C:\ProgramData\Stager\bin\{stager.exe,stager-runtime.exe}`
  - `C:\ProgramData\Stager\target.yaml`
  - `stager/specs/STAGER-DEPLOYMENT-LIFECYCLE/VERIFICATION.md`
  - `10-projects/Echo Forge/agentes/Stager - Cross-Platform Deployment Lifecycle.md`

## Motivo

- Completar la instalación owner-operated de F3.R para que una parada SCM mantenga el drain cooperativo sin deadline.

## Fuentes usadas

- Salida de PowerShell del owner del 2026-08-13, tras ejecutar el instalador elevado con `ExecutionPolicy Bypass` limitado a `Scope Process`.

## Resolución aplicada

- El servicio `StagerRuntime` quedó `Running`, Automatic y ejecutado como `LocalSystem`.
- La ruta de servicio apunta a `C:\ProgramData\Stager\bin\stager-runtime.exe service --target-config C:\ProgramData\Stager\target.yaml`.
- La configuración efectiva declara `shutdown_timeout: infinite`.

## Validación

- PASS: consulta SCM y lectura directa de configuración de Windows aportadas por el owner.
- Pendiente fuera de este hito: canary Symphony real tras preflight Temporal; no se tocó un release productivo.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Restaurar los binarios/servicio anteriores y el backup de `target.yaml` recupera el estado previo; no se modificaron releases ni receipts.
