---
type: change_log
schema_version: 1
scope: session
created: "2026-09-17"
updated: "2026-09-17"
area: "[[Meli]]"
project: "[[Vulnerabilidades WebSec — RIO Foundation]]"
application:
entities:
  - "[[RIO]]"
  - "[[ads-signals-skills-marketplace]]"
related:
  - "[[rio-sunset-update]]"
  - "[[meli-agent-dev]]"
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
  - area/meli
  - action/skill-authoring
---

# 2026-09-17-rio-sunset-update-skill-import

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** created + updated
- **Archivo(s):**
  - `30-resources/agents/skills/rio-sunset-update/` — skill canónica, referencias y gates ejecutables.
  - `30-resources/agents/skills/meli-agent-dev/SKILL.md` — routing de sunsets RIO.
  - `30-resources/tools/ads-signals-skills-marketplace.md` — link a la adaptación canónica.
  - `30-resources/tools/sources/ads-signals-skills-marketplace-source.md` — provenance de la propuesta y evidencia de validación.

## Motivo

- Incorporar al vault la skill propuesta por `feat/rio-sunset-update` para ejecutar remediaciones manuales de sunsets RIO con gates fail-closed y dejarla disponible desde el router Meli.

## Fuentes usadas

- Repo `ads-signals-skills-marketplace`, ref local `origin/pr/2@a7872cd`, correspondiente a la propuesta `feat/rio-sunset-update`.
- Contratos `80-agents/skills/_shared/skill-contract.md`, `80-agents/skills/_shared/note-types.md` y runbook `80-agents/memory/public/runbook/agents-os-skill-authoring.md`.

## Resolución aplicada

- Se materializó la skill bajo el contrato S1, se importaron referencias y scripts, se adaptó el frontmatter portable al schema del vault y se agregó el handoff en `meli-agent-dev`.
- Se corrigió una contradicción de la propuesta: el workflow declaraba Fury CLI fuera del contrato mientras la revisión más reciente exige `fury create-version`; la versión canónica la declara capacidad obligatoria desde el preflight.

## Validación

- Marketplace upstream: `Marketplace válido: 3 skill(s) revisada(s).`; `git diff --check` verde.
- Gates importados: `validate-input.test.mjs` y `validate-gates.test.mjs` verdes.
- Draft→Ready: schema/frontmatter, secciones requeridas, routing y activaciones validados por los checks del vault registrados al cierre de esta operación.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Eliminar `30-resources/agents/skills/rio-sunset-update/`, retirar su fila de `meli-agent-dev` y revertir los enlaces/provenance agregados en las páginas del marketplace.
