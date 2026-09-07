---
type: feedback
schema_version: 1
scope: graphify
created: 2026-08-11
updated: 2026-08-11
area: "[[Personal]]"
project: "[[AGENTS OS]]"
entities:
  - "[[AGENTS OS]]"
  - "[[graphify]]"
related:
  - "[[agents-os-graphify-install]]"
aliases: []
agent: Codex
session_goal: Regularizar bundles globales de Graphify y cerrar AGENTS OS con estado exacto.
source_session:
confidence: high
load_policy: manual
indexable: false
index_priority: low
tags:
  - kind/feedback
  - scope/graphify
  - project/agents-os
  - agent/system1
---

# Graphify Feedback — El instalador global de Gemini escribe hooks locales

## Context

- **Entidad:** [[AGENTS OS]].
- **Operación:** sincronizar bundles globales Copilot, Antigravity y Gemini con Graphify `0.9.6.post2`.
- **Resultado:** bundles alineados y warning eliminado; reindex/retrieval sin degradación.

## What Complicated The Session Most

- **Observación:** `graphify install --platform gemini` instaló correctamente el bundle global, pero también creó `GEMINI.md` y `.gemini/settings.json` en el directorio actual.
- **Riesgo:** una regularización global puede contaminar un proyecto o vault con hooks locales no solicitados.
- **Mitigación aplicada:** inspección inmediata y movimiento de ambos artefactos a la Papelera; el bundle global se conservó.

## Missing Support

- **Gap:** el CLI no distingue claramente instalación global del bundle y registro de hooks en el proyecto actual para Gemini.
- **Mejora propuesta:** agregar un modo global sin efectos project-local o exigir `--project` para escribir `GEMINI.md`/`.gemini/settings.json`; mientras tanto, ejecutar desde un directorio temporal seguro o auditar los side effects inmediatamente.

## Pain Pattern Candidate

- **Repetible:** sí.
- **Severidad:** medium.
- **Owner candidato:** Graphify installer.
- **Promoción a L3:** defer; promover si reaparece o se incorpora mantenimiento periódico de bundles.

## One Next Improvement

- Incorporar este caso al próximo ciclo de higiene/Kaizen y decidir si requiere known error o ajuste de runbook.
