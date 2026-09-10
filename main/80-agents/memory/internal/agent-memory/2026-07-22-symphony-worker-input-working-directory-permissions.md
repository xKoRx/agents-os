---
type: agent_memory
scope: project
created: 2026-07-22
updated: 2026-09-09
index_priority: never
indexable: false
load_policy: manual
memory_state: archived
tags:
  - project/symphony
  - tech/systemd
  - bug/permissions
---

# Symphony worker relative input path depends on WorkingDirectory

Diagnóstico verificado el 2026-07-22 en los workers SQX versión `0.1.130`:

- Zeus ejecuta `symphony-worker.service` como `kor:kor` con `WorkingDirectory=/var/lib/symphony`; el proceso `symphony` hereda ese cwd y puede crear `input/`.
- Hera y Kronos conservan unidades antiguas con `WorkingDirectory=/opt/symphony/current/bin`; el symlink resuelve al directorio de release, propiedad `symphony:symphony` y modo `0755`, por lo que `kor` no puede crear `input/`.
- `apply_selected_run` usa una ruta relativa `input/<strategy>.sqx` y llama `os.MkdirAll`, causando `mkdir input: permission denied` en Hera y Kronos.
- Los logs confirmaron el mismo workflow y artifact fallando en ambos hosts; Zeus no presentó el error.

Remediación aplicada y verificada: Hera y Kronos recibieron una copia exacta de la unidad de Zeus, se ejecutó `systemctl daemon-reload` y se reiniciaron ambos servicios. Los tres hosts quedaron activos en `0.1.130`, con cwd `/var/lib/symphony`, prueba de escritura exitosa y SHA-256 de unidad `c8ecff5db3f9e7e2e9e5f4eb9cf4aed1b2c339124ffd00a924063eafab8f9a03`. Temporal ejecutó después el intento 9 de `apply_selected_run` y el workflow avanzó a `mt5_exporter`, confirmando la recuperación. La fuente operativa compartida quedó en `.agents/skills/worker-troubleshooting/SKILL.md` del repositorio Symphony; no relajar permisos dentro del release.
