---
type: feedback
scope: session
created: 2026-08-07
updated: 2026-08-07
area: "[[Personal]]"
project: "[[AGENTS OS - Fase 2]]"
entities:
  - "[[AGENTS OS]]"
  - "[[AGENTS OS - Fase 2]]"
related:
  - "[[2026-08-07-agents-os-fase2-g2-gaps-closure]]"
  - "[[agents-os-doctor]]"
aliases: []
agent: Claude
session_goal: cerrar los 2 gaps de G2
source_session:
confidence: high
load_policy: manual
indexable: false
index_priority: low
tags:
  - kind/feedback
  - scope/session
  - area/personal
  - project/agents-os
---

# Session Feedback - 2026-08-07 - agents-os-startup-budget-hotpath-drift

## Context

- Cierre de gaps de G2. El doctor `--strict` arrancó en `MEDIUM=1` (startup ≈5012 > 5k soft) **sin** que este trabajo tocara el set always-load.

## What Complicated The Session Most

- La nota interna global `agents-os-operating-continuity.md` (always-load) había crecido +241 chars en una sesión previa, duplicando el estado de G2 que ya vive en el planner; eso empujó el startup sobre el techo blando. Solo lo detecté al correr el doctor, no en tiempo de escritura.
- Ninguna barrera previene, al escribir, que una nota `load_policy: always` acumule estado que pertenece al planner. El lint all-vault de F3 (T3.3/T3.5) es el lugar natural para añadir un check del presupuesto always-load (startup ≤ soft target), además del frontmatter.

## Pain Pattern Candidate

- Is this likely to repeat? yes
- Suggested severity: low
- Candidate owner: AGENTS OS (Fase 3 lint)
- Promote to L3 memory? defer (cubierto por el change_log y esta nota; reconsiderar si reaparece)
