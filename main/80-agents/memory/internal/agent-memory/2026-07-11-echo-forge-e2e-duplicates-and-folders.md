---
type: agent_memory
scope: internal
created: "2026-07-11"
updated: "2026-07-11"
load_policy: manual
indexable: false
tags:
  - kind/agent-memory
  - scope/internal
---

# Continuidad — Echo Forge E2E Duplicates & Dynamic Folders (2026-07-11)

- **Estado actual**: Se ha validado con éxito el desacoplamiento de archivos `.sqx` en tareas exportadoras y la parametrización dinámica de carpetas para robustez.
  - Parent Workflow: `sqx-main-00_configs-v14-NDX-H1-L-1783793477` (Ola `v14`).
  - Versión del Worker Activa: `0.1.85` (compilada y desplegada en Zeus, 192.168.31.101).
- **Logros clave**:
  1. **Cero Duplicados en PostgreSQL y MinIO**: Verificamos mediante `inspect_postgres.go` y `count_v14_minio.go` que las tareas de tipo exportador (`overview_exporter` y `wfm_exporter`) procesan exclusivamente metadatos y no registran ni suben archivos `.sqx`.
  2. **Carpetas Dinámicas**: Parametrizamos el destino de `apply_selected_run` inyectando `task.Folder` (ej. `"04_optimizer_robust"`).
  3. **Ejecución Completa**: El watcher detectó exitosamente `input/config.json`, validó y gatilló la ola `v14` que corrió hasta el paso `generate_report` de manera exitosa.
- **Auditoría de Datos (v14)**:
  - **MinIO**: La carpeta `metadata/` tiene 0 archivos `.sqx`. Las estrategias se almacenan únicamente bajo `01_builder/` y `02_retester/`. Las carpetas `03_optimizer/` y `04_optimizer_robust/` sólo contienen su `.folder_marker` debido a descarte legítimo del motor SQX en esta iteración.
  - **PostgreSQL**: Registró 13 estrategias para `01_builder` y 33 para `02_retester`. Registros en `03_optimizer`, `metadata` o exportadores en la versión `v14` son exactamente **0**, confirmando la remoción total de duplicados.
