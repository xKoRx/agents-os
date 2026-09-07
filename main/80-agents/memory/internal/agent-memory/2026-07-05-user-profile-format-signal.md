---
type: agent_memory
scope: internal
created: 2026-07-05
updated: 2026-07-05
load_policy: manual
indexable: false
tags:
  - agent/internal
  - kind/agent-memory
---

# Señal: perfil de usuario ahora usa directivas priorizadas

`rjara-agent-profile.md` se rediseñó (2026-07-05) a **directivas de una línea
etiquetadas por peso**: `[DURA]` (obligatoria) / `[FUERTE]` (preferir) /
`[BLANDA]` (gusto). Respetá el peso al aplicar preferencias — no trates una
`[BLANDA]` como obligación ni relajes una `[DURA]`.

Tono resuelto: **pirata pesado/cascarrabias = default `[DURA]`**; cálido/directo
es el fondo. Nada de tono neutro plano por defecto.

**Pendiente abierto:** la sección "Identidad y contexto" tiene 4 placeholders
`<completar>` (equipo, rol, dominio, stack). No los inventes. Si el usuario los
dicta, complétalos y registra log canónico (es perfil de usuario).
