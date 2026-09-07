---
type: agent_memory
scope: internal
created: 2026-07-18
updated: 2026-07-18
tags:
  - kind/agent_memory
  - tech/screen
  - app/symphony
  - topic/operations
---

# Continuidad Operativa: Lanzamiento local de deployer y watcher en screen

## Qué se hizo
- Se reactivó la ejecución local de **Deployer Watcher** y **SQX Watcher** bajo sesiones detached de `screen` forzando de forma explícita el entorno productivo:
  1. **Deployer Watcher**: Iniciado en la sesión de `screen` `deployer` con el comando `ENV=production screen -dmS deployer ./run_deployer.sh ./deploy deploy`.
  2. **SQX Watcher**: Iniciado en la sesión de `screen` `watcher` con el comando `ENV=production screen -dmS watcher ./run_watcher.sh ./input`.
- Se verificó que ambas sesiones quedaron correctamente iniciadas y en estado `Detached` en el host local.

## Notas de Triage y Diagnóstico
- **Procesos Huérfanos**: Al bajar o matar las sesiones de `screen` de manera abrupta, los procesos hijos (`go run ...` y `run_watcher.sh`/`run_deployer.sh`) continuaron ejecutándose como procesos huérfanos en segundo plano en la máquina local. Se debió ejecutar `kill -9` a todos los PIDs huérfanos antes de poder levantar con éxito los servicios de nuevo.
- **Forzado de producción**: Es indispensable forzar `ENV=production` en los comandos de inicio del watcher local para que se conecte al Temporal productivo, de lo contrario heredará el entorno de desarrollo y enviará tareas a colas sin workers activos.

