---
type: agent_memory
scope: project
tags:
  - kind/learning
  - project/symphony
  - area/sqx
created: 2026-07-15
updated: 2026-07-15
---

# Continuidad Cognitiva: Análisis de Mismatch de Namespaces y Task Queues (Zeus vs Local)

En esta sesión se diagnosticó y resolvió un problema de ejecución de flujos de trabajo en Temporal tras el despliegue de la versión `0.1.123` en el worker Zeus.

## Diagnóstico y Causa Raíz

1. **Estado de Zeus**:
   - Tanto `symphony-worker` (versión `0.1.123`) como `symphony-watcher` en Zeus están activos.
   - El worker de Zeus está registrado y escuchando activamente en la cola de tareas `sqx-main-queue` bajo el namespace **`sqx-prop`**.

2. **Mismatch de Namespaces y Task Queues**:
   - Los archivos de configuración de la ejecución fueron depositados en la carpeta local `./input` del MacBook, no en Zeus.
   - El watcher local (con `ENV=development`) detectó los archivos, los procesó y despachó el workflow al namespace **`sqx-dev`** (desarrollo) y en la task queue **`sqx-dev-queue`**.
   - Los workers de Zeus escuchaban solo en `sqx-prop` y en `sqx-main-queue`.

3. **Acciones Tomadas**:
   - Se actualizó la clave de ETCD `/sqx-watcher/development/temporal/namespace` a `"sqx-prop"`.
   - Se actualizó la clave de ETCD `/sqx-watcher/development/sqx/task_queue` a `"sqx-main-queue"`.
   - Se terminaron de forma ordenada las ejecuciones anteriores en Temporal que estaban congeladas.
   - Se limpió y reinició la sesión de `screen` `watcher` local con las nuevas configuraciones de ETCD.
   - Se volvieron a encolar los archivos en `input/` eliminando el prefijo del nombre para que el watcher local volviera a procesar de forma íntegra.

4. **Resultado**:
   - El watcher local despachó con éxito el workflow `sqx-main-00_configs-v38-NDX-H1-L-1784094403` a `sqx-prop` y `sqx-main-queue`.
   - El worker de Zeus tomó la ejecución inmediatamente y está completando las actividades.
