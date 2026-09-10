---
type: doc
schema_version: 1
status: active
tags:
  - kind/doc
  - kind/system
  - tech/agents-os
created: 2026-06-27
updated: 2026-09-03
aliases:
  - Agent Memory System
---

# Agent Memory System — Guía Operativa

## Propósito

AGENTS OS convierte trabajo con agentes en conocimiento Markdown recuperable con el menor contexto suficiente. Este archivo es un mapa; no ejecuta ni duplica procedimientos.

## Contenido

### Fuentes Canónicas

| Responsabilidad | Fuente |
|---|---|
| Startup cold/warm/cambio de entidad | `80-agents/skills/agents-os-bootstrap/SKILL.md` |
| Invariantes | `80-agents/agents-os/agent-constitution.md` |
| Preferencias globales | la única nota always-load bajo `80-agents/memory/public/user-preference/` |
| Retrieval | `80-agents/skills/agents-os-context-retrieval/SKILL.md` |
| Modelo conceptual de retrieval (no ejecutable) | `80-agents/agents-os/context-router.md` |
| Cierre explícito | `80-agents/skills/agents-os-session-close/SKILL.md` |
| Metadata y tipos | `80-agents/skills/_shared/` |
| Estado y roadmap | `10-projects/Personal/AGENTS OS/AGENTS OS.md` |

Markdown es fuente de verdad; Graphify es índice derivado. Journal, snapshots
y packs generados son auditoría o distribución, nunca autoridad vigente.
Todas las rutas de esta guía son relativas a `VAULT_ROOT`; las rutas absolutas
de una máquina no forman parte del contrato.

## Modelo

- **Sistema 1:** skills, memoria pública/interna, decisiones, known errors,
  runbooks y journal.
- **Sistema 2:** proyectos, áreas, aplicaciones, servicios, tecnologías y
  demás entidades reales.

Sistema 2 se crea desde `70-templates/`. Sistema 1 usa
`80-agents/templates/` cuando corresponde. Una fuente por hecho; enlazar en
vez de repetir.

## Contexto Y Skills

Bootstrap clasifica cold/warm/cambio de entidad. Context Retrieval elige la
capa más barata relevante para la intención y escala solo ante insuficiencia:

```text
metadata/tags → índice curado → grafo → cuerpo seleccionado
```

Core always-load: constitución, perfil global, bootstrap y una sola memoria interna global compacta. Context Retrieval y toda memoria de dominio son lazy/scoped y entran sólo cuando la pregunta requiere una entidad del vault. La continuidad usa un slot activo por `continuity_key`, actualizado en lugar de acumular checkpoints; memorias superseded/archived quedan fuera del retrieval normal. El catálogo está en `80-agents/skills/INDEX.md`; bootstrap decide qué skill principal cargar.

## Estructura

```text
10-projects/                  proyectos y control
20-areas/                     áreas
30-resources/                 wiki curada de recursos
70-templates/                 templates Sistema 2
80-agents/agents-os/          guía + constitución
80-agents/memory/public/      memoria compartida
80-agents/memory/internal/    continuidad privada
80-agents/skills/             procedimientos canónicos
80-agents/journal/            auditoría, sesiones y feedback
```

## Persistencia Y Cierre

Cambios canónicos dejan un único `change_log`. La memoria interna se actualiza
solo ante delta durable. El cierre completo ocurre únicamente por pedido
explícito y lo ejecuta `agents-os-session-close`: persiste por delta y reporta
por defecto solo resultado y próximo paso. Feedback es event-driven.

## Proyectos De Agente

Un proyecto `owner: agent` vive bajo `agentes/`, declara `parent` y usa su nota
como planificador único. El proyecto padre conserva una sola tarea puente
humana. El procedimiento vive en
`agents-os-agent-project-workflow/SKILL.md`.
