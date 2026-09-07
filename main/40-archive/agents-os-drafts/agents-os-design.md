---
type: doc
status: draft
tags:
  - kind/doc
  - kind/system
  - tech/agents-os
created: 2026-06-27
updated: 2026-06-27
aliases:
  - AGENTS OS
  - Agent Memory System
---

# AGENTS OS — Análisis y Diseño

> [!abstract]+ Qué es este documento
> Análisis y **diseño** del *AGENTS OS*: el sistema de **memoria y aprendizaje para agentes** montado sobre este vault de Obsidian + Graphify.
> **No** son las reglas operativas (la "constitución" del agente). Esto explica el problema, la visión, la arquitectura, los flujos, las decisiones y lo que falta decidir, para que un humano o **otra IA** entiendan el proyecto sin huecos.

## Estado

`draft` · beta operativa en hardening. La **Capa 1** (documentación/entidades) ya está implementada en el vault; la **Capa 2** (memoria del agente) ya tiene estructura, templates, memoria always-load y skills locales en uso.

## Idea en una frase

> No quiero que el agente recuerde todo. Quiero que **recupere lo importante, en el momento correcto, con el menor costo posible** — y que, mientras más lo use, mejor entienda mis necesidades, prioridades y problemas en **todos mis ámbitos**.

## El quiebre central: dos sistemas, un vault

Este es el concepto que ordena todo el proyecto. Conviven **dos sistemas distintos** dentro del mismo vault:

1. **Capa 1 — Documentación (entidades reales).** Describe **qué son** las cosas de trabajo/vida: proyectos, aplicaciones, áreas, servicios, conceptos. Es la **fuente de verdad**, para humano y agente. *Ya construida.*
2. **Capa 2 — Memoria del agente (AGENTS OS).** No describe qué es una cosa, sino **cómo el usuario y los agentes han interactuado con ella**: aprendizajes, memorias de uso, preferencias, y las reglas de cómo el agente debe **generar y consumir** información a lo largo del tiempo.

La Capa 2 **se monta sobre** la Capa 1: la memoria **siempre cuelga de una entidad real vía link**, nunca la duplica ni la ensucia. **Graphify** es el índice derivado que recorre lo indexable de ambas capas para retrieval barato.

```text
Capa 1 (Documentación)  = qué es algo            → fuente de verdad
Capa 2 (Memoria agente) = cómo se ha trabajado   → aprendizaje del agente
Graphify                = índice derivado         → retrieval barato
Reindex + higienización = proceso aparte          → mantenimiento
```

## Documentos de este set

- [[01-problema-y-vision]] — por qué existe y qué resuelve.
- [[02-arquitectura]] — las dos capas, niveles de memoria (L0–L4), componentes y roles.
- [[03-flujos]] — cierre de sesión, inicio/retrieval, conflicto, higienización.
- [[04-principios-y-decisiones]] — principios duros, decisiones tomadas y descartadas.
- [[05-preguntas-abiertas]] — qué está decidido y qué falta.
- [[06-glosario]] — términos del sistema.
- [[07-skills-y-tareas]] — backlog y drafts de skills para operar el AGENTS OS.

## Avances a la fecha (2026-06-27)

**Ya existe en el vault (base sobre la que se construye):**

- Estructura PARA numerada (`00-inbox` … `95-graphify`).
- **Entidades de Capa 1**: áreas (11), proyectos con subproyectos, **aplicaciones** (`30-resources/applications/`, `type: application` con github/path/stack), sprints y quarters (`10-projects/_planning/`).
- **Convenciones** de tareas en `90-system/convenciones.md`: estados (`To Do/WIP/Review/Done/Canceled`), tipos (`#type/dev|admin|research|pr-review`), tags de contexto (`#area/ #sprint/ #quarter/`).
- **Graphify** instalado como CLI de macOS del usuario (`graphify`, `graphify-personal`, `graphify-obsidian`); outputs en `95-graphify/`.
- `80-agents/AGENTS.md`: reglas iniciales de trabajo del agente + draft del sistema de memoria.

**Decidido en la fase de diseño (esta conversación):** ver [[04-principios-y-decisiones]] y [[05-preguntas-abiertas]].

**Fase 0 cerrada (2026-06-27):**

- Beta sobre proyectos Meli: [[java-polycard-sdk]], [[search-middleware]], [[vis-octopus-lib]], [[vpp-backend]].
- Memoria centralizada en `80-agents/memory/`:
  - `public/` para memoria pública auditable.
  - `internal/` para memoria interna indexable y de carga preferente/always-load.
- Journal separado en `80-agents/journal/` para raw sessions, summaries si se usan y logs.
- Sin `status` en memorias: lo obsoleto se elimina o reemplaza con log.
- Conflictos resueltos por el agente con log auditable, no consulta humana obligatoria.
- Graphify del vault: `graphify-obsidian`; watcher fuera de beta.
- Validación con Codex, Claude, Cursor y Antigravity.

**Implementado en Fase 1 y Fase 2:**

- Contratos compartidos en `80-agents/skills/_shared/`:
  - `metadata-schema.md`;
  - `note-types.md`;
  - `graphify-contract.md`;
  - `skill-contract.md`.
- Estructura física inicial:
  - `80-agents/memory/public/`;
  - `80-agents/memory/internal/`;
  - `80-agents/journal/sessions/raw/`;
  - `80-agents/journal/logs/`;
  - `80-agents/templates/`.
- Templates mínimos para L0/L1/L3/log/constitution/user-preference.
- Memoria always-load inicial:
  - `80-agents/memory/public/constitution/agent-constitution.md`;
  - `80-agents/memory/public/user-preference/rjara-agent-profile.md`.
- `.graphifyignore` beta con exclusiones de journal/raw/scratch/evidencia pesada.

**Pendiente aún:** forward-test de `agents-os-session-close` con transcript real, beta end-to-end con proyecto real, validación con Claude/Cursor/Antigravity y reporte de medición beta.

**Adaptadores creados:** `80-agents/adapters/` documenta el contrato operativo para Codex, Claude, Cursor y Antigravity. `SKILL.md` sigue siendo la fuente canónica; los adaptadores solo definen carga inicial, Graphify/retrieval, edición y modo degradado por superficie.

**Drafts creados:** set inicial de skills en `80-agents/skills/` para bootstrap, retrieval, cierre de sesión, destilación, updates de entidades, conflictos, Graphify, higiene y retrofit.
