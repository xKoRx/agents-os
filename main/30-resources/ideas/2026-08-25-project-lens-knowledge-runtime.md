---
type: idea
schema_version: 1
status: seed
priority: P3
area: "[[Personal]]"
project:
application:
entities:
  - "[[AGENTS OS]]"
related: []
visibility: public
governed_by: user
promotion_target: project
source: Propuesta de arquitectura Project Lens (revisión externa 2026-08-24)
aliases:
  - Project Lens
  - Lens Core
  - knowledge runtime del vault
tags:
  - kind/idea
  - area/personal
  - idea/opportunity
  - size/large
created: "2026-08-25"
updated: "2026-08-25"
---

# 💡 Project Lens — Knowledge Runtime del vault

> [!tip]+ De viewer a knowledge runtime
> _Idea en bruto. Estados: seed → exploring → promoted → discarded. Si madura, promover a proyecto, tarea o aprendizaje._

## 🧠 La idea

- Construir **Project Lens**: un runtime de conocimiento local en Go que convierte el vault Markdown en un grafo estructurado y consultable por humanos y agentes, manteniendo Markdown como única fuente de verdad. No es "otro Obsidian": es una proyección consultable del second brain con interfaces intercambiables.
- Arquitectura en capas con dependencias hacia adentro: `Markdown vault → Scan/Parse (Goldmark + frontmatter) → Lens Core (syntax model ≠ semantic model) → proyección SQLite derivada y descartable (relacional + FTS5) → Application API → adapters (HTTP/SPA, MCP, CLI/export)`.
- El Core no sabe que existe una UI: corre como CLI (`lens index|serve|query|mcp|export`). Si la UI envejece, se bota la UI sin botar Project Lens.
- Dos modelos separados: **Syntax Model** (lo que existe físicamente en Markdown: Document, headings, wikilinks, embeds, block refs, tags, tasks, frontmatter) y **Semantic Model** (lo que significan: Project, Area, Resource, Task, Decision…). Cambiar la semántica de `type:` no toca el parser.
- SQLite desde el día 1 como read projection derivada (`rm lens.db && lens rebuild` no pierde nada), con invariancia obligatoria: rebuild completo == incremental, mismo estado semántico.
- Query engine nativo con query model tipado primero (`ProjectQuery`, `TaskQuery`); rescatar la semántica de los bloques Dataview/Bases actuales sin implementar DataviewJS ni el engine de Bases. LensQL diferido.
- **Context Bundles** como feature clave: `lens.get_context("Echo Forge")` devuelve identidad, estado, tareas, decisiones, cambios recientes, relaciones y documentos fuente; cualquier agente consume eso vía MCP en vez de hacer grep del vault.
- Watcher (`fsnotify`) es optimización, no autoridad: scan completo = correctness; watcher + debounce = incremental; reconciliación periódica posible.
- MCP como adapter read-only desde temprano (`lens.search`, `lens.get_document`, `lens.list_projects`, `lens.query_tasks`, `lens.get_backlinks`, `lens.build_context`), conversando naturalmente con [[AGENTS OS]].
- Stack: Go puro + Goldmark (AST CommonMark con extensiones para sintaxis Obsidian; regex sólo dentro de nodos concretos) + fsnotify + SQLite. Sin Kafka/Temporal (single user, local, read-heavy, rebuildable); Wails diferido porque v3 sigue en alpha.

## 🎯 Motivo / por qué

- MELI restringió Obsidian en el trabajo; esto recupera el valor perdido (projects/tasks/backlinks/search) sin clonarlo visualmente ni saltarse políticas: opera por canales permitidos (local/navegador/snapshot estático).
- El índice persistente resuelve media arquitectura: búsquedas FTS5, backlinks, queries relacionales y consumo por agentes sobre una proyección reconstruible.
- Hoy cada agente entiende el vault haciendo grep ad-hoc; un Context Bundle convierte eso en una API de conocimiento determinista y barata.
- North Star propuesta: "Project Lens convierte un vault Markdown en un grafo de conocimiento estructurado, consultable y consumible por humanos y agentes, manteniendo Markdown como única fuente de verdad."

## ❄️ Decisiones arquitectónicas propuestas (F0 — Architecture Freeze)

- ADR-001 Markdown is the authority · ADR-002 derived SQLite projection · ADR-003 Syntax Model ≠ Semantic Model · ADR-004 Core has no UI/transports · ADR-005 native query engine, no ejecución Dataview · ADR-006 MCP is an adapter · ADR-007 read-only v1 · ADR-008 local security model (bind 127.0.0.1, sin remote `0.0.0.0`, CSP, sandbox al vault, path traversal/symlinks) · ADR-009 deployment adapters · ADR-010 identity model explícito (`VaultID`, `DocumentID`, `EntityID`, `TaskID`; no dejar identidad implícita en filenames).

## 🗺️ Roadmap propuesto

- **F0** Architecture Freeze (ADRs arriba) → **F1** Lens Core (scanner, parser AST, wikilinks, resolver, backlinks, entidades semánticas; corpus `testdata/vault/`) → **F2** SQLite Projection (tablas documents/entities/tasks/links/tags/relations + FTS5 + migraciones; tests de invariancia rebuild) → **F3** Query Engine (`GetDocument`, `Search`, `ListProjects`, `GetProject`, `QueryTasks`, `GetBacklinks`, `GetRelated`, `GetRecentChanges`) → **F4** HTTP + UI usable (`/api/v1/*`, SPA embebida `go:embed`: explorer, viewer, dashboard projects, board tasks, search, backlinks) → **F5** MCP adapter → **F6** static export / snapshot mode (`lens export`) → futuro: **F7** desktop adapter (Wails u otro) y **F8** mutations (CQRS chico: comando → patch determinista de Markdown → reindex).
- Recomendación de la revisión: arrancar fuerte por **F0 → F3**; UI/MCP/desktop pasan a accesorios si esas capas quedan impecables.

## 🚫 No implementar

- DataviewJS runtime, evaluator JS, plugin APIs de Obsidian ni compatibilidad 1:1 con Bases.
- Regex como parser principal del documento.
- Kafka/Temporal/NATS o cualquier pieza distribuida.
- Remote mode sin autenticación explícita (`--host 0.0.0.0` prohibido por defecto).
- Mutaciones write antes de F8.

## Señales para promover

Promover a proyecto si ocurre al menos una:

1. El owner decide comprometer la ejecución formal de F0–F3 como iniciativa multi-sesión.
2. La restricción de Obsidian en Meli bloquea flujo real de trabajo y se necesita el reemplazo operativo.
3. [[AGENTS OS]] requiere contexto estructurado del vault vía MCP más allá de grep/Graphify.

No promover sólo porque "podría ser útil".

## 🧭 Routing

- **Área:** [[Personal]]
- **Proyecto:** — (sin proyecto aún; promotion_target: project)
- **Aplicación:** —
- **Entidades:** [[AGENTS OS]]

## 🏷️ Clasificación

- **Tamaño:** large.
- **Tipo:** opportunity.
- **Prioridad:** P3.
- **Estado:** seed.
- **Visibilidad:** public.
- **Gobernada por:** user.
- **Criterio de promoción:** decisión explícita del owner de arrancar F0 (Architecture Freeze) y ejecutar F1–F3 como proyecto formal.

## 🔗 Relacionado

- [[AGENTS OS]] — consumidor natural vía MCP adapter y Context Bundles.

## 🌱 Próximo paso

- [ ] Decidir promoción a proyecto y, si procede, abrir ciclo F0 (redactar ADR-001…ADR-010 y estructura de repo) #owner/me #type/research #area/personal
