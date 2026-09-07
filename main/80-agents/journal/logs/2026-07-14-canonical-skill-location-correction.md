---
type: change_log
scope: global
created: 2026-07-14
updated: 2026-07-14
share_scope: team
project: "[[AGENTS OS]]"
entities:
  - "[[AGENTS OS]]"
related:
  - "[[agents-os-install]]"
  - "[[AGENTS OS - Beta y Hardening]]"
aliases: []
confidence: verified
source_session:
source_feedbacks: []
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/global
  - project/agentsos
  - change/updated
---

# Corrección de ubicación canónica de skills

## Cambio

- Se creó la decisión pública
  `80-agents/memory/public/decision/agents-os/canonical-skill-location.md` como
  fuente canónica del rationale arquitectónico.
- Se removieron las copias generadas bajo `.agents/skills/` y
  `.claude/skills/`.
- Codex y Claude quedan configurados por reglas que apuntan directamente a
  `80-agents/skills/`.
- La validación anterior demostró carga de reglas y adapters, pero no la
  arquitectura sin copias; esa conclusión queda superseded por este log.

## Motivo

- Mantener una sola fuente física, portable y agnóstica al cliente.

## Validación

- Duplicate check: Graphify más búsqueda fuente; no existía otro ADR con el
  mismo alcance.
- Reglas y limpieza mecánica se validaron en esta sesión.
- Codex y Claude localizaron por nombre y leyeron directamente
  `80-agents/skills/agents-os-hygiene-cycle/SKILL.md` en smoke tests read-only.
- El catálogo nativo de una sesión Codex ya abierta conservó la ruta antigua
  después de eliminarla; esto se trata como caché de proceso y obliga a validar
  discovery nativo sólo en una sesión reiniciada.
- Graphify se reindexó y ya no contiene el script ni los nodos de adapters
  eliminados.
- Invocación real sin copias y optimización por superficie quedan pendientes en
  [[AGENTS OS - Beta y Hardening]].

## Compartibilidad

- **Scope:** team
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- No restaurar adapters; registrar limitaciones por superficie y resolverlas
  sin crear una segunda fuente física.
