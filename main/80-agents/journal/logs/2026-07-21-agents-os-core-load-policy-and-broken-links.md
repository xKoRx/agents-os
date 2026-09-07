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
  - "[[agents-os-bootstrap]]"
  - "[[agents-os-context-retrieval]]"
  - "[[agents-os-session-close]]"
  - "[[agent-constitution]]"
related:
  - "[[context-router]]"
aliases:
  - AGENTS OS core load policy and broken links fixed
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

# 2026-07-21 — AGENTS OS Core: load_policy + Links Rotos

## Cambio

- **Tipo:** fix / consistency
- **Archivo(s):**
  - `80-agents/agents-os/agents-os.md`
  - `80-agents/skills/agents-os-bootstrap/SKILL.md`
  - `80-agents/skills/agents-os-context-retrieval/SKILL.md`
  - `80-agents/skills/agents-os-session-close/SKILL.md`

## Motivo

Auditoría del núcleo de AGENTS OS detectó dos clases de drift entre el contrato
de la constitución/guía operativa y los archivos canónicos:

1. **Wikilinks rotos por placeholders literales** en
   `80-agents/agents-os/agents-os.md` sección "Regla de proyectos humanos vs
   proyectos de agente". El bloque contenía `[[Proyecto humano padre]]` (que no
   apunta a ninguna nota existente en el vault) y `[[<proyecto de agente>]]` /
   `<slug>` con sintaxis de placeholder que rompe el parser de Obsidian.
2. **`load_policy: always` ausente en las tres skills core** que
   `agents-os.md` L184 declara explícitamente como "Skills Core (Always-run)".
   Sin esa propiedad, un agente que escanea por `load_policy: always` (contrato
   del `metadata-schema.md`) no marca las skills como críticas y la promesa de
   "ejecución incondicional al inicio o al cierre" queda sin enforcement
   técnico.

Adicionalmente, el bullet list de skills adicionales en `agents-os.md`
L102-117 omitía 6 skills que sí existen en `80-agents/skills/` y aparecen en
`80-agents/skills/INDEX.md` (`agents-os-graphify-install`,
`agents-os-resource-wiki`, `agents-os-skill-authoring`,
`agents-os-tagging-system`), dejándolas invisibles para agentes que sólo
carguen la guía operativa.

## Fuentes usadas

- Auditoría del núcleo guiada por `80-agents/agents-os/agents-os.md`,
  constitución, INDEX de skills y Graphify (`graphify-obsidian explain/path`).
- Constitución L42-43 (carga always-load) y L184-189 (skills core Always-run).
- `80-agents/skills/_shared/metadata-schema.md` (contrato de
  `entities`/`load_policy`/`indexable`/`index_priority`).
- Confirmación del usuario en sesión actual (corregir los 8 hallazgos
  priorizados, escape con corchetes textuales, alias en constitución).

## Resolución aplicada

- `agents-os.md` sección "Regla de proyectos humanos vs proyectos de agente":
  los literales `[[Proyecto humano padre]]` y `[[<proyecto de agente>]]` se
  reemplazan por texto corcheteado con `<…>` (sin sintaxis de wikilink) y se
  amplía el bloque 6 con bullets faltantes para alinear con `INDEX.md`.
- `agents-os.md` L102-117: añadidos bullets para
  `agents-os-graphify-install`, `agents-os-resource-wiki`,
  `agents-os-skill-authoring`, `agents-os-tagging-system`. Las skills
  `agents-os-install` y `agents-os-hygiene-cycle` ya estaban listadas y se
  mantuvieron.
- Las tres skills core (`agents-os-bootstrap`,
  `agents-os-context-retrieval`, `agents-os-session-close`) reciben en su
  frontmatter:
  - `entities: ["[[AGENTS OS]]", "[[agents-os]]", …]`
  - `load_policy: always`
  - `indexable: true`
  - `index_priority: critical`
  - tag adicional `agent/alwaysload` (alineado con constitución y perfil de
    usuario).
- Sin cambios en constitución, perfil de usuario ni en skills adicionales; esos
  refinamientos se agrupan en un PR 2 posterior para mantener PRs ≤ 20 archivos
  y diffs enfocados.

## Validación

- `grep -oE '\[\[[^]]+\]\]' 80-agents/agents-os/agents-os.md` no contiene
  `[[Proyecto humano padre]]` ni `[[<…>]]` con sintaxis de placeholder rota.
- `grep -c "load_policy: always"` sobre las tres SKILL.md devuelve `1` en cada
  una.
- `grep -c "agent/alwaysload"` sobre las tres SKILL.md devuelve `1` en cada
  una.
- Búsqueda en `80-agents/skills/` confirma que las 6 skills añadidas a la
  lista de `agents-os.md` existen y tienen su SKILL.md.
- Pendiente para PR 2: rebuild de `95-graphify/obsidian/graph.json` tras añadir
  alias `agent-constitution` y el campo `entities:` en `context-router.md`.