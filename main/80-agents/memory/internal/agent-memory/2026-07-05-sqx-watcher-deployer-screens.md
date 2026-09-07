---
type: agent_memory
scope: internal
created: 2026-07-05
updated: 2026-07-05
tags:
  - kind/agent_memory
  - tech/screen
  - app/symphony
  - topic/operations
---

# Continuidad Operativa: Activación de Watcher y Deployer en screen

## Qué se hizo
- Levantamos los servicios de monitoreo y sincronización local en el servidor utilizando `screen`:
  1. **SQX Watcher**: Corriendo en la sesión de screen `watcher` con el comando `./run_watcher.sh ./input`.
  2. **Deployer Watcher**: Corriendo en la sesión de screen `deployer` con el comando `./run_deployer.sh ./deploy deploy`.
- Ambos servicios se encuentran ejecutándose en segundo plano (`Detached`) y compilando/corriendo sus respectivos binarios de Go.
