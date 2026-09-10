---
type: agent_memory
scope: internal
created: 2026-07-05
updated: 2026-09-09
index_priority: never
indexable: false
load_policy: manual
memory_state: archived
tags:
  - kind/agent_memory
  - tech/go
  - app/echo-forge
  - topic/workflow
  - topic/configuration
---

# Continuidad Operativa: Configuración de Flujo SQX con Builder, Export y Rankeo

## Qué se hizo
- Configuramos un flujo de trabajo SQX de 3 tareas: Builder, Export y Rankeo (classify_and_rank).
- Escribimos un archivo de configuración JSON de ejemplo en `input/example/config.json` dentro de la raíz del repositorio `symphony`.
- Documentamos cómo funciona cada una de las 3 tareas y qué pasos ejecuta el orquestador `GenericSQXWorkflow`.
- **Diagnóstico y Corrección (WIP & Success)**:
  - Descubrimos que el flujo fallaba en `classify_and_rank` con `metadata missing for wave` debido a que el worker arrancaba en modo legacy sin MongoDB.
  - La causa raíz fue que la clave `/sqx-worker/production/feature/metadata_export` no existía en ETCD.
  - Escribimos el valor `"true"` a `/sqx-worker/production/feature/metadata_export` en ETCD.
  - Reiniciamos el servicio `symphony-worker` en el worker Zeus.
  - Copiamos el archivo de configuración y la base de builder a `./input` para re-lanzar el flujo.
  - El flujo `sqx-main-00_configs-v1-NDX-H1-L-1783290279` se procesó por completo, exportó la metadata a MongoDB (`databank_metadata` y `export_runs`), y rankeó exitosamente las estrategias guardándolas en `type_rankings`.
- **Limpieza de Colecciones y Nueva Verificación**:
  - Vaciamos por completo las colecciones de MongoDB: `databank_metadata`, `type_rankings` y `export_runs`.
  - Re-lanzamos el flujo con `sqx-main-00_configs-v1-NDX-H1-L-1783291196`.
  - El flujo ejecutó exitosamente las 3 tareas en limpio, insertando exactamente 1 registro en `export_runs`, 52 registros en `databank_metadata` y 24 registros en `type_rankings`.
- **Extensión con Subflujo de Retesteo y Early Exit**:
  - Extendimos `input/example/config.json` agregando una tarea de tipo `group` con origen en `ranking` y `top_n_per_logical_type: 1`.
  - Configuramos `batch_size: 2` y una subtarea de tipo `project` para ejecutar `02_retester_full` en Zeus.
  - Vaciamos MongoDB y relanzamos el flujo (`sqx-main-00_configs-v1-NDX-H1-L-1783292639`).
  - El flujo ejecutó en paralelo para los 27 tipos lógicos, subdividiendo en lotes de 2 y aplicando early-exit al pasar al menos 1 estrategia retesteada con éxito. Completó exitosamente sin fallos.



