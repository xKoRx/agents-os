# WINDOWS-HANDOFF-KRONOS — Estado operacional efectivo del worker MT5 (2026-10-15)

> **ACTUALIZACIÓN 2026-10-15 (posterior):** el mecanismo de arranque documentado
> aquí (`C:\Temp\session_worker.ps1`, deudas sin watchdog/update) fue REGULARIZADO
> la misma fecha por el runtime hardening: supervisor versionado
> `deploy/windows/session-worker/` en `C:\ProgramData\Stager\bin\`, tarea
> `\EchoForgeMT5WorkerSession` re-registrada (sin límite 72h), `C:\Temp` eliminado,
> causa de la degradación session 0 resuelta como degradación transitoria
> recurrente (probe SYSTEM PASS) y certificación de ciclo de vida A–E. Estado
> vigente y evidencia: **WINDOWS-RUNTIME-HARDENING-20261015.md** (mismo
> directorio) y `worker-troubleshooting` §10. El estado físico del worker,
> layout, identidades de release y perfiles de acceso de este documento siguen
> vigentes.

**STATUS: OPERATIONAL_DOCUMENTED** — inspección read-only (perfiles `mt5-kronos-admin`, `mt5-kronos-operator`); no se reinició el host, no se alteró el worker, no se ejecutó ninguna hipótesis destructiva. Host: `WORKER-KRONOS` (VM 135, `mt5-kronos.lab.aranea.cl`), ambiente operacional único de Forge (`production`, contrato §0 de [[Echo + Echo Forge — Environment Contract]]).

## Estado efectivo verificado

- **Worker vivo:** `sqx-mt5-worker` PID 35616, `Path = C:\ProgramData\Stager\releases\0.2.141\bin\sqx-mt5-worker.exe`, StartTime 2026-10-14 21:47:42 (local, 1 s tras el Last Run de la tarea), `env=production` en logs. SHA256 del exe en disco `bf247d6167421dc7182dece9633ac15162b27a1f91a2a6e3a9cf86121aaefc96` — idéntico byte a byte al manifest de la release 0.2.141 (`deploy/manifest.json` de `xKoRx/symphony` @ `eab4302`, windows-amd64). El mismo proceso ejecutó el cierre de wave3t: uploads durables 2026-10-15T03:28Z (HTM 2.6 MB del finalista rank 5 `0cb29320`, ini/terminal/tester/agent logs) en `session-worker.out.log`.
- **Tarea `\EchoForgeMT5WorkerSession`:** Enabled, `Logon Mode: Interactive only`, `Run As: KoR`, disparador **At logon**, acción `powershell -NoProfile -ExecutionPolicy Bypass -File C:\Temp\session_worker.ps1`. Last Run 2026-10-14 21:47:41, Last Result **1** (anomalía cosmética: el worker lanzado a las 21:47:42 sigue vivo; el launcher escribe `[start]` con `Add-Content` y `Start-Process -RedirectStandardOutput` trunca el mismo archivo, y `Wait-Process` no retiene el estado Running de la tarea — la supervisión debe keyar por proceso+log, no por Last Result de la tarea).
- **Launcher `C:\Temp\session_worker.ps1`:** lee `C:\ProgramData\Stager\CURRENT` (actualmente `0.2.141`), resuelve `releases\<CURRENT>\bin\sqx-mt5-worker.exe`, setea `ENV=production`, lanza el exe en la sesión interactiva de consola con stdout→`session-worker.out.log` / stderr→`session-worker.err.log` y espera su salida. Comentario en el propio script: MT5 build 6182 no escribe el reporte HTM del tester desde sesión 0 (degradación del host desde 2026-10-14 ~16:42 local); en sesión interactiva el reporte sí se materializa.
- **Sesión de ejecución:** `console` sesión 2, usuario **KoR, Active** (efecto del `tscon 2 /dest:console` del 14-oct vigente). Requisito duro: los terminales MT5 necesitan la sesión interactiva de consola; una sesión RDP o Disc degrada el stack gráfico (`MDI create failed`, reportes HTM no escritos — causa documentada de los `report_not_found` del intento r2).
- **Servicio `StagerRuntime`:** **Stopped + Disabled** (intencional; era el supervisor en sesión 0). `C:\ProgramData\Stager\target.yaml` aún declara `runtime.driver: windows-scm → StagerRuntime` como objetivo nominal — divergencia declarado-vs-efectivo documentada.
- **Tarea `\StagerReconcile`:** Enabled, Run As SYSTEM, repetición cada minuto, Last Run 2026-10-15 10:13:01 con **Last Result 0**. Es el loop activo de staging: materializa `releases\<versión>` (p. ej. `0.2.141` staged 2026-10-14 20:29 con el servicio ya Disabled) y mantiene `CURRENT`.
- **Tarea auxiliar de evidencia:** existe una tarea que ejecuta `C:\ProgramData\Aranea\aranea-stager-evidence.ps1` (recolección de evidencia del stager).
- **Layout:** `C:\ProgramData\Stager\{CURRENT, target.yaml, bin\stager.exe, releases\<ver>\bin\sqx-mt5-worker.exe, session-worker.out.log, session-worker.err.log}`; terminales/slots MT5 en `C:\MT5\slots\slot-N` (smoke r3 usó `slot-2`, leases y workspaces `C:\MT5\slots\slot-2\EchoForgeJobs\<job>`); logs del worker con `env=production`.
- **Acceso:** `echo-dev` NO ve la tarea ni puede consultar SCM/CIM (ACL); la vista operativa requiere el perfil admin (`mt5-kronos-admin`, cuenta `ariadna-win`). El perfil viewer `mt5-kronos` rechaza todo comando.

## Recuperación por escenario (análisis documental — no se ejecutaron reinicios ni se tocó un worker saludable)

- **Crash/salida del worker (hoy):** NO hay auto-restart. La tarea ya se disparó y el wrapper powershell terminó; el worker queda huérfano pero vivo. Procedimiento: verificar sesión KoR Active en consola (`qwinsta` → `console KoR Active`), luego `schtasks /run /tn EchoForgeMT5WorkerSession` (desde contexto de KoR/admin) o rerun del launcher; el worker releerá `CURRENT` vigente. Deuda explícita: sin watchdog.
- **Reinicio del host (deuda principal):** la tarea es `At logon` + `Interactive only` y **NO existe autologon** (`HKLM\...\Winlogon\AutoAdminLogon` y `DefaultUserName` ausentes). Tras un boot, el worker NO vuelve solo: exige que una persona inicie sesión KoR en la **consola** (el disparador At logon dispara `session_worker.ps1`, que lee `CURRENT` y levanta la release vigente). Ejecución desatendida post-reboot NO está garantizada sin rediseño (autologon en consola + tarea con trigger adicional, o restaurar un supervisor en sesión interactiva); se deja como deuda reproducible, no como hipótesis certificada — no se reinició el host para probarla.
- **Desconexión/toma de sesión:** si la sesión 2 de KoR pasa a Disc o es tomada por RDP, los backtests MT5 dejan de escribir HTM (degradación gráfica documentada). Recuperación validada el 14-oct: desde admin, `tscon 2 /dest:console` para re-anclar la sesión a la consola y dejarla Active antes de despachar trabajo MT5.
- **Actualización de release:** `StagerReconcile` (SYSTEM, cada minuto) stagea la nueva release en `releases\<ver>` y actualiza `CURRENT`; el worker sigue en el exe viejo hasta reinicio. Procedimiento vigente (ejercitado 0.2.140→0.2.141): reconciliar `releases\<nueva>`+`CURRENT`, terminar el worker viejo (`taskkill` del PID de `sqx-mt5-worker`; `schtasks /end` no basta porque el wrapper ya salió), y `schtasks /run /tn EchoForgeMT5WorkerSession`. Nota: `echo-dev` no puede; requiere admin y sesión KoR en consola.
- **Límite 72 h de la tarea:** `Stop Task If Runs 72:00:00` puede detener la instancia de la tarea sobre un worker de larga vida; el worker queda huérfano y sin watchdog. Deuda menor documentada.
- **Renicio del host, sesión y release — postcondición compartida:** tras cualquier recuperación, verificación mínima: PID de `sqx-mt5-worker` con `Path` bajo `releases\<CURRENT>`, `env=production` en `session-worker.out.log`, consola `KoR Active`, y un poll de Temporal `sqx-prop`/`sqx-main-queue` observable en el log al primer despacho.

## Identidades de release 0.2.141 (recap)

Source `1a48cb3cbc6f33be0dd6009b300294797064eedc` (`vcs.modified=false`, `vcs.time=2026-10-14T23:24:05Z`, ancestro de `origin/master=eab4302` pusheado el 2026-10-15 09:38); manifest `xKoRx/symphony:deploy/manifest.json` (version `0.2.141`); SHA256: windows `sqx-mt5-worker.exe` `bf247d61…efc96` (idéntico al binario vivo de este host), linux `symphony` `57537674…b1dc`, linux `sqx-watcher` `9e408591…4f93`. Fix habilitante: `5eaeaa2` (serializa actividades MT5, INFRA-1). Publicación: commit `33f1fee` (0.2.140 intermedia `d31a…` reemplazada por 0.2.141 `bf247d61…`), commit final de docs `eab4302`.
