---
type: index
scope: project
created: 2026-07-04
updated: 2026-07-04
area: "[[Personal]]"
project: "[[AGENTS OS]]"
entities:
  - "[[AGENTS OS]]"
  - "[[Aranea]]"
related:
  - "[[dashboard-hermes-agent]]"
  - "[[hermes-dashboard-systemd-source-of-truth]]"
  - "[[hermes-dashboard-reverse-proxy-websocket-origin]]"
aliases:
  - hermes dashboard recovery
  - recuperar dashboard hermes
confidence: verified
load_policy: when_project_loaded
indexable: true
index_priority: high
tags:
  - kind/index
  - tech/hermes
  - action/recovery
  - area/personal
  - project/agents-os
  - scope/agent
---

# Hermes Dashboard Recovery — puente (no es skill ni runbook canónico)

%% Nota-puente deliberada: nodo buscable que apunta a las dos fuentes de verdad reales.
No duplica procedimiento. Reclasificada desde una copia-skill (`80-agents/skills/`) el
2026-07-04 por ser un runbook vestido de skill + espejo de una skill externa. %%

Cuándo importa: dashboard del Hermes Agent caído o parcial (timeout / connection refused /
502 / `origin_mismatch` / chat WebSocket con `paths[0] undefined`), típicamente tras update
de Hermes (v0.17.0+).

## Dónde vive lo real

- **Procedimiento canónico** (diagnóstico por capas, smoke tests, tabla de rollback):
  [[dashboard-hermes-agent]] (`30-resources/aranea/02-servicios/`, `type: runbook`). **Fuente
  de verdad operativa del vault.**
- **Skill vivo invocable** (se actualiza por incidente, fuera del vault):
  `~/.hermes/profiles/ariadna/skills/devops/hermes-dashboard-bind-loopback-post-update/SKILL.md`.
- **Contexto de diseño:** learnings [[hermes-dashboard-systemd-source-of-truth]] y
  [[hermes-dashboard-reverse-proxy-websocket-origin]]; incidente en
  `80-agents/journal/sessions/2026-07-01-1130-hermes-dashboard-post-update-recovery-summary.md`.

## Por qué es un puente y no una skill

No se invoca como skill (la invocable es la externa) ni es el runbook canónico (ese vive en
resources). Existe solo como nodo buscable en el vault que enruta a las dos fuentes reales,
evitando una tercera copia del procedimiento (constitución: "una fuente canónica por hecho").
