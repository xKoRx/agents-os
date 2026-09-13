---
type: learning
schema_version: 1
scope: global
created: "2026-09-12"
updated: "2026-09-12"
area: "[[Personal]]"
project: "[[AGENTS OS]]"
application:
entities:
  - "[[AGENTS OS]]"
related:
  - "[[delegacion-a-subagentes]]"
  - "[[zcode-docs-agent-factory-continuity]]"
aliases:
  - formato de subagents ZCode
  - frontmatter de custom agents
  - thoughtLevel y model ref de subagentes
confidence: verified
source_session: sesión ZCode 2026-09-12 (fábrica de subagents para campaña Echo + Echo Forge)
load_policy: manual
indexable: true
index_priority: high
tags:
  - kind/learning
  - scope/global
  - project/agents-os
  - tech/zcode
---

# zcode-custom-subagent-definition-format

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Aprendizaje

- Los custom subagents de ZCode (v3.11.2) son Markdown con frontmatter en `~/.zcode/agents/` (user scope) o `<repo>/.zcode/agents/` (project scope), parseados por `parseAgentProfileFromMarkdown`: campos válidos exactos `name` y `description` (requeridos), `model`, `thoughtLevel`, `color` (`red|blue|green|yellow|purple|orange|pink|cyan`), `permissionMode` (sólo se honra en user scope: `acceptEdits|auto|bypassPermissions|default|dontAsk|plan`), `maxTurns`, `memory` (`user|project|local`), `tools`, `disallowedTools`, `skills`, `background`, `injectAgentsMd`, `mcpServers`; el cuerpo del archivo es el system prompt.
- El model ref de subagente acepta aliases (`inherit|main|sonnet|opus|lite|haiku`) que resuelven dinámicamente, o un ref concreto `custom:<providerId>:<modelName>`; para fijar el pool promocional se usa `custom:builtin:zai-start-plan:GLM-5.3-Flash` (provider habilitado que expone ese modelo). Los overrides de agentes builtin viven en `~/.zcode/v2/agents-state.json` (`builtInModelOverrides`, `builtInThoughtLevelOverrides`, `disabledAgentIds`).
- El campo de reasoning en frontmatter se llama exactamente `thoughtLevel` y los valores válidos son los variants declarados en la config del provider (`~/.zcode/v2/config.json`): `low | high | max` para GLM-5.3/5.3-Flash.
- La guía oficial instalada (`zcode-configuration-guide`) documenta skills, commands, MCP, hooks y plugins, pero NO el formato de agents: ante dudas, la fuente es el parser dentro del bundle instalado (`/opt/ZCode/resources/glm/zcode.cjs`), no la documentación.
- Los perfiles se cargan al bootstrap de sesión: los archivos nuevos en `~/.zcode/agents/` no aparecen en el registry del Agent tool hasta una sesión/task nueva.

## Aplicabilidad

- **Cuándo cargarlo:** al crear, auditar o reparar custom subagents de ZCode, o al fijar modelo/thinking de una flota de agentes.
- **Cuándo no cargarlo:** para delegación conductual a subagentes ([[delegacion-a-subagentes]] cubre esa preocupación) o para skills/commands/MCP/hooks/plugins (eso lo cubre la guía instalada).

## Entidades relacionadas

- [[AGENTS OS]] — superficie de ejecución de la flota.

## Evidencia

%% Cita de fuente, NO prosa narrativa: link a sesión/log/archivo + una línea de qué la respalda. No re-parafrasear el aprendizaje ya destilado arriba (constitución: memorias compactas). %%

- Fuente: `/opt/ZCode/resources/glm/zcode.cjs` (v3.11.2, funciones `parseAgentProfileFromMarkdown`, `decodeCustomModelValue`, `resolveCo...`) — parser real del binario instalado.
- Fuente: `~/.zcode/cli/plugins/cache/zcode-plugins-official/document-skills/0.1.4/agents/judge.md` — agente existente de referencia con el formato en producción.
- Fuente: `~/.zcode/v2/config.json` y `~/.zcode/v2/agents-state.json` — variants de reasoning y formato de model ref en uso.
- Fuente: `~/.zcode/agents/*.md` (10 archivos validados 2026-09-12 con script contra las reglas del parser) — materialización verificada.
