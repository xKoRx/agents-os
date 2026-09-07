---
type: change_log
scope: session
created: 2026-07-23
updated: 2026-07-23
area: "[[Echo]]"
project: "[[Echo Forge]]"
application: "[[echo-forge]]"
entities:
  - "[[Echo Forge]]"
  - "[[Echo Forge - Etapa 4]]"
  - "[[Echo Forge - Cierre de Etapa 4]]"
related: []
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
  - scope/session
  - area/echo
  - project/echo-forge
---

# Echo Forge — whitelist de proyectos fijos y deprecación de Automator

> [!warning]
> **Superseded el 2026-07-23:** la afirmación “exactamente cuatro proyectos” fue corregida por el owner. La resolución vigente está en `2026-07-23-echo-forge-tradelist-fifth-dynamic-project-conflict-resolution.md`: son cinco proyectos independientes y TradeList es el quinto.

## Cambio

- **Tipo:** conflict-resolution
- **Archivo(s):**
  - `10-projects/Echo Forge/Echo Forge.md`
  - `10-projects/Echo Forge/agentes/Echo Forge - Etapa 4.md`
  - `10-projects/Echo Forge/agentes/Echo Forge - Cierre de Etapa 4.md`
  - `10-projects/Echo Forge/agentes/PHASE-0-SPEC-ALIGNMENT.md`
  - `80-agents/memory/internal/agent-memory/2026-07-23-echo-forge-stage4-phased-metrics-continuity.md`

## Motivo

- La documentación vigente trataba `EchoForgeAutomator` como proyecto fijo y permitía interpretar `EchoForgeTradeListExporter` como un quinto proyecto SQX.
- El owner confirmó que `EchoForgeAutomator` está deprecado y que la arquitectura debe conservar exactamente cuatro proyectos fijos especializados.

## Fuentes usadas

- Decisión explícita del owner, 2026-07-23.
- Plan canónico `[[Echo Forge - Cierre de Etapa 4]]`.
- Arquitectura del proyecto padre `[[Echo Forge]]`.

## Resolución aplicada

- Whitelist exclusiva: `EchoForgeOverviewExporter`, `EchoForgeWFMExporter`, `EchoForgeMT5Exporter`, `EchoForgeRobustRunExporter`.
- `EchoForgeAutomator` queda como evidencia histórica/deprecada y no puede usarse como project, mapping, stage, task type, deployment target ni fallback.
- `EchoForgeTradeListExporter` se mantiene como componente Java dedicado, no como proyecto fijo. F0 debe fijar su host runtime entre WFM, RobustRun o ambos.
- El plan sube a v0.8 e incorpora `OD-A01`, asserts de gate, DoD, tareas y prompt executor para proteger la whitelist.

## Validación

- `validate_plan.py` pasó: `7` fases, `7` gates, `7` dispatches, `65` referencias locales, `0` errores y `0` warnings.
- Búsqueda enfocada confirmó que toda mención restante a Automator está marcada como histórica, deprecada, prohibida o como condición de migración/bloqueo.
- La única aparición positiva de `EchoForgeTradeListExporter/` está dentro de reglas que prohíben crear ese proyecto fijo.
- El vault no expone un worktree Git utilizable desde esta ruta; la validación estructural se realizó con el validador canónico y búsquedas focalizadas.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin secretos ni evidencia pesada.

## Rollback

- Revertir estos cambios documentales solo si el owner redefine explícitamente la whitelist de proyectos fijos; no restaurar Automator por inferencia desde nombres históricos de JAR o código.
