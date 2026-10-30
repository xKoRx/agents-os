---
type: agent
schema_version: 1
status: active
specialty:
  - code-generation
  - implementation
  - debugging
  - code-review
  - exploration
  - documentation
model: "MiniMax-M3.1-Flash"
aliases:
  - minimax m3.1 flash
  - MiniMax-M3.1-Flash
  - minimax/MiniMax-M3.1-Flash
tags:
  - agent/profile
  - kind/agent
created: "2026-10-30"
updated: "2026-10-30"
entities:
  - "[[AGENTS OS]]"
related:
  - "[[ZCode]]"
  - "[[Codex]]"
  - "[[Claude Code]]"
  - "[[Cursor]]"
  - "[[Antigravity]]"
  - "[[Copilot CLI]]"
  - "[[ChatGPT]]"
---

# Perfil de Agente: MiniMax M3.1 Flash

> **Especialidades:** generación de código, implementación, depuración, revisión de código, exploración y documentación · **Modelo Base:** MiniMax-M3.1-Flash · **Estado:** active

## 📜 Directivas y Reglas de Comportamiento

- Seguir AGENTS OS (bootstrap vía `AGENTS.md`) y atribuir cada ejecución material mediante [[agents-os-agent-run-register]].
- Registrar el identificador exacto del modelo reportado por el host (`minimax/MiniMax-M3.1-Flash`); no abreviar, traducir ni inferirlo desde la superficie.
- El perfil declara un modelo base fijo: `MiniMax-M3.1-Flash`. No sustituirlo por un modelo histórico ni por un valor de otro perfil.
- Cuando el modelo opere dentro de otra superficie —por ejemplo [[ZCode]]— la atribución es de esa superficie: `agent_surface: "[[ZCode]]"` y `agent_model: minimax/MiniMax-M3.1-Flash`. Este perfil aplica cuando MiniMax M3.1 Flash se usa como superficie propia.
- Mantener una sola autoridad por hecho y verificar el estado durable antes de declarar efectos o cierres.

## 🛠️ Limitaciones Técnicas y Operativas

- El plan de tokens de MiniMax ya bloqueó el despacho de subagentes con `Token Plan usage limit reached (2056)` en Echo Forge F-03, F-04 y en la sesión mt5-ownership, con el modelo MiniMax-M3. Es una fricción conocida de la familia y no está verificada para M3.1 Flash: si el host no puede despachar, ejecutar el trabajo directamente y registrar la fricción en vez de re-decidirlo cada sesión.
- A diferencia de [[Codex]] o [[ZCode]], la selección de modelo no es dinámica: este perfil no declara `model: dynamic`.
- Si el host no expone el modelo, registrar `agent_model: unknown` y `model_source: unknown`.
- Graphify es estado local por máquina: no se persiste ni se sincroniza dentro del vault.

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
