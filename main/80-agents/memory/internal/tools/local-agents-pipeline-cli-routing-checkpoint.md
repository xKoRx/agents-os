---
type: agent_memory
schema_version: 1
scope: tool
created: 2026-09-14
updated: 2026-09-14
area: "[[Personal]]"
project: "[[AGENTS OS]]"
application:
entities:
  - "[[local-agents-pipeline-cli]]"
related:
  - "[[zord-output-json-false-green-on-total-reviewer-failure]]"
aliases: []
confidence: high
memory_state: active
continuity_key: tool/local-agents-pipeline-cli/zord-routing
supersedes:
superseded_by:
load_policy: when_tool_loaded
indexable: true
index_priority: high
tags:
  - kind/agent-memory
  - scope/tool
  - tech/zord
---

# Continuidad de routing por Zord

## Continuidad

- En el checkout owner de `local-agents-pipeline-cli`, branch `feature/zords-technical-authoring`, hay cambios no committeados que agregan `execution.zord_overrides` con provider/model/reasoning por Zord, sin avanzar el cursor del pool para asignaciones explícitas.
- La configuración global enruta sólo `rjara-rio-impact` a `codex`, modelo `gpt-5.6-sol`, reasoning `medium`; su timeout quedó en 1.200 s y cada Zord se ejecuta una sola vez, sin retry automático. Los ocho budgets bundled y el global quedaron en USD 1,00 para Claude; Codex no aplica ese límite monetario.
- La rama local ahora hace fail-closed ante cualquier reviewer fallido: conserva errores en `--output-json`, emite `status: "BLOCKED"` y `failed_zords`, grita por `stderr` incluso con `--quiet`, omite síntesis parcial y retorna exit `2`. Tests completos: 37 suites/549 tests pass, 95,84% statements y 96,02% lines; build pass; lint 0 errores y 12 warnings preexistentes; `git diff --check` limpio.
- El Zord global inició correctamente con Sol/medium pero las dos mediciones anteriores agotaron 300 s; la segunda usó el diff exacto del PR #1126. Aún no existe una corrida end-to-end completada con el nuevo techo de 1.200 s.

## Señales de carga

- Cargar al retomar cambios, commit/release o diagnóstico de routing, provider, timeout y falso verde de Zord.
- No declarar el global operativo hasta observar `{ reviewer: "rjara-rio-impact", findings, summary }` y un resultado no vacío dentro de los 1.200 s.

## Próxima acción

- Ejecutar una corrida end-to-end con el nuevo timeout y medir duración/calidad; luego optimizar el retrieval de la knowledge library RIO antes de committear/publicar la rama si el owner lo decide.
