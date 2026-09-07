---
type: agent
schema_version: 1
status: active
specialty:
  - code-generation
  - debugging
  - code-review
model: dynamic
aliases:
  - Claude
  - claude-code
tags:
  - agent/profile
  - kind/agent
created: "2026-08-11"
updated: "2026-08-11"
---

# Perfil de Agente: Claude Code

> **Especialidades:** generación de código, depuración y revisión de código · **Selección de modelo:** dinámica por ejecución · **Estado:** active

## 📜 Directivas y Reglas de Comportamiento

- Seguir AGENTS OS y atribuir cada ejecución material mediante `agents-os-agent-run-register`.
- Registrar el identificador exacto del modelo expuesto por Claude Code; un cambio mediante `/model` abre otro run atribuible.

## 🛠️ Limitaciones Técnicas y Operativas

- La selección de modelo es dinámica y puede cambiar dentro de una sesión; el perfil no declara un modelo base.
- Si la superficie no expone el modelo, registrar `agent_model: unknown` y `model_source: unknown`.

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
