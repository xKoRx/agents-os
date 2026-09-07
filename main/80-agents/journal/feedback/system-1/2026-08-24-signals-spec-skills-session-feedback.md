---
type: feedback
schema_version: 1
scope: session
created: 2026-08-24
updated: 2026-08-24
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

# Session Feedback - 2026-08-24 - skills de autoría de specs

## Context

- Agent surface: [[Claude Code]]
- Agent model: claude-opus-5
- Agent run: [[2026-08-24-component-context-spec-rewrite-and-impl-alignment]]
- Session goal: corregir SIG-590, crear canon para specs técnicas y alinear la implementación
- Main entity: [[Crear Context]]
- Skills used: [[agents-os-bootstrap]], [[signals-func-spec-authoring]], [[signals-tech-spec-authoring]], meli-security-expert
- Retrieval mode: cold start + entidad
- Artifacts changed: dos skills, una regla compartida nueva, INDEX, un runbook de recursos, un known-error

## Scores

- Startup clarity: 4
- Retrieval usefulness: 3
- Skill fit: 2
- Template fit: 4
- Closeout friction: 3
- Overall confidence: 4

## What Complicated The Session Most

- Observation: la skill `signals-spec-authoring` existía en **dos** lugares con contenido distinto — 6.5k en el vault, 13k en el cliente — y nada lo señalaba.
- Why it was hard: la canónica del vault era la **vieja**. Un agente que cargara esa habría aplicado convenciones desactualizadas creyéndolas canon, sin ninguna señal de conflicto.
- Proposed improvement: un chequeo del hygiene cycle que compare cada skill del vault con su contraparte en el cliente y falle ante divergencia. El patrón router-en-vez-de-copia ya existe en [[pr-description]] pero no estaba aplicado acá.

## Most Useful Part Of Sistema 1

- What helped: la constitución, puntualmente el mandamiento sobre versiones productivas en ramas feature.
- Why it helped: detectó que la spec escrita en esta misma sesión mandaba fijar la versión productiva en la rama, violando la regla. Sin esa invariante cargada, el error se publicaba.
- Keep/change: keep.

## Least Useful Or Noisy Part

- What did not help: nada material.
- Why it was weak/noisy: —
- Proposed cleanup: —

## Missing Support

- Problem not solved by Sistema 1: no había canon para specs **técnicas**, y el hueco sólo se hizo visible al intentar corregir una.
- How Sistema 1 could help next time: resuelto — [[signals-tech-spec-authoring]], derivada de las 33 specs técnicas reales del proyecto.
- Suggested artifact type: skill (creada).

## Retrieval Feedback

- Useful query or source: el corpus de specs de Spellbook vía CLI. Derivar convenciones de ahí corrigió **dos** reglas inventadas por intuición en esta misma sesión: el identificador de decisión del equipo, y el criterio de anclaje al código.
- Missing context: —
- Duplicate/noisy result: —
- Better future query: antes de escribir una convención de equipo, listar el corpus real y medirlo. La intuición sobre "cómo escribe el equipo" falló dos de dos veces.

## Skill Feedback

- Skill that worked well: [[agents-os-bootstrap]].
- Skill that was confusing: la de specs funcionales, por el drift descrito arriba.
- Trigger/routing gap: los nombres desalineados no dejaban leer la relación entre las dos skills pareadas.
- Suggested contract change: para skills pareadas, nombres simétricos y una fuente compartida para lo que ambas exigen.

## Template Feedback

- Template used: change-log, agent-run, known-error, session-feedback.
- Field that helped: el bloque de rollback del change-log.
- Field that felt redundant: —
- Missing field: —

## Memoria Interna (Internal Memory)

- ¿Consultaste la memoria interna al iniciar? sí, vía bootstrap.
- ¿Qué valor operativo aportó? continuidad sobre el estado de las ramas y los hallazgos de seguridad ya verificados; evitó re-auditar el cifrado ausente.
- ¿Dejaste algún mensaje para el próximo agente? no en memoria interna; el estado quedó en la nota de proyecto y en el agent run.
- ¿Utilidad del espacio privado (1-5)? 4.

## Pain Pattern Candidate

- Is this likely to repeat? yes
- Suggested severity: medium
- Candidate owner: [[AGENTS OS]]
- Promote to L3 memory? defer — el patrón router ya está documentado; falta el chequeo automático.

## One Next Improvement

- Chequeo de divergencia vault↔cliente para todas las skills, en el hygiene cycle.
