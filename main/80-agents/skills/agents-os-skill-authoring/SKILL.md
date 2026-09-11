---
type: skill
schema_version: 1
name: agents-os-skill-authoring
scope: global
created: 2026-07-03
updated: 2026-09-11
description: Classify, design, review, refine, or deprecate an AGENTS OS skill. Use when shaping a repeatable agent workflow or deciding whether responsibility belongs to a skill, runbook, or memory. Keeps SKILL.md lean, defines the trigger boundary, and delegates deterministic materialization, validation, rollback, and change-log mechanics to the linked runbook.
aliases:
  - agents-os-skill-authoring
load_policy: manual
indexable: true
index_priority: high
tags:
  - kind/skill
  - action/skill-authoring
  - tech/agents-os
  - scope/global
---

# AGENTS OS Skill Authoring

## Purpose

Diseñar o revisar el contrato de comportamiento de una skill de AGENTS OS.

Esta skill es policy + orchestration: decide clasificación, trigger boundary, forma del contenido y handoffs. No ejecuta materialización determinista, validaciones mecánicas, rollback ni la mecánica del `change_log`; eso pertenece al runbook enlazado.

Trigger boundary:

- **Sí cargar:** crear, revisar, refinar o deprecar una skill; o clasificar un workflow repetible antes de diseñarlo.
- **No cargar:** ejecutar un procedimiento operacional ya definido, capturar memoria o editar documentación que no cambia el contrato de una skill.
- **Handoff:** runbook → flujo/runbook correspondiente; memoria → `agents-os-memory-distillation`; trabajo mecánico sobre una skill → `../../memory/public/runbook/agents-os-skill-authoring.md`.

## Minimal Read

Leer sólo:

1. `../_shared/note-types.md` — clasificación skill vs runbook vs memoria.
2. `../_shared/skill-contract.md` — contrato canónico y criterio Draft→Ready.
3. `../../templates/skill.md` — shape canónico de una skill.
4. `../../memory/public/runbook/agents-os-skill-authoring.md` — sólo al materializar, modificar, validar, deprecar o recuperar una skill.

No repetir aquí el contenido de esas fuentes: siguen siendo canónicas.

## Procedure

1. **Clasificar el artefacto.** Decidir skill, runbook o memoria antes de diseñar contenido. Si no es skill, detener este flujo y hacer handoff al artefacto dueño.
2. **Definir el trigger boundary.** Explicitar qué habilita la skill, cuándo sí carga, cuándo no carga y qué artefacto vecino posee lo fuera de scope.
3. **Elegir el grado de libertad.** Mantener decisiones contextuales y juicio del agente en la skill. Mover procedimientos deterministas, mecánicos, sensibles a fallos, checkpointed o rollbackable a runbook o recurso ejecutable.
4. **Diseñar el contrato mínimo útil.** Usar las secciones requeridas por `skill-contract.md`. Cada instrucción debe cambiar una decisión del agente, prevenir un fallo conocido, definir un handoff o restringir el output.
5. **Externalizar soporte.** Rationale y explicación humana extensa van fuera de `SKILL.md`; referencias grandes, ejemplos y material reusable también. Enlazar fuentes canónicas en vez de copiarlas.
6. **Revisar discoverability y activación.** `name`, `description`, Purpose y Procedure deben describir la misma capacidad. Probar al menos un caso positivo, uno negativo y uno adyacente.
7. **Delegar ejecución determinista.** Usar `../../memory/public/runbook/agents-os-skill-authoring.md` para materializar o modificar archivos, validar Draft→Ready, manejar fallos/rollback y registrar el `change_log` requerido.

## Output

```text
Artefacto:            skill | runbook | memoria — <justificación breve>
Trigger boundary:
  Sí:                 <cuándo cargar>
  No:                 <cuándo no cargar>
  Handoff:            <artefacto vecino, si aplica>

Skill:                <ruta | no aplica>
Runbook:              <ruta usada/creada | no aplica>
Fuentes canónicas:    <rutas>
Draft→Ready:          PASS | FAIL — <motivo>
Activación:
  Positiva:           PASS | FAIL
  Negativa:           PASS | FAIL
  Adyacente:          PASS | FAIL
Change log:           <ruta | pendiente si FAIL>
```

## Hard Rules

- Un artefacto tiene un tipo primario; nunca fusionar skill, runbook y memoria.
- Reglas canónicas se referencian, no se duplican.
- `description` debe expresar capacidad y contexto de activación; evitar triggers catch-all.
- `SKILL.md` permanece agent-facing y lean; rationale y explicación larga viven fuera.
- Procedimientos deterministas, checkpointed o rollbackable pertenecen a runbook o recurso ejecutable.
- Toda skill creada, refinada o deprecada debe pasar el criterio Draft→Ready canónico vigente.
- Todo cambio de lifecycle de una skill debe producir el `change_log` exigido por la constitución.
- No inventar sintaxis de tooling: la ejecución mecánica debe consultar el contrato y ayuda vigentes.
