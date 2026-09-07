---
type: feedback
scope: graphify
created: 2026-07-22
updated: 2026-07-22
area: "[[Personal]]"
project: "[[AGENTS OS]]"
entities:
  - "[[AGENTS OS]]"
  - "[[graphify]]"
  - "[[Symphony]]"
related:
  - "[[2026-07-22-symphony-worker-permissions-summary]]"
aliases: []
agent: Cursor coding agent
session_goal: Diagnosticar permisos del worker Symphony
source_session:
confidence: high
load_policy: manual
indexable: false
index_priority: low
tags:
  - kind/feedback
  - scope/graphify
  - project/agents-os
  - project/symphony
  - agent/system1
---

# Graphify Session Feedback — 2026-07-22 — Symphony Worker Permissions

## Context

- Agent: Cursor coding agent
- Session goal: localizar el origen de `mkdir input: permission denied` y contrastarlo con la configuración viva.
- Main entity/topic: [[Symphony]]

## Utilidad y Valor Aportado

- Utilidad: 3/5.
- La consulta orientó hacia el worker y permitió pasar a búsquedas quirúrgicas del mensaje exacto.
- El hallazgo decisivo fue externo al grafo: la diferencia viva de `WorkingDirectory` en systemd.

## Fricción y Entorpecimiento

- La consulta inicial fue amplia y devolvió nodos genéricos de `Worker`.
- `graphify-obsidian` no tenía un `graph.json` disponible para el vault durante la búsqueda de duplicados.
- El índice de código no puede representar drift de configuración remota sin una fuente versionada.

## Usabilidad y Comprensión

- La regla de Graphify-first guio correctamente la orientación inicial.
- Fue necesario usar búsqueda textual específica y SSH después de que el grafo acotó el área.

## Propuestas de Mejora de la Herramienta

- Mejorar el ranking cuando la query contiene un mensaje de error literal.
- Exponer un estado claro del índice por wrapper para evitar descubrir tarde que el índice Obsidian no existe.
