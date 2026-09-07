---
type: change_log
scope: project
created: 2026-07-03
area: "[[Personal]]"
project: "[[AGENTS OS]]"
entities:
  - "[[AGENTS OS]]"
related:
  - "[[context-router]]"
  - "[[Economía de Tokens]]"
  - "[[token-economy-indexing-architecture]]"
tags:
  - kind/changelog
  - area/personal
  - project/agents-os
---

# 2026-07-03 — Concepto Context Router + PoC handoff-ready

## Motivo
La PoC del builder la construirá **otra IA**, así que el proyecto debe quedar auto-contenido.
Y el owner pidió un nuevo concepto del sistema, "Context Router", que se evangelizará a un equipo de TI.

## Cambios
- **Nuevo concepto (operating doc Sistema 1):** `80-agents/agents-os/context-router.md` — capa de
  decisión "qué/cuánto/en qué orden" cargar; routing table, context-pack, principios. Material
  de evangelización.
- **ADR actualizado:** `token-economy-indexing-architecture.md` referencia el Context Router.
- **Proyecto `Economía de Tokens` enriquecido para handoff:** sección "PoC builder — spec de
  handoff" con criterios de aceptación medibles y el detalle crítico del **node-id
  `{parent_dir}_{stem}`** (necesario para que `merge-graphs` una nodos). Nuevas tareas de
  Context Router. Objetivo marca el destino de evangelización al equipo.

## Validación
- Concepto creado; referencias cruzadas (ADR ↔ context-router ↔ proyecto) estilo LLM Wiki.
- Sin cambios a páginas canónicas de apps.
