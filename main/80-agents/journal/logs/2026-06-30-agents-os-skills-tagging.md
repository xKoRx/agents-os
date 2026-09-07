---
type: change_log
scope: session
created: "2026-06-30"
updated: "2026-06-30"
area: "[[Personal]]"
project: "[[AGENTS OS]]"
application:
entities:
  - "[[AGENTS OS]]"
related: []
aliases: []
confidence: verified
source_session: "54d8c0b6-cc0b-4ea4-a93a-8968ff47d026"
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# Change Log - 2026-06-30 - Tagging and Indexing of AGENTS OS Skills

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - [agents-os.md](file:///Users/rjara/obsidian/SecondBrain/main/80-agents/agents-os/agents-os.md)
  - [INDEX.md](file:///Users/rjara/obsidian/SecondBrain/main/80-agents/skills/INDEX.md)
  - 18 archivos `SKILL.md` bajo `80-agents/skills/`
  - [agents-os-tagging-system/SKILL.md](file:///Users/rjara/obsidian/SecondBrain/main/80-agents/skills/agents-os-tagging-system/SKILL.md)
  - [_shared/skill-contract.md](file:///Users/rjara/obsidian/SecondBrain/main/80-agents/skills/_shared/skill-contract.md)
  - [skill.md](file:///Users/rjara/obsidian/SecondBrain/main/80-agents/templates/skill.md)

## Motivo

- Habilitar el descubrimiento semántico y la carga dinámica de habilidades especializadas por parte de agentes basados en Graphify.
- Eliminar el aislamiento (nodos huérfanos) de las notas de skills en el grafo.
- Formalizar las reglas core del bucle operativo para regular la carga de estas skills y prevenir que se vuelvan a crear sin tags en el futuro.

## Fuentes usadas

- [[agents-os]]
- [[INDEX]] (skills)
- [[skill-contract]]

## Resolución aplicada

- **agents-os.md**: Añadida la sección `Carga Dinámica de Skills (Habilidades)` que clasifica las skills en Core (siempre cargadas) y Especializadas (cargadas dinámicamente si Graphify las reporta) y establece la obligatoriedad del `view_file`.
- **INDEX.md**: Modificada la tabla para usar wikilinks de Obsidian apuntando directamente a cada `SKILL.md`. Agregada la skill `operational-healthcheck-policy` al índice.
- **SKILL.md (18 archivos)**: Agregados tags YAML consistentes en el frontmatter (`kind/skill`, `tech/agents-os` y tags específicos de acción/dominio).
- **agents-os-tagging-system/SKILL.md**: Añadido el tipo de nota `kind/skill` en los metadatos permitidos.
- **_shared/skill-contract.md**: Actualizado el checklist de preparación para exigir el tagueo estándar.
- **skill.md**: Creada la plantilla oficial para nuevas skills con tags y estructura YAML preconfigurada.

## Validación

- Se ejecutó `graphify-obsidian update`.
- Se validaron consultas con `graphify-obsidian query` verificando la resolución de aristas de relación desde el catálogo hacia las skills y la recuperación de nodos al consultar tags.
