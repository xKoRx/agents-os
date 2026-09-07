---
type: agent_memory
schema_version: 1
scope: global
created: 2026-06-27
updated: 2026-09-03
area: "[[Personal]]"
project: "[[AGENTS OS]]"
entities:
  - "[[AGENTS OS]]"
related:
  - "[[agent-constitution]]"
aliases: []
confidence: high
memory_state: active
continuity_key: global/agents-os-operating-continuity
supersedes: "[[agents-os-operating-continuity-archive]]"
load_policy: always
indexable: true
index_priority: critical
tags:
  - agent/alwaysload
  - agent/internal
  - kind/agent-memory
  - project/agents-os
  - scope/global
---

# AGENTS OS Operating Continuity

## Continuidad

- Ante un retry, timeout o resultado incierto, leer primero el estado durable y no repetir efectos laterales hasta demostrar que la operación anterior no ocurrió.
- Resolver identidad desde la autoridad canónica; nombres de archivo, paths, timestamps, etiquetas y claves de transporte son señales de routing, no identidad de negocio.
- Un comando verde, un mock o un estado lógico terminal no prueban por sí solos el resultado real: verificar el outcome en la capa que posee la semántica y, cuando corresponda, la identidad exacta del artefacto o runtime.
- Antes de reutilizar recursos o declarar cierre, comprobar que los efectos físicos y procesos dependientes terminaron; terminalidad lógica y drenaje físico son contratos distintos.
- Preservar cambios ajenos, separar baseline de delta y fallar cerrado cuando la evidencia vigente contradiga el estado esperado.
- Los índices derivados, caches, historiales y binarios de Graphify son estado
  local por máquina: nunca guardarlos ni sincronizarlos dentro del vault. Las
  queries de `graphify-obsidian` resuelven y refrescan ese estado automáticamente.

## Señales de carga

- Esta nota contiene sólo comportamientos transferibles. Estado, releases, hashes, incidentes, tareas y próximos pasos de un dominio se recuperan por entidad mediante Context Retrieval.
- Cargar sólo en cold start. En turnos warm se reutiliza la base y se obtiene únicamente el delta requerido por la pregunta.
