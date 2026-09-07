---
type: doc
schema_version: 1
status: active
area: "[[Personal]]"
related:
  - "[[Codex]]"
  - "[[Claude Code]]"
  - "[[Cursor]]"
  - "[[Antigravity]]"
  - "[[Copilot CLI]]"
  - "[[ZCode]]"
aliases: []
tags:
  - kind/doc
created: 2026-08-10
updated: 2026-09-07
---

# Registro de la Tripulación (Crew Dashboard)

## Propósito

Registro canónico de superficies de generación de código y dashboard de performance por superficie×modelo.

## Contenido


Este directorio centraliza las superficies autorizadas para generar código en el Second Brain. La superficie es una entidad estable; el modelo es un atributo exacto y mutable de cada ejecución, no una entidad ni un valor base del perfil.

### Contrato de identidad

- **Superficies registradas:** [[Codex]], [[Claude Code]], [[Cursor]], [[Antigravity]], [[Copilot CLI]] y [[ZCode]].
- **Registro de ejecución:** `80-agents/journal/agent-runs/` mediante [[agents-os-agent-run-register]].
- **Clave de comparación:** `agent_surface × agent_model`; un cambio de cualquiera crea otro run atribuible.
- **Modelo:** identificador exacto reportado por el host o usuario; `unknown` si no existe evidencia, nunca inferido.
- **Evidencia primaria:** outcome, verificación y rework del usuario. Los scores 1–5 son secundarios y siempre declaran evaluator.
- **Historial:** los valores legacy en texto libre no se migran por heurística.

## 👥 Agentes Registrados

```dataview
TABLE 
    specialty as "Especialidades", 
    model as "Selección de modelo",
    status as "Estado"
FROM "80-agents/crew"
WHERE type = "agent"
```

## 📈 Desempeño Por Superficie × Modelo

Esta tabla consolida ejecuciones comparables. Las medias usan sólo scores presentes; outcome, verificación y rework deben revisarse antes de concluir que una combinación es mejor.

```dataview
TABLE WITHOUT ID
    key as "Superficie × modelo",
    length(rows) as "Runs",
    round(average(rows.score_correctness), 2) as "Correctness",
    round(average(rows.score_autonomy), 2) as "Autonomy",
    round(average(rows.score_efficiency), 2) as "Efficiency",
    round(average(rows.score_tool_use), 2) as "Tool use",
    round(average(rows.score_overall), 2) as "Overall"
FROM "80-agents/journal/agent-runs"
WHERE type = "agent_run"
GROUP BY string(agent_surface) + " × " + agent_model
SORT length(rows) DESC
```

## 📊 Evidencia Reciente

```dataview
TABLE
    agent_surface as "Superficie",
    agent_model as "Modelo",
    task_type as "Tipo",
    task_complexity as "Complejidad",
    outcome as "Outcome",
    verification as "Verificación",
    user_rework as "Rework",
    evaluator as "Evaluator"
FROM "80-agents/journal/agent-runs"
WHERE type = "agent_run"
SORT created DESC
LIMIT 50
```
