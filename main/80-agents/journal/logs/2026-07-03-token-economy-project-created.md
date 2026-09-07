---
type: change_log
scope: project
created: 2026-07-03
area: "[[Personal]]"
project: "[[AGENTS OS]]"
entities:
  - "[[AGENTS OS]]"
related:
  - "[[Economía de Tokens]]"
  - "[[token-economy-indexing-architecture]]"
tags:
  - kind/changelog
  - area/personal
  - project/agents-os
---

# 2026-07-03 — Proyecto "Economía de Tokens" creado

## Motivo
El owner pidió un proyecto que sea el planificador único de todas las modificaciones del
sistema de indexación (incluida la actualización del proceso de higienización).

## Cambios (Sistema 2)
- **Nuevo proyecto raíz:** `10-projects/Economía de Tokens/Economía de Tokens.md`
  (`owner: me`, `root: true`, area Personal). Backlog de 9 tareas + bitácora + decisiones.

## Hallazgo técnico registrado (verificado 2026-07-03)
- `graphify` (modo AST) **NO captura los `[[wikilinks]]` de Obsidian como edges**:
  `affected "java-polycard-sdk"` → 0, `explain "recommendations-decoration-sdk"` → no node,
  pese a que los cuerpos contienen esos links (grep confirma). → El grafo de relaciones del
  vault requiere un **builder propio**; graphify queda fuerte solo en código.
- Candidato a promover a `learning`/`known_error` cuando se confirme en el PoC.

## Validación
- Proyecto creado desde `70-templates/project.md`. Sin cambios a páginas canónicas de apps.
