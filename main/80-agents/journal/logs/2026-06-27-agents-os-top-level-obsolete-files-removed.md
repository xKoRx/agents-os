---
type: change_log
scope: project
created: "2026-06-27"
updated: "2026-06-27"
area: "[[Personal]]"
project: "[[AGENTS OS]]"
application:
entities:
  - "[[AGENTS OS]]"
related:
  - "[[agents-os]]"
aliases:
  - AGENTS OS obsolete top-level files removed
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
  - tech/agentsos
---
# 2026-06-27 AGENTS OS Top-Level Obsolete Files Removed

## Cambio

- **Tipo:** deleted / updated
- **Archivo(s):**
  - `80-agents/AGENTS.md`
  - `80-agents/LLM Wiki.md`
  - `80-agents/skills/_shared/skill-contract.md`
  - `80-agents/skills/agents-os-bootstrap/SKILL.md`
  - `README.md`

## Motivo

- Tras consolidar `80-agents/agents-os/agents-os.md` como guía operativa única, `80-agents/AGENTS.md` y `80-agents/LLM Wiki.md` quedaban como top-level obsoleto y podían confundir a futuros agentes.
- El `README.md` todavía mencionaba carpetas no existentes (`50-monitors`, `60-actions`) y describía `80-agents/` como dependiente de `AGENTS.md`.

## Fuentes usadas

- Inventario de `80-agents/`.
- Búsqueda de referencias activas a `AGENTS.md`, `LLM Wiki`, `50-monitors`, `60-actions` y `40-decisions`.

## Resolución aplicada

- Se eliminaron `80-agents/AGENTS.md` y `80-agents/LLM Wiki.md`.
- Se actualizaron reglas de bootstrap/skill contract para no apuntar a `AGENTS.md`.
- Se actualizó el mapa principal del vault para reflejar la estructura real.

## Validación

- `find 80-agents -maxdepth 2 -type f` ya no muestra archivos top-level obsoletos.
- `rg 'AGENTS\.md|LLM Wiki|50-monitors|60-actions|40-decisions' README.md 10-projects/AGENTS\ SO.md 80-agents .graphifyignore` no devuelve referencias operativas; solo queda una entrada histórica en el progress log de `agents-os-bootstrap`.
- `graphify-obsidian update` ejecutado tras la eliminación: 739 nodes, 652 edges, 87 communities.
- `rg '80-agents/AGENTS\.md|80-agents/LLM Wiki\.md|40-archive|agents-os-drafts|AGENTS\.md|LLM Wiki' 95-graphify/obsidian/graph.json` no encontró fuentes obsoletas ni archivadas en el grafo vivo.
- `graphify-obsidian query 'AGENTS OS guía operativa bootstrap retrieval session close' --budget 1200` recuperó `80-agents/agents-os/agents-os.md`.
