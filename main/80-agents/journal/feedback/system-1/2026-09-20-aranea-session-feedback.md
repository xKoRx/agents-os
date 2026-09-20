---
type: session_feedback
schema_version: 1
created: "2026-09-20"
area: "[[Aranea]]"
project: "[[BACKUP-DR-OWNER-PROJECT]]"
source_session:
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/session-feedback
  - scope/session
  - area/aranea
---

# 2026-09-20-aranea-session-feedback

Fricción real detectada en esta sesión:

- `memory` tool: límite 2.200 chars alcanzado; un batch requiere contar caracteres de TODAS las entradas a mano (las operaciones largas fallan all-or-nothing con delta de 3 chars). Pain pattern candidate: la herramienta no entrega el tamaño por entrada, obligando a cálculo manual iterativo (3 intentos en esta sesión).
- `patch` sobre tablas markdown largas: un old_string parcial puede dejar filas deformadas (celda extra) cuando el reemplazo cambia el número de columnas; requirió re-patch de la fila. Sugerencia: validar conteo de `|` por fila en edits de tablas.
- Matriz generada por script y concatenada con `cat >>` funcionó bien ( patrón a repetir para tablas grandes), pero el write_file inicial del mismo archivo perdió el cierre de tabla header — concatener header+rows en una sola operación hubiera evitado un parche.
