---
type: agent_memory
scope: internal
created: 2026-07-10
updated: 2026-09-09
index_priority: never
indexable: false
load_policy: manual
memory_state: archived
tags:
  - kind/agent_memory
  - tech/screen
  - app/symphony
  - topic/operations
---

# Continuidad Operativa: Watcher y Deployer reiniciados localmente

## Qué se hizo
- Se reiniciaron las sesiones de `screen` locales para el monitoreo y despliegue del SQX Worker:
  1. **SQX Watcher**: Corriendo bajo la sesión de `screen` `watcher` con el comando `./run_watcher.sh ./input`.
  2. **Deployer Watcher**: Corriendo bajo la sesión de `screen` `deployer` con el comando `./run_deployer.sh ./deploy deploy`.
- Ambas sesiones quedaron en estado `Detached`.

## Diagnóstico de Falla (2026-07-10)
- El watcher falló al validar la configuración de `input/config.json`.
- Específicamente, `config.json` busca el archivo `retester_test.cfx`, pero en la carpeta `input/` el archivo se llama físicamente `retest_test.cfx`.
- Error reportado: `archivos de configuración faltantes: [retester_test.cfx]`.

