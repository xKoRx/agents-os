---
type: change_log
scope: global
created: 2026-07-02
area: "[[Personal]]"
project: "[[AGENTS OS]]"
entities:
  - "[[AGENTS OS]]"
related:
  - "[[agent-constitution]]"
  - "[[graphify]]"
tags:
  - kind/changelog
  - area/personal
  - project/agents-os
---

# 2026-07-02 — Resource Wiki (piloto) + Graphify corpus purge + Constitución

## Motivo

Formalizar el patrón *LLM Wiki* dentro de `30-resources/` (wiki compilada e
incremental) conviviendo con Graphify como índice derivado, y depurar el corpus de
Graphify que estaba devolviendo resultados basura.

## Cambios canónicos / públicos

### Constitución (`agent-constitution.md`) — `updated` 2026-07-01 → 2026-07-02
- **Reglas Base**: nueva regla "Wiki compilada de recursos" — `30-resources/` opera
  como LLM Wiki; páginas Sistema 2 desde template; `00-index.md` + `log.md`; Graphify
  = índice derivado; no confundir wiki curada con `--wiki` derivado de Graphify.
- **Mandamientos de Memoria Interna**: nuevo mandamiento **16** — toda sesión debe
  ejecutar al menos una acción (crear/modificar/deprecar) sobre
  `80-agents/memory/internal/`.

### Templates
- Nuevo `70-templates/index.md` (`type: index`) — requerido por regla dura de Sistema 2
  para páginas `00-index.md`.

### Skills
- Nueva skill `agents-os-resource-wiki` (ingest/query/lint de la resource wiki).
- Registrada en `80-agents/skills/INDEX.md`.

### Runbook
- Nuevo `80-agents/memory/public/runbook/resource-wiki-lint-reindex.md` — parte
  mecánica (reindex + purga de corpus + validación de índice/huérfanos). La skill lo invoca.

### Sistema 2 / recursos
- Nuevo `30-resources/00-RESOURCE-WIKI.md` — schema/reglas de la wiki.
- Piloto `30-resources/applications/00-index.md` (11 apps, datos reales) + `log.md`.
  **No se modificó ninguna página canónica de app.**

### Graphify (índice derivado, no requiere log pero se documenta)
- `.graphifyignore` ampliado: excluye `trash/**`, `**/*.json`, `95-graphify/**`,
  `graphify-out/**`, `**/GRAPH_REPORT.md`, `**/graph.json`, `**/graph.html`.

## Evidencia (auditoría del grafo 2026-07-02, 3806 nodos)
- 512 nodos desde `trash/` (no excluido) + 170 desde un `*.json` schema + 190 desde
  `40-archive/` pese a estar ignorado (nodos stale no purgados por update incremental).
- `_origin` 100% `ast`: sin capa semántica → queries devolvían tokens de heading.

## Desenlace del retrieval (2026-07-03)
- Se exploró encender la capa semántica de Graphify (`extract --mode deep`).
  Resultado: **descartado**. deepseek-r1 local da calidad pobre (nodos sin label,
  edges alucinados); el free tier de Gemini no alcanza (`gemini-2.0-flash` quota 0,
  `gemini-3-flash` 5 req/min → 7 chunks del vault caen por 429).
- **Decisión del owner: operar SOLO con índices.** Retrieval primario = `00-index.md`
  curado; Graphify en modo `update` (AST, gratis) como índice estructural. La capa
  semántica queda parqueada (solo con billing si algún día se justifica).
- `GEMINI_API_KEY` removida de `~/.zshrc` (backup `.zshrc.bak-*`).
- Grafo AST reconstruido y purgado: **3163 nodos** (desde 3806), `trash=0/archive=0/json=0`.
- Corrección registrada: `--mode deep` es de `extract`, NO de `update`.

## Validación
- Constitución, template, skill, runbook, schema doc, índice y log creados/editados.
- Graphify AST limpio y verificado. Retrieval por índices operativo.
