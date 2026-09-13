---
type: change_log
schema_version: 1
scope: session
created: "2026-09-12"
updated: "2026-09-12"
area: "[[Personal]]"
project: "[[AGENTS OS]]"
application:
entities:
  - "[[AGENTS OS]]"
  - "[[Aranea]]"
related:
  - "[[30-resources/runbooks/00-index]]"
  - "[[2026-09-12-agents-os-skills-restructure]]"
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

# 2026-09-12-agents-os-runbooks-restructure

%% Routing: area/project/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated + created
- **Archivo(s):**
  - `git mv` desde `80-agents/memory/public/runbook/` a `30-resources/runbooks/`: `aranea-ssh-mcp.md`, `aranea-postgres-mcp.md`, `aranea-mongodb-mcp.md`, `aranea-hasura-mcp.md`, `aranea-mcp-capability-plane.md`, `signals-code-review-runbook.md`, `signals-code-review.md`, `resolver-versiones-java-sin-construir-via-fury-nexus.md`, `stager-windows-mt5-cutover-and-occupieddrain.md`, `2026-07-25-fix-pack-for-gate-handoff-review.md` y la subcarpeta `symphony/` (8 runbooks).
  - `30-resources/runbooks/signals-code-review.md` — marcado `status: superseded` con `superseded_by: [[signals-code-review-runbook]]` (variante anterior del mismo día con los mismos aliases; la canónica es la versión con gate Meli y `rjara-rio-impact`).
  - `30-resources/runbooks/00-index.md` + `log.md` — dominio wiki activado explícitamente con catálogo de 15 runbooks + subcarpeta symphony.
  - `30-resources/agents/skills/aranea-mcps-expert/SKILL.md` — paths de runbooks actualizados a `30-resources/runbooks/`.
  - `30-resources/agents/skills/signals-code-review/SKILL.md` — refs al runbook a `../../runbooks/signals-code-review-runbook.md`.
  - `30-resources/aranea/02-servicios/ml-ia.md`, `30-resources/agents/00-index.md` — paths actualizados.
  - `30-resources/00-RESOURCE-WIKI.md` — lista de dominios activos incorpora `runbooks/`.

## Motivo

- El usuario pidió replicar la restructura de skills en los runbooks: los de AGENTS OS quedan en `80-agents/memory/public/runbook/`; los de dominios y aplicaciones van a `30-resources/runbooks/`.

## Fuentes usadas

- Frontmatter (`entities`) de cada runbook para clasificar; diff de las dos variantes `signals-code-review*` para resolver el duplicado; `30-resources/00-RESOURCE-WIKI.md` para el contrato de dominio.

## Resolución aplicada

- Quedaron en `80-agents/memory/public/runbook/` sólo: `agents-os-skill-authoring.md`, `delegacion-a-subagentes.md`, `graphify-obsidian-install.md`, `reindex-bloqueado-por-deuda-global.md`, `resource-wiki-lint-reindex.md`.
- `runbooks/` se promovió a dominio activo por decisión explícita del usuario (el contrato exige que la promoción no sea implícita; ésta fue dirigida).

## Validación

- Barrida de referencias: `grep memory/public/runbook/<movidos>` da 0 matches fuera de journal, `.trash`, `core-export` y la entrada histórica del `log.md` de `agents/` (evidencia histórica, no se reescribe).
- `doctor.py --strict`: HIGH=0 MEDIUM=0 LOW=0.

## Compartibilidad

- **Scope:** local / team
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- `git revert` del commit, o `git mv` inverso de los archivos + restaurar `00-index.md`/`log.md` de runbooks y las refs desde el commit previo.
