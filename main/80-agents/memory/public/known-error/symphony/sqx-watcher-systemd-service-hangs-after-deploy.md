---
type: known_error
scope: application
created: "2026-07-27"
updated: "2026-07-27"
area: "[[Echo Forge]]"
project: "[[Echo Forge - Cierre de Etapa 4]]"
application: "[[sqx-watcher]]"
entities:
  - "[[StrategyQuant X]]"
  - "[[Symphony]]"
  - "[[Zeus]]"
related:
  - "[[sqx-deployer]]"
  - "[[deployer-watcher]]"
aliases:
  - symphony-watcher.service colgado
  - sqx-watcher no procesa config.json
  - watcher systemd active pero idle
confidence: high
source_session: "2026-07-27-echo-forge-trade-list-exporter"
load_policy: when_error_matches
indexable: true
index_priority: high
tags:
  - app/sqx-watcher
  - area/echo
  - kind/known-error
  - project/echo-forge
  - scope/application
  - tool/strategyquant
  - tool/systemd
---

# SQX Watcher — systemd service queda colgado (active/idle) tras un deploy

> El servicio `symphony-watcher.service` (Zeus) reporta `active (running)` en
> `systemctl status` pero **no encola nuevos `config.json`** aunque
> `inotify` confirme eventos en el watch dir.

%% Routing: area/project/application/entities/related usan links canónicos. %%

## Síntoma

- `systemctl status symphony-watcher.service` → `active (running)`,
  `Main PID` presente, sin `failed` reciente.
- `journalctl -u symphony-watcher.service -n 100` muestra el último evento
  anterior al deploy y luego silencio absoluto, aunque se copie un nuevo
  `config.json` al watch dir.
- `inotifywait -m /var/lib/symphony/input/` SÍ emite `MODIFY`/`CREATE`
  para el nuevo `config.json`. La pérdida está aguas abajo del kernel:
  el watcher no consumió el evento.
- Reiniciar `systemctl restart symphony-watcher.service` recupera el
  comportamiento sin re-deploy.

## Causa raíz

El binario nuevo del watcher reemplaza el `ExecStart` mientras un proceso
del binario anterior sigue vivo como huérfano (`/proc/<old_pid>` sin padre
vivo o con `PPID=1`). `systemd` ve su unidad principal sana y reporta
`active`, pero el fsnotify listener que debería consumir el directorio
pertenece al proceso anterior, no al nuevo.

En la sesión del 2026-07-27 se observó en Zeus exactamente esto:

- `pgrep -fa sqx-watcher` devolvía **dos** instancias: una con PID de
  systemd (`MAIN PID`) y otra huérfana anterior que aún sostenía el
  inotify watch sobre `/var/lib/symphony/input/`.
- `kill <huérfano>` sin reiniciar el servicio bastó para que el watcher
  "principal" (systemd) tomara el control de inmediato.

## Mitigación operativa (workflow recomendado)

Después de cada deploy nuevo del watcher:

1. Identificar huérfanos:
   `pgrep -fa sqx-watcher` → debe devolver exactamente **una** línea.
   Si hay más de una, alguna es huérfana.
2. `kill <huérfano>` (SIGTERM) y revalidar con `pgrep`.
3. Si tras SIGTERM no hay progreso, escalar a `kill -9` y luego
   `systemctl restart symphony-watcher.service` para garantizar un
   `ExecStart` fresco bajo systemd.
4. Confirmar recuperacion disparando un `config.json` de prueba y
   leyendo `journalctl -u symphony-watcher.service -f`.

## Mitigación duradera (código)

- El binario debería manejar `SIGHUP`/`SIGTERM` con un
  `signal.Notify(... ctx)` y `cancel()` que cierre el listener fsnotify
  antes de salir. Sin eso, cualquier rotación (deploy, restart manual)
  deja un watcher zombi que retiene el FD de inotify.
- El servicio systemd debería tener `Restart=on-failure` + un
  `ExecStopPost` que ejecute `pkill -9 -f sqx-watcher || true` para
  limpiar huérfanos en paradas controladas.

## Por qué no es bug del deployer

El `deployer-watcher` local sube bien los artefactos a MinIO y el
stager remoto los baja y activa el symlink correctamente. El problema
es 100% en el lado del binario/systemd del worker, no en la cadena
de release.
