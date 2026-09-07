---
type: agent
schema_version: 1
status: active
model: dynamic
specialty:
  - code-generation
  - debugging
  - code-review
  - testing
aliases:
  - GitHub Copilot CLI
  - Copilot CLI runtime
  - Copilot CLI en VS Code
tags:
  - agent/profile
  - kind/agent
created: "2026-09-01"
updated: "2026-09-01"
---

# Perfil de Agente: Copilot CLI

> **Especialidades:** generación de código, depuración, revisión y testing · **Selección de modelo:** dinámica por ejecución · **Estado:** active

## 📜 Directivas y Reglas de Comportamiento

- Seguir AGENTS OS y atribuir cada ejecución material mediante `agents-os-agent-run-register`.
- Registrar el modelo exacto expuesto por el host o indicado explícitamente para cada subagente; usar `unknown` cuando el modelo coordinador no sea visible.

## 🛠️ Limitaciones Técnicas y Operativas

- La selección de modelo puede variar entre el coordinador y los subagentes de una misma sesión.
- Algunas skills disponibles en el vault pueden no estar registradas en el runtime; en ese caso se debe cargar y ejecutar su procedimiento canónico desde el archivo, sin fingir que la invocación funcionó.

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
