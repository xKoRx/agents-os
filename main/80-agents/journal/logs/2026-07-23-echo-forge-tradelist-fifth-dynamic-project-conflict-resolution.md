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
related:
  - "[[Echo Forge - Desacoplamiento SOLID del Pipeline]]"
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

# Echo Forge — TradeList como quinto proyecto dinámico

## Cambio

- **Tipo:** conflict-resolution
- **Archivo(s):**
  - `10-projects/Echo Forge/Echo Forge.md`
  - `10-projects/Echo Forge/agentes/Echo Forge - Etapa 4.md`
  - `10-projects/Echo Forge/agentes/Echo Forge - Cierre de Etapa 4.md`
  - `10-projects/Echo Forge/agentes/Echo Forge - Desacoplamiento SOLID del Pipeline.md`
  - `10-projects/Echo Forge/agentes/PHASE-0-SPEC-ALIGNMENT.md`
  - `80-agents/memory/internal/agent-memory/2026-07-23-echo-forge-stage4-phased-metrics-continuity.md`
  - `80-agents/journal/logs/2026-07-23-echo-forge-fixed-project-whitelist-conflict-resolution.md`

## Motivo

- El agente asumió incorrectamente que TradeList debía alojarse dentro de WFM/RobustRun para conservar cuatro proyectos.
- El owner aclaró que `EchoForgeTradeListExporter` debe ser un quinto proyecto fijo independiente y que la definición dinámica del flujo decide qué piezas usar y cuándo.

## Fuentes usadas

- Corrección explícita del owner, 2026-07-23.
- Plan canónico `[[Echo Forge - Cierre de Etapa 4]]`.

## Resolución aplicada

- Registro objetivo: Overview, WFM, TradeList, MT5 y RobustRun como cinco proyectos fijos independientes.
- `EchoForgeAutomator` continúa deprecado.
- El flujo elige proyecto, source/input y orden por configuración; no usa mappings estáticos por tipo ni invocaciones implícitas entre exporters.
- El plan sube a v0.9 y reabre de forma acotada T0.1/T0.2/T0.4; T0.3 continúa pendiente y es requisito de G0. La evidencia F0 existente se reutiliza; G0 permanece `pending`.
- F0 valida contratos/capabilities y deja TradeList como `create`; F2 crea y prueba el proyecto real.

## Validación

- Validador canónico: `phases=7`, `gates=7`, `dispatches=7`, `local_refs=65`, `errors=0`, `warnings=0`.
- No quedan prohibiciones activas contra el quinto proyecto; las afirmaciones v0.8 sobreviven únicamente como historial explícitamente superseded.
- F0 distingue cuatro proyectos actualmente presentes + `EchoForgeTradeListExporter` target `missing/create`; el smoke real del quinto proyecto queda reservado a F2/G2.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin secretos ni evidencia pesada.

## Rollback

- Solo una nueva decisión explícita del owner puede cambiar el registro de cinco proyectos o volver estática la composición del flujo.
