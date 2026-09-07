---
type: agent
schema_version: 1
status: active
specialty: []
model: dynamic
aliases: []
tags:
  - agent/profile
  - kind/agent
created: "{{date:YYYY-MM-DD}}"
updated: "{{date:YYYY-MM-DD}}"
---

# Perfil de Agente: {{title}}

> **Especialidades:** `specialty` · **Selección de modelo:** dinámica por ejecución · **Estado:** `status`

## 📜 Directivas y Reglas de Comportamiento

- [Directivas específicas de personalidad o comportamiento en interacciones]
- [Parámetros de respuesta o restricciones de idioma]

## 🛠️ Limitaciones Técnicas y Operativas

- [Limitaciones de contexto, tokens o herramientas del modelo]
- [Patrones de error conocidos u operaciones a evitar]

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
