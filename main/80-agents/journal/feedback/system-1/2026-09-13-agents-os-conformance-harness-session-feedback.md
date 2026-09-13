---
type: feedback
schema_version: 1
scope: session
created: 2026-09-13
updated: 2026-09-13
area: "[[Personal]]"
project: "[[AGENTS OS]]"
entities:
  - "[[AGENTS OS]]"
related: []
aliases: []
agent_surface: "[[ZCode]]"
agent_model: builtin:zai-start-plan/GLM-5.3-Flash
agent_run: "[[2026-09-13-zcode-glm-5-3-flash-conformance-harness]]"
session_goal: Implementar el AGENTS OS Conformance Harness (bootstrap/cold/warm/switch/isolation/skills/MCP/deprecated) con evidencia reproducible
source_session: sess_8c7d3b7a-0c03-407d-be50-724cf2b06d6e
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

# Session Feedback - 2026-09-13 - agents-os-conformance-harness

## Context

- Agent surface: [[ZCode]]
- Agent model: builtin:zai-start-plan/GLM-5.3-Flash (identificador reportado por el host)
- Agent run: [[2026-09-13-zcode-glm-5-3-flash-conformance-harness]]
- Session goal: conformance harness para Agents-OS con audits A/B/C, spec, implementación y verificación adversarial
- Main entity: [[AGENTS OS]]
- Skills used: agents-os-bootstrap, agents-os-agent-project-workflow, agents-os-agent-run-register, agents-os-session-close, agents-os-session-feedback
- Retrieval mode: lecturas directas + grep enfocado; Graphify no fue necesario (fixtures conocidos por ruta canónica)
- Artifacts changed: proyecto `[[AGENTS OS - Conformance Harness]]`, harness en `80-agents/tools/conformance-harness/`, agent_run y esta feedback; sin L0/L1 (sin transcript disponible ni pedido de placeholder)

## Scores

- Startup clarity: 5
- Retrieval usefulness: 4
- Skill fit: 5
- Template fit: 4
- Closeout friction: 4
- Overall confidence: 5

## What Complicated The Session Most

- Observation: los lanzamientos paralelos de subagents en background fallaron 3 veces con "user concurrency limit exceeded" antes de ejecutarse; hubo que serializar A→B→C y usar modo síncrono.
- Why it was hard: el mandato pedía A/B/C en paralelo y el entorno lo impide; cada reintento gastó un turno y una notificación de fallo.
- Proposed improvement: que la superficie exponga el límite de concurrencia real o una cola de subagents, para no descubrirlo por fallo.

## Most Useful Part Of Sistema 1

- What helped: bootstrap + constitución como autoridades únicas y el materializador canónico.
- Why it helped: la extracción de contratos fue determinista (cada regla citable) y las notas canónicas nacieron sin frontmatter manual.
- Keep/change: mantener; el par skill-canónica/materializador es el que hizo testeable el sistema.

## Least Useful Or Noisy Part

- What did not help: el auto-sync del vault commitea cada minuto; el HEAD se movió 4+ veces durante la sesión y los commits del harness quedaron mezclados con sync.
- Why it was weak/noisy: complica el tracking de baseline y la atribución de cambios en un proyecto de agente.
- Proposed cleanup: ventana de gracia del auto-sync mientras hay sesión activa, o exclusión de `80-agents/tools/` en progreso.

## Missing Support

- Problem not solved by Sistema 1: no existe observabilidad runtime de qué contextos/skills cargó un agente real (OBSERVABILITY GAPS de los audits); el harness sólo pudo replicar decisiones y auto-reportes.
- How Sistema 1 could help next time: un registro ligero de cargas por sesión (opt-in, agnóstico a superficie) haría testeables los contratos C02/C06/C07 en vivo.
- Suggested artifact type: runbook + campo en journal de sesión; no memoria always.

## Retrieval Feedback

- Useful query or source: grep de frontmatter (`load_policy`, `area`, `memory_state`) sobre `80-agents/memory/` — la base del L0.
- Missing context: nada material; los fixtures estaban donde las autoridades los declaran.
- Duplicate/noisy result: los grep whole-vault necesitan excluir siempre `40-archive/`, journal y packaging (`30-resources/agents-os/`); sin eso el club cerrado da falsos positivos.
- Better future query: un grep helper canónico con las exclusiones de doctor Check 1 evitaría re-inventarlas por sesión.

## Skill Feedback

- Skill that worked well: agents-os-bootstrap (el domain gate y el cold set estaban completamente especificados) y agents-os-agent-project-workflow (la nota como planificador único sostuvo toda la sesión).
- Skill that was confusing: ninguna materialmente; `agents-os-doctor` es lazy manual y la suite debió duplicar sus checks 3/4/7/8 como gates autónomos (overlap declarado en los artifacts).
- Trigger/routing gap: no hubo routing ambiguo; la sesión era [[AGENTS OS]] → sin domain router, correcto.
- Suggested contract change: none.

## Template Feedback

- Template used: project, agent_run, feedback (vía materializador).
- Field that helped: `agent_model` + `model_source: host` distinguieron el identificador exacto sin inferencia.
- Field that felt redundant: none.
- Missing field: en `agent_run`, un campo `subagent_provenance` opcional ayudaría a atribuir segmentos ejecutados por subagents de la misma superficie×modelo.

## Memoria Interna (Internal Memory)

- ¿Consultaste la memoria interna (`80-agents/memory/internal/`) al iniciar? sí (nota global always del cold start).
- ¿Qué valor operativo aportó para esta sesión (continuidad, detalles crudos, advertencias)? moderado: los comportamientos transferibles (verificar outcome en la capa dueña de la semántica, preservar cambios ajenos, fallar cerrado) se aplicaron literalmente en el diseño del harness.
- ¿Dejaste algún mensaje, instrucción o hipótesis para el próximo agente en la memoria interna? no — el estado durable quedó en la nota del proyecto, que es el planificador único; sin delta interno que justifique escritura.
- ¿Qué tan útil te resulta tener este espacio privado fuera de la vista directa del usuario (1-5) y cómo podemos mejorar su utilidad? 4; ya está bien enfocado tras la compaction de 2026-09-03.

## Pain Pattern Candidate

- Is this likely to repeat? yes
- Suggested severity: medium
- Candidate owner: superficie ZCode (no Sistema 1)
- Promote to L3 memory? defer — es una limitación del entorno de ejecución, no del vault; registrarla como L3 sería mezclar capas.

## One Next Improvement

- Resolver F1 (validador de schema en rojo por `agents-os-skill-authoring` como entrypoint sin materializador) para que el gate L0 del harness quede verde y la suite completa deje de cortar en L0.
