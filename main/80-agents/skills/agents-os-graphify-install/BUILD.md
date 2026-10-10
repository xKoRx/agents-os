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
  - scope/tool
---

# Graphify-Obsidian — build local

## Propósito

El fork vault-aware se instala por máquina y sus wheels no se almacenan ni se
sincronizan dentro del vault.

## Contenido

- Paquete actual: `graphifyy 0.9.81.post1`.
- Repo fuente local: resolver por `AGENTS_OS_GRAPHIFY_REPO` o por la ubicación
  configurada en la máquina; rama
  `feat/obsidian-vault-wikilinks-0.9.81`, base tag upstream `v0.9.81` más el port local
  metadata-aware documentado en el historial del proyecto.
- Wheel actual SHA-256:
  `a85eb20603b40b443ee87fc9b6e3818eff43b37b3028dd7d9667220604fbb2e1`.
- Ubicación local de artefactos: `~/.local/share/graphify-obsidian/dist/`.
- Wrapper canónico pequeño:
  `80-agents/skills/agents-os-graphify-install/scripts/graphify-obsidian`.

Los agentes nunca deben publicar `graph.json`, `GRAPH_REPORT.md`, HTML, cachés,
manifests, snapshots o wheels dentro del vault. Markdown sigue siendo la fuente
de verdad y el índice es reconstruible.
