---
type: feedback
schema_version: 1
scope: session
created: 2026-10-21
updated: 2026-10-21
area: "[[Personal]]"
project: "[[AGENTS OS]]"
entities:
  - "[[AGENTS OS]]"
related: []
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

# Session Feedback - 2026-10-21 - short-topic

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

## Fricción observada (mandato S04/4-bis, corrección L1–L5 del laboratorio Echo Futures)

1. **Sobredeclaración de completitud con helpers sueltos**: el corte anterior entregó `search_round`/`resume` como capacidades C04 sin que sus outputs se consumieran entre sí (la ayuda anunciaba `search` que `main()` ni registraba; los midpoints no tenían camino a prepare/run). Lección operativa: exigir la matriz "L→comando→entrada→salida observada" ANTES de aceptar una fila como DEMOSTRADO; el nombre correcto de la función no es evidencia.
2. **Métricas derivadas del nombre del campo, no de eventos**: dos fills del mismo lado se cerraban como "trade ganador" y un string `purchased_at` acreditaba compra (PAUSED_SESSION comprada quedaba como other_terminal con pending=0). La reparación obligó a reconstruir posición firmada, censo por eventos PURCHASE y sesiones por `account_day_id`. Los reportes deberían nacer del ledger reconstruido, nunca de campos acumulados.
3. **Identidad build en la costura de ejecución**: el motor valida el commit declarado contra su binario (`BINARY_BUILD_REVISION_CONFLICT`); se gastó un intento por declarar HEAD en vez del commit del binario sellado. El MANUAL del laboratorio ya documenta la regla para la próxima ejecución.
4. **Coverage por archivo como meta ciega**: el piso ≥95% se cumplió declarando el denominador correcto (delta corregido completo, trace + despacho CLI vía subprocess), no ampliando legacy; un guard `LAB_CENSUS_BROKEN` era inalcanzable por construcción y se hizo real contando desde eventos — cubrir la versión muerta habría premiado código sin efecto.
