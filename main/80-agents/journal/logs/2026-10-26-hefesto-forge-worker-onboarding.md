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

## Fuentes usadas

Inventario físico de Zeus/Hera/Kronos por SSH, etcd de producción
(`/sqx-worker/production/*`, `/symphony/production/*`), repo Symphony local y
log del worker en Hefesto.
