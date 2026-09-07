---
type: change_log
scope: project
created: 2026-08-08
updated: 2026-08-08
area: "[[Personal]]"
project: "[[AGENTS OS - Fase 2]]"
entities:
  - "[[AGENTS OS]]"
  - "[[AGENTS OS - Fase 2]]"
related:
  - "[[agents-os-bootstrap]]"
  - "[[agents-os-doctor]]"
  - "[[Paths explícitos en lint omiten las exclusiones del corpus]]"
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
  - scope/project
  - project/agents-os
---

# AGENTS OS — G6 aceptado e inicio F7

## Cambio

- G6 pasó de `review` a `accepted` por autorización condicionada del owner,
  satisfecha con evidencia verde.
- El planificador corrigió estados obsoletos de requerimientos y abrió el
  paquete F7 de retrofit/endurecimiento gradual.
- La tarea puente del parent volvió a WIP mientras G7 siga abierto.
- Se publicó el aprendizaje reusable sobre la diferencia entre baseline
  all-vault sin paths y lint dirigido con paths explícitos.

## Validación

- Doctor estricto: `HIGH=0 MEDIUM=0 LOW=0`, startup aproximado 4979 tokens.
- Graphify reindexó y `explain "AGENTS OS - Fase 2"` resolvió el planificador
  canónico vigente.
- Baseline lint canónico: `ERROR=237 WARN=84`, 485 notas. Clases ERROR:
  `missing-field=149`, `unknown-type=60`, `s1-status=24`, `bad-status=3`,
  `bad-owner=1`. Clases WARN: `no-frontmatter=81`, `no-type=3`.
- Distribución de ERROR por raíz: `80-agents=182`, `30-resources=32`,
  `10-projects=21`, `90-system=2`.

## Decisión F7

- Priorizar lotes P1 con metadata verificable.
- Mantener `warn-first` hasta limpiar el corpus activo o justificar exclusiones.
- No escalar moves por área antes de validar rescan path-based en una vista
  real.
- Próximo paso exacto: T7.3.

## Rollback

- Volver G6 a `review`, retirar el paquete/tareas G7 y devolver la tarea puente
  a Review. No hubo cambios de runtime ni movimientos físicos.
