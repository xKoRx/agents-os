---
type: feedback
schema_version: 1
scope: session
created: 2026-10-20
updated: 2026-10-20
area: "[[Personal]]"
project: "[[AGENTS OS]]"
entities:
  - "[[AGENTS OS]]"
related: []
aliases: []
agent_surface: "[[ZCode]]"
agent_model: GLM-5.3-Flash (ZCode local)
agent_run:
session_goal: Procesar Clutifx ep06 (failure swing) con course-knowledge-extraction y publicar la biblioteca ch06 completa.
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

# Session Feedback - 2026-10-20 - documentation-verifier provider gap (Clutifx ch06)

## Context

- Agent surface:
- Agent model:
- Agent run:
- Session goal:
- Main entity:
- Skills used:
- Retrieval mode:
- Artifacts changed:

## Scores

Use 1-5, where 1 is poor and 5 is excellent.

- Startup clarity:
- Retrieval usefulness:
- Skill fit:
- Template fit:
- Closeout friction:
- Overall confidence:

## What Complicated The Session Most

- Observation:
- Why it was hard:
- Proposed improvement:

## Most Useful Part Of Sistema 1

- What helped:
- Why it helped:
- Keep/change:

## Least Useful Or Noisy Part

- What did not help:
- Why it was weak/noisy:
- Proposed cleanup:

## Missing Support

- Problem not solved by Sistema 1:
- How Sistema 1 could help next time:
- Suggested artifact type:

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

- Is this likely to repeat? yes/no/unknown
- Suggested severity: low/medium/high
- Candidate owner:
- Promote to L3 memory? yes/no/defer

## One Next Improvement

-

## Observación

Recurrente (4º capítulo consecutivo: ch03, ch04, ch05, ch06): el tipo de agente
`documentation-verifier` no es lanzable en esta cuenta — el dispatcher resuelve
`account:zai-start-plan/GLM-5.3-Flash` y el provider no existe
("Provider unavailable / 供应商不存在或不可用"). El resto de tipos
(`general-purpose`, etc.) funciona normal en la misma sesión.

## Impacto

El rol DOCUMENTATION_VERIFIER de `course-knowledge-worker` se ejecuta con
`general-purpose` + prompt adversarial (fallback ya documentado en
METHODOLOGY-FEEDBACK del curso). Funciona, pero pierde las garantías del
especialista (read-only por contrato del tipo) y depende de que el prompt
reproduzca el contrato a mano.

## Sugerencia

Revisar el binding del tipo `documentation-verifier` en la configuración de
agentes de esta cuenta (apunta a un provider de otro plan). No bloquea la
metodología: el fallback está probado en 4 capítulos sin falsos PASS.
