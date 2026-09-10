---
type: skill
schema_version: 1
name: agents-os-agent-project-workflow
scope: global
created: 2026-07-01
updated: 2026-08-24
description: Defines how an agent must operate an agent project (owner:agent) end to end — using the project's own note as the single planner, keeping its tasks/state/bitácora honest as work advances, and managing the parent's bridge task lifecycle (WIP -> Review -> human Done, or WIP <- Review on rejection). Use whenever an agent starts, resumes, advances, or closes work on an owner:agent project, or when creating one for the first time.
aliases:
  - agents-os-agent-project-workflow
load_policy: manual
indexable: true
index_priority: high
tags:
  - kind/skill
  - scope/global
  - action/agent-project-workflow
  - tech/agents-os
---

# agents-os-agent-project-workflow - Operar un proyecto de agente

## Purpose

Un proyecto de agente (`owner: agent`, ver `[[project-ownership-human-vs-agent]]`) es ejecución delegada con detalle pesado. Esta skill define cómo el agente debe trabajarlo sesión a sesión para que:

1. el progreso real quede siempre visible en la propia nota del proyecto (no en la cabeza del agente ni en un documento externo);
2. el humano pueda seguir el curro delegado con una sola tarea puente en su proyecto padre;
3. si el chat/sesión se corta o se pierde, **cualquier agente fresco** pueda retomar exactamente donde quedó, leyendo solo la nota.

Esta skill no reemplaza `agents-os-entity-lifecycle` (crear la entidad) ni `agents-os-session-close` (cierre completo de sesiones grandes). Es el protocolo de ejecución **dentro** de un proyecto de agente ya creado, y define un cierre proporcional para sesiones de ejecución.

## Minimal Read

Read only:
1. La nota del proyecto de agente en cuestión (planificador único — ver más abajo).
2. La tarea puente correspondiente en su proyecto padre.
3. `90-system/convenciones.md` sección "Proyectos humanos vs proyectos de agente" si hay duda de sintaxis/tags.

## El proyecto ES el planificador

**Regla dura:** la nota del proyecto de agente (`## 🎯 Objetivo`, `## 📊 Estado actual`, `## ✅ Tareas`, `## 📆 Bitácora`, `progress:`) es la única fuente de verdad de planificación para ese trabajo. No crear un plan paralelo en un archivo de scratch, un documento externo, o solo en el contexto de la conversación.

- Herramientas de tareas efímeras del entorno de ejecución (ej. `TaskCreate`/`TaskUpdate` del harness) se pueden usar libremente **dentro de una sesión** para organizar el trabajo inmediato, pero son desechables: antes de que la sesión termine, todo lo que deba sobrevivir (qué se hizo, qué falta, qué se decidió) debe quedar reflejado en la nota del proyecto. Si la sesión se corta antes de sincronizar, el estado durable es el que quedó escrito en la nota, no el que vivía solo en las tareas efímeras.
- Si el proyecto de agente no trae ya su plan de trabajo (checklist de tareas concreto), el agente debe escribirlo en `## ✅ Tareas` antes de empezar a ejecutar, no solo enumerarlo verbalmente en el chat.

## Procedure

### 1. Al iniciar o retomar

1. Abrir la nota del proyecto de agente. Leer `📊 Estado actual`, la fuente de tareas y la última entrada de `📆 Bitácora` — ahí está el punto exacto donde quedó el trabajo.
2. Si es un proyecto de desarrollo, validar `## 🧱 Entrega de desarrollo` antes de tocar código: cada repo afectado debe tener branch, base, SPEC funcional y SPEC técnica. Completar datos verificables; si falta una decisión material del owner, registrarla como bloqueo en vez de inventarla.
3. Si es la primera sesión sobre este proyecto y no trae checklist de tareas, escribirlo en `## ✅ Tareas` (fuente de tareas del proyecto) antes de tocar código u otros sistemas.
4. Confirmar que la tarea puente existe en el proyecto padre (`#owner/me #type/supervision`, ver [[project-ownership-human-vs-agent]]). Si no existe, crearla ahí mismo — es un requisito de la regla de creación de proyectos de agente en `agents-os.md`.

### 2. Mientras se ejecuta

1. Actualizar el estado de cada tarea (`[ ]→[/]→[r]→[x]`) en la nota **a medida que avanza el trabajo real**, no en un batch al final. Esto es lo que permite a otro agente saber, en cualquier punto, qué está hecho y qué no.
2. Actualizar `progress:` (frontmatter) y `## 📊 Estado actual` cuando cambien de forma material.
3. Agregar una línea a `## 📆 Bitácora` en hitos reales (no en cada micro-cambio): decisiones tomadas, hallazgos, bloqueos, y siempre que se retome tras una interrupción.
4. Si aparece un hallazgo que cambia el plan (ej. un requerimiento oculto, una regresión adicional), registrarlo en la nota antes de seguir — el plan vive ahí, se actualiza ahí.

