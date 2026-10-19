# ZEUS-WRITER-FORENSICS — Snippet Integrity P0 (2026-10-19)

## Respuesta a la pregunta central

**¿QUÉ PROCESO ESCRIBIÓ O RESTAURÓ EL SNIPPET ANTIGUO?** — **Ninguno. No hubo escritura ni restauración del contenido antiguo durante el incidente.** El archivo antiguo (`03106b81…`, mtime 2026-09-06 10:13:10) permaneció en disco ininterrumpidamente desde su instalación inicial. Lo que falló fue la escritura del contenido nuevo: `deploy-plugin-s02.sh` reportó un swap que no ocurrió.

## Descarte de candidatos (con evidencia)

| Candidato | Veredicto | Evidencia |
|---|---|---|
| Recompilación SQX escribe el fuente | DESCARTADO — sqcli recompila fuente→bytecode, jamás reescribe el `.java`; no existe ruta Go/worker que escriba snippets (grep del repo symphony: el worker sólo escribe XMLs de proyecto y `exporter.properties`) | código `sqx/activities/worker/steps/steps.go`, `sqx/core/runtime/config.go` |
| Watcher inotify/fanotify restaurador | DESCARTADO — escaneo root de `/proc/*/fdinfo` en Zeus: únicamente systemd (1, --user), dbus, logind, agetty, timesyncd, udevd, resolved, multipathd, udisksd, polkitd | escaneo 2026-10-19 ~22:1xZ |
| `stager.timer` (dispara cada 30 s) | DESCARTADO — unidad `User=stager`, `NoNewPrivileges=true`, `ProtectSystem=full`; sólo reconcilia `/opt/symphony`; logs de stager sin actividad oct-19 | `systemctl cat stager.service`, `/var/log/symphony/stager.log` |
| Cron/timers de root | DESCARTADO — sólo `sysstat` (sa1, minutos 5-55/10 = las sesiones CRON del journal) + `cron.hourly` estándar; nada toca `/home/kor/sqx` | `/etc/crontab`, `/etc/cron.d/{e2scrub_all,sysstat}`, `systemctl list-timers` |
| sqx-instrument-sync | DESCARTADO — alcance exclusivo `~/sqx/user/data` (sync Zeus→Hera/Kronos, jamás snippets; jamás dirección inversa) | skill `sqx-instrument-sync` v3.0.0 |
| Deployer/watcher de Symphony | DESCARTADO — no tocan `user/extend`; el worker en Zeus corre 0.3.2 desde 16:53Z sin escribir en el arbol SQX | `ps aux`, código worker |
| Proceso externo sub-segundo (ventana mv→sello = ~14 ms) | DESCARTADO — la ventana no existía: la línea 95 nunca creó ni renombró nada (EACCES); la secuencia 18:03:34.425 (jar) → 34.429 (Snippets.jar) → 34.431 (EACCES) → 34.439 (sello) es la ejecución normal del script con el swap fallido | ctimes de dirs + sellos |
| Sobreescritura desde backup/142 | DESCARTADO como evento — son copias estáticas (identidad de bytes `03106b81` y mtime sep-6 coinciden con el estado pre-deploy); nadie las copió de vuelta: el mtime del live nunca cambió hasta 18:22:43Z | `stat` del live: mtime==ctime==18:22:43Z (primera y única escritura del día) |

## Quién escribió qué, realmente

- **18:03:31–34Z** — `kor` (SSH exec, sin pty → sin registro wtmp/journal), ejecutando `deploy-plugin-s02.sh`: escribió JARs (`user/libs`, `internal/libs`), NO escribió el snippet (fallo EACCES en `cp … && mv …` bajo `set -e`), y escribió sellos/rollback que reportaban éxito.
- **18:22:43Z** — identidad `echo-dev` (canal MCP operator; la instalación como dueño no requiere sudo: `chown` a uid propio es no-op permitido): primera y única escritura real del snippet ese día (`install`/`cp` con `-o echo-dev -g echo-dev -m 664`), estable desde entonces.

## La ilusión de la "restauración"

La narrativa "reapareció con contenido y mtime del 14 de octubre" se explica como lectura post-hoc del archivo viejo que nunca se fue: contenido antiguo sí (la versión sep-6 = la vigente hasta el 18-oct), mto antiguo sí (sep-6, no 14-oct — no existe ninguna copia con mtime 14-oct en el host; verificado con `find` de nombre `EchoForgeOverviewExporter*` sobre `/home /opt /srv /var/tmp /tmp`). El sorpreso del operador provino del sello engañoso (línea 1 = src nuevo) y del mensaje `swap aplicado… DEPLOY OK`.

## Lección de forense

El "escritor" de un incidente de integridad puede ser el propio procedimiento de despliegue cuando sus verificaciones son ilusorias. La regla operacional resultante: **ningún paso de deploy que reporte éxito sin verificación de la superficie live** (implementado en `deploy-plugin.sh` @ `fix/snippet-integrity-p0`).
