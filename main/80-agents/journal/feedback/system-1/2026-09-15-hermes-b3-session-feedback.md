---
type: feedback
schema_version: 1
scope: session
created: "2026-09-15"
updated: "2026-09-15"
area: "[[Aranea]]"
project: "[[HERMES — Bootstrap & Self-Sufficiency]]"
entities:
  - "[[HERMES — Bootstrap & Self-Sufficiency]]"
  - "[[AGENT-PLATFORM - MCP Access Plane]]"
related:
  - "[[aranea-mcp-plane-operator]]"
aliases: []
agent_surface: "[[Ariadna]]"
agent_model: glm-5.3-flash (Hermes Agent / zai)
agent_run:
session_goal: B3.1 skill operador MCP plane + B3.2 golden self-repair DEV end-to-end
source_session:
confidence: high
load_policy: manual
indexable: false
index_priority: low
tags:
  - kind/feedback
  - scope/session
  - area/aranea
  - agent/system1
---

# Session Feedback - 2026-09-15 - hermes b3 golden repair

## Context

- Agent surface: [[Ariadna]] (Hermes Agent TUI)
- Agent model: glm-5.3-flash (Hermes Agent / zai)
- Agent run: no material code-generation segment; sólo scripts de smoke desechables en /tmp
- Session goal: B3.1 skill operador + B3.2 golden repair DEV
- Main entity: [[HERMES — Bootstrap & Self-Sufficiency]]
- Skills used: [[aranea-mcps-expert]] (boundary), agents-os-skill-authoring + runbook, [[mcp-access-plane-operations]] (Hermes), agents-os-session-close
- Retrieval mode: find directo + lectura de notas canónicas
- Artifacts changed: SKILL.md nueva, change_log, nota de proyecto, esta nota

## Scores

- Startup clarity: 5
- Retrieval usefulness: 4
- Skill fit: 5
- Template fit: 4
- Closeout friction: 4
- Overall confidence: 5

## What Complicated The Session Most

- Observation: `skill_view` del runtime Hermes no resuelve las skills del vault Agents-OS (sólo skills del perfil Hermes); las skills canónicas se leyeron por path directo.
- Why it was hard: doble naming space (perfil Hermes vs vault) confunde al inicio de sesión.
- Proposed improvement: un índice puente en el bootstrap que mapee triggers de skills del vault a paths.

## Most Useful Part Of Sistema 1

- What helped: materialize_schema_note.py + validate + lint strict deterministas.
- Why it helped: cero ambigüedad de frontmatter; PASS/FAIL objetivo.
- Keep/change: keep.

## Least Useful Or Noisy Part

- What did not help: template de feedback asume superficie Codex y campos genéricos.
- Why it was weak/noisy: requiere edición de metadatos por defecto en cada uso.
- Proposed cleanup: default `agent_surface`/`area` por variable de perfil.

## Missing Support

- Problem not solved by Sistema 1: smoke scripts MCP desechables se reescriben desde cero cada sesión (B2 los dejó durables en Daedalus, pero el server-side de mcps es throwaway en /tmp).
- How Sistema 1 could help next time: un script de smoke server-side duradero por familia o en el skill package.
- Suggested artifact type: recurso ejecutable referenciado por [[aranea-mcp-plane-operator]].

## Retrieval Feedback

- Useful query or source: find por nombre de archivo; runbook capability-plane.
- Missing context: ninguna material.
- Duplicate/noisy result: n/a.
- Better future query: n/a.

## Skill Feedback

- Skill that worked well: [[mcp-access-plane-operations]] (gotchas scp/sudo-find exactos y correctos).
- Skill that was confusing: n/a.
- Trigger/routing gap: skill_view Hermes vs skills vault (ver arriba).
- Suggested contract change: ninguno.

## Template Feedback

- Template used: skill.md + change-log.md + session-feedback.md.
- Field that helped: load_policy/index_priority consistentes.
- Field that felt redundant: agent_surface default fijo.
- Missing field: n/a.

## Memoria Interna (Internal Memory)

- ¿Consultaste la memoria interna al iniciar? no — bootstrap cold se resolvió con prompt de sesión + nota de proyecto.
- ¿Qué valor operativo aportó? n/a esta sesión.
- ¿Dejaste mensaje para el próximo agente? no; el delta durable quedó en la nota de proyecto y change_log.
- Utilidad del espacio privado (1-5): 4.

## Pain Pattern Candidate

- Is this likely to repeat? yes
- Suggested severity: low
- Candidate owner: [[aranea-mcp-plane-operator]] (smoke server-side re-escrito por sesión)
- Promote to L3 memory? defer — recién si B3.3/B4 lo confirman repetitivo.

## One Next Improvement

- Dotar al operador de un smoke script server-side duradero (mcps:/opt o skill assets) para eliminar la reescritura por sesión.

## Context Efficiency

- context_high_water_mark: unknown
- main_context_growth_sources: lecturas de notas canónicas (proyecto 26KB, arquitectura 15KB); outputs de docker inspect.
- avoidable_context_growth: una re-lectura del proyecto completo donde bastaba la sección B3.
- compaction_opportunity: sí — tras cerrar B3.2 antes de escribir artefactos.
- efficiency_assessment: GOOD
