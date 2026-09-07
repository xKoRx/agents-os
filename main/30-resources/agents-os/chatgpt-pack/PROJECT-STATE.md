---
type: context_pack
schema_version: 1
status: snapshot
area: "[[Personal]]"
project: "[[AGENTS OS]]"
entities:
  - "[[AGENTS OS]]"
related:
  - "[[AGENTS OS - Fase 3]]"
  - "[[agents-os]]"
  - "[[context-router]]"
aliases:
  - AGENTS OS ChatGPT project state
created: 2026-07-11
updated: 2026-08-10
snapshot_date: 2026-08-10
source_of_truth: false
tags:
  - kind/context-pack
  - project/agents-os
---

# AGENTS OS — Estado para iteración externa

> [!warning] Snapshot derivado
> Este documento orienta, pero no reemplaza las fuentes canónicas incluidas en
> `sources/`. Ante una contradicción, manda Markdown canónico.

## Propósito

Orientar una iteración externa con un snapshot verificable del estado activo de AGENTS OS.

## Jerarquía de autoridad

Markdown canónico manda; este snapshot, el manifest, los outputs y Graphify son derivados.

## Estado ejecutivo

La iteración activa es [[AGENTS OS - Fase 3]]. F0–F3 están aceptadas: `30-resources/agents/` es la home de assets portables, las tres skills portables viven bajo `agents/skills/`, `type: prompt` tiene contrato/template/fixture y las dos skills app-owned pendientes se migraron sin copia a `xKoRx/symphony/.agents/skills/`.

G3 está `accepted`; F4 quedó habilitada sin iniciar y T4.1 es el próximo paso exacto: diseñar la proyección de metadata y facets. El gate aceptado se apoya en source único, registry/packs actualizados, hashes, lint/Doctor/Graphify y forward-test de core, portable y app-owned.

## Arquitectura vigente

```text
AGENTS.md
  └── agents-os-bootstrap
      ├── cold / warm / cambio de entidad
      ├── Context Retrieval
      └── una skill especializada

Sistema 1: 80-agents/{agents-os,memory,skills,journal,templates}
Sistema 2: 10-projects, 20-areas, 30-resources, apps/repos
Derivados: Graphify y outputs del pack
```

- Markdown es fuente de verdad; Graphify es índice derivado.
- Bootstrap es la única máquina de startup.
- Las skills tienen una sola fuente y un registry federado.
- Sistema 1 y Sistema 2 tienen contratos separados y lint determinístico.
- Resource Wiki mantiene conocimiento curado; specs concretas quedan en sus
  proyectos o repositorios.

## Gates

| Gate | Estado | Resultado |
|---|---|---|
| G0 | accepted | baseline reproducible |
| G1 | accepted | autoridades y doctor coherentes |
| G2 | accepted | skills por ownership y discovery federado |
| G3 | accepted | topología Resources/agents, ownership, prompts, packs y discovery |
| G4 | pending | Graphify metadata-aware |
| G5 | pending | Context Router metadata→grafo→body |
| G6 | pending | retrofit, segundo piloto y gate estricto |

## Fuentes

- `sources/80-agents/agents-os/agents-os.md`
- `sources/80-agents/agents-os/agent-constitution.md`
- `sources/80-agents/skills/_shared/`
- `sources/80-agents/skills/agents-os-*/`
- `sources/30-resources/agents/`
- `sources/10-projects/Personal/AGENTS OS/AGENTS OS.md`
- `sources/10-projects/Personal/AGENTS OS/agentes/AGENTS OS - Fase 3.md`
- `sources/30-resources/methodologies/sdd/`

## Preguntas útiles para una iteración externa

1. ¿Las fuentes canónicas sostienen la arquitectura y el estado declarado?
2. ¿La topología `30-resources/agents/` preserva ownership, discovery y economía de tokens?
3. ¿Qué diseño de proyección de metadata y facets debe cerrar T4.1 antes de implementar?
4. ¿Qué deuda debe quedar explícita para Graphify metadata-aware y el strict gate final?
