---
type: change_log
schema_version: 1
scope: session
created: "2026-08-16"
updated: "2026-08-16"
area:
project:
application:
entities:
  - "[[Echo — Workspace Go de repositorios]]"
  - "[[Fuentes — Workspace de repositorios]]"
related: []
aliases: []
confidence: verified
source_session:
source_feedbacks:
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# Workspaces de repos — separación Echo (`~/go`) vs Meli (`~/fuentes`)

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** created + updated
- **Archivo(s):**
  - `30-resources/storage/echo-go-workspace.md` (creada vía `materialize_schema_note.py`, tipo `storage`)
  - `30-resources/storage/fuentes-workspace.md`
  - `80-agents/agents-os/agent-constitution.md` (regla 12)

## Motivo

- La regla 12 de la constitución presentaba `~/fuentes` como workspace único de clones, pero ese workspace es Meli/RIO (`rio-*`). Los repos del ecosistema Echo Forge (`symphony`, `sdk`, `stager`, `echo`, `mde`, `api-core`, `api-persist`) viven en `~/go/src/github.com/xKoRx`. Un agente siguió la regla literal y buscó el repo Echo en `~/fuentes`; la corrección del owner confirmó el split.

## Resolución aplicada

- Nueva nota canónica [[Echo — Workspace Go de repositorios]] documenta `~/go/src/github.com/xKoRx`, con nombres del remote y reglas de uso.
- [[Fuentes — Workspace de repositorios]] queda explícitamente scoped a repos Meli/RIO y enlaza al workspace Echo.
- Regla 12 de la constitución ahora refiere ambos workspaces por familia de repos; el resto del texto (nada de clones bajo `VAULT_ROOT`, notas solo con repo + path relativo) no cambia.
