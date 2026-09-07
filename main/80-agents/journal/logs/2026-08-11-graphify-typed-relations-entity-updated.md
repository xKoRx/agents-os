---
type: change_log
schema_version: 1
scope: session
created: "2026-08-11"
updated: "2026-08-11"
area: "[[Personal]]"
project: "[[AGENTS OS - Relaciones Tipadas de Graphify]]"
application:
entities:
  - "[[AGENTS OS]]"
  - "[[graphify]]"
related:
  - "[[graphify-frontmatter-alias-and-typed-edge-dedup-gaps]]"
  - "[[graphify-obsidian-install]]"
aliases: []
confidence: verified
source_session:
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# Graphify typed relations — entity updated

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** created / updated
- **Archivo(s):** `10-projects/Personal/AGENTS OS/AGENTS OS.md`; `10-projects/Personal/AGENTS OS/agentes/AGENTS OS - Relaciones Tipadas de Graphify.md`; `30-resources/tools/graphify.md`; `30-resources/tools/00-index.md`; `30-resources/tools/log.md`; `80-agents/memory/public/known-error/agents-os/graphify-frontmatter-alias-and-typed-edge-dedup-gaps.md`; `80-agents/memory/public/runbook/graphify-obsidian-install.md`; `80-agents/skills/agents-os-context-retrieval/scripts/context_router_e2e.py`; `95-graphify/dist/BUILD.md`; `95-graphify/dist/README.md`; `95-graphify/dist/graphifyy-0.9.6.post2-py3-none-any.whl`; repo `graphify` en su rama `feat/obsidian-vault-wikilinks`.

## Motivo

- Graphify `0.9.6.post1` perdía una relación tipada cuando dos campos de frontmatter apuntaban al mismo target. El cambio actualiza la verdad vigente desde “gap mitigado por higiene de fuente” a “resuelto por representación lossless compatible en `0.9.6.post2`”.

## Fuentes usadas

- Reproducción mínima sobre el repo `graphify`: extracción `references + child_of + related_to`; build anterior `related_to` solamente.
- Código y tests del repo `graphify`; ejecución de suite completa, Ruff, build de wheel, instalación aislada, gate del vault, reindex y Context Router E2E.
- [[graphify-frontmatter-alias-and-typed-edge-dedup-gaps]], [[graphify-contract]] y [[AGENTS OS - Fase 3]].

## Resolución aplicada

- `relation` conserva el escalar legacy y `relations` registra la lista ordenada y deduplicada de variantes semánticas del par. `affected` filtra ambas representaciones; `path`, `explain` y MCP muestran el conjunto. Se creó y completó [[AGENTS OS - Relaciones Tipadas de Graphify]], se actualizó la entidad [[graphify]], su índice/log de Resource Wiki, el runbook, el known error y el cockpit [[AGENTS OS]]. El owner aceptó la entrega y cerró la tarea puente.

## Validación

- Suite focalizada `74 passed`; suite completa aislada de `core.hooksPath` global `2844 passed, 28 skipped`; Ruff verde; grafo de código `10415/17579`; wheel `0.9.6.post2` SHA-256 `fd36205f41f9d9455c67f40cca1d191e1662b7c6f7146a9aebe23e56c57dc4a8`; instalación verificada; lint/gate vault `0 ERROR / 0 WARN`; reindex final de cierre `5138 nodes / 6134 edges`; Context Router `14/14`, 0 misses y precisión proxy 100%.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin secretos, memoria interna ni paths absolutos persistidos.

## Rollback

- Reinstalar `95-graphify/dist/graphifyy-0.9.6.post1-py3-none-any.whl` con `--reinstall --no-deps` y ejecutar `graphify-obsidian update`; el índice es derivado y Markdown permanece intacto.
