---
type: doc
schema_version: 1
scope: tool
status: active
created: 2026-09-03
updated: 2026-09-03
indexable: true
tags:
  - kind/doc
  - tech/graphify
  - project/agents-os
---

# Graphify-Obsidian — build local

## Propósito

El fork vault-aware se instala por máquina y sus wheels no se almacenan ni se
sincronizan dentro del vault.

## Contenido

- Paquete actual: `graphifyy 0.9.6.post2`.
- Repo fuente local: resolver por `AGENTS_OS_GRAPHIFY_REPO` o por la ubicación
  configurada en la máquina; rama
  `feat/obsidian-vault-wikilinks`, base `220fb0a` más el snapshot local
  metadata-aware documentado en el historial del proyecto.
- Wheel actual SHA-256:
  `fd36205f41f9d9455c67f40cca1d191e1662b7c6f7146a9aebe23e56c57dc4a8`.
- Ubicación local de artefactos: `~/.local/share/graphify-obsidian/dist/`.
- Wrapper canónico pequeño:
  `80-agents/skills/agents-os-graphify-install/scripts/graphify-obsidian`.

Los agentes nunca deben publicar `graph.json`, `GRAPH_REPORT.md`, HTML, cachés,
manifests, snapshots o wheels dentro del vault. Markdown sigue siendo la fuente
de verdad y el índice es reconstruible.
