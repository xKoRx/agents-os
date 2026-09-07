---
type: learning
scope: project
created: 2026-08-08
updated: 2026-08-08
area: "[[Personal]]"
project: "[[AGENTS OS]]"
entities:
  - "[[AGENTS OS]]"
related:
  - "[[AGENTS OS Fase 5 — Piloto de layout por área]]"
aliases:
  - path-based plugin caches after vault moves
confidence: verified
source_session:
load_policy: when_project_loaded
indexable: true
index_priority: high
tags:
  - kind/learning
  - project/agents-os
  - action/vault-refactor
---

# Moves externos del vault requieren rescan de caches de plugins

## Aprendizaje

- Un move externo puede preservar Markdown, wikilinks y Graphify, pero dejar
  stale una caché de plugin basada en paths. La validación estructural debe
  incluir un rescan nativo del plugin y una vista real; su JSON derivado nunca
  reemplaza las fuentes Markdown.

## Aplicabilidad

- **Cuándo cargarlo:** al mover o renombrar árboles del vault que contienen
  proyectos, tareas o notas consumidas por plugins.
- **Cuándo no cargarlo:** en cambios de contenido que no alteran paths.

## Entidades relacionadas

- [[AGENTS OS]]

## Evidencia

- Fuente: [[AGENTS OS Fase 5 — Piloto de layout por área]] — el piloto quedó
  verde en lint/pack/Graphify, mientras Task Board conservó paths anteriores.
