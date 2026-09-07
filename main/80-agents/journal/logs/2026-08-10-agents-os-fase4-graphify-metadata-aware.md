---
type: change_log
schema_version: 1
scope: session
created: "2026-08-10"
updated: "2026-08-10"
area: "[[Personal]]"
project: "[[AGENTS OS - Fase 3]]"
application:
entities:
  - "[[AGENTS OS]]"
  - "[[graphify]]"
related:
  - "[[graphify-frontmatter-alias-and-typed-edge-dedup-gaps]]"
  - "[[graphify-obsidian-install]]"
aliases:
  - AGENTS OS F4 Graphify metadata-aware change log
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

# 2026-08-10-agents-os-fase4-graphify-metadata-aware

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** created / updated
- **Archivo(s):** `/Users/rjara/fuentes/graphify/{graphify,tests,pyproject.toml}`, `.graphifyignore`, `95-graphify/dist/`, `95-graphify/obsidian/`, `80-agents/memory/public/{known-error,runbook}/`, [[AGENTS OS - Fase 3]] y [[AGENTS OS]].

## Motivo

- Ejecutar todos los T4.* de Fase 4 para que Graphify consuma metadata confiable sin convertirse en autoridad ni romper las operaciones existentes.

## Fuentes usadas

- [[AGENTS OS - Fase 3]], `80-agents/skills/_shared/schema-contract.md`, fixtures contractuales, `.graphifyignore`, suite upstream del fork y baseline rollback `graphifyy 0.9.6`.

## Resolución aplicada

- Se implementó parser fail-closed, proyección allowlisted en file nodes, facets exactos, siete relaciones de frontmatter, filtros CLI, resolución compartida de aliases, deduplicación relation-aware con precedencia tipada, exclusión única y serialización GraphML compatible.
- Se construyó/instaló `graphifyy 0.9.6.post1`, se conservó el wheel 0.9.6 como rollback, se actualizó el wrapper para consultas de versión sin reindex y se reconstruyó el índice final.

## Validación

- Suite completa con `GIT_CONFIG_GLOBAL=/dev/null`: `2840 passed, 28 skipped`; Ruff verde; lint gate `ERROR=94 WARN=81 new=0`.
- E2E: alias/filter/query/explain/path/affected verdes; `359` file nodes proyectados, 15 dimensiones facet, `689` edges tipados, `0` tag-nodes y `0` ignored paths.
- Comparación rollback sobre el mismo corpus: 0.9.6=`4984/5889/497`, `12.60 s`, `4,634,091 bytes`; 0.9.6.post1=`4984/5893/493`, `15.93 s`, `5,308,347 bytes`.
- Refresh posterior a los registros canónicos: `4985` nodos y `5894` edges; las comunidades no se usan como gate porque su partición varía entre reconstrucciones equivalentes.
- Wheel final SHA-256 `ecdb3e67c4d3a31153ddb38b08c15c106c102844ce88503c99e23bd3971225d1`; snapshot fuente SHA-256 `39c2061b3446a65666e5734dc5d65bb0ac33aa933303d2237356f41da1d11b90`.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin secretos; conserva paths locales sólo porque documenta un fork y artefacto instalados en esta máquina.

## Rollback

- Reinstalar `95-graphify/dist/graphifyy-0.9.6-py3-none-any.whl` con `--reinstall --no-deps`, restaurar el wrapper previo si fuera necesario y ejecutar `graphify-obsidian update`; Markdown canónico no depende del índice derivado.
