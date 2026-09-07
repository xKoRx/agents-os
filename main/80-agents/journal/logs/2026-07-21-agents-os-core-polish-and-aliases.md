---
type: change_log
scope: project
created: 2026-07-21
updated: 2026-07-21
share_scope: team
area:
  - "[[Personal]]"
project:
  - "[[AGENTS OS]]"
application:
entities:
  - "[[AGENTS OS]]"
  - "[[agents-os]]"
  - "[[agent-constitution]]"
  - "[[context-router]]"
related:
aliases:
  - AGENTS OS core polish and aliases
confidence: verified
source_session: 2026-07-21-agents-os-audit-and-fixes
load_policy: manual
indexable: false
index_priority: never
tags:
  - area/personal
  - kind/changelog
  - project/agents-os
  - project/agentsos
  - scope/project
---

# 2026-07-21 — AGENTS OS Core: Polish + Aliases (PR 2)

## Cambio

- **Tipo:** fix / consistency
- **Archivo(s):**
  - `80-agents/agents-os/agent-constitution.md`
  - `80-agents/agents-os/context-router.md`
  - `80-agents/skills/INDEX.md`

## Motivo

PR 1 cerró los hallazgos críticos (links rotos y `load_policy` ausente en
skills core). Este PR 2 cierra los refinamientos de consistencia
documentados en la auditoría del 2026-07-21:

1. `rjara-agent-profile.md` referencia `[[agent-constitution]]` (forma kebab),
   pero `agent-constitution.md` no la tenía en `aliases:`. Obsidian sólo
   resuelve el alias si está declarado, así que el link dependía de la
   coincidencia exacta con el filename. Añadir el alias elimina esa fragilidad.
2. `context-router.md` tenía un bloque `> [!success]` con conteo absoluto
   (`852/852 edges resueltos`) que ya era historia: cada reindex de Graphify
   cambia los números y la métrica útil es **0 edges colgantes**, no el total.
3. `context-router.md` carecía de `entities:` y `load_policy:` en
   frontmatter,违背 el contrato del `metadata-schema.md` que exige esos campos
   en notas consumibles por agentes.
4. `INDEX.md` (catálogo de skills) no tenía `entities:`, `load_policy:` ni
   `next_audit:` en frontmatter, lo que impedía a `agents-os-hygiene-cycle`
   tener un disparador explícito para reauditarlo.

## Fuentes usadas

- Auditoría del 2026-07-21, registro en
  `80-agents/journal/logs/2026-07-21-agents-os-core-load-policy-and-broken-links.md`.
- Constitución L42-43 (carga always-load) y L82 (changelog en journal/logs).
- `80-agents/skills/_shared/metadata-schema.md` (contrato de frontmatter).
- Confirmación del usuario en sesión actual (preferir añadir alias en
  constitución antes que corregir el link del perfil).

## Resolución aplicada

- `agent-constitution.md` frontmatter `aliases:` recibe la entrada
  `agent-constitution` (forma kebab-canónica). El resto de aliases se conserva.
- `context-router.md`:
  - Bloque `> [!success]` reescrito: se reemplaza el conteo "852/852" por la
    regla invariante "**0 edges colgantes**"; se conserva la query correcta
    de backlinks y los enlaces a [[Economía de Tokens]] y
    `../skills/_shared/graphify-contract.md`.
  - Frontmatter gana `entities:`, `related:`, `load_policy: manual`,
    `indexable: true`, `index_priority: high` y `updated: 2026-07-21`.
- `INDEX.md`:
  - Frontmatter gana `entities:`, `related:`, `load_policy: manual`,
    `indexable: true`, `index_priority: high`, `next_audit: 2026-08-21` y
    `updated: 2026-07-21`.
- Sin cambios en constitución, perfil de usuario ni en skills adicionales
  (cubiertos por PR 1).

## Validación

- `grep "agent-constitution"` en `agent-constitution.md` muestra la entrada
  nueva dentro del bloque `aliases:`.
- `grep "load_policy: manual"` en `context-router.md` e `INDEX.md` devuelve
  `1` en cada uno.
- `grep "next_audit"` en `INDEX.md` devuelve `1`.
- `bash "10-projects/AGENTS OS/chatgpt-pack/build-pack.sh"` regenera
  `outputs/agents-os-chatgpt/` con 120 archivos copiados y validación pasada.
- Pendiente para `agents-os-hygiene-cycle`: reindex de Graphify tras añadir
  `entities:` en `context-router.md` y `INDEX.md`, y validación de que el
  alias `agent-constitution` se resuelve en el grafo.