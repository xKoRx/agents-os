---
type: agent
schema_version: 1
status: active
specialty:
  - code-generation
  - debugging
  - code-review
  - testing
model: dynamic
aliases:
  - zcode
  - ZCode coding agent
tags:
  - agent/profile
  - kind/agent
created: "2026-08-14"
updated: "2026-08-14"
entities:
  - "[[AGENTS OS]]"
related:
  - "[[Codex]]"
  - "[[Claude Code]]"
  - "[[Cursor]]"
  - "[[Antigravity]]"
---

# Perfil de Agente: ZCode

> **Especialidades:** generación de código, depuración, revisión y testing · **Selección de modelo:** dinámica por ejecución · **Estado:** active

## 📜 Directivas y Reglas de Comportamiento

- Seguir AGENTS OS (bootstrap vía AGENTS.md) y atribuir cada ejecución material mediante `agents-os-agent-run-register`.
- Registrar el identificador exacto del modelo reportado por el host (p. ej. `builtin:zai-coding-plan/GLM-5.3`); no abreviar ni traducir.

## 🛠️ Limitaciones Técnicas y Operativas

- La selección de modelo es dinámica; el perfil no declara un modelo base.
- Si el host no expone el modelo, registrar `agent_model: unknown` y `model_source: unknown`.

## 📊 Historial de Desempeño

```dataview
TABLE
    agent_model as "Modelo",
    task_type as "Tipo",
    outcome as "Outcome",
    verification as "Verificación",
    user_rework as "Rework",
    score_overall as "Score"
FROM "80-agents/journal/agent-runs"
WHERE type = "agent_run" AND agent_surface = this.file.link
SORT created DESC
```
