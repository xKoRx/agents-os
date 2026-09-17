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

# 2026-09-17-f05c-cert-f04-01-access-recovery

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `10-projects/Echo/agentes/Echo + Echo Forge — Deferred Certification Backlog.md` (delta fechado `2026-09-17 — Desbloqueo Windows access owner CERT-F04-01 (capability parcialmente restaurada; inspector elevado stageado; convergencia UNKNOWN owner-gated)` + `updated` del frontmatter; sin cambio de clases A/B/C ni de estados de gates físicos)
  - `80-agents/journal/agent-runs/2026-09-17-hermes-ariadna-f05c-cert-f04-01-access-recovery.md` (creado)

## Motivo

- Misión del responsable del Aranea MCP Access Plane: restaurar la capability mínima para identificar y converger el worker Windows de Echo Forge en `worker-kronos` contra `worker/sqx/0.2.98/windows-amd64/sqx-mt5-worker.exe` (SHA256 `0bceda4badd982b25b01f13ec40a23eb95c8179e28d8a6d955036b30fc7aa474`), demostrando la topología real Stager/Reconcile → proceso → ejecutable → hash → release con canal privilegiado autorizado, exclusivamente read-only. NO ejecutar CERT-F04-01; no deshabilitar StagerReconcile; no detener StagerRuntime; no iniciar segundo worker; no modificar ETCD; no ejecutar campañas.

## Fuentes usadas

- Vault: backlog (deltas preexec-lock/readiness-R1/windows-convergence 2026-09-17), runbook `aranea-ssh-mcp.md`, `stager-app.md`, runbook `stager-windows-mt5-cutover-and-occupieddrain.md`, skill `aranea-mcps-expert`, handoff anterior (`2026-09-17-f05c-cert-f04-01-windows-convergence`).
- Plane: `aranea-ssh` (`mcps.lab.aranea.cl:3000`, ssh-mcp 2.8.0) con perfiles `mt5-kronos` (viewer) y `mt5-kronos-operator` (operator), identidad remota `worker-kronos\echo-dev`; consumer-side vía SDK MCP certificado (sesión única por probe, bearer por stdin, jamás impreso).
- Estado del plane por management path nativo `~/aranea/bin/mcps-ops` (sólo lecturas + un `docker restart ssh-mcp` operacional).

## Resolución aplicada

- **Topología demostrada en vivo (read-only):** worker `sqx-mt5-worker` sigue siendo **PID 1700** con poller vivo (`netstat :7233` ESTABLISHED 1700→Temporal `192.168.31.46`) + OTel `192.168.31.60:14317`; supervisor `stager-runtime` PID 30700; servicio `StagerRuntime` START=2 AUTO, ImagePath `C:\ProgramData\Stager\bin\stager-runtime.exe service --target-config C:\ProgramData\Stager\target.yaml`, **ObjectName `.\kor`** (corrección material: el servicio NO corre como SYSTEM); `StagerReconcile` NO aparece en `schtasks /Query` completo (API legada, exit 0) y CIM la deniega a esta identidad ⇒ presencia de la tarea no demostrable por canal certificado (el dato "cada 1 min SYSTEM" del handoff previo proviene del instalador, no de observación de la tarea viva).
- **Boundary ratificado (fail-closed, sin bypass):** `tasklist /FI` Access denied; `sc.exe query` OpenSCManager FAILED 5; `Get-ScheduledTask` CIM Access denied; `C:\ProgramData\Stager` (dir, `CURRENT`, `PENDING`, `releases\`) denegados por ACL (`icacls /inheritance:r`, grant sólo Administrators+SYSTEM según `C:\stager\install-stager.ps1`); TaskCache denegado. Gotcha documentado: `Get-ChildItem C:\stager` oculta por atributo Hidden archivos legibles por path directo (instalador y `stager-target.yaml.example` leídos OK). `C:\SQX` no existe; `C:\stager_old` existe; jobs root sin actividad desde 2026-09-05 21:18 (drain PASS re-confirmado).
- **Resolución de acceso (§3): A (viewer) y B (operator) insuficientes para el paso 0; C implementado como INSPECTOR stageado, no como perfil nuevo.** Cero cambios de configuración del plane (sin perfiles, keys ni permisos nuevos; sin ampliación de `echo-dev`). Recovery operacional: `docker restart ssh-mcp` por pool de 64 sesiones agotado (503 `Server is at its session limit` con `/status` healthy y `connections:[]`; diagnóstico exigido previo). Inspector `stager-identity-inspect.ps1` (write-surface SOLO stdout; líneas sensibles de target.yaml redactadas; re-ejecutable) stageado a `C:\Windows\Temp\stager-identity-inspect.ps1` vía `sftp-upload` certificado, sha256 verificado byte-exacto local/remote `4f6712bc159ea15545f6f90996f57794cf0a30db317d177f355464ed7f9f2818` (3373 B).
- **Certificación de capability (§4): PASS acotado.** Prueba consumer-side real (SDK+plane): PID 1700, poller ESTABLISHED, ImagePath y ObjectName leídos en vivo; negativo H2 viewer (`run-command` → POLICY_DENIED) vigente; boundaries no-admin documentados con error exacto. El SHA256 del ejecutable en ejecución queda INDETERMINADO: único gap, blocker = elevación (identidad Windows, no del plane).
- **Decisión de convergencia (§5): UNKNOWN — owner-gated.** OWNER ACTION BUNDLE en `~/aranea/work/f04-window/` (`owner-action-bundle.md` + `stager-identity-inspect.ps1`): paso 1 = inspector elevado (única acción requerida para cerrar hash/padre/CURRENT/releases/StagerReconcile); paso 2 = decisión de modelo: (A) stager aceptado ⇒ hash coincidente ⇒ WINDOWS CONVERGED sin instalar, hash distinto ⇒ convergencia por stager (target/manifest 0.2.98 ya publicado en MinIO `deploy`); (B) modelo canónico `C:\SQX` ⇒ disable `StagerReconcile` (si existe), `sc.exe stop/config` StagerRuntime (como `.\kor` el stop/disable no requiere su contraseña), install versionado 0.2.98 con scripts canónicos + `ENV` owner, proofs y rollback canónico.

## Validación

- Todas las operaciones sobre `worker-kronos` fueron lecturas más un upload verificado del inspector en `C:\Windows\Temp` (KEEP hasta ejecución owner; rollback = `del`). Cero stops/starts de procesos o servicios; cero instalación; cero writes fuera del inspector; cero cambios en repos, ETCD, DBs o MinIO.
- Integridad del canal: hash sha256 local == remote del inspector; bearer sólo por stdin; ningún valor de secreto impreso o registrado.
- El veredicto de convergencia NO se declaró por correlación (target.yaml/manifest no prueban el binario en ejecución); cada canal denegado quedó registrado con su error exacto.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, sin secretos, sin paths con credenciales

## Rollback

- Revertir el delta fechado en el backlog y borrar este log + el agent-run. En `worker-kronos`: `del C:\Windows\Temp\stager-identity-inspect.ps1`. En el plane: ninguno (sin cambios de configuración; el restart de ssh-mcp es estado operacional, no configuración).
