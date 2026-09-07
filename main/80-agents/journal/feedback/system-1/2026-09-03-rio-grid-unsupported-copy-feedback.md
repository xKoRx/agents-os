---
type: feedback
schema_version: 1
scope: session
created: 2026-09-03
updated: 2026-09-03
area: "[[Meli]]"
project: "[[Estandarización de Scopes RIO]]"
entities:
  - "[[RIO]]"
related:
  - "[[2026-09-03-rio-scope-grid-v3-reconciliation]]"
aliases: []
agent_surface: "[[Copilot CLI]]"
agent_model: unknown
agent_run: "[[2026-09-03-copilot-cli-unknown-rio-scope-grid-v3]]"
session_goal: "Corregir y publicar el Grid de scopes RIO alineado estrictamente con SIG-599"
source_session: "copilotcli:/5b927834-436d-4b97-b477-a57d55119950"
confidence: high
load_policy: manual
indexable: false
index_priority: low
tags:
  - kind/feedback
  - scope/session
  - project/scopes-rio
  - agent/system1
---

# Session Feedback — RIO Grid unsupported copy

## Context

- Agent surface: [[Copilot CLI]]
- Agent model: unknown
- Agent run: [[2026-09-03-copilot-cli-unknown-rio-scope-grid-v3]]
- Session goal: corregir y publicar el Grid de scopes RIO alineado estrictamente con SIG-599.
- Main entity: [[Estandarización de Scopes RIO]]
- Artifacts changed: generador, contrato funcional, HTML/Markdown derivados y documento Grid remoto.

## What Complicated The Session Most

- Observation: el Grid agregó una instrucción que pedía confirmaciones a “cada equipo”, mostró una rotulación editorial de versión, usó un enlace no canónico de SIG-599 y publicó un formato backend incompleto; luego Spellbook ocultó los placeholders crudos con `<…>` al interpretarlos como tags HTML.
- Why it was hard: se transformó incorrectamente una regla descriptiva (“depende de las necesidades”) en una acción asignada a actores que el usuario no había nombrado.
- Proposed improvement: validar toda frase imperativa y cada patrón de naming contra la SPEC o una instrucción literal del usuario; mantener el versionado técnico fuera del contenido publicado; fijar la URL y el formato backend canónicos en un gate; escapar los placeholders angulares antes de publicar en Spellbook.

## Pain Pattern Candidate

- Is this likely to repeat? yes
- Suggested severity: high
- Candidate owner: agent
- Promote to L3 memory? no; el gate quedó implementado en el generador.

## One Next Improvement

- No convertir descripciones funcionales en tareas para equipos o personas si la fuente no las asigna explícitamente.
