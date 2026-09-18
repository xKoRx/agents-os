---
type: change_log
schema_version: 1
created: "2026-09-18"
area: "[[Personal]]"
project: "[[Loom — Product v0.2]]"
application: "[[Loom]]"
entities:
  - "[[Loom]]"
  - "[[Loom — Product v0.2]]"
tags:
  - kind/change-log
  - area/personal
---

# Change Log — 2026-09-18 Loom v0.2.1 release preparation (READY FOR OWNER ACCEPTANCE)

## Cambios

- **[[Loom — Product v0.2]]:** (1) nuevo primer bullet en *Estado actual* (READY FOR OWNER ACCEPTANCE @ `0cba972` con los 4 resultados del mandato); (2) 4 tareas nuevas ✅ en la fuente de tareas (fix arnés, accesibilidad, paquete de evidencia, gates SHA final); (3) entrada nueva al inicio de *Bitácora* (arnés, accesibilidad, evidencia, gates + justificación de gates no re-ejecutados). Sin cambios de decisiones ni de contrato; Reviews humanas intactas.
- **Nuevo run register:** `80-agents/journal/agent-runs/2026-09-18-zcode-glm-loom-v021-release-preparation.md`.

## Motivo

Mandato de dirección técnica "LOOM — FINAL RELEASE PREPARATION v0.2.1" (mismo día): corregir arnés de invarianza, cerrar evidencia de accesibilidad, exportar paquete visual y dejar la entrega lista para aceptación humana.

## Rollback

- Vault: revertir los 3 edits del planner (los bloques previos están en el historial de git del vault) y eliminar el run register + este change_log.
- Repo `xKoRx/loom`: el commit `0cba972` es aditivo sobre `ff53337` y sólo toca `internal/index/invariance_test.go`; revertir = `git revert 0cba972` + push (restauraría la dependencia ambiental del suite). El paquete de evidencia es un directorio/tarball fuera del repo: eliminarlo no afecta al producto.
