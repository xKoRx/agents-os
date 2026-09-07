---
type: change_log
scope: session
created: "2026-07-01"
updated: "2026-07-01"
area: "[[Personal]]"
project: "[[AGENTS OS]]"
application:
entities:
  - "[[AGENTS OS]]"
  - "[[AGENTS OS - Beta y Hardening]]"
related:
  - "[[project-ownership-human-vs-agent]]"
  - "[[agents-os-agent-project-workflow]]"
  - "[[agents-os-vault-refactor]]"
aliases:
  - agents os self migration
  - agents os dogfooding ownership model
confidence: verified
source_session:
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# Migración de AGENTS OS al modelo de ownership humano/agente (dogfooding)

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/slugs son solo automatización. %%

## Cambio

- **Tipo:** created / updated
- **Archivo(s):**
  - `10-projects/AGENTS OS/agentes/AGENTS OS - Beta y Hardening.md` (creado)
  - `10-projects/AGENTS OS.md` (editado)
  - `80-agents/memory/public/decision/agents-os/project-ownership-human-vs-agent.md` (editado, sección Consecuencias)

## Motivo

- El proyecto `[[AGENTS OS]]` (`owner: me`) tenía prácticamente todo su roadmap interno (Fases 0-6) como tareas sueltas `#owner/agent` sin tarea puente ni proyecto de agente separado, inconsistente con el modelo de ownership humano/agente que el propio proyecto implementó en el resto del vault. Esta deuda ya estaba flageada explícitamente en la bitácora de `AGENTS OS.md` (2026-07-01) y en las consecuencias de `[[project-ownership-human-vs-agent]]`.
- Tarea: evaluar (a) dejarlo como excepción documentada por ser el proyecto meta del sistema, vs. (b) migrar siguiendo `agents-os-vault-refactor` y `agents-os-agent-project-workflow`.

## Evaluación

- **Contra la excepción (a):** la propia decisión que originó el modelo ya registraba esto como deuda pendiente de migración, no como excepción aceptada. Mantener AGENTS OS afuera del modelo que él mismo define rompe la credibilidad del dogfooding y viola la regla de higiene/consistencia de la constitución (`agent-constitution.md`).
- **Contra migrar todo el roadmap sin acotar:** la mayoría de las Fases 0-4 y de la Fase 6 ya están `[x]` cerradas — son registro histórico del diseño del propio sistema, no ejecución activa que alguien deba supervisar vía tarea puente. Convertir historial cerrado en un proyecto de agente aparte habría fragmentado la narrativa de diseño (hoy legible de corrido en `AGENTS OS.md`) sin ganancia operativa real: una tarea `[x]` no ensucia los boards To Do/WIP/Review (se filtran por estado), y el único punto real donde sí aparecía sin filtrar era el Tablero final del propio proyecto (ver hallazgo abajo).
- **Decisión tomada:** migración acotada. Se migró únicamente la ejecución **abierta**: Fase 5 completa (beta en proyecto real, 6 tareas, ninguna iniciada) y el único ítem abierto de Fase 6 (evaluación de watcher post-beta). Esto es exactamente el tipo de trabajo delegado que `agents-os-agent-project-workflow` está diseñado para sostener (retomable por cualquier agente si se corta la sesión).

## Hallazgo adicional durante el refactor

- El Tablero final (`## 📋 Tablero`) de `AGENTS OS.md` no tenía el filtro `tags do not include #owner/agent` que sí tienen otros proyectos humanos (ej. `[[Echo Forge]]`). Esto ya era una inconsistencia latente, y se volvió operativamente relevante ahora porque `path includes AGENTS OS` empieza a matchear también la nueva subcarpeta `10-projects/AGENTS OS/agentes/`. Se agregó el filtro a las 4 queries del Tablero.

## Resolución aplicada

- Creado `10-projects/AGENTS OS/agentes/AGENTS OS - Beta y Hardening.md`: `owner: agent`, `root: false`, `parent: "[[AGENTS OS]]"`, con Fase 5 completa + ítem pendiente de Fase 6 como su `## ✅ Tareas`, siguiendo el template usado por `[[Echo Forge - Etapa 4]]`.
- En `AGENTS OS.md`: se reemplazaron los checklists abiertos migrados (Fase 5 y el ítem de watcher de Fase 6) por notas de redirección (sin checkbox, para que dejen de contarse como tareas del archivo padre); se sembró la tarea puente `- [ ] [[AGENTS OS - Beta y Hardening]] arrancar + seguimiento (proyecto de agente) #owner/me #type/supervision #area/personal`; se agregó `tags do not include #owner/agent` al Tablero final; se agregó entrada de Bitácora documentando la migración.
- En `project-ownership-human-vs-agent.md`: se actualizó la sección Consecuencias marcando la deuda como resuelta, con referencia a este log.
- Las Fases 0-4 y los ítems ya cerrados de Fase 6 se dejaron intactos en `AGENTS OS.md` como historial de diseño, incluyendo sus tags `#owner/agent` originales (no se retag-earon retroactivamente por ser cierre histórico, no ejecución activa).

## Judgment calls

- Se asumió que "ejecución activa" (candidata a migrar) = tareas no cerradas (`[ ]`), y que tareas `[x]` dentro de un roadmap ya cerrado no requieren retroactivamente vivir en un proyecto de agente ni tener tarea puente, porque la regla de ownership existe para gobernar dashboards de trabajo en curso, no para reescribir historial ya completado. Si el usuario prefiere pureza total del modelo (toda tarea `#owner/agent`, cerrada o no, debe vivir dentro de un proyecto de agente), este historial debería migrarse también — queda como ajuste pendiente si se pide explícitamente.
- No se movió el archivo `10-projects/AGENTS OS.md` a una estructura de carpeta (`10-projects/AGENTS OS/AGENTS OS.md`, como `[[Echo Forge]]`) porque no es necesario para cumplir la regla: la ruta objetivo pedida (`10-projects/AGENTS OS/agentes/`) puede coexistir en el filesystem con el archivo plano `AGENTS OS.md` sin conflicto de nombres, evitando un rename de la entidad canónica y de sus muchas referencias.

## Fuentes usadas

- `10-projects/AGENTS OS.md` (estado previo a la migración).
- `80-agents/memory/public/decision/agents-os/project-ownership-human-vs-agent.md`.
- `80-agents/skills/agents-os-agent-project-workflow/SKILL.md`.
- `80-agents/skills/agents-os-vault-refactor/SKILL.md`.
- `90-system/convenciones.md` (sección Proyectos humanos vs proyectos de agente).
- `10-projects/Echo Forge/Echo Forge.md` y `10-projects/Echo Forge/agentes/Echo Forge - Etapa 4.md` como referencia de patrón ya validado en el vault.

## Validación

- Archivos creados desde el patrón de proyecto de agente ya usado (Echo Forge), no desde un template `70-templates/` de tipo `project` dedicado — no se encontró uno distinto al patrón existente; si aparece un template formal de `project` en `70-templates/`, reconciliar en una próxima sesión.
- Pendiente: reindexar Graphify y validar que `[[AGENTS OS - Beta y Hardening]]` sea recuperable como entidad propia, y que `[[AGENTS OS]]` siga recuperable sin ruido.
