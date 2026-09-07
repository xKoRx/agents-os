---
type: change_log
scope: session
created: 2026-07-01
updated: 2026-07-01
area:
project: "[[AGENTS OS]]"
application:
entities:
  - "[[AGENTS OS]]"
related:
  - "[[agent-constitution]]"
  - "[[agents-os]]"
aliases: []
confidence: verified
source_session: 2026-07-01-prsm-scope-narrowed-to-artifact-differentiation
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
  - project/agents-os
---

# Constitución: diferenciación canónica Runbook / Skill / Memoria + change log obligatorio para skills

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `80-agents/memory/public/constitution/agent-constitution.md`

Dos ediciones quirúrgicas:

1. Nueva sección **"Diferenciación De Artefactos: Runbook, Skill y
   Memoria/Aprendizaje"**, insertada entre "Mandamientos De Memoria Interna" y
   "Evolución y Aprendizaje de Skills". Define de forma canónica y crisp los tres
   artefactos, agrega una regla de decisión rápida, y declara la constitución como
   versión de mayor autoridad frente a `_shared/note-types.md` (que sigue siendo la
   guía detallada). No duplica el detalle: lo referencia.
2. Nuevo **punto 6** en "Evolución y Aprendizaje de Skills": exige entrada
   `type: change_log` en `80-agents/journal/logs/` para toda skill creada, refinada
   o deprecada —incluida la autoevolución proactiva— cerrando el hueco por el que
   los cambios de skill no estaban en la lista de artefactos con log obligatorio.

## Motivo

- El owner acotó el alcance de la propuesta PRSM: conserva la diferenciación
  runbook/skill/memoria (su mayor aporte al sistema actual) y descarta las piezas
  que colisionaban (Policy como tipo nuevo, Inventory, Request Change).
- Se prioriza mantener las skills **autoevolutivas de manera proactiva** con
  bitácora impecable, en vez de introducir un gate de aprobación. Esto resuelve el
  conflicto de autonomía (antes C1) a favor de la proactividad + log auditable.
- La diferenciación ya existía en `_shared/note-types.md`; se eleva a principio de
  primera clase en la constitución (always-load, priority/critical) sin duplicar.

## Fuentes usadas

- `80-agents/skills/_shared/note-types.md` (sección "Skill vs Reusable Memory").
- Constitución vigente (§"Evolución y Aprendizaje de Skills", §"Reglas Base").
- `80-agents/agents-os/agents-os.md` (modelo Sistema 1 / Sistema 2).
- Decisión del owner en sesión: descartar Request Change / Policy / Inventory.

## Resolución aplicada

- Ediciones aplicadas directamente sobre la constitución (no vía Request Change,
  por decisión explícita del owner).
- Sin cambios a `note-types.md`; queda como guía detallada referenciada.
- No se introdujeron tipos, carpetas ni tags nuevos: cero colisión con lo vigente.

## Validación

- La constitución mantiene su estructura: Autoridad → Reglas Base → Mandamientos
  de Memoria Interna → **Diferenciación de Artefactos (nueva)** → Evolución y
  Aprendizaje de Skills (con punto 6 nuevo) → Cierre de Sesión.
- Frontmatter `updated: 2026-07-01` ya vigente; sin otros cambios de metadata.
- Pendiente: reindexar Graphify para reflejar la constitución actualizada
  (`graphify-obsidian update`) — no ejecutado en esta sesión.
