---
type: change_log
schema_version: 1
scope: session
created: "2026-09-13"
updated: "2026-09-13"
area: "[[Echo]]"
project: "[[Echo — Knowledge Base Consolidation]]"
application:
entities:
  - "[[Echo — Knowledge Base Consolidation]]"
  - "[[echo-forge-integration-boundary]]"
related:
  - "[[AGENTS OS]]"
aliases: []
confidence: verified
source_session:
source_feedbacks:
  - "[[2026-09-13-echo-kbc-session-feedback]]"
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-09-13-kbc-hygiene-pass-context-budget

%% Routing: area/project/application/entities/related usan links canónicos. %%

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `80-agents/skills/INDEX.md` — registro app-owned corregido: 3 → 21 skills reales en `xKoRx/symphony/.agents/skills/` (defecto demostrado F5 de [[2026-09-13-echo-kbc-session-feedback|auditoría KBC-J]]), pointer al repo owner como descubrimiento primario, y fila nueva marcando la divergencia `aranea-mcps-expert` duplicada repo-side (canónica en `30-resources/agents/skills/`).
  - `30-resources/agents-os/core-export/dist-files/` — 6 notas con frontmatter marcadas `indexable: false` + `index_priority: never` (elimina la duplicación `load_policy: always` del perfil de usuario desde el índice; F1). Los 4 archivos sin frontmatter (AGENTS.md, CLAUDE.md, INSTALL-PROMPT.md, README.md) quedan intactos: son dist crudo, sin club always, mutarlos rompería el artefacto.
  - `10-projects/Echo Forge/Echo Forge.md` — 1 nota subordinada al principio "Frontera API-First" enlazando [[echo-forge-integration-boundary]] con el estado real (entrega vía API NO cableada; F7).

## Motivo

- Fase K (hygiene pass acotado KISS) de la campaña [[Echo — Knowledge Base Consolidation]], ejecutada desde los findings priorizados de la auditoría de context budget (`08-context-budget.md`, 9 findings). Regla aplicada: sólo defectos demostrados; sin rediseño de bootstrap, sin tocar skills/runbooks/contratos/memoria histórica.

## Fuentes usadas

- `10-projects/Echo/agentes/kb-consolidation/artifacts/08-context-budget.md` (findings F1/F5/F7/F2)

## Resolución aplicada

- KISS: 3 ediciones, todas metadata o 1 línea. Credenciales (F2/P0) NO tocadas — escaladas al owner (rotación fuera del alcance de la campaña documental).

## Validación

- `grep` post-edición: INDEX declara 21 y enlaza repo owner; dist profile no-indexable; link a boundary resuelve por nombre. Sin cambios en superficies de publicación de la campaña (subdominio `applications/echo/` intacto).

## Compartibilidad

- **Scope:** team
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos (la contraseña SSH NO se reproduce en este log; ver feedback y artifact 07 para la remediación)

## Rollback

- Revertir los 3 archivos (git); cambios independientes entre sí.
