---
type: agent
schema_version: 1
status: active
specialty:
  - research
  - planning
  - docs
  - code-generation
  - debugging
  - code-review
  - ops
model: dynamic
aliases:
  - chatgpt
  - OpenAI ChatGPT
tags:
  - agent/profile
  - kind/agent
created: "2026-09-07"
updated: "2026-09-07"
entities:
  - "[[AGENTS OS]]"
---

# Perfil de Agente: ChatGPT

> **Especialidades:** investigación, planificación, documentación, generación y revisión de código, depuración y operaciones · **Selección de modelo:** dinámica por ejecución · **Estado:** active

## 📜 Directivas y Reglas de Comportamiento

- Seguir AGENTS OS desde el `AGENTS.md` del repo y su bootstrap canónico; no sustituirlo por una lectura amplia del vault.
- Para todo registro atribuible cuyo schema soporte identidad de superficie/modelo, usar `agent_surface: "[[ChatGPT]]"` y registrar el identificador exacto del modelo expuesto por el host para esa ejecución o feedback.
- El perfil representa la superficie estable ChatGPT, no un modelo concreto. Nunca inferir ni reutilizar un modelo histórico como valor actual.
- Mantener una sola autoridad por hecho, recuperar contexto por suficiencia y verificar estado durable antes de declarar efectos o cierres.

## 🛠️ Limitaciones Técnicas y Operativas

- La selección de modelo y configuración puede variar entre sesiones; `model: dynamic` es deliberado.
- ChatGPT no tiene acceso implícito al filesystem ni a procesos del host del usuario: debe usar las superficies y conectores disponibles y no afirmar validaciones locales que no ejecutó.
- Graphify es estado local por máquina y no se obtiene desde GitHub; cuando no esté expuesto como herramienta, el retrieval remoto debe degradar explícitamente a búsqueda/fetch enfocado sobre Markdown canónico.

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
