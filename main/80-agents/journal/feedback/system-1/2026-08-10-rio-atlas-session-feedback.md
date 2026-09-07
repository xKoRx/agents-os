---
type: feedback
schema_version: 1
scope: session
created: 2026-08-10
updated: 2026-08-10
area: "[[Personal]]"
project: "[[AGENTS OS]]"
entities:
  - "[[AGENTS OS]]"
related:
  - "[[Onboarding Signals]]"
  - "[[AGENTS OS - Fase 3]]"
aliases: []
agent: claude-opus-4-8
session_goal: Onboarding Signals — construir RIO Atlas (System Map + Integration Map generado)
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

# Session Feedback - 2026-08-10 - rio-atlas

## Context

- Agent: claude-opus-4-8
- Session goal: RIO Atlas (System Map + Integration Map generado por `rio-inspector`)
- Main entity: [[RIO]] / [[Onboarding Signals]]
- Skills used: agents-os-bootstrap; NO se usó agents-os-entity-lifecycle (ese fue el error)
- Artifacts changed: `rio-atlas/` (3 notas), [[RIO]] corregida, control doc, `~/fuentes/rio-inspector`

## What Complicated The Session Most

- Observation: creé 3 notas en `30-resources/rio-atlas/` escribiendo frontmatter a mano e inventé `type: reference` (inexistente en el contrato); el gate las frenó antes del reindex.
- Why it was hard: al construir documentación derivada dentro de un flujo de trabajo (Atlas + generador `rio-inspector`) salté el flujo canónico de creación sin darme cuenta; el contrato correcto era `resource` (system-map/integration-map) e `index` conforme (00-index).
- Proposed improvement: hacer obligatorio `materialize_schema_note.py` + `lint.py --strict` DENTRO de los flujos que emiten Markdown (agente y generadores como `rio-inspector`), no sólo en el reindex.

## Missing Support

- Problem not solved by Sistema 1: el contrato+gate DETECTA el drift fail-closed (funcionó), pero no fuerza la validación en el punto de creación de flujos/herramientas externas → el generador reintroduciría frontmatter no conforme en cada corrida.
- How Sistema 1 could help next time: shift-left del gate; `agents-os-entity-lifecycle` ya ordena el flujo, falta exigirlo en estos casos.
- Suggested artifact type: idea (ya registrada en [[AGENTS OS - Fase 3]]); tarea de remediación en [[Onboarding Signals]].

## Pain Pattern Candidate

- Is this likely to repeat? yes (siempre que un flujo/generador produzca notas)
- Suggested severity: medium
- Candidate owner: AGENTS OS (Fase 3)
- Promote to L3 memory? defer (idea ya capturada; promover si reaparece)

## One Next Improvement

- Antes de escribir cualquier nota canónica desde un flujo de construcción, pasar por `materialize_schema_note.py` y `lint --strict`; nunca frontmatter a mano ni tipos inventados.
