---
type: source
schema_version: 1
status: active
area: "[[Meli]]"
source_url: https://github.com/melisource/fury_ads-signals-skills-marketplace
repo: ads-signals-skills-marketplace
path: .
author: Mercado Libre / melisource
published:
captured: "2026-09-01"
license: MIT
checksum:
supersedes:
superseded_by:
aliases:
  - ads-signals-skills-marketplace repo
  - fuente ads-signals-skills-marketplace
tags:
  - kind/source
created: "2026-09-01"
updated: "2026-09-01"
---

# ads-signals-skills-marketplace-source

## Referencia

- **Origen resoluble:** repo `ads-signals-skills-marketplace`, path `.`, relativo a [[Fuentes — Workspace de repositorios]]; remoto upstream `https://github.com/melisource/fury_ads-signals-skills-marketplace`.
- **Fecha de captura:** 2026-09-01; branch `feature/human-first-technical-writing`, commit `d1515df`, basada en `master@ac72fb7`.

## Alcance

- README y contrato de contribución, catálogo `catalog/skills.json`, validador local, licencia y las tres skills presentes en el branch verificado.
- La captura incluye el cambio que agrega `human-first-technical-writing` v1.0.0 y eleva el catálogo a v1.2.0; el cambio está propuesto en `melisource/fury_ads-signals-skills-marketplace#1` y aún no forma parte de `master`.

## Notas de provenance

- `node scripts/validate-marketplace.mjs` reportó `Marketplace válido: 3 skill(s) revisada(s).` y `git diff --check` pasó sin errores.
- La skill nueva declara compatibilidad con Claude y Codex, sin permisos y con runtime `none`; no agrega scripts, conectores, variables de entorno ni recursos generados.
- El check remoto `Code Reviewer` terminó en `SUCCESS`; la revisión automática no encontró issues y aprobó el PR como low-risk.
- La página canónica [[ads-signals-skills-marketplace]] describe el contrato estable del repo. La presencia de la skill nueva y el número de versión del catálogo son estado de branch hasta que el PR sea mergeado.

## Lifecycle

- **Supersedes:** —
- **Superseded by:** —
