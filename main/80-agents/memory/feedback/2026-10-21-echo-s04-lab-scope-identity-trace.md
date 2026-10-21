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

# Session Feedback - 2026-10-21 - S04-lab: omisión de alcance, identidad de bytes y traza que perdía evidencia

## Context

- Agent surface: [[ZCode]] (GLM-5.3-Flash local)
- Agent run: `80-agents/journal/agent-runs/2026-10-21-zcode-glm53-flash-echo-s04-lab.md`
- Session goal: laboratorio C01–C09 completo + F1 + demo real (6 lanzamientos) + cierre
- Main entity: [[Echo Futures — Optimización de Campañas]]
- Skills used: agents-os-bootstrap, agents-os-agent-project-workflow (implícito por planner único), agents-os-agent-run-register, agents-os-session-feedback, agents-os-session-close
- Artifacts changed: planner (matriz C01–C10, Estado actual, bitácora), change_log, xKoRx/echo `experiment/campaign-lab-s04` `25a38402..872de033`

## Friction

1. **Omisión de alcance original (la causa raíz de este mandato):** los despachos S01–S04 anteriores recortaron el diseño a kernel+cableado y dejaron screening/proyección/filtros/export DECLARADOS sin implementar; ningún gate lo detectó porque la matriz de completitud contra el diseño completo no existía hasta este shot. **Medida:** todo shot de esta iniciativa abre actualizando la matriz vinculante (§9-bis) y la cierra contrastándola fila por fila — «declarado» nunca cuenta como fila funcional.
2. **Identidad por bytes de serialización:** `json.RawMessage` conserva el orden de claves, así que dos builders que escriben el mismo contenido en otro orden producen config_digest/run_id/signal_id distintos; el comparador lo reportó MISMATCH (correctamente) y costó un relanzamiento del tope. **Medida:** los builders de planes canonicalizan la serialización (binding-first) y los recibos comparan la spec canonizada ANTES de ejecutar; el REPLAY siempre deriva el plan del job referenciado (disciplina E6), nunca copia una base distinta.
3. **La traza descartaba la evidencia nueva:** `searchEconomicEvent` retenía sólo evaluaciones con señales, así que las decisiones de filtro (evidencia económica central de C05) desaparecían del registro en su punto técnico; se descubrió porque la demo real no cuadraba con el fixture. **Medida:** al introducir un estado nuevo con evidencia (absorbed+motivo), auditar el pipeline completo de RECORDS que lo consume en el mismo cambio, con una prueba de traza, no sólo de motor.
4. **Cobertura F1 arrastrada dos shots por presupuesto:** los 3 archivos de analytics quedaron bajo piso en S02-VERIFY, S03 y S04 porque las pruebas focalizadas siempre cayeron fuera del presupuesto del shot. **Medida:** el piso de cobertura del universo completo se mide al inicio del shot (no al cierre) y los tests focalizados se tratan como tarea de primera clase dentro del presupuesto, no como residual.
