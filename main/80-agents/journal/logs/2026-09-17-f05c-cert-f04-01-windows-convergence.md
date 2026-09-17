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

# 2026-09-17-f05c-cert-f04-01-windows-convergence

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `10-projects/Echo/agentes/Echo + Echo Forge — Deferred Certification Backlog.md` (delta fechado `2026-09-17 — Convergencia Windows owner CERT-F04-01 (veredicto BLOCKED; identidad PID 1700 indeterminable por canal; receta owner refinada con descubrimiento stager)` + `updated` del frontmatter; sin cambio de clases A/B/C y sin cambio de estados de gates físicos)
  - `80-agents/journal/agent-runs/2026-09-17-zcode-glm-5.3-flash-f05c-cert-f04-01-windows-convergence.md` (creado)

## Motivo

- Misión NORMAL F05C-F04-01-WINDOWS-CONVERGENCE del manager con autoridad owner explícita: cerrar únicamente la convergencia del worker Windows para CERT-F04-01 contra el artefacto publicado `worker/sqx/0.2.98/windows-amd64/sqx-mt5-worker.exe` (SHA256 `0bceda4badd982b25b01f13ec40a23eb95c8179e28d8a6d955036b30fc7aa474`): (1) identificar con autoridad suficiente el ejecutable real del PID 1700 y obtener su SHA256, (2) si coincide demostrar versión/proceso/poller sin reinstalar, (3) si no coincide ejecutar convergencia canónica con la autorización owner de stop+install, (4) proofs post-instalación, (5) sin campañas, sin source, sin releases, sin gates CERT.

## Fuentes usadas

- Worktree de certificación `symphony-f04-cert-20260913` @ `b57bfb2`: `deploy/0.2.98/windows-amd64/sqx-mt5-worker.exe` (SHA256 y tamaño verificados localmente contra el digest publicado).
- Repo `xKoRx/symphony` @ `3d0e8c9`: `deploy/windows/sqx-mt5-worker/` (Install/Start/Rollback + README), `docs/services/sqx-mt5-worker-windows.md` (modelo owner-operated foreground, ETCD keys F0, poller `sqx-mt5-queue`), `docs/deployment/stager-publisher-integration.md` (stager como consumidor de releases con plataforma `windows-amd64`), `sqx/cmd/sqx-mt5-worker/main.go` (`os.Getenv("ENV")`).
- SSH `aranea-ssh`: `mt5-kronos` viewer (identity) + `mt5-kronos-operator` (sólo lecturas y un probe de directorio revertido): `whoami /groups`, `Get-Process`, `tasklist /v`, `.Modules`, `netstat -ano`, `sc.exe queryex`, registro `HKLM\SYSTEM\CurrentControlSet\Services`, `Get-Content/Get-ChildItem` sobre `C:\stager`, `C:\ProgramData\Stager`, `C:\Windows\Prefetch`, `C:\MT5\test\EchoForgeJobs`, eventos SCM, `Get-ScheduledTask`, `New-Item/Remove-Item C:\SQX`.
- [[Echo + Echo Forge — Deferred Certification Backlog]] (delta preexec lock 2026-09-17: receta owner, precondición B FAIL), [[Echo Forge — F-04 Magic allocation, version seal and handoff]] (modelo físico), [[aranea-mcps-expert]] + [[aranea-ssh-mcp]] (autoridades mínimas por target).

## Resolución aplicada

- Delta en el backlog que registra el veredicto **WINDOWS CONVERGENCE BLOCKED**: (1) paso 0 identity read-back INDETERMINABLE — `echo-dev` sin membresía `BUILTIN\Administrators` (S-1-5-32-544 ausente; Mandatory Level Medium), `Get-Process -Id 1700` sin Path/StartTime, `tasklist /v` Access denied, `.Modules` RuntimeException (sin `PROCESS_QUERY` ⇒ sin `PROCESS_TERMINATE`), `sc.exe queryex` OpenSCManager FAILED 5, `Get-ScheduledTask` CIM Access denied, Prefetch UnauthorizedAccessException, `C:\ProgramData\Stager` ACL-bloqueado — SHA256 del ejecutable real no obtenible ⇒ comparación con `0bceda4b…` imposible; (2) descubrimiento: el worker Windows es stager-managed — servicio `StagerRuntime` (AUTO, OWN_PROCESS, ImagePath `C:\ProgramData\Stager\bin\stager-runtime.exe service --target-config C:\ProgramData\Stager\target.yaml` legible por registro) + tarea `StagerReconcile` cada 1 min como SYSTEM RunLevel Highest + `icacls /inheritance:r` Administrators+SYSTEM only (ACL-block by design); tensión de modelo con el contrato canónico C:\SQX owner-operated foreground; (3) idle/drain PASS (jobs root sin actividad desde 2026-09-05 21:18; netstat PID 1700 sólo Temporal 7233 + OTel 14317); (4) backup y scripts canónicos verificados en source; artefacto staging byte-exacto verificado local; (5) instalación factible (probe `C:\SQX` creado y eliminado, footprint cero; `sftp-upload` certificado) pero el stop del incumbent cross-identity y del par servicio/tarea stager es imposible por canal ⇒ se rechazó arrancar un segundo poller con PID 1700 vivo; (6) acción exacta pendiente owner refinada: paso 0 elevado, decisión de modelo (stager aceptado ⇒ converged sin instalar si hash coincide; C:\SQX ⇒ Disable-ScheduledTask StagerReconcile + stop/disable StagerRuntime + convergencia canónica).

## Validación

- Artefacto local verificado byte-exacto: `sha256sum` del exe del worktree cert == `0bceda4b…` y size 37250048 == manifest == read-back MinIO EXACT_MATCH del preexec lock.
- Windows: todas las operaciones fueron lecturas; la única mutación fue el probe `New-Item C:\SQX` creado y eliminado en la misma sesión (`SQX_PROBE_REMOVED=True`, footprint cero); cero stop/start de procesos o servicios, cero instalación, cero writes de archivos.
- Boundary negativo documentado por evidencia (no asumido): cada canal denegado quedó registrado con su error exacto; ningún bypass de ACL/policy intentado.
- Ningún estado de gate cambiado; sin SQX/MT5/Temporal/DB/MinIO writes; sin secretos leídos ni registrados; repos sin cambios.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Revertir el delta fechado en el backlog y borrar este log + el agent-run; ningún otro artefacto tocado (el probe C:\SQX ya fue eliminado).
