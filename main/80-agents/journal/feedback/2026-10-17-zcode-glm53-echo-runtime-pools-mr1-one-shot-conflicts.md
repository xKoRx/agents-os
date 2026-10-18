---
type: feedback
schema_version: 1
scope: session
created: 2026-10-18
updated: 2026-10-18
area: "[[Echo]]" "[[Personal]]"
project: "[[Echo Futures — Runtime Pools]]" "[[AGENTS OS]]"
entities:
  - "[[AGENTS OS]]"
related:
  - "[[technical-project-manager]]"
aliases: []
agent_surface: "[[Codex]]"
agent_model: unknown
agent_run:
session_goal:
source_session:
confidence: high
load_policy: manual
indexable: false
index_priority: low
tags:
  - kind/feedback
  - scope/session
  - project/agents-os
  - agent/system1
---

# Session Feedback - 2026-10-18 - short-topic

## Context
Sesión MR1 del submanager local del proyecto [[Echo Futures — Runtime Pools]]: reparación MR01–MR06 de la entrega S02 con 5 subagentes one-shot (MR-A..MR-E) y 4 retornos acotados. Related run: [[2026-10-17-zcode-glm53-echo-runtime-pools-mr1-repair]].

## Scores

Use 1-5, where 1 is poor and 5 is excellent.

- Startup clarity:
- Retrieval usefulness:
- Skill fit:
- Template fit:
- Closeout friction:
- Overall confidence:

## What Complicated The Session Most
Mandatos one-shot con allowlist estricta ante conflictos reales mandato-vs-código: MR-A encontró que la política TGMM congelada exigía un campo fuera de su allowlist y no tenía camino legítimo (preguntar no era posible en contexto desatendido); terminó decidiendo por mejor juicio y declarando PLAN_CONFLICT a posteriori. La misma estructura produjo retornos adicionales (MR-B-R1, MR-C-R1, MR-B-R2). La defensa que funcionó: el oráculo preexistente (MR-E) cazó la regresión H1 del propio delta.

## Most Useful Part Of Sistema 1

- What helped:
- Why it helped:
- Keep/change:

## Least Useful Or Noisy Part

- What did not help:
- Why it was weak/noisy:
- Proposed cleanup:

## Missing Support
La plantilla de mandato one-shot (technical-project-manager, sección de mandato maestro) no declara quién resuelve un PLAN_CONFLICT ni con qué autoridad en contextos no interactivos. Sugerencia: sección `/conflicts` explícita — clasificar (wiring mínimo vs rediseño vs contrato congelado), aplicar wiring mínimo reversible con evidencia cuando proceda y reportar la desviación como campo obligatorio del handoff, con ratificación/reversión del submanager antes de integrar. No depender de AskUserQuestion en ejecución desatendida.

## Retrieval Feedback

- Useful query or source:
- Missing context:
- Duplicate/noisy result:
- Better future query:

## Skill Feedback

- Skill that worked well:
- Skill that was confusing:
- Trigger/routing gap:
- Suggested contract change:

## Template Feedback

- Template used:
- Field that helped:
- Field that felt redundant:
- Missing field:

## Memoria Interna (Internal Memory)

- ¿Consultaste la memoria interna (`80-agents/memory/internal/`) al iniciar? [sí/no]
- ¿Qué valor operativo aportó para esta sesión (continuidad, detalles crudos, advertencias)?
- ¿Dejaste algún mensaje, instrucción o hipótesis para el próximo agente en la memoria interna?
- ¿Qué tan útil te resulta tener este espacio privado fuera de la vista directa del usuario (1-5) y cómo podemos mejorar su utilidad?

## Pain Pattern Candidate
"Otro archivo ⇒ STOP + PLAN_CONFLICT" sin ruta de resolución convierte un guard de ownership en un bloqueo silencioso o en una desviación sin autoridad. Patrón visto 1× con resolución buena (ratificación); vigilar en próximos mandatos one-shot.

## One Next Improvement

-
