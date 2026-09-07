---
type: known_error
schema_version: 1
scope: global
created: 2026-08-08
updated: 2026-08-11
area: "[[Personal]]"
project: "[[AGENTS OS - Relaciones Tipadas de Graphify]]"
application:
entities:
  - "[[AGENTS OS]]"
  - "[[graphify]]"
related:
  - "[[graphify-contract]]"
  - "[[agents-os-context-retrieval]]"
  - "[[AGENTS OS - Fase 3]]"
aliases:
  - Graphify alias explain gap
  - Graphify typed relation dedup gap
confidence: verified
source_session:
load_policy: when_error_matches
indexable: true
index_priority: high
tags:
  - kind/known-error
  - scope/global
  - project/agents-os
  - tech/graphify
  - action/retrieval
---

# Graphify frontmatter alias and typed-edge dedup gaps

## Síntoma

- En Graphify vault-aware 0.9.6, `graphify-obsidian explain "<frontmatter alias>"` no encontraba una nota que sí resolvía por su título canónico.
- En Graphify vault-aware 0.9.6, un link tipado como `depende de [[X]]` podía no producir `depende_de` cuando el mismo archivo ya enlazaba `[[X]]` como referencia genérica.
- En Graphify vault-aware `0.9.6.post1` o anterior, si una nota declara el mismo target en dos campos tipados de frontmatter —por ejemplo `related` y `parent`— puede sobrevivir sólo `related_to` y desaparecer `child_of` de `affected`, aunque el frontmatter y el lint sean válidos.

## Causa

- El índice de aliases del fork se usaba para resolver wikilinks, pero la selección de `explain` no consultaba esa misma resolución.
- La deduplicación de links Markdown usaba sólo el target y el grafo simple podía permitir que un `references` posterior, incluso inverso, sobreescribiera la relación tipada del mismo par.
- La reproducción de F6 acotó un gap residual entre dos relaciones tipadas de frontmatter para el mismo par source-target. La validación en código confirmó que la extracción conservaba todas las variantes y `build_from_json` las colapsaba al materializar un `Graph`/`DiGraph`, cuyo modelo simple admite un solo edge por par.

## Impacto

- Routing inconsistente entre wikilinks y operaciones Graphify.
- `affected`/`path` podían omitir una relación tipada real, degradando el Context Router y el análisis de impacto.

## Detección

- Comparar `explain` por título y por alias declarado en la misma nota.
- Inspeccionar `graph.json` y ejecutar `affected "<nota>.md" --relation <relación>` cuando existe un link genérico anterior al link tipado.
- Comparar `path "<child>.md" "<parent>.md"` con `affected "<parent>.md" --relation child_of` cuando el parent también aparece en `related`.

## Mitigación

- Para instalaciones 0.9.6 o anteriores, usar el título canónico y verificar manualmente el edge en `graph.json`.
- Para instalaciones actuales, instalar el wheel `0.9.6.post2` siguiendo [[graphify-obsidian-install]] y reconstruir el índice derivado.
- En `0.9.6.post1` o anterior, usar como mitigación temporal la higiene de fuente: no duplicar el target de `parent` dentro de `related`; conservar la relación canónica necesaria y reindexar.

## Resolución

- Resolución completa en Graphify vault-aware `0.9.6.post2`: el atributo escalar `relation` conserva compatibilidad y la lista ordenada `relations` guarda todas las variantes semánticas colapsadas del par; `affected` filtra sobre ambas representaciones y `path`/`explain`/MCP muestran el conjunto.
- Regresiones dirigidas cubren aliases y colisiones same-direction/reverse-direction; la suite completa quedó `2840 passed, 28 skipped` y Ruff verde.
- Validación E2E: `explain "AGENTS OS Executable Schema"` selecciona [[AGENTS OS - Fase 3]] y `affected "AGENTS OS.md" --relation child_of` devuelve Fase 2 y Fase 3.
- Workaround validado en F6: retirar el parent redundante de `related` restaura `child_of` para los proyectos 00 y 09 sin cambiar la fuente canónica del vínculo.
- Regresión post2: una nota con `parent` y `related` al mismo target conserva `references`, `child_of` y `related_to`; consultas separadas de `affected --relation child_of` y `affected --relation related_to` recuperan el source.

## Evidencia

- Gap reproducido sobre Graphify vault-aware 0.9.6 durante G0 de Fase 3.
- Fix y provenance registrados en [[AGENTS OS - Fase 3]],
  `80-agents/skills/agents-os-graphify-install/BUILD.md` y [[graphify-obsidian-install]].
- Regresión residual reproducida durante T6.1 con `agent-project-00-policy-and-doc-cleanup` y `agent-project-09-service-docs-rollout`: `path` devolvió `related_to` y `affected --relation child_of` omitió ambos hijos hasta retirar el `related` redundante.
