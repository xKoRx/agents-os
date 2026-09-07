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
  - "[[Stager]]"
related:
  - "[[Echo Forge]]"
aliases:
  - CURRENT CRLF Windows Stager
  - Set-Content CURRENT unsafe
  - target.yaml 640 User=kor
confidence: verified
source_session: a896f77f-7e50-4c60-b186-a027e8f81792
load_policy: when_error_matches
indexable: true
index_priority: high
tags:
  - kind/known-error
  - scope/application
  - area/echo
  - app/stager
  - project/stager-cross-platform-deployment-lifecycle
---

# stager-windows-powershell-crlf-current

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Síntoma

- `Restart-Service StagerRuntime` falla o el runtime declara CURRENT unsafe / no selecciona `f33-lifecycle`.
- Hex de `state\CURRENT` termina en `0D 0A` (CRLF) o incluye BOM; Stager exige exactamente un LF.
- En Linux, `stager-runtime` con `User=kor` loguea `permission denied` al leer `target.yaml` si el archivo es `640 root:stager`.

## Causa

- PowerShell 5.1 `Set-Content` escribe `f33-lifecycle\r\n`. El parser de CURRENT no acepta `\r`.
- Drop-in Linux `User=kor` no puede leer `target.yaml` `0640 root:stager`; el keep canary era `0644`.

## Impacto

- Cutover Windows queda en fake `f28-canary` o servicio que no arranca; F3.5 se finge PASS con worker falso.
- Cutover Linux con drop-in Symphony no carga target y el child no pollea.

## Detección

- Windows: `(Format-Hex 'C:\ProgramData\Stager\state\CURRENT')` debe terminar `0A` sin `0D`.
- Linux: `stat -c '%a %U:%G' /opt/stager/target.yaml` debe ser `644`; `journalctl -u stager-runtime` busca `permission denied`.

## Mitigación

- Escribir CURRENT con `[IO.File]::WriteAllText($path, "f33-lifecycle`n", (New-Object System.Text.UTF8Encoding $false))`. No usar `Set-Content`.
- En Linux restaurar `chmod 644` en `target.yaml` cuando el runtime corre como `kor`.
- Esto no es BLOQ: se repara en el host y se continúa el cutover.

## Evidencia

- [[2026-08-13-stager-f3-g3-cutover-handoff]] — F3.3 Zeus `640` y F3.5 Windows CRLF observados en la misma línea de cutover.
