---
type: learning
scope: project
created: 2026-06-27
updated: 2026-06-27
area: "[[Personal]]"
project: "[[AGENTS OS]]"
application:
entities:
  - "[[AGENTS OS]]"
related:
  - "[[agents-os]]"
aliases:
  - official docs vs memory boundary
  - documentación oficial no es memoria
confidence: verified
source_session:
load_policy: when_project_loaded
indexable: true
index_priority: high
tags:
  - area/personal
  - kind/learning
  - priority/high
  - project/agents-os
  - project/agentsos
  - scope/project
---
# Official Docs And Memory Are Separate Surfaces

## Aprendizaje

Cuando el usuario pida desacoplar la documentación oficial del sistema, no se
debe inferir que hay que eliminar referencias de memoria pública o interna.

## Regla Operativa

- La documentación oficial del sistema debe evitar cargar contexto indebido del
  proyecto de desarrollo.
- La memoria sí puede y debe referenciar proyectos concretos cuando esa memoria
  trata sobre ellos.
- La memoria del proyecto `[[AGENTS OS]]` debe seguir linkeada a `[[AGENTS OS]]`
  para que pueda recuperarse cuando el trabajo activo sea mantener o evolucionar
  ese proyecto.
- Antes de tocar memoria persistente por una instrucción sobre documentación,
  distinguir explícitamente: documentación oficial, memoria pública, memoria
  interna, journal y proyecto de control.

## Error Que Evita

No mover, renombrar ni des-scopear memorias de proyecto solo porque la guía
operativa del sistema no debe depender del proyecto.
