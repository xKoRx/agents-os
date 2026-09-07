---
type: feedback
scope: session
created: 2026-07-03
updated: 2026-07-03
area: "[[Personal]]"
project: "[[AGENTS OS]]"
entities:
  - "[[AGENTS OS]]"
related:
  - "[[Economía de Tokens]]"
aliases: []
agent: Claude
session_goal: Diseñar sistema de indexación óptimo en tokens (LLM Wiki + Graphify + Context Router)
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

# Session Feedback - 2026-07-03 - economía de tokens / indexación

## Context

- Agent: Claude
- Session goal: LLM Wiki en resources + evaluar Graphify + diseñar Context Router
- Main entity: [[Economía de Tokens]] / [[AGENTS OS]]
- Skills used: bootstrap, resource-wiki, skill-authoring (creadas), graphify-maintenance
- Retrieval mode: Graphify (degradado) + grep + lectura directa
- Artifacts changed: ADR, concepto, proyecto, 2 skills, runbook, constitución, contrato, piloto

## Scores

- Startup clarity: 5
- Retrieval usefulness: 2 (Graphify semántico no confiable en markdown)
- Skill fit: 4
- Template fit: 4
- Closeout friction: 3
- Overall confidence: 4

## What Complicated The Session Most

- Observation: perseguir la capa semántica de Graphify (ollama, Gemini) fue un pozo.
- Why it was hard: doc `graphify.md` desactualizada (`--mode deep` mal), free tier insuficiente, reasoning model rompe JSON. Un comando inventado borró el grafo.
- Proposed improvement: verificar el CLI real ANTES de recomendar; no tocar `graph.json` sin rebuild que lo regenere.

## Most Useful Part Of Sistema 1

- What helped: constitución (frontera skill/runbook/memoria, "una fuente por hecho") y el patrón wiki de aranea como referencia.

## Least Useful Or Noisy Part

- What did not help: la doc de Graphify tenía datos falsos; me indujo a error.
- Proposed cleanup: ya corregida (`graphify.md`), pero conviene la auditoría de consistencia doc↔realidad.

## Missing Support

- Problem not solved: no hay builder de wikilinks → grafo del vault sin relaciones.
- Suggested artifact type: skill/tool builder (tarea en el proyecto).

## Retrieval Feedback

- Useful query: `explain`/`affected` con nombre canónico (para código funciona muy bien).
- Duplicate/noisy: queries genéricas y corpus con trash/json (ya purgado).

## Skill Feedback

- Worked well: resource-wiki, skill-authoring.
- Trigger gap: faltaba una skill de retrieval que encode el Context Router (tarea pendiente).

## Template Feedback

- Template used: project, idea, decision, known-error, session-*. Buenos.

## Memoria Interna

- ¿Consultaste memoria interna al iniciar? sí.
- Valor: continuidad de AGENTS OS y stance "no cargar Nexus/MELI".
- ¿Dejaste mensajes para el próximo agente? sí: hallazgo de wikilinks, decisión indices-only, no reintentar extract sin billing.
- Utilidad del espacio privado (1-5): 5.

## Pain Pattern Candidate

- Repeat? yes
- Severity: medium
- Promote to L3? done (known-error de Graphify creado).

## One Next Improvement

- Auditoría de consistencia entre la doc de AGENTS OS y los artefactos (definir A / hacer A).
