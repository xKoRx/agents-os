---
type: known_error
schema_version: 1
scope: application
created: 2026-07-29
updated: 2026-08-11
area: "[[Echo]]"
project: "[[Echo Forge]]"
application: "[[sqx-watcher]]"
entities:
  - "[[sqx-watcher]]"
  - "[[Hera]]"
  - "[[Kronos]]"
  - "[[deployer-screen]]"
related:
  - "[[Zeus]]"
  - "[[Echo Forge - Cierre de Etapa 4]]"
  - "[[echo-forge-workers-shared-access]]"
aliases:
  - watcher-hera-kronos-missing
  - watcher-unit-not-installed
confidence: verified
source_session: 2026-07-29-temporal-flow-44-evidence-pack
load_policy: when_error_matches
indexable: true
index_priority: high
tags:
  - kind/known-error
  - tech/sqx-watcher
  - tech/deployer
  - tech/multi-node
  - scope/application
---

# `sqx-watcher` ausente en Hera y Kronos (gap de despliegue multi-nodo)

## Síntoma

- `/opt/symphony/current/bin/` en Hera (`.111`) y Kronos (`.121`) **no contiene el binario `sqx-watcher`** ni el shell runner `start-symphony-worker.sh` (este último sí está, pero el binario no).
- `systemctl status symphony-watcher.service` retorna `Unit symphony-watcher.service could not be found.` en ambos.
- `/var/lib/symphony/input/` en Hera/Kronos está completamente vacío (solo `.` y `..`).
- Solo Zeus (`.101`) corre el watcher: `active (running) since Wed 2026-07-29 20:53:09`, md5 `ff4293e58a0cbf0aa146b7faa9e33330`.

## Causa

- El binario **sí se sube a MinIO** en `worker/sqx/0.2.6/linux-amd64/sqx-watcher` (etag `7bffa2ca3c69813dff1e298698701ae3-2`, 29 372 600 B), idéntico para 0.2.2 a 0.2.6.
- El stager de Hera/Kronos dice `ya en versión 0.2.6; nada que hacer` en loop, **no error**.
- Pero el filesystem no contiene `sqx-watcher` y el unit systemd no existe.
- Hipótesis: el stager filtra binarios por nombre/patrón y omite `sqx-watcher`, o falla silenciosamente al materializarlo y reporta éxito igual.

## Impacto

- Cualquier flujo despachado contra Hera/Kronos por Temporal **no es consumido por el watcher local** porque no existe.
- En este flujo (flow_44) no impactó porque el watcher de Zeus lo recogió, pero si Zeus cae, el cluster pierde la capacidad de inyectar flujos.
- Asimetría de diseño vs realidad: el informe de cierre decía "Solo Zeus corre sqx-watcher; Hera/Kronos solo son workers para Temporal (correcto por diseño)". Eso es FALSO: son workers equivalentes y los 3 deberían correr el watcher para que `input/` reciba flujos en cualquiera de los 3 nodos.

## Mitigación

- `scp` desde Zeus: `scp /opt/symphony/current/bin/sqx-watcher kor@192.168.31.111:/tmp/ && ssh kor@192.168.31.111 'sudo install -m 0755 /tmp/sqx-watcher /opt/symphony/current/bin/sqx-watcher'`.
- Copiar unit: `scp /etc/systemd/system/symphony-watcher.service kor@192.168.31.111:/tmp/`.
- Activar: `ssh kor@192.168.31.111 'sudo systemctl daemon-reload && sudo systemctl enable --now symphony-watcher.service'`.

## Fix pendiente (no diagnosticado, requiere análisis del stager)

1. ¿Por qué el stager de Hera/Kronos no materializa `sqx-watcher` aunque el manifest sí lo referencia?
2. ¿Por qué el unit `symphony-watcher.service` no se crea/instala en Hera/Kronos?
3. ¿La decisión arquitectónica "Zeus es el watcher, Hera/Kronos solo Temporal workers" fue intencional y está mal documentada, o es un bug de despliegue que arrastramos?

## Evidencia reproducible

- `for WORKER in zeus hera kronos; do echo "=== $WORKER ==="; echo-forge-worker ssh "$WORKER" 'ls -la /opt/symphony/current/bin/; systemctl status symphony-watcher.service --no-pager -l | head -5; ls /var/lib/symphony/input/'; done`
- Manifest vigente: `deploy/manifest.json` → `artifacts.linux-amd64.watcher` = `deploy/worker/sqx/0.2.6/linux-amd64/sqx-watcher`.
- Deployer log: `grep "0.2.6/linux-amd64/sqx-watcher" deployer_screen.log` confirma subida a MinIO.
