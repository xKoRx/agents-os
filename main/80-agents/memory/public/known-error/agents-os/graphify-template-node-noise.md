---
type: known_error
scope: project
created: 2026-06-27
updated: 2026-09-03
area: "[[Personal]]"
project: "[[AGENTS OS]]"
application:
entities:
  - "[[AGENTS OS]]"
related:
  - "[[agents-os-context-retrieval]]"
  - "[[Agent Memory System Graphify Contract]]"
aliases:
  - graphify template node noise
  - noisy graphify template retrieval
  - generic graphify query anchors templates
confidence: high
source_session:
load_policy: when_error_matches
indexable: true
index_priority: high
tags:
  - area/personal
  - kind/known-error
  - priority/high
  - project/agents-os
  - project/agentsos
  - scope/project
  - tool/graphify
---
# Graphify Template Node Noise

## Sintoma

- Queries con terminos genericos como `transcript`, `pendiente`, `retrieval` o `Graphify` pueden devolver primero nodos de `80-agents/templates/` en vez de memoria viva o documentos canonicos.
- Ejemplos observados:
  - Queries enfocadas en ruido de templates devolvieron `80-agents/templates/constitution.md` y `80-agents/templates/hygiene-report.md`.
  - Queries con `transcript` y `pendiente` devolvieron `80-agents/templates/raw-session.md`, `80-agents/templates/constitution.md` y `80-agents/templates/session-summary.md`.

## Causa

- Graphify indexa encabezados y secciones de templates. Cuando la query usa palabras comunes presentes en esos templates, el recorrido puede arrancar desde nodos genericos como `Transcript`, `Pendiente`, `Retrieval` o `Graphify`.

## Impacto

- Un agente puede interpretar ruido de templates como contexto real del proyecto.
- Tambien puede concluir erroneamente que una memoria viva no existe si la query queda atrapada en nodos genericos.

## Deteccion

- Revisar si los primeros candidatos tienen `source_file` bajo `80-agents/templates/`.
- Revisar si el traversal indica `Context: generic_arg` o arranca desde nodos genericos.
- Comparar contra archivos fuente o el `graph.json` resuelto por `graphify-obsidian cache-path` antes de decidir que falta conocimiento.

## Mitigacion

- Reintentar con query estricta: `entidad + tipo de memoria + sintoma/decision/operacion concreta`.
- No usar nodos de template como evidencia de estado vivo.
- Si la query sigue ruidosa, validar con `graphify-obsidian explain "<titulo exacto>"`, abrir el archivo fuente o inspeccionar el índice local resuelto por `cache-path`.

## Evidencia

- Observado durante mantenimiento del sistema de memoria el 2026-06-27.
- Se actualizaron `80-agents/skills/_shared/graphify-contract.md` y `80-agents/skills/agents-os-context-retrieval/SKILL.md` para documentar el manejo.
