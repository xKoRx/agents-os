---
type: agent_memory
scope: project
tags:
  - tech/agents-os
  - tech/graphify
  - project/agents-os
  - kind/learning
created: 2026-07-08
updated: 2026-09-09
index_priority: never
indexable: false
load_policy: manual
memory_state: archived
aliases:
  - Vibe Coding Migration and Graphify Learning
---

# Continuidad Operativa: Uso Obligatorio de Graphify y Migración de Vibe Coding

Esta memoria documenta una lección y corrección crítica de comportamiento de la sesión del 2026-07-08 para guiar la continuidad operativa de futuras IAs en este Workspace.

## Regla de Oro Violada (Corrección del Usuario)
* **El Error**: Inicié la sesión haciendo búsquedas manuales del sistema (`find`, `grep_search`, `list_dir`) para buscar archivos de "vibe-coding" en lugar de utilizar **Graphify** primero.
* **La Regla (rjara-agent-profile.md)**:
  * > "Usar obligatoriamente el CLI `graphify-*` (obsidian/personal/work) como retrieval primario antes de usar búsquedas manuales (find/grep/list_dir)."
* **Criterio para futuros agentes**: NUNCA saltes esta regla. La primera acción de búsqueda debe ser siempre a través del CLI de Graphify correspondiente.


## Estado Final de la Tarea de Vibe Coding
1. **Documentación Migrada**: Creamos el dominio `30-resources/vibe-coding/` en el Vault con toda la documentación V2 consolidada:
   - `00-index.md` (Índice catálogo)
   - `log.md` (Bitácora cronológica)
   - `context-v2.md` (Pilar 1 - Gestión de contexto)
   - `agents-v2.md` (Pilar 2 - Operación multi-agente)
   - `prompts-v2.md` (Pilar 3 - Flow engineering)
   - `rules-toon.md` (Pilar 4 - Reglas y migración TOON)
   - `config.toon` (Archivo de configuración TOON listo para replicar)
   - `sdd-prompts-pack-v4.md` (Pack de prompts de Spec-Driven Development v4)
2. **Registro de Dominio**: Registrado en `30-resources/00-RESOURCE-WIKI.md`.
3. **Indexación Ejecutada**:
   - Actualizamos los grafos de desarrollo en `symphony`, `echo`, `sdk` y `java-polycard-sdk` mediante `graphify-personal update`.
   - Re-indexamos el grafo completo de Obsidian mediante `graphify-obsidian update`.
