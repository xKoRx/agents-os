---
type: change_log
scope: session
created: 2026-07-01
updated: 2026-07-01
area: "[[Personal]]"
project: "[[AGENTS OS]]"
entities:
  - "[[AGENTS OS]]"
  - "[[convenciones]]"
  - "[[Destaques de Precio]]"
  - "[[Bajó de Precio]]"
  - "[[Echo Forge]]"
related:
  - "[[Panel de Proyectos]]"
  - "[[Search Middleware - Correccion Bajo de Precio Motors]]"
  - "[[echo-forge-wfm-troubleshooting]]"
aliases: []
confidence: verified
source_session:
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
  - project/agentsos
  - change/updated
---

# Sistema de ownership de proyectos: humano vs agente + tarea puente

## Cambio

- **Tipo:** updated / created
- **Archivo(s):**
  - `70-templates/project.md` — frontmatter `owner: me` + `root: false`; callout de ownership y tarea puente.
  - `70-templates/task.md` — ejemplo de tarea puente `#type/supervision`.
  - `70-templates/dashboard.md` — template nuevo (faltaba, requerido por política Sistema 2).
  - `90-system/convenciones.md` — tipo `#type/supervision`; secciones "Ownership humano vs agente", "Proyectos humanos vs proyectos de agente", "Regla anti-huérfano".
  - `80-agents/agents-os/agents-os.md` — regla de creación de proyectos de agente (owner, parent, carpeta `agentes/`, tarea puente).
  - `90-system/Panel de Proyectos.md` — dashboard nuevo (cockpit de supervisión, agente/humano, huérfanos, sin owner).
  - `00-inbox/Home.md` — enlace a [[Panel de Proyectos]].
  - Frontmatter `owner`/`root` en: Destaques de Precio (me/root), Bajó de Precio (me), Automatización despliegue FURY (me/root), Corrección masiva de tags (me/root), Refactor Polycard (me/root), AGENTS OS (me/root), Echo Forge (me/root).
  - `owner: agent` + movimiento a `agentes/`: Search Middleware → `Destaques de Precio/agentes/`; echo-forge-wfm-troubleshooting → `Echo Forge/agentes/`.
  - Tareas puente sembradas: `[[Search Middleware…]]` en Bajó de Precio (`[/]`); `[[echo-forge-wfm-troubleshooting]]` en Echo Forge (`[x]`).

## Motivo

- El usuario mezclaba proyectos/tareas propios con los de agentes sin un sistema, y sus listas humanas se contaminaban con tareas de agente. Un proyecto nuevo quedó sin enlace a padre por falta de una regla que lo obligara.

## Fuentes usadas

- `agents-os.md`, `agent-constitution.md`, `rjara-agent-profile.md`, `convenciones.md`, `_shared/metadata-schema.md`, `_shared/note-types.md`, skill `agents-os-vault-refactor`.
- Estado real de proyectos en `10-projects/`.

## Resolución aplicada

- Dos ejes de ownership: proyecto (`owner: me|agent`) y tarea (`#owner/me|agent`, ya existente).
- **Tarea puente**: un proyecto de agente se representa en el padre humano con UNA tarea `#owner/me #type/supervision`; las tareas finas del agente viven dentro del proyecto de agente.
- Proyectos de agente en subcarpeta `agentes/` de la iniciativa; los links `[[...]]` (por nombre) no se rompen al mover.
- Regla anti-huérfano: subproyectos con `parent`; raíces con `root: true`; huérfanos y sin-owner se cazan en el dashboard.
- Decisiones del usuario: separación frontmatter + carpetas; tag `#type/supervision`; ejecutar barrido completo.

## Validación

- Editada la frontmatter de 9 proyectos + 2 movimientos + 2 tareas puente sin romper links por nombre.
- Vistas del dashboard usan filtros `base` consistentes con Home (`type == "project"`, `!note.parent`, `note.owner`).
- Pendiente: reindex Graphify y validar query enfocada.

## Seguimiento diferido

- Clasificar `owner` de los archivos de etapa de Echo Forge (Etapas 1-3/5-7/8-10, Etapa 4); hoy aparecen en "Sin owner" del dashboard.
- Confirmar clasificación `owner: agent` de echo-forge-wfm-troubleshooting (inferida, no marcada por el usuario).