### 3. Al terminar el trabajo planificado (listo para revisión humana)

1. Verificar que todas las tareas planificadas del ciclo actual quedaron en `[x]` (o explícitamente descartadas con motivo en la bitácora) dentro de la nota del proyecto de agente.
2. Actualizar `## 📊 Estado actual` con el resultado final verificable (tests corridos, comandos ejecutados, evidencia).
3. En el proyecto **padre**, mover la tarea puente de WIP (`[/]`) a **Review** (`[r]`). El agente nunca marca la tarea puente como Done (`[x]`) — esa decisión es del humano, es la semántica de "puente": el agente entrega, el humano acepta.
4. Dejar en la bitácora del proyecto de agente un resumen breve de qué queda listo para revisión y qué evidencia lo respalda.

### 4. Si el humano rechaza la entrega

1. Mover la tarea puente en el proyecto padre de Review (`[r]`) de vuelta a WIP (`[/]`).
2. Registrar el motivo del rechazo en `## 📆 Bitácora` del proyecto de agente (qué se rechazó y por qué, en la medida en que el humano lo haya explicado).
3. Reabrir/crear las tareas necesarias en `## ✅ Tareas` para corregir.
4. Corregir, repitiendo el paso 2 (mientras se ejecuta).
5. Al corregir, avanzar la tarea puente nuevamente a Review (`[r]`). Repetir el ciclo tantas veces como sea necesario.

### 5. Cierre proporcional de la sesión de ejecución

No todo avance sobre un proyecto de agente amerita un cierre completo de AGENTS OS (L0+L1+feedback+distillation). Usar:

- **Cierre liviano** (default para una sesión normal de ejecución sobre un proyecto de agente ya existente): dejar la nota del proyecto actualizada (pasos 2-4 arriba) y, si cambió una entidad Sistema 2 real (ej. una app, un contrato), llamar a `agents-os-entity-update` con su log. No se requiere L0/L1/feedback por cada sesión de ejecución.
- **Cierre completo** (`agents-os-session-close`): cuando la sesión produjo conocimiento reusable más allá del propio proyecto (un aprendizaje, una decisión, un known error, un runbook), cuando el usuario pide explícitamente cerrar sesión, o cuando el proyecto de agente mismo se da por terminado (todas sus tareas `[x]`, tarea puente en `[x]` confirmada por el humano).

## Output

```text
Proyecto de agente:
Tarea puente (proyecto padre):
Estado de tareas actualizado en la nota: sí/no
Progreso (frontmatter): antes -> después
Bitácora actualizada: sí/no
Tarea puente movida: [ ]/[/]/[r]/[x] -> [ ]/[/]/[r]/[x]
Motivo (si fue rechazo): 
Cierre aplicado: liviano/completo
```

## Hard Rules

- La nota del proyecto de agente es el planificador único. No mantener un plan paralelo fuera de ella que sobreviva más allá de la sesión actual.
- El agente nunca marca `[x]` la tarea puente. Máximo llega a `[r]` (Review).
- Un rechazo del humano siempre se registra en la bitácora del proyecto de agente antes de corregir — no se corrige en silencio.
- No dejar la nota "desactualizada pero mentalmente al día" al terminar una sesión: si el chat se corta ahora mismo, la nota debe ser suficiente para que otro agente continúe sin preguntar nada al humano.
- No ejecutar cambios de un proyecto de desarrollo con SPECs o branch/base sin especificar; la tabla del proyecto es el gate durable y se actualiza cuando cambie cualquiera de esas referencias.
- Esta skill aplica a proyectos `owner: agent`. Para proyectos `owner: me`, el principio de "usar la nota como planificador" es buena práctica recomendada, pero el ciclo de tarea puente no aplica (el humano ya es dueño directo de sus propias tareas).

## Judgment Calls Registrados

Estas decisiones no estaban completamente especificadas por el usuario al crear esta skill; se registran aquí explícitamente para que puedan revisarse o corregirse:

- Se asumió que **solo el humano** cierra la tarea puente (`[x]`), nunca el agente. Basado en la semántica de "puente" y en que el usuario describió el ciclo como avanzar a Review tras corregir, no como auto-cerrar.
- Se definió una distinción entre **cierre liviano** (una sesión normal de ejecución) y **cierre completo** (`agents-os-session-close`) para evitar que cada micro-avance sobre un proyecto de agente dispare L0/L1/feedback completos, lo cual sería desproporcionado y ruidoso. El criterio de cuándo aplica cada uno queda sujeto a ajuste si genera fricción.
- El principio de "usar la nota como planificador" se extendió como recomendación (no regla dura) también a proyectos `owner: me`, por consistencia, aunque el usuario lo pidió explícitamente solo para proyectos de agente.
