---
type: agent_memory
scope: continuity
created: "2026-07-20"
updated: 2026-09-09
index_priority: never
indexable: false
memory_state: archived
area: symphony
project: "[[Symphony]]"
application: "[[Echo Forge]]"
entities:
  - "[[Symphony]]"
related:
  - "[[2026-07-20-sqx-parallel-concurrency-verification-success]]"
aliases: []
confidence: verified
load_policy: manual
tags:
  - kind/continuity
  - scope/session
---

# SQX RequestID-TraceID Alignment v0.1.126 Continuity

## Estado

- **Deploy v0.1.126** staged y activo en Zeus (PID 782876, desde 2026-07-20T09:45:05-04:00).
- **Cambios**: `generic_workflow.go` alinea `RequestID` con `TraceID` de telemetría; `steps.go` agrega fallback de descarga usando TraceID del contexto.
- **Pendiente**: Validación E2E con 3+ flujos paralelos (example_flow_13/14/15).

## Causa raíz resuelta

El watcher subía configs a MinIO bajo el TraceID (ej. `8ea5254c...`), pero el workflow generaba un RequestID random UUID, provocando `NoSuchKey` intermitente al descargar.

## Atención para próxima sesión

1. Ejecutar validación E2E usando el prompt maestro en `prompt_maestro_validacion.md` (artifact de la sesión 9bd0bcfc).
2. Si el fallback se activa en logs → la alineación primaria no resolvió todos los casos → investigar flujo de propagación de `Telemetry.TraceID` en la cadena watcher→config→workflow.
3. Verificar que no haya regresiones en otros tipos de tareas (evaluate_wfm, select_robust_run, apply_selected_run).
