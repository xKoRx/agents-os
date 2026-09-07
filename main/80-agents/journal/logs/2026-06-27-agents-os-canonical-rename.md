---
type: change_log
scope: project
created: 2026-06-27
updated: 2026-06-27
area:
  - "[[Personal]]"
project:
  - "[[AGENTS OS]]"
application:
entities:
  - "[[AGENTS OS]]"
related:
  - "[[agents-os]]"
  - "[[agents-os-bootstrap]]"
aliases:
  - AGENTS OS canonical rename
confidence: verified
source_session:
load_policy: manual
indexable: false
index_priority: never
tags:
  - area/personal
  - kind/changelog
  - project/agents-os
  - project/agentsos
  - scope/project
---
# 2026-06-27 AGENTS OS Canonical Rename

## Cambio

- **Tipo:** updated / renamed
- **Archivo(s):**
  - `10-projects/AGENTS OS.md`
  - `80-agents/agents-os/agents-os.md`
  - `80-agents/skills/agents-os-*/SKILL.md`
  - `80-agents/memory/public/**/agents-os/`
  - `80-agents/memory/internal/agent-memory/global/agents-os-operating-continuity.md`
  - `80-agents/journal/**`
  - `40-archive/agents-os-drafts/`
  - `.obsidian/plugins/task-board/tasks.json`
  - `.obsidian/workspace.json`
  - `.graphifyignore`
  - `README.md`

## Motivo

- El nombre canónico correcto del sistema es `AGENTS OS`.
- El usuario pidió aplicar el cambio de forma masiva en todo el Second Brain y cerrar sesión.

## Fuentes usadas

- Solicitud explícita del usuario en la sesión actual.
- `agents-os-bootstrap` como skill de arranque del sistema.
- Guía operativa, constitución, perfil de usuario y memoria interna always-load.

## Resolución aplicada

- Se renombró el proyecto, la guía operativa, skills, paths de memoria, journal, drafts archivados y metadata de Obsidian para usar `agents-os` / `AGENTS OS`.
- Se actualizaron referencias, tags, aliases, links y paths relacionados.
- Se agregó línea de progreso a las skills canónicas indicando el rename.

## Validación

- `rg -uu` sobre el vault fuente, excluyendo `.git` y `95-graphify`, no encuentra el identificador anterior.
- `find` sobre paths fuente, excluyendo `.git` y `95-graphify`, no encuentra rutas con el identificador anterior.
- `graphify-obsidian update` completó después del rename: 715 nodos, 632 edges, 83 comunidades.
- Se corrigió una referencia remanente en `95-graphify/README.md`.
- `rg -uu` sobre todo el workspace, excluyendo solo `.git`, no encuentra el identificador anterior.
- `graphify-obsidian explain "AGENTS OS"` resuelve a `10-projects/AGENTS OS.md`.
- `graphify-obsidian query "agents-os-bootstrap Agent Memory System Startup Invocation System Prompt Contract" --budget 1400` recupera `agents-os-bootstrap - Agent Memory System Startup`, `Invocation` y `System Prompt Contract`.
- `rg` por los filenames de cierre en `95-graphify/obsidian/graph.json` no devuelve resultados, validando que journal/raw/session siguen fuera del grafo normal.
