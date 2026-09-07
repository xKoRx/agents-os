---
type: change_log
schema_version: 1
scope: session
created: "2026-08-24"
updated: "2026-08-24"
area:
project: "[[Crear Context]]"
application:
entities:
  - "[[Crear Context]]"
  - "[[Onboarding Signals]]"
related: []
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

# 2026-08-24-signals-spec-skills-split-and-context-spec-rewrite

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** created / updated / deleted
- **Archivo(s):**
  - `80-agents/skills/signals-func-spec-authoring/` — **renombrado** desde `signals-spec-authoring`; incorpora la versión rica que vivía sólo en el cliente, más `§0` (atemporalidad + creación vía Grimoire) y el workflow reescrito.
  - `80-agents/skills/signals-func-spec-authoring/references/que-es-una-spec.md` — **nuevo**; regla canónica compartida por las dos skills de specs.
  - `80-agents/skills/signals-tech-spec-authoring/` — **nuevo**; SKILL.md + `references/failure-modes.md`.
  - `80-agents/skills/signals-spec-authoring/` — **eliminado** (reemplazado por el nombre alineado).
  - `80-agents/skills/INDEX.md` — fila reemplazada por las dos nuevas.
  - `30-resources/runbooks/Signals - Escribir specs funcionales (SIG).md` — enlaces al nombre nuevo.

## Motivo

Los dos artefactos de autoría de specs tenían nombres desalineados (`signals-spec-authoring` vs `signals-tech-spec-authoring`) y la skill funcional había **driftado**: 6.5k en el vault contra 13k en el cliente. Además no existía canon para la spec **técnica**, y el hueco se notó al corregir SIG-590.

## Fuentes usadas

- Las **33 specs técnicas reales** del proyecto SIG en Spellbook (fecaputo, vmilesi, frsalazar, wvenera, dochoa, eolopes, dilimaa, jupereira). De ahí salen `DD-N`, el diagrama con marcadores de cambio, la mediana de ~10k caracteres y el criterio de anclaje por nombre de clase en vez de `archivo:línea`.
- `develop @ 0524ce49e` de `rio-playmaker` y `master @ 9d86eb8` de `rio-sdk-events` para verificar cada hecho citado.

## Resolución aplicada

- Canónicas en el vault; en `~/.claude/skills/` quedan **routers**, nunca copias — el patrón de [[pr-description]], adoptado justamente para no repetir el drift que motivó este cambio.
- La regla de atemporalidad vive en **una** fuente (`que-es-una-spec.md`) y las dos skills la referencian con un resumen de cinco líneas en el hot path.

## Validación

- Las dos skills quedan visibles y cargables por el cliente bajo los nombres nuevos.
- Referencias cruzadas al nombre viejo actualizadas en INDEX, runbooks y memoria del cliente. Los journals y logs históricos **no** se reescriben: son auditoría.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Restaurar `80-agents/skills/signals-spec-authoring/` desde el historial del vault y revertir la fila de `INDEX.md`. Los routers del cliente se borran solos al no tener canónica.
