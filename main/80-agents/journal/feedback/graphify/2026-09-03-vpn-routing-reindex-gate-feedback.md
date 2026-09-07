---
type: feedback
schema_version: 1
scope: graphify
created: 2026-09-03
updated: 2026-09-03
area: "[[Personal]]"
project: "[[AGENTS OS]]"
entities:
  - "[[AGENTS OS]]"
  - "[[graphify]]"
  - "[[Meli]]"
  - "[[Aranea]]"
related:
  - "[[rjara-vpn-routing-preferences]]"
  - "[[2026-09-03-vpn-routing-session-feedback]]"
aliases: []
agent_surface: "[[Codex]]"
agent_model: unknown
agent_run: "[[2026-09-03-codex-unknown-component-context-review-release]]"
session_goal: "Indexar la preferencia canónica que distingue GlobalProtect de Aranea"
confidence: high
load_policy: manual
indexable: false
index_priority: low
tags:
  - kind/feedback
  - scope/graphify
  - project/agents-os
  - agent/system1
---

# Graphify Session Feedback — Gate global bloquea reindex dirigido

## Context

- Se creó [[rjara-vpn-routing-preferences]] y sus ocho archivos relacionados pasaron lint estricto con 0 errores y 0 warnings.
- `graphify-obsidian update` abortó antes de indexar por 32 findings globales ajenos en notas de Symphony, known errors y skills de specs.

## Utilidad y valor aportado

- La documentación de Graphify indicó correctamente que el índice debía reconstruirse después de cambiar memoria indexable.
- El gate evitó incorporar notas con frontmatter global inválido, pero no permitió publicar un cambio dirigido ya validado.

## Fricción

- El reindex es all-or-nothing: deuda nueva en cualquier parte del vault bloquea la actualización de una nota independiente que pasa lint estricto.
- No existe una vía documentada para actualizar un subconjunto seguro o aceptar temporalmente findings ajenos con baseline explícito.

## Propuesta de mejora

- Agregar un modo de reindex dirigido que valide el corpus global pero permita actualizar paths explícitos ya aprobados, o un flujo claro para refrescar el baseline sin ocultar la deuda.
- Mientras no exista, reportar separadamente `changed paths clean` y `global blockers`, conservando el índice anterior sin afirmar éxito.
