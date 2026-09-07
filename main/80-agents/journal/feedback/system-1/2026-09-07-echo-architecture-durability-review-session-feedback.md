---
type: feedback
schema_version: 1
scope: session
created: 2026-09-07
updated: 2026-09-07
area: "[[Echo]]"
project: "[[Echo - Discovery y Estado]]"
entities:
  - "[[echo-core]]"
  - "[[echo-forge]]"
related:
  - "[[Echo + Echo Forge — Architecture Durability and Contract Review — Fable 5.1]]"
aliases: []
agent_surface: "[[Cursor]]"
agent_model: "Claude Fable 5.1 (effort high)"
agent_run: "[[2026-09-07-cursor-claude-fable-5-1-echo-architecture-durability-review]]"
session_goal: "Revisión de durabilidad arquitectónica V1 Echo + Echo Forge y consistencia del contrato Astra"
source_session: "ECHO-ECHO-FORGE-V1-ARCHITECTURE-DURABILITY-AND-CONTRACT-CONSISTENCY-REVIEW"
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

# Session Feedback - 2026-09-07 - echo-architecture-durability-review

## Context

- Agent surface: [[Cursor]]
- Agent model: Claude Fable 5.1 (effort high, reportado por usuario)
- Agent run: [[2026-09-07-cursor-claude-fable-5-1-echo-architecture-durability-review]]
- Session goal: revisión independiente de durabilidad del V1 y del contrato Live Authority; cierre por skill solicitado explícitamente.
- Main entity: [[echo-core]] / [[echo-forge]]
- Skills used: bootstrap, context-retrieval, resource-wiki, agent-run-register, session-feedback, session-close
- Retrieval mode: Graphify vault + Resources íntegros + graphify-personal en Symphony + dos subagentes explore
- Artifacts changed: Resource nuevo, tres deltas de una línea, índice/log applications, checkpoint proyecto, run, feedback, change_log

## Scores

- Startup clarity: 4
- Retrieval usefulness: 4
- Skill fit: 4
- Template fit: 4
- Closeout friction: 3
- Overall confidence: 4

## What Complicated The Session Most

- Observation: los tres Resources canónicos son muy largos y hubo que leerlos íntegros para no heredar autoridad equivocada.
- Why it was hard: no existe una vista compacta "disposición vigente por contrato" separada de la narrativa.
- Proposed improvement: mantener una freeze matrix única viva (ahora en el Resource nuevo §13) y que futuras revisiones la actualicen en vez de crear narrativas paralelas.

## Most Useful Part Of Sistema 1

- What helped: notas D (identidad V2, BuilderSupply, Finalist V2, MT5 V3) y la nota de decisión I de Astra separadas del Resource.
- Why it helped: permitió distinguir D de I sin releer los Resources para cada contrato.
- Keep/change: keep.

## Least Useful Or Noisy Part

- What did not help: recordatorios repetidos "MANDATORY graphify" en cada lectura del vault, donde `graphify-personal` apunta al repo Symphony, no al vault.
- Why it was weak/noisy: ruido de contexto sin cambio de comportamiento.
- Proposed cleanup: limitar el recordatorio a lecturas dentro del repo con `graphify-out/`.

## Missing Support

- Problem not solved by Sistema 1: `graphify-obsidian update` rechaza el rebuild completo por 66 errores de frontmatter en notas ajenas (templates `{{date}}`, memorias sin `scope/project`); una sesión no puede reindexar su delta sin sanear deuda global.
- Problem not solved by Sistema 1: el cierre anterior falló en visibilidad de rutas; ninguna skill exige listar rutas exactas de los artefactos de cierre en el mensaje final cuando el owner lo pide.
- How Sistema 1 could help next time: en modo detallado, incluir rutas vault-relativas exactas de feedback/run/log.
- Suggested artifact type: ajuste menor en `agents-os-session-close` (Detailed Mode).

## Retrieval Feedback

- Useful query or source: `graphify-personal query "CanonicalStrategyID host key"` orientó al archivo exacto; el hallazgo `HOST_KEY` salió de lectura directa.
- Missing context: ninguno material.
- Duplicate/noisy result: nodos `T`/`State` sin source en el subgrafo.
- Better future query: nombre exacto del símbolo Go.

## Skill Feedback

- Skill that worked well: `materialize_schema_note.py` + `lint.py --strict`.
- Skill that was confusing: `resolve_schema_type.py` sin `--help`.
- Trigger/routing gap: ninguno.
- Suggested contract change: ninguno.

## Template Feedback

- Template used: resource, change-log, agent-run, session-feedback.
- Field that helped: `sources` + `last_verified` en resource.
- Field that felt redundant: `Evaluación` con scores 1–5 en agent-run para trabajo de revisión documental.
- Missing field: ninguno.

## Memoria Interna (Internal Memory)

- ¿Consultaste la memoria interna al iniciar? sí (continuidad global y continuidad de la revisión independiente anterior).
- Valor operativo: confirmó que la revisión anterior estaba cerrada y qué quedó como I; evitó reabrir MT5.
- ¿Dejaste mensaje para el próximo agente? no; la continuidad quedó en el checkpoint del proyecto (una sola superficie, por skill).
- Utilidad del espacio privado (1-5): 3; mejoraría con un puntero al checkpoint vigente por entidad.

## Context Efficiency

- context_high_water_mark: unknown
- main_context_growth_sources: lectura íntegra de tres Resources largos; reportes de dos subagentes; system reminders repetidos.
- avoidable_context_growth: reminders graphify en lecturas del vault.
- compaction_opportunity: sí, tras terminar la lectura de Resources (ocurrió una compactación).
- efficiency_assessment: GOOD

## Pain Pattern Candidate

- Is this likely to repeat? yes
- Suggested severity: medium
- Candidate owner: agents-os-hygiene-cycle (deuda de frontmatter bloquea reindex Graphify)
- Promote to L3 memory? defer

## One Next Improvement

- Modo detallado de cierre con rutas exactas de artefactos cuando el owner pide verificación explícita.
