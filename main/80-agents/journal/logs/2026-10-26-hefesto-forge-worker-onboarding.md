---
type: change_log
schema_version: 1
scope: session
created: "2026-10-26"
updated: "2026-10-26"
area: "[[Echo]]"
project: "[[Echo Forge — Operación Real V2]]"
application:
entities: []
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

# 2026-10-26-hefesto-forge-worker-onboarding

## Cambio

- **Tipo:** updated.
- **Archivos:** `80-agents/tools/echo-forge-worker-access/echo-forge-worker` (wrapper) y commit `34c13a5` del repo Symphony (AGENTS.md + skills `worker-ssh` y `worker-troubleshooting`): Hefesto agregado a los inventarios de workers.

## Motivo

El owner pidió activar Hefesto como un worker más de Forge, alineado en esta
máquina y corriendo como en Kronos, Zeus y Hera. Además del registro en los
inventarios, el trabajo principal fue físico sobre la máquina:

- Stack desplegado en Hefesto (Ubuntu 26.04, 192.168.31.164, hostname
  `sqx-ulab-hefesto-0`): usuarios de sistema `stager`/`symphony`, `/opt/stager`
  (root del stager Go), `/usr/local/lib/stager/{stager,stager-runtime}`
  (byte-idénticos a Zeus), `/etc/stager/{target.yaml,stager.env}`,
  `stager.timer` + `stager.service` + `stager-runtime.service` con drop-in
  `symphony-canary.conf`, árbol legacy `/opt/symphony` (release 0.2.40 para
  compat CURRENT/PENDING), `/var/lib/symphony` y `/var/log/symphony` con
  logrotate, regla polkit acotada (`49-stager-runtime.rules`) para que el
  usuario `stager` reinicie sólo `stager-runtime.service`.
- SQX copiado desde Zeus por rsync y verificado por lista de archivos con
  locale C (única diferencia deliberada: `user/log/`): versiones `142` (2.0G) y
  `144` (9.1G, la activa según etcd `sqx/sqx_version`), `j64` (Zulu 21 embebido,
  no se necesita Java de sistema), `user/` con proyectos `custom` y EchoForge*,
  plugin `EchoForgeAutomator.jar` en `user/libs`, y symlinks raíz (`sqcli`,
  `StrategyQuantX_nocheck`, etc.).
- Entorno: `/etc/environment` con `ENV=production` y `HOST_KEY=f0` (z0/h0/k0
  tomados por zeus/hera/kronos).
- Desviación deliberada: heap JVM `-Xms1g -Xmx5g` (máquina de 13 GB) vs
  `-Xms34g -Xmx55g` de la flota grande; documentada en AGENTS.md del repo.
- Verificación física: stager stageó 0.3.2 desde MinIO (SHA del binario
  `6abfb00b…` idéntico a Zeus y al commit del manifest), worker registrado
  (`SQX Worker registrado`, `Started Worker Namespace sqx-prop TaskQueue
  sqx-main-queue WorkerID 72880@sqx-ulab-hefesto-0@`), conexión gRPC ESTAB
  hacia Temporal `192.168.31.46:7233`, watch de etcd activo sobre
  `maintenance/control`, `sqcli` 144 ejecutable con el JRE embebido.

## Actualización (mismo día, pedido del owner: modo intermitente + heap 13 GB)

- Heap del drop-in reajustado a `-Xms2g -Xmx9g` (13 GB RAM + 12 GB swap; el
  env hereda al JVM de `sqcli` de cada corrida del worker). Aplicado y
  verificado en `/proc/<pid>/environ` del worker 75421.
- Modo intermitente: `forge-worker-guard.timer` (tick 60s, unit
  `forge-worker-guard.service`) apaga el worker con drain graceful
  ("stop-after-current": la activity en vuelo termina, verified contra el
  código — `FileQuiesceWatcher` trata SIGTERM/PENDING como drain request)
  cuando detecta backtester Clutifx (`echo-backtest-clf*` por argv,
  `run_g2_wave.py`/`research_lab.py` por cmdline) o `MemAvailable<3G`; lo
  reenciende con ≥5G libres. Control manual: `forge-worker-ctl
  {status|on|off|auto}` (hold manual en
  `/var/lib/symphony/forge-worker-manual-off`). Instalado en
  `/usr/local/sbin/forge-worker-guard` + `/usr/local/bin/forge-worker-ctl`.
- Test cerrado con evidencia en journal (`journalctl -t forge-worker-guard`):
  stop por backtester 21:28:41, re-arranque 21:29:42, poller ESTAB a Temporal.
  Lección de test: `pgrep -f` genérico produce falsos positivos con cmdlines
  que mencionan el nombre (incluidos wrappers de agentes); por eso el patrón
  es `echo-backtest-clf` y no `echo-backtest`.
- Registro del worker: NO hay registry estático en la flota — Temporal
  (pollers dinámicos `pid@sqx-ulab-hefesto-0@`), Prometheus
  (`symphony_sqx_activity_result_total{host_key}`) y etcd
  (`maintenance/state/<host_key>` escrito por ops) son los canales; hefesto
  aparece/desaparece como poller 4 según el guard. Docs del repo actualizadas
  (commit `24975fb`): AGENTS.md, `worker-ssh` y preflight de
  `forge-wave-dispatch` (no contar hefesto en el 3/3 ni subir K por él).

## Fuentes usadas

Inventario físico de Zeus/Hera/Kronos por SSH, etcd de producción
(`/sqx-worker/production/*`, `/symphony/production/*`), repo Symphony local y
log del worker en Hefesto.
