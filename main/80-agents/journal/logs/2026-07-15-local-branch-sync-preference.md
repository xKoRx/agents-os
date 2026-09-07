---
type: change_log
scope: user
created: 2026-07-15
updated: 2026-07-15
share_scope: local
project: "[[AGENTS OS]]"
entities:
  - "[[AGENTS OS]]"
related:
  - "[[sync-local-branch]]"
aliases: []
confidence: verified
source_session:
source_feedbacks: []
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/user
  - project/agentsos
  - change/created
---

# Preferencia de sincronización Git local

## Cambio

- Se agregó al perfil always-load la preferencia de operar sincronizaciones Git exclusivamente con ramas locales.
- Se estableció como bloqueo la ausencia de una rama local, un working tree sucio o una resolución ambigua.

## Motivo

- Preservar los commits y la funcionalidad de la rama objetivo y de la rama base sin operaciones remotas o destructivas no autorizadas.

## Validación

- La preferencia quedó respaldada por la skill canónica `80-agents/skills/sync-local-branch/SKILL.md`.
- En la tarea de origen, `feature/new-title-motors` existe localmente y `develop` no existe localmente; por eso no se ejecutó el merge.
