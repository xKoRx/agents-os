---
type: change_log
scope: session
created: 2026-06-30
updated: 2026-06-30
area: "[[Personal]]"
project: "[[AGENTS OS]]"
entities:
  - "[[AGENTS OS]]"
related: []
aliases: []
confidence: verified
source_session: 368404ab-3fb1-430d-890b-818e5b654c67
load_policy: manual
indexable: false
index_priority: never
tags:
  - area/personal
  - kind/changelog
  - project/agents-os
  - project/agentsos
  - scope/session
---
# 2026-06-30 Hermes Obsidian Tagging Rules Change Log

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - [hermes_obsidian_livesync_troubleshooting.md](file:///Users/rjara/obsidian/SecondBrain/main/30-resources/runbooks/hermes_obsidian_livesync_troubleshooting.md) (updated)
  - [SKILL.md](file:///Users/rjara/obsidian/SecondBrain/main/80-agents/skills/agents-os-tagging-system/SKILL.md) (updated)

## Motivo

- Clasificar correctamente el runbook de Hermes y Obsidian LiveSync de acuerdo con el Tag Contract del Second Brain.
- Fortalecer la skill canónica `agents-os-tagging-system` para cubrir de manera integrada y robusta la taxonomía de tags de notas y de tareas.

## Fuentes usadas

- `90-system/convenciones.md`
- `80-agents/skills/_shared/metadata-schema.md`

## Resolución aplicada

- **Runbook:** Se insertó el bloque de YAML frontmatter con tags normalizados (`kind/runbook`, `scope/service`, `area/personal`, `tech/obsidian`, `tech/couchdb`, `tech/linux`, `tool/hermes`) y campos de ruteo adecuados (`type`, `scope`, `area`, `confidence`, `load_policy`, `indexable`, `index_priority`).
- **Skill:** Se reescribió `agents-os-tagging-system/SKILL.md` definiendo un sistema de namespaces ordenados y coherentes para las notas del vault y estandarizando las reglas generales de taggeo.

## Validación

- Se corrió `graphify-obsidian update` de manera exitosa para reindexar el vault.
