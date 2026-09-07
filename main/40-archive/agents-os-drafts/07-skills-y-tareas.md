---
type: doc
status: draft
tags:
  - kind/doc
  - kind/system
  - tech/agents-os
  - tech/skills
created: 2026-06-27
updated: 2026-06-27
---

# 07 — Skills y tareas de implementación

[[agents-os|← Volver al índice]]

## Objetivo

Definir el backlog para terminar las skills del **AGENTS OS**. Cada skill vive en `80-agents/skills/`, tiene un `SKILL.md` compacto y registra su avance en el mismo archivo.

La regla de diseño es: **cargar poco, decidir rápido y abrir referencias solo cuando hagan falta**.

## Estructura creada

```text
80-agents/memory/
  public/
    constitution/
    user-preference/
    learning/
    decision/
    known-error/
    runbook/
  internal/
    agent-memory/global/
80-agents/journal/
  sessions/raw/
  logs/
  hygiene/
80-agents/templates/
  raw-session.md
  session-summary.md
  learning.md
  decision.md
  known-error.md
  runbook.md
  change-log.md
  hygiene-report.md
  constitution.md
  user-preference.md
80-agents/skills/
  _shared/
    graphify-contract.md
    metadata-schema.md
    note-types.md
    skill-contract.md
  agents-os-bootstrap/
  agents-os-context-retrieval/
  agents-os-session-close/
  agents-os-memory-distillation/
  agents-os-entity-update/
  agents-os-conflict-resolution/
  agents-os-graphify-maintenance/
  agents-os-hygiene-review/
  agents-os-retrofit-raw-session/
  agents-os-behavior-config/
80-agents/adapters/
  codex.md
  claude.md
  cursor.md
  antigravity.md
```

## Orden recomendado

1. **Contrato base** — cerrar `_shared/skill-contract.md`, reconciliar `_shared/metadata-schema.md` con `80-agents/agents-os/_drafts/Agent Memory Properties.md`, cerrar `_shared/note-types.md` y `_shared/graphify-contract.md`.
2. **MVP operativo** — terminar `agents-os-bootstrap`, `agents-os-context-retrieval`, `agents-os-session-close`, `agents-os-memory-distillation`, `agents-os-conflict-resolution`.
3. **Mantenimiento** — terminar `agents-os-entity-update`, `agents-os-graphify-maintenance`, `agents-os-hygiene-review`.
4. **Retrofit** — terminar `agents-os-retrofit-raw-session`.
5. **Configuracion conversacional** — terminar `agents-os-behavior-config` para actualizar comportamiento, preferencias y promocion de memoria interna.
6. **Adaptadores por superficie** — mantener `80-agents/adapters/` como capa operativa para Codex, Claude, Cursor y Antigravity sin cambiar semántica de `SKILL.md`.

## Backlog por skill

### 00 — Bootstrap

Ruta: `80-agents/skills/agents-os-bootstrap/SKILL.md`

- [x] Definir fuente final de reglas globales.
- [x] Definir fallback exacto cuando Graphify no esté disponible.
- [x] Agregar ejemplos de sesión por proyecto, app y ámbito transversal.
- [x] Probar con un agente fresco sobre una tarea real.

### 01 — Context Retrieval

Ruta: `80-agents/skills/agents-os-context-retrieval/SKILL.md`

- [x] Confirmar comandos finales de Graphify.
- [x] Definir contrato para IDEs/agentes sin shell.
- [x] Definir política de recorte por presupuesto de contexto.
- [x] Agregar ejemplo con una aplicación real del vault.
- [x] Incorporar memoria interna always-load y objetivo de contexto inicial cercano a 3.000 tokens.

### 02 — Session Close

Ruta: `80-agents/skills/agents-os-session-close/SKILL.md`

- [x] Usar ubicación física final de raw sessions y summaries bajo `80-agents/journal/sessions/`.
- [x] Crear templates L0/L1.
- [x] Definir cierre liviano para sesiones sin conocimiento persistible.
- [ ] Probar con un transcript real.

### 03 — Memory Distillation

Ruta: `80-agents/skills/agents-os-memory-distillation/SKILL.md`

- [x] Finalizar templates de learning, ADR, known error y runbook.
- [x] Definir umbrales de promoción y confidence.
- [x] Definir detección de duplicados.
- [x] Agregar ejemplos de descarte por no reutilizable.
- [x] Definir creación/edición/eliminación directa de memoria pública con log auditable.

### 04 — Entity Update

Ruta: `80-agents/skills/agents-os-entity-update/SKILL.md`

- [x] Definir secciones canónicas para entidades.
- [x] Implementar edición directa para MVP con log en `80-agents/journal/logs/`.
- [x] Agregar ejemplos de app, proyecto y concepto.
- [x] Definir reglas de alias/nombres entre repos y entidades.

### 05 — Conflict Resolution

Ruta: `80-agents/skills/agents-os-conflict-resolution/SKILL.md`

- [x] Definir formato de log para conflictos resueltos.
- [x] Crear template de resolución si se decide usar nota dedicada.
- [x] Agregar ejemplos de fact obsoleto y learning obsoleto resueltos por agente.

### 06 — Graphify Maintenance

Ruta: `80-agents/skills/agents-os-graphify-maintenance/SKILL.md`

- [x] Documentar watcher como mejora post-beta.
- [x] Documentar `.graphifyignore` y rutas include/exclude.
- [x] Agregar queries de validación reales.
- [x] Definir detección de índice obsoleto.

### 07 — Hygiene Review

Ruta: `80-agents/skills/agents-os-hygiene-review/SKILL.md`

- [x] Definir formato del reporte diario.
- [x] Separar fixes automáticos, ediciones directas con log y hallazgos que requieren tarea posterior.
- [x] Definir marcador de última revisión.
- [x] Agregar checks de links rotos y aliases.

### 08 — Retrofit Raw Session

Ruta: `80-agents/skills/agents-os-retrofit-raw-session/SKILL.md`

- [x] Definir metadata de backfill.
- [x] Definir límites de batch/contexto.
- [x] Implementar detección de duplicados contra L3.
- [x] Probar con una sesión antigua.

### 09 — Behavior Config

Ruta: `80-agents/skills/agents-os-behavior-config/SKILL.md`

- [x] Definir clasificación entre instrucción temporal, preferencia, constitución, memoria pública, memoria interna y Capa 1.
- [x] Definir edición directa con logs para cambios de comportamiento persistente.
- [x] Definir promoción de memoria interna a pública.
- [x] Probar con una directiva conversacional temporal que no debe persistirse.

## Cómo registrar avance

Cuando un agente tome una tarea:

1. Marcar la tarea en este documento si cambia el estado general.
2. Marcar la tarea equivalente dentro del `SKILL.md`.
3. Agregar una línea breve en `## Progress Log` de la skill.
4. Si surge una decisión de diseño estable, promoverla a ADR más adelante.

Formato de bitácora:

```md
- 2026-06-27: Se cerró X. Archivos tocados: Y. Pendiente: Z.
```

## Criterio de terminado

Una skill pasa de draft a ready cuando:

- el `SKILL.md` se valida como skill;
- sus referencias necesarias existen;
- tiene ejemplos suficientes para no depender del autor original;
- fue probada al menos una vez con una tarea real;
- no necesita leer el monolito `80-agents/AGENTS.md` para operar.
