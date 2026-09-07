---
type: change_log
scope: project
created: 2026-07-03
area: "[[Personal]]"
project: "[[AGENTS OS]]"
entities:
  - "[[AGENTS OS]]"
related:
  - "[[token-economy-indexing-architecture]]"
tags:
  - kind/changelog
  - area/personal
  - project/agents-os
---

# 2026-07-03 — ADR arquitectura de indexación (economía de tokens)

## Motivo
Fijar la arquitectura de retrieval en 4 capas y el rol de cada índice, para que ningún
agente futuro vuelva a meter basura al contexto ni a pagar semántica LLM innecesaria.

## Cambios (memoria pública / Sistema 2)
- **Nueva decisión (ADR):** `80-agents/memory/public/decision/agents-os/token-economy-indexing-architecture.md`
  — 4 capas (tags → index.md → graph.json → body); roles fijos; veredicto "Graphify
  solo-índices aporta y no estorba si se mantiene limpio y acotado".
- **Nueva idea (Sistema 2):** `30-resources/ideas/2026-07-03-sistema-experimentos-feedback-retrieval.md`
  — sistema de experimentos+feedback, dejado como `seed`, NO implementar aún (decisión del owner).
- **Doc actualizada:** `30-resources/00-RESOURCE-WIKI.md` referencia el ADR para el aporta/estorba.

## Pendiente / próximos pasos
- Construir el wrapper / capa delgada sobre `graph.json` + `00-index.md` (contexto mínimo con tope de tokens).
- Escribir/actualizar la skill de retrieval con el protocolo de 4 capas.
- No parchear `site-packages` de graphify; fork editable solo si se justifica.

## Validación
- ADR, idea y changelog creados desde template. Sin cambios a páginas canónicas de apps.
